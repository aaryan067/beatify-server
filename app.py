from flask import Flask, jsonify, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "Beatify Stream Server Running"})

@app.route('/stream')
def get_stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "No video ID"}), 400
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'noplaylist': True,
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                "https://www.youtube.com/watch?v=" + video_id, download=False)
            url = info.get('url')
            if not url and info.get('formats'):
                url = info['formats'][-1]['url']
            return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
