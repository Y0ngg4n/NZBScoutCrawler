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

caps = """<?xml version="1.0" encoding="UTF-8"?>
  <caps>
    <!-- server information -->
    <server version="1.0" title="Newznab" strapline="A great usenet indexer"
            email="info@newznab.com" url="http://servername.com/"
            image="http://servername.com/theme/black/images/banner.jpg"/>

    <!-- limit parameter range -->
    <limits max="100" default="50"/>

    <!-- the server NZB retention -->
    <retention days="400"/>

    <!-- registration available or not -->
    <registration available="yes" open="yes" />

    <!--
         The search functions available at the server
         The only currently defined search functions are SEARCH and TV-SEARCH.
         Any conforming implementation should at least support the basic search.
         Other search functions are optional.
    -->
    <searching>
        <search available="yes"/>
        <tv-search available="yes"/>
        <movie-search available="yes"/>
    </searching>

    <!-- supported categories -->
    <categories>
        <category id="2000" name="Movies">
            <subcat id="2060" name="3D"/>
            <subcat id="2050" name="BluRay"/>
            <subcat id="2010" name="Foreign"/>
            <subcat id="2040" name="HD"/>
            <subcat id="2020" name="Other" description="Other"/>
            <subcat id="2030" name="SD"/>
            <subcat id="2045" name="UHD"/>
        </category>
        <category id="3000" name="Audio ">
            <subcat id="3030" name="Books" description="Books"/>
            <subcat id="3040" name="Lossless"/>
            <subcat id="3010" name="MP3"/>
            <subcat id="3020" name="Video"/>
        </category>
        <category id="5000" name="TV">
            <subcat id="5070" name="Anime"/>
            <subcat id="5080" name="Doc"/>
            <subcat id="5020" name="Foreign"/>
            <subcat id="5040" name="HD"/>
            <subcat id="5050" name="Other "/>
            <subcat id="5030" name="SD"/>
            <subcat id="5060" name="Sport"/>
            <subcat id="5045" name="UHD"/>
        </category>
    </categories>
  </caps>"""

@app.get("/api/")
async def api(t: str, apikey: str, q: str, rcache: ResponseCache = cache_manager.from_request()):
    if rcache.exists():
        print("Cache hit!")
        return rcache.data

    if t == "caps":
        return Response(content=caps, media_type="application/xml")

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