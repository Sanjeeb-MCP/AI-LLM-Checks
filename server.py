from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scrapling.fetchers import StealthyFetcher
import uvicorn

app = FastAPI()

# Allow CORS so our local HTML file can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fetch")
def fetch_html(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    print(f"Fetching URL with Scrapling StealthyFetcher: {url}")
    try:
        # Scrapling's StealthyFetcher bypasses anti-bot like Cloudflare
        # network_idle=True waits for JS and network requests to settle
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
        
        # Prioritize body or html_content, fallback to text
        html_content = getattr(page, 'body', None) or getattr(page, 'html_content', None) or getattr(page, 'text', None)
        return {"contents": html_content}
        
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scrapling fetch failed: {str(e)}")

if __name__ == "__main__":
    print("Starting Scrapling Proxy Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
