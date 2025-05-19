# ![YouTube Caption Downloader](https://img.shields.io/badge/-red?logo=youtube) YouTube Caption Downloader API
# **A simple Flask API to download and summarize YouTube video captions as plain text.**

## Features

- Download YouTube captions (subtitles) as `.txt` via API.
- Supports multiple languages.
- Summarize any text using a state-of-the-art transformer model.

## Installation

1. Clone this repository.
2. Install dependencies (Python 3.7+):

   ```bash
   pip3 install flask youtube-transcript-api
   ```
**Note:** If you have multiple Python versions, use `pip3` and `python3` for Python 3.7+.

## Usage

### 1. Run the application:
   ```bash
   python app.py
   ```
### 2. Get Captions: 
**The API will return a JSON with the video ID and captions.**

Send a POST request to /api/get-caption with a JSON body:

```
{
  "link": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID",
  "languages": ["en"]
}
```

- link: YouTube video URL or ID (required)
- languages: List of language codes (optional, default: ["vi", "en"])

### 3. Summarize Text
**The API will return a summary and token information.**

Send a POST request to /api/summarize with a JSON body:
   ```
{
  "text": "Your text to summarize here"
}
   ```

### 4. Example using curl
**Get Captions:**
```
curl -X POST http://localhost:5000/api/get-caption \
     -H "Content-Type: application/json" \
     -d '{"link": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}'
```
**Summarize Text:**
```
curl -X POST http://localhost:5000/api/summarize \
     -H "Content-Type: application/json" \
     -d '{"text": "Paste your text here"}'
```

## 📚 Source & Credits
[![Model: facebook/bart-large-cnn](https://img.shields.io/badge/model-facebook%2Fbart--large--cnn-blueviolet)](https://huggingface.co/facebook/bart-large-cnn)
[![youtube-transcript-api](https://img.shields.io/badge/youtube--transcript--api-v0.6.1-orange)](https://github.com/jdepoix/youtube-transcript-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

