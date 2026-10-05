# -*- coding: utf-8 -*-
"""내 연봉 10억 만들기 — 정적 페이지 빌드 스크립트.
python3 build.py 실행 시 index.html 과 하위 폴더 index.html 을 전부 새로 씁니다.
(부분 수정 금지 원칙: 매번 파일 전체를 다시 생성)"""
import json, os, datetime

UPDATED = "2026-10-05"
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
.lu-node{animation:luBreathe 3.8s ease-in-out infinite}
.lu-lab{paint-order:stroke;stroke:#0a1016;stroke-width:3px;stroke-linejoin:round}
.uni-hit{cursor:pointer}
.uni-reg{transition:opacity .25s}
.uni-nd.sel text{fill:#fff;font-weight:700}
.uni-nd.sel circle{stroke:#fff}
#uniPanel .tag{margin-right:6px}
@media (prefers-reduced-motion: reduce){.lu-halo,.lu-star,.lu-flow,.lu-spoke,.lu-node{animation:none}}
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
  {"d":"2026-09-20","t":"Apps Script '헤메네일 공공 가격 수집' 권한 승인 1회 + setup 실행","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea04816bb79af990d142183a","cash":False},
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
  {"d":"2026-10-07","t":"뿌요 짠테크 유튜브 3화 '연쇄적금러' 대본 작성","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea04818f9d6fdd1b114a853e","cash":False},
  {"d":"2026-10-07","t":"물류 권한 재설계 + 감사 로그","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"지영 예약·매출 간단 대시보드 완료 목표","who":"지영","p":"P2","cash":False},
  {"d":"2026-10-08","t":"종혁 본부장 미팅 — 락인 축(챌린지·카페·광고) 역할과 1:1:1 배분안 제시 [설명서]","who":"루크·메이브님","p":"P0","g":"platform-director-meeting","n":"https://app.notion.com/p/3eb0cf8fea04816b8d8ee9e56061c6d0","cash":True},
  {"d":"2026-10-08","t":"최은봉 대표님 미팅 14:00 — 당근 광고 중간 결과 화면 리뷰 (노션은 10/8, 녹음은 '수요일'=10/7 · 날짜 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04814c922bc0af3fa5ab4f","cash":True},
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
  {"d":"2026-10-11","t":"[결정 필요] 헤메네일 전화 버튼 없는 62% — 카카오 공식 API 전화번호를 상세 열 때만 표시할지","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481e0b230e9b3c2c7a05f","cash":False},
  {"d":"2026-10-11","t":"[결정 필요] 헤메네일 상가(상권)정보로 실제 영업 여부 교차 확인 — 파일 다운로드 허락 (10/4 대조 완료 보고가 있음 · 노션 상태 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04814eaddef5b63c435bce","cash":False},
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
  {"d":"2026-10-31","t":"[결정 필요] 헤메네일 가격 최신화 — 추천 4단계 중 어디까지 만들지","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048175a219dadbae197e5d","cash":False},
  {"d":"2026-10-31","t":"헤메네일 가격비교 → AI 진단 링크 연결 (보조 송객 채널)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048134b9ede80fe9d7ed0f","cash":False},
  {"d":"2026-10-31","t":"업무용 맥북 교체 (중고 M4 맥북에어 16GB 검토, M1 에어는 중고 판매)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea04817bba04cb14d260f50f","cash":False},
  {"d":"2026-10-31","t":"Vercel 팀을 Pro($20/월)로 바꿀지 결정 — 무료(Hobby)는 비상업 전용인데 공방 유료 결제 운영 중","who":"담당 미기재","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea0481ab90bcfc0684789878","cash":False},
  {"d":"2026-10-31","t":"원크루 사이트 4단계 — 로그인·가입 + 원크루 회원 표 + 회원 넣기/빼기 관리자 화면","who":"담당 미기재","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048181a121fa70732b2b17","cash":False},
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
  {"d":"2026-11-04","t":"헤메네일 영업 확인 목록 월간 갱신 (상가정보 분기·카카오 재점검)","who":"루크","p":"P2","n":"https://app.notion.com/p/3ef0cf8fea0481f0b204f783bc8a2216","cash":False},
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
    <li data-n="https://app.notion.com/p/3ef0cf8fea04814eaddef5b63c435bce"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 헤메네일 — 카카오 지도에 없는 매장을 순위에 소폭 반영할지</div><div class="m">10/4 상황판 '막힘' 보고(폐업 의심 매장 순위 내리기) · 함께 물었던 상가(상권)정보 대조는 10/4·10/5 완료 보고에 이미 반영된 것으로 보임 — 노션 '[결정 필요] 상가정보 교차 확인'(기한 10/11)은 아직 시작 전이라 확인 필요 · <a href="status/?p=헤메네일">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048141a4aee0ab6b56da87"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 키티티 정부지원 — 초창패 본선 + 모두의 창업 보험으로 갈지 · 이종 사업자 등록 방식(업종 추가 vs 새 사업자)</div><div class="m">10/4 노션 [보고] '정부지원 전략 v13' 메모의 '[막힘] 루크 결정 필요' (노션 상태는 완료) · 다음: 창업진흥원 1357·세무사 확인, 트랙(일반/기술 vs 로컬) 결정 · <a href="reports/kititi-grant-strategy/?v=13">보고서</a></div></li>
    <li data-g="developer-accounts"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 (Apple · Google Play · Microsoft)</div><div class="m">툴박스·영상공장·블로그타이퍼를 폰·맥·윈도우로 배포하는 모든 일의 앞단. Apple은 승인에 며칠 걸림 · 기한 10/2 지남(노션 미완료)</div></li>
    <li data-g="platform-pd-meeting"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 3자 구도 — PD 미팅(기한 10/5) → 10/8 본부장 미팅</div><div class="m">플레이어·강사교육 = 루크·메이브님 / 락인(챌린지 영상·네이버 카페·광고) = 종혁 본부장 / 모객 = 초이스토리 PD · <a href="platform/">전략 페이지</a></div></li>
    <li data-g="3pl-resale"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">3PL 수강생 재고 당근·외부 판매 첫 등록</div><div class="m">동의서(수수료 15~20%) → 재고 시트 판매 열 + 사진 → 당근 비즈프로필 → 30개 등록 · 통신판매업 신고 사업자 명의 필수 · 기한 10/1 지남(노션 미완료)</div></li>
    <li data-g="dino-12weeks"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">디노(미니쌤) 12주 빌드업 합의 → 10/5 1주차 시작</div><div class="m">AI 셀러 실무 교육 · 1달 90 / 2달 200 / 3달 350만 기준 · 상품별 배분 비율 확정</div></li>
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
<p class="note">기준: 현금에 가깝고 다른 일의 선행 조건일수록 위. 기한은 노션 액션보드 기준. [결정]은 완료로, [보류]는 P3로. <span class="tag">새 항목</span>은 최근 7일(9/28~) 안에 노션에 생긴 미완료 항목입니다.</p>

<h2>P0 · 이번 주 <small>~10/11</small></h2>
<div class="card red">
  <ul class="list tasks">
    <li data-g="developer-accounts"><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 — Apple Developer / Google Play / Microsoft Store</div><div class="m">기한 10/2 지남(노션 미완료) · 앱 배포(툴박스 PWA→앱, 영상공장, 블로그타이퍼) 전부의 앞단. 루크가 "제일 높은 등급"으로 지정(9/30)</div></li>
    <li data-g="platform-pd-meeting"><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 3자 구도 — 초이스토리 PD 미팅(모객, 기한 10/5) → 10/8 종혁 본부장(락인)</div><div class="m"><a href="../platform/">전략 페이지</a> · 나머지 우선순위는 이 둘의 결과에 따라 달라짐(루크 9/30)</div></li>
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
    <li><span class="tag done">결정</span><div class="t">원크루 사이트는 공방(거인의 도구 공방) Supabase를 같이 씀 — 원크루 표시로 입구에서 막고, 두 사이트 회원 통로는 만들지 않음 (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">원크루 사이트 도메인은 맨 나중에 — 그동안 vercel.app 기본 주소로 진행 (10/5)</div></li>
    <li><span class="tag done">결정</span><div class="t">AI 진단은 각 샵이 직접 홍보하는 손님 끌기 도구, 헤메네일은 보조 송객 (10/4)</div></li>
    <li><span class="tag done">결정</span><div class="t">AI 뷰티 플랫폼은 샵 고객 유치·시술 중심, 화장품 커머스는 확장 옵션 (10/4)</div></li>
    <li><span class="tag done">결정</span><div class="t">초창패 신청 주체 = 키티티, 루크는 협력사 (10/4)</div></li>
    <li><span class="tag done">결정</span><div class="t">6기 라이브 3PL 안내: 기본 택배비 3,000원에 부자재·포장·발송, 보관 무료 / 강의 연차는 '5년 넘게' / PPT는 원본 분량(약 300장) (10/4)</div></li>
  </ul>
</div>
"""

# 최근 7일(9/28~) 안에 노션 액션보드에 새로 생긴 미완료 항목 — 우선순위 페이지 각 P 구간 끝에 붙는다.
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
  ("영상공장 윈도우 PC 설치·첫 영상 테스트", "기한 9/30 · 진행 중 · API 키 5개·목소리 녹음은 10/5", _N+"3e90cf8fea04815da58cc6d8030ca735", False),
  ("록터뷰 2회차 인터뷰 촬영", "기한 9/28 · 노션 '진행 중' — 촬영이 끝났으면 완료 처리 필요", _N+"3e90cf8fea048107ba1dff3afb73cedd", False),
  ("키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체", "기한 10/8 · 진행 중 (10/1 등록)", _N+"3ec0cf8fea0481698468f35e62d2e19b", False),
  ("평생컨설팅 문의(뷰셀 수강생·쿠팡 영구정지) 답변 + 진단 상담 잡기", "기한 10/3 · 진행 중 · 10/2 답장 발송, 회신 오면 일정 확정 · 메이브님 수강생이라 배분 사전 합의 필요 (10/2 등록)", _N+"3ed0cf8fea0481839c31e0155118809c", True),
  ("10/6 12:00 소싱 멘토링 실습 진행 — 수강생 소싱 10개 점검", "플라우드 10/2 멘토링 Action Item · 일시는 노트 기재값 — 확인 필요 (10/3 등록)", _N+"3ed0cf8fea048154a15bddc7596e1165", True),
  ("상품소싱 시트 마진 공식에 매입 배송비 반영 + 백설 와플믹스 10kg 역마진 재확인", "기한 10/4 (10/2 등록)", _N+"3ed0cf8fea04813d9f8aedfc7e183098", True),
  ("마진메이커 크롬 확장 프로그램 설치·서버 배포", "기한 10/4 · 진행 중 · v1 완성, 설치가이드 1~4단계 남음 (10/2 등록)", _N+"3ed0cf8fea0481b18770d4c9279c70a1", False),
  ("힐링디어스(주) 본점 주소 확보 + 본점이전 등기·사업자등록 정정", "기한 10/2 지남 · 진행 중 (10/2 등록)", _N+"3ed0cf8fea0481a7b0c0cfc85f4b3475", False),
  ("멘토루크 블로그 — 블로그 프로그램을 개인 브랜딩(케어 이야기 중심)으로 독립 분기 1차 전환", "기한 10/10 · 진행 중 (10/3 등록)", _N+"3ed0cf8fea0481bc8287dc9e35045f45", False),
  ("다음 주 평일 저녁 팀 회식 장소 확정·예약", "기한 10/5 (10/2 등록)", _N+"3ed0cf8fea0481a08c7ac705e54340e1", False),
  ("홍○○ 대표님(원크루 상담 10/3)께 상담 리포트 링크 발송", "기한 10/4 · 진행 중 (10/3 등록)", _N+"3ee0cf8fea04812e8d21df33ab1687df", True),
  ("매장 대청소 업체 선정 — 10/13까지 (여행 중 작업)", "노션 기한 칸은 비어 있고 제목에 10/13 · 담당·목표 미기재 · 10/4 노션에 '[완료] 매장 대청소 — 비포에프터클린, 10/5 작업' 기록이 생김(상태는 시작 전) — 끝났으면 완료 처리 필요 (10/4 등록)", _N+"3ee0cf8fea0481fa9237cd0b76f22b45", False),
  ("6기 무료 라이브(10/25) 준비 — PPT 제작(B스타일 네이비&크림으로 새로) · 남은 미결정 사항 확정 · 수강생 인터뷰 5명 섭외·자료", "모두 기한 10/11 · PPT·미결정 사항은 진행 중 (10/4 등록 4건)", _N+"3ee0cf8fea04815d91cdf96ae0a85075", True),
  ("키티티 AI 뷰티 플랫폼 — 전환 검증 실험(랜딩+사전예약) · 진단 링크 홍보·파트너샵 마케팅 키트 1판 · 홈페이지 클릭 수 기록 시작 · K-뷰티 크리에이터 챌린지 공고 확인", "모두 기한 10/11 · 검증 통과 기준: 랜딩 방문 300명 중 예약금 결제 10명 (10/4 등록 4건)", _N+"3ef0cf8fea04812c9dbfcf46c011ba42", True),
 ],
 "P1": [
  ("박태경 대표님 — 안내 템플릿 3종(10/5) · 빠른 거절·통보 기준(10/6) · 4회차 자료 재공유(10/7) · 자동 알림 조사(10/7) · 겨울 시즌 리스트·광고 가이드(10/10)", "플라우드 9/30 세션 할 일 목록에서 새로 등록", _N+"3eb0cf8fea04812c84d8d9344b5cfec6", True),
  ("최은봉 대표님 — 10/20 당근 2주 결과 판정 · 성과 기반 파일럿 제안서·착수금 템플릿(10/31)", "", _N+"3eb0cf8fea0481eabc25d08c7f5019f3", True),
  ("일십백천 수강생 수경 브랜드 10월 재시동 지원", "기한 10/31 · 보조 품목 규칙 사전조사, 다음 컨설팅 일정 확정", _N+"3eb0cf8fea048138a1e5d67100f3785c", True),
  ("수강생 전체 공지·교육자료 — 화장품 2차 포장(단상자)·표시사항 유지, 도매처 검증 체크리스트", "기한 9/30 지남", _N+"3ea0cf8fea0481969503d67f972a91e1", True),
  ("배수진(돈 걸고 목표달성 앱) 프로토타입 검토", "기한 10/6 · 진행 중", _N+"3ea0cf8fea0481af8112d35bc3c0e23b", True),
  ("뿌요 짠테크 유튜브 — 3화 대본(10/7) · 2화 촬영·편집(10/10)", "", _N+"3ea0cf8fea04818f9d6fdd1b114a853e", False),
  ("뷰셀 회차 주제 후보 22개 — 순서 확정과 수치 검증", "기한 10/31 · 진행 중", _N+"3eb0cf8fea0481e084eac0131859e2ca", False),
  ("미니쌤 채널 공지 3회 (10/12주 · 10/26주 · 11/23주)", "기한 10/16", _N+"3e90cf8fea0481dc8e86ef413c4e23c8", False),
  ("미용인 라운지 사이트 v1 · 하루블록 v1.0 무료 배포 준비", "둘 다 기한 9/30 · 진행 중", _N+"3e90cf8fea0481faadcdf4ad3356a80b", False),
  ("앱 배포 계정·인증서 준비 (윈도우·맥·아이폰·갤럭시)", "기한 9/30 · 진행 중 · P0 '개발자 계정 3종'과 같이", _N+"3e90cf8fea0481468c69f67787077a44", False),
  ("현재 사무실 임대료·관리비 정산", "플라우드 9/29 회의 · 기한 10/5는 추정 — 확인 필요", _N+"3eb0cf8fea0481c2a29df44aa8ee126e", False),
  ("정부지원사업 맞춰 보기 사이트 「되는 지원사업 찾기」 구축 (클로드 코드)", "기한 10/8 · 진행 중 (10/1 등록)", _N+"3ec0cf8fea048151a8acff9e6bbd0442", False),
  ("10/2 소싱 멘토링 후속 문서 — 총액 계산 시트 템플릿(10/8) · 선별 기준표(10/9) · 미스매치 재검증 체크리스트·실질 단가 환산 규칙(10/10~11) · 소액 테스트 프로토콜(10/12)", "플라우드 10/2 멘토링 Action Item 중 루크 담당 · 기한은 노트 기재값 (10/3 노션 등록 4건)", _N+"3ed0cf8fea0481a4837dc07d4eeaa7a7", True),
  ("교육회사(셀러들의 수다)+3PL 법인 — 신규 설립 vs 힐링디어스 변경 결정", "기한 10/31 (10/2 등록)", _N+"3ed0cf8fea048121be35ee82635e54a4", True),
  ("키티티 원장님 — /admin 노트 사용법 전달·시술 방향 피드백 + /guide 내용 피드백 받기", "둘 다 기한 10/9 (10/2 등록 2건)", _N+"3ed0cf8fea04810b808df66fdd4ed562", False),
  ("무료 라이브 특강 참석자 선물 준비 — 소싱처 전자책 + 자동 등록 프로그램 7일 이용권", "10/2 인터뷰 녹음에서 약속 · 기한 10/24는 추정 — 확인 필요 (10/3 등록)", _N+"3ed0cf8fea0481ab9090e503641c10b6", False),
  ("API 캐시 자동 충전 설정 — 잔액 8,000원 미만이면 8,000원 충전", "플라우드 10/2 멘토링 Action Item · 기한 없음 (10/3 등록)", _N+"3ed0cf8fea0481b19467f1586979d14c", False),
  ("홍○○ 대표님 원크루 재문의 여부 확인", "기한 10/17 · 10/3 상담 후속 (10/3 등록)", _N+"3ee0cf8fea0481b58bcec3ba614eec0f", True),
  ("키티티 AI 뷰티 플랫폼 — 협력 계약서 초안 · 홈페이지 파트너샵용 템플릿 · 파트너 의향서 양식(3곳)·의향 샵 10곳 모집 · 개발비·유지비 구조 재검토 · 업종 추가 세무사 확인 · 초창패 자부담 마련 계획 · 원장 자격·수상 목록 · 웨딩·이벤트 패키지 연결 · 헤메네일→진단 링크", "모두 기한 10/31 · <a href=\"../reports/kititi-win-plan/?v=1\">초창패 승부수 보고서</a> (10/4 등록 10건)", _N+"3ef0cf8fea0481388f9cc6a8fd0cd7db", True),
  ("[결정 필요] 헤메네일 — 전화 버튼 없는 62%에 카카오 전화번호 표시(10/11) · 상가정보 교차 확인 파일 허락(10/11) · 가격 최신화 4단계 중 어디까지(10/31)", "상가정보 대조는 10/4 완료 보고가 있음 — 노션 상태 확인 필요 (10/4 등록 3건)", _N+"3ef0cf8fea0481e0b230e9b3c2c7a05f", False),
  ("원크루 사이트 4단계 — 로그인·가입 + 원크루 회원 표 + 관리자 화면", "기한 10/31 · 처음 넣을 회원 명단 루크 확인 필요 · 3단계(빈 입구 배포)는 10/5 완료 (10/5 등록)", _N+"3ef0cf8fea048181a121fa70732b2b17", False),
  ("Vercel 팀을 Pro($20/월)로 바꿀지 결정 — 무료(Hobby)는 비상업 전용인데 공방 유료 결제 운영 중", "기한 10/31 (10/5 등록)", _N+"3ef0cf8fea0481ab90bcfc0684789878", False),
  ("업무용 맥북 교체 — 중고 M4 맥북에어 16GB 검토, M1 에어는 중고 판매", "기한 10/31 · 진행 중 (10/4 등록)", _N+"3ef0cf8fea04817bba04cb14d260f50f", False),
  ("루크 툴박스 자동 메시지(알림톡·문자) 연동", "기한 없음 · 루크 할 일 3개: 카카오톡 채널+비즈니스 인증 · 솔라피 가입+발신번호 등록 · API 키 전달 (10/4 등록)", _N+"3ef0cf8fea0481dfa1b6d552232ecaa9", False),
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
  ("헤메네일 — [결정 필요] 카카오 로컬 API로 추천 1~3위 업종 실시간 대조(표시만 vs 순위 반영, 11/30) · 영업 확인 목록 월간 갱신(11/4)", "(10/4 등록 2건)", _N+"3ee0cf8fea048171ad3ef13b0f780e44", False),
 ],
 "P3": [
  ("[공개 직전] 헤메네일 — 도메인 hemenail.kr 선점 · 상표 35류 출원 · 기술 작업 7가지(가격제보·리뷰 이식, 검색노출, 약관 등)", "공개 직전에 할 일 · 기한 없음 (10/1 등록 3건)", _N+"3ec0cf8fea048104bdd0da8356e9bc11", False),
  ("[공개 직전] 헤메네일 업종별 정보 페이지 테마 (헤어·메이크업·네일 별도 톤)", "공개 직전에 할 일 · 기한 없음 (10/3 등록)", _N+"3ee0cf8fea0481ef8c22d7f5a93de94e", False),
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

# ---------------------------------------------------------------- 사업 유니버스 지도
UNI_REGIONS = [
 {"id":"ch","no":"①","name":"채널·브랜딩","sub":"신뢰 → 유입","color":"#4fd1a5","ax":90,"ay":130,
  "desc":"사람이 나를 알게 되는 입구. 이 구역이 꺼지면 나머지 구역의 신규 유입이 멈춥니다.",
  "nodes":[
   {"id":"yt","n":"유튜브 1만","full":"유튜브 멘토루크","st":"on","big":1,"d":"구독자 약 1만 명. 주 1개 공개 강의 업로드 유지. 멤버십 4,900원(특강 풀버전·월 상품 브리핑) 개설 예정."},
   {"id":"cafe","n":"네이버 카페","full":"네이버 카페","st":"on","d":"선판매·공지 라인. 신규 강의 플랫폼에서는 이 역할을 '락인 축'이 맡는 구조로 설계 중."},
   {"id":"kakao","n":"카톡 1천","full":"카카오톡 커뮤니티","st":"on","d":"약 1,000명. 특강 공지와 선판매가 여기서 돕니다."},
   {"id":"vcell","n":"뷰셀 채널","full":"뷰셀 채널 (메이브님)","st":"on","d":"화장품 쪽 유입. 2화 촬영 완료, 10/7 공개 예정."},
   {"id":"live","n":"무료 라이브","full":"10월 말 무료 라이브","st":"build","d":"록터뷰 2회차 영상 설명란·고정댓글에 신청 링크를 넣어 신규 리스트를 만드는 자리. 10/2 녹음에서 10/25(일) 19:00로 언급 — 확정 여부와 신청 링크는 확인 필요.","href":"../guides/free-live/","hl":"설명서"},
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
   {"id":"callai","n":"전화 상담 AI","full":"전화 상담 AI","st":"idea","exp":1,"d":"'이거 괜찮은 겁니까' 유형의 계약 문의 전화가 매우 많고 녹음이 100건 넘게 있음(한 통 10~30분). 이 사례들을 분석해 해당 유형만이라도 AI가 답하게 만들려는 구상.","from":"상담 전화 자동화 논의 (9/17)"},
  ]},
 {"id":"pr","no":"③","name":"상품·유통","sub":"반복 → 회전","color":"#8fb0ff","ax":268,"ay":600,
  "desc":"신뢰가 없어도 상품 자체로 유입이 생기는 줄. 채널이 쉬어도 돈이 끊기지 않게 받쳐주는 자리입니다.",
  "nodes":[
   {"id":"tpl","n":"3PL 물류","full":"3PL 물류 대행","st":"on","big":1,"d":"수강생 재고 보관·출고 대행. 뿌요가 운영. 입고 미처리 상태에서 운송장이 나가는 오류를 잡는 안정화가 진행 중.","href":"../guides/logistics-stabilize/","hl":"설명서"},
   {"id":"resale","n":"재고 판매","full":"수강생 재고 외부 판매","st":"build","d":"창고에 잠든 수강생 재고를 회사가 당근·번개장터·네이버에서 판매하고 수수료 15~20%. 동의서 → 재고 시트 → 당근 비즈프로필 → 30개 등록 순서.","href":"../guides/3pl-resale/","hl":"설명서"},
   {"id":"store","n":"창고형 매장","full":"오프라인 창고형 매장","st":"idea","exp":1,"d":"창고 재고를 오프라인에서 직접 파는 구조. 고정비가 낮은 오픈데이+온라인 판매 모델을 더 무거운 대안보다 먼저 두기로 한 기록이 있음. 위치·평수·운영 인력·취급 품목은 아직 미정 — 확인 필요.","from":"3PL 수익 구상 (10월)"},
   {"id":"toolbox","n":"루크 툴박스","full":"루크 툴박스","st":"build","big":1,"d":"월 19,900 / 연 199,000, 오프라인샵 팩 +9,900. 아래 도구들을 하나의 구독으로 묶어 파는 자리. 12월 500명 → 3월 1,000명 목표. 개발자 계정 3종 등록이 모든 배포의 앞단.","href":"../guides/developer-accounts/","hl":"개발자 계정 설명서"},
   {"id":"consign","n":"위탁판매","full":"위탁판매 (메이크업헬퍼)","st":"build","d":"원크루 최은봉 대표 건. 위수탁계약서 기준(사입 아님). 국내는 토스·당근 등 브랜드사 미입점 플랫폼·폐쇄몰·공동구매, 해외는 쇼피·큐텐재팬·이베이. 12주 테스트, 광고 상한 약 189만, 11월 말 판정."},
   {"id":"beauty","n":"미용 가격비교","full":"미용 가격비교 사이트","st":"idea","exp":1,"d":"미용 가격 정보를 확인하는 사이트. 9/28 회의에서 루크가 개발하려는 세 사이트 중 하나로 언급됨.","from":"9/28 회의 (메이브님·디노)"},
  ]},
 {"id":"base","no":"④","name":"기반·자금","sub":"받치는 땅","color":"#b79cff","ax":78,"ay":560,
  "desc":"세 줄을 떠받치는 바닥. 돈을 버는 줄은 아니지만 여기가 흔들리면 위의 셋이 같이 흔들립니다.",
  "nodes":[
   {"id":"grant","n":"정부지원사업","full":"정부지원사업","st":"build","d":"루크 본인은 해당 없고 지영 원장·메이브님·디노·뿌요가 대상. 2026년 해당분 정리와 2027년 도전 리스트(지원금·자격·과제·경쟁률)를 따로 모아 뒀습니다.","href":"../grants/","hl":"정부지원사업 페이지"},
   {"id":"corp","n":"힐링디어스(주)","full":"힐링디어스(주)","st":"on","d":"설립 후 매출 없이 유지된 업력 약 5년 법인. 스칸센 A동 709호는 9/30부로 계약 종료, 새 본점은 비과밀억제권역을 피해 구리 시내 비상주 사무실로 알아보기로 함."},
   {"id":"seoul","n":"서울 이전·건물","full":"서울 이전 · 건물 매입","st":"idea","exp":1,"d":"내년 초 사무실·강의장을 서울로, 현 사무실은 창고·물류 거점으로. 월 렌트가 300~500만을 넘어가면 자체 건물 매입을 검토.","from":"9/29 메이브님 회의"},
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
   {"id":"autoreg","n":"자동등록","full":"자동 상품등록 프로그램","st":"build","exp":1,"d":"상품을 자동으로 등록하는 프로그램. 글자 추출(OCR)은 확장 프로그램 단에서 하고 AI는 추출된 텍스트로 상세페이지만 만드는 구조가 낫다고 봄. 네이버 API 정책·키·IP 차단으로 등록 실패가 나던 건의 원인 진단이 남아 있음.","from":"9/28 회의 · 도구 개발"},
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
 ("beauty","kititi","미용 가격 정보라 지영 원장 쪽과 맞닿음 (확인 필요)"),
 ("beauty","toolbox","오프라인샵 팩과 같은 묶음인지 확인 필요"),
 ("commu","toolbox","자체 사이트·구독 사이트를 같은 스택으로 짓는 구상 (확인 필요)"),
]

def universe_html():
    nodes = [{"id":"luke","n":"루크","full":"루크 (ONE CREW)","st":"on","big":2,"reg":"core","c":"#f0cd84",
              "ax":180,"ay":370,"exp":0,"from":"",
              "d":"다섯 구역이 전부 루크 한 사람을 지나갑니다. 그래서 구역을 늘리는 것보다 각 구역에 사람을 앉히는 것이 먼저입니다."}]
    for R in UNI_REGIONS:
        for N in R["nodes"]:
            nodes.append({"id":N["id"],"n":N["n"],"full":N["full"],"st":N["st"],"big":N.get("big",0),
                          "reg":R["id"],"c":R["color"],"ax":R["ax"],"ay":R["ay"],"d":N["d"],
                          "exp":N.get("exp",0),"from":N.get("from",""),
                          "href":N.get("href",""),"hl":N.get("hl","")})
    data = {
      "nodes": nodes,
      "edges": [{"a":a,"b":b,"l":l} for a,b,l in UNI_EDGES],
      "regions": [{"id":R["id"],"no":R["no"],"name":R["name"],"sub":R["sub"],"color":R["color"],"desc":R["desc"]} for R in UNI_REGIONS],
    }
    body = """
<h1>사업 유니버스</h1>
<p class="note">사업·채널·상품·도구를 점으로 두고, <b>실제로 이어져 있는 관계만 줄로 묶은 관계망</b>입니다. 점을 누르면 그 점과 이어진 것만 남고, 무엇으로 이어져 있는지가 아래에 열립니다. 점을 끌어서 옮길 수도 있습니다. 사람들과의 대화에서 나온 <b>확장 구상</b>도 같이 올렸고, 어디서 나온 이야기인지 각 점에 적어 뒀습니다.</p>

<div class="sky"><svg viewBox="0 0 360 820" id="uniMap" role="img" aria-label="사업 유니버스 관계망" style="font-family:'Noto Sans KR',sans-serif;touch-action:none"></svg></div>
<div class="legend" id="uniLeg">
  <span><i style="background:#f0cd84"></i>루크</span>
  <span><a href="#" data-reg="ch"><i style="background:#4fd1a5"></i>채널·브랜딩</a></span>
  <span><a href="#" data-reg="kn"><i style="background:#e3b04b"></i>지식·교육</a></span>
  <span><a href="#" data-reg="pr"><i style="background:#8fb0ff"></i>상품·유통</a></span>
  <span><a href="#" data-reg="base"><i style="background:#b79cff"></i>기반·자금</a></span>
  <span><a href="#" data-reg="tool"><i style="background:#ff9f7a"></i>도구·자동화</a></span>
</div>
<div class="legend" style="margin-top:-8px">
  <span><i style="background:var(--muted)"></i>채움 = 돌아감</span>
  <span><i style="border:2px solid var(--muted);background:transparent"></i>테두리 = 세우는 중</span>
  <span><i style="border:2px dotted var(--muted);background:transparent"></i>점선 = 구상</span>
  <span><a href="#" id="uniExp">확장 구상만 보기</a></span>
  <span><a href="#" id="uniReset">재배치</a></span>
</div>

<div class="card" id="uniPanel"></div>

<h2>이 관계망 보는 법</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">줄이 곧 사업</div><div class="m">점 세 개가 따로 있으면 부업 셋입니다. 줄로 엮여야 하나가 흔들려도 나머지가 받칩니다 — <a href="../philosophy/">삼각 파이프라인</a>의 핵심</div></li>
    <li><div class="t">가운데 루크에 줄이 몰리는 것이 지금의 병목</div><div class="m">루크에 직접 붙은 줄을 사람에게 넘기는 것이 구역을 늘리는 것보다 먼저입니다</div></li>
    <li><div class="t">⑤ 도구·자동화는 혼자 돈이 되지 않습니다</div><div class="m">만들어서 루크 툴박스 구독으로 묶이거나, 수강생에게 기본판을 풀어 강의 후킹이 될 때 돈이 됩니다. 줄이 툴박스로 모이는 이유</div></li>
    <li><div class="t">'확인 필요'가 붙은 줄</div><div class="m">아직 기록으로 확인되지 않은 연결입니다. 맞는지 알려주시면 확정하거나 지웁니다</div></li>
  </ul>
</div>

<h2>아직 비어 있는 자리</h2>
<div class="card gold">
  <p style="margin:0 0 8px">말씀해주시면 점이든 줄이든 그대로 넣습니다.</p>
  <ul class="list">
    <li><div class="t">오프라인 창고형 매장</div><div class="m">위치·평수·취급 품목·운영 인력·여는 시점. 3PL 재고를 쓰는 건지, 별도 매입인지</div></li>
    <li><div class="t">개인 트레이드 채널</div><div class="m">무엇을 다루는 채널인지, 어느 플랫폼인지</div></li>
    <li><div class="t">10월 말 무료 라이브</div><div class="m">10/25(일) 19:00이 확정인지, 신청 링크</div></li>
    <li><div class="t">빠진 확장 구상</div><div class="m">사람들과 얘기했지만 여기 없는 것. 이름과 한 줄, 누구와 한 이야기인지</div></li>
  </ul>
</div>

<div class="src" style="margin-top:14px">근거: <a href="../roadmap/">돈 버는 로드맵</a> · <a href="../philosophy/">삼각 파이프라인</a> · <a href="../platform/">강의 플랫폼 전략</a> · <a href="../grants/">정부지원사업</a> · 8/25~10/4 노션 액션보드·플라우드 녹음·클로드 대화 기록. 확장 구상 점에는 어느 대화에서 나온 것인지 적어 두었습니다. 금액은 모두 계획값이며 실적이 아닙니다.</div>

<script>
(function(){
var D = __DATA__;
var W=360, H=820, svg=document.getElementById('uniMap'), panel=document.getElementById('uniPanel');
var NS='http://www.w3.org/2000/svg';
var N={}, nodes=D.nodes, edges=D.edges, regs={};
D.regions.forEach(function(r){regs[r.id]=r;});
regs.core={id:'core',no:'',name:'루크',sub:'',color:'#f0cd84',desc:'다섯 구역이 전부 여기를 지나갑니다.'};
var seed=20261005;
function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff;}
function place(){
  nodes.forEach(function(n){ n.x=n.ax+(rnd()-0.5)*110; n.y=n.ay+(rnd()-0.5)*110; n.vx=0; n.vy=0; });
}
nodes.forEach(function(n){ N[n.id]=n; n.r=n.big===2?16:(n.big===1?8:6); n.deg=0; n.adj=[]; n.hw=Math.min(n.n.length*4.7+4, 62); });
edges.forEach(function(e){
  var a=N[e.a], b=N[e.b]; if(!a||!b) return;
  a.deg++; b.deg++; a.adj.push({id:e.b,l:e.l}); b.adj.push({id:e.a,l:e.l});
  e.t = rnd();
});
place();
function tick(k){
  for(var i=0;i<nodes.length;i++){ for(var j=i+1;j<nodes.length;j++){
    var a=nodes[i], b=nodes[j], dx=b.x-a.x, dy=b.y-a.y, d2=dx*dx+dy*dy;
    if(d2<1) d2=1; var d=Math.sqrt(d2);
    var f=2200/d2; if(f>3) f=3;
    var ux=dx/d, uy=dy/d;
    a.vx-=ux*f; a.vy-=uy*f; b.vx+=ux*f; b.vy+=uy*f;
    var min=a.r+b.r+20;
    if(d<min){ var p=(min-d)*0.5; a.vx-=ux*p; a.vy-=uy*p; b.vx+=ux*p; b.vy+=uy*p; }
  }}
  edges.forEach(function(e){
    var a=N[e.a], b=N[e.b]; if(!a||!b) return;
    var dx=b.x-a.x, dy=b.y-a.y, d=Math.sqrt(dx*dx+dy*dy)||1;
    var f=(d-74)*0.012, ux=dx/d, uy=dy/d;
    a.vx+=ux*f; a.vy+=uy*f; b.vx-=ux*f; b.vy-=uy*f;
  });
  nodes.forEach(function(n){
    n.vx += (n.ax-n.x)*0.006; n.vy += (n.ay-n.y)*0.006;
    if(n.id==='luke'){ n.vx += (180-n.x)*0.05; n.vy += (370-n.y)*0.05; }
    if(n.drag) { n.vx=0; n.vy=0; return; }
    n.vx*=0.80; n.vy*=0.80;
    n.x+=n.vx*k; n.y+=n.vy*k;
    var mx=Math.max(n.r+10, n.hw+6), my=n.r+16;
    if(n.x<mx) n.x=mx; if(n.x>W-mx) n.x=W-mx;
    if(n.y<my+10) n.y=my+10; if(n.y>H-my-18) n.y=H-my-18;
  });
}
function settle(){ for(var s=0;s<620;s++) tick(1); }
settle();

function el(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);return e;}
var gEdge=el('g',{}), gPulse=el('g',{}), gNode=el('g',{});
svg.appendChild(gEdge); svg.appendChild(gPulse); svg.appendChild(gNode);
edges.forEach(function(e){
  e.el = el('line',{'stroke':'#7fa8bd','stroke-width':'1','stroke-linecap':'round','opacity':'.38'});
  gEdge.appendChild(e.el);
  e.p = el('circle',{'r':'1.8','fill':'#dff6ef','opacity':'.8'});
  gPulse.appendChild(e.p);
});
nodes.forEach(function(n){
  var g=el('g',{'class':'uni-nd','style':'cursor:pointer'});
  var at={'r':n.r,'fill':n.c};
  if(n.st==='build'){at={'r':n.r,'fill':'#0c1a20','stroke':n.c,'stroke-width':'2'};}
  if(n.st==='idea'){at={'r':n.r,'fill':'#0c1a20','stroke':n.c,'stroke-width':'1.6','stroke-dasharray':'2 2.4'};}
  if(n.id==='luke'){at={'r':n.r,'fill':'#ffe9b8','stroke':'#e3b04b','stroke-width':'2'};}
  n.halo = el('circle',{'r':n.r+7,'fill':n.c,'opacity':'0'});
  n.c1 = el('circle',at);
  n.t1 = el('text',{'text-anchor':'middle','font-size':n.big?'10':'9','fill':'#e8eef2','class':'lu-lab'});
  n.t1.textContent=n.n;
  n.hit = el('circle',{'r':Math.max(n.r+10,14),'fill':'transparent'});
  g.appendChild(n.halo); g.appendChild(n.c1); g.appendChild(n.t1); g.appendChild(n.hit);
  gNode.appendChild(g); n.g=g;
});
function draw(){
  edges.forEach(function(e){
    var a=N[e.a], b=N[e.b];
    e.el.setAttribute('x1',a.x); e.el.setAttribute('y1',a.y);
    e.el.setAttribute('x2',b.x); e.el.setAttribute('y2',b.y);
    e.t += 0.003; if(e.t>1) e.t-=1;
    e.p.setAttribute('cx', a.x+(b.x-a.x)*e.t); e.p.setAttribute('cy', a.y+(b.y-a.y)*e.t);
  });
  nodes.forEach(function(n){
    n.halo.setAttribute('cx',n.x); n.halo.setAttribute('cy',n.y);
    n.c1.setAttribute('cx',n.x); n.c1.setAttribute('cy',n.y);
    n.hit.setAttribute('cx',n.x); n.hit.setAttribute('cy',n.y);
    n.t1.setAttribute('x',n.x); n.t1.setAttribute('y',n.y+n.r+10);
  });
}
var reduce=false;
try{ reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){}
function loop(){ tick(0.35); draw(); if(!reduce) requestAnimationFrame(loop); }
draw(); if(!reduce) requestAnimationFrame(loop);

var ST={on:['돌아감','p0'],build:['세우는 중','p1'],idea:['구상','p2']};
var sel=null, filt=null;
function apply(){
  var keep=null;
  if(sel){ keep={}; keep[sel]=1; N[sel].adj.forEach(function(a){keep[a.id]=1;}); }
  else if(filt==='exp'){ keep={}; nodes.forEach(function(n){ if(n.exp) keep[n.id]=1; }); keep['luke']=1; }
  else if(filt){ keep={}; nodes.forEach(function(n){ if(n.reg===filt) keep[n.id]=1; }); keep['luke']=1; }
  nodes.forEach(function(n){
    var on = !keep || keep[n.id];
    n.g.style.opacity = on? '1':'.12';
    n.halo.setAttribute('opacity', (sel===n.id)?'.35':'0');
  });
  edges.forEach(function(e){
    var on = sel ? (e.a===sel||e.b===sel) : (!keep || (keep[e.a] && keep[e.b]));
    e.el.setAttribute('opacity', on? (sel?'.9':'.38') : '.04');
    e.el.setAttribute('stroke', (sel && on)? N[sel].c : '#7fa8bd');
    e.el.setAttribute('stroke-width', (sel && on)? '1.8':'1');
    e.p.setAttribute('opacity', on? '.8':'0');
  });
}
function lk(n){ return '<a href="#" data-go="'+n.id+'">'+n.n+'</a>'; }
function home(){
  sel=null; filt=null; apply();
  var ex=nodes.filter(function(n){return n.exp;});
  var h='<h3>관계망 전체</h3><p class="note" style="margin-top:0">점 '+nodes.length+'개 · 줄 '+edges.length+'개. 그중 대화에서 나온 확장 구상이 '+ex.length+'개입니다 — <a href="#" data-f="exp">확장 구상만 보기</a></p><ul class="list">';
  D.regions.forEach(function(r){
    var ns=nodes.filter(function(n){return n.reg===r.id;});
    h+='<li><div class="t"><a href="#" data-f="'+r.id+'" style="color:'+r.color+'">'+r.no+' '+r.name+'</a></div><div class="m">'+ns.map(lk).join(' · ')+'</div></li>';
  });
  var top=nodes.slice().sort(function(a,b){return b.deg-a.deg;}).slice(0,4);
  h+='</ul><div class="note">줄이 가장 많이 몰린 곳: '+top.map(function(n){return lk(n)+' '+n.deg;}).join(' · ')+'</div>';
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
  h+='</ul><p class="note"><a href="#" data-go="home">← 관계망 전체</a></p>';
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
  h+='</ul><p class="note"><a href="#" data-go="home">← 관계망 전체</a></p>';
  panel.innerHTML=h;
}
function show(id){
  var n=N[id]; if(!n) return home();
  sel=id; filt=null; apply();
  var r=regs[n.reg];
  var h='<span class="tag '+ST[n.st][1]+'">'+ST[n.st][0]+'</span><span class="tag" style="color:'+r.color+';border-color:'+r.color+'">'+(r.no?r.no+' ':'')+r.name+'</span>';
  h+='<h3 style="margin-top:8px">'+n.full+'</h3><p style="margin-bottom:8px">'+n.d+'</p>';
  if(n['from']) h+='<div class="note" style="margin-bottom:8px">어디서 나온 이야기: '+n['from']+'</div>';
  if(n.href) h+='<p style="margin-bottom:8px"><a href="'+n.href+'">'+n.hl+' →</a></p>';
  h+='<h3 style="margin-top:12px">이어진 것 '+n.adj.length+'개</h3><ul class="list">';
  n.adj.forEach(function(a){
    var m=N[a.id];
    h+='<li><div class="t"><a href="#" data-go="'+a.id+'" style="color:'+m.c+'">'+m.full+'</a></div><div class="m">'+a.l+'</div></li>';
  });
  h+='</ul><p class="note"><a href="#" data-f="'+n.reg+'">← '+r.name+'</a> · <a href="#" data-go="home">관계망 전체</a></p>';
  panel.innerHTML=h;
}
function route(e){
  var a=e.target.closest?e.target.closest('[data-go],[data-f],[data-reg]'):null;
  if(!a) return; e.preventDefault();
  var g=a.getAttribute('data-go'), f=a.getAttribute('data-f')||a.getAttribute('data-reg');
  if(g==='home') home();
  else if(g) show(g);
  else if(f==='exp') showExp();
  else if(f) showReg(f);
  panel.scrollIntoView({block:'nearest'});
}
panel.addEventListener('click',route);
document.getElementById('uniLeg').addEventListener('click',route);
document.getElementById('uniExp').addEventListener('click',function(e){e.preventDefault();showExp();panel.scrollIntoView({block:'nearest'});});
document.getElementById('uniReset').addEventListener('click',function(e){
  e.preventDefault(); seed=20261005; place(); settle(); draw();
});
var drag=null, moved=0, pt=svg.createSVGPoint();
function loc(ev){ pt.x=ev.clientX; pt.y=ev.clientY; var m=svg.getScreenCTM(); return m?pt.matrixTransform(m.inverse()):{x:0,y:0}; }
function hitNode(p){
  var best=null, bd=1e9;
  nodes.forEach(function(n){ var d=(n.x-p.x)*(n.x-p.x)+(n.y-p.y)*(n.y-p.y); var rr=Math.max(n.r+10,14); if(d<rr*rr && d<bd){bd=d;best=n;} });
  return best;
}
svg.addEventListener('pointerdown',function(ev){
  var p=loc(ev), n=hitNode(p); if(!n) return;
  drag=n; n.drag=1; moved=0; svg.setPointerCapture(ev.pointerId); ev.preventDefault();
});
svg.addEventListener('pointermove',function(ev){
  if(!drag) return; var p=loc(ev);
  moved += Math.abs(p.x-drag.x)+Math.abs(p.y-drag.y);
  drag.x=p.x; drag.y=p.y; draw(); ev.preventDefault();
});
svg.addEventListener('pointerup',function(ev){
  if(!drag) return; var n=drag; n.drag=0; drag=null;
  if(moved<6) show(n.id);
  try{svg.releasePointerCapture(ev.pointerId);}catch(e){}
});
svg.addEventListener('pointercancel',function(){ if(drag){drag.drag=0;drag=null;} });
home();
})();
</script>
"""
    return body.replace("__DATA__", json.dumps(data, ensure_ascii=False))

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
  <ul><li>전체 항목의 할 일·기한·상태·[결정] (10/5 06:40 조회). 미완료·기한 있는 항목은 일정에, 최근 7일 새 항목은 우선순위에 반영. 목표가 '사업 외 개인'인 항목은 넣지 않음(상표권 제외)</li>
  <li>10/1 새로 만든 항목 9건: 박태경 대표님 지원 5건(플라우드 9/30), 사무실 임대료 정산·서울 이전 로드맵·트레이드 채널·'하루를 4번 쓰는 법' 영상(플라우드 9/29). 뒤 4건의 기한은 추정이라 '확인 필요'로 표시</li>
  <li>10/2 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/1에 노션에 새로 생긴 기한 항목 7건을 일정에 추가(상표 출원·키티티 사이트·지원사업 3건·전자책·수파베이스) · 최근 [결정]에 10/1 결정 2건 반영 · 플라우드는 10/1~10/2 새 녹음이 없어 노션에 새로 만든 항목 0건 (9/30 녹음의 루크 담당 Action Item은 이미 액션보드에 있음)</li>
  <li>10/3 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/2에 노션에 새로 생긴 기한 항목 9건을 일정에 추가(평생컨설팅 문의·상품소싱 시트·마진메이커·힐링디어스 본점·회식·키티티 피드백 2건·멘토루크 블로그·법인 결정) · 플라우드 10/2 녹음 4건에서 노션 새 항목 7건(소싱 멘토링 6건 + 무료 라이브 선물 준비 1건), 기한은 노트 기재값·추정이라 '확인 필요' · 최근 [결정]에 10/2 마진메이커 결정 반영 · 7일이 지난 진행 중 항목 3건은 '새 항목' 표시를 뗌</li>
  <li>10/4 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/3에 노션에 새로 생긴 기한 항목 2건을 일정에 추가(원크루 상담 리포트 링크 발송 10/4 · 재문의 확인 10/17) · 우선순위 '새 항목'에 4건 추가, 7일 지난 1건(셀수다 설치)은 일반 줄로 · 최근 [결정] 맨 위에 10/4 통합 보고 구조 · 플라우드 10/3 녹음 1건(원크루 상담)에서 노션 새 항목 0건 · 상황판 보고 피드: 어제 이후 새 보고 0건(피드의 2건은 9/30·10/1자이고 노션에 이미 완료로 있음), 막힘 0건</li>
  <li>10/5 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건(윤지영 원장 개업연월일 확인) 제거 · 10/4~10/5에 노션에 새로 생긴 기한 항목 27건을 일정에 추가(6기 무료 라이브 준비 4건 · 키티티 AI 뷰티 플랫폼 15건 · 헤메네일 5건 · 맥북 교체 · Vercel Pro 결정 · 원크루 사이트 4단계) · 우선순위 '새 항목'에서 완료 2건(카카오맵 JS키·개업연월일 확인) 빼고 새 묶음 10줄 추가 · 최근 [결정] 6개를 10/4~10/5 결정으로 교체 · 무료 라이브 날짜 10/25는 10/4 [결정]으로 확정 표시(시간·신청 링크는 확인 필요) · 플라우드 10/3 인터뷰 녹음 1건에서 노션 새 항목 0건 · 상황판: 노션 [보고] 5건 중 1건(메이크업헬퍼 AI 기술 5가지 제안)을 피드에 새로 옮김 — 나머지 4건은 클로드 코드가 이미 직접 올린 보고와 같은 일이라 그대로 둠 · 허브 맨 위에 [결정 필요] 2건(헤메네일 카카오 미등록 매장 순위 · 키티티 정부지원 방식). 피드의 '막힘' 중 키티티 도메인 구매·원크루 Supabase 한도는 뒤이은 완료 보고·노션 [결정]으로 해결된 것으로 확인돼 올리지 않음</li></ul>
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
