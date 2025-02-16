# b站视频转存为MP3和M4A

无需调用API,通过爬虫方法获取视频的音频流，然后下载保存为MP3和M4A格式。并且获取视频的封面图。

M4A格式可以方便导入到Apple Music中。并且可以通过调整方法`convert_mp3_to_m4a`中的`bitrate`来调整音质。  
常见的bitrate有：128, 192, 256, 512。越高音质越好，文件越大。  

需要先下载FFmpeg并配置环境变量。

```shell
pip install requests

python video2audio.py

# 输入视频url
```