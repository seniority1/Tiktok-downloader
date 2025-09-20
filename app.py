from flask import Flask, request, render_template_string, send_file
import requests
import io

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>TikTok Downloader</title>
</head>
<body style="font-family:sans-serif; text-align:center; margin-top:50px;">
  <h1>TikTok Downloader (No Watermark)</h1>
  <form method="POST">
    <input name="url" placeholder="Paste TikTok link here" style="width:60%;padding:10px;">
    <button type="submit" style="padding:10px;">Download</button>
  </form>
  {% if error %}
    <p style="color:red;">{{ error }}</p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tiktok_url = request.form.get("url")
        try:
            video_id = tiktok_url.split("/")[-1]
            headers = {"User-Agent": "Mozilla/5.0"}
            api_url = f"https://www.tiktok.com/api/item/detail/?itemId={video_id}"
            resp = requests.get(api_url, headers=headers).json()
            video_info = resp["itemInfo"]["itemStruct"]["video"]
            play_url = video_info.get("playAddr", None)
            if not play_url:
                return render_template_string(HTML, error="Could not find video URL")
            video_data = requests.get(play_url, headers=headers).content
            return send_file(
                io.BytesIO(video_data),
                as_attachment=True,
                download_name="tiktok.mp4",
                mimetype="video/mp4"
            )
        except Exception as e:
            return render_template_string(HTML, error=f"Error: {str(e)}")
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
