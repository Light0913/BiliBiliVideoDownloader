'''
作者: Light_LE
开源协议: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
'''

# 导入数据请求模块
import requests
# 导入正则表达式模块
import re
# 导入json模块
import json
# 导入os模块
import os
# 导入datetime模块
import datetime

# 用于合并视频和音频
def merge_video_audio(title, video_path, audio_path) :
    output_path = ".\\video_and_audio\\" + title + ".mp4"

    # 删除已存在的文件
    if os.path.exists(output_path) :
        os.remove(output_path)
    if os.path.exists(".\\video_and_audio\\merged.mp4") :
        os.remove(".\\video_and_audio\\merged.mp4")

    # 使用ffmpeg命令合并视频和音频
    # 执行命令
    os.system(f".\\ffmpeg.exe -i {video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental .\\video_and_audio\\merged.mp4")

    if not os.path.exists(".\\video_and_audio\\merged.mp4") :
        print(get_current_time(), "\033[31m音视频合并失败\033[0m")
        os.system("pause")
        os._exit(1)

    os.rename(".\\video_and_audio\\merged.mp4", output_path)
# 获取当前时间
def get_current_time() :
    return "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"

url = ""
cookie = ""
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"

# 初始化
def init() :
    os.system("title B站视频下载器")

    os.makedirs(".\\video_and_audio", exist_ok = True)
    os.makedirs(".\\log", exist_ok = True)

    # 检查 ffmpeg 是否安装
    if not os.path.exists(".\\ffmpeg.exe") :
        print(get_current_time(), "\033[31m未找到 ./ffmpeg.exe\033[0m")
        os.system("pause")
        os._exit(1)

    # 检查 request.json 是否存在
    if not os.path.exists(".\\request.json") :
        with open(".\\request.json", mode = "w", encoding = "utf-8") as f :
            f.write('{\n    "url": "", \n    "cookie": "", \n    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"\n}')

        print(get_current_time(), "\033[31m未找到 ./request.json, 已自动创建\033[0m")
        os.system("pause")
        os._exit(1)
    
    # 读取 request.json
    global url, cookie, user_agent
    with open(".\\request.json", mode = "r", encoding = "utf-8") as f :
        request_json = json.load(f)
        
    if request_json["url"] == "" :
        print(get_current_time(), "\033[31m请先在 ./request.json 里输入请求网址 url\033[0m")
        os.system("pause")
        os._exit(1)
    if request_json["user_agent"] == "" :
        print(get_current_time(), "\033[31m请先在 ./request.json 里输入用户代理 user_agent\033[0m")
        os.system("pause")
        os._exit(1)

    url = request_json["url"]
    cookie = request_json["cookie"]
    user_agent = request_json["user_agent"]
    


### 程序从这里开始执行
# 初始化
def main():
    print(get_current_time(), "开始初始化")
    init()
    print(get_current_time(), "\033[32m初始化完成\033[0m")

    # 定义请求头
    global url, cookie, user_agent
    headers = {
        # Referer 防盗链, 告诉服务器你请求链接是从哪里跳转过来的
        # "Referer": "https://www.bilibili.com/video/BV1454y187Er/",
        "Referer": url,
        # User-Agent 用户代理, 表示浏览器/设备基本身份信息
        "User-Agent": user_agent,
        # Cookie 用户登录信息
        "Cookie": cookie
    }
    # 发送请求
    print(get_current_time(), "开始发送请求")
    try:
        response = requests.get(url = url, headers = headers)
    except Exception as e :
        print(get_current_time(), "\033[31m请求发送失败\033[0m")
        print(get_current_time(), "\033[31m错误信息:", e, "\033[0m")
        os.system("pause")
        os._exit(1)
    print(get_current_time(), "\033[32m请求发送成功\033[0m")

    html = response.text
    with open(".\\log\\request.html", mode = "w", encoding = "utf-8") as f :
        f.write(html)

    # 提取视频信息
    title = re.findall('title="(.*?)"', html)[0]
    info = re.findall("window.__playinfo__=(.*?)</script>", html)[0]
    with open(".\\log\\info.json", mode = "w", encoding = "utf-8") as f :
        f.write(info)
    # info -> json字符串转成json字典
    json_data = json.loads(info)

    # 提取视频链接
    video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
    with open (".\\log\\video_url.txt", mode = "w", encoding = "utf-8") as f :
        f.write(video_url)
    # 提取音频链接
    audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
    with open (".\\log\\audio_url.txt", mode = "w", encoding = "utf-8") as f :
        f.write(audio_url)

    # 获取视频内容
    print(get_current_time(), "开始下载视频")
    try:
        video_content = requests.get(url = video_url, headers = headers).content
    except Exception as e :
        print(get_current_time(), "\033[31m视频下载失败\033[0m")
        print(get_current_time(), "\033[31m错误信息:", e, "\033[0m")
        os.system("pause")
        os._exit(1)
    print(get_current_time(), "\033[32m视频下载完成\033[0m")

    # 获取音频内容
    print(get_current_time(), "开始下载音频")
    try:
        audio_content = requests.get(url = audio_url, headers = headers).content
    except Exception as e :
        print(get_current_time(), "\033[31m音频下载失败\033[0m")
        print(get_current_time(), "\033[31m错误信息:", e, "\033[0m")
        os.system("pause")
        os._exit(1)
    print(get_current_time(), "\033[32m音频下载完成\033[0m")

    # 保存数据
    video_path = ".\\video_and_audio\\video.mp4"
    with open(video_path, mode = "wb") as v :
        v.write(video_content)
    audio_path = ".\\video_and_audio\\audio.mp3"
    with open(audio_path, mode = "wb") as a :
        a.write(audio_content)

    # 合并音视频
    print(get_current_time(), "开始合并音视频")
    merge_video_audio(title, video_path, audio_path)
    print(get_current_time(), "\033[32m音视频合并完成\033[0m")

    print()
    print(get_current_time(), "\033[32mDone! 所有操作已完成!\033[0m")
    os.system("pause")
    os._exit(0)

if __name__ == "__main__" :
    main()