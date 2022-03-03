from fastapi import FastAPI, Response, HTTPException
import os
from search import Search
from fastapi_caching import CacheManager, InMemoryBackend, ResponseCache
from dotenv import load_dotenv
app = FastAPI()

cache_backend = InMemoryBackend()
cache_manager = CacheManager(cache_backend)

load_dotenv()  # take environment variables from .env.

@app.get("/")
async def root():
    return {"message": "NZBScoutCrawler"}


@app.get("/api/")
async def api(t: str, apikey: str, q: str, rcache: ResponseCache = cache_manager.from_request()):
    if rcache.exists():
        print("Cache hit!")
        return rcache.data
    print(os.getenv("API_KEY"))
    if apikey != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Wrong API Key")

    xml = await Search.search(q, t)

    response = Response(content=xml, media_type="application/xml")
    await rcache.set(response, tag="api")
    return response



@app.get("/__admin/reset/cache")
async def reset_cache():
    await cache_backend.reset()
    return {"ok": True}