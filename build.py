# -*- coding: utf-8 -*-
"""내 연봉 10억 만들기 — 정적 페이지 빌드 스크립트.
python3 build.py 실행 시 index.html 과 하위 폴더 index.html 을 전부 새로 씁니다.
(부분 수정 금지 원칙: 매번 파일 전체를 다시 생성)"""
import json, os, datetime

UPDATED = "2026-09-30"
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
# who: 루크 / 메이브님 / 디노 / 뿌요 / 지영 / 리나님(물류)
EVENTS = [
  # 9월 말
  {"d":"2026-09-30","t":"뷰셀 2화 대본 제공 (화장품 10년 트렌드·성분·브랜드)","who":"루크→메이브님","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-09-30","t":"물류 업데이트/운영 책임자 지정 + 현안 이슈 보드 시작 [설명서]","who":"뿌요·루크","p":"P0","g":"logistics-stabilize","cash":False},
  {"d":"2026-09-30","t":"잔디 이슈 채널 운영 규칙(이슈 템플릿·상태 태그)","who":"루크","p":"P1","cash":False},
  # 10월 첫째 주
  {"d":"2026-10-02","t":"개발자 계정 3종 등록 — Apple Developer($99/년) · Google Play($25 1회) · Microsoft Store(무료) [설명서]","who":"루크","p":"P0","cash":True,"g":"developer-accounts"},
  {"d":"2026-10-03","t":"초이스토리 PD 화상 미팅 — 3자 구도(모객) 제안 [설명서]","who":"루크·메이브님","p":"P0","cash":True,"g":"platform-pd-meeting"},
  {"d":"2026-10-01","t":"3PL 수강생 재고 당근·외부 판매 — 첫 등록 (동의서·시트·비즈프로필) [설명서]","who":"루크·루나","p":"P0","g":"3pl-resale","n":"https://app.notion.com/p/3de0cf8fea0481b2a948d2dc4f7802ed","cash":True},
  {"d":"2026-10-01","t":"키티티바이지영 상표권 출원 (KIPRIS 선행검색 → 출원, 30분)","who":"루크·지영","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea0481eda6d9db338d52c92c","cash":False},
  {"d":"2026-10-01","t":"물류 삭제/무효화 임시 규칙 + 핸드오버 체크리스트","who":"루크·뿌요","p":"P1","cash":False},
  {"d":"2026-10-01","t":"지영 인스타 주간 운영 캘린더 시작","who":"지영","p":"P1","cash":False},
  {"d":"2026-10-02","t":"뷰셀 2화 촬영 (공개 10/7)","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-10-02","t":"물류·전산 전체 프로세스 맵 + 병목 표시","who":"뿌요","p":"P1","cash":False},
  {"d":"2026-10-03","t":"물류 중복·충돌 기능 정리 우선순위","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-04","t":"디노(미니쌤) 12주 빌드업안 전달·합의 (PDF 『미니쌤, 12주의 지도』) [설명서]","who":"루크→디노","p":"P0","g":"dino-12weeks","n":"https://app.notion.com/p/3e90cf8fea048120bd88de7b8953d9dc","cash":True},
  {"d":"2026-10-04","t":"물류 표준 운영 가이드 배포 / 피크일(월·화) 택배 우선 운영안","who":"루크·뿌요","p":"P1","cash":False},
  {"d":"2026-10-05","t":"디노 12주 프로그램 1주차 시작 (AI 셀러 실무 교육 빌드업)","who":"디노","p":"P0","n":"https://app.notion.com/p/3e90cf8fea048120bd88de7b8953d9dc","cash":True},
  {"d":"2026-10-05","t":"리나님 시간 기록 시트 1~2주 시범 운영 (매일 퇴근 전 피드백)","who":"리나님·루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea0481f386b9d5f0d96feb05","cash":False},
  {"d":"2026-10-05","t":"키티티 상담 사이트 원장님 확인 (사진 동의·한마디·비포애프터)","who":"지영","p":"P1","n":"https://app.notion.com/p/3e90cf8fea0481d2aa25e18cf01f6b09","cash":False},
  {"d":"2026-10-05","t":"영상공장 API 키 5개 발급 + 목소리 1~3분 녹음","who":"루크","p":"P1","n":"https://app.notion.com/p/3e90cf8fea048106ab46ee6d7425f2c8","cash":False},
  {"d":"2026-10-06","t":"수강생 화장품법 소송 대응 지원 — 답변서 기한·변호사 연결 (익명)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ea0cf8fea048198857ef162cf15ad7a","cash":False},
  {"d":"2026-10-06","t":"물류 CS 포인트 분석 + 사전 안내 스크립트 정비","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"뷰셀 2화 공개 (수)","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea04810db76ac350033501af","cash":False},
  {"d":"2026-10-07","t":"물류 권한 재설계 + 감사 로그","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"지영 예약·매출 간단 대시보드 완료 목표","who":"지영","p":"P2","cash":False},
  {"d":"2026-10-08","t":"종혁 본부장 미팅 — 신규 강의 플랫폼 1:1:1 역할·수익 배분안 제시 [설명서]","who":"루크·메이브님","p":"P0","g":"platform-director-meeting","cash":True},
  {"d":"2026-10-08","t":"지영 미팅 — 정부지원사업 후보 3개 + 사업계획서 초안 리뷰","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-08","t":"사진 기반 입고/검수 자동화 플로우 설계","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-10","t":"물류 선반 추가·라벨링·박스 재배치","who":"뿌요","p":"P2","cash":False},
  {"d":"2026-10-15","t":"미입고 자동 알림·반품 트리거 프로토타입","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-15","t":"지영 내년 조달(최소 1억) 월별 마일스톤 확정","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-31","t":"10월 말 무료 라이브 — 날짜·시간·신청 링크 확인 필요 (록터뷰 영상에 링크) [설명서]","who":"루크","p":"P0","g":"free-live","n":"https://app.notion.com/p/3e90cf8fea048171ac6bd0e23e1c5669","cash":True},
  {"d":"2026-11-30","t":"메이크업헬퍼 12주 테스트 9주차 판정 (11월 말)","who":"루크·최은봉","p":"P1","cash":True},
  {"d":"2026-12-31","t":"루크 툴박스 구독 500명 목표 / 3PL 판매 실적 정리(내년 강의 증거)","who":"루크","p":"P1","cash":True},
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
    <li data-g="developer-accounts"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 (Apple · Google Play · Microsoft)</div><div class="m">툴박스·영상공장·블로그타이퍼를 폰·맥·윈도우로 배포하는 모든 일의 앞단. Apple은 승인에 며칠 걸리므로 오늘 시작 · 기한 10/2</div></li>
    <li data-g="platform-pd-meeting"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 3자 구도 — PD 미팅 → 10/8 본부장 미팅</div><div class="m">플레이어·강사교육 = 루크·메이브님 / 락인(챌린지 영상·네이버 카페·광고) = 종혁 본부장 / 모객 = 초이스토리 PD · <a href="platform/">전략 페이지</a></div></li>
    <li data-g="3pl-resale"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">3PL 수강생 재고 당근·외부 판매 첫 등록</div><div class="m">동의서(수수료 15~20%) → 재고 시트 판매 열 + 사진 → 당근 비즈프로필 → 30개 등록 · 통신판매업 신고 사업자 명의 필수 · 기한 10/1</div></li>
    <li data-g="dino-12weeks"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">디노(미니쌤) 12주 빌드업 합의 → 10/5 1주차 시작</div><div class="m">AI 셀러 실무 교육 · 1달 90 / 2달 200 / 3달 350만 기준 · 상품별 배분 비율 확정</div></li>
    <li data-g="onecrew-inquiry"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">원크루·툴박스 문의 대응 — 가격 안내 후 상담 통화</div><div class="m">원크루 정가 3,900만 / 수강생 출신 3,300만 · 일십백천 990만 · 툴박스 사전 신청 안내 문구 확정</div></li>
    <li data-g="free-live"><span class="tag p0">P0</span><div class="t">10월 말 무료 라이브 날짜·신청 링크 확정</div><div class="m">록터뷰 2회차 영상 설명란·고정댓글에 링크 → 신규 리스트 확보 · <b>날짜 확인 필요</b></div></li>
  </ul>
</div>

<h2>페이지</h2>
<div class="grid nav">
  <a href="roadmap/"><b>돈 버는 로드맵</b><span>수익 줄 · 3단계 · 원칙</span></a>
  <a href="priority/"><b>우선순위</b><span>P0 → P3 · 보류 목록</span></a>
  <a href="people/"><b>사람별 현황</b><span>메이브님·디노·뿌요·지영</span></a>
  <a href="schedule/"><b>일정 도식</b><span>10월 타임라인 · 마일스톤</span></a>
  <a href="philosophy/"><b>삼각 파이프라인</b><span>원크루 · 일십백천 · 불씨 이론</span></a>
  <a href="platform/"><b>강의 플랫폼 전략</b><span>유입 · 락인 · 플레이어 3자 구도</span></a>
  <a href="guides/"><b>할 일 설명서</b><span>항목별 어떻게 하는지 단계별</span></a>
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
const over = EVENTS.filter(e=>dayN(e.d)<0 && dayN(e.d)>=-14);
const td = EVENTS.filter(e=>e.d===today);
const up = EVENTS.filter(e=>dayN(e.d)>0 && dayN(e.d)<=3);
function li(e,label){return '<li data-n="'+(e.n||'')+'" data-g="'+(e.g||'')+'"><span class="tag '+P[e.p]+'">'+e.p+'</span>'+(e.cash?'<span class="tag cash">현금</span>':'')+(label?'<span class="tag">'+label+'</span>':'')+'<div class="t">'+e.t+'</div><div class="m">'+e.who+' · '+e.d.slice(5).replace('-','/')+'</div></li>';}
let html='';
if(td.length) html+='<h3>오늘</h3><ul class="list tasks">'+td.map(e=>li(e)).join('')+'</ul>';
if(over.length) html+='<h3 style="margin-top:12px">지난 기한 (밀린 것부터)</h3><ul class="list tasks">'+over.sort((a,b)=>a.d<b.d?-1:1).map(e=>li(e,'D'+dayN(e.d))).join('')+'</ul>';
if(up.length) html+='<h3 style="margin-top:12px">다가오는 3일</h3><ul class="list tasks">'+up.sort((a,b)=>a.d<b.d?-1:1).map(e=>li(e,'D+'+dayN(e.d))).join('')+'</ul>';
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
<p class="note">기준: 현금에 가깝고 다른 일의 선행 조건일수록 위. 기한은 노션 액션보드 기준. [결정]은 완료로, [보류]는 P3로.</p>

<h2>P0 · 이번 주 <small>~10/5</small></h2>
<div class="card red">
  <ul class="list tasks">
    <li data-g="developer-accounts"><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 — Apple Developer / Google Play / Microsoft Store</div><div class="m">기한 10/2 · 앱 배포(툴박스 PWA→앱, 영상공장, 블로그타이퍼) 전부의 앞단. 루크가 "제일 높은 등급"으로 지정(9/30)</div></li>
    <li data-g="platform-pd-meeting"><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 3자 구도 — 초이스토리 PD 미팅(모객) → 10/8 종혁 본부장(락인)</div><div class="m"><a href="../platform/">전략 페이지</a> · 나머지 우선순위는 이 둘의 결과에 따라 달라짐(루크 9/30)</div></li>
    <li><span class="tag cash">현금</span><div class="t">3PL 수강생 재고 당근·외부 판매 — 2주 내 첫 등록</div><div class="m">기한 10/1 · 동의서 → 시트·사진 → 당근 비즈프로필 → 30개 등록 → 광고 10만 테스트</div></li>
    <li><span class="tag cash">현금</span><div class="t">디노 12주 빌드업안 전달·합의 (10/4) → 10/5 1주차</div><div class="m">상품별 배분 비율 확정 · 1주차 콘셉트 3안 중 선택</div></li>
    <li><span class="tag cash">현금</span><div class="t">원크루 문의(오픈채팅) 가격 안내 + 상담 통화</div><div class="m">3,900만 / 3,300만 · 신한카드 네이버페이 60개월 '세팅 가능'으로 표현</div></li>
    <li><span class="tag cash">현금</span><div class="t">툴박스 구독권 오픈일·가격·사전 신청 안내 문구</div><div class="m">토스페이먼츠 심사 전이라 사전 신청 형태</div></li>
    <li><div class="t">10월 말 무료 라이브 날짜·시간·신청 링크</div><div class="m">록터뷰 2회차 영상에 링크 · 날짜 확인 필요</div></li>
    <li><div class="t">뷰셀 유튜브 2화 — 대본 9/30 · 촬영 10/2 · 공개 10/7</div><div class="m">담당 메이브님 · 3화는 실제 상품 마진 계산</div></li>
    <li><div class="t">물류 안정화 — 책임자 단일화(9/30), 삭제/무효화 임시 규칙(10/1), 프로세스 맵(10/2), 운영 가이드(10/4)</div><div class="m">입고 미처리 상태에서 운송장 출력되는 오류 긴급 대응</div></li>
    <li><div class="t">키티티바이지영 상표권 출원 (10/1, 30분)</div><div class="m">등록 1년 이상 소요 → 2월 오픈 역산 마지노선</div></li>
    <li><div class="t">수강생 화장품법 소송 초동 대응 지원 (10/6)</div><div class="m">답변서 기한·변호사 연결 · 대응 전자책 20쪽 완성됨</div></li>
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
    <li><div class="t">메이크업헬퍼 — 계약서 수정본·공급가 재협상 전달, 12주 테스트 착수</div></li>
    <li><div class="t">리나님 시간 기록 시트 2주 시범 → 크롬 확장 설계</div></li>
    <li><div class="t">영상공장 API 키 5개 + 목소리 녹음 → 첫 실제 영상</div></li>
    <li><div class="t">인스타 크리에이터 계정 전환 + 마케팅 업체 채널 인계 (유튜브 편집자 권한·틱톡 신규 계정)</div></li>
    <li><div class="t">디노 AI 영상(힉스필드) 학습 기록 → 무료 전자책 → 유료 전자책 파이프라인</div></li>
  </ul>
</div>

<h2>P2 · 다음 달 말</h2>
<div class="card">
  <ul class="list tasks">
    <li><div class="t">사진 기반 입고/검수 자동화 (설계 10/8 → 프로토타입 10/15)</div></li>
    <li><div class="t">물류 권한 재설계·감사 로그 · 선반·라벨링 · CS 스크립트</div></li>
    <li><div class="t">개인 트레이드 채널 개설·운영 (9/29 액션)</div></li>
    <li><div class="t">'하루를 4번 쓰는 법' 영상 — 6h×4 슬롯 7일 파일럿 후 대본·촬영</div></li>
    <li><div class="t">서울 이전·건물 매입 대비 로드맵 (내년 초)</div></li>
    <li><div class="t">전화 상담 AI — 100건 통화 녹음 분석 (내 목소리 엔진 연계)</div></li>
  </ul>
</div>

<h2>P3 · 보류</h2>
<div class="card">
  <ul class="list">
    <li><span class="tag p3">보류</span><div class="t">새 사이트·앱 개발, 새 강의 시리즈, 셀러 OS — 10월 정산 확인 전까지</div></li>
    <li><span class="tag p3">보류</span><div class="t">개발자 채용 — 구독자 수 기준으로 판단, 우선 PWA</div></li>
    <li><span class="tag p3">보류</span><div class="t">사업가·자기계발용 핸드폰 앱(동기부여) — 6개월 후 단독 구독 검토</div></li>
    <li><span class="tag p3">보류</span><div class="t">깃허브 저장소 전부 Private 전환 (Pages 유지하려면 Pro 필요)</div></li>
  </ul>
</div>

<h2>최근 [결정]</h2>
<div class="card accent">
  <ul class="list">
    <li><span class="tag done">결정</span><div class="t">신규 파이프라인 = 1인 AI 소프트웨어 스튜디오 → 가격은 소액 대량, 툴박스 구독 하나로 통합</div></li>
    <li><span class="tag done">결정</span><div class="t">보유 현금 배분 — 재고·개발 0, 런칭 광고에만</div></li>
    <li><span class="tag done">결정</span><div class="t">영상공장은 배포용 데스크톱 앱(각자 자기 키)</div></li>
    <li><span class="tag done">결정</span><div class="t">록터뷰 2회차는 시연형 · 뷰셀 2화 주제 변경(트렌드·성분·브랜드)</div></li>
    <li><span class="tag done">결정</span><div class="t">메이크업헬퍼 12주 5단계·손절선 (누적 광고적자 50만 정지)</div></li>
    <li><span class="tag done">결정</span><div class="t">메이브님: GPT 해지 → 클로드·캔바 유료 (9/29)</div></li>
  </ul>
</div>
"""

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
    <dt>다음</dt><dd>상표권 출원(10/1) · 인스타 주간 캘린더(10/1) · 상담 사이트 원장 확인(10/5) · 대시보드(10/7) · 10/8 미팅(지원사업 후보 3개·사업계획서 초안) · 조달 마일스톤(10/15) · 샵 2월 오픈</dd>
  </dl>
</div>

<h2>그 외</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">루나</div><div class="m">콘텐츠 제작·발행 총괄. 3PL 재고 사진 촬영 담당. 가장 레버리지 큰 팀원</div></li>
    <li><div class="t">리나님 (물류)</div><div class="m">시간 기록 시트 2주 시범(9/29~10/12) → 크롬 확장 설계</div></li>
    <li><div class="t">박태경 대표 (원크루)</div><div class="m">3회차 컨설팅 진행 중 · 100문100답 세션 내 공동 작성 · 결정 규칙표·손절 규칙표</div></li>
    <li><div class="t">최은봉 대표 (원크루) — 메이크업헬퍼</div><div class="m">위탁판매 계약서 수정본·공급가 재협상 · 12주 테스트 설계서 · 당근 1순위, 토스 2순위</div></li>
    <li><div class="t">종혁 본부장 / 초이스토리 PD</div><div class="m">신규 강의 플랫폼 협업 후보. PD 먼저, 본부장 10/8</div></li>
  </ul>
</div>
"""

# ---------------------------------------------------------------- 일정
def timeline_html():
    out = []
    for e in EVENTS:
        cls = "big" if e["cash"] else ""
        d = datetime.date.fromisoformat(e["d"])
        wd = "월화수목금토일"[d.weekday()]
        out.append(f'<li class="{cls}"><div class="d">{e["d"][5:].replace("-","/")} ({wd}) · {e["who"]} · {e["p"]}</div><div class="t">{e["t"]}</div></li>')
    return "\n".join(out)

SCHEDULE = f"""
<h1>일정 도식</h1>
<p class="note">확정·기한이 있는 것만. 금색 점은 현금에 직접 닿는 일. 날짜가 없는 일은 <a href="../priority/">우선순위</a>에.</p>

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

<h2>10월 타임라인</h2>
<div class="card">
  <ul class="tl">
    {timeline_html()}
  </ul>
</div>

<h2>마일스톤</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">10/8 · 신규 강의 플랫폼 3자 구도 결정</div><div class="bar"><i style="width:30%"></i></div><div class="m">PD 접촉 → 본부장 미팅 → 배분안 합의</div></li>
    <li><div class="t">10월 말 · 무료 라이브 → 신규 리스트</div><div class="bar"><i style="width:20%"></i></div><div class="m">록터뷰 2회차 촬영 완료, 날짜 미정</div></li>
    <li><div class="t">11월 말 · 메이크업헬퍼 9주차 판정</div><div class="bar"><i style="width:15%"></i></div><div class="m">계약서·설계서 완료, 공급가 재협상 중</div></li>
    <li><div class="t">12월 · 툴박스 500명</div><div class="bar"><i style="width:10%"></i></div><div class="m">사이트 구축 완료, 결제 심사·공개 문구 남음</div></li>
    <li><div class="t">2027 2월 · 키티티 샵 오픈</div><div class="bar"><i style="width:25%"></i></div><div class="m">상표권 출원 10/1이 마지노선</div></li>
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

# ---------------------------------------------------------------- 할 일 설명서
GUIDES = [
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
 {"slug":"platform-pd-meeting","title":"초이스토리 PD 화상 미팅 (모객 축 제안)","p":"P0","due":"이번 주","why":"3자 구도의 첫 단추. PD가 모객을 맡아주면 10/8 본부장 미팅에서 완성형을 제시할 수 있다.",
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
 {"slug":"free-live","title":"10월 말 무료 라이브 확정","p":"P0","due":"확인 필요","why":"록터뷰 2회차 영상에 신청 링크가 들어가야 신규 리스트가 생긴다. 날짜가 없으면 영상 설명란도 못 쓴다.",
  "prep":["10월 마지막 주 저녁 중 비는 날 2개","네이버 폼 또는 기존 신청 폼 템플릿(추석 특강 때 naver.me 링크 방식)"],
  "steps":[
   ("날짜·시간 확정","10월 마지막 주 평일 저녁 1회(예비 1회). 캘린더에 박기."),
   ("신청 폼 만들기","추석 특강 폼 복제 → 제목·날짜만 교체. 연락처 필수."),
   ("링크 배치","록터뷰 영상 설명란·고정댓글, 카톡방, 카페 공지, 인스타 프로필."),
   ("흐름 유지","라이브 당일 무료 → 7일 다시보기 → 이후 유튜브 멤버십 전용."),
  ],
  "done":"날짜·폼 링크가 노션에 있고 록터뷰 영상 설명란에 들어감.",
  "src":["노션 '10월 말 무료 라이브 날짜·시간·신청 링크 확정' (9/28)"]},
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

# ---------------------------------------------------------------- 출처
SOURCES = """
<h1>출처 · 갱신 방법</h1>

<h2>이 페이지의 근거</h2>
<div class="card src">
  <p>모든 숫자·날짜·이름은 루크 본인의 기록에서 가져왔습니다. 외부 검색으로 확인한 사실은 없으며, 계획값은 실적이 아닙니다.</p>
  <h3>플라우드 녹음 (요약 노트)</h3>
  <ul>
    <li>09-29 메이븐 — 신규 강의 플랫폼 사업 구상 및 전략 수립 회의</li>
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
  <ul><li>9/14~9/29 항목의 할 일·기한·상태·[결정]</li></ul>
  <h3>프로젝트 기록</h3>
  <ul><li>내 연봉 10억 만들기 프로젝트의 overview · principles · ways-of-working · luke-toolbox · 3pl-service</li></ul>
</div>

<h2>갱신 방법</h2>
<div class="card">
  <ul class="list">
    <li><div class="t">완료 체크</div><div class="m">각 항목 앞 체크박스 → 이 기기에 저장되고 줄이 그어짐. 하단 '완료 목록 복사'를 눌러 클로드 채팅에 붙여넣으면 클로드가 노션을 완료 처리하고 페이지를 다시 만들어 올림. 노션 ↗ 링크가 있는 항목은 노션에서 완료로 바꿔도 됨.</div></li>
    <li><div class="t">수동</div><div class="m">클로드에게 "10억 페이지 갱신"이라고 하면 노션·플라우드·최근 대화를 다시 읽고 파일 전체를 새로 써서 push합니다. 링크는 ?v=숫자를 올려서 공유.</div></li>
    <li><div class="t">자동 (선택)</div><div class="m">매일 아침 스케줄 작업으로 같은 절차를 돌리면 '오늘의 추천 일정'이 매일 새 데이터로 바뀝니다. 설정 여부는 루크가 결정.</div></li>
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
    write(os.path.join(base, "philosophy", "index.html"), page("삼각 파이프라인", PHILOSOPHY))
    write(os.path.join(base, "platform", "index.html"), page("강의 플랫폼 전략", PLATFORM))
    write(os.path.join(base, "guides", "index.html"), page("할 일 설명서", guide_index_html()))
    for g in GUIDES:
        write(os.path.join(base, "guides", g["slug"], "index.html"), page(g["title"], guide_page_html(g), root="../../"))
    write(os.path.join(base, "sources", "index.html"), page("출처·갱신 방법", SOURCES))
    print("built", UPDATED)

if __name__ == "__main__":
    main()
