class Item:

    def __init__(self, url, nzb_url, title, description, length, language, posted, file_size,
                 files, group, category, newznab_category1):
        self.url = url
        self.nzb_url = nzb_url
        self.title = title
        self.description = description
        self.length = length
        self.language = language
        self.posted = posted
        self.file_size = file_size
        self.category = category
        self.files = files
        self.group = group
        self.newznab_category1 = newznab_category1


remove_urls = ["/movies", "/movies/bluray", "/movies/3d", "/movies/sd", "/movies/foreign", "/movies/hd", "/movies/uhd",
               "javascript:;", "/tv", "/tv/sd", "/tv/hd", "/tv/uhd", "/tv/sport", "/tv/foreign", "/tv/documentary",
               "/tv/anime", "/audio", "/audio/video", "/audio/lossless", "/audio/mp3", "/audio/audiobook", "/books",
               "/books/ebook", "/books/comics", "/books/mags", "/games", "/games/psp", "/games/nds", "/games/nsw",
               "/games/ps3", "/games/ps4", "/games/wii", "/games/wiiware", "/games/xbox360dlc", "/games/xbox360",
               "/games/switch", "/games/xbox", "/games/pc"]

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
