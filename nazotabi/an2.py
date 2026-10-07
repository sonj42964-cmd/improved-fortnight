import csv,re,json,statistics as S,collections as C
from datetime import datetime
import sys,os;os.chdir(sys.argv[1])
R=list(csv.DictReader(open("videos.csv",encoding="utf-8-sig")))
def dur(d):
    m=re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",d);h,mi,s=[int(x or 0) for x in m.groups()];return h*3600+mi*60+s
for r in R:
    r["v"]=int(r["views"]);r["l"]=int(r["likes"]);r["c"]=int(r["comments"]);r["d"]=dur(r["duration"]);r["t"]=datetime.fromisoformat(r["published"].replace("Z","+00:00"))
R.sort(key=lambda r:r["t"])
print("영상",len(R),"기간",R[0]["t"].date(),"~",R[-1]["t"].date())
vs=[r["v"] for r in R];print("조회수 평균",int(S.mean(vs)),"중앙값",int(S.median(vs)),"최대",max(vs),"최소",min(vs))
print("분위 10/25/75/90",[int(x) for x in S.quantiles(vs,n=20)[1::5][:1]+S.quantiles(vs,n=4)[::2]+S.quantiles(vs,n=10)[-1:]])
ds=[r["d"] for r in R];print("길이 평균(분)",round(S.mean(ds)/60,1),"중앙값",round(S.median(ds)/60,1),"최단",min(ds),"초 최장",round(max(ds)/60,1),"분")
print("60초 이하",sum(d<=60 for d in ds),"1~5분",sum(60<d<=300 for d in ds),"5~10분",sum(300<d<=600 for d in ds),"10분+",sum(d>600 for d in ds))
print("좋아요율 평균%",round(S.mean(r["l"]/r["v"]*100 for r in R if r["v"]),2),"댓글/천뷰",round(S.mean(r["c"]/r["v"]*1000 for r in R if r["v"]),2))
yc=C.defaultdict(list)
for r in R:yc[r["t"].year].append(r)
for y,l in sorted(yc.items()):print(y,len(l),"편 평균조회",int(S.mean(x["v"] for x in l)),"중앙",int(S.median(x["v"] for x in l)),"평균길이분",round(S.mean(x["d"] for x in l)/60,1))
print("요일",C.Counter(r["t"].astimezone().strftime("%a") for r in R))
from datetime import timezone,timedelta
K=timezone(timedelta(hours=9));print("KST요일",C.Counter(r["t"].astimezone(K).strftime("%a") for r in R));print("KST시",C.Counter(r["t"].astimezone(K).hour for r in R).most_common(5))
g=[(R[i]["t"]-R[i-1]["t"]).days for i in range(1,len(R))];print("업로드 간격 일 중앙",S.median(g),"평균",round(S.mean(g),1),"최대",max(g))
last=[r for r in R if r["t"]>=R[-1]["t"]-timedelta(days=180)];print("최근180일",len(last),"편 평균조회",int(S.mean(x["v"] for x in last)))
print("\nTOP15");[print(r["v"],r["t"].date(),round(r["d"]/60,1),r["title"]) for r in sorted(R,key=lambda r:-r["v"])[:15]]
print("\nBOTTOM10");[print(r["v"],r["t"].date(),round(r["d"]/60,1),r["title"]) for r in sorted(R,key=lambda r:r["v"])[:10]]
print("\n최근10");[print(r["v"],r["t"].date(),round(r["d"]/60,1),r["title"]) for r in R[-10:]]
tl=[len(r["title"]) for r in R];print("\n제목길이 평균",round(S.mean(tl),1))
print("물음표",sum("?" in r["title"] for r in R),"숫자",sum(bool(re.search(r"\d",r["title"])) for r in R),"괄호",sum(bool(re.search(r"[\[\(]",r["title"])) for r in R))
w=C.Counter(x for r in R for x in re.findall(r"[가-힣A-Za-z0-9]{2,}",r["title"]));print(w.most_common(40))
tg=C.Counter(t for r in R for t in r["tags"].split("|") if t);print("태그",tg.most_common(15),"태그있는영상",sum(bool(r["tags"]) for r in R))
print(open("playlists.json").read())
