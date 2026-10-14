# 매일 구글 드라이브 폴더의 최신 data-*.json을 받아 catylang-ads_1.html의 숫자를 바꾼다
# img-<키>.jpg 파일이 있으면 소재 썸네일로 넣는다
import base64, json, re, urllib.request
FOLDER = '10BNeswBYXAR7nDmtDuQcAx9GAQYJmR7O'
PAGE = 'catylang-ads_1.html'
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=60).read()
def fetch(url):
    return get(url).decode('utf-8')
listing = fetch('https://drive.google.com/embeddedfolderview?id=' + FOLDER)
allf = [(n.strip(), i) for i, n in re.findall(r'/file/d/([\w-]+)/view.*?flip-entry-title">([^<]+)<', listing, re.S)]
files = sorted(f for f in allf if f[0].startswith('data-'))
if not files:
    raise SystemExit('드라이브 폴더에서 data 파일을 못 찾음')
name, fid = files[-1]
data = json.loads(fetch('https://drive.google.com/uc?export=download&id=' + fid))
html = open(PAGE, encoding='utf-8').read()
new = re.sub(r'var DATA=.*?;\n', lambda m: 'var DATA=' + json.dumps(data, ensure_ascii=False) + ';\n', html, count=1)
if 'white-space: pre-line' not in new:
    new = new.replace('.cs-lead { font-size', '.cs-lead { white-space: pre-line; font-size', 1)
for n, i in allf:
    m = re.match(r'img-([\w-]+)\.jpg$', n)
    if not m:
        continue
    key = m.group(1)
    if "'" + key + "': 'data:" in new:
        continue
    b64 = base64.b64encode(get('https://drive.google.com/uc?export=download&id=' + i)).decode()
    new = new.replace('IMG = { ', "IMG = { '" + key + "': 'data:image/jpeg;base64," + b64 + "', ", 1)
    new = re.sub(r'(const IMGK = \{[^}]*?)\s*\}', lambda mm: mm.group(1) + ', ' + key + ": IMG['" + key + "'] }", new, count=1)
    print('썸네일 추가:', key)
open(PAGE, 'w', encoding='utf-8').write(new)
print(name, '반영' if new != html else '변경 없음')
