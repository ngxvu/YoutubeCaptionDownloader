from flask import Flask, request, jsonify, send_file
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import tempfile
import re
import os

app = Flask(__name__)

def get_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    matches = re.findall(regex, url)
    return matches[0] if matches else url

@app.route("/api/get-caption", methods=["POST"])
def get_caption():
    data = request.json
    if not data or "link" not in data:
        return jsonify({"error": "Missing 'link' in request body"}), 400

    link = data["link"]
    languages = data.get("languages", ["en"])

    video_id = get_video_id(link)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 400
    except NoTranscriptFound:
        return jsonify({"error": f"No transcript found for languages: {languages}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    text = "\n".join([item["text"] for item in transcript])

    # Ghi ra file tạm thời
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".txt") as f:
        f.write(text)
        temp_filename = f.name

    # Trả về file txt cho client tải về
    response = send_file(temp_filename, mimetype="text/plain", as_attachment=True, download_name=f"{video_id}_caption.txt")
    # Xóa file tạm sau khi gửi xong
    @response.call_on_close
    def cleanup():
        try:
            os.remove(temp_filename)
        except Exception:
            pass

    return response

if __name__ == "__main__":
    app.run(debug=True)