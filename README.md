# AI-LLM-Checks

An AI Citation Readiness Audit tool that analyzes any URL and scores how well its content will be read, parsed, and cited by AI crawlers (Gemini, ChatGPT, Claude, Perplexity).

## What It Does

- **Structure** — heading hierarchy, declarative sentences, H1/title alignment
- **Payload** — robots meta tags blocking AI crawlers, HTML bloat vs. useful text ratio
- **Schema** — presence and quality of JSON-LD structured data
- **Accessibility** — fragment-anchor heavy TOCs, JavaScript content dependency

Produces a composite score (0–100), per-engine scores, estimated LLM token costs per crawl, and projected monthly inference billing at 10k and 100k page volumes.

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright browser binaries (required by Scrapling's StealthyFetcher)

```bash
playwright install chromium
```

### 3. Start the proxy server

```bash
python server.py
```

The server runs at `http://127.0.0.1:8000`.

### 4. Open the frontend

Open `index.html` directly in your browser (no build step needed).

## Usage

Enter any URL in the input field and click **Audit**. The tool fetches the page via the local proxy server (which uses a headless browser to render JavaScript-heavy pages), then analyzes the rendered HTML and displays the results.

> **Note:** The server must be running for the primary fetch to work. The frontend falls back to public CORS proxies (`allorigins.win`, `corsproxy.io`) if the local server is unavailable, but these proxies may not render JavaScript.

## Demo Mode

A yellow **Demo Mode** banner appears when you audit one of the pre-loaded benchmark domains (`vantagecircle.com`, `octanner.com`, `workhuman.com`, `achievers.com`). These domains display pre-authored results from manually audited PDF reports rather than a live computation. Enter any other URL to get a live audit.

## Architecture

```
index.html      Single-page frontend (HTML + CSS + JS, no build tooling)
server.py       FastAPI proxy — fetches URLs via Scrapling StealthyFetcher
requirements.txt  Python dependencies
```

## Security Notes

- The proxy server only accepts `http://` and `https://` URLs and blocks requests to private/internal IP ranges (127.x, 10.x, 172.16–31.x, 192.168.x, 169.254.x).
- Do not expose `server.py` on a public network — it is intended for local use only.
