#NZBScout Crawler
This is a crawler for the popular Website https://nzbscout.com.
I have built it mainly for integration with Radarr.

It is more like a quick and dirty approach than a good tested software.
Sometimes it won´t work for some items because it's reliability depends on the details of the post on NZBScout.

It uses multiple threads to download the NZBs concurrently. 
But because of the crawling and downloading it is much slower than already indexed sites.
It searches all Pages. And I can't guarantee that you don't get blocked from NZBScout.
Currently, it seems to work fine for me. If i see that there will be blocking I will attempt to code workarounds for it.


# Features
| Implemented | Tested | Name         | Description                                                                                          |
|-------------|--------|--------------|------------------------------------------------------------------------------------------------------|
| [x]         | [x]    | Newznab API  | You can add it to Prowlarr and NZBHydra2 or directly to Radarr and Sonarr and get the results there. |
| [x]         | [x]    | Movie Search | You can search for all Movies. Subcategories currently not supported.                                |
| [x]         | []     | TV Search    | Add shows and series to Sonarr. Not tested at all.                                                   |
| []          | []     | Audio        | Add songs to Lidarr. Not even implemented.                                                           | 

Feel free to create a issue or for the Repository if you have Problems.