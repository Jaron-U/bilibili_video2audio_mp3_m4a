# b站视频转存为MP3和M4A
A python script to download Bilibili video's audio stream and cover image.  
This script can convert the audio stream to `.mp3` and `.m4a` format.

无需调用API,通过爬虫方法获取视频的音频流，然后下载保存为`.mp3`和`.m4a`格式。并且获取视频的封面图。

`.m4a`格式可以方便导入到Apple Music中。并且可以通过调整方法`convert_mp3_to_m4a`中的`bitrate`来调整音质。  
常见的bitrate有：128, 192, 256, 512。越高音质越好，文件越大。 

直接为.m4a格式文件添加metadata信息，包含封面图，标题，艺术家，专辑等信息。支持一键导入到Apple Music。

需要先下载FFmpeg并配置环境变量。

```shell
pip install requests
pip install mutagen

python video2audio.py

# 输入视频url
```