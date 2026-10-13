# 매일 구글 드라이브 폴더의 최신 data-*.json을 받아 catylang-ads_1.html의 숫자를 바꾼다
import json, re, urllib.request
FOLDER = '10BNeswBYXAR7nDmtDuQcAx9GAQYJmR7O'
PAGE = 'catylang-ads_1.html'
def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8')
listing = fetch('https://drive.google.com/embeddedfolderview?id=' + FOLDER)
files = re.findall(r'/file/d/([\w-]+)/view.*?flip-entry-title">([^<]+)<', listing, re.S)
files = sorted((n.strip(), i) for i, n in files if n.strip().startswith('data-'))
if not files:
    raise SystemExit('드라이브 폴더에서 data 파일을 못 찾음')
name, fid = files[-1]
data = json.loads(fetch('https://drive.google.com/uc?export=download&id=' + fid))
html = open(PAGE, encoding='utf-8').read()
new = re.sub(r'var DATA=.*?;\n', lambda m: 'var DATA=' + json.dumps(data, ensure_ascii=False) + ';\n', html, count=1)
open(PAGE, 'w', encoding='utf-8').write(new)
print(name, '반영' if new != html else '변경 없음')
