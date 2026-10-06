# -*- coding: utf-8 -*-
"""내 연봉 10억 만들기 — 정적 페이지 빌드 스크립트.
python3 build.py 실행 시 index.html 과 하위 폴더 index.html 을 전부 새로 씁니다.
(부분 수정 금지 원칙: 매번 파일 전체를 다시 생성)"""
import json, os, datetime

UPDATED = "2026-10-07"
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
  {"d":"2026-10-02","t":"힐링디어스(주) 본점 주소 확보 + 본점이전 등기·사업자등록 정정 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481a7b0c0cfc85f4b3475","cash":False},
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
  {"d":"2026-10-05","t":"초이스토리 PD 화상 미팅 — 강의 플랫폼 모객 축 제안 (3자 구도) [설명서]","who":"루크·메이브님","p":"P0","g":"platform-pd-meeting","n":"https://app.notion.com/p/3eb0cf8fea04818c9bf6fda871eb645b","cash":True},
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
  {"d":"2026-10-06","t":"배수진(돈 걸고 목표달성 앱) 프로토타입 검토","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea0481af8112d35bc3c0e23b","cash":True},
  {"d":"2026-10-06","t":"박태경 대표님 빠른 거절·통보 기준 문서화 (예: 2시간 내 판단 룰)","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481989321faefe3f4f605","cash":True},
  {"d":"2026-10-06","t":"물류 CS 포인트 분석 + 사전 안내 스크립트 정비","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"박태경 대표님 5회차 준비 — 10월 첫 주 점검표 10개 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481eda67cda9ab46ad130","cash":True},
  {"d":"2026-10-07","t":"정○○ 대표님(원크루) 다음 컨설팅 — 매일 결산·금요일 상품 정리 점검","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481ea947cc6042c5ad37e","cash":True},
  {"d":"2026-10-07","t":"최은봉 대표님 1주 팔로업 — 10/1 당근 올리고 바로 광고, 10/3·5·6 플랫폼 가입 확인 (17:00 카톡)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea048161b042f4bf4fb3da5b","cash":True},
  {"d":"2026-10-07","t":"박태경 대표님 백문백답·4회차 교육자료 재확인·공유","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481fd8c72c6256ae03466","cash":True},
  {"d":"2026-10-07","t":"뷰셀 2화 공개 (수)","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-10-07","t":"스마트스토어 발송·지연·취소 카톡/문자 자동 알림 방법 조사","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea04815b9851f87faf14fae1","cash":False},
  {"d":"2026-10-08","t":"세무사 통화 — 최근 2년 수입금액 0인지 먼저 확인 (매출 있으면 휴면법인 논의 종료)","who":"루크","p":"P0","cash":True},
  {"d":"2026-10-09","t":"세무사 통화 — 임원 추가선임이 '50% 교체'인지, 3PL 창고가 중과 제외 업종인지","who":"루크","p":"P0","cash":True},
  {"d":"2026-10-09","t":"법무사 — 본점이전·상호변경·사업목적 추가(교육·물류·부동산임대업)를 한 신청서로 묶을 수 있는지","who":"루크","p":"P0","cash":False},
  {"d":"2027-03-16","t":"서울 꼬마빌딩 잔금은 이날 이후로 — 힐링디어스 설립 5년 충족일 (경기 외곽 창고형 매장은 권역 밖이면 해당 없음)","who":"루크","p":"P1","cash":True},
  {"d":"2027-03-16","t":"[참고] 힐링디어스 설립 5년 충족 — 이날 이후 취득해야 과밀억제권역 부동산 취득세 중과 없음","who":"루크","p":"P1","cash":True},
  {"d":"2026-10-15","t":"본점이전등기 접수 — 10/1 이전, 상법 2주 기한 마지막 날","who":"루크","p":"P0","cash":False},
  {"d":"2026-10-08","t":"정관 확인 — 본점 조항이 '경기도 구리시'까지인지, 임기·공고방법 조항","who":"루크","p":"P0","cash":False},
  {"d":"2026-10-16","t":"사업자등록 정정신고 — 등기 완료 직후 (사업자등록증·정정신고서·임대차계약서)","who":"루크","p":"P0","cash":False},
  {"d":"2026-10-07","t":"뿌요 짠테크 유튜브 3화 '연쇄적금러' 대본 작성","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea04818f9d6fdd1b114a853e","cash":False},
  {"d":"2026-10-07","t":"물류 권한 재설계 + 감사 로그","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"지영 예약·매출 간단 대시보드 완료 목표","who":"지영","p":"P2","cash":False},
  {"d":"2026-10-08","t":"종혁 본부장 미팅 — 락인 축(챌린지·카페·광고) 역할과 1:1:1 배분안 제시 [설명서]","who":"루크·메이브님","p":"P0","g":"platform-director-meeting","n":"https://app.notion.com/p/3eb0cf8fea04816b8d8ee9e56061c6d0","cash":True},
  {"d":"2026-10-08","t":"최은봉 대표님 미팅 14:00 — 당근 광고 중간 결과 화면 리뷰 (노션은 10/8, 녹음은 '수요일'=10/7 · 날짜 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04814c922bc0af3fa5ab4f","cash":True},
  {"d":"2026-10-08","t":"키티티 계약 — 10/8(목) (계약 종류·시간·장소 미정 · 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f00cf8fea0481a89260d919b12e75c3","cash":True},
  {"d":"2026-10-08","t":"키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체","who":"루크","p":"P0","n":"https://app.notion.com/p/3ec0cf8fea0481698468f35e62d2e19b","cash":False},
  {"d":"2026-10-08","t":"배송비 포함 총액 계산 시트 템플릿 배포 (10/2 멘토링 수강생용)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481a4837dc07d4eeaa7a7","cash":True},
  {"d":"2026-10-08","t":"지영 미팅 — 정부지원사업 후보 3개 + 사업계획서 초안 리뷰","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-08","t":"정부지원사업 맞춰 보기 사이트 「되는 지원사업 찾기」 구축 (클로드 코드)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ec0cf8fea048151a8acff9e6bbd0442","cash":False},
  {"d":"2026-10-08","t":"사진 기반 입고/검수 자동화 플로우 설계","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-09","t":"소싱 선별 기준표 작성 — 카탈로그 최저가순·총액 확인·리뷰 10개 이상·수량/용량 오류 점검","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481759627c752b5187600","cash":True},
  {"d":"2026-10-09","t":"키티티 원장님께 /admin 노트 사용법 전달 + 시술 방향 검토·피드백 받기 (습도·채광·장소·이동시간)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea04810b808df66fdd4ed562","cash":False},
  {"d":"2026-10-09","t":"키티티 /guide 내용 원장님 피드백 받기 (상담 12항목·데일리/촬영 기준·O/X 표·계절 색)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481839ab5c4f4a80c7caf","cash":False},
  {"d":"2026-10-10","t":"멘토루크 블로그 — 블로그 프로그램을 개인 브랜딩(케어 이야기 중심)으로 독립 분기 1차 전환 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481bc8287dc9e35045f45","cash":False},
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
  {"d":"2026-10-11","t":"인베이더 무료강의 라이브 PPT 제작","who":"루크","p":"P0","n":"https://app.notion.com/p/3ee0cf8fea04810e9f65d1802510734f","cash":False},
  {"d":"2026-10-11","t":"키티티 인스타·플레이스·매장 QR에 진단 링크 걸고 홍보 → 파트너샵 마케팅 키트 1판","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea0481c794b3ef4cc6242f2c","cash":False},
  {"d":"2026-10-11","t":"키티티 무료강의 ①② 제작 + 셀프메이크업 무료 PDF + 저가 VOD 5강 촬영","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea04813c88c1e7123b988adc","cash":False},
  {"d":"2026-10-12","t":"소액 테스트 프로토콜 문서화 — 초기 발주·리뷰 기준·가격 허용 범위·손절 조건","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea048178a51dcac4eccc0be0","cash":True},
  {"d":"2026-10-15","t":"블로그·인스타 자동화 프로그램 → '오프라인샵 팩'으로 정리 + 면책 화면 추가","who":"루크","p":"P1","n":"https://app.notion.com/p/3db0cf8fea0481d18720f2201f82b3b3","cash":True},
  {"d":"2026-10-15","t":"지영 내년 조달(최소 1억) 월별 마일스톤 확정","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-15","t":"미입고 자동 알림·반품 트리거 프로토타입","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-15","t":"[보류] 10월 정산 확인 전까지 하지 않을 것 — 재검토일","who":"루크","p":"P3","n":"https://app.notion.com/p/3d50cf8fea0481ae9cbdc532f42c5b95","cash":False},
  {"d":"2026-10-16","t":"미니쌤 채널 공지 3회 (2·4·8주차: 10/12주, 10/26주, 11/23주) — 카톡·카페·유튜브","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea0481dc8e86ef413c4e23c8","cash":False},
  {"d":"2026-10-17","t":"홍○○ 대표님 원크루 재문의 여부 확인 (10/3 상담 후속)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ee0cf8fea0481b58bcec3ba614eec0f","cash":True},
  {"d":"2026-10-18","t":"키티티 무료강의 라이브 → 저가 VOD 판매 오픈 + 개인 레슨 네이버 예약 등록","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea0481dc8934dc0c61d42b94","cash":True},
  {"d":"2026-10-20","t":"당근 2주 결과 판정 — 지속/수정/이동 답장 (최은봉 대표님)","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481eabc25d08c7f5019f3","cash":True},
  {"d":"2026-10-24","t":"무료 라이브 특강 참석자 선물 준비 — 소싱처 전자책 + 자동 등록 프로그램 7일 이용권 (기한 추정 · 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481ab9090e503641c10b6","cash":False},
  {"d":"2026-10-25","t":"6기 무료 라이브 특강 당일 — 날짜는 10/4 노션 [결정]으로 확정 (시간 19:00는 10/2 녹음 언급값 · 신청 링크 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea048171ac6bd0e23e1c5669","cash":False},
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
  {"d":"2026-10-31","t":"뷰셀 회차 주제 후보 22개 — 순서 확정과 확인 필요 수치 검증","who":"루크","p":"P1","n":"https://app.notion.com/p/3eb0cf8fea0481e084eac0131859e2ca","cash":False},
  {"d":"2026-10-31","t":"설치 가이드·원격 지원 체계 마련 (AI 스튜디오)","who":"루나","p":"P1","n":"https://app.notion.com/p/3db0cf8fea048160983ee84dfa106f34","cash":False},
  {"d":"2026-10-31","t":"런칭 광고 테스트 3회 (총 350만) — 300만 툴킷 프로그램","who":"루크","p":"P1","n":"https://app.notion.com/p/3db0cf8fea04811b920ed934eddfadd5","cash":False},
  {"d":"2026-10-31","t":"헤메네일 가격비교 → AI 진단 링크 연결 (보조 송객 채널)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048134b9ede80fe9d7ed0f","cash":False},
  {"d":"2026-10-31","t":"업무용 맥북 교체 (중고 M4 맥북에어 16GB 검토, M1 에어는 중고 판매)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04817bba04cb14d260f50f","cash":False},
  {"d":"2026-10-31","t":"Vercel 팀을 Pro($20/월)로 바꿀지 결정 — 무료(Hobby)는 비상업 전용인데 공방 유료 결제 운영 중","who":"담당 미기재","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481ab90bcfc0684789878","cash":False},
  {"d":"2026-10-31","t":"원크루 사이트 4단계 — 로그인·가입 + 원크루 회원 표 + 회원 넣기/빼기 관리자 화면","who":"담당 미기재","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048181a121fa70732b2b17","cash":False},
  {"d":"2026-10-31","t":"멘토루크 파인더 — 네이버 쇼핑 검색 API 종료(2026-07-31) 대응","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481deb27cffcc5b9737ca","cash":False},
  {"d":"2026-10-31","t":"원크루 라운지에 처음 열어 둘 자료 하나 정하기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f00cf8fea0481aea406c7180d0e367b","cash":False},
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
  {"d":"2026-11-30","t":"메이크업헬퍼 12주 테스트 9주차 판정 (11월 말)","who":"루크·최은봉","p":"P1","cash":True},
  {"d":"2026-11-30","t":"트리플 루프 빈 칸 설계 — 지영 채널 자체 수익(협찬·광고) + 실물 제품 유통 아이템","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea0481dd8721d7c5260db6d1","cash":True},
  {"d":"2026-11-30","t":"내년 초 서울 이전·건물 매입 대비 사업 로드맵 수립 (기한 추정 · 확인 필요)","who":"루크","p":"P2","n":"https://app.notion.com/p/3eb0cf8fea048126844ad335f1aefd2e","cash":True},
  {"d":"2026-11-30","t":"힐링디어스(주) 업력·매출 기준 2027 정부지원사업(초창패·디딤돌·도약패키지) 지원 가능 여부 확인","who":"루크","p":"P2","n":"https://app.notion.com/p/3ec0cf8fea04810e84d3e7ceb43c766d","cash":True},
  {"d":"2026-11-30","t":"사업자 실행 관리 웹앱(PWA) 1차 — 11월 착수","who":"루크","p":"P2","n":"https://app.notion.com/p/3db0cf8fea0481349f2adefbadef023c","cash":False},
  {"d":"2026-11-30","t":"[결정 필요] 헤메네일 카카오 로컬 API로 추천 1~3위 업종 실시간 대조 — 표시만 vs 순위 반영","who":"루크","p":"P2","n":"https://app.notion.com/p/3ee0cf8fea048171ad3ef13b0f780e44","cash":False},
  {"d":"2026-12-10","t":"뿌요 90일 결산 상담 — 300만 달성 여부·거취 결정","who":"루크","p":"P3","n":"https://app.notion.com/p/3d80cf8fea0481d69c3de62608ad02ac","cash":True},
  {"d":"2026-12-31","t":"루크 툴박스 구독 500명 목표 / 3PL 판매 실적 정리(내년 강의 증거)","who":"루크","p":"P1","cash":True},
  {"d":"2026-12-31","t":"회사 자체 강의 기획 (3PL 판매 실적 연계)","who":"루크","p":"P2","n":"https://app.notion.com/p/3de0cf8fea0481b9821dc015183213b4","cash":True},
  {"d":"2026-12-31","t":"초창패 PSST 계획서 초안 12월 안에 완료","who":"루크","p":"P2","n":"https://app.notion.com/p/3ef0cf8fea0481859a20e212db58d884","cash":True},
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
    <li data-n="https://app.notion.com/p/3f00cf8fea04818a937efb1274c10b22"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 키티티 AI 상담 — GPT 연결용 OpenAI API 키 발급(루크) · 원장님께 상담 정책 10가지 답 받기</div><div class="m">10/5 상황판 '막힘' 보고(상담실장 페르소나·가상 손님 9명 시험) · ChatGPT 구독과 API 키는 별개 — 키만 넣으면 연결되도록 코드는 준비됨(실제 호출은 미확인) · 정책 10가지: 소요 시간·2인 예약·할인·출장·결제·아기 동반·헬퍼/환복·토요일 오후·본식 업스타일·클래스 · <a href="status/?p=키티티 상담 사이트">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048144b71af1d096a2f0a2"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 루크 툴박스 — 자동화 도구 판매 조건(환불 기준·설치 대수·윈도우/맥·네이버 계정 처리·결제 방식) · 원크루 페이지 결정 5가지 + 루크 사진·영상</div><div class="m">10/5 상황판 '막힘' 보고(도구 구매 검토 회의) · 도구가 눈에 안 보임 1.6/5, 99만원 이상 구매 의향 2명(조건부) · 원크루 페이지 결정 5가지: 2명 고정·안심 문구·빚 문구·평생 범위·계산기 3년 · 도구 1단계(준비 중 표시 정리·로그인 전 상세)는 클로드가 바로 가능 · <a href="status/?p=루크 툴박스">상황판</a></div></li>
    <li><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 헤메네일 — 카카오 지도에 없는 매장을 순위에 소폭 반영할지</div><div class="m">10/4 상황판 '막힘' 보고(폐업 의심 매장 순위 내리기) · 함께 물었던 상가(상권)정보 대조·전화번호 표시·가격 최신화는 10/5 노션에서 완료 처리됨 · 이 건은 결정 기록이 없어 확인 필요 · <a href="status/?p=헤메네일">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048141a4aee0ab6b56da87"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 키티티 정부지원 — 초창패 본선 + 모두의 창업 보험으로 갈지 · 이종 사업자 등록 방식(업종 추가 vs 새 사업자)</div><div class="m">10/4 노션 [보고] '정부지원 전략 v13' 메모의 '[막힘] 루크 결정 필요' (노션 상태는 완료) · 다음: 창업진흥원 1357·세무사 확인, 트랙(일반/기술 vs 로컬) 결정 · <a href="reports/kititi-grant-strategy/?v=13">보고서</a></div></li>
    <li data-g="developer-accounts"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 (Apple · Google Play · Microsoft)</div><div class="m">툴박스·영상공장·블로그타이퍼를 폰·맥·윈도우로 배포하는 모든 일의 앞단. Apple은 승인에 며칠 걸림 · 기한 10/2 지남(노션 미완료)</div></li>
    <li data-g="platform-pd-meeting"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 3자 구도 — PD 미팅(기한 10/5 지남 · 노션 미완료) → 10/8 본부장 미팅</div><div class="m">플레이어·강사교육 = 루크·메이브님 / 락인(챌린지 영상·네이버 카페·광고) = 종혁 본부장 / 모객 = 초이스토리 PD · <a href="platform/">전략 페이지</a></div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea0481a89260d919b12e75c3"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">키티티 계약 — 10/8(목)</div><div class="m">10/5 노션 등록 · 계약 종류·시간·장소는 아직 미정 — <b>확인 필요</b> · 준비물: 신분증·도장, 서류 재확인, 계약서 사진 보관</div></li>
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
  <a href="iros/"><b>등기부 열람 — 클릭 순서</b><span>인터넷등기소에서 중임 기록 확인하기 (700원)</span></a>
  <a href="pilot/"><b>파일럿 강사 결정</b><span>가을 대표님 vs 뿌요 — 같은 기준으로 비교</span></a>
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
<p class="note">기준: 현금에 가깝고 다른 일의 선행 조건일수록 위. 기한은 노션 액션보드 기준. [결정]은 완료로, [보류]는 P3로. <span class="tag">새 항목</span>은 최근 7일(9/29~) 안에 노션에 생긴 미완료 항목입니다.</p>

<h2>P0 · 이번 주 <small>~10/11</small></h2>
<div class="card red">
  <ul class="list tasks">
    <li data-g="developer-accounts"><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 — Apple Developer / Google Play / Microsoft Store</div><div class="m">기한 10/2 지남(노션 미완료) · 앱 배포(툴박스 PWA→앱, 영상공장, 블로그타이퍼) 전부의 앞단. 루크가 "제일 높은 등급"으로 지정(9/30)</div></li>
    <li data-g="platform-pd-meeting"><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 3자 구도 — 초이스토리 PD 미팅(모객, 기한 10/5) → 10/8 종혁 본부장(락인)</div><div class="m">PD 미팅 기한 10/5 지남(노션 미완료) · <a href="../platform/">전략 페이지</a> · 나머지 우선순위는 이 둘의 결과에 따라 달라짐(루크 9/30)</div></li>
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
__NEW_P3__
  </ul>
</div>

<h2>최근 [결정] <small>노션 완료 항목 중 최신 6개</small></h2>
<div class="card accent">
  <ul class="list">
    <li><span class="tag done">결정</span><div class="t">원크루 회원 공간 이름 = '원크루 라운지' — 루크가 전용관·라운지 둘 다 제안, 라운지로 진행(최종 확정은 아님 · 코드 한 줄로 바꿀 수 있음) (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">원크루 사이트 = 원크루 회원이 쓰는 곳 — 대문은 '회원이 들어가는 문'(가입 홍보 아님), 가끔 무료 자료 공개로 호기심 (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">네이버 화면 보기 스킬 직접 제작 (naver-view) (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">원크루 입구는 '대문' — 팔지 않고 '합류하려면 어떻게 해야 하지?' 느낌만 (첫 화면 버튼·고정 버튼 없음) (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">원크루 사이트 얼굴 = 젠틀몬스터 느낌 (흑백 갤러리 톤, 큰 ONE CREW 워드마크, 화면 가득한 자연광 사진) (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">원크루 사이트는 공방(거인의 도구 공방) Supabase를 같이 씀 — 원크루 표시로 입구에서 막고, 두 사이트 회원 통로는 만들지 않음 (10/5)</div></li>
  </ul>
</div>
"""

# 최근 7일(9/29~) 안에 노션 액션보드에 새로 생긴 미완료 항목 — 우선순위 페이지 각 P 구간 끝에 붙는다.
# (할 일, 메모, 노션 url 또는 "", 현금 여부). 기존 줄에 이미 있는 항목은 넣지 않음.
_N = "https://app.notion.com/p/"
NEW_ITEMS = {
 "P0": [
  ("키티티 AI 스타일 미리보기(/try) 구축", "기한 10/4 · 진행 중 · 무료 1회·워터마크·유료 원본 다운로드", _N+"3eb0cf8fea04812b8f86e2d58503588d", True),
  ("최은봉 대표님(메이크업헬퍼) — PDF 재전송·9/30 리포트(10/1) → 1주 팔로업(10/7) → 당근 중간 결과 리뷰 미팅(14:00)", "미팅일: 노션 10/8, 녹음은 '수요일 14:00'(=10/7) — 날짜 확인 필요", _N+"3eb0cf8fea0481b8be99d8ebff105a1b", True),
  ("박태경 대표님 — 사입 재고 스프레드시트(10/2) · 상품·가격 체크리스트(10/4) · 5회차 준비(10/7)", "9/30 원크루 세션 Action Item", _N+"3eb0cf8fea0481029429c45d9b6bfe47", True),
  ("정○○ 대표님(원크루) 다음 컨설팅 — 매일 결산·금요일 상품 정리 점검", "기한 10/7", _N+"3eb0cf8fea0481ea947cc6042c5ad37e", True),
  ("수강생 컨설팅 후속 — 소장 대응 결정·리셀 정리·브랜드 재점검 (익명)", "기한 9/30 · 노션 '진행 중'", _N+"3eb0cf8fea0481b1af7ac611bcbe1835", True),
  ("키티티 '연봉 10억 만들기' 페이지 배포 (저장소 kititi-1b)", "기한 10/4 · 진행 중", _N+"3eb0cf8fea04814187b8c258b3a2d38e", True),
  ("최저가 찾기 소싱 프로그램 새 버전 공개", "기한 10/4 · 진행 중", _N+"3eb0cf8fea04817fa0caf144b0c513ee", False),
  ("키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체", "기한 10/8 · 진행 중 (10/1 등록)", _N+"3ec0cf8fea0481698468f35e62d2e19b", False),
  ("평생컨설팅 문의(뷰셀 수강생·쿠팡 영구정지) 답변 + 진단 상담 잡기", "기한 10/3 · 진행 중 · 10/2 답장 발송, 회신 오면 일정 확정 · 메이브님 수강생이라 배분 사전 합의 필요 (10/2 등록)", _N+"3ed0cf8fea0481839c31e0155118809c", True),
  ("10/6 12:00 소싱 멘토링 실습 진행 — 수강생 소싱 10개 점검", "플라우드 10/2 멘토링 Action Item · 일시는 노트 기재값 — 확인 필요 (10/3 등록)", _N+"3ed0cf8fea048154a15bddc7596e1165", True),
  ("상품소싱 시트 마진 공식에 매입 배송비 반영 + 백설 와플믹스 10kg 역마진 재확인", "기한 10/4 (10/2 등록)", _N+"3ed0cf8fea04813d9f8aedfc7e183098", True),
  ("마진메이커 크롬 확장 프로그램 설치·서버 배포", "기한 10/4 · 진행 중 · v1 완성, 설치가이드 1~4단계 남음 (10/2 등록)", _N+"3ed0cf8fea0481b18770d4c9279c70a1", False),
  ("힐링디어스(주) 본점 주소 확보 + 본점이전 등기·사업자등록 정정", "기한 10/2 지남 · 진행 중 (10/2 등록)", _N+"3ed0cf8fea0481a7b0c0cfc85f4b3475", False),
  ("멘토루크 블로그 — 블로그 프로그램을 개인 브랜딩(케어 이야기 중심)으로 독립 분기 1차 전환", "기한 10/10 · 진행 중 (10/3 등록)", _N+"3ed0cf8fea0481bc8287dc9e35045f45", False),
  ("다음 주 평일 저녁 팀 회식 장소 확정·예약", "기한 10/5 (10/2 등록)", _N+"3ed0cf8fea0481a08c7ac705e54340e1", False),
  ("홍○○ 대표님(원크루 상담 10/3)께 상담 리포트 링크 발송", "기한 10/4 · 진행 중 (10/3 등록)", _N+"3ee0cf8fea04812e8d21df33ab1687df", True),
  ("매장 대청소 — 업체 선정(비포에프터클린) → 10/5 14:00 작업 입회·검수", "입회·검수 항목은 기한 10/5 · 노션 '진행 중', 업체 선정 항목은 '시작 전' — 끝났으면 둘 다 완료 처리 필요 (10/4·10/5 등록)", _N+"3ee0cf8fea0481fa9237cd0b76f22b45", False),
  ("6기 무료 라이브(10/25) 준비 — PPT 제작(B스타일 네이비&크림으로 새로) · 남은 미결정 사항 확정 · 수강생 인터뷰 5명 섭외·자료", "모두 기한 10/11 · PPT·미결정 사항은 진행 중 (10/4 등록 4건)", _N+"3ee0cf8fea04815d91cdf96ae0a85075", True),
  ("키티티 AI 뷰티 플랫폼 — 전환 검증 실험(랜딩+사전예약) · 진단 링크 홍보·파트너샵 마케팅 키트 1판 · 홈페이지 클릭 수 기록 시작 · K-뷰티 크리에이터 챌린지 공고 확인", "모두 기한 10/11 · 검증 통과 기준: 랜딩 방문 300명 중 예약금 결제 10명 (10/4 등록 4건)", _N+"3ef0cf8fea04812c9dbfcf46c011ba42", True),
  ("키티티 계약 — 10/8(목)", "계약 종류·시간·장소는 아직 미정 — 확인 필요 · 준비물: 신분증·도장, 서류 재확인, 계약서 사진 보관 (10/5 등록)", _N+"3f00cf8fea0481a89260d919b12e75c3", True),
 ],
 "P1": [
  ("박태경 대표님 — 안내 템플릿 3종(10/5) · 빠른 거절·통보 기준(10/6) · 4회차 자료 재공유(10/7) · 자동 알림 조사(10/7) · 겨울 시즌 리스트·광고 가이드(10/10)", "플라우드 9/30 세션 할 일 목록에서 새로 등록", _N+"3eb0cf8fea04812c84d8d9344b5cfec6", True),
  ("최은봉 대표님 — 10/20 당근 2주 결과 판정 · 성과 기반 파일럿 제안서·착수금 템플릿(10/31)", "", _N+"3eb0cf8fea0481eabc25d08c7f5019f3", True),
  ("일십백천 수강생 수경 브랜드 10월 재시동 지원", "기한 10/31 · 보조 품목 규칙 사전조사, 다음 컨설팅 일정 확정", _N+"3eb0cf8fea048138a1e5d67100f3785c", True),
  ("수강생 전체 공지·교육자료 — 화장품 2차 포장(단상자)·표시사항 유지, 도매처 검증 체크리스트", "기한 9/30 지남", _N+"3ea0cf8fea0481969503d67f972a91e1", True),
  ("배수진(돈 걸고 목표달성 앱) 프로토타입 검토", "기한 10/6 · 진행 중", _N+"3ea0cf8fea0481af8112d35bc3c0e23b", True),
  ("뿌요 짠테크 유튜브 — 3화 대본(10/7) · 2화 촬영·편집(10/10)", "", _N+"3ea0cf8fea04818f9d6fdd1b114a853e", False),
  ("뷰셀 회차 주제 후보 22개 — 순서 확정과 수치 검증", "기한 10/31 · 진행 중", _N+"3eb0cf8fea0481e084eac0131859e2ca", False),
  ("현재 사무실 임대료·관리비 정산", "플라우드 9/29 회의 · 기한 10/5는 추정 — 확인 필요", _N+"3eb0cf8fea0481c2a29df44aa8ee126e", False),
  ("정부지원사업 맞춰 보기 사이트 「되는 지원사업 찾기」 구축 (클로드 코드)", "기한 10/8 · 진행 중 (10/1 등록)", _N+"3ec0cf8fea048151a8acff9e6bbd0442", False),
  ("10/2 소싱 멘토링 후속 문서 — 총액 계산 시트 템플릿(10/8) · 선별 기준표(10/9) · 미스매치 재검증 체크리스트·실질 단가 환산 규칙(10/10~11) · 소액 테스트 프로토콜(10/12)", "플라우드 10/2 멘토링 Action Item 중 루크 담당 · 기한은 노트 기재값 (10/3 노션 등록 4건)", _N+"3ed0cf8fea0481a4837dc07d4eeaa7a7", True),
  ("교육회사(셀러들의 수다)+3PL 법인 — 신규 설립 vs 힐링디어스 변경 결정", "기한 10/31 (10/2 등록)", _N+"3ed0cf8fea048121be35ee82635e54a4", True),
  ("키티티 원장님 — /admin 노트 사용법 전달·시술 방향 피드백 + /guide 내용 피드백 받기", "둘 다 기한 10/9 (10/2 등록 2건)", _N+"3ed0cf8fea04810b808df66fdd4ed562", False),
  ("무료 라이브 특강 참석자 선물 준비 — 소싱처 전자책 + 자동 등록 프로그램 7일 이용권", "10/2 인터뷰 녹음에서 약속 · 기한 10/24는 추정 — 확인 필요 (10/3 등록)", _N+"3ed0cf8fea0481ab9090e503641c10b6", False),
  ("API 캐시 자동 충전 설정 — 잔액 8,000원 미만이면 8,000원 충전", "플라우드 10/2 멘토링 Action Item · 기한 없음 (10/3 등록)", _N+"3ed0cf8fea0481b19467f1586979d14c", False),
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
 ],
 "P2": [
  ("배민(B마트·배민스토어) 화장품 판매 채널 입점 가능성 확인", "기한 10/31", _N+"3eb0cf8fea0481069327e3ef0da7a08d", True),
  ("전자책 3종 — 「불평만 하고 도전은 안 하는 비겁한 사람들」 · 「끼리끼리 모이면 실패하는 이유」 · 「부자들은 하고 가난한 사람들은 하지 않는 말」", "기한 10/31 · 세 번째는 10/1 등록", _N+"3eb0cf8fea0481299b1aeaf71e8c9536", False),
  ("트리플 루프 빈 칸 설계 — 지영 채널 자체 수익 + 실물 제품 유통 아이템", "기한 11/30", _N+"3eb0cf8fea0481dd8721d7c5260db6d1", True),
  ("영상공장 AI 라벨 자동 켜기 확인 (유튜브 합성 콘텐츠·인스타 AI 정보)", "기한 없음", _N+"3eb0cf8fea04817e87d2c4ec5d319b6b", False),
  ("영상 자동화 프로그램 만들기 (지영 요청 개발건)", "기한 없음", _N+"3ea0cf8fea0481e8bccdcb6db430eeb4", False),
  ("힐링디어스(주) 업력·매출 기준 2027 정부지원사업(초창패·디딤돌·도약패키지) 지원 가능 여부 확인", "기한 11/30 (10/1 등록)", _N+"3ec0cf8fea04810e84d3e7ceb43c766d", True),
  ("디노 — 1년 사업자 업종코드가 9년 사업자와 다른지 확인 + 9년 사업자 폐업 시점 검토", "담당 수민님 · 기한 없음 (10/1 등록)", _N+"3ec0cf8fea04816eae8bcd7b7a2a9f54", True),
  ("수파베이스 전용 프로젝트 분리 여부 결정 (Pro 업그레이드 또는 기존 프로젝트 정리)", "기한 10/31 · 헤메네일 시세판 (10/1 등록)", _N+"3ec0cf8fea048134aac2dbc802115811", False),
  ("초창패 PSST 계획서 초안 12월 안에 완료", "기한 12/31 · 3개월 실측 숫자·파트너 의향서·대표자 자격 증빙 반영 (10/4 등록)", _N+"3ef0cf8fea0481859a20e212db58d884", True),
  ("헤메네일 — [결정 필요] 카카오 로컬 API로 추천 1~3위 업종 실시간 대조(표시만 vs 순위 반영)", "기한 11/30 · 함께 묶였던 '영업 확인 목록 월간 갱신'은 10/5 예약 작업으로 자동화돼 완료 (10/4 등록)", _N+"3ee0cf8fea048171ad3ef13b0f780e44", False),
 ],
 "P3": [
  ("[공개 직전] 헤메네일 — 도메인 hemenail.kr 선점 · 상표 35류 출원 · 기술 작업 7가지(가격제보·리뷰 이식, 검색노출, 약관 등)", "공개 직전에 할 일 · 기한 없음 (10/1 등록 3건)", _N+"3ec0cf8fea048104bdd0da8356e9bc11", False),
  ("[공개 직전] 헤메네일 업종별 정보 페이지 테마 (헤어·메이크업·네일 별도 톤)", "공개 직전에 할 일 · 기한 없음 (10/3 등록)", _N+"3ee0cf8fea0481ef8c22d7f5a93de94e", False),
  ("[공개 직전] 헤메네일 — 개인정보 보호책임자 이름·이메일 정하기 · 도메인 연결 뒤 검색 등록(구글 서치콘솔·네이버 서치어드바이저) · 카카오 링크 도메인 등록 후 '카카오톡으로 보내기' 버튼 켜기", "공개 직전에 할 일 · 기한 없음 (10/5 등록 3건)", _N+"3ef0cf8fea0481bfaf94d3c15ebbf9b9", False),
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
    <li><div class="t">리나님 (물류)</div><div class="m">시간 기록 시트 2주 시범(9/29~10/12) → 크롬 확장 설계</div></li>
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
    <li><div class="t">10/8 · 신규 강의 플랫폼 3자 구도 결정</div><div class="bar"><i style="width:30%"></i></div><div class="m">PD 접촉 → 본부장 미팅 → 배분안 합의</div></li>
    <li><div class="t">10월 말 · 무료 라이브 → 신규 리스트</div><div class="bar"><i style="width:20%"></i></div><div class="m">록터뷰 2회차 촬영 완료 · 날짜 10/25(일)는 10/4 노션 [결정]으로 확정 · 시간 19:00는 10/2 녹음 언급값, 신청 링크 확인 필요</div></li>
    <li><div class="t">11월 말 · 메이크업헬퍼 9주차 판정</div><div class="bar"><i style="width:15%"></i></div><div class="m">계약 체결 완료(9/30 녹음) · 10/1 당근 광고 테스트 시작 예정이었음(시작 여부 확인 필요) · 10/20 2주 판정</div></li>
    <li><div class="t">12월 · 툴박스 500명</div><div class="bar"><i style="width:10%"></i></div><div class="m">사이트 구축 완료, 결제 심사·공개 문구 남음</div></li>
    <li><div class="t">2027 2월 · 키티티 샵 오픈</div><div class="bar"><i style="width:25%"></i></div><div class="m">상표권 출원 10/1이 마지노선이었음 — 지영 명의 전자출원 '진행 중'(노션 기한 10/4)</div></li>
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
    <dt>강사 배분</dt><dd>광고비 등 <b>모든 비용을 뺀 순수익을 강사와 5:5</b> (광고비는 총매출의 8%로 추정)</dd>
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

<h2>숫자를 맞춰보면 — 두 군데가 어긋납니다 <small>계약 전에 닫을 것</small></h2>
<div class="card red">
  <h3 style="margin-bottom:8px">① 강사 몫이 계산보다 1,400~1,600만 적게 제시돼 있습니다</h3>
  <div class="wrapx"><table>
  <tr><th></th><th>30명</th><th>40명</th></tr>
  <tr><td>매출 (289만 × 인원)</td><td class="num">8,670만</td><td class="num">1억 1,560만</td></tr>
  <tr><td>− 루크 수수료 8%</td><td class="num">694만</td><td class="num">925만</td></tr>
  <tr><td>− 광고비 8%(추정)</td><td class="num">694만</td><td class="num">925만</td></tr>
  <tr><td>= 남는 돈</td><td class="num">7,282만</td><td class="num">9,710만</td></tr>
  <tr><td><b>5:5 하면 강사 몫</b></td><td class="num"><b>3,641만</b></td><td class="num"><b>4,855만</b></td></tr>
  <tr><td>회의에서 제시한 값</td><td class="num">2,200만</td><td class="num">3,200만</td></tr>
  </table></div>
  <p class="note" style="margin-top:8px">차이만큼 다른 비용(PG·PD 인건비·제작비 등)이 들어간다고 본 것이거나, 보수적으로 제시한 것입니다. 어느 쪽이든 <b>'비용'에 무엇이 들어가는지 목록을 못 박지 않으면 정산할 때 분쟁이 납니다.</b> 5:5는 비율이고, 분모를 정하는 것이 실제 계약입니다.</p>

  <h3 style="margin:16px 0 8px">② 8%가 두 번 나오는데 서로 다른 8%입니다</h3>
  <p style="margin:0 0 8px">루크 수수료 8%(PG 제외 매출 기준)와 광고비 8%(총매출 기준 추정)가 같은 숫자라 섞이기 쉽습니다. <b>'전체 매출'의 정의</b>(PG 전/후, 환불 전/후, 부가세 포함 여부)와 <b>광고비를 순수익 계산에서 빼는 주체</b>를 글로 적어야 합니다.</p>

  <h3 style="margin:16px 0 8px">③ 전환율 10%는 과거의 3배 이상입니다</h3>
  <p style="margin:0">과거 신규 강사 런칭 기록은 <b>DB 3,000개 → 라이브 유입 18~20%(540~600명) → 전환 3% 내외</b>였습니다. 같은 유입(400~600명)에서 과거 전환율을 쓰면 <b>16~18명</b>, 목표 전환율 10%를 쓰면 30~40명 — 두 배 이상 차이입니다. 숫자를 어느 쪽으로 잡고 광고비를 태울지가 손익을 가릅니다.</p>
</div>

<h2>결론이 안 난 다섯 가지</h2>
<div class="card gold">
  <ul class="list">
    <li><span class="tag p0">1</span><div class="t">루크의 참여 범위 — 단순 플레이어인가, 공동 기획인가</div><div class="m">여기에 따라 수익 배분이 달라집니다. 10/22·10/29에 옵션 정리와 배분 초안을 만들기로 했습니다</div></li>
    <li><span class="tag p0">2</span><div class="t">상품 최종 확정</div><div class="m">289만 단일로 갈지, 1:1 컨설팅반을 넣을지, 목표 객단가는 얼마인지</div></li>
    <li><span class="tag p0">3</span><div class="t">파일럿 강사 — 후보 두 분 중 미결</div><div class="m">10/7 기준 <b>가을(정복녀) 대표님</b>(40대 주부·원크루) 또는 <b>뿌요</b>. 11월 초 촬영이니 실제로 3주 남았습니다 — 두 분을 같은 기준에 올려 비교한 것은 <a href="../pilot/">파일럿 강사 결정</a>에 있습니다</div></li>
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

<div class="src" style="margin-top:14px">근거: 10/6 17:22 메이븐·초월스토리 회의 녹음(48분) · 10/6 16:30 초월스토리 촬영 녹음(42분). 표의 계산은 회의에 나온 수치(289만 · 8% · 5:5 · 30~40명)를 그대로 넣어 클로드가 맞춰본 것으로, 비용 항목이 확정되지 않아 실제와 다를 수 있습니다. 계약 조건은 구두 합의 단계이며 문서화 전입니다.</div>
"""

# ---------------------------------------------------------------- 파일럿 강사 결정
PILOT = """
<h1>파일럿 강사 — 누구로 갈 것인가</h1>
<p class="note">후보는 두 분입니다 — <b>가을(정복녀) 대표님</b>(40대 주부·원크루) 또는 <b>뿌요(최근영)</b>(30대 중후반). <a href="../chowol/">초월스토리 협업</a>에서 결론이 안 난 다섯 가지 중 3번이고, <b>12월 초 라이브를 지키려면 가장 먼저 닫아야 하는 칸</b>입니다. 11월 초에 촬영이 들어가야 하니 실제로 남은 시간은 3주입니다.</p>

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
<p class="note">2026-10-07 열람한 등기사항전부증명서(말소사항 포함) 기준으로 다시 썼습니다. 추측이 아니라 <b>등기부에 적힌 그대로</b>입니다. 실제 접수는 법무사 확인 후에 하세요. 전략 판단은 <a href="../corp/">힐링디어스 → 셀러들의 수다</a>에 있습니다.</p>

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

<div class="src" style="margin-top:14px">근거: 2026-10-07 열람한 힐링디어스 주식회사 등기사항전부증명서(말소사항 포함, 열람 700원) — 회사성립 2022-03-16 · 본점 경기도 구리시 갈매순환로 188 제7층(2023-12-01 변경, 2023-12-12 등기) · 1주 금액 5,000원 · 발행할 주식의 총수 200주 · 발행주식의 총수 200주 · 자본금 100만 원 · 공고방법 수원시 내 발행 일간 경기신문 · 목적에 부동산 매매업 및 임대업, 전자상거래 및 통신판매업 포함(2023-01-09 다수 추가) · 사내이사·감사 2025-03-16 중임, 2025-03-24 등기 · 관할 의정부지방법원 남양주지원 등기과. 그 외: 상법 제182조(본점 이전등기 2주) · 상법 제383조(이사 임기 3년) · 상법 제520조의2(최후 등기 후 5년 해산간주) · 본점이전 공과금 142,000원(같은 관할). <b>여러 변경을 한 신청서로 묶을 때의 등록면허세 계산, 증자 등록면허세 세율은 확인하지 못했습니다 — 법무사 확인 후 진행하세요.</b></div>
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
 "chowol":(2,22), "invader":(2,14),
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
  <ul><li>전체 항목의 할 일·기한·상태·[결정] (10/6 06:40 조회). 미완료·기한 있는 항목은 일정에, 최근 7일 새 항목은 우선순위에 반영. 목표가 '사업 외 개인'인 항목은 넣지 않음(상표권 제외)</li>
  <li>10/1 새로 만든 항목 9건: 박태경 대표님 지원 5건(플라우드 9/30), 사무실 임대료 정산·서울 이전 로드맵·트레이드 채널·'하루를 4번 쓰는 법' 영상(플라우드 9/29). 뒤 4건의 기한은 추정이라 '확인 필요'로 표시</li>
  <li>10/2 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/1에 노션에 새로 생긴 기한 항목 7건을 일정에 추가(상표 출원·키티티 사이트·지원사업 3건·전자책·수파베이스) · 최근 [결정]에 10/1 결정 2건 반영 · 플라우드는 10/1~10/2 새 녹음이 없어 노션에 새로 만든 항목 0건 (9/30 녹음의 루크 담당 Action Item은 이미 액션보드에 있음)</li>
  <li>10/3 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/2에 노션에 새로 생긴 기한 항목 9건을 일정에 추가(평생컨설팅 문의·상품소싱 시트·마진메이커·힐링디어스 본점·회식·키티티 피드백 2건·멘토루크 블로그·법인 결정) · 플라우드 10/2 녹음 4건에서 노션 새 항목 7건(소싱 멘토링 6건 + 무료 라이브 선물 준비 1건), 기한은 노트 기재값·추정이라 '확인 필요' · 최근 [결정]에 10/2 마진메이커 결정 반영 · 7일이 지난 진행 중 항목 3건은 '새 항목' 표시를 뗌</li>
  <li>10/4 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/3에 노션에 새로 생긴 기한 항목 2건을 일정에 추가(원크루 상담 리포트 링크 발송 10/4 · 재문의 확인 10/17) · 우선순위 '새 항목'에 4건 추가, 7일 지난 1건(셀수다 설치)은 일반 줄로 · 최근 [결정] 맨 위에 10/4 통합 보고 구조 · 플라우드 10/3 녹음 1건(원크루 상담)에서 노션 새 항목 0건 · 상황판 보고 피드: 어제 이후 새 보고 0건(피드의 2건은 9/30·10/1자이고 노션에 이미 완료로 있음), 막힘 0건</li>
  <li>10/5 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건(윤지영 원장 개업연월일 확인) 제거 · 10/4~10/5에 노션에 새로 생긴 기한 항목 27건을 일정에 추가(6기 무료 라이브 준비 4건 · 키티티 AI 뷰티 플랫폼 15건 · 헤메네일 5건 · 맥북 교체 · Vercel Pro 결정 · 원크루 사이트 4단계) · 우선순위 '새 항목'에서 완료 2건(카카오맵 JS키·개업연월일 확인) 빼고 새 묶음 10줄 추가 · 최근 [결정] 6개를 10/4~10/5 결정으로 교체 · 무료 라이브 날짜 10/25는 10/4 [결정]으로 확정 표시(시간·신청 링크는 확인 필요) · 플라우드 10/3 인터뷰 녹음 1건에서 노션 새 항목 0건 · 상황판: 노션 [보고] 5건 중 1건(메이크업헬퍼 AI 기술 5가지 제안)을 피드에 새로 옮김 — 나머지 4건은 클로드 코드가 이미 직접 올린 보고와 같은 일이라 그대로 둠 · 허브 맨 위에 [결정 필요] 2건(헤메네일 카카오 미등록 매장 순위 · 키티티 정부지원 방식). 피드의 '막힘' 중 키티티 도메인 구매·원크루 Supabase 한도는 뒤이은 완료 보고·노션 [결정]으로 해결된 것으로 확인돼 올리지 않음</li>
  <li>10/6 갱신: 일정에 있던 항목 중 완료로 바뀐 것 5건 제거(헤메네일 [결정 필요] 3건 — 카카오 전화번호 표시·상가정보 대조·가격 최신화 / Apps Script 권한 승인은 예약 작업으로 대체돼 불필요 / 영업 확인 목록 월간 갱신은 예약 작업으로 자동화) · 10/5에 노션에 새로 생긴 기한 항목 4건을 일정에 추가(매장 대청소 입회·검수 10/5 · 키티티 계약 10/8 · 멘토루크 파인더 네이버 쇼핑 API 종료 대응 10/31 · 원크루 라운지 첫 자료 10/31) · 우선순위 '새 항목'에 9줄 추가, 7일 지난 5건(9/28 등록분)은 일반 줄로 · 최근 [결정] 6개를 10/5 결정으로 교체 · 노션 [보고] 6건 중 새로 옮긴 것 0건('2027 정부지원사업 리스트'는 클로드 코드가 이미 직접 올린 보고와 같은 일) · 허브 맨 위 [결정 필요] 4건(10/5 '막힘' 보고 2건 추가: 키티티 AI 상담 OpenAI 키·루크 툴박스 도구 판매 조건) · 플라우드 10/4~10/6 새 녹음 없음 → 노션에 새로 만든 항목 0건</li></ul>
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
