import os, json, csv, urllib.request, urllib.parse
import sys
K=os.environ["YOUTUBE_API_KEY"]; H=sys.argv[1]
os.makedirs(sys.argv[2],exist_ok=True); os.chdir(sys.argv[2])
def api(ep, **p):
    p["key"]=K
    with urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/{ep}?"+urllib.parse.urlencode(p)) as r:
        return json.load(r)
ch=api("channels",part="snippet,statistics,contentDetails,brandingSettings,status",forHandle=H)["items"][0]; CH=ch["id"]
json.dump(ch,open("channel.json","w"),ensure_ascii=False,indent=1)
up=ch["contentDetails"]["relatedPlaylists"]["uploads"]
ids=[];tok=None
while True:
    d=api("playlistItems",part="contentDetails",playlistId=up,maxResults=50,**({"pageToken":tok} if tok else {}))
    ids+=[i["contentDetails"]["videoId"] for i in d["items"]]
    tok=d.get("nextPageToken")
    if not tok: break
rows=[]
for i in range(0,len(ids),50):
    for v in api("videos",part="snippet,statistics,contentDetails",id=",".join(ids[i:i+50]))["items"]:
        s,st=v["snippet"],v.get("statistics",{})
        rows.append(dict(id=v["id"],title=s["title"],published=s["publishedAt"],duration=v["contentDetails"]["duration"],
          views=st.get("viewCount",0),likes=st.get("likeCount",0),comments=st.get("commentCount",0),
          tags="|".join(s.get("tags",[])),desc=s.get("description","")[:200].replace("\n"," ")))
w=csv.DictWriter(open("videos.csv","w",newline="",encoding="utf-8-sig"),fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
pls=[];tok=None
while True:
    d=api("playlists",part="snippet,contentDetails",channelId=CH,maxResults=50,**({"pageToken":tok} if tok else {}))
    pls+=[dict(title=i["snippet"]["title"],count=i["contentDetails"]["itemCount"]) for i in d["items"]]
    tok=d.get("nextPageToken")
    if not tok: break
json.dump(pls,open("playlists.json","w"),ensure_ascii=False,indent=1)
print(ch["snippet"]["title"],ch["snippet"]["publishedAt"],ch["statistics"],len(rows),"videos",len(pls),"playlists")
print(ch["snippet"].get("description","")[:500]); print(ch["brandingSettings"].get("channel",{}).get("keywords"))
