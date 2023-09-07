#!/usr/bin/python
# -*- coding:utf-8 -*-

from typing import List,Dict
import re

import requests as rq
from urllib.parse import urlparse, quote



HEADERS={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
        }
HOMEPAGE = "https://www.hifini.com/"

def search_music(music_name: str)->List[Dict]:
    search_name_url_encode = quote(music_name)
    search_url = HOMEPAGE + "search-" + search_name_url_encode + "-1.htm"
    resp = rq.get(search_url, headers=HEADERS)
    if(resp.ok):
        match_str = r'<a href="(thread-\d+.htm)">(.+)</a>'
        matches = re.findall(match_str, resp.text)
        if(len(matches) > 0):
            ll = []
            for group in matches:
                url = HOMEPAGE + group[0]
                title = group[1].replace("<em>", "").replace(r"</em>", "").replace("amp;", "")
                ll.append({"url" : url, "title" : title})
            return ll
        return None
    else:
        return None

def download_music(url: str, save_path: str)->bool:
    resp = rq.get(url, headers=HEADERS)
    if(resp.ok):
        match_str = r"title:\s*'(.*)',\s*author:\s*'(.*)',\s*url:\s*'(.*)'"
        match = re.search(match_str, resp.text)
        if(match):
            title = match.group(1)
            author = match.group(2)
            music_url = match.group(3)
            if(music_url[:4] != "http"):
                music_url = HOMEPAGE + music_url
            music = rq.get(music_url, headers=HEADERS)
            if(music.ok):
                music_type = urlparse(music.url).path[-3:]
                full_path = save_path + title + "-" + author + "." + music_type
                with open(full_path, 'wb') as f:
                    for chunk in music.iter_content(chunk_size=8192):
                        f.write(chunk)
                        return True
    return False