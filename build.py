# -*- coding: utf-8 -*-
"""내 연봉 10억 만들기 — 정적 페이지 빌드 스크립트.
python3 build.py 실행 시 index.html 과 하위 폴더 index.html 을 전부 새로 씁니다.
(부분 수정 금지 원칙: 매번 파일 전체를 다시 생성)"""
import json, os, datetime

UPDATED = "2026-10-10"
SITE = "내 연봉 10억 만들기"

CSS = r"""
:root{
  --bg:#f6f4ef; --card:#ffffff; --ink:#1f2328; --muted:#6b7280; --line:#e6e2d8;
  --accent:#0f6e56; --accent-soft:#dff3ea; --gold:#b7791f; --gold-soft:#fbf1dc;
  --red:#b42318; --red-soft:#fde8e6; --blue:#1d4ed8; --blue-soft:#e3ebfd;
  --shadow:0 1px 2px rgba(0,0,0,.05),0 6px 20px rgba(0,0,0,.05);
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#121414; --card:#1c1f21; --ink:#ececec; --muted:#9aa3ad; --line:#2d3235;
    --accent:#4fd1a5; --accent-soft:#12312a; --gold:#e3b04b; --gold-soft:#3a2d12;
    --red:#ff7b6e; --red-soft:#3d1a17; --blue:#8fb0ff; --blue-soft:#1b2a4d;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 6px 20px rgba(0,0,0,.35);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans KR","Gowun Dodum",system-ui,-apple-system,sans-serif;line-height:1.6;font-size:16px}
.wrap{max-width:600px;margin:0 auto;padding:20px 16px 64px}
h1,h2,h3{font-family:"Gowun Dodum","Noto Sans KR",sans-serif;line-height:1.3;margin:0}
h1{font-size:26px;letter-spacing:-.01em}
h2{font-size:19px;margin:28px 0 12px;display:flex;align-items:baseline;gap:8px}
h2 small{font-size:13px;color:var(--muted);font-weight:400}
h3{font-size:16px;margin:0 0 6px}
p{margin:0 0 10px}
a{color:var(--accent);text-decoration:none}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;font-size:13px;color:var(--muted)}
.top a{color:var(--muted)}
.hero{background:linear-gradient(135deg,var(--accent) 0%,#134e3f 100%);color:#fff;border-radius:18px;padding:22px 20px;box-shadow:var(--shadow)}
.hero h1{color:#fff}
.hero .sub{opacity:.9;margin-top:6px;font-size:14px}
.hero .goal{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}
.hero .goal div{background:rgba(255,255,255,.14);border-radius:12px;padding:10px 12px;flex:1;min-width:130px}
.hero .goal b{display:block;font-size:20px;font-family:"Gowun Dodum",sans-serif}
.hero .goal span{font-size:12px;opacity:.9}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:var(--shadow);margin-bottom:12px}
.card.accent{border-color:var(--accent);background:var(--accent-soft)}
.card.gold{border-color:var(--gold);background:var(--gold-soft)}
.card.blue{border-color:var(--blue);background:var(--blue-soft)}
.sky{background:radial-gradient(ellipse at 50% 16%,#17323a 0%,#0e1a22 52%,#080d12 100%);border:1px solid var(--line);border-radius:16px;padding:8px 4px 4px;box-shadow:var(--shadow);margin-bottom:12px;overflow:hidden}
.sky svg{display:block;width:100%;height:auto}
.legend{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:-4px 0 14px 2px}
.legend span{display:inline-flex;align-items:center;gap:5px}
.legend i{width:9px;height:9px;border-radius:50%;display:inline-block}
@keyframes luPulse{0%,100%{opacity:.22;transform:scale(1)}50%{opacity:.5;transform:scale(1.16)}}
@keyframes luTwinkle{0%,100%{opacity:.2}50%{opacity:.85}}
@keyframes luDash{to{stroke-dashoffset:-56}}
@keyframes luBreathe{0%,100%{opacity:.55}50%{opacity:1}}
.lu-halo{transform-origin:180px 330px;animation:luPulse 4.6s ease-in-out infinite}
.lu-star{animation:luTwinkle 3.4s ease-in-out infinite}
.lu-flow{stroke-dasharray:5 9;animation:luDash 2.8s linear infinite}
.pg{display:flex;gap:11px;align-items:flex-start}
.pg .pgn{flex:0 0 auto;width:52px;text-align:center;background:var(--accent);color:#fff;border-radius:12px;padding:7px 4px;font-family:"Gowun Dodum",sans-serif;line-height:1.15}
.pg .pgn b{display:block;font-size:21px}
.pg .pgn span{font-size:10px;opacity:.88;letter-spacing:.02em}
.pg .pgn.q{background:var(--gold)}
.pg .pgb{min-width:0;flex:1}
.pg h3{margin-bottom:2px}
.say{background:var(--accent-soft);border-left:3px solid var(--accent);border-radius:8px;padding:10px 12px;margin:9px 0 0;font-size:14.5px;line-height:1.75}
.say:before{content:"말할 것";display:block;font-size:11px;letter-spacing:.08em;color:var(--accent);margin-bottom:4px;font-weight:700}
.emph{font-size:13px;background:var(--gold-soft);border-left:3px solid var(--gold);padding:8px 10px;border-radius:6px;margin-top:8px}
.emph b{color:var(--gold)}
.tm{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.hd{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.qa{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 13px;margin-bottom:8px;box-shadow:var(--shadow)}
.qa summary{cursor:pointer;font-size:14px;font-weight:500}
.qa .a{font-size:13.5px;color:var(--muted);margin-top:9px}
.qa .a b{color:var(--ink)}
.skiprow{display:grid;grid-template-columns:52px 1fr;gap:6px 11px;font-size:13px;align-items:baseline}
.skiprow dt{text-align:center;color:var(--muted);font-family:"Gowun Dodum",sans-serif}
.skiprow dd{margin:0;color:var(--muted)}
.fb{font-size:13px;color:var(--muted);border-left:2px solid var(--line);padding-left:10px;margin:0 0 9px;line-height:1.62}
.fb b{color:var(--ink);font-weight:500}
.ba2{margin:9px 0 0;font-size:13.5px;display:grid;gap:5px}
.ba2 .b,.ba2 .a{padding:8px 10px;border-radius:8px;line-height:1.62}
.ba2 .b{background:var(--red-soft)}
.ba2 .a{background:var(--accent-soft)}
.ba2 .b:before{content:"수정 전";display:block;font-size:10.5px;font-weight:700;color:var(--red);margin-bottom:3px;letter-spacing:.06em}
.ba2 .a:before{content:"수정 후";display:block;font-size:10.5px;font-weight:700;color:var(--accent);margin-bottom:3px;letter-spacing:.06em}
.en{font-family:Georgia,"Times New Roman",serif;font-style:italic;font-size:12.5px;color:var(--muted)}
.why2{font-size:13.5px;margin-top:9px;line-height:1.68}
.why2:before{content:"왜";display:inline-block;font-size:10.5px;font-weight:700;color:var(--gold);background:var(--gold-soft);border-radius:4px;padding:1px 6px;margin-right:6px;vertical-align:1px}
.ov{display:grid;grid-template-columns:70px 1fr;gap:7px 10px;font-size:13.5px}
.ov dt{color:var(--muted);font-family:"Gowun Dodum",sans-serif}
.ov dd{margin:0}
.lu-spoke{stroke-dasharray:3 7;animation:luDash 5.2s linear infinite}
.lu-pflow{animation:luDash 9s linear infinite}
.lu-node{animation:luBreathe 3.8s ease-in-out infinite}
.lu-lab{paint-order:stroke;stroke:#0a1016;stroke-width:3px;stroke-linejoin:round}
.uni-hit{cursor:pointer}
.uni-reg{transition:opacity .25s}
.uni-nd.sel text{fill:#fff;font-weight:700}
.uni-nd.sel circle{stroke:#fff}
#uniPanel .tag{margin-right:6px}
.uniBar{display:flex;gap:6px;flex-wrap:wrap;margin:-4px 0 10px}
.uniBar button{font:inherit;font-size:13px;padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer;box-shadow:var(--shadow)}
.uniBar button.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
body.uni-wide .wrap{max-width:1240px}
body.uni-wide .uni-split{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:18px;align-items:start}
body.uni-wide .uni-right{position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto}
body.uni-wide #uniPanel{margin-bottom:0}
body.uni-wide .uniPossGrid{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}
@media (max-width:920px){body.uni-wide .wrap{max-width:600px}body.uni-wide .uni-split{display:block}body.uni-wide .uni-right{position:static;max-height:none}body.uni-wide .uniPossGrid{display:block}}
body.uni-full{overflow:hidden}
#uniStage.full{position:fixed;inset:0;z-index:9998;background:#070c11;display:block;margin:0}
#uniStage.full .uni-left{position:absolute;inset:0}
#uniStage.full .sky{position:absolute;inset:0;border:0;border-radius:0;margin:0;padding:0;box-shadow:none}
#uniStage.full .sky svg{width:100%;height:100%}
#uniStage.full .uniBar{position:absolute;top:10px;left:10px;right:10px;z-index:3;margin:0}
#uniStage.full .legend{position:absolute;left:12px;z-index:3;margin:0;background:rgba(8,14,20,.74);padding:6px 10px;border-radius:12px;color:#c7d3dc;max-width:min(620px,72vw)}
#uniStage.full #uniLeg{bottom:80px}
#uniStage.full .uniLeg2{bottom:10px}
#uniStage.full .legend a{color:#dfe9f0}
#uniStage.full .uni-right{position:absolute;top:58px;right:12px;width:380px;max-height:calc(100% - 76px);overflow:auto;z-index:4}
@media (max-width:760px){
 #uniStage.full .uni-right{left:8px;right:8px;width:auto;top:auto;bottom:0;max-height:60%}
 #uniStage.full .legend{display:none}
 #uniStage.full .uniBar{gap:5px}
 #uniStage.full .uniBar button{font-size:12px;padding:6px 10px}
}
.uniForm{position:fixed;inset:0;z-index:10000;background:rgba(4,8,12,.74);display:none;align-items:center;justify-content:center;padding:16px}
.uniForm.on{display:flex}
.uniForm .box{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;max-width:470px;width:100%;max-height:88vh;overflow:auto;box-shadow:var(--shadow)}
.uniForm label{display:block;font-size:13px;color:var(--muted);margin:12px 0 4px}
.uniForm input,.uniForm select,.uniForm textarea{width:100%;font:inherit;font-size:15px;padding:10px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.uniForm textarea{min-height:88px;resize:vertical}
.uniForm .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.uniForm .row button{flex:1;min-width:120px;font:inherit;font-size:14px;padding:10px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.uniForm .row button.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
@media (prefers-reduced-motion: reduce){.lu-halo,.lu-star,.lu-flow,.lu-spoke,.lu-node,.lu-pflow{animation:none}}
.card.red{border-color:var(--red);background:var(--red-soft)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media (max-width:420px){.grid{grid-template-columns:1fr}}
.nav a{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;color:var(--ink);box-shadow:var(--shadow)}
.nav a b{display:block;font-family:"Gowun Dodum",sans-serif;font-size:16px;margin-bottom:2px}
.nav a span{font-size:13px;color:var(--muted)}
.tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;background:var(--line);color:var(--ink);margin-right:4px;vertical-align:middle;white-space:nowrap}
.tag.p0{background:var(--red-soft);color:var(--red)}
.tag.p1{background:var(--gold-soft);color:var(--gold)}
.tag.p2{background:var(--blue-soft);color:var(--blue)}
.tag.p3{background:var(--line);color:var(--muted)}
.tag.cash{background:var(--accent-soft);color:var(--accent)}
.tag.done{background:var(--accent-soft);color:var(--accent)}
ul.list{list-style:none;padding:0;margin:0}
ul.list li{padding:10px 0;border-top:1px solid var(--line)}
ul.list li:first-child{border-top:0;padding-top:0}
ul.list li .t{font-weight:600}
ul.list li .m{font-size:13px;color:var(--muted);margin-top:2px}
.kv{display:grid;grid-template-columns:96px 1fr;gap:6px 10px;font-size:14px}
.kv dt{color:var(--muted)}
.kv dd{margin:0}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:500;font-size:12px}
td.num{text-align:right;white-space:nowrap;font-family:"Gowun Dodum",sans-serif;color:var(--accent);font-weight:700}
.wrapx{overflow-x:auto}
.note{font-size:13px;color:var(--muted);margin-top:8px}
.warn{font-size:13px;background:var(--gold-soft);color:var(--ink);border-left:3px solid var(--gold);padding:8px 10px;border-radius:6px;margin-top:8px}
.tl{position:relative;padding-left:18px;margin:0}
.tl:before{content:"";position:absolute;left:5px;top:6px;bottom:6px;width:2px;background:var(--line)}
.tl li{list-style:none;position:relative;padding:0 0 14px 0}
.tl li:before{content:"";position:absolute;left:-17px;top:7px;width:8px;height:8px;border-radius:50%;background:var(--accent);border:2px solid var(--card)}
.tl li.big:before{background:var(--gold)}
.tl .d{font-size:12px;color:var(--muted)}
.tl .t{font-weight:600}
.steps{display:flex;gap:6px;align-items:stretch;margin:8px 0}
.steps div{flex:1;background:var(--accent-soft);border-radius:10px;padding:8px;font-size:12px;text-align:center}
.steps div b{display:block;font-size:14px;font-family:"Gowun Dodum",sans-serif}
.bar{height:8px;background:var(--line);border-radius:4px;overflow:hidden;margin:6px 0}
.bar i{display:block;height:100%;background:var(--accent)}
ul.list li.chk{display:grid;grid-template-columns:24px 1fr;gap:8px;align-items:start}
ul.list li.chk input{width:20px;height:20px;margin:3px 0 0;accent-color:var(--accent)}
ul.list li.done .t{text-decoration:line-through;color:var(--muted)}
ul.list li.done{opacity:.55}
.nlink{font-size:12px;margin-left:6px;color:var(--blue)}
.btnrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.btn{font:inherit;font-size:13px;padding:8px 12px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.btn.pri{background:var(--accent);color:#fff;border-color:var(--accent)}
details.donebox{margin-top:10px}
details.donebox summary{cursor:pointer;font-size:13px;color:var(--muted)}
.foot{margin-top:28px;font-size:12px;color:var(--muted);text-align:center}
.src{font-size:12px;color:var(--muted)}
.src ul{padding-left:16px;margin:6px 0}
.today{font-family:"Gowun Dodum",sans-serif;font-size:14px;color:var(--muted)}
.empty{font-size:14px;color:var(--muted)}
.slots{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.slots div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 6px;font-size:12px;text-align:center}
.slots div b{display:block;font-family:"Gowun Dodum",sans-serif;font-size:13px;color:var(--accent)}
.week{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;font-size:11px;text-align:center}
.week div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 2px}
.week div b{display:block;font-size:13px;font-family:"Gowun Dodum",sans-serif}
.week div.on{border-color:var(--accent);background:var(--accent-soft)}
"""

HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title} — {site}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="wrap">
<div class="top"><a href="{root}">← {site}</a><span>갱신 {updated}</span></div>
<script>window.LUKE_ROOT="{root}";</script>
"""

FOOT = """
<div class="card donebox-wrap"><details class="donebox"><summary>완료</summary><ul class="list donelist" style="margin-top:8px"></ul></details>
<div class="btnrow"><button class="btn pri" onclick="luke1bCopy()">완료 목록 복사 → 클로드에 붙여넣기</button><button class="btn" onclick="luke1bClear()">체크 초기화</button></div>
<div class="note">체크는 이 기기에만 저장됩니다. 클로드에게 알리려면 '복사' 눌러 채팅에 붙여넣으면 노션 완료 처리 + 페이지 갱신이 됩니다. 노션 ↗ 링크가 있는 항목은 노션에서 직접 완료로 바꿔도 다음 갱신 때 반영됩니다.</div></div>
<div class="foot">{site} · 갱신 {updated} · <a href="{root}sources/">출처·갱신 방법</a></div>
</div>

<script>
(function(){
  const KEY='luke1b-done';
  const load=()=>{try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}};
  const save=o=>{try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}};
  const state=load();
  const slug=t=>t.replace(/\\s+/g,' ').trim().slice(0,60);
  function wire(li){
    if(li.dataset.wired) return; li.dataset.wired='1';
    const t=li.querySelector('.t'); if(!t) return;
    const id=li.dataset.g||li.dataset.id||slug(t.textContent);
    li.dataset.id=id; li.classList.add('chk');
    const cb=document.createElement('input'); cb.type='checkbox'; cb.checked=!!state[id];
    const body=document.createElement('div'); while(li.firstChild) body.appendChild(li.firstChild);
    if(li.dataset.g){const g=document.createElement('a');g.href=(window.LUKE_ROOT||'./')+'guides/'+li.dataset.g+'/';g.className='nlink';g.textContent='설명서 →';body.querySelector('.t').appendChild(g);}
    if(li.dataset.n){const a=document.createElement('a');a.href=li.dataset.n;a.target='_blank';a.className='nlink';a.textContent='노션 ↗';body.querySelector('.t').appendChild(a);}
    li.appendChild(cb); li.appendChild(body);
    const apply=()=>{li.classList.toggle('done',cb.checked)};
    apply();
    cb.addEventListener('change',()=>{ li.dataset.wired='1'; if(cb.checked) state[id]={t:t.textContent.replace('노션 ↗','').replace('설명서 →','').trim(),at:new Date().toISOString().slice(0,10)}; else delete state[id]; save(state); apply(); render(); });
  }
  function render(){
    document.querySelectorAll('ul.list.tasks li, ul.list li[data-g], ul.list li[data-n]').forEach(wire);
    document.querySelectorAll('.donebox').forEach(box=>{
      if(!box.querySelector('.donelist')) return;
      const items=Object.values(state).sort((a,b)=>a.at<b.at?1:-1);
      box.querySelector('summary').textContent='내가 체크한 완료 '+items.length+'건 (이 기기에 저장)';
      box.querySelector('.donelist').innerHTML=items.length?items.map(i=>'<li><span class="tag done">'+i.at.slice(5).replace('-','/')+'</span>'+i.t+'</li>').join(''):'<li class="empty">아직 없음</li>';
    });
  }
  window.luke1bCopy=function(){
    const items=Object.values(state).sort((a,b)=>a.at<b.at?-1:1);
    const txt=items.length?('아래 항목 완료 처리했어. 노션 액션보드 상태 완료로 바꾸고 10억 페이지 갱신해줘.\\n'+items.map(i=>'- ['+i.at+'] '+i.t).join('\\n')):'완료 체크한 항목이 없습니다.';
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>alert('복사됨. 클로드 채팅에 붙여넣으세요.')).catch(()=>prompt('복사해서 클로드에 붙여넣기',txt));
  };
  window.luke1bClear=function(){ if(confirm('체크 기록을 모두 지울까요? (노션은 안 바뀜)')){for(const k in state)delete state[k];save(state);render();} };
  document.addEventListener('DOMContentLoaded',render); if(document.readyState!=='loading') render();
})();
</script>
</body>
</html>
"""

# ---------------------------------------------------------------- 데이터
# 일정 데이터: 허브의 "오늘의 추천 일정"과 일정 페이지가 같이 씀
# 출처: 노션 '루크 액션보드'에서 상태가 시작 전/진행 중이고 기한이 있는 항목(완료 제외, '사업 외 개인' 목표 제외)
#       + 노션에 없는 회의 기한(물류·지영 등) + 플라우드 Action Item으로 새로 만든 항목.
# d=기한, t=할 일, who=담당, p=우선순위, n=노션 url, g=설명서 slug,
# cash=노션 목표가 '9월 현금 1000만' 또는 '월 3000~5000만 구조'
# 기한순 → P순 → 현금순 정렬. 수강생 이름은 기존에 페이지에 있던 분 외에는 가림.
EVENTS = [
  {"d":"2026-09-10","t":"박태경 대표 1회차 컨설팅(2시간) 진행","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea0481218d29ee843e1db28c","cash":True},
  {"d":"2026-09-10","t":"주 1개 공개 강의 업로드 유지","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04813d9cf3f40113eed719","cash":False},
  {"d":"2026-09-13","t":"블로그타이퍼 v1 실제 네이버 검증 — 사진 1장 글 발행 1회","who":"루크","p":"P0","n":"https://app.notion.com/p/3d80cf8fea04812c9ca9c0492f22db5f","cash":True},
  {"d":"2026-09-13","t":"디노 주간 운영 규칙 합의 — 등록 20개/일, 대행 첫 10건, 일요일 저녁 일정·목표 선보고","who":"수민님","p":"P0","n":"https://app.notion.com/p/3d70cf8fea04816fabb8d5cde5e879a0","cash":True},
  {"d":"2026-09-13","t":"디노 재무 3시나리오 과제 제출","who":"수민님","p":"P0","n":"https://app.notion.com/p/3d70cf8fea0481fb8366f4101d44ad45","cash":True},
  {"d":"2026-09-13","t":"디노 신규 수익모델 3안(대행·뷰셀·운영대행) 제시하고 ①+② 병행 선택 확정","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea04816ca736c5ac1c016452","cash":True},
  {"d":"2026-09-13","t":"박태경 대표 스토어 데이터 수집(등록수·주문·마진·상위 20 상품) 및 1회차 진단 결과 공유","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea048109be98cee40b2ee7c2","cash":True},
  {"d":"2026-09-13","t":"드벨헤어 건물 임대 조건 검토·회신","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea0481e4b4f4e466acd29e02","cash":True},
  {"d":"2026-09-13","t":"디노 협업 경계 정책·계약 정산 기준 초안 작성 후 서명","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea0481309c23e7ffa90af2ca","cash":False},
  {"d":"2026-09-13","t":"사입 수익모델 네이밍 확정 (후보 30개 중 선택)","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea04817aaa83e01e45abe751","cash":False},
  {"d":"2026-09-13","t":"전자책 배포 수신자에게 후속 설문 참여 동의 항목 추가 (DM 자동화/신청 폼)","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea0481e6857af5f9e0e2d70f","cash":False},
  {"d":"2026-09-13","t":"사입 강의 후킹용 대표 상품군 선정","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea048153a383c225033b34ed","cash":False},
  {"d":"2026-09-13","t":"브랜딩 기획사 시트 10개 주제 내용 작성·전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea04810c99b8e6c02c3ba4cd","cash":False},
  {"d":"2026-09-13","t":"인베이더에 무료특강 콘셉트 통일 요구 — 솔직·직설 톤, 전문가 포지셔닝","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea04817bae50c8f5e0672022","cash":False},
  {"d":"2026-09-13","t":"뷰셀 유튜브 10분 대본 작성 — 화장품 돈 버는 유니버스 + 가장 빠른 로드맵(리셀)","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481fb912bcbdea617f61c","cash":False},
  {"d":"2026-09-13","t":"소통보드 실사용 세팅 — 팀원 등록·컨설팅URL·API 키","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481c39a5de622a40054d8","cash":False},
  {"d":"2026-09-13","t":"소명서 메이커 마무리 3건 — Vercel claim·Drive OAuth 클라이언트 ID·실제 API 키 테스트","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481bd8a77ff448e2cd41d","cash":False},
  {"d":"2026-09-13","t":"모든 클로드 프로젝트·클로드 코드에 노션 자동기록 프롬프트 적용","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481649e89fd96df043fbd","cash":False},
  {"d":"2026-09-13","t":"인포크링크 랜딩 페이지 제작","who":"루나","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481429661c705052acada","cash":False},
  {"d":"2026-09-13","t":"유튜브 채널 멤버십 개설 (4,900원)","who":"루나","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481468157e850ce768713","cash":False},
  {"d":"2026-09-13","t":"구독자 전용 오픈채팅 개설 + 입장 안내문","who":"루나","p":"P0","n":"https://app.notion.com/p/3d50cf8fea04814b864ecc232bca108c","cash":False},
  {"d":"2026-09-13","t":"스마트스토어에 진단 세션 상품 등록","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481719b64ff7a119598f0","cash":False},
  {"d":"2026-09-13","t":"메이브님과 컨설팅 판매 배분 합의","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea048181acf4ca4a9359f28e","cash":False},
  {"d":"2026-09-13","t":"스마트스토어에 '구독 창립멤버 연간권 10만' 등록","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481beb16ed36f0c6fe8eb","cash":False},
  {"d":"2026-09-13","t":"컨설팅 정가 확정 — 진단 20만 / 4주 집중 90만","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481dfb526ea93d0fbd5c0","cash":False},
  {"d":"2026-09-15","t":"박태경 대표에게 1회차 정리 페이지 + 2회차 예고편 잔디로 공유","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea048119b2f3cb3fac05e2c9","cash":True},
  {"d":"2026-09-16","t":"박태경 대표 2회차 사전준비 — 결정 규칙표 구글 시트 양식 + 고가 상품 후보 3개","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea048167a0a1cb1dc62d4509","cash":True},
  {"d":"2026-09-17","t":"원크루 추석 특강 한정 오퍼 확정 (보너스·신청 마감·상담 신청 방법)","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481d3bff3fee8aafdb86c","cash":True},
  {"d":"2026-09-17","t":"토스페이먼츠 가입 + 일반결제·빌링 심사 신청","who":"루크","p":"P0","n":"https://app.notion.com/p/3dc0cf8fea0481e69ef1e2ce09c46345","cash":True},
  {"d":"2026-09-17","t":"깃허브 저장소 전부 Private 전환","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea048181870ef9fc9aa383d1","cash":False},
  {"d":"2026-09-18","t":"추석 특강 4교시 강의안·실습 자료 제작 (소싱·등록·관리·프로그램 설치)","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481ddaa56e65846c257c4","cash":True},
  {"d":"2026-09-18","t":"뿌요에게 90일 작전서(전자책) 전달 + 상담 세션 진행","who":"루크","p":"P0","n":"https://app.notion.com/p/3d80cf8fea0481989059ec3931dfcad6","cash":True},
  {"d":"2026-09-18","t":"특강 1 라이브 — '10월에 올려야 할 상품 30개'","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea048137b746f47edf0cee6b","cash":False},
  {"d":"2026-09-18","t":"카톡 1,000명·카페 선판매 공지","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04818697efc9c2ae93ea3e","cash":False},
  {"d":"2026-09-19","t":"프로그램 설치 가이드 PDF 제작 + 새 PC에서 설치 테스트 (추석 특강)","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481248127e9de1f447df8","cash":True},
  {"d":"2026-09-19","t":"원크루 실적 사례집 정리 (수강생 3~5명, 숫자 중심)","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481938ddbf36fb285e0c0","cash":True},
  {"d":"2026-09-19","t":"특강 선물 페이지 제작 — 자료 다운로드 + 원크루 소개 + 상담 신청","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481c0b70fdc308e177680","cash":True},
  {"d":"2026-09-20","t":"유○○ 대표님 브랜딩 코칭 — 카페 글 발행 완성편 교육 진행","who":"루크","p":"P0","n":"https://app.notion.com/p/3df0cf8fea04816492bae3482b45f521","cash":True},
  {"d":"2026-09-20","t":"추석 특강 참석자 안내 메시지 4종 작성·예약 (전날·당일·D+1 선물·마감 D-1)","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481f8ba93d7ed2cf741ca","cash":True},
  {"d":"2026-09-20","t":"김○○ 대표님(일십백천) 0917 컨설팅 리포트(전자책 PDF) 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481749e93f85ee73cbdb2","cash":True},
  {"d":"2026-09-20","t":"김종진 대표님께 코칭 노트 전자책(PDF) 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea04814a8c95fc5746782cf3","cash":True},
  {"d":"2026-09-20","t":"브랜드(메이크업헬퍼) 제출용 12주 광고 운영 계획서 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea0481feb08ae244ee7e17f2","cash":True},
  {"d":"2026-09-20","t":"위탁판매 계약서 검토본(수정추적·반영본) 최은봉 대표님께 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea0481f784d7c4b705c7438d","cash":True},
  {"d":"2026-09-20","t":"네이버 가격비교·쿠팡에서 쿠션·팩트 실판매가 직접 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea0481e69d1adecf3cc3a477","cash":True},
  {"d":"2026-09-20","t":"최은봉 대표님께 검토 결과 전달 — 계약서 필수 수정 5곳 + 3개월 파일럿 공급가안","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea048187a6c7dc94789fe837","cash":True},
  {"d":"2026-09-20","t":"툴박스 사이트 1차 구축 (클로드 코드)","who":"루크","p":"P0","n":"https://app.notion.com/p/3dc0cf8fea048136a3fadc4620bd0ca1","cash":True},
  {"d":"2026-09-20","t":"박태경 대표 2회차 컨설팅(2시간) — 숫자 점검·100문 현장 작성·규칙/손절선/책임분담 교육","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea048154be86ca1644e7db9b","cash":True},
  {"d":"2026-09-20","t":"박태경 대표 100문100답 작성 독려 및 2회차 전 회수","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea0481c7b0f6cbfbb608119e","cash":True},
  {"d":"2026-09-20","t":"특강 신청 링크 공유 형태 결정 — QR / 카톡 미리보기 이미지 / 짧은 주소","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea0481ff8a62e975d66e2b9e","cash":False},
  {"d":"2026-09-20","t":"미용 단톡방 초대 명단 200명 세팅","who":"루크","p":"P0","n":"https://app.notion.com/p/3dc0cf8fea048113b25eedaceed94729","cash":False},
  {"d":"2026-09-20","t":"블로그 계정 확인 — 자동화가 개인 블로그에 연결됨, 샵 블로그로 바꿀지 결정","who":"루크","p":"P0","n":"https://app.notion.com/p/3dc0cf8fea048176bc35cac693cbfbdc","cash":False},
  {"d":"2026-09-20","t":"키티티 카드뉴스 6장 인스타 업로드 + 댓글 DM 자동화 연결","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481d49015de6297982e5e","cash":False},
  {"d":"2026-09-20","t":"키티티 AI 브리핑 노출 진단 — 조건형·정보형 검색어 4종 테스트","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481b49d02de192c76147c","cash":False},
  {"d":"2026-09-20","t":"키티티 스마트플레이스 정보 정비 (시술항목·가격·소요시간·사진·소개문)","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481ce9341f65e6a892448","cash":False},
  {"d":"2026-09-21","t":"키티티 컨설팅 유료화 — 자문 계약서","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea04816d8deed192e3f543f1","cash":True},
  {"d":"2026-09-21","t":"루크 툴킷 3개 묶음 + 300만 8주 프로그램 구성안 확정","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea04817dbae9d794af47d070","cash":True},
  {"d":"2026-09-21","t":"블로그 자동화 구독 웹앱 권한 승인 1회 (스크립트 실행·배포 승인)","who":"루크","p":"P0","n":"https://app.notion.com/p/3e00cf8fea0481449984cf589b2ba21d","cash":False},
  {"d":"2026-09-21","t":"계획 공유 페이지 luke-plan 비공개 저장소에 올리기","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea048192b48fc944976520bf","cash":False},
  {"d":"2026-09-21","t":"브랜드용 틱톡 신규 계정 생성 및 프로페셔널 전환 세팅","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea04811bad59ff3754885951","cash":False},
  {"d":"2026-09-21","t":"마케팅 업체에 인스타그램 계정 링크 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481b59a1fe8df55d2fce8","cash":False},
  {"d":"2026-09-21","t":"마케팅 업체에 유튜브 채널 업로드 권한 부여","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481648164fbe396ee2186","cash":False},
  {"d":"2026-09-21","t":"특강 편집 — 풀버전(멤버십) + 예고편 3분","who":"루나","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04817eb203f645fefcb13b","cash":False},
  {"d":"2026-09-23","t":"최은봉 대표님 정기통화 — 당근 화장품 입점 가능 여부·브랜드 희망가 회신 점검 후 수정 로드맵 확정","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea0481d399eec82c67f597f1","cash":True},
  {"d":"2026-09-24","t":"인스타그램 크리에이터 계정 전환 + 프로필명·소개·링크 세팅","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea0481dcb1d0e87c20df960c","cash":False},
  {"d":"2026-09-24","t":"중국 연휴 전 테무·중국발 발주 마감 처리","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea04812f8c8ac7a435d2ec01","cash":False},
  {"d":"2026-09-25","t":"뿌요 2주 실측 후 숫자표 갱신 (등록 속도·전환·건당 마진·역마진율·용역 입금)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d80cf8fea048171b2fbfac97843f6ed","cash":True},
  {"d":"2026-09-25","t":"138명 명단에 단톡방 링크 메일 발송","who":"루크","p":"P1","n":"https://app.notion.com/p/3e50cf8fea0481c3ad1dd52eef538ad6","cash":False},
  {"d":"2026-09-25","t":"등록 완료 파일 1~4주차 제작 (이미지·상세·가격·CSV)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea048166899dd2c2660aa929","cash":False},
  {"d":"2026-09-25","t":"특강 다시보기 7일 유지 → 8일째 멤버십 전용 전환","who":"루나","p":"P1","n":"https://app.notion.com/p/3d50cf8fea0481feb3a5cd48ca222420","cash":False},
  {"d":"2026-09-26","t":"김종진 대표님 9/26 코칭 준비 (재무 구조·브랜드 성공 사례)","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea0481529e48ff3fcaee267f","cash":True},
  {"d":"2026-09-26","t":"김종진 대표님 코칭 진행 (9/26 토)","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea048193bd07c350a84a36e1","cash":True},
  {"d":"2026-09-26","t":"김종진 대표님 아이템 파일 분석","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea0481b594f2e1d450ea399b","cash":True},
  {"d":"2026-09-27","t":"원크루 오픈채팅 문의자 가격 안내 발송 + 상담 통화 제안 [설명서]","who":"루크","p":"P0","g":"onecrew-inquiry","n":"https://app.notion.com/p/3e70cf8fea0481a69980e77594f1b740","cash":True},
  {"d":"2026-09-27","t":"키티티 교육상품·가격 확정 + 촬영 공간 세팅 (1주차)","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea0481018e13d1a3bf0fc433","cash":True},
  {"d":"2026-09-27","t":"툴박스 구독 상품 정의 (포함 목록·가격·약관)","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea04811581dffbdb65fcd9cd","cash":True},
  {"d":"2026-09-27","t":"AI 스튜디오 포트폴리오 + 가격표 랜딩 제작","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481299a48c867a00f779b","cash":True},
  {"d":"2026-09-27","t":"셀수다 v2026.9.26 설치 + 크롬 '카탈로그 수집기' 확장 설치","who":"루크","p":"P0","n":"https://app.notion.com/p/3e70cf8fea048151a2b9cb0abd28ebc4","cash":False},
  {"d":"2026-09-27","t":"툴박스 구독권 오픈일·가격·사전 신청 방식 확정해 안내 문구 만들기 [설명서]","who":"루크","p":"P0","g":"toolbox-presignup","n":"https://app.notion.com/p/3e70cf8fea0481b895bbd0b7c6fe15a2","cash":False},
  {"d":"2026-09-27","t":"블로그타이퍼 윈도우 클로드 코드로 이사 (깃허브 clone·데이터 복사·네이버 재로그인)","who":"루크","p":"P0","n":"https://app.notion.com/p/3e60cf8fea0481cca61cf923c28b9e54","cash":False},
  {"d":"2026-09-27","t":"셀수다 자동등록 설치파일 '바이러스 발견됨' 오탐 해결","who":"루크","p":"P0","n":"https://app.notion.com/p/3e10cf8fea04819d9453e64479413781","cash":False},
  {"d":"2026-09-27","t":"프로그램 시연 쇼츠·릴스 3개 촬영 (AI 스튜디오)","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea04815ea4afefeddb51d9e6","cash":False},
  {"d":"2026-09-28","t":"10월 말 무료 라이브 시간·신청 링크 확정 — 날짜 10/25(일)는 10/4 노션 [결정]으로 확정, 시간 19:00는 10/2 녹음 언급값·링크 확인 필요 [설명서]","who":"루크","p":"P0","g":"free-live","n":"https://app.notion.com/p/3e90cf8fea048171ac6bd0e23e1c5669","cash":False},
  {"d":"2026-09-28","t":"록터뷰 2회차 인터뷰 촬영 (사입 자동 소싱·자동 등록·상품 찾는 법)","who":"루크","p":"P0","n":"https://app.notion.com/p/3e90cf8fea048107ba1dff3afb73cedd","cash":False},
  {"d":"2026-09-30","t":"수강생 컨설팅 후속 — 소장 대응 결정·리셀 정리·브랜드 재점검 (익명)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481b1af7ac611bcbe1835","cash":True},
  {"d":"2026-09-30","t":"지인 10명 직접 영업 → 첫 3건 반값 계약 (AI 스튜디오)","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481fbb205f0c4d7e7c998","cash":True},
  {"d":"2026-09-30","t":"뷰셀 2화 대본 제공 (화장품 10년 트렌드·성분·브랜드)","who":"루크→메이브님","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-09-30","t":"물류 업데이트/운영 책임자 지정 + 현안 이슈 보드 시작 [설명서]","who":"뿌요·루크","p":"P0","g":"logistics-stabilize","cash":False},
  {"d":"2026-09-30","t":"영상공장 윈도우 PC에서 설치·첫 영상 테스트","who":"루크","p":"P0","n":"https://app.notion.com/p/3e90cf8fea04815da58cc6d8030ca735","cash":False},
  {"d":"2026-09-30","t":"수강생 전체 공지·교육자료 — 화장품 위탁판매 시 2차 포장(단상자)·표시사항 유지 필수, 도매처 검증 체크리스트","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea0481969503d67f972a91e1","cash":True},
  {"d":"2026-09-30","t":"유○○ 대표님 브랜딩 코칭 숙제 점검 — 카페 글 2편 발행 + 발행 기록표 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3df0cf8fea0481d7bb28cca228124c0a","cash":True},
  {"d":"2026-09-30","t":"연휴 후 원크루 상담 슬롯 확보 (9/28~10/2)","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea0481ee849bc598c8df1d37","cash":True},
  {"d":"2026-09-30","t":"김○○ 대표님(일십백천)께 새 소싱 프로그램 진행 상황 공유","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea0481d0805dd903b0b05d6f","cash":True},
  {"d":"2026-09-30","t":"키티티 빌드업 로드맵 전자책 지영에게 공유·피드백 받기","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea0481c7804adf53ebba3b46","cash":True},
  {"d":"2026-09-30","t":"키티티 토탈샵 임대 조건 재조율·권리금 협상 (공인중개사 통해)","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea04813aba17e8638ff1be86","cash":True},
  {"d":"2026-09-30","t":"키티티 토탈샵 대출 규모·오픈비 견적 확정 (지영과 논의)","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea048147acabc2f5a990da7a","cash":True},
  {"d":"2026-09-30","t":"코치님 스토어–뿌요 수익배분 6항목 합의 미팅 중재","who":"루크","p":"P1","n":"https://app.notion.com/p/3d80cf8fea04811dae02c8a8af043dc0","cash":True},
  {"d":"2026-09-30","t":"뿌요 실무 용역(등록 대행·1:1 코칭) 첫 고객 2명 연결 — 루크 승인 채널로","who":"루크","p":"P1","n":"https://app.notion.com/p/3d80cf8fea0481dbb916f9898dfe614f","cash":True},
  {"d":"2026-09-30","t":"클릭가이드 데모 테스트 + 네이버 가격비교 시나리오 채우기","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04818b8591c5f9f9fb71d7","cash":True},
  {"d":"2026-09-30","t":"잔디 이슈 채널 운영 규칙(이슈 템플릿·상태 태그)","who":"루크","p":"P1","cash":False},
  {"d":"2026-09-30","t":"앱 배포 계정·인증서 준비 (윈도우·맥·아이폰·갤럭시)","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea0481468c69f67787077a44","cash":False},
  {"d":"2026-09-30","t":"미용인 라운지 사이트 v1 구축·배포","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea0481faadcdf4ad3356a80b","cash":False},
  {"d":"2026-09-30","t":"하루블록 v1.0 무료 배포 준비 (회원관리 스크립트 승인 1번 + 설치파일 드라이브 업로드)","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea04814faafbf99d66cce65a","cash":False},
  {"d":"2026-09-30","t":"브랜드 소개 전자책 최종 검수 후 배포","who":"루크","p":"P1","n":"https://app.notion.com/p/3df0cf8fea0481f4ba25dcc53c160e92","cash":False},
  {"d":"2026-09-30","t":"DM 온 사람들에게 전자책 안내 이미지 1장 + 링크 발송","who":"루크","p":"P1","n":"https://app.notion.com/p/3df0cf8fea0481bf9f68d671bfdb7a12","cash":False},
  {"d":"2026-09-30","t":"ChatGPT에 Plaud(MCP) 연결하고 녹음 불러오기 테스트","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea0481919c0ac58611bb44c6","cash":False},
  {"d":"2026-09-30","t":"강의 계약 전화 상담 녹음 100건+ 전사 → 사례 분석 → 루크 판단 기준 문서화","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea04812a88b7c9649a02127f","cash":False},
  {"d":"2026-09-30","t":"전화 상담 AI 프로토타입 — 루크 판단 기준 답변 엔진 + 내 목소리 출력","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea0481d1898fe1c3d85f7ffc","cash":False},
  {"d":"2026-09-30","t":"인스타 크리에이터 계정 1장 가이드 PDF 배포","who":"루크","p":"P1","n":"https://app.notion.com/p/3de0cf8fea04814490b9d58d3fcfdefb","cash":False},
  {"d":"2026-09-30","t":"API·토큰 발급 — Claude API 키, 네이버 검색광고 API, 네이버 개발자센터 앱 키, 노션 연동 토큰","who":"루크","p":"P1","n":"https://app.notion.com/p/3dc0cf8fea0481f1b599f19a31bf1d93","cash":False},
  {"d":"2026-09-30","t":"인스타 댓글 키워드 → 자동 DM(자료 발송) 세팅","who":"루크","p":"P1","n":"https://app.notion.com/p/3dc0cf8fea0481df86b6d09ff4464aa3","cash":False},
  {"d":"2026-09-30","t":"키티티 블로그 Q&A·정의형 콘텐츠 발행 (고객 실제 질문 기반)","who":"루크","p":"P1","n":"https://app.notion.com/p/3db0cf8fea04818b9da3e30c5c00d213","cash":False},
  {"d":"2026-09-30","t":"전자책 프롬프트 템플릿에 신규 고정 요소 반영 (저자소개·문의·체크리스트·핵심박스·인포그래픽)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d80cf8fea0481a7a368e9df96f71a5f","cash":False},
  {"d":"2026-09-30","t":"기존 전자책 저자 소개 페이지를 새 공통 문안으로 교체","who":"루크","p":"P1","n":"https://app.notion.com/p/3d80cf8fea0481ab9756f944ffa4528b","cash":False},
  {"d":"2026-09-30","t":"홈택스 전자세금용 인증서 재발급 및 홈택스 등록","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea048161af02c3b521f3765e","cash":False},
  {"d":"2026-09-30","t":"인베이더 줌 미팅 녹음·기록 확보","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea04815cba5ac7ecb956390b","cash":False},
  {"d":"2026-09-30","t":"단톡방 유입용 정보공유 자료 6~7개 제작 (잘 팔리는 키워드·상품 리스트 등)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea048171b77ad4ddf3fcf8d1","cash":False},
  {"d":"2026-09-30","t":"비공개 유튜브 강의 영상 링크 기획사에 공유 (실제 화법 참고용)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea04819ab223ef120e052f56","cash":False},
  {"d":"2026-09-30","t":"단톡방 상시 오픈 + 신속 응대 체계 세팅 (목표 500~1000명)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea0481c8a076ed8dff223ced","cash":False},
  {"d":"2026-09-30","t":"인스타 프로필·스토리를 '브랜드 회사 대표 / AI 활용 셀러 전문가'로 갱신","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea0481f295a8c503f5ddc74a","cash":False},
  {"d":"2026-09-30","t":"전자책 「처음이라 걱정되는 당신에게」 검수 후 배포 채널 결정","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04819b9c0ae04ea28f3518","cash":False},
  {"d":"2026-09-30","t":"만능 프롬프트로 첫 주제 테스트 빌드 후 디자인·분량 보정","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04816e8cb6f20238d24d97","cash":False},
  {"d":"2026-09-30","t":"뿌요 짠테크 유튜브 1화 촬영·편집 (대본 완성)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04813e82a7f1b0f8fa4f4f","cash":False},
  {"d":"2026-09-30","t":"예약 페이지 v2 — 로그인·유형별 상담·가변 길이·자동 휴식","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea0481e5becadd103500be3a","cash":False},
  {"d":"2026-09-30","t":"상담봇 v2 테스트 후 Vercel 실서비스 이식 범위 확정","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04815f82b2eeb646a71c5c","cash":False},
  {"d":"2026-09-30","t":"GitHub 푸시 + v1.0.0 태그로 exe 빌드 → 윈도우 실기 체크리스트 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea0481a2b9d0e88a2ebf3a9f","cash":False},
  {"d":"2026-09-30","t":"네이버페이 자산 연결 + 첫 데이터 가져오기","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04815e8637e0811a3968d1","cash":False},
  {"d":"2026-09-30","t":"음성 엔진 세팅 — 오픈소스 TTS 한국어 비교 청취 후 내 목소리 등록","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea048196a7d2c6342d41aa64","cash":False},
  {"d":"2026-09-30","t":"전자책 표준 프롬프트 템플릿에 개정 요소 반영","who":"루크","p":"P2","n":"https://app.notion.com/p/3d80cf8fea048109a1cac8997ca2345c","cash":False},
  {"d":"2026-10-01","t":"3PL 수강생 재고 당근·외부 판매 — 첫 등록 (동의서·시트·비즈프로필) [설명서]","who":"루크·루나","p":"P0","g":"3pl-resale","n":"https://app.notion.com/p/3de0cf8fea0481b2a948d2dc4f7802ed","cash":True},
  {"d":"2026-10-01","t":"최은봉 대표님께 12주 계획·3p 요약 PDF 재전송 + 9/30 세션 리포트 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481b8be99d8ebff105a1b","cash":True},
  {"d":"2026-10-01","t":"키티티바이지영 상표권 출원 (KIPRIS 선행검색 → 출원, 30분) [설명서]","who":"루크·지영","p":"P0","g":"kititi-trademark","n":"https://app.notion.com/p/3ea0cf8fea0481eda6d9db338d52c92c","cash":False},
  {"d":"2026-10-01","t":"물류 삭제/무효화 임시 규칙 + 핸드오버 체크리스트","who":"루크·뿌요","p":"P1","cash":False},
  {"d":"2026-10-01","t":"지영 인스타 주간 운영 캘린더 시작","who":"지영","p":"P1","cash":False},
  {"d":"2026-10-01","t":"김○○ 대표님(일십백천) 상담 — 박스 후보 선정 + 일러스트 방향","who":"루크","p":"P2","n":"https://app.notion.com/p/3de0cf8fea0481488283f761e2951e9e","cash":True},
  {"d":"2026-10-02","t":"개발자 계정 3종 등록 — Apple Developer($99/년) · Google Play($25 1회) · Microsoft Store(무료) [설명서]","who":"루크","p":"P0","g":"developer-accounts","n":"https://app.notion.com/p/3eb0cf8fea0481d8bbb4e0cbd5746fd9","cash":True},
  {"d":"2026-10-02","t":"박태경 대표님 사입 재고 관리 스프레드시트 제작·공유","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481029429c45d9b6bfe47","cash":True},
  {"d":"2026-10-02","t":"뷰셀 2화 촬영 (공개 10/7)","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-10-02","t":"물류·전산 전체 프로세스 맵 + 병목 표시","who":"뿌요","p":"P1","cash":False},
  {"d":"2026-10-03","t":"평생컨설팅 문의(뷰셀 수강생·쿠팡 영구정지) 답변 + 진단 상담 잡기 — 10/2 답장 발송, 회신 오면 일정 확정","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481839c31e0155118809c","cash":True},
  {"d":"2026-10-03","t":"물류 중복·충돌 기능 정리 우선순위","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-04","t":"디노(미니쌤) 12주 빌드업안 전달·합의 (PDF 『미니쌤, 12주의 지도』) [설명서]","who":"루크→디노","p":"P0","g":"dino-12weeks","n":"https://app.notion.com/p/3e90cf8fea048120bd88de7b8953d9dc","cash":True},
  {"d":"2026-10-04","t":"키티티 AI 스타일 미리보기(/try) 구축 — 무료 1회·워터마크·유료 원본 다운로드","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04812b8f86e2d58503588d","cash":True},
  {"d":"2026-10-04","t":"키티티 '연봉 10억 만들기' 페이지 배포 — 저장소 kititi-1b 생성·권한 후 push","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04814187b8c258b3a2d38e","cash":True},
  {"d":"2026-10-04","t":"박태경 대표님 상품·가격 관리 체크리스트 제공 (주말 비판매 상품 솎아내기 등)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481449491c4a611a60d57","cash":True},
  {"d":"2026-10-04","t":"키티티바이지영 상표 출원 (지영 명의, 특허로 전자출원) — 진행 중","who":"루크","p":"P0","n":"https://app.notion.com/p/3ec0cf8fea0481919532d4927c656358","cash":True},
  {"d":"2026-10-04","t":"상품소싱 시트 마진 공식에 매입 배송비 반영 + 백설 와플믹스 10kg 역마진 재확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea04813d9f8aedfc7e183098","cash":True},
  {"d":"2026-10-04","t":"홍○○ 대표님(원크루 상담 10/3)께 상담 리포트 링크 발송 — 진행 중","who":"루크","p":"P0","n":"https://app.notion.com/p/3ee0cf8fea04812e8d21df33ab1687df","cash":True},
  {"d":"2026-10-04","t":"최저가 찾기 소싱 프로그램 새 버전 공개","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04817fa0caf144b0c513ee","cash":False},
  {"d":"2026-10-04","t":"'내 연봉 10억 만들기' 대시보드 페이지 배포 (이 페이지 — 배포됨, 노션은 아직 '진행 중')","who":"루크","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea048131b2d4dc645e92ac57","cash":False},
  {"d":"2026-10-04","t":"마진메이커 크롬 확장 프로그램 설치·서버 배포 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481b18770d4c9279c70a1","cash":False},
  {"d":"2026-10-04","t":"물류 표준 운영 가이드 배포 / 피크일(월·화) 택배 우선 운영안","who":"루크·뿌요","p":"P1","cash":False},
  {"d":"2026-10-05","t":"디노 12주 프로그램 1주차 시작 (AI 셀러 실무 교육 빌드업)","who":"디노","p":"P0","n":"https://app.notion.com/p/3e90cf8fea048120bd88de7b8953d9dc","cash":True},
  {"d":"2026-10-05","t":"리나님 시간 기록 시트 1~2주 시범 운영 (매일 퇴근 전 피드백)","who":"리나님·루크","p":"P0","n":"https://app.notion.com/p/3e90cf8fea0481f386b9d5f0d96feb05","cash":False},
  {"d":"2026-10-05","t":"키티티 상담 사이트 원장님 확인 (사진 동의·한마디·비포애프터)","who":"루크·지영","p":"P0","n":"https://app.notion.com/p/3e90cf8fea0481d2aa25e18cf01f6b09","cash":False},
  {"d":"2026-10-05","t":"영상공장 API 키 5개 발급 + 목소리 1~3분 녹음","who":"루크","p":"P0","n":"https://app.notion.com/p/3e90cf8fea048106ab46ee6d7425f2c8","cash":False},
  {"d":"2026-10-05","t":"다음 주 평일 저녁 팀 회식 장소 확정·예약","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481a08c7ac705e54340e1","cash":False},
  {"d":"2026-10-05","t":"매장 대청소 작업 입회·검수 (비포에프터클린 · 10/5 14:00 · 작업 전후 사진)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f00cf8fea048133b45ff8bb4dc6e7c9","cash":False},
  {"d":"2026-10-05","t":"박태경 대표님 고객 안내용 템플릿 메시지 3종 초안 (발송·지연·취소)","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea04812c84d8d9344b5cfec6","cash":True},
  {"d":"2026-10-05","t":"현재 사무실 임대료·관리비 정산 완료 (기한 추정 · 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481c2a29df44aa8ee126e","cash":False},
  {"d":"2026-10-06","t":"수강생 화장품법 소송 대응 지원 — 답변서 기한·변호사 연결 (익명) [설명서]","who":"루크","p":"P0","g":"lawsuit-support","n":"https://app.notion.com/p/3ea0cf8fea048198857ef162cf15ad7a","cash":True},
  {"d":"2026-10-06","t":"10/6 12:00 소싱 멘토링 실습 진행 — 수강생 소싱 10개 점검 (10/2 멘토링 후속 · 일시 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea048154a15bddc7596e1165","cash":True},
  {"d":"2026-10-06","t":"강의 플랫폼 3자 미팅 제안서 1차본 검토 — 초이스토리 × 종혁 본부장 × 셀수다","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04814e827ce3cca543028e","cash":True},
  {"d":"2026-10-06","t":"배수진(돈 걸고 목표달성 앱) 프로토타입 검토","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea0481af8112d35bc3c0e23b","cash":True},
  {"d":"2026-10-06","t":"박태경 대표님 빠른 거절·통보 기준 문서화 (예: 2시간 내 판단 룰)","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481989321faefe3f4f605","cash":True},
  {"d":"2026-10-06","t":"물류 CS 포인트 분석 + 사전 안내 스크립트 정비","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"박태경 대표님 5회차 준비 — 10월 첫 주 점검표 10개 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481eda67cda9ab46ad130","cash":True},
  {"d":"2026-10-07","t":"정○○ 대표님(원크루) 다음 컨설팅 — 매일 결산·금요일 상품 정리 점검","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481ea947cc6042c5ad37e","cash":True},
  {"d":"2026-10-07","t":"최은봉 대표님 1주 팔로업 — 10/1 당근 올리고 바로 광고, 10/3·5·6 플랫폼 가입 확인 (17:00 카톡)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea048161b042f4bf4fb3da5b","cash":True},
  {"d":"2026-10-07","t":"김종진 대표님 10/7 코칭 진행 — 후보 목록·AI 대화 횟수 점검 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481b38ce4d66a8cb866d9","cash":True},
  {"d":"2026-10-07","t":"김종진 대표님 9/30 녹음 반영 코칭 노트 전자책 신규 버전 제작 (노션 '진행 중' — v2·통합본 완료 기록이 있어 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481dd88e7e2491ed90fa8","cash":True},
  {"d":"2026-10-07","t":"김종진 대표님 10/7 코칭 — 지난주 과제(리스크 질 아이템 1~2개) 확정받기 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481bea2f4caed3f684a63","cash":True},
  {"d":"2026-10-07","t":"원크루 사이트 — 최은봉 대표 자료실 1~5회차 교육자료 게시 (배포 대기)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04810d8c83e87ecbc54cda","cash":False},
  {"d":"2026-10-07","t":"정복녀 대표님 원크루 사이트 회차 자료 배포 — 원크루 사이트 채팅에 '배포해 줘' 요청","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bc907df6b56c5a43b4","cash":False},
  {"d":"2026-10-07","t":"원크루 사이트 채팅에서 '배포해 줘' (최은봉 대표님 6회차)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea04812faaadfa28cc19b9fa","cash":False},
  {"d":"2026-10-07","t":"인스타 오늘 게시물 업로드 + '홍보하기' 일 5천원×7일 집행","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481299b44db868963f2be","cash":False},
  {"d":"2026-10-07","t":"최은봉 대표님 사업 구조화 페이지 — 저장소 생성·배포 대기 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea04812b8750c92c2d6ae837","cash":False},
  {"d":"2026-10-07","t":"박태경 대표님 백문백답·4회차 교육자료 재확인·공유","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481fd8c72c6256ae03466","cash":True},
  {"d":"2026-10-07","t":"뷰셀 2화 공개 (수)","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-10-07","t":"스마트스토어 발송·지연·취소 카톡/문자 자동 알림 방법 조사","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea04815b9851f87faf14fae1","cash":False},
  {"d":"2026-10-07","t":"뿌요 짠테크 유튜브 3화 '연쇄적금러' 대본 작성","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea04818f9d6fdd1b114a853e","cash":False},
  {"d":"2026-10-07","t":"물류 권한 재설계 + 감사 로그","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"지영 예약·매출 간단 대시보드 완료 목표","who":"지영","p":"P2","cash":False},
  {"d":"2026-10-08","t":"종혁 본부장 미팅 — 락인 축(챌린지·카페·광고) 역할과 1:1:1 배분안 제시 [설명서]","who":"루크·메이브님","p":"P0","g":"platform-director-meeting","n":"https://app.notion.com/p/3eb0cf8fea04816b8d8ee9e56061c6d0","cash":True},
  {"d":"2026-10-08","t":"최은봉 대표님 미팅 14:00 — 당근 광고 중간 결과 화면 리뷰 (노션은 10/8, 녹음은 '수요일'=10/7 · 날짜 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04814c922bc0af3fa5ab4f","cash":True},
  {"d":"2026-10-08","t":"키티티 계약 — 10/8(목) (플라우드 10/8 녹음: 토탈샵 임대차·권리양수도 계약 체결 · 노션 완료 처리 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f00cf8fea0481a89260d919b12e75c3","cash":True},
  {"d":"2026-10-08","t":"3자 1:1:1 안과 초월스토리 8% 모델 관계 정리 (대체 vs 병행) → 10/8 본부장 미팅 제안 수정","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e4a78edf0ea6527d5c","cash":True},
  {"d":"2026-10-08","t":"인베이더 종료 사실 확인 — 범위·시점·출처 파악 (강의만인지 전체인지)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b2b5f9c0ab5aa17594","cash":True},
  {"d":"2026-10-08","t":"키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체","who":"루크","p":"P0","n":"https://app.notion.com/p/3ec0cf8fea0481698468f35e62d2e19b","cash":False},
  {"d":"2026-10-08","t":"세무사에 최근 2년 수입금액 조회 — 0인지 먼저 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048142a77bc76c2cbddeb4","cash":False},
  {"d":"2026-10-08","t":"정관 본점 조항·등기사항전부증명서 확인 — 주주총회 필요 여부 정하기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b4a420f807f87de087","cash":False},
  {"d":"2026-10-08","t":"메이브님과 마지막 기수 공동 대응 합의 — 같은 명단 확보 동선 쓰기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04818daa2dec0849cd7a73","cash":False},
  {"d":"2026-10-08","t":"구리세무서 재산법인세과 전화 — 법인등기 진행 중, 완료 후 재신청 예정 알리기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481d396d6fb41d1c6ee6b","cash":False},
  {"d":"2026-10-08","t":"최은봉 대표님 이번 주 일정 체크 — 10/8 일본 직판 아카데미 면접 · ~10/9 정책자금 서류 · 10/12 정책자금 신청+출판기념회 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea048150950bf636e70899ed","cash":False},
  {"d":"2026-10-08","t":"배송비 포함 총액 계산 시트 템플릿 배포 (10/2 멘토링 수강생용)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481a4837dc07d4eeaa7a7","cash":True},
  {"d":"2026-10-08","t":"지영 미팅 — 정부지원사업 후보 3개 + 사업계획서 초안 리뷰","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-08","t":"정부지원사업 맞춰 보기 사이트 「되는 지원사업 찾기」 구축 (클로드 코드)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ec0cf8fea048151a8acff9e6bbd0442","cash":False},
  {"d":"2026-10-08","t":"사진 기반 입고/검수 자동화 플로우 설계","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-09","t":"목적 추가 문구 확정 — 창고업·물류 쪽을 넉넉하게 (꼬마빌딩 취득세 연결)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea048140aa1ece2d480e62f2","cash":True},
  {"d":"2026-10-09","t":"세무사 통화 — 임원 추가선임이 '50% 교체'인지, 지분 50% 양도가 '인수'인지","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048117871ec5f5c092cc1c","cash":False},
  {"d":"2026-10-09","t":"뷰셀 3화 대본 — 10년 안에 매출 열 배 뛴 브랜드 (촬영 10/9)","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048164a5c6f5877ec73e25","cash":False},
  {"d":"2026-10-09","t":"정관 원본 찾아 본점 조항 확인 — '구리시'까지인가 번지까지인가","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481cc8bc6f8687a37a03a","cash":False},
  {"d":"2026-10-09","t":"'셀러들의 수다' 상호 중복 확인 — 의정부지법 남양주지원 관할 내 (인터넷등기소 법인 상호검색)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea04817aa334df39bcb54f3e","cash":False},
  {"d":"2026-10-09","t":"신정현 대표님에게 등기 제출용 준비물 전달 + 인감 신고 여부 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea048160af98ebbd0e2d90e8","cash":False},
  {"d":"2026-10-09","t":"등기 서류 — 루크 확정 4가지만 정하고 출력·날인 (구글 드라이브 작성 완료 · 진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea048119872af76a2ef1a9d6","cash":False},
  {"d":"2026-10-09","t":"소싱 선별 기준표 작성 — 카탈로그 최저가순·총액 확인·리뷰 10개 이상·수량/용량 오류 점검","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481759627c752b5187600","cash":True},
  {"d":"2026-10-09","t":"키티티 원장님께 /admin 노트 사용법 전달 + 시술 방향 검토·피드백 받기 (습도·채광·장소·이동시간)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea04810b808df66fdd4ed562","cash":False},
  {"d":"2026-10-09","t":"키티티 /guide 내용 원장님 피드백 받기 (상담 12항목·데일리/촬영 기준·O/X 표·계절 색)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481839ab5c4f4a80c7caf","cash":False},
  {"d":"2026-10-10","t":"디노 토요일 잠정 평가 미팅 — 릴스 4편(수~토) 결과 보고 다음 주 기획안 확정 (플라우드 10/6)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04819ea0f3e061b27410ce","cash":True},
  {"d":"2026-10-10","t":"멘토루크 블로그 — 블로그 프로그램을 개인 브랜딩(케어 이야기 중심)으로 독립 분기 1차 전환 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481bc8287dc9e35045f45","cash":False},
  {"d":"2026-10-10","t":"정관 찾기 — 법무사·세무사·등기소 열람·외장하드 순서로","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481ba8918e112e5a5b6b0","cash":False},
  {"d":"2026-10-10","t":"박태경 대표님 겨울 시즌 상품 추천 리스트 + 광고 예산 재배분 가이드 송부","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481b6bb58d7ba75a7c299","cash":True},
  {"d":"2026-10-10","t":"최저가 미스매치 재검증 체크리스트(10/10) + 용량·구성 실질 단가 환산 규칙 문서화(10/11)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481289522d32db9f9c962","cash":True},
  {"d":"2026-10-10","t":"뿌요 짠테크 유튜브 2화 '겨자씨: 생애 첫 적금 100일 100만 원' 촬영·편집 (대본 완성)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea048156bcacce118e9d3edd","cash":False},
  {"d":"2026-10-10","t":"물류 선반 추가·라벨링·박스 재배치","who":"뿌요","p":"P2","cash":False},
  {"d":"2026-10-11","t":"6기 무료라이브 미결정 사항 확정 (날짜·모델명·가격/반 구성·주력 카테고리·재고 처리 정책)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ee0cf8fea04815d91cdf96ae0a85075","cash":True},
  {"d":"2026-10-11","t":"6기 라이브 수강생 인터뷰 5명 섭외·자료 준비(이름·이전 직업·결과 캡처·한마디)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ee0cf8fea04815cb405fa8d84e0fe85","cash":True},
  {"d":"2026-10-11","t":"AI 진단 → 유료 진단·시술 전환 검증 실험 (랜딩+사전예약)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea04812c9dbfcf46c011ba42","cash":True},
  {"d":"2026-10-11","t":"6기 라이브 PPT B스타일(네이비&크림)로 새로 제작 — 인포그래픽 강화","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea0481798d2ec8a648978d79","cash":True},
  {"d":"2026-10-11","t":"2026년 K-뷰티 크리에이터 챌린지 공고 확인 → 열려 있으면 신청","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea04816b964ef321bed57cea","cash":True},
  {"d":"2026-10-11","t":"키티티 홈페이지 AI 미리 보기·상담 메시지·예약 클릭 수 기록 시작","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea04816099cbd679c8f56304","cash":True},
  {"d":"2026-10-11","t":"[결정 필요] 셀러들의 수다 — 힐링디어스 상호변경으로 가는 것 확정하기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481dc8373e6926b48373b","cash":True},
  {"d":"2026-10-11","t":"가을 대표님 의향·11~12월 일정 확인 — 촬영 1일 + 라이브 4+1회(주말 포함) 가능 여부","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04810ba023cc3d57cac0e6","cash":True},
  {"d":"2026-10-11","t":"가을(정복녀) 대표님 성과 숫자·사업 내용 확보 — 월 매출·순수익·시작 시점·품목·성함 표기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04818fa003c9d49b80fe49","cash":True},
  {"d":"2026-10-11","t":"초월스토리 계약서 정산 기준 정리 — 전체 매출 정의·환불·지급 시점·정산 열람권·광고비 8%와 수수료 8% 구분·프로그램 사용 범위와 회수","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048126a2fec9d1efd1c0eb","cash":True},
  {"d":"2026-10-11","t":"루크 툴박스 — 토스 연동 + 깃허브 자동 업데이트·설치 세팅","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048125ae05dd985c5e7732","cash":True},
  {"d":"2026-10-11","t":"메이븐 스토어 재정비 + 집중 품목 선정 (4분기 월 순수익 1,000만·일 200건 목표)","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048159873bcb81c41d12e9","cash":True},
  {"d":"2026-10-11","t":"사입 재고 처리 가이드라인 수립 — 50일 경과 시 마진 조정·강사 처리 신청·대기열 순차 처리","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04818a9a03e11618ee7ecf","cash":True},
  {"d":"2026-10-11","t":"메이븐 스토어 재정비 · 집중 품목 선정","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04811ab5f7c42585eeeb16","cash":True},
  {"d":"2026-10-11","t":"백○○ 대표님께 전자책 전달 + 가격관리 프로그램 상시 실행 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e3b5eff0f52d73ee47","cash":True},
  {"d":"2026-10-11","t":"디노에게 힙스필드 4수익축 구조도 전달하고 가격표·카테고리 3개 확정","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04815393b4c9b512262ba3","cash":True},
  {"d":"2026-10-11","t":"[막힘] 지영 원장 수익모델 빌드업 페이지 배포 — kittiti-jiyoung 저장소 생성·Pages 켜기·Claude 권한 추가 (루크 직접)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea048152b55cec152c0f6fc9","cash":True},
  {"d":"2026-10-11","t":"신정현 대표 사업 구조화 페이지 — 저장소 onecrew-shin-jeonghyeon 만들기 + Pages 켜기 → 푸시 → 원크루 자료실 게시 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481b3943cf96700d0538e","cash":True},
  {"d":"2026-10-11","t":"토탈샵 인테리어(급배수·전기 증설·칸막이·냉난방기) 승인 별첨 문서 준비","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea048125b5f0cb4b24793347","cash":True},
  {"d":"2026-10-11","t":"토탈샵 건물 임대차 특약 수정안 협상 — 제소전화해·원상복구·갱신 (진행 중 · 10/8 계약 체결 녹음 있음, 완료 여부 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481f1a56ed3713160c671","cash":True},
  {"d":"2026-10-11","t":"인베이더 무료강의 라이브 PPT 제작","who":"루크","p":"P0","n":"https://app.notion.com/p/3ee0cf8fea04810e9f65d1802510734f","cash":False},
  {"d":"2026-10-11","t":"키티티 인스타·플레이스·매장 QR에 진단 링크 걸고 홍보 → 파트너샵 마케팅 키트 1판","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea0481c794b3ef4cc6242f2c","cash":False},
  {"d":"2026-10-11","t":"원크루 신정현 대표 자료실 — 10월 1주차·2주차 컨설팅 자료 배포 (원크루 사이트 채팅에 '배포해 줘')","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b787f0f6d0da8881f4","cash":False},
  {"d":"2026-10-11","t":"[결정 필요] 세무사 상의 — 2,000만 지출 처리 방식 결정","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b2a072c720ff4ca5ba","cash":False},
  {"d":"2026-10-11","t":"[결정 필요] 뿌요 역할·수익 구조 확정 — 장기 거취 먼저, 그다음 배분","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e19ba5cf10a588f7d7","cash":False},
  {"d":"2026-10-11","t":"인베이더 계약서 확인 — 수강생 명단·콘텐츠·후기 소유 조항","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04819eb940cf3625f83b83","cash":False},
  {"d":"2026-10-11","t":"디노 레퍼런스 30세트(비포/애프터) 제작 및 포트폴리오 링크 완성","who":"수민님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048123b9f8cc29e9b9ee50","cash":False},
  {"d":"2026-10-11","t":"힙스필드 요금제 결제 후 첫 달 크레딧 실제 소진량 기록","who":"수민님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481559b24fe698235b4b7","cash":False},
  {"d":"2026-10-11","t":"키티티 무료강의 ①② 제작 + 셀프메이크업 무료 PDF + 저가 VOD 5강 촬영","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea04813c88c1e7123b988adc","cash":False},
  {"d":"2026-10-12","t":"창고형 매장 1단계 범위 정하기 — 진열 공간, 첫 진열 재고 목록, 매장 가격 원칙","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481658a61d68b0e18c84c","cash":True},
  {"d":"2026-10-12","t":"가을(정복녀) 대표님께 원크루 강사 파트너 제안 — 제안서 전달·의사 확인 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea048167b893e89fdf2d8679","cash":True},
  {"d":"2026-10-12","t":"네 건을 한 신청서로 묶기 — 본점이전·상호변경·목적추가·이사선임 (서류는 직접 만들어 둬 셀프로도 가능)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04817f8c33fb44f46ab8b2","cash":False},
  {"d":"2026-10-12","t":"법무사 선정·위임 — 10/12(월) 오전 통화 후 당일 맡기기 (본점이전+상호+목적+수권주식+공고방법 묶음) (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04815ca384d05bfc4917f1","cash":False},
  {"d":"2026-10-12","t":"마지막 기수 수강생 명단을 자체 채널(카톡·카페·멤버십)로 옮기는 동선 넣기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04816e9059df8108fdd0c7","cash":False},
  {"d":"2026-10-12","t":"정복녀 대표님 사업 구조화 페이지 배포 — 저장소 생성 후 push (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481a0a90ce7a5386fc2c0","cash":False},
  {"d":"2026-10-12","t":"정복녀 대표님 원크루 5회차(10월 1주차) 교육자료 발행 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea04813f9eb8e174e5930bbf","cash":False},
  {"d":"2026-10-12","t":"전부개정 정관으로 가기 — 등기부 목적 전사 + 사업연도 확인 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481999f5ac46281d758d7","cash":False},
  {"d":"2026-10-12","t":"기장 세무사무소에 사업연도 확인 — 1월 1일~12월 31일 맞는지 전화 한 통","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481a3a3c8f22c07545cd2","cash":False},
  {"d":"2026-10-12","t":"신정현 대표님에게 인감 신고 여부 확인 + 서류 3종 수령 (취임승낙서·인감증명서·주민등록초본)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481828875fd289fd43c1c","cash":False},
  {"d":"2026-10-12","t":"등록면허세 중과 여부와 '그 밖의 등기' 건수 확인 — 세액이 20만원 움직임","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481198a1ddb474a22c9fc","cash":False},
  {"d":"2026-10-12","t":"법인인감카드 분실 — 인터넷등기소 사용정지 + 법인인감도장 여부 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea04810aaa8ce141622c0e17","cash":False},
  {"d":"2026-10-12","t":"법무사 위임으로 가는 경우 서류 목록 — 위임장과 법인인감증명서가 추가된다","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481a58ee3c00fe5ab11fb","cash":False},
  {"d":"2026-10-12","t":"소액 테스트 프로토콜 문서화 — 초기 발주·리뷰 기준·가격 허용 범위·손절 조건","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea048178a51dcac4eccc0be0","cash":True},
  {"d":"2026-10-13","t":"박태경 대표님 원크루 — 5회차 완료(10/6) 후 교육자료 발행 → 10/13 6회차 준비","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481649ba4d4714240eaa7","cash":True},
  {"d":"2026-10-13","t":"사입 재고 처리 가이드라인 — 50일 경과 시 마진 조정 → 강사 처리 신청 목록 순차 처리","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bab38bf16e2cc7d963","cash":True},
  {"d":"2026-10-13","t":"2,000만 원 지출 세무 처리 방식 세무사 확인 후 결정 (1,000만 루크 지급 vs 2,000만 유지)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bb9730c3375a2dffc7","cash":True},
  {"d":"2026-10-13","t":"3자 플랫폼 계약서에 '수강생 명단·결제 창구·강의 콘텐츠 = 셀수다 소유' 조항 넣기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e7831bcfab5d83841e","cash":True},
  {"d":"2026-10-13","t":"강의 플랫폼 시행 전 선행 조건 4가지 — 인베이더 계약 정리 / 역할 분배 확정 / 라이브 장소 셋팅 / 광고 운영 셋업","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e388cec4dc7fe4a8eb","cash":True},
  {"d":"2026-10-13","t":"구글 계정 — 현재 노트북 외 다른 기기 전부 로그아웃","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048146a7a0c4bc30ac8402","cash":False},
  {"d":"2026-10-14","t":"최은봉 대표님 7회차 컨설팅 — 당근 광고 첫 숫자·쇼피 첫 주문·면접 결과 점검","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481cfb10dff9aeed7df2d","cash":False},
  {"d":"2026-10-14","t":"박종혁 본부장에게 물어볼 한 가지 — 카페 월 4,000명 만들 당시 광고비","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea04816ca069c910adc45cca","cash":False},
  {"d":"2026-10-14","t":"김종진 대표님 조사 결과·조사 로그 검토 후 다음 코칭 피드백","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea0481518c46c8db8a768cb7","cash":True},
  {"d":"2026-10-15","t":"힐링디어스(주) 본점이전 등기·사업자등록 정정 — 새 본점 주소 확보 완료(10/9), 10/12 법무사 위임 → 접수 → 등기 후 정정 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481a7b0c0cfc85f4b3475","cash":False},
  {"d":"2026-10-15","t":"4대보험 사업장 소재지 변경신고 — 변경일부터 14일","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bda5e2f2a8846531fd","cash":False},
  {"d":"2026-10-15","t":"블로그·인스타 자동화 프로그램 → '오프라인샵 팩'으로 정리 + 면책 화면 추가","who":"루크","p":"P1","n":"https://app.notion.com/p/3db0cf8fea0481d18720f2201f82b3b3","cash":True},
  {"d":"2026-10-15","t":"지영 내년 조달(최소 1억) 월별 마일스톤 확정","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-15","t":"공고방법을 홈페이지 게재로 변경 — 지금은 수원 경기신문으로 돼 있음","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04818d8bc4e8dd106ecd1c","cash":False},
  {"d":"2026-10-15","t":"미입고 자동 알림·반품 트리거 프로토타입","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-15","t":"[보류] 10월 정산 확인 전까지 하지 않을 것 — 재검토일","who":"루크","p":"P3","n":"https://app.notion.com/p/3d50cf8fea0481ae9cbdc532f42c5b95","cash":False},
  {"d":"2026-10-16","t":"박종혁 본부장 계약 전 닫을 다섯 칸 — 6:4 분모, 총액·PD 단가, 3PL 귀속, 중단선, 고정급 성질","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea04811ca54cf38b0d15e46f","cash":True},
  {"d":"2026-10-16","t":"변경등기 제출 — 기한 10/16(금) (상법 제182조 2주, 이전일 10/2 기준). 서류 완성, 남은 것은 사업연도 확인·날인·증명서 발급","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e8b9e1cc147d2b6a9c","cash":False},
  {"d":"2026-10-16","t":"사업자등록 정정신고 — 등기 완료 직후 (10/7 취하 건 재신청 · 등기사항전부증명서 첨부)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048138b075f9bb51f5e97e","cash":False},
  {"d":"2026-10-16","t":"미니쌤 채널 공지 3회 (2·4·8주차: 10/12주, 10/26주, 11/23주) — 카톡·카페·유튜브","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea0481dc8e86ef413c4e23c8","cash":False},
  {"d":"2026-10-17","t":"홍○○ 대표님 원크루 재문의 여부 확인 (10/3 상담 후속)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ee0cf8fea0481b58bcec3ba614eec0f","cash":True},
  {"d":"2026-10-17","t":"디노 전자책 제작 지원 여부 결정 · 역할 분담 합의 (플라우드 10/6)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481498097ea0e7aff1dff","cash":True},
  {"d":"2026-10-17","t":"뿌요 3화 '연쇄적금러' 촬영·편집 (대본 완성)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048145b330dd35994154e3","cash":False},
  {"d":"2026-10-18","t":"키티티 무료강의 라이브 → 저가 VOD 판매 오픈 + 개인 레슨 네이버 예약 등록","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea0481dc8934dc0c61d42b94","cash":True},
  {"d":"2026-10-19","t":"박종혁 본부장 사무실 좌석 마련 + 온보딩 지원 (플라우드 10/9 · 기한 추정 — 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea048178bbbbeb6b52524035","cash":False},
  {"d":"2026-10-20","t":"당근 2주 결과 판정 — 지속/수정/이동 답장 (최은봉 대표님)","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481eabc25d08c7f5019f3","cash":True},
  {"d":"2026-10-20","t":"초월스토리 파일럿 강사 후보 소개","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048167bc15f5dc0646b939","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 강사 협업이 끝나도 원크루 관계는 유지 — 계약 전 구두로 못 박기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b4b7c6ed7ab7329d8c","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 루크 참여 범위 확정 — 단순 플레이어 vs 공동 빌드업, 배분 초안 작성","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04817c8fc5e1e6c7681869","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 초월스토리 정산 기준 문서화 — '전체 매출' 정의, 비용 항목 목록, 8% 두 개(루크 수수료·광고비)의 관계","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04818c9a01c1346a18f643","cash":True},
  {"d":"2026-10-22","t":"초월스토리 — 루크 참여 범위를 공동 기획으로 올릴지 (5:5 분모에 들어가는지) 10/22 배분 초안 전에 제기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481faa420daf4c6647ca1","cash":True},
  {"d":"2026-10-22","t":"가을 대표님 몫 2,200만의 산출 근거 확인 — 루크 4가 880만인지 1,590만인지가 여기서 갈린다","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea04813fab69eb44001ba56d","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 6:4를 숨길지, 공동 기획으로 공개할지 — 10/22가 돌릴 수 있는 마지막 자리","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea048164bd27f5664acd603b","cash":True},
  {"d":"2026-10-22","t":"가을 대표님과 6:4 합의를 서면으로 남기기 — 대가가 기획·PPT·라이브 코칭이라는 점 명시","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481af8f59d05cd4111cad","cash":True},
  {"d":"2026-10-22","t":"초월스토리 광고 예산 약 4,500만 확인 + 상한·중단 기준 받아내기 (4,500만은 역산값 — 확인 전)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481c58f8cfd00f6266b69","cash":True},
  {"d":"2026-10-22","t":"가을 대표님에게 사전 설명 — 손익분기 18명이라는 사실과 광고비 리스크 미리 알리기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481d4b796fed4ccceb00f","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 상품 최종 확정 — 289만 단일 여부, 1:1 컨설팅반 포함 여부, 목표 객단가","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04816ca0fedde155dd3162","cash":True},
  {"d":"2026-10-24","t":"전환율 가정 검증 — 과거 3%와 목표 10% 사이에서 광고비 상한 정하기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481aa94bac8bcc8dcda8b","cash":True},
  {"d":"2026-10-24","t":"무료 라이브 특강 참석자 선물 준비 — 소싱처 전자책 + 자동 등록 프로그램 7일 이용권 (기한 추정 · 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481ab9090e503641c10b6","cash":False},
  {"d":"2026-10-25","t":"10/25 무료 라이브에 가을 대표님 게스트 10분 — 카메라 테스트 겸","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481a399bdc56ed0e95b78","cash":False},
  {"d":"2026-10-25","t":"유튜브·라이브 출연 고연령 성과자 섭외 (불발 시 대안 마련)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048104a2f5fc1bcdce6b0a","cash":False},
  {"d":"2026-10-25","t":"10/25 무료 라이브 특강 진행 — 4종 자판기 전체 사용법 + 저가 소싱 노하우 (시간 19:00는 10/2 녹음 언급값 · 신청 링크 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481969cd8e18631295ba8","cash":False},
  {"d":"2026-10-25","t":"단톡방 입장자 전원에게 자동 등록 자판기 7일 무료 이용권 지급 세팅 (고정 댓글 링크 포함)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481eab944dc24121d573c","cash":False},
  {"d":"2026-10-28","t":"가을(정복녀) 대표님 수락 시 3주 강사 런칭 준비 (1주 판매·방향 / 2주 커리큘럼·자료 / 3주 리허설·모객)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea048154938ac0f560b7918f","cash":True},
  {"d":"2026-10-29","t":"초월스토리와 협업 모델 옵션(플레이어 vs 공동 빌드업) · 배분 초안 확정","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481bc9b1ee702bcb74f48","cash":True},
  {"d":"2026-10-31","t":"일십백천 수강생 수경 브랜드 10월 재시동 지원 — 보조 품목 규칙 사전조사, 다음 컨설팅 일정 확정","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea048138a1e5d67100f3785c","cash":True},
  {"d":"2026-10-31","t":"최은봉 대표님용 성과 기반 파일럿 제안서·착수금 템플릿 초안 지원","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea04819aab6fcd94e751e645","cash":True},
  {"d":"2026-10-31","t":"키티티 창업 VOD 패키지 촬영·얼리버드 오픈 + 컨설팅·오프라인 클래스 모집","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea04816d9296fe49272eb87c","cash":True},
  {"d":"2026-10-31","t":"교육회사(셀러들의 수다)+3PL 법인 — 신규 설립 vs 힐링디어스 변경 결정","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea048121be35ee82635e54a4","cash":True},
  {"d":"2026-10-31","t":"개발비·유지비 구조 재검토 (월 300만 유지비, 초창패 지원금 지급 가능 여부)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048173948fe8555a9666e7","cash":True},
  {"d":"2026-10-31","t":"헤메인에서 파트너 의향 샵 10곳 사전 모집 (LOI)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04815d9190d01a06e342ef","cash":True},
  {"d":"2026-10-31","t":"키티티 ↔ 루크 협력 계약서 초안 (권리·운영 범위·수익 배분)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481388f9cc6a8fd0cd7db","cash":True},
  {"d":"2026-10-31","t":"키티티 모바일 홈페이지를 파트너샵용 템플릿으로 정리","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481a8a032d31b487841aa","cash":True},
  {"d":"2026-10-31","t":"지영 개인사업자 업종 추가(소프트웨어·정보서비스) 세무사 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04814ea30af644b4557feb","cash":True},
  {"d":"2026-10-31","t":"초창패 현금 자부담 714만~1,430만원 마련 계획","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481de99cac54fe595da94","cash":True},
  {"d":"2026-10-31","t":"지영 원장 전체 자격·수상·경력 목록 받기 + 증서 스캔 정리","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481f6a15cd2ca57eebfc2","cash":True},
  {"d":"2026-10-31","t":"헤메인 파트너 의향서 양식 만들기 (10월 말까지 3곳)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048120abdccf151e7b9c22","cash":True},
  {"d":"2026-10-31","t":"진단 결과 페이지에 웨딩·이벤트 패키지 연결","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04817cbde2e2a4b06313bd","cash":True},
  {"d":"2026-10-31","t":"지분을 주식 양도로 줄지 증자로 줄지 결정","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048169aebcfa74ae080329","cash":True},
  {"d":"2026-10-31","t":"메이븐 스토어 매출 우수 상품 링크 공유 받아 추가 판매 전략 세팅","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048109be61c95277b4895a","cash":True},
  {"d":"2026-10-31","t":"프로그램 구독 사이트 구축 — 수강생 라운지·부업 콘텐츠·비수강생 오픈","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481a6b029e7c48ac0c6cb","cash":True},
  {"d":"2026-10-31","t":"토스 결제 연동 + 깃허브 자동 설치·업데이트 세팅 (셀수다 프로그램)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048152a437c172a43f9993","cash":True},
  {"d":"2026-10-31","t":"재고 못 판 수강생 상품 위탁판매 + 판매 일지","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04817ca113c3318de00839","cash":True},
  {"d":"2026-10-31","t":"셀러 자동화 프로그램 구독 사이트 오픈 (수강생 라운지 + 비수강생 구독 + 부업 콘텐츠)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048194b729fa84b69c9a04","cash":True},
  {"d":"2026-10-31","t":"뿌요님 역할 · 수익 배분 결정 (한 달 알바 형태 지급 이후)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481ae9d38f223f112387b","cash":True},
  {"d":"2026-10-31","t":"물동량 일 200건 · 월 6,000건 확대 → 택배비 재협상","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481dcad6cf63ec1a3aef8","cash":True},
  {"d":"2026-10-31","t":"졸업 후 반복 매출 가격안 — 프로그램 월 구독(소싱·자동등록·CS) + 3PL 등급(보관 무료 기간 후 보관료·처분 수수료)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048137bd9ac4df5325f1d0","cash":True},
  {"d":"2026-10-31","t":"뿌요님 12월 이후 자체 수익 구조 설계 (메이브님 강의 의존도 낮추기)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481128cfad15cee935285","cash":True},
  {"d":"2026-10-31","t":"돈블지PD 오프라인 사업 수익 구조화 (플라우드 10/6 · 이름·기한 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04810a8527ca4796cb449c","cash":True},
  {"d":"2026-10-31","t":"지영 원장에게 확인 — 평균 객단가·월 예약 건수·재방문율·시술별 비중","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea048118bf45dc9a319738de","cash":True},
  {"d":"2026-10-31","t":"PG 수수료 요율과 실제 광고비 비율 숫자 확보 — 둘만 들어오면 배분표가 하나로 확정된다","who":"루크","p":"P1","n":"https://app.notion.com/p/3f30cf8fea04813d8880ee10ef500869","cash":True},
  {"d":"2026-10-31","t":"뷰셀 회차 주제 후보 22개 — 순서 확정과 확인 필요 수치 검증","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481e084eac0131859e2ca","cash":False},
  {"d":"2026-10-31","t":"설치 가이드·원격 지원 체계 마련 (AI 스튜디오)","who":"루나","p":"P1","n":"https://app.notion.com/p/3db0cf8fea048160983ee84dfa106f34","cash":False},
  {"d":"2026-10-31","t":"런칭 광고 테스트 3회 (총 350만) — 300만 툴킷 프로그램","who":"루크","p":"P1","n":"https://app.notion.com/p/3db0cf8fea04811b920ed934eddfadd5","cash":False},
  {"d":"2026-10-31","t":"헤메네일 가격비교 → AI 진단 링크 연결 (보조 송객 채널)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048134b9ede80fe9d7ed0f","cash":False},
  {"d":"2026-10-31","t":"업무용 맥북 교체 (중고 M4 맥북에어 16GB 검토, M1 에어는 중고 판매)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04817bba04cb14d260f50f","cash":False},
  {"d":"2026-10-31","t":"Vercel 팀을 Pro($20/월)로 바꿀지 결정 — 무료(Hobby)는 비상업 전용인데 공방 유료 결제 운영 중","who":"담당 미기재","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481ab90bcfc0684789878","cash":False},
  {"d":"2026-10-31","t":"원크루 사이트 4단계 — 로그인·가입 + 원크루 회원 표 + 회원 넣기/빼기 관리자 화면","who":"담당 미기재","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048181a121fa70732b2b17","cash":False},
  {"d":"2026-10-31","t":"멘토루크 파인더 — 네이버 쇼핑 검색 API 종료(2026-07-31) 대응","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481deb27cffcc5b9737ca","cash":False},
  {"d":"2026-10-31","t":"원크루 라운지에 처음 열어 둘 자료 하나 정하기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f00cf8fea0481aea406c7180d0e367b","cash":False},
  {"d":"2026-10-31","t":"법인 서류 클라우드 폴더 만들기 — 정관·주주명부·의사록 비치 의무","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048167b10bd8cdca622f78","cash":False},
  {"d":"2026-10-31","t":"창고형 매장 후보지 3~5곳이 과밀억제권역 밖인지 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481c090bdf661e6f1909f","cash":False},
  {"d":"2026-10-31","t":"3PL 창고가 취득세 중과 제외 업종(창고업)에 해당하는지 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481e4a556efe81d008760","cash":False},
  {"d":"2026-10-31","t":"꼬마빌딩 — 목표 지역(과밀억제권역 안/밖)·시점·법인 명의 여부 정하기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048139849cd98e17f636fc","cash":False},
  {"d":"2026-10-31","t":"힐링디어스로 받을 매출 하나 정하기 — 휴면법인 판정 회피용","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481ef9569dc5122402d95","cash":False},
  {"d":"2026-10-31","t":"주소가 박혀 있는 것들 전부 교체 — 세금계산서·통장·스마트스토어·플레이스·거래처","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04818e88b0cfcbbe3d2313","cash":False},
  {"d":"2026-10-31","t":"초월스토리 런칭용 성과자 섭외 — 고연령 성과자(유튜브) + 성과자 2명(라이브), 본인 동의","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048113a71ada0c8358b93e","cash":False},
  {"d":"2026-10-31","t":"'사입으로 수익 낸 사례' 사입 특강 지속 개최","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048155bd03fce5658072dc","cash":False},
  {"d":"2026-10-31","t":"[결정 필요] 쿠팡 가격비교 크롤링 — 플랫폼 정책 검토 후 개발 여부 결정","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481ab824fdb0460ef0cef","cash":False},
  {"d":"2026-10-31","t":"헤어·메이크업 가격비교 사이트 + 커뮤니티 구축 완료 (공지된 가격만 사용)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481de9320eb05efd9034d","cash":False},
  {"d":"2026-10-31","t":"'사입으로 수익 낸 사례' 특강 정기 개최 일정 잡기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04811fbddde6fcbdd31d1e","cash":False},
  {"d":"2026-10-31","t":"프로그램 소개 유튜브 콘텐츠 (다양한 자동화 프로그램 어필)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481ef9dd8d191235f8204","cash":False},
  {"d":"2026-10-31","t":"6기·4기 수강생 성과·후기·비포애프터 수집 — 신규 플랫폼 1기 모집용 증거","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481838b77ff04c8c73200","cash":False},
  {"d":"2026-10-31","t":"뿌요님 목표 수익 관리 페이지 — 원크루로 제작 (프롬프트 준비됨)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04814ab443d10fda25aa0d","cash":False},
  {"d":"2026-10-31","t":"지영 원장에게 빌드업 페이지용 숫자 4가지 받기 — 매출·순이익·본인 몫, 목표 주택 위치·평형, 건물 매입 vs 신축, 목표 차량 모델명","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea0481a78df0ec77cc00af96","cash":False},
  {"d":"2026-10-31","t":"새 저장소 kittiti-jiyoung 생성 + Pages 켜기 (루크 직접)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea0481859045f9b892eb6fa9","cash":False},
  {"d":"2026-10-31","t":"crew.json 형식을 기존 원크루 자료실 규칙과 맞출지 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea048108aabccb4ecbf32b15","cash":False},
  {"d":"2026-10-31","t":"크루원 페이지 슬러그 규칙 확정 + 첫 사람에게 시험 적용","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea04812b8bb7fe957320fb6f","cash":False},
  {"d":"2026-10-31","t":"등기 끝난 뒤 할 일 10가지 — 사업자등록 정정, 법인인감 재제작, 사무실에 상호 통지, 통신판매업 변경신고","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea0481c99265f4b17f2ddc0c","cash":False},
  {"d":"2026-10-31","t":"법인 지방세 체납 여부 확인 — 위택스에서 납세증명서 발급을 시도해 보기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea048118a682f449e8f920fa","cash":False},
  {"d":"2026-10-31","t":"유튜브 콘텐츠 전략 재구성 — 수강생 성장 스토리 + 전문가 인사이트 (박종혁 본부장과 공동 · 플라우드 10/9 · 기한 추정 — 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea048172858acfe572f69aad","cash":False},
  {"d":"2026-10-31","t":"배민(B마트·배민스토어) 화장품 판매 채널 입점 가능성 확인","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea0481069327e3ef0da7a08d","cash":True},
  {"d":"2026-10-31","t":"블로그타이퍼 v3 — 구독 서비스(로그인·요금제별 기능·정기결제)","who":"루크","p":"P2","n":"https://app.notion.com/p/3d80cf8fea0481338e3ad7836584222b","cash":True},
  {"d":"2026-10-31","t":"블로그타이퍼 v2 — 내 인스타 수집(Graph API) → 글 발행 + 네이버 예약 발행","who":"루크","p":"P2","n":"https://app.notion.com/p/3d80cf8fea04818c9c36d5d109693855","cash":True},
  {"d":"2026-10-31","t":"전국 도매처·B2B 소싱 리스트 v3 검토 → 수강생 소싱 자료로 활용","who":"루크","p":"P2","n":"https://app.notion.com/p/3d80cf8fea04815ea60fe87f517b312f","cash":True},
  {"d":"2026-10-31","t":"전자책 제작 — 「불평만 하고 도전은 안 하는 비겁한 사람들」","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea0481299b1aeaf71e8c9536","cash":False},
  {"d":"2026-10-31","t":"전자책 제작 — 「끼리끼리 모이면 실패하는 이유」","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea04814f95baf68f427b5ea8","cash":False},
  {"d":"2026-10-31","t":"헤메네일 뷰티 트렌드 피드 구축 — 네이버 공식 검색API(블로그·뉴스) + 댓글·공유","who":"루크","p":"P2","n":"https://app.notion.com/p/3e00cf8fea04813eba93e475997268d3","cash":False},
  {"d":"2026-10-31","t":"블로그 테스트 임시저장 글 8개 + 테스트 댓글·답글 정리","who":"루크","p":"P2","n":"https://app.notion.com/p/3dc0cf8fea0481a388f6d59925327338","cash":False},
  {"d":"2026-10-31","t":"헤메네일 시세판 외부 공개 배포 (Vercel+Supabase) 여부 결정","who":"루크","p":"P2","n":"https://app.notion.com/p/3dc0cf8fea0481daa0b4c8b5b2d2065a","cash":False},
  {"d":"2026-10-31","t":"'위탁판매' 대신 쓸 루크만의 네이밍 만들기","who":"루크","p":"P2","n":"https://app.notion.com/p/3d60cf8fea04818083c0da4d257a3b9f","cash":False},
  {"d":"2026-10-31","t":"40대 수강생 성공 사례자 섭외 (공동 출연 콘텐츠)","who":"루크","p":"P2","n":"https://app.notion.com/p/3d60cf8fea04818fa3f4cb55a467649d","cash":False},
  {"d":"2026-10-31","t":"Claude API 연결 대화형 프로그램 — AI 답변을 내 목소리로 출력","who":"루크","p":"P2","n":"https://app.notion.com/p/3d50cf8fea0481919088e5b85e714cc1","cash":False},
  {"d":"2026-10-31","t":"텍스트→오디오 파일 생성 프로그램 (입력창+저장, 대본 배치 처리)","who":"루크","p":"P2","n":"https://app.notion.com/p/3d50cf8fea0481aa8c6ef66e0bb6d518","cash":False},
  {"d":"2026-10-31","t":"개인 트레이드 채널 개설·운영 시작 (기한 추정 · 확인 필요)","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea0481c99703fd2ab39116e4","cash":False},
  {"d":"2026-10-31","t":"'하루를 4번 쓰는 법' 영상 — 6h×4 슬롯 설계 초안 → 7일 파일럿 → 대본·촬영·발행 (기한 추정 · 확인 필요)","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea0481179e23f70b21ce0c10","cash":False},
  {"d":"2026-10-31","t":"전자책 제작 — 주제 「부자들은 하고 가난한 사람들은 하지 않는 말」","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea048100a595f978bb543814","cash":False},
  {"d":"2026-10-31","t":"수파베이스 전용 프로젝트 분리 여부 결정 (Pro 업그레이드 또는 기존 프로젝트 정리)","who":"루크","p":"P2","n":"https://app.notion.com/p/3ec0cf8fea048134aac2dbc802115811","cash":False},
  {"d":"2026-11-08","t":"창고형 매장 우리 재고로 4주 시범 판매 · 주간 매출·판매율 기록","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048113a3d7c503eec00deb","cash":True},
  {"d":"2026-11-30","t":"메이크업헬퍼 12주 테스트 9주차 판정 (11월 말)","who":"루크·최은봉","p":"P1","cash":True},
  {"d":"2026-11-30","t":"트리플 루프 빈 칸 설계 — 지영 채널 자체 수익(협찬·광고) + 실물 제품 유통 아이템","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea0481dd8721d7c5260db6d1","cash":True},
  {"d":"2026-11-30","t":"내년 초 서울 이전·건물 매입 대비 사업 로드맵 수립 (기한 추정 · 확인 필요)","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea048126844ad335f1aefd2e","cash":True},
  {"d":"2026-11-30","t":"힐링디어스(주) 업력·매출 기준 2027 정부지원사업(초창패·디딤돌·도약패키지) 지원 가능 여부 확인","who":"루크","p":"P2","n":"https://app.notion.com/p/3ec0cf8fea04810e84d3e7ceb43c766d","cash":True},
  {"d":"2026-11-30","t":"수강생 입점 조건 문서 — 수수료 15~20%·정산 주기·보관 기간·미판매 반환 (시범 판매 숫자 확인 뒤 공개)","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea048140bac9e2248d943be0","cash":True},
  {"d":"2026-11-30","t":"서울 이전 후보 빌딩 · 공동 투자자 정보 수집 (계약 판단은 반복 매출 확인 후)","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea048148b8a6eb95f9649d5d","cash":True},
  {"d":"2026-11-30","t":"1인 사업자용 블로그·카톡 자동화 구독 사이트 기획","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea04819e984acdd675ae57bb","cash":True},
  {"d":"2026-11-30","t":"사업자 실행 관리 웹앱(PWA) 1차 — 11월 착수","who":"루크","p":"P2","n":"https://app.notion.com/p/3db0cf8fea0481349f2adefbadef023c","cash":False},
  {"d":"2026-11-30","t":"[결정 필요] 헤메네일 카카오 로컬 API로 추천 1~3위 업종 실시간 대조 — 표시만 vs 순위 반영","who":"루크","p":"P2","n":"https://app.notion.com/p/3ee0cf8fea048171ad3ef13b0f780e44","cash":False},
  {"d":"2026-11-30","t":"서울 빌딩 후보 정보 수집 + 공동 투자자 — 이전할지 미룰지 먼저 결정","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea0481ab946eebb2fe19821b","cash":False},
  {"d":"2026-11-30","t":"쿠팡 가격 비교 프로그램 — 개발 전 크롤링 정책 위험 검토","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea0481188729f52df28c4e34","cash":False},
  {"d":"2026-11-30","t":"답변 웹페이지 발행 위치를 깃허브에서 원하는 위치로 바꾸기","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea0481789832f2fffe8102c8","cash":False},
  {"d":"2026-11-30","t":"박종혁 협업 커머스 — 소싱 자동화 프로그램 테스트 + 위탁 중심 물류 운영 체계 설계 (플라우드 10/9 · 기한 추정 — 확인 필요)","who":"루크","p":"P2","n":"https://app.notion.com/p/3f40cf8fea04813cb438ce0216f8b59c","cash":False},
  {"d":"2026-12-10","t":"뿌요 90일 결산 상담 — 300만 달성 여부·거취 결정","who":"루크","p":"P3","n":"https://app.notion.com/p/3d80cf8fea0481d69c3de62608ad02ac","cash":True},
  {"d":"2026-12-31","t":"루크 툴박스 구독 500명 목표 / 3PL 판매 실적 정리(내년 강의 증거)","who":"루크","p":"P1","cash":True},
  {"d":"2026-12-31","t":"회사 자체 강의 기획 (3PL 판매 실적 연계)","who":"루크","p":"P2","n":"https://app.notion.com/p/3de0cf8fea0481b9821dc015183213b4","cash":True},
  {"d":"2026-12-31","t":"초창패 PSST 계획서 초안 12월 안에 완료","who":"루크","p":"P2","n":"https://app.notion.com/p/3ef0cf8fea0481859a20e212db58d884","cash":True},
  {"d":"2026-12-31","t":"메이븐 스토어 4분기 순수익 월 1,000만","who":"메이브님","p":"P2","n":"https://app.notion.com/p/3f10cf8fea04811aa006c92f5797461a","cash":True},
  {"d":"2027-01-31","t":"꼬마빌딩 담보대출 심사 전에 대표자 신용 정리 마치기 (잔금은 2027-03-16 이후)","who":"루크","p":"P2","n":"https://app.notion.com/p/3f20cf8fea048176bc01e7f629aa7309","cash":True},
  {"d":"2027-03-16","t":"서울 꼬마빌딩 잔금은 2027-03-16 이후로 — 용도로는 중과를 못 피함","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea048189a9b5cdd665a5cd92","cash":False},
  {"d":"2027-03-16","t":"꼬마빌딩 취득은 2027-03-16 이후로 — 설립 5년 충족일","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea04819f838bcf83d9a08e94","cash":False},
]

def page(title, body, root="../"):
    return HEAD.format(title=title, site=SITE, css=CSS, root=root, updated=UPDATED) + body + FOOT.replace("{site}",SITE).replace("{updated}",UPDATED).replace("{root}",root)

# ---------------------------------------------------------------- 허브
INDEX = """
<div class="hero">
  <h1>내 연봉 10억 만들기</h1>
  <div class="sub">루크(유믿음) · 우선순위 · 로드맵 · 매일 추천 일정</div>
  <div class="goal">
    <div><b>10억</b><span>12개월 귀속매출 목표</span></div>
    <div><b>3,000~4,000만</b><span>강의와 무관한 신규 파이프라인 월 순수익 (2~3개월 내)</span></div>
    <div><b>1~2명</b><span>원크루 전환 (3,300~3,900만)</span></div>
  </div>
</div>

<h2>오늘의 추천 일정 <small id="today"></small></h2>
<div class="card accent" id="todayBox">
  <div class="empty">불러오는 중…</div>
</div>
<div class="card">
  <h3>이번 주 리듬</h3>
  <div class="week" id="week"></div>
  <div class="note">월 파이프라인 점검 · 수 대본 검토 · 목 배치 촬영 · 금 발주·공지 · 토 컨설팅 자료 · 일 주간 정리. 하루는 6시간×4 슬롯으로 (9/29 메모).</div>
</div>

<h2>이번 주 최우선 <small>현금에 가깝고 선행 조건일수록 위</small></h2>
<div class="card">
  <ul class="list tasks">
    <li data-n="https://app.notion.com/p/3f10cf8fea0481b3bd6dc3d1bfd8fa95"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 루크 툴박스 결제 — 포트원 결제사를 가입비 무료인 곳(KG이니시스)으로 확정하고 신청서 제출 · 070 번호 받기 · 통신판매업 신고번호·환불 기준 확인</div><div class="m">10/7 상황판 '막힘' 보고 11건(토스 연결 점검 → 토스 신청 멈춤 권고 → 포트원으로 결정 → 약관·개인정보처리방침·환불안내 배포, 결제 심사 사전 점검 8/9 통과) · 포트원 이용료는 월 거래액 5,000만원까지 무료, 결제사 가입비는 두 곳만 무료 · 토스는 테스트 키 상태라 지금은 손님이 결제해도 청구가 안 됨 — 실결제 전까지 프로그램 구매 길을 막을지도 결정 · 사업자등록증은 옛 주소본이라 홈택스 재발급 필요 · <a href="status/?p=루크 툴박스">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481a89c87d347be379b54"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 원크루 사이트 자동 배포 — 크롬 'Confirm access' 탭에서 깃허브 비밀번호 입력 후 Confirm (루크 클릭 한 번)</div><div class="m">10/6 상황판 '막힘' 보고 · Vercel에 깃허브 로그인 연결은 끝났고, 원크루 사이트 저장소 접근 권한 단계에서 대기 · 그동안 크루 자료는 수동 배포 중 · <a href="status/?p=원크루 사이트">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea048152b55cec152c0f6fc9"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 사업 구조화 페이지 4건 — 루크가 깃허브에서 저장소 만들고 Pages 켜기 (지영 원장 kittiti-jiyoung · 신정현 대표 onecrew-shin-jeonghyeon · 정복녀 대표님 · 최은봉 대표님 onecrew-ceb-fxddzyg9)</div><div class="m">10/7 노션 '[막힘]' 항목 · 페이지는 각 채팅에서 만들어 두었고 저장소가 없어 push 대기 · 공개 저장소 생성 → Pages(main / root) → Claude 깃허브 앱 권한 추가 · 기한 10/7~10/12 · 정복녀 대표님 저장소 이름은 기록에 없어 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea04818a937efb1274c10b22"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 키티티 AI 상담 — GPT 연결용 OpenAI API 키 발급(루크) · 원장님께 상담 정책 10가지 답 받기</div><div class="m">10/5 상황판 '막힘' 보고(상담실장 페르소나·가상 손님 9명 시험) · ChatGPT 구독과 API 키는 별개 — 키만 넣으면 연결되도록 코드는 준비됨(실제 호출은 미확인) · 정책 10가지: 소요 시간·2인 예약·할인·출장·결제·아기 동반·헬퍼/환복·토요일 오후·본식 업스타일·클래스 · <a href="status/?p=키티티 상담 사이트">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048144b71af1d096a2f0a2"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 루크 툴박스 — 자동화 도구 판매 조건(환불 기준·설치 대수·윈도우/맥·네이버 계정 처리·결제 방식) · 원크루 페이지 결정 5가지 + 루크 사진·영상</div><div class="m">10/5 상황판 '막힘' 보고(도구 구매 검토 회의) · 도구가 눈에 안 보임 1.6/5, 99만원 이상 구매 의향 2명(조건부) · 원크루 페이지 결정 5가지: 2명 고정·안심 문구·빚 문구·평생 범위·계산기 3년 · 도구 1단계(준비 중 표시 정리·로그인 전 상세)는 클로드가 바로 가능 · <a href="status/?p=루크 툴박스">상황판</a></div></li>
    <li><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 헤메네일 — 카카오 지도에 없는 매장을 순위에 소폭 반영할지</div><div class="m">10/4 상황판 '막힘' 보고(폐업 의심 매장 순위 내리기) · 함께 물었던 상가(상권)정보 대조·전화번호 표시·가격 최신화는 10/5 노션에서 완료 처리됨 · 이 건은 결정 기록이 없어 확인 필요 · <a href="status/?p=헤메네일">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048141a4aee0ab6b56da87"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 키티티 정부지원 — 초창패 본선 + 모두의 창업 보험으로 갈지 · 이종 사업자 등록 방식(업종 추가 vs 새 사업자)</div><div class="m">10/4 노션 [보고] '정부지원 전략 v13' 메모의 '[막힘] 루크 결정 필요' (노션 상태는 완료) · 다음: 창업진흥원 1357·세무사 확인, 트랙(일반/기술 vs 로컬) 결정 · <a href="reports/kititi-grant-strategy/?v=13">보고서</a></div></li>
    <li data-g="developer-accounts"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 (Apple · Google Play · Microsoft)</div><div class="m">툴박스·영상공장·블로그타이퍼를 폰·맥·윈도우로 배포하는 모든 일의 앞단. Apple은 승인에 며칠 걸림 · 기한 10/2 지남(노션 미완료)</div></li>
    <li data-g="platform-director-meeting"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">박종혁 본부장 협업 — 10/9 회의 진행(녹음) → 계약 전 닫을 다섯 칸(6:4 분모 · 총액·PD 단가 · 3PL 귀속 · 중단선 · 고정급 성질) 기한 10/16 · 그 전에 물어볼 한 가지: 카페 월 4,000명 만들 당시 광고비(10/14)</div><div class="m">플라우드 10/9 녹음 요약: 초기 3개월 월 300만 고정(용역 형태) 요청 · 수익 6:4(본부장:루크) · 3개월 안에 네이버 카페 신규 회원 3,000명이 지속 여부 기준 · 10월 중순 이후 시작 — 계약은 아직 미확정 · 3개월 총액은 양쪽 숫자가 달라 <b>확인 필요</b>(노션 메모: "천만에 전부 포함" vs "천만 + 광고 900만") · 6:4의 분모(매출인지 광고·PD 차감 후인지)에 따라 손익분기 21명 vs 33명 · 노션 '10/8 종혁 본부장 미팅'·'3자 미팅 제안서 검토'는 미완료 — 끝났으면 완료 처리, 3자 1:1:1 안과의 관계는 정리 필요 · 시행 전 선행 조건 4가지·계약서 소유 조항(기한 10/13) · 플라우드 Action Item으로 노션 새 항목 3건(좌석·온보딩 10/19 · 유튜브 전략 10/31 · 소싱 자동화·위탁 물류 11/30, 기한은 추정) · <a href="park/">협업 평가</a> · <a href="platform/">전략 페이지</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481e8b9e1cc147d2b6a9c"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">10/16(금) 변경등기 제출(기한이 10/15에서 하루 늦춰짐) — 10/12(월): 기장 세무사무소에 사업연도 확인 · 신정현 대표님 인감 신고 여부 확인+서류 3종 수령 · 등록면허세 중과 여부 확인 · 법인인감카드 사용정지 · 법무사 위임 시 위임장·법인인감증명서 준비</div><div class="m">10/9 노션 [결정] 3건: 본점 이전일 2026-10-02(사무실 계약서 기준 → 등기 기한 10/16) · 정관은 전부개정(설립 정관 분실 전제) · 유믿음 대표이사 선임(신정현 대표님은 대표권 없는 사내이사) · 서류는 구글 드라이브에 작성돼 있고 루크 확정 4가지·출력·날인이 남음(기한 10/9 지남 · 노션 진행 중) · 10/8 [결정]: 법무사에게 10/12(월) 위임 · 정관을 전부개정으로 가므로 '정관 찾기'(10/10)·'정관 원본 본점 조항 확인'(10/9) 항목은 완료 처리 확인 필요 · [결정 필요] 셀러들의 수다 = 힐링디어스 상호변경 확정(10/11) · 등기 뒤 4대보험 소재지 변경(10/15)·사업자등록 정정(10/16) · <a href="registry-forms/">등기 서류</a> · <a href="registry-prep/">준비물 체크리스트</a> · <a href="relocation/">등기 페이지</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048126a2fec9d1efd1c0eb"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">초월스토리 강사 협업 — 계약서 정산 기준 정리·가을 대표님 성과 숫자·일정 확인(기한 10/11) · 강사 파트너 제안서 전달·의사 확인(10/12) · 10/22 전에: 2,200만 산출 근거·광고 예산 확인, 6:4 합의 서면화</div><div class="m">파일럿 강사는 가을(정복녀) 대표님으로 확정(10/7 · 노션 '파일럿 강사 선정' 완료) · 10/8 노션 새 항목 6건: 가을 대표님 몫 2,200만 산출 근거 확인 · 광고 예산 약 4,500만(역산값 — 초월스토리 확인 전) 확인 + 상한·중단 기준 · 가을 대표님께 손익분기 인원·광고비 리스크 사전 설명 · 6:4 합의 서면화 · [결정 필요] 6:4를 숨길지 공동 기획으로 공개할지(이상 10/22) · PG 수수료 요율·실제 광고비 비율 확보(10/31) · 10/7 원크루 세션 녹음 요약: 11월 초 촬영·11월 말 런칭 언급 — 10/6 회의의 '12월 초 라이브'와 달라 <b>확인 필요</b> · 수락 시 3주 런칭 준비(10/28) · 10/6 회의 구두 합의(노션 [결정]): 루크 수수료 = PG 제외 전체 매출의 8%, 순수익은 초월스토리:강사 5:5, 289만 단일 상품 유력 · [결정 필요] 참여 범위·정산 기준 문서화·원크루 관계 유지(10/22) · <a href="chowol/">초월스토리 페이지</a> · <a href="pilot/">파일럿 강사 결정</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481b2b5f9c0ab5aa17594"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">인베이더 종료 대비 — 종료 사실(범위·시점·출처) 확인 · 메이브님과 마지막 기수 공동 대응 합의 (기한 10/8 지남 · 노션 미완료)</div><div class="m">계약서의 수강생 명단·콘텐츠·후기 소유 조항 확인(10/11) · 마지막 기수 명단을 자체 채널로 옮기는 동선(10/12) · 사입 재고 처리 가이드라인(10/13) · <a href="invader/">인베이더 종료 대비</a></div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea0481a89260d919b12e75c3"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">키티티 토탈샵 — 10/8(목) 임대차·권리양수도 계약 체결(녹음 기준) → 인테리어 승인 별첨 문서 준비 · 특약 수정안 협상 마무리 확인 (기한 10/11)</div><div class="m">플라우드 10/8 녹음 3건 요약: 2·3층 임대차 계약 서명·날인, 권리양수도 계약 함께 진행, 잔금일 12/31, 렌트프리 1개월, 1월 말 가오픈 계획 · 노션 '키티티 계약'은 아직 '시작 전', '특약 수정안 협상'은 '진행 중' — 끝났으면 완료 처리 필요 · 금액은 녹음 요약끼리 맞지 않는 숫자가 있어 싣지 않음(<b>확인 필요</b>) · 3층 창문 처리 방안은 인테리어 업체와 정해 임대인에게 전달(임차인 측 할 일)</div></li>
    <li data-g="3pl-resale"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">3PL 수강생 재고 당근·외부 판매 첫 등록</div><div class="m">동의서(수수료 15~20%) → 재고 시트 판매 열 + 사진 → 당근 비즈프로필 → 30개 등록 · 통신판매업 신고 사업자 명의 필수 · 기한 10/1 지남(노션 미완료)</div></li>
    <li data-g="dino-12weeks"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">디노(미니쌤) 12주 빌드업 합의 → 10/5 1주차 시작</div><div class="m">기한 10/4·10/5 지남(노션 진행 중) — 합의·시작 여부 확인 필요 · AI 셀러 실무 교육 · 1달 90 / 2달 200 / 3달 350만 기준 · 상품별 배분 비율 확정</div></li>
    <li data-g="onecrew-inquiry"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">원크루·툴박스 문의 대응 — 가격 안내 후 상담 통화</div><div class="m">원크루 정가 3,900만 / 수강생 출신 3,300만 · 일십백천 990만 · 툴박스 사전 신청 안내 문구 확정 · 10/2 평생컨설팅 문의(뷰셀 수강생)에 답장 발송 → 회신 오면 진단 상담 일정 확정(기한 10/3) · 10/3 원크루 상담(홍○○ 대표님) 리포트 링크 발송(기한 10/4) → 10/17 재문의 여부 확인</div></li>
    <li data-g="free-live"><span class="tag p0">P0</span><div class="t">10/25(일) 6기 무료 라이브 — 신청 링크 확정 · PPT·수강생 인터뷰 5명·남은 미결정 사항 (기한 10/11)</div><div class="m">날짜 <b>10/25</b>·모델명 '반자동 사입'·참석자 7일 이용권은 10/4 노션 [결정]으로 확정 · 시간 19:00는 10/2 녹음 언급값, 신청 링크는 <b>확인 필요</b> · 록터뷰 2회차 영상 설명란·고정댓글에 링크 → 신규 리스트 확보</div></li>
  </ul>
</div>

<h2>페이지</h2>
<div class="grid nav">
  <a href="roadmap/"><b>돈 버는 로드맵</b><span>수익 줄 · 3단계 · 원칙</span></a>
  <a href="priority/"><b>우선순위</b><span>P0 → P3 · 보류 목록</span></a>
  <a href="people/"><b>사람별 현황</b><span>메이브님·디노·뿌요·지영</span></a>
  <a href="schedule/"><b>일정 도식</b><span>10월 타임라인 · 마일스톤</span></a>
  <a href="invader/"><b>인베이더 종료 대비</b><span>10/6 들은 이야기 · 마지막 기수에 챙길 것</span></a>
  <a href="corp/"><b>힐링디어스 → 셀러들의 수다</b><span>경기 창고형 매장은 지금 · 서울 빌딩은 2027-03-16 이후</span></a>
  <a href="relocation/"><b>10/15 등기 — 등기부 확인 끝</b><span>중임은 완료 · 본점이전 + 상호 + 목적 + 수권주식</span></a>
  <a href="money/"><b>재정 정리 — 무엇부터 털어야 하나</b><span>대환 우선순위 · 금리 순서 · 시트는 26년 5월 기준</span></a>
  <a href="credit/"><b>신용점수 — KCB 622 / NICE 750</b><span>농협 카드 거절 이유 · 꼬마빌딩 대출 심사와의 연결</span></a>
  <a href="crew-prompt/"><b>크루원 사업 구조화 — 프롬프트</b><span>기존 흐름에 얹는 짧은 버전 · 이름·충돌·노출만</span></a>
  <a href="jiyoung-prompt/"><b>지영 원장 빌드업 페이지 — 프롬프트</b><span>새 저장소로 만들 때 복사해 쓸 프롬프트</span></a>
  <a href="jiyoung-survey/"><b>지영 설문지 발표 — 쪽마다 할 말</b><span>받은 피드백 → 고친 것 → 안 고친 이유</span></a>
  <a href="vault/"><b>셀프 등기 · 정관 찾기 · 서류 보관</b><span>법무사를 쓸지, 정관은 어디서 찾는지</span></a>
  <a href="registry-forms/"><b>등기 서류 — 다 만들어 뒀습니다</b><span>서류 8장 · 준비물·비용·동선 전부 · 대표이사 쟁점</span></a>
  <a href="registry-prep/"><b>등기 변경 — 준비물 체크리스트</b><span>금요일에 할 것 · 신정현 대표님 준비물 · 기한 10/15</span></a>
  <a href="iros/"><b>등기부 열람 — 클릭 순서</b><span>인터넷등기소에서 중임 기록 확인하기 (700원)</span></a>
  <a href="pilot/"><b>파일럿 강사 결정</b><span>가을 대표님으로 확정 (10/7) · 결정 근거</span></a>
  <a href="park/"><b>박종혁 본부장 협업 — 평가</b><span>10/10 수정판 · 네 가지 철회 · 남은 세 칸과 밀도 지표</span></a>
  <a href="chowol/"><b>초월스토리 강사 협업</b><span>10/6 계약 조건 · 12월 런칭 · 어긋나는 숫자</span></a>
  <a href="maven/"><b>메이브님 공동 액션 플랜</b><span>10/6 회의 — 구독·스토어·오프라인 3축</span></a>
  <a href="universe/"><b>사업 유니버스</b><span>지금 돌아가는 것 전부 — 지도</span></a>
  <a href="philosophy/"><b>삼각 파이프라인</b><span>원크루 · 일십백천 · 불씨 이론</span></a>
  <a href="platform/"><b>강의 플랫폼 전략</b><span>유입 · 락인 · 플레이어 3자 구도</span></a>
  <a href="guides/"><b>할 일 설명서</b><span>항목별 어떻게 하는지 단계별</span></a>
  <a href="status/"><b>상황판</b><span>모든 채팅·코드의 완료·진행 보고</span></a>
  <a href="grants/"><b>정부지원사업</b><span>키티티·메이브님·디노·뿌요 2026 → 2027</span></a>
  <a href="sources/"><b>출처·갱신</b><span>기록 근거 · 업데이트 방법</span></a>
</div>

<script>
const EVENTS = __EVENTS__;
const P = {P0:'p0',P1:'p1',P2:'p2',P3:'p3'};
function ymd(d){const z=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate());}
const now = new Date(); const today = ymd(now);
const days=['일','월','화','수','목','금','토'];
document.getElementById('today').textContent = today.replace(/-/g,'.')+' ('+days[now.getDay()]+')';
const dayN = s=>Math.round((new Date(s+'T00:00:00')-new Date(today+'T00:00:00'))/86400000);
const PR = {P0:0,P1:1,P2:2,P3:3};
const byPri = (a,b)=>(PR[a.p]-PR[b.p])||((b.cash?1:0)-(a.cash?1:0))||(a.d<b.d?1:-1);
const over = EVENTS.filter(e=>dayN(e.d)<0 && dayN(e.d)>=-14).sort(byPri);
const older = EVENTS.filter(e=>dayN(e.d)<-14).length;
const td = EVENTS.filter(e=>e.d===today).sort(byPri);
const up = EVENTS.filter(e=>dayN(e.d)>0 && dayN(e.d)<=3).sort((a,b)=>(a.d<b.d?-1:a.d>b.d?1:byPri(a,b)));
const TOP = 7;
function li(e,label){return '<li data-n="'+(e.n||'')+'" data-g="'+(e.g||'')+'"><span class="tag '+P[e.p]+'">'+e.p+'</span>'+(e.cash?'<span class="tag cash">현금</span>':'')+(label?'<span class="tag">'+label+'</span>':'')+'<div class="t">'+e.t+'</div><div class="m">'+e.who+' · '+e.d.slice(5).replace('-','/')+'</div></li>';}
let html='';
if(td.length) html+='<h3>오늘</h3><ul class="list tasks">'+td.map(e=>li(e)).join('')+'</ul>';
if(over.length){
  html+='<h3 style="margin-top:12px">지난 기한 '+over.length+'건 (P0·현금부터)</h3><ul class="list tasks">'+over.slice(0,TOP).map(e=>li(e,'D'+dayN(e.d))).join('')+'</ul>';
  if(over.length>TOP) html+='<details class="donebox"><summary>지난 기한 나머지 '+(over.length-TOP)+'건 펼치기</summary><ul class="list tasks" style="margin-top:8px">'+over.slice(TOP).map(e=>li(e,'D'+dayN(e.d))).join('')+'</ul></details>';
}
if(up.length) html+='<h3 style="margin-top:12px">다가오는 3일</h3><ul class="list tasks">'+up.map(e=>li(e,'D+'+dayN(e.d))).join('')+'</ul>';
if(older) html+='<div class="warn">2주 넘게 밀린 항목 '+older+'건은 <a href="schedule/">일정 도식</a> 아래에 접어 두었습니다. 끝난 일이면 노션에서 완료로 바꾸면 다음 갱신 때 빠집니다.</div>';
if(!html) html='<div class="empty">오늘 잡힌 기한이 없습니다. 이번 주 최우선 5개 중 위에서부터.</div>';
html += '<div class="note">추천 순서: 현금에 가까운 P0 → 기한 지난 것 → 오늘 기한 → 3일 내. 데이터는 노션 액션보드·플라우드 녹음·클로드 대화에서 정리(갱신일 기준).</div>';
document.getElementById('todayBox').innerHTML = html;
const rhythm=['주간 정리','파이프라인 점검','물류 피크 대응','대본 검토','배치 촬영','발주·공지','컨설팅 자료'];
document.getElementById('week').innerHTML = days.map((d,i)=>'<div class="'+(i===now.getDay()?'on':'')+'"><b>'+d+'</b>'+rhythm[i]+'</div>').join('');
</script>
""".replace("__EVENTS__", json.dumps(EVENTS, ensure_ascii=False))

# ---------------------------------------------------------------- 로드맵
ROADMAP = """
<h1>돈 버는 로드맵</h1>
<p class="note">강의·컨설팅은 이미 뽑을 만큼 뽑았다고 보고 독립 유지, 그와 무관한 신규 파이프라인으로 2~3개월 내 월 순수익 3,000~4,000만을 만드는 것이 9월 중순의 결정입니다. 여기에 9/29 메이브님과 논의한 '신규 강의 플랫폼'이 더해졌습니다.</p>

<h2>4분기 내부 방향 <small>10/8 업무지시</small></h2>
<div class="card accent">
  <p style="margin:0 0 10px">10~12월을 팀에 공유한 네 줄입니다. <b>위 두 줄은 지금 있는 것을 키우는 일이고, 아래 두 줄은 새로 여는 일</b>입니다.</p>
  <ul class="list">
    <li><div class="t">물류 시스템 보완</div><div class="m">아래 세 줄의 선행 조건입니다. 리나님 시간 기록 시트가 여기에 붙어 있습니다</div></li>
    <li><div class="t">유통 채널 판매량 키우기</div><div class="m">메이븐 스토어 4분기 목표(월 순수익 1,000만·일 200건)와 같은 줄입니다</div></li>
    <li><div class="t">신규채널 수익화 — <b>거인의 도구공방 사이트 판매 시작</b></div><div class="m">자체 사이트에서 직접 파는 첫 채널. 플랫폼 수수료와 노출 규칙 밖에 있습니다</div></li>
    <li class="big"><div class="t">오프라인 판매 시작</div><div class="m">'물류가 좀 정리되면' 조건이 붙어 있습니다. <b>1번이 늦으면 이 줄이 같이 밀립니다</b></div></li>
  </ul>
  <div class="note">네 줄 모두 <b>강의·컨설팅이 아닌 쪽</b>입니다. 9월 중순에 정한 '강의와 무관한 신규 파이프라인' 방향과 같은 방향이고, 같은 분기에 초월스토리 강의 건이 따로 돌아갑니다 — 12월에 두 축이 겹칩니다.</div>
</div>

<h2>돈이 나오는 줄 <small>지금 → 3개월</small></h2>
<div class="card wrapx">
<table>
<tr><th>줄</th><th>내용</th><th style="text-align:right">월 기대</th></tr>
<tr><td>원크루</td><td>평생 컨설팅 · 정가 3,900만 / 수강생 출신 3,300만 · 추석 특강 100명 → 1~2명 전환</td><td class="num">3,300만+/건</td></tr>
<tr><td>신규 강의 플랫폼</td><td>메이브님과 3인 구도(강사 / 기획·커뮤니티 / 모객). 250만×20명 = 5,000만, 광고 1,000만 제외 4,000만. 25명이면 각 1,300만</td><td class="num">1,300만+</td></tr>
<tr><td>특강 + 컨설팅</td><td>진단 20만 / 4주 60~90만, 메이브님 수강생 포함, 슬롯 주5·동시5 (배분 사전 합의)</td><td class="num">500만+</td></tr>
<tr><td>300만 툴킷 프로그램</td><td>자동등록+소명서+연출컷 1년 + 8주 코칭 + 파일 구독 = 300만 · 1기 8명 목표</td><td class="num">2,400만/기</td></tr>
<tr><td>구독 창립멤버</td><td>연 10만, 100명 한정, 스마트스토어 연간권 선판매</td><td class="num">1,000만</td></tr>
<tr><td>루크 툴박스</td><td>월 19,900 / 연 199,000 · 12월 500명 → 3월 1,000명 → 6월 월 3,000만</td><td class="num">12월 1,000만</td></tr>
<tr><td>AI 스튜디오 맞춤</td><td>지인 10명 영업 → 첫 3건 반값(75~100만) · 2주 안에 생존 판단</td><td class="num">225~300만</td></tr>
<tr><td>3PL 재고 외부 판매</td><td>수강생 재고를 회사가 당근·번개장터·네이버에서 판매, 수수료 15~20%</td><td class="num">재고 회전×수수료</td></tr>
<tr><td>키티티 컨설팅</td><td>월 고정 자문 + 매출 연동 (자문 계약서로 유료 전환)</td><td class="num">50~100만</td></tr>
<tr><td>유튜브 멤버십</td><td>4,900원, 특강 풀버전·월 상품 브리핑 (파일 X)</td><td class="num">35~100만</td></tr>
<tr><td>메이크업헬퍼 위탁</td><td>원크루 최은봉 대표 건 · 12주 테스트, 광고 상한 약 189만, 11월 말 판정</td><td class="num">판정 후</td></tr>
</table>
<div class="note">숫자는 모두 루크 본인 기록(9/14~9/29 노션·녹음) 기준의 계획값이며 실적이 아닙니다.</div>
</div>

<h2>3단계</h2>
<div class="card">
  <div class="steps">
    <div><b>1단계</b>지금~10월<br>현금 회수</div>
    <div><b>2단계</b>11~12월<br>구독·플랫폼 세우기</div>
    <div><b>3단계</b>2027 1분기<br>확장·이전</div>
  </div>
  <ul class="list">
    <li><div class="t">1단계 · 지금~10월 — 현금 회수</div><div class="m">원크루 1~2명 · 3PL 재고 판매 첫 등록 · 디노 12주 시작 · 툴박스 결제 심사 통과 후 사전 신청 → 창립멤버 · 10월 말 무료 라이브로 신규 리스트 · 10/8 본부장 미팅으로 플랫폼 3자 구도 확정</div></li>
    <li><div class="t">2단계 · 11~12월 — 구독·플랫폼 세우기</div><div class="m">툴박스 500명 · 신규 강의 플랫폼 1기 모집 · 메이크업헬퍼 11월 말 판정 · 3PL 판매 실적 정리 · 300만 툴킷 1기</div></li>
    <li><div class="t">3단계 · 2027 1분기 — 확장·이전</div><div class="m">회사 자체 강의(3PL 재고 판매와 연계) · 툴박스 1,000명 · 서울 이전 검토(현 사무실은 창고·물류 거점) · 키티티 샵 2월 오픈 · 지영 정부지원사업 3월 집중</div></li>
  </ul>
</div>

<h2>신규 강의 플랫폼 <small>9/29 메이브님 회의</small></h2>
<div class="card gold">
  <dl class="kv">
    <dt>구도</dt><dd>강사(플레이어) / 기획·커뮤니티 운영 / 모객 채널 — 3각. 커뮤니티 전담자 포함 1:1:1 배분</dd>
    <dt>수치</dt><dd>1인 250만 · 20명 = 5,000만 − 광고 약 1,000만 = 4,000만. 3인이면 25명 모집 시 각 1,300만</dd>
    <dt>후보</dt><dd>초이스토리 PD(인력 풀·채널 보유, 먼저 접촉) → 종혁 본부장(기획·판 키우기, 10/8 미팅)</dd>
    <dt>반면교사</dt><dd>인베이더 실패: 큰돈 위주 광고 집행, 폐쇄적 채널 확장, 상담 인력 부재, 관료적 강사 검증</dd>
    <dt>장기</dt><dd>내년 초 서울 이전(사무실·강의장), 현 사무실은 창고·물류 · 월 렌트 300~500만 넘으면 건물 매입 검토</dd>
  </dl>
</div>

<h2>원칙 · 하지 않기로 한 것</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">하지 않는다</div><div class="m">사입 확장(사무실 전체가 이미 사입 중) · 브랜드↔셀러망 공급 플랫폼 · B2B 운영 대행 · 고단가 강의 프로그램 신설</div></li>
    <li><div class="t">보류 (10월 정산 확인 전)</div><div class="m">새 사이트·앱 개발 · 새 강의 시리즈 기획 · 셀러 OS · 액션아이템 자동 수집 앱</div></li>
    <li><div class="t">돈 원칙</div><div class="m">재고·개발 0원, 보유 현금은 런칭 광고에만 · 선매입 금지 · 수강생에겐 도구 기본판 무료(강의 후킹), 외부·맞춤·구독은 유료</div></li>
    <li><div class="t">일 원칙</div><div class="m">루크는 녹화·협상·규칙 승인만, 운영은 사람과 자동화에 · 시스템 먼저, 사람 나중 · 정리해주는 선배 톤</div></li>
  </ul>
</div>
"""

# ---------------------------------------------------------------- 우선순위
PRIORITY = """
<h1>우선순위</h1>
<p class="note">기준: 현금에 가깝고 다른 일의 선행 조건일수록 위. 기한은 노션 액션보드 기준. [결정]은 완료로, [보류]는 P3로. <span class="tag">새 항목</span>은 최근 7일(10/3~) 안에 노션에 생긴 미완료 항목입니다.</p>

<h2>P0 · 이번 주 <small>~10/11</small></h2>
<div class="card red">
  <ul class="list tasks">
    <li data-g="developer-accounts"><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 — Apple Developer / Google Play / Microsoft Store</div><div class="m">기한 10/2 지남(노션 미완료) · 앱 배포(툴박스 PWA→앱, 영상공장, 블로그타이퍼) 전부의 앞단. 루크가 "제일 높은 등급"으로 지정(9/30)</div></li>
    <li data-g="platform-director-meeting"><span class="tag cash">현금</span><div class="t">박종혁 본부장 협업 — 10/9 회의 진행(녹음) → 계약 전 닫을 다섯 칸(10/16)</div><div class="m">월 300만 고정 3개월·수익 6:4·카페 3,000명 목표(녹음 요약, 계약 미확정 · 총액 확인 필요) · 노션 '10/8 종혁 본부장 미팅'은 미완료 — 완료 처리 확인 필요 · <a href="../park/">협업 평가</a> · <a href="../platform/">전략 페이지</a></div></li>
    <li><span class="tag cash">현금</span><div class="t">3PL 수강생 재고 당근·외부 판매 — 2주 내 첫 등록</div><div class="m">기한 10/1 지남(노션 미완료) · 동의서 → 시트·사진 → 당근 비즈프로필 → 30개 등록 → 광고 10만 테스트</div></li>
    <li><span class="tag cash">현금</span><div class="t">디노 12주 빌드업안 전달·합의 (10/4) → 10/5 1주차</div><div class="m">상품별 배분 비율 확정 · 1주차 콘셉트 3안 중 선택</div></li>
    <li><span class="tag cash">현금</span><div class="t">원크루 문의(오픈채팅) 가격 안내 + 상담 통화</div><div class="m">3,900만 / 3,300만 · 신한카드 네이버페이 60개월 '세팅 가능'으로 표현</div></li>
    <li><span class="tag cash">현금</span><div class="t">툴박스 구독권 오픈일·가격·사전 신청 안내 문구</div><div class="m">토스페이먼츠 심사 전이라 사전 신청 형태</div></li>
    <li><div class="t">10/25(일) 6기 무료 라이브 — 시간·신청 링크</div><div class="m">날짜는 10/4 노션 [결정]으로 확정 · 시간 19:00는 10/2 녹음 언급값, 신청 링크 확인 필요 · 록터뷰 2회차 영상에 링크</div></li>
    <li><div class="t">뷰셀 유튜브 2화 — 대본 9/30 · 촬영 10/2 · 공개 10/7</div><div class="m">담당 메이브님 · 3화는 실제 상품 마진 계산</div></li>
    <li><div class="t">물류 안정화 — 책임자 단일화(9/30), 삭제/무효화 임시 규칙(10/1), 프로세스 맵(10/2), 운영 가이드(10/4)</div><div class="m">입고 미처리 상태에서 운송장 출력되는 오류 긴급 대응</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea0481919532d4927c656358"><span class="tag cash">현금</span><div class="t">키티티바이지영 상표권 출원 — 지영 명의, 특허로 전자출원 (진행 중)</div><div class="m">원래 기한 10/1 지남 → 10/1 노션에 새 항목(기한 10/4) · 등록 1년 이상 소요 → 2월 오픈 역산 마지노선</div></li>
    <li><div class="t">수강생 화장품법 소송 초동 대응 지원 (10/6)</div><div class="m">답변서 기한·변호사 연결 · 대응 전자책 20쪽 완성됨 · 9/30 컨설팅에서 대응 선택지 논의(결정은 수강생 몫)</div></li>
    <li data-n="https://app.notion.com/p/3df0cf8fea0481d1ae56f9c71eb42aac"><div class="t">유형 검사(사업적성) 오픈 — 카카오 키 연결하고 단톡방 공유 시작</div><div class="m">진행 중 · 기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3e60cf8fea0481cca61cf923c28b9e54"><div class="t">블로그타이퍼 윈도우 클로드 코드로 이사</div><div class="m">기한 9/27 지남 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3e70cf8fea048151a2b9cb0abd28ebc4"><div class="t">셀수다 v2026.9.26 설치 + '카탈로그 수집기' 확장 설치</div><div class="m">기한 9/27 지남 · 노션 '시작 전'</div></li>
    <li data-n="https://app.notion.com/p/3e90cf8fea04815da58cc6d8030ca735"><div class="t">영상공장 윈도우 PC 설치·첫 영상 테스트</div><div class="m">기한 9/30 · 진행 중 · API 키 5개·목소리 녹음은 10/5</div></li>
    <li data-n="https://app.notion.com/p/3e90cf8fea048107ba1dff3afb73cedd"><div class="t">록터뷰 2회차 인터뷰 촬영</div><div class="m">기한 9/28 · 노션 '진행 중' — 촬영이 끝났으면 완료 처리 필요</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04812b8f86e2d58503588d"><span class="tag cash">현금</span><div class="t">키티티 AI 스타일 미리보기(/try) 구축</div><div class="m">기한 10/4 · 진행 중 · 무료 1회·워터마크·유료 원본 다운로드</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481b8be99d8ebff105a1b"><span class="tag cash">현금</span><div class="t">최은봉 대표님(메이크업헬퍼) — PDF 재전송·9/30 리포트(10/1) → 1주 팔로업(10/7) → 당근 중간 결과 리뷰 미팅(14:00)</div><div class="m">10/7 낮 원크루 세션 녹음이 있음 — 리뷰 미팅이 끝났으면 노션 완료 처리 필요</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481029429c45d9b6bfe47"><span class="tag cash">현금</span><div class="t">박태경 대표님 — 사입 재고 스프레드시트(10/2) · 상품·가격 체크리스트(10/4) · 5회차 준비(10/7)</div><div class="m">9/30 원크루 세션 Action Item</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481ea947cc6042c5ad37e"><span class="tag cash">현금</span><div class="t">정○○ 대표님(원크루) 다음 컨설팅 — 매일 결산·금요일 상품 정리 점검</div><div class="m">기한 10/7</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481b1af7ac611bcbe1835"><span class="tag cash">현금</span><div class="t">수강생 컨설팅 후속 — 소장 대응 결정·리셀 정리·브랜드 재점검 (익명)</div><div class="m">기한 9/30 · 노션 '진행 중'</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04814187b8c258b3a2d38e"><span class="tag cash">현금</span><div class="t">키티티 '연봉 10억 만들기' 페이지 배포 (저장소 kititi-1b)</div><div class="m">기한 10/4 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04817fa0caf144b0c513ee"><div class="t">최저가 찾기 소싱 프로그램 새 버전 공개</div><div class="m">기한 10/4 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea0481698468f35e62d2e19b"><div class="t">키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체</div><div class="m">기한 10/8 · 진행 중 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481839c31e0155118809c"><span class="tag cash">현금</span><div class="t">평생컨설팅 문의(뷰셀 수강생·쿠팡 영구정지) 답변 + 진단 상담 잡기</div><div class="m">기한 10/3 · 진행 중 · 10/2 답장 발송, 회신 오면 일정 확정 · 메이브님 수강생이라 배분 사전 합의 필요</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea048154a15bddc7596e1165"><span class="tag cash">현금</span><div class="t">10/6 12:00 소싱 멘토링 실습 진행 — 수강생 소싱 10개 점검</div><div class="m">플라우드 10/2 멘토링 Action Item · 일시는 노트 기재값 — 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea04813d9f8aedfc7e183098"><span class="tag cash">현금</span><div class="t">상품소싱 시트 마진 공식에 매입 배송비 반영 + 백설 와플믹스 10kg 역마진 재확인</div><div class="m">기한 10/4</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481b18770d4c9279c70a1"><div class="t">마진메이커 크롬 확장 프로그램 설치·서버 배포</div><div class="m">기한 10/4 · 진행 중 · v1 완성, 설치가이드 1~4단계 남음</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481a7b0c0cfc85f4b3475"><div class="t">힐링디어스(주) 본점 주소 확보 + 본점이전 등기·사업자등록 정정</div><div class="m">기한 10/15 · 진행 중 · 새 본점 주소 확보 완료(10/9) → 10/12 법무사 위임 → 등기 후 사업자등록 정정</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481bc8287dc9e35045f45"><div class="t">멘토루크 블로그 — 블로그 프로그램을 개인 브랜딩(케어 이야기 중심)으로 독립 분기 1차 전환</div><div class="m">기한 10/10(오늘) · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481a08c7ac705e54340e1"><div class="t">다음 주 평일 저녁 팀 회식 장소 확정·예약</div><div class="m">기한 10/5</div></li>
__NEW_P0__
  </ul>
</div>

<h2>P1 · 이달 <small>~10/31</small></h2>
<div class="card gold">
  <ul class="list tasks">
    <li><div class="t">300만 툴킷 프로그램 구성안 확정 (툴킷 3개 + 8주 + 파일 구독)</div></li>
    <li><div class="t">AI 스튜디오 — 포트폴리오·가격표 랜딩 + 시연 쇼츠 3개 + 지인 10명 영업</div></li>
    <li><div class="t">툴박스 공개용 문구·주소 채우기 (루크가 줄 것 6가지: 채널 주소·문의 주소·컨설팅 설명·상세 검토·연간가·사진)</div></li>
    <li><div class="t">키티티 — 자문 계약서 · 교육상품 가격 확정 · 상담 사이트 원장님 확인 · 미용 단톡방 200명</div></li>
    <li><div class="t">지영 — 인스타 캘린더(10/1) · 대시보드(10/7) · 10/8 미팅 · 조달 마일스톤(10/15)</div></li>
    <li><div class="t">메이크업헬퍼 — 계약 원안대로 체결(9/30 녹음) → 당근 광고 테스트 3만~10만 → 부진하면 토스로 이동</div><div class="m">10/1 당근 등록·광고 시작 · 중간 결과 리뷰 미팅 · 10/20 2주 판정 · 기준: 광고비 대비 수익 본전 이상</div></li>
    <li><div class="t">리나님 시간 기록 시트 2주 시범 → 크롬 확장 설계</div></li>
    <li><div class="t">영상공장 API 키 5개 + 목소리 녹음 → 첫 실제 영상</div></li>
    <li><div class="t">인스타 크리에이터 계정 전환 + 마케팅 업체 채널 인계 (유튜브 편집자 권한·틱톡 신규 계정)</div></li>
    <li><div class="t">디노 AI 영상(힉스필드) 학습 기록 → 무료 전자책 → 유료 전자책 파이프라인</div></li>
    <li data-n="https://app.notion.com/p/3e60cf8fea0481cda4d6fe91c714f354"><div class="t">툴박스 — 수강생 명단 자동 인증 · 상품 판매 시작 전 확인</div><div class="m">진행 중 · 기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3e90cf8fea0481dc8e86ef413c4e23c8"><div class="t">미니쌤 채널 공지 3회 (10/12주 · 10/26주 · 11/23주)</div><div class="m">기한 10/16</div></li>
    <li data-n="https://app.notion.com/p/3e90cf8fea0481faadcdf4ad3356a80b"><div class="t">미용인 라운지 사이트 v1 · 하루블록 v1.0 무료 배포 준비</div><div class="m">둘 다 기한 9/30 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3e90cf8fea0481468c69f67787077a44"><div class="t">앱 배포 계정·인증서 준비 (윈도우·맥·아이폰·갤럭시)</div><div class="m">기한 9/30 · 진행 중 · P0 '개발자 계정 3종'과 같이</div></li>
    <li data-n="https://app.notion.com/p/3ea0cf8fea0481969503d67f972a91e1"><span class="tag cash">현금</span><div class="t">수강생 전체 공지·교육자료 — 화장품 2차 포장(단상자)·표시사항 유지, 도매처 검증 체크리스트</div><div class="m">기한 9/30 지남</div></li>
    <li data-n="https://app.notion.com/p/3ea0cf8fea0481af8112d35bc3c0e23b"><span class="tag cash">현금</span><div class="t">배수진(돈 걸고 목표달성 앱) 프로토타입 검토</div><div class="m">기한 10/6 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3ea0cf8fea04818f9d6fdd1b114a853e"><div class="t">뿌요 짠테크 유튜브 — 3화 대본(10/7) · 2화 촬영·편집(10/10)</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04812c84d8d9344b5cfec6"><span class="tag cash">현금</span><div class="t">박태경 대표님 — 안내 템플릿 3종(10/5) · 빠른 거절·통보 기준(10/6) · 4회차 자료 재공유(10/7) · 자동 알림 조사(10/7) · 겨울 시즌 리스트·광고 가이드(10/10)</div><div class="m">플라우드 9/30 세션 할 일 목록에서 새로 등록</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481eabc25d08c7f5019f3"><span class="tag cash">현금</span><div class="t">최은봉 대표님 — 10/20 당근 2주 결과 판정 · 성과 기반 파일럿 제안서·착수금 템플릿(10/31)</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea048138a1e5d67100f3785c"><span class="tag cash">현금</span><div class="t">일십백천 수강생 수경 브랜드 10월 재시동 지원</div><div class="m">기한 10/31 · 보조 품목 규칙 사전조사, 다음 컨설팅 일정 확정</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481e084eac0131859e2ca"><div class="t">뷰셀 회차 주제 후보 22개 — 순서 확정과 수치 검증</div><div class="m">기한 10/31 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481c2a29df44aa8ee126e"><div class="t">현재 사무실 임대료·관리비 정산</div><div class="m">플라우드 9/29 회의 · 기한 10/5는 추정 — 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea048151a8acff9e6bbd0442"><div class="t">정부지원사업 맞춰 보기 사이트 「되는 지원사업 찾기」 구축 (클로드 코드)</div><div class="m">기한 10/8 · 진행 중 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481a4837dc07d4eeaa7a7"><span class="tag cash">현금</span><div class="t">10/2 소싱 멘토링 후속 문서 — 총액 계산 시트 템플릿(10/8) · 선별 기준표(10/9) · 미스매치 재검증 체크리스트·실질 단가 환산 규칙(10/10~11) · 소액 테스트 프로토콜(10/12)</div><div class="m">플라우드 10/2 멘토링 Action Item 중 루크 담당 · 기한은 노트 기재값</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea048121be35ee82635e54a4"><span class="tag cash">현금</span><div class="t">교육회사(셀러들의 수다)+3PL 법인 — 신규 설립 vs 힐링디어스 변경 결정</div><div class="m">기한 10/31</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea04810b808df66fdd4ed562"><div class="t">키티티 원장님 — /admin 노트 사용법 전달·시술 방향 피드백 + /guide 내용 피드백 받기</div><div class="m">둘 다 기한 10/9</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481ab9090e503641c10b6"><div class="t">무료 라이브 특강 참석자 선물 준비 — 소싱처 전자책 + 자동 등록 프로그램 7일 이용권</div><div class="m">10/2 인터뷰 녹음에서 약속 · 기한 10/24는 추정 — 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481b19467f1586979d14c"><div class="t">API 캐시 자동 충전 설정 — 잔액 8,000원 미만이면 8,000원 충전</div><div class="m">플라우드 10/2 멘토링 Action Item · 기한 없음</div></li>
__NEW_P1__
  </ul>
</div>

<h2>P2 · 다음 달 말</h2>
<div class="card">
  <ul class="list tasks">
    <li><div class="t">사진 기반 입고/검수 자동화 (설계 10/8 → 프로토타입 10/15)</div></li>
    <li><div class="t">물류 권한 재설계·감사 로그 · 선반·라벨링 · CS 스크립트</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481c99703fd2ab39116e4"><div class="t">개인 트레이드 채널 개설·운영 (9/29 액션)</div><div class="m">기한 10/31은 추정 · 채널 성격·기한 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481179e23f70b21ce0c10"><div class="t">'하루를 4번 쓰는 법' 영상 — 6h×4 슬롯 7일 파일럿 후 대본·촬영</div><div class="m">기한 10/31은 추정 · 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea048126844ad335f1aefd2e"><div class="t">서울 이전·건물 매입 대비 로드맵 (내년 초)</div><div class="m">기한 11/30은 추정 · 확인 필요</div></li>
    <li><div class="t">전화 상담 AI — 100건 통화 녹음 분석 (내 목소리 엔진 연계)</div></li>
    <li data-n="https://app.notion.com/p/3ea0cf8fea0481e8bccdcb6db430eeb4"><div class="t">영상 자동화 프로그램 만들기 (지영 요청 개발건)</div><div class="m">기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481069327e3ef0da7a08d"><span class="tag cash">현금</span><div class="t">배민(B마트·배민스토어) 화장품 판매 채널 입점 가능성 확인</div><div class="m">기한 10/31</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481299b1aeaf71e8c9536"><div class="t">전자책 3종 — 「불평만 하고 도전은 안 하는 비겁한 사람들」 · 「끼리끼리 모이면 실패하는 이유」 · 「부자들은 하고 가난한 사람들은 하지 않는 말」</div><div class="m">기한 10/31 · 세 번째는 10/1 등록</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481dd8721d7c5260db6d1"><span class="tag cash">현금</span><div class="t">트리플 루프 빈 칸 설계 — 지영 채널 자체 수익 + 실물 제품 유통 아이템</div><div class="m">기한 11/30</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04817e87d2c4ec5d319b6b"><div class="t">영상공장 AI 라벨 자동 켜기 확인 (유튜브 합성 콘텐츠·인스타 AI 정보)</div><div class="m">기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea04810e84d3e7ceb43c766d"><span class="tag cash">현금</span><div class="t">힐링디어스(주) 업력·매출 기준 2027 정부지원사업(초창패·디딤돌·도약패키지) 지원 가능 여부 확인</div><div class="m">기한 11/30 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea04816eae8bcd7b7a2a9f54"><span class="tag cash">현금</span><div class="t">디노 — 1년 사업자 업종코드가 9년 사업자와 다른지 확인 + 9년 사업자 폐업 시점 검토</div><div class="m">담당 수민님 · 기한 없음 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea048134aac2dbc802115811"><div class="t">수파베이스 전용 프로젝트 분리 여부 결정 (Pro 업그레이드 또는 기존 프로젝트 정리)</div><div class="m">기한 10/31 · 헤메네일 시세판 (10/1 등록)</div></li>
__NEW_P2__
  </ul>
</div>

<h2>P3 · 보류</h2>
<div class="card">
  <ul class="list">
    <li><span class="tag p3">보류</span><div class="t">새 사이트·앱 개발, 새 강의 시리즈, 셀러 OS — 10월 정산 확인 전까지</div></li>
    <li><span class="tag p3">보류</span><div class="t">개발자 채용 — 구독자 수 기준으로 판단, 우선 PWA</div></li>
    <li><span class="tag p3">보류</span><div class="t">사업가·자기계발용 핸드폰 앱(동기부여) — 6개월 후 단독 구독 검토</div></li>
    <li><span class="tag p3">보류</span><div class="t">깃허브 저장소 전부 Private 전환 (Pages 유지하려면 Pro 필요)</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea048104bdd0da8356e9bc11"><div class="t">[공개 직전] 헤메네일 — 도메인 hemenail.kr 선점 · 상표 35류 출원 · 기술 작업 7가지(가격제보·리뷰 이식, 검색노출, 약관 등)</div><div class="m">공개 직전에 할 일 · 기한 없음 (10/1 등록 3건)</div></li>
__NEW_P3__
  </ul>
</div>

<h2>최근 [결정] <small>노션 완료 항목 중 최신 6개</small></h2>
<div class="card accent">
  <ul class="list">
    <li><span class="tag done">결정</span><div class="t">대표이사를 넣는다 — 유믿음 대표이사 선임, 신정현 대표님은 대표권 없는 사내이사 (10/9)</div></li>
    <li><span class="tag done">결정</span><div class="t">정관은 전부개정으로 간다 — 2022년 설립 정관 분실 전제 (10/9)</div></li>
    <li><span class="tag done">결정</span><div class="t">본점 이전일 2026-10-02 — 사무실 계약서 기준, 등기 기한 10/16(금) (10/9)</div></li>
    <li><span class="tag done">결정</span><div class="t">4분기 내부 방향 4줄 — 물류 보완 / 유통 판매량 / 거인의 도구공방 사이트 판매 / 오프라인 판매 (10/8)</div></li>
    <li><span class="tag done">결정</span><div class="t">본점이전 등 변경등기는 법무사에게 10/12(월)에 맡긴다 — 셀프 전자신청 대신 위임 (10/8)</div></li>
    <li><span class="tag done">결정</span><div class="t">초월스토리 파일럿 강사는 가을(정복녀) 대표님 — 강의 기획 착수, 목표 40명 (10/7)</div></li>
  </ul>
</div>
"""

# 최근 7일(10/3~) 안에 노션 액션보드에 새로 생긴 미완료 항목 — 우선순위 페이지 각 P 구간 끝에 붙는다.
# (할 일, 메모, 노션 url 또는 "", 현금 여부). 기존 줄에 이미 있는 항목은 넣지 않음.
_N = "https://app.notion.com/p/"
NEW_ITEMS = {
 "P0": [
  ("홍○○ 대표님(원크루 상담 10/3)께 상담 리포트 링크 발송", "기한 10/4 · 진행 중 (10/3 등록)", _N+"3ee0cf8fea04812e8d21df33ab1687df", True),
  ("매장 대청소 — 업체 선정(비포에프터클린) → 10/5 14:00 작업 입회·검수", "입회·검수 항목은 기한 10/5 · 노션 '진행 중', 업체 선정 항목은 '시작 전' — 끝났으면 둘 다 완료 처리 필요 (10/4·10/5 등록)", _N+"3ee0cf8fea0481fa9237cd0b76f22b45", False),
  ("6기 무료 라이브(10/25) 준비 — PPT 제작(B스타일 네이비&크림으로 새로) · 남은 미결정 사항 확정 · 수강생 인터뷰 5명 섭외·자료", "모두 기한 10/11 · PPT·미결정 사항은 진행 중 (10/4 등록 4건)", _N+"3ee0cf8fea04815d91cdf96ae0a85075", True),
  ("키티티 AI 뷰티 플랫폼 — 전환 검증 실험(랜딩+사전예약) · 진단 링크 홍보·파트너샵 마케팅 키트 1판 · 홈페이지 클릭 수 기록 시작 · K-뷰티 크리에이터 챌린지 공고 확인", "모두 기한 10/11 · 검증 통과 기준: 랜딩 방문 300명 중 예약금 결제 10명 (10/4 등록 4건)", _N+"3ef0cf8fea04812c9dbfcf46c011ba42", True),
  ("키티티 계약 — 10/8(목)", "플라우드 10/8 녹음: 토탈샵 임대차·권리양수도 계약 체결 — 노션은 '시작 전', 완료 처리 확인 필요 (10/5 등록)", _N+"3f00cf8fea0481a89260d919b12e75c3", True),
  ("변경등기(본점이전·상호·목적·이사선임) — 한 신청서로 묶기·법무사 선정·위임(10/12) · [결정 필요] 셀러들의 수다 = 힐링디어스 상호변경 확정(10/11) · 4대보험 소재지 변경(10/15) · 등기 제출·사업자등록 정정(10/16) · 세무사 수입금액 조회(10/8)·세무사 통화(10/9)는 기한 지남 · 정관 찾기(10/10)", "법인 정리·사업장 이전 · 등기 기한은 10/16(금)으로 하루 늦춰짐 · 사업목적 41개·수권주식 100,000주는 [결정] 완료 · 정관은 10/9 [결정]으로 전부개정 — '정관 찾기' 항목은 완료 처리 확인 필요 · <a href=\"../relocation/\">등기 페이지</a> (10/7 등록)", _N+"3f10cf8fea0481e8b9e1cc147d2b6a9c", False),
  ("힐링디어스 법인 등기 — 정관 원본 찾아 본점 조항 확인('구리시'까지인지 번지까지인지) · '셀러들의 수다' 상호 중복 확인(인터넷등기소) · 신정현 대표님께 등기 제출용 준비물 전달 + 인감 신고 여부 확인", "모두 기한 10/9 · <a href=\"../registry-prep/\">준비물 체크리스트</a> (10/8 등록 3건)", _N+"3f30cf8fea0481cc8bc6f8687a37a03a", False),
  ("창고형 매장 1단계 범위 정하기 — 진열 공간, 첫 진열 재고 목록, 매장 가격 원칙", "기한 10/12 · 10/7 노션 [결정]: 사입 비율을 올리려면 창고형 매장을 먼저 돌려 판매를 보여 준다 (10/7 등록)", _N+"3f10cf8fea0481658a61d68b0e18c84c", True),
  ("초월스토리 강사 협업 — 계약서 정산 기준 정리·가을 대표님 의향·일정 확인·성과 숫자 확보(10/11) · [결정 필요] 루크 참여 범위·정산 기준 문서화·원크루 관계 유지(10/22) · 고연령 성과자 섭외(10/25)", "<a href=\"../chowol/\">초월스토리 페이지</a> · <a href=\"../pilot/\">파일럿 강사 결정</a> · '파일럿 강사 선정'은 노션 완료 (10/6·10/7 등록 7건)", _N+"3f10cf8fea048126a2fec9d1efd1c0eb", True),
  ("초월스토리 강사 협업(10/8 추가) — 가을 대표님 몫 2,200만 산출 근거 확인 · 광고 예산 약 4,500만 확인 + 상한·중단 기준 · 가을 대표님께 손익분기 인원·광고비 리스크 사전 설명 · 6:4 합의 서면화 · [결정 필요] 6:4를 숨길지 공동 기획으로 공개할지", "모두 기한 10/22 · 4,500만은 2,200만에서 역산한 값이라 초월스토리 확인 전 · <a href=\"../chowol/\">초월스토리 페이지</a> (10/8 등록 5건)", _N+"3f30cf8fea04813fab69eb44001ba56d", True),
  ("키티티 토탈샵 — 인테리어(급배수·전기 증설·칸막이·냉난방기) 승인 별첨 문서 준비 · 임대차 특약 수정안 협상(제소전화해·원상복구·갱신)", "둘 다 기한 10/11 · 특약 협상은 진행 중 — 10/8 계약 체결 녹음이 있어 완료 여부 확인 필요 (10/8 등록 2건)", _N+"3f30cf8fea048125b5f0cb4b24793347", True),
  ("10/25 무료 라이브 — 특강 진행(4종 자판기 전체 사용법 + 저가 소싱 노하우) · 단톡방 입장자 전원 자동 등록 자판기 7일 무료 이용권 지급 세팅 · 가을 대표님 게스트 10분", "모두 기한 10/25 (10/6·10/7 등록 3건)", _N+"3f10cf8fea0481969cd8e18631295ba8", False),
  ("신규 강의 플랫폼 — 3자 미팅 제안서 1차본 검토(10/6) · 3자 1:1:1 안과 초월스토리 8% 모델 관계 정리(10/8) · 시행 전 선행 조건 4가지·계약서에 '수강생 명단·결제 창구·강의 콘텐츠 = 셀수다 소유' 조항(10/13)", "<a href=\"../platform/\">전략 페이지</a> (10/6 등록 4건)", _N+"3f10cf8fea0481e4a78edf0ea6527d5c", True),
  ("인베이더 종료 대비 — 종료 사실 확인·메이브님과 마지막 기수 공동 대응 합의(10/8) · 계약서 소유 조항 확인(10/11) · 수강생 명단을 자체 채널로 옮기는 동선(10/12) · 사입 재고 처리 가이드라인(10/13)", "<a href=\"../invader/\">인베이더 종료 대비</a> (10/6 등록 5건)", _N+"3f10cf8fea0481b2b5f9c0ab5aa17594", True),
  ("메이브님 공동 액션(10/6 회의) — 메이븐 스토어 재정비·집중 품목 선정(메이브님) · 사입 재고 처리 가이드라인 · 루크 툴박스 토스 연동+깃허브 자동 업데이트 · [결정 필요] 2,000만 지출 세무 처리 · [결정 필요] 뿌요 역할·수익 구조", "기한 10/11~10/13 · 같은 회의가 노션에 두 번 등록돼 겹치는 항목이 있음(스토어 재정비·가이드라인·세무 처리) — 한쪽 정리 필요 · <a href=\"../maven/\">메이브님 공동 액션 플랜</a> (10/6 등록 7건)", _N+"3f10cf8fea048159873bcb81c41d12e9", True),
  ("디노 리부트 — 힙스필드 4수익축 구조도 전달·가격표·카테고리 3개 확정(루크) · 레퍼런스 30세트·첫 달 크레딧 소진량 기록(수민님) · 토요일 잠정 평가 미팅(10/10)", "기한 10/10~10/11 · 평가 미팅은 플라우드 10/6 디노 미팅 Action Item으로 새로 등록 (10/6·10/7 등록 4건)", _N+"3f10cf8fea04815393b4c9b512262ba3", True),
  ("원크루 크루 자료실 — 박태경 대표님 5회차 교육자료 발행 → 10/13 6회차 준비 · 최은봉 대표 1~5회차 게시(10/7) · 정복녀 대표님 회차 자료 배포(10/7) · 신정현 대표 10월 1·2주차 배포(10/11)", "10/7 상황판에 크루 자료실 배포 완료 보고가 있음 — 끝났으면 노션 완료 처리 필요 (10/6·10/7 등록 4건)", _N+"3f10cf8fea0481649ba4d4714240eaa7", True),
  ("백○○ 대표님께 전자책 전달 + 가격관리 프로그램 상시 실행 확인", "기한 10/11 · 코칭 교재 전자책 제작은 10/6 완료 (10/6 등록)", _N+"3f10cf8fea0481e3b5eff0f52d73ee47", True),
  ("뷰셀 3화 대본 — 10년 안에 매출 열 배 뛴 브랜드 (촬영 10/9)", "담당 메이브님 · 기한 10/9 · 진행 중 (10/6 등록)", _N+"3f10cf8fea048164a5c6f5877ec73e25", False),
  ("구글 계정 — 현재 노트북 외 다른 기기 전부 로그아웃", "기한 10/13 · 이전 컴퓨터 클로드 코드 로그인 해제는 완료 (10/6 등록)", _N+"3f10cf8fea048146a7a0c4bc30ac8402", False),
  ("루크 툴박스 결제·법적 필수 — 포트원 결제사 선택(KG이니시스, 루크 확인 후 제출) · 공방 사이트 유선번호 1개 · 실결제 전까지 프로그램 구매 길 막을지 결정 + 9월 테스트 구독·주문 자국 정리 · 토스 신청 멈춤 확인", "기한 없음 · 3개 문서·푸터는 완료 (10/7 등록 4건)", _N+"3f10cf8fea0481b3bd6dc3d1bfd8fa95", False),
  ("원크루 사이트 — '푸시하면 자동 배포' 연결(루크 클릭 대기) · 박태경 대표께 새 자료실 주소 전달 → 깃허브 원본 저장소 정리 · 관리자 비밀번호 정하기 · 뿌요님을 원크루 명단에 올리고 '목표 수익 관리' 열어 주기", "기한 없음 (10/6 등록 4건)", _N+"3f10cf8fea0481a89c87d347be379b54", False),
  ("가을(정복녀) 대표님 — 원크루 강사 파트너 제안서 전달·의사 확인 · 5회차(10월 1주차) 교육자료 발행 · 사업 구조화 페이지 배포", "모두 기한 10/12 · 진행 중 · 10/7 세션 녹음 요약에 긍정 수락이 있음 — 제안 항목 완료 처리 확인 필요 (10/7 등록 3건)", _N+"3f20cf8fea048167b893e89fdf2d8679", True),
  ("최은봉 대표님 — 6회차 자료 '배포해 줘'(10/7) · 이번 주 일정 체크(10/8 면접·10/12 신청) · 7회차 컨설팅(10/14) · 사업 구조화 페이지 저장소 생성·배포(10/7)", "6회차 자료실 배포는 상황판·노션에 완료 기록이 있음 — '배포해 줘' 항목 완료 처리 확인 필요 (10/7 등록 4건)", _N+"3f20cf8fea0481cfb10dff9aeed7df2d", False),
  ("김종진 대표님(일십백천) — 10/7 코칭(후보 목록·과제 확정) · 9/30 녹음 반영 전자책", "기한 10/7 · 노션 '진행 중' 3건 — 전자책 v2·통합본 전달과 10/7 통화는 완료 기록이 있어 완료 처리 확인 필요 (10/7 등록)", _N+"3f20cf8fea0481b38ce4d66a8cb866d9", True),
  ("[막힘] 사업 구조화 페이지 저장소 만들기 — 지영 원장(kittiti-jiyoung) · 신정현 대표(onecrew-shin-jeonghyeon)", "기한 10/11 · 루크가 깃허브에서 공개 저장소 생성 + Pages 켜기 + Claude 권한 추가 → 각 채팅이 push (10/7 등록 2건)", _N+"3f20cf8fea048152b55cec152c0f6fc9", True),
  ("초월스토리 — 루크 참여 범위를 공동 기획으로 올릴지 (5:5 분모에 들어가는지)", "기한 10/22 · 배분 초안 전에 제기 · <a href=\"../chowol/\">초월스토리 페이지</a> (10/7 등록)", _N+"3f20cf8fea0481faa420daf4c6647ca1", True),
  ("구리세무서 재산법인세과 전화 — 법인등기 진행 중, 완료 후 재신청 예정 알리기", "기한 10/8 · 10/7 사업장 이전 신고 취하 통지 — 거부가 아니라 순서 문제 · <a href=\"../relocation/\">10/15 등기 페이지</a> (10/7 등록)", _N+"3f20cf8fea0481d396d6fb41d1c6ee6b", False),
  ("일십백천 새 사이트에 넣을 값 확정 — 기수·정원·마감일, 환불·할부 문구, 강사 소개 숫자, 강사 사진, 후기 공개 범위, 도메인", "기한 없음 · 1차 제작은 10/8 완료 — 이 값만 채우면 공개 가능 (10/8 등록)", _N+"3f20cf8fea048198a344fb2711f2b3f5", True),
  ("인스타 게시물 업로드 + '홍보하기' 일 5천원×7일 집행", "기한 10/7 · 마케팅 업체 SNS 운영 (10/7 등록)", _N+"3f20cf8fea0481299b44db868963f2be", False),
  ("변경등기(10/9 추가) — 기장 세무사무소에 사업연도 확인 · 신정현 대표님 인감 신고 여부 확인+서류 3종 수령 · 등록면허세 중과 여부·'그 밖의 등기' 건수 확인 · 법인인감카드 분실 사용정지+법인인감도장 확인 · 법무사 위임 시 서류 목록(위임장·법인인감증명서) · 전부개정 정관 마무리(이상 10/12) · 루크 확정 4가지 정하고 출력·날인 · 목적 추가 문구 확정(이상 10/9)", "법인 정리·사업장 이전 · 10/9 [결정] 3건: 이전일 10/2 · 정관 전부개정 · 대표이사 선임 · <a href=\"../registry-forms/\">등기 서류 페이지</a> (10/9 등록 8건)", _N+"3f40cf8fea0481a3a3c8f22c07545cd2", False),
  ("박종혁 본부장 협업 — 계약 전 닫을 다섯 칸: 6:4 분모 · 총액·PD 단가 · 3PL 귀속 · 중단선 · 고정급 성질(10/16) · 물어볼 한 가지: 카페 월 4,000명 만들 당시 광고비(10/14)", "10/9 회의 녹음 재독 결과(노션 메모) · 6:4의 분모에 따라 손익분기 21명 vs 33명 · <a href=\"../park/\">협업 평가</a> (10/9 등록 2건)", _N+"3f40cf8fea04811ca54cf38b0d15e46f", True),
 ],
 "P1": [
  ("홍○○ 대표님 원크루 재문의 여부 확인", "기한 10/17 · 10/3 상담 후속 (10/3 등록)", _N+"3ee0cf8fea0481b58bcec3ba614eec0f", True),
  ("키티티 AI 뷰티 플랫폼 — 협력 계약서 초안 · 홈페이지 파트너샵용 템플릿 · 파트너 의향서 양식(3곳)·의향 샵 10곳 모집 · 개발비·유지비 구조 재검토 · 업종 추가 세무사 확인 · 초창패 자부담 마련 계획 · 원장 자격·수상 목록 · 웨딩·이벤트 패키지 연결 · 헤메네일→진단 링크", "모두 기한 10/31 · <a href=\"../reports/kititi-win-plan/?v=1\">초창패 승부수 보고서</a> (10/4 등록 10건)", _N+"3ef0cf8fea0481388f9cc6a8fd0cd7db", True),
  ("원크루 사이트 4단계 — 로그인·가입 + 원크루 회원 표 + 관리자 화면", "기한 10/31 · 처음 넣을 회원 명단 루크 확인 필요 · 3단계(빈 입구 배포)는 10/5 완료 (10/5 등록)", _N+"3ef0cf8fea048181a121fa70732b2b17", False),
  ("Vercel 팀을 Pro($20/월)로 바꿀지 결정 — 무료(Hobby)는 비상업 전용인데 공방 유료 결제 운영 중", "기한 10/31 (10/5 등록)", _N+"3ef0cf8fea0481ab90bcfc0684789878", False),
  ("업무용 맥북 교체 — 중고 M4 맥북에어 16GB 검토, M1 에어는 중고 판매", "기한 10/31 · 진행 중 (10/4 등록)", _N+"3ef0cf8fea04817bba04cb14d260f50f", False),
  ("루크 툴박스 자동 메시지(알림톡·문자) 연동", "기한 없음 · 루크 할 일 3개: 카카오톡 채널+비즈니스 인증 · 솔라피 가입+발신번호 등록 · API 키 전달 (10/4 등록)", _N+"3ef0cf8fea0481dfa1b6d552232ecaa9", False),
  ("[결정 필요] 헤메네일 광고 금액 확정 — 프리미엄·플러스·루키", "기한 없음 · 10/5 방침: 광고비로 순위가 움직이는 구조, 1차 구현·배포 완료 · 제안 금액: 프리미엄 49,000원/주 · 플러스 19,000원/주 · 루키(개업 1년 이내) 9,000원/2주 (10/5 등록)", _N+"3f00cf8fea04811598d8f4ff3c654f8f", True),
  ("[결정 필요] 헤메네일 추가 공공데이터 — 인허가 일간 API로 폐업 자동 반영 + 사업자 상태조회로 사장님 확인", "기한 없음 · 둘 다 data.go.kr 활용신청 필요(루크 허락 시 클로드가 신청) (10/5 등록)", _N+"3f00cf8fea04818e91f2fb85f0445a89", False),
  ("키티티 헤메네일 업종 정정 요청(주력 메이크업) + 가격표·네이버 예약 주소 올리기", "기한 없음 · 상호에 '메이크업'이 없어 업종 '모름'으로 분류됨 → 매장 상세 맨 아래 '업종 정보 정정 요청' (10/5 등록)", _N+"3f00cf8fea04812f81c6f8f751221178", False),
  ("키티티 AI 상담 — GPT 연결용 OpenAI API 키 발급(루크) · 원장님께 상담 정책 10가지 답 받기 · 원장님 답 채우기(주차·예약금·취소 규정·소요 시간) + 카카오 채널·톡톡에 주소 연결", "기한 없음 · 답은 /admin-chat '원장님이 알려주는 답'에 입력 (10/5 등록 3건)", _N+"3f00cf8fea04818a937efb1274c10b22", False),
  ("루크 툴박스 — 자동화 도구 구매 검토 결과 확인 + 루크 결정(환불 기준·설치 대수·윈도우/맥·네이버 계정 처리·결제 방식) · 원크루 페이지 결정 5가지 + 루크 사진·영상 전달", "기한 없음 · 원크루 페이지 1단계 개선은 10/5 배포 완료 (10/5 등록 2건)", _N+"3ef0cf8fea048144b71af1d096a2f0a2", False),
  ("원크루 라운지에 처음 열어 둘 자료 하나 정하기", "기한 10/31 · 대문 '살아 있는 느낌' 3.4점 — 실제 자료가 있어야 오름 · 루크가 자료 이름이나 파일을 주면 클로드가 넣음 (10/5 등록)", _N+"3f00cf8fea0481aea406c7180d0e367b", False),
  ("멘토루크 파인더 — 네이버 쇼핑 검색 API 종료(2026-07-31) 대응", "기한 10/31 · 진행 중 (10/5 등록)", _N+"3ef0cf8fea0481deb27cffcc5b9737ca", False),
  ("법인 정리 — 공고방법을 홈페이지 게재로 변경(10/15) · 지분을 주식 양도로 줄지 증자로 줄지 결정 · 창고형 매장 후보지 과밀억제권역 확인 · 3PL 창고 취득세 중과 제외 업종 확인 · 꼬마빌딩 지역·시점·명의 · 힐링디어스로 받을 매출 하나 정하기 · 법인 서류 클라우드 폴더 · 주소 박힌 것 전부 교체", "나머지 기한 10/31 · <a href=\"../corp/\">힐링디어스 → 셀러들의 수다</a> (10/7 등록 8건)", _N+"3f10cf8fea04818d8bc4e8dd106ecd1c", False),
  ("창고형 매장 우리 재고로 4주 시범 판매 · 주간 매출·판매율 기록", "기한 11/8 (10/7 등록)", _N+"3f10cf8fea048113a3d7c503eec00deb", True),
  ("초월스토리 — PG 수수료 요율과 실제 광고비 비율 숫자 확보", "기한 10/31 · 둘만 들어오면 배분표가 하나로 확정 · 지금은 PG 3.5% 가정·광고비 세 시나리오로 계산해 둠 (10/8 등록)", _N+"3f30cf8fea04813d8880ee10ef500869", True),
  ("초월스토리 — 파일럿 강사 후보 소개(10/20) · [결정 필요] 상품 최종 확정(10/22) · 전환율 가정 검증·광고비 상한(10/24) · 협업 모델 옵션·배분 초안 확정(10/29) · 런칭용 성과자 섭외(10/31)", "과거 전환율 3%와 목표 10% 사이 (10/6 등록 5건)", _N+"3f10cf8fea048167bc15f5dc0646b939", True),
  ("셀수다 프로그램 구독 — 구독 사이트 구축·오픈(수강생 라운지·부업 콘텐츠·비수강생 구독) · 토스 결제 연동+깃허브 자동 설치·업데이트 · 프로그램 소개 유튜브 콘텐츠", "기한 10/31 · 같은 회의가 두 번 등록돼 구독 사이트 항목이 2건 (10/6 등록 4건)", _N+"3f10cf8fea048194b729fa84b69c9a04", True),
  ("메이븐 스토어·3PL — 매출 우수 상품 링크 받아 추가 판매 전략 세팅(루크) · 재고 못 판 수강생 상품 위탁판매+판매 일지(메이브님) · 물동량 일 200건·월 6,000건 확대 → 택배비 재협상(메이브님)", "기한 10/31 (10/6 등록 3건)", _N+"3f10cf8fea048109be61c95277b4895a", True),
  ("인베이더 종료 대비 — 졸업 후 반복 매출 가격안(프로그램 월 구독 + 3PL 등급) · 6기·4기 수강생 성과·후기·비포애프터 수집 · '사입으로 수익 낸 사례' 특강 정기 개최", "기한 10/31 (10/6 등록 4건)", _N+"3f10cf8fea048137bd9ac4df5325f1d0", True),
  ("뿌요님 — 12월 이후 자체 수익 구조 설계 · 역할·수익 배분 결정 · 목표 수익 관리 페이지(원크루) · 3화 '연쇄적금러' 촬영·편집(10/17)", "나머지 기한 10/31 (10/6 등록 4건)", _N+"3f10cf8fea0481128cfad15cee935285", True),
  ("미용 가격비교 — 헤어·메이크업 가격비교 사이트 + 커뮤니티 구축(공지된 가격만 사용) · [결정 필요] 쿠팡 가격비교 크롤링은 플랫폼 정책 검토 후 개발 여부 결정", "기한 10/31 (10/6 등록 2건)", _N+"3f10cf8fea0481de9320eb05efd9034d", False),
  ("디노 전자책 제작 지원 여부 결정 · 역할 분담 합의", "기한 10/17 · 플라우드 10/6 디노 미팅 Action Item (10/7 등록)", _N+"3f10cf8fea0481498097ea0e7aff1dff", True),
  ("돈블지PD 오프라인 사업 수익 구조화", "플라우드 10/6 메이브님 회의 Action Item · 이름은 녹음 표기 그대로, 기한 10/31은 추정 — 확인 필요 (10/7 등록)", _N+"3f10cf8fea04810a8527ca4796cb449c", True),
  ("가을(정복녀) 대표님 수락 시 3주 강사 런칭 준비 — 1주 판매·방향 / 2주 커리큘럼·자료 / 3주 리허설·모객", "기한 10/28 (10/7 등록)", _N+"3f20cf8fea048154938ac0f560b7918f", True),
  ("김종진 대표님 조사 결과·조사 로그 검토 후 다음 코칭 피드백", "기한 10/14 · 대표님 숙제(키워드 검색량·커뮤니티 질문·조사 로그)를 받으면 검토 · 플라우드 10/7 코칭 Action Item과 같은 일 (10/7 등록)", _N+"3f20cf8fea0481518c46c8db8a768cb7", True),
  ("지영 원장 빌드업 페이지 — 숫자 받기(매출·순이익·본인 몫, 객단가·예약 건수·재방문율·시술별 비중 등) · 새 저장소 kittiti-jiyoung 생성 + Pages 켜기", "기한 10/31 · <a href=\"../jiyoung-prompt/\">프롬프트</a> (10/7 등록 3건)", _N+"3f20cf8fea0481a78df0ec77cc00af96", True),
  ("원크루 사이트 — crew.json 형식을 기존 자료실 규칙과 맞출지 확인 · 크루원 페이지 슬러그 규칙 확정 + 첫 사람에게 시험 적용", "기한 10/31 · <a href=\"../crew-prompt/\">크루원 프롬프트</a> (10/7 등록 2건)", _N+"3f20cf8fea048108aabccb4ecbf32b15", False),
  ("루크 툴박스 검색·AI 요약 정리 후속 — 채널 주소 전달과 '미니쏜' 정체 확인", "기한 없음 (10/7 등록)", _N+"3f20cf8fea04819d9fa9e130cdaba0fc", False),
  ("법인 등기 뒤 — 등기 끝난 뒤 할 일 10가지(사업자등록 정정·법인인감 재제작·사무실에 상호 통지·통신판매업 변경신고) · 법인 지방세 체납 여부 확인(위택스 납세증명서 발급 시도) · 비상주 사무실 계약 조항 3개 대응(우편물 폐기·말소 위임·만료일)", "앞 둘은 기한 10/31, 사무실 계약 조항은 기한 없음 · 체납이 있어도 이번 등기에는 지장 없음(노션 메모) (10/9 등록 3건)", _N+"3f40cf8fea0481c99265f4b17f2ddc0c", False),
  ("박종혁 본부장 사무실 좌석 마련 + 온보딩 지원 · 유튜브 콘텐츠 전략 재구성(수강생 성장 스토리 + 전문가 인사이트, 본부장과 공동)", "플라우드 10/9 회의 Action Item · 기한 10/19·10/31은 추정 — 확인 필요 (10/10 등록 2건)", _N+"3f40cf8fea048178bbbbeb6b52524035", False),
  ("[결정 필요] 원크루 수익화전략 02~10번 주제 확정", "기한 없음 · 후보 30가지와 추천 순서는 정리됨 · 08번(법인과 세금)은 숫자 확인·세무사 검토 문구 필요 (10/9 등록)", _N+"3f40cf8fea0481bf97e4e7de0fc3ce84", False),
 ],
 "P2": [
  ("초창패 PSST 계획서 초안 12월 안에 완료", "기한 12/31 · 3개월 실측 숫자·파트너 의향서·대표자 자격 증빙 반영 (10/4 등록)", _N+"3ef0cf8fea0481859a20e212db58d884", True),
  ("헤메네일 — [결정 필요] 카카오 로컬 API로 추천 1~3위 업종 실시간 대조(표시만 vs 순위 반영)", "기한 11/30 · 함께 묶였던 '영업 확인 목록 월간 갱신'은 10/5 예약 작업으로 자동화돼 완료 (10/4 등록)", _N+"3ee0cf8fea048171ad3ef13b0f780e44", False),
  ("서울 꼬마빌딩 취득·잔금은 2027-03-16(설립 5년 충족일) 이후로 — 용도로는 중과를 못 피함", "기한 2027-03-16 (10/7 등록 2건)", _N+"3f10cf8fea04819f838bcf83d9a08e94", False),
  ("수강생 입점 조건 문서 — 수수료 15~20%·정산 주기·보관 기간·미판매 반환", "기한 11/30 · 창고형 매장 시범 판매 숫자 확인 뒤 공개 (10/7 등록)", _N+"3f10cf8fea048140bac9e2248d943be0", True),
  ("서울 이전 — 후보 빌딩·공동 투자자 정보 수집, 이전할지 미룰지 먼저 결정", "기한 11/30 · 계약 판단은 반복 매출 확인 후 (10/6 등록 2건)", _N+"3f10cf8fea048148b8a6eb95f9649d5d", True),
  ("1인 사업자용 블로그·카톡 자동화 구독 사이트 기획", "기한 11/30 (10/6 등록)", _N+"3f10cf8fea04819e984acdd675ae57bb", True),
  ("쿠팡 가격 비교 프로그램 — 개발 전 크롤링 정책 위험 검토", "기한 11/30 (10/6 등록)", _N+"3f10cf8fea0481188729f52df28c4e34", False),
  ("메이븐 스토어 4분기 순수익 월 1,000만", "담당 메이브님 · 기한 12/31 · 진행 중 (10/6 등록)", _N+"3f10cf8fea04811aa006c92f5797461a", True),
  ("답변 웹페이지 발행 위치를 깃허브에서 원하는 위치로 바꾸기", "기한 11/30 (10/6 등록)", _N+"3f10cf8fea0481789832f2fffe8102c8", False),
  ("꼬마빌딩 담보대출 심사 전에 대표자 신용 정리 마치기", "기한 2027-01-31 · 잔금은 2027-03-16 이후 · <a href=\"../credit/\">신용점수 페이지</a> (10/7 등록)", _N+"3f20cf8fea048176bc01e7f629aa7309", True),
  ("수익모델 소개 사이트 개설 (100만 챌린지·마진 키워드)", "기한 없음 · 일십백천과 무관한 자료 분류·제작용 프롬프트는 준비됨 (10/8 등록)", _N+"3f20cf8fea04813098e0dc55cf5d6ecc", False),
  ("박종혁 협업 커머스 — 소싱 자동화 프로그램 테스트 + 위탁 중심 물류 운영 체계 설계", "플라우드 10/9 회의 Action Item(중장기) · 기한 11/30은 추정 — 확인 필요 (10/10 등록)", _N+"3f40cf8fea04813cb438ce0216f8b59c", False),
  ("[결정 필요] 트리플 플라이휠 자료에 의사 선생님 이름을 밝힐지", "기한 없음 · 지금은 이름 없이 게시 — 밝히려면 대화·장면을 사실에 맞게 다시 써야 함 (10/9 등록)", _N+"3f40cf8fea0481e19bced078b7db3b07", False),
 ],
 "P3": [
  ("[공개 직전] 헤메네일 업종별 정보 페이지 테마 (헤어·메이크업·네일 별도 톤)", "공개 직전에 할 일 · 기한 없음 (10/3 등록)", _N+"3ee0cf8fea0481ef8c22d7f5a93de94e", False),
  ("[공개 직전] 헤메네일 — 개인정보 보호책임자 이름·이메일 정하기 · 도메인 연결 뒤 검색 등록(구글 서치콘솔·네이버 서치어드바이저) · 카카오 링크 도메인 등록 후 '카카오톡으로 보내기' 버튼 켜기", "공개 직전에 할 일 · 기한 없음 (10/5 등록 3건)", _N+"3ef0cf8fea0481bfaf94d3c15ebbf9b9", False),
  ("[보류] 뿌요 파일럿 강사 기용 — 앞(강사)과 뒤(상담·운영) 자리 분리", "기한 없음 · <a href=\"../pilot/\">파일럿 강사 결정</a> (10/7 등록)", _N+"3f10cf8fea0481d09753d0013e1c7bd7", True),
  ("2028년 3월 중임등기 — 루크·감사 임기 만료", "기한 없음 · 등기부 기준 2025-03-16 중임이라 2028년 3월 전후 만료, 놓치면 과태료(500만원 이하) · 캘린더에 넣어 둘 것 (10/9 등록)", _N+"3f40cf8fea0481b48dedebc3ae86c46d", False),
 ],
}

def new_items_html(p):
    out = []
    for t, m, n, cash in NEW_ITEMS[p]:
        attr = f' data-n="{n}"' if n else ""
        tags = '<span class="tag">새 항목</span>' + ('<span class="tag cash">현금</span>' if cash else "")
        memo = f'<div class="m">{m}</div>' if m else ""
        out.append(f'    <li{attr}>{tags}<div class="t">{t}</div>{memo}</li>')
    return "\n".join(out)

for _p in ("P0", "P1", "P2", "P3"):
    PRIORITY = PRIORITY.replace(f"__NEW_{_p}__", new_items_html(_p))


# ---------------------------------------------------------------- 사람별
PEOPLE = """
<h1>사람별 현황</h1>
<p class="note">같이 돈을 만드는 사람 순. 관계·현재 상태·돈 흐름·다음 할 일만 적었습니다. 개인사는 뺐습니다.</p>

<h2>메이브님 · 뷰셀 (신정현)</h2>
<div class="card accent">
  <dl class="kv">
    <dt>관계</dt><dd>협력 계약(직원 아님), 같은 사무실. 현재 매출을 만들어주는 핵심 인력. 스토어 물류는 수희</dd>
    <dt>돈 흐름</dt><dd>강사 런칭(인베이더) 실효 수취율 GMV의 20% · 메이브님 수강생이 루크 수강생보다 훨씬 많이 유입 중 → 컨설팅 판매 배분 사전 합의 필요</dd>
    <dt>지금</dt><dd>9/29 신규 강의 플랫폼 회의: 3자 구도(강사/기획·커뮤니티/모객), 1:1:1 배분, 인베이더 반면교사, 내년 초 서울 이전 논의 · 뷰셀 유튜브 2화 진행(촬영 10/2, 공개 10/7)</dd>
    <dt>다음</dt><dd>초이스토리 PD 화상 미팅 → 10/8 종혁 본부장 미팅 · 캔바 재결제·클로드 유료 전환 · 가격관리 프로그램 스크롤 버그</dd>
  </dl>
</div>

<h2>디노 · 미니쌤 (김수민)</h2>
<div class="card">
  <dl class="kv">
    <dt>관계</dt><dd>협력 계약, 같은 사무실. 첫 런칭 부진 후 반사입 모델로 전환한 사례. 30대 중후반</dd>
    <dt>지금</dt><dd>9월 초 관계·계약 재정리 논의 → 9/28 멘토링에서 긍정적 변화 확인. 독립적인 신규 수익 모델 원함: <b>3개월 내 월 300만</b></dd>
    <dt>플랜</dt><dd>『미니쌤, 12주의 지도』— AI 셀러 실무 교육 (파일럿 2.9만 → 키트 2.9만/원데이 4.9만 → 실무반 39만, 대행 15만/건) · 1달 90 / 2달 200 / 3달 350만 · 10/5 1주차</dd>
    <dt>병행</dt><dd>힉스필드 등 AI 영상 학습을 인스타 '공부 N일차'로 기록 → 무료 전자책 → 유료 전자책 · 디노 전용 AI 서비스·프로그램 판매 사이트(루크가 구축)</dd>
    <dt>다음</dt><dd>린 MVP 테스트(7~10일 주기, 광고 10만) 반복 · 아이템 100개 리스트 · 시간 기록</dd>
  </dl>
</div>

<h2>뿌요 (최근영)</h2>
<div class="card">
  <dl class="kv">
    <dt>관계</dt><dd>디노 쪽 스태프이자 물류·코칭 담당. 물류 업데이트/운영 책임자 후보(9/30 지정)</dd>
    <dt>돈 흐름</dt><dd>발주(시간당 2만, 월 150만 수준) + 코칭/컨설팅(일 최대 12건) → 월 450만대 구조 목표. 발주는 금요일부터</dd>
    <dt>포지션</dt><dd>직함 '교육실장'으로 통일, 병원 상담실장급 톤앤매너 · 컨설팅 40분 표준 + 20분 정비</dd>
    <dt>다음</dt><dd>연휴 이후 컨설팅 오픈 안내 · 프로세스 맵(10/2) · 피크일 운영안·금요일 사전 공지(10/4) · 선반·라벨링(10/10) · 3기 종료 후 이미지 메이킹 지원(루크)</dd>
  </dl>
</div>

<h2>윤지영 · 키티티바이지영</h2>
<div class="card">
  <dl class="kv">
    <dt>관계</dt><dd>성신여대 인근 메이크업샵 컨설팅. 유료 자문(월 고정 + 매출 연동)으로 전환 예정</dd>
    <dt>지금</dt><dd>1인샵 월 450~1,100만 매출 · 웨딩 중심 프리미엄 토탈샵 확장 계획(헤어·메이크업·에스테틱) · 초기 고정비 약 1.1억, 부족분 약 5,000만 조달 방안 미정 · 정부지원사업으로 내년 최소 1억 조달 목표(2027-03~)</dd>
    <dt>만든 것</dt><dd>모바일 상담 사이트 v1 · 네이버 플레이스 카드뉴스 5종 · 블로그 타이퍼(키워드 전략 재검토: '데일리메이크업' 등 시술명 중심)</dd>
    <dt>다음</dt><dd>상표권 출원(지영 명의 전자출원 진행 중 · 10/4) · 인스타 주간 캘린더(10/1) · 상담 사이트 원장 확인(10/5) · 대시보드(10/7) · 10/8 미팅(지원사업 후보 3개·사업계획서 초안) · 조달 마일스톤(10/15) · 샵 2월 오픈</dd>
  </dl>
</div>

<h2>그 외</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">루나</div><div class="m">콘텐츠 제작·발행 총괄. 3PL 재고 사진 촬영 담당. 가장 레버리지 큰 팀원</div></li>
    <li><div class="t">리나님 (물류)</div><div class="m">시간 기록 시트 2주 시범(9/29~10/12) → 크롬 확장 설계 · 10/8 지시: 물동량 많으면 미리 도움 요청, 문제점·일정 스프레드시트 공유</div></li>
    <li><div class="t">박태경 대표 (원크루)</div><div class="m">9/30 세션 진행 · 다음은 5회차(준비 10/7) · 루크가 줄 것: 사입 재고 스프레드시트(10/2), 상품·가격 체크리스트(10/4), 안내 템플릿 3종(10/5) · 100문100답 세션 내 공동 작성 · 결정 규칙표·손절 규칙표</div></li>
    <li><div class="t">최은봉 대표 (원크루) — 메이크업헬퍼</div><div class="m">계약 원안대로 체결(9/30 녹음) · 당근 광고 테스트 3만~10만, 팩트 중심 세트 · 부진하면 토스로 이동 · 매주 수요일 14:00 미팅(노션에는 10/8로 기록 — 날짜 확인 필요) · 10/20 2주 판정</div></li>
    <li><div class="t">종혁 본부장 / 초이스토리 PD</div><div class="m">신규 강의 플랫폼 협업 후보. PD 먼저, 본부장 10/8</div></li>
  </ul>
</div>
"""

# ---------------------------------------------------------------- 일정
def _tl_li(e):
    cls = "big" if e["cash"] else ""
    d = datetime.date.fromisoformat(e["d"])
    wd = "월화수목금토일"[d.weekday()]
    return f'<li class="{cls}"><div class="d">{e["d"][5:].replace("-","/")} ({wd}) · {e["who"]} · {e["p"]}</div><div class="t">{e["t"]}</div></li>'

def _tl_split():
    # 갱신일 기준 14일보다 더 밀린 항목은 접어서 보여준다
    cut = (datetime.date.fromisoformat(UPDATED) - datetime.timedelta(days=14)).isoformat()
    return [e for e in EVENTS if e["d"] < cut], [e for e in EVENTS if e["d"] >= cut]

def timeline_html():
    return "\n".join(_tl_li(e) for e in _tl_split()[1])

def timeline_old_html():
    return "\n".join(_tl_li(e) for e in _tl_split()[0])

SCHEDULE = f"""
<h1>일정 도식</h1>
<p class="note">노션 액션보드에서 미완료이고 기한이 있는 것 + 회의에서 정한 기한. 금색 점은 현금에 직접 닿는 일(노션 목표 기준). 날짜가 없는 일은 <a href="../priority/">우선순위</a>에. 기한이 지났는데 남아 있는 줄은 노션 상태가 아직 완료가 아니라는 뜻입니다.</p>

<h2>하루 슬롯 <small>6시간 × 4</small></h2>
<div class="card">
  <div class="slots">
    <div><b>슬롯 1</b>딥워크<br>개발·대본</div>
    <div><b>슬롯 2</b>사람<br>컨설팅·미팅</div>
    <div><b>슬롯 3</b>실행<br>운영·촬영·발주</div>
    <div><b>슬롯 4</b>정리<br>기록·다음날</div>
  </div>
  <div class="note">한 슬롯 = 한 산출물. 고인지 작업은 앞 슬롯, 소통·실행은 뒤 슬롯. 슬롯 사이에 종료-준비-시작 리추얼(9/29 메모). 7일 파일럿 후 영상으로.</div>
</div>

<h2>타임라인 <small>최근 2주 밀린 것 → 앞으로</small></h2>
<div class="card">
  <ul class="tl">
    {timeline_html()}
  </ul>
</div>
<div class="card">
  <details class="donebox"><summary>2주 넘게 밀린 항목 {len(_tl_split()[0])}건 (노션 상태 정리 필요)</summary>
  <ul class="tl" style="margin-top:10px">
    {timeline_old_html()}
  </ul></details>
</div>

<h2>마일스톤</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">10/8 · 신규 강의 플랫폼 3자 구도 결정</div><div class="bar"><i style="width:30%"></i></div><div class="m">PD 접촉 → 본부장 미팅 → 배분안 합의 · 10/8 본부장 미팅 진행 여부·결과 확인 필요</div></li>
    <li><div class="t">10월 말 · 무료 라이브 → 신규 리스트</div><div class="bar"><i style="width:20%"></i></div><div class="m">록터뷰 2회차 촬영 완료 · 날짜 10/25(일)는 10/4 노션 [결정]으로 확정 · 시간 19:00는 10/2 녹음 언급값, 신청 링크 확인 필요</div></li>
    <li><div class="t">11월 말 · 메이크업헬퍼 9주차 판정</div><div class="bar"><i style="width:15%"></i></div><div class="m">계약 체결 완료(9/30 녹음) · 10/1 당근 광고 테스트 시작 예정이었음(시작 여부 확인 필요) · 10/20 2주 판정</div></li>
    <li><div class="t">12월 · 툴박스 500명</div><div class="bar"><i style="width:10%"></i></div><div class="m">사이트 구축 완료, 결제 심사·공개 문구 남음</div></li>
    <li><div class="t">2027 2월 · 키티티 샵 오픈</div><div class="bar"><i style="width:25%"></i></div><div class="m">상표권 출원 10/1이 마지노선이었음 — 지영 명의 전자출원 '진행 중'(노션 기한 10/4) · 10/8 토탈샵 임대차 계약 체결(플라우드 녹음 기준), 1월 말 가오픈 계획</div></li>
    <li><div class="t">2027 1분기 · 서울 이전 검토 · 회사 자체 강의</div><div class="bar"><i style="width:5%"></i></div><div class="m">플랫폼 안정화가 전제</div></li>
  </ul>
  <div class="note">진행 막대는 기록 기준의 대략적 감각값입니다(측정치 아님).</div>
</div>
"""


# ---------------------------------------------------------------- 철학 (원크루·일십백천)
PHILOSOPHY = """
<h1>삼각 파이프라인</h1>
<p class="note">루크가 원크루에서 가르치고, 일십백천에서 그중 '브랜딩'을 집중하는 수익 구조의 설명서. 다른 채팅에서 판매 페이지·강의안을 만들 때 이 페이지를 먼저 읽히면 됩니다. 이름은 '3 파이프 체이닝'을 다듬은 <b>삼각 파이프라인(Tri-Pipe)</b> — 세 줄이 서로를 떠받쳐서 하나가 흔들려도 무너지지 않는 구조.</p>

<h2>한 문장</h2>
<div class="card accent">
  <p style="font-size:17px;font-family:'Gowun Dodum',sans-serif;margin:0"><b>서로 연결된 세 개의 수익 줄</b>을 만들어, 한 줄이 휘청여도 다른 두 줄이 받쳐주고, 각 줄의 손님이 다른 줄로 흘러가게 하는 것.</p>
  <p class="note">독립된 파이프 세 개는 부업 세 개일 뿐입니다. 연관된 파이프 세 개가 사업입니다.</p>
</div>

<h2>도식 <small>가정의학 의사 예시</small></h2>
<div class="card">
  <svg viewBox="0 0 560 330" width="100%" role="img" aria-label="삼각 파이프라인 도식" style="font-family:'Noto Sans KR',sans-serif">
    <defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--muted)"/></marker></defs>
    <line x1="280" y1="70" x2="120" y2="255" stroke="var(--muted)" stroke-width="2" marker-end="url(#ar)" marker-start="url(#ar)"/>
    <line x1="280" y1="70" x2="440" y2="255" stroke="var(--muted)" stroke-width="2" marker-end="url(#ar)" marker-start="url(#ar)"/>
    <line x1="120" y1="255" x2="440" y2="255" stroke="var(--muted)" stroke-width="2" marker-end="url(#ar)" marker-start="url(#ar)"/>
    <g><rect x="190" y="10" width="180" height="70" rx="14" fill="var(--accent)"/><text x="280" y="38" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">① 채널 · 브랜딩</text><text x="280" y="60" text-anchor="middle" fill="#fff" font-size="12">다이어트 영상 → 신뢰·채널 수익</text></g>
    <g><rect x="20" y="240" width="200" height="70" rx="14" fill="var(--gold)"/><text x="120" y="268" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">② 지식 · 책/강의</text><text x="120" y="290" text-anchor="middle" fill="#fff" font-size="12">책·강의 → 지식창업 + 신규 유입</text></g>
    <g><rect x="340" y="240" width="200" height="70" rx="14" fill="var(--blue)"/><text x="440" y="268" text-anchor="middle" fill="#fff" font-size="15" font-weight="700">③ 상품 · 유통</text><text x="440" y="290" text-anchor="middle" fill="#fff" font-size="12">다이어트 단백질 → 매출 + 유입</text></g>
    <text x="280" y="180" text-anchor="middle" fill="var(--muted)" font-size="12">손님이 세 줄 사이를 돈다</text>
    <text x="280" y="198" text-anchor="middle" fill="var(--muted)" font-size="12">한 줄이 꺼져도 두 줄이 받친다</text>
  </svg>
  <div class="note">화살표가 양방향인 것이 핵심. 영상 보던 사람이 책을 사고, 책 독자가 단백질을 사고, 단백질 산 사람이 채널을 구독합니다.</div>
</div>

<h2>세 줄이 하는 일</h2>
<div class="card wrapx">
<table>
<tr><th>줄</th><th>역할</th><th>돈</th><th>다른 줄로 보내는 것</th></tr>
<tr><td><b>채널·브랜딩</b></td><td>신뢰를 만든다. 사람이 나를 알게 되는 입구</td><td>채널 수익(광고·멤버십)</td><td>책·강의 구매자, 상품 첫 고객</td></tr>
<tr><td><b>지식·책/강의</b></td><td>신뢰를 돈으로 바꾸고, 검색·서점에서 새 사람을 데려온다</td><td>책·강의·컨설팅</td><td>채널 구독자, 상품 재구매 고객</td></tr>
<tr><td><b>상품·유통</b></td><td>반복 매출. 신뢰가 없어도 상품 자체로 유입이 생긴다</td><td>판매 마진·공급</td><td>후기 → 채널 콘텐츠, 고객 → 강의 수강생</td></tr>
</table>
</div>

<h2>루크 자신의 삼각형 <small>지금 돌아가는 것</small></h2>
<div class="card gold">
  <div class="steps">
    <div><b>채널</b>유튜브 1만 · 카톡 1천 · 카페 · 뷰셀</div>
    <div><b>지식</b>강의 · 원크루 · 일십백천 · 툴박스</div>
    <div><b>상품·유통</b>3PL · 재고 판매 · 위탁 · 자동등록 도구</div>
  </div>
  <div class="note">가르치는 구조를 본인이 먼저 돌리고 있다는 것이 원크루의 증거 자료입니다.</div>
</div>

<h2>원크루 (ONE CREW)</h2>
<div class="card">
  <dl class="kv">
    <dt>무엇</dt><dd>평생 파트너십 컨설팅. 한 사람의 삼각 파이프라인을 <b>같이 설계하고 세우는 것</b>이 목표</dd>
    <dt>가격</dt><dd>정가 3,900만 원 · 루크 수강생 출신 3,300만 원 · 네이버페이 할부(신한카드 최대 60개월 세팅 가능)</dd>
    <dt>누구</dt><dd>이미 한 줄(대부분 스마트스토어 판매)로 돈을 벌어본 사람. 두 번째·세 번째 줄을 세우려는 사람</dd>
    <dt>방식</dt><dd>1:1 세션 + 세션 사이 과제. 100문100답(돈·시간·결정의 철학 점검) → 숫자 점검(매출·결제 건수 그래프) → 결정 규칙표·손절선·현금흐름 캘린더를 세션 안에서 같이 작성. 세션마다 교육자료 페이지·PDF 전자책으로 정리해 전달</dd>
    <dt>실제 사례</dt><dd>박태경 대표(스토어 운영 점검 → 객단가·결정 규칙) · 최은봉 대표(위탁판매 → 당근·토스 신규 채널 → 자체 브랜드·정부지원 구상까지 12주 계획) · 김종진 대표(정체 진단 → '자기만의 것' 탐색 일지)</dd>
  </dl>
</div>

<h2>일십백천</h2>
<div class="card">
  <dl class="kv">
    <dt>무엇</dt><dd>삼각형 중 <b>'브랜딩' 한 축에 집중</b>하는 브랜드 인큐베이팅 프로그램. 약 400개 영상 강의 + 1:1 컨설팅</dd>
    <dt>가격</dt><dd>정가 990만 원 (할인가는 안내하지 않음)</dd>
    <dt>이름 뜻</dt><dd>1 → 10 → 100 → 1,000 — 매출 계단을 한 단씩 올라가는 로드맵</dd>
    <dt>브랜딩의 세 형태</dt><dd><b>아이템</b>(햇반처럼 제품 자체가 브랜드) · <b>회사</b>(다이슨·샤오미) · <b>사람</b>(인플루언서·유튜버). 어느 것이 될지는 탐색해봐야 안다</dd>
    <dt>원크루와의 관계</dt><dd>일십백천 = 한 축을 세우는 것. 원크루 = 세 축을 잇는 것. 일십백천 수료자가 원크루로 올라오는 사다리</dd>
  </dl>
</div>

<h2>불씨 이론 <small>아이템·사업을 고르는 법</small></h2>
<div class="card accent">
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">불씨를 확인하려면 새로운 자극을 탐험해야 한다</div><div class="d">안 가본 카페, 안 뛰어본 코스, 박람회, 낯선 사람에게 말 걸기 — 실제로 내준 과제들</div></li>
    <li><div class="t">불씨를 키우려면 AI와 대화하며 확인한다</div><div class="d">"이게 맞나, 호기심이 이어지나" — 소개팅 일지처럼 기록. 계속 생각나는 아이템이 내 것일 확률이 높다</div></li>
    <li><div class="t">꺼지면 넘어간다 — 선택·집중·빠른 피벗</div><div class="d">7~10일 단위 린 테스트, AI로 2~3일 만에 MVP(전자책·상품 페이지), 광고 10만 원. 재미도 성과도 없으면 미련 없이 다음</div></li>
    <li class="big"><div class="t">보이기 시작하면 난로처럼 관리한다</div><div class="d">불씨 3~5개, 길어야 30개 안에 내 것이 보인다. 그때부터는 오래, 크게 — 큰 불이 된다</div></li>
  </ol>
  <p class="note" style="margin-top:4px"><b>피벗의 진짜 뜻:</b> 하나에 매달리지 않고 확인하고 넘어가는 것. 결혼을 전제로 연애하면 시작조차 못 한다. 성실함은 억지로 만드는 게 아니라 내 것을 만났을 때 저절로 나온다.</p>
</div>

<h2>코칭에서 반복해서 나오는 원칙</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">시간을 돈으로 환산해서 결정한다</div><div class="m">월 1,000만이면 24시간 내내 시간당 약 14,000원. 그 가치가 안 나오는 만남·일은 미룬다</div></li>
    <li><div class="t">완벽한 관리보다 손실을 감수하는 운영</div><div class="m">주문 5건 15분, 3~5분 안에 못 찾으면 역마진 처리, 표본 검사 3~4건. 디테일을 다 붙드는 것은 경영이 아니다</div></li>
    <li><div class="t">CS는 최대 만족이 아니라 불만 최소화</div><div class="m">브랜드가 아니면 필요악. 톡톡·게시판 중심, 필요한 정보를 한 번에 요청</div></li>
    <li><div class="t">선매입 금지 · 반사입부터</div><div class="m">팔린 뒤 사입. 재고 리스크가 모든 모델의 최대 위험</div></li>
    <li><div class="t">전쟁이 아니라 평시 전략</div><div class="m">영끌·채찍질이 아니라 성장 동력을 찾는 시기. 지속 가능한 모델만 살아남는다</div></li>
    <li><div class="t">시간을 돈으로 바꾸는 단계 → 가치를 돈으로 바꾸는 단계</div><div class="m">먼저 시간당 과금으로 안정, 그다음 마진율·강의·브랜드</div></li>
    <li><div class="t">규칙·손절선·책임분담을 글로 남긴다</div><div class="m">"10년 전에 없었던 세 가지". 결정 규칙표, 손절 규칙표, 현금흐름 캘린더</div></li>
    <li><div class="t">쉬는 것도 투자다</div><div class="m">번아웃은 버티기로 안 풀린다. 혼자·낯선 곳·연락 차단으로 비워내고 온다</div></li>
  </ul>
</div>

<h2>다른 채팅에 넘길 때</h2>
<div class="card gold">
  <p style="font-size:14px;margin:0">"<b>https://yoo-mideum.github.io/luke-1b/philosophy/</b> 읽고 원크루(또는 일십백천) 판매 페이지 만들어줘" 라고 하면 됩니다. 톤은 '정리해주는 선배' — 설득이 아니라 정리. 보장형 문장("누구나 월 100")은 쓰지 않습니다.</p>
</div>

<div class="src" style="margin-top:14px">근거: 9/27 김종진 대표 멘토링 · 9/28 디노 멘토링 · 9/10 박태경 원크루 1회차 · 9/16 최은봉 원크루 · 9/11·9/16 뿌요 상담 · 9/25 특강 '순수익 300만원을 위한 시간 운영과 사입' · 9/26 오픈채팅 문의 답변(가격) · 9/30 루크 설명(삼각 파이프라인·불씨)</div>
"""


# ---------------------------------------------------------------- 강의 플랫폼 전략
PLATFORM = """
<h1>강의 플랫폼 전략</h1>
<p class="note">9/29 메이브님 회의 + 9/30 루크 정리. 인베이더 없이 우리끼리 강의 플랫폼을 돌리기 위한 3자 구도. 이름·역할은 루크 구두 기준이며 상대방과 아직 합의 전입니다.</p>

<h2>구도 한눈에</h2>
<div class="card">
  <svg viewBox="0 0 360 470" width="100%" role="img" aria-label="유입-락인-플레이어 구도" style="font-family:'Noto Sans KR',sans-serif;max-width:360px;display:block;margin:0 auto">
    <defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--muted)"/></marker></defs>
    <text x="180" y="24" text-anchor="middle" fill="var(--ink)" font-size="15" font-weight="700">수익 1 : 1 : 1 (3자 배분)</text>
    <text x="180" y="44" text-anchor="middle" fill="var(--muted)" font-size="12">250만 × 20명 = 5,000만 − 광고 1,000만 = 4,000만</text>
    <rect x="30" y="62" width="300" height="96" rx="16" fill="var(--blue)"/>
    <text x="180" y="92" text-anchor="middle" fill="#fff" font-size="18" font-weight="700">① 유입 · 모객</text>
    <text x="180" y="116" text-anchor="middle" fill="#fff" font-size="14">초이스토리 PD</text>
    <text x="180" y="138" text-anchor="middle" fill="#fff" font-size="12">보유 채널·인력 풀로 특강 신청자 모집</text>
    <line x1="180" y1="160" x2="180" y2="186" stroke="var(--muted)" stroke-width="2.5" marker-end="url(#ar2)"/>
    <rect x="30" y="190" width="300" height="96" rx="16" fill="var(--gold)"/>
    <text x="180" y="220" text-anchor="middle" fill="#fff" font-size="18" font-weight="700">② 락인 · 커뮤니티</text>
    <text x="180" y="244" text-anchor="middle" fill="#fff" font-size="14">종혁 본부장</text>
    <text x="180" y="266" text-anchor="middle" fill="#fff" font-size="12">챌린지 영상 · 네이버 카페 · 광고 운영(같이)</text>
    <line x1="180" y1="288" x2="180" y2="314" stroke="var(--muted)" stroke-width="2.5" marker-end="url(#ar2)"/>
    <rect x="30" y="318" width="300" height="96" rx="16" fill="var(--accent)"/>
    <text x="180" y="348" text-anchor="middle" fill="#fff" font-size="18" font-weight="700">③ 플레이어 · 강사</text>
    <text x="180" y="372" text-anchor="middle" fill="#fff" font-size="14">루크 · 메이브님</text>
    <text x="180" y="394" text-anchor="middle" fill="#fff" font-size="12">강의 · 컨설팅 · 프로그램 · 강사 교육</text>
    <path d="M330,366 C356,366 356,110 332,110" fill="none" stroke="var(--muted)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ar2)"/>
    <text x="180" y="446" text-anchor="middle" fill="var(--muted)" font-size="12">수강생 성과·후기 → 다시 모객 소재로 (점선)</text>
  </svg>
</div>

<h2>역할표</h2>
<div class="card wrapx">
<table>
<tr><th>축</th><th>누가</th><th>하는 일</th><th>책임 지표</th></tr>
<tr><td><b>유입·모객</b></td><td>초이스토리 PD</td><td>보유 채널·인력 풀로 무료 특강 신청자 모집, 런칭 때 트래픽 공급</td><td>특강 신청자 수, 신청당 비용</td></tr>
<tr><td><b>락인·커뮤니티</b></td><td>종혁 본부장</td><td>챌린지 형식 영상 운영, 네이버 카페 운영으로 수강생 묶어두기, 광고 운영 설계(루크와 같이)</td><td>카페 활동률, 재등록·추천율, 환불률</td></tr>
<tr><td><b>플레이어·강사</b></td><td>루크 · 메이브님</td><td>강의·컨설팅·프로그램 제공, 신규 강사 교육·검증, 커리큘럼 관리</td><td>결제 전환율, 수강생 성과, 강사 배출</td></tr>
</table>
</div>

<h2>왜 이 구도인가 <small>인베이더에서 배운 것</small></h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">작은 수의 싸움을 할 사람이 있어야 한다</div><div class="m">인베이더는 부동산식 큰돈 집행에 익숙해 만 원·오천 원 단위 광고 효율을 못 봤다 → 광고 운영은 본부장·루크가 숫자로 같이 본다</div></li>
    <li><div class="t">모객을 안에서만 키우면 돈이 샌다</div><div class="m">자사 채널만 키우는 폐쇄적 운영이 실패 원인 → 이미 채널·인력 풀이 있는 PD를 모객 축으로</div></li>
    <li><div class="t">커뮤니티 전담이 없으면 강사가 현업과 운영을 동시에 못 한다</div><div class="m">수강생을 '다마고치'처럼 관리하는 전담 축이 필수 → 락인 축을 별도 인물로 분리하고 배분에 포함</div></li>
    <li><div class="t">상담 인력·강사 검증이 관료적이면 안 된다</div><div class="m">상담은 뿌요(교육실장) 라인, 강사 검증은 루크·메이브님이 직접</div></li>
  </ul>
</div>

<h2>순서</h2>
<div class="card">
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">이번 주</div><div class="t">초이스토리 PD 화상 미팅</div><div class="d">트래픽 유지엔 커뮤니티 운영이 필수라는 점 설명 → 커뮤니티 전담 포함 3자 모델 제안 → 긍정이면 다음 단계</div></li>
    <li><div class="d">10/8</div><div class="t">종혁 본부장 미팅</div><div class="d">락인 축(챌린지 영상·카페·광고) 역할과 1:1:1 배분안 제시. PD 반응을 들고 감</div></li>
    <li><div class="d">10월 중</div><div class="t">역할·배분·기간·IP 귀속을 문서 1장으로</div><div class="d">인베이더 때 못 한 것: 광고비 분담 명문, 콘텐츠·채널·수강생 DB 소유, 환불 시 정산 차감, 기간 2~3년</div></li>
    <li class="big"><div class="d">11~12월</div><div class="t">1기 런칭 (250만 × 20~25명)</div><div class="d">특강 무료 → 7일 다시보기 → 본강의. 광고 상한 1,000만, D+45 손익 리뷰</div></li>
  </ol>
</div>

<h2>미팅 전에 정할 것 <small>루크·메이브님</small></h2>
<div class="card accent">
  <ul class="list">
    <li><div class="t">배분 기준선</div><div class="m">1:1:1이 기본. 광고비를 누가 선부담하고 어느 시점에 차감하는지(선차감 후 배분 권장)</div></li>
    <li><div class="t">커뮤니티 전담자</div><div class="m">본부장이 직접 하는지, 본부장이 사람을 붙이는지. 후자면 그 인건비는 락인 축 몫에서</div></li>
    <li><div class="t">소유권</div><div class="m">카페·채널·수강생 DB는 누구 명의로 — 회사(힐링디어스) 명의 원칙</div></li>
    <li><div class="t">첫 상품</div><div class="m">1기는 메이브님 강의로 갈지, 루크 시그니처로 갈지, 둘 다인지</div></li>
    <li><div class="t">거절 기준</div><div class="m">PD가 '트래픽만 대고 배분은 더 달라'고 하면 어디까지 양보하는지 미리 정해두기</div></li>
  </ul>
</div>
<div class="src" style="margin-top:14px">근거: 9/29 메이븐 회의 녹음(플랫폼 구상·인베이더 분석·수치) · 9/30 루크 구두(역할 배정: PD=모객, 본부장=락인·챌린지·카페·광고, 루크·메이브님=플레이어·강사 교육) · 7월 10억 전략 대화(계약 조항). 이름 표기는 녹음 기준(초이스토리 PD·종혁 본부장) — 실명 확인 필요</div>
"""


# ---------------------------------------------------------------- 초월스토리 강사 협업
CHOWOL = """
<h1>초월스토리 강사 협업</h1>
<p class="note">10/6 두 건의 녹음에서 정리했습니다 — 16:30 촬영(온라인 셀러 자동화·성장 전략, 42분)과 17:22 메이브님·초월스토리 회의(신규 강사 협업 모델·런칭 계획, 48분). <a href="../invader/">인베이더가 접는다는 이야기</a>를 들은 당일에 그 자리를 대신할 틀이 잡힌 셈입니다.</p>

<h2>합의된 것</h2>
<div class="card accent">
  <dl class="kv">
    <dt>루크가 하는 일</dt><dd>강사 섭외 · 강의 기획 · PPT 제작 지원 · 라이브 코칭 · 프로그램 공유</dd>
    <dt>초월스토리가 하는 일</dt><dd>운영·모객·채널. 소수 정예로 임팩트 있는 강의를 지향</dd>
    <dt>루크 수수료</dt><dd><b>PG 수수료를 제외한 전체 매출의 8% 고정</b></dd>
    <dt>강사 배분</dt><dd>광고비 등 <b>모든 비용을 뺀 순수익을 초월스토리 : 강사 5:5</b>. 회의에서 광고비 비율은 숫자로 나오지 않았습니다 — 앞서 적었던 '총매출의 8%'는 제 오독이었고 지웠습니다</dd>
    <dt>강사 몫 재분할</dt><dd><b>가을 대표님 6 : 루크 4</b> — 10/8 루크 구두. 기준은 초월스토리가 가을 대표님께 제시할 약 2,200만이고 그중 4를 루크님이 받습니다. <b>초월스토리는 모르는 별도 계약</b>이며, 10/6 회의 녹음에는 이 비율이 없습니다</dd>
    <dt>PG 요율</dt><dd>회의에서 숫자 언급 없음 — <b>4% 가정</b>(10/8 루크)</dd>
    <dt>광고비</dt><dd>회의에서 숫자 언급 없음. 강사 제시액 2,200만에서 역산하면 <b>약 4,500만, 매출의 44.6%</b>(ROAS 2.24) — 초월스토리 확인 필요</dd>
    <dt>상품</dt><dd><b>289만 원 단일 프로젝트</b>가 유력 — 과거 사례에서 구성 차이가 전환율에 큰 영향이 없었음</dd>
    <dt>강사에게 제시한 수익</dt><dd>2,200만 ~ 3,200만 원</dd>
    <dt>역제안</dt><dd>초월스토리가 영입한 신규 강사의 역량이 부족하면, <b>최소 2개월 준비 기간</b>을 주면 프로그램 개발까지 지원</dd>
    <dt>강사 종료 기준</dt><dd>성과가 미흡하면 <b>2회 시도 후 협업 종료</b></dd>
  </dl>
</div>

<h2>런칭 계획 <small>5주 주기</small></h2>
<div class="card">
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">10월 말~11월 초</div><div class="t">촬영 시작</div><div class="d">출연자 1명 포함 촬영 기획안을 초월스토리가 전달</div></li>
    <li><div class="d">런칭 3주 전부터</div><div class="t">고연령 성과자·성과 수강생 영상 각 4편 업로드</div><div class="d">온드 채널만으로는 모자라서 신뢰도 높은 얼굴을 앞에 세우는 것</div></li>
    <li><div class="d">11~12월</div><div class="t">메타·구글 유료 광고 병행</div><div class="d">유튜브 라이브 시청자 400~600명 확보가 목표</div></li>
    <li class="big"><div class="d">12월 초</div><div class="t">라이브 — 정규 4회 + 보너스 1회</div><div class="d">전환율 10%로 30~40명 모집이 초기 목표</div></li>
  </ol>
  <div class="note">이와 별개로 <b>10/25 무료 라이브 특강</b>은 루크 자체 건으로 확정됐습니다 (4종 자판기 전체 사용법 + 저가 소싱 노하우, 고정 댓글 단톡방 입장자 전원에게 자동 등록 자판기 7일 무료 이용권).</div>
</div>

<h2>배분 구조 — 녹음으로 다시 맞췄습니다</h2>
<div class="card red">
  <p style="margin:0 0 10px">10/6 17:22 회의 녹음 48분, 발화 225개를 처음부터 끝까지 다시 확인했습니다. <b>루크님 말이 맞고, 제가 쓴 것 중 두 개가 틀렸습니다.</b></p>
  <ul class="list">
    <li><div class="t">맞은 것 — 8%는 선차감입니다</div><div class="m">초월스토리 발언 그대로: "<b>전체 매출의 PG 수수료만 제외하고 CRM이나 이런 운영비 다 포함 안하고 그냥 PG 수수료만 제외한 매출의 8%를 고정적으로 계속 드리는 거</b>". 비용을 빼기 전에 떼는 게 맞습니다. 제안한 쪽도 초월스토리입니다</div></li>
    <li><div class="t">틀린 것 ① — <b>광고비 8%는 회의에 없었습니다</b></div><div class="m">제가 '광고비 8%(추정)'로 한 줄을 더 뺐는데, 녹음에 그런 말이 없습니다. 실제 발언은 27:31의 "<b>그 정산표에 그러면 8%는 그냥 광고비로 넣는 게 좋을 것 같아요</b>" — 이건 <b>루크님 수수료를 장부에서 광고비 항목으로 계상하자</b>는 말입니다. 별개의 광고비가 아닙니다. <b>같은 8%를 제가 두 번 뺐습니다.</b> 광고비 실제 비율은 회의에서 한 번도 숫자로 나오지 않았습니다 — 다만 <b>강사 제시액에서 역산은 됩니다</b>(아래 '광고비 역산')</div></li>
    <li class="big"><div class="t">틀린 것 ② — <b>6:4는 이 녹음에 없습니다. 있을 이유도 없었습니다</b></div><div class="m">비율이 나오는 발언은 '5대5'와 '8%'뿐입니다. 10/8에 확인한 결과 <b>6:4는 루크님과 가을 대표님 사이의 별도 계약이고 초월스토리는 모르는 내용</b>이었습니다. 그래서 회의 녹음에 없는 게 당연합니다 — 제가 녹음에서 찾으려 한 것 자체가 번지수가 틀렸습니다</div></li>
  </ul>
  <div class="note"><b>'나는 2번 받는다'는 구조 자체는 성립합니다.</b> ① PG 제외 매출의 8% ② 가을 대표님 몫에서 다시 나누는 몫. 아래는 그 구조로 다시 계산한 것입니다.</div>
</div>

<h2>순서대로 쌓으면 이렇게 됩니다</h2>
<div class="card accent">
  <ol class="tl" style="margin-top:2px">
    <li><div class="t">매출에서 <b>PG 수수료</b>만 먼저 뺀다</div><div class="m">회의에서 PG 요율은 숫자로 나오지 않았습니다. 아래 표는 <b>3.5%로 가정</b>했습니다 — 실제 요율을 알려주시면 다시 계산합니다</div></li>
    <li><div class="t">그 금액의 <b>8%를 루크님이 먼저 가져간다</b></div><div class="m">여기까지는 비용과 무관하게 확정입니다. 인원이 적어도 줄기만 하고 사라지지 않습니다</div></li>
    <li><div class="t">남은 돈에서 <b>광고비와 나머지 비용</b>을 뺀다</div><div class="m">"다 차감하고"가 루크님 발언입니다. 항목 목록이 없는 게 지금 가장 큰 구멍입니다</div></li>
    <li><div class="t">남은 순수익을 <b>초월스토리 : 가을 대표님 = 5:5</b></div><div class="m">초월스토리 발언: "강사분이랑은 그러면 5대5로 하면 좋겠죠?"</div></li>
    <li class="big"><div class="t">가을 대표님 몫을 <b>루크님과 다시 6:4</b></div><div class="m">근거가 이 녹음에 없어서, 누가 6인지는 아래에서 양쪽 다 계산했습니다</div></li>
  </ol>
</div>

<h2>확정 — 가을 대표님이 6, 루크님이 4</h2>
<div class="card accent">
  <p style="margin:0 0 10px">10/8 확인: <b>기준점은 초월스토리가 가을 대표님께 제시할 약 2,200만</b>이고, <b>그 2,200만에서 루크님이 4</b>입니다. 어제 제가 역산으로 "가을 대표님이 6인 쪽이 맞다"고 쓴 것과 방향이 같습니다.</p>
  <div class="wrapx"><table>
  <tr><th>기준이 되는 가을 대표님 몫</th><th>루크 4</th><th>가을 6</th><th>루크 합계 (8% 892만 + 4)</th></tr>
  <tr><td><b>초월스토리 제시 하단 2,200만</b></td><td class="num"><b>880만</b></td><td class="num">1,320만</td><td class="num"><b>1,772만</b></td></tr>
  <tr><td>초월스토리 제시 상단 3,200만</td><td class="num">1,280만</td><td class="num">1,920만</td><td class="num">2,172만</td></tr>
  <tr><td>역산한 36명·광고 4,500만 기준 2,201만</td><td class="num">880만</td><td class="num">1,321만</td><td class="num">1,655만</td></tr>
  </table></div>
  <div class="note">2,200만은 초월스토리가 "1억 기준으로 생각해볼까요"라며 던진 하단값이고 <b>계산식은 회의에서 설명되지 않았습니다.</b> 그래서 거꾸로 풀었습니다 — 아래 '광고비 역산'에서 <b>그 2,200만이 광고비 약 4,500만을 전제로 한 숫자</b>라는 게 나옵니다. 역산값으로 다시 내려오면 5:5 몫이 2,201만, 루크님 4가 880만입니다. <b>세 줄 중 맨 아래가 지금 가장 현실에 가까운 줄입니다.</b></div>
</div>

<h2>초월스토리가 모르는 계약이라는 점 <small>10/8 확인</small></h2>
<div class="card red">
  <p style="margin:0 0 12px">6:4는 루크님과 가을 대표님 사이의 별도 계약이고 <b>초월스토리는 모른다</b>고 하셨습니다. 가을 대표님은 당사자니까 알고 서명합니다. 그러면 리스크는 한 곳에만 몰립니다 — <b>초월스토리가 나중에 알게 되는 경우</b>입니다. 판단은 루크님이 하실 일이고, 저는 어디서 드러나는지만 적어 둡니다.</p>
  <ul class="list">
    <li><div class="t">8%는 '소개 수수료'로 제안된 돈입니다</div><div class="m">녹음에서 초월스토리가 먼저 "<b>그러면 그 소개 수수료를 한 8% 혹시 한번 제안 드려</b>"라고 꺼냈습니다. 루크님을 <b>강사를 소개하는 사람</b>으로 보고 책정한 금액이라는 뜻입니다. 강사 몫의 40%를 또 받는 걸 알게 되면 8%의 전제가 흔들립니다</div></li>
    <li><div class="t">드러나는 경로는 정산 숫자입니다</div><div class="m">초월스토리는 가을 대표님께 2,200만을 드린다고 알고 있는데 실제 손에 남는 건 1,320만입니다. 초월스토리는 강사와 직접 소통합니다 — 단톡방·촬영·라이브. <b>약속한 금액이 지켜졌는지 묻는 대화 한 번이면 드러납니다</b></div></li>
    <li><div class="t">2회 종료 조건이 걸려 있습니다</div><div class="m">"성과가 미흡하면 2회 시도 후 협업 종료"가 이미 합의돼 있습니다. 성과 심사 시점과 겹치면 <b>종료의 명분이 하나 더 생깁니다</b></div></li>
    <li class="big"><div class="t">880만을 받는 서류가 남습니다</div><div class="m">가을 대표님이 받은 돈에서 루크님께 보내려면 가을 대표님은 전액을 소득으로 신고하고 880만을 비용으로 처리해야 합니다. 그러려면 <b>루크님이 세금계산서를 끊거나 원천징수가 들어갑니다.</b> 현금으로 받으면 법인 대표 개인의 미신고 소득이 됩니다 — <b>지금 KCB 622에 꼬마빌딩 대출을 앞둔 상황에서 가장 피해야 할 구간</b>입니다</div></li>
  </ul>
</div>

<h2>6:4는 '순수익의 20%'와 완전히 같은 금액입니다</h2>
<div class="card gold">
  <p style="margin:0 0 10px">계산을 정리하다 알았습니다. <b>가을 대표님 몫의 4를 받는 것은, 순수익의 20%를 받는 것과 수학적으로 똑같습니다.</b> 가을 대표님 몫이 순수익의 절반이니 그 40%는 0.5 × 0.4 = 0.2, 그대로 20%입니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th>루크 합계<br><small>36명·광고 4,500만 기준</small></th><th>초월스토리가 알고 있나</th></tr>
  <tr><td>숨긴 6:4</td><td class="num">1,655만</td><td>모름</td></tr>
  <tr><td>공개 — 순수익의 10% 추가</td><td class="num">1,214만</td><td>계약서에 있음</td></tr>
  <tr><td>공개 — 순수익의 15% 추가</td><td class="num">1,434만</td><td>계약서에 있음</td></tr>
  <tr><td><b>공개 — 순수익의 20% 추가</b></td><td class="num"><b>1,655만</b></td><td><b>계약서에 있음</b></td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>맨 위와 맨 아래가 같은 숫자입니다. 1원도 차이가 없습니다.</b> 그러면 숨기는 쪽을 택할 이유가 금액으로는 설명되지 않습니다. 남는 이유는 하나뿐입니다 — <b>'순수익의 20%를 달라'고 말했을 때 초월스토리가 거절할 것 같다</b>는 판단. 그건 협상의 문제이고, 거절당하면 그때 6:4로 돌아가도 됩니다. <b>순서를 바꾸는 것만으로 리스크가 사라집니다.</b></p>
  <div class="note">말할 근거도 이미 있습니다. 루크님이 하는 일이 섭외에서 끝나지 않습니다 — 강의 기획·PPT·라이브 코칭·프로그램 공유까지 다 하기로 돼 있고, <b>그건 소개자의 일이 아니라 공동 기획자의 일입니다.</b> 회의에서 결론이 안 난 다섯 가지 중 1번이 바로 '루크의 참여 범위 — 단순 플레이어인가, 공동 기획인가'이고, 10/22에 배분 초안을 만들기로 했습니다. <b>말을 꺼낼 자리가 이미 잡혀 있습니다.</b><br><br>그리고 가을 대표님은 원크루 크루원입니다. 이미 큰 돈을 낸 사람의 첫 강사 수익에서 또 40%를 가져가는 구조는 금액과 별개로 설명이 필요한 모양이 됩니다. 물론 기획·PPT·코칭을 전부 붙여 주는 대가이니 공짜가 아닙니다 — <b>그 대가를 가을 대표님도 같은 뜻으로 이해하고 있는지</b>만 서면으로 남겨 두시면 됩니다.</div>
</div>

<h2>광고비 역산 — 약 4,500만, 매출의 45%</h2>
<div class="card gold">
  <p style="margin:0 0 10px">2,200만을 물어보신 이유가 이거였다고 하셔서, 루크님 숫자(280만 × 36명 = 1억 80만, PG 4%)로 끝까지 풀었습니다.</p>
  <div class="wrapx"><table>
  <tr><td>매출 (280만 × 36명)</td><td class="num">1억 80만</td></tr>
  <tr><td>− PG 수수료 4%</td><td class="num">403만</td></tr>
  <tr><td>= PG 제외 매출</td><td class="num">9,677만</td></tr>
  <tr><td><b>− 루크 수수료 8%</b></td><td class="num"><b>774만</b></td></tr>
  <tr><td>= 비용 빼기 전 남은 돈</td><td class="num">8,903만</td></tr>
  <tr><td>− 강사 2,200만 + 채널 2,200만</td><td class="num">4,400만</td></tr>
  <tr><td><b>= 남는 자리 = 광고비</b></td><td class="num"><b>약 4,500만</b></td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>매출의 44.6%입니다. ROAS로 치면 2.24.</b> 1억을 벌기 위해 4,500만을 태운다는 뜻이고, 36명을 데려오는 데 1인당 125만 — 280만 상품에서 획득비가 <b>44.6%</b>입니다. 고가 라이브 퍼널에서 불가능한 숫자는 아니지만 <b>여유가 거의 없습니다.</b></p>
  <div class="note">검산도 맞습니다 — 광고비를 4,500만으로 두고 다시 내려오면 5:5 몫이 <b>2,201만</b>으로 나옵니다. 초월스토리가 말한 2,200만과 1만 원 차이입니다. <b>하단값 하나로 그쪽이 머릿속에 둔 광고 예산이 그대로 드러났습니다.</b></div>
</div>

<h2>광고비가 움직이면 누가 얼마나 흔들리나</h2>
<div class="card">
  <p style="margin:0 0 10px">36명을 고정하고 광고비만 바꿔봤습니다. 초월스토리 가정은 4,500만 줄입니다.</p>
  <div class="wrapx"><table>
  <tr><th>광고비</th><th>5:5 몫<br><small>초월이 말하는 금액</small></th><th>루크 4</th><th>가을 실수령<br><small>6:4 후</small></th><th>루크 합계<br><small>8% + 4</small></th></tr>
  <tr><td>3,000만</td><td class="num">2,951만</td><td class="num">1,181만</td><td class="num">1,771만</td><td class="num">1,955만</td></tr>
  <tr><td>4,000만</td><td class="num">2,451만</td><td class="num">981만</td><td class="num">1,471만</td><td class="num">1,755만</td></tr>
  <tr><td><b>4,500만 (초월 가정)</b></td><td class="num"><b>2,201만</b></td><td class="num"><b>880만</b></td><td class="num"><b>1,321만</b></td><td class="num"><b>1,655만</b></td></tr>
  <tr><td>5,000만</td><td class="num">1,951만</td><td class="num">781만</td><td class="num">1,171만</td><td class="num">1,555만</td></tr>
  <tr><td>5,500만</td><td class="num">1,701만</td><td class="num">681만</td><td class="num">1,021만</td><td class="num">1,455만</td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>광고비가 1,000만 더 나가면 이렇게 나눠집니다.</b></p>
  <div class="wrapx"><table>
  <tr><th></th><th>부담</th><th>비율</th><th>광고 집행 권한</th></tr>
  <tr><td>초월스토리</td><td class="num">−500만</td><td class="num">50%</td><td>있음</td></tr>
  <tr><td><b>가을 대표님</b></td><td class="num"><b>−300만</b></td><td class="num"><b>30%</b></td><td><b>없음</b></td></tr>
  <tr><td>루크님</td><td class="num">−200만</td><td class="num">20%</td><td>없음</td></tr>
  </table></div>
  <div class="note"><b>루크님 자리는 구조적으로 단단합니다.</b> 8% 774만은 광고비가 어떻게 되든 그대로 들어옵니다. 광고비에 노출된 건 4를 받는 부분뿐이라 <b>전체 리스크의 20%만 지십니다.</b> 반대로 <b>가을 대표님은 30%를 지는데 광고에 아무 권한이 없습니다.</b> 이건 미리 말해 두셔야 할 부분입니다.</div>
</div>

<h2>손익분기 18명 — 이게 이 구조의 급소입니다</h2>
<div class="card red">
  <p style="margin:0 0 10px">광고비 4,500만을 먼저 태우고 나서 나눕니다. 그래서 인원이 줄 때 <b>누가 먼저 0이 되는지가 순서로 정해져 있습니다.</b></p>
  <div class="wrapx"><table>
  <tr><th>인원</th><th>매출</th><th>순수익</th><th>5:5 몫</th><th>가을 실수령</th><th>루크 합계</th></tr>
  <tr><td>36명</td><td class="num">1억 80만</td><td class="num">4,403만</td><td class="num">2,201만</td><td class="num">1,321만</td><td class="num">1,655만</td></tr>
  <tr><td>30명</td><td class="num">8,400만</td><td class="num">2,919만</td><td class="num">1,459만</td><td class="num">876만</td><td class="num">1,229만</td></tr>
  <tr><td>24명</td><td class="num">6,720만</td><td class="num">1,435만</td><td class="num">718만</td><td class="num">431만</td><td class="num">803만</td></tr>
  <tr><td><b>18명</b></td><td class="num">5,040만</td><td class="num"><b>0원</b></td><td class="num"><b>0원</b></td><td class="num"><b>0원</b></td><td class="num"><b>387만</b></td></tr>
  <tr><td>12명</td><td class="num">3,360만</td><td class="num">−1,532만</td><td class="num">적자</td><td class="num">0원</td><td class="num">258만</td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>손익분기가 18명입니다.</b> 그 아래로는 강사도 채널도 0원이고 <b>루크님만 8%를 받습니다.</b> 그런데 같은 회의에서 루크님이 "얘는 진짜 3% 전환율만 하더라도"라고 하셨고, 과거 기록(DB 3,000개 → 라이브 유입 18~20% → 전환 3%)으로 계산하면 <b>16~18명</b> — <b>정확히 손익분기 지점</b>입니다.</p>
  <div class="note"><b>초월스토리의 2,200만은 전환율 10%가 그대로 맞았을 때의 숫자이고, 과거 실적대로 가면 0원입니다. 가운데가 거의 없습니다.</b> 24명이어도 가을 대표님 실수령은 431만입니다. 이 구조에서 가장 큰 변수는 인원 자체가 아니라 <b>광고비를 먼저 태운다는 순서</b>입니다 — 광고비가 뒤에 있으면 손실을 나눠 지지만, 앞에 있으면 광고비가 다 채워진 뒤에야 사람 몫이 생깁니다.</div>
</div>

<h2>그래서 물어볼 것과 말할 것</h2>
<div class="card accent">
  <p style="margin:0 0 10px"><b>초월스토리에</b></p>
  <ul class="list">
    <li><div class="t">광고비 4,500만이 맞나 — 본인 입으로 확인</div><div class="m">역산한 값이니 확인이 필요합니다. "2,200만이면 광고를 4,500만 정도 보시는 거죠?" 한 줄로 끝납니다</div></li>
    <li><div class="t">광고비 상한을 정할 수 있나</div><div class="m">상한이 없으면 가을 대표님과 루크님 몫이 집행하는 쪽 판단에 그대로 노출됩니다. <b>상한선 한 줄이 정산 열람권보다 실질적입니다</b></div></li>
    <li><div class="t">ROAS가 2.24 아래로 떨어지면 멈추는 기준이 있나</div><div class="m">지금은 '2회 후 종료'만 있고 <b>한 회차 안에서 멈추는 기준이 없습니다.</b> 그 안에서 광고비가 다 타면 아무도 못 받습니다</div></li>
    <li class="big"><div class="t">이 예산을 전환율 10%로 짰나, 과거 3%로 짰나</div><div class="m">10%로 짰다면 4,500만은 낙관 가정 위에 세운 예산입니다. 3%였다면 애초에 이 예산이 나올 수 없습니다 — <b>어느 쪽이냐가 가을 대표님께 할 말을 결정합니다</b></div></li>
  </ul>
  <p style="margin:14px 0 10px"><b>가을 대표님께</b></p>
  <ul class="list">
    <li><div class="t">2,200만은 전환율 10%가 맞았을 때의 숫자</div><div class="m">36명이면 2,201만, 18명이면 0원입니다. 중간이 거의 없습니다</div></li>
    <li class="big"><div class="t">광고비 리스크의 30%를 지는데 권한이 없다</div><div class="m">0원이 나온 뒤에 설명하는 것보다 지금 말하는 게 훨씬 쉽습니다. 그 자리에서 <b>루크님은 8%로 보호받고 가을 대표님은 안 그렇다는 사실</b>도 같이 드러나니, 먼저 꺼내시는 편이 낫습니다</div></li>
  </ul>
  <div class="note"><b>바닥을 깔아 두는 방법이 있습니다 — 최소 보장액.</b> 인원과 무관하게 강사에게 500만을 보장하고 그 이상은 5:5로 가는 식입니다. 광고 집행 권한이 초월스토리에 있으니 <b>바닥을 깔 책임도 그쪽에 있다</b>고 말할 근거가 됩니다. 가을 대표님이 첫 강사이고 성과자 영상 4편까지 겸하기로 돼 있으니 요구할 명분은 충분합니다. 이게 들어가면 6:4를 공개로 돌리기도 쉬워집니다 — <b>루크님이 가을 대표님 쪽 바닥을 받아내 준 사람이 되니까요.</b></div>
</div>

<h2>그래서 10/22 전에 닫을 다섯 칸</h2>
<div class="card">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">2,200만의 계산식 — 비용을 무엇으로 5,600만 잡았는지</div><div class="m">여기가 루크님 4의 크기를 결정합니다. 비용 가정이 과했다면 880만이 1,590만이 됩니다</div></li>
    <li><span class="tag p0">2</span><div class="t">8%를 초월스토리 비용으로 부담하는지 — 446만</div><div class="m">계약서 한 줄. 지금 '그렇게 해주셔도 됩니다'로 열려 있습니다</div></li>
    <li><span class="tag p0">3</span><div class="t">'다 차감'의 항목 목록</div><div class="m">광고비·PG·PD 인건비·제작비·CRM 중 무엇이 들어가고 누가 부담하는가. 5:5는 비율이고 <b>분모를 정하는 것이 실제 계약</b>입니다</div></li>
    <li><span class="tag p0">4</span><div class="t">광고비 상한과 중단 기준 — 역산값 4,500만</div><div class="m">이게 없으면 위 표의 어느 줄에 앉게 될지를 집행하는 쪽이 정합니다. <b>가을 대표님 최소 보장액도 여기서 같이</b></div></li>
    <li class="big"><span class="tag p0">5</span><div class="t">6:4를 숨길지, 공동 기획으로 공개할지</div><div class="m">금액 차이는 작고 리스크 차이는 큽니다. 10/22가 공개로 돌릴 수 있는 마지막 자리입니다 — 그 자리를 지나 계약서가 나오면 되돌리기 어렵습니다</div></li>
  </ul>
</div>

<h2>결론이 안 난 다섯 가지</h2>
<div class="card gold">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">루크의 참여 범위 — 단순 플레이어인가, 공동 기획인가</div><div class="m">여기에 따라 수익 배분이 달라집니다. 10/22·10/29에 옵션 정리와 배분 초안을 만들기로 했습니다</div></li>
    <li><span class="tag p0">2</span><div class="t">상품 최종 확정</div><div class="m">289만 단일로 갈지, 1:1 컨설팅반을 넣을지, 목표 객단가는 얼마인지</div></li>
    <li><span class="tag done">3</span><div class="t">파일럿 강사 — <b>가을(정복녀) 대표님으로 정해졌습니다</b></div><div class="m">10/7 기준으로 가을 대표님이 초월스토리와 함께 <b>강의 기획에 들어갔습니다.</b> 후보 비교는 <a href="../pilot/">파일럿 강사 결정</a>에 남겨 두었습니다. 남은 것은 사람 고르기가 아니라 <b>성과 숫자 확보와 11~12월 일정 확정</b>(기한 10/11)입니다</div></li>
    <li><span class="tag p1">4</span><div class="t">운영 부담</div><div class="m">강사가 늘면 단톡방·커뮤니케이션이 같이 늘어납니다. PD 위임 기준과 강사에게 기획 의도를 전달하는 방식을 정해야 합니다</div></li>
    <li><span class="tag p1">5</span><div class="t">퍼널이 안 먹힐 때의 대비가 없다</div><div class="m">전환율이 떨어졌을 때 쓸 대체 퍼널·A/B 로드맵이 비어 있습니다</div></li>
  </ul>
</div>

<h2>날짜가 잡힌 것</h2>
<div class="card wrapx">
<table>
<tr><th>날짜</th><th>할 일</th><th>누가</th></tr>
<tr><td>10/17</td><td>채널별 리드 소스 태깅 · UTM 표준화</td><td>초월스토리</td></tr>
<tr><td>10/19·10/25</td><td>PD 역할·권한 정의와 위임 기준</td><td>초월스토리</td></tr>
<tr><td>10/20</td><td>5주 런칭 캘린더 + 정규 4회·보너스 1회 편성표</td><td>초월스토리</td></tr>
<tr><td>10/20</td><td>라이브 단계별(등록→참여→체류→구매) 지표 정의·리포트 템플릿</td><td>초월스토리</td></tr>
<tr><td>10/21·10/23</td><td>단톡방 운영 프로토콜 · 파일럿 2회 성과 기준과 종료 조건 문서화</td><td>초월스토리</td></tr>
<tr><td>10/22·10/29</td><td><b>협업 모델 옵션(플레이어 vs 공동 빌드업) + 수익 배분 초안</b></td><td>루크·초월스토리</td></tr>
<tr><td>10/24</td><td>메타·구글애즈 캠페인 설계 + 라이브 모객 400~600명 KPI</td><td>초월스토리</td></tr>
<tr><td>10월 말~11월 초</td><td>출연자 1명 포함 촬영 기획안 전달</td><td>초월스토리</td></tr>
<tr><td>11월 초</td><td>첫 촬영 <span class="tag">담당 미지정</span></td><td>—</td></tr>
<tr><td>11/8</td><td>라이브 시청자 코호트(400/600/1000명)별 전환율 비교</td><td>초월스토리</td></tr>
<tr><td>12월 초</td><td>라이브 방송 <span class="tag">잠정</span></td><td>—</td></tr>
<tr><td>상시</td><td>적합한 강사 소개 · 강의 기획 · PPT · 라이브 코칭 지원</td><td>루크</td></tr>
<tr><td>상시</td><td>유튜브·라이브 출연 성과자 섭외 (불가 시 초월스토리가 별도 준비)</td><td>루크</td></tr>
</table>
</div>

<h2>이게 왜 중요한가</h2>
<div class="card blue">
  <ul class="list">
    <li><div class="t">인베이더가 하던 역할이 초월스토리로 넘어가는 그림</div><div class="m">기수를 돌리고 사람을 모아주던 자리입니다. 다만 조건이 다릅니다 — 인베이더는 수취율 20%였고, 여기서는 루크가 <b>받는</b> 쪽(8%)에 더해 강사 5:5까지 들어갑니다</div></li>
    <li><div class="t">루크의 자리가 '강사'에서 '강사를 공급하는 사람'으로 바뀐다</div><div class="m">직접 가르치는 대신 강사를 소개하고 기획·PPT·코칭을 붙여 수수료를 받는 구조. 시간을 덜 쓰고 반복 가능하다는 점에서 <a href="../philosophy/">원크루에서 가르치는 구조</a>를 본인에게 적용하는 것이기도 합니다</div></li>
    <li><div class="t">10/25 무료 라이브가 이 계획의 리허설이 된다</div><div class="m">유튜브 라이브 → 단톡방 → 무료 이용권 동선을 12월 런칭 전에 한 번 돌려보는 자리입니다. 여기서 나온 유입률·단톡방 반응이 400~600명 목표의 근거가 됩니다</div></li>
    <li><div class="t">그래도 11~12월 건이다</div><div class="m">촬영 11월, 라이브 12월. <b>10~11월 현금은 여전히 원크루 전환과 마지막 기수</b>에서 나옵니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: 10/6 17:22 메이븐·초월스토리 회의 녹음 — <b>2026-10-08에 48분 전사 225개 발화 전체를 재확인</b>했습니다. 확정 인용: 8% 기준은 "전체 매출의 PG 수수료만 제외하고 CRM이나 이런 운영비 다 포함 안하고 그냥 PG 수수료만 제외한 매출의 8%"(초월스토리 제안, 05:49·06:02) · "그 정산표에 그러면 8%는 그냥 광고비로 넣는 게 좋을 것 같아요"(초월스토리, 27:31)와 이에 대한 루크 "그렇게 해주셔도 됩니다"(27:43) · "강사분이랑은 그러면 5대5로 하면 좋겠죠?"(초월스토리, 27:24) · "1억 기준으로 생각해볼까요… 2,200, 3200 정도 편차 될 것 같습니다 / 3200 너무 높게 잡은 것 같긴 한데"(초월스토리, 40:28~42:20) · "전환율을 10% 기준으로 잡아도 될까요… 최소한 30명에서 40명은 나오고"(초월스토리, 28:16) · "얘는 진짜 3% 전환율만 하더라도"(루크, 24:14) · "네 프로젝트 289만원으로 해야 될 것 같긴 해요… 단일 프로젝트로 가도 될 것 같긴 해요"(초월스토리, 41:56). <b>녹음에 없는 것</b>: 광고비 비율, PG 요율, '6대4'라는 표현(같은 날 16:30 촬영 녹음 42분·15:00 신정현 녹음에도 없음). 6:4는 2026-10-08 루크 구두가 출처입니다 — <b>가을 대표님 6 : 루크 4</b>, 기준은 가을 대표님 몫 약 2,200만이며 <b>루크님과 가을 대표님 사이의 별도 계약으로 초월스토리는 모르는 내용</b>입니다. 2,200만의 산출 근거는 초월스토리가 회의에서 설명하지 않았습니다. 위 표의 금액은 2026-10-08 루크가 제시한 가정(280만·36명·PG 4%)으로 클로드가 계산한 <b>계획값이며 실적이 아닙니다.</b> 광고비 약 4,500만은 초월스토리의 강사 제시액 2,200만에서 역산한 값으로 <b>초월스토리가 확인한 숫자가 아닙니다.</b> 계약 조건은 구두 합의 단계이며 문서화 전입니다. 표의 계산은 회의에 나온 수치(289만 · 8% · 5:5 · 30~40명)를 그대로 넣어 클로드가 맞춰본 것으로, 비용 항목이 확정되지 않아 실제와 다를 수 있습니다. 계약 조건은 구두 합의 단계이며 문서화 전입니다.</div>
"""

# ---------------------------------------------------------------- 파일럿 강사 결정
PILOT = """
<h1>파일럿 강사 — 누구로 갈 것인가</h1>
<div class="card accent" style="margin-bottom:14px"><p style="margin:0"><span class="tag done">결정</span> <b>10/7 — 가을(정복녀) 대표님으로 정해졌습니다.</b> 초월스토리와 함께 강의 기획에 들어갔습니다. 아래 비교는 왜 이 결정이 맞는지의 근거로 남겨 둡니다. 다음 할 일은 <b>성과 숫자 확보와 11~12월 일정 확인</b>(기한 10/11), 그리고 <a href="../chowol/">40명 기준 수익 배분</a> 정리입니다.</p></div>
<p class="note">후보는 두 분이었습니다 — <b>가을(정복녀) 대표님</b>(40대 주부·원크루) 또는 <b>뿌요(최근영)</b>(30대 중후반). <a href="../chowol/">초월스토리 협업</a>에서 결론이 안 난 다섯 가지 중 3번이고, <b>12월 초 라이브를 지키려면 가장 먼저 닫아야 하는 칸</b>입니다. 11월 초에 촬영이 들어가야 하니 실제로 남은 시간은 3주입니다.</p>

<h2>먼저, 이 자리가 요구하는 것 <small>회의에서 나온 조건 그대로</small></h2>
<div class="card accent">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">289만 원을 파는 얼굴</div><div class="m">단일 고가 상품입니다. 기능 설명이 아니라 <b>"저 사람처럼 되고 싶다"</b>가 전환을 만듭니다</div></li>
    <li><span class="tag p0">2</span><div class="t">초월스토리가 요청한 것은 '고연령 성과자'</div><div class="m">런칭 3주 전부터 고연령 성과자 영상 4편 + 성과 수강생 영상 4편. 타깃이 50~60대 비중이 높은 초보층이라 그렇습니다</div></li>
    <li><span class="tag p0">3</span><div class="t">11월 초 촬영 · 12월 초 라이브 4+1회</div><div class="m">촬영일·라이브 5회를 비울 수 있는 사람이어야 합니다. 주말 포함</div></li>
    <li><span class="tag p1">4</span><div class="t">콘텐츠를 혼자 만들 필요는 없다</div><div class="m">강의 기획·PPT·라이브 코칭은 루크가 붙입니다. 필요한 건 제작 능력보다 <b>서사와 카메라 앞에서의 신뢰</b></div></li>
    <li><span class="tag p1">5</span><div class="t">2회 시도 후 종료 조건이 붙은 자리</div><div class="m">성과가 미흡하면 협업을 종료합니다. 강사 본인에게도 리스크가 있는 자리라는 뜻입니다</div></li>
    <li><span class="tag p1">6</span><div class="t">보상은 2,200만~3,200만 (계산상 3,641만~4,855만)</div><div class="m">적은 돈이 아닙니다. 제안을 받는 쪽 입장에서도 <b>인생 계획이 흔들리는 금액</b>이라는 걸 전제해야 합니다</div></li>
  </ul>
</div>

<h2>두 분을 같은 기준에 올려보면</h2>
<div class="card wrapx">
<table>
<tr><th>기준</th><th>가을(정복녀) 대표님</th><th>뿌요 (최근영)</th></tr>
<tr><td>나이·배경</td><td>40대 · 주부 → 대표</td><td>30대 중후반</td></tr>
<tr><td>타깃(50~60대 초보)과의 거리</td><td><b>가깝다</b> — 주부에서 시작한 서사</td><td>멀다 — 세대가 한 칸 아래</td></tr>
<tr><td>루크와의 관계</td><td>원크루 수강생(고객)</td><td>조직 안의 실무자 (교육실장·3PL 운영)</td></tr>
<tr><td>성과 숫자 기록</td><td><span class="tag">기록에 없음</span></td><td>현재 수익 월 400만 미만 (9/11 상담)</td></tr>
<tr><td>성과의 출처</td><td>본인 사업 <span class="tag">확인 필요</span></td><td>상당 부분이 <b>루크 쪽 용역·코칭 보수</b></td></tr>
<tr><td>가르친 경험</td><td><span class="tag">기록에 없음</span></td><td>1:1 코칭·컨설팅 일 6건 수행 중 (강단 강의 이력은 없음)</td></tr>
<tr><td>카메라·채널</td><td><span class="tag">기록에 없음</span></td><td>짠테크 유튜브 제작 중 (1~3화, 루크가 대본)</td></tr>
<tr><td>11~12월 가용 시간</td><td><span class="tag">확인 필요</span></td><td><b>이미 꽉 차 있음</b> — 오전 스토어 3시간 + 코칭 10~12건 목표 + 발주 + 물류 안정화</td></tr>
<tr><td>본인 의향</td><td><span class="tag">확인 필요</span></td><td><b>강사 준비를 미루기로 함</b> — 단기 수입 확보 우선 (9/11 상담)</td></tr>
<tr><td>12월에 걸려 있는 것</td><td>없음</td><td><b>12/10 90일 결산 — 거취 결정</b></td></tr>
</table>
<div class="note">가을님 칸이 비어 있는 건 적합하지 않다는 뜻이 아니라, <b>아직 확인한 기록이 없다</b>는 뜻입니다. 플라우드에는 8/15 이후 가을·정복녀 이름의 녹음이 없습니다.</div>
</div>

<h2>가을 대표님 — 역할과 모양이 맞습니다</h2>
<div class="card blue">
  <ul class="list">
    <li><div class="t">주부 → 대표라는 서사 자체가 상품이다</div><div class="m">50~60대 초보에게 가장 세게 작동하는 문장은 숫자가 아니라 <b>"나와 비슷한 사람이 해냈다"</b>입니다. 289만 원짜리 결정을 움직이는 건 이쪽입니다</div></li>
    <li><div class="t">초월스토리가 요청한 '성과 수강생' 요건을 본인이 충족한다</div><div class="m">영상 4편을 따로 섭외할 필요 없이 강사가 그 역할을 겸합니다 — 촬영 리소스가 한 번에 줄어듭니다</div></li>
    <li><div class="t">원크루를 통과했으니 커리큘럼 언어를 이미 공유한다</div><div class="m">루크가 강의 기획·PPT·라이브 코칭을 붙이는 구조에서, 같은 말을 쓰는 사람과 붙는 게 3주 안에 가능한 유일한 조건입니다</div></li>
    <li><div class="t">성과의 출처가 본인 사업이다</div><div class="m">"이 방법으로 이렇게 됐다"가 성립합니다. 조직 내부에서 받은 보수가 성과로 보이면 라이브에서 가장 먼저 무너지는 지점이 이쪽입니다</div></li>
  </ul>
  <div class="note">다만 <b>확인된 성과 숫자가 아직 없습니다.</b> 아래 '확인 필요'를 채우기 전까지는 후보이지 확정이 아닙니다.</div>
</div>

<h2>뿌요 — 지금 올리면 네 가지가 걸립니다</h2>
<div class="card red">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">본인이 강사를 미루겠다고 말했다</div><div class="m">9/11 상담에서 <b>"장기 목표인 강사 준비는 잠시 미루고 단기 수입 확보에 집중"</b>으로 정리했습니다. 의향이 반대 방향인 사람을 2회 실패 시 종료 조건이 붙은 자리에 세우는 건 순서가 뒤집힌 것입니다</div></li>
    <li><span class="tag p0">2</span><div class="t">12/10 거취 결정이 12월 초 라이브와 겹친다</div><div class="m">90일 결산으로 300만 달성 여부와 거취를 정하는 날입니다. <b>거취가 안 정해진 사람을 12월 상품의 얼굴로 세우면, 결산이 나쁘게 나올 때 상품까지 같이 흔들립니다</b></div></li>
    <li><span class="tag p0">3</span><div class="t">시간이 이미 없다</div><div class="m">오전 9~12시 스토어 운영 + 코칭 일 10~12건 목표 + 금요일 발주 + 3PL 물류 안정화. 번아웃 관리가 이미 과제로 올라와 있는 상태에서 촬영·라이브 5회를 얹는 것입니다. <b>강사를 올리면 상담·물류 자리가 빕니다</b></div></li>
    <li><span class="tag p1">4</span><div class="t">서사가 타깃과 어긋난다</div><div class="m">30대 중후반이고, 만들고 있는 채널은 <b>짠테크(절약)</b>입니다. 셀러 교육 타깃과 다른 결이라 자산으로 합산되지 않습니다. 또 본인이 자기 홍보 성격의 업무에 거부감이 있다고 말한 기록이 있어 라이브 판매석과 상성이 좋지 않습니다</div></li>
  </ul>
  <div class="note">뿌요가 부족하다는 뜻이 아닙니다. 코칭을 실제로 하루 6건 돌리는 사람은 흔하지 않고, 그건 <b>다른 자리의 강점</b>입니다 — 아래를 보세요.</div>
</div>

<h2>그래서 — 둘 중 하나를 고르는 문제가 아닙니다</h2>
<div class="card gold">
  <p style="margin:0 0 10px">이 런칭에는 자리가 두 개 있습니다. 같은 사람에게 둘을 다 맡기려다 선택이 막힌 것일 수 있습니다.</p>
  <div class="wrapx"><table>
  <tr><th>자리</th><th>필요한 것</th><th>맞는 사람</th></tr>
  <tr><td><b>앞</b> — 라이브에서 289만을 파는 강사</td><td>서사 · 권위 · 카메라 신뢰 · 타깃과의 거리</td><td class="num">가을 대표님</td></tr>
  <tr><td><b>뒤</b> — 들어온 30~40명을 받는 상담·운영</td><td>세션 표준화 · 응대 톤 · 처리량</td><td class="num">뿌요 (이미 하는 일)</td></tr>
  </table></div>
  <p class="note" style="margin-top:10px">뿌요를 앞으로 올리면 뒤가 비고, 그 자리를 또 채워야 합니다. 반대로 가을님을 앞에 세우면 <b>두 사람이 각자 잘하는 자리에 그대로 있습니다.</b> 2회 종료 조건이 붙은 자리에 조직 내부 인력을 올리지 않는 것도 리스크 관리로 맞습니다 — 실패하면 강사 한 명이 아니라 운영 인력까지 같이 잃습니다.</p>
</div>

<h2>권고 <small>조건부</small></h2>
<div class="card accent">
  <p style="font-size:17px;font-family:'Gowun Dodum',sans-serif;margin:0 0 8px"><b>가을 대표님으로 가되, 아래 네 가지를 확인한 다음에 확정하세요.</b></p>
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">이번 주</div><div class="t">성과 숫자를 받는다</div><div class="d">월 매출·순수익·시작 시점·판매 품목. 라이브에서 쓸 수 있는 숫자가 하나라도 나와야 강사가 성립합니다. 없으면 후보에서 내려야 합니다</div></li>
    <li><div class="d">이번 주</div><div class="t">본인 의향과 11~12월 일정을 확인한다</div><div class="d">촬영 1일 + 라이브 5회(주말 포함)를 비울 수 있는지. 주부시라면 가족 일정이 실제 제약입니다 — 금액보다 이걸 먼저 묻는 게 맞습니다</div></li>
    <li><div class="d">이번 주</div><div class="t">카메라 앞에 한 번 세워본다</div><div class="d">10/25 무료 라이브가 리허설입니다. 게스트로 10분만 붙여보면 3주 뒤 촬영에서 알게 될 것을 지금 알 수 있습니다</div></li>
    <li class="big"><div class="d">계약 전</div><div class="t">실패했을 때 원크루 관계는 분리한다</div><div class="d">본인의 고객을 2회 종료 조건이 붙은 자리에 세우는 것입니다. <b>"강사 협업이 끝나도 원크루 관계는 그대로"</b>를 먼저 말로 못 박아야 합니다. 이걸 안 하면 실패 시 수강생 한 명과 평판을 같이 잃습니다</div></li>
  </ol>
</div>

<h2>같이 짚어야 할 것</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">40대는 초월스토리가 말한 '고연령'이 아닐 수 있다</div><div class="m">타깃이 50~60대라면 고연령 성과자 영상 4편은 <b>별도로</b> 필요합니다. 원크루에 박태경·최은봉 대표님이 있지만 연령은 기록에 없습니다 — 강사와 별개로 영상 출연자 명단을 따로 만드는 게 맞습니다</li>
    <li><div class="t">강사에게 제시할 금액을 먼저 확정하라</div><div class="m">제시값 2,200만~3,200만과 계산값 3,641만~4,855만이 1,400~1,600만 차이 납니다 (<a href="../chowol/">근거</a>). <b>비용 항목 목록을 못 박기 전에 사람에게 숫자를 말하면 안 됩니다</b> — 나중에 내리는 건 불가능합니다</div></li>
    <li><div class="t">2개월 준비 기간 옵션을 쓸 수 있다</div><div class="m">회의에서 "역량이 부족하면 최소 2개월 준비 기간을 주면 프로그램 개발까지 지원"하기로 했습니다. 가을님이 숫자는 좋은데 전달이 약하다면, <b>12월을 밀고 2개월 붙이는 선택</b>이 열려 있습니다. 12월 날짜를 지키려고 사람을 억지로 맞출 필요는 없습니다</div></li>
    <li><div class="t">뿌요 거취 결정은 이것과 별개로 이번 주에 닫아야 한다</div><div class="m">강사로 안 가더라도 역할·수익 구조는 여전히 미결입니다 (<a href="../maven/">10/6 회의</a>). 12/10 결산 전에 정리해 두면 그날 선택지가 넓어집니다</div></li>
  </ul>
</div>

<h2>확인 필요 <small>가을 대표님 — 기록이 비어 있는 칸</small></h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">성함 표기</div><div class="m">'가을'이 활동명인지, '정복녀'가 본명인지. 영상·포스터·계약서에 들어갈 표기를 먼저 정해야 합니다</div></li>
    <li><div class="t">원크루 진행 상황</div><div class="m">몇 회차까지 왔는지, 상담 기록이 어디에 있는지. 플라우드에 8/15 이후 녹음이 없습니다</div></li>
    <li><div class="t">사업 내용과 성과</div><div class="m">업종·품목·시작 시점·월 매출·순수익. '대표님'의 사업체 형태(개인/법인)도</div></li>
    <li><div class="t">말하는 사람인지</div><div class="m">강의·발표·라이브·영상 경험. 없어도 되지만 그러면 준비 기간이 필요합니다</div></li>
    <li><div class="t">보유 채널</div><div class="m">유튜브·인스타·블로그 유무와 규모. 있으면 런칭 퍼널에 그대로 더해집니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: 10/6 17:22 메이븐·초월스토리 회의 녹음(강사 조건·2회 종료·2개월 준비·고연령 성과자 영상 4편) · 9/11 상담 녹음 최근영(뿌요) 63분(월 400만 미만·시급 2만·코칭 일 6건→10~12건·강사 준비 보류·오전 9~12시 스토어·자기 홍보 거부감) · 9/17 [뿌요] 운영 최적화 노트(교육실장 직함·컨설팅 40분 표준) · 프로젝트 일정표(12/10 뿌요 90일 결산·거취 결정, 짠테크 유튜브 1~3화). <b>가을(정복녀) 대표님에 관한 내용은 10/7 루크 구두 2줄(40대 주부·원크루 대표)이 전부이며, 플라우드 2026-08-15 이후 녹음·기존 페이지에서 해당 이름을 찾지 못했습니다.</b> 위 '맞는 이유'는 그 두 줄에서 도출한 판단이며 확인된 사실이 아닙니다.</div>
"""

# ---------------------------------------------------------------- 법인 사업장 이전 신고
RELOCATION = """
<h1>10/15 등기 — 등기부 확인 끝</h1>
<p class="note">2026-10-07 열람한 등기사항전부증명서(말소사항 포함) 기준으로 다시 썼습니다. 추측이 아니라 <b>등기부에 적힌 그대로</b>입니다. 전략 판단은 <a href="../corp/">힐링디어스 → 셀러들의 수다</a>에 있습니다.</p>
<div class="card gold" style="margin-bottom:14px"><p style="margin:0"><b>기한이 10/16(금)으로 하루 늦춰졌습니다.</b> 이 페이지는 이전일을 10/1로 보고 10/15라고 적었는데, 사무실 시설사용 계약서의 계약기간이 <b>2026년 10월 2일</b>부터였습니다. 그래서 상법 제182조 2주 기한은 <b>10월 16일(금)</b>입니다. 아래 10/15 표기는 전부 10/16으로 읽으세요. 서류는 <a href="../registry-forms/"><b>등기 서류 — 다 만들어 뒀습니다</b></a>에 완성본이 있고, 법무사 대신 셀프로 가도 되게 7장 전부 작성해 뒀습니다.</p></div>

<h2>10/7 구리세무서 문자 — 거부가 아니라 순서입니다</h2>
<div class="card red">
  <p style="margin:0 0 10px">구리세무서 재산법인세과에서 <b>사업장 이전 신고가 취하될 예정</b>이라는 문자가 왔습니다. 사유는 <b>"법인등기상 사업장 소재지와 이전된 소재지 상이"</b>입니다.</p>
  <p style="margin:0 0 10px">신고가 잘못된 게 아니라 <b>순서가 뒤바뀐 것</b>입니다. 법인은 등기부상 본점이 기준이라, 등기를 안 고친 채로 세무서에 새 주소를 내면 두 주소가 안 맞아서 받아주지 않습니다. 등기부상 본점은 아직 <b>갈매순환로 188 스칸센</b>으로 돼 있습니다.</p>
  <p style="margin:0"><b>순서는 등기 → 등기사항전부증명서 발급 → 사업자등록 정정 재신청입니다.</b> 등기만 끝내면 자동으로 풀립니다. 사업자등록 정정에는 법정 기한이 없으니 취하돼도 과태료는 없습니다.</p>
  <div class="note">덕분에 확인된 것 하나 — <b>세무서에 이미 새 주소를 내셨다는 건 주소가 정해졌다는 뜻</b>입니다. 등기도 <b>세무서에 낸 그 주소 그대로</b> 넣으셔야 합니다. 다르면 같은 사유로 또 반려됩니다.</div>
</div>

<h2>순서 재확인 — 등기가 먼저가 맞습니다</h2>
<div class="card blue">
  <p style="margin:0 0 10px">10/7에 따로 확인했습니다. 두 곳의 안내가 같은 순서를 말합니다.</p>
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">이사 결정서 (이사 1명이라 이사회 불요)</div></li>
    <li><div class="t">본점이전등기 신청 + 등록면허세 납부</div></li>
    <li><div class="t">등기 완료 후 <b>변경된 등기사항전부증명서 발급</b></div></li>
    <li class="big"><div class="t">그 증명서를 첨부해 사업자등록 정정 신고</div></li>
  </ol>
  <p style="margin:12px 0 0"><b>이유는 서류 하나입니다.</b> 법인의 사업자등록 정정에는 <b>변경된 법인등기부등본이 필수 첨부</b>입니다. 그 서류는 등기가 끝나야 나옵니다. 그래서 등기를 건너뛰고 세무서에 먼저 가면 낼 서류가 없고, 등기부 주소와 신고 주소가 달라 10/7에 받으신 것 같은 사유로 막힙니다.</p>
  <div class="note">참고로 같은 구리시 안이면 <b>관내이전</b>이라 정관 변경이 필요 없고 등기소도 한 곳입니다. 관할이 바뀌는 관외이전이었다면 주주총회 특별결의까지 필요했을 겁니다.</div>
</div>

<h2>그래서 등기를 10/15보다 당기세요</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">등기는 접수 즉시 끝나지 않습니다</div><div class="m">접수 후 완료까지 며칠 걸리고, 그다음에 등기사항전부증명서를 떼서 세무서에 다시 내야 합니다. 10/15에 아슬아슬하게 접수하면 세무서 재신청이 더 밀립니다</div></li>
    <li><div class="t">세무서에 전화 한 통 해두세요</div><div class="m">"법인등기 변경을 진행 중이고, 완료되면 바로 재신청하겠다"고 담당자에게 알려두면 됩니다. 취하는 어차피 되지만 사정이 기록에 남습니다</div></li>
    <li class="big"><div class="t">법무사에게 이 문자를 그대로 보여주세요</div><div class="m">세무서가 이미 한 번 막았다는 건 <b>급하다는 근거</b>입니다. 일정을 앞당겨 달라고 말하기 좋습니다</div></li>
  </ul>
</div>

<h2>걱정했던 두 가지 — 둘 다 괜찮습니다</h2>
<div class="card blue">
  <ul class="list">
    <li><div class="t">중임등기, 이미 하셨습니다</div><div class="m">사내이사와 감사 모두 <b>2025년 3월 16일 중임, 3월 24일 등기</b>. 만료일(3/16)로부터 8일 만에 접수하셨으니 2주 기한도 지켰습니다. <b>다음 만료는 2028년 3월 16일</b>이라 한참 남았습니다</div></li>
    <li><div class="t">해산간주도 위험 없습니다</div><div class="m">최후 등기가 <b>2025년 3월 24일</b>이라 5년이 되는 건 2030년입니다. 제가 "최후 등기가 설립등기일 수 있다"고 했던 건 틀렸습니다</div></li>
  </ul>
  <div class="note">받으셨다는 임원 임기 안내는 <b>2025년 3월 중임 때의 안내</b>였을 가능성이 높습니다. 그래서 기억에 남으신 것 같습니다.</div>
</div>

<h2>그래서 10/15에 꼭 해야 하는 건 하나입니다</h2>
<div class="card red">
  <p style="font-size:18px;font-family:'Gowun Dodum',sans-serif;margin:0 0 8px"><b>본점이전등기 — 10월 15일(목)까지</b></p>
  <p style="margin:0">등기부상 본점은 아직 <b>경기도 구리시 갈매순환로 188, 제7층(갈매동, 힐스테이트 갈매역 스칸센)</b>입니다. 2023년 12월 1일 변경, 12월 12일 등기된 주소고, 그 사무실에서 10/1에 나오셨으니 이전등기 대상입니다.</p>
  <div class="note">같은 구리시 안으로 옮기셨고 정관의 본점 조항이 '경기도 구리시'로만 적혀 있다면 정관 변경이 필요 없고, 이사가 1명이라 <b>이사 결정서</b>로 처리됩니다. 공과금은 142,000원.</div>
</div>

<h2>등기부에서 새로 보인 것 — 다섯 가지</h2>
<div class="card gold">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">수권주식 200주를 <b>전부 발행</b>한 상태입니다</div><div class="m">"발행할 주식의 총수 200주"인데 "발행주식의 총수"도 200주입니다. <b>지금 상태로는 신주를 한 주도 더 못 찍습니다.</b> 지분을 증자로 주시려면 정관을 고쳐 수권주식 수부터 늘려야 합니다 — 주주총회 특별결의가 필요하니 10/15 등기에 묶을 수 있습니다</div></li>

    <li><span class="tag p0">2</span><div class="t">목적에 <b>교육업·창고업·소프트웨어</b>가 없습니다</div><div class="m">반대로 <b>부동산 매매업 및 임대업은 이미 들어 있습니다</b> — 꼬마빌딩용으로 따로 추가할 필요가 없습니다. 전자상거래 및 통신판매업도 있습니다. 셀러들의 수다로 가시려면 <b>교육서비스업 · 창고업·물류대행업 · 소프트웨어 개발 및 공급업</b> 정도를 넣으세요</div></li>

    <li><span class="tag p1">3</span><div class="t">자본금이 <b>100만 원</b>입니다 (200주 × 5,000원)</div><div class="m">꼬마빌딩을 사고 대출을 받을 법인 치고는 작습니다. 심사에서 불리하게 볼 수 있어서, 증자는 지분 문제와 별개로 한 번 생각해 보실 거리입니다. 참고로 <b>51 / 26 / 23은 200주 기준 102주 / 52주 / 46주</b>로 정확히 떨어집니다</div></li>

    <li><span class="tag p1">4</span><div class="t">공고방법이 <b>"수원시 내에서 발행하는 일간 경기신문"</b>입니다</div><div class="m">본점은 구리인데 공고는 수원 신문으로 되어 있습니다. 설립 때 서식 그대로 간 것 같습니다. 나중에 증자·합병 같은 걸 하면 <b>실제로 신문에 광고를 내야 하고 비용이 듭니다.</b> 이번에 <b>"회사 인터넷 홈페이지에 게재한다"</b>로 바꿔두면 그 비용이 사라집니다 — 정관 변경 사항이라 어차피 여는 주주총회에 같이 올리면 됩니다</div></li>

    <li><span class="tag p1">5</span><div class="t">대표이사 주소가 2024년 4월에 변경 등기돼 있습니다</div><div class="m">그 뒤로 이사하셨다면 그것도 2주 내 변경등기 대상입니다. <b>지금 사시는 곳과 같은지</b>만 확인하세요 — 다르면 이것도 밀려 있는 겁니다</div></li>
  </ul>
</div>

<h2>이번 등기 최종 체크리스트</h2>
<div class="card wrapx">
<table>
<tr><th></th><th>항목</th><th>정관 변경</th><th>판단</th></tr>
<tr><td class="num">1</td><td><b>본점 이전</b></td><td>같은 시면 불필요</td><td class="num"><b>10/15까지 필수</b></td></tr>
<tr><td class="num">2</td><td><b>상호 변경</b> (셀러들의 수다)</td><td>필요</td><td class="num">같이 권장</td></tr>
<tr><td class="num">3</td><td><b>사업목적 추가</b> (교육·창고·소프트웨어)</td><td>필요</td><td class="num">같이 권장</td></tr>
<tr><td class="num">4</td><td><b>수권주식 수 증가</b></td><td>필요</td><td class="num">증자로 가실 거면 같이</td></tr>
<tr><td class="num">5</td><td><b>공고방법 변경</b> (홈페이지)</td><td>필요</td><td class="num">같이 하면 공짜</td></tr>
<tr><td class="num">—</td><td>임원 중임</td><td>—</td><td class="num"><b>이미 완료</b> (2028-03까지)</td></tr>
<tr><td class="num">—</td><td>신정현님 임원 선임</td><td>불필요</td><td class="num">세무사 확인 후 별도</td></tr>
<tr><td class="num">—</td><td>지분 51/26/23</td><td>—</td><td class="num">등기 아님 (주주명부)</td></tr>
</table>
<div class="note">2~5는 전부 <b>정관 변경</b>이라 주주총회 특별결의가 필요한데, 루크님이 100% 주주시라 <b>서면결의 한 장</b>으로 끝납니다. 어차피 여는 결의에 항목만 늘리는 거라 추가 부담이 거의 없습니다. 한 신청서로 묶을 때 등록면허세가 어떻게 계산되는지만 법무사에게 확인하세요.</div>
</div>

<h2>영문 상호도 같이 보세요</h2>
<div class="card">
  <p style="margin:0">등기부에 영문 상호가 <b>HEALING THE EARTH Co.,Ltd.</b>로 올라가 있습니다. 한글 상호를 '셀러들의 수다'로 바꾸시면 <b>영문도 같이 정하셔야</b> 합니다 — 안 바꾸면 한글과 영문이 전혀 다른 회사처럼 남습니다.</p>
</div>

<h2>지분은 여전히 등기 사항이 아닙니다</h2>
<div class="card blue wrapx">
<table>
<tr><th></th><th>주식 양도</th><th>신주발행(증자)</th></tr>
<tr><td>돈이 가는 곳</td><td class="num">루크 개인</td><td class="num"><b>법인</b></td></tr>
<tr><td>등기</td><td class="num">불필요</td><td class="num"><b>필요</b></td></tr>
<tr><td>선행 조건</td><td class="num">없음</td><td class="num"><b>수권주식 증가(정관 변경)</b></td></tr>
<tr><td>세금</td><td class="num">양도소득세 + 증권거래세</td><td class="num">등록면허세 (5년 내면 3배 중과)</td></tr>
</table>
<div class="note">양도로 가시면 루크님 200주 중 <b>52주를 신정현님께, 46주를 제3자에게</b> 넘기면 51 / 26 / 23이 됩니다. 증자로 가시면 수권주식부터 늘려야 하니 10/15 등기에 4번 항목이 들어갑니다.</div>
</div>

<h2>등기 말고 같이</h2>
<div class="card wrapx">
<table>
<tr><th>무엇</th><th>어디</th><th>기한</th></tr>
<tr><td><b>사업자등록 정정</b></td><td>세무서 / 홈택스</td><td class="num">지체 없이 (등기 직후)</td></tr>
<tr><td>4대보험 소재지 변경</td><td>공단</td><td class="num">해당 없음 <span class="tag">직원·유급임원 없음</span></td></tr>
<tr><td>등록면허세</td><td>관할 지자체</td><td class="num">등기 신청 시</td></tr>
<tr><td>주소·상호 교체</td><td>세금계산서·법인 통장·카드·거래처</td><td class="num">상호까지 바뀌니 함께</td></tr>
</table>
</div>

<h2>남은 확인 필요</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">정관의 본점 조항이 '경기도 구리시'까지만인지</div><div class="m">번지까지 적혀 있으면 같은 시 안이어도 정관 변경이 필요합니다</div></li>
    <li><div class="t">새 본점 주소 확정</div><div class="m">구리 시내 비상주 사무실</div></li>
    <li><div class="t">대표이사 현재 거주지가 등기부와 같은지</div></li>
    <li><div class="t">구리 관할에 '셀러들의 수다' 동일 상호가 있는지</div><div class="m">관할은 의정부지방법원 남양주지원 등기과입니다</div></li>
    <li><div class="t">지분을 양도로 줄지 증자로 줄지</div><div class="m">증자면 10/15 등기에 수권주식 증가가 들어갑니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: 2026-10-07 확인 — 법인 사업장 이전은 본점이전등기 → 등기 완료 후 등기부등본 재발급 → 그 등기부등본을 첨부해 사업자등록 정정 순서이며, 사업자등록 정정 시 변경된 법인등기부등본이 필수 첨부(스마트워킹스페이스 및 법인 주소변경 절차 안내 2건에서 동일 확인). 2026-10-07 열람한 힐링디어스 주식회사 등기사항전부증명서(말소사항 포함, 열람 700원) — 회사성립 2022-03-16 · 본점 경기도 구리시 갈매순환로 188 제7층(2023-12-01 변경, 2023-12-12 등기) · 1주 금액 5,000원 · 발행할 주식의 총수 200주 · 발행주식의 총수 200주 · 자본금 100만 원 · 공고방법 수원시 내 발행 일간 경기신문 · 목적에 부동산 매매업 및 임대업, 전자상거래 및 통신판매업 포함(2023-01-09 다수 추가) · 사내이사·감사 2025-03-16 중임, 2025-03-24 등기 · 관할 의정부지방법원 남양주지원 등기과. 그 외: 상법 제182조(본점 이전등기 2주) · 상법 제383조(이사 임기 3년) · 상법 제520조의2(최후 등기 후 5년 해산간주) · 본점이전 공과금 142,000원(같은 관할). <b>여러 변경을 한 신청서로 묶을 때의 등록면허세 계산, 증자 등록면허세 세율은 확인하지 못했습니다 — 법무사 확인 후 진행하세요.</b></div>
"""
# ---------------------------------------------------------------- 등기부 열람 가이드
IROS = """
<h1>등기부 열람 — 클릭 순서</h1>
<p class="note">힐링디어스(주) 등기사항전부증명서를 인터넷등기소에서 직접 보는 방법입니다. <b>열람 700원, 5분이면 끝납니다.</b> 확인할 것은 세 가지 — 중임 기록 · 임원 취임일 · 최후 등기일. 왜 봐야 하는지는 <a href="../relocation/">10/15 등기 체크리스트</a>에 있습니다.</p>

<h2>시작하기 전에</h2>
<div class="card">
  <dl class="kv">
    <dt>주소</dt><dd><a href="https://www.iros.go.kr" target="_blank" rel="noopener"><b>www.iros.go.kr</b></a> — 대법원 인터넷등기소</dd>
    <dt>준비물</dt><dd>카드·계좌이체·휴대폰 결제 중 하나. <b>공동인증서는 없어도 됩니다</b></dd>
    <dt>법인등록번호</dt><dd>모르셔도 상호로 찾을 수 있습니다. 알고 계시면 더 빠릅니다 — <b>법인 사업자등록증</b>에 적혀 있습니다</dd>
    <dt>비용</dt><dd>열람 700원 / 발급 1,000원</dd>
  </dl>
</div>

<h2>화면 순서</h2>
<div class="card accent">
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">1단계</div><div class="t">iros.go.kr 접속 → 상단 <b>[법인등기]</b> → <b>[열람/발급(출력)]</b></div><div class="d">부동산등기가 아니라 <b>법인등기</b>입니다. 메뉴가 나란히 있어서 헷갈리기 쉽습니다</div></li>

    <li><div class="d">2단계</div><div class="t">검색 조건 입력</div><div class="d">
      <b>관할등기소</b> — '전체'로 두세요 (구리 관할을 모르셔도 됩니다)<br>
      <b>법인구분</b> — 주식회사<br>
      <b>등기상태</b> — <b>살아있는 등기</b><br>
      <b>본지점구분</b> — 본점<br>
      <b>상호</b> — <b>힐링디어스</b> 입력 후 검색
    </div></li>

    <li><div class="d">3단계</div><div class="t">검색 결과에서 우리 회사 고르기</div><div class="d">같은 상호가 여러 개 뜰 수 있습니다. <b>본점 주소</b>를 보고 고르세요 — 등기부상으로는 아직 <b>경기도 구리시 갈매순환로 154 A408호</b>로 되어 있을 겁니다</div></li>

    <li class="big"><div class="d">4단계 — 여기가 핵심</div><div class="t">등기기록 유형에서 <b>'말소사항 포함'</b> 선택</div><div class="d">
      '전부'를 고르고, 그 안에서 <b>말소사항 포함</b>을 선택하세요.<br>
      <b>'현재 유효사항'만 고르면 과거 중임 기록이 안 보입니다.</b> 지금 확인하려는 게 바로 그 과거 기록이라, 여기서 잘못 고르면 헛수고가 됩니다
    </div></li>

    <li><div class="d">5단계</div><div class="t">주민등록번호 공개 여부 → <b>미공개</b></div><div class="d">본인 확인용이니 공개할 필요가 없습니다</div></li>

    <li><div class="d">6단계</div><div class="t">결제 → 화면에서 바로 열람</div><div class="d">열람 700원. 결제하면 바로 화면에 뜹니다</div></li>
  </ol>
</div>

<h2>열리면 세 군데를 보세요</h2>
<div class="card wrapx">
<table>
<tr><th>어디를</th><th>무엇을 찾나</th><th>어떻게 읽나</th></tr>
<tr><td><b>① 임원에 관한 사항</b></td><td>"사내이사 유믿음 2022년 3월 16일 취임" 밑에 <b>"○년 ○월 ○일 중임"</b>이 있는지</td><td><b>있으면</b> 그 날 + 3년이 다음 만료일 → 지금은 괜찮음<br><b>없으면</b> 2025-03경 만료 → 밀려 있음</td></tr>
<tr><td><b>② 같은 란의 감사</b></td><td>어머니 취임일과 중임 기록</td><td>감사는 임기 계산이 달라(상법 제410조) 이사와 만료일이 어긋납니다. 따로 보세요</td></tr>
<tr><td><b>③ 가장 아래 등기 날짜</b></td><td>마지막으로 등기한 날</td><td>이게 <b>해산간주 5년</b>의 기산점입니다. 2022-03-16(설립) 그대로면 2027년이 위험 구간</td></tr>
</table>
<div class="note">중임 기록은 보통 <b>취소선이 그어진 줄 바로 아래</b>에 새 줄로 나타납니다. 말소사항 포함으로 떼야 그 취소선 줄까지 보입니다.</div>
</div>

<h2>막히기 쉬운 곳</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">부동산등기 메뉴로 들어갔다</div><div class="m">상단에 [부동산등기]와 [법인등기]가 나란히 있습니다. <b>법인등기</b>로 들어가세요</div></li>
    <li><div class="t">검색 결과가 안 나온다</div><div class="m">상호를 '힐링디어스'까지만 넣어보세요. '(주)'나 '주식회사'를 붙이면 안 걸릴 수 있습니다. 그래도 안 되면 <b>법인등록번호</b>로 검색하세요 — 사업자등록증에 있습니다</div></li>
    <li><div class="t">'현재 유효사항'으로 떼버렸다</div><div class="m">과거 기록이 안 보입니다. 700원이 아깝지만 <b>말소사항 포함으로 다시 떼세요</b></div></li>
    <li><div class="t">법무사에게 줄 건데 열람으로 떼었다</div><div class="m">열람 화면에서 출력한 것은 <b>제출용으로 효력이 없습니다.</b> 제출하실 거면 발급 1,000원으로 다시 받으세요. 직접 보기만 할 거면 열람으로 충분합니다</div></li>
  </ul>
</div>

<h2>다 보시고 나면</h2>
<div class="card blue">
  <ul class="list">
    <li><div class="t">중임 기록이 있었다</div><div class="m">임원 쪽은 깨끗합니다. 10/15 등기는 <b>본점이전 + 상호변경 + 목적추가</b> 셋만 하면 됩니다</div></li>
    <li><div class="t">중임 기록이 없었다</div><div class="m">1년 반 밀려 있는 겁니다. <b>중임등기를 같이 넣으세요.</b> 어차피 상호·목적 때문에 주주총회를 여실 거라 결의를 한 번에 올리면 됩니다</div></li>
    <li class="big"><div class="t">최후 등기일이 2022-03-16 그대로였다</div><div class="m">해산간주 시계가 2027년 3월에 5년이 됩니다. <b>10/15 등기로 리셋되니 더더욱 미루면 안 됩니다</b></div></li>
  </ul>
  <div class="note">어느 경우든 화면을 캡처해서 법무사에게 보내시면 통화가 훨씬 빨라집니다. 받으셨다는 임원 임기 안내 우편물도 같이요.</div>
</div>

<div class="src" style="margin-top:14px">근거(2026-10-07 확인): 대법원 인터넷등기소 법인등기 열람·발급 절차(메뉴 [법인등기] → [열람/발급(출력)], 검색 조건으로 관할등기소·법인구분·등기상태·본지점구분·상호, 주민등록번호 공개 여부 선택, 열람 700원·발급 1,000원, 열람 화면 출력물은 제출용 효력 없음) · 상법 제383조(이사 임기 최대 3년) · 상법 제410조(감사 임기) · 상법 제520조의2(최후 등기 후 5년 해산간주). <b>화면 문구와 버튼 위치는 사이트 개편에 따라 달라질 수 있습니다.</b> 이 대화는 루크님 컴퓨터에 연결돼 있지 않아 제가 직접 열어서 보여드릴 수는 없었습니다.</div>
"""

# ---------------------------------------------------------------- 법인 서류와 등기 방식
VAULT = """
<h1>셀프 등기 · 정관 찾기 · 서류 보관</h1>
<p class="note">10/7에 주신 세 가지 질문에 대한 답입니다. 힐링디어스(주) 기준 — 자본금 100만 원, 주주 루크 100%, 이사 1명(대표이사), 감사 1명, 관할 의정부지방법원 남양주지원 등기과. 저는 법무사가 아닙니다.</p>

<h2>① 혼자 할까, 법무사를 쓸까</h2>
<div class="card accent">
  <p style="font-size:17px;font-family:'Gowun Dodum',sans-serif;margin:0 0 8px"><b>이번 건은 법무사를 쓰세요. 다음부터 단건은 혼자 하셔도 됩니다.</b></p>
  <p style="margin:0">셀프등기가 불가능해서가 아닙니다. 오히려 힐링디어스는 <b>셀프에 가장 유리한 조건</b>을 다 갖추고 있습니다. 문제는 이번 건의 성격입니다.</p>
</div>

<div class="card blue">
  <p style="margin:0 0 10px"><b>셀프에 유리한 조건 — 자본금 10억 미만 소규모 회사 특례</b></p>
  <ul class="list">
    <li><div class="t">정관·의사록 공증이 필요 없습니다</div><div class="m">자본금 10억 미만이면 인증 의무가 없습니다. 공증 사무소에 갈 일이 없습니다</div></li>
    <li><div class="t">주주총회를 실제로 열 필요가 없습니다</div><div class="m">주주 전원 동의로 소집절차를 생략할 수 있고 <b>서면결의</b>로 대체됩니다. 루크님이 100% 주주시니 <b>서류 한 장</b>으로 끝납니다</div></li>
    <li><div class="t">이사가 1명이라 이사회가 없습니다</div><div class="m">본점이전은 <b>이사 결정서</b>로 처리됩니다</div></li>
  </ul>
</div>

<div class="card red">
  <p style="margin:0 0 10px"><b>그런데 이번 건은 이렇습니다</b></p>
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">8일 남았고, 반려되면 되돌릴 시간이 없습니다</div><div class="m">상호 중복, 첨부서면 누락, 결의서 형식 — 처음 하면 한 번은 걸립니다. 보정하는 동안 10/15가 지나가면 과태료가 붙습니다</div></li>
    <li><span class="tag p0">2</span><div class="t">정관 원본이 아직 없습니다</div><div class="m">상호·목적·수권주식·공고방법을 바꾸려면 <b>지금 정관이 무엇인지부터 알아야</b> 합니다. 아래 ②번이 선행 조건인데, 등기소 열람·등사는 법무사가 대신 해줄 수 있습니다</div></li>
    <li><span class="tag p0">3</span><div class="t">앞으로 2년간 등기할 일이 줄줄이 있습니다</div><div class="m">지분 이전, 신정현님 임원 선임, 증자, 창고형 매장 지점 설치까지. <b>거래 법무사를 한 명 만들어 두는 게 전체 비용을 낮춥니다</b> — 매번 처음부터 설명하지 않아도 되니까요</div></li>
  </ul>
</div>

<div class="card wrapx">
<table>
<tr><th></th><th>혼자</th><th>법무사</th></tr>
<tr><td>공과금</td><td class="num">142,000원</td><td class="num">142,000원</td></tr>
<tr><td>수수료</td><td class="num">0원</td><td class="num"><span class="tag">확인 필요</span></td></tr>
<tr><td>정관 찾기</td><td class="num">직접</td><td class="num">대행 가능</td></tr>
<tr><td>반려 시</td><td class="num"><b>기한 초과 위험</b></td><td class="num">법무사가 보정</td></tr>
<tr><td>걸리는 시간</td><td class="num">처음이면 반나절~하루</td><td class="num">서류 전달만</td></tr>
</table>
<div class="note">법무사 수수료는 사무소마다 다릅니다 — <b>2~3곳에 전화해서 "본점이전 + 상호변경 + 목적추가 + 수권주식 증가 + 공고방법 변경, 자본금 100만 원 1인 회사"로 견적을 받아보세요.</b> 묶어서 하면 단건보다 유리한 경우가 많습니다.</div>
</div>

<div class="card gold">
  <p style="margin:0 0 8px"><b>다음부터 혼자 하셔도 되는 것</b></p>
  <ul class="list">
    <li><div class="t">대표이사 주소 변경</div><div class="m">결의도 필요 없고 서류가 단순합니다</div></li>
    <li><div class="t">같은 관할 안에서의 단순 본점이전</div><div class="m">이사 결정서 한 장</div></li>
    <li><div class="t">임원 중임등기</div><div class="m">2028년 3월에 또 오는 일입니다. 이번에 법무사가 하는 걸 옆에서 보고 서식을 받아두시면 다음엔 혼자 하실 수 있습니다</div></li>
  </ul>
  <div class="note">이번에 법무사에게 <b>이번 건의 첨부서면 일체를 PDF로 받아두세요.</b> 다음에 같은 걸 할 때 그게 교재가 됩니다.</div>
</div>

<h2>② 정관 — 새로 만들기 전에 찾으세요</h2>
<div class="card accent">
  <p style="margin:0 0 10px">정관은 <b>'새로 만드는' 게 아니라 '고치는' 문서</b>입니다. 설립 때 만든 원시정관이 법적으로 존재하고, 그걸 주주총회 결의로 변경해 온 이력이 있습니다. 어딘가에 반드시 있습니다 — 정관은 전산망에 등록되지 않고 <b>회사가 직접 보관</b>하는 문서라서 '발급'이 안 될 뿐입니다.</p>
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">등기를 맡겼던 법무사</div><div class="d">세 번의 등기가 있었습니다 — <b>설립(2022-03), 목적 대량 추가(2023-01), 중임(2025-03).</b> 각각 다른 사무소일 수도 있습니다. 가장 가능성 높은 경로입니다</div></li>
    <li><div class="t">세무사</div><div class="d">기장을 맡기면서 법인 서류 일체를 넘기셨을 수 있습니다. 어차피 수입금액 때문에 전화하실 거니 같이 물어보세요</div></li>
    <li class="big"><div class="t">관할 등기소 열람·등사 — 가장 확실합니다</div><div class="d"><b>의정부지방법원 남양주지원 등기과.</b> 등기 신청 때 제출한 정관이 편철돼 있고, <b>5년 이내 제출분</b>은 열람·등사를 신청할 수 있습니다. 설립(2022-03)도 목적변경(2023-01)도 모두 5년 안이라 지금은 됩니다. <b>5년이 지나면 폐기되니 올해 안에 받아두세요</b></div></li>
    <li><div class="t">공증 사무소</div><div class="d">설립 때 공증을 받았다면 그쪽에도 사본이 있습니다. 다만 자본금 10억 미만이라 공증을 안 했을 가능성이 높습니다</div></li>
    <li><div class="t">외장하드·메일 검색</div><div class="d">검색어는 <b>'정관', '힐링디어스', '발기인'</b>. 기간은 2022년 2~3월과 2023년 1월 전후</div></li>
  </ol>
</div>

<div class="card blue">
  <p style="margin:0 0 8px"><b>그래도 못 찾으면 — 어렵지 않습니다</b></p>
  <p style="margin:0">주주총회에서 <b>'정관 전부개정'</b> 결의를 하면 됩니다. 1인 주주라 서면결의로 가능하고 공증도 필요 없습니다. 등기부에 적힌 내용(상호·본점·목적·주식·공고방법)과 일치하게 재작성하는 작업이고, 법무사가 늘 하는 일입니다.</p>
  <div class="note">사실 이번에 <b>상호·목적·수권주식·공고방법 네 군데를 다 바꾸실 거라</b>, 원본을 찾아도 어차피 대폭 고칩니다. <b>처음부터 전부개정으로 가는 게 더 깔끔할 수 있습니다</b> — 법무사에게 이 선택지를 물어보세요.</div>
</div>

<h2>③ 서류 보관 — 지금은 목록 한 장이면 됩니다</h2>
<div class="card gold">
  <p style="margin:0 0 10px">프로그램을 만들 일은 맞는데 지금은 아닙니다. 외장하드 뒤지실 때 이 목록을 체크리스트로 쓰세요. <b>상법상 본점에 비치할 의무가 있는 것</b>부터 적었습니다.</p>
  <div class="wrapx"><table>
  <tr><th>문서</th><th>왜 필요한가</th><th>상태</th></tr>
  <tr><td><b>정관</b> (최신 + 변경 이력)</td><td>본점 비치 의무. 모든 등기의 출발점</td><td class="num"><b>찾는 중</b></td></tr>
  <tr><td><b>주주명부</b></td><td>본점 비치 의무. 지분 51/26/23의 근거가 될 문서</td><td class="num">확인 필요</td></tr>
  <tr><td><b>주주총회 의사록</b> 전부</td><td>본점 비치 의무. 정관 변경 이력의 증거</td><td class="num">확인 필요</td></tr>
  <tr><td>이사 결정서 / 이사회 의사록</td><td>본점이전 등 결의 기록</td><td class="num">확인 필요</td></tr>
  <tr><td>등기사항전부증명서</td><td>10/7 열람 완료</td><td class="num">확보</td></tr>
  <tr><td>법인인감증명서 · 인감카드</td><td>등기 신청에 필요</td><td class="num">확인 필요</td></tr>
  <tr><td>사업자등록증</td><td>법인등록번호 확인, 정정신고에 필요</td><td class="num">확인 필요</td></tr>
  <tr><td>설립 서류 일체</td><td>발기인총회 의사록, 주식인수증, 잔고증명 등</td><td class="num">확인 필요</td></tr>
  <tr><td>법인세·부가세 신고서, 재무제표</td><td>수입금액 확인, 빌딩 대출 심사</td><td class="num">세무사 보관</td></tr>
  <tr><td>임대차계약서</td><td>사업자등록 정정에 필요</td><td class="num">확인 필요</td></tr>
  </table></div>
  <div class="note">보관은 거창할 필요 없습니다 — <b>클라우드에 '법인/힐링디어스' 폴더 하나</b> 만들고 위 순서대로 넣으세요. 파일명 앞에 날짜를 붙이면(2022-03-16_정관.pdf) 그것만으로 이력이 됩니다. 프로그램은 넣을 서류가 다 모인 다음에 만들어도 늦지 않습니다.</div>
</div>

<h2>이번 주 순서</h2>
<div class="card">
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">오늘~내일</div><div class="t">법무사 2~3곳 견적 + 정관 보유 여부 확인</div><div class="d">설립을 맡겼던 곳이 있으면 거기부터. "정관 가지고 계신가요"를 먼저 물어보세요</div></li>
    <li><div class="d">같은 전화에</div><div class="t">세무사에게 수입금액 + 정관 보유 여부</div></li>
    <li><div class="d">둘 다 없으면</div><div class="t">등기소 열람·등사 신청 (또는 법무사에게 대행 요청)</div></li>
    <li class="big"><div class="d">10/15까지</div><div class="t">본점이전 + 상호 + 목적 + 수권주식 + 공고방법 접수</div><div class="d">정관이 안 나오면 <b>전부개정</b>으로 진행</div></li>
  </ol>
</div>

<div class="src" style="margin-top:14px">근거(2026-10-07 확인): 자본금 10억 원 미만 소규모 주식회사 특례 — 정관 공증 의무 없음, 이사 1~2명 가능(3명 미만이면 이사회 불요), 감사 임의, 주주총회 소집통지 10일, 주주 전원 동의 시 소집절차 생략 및 서면결의 가능(상법 제292조·제318조·제363조·제383조·제409조 관련) · 정관 분실 시 ① 설립 대행 법무사·변호사 ② 공증 사무소 ③ 관할 등기소 열람·등사(등기 신청 시 정관을 제출한 건에 한하며 <b>5년 경과 후 폐기</b>) · 상법 제396조(정관·주주총회 의사록은 본점과 지점에, 주주명부는 본점에 비치) · 본점이전 공과금 142,000원(같은 관할). <b>법무사 수수료는 사무소별로 달라 확인하지 못했습니다. 등기소 열람·등사의 구체적 신청 방법과 수수료도 확인 필요입니다.</b></div>
"""

# ---------------------------------------------------------------- 지영 페이지 프롬프트
JYPROMPT = """
<h1>지영 원장 빌드업 페이지 — 프롬프트</h1>
<p class="note">키티티바이지영(윤지영 원장)용 수익모델 빌드업 페이지를 새 세션에서 만들 때 쓰실 프롬프트입니다. 아래 버튼으로 복사해서 새 클로드 코드 세션에 그대로 붙여넣으세요.</p>

<h2>붙여넣기 전에 — 두 가지만</h2>
<div class="card red">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">luke-1b에 넣지 마세요. 새 저장소로 가세요</div><div class="m">luke-1b는 루크님 사업 전체가 담긴 페이지입니다. 지영 원장에게 링크를 주면 <b>인베이더·초월스토리·법인 정리·수익 배분까지 다 보입니다.</b> 저장소를 따로 만드셔야 합니다 — 프롬프트에 <b>kittiti-jiyoung</b>으로 넣어 뒀습니다. 저장소 생성과 Pages 켜기는 루크님이 직접 하셔야 합니다</div></li>
    <li><span class="tag p0">2</span><div class="t">꿈 사진은 공개 페이지에 올리지 않는 쪽이 낫습니다</div><div class="m">"개인 소장용"과 <b>공개 URL에 게시</b>하는 것은 다릅니다. 매물 사진·자동차 사진·브랜드 이미지를 가져다 올리면 저작권 문제가 생길 수 있고, 저도 브랜드 로고나 특정 차량 디자인을 코드로 재현하지는 않습니다. 대신 <b>코드로 그린 원본 일러스트 + 실제 가격 숫자</b>로 가도록 프롬프트에 넣었습니다</div></li>
  </ul>
</div>

<div class="card blue">
  <p style="margin:0 0 8px"><b>그리고 이게 더 세게 작동할 겁니다</b></p>
  <p style="margin:0">루크님 10억 페이지가 힘이 있는 건 사진이 아니라 <b>숫자와 날짜</b> 때문입니다. 지영 원장 페이지도 마찬가지로 — 성북구 고급 주택이 얼마고, 3층 건물이 얼마고, 차가 얼마인지 <b>실제 시세를 찾아 합계를 내고, 거기까지 필요한 연 순이익을 역산</b>하는 게 사진 열 장보다 셉니다. 프롬프트가 그렇게 시키도록 써 뒀습니다.</p>
</div>

<h2>프롬프트</h2>
<div class="card">
  <button class="cpy" data-t="p1" style="font:inherit;font-weight:700;padding:10px 16px;border-radius:10px;border:0;background:var(--ac,#5b8def);color:#fff;cursor:pointer;margin-bottom:10px">프롬프트 복사</button>
  <pre id="p1" style="white-space:pre-wrap;word-break:break-word;font-size:13px;line-height:1.65;margin:0;font-family:inherit">키티티바이지영(윤지영 원장)의 '수익모델 빌드업' 페이지를 만들어줘.
내 '내 연봉 10억 만들기' 대시보드(github.com/Yoo-Mideum/luke-1b)와 같은 형식이고, 지영 원장에게 공유할 페이지야.

[0] 저장소
- 새 저장소 kittiti-jiyoung 에 만들어줘. 저장소 생성과 Pages 켜기는 내가 직접 할 테니 필요하면 알려줘.
- luke-1b에는 절대 넣지 마. 내 다른 사업 내용이 지영 원장에게 보이면 안 돼.
- clone해서 작업하고 git push로 배포해줘. 기기 인증(device code) 방식은 이 환경에서 막혀 있으니 시도하지 마.
  push가 403이면 우회하지 말고 바로 알려줘. 내가 권한 열어줄게.
- 배포 후 링크는 ?v=1 처럼 숫자를 붙여서 줘.

[1] 페이지 규칙
- self-contained HTML 한 파일. CSS와 JS는 인라인, 외부는 구글 폰트만.
- 폴더 구조는 /항목명/index.html, 루트 index.html이 전체 목록 허브.
- 모바일 우선 max-width 600px, Gowun Dodum + Noto Sans KR, prefers-color-scheme 다크모드.
- 전부 build.py 하나에서 생성되게 해줘.
- 코드 고칠 때 한 줄 핀포인트 수정 말고 파일 전체를 새로 써줘.
- 커밋 메시지는 한글로, 바뀐 것을 목록으로.

[2] 먼저 자료를 모아줘 — 플라우드
Plaud MCP로 아래를 읽고 지영 원장 관련 사실을 뽑아줘.
- list_files로 '지영', '키티티', '메이크업'을 각각 검색해줘. 제목만 매칭되고 page_size는 최소 10이야.
- 이미 아는 파일 ID:
  of_b4b445dd8d81e2e5131aa0e66145580c   지영이 확장 미팅 / 갈매 (2026-09-08, 134분) — 가장 중요
  of_6a420befadc2996a3637c2a2c2817142   09-04 지영 뷰티 사업의 오프라인 및 디지털 현금흐름 구축 전략 회의 (20분)
  of_0c2012402fb03a930015fd5f60266c06   09-26 상담: 지영 - 정부지원사업을 통한 사업 확장
  of_d07e5712e0711ed74016d48d50f873da   9월 19일 박초희 교수님 - 지영이 레포트 피드백
- get_note(file_id=...)로 읽어줘. 본문이 길면 서브에이전트에 맡겨서 요약만 받아와 — 내 컨텍스트를 아끼고 싶어.
- 뽑을 것: 현재 매출과 객단가, 시술 종류별 비중, 고객 수와 재방문율, 확장 계획(샵 규모·인력·아카데미),
  정부지원사업 진행 상황, 자금 계획과 부족분, 원장이 직접 말한 목표와 걱정, 결정된 것과 아직 미결인 것.
- 녹음에 없는 건 지어내지 말고 '확인 필요'로 남겨줘.

[3] 페이지 구성
루트 허브 아래 이렇게 만들어줘.
1. 수익모델 — 지금 돈이 어디서 오는가. 시술별 매출·객단가·회전율, 각 축이 어디서 막히는가, 다음 축 후보.
2. 목표 — 세 가지 꿈을 숫자로.
   가) 성북구 고급 주택
   나) 3층 건물 '키티티바이지영' 메이크업샵 (원장 본인 소유 꼬마빌딩)
   다) 맥라렌 스파이더 (정확한 모델명은 원장에게 확인 필요로 표시)
   각각 실제 가격대를 검색해서 확인하고, 세 개 합계와 거기까지 가는 데 필요한 연 순이익을 역산해줘.
   못 찾으면 '확인 필요'라고 적고 그럴듯하게 채우지 마.
3. 경로 — 지금 매출에서 그 숫자까지 가는 단계. 1년 / 3년 / 5년으로 나누고,
   각 단계에서 무엇이 바뀌어야 하는지(객단가, 좌석 수, 인력, 아카데미, 온라인)를 적어줘.
4. 사업 유니버스 — 별자리 지도.
   luke-1b의 /universe/ 와 같은 방식으로 만들어줘. SVG와 인라인 JS, 노드와 엣지, 3D 회전, 전체화면.
   노드는 '지금 하는 것 / 준비 중 / 구상 중'으로 구분하고, 서로 어떻게 이어지는지 선으로 그려줘.
   luke-1b 저장소의 build.py에 있는 universe_html() 함수를 참고해도 좋아.
5. 일정 — 확정된 날짜만. 추정이면 '잠정'이라고 표시.
6. 출처 — 어느 녹음·자료에서 나온 내용인지 작게.

[4] 이미지 규칙 — 중요
- 이 페이지는 공개 URL이야. 남의 사진(매물 사진, 자동차 사진, 브랜드 이미지)을 가져다 올리지 마.
  개인 소장과 공개 게시는 다른 문제야.
- 브랜드 로고나 특정 차량 디자인을 코드로 재현하지도 마.
- 대신 이렇게 해줘.
  · 분위기는 코드로 그린 원본 일러스트(SVG 또는 CSS)로. 예를 들어 빛이 켜진 창이 있는 집 실루엣,
    3층 건물 단면도, 속도감을 주는 추상적인 선 같은 것.
  · 꿈은 사진보다 숫자로 보여줘. 가격, 필요한 연수, 월 순이익 목표가 사진보다 훨씬 세게 작동해.
  · 꼭 사진이 필요한 자리가 있으면 상업적 이용이 가능한 무료 이미지 출처만 알려줘. 내가 직접 넣을게.

[5] 톤과 범위
- 지영 원장이 직접 볼 페이지야. 내 수수료, 수익 배분, 내 다른 사업 이야기는 넣지 마.
- 원장을 평가하거나 훈계하는 투로 쓰지 마. 숫자와 선택지를 보여주고 결정은 원장이 하게 해줘.
- 주민번호, 계좌번호, 집 주소 같은 민감한 개인정보는 어디에도 쓰지 마.

[6] 사실 확인
- 숫자, 날짜, 가격, 법과 제도, 고유명사는 지어내지 말고 실제로 검색해서 확인한 것만 써줘.
- 확인이 안 되면 그냥 '확인 필요'라고 적어. 그럴듯하게 채우지 마.
- 링크는 실제로 열리는 것만. 검색어를 URL에 끼워넣은 가짜 링크는 금지.
- 출처가 있으면 페이지 안에 작게 남겨줘.

[7] 다 되면
공유 링크 하나와 짧은 요약만 줘. 작업 중계는 필요 없어.
내가 결정해야 할 게 있으면 그것만 짧게 물어봐.</pre>
</div>

<h2>원장에게 먼저 물어볼 것</h2>
<div class="card gold">
  <p style="margin:0 0 8px">프롬프트를 돌리기 전에 이 네 가지를 받아두시면 페이지가 훨씬 단단해집니다. 녹음에 없을 가능성이 높은 것들입니다.</p>
  <ul class="list">
    <li><div class="t">월 매출과 월 순이익, 그리고 본인이 가져가는 돈</div><div class="m">세 개가 다 다릅니다. 역산의 출발점이라 이게 없으면 목표 숫자가 공중에 뜹니다</div></li>
    <li><div class="t">성북구 어디쯤, 몇 평대를 생각하는지</div><div class="m">'고급 주택'만으로는 가격을 못 찾습니다. 동네와 평형이 있어야 실거래가를 뒤질 수 있습니다</div></li>
    <li><div class="t">꼬마빌딩은 사는 것인지 짓는 것인지</div><div class="m">매입과 신축은 금액이 완전히 다릅니다. 3층을 다 쓸 건지 일부는 임대할 건지도</div></li>
    <li><div class="t">맥라렌 모델명</div><div class="m">'스파이더'는 오픈카 라인업 이름이라 모델에 따라 가격 차이가 큽니다</div></li>
  </ul>
  <div class="note">그리고 이 페이지를 만드는 목적도 한 번 정하고 가세요 — <b>원장을 설득하려는 것인지, 원장이 스스로 보면서 쓰는 것인지</b>에 따라 톤이 달라집니다. 전자면 '지금 이대로면 몇 년'이 들어가야 하고, 후자면 '이번 달에 뭘 바꾸면 되는지'가 앞에 와야 합니다.</div>
</div>

<div class="src" style="margin-top:14px">근거: 2026-10-07 루크 구두(지영 원장의 세 가지 목표 — 성북구 고급 주택, 3층 키티티바이지영 건물, 맥라렌) · 플라우드 녹음 제목 4건(2026-09-04, 09-08, 09-19, 09-26) · luke-1b 페이지 제작 규칙. <b>목표 가격대, 원장의 현재 매출, 모델명은 아직 확인되지 않았습니다.</b> 저작권 관련 판단은 공개 게시를 전제로 한 일반적인 주의이며 법률 자문이 아닙니다.</div>

<script>
document.querySelectorAll('.cpy').forEach(function(b){
  b.addEventListener('click', function(){
    var t = document.getElementById(b.getAttribute('data-t')).innerText;
    navigator.clipboard.writeText(t).then(function(){
      var o = b.textContent; b.textContent = '복사됨';
      setTimeout(function(){ b.textContent = o; }, 1500);
    });
  });
});
</script>
"""

# ---------------------------------------------------------------- 크루원 페이지 범용 프롬프트
CREWPROMPT = """
<h1>크루원 사업 구조화 페이지 — 프롬프트</h1>
<p class="note">이미 돌아가는 발행·게시 흐름에 <b>얹기만 하는</b> 짧은 버전입니다. 자료 수집·페이지 구성·사실확인은 기존 방식 그대로 두고, 사람이 늘어날 때 실제로 사고가 나는 세 가지만 넣었습니다 — <b>이름 충돌 · 동시 작업 충돌 · 노출</b>.</p>

<h2>크루원 프로젝트 채팅용</h2>
<div class="card">
  <button class="cpy" data-t="c1" style="font:inherit;font-weight:700;padding:10px 16px;border-radius:10px;border:0;background:var(--ac,#5b8def);color:#fff;cursor:pointer;margin-bottom:10px">프롬프트 복사</button>
  <pre id="c1" style="white-space:pre-wrap;word-break:break-word;font-size:13px;line-height:1.65;margin:0;font-family:inherit">[채워 넣기]
크루원 이름: OOO
슬러그: ooo-slug          (영문 소문자와 하이픈만. 사람을 알아볼 수 있게)
저장소: onecrew-ooo-slug  (슬러그와 같게)
플라우드 검색어: OOO, (상호명), (사업 키워드)

위 사람의 사업 구조화 페이지를 만들어줘.
형식과 구성은 루크의 '내 연봉 10억 만들기'(github.com/Yoo-Mideum/luke-1b)와 같게,
자료는 플라우드 녹음과 기존 상담 기록에서 모아줘. 본인에게 공유할 페이지야.

[1] 이름 — 이것만 어기면 다른 사람 작업과 부딪혀
- 슬러그는 위에 적은 것만 써. 네가 임의로 줄이거나 바꾸지 마.
- 같은 슬러그를 저장소 이름, 폴더 이름, 페이지 주소에 전부 똑같이 써줘.
- site, page, new, test, temp, crew1 같은 일반 명사 단독은 쓰지 마.
- 만들기 전에 Yoo-Mideum 계정에 같은 이름의 저장소나 폴더가 이미 있는지 확인해줘.
  있으면 멈추고 나에게 물어봐. 절대 덮어쓰지 마.
- 저장소 생성과 Pages 켜기는 내가 직접 할게. 필요하면 알려줘.

[2] 배포 — 다른 세션이 같은 저장소를 건드릴 수 있어
- 작업을 시작할 때와 push 직전에 git pull --rebase 를 꼭 해줘.
- 충돌이 나면 build.py만 수동으로 합치고 나머지 HTML은 다시 빌드해서 풀어줘.
- 기기 인증(device code) 방식은 이 환경에서 막혀 있으니 시도하지 마.
  push가 403이면 우회하지 말고 바로 알려줘. 내가 권한 열어줄게.
- 배포 후 링크는 ?v=1 처럼 숫자를 붙여서 줘.

[3] 넣지 말 것 — 공개 URL이야
- 다른 크루원의 이름, 매출, 목표는 절대 넣지 마.
- 내 수수료, 수익 배분, 내 다른 사업 이야기도 넣지 마.
- 주민번호, 계좌번호, 집 주소, 전화번호는 어디에도 쓰지 마.
- 남의 사진(매물, 자동차, 브랜드 이미지)을 가져다 올리지 마. 개인 소장과 공개 게시는 달라.
  브랜드 로고나 특정 제품 디자인을 코드로 재현하지도 마.
  분위기가 필요하면 코드로 그린 원본 일러스트로 하고, 목표는 사진보다 숫자로 보여줘.

[4] 나머지는 기존 방식대로
- 페이지 규칙, 자료 수집 방식, 사실 확인 기준은 늘 하던 대로 해줘.
- 확인 안 된 숫자는 '확인 필요'로 남기고 그럴듯하게 채우지 마.

[5] 끝나면
- 공유 링크 하나와 짧은 요약만 줘.
- 마지막에 '원크루 사이트 채팅에 보낼 한 줄'을 적어줘. 크루원 이름과 저장소 이름이 들어가야 해.
- 내가 결정할 게 있으면 그것만 짧게 물어봐.</pre>
</div>

<h2>원크루 사이트 채팅에는</h2>
<div class="card blue">
  <p style="margin:0 0 8px">이미 한 번 해보셨으니 길게 쓸 필요 없습니다. 위 [5]에서 나온 한 줄을 그대로 던지시면 됩니다.</p>
  <button class="cpy" data-t="c2" style="font:inherit;font-weight:700;padding:9px 14px;border-radius:10px;border:0;background:var(--ac,#5b8def);color:#fff;cursor:pointer;margin-bottom:10px">복사</button>
  <pre id="c2" style="white-space:pre-wrap;word-break:break-word;font-size:13px;line-height:1.65;margin:0;font-family:inherit">OOO 사업 구조화 페이지를 onecrew-ooo-slug 에 푸시했어. 원크루 사이트 자료실에 걸어줘.
같은 사람 항목이 이미 있으면 새로 만들지 말고 내용만 갱신해줘.</pre>
</div>

<h2>왜 세 가지만 남겼나</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">이름 — 사람이 늘수록 반드시 겹칩니다</div><div class="m">겹치면 저장소 생성이 실패하거나, 더 나쁘게는 남의 폴더를 덮어씁니다. 슬러그 하나를 정해 전부 같은 값으로 쓰게 하는 게 가장 싼 예방입니다</div></li>
    <li><div class="t">pull --rebase — 세션이 여러 개라 생기는 사고</div><div class="m">오늘도 일정 파일에서 한 번 충돌이 났습니다. 한 줄이면 막힙니다</div></li>
    <li class="big"><div class="t">노출 — 깃허브 페이지는 주소를 알면 누구나 봅니다</div><div class="m">크루원끼리 서로의 매출이 보이는 건 되돌릴 수 없는 사고입니다. 로그인 뒤로 숨기려면 원크루 사이트 4단계가 먼저 끝나야 합니다</div></li>
  </ul>
  <div class="note">자료 수집·페이지 구성·사실확인은 이미 하시던 방식이 있으니 프롬프트에서 뺐습니다. 지시가 길수록 기존 방식과 충돌해서 오히려 결과가 나빠집니다.</div>
</div>

<div class="src" style="margin-top:14px">근거: 2026-10-07 루크 구두(크루원·원크루 페이지 동기화는 이미 한 번 해본 상태, 저장소·페이지 이름 충돌 주의, 개인 프로젝트 채팅에서 발행·푸시 → 원크루 사이트 채팅에서 게시하는 흐름) · luke-1b 배포 규칙 · 2026-10-07 작업 중 실제 발생한 git 충돌 1건.</div>

<script>
document.querySelectorAll('.cpy').forEach(function(b){
  b.addEventListener('click', function(){
    var t = document.getElementById(b.getAttribute('data-t')).innerText;
    navigator.clipboard.writeText(t).then(function(){
      var o = b.textContent; b.textContent = '복사됨';
      setTimeout(function(){ b.textContent = o; }, 1500);
    });
  });
});
</script>
"""
# ---------------------------------------------------------------- 신용점수 KCB NICE
CREDIT = """
<h1>신용점수 — KCB 622 / NICE 750</h1>
<p class="note">낮은 편입니다. 다만 두 점수를 평균 내서 볼 게 아니라 <b>KCB 622 하나만 문제</b>입니다. NICE 750은 보통 수준이고, 농협 카드가 거절된 것도 KCB 쪽에서 걸린 것으로 보입니다.</p>

<h2>지금 위치</h2>
<div class="card red">
  <div class="wrapx">
  <table>
    <thead><tr><th>구분</th><th>점수</th><th>등급 환산</th><th>위치</th></tr></thead>
    <tbody>
      <tr><td>NICE</td><td class="num">750</td><td>5등급 (750~804)</td><td>중신용 · 보통</td></tr>
      <tr><td><b>KCB(올크레딧)</b></td><td class="num"><b>622</b></td><td><b>7등급 (530~629)</b></td><td><b>저신용 구간 진입</b></td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:12px 0 0">금융위 등급 환산 기준으로 <b>7등급은 아래에서 약 14% 안에 들어가는 구간</b>입니다. NICE 750은 흔한 점수인데 KCB 622는 흔하지 않습니다. <b>128점 차이는 단순 기관 차이로 설명되는 폭이 아닙니다.</b></p>
  <div class="note">참고 — NICE 750은 하필 5등급의 <b>맨 아래 칸(750점이 시작점)</b>입니다. 1점만 떨어지면 6등급으로 내려갑니다. 올랐다고 안심할 자리가 아닙니다.</div>
</div>

<h2>왜 128점이 벌어졌나</h2>
<div class="card gold">
  <p style="margin:0 0 10px">두 회사가 보는 항목의 <b>비중이 다릅니다.</b></p>
  <div class="wrapx">
  <table>
    <thead><tr><th>평가 항목</th><th>KCB</th><th>NICE</th></tr></thead>
    <tbody>
      <tr><td><b>신용거래형태</b> (어디서 어떤 식으로 빌렸나)</td><td class="num"><b>38%</b></td><td class="num">30%</td></tr>
      <tr><td>부채수준</td><td class="num">24%</td><td class="num">26%</td></tr>
      <tr><td>상환이력 (연체했나)</td><td class="num">21%</td><td class="num">31%</td></tr>
      <tr><td>신용거래기간</td><td class="num">9%</td><td class="num">13.3%</td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:12px 0 0"><b>해석은 하나로 모입니다.</b> NICE가 750으로 버티는 건 <b>연체가 없다는 뜻</b>입니다(상환이력 31%가 안 깎였으니까). 그런데 KCB가 622인 건 <b>빌린 방식이 안 좋다는 뜻</b>입니다 — KCB가 38%를 걸어둔 항목이 그겁니다.</p>
  <ul class="list" style="margin-top:10px">
    <li><div class="t">카드 현금서비스 · 카드론</div><div class="m">KCB가 가장 세게 깎는 항목입니다. 한 번 쓰면 금액이 작아도 거래 형태 자체가 기록됩니다</div></li>
    <li><div class="t">2금융권 · 캐피탈 · 저축은행 대출</div><div class="m">같은 금액이어도 1금융권보다 불리하게 들어갑니다</div></li>
    <li class="big"><div class="t">여러 곳에서 동시에 빌린 상태 (다중채무)</div><div class="m">건수가 많을수록 금액과 별개로 깎입니다</div></li>
  </ul>
  <div class="note">연체는 없으신 것으로 보입니다. 그래서 고칠 게 더 명확합니다 — <b>갚는 습관이 아니라 빌린 경로</b>를 정리하는 문제입니다.</div>
</div>

<h2>농협 카드 거절 — 왜 거절인지</h2>
<div class="card">
  <p style="margin:0 0 10px">카드 발급 자격은 카드사 재량이 아니라 <b>금융당국 모범규준으로 하한선이 정해져 있습니다.</b> 아래 둘을 다 넘겨야 합니다.</p>
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">월 가처분소득 50만 원 이상</div></li>
    <li class="big"><div class="t">개인신용평점 <b>상위 누적구성비 93% 이하</b> 또는 장기연체가능성 0.65% 이하</div><div class="m">점수 몇 점이라는 식이 아니라 '전체에서 몇 번째냐'로 끊습니다</div></li>
  </ol>
  <p style="margin:12px 0 0"><b>KCB 622는 이 93% 선에 걸릴 가능성이 높습니다.</b> 7등급 이하가 전체의 약 14%니까, 7등급 중간쯤이면 상위 누적 93%를 넘어갑니다. 확정은 올크레딧에서 본인 비율을 직접 봐야 합니다.</p>
  <p style="margin:10px 0 0">그리고 농협은 <b>NICE와 KCB를 둘 다 참고</b>하는 곳으로 알려져 있습니다. 두 점수가 벌어져 있으면 <b>낮은 쪽이 기준이 됩니다.</b> NICE 750만 보고 판단하면 계속 거절됩니다.</p>
  <div class="note">하한선을 넘겨도 카드사가 따로 보는 항목이 11개 더 있습니다 — 소득 안정성, 직업 안정성, 재산, 금융거래 실적, 연체정보, <b>복수카드 사용</b>, <b>카드대출 과다</b>, <b>대출 다중채무</b>, <b>최근 신용카드 과다발급</b>, 국내인 여부, 연금 수급. 굵게 표시한 네 개가 KCB 622와 같은 원인을 가리킵니다.</div>
</div>

<h2>순서대로 이것만</h2>
<div class="card blue">
  <ol class="tl" style="margin-top:2px">
    <li><div class="t">올크레딧(KCB)에 로그인해 <b>'상위 누적 비율'과 '하락 사유'</b>를 직접 확인</div><div class="m">점수만 보고 추측할 일이 아닙니다. KCB는 무엇 때문에 깎였는지 항목으로 알려줍니다. 이걸 보기 전에는 어디를 고칠지 정할 수 없습니다. <b>본인 조회는 점수에 영향 없습니다</b></div></li>
    <li><div class="t">현금서비스 · 카드론이 남아 있으면 그것부터 정리</div><div class="m">KCB 38% 항목을 직접 건드립니다. 금액이 크지 않아도 효과가 가장 큽니다</div></li>
    <li><div class="t">카드 재신청은 지금 하지 마세요</div><div class="m">심사 항목에 '최근 신용카드 과다발급'이 있습니다. 거절 직후 다른 카드사에 연달아 넣으면 그 자체가 불리하게 쌓입니다</div></li>
    <li><div class="t">비금융정보(통신비 · 건강보험 · 국민연금 성실납부) 제출</div><div class="m">올크레딧과 나이스지키미에서 직접 넣습니다. 다만 <b>누구나 몇 점씩 오르는 건 아닙니다</b> — 개인차가 있고, 위 2번만큼 확실하지 않습니다. 공짜니까 해두는 정도</div></li>
    <li class="big"><div class="t">두 점수를 같이 보되 <b>낮은 쪽을 내 점수로 두고</b> 관리</div><div class="m">NICE가 올라도 KCB가 7등급이면 KCB를 보는 금융사에서 계속 막힙니다. 국민·카카오뱅크·우리·케이뱅크가 KCB를 보는 쪽으로 알려져 있습니다</div></li>
  </ol>
</div>

<h2>이게 사업 일정과 겹칩니다</h2>
<div class="card accent">
  <p style="margin:0 0 10px">카드 한 장 문제로 끝나지 않습니다. <b>2년 안에 꼬마빌딩 매입</b>을 보고 계시고, 취득세 중과를 피하려면 2027-03-16 이후 잔금이어야 합니다. 그 시점에 담보대출 심사를 받습니다.</p>
  <ul class="list">
    <li><div class="t">법인 담보대출 심사는 <b>대표자 개인 신용도</b>를 봅니다</div><div class="m">특히 자본금 100만 원 · 매출 실적이 얇은 법인은 법인 재무로 심사가 안 되니 대표자 쪽을 더 봅니다. 은행이 보는 건 보통 ① 대표자 소득 ② 대표자 신용도 ③ 법인 당기순이익 세 가지입니다</div></li>
    <li class="big"><div class="t">지금이 고칠 수 있는 유일한 구간입니다</div><div class="m">신용은 몇 달 단위로 움직입니다. 잔금 치를 때 올리려 하면 늦습니다. 2027년 봄까지 1년 반 — 지금 손대면 충분한 시간이고, 내년에 손대면 빠듯합니다</div></li>
  </ul>
  <div class="note">신정현 대표님과 지분을 나눠 '셀러들의 수다'로 가실 거라면, <b>공동 대표 구성 자체가 심사에 쓸 수 있는 카드</b>입니다. 두 사람 중 신용이 나은 쪽을 대표로 세우는 구조도 선택지에 있습니다. 지금 결정할 일은 아니지만 등기 설계할 때 기억해두시면 좋습니다.</div>
</div>

<h2>확인 필요</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">올크레딧 상위 누적 비율 — 93% 안인지 밖인지</div><div class="m">거절 원인이 신용평점인지 다른 항목인지가 여기서 갈립니다</div></li>
    <li><div class="t">현재 남아 있는 현금서비스 · 카드론 · 2금융권 대출 건수와 잔액</div></li>
    <li><div class="t">법인 명의 대출·카드가 대표자 개인 신용에 얹혀 있는지</div><div class="m">대표자 연대보증으로 들어간 법인 채무는 개인 쪽에도 잡힙니다</div></li>
    <li><div class="t">농협이 밝힌 구체적 거절 사유</div><div class="m">카드사에 요청하면 사유 구분을 알려줍니다. 신용평점 때문인지 소득 증빙 때문인지가 다릅니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거 · 2026-10-07 확인: 금융위 신용점수 등급 환산 기준(NICE 5등급 750~804 / 7등급 600~664, KCB 5등급 698~767 / 7등급 530~629, 7등급 이하 약 14%) · KCB·NICE 평가항목 반영비중(KCB 신용거래형태 38%·부채수준 24%·상환이력 21%·신용거래기간 9% / NICE 상환이력 31%·신용거래형태 30%·부채수준 26%·신용거래기간 13.3%)과 은행별 채택 평가사(국민·카카오뱅크·우리·케이뱅크 KCB, 신한 NICE, 농협·기업·토스 양쪽) — 뱅크샐러드 · 신용카드 발급 자격(월 가처분소득 50만원 이상 + 개인신용평점 상위 누적구성비 93% 이하 또는 장기연체가능성 0.65% 이하, 결제능력 심사 11개 항목) — BC카드 신용카드 업무처리 안내 · 비금융정보 제출 효과는 개인차가 있으며 일률적 가점이 아님 · 신설·소규모 법인 담보대출 심사에서 대표자 소득·신용도·법인 당기순이익을 본다는 점 — 한국경제 랜드밸류업. 일부 블로그가 카드 발급 최소선을 KCB 621·NICE 720으로 적고 있으나 <b>공식 기준이 아니어서 쓰지 않았습니다</b>. 본인 상위 누적 비율은 올크레딧에서 직접 확인이 필요합니다.</div>
"""

# ---------------------------------------------------------------- 재정 정리 대환 우선순위
MONEY = """
<h1>재정 정리 — 무엇부터 털어야 하나</h1>
<div class="card red"><p style="margin:0 0 10px"><b>먼저 정정합니다 — 이 시트는 2026년 5월 시점 자료입니다 (10/7 루크 확인).</b> 처음에 저는 탭 이름의 '10월'을 올해 10월로 읽고 '9월 대비 카드 여유가 819만 줄었다, 두 달 더 가면 막힌다'고 썼습니다. <b>그 문장은 틀렸고 지웠습니다.</b> 탭 이름의 월과 실제 시점이 어긋나 있어, 각 숫자가 정확히 어느 달인지는 시트만으로 확정할 수 없습니다.</p><p style="margin:0 0 10px"><b>남는 것과 사라지는 것을 나누면 이렇습니다.</b></p><div class="wrapx"><table><tr><th>살아남는 결론</th><th>무효가 된 결론</th></tr><tr><td>금리 순서 — 19.5% &gt; 17.3% &gt; 16% &gt; 10.62% &gt; 5.79%</td><td>9월→10월 카드 여유 819만 감소 추세</td></tr><tr><td>어떤 <b>종류</b>의 빚이 KCB를 깎는지 (카드사 대출·저축은행·다중채무)</td><td>롯데 한도 290만 하향과 농협 카드 거절이 같은 흐름이라는 해석</td></tr><tr><td>학자금 5.79%는 먼저 갚지 말 것</td><td>월 고정지출 1,012만이라는 현재값</td></tr><tr><td>햇살론 자격·금리 조건</td><td>3개월 계획의 금액 (988만 × 3)</td></tr><tr><td>대환보다 자격 만들기가 먼저라는 순서</td><td>연말 부채 3,600~4,500만 전망</td></tr></table></div><p style="margin:12px 0 0"><b>구조는 그대로 쓰셔도 됩니다. 금액은 쓰지 마세요.</b> 대출 5건의 현재 잔액과 카드 7장의 현재 이용금액만 알려주시면 같은 틀에 넣어 다시 계산하겠습니다. 어제 KCB 622를 보셨고 오늘 농협이 거절했으니, <b>지금 숫자가 5월보다 나빠졌을 가능성이 높고</b> 그렇다면 순서가 달라집니다.</p></div>
<p class="note">아래 금액은 모두 <b>2026년 5월 시점</b>입니다. 시트 내부 계산은 맞습니다 — 시트가 적어둔 '이번달 총지출 ₩10,123,029'와 제 합산이 1원 차이 없이 일치하고, 카드 총이용금액 ₩35,834,331도 맞습니다. 틀린 건 시트가 아니라 제가 읽은 시점입니다.</p>

<h2>두 달 사이에 있었던 일 <small>시점은 미확정</small></h2>
<div class="card">
  <p style="margin:0 0 10px">시트의 연속한 두 탭 사이에 이런 변화가 찍혀 있습니다. <b>언제인지는 확정할 수 없지만 무엇이 일어났는지는 분명합니다.</b></p>
  <div class="wrapx">
  <table>
    <thead><tr><th></th><th>앞 탭</th><th>뒤 탭</th><th>변화</th></tr></thead>
    <tbody>
      <tr><td>카드 총이용금액</td><td class="num">2,918만</td><td class="num">3,583만</td><td class="num"><b>+665만</b></td></tr>
      <tr><td>가능한도 합</td><td class="num">2,532만</td><td class="num">1,713만</td><td class="num"><b>-819만</b></td></tr>
      <tr><td>롯데카드 총한도</td><td class="num">2,820만</td><td class="num">2,530만</td><td class="num"><b>-290만</b></td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:12px 0 0"><b>롯데 한도가 290만 내려간 것은 카드사가 먼저 움직였다는 뜻입니다.</b> 시트에도 '한도 하향 270만'이라고 적어두셨죠. 고객이 요청하지 않은 한도 하향은 보통 카드사가 위험 신호를 봤을 때 나옵니다. 어제 보신 KCB 622와 같은 원인을 가리킵니다 — 다만 <b>이게 최근 일인지, 다섯 달 전 일인지는 확인이 필요합니다.</b></p>
  <div class="note">이 흐름이 지금도 이어지고 있다면 남은 여유가 더 줄었을 겁니다. 반대로 그 뒤에 정리를 하셨다면 나아졌을 수도 있습니다. <b>어느 쪽인지가 대환 순서를 바꿉니다.</b></div>
</div>

<h2>빚의 전체 모습 <small>2026년 5월 기준</small></h2>
<div class="card">
  <p style="margin:0 0 10px"><b>① 원금성 대출</b> — 금리 높은 순</p>
  <div class="wrapx">
  <table>
    <thead><tr><th>항목</th><th>잔액</th><th>금리</th><th>판단</th></tr></thead>
    <tbody>
      <tr><td>현대카드 장기카드대출</td><td class="num">2,166만</td><td class="num"><b>19.50%</b></td><td><b>1순위 — 가장 비싸고 가장 큼</b></td></tr>
      <tr><td>신한저축은행 사잇돌2</td><td class="num">360만</td><td class="num"><b>17.30%</b></td><td><b>즉시 완제 — 작고 비쌈</b></td></tr>
      <tr><td>하나 장기카드대출</td><td class="num">2,000만?</td><td class="num">16%</td><td><b>확인 필요 — 아래 참조</b></td></tr>
      <tr><td>BNK 경남은행</td><td class="num">1,000만</td><td class="num">10.62%</td><td>유지 (5년 균등상환)</td></tr>
      <tr><td>학자금대출</td><td class="num">416만</td><td class="num">5.79%</td><td><b>절대 먼저 갚지 마세요</b></td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:14px 0 10px"><b>② 카드 이용금액</b> — 한도 소진율</p>
  <div class="wrapx">
  <table>
    <thead><tr><th>카드</th><th>이용</th><th>한도</th><th>소진율</th></tr></thead>
    <tbody>
      <tr><td><b>롯데</b></td><td class="num">2,285만</td><td class="num">2,530만</td><td class="num"><b>90%</b></td></tr>
      <tr><td>국민</td><td class="num">137만</td><td class="num">200만</td><td class="num"><b>68%</b></td></tr>
      <tr><td>삼성</td><td class="num">226만</td><td class="num">340만</td><td class="num">66%</td></tr>
      <tr><td>신한</td><td class="num">643만</td><td class="num">1,010만</td><td class="num">64%</td></tr>
      <tr><td>농협</td><td class="num">110만</td><td class="num">200만</td><td class="num">55%</td></tr>
      <tr><td>현대</td><td class="num">113만</td><td class="num">300만</td><td class="num">38%</td></tr>
      <tr><td>하나</td><td class="num">69만</td><td class="num">780만</td><td class="num">9%</td></tr>
      <tr><td><b>합계</b></td><td class="num"><b>3,583만</b></td><td class="num"><b>5,360만</b></td><td class="num"><b>67%</b></td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:14px 0 0"><b>③ 가족</b> — 어머니 2,200~2,500만 (시트에 없음) · 아버지 1,000만 <b>완료</b></p>
  <div class="note">합산하면 <b>금융권 7,525만 + 가족 약 2,350만 = 약 9,900만</b>입니다. 하나 장기카드대출 2,000만이 살아 있으면 <b>약 1억 1,900만</b>. 이 2,000만의 생사가 지금 가장 큰 미지수입니다.</div>
</div>

<h2>어제 보신 KCB 622가 여기서 설명됩니다</h2>
<div class="card gold">
  <p style="margin:0 0 10px">KCB가 38%를 걸어둔 '신용거래형태' 항목에, 지금 상태가 거의 교과서처럼 들어맞습니다.</p>
  <ul class="list">
    <li><div class="t">카드사 장기카드대출 2건 (현대 + 하나)</div><div class="m">KCB가 가장 세게 깎는 종류입니다. 금액도 4,100만대</div></li>
    <li><div class="t">저축은행 대출 1건</div><div class="m">업권 자체가 불리하게 들어갑니다</div></li>
    <li><div class="t">카드 7장 전체 이용률 67%, 롯데는 90%</div><div class="m">부채수준 24% 항목까지 같이 건드립니다</div></li>
    <li class="big"><div class="t">금융사 7곳 이상에 걸친 다중채무</div><div class="m">금액과 별개로 건수만으로 깎입니다</div></li>
  </ul>
  <div class="note">반대로 보면 <b>NICE가 750을 유지하는 건 연체가 한 번도 없다는 뜻</b>입니다. 시트의 상환완료 칸이 거의 다 채워져 있는 게 증거입니다. 갚는 능력은 증명돼 있고, <b>구조만 비싼 상태</b>입니다. 그래서 고칠 수 있습니다.</div>
</div>

<h2>월 고정지출 1,012만 원 — 어디로 나가나 <small>2026년 5월 기준</small></h2>
<div class="card">
  <div class="wrapx">
  <table>
    <thead><tr><th>항목</th><th>월</th><th>비중</th></tr></thead>
    <tbody>
      <tr><td>롯데카드 결제</td><td class="num">240만</td><td class="num">24%</td></tr>
      <tr><td><b>아우디</b></td><td class="num">115만</td><td class="num">11%</td></tr>
      <tr><td><b>보험료</b></td><td class="num">110만</td><td class="num">11%</td></tr>
      <tr><td>신한카드</td><td class="num">102만</td><td class="num">10%</td></tr>
      <tr><td>현대카드 (원리금 포함)</td><td class="num">101만</td><td class="num">10%</td></tr>
      <tr><td>월세 2건 (709호 44 + 테라 55)</td><td class="num">99만</td><td class="num">10%</td></tr>
      <tr><td>관리비 2건 (테라 29 + 스칸센 28)</td><td class="num">58만</td><td class="num">6%</td></tr>
      <tr><td>삼성카드</td><td class="num">56만</td><td class="num">6%</td></tr>
      <tr><td>농협 · KB · 하나 · BNK</td><td class="num">85만</td><td class="num">8%</td></tr>
      <tr><td>신한저축은행</td><td class="num">11만</td><td class="num">1%</td></tr>
      <tr><td>학자금 4건</td><td class="num">10만</td><td class="num">1%</td></tr>
      <tr><td>힐링 부가세</td><td class="num">26만</td><td class="num">3%</td></tr>
      <tr><td><b>합계</b></td><td class="num"><b>1,012만</b></td><td class="num">—</td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:12px 0 0">4개월 평균도 거의 같습니다 — 7월 1,378만 · 8월 924만 · 9월 738만 · 10월 1,012만, <b>평균 1,013만</b>. 월 1,000만이 기준선입니다.</p>
  <div class="note">여기엔 <b>식비·주유·통신 같은 생활비가 빠져 있습니다.</b> 시트는 고정 결제만 담고 있으니, 실제 월 유출은 1,200만 안팎으로 보시는 게 안전합니다.</div>
</div>

<h2>대환 — 순서가 핵심입니다</h2>
<div class="card red">
  <p style="margin:0 0 10px"><b>지금 당장 대환 신청을 하면 거절될 가능성이 높습니다.</b> KCB 622로는 1금융권 대환 심사를 통과하기 어렵고, 농협 카드가 이미 거절됐습니다. 그래서 <b>대환 자격을 만드는 2개월이 대환보다 먼저</b>입니다.</p>
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">10월 — 신한저축은행 360만 완제</div><div class="m">17.3%에 잔액이 360만밖에 안 됩니다. <b>제2금융권 대출 1건이 통째로 사라집니다.</b> 비용 360만으로 KCB 38% 항목을 직접 건드리는 가장 싼 수단입니다. 월 11만도 같이 사라집니다</div></li>
    <li><div class="t">10월 — 남는 628만을 전부 롯데에 상환</div><div class="m">90% → 약 56%. 카드 전체 이용률 67% → 55%. 한도 하향이 더 오는 걸 막는 게 이 단계의 목적입니다</div></li>
    <li><div class="t">11월 — 다시 롯데, 그리고 올크레딧 재조회</div><div class="m">롯데 30%대, 전체 이용률 40%대. 이 시점에 KCB가 움직였는지 확인합니다. 신용은 보통 몇 달 단위로 반응합니다</div></li>
    <li class="big"><div class="t">11~12월 — 현대카드 19.50% 2,166만을 대환 신청</div><div class="m">여기가 본 게임입니다. 2,166만을 10%로 옮기면 <b>연 200만 가까이 절약</b>됩니다. 아래 햇살론 항목 참고</div></li>
  </ol>
  <div class="note"><b>학자금 5.79%는 손대지 마세요.</b> 가장 싼 돈입니다. 월 10만밖에 안 나가는데 이걸 갚으면 19.5%짜리를 그만큼 더 오래 안고 가게 됩니다. 같은 이유로 BNK 10.62%도 지금은 유지입니다.</div>
</div>

<h2>햇살론 — 자격이 맞을 수 있습니다</h2>
<div class="card blue">
  <p style="margin:0 0 10px">2026년 개편된 햇살론 일반보증 조건을 확인했습니다. <b>신용점수 쪽 조건은 지금 상태가 오히려 맞습니다.</b></p>
  <dl class="kv">
    <dt>신용 조건</dt><dd>연소득 3,500만~4,500만이면 <b>개인신용평점 하위 20%(KCB 약 700점 이하)</b> — KCB 622는 충족. 연소득 3,500만 이하면 신용평점 무관</dd>
    <dt>한도</dt><dd>최대 1,500만 원</dd>
    <dt>금리</dt><dd>연 6.0~10.0%</dd>
    <dt>중도상환수수료</dt><dd>면제</dd>
    <dt>용도</dt><dd>고금리 대출 대환 가능</dd>
  </dl>
  <p style="margin:12px 0 0"><b>현대카드 19.50% 중 1,500만을 8%로 옮기면 연 170만 정도가 남습니다.</b> 금리 조건으로 보면 지금 가장 현실적인 카드입니다.</p>
  <div class="note"><b>확인 필요 — 자격의 소득 쪽입니다.</b> 법인 대표가 햇살론 일반보증 대상에 들어가는지, 그리고 대표이사 급여를 어떻게 책정해 두셨는지에 따라 갈립니다. 이건 추측하면 안 되는 부분이라 <b>서민금융진흥원(1397)에 직접 확인</b>하시는 게 맞습니다. 사잇돌2를 이미 쓰고 계시니 상담 이력도 있을 겁니다.</div>
</div>

<h2>아우디와 건강보험료 — 이것도 고칩니다</h2>
<div class="card gold">
  <p style="margin:0 0 12px">이 두 줄을 '줄일 수 있는 고정비 월 225만'으로 적었는데 <b>둘 다 틀렸습니다.</b></p>

  <h3 style="margin:0 0 8px">아우디 월 115만 — 건드리면 손해입니다</h3>
  <p style="margin:0 0 8px">만기가 <b>약 16개월 뒤</b>이고 그때 <b>3,000만 원을 돌려받는</b> 구조라고 하셨습니다. 그러면 계산이 뒤집힙니다.</p>
  <div class="wrapx"><table>
  <tr><td>남은 기간 더 내는 돈 (115만 × 16)</td><td class="num">1,840만</td></tr>
  <tr><td>만기에 돌려받는 돈</td><td class="num">3,000만</td></tr>
  <tr><td><b>차액</b></td><td class="num"><b>+1,160만</b></td></tr>
  </table></div>
  <p style="margin:10px 0 0">월 115만의 상당 부분이 <b>비용이 아니라 묶여 있는 돈</b>이라는 뜻입니다. 중도 해지하면 그 3,000만을 포기하거나 깎이고 위약금까지 붙습니다. <b>끝까지 타시는 게 맞습니다.</b> 처분을 권한 앞 문단은 구조를 모르고 쓴 것이라 지웠습니다.</p>
  <div class="note"><b>오히려 시점이 좋습니다.</b> 16개월 뒤면 2028년 초입니다. 꼬마빌딩을 '빨라야 2년 이내'로 보고 계시고 취득세 중과가 풀리는 건 2027-03-16입니다. <b>자기자본이 필요한 구간에 3,000만이 도착합니다.</b><br><br><b>확인 한 가지</b> — 그 3,000만이 리스·유예할부의 <b>보증금 환급</b>이면 위 계산이 맞습니다. 그런데 만기에 차를 <b>반납하거나 팔아서 받는 값</b>이라면 얘기가 반대가 됩니다. 중고차는 16개월 더 타면 그만큼 감가되니, 그 경우엔 지금 파는 쪽이 유리할 수 있습니다. 계약서의 만기 조항 한 줄만 확인해 주세요.</div>

  <h3 style="margin:18px 0 8px">건강보험료 월 110만 — 이건 줄일 수 있습니다</h3>
  <p style="margin:0 0 8px">생명보험이 아니라 <b>건강보험료</b>라고 하셨습니다. 해지할 수 없는 법정 부담금이지만, <b>기준이 되는 보수월액은 바꿀 수 있습니다.</b></p>
  <p style="margin:0 0 8px">2026년 요율로 역산해 봤습니다. 건강보험 7.19% + 장기요양 0.9448%, 합쳐 보수월액의 약 8.13%입니다. 대표 1인 법인이면 가입자분·사업장분을 결국 본인이 다 내시는 셈이니 110만을 전액으로 보면,</p>
  <div class="wrapx"><table>
  <tr><td>월 110만에 해당하는 보수월액</td><td class="num">약 1,352만</td></tr>
  <tr><td>연 환산</td><td class="num">약 1억 6,200만</td></tr>
  <tr><td>다른 탭의 10만에 해당하는 보수월액</td><td class="num">약 123만</td></tr>
  </table></div>
  <p style="margin:10px 0 0"><b>자본금 100만 원 법인에서 보수월액 1,352만은 앞뒤가 맞지 않습니다.</b> 게다가 바로 앞 탭에는 이 줄이 0원입니다. 그래서 110만은 매달 나가는 돈이 아니라 <b>정산 소급분이 한 번에 부과된 것</b>일 가능성이 높습니다. 어느 쪽인지에 따라 월 고정지출이 1,012만인지 902만인지가 갈립니다.</p>
  <div class="note"><b>매달 110만이 맞다면 보수월액 변경신청으로 줄입니다.</b> 4대보험 연계센터(4insure.or.kr)에서 신청하고, <b>신청한 달의 다음 달부터 적용되며 소급은 안 됩니다.</b> 다음해 6월까지 적용된 뒤 과세자료로 사후정산되니 <b>없어지는 돈이 아니라 시점을 뒤로 미루는 것</b>입니다. 지금처럼 현금이 급한 구간에서는 그것만으로도 의미가 있습니다. 10/1 사업장 이전 신고와 같이 처리하시면 한 번에 끝납니다.</div>
</div>

<h2>그래서 실제로 줄일 수 있는 건</h2>
<div class="card accent">
  <ul class="list">
    <li><div class="t">건강보험료 — 성격 확인 후, 매달이면 보수월액 조정</div><div class="m">최대 월 110만. 다만 사후정산되므로 영구 절감이 아니라 시점 이동입니다</div></li>
    <li class="big"><div class="t">공간 3곳 — 709호 44만 + 테라 55만 + 관리비 58만 = 월 157만</div><div class="m">사업장을 이전하신 참이라 지금이 정리하기 좋은 시점입니다. <b>여기가 실제로 영구히 줄일 수 있는 유일한 큰 줄</b>입니다 — 세 군데가 지금도 다 필요한지가 핵심입니다</div></li>
  </ul>
  <div class="note">아우디는 빠집니다. 대환으로 아끼는 돈보다 큰 고정비를 찾자고 했는데, 실제로 남는 건 <b>공간 157만</b> 하나입니다.</div>
</div>

<h2>들어올 돈으로 계산하면 <small>고정지출은 5월 값이라 재계산 필요</small></h2>
<div class="card">
  <div class="wrapx">
  <table>
    <thead><tr><th></th><th>수입</th><th>고정지출</th><th>여유</th><th>쓸 곳</th></tr></thead>
    <tbody>
      <tr><td>10월</td><td class="num">2,000만</td><td class="num">1,012만</td><td class="num"><b>988만</b></td><td>저축은행 완제 360 + 롯데 628</td></tr>
      <tr><td>11월</td><td class="num">2,000만</td><td class="num">1,012만</td><td class="num"><b>988만</b></td><td>롯데 잔여 + 올크레딧 재조회</td></tr>
      <tr><td>12월</td><td class="num">2,000~3,000만</td><td class="num">1,012만</td><td class="num"><b>988~1,988만</b></td><td>현대카드 19.5% 공략</td></tr>
      <tr><td><b>3개월 누적</b></td><td class="num">6,000~7,000만</td><td class="num">3,036만</td><td class="num"><b>2,964~3,964만</b></td><td></td></tr>
    </tbody>
  </table>
  </div>
  <p style="margin:12px 0 0"><b>이 계산이 맞으면 연말에 금융권 부채가 7,525만 → 약 3,600~4,500만으로 내려갑니다.</b> 1년 반 뒤 꼬마빌딩 담보대출 심사를 생각하면 나쁘지 않은 궤도입니다.</p>
  <div class="note"><b>다만 세 가지가 이 표를 흔듭니다.</b> ① 2,000만이 세전인지 세후인지, 법인 수령인지 개인 수령인지 — 개인으로 받으면 소득세·건강보험이 붙고 법인으로 받으면 개인 부채 상환에 바로 못 씁니다. ② 생활비가 빠져 있어 여유는 988만보다 작습니다. ③ <b>1월 부가세와 5월 종소세</b>가 이 표 밖에 있습니다. 시트에도 '12월에는 2번 납부'라고 적어두셨습니다.</div>
</div>

<h2>1달 안에 수익을 만들고 싶다 — 숫자 기준만</h2>
<div class="card gold">
  <p style="margin:0 0 10px">신정현 대표님 쪽 2,000만은 <b>'느낌'이라고 하셨습니다.</b> 그 돈이 늦어지거나 줄면 이 계획 전체가 멈춥니다. 그래서 자력으로 덮어야 하는 금액을 숫자로 두면 이렇습니다.</p>
  <dl class="kv">
    <dt>생존선</dt><dd>월 <b>1,012만</b> — 고정 결제만. 이걸 못 넘기면 카드로 메우게 되고 이용률이 다시 올라갑니다</dd>
    <dt>현실선</dt><dd>월 <b>1,200만</b> — 생활비 포함</dd>
    <dt>탈출선</dt><dd>월 <b>1,500만</b> — 고정비를 덮고 월 300~500만씩 원금을 깎는 속도</dd>
  </dl>
  <p style="margin:12px 0 0"><b>한 달 안에 현금이 되는 것과 안 되는 것은 성격이 다릅니다.</b> 이미 손에 있는 것 — 수강생 명단, 3PL 창고에 쌓인 재고, 진행 중인 컨설팅 — 은 한 달 안에 현금이 됩니다. 새로 만드는 것 — 구독 사업, 신규 플랫폼 — 은 아무리 빨라도 한 달로는 안 됩니다. <b>지금 필요한 건 신규가 아니라 회수입니다.</b></p>
  <div class="note">구체적으로 어디서 얼마를 뽑을지는 숫자가 더 필요합니다 — 재고 금액, 재구매 가능한 수강생 수, 컨설팅 단가. 말씀해 주시면 월 1,500만이 가능한 조합인지 따로 계산해 드리겠습니다.</div>
</div>

<h2>확인 필요</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">하나 장기카드대출 2,000만 — 살아 있나</div><div class="m">2025년 5월 시트에는 '하나 장기카드대출 2,000만 / 36개월 / 25년 4월 시작 / 16%'로 적혀 있는데, 10월 시트의 대출내역에는 없습니다. 하나카드 총한도는 430만 → 780만으로 오히려 늘었습니다. 상환 완료인지 시트 누락인지에 따라 <b>총부채가 2,000만 달라집니다.</b> 이게 1순위</div></li>
    <li><div class="t">롯데 2,285만의 성격</div><div class="m">시트에 '미확정 금액 / 분할신청'이라고만 적혀 있습니다. 일시불인지 할부인지 리볼빙인지에 따라 수수료율이 전혀 다릅니다. 리볼빙이면 <b>현대카드 19.5%보다 비쌀 수 있어 1순위가 바뀝니다</b></div></li>
    <li><div class="t">핀다 대출 — 시트에 '₩500.00'</div><div class="m">입력 오류로 보입니다. 실제 잔액 확인 필요</div></li>
    <li><div class="t">대출 5건 현재 잔액 · 카드 7장 현재 이용금액</div><div class="m">이게 1순위입니다. 2026년 5월 숫자로는 대환 순서를 확정할 수 없습니다</div></li>
    <li><div class="t">건강보험료 110만 — 매달인지 정산 소급분인지</div><div class="m">매달이면 보수월액이 1,352만으로 신고돼 있다는 뜻이라 조정 대상이고, 소급분이면 월 고정지출이 902만으로 내려갑니다. 고지서 한 장이면 갈립니다</div></li>
    <li><div class="t">아우디 만기 3,000만의 성격 — 보증금 환급인지 차량 반납·처분가인지</div><div class="m">전자면 끝까지 타는 게 맞고, 후자면 지금 파는 쪽이 유리할 수 있습니다. 계약서 만기 조항</div></li>
    <li><div class="t">BNK 금리 — 6.64%인가 10.62%인가</div><div class="m">9월·8월 시트는 6.64%, 10월 시트는 10.62%로 적혀 있습니다. 8/4 연장 때 바뀐 것이라면 10.62%가 맞고, 그러면 우선순위가 학자금보다 위로 올라갑니다</div></li>
    <li><div class="t">어머니 차용금 — 2,200만인지 2,500만인지, 상환 약속이 있는지</div><div class="m">시트에 아예 없습니다. 금리가 없으니 숫자상으로는 후순위지만, 금융 상환과 별도로 시점을 정해두시는 게 좋습니다</div></li>
    <li><div class="t">신정현 대표님 입금 — 계약·일정·세전/세후, 법인 수령인지 개인 수령인지</div></li>
    <li><div class="t">햇살론 일반보증에 법인 대표가 해당되는지 (서민금융진흥원 1397)</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거 · 재정 수치는 2026-10-07 공유된 루크 본인 재정 시트(10월·09월·08월·07월·2025년 5월 탭, 카드 이용금액은 10/02 기준)에서 직접 합산. 월 고정지출 합계 ₩10,123,029는 시트의 '이번달 총지출' 값과 일치. 어머니 차용금 2,200~2,500만과 아버지 1,000만 완제는 2026-10-07 루크 구두(시트 미반영). 신정현 대표님 경유 10~12월 입금은 루크 표현 그대로 '느낌' 단계로 확정 아님. · <b>2026-10-07 루크 구두 정정</b>: 공유된 시트는 2026년 5월 시점 자료이며 최신본이 아님(탭 이름의 월과 실제 시점이 어긋나 각 수치의 월을 확정할 수 없음). '보험료' 줄은 건강보험료. 아우디는 약 16개월 뒤 만기에 3,000만 원을 돌려받는 구조. · 2026-10-07 확인: 2026년도 건강보험료율 7.19%(보수월액 기준, 가입자·사용자 각 50% 부담), 장기요양보험료율 0.9448% — 국민건강보험공단 2026년도 보험료율 인상 안내. 보수월액 1,352만은 110만을 전액 부담으로 보고 합산요율 8.13%로 역산한 <b>추정치이며 공단 고지 금액이 아님</b>. 보수월액 변경신청은 4대보험 연계센터에서 하고 신청일이 속한 달의 다음 달부터 적용·소급 불가, 다음해 6월까지 적용 후 과세자료로 사후정산 — 택슬리 4대보험 보수월액 변경신청 안내. · 2026-10-07 확인: 2026년 개편 햇살론 일반보증 — 연소득 3,500만 이하는 신용평점 무관, 3,500만~4,500만은 개인신용평점 하위 20%(KCB 약 700점 이하), 한도 최대 1,500만 원, 금리 연 6.0~10.0%, 중도상환수수료 면제, 고금리 대출 대환 용도 사용 가능 / 사잇돌2는 사업소득자 기준 사업 4개월 이상·연소득 600만 원 이상, 한도 최대 3,000만 원, 금리 연 8.9~19.9% — 폴리시노트 2026 서민금융 대개편 비교. 햇살론 일반보증에 <b>법인 대표가 해당되는지는 확인되지 않았습니다</b>. KCB·NICE 평가 비중과 카드 발급 기준은 <a href="../credit/">신용점수 페이지</a>의 근거와 같습니다.</div>
"""

# ---------------------------------------------------------------- 등기 서류 준비
PREP = """
<h1>등기 변경 — 준비물 체크리스트</h1>
<p class="note">서류는 전부 만들어 뒀습니다 — <a href="../registry-forms/"><b>등기 서류 — 다 만들어 뒀습니다</b></a>에 전부 넣어 두었습니다. 10/1 이전이니 <b>본점이전등기 기한은 10/15</b>입니다. 그런데 금요일(10/9)은 한글날이라 <b>주민센터·등기소가 쉽니다.</b> 그래서 금요일에 할 수 있는 것과 연휴 끝나고 해야 하는 것을 갈라 놨습니다.</p>

<div class="card red">
  <p style="margin:0 0 10px"><b>먼저 — 금요일에는 관공서 서류를 못 뗍니다.</b></p>
  <ul class="list">
    <li><div class="t">개인 인감증명서 — 주민센터 창구만 (600원)</div><div class="m">무인발급기로는 <b>개인 인감증명서가 발급되지 않습니다.</b> 정부24 온라인은 2024-09-30부터 무료로 열렸지만 <b>'일반용' 일부만</b>이고 등기·금융 제출용은 제한됩니다. 등기 제출용은 창구가 안전합니다</div></li>
    <li><div class="t">법인인감증명서 — 인터넷 발급 자체가 없습니다</div><div class="m">무인발급기(법인인감카드 + 비밀번호, 1,000원)나 등기소 창구(1,200원 / 인터넷 예약 1,100원)뿐이고, 둘 다 통상 <b>평일 9~18시</b>입니다</div></li>
  </ul>
  <p style="margin:12px 0 0"><b>남은 평일은 10/12(월)~10/15(목) 나흘입니다.</b> 금요일에 서류 작성과 정관 확인을 끝내 두면, 연휴 뒤에는 떼고 접수만 하면 됩니다. 그게 지금 할 수 있는 최선입니다.</p>
</div>

<h2>이번 등기에 들어가는 것</h2>
<div class="card accent">
  <div class="wrapx"><table>
  <tr><th>항목</th><th>필요한 결의</th><th>정관 변경</th></tr>
  <tr><td><b>본점이전</b> (구리 → 구리, 관내)</td><td>이사결정서<br><small>이사 1명이라 이사회 불요</small></td><td>원칙적으로 불필요<br><small>단 아래 확인</small></td></tr>
  <tr><td><b>상호변경</b> 힐링디어스 → 셀러들의 수다</td><td>주주총회 <b>특별결의</b></td><td><b>필요</b></td></tr>
  <tr><td><b>이사 선임</b> 신정현 대표님</td><td>주주총회 보통결의</td><td>불필요</td></tr>
  <tr><td><b>목적 추가</b> 교육업 · 창고업</td><td>주주총회 <b>특별결의</b></td><td><b>필요</b></td></tr>
  <tr><td>공고방법 변경 <span class="tag">선택</span></td><td>주주총회 <b>특별결의</b></td><td><b>필요</b></td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>루크님이 지분 100%라 주주총회가 간단합니다.</b> 자본금 10억 미만 소규모 회사는 <b>의사록 공증이 면제</b>되고 <b>주주 전원 서면결의서</b>로 갈음할 수 있습니다. 주주가 한 명이니 루크님 서명 하나로 끝납니다.</p>
  <div class="note"><b>공고방법은 지금 같이 하시는 걸 권합니다.</b> 등기부상 공고방법이 '수원시 내에서 발행하는 일간 경기신문'인데 본점은 구리입니다. 나중에 증자나 합병처럼 공고가 필요한 일이 생기면 수원 신문에 광고를 내야 합니다. 어차피 정관을 여는 등기이니 이번에 홈페이지 공고로 바꿔 두면 그 비용이 통째로 없어집니다.</div>
</div>

<h2>이번 등기에 안 들어가는 것 — 지분 23%</h2>
<div class="card gold">
  <p style="margin:0 0 10px"><b>신정현 대표님 지분 23%는 등기사항이 아닙니다.</b> 주주는 등기부에 올라가지 않습니다. 등기부에 올라가는 건 '이사 신정현'이라는 직위뿐이고, 지분은 <b>주주명부</b>에서 움직입니다. 그래서 금요일 서류 준비에서 분리하셔야 합니다.</p>
  <ul class="list">
    <li><div class="t">주식 양도로 준다면 — 등기와 무관</div><div class="m">주식양수도계약서 + 주주명부 변경 + 양도소득세 신고. 등기소에 갈 일이 없습니다. 루크님이 100%니까 본인 주식 일부를 넘기는 것이고, <b>액면가와 양도가액 차이에서 세금이 생깁니다</b></div></li>
    <li class="big"><div class="t">증자(신주 발행)로 준다면 — 정관을 먼저 고쳐야 합니다</div><div class="m">등기부상 <b>발행할 주식의 총수 200주가 전부 발행</b>돼 있습니다. 새로 찍을 주식이 없으니 정관의 '발행할 주식의 총수'를 먼저 올려야 하고, 그건 <b>주주총회 특별결의 + 정관변경 등기</b>입니다. 그 다음에 증자등기를 또 합니다 — 2단계입니다</div></li>
  </ul>
  <div class="note"><b>어느 쪽으로 가실지 정하지 않았다면, 이번 등기에는 넣지 마세요.</b> 본점이전 기한(10/15)에 맞춰 네 건을 먼저 끝내고, 지분은 따로 처리하는 쪽이 안전합니다. 다만 <b>'발행할 주식의 총수'를 이번에 미리 넉넉히 올려 두면</b> 나중에 증자할 때 등기를 한 번만 하면 됩니다 — 어차피 정관을 여니까요.</div>
</div>

<h2>금요일에 할 수 있는 것 <small>집·사무실에서</small></h2>
<div class="card blue">
  <ol class="tl" style="margin-top:2px">
    <li class="big"><div class="t">정관 원본 찾기 — <b>제일 중요합니다</b></div><div class="m">본점 조항이 <b>'경기도 구리시'까지만</b> 적혀 있으면 이사결정서로 끝납니다. <b>번지까지</b> 적혀 있으면 정관 변경이 되고 주주총회 특별결의가 필요합니다. 어차피 상호·목적 때문에 특별결의를 하실 거라 절차는 같지만, <b>개정 정관에 새 주소를 넣어야 하는지가 갈립니다.</b> 이것만 확인되면 나머지 서류가 한 번에 확정됩니다</div></li>
    <li><div class="t">'셀러들의 수다' 상호 중복 확인</div><div class="m">인터넷등기소 법인 상호검색은 24시간 됩니다. <b>같은 관할(의정부지방법원 남양주지원) 안에 동일 상호가 있으면 등기가 반려됩니다.</b> 유사 상호도 같이 보세요</div></li>
    <li><div class="t">서류 작성 — 공증이 없으니 전부 집에서 됩니다</div><div class="m">주주 전원 서면결의서(상호·목적·공고방법·이사 선임) · 이사결정서(본점이전) · 개정 정관 · 주주명부 · 주식회사변경등기신청서 · 신정현 대표님 취임승낙서</div></li>
    <li><div class="t">신정현 대표님께 준비물 전달</div><div class="m">여기가 병목입니다. 본인만 발급받을 수 있는 서류가 있어서 <b>연휴 중에 미리 말해 두셔야 10/12에 움직입니다.</b> 아래 목록 그대로 보내시면 됩니다</div></li>
    <li><div class="t">법인인감카드 위치 확인</div><div class="m">이게 없으면 무인발급기도 등기소 창구도 안 됩니다. 분실했으면 재발급부터 해야 하니 <b>금요일에 있는지 확인</b>해 두세요</div></li>
  </ol>
</div>

<h2>신정현 대표님께 보낼 목록</h2>
<div class="card">
  <p style="margin:0 0 10px">이사로 등기되는 분이라 <b>본인이 직접 준비해야 하는 것</b>이 있습니다. 그대로 복사해 보내시면 됩니다.</p>
  <div class="card" style="background:rgba(127,127,127,.08);margin:0">
  <ul class="list">
    <li><div class="t">개인 인감증명서 1부</div><div class="m">주민센터 창구. 무인발급기로는 안 됩니다</div></li>
    <li><div class="t">개인 인감도장</div><div class="m">인감증명서와 같은 도장이어야 합니다. 인감 미신고 상태면 신고부터 해야 하는데 그건 본인이 직접 방문해야 합니다</div></li>
    <li><div class="t">주민등록초본 1부</div><div class="m">주소와 주민등록번호가 나오는 것. 정부24 온라인·무인발급기 모두 가능합니다</div></li>
    <li><div class="t">취임승낙서에 서명 + 인감 날인</div><div class="m">서식은 루크님이 만들어 드리면 됩니다</div></li>
  </ul>
  </div>
  <div class="note"><b>인감을 신고해 두지 않았을 가능성을 먼저 물어보세요.</b> 인감 신고는 온라인이 안 되고 대리도 안 돼서, 10/12에 주민센터부터 가야 하는 경우가 생깁니다. 그러면 기한이 빡빡해집니다. 대안으로 <b>본인서명사실확인서</b>가 인감증명서를 대체할 수 있는지 등기소에 확인해 두시면 보험이 됩니다 — 그건 수수료가 2028-12-31까지 면제입니다.</div>
</div>

<h2>연휴 끝나고 — 10/12(월)부터</h2>
<div class="card">
  <ol class="tl" style="margin-top:2px">
    <li><div class="t">법인인감증명서 1~2부</div><div class="m">무인발급기(법인인감카드+비밀번호, 1,000원) 또는 남양주지원 등기과 창구(1,200원). 인터넷 예약하면 1,100원이고 <b>예약한 등기소에서만 수령</b>됩니다</div></li>
    <li><div class="t">루크님 개인 인감증명서 1부 + 인감도장</div><div class="m">주민센터 600원. 주주 겸 이사라 서면결의서와 신청서 양쪽에 들어갑니다</div></li>
    <li><div class="t">등록면허세 납부 — WETAX</div><div class="m">서울이 아니니 <b>WETAX</b>입니다. 본점이전은 112,500원, 상호·목적·임원 같은 '그 밖의 등기'는 건당 40,200원 + 지방교육세 20% 기준입니다. <b>금액은 WETAX가 계산해 주는 값을 따르시면 됩니다</b> — 아래 확인 필요 참고</div></li>
    <li><div class="t">등기신청수수료</div><div class="m">전자 6,000원. 방문 접수면 등기소 안 은행에서 납부합니다</div></li>
    <li class="big"><div class="t">남양주지원 등기과 접수 — 늦어도 10/15</div><div class="m">관할은 <b>의정부지방법원 남양주지원 등기과</b>입니다(등기번호 037104). 결과는 보통 2~3일 뒤에 나옵니다</div></li>
  </ol>
</div>

<h2>등기가 끝난 뒤에 따라오는 것</h2>
<div class="card accent">
  <ol class="tl" style="margin-top:2px">
    <li><div class="t">변경된 등기사항전부증명서 발급</div><div class="m">다음 단계의 필수 첨부입니다</div></li>
    <li class="big"><div class="t">사업자등록 정정 — 구리세무서</div><div class="m">10/7에 받으신 취하 통지가 이것 때문이었습니다. <b>등기가 끝나야 낼 서류가 나옵니다.</b> 부가가치세법 제8조⑧에 따라 지체 없이</div></li>
    <li><div class="t">법인인감 재제작 + 개인(改印)신고</div><div class="m">법인인감에 상호가 새겨져 있으면 '셀러들의 수다'로 다시 만들어 등기소에 신고해야 합니다. <b>그 전까지는 기존 인감이 유효</b>하니 등기 서류에는 지금 인감을 쓰시면 됩니다</div></li>
    <li><div class="t">통장·카드·계약서 명의</div><div class="m">법인 계좌와 카드의 상호, 거래처 계약서, 세금계산서 발행 정보. 거래처가 많지 않으니 한 번에 정리하기 좋은 시점입니다</div></li>
  </ol>
</div>

<h2>확인 필요</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">정관의 본점 조항 — '구리시'까지인가 번지까지인가</div><div class="m">금요일 1순위. 이것만으로 개정 정관 문안이 정해집니다</div></li>
    <li><div class="t">신정현 대표님 인감 신고 여부</div><div class="m">미신고면 10/12에 주민센터부터 — 일정이 하루 밀립니다</div></li>
    <li><div class="t">등록면허세 중과 여부 — 112,500원인가 337,500원인가</div><div class="m">구리시는 과밀억제권역이지만 중과(3배) 대상은 '대도시 <b>안으로의</b> 전입'입니다. 구리 안에서 옮기는 관내이전은 전입이 아니라 중과 제외로 보는 것이 일반적이나, <b>제가 확인하지 못했습니다.</b> WETAX에서 계산되는 금액을 따르시고, 애매하면 구리시청 세무과에 물어보세요. 차이는 22만 5천 원이라 일정을 흔들 금액은 아닙니다</div></li>
    <li><div class="t">목적에 넣을 업종 문구</div><div class="m">교육업·창고업을 어떤 문구로 넣을지. 참고로 <b>지방세법 시행령 제26조①의 취득세 중과 제외 업종에 창고업·물류터미널은 들어가고 교육업은 들어가지 않습니다</b> — 꼬마빌딩 매입 때 영향이 있으니 문구를 넉넉히 적어 두는 쪽이 낫습니다</div></li>
    <li><div class="t">'발행할 주식의 총수'를 이번에 올려 둘지</div><div class="m">200주 전부 발행 상태입니다. 나중에 증자하려면 어차피 올려야 하니 이번에 같이 할지 결정</div></li>
    <li><div class="t">신정현 대표님을 사내이사로 할지 공동대표이사로 할지</div><div class="m">직위에 따라 서류와 권한이 달라집니다. 공동대표면 거래 때마다 두 사람 인감이 필요해집니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거 · 2026-10-08 확인: 본점이전등기는 실제 이전일로부터 2주 내 신청, 관내이전은 이사회 결의(소규모 법인은 이사결정서로 대체)이며 정관 변경 불필요·관외이전은 주주총회 특별결의와 정관 변경 필요, 등록면허세 112,500원(과밀억제권역 이전 시 337,500원), 자본금 10억 원 미만 법인은 의사록 공증 면제 — 헬프미 법인 본점 이전 등기 안내. 변경등기 공통 서류(변경등기신청서·주주총회 의사록 또는 주주 전원 서면결의서·개정 정관·등록면허세영수필확인서·등기신청수수료 영수증·법인인감증명서·법인인감도장, 대리인 신청 시 위임장)와 '그 밖의 등기' 등록면허세 40,200원 + 지방교육세 8,040원, 등기신청수수료 6,000원, 서울 외 지역은 WETAX 납부 — ZUZU 목적 변경 셀프 등기 안내. 임원 취임등기는 선임 임원당 선임승낙서·개인인감증명서·주민등록등(초)본 각 1부 — ZUZU 임원 취임 셀프 등기 안내. 개인 인감증명서는 무인민원발급기로 발급되지 않고 주민센터 창구 600원이며, 정부24 온라인 무료 발급(2024-09-30 시행)은 일반용 일부로 제한되고 부동산 등기 목적·금융기관 제출용은 제외·본인만 신청 가능, 본인서명사실확인서는 2028-12-31까지 수수료 면제 — 인감증명서 발급 방법 정리. 법인인감증명서는 인터넷 발급이 불가하며 무인발급기(RF 또는 마그네틱 인감카드+비밀번호, 1,000원) 또는 등기소 창구(인터넷 예약 1,100원·미예약 1,200원), 통상 평일 09~18시 운영 — 헬프미 법인인감증명서 발급 방법. 관할 등기소·등기번호·발행주식 총수 200주·공고방법은 2026-10-07 열람한 힐링디어스 주식회사 등기사항전부증명서. <b>등록면허세 중과 적용 여부와 정관의 본점 조항 기재 수준은 확인하지 못했습니다.</b> 이 페이지는 법률 자문이 아닙니다.</div>
"""

# ---------------------------------------------------------------- 등기 서류 양식
FORMS = """
<h1>등기 서류 — 다 만들어 뒀습니다</h1>
<p class="note">출력할 서류 여섯 장은 <b>안내 글자가 한 글자도 없습니다.</b> 열어서 바로 인쇄하고 도장만 찍으면 됩니다. <b>법무사에게 맡기신다면 목록이 달라지니 아래 첫 칸부터 보세요.</b></p>

<h2>법무사에게 맡기면 — 목록이 바뀝니다</h2>
<div class="card red">
  <p style="margin:0 0 10px"><b>줄어듭니다. 대신 하나가 늘어납니다 — 위임장과 법인인감증명서.</b></p>
  <div class="wrapx"><table>
  <tr><th></th><th>법무사에게 줄 것</th><th>누가</th></tr>
  <tr><td>1</td><td><b>등기 위임장</b> — 법무사 양식에 <b>법인인감</b> 날인<small><br>법무사가 양식을 보내줍니다</small></td><td>루크님</td></tr>
  <tr><td>2</td><td><b>법인인감증명서</b> 1~2부<small><br>위임장에 찍은 법인인감을 증명하는 서류<br><b>→ 법무사가 대리 발급 가능</b></small></td><td>법무사<small> 또는 루크님</small></td></tr>
  <tr><td>3</td><td>루크님 개인 인감증명서 1부</td><td>루크님</td></tr>
  <tr><td>4</td><td>루크님 주민등록표 초본 1부</td><td>루크님</td></tr>
  <tr><td>5</td><td>신정현 님 취임승낙서 (인감 날인)</td><td>신정현 님</td></tr>
  <tr><td>6</td><td>신정현 님 개인 인감증명서 1부</td><td>신정현 님</td></tr>
  <tr><td>7</td><td>신정현 님 주민등록표 초본 1부</td><td>신정현 님</td></tr>
  <tr><td>8</td><td><b>결의 내용 확정본</b> — 1번·7번 문서<small><br>목적 41개 · 대표이사 선임 · 정관 전부개정</small></td><td>루크님</td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>법인인감증명서는 법무사가 대신 떼옵니다.</b> 직접 접수할 때는 신청서에 찍은 법인인감을 등기소가 인감대지와 대조하면 끝이라 증명서가 필요 없었습니다. 위임을 하면 <b>위임장의 법인인감이 진짜라는 증명</b>이 필요해지는데, 법인인감증명서는 <b>대리인도 발급받을 수 있습니다</b> — 법인인감이 날인된 위임장과 대리인 신분증만 있으면 됩니다. 그래서 루크님이 할 일은 <b>위임장에 법인인감도장을 찍는 것 하나</b>입니다. 그 도장 하나로 등기 위임과 인감증명서 발급 대리가 같이 처리됩니다.</p><p style="margin:0 0 8px">직접 떼실 경우에만 등기소 창구에서 <b>법인인감도장 + 신분증</b>으로 1,200원입니다(인감카드 불필요). <b>월요일에 한 줄 물어보세요</b> — "법인인감증명서는 그쪽에서 떼주시나요, 제가 떼서 드려야 하나요?"</p>
  <p style="margin:0 0 8px"><b>법무사가 알아서 하는 것</b></p>
  <p style="margin:0">변경등기신청서 작성 · 등록면허세 신고납부 · 접수 · 보정 대응. 그래서 <b>WETAX 납부와 신청서 양식은 루크님이 안 하셔도 됩니다</b> — 다만 "등록면허세도 대신 내주시나요"는 확인하세요. 실비로 청구하는 곳도, 미리 받는 곳도 있습니다.</p>
</div>

<h2>그래서 오늘은 — 출력만, 날인은 월요일</h2>
<div class="card gold">
  <p style="margin:0 0 10px"><b>법무사는 보통 자기 양식으로 다시 씁니다.</b> 그게 정상이고 그 편이 안전합니다 — 그 사무소가 관할 등기소에서 통과시켜 본 양식이니까요. 그러면 루크님이 오늘 인감도장을 찍은 서류는 쓰이지 않게 됩니다.</p>
  <p style="margin:0 0 8px"><b>그래도 출력은 하세요.</b> 제가 만든 1번·7번은 '양식'이 아니라 <b>내용 확정본</b>으로서 값이 있습니다. 이게 없으면 법무사가 월요일 통화에서 이렇게 막힙니다 —</p>
  <ul class="list">
    <li><div class="t">"사업목적 뭐 넣으실래요?"</div><div class="m">41개 전문이 7번 문서에 있습니다. 기존 29개를 등기부 원문 그대로 옮겨 둔 것이 핵심입니다</div></li>
    <li><div class="t">"정관 주세요"</div><div class="m">분실입니다. 전부개정으로 간다는 판단과 완성본이 7번 문서에 있습니다</div></li>
    <li class="big"><div class="t">"신정현 님 사내이사로 올리면 되죠?"</div><div class="m">여기서 <b>"대표이사도 같이 선임해 주세요"</b>라고 말하실 수 있어야 합니다. 상법 제383조 제6항 때문입니다. 법무사가 먼저 짚어주면 좋은 사무소이고, 안 짚으면 루크님이 짚으셔야 합니다</div></li>
  </ul>
  <div class="note"><b>월요일 오전 통화에서 한 줄만 물어보세요</b> — "서류는 제가 내용까지 다 만들어 뒀는데, 그쪽 양식으로 다시 쓰실 건가요, 제 걸 쓰셔도 되나요?" 답에 따라 날인 대상이 정해집니다. <b>인감도장은 그 통화 뒤에 찍으세요.</b></div>
</div>

<h2>오늘 밤에 할 일은 사실 하나입니다</h2>
<div class="card accent">
  <p style="margin:0 0 10px;font-size:16px;font-family:'Gowun Dodum',sans-serif"><b>신정현 님께 메시지 보내기</b></p>
  <p style="margin:0 0 10px">법무사를 쓰든 직접 하든 <b>신정현 님 서류 세 가지는 똑같이 필요하고, 가장 오래 걸립니다.</b> 인감 신고가 안 돼 있으면 본인이 평일에 주민센터에 가야 하고, 그게 월요일 오전을 다 먹습니다.</p>
  <p style="margin:0 0 10px"><a href="https://docs.google.com/document/d/1HStgazPdISVboIepxlCnqx_uqeIdcHs-nsgXQr6b3i0/edit"><b>10. 신정현 님께 보낼 메시지 →</b></a> 복사해서 그대로 보내시고, <a href="https://docs.google.com/document/d/1fVeIL6ApZ_255eJ34vcspLi9IaLNfc733lxUHHpQsLY/edit"><b>4. 취임승낙서</b></a>를 PDF로 같이 보내세요.</p>
  <div class="note">그리고 <b>법무사 사무소에 오늘 밤 메일 한 통</b>을 넣어 두시면 월요일 오전이 빨라집니다 — 등기사항전부증명서와 1번·7번 문서를 PDF로 붙이고 "본점이전·상호변경·목적추가·수권주식수·사내이사 취임·대표이사 선임 여섯 건, 기한 10/16입니다. 월요일 오전에 전화드립니다" 두 줄이면 됩니다.</div>
</div>

<h2>지금 출력할 여섯 장 — 바로 누르세요</h2>
<div class="card accent">
  <p style="margin:0 0 12px"><b>안내 글자를 한 글자도 넣지 않았습니다.</b> 열어서 바로 인쇄하고 도장만 찍으시면 됩니다. 편집할 것 없습니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th>문서</th><th>분량</th><th>찍을 도장</th></tr>
  <tr><td>1</td><td><a href="https://docs.google.com/document/d/1X6D8BlA5qchLLfgK9ae7uyD3JUSD5jzknZI44YYTv4M/edit"><b>주주 전원의 서면결의서</b></a></td><td class="num">4장</td><td><b>개인</b> + 간인</td></tr>
  <tr><td>2</td><td><a href="https://docs.google.com/document/d/1vc-CA7dUbKG-XoLlJZu39L0mCDtYGfOjod959unsh9M/edit"><b>이사결정서 (본점이전)</b></a></td><td class="num">1장</td><td><b>법인</b></td></tr>
  <tr><td>3</td><td><a href="https://docs.google.com/document/d/1Kw2gcbSwQkHEV02ApnajJrWBYTCWv5MYnvcdM6EUbpA/edit"><b>주주명부</b></a></td><td class="num">1장</td><td><b>법인</b></td></tr>
  <tr><td>4</td><td><a href="https://docs.google.com/document/d/1AdOznYRsfb9zblBe8LCjiIVWft3-q5fozYDwUbPoulA/edit"><b>신정현 님께 보낼 것</b></a><small><br>1쪽 취임승낙서 + 준비 안내<br><b>루크님은 출력 안 하셔도 됩니다</b></small></td><td class="num">—</td><td>신정현 본인</td></tr>
  <tr><td>5</td><td><a href="https://docs.google.com/document/d/1aFzYMIRD7iC9z7VlfhrJG03FfopTA3el8Ti25IhVS6A/edit"><b>취임승낙서 — 유믿음</b></a><small><br>대표이사</small></td><td class="num">1장</td><td><b>개인</b></td></tr>
  <tr><td>7</td><td><a href="https://docs.google.com/document/d/1juqQSdMT2BCvAVmp8Pq4ugkQZ5MXAZMvv2CjSLX4_Ss/edit"><b>전부개정 정관</b></a><small><br>목적 41개</small></td><td class="num">5장</td><td><b>법인</b> + 간인</td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>A4 세로, 배율 100%.</b> 각 2부씩 뽑아 두시면 도장이 번져도 다시 안 뽑습니다. 제출은 1부씩입니다.</p>
  <div class="note"><b>같이 열어 둘 문서</b> — <a href="https://docs.google.com/document/d/1qGTITR-dxkSQWbByY00-bG1UnQ5KdlD18Z2HTCP1p6s/edit"><b>9. 날인 위치 + 준비물</b></a>(들고만 보는 문서). 그리고 <b>신정현 님께는 위 4번 링크 하나만</b> 보내시면 됩니다 — 승낙서와 안내가 한 문서에 들어 있고, 다른 서류는 보이지 않습니다.</div>
</div>

<h2>도장은 두 개뿐입니다</h2>
<div class="card">
  <div class="wrapx"><table>
  <tr><th>문서</th><th>어디에</th><th>어느 도장</th></tr>
  <tr><td>1 서면결의서</td><td>마지막 장 '주 주 유 믿 음' 옆 (인)<br><small>+ 장 사이 겹친 자리에 간인</small></td><td><b>루크님 개인 인감</b></td></tr>
  <tr><td>2 이사결정서</td><td>'사 내 이 사 유 믿 음' 옆 (인)</td><td><b>법인인감</b></td></tr>
  <tr><td>3 주주명부</td><td>'사 내 이 사 유 믿 음' 옆 (인)</td><td><b>법인인감</b></td></tr>
  <tr><td>4 취임승낙서 (신정현)</td><td>—</td><td>신정현 님 본인</td></tr>
  <tr><td>5 취임승낙서 (유믿음)</td><td>'성 명 유 믿 음' 옆 (인)</td><td><b>루크님 개인 인감</b></td></tr>
  <tr><td>7 정관</td><td>마지막 장 '대 표 이 사' 옆 (인)<br><small>+ 장 사이 겹친 자리에 간인</small></td><td><b>법인인감</b></td></tr>
  </table></div>
  <p style="margin:14px 0 0"><b>개인 인감은 인감증명서와 같은 그 도장</b>이어야 합니다. 다르면 반려됩니다. <b>법인인감은 현재 '힐링디어스' 것</b>을 씁니다 — 새 상호 도장은 등기가 끝난 뒤에 만듭니다.</p>
  <div class="note"><b>간인 찍는 법.</b> 장을 조금씩 어긋나게 겹쳐 놓고 겹친 경계선 위에 도장을 한 번 찍습니다. 한 번 찍으면 두 장에 반씩 걸립니다. 5장이면 4군데입니다. 스테이플러로 묶고 찍어도 됩니다.</div>
</div>

<h2>준비물 — 루크님</h2>
<div class="card blue">
  <p style="margin:0 0 8px"><b>오늘 (10/9 · 관공서 휴무)</b></p>
  <ul class="list">
    <li><div class="t">서류 6장 출력 → 날인</div></li>
    <li class="big"><div class="t">신정현 님께 10번 문서 전송 + "인감 신고 하신 적 있어요?"</div><div class="m">월요일 일정이 이 한 마디에서 갈립니다</div></li>
    <li><div class="t">상호 중복 확인 — 인터넷등기소 법인 상호검색</div><div class="m">온라인이라 오늘 됩니다. 키프리스에서 상표도 같이</div></li>
    <li><div class="t">사업연도 확인 — 홈택스 법인세 신고내역의 과세기간 한 줄</div><div class="m">작년에 3월에 신고했으면 1/1~12/31 맞습니다</div></li>
    <li><div class="t">변경등기신청서 양식 받아 작성</div></li>
    <li><div class="t">인감카드 사용정지 — 인터넷등기소</div><div class="m">분실하셨으니 정지만 걸어 두세요. 재발급은 등기 후에</div></li>
  </ul>
  <p style="margin:14px 0 8px"><b>월요일 (10/12)</b></p>
  <ul class="list">
    <li><div class="t">개인 인감증명서 1부 — 주민센터 창구 600원</div><div class="m">전국 어디서나. <b>무인발급기 불가.</b> 3개월 이내</div></li>
    <li><div class="t">주민등록표 초본 1부 — 정부24 무료</div><div class="m"><b>주민등록번호 전체 표시</b> 선택 필수</div></li>
    <li><div class="t">등록면허세 납부 — WETAX</div><div class="m">구리시청 세무과에 중과 여부 먼저 확인</div></li>
    <li><div class="t">신정현 님 서류 3종 수령 (원본)</div></li>
    <li><div class="t">법인인감증명서 1~2부 — 등기소 창구 1,200원</div><div class="m">법인인감도장 + 신분증. 인감카드 없어도 됩니다. <b>법무사에게 맡기면 법무사가 대리 발급하므로 루크님은 위임장에 법인인감만 찍으면 됩니다</b></div></li>
    <li class="big"><div class="t">1544-0770 통화 — 네 가지를 한 번에</div><div class="m">① 서면결의서로 가능한지 ② '그 밖의 등기'가 1건인지 4건인지 ③ 본인서명사실확인서를 받아주는지 ④ 신청서를 법인인감 대신 개인 인감으로 낼 수 있는지</div></li>
    <li><div class="t">의정부지방법원 남양주지원 등기과 접수</div><div class="m">수수료 6,000원은 등기소 안 은행에서</div></li>
  </ul>
  <p style="margin:14px 0 8px"><b>들고 갈 것</b></p>
  <p style="margin:0">루크님 개인 인감도장 · 법인인감도장 · 신분증 · 날인 끝낸 서류 6장 · 신정현 님 서류 3종 · 등록면허세 영수필확인서 · 현금 · 클리어파일</p>
</div>

<h2>준비물 — 신정현 님</h2>
<div class="card red">
  <p style="margin:0 0 10px">받아야 할 것 세 가지. <b>전부 원본</b>입니다. 사본·사진은 반려됩니다.</p>
  <ul class="list">
    <li><div class="t">취임승낙서 — 자필 성명 + 인감도장 날인</div><div class="m">내용은 이미 다 채워져 있습니다. 주민번호·주소까지</div></li>
    <li><div class="t">개인 인감증명서 1부</div><div class="m">주민센터 창구 600원 · 본인 · 신분증. <b>무인발급기 불가.</b> 3개월 이내</div></li>
    <li><div class="t">주민등록표 초본 1부</div><div class="m">정부24 무료. <b>주민등록번호 전체 표시</b> 선택 필수</div></li>
  </ul>
  <p style="margin:14px 0 8px"><b>인감 신고를 한 적이 없으면</b></p>
  <p style="margin:0 0 10px">도장과 신분증을 들고 <b>주민등록지 관할 주민센터(남양주시 화도읍)에 본인이 직접</b> 가셔야 합니다. 지문을 찍고 신고한 뒤 그 자리에서 발급됩니다. <b>온라인도 대리도 안 되고 평일만</b> 됩니다.</p>
  <p style="margin:0 0 8px"><b>신정현 님이 안 해도 되는 것</b></p>
  <ul class="list">
    <li><div class="t">법인인감 신고 — 대표권이 없으므로 필요 없습니다</div></li>
    <li><div class="t">등기소 방문 — 루크님이 혼자 접수합니다</div></li>
    <li><div class="t">주소 공개 걱정 — 등기부에 성명과 주민등록번호만 올라갑니다</div><div class="m">상법 제317조 제2항. 주소가 등기되는 것은 대표이사뿐입니다</div></li>
  </ul>
  <div class="note"><b>도장이 없거나 시간이 없으면 본인서명사실확인서.</b> 인감증명서와 같은 효력이고 도장 없이 바로 발급됩니다. 이 경우 승낙서에는 도장 대신 <b>자필 서명</b>만 합니다. 등기소 수용 여부는 1544-0770에 확인하세요.</div>
</div>

<h2>서류를 받으면 네 가지만 대조하세요</h2>
<div class="card">
  <ul class="list">
    <li class="big"><div class="t">초본의 주민등록번호가 990115-1017613과 같은지</div><div class="m">한 자리라도 다르면 나중에 정정등기를 해야 합니다. <b>제가 받은 값이라 반드시 원본과 대조하세요</b></div></li>
    <li><div class="t">인감증명서 발급일이 3개월 이내인지</div></li>
    <li><div class="t">초본의 주민번호 뒷자리가 가려지지 않았는지</div></li>
    <li><div class="t">취임승낙서의 도장이 인감증명서의 도장과 같은지</div></li>
  </ul>
</div>

<h2>먼저 — 신정현 님도 단독으로 회사를 대표하게 됩니다</h2>
<div class="card red">
  <p style="margin:0 0 12px"><b>상법 제383조 제6항</b></p>
  <p style="margin:0 0 12px;padding:12px 14px;border-radius:10px;background:rgba(127,127,127,.09);font-size:14px;line-height:1.75">"자본금 10억 원 미만으로 이사를 1명 또는 2명 둔 회사에서는 <b>각 이사(정관에 따라 대표이사를 정한 경우에는 그 대표이사)가 회사를 대표한다.</b>"</p>
  <p style="margin:0 0 10px">신정현 님을 사내이사로만 올리면 이사가 2명이 됩니다. <b>대표이사를 정하지 않으면 법에 따라 신정현 님도 단독으로 회사를 대표합니다.</b> 회사 명의 계약·대출·법인인감 사용을 혼자 할 수 있게 됩니다.</p>
  <p style="margin:0 0 12px"><b>루크님이 지분 51%를 가지고 있어도 막히지 않습니다.</b> 지분은 주주총회에서 쓰는 힘이고, 대표권은 그것과 별개인 대외적 권한입니다. 51%로는 나중에 해임할 수 있을 뿐, 그 전에 체결된 계약은 유효합니다.</p>
  <p style="margin:0 0 8px"><b>그래서 두 가지를 넣었습니다.</b></p>
  <ul class="list">
    <li><div class="t">1번 서면결의서에 제7호 의안 — 루크님을 대표이사로 선임</div></li>
    <li><div class="t">7번 정관 제25조 — 대표이사 1명만 대표권을 갖고, 대표이사가 아닌 이사는 회사를 대표하지 않는다</div><div class="m">법이 "정관에 따라 대표이사를 정한 경우"라고 열어 둔 문을 쓰는 것입니다</div></li>
  </ul>
  <div class="note"><b>신정현 님께도 이편이 낫습니다.</b> 상법 제317조 제2항은 '회사를 대표할 이사'만 주소까지 등기하고(제9호), 그 밖의 이사는 성명과 주민등록번호만 등기합니다(제8호). 대표이사를 정해 두면 <b>신정현 님 주소는 등기부에 올라가지 않습니다.</b> 등기부는 누구나 열람할 수 있습니다. 각자 대표로 가면 주소가 공개되고 법인인감도 따로 신고해야 합니다.</div>
</div>

<h2>등기부의 수수께끼가 이것으로 풀립니다</h2>
<div class="card">
  <p style="margin:0 0 10px">등기부에 루크님이 <b>'사내이사'인데도 주소가 등기되어 있습니다.</b> 감사 김인숙 님은 성명과 주민등록번호만 있고 주소가 없습니다. 처음엔 왜 다른지 몰랐는데, 제383조 제6항을 보고 나니 설명이 됩니다 — <b>이사가 1명이어서 상법상 대표권이 있었고, 그래서 제317조 제2항 제9호에 따라 주소가 등기된 것</b>입니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th>등기부 기재</th><th>대표권</th></tr>
  <tr><td>사내이사 유믿음</td><td>성명 · 주민번호 · <b>주소</b></td><td><b>있음</b> (이사 1명)</td></tr>
  <tr><td>감사 김인숙</td><td>성명 · 주민번호</td><td>없음</td></tr>
  <tr><td colspan="3" style="padding-top:12px"><b>이번 등기 후</b></td></tr>
  <tr><td><b>대표이사 유믿음</b></td><td>성명 · 주민번호 · <b>주소</b></td><td><b>있음</b></td></tr>
  <tr><td>사내이사 신정현</td><td>성명 · 주민번호</td><td>없음</td></tr>
  <tr><td>감사 김인숙</td><td>성명 · 주민번호</td><td>없음</td></tr>
  </table></div>
  <p style="margin:12px 0 0">직함이 '대표이사'로 바뀌는 것은 <b>덤으로 따라오는 이득</b>입니다. 은행·거래처·입찰이 요구하는 직함이 '대표이사'이고, 지금은 등기부에 '사내이사'로만 적혀 있어 설명이 필요한 상태였습니다.</p>
</div>

<h2>서류 8장 — 폴더에 있습니다</h2>
<div class="card accent">
  <p style="margin:0 0 12px;font-size:15px"><a href="https://drive.google.com/drive/folders/1jxacOh1iNNmkaA0VJmq8D9QFz9g_WucH"><b>힐링디어스 등기 변경 서류 2026-10 →</b></a></p>
  <div class="wrapx"><table>
  <tr><th></th><th>문서</th><th>할 일</th></tr>
  <tr><td>0</td><td>먼저 읽어주세요</td><td>읽기</td></tr>
  <tr><td>1</td><td>주주 전원의 서면결의서<br><small>상호·목적·공고방법·수권주식수·정관개정·사내이사·<b>대표이사</b> — 의안 7개</small></td><td><b>출력·날인</b></td></tr>
  <tr><td>2</td><td>이사결정서<br><small>본점이전. 날짜 10/2</small></td><td><b>출력·날인</b></td></tr>
  <tr><td>3</td><td>주주명부</td><td><b>출력·날인</b></td></tr>
  <tr><td>4</td><td>취임승낙서 <b>2장</b> + 전달 메시지<br><small>신정현 님(사내이사) · 루크님(대표이사)</small></td><td><b>전송 + 출력</b></td></tr>
  <tr><td>6</td><td>정관 원본 찾는 법</td><td>참고<small> (못 찾아도 됩니다)</small></td></tr>
  <tr><td>7</td><td>전부개정 정관 완성본<small> — 목적 41개</small></td><td><b>출력·날인·간인</b></td></tr>
  <tr><td><b>8</b></td><td><b>준비물 전체 체크리스트</b><br><small>도장·증명서·비용·동선·등기 후 10가지</small></td><td><b>이게 핵심</b></td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>8번이 "서류 말고 뭘 더 준비해야 하나"에 대한 답입니다.</b> 아래는 그 요약입니다.</p>
</div>

<h2>등기소에 내는 것 — 12가지</h2>
<div class="card">
  <p style="margin:0 0 10px">전부 <b>원본</b>이어야 합니다. 사본·사진은 반려됩니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th>서류</th><th>부수</th><th>날인</th></tr>
  <tr><td>1</td><td>주식회사 변경등기신청서<small> — 인터넷등기소 양식</small></td><td class="num">1</td><td>법인인감</td></tr>
  <tr><td>2</td><td>주주 전원의 서면결의서<small> (문서 1)</small></td><td class="num">1</td><td>루크 개인인감</td></tr>
  <tr><td>3</td><td>이사결정서<small> (문서 2)</small></td><td class="num">1</td><td>루크</td></tr>
  <tr><td>4</td><td>주주명부<small> (문서 3)</small></td><td class="num">1</td><td>법인인감</td></tr>
  <tr><td>5</td><td>전부개정 정관<small> (문서 7)</small></td><td class="num">1</td><td>법인인감 + 간인</td></tr>
  <tr><td>6</td><td>취임승낙서<small> (문서 4) — 신정현 1장 + 루크 1장</small></td><td class="num">2</td><td>각 본인 인감</td></tr>
  <tr><td>7</td><td><b>신정현 님 개인 인감증명서</b></td><td class="num">1</td><td>—</td></tr>
  <tr><td>8</td><td><b>신정현 님 주민등록표 초본</b></td><td class="num">1</td><td>—</td></tr>
  <tr><td>9</td><td><b>루크님 개인 인감증명서</b></td><td class="num">1</td><td>—</td></tr>
  <tr><td>10</td><td><b>루크님 주민등록표 초본</b></td><td class="num">1</td><td>—</td></tr>
  <tr><td>11</td><td>등록면허세 영수필확인서<small> — WETAX</small></td><td class="num">1</td><td>—</td></tr>
  <tr><td>12</td><td>등기신청수수료 영수필확인서<small> — 등기소 내 은행</small></td><td class="num">1</td><td>—</td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>세 가지 함정</b></p>
  <ul class="list">
    <li><div class="t">초본은 '주민등록번호 전체 표시'로 떼야 합니다</div><div class="m">뒷자리가 가려진 초본은 반려됩니다. 발급할 때 체크하는 항목입니다</div></li>
    <li><div class="t">인감증명서는 발급일로부터 3개월 이내</div><div class="m">상업등기규칙. 초본도 같은 기준으로 보시면 안전합니다</div></li>
    <li class="big"><div class="t">도장과 서명을 섞으면 안 됩니다</div><div class="m">인감 날인 서류에는 <b>인감증명서</b>, 자필 서명 서류에는 <b>본인서명사실확인서</b>. 날인해야 할 곳에 서명만 하면 보정명령이 나옵니다</div></li>
  </ul>
  <div class="note"><b>법인인감증명서는 제출 목록에 없습니다.</b> 본인이 직접 신청하면 신청서에 날인한 법인인감을 등기소가 인감대지와 대조합니다. 다만 실무가 다를 수 있고 <b>어차피 세무서·은행에서 쓰게 되니</b> 1~2부 떼 두시면 헛걸음이 없습니다. <b>대리인이 접수하면 등기 위임장이 추가로 필요합니다.</b></div>
</div>

<h2>들고 갈 물건 — 서류 말고</h2>
<div class="card gold">
  <ul class="list">
    <li class="big"><div class="t">법인인감도장 — 지금 '힐링디어스' 것</div><div class="m">이번 등기까지는 이 도장을 씁니다. 새 상호 도장은 <b>등기가 끝난 뒤</b>에 만듭니다. 미리 만들면 쓸 데가 없습니다</div></li>
    <li><div class="t">루크님 개인 인감도장</div><div class="m">인감증명서와 <b>같은 도장</b>이어야 합니다. 다르면 반려됩니다</div></li>
    <li><div class="t">루크님 신분증</div></li>
    <li><div class="t">법인인감카드 + 비밀번호 — <b>없어도 됩니다</b></div><div class="m">카드는 <b>무인발급기 전용</b>입니다. 등기소 창구에서는 <b>법인인감도장과 신분증</b>만 있으면 법인인감증명서가 나옵니다(1,200원). 어차피 월요일에 등기소에 가시니 거기서 떼시면 됩니다. <b>카드를 분실하셨다면 아래 칸을 보세요</b></div></li>
    <li><div class="t">현금</div><div class="m">등기신청수수료는 등기소 안 은행에서 냅니다</div></li>
    <li><div class="t">클리어파일</div><div class="m">12가지를 순서대로. 창구에서 순서가 섞이면 시간이 갑니다</div></li>
  </ul>
</div>

<h2>법인인감카드를 분실했을 때 — 등기는 안 막힙니다</h2>
<div class="card gold">
  <p style="margin:0 0 10px"><b>이번 등기에 인감카드는 필요하지 않습니다.</b> 카드는 등기소·법원의 <b>무인발급기에서 법인인감증명서를 뽑는 매체</b>이고, 창구에서 빠르게 처리하는 수단입니다. 창구에서는 <b>법인인감도장 또는 인감카드 중 하나</b>만 있으면 되고, 법인인감증명서는 애초에 등기 제출 목록에도 없습니다.</p>
  <div class="wrapx"><table>
  <tr><th>없는 것</th><th>이번 등기</th><th>해야 할 일</th></tr>
  <tr><td>인감카드</td><td class="num"><b>지장 없음</b></td><td>사용정지 → 재발급</td></tr>
  <tr><td><b>법인인감도장</b></td><td class="num"><b>막힙니다</b></td><td>개인(改印)신고 먼저</td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>그래서 먼저 확인할 것은 도장입니다.</b> 설립 때 받은 서류 뭉치(정관·주주명부·등기필증·사업자등록증) 옆에 보통 같이 있습니다. 도장이 있으면 전부 해결됩니다.</p>
  <p style="margin:0 0 8px"><b>카드 분실 — 오늘 할 것</b></p>
  <ul class="list">
    <li class="big"><div class="t">인터넷등기소에서 사용정지 요청</div><div class="m">[신청] → [지원관리] → [인감카드 관리]에서 카드를 찾아 <b>카드번호와 비밀번호를 넣고 정지</b>. <b>이게 급합니다</b> — 분실한 카드로 누군가 법인인감증명서를 뽑으면 회사 명의로 뭐든 할 수 있습니다. 카드번호를 모르시면 월요일에 등기소 창구에서 처리하세요</div></li>
    <li><div class="t">월요일 등기소에서 재발급</div><div class="m">인감카드 재발급신청서(등기소 비치) + <b>법인인감도장</b> + 신분증 + 수수료. 비밀번호 6자리를 새로 등록하고 현장에서 바로 받습니다. 대리인은 법인인감 날인 위임장 추가</div></li>
    <li><div class="t">다만 — 상호가 바뀌니 순서를 생각하세요</div><div class="m">등기가 끝나면 '셀러들의 수다' 법인인감을 새로 만들어 개인(改印)신고를 하게 됩니다. <b>그때 카드도 같이 새로 만드는 게 한 번에 끝납니다.</b> 지금 급하게 재발급하면 2주 뒤에 또 바꿔야 합니다. 나중에 카드를 찾으면 등기소에 반납해야 합니다</div></li>
  </ul>
  <p style="margin:14px 0 8px"><b>도장까지 없을 때 — 개인(改印)신고</b></p>
  <p style="margin:0 0 8px">본점 관할 등기소에서 합니다. 분실한 인감을 폐지하고 새 인감을 등록하는 절차입니다.</p>
  <ul class="list">
    <li><div class="t">개인(改印) 신고서</div><div class="m">등기소 비치 또는 인터넷등기소 양식. <b>대표이사 개인 인감</b>으로 날인합니다</div></li>
    <li><div class="t">대표이사 개인 인감증명서 1부</div><div class="m">발행 3개월 이내. 이번 등기용으로 어차피 떼십니다</div></li>
    <li><div class="t">대표이사 개인 인감도장 + 신분증</div></li>
    <li><div class="t">새 법인인감도장 실물 + 인감대지</div><div class="m">기존 인감과 혼동되지 않게 모양·글꼴을 다르게 하는 편이 좋습니다</div></li>
  </ul>
  <div class="note"><b>도장이 없으면 일정이 꼬일 수 있습니다.</b> 등기부상 상호가 아직 '힐링디어스'라서, 지금 새로 만드는 인감도 <b>'힐링디어스' 이름</b>이어야 합니다. 그러면 2주 뒤 상호변경이 끝난 다음 '셀러들의 수다' 인감을 또 만들어 개인신고를 한 번 더 해야 합니다 — <b>도장 두 번, 신고 두 번</b>입니다. 그래서 <b>변경등기신청서를 법인인감 대신 대표이사 개인 인감으로 낼 수 있는지</b>를 1544-0770에 같이 물어보셔야 합니다. 된다면 개인신고를 등기 후로 미루고 한 번에 끝낼 수 있습니다. <b>저는 이 부분을 확인하지 못했습니다.</b></div>
</div>

<h2>신정현 님이 준비하실 것 — 오늘 꼭 물어볼 한 가지</h2>
<div class="card red">
  <p style="margin:0 0 10px"><a href="https://docs.google.com/document/d/1AdOznYRsfb9zblBe8LCjiIVWft3-q5fozYDwUbPoulA/edit"><b>이 링크 하나만 신정현 님께 보내세요 →</b></a> 1쪽이 취임승낙서, 그 아래가 준비 안내입니다. <b>다른 서류는 들어 있지 않습니다.</b> 요청하는 건 세 가지입니다.</p>
  <ul class="list">
    <li><div class="t">취임승낙서 — 자필 성명 + 인감도장 날인</div><div class="m">내용은 이미 다 채워져 있습니다. 주민번호·주소까지</div></li>
    <li><div class="t">개인 인감증명서 1부</div><div class="m">주민센터 창구 600원. 본인·신분증. <b>무인발급기로는 안 나옵니다</b></div></li>
    <li><div class="t">주민등록표 초본 1부</div><div class="m">정부24 온라인 무료. 주민번호 전체 표시 선택</div></li>
  </ul>
  <p style="margin:14px 0 8px"><b>★ 오늘 꼭 물어보세요 — "인감 신고 하신 적 있으세요?"</b></p>
  <p style="margin:0 0 10px">안 하셨으면 <b>도장과 신분증을 들고 주민등록지 관할 주민센터(남양주시 화도읍)에 본인이 직접</b> 가셔야 합니다. 지문을 찍고 신고한 뒤 그 자리에서 인감증명서가 나옵니다. <b>온라인도 대리도 안 되고 평일만 됩니다.</b> 이게 월요일 일정을 가장 크게 흔드는 변수입니다.</p>
  <div class="note"><b>도장이 없을 때의 탈출구 — 본인서명사실확인서.</b> 인감증명서와 같은 효력이고(본인서명사실 확인 등에 관한 법률), 도장 없이 주민센터에서 바로 발급됩니다. 이 경우 승낙서에는 도장 대신 <b>자필 서명</b>만 합니다. 대리 발급은 안 됩니다. 다만 <b>이번 등기에서 받아주는지는 1544-0770에 확인</b>해야 합니다 — 가능하면 인감증명서가 가장 확실합니다.</div>
</div>

<h2>떼야 하는 증명서 — 어디서, 얼마에</h2>
<div class="card blue">
  <div class="wrapx"><table>
  <tr><th></th><th>어디서</th><th>비용</th></tr>
  <tr><td>개인 인감증명서</td><td>주민센터 창구<br><small>전국 어디서나 · <b>무인발급기 불가</b><br>정부24 온라인은 일반용 일부로 제한</small></td><td class="num">600원</td></tr>
  <tr><td><b>인감 신고·변경</b></td><td><b>주민등록지 관할</b> 주민센터<br><small>본인만 · 도장 + 신분증 + 지문<br><b>대리·온라인 불가</b></small></td><td class="num">—</td></tr>
  <tr><td>주민등록표 초본</td><td>정부24 온라인<br><small>집에서 출력 · 주민번호 전체 표시</small></td><td class="num">무료</td></tr>
  <tr><td>법인인감증명서</td><td>등기소·법원 무인발급기<br><small>법인인감카드 + 비밀번호</small></td><td class="num">1,000원</td></tr>
  <tr><td></td><td>등기소 창구<small> / 인터넷 예약</small></td><td class="num">1,200원<small> / 1,100원</small></td></tr>
  </table></div>
  <div class="note"><b>법인인감증명서는 인터넷 발급이 안 됩니다.</b> 평일 09~18시에 직접 가셔야 합니다. 개인 인감증명서는 반대로 <b>무인발급기가 안 됩니다.</b> 둘을 헷갈려서 헛걸음하는 경우가 많습니다.</div>
</div>

<h2>비용 — 약 19만 원</h2>
<div class="card">
  <div class="wrapx"><table>
  <tr><td>등록면허세 — 본점이전등기</td><td class="num">112,500원</td></tr>
  <tr><td>지방교육세 (20%)</td><td class="num">22,500원</td></tr>
  <tr><td>등록면허세 — 그 밖의 등기<small><br>상호·목적·주식수·임원</small></td><td class="num">40,200원</td></tr>
  <tr><td>지방교육세 (20%)</td><td class="num">8,040원</td></tr>
  <tr><td>등기신청수수료 (창구)</td><td class="num">6,000원</td></tr>
  <tr><td>개인 인감증명서 2부</td><td class="num">1,200원</td></tr>
  <tr><td>법인인감증명서 1부</td><td class="num">1,000원</td></tr>
  <tr><td>주민등록초본 2부</td><td class="num">0원</td></tr>
  <tr><td><b>합계</b></td><td class="num"><b>약 191,500원</b></td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>납부 전에 확인할 두 가지 — 금액이 크게 움직입니다</b></p>
  <ul class="list">
    <li class="big"><div class="t">'그 밖의 등기' 40,200원이 1건인가 4건인가</div><div class="m">상호·목적·주식수·임원을 한 신청서에 묶으면 보통 1건으로 보지만 등기소·지자체 실무가 다릅니다. <b>4건이면 등록면허세가 약 19만 원으로 올라갑니다.</b> 1544-0770에 물어보세요</div></li>
    <li class="big"><div class="t">등록면허세 중과 3배(337,500원) 해당 여부</div><div class="m">구리시는 수도권정비계획법상 <b>과밀억제권역</b>입니다. 그런데 지방세법 제28조 제2항의 중과 요건은 <b>'대도시 밖에 있는 법인의 본점을 대도시로 전입'</b>하는 경우입니다. 구리시 → 구리시는 대도시 <b>안에서의 이동</b>이라 전입이 아니므로 중과 대상이 아닐 것으로 보입니다. 다만 차액이 20만 원을 넘으니 <b>WETAX 납부 전에 구리시청 세무과에</b> 한 줄 물어보세요 — "본점을 구리시 안에서 구리시 안으로 옮기는데 중과 대상입니까?"</div></li>
  </ul>
</div>

<h2>과거 지방세 체납이 있어도 등기는 안 막힙니다</h2>
<div class="card">
  <p style="margin:0 0 10px"><b>등기관이 보는 것은 이번 건의 등록면허세 영수필확인서 하나입니다.</b> 지방세징수법 제5조가 납세증명서를 반드시 내라고 정한 경우는 네 가지뿐입니다 — ① 국가·지자체·정부관리기관에서 대금을 받을 때 ② 지방세 납세의무가 있는 외국인이 출국할 때 ③ 내국인이 해외이주·1년 초과 체류 목적으로 거주목적 여권을 신청할 때 ④ 신탁을 원인으로 부동산 소유권을 수탁자에게 이전하는 등기를 신청할 때. <b>법인 변경등기는 여기에 없습니다.</b></p>
  <p style="margin:0 0 10px">등록면허세는 <b>신고납부</b> 세목이라 WETAX에서 이번 건만 따로 신고하고 결제할 수 있습니다. 과거 체납이 있어도 그 결제가 막히지는 않습니다. 다만 <b>WETAX에 로그인하면 미납·체납 내역이 같이 보입니다</b> — 보이는 것과 같이 내야 하는 것은 다릅니다.</p>
  <p style="margin:14px 0 8px"><b>그래도 이번에 같이 확인하실 이유 두 가지</b></p>
  <ul class="list">
    <li class="big"><div class="t">체납이 있으면 지방세 납세증명서가 안 나옵니다</div><div class="m">납세증명서는 '다른 체납액이 없다'는 증명이라, 징수유예·회생파산 관련이 아닌 체납이 있으면 증명이 안 됩니다. <b>정부지원사업·관급계약·대출 심사에서 바로 막히는 서류</b>입니다. 지원사업을 보고 계시니 이게 등기보다 실질적입니다</div></li>
    <li><div class="t">가산금이 계속 붙고, 오래 가면 법인 예금이 압류됩니다</div></li>
  </ul>
</div>

<h2>지방교육세 단독 체납은 없습니다 — 어디에 붙은 건지가 핵심</h2>
<div class="card gold">
  <p style="margin:0 0 10px"><b>지방교육세는 독립 세목이 아니라 다른 세금에 얹히는 부가세입니다.</b> 취득세·등록면허세·주민세·재산세·자동차세·담배소비세·레저세에 붙습니다. 그래서 "지방교육세를 안 냈다"면 <b>본세를 같이 안 낸 것</b>이고, 어느 본세인지가 금액을 결정합니다.</p>
  <div class="wrapx"><table>
  <tr><th>후보</th><th>가능성</th><th>왜</th></tr>
  <tr><td><b>주민세 사업소분</b></td><td class="num"><b>높음</b></td><td>고지서가 안 오는 <b>신고납부</b> 세목</td></tr>
  <tr><td>과거 등기의 등록면허세</td><td class="num">낮음</td><td>영수필확인서 없이는 등기가 안 됨</td></tr>
  <tr><td>자동차세·재산세</td><td class="num">낮음</td><td>고지서가 날아옴</td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>주민세 사업소분 — 법인이 가장 자주 빠뜨립니다</b></p>
  <ul class="list">
    <li><div class="t">과세기준일 매년 7월 1일, 신고납부 8월 1일~31일</div><div class="m">사업소를 둔 법인은 매출이 0이어도 납세의무자입니다. <b>고지서가 오지 않고 스스로 신고하는 세목</b>이라 모르고 넘어가기 쉽습니다</div></li>
    <li><div class="t">법인 기본세액 5만 / 10만 / 20만 원 — 자본금 규모별</div><div class="m">자본금 100만 원이면 <b>5만 원</b>입니다. 연면적이 330㎡를 넘으면 1㎡당 250원이 더 붙지만 비상주 사무실 1.7㎡는 해당 없습니다</div></li>
    <li><div class="t">여기에 지방교육세가 얹힙니다</div><div class="m">기본세액의 10%, 인구 50만 이상 시는 25%가 적용될 수 있습니다. <b>루크님이 기억하시는 '지방교육세'가 이것일 가능성이 가장 큽니다</b></div></li>
    <li class="big"><div class="t">설립이 2022년 3월이면 2022·2023·2024·2025·2026 다섯 번이 지나갔습니다</div><div class="m">한 해에 5만 원대라 전부 밀려 있어도 <b>원금은 30만 원 안쪽</b>입니다. 가산금이 붙어도 감당 가능한 금액이고, 지금 털어 두면 납세증명서가 깨끗해집니다</div></li>
  </ul>
  <div class="note"><b>관할이 두 곳일 수 있습니다.</b> 등기부상 본점 이력이 남양주시 별내동 → 구리시 갈매동 → 구리시이므로, <b>남양주시 분과 구리시 분이 따로 남아 있을 수 있습니다.</b> WETAX는 전국이 통합 조회되니 한 번에 보입니다(서울만 ETAX 별도).</div>
</div>

<h2>지금 5분 — 체납이 있는지 확인하는 가장 빠른 방법</h2>
<div class="card accent">
  <ul class="list">
    <li class="big"><div class="t">WETAX에서 '지방세 납세증명서' 발급을 시도해 보세요</div><div class="m"><b>나오면 체납 없음, 안 나오면 체납 있음</b>입니다. 미납내역을 하나하나 뒤지는 것보다 빠른 판별법입니다. 법인 로그인에는 법인 공동인증서가 필요합니다</div></li>
    <li><div class="t">안 나오면 WETAX 미납내역 조회로 세목·연도·금액을 확인</div><div class="m">세목이 '주민세 사업소분'이면 위 설명대로입니다</div></li>
    <li><div class="t">월요일 구리시청 세무과 통화에 한 줄 추가</div><div class="m">등록면허세 중과를 물어볼 때 <b>"우리 법인 지방세 체납 있나요? 주민세 사업소분 신고가 빠진 해가 있나요?"</b>를 같이. 남양주시 분이 따로 있으면 남양주시청에도 한 통</div></li>
  </ul>
  <div class="note">이번 등기와는 <b>별개로 처리하시면 됩니다.</b> 등록면허세는 이번 건만 신고·납부하고 접수하시고, 체납은 등기 끝난 뒤에 정리해도 됩니다. 순서를 섞어서 등기 기한(10/16)을 놓치는 것이 훨씬 비쌉니다.</div>
</div>

<h2>남은 확인 하나 — 사업연도</h2>
<div class="card gold">
  <p style="margin:0 0 10px">전부개정 정관 제29조에 <b>매년 1월 1일 ~ 12월 31일</b>로 적었습니다. 등기부에 나오지 않는 항목이라 <b>제가 가장 흔한 값으로 쓴 것</b>입니다.</p>
  <p style="margin:0 0 8px"><b>혼자 1분 안에 확인하는 방법 — 작년에 법인세를 몇 월에 신고했는지만 보세요.</b> 법인세 신고기한은 사업연도 종료일로부터 3개월 이내라서 역산이 됩니다.</p>
  <div class="wrapx"><table>
  <tr><th>신고한 달</th><th>결산일</th><th>사업연도</th></tr>
  <tr><td><b>3월</b></td><td>12월 31일</td><td class="num"><b>1/1~12/31 — 맞습니다</b></td></tr>
  <tr><td>6월</td><td>3월 31일</td><td class="num">4/1~3/31</td></tr>
  <tr><td>9월</td><td>6월 30일</td><td class="num">7/1~6/30</td></tr>
  </table></div>
  <p style="margin:12px 0 0">홈택스 법인세 신고내역을 열면 과세기간이 <b>"2025-01-01 ~ 2025-12-31"</b> 식으로 찍혀 있습니다. 그 한 줄만 보시면 끝입니다. 기장 세무사무소에 한 줄 보내는 것도 같은 속도입니다.</p>
  <div class="note"><b>왜 맞춰야 하나.</b> 실제가 다른데 1/1~12/31로 적으면 이 정관이 '사업연도를 변경한 문서'가 됩니다. 사업연도 변경은 주주총회 특별결의와 세무서 신고가 따로 필요한 별건이라, 신고 없이 정관만 바꾸면 <b>정관과 세무신고가 어긋난 상태로 남습니다.</b> 그러면 정기주주총회 시기(정관상 사업연도 종료 후 3개월 이내)와 재무제표 승인 시점도 실제와 안 맞게 됩니다. <b>등기에는 지장이 없습니다</b> — 등기관은 사업연도를 보지 않습니다. 새로 쓰는 정관에 틀린 한 줄을 영구히 남기지 않기 위한 확인입니다. 다르면 7번 문서 제29조의 날짜만 고치세요.</div>
</div>

<h2>오늘 (10/9 · 한글날 — 관공서 휴무)</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">사업연도 확인</div><div class="m">홈택스 과세기간 한 줄, 또는 세무사무소에 카톡 한 줄</div></li>
    <li class="big"><div class="t">신정현 님께 4번 문서 전송 + "인감 신고 하셨어요?" 확인</div><div class="m">안 하셨으면 월요일 오전이 주민센터로 먼저 갑니다. 오늘 알아야 일정이 안 깨집니다</div></li>
    <li><div class="t">상호 중복 확인 — 인터넷등기소 법인 상호검색</div><div class="m">온라인이라 오늘 됩니다. 같은 관할(의정부지방법원 남양주지원)에 동일 상호가 있으면 등기가 안 됩니다. <b>상표권은 별개입니다</b> — '셀러들의 수다'가 타인의 등록상표면 상호 등기는 되더라도 사용에서 다툼이 생깁니다. 키프리스에서 같이 검색해 두세요</div></li>
    <li><div class="t">문서 1·2·3·7 출력 → 날인</div><div class="m">루크님 개인 인감도장 + 법인인감도장. 정관은 간인까지</div></li>
    <li><div class="t">인터넷등기소에서 변경등기신청서 양식 받아 작성</div></li>
    <li><div class="t">법인인감카드 위치 확인</div></li>
  </ul>
</div>

<h2>월요일 (10/12)</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">주민센터 — 루크님 인감증명서 1부</div><div class="m">600원. 전국 어디서나 됩니다</div></li>
    <li><div class="t">정부24 — 루크님 주민등록초본 1부</div><div class="m">무료. 집에서 출력</div></li>
    <li class="big"><div class="t">1544-0770 통화 — 세 가지를 한 번에</div><div class="m">① 서면결의서로 가능한지 ② '그 밖의 등기' 등록면허세 건수 ③ 본인서명사실확인서 수용 여부 <b>④ 변경등기신청서를 법인인감 대신 대표이사 개인 인감으로 낼 수 있는지</b>(인감도장을 못 찾았을 때를 대비)</div></li>
    <li><div class="t">구리시청 세무과 — 등록면허세 중과 여부</div></li>
    <li><div class="t">WETAX에서 등록면허세 납부 → 영수필확인서 출력</div><div class="m">서울이 아니라 WETAX입니다</div></li>
    <li><div class="t">신정현 님 서류 수령 — 원본</div></li>
    <li><div class="t">법인인감증명서 1~2부</div></li>
    <li><div class="t">의정부지방법원 남양주지원 등기과 접수</div><div class="m">등기신청수수료 6,000원은 등기소 안 은행에서</div></li>
  </ul>
  <div class="note">월요일에 다 못 해도 됩니다. <b>기한은 10/16(금)</b>입니다. 다만 보정명령이 나올 여유를 두려면 월·화 접수가 안전합니다 — 보정은 보통 며칠 안에 고칠 수 있지만, 금요일에 접수했다가 보정이 나오면 기한을 넘깁니다.</div>
</div>

<h2>등기가 끝난 뒤 — 순서가 중요합니다</h2>
<div class="card accent">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">등기사항전부증명서 발급</div><div class="m">새 상호·새 본점·새 임원이 찍힌 것</div></li>
    <li class="big"><span class="tag p0">2</span><div class="t">사업자등록 정정 — 구리세무서, 이전일 10/2로</div><div class="m">이 순서를 지켜야 합니다. <b>등기 → 등기사항전부증명서 → 사업자등록 정정.</b> 10/7에 정정이 취하된 건 등기가 아직 안 돼 있었기 때문입니다. 필요: 등기사항전부증명서, 사업자등록증 원본, 사무실 계약서, 법인인감증명서</div></li>
    <li><span class="tag p0">3</span><div class="t">법인인감 재제작 → 개인(改印)신고</div><div class="m">상호가 바뀌므로 필수입니다. 등기소에 신고한 뒤 새 법인인감증명서를 받으세요</div></li>
    <li class="big"><span class="tag p1">4</span><div class="t">리카 공유오피스에 상호 변경 통지</div><div class="m">놓치기 쉽습니다. 계약서에 <b>"우편물 수취 후 1달 경과 시 폐기"</b> 조항이 있습니다. 사무실 측이 '힐링디어스'만 알고 있으면 <b>'셀러들의 수다' 명의 우편물을 반송하거나 폐기</b>할 수 있습니다. 등기소 보정명령과 세무서 안내가 이 주소로 갑니다</div></li>
    <li><span class="tag p1">5</span><div class="t">4대보험 사업장 소재지·상호 변경</div><div class="m">건강보험 EDI 또는 공단 지사</div></li>
    <li><span class="tag p1">6</span><div class="t">법인 통장·카드 상호 변경 — 은행 방문</div><div class="m">등기사항전부증명서 + 사업자등록증 + 법인인감증명서 + 법인인감도장 + 대표 신분증</div></li>
    <li><span class="tag p1">7</span><div class="t">통신판매업 변경신고 — 구리시청</div><div class="m">목적에 전자상거래 및 통신판매업이 있습니다. 상호·소재지가 바뀌면 변경신고 대상입니다</div></li>
    <li><span class="tag p1">8</span><div class="t">스마트스토어·오픈마켓 사업자 정보 수정</div><div class="m">홈페이지·쇼핑몰의 사업자정보 표시도 같이</div></li>
    <li><span class="tag p1">9</span><div class="t">거래처 통지 + 세금계산서 발행 정보 수정</div></li>
    <li class="big"><span class="tag p2">10</span><div class="t">2027-10-01을 지금 캘린더에 등록</div><div class="m">사무실 계약만료(2027-11-01) 1개월 전. 계약서 위임장에 <b>"연락 부재로 1개월 경과 시 대리인이 세무서에 사업자등록 말소를 위임한다"</b>는 조항에 서명하셨습니다</div></li>
  </ul>
</div>

<h2>이번 등기에 안 들어가는 것</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">지분 51 : 26 : 23</div><div class="m">주주는 등기부에 올라가지 않습니다. 200주로 102 / 52 / 46주가 정확히 나눠지니 <b>양도로 가면 등기소에 갈 일이 없고</b>, 증자로 가면 정수가 안 맞습니다</div></li>
    <li><div class="t">감사 김인숙 님</div><div class="m">변경이 없어 서류에 등장하지 않습니다. 2025.03.16 중임이라 다음 만료는 2028년 3월 전후입니다</div></li>
    <li><div class="t">자본금 100만 원</div><div class="m">이번에 바뀌지 않습니다. 올리는 것은 '발행할 주식의 총수' 한도뿐입니다</div></li>
    <li class="big"><div class="t">취득세 중과 — 등록면허세 중과와 전혀 다른 세금입니다</div><div class="m">설립일 2022-03-16 + 5년 = <b>2027-03-16 이후</b>에 부동산을 사야 유리합니다. 7번 정관의 <b>창고업·물류터미널 운영업</b> 두 줄이 그때 세금을 가릅니다 — 지방세법 시행령 제26조 제1항의 중과 제외 업종에 이 둘은 들어가고 <b>교육업은 안 들어갑니다</b></div></li>
  </ul>
</div>

<h2>2028년 3월을 미리 적어 두세요</h2>
<div class="card">
  <p style="margin:0">루크님과 감사 김인숙 님은 <b>2025.03.16 중임</b>이라 다음 만료가 2028년 3월 전후입니다. 신정현 님은 2026.10.12 취임이라 2029년 10월입니다. <b>만료 시점이 갈라집니다</b> — 2028년 3월에 중임등기를 한 번 더 해야 하고, 그걸 놓치면 상법 제635조에 따라 과태료(500만 원 이하)가 나옵니다. 지금 캘린더에 넣어 두시는 게 가장 쌉니다.</p>
</div>

<div class="src" style="margin-top:14px">근거 · 회사 정보(등기번호 037104 · 등록번호 284111-0371040 · 상호 힐링디어스 주식회사 · 본점 경기도 구리시 갈매순환로 188 제알토 현대클러스터동 제7층 제에이에이07-0009호 · 1주 5,000원 · 발행할 주식의 총수 200주 · 발행주식총수 200주 · 자본금 1,000,000원 · 공고방법 수원시 내에서 발행하는 일간 경기신문 · 목적 29개와 부대사업 일체 · 사내이사 유믿음(주소 등기)과 감사 김인숙(주소 미등기) 2025.03.16 중임 · 회사성립 2022.03.16 · 본점 이력 3회 · 관할 의정부지방법원 남양주지원 등기과)는 <b>2026-10-07 06:17 열람 등기사항전부증명서(말소사항 포함)</b>. 신정현 님 주민등록번호·주소는 2026-10-09 루크님 제공. 새 본점과 계약 조건은 리카 공유오피스 구리점 사무실 시설사용 계약서. <b>상법 제383조 제6항</b> — 자본금 10억 원 미만으로 이사를 1명 또는 2명 둔 회사에서는 각 이사(정관에 따라 대표이사를 정한 경우에는 그 대표이사)가 회사를 대표하며 이사회 기능도 이사 또는 대표이사가 담당, 2026-10-09 확인. <b>상법 제317조 제2항 제9호</b> — 회사를 대표할 이사 또는 집행임원의 성명·주민등록번호 및 주소를 등기, 2026-10-09 확인. 상법 제182조(본점이전 2주)·제183조·제396조·제635조, 제289조 제2항과 제437조의 4배 제한 삭제(각 2011년·1995년 개정) — 2026-10-08 확인. 자본금 10억 원 미만 소규모회사의 의사록 공증 면제·주주 전원 서면결의 갈음·이사 1~2명 가능 — 2026-10-08 확인. 임원 취임등기 제출서류(변경등기신청서·의사록 또는 서면결의서·취임승낙서·취임 임원당 개인인감증명서 1부·주민등록등(초)본 1부·정관·등록면허세영수필확인서·등기신청수수료 6,000원, 대리 접수 시 위임장)와 법인인감증명서·주주 인감증명서가 등기 제출목록에 없다는 점 — 2026-10-09 확인(ZUZU 임원 셀프등기 안내, 헬프미 임원 취임등기 안내). 등기 제출용 인감증명서는 발행일로부터 3개월 이내(상업등기규칙) — 2026-10-09 확인. 본인서명사실확인서는 인감증명서와 같은 효력(본인서명사실 확인 등에 관한 법률)이며 대리 발급 불가, 인감 날인 서류에 서명만 하면 보정명령 가능 — 2026-10-09 확인. 개인 인감증명서 600원·무인발급기 불가, 인감 신고는 주민등록지 관할 주민센터에서 도장·신분증·지문으로 본인만 가능, 법인인감증명서는 무인발급기 1,000원(법인인감카드+비밀번호)·창구 1,200원·인터넷 예약 1,100원이며 인터넷 발급 불가 — 2026-10-08~09 확인. 등록면허세 본점이전 112,500원·그 밖의 등기 40,200원·지방교육세 20%, 서울 외 지역은 WETAX — 2026-10-08 확인. 지방세법 제28조 제2항의 중과 요건이 '대도시 밖에 있는 법인의 본점을 대도시로 전입'하는 경우라는 점 — 2026-10-09 확인(대법원 2019.1.10. 선고 2017두31538 판결 보도자료). 법인세 신고기한은 사업연도 종료일로부터 3개월 이내이고 사업연도 변경에는 주주총회 특별결의와 세무서 신고가 필요하며 사업연도는 등기사항이 아니라는 점 — 2026-10-09 확인. 지방세법 제13조 제2항과 같은 법 시행령 제26조 제1항의 취득세 중과 제외 업종에 창고업·물류터미널이 포함되고 교육업은 미포함 — 2026-10-07 확인. 지방세징수법 제5조 제1항의 납세증명서 제출 대상은 ① 국가·지방자치단체·정부관리기관으로부터 대금을 받을 때 ② 지방세 납세의무가 있는 외국인의 출국 ③ 내국인의 해외이주 또는 1년 초과 체류 목적 거주목적 여권 신청 ④ 신탁을 원인으로 한 부동산 소유권 이전등기 신청 네 가지이며 법인등기 신청은 포함되지 않고, 납세증명서는 징수유예·회생파산 관련을 제외한 다른 체납액이 없다는 증명이라는 점 — 2026-10-09 확인. 지방교육세 과세대상에 취득세·등록면허세·주민세·재산세·자동차세 등이 포함된다는 점, 주민세 사업소분의 과세기준일 7월 1일·신고납부기간 8월 1~31일·사업소를 둔 법인은 납세의무자·법인 기본세액 자본금 규모별 5만/10만/20만 원·연면적 330㎡ 초과분 1㎡당 250원·기본세액에 지방교육세 10%(인구 50만 이상 시 25%) 부가 — 2026-10-09 확인(2차 자료 기준이므로 금액과 가산세 특례는 구리시청 세무과 확인 필요). <b>확인하지 못한 것 — 등록면허세 중과 해당 여부, '그 밖의 등기' 건수 계산, 관할 등기소의 서면결의서·본인서명사실확인서 수용 여부, 변경등기신청서를 대표이사 개인 인감으로 낼 수 있는지, 전자신청 시 수수료 할인액, 인감카드 재발급 수수료, 주민세 사업소분 가산세 면제 특례의 적용 범위, 이 법인의 실제 지방세 체납 유무. 위 서류는 실무 안내와 법령을 바탕으로 클로드가 작성한 초안이며 법률 자문이 아닙니다.</b></div>
"""

# ---------------------------------------------------------------- 박종혁 본부장 협업 평가
PARK = """
<h1>박종혁 본부장 협업 — 평가</h1>
<p class="note">10/9 회의 녹음 <b>119분 424개 발언 전체</b>를 읽고 썼고, <b>10/10 루크님 반론을 받아 네 군데를 고쳤습니다.</b> 손익분기는 수강생 21~33명입니다. 숫자는 넉넉히 넘습니다 — <b>남은 쟁점은 금액이 아니라 타이밍 하나와 정의 하나</b>입니다.</p>
<div class="card accent" style="margin-bottom:14px">
  <p style="margin:0 0 10px"><b>10/10 — 제가 접는 네 가지</b></p>
  <ul class="list">
    <li><div class="t">"박종혁 본인의 실적 숫자가 없다" — 철회합니다</div><div class="m">루크님이 <b>첫 강의를 같이 만들면서 성과를 함께 냈다</b>고 하셨습니다. 그건 녹음에 적힌 숫자보다 강한 증거입니다. 제가 "녹음에 없다"를 "모른다"로 번역한 게 과했습니다</div></li>
    <li><div class="t">"고정급의 성질이 미정" — 닫혔습니다</div><div class="m">첫 3개월은 선투자, 4개월째부터 차감. 이미 합의하신 내용이었습니다</div></li>
    <li><div class="t">"비대칭을 모르고 계실 것" — 틀렸습니다</div><div class="m">과거 성과에 대한 존중과 의사결정권 이전의 대가로 <b>알고 선택한 구조</b>였습니다. 숫자는 그대로 두되 해석을 고쳤습니다</div></li>
    <li><div class="t">"매출이 안 날 위험" — 동의합니다</div><div class="m">제 계산에서도 손익분기 전환율이 1% 안쪽이고 루크님 과거 전환율은 3%입니다. <b>모객이 되면 매출은 납니다.</b> 위험은 전환이 아니라 모객입니다</div></li>
  </ul>
</div>

<h2>먼저 — 기억하시는 것과 녹음이 다른 한 가지</h2>
<div class="card red">
  <p style="margin:0 0 10px">"1월달에 1번 쉬고 내 보자"로 기억하고 계신데, <b>녹음에 '쉰다'는 말은 없습니다.</b></p>
  <p style="margin:0 0 10px;padding:12px 14px;border-radius:10px;background:rgba(127,127,127,.09);font-size:14px;line-height:1.75"><b>[61:28] 박종혁</b> — "지금부터 삼 개월이면 일월이에요. 내년. 1월은 그래도 첫 시작이니까 가장 기대할 만한 수치잖아요. <b>1월달에 어느 정도 3개월 동안 모객을 한 다음에 1월달에 터트린다</b>는 생각을 가지고 있거든요."</p>
  <p style="margin:0"><b>10~12월은 쉬는 기간이 아니라 가장 바쁜 3개월입니다.</b> 그리고 그 3개월의 주연은 루크님입니다 — 다마고치 채널이 "멘토는 똑같고 멘티만 바뀌는" 포맷이라, 매주 촬영에 들어가셔야 합니다. '쉬고'로 잡아 두면 10월 일정이 바로 깨집니다.</p>
</div>

<h2>돈 — 루크님이 3개월에 얼마를 쓰나</h2>
<div class="card">
  <div class="wrapx"><table>
  <tr><th></th><th>월</th><th>3개월</th><th>근거</th></tr>
  <tr><td>박종혁 고정급</td><td class="num">300만</td><td class="num">900만</td><td><small>[76:49] "현재는 300이긴 합니다"</small></td></tr>
  <tr><td>광고비</td><td class="num">300만</td><td class="num">900만</td><td><small>[60:41] "한 달에 300은 태워야"</small></td></tr>
  <tr><td>PD 외주</td><td class="num">미정</td><td class="num"><b>미정</b></td><td><small>[54:56] "제가 부담할 순 없어요"</small></td></tr>
  <tr><td><b>합계</b></td><td class="num"><b>600만+</b></td><td class="num"><b>1,800만+</b></td><td></td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>그런데 1,000만원이라는 숫자가 두 가지 뜻으로 쓰였고, 정정되지 않았습니다.</b></p>
  <div class="wrapx"><table>
  <tr><th></th><th>말한 내용</th><th>3개월 총액</th></tr>
  <tr><td>박종혁 [56:35]</td><td>"3개월 기준으로 천만 원" — <b>PD 인건비 + 본인 고정비 + 구글·메타 광고비 전부 포함</b></td><td class="num">1,000만</td></tr>
  <tr><td>루크님 [75:24]</td><td>"운영 비용이 한 1,000만원에 광고비는 한 달에 300만원 정도, 그러면 한 달에 제가 내야 되는 돈이 600, 700만원"</td><td class="num">1,900만</td></tr>
  <tr><td><b>실제 산술</b></td><td><b>고정급만 900만이라 1,000만 안에 광고비·PD가 들어갈 자리가 없습니다</b></td><td class="num"><b>1,800만 + PD</b></td></tr>
  </table></div>
  <div class="note"><b>박종혁이 1,000만을 말한 3분 뒤에 광고비 300을 따로 말하고, 20분 뒤에 고정급 300을 또 따로 말했습니다.</b> 루크님이 75:24에서 "그럼 월 600~700이네요"로 다시 계산했을 때 <b>박종혁은 정정하지 않았습니다.</b> 즉 두 분이 서로 다른 총액을 머릿속에 두고 악수했을 가능성이 큽니다. <b>2월에 "원래 1,000만이라고 하셨잖아요"가 나오는 지점입니다.</b> PD 단가가 안 정해진 것도 같은 구멍입니다 — 월 100만이냐 250만이냐에 따라 3개월에 300만~750만이 움직입니다.</div>
</div>

<h2>손익분기 — 21명이냐 33명이냐</h2>
<div class="card gold">
  <p style="margin:0 0 10px">강의가 180만([58:33]), PG 4%, 비용 2,250만(고정급 900 + 광고 900 + PD 450 가정) 기준입니다. <b>6:4의 분모가 무엇이냐에 따라 손익분기가 12명 벌어집니다.</b></p>
  <div class="wrapx"><table>
  <tr><th></th><th>A안 — 매출의 6:4<br><small>비용은 전부 루크님</small></th><th>B안 — 비용 차감 후 6:4<br><small>광고·PD를 먼저 빼고 나눔</small></th></tr>
  <tr><td><b>루크님 손익분기</b></td><td class="num"><b>33명</b></td><td class="num"><b>21명</b></td></tr>
  <tr><td>필요 매출</td><td class="num">5,940만</td><td class="num">3,780만</td></tr>
  <tr><td>필요 전환율<small><br>카페 3,000명 기준</small></td><td class="num">1.1%</td><td class="num">0.7%</td></tr>
  </table></div>
  <p style="margin:14px 0 8px"><b>인원별 루크님 손익</b></p>
  <div class="wrapx"><table>
  <tr><th>수강생</th><th>매출</th><th>A안 루크</th><th>B안 루크</th><th>박종혁<small><br>A안 + 고정급</small></th></tr>
  <tr><td>0명</td><td class="num">0</td><td class="num">−2,250만</td><td class="num">−1,440만</td><td class="num"><b>+900만</b></td></tr>
  <tr><td><b>21명</b></td><td class="num">3,780만</td><td class="num">−798만</td><td class="num"><b>+12만</b></td><td class="num">+3,077만</td></tr>
  <tr><td>30명</td><td class="num">5,400만</td><td class="num">−176만</td><td class="num">+634만</td><td class="num">+4,010만</td></tr>
  <tr><td><b>33명</b></td><td class="num">5,940만</td><td class="num"><b>+31만</b></td><td class="num">+841만</td><td class="num">+4,321만</td></tr>
  <tr><td>60명</td><td class="num">1억 800만</td><td class="num">+1,897만</td><td class="num">+2,707만</td><td class="num">+7,121만</td></tr>
  <tr><td>90명</td><td class="num">1억 6,200만</td><td class="num">+3,971만</td><td class="num">+4,781만</td><td class="num">+1억 221만</td></tr>
  <tr><td>300명<small><br>박종혁 목표</small></td><td class="num">5억 4,000만</td><td class="num">+1억 8,486만</td><td class="num">+1억 9,296만</td><td class="num">+3억 2,004만</td></tr>
  </table></div>
  <div class="note"><b>맨 윗줄과 21명 줄을 같이 보세요.</b> 하나도 안 팔리면 박종혁은 +900만이고 루크님은 −2,250만입니다. <b>루크님이 겨우 본전인 21명 지점에서 박종혁은 이미 3,077만을 가져갑니다.</b> 루크님 철학대로 "책임지는 사람이 6"인 건 알겠는데, <b>이 구조에서 현금 리스크를 지는 사람은 루크님이고 책임의 방향과 반대입니다.</b></div>
</div>

<h2>구조를 숫자 없이 한 장으로</h2>
<div class="card red">
  <div class="wrapx"><table>
  <tr><th></th><th>박종혁</th><th>루크님</th></tr>
  <tr><td>하방</td><td><b>보호됨</b> — 고정급 900만</td><td><b>노출됨</b> — 1,800만+ 전액</td></tr>
  <tr><td>상방</td><td><b>60%</b></td><td>40%</td></tr>
  <tr><td>현금 투입</td><td class="num">0원</td><td class="num">1,800만+</td></tr>
  <tr><td>전력 투구</td><td><b>겸업 자유</b><small><br>[80:05] 루크님: "투잡을 하든 쓰리잡을 하시든 아예 상관없거든요"</small></td><td>본인 사업 + 촬영 주연</td></tr>
  </table></div>
  <p style="margin:14px 0 0"><b>이건 알고 선택한 구조입니다.</b> 루크님이 [82:44]에서 직접 말한 그대로고요 — "수익을 많이 드리는 거는 최종적으로 결정하시는 거에 대한 자유도 드리는 거라서, 여태까지 해오셨던 퍼포먼스나 결과물들에 대한 존중의 의미." 10/10에 덧붙이신 근거도 같은 방향입니다 — <b>첫 강의를 같이 만들며 함께 성과를 냈고, 그가 만들어준 수익이 컸으니 선투자로 본다.</b> 과거 실적에 값을 매겨 선투자하는 건 일관된 판단이고, 비대칭의 크기도 알고 택하신 겁니다. <b>그래서 이 표는 "고쳐야 할 문제"가 아니라 "석 달 동안 어디까지 버틸 수 있는지를 재는 자"으로 보시면 됩니다.</b></p>
  <div class="note"><b>한 가지만 짚어 두면 — 초월스토리 건과 정확히 반대 포지션입니다.</b> 거기서는 루크님이 8% 수수료로 하방을 보호받고 광고비 리스크의 20%만 졌습니다. 여기서는 하방 보호가 없고 리스크 100%를 집니다. 각각은 합리적인데 <b>같은 석 달에 겹치면 현금이 한 방향으로만 흐릅니다.</b> 10~12월에 나가는 1,800만원이 여기고, 초월스토리 쪽 회수는 12월 런칭 뒤입니다.</div>
</div>

<h2>박광진 모델과의 비교 — 루크님 판단은 절반만 맞습니다</h2>
<div class="card">
  <p style="margin:0 0 10px">"박광진 쪽은 단독 키워드 상품 판매라 수요가 말랐고, 리셀은 더 초보 대상이라 내가 더 잘할 수 있다" — 이 판단을 녹음과 대조했습니다.</p>
  <p style="margin:0 0 8px"><b>맞는 부분</b></p>
  <ul class="list">
    <li><div class="t">시장 크기는 루크님이 큽니다</div><div class="m">"재고 없이 시작"은 40~60대 초보에게 가장 강한 후크입니다. 키워드 단독 판매는 이미 한 번 해본 사람을 대상으로 하니 모집단이 작습니다</div></li>
    <li class="big"><div class="t">박종혁이 박광진을 못 쓰는 이유를 본인이 말했습니다 — 루크님이 가진 것</div><div class="m">[81:49] "<b>자기 커머스 매출은 없고 다 수강생 그걸로만, 전문 강사로서만 활동</b>" / [82:17] "<b>유튜브 채널에 일단 나갈 수가 없어요</b>" — 즉 박광진은 ① 실제 커머스 실적이 없어 플랫폼이 안 받아주고 ② 노출 수단이 막혀 있습니다. 루크님은 3PL 물동량(월 2,000~5,000건)과 수강생 3,000명이라는 <b>증명 가능한 실물</b>이 있습니다. 이게 이 협업의 진짜 자산입니다</div></li>
  </ul>
  <p style="margin:14px 0 8px"><b>위험한 부분 — 이쪽이 더 중요합니다</b></p>
  <ul class="list">
    <li class="big"><div class="t">초보가 많다는 건 성공 사례가 적게 나온다는 뜻입니다</div><div class="m">박종혁 전략의 심장은 <b>실증 사례 채널</b>입니다 — [51:28] "실제로 대표님이 어떻게 사람들을 가르치는지를 옆에서 보면서 각각의 사람들의 스토리를 잘 푸는 채널". 그런데 <b>성과 스토리가 가장 안 나오는 집단이 초보</b>입니다. 중도 이탈이 많고 매출 그래프가 안 그려집니다. 전략의 연료가 가장 희박한 곳에 전략을 세우는 모양입니다</div></li>
    <li><div class="t">박광진의 약점을 루크님도 일부 공유합니다</div><div class="m">"본인 커머스 매출이 없다"는 지적 — 루크님의 현재 수익도 강의와 3PL이 중심이고, <b>본인 스마트스토어의 최근 매출은 녹음에서 언급되지 않았습니다.</b> 3PL 물동량은 수강생 것이고 루크님 매출이 아닙니다. 다마고치 채널에서 "나는 지금도 팔고 있다"를 보여줄 수 있느냐가 박광진과 갈라지는 지점입니다</div></li>
    <li><div class="t">박종혁도 이 시장을 하락 국면으로 봅니다</div><div class="m">[37:07] "<b>앞으로 1년 정도는 더 될 수 있다</b>고 생각을 하는데 결과적으로는 그 방식 자체에 사람들이 피로감을 많이 느끼고 있어서 차별성이 없잖아요." — 리셀이 박광진보다 수요가 크다는 건 맞지만, <b>1년짜리 창을 보고 들어가는 것</b>입니다. 3개월 테스트가 그 창의 4분의 1입니다</div></li>
  </ul>
</div>

<h2>모객 숫자가 유일한 검증 대상입니다</h2>
<div class="card blue">
  <p style="margin:0 0 10px">박종혁이 제시한 성공 기준 — [58:33] "<b>카페가 3개월 이내에 3천명 정도 들어오면 프로젝트 성공</b>", [59:29] "<b>한 달에 천 명씩은 들어와야</b>". 이걸 광고 효율로 환산했습니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th></th></tr>
  <tr><td>광고비 월 300만 ÷ 카페 월 1,000명</td><td class="num"><b>가입 1명당 3,000원</b></td></tr>
  <tr><td>전환 10%<small> (박종혁 가정)</small> → 유료 1명당</td><td class="num">3만원 · ROAS 60배</td></tr>
  <tr><td>전환 3%<small> (루크님 과거 실적)</small> → 유료 1명당</td><td class="num">10만원 · ROAS 18배</td></tr>
  <tr><td>전환 1.1%<small> (A안 손익분기)</small> → 유료 1명당</td><td class="num">27만원 · ROAS 6.6배</td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>광고 효율은 걱정할 지점이 아닙니다.</b> 손익분기 전환율이 1% 안쪽이고 루크님 과거 전환율이 3%니까, <b>카페에 3,000명이 실제로 모이기만 하면 돈은 남습니다.</b> 전부 <b>"3,000원에 카페 가입 1명"이 되느냐</b>에 걸려 있습니다.</p>
  <div class="note"><b>그런데 그 숫자의 출처가 약합니다.</b> [59:58] "박광진 대표랑 일을 했을 때는 진짜 <b>한 달에 4천 명씩</b> 들어오게 만드는 적도 있었기 때문에" — 바로 다음 문장이 "<b>근데 그거는 광고비를 많이 태웠어요</b>"입니다. 월 300만으로 1,000명이 되는 근거는 녹음에 없습니다. <b>그때 광고비가 얼마였는지를 물어보시면 3,000원이 현실적인지 바로 나옵니다.</b> 이 질문 하나가 1,800만원의 운명을 가릅니다.</div>
</div>

<h2>실적 — 제가 틀렸고, 하나만 남습니다</h2>
<div class="card gold">
  <p style="margin:0 0 10px">어제 저는 "119분에 그가 직접 만든 숫자가 하나도 없다"를 근거로 실적 확인을 요구했습니다. <b>그 요구는 철회합니다.</b> 루크님이 <b>첫 강의를 같이 만들면서 성과를 함께 낸 당사자</b>라면, 녹음에 적힌 숫자보다 직접 겪은 쪽이 훨씬 강한 증거입니다. 녹음에 없다는 사실을 "검증되지 않았다"로 옮긴 게 제 잘못입니다 — 그가 루크님 앞에서 자기 실적을 숫자로 읊지 않은 건 <b>이미 아는 사람끼리 안 하는 말</b>이었을 뿐입니다.</p>
  <p style="margin:0 0 10px"><b>다만 하나는 신뢰와 무관하게 남습니다 — 박광진 건의 광고비.</b> 이건 사람에 대한 질문이 아니라 산수에 대한 질문입니다.</p>
  <div class="wrapx"><table>
  <tr><th>당시 광고비가</th><th>카페 1명당</th><th>월 300만으로</th><th>3개월</th></tr>
  <tr><td>월 1,000만</td><td class="num">2,500원</td><td class="num">1,200명</td><td class="num">3,600명 <b>달성</b></td></tr>
  <tr><td>월 2,000만</td><td class="num">5,000원</td><td class="num">600명</td><td class="num">1,800명 <b>미달</b></td></tr>
  <tr><td>월 3,000만</td><td class="num">7,500원</td><td class="num">400명</td><td class="num">1,200명 <b>크게 미달</b></td></tr>
  </table></div>
  <p style="margin:12px 0 0">[59:58] "한 달에 4천 명씩 들어오게 만드는 적도 있었기 때문에" 바로 다음 문장이 [60:19] "<b>광고비를 많이 태웠어요</b>"입니다. 월 4,000명을 만든 광고비를 모르면 <b>월 300만으로 월 1,000명</b>이 가능한 숫자인지 알 수 없고, 그러면 <b>성공 기준 3,000명 자체가 근거 없는 선</b>이 됩니다.</p>
  <div class="note">이 질문은 "당신 실력을 못 믿겠다"가 아니라 <b>"그 성과를 지금 예산으로 재현할 수 있나"</b>입니다. 묻는 방식도 그렇게 하시면 됩니다 — "그때 월 4천 명 나올 때 광고비가 얼마였어요? 그 단가면 지금 300만으로 몇 명 나올까요?" <b>그가 바로 답할 수 있는 질문이고, 답이 나오면 10월 첫 주에 목표선을 다시 그릴 수 있습니다.</b></div>
</div>

<h2>클래식 전략에 3개월 시한을 붙인 게 유일한 구조적 모순입니다</h2>
<div class="card red">
  <p style="margin:0 0 10px">"유행을 쫓다가 결국 안정적이고 클래식한 쪽으로 온다" — <b>이 테제에 저도 동의합니다.</b> 그리고 중요한 건, <b>박종혁도 같은 테제를 갖고 있다는 게 녹음에 있습니다.</b></p>
  <p style="margin:0 0 12px;padding:12px 14px;border-radius:10px;background:rgba(127,127,127,.09);font-size:14px;line-height:1.75"><b>[35:37] 박종혁</b> — "라이브는 긴박하고 뭘 팔아야 되고 약간 이러니까 <b>여기서 가치가 다 깎이는 것 같은 거예요.</b>" / <b>[34:59]</b> — "<b>대표님을 좀 만나기 어려운 사람으로 브랜딩을 했으면 좋겠다</b>는 생각을 했어요."</p>
  <p style="margin:0 0 10px"><b>두 분의 테제가 같다는 것이 이 협업의 가장 단단한 근거입니다.</b> 손익분기 21명보다 이게 중요합니다. 숫자가 맞는 협업은 많지만 세계관이 맞는 협업은 드뭅니다.</p>
  <p style="margin:0 0 10px"><b>그런데 클래식 전략의 비용은 돈이 아니라 시간입니다.</b> 그리고 박종혁 본인이 그 시간을 계산해 뒀습니다 —</p>
  <p style="margin:0 0 12px;padding:12px 14px;border-radius:10px;background:rgba(127,127,127,.09);font-size:14px;line-height:1.75"><b>[52:34] 박종혁</b> — "이거의 전체적인 과정을 가는데 저는 <b>6개월 정도는 걸릴 거라고 생각을 해요.</b> 6개월 정도 걸리는 시간 동안에 물론 세팅은 빠르면 빠를수록 좋으니까 하겠지만 <b>보수적으로 봐야 되는 건 맞고요.</b>"</p>
  <p style="margin:0"><b>본인 입으로 6개월이라고 한 전략에 3개월 시한과 매출 기준을 붙였습니다.</b> 이게 이 설계의 유일한 구조적 모순입니다. 1월 매출이 기대 이하로 나왔을 때 <b>"클래식 전략이 안 통한다"가 아니라 "클래식 전략을 3개월 만에 측정했다"일 가능성이 큽니다.</b> 그러면 맞는 전략을 조급하게 죽이게 됩니다.</p>
</div>

<h2>그래서 3개월 지표를 머릿수에서 밀도로 바꾸시는 게 낫습니다</h2>
<div class="card blue">
  <p style="margin:0 0 10px">박종혁이 만들고 싶다고 한 것은 회원 수가 아니라 <b>문화</b>입니다. 본인 표현이 그렇습니다 —</p>
  <p style="margin:0 0 12px;padding:12px 14px;border-radius:10px;background:rgba(127,127,127,.09);font-size:14px;line-height:1.75"><b>[52:34] 박종혁</b> — "저희가 그때 잘했던 거는 <b>스스로 월백에서 문화를 만들었어요.</b> 실제로 <b>내가 직접 해보고 그걸 글로 남기고</b> 다른 사람들한테 가서 다른 사람들이 어떻게 하는지 보고, 저는 <b>이 사이클의 문화를 네이버 카페를 통해서 만들면</b> 되게 좋겠다."</p>
  <p style="margin:0 0 10px"><b>그런데 성공 기준은 "3개월에 3,000명"으로 머릿수만 잡혔습니다.</b> 카페 가입자 3,000명은 광고비로 살 수 있고, 밀도는 살 수 없습니다. 그리고 1월에 돈이 되는 건 머릿수가 아니라 밀도입니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th>지금 기준</th><th>바꾸면</th></tr>
  <tr><td>모객</td><td>신규 회원 3,000명</td><td>신규 3,000명 <b>그대로</b></td></tr>
  <tr><td><b>밀도</b></td><td class="num">없음</td><td><b>글을 한 번이라도 쓴 사람 수</b></td></tr>
  <tr><td><b>반복</b></td><td class="num">없음</td><td><b>2회 이상 글 쓴 사람 수</b></td></tr>
  <tr><td><b>자산</b></td><td class="num">없음</td><td><b>촬영 완료한 멘티 편수</b></td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>"글을 두 번 이상 쓴 사람"이 1월 전환의 실제 모집단입니다.</b> 3,000명 중 그게 100명이면 1월은 됩니다. 3,000명인데 20명이면 머릿수만 산 것이고, 그건 광고를 끄면 사라집니다. <b>이 지표를 10월에 정해 두면 1월에 "됐다/안 됐다"를 다투지 않고 "어디까지 왔다"를 같이 볼 수 있습니다.</b></p>
  <div class="note">다마고치 편수도 같이 세어 두세요. 매출이 0이어도 <b>멘티 12편이 쌓였으면 그건 1월 이후에도 계속 일하는 자산</b>입니다. 반대로 매출이 조금 났는데 편수가 3편이면 1월에 쓸 탄약이 없습니다. <b>클래식 전략에서 3개월짜리 성과는 매출이 아니라 쌓인 자산입니다.</b></div>
</div>

<h2>1월에 두 가지가 겹칩니다</h2>
<div class="card red">
  <p style="margin:0 0 10px">[111:55] "인베이더랑 강의를 12월까지 할 거예요. <b>정산이 1월달까지는 나오니까</b>" — 그리고 새 프로젝트의 첫 매출 목표도 1월입니다.</p>
  <div class="wrapx"><table>
  <tr><th></th><th>10월</th><th>11월</th><th>12월</th><th>1월</th></tr>
  <tr><td>인베이더 정산</td><td class="num">들어옴</td><td class="num">들어옴</td><td class="num">들어옴</td><td class="num"><b>마지막</b></td></tr>
  <tr><td>이 프로젝트</td><td class="num">−600만+</td><td class="num">−600만+</td><td class="num">−600만+</td><td class="num"><b>첫 매출</b></td></tr>
  <tr><td>신정현 입금<small><br>"느낌"</small></td><td class="num">2,000만?</td><td class="num">2,000만?</td><td class="num">2~3,000만?</td><td class="num">—</td></tr>
  </table></div>
  <p style="margin:12px 0 0"><b>10~12월 세 달 동안 1,800만원이 나가고 들어오는 게 없습니다.</b> 그 구멍을 신정현 님 입금으로 메우는 구조인데, 루크님이 쓰신 표현이 "<b>들어올 것 같은 느낌</b>"이었습니다. <b>그 입금이 한 달 밀리면 이 프로젝트가 현금을 조입니다.</b> KCB 622에 대환을 검토하는 상황이라 여유가 두껍지 않습니다.</p>
  <div class="note"><b>제안 — 고정급을 월 300 고정이 아니라 "선급금"으로 두는 방법.</b> 루크님이 [75:59]에서 이미 꺼내셨습니다 — "만약에 한 달이 꾸준히 가게 되면 그때부터는 그냥 거기 나오는 돈으로 급여를" 하지만 <b>박종혁의 동의 발언이 녹음에 없습니다.</b> 즉 4개월째부터 고정급을 계속 주는지도 안 정해졌습니다. 1월 매출에서 선급 900만을 회수하고 그 뒤를 6:4로 돌리면, 루크님 하방이 −2,250만에서 −1,350만으로 줄고 박종혁의 상방은 그대로입니다.</div>
</div>

<h2>남은 것은 세 칸입니다 — 그중 하나는 타이밍입니다</h2>
<div class="card accent">
  <ul class="list">
    <li class="big"><span class="tag p0">1</span><div class="t">차감 규칙은 <b>1월이 아니라 10월에</b> 정해야 합니다</div><div class="m">"첫 3개월은 선투자, 뒤에부터 차감" — 방향은 이미 합의되셨습니다. 그런데 <b>차감 방식을 1기 결과를 본 뒤에 정하면 그건 합의가 아니라 협상이 됩니다.</b> 결과가 좋으면 서로 자기에게 유리한 해석을 들고 오고, 나쁘면 서로 상대 쪽 부담을 말합니다. <b>지금 정하면 둘 다 결과를 모르니 공정하고, 1월에 정하면 숫자를 쥔 상태의 흥정이 됩니다.</b> 오래 알던 사이가 깨지는 지점이 정확히 거기입니다 — <b>"신뢰하니까 나중에"가 아니라 "신뢰하니까 지금"</b>입니다. 종이 한 장이면 됩니다: 4개월째부터 광고비·PD비를 먼저 빼고 6:4, 고정급은 그 시점에 종료 또는 매출에서 회수 — 어느 쪽이든 <b>지금 한 줄</b></div></li>
    <li class="big"><span class="tag p0">2</span><div class="t">3PL · 리셀 · 프로그램 매출은 6:4 밖이라고 한 줄</div><div class="m">이것도 신뢰와 무관합니다. <b>분쟁 조항이 아니라 정의 조항</b>이기 때문입니다. 박종혁이 데려온 수강생이 루크님 3PL을 쓰고 프로그램을 삽니다. 그게 6:4 안이냐 밖이냐를 아무도 말하지 않았는데, <b>성공할수록 그 금액이 커집니다.</b> 지금은 1초면 합의되고, 물동량이 월 5,000건이 된 뒤에는 둘 다 양보하기 어려워집니다</div></li>
    <li><span class="tag p1">3</span><div class="t">총액 인식을 맞추는 메시지 한 통</div><div class="m">박종혁은 [56:35]에서 "3개월 천만 원에 PD·고정비·광고비 전부 포함"이라고 했고, 루크님은 [75:24]에서 "천만 + 광고 900만"으로 계산하셨습니다. <b>그가 아직 '총 1,000만'으로 알고 있으면, 루크님이 1,900만을 쓰는 걸 "약속보다 두 배를 써준 것"으로 인식하지 못합니다.</b> 선투자의 값이 절반으로 깎여서 전달되는 셈입니다. "3개월 동안 고정급 900 + 광고 900 + PD 별도로 제가 부담합니다" 한 줄이면 <b>같은 돈으로 더 큰 신뢰가 전달됩니다.</b> PD 월 단가도 이때 같이</div></li>
  </ul>
  <div class="note"><b>어제 다섯 칸에서 두 칸이 빠졌습니다.</b> 고정급의 성질(이미 합의)과 매출 기준 중단선(3개월은 투자금으로 확정하셨으니 중단선을 둘 자리가 아님) — 둘 다 접습니다. 대신 <b>밀도 지표</b>를 위 섹션에 새로 넣었습니다. 그게 중단선보다 쓸모가 있습니다.</div>
</div>

<h2>종합 — 10/10 수정판</h2>
<div class="card">
  <p style="margin:0 0 12px"><b>하세요. 어제보다 더 분명하게 하세요.</b> 어제는 "다섯 칸을 닫고"였는데, 루크님 설명을 듣고 나니 <b>남은 건 세 칸이고 그중 둘은 종이 한 장</b>입니다.</p>
  <p style="margin:0 0 10px"><b>판단의 근거가 숫자가 아니라는 걸 인정하는 게 정확합니다.</b> 손익분기 21명은 쉽게 넘는 선이고, 루크님 말대로 "사람이 들어왔는데 매출이 안 나는 것"은 두 분 경력에서 일어나기 어렵습니다. 진짜 근거는 세 가지입니다 — ① 첫 강의를 같이 만들며 함께 성과를 낸 이력 ② <b>세계관이 같다는 것</b>(라이브의 긴박함이 가치를 깎는다는 인식을 두 분이 공유합니다) ③ 1월 인베이더 종료 이후 자체 유입 경로가 필요하다는 시점. <b>이 세 가지면 2,000만원은 비싸지 않습니다.</b></p>
  <p style="margin:0 0 10px"><b>제가 어제 놓친 것.</b> 저는 녹음에 있는 것만 보고 "검증이 없다"고 썼습니다. 그런데 루크님에게는 <b>녹음 밖의 3년</b>이 있었습니다. 숫자로 확인할 수 없는 신뢰를 "미확인 리스크"로 분류한 건 제 틀이 좁았던 겁니다. 다만 그 반대도 참입니다 — <b>신뢰가 두꺼울 때 가장 안 적는 것이 정의와 타이밍</b>이고, 그 둘이 1월에 터집니다. 그래서 남긴 세 칸은 전부 "서로를 못 믿어서"가 아니라 <b>"믿는 사이에 생기는 종류의 사고"를 막는 것</b>입니다.</p>
  <p style="margin:0"><b>가장 값싼 한 수.</b> 박광진 건 광고비를 묻는 전화 5분. 신뢰 문제가 아니라 <b>같은 성과를 지금 예산으로 재현할 수 있는지</b>의 산수이고, 답에 따라 10월 첫 주에 목표선을 다시 그릴 수 있습니다. 3,000명이 처음부터 무리한 선이었다면 1월에 "실패"로 적지 않아도 됩니다.</p>
  <div class="note"><b>그리고 10월 일정을 비워 두지 마세요.</b> "1월에 터트린다"는 설계에서 10~12월 모객의 주연은 루크님입니다. 등기(10/16), 인베이더 마지막 기수(12월), 초월스토리 가을 대표님 건(12월 런칭), 이 프로젝트의 주간 촬영이 같은 석 달에 겹칩니다. 박종혁은 [54:18]에서 본인 업무량을 "하루 3~4시간, 플랫폼 구축이면 6~8시간"까지 계산해 뒀는데 <b>루크님 쪽 투입 시간은 녹음에 한 번도 나오지 않습니다.</b> "3개월 동안 제가 주당 몇 시간을 써야 하나요"를 숫자로 받아 두시면, 1월에 "루크님이 덜 움직였다"와 "그런 얘기 없었다"가 부딪히지 않습니다.</div>
</div>

<div class="src" style="margin-top:14px">근거 · 모든 인용은 2026-10-09 녹음(Plaud, 전사 424개 발언, 종료 약 119분 38초)의 전사에서 그대로 옮긴 것이고 대괄호 안은 타임스탬프입니다. 발언자는 전사의 화자 분리를 따랐습니다. 녹음 중 하이라이트 버튼 기록(mark_memo)은 이 파일에 없습니다. <b>녹음에 없어서 계산에 가정을 넣은 것 —</b> PD 외주 월 150만(3개월 450만)은 제 가정입니다. 녹음에는 PD 단가가 전혀 없습니다. PG 수수료 4%도 가정이며 녹음에 없습니다. 강의가 180만은 박종혁의 [58:33] 발언이고 확정이 아닙니다("이건 근데 제 생각이라서"). 전환율 3%는 루크님의 과거 실적(DB 3,000개 → 라이브 유입 18~20% → 전환 3%, 2026-10-08 확인)이고 이 프로젝트의 수치가 아닙니다. 수강생 1인당 실수령 172.8만원(180만 − PG 4%)으로 계산했습니다. <b>녹음에 명확히 없는 것 —</b> 6:4가 매출 기준인지 순이익 기준인지, 1,000만원에 광고비·PD가 포함인지, 매출 목표 수치, 목표 미달 시 중단·환수 규칙, 기수당 모집 인원, PD 단가와 인원, 계약 형식(박종혁은 [43:20] "용역 계약"이라 했고 루크님은 [111:55] "직원 계약"이라 표현), 박종혁 본인이 만든 과거 매출·수강생 수·ROAS, 박광진 건의 광고비, 3PL·리셀 매출의 귀속, 4개월째 이후 고정급의 존속, "3개월 안에 브랜딩을 완료한다"는 단정 발언. <b>저는 세무사도 변호사도 아니고, 위 손익 계산은 녹음에 나온 숫자와 명시한 가정만으로 만든 것입니다.</b></div>
"""

# ---------------------------------------------------------------- 힐링디어스 폐업 vs 유지
CORP = """
<h1>힐링디어스 → 셀러들의 수다</h1>
<p class="note">10/7 확인된 조건: <b>설립 2022-03-16</b> · 지분 루크 100% · 임원은 대표이사 루크 + 감사 어머니(지분 없음, 무보수) · 직원 없음 · 매출 없었던 것으로 추정(확인 필요), 기장은 계속 · 구상 지분 <b>루크 51 / 신정현 26 / 제3자 23</b> · 부동산은 둘 — <b>서울 꼬마빌딩</b>(사무실·여러 사업 용도, 일부 임대, 물류창고로는 안 씀)과 <b>경기 외곽 창고형 매장 3~5곳</b>. 저는 세무사도 변호사도 아닙니다. 실행 전에 세무사 확인이 필요합니다.</p>

<h2>결론 — 두 부동산은 완전히 다른 건입니다</h2>
<div class="card accent">
  <div class="wrapx"><table>
  <tr><th></th><th>어디</th><th>취득세 중과</th><th>언제</th></tr>
  <tr><td><b>창고형 매장 3~5곳</b></td><td>경기 외곽<br><span class="tag">권역 밖인지 확인</span></td><td class="num"><b>없음</b></td><td class="num"><b>지금 가능</b></td></tr>
  <tr><td><b>꼬마빌딩</b></td><td>서울 (과밀억제권역)</td><td class="num">5년 이내면 4%→8%</td><td class="num"><b>2027-03-16 이후</b></td></tr>
  </table></div>
  <p style="margin:10px 0 0">중과는 <b>과밀억제권역 안의 부동산</b>을 살 때만 걸립니다(지방세법 제13조②). 경기 외곽이 권역 밖이면 <b>창고형 매장은 5년과 무관하게 지금 사도 됩니다.</b> 묶여 있는 건 서울 건물 하나뿐이고, 거기까지 <b>160일</b> 남았습니다.</p>
  <div class="note">본점이 권역 안(구리)에 있어도 권역 밖 부동산 취득은 중과 대상이 아닙니다. 다만 경기도에도 과밀억제권역이 있습니다 — <b>의정부·구리·하남·고양·수원·성남·안양·부천·광명·과천·의왕·군포</b>와 시흥·남양주 일부. 후보지가 이 목록에 없는지만 확인하세요.</div>
</div>

<h2>서울 건물은 "용도 설계"로 피할 수 없습니다</h2>
<div class="card red">
  <p style="margin:0 0 10px">중과를 피하는 길은 <b>설립 5년</b>과 <b>중과 제외 업종에 직접 사용</b> 두 개인데, 서울 건물에서는 두 번째가 닫힙니다.</p>
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">창고로 안 쓰시면 제외 업종 카드가 없습니다</div><div class="m">목록에 있는 건 창고업·물류터미널·유통산업 쪽이고, <b>교육업은 목록에 없습니다.</b> 사무실로 쓰는 것은 제외 사유가 아닙니다</div></li>
    <li><span class="tag p0">2</span><div class="t">용도를 섞으면 오히려 불리합니다</div><div class="m">제외 업종을 겸용하면 <b>면적으로 안분</b>해 그 부분만 빼주는 식으로 다툼이 됩니다. "여러 용도로 쓴다"는 면제 근거가 아니라 분쟁 거리입니다</div></li>
    <li><span class="tag p1">3</span><div class="t">임대는 더 어렵습니다</div><div class="m">임대한 매장도 '직접 사용'으로 본 대법원 판결(2019-09-10)이 있지만 <b>유통산업(매장)</b> 사안입니다. 사무실을 세놓는 데 그대로 적용된다고 보기 어렵습니다</div></li>
  </ul>
  <div class="note">5년 이내에 사면 <b>용도와 무관하게</b> 중과입니다. 취득세 4% → 8%, 20억 기준 약 8,000만 원.</div>
</div>

<h2>5년을 넘기면 고민이 통째로 사라집니다</h2>
<div class="card blue">
  <div class="wrapx"><table>
  <tr><th></th><th>2027-03-16 전</th><th>2027-03-16 후</th></tr>
  <tr><td>취득세</td><td class="num">8% (중과)</td><td class="num"><b>4% (일반)</b></td></tr>
  <tr><td>사무실·일부 임대·용도 변경</td><td class="num">상관없이 중과</td><td class="num"><b>전부 자유</b></td></tr>
  </table></div>
  <p style="margin:10px 0 0">중과 제외 업종으로 빠지는 길은 '직접 사용' 상태를 몇 년 유지해야 하고 중간에 용도를 바꾸거나 임대로 돌리면 추징됩니다. <b>유연하게 쓰실 계획이라면 애초에 맞지 않는 길</b>입니다. 5년을 넘기면 그 뒤로는 아무것도 신경 쓰지 않아도 됩니다.</p>
  <div class="note">매입 후 <b>증축</b>을 하면 별도 조항(제13조①, 본점 사업용 부동산 신축·증축)이 5년과 무관하게 걸릴 수 있습니다. 리모델링 계획이 있으면 이것도 확인하세요.</div>
</div>

<h2>창고형 매장을 먼저 깔면 생기는 것</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">법인에 '사업 실적'이 생깁니다</div><div class="m">휴면법인 6호의 첫 조건이 "2년 이상 사업 실적이 없고"입니다. 창고형 매장이 돌기 시작하면 이 조건이 깨져서 <b>휴면법인 논의 자체가 끝납니다</b></div></li>
    <li><div class="t">창고업이 사업목적에 실제로 들어갑니다</div><div class="m">서울 건물에서는 못 쓰는 카드지만, 경기 쪽 매장에는 쓸 일이 생길 수 있습니다. 10/15 등기 때 목적에 넣어 두세요</div></li>
    <li><div class="t">순서가 자연스럽습니다</div><div class="m">경기 창고형 매장(지금) → 서울 빌딩(2027-03) 순서면 기다리는 시간을 비워 두지 않아도 됩니다</div></li>
  </ul>
</div>

<h2>지분 51 / 26 / 23 — 맞습니다</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">누구도 50%를 넘기지 않습니다</div><div class="m">루크님이 51%로 지배권 유지. 휴면법인 '인수'로 보기 어렵고, 부동산 보유 법인의 주식이 넘어갈 때 붙는 <b>과점주주 간주취득세</b>도 피합니다</div></li>
    <li><div class="t">49% 한 명보다 쪼개는 게 유리합니다</div><div class="m">상법상 <b>특별결의는 3분의 2</b>라 34% 이상을 가진 주주 한 명이면 단독으로 막습니다. 26·23은 둘 다 34% 미만</div></li>
    <li class="big"><div class="t">지분 이전은 부동산을 사기 전에 끝내세요</div><div class="m">창고형 매장이든 빌딩이든, <b>법인에 부동산이 들어온 뒤</b> 주식을 옮기면 주식 가치가 올라 양도세가 커지고 간주취득세 문제도 생깁니다. 경기 매장을 먼저 사실 거라면 <b>지분 정리가 더 급해집니다</b></div></li>
  </ul>
  <div class="note">제3자가 신정현님과 특수관계인이면 지분이 합산될 수 있습니다 — 합쳐도 49%라 과점주주는 아니지만 특별결의 거부권은 생깁니다.</div>
</div>

<h2>휴면법인 — 임원만 안 바꾸면 됩니다</h2>
<div class="card">
  <div class="wrapx"><table>
  <tr><th>시행령 제27조①6호</th><th>상태</th></tr>
  <tr><td>인수일 이전 <b>2년 이상 사업 실적이 없고</b></td><td>걸릴 가능성 높음 <span class="tag">수입금액 확인 필요</span></td></tr>
  <tr><td>인수일 전후 1년 이내 <b>임원의 50% 이상 교체</b></td><td class="num"><b>안 만들면 됨</b></td></tr>
  </table></div>
  <p style="margin:10px 0 0">두 조건을 <b>모두</b> 충족해야 성립합니다. 임원이 지금 두 분이라 <b>한 분만 바꿔도 50%</b>입니다. 어머니를 감사에서 빼거나 대표이사를 바꾸는 건 피하시고, 신정현님·제3자는 <b>이사로 추가</b> 선임하세요.</p>
  <div class="note">기장료 같은 지출만 있는 것은 '사업 실적'으로 보기 어려울 가능성이 높습니다 — 여기 기대지 마세요. <b>지난 2년 수입금액을 세무사에게 물어보는 게 가장 싼 확인</b>입니다. 이사가 3명 이상이 되면 상법상 이사회를 두게 되어 본점 이전 같은 것도 이사회 결의를 거칩니다.</div>
</div>

<h2>순서</h2>
<div class="card accent">
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">10/8</div><div class="t">세무사에게 지난 2년 수입금액 확인</div><div class="d">전화 한 통. 매출이 있었으면 휴면법인 논의가 바로 끝납니다</div></li>
    <li><div class="d">10/15까지</div><div class="t">본점이전 + 상호변경 + 사업목적을 한 신청서로</div><div class="d">기한이 있는 건 본점이전입니다. 늦어지면 <b>본점이전만 먼저</b>. 목적에는 교육서비스업 · 전자상거래·도소매업 · <b>창고업·물류대행업</b> · 부동산임대업</div></li>
    <li><div class="d">부동산 사기 전</div><div class="t">임원 설계 확정 + 51/26/23 지분 이전</div><div class="d">두 분 유임 + 추가 선임. 경기 매장을 먼저 사실 거라면 이게 먼저입니다</div></li>
    <li><div class="d">지분 정리 후</div><div class="t">경기 외곽 창고형 매장 — 권역 밖이면 바로 진행</div><div class="d">후보지가 과밀억제권역 목록에 없는지만 확인하세요</div></li>
    <li class="big"><div class="d">2027-03-16 이후</div><div class="t">서울 꼬마빌딩 매입</div><div class="d">취득일은 <b>잔금일과 등기일 중 빠른 날</b>. 계약은 먼저 해도 되지만 <b>잔금을 3/16 이후로</b> 맞추세요</div></li>
  </ol>
</div>

<h2>세무사에게 물어보실 것</h2>
<div class="card">
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">"힐링디어스의 최근 2년 수입금액이 0입니까?"</div></li>
    <li><div class="t">"대표이사·감사를 유임하고 이사 두 명을 <b>추가</b> 선임하면 시행령 제27조①6호의 '임원 50% 이상 교체'에 해당하지 않습니까?"</div></li>
    <li><div class="t">"51 / 26 / 23 구조면 휴면법인 '인수'도, 과점주주 간주취득세도 해당하지 않습니까?"</div></li>
    <li><div class="t">"본점이 구리인 법인이 <b>과밀억제권역 밖</b> 경기도에 창고형 매장을 매입하면 취득세 중과가 없는 게 맞습니까? 후보지 ○○시가 권역 밖입니까?"</div></li>
    <li><div class="t">"2027-03-16 이후 서울 건물을 사면 사무실·임대 등 <b>용도와 무관하게</b> 일반 세율이 맞습니까?"</div></li>
    <li class="big"><div class="t">"매입 후 증축이나 대수선을 하면 제13조① 본점 사업용 부동산 중과가 별도로 걸립니까?"</div></li>
  </ol>
</div>

<h2>확인 필요</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">창고형 매장 후보지 3~5곳이 과밀억제권역 밖인지</div><div class="m">경기도에도 권역이 있습니다 — 의정부·구리·하남·고양·수원·성남·안양·부천·광명·과천·의왕·군포, 시흥·남양주 일부</div></li>
    <li><div class="t">창고형 매장을 매입할지 임차할지</div><div class="m">임차면 취득세 논의가 없습니다</div></li>
    <li><div class="t">최근 2년 수입금액</div></li>
    <li><div class="t">제3자가 누구인지 · 신정현님과 특수관계인지</div></li>
    <li><div class="t">서울 빌딩 매입 시점이 2027년 3월 이후로 가능한지 · 리모델링·증축 계획</div></li>
    <li><div class="t">새 본점 주소(구리 시내 비상주 사무실) · 상호 '셀러들의 수다' 확정</div><div class="m">10/15 등기에 들어갈 내용</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거(2026-10-07 확인): 지방세법 제13조②(대도시=과밀억제권역 내 법인 설립·전입 후 5년 이내 <b>그 권역 내</b> 부동산 취득 시 중과, 승계취득 4% → 8%) · 본점이 권역 내여도 권역 밖 취득분은 중과 제외 · 지방세법 제13조①(본점 사업용 부동산 신축·증축 중과) · 시행령 제27조①6호(인수일 이전 2년 이상 사업 실적이 없고, 인수일 전후 1년 이내 임원의 100분의 50 이상 교체) — 조세심판례 인용분 · 시행령 제26조①의 중과 제외 업종에 유통산업·물류터미널사업·창고업 포함, 교육업 미포함(법무 서비스 업체 정리 기준) · 중과·제외 업종 겸업 시 안분 관련 조세심판례 존재 · 임대 매장도 '직접 사용'으로 본 대법원 2019-09-10 판결(유통산업 사안) · 과밀억제권역 범위(수도권정비계획법 시행령 별표1, 중소벤처기업부 온라인법인설립시스템 안내) · 상법상 특별결의 3분의 2 · 설립 2022-03-16 → 5년 충족일 2027-03-16. <b>확인하지 못한 것: '사업 실적'의 유권해석, 임원 '추가 선임'이 '교체'인지, 휴면법인 '인수'의 지분 비율 기준, 과점주주 간주취득세의 정확한 요건, 증축·대수선 시 제13조① 적용 범위, 개별 후보지의 권역 포함 여부. 세무사 확인 전에는 실행하지 마세요.</b> 금액은 본세만 단순 곱한 예시입니다.</div>
"""
# ---------------------------------------------------------------- 메이브님 공동 액션 플랜
MAVEN = """
<h1>메이브님 공동 액션 플랜</h1>
<p class="note">10/6 15:00 메이브님(신정현) 회의 녹음(30분)에서 뽑은 것입니다. 인베이더 종료 이야기를 들은 바로 그날 잡은 회의라, <a href="../invader/">강의 수입이 줄 때 무엇으로 받칠 것인가</a>가 사실상 이 회의의 주제였습니다.</p>

<h2>한 줄로</h2>
<div class="card accent">
  <p style="font-size:17px;font-family:'Gowun Dodum',sans-serif;margin:0">강의에서 나오던 돈을 <b>① 프로그램 구독 ② 메이븐 스토어 ③ 오프라인·가격비교</b> 세 곳으로 옮긴다.</p>
  <p class="note">셋 다 이미 있던 것입니다. 새로 벌이는 게 아니라 <b>일회성을 반복으로, 취미 규모를 생계 규모로</b> 바꾸는 작업입니다.</p>
</div>

<h2>① 프로그램을 구독으로 <small>루크 툴박스 구체화</small></h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">[결정] 일회성 판매 → 구독으로 전환</div><div class="m">유지보수 이슈 때문. 한 번 팔고 끝나면 고칠 때마다 손해가 납니다</div></li>
    <li><div class="t">사이트 구성</div><div class="m">셀러용 자동화 프로그램이 중심 · 부업 콘텐츠 · <b>수강생 전용 라운지</b> · 토스 연동 결제</div></li>
    <li><div class="t">배포는 깃허브로</div><div class="m">자동 업데이트·설치. 사람이 설치 안내할 일이 없어야 구독이 돈다</div></li>
    <li><div class="t">비수강생 대상 오픈</div><div class="m">지금까지 수강생 안에서만 돌던 도구를 밖으로. 강의 유입이 줄어도 도는 쪽</div></li>
    <li><div class="t">1인 사업자용 별도 사이트</div><div class="m">블로그·카톡 자동화 등 마케팅 도구 묶음. 셀러가 아닌 시장</div></li>
    <li><div class="t">수익 분배는 개발자별 차등 <span class="tag">검토 중</span></div><div class="m">만든 사람에 따라 비율을 다르게 — 기준 미정</div></li>
    <li><div class="t">홍보는 유튜브로 <span class="tag">루크·메이브님</span></div><div class="m">"프로그램이 이렇게 많다"를 보여주는 것이 목적</div></li>
  </ul>
</div>

<h2>② 메이븐 스토어를 생계 규모로 <small>숫자가 분명한 유일한 축</small></h2>
<div class="card blue wrapx">
<table>
<tr><th></th><th>지금</th><th>목표</th></tr>
<tr><td>월 순수익</td><td class="num">80~100만</td><td class="num">1,000만 <small>(4분기)</small></td></tr>
<tr><td>물동량</td><td class="num">월 2,300건 <small>(이번 달 예상)</small></td><td class="num">일 200 · 월 6,000건</td></tr>
</table>
<ul class="list" style="margin-top:10px">
  <li><div class="t">물동량을 올리는 이유가 두 개</div><div class="m">① 택배비 협상력 ② 보라 대표 인건비 충당. 매출 자체보다 <b>구조를 버티게 하는 숫자</b>입니다</div></li>
  <li><div class="t">방법</div><div class="m">스토어 재정비(이번 주) · 집중 품목 선정 · 사입 비중 확대 · 수강생 보유 재고 위탁판매</div></li>
  <li><div class="t">역할 분담</div><div class="m">메이브님은 스토어 수익에 집중 / 루크는 <b>매출 상위 상품 링크를 받아</b> 추가 판매 전략을 짬</div></li>
</ul>
<div class="note">80~100만에서 1,000만은 10배입니다. 물동량 목표(2,300 → 6,000)는 2.6배이므로, 나머지는 객단가·마진에서 나와야 합니다 — 집중 품목 선정이 그래서 핵심입니다. 달성 가능성은 계획값이며 검증 전입니다.</div>
</div>

<h2>③ 오프라인·가격비교 <small>지영 원장과</small></h2>
<div class="card">
  <ul class="list">
    <li><div class="t">헤어·메이크업 가격비교 사이트 + 커뮤니티 — 구축 중</div><div class="m">지도에서 '구상'이던 것이 '세우는 중'으로 올라갔습니다. 모델은 강남언니 벤치마킹</div></li>
    <li><div class="t">[결정] 가격은 공지된 것만 쓴다</div><div class="m">수집의 법적 이슈를 피하기 위해. 쿠팡 가격비교 쪽 크롤링은 플랫폼 정책 위반 가능성이 지적돼 <b>법적 검토 전에는 개발 보류</b></div></li>
    <li><div class="t">사무실 이전 — 보류했다가 재검토</div><div class="m">추가 보증금 부담으로 한 번 접었으나, 더 나은 상권을 위해 서울 시내 빌딩으로 재검토 중. <b>공동 투자자 물색</b> 중이며 자금 조달 계획은 아직 없음</div></li>
    <li><div class="t">돈벌쥐 PD 오프라인 사업 수익 구조화</div><div class="m">회의에서 과제로 나왔으나 범위·형태 확인 필요</div></li>
  </ul>
</div>

<h2>수강생 사입 재고 — 규칙을 만든다 <small>가장 즉시 효과 나는 것</small></h2>
<div class="card accent">
  <p style="margin:0 0 8px">수강생이 사입 재고 부담을 크게 느끼는 것이 사입 참여를 막고 있습니다. 회의에서 나온 해법:</p>
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">50일 경과 미판매 재고는 마진을 낮춰 원금 회수</div><div class="d">기간 기준을 주는 것만으로 "언제까지 안 팔리면 어떡하지"가 사라집니다</div></li>
    <li><div class="t">원금 회수도 어려우면 강사에게 재고 처리 신청</div><div class="d">3PL·재고 외부 판매와 그대로 이어집니다 — 이미 있는 창고와 판매 경로를 쓰는 것</div></li>
    <li><div class="t">신청 목록을 관리하며 순차 처리</div><div class="d">전부 즉시 받아주면 감당이 안 되므로 대기열로. 받아주는 속도가 곧 약속</div></li>
    <li class="big"><div class="t">'사입으로 수익 낸 사례' 특강을 계속 연다</div><div class="d">안전장치를 만들고 성공 사례를 보여주는 두 가지가 같이 가야 사입이 돕니다</div></li>
  </ol>
  <div class="note">이 규칙은 원크루·일십백천 판매에도 그대로 쓰입니다 — "최악이어도 재고는 회수된다"는 문장이 생기기 때문입니다.</div>
</div>

<h2>액션 플랜</h2>
<div class="card wrapx">
<table>
<tr><th>언제</th><th>무엇</th><th>누가</th></tr>
<tr><td><b>이번 주</b></td><td>스토어 재정비 완료 + 집중 품목 선정</td><td>메이브님</td></tr>
<tr><td><b>이번 주</b></td><td>사입 재고 처리 가이드라인 수립 (50일 규칙 · 신청 접수 · 대기열 운영)</td><td>루크</td></tr>
<tr><td><b>이번 주</b></td><td>토스 연동 + 깃허브 자동 업데이트·설치 세팅</td><td>루크</td></tr>
<tr><td><b>이번 주</b></td><td>뿌요 역할·수익 구조 결정 <span class="tag p0">미결</span></td><td>루크·메이브님</td></tr>
<tr><td><b>이번 주</b></td><td>세무사 상의 — 2,000만 지출 처리 방식 결정 <span class="tag p0">미결</span></td><td>루크</td></tr>
<tr><td>10월</td><td>프로그램 구독 사이트 구축 (수강생 라운지·부업 콘텐츠 포함)</td><td>루크</td></tr>
<tr><td>10월</td><td>헤어·메이크업 가격비교 사이트 + 커뮤니티 완성</td><td>루크·지영 원장</td></tr>
<tr><td>10월</td><td>스토어 불필요 프로세스 정리 / 물량 증가 대응 시스템</td><td>보라 대표</td></tr>
<tr><td>10월</td><td>매출 우수 상품 발견 시 즉시 링크 공유 → 판매 전략 세팅</td><td>메이브님 → 루크</td></tr>
<tr><td>10~12월</td><td>스토어 월 순수익 1,000만 / 일 200건·월 6,000건</td><td>메이브님</td></tr>
<tr><td>10~12월</td><td>비수강생 대상 구독 사이트 오픈 · 유튜브로 프로그램 홍보</td><td>루크·메이브님</td></tr>
<tr><td>미정</td><td>서울 빌딩 후보 정보 수집 + 공동 투자자 <span class="tag">자금 계획 없음</span></td><td>루크</td></tr>
<tr><td>미정</td><td>돈벌쥐 PD 오프라인 사업 수익 구조화 <span class="tag">범위 확인 필요</span></td><td>루크</td></tr>
</table>
</div>

<h2>결론이 안 난 것 네 가지 <small>이번 주에 닫아야 하는 것</small></h2>
<div class="card red">
  <ul class="list">
    <li><div class="t">뿌요의 역할과 수익 구조</div><div class="m">한 달 알바 형태로 약 450만 지급 논의가 있었으나, 이후 역할·배분 비율·자생 방안이 모두 미확정입니다. 사람 문제는 미루면 비용이 복리로 붙습니다 — <b>장기 거취부터 정하고 그다음 금액</b></div></li>
    <li><div class="t">세무 처리 — 2,000만 지출</div><div class="m">1,000만을 루크에게 지급하는 방식 vs 2,000만 유지. 세무사와 상의 후 결정하기로 했으나 아직 미결. 분기 마감 전에 닫는 게 깔끔합니다</div></li>
    <li><div class="t">사무실 이전 자금</div><div class="m">보증금 조달 계획이 "공동 투자자 물색" 외에 없습니다. <b>투자자를 찾을 것인지, 이전을 미룰 것인지</b> 둘 중 하나를 고르는 게 먼저</div></li>
    <li><div class="t">쿠팡 가격비교 크롤링</div><div class="m">수강생 내부용이라도 플랫폼 정책 위반 가능성이 있습니다. 헤어·메이크업 쪽에서 쓰기로 한 '공지된 가격만' 원칙을 여기에도 그대로 적용할지 결정 필요</div></li>
  </ul>
</div>

<h2>인베이더 건과 어떻게 맞물리는가</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">타이밍이 맞아떨어졌다</div><div class="m">강의 유입이 줄어드는 바로 그 시점에 구독·스토어·오프라인 세 축을 올리는 회의였습니다. 우연이지만 순서는 맞습니다</div></li>
    <li><div class="t">다만 셋 다 '씨 뿌리기'다</div><div class="m">구독 사이트·가격비교·스토어 10배는 전부 11~12월에야 돈이 됩니다. <b>10~11월 현금은 여전히 원크루 전환과 마지막 기수에서 나옵니다</b> — 그쪽을 비우면 안 됩니다</div></li>
    <li><div class="t">수강생 재고 규칙이 둘을 잇는다</div><div class="m">사입 안전장치는 지금 당장 원크루 상담에서 쓸 수 있는 문장이면서, 동시에 3PL 재고 판매의 물건을 모아줍니다 — 이번 주 항목 중 가장 수지가 맞습니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: 10/6 15:00 메이브님(신정현) 회의 녹음 요약 노트(30분). 금액·목표는 회의에서 나온 계획값이며 실적이 아닙니다. '돈벌쥐 PD'는 녹음에 '돈블지PD'로 표기됨 · '뿌요'는 '뿌연'으로 표기됨 — 표기 확인 필요. 세 번째 사람 '보라 대표'는 이 회의에서 처음 나온 이름으로, 역할 확인 필요.</div>
"""

# ---------------------------------------------------------------- 인베이더 종료 대비
INVADER = """
<h1>인베이더 종료 대비</h1>
<p class="note">10/6 루크가 들은 이야기 기준입니다. <b>확정된 사실이 아니라 전해 들은 것</b>이고, 아래 판단은 그 전제 위에서 세운 대비안입니다. 뒤집히면 그때 지우면 됩니다.</p>

<h2>들은 것 <small>10/6</small></h2>
<div class="card red">
  <ul class="list">
    <li><div class="t">인베이더가 강의를 접을 것 같다</div><div class="m">전해 들은 이야기 · 시점·범위 확인 필요</div></li>
    <li><div class="t">뷰셀(메이브님)은 이번 <b>4기가 마지막</b></div><div class="m">기수 일정 확인 필요</div></li>
    <li><div class="t">루크는 이번 <b>6기가 마지막일 확률이 높다</b></div><div class="m">기수 일정 확인 필요</div></li>
    <li><div class="t">이번 기수는 <b>광고비를 쓰지 않고 유튜브 채널에만 의존</b>해서 운영</div><div class="m">인베이더 쪽 방침</div></li>
  </ul>
</div>

<h2>이미 있던 전조 <small>기록에서</small></h2>
<div class="card">
  <ul class="list">
    <li><div class="t">10/2 — 인베이더 관련 촬영이 한꺼번에 끊겼다</div><div class="m">돈벌쥐 PD 인터뷰에서 나온 이야기. 외부 채널 촬영이 전부 빠지면서 여러 사람이 생계 타격을 체감했고, 타이탄이 인베이더에서 분리된 것 같다는 말도 함께 나왔습니다 — 광고·제작비부터 줄인 흐름</div></li>
    <li><div class="t">9/29 — 인베이더 없이 가는 플랫폼을 이미 설계 중</div><div class="m">메이브님과의 회의에서 3자 구도(모객·락인·플레이어)를 짜고 10/8 본부장 미팅까지 잡아둔 상태. <a href="../platform/">전략 페이지</a></div></li>
    <li><div class="t">원칙에 이미 적혀 있던 것</div><div class="m">"인베이더를 통한 수취율 20%는 매출 엔진이 아니라 <b>리스트 확보 엔진</b>이다. 자체 런칭(50%)이 물량 엔진이고 직접 고가(90% 마진)가 마진 엔진이다"</div></li>
  </ul>
</div>

<h2>그래서 무엇이 끊기는가</h2>
<div class="card wrapx">
<table>
<tr><th>인베이더가 해주던 것</th><th>끊기면</th><th>대체</th></tr>
<tr><td><b>신규 명단</b> — 광고로 사람을 모아 특강에 앉혀주던 것</td><td>가장 큰 손실. 매출보다 <b>리스트 유입</b>이 끊긴다</td><td>유튜브·카톡·카페 자체 리스트 + 신규 플랫폼 모객 축</td></tr>
<tr><td><b>광고비 집행</b> — 돈을 대신 태워주던 자리</td><td>이번 기수부터 이미 없음(유튜브만)</td><td>자체 광고 상한 설정 · 1기 1,000만 선</td></tr>
<tr><td><b>판 깔기</b> — 기수 운영·결제·고객 응대 틀</td><td>우리가 직접 짜야 함</td><td>신규 플랫폼 3자 구도(락인 축이 담당)</td></tr>
<tr><td>수취율 20%</td><td>안 떼이는 게 이득</td><td>자체 런칭은 배분 1/3, 직접 판매는 거의 전부</td></tr>
</table>
<div class="note">핵심은 돈이 아니라 <b>사람이 들어오던 입구</b>가 닫힌다는 것입니다.</div>
</div>

<h2>이번 기수가 마지막이라면, 반드시 챙길 것 <small>순서대로</small></h2>
<div class="card accent">
  <ol class="tl" style="margin-top:6px">
    <li><div class="t">수강생 명단을 우리 쪽으로 옮긴다</div><div class="d">인베이더 기수가 끝나면 그 명단은 남의 것입니다. 카톡 오픈채팅·네이버 카페·유튜브 멤버십 중 <b>최소 한 곳</b>에 들어오게 하는 동선을 이번 기수 안에 넣어야 합니다. 자료 배포·질의응답·사례집을 미끼로. 개인정보 수집은 동의 받고.</div></li>
    <li><div class="t">마지막 기수를 증거로 남긴다</div><div class="d">신규 플랫폼 1기를 모집할 때 필요한 것은 말이 아니라 숫자입니다. 6기·4기 수강생의 성과·후기·비포애프터를 <b>지금</b> 모아두세요. 끝나고 나면 연락이 안 됩니다.</div></li>
    <li><div class="t">PD·본부장 미팅을 앞당긴다</div><div class="d">10/5 초이스토리 PD · 10/8 종혁 본부장이 잡혀 있습니다. 인베이더가 접는다는 이야기는 이 미팅의 <b>명분이자 타이밍</b>입니다 — "그 자리가 비니 우리가 한다"가 설득 한 줄이 됩니다. 다만 들은 이야기이므로 단정해서 말하지는 마세요.</div></li>
    <li class="big"><div class="t">강사·촬영 인력이 흩어지기 전에 잡는다</div><div class="d">10/2 녹음대로라면 인베이더 라인의 영상 PD·강사들이 이미 일감이 끊긴 상태입니다. 신규 플랫폼에 필요한 사람을 지금 데려오기 가장 싼 때입니다.</div></li>
  </ol>
</div>

<h2>광고 없이 유튜브만으로 가면 <small>숫자가 어떻게 달라지나</small></h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">신청자 수는 준다 — 각오할 것</div><div class="m">광고로 밀어 넣던 인원이 빠집니다. 추석 특강 100명 신청 같은 규모는 기대하기 어렵습니다 (감소 폭은 예측 불가 · 확인 필요)</div></li>
    <li><div class="t">대신 들어오는 사람의 질은 올라간다 — 루크 본인이 한 말</div><div class="m">"광고 보고 바로 결제했지만 영상도 충분히 안 본 수강생은 신뢰가 낮아 관리가 어렵다. 영상을 많이 보고 비교·연구를 거쳐 들어온 사람은 신뢰도가 높다" (10/2 녹음). 유튜브만 남으면 뒤쪽만 들어옵니다</div></li>
    <li><div class="t">그러니 이번 기수는 '수'가 아니라 '전환'으로 본다</div><div class="m">신청자 수가 절반이 되어도 원크루 전환이 같으면 손해가 아닙니다. 애초에 목표가 1~2명(3,300~3,900만) 전환입니다</div></li>
    <li><div class="t">영상 쪽에 더 실어야 한다</div><div class="m">유입이 유튜브 하나로 좁아지면 업로드 주기와 영상 설명란 동선이 그대로 매출선이 됩니다. <b>10월 말 무료 라이브 신청 링크</b>가 더 중요해졌습니다</div></li>
  </ul>
</div>

<h2>대체 입구 세 개 <small>어디로 사람을 받을 것인가</small></h2>
<div class="card">
  <ul class="list">
    <li><span class="tag p0">P0</span><div class="t">신규 강의 플랫폼 — 10/8 본부장 미팅</div><div class="m">인베이더 자리를 그대로 대신하는 구조. 모객(PD) · 락인(본부장) · 플레이어(루크·메이브님). 250만×20명 = 5,000만 · <a href="../platform/">전략</a></div></li>
    <li><span class="tag p0">P0</span><div class="t">10월 말 무료 라이브 — 자체 리스트 만들기</div><div class="m">남의 명단이 아니라 내 명단을 만드는 유일한 직접 경로. 10/25(일) 19:00 언급 · 확정 여부 확인 필요 · <a href="../guides/free-live/">설명서</a></div></li>
    <li><span class="tag p1">P1</span><div class="t">원크루 직접 판매</div><div class="m">기수 모집 없이도 문의 하나가 3,300만. 유튜브·블로그 검색 유입에서 바로 상담으로 가는 동선을 이번 달에 손보는 게 수지가 맞습니다</div></li>
  </ul>
</div>

<h2>지금 확인해야 할 것</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">인베이더 종료가 사실인지, 어느 범위인지</div><div class="m">강의 사업만인지 전체인지 · 언제까지인지 · 누구에게서 들은 이야기인지</div></li>
    <li><div class="t">6기·4기 일정</div><div class="m">모집 시작·종료, 강의 기간. 명단 확보 동선을 넣을 수 있는 마지막 시점이 언제인지</div></li>
    <li><div class="t">계약 조건</div><div class="m">수강생 명단·콘텐츠·후기의 소유가 계약서에 어떻게 적혀 있는지. 명단을 우리 쪽으로 받는 것이 가능한 조건인지</div></li>
    <li><div class="t">메이브님과 입을 맞출 것</div><div class="m">4기·6기를 같이 마지막으로 치른다면, 두 사람이 같은 동선으로 명단을 모아야 합치는 의미가 있습니다</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: 10/6 루크 구두(인베이더 종료 전망·4기/6기·광고 없이 유튜브 의존 — 전해 들은 이야기, 미확정) · 10/2 돈벌쥐 PD 인터뷰 녹음(인베이더 촬영 중단, 타이탄 분리설, 광고 유입 수강생의 신뢰도) · 9/29 메이브님 회의 녹음(인베이더 실패 분석·3자 구도·10/8 미팅) · 프로젝트 원칙(수취율 20% = 리스트 엔진). 감소 폭·전환율 등 숫자는 예측이며 실적이 아닙니다.</div>
"""

# ---------------------------------------------------------------- 사업 유니버스 지도
UNI_REGIONS = [
 {"id":"ch","no":"①","name":"채널·브랜딩","sub":"신뢰 → 유입","color":"#4fd1a5","ax":90,"ay":130,
  "desc":"사람이 나를 알게 되는 입구. 이 구역이 꺼지면 나머지 구역의 신규 유입이 멈춥니다.",
  "nodes":[
   {"id":"yt","n":"유튜브 1만","full":"유튜브 멘토루크","st":"on","big":1,"d":"구독자 약 1만 명. 주 1개 공개 강의 업로드 유지. 멤버십 4,900원(특강 풀버전·월 상품 브리핑) 개설 예정."},
   {"id":"cafe","n":"네이버 카페","full":"네이버 카페","st":"on","d":"선판매·공지 라인. 신규 강의 플랫폼에서는 이 역할을 '락인 축'이 맡는 구조로 설계 중."},
   {"id":"kakao","n":"카톡 1천","full":"카카오톡 커뮤니티","st":"on","d":"약 1,000명. 특강 공지와 선판매가 여기서 돕니다."},
   {"id":"vcell","n":"뷰셀 채널","full":"뷰셀 채널 (메이브님)","st":"on","d":"화장품 쪽 유입. 2화 촬영 완료, 10/7 공개 예정."},
   {"id":"live","n":"무료 라이브","full":"10/25 무료 라이브 특강","st":"build","d":"10/6 촬영에서 확정 — 4종 자판기 전체 시스템 사용법과 저가 소싱 노하우를 공개하고, 고정 댓글 링크로 단톡방에 들어온 시청자 전원에게 자동 등록 자판기 7일 무료 이용권을 지급. 남의 명단이 아니라 내 명단을 만드는 자리이자 12월 초월스토리 런칭 퍼널의 리허설. 시각은 10/25(일) 19:00로 언급됨 — 재확인 필요.","href":"../guides/free-live/","hl":"설명서"},
   {"id":"mktg","n":"마케팅 대행","full":"SNS 채널 운영 대행","st":"build","exp":1,"d":"유튜브·인스타그램·틱톡 채널 운영(영상 업로드 포함)을 마케팅 업체에 맡기는 협업. 유튜브는 업체가 운영 전반을 맡는 구조라 '편집자' 권한으로, 틱톡은 기존 개인 계정 대신 브랜드용 신규 계정을 새로 만들어 넘기기로 결정.","from":"마케팅 업체와의 협의 (9/14)"},
   {"id":"blog","n":"멘토루크 블로그","full":"멘토루크 블로그","st":"build","exp":1,"d":"플라우드 녹음을 자동 수집해 글감으로 쓰는 루크 전용 블로그. 글 틀과 발화 분석(내 말 비율·상대 발화 수)까지 붙어 있음.","from":"클로드 코드 작업 보고 (10/4)"},
   {"id":"commu","n":"고객 커뮤니티 사이트","full":"고객 커뮤니티 사이트","st":"idea","exp":1,"d":"정보 게시 중심의 자체 커뮤니티 사이트. 9/28 회의에서 루크가 개발하려는 세 사이트 중 하나로 언급됨.","from":"9/28 회의 (메이브님·디노)"},
   {"id":"trade","n":"개인 트레이드 채널","full":"개인 트레이드 채널","st":"idea","exp":1,"d":"9/29 메이브님 회의에서 루크 개인 과제로 나온 신규 채널. 다루는 내용과 플랫폼은 아직 기록이 없어 확인 필요.","from":"9/29 메이브님 회의"},
  ]},
 {"id":"kn","no":"②","name":"지식·교육","sub":"신뢰 → 매출","color":"#e3b04b","ax":280,"ay":180,
  "desc":"신뢰를 돈으로 바꾸고, 검색·추천으로 새 사람을 데려오는 줄. 금액은 모두 계획값이며 실적이 아닙니다.",
  "nodes":[
   {"id":"onecrew","n":"원크루","full":"원크루 (ONE CREW)","st":"on","big":1,"d":"평생 파트너십 컨설팅. 정가 3,900만 / 루크 수강생 출신 3,300만. 한 사람의 삼각 파이프라인을 같이 설계하고 세우는 것이 목표.","href":"../philosophy/","hl":"삼각 파이프라인"},
   {"id":"ilsip","n":"일십백천","full":"일십백천","st":"on","d":"990만. 삼각형 중 '브랜딩' 한 축에 집중하는 브랜드 인큐베이팅. 약 400개 영상 강의 + 1:1. 수료자가 원크루로 올라오는 사다리.","href":"../philosophy/","hl":"삼각 파이프라인"},
   {"id":"plat","n":"강의 플랫폼","full":"신규 강의 플랫폼","st":"build","big":1,"d":"메이브님과 3자 구도(모객 / 락인 / 플레이어). 250만×20명 = 5,000만, 광고 약 1,000만 제외 4,000만. 3인이면 25명에 각 1,300만. 10/5 PD 미팅 → 10/8 종혁 본부장 미팅.","href":"../platform/","hl":"전략 페이지"},
   {"id":"toolkit","n":"300만 툴킷","full":"300만 툴킷 프로그램","st":"idea","d":"자동등록+소명서+연출컷 1년 + 8주 코칭 + 파일 구독 = 300만. 1기 8명 목표."},
   {"id":"dino","n":"디노 12주","full":"디노(미니쌤) 12주 빌드업","st":"build","d":"AI 셀러 실무 교육 라인. 1달 90 / 2달 200 / 3달 350만 기준, 상품별 배분 비율 확정 필요. 10/5 1주차 시작.","href":"../guides/dino-12weeks/","hl":"설명서"},
   {"id":"kititi","n":"키티티 컨설팅","full":"키티티바이지영 컨설팅","st":"on","d":"윤지영 원장(성신여대 인근 메이크업 샵)의 브랜딩·확장 자문. 상표 출원 진행 중, 2월 샵 오픈 목표, 상담 사이트 운영. 월 고정 자문 + 매출 연동으로 유료 전환이 과제.","href":"../grants/","hl":"정부지원사업 정리"},
   {"id":"sudan","n":"셀러들의 수다","full":"셀러들의 수다 (신규 교육회사)","st":"idea","exp":1,"d":"메이브님(신정현)과 운영하려는 교육회사 — 교육에 3PL을 묶은 형태. 신규 법인 설립 vs 힐링디어스 상호 변경 후 이사 선임 사이에서 고민 중이고, 이사로 들이면 기존 재무가 보일 수 있어 신규 설립 쪽으로 기울어 있음.","from":"메이브님과의 법인 논의 (10/2)"},
   {"id":"own","n":"자체 강의 2027","full":"회사 자체 강의 (2027)","st":"idea","exp":1,"d":"내년에 회사 이름으로 직접 강의를 열고, 3PL 재고 판매와 연계하려는 구상.","from":"3PL 수익 구상 (9월)"},
   {"id":"chowol","n":"초월스토리","full":"초월스토리 (강사 협업)","st":"build","exp":1,"d":"10/6 구두 합의 — 루크가 강사 섭외·강의 기획·PPT·라이브 코칭·프로그램 공유를 맡고, 초월스토리는 PG 수수료를 제외한 전체 매출의 8%를 고정 수수료로 지급. 강사와는 모든 비용을 뺀 순수익을 5:5. 289만 단일 상품이 유력하고 12월 초 유튜브 라이브로 30~40명 모집이 초기 목표. 문서화 전이며 비용 정의·참여 범위가 미확정.","from":"10/6 초월스토리 회의","href":"../chowol/","hl":"협업 조건 페이지"},
   {"id":"gaeul","n":"가을 강의 40명","full":"가을(정복녀) 대표님 강의 — 초월스토리","st":"build","big":1,"exp":1,"d":"10/7 루크 구두 — 가을 대표님이 초월스토리와 함께 강의 기획에 들어감. 후보 둘 중 미결이던 파일럿 강사가 사실상 확정된 것. 루크는 두 번 받는 구조다 — ① PG 제외 매출의 8%를 비용 차감 전에 먼저, ② 초월스토리:가을 5:5로 나눈 가을 몫에서 다시 6:4. 40명·289만·PG 3.5% 가정이면 ①이 892만이다. ②는 가을 대표님 6 : 루크 4이고 기준은 초월스토리가 제시할 약 2,200만이라, 루크 4는 880만·루크 합계 1,772만이 된다. 기준을 제시 상단 3,200만으로 두면 2,172만, 내 계산값 3,975만으로 두면 2,482만까지 올라간다 — 2,200만의 산출 근거를 초월스토리가 설명하지 않았으므로 그 비용 가정을 먼저 물어야 한다. 6:4는 초월스토리가 모르는 별도 계약이라 10/6 회의 녹음에는 없다. 모두 계획값.","from":"10/7 루크 구두","href":"../pilot/","hl":"파일럿 강사 결정"},
   {"id":"invader","n":"인베이더","full":"인베이더 (기수 강의 제휴)","st":"off","d":"지금까지 기수 강의로 신규 명단을 대 주던 제휴처. 수취율 20%는 매출 엔진이 아니라 리스트 확보 엔진이었습니다. 10/6에 '강의를 접을 것 같다'는 이야기를 들었고, 뷰셀은 4기·루크는 6기가 마지막일 확률이 높으며 이번 기수는 광고 없이 유튜브에만 의존해 돈다고 합니다. 모두 전해 들은 이야기로 미확정.","from":"10/6 루크 구두 (전해 들은 이야기)","href":"../invader/","hl":"종료 대비 페이지","exp":0},
   {"id":"callai","n":"전화 상담 AI","full":"전화 상담 AI","st":"idea","exp":1,"d":"'이거 괜찮은 겁니까' 유형의 계약 문의 전화가 매우 많고 녹음이 100건 넘게 있음(한 통 10~30분). 이 사례들을 분석해 해당 유형만이라도 AI가 답하게 만들려는 구상.","from":"상담 전화 자동화 논의 (9/17)"},
  ]},
 {"id":"pr","no":"③","name":"상품·유통","sub":"반복 → 회전","color":"#8fb0ff","ax":268,"ay":600,
  "desc":"신뢰가 없어도 상품 자체로 유입이 생기는 줄. 채널이 쉬어도 돈이 끊기지 않게 받쳐주는 자리입니다.",
  "nodes":[
   {"id":"tpl","n":"3PL 물류","full":"3PL 물류 대행","st":"on","big":1,"d":"수강생 재고 보관·출고 대행. 뿌요가 운영. 입고 미처리 상태에서 운송장이 나가는 오류를 잡는 안정화가 진행 중.","href":"../guides/logistics-stabilize/","hl":"설명서"},
   {"id":"resale","n":"재고 판매","full":"수강생 재고 외부 판매","st":"build","d":"창고에 잠든 수강생 재고를 회사가 당근·번개장터·네이버에서 판매하고 수수료 15~20%. 동의서 → 재고 시트 → 당근 비즈프로필 → 30개 등록 순서. 10/6 회의에서 규칙 합의 — 사입 50일이 지나도 안 팔리면 마진을 낮춰 원금 회수, 그래도 어려우면 강사에게 재고 처리를 신청하고 신청 목록을 대기열로 순차 처리.","href":"../guides/3pl-resale/","hl":"설명서"},
   {"id":"store","n":"창고형 매장","full":"오프라인 창고형 매장","st":"idea","exp":1,"d":"창고 재고를 오프라인에서 직접 파는 구조. 고정비가 낮은 오픈데이+온라인 판매 모델을 더 무거운 대안보다 먼저 두기로 한 기록이 있음. 위치·평수·운영 인력·취급 품목은 아직 미정 — 확인 필요.","from":"3PL 수익 구상 (10월)"},
   {"id":"toolbox","n":"루크 툴박스","full":"루크 툴박스","st":"build","big":1,"d":"월 19,900 / 연 199,000, 오프라인샵 팩 +9,900. 아래 도구들을 하나의 구독으로 묶어 파는 자리. 12월 500명 → 3월 1,000명 목표. 개발자 계정 3종 등록이 모든 배포의 앞단. 10/6 메이브님 회의에서 구체화 — 일회성 판매 대신 구독으로 전환(유지보수 때문), 토스 연동 결제, 깃허브 자동 업데이트·설치, 수강생 전용 라운지와 부업 콘텐츠를 같이, 비수강생에게도 열어 신규 유치, 1인 사업자용 마케팅 도구 사이트는 따로, 수익은 개발자별 차등 분배 검토 중.","href":"../guides/developer-accounts/","hl":"개발자 계정 설명서"},
   {"id":"mvstore","n":"메이븐 스토어","full":"메이븐 스토어 (신정현)","st":"on","d":"메이브님이 직접 돌리는 스마트스토어. 지금 월 순수익 80~100만, 이번 달 물동량 2,300건 예상. 4분기 목표는 월 순수익 1,000만과 일 200건·월 6,000건 — 물동량을 올리는 이유는 매출보다 택배비 협상력과 보라 대표 인건비 충당. 스토어 재정비·집중 품목 선정·사입 비중 확대·수강생 재고 위탁판매로 간다.","from":"10/6 메이브님 회의","exp":1},
   {"id":"consign","n":"위탁판매","full":"위탁판매 (메이크업헬퍼)","st":"build","d":"원크루 최은봉 대표 건. 위수탁계약서 기준(사입 아님). 국내는 토스·당근 등 브랜드사 미입점 플랫폼·폐쇄몰·공동구매, 해외는 쇼피·큐텐재팬·이베이. 12주 테스트, 광고 상한 약 189만, 11월 말 판정."},
   {"id":"giant","n":"거인의 도구공방","full":"거인의 도구공방 (신규 판매 채널)","st":"build","big":1,"exp":1,"d":"10/8 루크 업무지시 — 4분기 '신규채널 수익화'로 거인의 도구공방 사이트 판매를 시작한다. 자체 사이트에서 직접 파는 첫 채널이라, 스마트스토어·오픈마켓과 달리 플랫폼 수수료와 노출 규칙에서 벗어나 있다. 같은 분기에 오프라인 판매도 '물류가 좀 정리되면' 시작할 계획이어서 두 줄이 물류 보완에 함께 걸려 있다. 취급 품목·가격·사이트 구축 상태·오픈 시점은 아직 기록이 없어 확인 필요.","from":"10/8 루크 업무지시"},
   {"id":"beauty","n":"미용 가격비교","full":"헤어·메이크업 가격비교 사이트","st":"build","exp":1,"d":"지영 원장과 함께 구축 중. 가격 수집의 법적 이슈를 피해 공지된 가격만 쓰기로 했고, 커뮤니티를 함께 붙여 강남언니식 플랫폼 수익 구조를 벤치마킹할 계획. 쿠팡 가격비교 쪽 크롤링은 플랫폼 정책 위반 가능성이 지적돼 법적 검토 전까지 보류.","from":"10/6 메이브님 회의"},
  ]},
 {"id":"base","no":"④","name":"기반·자금","sub":"받치는 땅","color":"#b79cff","ax":78,"ay":560,
  "desc":"세 줄을 떠받치는 바닥. 돈을 버는 줄은 아니지만 여기가 흔들리면 위의 셋이 같이 흔들립니다.",
  "nodes":[
   {"id":"grant","n":"정부지원사업","full":"정부지원사업","st":"build","d":"루크 본인은 해당 없고 지영 원장·메이브님·디노·뿌요가 대상. 2026년 해당분 정리와 2027년 도전 리스트(지원금·자격·과제·경쟁률)를 따로 모아 뒀습니다.","href":"../grants/","hl":"정부지원사업 페이지"},
   {"id":"corp","n":"힐링디어스(주)","full":"힐링디어스(주)","st":"on","d":"설립 후 매출 없이 유지된 업력 약 5년 법인. 스칸센 A동 709호는 9/30부로 계약 종료, 새 본점은 비과밀억제권역을 피해 구리 시내 비상주 사무실로 알아보기로 함."},
   {"id":"seoul","n":"서울 이전·건물","full":"서울 이전 · 건물 매입","st":"idea","exp":1,"d":"내년 초 사무실·강의장을 서울로, 현 사무실은 창고·물류 거점으로. 월 렌트가 300~500만을 넘어가면 자체 건물 매입을 검토. 10/6 기준 — 추가 보증금 부담으로 한 번 보류했다가 더 나은 상권을 위해 서울 시내 빌딩으로 재검토 중이며 공동 투자자를 물색. 자금 조달 계획은 아직 없음.","from":"9/29 · 10/6 메이브님 회의"},
  ]},
 {"id":"tool","no":"⑤","name":"도구·자동화","sub":"만들어서 묶어 판다","color":"#ff9f7a","ax":180,"ay":760,
  "desc":"직접 만들어 쓰고, 수강생에게 기본판을 무료로 풀어 강의 후킹으로 쓰고, 외부·맞춤·구독은 유료로 받는 자리. 이것들이 모여 루크 툴박스 구독이 됩니다.",
  "nodes":[
   {"id":"margin","n":"마진메이커","full":"마진메이커","st":"build","exp":1,"d":"상품소싱 마진 자동계산 크롬 확장. 구매처 가격을 자동 계산하고, 모르는 사이트는 사용자가 캡처 영역을 지정해 OCR로 읽으며, 사이트별 할인 규칙을 서버에 쌓아 점점 정확해지게 하기로 결정.","from":"도구 개발 논의 (10월)"},
   {"id":"cut","n":"연출컷메이커","full":"연출컷메이커","st":"on","exp":1,"d":"AI 상품 연출컷 생성 크롬 확장. Gemini API를 BYOK(키는 사용자 것) 방식으로 써서 수강생에게 배포.","from":"도구 개발"},
   {"id":"typer","n":"블로그타이퍼","full":"블로그타이퍼","st":"build","exp":1,"d":"네이버 블로그에 붙여넣기가 아니라 사람이 키보드로 치듯 한 글자씩 입력하는 자동화. Claude Code + Playwright 방식으로 결정.","from":"블로그 자동화 논의 (8/30)"},
   {"id":"soam","n":"소명서 메이커","full":"정가품 소명서 메이커","st":"build","exp":1,"d":"네이버 정가품 소명서를 자동 생성하는 프로그램. Vercel claim·Drive OAuth 클라이언트 ID·실제 API 키 테스트 3건이 마무리로 남아 있음.","from":"수강생 대응 도구"},
   {"id":"videof","n":"영상공장","full":"영상공장 (동영상 자동 제작)","st":"build","exp":1,"d":"동영상을 자동으로 만드는 서비스. 9/28 회의에서 개발하려는 세 사이트 중 하나로 나왔고, API 키 5개 발급과 목소리 1~3분 녹음이 다음 단계.","from":"9/28 회의 (메이브님·디노)"},
   {"id":"voice","n":"내 목소리 엔진","full":"내 목소리 엔진","st":"idea","exp":1,"d":"유료 서비스를 쓰지 않고 직접 만들어, 본인 목소리만 특화 학습해 재현. AI API는 텍스트만 만들고 출력은 프로그램이 루크 목소리로. 텍스트를 넣으면 오디오 파일을 만드는 쪽도 함께 원함.","from":"음성 프로그램 구상 (9/8)"},
   {"id":"bsj","n":"배수진","full":"배수진 (목표달성 앱)","st":"idea","exp":1,"d":"돈을 걸고 목표를 달성하는 앱. 프로토타입 검토 단계. 셀러에 국한하지 않는 파이프라인을 원한다는 방향과 맞닿아 있음.","from":"앱 구상"},
   {"id":"autoreg","n":"자동등록","full":"자동 상품등록 프로그램 (등록 자판기)","st":"build","exp":1,"d":"4종 ‘자판기’ 프로그램 중 하나. 상품 선택 → 담기 → 등록 시작 3번 클릭으로 끝나고, 제미나이 연동으로 상품명·대표 사진·상세페이지를 3~5분 안에 자동 생성. 글자 추출(OCR)은 확장 프로그램 단에서 하고 AI는 추출된 텍스트로 상세페이지만 만드는 구조가 낫다고 봄. 네이버 API 정책·키·IP 차단으로 등록 실패가 나던 건의 원인 진단이 남아 있음.","from":"9/28 회의 · 도구 개발"},
  ]},
]

# (a, b, 관계 설명) — 확인되지 않은 연결은 설명에 '확인 필요'를 남김
UNI_EDGES = [
 ("luke","onecrew","1:1 세션을 루크가 직접 진행"),
 ("luke","plat","플레이어·강사 교육을 루크·메이브님이 맡는 구도"),
 ("luke","toolbox","프로그램 기획·개발이 루크 손에 있음"),
 ("luke","kititi","원장 자문을 루크가 직접"),
 ("luke","tpl","운영은 뿌요, 규칙 승인은 루크"),
 ("luke","yt","촬영·녹화가 루크 시간의 큰 몫"),
 ("luke","trade","9/29 회의에서 루크 개인 과제로 나온 신규 채널"),
 ("yt","live","영상 설명란·고정댓글에 라이브 신청 링크"),
 ("yt","onecrew","영상 보고 들어온 문의가 상담으로"),
 ("yt","toolbox","수강생에겐 도구 기본판 무료 → 외부·구독은 유료"),
 ("yt","mktg","유튜브 채널 운영을 업체에 '편집자' 권한으로 위임"),
 ("live","onecrew","라이브 참석자 → 상담 → 전환"),
 ("kakao","live","카톡 1천에 특강·라이브 공지"),
 ("cafe","kakao","같은 선판매·공지 라인"),
 ("cafe","plat","플랫폼의 락인 축이 카페 운영을 맡는 구조"),
 ("cafe","commu","네이버 카페 역할을 자체 사이트로 옮기는 구상"),
 ("vcell","plat","뷰셀 채널이 플랫폼 모객 자산"),
 ("vcell","consign","화장품 유입과 메이크업헬퍼가 같은 상품군"),
 ("blog","typer","사람처럼 치는 자동 입력 프로그램이 블로그를 돌림"),
 ("blog","yt","같은 녹음·강의 내용을 글로 다시 씀"),
 ("chowol","plat","강의 플랫폼 3자 구도에서 모객 축이 실제 계약으로 구체화된 자리"),
 ("chowol","invader","인베이더가 하던 기수 운영·모객 자리를 대신하는 그림"),
 ("chowol","yt","유튜브 라이브가 런칭 퍼널의 중심 — 시청자 400~600명 목표"),
 ("chowol","live","10/25 무료 라이브가 12월 런칭 퍼널의 리허설"),
 ("chowol","onecrew","강사를 공급하는 자리 — 루크가 가르치는 구조를 본인에게 적용"),
 ("gaeul","chowol","초월스토리 협업의 첫 실물 — 파일럿 강사 자리가 채워진 것"),
 ("gaeul","onecrew","원크루를 통과한 사람이 강사가 되는 첫 사례 — 사다리의 맨 윗칸"),
 ("gaeul","live","10/25 무료 라이브에 게스트 10분으로 카메라 테스트"),
 ("gaeul","yt","12월 라이브와 사전 영상 4편의 얼굴"),
 ("giant","tpl","물류가 정리돼야 오프라인·사이트 판매가 같이 열린다 — 4분기 선행 조건"),
 ("giant","resale","자체 사이트는 수강생 재고를 플랫폼 수수료 없이 돌릴 수 있는 출구"),
 ("invader","yt","이번 기수는 광고 없이 유튜브 채널로만 모객한다고 들음"),
 ("invader","onecrew","인베이더 기수 수강생이 원크루 전환 후보 풀이었다"),
 ("invader","vcell","뷰셀도 같은 라인 — 4기가 마지막이라고 들음"),
 ("invader","plat","여기가 닫히는 자리를 신규 강의 플랫폼이 대신한다"),
 ("invader","live","명단이 끊기면 자체 무료 라이브가 유일한 직접 입구"),
 ("mvstore","resale","수강생 재고를 메이븐 스토어가 위탁으로 받아 판다"),
 ("mvstore","tpl","물동량이 늘면 3PL 물류가 그만큼 받아야 한다"),
 ("mvstore","vcell","같은 사람의 채널과 스토어 — 콘텐츠가 곧 상품 홍보"),
 ("mvstore","luke","매출 상위 상품 링크를 받아 루크가 추가 판매 전략을 짠다"),
 ("beauty","kititi","지영 원장과 함께 구축 중 — 샵의 실제 가격·시술 데이터가 바탕"),
 ("onecrew","ilsip","일십백천 수료자가 원크루로 올라오는 사다리"),
 ("ilsip","kititi","키티티가 브랜딩 축 컨설팅의 실제 사례"),
 ("onecrew","consign","최은봉 대표(원크루) 건이 메이크업헬퍼 위탁"),
 ("onecrew","tpl","수강생 재고가 3PL 창고로 들어옴"),
 ("onecrew","callai","계약 문의 전화 녹음 100건+가 AI 학습 재료"),
 ("plat","onecrew","플랫폼 수강생이 원크루 후보 풀"),
 ("plat","sudan","메이브님과 같이 세우는 교육 축이라 한 몸으로 움직임"),
 ("sudan","corp","신규 법인 설립 vs 힐링디어스 상호 변경 사이에서 고민 중"),
 ("sudan","tpl","교육에 3PL을 묶은 형태의 회사 구상"),
 ("own","resale","자체 강의를 3PL 재고 판매와 연계하려는 구상"),
 ("own","sudan","자체 강의를 어느 회사 이름으로 할지와 맞물림 (확인 필요)"),
 ("toolkit","toolbox","툴킷에 들어가는 프로그램이 툴박스 구독 상품과 같은 것"),
 ("toolkit","autoreg","툴킷 구성의 자동등록 1년 이용권"),
 ("toolkit","soam","툴킷 구성의 소명서 1년 이용권"),
 ("toolkit","cut","툴킷 구성의 연출컷 1년 이용권"),
 ("dino","corp","디노 독립 수익이 서야 사무실 구조가 안정"),
 ("dino","videof","AI 영상 제작을 디노 라인에서 먼저 돌려봄"),
 ("tpl","resale","창고에 잠든 재고가 외부 판매 물건"),
 ("resale","store","창고형 매장이 재고를 오프라인으로 빼는 다음 칸 (확인 필요)"),
 ("tpl","store","같은 창고를 쓰는 구조인지 확인 필요"),
 ("resale","yt","팔린 실적이 다시 영상·강의 소재"),
 ("resale","cut","판매용 상품 사진을 연출컷으로 만드는 흐름 (확인 필요)"),
 ("grant","kititi","지영 원장이 2027 도전 대상"),
 ("grant","dino","디노 폐업·업력 시나리오를 같이 검토"),
 ("grant","vcell","메이브님도 지원사업 대상"),
 ("corp","tpl","통신판매업 신고·명의가 법인"),
 ("corp","seoul","본점 주소·이전 등기가 서울 이전과 맞물림"),
 ("seoul","store","서울 이전·건물 매입이 오프라인 매장 자리와 겹침 (확인 필요)"),
 ("seoul","plat","플랫폼이 안정되는 시점에 강의장 포함 이전"),
 ("margin","toolbox","툴박스 구독에 묶이는 도구"),
 ("cut","toolbox","툴박스 구독에 묶이는 도구"),
 ("typer","toolbox","툴박스 구독에 묶이는 도구"),
 ("soam","toolbox","툴박스 구독에 묶이는 도구"),
 ("videof","toolbox","툴박스 구독에 묶이는 도구"),
 ("autoreg","toolbox","툴박스 구독에 묶이는 도구"),
 ("bsj","toolbox","셀러에 국한하지 않는 파이프라인 — 툴박스가 가려는 방향"),
 ("margin","yt","수강생에게 기본판을 풀어 강의 후킹으로"),
 ("autoreg","tpl","등록·출고가 물류와 바로 이어짐"),
 ("callai","voice","AI가 루크 목소리로 답하도록 연결하려는 구상"),
 ("voice","videof","텍스트 → 루크 목소리 오디오를 영상에 얹음"),
 ("videof","yt","영상 제작 비용을 줄여 채널 운영을 가볍게"),
 ("beauty","toolbox","오프라인샵 팩과 같은 묶음인지 확인 필요"),
 ("commu","toolbox","자체 사이트·구독 사이트를 같은 스택으로 짓는 구상 (확인 필요)"),
]



# 가능성 연결 — 기록된 사실이 아니라 루크의 자산을 보고 클로드가 검토한 '이을 수 있는 선'
# (a, b, 왜 될 것 같은지, 그러려면 필요한 것, 거리 1=지금 당장 / 2=이번 분기 / 3=내년)
UNI_POSS = [
 ("resale","onecrew","수강생 재고를 회사가 팔아주는 것을 원크루·일십백천 혜택으로 묶으면, 고가 상품을 결제할 때 '최악이어도 재고는 회수된다'는 안전장치가 생긴다. 상담에서 가장 많이 걸리는 지점이 바로 손실 공포다.","판매 수수료와 회수 범위를 상품 설명에 명문화 · 재고 판매 첫 실적 몇 건",1),
 ("bsj","onecrew","컨설팅의 고질병은 숙제를 안 하는 것이다. 배수진(돈 걸고 목표달성)을 원크루·일십백천 과제 이행에 붙이면 실행률 장치가 된다. 내부에서 먼저 쓰고 그 데이터로 앱을 판다.","과제 단위 정의 · 돈을 거는 방식(환급·기부)의 법적 검토",1),
 ("autoreg","resale","재고 판매 상품을 여러 채널에 자동으로 올리면 사람 손 없이 회전한다. 지금 재고 판매가 느린 이유가 등록 노동이라면 바로 풀리는 병목.","자동등록의 네이버 API 차단 원인 해결 · 당근·번개장터 등록 경로 확인",1),
 ("typer","kititi","지영 원장 샵 블로그를 블로그타이퍼로 돌려 첫 외부 고객 사례를 만든다. '오프라인 샵 자동화'를 파는 데 필요한 것은 기능이 아니라 증거 한 건이다.","원장 동의 · 업종 글감 틀 · 네이버 제재 리스크 사전 설명",1),
 ("margin","beauty","가격비교는 '같은 물건이 어디서 얼마인지' 맞추는 같은 기술이다. 마진메이커 엔진을 미용 가격비교에 그대로 쓰면 새 사이트를 처음부터 짓지 않아도 된다.","시술명 표준화(상품명과 달리 표기가 제각각) · 수집 범위 결정",1),
 ("kititi","toolbox","툴박스 오프라인샵 팩(+9,900)의 첫 실사용자. 키티티에서 돌려보고 숫자가 나오면 미용 샵 대상 구독 영업의 레퍼런스가 된다.","샵용 기능 묶음 확정 · 한 달 사용 데이터",2),
 ("callai","toolbox","상담 AI를 '내 전화를 대신 받아주는 AI'로 돌리면 사업자 누구에게나 팔 수 있다. 내부용으로 만들어 외부로 파는 툴박스 공식 그대로.","녹음 100건의 사용 동의·비식별 처리 · 통화 연결 방식",2),
 ("soam","callai","소명·제재 대응 문의도 상담 전화의 큰 축이다. 같은 지식베이스로 묶으면 AI가 두 유형을 함께 답한다.","소명 사례 정리 · 답변 경계(법률 자문이 되지 않도록)",2),
 ("toolkit","dino","디노 12주 수료자가 300만 툴킷 1기의 첫 후보다. 교육 → 도구 묶음으로 올라가는 사다리가 이미 한 줄 있다.","12주 종료 시점과 툴킷 1기 모집 시점 맞추기 · 배분 비율",2),
 ("plat","videof","플랫폼의 챌린지 영상과 광고 소재를 영상공장으로 찍어내면 락인 축의 제작 부담이 크게 준다. 영상 제작비가 인베이더 실패의 한 축이었다.","영상공장 품질이 광고로 쓸 수준인지 1회차 검증",2),
 ("blog","onecrew","유튜브가 못 잡는 검색 수요를 블로그가 잡는다. 상담 사례 글은 '이거 괜찮은 겁니까' 유형이 검색으로 찾는 바로 그 글이다.","사례 공개 동의 · 상담 신청 동선 한 줄",2),
 ("commu","plat","플랫폼 락인 축이 쓸 커뮤니티를 자체 사이트로 지으면 네이버 카페 의존이 줄고 수강생 데이터를 회사가 갖는다. 소유권은 3자 협업에서 가장 중요한 조건이다.","본부장과의 역할·데이터 소유 합의가 먼저",2),
 ("mktg","vcell","채널 운영 대행 역량을 뷰셀에도 붙이면 메이브님 촬영 부담이 준다. 메이브님 시간이 플랫폼 쪽으로 넘어가야 하는 시점과 맞는다.","대행 범위에 뷰셀 포함 재협의 · 비용 분담",2),
 ("store","live","창고형 매장 오픈데이를 라이브 커머스 현장으로 쓰면 재고 소진과 콘텐츠를 한 번에 가져간다. 고정비 낮은 오픈데이 모델과 맞물린다.","매장 개설이 먼저 · 오픈데이 주기 결정",2),
 ("store","consign","메이크업헬퍼 위탁 물량을 오픈데이에서 직접 판다. 브랜드사 미입점 채널·폐쇄몰 조건과 성격이 맞는다 — 다만 계약서 문구 확인 필요.","위수탁계약의 판매 채널 조항 확인 · 매장 개설",3),
 ("voice","ilsip","내 목소리 엔진이 서면 400개 영상 강의의 개정과 재녹음을 다시 찍지 않고 한다. 강의 자산이 많을수록 이득이 커지는 구조.","엔진 품질이 강의로 쓸 수준인지 · 기존 강의 대본화",3),
 ("own","plat","플랫폼 1기는 3자 배분이지만 자체 강의는 전부 회사 몫이다. 플랫폼을 검증 무대로 쓰고 검증된 커리큘럼만 자체로 가져오는 순서가 자연스럽다.","플랫폼 협업 계약에 경업·IP 귀속 조항 정리가 먼저",3),
 ("own","tpl","자체 강의 수강생이 그대로 3PL 고객이 된다. 교육과 물류가 한 회사 안에서 도는 것이 셀러들의 수다 구상의 핵심이다.","법인 정리 · 3PL 수용 능력",3),
 ("grant","sudan","신규 법인은 업력이 짧아 창업 3년 이내 조건의 지원사업 문이 열린다. 힐링디어스(약 5년)로는 막히는 길이다.","대표자 요건·업종 코드 확인 필요 — 같은 업종 재창업으로 보면 제외될 수 있음",3),
 ("grant","store","오프라인 매장·물류 설비는 시설·공간 항목이 있는 지원사업과 맞는 구석이 많다.","사업 계획상 매장 개설 시점 · 해당 공고의 시설비 인정 범위 확인 필요",3),
 ("seoul","live","서울 강의장이 생기면 무료 라이브·특강을 오프라인 병행으로 돌릴 수 있다. 같은 사람을 만나도 전환이 다르다.","서울 이전 · 강의장 규모",3),
 ("trade","bsj","트레이드 채널과 '돈 걸고 목표달성'은 같은 관객(돈·성취)을 본다. 채널이 앱의 첫 사용자 풀이 된다.","트레이드 채널의 내용·플랫폼이 먼저 정해져야 함",3),
]

# 플라우드 최근 30일 녹음에서 센 언급 빈도 (recs=언급된 녹음 수, hits=총 언급 횟수)
BUZZ_WINDOW = "2026-09-06 ~ 2026-10-06"
BUZZ_SCANNED = 56
UNI_BUZZ = {
 "yt":(3,8), "cafe":(1,15), "kakao":(10,19), "vcell":(10,25), "live":(13,27), "mktg":(1,2),
 "blog":(2,6), "commu":(2,9), "trade":(1,1), "onecrew":(13,13), "ilsip":(1,1), "plat":(2,7),
 "toolkit":(0,0), "dino":(7,29), "kititi":(10,49), "sudan":(0,0), "own":(0,0), "callai":(3,6),
 "tpl":(7,23), "resale":(1,2), "store":(2,3), "toolbox":(0,0), "consign":(14,43), "beauty":(1,2),
 "grant":(3,9), "corp":(0,0), "seoul":(2,6), "margin":(0,0), "cut":(0,0), "typer":(0,0),
 "soam":(3,5), "videof":(1,2), "voice":(0,0), "bsj":(0,0), "autoreg":(15,46), "mvstore":(1,9),
 "chowol":(2,22), "invader":(2,14), "gaeul":(3,6), "giant":(1,1),
}
def buzz_score(i):
    r,h = UNI_BUZZ.get(i,(0,0)); return r + h/4.0
def buzz_heat(i):
    sc = buzz_score(i)
    return 3 if sc>=19 else (2 if sc>=10 else (1 if sc>0 else 0))


UNI_ANCHOR = {"ch":(96,180,-130), "kn":(268,250,95), "pr":(266,580,115), "base":(92,540,-75), "tool":(180,660,15)}

def universe_html():
    nodes = [{"id":"luke","n":"루크","full":"루크 (ONE CREW)","st":"on","big":2,"reg":"core","c":"#f0cd84",
              "ax":180,"ay":380,"az":0,"exp":0,"from":"","bz":0,"bh":0,"heat":0,
              "d":"다섯 구역이 전부 루크 한 사람을 지나갑니다. 그래서 구역을 늘리는 것보다 각 구역에 사람을 앉히는 것이 먼저입니다."}]
    for R in UNI_REGIONS:
        A = UNI_ANCHOR[R["id"]]
        for N in R["nodes"]:
            nodes.append({"id":N["id"],"n":N["n"],"full":N["full"],"st":N["st"],"big":N.get("big",0),
                          "reg":R["id"],"c":R["color"],"ax":A[0],"ay":A[1],"az":A[2],"d":N["d"],
                          "exp":N.get("exp",0),"from":N.get("from",""),
                          "bz":UNI_BUZZ.get(N["id"],(0,0))[0],"bh":UNI_BUZZ.get(N["id"],(0,0))[1],
                          "heat":buzz_heat(N["id"]),
                          "href":N.get("href",""),"hl":N.get("hl","")})
    data = {
      "nodes": nodes,
      "edges": [{"a":a,"b":b,"l":l} for a,b,l in UNI_EDGES],
      "poss": [{"a":a,"b":b,"l":l,"need":nd,"w":w} for a,b,l,nd,w in UNI_POSS],
      "buzz": {"window":BUZZ_WINDOW,"scanned":BUZZ_SCANNED},
      "regions": [{"id":R["id"],"no":R["no"],"name":R["name"],"sub":R["sub"],"color":R["color"],"desc":R["desc"]} for R in UNI_REGIONS],
    }
    body = """
<h1>사업 유니버스</h1>
<p class="note">사업·채널·상품·도구를 별로 두고, <b>실제로 이어져 있는 관계만 줄로 묶은 별자리</b>입니다. <b>전체 화면</b>으로 열면 지도만 꽉 차게 보고 그 안에서 바로 상세를 읽을 수 있습니다. <b>입체</b>로 바꾸면 손가락으로 돌려가며 볼 수 있고, <b>홈</b>을 누르면 처음 화면으로 돌아옵니다. <b>＋ 메모·새 별</b>로 지도 위에서 바로 새 사업이나 코멘트를 올릴 수 있습니다. 별을 누르면 그 별과 이어진 것만 남습니다. 사람들과의 대화에서 나온 확장 구상도 함께 올렸고, 어디서 나온 이야기인지 각 별에 적어 뒀습니다.</p>

<div class="uni-split" id="uniStage"><div class="uni-left">
<div class="sky"><svg viewBox="0 0 360 760" id="uniMap" role="img" aria-label="사업 유니버스 별자리" style="font-family:'Noto Sans KR',sans-serif;touch-action:none"></svg></div>
<div class="uniBar">
  <button type="button" id="uni2d" class="on">평면</button>
  <button type="button" id="uni3d">입체</button>
  <button type="button" id="uniHome">홈</button>
  <button type="button" id="uniFull">전체 화면</button>
  <button type="button" id="uniAdd">＋ 메모·새 별</button>
  <button type="button" id="uniDesk">데스크탑</button>
  <button type="button" id="uniPoss" class="on">가능성 선</button>
  <button type="button" id="uniBuzz">최근 많이 나온 별</button>
  <button type="button" id="uniExp">확장 구상만</button>
  <button type="button" id="uniReset">재배치</button>
</div>
<div class="legend" id="uniLeg">
  <span><i style="background:#f0cd84"></i>루크</span>
  <span><a href="#" data-reg="ch"><i style="background:#4fd1a5"></i>채널·브랜딩</a></span>
  <span><a href="#" data-reg="kn"><i style="background:#e3b04b"></i>지식·교육</a></span>
  <span><a href="#" data-reg="pr"><i style="background:#8fb0ff"></i>상품·유통</a></span>
  <span><a href="#" data-reg="base"><i style="background:#b79cff"></i>기반·자금</a></span>
  <span><a href="#" data-reg="tool"><i style="background:#ff9f7a"></i>도구·자동화</a></span>
</div>
<div class="legend uniLeg2" style="margin-top:-8px">
  <span><i style="background:var(--muted)"></i>채움 = 돌아감</span>
  <span><i style="border:2px solid var(--muted);background:transparent"></i>테두리 = 세우는 중</span>
  <span><i style="border:2px dotted var(--muted);background:transparent"></i>점선 = 구상</span>
  <span><svg width="26" height="8" style="vertical-align:-1px"><line x1="1" y1="4" x2="25" y2="4" stroke="#ffcf8a" stroke-width="2" stroke-dasharray="4 4"/></svg> 노란 점선 = 가능성</span>
  <span><i style="border:2px dotted #ff7b6e;background:transparent"></i>빨간 점선 = 종료 예정</span>
  <span>크고 고리가 번지는 별 = 최근 30일 대화에 많이 나온 것</span>
  <span id="uniTip"></span>
</div>

</div><div class="uni-right"><div class="card" id="uniPanel"></div></div></div>

<div class="uniForm" id="uniForm"><div class="box">
  <h3 id="ufTitle">내 메모 · 새 별 추가</h3>
  <p class="note" style="margin-top:4px">이 기기에 바로 저장돼 지도에 흰 별로 올라갑니다. <b>깃허브에 올리기</b>를 누르면 이슈로 접수되고, 다음 날 아침 자동 갱신 때 정식으로 지도에 반영됩니다.</p>
  <label for="ufKind">무엇을 추가할까요</label>
  <select id="ufKind"><option value="node">새 별 — 새 사업·채널·상품·도구</option><option value="comment">코멘트 — 기존 별에 메모</option></select>
  <div id="ufNodeBox">
    <label for="ufName">이름</label><input id="ufName" type="text" placeholder="예: 셀러 전용 중고 장비 마켓" maxlength="30">
  </div>
  <label for="ufTarget">어느 별에 이을까요 <span style="opacity:.7">(코멘트는 대상 별)</span></label>
  <select id="ufTarget"></select>
  <div id="ufLinkBox">
    <label for="ufLink">그 별과 어떤 관계인지 <span style="opacity:.7">(선택)</span></label>
    <input id="ufLink" type="text" placeholder="예: 창고 재고를 이쪽으로 돌린다" maxlength="60">
  </div>
  <label for="ufText">내용</label><textarea id="ufText" placeholder="무엇인지, 왜 하려는지, 지금 걸리는 것"></textarea>
  <div class="row">
    <button type="button" id="ufSave" class="on">지도에 올리기</button>
    <button type="button" id="ufGh">깃허브에 올리기</button>
  </div>
  <div class="row">
    <button type="button" id="ufCopy">클로드에 붙여넣을 글 복사</button>
    <button type="button" id="ufClose">닫기</button>
  </div>
  <div id="ufList"></div>
</div></div>

<div class="card red" style="margin-bottom:16px">
  <div class="t">10/6 — 인베이더가 강의를 접을 것 같다는 이야기</div>
  <div class="m">지도에 <b>인베이더</b> 별을 빨간 점선(종료 예정)으로 올렸습니다. 거기서 끊기는 줄이 어디로 가야 하는지와 마지막 기수에 챙길 것은 <a href="../invader/">인베이더 종료 대비</a>에 정리했습니다. 전해 들은 이야기로 아직 미확정입니다.</div>
</div>

<h2>최근 대화에 많이 나온 것 <small>플라우드 __BZWIN__</small></h2>
<p class="note">녹음 <b>__BZN__건</b>(2분 이상 업무 녹음, 사적인 것 제외)의 요약 노트에서 각 사업이 몇 번 나왔는지 센 결과입니다. 많이 나온 별일수록 지도에서 <b>크고, 고리가 번지고, 거기서 나가는 줄이 밝고 빠르게</b> 흐릅니다.</p>
<div id="uniBuzzList">__BUZZ__</div>

<h2>가능성 선 <small>지금 자산으로 이을 수 있는 것</small></h2>
<p class="note">기록에 있는 사실이 아니라, 지금 가진 것들을 보고 <b>이을 수 있어 보이는 연결</b>을 정리한 것입니다. 지도에서 노란 점선으로 그어 뒀고, 별을 누르면 그 별에서 뻗는 가능성만 모아 보입니다. 아니라고 보시면 지웁니다.</p>
__POSS__

<h2>이 별자리 보는 법</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">줄이 곧 사업</div><div class="m">별 세 개가 따로 있으면 부업 셋입니다. 줄로 엮여야 하나가 흔들려도 나머지가 받칩니다 — <a href="../philosophy/">삼각 파이프라인</a>의 핵심</div></li>
    <li><div class="t">입체로 보면 구역이 앞뒤로 갈라집니다</div><div class="m">같은 색끼리 깊이가 비슷하게 놓여 있어, 돌려 보면 어느 구역이 어디에 몰려 있는지 덩어리로 보입니다</div></li>
    <li><div class="t">가운데 루크에 줄이 몰리는 것이 지금의 병목</div><div class="m">루크에 직접 붙은 줄을 사람에게 넘기는 것이 구역을 늘리는 것보다 먼저입니다</div></li>
    <li><div class="t">⑤ 도구·자동화는 혼자 돈이 되지 않습니다</div><div class="m">만들어서 루크 툴박스 구독으로 묶이거나, 수강생에게 기본판을 풀어 강의 후킹이 될 때 돈이 됩니다. 줄이 툴박스로 모이는 이유</div></li>
    <li><div class="t">'확인 필요'가 붙은 줄</div><div class="m">아직 기록으로 확인되지 않은 연결입니다. 맞는지 알려주시면 확정하거나 지웁니다</div></li>
  </ul>
</div>

<h2>지도 위에서 바로 올리기</h2>
<div class="card accent">
  <ul class="list">
    <li><div class="t">＋ 메모·새 별</div><div class="m">지도 위 버튼(전체 화면 안에서도 됩니다). 새 사업·채널·상품을 올리거나, 고른 별에 코멘트를 답니다</div></li>
    <li><div class="t">지도에 올리기 — 바로 보입니다</div><div class="m">흰 점선 별로 지도에 즉시 올라갑니다. 다만 이 기기(브라우저)에만 저장돼 다른 기기에서는 안 보입니다</div></li>
    <li><div class="t">깃허브에 올리기 — 정식으로 들어갑니다</div><div class="m">깃허브 이슈로 접수됩니다. 매일 아침 6시 40분 자동 갱신이 이슈를 읽어 지도에 정식으로 넣고, 반영했다고 댓글을 달고 이슈를 닫습니다. 그때부터 모든 기기에서 보입니다</div></li>
    <li><div class="t">클로드에 붙여넣을 글 복사</div><div class="m">아침까지 기다리기 싫을 때. 복사해서 클로드 대화에 붙여넣으면 바로 올려 드립니다</div></li>
  </ul>
</div>

<h2>아직 비어 있는 자리</h2>
<div class="card gold">
  <p style="margin:0 0 8px">말씀해주시면 별이든 줄이든 그대로 넣습니다.</p>
  <ul class="list">
    <li><div class="t">오프라인 창고형 매장</div><div class="m">위치·평수·취급 품목·운영 인력·여는 시점. 3PL 재고를 쓰는 건지, 별도 매입인지</div></li>
    <li><div class="t">개인 트레이드 채널</div><div class="m">무엇을 다루는 채널인지, 어느 플랫폼인지</div></li>
    <li><div class="t">10월 말 무료 라이브</div><div class="m">10/25(일) 19:00이 확정인지, 신청 링크</div></li>
    <li><div class="t">빠진 확장 구상</div><div class="m">사람들과 얘기했지만 여기 없는 것. 이름과 한 줄, 누구와 한 이야기인지</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: <a href="../roadmap/">돈 버는 로드맵</a> · <a href="../philosophy/">삼각 파이프라인</a> · <a href="../platform/">강의 플랫폼 전략</a> · <a href="../grants/">정부지원사업</a> · 8/25~10/4 노션 액션보드·플라우드 녹음·클로드 대화 기록. 확장 구상 별에는 어느 대화에서 나온 것인지 적어 두었습니다. 금액은 모두 계획값이며 실적이 아닙니다.</div>

<script>
(function(){
var D = __DATA__;
var VIEWS={
 m:{W:360,H:760,CX:180,CY:380,F:760,L:74,K:2200,PL:120,Z3:0.82,G:0.006,FC:3,FS:9,NR:1,SEP:20,J:110,
    A:{core:[180,380,0],ch:[96,180,-130],kn:[268,250,95],pr:[266,580,115],base:[92,540,-75],tool:[180,660,15],my:[180,250,40]}},
 d:{W:1180,H:710,CX:590,CY:350,F:1500,L:150,K:11500,PL:230,Z3:0.92,G:0.013,FC:6.5,FS:13.5,NR:1.5,SEP:40,J:190,
    A:{core:[590,350,0],ch:[215,170,-130],kn:[960,180,95],pr:[965,505,115],base:[205,515,-75],tool:[590,560,15],my:[590,200,40]}}
};
var VIEW='m', CFG=VIEWS.m;
var W=CFG.W, H=CFG.H, CX=CFG.CX, CY=CFG.CY, F=CFG.F;
var svg=document.getElementById('uniMap'), panel=document.getElementById('uniPanel'), tip=document.getElementById('uniTip');
var NS='http://www.w3.org/2000/svg';
var N={}, nodes=D.nodes, edges=D.edges, regs={};
D.regions.forEach(function(r){regs[r.id]=r;});
regs.core={id:'core',no:'',name:'루크',sub:'',color:'#f0cd84',desc:'다섯 구역이 전부 여기를 지나갑니다.'};
regs.my={id:'my',no:'＋',name:'내 메모',sub:'이 기기에 저장됨',color:'#ffffff',desc:'이 화면에서 직접 올린 것입니다. 지금은 이 기기에만 저장돼 있고, 깃허브에 올리면 다음 갱신 때 정식으로 들어갑니다.'};
var NOTEK='luke1b-uninotes';
function loadNotes(){ try{ return JSON.parse(localStorage.getItem(NOTEK)||'[]'); }catch(e){ return []; } }
function saveNotes(a){ try{ localStorage.setItem(NOTEK, JSON.stringify(a)); }catch(e){} }
var notes=loadNotes();
var byId={}; nodes.forEach(function(n){ byId[n.id]=n; });
notes.forEach(function(nt){
  if(nt.kind==='node'){
    if(byId[nt.id]) return;
    var nn={id:nt.id,n:nt.name,full:nt.name,st:'idea',big:0,reg:'my',c:'#ffffff',
            ax:0,ay:0,az:0,exp:0,from:'내가 '+(nt.ts||'').slice(0,10)+'에 올림',mine:1,
            d:nt.text||'(설명 없음)'};
    nodes.push(nn); byId[nn.id]=nn;
    if(nt.target && byId[nt.target]) edges.push({a:nt.id,b:nt.target,l:nt.link||'내가 이어둔 선',mine:1});
  }
});
notes.forEach(function(nt){
  if(nt.kind==='comment' && byId[nt.target]){
    var t=byId[nt.target]; if(!t.mem) t.mem=[]; t.mem.push(nt);
  }
});
var seed=20261005;
function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff;}
var MODE='2d', rotY=0, rotX=0, spin=0, zoom=1;
var HOME={rotY:0.55, rotX:-0.22};

var HEATR={0:1,1:1.10,2:1.34,3:1.62};
var OFFC='#ff7b6e';
function sizeNodes(){
  nodes.forEach(function(n){
    var hm=HEATR[n.heat||0];
    n.r=(n.big===2?15:(n.big===1?7.5:5.8))*CFG.NR*hm;
    n.fs=(n.big?CFG.FS+1:CFG.FS)*(n.heat>=3?1.22:(n.heat>=2?1.1:1));
    n.hw=Math.min(n.n.length*(n.fs*0.52)+4, CFG.W*0.17);
    if(n.t1){ n.t1.setAttribute('font-size',n.fs); n.t1.textContent=n.n; }
  });
}
nodes.forEach(function(n){ N[n.id]=n; n.deg=0; n.adj=[]; });
sizeNodes();
edges.forEach(function(e){
  var a=N[e.a], b=N[e.b]; if(!a||!b) return;
  a.deg++; b.deg++; a.adj.push({id:e.b,l:e.l}); b.adj.push({id:e.a,l:e.l}); e.t=rnd();
});
var poss=D.poss;
nodes.forEach(function(n){ n.pot=[]; });
poss.forEach(function(e){
  var a=N[e.a], b=N[e.b]; if(!a||!b) return;
  a.pot.push({id:e.b,l:e.l,need:e.need,w:e.w}); b.pot.push({id:e.a,l:e.l,need:e.need,w:e.w});
});
function place(){ nodes.forEach(function(n){ n.x=n.ax+(rnd()-0.5)*CFG.J; n.y=n.ay+(rnd()-0.5)*CFG.J; n.z=n.az+(rnd()-0.5)*90; n.vx=0;n.vy=0;n.vz=0; }); }
place();
function tick(k){
  var flat = (MODE==='2d');
  for(var i=0;i<nodes.length;i++){ for(var j=i+1;j<nodes.length;j++){
    var a=nodes[i], b=nodes[j], dx=b.x-a.x, dy=b.y-a.y, dz=b.z-a.z;
    var d2=dx*dx+dy*dy+dz*dz; if(d2<1) d2=1; var d=Math.sqrt(d2);
    var f=CFG.K/d2; if(f>CFG.FC) f=CFG.FC;
    var ux=dx/d, uy=dy/d, uz=dz/d;
    a.vx-=ux*f; a.vy-=uy*f; a.vz-=uz*f; b.vx+=ux*f; b.vy+=uy*f; b.vz+=uz*f;
    var min=a.r+b.r+CFG.SEP;
    if(d<min){ var p=(min-d)*0.5; a.vx-=ux*p; a.vy-=uy*p; a.vz-=uz*p; b.vx+=ux*p; b.vy+=uy*p; b.vz+=uz*p; }
    if(Math.abs(dy)<CFG.FS*1.9 && Math.abs(dz)<70){
      var needx=a.hw+b.hw+8, adx=Math.abs(dx);
      if(adx<needx){ var sg=(dx<0?-1:1), pw=(needx-adx)*0.22;
        a.vx-=sg*pw; b.vx+=sg*pw; a.vy-=(dy<0?-1:1)*0.5; b.vy+=(dy<0?-1:1)*0.5; }
    }
  }}
  edges.forEach(function(e){
    var a=N[e.a], b=N[e.b]; if(!a||!b) return;
    var dx=b.x-a.x, dy=b.y-a.y, dz=b.z-a.z, d=Math.sqrt(dx*dx+dy*dy+dz*dz)||1;
    var f=(d-CFG.L)*0.012, ux=dx/d, uy=dy/d, uz=dz/d;
    a.vx+=ux*f; a.vy+=uy*f; a.vz+=uz*f; b.vx-=ux*f; b.vy-=uy*f; b.vz-=uz*f;
  });
  poss.forEach(function(e){
    var a=N[e.a], b=N[e.b]; if(!a||!b) return;
    var dx=b.x-a.x, dy=b.y-a.y, dz=b.z-a.z, d=Math.sqrt(dx*dx+dy*dy+dz*dz)||1;
    var f=(d-CFG.PL)*0.004, ux=dx/d, uy=dy/d, uz=dz/d;
    a.vx+=ux*f; a.vy+=uy*f; a.vz+=uz*f; b.vx-=ux*f; b.vy-=uy*f; b.vz-=uz*f;
  });
  nodes.forEach(function(n){
    n.vx += (n.ax-n.x)*CFG.G; n.vy += (n.ay-n.y)*CFG.G;
    n.vz += ((flat?0:n.az)-n.z)*(flat?0.14:0.008);
    if(n.id==='luke'){ n.vx += (CX-n.x)*0.05; n.vy += (CY-n.y)*0.05; n.vz += (0-n.z)*0.05; }
    n.vx*=0.80; n.vy*=0.80; n.vz*=0.80;
    n.x+=n.vx*k; n.y+=n.vy*k; n.z+=n.vz*k;
    var mx=Math.max(n.r+10, n.hw+6);
    var xmax=(CFG.XMAX||W);
    if(n.x<mx) n.x=mx; if(n.x>xmax-mx) n.x=xmax-mx;
    var yt=Math.max(60,H*0.155), yb=H-Math.max(46,H*0.125);
    if(n.y<yt) n.y=yt; if(n.y>yb) n.y=yb;
    if(n.z<-150) n.z=-150; if(n.z>150) n.z=150;
  });
}
function settle(){ for(var s=0;s<620;s++) tick(1); }
settle();

function el(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);return e;}
var defs=el('defs',{});
var rg=el('radialGradient',{id:'uGlow'});
rg.appendChild(el('stop',{offset:'0%','stop-color':'#ffffff','stop-opacity':'.55'}));
rg.appendChild(el('stop',{offset:'100%','stop-color':'#ffffff','stop-opacity':'0'}));
defs.appendChild(rg); svg.appendChild(defs);
var gStar=el('g',{}), gPoss=el('g',{}), gEdge=el('g',{}), gPulse=el('g',{}), gNode=el('g',{});
svg.appendChild(gStar); svg.appendChild(gPoss); svg.appendChild(gEdge); svg.appendChild(gPulse); svg.appendChild(gNode);

var STARS=[];
for(var i=0;i<110;i++){
  var th=rnd()*Math.PI*2, ph=Math.acos(2*rnd()-1), R=640+rnd()*260;
  STARS.push({x:R*Math.sin(ph)*Math.cos(th), y:R*Math.sin(ph)*Math.sin(th)*0.7, z:R*Math.cos(ph),
              s:0.5+rnd()*1.1, ph:rnd()*6.28, el:el('circle',{fill:'#cfe9ff',r:'1'})});
}
STARS.forEach(function(s){ gStar.appendChild(s.el); });

edges.forEach(function(e){
  var A=N[e.a], B=N[e.b];
  e.hot = Math.max((A&&A.heat)||0,(B&&B.heat)||0);
  var col = e.mine ? '#ffffff' : (e.hot>=3?'#bfe9ff':(e.hot>=2?'#9ec6dd':'#7fa8bd'));
  var op  = e.mine ? .6 : (e.hot>=3?.78:(e.hot>=2?.56:.32));
  e.base = {c:col,o:op,w:1+0.35*e.hot};
  e.el = el('line',{'stroke':col,'stroke-width':e.base.w,'stroke-linecap':'round','opacity':op});
  gEdge.appendChild(e.el);
  e.p = el('circle',{'r':1.8+0.45*e.hot,'fill':(e.hot>=2?'#ffffff':'#dff6ef'),'opacity':(e.hot>=2?'.95':'.8')});
  gPulse.appendChild(e.p);
  if(e.hot>=3){ e.p2 = el('circle',{'r':1.8+0.45*e.hot,'fill':'#ffffff','opacity':'.75'}); gPulse.appendChild(e.p2); e.t2=rnd(); }
});
var POPA={1:.62,2:.42,3:.28};
poss.forEach(function(e){
  e.el = el('line',{'stroke':'#ffcf8a','stroke-width':'1.2','stroke-linecap':'round',
                    'stroke-dasharray':(e.w===1?'5 4':(e.w===2?'4 6':'2 7')),
                    'opacity':POPA[e.w],'class':'lu-pflow'});
  gPoss.appendChild(e.el);
});
nodes.forEach(function(n){
  var g=el('g',{'class':'uni-nd','style':'cursor:pointer'});
  var at={'r':n.r,'fill':n.c};
  if(n.st==='build'){at={'r':n.r,'fill':'#0c1a20','stroke':n.c,'stroke-width':'2'};}
  if(n.st==='idea'){at={'r':n.r,'fill':'#0c1a20','stroke':n.c,'stroke-width':'1.6','stroke-dasharray':'2 2.4'};}
  if(n.st==='off'){at={'r':n.r,'fill':'#2a1113','stroke':'#ff7b6e','stroke-width':'2','stroke-dasharray':'1.5 3'};}
  if(n.id==='luke'){at={'r':n.r,'fill':'#ffe9b8','stroke':'#e3b04b','stroke-width':'2'};}
  if(n.mine){at={'r':n.r,'fill':'#0c1a20','stroke':'#ffffff','stroke-width':'2','stroke-dasharray':'3 3'};}
  n.ring = el('circle',{'r':n.r,'fill':'none','stroke':(n.st==='off'?OFFC:n.c),'stroke-width':'1.6','opacity':'0'});
  n.ph = rnd();
  n.glow = el('circle',{'r':n.r*3.2,'fill':'url(#uGlow)','opacity':'.5'});
  n.halo = el('circle',{'r':n.r+7,'fill':n.c,'opacity':'0'});
  n.c1 = el('circle',at);
  n.t1 = el('text',{'text-anchor':'middle','font-size':n.fs,'fill':'#e8eef2','class':'lu-lab'});
  n.t1.textContent=n.n;
  if(n.heat>=3) n.t1.setAttribute('font-weight','700');
  n.hit = el('circle',{'r':Math.max(n.r+10,14),'fill':'transparent'});
  g.appendChild(n.glow); g.appendChild(n.ring); g.appendChild(n.halo); g.appendChild(n.c1); g.appendChild(n.t1); g.appendChild(n.hit);
  gNode.appendChild(g); n.g=g;
});

function proj(x,y,z){
  var dx=x-CX, dy=y-CY, dz=z;
  var cy=Math.cos(rotY), sy=Math.sin(rotY);
  var X=dx*cy+dz*sy, Z=-dx*sy+dz*cy;
  var cx2=Math.cos(rotX), sx2=Math.sin(rotX);
  var Y=dy*cx2-Z*sx2; var Z2=dy*sx2+Z*cx2;
  var d=F/(F+Z2), s=d*zoom;
  return {x:CX+X*s, y:CY+Y*s, s:s, d:d, z:Z2};
}
function projStar(st){
  var cy=Math.cos(rotY), sy=Math.sin(rotY);
  var X=st.x*cy+st.z*sy, Z=-st.x*sy+st.z*cy;
  var cx2=Math.cos(rotX), sx2=Math.sin(rotX);
  var Y=st.y*cx2-Z*sx2; var Z2=st.y*sx2+Z*cx2;
  if(Z2<-F+40) return null;
  var s=F/(F+Z2);
  return {x:CX+X*s*(W/720), y:CY+Y*s*(W/720), s:s};
}
var tms=0;
function draw(){
  tms+=0.016;
  var three = (MODE==='3d');
  STARS.forEach(function(st){
    if(!three){ st.el.setAttribute('opacity','0'); return; }
    var p=projStar(st);
    if(!p){ st.el.setAttribute('opacity','0'); return; }
    st.el.setAttribute('cx',p.x); st.el.setAttribute('cy',p.y);
    st.el.setAttribute('r',Math.max(0.3, st.s*p.s*0.9));
    st.el.setAttribute('opacity', (0.25+0.45*Math.abs(Math.sin(tms*0.7+st.ph)))*Math.min(1,p.s));
  });
  nodes.forEach(function(n){ var p=proj(n.x,n.y,n.z); n.px=p.x; n.py=p.y; n.ps=p.s; n.pd=p.d; n.pz=p.z; });
  poss.forEach(function(e){
    var a=N[e.a], b=N[e.b];
    e.el.setAttribute('x1',a.px); e.el.setAttribute('y1',a.py);
    e.el.setAttribute('x2',b.px); e.el.setAttribute('y2',b.py);
  });
  edges.forEach(function(e){
    var a=N[e.a], b=N[e.b];
    e.el.setAttribute('x1',a.px); e.el.setAttribute('y1',a.py);
    e.el.setAttribute('x2',b.px); e.el.setAttribute('y2',b.py);
    var sp = 0.003*(1+0.85*(e.hot||0));
    e.t += sp; if(e.t>1) e.t-=1;
    e.p.setAttribute('cx', a.px+(b.px-a.px)*e.t); e.p.setAttribute('cy', a.py+(b.py-a.py)*e.t);
    if(e.p2){ e.t2 += sp; if(e.t2>1) e.t2-=1;
      e.p2.setAttribute('cx', a.px+(b.px-a.px)*e.t2); e.p2.setAttribute('cy', a.py+(b.py-a.py)*e.t2); }
    if(three){ var dd=(a.pd+b.pd)/2; e.el.setAttribute('stroke-width', (0.5+1.3*(dd-0.82))*(e.hi?1.9:1)); }
    else e.el.setAttribute('stroke-width', e.hi?1.8:1);
  });
  nodes.forEach(function(n){
    var s=three?n.ps:1;
    n.glow.setAttribute('cx',n.px); n.glow.setAttribute('cy',n.py); n.glow.setAttribute('r',n.r*3.2*s);
    n.glow.setAttribute('opacity', (three?(0.12+0.55*Math.max(0,Math.min(1,(n.pd-0.84)*2.6))):0.42)*(1+0.30*(n.heat||0)));
    n.halo.setAttribute('cx',n.px); n.halo.setAttribute('cy',n.py); n.halo.setAttribute('r',(n.r+7)*s);
    if(n.heat>=2){
      var ph=((tms*0.40+n.ph)%1);
      n.ring.setAttribute('cx',n.px); n.ring.setAttribute('cy',n.py);
      n.ring.setAttribute('r', n.r*s*(1+1.15*ph));
      n.ring.setAttribute('opacity', (n.heat>=3?0.55:0.34)*(1-ph));
    }
    n.c1.setAttribute('cx',n.px); n.c1.setAttribute('cy',n.py); n.c1.setAttribute('r',n.r*s);
    n.hit.setAttribute('cx',n.px); n.hit.setAttribute('cy',n.py); n.hit.setAttribute('r',Math.max(n.r*s+10,14));
    n.t1.setAttribute('x',n.px); n.t1.setAttribute('y',n.py+n.r*s+10*s);
    n.t1.setAttribute('font-size', n.fs*Math.max(0.7,s));
    n.t1.setAttribute('opacity', three? Math.max(0, Math.min(1,(n.pd-0.92)*6)) : 1);
  });
  if(three){
    var order=nodes.slice().sort(function(a,b){return b.pz-a.pz;});
    for(var i=0;i<order.length;i++) gNode.appendChild(order[i].g);
  }
}
var reduce=false;
try{ reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){}
function loop(){
  if(MODE==='3d' && !dragRot && spin) rotY += 0.0014;
  tick(MODE==='2d'?0.35:0.3); draw();
  if(!reduce) requestAnimationFrame(loop);
}
draw(); if(!reduce) requestAnimationFrame(loop);

var ST={on:['돌아감','p0'],build:['세우는 중','p1'],idea:['구상','p2'],off:['종료 예정','p0']};
var WD={1:'지금 당장',2:'이번 분기',3:'내년'};
var sel=null, filt=null, showP=true;
function apply(){
  var keep=null;
  if(sel){ keep={}; keep[sel]=1; N[sel].adj.forEach(function(a){keep[a.id]=1;}); }
  else if(filt==='exp'){ keep={}; nodes.forEach(function(n){ if(n.exp) keep[n.id]=1; }); keep['luke']=1; }
  else if(filt==='buzz'){ keep={}; nodes.forEach(function(n){ if(n.heat>=2) keep[n.id]=1; }); keep['luke']=1; }
  else if(filt){ keep={}; nodes.forEach(function(n){ if(n.reg===filt) keep[n.id]=1; }); keep['luke']=1; }
  nodes.forEach(function(n){
    var on = !keep || keep[n.id];
    n.g.style.opacity = on? '1':'.1';
    n.halo.setAttribute('opacity', (sel===n.id)?'.35':'0');
  });
  poss.forEach(function(e){
    var on = showP && (sel ? (e.a===sel||e.b===sel) : (!keep || (keep[e.a] && keep[e.b])));
    e.el.setAttribute('opacity', on? (sel?0.95:POPA[e.w]) : 0);
    e.el.setAttribute('stroke-width', (sel && on)? '2':'1.2');
  });
  edges.forEach(function(e){
    var on = sel ? (e.a===sel||e.b===sel) : (!keep || (keep[e.a] && keep[e.b]));
    e.hi = !!(sel && on);
    e.el.setAttribute('opacity', on? (sel?'.9':'.38') : '.04');
    e.el.setAttribute('stroke', (sel && on)? N[sel].c : '#7fa8bd');
    e.p.setAttribute('opacity', on? (e.hot>=2?'.95':'.8'):'0');
    if(e.p2) e.p2.setAttribute('opacity', on? '.75':'0');
    if(!on && e.hot>=2){ e.el.setAttribute('stroke','#7fa8bd'); }
  });
  nodes.forEach(function(n){ if(n.heat<2) return; var kp=!keep||keep[n.id]; if(!kp) n.ring.setAttribute('opacity','0'); });
}
function lk(n){ return '<a href="#" data-go="'+n.id+'">'+n.n+'</a>'; }
function home(){
  sel=null; filt=null; apply();
  var ex=nodes.filter(function(n){return n.exp;});
  var h='<h3>별자리 전체</h3><p class="note" style="margin-top:0">별 '+nodes.length+'개 · 지금 이어진 줄 '+edges.length+'개 · 이을 수 있는 노란 점선 '+poss.length+'개. 대화에서 나온 확장 구상은 '+ex.length+'개입니다 — <a href="#" data-f="exp">확장 구상만 보기</a></p><ul class="list">';
  D.regions.forEach(function(r){
    var ns=nodes.filter(function(n){return n.reg===r.id;});
    h+='<li><div class="t"><a href="#" data-f="'+r.id+'" style="color:'+r.color+'">'+r.no+' '+r.name+'</a></div><div class="m">'+ns.map(lk).join(' · ')+'</div></li>';
  });
  var mine=nodes.filter(function(n){return n.mine;});
  if(mine.length) h+='<li><div class="t" style="color:#fff">＋ 내 메모</div><div class="m">'+mine.map(lk).join(' · ')+'</div></li>';
  var top=nodes.slice().sort(function(a,b){return b.deg-a.deg;}).slice(0,4);
  h+='</ul><div class="note">줄이 가장 많이 몰린 곳: '+top.map(function(n){return lk(n)+' '+n.deg;}).join(' · ')+'</div>';
  var bz=buzzRank().slice(0,5);
  h+='<div class="note">최근 30일 대화에 가장 많이 나온 별: '+bz.map(function(n){return lk(n)+' '+n.bz+'건';}).join(' · ')+' — <a href="#" data-f="buzz">그것만 보기</a></div>';
  panel.innerHTML=h;
}
function buzzRank(){ return nodes.filter(function(n){return n.bz>0||n.bh>0;})
  .sort(function(a,b){ return (b.bz+b.bh/4)-(a.bz+a.bh/4); }); }
function showBuzz(){
  sel=null; filt='buzz'; apply();
  var r=buzzRank();
  var h='<h3>최근 많이 나온 별 <small style="color:var(--muted);font-weight:400">'+D.buzz.window+'</small></h3>'+
    '<p class="note" style="margin-top:0">플라우드 녹음 '+D.buzz.scanned+'건(2분 이상 업무 녹음, 사적인 것 제외)의 요약 노트에서 각 사업이 몇 번 나왔는지 센 것입니다. 많이 나온 별일수록 크고, 고리가 번지고, 거기서 나가는 줄이 밝고 빠릅니다.</p><ul class="list">';
  r.slice(0,14).forEach(function(n,i){
    h+='<li><span class="tag '+(n.heat>=3?'p0':(n.heat>=2?'p1':'p2'))+'">'+(i+1)+'위</span>'+
       '<div class="t"><a href="#" data-go="'+n.id+'" style="color:'+n.c+'">'+n.full+'</a></div>'+
       '<div class="m">녹음 '+n.bz+'건 · '+n.bh+'번 언급</div></li>';
  });
  h+='</ul><p class="note"><a href="#" data-go="home">← 별자리 전체</a></p>';
  panel.innerHTML=h;
}
function showExp(){
  sel=null; filt='exp'; apply();
  var h='<h3>확장 구상 <small style="color:var(--muted);font-weight:400">대화에서 나온 것</small></h3>'+
        '<p class="note" style="margin-top:0">사람들과 얘기하면서 나왔지만 아직 돈이 되는 줄로 서지 않은 것들입니다. 어디서 나온 이야기인지 함께 적었습니다.</p><ul class="list">';
  D.regions.forEach(function(r){
    var ns=nodes.filter(function(n){return n.reg===r.id && n.exp;});
    if(!ns.length) return;
    h+='<li><div class="t" style="color:'+r.color+'">'+r.no+' '+r.name+'</div><div class="m">';
    h+=ns.map(function(n){return '<a href="#" data-go="'+n.id+'">'+n.full+'</a> <span style="opacity:.7">— '+ST[n.st][0]+(n['from']?' · '+n['from']:'')+'</span>';}).join('<br>');
    h+='</div></li>';
  });
  h+='</ul><p class="note"><a href="#" data-go="home">← 별자리 전체</a></p>';
  panel.innerHTML=h;
}
function showReg(rid){
  var r=regs[rid]; if(!r) return home();
  sel=null; filt=rid; apply();
  var ns=nodes.filter(function(n){return n.reg===rid;});
  var h='<h3 style="color:'+r.color+'">'+r.no+' '+r.name+' <small style="color:var(--muted);font-weight:400">'+r.sub+'</small></h3>';
  h+='<p class="note" style="margin-top:0">'+r.desc+'</p><ul class="list">';
  ns.forEach(function(n){
    h+='<li><span class="tag '+ST[n.st][1]+'">'+ST[n.st][0]+'</span><div class="t"><a href="#" data-go="'+n.id+'">'+n.full+'</a></div><div class="m">'+n.d+'</div></li>';
  });
  h+='</ul><p class="note"><a href="#" data-go="home">← 별자리 전체</a></p>';
  panel.innerHTML=h;
}
function show(id){
  var n=N[id]; if(!n) return home();
  sel=id; filt=null; apply();
  var r=regs[n.reg];
  var h='<span class="tag '+ST[n.st][1]+'">'+ST[n.st][0]+'</span><span class="tag" style="color:'+r.color+';border-color:'+r.color+'">'+(r.no?r.no+' ':'')+r.name+'</span>';
  h+='<h3 style="margin-top:8px">'+n.full+'</h3><p style="margin-bottom:8px">'+n.d+'</p>';
  if(n.bz||n.bh) h+='<div class="note" style="margin-bottom:8px">최근 30일 대화 언급: 녹음 <b>'+n.bz+'건</b> · <b>'+n.bh+'번</b>'+(n.heat>=3?' — 가장 많이 나온 축':(n.heat>=2?' — 자주 나오는 축':''))+'</div>';
  if(n['from']) h+='<div class="note" style="margin-bottom:8px">어디서 나온 이야기: '+n['from']+'</div>';
  if(n.mem && n.mem.length){
    h+='<h3 style="margin-top:12px">내 메모 '+n.mem.length+'개</h3><ul class="list">';
    n.mem.forEach(function(m){ h+='<li><div class="m" style="opacity:.75">'+(m.ts||'').slice(0,10)+'</div><div class="t" style="font-weight:400">'+m.text+'</div></li>'; });
    h+='</ul>';
  }
  h+='<p class="note" style="margin-bottom:8px"><a href="#" data-add="'+n.id+'">＋ 이 별에 메모 달기</a></p>';
  if(n.href) h+='<p style="margin-bottom:8px"><a href="'+n.href+'">'+n.hl+' →</a></p>';
  h+='<h3 style="margin-top:12px">이어진 것 '+n.adj.length+'개</h3><ul class="list">';
  n.adj.forEach(function(a){
    var m=N[a.id];
    h+='<li><div class="t"><a href="#" data-go="'+a.id+'" style="color:'+m.c+'">'+m.full+'</a></div><div class="m">'+a.l+'</div></li>';
  });
  h+='</ul>';
  if(n.pot.length){
    h+='<h3 style="margin-top:12px">이어질 수 있는 것 '+n.pot.length+'개 <small style="color:var(--muted);font-weight:400">가능성</small></h3><ul class="list">';
    n.pot.slice().sort(function(a,b){return a.w-b.w;}).forEach(function(a){
      var m=N[a.id];
      h+='<li><span class="tag '+(a.w===1?'p0':(a.w===2?'p1':'p2'))+'">'+WD[a.w]+'</span><div class="t"><a href="#" data-go="'+a.id+'" style="color:'+m.c+'">'+m.full+'</a></div><div class="m">'+a.l+'</div><div class="m" style="opacity:.75">필요한 것: '+a.need+'</div></li>';
    });
    h+='</ul>';
  }
  h+='<p class="note"><a href="#" data-f="'+n.reg+'">← '+r.name+'</a> · <a href="#" data-go="home">별자리 전체</a></p>';
  panel.innerHTML=h;
}
function route(e){
  var ad=e.target.closest?e.target.closest('[data-add]'):null;
  if(ad){ e.preventDefault(); openForm('comment', ad.getAttribute('data-add')); return; }
  var a=e.target.closest?e.target.closest('[data-go],[data-f],[data-reg]'):null;
  if(!a) return; e.preventDefault();
  var g=a.getAttribute('data-go'), f=a.getAttribute('data-f')||a.getAttribute('data-reg');
  if(g==='home') home(); else if(g) show(g);
  else if(f==='exp') showExp(); else if(f==='buzz') showBuzz(); else if(f) showReg(f);
  panel.scrollIntoView({block:'nearest'});
}
panel.addEventListener('click',route);
document.getElementById('uniLeg').addEventListener('click',route);
['uniPossList','uniBuzzList'].forEach(function(id){ var q=document.getElementById(id); if(q) q.addEventListener('click',function(e){
  var a=e.target.closest?e.target.closest('[data-go]'):null; if(!a) return; e.preventDefault(); show(a.getAttribute('data-go'));
  var sk=document.querySelector('.sky'); if(sk) sk.scrollIntoView({block:'start',behavior:'smooth'}); }); });
var pl=document.getElementById('uniPossList');
if(pl) pl.addEventListener('click',function(e){
  var a=e.target.closest?e.target.closest('[data-go]'):null;
  if(!a) return; e.preventDefault(); show(a.getAttribute('data-go'));
  var sk=document.querySelector('.sky'); if(sk) sk.scrollIntoView({block:'start',behavior:'smooth'});
});
var b2=document.getElementById('uni2d'), b3=document.getElementById('uni3d');
function setMode(m){
  MODE=m; spin=(m==='3d')?1:0;
  if(m==='3d'){ rotY=HOME.rotY; rotX=HOME.rotX; zoom=CFG.Z3; } else { rotY=0; rotX=0; zoom=1; }
  b2.className = (m==='2d')?'on':''; b3.className=(m==='3d')?'on':'';
  tip.textContent = (m==='3d')?'손가락으로 끌어 돌리기 · 두 손가락으로 확대':'';
  draw();
}
b2.addEventListener('click',function(){setMode('2d');});
b3.addEventListener('click',function(){setMode('3d');});
document.getElementById('uniHome').addEventListener('click',function(){
  setMode('2d'); seed=20261005; place(); settle(); showP=true; bp.className='on'; home(); draw();
});
var bd=document.getElementById('uniDesk');
function setView(v){
  VIEW=v; CFG=VIEWS[v];
  W=CFG.W; H=CFG.H; CX=CFG.CX; CY=CFG.CY; F=CFG.F;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  nodes.forEach(function(n){ var a=CFG.A[n.reg]||CFG.A.core; n.ax=a[0]; n.ay=a[1]; n.az=a[2]; });
  sizeNodes();
  document.body.classList.toggle('uni-wide', v==='d');
  if(v!=='f'){ bd.className=(v==='d')?'on':''; bd.textContent=(v==='d')?'모바일':'데스크탑'; }
  if(MODE==='3d') zoom=CFG.Z3;
  seed=20261005; place(); settle(); draw();
  if(v!=='f'){ try{ localStorage.setItem('luke1b-uniview', v); }catch(e){} }
}
bd.addEventListener('click',function(){ setView(VIEW==='d'?'m':'d'); });
var bp=document.getElementById('uniPoss');
bp.addEventListener('click',function(){ showP=!showP; bp.className=showP?'on':''; apply(); });
document.getElementById('uniBuzz').addEventListener('click',function(){showBuzz();panel.scrollIntoView({block:'nearest'});});
document.getElementById('uniExp').addEventListener('click',function(){showExp();panel.scrollIntoView({block:'nearest'});});
document.getElementById('uniReset').addEventListener('click',function(){
  seed=20261005; place(); settle(); draw();
});

var drag=null, dragRot=false, moved=0, lastP=null, pt=svg.createSVGPoint(), pts={};
function loc(ev){ pt.x=ev.clientX; pt.y=ev.clientY; var m=svg.getScreenCTM(); return m?pt.matrixTransform(m.inverse()):{x:0,y:0}; }
function hitNode(p){
  var best=null, bd=1e9;
  nodes.forEach(function(n){ var rr=Math.max((n.r*(MODE==='3d'?n.ps:1))+10,14);
    var d=(n.px-p.x)*(n.px-p.x)+(n.py-p.y)*(n.py-p.y); if(d<rr*rr && d<bd){bd=d;best=n;} });
  return best;
}
svg.addEventListener('pointerdown',function(ev){
  pts[ev.pointerId]={x:ev.clientX,y:ev.clientY};
  var p=loc(ev), n=hitNode(p); moved=0; lastP={x:ev.clientX,y:ev.clientY};
  if(n && MODE==='2d'){ drag=n; n.drag=1; }
  else { dragRot=true; }
  try{svg.setPointerCapture(ev.pointerId);}catch(e){}
  ev.preventDefault();
});
svg.addEventListener('pointermove',function(ev){
  if(pts[ev.pointerId]) pts[ev.pointerId]={x:ev.clientX,y:ev.clientY};
  var ids=Object.keys(pts);
  if(MODE==='3d' && ids.length>=2){
    var a=pts[ids[0]], b=pts[ids[1]];
    var d=Math.hypot(a.x-b.x,a.y-b.y);
    if(svg._pd) zoom = Math.max(0.5, Math.min(2.2, zoom*(d/svg._pd)));
    svg._pd=d; moved+=20; return;
  }
  if(drag){ var p=loc(ev); moved+=Math.abs(p.x-drag.x)+Math.abs(p.y-drag.y); drag.x=p.x; drag.y=p.y; draw(); ev.preventDefault(); return; }
  if(dragRot && lastP){
    var dx=ev.clientX-lastP.x, dy=ev.clientY-lastP.y;
    moved+=Math.abs(dx)+Math.abs(dy);
    if(MODE==='3d'){ rotY += dx*0.008; rotX = Math.max(-1.1, Math.min(1.1, rotX + dy*0.006)); draw(); }
    lastP={x:ev.clientX,y:ev.clientY};
    ev.preventDefault();
  }
});
function endPtr(ev){
  delete pts[ev.pointerId]; if(Object.keys(pts).length<2) svg._pd=0;
  if(drag){ var n=drag; n.drag=0; drag=null; if(moved<6) show(n.id); }
  else if(dragRot){ dragRot=false; if(moved<6){ var p=loc(ev), n2=hitNode(p); if(n2) show(n2.id); } }
  lastP=null;
  try{svg.releasePointerCapture(ev.pointerId);}catch(e){}
}
svg.addEventListener('pointerup',endPtr);
svg.addEventListener('pointercancel',endPtr);
svg.addEventListener('wheel',function(ev){
  if(MODE!=='3d') return; ev.preventDefault();
  zoom = Math.max(0.5, Math.min(2.2, zoom*(ev.deltaY>0?0.94:1.06))); draw();
},{passive:false});

// ---------------- 전체 화면 ----------------
var stage=document.getElementById('uniStage'), bf=document.getElementById('uniFull'), prevView='m';
function fullCfg(w,h){
  var n=nodes.length, xm=(w>900? w-398 : w);
  var L=Math.max(86, Math.sqrt(xm*h/n)*0.90);
  return {W:w,H:h,XMAX:xm,CX:xm/2,CY:h/2,F:Math.max(w,h)*1.25,L:L,K:L*L*0.5,PL:L*1.55,Z3:0.9,
    G:0.013,FC:6.5,FS:Math.max(10,Math.min(16,L*0.095)),NR:Math.max(1,Math.min(1.9,L/100)),
    SEP:L*0.27,J:L*1.25,
    A:{core:[xm*0.50,h*0.50,0],ch:[xm*0.19,h*0.24,-130],kn:[xm*0.81,h*0.25,95],
       pr:[xm*0.82,h*0.74,115],base:[xm*0.18,h*0.75,-75],tool:[xm*0.50,h*0.86,15],
       my:[xm*0.50,h*0.30,40]}};
}
function sizeFull(){
  var r=stage.getBoundingClientRect();
  VIEWS.f=fullCfg(Math.max(320,Math.round(r.width)), Math.max(360,Math.round(r.height)));
  setView('f');
}
function enterFull(){
  if(VIEW!=='f') prevView=VIEW;
  stage.classList.add('full'); document.body.classList.add('uni-full');
  bf.className='on'; bf.textContent='화면 닫기';
  try{ if(stage.requestFullscreen) stage.requestFullscreen(); }catch(e){}
  try{ localStorage.setItem('luke1b-unifull','1'); }catch(e){}
  setTimeout(sizeFull, 60);
}
function exitFull(){
  stage.classList.remove('full'); document.body.classList.remove('uni-full');
  bf.className=''; bf.textContent='전체 화면';
  try{ if(document.fullscreenElement && document.exitFullscreen) document.exitFullscreen(); }catch(e){}
  try{ localStorage.removeItem('luke1b-unifull'); }catch(e){}
  setView(prevView==='f'?'m':prevView);
}
bf.addEventListener('click',function(){ if(stage.classList.contains('full')) exitFull(); else enterFull(); });
document.addEventListener('fullscreenchange',function(){
  if(!document.fullscreenElement && stage.classList.contains('full')) exitFull();
});
document.addEventListener('keydown',function(ev){
  if(ev.key==='Escape'){ if(form.classList.contains('on')) closeForm(); else if(stage.classList.contains('full')) exitFull(); }
});
var rsT=null;
window.addEventListener('resize',function(){
  if(!stage.classList.contains('full')) return;
  clearTimeout(rsT); rsT=setTimeout(sizeFull,180);
});

// ---------------- 메모 · 새 별 ----------------
var form=document.getElementById('uniForm'), ufKind=document.getElementById('ufKind'),
    ufName=document.getElementById('ufName'), ufTarget=document.getElementById('ufTarget'),
    ufLink=document.getElementById('ufLink'), ufText=document.getElementById('ufText'),
    ufNodeBox=document.getElementById('ufNodeBox'), ufLinkBox=document.getElementById('ufLinkBox'),
    ufList=document.getElementById('ufList');
function fillTargets(){
  var h='<option value="">(선택 안 함)</option>';
  D.regions.forEach(function(r){
    h+='<optgroup label="'+r.no+' '+r.name+'">';
    nodes.filter(function(n){return n.reg===r.id;}).forEach(function(n){ h+='<option value="'+n.id+'">'+n.full+'</option>'; });
    h+='</optgroup>';
  });
  h+='<optgroup label="루크"><option value="luke">루크 (ONE CREW)</option></optgroup>';
  var mine=nodes.filter(function(n){return n.mine;});
  if(mine.length){ h+='<optgroup label="＋ 내 메모">'; mine.forEach(function(n){ h+='<option value="'+n.id+'">'+n.full+'</option>'; }); h+='</optgroup>'; }
  ufTarget.innerHTML=h;
}
function syncKind(){
  var k=ufKind.value;
  ufNodeBox.style.display = (k==='node')?'':'none';
  ufLinkBox.style.display = (k==='node')?'':'none';
  document.getElementById('ufTitle').textContent = (k==='node')?'새 별 추가':'코멘트 달기';
}
ufKind.addEventListener('change',syncKind);
function renderNoteList(){
  if(!notes.length){ ufList.innerHTML='<p class="note" style="margin-top:14px">아직 올린 것이 없습니다.</p>'; return; }
  var h='<h3 style="margin-top:18px">올려둔 것 '+notes.length+'개</h3><ul class="list">';
  notes.slice().reverse().forEach(function(nt){
    var who = nt.kind==='node' ? ('새 별 · '+nt.name) : ('코멘트 · '+(nt.targetName||''));
    h+='<li><div class="t" style="font-size:14px">'+who+'</div><div class="m">'+(nt.text||'')+'</div>'+
       '<div class="m"><a href="'+ghUrl(nt)+'" target="_blank" rel="noopener">깃허브에 올리기</a> · <a href="#" data-del="'+nt.key+'">지우기</a></div></li>';
  });
  ufList.innerHTML=h+'</ul>';
}
ufList.addEventListener('click',function(e){
  var a=e.target.closest?e.target.closest('[data-del]'):null;
  if(!a) return; e.preventDefault();
  var k=a.getAttribute('data-del');
  notes=notes.filter(function(x){return x.key!==k;}); saveNotes(notes);
  location.reload();
});
function openForm(kind,target){
  fillTargets(); ufKind.value=kind||'node'; syncKind();
  ufName.value=''; ufLink.value=''; ufText.value='';
  ufTarget.value = target || (sel||'');
  renderNoteList();
  form.classList.add('on'); setTimeout(function(){ (kind==='comment'?ufText:ufName).focus(); },30);
}
function closeForm(){ form.classList.remove('on'); }
document.getElementById('uniAdd').addEventListener('click',function(){ openForm('node', sel||''); });
document.getElementById('ufClose').addEventListener('click',closeForm);
form.addEventListener('click',function(e){ if(e.target===form) closeForm(); });
function nameOf(id){ var n=N[id]||byId[id]; return n?n.full:''; }
function collect(){
  var k=ufKind.value, t=ufTarget.value, txt=(ufText.value||'').trim();
  var nm=(ufName.value||'').trim();
  if(k==='node' && !nm){ alert('이름을 적어주세요.'); return null; }
  if(k==='comment' && !t){ alert('어느 별에 다는 코멘트인지 골라주세요.'); return null; }
  if(!txt){ alert('내용을 적어주세요.'); return null; }
  var ts=new Date().toISOString();
  return {key:'k'+Date.now(), kind:k, id:'my-'+Date.now(), name:nm, target:t,
          targetName:nameOf(t), link:(ufLink.value||'').trim(), text:txt, ts:ts};
}
function ghUrl(nt){
  var title, body;
  if(nt.kind==='node'){
    title='[유니버스] 새 별: '+nt.name;
    body='종류: 새 별 (사업·채널·상품·도구)\\n이름: '+nt.name+'\\n설명: '+nt.text+
         '\\n이을 곳: '+(nt.targetName||'(없음)')+'\\n관계: '+(nt.link||'(없음)')+'\\n적은 때: '+nt.ts+
         '\\n\\n사업 유니버스 페이지에서 보냄 — 다음 갱신 때 지도에 반영해 주세요.';
  }else{
    title='[유니버스] 코멘트: '+(nt.targetName||'');
    body='종류: 코멘트\\n대상 별: '+(nt.targetName||'')+'\\n내용: '+nt.text+'\\n적은 때: '+nt.ts+
         '\\n\\n사업 유니버스 페이지에서 보냄 — 다음 갱신 때 지도에 반영해 주세요.';
  }
  return 'https://github.com/Yoo-Mideum/luke-1b/issues/new?labels=universe&title='+
         encodeURIComponent(title)+'&body='+encodeURIComponent(body);
}
function asText(nt){
  if(nt.kind==='node') return '유니버스에 새 별 추가\\n이름: '+nt.name+'\\n설명: '+nt.text+'\\n이을 곳: '+(nt.targetName||'(없음)')+'\\n관계: '+(nt.link||'(없음)');
  return '유니버스 코멘트\\n대상 별: '+(nt.targetName||'')+'\\n내용: '+nt.text;
}
document.getElementById('ufSave').addEventListener('click',function(){
  var nt=collect(); if(!nt) return;
  notes.push(nt); saveNotes(notes);
  try{ if(stage.classList.contains('full')) localStorage.setItem('luke1b-unifull','1'); }catch(e){}
  location.reload();
});
document.getElementById('ufGh').addEventListener('click',function(){
  var nt=collect(); if(!nt) return;
  notes.push(nt); saveNotes(notes);
  window.open(ghUrl(nt),'_blank','noopener');
  renderNoteList();
});
document.getElementById('ufCopy').addEventListener('click',function(){
  var nt=collect(); if(!nt) return;
  var t=asText(nt);
  try{ navigator.clipboard.writeText(t); alert('복사했습니다. 클로드 대화에 붙여넣으면 지도에 넣어 드립니다.'); }
  catch(e){ prompt('복사해서 클로드에 붙여넣으세요', t); }
});

home();
(function(){
  var v=null;
  try{ v=localStorage.getItem('luke1b-uniview'); }catch(e){}
  if(!v) v = (window.innerWidth>=1040) ? 'd' : 'm';
  if(v==='d') setView('d'); else { bd.textContent='데스크탑'; }
  var wasFull=null; try{ wasFull=localStorage.getItem('luke1b-unifull'); }catch(e){}
  if(wasFull==='1'){ prevView=(v==='d'?'d':'m'); stage.classList.add('full'); document.body.classList.add('uni-full');
    bf.className='on'; bf.textContent='화면 닫기'; setTimeout(sizeFull,60); }
})();
})();
</script>
"""
    NAME = {}
    for R in UNI_REGIONS:
        for Nn in R["nodes"]:
            NAME[Nn["id"]] = (Nn["full"], R["color"])
    NAME["luke"] = ("루크 (ONE CREW)", "#f0cd84")
    WLBL = {1:("지금 당장","p0"), 2:("이번 분기","p1"), 3:("내년","p2")}
    cards = []
    for w, cls in [(1,"accent"), (2,"gold"), (3,"")]:
        rows = [x for x in UNI_POSS if x[4]==w]
        if not rows: continue
        cards.append('<h3 style="margin:16px 0 8px">%s <small style="color:var(--muted);font-weight:400">%d개</small></h3>' % (WLBL[w][0], len(rows)))
        cards.append('<div class="card %s"><ul class="list">' % cls)
        for a,b,l,nd,_w in rows:
            an,ac = NAME[a]; bn,bc = NAME[b]
            cards.append('<li><div class="t"><a href="#" data-go="%s" style="color:%s">%s</a> <span style="color:var(--muted)">↔</span> <a href="#" data-go="%s" style="color:%s">%s</a></div><div class="m">%s</div><div class="m" style="opacity:.75">필요한 것: %s</div></li>' % (a,ac,an,b,bc,bn,l,nd))
        cards.append('</ul></div>')
    NM = {}
    for R in UNI_REGIONS:
        for Nn in R["nodes"]:
            NM[Nn["id"]] = (Nn["full"], R["color"])
    rank = sorted([i for i in UNI_BUZZ if UNI_BUZZ[i][0] or UNI_BUZZ[i][1]], key=lambda i:-buzz_score(i))
    rows = []
    tier = {3:("가장 많이 나온 축","accent"),2:("자주 나오는 축","gold"),1:("가끔 나오는 축","")}
    for t in (3,2,1):
        ids = [i for i in rank if buzz_heat(i)==t and i in NM]
        if not ids: continue
        rows.append('<h3 style="margin:16px 0 8px">%s <small style="color:var(--muted);font-weight:400">%d개</small></h3><div class="card %s"><ul class="list">' % (tier[t][0], len(ids), tier[t][1]))
        for i in ids:
            r,hh = UNI_BUZZ[i]; nm,cl = NM[i]
            rows.append('<li><div class="t"><a href="#" data-go="%s" style="color:%s">%s</a></div><div class="m">녹음 %d건 · %d번 언급</div></li>' % (i, cl, nm, r, hh))
        rows.append('</ul></div>')
    zero = [NM[i][0] for i in UNI_BUZZ if not (UNI_BUZZ[i][0] or UNI_BUZZ[i][1]) and i in NM]
    rows.append('<div class="card"><div class="t">최근 30일 녹음에 한 번도 안 나온 것 %d개</div><div class="m">%s</div>'
                '<div class="note">말이 안 나온다고 중요하지 않은 것은 아닙니다 — 혼자 만들고 있어서 대화에 안 올라오는 것(도구 쪽)과, 정말 멈춰 있는 것을 구분해 보세요.</div></div>' % (len(zero), " · ".join(zero)))
    rows.append('<div class="src">세는 법: 녹음 요약 노트에서 각 사업의 이름과 별칭이 나온 횟수. 제목에만 나오고 본문에 없으면 그대로 집계했고(원크루 13건이 그런 경우), \'법인\'처럼 다른 뜻으로 쓰인 말은 빼고, \'당근\'은 거래처 상품 판매 맥락과 수강생 재고 재판매 맥락을 나눠서 뒤쪽만 셌습니다. 사적인 녹음 18건과 2분 미만 23건은 제외했습니다. 사람이 말한 횟수이지 매출이나 중요도가 아닙니다.</div>')
    body = body.replace("__BUZZ__", "".join(rows)).replace("__BZWIN__", BUZZ_WINDOW).replace("__BZN__", str(BUZZ_SCANNED))
    body2 = body.replace("__POSS__", '<div id="uniPossList" class="uniPossGrid">' + "".join(cards) + '</div>')
    return body2.replace("__DATA__", json.dumps(data, ensure_ascii=False))

# ---------------------------------------------------------------- 할 일 설명서
GUIDES = [
 {"slug":"report-protocol","title":"보고 프로토콜 — 다른 채팅·코드가 상황판에 보고하는 법","p":"P1","due":"상시","why":"흩어진 채팅의 결과를 한 곳(상황판)에서 보려면 모든 채팅이 같은 형식으로 남겨야 한다. 클로드 채팅의 GitHub 커넥터는 읽기 전용이라 깃허브에 직접 못 쓴다 → 노션 액션보드에 남기고, 매일 06:40 갱신이 상황판으로 옮긴다.",
  "prep":["각 채팅·세션에 아래 '공통 지시문' 붙여넣기 (프로젝트 지침에 넣어두면 매번 안 붙여도 됨)","클로드 코드 세션은 선택적으로 add_repo(Yoo-Mideum/luke-1b, push)로 직접 push 가능 — 그러면 즉시 반영"],
  "steps":[
   ("언제","루크가 준 명령 하나가 최종 완료됐을 때, 또는 루크 결정이 필요해 막혔을 때. 중간 진행은 평소처럼 노션만."),
   ("무엇을","노션 액션보드에 항목 1개: 할 일 = \"[보고] <프로젝트> — <제목>\" · 상태 = 완료/진행 중/시작 전(막힘)/보류 · 프로젝트 = 같은 프로젝트는 같은 이름 · 기대 결과 = 한 줄 요약 · 메모 = \"다음: … | 결과물: <URL> | 채팅: <URL 또는 빈칸> | 출처: claude 또는 claude-code | 상세: …\" · 채팅 = \"상황판 보고 (날짜)\" · 막힘이면 메모 맨 앞에 \"[막힘] 루크 결정 필요: …\""),
   ("상황판 반영","매일 06:40 갱신이 [보고] 항목을 reports/index.json으로 옮기고(노션 페이지 id로 중복 방지) 상황판에 표시. 막힘은 허브 최우선 맨 위로 승격."),
   ("클로드 코드 세션 (선택)","즉시 반영이 필요하면 add_repo로 luke-1b 추가 → clone → reports/index.json 맨 앞에 객체 추가 → push. 노션 [보고]도 같이 남기면 중복은 갱신 때 id로 걸러짐."),
   ("채팅 답변은","세 줄: ①완료/막힘 한 줄 ②결과물 링크 ③\"노션 반영: n건 (보고 포함)\". 긴 설명은 메모 '상세'에."),
   ("링크 규칙","클로드 코드 원격 세션은 세션 URL(claude.ai/code/session_…)을 채팅 칸에. 클로드 채팅은 자기 URL을 모를 수 있음 → 루크가 주소를 주면 넣고, 아니면 빈칸. 로컬 터미널 세션은 프로젝트 폴더 경로."),
  ],
  "done":"노션에 [보고] 항목이 있고, 다음 날 06:40 이후 상황판(status/)에 카드가 보임.",
  "src":["노션 액션보드 2836c774… · 이 저장소 reports/index.json · status/index.html"]},
 {"slug":"developer-accounts","title":"개발자 계정 3종 등록","p":"P0","due":"10/2","why":"툴박스·영상공장·블로그타이퍼를 아이폰·갤럭시·맥·윈도우로 배포하려면 스토어 계정이 먼저다. Apple은 심사에 며칠 걸리므로 가장 먼저 시작.",
  "prep":["힐링디어스(주) 사업자등록증 · 대표자 신분증 · 법인카드 또는 개인 신용카드","회사 이메일(개인 지메일 X) · 2단계 인증 가능한 폰","법인으로 등록하려면 D-U-N-S 번호 (Apple 필수) — 없으면 개인 명의로 먼저 시작해도 됨"],
  "steps":[
   ("Apple Developer Program — 연 $99","https://developer.apple.com/programs/enroll/ 에서 Apple ID로 로그인 → 개인(Individual) 또는 조직(Organization) 선택. 조직은 D-U-N-S 번호 필수(정부기관 제외). 결제 후 승인 대기. 아이폰 앱과 맥 앱 공증(notarization) 둘 다 이 계정 하나로 됨."),
   ("Google Play Console — $25 1회","https://play.google.com/console 에서 Google 계정으로 가입 → 본인 법적 이름의 국가 발급 신분증 + 신용카드로 신원 확인 → $25 결제. 신규 개인 계정은 앱 게시 전 테스트 요구사항이 있음(테스터 수·기간은 Play 고객센터에서 확인 필요)."),
   ("Microsoft Store — 무료","https://storedeveloper.microsoft.com 에서 '무료로 시작' → 개별 개발자 또는 회사 선택 → 정부 발급 신분증 + 셀카로 신원 확인 → 파트너 센터 대시보드. 개별→회사 전환은 안 되니 회사로 낼 거면 처음부터 회사 계정."),
   ("윈도우 설치파일 '바이러스' 경고 대책","스토어 밖 exe 배포(셀수다 자동등록 등)에서 나는 SmartScreen 경고는 코드 서명 인증서가 별도로 필요. 비용·발급처는 확인 필요 — 이번 주는 계정 3종만 끝내고 이건 다음 항목으로."),
   ("등록 정보 한 곳에 기록","계정 이메일·결제일·갱신일(Apple 1년)·팀 ID를 노션 액션보드 메모 또는 비밀번호 관리자에. 갱신 놓치면 앱이 스토어에서 내려감."),
  ],
  "done":"세 계정 모두 대시보드 로그인이 되고, Apple은 '승인 대기' 이상 상태.",
  "src":["Apple: developer.apple.com/programs/enroll — $99/년, 조직은 D-U-N-S 필수","Google: support.google.com/googleplay/android-developer/answer/6112435 — $25 1회, 신분증+신용카드","Microsoft: learn.microsoft.com … partner-center-developer-account — 등록 무료, 신분증+셀카"]},
 {"slug":"platform-pd-meeting","title":"초이스토리 PD 화상 미팅 (모객 축 제안)","p":"P0","due":"10/5","why":"3자 구도의 첫 단추. PD가 모객을 맡아주면 10/8 본부장 미팅에서 완성형을 제시할 수 있다.",
  "prep":["<a href='../../platform/'>강의 플랫폼 전략</a> 페이지 한 번 읽기","메이브님과 배분 기준선(1:1:1, 광고비 선차감) 합의","우리 쪽 숫자: 추석 특강 100명 신청, 뷰셀 유튜브, 원크루 사례 2~3개"],
  "steps":[
   ("미팅 잡기","PD에게 카톡: '강의 플랫폼 3자 협업 건으로 30분 화상 가능하실까요' + 날짜 2개 제시. 메이브님 동석."),
   ("10분: 우리 그림","인베이더 없이 가는 이유(수취율 20% → 직접 하면 배분 1/3), 3축 구도 그림 보여주기(전략 페이지 도식 화면 공유)."),
   ("10분: PD 역할 제안","'모객·유입을 맡아주시면 좋겠다' — 보유 채널·인력 풀로 특강 신청자 모집. 책임 지표는 신청자 수와 신청당 비용."),
   ("5분: 커뮤니티 전담의 필요성","트래픽은 락인 없이는 새는 물. 그래서 커뮤니티 전담 축을 따로 두고 배분에 포함한다는 점을 먼저 설명(본부장 이름은 PD 반응 본 뒤)."),
   ("5분: 다음 단계","긍정이면 '10/8 이후 3자 미팅' 제안. 유보면 '무엇이 걸리는지' 하나만 묻고 마무리. 통화는 플라우드 녹음."),
  ],
  "done":"PD의 참여 의사(예/유보/아니오)와 걸리는 조건 1~2개가 노션 메모에 적혀 있음.",
  "src":["9/29 메이븐 회의 녹음 — PD 먼저 접촉 후 본부장 순서 결정"]},
 {"slug":"platform-director-meeting","title":"10/8 종혁 본부장 미팅 (락인 축 제안)","p":"P0","due":"10/8","why":"락인·커뮤니티 축을 맡길 사람. 챌린지 영상·네이버 카페·광고 운영을 같이 설계할 파트너.",
  "prep":["PD 미팅 결과","1:1:1 배분안 + 광고비 선차감 원칙 문서 1장","인베이더 실패 분석 3줄(큰돈 광고·폐쇄적 채널·상담 인력 부재)"],
  "steps":[
   ("역할 제안","챌린지 형식 영상 운영 + 네이버 카페 운영으로 수강생 락인 + 광고 운영을 루크와 같이. 책임 지표: 카페 활동률·재등록률·환불률."),
   ("배분 제안","커뮤니티 전담 포함 1:1:1. 본부장이 사람을 붙이면 그 비용은 락인 축 몫에서."),
   ("소유권 원칙","카페·채널·수강생 DB는 회사 명의. 콘텐츠 2차 활용권 명시. 기간 2~3년."),
   ("광고 운영 원칙 합의","광고 상한(1기 1,000만), 주간 숫자 리뷰, 신청당 비용 기준선 — '작은 수의 싸움'을 같이 하자는 프레임."),
   ("마무리","10월 중 3자 문서 1장 작성 일정 잡기. 녹음."),
  ],
  "done":"본부장의 참여 의사 + 배분·소유권에 대한 반응이 기록되고, 3자 문서 작성 날짜가 잡힘.",
  "src":["9/29 메이븐 회의 녹음 — 10/8 미팅 예정, 1:1:1","9/30 루크 구두 — 본부장 = 챌린지 영상·카페·광고"]},
 {"slug":"3pl-resale","title":"3PL 수강생 재고 당근·외부 판매 첫 등록","p":"P0","due":"10/1","why":"창고에 잠든 수강생 재고를 회사가 팔아 수수료(15~20%)를 만들고, 내년 자체 강의의 증거 자료로 쓴다.",
  "prep":["3PL 재고 시트 최신본","통신판매업 신고된 사업자(회사 명의) — 개인 계정 판매 금지","루나(사진 촬영) 시간 확보"],
  "steps":[
   ("동의서 1장","수강생에게 받을 것: 위탁 위임 · 수수료율(15~20%) · 정산 주기 · 희망가 · 미판매 시 처리. 카톡으로 배포, 동의한 사람만 진행."),
   ("시트에 열 3개 추가","'위탁 여부 / 희망가 / 사진'. 동의 재고부터 루나가 촬영해 링크 넣기."),
   ("당근 비즈프로필 개설","사업자 명의로. 프로필에 '수강생 재고 위탁 판매' 명시."),
   ("첫 30개 등록","동의 재고 중 회전 빠를 것 30개. 제목·가격은 시트 기준, 광고 10만 원 테스트."),
   ("정산 규칙","판매 즉시 시트에 기록, 월 1회 수강생 정산. 회사 수수료는 별도 계좌."),
  ],
  "done":"당근에 30개 이상 올라가 있고, 동의서·시트·정산 규칙이 한 폴더에 있음.",
  "src":["노션 액션보드 '3PL 수강생 재고 당근·외부 판매' (9/17)"]},
 {"slug":"dino-12weeks","title":"디노(미니쌤) 12주 빌드업 합의 → 10/5 시작","p":"P0","due":"10/4","why":"디노의 독립 수익(3개월 월 300만)이 서야 사무실 구조가 안정된다. PDF는 이미 완성됨.",
  "prep":["『미니쌤, 12주의 지도』 PDF","상품별 배분 비율 초안","1주차 콘셉트 3안"],
  "steps":[
   ("PDF 전달 + 30분 통화","목표 숫자(1달 90 / 2달 200 / 3달 350만)와 주차별 일정표를 같이 보며 '할 수 있겠나' 확인."),
   ("배분 비율 확정","파일럿 2.9만 / 키트 2.9만 / 원데이 4.9만 / 실무반 39만 / 대행 15만 — 각 상품의 디노:회사 비율을 숫자로."),
   ("1주차 콘셉트 선택","3안 중 루크가 고르고 디노가 동의. 첫 MVP(전자책 또는 상품 페이지) 2~3일 안에."),
   ("매일 8시간 일정표 붙이기","시간 기록 시트 공유. 주 1회 15분 점검 일정 고정."),
   ("10/5 시작 알림","디노 인스타 '공부 1일차' 첫 게시 확인."),
  ],
  "done":"디노가 12주 일정표에 동의했고, 1주차 콘셉트와 배분 비율이 노션에 적혀 있음.",
  "src":["노션 '디노(미니쌤) 인스타+AI 셀러 실무 교육 12주 빌드업안' (9/28)","9/28 디노 멘토링 녹음"]},
 {"slug":"onecrew-inquiry","title":"원크루·툴박스 문의 대응","p":"P0","due":"즉시","why":"문의 하나가 3,300만 원. 답이 늦거나 흔들리면 식는다.",
  "prep":["가격표: 원크루 정가 3,900만 / 수강생 출신 3,300만 · 일십백천 990만(할인가 언급 X) · 툴박스는 사전 신청","<a href='../../philosophy/'>삼각 파이프라인</a> 페이지 링크"],
  "steps":[
   ("1차 답변(당일)","정가만 안내 + '30분 통화로 상황 듣고 맞는지 같이 보자' 제안. 할부는 '네이버페이 신한카드 최대 60개월 세팅 가능'으로만(보장 X)."),
   ("통화 전","상대 스토어·매출 단계 1분 확인. 삼각형 중 몇 번째 줄까지 있는지 그림에 대입."),
   ("통화(30분)","현재 줄 → 다음 줄 → 원크루가 세워줄 것 순서. 마지막에 '결정은 며칠 뒤에' — 압박 X, 정리해주는 선배 톤."),
   ("후속","통화 요약 + 관련 사례 1개 카톡. 노션에 상태 기록."),
  ],
  "done":"문의자마다 '1차 답변 → 통화 → 후속' 3단계가 노션에 남아 있음.",
  "src":["노션 '오픈채팅 문의자 가격 안내' (9/26)","9/26 오픈채팅 문의 답변 다듬기 대화"]},
 {"slug":"free-live","title":"10월 말 무료 라이브 확정","p":"P0","due":"10/25(일) 확정 · 시간·링크 확인 필요","why":"록터뷰 2회차 영상에 신청 링크가 들어가야 신규 리스트가 생긴다. 날짜가 없으면 영상 설명란도 못 쓴다.",
  "prep":["10월 마지막 주 저녁 중 비는 날 2개","네이버 폼 또는 기존 신청 폼 템플릿(추석 특강 때 naver.me 링크 방식)"],
  "steps":[
   ("날짜·시간 확정","10월 마지막 주 평일 저녁 1회(예비 1회). 캘린더에 박기."),
   ("신청 폼 만들기","추석 특강 폼 복제 → 제목·날짜만 교체. 연락처 필수."),
   ("링크 배치","록터뷰 영상 설명란·고정댓글, 카톡방, 카페 공지, 인스타 프로필."),
   ("흐름 유지","라이브 당일 무료 → 7일 다시보기 → 이후 유튜브 멤버십 전용."),
  ],
  "done":"날짜·폼 링크가 노션에 있고 록터뷰 영상 설명란에 들어감.",
  "src":["노션 '10월 말 무료 라이브 날짜·시간·신청 링크 확정' (9/28)","플라우드 10/2 인터뷰 녹음 2건 — 10월 25일 저녁 7시 무료 라이브 특강, 참석자에게 자동 등록 프로그램 7일 이용권·소싱처 전자책 (확정 여부 확인 필요)"]},
 {"slug":"logistics-stabilize","title":"물류 안정화 — 책임자 단일화·이슈 보드·임시 규칙","p":"P0","due":"9/30~10/4","why":"입고 미처리 상태에서 운송장이 나가는 오류는 CS 폭탄. 책임자가 둘이면 아무도 안 고친다.",
  "prep":["9/28 주간 회의 노트","잔디 개인 채널"],
  "steps":[
   ("9/30 책임자 지정","업데이트/운영 책임자를 뿌요 또는 대표 한 명으로. 역할·권한 한 줄로 공지."),
   ("9/30 이슈 보드","현안 목록을 체크오프 보드로(잔디 스레드 1개 = 이슈 1개, 상태 태그)."),
   ("10/1 삭제/무효화 임시 규칙","요청 템플릿 → 승인 → 롤백 로그. 핸드오버 체크리스트도 같은 날."),
   ("10/2 프로세스 맵","전산-물류 전체 흐름 한 장 + 병목 표시(뿌요)."),
   ("10/4 운영 가이드 + 피크 운영안","월·화 택배 우선·검수 후순위, 금요일 사전 공지."),
   ("매일 30분","업무 시작 전 이슈 리뷰 + 대표 PC 로그 확인."),
  ],
  "done":"책임자 1명, 이슈 보드 가동, 임시 규칙 문서, 프로세스 맵, 운영 가이드 — 5개가 잔디에 있음.",
  "src":["9/28 주간 회의 녹음(업무 프로세스 효율화·물류 안정화)"]},
 {"slug":"kititi-trademark","title":"키티티바이지영 상표권 출원","p":"P0","due":"10/1","why":"등록까지 1년 이상. 2월 샵 오픈 역산하면 지금이 마지노선.",
  "prep":["공동인증서","로고 파일 — 문자만 vs 도형 포함 결정"],
  "steps":[
   ("KIPRIS 선행검색","kipris.or.kr 에서 '키티티' '키티티바이지영' 동일·유사 상표 확인."),
   ("상품류 확정","미용업·메이크업 서비스(44류)와 교육(41류) 등 — 정확한 류는 특허로 안내 확인 필요."),
   ("출원인코드 발급 → 출원서 제출","patent.go.kr(특허로). 원장 명의인지 회사 명의인지 먼저 결정."),
   ("접수번호 기록","노션 메모에. 심사 통지 오면 대응."),
  ],
  "done":"특허로 접수번호가 노션에 있음.",
  "src":["노션 '키티티바이지영 상표권 출원' (9/29)"]},
 {"slug":"lawsuit-support","title":"수강생 화장품법 소송 초동 대응 지원","p":"P0","due":"10/6","why":"답변서 기한(송달일+30일)을 넘기면 불리. 대응 전자책은 이미 만들어 둠.",
  "prep":["소장 대응 전자책 PDF(20쪽)","송달일·총 판매 수량 — 수강생에게 확인"],
  "steps":[
   ("송달일·판매 수량 받기","이 둘이 와야 답변서 빈칸이 채워짐."),
   ("판매 중단 확인","해당 상품 전 채널 판매 중지 캡처."),
   ("변호사 연결","전자책의 예시 답변서·합의 제안서를 들고 변호사 검토 1회."),
   ("전자소송 가입·답변서 제출","ecfs.scourt.go.kr, 조정 희망 기재. 원고 대리인에 합의 제안서 병행."),
  ],
  "done":"답변서가 기한 내 제출되고 합의 제안서가 발송됨.",
  "src":["노션 '수강생 화장품법 소송 초동 대응 지원' (9/29)"]},
 {"slug":"toolbox-presignup","title":"툴박스 사전 신청 안내 문구","p":"P0","due":"이번 주","why":"결제 심사 전이라 돈은 못 받지만 '기다리는 사람'은 지금 모을 수 있다.",
  "prep":["툴박스 사이트 가입 페이지(luke-toolbox.vercel.app)","창립멤버 조건(연 10만, 100명 한정) 확정 여부"],
  "steps":[
   ("문구 3줄","무엇(프로그램 구독) · 언제(결제 오픈 예정, 심사 후) · 지금 할 일(가입해두면 오픈 알림+창립가)."),
   ("사전 신청 = 회원가입","별도 폼 대신 사이트 가입으로 통일. 가입자 수가 곧 대기자 수."),
   ("오픈채팅 답변 + 고정 공지","문의자에게 먼저 보내고, 카톡방 공지로 올리기."),
   ("결제 심사 상태 확인","토스페이먼츠 심사 진행 상황 주 1회 체크."),
  ],
  "done":"안내 문구가 카톡방 공지에 있고, 가입자 수를 매주 기록.",
  "src":["노션 '구독권 오픈일·가격·사전 신청 방식 확정' (9/26)"]},
]

def guide_index_html():
    items=[]
    for g in GUIDES:
        items.append(f'<li data-g="{g["slug"]}"><span class="tag {g["p"].lower()}">{g["p"]}</span><span class="tag">{g["due"]}</span><div class="t"><a href="{g["slug"]}/">{g["title"]}</a></div><div class="m">{g["why"]}</div></li>')
    return f"""
<h1>할 일 설명서</h1>
<p class="note">각 항목을 '어떻게' 하는지 단계별로. 허브·일정·우선순위의 '설명서 →' 링크가 여기로 옵니다. 완료 체크는 설명서 안에서도 됩니다.</p>
<div class="card"><ul class="list tasks">{''.join(items)}</ul></div>
"""

def guide_page_html(g):
    prep=''.join(f'<li>{x}</li>' for x in g["prep"])
    steps=''.join(f'<li><div class="t">{i+1}. {t}</div><div class="d">{d}</div></li>' for i,(t,d) in enumerate(g["steps"]))
    src=''.join(f'<li>{x}</li>' for x in g["src"])
    return f"""
<div class="top" style="margin-top:-8px"><a href="../">← 설명서 목록</a><span></span></div>
<h1>{g["title"]}</h1>
<p><span class="tag {g["p"].lower()}">{g["p"]}</span><span class="tag">기한 {g["due"]}</span></p>
<div class="card accent"><h3>왜 지금</h3><p style="margin:0;font-size:14px">{g["why"]}</p></div>
<h2>준비물</h2>
<div class="card"><ul style="margin:0;padding-left:18px;font-size:14px">{prep}</ul></div>
<h2>순서</h2>
<div class="card"><ol class="tl" style="margin-top:6px">{steps}</ol></div>
<h2>끝난 기준</h2>
<div class="card gold"><p style="margin:0;font-size:14px">{g["done"]}</p></div>
<div class="card"><ul class="list"><li data-g="{g["slug"]}"><div class="t">{g["title"]}</div><div class="m">여기서 체크하면 허브에서도 완료로 보입니다</div></li></ul></div>
<div class="src"><b>근거</b><ul>{src}</ul></div>
"""

# ---------------------------------------------------------------- 정부지원사업
GRANTS = """
<h1>정부지원사업</h1>
<p class="note">루크 본인은 나이(만 39세 초과)·법인 대표권 때문에 창업 지원 대부분이 해당 없음. 이 페이지는 <b>키티티(윤지영 원장)·메이브님·디노·뿌요</b>가 받을 수 있는 것을 정리한 것. 2026-10-01 기준, 공고 원문에서 확인한 것만 [확인], 언론·정리글은 [2차], 못 찾은 것은 "확인 필요". 경쟁률은 공식 수치가 없으면 추정이라고 표시.</p>

<h2>먼저 알아야 할 규칙 <small>창업의 법적 정의</small></h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">업력은 '최초 개업일' 기준</div><div class="m">개인사업자는 사업자등록증 개업연월일. 기존 사업을 계속하면서 새 사업자를 또 내면 새 사업자는 '창업'으로 안 쳐준다(시행령 제2조 2호) [확인]</div></li>
    <li><div class="t">폐업 후 같은 업종 재창업은 1년 지나야 창업</div><div class="m">2026년 9월 시행 개정으로 3년 → 1년으로 단축 [2차: 아시아투데이·아시아경제 2026-08-25]. 중기부 보도자료 원문 확인 필요</div></li>
    <li><div class="t">제외 사유를 7년 안에 해소하면 해소한 날부터 창업 인정</div><div class="m">2026-01-01 시행 개정 [확인: 중기부 공지]</div></li>
    <li><div class="t">같은 해 창업사업화 사업 2개 동시 수행 불가, 누적 3회 선정 시 제외</div><div class="m">국세·지방세 체납, 채무불이행도 제외 [확인: 초창패 2026 공고]</div></li>
  </ul>
  <div class="src">법령: <a href="https://www.law.go.kr" target="_blank">law.go.kr</a> 중소기업창업 지원법 시행령 제2조 · 해설 <a href="https://cert.k-startup.go.kr/usr/info/policyInfo.do?tempValue=0102" target="_blank">창업기업확인시스템</a> · 개정 공지 <a href="https://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=86&bcIdx=1064087&parentSeq=1064087" target="_blank">mss.go.kr</a></div>
</div>

<h2>윤지영 원장 — 2026년에 지원할 수 있었던 것</h2>
<p class="note">전제: 1998년생(만 28세) 여성 · 서울 성북구 1인 메이크업샵(개인사업자, 업력 3년 이내, 오프라인 매출) · 대학원생 · 인스타 1,000+ · 2027년 2월 웨딩 중심 토탈샵 오픈 예정. <b>개업연월일 확인이 선행 과제</b> — 2027년 1~3월 공고 기준일에 3년을 넘으면 초기 트랙에서 빠진다.</p>

<div class="card">
  <h3>① 청년창업사관학교 16기 (중기부·중진공) <span class="tag p0">사업화자금</span></h3>
  <dl class="kv">
    <dt>자격</dt><dd>만 39세 이하 대표, 창업 3년 이내(기본과정) · 예비창업자 포함 [확인]</dd>
    <dt>지원</dt><dd>최대 1억(총사업비 70% 이내, 평균 0.7억) + 사무공간·코칭·판로 [확인] · 자부담 30% [2차]</dd>
    <dt>과제</dt><dd>서류 → 발표심사 → 협약 → 1년 입교 과정 [확인]</dd>
    <dt>2026 접수</dt><dd>1/30 ~ 2/13 · 기본 650 + 심화 300명 [2차: 아시아경제]</dd>
    <dt>경쟁률</dt><dd><b>5.5:1</b> (2025년 15기, 850명 모집·4,671명 지원, 중진공 발표) [확인]</dd>
    <dt>맞는 이유</dt><dd>나이·업력 충족. 토탈샵 확장 자금으로 가장 큼. 단 '혁신성' 평가라 레슨 VOD·웨딩 패키지 등 서비스 모델로 포장 필요</dd>
    <dt>링크</dt><dd><a href="https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?pbancClssCd=PBC010&schM=view&pbancSn=176107" target="_blank">K-Startup 공고</a> · <a href="https://start.kosmes.or.kr/yh_mbi011_001.do" target="_blank">사업소개</a> · 경쟁률 <a href="https://www.asiae.co.kr/article/2025032620465864400" target="_blank">아시아경제</a></dd>
  </dl>
</div>

<div class="card">
  <h3>② 초기창업패키지 일반형 (중기부·창업진흥원) <span class="tag p0">사업화자금</span></h3>
  <dl class="kv">
    <dt>자격</dt><dd>2023-01-23 ~ 2026-01-22 개업 · 나이 제한 없음 [확인]</dd>
    <dt>지원</dt><dd>평균 5천만, 최대 1억, 10개월 · <b>수도권 자부담 현금 30%</b> [확인: 공고 제2026-38호]</dd>
    <dt>과제</dt><dd>서류(2배수) → 심층인터뷰 → 발표. 평가 = 문제인식·실현가능성·성장전략·팀(PSST) [확인]</dd>
    <dt>2026 접수</dt><dd>1/23 ~ 2/13 · 400개사 내외 [확인]</dd>
    <dt>경쟁률</dt><dd>공식 수치 없음 · 추정 5~8:1 (청창사와 지원자 풀 겹치고 나이 제한 없음)</dd>
    <dt>링크</dt><dd><a href="https://www.kised.or.kr/menu.es?mid=a10205020000" target="_blank">창업진흥원</a> · <a href="https://www.k-startup.go.kr" target="_blank">K-Startup</a></dd>
  </dl>
</div>

<div class="card accent">
  <h3>③ 소상공인 도약 지원사업 (舊 강한소상공인 + 로컬크리에이터) <span class="tag p0">2027 1순위</span></h3>
  <dl class="kv">
    <dt>자격</dt><dd>정상 영업 중인 소상공인 · 업력·나이 무관 · 유형: 로컬기업 육성(초기) / 강한소상공인(성장) [확인]</dd>
    <dt>지원</dt><dd>1단계 300만 → 로컬 최대 5,000만 / 강한소상공인 최대 1억 · 자부담 20% 이상 [확인: 공고 전문]</dd>
    <dt>과제</dt><dd>서류 → 성장지원 1,000개사 → 권역 오디션 540개사 → 전국 오디션 [확인]</dd>
    <dt>2026 접수</dt><dd>4/1 ~ 5/6 (연장) [확인] · 가점: 신사업창업사관학교 수료 2점 등</dd>
    <dt>경쟁률</dt><dd>공식 수치 없음 · 추정 4~6:1 (성장지원 단계)</dd>
    <dt>맞는 이유</dt><dd>'라이프스타일·뷰티' 소상공인이 정확히 타깃. 오프라인 매출 있는 점포가 유리. 1인샵 → 웨딩 토탈샵 확장이 '성장' 서사 그대로</dd>
    <dt>링크</dt><dd><a href="https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000120120" target="_blank">기업마당 공고</a> · 접수 소상공인24</dd>
  </dl>
</div>

<div class="card">
  <h3>④ 소상공인 스마트상점 기술보급 (소진공)</h3>
  <dl class="kv">
    <dt>자격</dt><dd>정상 영업 점포 · 미용업은 제외 업종 아님 [확인: 공고문]</dd>
    <dt>지원</dt><dd>구입형 700만 한도(국비 70%) / 보편형 500만(50%) / 렌탈 연 350만 / S/W 연 30만(100%) [확인]</dd>
    <dt>2026 접수</dt><dd>3/13 ~ 4/1 · 서면평가 [확인] · 경쟁률 확인 필요(추정 2~3:1)</dd>
    <dt>맞는 이유</dt><dd>새 매장 예약·키오스크·CRM 설비 시점과 맞물림</dd>
    <dt>링크</dt><dd><a href="https://www.sbiz.or.kr/smst/main.do" target="_blank">sbiz.or.kr 스마트상점</a></dd>
  </dl>
</div>

<div class="card">
  <h3>⑤ 소상공인 온라인판로 지원 (판판대로) · ⑥ 서울시 소상공인 온라인 판로개척</h3>
  <dl class="kv">
    <dt>⑤</dt><dd>상세페이지·콘텐츠 제작, 라이브커머스 제작·운영, SNS 마케팅 메뉴판 신청 · 2차 접수 5/27~6/10 [확인] · 금액·자부담 메뉴별 확인 필요 · <a href="https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000122456" target="_blank">공고</a> · <a href="https://www.fanfandaero.kr" target="_blank">판판대로</a></dd>
    <dt>⑥</dt><dd>서울 소재 소상공인 약 300개사, 진단→전략→판로 개설 · 접수 ~5/25 [확인] · <a href="https://news.seoul.go.kr/economy/archives/572407" target="_blank">서울시 공고</a></dd>
    <dt>맞는 이유</dt><dd>레슨 VOD·전자책을 온라인 상품화할 때 콘텐츠 제작비·라이브커머스가 바로 연결</dd>
  </dl>
</div>

<div class="card">
  <h3>⑦ 여성창업경진대회 제27회 (여성기업종합지원센터) <span class="tag p1">상금·가점</span></h3>
  <dl class="kv">
    <dt>자격</dt><dd>창업 7년 미만 여성 창업팀 + 예비 · 분야에 <b>K-뷰티</b> 명시 [확인]</dd>
    <dt>지원</dt><dd>44팀 포상 총 1.1억 · 3년 미만 상위 13팀 '도전! K-스타트업' 예선 진출 [확인]</dd>
    <dt>2026 접수</dt><dd>3/23 ~ 4/16 [확인]</dd>
    <dt>경쟁률</dt><dd><b>39:1</b> (1,712팀 지원 / 44팀 포상, 센터 발표) [확인: 아시아경제 2026-04-28]</dd>
    <dt>링크</dt><dd><a href="https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000120559" target="_blank">공고</a> · <a href="https://www.wbiz.or.kr" target="_blank">wbiz.or.kr</a></dd>
  </dl>
</div>

<div class="card">
  <h3>⑧ 학생 창업유망팀 300+ (교육부) · ⑨ 창업중심대학 · ⑩ 성북구 창업챌린지</h3>
  <dl class="kv">
    <dt>⑧</dt><dd>구성원 전원 학생(대학원생 포함 여부 확인 필요) · 멘토링·시제품·교육부장관 인증서(타 사업 가점) · 접수 4/2~4/27 [확인] · <a href="https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000121096" target="_blank">공고</a> · <a href="https://u300.kr" target="_blank">u300.kr</a></dd>
    <dt>⑨</dt><dd>예비~7년 이내, 지역기반 평균 5천·최대 1억, 청년 60% 우선, 기창업자 자부담 30% [2차] · 접수 3/3~3/23 [확인] · 서울 권역 담당 대학 확인 필요 · 추정 5:1</dd>
    <dt>⑩</dt><dd>성북구 3년 이내 창업자, 5개사 × 약 600만 + 성신여대 등 6개 대학 창업지원단 인큐베이팅 · 접수 ~4/6 [2차: 서울신문] · ICT 접목 우대 · <a href="https://go.seoul.co.kr/news/newsView.php?id=20260324500168" target="_blank">기사</a></dd>
  </dl>
</div>

<div class="card">
  <h3>⑪ 서울뷰티위크 비즈니스 밋업 피칭 · ⑫ SBA 크리에이티브포스(뷰티) · ⑬ 서울창업허브</h3>
  <dl class="kv">
    <dt>⑪</dt><dd>예비~7년 이내 뷰티·웰니스·플랫폼, 9팀, 총 상금 2,000만(대상 1,000만), 접수 5/26~6/26 [확인] · 제품·테크 중심이라 VOD 플랫폼 모델로 접근해야 가능성 · <a href="https://news.seoul.go.kr/economy/archives/572984" target="_blank">공고</a></dd>
    <dt>⑫</dt><dd>서울 1인 창작자, 뷰티 트랙은 채널 6개월·K-뷰티 콘텐츠 10개 이상(2024 기준), 완주 시 제작비 500만 [2차] · 2026 공고 확인 필요 · <a href="https://creativeforce.sba.kr" target="_blank">creativeforce.sba.kr</a></dd>
    <dt>⑬</dt><dd>공덕 입주(7년 이내, 4/6~4/20), AI 솔로창업단(1인 창업자, 6/29~7/15) [2차] · 투자형 스타트업 지향이라 지금 모델과는 거리 · <a href="https://www.startup-plus.kr" target="_blank">startup-plus.kr</a></dd>
  </dl>
</div>

<div class="card">
  <h3>⑭ 대출 — 보조금보다 현실적인 '보증금·인테리어' 재원</h3>
  <dl class="kv">
    <dt>서울시 창업기업자금</dt><dd>서울신용보증재단 창구, 최대 1억, 이차보전 1.8%(4년), 상시 접수 [2차: 복지로 요약] · <a href="https://www.seoul.go.kr/news/news_notice.do?nttNo=465395" target="_blank">서울시 공고</a> · <a href="https://www.seoulshinbo.co.kr" target="_blank">서울신보</a></dd>
    <dt>청년고용연계자금</dt><dd>만 39세 이하 대표, 한도 7천만, 기준금리(가산 없음), 거치 2년+상환 3년, 미용업 가능 [확인: 공고 제2025-656호] · 분기별 접수 · <a href="https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_000000000117021" target="_blank">공고</a> · <a href="https://ols.semas.or.kr" target="_blank">소진공 OLS</a></dd>
    <dt>청년전용창업자금</dt><dd>중진공, 만 39세 이하·업력 3년 미만, 한도 1억, 연 2.5% 고정 [2차] · 2026 공고 원문 확인 필요 · <a href="https://www.gov.kr/portal/service/serviceInfo/142000000099" target="_blank">정부24</a></dd>
  </dl>
</div>

<div class="card">
  <h3>2026년에 자격이 안 됐던 것</h3>
  <p style="font-size:14px;margin:0">예비창업패키지(사업자 미보유자만, 3/6~3/24) · 신사업창업사관학교(예비창업자 대상) · 생애최초 청년창업(만 29세 이하 예비창업자)</p>
</div>

<h2>윤지영 원장 — 2027년 도전 리스트</h2>
<div class="card red">
  <p style="font-size:14px;margin:0 0 8px"><b>2027년 2월 새 샵 오픈이 업력에 미치는 영향:</b> 기존 사업자를 유지한 채 새 사업자를 추가해도, 폐업하고 동종 사업자를 새로 내도 업력은 <b>최초 개업일 기준</b>. 가장 단순한 길은 <b>같은 사업자에 사업장 이전 + 업종 추가(헤어·에스테틱)</b> — 지원사업상 불이익 없음.</p>
</div>
<div class="card wrapx">
<table>
<tr><th>사업</th><th>2027 자격</th><th>공고 시기</th><th>금액</th></tr>
<tr><td><b>소상공인 도약 지원</b></td><td>유지(업력 무관) — 1순위</td><td>4월</td><td class="num">~1억</td></tr>
<tr><td>청년창업사관학교 17기</td><td>만 29세 · 업력 3년 이내면 기본, 넘으면 심화(7년)</td><td>1월 말~2월</td><td class="num">~1억</td></tr>
<tr><td>초기창업패키지</td><td>업력 3년 이내일 때만</td><td>1월 말~2월</td><td class="num">~1억</td></tr>
<tr><td>창업중심대학</td><td>유지(7년 이내)</td><td>3월</td><td class="num">~1억</td></tr>
<tr><td>스마트상점 기술보급</td><td>유지 — 새 매장 설비와 맞물림</td><td>3월</td><td class="num">~700만</td></tr>
<tr><td>온라인판로(판판대로)</td><td>유지</td><td>3~4월 / 5~6월</td><td class="num">메뉴별</td></tr>
<tr><td>서울시 온라인 판로개척</td><td>유지</td><td>4~5월</td><td class="num">확인 필요</td></tr>
<tr><td>여성창업경진대회</td><td>유지(7년 미만)</td><td>3월 중순~4월</td><td class="num">상금</td></tr>
<tr><td>서울뷰티위크 피칭</td><td>유지(7년 이내)</td><td>5~6월</td><td class="num">~1,000만</td></tr>
<tr><td>학생 창업유망팀 300+</td><td>대학원 재학 중이면</td><td>4월</td><td class="num">인증·멘토링</td></tr>
<tr><td>성북구 창업챌린지</td><td>성북구 내 유지 시</td><td>3~4월</td><td class="num">~600만</td></tr>
<tr><td>서울신보 창업자금 / 청년고용연계 / 청년전용창업</td><td>유지(청년전용은 업력 3년 미만)</td><td>연중·분기</td><td class="num">7천만~1억</td></tr>
</table>
<div class="note">같은 해에 중앙정부 창업사업화(청창사·초창패·창업중심대학) 2개 동시 수행 불가 → 하나 고르고, 소상공인 도약·스마트상점·판로는 별도 축이라 병행 가능(확인 필요).</div>
</div>

<h2>2027년 일정 역산 <small>지금부터</small></h2>
<div class="card">
  <ol class="tl" style="margin-top:6px">
    <li><div class="d">10월</div><div class="t">개업연월일 확인 · 사업자 하나로 갈지 결정 · 매출 증빙 정리(월별 카드·현금영수증)</div></li>
    <li><div class="d">11월</div><div class="t">PSST 사업계획서 초안 — 문제(웨딩 준비 동선 분산) / 해결(토탈샵+레슨 VOD) / 성장(교육·전자책·플랫폼) / 팀</div></li>
    <li><div class="d">12월</div><div class="t">K-Startup 회원가입·기업정보 등록, 세금 체납 0 확인, 인스타 콘텐츠 10개 이상 정리(크리에이티브포스용)</div></li>
    <li class="big"><div class="d">1월 말~2월</div><div class="t">청창사 17기 또는 초창패 중 하나 접수 (둘 다 넣고 한 곳만 수행 가능)</div></li>
    <li><div class="d">3월</div><div class="t">스마트상점 · 창업중심대학 · 여성창업경진대회 · 성북구 챌린지</div></li>
    <li class="big"><div class="d">4월</div><div class="t">소상공인 도약 지원 (1순위) · 학생 창업유망팀 300+</div></li>
    <li><div class="d">5~6월</div><div class="t">온라인판로 2차 · 서울시 판로개척 · 서울뷰티위크 피칭</div></li>
  </ol>
</div>

<h2>디노 — 9년 사업자 폐업하고 1년 사업자만 두면?</h2>
<div class="card gold">
  <ul class="list">
    <li><div class="t">지금(두 사업자 병행) 상태로는 1년 사업자가 '창업'이 아니다</div><div class="m">기존 사업을 계속하면서 새로 낸 사업 → 시행령 제2조 2호. 청창사·초창패 신청 불가(또는 9년 기준) [확인]</div></li>
    <li><div class="t">9년 사업자를 폐업하면 → 폐업일(해소일)부터 1년 사업자가 창업기업으로 인정</div><div class="m">2026-01-01 개정 "제외 사유 해소 시 해소일부터 창업 인정" [확인]. 단 업력 기산점이 1년 사업자 개업일인지 해소일인지는 공고 FAQ 확인 필요</div></li>
    <li><div class="t">두 사업자가 같은 업종(온라인 판매)이면 '폐업 후 동종 계속' 논점 추가</div><div class="m">1년 사업자의 업종코드가 9년 사업자와 다른지 먼저 확인. 같으면 폐업 후 1년 경과 기준이 걸릴 수 있음(확인 필요)</div></li>
    <li><div class="t">폐업 후 가능 후보</div><div class="m">청년창업사관학교(만 39세 이하면) · 초기창업패키지(3년 이내) · 창업중심대학(7년 이내) · 소상공인 도약·온라인판로(소상공인이면 폐업 무관) · 재도전성공패키지는 '재창업이 폐업보다 먼저'라 자격 해석 불확실 → 주관기관 문의</div></li>
    <li><div class="t">폐업 전 체크</div><div class="m">9년 사업자의 창업사업화 선정 이력(누적 3회 제한) · 세금 체납 0 · 폐업 시점이 2027년 1~2월 공고 기준일 <b>이전</b></div></li>
  </ul>
  <div class="src">재도전성공패키지 2026(폐업 후 재창업 7년 이내, 최대 1억, 접수 2/11~3/4) · 희망리턴패키지 재창업 성장형(폐업 후 재창업 1년 이내, 최대 2,000만) <a href="https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000117934" target="_blank">공고</a> · 서울형 다시서기 <a href="https://news.seoul.go.kr/economy/archives/573571" target="_blank">서울시</a></div>
</div>

<h2>메이브님 · 뿌요 — 바로 볼 것</h2>
<div class="card">
  <dl class="kv">
    <dt>메이브님</dt><dd>업력·나이 확인 필요. 3년 이내면 청창사(39세 이하)·초창패, 3~7년이면 창업도약패키지·창업중심대학. 소상공인 도약 지원은 업력 무관. 뷰셀 유튜브가 있으니 콘텐츠 제작비 쪽(온라인판로·크리에이티브포스)도 해당</dd>
    <dt>뿌요</dt><dd>사업자 유무·나이 확인 필요. 예비창업자면 예비창업패키지(3월)·신사업창업사관학교·생애최초 청년창업(만 29세 이하). 사업자 있으면 위 윤지영 표와 동일 기준</dd>
    <dt>루크</dt><dd>해당 없음(만 39세 초과 + 법인 대표). 힐링디어스 법인 설립일 기준 3년 이내면 초창패, 7년 이내면 디딤돌 R&D(소명서·효율 계산기 등 프로그램을 기술개발 과제로) 가능성만 남음 — 설립일 확인 필요</dd>
  </dl>
</div>

<h2>공통 준비물</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">PSST 사업계획서</div><div class="m">문제인식 · 실현가능성 · 성장전략 · 팀. K-Startup 공고 첨부 양식, 온라인 접수만 [확인]</div></li>
    <li><div class="t">자기부담금</div><div class="m">초창패 수도권 현금 30% · 청창사 30% · 창업중심대학 기창업 30% · 소상공인 도약 20% · 스마트상점 30~50% · 예비창업자는 100% 지원 가능 · VAT는 미지원 [2차]</div></li>
    <li><div class="t">가점 만들기</div><div class="m">여성창업경진대회 수상, 학생창업유망팀 인증서, 신사업창업사관학교 수료(도약 지원 2점) — 2026년 안에 하나라도 따두면 2027 본게임에 가점</div></li>
    <li><div class="t">공통 제외</div><div class="m">세금 체납 · 채무불이행 · 창업사업화 3회 이상 · 동일연도 중복 수행 · 환수금 미반환</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">원문 접근 실패로 '확인 필요'로 남긴 것: K-Startup 공고 본문(빈 페이지), law.go.kr 조문, 중진공·소진공 사이트, 2026 신사업창업사관학교 공고, 서울시 육성자금 첨부. 세부 요건은 매년 바뀌니 2027년 공고는 반드시 원문으로. 조사: 2026-10-01 클로드 웹 리서치.</div>
"""


# ---------------------------------------------------------------- 상황판
STATUS = """
<h1>상황판</h1>
<p class="note">다른 클로드 채팅·클로드 코드가 작업을 끝내면 노션 액션보드에 <b>[보고]</b> 항목을 남기고, 매일 06:40 갱신이 그걸 <code>reports/index.json</code>으로 옮겨 이 페이지에 보여줍니다(클로드 코드 세션은 직접 push하면 즉시). 보고 규칙은 <a href="../guides/report-protocol/">보고 프로토콜</a>.</p>
<div class="card" style="padding:10px 12px">
  <div class="btnrow" style="margin:0" id="filters"></div>
</div>
<div id="statusBody"><div class="card"><div class="empty">불러오는 중…</div></div></div>
<script>
(async function(){
  const root=(window.LUKE_ROOT||'../');
  let data=[];
  try{ const r=await fetch(root+'reports/index.json?t='+Date.now()); data=await r.json(); }catch(e){ document.getElementById('statusBody').innerHTML='<div class="card"><div class="empty">reports/index.json 을 읽지 못했습니다.</div></div>'; return; }
  data.sort((a,b)=>a.date<b.date?1:-1);
  const q=new URLSearchParams(location.search); let proj=q.get('p')||'전체'; const rid=q.get('r');
  const projects=['전체',...Array.from(new Set(data.map(d=>d.project))).sort()];
  const F=document.getElementById('filters');
  F.innerHTML=projects.map(p=>'<button class="btn '+(p===proj?'pri':'')+'" data-p="'+p+'">'+p+'</button>').join('');
  F.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;proj=b.dataset.p;history.replaceState(null,'','?p='+encodeURIComponent(proj));F.querySelectorAll('button').forEach(x=>x.classList.toggle('pri',x.dataset.p===proj));render();});
  const S={'진행 중':'p1','완료':'done','보류':'p3','막힘':'p0'};
  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function links(d){let h='';if(d.deploy_url)h+='<a class="btn" href="'+esc(d.deploy_url)+'" target="_blank">결과물 열기</a>';if(d.chat_url)h+='<a class="btn" href="'+esc(d.chat_url)+'" target="_blank">'+(d.source==='claude-code'?'클로드 코드 세션':'클로드 채팅')+' 열기</a>';if(d.notion_url)h+='<a class="btn" href="'+esc(d.notion_url)+'" target="_blank">노션</a>';return h?'<div class="btnrow">'+h+'</div>':'';}
  function card(d,open){return '<div class="card'+(d.status==='막힘'?' red':'')+'" id="r-'+esc(d.id)+'"><div><span class="tag '+(S[d.status]||'')+'">'+esc(d.status)+'</span><span class="tag">'+esc(d.project)+'</span><span class="tag">'+esc(d.date.slice(5).replace('-','/'))+'</span><span class="tag">'+(d.source==='claude-code'?'코드':'채팅')+'</span></div><h3 style="margin-top:6px">'+esc(d.title)+'</h3><p style="font-size:14px;margin:4px 0">'+esc(d.summary)+'</p>'+(d.next?'<div class="m" style="font-size:13px;color:var(--muted)">다음: '+esc(d.next)+'</div>':'')+(d.detail?'<details'+(open?' open':'')+' style="margin-top:8px"><summary style="font-size:13px;color:var(--muted);cursor:pointer">자세히</summary><div style="font-size:14px;margin-top:6px">'+d.detail+'</div></details>':'')+links(d)+'</div>';}
  function render(){
    const rows=data.filter(d=>proj==='전체'||d.project===proj);
    const groups=[['막힘','막힘 — 루크 결정 필요'],['진행 중','진행 중'],['완료','완료 (최근 30건)'],['보류','보류']];
    let h='';
    const byProj={}; rows.forEach(d=>{(byProj[d.project]=byProj[d.project]||{}); byProj[d.project][d.status]=(byProj[d.project][d.status]||0)+1;});
    if(proj==='전체'){h+='<h2>프로젝트별 <small>'+rows.length+'건</small></h2><div class="card wrapx"><table><tr><th>프로젝트</th><th>진행 중</th><th>완료</th><th>막힘</th><th>마지막 보고</th></tr>'+Object.keys(byProj).sort().map(p=>{const last=rows.find(d=>d.project===p);return '<tr><td><a href="?p='+encodeURIComponent(p)+'">'+esc(p)+'</a></td><td class="num">'+(byProj[p]['진행 중']||0)+'</td><td class="num">'+(byProj[p]['완료']||0)+'</td><td class="num" style="color:var(--red)">'+(byProj[p]['막힘']||0)+'</td><td>'+esc(last.date.slice(5).replace('-','/'))+'</td></tr>';}).join('')+'</table></div>';}
    for(const [st,label] of groups){let g=rows.filter(d=>d.status===st); if(st==='완료')g=g.slice(0,30); if(!g.length)continue; h+='<h2>'+label+' <small>'+g.length+'</small></h2>'+g.map(d=>card(d,d.id===rid)).join('');}
    document.getElementById('statusBody').innerHTML=h||'<div class="card"><div class="empty">보고가 없습니다.</div></div>';
    if(rid){const el=document.getElementById('r-'+rid); if(el) el.scrollIntoView();}
  }
  render();
})();
</script>
"""

# ---------------------------------------------------------------- 출처
SOURCES = """
<h1>출처 · 갱신 방법</h1>

<h2>이 페이지의 근거</h2>
<div class="card src">
  <p>모든 숫자·날짜·이름은 루크 본인의 기록에서 가져왔습니다. 외부 검색으로 확인한 사실은 없으며, 계획값은 실적이 아닙니다.</p>
  <h3>플라우드 녹음 (요약 노트)</h3>
  <ul>
    <li>10-08 녹음: 회의 3건(성북구 미용업 권리양수도 · 상가 임대차 계약 설명 · 임대차 계약 체결) — Action Item은 임차인(지영 원장)·양도인·중개 측 담당이라 노션에 새로 만든 항목 없음. 루크 담당 후속 2건(인테리어 승인 별첨 문서 · 특약 수정안 협상)은 당일 클로드 대화가 이미 노션에 등록. 계약 금액은 녹음 요약끼리 맞지 않는 숫자가 있어 페이지에 싣지 않음(확인 필요). '캐주얼 모임' 녹음과 제목 없는 28초 녹음은 읽지 않음</li>
    <li>10-07 녹음: 김종진 대표님 10기 코칭 · [OneCrew] 정복녀 대표님 7기 · [OneCrew] 최은봉 대표님 · 9/30 김종진 대표님 코칭(10/7 업로드) — 루크 담당 Action Item(조사 결과 검토 · 강사 런칭 지원 · 상담 요약 전달)은 당일 클로드 대화가 이미 노션에 등록해 새로 만든 항목 없음. '인터뷰: 리더십·샵 비전'과 '메모: 샵 매니저 역할·사무실 위치'는 담당·기한이 없는 메모라 넣지 않음(확인 필요). '일상 대화'와 개인 녹음 2건은 읽지 않음</li>
    <li>10-06 녹음 6건: 디노(김수민) 미팅 · 가격관리 프로그램 운용 실습 강의 · 메이븐(신정현) 15:00 회의 · 초월스토리 영상 촬영(자동화 시스템·성장 전략) · 메이븐/초월스토리 신규 강사 협업 회의 · 박태경 원크루 5회차 — 루크 담당 Action Item 대부분은 당일 클로드 대화에서 이미 노션에 등록돼 있었고, 빠져 있던 3건만 새로 등록(디노 토요일 평가 미팅 10/10 · 디노 전자책 지원 여부 10/17 · 돈블지PD 오프라인 사업 수익 구조화 — 이름·기한 확인 필요). 수강생·고객이 할 과제는 넣지 않음</li>
    <li>10-03 인터뷰: 네이버 온라인 셀러 운영과 자동화 판매 방식 (촬영) — Action Item 없음. 10/25(일) 저녁 무료 특강 안내만 확인(이미 일정에 있음). 촬영 뒤 개인 대화는 넣지 않음</li>
    <li>10-03 원크루 상담(홍○○ 대표님) — 후속 2건(리포트 링크 발송 10/4 · 재문의 확인 10/17)은 당일 클로드 대화에서 이미 노션에 등록돼 있어 일정에만 반영. AI 요약의 '해야 할 일' 8건은 담당이 적혀 있지 않은 제안 목록이라 새로 만들지 않음</li>
    <li>10-02 멘토링: 상품 소싱 및 온라인 판매 전략 — 루크 담당 Action Item 6건을 노션에 새로 등록 · 10-02 인터뷰 3건(온라인 셀러 멘토루크 · 스마트스토어 소자본 창업 · 강의·사업·성장 방식) — Action Item 없음, 무료 라이브 특강 일시(10/25 19:00)와 참석자 선물 언급만 반영</li>
    <li>09-30 박태경 원크루(2건) · 최은봉 대표님 · 정○○ 대표님 원크루 · 수강생 소장 대응 상담 — 컨설팅 Action Item 중 루크 담당분만 반영 (건강·개인사 제외)</li>
    <li>09-29 메이븐 — 신규 강의 플랫폼 사업 구상 및 전략 수립 회의 (19:16~20:11, 54분). <b>'본부장+초월스토리 강의 플랫폼' 녹음을 10/4에 다시 찾아본 결과 이 1건이 유일</b> — 8/15 이후 녹음 157건 전체에서 본부장·초이스토리·플랫폼 관련은 이것뿐이고, 혼자 정리한 녹음은 없음. 녹음 표기는 '초이스토리 PD'·'종혁 본부장'</li>
    <li>10-02 인터뷰: 멘토루크와 신정현의 강의·사업·성장 방식 — 인터뷰어는 <b>돈벌쥐 PD</b>(성북구 스튜디오·영상 촬영)로 '초이스토리 PD'와 다른 사람. 10/4에 이 녹음을 강의 플랫폼 모객 축 근거로 잠깐 반영했다가 루크 확인 후 되돌림. 강의 플랫폼 내용은 메이븐(신정현)님과의 대화만 사용</li>
    <li>09-29 하루를 4번 쓰는 법 (작업 슬롯 메모)</li>
    <li>09-28 회의 — AI 영상 제작 전략·신규 사이트·자동 등록 오류·소싱 재교육</li>
    <li>09-28 주간 회의 — 업무 프로세스 효율화 및 물류 시스템 안정화</li>
    <li>09-28 디노(김수민) 멘토링 · 09-07 관계 정리 상담 (개인사 제외)</li>
    <li>09-26 상담: 지영 — 정부지원사업 · 09-09 지영 확장 미팅/갈매 · 09-04 지영 뷰티 사업 현금흐름 회의</li>
    <li>09-17 [뿌요] 사업 운영 최적화 노트 · 09-11 상담: 최근영(뿌요) · 09-16 디노 번아웃 멘토링</li>
    <li>09-30 루크 구두 — 개발자 등록 최우선, 플랫폼 3자 역할(PD 모객 / 본부장 락인 / 루크·메이브님 플레이어) · 개발자 등록 비용은 Apple·Google·Microsoft 공식 페이지 확인</li>
    <li>09-10 박태경 원크루 1회차 · 09-16 최은봉 원크루 · 09-27 김종진 대표 멘토링 · 09-25 특강(순수익 300만원 시간 운영·사입)</li>
  </ul>
  <h3>클로드 대화</h3>
  <ul>
    <li>1년 내 10억 수익 달성을 위한 사업 전략 컨설팅 (7월)</li>
    <li>온라인 부업 수익 모델 전략 상담 (8/29) · 9월 수익 전략 (9/15, 9/17)</li>
    <li>추석 특강 후 원크루 전환 전략 (9/17~26) · 오픈채팅 문의 답변 다듬기 (9/26)</li>
    <li>디노 인스타+AI 사업 빌드업 (9/28) · 뷰셀 10분 대본 빌드업 (9/29)</li>
  </ul>
  <h3>노션 '루크 액션보드'</h3>
  <ul><li>전체 항목의 할 일·기한·상태·[결정] (10/10 06:40 조회). 미완료·기한 있는 항목은 일정에, 최근 7일 새 항목은 우선순위에 반영. 목표가 '사업 외 개인'인 항목은 넣지 않음(상표권 제외)</li>
  <li>10/1 새로 만든 항목 9건: 박태경 대표님 지원 5건(플라우드 9/30), 사무실 임대료 정산·서울 이전 로드맵·트레이드 채널·'하루를 4번 쓰는 법' 영상(플라우드 9/29). 뒤 4건의 기한은 추정이라 '확인 필요'로 표시</li>
  <li>10/2 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/1에 노션에 새로 생긴 기한 항목 7건을 일정에 추가(상표 출원·키티티 사이트·지원사업 3건·전자책·수파베이스) · 최근 [결정]에 10/1 결정 2건 반영 · 플라우드는 10/1~10/2 새 녹음이 없어 노션에 새로 만든 항목 0건 (9/30 녹음의 루크 담당 Action Item은 이미 액션보드에 있음)</li>
  <li>10/3 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/2에 노션에 새로 생긴 기한 항목 9건을 일정에 추가(평생컨설팅 문의·상품소싱 시트·마진메이커·힐링디어스 본점·회식·키티티 피드백 2건·멘토루크 블로그·법인 결정) · 플라우드 10/2 녹음 4건에서 노션 새 항목 7건(소싱 멘토링 6건 + 무료 라이브 선물 준비 1건), 기한은 노트 기재값·추정이라 '확인 필요' · 최근 [결정]에 10/2 마진메이커 결정 반영 · 7일이 지난 진행 중 항목 3건은 '새 항목' 표시를 뗌</li>
  <li>10/4 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/3에 노션에 새로 생긴 기한 항목 2건을 일정에 추가(원크루 상담 리포트 링크 발송 10/4 · 재문의 확인 10/17) · 우선순위 '새 항목'에 4건 추가, 7일 지난 1건(셀수다 설치)은 일반 줄로 · 최근 [결정] 맨 위에 10/4 통합 보고 구조 · 플라우드 10/3 녹음 1건(원크루 상담)에서 노션 새 항목 0건 · 상황판 보고 피드: 어제 이후 새 보고 0건(피드의 2건은 9/30·10/1자이고 노션에 이미 완료로 있음), 막힘 0건</li>
  <li>10/5 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건(윤지영 원장 개업연월일 확인) 제거 · 10/4~10/5에 노션에 새로 생긴 기한 항목 27건을 일정에 추가(6기 무료 라이브 준비 4건 · 키티티 AI 뷰티 플랫폼 15건 · 헤메네일 5건 · 맥북 교체 · Vercel Pro 결정 · 원크루 사이트 4단계) · 우선순위 '새 항목'에서 완료 2건(카카오맵 JS키·개업연월일 확인) 빼고 새 묶음 10줄 추가 · 최근 [결정] 6개를 10/4~10/5 결정으로 교체 · 무료 라이브 날짜 10/25는 10/4 [결정]으로 확정 표시(시간·신청 링크는 확인 필요) · 플라우드 10/3 인터뷰 녹음 1건에서 노션 새 항목 0건 · 상황판: 노션 [보고] 5건 중 1건(메이크업헬퍼 AI 기술 5가지 제안)을 피드에 새로 옮김 — 나머지 4건은 클로드 코드가 이미 직접 올린 보고와 같은 일이라 그대로 둠 · 허브 맨 위에 [결정 필요] 2건(헤메네일 카카오 미등록 매장 순위 · 키티티 정부지원 방식). 피드의 '막힘' 중 키티티 도메인 구매·원크루 Supabase 한도는 뒤이은 완료 보고·노션 [결정]으로 해결된 것으로 확인돼 올리지 않음</li>
  <li>10/6 갱신: 일정에 있던 항목 중 완료로 바뀐 것 5건 제거(헤메네일 [결정 필요] 3건 — 카카오 전화번호 표시·상가정보 대조·가격 최신화 / Apps Script 권한 승인은 예약 작업으로 대체돼 불필요 / 영업 확인 목록 월간 갱신은 예약 작업으로 자동화) · 10/5에 노션에 새로 생긴 기한 항목 4건을 일정에 추가(매장 대청소 입회·검수 10/5 · 키티티 계약 10/8 · 멘토루크 파인더 네이버 쇼핑 API 종료 대응 10/31 · 원크루 라운지 첫 자료 10/31) · 우선순위 '새 항목'에 9줄 추가, 7일 지난 5건(9/28 등록분)은 일반 줄로 · 최근 [결정] 6개를 10/5 결정으로 교체 · 노션 [보고] 6건 중 새로 옮긴 것 0건('2027 정부지원사업 리스트'는 클로드 코드가 이미 직접 올린 보고와 같은 일) · 허브 맨 위 [결정 필요] 4건(10/5 '막힘' 보고 2건 추가: 키티티 AI 상담 OpenAI 키·루크 툴박스 도구 판매 조건) · 플라우드 10/4~10/6 새 녹음 없음 → 노션에 새로 만든 항목 0건</li></ul>
  <li>10/7 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건 제거(초이스토리 PD 화상 미팅) · 10/6~10/7 새벽에 노션에 새로 생긴 기한 항목 90건을 일정에 추가(법인 정리·사업장 이전 22건 · 초월스토리 강사 협업 13건 · 메이브님 공동 액션·셀수다 구독·인베이더 종료 대비·디노 리부트·창고형 매장·원크루 자료실 등) · 밤사이 다른 세션이 노션 링크 없이 넣어 둔 법인 일정 10줄은 같은 노션 항목으로 교체 · 목표가 '사업 외 개인'인 1건과 상태가 '시작 전'인 [결정] 1건은 넣지 않음 · 우선순위 '새 항목'에 32줄 추가, 9/29 등록 4건은 일반 줄로 · 최근 [결정] 6개 교체 · 플라우드 10/6 녹음 6건에서 노션 새 항목 3건 · 허브 [결정 필요]에 루크 툴박스 결제·원크루 자동 배포 2건 추가 · 유니버스 접수함 열린 이슈 0건</li>
  <li>10/8 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/7~10/8 새벽에 노션에 새로 생긴 기한 항목 23건을 일정에 추가(가을 대표님 강사 제안·런칭 준비 · 김종진 대표님 코칭 4건 · 최은봉 대표님 4건 · 사업 구조화 페이지 저장소 4건 · 지영 원장 빌드업 페이지 · 구리세무서 전화 등) · 다른 세션이 넣은 노션 링크 없는 법인 일정 11줄은 같은 일의 노션 항목으로 교체 · 우선순위 '새 항목'에 15줄 추가, 9/30 등록 16줄은 일반 줄로 · 최근 [결정]에 김종진 대표님 결정 3건 반영 · 플라우드 10/7 녹음에서 새로 만든 노션 항목 없음 · 상황판 새 '막힘' 없음, 허브에 [결정 필요] 1건(사업 구조화 페이지 저장소 만들기) 추가 · 사업 유니버스 접수 이슈 0건</li>
  <li>10/9 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건 제거(초월스토리 파일럿 강사 선정) · 법무사 항목은 노션에서 '선정·위임 10/12'로 바뀌어 기한·제목 수정 · 10/8에 노션에 새로 생긴 기한 항목 11건을 일정에 추가(힐링디어스 법인 등기 3건 10/9 · 키티티 토탈샵 2건 10/11 · 초월스토리 강사 협업 6건 10/22·10/31) · 우선순위 '새 항목'에 5줄 추가, 10/1 등록 6줄은 일반 줄로 · 최근 [결정]에 10/8 결정 2건(4분기 내부 방향 · 법무사 위임) 반영 · 플라우드 10/8 녹음 3건(토탈샵 계약)에서 새로 만든 노션 항목 없음 · 상황판: 10/8자 보고 9건 모두 완료·1차 완료, 새 '막힘' 없음 — 허브 [결정 필요] 7건 그대로 · 노션 [보고] 6건 중 새로 옮긴 것 0건 · 사업 유니버스 접수 이슈 0건</li>

  <li>10/10 갱신: 일정에 있던 항목 중 완료로 바뀐 것 2건 제거([결정] 사업목적 41개 확정 · [결정] 수권주식 200주 → 100,000주) · 노션에서 기한이 바뀐 3건 수정(변경등기 제출 10/15 → 10/16 · 한 신청서로 묶기 10/8 → 10/12 · 본점이전 등기·사업자등록 정정 10/2 → 10/15) · 10/9에 노션에 새로 생긴 기한 항목 12건을 일정에 추가(변경등기 10건 10/9·10/12·10/31 · 박종혁 본부장 협업 2건 10/14·10/16) · 플라우드 10/9 박종혁 본부장 회의 녹음에서 노션 새 항목 3건(좌석·온보딩 10/19 · 유튜브 전략 재구성 10/31 · 소싱 자동화·위탁 물류 11/30 — 기한은 모두 추정) · 우선순위 '새 항목'에 8줄 추가, 10/2 등록 12줄은 일반 줄로 · 최근 [결정]에 10/9 결정 3건(대표이사 선임 · 정관 전부개정 · 본점 이전일 10/2) 반영 · 상황판: 10/9자 보고 10건(완료 9 · 진행 중 1)과 10/10자 1건, 새 '막힘' 없음 — 허브 [결정 필요] 7건 그대로 · 노션 [보고] 6건 중 새로 옮긴 것 0건 · 사업 유니버스 접수 이슈 0건</li>
  <h3>프로젝트 기록</h3>
  <ul><li>내 연봉 10억 만들기 프로젝트의 overview · principles · ways-of-working · luke-toolbox · 3pl-service</li></ul>
</div>

<h2>갱신 방법</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">완료 체크</div><div class="m">각 항목 앞 체크박스 → 이 기기에 저장되고 줄이 그어짐. 하단 '완료 목록 복사'를 눌러 클로드 채팅에 붙여넣으면 클로드가 노션을 완료 처리하고 페이지를 다시 만들어 올림. 노션 ↗ 링크가 있는 항목은 노션에서 완료로 바꿔도 됨.</div></li>
    <li><div class="t">수동</div><div class="m">클로드에게 "10억 페이지 갱신"이라고 하면 노션·플라우드·최근 대화를 다시 읽고 파일 전체를 새로 써서 push합니다. 링크는 ?v=숫자를 올려서 공유.</div></li>
    <li><div class="t">자동</div><div class="m">매일 06:40 스케줄 작업이 노션 액션보드(완료 제거·새 기한 추가)와 플라우드 최근 2일 녹음(루크 담당 Action Item → 노션 새 항목)을 읽고 build.py 전체를 새로 써서 push합니다 (9/30 결정).</div></li>
    <li><div class="t">구조</div><div class="m">build.py 하나가 모든 index.html을 생성. CSS·JS 인라인, 외부는 구글 폰트만. 검색엔진 noindex.</div></li>
  </ul>
</div>

<h2>주의</h2>
<div class="card gold">
  <p style="font-size:14px">협력자 이름과 계획 금액이 들어 있으니 링크는 팀 내부에만 공유하세요. 수강생 소송 건은 이름을 뺐고, 건강·개인 관계 기록은 넣지 않았습니다.</p>
</div>
"""

# ---------------------------------------------------------------- 지영 설문지 발표
SURVEYTALK = """
<h1>지영 설문지 발표 — 쪽마다 할 말</h1>
<p class="note">이 페이지만 보고도 발표할 수 있게 <b>지적 원문 · 실제 문항 문구 · 고친 이유</b>를 다 넣었습니다. 흐름은 <b>① 받은 피드백 → ② 고친 것은 몇 쪽에 어떻게 → ③ 안 고친 것은 왜</b> 세 토막입니다.</p>
<div class="card accent" style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
  <div style="flex:1;min-width:0">
    <h3 style="margin:0 0 2px">전자책 (PDF 16쪽)</h3>
    <div class="note" style="margin:0">이 페이지와 같은 내용을 A4 16쪽으로. 인쇄하거나 폰에 받아 두고 보세요.</div>
  </div>
  <a class="btn pri" href="guide.pdf" style="text-decoration:none;white-space:nowrap">PDF 내려받기</a>
</div>

<div class="card accent">
  <h3>반드시 남겨야 할 한 문장</h3>
  <p style="font-size:16px;margin:6px 0 0;font-family:'Gowun Dodum',sans-serif;line-height:1.6">원척도에 원래 있던 문제는 자료 없이 손대지 않았고,<br>제 번안에서 생긴 문제는 바로 고쳤습니다.</p>
  <div class="note">③ 들어갈 때 한 번, 마무리에 한 번 — 두 번 말합니다.</div>
</div>

<h2>먼저 외울 것 <small>연구가 뭐냐고 물으면 이것만</small></h2>
<div class="card">
  <dl class="ov">
    <dt>제목</dt><dd><b>1인 헤어·메이크업 사업자의 디지털 마케팅 자기효능감이 마케팅 성과에 미치는 영향</b> : 플랫폼 활용의 매개효과 <span class="tag">가제</span></dd>
    <dt>대상</dt><dd>네이버 스마트플레이스에 등록하고, 헤어 또는 메이크업을 주 시술로 <b>혼자</b> 운영하며, <b>운영 1년 이상</b>인 사업자</dd>
    <dt>독립</dt><dd>디지털 마케팅 자기효능감 — 하위요인 2개 · <b>8문항 · 7점</b> · "~할 수 있다"</dd>
    <dt>매개</dt><dd>플랫폼 활용 — 하위요인 2개 · <b>10문항 · 5점</b> · "~하는 데 도움이 된다"</dd>
    <dt>종속</dt><dd>마케팅 성과 — 단일요인 · <b>4문항 · 5점</b> · "주변 샵과 비교해 ~가 늘었다"</dd>
    <dt>통제</dt><dd>연령대 · 샵 운영 기간 · 스마트플레이스 등록 기간 &nbsp;|&nbsp; 조절변수 없음</dd>
    <dt>AI부</dt><dd>AI 검색환경 6문항 — <b>측정 변수가 아니라 연구 배경</b>. 합산도 요인분석도 안 함</dd>
    <dt>문항</dt><dd>선별 4 + 기본 6 + 8 + 10 + 4 + 6 = <b>총 38문항</b> (선별 뺀 본 설문은 34문항)</dd>
  </dl>
  <div class="emph" style="margin-top:11px"><b>척도 출처 세 개 — 이것도 물어볼 수 있습니다</b><br>
  · 자기효능감 = Wang, Tseng, Wang &amp; Chu (2020) <b>IESES</b> 16문항 중 8문항<br>
  · 플랫폼 활용 = Tajudeen, Jaafar &amp; Ainin (2018) 13문항 중 <b>2개 하위요인 10문항</b><br>
  · 마케팅 성과 = Vorhies &amp; Morgan (2005) <b>Market Effectiveness</b> 4문항</div>
</div>

<h2>세 토막 <small>5분 기준</small></h2>
<div class="card">
  <div class="steps">
    <div><b>1:00</b>①<br>받은 피드백</div>
    <div><b>2:00</b>②<br>고친 것 8건</div>
    <div><b>1:30</b>③<br>안 고친 것 3건</div>
    <div><b>0:30</b>—<br>마무리</div>
  </div>
  <div class="warn">②는 한 건에 15초입니다. 전·후만 읽고 넘기세요. 여기서 설명을 늘리면 ③이 날아갑니다.</div>
</div>

<h2>① 받은 피드백 <small>1:00 · 2쪽</small></h2>
<div class="card">
 <div class="pg">
  <div class="pgn"><b>2</b><span>1:00</span></div>
  <div class="pgb">
   <div class="say">받은 피드백은 모두 <b>9건</b>입니다. 성격으로 묶으면 네 갈래였습니다. 처리 방식이 갈리는 것을 나눠 10개 항목으로 정리했고, 결과는 <b>8건 수정, 3건 미수정</b>입니다.</div>
  </div>
 </div>
 <div class="note" style="margin-top:12px">아래는 지적 원문입니다. 발표에서는 <b>굵은 부분만</b> 읽고 넘어가세요.</div>

 <h3 style="margin-top:12px">갈래 1 · 연구 범위 <span class="tag">1건</span></h3>
 <div class="fb">"제목은 1인 미용사업자로 넓게 표현되지만 <b>실제 대상은 헤어·메이크업 1인 사업자로 한정</b>되어 있습니다. 제목을 실제 대상에 맞게 구체화하거나 대상 범위를 조정하면 좋겠습니다."</div>

 <h3>갈래 2 · 척도 구조 <span class="tag">3건</span> <span class="tag p1">여기서 미수정 2건</span></h3>
 <div class="fb">"<b>3문항 중 한 문항이 삭제될 경우 문항 수가 부족해질 가능성</b>도 고려해 주세요."</div>
 <div class="fb">"촬영 장비 사용은 <b>파일 관리·플랫폼 기능 설정과 성격이 다를 수 있습니다.</b> 예비조사에서 하나의 요인으로 묶이는지 확인하면 좋겠습니다."</div>
 <div class="fb">"고객 응대와 고객 상담·응대 활동은 <b>유사하게 받아들여질 수 있습니다.</b> 서로 다른 하위요인에 포함되어 있으므로 예비조사에서 중복·변별성을 확인하고 표현 구분 또는 삭제 여부를 검토하면 좋겠습니다."</div>

 <h3>갈래 3 · 설문 설계 <span class="tag">2건</span> <span class="tag p1">여기서 미수정 1건</span></h3>
 <div class="fb">"<b>직원이 있거나 스마트플레이스 미등록 응답자도 끝까지 응답한 뒤 분석에서 제외된다.</b> → 설문 앞부분에 선별 문항으로 배치하고 해당 시 설문 종료"</div>
 <div class="fb">"<b>운영·등록 기간이 1년 미만인 응답자는 최근 1년의 성과 변화를 판단하기 어려울 수 있습니다.</b> 대상의 최소 운영·등록 기간을 정하거나 비교 기준 기간을 조정할지 검토하면 좋겠습니다."</div>

 <h3>갈래 4 · 문항 표현 <span class="tag">4건</span></h3>
 <div class="fb">"<b>지역 내 샵이 차지하는 비중은 응답자가 판단하기에 추상적</b>일 수 있습니다. 시장점유율이라는 원척도의 의미를 유지하면서 쉽게 이해할 수 있는 표현으로 보완할 수 있는지 검토하면 좋겠습니다."</div>
 <div class="fb">"<b>1인 샵은 매출 대부분이 단골에서 나올 수 있어 두 문항이 겹칠 수 있다.</b> → MP2를 '전체 매출', MP3를 '기존 고객 매출'로 변경"</div>
 <div class="fb">"<b>'표시된 것'(샵 이름인지 리뷰 인용인지)과 '영향'(긍정·부정 방향)이 모호하다.</b> → 표시 형태와 영향의 방향을 구체적으로 명시"</div>
 <div class="fb">"<b>'거의 없다'와 '1시간 미만'이 비슷하다.</b> → 두 구간 통합"</div>

 <div class="emph"><b>①을 닫는 한 마디</b> — "앞의 세 갈래는 대부분 고쳤고, 고치지 않은 세 건은 전부 <b>척도 구조</b>와 <b>설문 설계</b>에서 나왔습니다. 이유는 뒤에서 말씀드리겠습니다."</div>
</div>

<h2>② 고친 것 — 몇 쪽에 어떻게 <small>2:00 · 3 → 4 → 5 → 6쪽</small></h2>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>3</b><span>0:15</span></div>
  <div class="pgb">
   <h3>수정 ① 제목을 실제 대상에 맞춤</h3>
   <div class="fb">지적 — 제목은 '1인 미용사업자'인데 실제 대상은 헤어·메이크업뿐이라 네일·피부·속눈썹이 빠진다</div>
   <div class="ba2">
     <div class="b">1인 <b>미용사업자</b>의 디지털 마케팅 자기효능감이 마케팅 성과에 미치는 영향</div>
     <div class="a">1인 <b>헤어·메이크업 사업자</b>의 디지털 마케팅 자기효능감이 마케팅 성과에 미치는 영향</div>
   </div>
   <div class="why2">선생님이 주신 선택지는 둘이었습니다. 대상을 넓히거나, 제목을 고치거나. <b>넓히면 업종을 통제변수로 넣어야 해서 표본이 더 필요</b>합니다. 제목을 고치면 측정도구를 하나도 안 건드립니다. 제목 변경은 지도교수님 승인이 필요해 <b>가제</b>로 적었습니다.</div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>3</b><span>0:15</span></div>
  <div class="pgb">
   <h3>수정 ② 플랫폼 운영 3문항 → 4문항</h3>
   <div class="fb">지적 — 3문항 중 하나가 삭제되면 문항 수가 부족해진다</div>
   <div class="ba2">
     <div class="b">IESES 요인 2(기술 활용) 4문항 중 <b>3문항만 선별</b> (6·8·9번). 7번은 "미용업에 과한 기술 수준"이라며 제외했었음</div>
     <div class="a">요인 2의 <b>4문항 전체</b> 채택 (6·7·8·9번). 7번을 SE2로 되살림<br><span class="en">IESES 7번 "I can install and manipulate basic types of computer hardware to help my business"</span><br>→ "나는 샵 운영에 쓰는 기기를 설치하고 다룰 수 있다 (컴퓨터·태블릿·프린터 등)"</div>
   </div>
   <div class="why2">한 문항이 빠지면 2문항이 되어 하위요인이 성립하지 않습니다. <b>요인을 통째로 쓰면 여유가 생기고, 제가 임의로 골랐다는 지적도 함께 풀립니다.</b></div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>4</b><span>0:15</span></div>
  <div class="pgb">
   <h3>수정 ③ MP4 — 시장점유율의 비교 기준 명시</h3>
   <div class="fb">지적 — '차지하는 비중'은 응답자가 판단하기에 추상적이다</div>
   <div class="ba2">
     <div class="b">우리 지역의 비슷한 샵들 중에서 우리 샵이 차지하는 <b>비중</b>이 커졌다</div>
     <div class="a">우리 지역의 비슷한 샵들 <b>전체를 100이라고 볼 때</b>, 그중 우리 샵이 차지하는 <b>몫</b>이 커졌다<br><span style="font-size:12.5px;color:var(--muted)">(보조 설명) 우리 지역에서 헤어·메이크업을 받는 손님 전체 가운데 우리 샵에 오는 비율</span></div>
   </div>
   <div class="why2">원척도 <span class="en">"Market share growth relative to competitors"</span>의 점유율 의미는 두고, <b>무엇을 분모로 보고 답할지만 숫자로 못 박았습니다.</b> '비중'만으로는 매출 비중인지 손님 비중인지 알 수 없어 손님 기준임을 밝혔습니다.</div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>4</b><span>0:15</span></div>
  <div class="pgb">
   <h3>수정 ④ MP2·MP3 — 전체 매출과 단골 매출 구분</h3>
   <div class="fb">지적 — 1인 샵은 매출 대부분이 단골에서 나와 두 문항이 겹친다</div>
   <div class="ba2">
     <div class="b">MP2 매출이 늘었다 &nbsp;/&nbsp; MP3 단골 고객에게서 나오는 매출이 늘었다</div>
     <div class="a">MP2 <b>샵 전체 매출</b>이 늘었다 &nbsp;/&nbsp; MP3 <b>단골(기존) 고객</b>에게서 나오는 매출이 늘었다</div>
   </div>
   <div class="why2">지적대로 1인 샵은 두 값이 거의 같을 수 있습니다. 다만 <b>원척도가 두 문항으로 나눠 둔 것</b>이라 합치지 않고 수식어만 붙였습니다. 원척도도 <span class="en">"Growth in sales revenue"</span>(전체)와 <span class="en">"Increasing sales to existing customers"</span>(기존 고객)로 나눠 둡니다. 두 문항의 상관이 지나치게 높으면 예비조사에서 다시 봅니다.</div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>5</b><span>0:20</span></div>
  <div class="pgb">
   <h3>수정 ⑤ 참여 대상 확인을 맨 앞으로</h3>
   <div class="note" style="margin-top:0">다른 분들도 바로 쓸 수 있는 부분 — '공통 수정사항'으로 불릴 가능성이 큼</div>
   <div class="fb">지적 — 직원이 있거나 미등록인 분도 끝까지 응답한 뒤 분석에서 제외된다</div>
   <div class="ba2">
     <div class="b">Ⅰ부 기본사항 5번(직원 유무)·6번(등록 기간)에 섞여 있었고, 해당하지 않아도 <b>끝까지 응답한 뒤 분석에서 제외</b></div>
     <div class="a">설문 맨 앞에 <b>「참여 대상 확인」 4문항 신설</b>. 하나라도 '아니오'면 그 자리에서 종료<br>S1 주 시술이 헤어 또는 메이크업인지 · S2 혼자 운영하는지 · S3 스마트플레이스 등록 여부 · S4 운영 1년 이상인지</div>
   </div>
   <div class="why2">대상이 아닌 분이 8~10분을 쓰는 일이 없어지고, 회수하고 버리는 설문지도 줄어듭니다. Ⅰ부에서는 <b>직원 유무 문항을 삭제</b>해 7문항이 6문항이 됐습니다.</div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>5</b><span>0:15</span></div>
  <div class="pgb">
   <h3>수정 ⑥ 최소 운영 기간 1년</h3>
   <div class="fb">지적 — 운영·등록 1년 미만은 최근 1년의 성과 변화를 판단하기 어렵다</div>
   <div class="ba2">
     <div class="b">운영 기간 제한 없음. Ⅰ부 보기에 '1년 미만' 포함. Ⅳ부는 "최근 1년"을 기준으로 질문</div>
     <div class="a">선별 <b>S4에 "운영 1년 이상"</b> 추가. Ⅰ부 운영 기간 보기에서 '1년 미만' 삭제. <b>Ⅳ부의 "최근 1년" 기준은 그대로</b></div>
   </div>
   <div class="why2">두 선택지 중 <b>대상을 좁히는 쪽</b>을 골랐습니다. 비교 기간을 6개월로 줄이면 짧은 기간의 변화를 성과로 읽어야 합니다. <b>등록 기간은 안 잘랐습니다 — ③에서 설명합니다.</b></div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>6</b><span>0:15</span></div>
  <div class="pgb">
   <h3>수정 ⑦ AI2·AI6 — 묻는 대상과 방향을 분명히</h3>
   <div class="fb">지적 — '표시된 것'(샵 이름인지 리뷰 인용인지)과 '영향'(긍정·부정 방향)이 모호하다</div>
   <div class="ba2">
     <div class="b">AI2 우리 샵이 그 AI 요약에 <b>표시된 것</b>을 보신 적이 있습니까?<br>AI6 AI 요약이 우리 샵 홍보에 <b>영향을 준다</b>고 느끼십니까? → ① 전혀 그렇지 않다 ~ ⑤ 매우 그렇다</div>
     <div class="a">AI2 네이버에서 우리 지역 미용 업체를 검색했을 때, AI 요약 안에 <b>우리 샵 이름이 나온 것</b>을 보신 적이 있습니까?<br>AI6 AI 요약이 우리 샵을 알리는 데 <b>도움이 된다</b>고 느끼십니까? → ① 전혀 그렇지 않다 ~ ⑤ 매우 그렇다</div>
   </div>
   <div class="why2">AI2는 표시 형태를 <b>샵 이름 하나로 특정</b>했습니다. 리뷰 인용까지 포함하면 응답자마다 다른 걸 떠올립니다. AI6는 <b>보기가 '전혀 그렇지 않다~매우 그렇다'인데 문항이 '영향'을 물으면 부정적 영향을 받은 분은 표시할 데가 없습니다.</b> 문항과 보기의 방향을 맞춘 것입니다.</div>
  </div>
 </div>
</div>

<div class="card">
 <div class="pg">
  <div class="pgn"><b>6</b><span>0:10</span></div>
  <div class="pgb">
   <h3>수정 ⑧ 주당 홍보 시간 — 겹치는 구간 통합</h3>
   <div class="fb">지적 — '거의 없다'와 '1시간 미만'이 비슷하다</div>
   <div class="ba2">
     <div class="b">① 거의 없다 ② 1시간 미만 ③ 1~3시간 ④ 3~5시간 ⑤ 5시간 이상</div>
     <div class="a">① <b>1시간 미만</b> ② 1~3시간 ③ 3~5시간 ④ <b>5~10시간</b> ⑤ <b>10시간 이상</b></div>
   </div>
   <div class="why2">응답자가 구분할 수 없는 같은 구간이라 합쳤습니다. 비는 칸은 <b>위쪽을 쪼개는 데</b> 썼습니다 — 전업처럼 매달리는 분과 주 5시간 쓰는 분이 같은 칸에 들어가 있었습니다.</div>
  </div>
 </div>
</div>

<div class="card blue">
  <h3>②를 닫으며 한 쪽만 — 18쪽</h3>
  <div class="note" style="margin-top:4px">"앞의 수정이 실제 설문지에는 이렇게 들어갔습니다. 맨 앞 네 문항이 참여 대상 확인이고, '아니오'면 여기서 종료된다고 응답자에게 알립니다."</div>
  <dl class="skiprow" style="margin-top:9px">
    <dt>11</dt><dd>자기효능감 8문항 — 늘어난 SE2가 들어간 모습 (수정 ②)</dd>
    <dt>14</dt><dd>선별 4문항 · 일반적 특성 6문항 (수정 ⑤)</dd>
    <dt>18</dt><dd><b>실제 배포용 설문지 맨 앞</b> — '아니오 → 설문이 종료됩니다'</dd>
    <dt>21</dt><dd>Ⅳ부 마케팅 성과 · Ⅴ부 AI — 수정 ③④⑦의 최종 문항</dd>
  </dl>
</div>

<h2>③ 안 고친 것 — 왜 <small>1:30 · 이 발표의 중심</small></h2>
<div class="card gold">
  <div class="note" style="margin-top:0">들어가는 말 — "세 건은 고치지 않았습니다. <b>지적이 틀려서가 아니라, 지금 고치면 오히려 문제가 생기거나 자료 없이는 판단할 수 없어서</b>입니다."</div>
</div>

<div class="card gold">
 <div class="pg">
  <div class="pgn q"><b>7</b><span>0:35</span></div>
  <div class="pgb">
   <h3>미수정 ① 촬영 장비 문항을 분리하지 않음</h3>
   <div class="fb">지적 — "촬영 장비 사용은 파일 관리·플랫폼 기능 설정과 성격이 다를 수 있습니다."</div>
   <div class="note" style="margin-top:0"><b>문제가 된 네 문항 (Ⅱ부 플랫폼 운영 · 11쪽)</b></div>
   <dl class="skiprow" style="margin-top:6px;grid-template-columns:34px 1fr">
     <dt>SE1</dt><dd>나는 우리 샵의 사진·영상 파일을 정리하고 관리할 수 있다 <span class="en">IESES 6번</span></dd>
     <dt>SE2</dt><dd>나는 샵 운영에 쓰는 기기를 설치하고 다룰 수 있다 <span class="en">IESES 7번</span></dd>
     <dt>SE3</dt><dd><b>나는 우리 샵 홍보에 필요한 촬영 장비를 다룰 수 있다</b> <span class="en">IESES 8번 — 지적받은 문항</span></dd>
     <dt>SE4</dt><dd>나는 온라인 플랫폼의 기능을 설정하고 사용할 수 있다 <span class="en">IESES 9번</span></dd>
   </dl>
   <div class="say">맞는 지적입니다. 그런데 <b>이 네 문항은 제가 묶은 게 아니라 원척도가 '요인 2 · 기술 활용'으로 묶어 둔 것</b>입니다. 자료를 한 건도 받지 않은 상태에서 제가 먼저 쪼개면 원척도의 요인구조를 근거 없이 바꾸는 일이 됩니다. 대신 말씀대로 <b>예비조사에서 하나로 묶이는지 확인</b>하고, SE3가 떨어져 나가도 3문항이 남도록 <b>문항 수를 4개로 늘려 뒀습니다.</b></div>
  </div>
 </div>
</div>

<div class="card gold">
 <div class="pg">
  <div class="pgn q"><b>7</b><span>0:35</span></div>
  <div class="pgb">
   <h3>미수정 ② 겹치는 두 문항을 그대로 둠</h3>
   <div class="fb">지적 — "고객 응대와 고객 상담·응대 활동은 유사하게 받아들여질 수 있습니다. … 표현 구분 또는 삭제 여부를 검토하면 좋겠습니다."</div>
   <div class="note" style="margin-top:0"><b>문제가 된 두 문항 (Ⅲ부 플랫폼 활용 · 12쪽)</b></div>
   <dl class="skiprow" style="margin-top:6px;grid-template-columns:40px 1fr">
     <dt>PU4</dt><dd>고객 응대를 하는 데 도움이 된다 — <b>마케팅</b> 하위요인<br><span class="en">SMM4 "It provides aids to deliver customer services"</span></dd>
     <dt>PU7</dt><dd>고객 상담·응대 활동을 하는 데 도움이 된다 — <b>고객관계</b> 하위요인<br><span class="en">CR3 "Conduct customer service activities"</span></dd>
   </dl>
   <div class="say">이것도 맞습니다. 다만 영어 원문을 보시면 아시겠지만 <b>이 중복은 제 번안에서 생긴 게 아니라 원척도에 이미 있는 중복</b>입니다. 서로 달라 보이게 고치면 <b>원문에 없는 구분을 제가 만들어 넣는 셈</b>이고, 한쪽을 지우면 자료 없이 연구자 판단만으로 문항을 삭제하는 셈이 됩니다. 예비조사에서 <b>교차적재와 상관</b>을 보고 자료를 근거로 판단하겠습니다.</div>
   <div class="emph"><b>이 두 문장을 또박또박</b><br>· "제가 묶은 게 아니라 원척도가 묶은 것"<br>· "번안에서 생긴 게 아니라 원척도에 있는 중복"</div>
  </div>
 </div>
</div>

<div class="card gold">
 <div class="pg">
  <div class="pgn q"><b>8</b><span>0:20</span></div>
  <div class="pgb">
   <h3>미수정 ③ 등록 기간은 자르지 않음</h3>
   <div class="fb">지적 — "대상의 최소 운영·등록 기간을 정하거나 비교 기준 기간을 조정할지 검토하면 좋겠습니다." (운영 기간만 반영)</div>
   <div class="say">운영 기간은 1년 이상으로 잘랐지만 등록 기간은 안 잘랐습니다. 등록까지 1년으로 묶으면 <b>스마트플레이스를 최근에 시작한 분들이 빠지는데, 이 연구가 보려는 변화를 가장 크게 겪는 집단</b>입니다. 대신 등록 기간은 Ⅰ부에서 받아 <b>통제변수로</b> 넣습니다. <b>잘라내는 것보다 통계적으로 통제하는 쪽이 정보를 덜 잃습니다.</b></div>
   <div class="why2">다만 등록 6개월 미만이 많이 모이면 매개변수와 성과의 시간 순서가 어긋날 수 있어, <b>예비조사에서 등록 기간 분포를 보고 다시 여쭙겠다</b>고 문서에 적어 뒀습니다.</div>
  </div>
 </div>
</div>

<h2>마무리 <small>0:30 · 9쪽</small></h2>
<div class="card">
 <div class="pg">
  <div class="pgn"><b>9</b><span>0:30</span></div>
  <div class="pgb">
   <h3>사실 확인이 남은 것 + 판단 기준</h3>
   <div class="note" style="margin-top:0">9쪽에 '확인한 것'과 '추정이라 확인이 남은 것'을 두 표로 나눠 뒀습니다</div>
   <dl class="skiprow" style="margin-top:7px;grid-template-columns:18px 1fr">
     <dt>·</dt><dd>네일·피부까지 넓히면 시술 단가·재방문 주기가 다르다 → 업종별 통계로 확인</dd>
     <dt>·</dt><dd>1인 샵은 전체 매출과 단골 매출이 거의 같다 → 예비조사 상관계수로 확인</dd>
     <dt>·</dt><dd>운영 1년이면 '최근 1년' 상대 비교에 답할 수 있다 → 예비조사 무응답 패턴으로 확인</dd>
     <dt>·</dt><dd><b>IESES 신뢰도 α=.94는 적응 연구가 인용한 수치</b> → Wang 외(2020) 원문 대조 필요</dd>
   </dl>
   <div class="say">마지막으로, 제가 추정으로 적은 네 가지는 따로 표로 뺐습니다. 예를 들어 자기효능감 척도의 신뢰도는 <b>원 개발 논문을 직접 못 보고 적응 연구가 인용한 수치를 본 것</b>이라, 본문에 쓰지 않고 '확인 필요'로만 남겼습니다.<br><br>
   정리하면 기준은 하나였습니다. <b>원척도에 원래 있던 건 자료 없이 손대지 않았고, 제 번안에서 생긴 건 바로 고쳤습니다.</b></div>
  </div>
 </div>
</div>

<h2>넘기는 쪽 <small>질문 오면 펼칠 위치</small></h2>
<div class="card">
  <dl class="skiprow">
    <dt>1</dt><dd>표지</dd>
    <dt>10</dt><dd><b>연구 개요·연구모형</b> — "연구가 뭐냐" 질문</dd>
    <dt>12</dt><dd><b>플랫폼 활용 10문항 + 영어 원문</b> — "척도 원문 봤냐" 질문</dd>
    <dt>13</dt><dd>마케팅 성과 4문항 · AI 6문항 (설명부)</dd>
    <dt>15</dt><dd><b>참고문헌 · 지도교수님께 여쭐 것</b> — 교수님 질문 대부분이 여기로 받힘</dd>
    <dt>16</dt><dd>부록 간지</dd>
    <dt>17</dt><dd>설문 안내문</dd>
    <dt>19</dt><dd>Ⅱ부 자신감 8문항 (7점)</dd>
    <dt>20</dt><dd>Ⅲ부 플랫폼 활용 10문항 (5점)</dd>
  </dl>
</div>

<h2>나올 만한 질문 일곱</h2>
<details class="qa"><summary>제목 바꾸는 건 지도교수님께 말씀드렸나요?</summary>
<div class="a">아직입니다. <b>가제로 표기</b>했고 <b>15쪽</b> '여쭐 것' 1번에 올려 뒀습니다. 승인이 안 나면 되돌리면 되고, 측정도구는 그대로라 되돌려도 설문지는 안 바뀝니다.</div></details>

<details class="qa"><summary>겹친다는 그 두 문항, 그냥 하나 지우면 되지 않나요?</summary>
<div class="a"><b>7쪽.</b> 원척도 단계의 중복입니다(<span class="en">SMM4 "It provides aids to deliver customer services"</span> / <span class="en">CR3 "Conduct customer service activities"</span>). 자료 없이 제 판단만으로 지우면 다른 문항도 같은 논리로 지울 수 있게 됩니다. 예비조사에서 <b>교차적재와 상관</b>을 보고 지우겠습니다.</div></details>

<details class="qa"><summary>문항이 38개면 너무 많지 않나요?</summary>
<div class="a">선별 4문항을 빼면 <b>본 설문은 34문항</b>이고, 선별에서 걸리는 분은 4문항에서 끝납니다. 그래도 많다고 보시면 <b>Ⅴ부 AI 6문항을 줄이는 안</b>을 15쪽에 적어 뒀습니다. AI부는 측정 변수가 아니라 연구 배경이라 줄여도 모형에 영향이 없습니다.</div></details>

<details class="qa"><summary>운영 1년 이상으로 자르면 표본이 모이나요?</summary>
<div class="a">표본이 줄어드는 건 맞습니다. 다만 성과를 '최근 1년'으로 묻기 때문에 맞춘 것입니다. 비교 기간을 6개월로 줄이는 쪽도 있었지만 <b>측정도구에 손을 덜 대는 쪽</b>을 골랐습니다. 이 맞바꿈도 15쪽 여쭐 것 2번에 올려 뒀습니다.</div></details>

<details class="qa"><summary>척도 원문은 어디서 확인했나요?</summary>
<div class="a"><b>12쪽</b>에 문항마다 영어 원문을 나란히 실었습니다. 플랫폼 활용 13문항은 <b>Qalati 외(2021) <i>Sustainability</i> 13(1), 75의 Appendix A</b>, 자기효능감 16문항은 <b>Torres-Miranda 외(2024) <i>Frontiers in Education</i> 9:1370490 TABLE 1</b>에서 봤습니다. <b>원 개발 논문(Wang 외, 2020)은 아직 못 봐서 9쪽에 '확인 필요'로 적어 뒀습니다.</b></div></details>

<details class="qa"><summary>독립변수와 매개변수가 겹치지 않나요?</summary>
<div class="a">Ⅱ부는 <b>"~할 수 있다"</b>(할 수 있다고 믿는 정도, 7점), Ⅲ부는 <b>"~하는 데 도움이 된다"</b>(플랫폼을 어떤 목적에 쓰는지, 5점)입니다. 묻는 대상도 응답 보기도 다릅니다. 예비조사에서 <b>판별타당도</b>로 확인합니다.</div></details>

<details class="qa"><summary>AI 문항은 변수인가요?</summary>
<div class="a">아닙니다. <b>연구 배경</b>이라 하나의 점수로 합산하지 않고 요인분석·신뢰도분석도 하지 않습니다. 빈도와 백분율로 표본 특성만 기술하고, <b>통제변수로도 조절변수로도 넣지 않습니다.</b></div></details>

<h2>3분으로 줄여야 하면</h2>
<div class="card blue">
  <div class="steps">
    <div><b>0:30</b>①<br>네 갈래</div>
    <div><b>1:00</b>②<br>5쪽만</div>
    <div><b>1:10</b>③<br>7·8쪽</div>
    <div><b>0:20</b>마무리</div>
  </div>
  <div class="note">②에서는 <b>5쪽(선별문항)</b> 하나만 펴고 나머지 일곱 건은 "표현을 분명히 하거나 보기를 정리한 것들"로 묶어 한 문장에 넘깁니다. ③은 어떤 경우에도 줄이지 않습니다.</div>
</div>

<h2>발표 직전 점검</h2>
<div class="card">
  <ul class="list">
    <li>넘길 순서 외우기 — <b>2 → 3 → 4 → 5 → 6 → 18 → 7 → 8 → 9</b></li>
    <li>15쪽(여쭐 것)은 질문용으로 따로 열어 두기</li>
    <li>②는 한 건 15초 — 전·후만 읽고 넘기기</li>
    <li>숫자 세 개 — <b>피드백 9건 · 수정 8 · 미수정 3</b></li>
    <li>③ 들어갈 때와 마무리에 같은 문장 — "원척도에 있던 건 손대지 않았고, 제 번안에서 생긴 건 고쳤습니다"</li>
  </ul>
</div>

<div class="src">
  <b>근거</b>
  <ul>
    <li>지적 원문·문항 문구·쪽 번호는 「윤지영_1인 헤어·메이크업 사업자의 디지털 마케팅 자기효능감이 마케팅 성과에 미치는 영향_설문지 수정본.pdf」 21쪽 본문에서 그대로 옮김</li>
    <li>발표 시간(5분)은 수업 공지에 없어 <b>확인 필요</b> — 배분은 5분 가정값이고, 실제 시간이 다르면 비율만 유지하면 됩니다</li>
    <li>교수님 공지 원문: "토요일 수업에서는 제출한 내용을 바탕으로 공통적인 수정사항과 판단 기준을 함께 살펴보겠습니다."</li>
  </ul>
</div>
"""

def write(path, html):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    write(os.path.join(base, "index.html"), page("홈", INDEX, root="./"))
    write(os.path.join(base, "roadmap", "index.html"), page("돈 버는 로드맵", ROADMAP))
    write(os.path.join(base, "priority", "index.html"), page("우선순위", PRIORITY))
    write(os.path.join(base, "people", "index.html"), page("사람별 현황", PEOPLE))
    write(os.path.join(base, "schedule", "index.html"), page("일정 도식", SCHEDULE))
    write(os.path.join(base, "invader", "index.html"), page("인베이더 종료 대비", INVADER))
    write(os.path.join(base, "maven", "index.html"), page("메이브님 공동 액션 플랜", MAVEN))
    write(os.path.join(base, "chowol", "index.html"), page("초월스토리 강사 협업", CHOWOL))
    write(os.path.join(base, "pilot", "index.html"), page("파일럿 강사 결정", PILOT))
    write(os.path.join(base, "relocation", "index.html"), page("10/15 등기 — 등기부 확인 끝", RELOCATION))
    write(os.path.join(base, "iros", "index.html"), page("등기부 열람 — 클릭 순서", IROS))
    write(os.path.join(base, "registry-prep", "index.html"), page("등기 변경 — 준비물 체크리스트", PREP))
    write(os.path.join(base, "registry-forms", "index.html"), page("등기 서류 — 다 만들어 뒀습니다", FORMS))
    write(os.path.join(base, "park", "index.html"), page("박종혁 본부장 협업 — 평가", PARK))
    write(os.path.join(base, "vault", "index.html"), page("셀프 등기 · 정관 찾기 · 서류 보관", VAULT))
    write(os.path.join(base, "jiyoung-prompt", "index.html"), page("지영 원장 빌드업 페이지 — 프롬프트", JYPROMPT))
    write(os.path.join(base, "jiyoung-survey", "index.html"), page("지영 설문지 발표 — 쪽마다 할 말", SURVEYTALK))
    write(os.path.join(base, "crew-prompt", "index.html"), page("크루원 사업 구조화 페이지 — 프롬프트", CREWPROMPT))
    write(os.path.join(base, "credit", "index.html"), page("신용점수 — KCB 622 / NICE 750", CREDIT))
    write(os.path.join(base, "money", "index.html"), page("재정 정리 — 무엇부터 털어야 하나", MONEY))
    write(os.path.join(base, "corp", "index.html"), page("힐링디어스 → 셀러들의 수다", CORP))
    write(os.path.join(base, "universe", "index.html"), page("사업 유니버스", universe_html()))
    write(os.path.join(base, "philosophy", "index.html"), page("삼각 파이프라인", PHILOSOPHY))
    write(os.path.join(base, "platform", "index.html"), page("강의 플랫폼 전략", PLATFORM))
    write(os.path.join(base, "guides", "index.html"), page("할 일 설명서", guide_index_html()))
    write(os.path.join(base, "grants", "index.html"), page("정부지원사업", GRANTS))
    write(os.path.join(base, "status", "index.html"), page("상황판", STATUS))
    for g in GUIDES:
        write(os.path.join(base, "guides", g["slug"], "index.html"), page(g["title"], guide_page_html(g), root="../../"))
    write(os.path.join(base, "sources", "index.html"), page("출처·갱신 방법", SOURCES))
    print("built", UPDATED)

if __name__ == "__main__":
    main()
