## 代码来源：https://developer.aliyun.com/article/1639947

import requests
import json
import re
import os
import subprocess
from pprint import pprint 

"""获取url响应体"""
def getResponse(url):
    # 设置请求头
    headers = {
        'referer': 'https://www.bilibili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    # 发起get请求
    response = requests.get(url=url, headers=headers)
    return response

"""解析响应体"""
def parseResponse(url):
    # 获取url响应体
    response = getResponse(url)

    # 用正则表达式取出返回的视频数据
    html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)[0]
    # 解析成json数据
    jsonData = json.loads(html_data)
    # 获取视频标题
    videoTitle = re.findall('<title data-vue-meta="true">(.*?)</title>', response.text)[0]

    # 获取音频
    audioUrl = jsonData['data']['dash']['audio'][0]['baseUrl']
    # 获取视频
    videoUrl = jsonData['data']['dash']['video'][0]['baseUrl']
    # 封装视频信息
    videoInfo = {
   
        'videoTitle': videoTitle,
        'audioUrl': audioUrl,
        'videoUrl': videoUrl,
    }
    print("获取Response信息成功！")
    return videoInfo

"""保存视频和音频"""
def saveMedia(fileName, content, mediaType, folderName):
    # 创建目录（如果不存在）
    os.makedirs(f'bilibili/{folderName}', exist_ok=True)
    # 写入文件
    with open(f'bilibili/{folderName}/{fileName}.{mediaType}', mode='wb') as f:
        f.write(content)
    print(f"保存{mediaType}成功！")

"""将mp3文件转换为m4a文件"""
def convert_mp3_to_m4a(mp3_file, m4a_file, bitrate):
    command = ['ffmpeg', '-i', mp3_file, '-c:a', 'aac', '-b:a', bitrate, m4a_file]
    subprocess.call(command)
    print(f"转换mp3文件为m4a文件成功！")

def extract_bv_id(url):
    """
    从B站视频URL中提取BV号
    """
    # 使用正则表达式匹配BV号
    match = re.search(r"(BV\w+)", url)
    if match:
        return match.group(1)  # 返回匹配到的BV号
    return None

def get_cover_image(bv_id, folderName):
    """
    根据BV号获取封面图并下载
    """
    # B站API地址
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"

    try:
        # 发送请求获取视频信息
        response = getResponse(api_url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        # 提取封面图URL
        if data['code'] == 0:  # 确保返回的数据是成功的
            cover_url = data['data']['pic']
            print(f"封面图URL: {cover_url}")
            
            # 下载封面图
            download_image(cover_url, bv_id, folderName)
        else:
            print("无法获取视频信息，请检查BV号是否正确！")
    except Exception as e:
        print(f"发生错误: {e}")

def download_image(url, bv_id, folderName):
    """
    下载封面图并保存到本地
    """
    try:
        # 创建保存图片的目录
        os.makedirs(f"bilibili/{folderName}", exist_ok=True)

        # 下载图片
        response = requests.get(url)
        response.raise_for_status()
        
        # 保存图片到本地
        file_path = f"bilibili/{folderName}/{bv_id}.jpg"
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"封面图已保存到: {file_path}")
    except Exception as e:
        print(f"下载封面图失败: {e}")

def main():
    url = input("请输入B站视频url地址:")
    videoInfo = parseResponse(url)
    # 获取视频标题
    fileName = videoInfo['videoTitle']
    # 提取BV号
    bv_id = extract_bv_id(url)
    # 创建文件夹
    folderName = re.sub(r'[\\/*?:"<>|]', "", fileName) # 去除标题中的非法字符
    # 下载并保存音频
    audioContent = getResponse(videoInfo['audioUrl']).content
    saveMedia(fileName, audioContent, 'mp3', folderName)
    # 转换音频格式
    mp3_file = f'bilibili/{folderName}/{fileName}.mp3'
    m4a_file = f'bilibili/{folderName}/{fileName}.m4a'
    convert_mp3_to_m4a(mp3_file, m4a_file, '192k')
    # 下载封面
    get_cover_image(bv_id, folderName)

if __name__ == '__main__':
    main()