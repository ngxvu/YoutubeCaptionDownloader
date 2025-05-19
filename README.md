# ![YouTube Caption Downloader](https://img.shields.io/badge/-red?logo=youtube) YouTube Caption Downloader API

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green?logo=flask)](https://flask.palletsprojects.com/)
[![youtube-transcript-api](https://img.shields.io/badge/youtube--transcript--api-v0.6.1-orange)](https://github.com/jdepoix/youtube-transcript-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# **A simple Flask API to download YouTube video captions (subtitles) as a `.txt` file.**
## Installation

1. Clone this repository.
2. Install dependencies (Python 3.7+):

   ```bash
   pip3 install flask youtube-transcript-api
   ```
**Note:** If you have multiple Python versions, use `pip3` and `python3` for Python 3.7+.

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. Send a POST request to `/api/get-caption` with a JSON body:

   ```json
   {
     "link": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID",
     "languages": ["en"]
   }
   ```

   - `link`: YouTube video URL or ID (**required**)
   - `languages`: List of language codes (optional, default: `["en"]`)

The API will return a `.txt` file containing the captions.


### Example using `curl`

```bash
curl -X POST http://localhost:5000/api/get-caption \
     -H "Content-Type: application/json" \
     -d '{"link": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}' --output captions.txt
```

## 📚 Source & Credits

[![youtube-transcript-api](https://img.shields.io/badge/youtube--transcript--api-MIT%20License-orange)](https://github.com/jdepoix/youtube-transcript-api)