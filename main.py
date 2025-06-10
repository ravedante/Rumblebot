from flask import Flask, Response
import requests
import re
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor Rumble Proxy está online."

@app.route("/rumble/<video_id>")
def rumble_proxy(video_id):
    try:
        url = f"https://rumble.com/embed/{video_id}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(url, headers=headers)
        m3u8_match = re.search(r'"(https://.*?\.m3u8.*?)"', r.text)

        if not m3u8_match:
            return "Vídeo não encontrado ou Rumble bloqueou.", 404

        m3u8_url = m3u8_match.group(1)
        html = f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Rumble Proxy</title>
                <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            </head>
            <body style="margin:0;background:#000;">
                <video id="video" controls autoplay style="width:100%;height:auto;">
                    <source type="application/x-mpegURL" src="{m3u8_url}">
                </video>
                <script>
                    var video = document.getElementById('video');
                    if (Hls.isSupported()) {{
                        var hls = new Hls();
                        hls.loadSource("{m3u8_url}");
                        hls.attachMedia(video);
                    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                        video.src = "{m3u8_url}";
                    }}
                </script>
            </body>
        </html>
        """
        return Response(html, mimetype="text/html")

    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
