# b站视频转存为MP3和M4A

无需调用API,通过爬虫方法获取视频的音频流，然后下载保存为MP3和M4A格式。并且获取视频的封面图。

需要先下载FFmpeg并配置环境变量。

```shell
pip install requests

python video2audio.py

# 输入视频url
```