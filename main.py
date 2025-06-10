from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/rumble/<video_id>')
def rumble_proxy(video_id):
    video_url = f"https://rumble.com/embed/{video_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=10)
        return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get("Content-Type"))
    except Exception as e:
        return f"Erro: {str(e)}", 500