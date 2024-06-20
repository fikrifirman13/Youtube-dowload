from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pytube import Playlist
import yt_dlp
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Path untuk menyimpan file yang didownload
output_path = r'\\192.168.3.6\New Volume\00.FOLDER FIKRI\ALL Lagu\NEW MUSIC'

# Path ke ffmpeg
ffmpeg_path = 'C:\PATH_Programs'  # Ganti dengan path ke ffmpeg Anda

# Pastikan direktori output ada
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Fungsi untuk mendownload video sebagai audio
def download_audio(video_url, socketio):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': 'C:\PATH_Programs',  # Menambahkan  
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        socketio.emit('update', f"Downloaded and converted: {video_url}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_download')
def handle_start_download(playlist_url):
    playlist = Playlist(playlist_url)
    for video_url in playlist.video_urls:
        try:
            download_audio(video_url, socketio)
        except Exception as e:
            socketio.emit('update', f"Error downloading {video_url}: {e}")
    socketio.emit('finished')

if __name__ == '__main__':
    socketio.run(app, debug=True)
