import os
import requests
from googleapiclient.discovery import build

# 读取链接文件中的音乐名
def read_music_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# 使用YouTube Data API根据音乐名称搜索视频
def search_youtube(song_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        q=song_name,
        type='video',
        maxResults=1  # 获取第一个结果
    )
    try:
        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            print(f"没有找到与 {song_name} 相关的YouTube视频")
            return None
    except Exception as e:
        print(f"搜索YouTube时出错: {e}")
        return None

# 调用Cobalt API并下载文件
def download_from_cobalt(link, save_dir):
    api_url = "http://localhost:9000/"  # Cobalt API 实例的地址
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # 构建请求体
    data = {
        "url": link,
        "videoQuality": "1080",  # 视频质量
        "audioFormat": "mp3",    # 音频格式
        "downloadMode": "auto"   # 下载模式
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        print(f"API 返回的响应: {response.text}")
        response_data = response.json()

        if response_data["status"] in ["tunnel", "redirect"]:
            # 获取下载链接
            download_url = response_data["url"]
            file_name = response_data.get("filename", "downloaded_file")

            # 下载文件并保存
            download_response = requests.get(download_url)
            file_path = os.path.join(save_dir, file_name)

            with open(file_path, 'wb') as file:
                file.write(download_response.content)

            print(f"成功下载: {file_name} (来自 {link})")
        else:
            print(f"下载失败 {link}: {response_data.get('message', '未知错误')}")
    except Exception as e:
        print(f"处理链接失败 {link}: {e}")

# 主程序
def main():
    # 文件路径和API密钥
    link_file = "E:/mu/new.txt"
    save_dir = "E:/mu/new"
    youtube_api_key = "AIzaSyALoOCTen--aghhNGks-5Il3P1GwPauecY"  # 替换为你的YouTube Data API Key

    # 确保保存目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 读取音乐名称
    music_names = read_music_names(link_file)

    # 逐个处理每个音乐名称
    for song in music_names:
        print(f"正在处理: {song}")
        # 使用YouTube Data API搜索视频
        youtube_link = search_youtube(song, youtube_api_key)
        
        if youtube_link:
            print(f"找到视频链接: {youtube_link}")
            # 调用Cobalt API下载
            download_from_cobalt(youtube_link, save_dir)
        else:
            print(f"没有找到 {song} 的视频")

if __name__ == "__main__":
    main()
