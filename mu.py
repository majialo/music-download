import os
import time
from googleapiclient.discovery import build
from googleapiclient.discovery import build
import time

# 读取歌曲列表文件
def read_song_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# 使用YouTube Data API进行搜索
def search_youtube(song_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        q=song_name,
        type='video',
        maxResults=1  # 获取一个结果来减少API调用次数
    )
    try:
        response = request.execute()
    except Exception as e:
        print(f"查询 {song_name} 时出现错误: {e}")
        return None

    # 获取第一个视频的链接
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return None

# 保存链接到文件
def save_links(links, save_path):
    with open(save_path, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')

# 主程序
def main():
    # 设置 API Key
    api_key = "AIzaSyA90Uyp0oOfTXUC4PP6K3N_0tUVAAcYWKc"  # 替换为你的API Key
    time.sleep(1)
    # 歌曲列表文件路径
    song_list_file = os.path.join(os.path.dirname(__file__), "mu.txt") # 替换为你的文件路径
    # 保存YouTube链接的文件
    save_file = os.path.join(os.path.dirname(__file__), "new.txt")

    # 读取歌曲列表
    songs = read_song_list(song_list_file)

    # 搜索每首歌并获取链接
    links = []
    for song in songs:
        link = search_youtube(song, api_key)
        if link:
            links.append(link)
            print(f"找到 {song} 的链接: {link}")
        else:
            print(f"没有找到 {song} 的视频")
        time.sleep(1)  # 每次查询后等待1秒，防止快速超出API配额

    # 保存所有链接到文件
    save_links(links, save_file)
    print(f"已保存所有视频链接到 {save_file}")

if __name__ == "__main__":
    main()

