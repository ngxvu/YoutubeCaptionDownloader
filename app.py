from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

max_input_tokens = getattr(model.config, "max_position_embeddings", None)
if max_input_tokens is None:
    max_input_tokens = 1024

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
    languages = data.get("languages", ["vi", "en"])

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
    return jsonify({
        "video_id": video_id,
        "caption": text
    })


@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    tokens = tokenizer.encode(text)
    num_tokens = len(tokens)

    if num_tokens > max_input_tokens:
        return jsonify({
            "error": f"Văn bản bạn nhập có {num_tokens} tokens, vượt quá giới hạn {max_input_tokens} tokens của model {model_name}. Hãy chia nhỏ văn bản trước khi tóm tắt."
        }), 400

    try:
        result = summarizer(text, max_length=max_input_tokens, min_length=40, do_sample=False)
        summary = result[0]['summary_text']
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "summary": summary,
        "num_tokens": num_tokens,
        "max_input_tokens": max_input_tokens
    })

if __name__ == "__main__":
    app.run(debug=True)