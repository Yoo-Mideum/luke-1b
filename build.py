# -*- coding: utf-8 -*-
"""내 연봉 10억 만들기 — 정적 페이지 빌드 스크립트.
python3 build.py 실행 시 index.html 과 하위 폴더 index.html 을 전부 새로 씁니다.
(부분 수정 금지 원칙: 매번 파일 전체를 다시 생성)"""
import json, os, datetime

UPDATED = "2026-11-13"
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
/* ===== 회의록 밝은 테마 ===== */
.mtg{--mA:#0ea5a4;--mB:#3b82f6;--mC:#f59e0b;--mD:#ec4899;--mE:#8b5cf6;
     --sPD:#eef4ff;--sMT:#e7fbf7;--sLK:#fff6e6;--sNT:#fdf0f7}
@media (prefers-color-scheme: dark){
  .mtg{--sPD:#162238;--sMT:#0e2b2a;--sLK:#2e2410;--sNT:#2b1724}
}
.mtg .hero{background:linear-gradient(130deg,#12b2a6 0%,#3b82f6 58%,#8b5cf6 100%)}
.mtg h2{position:relative;padding-left:14px}
.mtg h2:before{content:"";position:absolute;left:0;top:.26em;bottom:.16em;width:5px;border-radius:3px;
  background:linear-gradient(180deg,var(--mA),var(--mB))}
.mtg .card{box-shadow:0 2px 4px rgba(0,0,0,.04),0 10px 28px rgba(0,0,0,.07)}
.mtg table th{background:linear-gradient(180deg,var(--sMT),transparent)}

/* 담당자 카드 */
.who{border:1px solid var(--line);border-radius:18px;overflow:hidden;margin-bottom:12px;background:var(--card);
  box-shadow:0 2px 4px rgba(0,0,0,.04),0 10px 28px rgba(0,0,0,.07)}
.who>.hd2{color:#fff;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px}
.who>.hd2 b{font-family:"Gowun Dodum",sans-serif;font-size:17px}
.who>.hd2 span{font-size:12px;opacity:.92;background:rgba(255,255,255,.2);border-radius:999px;padding:3px 10px;white-space:nowrap}
.who.pd>.hd2{background:linear-gradient(100deg,#3b82f6,#6366f1)}
.who.mint>.hd2{background:linear-gradient(100deg,#0ea5a4,#14b8a6)}
.who.luke>.hd2{background:linear-gradient(100deg,#f59e0b,#f97316)}
.who.pd{background:var(--sPD)} .who.mint{background:var(--sMT)} .who.luke{background:var(--sLK)}
.who .bd{padding:13px 15px}
.who .bd .list li{border-bottom-color:rgba(128,128,128,.18)}

/* 실시간 D-day */
.dday{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;border-radius:999px;
  padding:3px 10px;font-variant-numeric:tabular-nums;white-space:nowrap;background:var(--accent-soft);color:var(--accent)}
.dday .cd{font-weight:500;opacity:.85}
.dday.soon{background:var(--gold-soft);color:var(--gold)}
.dday.urgent{background:var(--red-soft);color:var(--red)}
.dday.past{background:var(--line);color:var(--muted)}
.who .dday{background:rgba(255,255,255,.22);color:#fff}
.who .dday.past{background:rgba(0,0,0,.18);color:rgba(255,255,255,.75)}
.ddrow{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;
  padding:10px 0;border-bottom:1px solid var(--line)}
.ddrow:last-child{border-bottom:0}
.ddrow .lab{min-width:0;flex:1}
.ddrow .lab b{display:block;font-size:14.5px}
.ddrow .lab span{font-size:12.5px;color:var(--muted)}

/* 회의록 메뉴 */
.mnav{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 14px}
.mnav a{font-size:13px;padding:7px 13px;border-radius:999px;border:1px solid var(--line);
  background:var(--card);color:var(--ink);box-shadow:var(--shadow)}
.mnav a.on{background:linear-gradient(100deg,var(--mA,#0ea5a4),var(--mB,#3b82f6));border-color:transparent;color:#fff;font-weight:700}

/* 인포그래픽 */
.ig{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 12px 10px;
  margin-bottom:12px;box-shadow:var(--shadow)}
.ig svg{display:block;width:100%;height:auto}
.ig .cap{font-size:12px;color:var(--muted);margin:8px 2px 0;line-height:1.55}

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
:root{--f1:#6fbb9f;--f2:#3d9273;--f3:#1a6d54;--f4:#054d39}
@media (prefers-color-scheme: dark){:root{--f1:#35775f;--f2:#43997d;--f3:#4cbc95;--f4:#62dcb0}}
.fig{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 12px;box-shadow:var(--shadow);margin-bottom:12px}
.fig svg{display:block;width:100%;height:auto}
.fig figcaption{font-size:12.5px;color:var(--muted);margin-top:8px;padding:0 4px}
.now{display:grid;grid-template-columns:76px 1fr;gap:8px 10px;font-size:14px;align-items:start}
.now dt{font-size:11.5px;font-weight:700;letter-spacing:.02em;text-align:center;border-radius:999px;padding:3px 0}
.now dd{margin:0}
.now .ok{background:var(--accent-soft);color:var(--accent)}
.now .go{background:var(--blue-soft);color:var(--blue)}
.now .zero{background:var(--red-soft);color:var(--red)}
.now .q{background:var(--gold-soft);color:var(--gold)}
.ms{border-left:3px solid var(--line);padding:2px 0 2px 14px;margin:0 0 16px}
.ms.on{border-left-color:var(--accent)}
.ms h3{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.ms h3 .when{font-size:12px;color:var(--muted);font-weight:400}
.ms ul{list-style:none;padding:0;margin:8px 0 0}
.ms li{font-size:14px;padding:4px 0 4px 22px;position:relative}
.ms li:before{content:"";position:absolute;left:0;top:9px;width:12px;height:12px;border:1.5px solid var(--line);border-radius:3px}
.ms .one{margin-top:10px;font-size:13.5px;background:var(--accent-soft);border-radius:8px;padding:8px 10px}
.ms .one b{color:var(--accent)}
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

<script>
(function(){
  function kd(ms){return new Date(ms).toLocaleDateString('en-CA',{timeZone:'Asia/Seoul'});}
  function pad(n){return n<10?'0'+n:''+n;}
  function tick(){
    var now=Date.now();
    var els=document.querySelectorAll('[data-due]');
    for(var i=0;i<els.length;i++){
      var el=els[i], due=Date.parse(el.getAttribute('data-due'));
      if(isNaN(due)) continue;
      var dn=Math.round((Date.parse(kd(due)+'T00:00:00+09:00')-Date.parse(kd(now)+'T00:00:00+09:00'))/86400000);
      var diff=due-now, a=Math.abs(diff);
      var d=Math.floor(a/86400000), h=Math.floor(a%86400000/3600000), m=Math.floor(a%3600000/60000), sc=Math.floor(a%60000/1000);
      el.classList.remove('soon','urgent','past');
      var cd=(d?d+'일 ':'')+pad(h)+':'+pad(m)+':'+pad(sc);
      if(diff<0){ el.classList.add('past');
        el.innerHTML='<span>D+'+Math.abs(dn)+'</span><span class="cd">'+cd+' 지남</span>'; }
      else{
        if(dn<=0) el.classList.add('urgent'); else if(dn<=2) el.classList.add('soon');
        el.innerHTML='<span>'+(dn===0?'D-DAY':'D-'+dn)+'</span><span class="cd">'+cd+' 남음</span>'; }
    }
  }
  tick(); setInterval(tick,1000);
  document.addEventListener('DOMContentLoaded',tick);
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
  {"d":"2026-09-10","t":"주 1개 공개 강의 업로드 유지","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04813d9cf3f40113eed719","cash":False},
  {"d":"2026-09-13","t":"드벨헤어 건물 임대 조건 검토·회신","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea0481e4b4f4e466acd29e02","cash":True},
  {"d":"2026-09-13","t":"디노 협업 경계 정책·계약 정산 기준 초안 작성 후 서명","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea0481309c23e7ffa90af2ca","cash":False},
  {"d":"2026-09-13","t":"사입 수익모델 네이밍 확정 (후보 30개 중 선택)","who":"루크","p":"P0","n":"https://app.notion.com/p/3d70cf8fea04817aaa83e01e45abe751","cash":False},
  {"d":"2026-09-13","t":"전자책 배포 수신자에게 후속 설문 참여 동의 항목 추가 (DM 자동화/신청 폼)","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea0481e6857af5f9e0e2d70f","cash":False},
  {"d":"2026-09-13","t":"사입 강의 후킹용 대표 상품군 선정","who":"루크","p":"P0","n":"https://app.notion.com/p/3d60cf8fea048153a383c225033b34ed","cash":False},
  {"d":"2026-09-13","t":"모든 클로드 프로젝트·클로드 코드에 노션 자동기록 프롬프트 적용","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481649e89fd96df043fbd","cash":False},
  {"d":"2026-09-13","t":"인포크링크 랜딩 페이지 제작","who":"루나","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481429661c705052acada","cash":False},
  {"d":"2026-09-13","t":"유튜브 채널 멤버십 개설 (4,900원)","who":"루나","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481468157e850ce768713","cash":False},
  {"d":"2026-09-13","t":"구독자 전용 오픈채팅 개설 + 입장 안내문","who":"루나","p":"P0","n":"https://app.notion.com/p/3d50cf8fea04814b864ecc232bca108c","cash":False},
  {"d":"2026-09-13","t":"스마트스토어에 진단 세션 상품 등록","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481719b64ff7a119598f0","cash":False},
  {"d":"2026-09-13","t":"메이브님과 컨설팅 판매 배분 합의","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea048181acf4ca4a9359f28e","cash":False},
  {"d":"2026-09-13","t":"스마트스토어에 '구독 창립멤버 연간권 10만' 등록","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481beb16ed36f0c6fe8eb","cash":False},
  {"d":"2026-09-13","t":"컨설팅 정가 확정 — 진단 20만 / 4주 집중 90만","who":"루크","p":"P0","n":"https://app.notion.com/p/3d50cf8fea0481dfb526ea93d0fbd5c0","cash":False},
  {"d":"2026-09-18","t":"특강 1 라이브 — '10월에 올려야 할 상품 30개'","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea048137b746f47edf0cee6b","cash":False},
  {"d":"2026-09-18","t":"카톡 1,000명·카페 선판매 공지","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04818697efc9c2ae93ea3e","cash":False},
  {"d":"2026-09-20","t":"키티티 카드뉴스 6장 인스타 업로드 + 댓글 DM 자동화 연결","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481d49015de6297982e5e","cash":False},
  {"d":"2026-09-20","t":"키티티 AI 브리핑 노출 진단 — 조건형·정보형 검색어 4종 테스트","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481b49d02de192c76147c","cash":False},
  {"d":"2026-09-20","t":"키티티 스마트플레이스 정보 정비 (시술항목·가격·소요시간·사진·소개문)","who":"루크","p":"P0","n":"https://app.notion.com/p/3db0cf8fea0481ce9341f65e6a892448","cash":False},
  {"d":"2026-09-21","t":"키티티 컨설팅 유료화 — 자문 계약서","who":"루크","p":"P0","n":"https://app.notion.com/p/3de0cf8fea04816d8deed192e3f543f1","cash":True},
  {"d":"2026-09-21","t":"특강 편집 — 풀버전(멤버십) + 예고편 3분","who":"루나","p":"P1","n":"https://app.notion.com/p/3d50cf8fea04817eb203f645fefcb13b","cash":False},
  {"d":"2026-09-25","t":"등록 완료 파일 1~4주차 제작 (이미지·상세·가격·CSV)","who":"루크","p":"P1","n":"https://app.notion.com/p/3d50cf8fea048166899dd2c2660aa929","cash":False},
  {"d":"2026-09-25","t":"특강 다시보기 7일 유지 → 8일째 멤버십 전용 전환","who":"루나","p":"P1","n":"https://app.notion.com/p/3d50cf8fea0481feb3a5cd48ca222420","cash":False},
  {"d":"2026-09-27","t":"키티티 교육상품·가격 확정 + 촬영 공간 세팅 (1주차)","who":"루크","p":"P0","n":"https://app.notion.com/p/3dd0cf8fea0481018e13d1a3bf0fc433","cash":True},
  {"d":"2026-09-30","t":"수강생 컨설팅 후속 — 소장 대응 결정·리셀 정리·브랜드 재점검 (익명)","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea0481b1af7ac611bcbe1835","cash":True},
  {"d":"2026-09-30","t":"물류 업데이트/운영 책임자 지정 + 현안 이슈 보드 시작 [설명서]","who":"뿌요·루크","p":"P0","g":"logistics-stabilize","cash":False},
  {"d":"2026-09-30","t":"수강생 전체 공지·교육자료 — 화장품 위탁판매 시 2차 포장(단상자)·표시사항 유지 필수, 도매처 검증 체크리스트","who":"루크","p":"P1","n":"https://app.notion.com/p/3ea0cf8fea0481969503d67f972a91e1","cash":True},
  {"d":"2026-09-30","t":"키티티 빌드업 로드맵 전자책 지영에게 공유·피드백 받기","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea0481c7804adf53ebba3b46","cash":True},
  {"d":"2026-09-30","t":"키티티 토탈샵 임대 조건 재조율·권리금 협상 (공인중개사 통해)","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea04813aba17e8638ff1be86","cash":True},
  {"d":"2026-09-30","t":"키티티 토탈샵 대출 규모·오픈비 견적 확정 (지영과 논의)","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea048147acabc2f5a990da7a","cash":True},
  {"d":"2026-09-30","t":"잔디 이슈 채널 운영 규칙(이슈 템플릿·상태 태그)","who":"루크","p":"P1","cash":False},
  {"d":"2026-09-30","t":"키티티 블로그 Q&A·정의형 콘텐츠 발행 (고객 실제 질문 기반)","who":"루크","p":"P1","n":"https://app.notion.com/p/3db0cf8fea04818b9da3e30c5c00d213","cash":False},
  {"d":"2026-09-30","t":"홈택스 전자세금용 인증서 재발급 및 홈택스 등록","who":"루크","p":"P1","n":"https://app.notion.com/p/3d60cf8fea048161af02c3b521f3765e","cash":False},
  {"d":"2026-10-01","t":"3PL 수강생 재고 당근·외부 판매 — 첫 등록 (동의서·시트·비즈프로필) [설명서]","who":"루크·루나","p":"P0","g":"3pl-resale","n":"https://app.notion.com/p/3de0cf8fea0481b2a948d2dc4f7802ed","cash":True},
  {"d":"2026-10-01","t":"키티티바이지영 상표권 출원 (KIPRIS 선행검색 → 출원, 30분) [설명서]","who":"루크·지영","p":"P0","g":"kititi-trademark","n":"https://app.notion.com/p/3ea0cf8fea0481eda6d9db338d52c92c","cash":False},
  {"d":"2026-10-01","t":"물류 삭제/무효화 임시 규칙 + 핸드오버 체크리스트","who":"루크·뿌요","p":"P1","cash":False},
  {"d":"2026-10-01","t":"지영 인스타 주간 운영 캘린더 시작","who":"지영","p":"P1","cash":False},
  {"d":"2026-10-02","t":"물류·전산 전체 프로세스 맵 + 병목 표시","who":"뿌요","p":"P1","cash":False},
  {"d":"2026-10-03","t":"물류 중복·충돌 기능 정리 우선순위","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-04","t":"키티티 AI 스타일 미리보기(/try) 구축 — 무료 1회·워터마크·유료 원본 다운로드","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04812b8f86e2d58503588d","cash":True},
  {"d":"2026-10-04","t":"키티티 '연봉 10억 만들기' 페이지 배포 — 저장소 kititi-1b 생성·권한 후 push","who":"루크","p":"P0","n":"https://app.notion.com/p/3eb0cf8fea04814187b8c258b3a2d38e","cash":True},
  {"d":"2026-10-04","t":"키티티바이지영 상표 출원 (지영 명의, 특허로 전자출원) — 진행 중","who":"루크","p":"P0","n":"https://app.notion.com/p/3ec0cf8fea0481919532d4927c656358","cash":True},
  {"d":"2026-10-04","t":"물류 표준 운영 가이드 배포 / 피크일(월·화) 택배 우선 운영안","who":"루크·뿌요","p":"P1","cash":False},
  {"d":"2026-10-05","t":"리나님 시간 기록 시트 1~2주 시범 운영 (매일 퇴근 전 피드백)","who":"리나님·루크","p":"P0","n":"https://app.notion.com/p/3e90cf8fea0481f386b9d5f0d96feb05","cash":False},
  {"d":"2026-10-05","t":"키티티 상담 사이트 원장님 확인 (사진 동의·한마디·비포애프터)","who":"루크·지영","p":"P0","n":"https://app.notion.com/p/3e90cf8fea0481d2aa25e18cf01f6b09","cash":False},
  {"d":"2026-10-05","t":"매장 대청소 작업 입회·검수 (비포에프터클린 · 10/5 14:00 · 작업 전후 사진)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f00cf8fea048133b45ff8bb4dc6e7c9","cash":False},
  {"d":"2026-10-06","t":"수강생 화장품법 소송 대응 지원 — 답변서 기한·변호사 연결 (익명) [설명서]","who":"루크","p":"P0","g":"lawsuit-support","n":"https://app.notion.com/p/3ea0cf8fea048198857ef162cf15ad7a","cash":True},
  {"d":"2026-10-06","t":"강의 플랫폼 3자 미팅 제안서 1차본 검토 — 초이스토리 × 종혁 본부장 × 셀수다","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04814e827ce3cca543028e","cash":True},
  {"d":"2026-10-06","t":"물류 CS 포인트 분석 + 사전 안내 스크립트 정비","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"물류 권한 재설계 + 감사 로그","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-07","t":"지영 예약·매출 간단 대시보드 완료 목표","who":"지영","p":"P2","cash":False},
  {"d":"2026-10-08","t":"종혁 본부장 미팅 — 락인 축(챌린지·카페·광고) 역할과 1:1:1 배분안 제시 [설명서]","who":"루크·메이브님","p":"P0","g":"platform-director-meeting","n":"https://app.notion.com/p/3eb0cf8fea04816b8d8ee9e56061c6d0","cash":True},
  {"d":"2026-10-08","t":"3자 1:1:1 안과 초월스토리 8% 모델 관계 정리 (대체 vs 병행) → 10/8 본부장 미팅 제안 수정","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e4a78edf0ea6527d5c","cash":True},
  {"d":"2026-10-08","t":"인베이더 종료 사실 확인 — 범위·시점·출처 파악 (강의만인지 전체인지)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b2b5f9c0ab5aa17594","cash":True},
  {"d":"2026-10-08","t":"키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체","who":"루크","p":"P0","n":"https://app.notion.com/p/3ec0cf8fea0481698468f35e62d2e19b","cash":False},
  {"d":"2026-10-08","t":"세무사에 최근 2년 수입금액 조회 — 0인지 먼저 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048142a77bc76c2cbddeb4","cash":False},
  {"d":"2026-10-08","t":"정관 본점 조항·등기사항전부증명서 확인 — 주주총회 필요 여부 정하기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b4a420f807f87de087","cash":False},
  {"d":"2026-10-08","t":"메이브님과 마지막 기수 공동 대응 합의 — 같은 명단 확보 동선 쓰기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04818daa2dec0849cd7a73","cash":False},
  {"d":"2026-10-08","t":"구리세무서 재산법인세과 전화 — 법인등기 진행 중, 완료 후 재신청 예정 알리기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481d396d6fb41d1c6ee6b","cash":False},
  {"d":"2026-10-08","t":"지영 미팅 — 정부지원사업 후보 3개 + 사업계획서 초안 리뷰","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-08","t":"사진 기반 입고/검수 자동화 플로우 설계","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-09","t":"목적 추가 문구 확정 — 창고업·물류 쪽을 넉넉하게 (꼬마빌딩 취득세 연결)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea048140aa1ece2d480e62f2","cash":True},
  {"d":"2026-10-09","t":"세무사 통화 — 임원 추가선임이 '50% 교체'인지, 지분 50% 양도가 '인수'인지","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048117871ec5f5c092cc1c","cash":False},
  {"d":"2026-10-09","t":"정관 원본 찾아 본점 조항 확인 — '구리시'까지인가 번지까지인가","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481cc8bc6f8687a37a03a","cash":False},
  {"d":"2026-10-09","t":"'셀러들의 수다' 상호 중복 확인 — 의정부지법 남양주지원 관할 내 (인터넷등기소 법인 상호검색)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea04817aa334df39bcb54f3e","cash":False},
  {"d":"2026-10-09","t":"신정현 대표님에게 등기 제출용 준비물 전달 + 인감 신고 여부 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea048160af98ebbd0e2d90e8","cash":False},
  {"d":"2026-10-09","t":"키티티 원장님께 /admin 노트 사용법 전달 + 시술 방향 검토·피드백 받기 (습도·채광·장소·이동시간)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea04810b808df66fdd4ed562","cash":False},
  {"d":"2026-10-09","t":"키티티 /guide 내용 원장님 피드백 받기 (상담 12항목·데일리/촬영 기준·O/X 표·계절 색)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ed0cf8fea0481839ab5c4f4a80c7caf","cash":False},
  {"d":"2026-10-10","t":"정관 찾기 — 법무사·세무사·등기소 열람·외장하드 순서로","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481ba8918e112e5a5b6b0","cash":False},
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
  {"d":"2026-10-11","t":"메이븐 스토어 재정비 + 집중 품목 선정 (4분기 월 순수익 1,000만·일 200건 목표)","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048159873bcb81c41d12e9","cash":True},
  {"d":"2026-10-11","t":"메이븐 스토어 재정비 · 집중 품목 선정","who":"메이브님","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04811ab5f7c42585eeeb16","cash":True},
  {"d":"2026-10-11","t":"[막힘] 지영 원장 수익모델 빌드업 페이지 배포 — kittiti-jiyoung 저장소 생성·Pages 켜기·Claude 권한 추가 (루크 직접)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea048152b55cec152c0f6fc9","cash":True},
  {"d":"2026-10-11","t":"토탈샵 인테리어(급배수·전기 증설·칸막이·냉난방기) 승인 별첨 문서 준비","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea048125b5f0cb4b24793347","cash":True},
  {"d":"2026-10-11","t":"토탈샵 건물 임대차 특약 수정안 협상 — 제소전화해·원상복구·갱신 (진행 중 · 10/8 계약 체결 녹음 있음, 완료 여부 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481f1a56ed3713160c671","cash":True},
  {"d":"2026-10-11","t":"인베이더 무료강의 라이브 PPT 제작","who":"루크","p":"P0","n":"https://app.notion.com/p/3ee0cf8fea04810e9f65d1802510734f","cash":False},
  {"d":"2026-10-11","t":"키티티 인스타·플레이스·매장 QR에 진단 링크 걸고 홍보 → 파트너샵 마케팅 키트 1판","who":"루크","p":"P0","n":"https://app.notion.com/p/3ef0cf8fea0481c794b3ef4cc6242f2c","cash":False},
  {"d":"2026-10-11","t":"[결정 필요] 세무사 상의 — 2,000만 지출 처리 방식 결정","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b2a072c720ff4ca5ba","cash":False},
  {"d":"2026-10-11","t":"[결정 필요] 뿌요 역할·수익 구조 확정 — 장기 거취 먼저, 그다음 배분","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e19ba5cf10a588f7d7","cash":False},
  {"d":"2026-10-11","t":"인베이더 계약서 확인 — 수강생 명단·콘텐츠·후기 소유 조항","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04819eb940cf3625f83b83","cash":False},
  {"d":"2026-10-11","t":"키티티 무료강의 ①② 제작 + 셀프메이크업 무료 PDF + 저가 VOD 5강 촬영","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea04813c88c1e7123b988adc","cash":False},
  {"d":"2026-10-12","t":"네 건을 한 신청서로 묶기 — 본점이전·상호변경·목적추가·이사선임 (서류는 직접 만들어 둬 셀프로도 가능)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04817f8c33fb44f46ab8b2","cash":False},
  {"d":"2026-10-12","t":"마지막 기수 수강생 명단을 자체 채널(카톡·카페·멤버십)로 옮기는 동선 넣기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04816e9059df8108fdd0c7","cash":False},
  {"d":"2026-10-12","t":"전부개정 정관으로 가기 — 등기부 목적 전사 + 사업연도 확인 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481999f5ac46281d758d7","cash":False},
  {"d":"2026-10-12","t":"기장 세무사무소에 사업연도 확인 — 1월 1일~12월 31일 맞는지 전화 한 통","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481a3a3c8f22c07545cd2","cash":False},
  {"d":"2026-10-12","t":"등록면허세 중과 여부와 '그 밖의 등기' 건수 확인 — 세액이 20만원 움직임","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481198a1ddb474a22c9fc","cash":False},
  {"d":"2026-10-12","t":"법인인감카드 분실 — 인터넷등기소 사용정지 + 법인인감도장 여부 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea04810aaa8ce141622c0e17","cash":False},
  {"d":"2026-10-12","t":"법무사 위임으로 가는 경우 서류 목록 — 위임장과 법인인감증명서가 추가된다","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea0481a58ee3c00fe5ab11fb","cash":False},
  {"d":"2026-10-13","t":"사입 재고 처리 가이드라인 — 50일 경과 시 마진 조정 → 강사 처리 신청 목록 순차 처리","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bab38bf16e2cc7d963","cash":True},
  {"d":"2026-10-13","t":"2,000만 원 지출 세무 처리 방식 세무사 확인 후 결정 (1,000만 루크 지급 vs 2,000만 유지)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bb9730c3375a2dffc7","cash":True},
  {"d":"2026-10-13","t":"3자 플랫폼 계약서에 '수강생 명단·결제 창구·강의 콘텐츠 = 셀수다 소유' 조항 넣기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e7831bcfab5d83841e","cash":True},
  {"d":"2026-10-13","t":"강의 플랫폼 시행 전 선행 조건 4가지 — 인베이더 계약 정리 / 역할 분배 확정 / 라이브 장소 셋팅 / 광고 운영 셋업","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481e388cec4dc7fe4a8eb","cash":True},
  {"d":"2026-10-14","t":"박종혁 본부장에게 물어볼 한 가지 — 카페 월 4,000명 만들 당시 광고비","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea04816ca069c910adc45cca","cash":False},
  {"d":"2026-10-15","t":"힐링디어스(주) 본점이전 등기·사업자등록 정정 — 새 본점 주소 확보 완료(10/9), 10/12 법무사 위임 → 접수 → 등기 후 정정 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3ed0cf8fea0481a7b0c0cfc85f4b3475","cash":False},
  {"d":"2026-10-15","t":"4대보험 사업장 소재지 변경신고 — 변경일부터 14일","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481bda5e2f2a8846531fd","cash":False},
  {"d":"2026-10-15","t":"지영 내년 조달(최소 1억) 월별 마일스톤 확정","who":"루크·지영","p":"P1","cash":False},
  {"d":"2026-10-15","t":"공고방법을 홈페이지 게재로 변경 — 지금은 수원 경기신문으로 돼 있음","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04818d8bc4e8dd106ecd1c","cash":False},
  {"d":"2026-10-15","t":"미입고 자동 알림·반품 트리거 프로토타입","who":"루크","p":"P2","cash":False},
  {"d":"2026-10-15","t":"[보류] 10월 정산 확인 전까지 하지 않을 것 — 재검토일","who":"루크","p":"P3","n":"https://app.notion.com/p/3d50cf8fea0481ae9cbdc532f42c5b95","cash":False},
  {"d":"2026-10-16","t":"박종혁 본부장 협업 — 10월에 정할 세 칸(다섯 칸에서 축소): 차감 산정 방식 · 3PL·리셀·프로그램 매출은 6:4 밖 · 총액 인식 일치","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea04811ca54cf38b0d15e46f","cash":True},
  {"d":"2026-10-16","t":"등기 서류 전부 출력 완료 — 법무사 통화 뒤에 날인하고 접수 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f40cf8fea048119872af76a2ef1a9d6","cash":False},
  {"d":"2026-10-16","t":"법무사 10/12 상담 후속 — 사업자등록증 사본 문자 전송 · 서류 재준비해 재방문 일정 조율 · 정관·회의록 재작성 결과 확인(터미널 운영·화물 운송 목적 제외 · 주식 수 100만 주 권고는 기존 [결정] 100,000주와 달라 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f80cf8fea0481c78c58d84e2b504612","cash":False},
  {"d":"2026-10-18","t":"키티티 무료강의 라이브 → 저가 VOD 판매 오픈 + 개인 레슨 네이버 예약 등록","who":"루크","p":"P1","n":"https://app.notion.com/p/3dd0cf8fea0481dc8934dc0c61d42b94","cash":True},
  {"d":"2026-10-19","t":"지영 검토용 보관함 노션 1페이지 개설 — 준비해 둔 AI 제안·웹 개선안 이동, 알림 없이 지영이 꺼낼 때만 공개","who":"루크","p":"P0","n":"https://app.notion.com/p/3fb0cf8fea04811c8806e29ce0d66548","cash":False},
  {"d":"2026-10-19","t":"네이버 플레이스 예약 슬롯 설계 1장 (데일리 1시간·헤어 30분, 입력 순서대로) → 지영은 11/1 입력만","who":"루크","p":"P0","n":"https://app.notion.com/p/3fb0cf8fea0481c3a3b0ed433d9730d5","cash":False},
  {"d":"2026-10-19","t":"박종혁 본부장 사무실 좌석 마련 + 온보딩 지원 (플라우드 10/9 · 기한 추정 — 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea048178bbbbeb6b52524035","cash":False},
  {"d":"2026-10-20","t":"초월스토리 파일럿 강사 후보 소개","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048167bc15f5dc0646b939","cash":True},
  {"d":"2026-10-21","t":"박종혁 본부장 10/21(수) 첫 출근 — 사무실 책상 정리 + 수요일 일정 조율·피자 회식 (플라우드 10/19 · 메이브님과 공동)","who":"루크","p":"P0","n":"https://app.notion.com/p/3fe0cf8fea0481f187f4d10ef54018eb","cash":True},
  {"d":"2026-10-21","t":"민트(박종혁) 계약서 초안 완성 — 10/21 미팅에서 일곱 칸 채우기(6:4 방향 · 분모 A/B안 · 3개월 총액 · PD 외주 단가 · 광고 첫 집행일 · 1월 객단가 · 과거 CAC)","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea0481adaadcc68d440bc3a3","cash":False},
  {"d":"2026-10-21","t":"[중요] 카페·유튜브·광고계정을 갑(법인) 명의로 먼저 만들기 — 민트님에게는 관리자 권한만","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea04810ba2fdf3a28155c4a9","cash":False},
  {"d":"2026-10-21","t":"민트님께 협업 조건 요약본(/park-terms/) 발송 → 수정 의견 받기 (/park-contract/는 내부용)","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea04812184e8f7da9f48c9d8","cash":False},
  {"d":"2026-10-21","t":"민트님 입력 폼 발송 — /park-terms/ 링크 하나만(일곱 칸 + 확인 항목 + 지급 계좌)","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea048186bdccd8de4fc59b8a","cash":False},
  {"d":"2026-10-22","t":"[결정 필요] 강사 협업이 끝나도 원크루 관계는 유지 — 계약 전 구두로 못 박기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea0481b4b7c6ed7ab7329d8c","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 루크 참여 범위 확정 — 단순 플레이어 vs 공동 빌드업, 배분 초안 작성","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04817c8fc5e1e6c7681869","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 초월스토리 정산 기준 문서화 — '전체 매출' 정의, 비용 항목 목록, 8% 두 개(루크 수수료·광고비)의 관계","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea04818c9a01c1346a18f643","cash":True},
  {"d":"2026-10-22","t":"초월스토리 — 루크 참여 범위를 공동 기획으로 올릴지 (5:5 분모에 들어가는지) 10/22 배분 초안 전에 제기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f20cf8fea0481faa420daf4c6647ca1","cash":True},
  {"d":"2026-10-22","t":"가을 대표님 몫 2,200만의 산출 근거 확인 — 루크 4가 880만인지 1,590만인지가 여기서 갈린다","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea04813fab69eb44001ba56d","cash":True},
  {"d":"2026-10-22","t":"[결정 필요] 6:4를 숨길지, 공동 기획으로 공개할지 — 10/22가 돌릴 수 있는 마지막 자리","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea048164bd27f5664acd603b","cash":True},
  {"d":"2026-10-22","t":"가을 대표님과 6:4 합의를 서면으로 남기기 — 대가가 기획·PPT·라이브 코칭이라는 점 명시","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481af8f59d05cd4111cad","cash":True},
  {"d":"2026-10-22","t":"초월스토리 광고 예산 약 4,500만 확인 + 상한·중단 기준 받아내기 (4,500만은 역산값 — 확인 전)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481c58f8cfd00f6266b69","cash":True},
  {"d":"2026-10-22","t":"가을 대표님에게 사전 설명 — 손익분기 18명이라는 사실과 광고비 리스크 미리 알리기","who":"루크","p":"P0","n":"https://app.notion.com/p/3f30cf8fea0481d4b796fed4ccceb00f","cash":True},
  {"d":"2026-10-22","t":"인스타 편집 협업자 위임 시스템 — 역할 정의 1장 + 15분 가이드 템플릿 + 첫 작업 가이드 1건, 협업자에게 루크가 직접 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/3fb0cf8fea0481a98630d7d3e65ed5bd","cash":False},
  {"d":"2026-10-22","t":"[결정 필요] 상품 최종 확정 — 289만 단일 여부, 1:1 컨설팅반 포함 여부, 목표 객단가","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04816ca0fedde155dd3162","cash":True},
  {"d":"2026-10-23","t":"사업자등록 정정신고 — 등기 완료 직후 (10/7 취하 건 재신청 · 등기사항전부증명서 첨부)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048138b075f9bb51f5e97e","cash":False},
  {"d":"2026-10-23","t":"6기 무료 라이브 최종 리허설 10/23(금) 11:00 — 수정 PPT·세일즈 흐름 점검 + 전날 리마인드 발송 (플라우드 10/19 · 일시는 노트 기재값)","who":"루크","p":"P0","n":"https://app.notion.com/p/3fe0cf8fea0481cb8bd8d421504fad3b","cash":False},
  {"d":"2026-10-23","t":"라이브 PPT — FAQ 섹션(첫 수익까지 기간·월 천만 기대치 조정) · '시작 직후 하루~3일 내 첫 수익' 메시지 재정의 · 50·60대 톤 문구 · 성과 수치 옆 기대치 관리 문안 (플라우드 10/19 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/3fe0cf8fea048158a9ead567330b045c","cash":False},
  {"d":"2026-10-23","t":"민트님께 받을 네 가지 — 주소·생년월일·연락처·지급 계좌 → 계약서 당사자란·제5조 채우고 서명","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea0481749ac7eac8953eb425","cash":False},
  {"d":"2026-10-24","t":"1월 자사 강의 객단가 확정 — 180만원은 가정값 · 6:4의 분모(A안 매출 기준 / B안 비용 차감 후)와 3자 분배 해석(루크 36%·종혁 40%·정현 24%로 읽은 것)도 같이 확정","who":"루크","p":"P0","n":"https://app.notion.com/p/3fc0cf8fea0481acaa81f970cc74f260","cash":True},
  {"d":"2026-10-24","t":"라이브 출연 수강생 — 연락처 수령 후 당일 16:00 이전 도착 사전 연락·일정 조율 (플라우드 10/19 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/3fe0cf8fea0481319c91ceca079ab94f","cash":False},
  {"d":"2026-10-24","t":"전환율 가정 검증 — 과거 3%와 목표 10% 사이에서 광고비 상한 정하기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481aa94bac8bcc8dcda8b","cash":True},
  {"d":"2026-10-24","t":"[결정] 촬영팀은 돈벌쥐 PD님 쪽으로 — 김○○ PD 회사 안 씀 (진행 중)","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea04816fa122f7b7c2e3b397","cash":False},
  {"d":"2026-10-25","t":"토탈샵 헤어 기기·약제 공급처 결정 — 로레알 계약 1순위(소개 미팅에서 7가지 답 확보) · 2순위 헤어2000+워맥스 · 기존 기기 4대는 전부 철거","who":"루크","p":"P0","n":"https://app.notion.com/p/3fd0cf8fea0481858d7ce31805c939c2","cash":True},
  {"d":"2026-10-25","t":"권리금 계약 인도 조건 부속 합의 — 중개사에 문자 발송(1~3안 중 택1) → 인수·철거 목록(사진 번호) 작성 → 부속 합의서 + 임대인 특약 별첨 동일 목록","who":"루크","p":"P0","n":"https://app.notion.com/p/3fd0cf8fea04817ebf63f7d0859fdf49","cash":True},
  {"d":"2026-10-25","t":"유튜브·라이브 출연 고연령 성과자 섭외 (불발 시 대안 마련)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f10cf8fea048104a2f5fc1bcdce6b0a","cash":False},
  {"d":"2026-10-25","t":"키티티 토탈샵 인스타 공식 계정 구조 1장 — 공식 계정 신설, 기존 계정은 '대표원장' 개인, 직원 게시물 공동 작업자 규칙","who":"루크","p":"P0","n":"https://app.notion.com/p/3fd0cf8fea048179a3aed5da456e2b71","cash":False},
  {"d":"2026-10-25","t":"인터뷰 전 테라피님(6기 라이브 출연 수강생) 가격관리 가입·자동등록 실사용 확인 — 10/23 기준 미가입, 안 되면 '이번에 막 세팅했다'로 답변 (라이브는 10/25 진행됨 · 노션 미완료)","who":"루크","p":"P0","n":"https://app.notion.com/p/4040cf8fea0481e59c55c8b91c9642b1","cash":False},
  {"d":"2026-10-26","t":"부가세 2기 예정분 신고·납부 — 힐링디어스(주) 신고 대상인지 / 개인 예정고지 확인 (예정고지 납부는 11/2)","who":"루크","p":"P0","n":"https://app.notion.com/p/3f80cf8fea048164b79ef6d1c68a5bb7","cash":False},
  {"d":"2026-10-26","t":"최은봉 10월 4주차(8회차, 일본 직판) 교육자료 발행 — 작성·push 완료, 맥에서 배포 필요 (노션 진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/4030cf8fea0481fa99adccab0f1e3d76","cash":True},
  {"d":"2026-10-26","t":"첫 '결정 묶음' 세션 — 10/26(일) 15분: ① 촬영 작가 ② 임대 특약 서명 ③ 상표 대행 선택 (선택지 2개 + 추천 1개씩)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fb0cf8fea048166b25ffd0e07213cf4","cash":False},
  {"d":"2026-10-27","t":"물류팀 매일 18:30 브리핑(15~20분) 고정 + 사실/경험/의견 분리 보고 양식 도입","who":"루크","p":"P0","n":"https://app.notion.com/p/4020cf8fea048130a802fa2cefc1c2cb","cash":False},
  {"d":"2026-10-29","t":"최은봉 10월 5주차(9회차) 교육자료 발행 — 10/28 세션 + 지난주 업데이트 정리해 원크루 사이트 게시 (플라우드 10/28 · 노트 기한 '오늘'=10/28 → 10/29로)","who":"루크","p":"P0","n":"https://app.notion.com/p/4070cf8fea0481e4b3cff5506781f63d","cash":False},
  {"d":"2026-10-29","t":"초월스토리와 협업 모델 옵션(플레이어 vs 공동 빌드업) · 배분 초안 확정","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481bc9b1ee702bcb74f48","cash":True},
  {"d":"2026-10-29","t":"사진 재촬영 컨셉보드 1장 + 작가 후보 3명 견적 → 지영은 작가 1명·날짜만 선택","who":"루크","p":"P1","n":"https://app.notion.com/p/3fb0cf8fea0481e0b666f760a50230b5","cash":False},
  {"d":"2026-10-30","t":"가을 대표님 수강생 코칭 알바 운영안 확정 — 30~40분/1인 1만원, 주제: 설치·자동등록·상품 찾기 (메이브님과 일정 조율) (플라우드 10/28 정복녀 7기 · 기한은 노트 기재값)","who":"루크","p":"P0","n":"https://app.notion.com/p/4070cf8fea048186b60cdc9e58c31272","cash":True},
  {"d":"2026-10-30","t":"계약서 제8조·제9조 수정 — 외주 한도 700~800만, 런칭일 1/20 확정","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea04813e8a9aec2a3964f82a","cash":False},
  {"d":"2026-10-30","t":"1월 강의 객단가 확정 — 10/30 미팅에서","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481c4a2e4cff70af7aa69","cash":False},
  {"d":"2026-10-30","t":"3,000만 예산의 정확한 구성 닫기 — 용역비 900만 포함인지","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481f8a6efd7ea3c215036","cash":False},
  {"d":"2026-10-30","t":"10/30 영상팀 세팅 미팅 어떻게 할지 — 민트님이 잡아둔 일정","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481579b5ee470f6489efd","cash":False},
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
  {"d":"2026-10-31","t":"재고 못 판 수강생 상품 위탁판매 + 판매 일지","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04817ca113c3318de00839","cash":True},
  {"d":"2026-10-31","t":"물동량 일 200건 · 월 6,000건 확대 → 택배비 재협상","who":"메이브님","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481dcad6cf63ec1a3aef8","cash":True},
  {"d":"2026-10-31","t":"졸업 후 반복 매출 가격안 — 프로그램 월 구독(소싱·자동등록·CS) + 3PL 등급(보관 무료 기간 후 보관료·처분 수수료)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048137bd9ac4df5325f1d0","cash":True},
  {"d":"2026-10-31","t":"지영 원장에게 확인 — 평균 객단가·월 예약 건수·재방문율·시술별 비중","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea048118bf45dc9a319738de","cash":True},
  {"d":"2026-10-31","t":"PG 수수료 요율과 실제 광고비 비율 숫자 확보 — 둘만 들어오면 배분표가 하나로 확정된다","who":"루크","p":"P1","n":"https://app.notion.com/p/3f30cf8fea04813d8880ee10ef500869","cash":True},
  {"d":"2026-10-31","t":"네일 오픈샵 세트 비교표 — 사라센 디젤 A/B·다이아미·모스티브(컬러 수·램프 포함·가격) + 흡진기 포함 총액","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea0481309185f76381e70360","cash":True},
  {"d":"2026-10-31","t":"헤메네일 가격비교 → AI 진단 링크 연결 (보조 송객 채널)","who":"루크","p":"P1","n":"https://app.notion.com/p/3ef0cf8fea048134b9ede80fe9d7ed0f","cash":False},
  {"d":"2026-10-31","t":"법인 서류 클라우드 폴더 만들기 — 정관·주주명부·의사록 비치 의무","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048167b10bd8cdca622f78","cash":False},
  {"d":"2026-10-31","t":"창고형 매장 후보지 3~5곳이 과밀억제권역 밖인지 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481c090bdf661e6f1909f","cash":False},
  {"d":"2026-10-31","t":"3PL 창고가 취득세 중과 제외 업종(창고업)에 해당하는지 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481e4a556efe81d008760","cash":False},
  {"d":"2026-10-31","t":"꼬마빌딩 — 목표 지역(과밀억제권역 안/밖)·시점·법인 명의 여부 정하기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048139849cd98e17f636fc","cash":False},
  {"d":"2026-10-31","t":"힐링디어스로 받을 매출 하나 정하기 — 휴면법인 판정 회피용","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481ef9569dc5122402d95","cash":False},
  {"d":"2026-10-31","t":"주소가 박혀 있는 것들 전부 교체 — 세금계산서·통장·스마트스토어·플레이스·거래처","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04818e88b0cfcbbe3d2313","cash":False},
  {"d":"2026-10-31","t":"초월스토리 런칭용 성과자 섭외 — 고연령 성과자(유튜브) + 성과자 2명(라이브), 본인 동의","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048113a71ada0c8358b93e","cash":False},
  {"d":"2026-10-31","t":"[결정 필요] 쿠팡 가격비교 크롤링 — 플랫폼 정책 검토 후 개발 여부 결정","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481ab824fdb0460ef0cef","cash":False},
  {"d":"2026-10-31","t":"'사입으로 수익 낸 사례' 특강 정기 개최 일정 잡기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea04811fbddde6fcbdd31d1e","cash":False},
  {"d":"2026-10-31","t":"6기·4기 수강생 성과·후기·비포애프터 수집 — 신규 플랫폼 1기 모집용 증거","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea0481838b77ff04c8c73200","cash":False},
  {"d":"2026-10-31","t":"지영 원장에게 빌드업 페이지용 숫자 4가지 받기 — 매출·순이익·본인 몫, 목표 주택 위치·평형, 건물 매입 vs 신축, 목표 차량 모델명","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea0481a78df0ec77cc00af96","cash":False},
  {"d":"2026-10-31","t":"새 저장소 kittiti-jiyoung 생성 + Pages 켜기 (루크 직접)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f20cf8fea0481859045f9b892eb6fa9","cash":False},
  {"d":"2026-10-31","t":"등기 끝난 뒤 할 일 10가지 — 사업자등록 정정, 법인인감 재제작, 사무실에 상호 통지, 통신판매업 변경신고","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea0481c99265f4b17f2ddc0c","cash":False},
  {"d":"2026-10-31","t":"법인 지방세 체납 여부 확인 — 위택스에서 납세증명서 발급을 시도해 보기","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea048118a682f449e8f920fa","cash":False},
  {"d":"2026-10-31","t":"유튜브 콘텐츠 전략 재구성 — 수강생 성장 스토리 + 전문가 인사이트 (박종혁 본부장과 공동 · 플라우드 10/9 · 기한 추정 — 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f40cf8fea048172858acfe572f69aad","cash":False},
  {"d":"2026-10-31","t":"키티티 사이트 웨딩 페이지 — 교육·수강 관련 정보 빼고 읽기 쉬운 문구로 다시 쓰기 (플라우드 10/11 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f60cf8fea0481268d1cf30e554b0457","cash":False},
  {"d":"2026-10-31","t":"키티티 AI 가상 메이크업 — '가상 체험' 안내 문구 크게 + 스타일 표본 선택 방식으로 재설계 (플라우드 10/11 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3f60cf8fea0481838e13e888a92f7c96","cash":False},
  {"d":"2026-10-31","t":"인베이더 강의 종료 공식 공지 → 수강생 소통용 단톡방 개설·이관 (플라우드 10/19 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fe0cf8fea0481458966cdb0905f656a","cash":False},
  {"d":"2026-10-31","t":"3PL 금요일 택배비 할인 프로모션 — 출고 적은 요일 건당 1,000원 지원으로 재고 회전 촉진 (플라우드 10/19 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fe0cf8fea04814dabc4e0ea88a803be","cash":False},
  {"d":"2026-10-31","t":"최은봉 자료실 — 일본직판(티쿤) 전자책을 7회차 '참고자료'로 편입 완료 → 맥에서 npm run deploy(배포 대기)","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea0481ea9964f5b3c6a14470","cash":False},
  {"d":"2026-10-31","t":"12월 메이븐 정산 1,800만 확정 여부 닫기 — 언제까지 결정할지부터","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea04816ab986e866e792a04a","cash":False},
  {"d":"2026-10-31","t":"민트 건 배분 — 루크 40%인가 24%인가 (정현님 몫 여부)","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea04818eafb8ed52a94114a4","cash":False},
  {"d":"2026-10-31","t":"가을님 정산액 6:4 방향 확정 — 어느 쪽이 6인지","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481688c9ad00d51fb263f","cash":False},
  {"d":"2026-10-31","t":"물류팀 일일 KPI(처리 건수·시간 준수·보고 적시성) 설정 → 1주 단위 평가 + 1:1 면담으로 역할 기대치 합의","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea04817a8e32e54f2fbaec46","cash":False},
  {"d":"2026-10-31","t":"주간 촬영 출장 메이크업 계약(엑셀 방송 대표) 조건 문서화 — 장소·시간·인원, 출장비 면제·업스타일 제외·정가 요금표·추가요금·변경 페널티 (플라우드 10/24 메모 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4030cf8fea04810aa183f4321102b969","cash":True},
  {"d":"2026-10-31","t":"헤어팀 보상안·2인 배치 손익 시뮬레이션 — 기본급+매출 초과분 인세 구조, 인세율·정산 주기·KPI 정의, 월 손익분기 매출 산출 (플라우드 10/24 메모 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4030cf8fea048111900bfbf73486cef7","cash":True},
  {"d":"2026-10-31","t":"테라피님 CS 응대 템플릿(반품·환불·항의) 제작·전달 — 다른 수강생 공용 템플릿으로 확장 가능 (10/23 코칭 Action Item, 10/25 노션 등록)","who":"루크","p":"P1","n":"https://app.notion.com/p/4040cf8fea0481659c16d859e5a5cc04","cash":False},
  {"d":"2026-10-31","t":"키티티 40×10cm 배너 제작 — 프롬프트①로 인물·배경 생성 후 캔바에서 텍스트·QR 2개 올려 인쇄 입고 (10/26 스타일 합격 · 남은 작업: 재생성·4:1 확인·QR 스캔 테스트·4724px 업스케일·CMYK PDF 입고)","who":"루크","p":"P1","n":"https://app.notion.com/p/4050cf8fea0481e1bd2fc390bea0769f","cash":False},
  {"d":"2026-10-31","t":"신규 수강생 한 분 환영 메시지 발송 — 첫 주 이탈 방지, 첫 주문까지 질문하며 따라오게 (초안 2종 작성됨 → 발송 후 완료 처리)","who":"루크","p":"P1","n":"https://app.notion.com/p/4090cf8fea0481f38d3fc3dbc35a50f9","cash":False},
  {"d":"2026-11-01","t":"키티티 배너 캔바 편집본 만들기 (이미지·텍스트 레이어 분리) — 같은 날 '편집본(40x10cm) 만들기'는 완료 처리됨, 같은 일이면 완료 처리 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/4050cf8fea0481d7ad23ca41accf02d4","cash":False},
  {"d":"2026-11-01","t":"가을 대표님용 프로그램 설치·자동등록 사용법 표준 가이드 제작·배포 — 코칭 알바 FAQ 답변 멘트 포함 (플라우드 10/28 정복녀 7기 · 기한은 노트 기재값)","who":"루크","p":"P0","n":"https://app.notion.com/p/4070cf8fea0481d1afc4d04cffe3428a","cash":False},
  {"d":"2026-11-01","t":"상표 출원 대행 견적 2곳 + '키티티바이지영' 지정상품(헤어·메이크업·토탈샵 서비스업) 초안","who":"루크","p":"P0","n":"https://app.notion.com/p/3fb0cf8fea0481779703c5e6f9d2683c","cash":True},
  {"d":"2026-11-01","t":"지영 특허고객번호 신청 + 상표 의견서용 사용 증거 수집('만지다' 어원 언어 확인 포함)","who":"루크","p":"P0","n":"https://app.notion.com/p/4080cf8fea0481849c91e543cc4dbfd7","cash":True},
  {"d":"2026-11-01","t":"초월스토리 파트너십 계약서 초안 작성 · 법 조항 확인 · 상호 교환","who":"루크","p":"P0","n":"https://app.notion.com/p/40a0cf8fea04812c86b1ca5619a915e3","cash":True},
  {"d":"2026-11-01","t":"초월스토리 가을님 — 11월 첫째 주 촬영 일정 확정 + 콘셉트·스크립트·자료 공동 기획","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481158891d710ffaf20f8","cash":True},
  {"d":"2026-11-02","t":"11/2 16시 조윤호 PD님 통화 — 보상 3층 구조 제안, 1단계만 닫기 (통화는 11/2 17:47 진행 · 플라우드 44분)","who":"루크","p":"P1","n":"https://app.notion.com/p/40c0cf8fea0481368e89eac973bdbfc8","cash":False},
  {"d":"2026-11-02","t":"[검토] 채널 수익 배분은 4분할 — 애드센스 PD 100%, 협찬 50:50, 강의는 구간 정액","who":"루크","p":"P1","n":"https://app.notion.com/p/40c0cf8fea0481a791badce13d8a97a4","cash":False},
  {"d":"2026-11-04","t":"최은봉 대표님 회사소개서 초안 검토 → 개선안(복수 안) 작성·피드백 — 초안 수령 후 (플라우드 10/28 · 기한은 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4070cf8fea0481df9ec9fcdaee1cac2c","cash":False},
  {"d":"2026-11-04","t":"이전 대행사 성과 저조 콘텐츠 영상 링크를 조윤호 PD님께 전달 — 부진 원인 분석용 (플라우드 11/2 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40c0cf8fea048172a9d9ffbd1ab3c8a8","cash":False},
  {"d":"2026-11-05","t":"지영 원장 영업신고증·미용사 면허 종류 확인 + 성북구청 위생과 문의(2·3층 단일 영업소, 속눈썹 업종, 샵인샵 구획)","who":"루크","p":"P0","n":"https://app.notion.com/p/4080cf8fea0481aebd1de20523faf9d0","cash":True},
  {"d":"2026-11-05","t":"가을 대표님께 3주 코칭 후보 3명 연락처·참여 각오 전달 → 가을 대표님이 2명 선정 (11/4 중 전달 약속 · 플라우드 11/4 정복녀 세션)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea048159912df03bc6653048","cash":True},
  {"d":"2026-11-05","t":"가을 대표님께 손익분기 18명 사전 고지 — 촬영 전에","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481d39c18e2aba3287793","cash":False},
  {"d":"2026-11-05","t":"12월 촬영분을 11월에 당겨 찍는 일정 짜기 — PD 12월 공백","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481af98cfd6f61f374099","cash":False},
  {"d":"2026-11-05","t":"초월스토리 PD와 촬영 장소(가을님 지역 vs 서울 근교)·첫 회차 동행·현장 피드백 계획 + 채널 분산 전략(인베이더 외 채널 병행·기간 분리) 확정 (플라우드 10/28 정복녀 7기 · 기한은 노트 기재값)","who":"루크","p":"P1","n":"https://app.notion.com/p/4070cf8fea0481df9fc3f305e2ea4edb","cash":True},
  {"d":"2026-11-06","t":"이○○ 대표님 3주 집중 코칭 — 11/6(금) 14:15 세션(못 당기면 30분 숙제 검사) · 다음 주말 일정 확정 · 숙제 미이행 시 중단 조건 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481bcb208c966e1e934da","cash":True},
  {"d":"2026-11-06","t":"자동등록 — 2개/4개 묶음 신규 옵션 자동 생성·마진 자동 계산 기능 배포 + 실행 시 검정 화면 깜빡임 미노출 처리 (11/6 심○○ 대표님 보충 통화 Action Item — v241·v242에 포함됐는지 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/4100cf8fea04814083c9fad3e8231a0b","cash":False},
  {"d":"2026-11-06","t":"민트 건 광고 3,000만 — 한 번에 태우지 말고 11/20 모집 결과 보고 분할","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea048153b5dff80f24f6eb7d","cash":False},
  {"d":"2026-11-06","t":"다음 주 화/수(11/10·11/11) 저녁 조윤호 PD님 대면 식사 미팅 일정 확정 — 민트님 동석 여부 조율 (플라우드 11/2 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40c0cf8fea048140a7a9c88f9ef36179","cash":True},
  {"d":"2026-11-06","t":"심○○ 대표님 코칭 교육자료 PDF 전달 + 11/6(금) 소싱 프로그램·엑셀 보충설명 (진행 중)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea048163bf10d0ff3968dc36","cash":True},
  {"d":"2026-11-07","t":"인베이더 파트너십 최종 종료 미팅 준비 + 합의서 작성","who":"루크","p":"P0","n":"https://app.notion.com/p/40a0cf8fea0481d5bfeae583035ff37d","cash":True},
  {"d":"2026-11-07","t":"강의 PPT 초안 작성(루크·뷰셀님) → 세일즈 파트에 전달해 소구점·성과 데이터(연 200억 수강생 사례 등) 보강","who":"루크","p":"P0","n":"https://app.notion.com/p/40a0cf8fea0481e5809bd70e91b0e123","cash":True},
  {"d":"2026-11-07","t":"가을 계약서 — 출연 RS 20%를 루크 동의 없이 변경 못하게 별도 계약에 명시(제10조 2항: 배분율·공제기준 변경은 회사·강사 합의만으로 가능, 루크는 당사자 아님)","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea04810f9bc9ca630c8766bd","cash":False},
  {"d":"2026-11-07","t":"가을 파트너십 계약서에 시스템 이용료 8%(PG 공제 후) 들어갔는지 확인 — 강사용역계약서에는 출연 RS 20%만 있고 8% 없음 → 조항 확인 또는 추가 요청","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea04816eb6dfcc4487916e10","cash":False},
  {"d":"2026-11-07","t":"가을 계약서의 인터뷰 채널 출연 RS 20%가 누구 몫인지 확인 — 채널 주체·최소 의무(편수·송출량) 확정(계약서에 채널명·출연 횟수·송출량 없음)","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea0481928847f3c45cfed4cf","cash":False},
  {"d":"2026-11-07","t":"가을 6 : 루크 4 약정의 법적 형태 정리 — 회사에 공개 후 반영하거나 루크→가을 코칭 용역 대가로 별도 계약화(제18조 1항 양도 금지·제13조 비밀유지 소지)","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea0481999254cae036f1f5d7","cash":False},
  {"d":"2026-11-07","t":"3층(가을 6 : 루크 4)을 코칭·강의설계·운영자문 용역계약으로 전환 — 산정 기준은 가을이 업체로부터 수령한 금액의 40%(결과 동일, 양도금지·비밀유지·세금계산서 정리)","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea048139860ad43d71646c00","cash":False},
  {"d":"2026-11-07","t":"출연 RS 20%가 10/31 합의에 없던 점 업체에 확인 — 채널 주체·최소 출연·송출 의무 확정, 성과 연동 없으면 삭제 또는 상한(녹취 364세그먼트 전수 검색에 'RS'·'20%'·'인터뷰 채널' 없음)","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea048143b8ddc5f0e589b56a","cash":False},
  {"d":"2026-11-07","t":"토요일 상담 통화 — 개선 의지 확인 후 진행 여부 결정(메이브님이 공유한 상담 희망자)","who":"루크","p":"P0","n":"https://app.notion.com/p/40f0cf8fea0481c9817dc1d41e3aef99","cash":True},
  {"d":"2026-11-07","t":"11/6 상담 수강생 — 추석 특강 녹화 강의·소싱/프로그램 설치 링크·상담 요약본 카카오톡 전달 + 질문 접수 (기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/4100cf8fea0481778b0feb58a2206843","cash":True},
  {"d":"2026-11-07","t":"초월스토리와 카톡·줌 소통 채널 개설 + 피드백 응대 SLA 설정","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea048197acbde514d247a0c7","cash":False},
  {"d":"2026-11-07","t":"오프라인 사무실·3PL 현장 촬영 허가 규정 정리 (11월 둘째 주 촬영 전)","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481219dc8c3bf5ff892df","cash":False},
  {"d":"2026-11-07","t":"가을 대표님 스토어 소명자료 검토 — 문구 말투·인사말·개인정보 수집·이용 동의 체크 확인 후 제출 (플라우드 11/4 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea048192b515dd683e05d90d","cash":False},
  {"d":"2026-11-07","t":"박○○ 대표님께 11/5 미팅에서 논의한 신규 플랫폼 내용 메시지로 정리해 보내기 (기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40f0cf8fea0481c3bffffae0af64ddfa","cash":True},
  {"d":"2026-11-08","t":"최은봉 10월 5주차(9회차) 교육자료 발행 — 맥 배포 필요 (11/4 s09 작성·push 완료, 진행 중 · 10/29 항목과 같은 일)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea048146ba38e897aff07cb4","cash":True},
  {"d":"2026-11-08","t":"6기 수강생 두 분 후속 — 다음 주 코칭 시간 회신 · 향수 주문 처리(가품 위험 품목) · 옵션 변경법·온라인 구매 실습","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481349764f9495f286239","cash":True},
  {"d":"2026-11-08","t":"디노 원크루 자료실 첫 배포 — onecrew-dino 저장소 생성·Pages 활성화·교육자료(기본기 10과) 업로드 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea048137b4c5c8e0c403a2a8","cash":False},
  {"d":"2026-11-08","t":"메이브님과 통화 — 박○○ 대표님 새 수익 모델 설명·상의 (내년 초 진행 여부 합의)","who":"루크","p":"P0","n":"https://app.notion.com/p/40f0cf8fea0481369c55f7c075d8de74","cash":True},
  {"d":"2026-11-08","t":"창고형 매장 우리 재고로 4주 시범 판매 · 주간 매출·판매율 기록","who":"루크","p":"P1","n":"https://app.notion.com/p/3f10cf8fea048113a3d7c503eec00deb","cash":True},
  {"d":"2026-11-09","t":"자동소싱 결과의 상품 주소값·수량별 주소 번호 오류 수정 — 2주차(11/9~15) 자동등록 연동·작업지시서 안내 전 (플라우드 11/3 강의 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/40d0cf8fea04813dbf55c9361384d165","cash":False},
  {"d":"2026-11-09","t":"수강생 → 활성 셀러 전환율 실측 — 3PL 이용 수강생 수와 월 매출이 꾸준한 사람 수 (300억 가능 여부를 가르는 지표)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea04815e9d9efd7107fd5765","cash":False},
  {"d":"2026-11-09","t":"박태경 대표 강의 런칭 제안 — 가부 이번 주 내 회신 대기 (11/4 세션에서 예행연습·12월 말~1월 런칭까지 논의, 진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea048152ac78c55d13b1ec3e","cash":True},
  {"d":"2026-11-09","t":"공유용 페이지를 별도 저장소로 분리할지 결정 — luke-1b가 public이라 build.py 소스·커밋 히스토리가 열려 있음 (private 전환 / 별도 저장소 / 그대로)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481e28405e87c48dd19f4","cash":False},
  {"d":"2026-11-09","t":"가을 대표님 3주 코칭 진행 가이드 정리·전달 — 평일 5일·하루 2시간·3주, 소싱·등록 중심, 어려운 CS 문의는 확인 후 응답 (플라우드 11/4 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481bca8bad0588bd0bffd","cash":True},
  {"d":"2026-11-09","t":"11/6 상담 수강생 2차 상담(일요일경) — 자택 IP 등록·운송장 프로그램 설치·엑셀 주문 처리 교육 + 사업자등록증 발급 확인 뒤 통신판매업 신고 안내 (기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/4100cf8fea0481b8a728ea78269e7379","cash":True},
  {"d":"2026-11-09","t":"민○○ 대표님 — 운영 계정 1개 확정·테스트 상품 삭제 확인, 11/9부터 본격 등록 점검","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea0481e1be43e83d6bdc7cb0","cash":True},
  {"d":"2026-11-10","t":"뷰셀님 측 강의 기획사 미팅 일정 조율·아젠다 준비 — 돈벌쥐 PD 컨택 결과 받은 뒤","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea048145ae64ce28509af4ec","cash":True},
  {"d":"2026-11-10","t":"가을님 프로필 사진 촬영·메이크업 예약(협력사, 비용은 강의 론칭 후 정산) + 라이브 촬영일 메이크업·이동 동선 검토 (플라우드 10/28 정복녀 7기 · 기한은 노트 기재값)","who":"루크","p":"P1","n":"https://app.notion.com/p/4070cf8fea048153a073d6bed35a360d","cash":True},
  {"d":"2026-11-10","t":"가을님 프로젝트 매출 목표 1억 달성 로드맵 문서화 — 상품 등록 확대·강의·라이브 후킹·코칭 전환 (플라우드 10/28 정복녀 7기 · 기한은 노트 기재값)","who":"루크","p":"P1","n":"https://app.notion.com/p/4070cf8fea0481cd9754e5ce0c5e1acc","cash":True},
  {"d":"2026-11-10","t":"매출 인증 자료(실제 매출 캡처·송금 내역) + 수강생 성과 증빙(카톡) 취합","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481faae8cc6e9818bdb24","cash":False},
  {"d":"2026-11-10","t":"가을 대표님 스토리 콘텐츠 반영 범위 본인 확인 + 인터뷰 설계","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481f4ae17fb54dd40bb8f","cash":False},
  {"d":"2026-11-10","t":"화장품 콘셉트 4주 커리큘럼 표준화 + 6주 변형안(3주+보너스 주) 가이드 + 주간 숙제(주 1편 영상) 제도","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea04818c8fd2fa78bab6f137","cash":True},
  {"d":"2026-11-10","t":"가을 계약서 11.76% 결제 수수료 산출 근거 요율표 요청 — 카드 가맹점 수수료+PG 대행료+무이자 할부 부담 개월 수, 근거 설명 안 되면 실제 정산+상한 방식으로 변경 요청","who":"루크","p":"P1","n":"https://app.notion.com/p/40d0cf8fea0481c3bc2ac5f7ef96b41e","cash":False},
  {"d":"2026-11-10","t":"박태경 대표 한 달 상담 예행연습 세팅 — 11월부터 하루 2~3시간 수강생 상담(설치·꼬리물기) 배정·주간 시간표, 신청자 47명 중 숙제 수행·월 매출 1,000만 이상 우선 (플라우드 11/4 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea048187aff5df95f4d54391","cash":True},
  {"d":"2026-11-10","t":"심○○ 대표님 11/6 보충 후속 — 홈페이지 추천상품 소싱 시연 + 소싱 엑셀 결과로 상품 등록·슬롯 설정 함께 확인 (기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4100cf8fea0481d0a01ad68396b9b83d","cash":True},
  {"d":"2026-11-11","t":"신정현 대표님 원크루 자료실 링크 전달 + 13장 내용 검토 (onecrew-sjh 11/4 첫 배포, 진행 중)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea04818ba403d1c69c28a528","cash":True},
  {"d":"2026-11-12","t":"세무사 미팅(14:00) — 수취 주체 법인 전환·법인 매출 잡는 순서 등 세무 상의 안건 정리해서 가기 (플라우드 11/7 일정 조율 → 노션 11/9 등록)","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea04817fbc0afa80e51e196e","cash":False},
  {"d":"2026-11-12","t":"11/9 오배송 갤럭시 탭 2대(각 50만 상당, 확인 필요) 반송 요청 — 택배 기사 연락처 확인 후 · 보라님과 출고 건 교차 확인 (플라우드 11/10 운영 회의 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/4140cf8fea0481949513ca99041fa74a","cash":False},
  {"d":"2026-11-13","t":"소싱 프로그램 수량별 주소값 오류 수정 + 수강생 사이트 비밀번호 변경 기능 추가 (주소값 건은 11/9 P0 항목과 같은 일)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea0481fe9945ef1924f311f3","cash":False},
  {"d":"2026-11-14","t":"대학교 광고지 QR 4개 학교별 유입 통계 세팅 — 네이버 QR + 학교별 꼬리표 링크(?from=학교명), 통계는 홈페이지에서 통합 확인","who":"루크","p":"P0","n":"https://app.notion.com/p/4100cf8fea04817d9b17ce6116628e33","cash":False},
  {"d":"2026-11-14","t":"뷰셀님 12월 강의 일정 — 초월스토리와 공동 진행 여부 결정 + 대안 파트너 비교","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea048145a31ad5ed891507bb","cash":True},
  {"d":"2026-11-14","t":"개인 채널(퍼스널 브랜딩) 운영 니즈 문서화 → PD님께 전달해 대행 패키지·견적 산정 (플라우드 11/2 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40c0cf8fea0481be860fe196f59c25d8","cash":False},
  {"d":"2026-11-14","t":"4년 전 스스로 월백 영상 사용 허락 여부 확인 — 출연자 본인 동의","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea048143b713c52abbcee8b8","cash":False},
  {"d":"2026-11-14","t":"유○○ 대표님 — 1~2주 알고리즘 작업 후 Claude·영상 제작·업로드 교육(1~2시간) 일정 잡기","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea0481619400f5b7212de0d6","cash":False},
  {"d":"2026-11-15","t":"6기 8명 수익 계산 — 매출·인베이더 몫·광고비·순수익, 마지막 기수 정산 금액 확정 (12월 현금 공백 크기를 숫자로)","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea048166a06bffd14d3873c8","cash":True},
  {"d":"2026-11-15","t":"인베이더 해지계약서 검토 — 대기방 DB 귀속 문구·종료일·6기·4기 정산 기준·영상 자산 소유·라이브 링크 금지 확인 후 서명","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea0481adae26c839f6029000","cash":True},
  {"d":"2026-11-15","t":"스스로 월백 3,000만 회수 계산 — 1/20 라이브 전환률(과거 4%)·객단가·민트·PD 배분 뒤 루크 손익분기 결제 인원 (촬영 전에 필요 모수 확인)","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea048145945fed020684bc54","cash":True},
  {"d":"2026-11-15","t":"[결정 필요] 셀러 멤버십과 스월백 강의 판매 충돌 해소 규칙 — 강의=평생 소유 / 멤버십=월 임대(라이트 한도) · 스월백 유입자에겐 1/20 라이브 다음 날 다운셀로만 · 12월 파일럿은 인베이더 대기방만 · 민트에게 멤버십 유입 RS 소액 + 멤버십→강의 전환 시 강의 RS 그대로","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea048150a764d1f6595d1765","cash":True},
  {"d":"2026-11-15","t":"리나님 역할·조건 재정의 합의 — 스토어 전체 책임자 → 출고 책임자, 시간당 40건·정시 출퇴근, 300건 초과분 40건당 알바 1시간, 알바 미달분은 리나님 책임 (급여 조건은 싣지 않음)","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea048161ab59ea7779dbf06e","cash":False},
  {"d":"2026-11-15","t":"임원전용 운영 공유 사이트 배포 마무리 — Cloudflare Zero Trust 활성화(루크 직접) → Access 정책 '임원 이메일 허용' → 디노님·메이브님 이메일 추가·링크 공유 (진행 중 · Access 켜기 전까지 사이트 공개 상태)","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea048143944fcb5cae7793c7","cash":False},
  {"d":"2026-11-15","t":"강사님(가을 대표님) 새 닉네임 확정 — '가을' 폐기, 후보 도매언니(1순위)/창고언니, 핸들 확인 + 얼굴·실명 노출 범위","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea0481a79db1db46ae5514a9","cash":False},
  {"d":"2026-11-15","t":"가을님 화장품 소량 리셀 직접 시작(11월 3주) — 사입 → 3PL 입고 → 판매·매일 결산으로 12월 라이브용 본인 기록 확보","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea0481f78dcff3d86d1a67ab","cash":True},
  {"d":"2026-11-15","t":"가을님 코칭생 2~3명 촬영·숫자·사연 사용 동의서 받기 (촬영 전)","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea048146a0e6d2bbb6392c4d","cash":True},
  {"d":"2026-11-15","t":"강사님 12월 강의 컨셉 확정 — '화장품 도매 창고 + 올려드림'(얼굴·SNS·재고 없이 네이버 최저가로), 타겟 30~40대 경단녀","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea0481a3bce8c1dfd768f152","cash":True},
  {"d":"2026-11-15","t":"화장품 도매 창고 모델 4개 룰 설계 — 수강생 1인 SKU 배정 수·최저가 하한(마진 바닥)·월 재고 상한·창고 vs 수강생 책임선 → 정원 산출","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea04814ea200eae1842c0037","cash":True},
  {"d":"2026-11-15","t":"강사님 11~12월 수익을 모델별로 분리 기록(화장품 도매+자동등록 vs 기타 위탁) — 12월 라이브에 말할 숫자의 출처 확보","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea0481bc8cd5ef31697f20f8","cash":True},
  {"d":"2026-11-15","t":"강사님 강의 회사 채널 시청자층 확인 — 30~40대 여성인지, 아니면 타겟↔채널 어느 쪽을 맞출지","who":"루크","p":"P0","n":"https://app.notion.com/p/4120cf8fea0481c09102e91744c2fff2","cash":False},
  {"d":"2026-11-15","t":"디노님에게 물류 파트 인계 + 바코드 분류 체계 변경 적용 — 전달된 물류 메인 시트·매뉴얼 확인 (플라우드 11/10 운영 회의 결론 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/4140cf8fea0481b89963e88c89c37287","cash":False},
  {"d":"2026-11-15","t":"가을님 강의 제작 자료 전달 — 프로필 사진 구글드라이브 업로드 · 유튜브 촬영·수강생 촬영 일정 회신 · 상세페이지 자료(수강생 매출 인증·과거 사진) 정리 (플라우드 11/11 루크 메모 · 기한 추정)","who":"루크","p":"P0","n":"https://app.notion.com/p/4150cf8fea0481c6ae54cf60f4d77b3c","cash":True},
  {"d":"2026-11-15","t":"토탈샵 인테리어 업체 3~4곳 사전 상담 + 현장 실측 일정 수립 — 가벽·페인트·시트지 중심, 3층 에스테틱 룸 3개·세탁기 배수 위치 포함 (기한은 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea048119a6b8f88fe0454c87","cash":True},
  {"d":"2026-11-15","t":"에스테틱·베드 기기 조사 — 베드 2대(얼굴 구멍 개폐형·전동 여부) · 스티머·타월 온장고·왜건·아쿠아필 · 예산 상한선 (기한은 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea048179b30fc4bbe7d65bb8","cash":True},
  {"d":"2026-11-15","t":"키티티 토탈샵 3층 창문 처리 — 인테리어 협의 후 임대인에 서면 전달 (누수 책임 갈림)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fb0cf8fea048152bc00c4d7dc4e172e","cash":False},
  {"d":"2026-11-15","t":"토탈샵 브랜딩 초안 묶음 — 명함·로고 3안 · 간판 이동·외부 교체 견적 2곳 · 층별 음악 플레이리스트 2개 + 재생 기기 안","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea0481f8b60ef76c375b52bb","cash":False},
  {"d":"2026-11-15","t":"토탈샵 페르소나('블랙 앤 실버 · 영 프리미엄') 홍보 콘텐츠 기획 — '이 샵의 페르소나는?' 주제 (기한은 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea0481e48d4ee36a2ae57873","cash":False},
  {"d":"2026-11-15","t":"무료 강의 공지 · 앵콜 라이브(최소 2회) · 줌 세션 운영 계획 수립","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481a191d8d03c7609b99b","cash":False},
  {"d":"2026-11-15","t":"무료 혜택용 전자책·실무책 제작 + 배포 플랜 수립","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481c0ab02cb13ab385e5e","cash":False},
  {"d":"2026-11-15","t":"수강생 제공 프로그램 3종(소싱·자동등록·가격관리) 계정 권한 세팅·안정화 + 사용 매뉴얼 · AI 실비(건당 150~300원) · 가격 변경 1시간 주기 정책 공지","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea04811a9a21dc900e572736","cash":False},
  {"d":"2026-11-15","t":"대리등록 제공 범위(수량·계정 보안·실행 가이드) 산정 → 심화반 패키지 상품화","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481cd9ae7db83be591aff","cash":True},
  {"d":"2026-11-15","t":"수강 신청자 사전 확인 절차 — 기존 사업 경험·현재 사업 상황·참여 목적 확인 + 초급 수업 범위·기대 수준 사전 안내 (플라우드 11/3 강의 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40d0cf8fea0481579e63f7c67f256911","cash":False},
  {"d":"2026-11-15","t":"신규 수강생(11/2 밤 1회차) 2주차 코칭 — 주문서 양식·꼬리물기 심화·법규 안내","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea04814b986ef09dd6e2f034","cash":True},
  {"d":"2026-11-15","t":"2주차 강의 종료 후 소싱·사입 운영 프로그램 관련 내용 정리해 박○○ 대표님께 전달 (기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40f0cf8fea04816d9261fb9619580975","cash":True},
  {"d":"2026-11-15","t":"패시브 인컴(유통) 구조 설계 세션 준비 — 현재 숫자 3개 모으기: 3PL 이용 수강생 수·월 출고 건수·건당 단가 / 수강생 중 사입 전환 비율 / 메이븐 스토어 공급처·마진율","who":"루크","p":"P1","n":"https://app.notion.com/p/4110cf8fea0481e299b5feffcdec2779","cash":True},
  {"d":"2026-11-16","t":"역직구 파일럿 — 후보 SKU 100개 현지 최저가 비교표로 30~50개 선정 + 실적 상위 수강생 15명 선발 (90일 통과 기준은 제안값)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fe0cf8fea0481fc9889e7eeb05c1800","cash":True},
  {"d":"2026-11-17","t":"모집 광고 예산 확정 — 11/18 유튜브 광고 집행 전","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481f09e0acacf2cb65eb4","cash":True},
  {"d":"2026-11-17","t":"다마고치 모집 공고 초안 — 인원 비공개 · '각자 벌되 추이 차등' 콘셉","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea04810c9f26eb275fdf8116","cash":False},
  {"d":"2026-11-17","t":"민트님 다마고치 신청서 양식·신청자 CRM 관리안 받아 확인 — 담주초","who":"루크","p":"P0","n":"https://app.notion.com/p/4150cf8fea04812e8504dee485e8b7ec","cash":False},
  {"d":"2026-11-18","t":"'0원 다마고치' 채널을 법인 명의 구글 계정으로 개설 — 소유자는 루크(법인), 민트·PD는 편집자","who":"루크","p":"P0","n":"https://app.notion.com/p/40c0cf8fea04813c8e69ea1de97a5ca2","cash":False},
  {"d":"2026-11-18","t":"신규 유튜브 채널 '0원 다마고치' 개설 + 민트·PD 편집자 초대 — 다음 주 수요일까지 (11/11 민트님 요청)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481ff996cd49d198e87cd","cash":False},
  {"d":"2026-11-18","t":"PD·민트를 유튜브 채널 관리자로 추가 + 지표 화면 전달","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481349429f2cc10000246","cash":False},
  {"d":"2026-11-18","t":"모집영상 편집본 피드백 → 11/18 업로드·유튜브 광고 집행 (11/9 촬영 완료 · 11/13 PD 일정 공유)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481e8b4e6fd0ff8dabb71","cash":False},
  {"d":"2026-11-18","t":"카카오톡 채널(플러스친구) 개설 또는 기존 채널 공유 — 다음 주 수요일까지","who":"루크","p":"P0","n":"https://app.notion.com/p/4150cf8fea0481cb904ed4723a1b76fd","cash":False},
  {"d":"2026-11-18","t":"1/20 라이브를 지킬 수 있는 일정인지 확인 — 10/30 '에이전시 2개월 → 2월 런칭' 발언과 어긋남, 11/11 정기회의에서 1/20 고정 확인 (2월로 밀리면 현금 한 달 공백)","who":"루크","p":"P1","n":"https://app.notion.com/p/40c0cf8fea0481758297e30a5542b0dd","cash":False},
  {"d":"2026-11-18","t":"상금 300만 분배 방식 확정 — 모집 공고 전 (매주 숙제 1등 소액 / 최종 매출 1등 / 챌린지 참여자 1등)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea048187b0b7c39d065e9f90","cash":False},
  {"d":"2026-11-19","t":"11/19 화장품 제품 업체·헤어 기기 미팅 — 업체명·안건 확인 후 준비 (플라우드 11/7 일정 조율 → 노션 11/9 등록 · 토탈샵 헤어 기기 공급처 건과 같은 건인지 확인 필요)","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea0481d5b165cd8c8628c699","cash":False},
  {"d":"2026-11-17","t":"물류 직무 범위·협업 프로세스 확정 전체 회의 소집·진행 — 11/17(화), 출고 전담 vs 전체 운영 전담 결정 포함 (플라우드 11/10 물류 현안 진단 → 11/11 녹음에서 '다음 주 화요일'로 확인)","who":"루크","p":"P0","n":"https://app.notion.com/p/4140cf8fea0481349decd4bd393e6135","cash":False},
  {"d":"2026-11-17","t":"11/17(화) 물류 역할 조율 자리 전 현장 검증 — 일주일간 입고·출고·반품·전산·CS 직접 확인, 소요 시간·처리량·병목 기록 → 업무 처리 기준 정리 (플라우드 11/11 물류 녹음)","who":"루크","p":"P0","n":"https://app.notion.com/p/4150cf8fea048129888dc82dd4082f12","cash":False},
  {"d":"2026-11-20","t":"민트님 프리랜서 용역비 1회차 지급 11/20(금) — 기준일 매월 22일, 주말이면 직전 영업일 · 지급 계좌 회신 대기","who":"루크","p":"P1","n":"https://app.notion.com/p/4000cf8fea048145aee9ccd531b9c734","cash":False},
  {"d":"2026-11-22","t":"토탈샵 주말 발품 — 11월 1주 헤어(부천) · 2주 네일 · 3주 에스테틱, 한 주에 하나만","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea04818c844cff1fa73e9b9e","cash":True},
  {"d":"2026-11-28","t":"코칭 알바 한 달 뒤 수강생 4~5명 대상 라이브 출연 협의 — 1~2명 선정 목표, 불발 시 대체 시나리오 제작 (플라우드 10/28 정복녀 7기 · 기한은 노트 기재값)","who":"루크","p":"P2","n":"https://app.notion.com/p/4070cf8fea0481169f7cc8b84f35d9c8","cash":True},
  {"d":"2026-11-30","t":"모든 수취 주체를 힐링디어스 법인으로 전환 — 가을 1층 8%·민트 건·메이븐 기수 정산을 법인 명의로 (세무사 확인 필요)","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea048119b5d8e052db84f19d","cash":False},
  {"d":"2026-11-30","t":"메이븐·디노와 주주간계약 체결 — 베스팅 4년+1년 클리프(루크 포함 전원)·드래그얼롱·우선매수권, 변호사 작성","who":"루크","p":"P0","n":"https://app.notion.com/p/40e0cf8fea0481899418d7cdb999df48","cash":False},
  {"d":"2026-11-30","t":"[결정 필요] 수익을 힐링디어스 법인으로 모으는 전환 계획 — 어느 수익줄(강의·컨설팅·3PL·툴박스)부터 법인 매출로 잡을지, 언제부터 (세무사와 같이)","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea0481bc9957e923998c0439","cash":True},
  {"d":"2026-11-30","t":"[결정 필요] 물류 수익에 루크·법인 몫이 없는 구조 — 엑시트 핵심 자산(3PL)의 매출이 법인 밖으로 나가는 문제, 배분 전에 법인 매출 경로 먼저","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea048163b8eef50d67cae2fc","cash":True},
  {"d":"2026-11-30","t":"가을 대표님 런칭 기획(11월, 루크) — 초월스토리에서 메이븐 플랫폼 수익 모델 그대로 적용 · 11월 안에 기획·커리큘럼·가격 확정 (진행 중)","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea04818aa26cfa7f3020ab3b","cash":True},
  {"d":"2026-11-30","t":"보험·적금 모델 구조 확인 — 수강생 DB 제3자 제공 마케팅 동의 유무 · 모집 자격(설계사/대리점 등록) · 수수료 환수(중도해지 시 반환) 조건 · 수수료 수령 주체(법인/개인)","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea048151a74fc730231615a3","cash":True},
  {"d":"2026-11-30","t":"셀러 멤버십 파일럿 설계 확정 — 9월 '멤버십+공급형' 기획서 v0.1 기반, 12월 창립 멤버 50명(대기방 10개 · 월 2.9만 · 주간 공급 상품 10개 + 프로그램 + 3PL 옵션 · 노코드) · 위너/슬롯 규칙·반사입 원칙·KPI(3개월 유지율 70%)","who":"루크","p":"P0","n":"https://app.notion.com/p/4110cf8fea048130812ed113351546f8","cash":True},
  {"d":"2026-11-30","t":"메이크업헬퍼 12주 테스트 9주차 판정 (11월 말)","who":"루크·최은봉","p":"P1","cash":True},
  {"d":"2026-11-30","t":"토탈샵 전원 직원(고정급) 구조 손익 버전 계산 — 9월 파트너 정률안과 나란히(12월 결정 묶음용), 가격표(11월 말) 이후","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea0481daab23ee4bec466fce","cash":True},
  {"d":"2026-11-30","t":"토탈샵 초기 투자 재계산 — 필요 현금·회수 대상 산출, 인테리어 견적 3곳 받은 뒤 실가로 교체 (월별 현금 12월·1월·2월)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea0481ceb886cb95c2c21669","cash":True},
  {"d":"2026-11-30","t":"토탈샵 직원 급여 기준 확정 — 파트별 기본급+인센티브, 사업주 비용 ×1.18 · 손익분기 인원(헤어 월 108명·네일 48·에스테틱 39) · 11월 가격표 뒤 공고 시세로 재검증","who":"루크","p":"P1","n":"https://app.notion.com/p/3fd0cf8fea0481168756dfa2f799cd1c","cash":True},
  {"d":"2026-11-30","t":"1월에 떨어지는 수입 하나 더 만들기 — 순현금 마이너스 구간","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481979785f80df4d8c08e","cash":False},
  {"d":"2026-11-30","t":"메이븐 5기 정산이 1월인지 2월인지 확인","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481dbb13bf0b9dfe23fa6","cash":False},
  {"d":"2026-11-30","t":"인베이더 없이 메이븐 기수를 돌릴 수 있는지 판단 — 연 1.2억이 걸린 질문","who":"루크","p":"P1","n":"https://app.notion.com/p/4020cf8fea0481179854dbf9a4b3785c","cash":False},
  {"d":"2026-11-30","t":"3PL 위탁·사입 운영 프로세스 표준화(주문서 연동·발송 SLA) + 사입 전환 온보딩 가이드·위탁/사입 비교 자료","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481bdbdaad969b8af3d93","cash":False},
  {"d":"2026-11-30","t":"수강생 재고 처리 지원 프로세스(공동구매·수강생 간 교환·오프라인 판매·운영 측 매입) 문서화","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea04812f8fc2d20d376f3120","cash":False},
  {"d":"2026-11-30","t":"스마트스토어 카탈로그 자동 매칭 프로그램 운영 + 베스트 소싱 매뉴얼 제작","who":"루크","p":"P1","n":"https://app.notion.com/p/40a0cf8fea0481c98e8be63a3fcacfd8","cash":False},
  {"d":"2026-11-30","t":"가을 기수 광고·운영비 상한을 운영자 자격으로 요구 — 기수별 상한 합의와 집행 전 공유(제4조 9항은 사전 공개·승인 요건 없음, 비용 167만마다 손익분기 1명 상승)","who":"루크","p":"P1","n":"https://app.notion.com/p/40d0cf8fea0481e2a5dfe0139c613190","cash":False},
  {"d":"2026-11-30","t":"물류 수익 배분·3PL 이용료 구체화 — 파레트 단위 등 3PL 요금 · 외부 고객 유치 보상 · 오프라인 판매 수익·회사 환원 · 성과급 구조, 물류 담당 파트너와 협의 (플라우드 11/3 물류 회의 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40d0cf8fea0481459ed7c7f5b2bfe046","cash":True},
  {"d":"2026-11-30","t":"다마고치 11월 말까지 모집·선정 완료","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea0481d6ad50c57a27cbcef8","cash":False},
  {"d":"2026-11-30","t":"본편 5편 회차별 구성 확정 — 민트 빈칸 기획안 같이 채우기","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea0481849235eb99659d2805","cash":False},
  {"d":"2026-11-30","t":"보부상님 엑시트 상세 5가지 파악 — 본명·채널·법인 / 300억이 현금인지 언아웃 포함인지 / 무엇을 팔았나 / 매각 시점 매출·영업이익 / 인수자 유형","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea04815d9afce90e4024e191","cash":False},
  {"d":"2026-11-30","t":"박태경 대표 강의 런칭 — 기본 틀·기획안 초안 작성, 대표님 경험·화법에 맞게 직접 다듬도록 전달 (플라우드 11/4 · 런칭 12월 말~1월 잠정 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea0481c6809ec28b9bbcd1b5","cash":True},
  {"d":"2026-11-30","t":"박태경 대표 강의 런칭 협력 업체 미팅·조건 확인·최종 선정 + 런칭 일정(12월 말~1월) 구체화 (플라우드 11/4 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/40e0cf8fea048199ac2dd182a4fee333","cash":True},
  {"d":"2026-11-30","t":"돈벌쥐 PD 연결 에이전시 미팅 잡기 — 박○○ 대표님 안과 조건 비교","who":"루크","p":"P1","n":"https://app.notion.com/p/40f0cf8fea0481fc9909c08ab0b45dd8","cash":True},
  {"d":"2026-11-30","t":"쇼핑몰 5곳 구매 교육자료(HTML 5장+목차+PDF) 완성 → 루크 검토·빠진 화면(결제 직후·앱 알림) 직접 캡처","who":"루크","p":"P1","n":"https://app.notion.com/p/4100cf8fea04813f8794cadafe0a1440","cash":False},
  {"d":"2026-11-30","t":"보부상 300억 엑시트 사례 확인 — 매출 규모·수익률·인수자가 산 것(수강생 DB / 강사망 / 브랜드) 세 가지를 업계 지인에게 묻기","who":"루크","p":"P1","n":"https://app.notion.com/p/4110cf8fea048141ac5cf913bc3ff77d","cash":True},
  {"d":"2026-11-30","t":"창고 택배비 결제 개통을 툴박스 보류와 분리할지 결정 — 통판 신고는 어차피 필요(유료 판매 전부)","who":"루크","p":"P1","n":"https://app.notion.com/p/4110cf8fea0481f68415ee56be929768","cash":False},
  {"d":"2026-11-30","t":"금융상품 제휴 전 확인 — 미등록자가 가입 건당 수수료를 받아도 되는지(보험업법 모집수수료 금지), 정액 광고·콘텐츠비 구조로 바꿔야 하는지 — 보험 전문 변호사 또는 금감원 안내로","who":"루크","p":"P1","n":"https://app.notion.com/p/4110cf8fea048195bae0d059367fe347","cash":True},
  {"d":"2026-11-30","t":"[검토] 상품 등록 대행 서비스 — 멤버십 프로 티어/애드온(월 50개 49,000 안) · 스마트스토어 매니저 권한으로 접근 · 자동등록 프로그램으로 B 엔진 직원이 수행 · 제재 책임·수량 한도 약관 — 10/31 '대리등록 수십 개' 항목과 통합","who":"루크","p":"P1","n":"https://app.notion.com/p/4110cf8fea048139a7f2fa9e81fa3000","cash":True},
  {"d":"2026-11-30","t":"매뉴얼 v1.2 반영 요청 — 2중 카트 입고 동선·선반 즉시 정리·사서함 단위 포장·300건 기준 타임테이블·미출고 플로우(출력→출고→미출고 입력→시스템 판정→수강생 확인)","who":"메이브님","p":"P1","n":"https://app.notion.com/p/4120cf8fea0481eaa4efc4aa7132209d","cash":False},
  {"d":"2026-11-30","t":"바코드 통합재고 수강생 약정서 초안 — 변상 기준(시점·단가)·재고 인수 조건·소유권 귀속·FIFO 혼입 동의","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea048102b0b4f08d67b3227d","cash":False},
  {"d":"2026-11-30","t":"물류 시스템 과제 4건 — ① 출고 취소 차단(13시 이후 자동 거절) ② 수강생 셀프 조회·챗봇(입고·재고·송장) ③ 미출고 자동 판정 ④ 바코드 통합재고","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea048177a2c2f2c7fa515531","cash":False},
  {"d":"2026-11-30","t":"가을님 유튜브 촬영 플랜 확정 — 가을님 2~3편(사연·실전·코칭생 첫 주문) + 코칭생 2~3명 × 1~2편(인터뷰, 가을님이 질문자) · 11월 3~4주 촬영","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea0481c19fffd8ba3f6408e4","cash":False},
  {"d":"2026-11-30","t":"가을님 라이브 PPT 제작 — 7구간(사연→증거→실연 1건→구조→리스크→정원→루크 보증) 한 장 한 문장, 메이브님 PPT와 다른 톤","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea048124b559e7296dada9f5","cash":True},
  {"d":"2026-11-30","t":"메이브님과 화장품 강의 내부 영역 분리 합의 — 공개적으로는 가을님을 별개 인물로(교차 언급 없음), 내부는 소량 리셀(가을) vs 물량·풀필먼트(메이브)","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea04817d86fafe4bc775a2d4","cash":True},
  {"d":"2026-11-30","t":"등록 대행 티어·요금 구조 결정 — 셀프(프로그램) / 올려드림(100개) / 맡김(300개+가격관리), 강의료와 분리된 서비스 요금으로 갈지","who":"루크","p":"P1","n":"https://app.notion.com/p/4120cf8fea0481019ba2db89b8cd9e4d","cash":True},
  {"d":"2026-11-30","t":"강의 종료 후 재고조사 일정 잡기 · 상품별(바코드) 통합 재고 정리 검토 (플라우드 11/10 운영 회의 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4140cf8fea0481f9a73ff7055f7489cf","cash":False},
  {"d":"2026-11-30","t":"입고 리스트 기준 도입 — 수강생이 카탈로그명·운송장 번호 직접 입력, 사전 정보 없는 물품 처리 기준(3PL·배대지 방식 참고) + 입고 리스트 기반 자동 처리 프로그램 (플라우드 11/10 운영 회의 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4140cf8fea0481e7bef5d0a9cf9f4049","cash":False},
  {"d":"2026-11-30","t":"물류 센터 현장 견학(2~3일~1주) 기획·일정 조율 — 대량 물류 운영 흐름 습득 (플라우드 11/10 물류 현안 진단 · 11/3 현장 실습 건과 같은 건인지 확인 필요 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4140cf8fea0481db92eae7b75bdb35f4","cash":False},
  {"d":"2026-11-30","t":"신규 강사 복수 플랫폼 배치 검토 — 11월 중 플랫폼 1~2곳 확인 · 촬영 PD 통해 '타이탄' 측 연결 가능 여부 · 초월스토리 등 진행 결과 확인 뒤 배치 방향 결정 (플라우드 11/10 운영 회의 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4140cf8fea04810f825cf07fe8f9656c","cash":True},
  {"d":"2026-11-30","t":"PD 15%의 '순수익' 정의·경비 상한·환불 정산을 민트 계약서 배분 기준액과 맞추기","who":"루크","p":"P1","n":"https://app.notion.com/p/4150cf8fea0481e2bc26c492f463e5d8","cash":True},
  {"d":"2026-11-30","t":"물류 창고 배치·전산·운영 자료를 신규 인력이 처음 봐도 3일 안에 적응할 수준으로 단순화 검토 (플라우드 11/11 물류 녹음 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4150cf8fea0481ac9c1cf623e2fb2519","cash":False},
  {"d":"2026-11-30","t":"토탈샵 사업자 분리 등록 준비 — 서비스별(헤어·메이크업·네일·에스테틱) 공간 구획 + 각 사업자 임대차(또는 전대차) 계약·영업허가증 준비 → 세무대리인에게 전달해 등록·업종 코드 재확인 (플라우드 11/12 세무사 상담 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4160cf8fea0481ab8d16e4b9989a73aa","cash":False},
  {"d":"2026-11-30","t":"토탈샵 인테리어 공사비 — 사업자별 매입세금계산서 발급·환급 방식 + 간이과세 포기·일반과세 전환 여부를 세무대리인과 확인 (플라우드 11/12 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4160cf8fea048108a92fd91e29477da4","cash":False},
  {"d":"2026-11-30","t":"토탈샵 인력 운용 서류 — 표준 근로계약서·프리랜서 계약서 샘플 검토·작성 → 세무대리인 전달 + 사업 지출(식대·교통비 등) 구분 기록 시작 (플라우드 11/12 · 기한 추정)","who":"루크","p":"P1","n":"https://app.notion.com/p/4160cf8fea0481d89ee7fb6dd00fb486","cash":False},
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
  {"d":"2026-11-30","t":"종소세 중간예납 고지 확인 후 납부 (개인 명의 소득 있을 때 · 고지서 11월 초)","who":"루크","p":"P2","n":"https://app.notion.com/p/3f80cf8fea048180b6a8fc35879b82d1","cash":False},
  {"d":"2026-11-30","t":"역직구 위너 시스템 — 개발 전 수동 파일럿으로 가격 경쟁력 검증 (1개 마켓·1개 카테고리·SKU 30~50개·수강생 10~20명)","who":"루크","p":"P2","n":"https://app.notion.com/p/3fe0cf8fea04811d871fe60944c87ae4","cash":True},
  {"d":"2026-11-30","t":"지역 당일 직배송 테스트 — 배달 플랫폼(쿠팡이츠·배민) 연계, 배송비 2,000원 선·30~60분 (플라우드 10/19 · 기한 추정)","who":"루크","p":"P2","n":"https://app.notion.com/p/3fe0cf8fea0481149b83d52e9a5287ee","cash":True},
  {"d":"2026-11-30","t":"30대 목표 달성 노션 템플릿 v1 (액션보드 간소화판)","who":"루크","p":"P2","n":"https://app.notion.com/p/4020cf8fea04813682c0ce397533f286","cash":True},
  {"d":"2026-11-30","t":"리셀 윤리 가이드(타 셀러 복제 금지 등) 제정 + 법적·민원(톡톡·상세페이지) 대응 템플릿 최신화","who":"루크","p":"P2","n":"https://app.notion.com/p/40a0cf8fea04810880f2f06d85822dfe","cash":False},
  {"d":"2026-11-30","t":"숏폼 등 유통 외 부업형 강의 모델 설계 + 추가 강사 후보군 탐색","who":"루크","p":"P2","n":"https://app.notion.com/p/40a0cf8fea04818aa4d9dc8482f99f47","cash":True},
  {"d":"2026-11-30","t":"50대 성과 강사(월 매출 5천 사례) 런칭 — 연내 추진 여부·일정·패키지 협의","who":"루크","p":"P2","n":"https://app.notion.com/p/40a0cf8fea0481478ed5d6885217e212","cash":True},
  {"d":"2026-11-30","t":"김한준 PD 편당 100만에 편집이 포함인지 확인","who":"루크","p":"P2","n":"https://app.notion.com/p/40e0cf8fea0481589163edeaa98c89cd","cash":True},
  {"d":"2026-11-30","t":"11/10 상담 수강생 재상담 시 확인 — 6개월 이상 운영 가능 여부 · 『인간관계론』 독서 · 무료 콘텐츠로 실제 소싱·상품 등록 실행 내용 (플라우드 11/10 상담 30분 · 재상담 일정 미정, 기한 추정)","who":"루크","p":"P2","n":"https://app.notion.com/p/4140cf8fea0481e49122e82d395c3597","cash":False},
  {"d":"2026-12-03","t":"11월 제작경비 시트 기입 확인(11/30) → 12월 초 3영업일 내 일괄 입금 — 매월 반복","who":"루크","p":"P1","n":"https://app.notion.com/p/4150cf8fea0481d8ac37c538934a9b05","cash":True},
  {"d":"2026-12-10","t":"뿌요 90일 결산 상담 — 300만 달성 여부·거취 결정","who":"루크","p":"P3","n":"https://app.notion.com/p/3d80cf8fea0481d69c3de62608ad02ac","cash":True},
  {"d":"2026-12-31","t":"루크 툴박스 구독 500명 목표 / 3PL 판매 실적 정리(내년 강의 증거)","who":"루크","p":"P1","cash":True},
  {"d":"2026-12-31","t":"키티티 토탈샵 12/31 잔금일 현금 준비 — 권리금·보증금 잔금 + 중개수수료 (금액은 공개 페이지에 싣지 않음)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fb0cf8fea0481d7a484f3ac31e7ae28","cash":True},
  {"d":"2026-12-31","t":"회사 자체 강의 기획 (3PL 판매 실적 연계)","who":"루크","p":"P2","n":"https://app.notion.com/p/3de0cf8fea0481b9821dc015183213b4","cash":True},
  {"d":"2026-12-31","t":"초창패 PSST 계획서 초안 12월 안에 완료","who":"루크","p":"P2","n":"https://app.notion.com/p/3ef0cf8fea0481859a20e212db58d884","cash":True},
  {"d":"2026-12-31","t":"메이븐 스토어 4분기 순수익 월 1,000만","who":"메이브님","p":"P2","n":"https://app.notion.com/p/3f10cf8fea04811aa006c92f5797461a","cash":True},
  {"d":"2026-12-31","t":"1월 신규 강의 런칭 준비 (11월 강의 종료 후 12월 준비 기간)","who":"메이브님","p":"P2","n":"https://app.notion.com/p/40f0cf8fea0481d881c2f4c25b65708b","cash":True},
  {"d":"2026-12-31","t":"자체 무료 도구(연출컷메이커·마진메이커 등)로 '댓글 키워드 → 무료배포 → 카톡/카페 가입' 쇼츠 퍼널 테스트 (유튜브 리드 퍼널)","who":"루크","p":"P2","n":"https://app.notion.com/p/4110cf8fea048146abc7c8ca9ac089cf","cash":False},
  {"d":"2026-12-31","t":"[검토] 저축 스몰 챌린지(한 달에 얼마씩 모으기) — 목표 실행 챌린지 대신 검토, 셀러 커뮤니티와 연결('번 돈 남기기')할지 별도 브랜드로 갈지 결정","who":"루크","p":"P2","n":"https://app.notion.com/p/4110cf8fea0481628bbcf7e5259e7be9","cash":False},
  {"d":"2027-01-31","t":"1분기 실측 두 숫자 — 실제 CAC(광고비 ÷ 카페 신규 회원) · 실제 전환율(본 강의 구매자 ÷ 카페 회원) · 전자책 전환율 (연간 루크 몫 1.54억~7.14억은 가정값)","who":"루크","p":"P1","n":"https://app.notion.com/p/3fc0cf8fea0481d1acf1ed16928d5a27","cash":True},
  {"d":"2027-01-31","t":"꼬마빌딩 담보대출 심사 전에 대표자 신용 정리 마치기 (잔금은 2027-03-16 이후)","who":"루크","p":"P2","n":"https://app.notion.com/p/3f20cf8fea048176bc01e7f629aa7309","cash":True},
  {"d":"2027-01-31","t":"물류 담당 파트너 이사 등재 시점·권한·수익 배분 협의 — 2027년 초 본사 서울 이전·회사 신고 시점에 맞춰 (플라우드 11/3 물류 회의 · 기한 추정)","who":"루크","p":"P2","n":"https://app.notion.com/p/40d0cf8fea04813093f4d61f93e85ee9","cash":False},
  {"d":"2027-03-16","t":"서울 꼬마빌딩 잔금은 2027-03-16 이후로 — 용도로는 중과를 못 피함","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea048189a9b5cdd665a5cd92","cash":False},
  {"d":"2027-03-16","t":"꼬마빌딩 취득은 2027-03-16 이후로 — 설립 5년 충족일","who":"루크","p":"P2","n":"https://app.notion.com/p/3f10cf8fea04819f838bcf83d9a08e94","cash":False},
]


SHARED_SITE = "스스로 월백 프로젝트"

HEAD_S = """<!DOCTYPE html>
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
<div class="top"><span>{site}</span><span>갱신 {updated}</span></div>
"""

FOOT_S = """
<div class="foot">{site} · 갱신 {updated}</div>
</div>
<script>
(function(){
  function kd(ms){return new Date(ms).toLocaleDateString('en-CA',{timeZone:'Asia/Seoul'});}
  function pad(n){return n<10?'0'+n:''+n;}
  function tick(){
    var now=Date.now(), els=document.querySelectorAll('[data-due]');
    for(var i=0;i<els.length;i++){
      var el=els[i], due=Date.parse(el.getAttribute('data-due'));
      if(isNaN(due)) continue;
      var dn=Math.round((Date.parse(kd(due)+'T00:00:00+09:00')-Date.parse(kd(now)+'T00:00:00+09:00'))/86400000);
      var diff=due-now, a=Math.abs(diff);
      var d=Math.floor(a/86400000), h=Math.floor(a%86400000/3600000), m=Math.floor(a%3600000/60000), sc=Math.floor(a%60000/1000);
      el.classList.remove('soon','urgent','past');
      var cd=(d?d+'일 ':'')+pad(h)+':'+pad(m)+':'+pad(sc);
      if(diff<0){ el.classList.add('past'); el.innerHTML='<span>D+'+Math.abs(dn)+'</span><span class="cd">'+cd+' 지남</span>'; }
      else{ if(dn<=0) el.classList.add('urgent'); else if(dn<=2) el.classList.add('soon');
        el.innerHTML='<span>'+(dn===0?'D-DAY':'D-'+dn)+'</span><span class="cd">'+cd+' 남음</span>'; }
    }
  }
  tick(); setInterval(tick,1000);
  document.addEventListener('DOMContentLoaded',tick);
})();
</script>
</body>
</html>
"""

def page_shared(title, body):
    """외부 공유용 — 대시보드 백링크·완료체크·출처 링크 없음."""
    return (HEAD_S.replace("{title}",title).replace("{site}",SHARED_SITE)
            .replace("{css}",CSS).replace("{updated}",UPDATED)
            + body
            + FOOT_S.replace("{site}",SHARED_SITE).replace("{updated}",UPDATED))


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
    <li data-n="https://app.notion.com/p/4110cf8fea0481bc9957e923998c0439"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 수익을 힐링디어스 법인으로 모으는 전환 계획 — 어느 수익줄(강의·컨설팅·3PL·툴박스)부터 법인 매출로 잡을지, 언제부터 (11/30 P0)</div><div class="m">11/7 낮 채팅(액션보드 대정리) 노션 새 항목 · 법인 매출이 없으면 엑시트 논의 자체가 성립 안 됨 — 전환 순서와 시작일 확정, 세무사와 같이 · 같은 날 [결정 필요] 2건 더(아래) · <a href="exit300/">300억 엑시트 — 가능한가</a></div></li>
    <li data-n="https://app.notion.com/p/4110cf8fea048163b8eef50d67cae2fc"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 물류 수익에 루크·법인 몫이 없는 구조 — 엑시트 핵심 자산(3PL)의 매출이 법인 밖으로 나가는 문제, 배분 전에 법인 매출 경로 먼저 (11/30 P0)</div><div class="m">11/7 노션 새 항목 · 기대 결과: 3PL 매출이 힐링디어스 매출로 잡히고 그 안에서 배분 · 11/7 [결정] 디노 합류 — 물류 책임자, 물류 수익은 메이븐+디노+리나님 구조 가능성, 리나님 역할 정리는 더 보고</div></li>
    <li data-n="https://app.notion.com/p/4110cf8fea048150a764d1f6595d1765"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 셀러 멤버십과 스월백 강의 판매 충돌 해소 규칙 — 강의=평생 소유 / 멤버십=월 임대(라이트 한도) · 스월백 유입자에겐 1/20 라이브 다음 날 다운셀로만 · 12월 파일럿은 인베이더 대기방만 · 민트에게 멤버십 유입 RS 소액 (11/15 P0)</div><div class="m">11/7 노션 새 항목 · 기대 결과: 민트에게 설명할 수 있는 한 장 — 멤버십은 강의 경쟁자가 아니라 라이브 미결제 96%를 잡는 2차 퍼널 · 같은 날 P0 '셀러 멤버십 파일럿 설계 확정'(11/30)과 묶음</div></li>
    <li data-n="https://app.notion.com/p/4000cf8fea04812394e8d9f178a0c95d"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 원크루 사이트 아이디어 점검 — 루크가 Supabase(공방 프로젝트)에 로그인해 표 만들기 SQL(migrations/0002) 한 번 실행 → 회원 아이디어 점검 화면이 열림</div><div class="m">10/21 상황판 '막힘' 보고(사업 아이디어 점검 — 회차 주고받기, 클로드 코드 직접 push) · 노션 P0 2건(진행 중 · 시작 전) · 클로드가 크롬으로 대신 하려 했으나 Supabase 로그인이 풀려 있어 멈춤 · 표 둘(crew_idea_threads · crew_idea_rounds) + crew_members에 drive_url 칸, 기존 표는 안 건드림 · <a href="status/?p=원크루 사이트">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481b3bd6dc3d1bfd8fa95"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 루크 툴박스 결제 — 포트원 결제사를 가입비 무료인 곳(KG이니시스)으로 확정하고 신청서 제출 · 070 번호 받기 · 통신판매업 신고번호·환불 기준 확인</div><div class="m">10/7 상황판 '막힘' 보고 11건(토스 연결 점검 → 토스 신청 멈춤 권고 → 포트원으로 결정 → 약관·개인정보처리방침·환불안내 배포, 결제 심사 사전 점검 8/9 통과) · 포트원 이용료는 월 거래액 5,000만원까지 무료, 결제사 가입비는 두 곳만 무료 · 토스는 테스트 키 상태라 지금은 손님이 결제해도 청구가 안 됨 — 실결제 전까지 프로그램 구매 길을 막을지도 결정 · 사업자등록증은 옛 주소본이라 홈택스 재발급 필요 · <a href="status/?p=루크 툴박스">상황판</a> · <b>11/7 [결정] 툴박스 잠정 보류</b>(거인의 도구공방 → 박○○ 대표님 수익 모델 강화로 전환) — 창고 택배비 결제 개통을 툴박스 보류와 분리할지는 노션 새 항목(11/30 P1)으로 따로 결정</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481a89c87d347be379b54"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 원크루 사이트 자동 배포 — 크롬 'Confirm access' 탭에서 깃허브 비밀번호 입력 후 Confirm (루크 클릭 한 번)</div><div class="m">10/6 상황판 '막힘' 보고 · Vercel에 깃허브 로그인 연결은 끝났고, 원크루 사이트 저장소 접근 권한 단계에서 대기 · 그동안 크루 자료는 수동 배포 중 · <a href="status/?p=원크루 사이트">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea048152b55cec152c0f6fc9"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 사업 구조화 페이지 4건 — 루크가 깃허브에서 저장소 만들고 Pages 켜기 (지영 원장 kittiti-jiyoung · 신정현 대표 onecrew-shin-jeonghyeon · 정복녀 대표님 · 최은봉 대표님 onecrew-ceb-fxddzyg9)</div><div class="m">10/7 노션 '[막힘]' 항목 · 페이지는 각 채팅에서 만들어 두었고 저장소가 없어 push 대기 · 공개 저장소 생성 → Pages(main / root) → Claude 깃허브 앱 권한 추가 · 기한 10/7~10/12 · 정복녀 대표님 저장소 이름은 기록에 없어 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea04818a937efb1274c10b22"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 키티티 AI 상담 — GPT 연결용 OpenAI API 키 발급(루크) · 원장님께 상담 정책 10가지 답 받기</div><div class="m">10/5 상황판 '막힘' 보고(상담실장 페르소나·가상 손님 9명 시험) · ChatGPT 구독과 API 키는 별개 — 키만 넣으면 연결되도록 코드는 준비됨(실제 호출은 미확인) · 정책 10가지: 소요 시간·2인 예약·할인·출장·결제·아기 동반·헬퍼/환복·토요일 오후·본식 업스타일·클래스 · <a href="status/?p=키티티 상담 사이트">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048144b71af1d096a2f0a2"><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 루크 툴박스 — 자동화 도구 판매 조건(환불 기준·설치 대수·윈도우/맥·네이버 계정 처리·결제 방식) · 원크루 페이지 결정 5가지 + 루크 사진·영상</div><div class="m">10/5 상황판 '막힘' 보고(도구 구매 검토 회의) · 도구가 눈에 안 보임 1.6/5, 99만원 이상 구매 의향 2명(조건부) · 원크루 페이지 결정 5가지: 2명 고정·안심 문구·빚 문구·평생 범위·계산기 3년 · 도구 1단계(준비 중 표시 정리·로그인 전 상세)는 클로드가 바로 가능 · <a href="status/?p=루크 툴박스">상황판</a> · <b>11/7 [결정] 툴박스 잠정 보류</b> — 판매 조건 결정은 보류 상태(노션 항목은 P1 미완료 그대로)</div></li>
    <li><span class="tag p0">결정 필요</span><div class="t">[결정 필요] 헤메네일 — 카카오 지도에 없는 매장을 순위에 소폭 반영할지</div><div class="m">10/4 상황판 '막힘' 보고(폐업 의심 매장 순위 내리기) · 함께 물었던 상가(상권)정보 대조·전화번호 표시·가격 최신화는 10/5 노션에서 완료 처리됨 · 이 건은 결정 기록이 없어 확인 필요 · <a href="status/?p=헤메네일">상황판</a></div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048141a4aee0ab6b56da87"><span class="tag p0">결정 필요</span><span class="tag cash">현금</span><div class="t">[결정 필요] 키티티 정부지원 — 초창패 본선 + 모두의 창업 보험으로 갈지 · 이종 사업자 등록 방식(업종 추가 vs 새 사업자)</div><div class="m">10/4 노션 [보고] '정부지원 전략 v13' 메모의 '[막힘] 루크 결정 필요' (노션 상태는 완료) · 다음: 창업진흥원 1357·세무사 확인, 트랙(일반/기술 vs 로컬) 결정 · <a href="reports/kititi-grant-strategy/?v=13">보고서</a></div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea0481ff996cd49d198e87cd"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">스스로 월백 리턴즈 — 유튜브 다마고치로 셀러를 모아 1/20 세일즈 라이브로 전환(4년 전 '스스로 월백' 리부트) · 루크(멘토·출연) / 민트(기획·퍼널·광고) / 조윤호 PD(촬영·편집) · 정기회의 매주 수 13시 줌(10/30 킥오프 · 11/4 · 11/11) · <b>11/9(월) 모집영상 청문회 콘셉트로 촬영 완료</b>(1안 11/10보다 하루 앞당김) · <b>11/11 의결</b>: 윤호 PD 보상 = 프로젝트 순수익 15%(순수익 = 광고비·제작비 및 운영비·환불금액 제외, 강의 모집일 기준 익월 10일 입금) · 제작경비는 공유 시트에 월말까지 기입 → 루크가 월초 3영업일 내 일괄 입금, 순수익에서 제외 · 11/13(금) PD 편집·업로드 일정 공유 → <b>11/18 업로드·유튜브 광고</b> → 다마고치 미팅·첫 촬영 11월 말~12월 초 → 2027-01-20 라이브 · <b>루크 다음 주 수요일(11/18)까지</b>: 신규 유튜브 '0원 다마고치' 개설(법인 계정 · 민트·PD 편집자) · 카카오톡 채널(플러스친구) 개설 또는 공유 · 민트는 신청서 양식·CRM 담주초</div><div class="m"><b>확정(10/30·11/4)</b>: 본편 5화 + 모집영상 1편 · 타깃 40대 초 · 유튜브는 월 순수익 100만까지 · 상금 300만 매출 기준 · 다마고치 최대 2명·인원 비공개 · 30일 챌린지 · 구성작가 없음 · 구글 광고 중심 · <b>미결</b>: 상금 분배(11/18) · 광고 예산(11/17) · 본편 회차별 구성(11/30) · '0원 다마고치'와 셀러들의 수다 공동작업자 연결 유지 여부(11/4 결정은 '스스로 월백' 채널 기준) · 1/20 고정 재확인(11/18 — 첫 촬영이 12월 초면 본편 5편을 6주에) · <b>11/11 의결의 빈 곳</b>(노션 11/30): '운영비'에 민트 용역비·PG·상금이 들어가는지 · 15%를 민트 6:4 전에 떼는지 · 2/10 입금 뒤 환불 시 회수 조항 없음 · 경비 시트에 월 상한·사전 승인 없음 · 공유 회의록 <a href="meetings/">스스로 월백 회의록</a>(11/11 페이지 추가 — 배분·입금 수치와 경비 시트 링크는 싣지 않음) · 채널 개설 방법은 클로드 페이지 '0원 다마고치 채널 개설'(11/11)</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea04815e9d9efd7107fd5765"><span class="tag p0">P0</span><div class="t">300억 엑시트(11/4 클로드 페이지 <a href="exit300/">300억 엑시트 — 가능한가</a>) — 수강생 → 활성 셀러 전환율 실측(11/9 · 300억 가능 여부를 가르는 지표: 풀 5,400명 기준 37%면 288억, 10%면 78억 — 가정값) · 모든 수취 주체를 힐링디어스 법인으로 전환(11/30 · 가을 1층 8%·민트 건·메이븐 정산을 법인 명의로, 세무사 확인) · 메이븐·디노와 주주간계약(11/30 · 베스팅 4년+1년 클리프 전원 적용·드래그얼롱·우선매수권, 변호사 작성) · 보부상님 엑시트 상세 5가지 파악(11/30 P1 · 공개 보도 검색 안 됨)</div><div class="m">11/4 노션 새 항목 4건(목표 칸 비어 있음) · 메모: 2년째 법인 매출이 거의 없고 수익이 인베이더·메이븐·초월스토리를 거쳐 개인·파트너 계산으로 흩어짐 — 인수자는 법인의 반복 가능한 수익을 삼, 2년 치 재무제표가 쌓여야 함 · <b>11/7 새 항목</b>: [결정 필요] 수익 법인 전환 계획(11/30 P0) · [결정 필요] 물류 수익 구조(11/30 P0) · 보부상 사례 세 가지 확인(11/30 P1) · 패시브 인컴(유통) 구조 설계 세션 준비 — 3PL 이용 수강생 수·월 출고 건수·건당 단가 / 사입 전환 비율 / 메이븐 스토어 공급처·마진율(11/15 P1) · 11/7 [결정] 디노 합류(물류 책임자)</div></li>
    <li data-n="https://app.notion.com/p/4110cf8fea048130812ed113351546f8"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">셀러 멤버십(11/7 신규 프로젝트) — 파일럿 설계 확정(11/30 P0): 9월 '멤버십+공급형' 기획서 v0.1 기반, 12월 창립 멤버 50명(대기방 10개 · 월 2.9만 · 주간 공급 상품 10개 + 프로그램 + 3PL 옵션 · 노코드) · 위너/슬롯 규칙·반사입 원칙·KPI(3개월 유지율 70%) · [검토] 상품 등록 대행 서비스 — 프로 티어/애드온(월 50개 49,000 안), 10/31 대리등록 항목과 통합(11/30 P1) · 가을 대표님 런칭 기획(11월, 진행 중 · 11/30 P0)</div><div class="m">11/7 노션 메모: 루크가 생산할 것 = '팔 상품 + 올리는 도구 + 보내는 창고' · 강사 네트워크(유입) + 멤버십(락인) + 3PL(반복)이 파는 회사 · 선행: 통판 신고·토스 운영 키 · 기대 결과: 반복층의 첫 상품, 3월 300명 월 2,000만 목표 · 첫 주문률이 멤버십 1순위 리스크 · 【최우선】 결제 시스템 실제 열기(창고 택배비, 11/8부터 매일 알림 · 노션 진행 중)는 툴박스 보류와 별개로 필요한지 확인(11/30 P1) · 11/10 운영 회의: 무제한 외에 월 100개 등록 등 횟수 제한 라이트 버전 → 기본 강의 연결 안 — 구독 모델은 계속 검토, 횟수·가격·강의 연결 방식 미정</div></li>
    <li data-n="https://app.notion.com/p/4120cf8fea048143944fcb5cae7793c7"><span class="tag p0">P0</span><div class="t">임원전용 운영 공유 사이트(11/8 신규 프로젝트) — 배포 마무리(11/15 P0 진행 중): Cloudflare Zero Trust 무료 요금제 활성화(결제수단·약관, 루크 직접) → Access 정책을 '임원 이메일 목록 허용'으로 변경 → 디노님·메이브님 이메일 추가 후 링크 공유 · <b>Access 활성화 전까지 사이트가 공개 상태</b></div><div class="m">11/8 [결정] Vercel 비밀번호 보호(Pro·공용 비밀번호 1개)·GitHub Pages(접근 제어 없음) 대신 Cloudflare Pages + Access · 저장소 Yoo-Mideum/sooda-exec(비공개), 루트 허브 + 문서 1개=폴더 1개, 첫 문서 = 물류 매뉴얼 v1.1 피드백 정리 · 11/8 12:00 Pages 배포 완료·Access 앱 생성 · 일상 할 일은 노션 액션보드, 정리 문서는 사이트</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea0481af98cfd6f61f374099"><span class="tag p1">P1</span><span class="tag cash">현금</span><div class="t">돈벌쥐 PD 공동 프로젝트(10/23 통화) — 10/24(토) 오전 PD님께 연락 예정이었음 — 10/30(금) 민트님·PD님 3자 미팅 진행(플라우드 112분, '스스로월100 미팅') — 다마고치 콘셉트 신규 채널 프로젝트: 11월 시작 · 총 5개 에피소드 · 세일즈 라이브 2027-01-20 · 타깃 40대 초반 · 브랜드 '스스로 월백' · 상금 총 300만(광고비 일부 전환) · 정기 회의 매주 수 13시 Zoom → 노션 새 항목 5건(포맷 확정·12월 착수 여부 11/4 · PD 위임 범위·배분 모델 11/4 · 송출 채널 11/11 · 첫 에피소드 면접 콘셉트 촬영 준비 11/15 — 기한은 추정) · PD 몫 출처·3,000만 구성은 미팅 요약에 없음(노션 2건 미완료 · <b>확인 필요</b>) · 정할 것 넷: PD 몫을 어디서 떼지(배분 전 매출 / 우리 4 / 촬영비 800만 자리 대체) · PD 역할 범위(라이브 지원 포함 여부) · 3,000만에 용역비 900만 포함 여부 · 12월 촬영분을 11월에 당겨 찍는 일정(PD 12월 둘째·셋째 주 금토일 고정, 11/5) · <b>11/2</b> 클로드 페이지 2건(<a href="pd/">장기 파트너십 설계</a> · <a href="pd-long/">비용 산정</a>) → 노션 새 항목 7건(통화 준비 4건+[검토] 4분할, 기한 11/2 — 모두 지남·시작 전 · '스스로 월백' 법인 명의 11/8 · 1만 채널 애드센스 실적 확인 P2) · <b>11/2 17:47 PD님 통화(플라우드 44분)</b>: 신규 강의 프로젝트 — 홍보 영상 촬영 3~4명(인당 30~35만, 약 120만)·본편 2명(60~70만), 편집은 PD 직접, RS는 팀 단위 턴키(전체 매출의 일정 %) — 세부 %·규모는 수요일(11/4) 줌에서 기획안 확정 후 민트님·PD 직접 협의 · PD는 개인 수익 기대보다 촬영 인건비·팀 운영비 확보 우선 · 루크 개인 채널 퍼스널 브랜딩('유믿음' 인물 먼저 → 전문성)은 신규 프로젝트 안정화 → PD '여자들의 수다' 첫 화(13일 촬영) 뒤 본격 논의(대행 체계+하이브리드 보상) · 다음 주 화/수 저녁 대면 식사 미팅 → 노션 새 항목 4건(민트님께 인건비·턴키 RS 공유 11/4 P0 · 영상 링크 전달 11/4 · 식사 미팅 확정 11/6(지남 · 노션 미완료) · 니즈 문서화 11/14 — 기한 추정) · 요약의 '추석 전 런칭'은 1/20 라이브 계획과 달라 <b>확인 필요</b> · 통화는 진행됐으니 11/2 준비 항목은 완료 처리하면 빠짐 · 11/4(수) 13시 줌 정기 회의 당일 — 기한 11/4 항목 6건(민트님께 인건비·턴키 RS 공유 P0 · 다마고치 포맷·12월 착수 P0 · PD 위임 범위·배분 모델 · 영상 링크 전달 · 최은봉 회사소개서) · <b>11/4 정기회의 이후 다마고치 진행은 위 '스스로 월백 리턴즈' 줄</b>(포맷·12월 착수·송출 채널 3건 완료 처리)</div><div class="m">[결정](진행 중) 촬영팀은 돈벌쥐 PD님 쪽으로 — 김○○ PD 회사 대신, 외주비가 아니라 수익 배분으로 프로젝트에 참여 · 민트님께 카톡 상의 후 진행(김○○ PD 회사가 별로라서가 아니라 채널을 길게 가져갈 파트너가 필요하다는 틀) · 1~2월 영상 5~8편 + 카페 3,000명 추가 모집 → 1/20 라이브, 전환 5~10% 가정 150명·강의비 180만(가정값) · 뷰셀님 측 강의 기획사 미팅은 PD 컨택 결과(11/8) 뒤 조율(11/10) · <a href="oct23/">10월 23일 세 대화</a> · 11/7 대정리: 10/23 통화 후속 항목은 정리됨, 'PD 12월 촬영분을 11월에 당겨 찍는 일정'(11/5 지남 · 노션 미완료)만 남음</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea04816ab986e866e792a04a"><span class="tag p1">P1</span><span class="tag cash">현금</span><div class="t">메이븐(메이브님) 정산 — 12월 정산 1,800만 확정 여부를 언제까지 정할지(10/31) · 5기 정산이 1월인지 2월인지(11/30) · 인베이더 없이 메이븐 기수를 돌릴 수 있는지 판단(11/30)</div><div class="m">10/23 [결정] 2건: 메이븐 5기 12/20 강의 · 앞으로 격달 2,000만 정산(연 1.2억, 바닥 수입) / 배분 네 건 확정(가을 6:루크 4 · 민트 건 루크 24%·메이븐 16% · 메이븐 기수 루크 20%) · 11·12월 각 1,800만은 가정값이고 실제 수령은 10월분뿐 — 12월분이 빠지면 11~1월 순현금 2,380만 → 580만 · 1월은 가을님 수입 630만 vs 지출 900만으로 −270만 → 1월에 떨어지는 수입 하나 더(도구공방, 11/30) · 10/23 민트님 협의 녹음: 인베이더 의장이 상품 중심 전환 언급·그만둘 소문 — 메이븐 기수 수익은 인베이더와 5:5라 끊기면 바닥이 사라지고, 반대로 인베이더 없이 돌리면 루크 몫 두 배 · <a href="cash/">11~2월 현금 흐름</a></div></li>
    <li data-n="https://app.notion.com/p/4090cf8fea0481a2982cf9e5b5e7aa70"><span class="tag p0">P0</span><div class="t">루크 툴박스·자동등록 — 자동상품등록 프로그램(자동후불사입용) 전면 개편 12개 항목(P0 진행 중, 기한 없음): 설치 진행률·화면 2버튼·전자책·사전점검·수동입력·재설치 없는 업데이트 + AI 비용 60~70% 절감 · 자동소싱 인수 — 소싱 연동을 붙일 곳 결정(A: 내 v234에 이식 / B: 인계본으로 갈아타기 / C: 소싱만 따로 — A안 권장, P0) · 구글시트를 원작자와 같이 쓸지 따로 쓸지(P1) · 6기 1주차 덱별 영상 8개 유튜브 업로드(스튜디오에서 직접, P0) · <b>10/31</b>: 6기 1주차 편집본 8개 완성(루나 — 3:48:26 · 자막 4,948개 · 4.2GB · 자막 밀림 최대 9초의 원인(자막 트랙 time_base 불일치) 수정) → 루크 확인 후 강의 사이트(인베이더스쿨 1~8교시) 업로드만 남음(P0, 기한 없음) · 자동소싱 v4.94 배포본·설치안내(완료) → v4.95 재설치 없는 업데이트+설치파일+2주 리뷰 수(진행 중, 배포 저장소 공개·2단계 인증 완료) → v4.96 빈 수량 자리 찾기(코드·시험 101/101 완료 — 네이버가 제목 ', 4개'로 새 수량 옵션을 만드는지 루크 확인 전 배포 보류) · 루크 몫: 자동소싱 로그인 한 번 + 묶음 키워드 한 판(P0, 기한 없음) · 3주 집중 코칭 신청 화면 공개(2명 모집·띠 배너·신청 통계 · 코치 실명은 '가을님'으로만 — 10/31 직접 보고 2건 완료, 노션 P 없음) → <b>11/1</b> 코칭 모집 화면 손질 3건(제목 「3주간 매일 1시간씩 1:1 교육 받으실 분 모집!」·블로그 말투 → 주소를 /p/ 임의 주소로 옮기고 무료 이벤트 강조 → 신청하기 → 로그인 → 설문 → 확인창(약속 3가지) 흐름) + 6기 강의 서포트 화면 '같이 듣는 분' 명단(지난 기수 세 분이 6기 화면을 같이 보게, 기수·도구 권한은 그대로) — 클로드 코드 직접 보고 4건, 모두 완료(노션 완료 4건, P·기한 없음) → <b>11/2</b> 직접 보고 10건(모두 완료): 온라인 상담·원격 수업 준비 안내(그림 5장) → 2판(수업 전 설치/당일 분리) · 6기 명단 11명 정리 + 6기 전용 설치 파일(자동등록 신규·자동소싱 v4.98) · 운영진 한 분 관리자 · 설치 파일 사이트 전체 같은 주소 · 마이페이지 바로 가기 다섯 묶음 · 자동소싱 받는 자리 분리 · 가입 전 대표님 한 분 추석 특강 사전 개방 예약 · 소명자료 PDF 4권+수강생 전용 화면 · 코칭 모집 마감 11/3(화) 23:59로 연장(발표 11/4)+신청자 실시간 관리자 화면 · 노션 완료 2건: 자동등록 로그인을 뷰셀 290명·미니쌤 23명 명단까지 · 자동등록 v235(내 가게 기본정보 + 2~4개 한 번에) · 6기 1주차 편집본 8편 유튜브 재생목록 정리·썸네일 8장(노션 시작 전, P·기한 없음) · 11/2 수강생 녹음 4건(1:1 세팅·재설치 상담 29·50·29분 + 밤 1:1 컨설팅 117분): 재설치·API 키·IP 재등록을 되풀이 안내 — 설치·자동등록 표준 가이드(11/1 지남)와 같은 요청 · 신규 수강생 한 분 1:1 세션 11/4(수) 10:00·11/6(금) 14:15 예정 · 7기 부반장(녹음 제목 표기 그대로) 세팅에서 3PL 추천 상품 배정 인원 제한(상품당 2~3명) 후속 안내 필요(AI 제안) → <b>11/3</b> 직접 보고 7건(모두 완료): 추석 특강 1명 열기 · 비밀번호 찾기 메일(Resend, no-reply@giantstoolbox.com) · 발주 전 셋팅 페이지(/order-setup) · 코칭 신청 관리자 머리글 정렬+엑셀 내려받기 · 소명자료 ⑤ 실제 정품 소명서 예시(개인정보 가림) · 6기 「1주차 강의 정리」 페이지 · 사이트 속도 개선(서버 함수 서울 icn1, 첫 응답 1.0→0.15초) · 노션 완료 3건: 자동등록 v236(컴퓨터 3대 막힘 로그인 화면에서 지우기) · 6기 1주차 재생목록 대표 이미지 · 쇼츠 5편 · 11/3 수강생 녹음 4건(1:1 코칭·실습 58·69·31분 + 심○○ 대표님 컨설팅 118분): 되풀이 요청 = 수정판 재설치·소싱 프로그램 설치·역마진 계산 기준·품절 대체·송장 입력·자동 배송 연동 안내·코칭 예약 시간 중복 방지 — 설치·자동등록 표준 가이드(11/1 지남)와 같은 일 · 심○○ 대표님 후속: 11/6 소싱 프로그램·엑셀 데이터 보충 설명 · 11/10 주간 후속 점검(전자제품 조사) — 과제는 수강생 몫이라 노션 새 항목 없음 · 코칭 모집 마감 11/3 23:59 → 11/4 발표 · <b>11/4 직접 보고 14건</b>(상황판): 6기 1주차 보충 자료 8편 + 3주 코칭 신청 마감 화면(신청 47명 → 매출 100만 아래 31명은 다음 기회 안내, 16명은 따로 연락, 뽑힌 2명 전화는 루크) · 「부업을 시작하기 전에 반드시 읽어두세요!」 /before · 마이페이지 원격 수업 준비 링크 · 소명자료 ⑥ 확약서 예시 · 6기 화면 정리(추석특강 숨김) · 프로그램 받기 링크 깃허브 설치 파일로 통일 + 비수강생은 구매 안내 · 원크루 책장 2호 『가격은 어떻게 형성되는가』(11/3 수업 녹음 기반, 익명) · 원크루 자료 3건 게시 · 키티티 상담 사이트 5건 · 6기 수강생 계정 1건 정리 · <b>노션 11/4 등록(일정 추가)</b>: 심○○ 대표님 교재 PDF+11/6 보충(11/6 보충 통화 4건 진행됨 · 노션 진행 중) · 이○○ 대표님 11/6 14:15 세션(노션 진행 중) · 6기 수강생 두 분 후속(11/8) · 디노 원크루 자료실 첫 배포(11/8) · 민○○ 대표님 11/9 본격 등록 · 신정현 대표님 자료실 13장(onecrew-sjh, 11/11) · 유○○ 대표님 교육 일정(11/14) · 신규 수강생 2주차 코칭(11/15) · 소싱 주소값+비밀번호 변경(11/13 — 11/9 주소값 항목과 겹침) · 공유용 페이지 별도 저장소 결정(11/9 P0) → <b>11/5 직접 보고 3건</b>(상황판): 원크루 교육자료 두 건 게시(원본과 차이 0, 완료) · 키티티 상담 사이트 링크 공유 미리보기 교체(완료) · 창고 사서함·재고 관리(/warehouse 수강생 화면 · /admin/warehouse 관리자 — 사서함 번호 HD-1001~ 자동 발급, 입고/출고 기록, 사진 180일 뒤 삭제 · 지금은 관리자만, 루크가 확인하고 「열어」 하면 수강생에게 공개 — 진행 중, 노션 P·기한 없음) · 노션 11/5 자동등록 테스트판 2건(P0 진행 중, 기한 없음): v237 소싱 엑셀 그대로 붙여넣어 올리기 · v239 등록 현황 달력·하루 목표 + 점검 접기 → <b>11/6 직접 보고 17건</b>(상황판, 완료 16·진행 중 1): 거인의 창고 2판·3판(입고/출고 탭·상품 코드 FD/BT/LV…·유통기한·검수 → 엑셀 출고·운송장·코드 체계·관리자 탭 /admin/warehouse) · 카테고리 자동 분류·운송장 원본 서식 · 운송장 추적·관리자 재고 관리 탭 · 출고 취소·반품 관리 탭 · 입고(밤 11:59)·출고(오후 3시) 접수 마감 카운트다운 · 출고 취소 1시 카운트다운(공휴일 목록은 아직 없음) · 수강생 재고 관리 탭+보관 기간 신호등(진행 중) · 마이페이지 묶음 칸(펼치기/닫기) · 52주 추천상품 맨 위 · 접근 조이기(강의·자료·설치 파일은 승인 수강생만) · 6기 2주차(11/6 19:00 진행, 플라우드 313분 녹음 — AI 노트 없음): 카운트다운 팝업·안내 화면 · 쇼핑몰 5곳 구매 화면 가이드(수강생 전용, 사진 265장·PDF 6) · 임시 다시보기·꼬리물기 예시 구글 시트 · 스마트스토어 공지 문구 5개(복사 단추) · 강의 끝난 뒤 안내 칸 숨김 · 노션 완료 2건: 자동등록 v241(동시등록만 잠금)·v242(위탁·사입을 상품코드로) · <b>【최우선】 결제 시스템 실제 열기</b>(노션 11/6 진행 중, P·기한 없음 — 토스페이먼츠 열쇠가 테스트용이라 실제 입금 안 됨, 통신판매업 신고 「준비 중」 → ① 통신판매업 신고번호 ② 토스 심사 → 운영 열쇠 발급 → Vercel 환경변수 교체 ③ 창고 출고 택배비 결제 화면 · 11/8부터 매일 09:00 알림) · 쇼핑몰 5곳 구매 교육자료 완성(사이트별 HTML 5장+목차+PDF 6, 사진 249장·인포그래픽 53개) → 루크 검토·빠진 화면 직접 캡처(11/30 P1) · <b>11/6 심○○ 대표님 보충 통화 4건</b>(플라우드 59·44·10·5분): 소분 포장 확인 · 매입 총액 기준 마진 엑셀 · 2개/4개 묶음 옵션·토너 앵커링 전략 · 식품 카테고리 꼬리물기 소싱 실습(11/2~11/8) → 가전·디지털(11/9~11/15) — 대표님 몫은 노션 새 항목 없음, 루크 몫 2건 노션 새 항목(프로그램 묶음 옵션 자동 생성·검정 화면 깜빡임 11/6 P0 — v241·v242에 포함됐는지 확인 필요 · 추천상품 소싱 시연+엑셀 결과 등록·슬롯 설정 확인 11/10 P1, 기한 추정) · <b>11/6 상담 녹음</b>(72분, 12:23 KST): 신규 상담 수강생 한 분 기초 세팅(월 50만 부업 목표 · 사업자등록 신청·스마트스토어 개설·IP 등록, 상품 등록은 아직 없음 · 기기 조작 밀착 지원 필요) → 루크 몫 2건 노션 새 항목(녹화 강의·설치 링크·상담 요약 카톡 전달 11/7 P0 · 2차 상담(일요일경) 자택 IP·운송장 프로그램·엑셀 주문 처리+통신판매업 신고 안내 11/9 P0 — 기한 추정)</div><div class="m">10/30~10/31 클로드 코드·채팅 → 노션 새 항목 19건(완료 13건) · 인계본 286개 파일 전수 분석 완료: 소싱 4.90(크롬 확장) + 등록 v235/b182, 등록대기목록.csv 한 파일로만 연결 · 내 v234/b177에는 소싱연동·제외브랜드·하루상한 등 함수 29개가 없고 인계본에는 윈도우 OCR·무재설치 업데이트 등 27개가 없음 · 시트를 따로 쓰면 새 시트 2개·앱스스크립트 2개 배포 후 재빌드 + 수강생 전원 재가입 필요 · 상세이미지 글자 읽기는 제미나이 비전(상품당 약 114원) → 윈도우 OCR 하이브리드 · 10/30 직접 보고 7건(강의 서포트 화면·꼬리물기 키워드 도구·추석 특강 열기, 모두 완료) · <a href="status/?p=루크 툴박스">상황판</a> · <b>11/7 [결정] 툴박스 잠정 보류</b> — 거인의 도구공방에서 박○○ 대표님 수익 모델 강화로 전환 · 11/7 완료 '자동등록 v243 — 프로그램 강제 종료' · 창고 택배비 결제 개통 분리 여부 결정(11/30 P1) · 【최우선】 결제 시스템 실제 열기(진행 중, 11/8부터 매일 알림) · 11/10 직접 보고 2건(완료): 꼬리물기 '남는 돈' 카드 할인을 구매가에서 빼도록 셈 수정 · 원크루 사이트 공개 34번 긴 칼럼 '자아실현과 부의 길' 발행(6,874자·그림 10개, 갈래 '나와 돈' 신설) · <b>11/12 직접 보고 2건(완료)</b>: 셀수다 자동 소싱 v5.6 윈도우 설치파일 → 맥 설치판(dmg) 변환(바탕화면 자동 풀기·진행바·자동 업데이트, 실기기 설치 확인 · 애플 공증 없음 → 처음 '그래도 열기' 1회 · 다른 맥 1회 확인 남음) · 툴박스 /setup·자료실·강의 화면에 맥 설치판 받기 링크 추가(깃허브 릴리스 v5.6 업로드, 맥이면 맥판 먼저 — 새 버전은 dmg 재빌드 → 릴리스 → 주소 버전만 교체)</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea048130a802fa2cefc1c2cb"><span class="tag p0">P0</span><div class="t">물류팀 보고 체계 — 매일 18:30 브리핑(15~20분) 고정 + 사실/경험/의견 분리 보고 양식(10/27 · 기한 지남, 노션 미완료 — 도입 여부 기록 없음) → 일일 KPI(처리 건수·시간 준수·보고 적시성) 설정·1주 평가·1:1 면담(10/31) · <b>11/3 물류 회의(플라우드 40분, 17:36 KST)</b>: 물류 현장 실습 3일(11/4~11/6 수·목·금, 08~18시 — 중국 수입→쿠팡 납품 업체, 업체·일정 확정 여부는 요약에 불분명 · 노션 '블럭마트 출근 전 기업 실사 마무리'(11/10 P0)는 목표 '사업 외 개인'으로 등록돼 일정에서 제외 · 녹음·촬영은 업체 동의 범위 확인) · 물류가 자리 잡으면 외부 3PL 고객·풀필먼트·오프라인 판매로 확장, 물류 수익은 담당자 성과 배분('최소 6' vs 강의 6:4 사례 — 미정) · 2027년 초 본사 서울 이전 시 강의 공간·창고 분리, 안정되면 창고 추가 임대(2027 하반기) · 회사 신고 시 물류 담당 파트너 이사 등재(요약은 '메이브님'으로 표기 — 화자 <b>확인 필요</b>) → 노션 새 항목 2건(수익 배분·3PL 이용료 구체화 11/30 P1 · 이사 등재 협의 2027-01-31 P2 — 기한 추정)</div><div class="m">10/24 새벽 물류 업무 회의(플라우드 25분, 루크·리나님·뿌요) 조치 사항 → 노션 새 항목 2건: 송장 잔류 금지(미처리 0건 확인 후 퇴근) · 합배송 출고 오류 사전 신고 · 오배송·반품·재고 부족 즉시 공유와 고객 보상 표준화 · 근무표·알람(CS 시간) 의무화 · 처리량은 하루 300건 기준 탄력 조정 · 재고 신속 처리 · <b>11/8 물류 채팅</b> → 노션 [결정] 3건(바코드 기반 통합 재고 운영 · 오후 1시 이후 출고 취소 불가 — 수강생 공지 완료, 시스템 차단은 아직 · 입고 동선 2중 카트·사서함 단위 포장) + 새 항목 4건: 리나님 역할 재정의(스토어 전체 책임자 → 출고 책임자 · 시간당 40건 · 300건 초과분 알바, 11/15 P0 — 급여 조건은 공개 페이지에 싣지 않음) · 매뉴얼 v1.2 반영(메이브님 담당, 11/30) · 통합재고 수강생 약정서 초안(11/30) · 물류 시스템 과제 4건(출고 취소 차단 > 셀프 조회·챗봇 > 미출고 판정 > 바코드, 11/30) · 목표: 하루 300건 출고 체계, 디노님 = 운영책임+입고(일 30만·월 660만은 노션 기대값) · <b>11/10 운영 회의</b>(플라우드 70분, 16:14 KST, 4명): 전날 300건 넘는 출고 중 약 100건만 처리·당일도 지연 → 디노님이 물류 파트 전담 관리로 정리(인계·바코드 분류 체계 적용 → 노션 새 항목 11/15 P0) · 11/9 갤럭시 탭 2대 오배송(스토어 주문 환불, 반송 요청 → 11/12 P0) · 입고 리스트 기준(수강생이 카탈로그명·운송장 직접 입력) 도입 → 11/30 P1 · 강의 종료 후 재고조사·상품별 재고 정리 → 11/30 P1 · 물류 담당자 조건 회신 11/15(리나님 역할 재정의 항목과 같은 건, '보라님' 역할·협업 방식은 이번 주 안 결정 — 같은 사람인지 <b>확인 필요</b>) · 금융상품 수익 모델은 진행 안 하기로(11/7 [결정]과 같음) · <b>11/10 물류 현안 진단</b>(플라우드 74분, 17:36 KST, 루크·물류 담당자): 선제 보고 체계(착수 시 소요 시간·필요 지원 수치화, 퇴근 전 미결 현황 공유) 합의 · 건당 1,000원 구조에서 일 100건은 적자, 출고 전담이면 일 280~300건·월 약 600만 규모(회의 발언, 확인 필요) · 다음 주 전체 회의(11/17 화 P0 — 처음 11/20 추정, 11/11 녹음으로 확정)·물류 센터 견학 기획(11/30 P1) → 노션 새 항목 · 급여 체계 논의는 싣지 않음 · <b>11/11 물류 녹음</b>(플라우드 77분, 10:54 KST — 루크가 물류 총괄을 맡을 분(요약의 '대표님', 디노님으로 추정 · 같은 사람인지 <b>확인 필요</b>)과 역할 논의): 창고 배치·전산·운영 자료를 신규 인력이 처음 봐도 3일 안에 적응할 수준으로 단순화(기능 추가보다 감추기·통합 · 인력은 1년 안팎 교체 가능성 전제) → 노션 새 항목 11/30 P1 · 총괄 후보가 일주일간 입고·출고·반품·전산·CS를 직접 측정(4시간 100건=시간당 25건 vs 메이브님 기대 3시간 100건 — 검증 전 수치) → 11/17(화) 리나님·메이브님과 역할·업무 범위 조율 자리의 근거 → 노션 새 항목 11/17 P0 · 리나님 역할 범위는 11/17 자리에서 본인이 설명 · 메이브님은 외부 고객 유치·강의 집중, 총괄이 현장·데이터 정리안 · 급여·감정 관리 조언은 싣지 않음</div></li>
    <li data-g="developer-accounts"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 (Apple · Google Play · Microsoft)</div><div class="m">툴박스·영상공장·블로그타이퍼를 폰·맥·윈도우로 배포하는 모든 일의 앞단. Apple은 승인에 며칠 걸림 · 기한 10/2 지남(노션 미완료)</div></li>
    <li data-n="https://app.notion.com/p/3fc0cf8fea0481acaa81f970cc74f260"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">식스 엔진 지난 주 결과 확인(10/19~10/25 · 1주 목표·객단가 확정·500명 자산 확인·주간 고정 일정 모두 노션 미완료, 달성 여부 기록 없음 — <b>확인 필요</b> · 지난 주(11/2~11/8) 결과 기록·이번 주(11/9~11/15) 목표 모두 노션에 없음 — 지난 주 결과 확인) — 박종혁 본부장(사내 활동명 '민트', 10/21 노션 [결정]) 10/21(수) 근무 시작 → 닫을 것 다섯 중 6:4 분모는 B안(비용 차감 후)으로 확정(10/21 [결정]), 광고 첫 집행일 · 과거 CAC · 객단가 · 3개월 총액은 민트님 입력 폼(/park-terms/) 회신 대기 · 1월 자사 강의 객단가 확정(180만은 가정값 · 10/24) · 500명 자산 확인 4가지(메이브님 측 분배·회원 정의·고가 실단가·실제 재구매율 · 10/24) · 합류 전까지 카페 글·환영 동선·공지 쌓기</div><div class="m">10/17 노션 [결정] 2건: 수익 프로젝트 6개를 '식스 엔진' 체계로(엔진1 매일 고정, 5개 월~토 순환) · 거인의 도구공방을 교육+프로그램 판매 기본 사이트로(일십백천·원크루는 심화) · 10/17 설계 메모의 지연 비용(합류 1주 지연마다 루크 몫 약 1,555만 감소)·연 1.72억·CAC 3,000원·전환 10%는 모두 클로드 가정값 — 실측 전 · 같은 메모의 '10/20 라이브 → 10/25 6기 런칭'은 이 페이지의 10/25(일) 무료 라이브와 날짜가 달라 <b>확인 필요</b> · 10/18 주간 고정 일정(노션): 월 새벽·화 오후 물류, 화 19:30 메이브님 4기 라이브 참관(동시접속 최고·신청 전환·완주율 세 숫자만), 수 13~16시 합류 미팅, 금 사업자등록 정정 기한, 일 주간 리뷰·6기 런칭 — 엔진 09~12시 블록은 비우지 않음 · 루크가 고치는 '6기 무료 라이브 PPT'는 10/20용이 아니라 어느 날 라이브용인지 <b>확인 필요</b> · <a href="engine/">식스 엔진</a> · <a href="map/">지금 어디 있는가</a> · <b>11/7 대정리</b>: 1주 목표·500명 자산 확인·주간 고정 일정 항목은 노션에서 정리됨 — '1월 자사 강의 객단가 확정'(10/24 지남 · P0 미완료)만 남음 · <b>11/9 노션 완료 처리 2건</b>: '식스 엔진 1달 목표(~11/17)'(카페 1,000명·도구공방 첫 결제·전자책 1종·가을 촬영 — 달성 여부는 노션에 기록 없음, 확인 필요) · '[결정 필요] 연애상담 코스·앱 제작 정지 여부'(결정 내용 기록 없음) — 둘 다 일정·우선순위에서 뺌</div></li>
    <li data-n="https://app.notion.com/p/3fd0cf8fea0481858d7ce31805c939c2"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">키티티 토탈샵 오픈 준비 — 10/25 기한 3건 지남(노션 미완료): 헤어 기기·약제 공급처 결정(로레알 1순위 · 소개 미팅에서 7가지 답 확보 · 기존 기기 4대 철거) · 권리금 계약 인도 조건 부속 합의(중개사 문자 1~3안 → 인수·철거 목록 → 부속 합의서) · 인스타 공식 계정 구조 1장 · 10/24 아침 메모 → 새 항목 2건(10/31, 추정): 주간 촬영 출장 메이크업 계약(엑셀 방송 대표) 조건 문서화 · 헤어팀 보상안·2인 배치 손익 시뮬레이션 · 10/26 새 항목: 고대생 첫방문 20% 할인 배너(40×10cm) — 캔바 편집본은 10/27 완료 등록 2건(글자·이미지 레이어 분리 + 원본 소재로 해상도 복구, 2000×496 · 인스타 QR은 새로 받은 파일이 맞음 — 루크 확인) → 11/1 P0 '진행 중' 항목(캔바 편집본 만들기)은 같은 일이라 완료 처리하면 빠짐(11/1 지남 · 노션 미완료) · AI 생성 인물·배경 + 캔바 텍스트·QR → 인쇄 입고(10/31 진행 중, 10/26 스타일 합격 · 남은 것: 인쇄용 CMYK PDF·입고) · 10/29 새 항목 2건(P0): 지영 원장 영업신고증·면허 종류 확인 + 성북구청 위생과 문의(11/5 지남 · 노션 미완료 · 인테리어 도면 확정 전 선행 조건) · 상표 출원 — 특허고객번호 신청 + 사용 증거 수집(11/1 지남 · 노션 시작 전) · 대행 견적·지정상품 초안(11/1 지남 · 노션 P0 진행 중) · 10/29 [보고] 토탈샵 전환 영업신고·사업자등록 변경 정리(<a href="totalshop-license/">페이지</a> · 핵심 병목은 원장 본인 면허 — 피부·네일 면허 없으면 3층은 샵인샵 별도 신고) · <b>11/3</b> 키티티 홈페이지 리틀리형 전면 개편(인트로 유지·링크 한 장) + 리틀리식 관리자 편집기(/admin — 블록·프로필·디자인·기록, 옛 사이트는 archive/v5) 완료 → 링크 홈 내용 채우기(프로필 사진·버튼·사진)는 원장 몫(노션 P1, 기한 없음) · <b>11/4</b> 상담 사이트 보고 5건 완료(스킨 10개+키티티 시그니처 · 리틀리식 관리자(이전 공지·예약 메뉴, 2월 오픈 버튼) · 배경 로고(파일 미전달 막힘 → 수령 후 적용) · 원장 수정 요청 6건 · 관리자 코드 임시 변경) → 원장 몫 2건(노션, 기한 없음): 스킨·커버 사진 확정 · 2월 오픈 때 커트·펌/네일/에스테틱 예약 주소 넣기</div><div class="m">10/18 회의 녹음 4건 → 노션 [결정] 3건: 오픈 준비 순서(공간 구조 → 인원 → 원가 → 가격표 → 공고 → 브랜딩 → 1월 시공) · 인력 구조 권장안(직원 4 + 실장 2 정률, 네일·에스테틱은 3월 합류) · 프리오픈 1/26~31·정식 오픈 2/2(조건: 인테리어 계약 12/15 전, 1/5 착공, 급배수·전기 설계 11월 내) · 11월 할 일 9건(네일 세트 비교표 10/31 · 브랜딩 초안·인테리어 상담·에스테틱 기기 조사·페르소나 콘텐츠 11/15 · 주말 발품 11/22 · 손익·투자·급여 11/30 — 인테리어·기기·콘텐츠 3건은 플라우드 Action Item, 기한은 추정) · 로레알 월 약제 매입 조건(100만~300만)이 기기 지원과 묶이는지 <b>확인 필요</b> · 임대차·권리금 금액은 공개 페이지에 싣지 않음 · <a href="hair-vendor/">헤어 공급처 비교</a> · <b>11/19 화장품 제품 업체·헤어 기기 미팅</b>(플라우드 11/7 일정 조율 녹음 → 노션 새 항목 P1 — 업체명·안건은 녹음에 없음, 로레알 공급처 건과 같은 건인지 확인 필요) · <b>11/12 세무사 상담</b>(플라우드 134분, 14:16 KST — 지영 원장 토탈샵 건, 루크 동석): 네이버 플레이스 노출을 위해 헤어·메이크업·네일·에스테틱을 서비스별 사업자로 나누는 방향(관리 비용·기장료 증가는 감수) — 같은 주소라도 공간 구획 + 사업자별 임대차(또는 전대차) 계약·영업허가 필요, 실제 허용 구획·서류는 임대인·관할 기관 확인 · 기존 등록 업종 코드가 피부미용·왁싱 쪽으로 보인다는 지적 → 서류 재점검 · 분리 시 기존 사업자 지원 혜택 유지 못 할 가능성 · 간이과세 포기·일반과세 전환으로 인테리어 매입세액 환급 검토(전환 여부·시점 미확정 · 공사비 금액은 미확정) · 프리랜서 명칭이라도 정기 출퇴근·지휘 통제면 근로자성(퇴직금) · 사업자별 카드 단말기 분리 원칙 · 토탈 회원권 매출의 사업자 귀속·인센티브 계산은 미결 · 네이버페이 예약금 결제 도입함, 매출관리 프로그램은 미정 · 세무대리인이 단체 대화방 개설 예정 → <b>노션 새 항목 3건(11/30 P1, 기한 추정)</b>: 사업자 분리 서류 준비 · 인테리어 세금계산서·과세유형 · 근로/프리랜서 계약서 + 지출 구분 기록 · 정부 지원 여부는 기존 [결정 필요] 키티티 정부지원 건과 같이 확인</div></li>
    <li data-g="platform-director-meeting"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">박종혁 본부장 협업 — 10/9 회의 진행(녹음) → 10월에 정할 세 칸(차감 산정 방식 · 3PL·리셀·프로그램 매출은 6:4 밖 · 총액 인식 일치 — 10/10 다섯 칸에서 축소) 기한 10/16 지남 · 노션 미완료 · 그 전에 물어볼 한 가지: 카페 월 4,000명 만들 당시 광고비(기한 10/14 지남 · 노션 미완료)</div><div class="m">플라우드 10/9 녹음 요약: 초기 3개월 월 300만 고정(용역 형태) 요청 · 수익 6:4(본부장:루크) · 3개월 안에 네이버 카페 신규 회원 3,000명이 지속 여부 기준 · 10/21(수) 근무 시작(노션 [결정] 2건: 사내 활동명 '민트' · 강의 런칭 프로젝트 담당 · 1차 계약기간 2027-01-20까지 / 수익 배분 민트 6:루크 4, 배분 기준액 = 매출 − PG·광고비·외주비 차감 후 B안) · 1차 계약서 17개 조 + 별지 완성(<a href="park-contract/">계약서</a>) — 남은 빈칸은 민트님 인적 사항 넷(기한 10/23 지남 · 노션 미완료) → 변호사 근로자성 검토 → 서명 · 10/23 민트 회의 2건(플라우드 22분·21분): 라이브 마지노선 2027-01-20 확정 · 영상 편당 100만×7~8편 → 계약서 제8·9조 수정(외주 한도 700~800만 · 10/30) · 3,000만은 광고비가 아니라 총 예산(용역 900+광고 900+촬영 800 — 용역비 포함이면 제5조 3항과 충돌, <b>확인 필요</b>) · 10/30 미팅은 진행됐으나(플라우드 112분 — 다마고치 프로젝트 기획 중심) 객단가(180만은 가정값, 메이븐 4기는 285만)·계약서 제8·9조·3,000만 구성 결정은 요약에 없음(10/30 기한 4건 지남 · 노션 미완료, <b>확인 필요</b>) · 촬영팀은 돈벌쥐 PD님 쪽으로([결정] 진행 중) — 10/30 미팅에 PD님 참석 · 민트 건 주간 정기 회의는 매주 수요일 13시 Zoom으로(10/30 미팅), 첫 회 10/28 기획안 검토는 진행 기록 없음(노션 미완료) · <a href="oct23/">10월 23일 세 대화</a> · <a href="cash/">11~2월 현금 흐름</a> · 10/21 미팅 당일 할 일(노션 미완료): 과거 CAC 확정(3,000원 vs 6,000원) · 계정 법인 명의 개설 · 요약본·입력 폼 발송(<a href="park-terms/">발송용</a>) · 10/19 신정현 대표님 회의(플라우드): 수요일 출근에 맞춰 책상 정리·일정 조율·회식(노션 새 항목) · 3개월 총액은 양쪽 숫자가 달라 <b>확인 필요</b>(노션 메모: "천만에 전부 포함" vs "천만 + 광고 900만" — 10/21 계약서 초안의 일곱 칸 중 하나) · 6:4의 분모는 B안(비용 차감 후)으로 확정, 민트님이 A안으로 이해했을 수 있어 서명 전 별지 예시를 같이 읽을 것 · 노션 '10/8 종혁 본부장 미팅'·'3자 미팅 제안서 검토'는 미완료 — 끝났으면 완료 처리, 3자 1:1:1 안과의 관계는 정리 필요 · 시행 전 선행 조건 4가지·계약서 소유 조항(기한 10/13) · 플라우드 Action Item으로 노션 새 항목 3건(좌석·온보딩 10/19 · 유튜브 전략 10/31 · 소싱 자동화·위탁 물류 11/30, 기한은 추정) · <a href="park/">협업 평가</a> · <a href="platform/">전략 페이지</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048138b075f9bb51f5e97e"><span class="tag p0">P0</span><span class="tag cash">선행 조건</span><div class="t">변경등기 제출은 10/16 완료(노션) → 남은 것: 사업자등록 정정신고 — 노션 기한 10/16 → 10/23(금)으로 바뀜 — 10/23 지남 · 노션 미완료(10/7 취하 건 재신청 · 등기사항전부증명서 첨부) · 4대보험 사업장 소재지 변경신고(10/15 지남 · 노션 미완료) · 사업연도 확인·등록면허세·법인인감카드 사용정지(10/12 · 노션 미완료) · 법무사 10/12 상담 후속(사업자등록증 사본 문자·재방문 · 10/16 · 노션 미완료)</div><div class="m">등기 완료(등기사항전부증명서 발급) 여부는 노션에 기록 없음 — <b>확인 필요</b> · 주식 수 100만 주 권고(법무사 10/12) vs 기존 [결정] 수권주식 100,000주도 어느 쪽으로 접수됐는지 확인 필요 · 정관을 전부개정으로 가므로 '정관 찾기'(10/10)·'정관 원본 본점 조항 확인'(10/9) 항목은 완료 처리 확인 필요 · <a href="registry-forms/">등기 서류</a> · <a href="relocation/">등기 페이지</a> · <b>11/12(목) 14:00 세무사 미팅 진행됨</b>(플라우드 134분 녹음 — 요약은 키티티 토탈샵 사업자 분리·과세유형·노무 중심, 수취 주체 법인 전환·법인 매출 잡는 순서 안건이 다뤄졌는지는 요약에 없음 — <b>확인 필요</b> · 노션 '세무사 미팅' 항목(11/12 P0)은 아직 시작 전 — 끝났으면 완료 처리 대상)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048126a2fec9d1efd1c0eb"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">초월스토리 강사 협업 — 계약서 정산 기준 정리·가을 대표님 성과 숫자·일정 확인(기한 10/11 지남 · 노션 미완료) · 강사 파트너 제안서 전달·의사 확인(10/12) · 10/22까지: 2,200만 산출 근거·광고 예산 확인, 6:4 합의 서면화 (기한 10/22 지남 · 노션 미완료 — [결정 필요] 4건 포함) · 10/23 새 항목: 가을님 정산액 6:4 어느 쪽이 6인지(10/31 · 같은 날 [결정]에서 가을 6:루크 4로 확정, 항목은 미완료) · 손익분기 18명 사전 고지(11/5 지남 · 노션 미완료) · 11월 첫째 주 촬영 일정 확정·공동 기획(11/1) · 협업 모델 옵션(플레이어 vs 공동 빌드업)·배분 초안 확정(10/29 지남 · 노션 미완료) · 3주 런칭 준비(10/28 지남 · 노션 미완료 — 10/28 7기 세션에서 11월부터 강의 준비 착수로 정리) · 10/28 7기 세션(플라우드 32분+12분) Action Item → 노션 새 항목 6건: 코칭 알바 운영안(10/30 지남 · 노션 미완료) · 설치·자동등록 표준 가이드(11/1 지남 · 노션 미완료) · 촬영 장소·채널 분산(11/5) · 프로필 촬영·로드맵 1억(11/10) · 수강생 출연 협의(11/28) · <b>10/31(토) 초월스토리 회의(플라우드 76분, 15:55 KST)</b>: 가을 대표님은 뷰셀님처럼 화장품 콘셉트로 런칭 · 4주 커리큘럼 기본(6주 변형 검토) · 기본반(289만 기준)+심화 프리미엄반(컨설팅·오피스 초빙·대리등록) 이원화 검토 · 정산은 순수익 5:5 + 시스템 전체 이용 시 PG 제외 8%, 단순 강사 소개 4% · 촬영은 11월 둘째 주(프로필·모객 영상, 1회 방문 다회차) · 기수별 유튜브 출연 수강생 2명(40대 이상 여성)·라이브 출연 2명을 설문으로 선발(11/4) · 프로그램 3종(소싱·자동등록·가격관리) 수강생 무상 제공, 자동등록 AI 비용(건당 150~300원)만 실비 → 노션 새 항목 19건(P0 3건: 파트너십 계약서 초안·상호 교환 11/1(지남 · 노션 시작 전, 교환 결과 기록 없음 — <b>확인 필요</b>) · 강의 PPT 초안 → 세일즈 파트 보강 11/7 · 인베이더 최종 종료 미팅·합의서 11/7 — 11/1·11/7은 요약 기재값, 나머지 기한은 추정) · 기존 '11월 첫째 주 촬영 일정 확정'(11/1 지남 · 노션 미완료)은 회의에서 11월 둘째 주로 — 노션 기한 변경 필요 · <b>11/3 가을 대표님 계약서 검토</b>(클로드 페이지 <a href="gaeul-contract/">가을 대표님 계약서 — 괜찮은가</a>: 셀피티클래스 × 정복녀 강사용역계약서를 10/31 녹취 전문과 대조 — 합의에 없던 두 줄(인터뷰 채널 출연 RS 20% · 11.76% 결제 수수료 고정)이 65명 기준 5,022만, 루크 몫 603만 손해 · 계약서 초안은 수령된 것으로 보이나 노션 '계약서 초안·상호 교환'(11/1) 항목은 여전히 시작 전) → 노션 새 항목 10건: P0 6건(11/7 — 출연 RS 20% 변경 금지 조항 · 8% 조항 확인 · RS 20% 누구 몫 · 6:4 법적 형태 · 3층 코칭 용역계약 전환 · RS 20%가 합의에 없던 점 업체 확인) · P1 2건(수수료 요율표 요청 11/10 · 기수 광고·운영비 상한 요구 11/30) · [보류] 2건(최소 보장 강사료 · 8% 재원 회사 50%) · [결정] 3건(제한 조항 수정 없이 수용 · 8%는 광고비 내역으로 계상 · 광고 문구 보증 범위 제외 요청 안 함)</div><div class="m">파일럿 강사는 가을(정복녀) 대표님으로 확정(10/7 · 노션 '파일럿 강사 선정' 완료) · 10/8 노션 새 항목 6건: 가을 대표님 몫 2,200만 산출 근거 확인 · 광고 예산 약 4,500만(역산값 — 초월스토리 확인 전) 확인 + 상한·중단 기준 · 가을 대표님께 손익분기 인원·광고비 리스크 사전 설명 · 6:4 합의 서면화 · [결정 필요] 6:4를 숨길지 공동 기획으로 공개할지(이상 10/22) · PG 수수료 요율·실제 광고비 비율 확보(10/31) · 10/7 원크루 세션 녹음 요약: 11월 초 촬영·11월 말 런칭 언급 — 10/6 회의의 '12월 초 라이브'와 달라 <b>확인 필요</b> · 수락 시 3주 런칭 준비(10/28) · 10/6 회의 구두 합의(노션 [결정]): 루크 수수료 = PG 제외 전체 매출의 8%, 순수익은 초월스토리:강사 5:5, 289만 단일 상품 유력 · [결정 필요] 참여 범위·정산 기준 문서화·원크루 관계 유지(10/22) · 10/23 [결정] 배분: 루크 = 전체 매출 8% + 가을님 정산액에서 가을 6:루크 4(1억 기준 루크 1,634만), 8%의 기준은 10/31 회의에서 'PG사 수수료 제외 후 8%'로 언급(계약서 초안에 반영 확인) · 광고 4,500만 선회수 구조라 18명 아래면 가을님 몫 0원인데 루크 8%는 그 구간에도 나옴 — 촬영 전 직접 설명 · 10/28 세션 요지: 강의 시작 전 한 달 수강생 코칭 알바(1인 30~40분 1만원) → 라포 형성 수강생 4~5명 중 1~2명 출연 · 채널은 인베이더 채널과 분산 · 프로필 촬영은 협력사, 비용은 론칭 후 정산 · 매출 목표 1억(목표값) · 가을님 메인 스토어는 이용 정지 예정 통보를 받아 소명 회신·서브 스토어 상품 이전 진행 중(10/28) · <b>11/8 [결정]</b> 강사님 강의는 3PL이 아니라 '화장품 도매 창고'로 표현 · '가을' 호칭 폐기(내부 호칭이었음 — 새 닉네임 후보 도매언니/창고언니, 11/15 확정) · 타겟 30~40대 여성(경단녀) · 새 P0 7건(11/15): 소량 리셀 직접 시작(11월 3주, 12월 라이브용 본인 기록) · 코칭생 2~3명 동의서 · 12월 컨셉 확정('화장품 도매 창고 + 올려드림') · 도매 창고 4개 룰 → 정원 산출 · 11~12월 수익 모델별 분리 기록(런칭 전 월 500만은 목표값) · 강의 회사 채널 시청자층 확인 · P1 4건(11/30): 유튜브 촬영 플랜 · 라이브 PPT 7구간 · 메이브님과 내부 영역 분리 합의 · 등록 대행 티어·요금 — 본인 기록 없으면 가을님 런칭은 1월로 이월 판단(노션 메모) · 이 페이지의 '가을' 표기는 노션 프로젝트명 기준 · 11/10 운영 회의: 이번 달 촬영 시작·12월 런칭 목표 재확인 · 신규 강사를 한 플랫폼에만 두지 않고 복수 플랫폼 운영 검토(촬영 PD 통해 '타이탄' 측 연결 확인 · 초월스토리·셀피티 전략 논의는 긍정 평가, 다른 쪽 역량·예산은 미확신) → 노션 새 항목 11/30 P1 · <b>11/11 루크 메모</b>(플라우드 26초): 강의 업체 쪽 요청 — 프로필 사진 구글드라이브 업로드 · 유튜브 촬영·수강생 촬영 일정(상대가 정하면 우리가 맞추기로 회신) · 상세페이지 자료(수강생 매출 인증·과거 사진) 정리 전달 → 노션 새 항목 11/15 P0 추정 · <a href="chowol/">초월스토리 페이지</a> · <a href="pilot/">파일럿 강사 결정</a></div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481b2b5f9c0ab5aa17594"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">인베이더 종료 대비 — 종료 사실(범위·시점·출처) 확인 · 메이브님과 마지막 기수 공동 대응 합의 (기한 10/8 지남 · 노션 미완료) · <b>10/31 초월스토리 회의</b>: 기존 인베이더 협업은 최종 미팅으로 정리하기로 → 최종 종료 미팅 준비·합의서 작성(11/7, 노션 새 항목 P0) · <b>11/5(목) 박○○ 대표님 미팅</b>(플라우드 123분, 11:17 KST — 신규 교육 플랫폼 운영자, 화자 2 = 루크): 인베이더 12월 이후 운영 불확실 → 별도 플랫폼 준비 중(사이트 구축·심사 약 3주, 1월 진행 안은 조율 중 — 확정 아님) · 미활용 수강생 단톡방 150개+ → 무료 챌린지·기초 강의(30~50명)로 묶어 멤버십·DB 연결 모델(상대측 전달 사례의 수익 숫자는 <b>확인 필요</b>) · 광고비는 집행 총액 공개 또는 실비+10~15% 방식 언급 · 강사 육성 — 내년부터 직강 줄이고 수강생 중 강사 발굴·지원 · 신규 기수 냉장·냉동 상품 스티로폼 추가 비용 1,000원 규칙 계획 → 같은 날 노션 [결정] <b>루크·메이브님 현 강의업체 강의 해지(메이브님은 11월 강의 마지막)</b> + 새 항목 4건(프로젝트 '강의업체 이전'): 메이브님과 통화 — 새 수익 모델 설명·상의(11/8 P0) · 돈벌쥐 PD 연결 에이전시 미팅 — 박○○ 대표님 안과 조건 비교(11/30 P1) · 1월 신규 강의 런칭 준비(메이브님, 12/31 P2) · 토요일 상담 통화 — 메이브님이 공유한 상담 희망자, 개선 의지 확인 후 진행 여부(11/7 P0) + 플라우드 루크 Action Item 2건 노션 새 항목(기한 추정): 플랫폼 논의 내용 메시지로 정리해 전달(11/7) · 2주차 강의 뒤 소싱·사입 운영 프로그램 내용 정리 전달(11/15) · 녹음 후반 개인 대화는 어디에도 적지 않음</div><div class="m">계약서의 수강생 명단·콘텐츠·후기 소유 조항 확인(10/11) · 마지막 기수 명단을 자체 채널로 옮기는 동선(10/12) · 사입 재고 처리 가이드라인(10/13) · 10/23 민트님·테디 협의 녹음(플라우드 21분): 인베이더 의장이 수익성 이유로 상품 중심 전환을 언급했고 그만둘 것이라는 소문도 확인 — 루크 "이번 과정 뒤에는 안 하게 될 것 같다" · PPT는 이번에도 네 차례 변경 · 메이븐 기수 수익은 인베이더와 5:5라 끊기면 격달 2,000만(연 1.2억) 바닥에 영향 → 인베이더 없이 돌릴 수 있는지 판단(11/30, 노션 새 항목) · 다른 기획사(PD 소개 매니지먼트)와도 가볍게 만나보기로 · <a href="invader/">인베이더 종료 대비</a> · <b>11/7 [결정] 인베이더 파트너십 종료 확정</b> — 해지계약서 다음 주 수령, 루크 6기(8명)·메이븐 4기(11월)가 마지막, 12월 강의 없음, 대기방 DB(루크 6·메이븐 4)는 우리 귀속 · 새 P0: 6기 8명 수익 계산(11/15) · 해지계약서 검토 후 서명(11/15 — DB 귀속 '우리'에 박○○ 대표님 쪽이 포함되는지 분명히) · 강의업체 이전: 11/7 [결정] 신규 플랫폼(박○○ 대표님)에 메이븐(뷰셀) 1월 런칭 + 적금 모델 → 같은 날 [결정] 금융상품(적금 모델) 건은 내년 메인 수익 축에서 제외(인베이더 종료 뒤 상품명·환급률표 받고 재검토) · 보험·적금 모델 구조 확인(11/30 P0) · 금융상품 제휴 전 수수료 합법 여부 확인(11/30 P1) · 11/10 운영 회의: 금융상품 수익 모델은 원금 손실·민원·평판 리스크로 진행하지 않는 쪽으로 의견 모음(대체 모델 미정) · 계약 해지·해지서 마무리 뒤 상대와 본격 논의</div></li>
    <li data-n="https://app.notion.com/p/3f30cf8fea048125b5f0cb4b24793347"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">키티티 토탈샵 — 10/8(목) 임대차·권리양수도 계약 체결(노션 완료) → 인테리어 승인 별첨 문서 준비 · 특약 수정안 협상 마무리 확인 (기한 10/11 지남 · 노션 미완료)</div><div class="m">플라우드 10/8 녹음 3건 요약: 2·3층 임대차 계약 서명·날인, 권리양수도 계약 함께 진행, 잔금일 12/31, 렌트프리 1개월, 1월 말 가오픈 계획 · 노션 '키티티 계약'은 완료 처리됨 · '특약 수정안 협상'은 '진행 중', '인테리어 승인 별첨 문서'는 '시작 전' — 끝났으면 완료 처리 필요 · 금액은 녹음 요약끼리 맞지 않는 숫자가 있어 싣지 않음(<b>확인 필요</b>) · 3층 창문 처리 방안은 인테리어 업체와 정해 임대인에게 전달(임차인 측 할 일)</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea048146ba38e897aff07cb4"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">원크루 두 대표님 — 최은봉 7회차 자료 발행(10/18, 맥에서 배포) · 네이버 정품 소명 기한 10/21 전 신규 스토어 상품 DB 이관 지원(복제 API 오류 시 대응) · 정복녀 대표님 추가 강의 링크 전달(10/20) → 10/23(금) 7기 세션 진행(플라우드 45분: 한 카테고리 두 달 집중·주 100개 등록·리뷰 이벤트 유지·실마진 산출) → 11월 첫째 주 촬영 일정·콘셉트·스크립트 공동 기획(11/1 지남 · 노션 미완료 — 10/31 초월스토리 회의에서 촬영은 11월 둘째 주로, 노션 기한 변경 필요) · 10/24 클로드 코드: 정복녀 7회차(10/23 통화) 교육자료 발행·푸시 완료(노션 완료) · 최은봉 8회차(일본 직판) 자료 작성·push 완료 → 맥 배포만 남음(기한 10/26 지남, 노션 진행 중 — 배포했으면 완료 처리) · 10/26(월)부터 매주 월요일 정기 무료 특강 라이브 + 과제 첨삭 운영 시작(10/19 회의 Action Item, 기한은 추정 · 첫 회 진행 기록 없음, 노션 미완료) · 박태경 대표님 성과 평가·외부 도움 전환 결정(10/27 지남 · 노션 미완료, 결과 기록 없음) → 공동 상품 찾기 2시간 세션(10/28 지남 · 플라우드 녹음 없음, 노션 미완료 — 진행 여부 <b>확인 필요</b>) · 10/28 최은봉 세션(플라우드 24분): 정품 소명 건은 플랫폼 회수·환불로 종결 · 개인정보 위수탁 소명 연장(10/30) 요청 회신 대기(10/31 기준 결과 기록 없음) · 천안 비상주 사무실 신규 사업자등록 발급 · 일본 야구 유니폼 직판은 토요일 재무·원가 강의 뒤 지속 여부 결정(노션 메모의 11/1은 일요일 — 10/31 플라우드에 해당 강의 녹음 없음, <b>확인 필요</b>) → 루크 몫: 9회차 교육자료 발행(10/29 지남 · 노션 시작 전) · 회사소개서 개선안(11/4, 추정) · <b>11/4 세션 3건(플라우드)</b>: 정복녀 대표님 7기(58분, 17:59 KST) — 오전 9~11:30 소싱 시간 고정·하루 10건 등록·발주/CS는 오후(대표님 과제) · 가을 대표님 3주 코칭(신청 47명 → 최종 후보 5명 중 2명): 루크가 후보 3명 연락처·참여 각오 전달(11/4 약속 → 11/5) → 코칭 진행 가이드(평일 5일·하루 2시간·3주, 어려운 CS는 확인 후 응답) 정리 전달(11/9, 추정) · 스토어 소명자료 검토(11/7, 추정) · 프로필 사진은 전문 촬영(60~100만) 대신 스마트폰 촬영(11/8까지)+루크 AI 보정 — 기존 '프로필 사진 촬영·메이크업 예약'(11/10) 계획 변경 · 9회차 교육자료 발행·푸시 완료(노션 완료) · 박태경 대표(108분, 16:48 KST) — 하루 10개 소싱·일일 기록·가격관리 프로그램 매일 로그인·달바 정품 소명·리뉴얼 공지(대표님 과제) · 강의 런칭: 한 달 상담 예행연습(하루 2~3시간, 신청자 47명 중) → 기본 틀·기획안은 강사가, 협력 업체는 미팅 후 선정, 런칭 12월 말~1월 잠정, 유튜브 출연·온라인 세팅·리허설·초기 2기수 지원 → 노션 새 항목 3건(기한 추정) · 8회차 교육자료 발행 완료(노션 완료) · 노션 '강의 런칭 제안 가부 회신 대기'(11/9 진행 중) · 최은봉 대표님(30분, 14:30 KST) — 해외직판 초기 자금·인력 계획, 위수탁·정가품 소명 대응·판매처 이전 실무 논의 — 루크 Action Item 없음(과제는 대표님 몫) · 9회차 교육자료는 노션에 2건(10/29 시작 전 · 11/4 '맥 배포 필요' 진행 중) — 같은 일, 한쪽 정리 · 회사소개서 초안 검토(11/4) 결과 기록 없음</div><div class="m">플라우드 10/16 녹음 2건(정복녀 7기 · 최은봉) · 최은봉: 라로슈포제 리셀 가품 이슈로 네이버가 정품 소명 요구 — 11번가 통화 녹취는 불인정, 소명 기한 10/21 → 플라우드 10/21 세션: 장문 소명 메일 발송(수신 확인됨, 결과 미정 · 10월 말까지 연장 요청) · 비상주 사무실로 천안 사업자등록 신청 10/21(세무서 검토 중) · 개인정보 도용 신고 건 소명도 요구받음 · 일본직판(티쿤) 교육 내용은 전자책으로 7회차 참고자료에 편입(맥 배포 대기) · 10/28 세션에서 일본 야구 유니폼 직판 구조 점검: 티쿤 일본 법인 자사몰·월 정산 후 15일 지급(자금 회수 최장 45일), 일본인 직원 채용 권고 — 마진·고정비 숫자는 추산값이라 싣지 않음 · 내부 분장: 기존 스토어 운영은 직원, 사입·정식 위탁 모델 개발은 다른 직원, 대표는 일본 직판 총괄 · 박태경: 10/21 세션 2건 — 이번 주 상품 100개 등록 목표(10/25) → 성과 평가 10/27 · 공동 상품 찾기 세션 10/28 · 허위 송장 벌점 6점 · 개인사업자 소재지 분리로 사업자 3개까지·사업자당 스토어 3개 · 정복녀: 월·화 작업 공백이 주간 피크를 놓침 → 작업 일지·주 100개 등록·최저가 불일치 상품 단계 인상 후 삭제 · 7회차 자료는 10/16 발행 완료(노션) · 기한 10/20·10/23은 추정 · <b>11/7 대정리</b>: 기한 지난 코칭 후속(박태경·최은봉·정복녀 10월분)은 노션에서 정리됨 — 남은 것: 최은봉 9회차 교육자료(11/8 P0 진행 중) · 박태경 자료 회신(11/9) · 정복녀 후보 3명 연락처(11/5 지남)·2차 상담(11/9) · 신정현 자료실(11/11)</div></li>
    <li data-g="3pl-resale"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">3PL 수강생 재고 당근·외부 판매 첫 등록</div><div class="m">동의서(수수료 15~20%) → 재고 시트 판매 열 + 사진 → 당근 비즈프로필 → 30개 등록 · 통신판매업 신고 사업자 명의 필수 · 기한 10/1 지남(노션 미완료)</div></li>
    <li data-g="dino-12weeks"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">디노(미니쌤) 12주 빌드업 합의 → 10/5 1주차 시작</div><div class="m">기한 10/4·10/5 지남(노션 진행 중) — 합의·시작 여부 확인 필요 · AI 셀러 실무 교육 · 1달 90 / 2달 200 / 3달 350만 기준 · 상품별 배분 비율 확정</div></li>
    <li data-g="onecrew-inquiry"><span class="tag p0">P0</span><span class="tag cash">현금</span><div class="t">원크루·툴박스 문의 대응 — 가격 안내 후 상담 통화</div><div class="m">원크루 정가 3,900만 / 수강생 출신 3,300만 · 일십백천 990만 · 툴박스 사전 신청 안내 문구 확정 · 10/2 평생컨설팅 문의(뷰셀 수강생)에 답장 발송 → 회신 오면 진단 상담 일정 확정(기한 10/3) · 10/3 원크루 상담(홍○○ 대표님) 리포트 링크 발송(기한 10/4) → 10/17 재문의 여부 확인 · <b>11/10 상담</b>(플라우드 30분, 13:02 KST — 신규 상담 한 분): 유료 등록 전 무료 자료로 도매꾹 중심 소싱·상품 등록을 직접 해보고 재상담하기로, 전업 진입은 경계 · 네이버 정산 7일·빠른 정산 3개월 후, 쿠팡 빠른 정산 수수료 약 0.3%(강사 설명) → 재상담 확인 3가지 노션 새 항목(11/30 P2 추정) · 상담자 개인 사정은 적지 않음</div></li>
    <li data-g="free-live"><span class="tag p0">P0</span><div class="t">10/25(일) 6기 무료 라이브 진행됨(플라우드 4시간 47분 녹음, 19:29 시작) — 참석자 수·전환·7일 이용권 지급 결과는 기록 없음(<b>확인 필요</b>) · 라이브에서 안내한 정규 4주 과정: 11/6(금) 19시 시작·매주 금 라이브(3~5시간)·녹화본 12개월 · 선착순 약 30명 혜택(1:1 과외 5회·원격 설치·자동화 3종 영구 무료) · 수강료 269만(정가 319만, 12개월 무이자) · 수익 보장 환불제(3개월 과제 수행 후 무매출 시 전액 환불) · 52주 키워드표 12월 공개 예정 → 10/30(금) 저녁 6기 1주차 강의 진행(녹화 4시간 29분 → 캔바 덱 ①~⑧ 8개 영상 분할 + 유튜브 챕터 83개, 루나 · 통영상 챕터 적용 완료 · 덱별 영상 8개 업로드는 루크 몫, P0 · ⑦-2 꼬리물기는 2주차로) · 10/31 편집본 8개 완성(루나) → 강의 사이트 업로드만 남음 · 무료 공개용 5분 영상 3편 완성 — 어디에 올릴지 결정 대기(P 없음) — 라이브에서 안내한 11/6 시작과 날짜가 달라 <b>확인 필요</b> · 10/30 강의 서포트 페이지(/class) 공개: 설치 파일·1:1 상담 신청·강의 주소는 끝나면 다시보기로(클로드 코드 직접 보고 7건, 모두 완료) · [결정] ⑥ 시연 구간 메일 주소 노출은 그대로 두기(10/31) · 신규 수강생 한 분 환영 메시지 발송(10/31, P1) → <b>11/3</b> 6기 1주차: 재생목록 대표 이미지·쇼츠 5편(셀러들의 수다 채널 유입) 완료 · 「1주차 강의 정리」 페이지(영상 8편 요약 + 유튜브 편집본 8편 탭 + 이번 주 할 일 + 주문 임시 5단계) 마이페이지 맨 위 · 11/3 21:31 강의(플라우드 179분): 1주차(11/3~8) 자동등록·프로그램 작동 연습 → 2주차(11/9~15) 수동 소싱·작업지시서·옵션 변경·자동등록 연동 · 등록 비용 건당 170원 · 강사가 자동소싱 주소값 오류 수정 약속(노션 새 항목 11/9 P0) · 수강 신청자 사전 확인 절차(노션 새 항목 11/15 P1) · '6기 1주차 덱별 영상 업로드'·'편집본 업로드' 노션 항목은 여전히 미완료 — 유튜브 재생목록·강의 정리 페이지가 올라갔으니 완료 처리하면 빠짐</div><div class="m">10/25 기한 라이브 관련 노션 항목(특강 진행 · 단톡방 입장자 7일 이용권 세팅 · 가을 대표님 게스트 10분 · 테라피님 가격관리 실사용 확인)은 모두 미완료 — 끝났으면 완료 처리 · 라이브 전 클로드 코드 직접 보고 12건(방송용 임시 계정·아이디 로그인·52주 추천상품 페이지·CS 답변 템플릿 24가지·설치 무료자료·컴퓨터 생존 수첩·마이페이지 카드 등, 모두 완료) · 10/27 클로드 코드 직접 보고 6건(가입 예약 명단 · 기수별 자료 잠금 · 처음 오신 분 '파는 자리 열기' 화면 · 새 기수 분류 · 찐초보 6기 수강생 3분 등록 → 6기 5분 · 재수강 1분 처리, 모두 완료) · 남은 루크 확인(P 없음): CS 템플릿 문구 검토 · 제미나이·네이버 발급처 주소 · PDF 표지 문구 「6기 수강생 전용 자료」 · 방송 계정 카드 문구 · 설치·사용 영상 클립 7개(진행 중) · 10/27 노션 새 항목(P·기한 없음): 금요일 본강의 뒤 6기 자료 열기(같은 항목이 2건 등록 — 10/30인지 11/6인지 <b>확인 필요</b>) · 설치·사용 영상 구간 7개 올릴 곳 정하기 · 재수강 한 분 자동 처리(진행 중) · 이전 미확정 사항(신청 링크·7일 이용권 배포 채널·창고 대행 절차·마진 하한선·CS SLA·269만 환급 조건·인베이더 측 장표 수정본 수령·10/23 리허설 진행 여부)은 결과 기록 없음 · <a href="status/?p=루크 툴박스">상황판</a></div></li>
  </ul>
</div>

<h2>페이지</h2>
<div class="grid nav">
  <a href="engine/"><b>식스 엔진 — 6개 수익 프로젝트</b><span>하루 하나씩 점화 · 수익 모델 · 주간 로테이션 · 90일 타임라인</span></a>
  <a href="map/"><b>지금 어디 있는가</b><span>과거·현재·미래 · 1주/1달/분기/반기/1년에 얻어야 하는 결과</span></a>
  <a href="ilsip/"><b>일십백천 — 유지할 것과 바꿀 것</b><span>간판은 바꾸고 커리큘럼은 지킨다 · 500명 중 8명을 집어내는 장치</span></a>
  <a href="review/"><b>전략 재점검 — 남에게 가르친 것과 자기 회사</b><span>플라우드 3인 대화 · 광고비 2배 충돌 · 전문가 6인 비평</span></a>
  <a href="park-contract/"><b>민트(박종혁) — 1차 계약서</b><span>서명 가능한 완성본 · 민트 6:루크 4 · 제가 정한 일곱 가지</span></a>
  <a href="cash/"><b>11월 ~ 2월 — 들어올 돈과 나갈 돈</b><span>월별 순현금 · 민트 건 첫 수익은 2/22 · 계약서 수정 2건</span></a>
  <a href="oct23/"><b>10월 23일 — 세 대화</b><span>민트·메이븐·돈벌쥐 PD · 3,000만의 정체 · 인베이더 리스크</span></a>
  <a href="pd/"><b>조윤호 PD — 장기 파트너십 설계</b><span>보상 3층 구조 · 구간별 정액 · 채널 소유는 법인</span></a>
  <a href="pd-long/"><b>채널 운영 — 비용을 어떻게 잡나</b><span>유튜브 6:4 검토 · 애드센스는 PD 100% · 장기 %는 미루기</span></a>
  <a href="exit300/"><b>300억 엑시트 — 가능한가</b><span>2년 내 300억 역산 · 활성 셀러 2,000명 · 법인 장부가 먼저</span></a>
  <a href="meetings/"><b>스스로 월백 회의록 (공유용)</b><span>민트님·PD님과 함께 보는 외부용 · 10/30 킥오프 · 11/4 정기회의</span></a>
  <a href="pd-cost/"><b>PD 촬영비 — 민트님께 드릴 내용</b><span>11/2 조윤호 PD 통화 · 인당 30~35만 · RS는 턴키 매출 %</span></a>
  <a href="gaeul-contract/"><b>가을 대표님 계약서 — 괜찮은가</b><span>10/31 녹취 대조 · 합의에 없던 두 줄이 5,022만 · 루크님 몫 603만</span></a>
  <a href="park-terms/"><b>협업 조건 정리 (민트님 발송용)</b><span>외부용 · 입력란과 메일 발송 버튼 포함</span></a>
  <a href="roadmap/"><b>돈 버는 로드맵</b><span>수익 줄 · 3단계 · 원칙</span></a>
  <a href="priority/"><b>우선순위</b><span>P0 → P3 · 보류 목록</span></a>
  <a href="people/"><b>사람별 현황</b><span>메이브님·디노·뿌요·지영</span></a>
  <a href="schedule/"><b>일정 도식</b><span>10월 타임라인 · 마일스톤</span></a>
  <a href="invader/"><b>인베이더 종료 대비</b><span>10/6 들은 이야기 · 마지막 기수에 챙길 것</span></a>
  <a href="corp/"><b>힐링디어스 → 셀러들의 수다</b><span>경기 창고형 매장은 지금 · 서울 빌딩은 2027-03-16 이후</span></a>
  <a href="relocation/"><b>10/16 등기 — 등기부 확인 끝</b><span>중임은 완료 · 본점이전 + 상호 + 목적 + 수권주식</span></a>
  <a href="money/"><b>재정 정리 — 무엇부터 털어야 하나</b><span>대환 우선순위 · 금리 순서 · 시트는 26년 5월 기준</span></a>
  <a href="credit/"><b>신용점수 — KCB 622 / NICE 750</b><span>농협 카드 거절 이유 · 꼬마빌딩 대출 심사와의 연결</span></a>
  <a href="crew-prompt/"><b>크루원 사업 구조화 — 프롬프트</b><span>기존 흐름에 얹는 짧은 버전 · 이름·충돌·노출만</span></a>
  <a href="jiyoung-prompt/"><b>지영 원장 빌드업 페이지 — 프롬프트</b><span>새 저장소로 만들 때 복사해 쓸 프롬프트</span></a>
  <a href="jiyoung-survey/"><b>지영 설문지 발표 — 쪽마다 할 말</b><span>받은 피드백 → 고친 것 → 안 고친 이유</span></a>
  <a href="vault/"><b>셀프 등기 · 정관 찾기 · 서류 보관</b><span>법무사를 쓸지, 정관은 어디서 찾는지</span></a>
  <a href="registry-forms/"><b>등기 서류 — 다 만들어 뒀습니다</b><span>서류 8장 · 준비물·비용·동선 전부 · 대표이사 쟁점</span></a>
  <a href="registry-prep/"><b>등기 변경 — 준비물 체크리스트</b><span>금요일에 할 것 · 신정현 대표님 준비물 · 기한 10/16(페이지 안 10/15 표기는 옛 기한)</span></a>
  <a href="iros/"><b>등기부 열람 — 클릭 순서</b><span>인터넷등기소에서 중임 기록 확인하기 (700원)</span></a>
  <a href="pilot/"><b>파일럿 강사 결정</b><span>가을 대표님으로 확정 (10/7) · 결정 근거</span></a>
  <a href="park/"><b>박종혁 본부장 협업 — 평가</b><span>10/10 수정판 · 네 가지 철회 · 남은 세 칸과 밀도 지표</span></a>
  <a href="chowol/"><b>초월스토리 강사 협업</b><span>10/6 계약 조건 · 12월 런칭 · 어긋나는 숫자</span></a>
  <a href="maven/"><b>메이브님 공동 액션 플랜</b><span>10/6 회의 — 구독·스토어·오프라인 3축</span></a>
  <a href="trademark/"><b>키티티바이지영 상표 출원 설계안</b><span>키프리스 0건 · 44+41류 · 유리한 근거 7가지 · 견적 준비물 (10/29 v2)</span></a>
  <a href="totalshop-license/"><b>토탈샵 전환 — 영업신고·사업자등록</b><span>원장 면허 병목 · 서비스별 업종 · 샵인샵 3경로 · 위생과 질문 (10/29)</span></a>
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
<p class="note"><b>11/7 액션보드 대정리</b>: 루크가 노션 미완료 896건 중 329건을 휴지통으로 옮김(30일 복구 가능 · '나중에 할 안건' 페이지 95건) — 이 페이지와 일정에서 해당 항목 239건을 11/8에 뺐음. 기준: 현금에 가깝고 다른 일의 선행 조건일수록 위. 기한은 노션 액션보드 기준. [결정]은 완료로, [보류]는 P3로. <span class="tag">새 항목</span>은 최근 7일(11/6~) 안에 노션에 생긴 미완료 항목입니다.</p>

<h2>P0 · 이번 주 <small>~11/15</small></h2>
<div class="card red">
  <ul class="list tasks">
    <li data-g="developer-accounts"><span class="tag cash">선행 조건</span><div class="t">개발자 계정 3종 등록 — Apple Developer / Google Play / Microsoft Store</div><div class="m">기한 10/2 지남(노션 미완료) · 앱 배포(툴박스 PWA→앱, 영상공장, 블로그타이퍼) 전부의 앞단. 루크가 "제일 높은 등급"으로 지정(9/30)</div></li>
    <li data-g="platform-director-meeting"><span class="tag cash">현금</span><div class="t">박종혁 본부장 협업 — 10/9 회의 진행(녹음) → 10월에 정할 세 칸(10/16 · 다섯 칸에서 축소)</div><div class="m">월 300만 고정 3개월·수익 6:4·카페 3,000명 목표(녹음 요약, 계약 미확정 · 총액 확인 필요) · 노션 '10/8 종혁 본부장 미팅'은 미완료 — 완료 처리 확인 필요 · <a href="../park/">협업 평가</a> · <a href="../platform/">전략 페이지</a></div></li>
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
    <li data-n="https://app.notion.com/p/3eb0cf8fea04812b8f86e2d58503588d"><span class="tag cash">현금</span><div class="t">키티티 AI 스타일 미리보기(/try) 구축</div><div class="m">기한 10/4 · 진행 중 · 무료 1회·워터마크·유료 원본 다운로드</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481b1af7ac611bcbe1835"><span class="tag cash">현금</span><div class="t">수강생 컨설팅 후속 — 소장 대응 결정·리셀 정리·브랜드 재점검 (익명)</div><div class="m">기한 9/30 · 노션 '진행 중'</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04814187b8c258b3a2d38e"><span class="tag cash">현금</span><div class="t">키티티 '연봉 10억 만들기' 페이지 배포 (저장소 kititi-1b)</div><div class="m">기한 10/4 · 진행 중</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea0481698468f35e62d2e19b"><div class="t">키티티 사이트 웨딩 메인 전환 + 첫 화면 사진 30초 자동 교체</div><div class="m">기한 10/8 · 진행 중 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481a7b0c0cfc85f4b3475"><div class="t">힐링디어스(주) 본점 주소 확보 + 본점이전 등기·사업자등록 정정</div><div class="m">기한 10/15 · 진행 중 · 새 본점 주소 확보 완료(10/9) → 10/12 법무사 위임 완료 → 10/16 등기 제출 후 사업자등록 정정</div></li>
    <li data-n="https://app.notion.com/p/3ee0cf8fea0481fa9237cd0b76f22b45"><div class="t">매장 대청소 — 업체 선정(비포에프터클린) → 10/5 14:00 작업 입회·검수</div><div class="m">입회·검수 항목은 기한 10/5 · 노션 '진행 중', 업체 선정 항목은 '시작 전' — 끝났으면 둘 다 완료 처리 필요 (10/4·10/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ee0cf8fea04815d91cdf96ae0a85075"><span class="tag cash">현금</span><div class="t">6기 무료 라이브(10/25) 준비 — PPT 제작(B스타일 네이비&크림으로 새로) · 남은 미결정 사항 확정 · 수강생 인터뷰 5명 섭외·자료</div><div class="m">모두 기한 10/11 · PPT·미결정 사항은 진행 중 (10/4 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea04812c9dbfcf46c011ba42"><span class="tag cash">현금</span><div class="t">키티티 AI 뷰티 플랫폼 — 전환 검증 실험(랜딩+사전예약) · 진단 링크 홍보·파트너샵 마케팅 키트 1판 · 홈페이지 클릭 수 기록 시작 · K-뷰티 크리에이터 챌린지 공고 확인</div><div class="m">모두 기한 10/11 · 검증 통과 기준: 랜딩 방문 300명 중 예약금 결제 10명 (10/4 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481e4a78edf0ea6527d5c"><span class="tag cash">현금</span><div class="t">신규 강의 플랫폼 — 3자 미팅 제안서 1차본 검토(10/6) · 3자 1:1:1 안과 초월스토리 8% 모델 관계 정리(10/8) · 시행 전 선행 조건 4가지·계약서에 '수강생 명단·결제 창구·강의 콘텐츠 = 셀수다 소유' 조항(10/13)</div><div class="m"><a href="../platform/">전략 페이지</a> (10/6 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481b2b5f9c0ab5aa17594"><span class="tag cash">현금</span><div class="t">인베이더 종료 대비 — 종료 사실 확인·메이브님과 마지막 기수 공동 대응 합의(10/8) · 계약서 소유 조항 확인(10/11) · 수강생 명단을 자체 채널로 옮기는 동선(10/12) · 사입 재고 처리 가이드라인(10/13)</div><div class="m"><a href="../invader/">인베이더 종료 대비</a> (10/6 등록 5건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048159873bcb81c41d12e9"><span class="tag cash">현금</span><div class="t">메이브님 공동 액션(10/6 회의) — 메이븐 스토어 재정비·집중 품목 선정(메이브님) · 사입 재고 처리 가이드라인 · 루크 툴박스 토스 연동+깃허브 자동 업데이트 · [결정 필요] 2,000만 지출 세무 처리 · [결정 필요] 뿌요 역할·수익 구조</div><div class="m">기한 10/11~10/13 · 같은 회의가 노션에 두 번 등록돼 겹치는 항목이 있음(스토어 재정비·가이드라인·세무 처리) — 한쪽 정리 필요 · <a href="../maven/">메이브님 공동 액션 플랜</a> (10/6 등록 7건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481a89c87d347be379b54"><div class="t">원크루 사이트 — '푸시하면 자동 배포' 연결(루크 클릭 대기) · 박태경 대표께 새 자료실 주소 전달 → 깃허브 원본 저장소 정리 · 관리자 비밀번호 정하기 · 뿌요님을 원크루 명단에 올리고 '목표 수익 관리' 열어 주기</div><div class="m">기한 없음 (10/6 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048138b075f9bb51f5e97e"><div class="t">변경등기(본점이전·상호·목적·이사선임) 제출은 10/16 완료(노션) → 사업자등록 정정신고(노션 기한 10/16 → 10/23) · [결정 필요] 셀러들의 수다 = 힐링디어스 상호변경 확정(10/11) · 4대보험 소재지 변경(10/15) · 세무사 수입금액 조회(10/8)·세무사 통화(10/9)는 기한 지남 · 정관 찾기(10/10)</div><div class="m">법인 정리·사업장 이전 · 등기 완료(등기사항전부증명서) 여부는 노션에 기록 없음 — 확인 필요 · 사업목적 41개·수권주식 100,000주는 [결정] 완료 · 정관은 10/9 [결정]으로 전부개정 — '정관 찾기' 항목은 완료 처리 확인 필요 · <a href="../relocation/">등기 페이지</a> (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048126a2fec9d1efd1c0eb"><span class="tag cash">현금</span><div class="t">초월스토리 강사 협업 — 계약서 정산 기준 정리·가을 대표님 의향·일정 확인·성과 숫자 확보(10/11) · [결정 필요] 루크 참여 범위·정산 기준 문서화·원크루 관계 유지(10/22) · 고연령 성과자 섭외(10/25)</div><div class="m"><a href="../chowol/">초월스토리 페이지</a> · <a href="../pilot/">파일럿 강사 결정</a> · '파일럿 강사 선정'은 노션 완료 (10/6·10/7 등록 7건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481b3bd6dc3d1bfd8fa95"><div class="t">루크 툴박스 결제·법적 필수 — 포트원 결제사 선택(KG이니시스, 루크 확인 후 제출) · 공방 사이트 유선번호 1개 · 실결제 전까지 프로그램 구매 길 막을지 결정 + 9월 테스트 구독·주문 자국 정리 · 토스 신청 멈춤 확인</div><div class="m">기한 없음 · 3개 문서·푸터는 완료 (10/7 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea048152b55cec152c0f6fc9"><span class="tag cash">현금</span><div class="t">[막힘] 사업 구조화 페이지 저장소 만들기 — 지영 원장(kittiti-jiyoung) · 신정현 대표(onecrew-shin-jeonghyeon)</div><div class="m">기한 10/11 · 루크가 깃허브에서 공개 저장소 생성 + Pages 켜기 + Claude 권한 추가 → 각 채팅이 push (10/7 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea0481faa420daf4c6647ca1"><span class="tag cash">현금</span><div class="t">초월스토리 — 루크 참여 범위를 공동 기획으로 올릴지 (5:5 분모에 들어가는지)</div><div class="m">기한 10/22 · 배분 초안 전에 제기 · <a href="../chowol/">초월스토리 페이지</a> (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea0481d396d6fb41d1c6ee6b"><div class="t">구리세무서 재산법인세과 전화 — 법인등기 진행 중, 완료 후 재신청 예정 알리기</div><div class="m">기한 10/8 · 10/7 사업장 이전 신고 취하 통지 — 거부가 아니라 순서 문제 · <a href="../relocation/">10/15 등기 페이지</a> (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f30cf8fea0481cc8bc6f8687a37a03a"><div class="t">힐링디어스 법인 등기 — 정관 원본 찾아 본점 조항 확인('구리시'까지인지 번지까지인지) · '셀러들의 수다' 상호 중복 확인(인터넷등기소) · 신정현 대표님께 등기 제출용 준비물 전달 + 인감 신고 여부 확인</div><div class="m">모두 기한 10/9 · <a href="../registry-prep/">준비물 체크리스트</a> (10/8 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3f30cf8fea04813fab69eb44001ba56d"><span class="tag cash">현금</span><div class="t">초월스토리 강사 협업(10/8 추가) — 가을 대표님 몫 2,200만 산출 근거 확인 · 광고 예산 약 4,500만 확인 + 상한·중단 기준 · 가을 대표님께 손익분기 인원·광고비 리스크 사전 설명 · 6:4 합의 서면화 · [결정 필요] 6:4를 숨길지 공동 기획으로 공개할지</div><div class="m">모두 기한 10/22 · 4,500만은 2,200만에서 역산한 값이라 초월스토리 확인 전 · <a href="../chowol/">초월스토리 페이지</a> (10/8 등록 5건)</div></li>
    <li data-n="https://app.notion.com/p/3f30cf8fea048125b5f0cb4b24793347"><span class="tag cash">현금</span><div class="t">키티티 토탈샵 — 인테리어(급배수·전기 증설·칸막이·냉난방기) 승인 별첨 문서 준비 · 임대차 특약 수정안 협상(제소전화해·원상복구·갱신)</div><div class="m">둘 다 기한 10/11 지남 · 특약 협상은 진행 중 — 10/8 계약은 노션 완료 처리됨, 이 둘도 끝났으면 완료 처리 필요 (10/8 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea048198a344fb2711f2b3f5"><span class="tag cash">현금</span><div class="t">일십백천 새 사이트에 넣을 값 확정 — 기수·정원·마감일, 환불·할부 문구, 강사 소개 숫자, 강사 사진, 후기 공개 범위, 도메인</div><div class="m">기한 없음 · 1차 제작은 10/8 완료 — 이 값만 채우면 공개 가능 (10/8 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea0481a3a3c8f22c07545cd2"><div class="t">변경등기(10/9 추가) — 기장 세무사무소에 사업연도 확인 · 등록면허세 중과 여부·'그 밖의 등기' 건수 확인 · 법인인감카드 분실 사용정지+법인인감도장 확인 · 법무사 위임 시 서류 목록(위임장·법인인감증명서) · 전부개정 정관 마무리(이상 10/12) · 루크 확정 4가지 정하고 출력·날인 · 목적 추가 문구 확정(이상 10/9)</div><div class="m">법인 정리·사업장 이전 · 신정현 대표님 서류 3종 수령은 10/12 완료 · 10/9 [결정] 3건: 이전일 10/2 · 정관 전부개정 · 대표이사 선임 · <a href="../registry-forms/">등기 서류 페이지</a> (10/9 등록 8건)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea04811ca54cf38b0d15e46f"><span class="tag cash">현금</span><div class="t">박종혁 본부장 협업 — 10월에 정할 세 칸: 차감 산정 방식 · 3PL·리셀·프로그램 매출은 6:4 밖 · 총액 인식 일치(10/16) · 물어볼 한 가지: 카페 월 4,000명 만들 당시 광고비(10/14)</div><div class="m">10/10 루크 반론을 반영해 다섯 칸에서 세 칸으로 축소(노션 메모) · 3개월 지표는 머릿수에 밀도(글 쓴 사람 수 등)를 함께 봄 · <a href="../park/">협업 평가</a> (10/9 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f60cf8fea0481f4b959c5ab85ecda7a"><div class="t">일십백천 새 강의실 — 아임웹 강의실에 한 번 로그인해 두기 (강의 제목·영상 주소 옮기기용)</div><div class="m">기한 없음 · 수강생 강의실 제작은 10/11 완료(담당 루나) · 크롬에서 아임웹에 로그인해 두면 클로드가 강의 제목·영상 주소를 그대로 옮김 (10/11 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f80cf8fea048164b79ef6d1c68a5bb7"><div class="t">부가세 2기 예정분 신고·납부 — 힐링디어스(주) 신고 대상인지 / 개인 예정고지 확인</div><div class="m">기한 10/26(법인 신고) · 예정고지 납부는 11/2 · 법인은 직전 반기 공급가액 1.5억 이상이면 예정신고 (10/13 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f80cf8fea0481c78c58d84e2b504612"><div class="t">법무사 10/12 상담 후속 — 사업자등록증 사본 문자 전송 · 빠진 서류 재준비해 재방문 일정 조율 · 정관·회의록 재작성 결과 확인(터미널 운영·화물 운송 목적 제외)</div><div class="m">기한 10/16 · 플라우드 10/12 상담 녹음 · 주식 수 100만 주 권고는 기존 [결정] 수권주식 100,000주와 달라 확인 필요 (10/14 등록)</div></li>
    <li data-n="https://app.notion.com/p/3fb0cf8fea04811c8806e29ce0d66548"><div class="t">지영 서포트 운영(10/16 재설계) — 검토용 보관함 노션 1페이지 개설(10/19) · 네이버 플레이스 예약 슬롯 설계 1장(10/19, 지영은 11/1 입력만) · 인스타 편집 협업자 위임 시스템 — 역할 정의·15분 가이드 템플릿·첫 작업 가이드(10/22)</div><div class="m">10/11 플라우드 녹음 근거 [결정] 서포트 모드 전환(결정 요청 주 1회·3개 이내 묶음, 질문 대신 초안, 보관함은 알리지 않음) · 협업자는 수습 프레임, 피드백은 루크가 주 1회 10분 (10/16 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3fd0cf8fea0481858d7ce31805c939c2"><span class="tag cash">현금</span><div class="t">키티티 토탈샵 오픈 준비 — 헤어 기기·약제 공급처 결정(로레알 1순위 · 7가지 답 확보 · 기존 기기 4대 철거, 10/25) · 권리금 계약 인도 조건 부속 합의(중개사 문자 → 인수·철거 목록 → 부속 합의서 + 임대인 특약 별첨, 10/25) · 인스타 공식 계정 구조 1장(10/25)</div><div class="m">10/18 회의 녹음 4건 근거 · [결정] 3건 완료(오픈 준비 순서 · 인력 구조 권장안 · 프리오픈 1/26~31·정식 2/2) · 계약금 10% 기납부, 해제 카드는 쓰지 않음 · <a href="../hair-vendor/">헤어 공급처 비교</a> (10/18 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3fe0cf8fea0481cb8bd8d421504fad3b"><div class="t">6기 무료 라이브(10/25) 10/19 기획 회의 후속 — 최종 리허설 10/23(금) 11:00 + 전날 리마인드 · FAQ 섹션·'하루~3일 내 첫 수익' 메시지·50·60대 톤 문안(10/23) · 출연 수강생 연락처 수령 후 16시 전 도착 사전 연락(10/24)</div><div class="m">플라우드 10/19 녹음 Action Item 3건 — Speaker 1을 루크로 추정, 기한 10/23·10/24는 추정 · PPT 3부 리빌드·수동 vs 프로그램 비교 시나리오·세일즈 혜택 정리는 강사 측 · 미확정: 데모 범위·무료 수강권 퀴즈 규칙·출연 식순·재고 매입 혜택 조건 (10/20 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3fe0cf8fea0481f187f4d10ef54018eb"><span class="tag cash">현금</span><div class="t">박종혁 본부장 10/21(수) 첫 출근 — 사무실 책상 정리 + 수요일 일정 조율·피자 회식</div><div class="m">플라우드 10/19 신정현 대표님 회의 Action Item(루크·메이브님 공동) · 합류 첫 미팅(닫을 것 다섯)은 별도 (10/20 등록)</div></li>
    <li data-n="https://app.notion.com/p/4000cf8fea048121af5ddd2840682d1f"><div class="t">원크루 사이트 — 사업 아이디어 점검(회차 주고받기 · 관리자 '클로드에 붙여 넣을 글 복사' 버튼 · 관리자 전체 진입) 발행 → Supabase에 아이디어 점검 표 만들기(migrations/0002 SQL 1회 실행)는 루크 로그인 뒤 실행</div><div class="m">10/21 노션 2건(진행 중 · 시작 전) · 10/21 상황판 '막힘' 보고(클로드 코드 직접 push): 데이터베이스 로그인이 풀려 있어 표 만들기에서 멈춤 — 루크가 Supabase에 로그인하면 이어서 실행 · 외부 AI를 사이트에 붙이지 않아 비용 0원 · 자료는 회원별 구글 드라이브 폴더(회원 정보에 주소 칸) · 교육자료 동의 체크 · 담당 미기재 · <a href="../status/?p=원크루 사이트">상황판</a> (10/21 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea048130a802fa2cefc1c2cb"><div class="t">물류팀 보고 체계 — 매일 18:30 브리핑(15~20분) 고정 + 사실/경험/의견 분리 보고 양식(10/27) · 일일 KPI(처리 건수·시간 준수·보고 적시성) 설정 → 1주 평가 + 1:1 면담(10/31, P1)</div><div class="m">10/24 새벽 물류 업무 회의(플라우드 25분, 루크·리나님·뿌요) 조치 사항 → 노션 새 항목 2건 · 함께: 송장 잔류 금지(미처리 0건 확인 후 퇴근) · 합배송 출고 오류 사전 신고 · 오배송·반품 즉시 공유 · 근무표·알람(CS 시간) 의무화 · 처리량은 하루 300건 기준 탄력 조정 (10/24 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/4030cf8fea0481fa99adccab0f1e3d76"><span class="tag cash">현금</span><div class="t">최은봉 대표님 — 10월 4주차(8회차, 일본 직판) 교육자료 발행 · 작성·push는 끝났고 맥에서 배포만 남음(10/26, 진행 중)</div><div class="m">10/24 클로드 코드: 플라우드 10/21 세션(57분) → s08 작성·check:crew 통과·push 완료(노션 메모) · 같은 날 정복녀 대표님 7회차(10/23 통화) 자료 발행·푸시는 완료 처리됨 · 7회차 참고자료(일본직판 전자책)·원크루 개인 자료실도 같은 맥 배포 대기(10/31) (10/24 등록 2건, 완료 1건 제외)</div></li>
    <li data-n="https://app.notion.com/p/4040cf8fea0481e59c55c8b91c9642b1"><div class="t">테라피님(6기 라이브 출연 수강생) 인터뷰 준비 — 인터뷰 전 가격관리 가입·자동등록 실사용 확인(10/25 · 10/23 기준 미가입, 안 되면 '이번에 막 세팅했다'로 답변) · 인터뷰 준비 가이드북(Claude Docs + A4 15쪽 PDF)은 10/25 완료</div><div class="m">10/23 인터뷰 준비 코칭(플라우드 54분) 기반 · 라이브는 10/25 진행됨(플라우드 4시간 47분 녹음) — 실사용 확인 항목은 노션 미완료, 끝났으면 완료 처리 (10/25 등록 3건, 완료 1건 제외)</div></li>
    <li data-n="https://app.notion.com/p/4050cf8fea0481d7ad23ca41accf02d4"><div class="t">키티티 토탈샵 고대생 할인 배너(40×10cm) — 캔바 편집본 만들기(이미지·텍스트 레이어 분리, 11/1 · 진행 중)</div><div class="m">10/26 노션(채팅 '키티티 배너 캔바 변환') · 클로드 작업공간에서 canva.com 직접 업로드가 막혀 루크가 캔바에 이미지를 올리거나 업로드 경로를 정하면 진행 · 같은 날 '배너 캔바 편집본(40x10cm) 만들기'는 완료 처리됨(글씨 13개는 편집 가능한 텍스트, 그림은 조각별 업로드, 캔바 편집 주소 확보) — 같은 일이면 진행 중 항목 완료 처리 확인 (10/26 등록 2건, 완료 1건 제외)</div></li>
    <li data-n="https://app.notion.com/p/4070cf8fea048186b60cdc9e58c31272"><span class="tag cash">현금</span><div class="t">가을(정복녀) 대표님 코칭 알바 운영안 확정 — 강의 시작 전 한 달, 수강생 1인 30~40분 1만원, 주제는 설치·자동등록·상품 찾기, 메이브님과 일정 조율(10/30 지남 · 노션 미완료) · 설치·자동등록 표준 가이드 + FAQ 답변 멘트 제작·배포(11/1)</div><div class="m">플라우드 10/28 '[OneCrew] 정복녀 대표님 찐초보 7기'(32분) Action Item → 노션 새 항목 2건, 기한은 노트 기재값 · 메인은 프로그램 기반, 수동 '꼬리물기'는 보조 · 예약 방식·결제(선불/후불)·품질 기준은 미정 · 가을님 몫(판매 이력 상품 재등록 · 근무 로그 1개월 기록 · 초월스토리 영상 2개 시청)은 넣지 않음 · 가을님 가능 시간대는 녹음 참고 (10/29 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/4070cf8fea0481e4b3cff5506781f63d"><span class="tag cash">현금</span><div class="t">최은봉 대표님 — 10월 5주차(9회차) 교육자료 발행: 10/28 세션 + 지난주 업데이트 정리해 원크루 사이트 게시(10/29 · 노트 기한 '오늘'=10/28 지남)</div><div class="m">플라우드 10/28 '[OneCrew] 최은봉 대표님'(24분) 루크 Action Item · 세션 요지: 천안 비상주 사무실 신규 사업자등록 발급 · 정품 소명 건은 플랫폼 회수·환불로 종결 · 개인정보 위수탁 소명 연장(10/30) 회신 대기 · 신규 스마트스토어는 사업자 아이디로 개설 추진 · 일본 야구 유니폼 직판은 토요일(11/1) 재무·원가 강의 뒤 지속 여부 결정 · 8회차(10/26) 맥 배포도 아직 노션 진행 중 (10/29 등록)</div></li>
    <li data-n="https://app.notion.com/p/4080cf8fea0481849c91e543cc4dbfd7"><span class="tag cash">현금</span><div class="t">키티티바이지영 상표 출원 — 지영 특허고객번호 신청(특허로, 수수료 없음) + 의견서용 사용 증거 수집(간판·플레이스·인스타·사업자등록증 캡처, '만지다' 어원 언어 확인)(11/1) · 상표 출원 대행 견적 2곳 + 지정상품 초안은 10/29 → 11/1 P0 '진행 중'으로 바뀜</div><div class="m">10/29 클로드 대화 '키티티바이지영 상표 출원' → 노션 새 항목 1건 + 기존 항목 기한·P 변경 · <a href="../trademark/">상표 출원 설계안 v2</a>(키프리스 키티티·KITITI 0건, 44류 KITTY 6건 · 유리한 근거 7가지·반대 판례 3건 · 견적 요청 시 '의견서 대응 포함 여부' 비교) · 로고에 고양이 모티프 넣지 말 것 (10/29 등록)</div></li>
    <li data-n="https://app.notion.com/p/4080cf8fea0481aebd1de20523faf9d0"><span class="tag cash">현금</span><div class="t">키티티 토탈샵 전환 — 지영 원장 영업신고증·미용사 면허 종류 확인 + 성북구청 위생과 문의(2·3층 단일 영업소 · 속눈썹 업종 · 샵인샵 구획)(11/5) — 인테리어 도면(1월 시공) 확정 전 선행 조건</div><div class="m">10/29 클로드 대화 '토탈샵 전환 영업신고 변경' → 노션 [보고] 1건(완료, 상황판 이관) + 새 항목 1건 · <a href="../totalshop-license/">영업신고·사업자등록 변경 정리</a>: 핵심 병목은 원장 본인 면허(업종 추가 시 해당 면허 필요, 법인·이중신고 불가) — 피부·네일 면허가 없으면 3층은 샵인샵 별도 신고 · 함께 확인: 건축물대장 2·3층 근린생활시설, 세무사 업종코드 추가·과세유형, 상표 지정서비스에 피부·네일 포함 여부 (10/29 등록)</div></li>
    <li data-n="https://app.notion.com/p/4090cf8fea0481a2982cf9e5b5e7aa70"><div class="t">셀수다 자동상품등록 프로그램(자동후불사입용) 전면 개편 — 12개 항목: 설치 진행률·화면 2버튼·전자책·사전점검·수동입력·재설치 없는 업데이트 + AI 비용 60~70% 절감 (진행 중, 기한 없음)</div><div class="m">10/30 채팅 '셀수다 자동등록 / 전면개편' · 상세이미지 글자 읽기를 제미나이 비전(상품당 19회·약 114원)에서 윈도우 내장 OCR(2배 확대 시 라벨 정확, 0.3초) 하이브리드로 전환 · 확장은 압축해제 로드라 chrome.runtime.reload()로 무재설치 업데이트 가능 · 미확인: 가입자 관리용 컨설팅 시트 주소·열 구성 · 함께 등록: 내려받는 주소 + 안내 문구 바로잡기(v234/b177, P 없음) (10/30 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/4090cf8fea0481ab9bb9e616b865e702"><div class="t">자동소싱 인수 — 소싱 연동을 어디에 붙일지 결정(A: 내 v234에 이식 / B: 인계본으로 갈아타기 / C: 소싱만 따로 — A안 권장) · 구글시트를 원작자와 같이 쓸지 따로 쓸지(P1) · 기한 없음</div><div class="m">10/31 채팅 '자동소싱 인수 / 분석': 인계본 286개 파일 전수 분석 완료(소싱 4.90 크롬 확장 + 등록 v235/b182, 등록대기목록.csv 한 파일로만 연결 · 정리 문서 인수분석_정리.md) · 내 v234/b177에는 소싱연동·번갈아·제외브랜드·허용카테고리·하루상한 함수 29개가 없고, 인계본에는 윈도우 OCR·무재설치 업데이트·수동입력·보안점검 27개가 없음 · 인계본은 원작자 시트로 로그인·기록을 보내게 빌드돼 있음 — 따로 쓰려면 새 시트 2개+앱스스크립트 2개 배포 후 AUTH_URL·SCRIPT_URL 바꿔 재빌드, 수강생 전원 재가입 필요(비밀번호 이관 불가) (10/31 등록 3건, 완료 1건 제외)</div></li>
    <li data-n="https://app.notion.com/p/4090cf8fea048110bd60ebd0eaf0b6c0"><div class="t">6기 1주차 덱별 영상 8개 유튜브 업로드(스튜디오에서 직접) — 재생목록 '6기 1주차', 각 설명란에 챕터 · 기한 없음</div><div class="m">10/31 클로드 코드: 1주차 녹화(원본 4:28:57 → 대기·휴식 제외 실강 3:53:37)를 캔바 덱 ①~⑧ 8개 영상으로 분할 + 챕터 83개(완료, 루나) · 통영상 설명란 챕터 83개 적용 완료(vidIQ, 일부공개 유지) · vidIQ로는 새 업로드 불가, 파일·설명문은 덱별_설명문 폴더에 준비됨 · ⑦-2 심화 실천(꼬리물기)은 녹화에 없어 2주차로 · [결정] ⑥ 시연 구간 메일 주소 노출은 그대로 두기 (10/31 등록 4건, 완료 3건 제외)</div></li>
    <li data-n="https://app.notion.com/p/40a0cf8fea0481d1978df8d03cc3729b"><div class="t">6기 1주차 편집본 8개 완성(루나, 10/31) → 루크 확인 후 강의 사이트(인베이더스쿨 1~8교시) 업로드만 남음 — 3:48:26 · 자막 4,948개 · 4.2GB(전 7.4GB) · 제목·설명은 영상 옆 _편집본_타임라인.txt 그대로 · 덱별영상 폴더(자막 없음)는 올리지 말 것 (P0, 기한 없음)</div><div class="m">10/31 클로드 코드(루나) 진행 중 5건: 재생 문제 점검+키프레임 설정 · 자막 문맥 끊기 규칙 재작성(어색한 끊김 1,398 → 94곳) · 챕터 화면 빼고 음성인식 새로(mlx-whisper, 단어 단위 싱크) · 대사 전문 교정 177개 · 자막 밀림 최대 9초 원인(자막 트랙 time_base 1/25 vs 1/30 기준 소수) 수정 → 최종 검사 64곳 모두 제자리 · 루크 몫 2건(편집본 확인 후 업로드 · 업로드만 남음)은 같은 일 — 한쪽 정리 · 함께: 무료 공개용 5분 영상 3편 완성, 올릴 곳 결정 대기(P 없음) (10/31 등록 8건, 완료 1건 제외)</div></li>
    <li data-n="https://app.notion.com/p/40a0cf8fea0481dc9af9fd9e61ceb1b0"><div class="t">셀수다 자동소싱 v4.94 → v4.96 — 루크: 로그인 한 번 + 묶음 키워드 한 판 돌려보기(기한 없음) · 루나: v4.95 재설치 없는 업데이트+설치파일 10.2MB+2주 리뷰 수(진행 중) · v4.96 빈 수량 자리 찾기(코드·시험 101/101 완료 — 네이버가 제목 ', 4개'로 새 수량 옵션을 만드는지 루크 확인 전 배포 보류)</div><div class="m">10/31 클로드 코드(루나) · 완료 2건: v4.94 배포본 묶기(11개 파일 224KB)+설치안내·바뀐것 새로 씀 · 소싱 배포 저장소 공개+깃허브 2단계 인증(0.1→4.95 갱신 실측, 바뀐 1개만 받음) · 비밀번호는 루나가 다룰 수 없어 틀린 비번으로 통로만 확인하는 시험 스크립트 준비 → 한 판 돌린 뒤 진단 파일을 주면 선택자 보정 (10/31 등록 5건, 완료 2건 제외)</div></li>
    <li data-n="https://app.notion.com/p/40a0cf8fea04812c86b1ca5619a915e3"><span class="tag cash">현금</span><div class="t">초월스토리 10/31 회의 후속 P0 3건 — 파트너십 계약서 초안 작성·법 조항 확인·상호 교환(11/1) · 강의 PPT 초안(루크·뷰셀님) → 세일즈 파트에 전달해 소구점·성과 데이터 보강(11/7) · 인베이더 파트너십 최종 종료 미팅 준비+합의서(11/7)</div><div class="m">플라우드 10/31 '10-31 회의'(76분, 초월스토리 측과 가을 대표님 강사 런칭) Action Item → 노션 새 항목 19건 중 P0 · 정산 틀: 순수익 5:5 · 시스템 전체 이용 시 PG 제외 8% · 단순 강사 소개 4% · 광고비 회계 처리 기준 · 기본반(289만 기준)+심화 프리미엄반 이원화 검토 · 11/1·11/7은 요약 기재값 (11/1 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/40c0cf8fea0481aaa079de43c9e517af"><div class="t">멘토루크 예약시스템 — 6기 수강생 등록(11명 중 10명 → '가입대기' 명단으로 11명 전원 완료) + 1:1 과외 신청(2시간) 메뉴·공지 (P0 진행 중, 기한 없음)</div><div class="m">11/2 클로드 코드: 유형 수강생·메모 '6기'·잔여 5회 · 기존 웹가입 8명은 줄 수정, 2명 신규 등록 · '가입대기' 시트 신설(적어두면 가입 즉시 수강생 자동 전환 · 완료) · 화요일 저녁 닫힘 원인(월세 입금 알림)·금요일 알림 해제(완료) — 미결: 11/4 13:30~18:00 은행 일정도 무시할지 루크 확인 (11/2 등록 3건, 완료 2건 제외)</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea04810f9bc9ca630c8766bd"><div class="t">가을 대표님 계약서 검토(11/3 클로드 페이지 /gaeul-contract/) 후속 P0 6건(모두 11/7) — 출연 RS 20%를 루크 동의 없이 변경 못하게 별도 계약 명시 · 파트너십 계약서에 8% 조항 확인 · 인터뷰 채널 출연 RS 20%가 누구 몫인지 · 가을 6:루크 4 약정의 법적 형태 · 3층을 코칭 용역계약으로 전환 · RS 20%가 10/31 합의에 없던 점 업체 확인</div><div class="m">11/3 채팅 '가을 대표님 계약서 검토' → 노션 P0 6건(11/3 등록) · 합의에 없던 두 줄(출연 RS 20% · 11.76% 수수료 고정)이 65명 기준 5,022만 — 루크 603만·가을 904만·업체 1,507만 손해 · [결정] 3건(제한 조항 수용 · 8%는 광고비 계상 · 광고 문구 보증 제외 요청 안 함) · [보류] 2건(최소 보장 강사료 · 8% 재원)</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea04813dbf55c9361384d165"><div class="t">자동소싱 결과의 상품 주소값·수량별 주소 번호 오류 수정 — 2주차(11/9~15) 자동등록 연동·작업지시서 안내 전(11/9, 추정)</div><div class="m">플라우드 11/3 강의(179분)에서 강사가 주소값 처리 부분 확인·수정 약속(11/4 등록) · 같은 강의: 제목 수량 옵션 자동 생성 기능은 아직 없음 · 등록 비용 건당 170원</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea04815e9d9efd7107fd5765"><div class="t">300억 엑시트(11/4 클로드 페이지 /exit300/) P0 3건 — 수강생 → 활성 셀러 전환율 실측(11/9) · 모든 수취 주체를 힐링디어스 법인으로 전환(11/30) · 메이븐·디노와 주주간계약 체결(11/30)</div><div class="m">11/4 노션 4건(11/4 등록, 목표 칸 비어 있음) · 2년째 법인 매출이 거의 없음 — 인수자는 법인의 반복 가능한 수익을 삼 · 전환율이 300억 가능 여부를 가르는 지표(풀 5,400명 기준 37%면 288억, 10%면 78억 — 가정값) · 베스팅 4년+1년 클리프 전원 적용, 변호사 작성 · 세무사 확인 필요</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea0481349764f9495f286239"><span class="tag cash">현금</span><div class="t">11/4 등록 코칭·자료실 P0 5건 — 6기 수강생 두 분 후속(코칭 시간 회신·주문 처리·옵션 변경 실습, 11/8) · 디노 원크루 자료실 첫 배포(onecrew-dino 저장소·Pages, 11/8 진행 중) · 최은봉 9회차 교육자료 맥 배포(11/8 진행 중 — 10/29 항목과 중복) · 이○○ 대표님 집중 코칭 11/6 14:15 세션(진행 중) · 박태경 대표 강의 런칭 제안 가부 회신 대기(11/9 진행 중)</div><div class="m">11/4 클로드 채팅들이 등록(11/4 등록) · 수강생 이름·개인 사정은 대시보드에 안 씀</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea0481e28405e87c48dd19f4"><div class="t">공유용 페이지를 별도 저장소로 분리할지 결정(11/9) — luke-1b가 public이라 build.py 소스·커밋 히스토리가 열려 있음 · 선택지: private 전환(Pages는 Pro) / 공유용 별도 저장소 / 그대로</div><div class="m">11/4 채팅 '깃허브 페이지 보안'(11/4 등록) · 페이지 자체는 page_shared()로 백링크·내부 링크를 제거했으나 소스는 열려 있음</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea048159912df03bc6653048"><span class="tag cash">현금</span><div class="t">가을 대표님 3주 코칭(신청 47명 → 2명) — 후보 3명 연락처·참여 각오 전달(11/5 · 11/4 약속) → 가을 대표님이 2명 선정 · 코칭 진행 가이드(평일 5일·하루 2시간·3주, 어려운 CS는 확인 후 응답) 정리·전달(11/9, 추정)</div><div class="m">플라우드 11/4 '[OneCrew] 정복녀 대표님 찐초보 7기'(58분) 상담자(루크) Action Item(11/5 등록) · 프로필 사진은 전문 촬영(60~100만) 대신 스마트폰 촬영 → 루크 AI 보정, 사진 11/8까지 — 기존 '프로필 사진 촬영·메이크업 예약'(11/10) 계획 변경 · 코칭 사례는 유튜브 출연에 활용</div></li>
    <li data-n="https://app.notion.com/p/40f0cf8fea0481369c55f7c075d8de74"><span class="tag cash">현금</span><div class="t">강의업체 이전(11/5 박○○ 대표님 미팅 → 노션 [결정] 루크·메이브님 현 강의업체 강의 해지, 메이브님은 11월 강의 마지막) — 메이브님과 통화: 박○○ 대표님 새 수익 모델 설명·상의, 내년 초 진행 여부 합의(11/8)</div><div class="m">11/5 채팅 등록 4건 중 P0 · 루크는 박○○ 대표님 쪽으로 거의 기운 상태(노션 메모) · 신규 플랫폼은 사이트 구축·심사 약 3주, 1월 진행 안은 조율 중 (11/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/40f0cf8fea0481c9817dc1d41e3aef99"><span class="tag cash">현금</span><div class="t">토요일(11/7) 상담 통화 — 개선 의지 확인 후 상담 진행 여부 결정 (의지 있으면 이어가고, 없으면 위로 위주로 마무리)</div><div class="m">메이브님이 공유해 준 상담 희망자 · 프로젝트 '상담' (11/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/40f0cf8fea0481d1b4b2edbafe526e6d"><div class="t">자동등록 테스트판 2건 — v237 소싱 엑셀을 그대로 붙여넣어 올리기 · v239 등록 현황 달력·하루 목표 + 점검 접기 (P0 진행 중, 기한 없음)</div><div class="m">11/5 클로드 코드 등록 · 같은 날 창고 사서함·재고 관리(/warehouse)는 P 없음 — 허브 툴박스 줄에 (11/5 등록)</div></li>
__NEW_P0__
  </ul>
</div>

<h2>P1 · 이달 <small>~11/30</small></h2>
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
    <li data-n="https://app.notion.com/p/3ea0cf8fea0481969503d67f972a91e1"><span class="tag cash">현금</span><div class="t">수강생 전체 공지·교육자료 — 화장품 2차 포장(단상자)·표시사항 유지, 도매처 검증 체크리스트</div><div class="m">기한 9/30 지남</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea048121be35ee82635e54a4"><span class="tag cash">현금</span><div class="t">교육회사(셀러들의 수다)+3PL 법인 — 신규 설립 vs 힐링디어스 변경 결정</div><div class="m">기한 10/31</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea04810b808df66fdd4ed562"><div class="t">키티티 원장님 — /admin 노트 사용법 전달·시술 방향 피드백 + /guide 내용 피드백 받기</div><div class="m">둘 다 기한 10/9</div></li>
    <li data-n="https://app.notion.com/p/3ed0cf8fea0481b19467f1586979d14c"><div class="t">API 캐시 자동 충전 설정 — 잔액 8,000원 미만이면 8,000원 충전</div><div class="m">플라우드 10/2 멘토링 Action Item · 기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea0481388f9cc6a8fd0cd7db"><span class="tag cash">현금</span><div class="t">키티티 AI 뷰티 플랫폼 — 협력 계약서 초안 · 홈페이지 파트너샵용 템플릿 · 파트너 의향서 양식(3곳)·의향 샵 10곳 모집 · 개발비·유지비 구조 재검토 · 업종 추가 세무사 확인 · 초창패 자부담 마련 계획 · 원장 자격·수상 목록 · 웨딩·이벤트 패키지 연결 · 헤메네일→진단 링크</div><div class="m">모두 기한 10/31 · <a href="../reports/kititi-win-plan/?v=1">초창패 승부수 보고서</a> (10/4 등록 10건)</div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea0481dfa1b6d552232ecaa9"><div class="t">루크 툴박스 자동 메시지(알림톡·문자) 연동</div><div class="m">기한 없음 · 루크 할 일 3개: 카카오톡 채널+비즈니스 인증 · 솔라피 가입+발신번호 등록 · API 키 전달 (10/4 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea04811598d8f4ff3c654f8f"><span class="tag cash">현금</span><div class="t">[결정 필요] 헤메네일 광고 금액 확정 — 프리미엄·플러스·루키</div><div class="m">기한 없음 · 10/5 방침: 광고비로 순위가 움직이는 구조, 1차 구현·배포 완료 · 제안 금액: 프리미엄 49,000원/주 · 플러스 19,000원/주 · 루키(개업 1년 이내) 9,000원/2주 (10/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea04818e91f2fb85f0445a89"><div class="t">[결정 필요] 헤메네일 추가 공공데이터 — 인허가 일간 API로 폐업 자동 반영 + 사업자 상태조회로 사장님 확인</div><div class="m">기한 없음 · 둘 다 data.go.kr 활용신청 필요(루크 허락 시 클로드가 신청) (10/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea04812f81c6f8f751221178"><div class="t">키티티 헤메네일 업종 정정 요청(주력 메이크업) + 가격표·네이버 예약 주소 올리기</div><div class="m">기한 없음 · 상호에 '메이크업'이 없어 업종 '모름'으로 분류됨 → 매장 상세 맨 아래 '업종 정보 정정 요청' (10/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f00cf8fea04818a937efb1274c10b22"><div class="t">키티티 AI 상담 — GPT 연결용 OpenAI API 키 발급(루크) · 원장님께 상담 정책 10가지 답 받기 · 원장님 답 채우기(주차·예약금·취소 규정·소요 시간) + 카카오 채널·톡톡에 주소 연결</div><div class="m">기한 없음 · 답은 /admin-chat '원장님이 알려주는 답'에 입력 (10/5 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea048144b71af1d096a2f0a2"><div class="t">루크 툴박스 — 자동화 도구 구매 검토 결과 확인 + 루크 결정(환불 기준·설치 대수·윈도우/맥·네이버 계정 처리·결제 방식) · 원크루 페이지 결정 5가지 + 루크 사진·영상 전달</div><div class="m">기한 없음 · 원크루 페이지 1단계 개선은 10/5 배포 완료 (10/5 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048167bc15f5dc0646b939"><span class="tag cash">현금</span><div class="t">초월스토리 — 파일럿 강사 후보 소개(10/20) · [결정 필요] 상품 최종 확정(10/22) · 전환율 가정 검증·광고비 상한(10/24) · 협업 모델 옵션·배분 초안 확정(10/29 지남) · 런칭용 성과자 섭외(10/31)</div><div class="m">과거 전환율 3%와 목표 10% 사이 (10/6 등록 5건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048109be61c95277b4895a"><span class="tag cash">현금</span><div class="t">메이븐 스토어·3PL — 매출 우수 상품 링크 받아 추가 판매 전략 세팅(루크) · 재고 못 판 수강생 상품 위탁판매+판매 일지(메이브님) · 물동량 일 200건·월 6,000건 확대 → 택배비 재협상(메이브님)</div><div class="m">기한 10/31 (10/6 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048137bd9ac4df5325f1d0"><span class="tag cash">현금</span><div class="t">인베이더 종료 대비 — 졸업 후 반복 매출 가격안(프로그램 월 구독 + 3PL 등급) · 6기·4기 수강생 성과·후기·비포애프터 수집 · '사입으로 수익 낸 사례' 특강 정기 개최</div><div class="m">기한 10/31 (10/6 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea04818d8bc4e8dd106ecd1c"><div class="t">법인 정리 — 공고방법을 홈페이지 게재로 변경(10/15) · 지분을 주식 양도로 줄지 증자로 줄지 결정 · 창고형 매장 후보지 과밀억제권역 확인 · 3PL 창고 취득세 중과 제외 업종 확인 · 꼬마빌딩 지역·시점·명의 · 힐링디어스로 받을 매출 하나 정하기 · 법인 서류 클라우드 폴더 · 주소 박힌 것 전부 교체</div><div class="m">나머지 기한 10/31 · <a href="../corp/">힐링디어스 → 셀러들의 수다</a> (10/7 등록 8건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048113a3d7c503eec00deb"><span class="tag cash">현금</span><div class="t">창고형 매장 우리 재고로 4주 시범 판매 · 주간 매출·판매율 기록</div><div class="m">기한 11/8 (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea0481a78df0ec77cc00af96"><span class="tag cash">현금</span><div class="t">지영 원장 빌드업 페이지 — 숫자 받기(매출·순이익·본인 몫, 객단가·예약 건수·재방문율·시술별 비중 등) · 새 저장소 kittiti-jiyoung 생성 + Pages 켜기</div><div class="m">기한 10/31 · <a href="../jiyoung-prompt/">프롬프트</a> (10/7 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea04819d9fa9e130cdaba0fc"><div class="t">루크 툴박스 검색·AI 요약 정리 후속 — 채널 주소 전달과 '미니쏜' 정체 확인</div><div class="m">기한 없음 (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f30cf8fea04813d8880ee10ef500869"><span class="tag cash">현금</span><div class="t">초월스토리 — PG 수수료 요율과 실제 광고비 비율 숫자 확보</div><div class="m">기한 10/31 · 둘만 들어오면 배분표가 하나로 확정 · 지금은 PG 3.5% 가정·광고비 세 시나리오로 계산해 둠 (10/8 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea0481c99265f4b17f2ddc0c"><div class="t">법인 등기 뒤 — 등기 끝난 뒤 할 일 10가지(사업자등록 정정·법인인감 재제작·사무실에 상호 통지·통신판매업 변경신고) · 법인 지방세 체납 여부 확인(위택스 납세증명서 발급 시도) · 비상주 사무실 계약 조항 3개 대응(우편물 폐기·말소 위임·만료일)</div><div class="m">앞 둘은 기한 10/31, 사무실 계약 조항은 기한 없음 · 체납이 있어도 이번 등기에는 지장 없음(노션 메모) (10/9 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea048178bbbbeb6b52524035"><div class="t">박종혁 본부장 사무실 좌석 마련 + 온보딩 지원 · 유튜브 콘텐츠 전략 재구성(수강생 성장 스토리 + 전문가 인사이트, 본부장과 공동)</div><div class="m">플라우드 10/9 회의 Action Item · 기한 10/19·10/31은 추정 — 확인 필요 (10/10 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f60cf8fea04815a9680e74e11816ed0"><div class="t">키티티 상담 사이트 — 구글 서치 콘솔·네이버 서치어드바이저 등록 + 플레이스·인스타·블로그에 새 주소 넣기</div><div class="m">기한 없음 · 검색 준비물(로봇 안내·사이트 지도·대표 주소)은 10/11 완료 · 구글·네이버 로그인 필요 (10/11 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f60cf8fea0481268d1cf30e554b0457"><div class="t">키티티 상담 사이트(10/11 원장님 피드백) — 웨딩 페이지에서 교육·수강 정보 빼고 문구 다시 쓰기 · AI 가상 메이크업을 '가상 체험' 안내 + 스타일 표본 선택 방식으로 재설계</div><div class="m">플라우드 10/11 녹음 Action Item · 기한 10/31은 추정 — 확인 필요 · 속도는 늦추기로 함 (10/12 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f80cf8fea0481c99e8bea69a1f28e02"><div class="t">일십백천 새 강의실 — 영상이 잘못 연결된 강의 5편의 올바른 유튜브 주소 알려주기</div><div class="m">기한 없음 · 쿠팡 5-1~5-3(전부 8주차 6-2 영상) · 알리 3-8(쿠팡 6-1 영상) · 최적화 1-3(9주차 1-3 영상) — 지금은 '준비 중' 표시 (10/13 등록)</div></li>
    <li data-n="https://app.notion.com/p/3fb0cf8fea048166b25ffd0e07213cf4"><span class="tag cash">현금</span><div class="t">지영 서포트 운영 — 첫 '결정 묶음' 세션 10/26(일) 15분(① 촬영 작가 ② 임대 특약 서명 ③ 상표 대행 선택) · 상표 출원 대행 견적 2곳 + '키티티바이지영' 지정상품 초안(10/29 → 11/1 P0 진행 중 · <a href="../trademark/">설계안 v2</a>) · 사진 재촬영 컨셉보드 1장 + 작가 후보 3명 견적(10/29 지남)</div><div class="m">결정 3개는 각각 선택지 2개 + 추천 1개 형태로 준비 · '생각해 볼게'도 답으로 인정 (10/16 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3fb0cf8fea048152bc00c4d7dc4e172e"><span class="tag cash">현금</span><div class="t">키티티 토탈샵 계약 후속 — 3층 창문 처리 인테리어 협의 후 임대인에 서면 전달(11/15, 누수 책임 갈림) · 12/31 잔금일 현금 준비(권리금·보증금 잔금 + 중개수수료)</div><div class="m">10/8 임대차·권리양수도 계약 녹음에서 나온 미결 건 · 같은 녹음의 다른 미결: 시설 인수·반출 품목 합의서 · 기존 사업자 폐업신고→신규 영업신고 · 업종 변경 신고 필요 여부 · 금액은 공개 페이지에 싣지 않음 (10/16 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3fc0cf8fea0481e696f8cfa6d15a2f9c"><div class="t">원크루 심화 자료 12편 게시 완료(10/17, 회원 전용) → 예로 든 숫자 다섯 군데 루크 확인 — 심화 10 한 달 남는 돈 400만 · 심화 12 석 달 300만→한 해 2,000만 계단 · 심화 07 묶음 값 셈 · 심화 09 조건 하나당 깎이는 폭 · 심화 06 손절 선(30일 3할·60일 반)</div><div class="m">기한 없음 · 지금은 모두 '예로 든 숫자'로 표시 · 비회원 화면에는 제목 없이 편수만 보임, 공개 자료 31편은 그대로 (10/17 등록)</div></li>
    <li data-n="https://app.notion.com/p/3fd0cf8fea0481309185f76381e70360"><span class="tag cash">현금</span><div class="t">키티티 토탈샵 11월 준비 — 네일 오픈샵 세트 비교표(10/31) · 브랜딩 초안 묶음(명함·로고 3안·간판 견적 2곳·층별 플레이리스트, 11/15) · 인테리어 업체 3~4곳 상담+실측 일정(11/15) · 에스테틱·베드 기기 조사(11/15) · 페르소나 홍보 콘텐츠 기획(11/15) · 주말 발품 헤어→네일→에스테틱(11/22) · 전원 직원 손익 버전 · 초기 투자 재계산 · 직원 급여 기준(11/30)</div><div class="m">10/18 녹음 근거 · 인테리어·기기·콘텐츠 3건은 플라우드 Action Item으로 노션에 새로 등록, 기한 11/15는 추정 · 에스테틱은 경락·핸드 중심 소규모(베드 2대 먼저) · 보증금·권리금 금액은 싣지 않음 (10/18 등록 9건)</div></li>
    <li data-n="https://app.notion.com/p/3fd0cf8fea0481dc9032d820cee0d030"><div class="t">원크루 영업 자료(공개 32번 + 심화 13·14편, 10/18 게시) — 예로 든 숫자 다섯 군데 루크 확인(한 주 목표 150만 · 비는 주 10→2주 · 열 명에게 걸면 세 건·두 건 · 첫 줄 바꿔 한 명→네 명 · 석 달이면 다시 걸 사람 48명)</div><div class="m">기한 없음 · 지금은 모두 '예로 든 숫자'로 표시 · 담당 미기재 (10/18 등록)</div></li>
    <li data-n="https://app.notion.com/p/3fe0cf8fea0481e7af2fea3058e97c61"><div class="t">고려대 거울 광고 2칸 — 카피·칸 구성 확정(기본값 A좌+B우, 위치 미확인 시 F) + 고대 거울 전용 QR 링크</div><div class="m">진행 중 · 기한 없음 · 확인 필요: 거울 설치 건물·층·성별, 이전 후 보문역 도보 시간, 광고 단가, 인스타 핸들 고정 여부 · 다음: 위치 확인 → 카피 확정 → QR 전용 주소 → 디자인 파일 · <a href="../mirror-ad/">시안 페이지</a> (10/19 등록)</div></li>
    <li data-n="https://app.notion.com/p/4000cf8fea0481adaadcc68d440bc3a3"><div class="t">민트(박종혁) 계약 묶음 — 10/21 미팅: 계약서 초안 일곱 칸 채우기 · 과거 CAC 확정(3,000원 vs 6,000원) · 카페·유튜브·광고계정 법인 명의로 개설 · 요약본·입력 폼(/park-terms/) 발송 → 네 가지(주소·생년월일·연락처·계좌) 회신 10/23 → 변호사 검토(근로자성 — 주 4일 출근 + 고정 좌석 + 월 고정급) → 최종본 서명 · 용역비 1회차 11/20</div><div class="m">10/21 노션 12건(완료 [결정] 2건 포함: 활동명 '민트' · 10/21 근무 시작 · 1차 계약기간 2027-01-20까지 / 수익 배분 민트 6:루크 4 · 배분 기준액 = 매출 − PG 수수료 − 광고비 − 외주비(B안)) · 1차 계약서는 17개 조 + 별지(60명 기준 계산 예시) 완성, 남은 빈칸은 민트님 인적 사항 넷 · 개방 항목(커머스 세부품목·오프라인·역직구·PD 채용 주체·4개월차 이후)은 제16조 별도 합의로 유예 · 지메일 커넥터를 연결하면 회신 메일을 클로드가 바로 반영 가능(검토 항목) · 급여·단가 숫자는 노션 메모에만 · <a href="../park-contract/">1차 계약서</a> · <a href="../park-terms/">협업 조건(발송용)</a> (10/21 등록 12건)</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea04816ab986e866e792a04a"><div class="t">메이븐(메이브님) 정산 — 12월 정산 1,800만 확정 여부를 언제까지 정할지(10/31) · 5기 정산이 1월인지 2월인지 확인(11/30) · 인베이더 없이 메이븐 기수를 돌릴 수 있는지 판단(11/30)</div><div class="m">10/23 [결정] 메이븐 5기 12/20 강의 · 앞으로 격달 2,000만 정산(연 1.2억, 바닥 수입) · 11·12월 각 1,800만은 가정값이고 실제 수령은 10월분뿐 — 12월분이 빠지면 11~1월 순현금 2,380만 → 580만 · 10/23 민트님 협의 녹음: 인베이더 의장 상품 중심 전환 언급·그만둘 소문, 메이븐 기수 수익은 인베이더와 5:5 (10/23 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea04818eafb8ed52a94114a4"><div class="t">민트(박종혁) 협업 10/23 회의 후속 — 배분 루크 40%인가 24%인가(정현님 몫, 10/31) · 계약서 제8·9조 수정(외주 한도 700~800만 · 런칭일 2027-01-20, 10/30) · 1월 강의 객단가 확정(10/30) · 3,000만 예산 구성 — 용역비 900만 포함 여부(10/30) · 10/30 영상팀 세팅 미팅 안건·참석자(10/30) · 광고 3,000만은 11/20 모집 결과 보고 분할(11/6) · 주간 정기 회의 매주 수, 첫 회 10/28 — 10/30 미팅은 진행(플라우드 112분)됐으나 결정 기록 없음, 10/30 기한 4건 지남 · 노션 미완료</div><div class="m">10/23 민트·다마고치 기획 회의(플라우드 22분) + [결정] 배분 네 건(민트 건 민트 60%·루크 24%·메이븐 16%) · 라이브 마지노선 2027-01-20(설 연휴 전 소비력 저하 회피) · 모집 영상 촬영 11/5 → 광고 11/6~11/20 → 첫 본편 촬영 11/30 → 첫 업로드 12/5 → 최종편 1/15 · 미결: 채널(셀러들의 수다 vs 개인 vs 신규)·콘티 A/B/C안·총 편수 7~8편·광고비 배분 — 채널·편수는 11/4 결론(셀수다 본진+스스로 월백 공동작업자 · 본편 5+모집 1), 주간 정기 회의 항목 완료 처리 · <a href="../oct23/">10월 23일 세 대화</a> (10/23~10/24 등록 7건)</div></li>
    <li data-n="https://app.notion.com/p/4020cf8fea0481688c9ad00d51fb263f"><div class="t">초월스토리 가을 대표님 — 정산액 6:4 어느 쪽이 6인지(10/31 · 같은 날 [결정]에서 가을 6:루크 4로 확정, 노션 항목은 미완료) · 손익분기 18명 사전 고지, 촬영 전에(11/5) · 11월 첫째 주 촬영 일정 확정 + 콘셉트·스크립트·자료 공동 기획(11/1)</div><div class="m">루크 = 전체 매출 8% + 가을님 정산액의 4 · 1억 매출 기준 루크 1,634만 · 8%의 기준이 전체 매출인지 PG 제외인지 남음 · 광고 4,500만 선회수 구조라 18명 아래면 가을님 몫 0원인데 루크 8%는 그 구간에도 나오니 촬영 전 직접 설명 · 10/23 7기 세션(플라우드 45분) 타임라인: 11월 첫째 주 촬영 → 12월 본 강의 → 1월 정산 (10/23~10/24 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/4030cf8fea04810aa183f4321102b969"><span class="tag cash">현금</span><div class="t">키티티 토탈샵 — 주간 촬영 출장 메이크업 계약(엑셀 방송 대표) 조건 문서화(10/31) · 헤어팀 보상안·2인 배치 손익 시뮬레이션(10/31)</div><div class="m">10/24 아침 플라우드 메모(72초, 루크 혼자) → 노션 새 항목 2건, 기한 10/31은 추정 · 촬영: 매주 금요일, 남양주 또는 파주, 여2·남2 — 출장비 면제·업스타일 제외·정가 청구로 제안, 정가 기준표·추가 요청 과금·이동 대기 시간 처리는 확인 필요 · 보상안: 기본급 + 월 매출 기준선 초과분부터 인세 — 급여·기준선 숫자는 노션 메모에만 · 10/18 [결정] 인력 구조(직원 4 + 실장 2 정률)와 정합성 확인 (10/25 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/4040cf8fea0481659c16d859e5a5cc04"><div class="t">테라피님 CS 응대 템플릿(반품·환불·항의) 제작·전달(10/31) — 다른 수강생 공용 템플릿으로 확장 가능</div><div class="m">10/23 코칭 Action Item · 10/24 플라우드로 만든 'CS 템플릿·프로그램 원격 세팅 지원'(10/31) 항목과 같은 일이 채팅에서 따로 등록됨 — 한쪽 정리 필요 · 같은 날 클로드 코드가 공용 'CS 답변 템플릿 24가지(위탁·사입)'를 발행(완료) → 루크 문구 검토 항목은 P 없음 (10/25 등록)</div></li>
    <li data-n="https://app.notion.com/p/4050cf8fea0481e1bd2fc390bea0769f"><div class="t">키티티 40×10cm 배너 제작 — 프롬프트①로 인물·배경 생성 → 캔바에서 텍스트·QR 2개 올려 인쇄 입고(10/31 · 진행 중)</div><div class="m">10/26 20:07 스타일 합격 · 미세 조정: 상호 위로, TOTAL BEAUTY 크게, '메이크업 & 헤어스타일링 전문' 타이틀 위 아이브로우로, 하단 바 80% 반투명 블랙, 대표원장 문구 서체 고급화·확대, 시술 5종 개별 골드 아이콘 · 남은 작업 ① 재생성 ② 4:1 확인 ③ QR 스캔 테스트 ④ 4724px 업스케일 ⑤ CMYK PDF 입고 · 고대생 첫방문 20% 혜택 담은 리블링 스타일 1종 (10/26 등록)</div></li>
    <li data-n="https://app.notion.com/p/4070cf8fea0481df9fc3f305e2ea4edb"><span class="tag cash">현금</span><div class="t">초월스토리 가을님 10/28 세션 후속 3건 — 초월스토리 PD와 촬영 장소(가을님 지역 vs 서울 근교)·첫 회차 동행·현장 피드백 계획 + 채널 분산 전략(인베이더 외 채널 병행·기간 분리) 확정(11/5) · 프로필 사진 촬영·메이크업 예약(협력사, 비용은 론칭 후 정산) + 라이브 촬영일 동선(11/10) · 매출 목표 1억 로드맵 문서화(11/10)</div><div class="m">플라우드 10/28 정복녀 7기 Action Item(루크·초월스토리 PD 공동) · 11월부터 강의 준비 착수, 시리즈물 기획 · 장소 선택 기준(접근성·촬영 환경·인력 배치)과 라이브 당일 타임테이블은 미정 · 가을님은 콘텐츠 수행에 집중, 운영·세팅은 지원팀 · 1억은 목표값(실적 아님) (10/29 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/4070cf8fea0481df9ec9fcdaee1cac2c"><div class="t">최은봉 대표님 회사소개서 초안 검토 → 개선안(복수 안) 작성·피드백 — 초안 수령 후(11/4, 추정)</div><div class="m">플라우드 10/28 최은봉 세션 Action Item(기한 TBD → 다음 세션 전으로 추정) · 파트너·공급사 협업용, AI 도구로 버전별 제안 · 초안 송부는 대표님 몫 (10/29 등록)</div></li>
    <li data-n="https://app.notion.com/p/4090cf8fea0481f38d3fc3dbc35a50f9"><div class="t">신규 수강생 한 분 환영 메시지 발송(10/31) — 첫 주 이탈 방지, 첫 주문까지 질문하며 따라오게</div><div class="m">10/30 채팅 '신규 수강생 환영 메시지' · 환영 메시지 초안 2종 작성됨 → 발송 후 완료 처리 (10/31 등록)</div></li>
    <li data-n="https://app.notion.com/p/40a0cf8fea048197acbde514d247a0c7"><span class="tag cash">현금</span><div class="t">초월스토리 10/31 회의 후속 P1 — 카톡·줌 소통 채널+응대 SLA(11/7) · 사무실·3PL 현장 촬영 허가 규정(11/7) · 매출 인증·수강생 성과 증빙 취합(11/10) · 가을 대표님 스토리 콘텐츠 반영 범위 본인 확인+인터뷰 설계(11/10) · 4주 커리큘럼 표준화+6주 변형안+주간 숙제 제도(11/10) · 뷰셀님 12월 강의 일정 공동 진행 여부(11/14, '뷰셀링' 표기 확인 필요) · 무료 강의 공지·앵콜 라이브 2회·줌 세션 계획(11/15) · 무료 혜택용 전자책(11/15) · 대리등록 범위 산정 → 심화반 패키지(11/15)</div><div class="m">플라우드 10/31 '10-31 회의' Action Item, 기한은 모두 추정 · 촬영 11월 둘째 주(1회 방문 다회차) · 유튜브 출연 수강생 2명(40대 이상 여성)·라이브 출연 2명 설문 선발(11/4)은 기존 '성과자 섭외' 항목과 같아 새로 만들지 않음 · 리드 즉시 콜링·블로그/카페/스레드·모객 영상 제작은 초월스토리 측 몫 · 가을 대표님 개인 사정은 본인 동의 범위 안에서만 (11/1 등록 9건)</div></li>
    <li data-n="https://app.notion.com/p/40a0cf8fea04811a9a21dc900e572736"><div class="t">수강생 프로그램·3PL 운영 표준(10/31 회의) — 프로그램 3종(소싱·자동등록·가격관리) 계정 권한 세팅·안정화 + 사용 매뉴얼 · AI 실비(건당 150~300원) · 가격 변경 1시간 주기 정책 공지(11/15) · 3PL 위탁·사입 운영 프로세스 표준화(주문서 연동·발송 SLA)+사입 전환 온보딩 가이드(11/30) · 수강생 재고 처리 지원 프로세스(공구·교환·오프라인·매입) 문서화(11/30) · 스마트스토어 카탈로그 자동 매칭 운영+베스트 소싱 매뉴얼(11/30)</div><div class="m">플라우드 10/31 '10-31 회의' Action Item(운영·IT·물류), 기한은 추정 · 프로그램은 기본 무상, 자동등록의 Gemini 비용만 외부 실비 · 가격관리는 네이버 차단 방지로 1시간 간격 일괄 변경 기본 · 사입·3PL 창고 발송은 위탁 대비 주문 처리 1~2분 단축 · 미결: 주문 급증 시 처리 용량·오류율·비상 절차 (11/1 등록 4건)</div></li>
    <li data-n="https://app.notion.com/p/40c0cf8fea04813c8e69ea1de97a5ca2"><div class="t">돈벌쥐 PD 공동 프로젝트 11/2 클로드 페이지(/pd/·/pd-long/) 후속 6건 — 통화 전 준비 4건(1/20 라이브 가능 여부 확인 · 16시 통화 보상 3층 구조 제안 · 민트님께 배분 전 비용 차감 사전 고지 · 장기 비율 확정 보류) + [검토] 채널 수익 4분할(애드센스 PD 100%·협찬 50:50·강의 구간 정액) — 5건 모두 11/2 지남·노션 시작 전 — 11/11 PD 보상 의결(순수익 15%)로 배분 전 고지·장기 비율 보류 2건 완료 · '0원 다마고치' 채널 법인(힐링디어스) 명의 개설(11/18)</div><div class="m">11/2 클로드 대화 2건(채널 운영 비용 산정 · 장기 파트너십 설계): 1층 편당 70만×월 4편 · 2층 런칭 매출 구간별 정액 · 3층 장기는 채널 자체 수익만 비율, PD 보상은 배분 전 비용 차감 · 통화는 11/2 17:47 진행(플라우드 44분) — 끝난 것은 완료 처리하면 빠짐 · <a href="../pd/">장기 파트너십 설계</a> · <a href="../pd-long/">비용 산정</a> (11/2 등록 6건)</div></li>
    <li data-n="https://app.notion.com/p/40c0cf8fea048172a9d9ffbd1ab3c8a8"><div class="t">돈벌쥐 PD 11/2 통화 후속 P1 3건 — 이전 대행사 성과 저조 영상 링크 PD께 전달(11/4) · 다음 주 화/수(11/10·11/11) 저녁 대면 식사 미팅 일정 확정·민트님 동석 여부(11/6) · 개인 채널 퍼스널 브랜딩 운영 니즈 문서화 → 대행 패키지·견적(11/14) — 기한 모두 추정</div><div class="m">PD 제안: '유믿음' 인물을 먼저 각인 → 전문성 · 보상은 채널 수익 쉐어 vs 월 단위 대행 중 하이브리드 선호 · 순서: 신규 프로젝트 안정화 → PD '여자들의 수다' 첫 화(13일 촬영) → 개인 채널 논의 (11/3 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea0481c3bc2ac5f7ef96b41e"><div class="t">가을 계약서 후속 P1 2건 — 11.76% 결제 수수료 산출 근거 요율표 요청(11/10) · 기수 광고·운영비 상한을 운영자 자격으로 요구(11/30)</div><div class="m">11/3 채팅 '가을 대표님 계약서 검토'(11/3 등록) · 매출 1.7억이면 수수료 1%p가 170만, 절반이 가을 부담 · 비용 167만마다 손익분기 1명 상승</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea0481e9a29cd3b4402bc045"><div class="t">키티티 링크 홈 내용 채우기(프로필 사진·버튼·사진) — 원장 몫, kititibyjiyoung.com/admin · 기한 없음</div><div class="m">11/3 채팅 '키티티 상담 사이트'(11/3 등록) · 리틀리형 전면 개편+관리자 편집기는 완료</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea0481459ed7c7f5b2bfe046"><span class="tag cash">현금</span><div class="t">물류 수익 배분·3PL 이용료 구체화 — 파레트 단위 등 3PL 요금 · 외부 고객 유치 보상 · 오프라인 판매 수익·회사 환원 · 성과급 구조, 물류 담당 파트너와 협의(11/30, 추정)</div><div class="m">플라우드 11/3 물류 회의 Action Item(11/4 등록) · '전부 가져가는 방안'·'최소 6'·회사와 나누는 방식이 함께 언급돼 기준 조율 필요 · 책임자급 합류 수익 쉐어 제안은 조건 협의 안 됨</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea0481579e63f7c67f256911"><div class="t">수강 신청자 사전 확인 절차 — 기존 사업 경험·현재 사업 상황·참여 목적 확인 + 초급 수업 범위·기대 수준 사전 안내(11/15, 추정)</div><div class="m">플라우드 11/3 강의 녹음 말미 논의(11/4 등록) · 경험 많은 지원자가 초급 수업에 오면 기대 수준이 어긋남</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea048163bf10d0ff3968dc36"><span class="tag cash">현금</span><div class="t">11/4 등록 코칭 P1 5건 — 심○○ 대표님 교재 PDF 전달 + 11/6 소싱 프로그램·엑셀 보충(11/6 진행 중) · 민○○ 대표님 운영 계정 확정·11/9 본격 등록 점검(11/9) · 유○○ 대표님 Claude·영상 제작 교육 일정(11/14) · 신규 수강생 2주차 코칭(11/15) · 신정현 대표님 자료실 링크 전달+13장 검토(onecrew-sjh 11/4 첫 배포, 11/11 진행 중)</div><div class="m">11/4 클로드 채팅들이 등록(11/4 등록) · 수강생 이름·개인 사정은 대시보드에 안 씀</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea0481fe9945ef1924f311f3"><div class="t">소싱 프로그램 수량별 주소값 오류 수정 + 수강생 사이트 비밀번호 변경 기능(11/13) — 주소값 건은 11/9 P0 항목과 같은 일, 한쪽 정리 · 보부상님 엑시트 상세 5가지 파악(11/30) — 본명·채널·법인, 300억이 현금인지 언아웃 포함인지, 무엇을 팔았나, 매각 시 매출·영업이익, 인수자 유형</div><div class="m">(11/4 등록) · 보부상 건은 공개 보도 검색 안 됨, 실제 배수 계산용</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea0481c6809ec28b9bbcd1b5"><span class="tag cash">현금</span><div class="t">박태경 대표 강의 런칭(플라우드 11/4 세션 108분) 3건 — 기본 틀·기획안 초안(11/30) · 협력 업체 미팅·조건 확인·선정 + 런칭 일정 12월 말~1월 구체화(11/30) · 한 달 상담 예행연습 세팅(하루 2~3시간, 신청자 47명 중 배정·주간 시간표, 11/10) — 기한 모두 추정</div><div class="m">강사가 유튜브 출연·온라인 세팅·리허설·초기 2기수까지 지원 · 같은 47명을 가을 대표님 3주 코칭과 나누는지 확인 필요 · 노션 '강의 런칭 제안 가부 회신 대기'(11/9)와 이어짐 (11/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/40e0cf8fea048192b515dd683e05d90d"><div class="t">가을 대표님 스토어 소명자료 검토 — 문구 말투('구입·배송 내역이 존재하지 않습니다' 등)·인사말·개인정보 동의 체크 확인 후 제출(11/7, 추정)</div><div class="m">플라우드 11/4 정복녀 세션 Action Item — 제출 기한은 요약에 없음 (11/5 등록)</div></li>
    <li data-n="https://app.notion.com/p/40f0cf8fea0481fc9909c08ab0b45dd8"><span class="tag cash">현금</span><div class="t">돈벌쥐 PD 연결 에이전시 미팅 잡기 — 박○○ 대표님 안과 조건 비교, 더 나은 쪽 선택 · 괜찮으면 그 에이전시엔 신규 강사 연결 검토(11/30)</div><div class="m">11/5 채팅 '강의업체 이전' · 관계 쌓기만으로도 의미 있음(노션 메모) (11/5 등록)</div></li>
__NEW_P1__
  </ul>
</div>

<h2>P2 · 다음 달 말</h2>
<div class="card">
  <ul class="list tasks">
    <li><div class="t">사진 기반 입고/검수 자동화 (설계 10/8 → 프로토타입 10/15)</div></li>
    <li><div class="t">물류 권한 재설계·감사 로그 · 선반·라벨링 · CS 스크립트</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea048126844ad335f1aefd2e"><div class="t">서울 이전·건물 매입 대비 로드맵 (내년 초)</div><div class="m">기한 11/30은 추정 · 확인 필요</div></li>
    <li><div class="t">전화 상담 AI — 100건 통화 녹음 분석 (내 목소리 엔진 연계)</div></li>
    <li data-n="https://app.notion.com/p/3ea0cf8fea0481e8bccdcb6db430eeb4"><div class="t">영상 자동화 프로그램 만들기 (지영 요청 개발건)</div><div class="m">기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea0481dd8721d7c5260db6d1"><span class="tag cash">현금</span><div class="t">트리플 루프 빈 칸 설계 — 지영 채널 자체 수익 + 실물 제품 유통 아이템</div><div class="m">기한 11/30</div></li>
    <li data-n="https://app.notion.com/p/3eb0cf8fea04817e87d2c4ec5d319b6b"><div class="t">영상공장 AI 라벨 자동 켜기 확인 (유튜브 합성 콘텐츠·인스타 AI 정보)</div><div class="m">기한 없음</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea04810e84d3e7ceb43c766d"><span class="tag cash">현금</span><div class="t">힐링디어스(주) 업력·매출 기준 2027 정부지원사업(초창패·디딤돌·도약패키지) 지원 가능 여부 확인</div><div class="m">기한 11/30 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ec0cf8fea04816eae8bcd7b7a2a9f54"><span class="tag cash">현금</span><div class="t">디노 — 1년 사업자 업종코드가 9년 사업자와 다른지 확인 + 9년 사업자 폐업 시점 검토</div><div class="m">담당 수민님 · 기한 없음 (10/1 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea0481859a20e212db58d884"><span class="tag cash">현금</span><div class="t">초창패 PSST 계획서 초안 12월 안에 완료</div><div class="m">기한 12/31 · 3개월 실측 숫자·파트너 의향서·대표자 자격 증빙 반영 (10/4 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ee0cf8fea048171ad3ef13b0f780e44"><div class="t">헤메네일 — [결정 필요] 카카오 로컬 API로 추천 1~3위 업종 실시간 대조(표시만 vs 순위 반영)</div><div class="m">기한 11/30 · 함께 묶였던 '영업 확인 목록 월간 갱신'은 10/5 예약 작업으로 자동화돼 완료 (10/4 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048148b8a6eb95f9649d5d"><span class="tag cash">현금</span><div class="t">서울 이전 — 후보 빌딩·공동 투자자 정보 수집, 이전할지 미룰지 먼저 결정</div><div class="m">기한 11/30 · 계약 판단은 반복 매출 확인 후 (10/6 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea04819e984acdd675ae57bb"><span class="tag cash">현금</span><div class="t">1인 사업자용 블로그·카톡 자동화 구독 사이트 기획</div><div class="m">기한 11/30 (10/6 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481188729f52df28c4e34"><div class="t">쿠팡 가격 비교 프로그램 — 개발 전 크롤링 정책 위험 검토</div><div class="m">기한 11/30 (10/6 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea04811aa006c92f5797461a"><span class="tag cash">현금</span><div class="t">메이븐 스토어 4분기 순수익 월 1,000만</div><div class="m">담당 메이브님 · 기한 12/31 · 진행 중 (10/6 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481789832f2fffe8102c8"><div class="t">답변 웹페이지 발행 위치를 깃허브에서 원하는 위치로 바꾸기</div><div class="m">기한 11/30 (10/6 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea04819f838bcf83d9a08e94"><div class="t">서울 꼬마빌딩 취득·잔금은 2027-03-16(설립 5년 충족일) 이후로 — 용도로는 중과를 못 피함</div><div class="m">기한 2027-03-16 (10/7 등록 2건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea048140bac9e2248d943be0"><span class="tag cash">현금</span><div class="t">수강생 입점 조건 문서 — 수수료 15~20%·정산 주기·보관 기간·미판매 반환</div><div class="m">기한 11/30 · 창고형 매장 시범 판매 숫자 확인 뒤 공개 (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea048176bc01e7f629aa7309"><span class="tag cash">현금</span><div class="t">꼬마빌딩 담보대출 심사 전에 대표자 신용 정리 마치기</div><div class="m">기한 2027-01-31 · 잔금은 2027-03-16 이후 · <a href="../credit/">신용점수 페이지</a> (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f20cf8fea04813098e0dc55cf5d6ecc"><div class="t">수익모델 소개 사이트 개설 (100만 챌린지·마진 키워드)</div><div class="m">기한 없음 · 일십백천과 무관한 자료 분류·제작용 프롬프트는 준비됨 (10/8 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea0481e19bced078b7db3b07"><div class="t">[결정 필요] 트리플 플라이휠 자료에 의사 선생님 이름을 밝힐지</div><div class="m">기한 없음 · 지금은 이름 없이 게시 — 밝히려면 대화·장면을 사실에 맞게 다시 써야 함 (10/9 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea04813cb438ce0216f8b59c"><div class="t">박종혁 협업 커머스 — 소싱 자동화 프로그램 테스트 + 위탁 중심 물류 운영 체계 설계</div><div class="m">플라우드 10/9 회의 Action Item(중장기) · 기한 11/30은 추정 — 확인 필요 (10/10 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f60cf8fea04812fbfd9c8c68ae275e4"><div class="t">[루크] 원크루 수익화전략 자료 속 숫자 몇 개 확인 — 02·03·06·18번 + 소개 화면 '도구' 칸에 넣을 프로그램 이름</div><div class="m">기한 없음 · 지금은 화면에 '예로 든 숫자'라고 적혀 있음 (10/11 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f80cf8fea048180b6a8fc35879b82d1"><div class="t">종소세 중간예납 고지 확인 후 납부 (개인 명의 소득 있을 때)</div><div class="m">기한 11/30 · 고지서 11월 초 발송 · 1천만 원 초과 시 분납 검토 (10/13 등록)</div></li>
    <li data-n="https://app.notion.com/p/4070cf8fea0481169f7cc8b84f35d9c8"><span class="tag cash">현금</span><div class="t">코칭 알바 한 달 뒤 수강생 4~5명 대상 라이브 출연 협의 — 1~2명 선정 목표, 불발 시 대체 시나리오(11/28)</div><div class="m">플라우드 10/28 정복녀 7기 Action Item · 라포가 형성된 수강생 중 출연자 확보 (10/29 등록)</div></li>
    <li data-n="https://app.notion.com/p/40a0cf8fea04810880f2f06d85822dfe"><div class="t">10/31 회의 후속 P2 — 리셀 윤리 가이드(타 셀러 복제 금지 등)+법적·민원(톡톡·상세페이지) 대응 템플릿 최신화(11/30) · 숏폼 등 유통 외 부업형 강의 모델 설계+추가 강사 후보군(11/30) · 50대 성과 강사(월 매출 5천 사례) 런칭 연내 추진 여부·패키지 협의(11/30)</div><div class="m">플라우드 10/31 '10-31 회의' Action Item, 기한은 추정 · 화장품 카테고리 피로도가 생기면 다른 커머스(의류·전자·생필품)·부업형으로 확장 검토 (11/1 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/40c0cf8fea048124bb2fe924cd6aded9"><div class="t">기존 구독자 1만 채널 애드센스 실적 확인 — /pd-long/ 페이지의 애드센스 월 수익(RPM 2,000~4,000원 가정)은 클로드 추정치, 실측치로 교체용 (P2, 기한 없음)</div><div class="m">11/2 채팅 '채널 운영 비용 산정' · 협찬 단가도 40대 초반 부업 카테고리면 높지 않을 수 있음 (11/2 등록)</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea04813093f4d61f93e85ee9"><div class="t">물류 담당 파트너 이사 등재 시점·권한·수익 배분 협의 — 2027년 초 본사 서울 이전·회사 신고 시점에 맞춰(2027-01-31, 추정)</div><div class="m">플라우드 11/3 물류 회의 Action Item(11/4 등록) · 기존 '내년 초 서울 이전·건물 매입 대비 사업 로드맵'(11/30)과 묶어서</div></li>
    <li data-n="https://app.notion.com/p/40f0cf8fea0481d881c2f4c25b65708b"><span class="tag cash">현금</span><div class="t">1월 신규 강의 런칭 준비 — 11월 강의 종료 후 12월 준비 기간, 1월 신규 업체에서 런칭(메이브님 담당, 12/31)</div><div class="m">11/5 채팅 '강의업체 이전' (11/5 등록)</div></li>
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
    <li data-n="https://app.notion.com/p/3ee0cf8fea0481ef8c22d7f5a93de94e"><div class="t">[공개 직전] 헤메네일 업종별 정보 페이지 테마 (헤어·메이크업·네일 별도 톤)</div><div class="m">공개 직전에 할 일 · 기한 없음 (10/3 등록)</div></li>
    <li data-n="https://app.notion.com/p/3ef0cf8fea0481bfaf94d3c15ebbf9b9"><div class="t">[공개 직전] 헤메네일 — 개인정보 보호책임자 이름·이메일 정하기 · 도메인 연결 뒤 검색 등록(구글 서치콘솔·네이버 서치어드바이저) · 카카오 링크 도메인 등록 후 '카카오톡으로 보내기' 버튼 켜기</div><div class="m">공개 직전에 할 일 · 기한 없음 (10/5 등록 3건)</div></li>
    <li data-n="https://app.notion.com/p/3f10cf8fea0481d09753d0013e1c7bd7"><span class="tag cash">현금</span><div class="t">[보류] 뿌요 파일럿 강사 기용 — 앞(강사)과 뒤(상담·운영) 자리 분리</div><div class="m">기한 없음 · <a href="../pilot/">파일럿 강사 결정</a> (10/7 등록)</div></li>
    <li data-n="https://app.notion.com/p/3f40cf8fea0481b48dedebc3ae86c46d"><div class="t">2028년 3월 중임등기 — 루크·감사 임기 만료</div><div class="m">기한 없음 · 등기부 기준 2025-03-16 중임이라 2028년 3월 전후 만료, 놓치면 과태료(500만원 이하) · 캘린더에 넣어 둘 것 (10/9 등록)</div></li>
    <li data-n="https://app.notion.com/p/40d0cf8fea0481e69828e262820d9434"><div class="t">[보류] 가을 대표님 최소 보장 강사료 도입(기수당 300~500만, 재원은 회사 50%) · [보류] 루크 8% 재원을 회사 50%에서 충당 — 기한 없음</div><div class="m">11/3 채팅 '가을 대표님 계약서 검토'(11/3 등록) · 루크가 대신 운영하는 구조라 현재는 불필요, 1기 실적이 20~30명에서 멈추면 다시 · 8%는 '1층 계약서 보호 문구' 항목으로 흡수</div></li>
__NEW_P3__
  </ul>
</div>

<h2>최근 [결정] <small>노션 완료 항목 중 최신 6개</small></h2>
<div class="card accent">
  <ul class="list">
    <li><span class="tag done">결정</span><div class="t">스스로 월백 리턴즈 11/11 정기회의 — 윤호 PD 보상 = 프로젝트 순수익 15%(광고비·제작비 및 운영비·환불 제외, 강의 모집일 기준 익월 10일) · 제작경비는 공유 시트 기입 → 루크 월초 3영업일 내 일괄 입금 · 11/18 업로드·유튜브 광고 · 다마고치 첫 촬영 11월 말~12월 초 (11/11)</div></li>
    <li><span class="tag done">결정</span><div class="t">강사님(정복녀 대표님) 강의는 3PL이 아니라 '화장품 도매 창고'로 표현 · '가을' 호칭 폐기 · 타겟 30~40대 여성(경단녀·집에서 시작) — 뷰셀은 메인 강의 회사, 강사님은 작은 회사: 같은 모델을 여러 강사·위치로 뿌려 모객하는 전략 (11/8)</div></li>
    <li><span class="tag done">결정</span><div class="t">셀러들의 수다 임원전용 운영 공유 사이트 — Vercel 대신 Cloudflare Pages + Access(임원 이메일 로그인), 저장소 sooda-exec(비공개) 생성·초기 문서 push 완료 · Access 활성화 전까지 사이트 공개 상태 (11/8)</div></li>
    <li><span class="tag done">결정</span><div class="t">바코드 기반 통합 재고 운영 — 수강생 재고를 바코드(상품) 단위로 묶어 운영, 최종 수량 불일치 시 못 판 수강생에게 변상 또는 재고 인수 (메이븐님 제안 · 약정서 선행 필요) (11/8)</div></li>
    <li><span class="tag done">결정</span><div class="t">오후 1시 이후 출고 취소 신청 불가 — 수강생 공지 완료(2주차 강의) · 시스템 차단은 아직 없음 → 물류 시스템 과제에서 개발 (11/8)</div></li>
    <li><span class="tag done">결정</span><div class="t">입고 동선 — 2중 카트(구매 완료) 위에서 바로 검수·정리, 선반 정리는 입고 즉시 / 포장은 사서함 단위 + 완료품 녹색 카트 → 매뉴얼 v1.2 반영 (11/8)</div></li>
  </ul>
</div>
"""

# 최근 7일(11/6~) 안에 노션 액션보드에 새로 생긴 미완료 항목 — 우선순위 페이지 각 P 구간 끝에 붙는다.
# (할 일, 메모, 노션 url 또는 "", 현금 여부). 기존 줄에 이미 있는 항목은 넣지 않음.
_N = "https://app.notion.com/p/"
NEW_ITEMS = {
 "P0": [
  ("스스로 월백 리턴즈 11/11 정기회의 후속 P0 — 신규 유튜브 '0원 다마고치' 개설(법인 계정 · 민트·PD 편집자)·카카오톡 채널(11/18) · 민트 신청서·CRM 확인(11/17) · 모집 공고 초안(11/17) · 광고 예산(11/17) · 편집본 피드백 → 11/18 업로드·유튜브 광고", "11/9(월) 모집영상 청문회 콘셉트 촬영 완료 · 11/11 의결: 윤호 PD 순수익 15% · 제작경비 시트 → 월초 3영업일 일괄 입금 · 다마고치 첫 촬영 11월 말~12월 초 · 11/4 후속 P0 10건 중 7건 완료 (11/11 등록)", _N+"40e0cf8fea0481ff996cd49d198e87cd", False),
  ("자동등록 — 2개/4개 묶음 신규 옵션 자동 생성·마진 자동 계산 기능 배포 + 실행 시 검정 화면 깜빡임 미노출 처리(11/6 저녁) · 11/6 상담 수강생 한 분 — 녹화 강의·설치 링크·상담 요약 카톡 전달(11/7) → 2차 상담(일요일경, 11/9) 자택 IP·운송장 프로그램·엑셀 주문 처리 + 통신판매업 신고 안내", "플라우드 11/6 심○○ 대표님 보충 통화(59분) Speaker 2(루크) Action Item — 같은 날 배포한 v241·v242에 포함됐는지 확인 필요 · 11/6 상담 녹음(72분) 멘토 몫 — 기한 추정, 수강생 개인 사정은 안 씀 (11/7 등록 3건)", _N+"4100cf8fea04814083c9fad3e8231a0b", False),
  ("대학교 광고지 QR 4개 학교별 유입 통계 세팅(11/14) — [결정] 4개 학교 모두 네이버 QR + 학교별 꼬리표 링크(?from=학교명), 통계는 홈페이지에서 통합 확인 · 이미 배포한 1개 학교 QR은 연결 주소만 수정, 나머지 3개는 새로 생성", "11/7 채팅 'QR코드 자체 제작 가능 여부' · 확인할 것: 어느 사이트(아임웹/GitHub Pages)인지, 방문 통계 도구 설치 여부 (11/7 등록)", _N+"4100cf8fea04817d9b17ce6116628e33", False),
  ("300억 엑시트 11/7 후속 P0 — [결정 필요] 수익을 힐링디어스 법인으로 모으는 전환 계획(11/30) · [결정 필요] 물류 수익에 루크·법인 몫이 없는 구조 — 배분 전에 법인 매출 경로 먼저(11/30)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 노션 메모: 법인 2년째 매출 거의 없음, 수익이 개인으로 흩어짐 — 300억 목표보다 선행, 세무사와 같이 볼 것 · 같은 날 [결정] 디노 합류(물류 책임자)", _N+"4110cf8fea0481bc9957e923998c0439", True),
  ("인베이더 종료 대비 11/7 P0 — 6기 8명 수익 계산(매출·인베이더 몫·광고비·순수익, 마지막 기수 정산 금액 확정 · 11/15) · 해지계약서 검토(대기방 DB 귀속 문구·종료일·6기·4기 정산 기준·영상 자산 소유·라이브 링크 금지) 후 서명(11/15)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 11/7 [결정] 인베이더 파트너십 종료 확정 — 해지계약서 다음 주 수령, 루크 6기·메이븐 4기가 마지막, 12월 강의 없음, 대기방 DB는 우리 귀속 · '우리'에 박○○ 대표님 쪽이 포함되는지 해지계약서에서 분명히", _N+"4110cf8fea048166a06bffd14d3873c8", True),
  ("셀러 멤버십 파일럿 설계 확정(11/30) — 9월 '멤버십+공급형' 기획서 v0.1 기반, 12월 창립 멤버 50명(대기방 10개 · 월 2.9만 · 주간 공급 상품 10개 + 프로그램 + 3PL 옵션 · 노코드) · 위너/슬롯 규칙·반사입 원칙·KPI(3개월 유지율 70%) · [결정 필요] 멤버십과 스월백 강의 판매 충돌 해소 규칙(11/15)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 선행: 통판 신고·토스 운영 키 · 기대 결과: 반복층의 첫 상품, 3월 300명 월 2,000만 목표 · 충돌 규칙: 강의=평생 소유 / 멤버십=월 임대, 스월백 유입자는 1/20 라이브 다음 날 다운셀로만, 12월 파일럿은 인베이더 대기방만", _N+"4110cf8fea048130812ed113351546f8", True),
  ("스스로 월백 3,000만 회수 계산(11/15) — 1/20 라이브 전환률(과거 4%)·객단가·민트·PD 배분 뒤 루크 손익분기 결제 인원", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 11/7 [결정] 예산 약 3,000만 · 돈벌쥐 PD님 합류 · 11/10(월) 첫 촬영 · 기대 결과: 촬영 전에 필요 모수를 알고 광고 예산 배분", _N+"4110cf8fea048145945fed020684bc54", True),
  ("강의업체 이전 — 보험·적금 모델 구조 확인(11/30): 수강생 DB 제3자 제공 마케팅 동의 유무 · 모집 자격(설계사/대리점 등록) · 수수료 환수(중도해지 시 반환) 조건 · 수수료 수령 주체(법인/개인)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 11/5 미팅에서 상대도 중도해지 시 소개자 수수료 일부 반환 가능성을 언급 · 11/7 [결정] 적금 모델 건은 내년 메인 수익 축에서 제외 — 인베이더 종료 뒤 상품명·환급률표 받고 재검토", _N+"4110cf8fea048151a74fc730231615a3", True),
  ("가을 대표님 런칭 기획(11월, 루크 · 진행 중 · 11/30) — 초월스토리에서 메이븐 플랫폼 수익 모델 그대로 적용, 11월 안에 기획·커리큘럼·가격 확정", "11/7 낮 채팅에서 노션 등록(11/7 등록)", _N+"4110cf8fea04818aa26cfa7f3020ab3b", True),
  ("가을 대표님 12월 강의 런칭 11/8 P0 7건(모두 11/15) — 새 닉네임 확정('가을' 폐기 · 도매언니/창고언니 후보) · 화장품 소량 리셀 직접 시작(11월 3주, 12월 라이브용 본인 기록) · 코칭생 2~3명 촬영·숫자 사용 동의서 · 12월 강의 컨셉 확정('화장품 도매 창고 + 올려드림', 타겟 30~40대 경단녀) · 도매 창고 모델 4개 룰 설계(SKU 배정·최저가 하한·재고 상한·책임선 → 정원) · 11~12월 수익 모델별 분리 기록 · 강의 회사 채널 시청자층 확인", "11/8 [결정] 강사님 강의는 3PL이 아니라 '화장품 도매 창고'로 표현·'가을' 호칭 폐기·타겟 30~40대 여성(경단녀) · 런칭 전 월 500만은 목표값 · 본인 기록 없으면 가을님 런칭은 1월로 이월 판단 (11/8 등록 7건)", _N+"4120cf8fea0481f78dcff3d86d1a67ab", True),
  ("리나님 역할·조건 재정의 합의(11/15) — 스토어 전체 책임자 → 출고 책임자, 시간당 40건·정시 출퇴근, 300건 초과분 40건당 알바 1시간, 알바 미달분은 리나님 책임", "11/8 물류 채팅 → 노션 등록 · 미결: 알바 공급처·당일 호출 가능 여부, 300건 미달 날 책임, 200건 미만 날 유휴 시간 · 기대: 하루 300건 출고 체계 안정화, 디노님 = 운영책임+입고 · 급여 조건은 공개 페이지에 싣지 않음 (11/8 등록)", _N+"4120cf8fea048161ab59ea7779dbf06e", False),
  ("임원전용 운영 공유 사이트 배포 마무리(11/15, 진행 중) — Cloudflare Zero Trust 무료 요금제 활성화(루크 직접) → Access 정책을 '임원 이메일 허용'으로 → 디노님·메이브님 이메일 추가 후 링크 공유", "11/8 [결정] Vercel 대신 Cloudflare Pages + Access, 저장소 sooda-exec(비공개) · 11/8 12:00 Pages 배포 완료·Access 앱 생성 · <b>Access 활성화 전까지 사이트 공개 상태</b> · 첫 문서 = 물류 매뉴얼 v1.1 피드백 정리 (11/8 등록)", _N+"4120cf8fea048143944fcb5cae7793c7", False),
  ("세무사 미팅(11/12) — 수취 주체 법인 전환·법인 매출 잡는 순서 등 세무 상의 안건 정리해서 가기", "플라우드 11/7 '일정 조율' 녹음(81초) 실행 항목 → 노션 등록 · 안건은 녹음에 없음 — 노션 열린 세무 건(수취 주체 법인 전환 11/30 · [결정 필요] 수익 법인 전환 계획 11/30)과 묶어서 (11/9 등록)", _N+"4120cf8fea04817fbc0afa80e51e196e", False),
  ("물류·3PL 11/10 운영 회의·현안 진단 후속 P0 3건 — 11/9 오배송 갤럭시 탭 2대 반송 요청·출고 건 교차 확인(11/12) · 디노님에게 물류 파트 인계 + 바코드 분류 체계 적용·메인 시트·매뉴얼 확인(11/15) · 물류 직무 범위·협업 프로세스 확정 전체 회의 소집(다음 주 → 11/20) — 기한 모두 추정", "플라우드 11/10 '운영 회의: 물류 안정화·재고 관리·강의 런칭'(70분)·'물류 운영 현안 진단'(74분) → 노션 새 항목 3건(11/10 등록) · 전날 300건 중 약 100건 처리 → 디노님 물류 전담 · 선제 보고 체계 합의 · 급여 조건은 싣지 않음", _N+"4140cf8fea0481b89963e88c89c37287", False),
  ("물류 11/11 녹음 후속 P0 — 11/17(화) 물류 역할 조율 자리 전 현장 검증: 일주일간 입고·출고·반품·전산·CS를 직접 확인해 소요 시간·처리량·병목 기록 → 업무 처리 기준 정리(11/17) · 전체 회의 소집 기한 11/20(추정) → 11/17(화)로 수정", "플라우드 11/11 '물류 운영 표준화와 총괄 책임자의 역할 논의'(77분, 10:54 KST) — 요약의 '대표님'(물류 총괄 맡을 분, 디노님으로 추정·확인 필요) Action Item → 노션 새 항목(11/12 등록) · 4시간 100건(시간당 25건)·메이브님 기대 3시간 100건은 회의 발언, 검증 전 · 리나님 역할 범위는 11/17 자리에서 본인이 설명 · 급여·감정 관리 조언은 싣지 않음", _N+"4150cf8fea048129888dc82dd4082f12", False),
  ("가을님 강의 제작 자료 전달(11/15, 추정) — 프로필 사진 구글드라이브 업로드 · 유튜브 촬영·수강생 촬영 일정(업체가 정하면 우리가 맞추기로 회신) · 상세페이지 자료(수강생 매출 인증·과거 사진) 정리", "플라우드 11/11 10:26 루크 메모(26초) → 노션 새 항목(11/12 등록) · 11/4 프로필 사진 스마트폰 촬영+AI 보정 안·11/8 유튜브 촬영 플랜(11/30)과 이어짐 · 기한 추정", _N+"4150cf8fea0481c6ae54cf60f4d77b3c", True),
 ],
 "P1": [
  ("스스로 월백 리턴즈 미결 — 상금 300만 분배 방식(11/18) · 1/20 고정 재확인(11/18) · 본편 5편 회차별 구성(11/30) · PD 15% '순수익' 정의·경비 상한·환불 정산을 민트 계약서와 맞추기(11/30) · 11월 제작경비 일괄 입금(12/3) · 11월 말 선정", "11/11 정기회의에서도 결론 안 난 것 · 상금은 다마고치 2명이면 '1등 300만' 단일안이 1명만 받는 구조 · 광고비·상금이 순수익에서 빠지므로 많이 쓸수록 PD 15%도 줄어듦 (11/11 등록)", _N+"40e0cf8fea048187b0b7c39d065e9f90", False),
  ("11/5 박○○ 대표님 미팅(플라우드 123분) 루크 Action Item 2건 — 플랫폼 논의 내용(1월 안·광고비 공개 방식·단톡방 활용 모델) 메시지로 정리해 전달(11/7, 추정) · 2주차 강의 종료 후 소싱·사입 운영 프로그램 관련 내용 정리해 전달(11/15, 추정)", "요약 기한은 TBD·'다음 주' → 메이브님 통화(11/8) 전 / 6기 2주차(11/9~15) 종료 후로 추정 · 상대측 몫(플랫폼 사이트 준비·심사, 단톡방 자료 전달)은 넣지 않음 (11/6 등록)", _N+"40f0cf8fea0481c3bffffae0af64ddfa", True),
  ("쇼핑몰 5곳 구매 교육자료 완성(사이트별 HTML 5장+목차+PDF 6, 사진 249장·인포그래픽 53개) → 루크 검토 후 빠진 화면(결제 직후·앱 알림) 직접 캡처(11/30) · 심○○ 대표님 11/6 보충 후속 — 홈페이지 추천상품 소싱 시연 + 소싱 엑셀 결과로 상품 등록·슬롯 설정 확인(11/10, 추정)", "11/6 채팅 '쇼핑몰 구매방법 교육자료'(진행 중) — 6기 2주차 자료실에 수강생 전용으로 이미 게시 · 보충 후속은 플라우드 11/6 통화 '강사' Action Item(요약 기한 11/6 저녁은 지남) (11/6~11/7 등록 2건)", _N+"4100cf8fea04813f8794cadafe0a1440", False),
  ("300억 엑시트 11/7 후속 P1 — 보부상 300억 엑시트 사례 확인: 매출 규모·수익률·인수자가 산 것(수강생 DB / 강사망 / 브랜드) 세 가지를 업계 지인에게(11/30) · 패시브 인컴(유통) 구조 설계 세션 준비 — 3PL 이용 수강생 수·월 출고 건수·건당 단가 / 사입 전환 비율 / 메이븐 스토어 공급처·마진율(11/15)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 숫자가 아니라 구조를 알아야 힐링디어스에 대입 가능 · 반복층(3PL·공급·구독) 월 1,000만 목표의 현재 위치를 숫자로 — 숫자 받으면 클로드가 계산 모델 페이지 제작", _N+"4110cf8fea048141ac5cf913bc3ff77d", True),
  ("금융상품 제휴 전 확인(11/30) — 미등록자가 가입 건당 수수료를 받아도 되는지(보험업법 모집수수료 금지), 정액 광고·콘텐츠비 구조로 바꿔야 하는지 — 보험 전문 변호사 또는 금감원 안내로", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 노션 메모: 건당 수수료 = 모집수수료 성격, 유명인 강연 모델은 보통 정액 강연료·광고비 · 인베이더 해지 마무리 뒤(11월 말) 상품명·해지환급률표·수수료 구조 요구", _N+"4110cf8fea048195bae0d059367fe347", True),
  ("창고 택배비 결제 개통을 툴박스 보류와 분리할지 결정(11/30) — 통판 신고는 어차피 필요(유료 판매 전부)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 11/7 [결정] 툴박스 잠정 보류 · 【최우선】 결제 시스템 실제 열기(진행 중)와 같은 뿌리", _N+"4110cf8fea0481f68415ee56be929768", False),
  ("[검토] 상품 등록 대행 서비스(11/30) — 멤버십 프로 티어/애드온(월 50개 49,000 안) · 스마트스토어 매니저 권한으로 접근 · 자동등록 프로그램으로 B 엔진 직원이 수행 · 제재 책임·수량 한도 약관 — 10/31 '대리등록 수십 개' 항목과 통합", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 첫 주문률(멤버십 1순위 리스크)을 올리는 직접 수단", _N+"4110cf8fea048139a7f2fa9e81fa3000", True),
  ("가을 대표님 런칭 11/8 P1 4건(모두 11/30) — 유튜브 촬영 플랜(가을님 2~3편 + 코칭생 2~3명 인터뷰, 11월 3~4주 촬영) · 라이브 PPT 7구간(사연→증거→실연→구조→리스크→정원→루크 보증) · 메이브님과 화장품 강의 내부 영역 분리 합의(공개적으로는 별개 인물) · 등록 대행 티어·요금 구조(셀프 / 올려드림 100개 / 맡김 300개)", "11/8 채팅 → 노션 등록 · 프로그램 시연편은 만들지 않음 · 초월스토리 12월 초 라이브 일정 확인 필요 · 알바 1인 100개 등록 공수 측정 필요 (11/8 등록 4건)", _N+"4120cf8fea0481c19fffd8ba3f6408e4", True),
  ("물류·3PL 11/8 P1 3건(모두 11/30) — 매뉴얼 v1.2 반영 요청(메이브님 담당: 2중 카트 동선·선반 즉시 정리·사서함 단위 포장·300건 타임테이블·미출고 플로우) · 바코드 통합재고 수강생 약정서 초안(변상 기준·재고 인수·소유권·FIFO 동의) · 물류 시스템 과제 4건(출고 취소 차단 > 셀프 조회·챗봇 > 미출고 판정 > 바코드)", "11/8 [결정] 3건: 바코드 기반 통합 재고 운영 · 오후 1시 이후 출고 취소 불가(2주차 강의 공지) · 입고 동선 2중 카트·사서함 단위 포장 · 매뉴얼 원본은 메이브님 v1.1(1인 기준) (11/8 등록 3건)", _N+"4120cf8fea0481eaa4efc4aa7132209d", False),
  ("11/19 화장품 제품 업체·헤어 기기 미팅 — 업체명·안건 확인 후 준비", "플라우드 11/7 '일정 조율' 녹음 실행 항목 → 노션 등록 · 토탈샵 헤어 기기 공급처(로레알 1순위) 건과 같은 건인지 확인 필요 (11/9 등록)", _N+"4120cf8fea0481d5b165cd8c8628c699", False),
  ("물류·3PL 11/10 후속 P1 3건(모두 11/30, 추정) — 강의 종료 후 재고조사·상품별(바코드) 통합 재고 정리 검토 · 입고 리스트 기준 도입(수강생이 카탈로그명·운송장 직접 입력, 미확인 물품 처리 기준) + 자동 처리 프로그램 · 물류 센터 현장 견학 기획(11/3 현장 실습 건과 같은 건인지 확인 필요)", "플라우드 11/10 운영 회의·물류 현안 진단 → 노션 새 항목 3건(11/10 등록)", _N+"4140cf8fea0481f9a73ff7055f7489cf", False),
  ("신규 강사 복수 플랫폼 배치 검토(11/30, 추정) — 11월 중 플랫폼 1~2곳 확인 · 촬영 PD 통해 '타이탄' 측 연결 가능 여부 · 초월스토리 등 진행 결과 확인 뒤 배치 방향 결정 · 런칭 3주 뒤 단발성 강의 순환 런칭 모델 검토", "플라우드 11/10 운영 회의 → 노션 새 항목(11/10 등록) · 금융상품 수익 모델은 진행 안 하는 쪽(대체 모델 미정)", _N+"4140cf8fea04810f825cf07fe8f9656c", True),
  ("물류 창고 배치·전산·운영 자료를 신규 인력이 처음 봐도 3일 안에 적응할 수준으로 단순화 검토(11/30, 추정) — 출구·입구·반품 위치 한눈에, 전산은 입고·출고·반품 수치 혼동 없게(기능 추가보다 감추기·통합), 첫날 한 가지 작업 → 단계적 확대", "플라우드 11/11 물류 녹음 Action Item → 노션 새 항목(11/12 등록) · 교육 담당자가 장시간 붙는 방식 대신 자료·배치가 교육을 대신", _N+"4150cf8fea0481ac9c1cf623e2fb2519", False),
  ("키티티 토탈샵 11/12 세무사 상담 후속 P1 3건(모두 11/30, 추정) — 사업자 분리 등록 준비(서비스별 공간 구획 + 임대차/전대차 계약·영업허가증 → 세무대리인 전달·업종 코드 재확인) · 인테리어 공사비 사업자별 세금계산서·환급 + 간이과세 포기·일반과세 전환 여부 확인 · 표준 근로계약서·프리랜서 계약서 샘플 검토 → 전달 + 사업 지출 구분 기록 시작", "플라우드 11/12 '뷰티 토탈샵 확장 및 세무·노무 상담'(134분, 14:16 KST — 11/12 14:00 세무사 미팅) '대표' Action Item 6건 중 지영 원장·루크 서포트 몫 → 노션 새 항목 3건(11/13 등록) · 정부 지원 확인은 기존 항목과 같은 일 · 세무대리인 몫·금액·급여는 싣지 않음", _N+"4160cf8fea0481ab8d16e4b9989a73aa", False),
 ],
 "P2": [
  ("유튜브 리드 퍼널 — 자체 무료 도구(연출컷메이커·마진메이커 등)로 '댓글 키워드 → 무료배포 → 카톡/카페 가입' 쇼츠 퍼널 테스트(12/31)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 참고 사례(시스메이커 쇼츠)는 해외 오픈소스 소개 + 이메일 게이트 + 99,000원 상품 — 50~60대 핵심 고객은 Claude Code 안 씀 → 자체 도구로 변형", _N+"4110cf8fea048146abc7c8ca9ac089cf", False),
  ("[검토] 저축 스몰 챌린지(한 달에 얼마씩 모으기 · 12/31) — 목표 실행 챌린지 대신 검토, 셀러 커뮤니티와 연결('번 돈 남기기')할지 별도 브랜드로 갈지 결정 → 유료 소액 챌린지 1기수 설계안", "11/7 낮 채팅에서 노션 등록(11/7 등록)", _N+"4110cf8fea0481628bbcf7e5259e7be9", False),
  ("11/10 상담 수강생 재상담 시 확인(11/30, 추정) — 6개월 이상 운영 가능 여부 · 『인간관계론』 독서 · 무료 콘텐츠로 실제 소싱·상품 등록 실행 내용", "플라우드 11/10 '이커머스 소싱·판매 진입 상담'(30분) 강사 Action Item → 노션 새 항목(11/10 등록) · 재상담 일정 미정 · 상담자 개인 사정은 적지 않음", _N+"4140cf8fea0481e49122e82d395c3597", False),
 ],
 "P3": [
  ("youtube-agent-skill 설치 후 /yt-comment·/yt-shorts·/yt-chapters 내 채널에 테스트 — 먼저 내 영상 3편 자막으로 voice.md 생성 (P3, 기한 없음)", "11/7 낮 채팅에서 노션 등록(11/7 등록) · 댓글 답장·쇼츠 구간 추출 시간 절감 여부 확인", _N+"4110cf8fea0481d3a6e1cdc7b3fc282c", False),
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
<h1>10/16 등기 — 등기부 확인 끝</h1>
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
    <li>11-12 녹음 2건(11/13 06:41 조회, 11/11~11/13 범위 4건 중 11/11 2건은 11/12 반영 완료): '11-12 뷰티 토탈샵 확장 및 세무·노무 상담 요약'(134분, 14:16 KST — 11/12 14:00 세무사 미팅, 지영 원장 토탈샵 건 중심 · 루크 동석) → 요약 '대표' Action Item 6건 중 지영 원장·루크 서포트 몫을 묶어 노션 새 항목 3건(11/30 P1, 기한 추정 — 사업자 분리 서류 · 인테리어 세금계산서·과세유형 · 근로/프리랜서 계약서+지출 구분 · 정부 지원 확인은 기존 항목과 같은 일) · 세무대리인 몫 4건·공사비 금액·급여·개인 일정은 싣지 않음 · '11-12 인테리어 자금 확보를 위한 지인 지원과 금융 대출 비교'(58초, 개인 재정 메모라 싣지 않음) → 노션 새 항목 3건</li>
    <li>11-11 녹음 2건(11/12 06:41 조회, 11/10~11/12 범위 5건 중 11/10 3건은 11/11 반영 완료): '11-11 물류 운영 표준화와 총괄 책임자의 역할 논의'(77분, 10:54 KST — 루크와 물류 총괄을 맡을 분(요약 '대표님', 디노님으로 추정·확인 필요)의 역할 논의) → 회사 몫 Action Item 2건 노션 새 항목(현장 검증 → 11/17 역할 조율 P0 · 창고·전산 단순화 11/30 P1 추정), 기존 전체 회의 소집 항목 기한 11/20 → 11/17(화)로 수정 · 리나님 거취·급여·감정 관리 조언·대인 관계 내용은 적지 않음 · '2026-11-11 10:26:17'(26초, 루크 메모 — 가을님 강의 제작 자료: 프로필 사진·촬영 일정·상세페이지 자료) → 노션 새 항목 1건(11/15 P0 추정) → 노션 새 항목 3건</li>
    <li>11-10 녹음 3건(11/11 06:41 조회, 11/9~11/11 범위 5건 중 11/9 밤 메모 2건은 11/10 반영 완료): '11-10 이커머스 소싱·판매 진입 상담 및 실행 방향'(30분, 13:02 KST — 신규 상담 한 분, 유료 등록 전 무료 자료로 소싱·등록 실행 후 재상담 · 강사 Action Item 1건 → 노션 새 항목 11/30 P2 추정, 상담자 개인 사정은 적지 않음) · '11-10 운영 회의: 물류 안정화·재고 관리·강의 런칭'(70분, 16:14 KST, 4명 — 금융상품 모델 진행 안 함 · 라이트 구독 검토 · 디노님 물류 전담 · 갤럭시 탭 2대 오배송 · 입고 리스트 기준 · 복수 플랫폼 배치 · 11/9 카메라 8대 촬영 언급) → 루크·회사 몫 후속 조치 6건 노션 새 항목(오배송 반송 11/12 P0 · 디노님 인계 11/15 P0 · 재고조사·입고 리스트·복수 플랫폼 11/30 P1), 계약 해지·리나님 역할·강사 촬영·녹음본 확인은 기존 항목과 같아 허브에만 · '11-10 물류 운영 현안 진단 및 업무 프로세스 개선 협의'(74분, 17:36 KST — Speaker 1 루크·Speaker 2 물류 담당자) → 루크 Action Item 2건 노션 새 항목(전체 회의 소집 11/20 P0 추정 · 물류 센터 견학 11/30 P1), 담당자 몫·급여 체계는 적지 않음 → 노션 새 항목 8건</li>
    <li>11-09 녹음 2건(11/10 06:41 조회, 11/8~11/10 범위 2건 · 11/8 녹음 없음): '2026-11-10 00:16:15'(20초, 예약 시점 메모)·'11-10 논의: 프라이빗 검색과 가격 알고리즘'(30초, 반복 검색 시 가격 상승 메모) — 둘 다 00:16 KST 개인 메모, 실행 항목 없음 → 노션 새 항목 0건</li>
    <li>11-07 녹음 1건(11/9 06:41 조회, 11/7~11/9 범위 1건 · 11/8 녹음 없음): '11-07 일정 조율 회의'(81초, 18:45 KST) — 사업 항목 2건만 반영(세무사 미팅 11/12 · 화장품 제품 업체·헤어 기기 미팅 11/19 → 노션 새 항목 2건, 기한은 녹음 날짜 그대로, 안건·업체명은 녹음에 없음) · 개인 일정은 적지 않음</li>
    <li>11-07 녹음 없음(11/8 06:41 조회, 11/6~11/8 범위 6건 = 11/6 녹음, 11/7에 반영 완료) → 노션 새 항목 0건</li>
    <li>11-06 녹음 7건(11/7 06:41 조회, 11/5~11/7 범위 8건 중 11/5 1건은 11/6 반영 완료): '11-06 상담: 네이버 스마트스토어 부업 창업 기초 세팅 및 멘토링'(72분, 12:23 KST — 신규 상담 수강생 한 분: 월 50만 부업 목표 · 사업자등록 신청·스마트스토어 개설·계정 인증·IP 등록 진행, 상품 등록 없음 · 통신판매업 신고는 11/9 주간 · 2차 상담 일요일경) → 멘토 몫 2건 노션 새 항목(11/7·11/9, 기한 추정), 수강생 몫(녹화 시청·사업자등록 확인)은 넣지 않음, 개인 사정은 안 씀 · 심○○ 대표님 mvoip 통화 4건(59·44·10·5분, 09:36~11:30 KST — 소분 포장 규정·마진 엑셀·묶음 옵션·네이버 50% 가격 제한 대응·식품 꼬리물기 소싱 실습·통조림 후보) → 대표님 몫은 새 항목 없음, Speaker 2·강사(루크) 몫 2건 노션 새 항목(프로그램 묶음 옵션·깜빡임 11/6 P0 · 시연+엑셀 등록 확인 11/10 P1) · '2026-11-06 19:03:59'(313분 — 6기 2주차 강의로 추정, AI 노트 없음, 읽지 않음) · '좋아하는 사람'(7분)은 개인 녹음이라 읽지 않음</li>
    <li>11-05 녹음 1건(11/6 06:41 조회, 11/4~11/6 범위 8건 중 11/4 7건은 11/5 반영 완료): '11-05 목요일 — 박○○ 대표님 미팅 (업무 블록 넣지 않기)'(123분, 11:17 KST 시작 — 신규 교육 플랫폼 운영자와 미팅, 화자 2 = 루크·화자 3 = 상대: 인베이더 12월 이후 불확실 → 신규 플랫폼 구상(구축·심사 약 3주, 1월 안 조율 중) · 수강생 단톡방 활용 무료 챌린지·멤버십 모델 · 마켓별 운영 관찰 · 인력·물류 효율화 · 강사 육성). 11/5 저녁 채팅이 노션에 [결정] 1건+새 항목 4건(프로젝트 '강의업체 이전')을 이미 등록 → 요약 '후속 조치'의 화자 2(루크) 몫 2건만 노션 새 항목(11/7·11/15, 기한 추정), 화자 3 몫 2건은 넣지 않음 · 후반 개인 대화·이동 중 대화는 읽지 않음</li>
    <li>11-04 녹음 7건(11/5 06:41 조회, 11/3~11/5 범위 14건 중 11/3 7건은 11/4 반영 완료): '11-04 기획 회의: 유튜브 신규 채널 개설 및 다마고치 프로젝트 일정'(38분, 12:01 KST)·'[윤호PD님/민트님/루크님] 2차 회의'(9분, 12:41 KST — 청문회 콘셉트·면접관 4~5명 섭외·엑스트라 인당 15만) → 11/4 저녁 채팅이 노션·공유 회의록(meetings/)에 이미 반영, 새 항목 없음 · '[OneCrew] 최은봉 대표님'(30분, 14:30 KST — 해외직판 자금·인력 계획, 위수탁·정가품 소명 대응) → 과제는 대표님 몫, 새 항목 없음 · '박태경 원크루'(108분, 16:48 KST — 소싱 습관화·달바 정품 소명·리뉴얼 공지·강의 런칭 준비) → 강사 몫 3건 노션 새 항목(기한 추정) · '[OneCrew] 정복녀 대표님 찐초보 7기'(58분, 17:59 KST — 소싱 시간 확보·가을 대표님 3주 코칭 2명 선정·프로필 사진·소명자료) → 상담자(루크) 몫 3건 노션 새 항목(11/5 · 11/9·11/7 추정) · 1차 회의(14초)·'2026-11-04 12:00:33'(82초, 내용 없음)은 노트 없음 · 요약에 섞인 가정·건강·심리 사정은 어디에도 적지 않음</li>
    <li>11-03 녹음 7건(11/4 06:41 조회, 11/2~11/4 범위 15건 중 11/2 8건은 11/3 반영 완료): '11-03 회의: 물류 현장 실습 및 3PL 사업·창고 확장 계획'(40분, 17:36 KST — 3일 현장 실습 관찰 요령 · 물류 안정화 후 3PL 외부 고객·풀필먼트 · 수익 배분 기준 미정 · 2027 초 본사 서울 이전·창고 확장 · 이사 등재) → 노션 새 항목 2건(11/30 P1 · 2027-01-31 P2, 기한 추정) · '11-03 강의: 온라인 판매 상품 소싱과 가격 경쟁 전략'(179분, 21:31 KST — 시장 가격·수동 소싱·프로그램 설정·주문 처리, 1주차 11/3~8 → 2주차 11/9~15) → 강사 몫 2건 노션 새 항목(주소값 오류 수정 11/9 P0 · 수강 신청자 사전 확인 11/15 P1, 기한 추정) · '심○○ 대표님 11기'(118분, 16:58 KST — 1:1 컨설팅, 과제는 수강생 몫 · 11/6 보충 설명·11/10 후속 점검 일정만 반영, 개인 재정·건강 사정은 어디에도 적지 않음) · mvoip 1:1 코칭 3건(11:01 58분 · 12:30 69분 · 14:16 31분 — 재설치·소싱 프로그램·엑셀·자동등록 실습, 수강생 몫이라 노션 새 항목 없음, 수강생 가족·거주지 등 개인 정보는 싣지 않음) · '11-03 높은 기대와 근거 있는 전망'(37초, 메모 — Action Item 없음)</li>
    <li>11-02 녹음 7건(11/3 06:41 조회, 11/1~11/3 범위 9건 중 11/1 2건은 11/2 반영 완료): '돈벌쥐 조윤호 PD님'(44분, 17:47 KST — 퍼스널 브랜딩 채널 장기 방향·대행/RS 하이브리드, 신규 강의 프로젝트 촬영 인건비·턴키 RS, 수요일 줌·다음 주 대면 미팅) → 노션 새 항목 4건(기한 추정) · 수강생 1:1 세팅·코칭·재설치 상담 3건(29·50·29분)과 밤 1:1 컨설팅(117분)은 과제가 수강생 몫이라 노션 새 항목 없음, 안내 일정·공통 요청만 허브에 · 개인 대화 2건은 읽지 않음</li>
    <li>11-01 녹음 2건(11/2 06:41 조회, 10/31~11/2 범위 3건 중 10/31 회의는 11/1 반영 완료): '술자리: 일상 대화 및 음주 중 불만 표현'(8분, 개인 녹음이라 읽지 않음) · '2026-11-01 19:01:28'(4초, 노트 없음) → 노션 새 항목 0건</li>
    <li>10-31 녹음 1건(11/1 06:41 조회, 10/30~11/1 범위 2건 중 10/30 미팅은 10/31 반영 완료): '10-31 회의: 강의 런칭·커리큘럼 표준화, 프로그램 운영 정책, 스마트스토어·3PL 물류, 마케팅·출연자 운영, 패키징·가격 전략, 파트너십·정산 체계'(76분, 15:55 KST 시작 — 초월스토리 측과 가을 대표님 강사 런칭 회의, Speaker 1 = 루크). 작업 항목 중 초월스토리 측(마케팅·세일즈·콜링·블로그/카페/스레드) 몫은 빼고 루크·회사 측(교육기획·운영·IT·물류·'[Insert Name]') 몫 19건을 노션 새 항목으로(11/1·11/7은 요약 기재값, 나머지 기한은 추정). 설문으로 출연 수강생 2명 선발(11/4)은 기존 '성과자 섭외'(10/31) 항목과 같아 새로 만들지 않음. '뷰셀링'은 뷰셀님 12월 강의로 읽었으나 확인 필요. 개인 사정(가족·건강·거주지) 언급은 넣지 않음</li>
    <li>10-30 녹음 1건(10/31 06:41 조회, 10/29~10/31 범위): '스스로월100 미팅 : 민트님 : 돈벌쥐 PD님'(112분, 12:04 KST 시작 — 다마고치 콘셉트 신규 채널 프로젝트 기획: 네이버 운영·마진 룰, 모집·제작 운영, 타깃·브랜딩, 포맷·상금형 경쟁, 면접형 첫 에피소드, CRM 퍼널·에이전시 일정). 요약의 '핵심 이슈' 중 루크 몫 → 노션 새 항목 5건(기한은 정기 회의 매주 수 13시 기준 추정) · 네이버 운영 룰(저가 유입·꼬리물기 소싱·반사입)은 강의 내용이라 항목 없음 · 10/29 녹음 없음</li>
    <li>10-29 녹음 없음(10/30 06:41 조회, 10/28~10/30 범위 3건 = 10/28 녹음 3건, 10/29에 반영 완료) → 노션 새 항목 0건</li>
    <li>10-28 녹음 3건(10/29 06:41 조회, 10/27~10/29 범위): '[OneCrew] 정복녀 대표님 찐초보 7기' 2건(14:22 KST 12분 — 메인 스토어 이용 정지 예정 통보 소명·서브 스토어 상품 이전·프로그램 로그인 오류 원격 지원 / 14:56 32분 — 상품 등록 최적화·초월스토리 강의 준비·코칭 알바·채널 분산·매출 목표 1억) · '[OneCrew] 최은봉 대표님'(12:24 KST 24분 — 신규 사업자등록·소명 2건·일본 야구 유니폼 직판·업무 분장·회사소개서). Speaker 1=루크로 보고 루크 Action Item만 노션 새 항목 8건(정복녀 6 · 최은봉 2), 대표님 몫 과제는 넣지 않음 · 가을님 가능 시간대·마진·고정비 추산값은 싣지 않음</li>
    <li>10-27 녹음 1건(10/28 06:41 조회, 10/26~10/28 범위): '김종진 대표님 10기'(56분, 17:57 KST 시작 — 러닝 브랜드 디자인 콘셉트·페르소나·세일즈 코칭). 과제는 대표님 몫(강사를 고객으로 놓고 30만원 운동복 예약구매 설득 연습)이라 노션 새 항목 0건</li>
    <li>10-26 녹음 없음(10/27 06:41 조회, 10/25~10/27 범위 1건 = 10/25 라이브 본편, 10/26에 반영 완료) → 노션 새 항목 0건</li>
    <li>10-25 녹음 1건(10/26 06:41 조회, 10/24~10/26 범위): '10-25 특강: 스마트스토어 자동 후불 사입 및 무재고 창업 전략'(4시간 47분, 19:29 시작 — 6기 무료 라이브 본편). 강의 녹음이라 루크 담당 Action Item 없음(요약의 '과제/활동 제안'은 참석자 몫) → 노션 새 항목 0건. 라이브에서 안내한 정규 과정 일정(11/6 금 19시 시작·4주·선착순 약 30명·269만)은 허브에 기록, 참석·전환 숫자는 요약에 없음</li>
    <li>10-24 녹음 1건 추가(10/25 06:41 조회, 10/23~10/25 범위 12건 중 11건은 10/24 반영): '주간 촬영 메이크업·헤어 운영 및 보상 구조 고정화 계약 안'(72초 메모, 루크 혼자) → 노션 새 항목 2건(촬영 출장 계약 조건 문서화 · 헤어팀 보상안·2인 배치 손익 시뮬레이션, 기한 10/31은 추정). 요약의 역할 배정(@영업리드 등)은 AI가 붙인 것이라 전부 루크 담당으로 봄 · 급여·기준선 숫자는 노션 메모에만. 10-25 녹음 없음</li>
    <li>10-23~10-24 녹음 11건(10/24 06:41 조회, 10/22~10/24 범위): [인베이더 대표님 6기 라이브 피피티 장표 수정](33분) · 10-23 기획 회의 — 무료 라이브 강의 자료 개선(29분) · [OneCrew] 정복녀 대표님 찐초보 7기(45분) · 민트/다마고치 10-23 회의(22분) · 테라피님 인터뷰 준비 코칭(54분) · 민트님 프로젝트기획 협의 — 인베이더 지속 여부와 촬영·채널 운영 비용(21분) · 돈벌쥐 PD님 통화(15분) · 10-24 업무 회의 — 보고 체계·출고·재고(25분) · 10-24 회의 — 팀 내 갈등 공유·중재 절차(3분, 대인 관계·인사라 넣지 않음) · 상담: 부채 상환(개인, 읽지 않음) · F1 패널 토론(개인, 읽지 않음). 루크 담당 Action Item 중 노션에 없던 6건을 새로 등록(민트 주간 정기 회의 10/28 · 뷰셀님 측 기획사 미팅 11/10 · 초월스토리 촬영 일정 11/1 · 테라피님 CS 템플릿·세팅 10/31 · 물류 브리핑 10/27 · 물류 KPI 10/31, 기한은 노트 기재값·추정) — 나머지는 당일 클로드 대화가 이미 노션에 등록(10/23 새 항목 33건)</li>
    <li>10-22 녹음 3건(10/23 06:41 조회, 10/21~10/23 범위): '미팅: 샵 일정 확인 및 1시 30분 미용 재료 조율'(2분, 샵 일정 확인뿐이라 Action Item 없음) · 'HGV 타임셰어 체험 프로그램 고객 상담'(2시간 37분, '사업 외 개인'인 힐튼 설명회라 읽지 않음) · '2026-10-22 18:03:02'(2초, 노트 없음) → 노션 새 항목 0건</li>
    <li>10-21 녹음 4건(10/22 06:41 조회, 10/20~10/22 범위): 박태경 원크루 세션 2건(15:01 57분 · 16:03 51분) · [OneCrew] 최은봉 대표님(57분) · '10-21 엔진 3 — 거인의 도구공방'(6분, 내용 없음). 박태경 공동 Action Item 2건 → 노션 새 항목(성과 평가 10/27 · 공동 상품 찾기 10/28, 기한은 노트 기재값) · 대표님 과제(100개 등록 · 꾸준 판매 리스트 · 밥솥 링크)는 넣지 않음 · 최은봉 세션의 강사 Action Item(일본 직판 교육 내용 정리·전달)은 당일 노션 '일본직판 전자책 편입' 항목과 같은 일이라 새로 만들지 않음, 대표님 과제(주차별 실행 계획)는 제외</li>
    <li>10-20 녹음 없음(10/21 06:41 조회, 10/19~10/21 범위) — 10/19 녹음 3건은 10/20에 반영 완료</li>
    <li>10-19 녹음 3건(10/20 06:41 조회, 10/18~10/20 범위): 신정현 대표님 이커머스 확장·교육 고도화 회의(69분) · 인베이더 강의 기획 회의 — 강의 자료 개편·프로그램 데모(39분) · 뿌요 코칭 세션(3시간 38분, 개인 코칭이라 Action Item 반영 안 함). 당일 클로드 대화가 역직구 위너 시스템 4건(결정 1 포함)·고려대 거울 광고를 이미 노션에 등록 → 빠진 루크 담당 Action Item 10건만 새로 등록(신정현 회의 7건: 월요일 정기 라이브 10/26 · 인베이더 종료 공지 단톡방·금요일 택배비 할인·채용 공고 영상·핵심 인력 성과 기준 10/31 · 당일 직배송 테스트 11/30 · 박종혁 첫 출근 준비 10/21 / 기획 회의 3건: 최종 리허설·FAQ 문안 10/23 · 출연 수강생 연락 10/24 — 기획 회의의 Speaker 1은 루크로 추정, 리허설 일시 외 기한은 추정). 강사(Speaker 3)·뿌요(Speaker 3) 담당과 담당 미기재 항목은 넣지 않음</li>
    <li>10-18 녹음 4건(10/19 06:41 조회, 10/17~10/19 범위): 뷰티 토탈샵 오픈 준비 회의(20분) · 미용실 매장 인수 및 가오픈 준비 회의(59분) · 개업 준비: 미용·에스테틱 장비와 공간 구성(38분) · 뷰티 샵 운영 전략 및 연인 간 소통(75분, 사적 대화 부분은 읽지 않음) — 당일 클로드 대화가 이미 노션에 12건 등록(헤어 공급처·네일 세트·인스타 구조·발품·브랜딩·손익·투자·급여·권리금 부속 합의·[결정] 3건) → 빠진 루크 담당 Action Item 3건만 새로 등록(인테리어 업체 상담+실측 · 에스테틱·베드 기기 조사 · 페르소나 콘텐츠 기획, 기한 11/15 추정). 미배정 항목(샴푸대 점검·헤드스파 옵션·의자 천갈이·종이컵 주문)과 고객(지영 원장) 과제는 넣지 않음. 2초·16초 짜리 2건은 내용 없음</li>
    <li>10-17 녹음 없음(10/18 06:41 조회)</li>
    <li>10-16 녹음 8건(10/17 06:40 조회): 일십백천 수강생(소송 건, 익명) 10기 상담(29분) · 최보라·뿌요 물류 미팅(77분) · [OneCrew] 정복녀 대표님 찐초보 7기(30분) · [OneCrew] 최은봉 대표님(59분) · '좋아하는 사람' 4건(읽지 않음). 컨설팅 녹음의 고객(대표님) 과제는 넣지 않고 컨설턴트·공동 Action Item만 노션 새 항목 4건으로(정복녀 링크 전달 10/20·세션 10/23 · 최은봉 스토어 이관 지원 10/21 · 일십백천 수강생 다음 컨설팅 10/23 — 10/20은 추정). 물류 미팅 Action Item은 관리자·실무자 담당(루크 몫 없음)이라 넣지 않음 — 월요일(10/19) 적체 공동 정리·화요일까지 정상화 목표만 기록. 10-15·10-14 녹음 없음. 10-13 녹음: 박태경 원크루 6회차(90분) — 대표님 과제는 대표님 몫, 컨설턴트·공동 Action Item(다음 주 현장 작업 세션·7회차 점검)만 노션 새 항목 1건(기한 10/20은 추정). 10-12 녹음 2건: 2차 PPT 피드백/리허설(64분) — 실행·작업 계획 중 루크 몫을 노션 새 항목 1건으로(기한 10/24는 추정) · 법무사 상담(33분) — 사업자 서류 부분(재방문·사업자등록증 사본·정관·회의록 재작성)만 노션 새 항목 1건, 같은 녹음의 개인 법률 문제는 반영하지 않음</li>
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
  <ul><li>전체 항목의 할 일·기한·상태·[결정] (11/13 06:41 조회). 미완료·기한 있는 항목은 일정에, 최근 7일 새 항목은 우선순위에 반영. 목표가 '사업 외 개인'인 항목은 넣지 않음(상표권 제외)</li>
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
  <li>10/12 갱신(10/11 갱신 기록은 없음): 일정에 있던 항목 중 완료로 바뀐 것 1건 제거(키티티 계약 10/8) · 노션에서 제목이 바뀐 1건 수정(박종혁 본부장 협업 — 다섯 칸 → 10월에 정할 세 칸, 기한 10/16 그대로) · 10/10~10/11에 노션에 새로 생긴 기한 항목은 모두 '사업 외 개인'이라 일정에 넣지 않음 · 플라우드 10/11 녹음(키티티 사이트 피드백)에서 노션 새 항목 2건(웨딩 페이지 문구 다시 쓰기 · AI 가상 메이크업 '가상 체험' 재설계, 기한 10/31은 추정)을 만들어 일정에 추가 — 같은 녹음의 개인 용무는 반영하지 않음 · 플라우드 10/10 메모(미용업 무료 정산 프로그램 구상)는 담당·기한이 없어 노션에 넣지 않음 · 우선순위 '새 항목'에 4줄 추가(일십백천 강의실 아임웹 로그인 · 키티티 검색 등록 · 키티티 사이트 피드백 2건 · 수익화전략 숫자 확인), 10/3·10/4 등록 11줄은 일반 줄로, 완료된 2줄(키티티 계약 · 수익화전략 02~10번 주제 확정) 제거 · 최근 [결정]에 10/10·10/11 결정 2건(수익화전략 주제 확정 · 18·24번 성과 예시) 반영 · 상황판: 노션 [보고] 10건 중 새로 옮긴 것 4건(지영 학술지 논문 발표 가이드 4건, 모두 완료) · 10/10~10/11자 직접 보고 19건(완료 17 · 판단 대기 2 — 둘 다 이후 루크 확인·[결정]으로 정리됨), 새 '막힘' 없음 — 허브 [결정 필요] 7건 그대로 · 사업 유니버스 접수 이슈 0건</li>
  <li>10/14 갱신(10/13 갱신 기록은 없음): 일정에 있던 항목 중 완료로 바뀐 것 2건 제거(법무사 선정·위임 10/12 · 신정현 대표님 인감 신고 확인+서류 3종 수령 10/12) · 노션에서 기한·제목이 바뀐 1건 수정(등기 서류 — 루크 확정 4가지·출력·날인 10/9 → 전부 출력 완료, 법무사 통화 뒤 날인·접수 10/16) · 10/13에 노션에 새로 생긴 기한 항목 3건을 일정에 추가(아임웹 자동결제 환불 10/18 · 부가세 2기 예정분 10/26 · 종소세 중간예납 11/30) · 10/12~10/13 새 항목 중 기한 없는 아임웹·일십백천 사이트 6건은 우선순위에만 · 플라우드 10/12~10/13 녹음 3건에서 노션 새 항목 3건(박태경 현장 세션 10/20 · 라이브 PPT 2차 피드백 반영 10/24 · 법무사 상담 후속 10/16 — 앞 둘의 기한은 추정)을 만들어 일정에 추가 · 우선순위 '새 항목'에 7줄 추가, 10/5·10/6 등록 28줄은 일반 줄로 · 최근 [결정]은 새 결정이 없어 그대로 · 허브: 등기 줄을 10/12 완료분 반영해 고치고 아임웹 정리 줄 추가, [결정 필요] 7건 그대로 · 상황판: 노션 [보고] 10건 중 새로 옮긴 것 0건 · 10/13자 직접 보고 5건(모두 완료), 새 '막힘' 없음 · 사업 유니버스 접수 이슈 0건</li>
  <li>10/15 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 노션에 새로 생긴 기한 항목은 10/14 2건 모두 '사업 외 개인'이라 일정에 넣지 않음 · 기한·제목이 바뀐 항목 없음 · 플라우드 10/13~10/14 녹음은 박태경 6회차 1건뿐이고 10/14 갱신에서 이미 반영 → 노션 새 항목 0건 · 우선순위 '새 항목' 창을 10/8~로 올려 10/6·10/7 등록 27줄은 일반 줄로(새 줄 없음) · 최근 [결정]은 새 결정이 없어 그대로(최신 10/11) · 허브: 박종혁 질문(10/14)은 기한 지남 표시, 4대보험 소재지 변경(10/15) 추가, 등기 카드 표기를 10/16으로 · 상황판: 노션 [보고] 11건 중 새로 옮긴 것 0건 · 10/14자 직접 보고 0건, 새 '막힘' 없음 — [결정 필요] 7건 그대로 · 사업 유니버스 접수 이슈 0건</li>
  <li>10/16 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 노션에 새로 생긴 항목은 10/14~10/15 2건 모두 '사업 외 개인'이라 일정·우선순위에 넣지 않음 · 기한·제목이 바뀐 항목 없음 · 플라우드 10/14~10/15 녹음 없음 → 노션 새 항목 0건 · 우선순위 '새 항목' 창을 10/9~로 올려 10/8 등록 6줄은 일반 줄로(새 줄 없음) · 최근 [결정]은 새 결정이 없어 그대로(최신 10/11) · 허브: 등기 제출·박종혁 세 칸을 '10/16 오늘'로, 4대보험 소재지 변경(10/15)은 기한 지남 표시 · 상황판: 노션 [보고] 11건 중 새로 옮긴 것 0건 · 10/15자 직접 보고 0건, 새 '막힘' 없음 — [결정 필요] 7건 그대로 · 사업 유니버스 접수 이슈 0건</li>
  <li>10/17 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/16에 노션에 새로 생긴 항목 22건 중 기한 있는 사업 항목 10건을 일정에 추가(지영 서포트 운영 6건 · 키티티 토탈샵 계약 후속 2건 · 최은봉 7회차 자료 10/18 · 최은봉 당근 광고 10/31) — '사업 외 개인' 10건(데이트·힐튼 설명회·대여·글램핑 등)과 기한·P 없는 1건은 넣지 않음 · 기한·제목이 바뀐 항목 없음 · 플라우드 10/16 녹음 4건에서 노션 새 항목 4건(정복녀 링크 전달 10/20·세션 10/23 · 최은봉 스토어 이관 지원 10/21 · 일십백천 수강생 다음 컨설팅 10/23) → 일정 402 → 416 · 우선순위 '새 항목' 창을 10/10~로 올려 10/9 등록 5줄은 일반 줄로, 새 줄 7개 추가 · 최근 [결정]에 10/16 '지영 서포트 모드 전환' 추가 · 허브: 변경등기 제출·박종혁 세 칸(10/16)은 기한 지남 표시, 원크루 두 대표님 이번 주 항목 추가, 무료 라이브 D-8 · 상황판: 노션 [보고] 11건 중 새로 옮긴 것 0건 · 10/16자 직접 보고(원크루 새 회차 세 건) 1건은 다른 세션이 push · 새 '막힘' 없음 — [결정 필요] 7건 그대로 · 사업 유니버스 접수 이슈 0건</li>
  <li>10/18 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건 제거(변경등기 제출 10/16 — 허브·우선순위 줄은 남은 사업자등록 정정신고로 바꿈) · 노션에서 기한이 바뀐 1건 수정(사업자등록 정정신고 10/16 → 10/23) · 10/17에 노션에 새로 생긴 항목 20건 중 기한 있는 사업 항목 7건을 일정에 추가(식스 엔진 7건 — 1주 목표 10/25 · 객단가 확정 10/24 · 500명 자산 확인 10/24 · 전자책+독서 10/31 · 500명 고가 전환 10/31 · 1달 목표 11/17 · 1분기 실측 2027-01-31) · '사업 외 개인' 7건(데이트·여행)·기한 없는 4건(심화 자료 숫자 확인은 우선순위에만)·완료 6건은 넣지 않음 · 최근 [결정]에 10/17 2건(식스 엔진 체계 · 도구공방 기본 사이트) 추가 · 우선순위 새 항목 창 10/11~, 10/10 등록 2줄은 일반 줄로 · 플라우드 10/17~10/18 녹음 없음 · 노션 [보고] 새 이관 0건 · 유니버스 이슈 0건</li>
  <li>10/19 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 10/18에 노션에 새로 생긴 항목 22건 중 기한 있는 미완료 사업 항목 12건을 일정에 추가(박종혁 합류 첫 미팅 10/21 · 일십백천 컨설팅 질문 10/23 · 주간 고정 일정·인스타 계정 구조·헤어 공급처 결정·권리금 부속 합의 10/25 · 네일 세트 비교표 10/31 · 브랜딩 초안 11/15 · 주말 발품 11/22 · 전원 직원 손익·초기 투자 재계산·급여 기준 11/30) · 플라우드 10/18 녹음 Action Item 3건 노션 신규 등록 후 일정 추가(11/15 추정) · 완료 6건([결정] 4건 · 영업 자료 · 헤어 공급처 페이지 발행)·기한 없는 4건은 일정 제외 · 우선순위 새 항목 창 10/12~(10/11 등록 3줄은 일반 줄로), 새 묶음 5줄(P0 식스 엔진 주간 배치 · P0 토탈샵 이번 주 · P1 토탈샵 11월 · P1 일십백천 후속 · P1 원크루 영업 자료 숫자) · 최근 [결정]에 10/18 4건, 10/16·10/11 2건 빠짐 · 허브: P0 제목 ~10/25, 토탈샵 이번 주 항목 신설, 식스 엔진 줄에 합류일 10/21 확정 반영, 무료 라이브 D-6 · 상황판: 노션 [보고] 새 이관 0건(10/10 이후 새 [보고] 없음), 새 막힘 0 · 유니버스 이슈 0건</li>
  <li>10/20 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/19에 노션에 새로 생긴 항목 11건 중 기한 있는 미완료 사업 항목 3건을 일정에 추가(역직구 첫 판매 마켓 결정 10/25 · 파일럿 SKU 선정 11/16 · 수동 파일럿 11/30) — [결정] 1건·완료 개발 보고 4건·기한 없는 2건(고려대 거울 광고는 우선순위에만, 뽀요·디노님 가입은 P 없음)은 일정 제외 · 플라우드 10/19 녹음 3건에서 노션 새 항목 10건 → 일정 437 → 450 · 우선순위 새 항목 창 10/13~(10/12 등록 1줄은 일반 줄로), 새 묶음 5줄(P0 역직구·라이브 기획 후속·박종혁 첫 출근 / P1 거울 광고·신정현 회의 루크 몫) · 최근 [결정]에 10/19 역직구 운영 원칙 추가, 10/17 식스 엔진 체계 빠짐 · 허브: 역직구 이번 주 항목 신설, 무료 라이브 줄에 10/23 리허설·FAQ·출연 수강생 연락 반영, 박종혁 줄에 10/21 출근 준비, 무료 라이브 D-5 · 상황판: 노션 [보고] 새 이관 0건(10/10 이후 새 [보고] 없음), 새 막힘 0 — 10/19 다른 세션 직접 보고 4건(운송장 읽기·로그인 도와주기·운영자 승인제) · 유니버스 이슈 0건</li>
  <li>10/21 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/20에 노션에 새로 생긴 항목은 완료 보고 3건(추석특강 열기 · 배송지연 클레임 수강생 자료 · 명단 일괄 적용 — 클로드 코드가 상황판에 직접 push, 기한 없음)뿐이라 일정 변동 없음(450건 유지) · 플라우드 10/20 녹음 없음 · 노션 [보고] 새 이관 0건 · 유니버스 이슈 0건 · 우선순위 새 항목 창 10/14~(10/13 등록 4줄 — 아임웹 정리·부가세 예정신고·강의실 영상 주소·종소세 중간예납 — 은 일반 줄로) · 허브 무료 라이브 D-4, 박종혁 본부장 합류 미팅·첫 출근 당일 표기</li>
  <li>10/22 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/21에 노션에 새로 생긴 항목 33건 중 기한 있는 미완료 사업 항목 9건을 일정에 추가(민트(박종혁) 계약 관련 6건 — CAC 확정·계약서 초안·계정 법인 명의·요약본·입력 폼 10/21, 네 가지 회신 10/23, 용역비 1회차 11/20 · 맥 배포 대기 2건 10/31) · 기한 없는 11건(전략 재점검 6건·변호사 검토·최종본·지메일 커넥터·아이디어 점검 2건)은 우선순위 새 항목에만 · 완료 9건([결정] 2건·원크루 책장·박태경 7회차 3건·식품값 전자책·글 쓰는 법·예약시스템)과 P 없는 2건(위수탁 계약서·카드뉴스)은 제외 · 플라우드 10/21 녹음 4건 → 박태경 공동 Action Item 2건 노션 신규(10/27·10/28) → 일정 450 → 461 · 우선순위 새 항목 창 10/15~(10/14 등록 3줄 — 박태경 현장 세션·라이브 PPT 2차·법무사 후속 — 은 일반 줄로), 새 묶음 5줄(P0 아이디어 점검 / P1 민트 계약·전략 재점검·맥 배포 2건·박태경 후속) · 최근 [결정]에 10/21 민트 2건 추가, 10/18 일십백천·10/17 도구공방 빠짐 · 허브: 맨 위에 [결정 필요] Supabase 로그인(10/21 상황판 '막힘') 신설, 식스 엔진·박종혁 줄에 10/21 [결정]·계약서 반영, 최은봉 줄에 소명 메일 발송·천안 사업자등록, 무료 라이브 D-3 · 상황판: 노션 [보고] 새 이관 0건(10/10 이후 새 [보고] 없음), 10/21 클로드 코드 직접 push 3건(아이디어 점검 '막힘' · 글 쓰는 법 100가지 · 식품값 전자책) · 유니버스 이슈 0건</li>
  <li>10/23 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/22에 노션에 새로 생긴 항목 5건은 완료 3건(자주 묻는 것 페이지·고객관리 자료·카드 할인 안내 — 클로드 코드가 상황판에 직접 push)과 P·기한 없는 2건('⚠️ Vercel 요금제 올리기' · 원크루 33번)이라 일정 변동 없음(461건 유지) · 미완료+기한 508건 중 일정 밖 67건은 전부 사업 외 개인·시작 전 [결정]·비트윈 앨범(의도된 제외)임을 재확인 · 플라우드 10/22 녹음 3건에서 노션 새 항목 0건 · 우선순위 새 항목 창 10/16~(10/15 등록 줄 없음 → 이동 없음), 새 줄 0 · 최근 [결정] 변동 없음 · 허브: 맨 위에 [결정 필요] 호스팅(Vercel) 계정 차단(10/23 상황판 '막힘' 2건) 신설 → [결정 필요] 9건, 초월스토리 10/22 묶음 기한 지남 표시, 사업자등록 정정신고·정복녀 세션 오늘(10/23) 표기, 무료 라이브 D-2 · 상황판: 노션 [보고] 새 이관 0건(10/10 이후 새 [보고] 없음), 10/22~10/23 클로드 코드 직접 push 5건(막힘 2 = 호스팅 계정 차단 · 완료 3) · 유니버스 이슈 0건</li>
  <li>10/24 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/23에 노션에 새로 생긴 항목 33건 중 기한 있는 미완료 사업 항목 21건을 일정에 추가(목표 달성 브랜드 채널 3건 10/25·10/31·11/30 · 저가 상품 10/31 · [결정 필요] 연애상담 코스 정지 10/31 · 메이븐 정산 3건 · 민트 협업 6건 10/30·10/31·11/6 · 초월스토리 2건 10/31·11/5 · 돈벌쥐 PD 4건 10/24·11/5 · 도구공방 1월 수입 11/30) + 플라우드에서 만든 6건 = 461 → 488건 · 완료 [결정] 6건(배분 구조 2건·메이븐 5기·브랜드 채널 2건 + 10/21 B안)으로 최근 [결정] 교체 · 완료 7건(원크루 33번·Vercel Pro 전환·사이트 7곳 복구·후기 추가 등)과 P 없는 3건(Vercel 2FA·화면 새로 그리기·후기 동의)은 일정 제외 · 허브: 맨 위 [결정 필요] 호스팅 차단은 10/23 Pro 전환으로 해결돼 제거([결정 필요] 8건) · 돈벌쥐 PD·메이븐 정산·브랜드 채널·물류 보고 체계 줄 신설 · 정정신고 10/23 지남, 정복녀 10/23 세션 결과, 박종혁 10/23 회의 2건, 인베이더 지속 여부, 무료 라이브 D-1·장표 수정 회의 반영 · 우선순위 '새 항목' 창 10/17~(10/16 등록 4줄은 일반 줄로, 새 줄 9) · 상황판: 노션 [보고] 새 이관 0건 · 유니버스 이슈 0건</li>
  <li>10/25 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/24에 노션에 새로 생긴 항목 11건(모두 클로드 코드가 등록) 중 기한 있는 미완료 사업 항목 1건을 일정에 추가(최은봉 8회차 자료 맥 배포 10/26) — 완료 8건(전자책·후기·스태프 공지·오프라인 강의 자료 3건·강의 이벤트·정복녀 7회차 자료)과 P·기한 없는 2건(52주 추천상품 페이지)은 제외 · 플라우드 10/24 아침 메모 1건에서 노션 새 항목 2건(촬영 출장 계약 조건 · 헤어팀 보상안, 10/31 추정) → 일정 488 → 491건 · 미완료+기한 536건 중 일정 밖 67건은 전부 의도된 제외(변동 없음) · 우선순위 새 항목 창 10/18~(10/17 등록 6줄 — 최은봉 7회차·정복녀 링크·식스 엔진 이번 주·일십백천 컨설팅·식스 엔진 이달~1분기·심화 자료 숫자 — 은 일반 줄로), 새 줄 2(P0 최은봉 8회차 · P1 토탈샵 메모 2건) · 최근 [결정] 변동 없음(최신 10/23) · 허브: 무료 라이브 오늘(D-0) 표기 · 돈벌쥐 PD 10/24 연락 결과 기록 없음 표기 · 원크루 줄에 정복녀 7회차 완료·최은봉 8회차 배포 대기 · 토탈샵 줄에 메모 2건 · [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건(10/10 이후 새 [보고] 없음), 10/24 클로드 코드 직접 push 3건(강의 이벤트·사진 안내·크루 교육자료 2건) · 유니버스 이슈 0건</li>
  <li>10/26 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/25에 노션에 새로 생긴 항목 23건 중 기한 있는 미완료 사업 항목 2건을 일정에 추가(테라피님 가격관리 실사용 확인 10/25 · 테라피님 CS 응대 템플릿 10/31) — 완료 14건(테라피님 가이드북 · 루크 툴박스 라이브 준비 보고 12건 · 심수현님 5기 변경)과 P·기한 없는 진행 중 5건(CS 템플릿 문구 검토·발급처 주소·방송 계정 카드 문구·PDF 표지 문구·영상 클립 7개)은 제외 · 플라우드 10/25 라이브 녹음 1건에서 노션 새 항목 0건 → 일정 491 → 493건 · 미완료+기한 540건 중 일정 밖 69건은 전부 의도된 제외(67건 + 위 2건 반영 전 기준) · 우선순위 새 항목 창 10/19~(10/18 등록 5줄 — 식스 엔진 주간 배치·토탈샵 오픈 준비·토탈샵 11월 준비·일십백천 재평가 후속·원크루 영업 자료 — 는 일반 줄로), 새 줄 2(P0 테라피님 인터뷰 준비 · P1 CS 응대 템플릿) · P0 제목 '~11/1' · 최근 [결정] 변동 없음(최신 10/23) · 허브: 무료 라이브 줄을 결과 확인 줄로(정규 과정 11/6 시작 안내 기록), 식스 엔진 1주 목표·토탈샵·역직구 10/25 기한 줄은 지난 주 결과 확인으로, [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건 · 10/25 클로드 코드 직접 보고 12건(모두 완료, 막힘 0) · 유니버스 이슈 0건</li>
  <li>10/27 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/26에 노션에 새로 생긴 항목 3건(키티티 배너, 모두 클로드 채팅 등록) 중 기한 있는 미완료 2건을 일정에 추가(캔바 편집본 레이어 분리 11/1 P0 · 40×10cm 배너 제작·인쇄 입고 10/31 P1) — 완료 1건(배너 캔바 편집본 40x10cm, 캔바 편집 주소 확보)은 제외 · 플라우드 10/25~10/27 범위 녹음은 10/25 라이브 본편뿐 → 노션 새 항목 0건 → 일정 493 → 495건 · 미완료+기한 542건 중 일정 밖 67건은 전부 의도된 제외(변동 없음) · 우선순위 새 항목 창 10/20~(10/19 등록 2줄 — P0 역직구 위너 시스템 · P1 고려대 거울 광고 — 은 일반 줄로), 새 줄 2(P0 배너 캔바 편집본 · P1 배너 제작) · 최근 [결정] 변동 없음(최신 10/23) · 허브: 최은봉 8회차 맥 배포 '10/26 오늘' → 기한 지남 표기, 월요일 정기 라이브 첫 회(10/26) 진행 기록 없음 표기, 박태경 성과 평가·물류 18:30 브리핑 '10/27 오늘', 토탈샵 줄에 배너 2건, 돈벌쥐 PD 연락 결과 10/27 기준 기록 없음, [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건(10/10 이후 새 [보고] 없음) · 10/26 클로드 코드 직접 보고 0건 · 유니버스 이슈 0건</li>
  <li>10/28 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/27에 노션에 새로 생긴 항목 13건(모두 클로드 코드·채팅 등록)은 완료 9건(루크 툴박스 6기 등록·자료 잠금·가입 예약 명단 등 7건 · 키티티 배너 [완료] 2건)과 P·기한 없는 미완료 4건(금요일 본강의 뒤 6기 자료 열기 2건 · 영상 구간 7개 올릴 곳 · 재수강 자동 처리)이라 일정에 넣지 않음 · 플라우드 10/27 김종진 대표님 10기 세션(56분)에서 루크 Action Item 없음 → 노션 새 항목 0건 → 일정 495건 유지 · 미완료+기한 542건 중 일정 밖 67건은 전부 의도된 제외(변동 없음) · 우선순위 새 항목 창 10/21~(10/20 등록 3줄 — P0 라이브 기획 회의 후속·박종혁 첫 출근 · P1 신정현 회의 루크 몫 — 은 일반 줄로), 새 줄 0 · 최근 [결정] 변동 없음 · 허브: 물류 보고 양식·박태경 성과 평가 '오늘' 표기 정리, 토탈샵 배너 10/27 완료 2건 반영, 라이브 줄에 10/27 직접 보고 6건 · 상황판 [보고] 이관 0 · 유니버스 이슈 0</li>
  <li>10/29 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/28에 노션에 새로 생긴 항목 1건('425마켓-힐링디어스 위수탁 계약서 작성', P·기한·목표 없음)은 일정·우선순위에 넣지 않음 · 플라우드 10/28 녹음 3건(정복녀 7기 2건 · 최은봉) 루크 Action Item → 노션 새 항목 8건 → 일정 495 → 503건 · 미완료+기한 542건 중 일정 밖 67건은 전부 의도된 제외(변동 없음) · 우선순위 새 항목 창 10/22~(10/21 등록 4줄 — P0 원크루 아이디어 점검 · P1 민트 계약 묶음·전략 재점검·맥 배포 2건 — 은 일반 줄로), 새 줄 5(P0 2 · P1 2 · P2 1) · 최근 [결정] 변동 없음 · 허브: 초월스토리 줄에 10/28 세션 후속 6건·협업 모델 확정(10/29), 원크루 두 대표님 줄에 최은봉 10/28 세션(정품 소명 종결·위수탁 소명 연장 대기)·박태경 공동 상품 찾기 세션 진행 기록 없음, 민트 주간 회의 첫 회 진행 기록 없음 · 상황판 [보고] 이관 0 · 유니버스 이슈 0</li>
  <li>10/30 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·우선순위가 바뀐 항목 1건(상표 출원 대행 견적·지정상품 초안 10/29 P1 → 11/1 P0 진행 중) · 10/29에 노션에 새로 생긴 항목 4건 중 기한 있는 미완료 2건 추가(지영 원장 영업신고증·면허 확인+위생과 문의 11/5 P0 · 특허고객번호 신청+사용 증거 수집 11/1 P0) → 일정 503 → 505건, [보고] 1건(토탈샵 전환 영업신고 정리, 완료)은 상황판 이관, 다낭 여행 1건은 사업 외 개인이라 제외 · 미완료+기한 552건 중 일정 밖 67건은 전부 의도된 제외(변동 없음) · 플라우드 10/29 녹음 없음 · 우선순위 새 항목 창 10/23~(10/22 등록 1줄 — P1 박태경 10/21 세션 후속 — 은 일반 줄로), 새 줄 2(P0 상표 출원 · 토탈샵 전환 영업신고) · 최근 [결정] 변동 없음 · 허브: 토탈샵 줄에 10/29 새 항목 2건·[보고] 1건, 10/29 기한(초월스토리 협업 모델 옵션·최은봉 9회차 발행·사진 재촬영 컨셉보드) 지남 표기, 페이지 목록에 상표 출원 설계안·토탈샵 영업신고 정리 추가 · 상황판 [보고] 이관 1 · 유니버스 이슈 0</li>
  <li>10/31 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/30~10/31 새벽에 노션에 새로 생긴 항목 19건(완료 13건 — 6기 강의 서포트 페이지 /class · 꼬리물기 도구 3건 · 1주차 녹화 분할·챕터 83개 · 인계본 전수 분석 · [결정] 메일 주소 노출 · 팔찌(사업 외 개인) 등) 중 기한 있는 미완료 사업 항목 1건(신규 수강생 환영 메시지 10/31 P1)을 일정에 추가 · P 있고 기한 없는 4건(자동등록 전면 개편 P0 · 자동소싱 인수 2건 · 1주차 덱별 영상 업로드 P0)은 우선순위에만 · 플라우드 10/30 민트·돈벌쥐 PD 미팅 → 노션 새 항목 5건을 일정에 추가 → 505 → 511건 · 미완료+기한 553(새 5건 전) · 완료 486 · 상황판 [보고] 이관 0, 클로드 코드 직접 보고 7건(모두 완료) · 유니버스 이슈 0</li>
  <li>11/1 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 10/31 새벽~밤 노션 새 항목 16건(완료 4건 — 6기 1주차 편집본 완성(루나) · 자동소싱 v4.94 배포본 · 배포 저장소 공개 · 코칭 화면 실명 가리기 / 진행 중·시작 전 12건은 모두 기한 없음 — P0 있는 10건은 우선순위에만(6기 1주차 영상정리 루나 5건 · 편집본 업로드 루크 2건 · 자동소싱 v4.95·v4.96 루나 2건 · 로그인 한 판 루크 1건) · P 없는 2건(무료 공개용 5분 영상 3편 · 3주 집중 코칭 신청 화면)은 허브에만) · 플라우드 10/31 초월스토리 회의 → 노션 새 항목 19건을 일정에 추가 → 511 → 530건 · 미완료+기한 558(새 19건 전) · 완료 490 · 상황판 [보고] 이관 0, 클로드 코드 직접 보고 2건(코칭 신청 화면·실명 가리기, 모두 완료) · 유니버스 이슈 0</li>
  <li>11/2 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 11/1 노션 새 항목 4건은 모두 완료(코칭 모집 화면 3건 · 6기 강의 서포트 같이 듣는 분 명단 — 클로드 코드가 상황판에 직접 push, P·기한 없음)라 일정 변동 없음(530건 유지) · 미완료+기한 577 · 완료 494 · 플라우드 11/1 녹음 2건은 개인 녹음·4초 녹음이라 노션 새 항목 0건 · 우선순위 새 항목 창 10/26~(10/25 등록 3줄 — P0 테라피님 인터뷰 준비 · P1 키티티 촬영 출장 계약·헤어팀 보상안 · P1 테라피님 CS 템플릿 — 은 일반 줄로), 새 줄 없음 · P0 제목 ~11/8, 허브 식스 엔진 줄 '이번 주' → 지난 주 결과 확인 · 11/1 기한 6건(상표 특허고객번호·대행 견적 · 배너 캔바 편집본 · 설치·자동등록 가이드 · 촬영 일정 공동 기획 · 초월 계약서 초안) 모두 노션 미완료 — 허브에 기한 지남 표기 · 최근 [결정] 새 것 없음(최신 10/31) · 상황판 [보고] 이관 0(노션 [보고] 11건 전부 피드에 있음), 직접 보고 4건 모두 완료, 막힘 0 · 유니버스 이슈 0</li>
  <li>11/4 18:40 추가 갱신(채팅 '스스로 월백 리턴즈 관리'): 공유 회의록 3페이지(/meetings/ · /min1030/ · /min1104/) 대조 → 노션 완료 6건(다마고치 포맷·12월 착수·송출 채널 — 11/4 결정, 주간 정기회의 첫 회 — 11/4 진행, 채널 개설 중복 1건 정리) · 기한·우선순위 변경 4건(1/20 정합 11/2→11/11 · PD 보상 11/4→11/11 · 촬영비 7항목 11/4→11/9 P0 · 첫 에피소드 촬영 준비 11/15→11/9 P0) · 새 항목 9건(장소 확정·면접관 섭외 확인·상금 분배·광고 예산·회차별 구성·가편→업로드 + [결정] 3건) · 11/4 낮 다른 채팅이 만든 '스스로 월백' 항목 12건 포함해 일정 추가 · 프로젝트명 '스스로 월백 리턴즈'로 통일 · 허브 새 줄 '스스로 월백 리턴즈'</li>
  <li>11/11 19:10 추가 갱신(채팅 '스스로 월백 리턴즈 관리'): 11/11 정기회의 의결(민트님 단톡방 공지 3건 + 루크 확인) + 11/9 모집영상 촬영 완료 → 노션 완료 12건(촬영 일정·장소·면접관·콘티·1화 촬영 준비·질문 소재·촬영비 7항목·촬영비 공유 2건·PD 보상·배분 전 고지·장기 비율) · 기한·제목 변경 8건 · 새 항목 5건(카카오 채널 · 경비 일괄 입금 · 순수익 정의 · 신청서·CRM 확인 · [결정] 11/11) → 일정 정리 · 공유 회의록 min1111/ 신설(배분·입금 수치는 제외)</li>
  <li>11/13 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음(미완료+기한 392 중 일정 밖 14건 = 의도된 제외 8 + 데이트 준비 3 + 명동 일정 1 + 11/12 등록 개인 2(과태료 납부 · 컨디션 회복, 목표 '사업 외 개인')) · 11/12 노션 새 항목 5건: 완료 2(= 11/12 직접 보고 2건, 자동소싱 맥 설치판) · 개인 3([결정] 데이트 식당 페이지 포함) → 일정·우선순위 추가 없음, 최근 [결정]은 사업 결정이 없어 그대로 · 플라우드 11/12 녹음 2건(세무사 상담 134분 · 개인 메모 58초)에서 토탈샵 세무사 상담 후속 → 노션 새 항목 3건(11/30 P1, 기한 추정) → 일정 395 → 398 · 우선순위 새 항목 창 11/6~(11/5 등록 8줄은 일반 줄로 — P0 가을 3주 코칭·메이브님 통화·토요일 상담 통화·자동등록 테스트판 2건 / P1 박태경 런칭 3건·가을 소명자료·돈벌쥐 PD 에이전시 / P2 1월 신규 강의 런칭), 새 줄 1(P1 토탈샵 세무사 상담 후속 3건 묶음) · 허브: 키티티 토탈샵 줄에 11/12 세무사 상담 요지·새 항목 3건, 변경등기 줄 '세무사 미팅 진행됨(법인 안건은 확인 필요)', 툴박스 줄에 11/12 직접 보고 2건(맥 설치판) · [결정 필요] 11건 그대로 · 상황판: 노션 [보고] 12건 전부 피드에 있음(이관 0), 11/12 직접 보고 2건(완료, 막힘 0) · 유니버스 이슈 0</li>
  <li>11/12 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음(미완료+기한 387 중 일정 밖 12건 = 의도된 제외 8 + 데이트 준비 3 + 11/11 등록 '11/12 명동 일정'(목표 '사업 외 개인') 1 — 그 항목의 14:00 세무사 미팅 시각만 허브·일정 제목에 반영) · 11/11 노션 새 항목 7건: 11/11 저녁 채팅의 스월백 5건(이미 반영 — [결정] 1 완료·기한 4건)·개인 2건(DVD 구매 P3·명동 일정) → 일정·우선순위 추가 없음 · 플라우드 11/11 녹음 2건(물류 역할 논의 77분 · 루크 메모 26초)에서 회사 몫 Action Item → 노션 새 항목 3건(P0 2 · P1 1, 기한 추정) + 전체 회의 소집 기한 11/20 → 11/17(화) 수정 → 일정 392 → 395 · 우선순위 새 항목 창 11/5~(11/4 등록 9줄은 일반 줄로 — P0 자동소싱 주소값·300억 P0 3건·코칭 P0 5건·저장소 분리 / P1 물류 수익 배분·수강 신청자 확인·코칭 P1 5건·주소값+비밀번호 / P2 물류 파트너 이사 등재), 새 줄 3(P0 물류 현장 검증·가을님 자료 / P1 창고·전산 단순화) · 최근 [결정]은 11/11 결정이 전날 저녁에 이미 올라가 그대로 · 허브: 물류팀 보고 체계·초월스토리·변경등기(세무사 14:00) 줄 갱신 · 상황판 [보고] 이관 0건(노션 [보고] 12건 전부 피드에 있음) · 11/11 직접 보고 0건 · 유니버스 이슈 0건</li>
  <li>11/11 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음(미완료+기한 386 중 일정 밖 11건 = 의도된 제외 8 + 데이트 준비 3, 그대로) · 11/10 노션 새 항목 2건은 모두 완료(11/10 직접 보고 2건과 같음 — 원크루 사이트 공개 34번 긴 칼럼 · 꼬리물기 카드 할인 셈 수정, P·기한 없음) → 일정·우선순위 변동 없음 · 플라우드 11/10 녹음 3건(상담 30분 · 운영 회의 70분 · 물류 현안 진단 74분)에서 루크 몫 Action Item → 노션 새 항목 8건(P0 3 · P1 4 · P2 1, 기한 전부 추정) → 일정 392 → 400 · 우선순위 새 항목 창 11/4~(11/3 등록 6줄은 일반 줄로 — P0 돈벌쥐 PD 후속·가을 계약서 후속 6건 / P1 돈벌쥐 PD 후속 3건·가을 계약서 P1 2건·키티티 링크 홈 / P3 [보류] 가을 최소 보장), 새 줄 4(P0 물류 3건 묶음 · P1 물류 3건 묶음·복수 플랫폼 · P2 재상담 확인) · 최근 [결정]은 새 결정이 없어 그대로 · 허브: 물류팀 보고 체계·스월백(11/9 촬영 언급은 확인 필요)·셀러 멤버십·초월스토리·인베이더·툴박스·문의 대응 줄에 11/10 회의·보고 요지 · 상황판 [보고] 이관 0건(노션 [보고] 12건 전부 피드에 있음) · 11/10 직접 보고 2건(모두 완료, 막힘 0) · 유니버스 이슈 0건</li>
  <li>11/10 갱신: 일정에 있던 항목 중 완료로 바뀐 것 2건 제거 — 식스 엔진 1달 목표(~11/17, 11/9 노션 완료) · [결정 필요] 연애상담 코스·앱 제작 정지 여부(10/31, 11/9 노션 완료) → 394 → 392 · 우선순위에서 완료 항목 줄 2개 제거(연애상담 [결정 필요] · 10/21 전략 재점검 루크 몫 6건) · 기한·제목이 바뀐 항목 없음(미완료+기한 386 중 일정 밖 11건 = 의도된 제외 8 + 데이트 준비 3, 기준선 그대로) · 11/9 노션 새 항목 0건(11/9 06:41 뒤 등록된 것은 그날 실행이 만든 2건뿐) · [결정] 새 항목 없음 · 플라우드 11/9 녹음 2건은 개인 메모 → 노션 새 항목 0건 · 우선순위 새 항목 창 11/3~(11/2 등록 3줄을 일반 줄로 이동: P0 멘토루크 예약시스템 · P1 돈벌쥐 PD 후속 6건 · P2 애드센스 실적) · 상황판 [보고] 이관 0 · 유니버스 이슈 0</li>
  <li>11/9 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음(11/7 대정리 뒤 기준선 그대로: 미완료+기한 386 중 일정 밖 11건 = 의도된 제외 8 + 데이트 준비 3) · 11/8 노션 새 항목 25건: 완료 6건([결정] 5 — 화장품 도매 창고 컨셉·'가을' 호칭 폐기 / 임원전용 사이트 Cloudflare / 바코드 통합 재고 / 13시 이후 출고 취소 불가 / 입고 동선 — + 개인 1) · '사업 외 개인'(데이트 준비) 3건 제외 · 기한 있는 미완료 16건 일정 추가 — 가을 대표님 강의 런칭 P0 7건(11/15)·P1 4건(11/30) · 물류·3PL P0 1건(리나님 역할 재정의 11/15)·P1 3건(11/30) · 임원전용 사이트 배포 마무리(11/15 P0) · 플라우드 11/7 녹음 → 노션 새 항목 2건(세무사 미팅 11/12 P0 · 업체 미팅 11/19 P1) → 일정 376 → 394 · 최근 [결정] 5건 교체 · 우선순위 창 11/2~(11/1 등록 4줄 일반 줄로 이동, 새 줄 P0 4·P1 3) · P0 제목 ~11/15, P1 제목 ~11/30 · 허브: 임원전용 사이트 줄 신설, 초월스토리·물류·법인·토탈샵 줄에 11/8 요지, 식스 엔진 줄 한 주 밀기 · [결정 필요] 11건 그대로 · 상황판 [보고] 이관 0 · 유니버스 이슈 0</li>
  <li>11/8 갱신: <b>11/7 낮 액션보드 대정리 반영</b> — 루크가 노션 미완료 896건 중 329건을 휴지통으로 이동(30일 복구 가능 · '나중에 할 안건' 페이지 95건) → 일정에 있던 항목 중 노션에서 사라진 239건을 일정에서 제거(599 → 360), 우선순위 페이지에서 같은 항목 77줄 제거, 허브 줄 3개(목표 달성 브랜드 채널 · 역직구 위너 시스템 · 아임웹 정리) 제거·4개는 남은 노션 항목으로 링크 교체 · 완료로 바뀐 기존 일정 0건 · 기한·제목 변경 0건 · 11/7 노션 새 항목 25건: 완료 8건([보고] 대정리 1 · [결정] 6 · 자동등록 v243 1) · 기한 있는 미완료 16건 일정 추가(376건) — 300억 엑시트 4(법인 전환 [결정 필요]·물류 수익 구조 [결정 필요]·보부상 사례·패시브 인컴 세션) · 인베이더 종료 대비 2(6기 수익 계산·해지계약서 검토) · 셀러 멤버십 3(파일럿 설계·충돌 규칙 [결정 필요]·[검토] 등록 대행) · 강의업체 이전 2(보험·적금 모델 구조·금융상품 제휴 전 확인) · 스월백 3,000만 회수 계산 · 가을 런칭 기획 · 창고 택배비 결제 분리 결정 · 쇼츠 퍼널 테스트 · [검토] 저축 챌린지 · P3 기한 없는 1건(youtube-agent-skill)은 우선순위에만 · 미완료+기한 367 중 일정 밖 8건은 의도된 제외('사업 외 개인' 6 · 시작 전 [결정] 2) · 최근 [결정]은 11/7 6건으로 교체 · 플라우드 11/7 녹음 없음 · 상황판: [보고] 액션보드 대정리 1건 이관, 11/7 직접 보고 4건(키티티 QR·통계·GEO, 모두 완료) · 유니버스 이슈 0</li>
  <li>11/7 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 11/6 노션 새 항목 25건(11/6 06:41 조회 뒤 등록한 2건 제외 23건): 완료 17건(11/6 직접 보고 17건과 같음 — 거인의 창고 2·3판·취소·반품·마감 카운트다운·2주차 자료·접근 조이기·v241·v242) · '사업 외 개인'(데이트 준비) 3건 제외 · 기한 있는 미완료 2건 일정 추가 — 대학교 광고지 QR 유입 통계(11/14 P0) · 쇼핑몰 5곳 구매 교육자료 검토(11/30 P1) · P·기한 없는 1건(【최우선】 결제 시스템 실제 열기, 진행 중)은 허브 툴박스 줄에만 + 플라우드 11/6 심○○ 대표님 보충 통화·11/6 상담 녹음 루크 Action Item → 노션 새 항목 4건(11/6 P0·11/7 P0·11/9 P0·11/10 P1, 기한 추정) → 일정 593 → 599 · 미완료+기한 646 중 일정 밖 71건 = 의도된 제외 68건 + 오늘 제외 3건(조회 뒤 추가한 4건은 다음 날 조회에 들어옴) · 완료 563 · 최근 [결정] 변동 없음(11/5 1 + 11/4 4 + 11/3 1) · 우선순위 새 항목 창 10/31~(10/30 등록 1줄 — P0 자동등록 프로그램 전면 개편 — 일반 줄로), 새 줄 3(P0 2 · P1 1) · P0 제목 ~11/8 유지 · 허브: 툴박스 줄에 11/6 직접 보고 17건·결제 시스템 최우선·교육자료·보충 통화·상담 녹음, 11/6 기한 4건(촬영 장소·PD 식사 미팅·이○○ 세션·심○○ 보충) 지남·노션 미완료 표기 · [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건(11건 전부 피드에 있음), 11/6 직접 보고 17건(완료 16·진행 중 1, 막힘 0), 피드 268건 · 유니버스 이슈 0건</li>
  <li>11/6 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 11/5 노션 새 항목 8건(11/4 밤 플라우드 등록분 6건 제외): [결정] 1건(루크·메이브님 현 강의업체 강의 해지) · 기한 있는 미완료 4건 일정 추가 — 토요일 상담 통화(11/7 P0) · 메이브님과 통화 — 새 수익 모델(11/8 P0) · 돈벌쥐 PD 연결 에이전시 미팅(11/30 P1) · 1월 신규 강의 런칭 준비(메이브님, 12/31 P2) · P 있고 기한 없는 2건(자동등록 v237·v239 테스트판)은 우선순위 새 항목에만 · P·기한 없는 1건(창고 사서함·재고)은 허브 툴박스 줄에만 + 플라우드 11/5 박○○ 대표님 미팅 루크 Action Item → 노션 새 항목 2건(11/7·11/15, 기한 추정) → 일정 587 → 593 · 미완료+기한 639 중 일정 밖 72건 = 10/23부터의 의도된 제외 68건 + 오늘 추가한 4건(조회 뒤 추가) · 완료 546 · 최근 [결정] 맨 위에 11/5 1건, 11/3 8% 광고비 계상 빠짐 · 우선순위 새 항목 창 10/30~(10/29 등록 7줄 — P0 코칭 알바·최은봉 9회차·상표 출원·토탈샵 전환 / P1 가을 10/28 세션 후속·최은봉 회사소개서 / P2 라이브 출연 협의 — 일반 줄로), 새 줄 6(P0 3 · P1 2 · P2 1) · P0 제목 ~11/8 유지 · 허브: 인베이더 줄에 11/5 미팅·[결정]·새 항목 6건, 툴박스 줄에 11/5 직접 보고 3건·자동등록 v237·v239, 11/5 기한 2곳(손익분기 고지·위생과 문의) 지남 표기 · [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건(11건 전부 피드에 있음), 11/5 직접 보고 3건(완료 2·진행 중 1, 막힘 0), 피드 251건 · 유니버스 이슈 0건</li>
  <li>11/5 갱신: 일정에 있던 항목 중 완료로 바뀐 것 1건 제거(민트 건 주간 정기 회의 첫 회 — 11/4 저녁 채팅에서 완료 처리) · 기한·제목이 바뀐 항목 없음 · 11/4 노션 새 항목 54건(완료 19건 = 11/4 직접 보고 14건과 같은 일 + 정복녀 9회차·박태경 8회차 교육자료·원크루 책장 2호·회의록 + [결정] 4건 / 미완료 35건 중 스스로 월백 리턴즈 17건은 11/4 저녁 채팅이 이미 일정에 넣음 · 나머지 기한 있는 사업 항목 16건 일정 추가 — 300억 엑시트 4건·코칭·자료실 9건·소싱 주소값+비밀번호·공유 저장소 결정·최은봉 9회차 / P·기한 없는 2건(키티티 스킨·예약 주소)은 허브에만) + 플라우드 11/4 녹음에서 노션 새 항목 6건(가을 3주 코칭 3 · 박태경 강의 런칭 3) → 일정 566 → 587 · 최근 [결정]에 11/4 스스로 월백 4건 추가, 11/3 1건·10/31 1건·10/23 2건 빠짐 · 우선순위 새 항목 창 10/29~(이동 줄 없음), 새 줄 8 · 허브: 300억 엑시트 새 줄 · 원크루 줄에 11/4 세션 3건 · 툴박스 줄에 11/4 직접 보고 14건·노션 등록분 · 키티티 줄에 상담 사이트 5건 · [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건(11건 전부 피드에 있음), 11/4 직접 보고 14건 중 막힘 1건(키티티 로고 파일 미전달)은 뒤이은 완료 보고로 해소, 피드 248건 · 유니버스 이슈 0건</li>
  <li>11/4 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 11/3 노션 새 항목 27건(완료 14건 = 11/3 직접 보고 7건과 같은 일 + 자동등록 v236·재생목록 대표 이미지·쇼츠 5편·키티티 리틀리형 개편 + [결정] 3건 / 미완료 13건 중 기한 있는 사업 항목 8건 일정 추가 — 가을 계약서 검토 후속 P0 6건(11/7)·수수료 요율표(11/10)·광고·운영비 상한(11/30) / '사업 외 개인' 2건(블럭마트 기업 실사·와인) 제외 / P 있고 기한 없는 3건(키티티 링크 홈 내용 · [보류] 2건)은 우선순위 새 항목에만) + 플라우드 11/3 녹음에서 노션 새 항목 4건 → 일정 540 → 552 · 최근 [결정]에 11/3 가을 계약서 3건 추가, 10/23 3건 빠짐 · 우선순위 새 항목 창 10/28~(이동 줄 없음), 새 줄 8 · 허브: 초월스토리 줄에 11/3 계약서 검토(클로드 페이지 gaeul-contract/)·노션 10건, 툴박스 줄에 11/3 직접 보고 7건·수강생 녹음 4건, 물류 줄에 11/3 물류 회의, 6기 줄에 쇼츠·강의 정리 페이지·11/3 강의, 키티티 줄에 리틀리형 개편 · [결정 필요] 8건 그대로 · 상황판: 노션 [보고] 새 이관 0건(11건 전부 피드에 있음), 11/3 직접 보고 8건 모두 완료(막힘 0), 피드 234건 · 유니버스 이슈 0건</li>
  <li>11/3 갱신: 일정에 있던 항목 중 완료로 바뀐 것 없음 · 기한·제목이 바뀐 항목 없음 · 11/2 노션 새 항목 24건(완료 14건 = 11/2 직접 보고 10건과 같은 일 + 자동등록 로그인·v235 등) 중 기한 있는 6건(돈벌쥐 PD 통화 준비 4건+[검토] 4분할 11/2 · '스스로 월백' 법인 명의 11/8)을 일정에 추가 · 플라우드 11/2 돈벌쥐 PD님 통화(44분) 루크 Action Item → 노션 새 항목 4건(11/4 P0 · 11/4 · 11/6 · 11/14, 기한 추정)도 일정에 추가 → 530 → 540 · 우선순위 창 10/27~(10/26 등록 2줄 — P0 배너 캔바 편집본 · P1 배너 제작 — 은 일반 줄로), 새 줄 5(P0 2 · P1 2 · P2 1) · 허브 돈벌쥐 PD 줄에 11/2 페이지·통화 요지, 툴박스 줄에 11/2 직접 보고 10건·수강생 녹음 4건 · 최근 [결정] 새 것 없음(최신 10/31) · 상황판 [보고] 이관 0(노션 [보고] 11건 전부 피드에 있음), 직접 보고 10건 모두 완료, 막힘 0 · 유니버스 이슈 0</li>
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

# ---------------------------------------------------------------- 식스 엔진
ENGINE = '<div class="hero">\n  <h1>식스 엔진</h1>\n  <div class="sub">6개 수익 프로젝트 · 하루 하나씩 점화 · 2026.10 ~ 2027.10</div>\n  <div class="goal">\n    <div><b>4,100~4,600만</b><span>11~12월 확보 예상</span></div>\n    <div><b>7.14억</b><span>분기 4회 돌렸을 때 연간 루크 몫</span></div>\n    <div><b>3,000명</b><span>분기마다 새로 들여올 카페 회원</span></div>\n    <div><b>1.72억</b><span>기존 회원 500명의 연 잠재력</span></div>\n  </div>\n</div>\n\n<div class="card">\n  <p style="margin:0">6기통 엔진은 실린더가 하나씩 순서대로 터지지만 <b>엔진 전체는 멈추지 않습니다.</b> 오늘 터지는 실린더가 오늘의 집중 프로젝트고, 나머지 다섯은 꺼진 게 아니라 예열 상태입니다.</p>\n  <div class="note">이름이 마음에 안 드시면 바꿉니다. \'머스크 모드\', \'1억 엔진\'도 후보였습니다.</div>\n</div>\n\n<h2>여섯 개 엔진 <small>현금 기여 순</small></h2>\n<div class="card accent">\n  <div class="pg">\n    <div class="pgn"><b>1</b><span>매일</span></div>\n    <div class="pgb">\n      <h3>멘토루크 강의 판매 <span class="tag cash">현금</span></h3>\n      <p style="margin:0 0 6px">박종혁 본부장과 공동. 카페 3,000명 모집 → 10% 전환 → 1월 자사 강의 런칭.</p>\n      <div class="kv">\n        <dt>기간</dt><dd>10월 4주차 ~ 2027년 1월</dd>\n        <dt>루크 몫</dt><dd>36% (종혁 40% · 정현 24%)</dd>\n        <dt>예상</dt><dd>분기 <b>1.78억</b> · 연 4회 <b>7.14억</b> (B안)</dd>\n        <dt>병목</dt><dd>분기마다 신규 3,000명 — 광고 900만, CAC 3,000원</dd>\n      </div>\n      <div class="emph"><b>이 하나가 나머지 다섯을 전부 합친 것보다 큽니다.</b> 그래서 로테이션에서 빼고 매일 고정 블록으로 돌립니다.</div>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn q"><b>2</b><span>화</span></div>\n    <div class="pgb">\n      <h3>신규강사 런칭 — 가을님 <span class="tag cash">현금</span></h3>\n      <p style="margin:0 0 6px">초월스토리 + 가을(정복녀) 대표님. 11월 초 촬영 → 12월 강의 → 1월 정산.</p>\n      <div class="kv">\n        <dt>루크 몫</dt><dd>PG 제외 매출의 <b>8%</b> (광고비와 무관)</dd>\n        <dt>목표</dt><dd>최소 500만원 → <b>23명</b>이면 달성</dd>\n        <dt>1억 매출 시</dt><dd><b>768만원</b></dd>\n      </div>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn q"><b>3</b><span>수</span></div>\n    <div class="pgb">\n      <h3>거인의 도구공방 — 입문 기본 사이트 <span class="tag cash">현금</span></h3>\n      <p style="margin:0 0 6px">교육 + 프로그램 판매의 <b>기본 사이트</b>. 전자책·독서 프로젝트·툴박스가 전부 여기 올라갑니다. 전자책 판매처를 따로 두지 않습니다.</p>\n      <div class="kv">\n        <dt>역할</dt><dd>카페에서 들어온 사람이 <b>처음 돈을 쓰는 자리</b></dd>\n        <dt>상품</dt><dd>전자책 3만 · 독서 프로젝트 3만/월 · 프로그램</dd>\n        <dt>다음 칸</dt><dd>본 강의 → 일십백천 · 원크루</dd>\n        <dt>선행</dt><dd>툴박스 결제 연결(포트원)</dd>\n      </div>\n      <div class="emph">엔진 3은 미지수가 아니라 <b>퍼널의 허리</b>입니다. 여기가 비면 카페에서 본 강의까지 3개월을 맨입으로 기다려야 합니다.</div>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn q"><b>4</b><span>목</span></div>\n    <div class="pgb">\n      <h3>앱 제작 및 판매</h3>\n      <p style="margin:0 0 6px">개발자 계정 3종(Apple · Google Play · Microsoft) 등록이 모든 배포의 앞단입니다.</p>\n      <div class="note">리드타임이 가장 깁니다. Apple 승인만 며칠. 현금까지 가장 먼 엔진.</div>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn q"><b>5</b><span>금</span></div>\n    <div class="pgb">\n      <h3>연애상담 코스</h3>\n      <p style="margin:0 0 6px">띠동갑 커플 콘텐츠 + 과거 300명 상담 경험을 코스로.</p>\n      <div class="note">신규 브랜드라 모객을 처음부터 쌓아야 합니다. 단, 콘텐츠 소재는 이미 있고 제작비가 거의 0입니다.</div>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn q"><b>6</b><span>토</span></div>\n    <div class="pgb">\n      <h3>정부지원사업 구축 자동화 사이트 <span class="tag p3">서브</span></h3>\n      <p style="margin:0 0 6px">루크님이 직접 \'서브\'로 두신 프로젝트입니다.</p>\n      <div class="note">다른 다섯이 막혔을 때 손대는 자리. 여기에 시간을 당겨 쓰면 1번이 느려집니다.</div>\n    </div>\n  </div>\n</div>\n\n<h2>11~12월 — 이미 보이는 돈</h2>\n<div class="card accent">\n  <div class="wrapx"><table>\n  <tr><th>시점</th><th>항목</th><th>금액</th></tr>\n  <tr><td>11월</td><td>메이븐 정산</td><td class="num">1,800만</td></tr>\n  <tr><td>12월</td><td>메이븐 정산</td><td class="num">1,800만</td></tr>\n  <tr><td>12월</td><td>6기 강의 정산</td><td class="num">500~1,000만</td></tr>\n  <tr><td colspan="2"><b>합계</b></td><td class="num"><b>4,100~4,600만</b></td></tr>\n  </table></div>\n  <div class="warn">메이븐 11·12월 1,800만은 <b>루크님 가정값</b>입니다. 10월분만 실제로 정산받으셨습니다. 6기 정산액은 10/20 라이브 반응과 10/25 런칭 결과로 정해집니다.</div>\n</div>\n\n<h2>엔진 2 — 가을님 건, 매출별 루크 몫</h2>\n<div class="card">\n  <p style="margin:0 0 8px">계산 구조: <b>매출 → PG 4% 제외 → 루크 8% → 광고비 차감 → 나머지를 초월스토리:강사 5:5</b></p>\n  <div class="wrapx"><table>\n  <tr><th>매출</th><th>인원<br><small>289만 기준</small></th><th>루크</th><th>강사(가을)</th></tr>\n  <tr><td>3,000만</td><td>11명</td><td class="num">230만</td><td class="num">0원</td></tr>\n  <tr><td>5,000만</td><td>18명</td><td class="num">384만</td><td class="num">0원</td></tr>\n  <tr><td>6,500만</td><td><b>23명</b></td><td class="num"><b>499만</b></td><td class="num">620만</td></tr>\n  <tr><td>1억</td><td>35명</td><td class="num">768만</td><td class="num">2,166만</td></tr>\n  <tr><td>1.5억</td><td>52명</td><td class="num">1,152만</td><td class="num">4,374만</td></tr>\n  <tr><td>2억</td><td>70명</td><td class="num">1,536만</td><td class="num">6,582만</td></tr>\n  </table></div>\n  <div class="emph"><b>목표 500만원은 23명이면 넘습니다.</b> 1억 매출이면 768만원입니다.</div>\n  <div class="warn"><b>관계 리스크 하나.</b> 루크님 8%는 광고비와 무관하게 나오지만, <b>18명 아래면 가을 대표님 몫이 0원</b>입니다. 광고 4,500만을 먼저 회수하는 구조라서요. 루크는 받고 강사는 못 받는 구간이 생깁니다 — <b>촬영 전에 손익분기 18명을 가을 대표님께 직접 말씀드리세요.</b> 나중에 알면 관계가 상합니다.</div>\n  <div class="note">검증: 1억 매출 → PG 제외 9,600만 → 루크 768만 → 광고 4,500만 차감 4,332만 → 5:5 = <b>2,166만</b>. 노션에 적힌 "가을 대표님 몫 2,200만"과 맞습니다. 구조가 확인됐습니다.</div>\n</div>\n\n<h2>엔진 1 — 1월 자사 강의, 시나리오별</h2>\n<div class="card">\n  <p style="margin:0 0 8px">분배 <b>루크 36% · 종혁 40% · 정현 24%</b> (종혁과 6:4 → 루크 몫을 다시 정현과 6:4)</p>\n  <div class="wrapx"><table>\n  <tr><th>객단가</th><th>인원</th><th>매출</th><th>루크 (A안)</th><th>루크 (B안)</th></tr>\n  <tr><td>120만</td><td>150명</td><td>1.8억</td><td class="num">3,971만</td><td class="num">5,411만</td></tr>\n  <tr><td>120만</td><td>300명</td><td>3.6억</td><td class="num">1.02억</td><td class="num">1.16억</td></tr>\n  <tr><td><b>180만</b></td><td>150명</td><td>2.7억</td><td class="num">7,081만</td><td class="num">8,521만</td></tr>\n  <tr><td><b>180만</b></td><td><b>300명</b></td><td><b>5.4억</b></td><td class="num"><b>1.64억</b></td><td class="num"><b>1.78억</b></td></tr>\n  <tr><td>250만</td><td>150명</td><td>3.75억</td><td class="num">1.07억</td><td class="num">1.22억</td></tr>\n  <tr><td>250만</td><td>300명</td><td>7.5억</td><td class="num">2.37억</td><td class="num">2.51억</td></tr>\n  </table></div>\n  <div class="note"><b>A안</b> 매출 기준으로 나누고 비용 2,250만은 루크가 전부 부담 · <b>B안</b> 비용을 먼저 빼고 나눔. <b>어느 쪽이든 차이는 정확히 1,440만원</b>입니다(2,250만 × 64%). 계약 전에 닫아야 할 칸입니다.</div>\n  <div class="warn"><b>객단가 180만원은 가정값</b>입니다. 10/9 분석에서 쓴 숫자이고 6기 가격과 다를 수 있습니다 — <b>확인 필요</b>. 비용 2,250만(고정급 900 + 광고 900 + PD 450)도 3개월 가정값입니다.</div>\n</div>\n\n<h2>분기 엔진 — 광고 900만으로 3,000명, 연 4회</h2>\n<div class="card accent">\n  <p style="margin:0 0 8px">누적 회원에서 반복해 뽑는 게 아니라 <b>매 분기 광고로 3,000명을 새로 들여오는 획득 엔진</b>입니다. 그러면 풀이 고갈되지 않습니다.</p>\n  <div class="steps">\n    <div><b>900만</b>분기 광고비<small><br>월 300만 × 3</small></div>\n    <div><b>3,000명</b>분기 신규 유입<small><br>CAC 3,000원</small></div>\n    <div><b>300명</b>전환 10%</div>\n    <div><b>5.4억</b>분기 매출<small><br>객단가 180만</small></div>\n  </div>\n  <div class="wrapx"><table>\n  <tr><th></th><th>분기</th><th>연 4회</th></tr>\n  <tr><td>광고비</td><td class="num">900만</td><td class="num">3,600만</td></tr>\n  <tr><td>신규 유입 <small>카페</small></td><td class="num">3,000명</td><td class="num">12,000명</td></tr>\n  <tr><td>구매자 <small>전환 10%</small></td><td class="num">300명</td><td class="num">1,200명</td></tr>\n  <tr><td>매출</td><td class="num">5.4억</td><td class="num">21.6억</td></tr>\n  <tr><td><b>루크 (B안)</b></td><td class="num">1.78억</td><td class="num"><b>7.14억</b></td></tr>\n  </table></div>\n  <div class="note">연 비용 9,000만 가정 (고정급 3,600 + PD 1,800 + 광고 3,600). B안 = 비용 차감 후 분배. A안이면 <b>6.56억</b>으로 5,760만원 낮습니다. 종혁 7.93억 / 정현 4.76억 (B안).</div>\n  <div class="emph"><b>광고비가 매출의 1.7%, ROAS 60배입니다.</b> 이 숫자가 유지되면 모객이 병목이지 전환이 병목이 아닙니다 — 돈을 더 태우면 더 들어온다는 뜻이니까요.</div>\n</div>\n\n<div class="card">\n  <h3>숫자 두 개를 헷갈리지 않기</h3>\n  <div class="kv">\n    <dt>유입</dt><dd>광고로 <b>카페에 들어온 사람</b> — 분기 3,000명 / 연 <b>12,000명</b></dd>\n    <dt>구매자</dt><dd>그중 <b>본 강의를 산 사람</b> — 분기 300명 / 연 <b>1,200명</b> (전환 10%)</dd>\n  </div>\n  <div class="note">매출은 구매자 수로만 납니다. 유입은 구매자를 만드는 모수일 뿐이고, 사지 않은 10,800명은 카페에 남아 다음 분기 모수가 됩니다.</div>\n</div>\n\n<h2>미전환 재고 — 떠나지 않는 사람들</h2>\n<div class="card gold">\n  <p style="margin:0 0 8px">1분기에 전환 안 된 2,700명은 카페에 <b>남아 있습니다.</b> 2분기부터는 신규 3,000명에 더해 이 사람들도 모집 대상이 됩니다.</p>\n  <div class="wrapx"><table>\n  <tr><th>분기</th><th>신규분</th><th>기존분</th><th>합계</th><th>분기말 미전환</th></tr>\n  <tr><td>1분기</td><td class="num">300명</td><td class="num">—</td><td class="num">300명</td><td>2,700명</td></tr>\n  <tr><td>2분기</td><td class="num">300명</td><td class="num">68명</td><td class="num">368명</td><td>5,332명</td></tr>\n  <tr><td>3분기</td><td class="num">300명</td><td class="num">133명</td><td class="num">433명</td><td>7,899명</td></tr>\n  <tr><td>4분기</td><td class="num">300명</td><td class="num">198명</td><td class="num">498명</td><td>10,402명</td></tr>\n  <tr><td><b>연간</b></td><td colspan="2"></td><td class="num"><b>1,598명</b></td><td>누적 유입 12,000명</td></tr>\n  </table></div>\n  <div class="note">기존 미전환자의 분기 재전환율 2.5%로 계산. <b>이 2.5%는 클로드 가정값이고 근거가 없습니다</b> — 1분기 뒤 실측으로 바꿔야 합니다. 맞다면 연 1,200명이 아니라 1,598명이고, 뒤로 갈수록 광고 없이 버는 몫이 커집니다.</div>\n  <div class="warn"><b>대신 피로도를 관리해야 합니다.</b> 같은 강의를 1년에 네 번 팔면 4분기쯤 카페 고참이 신규 유입자에게 "저거 지난 분기에도 했어"라고 말합니다. 기수제(6기·7기·8기)를 이미 쓰고 계시니 희소성은 그걸로 유지되지만, <b>기수마다 커리큘럼이나 혜택에 실제로 달라지는 칸</b>이 하나는 있어야 합니다.</div>\n</div>\n\n<h2>모델이 깨지는 두 숫자</h2>\n<div class="card red">\n  <p style="margin:0 0 8px">위 숫자 전부가 <b>CAC 3,000원</b>과 <b>전환율 10%</b> 두 개에 매달려 있습니다. 둘 다 아직 실측 전입니다.</p>\n  <div class="wrapx"><table>\n  <tr><th>CAC</th><th>분기 유입<br><small>카페 신규</small></th><th>전환 5%</th><th>전환 10%</th><th>전환 15%</th></tr>\n  <tr><td><b>3,000원</b></td><td>3,000명</td><td class="num">150명</td><td class="num">300명</td><td class="num">450명</td></tr>\n  <tr><td>4,500원</td><td>2,000명</td><td class="num">100명</td><td class="num">200명</td><td class="num">300명</td></tr>\n  <tr><td>6,000원</td><td>1,500명</td><td class="num">75명</td><td class="num">150명</td><td class="num">225명</td></tr>\n  <tr><td>9,000원</td><td>1,000명</td><td class="num">50명</td><td class="num">100명</td><td class="num">150명</td></tr>\n  </table></div>\n  <p style="margin:12px 0 6px"><b>연간 루크 몫으로 환산하면</b></p>\n  <div class="wrapx"><table>\n  <tr><th>CAC</th><th>전환</th><th>연 유입<br><small>카페 신규</small></th><th>연 구매자</th><th>연 매출</th><th>루크 (B안)</th></tr>\n  <tr><td>3,000원</td><td>10%</td><td>12,000명</td><td><b>1,200명</b></td><td>21.6억</td><td class="num">7.14억</td></tr>\n  <tr><td>3,000원</td><td>5%</td><td>12,000명</td><td>600명</td><td>10.8억</td><td class="num">3.41억</td></tr>\n  <tr><td>4,500원</td><td>10%</td><td>8,000명</td><td>800명</td><td>14.4억</td><td class="num">4.65억</td></tr>\n  <tr><td>4,500원</td><td>5%</td><td>8,000명</td><td>400명</td><td>7.2억</td><td class="num">2.16억</td></tr>\n  <tr><td>6,000원</td><td>10%</td><td>6,000명</td><td>600명</td><td>10.8억</td><td class="num">3.41억</td></tr>\n  <tr><td>6,000원</td><td>5%</td><td>6,000명</td><td>300명</td><td>5.4억</td><td class="num">1.54억</td></tr>\n  </table></div>\n  <div class="emph"><b>1.54억에서 7.14억 사이. 4.6배 폭입니다.</b> 그래서 1분기가 끝나면 <b>딱 두 숫자만 재면 됩니다</b> — 실제로 쓴 광고비 ÷ 실제로 들어온 사람 수, 그리고 실제 구매 전환율. 그 둘이 나머지 세 분기를 확정합니다.</div>\n  <div class="note">CAC는 보통 분기가 갈수록 오릅니다. 관심이 높은 사람부터 먼저 들어오고, 같은 소재를 반복하면 광고 피로가 쌓이기 때문입니다. 다만 종혁 본부장이 과거 카페 <b>월 4,000명</b>을 만든 실적이 있다고 하셨으니 월 1,000명은 그 1/4 수준이라 보수적인 목표입니다 — <b>그때 광고비를 물어보면 이 표의 첫 줄이 확정됩니다.</b></div>\n</div>\n\n<h2>그래서 엔진 1을 매일 돌려야 합니다</h2>\n<div class="card accent">\n  <p style="margin:0">이 모델에서 <b>광고와 모객은 매출의 선행 지표</b>입니다. 이번 분기에 3,000명을 못 모으면 다음 분기 강의 모집이 그냥 없어집니다. 매출이 줄어드는 게 아니라 <b>회차 자체가 사라집니다.</b></p>\n  <div class="note">하루에 한 엔진씩 6개를 똑같이 돌리면 엔진 1에 주 1일이 갑니다. 그래서 엔진 1만 매일 06:00~08:00 고정으로 빼두는 설계입니다.</div>\n</div>\n\n<h2>사이트 구조 — 입문에서 심화로</h2>\n<div class="card accent">\n  <p style="margin:0 0 10px">전자책 판매처를 따로 두지 않습니다. <b>거인의 도구공방이 기본 사이트</b>이고, 일십백천·원크루가 그 위 심화입니다.</p>\n  <ul class="tl">\n    <li><div class="d">0원 · 유입</div><div class="t">네이버 카페</div><div class="m">엔진 1. 광고 900만으로 분기 3,000명</div></li>\n    <li class="big"><div class="d">3만원 · 입문</div><div class="t">거인의 도구공방 — 전자책 · 독서 프로젝트</div><div class="m">처음 돈을 쓰는 자리. 여기서 결제한 사람만 다음 칸으로 셉니다</div></li>\n    <li><div class="d">프로그램</div><div class="t">거인의 도구공방 — 툴박스</div><div class="m">같은 사이트 안에서 올라갑니다</div></li>\n    <li class="big"><div class="d">180만원 · 본 강의</div><div class="t">멘토루크 강의 (분기 1회)</div><div class="m">엔진 1의 매출이 여기서 납니다</div></li>\n    <li><div class="d">심화</div><div class="t">일십백천 · 원크루</div><div class="m">1:1 컨설팅과 크루. 인원은 적고 단가는 가장 높습니다</div></li>\n  </ul>\n</div>\n\n<h2>이 구조가 만드는 숫자 — 광고비가 당월에 돌아옵니다</h2>\n<div class="card gold">\n  <p style="margin:0 0 8px">지금은 카페에 사람이 들어와도 <b>분기 말 본 강의까지 최대 3개월</b>을 기다려야 광고비가 회수됩니다. 중간에 3만원짜리가 있으면 <b>유입된 달에 회수가 시작됩니다.</b></p>\n  <div class="wrapx"><table>\n  <tr><th>전자책 전환</th><th>구매</th><th>회수액</th><th>광고 900만 대비</th></tr>\n  <tr><td>5%</td><td>150명</td><td class="num">450만</td><td>절반 회수</td></tr>\n  <tr><td><b>10%</b></td><td><b>300명</b></td><td class="num"><b>900만</b></td><td><b>전액 회수</b></td></tr>\n  <tr><td>15%</td><td>450명</td><td class="num">1,350만</td><td>450만 순증</td></tr>\n  </table></div>\n  <div class="emph"><b>전자책 전환 10%가 광고비 손익분기입니다.</b> CAC 3,000원과 전자책 3만원 × 10%가 정확히 같은 값이라 그렇습니다. 그 선을 넘으면 <b>분기 본 강의 5.4억이 전부 순증</b>이 됩니다 — 광고비는 이미 전자책이 갚았으니까요.</div>\n  <div class="note">독서 프로젝트는 3만원/월 구독이라 2개월차부터는 광고비 없이 들어옵니다. 210명 × 3만 × 3개월 = 1,890만 (전환 7% 가정).</div>\n  <div class="warn">전환율 10%·7%는 <b>클로드 가정값이고 근거가 없습니다.</b> 1분기 전자책 판매가 실측값입니다 — 그 숫자 하나가 "광고를 더 태워도 되는가"를 정합니다.</div>\n</div>\n\n<h2>엔진 3이 엔진 1의 하위가 아닌 이유</h2>\n<div class="card">\n  <p style="margin:0 0 8px">앞서 전자책을 엔진 1 하위 과제로 붙이자고 했는데, 말씀을 듣고 보니 틀렸습니다. <b>엔진 3이 독립 사이트여야 하는 이유</b>가 있습니다.</p>\n  <ul class="list">\n    <li><div class="t">판매처가 하나로 모입니다</div><div class="m">전자책·프로그램·소액 교육이 흩어지면 결제 연결도·약관도·정산도 전부 따로 관리해야 합니다</div></li>\n    <li><div class="t">카페 밖에서도 팔립니다</div><div class="m">엔진 1 하위로 두면 카페 회원에게만 팝니다. 독립 사이트면 검색·유튜브·인스타에서 바로 들어옵니다</div></li>\n    <li><div class="t">심화로 올리는 길이 생깁니다</div><div class="m">도구공방에서 결제한 사람이 일십백천·원크루 후보 명단이 됩니다. 무료 카페 회원과 <b>돈을 한 번 쓴 사람</b>은 전혀 다른 명단입니다</div></li>\n  </ul>\n  <div class="note">그래서 수요일 엔진 3 블록은 \'언젠가 할 것\'이 아니라 <b>1분기 안에 결제가 돌아야 하는 자리</b>입니다. 툴박스 포트원 연결이 그 앞단입니다.</div>\n</div>\n\n<h2>기존 회원 500명 — 콜드와 전혀 다른 자산</h2>\n<div class="card accent">\n  <p style="margin:0 0 8px">메이븐과 함께 2026년 안에 만들 <b>500명</b>은 광고로 사오는 12,000명과 성질이 다릅니다. CAC가 0원이라서가 아니라 <b>고가 상품을 살 수 있는 유일한 모수</b>이기 때문입니다.</p>\n  <div class="wrapx"><table>\n  <tr><th>상품</th><th>단가</th><th>전환</th><th>인원</th><th>연 기여</th><th>비중</th></tr>\n  <tr><td>전자책</td><td>3만</td><td>20%</td><td>100명</td><td class="num">300만</td><td>1.7%</td></tr>\n  <tr><td>독서 프로젝트</td><td>3만/월</td><td>8%</td><td>40명</td><td class="num">1,440만</td><td>8.4%</td></tr>\n  <tr><td>본 강의</td><td>180만</td><td>8%</td><td>40명</td><td class="num">7,200만</td><td>41.9%</td></tr>\n  <tr><td><b>고가 — 일십백천·원크루</b></td><td>1,650만</td><td>1%</td><td><b>5명</b></td><td class="num"><b>8,250만</b></td><td><b>48.0%</b></td></tr>\n  <tr><td colspan="4"><b>합계</b></td><td class="num"><b>1.72억</b></td><td>1인당 34만</td></tr>\n  </table></div>\n  <div class="warn">전환율 20%·8%·8%·1%는 <b>전부 클로드 가정값이고 근거가 없습니다.</b> 루크님은 5년치 수강생 데이터를 갖고 계시니, 이 네 칸을 실제 숫자로 바꾸면 아래 계산이 전부 확정됩니다.</div>\n</div>\n\n<h2>고가 한 칸이 전부를 정합니다</h2>\n<div class="card red">\n  <p style="margin:0 0 8px"><b>고가를 빼면 500명과 콜드 유입이 같습니다.</b></p>\n  <div class="wrapx"><table>\n  <tr><th></th><th>1명당 연 기여</th></tr>\n  <tr><td>카페 콜드 1명 <small>(전환 10% × 180만)</small></td><td class="num">18.0만</td></tr>\n  <tr><td>기존 회원 1명 — <b>고가 제외</b></td><td class="num">17.9만</td></tr>\n  <tr><td>기존 회원 1명 — 고가 포함</td><td class="num">34.4만</td></tr>\n  </table></div>\n  <div class="emph"><b>0.99배입니다.</b> 전자책과 본 강의만 판다면 500명은 광고로 사온 사람과 수익이 똑같습니다. 벌어지는 1.9배가 <b>전부 고가 한 줄에서</b> 나옵니다.</div>\n  <p style="margin:12px 0 6px"><b>고가 전환율만 움직여 본 것</b></p>\n  <div class="wrapx"><table>\n  <tr><th>고가 전환</th><th>인원</th><th>고가 매출</th><th>500명 총합</th><th>1인당</th></tr>\n  <tr><td>0%</td><td>0명</td><td class="num">0원</td><td class="num">8,940만</td><td>17.9만</td></tr>\n  <tr><td>0.5%</td><td>2.5명</td><td class="num">4,125만</td><td class="num">1.31억</td><td>26.1만</td></tr>\n  <tr><td><b>1%</b></td><td><b>5명</b></td><td class="num">8,250만</td><td class="num"><b>1.72억</b></td><td>34.4만</td></tr>\n  <tr><td>2%</td><td>10명</td><td class="num">1.65억</td><td class="num">2.54억</td><td>50.9만</td></tr>\n  <tr><td>3%</td><td>15명</td><td class="num">2.48억</td><td class="num">3.37억</td><td>67.4만</td></tr>\n  <tr><td>5%</td><td>25명</td><td class="num">4.12억</td><td class="num">5.02억</td><td>100.4만</td></tr>\n  </table></div>\n  <div class="emph"><b>고가 1명이 8,250만원 중 1,650만원입니다.</b> 전자책 550명을 팔아야 나오는 돈을 한 사람이 냅니다. 500명 자산 운영의 전부는 <b>이 다섯에서 열다섯 명을 만드는 일</b>입니다.</div>\n</div>\n\n<h2>그래서 전자책의 역할이 둘로 갈립니다</h2>\n<div class="card gold">\n  <div class="wrapx"><table>\n  <tr><th>누구에게</th><th>전자책의 역할</th><th>봐야 할 숫자</th></tr>\n  <tr><td><b>콜드 12,000명</b></td><td>광고비 회수 장치</td><td>전환 10%면 광고 900만 전액 상계</td></tr>\n  <tr><td><b>기존 500명</b></td><td>고가로 올리는 계단</td><td>매출 비중은 1.7%뿐 — 돈이 목적이 아님</td></tr>\n  </table></div>\n  <div class="note">같은 3만원짜리인데 역할이 다릅니다. 500명에게 전자책을 파는 이유는 300만원이 아니라, <b>산 사람과 안 산 사람을 가르는 명단</b>을 얻기 위해서입니다. 3만원을 낸 사람이 1,650만원을 낼 후보입니다.</div>\n</div>\n\n<h2>역산 — 목표를 정하면 필요한 전환율이 나옵니다</h2>\n<div class="card">\n  <div class="wrapx"><table>\n  <tr><th>500명에서 받고 싶은 돈</th><th>필요한 고가 전환</th><th>인원</th></tr>\n  <tr><td>5,000만</td><td>0%</td><td>0명 <small>(나머지만으로 넘음)</small></td></tr>\n  <tr><td>1억</td><td>0.13%</td><td>1명</td></tr>\n  <tr><td><b>2억</b></td><td>1.34%</td><td><b>7명</b></td></tr>\n  <tr><td>3억</td><td>2.55%</td><td>13명</td></tr>\n  </table></div>\n  <div class="note">전자책 20% · 독서 8% · 본 강의 8%를 유지한다는 전제입니다. <b>2억을 목표로 하면 500명 중 일곱 명</b>을 고가로 올리면 됩니다 — 분기당 두 명 꼴입니다.</div>\n</div>\n\n<h2>500명이 2027년에도 500명이려면</h2>\n<div class="card">\n  <div class="wrapx"><table>\n  <tr><th>연 이탈</th><th>2027년 모수</th><th>연 기여</th></tr>\n  <tr><td>0%</td><td>500명</td><td class="num">1.72억</td></tr>\n  <tr><td>20%</td><td>400명</td><td class="num">1.38억</td></tr>\n  <tr><td>40%</td><td>300명</td><td class="num">1.03억</td></tr>\n  </table></div>\n  <div class="warn"><b>500명은 한 번 수확하고 끝나는 자산이 아니라 관리해야 하는 자산입니다.</b> 같은 사람들에게 분기마다 네 번 팔면 명단이 탑니다 — 메일을 안 열고, 카페에 안 들어오고, 그러면 이탈 40%가 됩니다. 분기에 한 번은 <b>아무것도 안 파는 분기</b>를 두시거나, 파는 것 사이에 주는 것을 끼우셔야 합니다.</div>\n</div>\n\n<h2>전체 그림 — 두 엔진을 합치면</h2>\n<div class="card accent">\n  <div class="wrapx"><table>\n  <tr><th>자산</th><th>규모</th><th>연 기여</th><th>성격</th></tr>\n  <tr><td>카페 콜드 유입</td><td>연 12,000명</td><td class="num">21.6억 <small>(전체 매출)</small></td><td>광고로 삼 · 분배 있음</td></tr>\n  <tr><td>기존 회원</td><td>500명</td><td class="num">1.72억</td><td>이미 보유 · 광고비 0</td></tr>\n  </table></div>\n  <div class="emph">콜드 21.6억은 <b>전체 매출</b>이고 루크님 몫은 36%(B안 7.14억)입니다. 500명 1.72억은 <b>분배 전</b> 숫자고, 메이븐과의 공동 자산이라 여기도 나눌 몫이 있을 수 있습니다 — <b>확인 필요</b>.</div>\n</div>\n\n<h2>500명에 대해 확인할 네 가지</h2>\n<div class="card red">\n  <ul class="list">\n    <li class="big"><div class="t">1. 메이븐과의 분배</div><div class="m">공동으로 만드는 500명이면 여기서 나는 수익도 나눌 몫이 있을 수 있습니다. 지금 월 1,800만 정산 구조와 어떤 관계인지가 1.72억을 반으로 가를 수 있습니다</div></li>\n    <li><div class="t">2. \'회원\'의 정의</div><div class="m">무료 카페 가입자 500명인지, <b>돈을 낸 수강생</b> 500명인지에 따라 고가 전환율이 완전히 달라집니다. 이 분석은 후자를 가정했습니다</div></li>\n    <li class="big"><div class="t">3. 고가 상품 실제 단가</div><div class="m">1,650만원은 대시보드의 \'원크루 1~2명 전환 = 3,300~3,900만\'에서 역산한 값입니다. 일십백천과 원크루 가격이 다르면 48% 칸이 통째로 바뀝니다</div></li>\n    <li><div class="t">4. 전환율 네 개 — 루크님 데이터로</div><div class="m">전자책 20% · 독서 8% · 본 강의 8% · 고가 1%는 전부 제 가정입니다. 5년치 수강생 기록에서 실제 재구매율을 꺼내면 이 페이지가 추정에서 계획으로 바뀝니다</div></li>\n  </ul>\n</div>\n\n<h2>주간 로테이션 <small>캘린더에 올라가 있습니다</small></h2>\n<div class="card accent">\n  <div class="wrapx"><table>\n  <tr><th>요일</th><th>09:00–12:00</th><th>비고</th></tr>\n  <tr><td>월</td><td><b>엔진 1</b> — 카페 모객 + 주간 설계</td><td>한 주의 방향</td></tr>\n  <tr><td>화</td><td><b>엔진 2</b> — 가을님 신규강사 런칭</td><td>초월스토리·촬영</td></tr>\n  <tr><td>수</td><td><b>엔진 3</b> — 거인의 도구공방</td><td>전자책·프로그램 판매처</td></tr>\n  <tr><td><b>목</b></td><td><b>비움</b></td><td>지영 일정</td></tr>\n  <tr><td>금</td><td><b>엔진 4</b> — 앱 제작·판매</td><td>개발자 계정이 앞단</td></tr>\n  <tr><td>토</td><td><b>엔진 5</b> — 연애상담 + 콘텐츠 몰아찍기</td><td>11시부터 촬영</td></tr>\n  <tr><td>일</td><td>주간 리뷰 (09:00–10:00)</td><td>여유 있으면 엔진 6</td></tr>\n  </table></div>\n  <div class="emph"><b>매일 09:00–09:30은 엔진 1(카페 모객)입니다.</b> 요일과 무관하게 고정입니다. 목요일에도 이 30분만 돌립니다. 엔진 1이 전체 현금의 80% 이상이고, 카페 모객은 하루 멈추면 바로 유입이 끊기기 때문입니다.</div>\n  <div class="note"><b>엔진 6(정부지원 자동화)은 고정 슬롯이 없습니다.</b> 루크님이 직접 \'서브\'로 두셨고, 여섯을 다섯 요일에 넣으면 하나는 남습니다. 일요일 리뷰 뒤 여유가 있을 때만 손대는 자리입니다 — 여기에 시간을 당겨 쓰면 엔진 1이 느려집니다.</div>\n</div>\n\n<h2>컨설팅 리듬 — 묻고, 평가하고, 고칩니다</h2>\n<div class="card gold">\n  <div class="wrapx"><table>\n  <tr><th>언제</th><th>무엇</th></tr>\n  <tr><td><b>08:23</b><br><small>월·화·수·금·토</small></td><td><b>아침 브리핑</b> — 오늘의 엔진과 09:00~12:00에 끝낼 것 3가지. 끝났는지 아닌지 판정 가능한 것만. 어제 미완은 맨 위로</td></tr>\n  <tr><td><b>20:53</b><br><small>월~토</small></td><td><b>저녁 성과 체크</b> — 카페 유입 / 3가지 중 몇 개 / 들어온 돈 / 막힌 것. 답을 주시면 목표 대비 %로 평가하고 내일 바꿀 것 하나를 드립니다</td></tr>\n  <tr><td><b>일 09:52</b></td><td><b>주간 컨설팅</b> — 실측 CAC 계산, 주 250명 대비 달성률, 엔진별 평가, 다음 주에 바꿀 것 하나</td></tr>\n  </table></div>\n  <div class="emph"><b>매주 재는 숫자는 둘입니다 — 실측 CAC와 실측 전환율.</b> 쓴 광고비 ÷ 들어온 사람 수, 그리고 구매자 ÷ 카페 회원. 이 둘이 연간 루크님 몫을 1.54억과 7.14억 사이 어디로 보낼지 정합니다.</div>\n  <div class="warn"><b>멈춤 기준을 미리 정해 둡니다.</b> 주 250명 대비 <b>2주 연속 70% 아래</b>면 1월 300명 목표를 내려 잡습니다. 희망 섞인 숫자를 들고 1월까지 가면 그때 가서 고치는 비용이 훨씬 큽니다. <b>가정값이 석 달째 그대로인 것</b>도 같은 경고입니다 — 숫자 하나 재는 데 석 달이 걸릴 일은 없습니다.</div>\n  <div class="note">답을 안 하시면 거기서 멈춥니다. 추측으로 평가서를 쓰지 않습니다.</div>\n</div>\n\n<h2>하루 일과</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">06:00 – 08:00 · 엔진 1 (매일 고정)</div><div class="m">카페 글 발행 · 댓글·DM 응대 · 유입 숫자 기록. 가장 머리가 맑은 시간을 가장 큰 엔진에</div></li>\n    <li><div class="t">08:00 – 09:00 · 유지 블록</div><div class="m">오늘의 엔진을 뺀 나머지 4개 × 15분. 타이머 걸고 끊기. 진척이 아니라 <b>안 죽이는 것</b>이 목적</div></li>\n    <li class="big"><div class="t">09:00 – 12:30 · 오늘의 엔진 1차</div><div class="m">만드는 시간. 회의·통화 금지</div></li>\n    <li><div class="t">13:30 – 17:00 · 오늘의 엔진 2차</div><div class="m">이어서. 하루에 한 엔진을 7시간 밀면 한 주에 각 엔진이 7시간씩 받습니다</div></li>\n    <li><div class="t">17:00 – 19:00 · 외부</div><div class="m">미팅·통화·컨설팅. 몰아서 여기로</div></li>\n    <li><div class="t">19:00 – 21:00 · 촬영 또는 내부 수익</div><div class="m">전자책·독서 프로젝트 제작이 여기 들어갑니다</div></li>\n    <li><div class="t">21:00 – 21:30 · 기록</div><div class="m">오늘 숫자 3개(카페 유입·문의·매출) + 내일 1순위 3개</div></li>\n  </ul>\n  <div class="note">집중 시간 합계 약 10시간. 엔진 1에 주 14시간, 나머지 각 엔진에 주 7~8시간이 갑니다.</div>\n</div>\n\n<h2>90일 타임라인</h2>\n<div class="card">\n  <ul class="tl">\n    <li class="big"><div class="d">10/20 (화)</div><div class="t">라이브 — 6기 수강생 수 가늠</div><div class="m">12월 정산 규모가 여기서 보입니다</div></li>\n    <li class="big"><div class="d">10/25 (일)</div><div class="t">6기 강의 런칭</div><div class="m">문의 80명 → 전환율이 다음 기수 가격 설계의 근거가 됩니다</div></li>\n    <li><div class="d">10월 4주차</div><div class="t">엔진 1 시작 — 카페 모객 개시</div><div class="m">광고 집행·콘텐츠 발행. <b>1월 런칭의 모든 것이 여기서 시작</b></div></li>\n    <li><div class="d">11월 초</div><div class="t">가을님 촬영</div><div class="m">그 전에 손익분기 18명 설명 완료</div></li>\n    <li><div class="d">11월</div><div class="t">6기 강의 진행 · 전자책 초고</div><div class="m">메이븐 정산 1,800만 (가정)</div></li>\n    <li><div class="d">12월</div><div class="t">가을님 강의 · 6기 정산</div><div class="m">메이븐 1,800만 + 6기 500~1,000만</div></li>\n    <li class="big"><div class="d">12월 말</div><div class="t">카페 3,000명 도달 여부 판정</div><div class="m">여기서 미달이면 1월 런칭 규모를 다시 잡아야 합니다. 중단이 아니라 <b>숫자를 다시 세우는</b> 지점</div></li>\n    <li class="big"><div class="d">2027년 1월</div><div class="t">자사 강의 300명 런칭 + 가을님 정산</div><div class="m">루크 1.6~1.8억 + 768만 (1억 매출 시)</div></li>\n  </ul>\n</div>\n\n<h2>확인 필요 — 숫자를 확정하려면</h2>\n<div class="card red">\n  <ul class="list">\n    <li><div class="t">1. 자사 강의 객단가</div><div class="m">180만원은 10/9 분석의 가정값. 6기 실제 가격과 1월 상품 가격을 정해야 이 페이지 숫자가 확정됩니다</div></li>\n    <li class="big"><div class="t">2. 6:4의 분모 — A안인가 B안인가</div><div class="m">루크님 몫이 <b>1,440만원</b> 움직입니다. 종혁 본부장과 계약 전에 반드시</div></li>\n    <li><div class="t">3. 루크 36% / 정현 24% 해석이 맞는지</div><div class="m">"종혁과 6:4, 거기서 내가 6 정현님 4"를 그렇게 읽었습니다. 정현님 몫이 전체의 24%라는 데 두 분이 동의하셨는지</div></li>\n    <li><div class="t">4. 3개월 비용 총액</div><div class="m">2,250만(고정급 900 + 광고 900 + PD 450)은 가정. 노션에 "천만에 전부 포함" vs "천만 + 광고 900만" 두 기록이 충돌합니다</div></li>\n    <li><div class="t">5. 가을님 건 광고 예산 4,500만</div><div class="m">역산값입니다. 초월스토리 PD님께 실제 예산과 상한·중단 기준을 받아야 합니다</div></li>\n    <li class="big"><div class="t">6. CAC 3,000원과 전환율 10% — 1분기 실측</div><div class="m">연간 루크 몫이 1.54억에서 7.14억까지 움직이는 두 숫자. 1분기 끝에 (쓴 광고비 ÷ 들어온 사람 수)와 (구매자 ÷ 카페 회원)만 재면 나머지 세 분기가 확정됩니다. 종혁 본부장이 과거 월 4,000명 만들 때 광고비를 물으면 첫 줄이 미리 확정됩니다</div></li>\n    <li><div class="t">7. 전자책 전환율 — 광고비 손익분기선</div><div class="m">10%면 광고비가 전액 회수되고 그 위는 순증입니다. 1분기 전자책 판매가 실측값. 연애상담(엔진 5)은 아직 상품·단가가 없어 전망을 못 세웁니다</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  <b>근거</b>\n  <ul>\n    <li>메이븐 10월 정산 1,800만원, 11·12월 동액 가정, 6기 문의 80명, 12월 정산 500~1,000만원, 분배 구조(종혁 6:4 → 정현 6:4), 분기 반복 계획, 전자책·독서 프로젝트 3만원 — 전부 2026-10-17 루크님 말씀</li>\n    <li>초월스토리 분배 구조(루크 수수료 = PG 제외 매출의 8% · 순수익 초월스토리:강사 5:5 · 289만 단일 상품) — 10/6 회의 구두 합의, 노션 [결정] 기록</li>\n    <li>광고 예산 4,500만원과 가을 대표님 몫 2,200만원 — 노션 10/8 항목의 역산값. 1억 매출 모델에서 강사 몫 2,166만원이 나와 구조가 교차 검증됨</li>\n    <li>객단가 180만원 · PG 4% · 3개월 비용 2,250만원 — 10/9 박종혁 본부장 협업 분석에서 쓴 가정값, <b>실제 확인 전</b></li>\n    <li>카페 3,000명 · 전환 10% · 1월 300명 — 루크님 목표치</li>\n    <li>분기마다 광고 900만원(월 300만 × 3개월)으로 신규 3,000명을 모으고 분기에 한 번 강의를 모집해 연 4회 반복 — 2026-10-17 루크님 말씀</li>\n    <li>거인의 도구공방이 교육 + 프로그램 판매의 기본 사이트이고 일십백천·원크루가 심화 사이트, 전자책 판매처를 따로 두지 않음 — 2026-10-17 루크님 말씀</li>\n    <li>메이븐과 함께 2026년 안에 회원 500명을 만들 수 있을 것으로 본다 — 2026-10-17 루크님 말씀</li>\n    <li>고가 상품 단가 1,650만원 — 대시보드의 \'원크루 1~2명 전환 = 3,300~3,900만\'에서 역산. <b>확인 필요</b></li>\n    <li>미전환자 분기 재전환율 2.5% · 전자책 전환 10%(콜드)·20%(기존) · 독서 7~8% · 본 강의 8% · 고가 1% — 전부 클로드 가정값, 근거 없음</li>\n  </ul>\n</div>\n'

# ---------------------------------------------------------------- 지금 어디 있는가
MAP = '<div class="hero">\n  <h1>지금 어디 있는가</h1>\n  <div class="sub">과거 · 현재 · 미래 · 구간별로 얻어야 하는 결과</div>\n  <div class="goal">\n    <div><b>0명</b><span>카페 신규 유입 — 아직 시작 전</span></div>\n    <div><b>13주</b><span>분기 3,000명까지 남은 시간</span></div>\n    <div><b>6개</b><span>아직 가정값인 숫자</span></div>\n  </div>\n</div>\n\n<div class="card accent">\n  <p style="margin:0"><b>한 문장으로 된 현재 위치 — 모델은 다 그렸고, 실측값이 하나도 없습니다.</b></p>\n  <div class="note">계산은 끝났습니다. 21.6억도 7.14억도 1.72억도 전부 종이 위 숫자고, 그걸 사실로 만드는 첫 숫자는 <b>카페에 들어온 사람 수</b> 하나입니다. 오늘 그 값이 0입니다.</div>\n</div>\n\n<h2>과거 — 어디서 왔나</h2>\n<div class="card">\n  <ul class="tl">\n    <li><div class="d">~2021</div><div class="t">롯데택배 · 마켓컬리</div><div class="m">배달하며 스마트스토어 위탁판매를 시작. 이마트 한우에서 깨달은 것이 출발점</div></li>\n    <li><div class="d">2022.03</div><div class="t">법인 설립 — 힐링디어스(주)</div><div class="m">개인에서 법인으로</div></li>\n    <li><div class="d">~2026</div><div class="t">5년 · 수강생 3,000명</div><div class="m">50~60대 초보 중심. 유튜브 1만, 카톡 1천, 네이버 카페</div></li>\n    <li class="big"><div class="d">현재</div><div class="t">인베이더 종료 대비 · 메이븐 협력</div><div class="m">월 1,800만 정산이 지금의 현금줄</div></li>\n  </ul>\n  <div class="emph"><b>과거에서 가져갈 교훈 한 줄.</b> 지금까지 강의는 <b>남의 유통</b>을 타고 팔렸습니다. 인베이더가 끝난다는 건 그 통로가 닫힌다는 뜻이고, 식스 엔진 전체가 결국 <b>내 유입 · 내 판매처 · 내 심화</b>를 직접 짓는 일입니다. 그래서 엔진 1(카페)이 첫 칸입니다.</div>\n</div>\n\n<h2>현재 — 2026년 10월 17일의 정확한 좌표</h2>\n<div class="card">\n  <dl class="now">\n    <dt class="ok">확정</dt><dd>10월 메이븐 정산 1,800만 수령 · 법인 변경등기 법무사 위임 · 6기 문의 80명 · 초월스토리 분배 구조 합의(루크 8%)</dd>\n    <dt class="go">진행</dt><dd>10/20 라이브 → 10/25 6기 런칭 · 가을님 11월 초 촬영</dd>\n    <dt class="zero">0</dt><dd><b>카페 신규 유입 0명</b> · 도구공방 결제 미연결 · 전자책 0종 · 연애상담 상품 없음 · 개발자 계정 미등록</dd>\n    <dt class="q">가정</dt><dd>CAC 3,000원 · 전환율 10% · 객단가 180만 · 6:4 분모 · 메이븐 500명 분배 · 고가 단가 1,650만</dd>\n  </dl>\n  <div class="warn"><b>\'0\' 줄이 지금 가장 중요한 줄입니다.</b> 확정된 것들은 이미 번 돈이거나 끝난 일이고, 앞으로의 7.14억은 전부 저 0에서 시작합니다.</div>\n</div>\n\n<h2>미래 — 어디로 가나</h2>\n<div class="card">\n  <ul class="tl">\n    <li><div class="d">2026 Q4 · 쌓는 분기</div><div class="t">카페 3,000명을 모은다</div><div class="m">버는 건 메이븐 정산과 6기뿐. 이 분기는 수확이 아니라 <b>파종</b>입니다</div></li>\n    <li class="big"><div class="d">2027 Q1 · 첫 수확</div><div class="t">1월 자사 강의 300명 런칭</div><div class="m">루크 1.79억. 여기서 모델이 맞았는지 틀렸는지 판정됩니다</div></li>\n    <li><div class="d">2027 · 반복</div><div class="t">분기마다 광고 900만 → 3,000명 → 300명</div><div class="m">연 4회로 매출 21.6억, 루크 7.14억 (CAC·전환율이 가정대로일 때)</div></li>\n    <li><div class="d">그 위에</div><div class="t">기존 회원 500명에서 고가 5~15명</div><div class="m">1.72억~3.37억. 광고비 0원으로 버는 칸</div></li>\n  </ul>\n</div>\n\n<h2>돈이 어디서 나오는가 <small>기존 회원 500명 기준</small></h2>\n<figure class="fig">\n  <svg viewBox="0 0 400 220" role="img" aria-label="기존 회원 500명의 단계별 연 기여. 보유 500명 0원, 전자책 100명 300만원, 본 강의 40명 7,200만원, 심화 5명 8,250만원."><text x="10" y="16" font-size="11" fill="var(--muted)">단계 · 인원 · 1인당</text><text x="184" y="16" font-size="11" fill="var(--muted)">연 기여</text><line x1="174" y1="24" x2="174" y2="210" stroke="var(--line)" stroke-width="1"/><rect x="10" y="32" width="5" height="36" rx="2.5" fill="var(--f1)"/><text x="25" y="48" font-size="13" fill="var(--ink)" font-weight="700">보유 회원</text><text x="25" y="63" font-size="11.5" fill="var(--muted)">500명 · 0원</text><text x="191" y="55" font-size="12.5" fill="var(--ink)" font-weight="700">—</text><rect x="10" y="78" width="5" height="36" rx="2.5" fill="var(--f2)"/><text x="25" y="94" font-size="13" fill="var(--ink)" font-weight="700">전자책</text><text x="25" y="109" font-size="11.5" fill="var(--muted)">100명 · 3만원</text><rect x="184" y="89" width="6" height="14" rx="4" fill="var(--f2)"/><text x="197" y="101" font-size="12.5" fill="var(--ink)" font-weight="700">300만</text><rect x="10" y="124" width="5" height="36" rx="2.5" fill="var(--f3)"/><text x="25" y="140" font-size="13" fill="var(--ink)" font-weight="700">본 강의</text><text x="25" y="155" font-size="11.5" fill="var(--muted)">40명 · 180만원</text><rect x="184" y="135" width="133" height="14" rx="4" fill="var(--f3)"/><text x="324" y="147" font-size="12.5" fill="var(--ink)" font-weight="700">7,200만</text><rect x="10" y="170" width="5" height="36" rx="2.5" fill="var(--f4)"/><text x="25" y="186" font-size="13" fill="var(--ink)" font-weight="700">심화</text><text x="25" y="201" font-size="11.5" fill="var(--muted)">5명 · 1,650만원</text><rect x="184" y="181" width="152" height="14" rx="4" fill="var(--f4)"/><text x="343" y="193" font-size="12.5" fill="var(--ink)" font-weight="700">8,250만</text></svg>\n  <figcaption><b>인원은 줄고 금액은 커집니다.</b> 맨 아래 \'심화\'는 일십백천·원크루입니다. 5명이 100명보다 27배 많은 돈을 냅니다. 전자책을 파는 이유는 300만원이 아니라, 1,650만원을 낼 다섯 명을 찾아내기 위해서입니다. 전환율은 전부 가정값입니다.</figcaption>\n</figure>\n\n<h2>13주 — 분기까지 남은 시간</h2>\n<figure class="fig">\n  <svg viewBox="0 0 400 206" role="img" aria-label="카페 누적 유입 목표 궤적. 주 250명씩 13주에 3,250명. 현재 0주차 0명."><line x1="36" y1="162.0" x2="384" y2="162.0" stroke="var(--line)" stroke-width="1"/><text x="30" y="166.0" font-size="10.5" fill="var(--muted)" text-anchor="end">0</text><line x1="36" y1="121.4" x2="384" y2="121.4" stroke="var(--line)" stroke-width="1"/><text x="30" y="125.4" font-size="10.5" fill="var(--muted)" text-anchor="end">1,000</text><line x1="36" y1="80.8" x2="384" y2="80.8" stroke="var(--line)" stroke-width="1"/><text x="30" y="84.8" font-size="10.5" fill="var(--muted)" text-anchor="end">2,000</text><line x1="36" y1="40.2" x2="384" y2="40.2" stroke="var(--line)" stroke-width="1"/><text x="30" y="44.2" font-size="10.5" fill="var(--muted)" text-anchor="end">3,000</text><polyline points="36.0,162.0 62.8,151.8 89.5,141.7 116.3,131.5 143.1,121.4 169.8,111.2 196.6,101.1 223.4,90.9 250.2,80.8 276.9,70.6 303.7,60.5 330.5,50.3 357.2,40.2 384.0,30.0" fill="none" stroke="var(--f3)" stroke-width="2" stroke-linejoin="round"/><circle cx="62.8" cy="151.8" r="4.5" fill="var(--f4)" stroke="var(--card)" stroke-width="2"/><text x="62.8" y="140.8" font-size="11" fill="var(--ink)" text-anchor="middle" font-weight="700">1주</text><circle cx="143.1" cy="121.4" r="4.5" fill="var(--f4)" stroke="var(--card)" stroke-width="2"/><text x="143.1" y="110.4" font-size="11" fill="var(--ink)" text-anchor="middle" font-weight="700">1달</text><circle cx="384.0" cy="30.0" r="4.5" fill="var(--f4)" stroke="var(--card)" stroke-width="2"/><text x="384.0" y="19.0" font-size="11" fill="var(--ink)" text-anchor="end" font-weight="700">분기</text><circle cx="36.0" cy="162.0" r="5" fill="var(--red)"/><text x="47.0" y="178.0" font-size="11.5" fill="var(--red)" font-weight="700">지금 0명</text><text x="36" y="198" font-size="10.5" fill="var(--muted)">10/19</text><text x="143.1" y="198" font-size="10.5" fill="var(--muted)" text-anchor="middle">11/17</text><text x="384" y="198" font-size="10.5" fill="var(--muted)" text-anchor="end">2027/1/17</text></svg>\n  <figcaption>주 250명이 분기 3,000명 속도입니다. 한 주를 비우면 250명이 사라지고, 그만큼 1월 런칭 인원이 줄어듭니다. <b>빨간 점이 오늘입니다.</b></figcaption>\n</figure>\n\n<h2>구간별로 얻어야 하는 결과</h2>\n<div class="card">\n  <p style="margin:0 0 6px">각 구간에 <b>딱 하나</b>의 집중이 있습니다. 나머지는 그 하나를 떠받치는 것들입니다.</p>\n  <div class="note">네모는 끝났는지 아닌지 판정 가능한 것만 적었습니다. \'검토한다\' 같은 건 결과가 아닙니다.</div>\n</div>\n\n<div class="ms on">\n  <h3>1주 <span class="when">10/19 월 ~ 10/25 일</span></h3>\n  <ul>\n    <li>카페 신규 <b>250명</b></li>\n    <li>실측 CAC 한 개 — 쓴 광고비 ÷ 들어온 사람 수</li>\n    <li>6기 강의 런칭 완료 (10/25)</li>\n    <li>6:4의 분모 확정 — A안인가 B안인가 (<b>1,440만원</b> 차이)</li>\n    <li>종혁 본부장에게 과거 카페 월 4,000명 당시 광고비 확인</li>\n  </ul>\n  <div class="one"><b>이번 주의 하나 — 광고를 켜는 것.</b> 지금 0입니다. 다른 다섯이 다 밀려도 이건 월요일에 켜야 합니다. 분기 전체가 여기서 시작합니다.</div>\n</div>\n\n<div class="ms">\n  <h3>1달 <span class="when">~ 11/17</span></h3>\n  <ul>\n    <li>카페 누적 <b>1,000명</b> (4주 × 250)</li>\n    <li>도구공방 결제 가동 — 포트원 연결 완료</li>\n    <li>전자책 1종 발행 + <b>첫 결제 발생</b></li>\n    <li>가을님 촬영 완료 — 그 전에 손익분기 18명 사전 고지</li>\n    <li>CAC 4주 추세 확인 (오르는가 유지되는가)</li>\n    <li>11월 메이븐 정산 1,800만</li>\n  </ul>\n  <div class="one"><b>이번 달의 하나 — 첫 결제가 도는 것.</b> 금액은 상관없습니다. 3만원이라도 결제가 한 번 돌면 \'팔 수 있는 구조\'가 증명되고, 그때부터 광고를 늘릴 근거가 생깁니다.</div>\n</div>\n\n<div class="ms">\n  <h3>분기 <span class="when">~ 2027/1/17</span></h3>\n  <ul>\n    <li>카페 누적 <b>3,000명</b></li>\n    <li>1월 자사 강의 런칭 — <b>300명</b></li>\n    <li>12월 정산 2,300~2,800만 (메이븐 + 6기)</li>\n    <li>가을님 정산 500만 이상 = <b>23명</b></li>\n    <li>가정값 6개가 전부 실측값으로 바뀜</li>\n  </ul>\n  <div class="one"><b>이번 분기의 하나 — 1월 런칭 인원.</b> 누적 루크 수익 <b>2.27~2.32억</b>이 여기서 결정됩니다. 300명이면 1.79억, 150명이면 8,521만입니다.</div>\n</div>\n\n<div class="ms">\n  <h3>반기 <span class="when">~ 2027/4/17</span></h3>\n  <ul>\n    <li>2회차 런칭 완료 (4월) — 누적 <b>4.06~4.11억</b></li>\n    <li>카페 누적 6,400명</li>\n    <li>기존 500명에서 고가 <b>2명</b></li>\n    <li>여섯 엔진 중 <b>3개 이상</b>이 실제로 현금을 냄</li>\n  </ul>\n  <div class="one"><b>반기의 하나 — 반복이 되는가.</b> 1회는 운이고 2회는 시스템입니다. 2회차가 1회차의 70% 아래면 모델이 아니라 일회성 이벤트였던 겁니다.</div>\n</div>\n\n<div class="ms">\n  <h3>1년 <span class="when">~ 2027/10/17</span></h3>\n  <ul>\n    <li>분기 4회 완주 — 누적 <b>7.63~7.68억</b></li>\n    <li>카페 누적 12,000명 유입 / 구매자 1,200명</li>\n    <li>기존 회원 고가 <b>5~7명</b></li>\n    <li>상호변경 + 사무실 이전 등기 완료</li>\n  </ul>\n  <div class="one"><b>1년의 하나 — 광고를 끄면 멈추는가.</b> 멈춘다면 1년 동안 광고 대행사를 만든 것이고, 안 멈춘다면 자산을 만든 겁니다. 그 답은 <b>미전환 10,800명과 기존 500명이 광고 없이 얼마를 내는가</b>로 나옵니다.</div>\n</div>\n\n<h2>집중을 지키는 규칙 셋</h2>\n<div class="card gold">\n  <ul class="list">\n    <li><div class="t">1. 매일 09:00~09:30은 엔진 1</div><div class="m">요일과 무관. 목요일에도. 이걸 빼면 나머지 다섯 엔진의 모수가 사라집니다</div></li>\n    <li><div class="t">2. 구간마다 \'하나\'만 본다</div><div class="m">1주는 광고 켜기, 1달은 첫 결제, 분기는 런칭 인원. 나머지 항목이 밀려도 이 하나가 되면 그 구간은 성공입니다</div></li>\n    <li class="big"><div class="t">3. 2주 연속 70% 아래면 숫자를 내려 잡는다</div><div class="m">주 250명 대비. 희망 섞인 목표를 1월까지 들고 가면 그때 고치는 비용이 훨씬 큽니다</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  <b>근거</b>\n  <ul>\n    <li>과거 이력(롯데택배·마켓컬리, 법인 설립 2022-03-16, 수강생 약 3,000명, 유튜브 1만·카톡 1천) — 루크님이 그동안 말씀하신 것</li>\n    <li>현재 \'확정\' 줄 — 10월 메이븐 1,800만 수령, 6기 문의 80명, 초월스토리 루크 8% 합의는 모두 루크님 말씀 또는 노션 [결정] 기록</li>\n    <li>카페 유입 0명·도구공방 미연결·전자책 0종 — 2026-10-17 기준 아직 시작 전이라는 전제. <b>이미 진행된 것이 있으면 알려주시면 고칩니다</b></li>\n    <li>누적 수익 2.27억 / 4.06억 / 7.63억 — 분기당 루크 1.79억(B안, 300명·객단가 180만)에 11~12월 확정분과 가을님 768만을 더한 값. 전부 가정값 위에 쌓은 숫자입니다</li>\n    <li>주 250명 = 분기 3,000명 ÷ 12주. 13주차 3,250명은 선형 환산값</li>\n    <li>색 램프는 순서형(ordinal) 기준으로 밝기 단조·단일 색상·표면 대비를 검증해 밝은·어두운 테마 각각 통과시킨 값입니다</li>\n  </ul>\n</div>\n'

def write(path, html):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

# ---------------------------------------------------------------- 일십백천 전략 재평가
ILSIP = '<div class="hero">\n  <h1>일십백천 — 유지할 것과 바꿀 것</h1>\n  <div class="sub">수요가 적은 게 문제인가, 500명에서 8명을 집어내는 장치가 없는 게 문제인가</div>\n  <div class="goal">\n    <div><b>990만</b><span>일십백천 정가 (확인됨)</span></div>\n    <div><b>8.3명</b><span>자산 가치 48%를 지는 인원</span></div>\n    <div><b>1.7%</b><span>500명 중 그 8명의 비중</span></div>\n    <div><b>없음</b><span>지금 있는 선별 장치</span></div>\n  </div>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 8px">결론 먼저</h3>\n  <p style="margin:0 0 10px"><b>개편은 맞습니다. 다만 커리큘럼이 아니라 이름과 앞단입니다.</b></p>\n  <ul class="list">\n    <li><div class="t">커리큘럼 — 그대로 둡니다</div><div class="m">가볍게 만들면 자산 가치의 48%를 지고 있는 한 줄을 깎습니다</div></li>\n    <li><div class="t">이름과 약속 — 바꿉니다</div><div class="m">비용 0원. 지금 팔고 있는 이름과 실제 배송물이 어긋나 있습니다</div></li>\n    <li><div class="t">간단한 점수 — 신설합니다. 단 일십백천 안이 아니라 도구공방 앞단에</div><div class="m">점수는 상품이 아니라 선별기입니다</div></li>\n  </ul>\n  <div class="note">원크루는 말씀대로 이번 논의에서 제외했습니다.</div>\n</div>\n\n<h2>1. 지금 실제로 일어나고 있는 일</h2>\n<div class="card">\n  <p style="margin:0 0 10px">일십백천 수강생 컨설팅 기록에 실제로 올라온 주제들입니다.</p>\n  <ul class="list">\n    <li><div class="t">타오바오 소싱 · 수경 호환 재문의</div></li>\n    <li><div class="t">박스 후보 선정 · 일러스트 방향</div></li>\n    <li><div class="t">식품 파일럿 예산 600만 · 손절 기준</div></li>\n    <li><div class="t">수경 브랜드 10월 재시동 · 보조 품목 규칙 사전조사</div></li>\n    <li><div class="t">새 소싱 프로그램 진행 상황 공유</div></li>\n  </ul>\n  <div class="emph">이 중 \'브랜드 인큐베이팅\'으로 읽히는 건 <b>일러스트 방향 하나</b>입니다. 나머지는 전부 <b>무엇을 팔지 고르고, 얼마까지 걸고, 어디서 끊을지</b>에 대한 것입니다.</div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">수요가 적어 보이는 첫 번째 후보</h3>\n  <p style="margin:0">수요 그 자체가 아니라 <b>이 어긋남</b>입니다. 990만원을 쓰는 사람은 "브랜드를 인큐베이팅하고 싶어서" 결제하지 않습니다. <b>뭘 팔지 모르겠고 잃는 게 무서워서</b> 결제합니다. 지금 간판은 전자를 약속하는데, 안에서 배송되는 건 후자입니다.</p>\n  <div class="note">그래서 개편 1순위는 커리큘럼이 아니라 간판입니다. 돈도 시간도 들지 않습니다.</div>\n</div>\n\n<h2>2. "수요가 적다" — 맞지만 오진입니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">500명 자산 분석에서 나온 숫자를 확인된 정가로 다시 계산했습니다.</p>\n  <div class="kv">\n    <dt>500명 연 잠재력</dt><dd>1.72억</dd>\n    <dt>그중 고가 전환</dt><dd><b>8,250만 (48%)</b></dd>\n    <dt>÷ 990만</dt><dd><b>8.3명</b></dd>\n    <dt>500명 중 비중</dt><dd>1.7%</dd>\n  </div>\n</div>\n\n<figure class="fig">\n<svg viewBox="0 0 400 132" role="img" aria-label="500명 중 일십백천 구매자는 인원으로는 1.7퍼센트지만 가치로는 48퍼센트를 차지한다">\n  <text x="2" y="13" font-size="12" font-weight="700" fill="var(--ink)">인원</text>\n  <text x="398" y="13" font-size="11" fill="var(--muted)" text-anchor="end">8명 / 500명 · 1.7%</text>\n  <rect x="2" y="19" width="396" height="22" rx="3" fill="var(--f1)"/>\n  <rect x="2" y="19" width="6.6" height="22" rx="2" fill="var(--f4)"/>\n\n  <text x="2" y="69" font-size="12" font-weight="700" fill="var(--ink)">가치</text>\n  <text x="398" y="69" font-size="11" fill="var(--muted)" text-anchor="end">8,250만 / 1.72억 · 48%</text>\n  <rect x="2" y="75" width="396" height="22" rx="3" fill="var(--f1)"/>\n  <rect x="2" y="75" width="190" height="22" rx="3" fill="var(--f4)"/>\n\n  <rect x="2" y="115" width="10" height="10" rx="2" fill="var(--f4)"/>\n  <text x="17" y="124" font-size="11" fill="var(--muted)">일십백천 구매자</text>\n  <rect x="150" y="115" width="10" height="10" rx="2" fill="var(--f1)"/>\n  <text x="165" y="124" font-size="11" fill="var(--muted)">나머지 492명</text>\n</svg>\n<figcaption>같은 500명을 두 번 재면 이렇게 됩니다. 인원으로는 눈에 안 보이는 1.7%가 가치의 절반을 지고 있습니다.</figcaption>\n</figure>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">정정 — 필요한 성사 건수가 1.7배 늘었습니다</h3>\n  <p style="margin:0">500명 분석을 만들 때 저는 고가 단가를 <b>1,650만</b>으로 잡았고, 그래서 8,250만이 <b>5명</b>이었습니다. 확인된 정가는 <b>990만</b>입니다. 같은 8,250만을 만들려면 <b>5명이 아니라 8~9명</b>을 닫아야 합니다.</p>\n  <div class="note">선별 장치가 더 급해졌다는 뜻입니다. 감으로 5명을 찾는 것과 8~9명을 찾는 것은 다른 난이도입니다.</div>\n</div>\n\n<div class="card">\n  <p style="margin:0"><b>990만 티어는 수요가 적어야 정상인 티어입니다.</b> 연 8명이면 자산의 절반을 만듭니다. 300명을 모을 필요가 없는 상품에 "수요가 적다"는 진단을 붙이면, 고치지 않아도 되는 걸 고치게 됩니다.</p>\n  <div class="emph">병목은 수요 총량이 아니라 <b>500명에서 그 8명을 집어내는 장치</b>입니다. 그게 지금 없습니다.</div>\n</div>\n\n<h2>3. "린하지 못하게 만든다" — 맞지만 층을 잘못 지목했습니다</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">층</th><th style="white-space:nowrap">가격</th><th style="white-space:nowrap">연 인원</th><th>린해야 하나</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">전자책</td><td style="white-space:nowrap">3만</td><td style="white-space:nowrap">300명</td><td><b>린해야 함</b> — 당장 움직이는 게 전부</td></tr>\n      <tr><td style="white-space:nowrap">본강의</td><td style="white-space:nowrap">180만</td><td style="white-space:nowrap">300명</td><td><b>린해야 함</b> — 혼자 고쳐야 하니까</td></tr>\n      <tr><td style="white-space:nowrap">일십백천</td><td style="white-space:nowrap">990만</td><td style="white-space:nowrap">8~9명</td><td><b>깊어야 함</b> — 깊이를 산 사람입니다</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <p style="margin:10px 0 0">약 400편 영상 강의와 1:1을 990만에 산 사람에게 "빠르게 MVP 내고 피벗하세요"는 그가 산 물건이 아닙니다. 그는 <b>혼자 결정하지 않아도 되는 상태</b>를 샀습니다.</p>\n  <div class="emph">간단한 개념은 <b>아래로</b> 내려야 합니다. 일십백천을 깎는 데 쓰면 48% 한 줄을 깎습니다.</div>\n</div>\n\n<h2>4. 점수가 실제로 하는 일 — 상품이 아니라 선별기</h2>\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>a</b><span>린</span></div>\n    <div class="pgb">\n      <h3>오늘 재고 오늘 하나 고친다</h3>\n      <p style="margin:0">점수가 있으면 수강생이 "다음 주 강의까지 기다릴" 이유가 없어집니다. 피벗이 빨라집니다. 말씀하신 걱정을 정확히 해결하는 부분입니다.</p>\n    </div>\n  </div>\n</div>\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>b</b><span>욕구</span></div>\n    <div class="pgb">\n      <h3>격차가 숫자로 보이면 990만이 설득이 아니라 산수가 된다</h3>\n      <p style="margin:0">"지금 23점, 혼자 가면 45점, 같이 가면 80점." 이 문장은 설득이 아니라 비교입니다. 상담에서 가장 많이 걸리는 지점이 손실 공포인데, 격차가 숫자면 공포가 계산으로 바뀝니다.</p>\n    </div>\n  </div>\n</div>\n<div class="card accent">\n  <div class="pg">\n    <div class="pgn"><b>c</b><span>선별</span></div>\n    <div class="pgb">\n      <h3>500명이 점수대로 자동 분류된다</h3>\n      <p style="margin:0">낮으면 전자책·본강의, 높고 자본·시간이 있으면 일십백천 후보. <b>이게 지금 없는 바로 그것입니다.</b></p>\n      <div class="emph">(a)와 (b)는 수강생 편의입니다. <b>(c)가 매출입니다.</b> 루크에게 가장 값진 건 점수가 가르치는 기능이 아니라 <b>8명을 지목하는 기능</b>입니다.</div>\n    </div>\n  </div>\n</div>\n\n<h2>5. 확인된 것과 확인 못 한 것</h2>\n<div class="card blue">\n  <h3 style="margin:0 0 8px">확인된 것 — 정량화를 앞단에 두는 방향 자체</h3>\n  <p style="margin:0">자청 쪽 수업 후기(오픈애즈)에 따르면 수업의 핵심 원칙은 <b>"사업의 객관화와 정량화"</b>입니다. 감정적·추상적 표현 대신 숫자로 설명하게 만들고, 예시로 든 한 줄이 "10년 동안 뷰티 마케팅 1632개를 했습니다"입니다. 2시간 안에 자기 사업 소개 영상을 찍게 하는 <b>메타인지 훈련</b>도 나옵니다.</p>\n  <div class="note">점수라는 형태는 그 글에 없습니다. 다만 <b>정량화를 앞단에 두는 방향</b> 자체는 후기로 확인됩니다 — 가려는 방향은 맞습니다.</div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">확인 못 한 것 — V스코어의 실제 정의</h3>\n  <p style="margin:0 0 8px">검색 6회(자청 · 이상한마케팅 · 브이스코어 · V-Score · 사업 진단 조합)에서 <b>정의가 적힌 문서를 찾지 못했습니다.</b> 지어내지 않겠습니다.</p>\n  <p style="margin:0">위 4번의 (a)(b)(c)는 <b>\'점수라는 장치가 구조적으로 하는 일\'</b>이고, 자청 쪽 실제 설계가 아닙니다. 들으신 출처(라이브인지 유튜브인지 수업인지)를 주시면 실제 설계로 다시 평가합니다.</p>\n  <div class="warn">"엠타트업"도 검색으로 확인되지 않았습니다. 철자 확인 필요 — 엠스타트업·M스타트업으로도 안 나왔습니다.</div>\n</div>\n\n<h2>6. 그래서 무엇을 바꾸나</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th></th><th>지금</th><th>바꾼 뒤</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">이름·약속</td><td>브랜드 인큐베이팅</td><td><b>실제 하는 일로</b> — 뭘 팔지 고르고 어디서 끊을지 같이 앉아 돌리는 것</td></tr>\n      <tr><td style="white-space:nowrap">커리큘럼</td><td>약 400편 + 1:1</td><td>그대로</td></tr>\n      <tr><td style="white-space:nowrap">가격</td><td>990만</td><td>그대로</td></tr>\n      <tr><td style="white-space:nowrap">앞단</td><td>없음</td><td><b>점수 5문항</b> — 도구공방에</td></tr>\n      <tr><td style="white-space:nowrap">선별</td><td>감</td><td>점수대</td></tr>\n      <tr><td style="white-space:nowrap">원크루와의 관계</td><td>수료자가 올라오는 사다리</td><td>그대로 (이번 논의 제외)</td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<h2>7. 이 판단이 깨지는 조건</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">일십백천 수강생이 이미 충분히 많다면</div><div class="m">기록에서 확인되는 건 김종진 대표님과 익명 1명, <b>2명</b>입니다. 실제로 훨씬 많다면 선별기 얘기가 아니라 증설 얘기가 맞습니다 — 실제 인원 <b>확인 필요</b></div></li>\n    <li><div class="t">완주율·만족도가 낮다면</div><div class="m">"깊이를 유지하라"가 흔들립니다. 깊이를 팔았는데 배송이 안 되고 있다는 뜻이니까요 — <b>확인 필요</b></div></li>\n    <li><div class="t">500명 중 990만을 낼 수 있는 사람이 8명 미만이면</div><div class="m">48%는 종이 위 숫자입니다. 그러면 일십백천이 아니라 중간 티어(180만)를 두껍게 하는 게 맞습니다</div></li>\n  </ul>\n  <div class="note">세 조건 중 하나라도 걸리면 권고가 바뀝니다. 먼저 재고 그 다음에 고치는 순서입니다.</div>\n</div>\n\n<h2>8. 지금 할 일 셋</h2>\n<div class="card accent">\n  <ul class="list"><li><div class="t">1. 10/23 컨설팅에서 한 문장 질문</div><div class="m">"결제 직전에 가장 무서웠던 게 뭐였나요?" — 이 답이 새 간판의 원료입니다. 일정은 이미 잡혀 있습니다(타오바오 소싱·식품 파일럿 예산·손절 기준 점검).</div></li><li><div class="t">2. 점수 5문항 초안</div><div class="m">일십백천 커리큘럼에서 뽑아서 도구공방 앞단에 둡니다. 상품이 아니라 선별기이므로 무료 또는 전자책에 묶습니다.</div></li><li><div class="t">3. 수강생 실제 수와 완주율 세기</div><div class="m">아임웹 정리(정기결제 해지·환불 요청)할 때 강의실 로그로 같이 셉니다. 7번의 세 조건을 여기서 닫습니다.</div></li></ul>\n</div>\n\n<h2>확인 필요</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">V스코어의 실제 정의와 출처</div><div class="m">검색 6회 실패. 들으신 경로(라이브·유튜브·수업)</div></li>\n    <li><div class="t">"엠타트업" 정확한 철자·회사명</div></li>\n    <li><div class="t">일십백천 누적 수강생 수 · 완주율</div></li>\n    <li><div class="t">500명 중 990만 결제 가능 자본을 가진 인원</div></li>\n    <li><div class="t">고가 전환율</div><div class="m">500명 분석에서 제가 가정한 값입니다. 단가 990만은 확인됐지만 전환율은 아직 가정입니다</div></li>\n  </ul>\n</div>\n\n<p class="src">근거 — 가격(일십백천 990만 / 원크루 정가 3,900만 · 수강생 출신 3,300만): 루크 노션 가격표. 커리큘럼(약 400편 영상 + 1:1): <a href="../philosophy/">삼각 파이프라인</a>. 수강생 컨설팅 주제 5건: 노션 Action Item 기록(2026-09-20 · 09-30 · 10-01 · 10-23 · 10-31). 500명 자산 1.72억 · 고가 8,250만(48%): <a href="../engine/">식스 엔진</a> 500명 분석. 자청 쪽 수업 원칙(객관화·정량화, "뷰티 마케팅 1632개", 2시간 메타인지 미션): <a href="https://www.openads.co.kr/content/contentDetail?contsId=9383">오픈애즈 수업 후기</a>. V스코어 정의 및 "엠타트업": 확인 실패 — 지어내지 않았습니다.</p>\n'


# ---------------------------------------------------------------- 전략 재점검 (플라우드 3인)
REVIEW = '<div class="hero">\n  <h1>전략 재점검 — 남에게 가르친 것과 자기 회사</h1>\n  <div class="sub">플라우드 녹음 4건(신정현·뿌요·디노)에서 꺼낸 전략 정리와 전문가 6인 비평</div>\n  <div class="goal">\n    <div><b>16개</b><span>벌려 둔 전선 (기존 6 + 신규 10)</span></div>\n    <div><b>2배</b><span>광고비 900만 vs 1,800만 충돌</span></div>\n    <div><b>0개</b><span>손절 기준이 문서화된 엔진</span></div>\n    <div><b>3명</b><span>동시에 뽑겠다고 한 신규 인력</span></div>\n  </div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">먼저 — 오늘이 그 수요일입니다</h3>\n  <p style="margin:0">10/19 신정현님 회의에 <b>"정혁 본부장 수요일 출근"</b>이 Action Item으로 올라가 있습니다. 오늘(10/21)이 그날이고, 아래 <b>충돌 1</b>이 그 자리에서 닫아야 할 1번 의제입니다. 그거 하나만 닫아도 이 페이지 값은 합니다.</p>\n</div>\n\n<h2>세 대화에서 나온 것</h2>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">신정현 10-19 <span class="tag">68분</span></h3>\n  <p style="margin:0 0 8px"><b>확장.</b> 파트너 레벨에서 새 전선을 여는 회의였습니다.</p>\n  <ul class="list">\n    <li><div class="t">내수 + 역직구 플랫폼 2개 구축</div><div class="m">위너 시스템(카탈로그 매칭·최저가 우선 노출) · 플레이오토 연동 · 쇼피/아마존 단일 모체 계정</div></li>\n    <li><div class="t">물류 회전 프로모션</div><div class="m">출고 적은 요일(금요일) 건당 택배비 1,000원 지원</div></li>\n    <li><div class="t">오프라인 + 퀵커머스</div><div class="m">무인점포·샵인샵(올리브영 편의점화 벤치마킹) · 쿠팡이츠/배민 연계 2,000원 당일 직배송</div></li>\n    <li><div class="t">교육 린 전환</div><div class="m">주입식·밀착형 → VOD + 전자책 · 매주 월요일 무료 라이브 특강 + 과제 첨삭</div></li>\n    <li><div class="t">커뮤니티 개방</div><div class="m">통제형 → 오픈 단톡방, 자율 해결 원칙 · 주간/야간 질의응답 튜터 2명</div></li>\n    <li><div class="t">강사 라이선스</div><div class="m">콘텐츠 + 프로그램 제공하고 매출 10% 공유 또는 구독료</div></li>\n    <li><div class="t">조직</div><div class="m">책임자급 월 518만 수준 · 신규 수습 3개월 250만 → 정식 300만 · 유튜브 공고 · 지인 채용 지양 · \'기말고사\' 프레이밍</div></li>\n    <li><div class="t">장기</div><div class="m">무차입 성장 · 2년 집중 후 높은 밸류에이션 엑시트</div></li>\n  </ul>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 6px">뿌요(최근영) 10-19 <span class="tag">3시간 38분</span></h3>\n  <p style="margin:0 0 8px"><b>절제.</b> 뿌요님 코칭인데, 회사 로드맵이 여기서 가장 구체적으로 나왔습니다.</p>\n  <ul class="list">\n    <li><div class="t">2027년 서울 이전 — 성신여대·보문</div><div class="m">현 거점은 물류/3PL 전용, 신규 공간은 사무·강의·커뮤니티 오픈스페이스로 이원화</div></li>\n    <li><div class="t">2027년 1월 대규모 강의 런칭</div><div class="m"><b>광고비 1,800만</b> · 수강생 300명(전환율 10%) · 카페 월 신규 1,000명 × 3개월 = 총 3,000명</div></li>\n    <li><div class="t">그 외 런칭</div><div class="m">인베이더 강의 40~80명 · 가을님 리셀 강의 11월 말 런칭 45명 목표</div></li>\n    <li><div class="t">카르텔 배분</div><div class="m">기획 6 : 강사·운영 4</div></li>\n    <li><div class="t">뿌요님께 준 원칙 — 이게 핵심입니다</div><div class="m">광고비는 대출이 아니라 순수익에서 재투자 · ROAS &lt; 1 지속 시 즉시 손절 · 생활비(200~300만)와 사업 계좌 분리 · 3개월 유지=최소 실력, 1년=안정성, 3년=업계 인정 · 수익 하락 시 즉각 비용 절감 프로토콜 · 허영심 통제</div></li>\n  </ul>\n</div>\n\n<div class="card blue">\n  <h3 style="margin:0 0 6px">디노(김수민) 09-28 · 10-06 <span class="tag">30분 + 21분</span></h3>\n  <p style="margin:0 0 8px"><b>린.</b> 사흘 전 제가 \'점수\'를 제안했던 그 개념이, 이미 루크님 입에서 나와 있었습니다.</p>\n  <ul class="list">\n    <li><div class="t">09-28 — 린 MVP 방법론을 직접 가르침</div><div class="m">7~10일 짧은 주기로 아이템 하나 · AI로 2~3일 만에 전자책/상품페이지 MVP · 10만원 소액 광고로 즉시 반응 테스트 · 재미 없거나 성과 없으면 미련 없이 버리고 다음 · 짧게 3~5개, 길어도 30개 이내에 성공 아이템 발견</div></li>\n    <li><div class="t">09-28 — 그리고 \'점수\'의 원형</div><div class="m">AI로 실행 가능한 수익 아이템 100개를 <b>상대평가 학점(S, A+ …)과 예상 수익</b>으로 정리하게 함</div></li>\n    <li><div class="t">10-06 — 단가가 이미 깨져 있음</div><div class="m">힉스필드 영상 <b>1건당 약 20만원</b> · 크레딧 1200 소진에 10~20만원 · "수익성 악화 확인됨"</div></li>\n    <li><div class="t">10-06 — 루틴 고정</div><div class="m">3일 학습-제작 사이클 · 토 평가 / 일 재기획 / 월·화 학습 / 수 발행 · 릴스 매일 1개</div></li>\n  </ul>\n</div>\n\n<h2>충돌 1 — 광고비가 두 버전으로 존재합니다</h2>\n<div class="card">\n  <div class="kv">\n    <dt>식스 엔진 페이지</dt><dd>분기 광고 <b>900만</b> → 3,000명 (CAC 3,000원)</dd>\n    <dt>뿌요 세션 10-19</dt><dd>2027년 1월 광고비 <b>1,800만</b> → 3,000명 (CAC 6,000원)</dd>\n  </div>\n  <p style="margin:10px 0 0">같은 3,000명인데 숫자가 두 배입니다. 둘 중 하나는 틀렸고, 어느 쪽이 틀렸느냐에 따라 전체 모델의 절반이 움직입니다.</p>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">두 가지 해석, 전혀 다른 결과</h3>\n  <ul class="list">\n    <li><div class="t">(가) 예산을 1,800만으로 늘린 것이다</div><div class="m">비용이 분기당 900만 늘어납니다. 연 3,600만. 견딜 만합니다.</div></li>\n    <li><div class="t">(나) 실제 CAC가 6,000원이다</div><div class="m">900만으로는 <b>1,500명밖에 안 모입니다.</b> 전환 10%면 150명. 매출 5.4억 → 2.7억. <b>반토막입니다.</b></div></li>\n  </ul>\n</div>\n\n<figure class="fig">\n<svg viewBox="0 0 400 108" role="img" aria-label="같은 광고비 900만원으로 CAC 3000원이면 3000명, CAC 6000원이면 1500명이 모인다">\n  <text x="2" y="13" font-size="12" font-weight="700" fill="var(--ink)">광고 900만 · CAC 3,000원</text>\n  <text x="398" y="13" font-size="11" fill="var(--muted)" text-anchor="end">3,000명 → 5.4억</text>\n  <rect x="2" y="19" width="396" height="22" rx="3" fill="var(--f4)"/>\n\n  <text x="2" y="69" font-size="12" font-weight="700" fill="var(--ink)">광고 900만 · CAC 6,000원</text>\n  <text x="398" y="69" font-size="11" fill="var(--muted)" text-anchor="end">1,500명 → 2.7억</text>\n  <rect x="2" y="75" width="198" height="22" rx="3" fill="var(--f2)"/>\n</svg>\n<figcaption>예산을 안 늘리고 CAC만 두 배가 되면 이렇게 됩니다. 1월 런칭 하나에서 2.7억이 왔다 갔다 합니다.</figcaption>\n</figure>\n\n<div class="warn">종혁 본부장님께 오늘 물어볼 한 문장: <b>"과거에 카페 회원 1명 모으는 데 실제로 얼마 들었습니까?"</b> 이 답이 3,000원이면 식스 엔진이 맞고, 6,000원이면 모든 페이지의 7.14억을 다시 써야 합니다.</div>\n\n<h2>충돌 2 — 가르친 것과 하는 것이 다릅니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">이게 이번 정리에서 가장 날카로운 지점입니다. 루크님이 뿌요님과 디노님께 준 원칙을, 루크님 회사에 그대로 대 봤습니다.</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:42%">남에게 한 말</th><th>자기 회사는</th></tr></thead>\n    <tbody>\n      <tr><td>"7~10일 안에 안 되면 버려라"<br><small>→ 디노</small></td><td>신규 전선 10개를 한 회의에서 동시에 염. 기존 6개 위에 얹힘. <b>어느 것도 폐기 기한이 없음</b></td></tr>\n      <tr><td>"ROAS &lt; 1 지속 시 즉시 손절"<br><small>→ 뿌요</small></td><td>6개 엔진 중 손절 기준이 문서화된 것 <b>0개</b></td></tr>\n      <tr><td>"광고비는 대출이 아니라 순수익에서"<br><small>→ 뿌요</small></td><td>1월 광고비 1,800만의 출처가 명시되지 않음 — <b>확인 필요</b></td></tr>\n      <tr><td>"3개월 유지해야 최소 실력"<br><small>→ 뿌요</small></td><td>메이븐 1,800만은 10월·11월 2개월. 12월은 "20일 라이브 보고 결정". <b>아직 3개월 기준 미달</b></td></tr>\n      <tr><td>"수익 하락 시 즉각 비용 절감"<br><small>→ 뿌요</small></td><td>매출 확정 전에 서울 이전 + 3명 채용이 먼저 섭니다</td></tr>\n      <tr><td>"성과 없으면 미련 없이 폐기"<br><small>→ 디노</small></td><td>디노님 영상 건은 10-06에 이미 "수익성 악화 확인". <b>본인 기준대로면 손절 신호였는데 비용 절감 최적화로 갔습니다</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="emph">이건 능력 문제가 아니라 <b>비대칭</b>입니다. 남의 사업은 린하게 보면서 자기 사업은 전부 살려두고 있습니다. 코치가 자기 코칭을 안 받는 전형적인 형태입니다.</div>\n</div>\n\n<h2>전문가 6인 비평</h2>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px"><span class="tag">CFO</span> 매출이 아니라 고정비가 먼저 섭니다</h3>\n  <p style="margin:0 0 8px">신규 고정비로 올라온 것을 세어 보면 — 실행 인재 250만(수습)→300만, 튜터 2명(금액 미정), 서울 사무실(임대료 미정), 책임자급 518만. <b>확정된 것만 월 250만, 미정이 셋입니다.</b></p>\n  <p style="margin:0 0 8px">11~12월 확보 예상이 4,100~4,600만입니다. 여기서 신규 고정비 3개월치가 빠지고, 1월 광고비 1,800만(또는 900만)이 또 빠집니다. <b>무차입 원칙이면 이 전부가 현금에서 나옵니다.</b></p>\n  <div class="emph">판정: 채용과 이전을 <b>1월 런칭 정산 이후로 미루십시오.</b> 매출이 선행하지 않은 고정비는 무차입 원칙과 정면으로 충돌합니다. 뿌요님께 "생활비와 사업 계좌를 분리하라"고 하신 것과 같은 말입니다.</div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px"><span class="tag">유통·물류</span> 위너 시스템은 고객끼리 마진을 깎게 만듭니다</h3>\n  <p style="margin:0 0 8px">내수 사이트에 "동일 상품 간 가격 흥정·비교 구매", 역직구에 "최저가 선정 판매자 우선 노출". 그런데 <b>그 판매자들이 전부 루크님 수강생입니다.</b></p>\n  <p style="margin:0 0 8px">쿠팡 위너가 작동하는 건 쿠팡이 트래픽을 독점하고 있어서입니다. 판매자는 마진을 깎아도 거래량이 늘어나 남습니다. <b>트래픽이 없는 위너 시스템은 마진만 깎고 거래는 안 늘립니다.</b> 수강생 입장에서는 돈 내고 배운 뒤 돈 내고 서로 싸우는 구조가 됩니다.</p>\n  <div class="emph">판정: 위너(최저가 경쟁) 말고 <b>카탈로그 통합 + 중복 상품 1인 독점 노출</b>로 뒤집으십시오. 같은 상품에 여러 수강생이 걸리면 가격이 아니라 <b>선착순·기여도·재고 보유</b>로 한 명을 세웁니다. 그러면 플랫폼이 마진을 지켜 주는 쪽이 되고, 그게 수강생이 돈 내고 쓸 이유가 됩니다.</div>\n  <div class="note">퀵커머스 2,000원 · 30~60분 배송은 별건입니다. 단가가 성립하는지만 따로 보십시오 — <b>확인 필요</b>.</div>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 8px"><span class="tag">교육사업</span> 린 전환은 맞습니다. 단 층을 구분하십시오</h3>\n  <p style="margin:0 0 8px">"주입식·밀착형 → VOD + 전자책"은 <b>대중 강의층에서는 전적으로 옳습니다.</b> 그리고 이건 사흘 전 일십백천 판단과 충돌하지 않습니다. 린하게 바꾸자고 한 건 3만~180만 층이고, 990만 층이 아닙니다.</p>\n  <p style="margin:0 0 8px"><b>그리고 좋은 소식이 하나 있습니다.</b> 제가 "점수 선별기를 도구공방 앞단에 신설하라"고 했던 그 자리가, 이미 생겼습니다 — <b>매주 월요일 무료 라이브 + 과제 첨삭</b>입니다. 새 채널을 만들 필요가 없습니다. 월요일마다 점수를 재면 500명이 자동으로 분류됩니다.</p>\n  <p style="margin:0 0 8px">문항 설계도 이미 있습니다. 디노님께 시킨 <b>"아이템 100개를 상대평가 학점(S, A+)과 예상 수익으로 정리"</b>가 점수의 원형입니다.</p>\n  <div class="emph">판정: 점수를 새로 발명하지 마십시오. <b>디노님께 준 학점 체계 + 월요일 라이브</b> 두 개를 붙이면 끝납니다. 이번 주 안에 가능합니다.</div>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px"><span class="tag">조직·HR</span> \'기말고사\'는 평가가 아니라 통보입니다</h3>\n  <p style="margin:0 0 8px">책임자급 518만에 걸맞은 성과를 내야 한다는 건 맞습니다. 문제는 <b>평가 기준이 사후에 생기고 있다는 것</b>입니다. 기말고사는 시험 범위를 먼저 알려줘야 기말고사입니다. 범위 없이 보는 시험은 평가가 아니라 통보고, 통보는 조직에서 신뢰를 깎습니다.</p>\n  <p style="margin:0 0 8px">수습 250만 → 정식 300만도, <b>무엇을 하면 300만이 되는지</b>가 공고에 없으면 좋은 사람이 안 옵니다. 회의에서 "탁월한 인재는 이미 자기 사업을 한다"고 하셨는데, 맞습니다. 그런 사람을 250만으로 데려오려면 <b>돈이 아닌 것</b>을 줘야 합니다 — 지분, 매출 연동, 또는 자기 브랜드를 키울 자리.</p>\n  <div class="emph">판정: 3명 동시 채용은 과합니다. <b>실행 인재 1명만 먼저</b> 뽑고, 튜터 2명은 커뮤니티를 열어 본 뒤 실제 질문량을 보고 결정하십시오. 질문이 안 오면 튜터는 0명이어도 됩니다.</div>\n</div>\n\n<div class="card blue">\n  <h3 style="margin:0 0 8px"><span class="tag">M&amp;A</span> 지금 구조로는 2년 뒤 밸류가 안 나옵니다</h3>\n  <p style="margin:0 0 8px">"2년 집중 후 높은 밸류에이션 엑시트"가 목표인데, 매출의 대부분이 <b>루크님 얼굴과 이름에 붙어 있습니다.</b> 멘토루크 브랜드, 1:1 컨설팅, 라이브, 상담. 인수자는 창업자가 빠지면 매출이 빠지는 사업에 배수를 낮게 매깁니다. 교육업은 특히 그렇습니다.</p>\n  <p style="margin:0 0 8px">또 <b>무차입 + 2년 엑시트는 서로 당깁니다.</b> 무차입은 성장 속도를 제한하고, 인수자는 성장률을 봅니다. 둘 다 가지려면 자본 대신 <b>남의 매출</b>을 붙여야 하는데, 그게 정확히 회의에 나온 <b>강사 라이선스(매출 10% 또는 구독료)</b>입니다.</p>\n  <div class="emph">판정: 엑시트를 진짜 할 거면 오늘부터 KPI를 하나 추가하십시오 — <b>"루크 없이 나온 매출 비중 %"</b>. 강사 라이선스 건수와 그 매출이 이 지표입니다. 회의에 아이디어로는 올라왔지만 숫자 목표가 없습니다. 2년 뒤 이 비중이 40%를 넘지 않으면 엑시트는 희망사항입니다.</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px"><span class="tag">코치</span> 디노님 건은 본인 기준대로면 이미 손절이었습니다</h3>\n  <p style="margin:0 0 8px">09-28에 "7~10일 안에 성과 없으면 미련 없이 버려라"라고 하셨습니다. 10-06에 영상 1건 20만원, "수익성 악화 확인". 릴스를 매일 1개 올리면 <b>월 30건 × 20만 = 600만원</b>입니다. 디노님 상황에서 월 600만 제작비는 성립하지 않습니다.</p>\n  <p style="margin:0 0 8px">그런데 10-06 회의는 손절이 아니라 <b>비용 절감 최적화</b>로 갔습니다. 모델 비교, 프롬프트 수정 규칙, MCP 연동. 전부 합리적이지만, 전부 <b>이 아이템을 살리는 방향</b>입니다. 본인이 준 규칙대로면 이건 폐기하고 100개 리스트의 2번으로 넘어갈 자리였습니다.</p>\n  <div class="emph">판정: 디노님께 <b>단가 상한을 먼저 주십시오</b> — "영상 1건 2만원 안에 안 들어오면 이 아이템은 버린다." 숫자가 없으면 최적화는 무한히 계속됩니다. 그리고 같은 질문을 루크님 엔진 6개에도 던지십시오.</div>\n</div>\n\n<h2>종합 판정</h2>\n<div class="card accent">\n  <p style="margin:0 0 10px"><b>방향은 맞고, 개수가 틀렸습니다.</b></p>\n  <ul class="list">\n    <li><div class="t">맞는 것</div><div class="m">교육 린 전환 · 커뮤니티 개방 · 강사 라이선스 · 무차입 · 물류를 자산으로 보는 시각</div></li>\n    <li><div class="t">틀린 것</div><div class="m">전선 개수(16개) · 위너 시스템의 방향 · 채용·이전 타이밍 · 손절 기준 부재</div></li>\n    <li><div class="t">모르는 것</div><div class="m">실제 CAC. 이거 하나가 7.14억이냐 3.5억이냐를 가릅니다</div></li>\n  </ul>\n  <div class="emph">루크님은 <b>남의 사업을 진단하는 능력은 이미 증명됐습니다.</b> 뿌요님께 준 재무 원칙, 디노님께 준 린 방법론 — 둘 다 정확합니다. 부족한 건 통찰이 아니라 <b>그 통찰을 자기 회사에 적용하는 규율</b>입니다. 그래서 이번 주에 새로 배울 건 없습니다. 이미 아는 걸 자기한테 쓰면 됩니다.</div>\n</div>\n\n<h2>이번 주에 할 일 다섯</h2>\n<div class="card accent">\n  <ul class="list"><li><div class="t">1. 오늘(10/21) 종혁 본부장님께 CAC 확정</div><div class="m">"과거에 카페 회원 1명 모으는 데 실제로 얼마 들었습니까?" 3,000원이면 유지, 6,000원이면 전 페이지 수치 재작성.</div></li><li><div class="t">2. 엔진 6개에 손절 기준 한 줄씩</div><div class="m">"언제까지 얼마가 안 나오면 끈다." 6줄이면 끝납니다. 뿌요님께 준 ROAS 규칙을 자기 것으로 가져오는 작업입니다.</div></li><li><div class="t">3. 신규 10개를 3개로 줄이기</div><div class="m">남길 것 제안: 월요일 무료 라이브(점수 선별기 자리) · 강사 라이선스(엑시트 지표) · 역직구 1개. 나머지 7개는 1월 런칭 정산 후로.</div></li><li><div class="t">4. 채용 3명 → 1명</div><div class="m">실행 인재만. 튜터는 커뮤니티 열고 질문량 보고 결정.</div></li><li><div class="t">5. 디노님께 단가 상한 통보</div><div class="m">"영상 1건 N만원 안에 안 들어오면 버린다." 본인이 가르친 규칙을 본인 사람에게 적용.</div></li></ul>\n</div>\n\n<h2>확인 필요</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">실제 CAC — 3,000원인가 6,000원인가</div><div class="m">가장 급한 한 가지</div></li>\n    <li><div class="t">1월 광고비 1,800만의 출처</div><div class="m">11~12월 순수익에서 나오는지, 아니면 다른 데서 당겨오는지</div></li>\n    <li><div class="t">튜터 2명 인건비 · 서울 사무실 임대료</div><div class="m">신규 고정비 총액이 이 둘 없이는 안 나옵니다</div></li>\n    <li><div class="t">책임자급 518만이 기존 인력인지 신규인지</div></li>\n    <li><div class="t">퀵커머스 2,000원 · 30~60분 배송의 실제 단가</div><div class="m">배달 플랫폼 수수료 포함 시 성립하는지</div></li>\n    <li><div class="t">디노님 영상 건의 손절 단가 기준</div><div class="m">아직 정해진 숫자가 없습니다</div></li>\n  </ul>\n</div>\n\n<p class="src">근거 — 플라우드 녹음 4건: 「신정현 10-19 이커머스 비즈니스 확장 및 교육 사업 고도화 전략 회의」(68분) · 「뿌요 10-19 코칭 세션: 비즈니스 정상화 및 온·오프라인 확장 로드맵」(3시간 38분) · 「09-28 디노(김수민)의 성장과 사업 방향성 재정립을 위한 멘토링」(30분) · 「김수민 2026-10-06」(21분). 숫자(광고비·인원·급여·단가)는 각 녹음 요약에 적힌 값 그대로이고, CAC 6,000원(=1,800만÷3,000명), 월 600만(=30건×20만), 전선 16개(기존 6 + 신규 10)는 그 값으로 제가 한 산수입니다. 기존 모델 수치는 <a href="../engine/">식스 엔진</a>, 990만 티어 판단은 <a href="../ilsip/">일십백천</a> 참조.</p>\n'


# ---------------------------------------------------------------- 박종혁 계약서 초안
CONTRACT = '<div class="hero">\n  <h1>민트(박종혁) — 1차 계약서</h1>\n  <div class="sub">10/9 합의 내용 전부 반영 · 서명 가능한 완성본 · 2026.10.21</div>\n  <div class="goal">\n    <div><b>민트 6</b><span>수익 배분 (루크 4)</span></div>\n    <div><b>2,250만</b><span>3개월 비용 총 한도</span></div>\n    <div><b>7가지</b><span>제가 기준을 정한 항목</span></div>\n    <div><b>2칸</b><span>남은 빈칸 — 민트님 인적사항·계좌</span></div>\n  </div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">먼저 읽어 주십시오</h3>\n  <p style="margin:0 0 8px">저는 변호사가 아닙니다. 이 계약서는 <b>10월 9일 녹음에서 합의된 내용</b>과, 계약서에 반드시 들어가야 하는데 아직 안 정해진 항목에 대해 <b>제가 기준을 정해 채운 것</b>입니다. 서명 전에 변호사 또는 법무사 검토를 받으십시오.</p>\n  <p style="margin:0">제가 정한 7가지는 바로 아래에 모아 뒀습니다. <b>마음에 안 드는 칸은 말씀만 하시면 바꿉니다.</b></p>\n</div>\n\n<h2>제가 기준을 정한 일곱 가지</h2>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">① 배분 기준은 B안 — "수익"에서 비용을 먼저 뺍니다 <span class="tag">제6조</span></h3>\n  <p style="margin:0 0 8px"><b>배분 기준액 = 매출 − PG 수수료 − 광고비 − 외주비</b></p>\n  <p style="margin:0">근거 둘입니다. 하나, 10/9 녹음의 단어가 <b>"수익"</b>이지 "매출"이 아닙니다. 한국어에서 수익은 통상 비용을 뺀 뒤를 가리킵니다. 둘, 광고비와 외주비를 갑이 <b>전액</b> 부담하므로 그걸 빼지 않고 나누면 갑만 비용을 지고 분배는 6을 내주는 구조가 됩니다.</p>\n  <div class="warn">민트님은 A안(매출 기준)으로 이해하고 계실 수 있습니다. 그래서 계약서 맨 뒤에 <b>숫자 예시</b>를 붙였습니다. 서명 전에 이 예시를 같이 읽으시면 오해가 남지 않습니다.</div>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">② 외주(PD) 월 한도 150만원 → 3개월 총액 2,250만원 <span class="tag">제8조</span></h3>\n  <p style="margin:0">고정 용역비 900만 + 광고비 900만 + 외주비 450만 = <b>2,250만원</b>. 민트님이 [56:35]에서 "3개월 기준으로 천만 원"이라고 하신 것과는 차이가 있는데, 고정급만 900만이라 1,000만 안에는 광고비가 들어갈 자리가 없습니다. <b>한도(상한)로 적었으니 덜 쓰면 그만큼 안 나갑니다.</b></p>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">③ 광고는 계약 개시 후 14일 이내 집행 — 늦어도 11월 4일 <span class="tag">제8조</span></h3>\n  <p style="margin:0">날짜를 비워 두면 3,000명의 기한도 같이 사라집니다. 기한을 박아 두고, 집행이 늦어지면 성과 평가 시점만 그만큼 밀리게 했습니다.</p>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">④ 1월 강의 객단가 180만원 <span class="tag">제9조</span></h3>\n  <p style="margin:0">[58:33]에서 나온 값 그대로 넣었습니다. 서면 합의로 바꿀 수 있게 했습니다.</p>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">⑤ 월 300만원은 세전 · 사업소득 3.3% 원천징수 <span class="tag">제5조</span></h3>\n  <p style="margin:0">용역계약의 표준 처리입니다. 민트님이 사업자등록을 갖고 계시면 세금계산서 발행 + 부가세 별도로 전환할 수 있게 단서를 달았습니다.</p>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">⑥ 수익 정산일은 익월 22일 <span class="tag">제6조</span></h3>\n  <p style="margin:0">고정 용역비 지급일과 같은 날로 맞췄습니다. 송금이 한 번에 끝납니다.</p>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 6px">⑦ 고객 비유인 6개월 — 경업금지는 안 넣었습니다 <span class="tag">제12조</span></h3>\n  <p style="margin:0">겸업을 자유롭게 하시겠다고 [80:05]에서 말씀하셨으니 넓은 경업금지는 앞뒤가 안 맞습니다. 대신 <b>갑의 수강생·고객을 대상으로 한 동종 교육 상품 판매만</b> 종료 후 6개월 제한했습니다. 좁고 집행 가능한 선입니다.</p>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">계약서에서 뺀 것 — 추후 정하면 되는 것들</h3>\n  <ul class="list">\n    <li><div class="t">과거 카페 모집 단가(CAC)</div><div class="m">운영 판단에 필요한 숫자지 계약 조항이 아닙니다. 따로 여쭤보십시오</div></li>\n    <li><div class="t">커머스 카테고리 세부 품목</div></li>\n    <li><div class="t">오프라인 매장·역직구 확장</div></li>\n    <li><div class="t">PD 채용 주체와 R&amp;R</div></li>\n    <li><div class="t">4개월차 이후의 조건</div></li>\n  </ul>\n  <div class="note">이 다섯은 제16조(별도 합의 사항)에 "나중에 서면으로 정한다"고 넣어 뒀습니다. 지금 비워 둬도 계약은 성립합니다.</div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">서명 전에 한 번 더 — 근로자성</h3>\n  <p style="margin:0 0 8px">녹음에 있던 <b>주 4일 출근</b>을 말씀대로 제3조에 넣었습니다. 다만 주 4일 출근 + 사무실 고정 좌석 + 월 300만 고정급은 <b>근로자성 징표 셋</b>이 모인 모양입니다. 근로자로 판단되면 4대보험 소급·퇴직금·해고 제한이 따라붙어, 3개월 뒤 "성과 미달이니 종료"가 자유롭지 않게 될 수 있습니다.</p>\n  <div class="emph">변호사 검토 때 <b>이것 하나만은 꼭</b> 물어보십시오. 필요하면 출근 조항을 빼거나, 3개월 기간제 근로계약 + 수익 배분 별도 약정으로 나누는 방법이 있습니다.</div>\n</div>\n\n<h2 id="contract">계약서 본문</h2>\n\n<div class="card">\n<h3 style="margin:0 0 10px;text-align:center">공동사업 및 용역 계약서</h3>\n\n<p style="margin:0 0 12px">힐링디어스 주식회사(이하 "갑")와 박종혁(이하 "을")은 온라인 교육·커머스 사업의 공동 추진에 관하여 다음과 같이 계약을 체결한다.</p>\n\n<div class="kv">\n  <dt>갑</dt><dd>힐링디어스 주식회사 · 대표이사 유믿음<br>경기도 구리시 갈매순환로 154 A408호</dd>\n  <dt>을</dt><dd>박종혁 (사내 활동명 <b>민트</b>)<br>주소 [ ______ ] · 생년월일 [ ______ ] · 연락처 [ ______ ]</dd>\n</div>\n\n<h3>제1조 (목적)</h3>\n<p style="margin:0 0 10px">본 계약은 갑이 보유한 리셀 교육 노하우·물류 인프라·수강생 기반과, 을이 보유한 강의 기획·미디어 운영·커뮤니티 구축 역량을 결합하여 온라인 교육 및 커머스 사업을 공동으로 추진하고, 그 역할과 비용 부담 및 수익 배분을 정함을 목적으로 한다.</p>\n\n<h3>제2조 (계약 기간)</h3>\n<p style="margin:0 0 6px">① 본 계약의 기간은 <b>2026년 10월 21일부터 2027년 1월 20일까지 3개월</b>로 한다.</p>\n<p style="margin:0 0 6px">② 제10조의 성과 지표를 산정하는 기산일은 제8조 제1항의 광고 최초 집행일로 한다. 광고 집행이 계약 개시일보다 늦어지는 경우 성과 평가 시점은 그 지연 일수만큼 순연하되, 고정 용역비의 지급 기간은 제1항에 따른다.</p>\n<p style="margin:0 0 10px">③ 기간 만료 14일 전까지 일방이 서면으로 종료 의사를 통지하지 않으면 동일 조건으로 3개월 자동 연장된다.</p>\n\n<h3>제3조 (을의 업무)</h3>\n<p style="margin:0 0 6px">① 을은 <b>강의 런칭 프로젝트 담당</b>으로서 다음 업무를 수행한다.</p>\n<ul class="list">\n  <li><div class="t">1. 강의 기획 및 커리큘럼 설계</div></li>\n  <li><div class="t">2. 온드미디어(유튜브 등 자체 채널) 기획·운영</div></li>\n  <li><div class="t">3. 네이버 카페 등 커뮤니티 구축 및 활성화</div></li>\n  <li><div class="t">4. 화장품·건강기능식품 등 합의된 커머스 카테고리의 운영</div></li>\n  <li><div class="t">5. 광고 운영 및 유입 퍼널 설계</div></li>\n</ul>\n<p style="margin:10px 0 6px">② 을은 <b>주 4일</b> 갑이 제공하는 업무 공간에서 근무하는 것을 원칙으로 하되, 업무 수행의 구체적 방법과 시간은 을이 자율적으로 정한다.</p>\n<p style="margin:0 0 10px">③ 을은 주 1회 진행 상황을 갑에게 공유한다.</p>\n\n<h3>제4조 (갑의 업무 및 지원)</h3>\n<p style="margin:0 0 6px">갑은 다음을 제공한다.</p>\n<ul class="list">\n  <li><div class="t">1. 리셀·소싱 운영 노하우 및 교육 콘텐츠</div></li>\n  <li><div class="t">2. 물류(3PL) 시스템 — 일 2,000~5,000건 처리 역량</div></li>\n  <li><div class="t">3. 기존 수강생 기반 및 채널 자원</div></li>\n  <li><div class="t">4. 제8조에 따른 광고비 및 외주 제작비</div></li>\n  <li><div class="t">5. 업무 공간 및 집기</div></li>\n</ul>\n\n<h3>제5조 (고정 용역비)</h3>\n<p style="margin:10px 0 6px">① 갑은 을에게 계약 기간 3개월간 <b>매월 금 3,000,000원(세전)</b>을 다음 각 호의 날에 지급한다. 지급일이 토요일·일요일 또는 공휴일인 경우 <b>직전 영업일</b>에 지급한다.</p>\n<div class="wrapx">\n<table>\n  <thead><tr><th style="white-space:nowrap">회차</th><th style="white-space:nowrap">기준일</th><th style="white-space:nowrap">실제 지급일</th><th>비고</th></tr></thead>\n  <tbody>\n    <tr><td>1회</td><td>2026-11-22</td><td><b>2026-11-20 (금)</b></td><td>기준일이 일요일이라 직전 영업일</td></tr>\n    <tr><td>2회</td><td>2026-12-22</td><td><b>2026-12-22 (화)</b></td><td>그대로</td></tr>\n    <tr><td>3회</td><td>2027-01-22</td><td><b>2027-01-22 (금)</b></td><td>그대로</td></tr>\n  </tbody>\n</table>\n</div>\n<p style="margin:10px 0 6px">② 제1항의 금액은 세전 금액으로서, 갑은 관계 법령에 따른 <b>사업소득 원천징수세액(3.3%)</b>을 공제한 후 지급한다. 다만 을이 사업자등록을 갖추고 세금계산서를 발행하는 경우, 양 당사자는 서면 합의로 부가가치세 별도 지급 방식으로 전환할 수 있다.</p>\n<p style="margin:0 0 6px">③ 제1항의 고정 용역비는 <b>갑의 선투자</b>로서, 계약 기간 3개월 동안은 제6조의 수익 배분액에서 차감하지 아니한다.</p>\n<p style="margin:0 0 10px">④ 계약 개시일로부터 4개월째 되는 달부터는, 지급되는 고정 용역비를 해당 월 을의 수익 배분액에서 차감한다.</p>\n<p style="margin:0 0 10px">⑤ 지급 계좌 — [ ______ ] 은행 / 계좌번호 [ ______ ] / 예금주 [ ______ ]</p>\n\n<h3>제6조 (수익 배분)</h3>\n<p style="margin:10px 0 6px">① 제7조에 정한 대상 매출에서 발생한 수익은 <b>을 6 : 갑 4</b>의 비율로 배분한다.</p>\n<p style="margin:0 0 6px">② 제1항의 "수익"이라 함은 다음 산식에 따라 산정한 금액(이하 "배분 기준액")을 말한다.</p>\n<div class="emph" style="text-align:center"><b>배분 기준액 = 대상 매출 − PG 수수료 − 광고비 − 외주 제작비</b></div>\n<p style="margin:10px 0 6px">③ 배분 기준액이 음수인 달에는 배분을 실시하지 아니하며, 그 음수액은 다음 달 이후의 배분 기준액에서 순차적으로 공제한다.</p>\n<p style="margin:0 0 6px">④ 매출은 <b>결제 완료일</b>을 기준으로 인식하고, 환불·취소분은 그 환불이 발생한 달의 대상 매출에서 차감한다.</p>\n<p style="margin:0 0 6px">⑤ 정산은 매월 말일을 기준으로 산정하여 <b>익월 22일</b>(토요일·일요일·공휴일인 경우 직전 영업일)에 지급한다.</p>\n<p style="margin:0 0 10px">⑥ 갑은 정산 시 매출·수수료·광고비·외주비의 명세를 을에게 서면 또는 전자적 방법으로 제공한다.</p>\n\n<h3>제7조 (배분 대상 매출의 범위)</h3>\n<p style="margin:10px 0 6px">① 제6조의 배분 대상이 되는 매출은 <b>본 계약에 따라 신규로 기획·런칭한 교육 상품 및 커머스 상품의 매출</b>에 한한다.</p>\n<p style="margin:0 0 6px">② 다음 각 호의 매출은 배분 대상에서 <b>제외</b>한다.</p>\n<ul class="list">\n  <li><div class="t">1. 갑의 기존 3PL(물류 대행) 매출</div></li>\n  <li><div class="t">2. 갑의 기존 리셀 및 자체 커머스 매출</div></li>\n  <li><div class="t">3. 갑의 프로그램·소프트웨어 판매 및 구독 매출</div></li>\n  <li><div class="t">4. 본 계약 체결 이전에 모집이 개시된 강의의 매출</div></li>\n  <li><div class="t">5. 기타 양 당사자가 서면으로 제외하기로 합의한 매출</div></li>\n</ul>\n\n<h3>제8조 (비용 부담 및 한도)</h3>\n<p style="margin:10px 0 6px">① 갑은 광고비로 <b>월 금 3,000,000원</b>을 부담한다. 광고의 최초 집행은 <b>계약 개시일로부터 14일 이내</b>에 개시하며, 갑은 그 집행일을 을에게 서면으로 통지한다.</p>\n<p style="margin:0 0 6px">② 영상 제작 등 외주 비용은 <b>월 금 1,500,000원을 한도로</b> 갑이 부담한다.</p>\n<p style="margin:0 0 6px">③ 계약 기간 3개월간 갑이 부담하는 비용의 <b>총 한도는 금 22,500,000원</b>으로 한다(고정 용역비 900만 + 광고비 900만 + 외주비 450만). 이를 초과하는 지출은 사전 서면 합의가 있는 경우에만 집행한다.</p>\n<p style="margin:0 0 10px">④ 을이 갑의 사전 동의 없이 집행한 비용은 갑이 부담하지 아니한다.</p>\n\n<h3>제9조 (강의 런칭)</h3>\n<p style="margin:10px 0 6px">① 본 협업의 1차 강의 런칭은 <b>2027년 1월 중</b>에 실시하며, <b>2027년 1월 16일은 런칭일에서 제외</b>한다.</p>\n<p style="margin:0 0 6px">② 구체적 런칭일은 늦어도 <b>2026년 12월 20일</b>까지 양 당사자가 서면으로 확정한다.</p>\n<p style="margin:0 0 10px">③ 1차 강의의 기준 객단가는 <b>금 1,800,000원</b>으로 하며, 서면 합의로 변경할 수 있다.</p>\n\n<h3>제10조 (성과 기준과 계약의 지속)</h3>\n<p style="margin:10px 0 6px">① 본 계약의 핵심 성과 지표는 <b>제2조 제2항의 기산일로부터 3개월 내 네이버 카페 신규 회원 3,000명 유치</b>로 한다.</p>\n<p style="margin:0 0 6px">② 중간 점검은 매월 말 1회 실시하며, 2개월차 종료 시점에 누적 <b>1,800명</b>에 미달하는 경우 양 당사자는 즉시 조건 재협의에 들어간다.</p>\n<p style="margin:0 0 10px">③ 제1항의 달성 여부에 따라 양 당사자는 계약의 지속·조건 변경·종료를 협의하여 결정한다.</p>\n\n<h3>제11조 (산출물 및 자산의 귀속)</h3>\n<p style="margin:10px 0 6px">① 본 계약 기간 중 생성된 다음 자산은 <b>갑에게 귀속</b>한다.</p>\n<ul class="list">\n  <li><div class="t">1. 네이버 카페 및 그 회원 데이터</div></li>\n  <li><div class="t">2. 유튜브 등 온드미디어 채널 및 그 콘텐츠</div></li>\n  <li><div class="t">3. 강의 커리큘럼·교안·영상 등 교육 콘텐츠</div></li>\n  <li><div class="t">4. 수강생 및 고객 정보 일체</div></li>\n  <li><div class="t">5. 광고 계정 및 그 운영 데이터</div></li>\n</ul>\n<p style="margin:10px 0 6px">② 각 자산의 계정 소유자·관리자 권한은 <b>계약 개시와 동시에 갑 명의로 설정</b>하고, 을에게는 업무 수행에 필요한 범위의 권한을 부여한다.</p>\n<p style="margin:0 0 6px">③ 을이 기여한 콘텐츠에 대하여 을은 <b>본인의 포트폴리오 용도로 사용할 권리</b>를 가진다.</p>\n<p style="margin:0 0 10px">④ 계약 종료 시 을은 보유 중인 계정 권한·자료 일체를 <b>7일 이내</b>에 갑에게 반환 또는 이관하고, 사본을 파기한다.</p>\n\n<h3>제12조 (겸업 및 고객 비유인)</h3>\n<p style="margin:10px 0 6px">① 갑은 을이 본 계약 외의 사업 또는 업무를 겸하는 것을 <b>제한하지 아니한다.</b></p>\n<p style="margin:0 0 6px">② 다만 을은 계약 기간 중 및 종료 후 <b>6개월</b>간, 갑의 수강생·고객을 대상으로 본 계약과 동종의 교육 상품을 자기 또는 제3자의 계산으로 판매하지 아니한다.</p>\n<p style="margin:0 0 10px">③ 을은 본 계약 체결 시점에 제3자와 체결한 근로계약·용역계약 중 본 계약 수행에 저촉되는 것이 없음을 보증한다.</p>\n\n<h3>제13조 (비밀유지 및 개인정보)</h3>\n<p style="margin:10px 0 6px">① 양 당사자는 본 계약 수행 중 알게 된 상대방의 영업비밀·고객정보·매출정보를 제3자에게 누설하지 아니하며, 이 의무는 계약 종료 후 3년간 존속한다.</p>\n<p style="margin:0 0 10px">② 수강생 및 고객의 개인정보는 「개인정보 보호법」에 따라 처리하며, 을은 위탁받은 범위를 넘어 이를 이용하거나 외부로 반출하지 아니한다.</p>\n\n<h3>제14조 (법규 준수)</h3>\n<p style="margin:10px 0 10px">화장품·건강기능식품 등을 취급하는 경우 양 당사자는 「화장품법」, 「건강기능식품에 관한 법률」, 「전자상거래 등에서의 소비자보호에 관한 법률」, 「표시·광고의 공정화에 관한 법률」 등 관계 법령상 신고·표시·광고 규제를 준수한다. 위반으로 인한 행정처분·손해는 그 원인을 제공한 당사자가 부담한다.</p>\n\n<h3>제15조 (계약의 해지)</h3>\n<p style="margin:10px 0 6px">① 일방이 본 계약상 의무를 중대하게 위반하고 상대방의 서면 최고 후 14일 내에 시정하지 아니하는 경우, 상대방은 계약을 해지할 수 있다.</p>\n<p style="margin:0 0 6px">② 양 당사자는 <b>30일 전 서면 통지</b>로써 계약을 해지할 수 있다.</p>\n<p style="margin:0 0 10px">③ 해지 시 기 발생한 수익의 배분과 제11조의 자산 이관 의무는 그대로 유효하다.</p>\n\n<h3>제16조 (별도 합의 사항)</h3>\n<p style="margin:10px 0 6px">다음 각 호는 본 계약 체결 이후 양 당사자가 <b>서면으로 별도 합의</b>하여 정한다. 합의가 이루어지기 전까지는 본 계약의 효력에 영향을 미치지 아니한다.</p>\n<ul class="list">\n  <li><div class="t">1. 커머스 카테고리의 세부 품목과 운영 방식</div></li>\n  <li><div class="t">2. 오프라인 매장 및 역직구 사업으로의 확장</div></li>\n  <li><div class="t">3. 영상 제작 인력(PD)의 채용 주체와 역할</div></li>\n  <li><div class="t">4. 계약 개시일로부터 4개월째 이후의 보수 및 배분 조건</div></li>\n  <li><div class="t">5. 기타 양 당사자가 필요하다고 인정하는 사항</div></li>\n</ul>\n\n<h3>제17조 (분쟁의 해결)</h3>\n<p style="margin:10px 0 10px">본 계약에 정하지 아니한 사항은 상호 협의하여 정하고, 협의가 이루어지지 않을 경우 <b>갑의 본점 소재지를 관할하는 법원</b>을 제1심 관할 법원으로 한다.</p>\n\n<p style="margin:16px 0 10px">본 계약의 성립을 증명하기 위하여 2부를 작성하여 각 1부씩 보관한다.</p>\n\n<div class="kv">\n  <dt>계약일</dt><dd>2026년 10월 [ __ ]일</dd>\n  <dt>갑</dt><dd>힐링디어스 주식회사 대표이사 유믿음 &nbsp;(인)</dd>\n  <dt>을</dt><dd>박종혁 &nbsp;(인)</dd>\n</div>\n</div>\n\n<h2>별지 — 수익 배분 계산 예시</h2>\n<div class="card">\n  <p style="margin:0 0 10px">제6조 제2항의 산식을 숫자로 옮긴 것입니다. <b>서명 전에 민트님과 같이 읽으십시오.</b> 6:4를 매출 기준으로 오해하면 2월에 분쟁이 납니다.</p>\n  <p style="margin:0 0 10px"><b>가정</b> — 3개월간 수강생 60명 · 객단가 180만원 · PG 4% · 광고비 900만 · 외주비 450만</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>항목</th><th style="white-space:nowrap">금액</th></tr></thead>\n    <tbody>\n      <tr><td>대상 매출 (60명 × 180만)</td><td style="white-space:nowrap">1억 800만</td></tr>\n      <tr><td>− PG 수수료 4%</td><td style="white-space:nowrap">−432만</td></tr>\n      <tr><td>− 광고비</td><td style="white-space:nowrap">−900만</td></tr>\n      <tr><td>− 외주 제작비</td><td style="white-space:nowrap">−450만</td></tr>\n      <tr><td><b>배분 기준액</b></td><td style="white-space:nowrap"><b>9,018만</b></td></tr>\n      <tr><td>을(민트) 6 —</td><td style="white-space:nowrap"><b>5,411만</b></td></tr>\n      <tr><td>갑(멘토루크) 4 —</td><td style="white-space:nowrap"><b>3,607만</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <p style="margin:12px 0 0">여기에 고정 용역비 900만원을 더하거나 빼면 3개월 최종 손익입니다.</p>\n  <div class="kv">\n    <dt>을(민트) 최종</dt><dd>5,411만 + 고정 용역비 900만 = <b>6,311만원</b></dd>\n    <dt>갑(멘토루크) 최종</dt><dd>3,607만 − 고정 용역비 900만 = <b>2,707만원</b></dd>\n  </div>\n  <div class="note">같은 매출을 A안(매출 기준)으로 나누면 을이 6,221만, 갑이 4,147만에서 비용 2,250만을 전부 떠안아 1,897만이 됩니다. 두 안의 차이가 갑 기준 <b>810만원</b>입니다.</div>\n</div>\n\n<h2>남은 빈칸 — 민트님께 받을 것</h2>\n<div class="card gold">\n  <ul class="list">\n    <li><div class="t">주소 · 생년월일 · 연락처</div><div class="m">계약서 당사자 표시</div></li>\n    <li><div class="t">지급 계좌 — 은행 / 계좌번호 / 예금주</div><div class="m">제5조 제5항</div></li>\n  </ul>\n  <div class="note">이 둘만 채우면 서명할 수 있습니다. <a href="../park-terms/">조건 확인 페이지</a>에서 민트님이 직접 입력해 보내실 수 있게 해 뒀습니다.</div>\n</div>\n\n<p class="src">근거 — 합의 조건은 플라우드 녹음 「박종혁 본부장님 10-09 회의」(119분) 요약 및 전사 인용([54:56] 외주비 부담 · [56:35] 3개월 비용 · [58:33] 객단가 180만·카페 3,000명 · [59:29] 월 1,000명 · [60:41] 광고 월 300만 · [76:49] 고정급 300만 · [80:05] 겸업 자유 · [82:44] 배분의 취지). 수익 배분 민트 6 : 루크 4는 2026-10-21 루크님 확정. 고정급의 선투자·4개월차 차감은 10/10 루크님 확인. 근무 시작일·지급일·런칭일 제외일은 2026-10-21 루크님 지정. 위 \'제가 기준을 정한 일곱 가지\'는 녹음에 없는 항목에 대한 제 판단이며 법률 자문이 아닙니다. 계산 예시는 <a href="../park/">박종혁 본부장 협업 — 평가</a>의 손익표와 같은 전제로 산출했습니다.</p>\n'


# ---------------------------------------------------------------- 박종혁 협업 조건 요약 (외부 발송용)
TERMS = '<div class="hero">\n  <h1>협업 조건 정리</h1>\n  <div class="sub">멘토루크 × 민트(박종혁 본부장) · 강의 런칭 프로젝트</div>\n  <div class="goal">\n    <div><b>10/21</b><span>근무 시작</span></div>\n    <div><b>3개월</b><span>1차 기간</span></div>\n    <div><b>3,000명</b><span>카페 신규 회원 — 성과 기준</span></div>\n    <div><b>민트 6</b><span>수익 배분 (멘토루크 4)</span></div>\n  </div>\n</div>\n\n<div class="card accent">\n  <p style="margin:0 0 8px">민트님, 합류 축하드립니다. 10월 9일에 나눈 이야기를 조건 단위로 정리했습니다. <b>정해진 것</b>과 <b>아직 숫자가 안 정해진 것</b>을 나눠 적었습니다.</p>\n  <p style="margin:0">맨 아래 <b>입력란</b>에 인적사항과 계좌를 적어 주시고, 조건 중 다르게 보시는 부분이 있으면 같이 적어 주세요. 버튼을 누르면 메일로 보내거나 내용을 복사하실 수 있습니다.</p>\n</div>\n\n<h2>정해진 것</h2>\n<div class="card">\n  <div class="kv">\n    <dt>역할</dt><dd>민트 — <b>강의 런칭 프로젝트 담당</b></dd>\n    <dt>근무 시작</dt><dd><b>2026년 10월 21일 (수)</b></dd>\n    <dt>1차 기간</dt><dd>3개월 — 2027년 1월 20일까지</dd>\n    <dt>고정 용역비</dt><dd>월 300만원 × 3회</dd>\n    <dt>지급일</dt><dd><b>11/20(금)</b> · <b>12/22(화)</b> · <b>1/22(금)</b></dd>\n    <dt>지급일 규칙</dt><dd>기준일은 매월 22일, 주말·공휴일이면 직전 영업일<br><span class="note" style="display:inline-block;margin-top:4px">11월 22일은 일요일이라 11월 20일(금)에 드립니다</span></dd>\n    <dt>용역비 성격</dt><dd><b>선투자</b> — 3개월간은 수익 배분액에서 차감하지 않음. 4개월차부터 차감</dd>\n    <dt>광고비</dt><dd>월 300만원 — 멘토루크 부담</dd>\n    <dt>강의 런칭</dt><dd>2027년 1월 중 · <b>1월 16일은 제외</b></dd>\n    <dt>수익 배분</dt><dd><b>민트 6 : 멘토루크 4</b></dd>\n    <dt>배분 기준액</dt><dd>매출 − PG 수수료 − 광고비 − 외주 제작비<br><span class="note" style="display:inline-block;margin-top:4px">광고비·외주비를 멘토루크가 전액 부담하므로 이를 먼저 뺀 \'수익\'을 나눕니다</span></dd>\n    <dt>정산일</dt><dd>매월 말 산정 → 익월 22일 (용역비 지급일과 동일)</dd>\n    <dt>외주(PD) 한도</dt><dd>월 150만원</dd>\n    <dt>광고 집행</dt><dd>계약 개시 후 14일 이내 개시</dd>\n    <dt>1월 강의 객단가</dt><dd>180만원 기준</dd>\n    <dt>겸업</dt><dd><b>제한 없음</b></dd>\n    <dt>업무 방식</dt><dd>방법과 시간은 자율 · 주 1회 진행 공유</dd>\n  </div>\n</div>\n\n<h2>역할 분담</h2>\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>민</b><span>민트</span></div>\n    <div class="pgb">\n      <ul class="list">\n        <li><div class="t">강의 기획 및 커리큘럼 설계</div></li>\n        <li><div class="t">온드미디어(유튜브 등 자체 채널) 기획·운영</div></li>\n        <li><div class="t">네이버 카페 커뮤니티 구축·활성화</div></li>\n        <li><div class="t">화장품·건강기능식품 등 합의된 커머스 카테고리 운영</div></li>\n        <li><div class="t">광고 운영 및 유입 퍼널 설계</div></li>\n      </ul>\n    </div>\n  </div>\n</div>\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>루</b><span>멘토루크</span></div>\n    <div class="pgb">\n      <ul class="list">\n        <li><div class="t">리셀·소싱 운영 노하우 및 교육 콘텐츠</div></li>\n        <li><div class="t">물류(3PL) 시스템 — 일 2,000~5,000건 처리</div></li>\n        <li><div class="t">기존 수강생 기반 및 채널 자원</div></li>\n        <li><div class="t">광고비 및 외주 제작비 부담</div></li>\n        <li><div class="t">업무 공간</div></li>\n      </ul>\n    </div>\n  </div>\n</div>\n\n<h2>배분 대상이 되는 매출</h2>\n<div class="card">\n  <p style="margin:0 0 8px">본 협업으로 <b>새로 기획·런칭한 교육 상품과 커머스 상품</b>의 매출을 대상으로 합니다. 다음은 제외합니다.</p>\n  <ul class="list">\n    <li><div class="t">멘토루크의 기존 3PL(물류 대행) 매출</div></li>\n    <li><div class="t">멘토루크의 기존 리셀·자체 커머스 매출</div></li>\n    <li><div class="t">프로그램·소프트웨어 판매 및 구독 매출</div></li>\n    <li><div class="t">본 협업 전에 모집이 시작된 강의의 매출</div></li>\n  </ul>\n  <div class="note">기존에 돌아가던 사업과 새로 만드는 사업을 섞지 않으려는 구분입니다.</div>\n</div>\n\n<h2>성과 기준</h2>\n<div class="card">\n  <div class="kv">\n    <dt>핵심 지표</dt><dd>3개월 내 네이버 카페 신규 회원 <b>3,000명</b></dd>\n    <dt>기산일</dt><dd>광고 최초 집행일 (근무 시작일과 다를 경우 그만큼 순연)</dd>\n    <dt>중간 점검</dt><dd>매월 말 1회 · 2개월차에 누적 수치 확인</dd>\n    <dt>3개월 후</dt><dd>달성 여부를 보고 지속 · 조건 변경 · 종료를 협의</dd>\n  </div>\n</div>\n\n<h2>계정과 자산</h2>\n<div class="card">\n  <p style="margin:0 0 8px">카페 · 유튜브 채널 · 광고 계정 · 교육 콘텐츠 · 고객 정보는 <b>법인(힐링디어스) 명의</b>로 두고, 민트님께는 업무에 필요한 관리자 권한을 드립니다.</p>\n  <p style="margin:0">민트님이 만드신 콘텐츠는 <b>본인 포트폴리오로 자유롭게 사용</b>하실 수 있습니다.</p>\n  <div class="note">광고비와 운영비를 법인이 부담하기 때문에 자산을 법인에 두는 구조입니다. 계정은 처음 만들 때부터 이렇게 세팅하는 게 나중에 번거롭지 않습니다.</div>\n</div>\n\n<h2>수익 배분 계산 예시</h2>\n<div class="card">\n  <p style="margin:0 0 10px">6:4가 어디에 적용되는지 숫자로 보여 드립니다. <b>가정</b> — 3개월간 수강생 60명 · 객단가 180만원</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>항목</th><th style="white-space:nowrap">금액</th></tr></thead>\n    <tbody>\n      <tr><td>매출 (60명 × 180만)</td><td style="white-space:nowrap">1억 800만</td></tr>\n      <tr><td>− PG 수수료 4%</td><td style="white-space:nowrap">−432만</td></tr>\n      <tr><td>− 광고비</td><td style="white-space:nowrap">−900만</td></tr>\n      <tr><td>− 외주 제작비</td><td style="white-space:nowrap">−450만</td></tr>\n      <tr><td><b>배분 기준액</b></td><td style="white-space:nowrap"><b>9,018만</b></td></tr>\n      <tr><td>민트 6 —</td><td style="white-space:nowrap"><b>5,411만</b></td></tr>\n      <tr><td>멘토루크 4 —</td><td style="white-space:nowrap"><b>3,607만</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="kv">\n    <dt>민트님 최종</dt><dd>5,411만 + 고정 용역비 900만 = <b>6,311만원</b></dd>\n  </div>\n</div>\n\n<h2>추후 별도로 정할 것</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">커머스 카테고리의 세부 품목과 운영 방식</div></li>\n    <li><div class="t">오프라인 매장 및 역직구 확장</div></li>\n    <li><div class="t">영상 제작 인력(PD) 채용 주체와 역할</div></li>\n    <li><div class="t">4개월차 이후의 보수·배분 조건</div></li>\n  </ul>\n  <div class="note">지금 정하지 않아도 계약은 성립합니다. 필요할 때 서면으로 더하면 됩니다.</div>\n</div>\n\n<h2 id="form">입력란</h2>\n<div class="card gold">\n  <p style="margin:0">인적사항과 계좌를 적어 주시고, 위 조건 중 다르게 보시는 부분이 있으면 맨 아래에 적어 주세요. <b>입력 중인 내용은 이 브라우저에 자동 저장</b>되니 중간에 닫으셔도 괜찮습니다.</p>\n</div>\n\n<form id="f" class="card" onsubmit="return false">\n\n<h3>인적사항</h3>\n<input class="inp" type="text" name="addr" placeholder="주소">\n<input class="inp" type="text" name="birth" placeholder="생년월일 (예: 1985-03-12)">\n<input class="inp" type="text" name="tel" placeholder="연락처">\n\n<h3>지급 계좌</h3>\n<input class="inp" type="text" name="bank" placeholder="은행 / 계좌번호 / 예금주">\n\n<h3>확인해 주실 것</h3>\n<label class="opt"><input type="checkbox" name="c1"> 근무 시작일 <b>2026-10-21</b>이 맞습니다</label>\n<label class="opt"><input type="checkbox" name="c2"> 지급일 <b>11/20 · 12/22 · 1/22</b>가 맞습니다</label>\n<label class="opt"><input type="checkbox" name="c3"> 수익 배분 <b>민트 6 : 멘토루크 4</b>가 맞습니다</label>\n<label class="opt"><input type="checkbox" name="c4"> 배분 기준액이 <b>매출에서 PG·광고비·외주비를 뺀 금액</b>인 점에 동의합니다</label>\n<label class="opt"><input type="checkbox" name="c5"> 고정 용역비가 <b>3개월간 선투자, 4개월차부터 차감</b>인 점에 동의합니다</label>\n<label class="opt"><input type="checkbox" name="c6"> <b>배분 제외 범위</b>(기존 3PL·리셀·프로그램 매출)에 동의합니다</label>\n<label class="opt"><input type="checkbox" name="c7"> <b>계정·자산을 법인 명의</b>로 두는 것에 동의합니다</label>\n<label class="opt"><input type="checkbox" name="c8"> <b>겸업 제한 없음</b>을 확인했습니다</label>\n\n<h3>참고로 여쭙습니다 <small>계약 조건은 아닙니다</small></h3>\n<p class="hint">이전에 카페 월 4,000명 모으셨을 때의 광고 단가를 알려주시면, 월 300만원으로 월 1,000명이 현실적인 선인지 같이 계산해 보려 합니다</p>\n<input class="inp" type="text" name="cac" placeholder="예: 월 광고비 1,000만원 / 가입 1명당 2,500원">\n\n<h3>강의 런칭 희망일 <small>2027년 1월 중 · 16일 제외</small></h3>\n<input class="inp" type="date" name="launch">\n\n<h3>그 밖에 하실 말씀</h3>\n<p class="hint">조건 중 다르게 보시는 부분, 빠진 부분, 그 밖의 의견</p>\n<textarea class="inp" name="memo" rows="5" placeholder="자유롭게 적어 주세요"></textarea>\n\n<div class="btns">\n  <button type="button" class="btn primary" id="mailBtn">메일로 보내기</button>\n  <button type="button" class="btn" id="copyBtn">내용 복사하기</button>\n</div>\n<p class="hint" id="status" style="margin-top:8px"></p>\n<p class="hint">\'메일로 보내기\'를 누르면 기본 메일 앱이 열리고 내용이 채워집니다. 마지막에 <b>보내기</b>를 눌러 주세요. 메일 앱이 안 열리면 \'내용 복사하기\'로 복사해서 카톡으로 보내 주셔도 됩니다.</p>\n</form>\n\n<style>\n#f h3{margin:18px 0 6px;font-size:16px}\n#f h3:first-of-type{margin-top:0}\n#f h3 small{font-weight:400;color:var(--muted);font-size:13px}\n.opt{display:block;padding:10px 12px;margin:6px 0;border:1px solid var(--line);border-radius:10px;cursor:pointer;line-height:1.5}\n.opt:hover{border-color:var(--accent)}\n.opt input{margin-right:8px}\n.inp{display:block;width:100%;box-sizing:border-box;padding:11px 12px;margin:6px 0;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font:inherit;font-size:15px}\n.inp:focus{outline:2px solid var(--accent);outline-offset:-1px}\ntextarea.inp{resize:vertical}\n.hint{font-size:13px;color:var(--muted);margin:2px 0 4px}\n.btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}\n.btn{flex:1;min-width:140px;padding:14px 16px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--ink);font:inherit;font-size:15px;font-weight:700;cursor:pointer}\n.btn:hover{border-color:var(--accent)}\n.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}\n</style>\n\n<script>\n(function(){\n  var f=document.getElementById(\'f\'), K=\'park-terms-v1\';\n  var S=document.getElementById(\'status\');\n  function fields(){return f.querySelectorAll(\'input,textarea\');}\n  try{\n    var saved=JSON.parse(localStorage.getItem(K)||\'{}\');\n    fields().forEach(function(el){\n      if(el.type===\'checkbox\'){ if(saved[el.name]) el.checked=true; }\n      else if(el.type===\'radio\'){ if(saved[el.name]===el.value) el.checked=true; }\n      else if(saved[el.name]!=null) el.value=saved[el.name];\n    });\n  }catch(e){}\n  function save(){\n    try{\n      var o={};\n      fields().forEach(function(el){\n        if(el.type===\'checkbox\'){ if(el.checked) o[el.name]=1; }\n        else if(el.type===\'radio\'){ if(el.checked) o[el.name]=el.value; }\n        else if(el.value) o[el.name]=el.value;\n      });\n      localStorage.setItem(K,JSON.stringify(o));\n    }catch(e){}\n  }\n  f.addEventListener(\'input\',save);\n  f.addEventListener(\'change\',save);\n\n  function v(n){var el=f.elements[n];\n    if(!el) return \'\';\n    if(el.length && el[0] && el[0].type===\'radio\'){\n      for(var i=0;i<el.length;i++) if(el[i].checked) return el[i].value;\n      return \'\';\n    }\n    if(el.type===\'checkbox\') return el.checked?\'예 (확인함)\':\'— (아직 확인 안 하심)\';\n    return el.value||\'\';\n  }\n  function line(label,val){ return label+\': \'+(val?val:\'(미입력)\'); }\n  function build(){\n    var L=[];\n    L.push(\'멘토루크 × 민트 — 계약 조건 확인 회신\');\n    L.push(\'작성일: \'+new Date().toLocaleString(\'ko-KR\'));\n    L.push(\'\');\n    L.push(\'[인적사항]\');\n    L.push(line(\'주소\',v(\'addr\')));\n    L.push(line(\'생년월일\',v(\'birth\')));\n    L.push(line(\'연락처\',v(\'tel\')));\n    L.push(line(\'지급 계좌\',v(\'bank\')));\n    L.push(\'\');\n    L.push(\'[확인 항목]\');\n    L.push(line(\'근무 시작일 2026-10-21\',v(\'c1\')));\n    L.push(line(\'지급일 11/20 · 12/22 · 1/22\',v(\'c2\')));\n    L.push(line(\'수익 배분 민트 6 : 멘토루크 4\',v(\'c3\')));\n    L.push(line(\'배분 기준액 = 매출 − PG − 광고비 − 외주비\',v(\'c4\')));\n    L.push(line(\'선투자 후 4개월차 차감\',v(\'c5\')));\n    L.push(line(\'배분 제외 범위\',v(\'c6\')));\n    L.push(line(\'계정·자산 법인 명의\',v(\'c7\')));\n    L.push(line(\'겸업 제한 없음\',v(\'c8\')));\n    L.push(\'\');\n    L.push(line(\'[참고] 과거 카페 모집 단가\',v(\'cac\')));\n    L.push(line(\'[참고] 강의 런칭 희망일\',v(\'launch\')));\n    L.push(\'\');\n    L.push(\'[다르게 보시는 부분 / 그 밖의 의견]\');\n    L.push(v(\'memo\')||\'(없음)\');\n    return L.join(\'\\n\');\n  }\n  var to=[\'fund.mid16\',\'gmail.com\'].join(\'@\');\n  document.getElementById(\'mailBtn\').addEventListener(\'click\',function(){\n    var sub=\'[계약 조건 확인] 민트 — 멘토루크\';\n    location.href=\'mailto:\'+to+\'?subject=\'+encodeURIComponent(sub)+\'&body=\'+encodeURIComponent(build());\n    S.textContent=\'메일 앱을 여는 중입니다. 마지막에 보내기를 눌러 주세요.\';\n  });\n  document.getElementById(\'copyBtn\').addEventListener(\'click\',function(){\n    var t=build();\n    function done(){ S.textContent=\'복사했습니다. 카톡 등에 붙여넣어 주세요.\'; }\n    if(navigator.clipboard && navigator.clipboard.writeText){\n      navigator.clipboard.writeText(t).then(done,function(){fallback(t);});\n    } else fallback(t);\n    function fallback(txt){\n      var ta=document.createElement(\'textarea\');\n      ta.value=txt; ta.style.position=\'fixed\'; ta.style.opacity=\'0\';\n      document.body.appendChild(ta); ta.select();\n      try{document.execCommand(\'copy\'); done();}\n      catch(e){S.textContent=\'복사가 안 됩니다. 내용을 길게 눌러 직접 복사해 주세요.\';}\n      document.body.removeChild(ta);\n    }\n  });\n})();\n</script>\n\n<h2>다음 절차</h2>\n<div class="card accent">\n  <ul class="list"><li><div class="t">1. 위 입력란을 채워 보내 주시기</div></li><li><div class="t">2. 받은 내용으로 계약서 최종본 작성</div></li><li><div class="t">3. 양측 검토 후 서명</div></li></ul>\n</div>\n\n<p class="src">이 문서는 2026년 10월 9일 회의 내용을 바탕으로 정리한 <b>협의용 초안</b>이며, 그 자체로 법적 효력을 갖지 않습니다. 최종 조건은 서명된 계약서에 따릅니다. 입력하신 내용은 이 브라우저에만 저장되며, 버튼을 누르기 전에는 어디로도 전송되지 않습니다.</p>\n'


# ---------------------------------------------------------------- 11~2월 현금 흐름
CASH = '<div class="hero">\n  <h1>11월 ~ 2월 — 들어올 돈과 나갈 돈</h1>\n  <div class="sub">배분 구조 전부 확정 · 메이븐 5기 12/20 · 민트 라이브 1/20</div>\n  <div class="goal">\n    <div><b>1.2억</b><span>메이븐 격달 2,000만의 연 환산</span></div>\n    <div><b>24%</b><span>민트 건 루크님 지분</span></div>\n    <div><b>4,650만</b><span>11~1월 민트 건 선지출</span></div>\n    <div><b>2/22</b><span>민트 건 회수일</span></div>\n  </div>\n</div>\n\n<h2>배분 구조 — 네 건 전부 확정</h2>\n<div class="card accent">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>건</th><th>구조</th><th style="white-space:nowrap">루크 지분</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">메이븐</td><td>매출 − 광고비 → 인베이더 5:5 → 메이븐 6 : 루크 4</td><td style="white-space:nowrap">20%</td></tr>\n      <tr><td style="white-space:nowrap">가을님</td><td>전체 매출 8% + 가을님 정산액의 40% <small>(가을 6 : 루크 4)</small></td><td style="white-space:nowrap">8% + α</td></tr>\n      <tr><td style="white-space:nowrap">민트</td><td>매출 − 광고비 → 민트 6 : 우리 4 → 루크 6 : 메이븐 4</td><td style="white-space:nowrap"><b>24%</b></td></tr>\n      <tr><td style="white-space:nowrap">6기</td><td>자체 강의</td><td style="white-space:nowrap">—</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">민트 건에서 민트 60% · 루크 24% · 메이븐 16%입니다. 메이븐님이 두 건(메이븐 기수 + 민트 건)에 걸쳐 있습니다.</div>\n</div>\n\n<h2>메이븐 — 격달 2,000만이 깔립니다</h2>\n<div class="card">\n  <div class="kv">\n    <dt>3기</dt><dd>11월 정산 <b>약 2,000만</b></dd>\n    <dt>4기</dt><dd>12월 정산 <b>2,905만</b> — 65명 × 285만 = 매출 1억 8,525만</dd>\n    <dt>5기</dt><dd>강의 <b>2026-12-20</b>쯤</dd>\n    <dt>앞으로</dt><dd>기수를 1~2달에 한 번 열고, 루크님께 <b>격달 2,000만</b> 정산</dd>\n  </div>\n  <div class="emph">격달 2,000만이면 <b>연 6회 × 2,000만 = 1.2억</b>, 월평균 1,000만입니다. 다른 어느 엔진보다 먼저 깔리는 바닥 수입입니다 — 민트 건이 터지든 안 터지든 이건 돌아갑니다.</div>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">5기 정산이 1월인지 2월인지로 그림이 갈립니다</h3>\n  <p style="margin:0 0 8px">3기(11월)·4기(12월)는 연달아 들어오는데 앞으로는 격달이라고 하셨으니, 5기 강의가 12/20이면 정산은 1월 또는 2월입니다.</p>\n  <div class="kv">\n    <dt>A안 — 1월 정산</dt><dd>11~1월 수입 8,152~10,807만 → 순현금 <b>+3,452~+6,207만</b></dd>\n    <dt>B안 — 2월 정산</dt><dd>11~1월 수입 6,152~8,807만 → 순현금 <b>+1,452~+4,207만</b></dd>\n  </div>\n  <div class="note">1월은 지금 가을님 하나뿐이라 가장 얇은 달입니다. 5기 정산이 1월로 오면 1월이 편해집니다 — <b>메이브님께 확인하십시오</b>.</div>\n</div>\n\n<h2>월별 수입 — 루크님 몫</h2>\n<figure class="fig">\n<svg viewBox="0 0 400 128" role="img" aria-label="월별 루크 수입은 11월 2000만, 12월 3655만, 1월 1825만, 2월 7760만">\n  <text x="2" y="29" font-size="12" font-weight="700" fill="var(--ink)">11월</text>\n  <rect x="60" y="14" width="59" height="20" rx="3" fill="var(--f2)"/>\n  <text x="398" y="29" font-size="11" fill="var(--muted)" text-anchor="end">2,000만</text>\n\n  <text x="2" y="57" font-size="12" font-weight="700" fill="var(--ink)">12월</text>\n  <rect x="60" y="42" width="108" height="20" rx="3" fill="var(--f2)"/>\n  <text x="398" y="57" font-size="11" fill="var(--muted)" text-anchor="end">3,655만</text>\n\n  <text x="2" y="85" font-size="12" font-weight="700" fill="var(--ink)">1월</text>\n  <rect x="60" y="70" width="54" height="20" rx="3" fill="var(--f2)"/>\n  <text x="398" y="85" font-size="11" fill="var(--muted)" text-anchor="end">1,825만</text>\n\n  <text x="2" y="113" font-size="12" font-weight="700" fill="var(--ink)">2월</text>\n  <rect x="60" y="98" width="230" height="20" rx="3" fill="var(--f4)"/>\n  <text x="398" y="113" font-size="11" fill="var(--muted)" text-anchor="end">7,760만</text>\n</svg>\n<figcaption>B안(5기 2월 정산) · 6기 750만 · 가을님 1,825만 · 민트 150명 기준 중간값입니다. 11~1월에 민트 건으로 4,650만이 나갑니다.</figcaption>\n</figure>\n\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">월</th><th>항목</th><th style="white-space:nowrap">금액</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">11월</td><td>메이븐 3기</td><td style="white-space:nowrap">약 2,000만</td></tr>\n      <tr><td style="white-space:nowrap">12월</td><td>메이븐 4기</td><td style="white-space:nowrap">2,905만</td></tr>\n      <tr><td style="white-space:nowrap">12월</td><td>6기 강의 <small>10/25 결과</small></td><td style="white-space:nowrap">500~1,000만</td></tr>\n      <tr><td style="white-space:nowrap">1월</td><td>가을님 초월스토리</td><td style="white-space:nowrap">747~2,902만</td></tr>\n      <tr><td style="white-space:nowrap">1 or 2월</td><td>메이븐 5기</td><td style="white-space:nowrap">2,000만</td></tr>\n      <tr><td style="white-space:nowrap">2월</td><td>민트 라이브 <small>토스 정산</small></td><td style="white-space:nowrap">1,440~10,080만</td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<h2>민트 1월 라이브 — 2월 정산</h2>\n<div class="card">\n  <p style="margin:0 0 10px">객단가 180만 · 광고비 3,000만 차감 · 민트 6 : 우리 4 · 그 4에서 루크 6 : 메이븐 4</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">인원</th><th style="white-space:nowrap">매출</th><th style="white-space:nowrap">광고 차감 후</th><th style="white-space:nowrap">민트 60%</th><th style="white-space:nowrap">루크 24%</th><th style="white-space:nowrap">메이븐 16%</th></tr></thead>\n    <tbody>\n      <tr><td>50명</td><td style="white-space:nowrap">9,000만</td><td style="white-space:nowrap">6,000만</td><td style="white-space:nowrap">3,600만</td><td style="white-space:nowrap"><b>1,440만</b></td><td style="white-space:nowrap">960만</td></tr>\n      <tr><td>100명</td><td style="white-space:nowrap">1.8억</td><td style="white-space:nowrap">1.5억</td><td style="white-space:nowrap">9,000만</td><td style="white-space:nowrap"><b>3,600만</b></td><td style="white-space:nowrap">2,400만</td></tr>\n      <tr><td>150명</td><td style="white-space:nowrap">2.7억</td><td style="white-space:nowrap">2.4억</td><td style="white-space:nowrap">1.44억</td><td style="white-space:nowrap"><b>5,760만</b></td><td style="white-space:nowrap">3,840만</td></tr>\n      <tr><td>200명</td><td style="white-space:nowrap">3.6억</td><td style="white-space:nowrap">3.3억</td><td style="white-space:nowrap">1.98억</td><td style="white-space:nowrap"><b>7,920만</b></td><td style="white-space:nowrap">5,280만</td></tr>\n      <tr><td>250명</td><td style="white-space:nowrap">4.5억</td><td style="white-space:nowrap">4.2억</td><td style="white-space:nowrap">2.52억</td><td style="white-space:nowrap"><b>1.008억</b></td><td style="white-space:nowrap">6,720만</td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">손익분기 38명 · 객단가가 다 바꿉니다</h3>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">객단가</th><th style="white-space:nowrap">손익분기</th><th style="white-space:nowrap">150명일 때 루크</th></tr></thead>\n    <tbody>\n      <tr><td>150만</td><td>45명</td><td style="white-space:nowrap">4,680만</td></tr>\n      <tr><td>180만 <small>현재 가정</small></td><td>38명</td><td style="white-space:nowrap">5,760만</td></tr>\n      <tr><td>285만 <small>메이븐 4기 수준</small></td><td><b>24명</b></td><td style="white-space:nowrap"><b>9,540만</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="warn"><b>17명 아래로 팔리면 광고비 3,000만을 루크님이 전액 떠안습니다.</b> 1회성 런칭이라 계약서 제6조 ③의 "다음 달 이월"이 작동할 다음 달이 없습니다. 그 구간에서도 민트님은 고정 용역비 900만을 받습니다.</div>\n</div>\n\n<h2>가을님 — 1월 정산</h2>\n<div class="card">\n  <p style="margin:0 0 10px">매출 → PG 4% → <b>루크 8%</b> → 광고 4,500만 차감 → 초월스토리 : 가을 5:5 → 가을님 정산액에서 <b>가을 6 : 루크 4</b></p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">매출</th><th style="white-space:nowrap">인원</th><th style="white-space:nowrap">루크 8%</th><th style="white-space:nowrap">+ 가을 정산액 40%</th><th style="white-space:nowrap">루크 합계</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">6,500만</td><td>23명</td><td style="white-space:nowrap">499만</td><td style="white-space:nowrap">248만</td><td style="white-space:nowrap"><b>747만</b></td></tr>\n      <tr><td style="white-space:nowrap">1억</td><td>35명</td><td style="white-space:nowrap">768만</td><td style="white-space:nowrap">866만</td><td style="white-space:nowrap"><b>1,634만</b></td></tr>\n      <tr><td style="white-space:nowrap">1.5억</td><td>52명</td><td style="white-space:nowrap">1,152만</td><td style="white-space:nowrap">1,750만</td><td style="white-space:nowrap"><b>2,902만</b></td></tr>\n      <tr><td style="white-space:nowrap">2억</td><td>70명</td><td style="white-space:nowrap">1,536만</td><td style="white-space:nowrap">2,633만</td><td style="white-space:nowrap"><b>4,169만</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="warn">손익분기 <b>18명</b> 아래면 가을 대표님 몫이 0원입니다(광고 4,500만을 먼저 회수하는 구조). 그런데 루크님 8%는 그 구간에도 나옵니다. <b>촬영 전에 가을 대표님께 18명을 직접 말씀하십시오.</b> 나중에 알면 관계가 상합니다.</div>\n  <div class="note">8%의 기준이 전체 매출인지 PG 제외 매출인지가 남았습니다. 위 표는 PG 제외 기준이고, 전체 매출 기준이면 1억에서 32만 늘어납니다.</div>\n</div>\n\n<h2>지출 — 민트 건 (11~1월 선지출)</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>항목</th><th style="white-space:nowrap">금액</th><th>시점</th></tr></thead>\n    <tbody>\n      <tr><td>광고비</td><td style="white-space:nowrap">3,000만</td><td>11/6(금) 집행 시작</td></tr>\n      <tr><td>고정 용역비</td><td style="white-space:nowrap">900만</td><td>11/20(금) · 12/22(화) · 1/22(금)</td></tr>\n      <tr><td>영상 제작</td><td style="white-space:nowrap">700~800만</td><td>편당 100만 × 7~8편</td></tr>\n      <tr><td><b>합계</b></td><td style="white-space:nowrap"><b>4,600~4,700만</b></td><td>회수는 2/22</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">광고비 3,000만은 배분 전에 차감되니 최종적으로는 공동 부담입니다. 다만 <b>현금은 루크님이 먼저 씁니다.</b></div>\n</div>\n\n<h2>계약서 수정할 것</h2>\n<div class="card red">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>조항</th><th style="white-space:nowrap">계약서</th><th style="white-space:nowrap">실제</th></tr></thead>\n    <tbody>\n      <tr><td>제8조 ① 광고비</td><td style="white-space:nowrap">900만</td><td style="white-space:nowrap"><b>3,000만</b></td></tr>\n      <tr><td>제8조 ② 외주 한도</td><td style="white-space:nowrap">450만</td><td style="white-space:nowrap"><b>700~800만</b></td></tr>\n      <tr><td>제8조 ③ 총 한도</td><td style="white-space:nowrap">2,250만</td><td style="white-space:nowrap"><b>4,600~4,700만</b></td></tr>\n      <tr><td>제9조 런칭일</td><td style="white-space:nowrap">1월 중·16일 제외</td><td style="white-space:nowrap"><b>1/20(수)</b></td></tr>\n      <tr><td>제6조 ① 배분</td><td style="white-space:nowrap">을 6 : 갑 4</td><td style="white-space:nowrap">그 4를 <b>루크 6 : 메이븐 4</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="emph">총 한도가 <b>2배 넘게</b> 차이납니다. 10/30 영상팀 미팅에서 총액이 나오면 한 번에 고치겠습니다. 제6조에는 메이븐님 16%를 넣든가 별도 약정으로 빼든가 정하셔야 합니다.</div>\n</div>\n\n<h2>지금 걸리는 것 넷</h2>\n<div class="card accent">\n  <ul class="list">\n    <li><div class="t">1. 광고 3,000만을 한 번에 태우지 마십시오</div><div class="m">17명 아래면 전액 날립니다. 11/6 일부 집행 → <b>11/20 모집 결과를 보고 나머지</b>로 가면 하방이 막힙니다. 이게 이번 달 가장 돈 되는 결정입니다</div></li>\n    <li><div class="t">2. 1월 객단가를 10/30에 정하십시오</div><div class="m">180만은 10/9 분석의 가정값입니다. 메이븐 4기가 285만이었습니다. 285만이면 손익분기가 38명에서 <b>24명</b>으로, 150명 기준 루크님 몫이 5,760만에서 <b>9,540만</b>으로 바뀝니다</div></li>\n    <li><div class="t">3. 메이븐 5기 정산이 1월인지 2월인지</div><div class="m">1월은 지금 가을님 하나뿐이라 가장 얇습니다. 5기가 1월로 오면 1월 수입이 2배가 됩니다</div></li>\n    <li><div class="t">4. 가을 대표님께 손익분기 18명 사전 고지</div><div class="m">18명 아래면 가을님 몫이 0원인데 루크님 8%는 나옵니다. 촬영이 11월 초입니다</div></li>\n  </ul>\n</div>\n\n<h2>확인 필요</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">메이븐 5기 정산 시점 — 1월인지 2월인지</div></li>\n    <li><div class="t">메이븐 3기 2,000만의 정확한 금액과 입금 예정일</div><div class="m">"약 2,000만"으로 주셨습니다</div></li>\n    <li><div class="t">민트 건 광고 3,000만의 집행 일정</div><div class="m">한 번에인지 분할인지</div></li>\n    <li><div class="t">1월 강의 객단가</div></li>\n    <li><div class="t">가을님 8%의 기준</div><div class="m">전체 매출인지 PG 제외 매출인지 — 1억 기준 32만 차이</div></li>\n    <li><div class="t">민트 시나리오에 PG·토스 수수료를 넣을지</div><div class="m">말씀대로 광고비만 뺐습니다. 수수료가 따로 빠지면 각 구간이 3~4% 줄어듭니다</div></li>\n    <li><div class="t">메이븐님 16%를 계약서에 넣을지 별도 약정으로 뺄지</div></li>\n  </ul>\n</div>\n\n<p class="src">근거 — 배분 구조 네 건(메이븐 6:루크 4 · 가을 6:루크 4 · 민트 6:우리 4, 그 안에서 루크 6:메이븐 4), 메이븐 3기 약 2,000만·4기 65명×285만·5기 12/20·격달 2,000만 정산, 민트 건 광고비 3,000만과 토스 2월 정산: 2026-10-23 루크님 직접 확인. 런칭일 1/20·영상 편당 100만×7~8편·일정: 플라우드 「민트 / 다마고치 10-23 회의」. 가을님 5:5 구조와 광고 4,500만·손익분기 18명, 1월 객단가 180만: <a href="../engine/">식스 엔진</a>(10/9 분석). 계약 조항 번호: <a href="../park-contract/">민트 1차 계약서</a>. 각 구간 금액·손익분기·연 환산은 위 전제로 제가 계산한 값입니다.</p>\n'


# ---------------------------------------------------------------- 10/23 세 대화
OCT23 = '<div class="hero">\n  <h1>10월 23일 — 세 대화</h1>\n  <div class="sub">민트(오전) → 메이븐(22:32) → 돈벌쥐 조윤호 PD(23:08)</div>\n  <div class="goal">\n    <div><b>3,000명</b><span>카페에 이미 있는 회원</span></div>\n    <div><b>180만</b><span>객단가 확정</span></div>\n    <div><b>1,000만</b><span>예산이 늘어난 폭</span></div>\n    <div><b>10/24</b><span>PD에게 답 줘야 하는 날</span></div>\n  </div>\n</div>\n\n<h2>① 민트 — 다마고치 기획 (오전)</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">라이브 2027-01-20(수) 확정</div><div class="m">2월 설 전후 소비력 저하를 피하려는 판단</div></li>\n    <li><div class="t">일정</div><div class="m">10/30 영상팀·광고대행사 세팅 → 11/5 모집 촬영 → 11/6~20 모집 광고 → 11/30 첫 본편 → 12/5 첫 업로드 → 1/15 최종편 → 1/20 라이브</div></li>\n    <li><div class="t">영상 편당 100만 × 7~8편</div><div class="m">김한준 PD 회사</div></li>\n    <li><div class="t">퍼널</div><div class="m">유튜브 → 네이버 카페 + 오픈채팅(하루 2시간만 개방) · 30일 챌린지 + 크롤링 프로그램 무료 이용권</div></li>\n  </ul>\n</div>\n\n<h2>② 메이븐 — 인베이더 지속 여부와 비용 (22:32)</h2>\n<div class="card red">\n  <h3 style="margin:0 0 8px">인베이더가 흔들립니다</h3>\n  <ul class="list">\n    <li><div class="t">의장이 사업을 상품 중심으로 바꾸겠다고 했고, 그만둘 거라는 소문도 돌고 있음</div></li>\n    <li><div class="t">루크님은 "이번 성과 보고 인베이더와는 이번 과정 뒤에 안 하게 될 것 같다"</div></li>\n    <li><div class="t">PPT가 네 번 바뀜</div><div class="m">지난주엔 "숫자가 많아 어려우니 빼라" → 이번엔 "숫자가 부족하다". 민트님도 5기 때 "콘셉트를 완전히 갈아엎자"를 들음</div></li>\n    <li><div class="t">기획 지원이 없음</div><div class="m">트렌드헌터는 포지션이 겹치지 않게 조율해줬는데, 인베이더는 강사에게 강점·포지션을 찾아오라고 함. 광고비·채널·공간보다 <b>기획 지원</b>이 더 필요하다는 판단</div></li>\n    <li><div class="t">대안 검토 중</div><div class="m">PD가 소개한 매니지먼트 소속이면 광고비 제하고도 수익이 더 높을 가능성 · 역할 분산(가을=소규모 업체 / 대표=큰 업체 / 강사=개인 채널)</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">3,000만 예산에 동의하지 않으셨습니다</h3>\n  <div class="kv">\n    <dt>민트 제안</dt><dd>용역 900 + 광고 900 = 1,800만이 먼저, 거기에 <b>8회 × 100만 = 800만</b></dd>\n    <dt>당초 생각</dt><dd>광고비 월 300만 안에서 100만 정도만 더 → 총 <b>2,000만</b></dd>\n    <dt>늘어난 폭</dt><dd><b>약 1,000만</b></dd>\n    <dt>루크님 의견</dt><dd>"회당 30만이면 충분" · "월 4회 400만이면 그 돈으로 PD를 고용하겠다" · 라이브 스튜디오도 없는 상황</dd>\n  </div>\n</div>\n\n<figure class="fig">\n<svg viewBox="0 0 400 96" role="img" aria-label="민트 제안은 용역과 광고 1800만에 촬영 800만을 더해 2600만, 회당 30만이면 촬영이 240만으로 줄어 총 2040만">\n  <text x="2" y="30" font-size="12" font-weight="700" fill="var(--ink)">민트 제안</text>\n  <rect x="86" y="16" width="159" height="22" rx="3" fill="var(--f2)"/>\n  <rect x="245" y="16" width="71" height="22" rx="3" fill="var(--f4)"/>\n  <text x="398" y="31" font-size="11" fill="var(--muted)" text-anchor="end">2,600만</text>\n\n  <text x="2" y="68" font-size="12" font-weight="700" fill="var(--ink)">회당 30만</text>\n  <rect x="86" y="54" width="159" height="22" rx="3" fill="var(--f2)"/>\n  <rect x="245" y="54" width="21" height="22" rx="3" fill="var(--f4)"/>\n  <text x="398" y="69" font-size="11" fill="var(--muted)" text-anchor="end">2,040만</text>\n\n  <rect x="86" y="86" width="9" height="9" rx="2" fill="var(--f2)"/>\n  <text x="100" y="94" font-size="10" fill="var(--muted)">용역 900 + 광고 900</text>\n  <rect x="245" y="86" width="9" height="9" rx="2" fill="var(--f4)"/>\n  <text x="259" y="94" font-size="10" fill="var(--muted)">촬영비</text>\n</svg>\n<figcaption>차이는 전부 촬영비입니다. 8회 기준 800만 vs 240만 — <b>560만</b>이 여기서 갈립니다.</figcaption>\n</figure>\n\n<h2>③ 돈벌쥐 조윤호 PD — 공동 프로젝트 제안 (23:08)</h2>\n<div class="card accent">\n  <ul class="list">\n    <li><div class="t">촬영 외주가 아니라 <b>수익 배분 공동 프로젝트</b></div><div class="m">루크님이 먼저 제안하신 형태입니다 — 촬영·편집·기획·채널 운영을 PD가 맡고 수익을 퍼센티지로 배분. PD님도 긍정적으로 받으셨고 기획도 직접 한다고 함</div></li>\n    <li><div class="t">1~2월 영상 5~8개, 영상별 광고 집행</div></li>\n    <li><div class="t">카페 — 현재 <b>3,000명</b>, 추가 3,000명 목표</div></li>\n    <li><div class="t">전환율 최고 10% / 현실 가정 <b>5% → 150명</b> · 강의비 <b>180만</b></div></li>\n    <li><div class="t">미확정</div><div class="m">PD 역할 범위(라이브 지원 포함 여부)와 <b>수익 배분 퍼센티지</b></div></li>\n    <li><div class="t">뷰셀(메이븐)님 다음 기수 라이브는 <b>12월 중순</b></div><div class="m">뷰셀님 측 강의 기획사 미팅도 PD가 컨택하기로</div></li>\n  </ul>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">PD 일정이 12월에 막혀 있습니다</h3>\n  <div class="kv">\n    <dt>12월 둘째·셋째 주</dt><dd>금토일 2박 3일 × 2회 (스키장협회 — 엘리시안 강촌, 춘천·태백)</dd>\n    <dt>격주 금요일</dt><dd>TV조선 촬영</dd>\n    <dt>10/25(일) ~ 10/29(목)</dt><dd>태국 출장 — ESIM 연락 가능하나 응답 지연</dd>\n    <dt>내일 통화 가능</dt><dd><b>12:30 이전 또는 17시 이후</b></dd>\n  </div>\n  <div class="warn">민트 일정의 <b>11/30 첫 본편 촬영 · 12/5 첫 업로드</b>가 PD의 12월 둘째·셋째 주 공백과 맞물립니다. 12월 촬영분은 <b>11월 안에 당겨 찍어야</b> 1/15 최종편이 지켜집니다.</div>\n</div>\n\n<h2>숫자가 어긋난 곳 — 3,000만의 정체</h2>\n<div class="card red">\n  <p style="margin:0 0 8px">아까 "비용은 3천만원 광고비로 빼달라"고 하셔서 저는 <b>광고비만 3,000만</b>으로 계산했습니다. 그런데 녹음을 보면 3,000만은 <b>총 예산</b>입니다 — 용역 900 + 광고 900 + 촬영 800.</p>\n  <div class="kv">\n    <dt>현금 흐름 페이지</dt><dd>광고 3,000 + 용역 900 + 영상 750 = <b>선지출 4,650만</b> — <b>틀렸습니다</b></dd>\n    <dt>실제</dt><dd>총 <b>3,000만</b> 안에 셋이 다 들어 있음</dd>\n  </div>\n  <p style="margin:10px 0 0">2월 시나리오표(매출 − 3,000만 → 민트 6 : 우리 4)는 그대로 유효합니다. <b>선지출 금액만 4,650만 → 3,000만으로 내려갑니다.</b> 11~1월 현금은 그만큼 좋아집니다.</p>\n  <div class="warn">다만 <b>용역비 900만이 3,000만 안에 포함되는지</b>가 남습니다. 계약서 제5조 ③은 "고정 용역비는 갑의 선투자로서 수익 배분액에서 차감하지 아니한다"입니다. 3,000만에 용역비가 들어가면 이 조문과 충돌합니다 — 150명 기준 <b>588만</b> 차이입니다.</div>\n</div>\n\n<h2>가장 큰 것 — 바닥 수입의 전제가 흔들립니다</h2>\n<div class="card red">\n  <p style="margin:0 0 8px">어제 제가 "메이븐 격달 2,000만이 바닥을 깔아준다, 민트 건이 터지든 안 터지든 돌아간다"고 했습니다. <b>그 전제가 오늘 흔들렸습니다.</b></p>\n  <p style="margin:0 0 8px">메이븐 기수 수익은 <b>인베이더와 5:5</b> 구조입니다. 인베이더 의장이 상품 중심으로 돌아서고 루크님도 "이번 과정 뒤에는 안 하게 될 것 같다"고 하셨으면, <b>연 1.2억짜리 바닥 수입이 5기나 6기에서 끊길 수 있습니다.</b></p>\n  <div class="emph">11~2월 안에서는 3기·4기·5기가 이미 걸려 있어 괜찮습니다. 문제는 <b>그 다음</b>입니다. 인베이더 없이 메이븐 기수를 계속 돌릴 수 있는지 — 그게 되면 5:5가 빠져서 루크님 몫이 오히려 <b>두 배</b>가 되고, 안 되면 바닥이 사라집니다.</div>\n</div>\n\n<h2>지금 테이블 위에 있는 선택지</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">안</th><th>내용</th><th style="white-space:nowrap">비용</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">A</td><td>민트 제안대로 — 김한준 PD 회사에 8회 × 100만</td><td style="white-space:nowrap">2,600~3,000만</td></tr>\n      <tr><td style="white-space:nowrap">B</td><td>촬영 단가만 낮춤 — 회당 30만</td><td style="white-space:nowrap">약 2,040만</td></tr>\n      <tr><td style="white-space:nowrap">C</td><td><b>돈벌쥐 PD 공동 프로젝트</b> — 촬영·편집·기획·채널을 수익 배분으로</td><td style="white-space:nowrap">현금 지출 최소</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">C는 현금이 안 나가는 대신 지분이 나갑니다. 민트 60% · 루크 24% · 메이븐 16%에서 PD 몫을 어디서 떼느냐가 쟁점입니다 — 민트 몫에서인지, 우리 4에서인지, 배분 전 매출에서인지.</div>\n</div>\n\n<h2>내일(10/24) PD에게 연락하기 전에 정할 것</h2>\n<div class="card accent">\n  <ul class="list">\n    <li><div class="t">1. PD 몫을 어디서 뗄지</div><div class="m">PD 통화 전에 이것만은 정해져 있어야 숫자를 말할 수 있습니다. 배분 전 매출에서 떼면 민트·루크·메이븐이 같이 부담하고, 우리 4에서 떼면 루크·메이븐만 부담합니다</div></li>\n    <li><div class="t">2. PD 역할 범위 — 라이브 지원 포함인지</div><div class="m">1/20 라이브 운영까지면 지분이 커질 수밖에 없습니다</div></li>\n    <li><div class="t">3. 3,000만에 용역비 900만이 포함인지</div><div class="m">민트님과 먼저 닫아야 PD에게 제시할 예산이 나옵니다</div></li>\n    <li><div class="t">4. 12월 촬영분을 11월에 당겨 찍는 일정</div><div class="m">PD 12월 공백이 확정적입니다</div></li>\n  </ul>\n  <div class="note">PD는 모레(10/25)부터 목요일까지 태국입니다. <b>내일 오전 12:30 이전</b>이 가장 깨끗한 창입니다.</div>\n</div>\n\n<h2>확인 필요</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">3,000만의 정확한 구성 — 용역비 포함 여부</div></li>\n    <li><div class="t">카페 기존 3,000명의 성격</div><div class="m">유료 수강생인지 무료 가입자인지. 1/20 라이브에 그대로 뿌릴 수 있는 사람들인지</div></li>\n    <li><div class="t">인베이더 없이 메이븐 기수를 돌릴 수 있는지</div><div class="m">연 1.2억이 걸린 질문입니다</div></li>\n    <li><div class="t">다음 주 화요일(10/27) 미팅의 상대</div><div class="m">민트님인지 PD인지 다른 업체인지</div></li>\n    <li><div class="t">"다른 업체"와 매니지먼트의 실체</div><div class="m">PD가 소개한 곳이 어디인지</div></li>\n  </ul>\n</div>\n\n<p class="src">근거 — 플라우드 녹음 3건: 「민트 / 다마고치 10-23 회의」(22분) · 「민트님 프로젝트기획 협의: 인베이더 지속 여부와 촬영·채널 운영 비용」(21분, 10/23 22:32) · 「돈벌쥐 조윤호 PD님_261023_2254」(15분, 23:08). 녹음 요약의 고유명사 표기가 일부 흔들려(인메이저·돈보이즈·신종교 등) 문맥으로 바로잡았습니다 — 틀린 곳이 있으면 알려주십시오. 촬영비 비교 금액과 588만 차이는 위 전제로 제가 계산한 값입니다. 기존 수치는 <a href="../cash/">11~2월 현금 흐름</a>, 계약 조항은 <a href="../park-contract/">민트 1차 계약서</a>.</p>\n'


# ---------------------------------------------------------------- 조윤호 PD 파트너십
PDDEAL = '<div class="hero">\n  <h1>조윤호 PD — 장기 파트너십 설계</h1>\n  <div class="sub">11/2(월) 16시 통화용 · 10/28 RS 논의와 10/30 3자 미팅 반영</div>\n  <div class="goal">\n    <div><b>3층</b><span>보상 구조 — 고정 · 구간 · 장기</span></div>\n    <div><b>662만</b><span>2.7억 때 루크님이 더 쓰는 돈</span></div>\n    <div><b>2,760만</b><span>같은 조건에서 PD가 받는 돈</span></div>\n    <div><b>2단계</b><span>지금은 1단계만 합의</span></div>\n  </div>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 8px">통화 30초 전에 기억할 세 가지</h3>\n  <ul class="list">\n    <li><div class="t">숫자를 먼저 말하지 마십시오</div><div class="m">PD님이 생각하는 몫이 있을 겁니다. 먼저 들으면 협상 폭이 생깁니다</div></li>\n    <li><div class="t">오늘은 1단계만 닫습니다</div><div class="m">장기 구조는 "런칭 결과 보고 2월에 다시 앉자"로 미루는 게 양쪽 다 안전합니다</div></li>\n    <li><div class="t">채널 소유는 협상 대상이 아닙니다</div><div class="m">보상은 넉넉히, 소유는 법인. 이건 처음부터 깔고 들어가십시오</div></li>\n  </ul>\n</div>\n\n<h2>먼저 물어볼 것 넷</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">1. "어떤 형태를 생각하고 계셨어요?"</div><div class="m">PD님이 먼저 말하게. 외주 단가를 생각하는지 지분을 생각하는지에 따라 대화가 완전히 달라집니다</div></li>\n    <li><div class="t">2. 투입량 — 월 몇 편, 주 몇 시간</div><div class="m">TV조선 격주 금요일, 12월 둘째·셋째 주 금토일 스키장협회가 이미 있습니다. 수요일 13시 정기 회의 참석이 가능한지도</div></li>\n    <li><div class="t">3. 범위 — 기획까지인지 촬영·편집까지인지</div><div class="m">10/28에 루크님이 직접 "기획을 내부가 하면 RS를 낮춘다"고 하셨습니다. 기획을 넘기면 비싸집니다. 이 선을 먼저 그으십시오</div></li>\n    <li><div class="t">4. 계약 주체 — 개인인지 회사인지</div><div class="m">세금계산서·원천징수가 갈립니다. 편집 인력이 PD님 본인인지 팀인지도</div></li>\n  </ul>\n</div>\n\n<h2>제안할 구조 — 보상을 3층으로</h2>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>1</b><span>고정</span></div>\n    <div class="pgb">\n      <h3 style="margin:0 0 6px">편당 제작비 <span class="tag">월 280만 선</span></h3>\n      <p style="margin:0 0 6px">편당 <b>70만 × 월 4편</b> 기준. 10/28에 잡으신 50~80만 범위 안입니다.</p>\n      <div class="note">PD님 입장에서 1~2월까지 정산이 없으니 이게 버티는 돈입니다. 월 제작비 예산 700만 중 280만이 여기, 나머지는 광고용 별도 촬영·장비·공간.</div>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>2</b><span>구간</span></div>\n    <div class="pgb">\n      <h3 style="margin:0 0 6px">런칭 매출 구간별 정액 <span class="tag">비율 아님</span></h3>\n      <p style="margin:0">비율(%)이 아니라 <b>구간별 정액</b>으로 가야 합니다. 비율이면 민트 60%·루크 24%·메이븐 16% 위에 또 얹혀서 계산이 꼬이고, 매출이 커질수록 통제가 안 됩니다. 10/28에 이미 5,000만/1억/1.5억/2억 구간을 잡아 두셨으니 그대로 쓰면 됩니다.</p>\n    </div>\n  </div>\n</div>\n\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>3</b><span>장기</span></div>\n    <div class="pgb">\n      <h3 style="margin:0 0 6px">채널이 스스로 번 돈만 비율로 <span class="tag">2월 이후</span></h3>\n      <p style="margin:0">협찬·브랜디드·채널 경유 상품 매출. <b>오늘 숫자를 정하지 말고 방향만 합의</b>하십시오. 런칭 결과를 보고 2월에 앉는 게 양쪽 다 낫습니다.</p>\n    </div>\n  </div>\n</div>\n\n<h2>1단계 숫자 — 이대로 제시하시면 됩니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">PD 보상은 <b>배분 전 비용으로 차감</b>합니다. 그래야 민트·루크·메이븐이 지분대로 나눠 부담하고, 루크님만 떠안지 않습니다.</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">런칭 매출</th><th style="white-space:nowrap">PD 구간</th><th style="white-space:nowrap">PD 총수령</th><th style="white-space:nowrap">루크 24%</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">5,000만</td><td style="white-space:nowrap">400만</td><td style="white-space:nowrap">960만</td><td style="white-space:nowrap">250만</td></tr>\n      <tr><td style="white-space:nowrap">1억</td><td style="white-space:nowrap">800만</td><td style="white-space:nowrap">1,360만</td><td style="white-space:nowrap">1,354만</td></tr>\n      <tr><td style="white-space:nowrap">1.5억</td><td style="white-space:nowrap">1,200만</td><td style="white-space:nowrap">1,760만</td><td style="white-space:nowrap">2,458만</td></tr>\n      <tr><td style="white-space:nowrap">2억</td><td style="white-space:nowrap">1,700만</td><td style="white-space:nowrap">2,260만</td><td style="white-space:nowrap">3,538만</td></tr>\n      <tr><td style="white-space:nowrap">2.7억 <small>150명</small></td><td style="white-space:nowrap">2,200만</td><td style="white-space:nowrap"><b>2,760만</b></td><td style="white-space:nowrap"><b>5,098만</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">광고 3,000만 + PD 고정 560만(70만 × 8편)을 먼저 뺀 금액을 민트 60 : 루크 24 : 메이븐 16으로 나눈 값입니다.</div>\n</div>\n\n<figure class="fig">\n<svg viewBox="0 0 400 132" role="img" aria-label="매출 2.7억일 때 PD 없이 루크 5760만, PD 포함 5098만, PD 수령 2760만">\n  <text x="2" y="36" font-size="12" font-weight="700" fill="var(--ink)">루크 — PD 없이</text>\n  <rect x="120" y="20" width="200" height="22" rx="3" fill="var(--f1)"/>\n  <text x="398" y="36" font-size="11" fill="var(--muted)" text-anchor="end">5,760만</text>\n\n  <text x="2" y="72" font-size="12" font-weight="700" fill="var(--ink)">루크 — PD 포함</text>\n  <rect x="120" y="56" width="177" height="22" rx="3" fill="var(--f4)"/>\n  <text x="398" y="72" font-size="11" fill="var(--muted)" text-anchor="end">5,098만</text>\n\n  <text x="2" y="108" font-size="12" font-weight="700" fill="var(--ink)">PD 총수령</text>\n  <rect x="120" y="92" width="96" height="22" rx="3" fill="var(--f2)"/>\n  <text x="398" y="108" font-size="11" fill="var(--muted)" text-anchor="end">2,760만</text>\n</svg>\n<figcaption>매출 2.7억(150명) 기준입니다. 루크님이 <b>662만</b>을 더 내고 기획·촬영·편집·채널 운영을 받습니다. PD 수령 2,760만 중 나머지는 민트님과 메이븐님이 지분대로 부담합니다.</figcaption>\n</figure>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">이 표가 설득력 있는 이유</h3>\n  <p style="margin:0">김한준 PD 회사 안이 <b>8회 × 100만 = 800만 순수 외주</b>였습니다. 이 구조면 PD님은 매출 1억만 넘겨도 1,360만, 2.7억이면 <b>2,760만</b> — 외주의 3.5배입니다. 대신 안 팔리면 960만입니다. <b>같이 걸고 같이 먹는 구조</b>라는 걸 그대로 말씀하시면 됩니다.</p>\n</div>\n\n<h2>장기 구조 — 방향만 합의</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>수익원</th><th>제안</th><th style="white-space:nowrap">시점</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">강의·프로그램 매출</td><td>구간별 정액 (1단계와 동일 방식)</td><td style="white-space:nowrap">기수마다</td></tr>\n      <tr><td style="white-space:nowrap">협찬·브랜디드</td><td>PD가 영업·제작까지 하면 <b>40~50%</b></td><td style="white-space:nowrap">2월 이후</td></tr>\n      <tr><td style="white-space:nowrap">애드센스</td><td><b>PD 100%</b> — 협상 카드로 쓰십시오</td><td style="white-space:nowrap">2월 이후</td></tr>\n      <tr><td style="white-space:nowrap">채널 경유 신규 상품</td><td>5~8% (배분 전 차감)</td><td style="white-space:nowrap">2월 이후</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="emph">애드센스는 10/28에 "조회수 수익 배제"로 정리하셨는데, <b>장기에는 PD님께 100% 주는 게 낫습니다.</b> 금액은 작은데 PD가 조회수를 끌어올릴 직접적인 이유가 됩니다. 루크님은 어차피 강의 매출로 먹습니다 — 싸게 사는 동기부여입니다.</div>\n</div>\n\n<h2>계약에 반드시 넣을 셋</h2>\n<div class="card red">\n  <ul class="list">\n    <li><div class="t">1. 채널·계정·브랜드는 법인 명의</div><div class="m">"스스로 월백" 채널, 유튜브·광고 계정, 상표, 도메인 전부. PD님께는 운영 권한만. 종료 시 7일 내 이관, 포트폴리오 사용권은 드립니다. <b>처음 채널 만들 때 바로 적용</b>해야 나중에 안 싸웁니다</div></li>\n    <li><div class="t">2. 최소 산출량</div><div class="m">월 N편, 수요일 13시 정기 회의 참석, 러프컷 납기. 숫자가 없으면 RS만 가져가고 산출은 적을 수 있습니다. PD님 본업 일정이 12월에 겹칩니다</div></li>\n    <li><div class="t">3. 출구</div><div class="m">1단계는 런칭까지. 2단계는 1년 + 분기 점검. 평가 기준을 숫자로 미리 — 구독자, 영상당 조회, 카페 유입, 전환율</div></li>\n  </ul>\n</div>\n\n<h2>짚이는 것 넷</h2>\n<div class="card red">\n  <h3 style="margin:0 0 8px">① 런칭이 2월로 밀리면 현금이 한 달 빕니다</h3>\n  <p style="margin:0">10/30에 "에이전시 2달 리드타임, 12월 착수면 1월을 넘길 수 있다"가 나왔습니다. 2월 런칭이면 정산은 <b>3월</b>입니다. 그런데 민트님 계약은 1/20 종료고 용역비는 1/22까지 나갑니다. <b>한 달이 통째로 빕니다.</b> 오늘 통화에서 PD님께 "1월 20일을 지킬 수 있는 일정인지"를 꼭 확인하십시오.</p>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">② 전환율 4%가 실측값입니다</h3>\n  <p style="margin:0">10/28에 "최근 라이브 결제 전환율 약 4%"가 나왔습니다. 제가 쓰던 5% 가정보다 낮습니다. 유입 3,000명 × 4% = <b>120명 · 매출 2.16억</b>이 현실선입니다. 위 표에서 2억 줄을 기준으로 보시는 게 안전합니다.</p>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">③ 타깃이 40대 초반으로 바뀌었습니다</h3>\n  <p style="margin:0">10/30에 50~60대는 이탈률이 높아 배제하기로 하셨습니다. 그런데 기존 수강생과 카페 3,000명이 바로 그 층입니다. <b>새 채널로 모으는 사람과 기존 카페에 있는 사람이 다른 층</b>이 됩니다. 1/20 라이브에 둘을 같이 부르면 메시지가 갈라지고, 그게 4% 전환율을 더 끌어내릴 수 있습니다. 라이브를 한 번에 할지 나눌지 생각해 두십시오.</p>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">④ 민트님 동의가 먼저입니다</h3>\n  <p style="margin:0">PD 보상을 배분 전 비용으로 빼면 <b>민트님이 60% 지분만큼 부담</b>합니다. 2.7억 기준 민트님 몫이 1,656만 줄어듭니다. 오늘 PD님과 합의하기 전에 민트님께 한 줄이라도 깔아 두시는 게 낫습니다 — 나중에 알면 두 번 설명해야 합니다.</p>\n</div>\n\n<h2>확인 필요</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">PD님이 생각하는 보상 수준</div><div class="m">오늘 가장 먼저 들을 것</div></li>\n    <li><div class="t">"스스로 월백" 브랜드·채널의 소유 주체</div><div class="m">새 브랜드라 지금 정하지 않으면 나중에 복잡해집니다</div></li>\n    <li><div class="t">신규 채널인지 기존 1만 채널인지</div><div class="m">10/30에 공동작업자 기능으로 테스트 후 확정하기로 했는데, 어느 쪽이냐에 따라 소유 문제의 성격이 달라집니다</div></li>\n    <li><div class="t">월 제작비 700만의 세부 배분</div><div class="m">PD 편당비 · 광고용 별도 촬영 · 장비·공간</div></li>\n    <li><div class="t">1/20 라이브를 지킬 수 있는지</div><div class="m">에이전시 리드타임 2달과 충돌</div></li>\n    <li><div class="t">차기 기수 광고비 선적립 "약 2"의 단위</div><div class="m">2,000만으로 읽었는데 맞는지</div></li>\n  </ul>\n</div>\n\n<p class="src">근거 — RS 혼합 모델·편당 50~80만·매출 구간(5,000만/1억/1.5억/2억)·월 예산 1,000만 중 제작비 700만·지급일 매월 22일·라이브 전환율 4%·인베이더 12월 종료: 플라우드 「10-28 회의: 유튜브 PD 협업 전환, RS·예산·계약 구조」. 브랜드 "스스로 월백"·타깃 40대 초반·5개 에피소드·상금 300만·채널 위임 범위와 수익 배분 미협의·에이전시 2달 리드타임·수요일 13시 정기 회의: 플라우드 「스스로월100 미팅 : 민트님 : 조윤호 피디님」(10/30, 112분). 배분 민트 60 : 루크 24 : 메이븐 16과 광고 3,000만: <a href="../cash/">11~2월 현금 흐름</a>. PD 구간 금액과 각 구간 배분액은 위 전제로 제가 계산한 제안값이며 합의된 숫자가 아닙니다.</p>\n'


# ---------------------------------------------------------------- 채널 운영 비용 산정
PDLONG = '<div class="hero">\n  <h1>채널 운영 — 비용을 어떻게 잡나</h1>\n  <div class="sub">"유튜브 수익 6:4 + 강의 RS" 구상에 대한 검토 · 11/2 16시 통화 전</div>\n  <div class="goal">\n    <div><b>월 40~160만</b><span>회사가 4를 가져가 봐야 받는 돈</span></div>\n    <div><b>2가지</b><span>\'유튜브 수익\'에 섞여 있는 성격</span></div>\n    <div><b>1.16억</b><span>그 구조로 가면 PD 연 수령</span></div>\n    <div><b>1.54억</b><span>같은 해 루크님 몫</span></div>\n  </div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">먼저 — 6:4를 그대로 가시면 안 됩니다</h3>\n  <p style="margin:0 0 8px">"유튜브 운영 수익"에 <b>성격이 전혀 다른 두 가지</b>가 섞여 있습니다.</p>\n  <div class="kv">\n    <dt>애드센스</dt><dd>조회수로 나오는 돈. <b>작습니다.</b> 월 50만 뷰여도 100~200만</dd>\n    <dt>협찬·브랜디드</dt><dd>루크님 얼굴과 브랜드로 들어오는 돈. <b>건당 수백~수천만</b></dd>\n  </div>\n  <div class="emph">앞엣것은 6이 아니라 <b>PD 100%를 줘도 됩니다.</b> 뒤엣것은 <b>6이 과합니다.</b> 하나로 묶으면 둘 다 틀립니다.</div>\n</div>\n\n<h2>애드센스 — 4를 가져가는 게 손해입니다</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="white-space:nowrap">월 조회수</th><th style="white-space:nowrap">월 수익</th><th style="white-space:nowrap">회사 4</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">20만 뷰</td><td style="white-space:nowrap">40~80만</td><td style="white-space:nowrap">16~32만</td></tr>\n      <tr><td style="white-space:nowrap">50만 뷰</td><td style="white-space:nowrap">100~200만</td><td style="white-space:nowrap">40~80만</td></tr>\n      <tr><td style="white-space:nowrap">100만 뷰</td><td style="white-space:nowrap">200~400만</td><td style="white-space:nowrap">80~160만</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <p style="margin:10px 0 0">잘 돼도 회사 몫이 <b>월 몇십만원</b>입니다. 그 돈 받자고 PD가 조회수를 올릴 이유를 깎습니다.</p>\n  <div class="emph">애드센스는 <b>PD 100%</b>로 주십시오. 협상에서 내주는 게 아니라 <b>싸게 사는 동기부여</b>입니다. "조회수는 전부 PD님 겁니다"라고 말하면 그 한마디가 고정비 몇백만원어치 일을 합니다.</div>\n</div>\n\n<h2>수익원을 넷으로 쪼개십시오</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>수익원</th><th>누가 만드나</th><th style="white-space:nowrap">제안</th></tr></thead>\n    <tbody>\n      <tr><td style="white-space:nowrap">애드센스</td><td>PD (조회수)</td><td style="white-space:nowrap"><b>PD 100%</b></td></tr>\n      <tr><td style="white-space:nowrap">협찬·브랜디드</td><td>PD 영업 + 루크 얼굴</td><td style="white-space:nowrap"><b>PD 50 : 회사 50</b></td></tr>\n      <tr><td style="white-space:nowrap">강의·프로그램</td><td>루크 상품 + PD 유입</td><td style="white-space:nowrap"><b>구간별 정액</b></td></tr>\n      <tr><td style="white-space:nowrap">채널 운영 자체</td><td>PD 노동</td><td style="white-space:nowrap"><b>월 고정비</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">강의 매출에 비율을 걸면 민트 60 · 루크 24 · 메이븐 16 위에 또 얹혀서 매출이 커질수록 통제가 안 됩니다. 구간별 정액이어야 합니다.</div>\n</div>\n\n<h2>"비용을 어떻게 산정하나" — 앵커 두 개</h2>\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>1</b><span>대체비용</span></div>\n    <div class="pgb">\n      <h3 style="margin:0 0 6px">같은 일을 외주로 사면 얼마인가</h3>\n      <p style="margin:0">김한준 안이 편당 100만이었습니다. 월 4편이면 400만. 거기에 기획·업로드·댓글·분석까지 붙으면 <b>월 500~600만</b>이 시장가입니다.</p>\n    </div>\n  </div>\n</div>\n<div class="card">\n  <div class="pg">\n    <div class="pgn"><b>2</b><span>기회비용</span></div>\n    <div class="pgb">\n      <h3 style="margin:0 0 6px">PD님이 그 시간에 다른 일을 하면 얼마를 버나</h3>\n      <p style="margin:0">TV조선 격주 금요일, 스키장협회 2박 3일 건들이 이미 있습니다. 그 단가가 바닥선입니다.</p>\n    </div>\n  </div>\n</div>\n<div class="card accent">\n  <p style="margin:0"><b>두 앵커 사이에서 월 300~400만을 고정으로 잡고, 나머지는 성과로 넘기십시오.</b> 시장가(500~600만)보다 낮게 고정을 잡는 대신 RS로 메우는 구조 — 이게 "같이 걸고 같이 먹는다"의 실제 모양입니다.</p>\n</div>\n\n<h2>그런데 숫자를 돌려보면 문제가 보입니다</h2>\n<div class="card red">\n  <p style="margin:0 0 10px">기수 4회 · 매출 2.16억/기수(전환 4%) · 고정 월 300만 · 구간 1,700만 가정으로 1년을 돌려봤습니다.</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th>항목</th><th style="white-space:nowrap">연 금액</th></tr></thead>\n    <tbody>\n      <tr><td>PD 고정 (월 300만 × 12)</td><td style="white-space:nowrap">3,600만</td></tr>\n      <tr><td>PD 구간 RS (1,700만 × 4기)</td><td style="white-space:nowrap">6,800만</td></tr>\n      <tr><td>PD 애드센스 (월 100만 × 12)</td><td style="white-space:nowrap">1,200만</td></tr>\n      <tr><td><b>PD 합계</b></td><td style="white-space:nowrap"><b>1억 1,600만</b></td></tr>\n      <tr><td><b>같은 해 루크님 몫 (24%)</b></td><td style="white-space:nowrap"><b>1억 5,360만</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="emph">연 매출 8.6억을 만들어서 <b>PD가 1.16억, 루크님이 1.54억</b>입니다. 거의 비슷합니다. PD 단가가 비싸서가 아닙니다 — <b>루크님이 24%밖에 안 가져가기 때문</b>입니다.</div>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">그래서 오늘 장기 %를 확정하지 마십시오</h3>\n  <p style="margin:0 0 8px">민트님 계약은 <b>1기 런칭까지 3개월 + 자동연장</b>입니다. 2기부터는 민트님 60%도 재협상 대상입니다. 그런데 오늘 PD님과 장기 비율을 못박으면, <b>민트님과 다시 앉을 때 루크님이 움직일 폭이 없어집니다.</b></p>\n  <div class="emph">PD 몫이 들어갈 자리는 민트님 60%에서 나와야지, 루크님 24%에서 나오면 안 됩니다. 그 조정을 하려면 두 협상을 같이 봐야 합니다.</div>\n</div>\n\n<h2>오늘 하실 말 — 이 정도면 충분합니다</h2>\n<div class="card accent">\n  <ul class="list">\n    <li><div class="t">1. "장기로 채널을 같이 운영한다는 전제는 저도 같습니다"</div><div class="m">방향은 확실히 주십시오. 이게 PD님이 듣고 싶은 말입니다</div></li>\n    <li><div class="t">2. "구조는 월 고정 + 성과 RS로 가려 합니다"</div><div class="m">고정은 월 300~400만 선, 성과는 기수 매출 구간별 정액</div></li>\n    <li><div class="t">3. "유튜브 조회수 수익은 전부 PD님 가져가십시오"</div><div class="m">여기서 한 번 크게 주십시오. 비용은 작고 효과는 큽니다</div></li>\n    <li><div class="t">4. "협찬이 들어오면 반반으로 봅니다"</div><div class="m">숫자까지 확정하지 말고 방향만</div></li>\n    <li><div class="t">5. "정확한 비율은 1기 런칭 결과 보고 2월에 확정하시죠"</div><div class="m">민트님 재협상과 묶여 있다는 말까지는 안 하셔도 됩니다</div></li>\n  </ul>\n</div>\n\n<h2>그리고 반드시 — 세 줄</h2>\n<div class="card red">\n  <ul class="list">\n    <li><div class="t">채널·계정·상표는 법인 명의</div><div class="m">"스스로 월백" 전부. PD님은 운영 권한, 종료 시 7일 내 이관, 포트폴리오 사용권은 부여. <b>채널 만들 때 바로</b></div></li>\n    <li><div class="t">최소 산출량을 숫자로</div><div class="m">월 N편, 수요일 13시 회의 참석, 분석 리포트 월 1회. 없으면 "운영해준다"는 말만 남습니다</div></li>\n    <li><div class="t">기간은 1년, 분기 점검</div><div class="m">PD님이 바빠져서 월 1편만 올려도 비율은 계속 나갑니다. 끊을 수 있어야 합니다</div></li>\n  </ul>\n</div>\n\n<h2>확인 필요</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">PD님이 생각하는 보상 수준</div><div class="m">오늘 가장 먼저 들으실 것 — 숫자를 먼저 꺼내지 마십시오</div></li>\n    <li><div class="t">애드센스 실제 규모</div><div class="m">위 표는 RPM 2,000~4,000원 가정입니다. 기존 1만 채널 실적이 있으면 그걸로 바꾸면 됩니다</div></li>\n    <li><div class="t">협찬이 실제로 들어올 채널인지</div><div class="m">타깃 40대 초반 · 부업 카테고리면 협찬 단가가 높지 않을 수 있습니다</div></li>\n    <li><div class="t">2기부터 민트님 조건을 바꿀 수 있는지</div><div class="m">PD 장기 비율의 재원이 여기서 나와야 합니다</div></li>\n  </ul>\n</div>\n\n<p class="src">근거 — 수익 배분 민트 60 : 루크 24 : 메이븐 16, 광고 분기 3,000만: <a href="../cash/">11~2월 현금 흐름</a>. 편당 50~80만·매출 구간·월 제작비 700만·전환율 4% 실측: 플라우드 「10-28 회의: 유튜브 PD 협업 전환, RS·예산·계약 구조」. 브랜드 "스스로 월백"·채널 위임 범위와 수익 배분 미협의: 플라우드 「스스로월100 미팅」(10/30). 민트 계약 기간 3개월 + 자동연장: <a href="../park-contract/">민트 1차 계약서</a> 제2조. 애드센스 월 수익은 RPM 2,000~4,000원 가정으로 제가 계산한 <b>추정치</b>이고 실제 채널 실적이 아닙니다 — 기존 채널 수치가 있으면 바꿔야 합니다. PD 연 수령 1.16억과 루크 1.54억도 위 가정에 따른 계산값입니다. 기본 제안 구조는 <a href="../pd/">조윤호 PD 파트너십 설계</a>.</p>\n'


# ---------------------------------------------------------------- 가을 계약서 검토
GAEULC = '<div class="hero">\n  <h1>가을 대표님 계약서 — 괜찮은가</h1>\n  <div class="sub">셀피티클래스 × 정복녀 강사용역계약서 · 10/31 녹취 전문 대조 · 갱신 11/04</div>\n  <div class="goal">\n    <div><b>5,022만</b><span>10/31에 없던 두 줄이 가져가는 돈</span></div>\n    <div><b>603만</b><span>그중 루크님이 잃는 금액</span></div>\n    <div><b>30명</b><span>가을님 손익분기 (광고·운영 5,000만)</span></div>\n    <div><b>24명</b><span>20% 줄이 없었다면</span></div>\n  </div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">10/31 녹음에 없는 두 줄이 계약서에 들어와 있습니다</h3>\n  <p style="margin:0 0 10px">녹취 전문(76분, 364세그먼트) 전체를 검색했습니다. <b>"11.76"도, "RS"도, "20%"도, "인터뷰 채널"도 한 번도 나오지 않습니다.</b> 그날 결제 수수료에 관해 나온 말은 <b>"PG 사 수수료만 제외하고"</b> 한마디뿐이고, 요율은 정해진 적이 없습니다.</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:38%">항목</th><th>10/31 녹음</th><th>계약서</th></tr></thead>\n    <tbody>\n      <tr><td>루크님 8%</td><td>합의 (1:00:22까지)</td><td>광고비로 계상 ✓</td></tr>\n      <tr><td>순수익 5:5</td><td>합의 (1:00:27)</td><td>제10조 1항 ✓</td></tr>\n      <tr><td>결제 수수료 <b>11.76% 고정</b></td><td><b>없음</b> — "PG 수수료만 제외"</td><td>제10조 3항 2호</td></tr>\n      <tr><td>인터뷰 채널 출연 <b>RS 20%</b></td><td><b>없음</b></td><td>제10조 3항 3호</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="warn">그날의 합의는 <b>세 턴이 연속으로 붙어 있습니다.</b> 59:56 "PG 사 수수료만 제외하고 8%" → 1:00:22 <b>"수수료는 광고비 내역으로 넣겠습니다"</b> → 1:00:27 <b>"순수익에서 5 대 5 로 나눠보려고 합니다"</b>. 그 자리에서 정산 구조는 끝났고, 20%와 11.76%는 그 뒤 문서 작성 단계에서 붙은 줄입니다.</div>\n  <div class="note">물론 10/31 이후 통화나 카톡으로 합의했을 수 있습니다 — <b>그 기억이 없으시면 합의된 적이 없는 겁니다.</b> 그리고 계약서는 가을님께 가기 전에 루크님이 먼저 컨펌하기로 되어 있습니다([06:14] "전복녀님 계약서는 일단 대표님한테 먼저 컨펌을 받으면 될까요?"). <b>지금이 그 줄을 걸러낼 수 있는 유일한 시점입니다.</b></div>\n</div>\n\n<div class="card gold">\n  <h3 style="margin:0 0 8px">이미 닫은 것들 (11/04 결정)</h3>\n  <ul class="list">\n    <li><div class="t">독점·경쟁모집 제한·비유인·중도이탈 배상 — 수용</div><div class="m">루크님이 에이전시처럼 대신 운영하는 구조라 실질 위험 없음</div></li>\n    <li><div class="t">10배 배상 조항 — 수용</div><div class="m">허위·과장과 명예훼손에만 걸리므로 정상 운영 시 발동 안 함</div></li>\n    <li><div class="t">광고 문구 보증 범위 제외 — 요청 안 함</div><div class="m">업계 표준. 퍼블리시 전 최종 문구만 루크님이 확인</div></li>\n    <li><div class="t">루크님 8%를 계약서에 명시 — 불필요</div><div class="m">가을님께 1층 조건을 노출하지 않기 위해 의도적으로 뺀 것. 광고비 내역으로 계상하기로 10/31에 합의 완료</div></li>\n  </ul>\n</div>\n\n<h2>① 돈이 어떻게 흐르는가</h2>\n<div class="card">\n  <div class="kv">\n    <dt>매출 (D)</dt><dd>부가세 제외, 환불 차감 후</dd>\n    <dt>− 결제 수수료 (E)</dt><dd>D의 <b>11.76% 고정</b> · 차액 정산 없음 · <b>10/31 합의에 없음</b></dd>\n    <dt>− 출연 RS (F)</dt><dd>(D−E)의 <b>20%</b> → 인터뷰 채널 · <b>10/31 합의에 없음</b></dd>\n    <dt>− 광고비 (G)</dt><dd>실제 광고 + <b>루크님 8%</b>가 여기 계상됨 · 상한 없음</dd>\n    <dt>− 운영비 (H)</dt><dd>CRM·외주 전액 · 상한 없음</dd>\n    <dt>= 순수익 (I)</dt><dd>가을 50% / 업체 50%</dd>\n    <dt>루크님 총 수령</dt><dd>8%(=(D−E)의 8%) + 가을님 K의 40%</dd>\n  </div>\n  <div class="note">8%가 광고비로 들어가므로 <b>순수익이 그만큼 줄고 가을님과 업체가 절반씩 부담합니다.</b> 루크님은 8%를 받는 대신 자기 40%분이 줄어드는 구조 — 65명 기준 1,206만을 받고 241만을 잃어 순증 965만입니다. 이건 의도된 설계이니 그대로 둡니다.</div>\n</div>\n\n<h2>② 65명이면 1억 7,077만원이 이렇게 갈립니다</h2>\n<div class="card">\n  <div class="note" style="margin:0 0 10px">단가 289만(결제액, 부가세 포함 가정 → 공급가액 262.7만) · 실제 광고 4,000만 + 운영 1,000만 (루크님 8%는 별도로 광고비에 계상)</div>\n  <div class="fig">\n  <svg viewBox="0 0 400 132" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="65명 기준 매출 배분">\n    <text x="2" y="15" font-size="10" fill="currentColor">광고·운영비</text>\n    <rect x="92" y="6" width="240" height="11" fill="var(--f1)"/>\n    <text x="398" y="15" font-size="10" text-anchor="end" fill="currentColor">5,000만</text>\n\n    <text x="2" y="37" font-size="10" fill="currentColor">인터뷰 채널</text>\n    <rect x="92" y="28" width="145" height="11" fill="var(--f3)"/>\n    <text x="398" y="37" font-size="10" text-anchor="end" fill="currentColor">3,014만</text>\n\n    <text x="2" y="59" font-size="10" fill="currentColor">셀피티클래스</text>\n    <rect x="92" y="50" width="140" height="11" fill="var(--f3)"/>\n    <text x="398" y="59" font-size="10" text-anchor="end" fill="currentColor">2,925만</text>\n\n    <text x="2" y="81" font-size="10" fill="currentColor">루크님 (8%+40%)</text>\n    <rect x="92" y="72" width="114" height="11" fill="var(--f2)"/>\n    <text x="398" y="81" font-size="10" text-anchor="end" fill="currentColor">2,375만</text>\n\n    <text x="2" y="103" font-size="10" fill="currentColor">PG·카드</text>\n    <rect x="92" y="94" width="96" height="11" fill="var(--f1)"/>\n    <text x="398" y="103" font-size="10" text-anchor="end" fill="currentColor">2,008만</text>\n\n    <text x="2" y="125" font-size="10" fill="currentColor">가을 대표님</text>\n    <rect x="92" y="116" width="84" height="11" fill="var(--f4)"/>\n    <text x="398" y="125" font-size="10" text-anchor="end" fill="currentColor">1,755만</text>\n  </svg>\n  </div>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:22%">인원</th><th>가을</th><th>루크</th><th>업체</th></tr></thead>\n    <tbody>\n      <tr><td>20명</td><td><b>0원</b></td><td>371만</td><td>0원 (손실 1,662만)</td></tr>\n      <tr><td>30명</td><td>2만</td><td>558만</td><td>4만</td></tr>\n      <tr><td>40명</td><td>503만</td><td>1,077만</td><td>838만</td></tr>\n      <tr><td>65명</td><td>1,755만</td><td>2,375만</td><td>2,925만</td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<h2>③ 20% 줄 하나가 모두에게서 얼마를 가져가나</h2>\n<div class="card red">\n  <p style="margin:0 0 10px">65명 기준, 출연 RS 20%가 <b>있을 때와 없을 때</b>의 차이입니다. 다른 조건은 전부 같습니다.</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:28%"></th><th>20% 있음</th><th>없으면</th><th>차이</th></tr></thead>\n    <tbody>\n      <tr><td>가을</td><td>1,755만</td><td>2,659만</td><td><b>−904만</b></td></tr>\n      <tr><td><b>루크님</b></td><td>2,375만</td><td>2,978만</td><td><b>−603만</b></td></tr>\n      <tr><td>업체</td><td>2,925만</td><td>4,432만</td><td><b>−1,507만</b></td></tr>\n      <tr><td>인터뷰 채널</td><td>3,014만</td><td>0원</td><td>+3,014만</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="warn"><b>루크님도 603만을 잃습니다.</b> 가을님을 위한 얘기가 아니라 루크님 돈 얘기입니다. 그리고 <b>업체가 1,507만으로 가장 크게 잃는데도 계약서에 이 줄을 넣었다는 게 핵심</b>입니다 — 업체가 손해를 보면서 제3자에게 3,014만을 주는 계약은 없습니다. 둘 중 하나입니다.</div>\n  <ul class="list">\n    <li><div class="t">(가) 인터뷰 채널 = 업체 자신 또는 업체 관계사</div><div class="m">그러면 업체 실질 = 3,014 + 2,925 = <b>5,939만</b>이고 가을님은 1,755만입니다. "순수익 5:5"는 말만 5:5입니다. 1:00:27의 "순수익에서 5 대 5"와 다른 계약입니다.</div></li>\n    <li><div class="t">(나) 진짜 제3의 출연 채널</div><div class="m">그러면 업체가 1,507만을 내주고 데려온 채널이라는 뜻이니, <b>그만큼 모객을 책임진다는 합의가 어딘가 있어야 합니다.</b> 계약서에는 채널명도 최소 편수도 송출량도 없습니다.</div></li>\n  </ul>\n  <div class="note"><b>→ 물어볼 말 한 줄:</b> "출연 RS 20%는 10/31에 없던 내용인데 어느 채널이고 최소 출연·송출은 어떻게 됩니까? 성과 연동이 없으면 이 줄은 빼거나 상한을 거는 게 맞을 것 같습니다."</div>\n</div>\n\n<h2>④ 11.76%도 같은 자리에 있습니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">10/31에 나온 말은 <b>"PG 사 수수료만 제외하고"</b>가 전부입니다. 요율은 없었습니다. 계약서는 거기에 <b>11.76% 고정</b>을 넣고 <b>"실제 수수료의 다과와 관계없이 적용"</b>하며 차액 정산을 하지 않는다고 못 박았습니다(제10조 3항 2호).</p>\n  <p style="margin:0 0 10px"><b>이건 루크님 8%의 분모를 직접 깎습니다.</b> 8%의 기준이 "PG 수수료를 뺀 매출"이니까요. 매출 1.7억에서 <b>1%p가 170만원</b>이고, 루크님은 그 8%(약 14만) + 순수익 감소분의 40%(약 34만) = <b>1%p당 약 48만원</b>을 잃습니다.</p>\n  <div class="warn"><b>→ 요율표를 받으십시오.</b> 카드 가맹점 수수료 + PG 대행료 + 무이자 할부를 몇 개월까지 가맹점이 부담하는지. 무이자를 길게 돌리면 11.76%가 설명될 수 있습니다. 설명이 되면 그대로 두고, 안 되면 <b>실제 정산 + 상한</b>으로.</div>\n  <div class="note">국내 카드 가맹점 수수료율과 PG 대행료의 구체 수치는 가맹점별 계약 사항이라 공개 자료로 확인되지 않았습니다 — <b>확인 필요.</b> 여기서는 금액 영향만 계산했습니다.</div>\n</div>\n\n<h2>⑤ 광고·운영비 상한 — 이건 루크님이 운영자 자격으로 요구할 수 있습니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">제4조 9항: <b>"광고 예산의 사전 공개나 강사의 별도 승인을 집행 요건으로 하지 않는다."</b> 그 전액이 순수익에서 빠지고 절반을 가을님이, 그 40%를 루크님이 부담합니다. 상한도 사전 통지 의무도 없습니다.</p>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:34%">광고 + 운영비</th><th>가을님 손익분기</th><th>20% 줄이 없으면</th></tr></thead>\n    <tbody>\n      <tr><td>3,000만</td><td>18명</td><td>14명</td></tr>\n      <tr><td>4,000만</td><td>24명</td><td>19명</td></tr>\n      <tr><td>5,000만</td><td><b>30명</b></td><td><b>24명</b></td></tr>\n      <tr><td>6,000만</td><td>36명</td><td>28명</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">1인당 순수익 기여 = 262.7만 × 0.8824 × (1−0.20) − 루크님 8%(18.6만) = <b>166.9만</b>. 비용 167만마다 손익분기가 1명 올라갑니다.<br><b>요구하는 프레임이 중요합니다.</b> "가을님을 보호하기 위해"가 아니라 <b>"제가 실질 운영자이니 기수 예산은 같이 정합시다"</b>로 가십시오. 10/31에 루크님이 직접 말씀하신 인베이더 기존 조건이 <b>"광고비 나가는 거는 반반"</b>(14:51)이었으니, 그 선을 기준으로 삼으면 됩니다.</div>\n</div>\n\n<h2>⑥ 잘 쓰인 부분 — 공정하게</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">지급유보에 제동장치가 있다 — 제10조의2</div><div class="m">유보일부터 60일 내 손해액을 확정 못 하면 소를 제기하거나 유보 해제, 부당한 유보였으면 <b>연 6% 이자</b>. 10영업일 소명권도 있습니다.</div></li>\n    <li><div class="t">하도급법 우선 적용을 스스로 썼다 — 제10조 8항, 제10조의2 4항</div><div class="m">지급기일 60일 초과 금지와 공정위 고시 지연이자를 받아들였습니다.</div></li>\n    <li><div class="t">경쟁강의 범위를 좁혔다 — 제9조 2항·3항</div><div class="m">"실질적으로 대체하는 강의"로 한정하고, 같은 이커머스 분야라는 사정만으로는 아니라고 명시. 기존 VOD·전자책·저서도 제외.</div></li>\n    <li><div class="t">근로자성 리스크를 낮췄다 — 제3조, 제4조 1항·3항</div><div class="m">출퇴근·근태를 관리하지 않는다고 못 박았습니다.</div></li>\n    <li><div class="t">정산 투명성 — 별지 2</div><div class="m">A~M 항목이 전부 열려 있고 증빙 확인 요청권(제10조 4항)이 있습니다. <b>다만 별지 2를 가을님이 받으면 광고비(G) 안에 루크님 8%가 섞여 있는 게 보일 수 있습니다</b> — 비용 명세를 항목별로 첨부하게 되어 있어서(별지 2 하단), 그 첨부를 어떻게 쓸지 업체와 미리 맞춰두십시오.</div></li>\n  </ul>\n</div>\n\n<h2>⑦ 남은 세 가지</h2>\n<div class="card accent">\n  <ul class="list">\n    <li><div class="t">1. 출연 RS 20% — 어느 채널이고 최소 의무가 무엇인가</div><div class="m">10/31에 없던 줄. 65명 기준 3,014만. 루크님 몫에서 603만.</div></li>\n    <li><div class="t">2. 11.76% 요율표</div><div class="m">10/31에 없던 숫자. 1%p당 루크님 약 48만.</div></li>\n    <li><div class="t">3. 기수 광고·운영비 상한</div><div class="m">운영자 자격으로. 인베이더 기준이 "광고비 반반"이었음.</div></li>\n  </ul>\n  <div class="note">가을님 쪽 조항(독점·10배·비유인·광고 문구)은 전부 수용으로 닫았습니다. 위 세 가지는 가을님 보호가 아니라 <b>루크님 수익과 운영 권한</b>에 걸린 항목입니다.</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">확인 필요</h3>\n  <ul class="list">\n    <li><div class="t">인터뷰 채널의 정체</div><div class="m">업체 자체·관계사인지 제3자인지. 10/31 녹취에는 등장하지 않음</div></li>\n    <li><div class="t">10/31 이후 20%·11.76%를 따로 합의했는지</div><div class="m">통화·카톡 기록 확인</div></li>\n    <li><div class="t">셀피티클래스(대표 황태현)와 초월스토리의 관계</div><div class="m">10/31 녹취에 두 이름 모두 등장하지 않음. 녹취 속 상대측 화자가 누구인지 전사만으로는 특정 불가</div></li>\n    <li><div class="t">11.76%의 산출 근거</div><div class="m">결제 수단별 실제 요율표와 무이자 할부 부담 개월 수</div></li>\n    <li><div class="t">289만이 부가세 포함인지</div><div class="m">포함 가정(공급가액 262.7만). 면세·별도면 손익분기가 2~3명 내려갑니다</div></li>\n    <li><div class="t">이 건의 실제 광고·운영비 예산</div><div class="m">계산에 쓴 4,000만 + 1,000만은 가정. 10/31에 금액 합의 없었음</div></li>\n    <li><div class="t">4%(단순 소개)와 8%의 경계</div><div class="m">10/31에 루크님이 4%를 제시했고 "확인해보겠다"로 끝남 — 미확정</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  근거 · 첨부 계약서(강사용역계약서, 셀피티클래스–정복녀, 전 18조 + 별지 1~3) 전문 ·\n  2026-10-31 회의 녹취 전문(76분, transaction·transaction_polish 364세그먼트 전수 검색) ·\n  인용 타임스탬프 06:14 / 14:51 / 56:31 / 59:56 / 1:00:22 / 1:00:27 ·\n  3층 구조(1층 루크–업체 8% / 2층 업체–가을 순수익 5:5 / 3층 가을–루크 6:4)는 루크님 설명 ·\n  국내 카드 가맹점 수수료율·PG 대행료의 구체 수치는 공개 자료로 확인되지 않아 금액 영향만 계산 (확인 필요) ·\n  금액은 단가 289만(부가세 포함 가정)·실제 광고 4,000만·운영 1,000만 가정 하의 계산값 ·\n  녹취 고유명사는 전사 품질이 낮아 인명 표기가 일부 뭉개져 있음 (숫자·비율은 원본과 폴리시본 일치)\n</div>\n'

# ---------------------------------------------------------------- PD 촬영비 민트 공유
PDCOST = '<div class="hero">\n  <h1>PD 촬영비 — 민트님께 드릴 내용</h1>\n  <div class="sub">11/2(월) 조윤호 PD 통화 31:40~41:38 · 이번 런칭 프로젝트 비용만 추림</div>\n  <div class="goal">\n    <div><b>30~35만</b><span>촬영 인건비 1인당</span></div>\n    <div><b>120만</b><span>홍보 영상 1편 (4명)</span></div>\n    <div><b>60~70만</b><span>본편 1편 (2명)</span></div>\n    <div><b>0원</b><span>편집 — PD가 직접</span></div>\n  </div>\n</div>\n\n<div class="card accent">\n  <h3 style="margin:0 0 8px">한 줄 요약</h3>\n  <p style="margin:0 0 10px"><b>PD님은 "촬영 팀원 인건비만 실비로 받고, 본인 몫은 RS로 가져가겠다"는 입장입니다.</b> 편당 단가를 부르는 외주가 아니라, <b>고정비는 최소로 하고 성과에 걸겠다</b>는 구조입니다.</p>\n  <p style="margin:0">본인 수익 목표는 아예 안 정해 두셨습니다 — [33:07] <i>"크게 생각을 해본 적은 없는 것 같긴 한데요 여기서는 이제 대표님이 어련히 해주셨지 했었던 것 같긴 합니다."</i> <b>숫자를 먼저 부르는 쪽이 기준을 잡습니다.</b></p>\n</div>\n\n<h2>① 단가 — PD님이 직접 말한 숫자</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:34%">항목</th><th>인원</th><th>금액</th></tr></thead>\n    <tbody>\n      <tr><td>촬영 인건비 기준</td><td>1인당</td><td><b>30~35만</b></td></tr>\n      <tr><td>홍보(모객) 영상</td><td>3~4명</td><td><b>약 120만</b> (4명 기준)</td></tr>\n      <tr><td>본편 에피소드</td><td>최소 2명</td><td><b>60~70만</b></td></tr>\n      <tr><td>편집</td><td>PD 직접</td><td><b>별도 청구 없음</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">[36:19] <i>"그냥 최저로 잡으면 한 인당 30 에서 35 정도 인건비를 받거든요"</i> — <b>"최저로 잡으면"</b>이라는 단서가 붙어 있고, <b>"장비나 이런 거에 따라 조금 달라진다"</b>고 하셨습니다. 장비가 늘면 올라갑니다.<br>[36:48] <i>"한 4 명 한다고 하면 120 만 원 정도 거기 편집 같은 경우에는 별도로 해서 들어가긴 하는데 그건 제가 맡아서 할 부분이라서 그 부분은 제가 좀 더 편하게 해드릴 수 있고"</i><br>[38:42] <i>"지금 머릿속에는 2 명 해서 인건비 60,70 정도?"</i> — 본인이 <b>"머릿속"</b>이라고 하셨고 [38:19] <b>"기획이 아직 나온 상태가 아니라 정확하게 말씀드리기는 어렵지만"</b>이 붙습니다.</div>\n</div>\n\n<h2>② 편수를 넣으면 총액</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:28%">본편 편수</th><th>2명 투입</th><th>3명 투입</th></tr></thead>\n    <tbody>\n      <tr><td>3편 + 홍보 1편</td><td>300~330만</td><td>390~435만</td></tr>\n      <tr><td><b>5편 + 홍보 1편</b></td><td><b>420~470만</b></td><td>570~645만</td></tr>\n      <tr><td>8편 + 홍보 1편</td><td>600~680만</td><td>840~960만</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">10/30 미팅 기준 에피소드는 <b>5개</b>였으니 <b>420~470만</b> 선이 기본 시나리오입니다. 본편 투입 인원은 [37:39] <i>"한 세 명이 붙냐 두 명이 붙냐"</i>로 아직 2명/3명 사이입니다 — <b>기획이 나와야 확정됩니다.</b></div>\n  <div class="warn"><b>비교 기준:</b> 10/23에 민트님이 제안하신 안은 <b>편당 100만 × 7~8편 = 800만</b>(김한준 PD 회사)이었습니다. 같은 분량이면 <b>600~680만 vs 800만</b>이고, 5편 기준이면 <b>420~470만</b>입니다. 다만 김한준 측 단가에 편집이 포함인지는 확인되지 않았습니다 — <b>확인 필요.</b> 조윤호 PD 쪽은 편집이 확실히 포함입니다.</div>\n</div>\n\n<h2>③ RS는 턴키·매출 퍼센트입니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">루크님이 [39:10] <i>"명당 RS를 드려야 되는 건지 아니면 전체 매출에서 이 정도 퍼센테이지를 가져가고 싶다 이렇게 가야 되는 건지"</i>라고 물었고, PD님 답이 명확합니다.</p>\n  <div class="warn">[39:41] <i>"<b>턴키로 해서 통으로 해가지고 매출의 어느 정도 퍼센테이지 해서 그렇게 해주시면 될 것 같은데요?</b>"</i><br>[39:50] <i>"이게 인당 인당으로 가실 이유는 없을 것 같고 … 어차피 제가 한 팀으로 묶어서 오는 거다 보니까"</i></div>\n  <p style="margin:10px 0 0"><b>퍼센트 숫자는 안 나왔습니다.</b> 그리고 우선순위를 이렇게 말씀하셨습니다 — [41:38] <i>"우선 기본적인 그 촬영에 대한 인건비는 제 사람들부터 챙기고 그 다음에 말씀드렸던 것처럼 RS나 그런 부분에서 제가 뭐 가져갈 수 있으면 그렇게 하면 되는 거니까 <b>그런 금액적인 부분은 저는 커다랗게 지금은 없는 것 같고</b>"</i></p>\n</div>\n\n<h2>④ 아직 안 정해진 것 — 오늘 미팅에서 채울 칸</h2>\n<div class="card red">\n  <ul class="list">\n    <li><div class="t">RS 퍼센트</div><div class="m">"어느 정도 퍼센테이지"까지만. 숫자 없음</div></li>\n    <li><div class="t">본편 편수와 투입 인원</div><div class="m">기획이 나와야 2명/3명이 정해지고, 그래야 총액이 나옴</div></li>\n    <li><div class="t">지급 시기·분할·선금 잔금</div><div class="m">언급 없음</div></li>\n    <li><div class="t">비용 포함 범위</div><div class="m">촬영 인건비와 편집만 언급. 기획·썸네일·장비·교통 구분 없음</div></li>\n    <li><div class="t">추가 촬영·재촬영·수정 횟수</div><div class="m">언급 없음 — 여기서 추가 비용이 가장 잘 샙니다</div></li>\n    <li><div class="t">라이브 중계가 별도인지 포함인지</div><div class="m">언급 없음. 1/20 라이브가 있다면 이게 큰 항목</div></li>\n    <li><div class="t">세금계산서·부가세 별도 여부</div><div class="m">언급 없음</div></li>\n  </ul>\n</div>\n\n<h2>⑤ 민트님께 보낼 메시지</h2>\n<div class="card">\n  <div class="note" style="margin:0 0 10px">그대로 복사해서 보내시면 됩니다</div>\n  <div class="emph" style="white-space:pre-wrap">민트님, 월요일에 조윤호 PD님과 통화하면서 이번 프로젝트 촬영 비용 이야기를 나눴습니다. 오늘 미팅 전에 공유드립니다.\n\n<b>1. 촬영 인건비</b>\nPD님 기준으로 촬영 인력 1인당 30~35만 원입니다. 장비 구성에 따라 달라질 수 있고, 말씀하신 건 최저 기준입니다.\n\n<b>2. 구성별 예상</b>\n· 홍보(모객) 영상 — 3~4명 투입, 4명 기준 약 120만 원\n· 본편 에피소드 — 최소 2명, 편당 60~70만 원\n· <b>편집은 PD님이 직접 맡아주시기로 해서 별도 비용이 없습니다</b>\n\n에피소드 5편 + 홍보 1편으로 잡으면 420~470만 원 선입니다. 다만 본편에 2명이 붙을지 3명이 붙을지는 기획이 확정돼야 나온다고 하셨습니다.\n\n<b>3. 수익 배분</b>\nPD님은 인당 정산이 아니라 <b>팀을 턴키로 묶어서 전체 매출의 일정 퍼센트</b>로 가져가는 방식을 말씀하셨습니다. 퍼센트는 아직 정하지 않으셨습니다.\n\n그리고 "촬영 팀원 인건비는 먼저 챙기고, 본인 몫은 RS로 가져가면 된다"는 입장이셨습니다. 본인 수익 목표는 따로 생각해두신 게 없다고 하셨고요.\n\n<b>4. 오늘 정하면 좋을 것</b>\n· 본편 편수와 구성 (→ 투입 인원 → 총액이 여기서 나옵니다)\n· RS 퍼센트\n· 추가 촬영·재촬영이 생겼을 때의 처리\n· 라이브 중계가 촬영비에 포함인지 별도인지\n· 지급 시기와 세금계산서 처리\n\n비용과 RS 세부는 민트님과 PD님이 직접 상의하시는 게 좋겠다고 PD님도 말씀하셨습니다. 오늘 미팅에서 같이 보시면 될 것 같습니다.</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">확인 필요</h3>\n  <ul class="list">\n    <li><div class="t">김한준 PD 측 편당 100만에 편집이 포함인지</div><div class="m">10/23 민트님 제안. 포함 여부에 따라 비교가 달라집니다</div></li>\n    <li><div class="t">본편 편수 확정</div><div class="m">10/30 미팅 기준 5개. 계산은 그 전제</div></li>\n    <li><div class="t">"추석 전에 결론" 발언</div><div class="m">녹음일이 11/2라 시기가 안 맞습니다. 전사 오인식으로 보여 날짜 근거로 쓰지 않았습니다</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  근거 · 2026-11-02 조윤호 PD 통화 녹취(44분) 전문, transaction_polish 177세그먼트 전수 + 금액 구간 원본 대조 ·\n  인용 타임스탬프 31:40 / 33:07 / 34:59 / 36:19 / 36:48 / 37:39 / 38:14 / 38:19 / 38:42 / 39:10 / 39:41 / 39:50 / 41:38 ·\n  에피소드 5편은 2026-10-30 민트·PD 3자 미팅 기준 · 편당 100만 × 7~8편은 2026-10-23 민트님 제안 ·\n  총액 표는 위 단가에 편수를 곱한 계산값 (PD님이 제시한 총액이 아님) ·\n  개인 브랜드 채널 운영 비용·수익 배분(통화 09:46~31:33)은 요청대로 제외\n</div>\n'

# ---------------------------------------------------------------- 300억 엑시트 검토
EXIT300 = '<div class="hero">\n  <h1>300억 엑시트 — 가능한가</h1>\n  <div class="sub">루크 · 메이븐 · 디노 공동창업 · 2년 내 목표 · 2026-11-04 검토</div>\n  <div class="goal">\n    <div><b>0원</b><span>2년째 법인 매출</span></div>\n    <div><b>30~50억</b><span>300억이 요구하는 연 영업이익</span></div>\n    <div><b>2,000명</b><span>그걸 만드는 활성 셀러 수</span></div>\n    <div><b>37%</b><span>수강생 중 그만큼 전환시켜야 함</span></div>\n  </div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">먼저 결론</h3>\n  <p style="margin:0 0 10px"><b>지금 사업의 연장선에서는 2년 내 300억이 안 됩니다.</b> 교육을 더 잘 팔아서 가는 길은 산수가 10배 이상 모자랍니다. 월 신규 50~100명에 객단가 300만을 다 채워도 연 36억이고, 교육업 배수로는 100억 근처입니다.</p>\n  <p style="margin:0 0 10px"><b>그런데 산수가 맞는 경로가 하나 있습니다.</b> 교육을 파는 회사가 아니라 <b>셀러한테서 매달 걷는 회사</b>가 되는 것 — 3PL·프로그램·판로를 묶어서 활성 셀러 2,000명에게 월 50만씩. 연 120억, 영업이익 36억, 인프라 배수 8배면 <b>288억</b>입니다. 300억이 거기서 보입니다.</p>\n  <p style="margin:0"><b>그리고 지금 가장 급한 건 전략이 아니라 장부입니다.</b> 2년째 법인 매출이 없으면, 2년 뒤에 인수자에게 보여줄 재무제표가 없습니다. 아무리 좋은 사업을 지어도 <b>힐링디어스 이름으로 쌓이지 않으면 팔리지 않습니다.</b></p>\n</div>\n\n<h2>① 300억이 요구하는 숫자</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:26%">경로</th><th>통상 배수</th><th>필요 실적</th></tr></thead>\n    <tbody>\n      <tr><td>교육업 매각</td><td>영업이익 4~6배</td><td>연 영업이익 <b>50~75억</b> → 매출 200~300억</td></tr>\n      <tr><td>구독·SaaS</td><td>연 반복매출 3~6배</td><td>ARR <b>50~100억</b> → 월 3만원 상품 14~28만 명</td></tr>\n      <tr><td>물류·유통 인프라</td><td>영업이익 6~10배</td><td>연 영업이익 <b>30~50억</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note">배수는 딜마다 다르고 공개 자료로 확정할 수 없어 <b>통상 범위로만</b> 썼습니다 — <b>확인 필요.</b> 다만 방향은 분명합니다: <b>교육업이 가장 낮고 인프라가 가장 높습니다.</b> 같은 300억을 받는 데 교육은 영업이익 50~75억이 필요하고 물류는 30~50억이면 됩니다. 사교육 쪽 매각이 실적 부진으로 난항을 겪은 사례도 보도된 바 있습니다.</div>\n</div>\n\n<h2>② 지금 가장 큰 구멍 — 팔 법인이 없습니다</h2>\n<div class="card red">\n  <p style="margin:0 0 10px"><b>2년째 법인 매출이 거의 없다는 게 이 검토에서 가장 무거운 사실입니다.</b> 돈이 안 벌린다는 뜻이 아닙니다 — 벌리는 돈이 인베이더·메이븐·초월스토리를 거쳐 <b>개인과 파트너 계산으로 흩어지고 있다</b>는 뜻입니다. 민트 건도, 가을 건도 그렇습니다.</p>\n  <p style="margin:0 0 10px">인수자는 사람을 사는 게 아니라 <b>법인의 반복 가능한 수익</b>을 삽니다. 이커머스 매각 중개를 하는 이숲도 평가 방식을 이렇게 설명합니다 — <b>"매도자가 제출하는 장부만으로는 인수자를 설득하기 어렵고, 절세 목적의 재무제표는 실제 수익력을 보여주지 못한다"</b>, 그래서 판매 채널을 직접 연동해 매출을 검증하고 실제 지출로 손익을 재구성한다고요.</p>\n  <div class="warn"><b>재구성할 손익조차 법인에 없으면 출발선이 마이너스입니다.</b> 지금 체결 중인 계약들의 수취 주체를 법인으로 바꾸는 것만으로 시작됩니다. 가을 건 1층 계약(8%)도, 민트 건도, 메이븐 기수도 — <b>개인이 아니라 힐링디어스가 받게</b> 하십시오. 2년 치 재무제표가 쌓여야 2년 뒤에 팔 게 있습니다. 이건 전략이 아니라 지금 당장의 서류 작업입니다.</div>\n  <div class="note">세무·법인 구조 변경은 세무사와 확인하셔야 합니다. 여기서는 매각 관점에서만 짚었습니다.</div>\n</div>\n\n<h2>③ 두 번째 구멍 — 루크님이 빠지면 0이 됩니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">강의도, 라이브도, 인터뷰도, 코칭도 전부 루크님 얼굴입니다. 인수자 눈에는 <b>키맨 리스크 100%</b>입니다. 이런 딜은 거의 예외 없이 <b>언아웃(2~3년 잔류·성과 조건)</b>이 걸립니다.</p>\n  <div class="warn"><b>"300억 엑시트"가 "300억 현금"인 경우는 드뭅니다.</b> 통상 계약금 + 잔류 조건부 + 성과 조건부로 쪼개지고, 조건을 못 채우면 뒤쪽은 못 받습니다. 300억에 사인하고 실수령 150억으로 끝나는 구조가 가장 흔합니다. <b>보부상님 건도 이 구분을 먼저 확인하셔야 합니다</b>(아래 ⑦).</div>\n  <p style="margin:10px 0 0">300억을 온전히 받으려면 <b>루크님 없이 돌아가는 매출의 비중</b>이 커야 합니다. 프로그램 구독, 3PL 수수료, 셀러 네트워크 — 얼굴이 필요 없는 수익입니다. 지금 그 비중이 몇 %인지가 밸류에이션의 절반을 결정합니다.</p>\n</div>\n\n<h2>④ 세 번째 구멍 — 6개로 쪼개져 있습니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">식스 엔진으로 하루에 하나씩 돌리는 방식은 현금 흐름에는 맞지만 <b>매각에는 정반대</b>입니다. 인수자는 6개 중 1~2개만 원하고, 나머지는 <b>"정리해야 할 것"으로 보여 할인 요인</b>이 됩니다.</p>\n  <div class="note">2년 뒤에 파는 걸 전제로 한다면, <b>하나를 고르고 나머지 다섯은 그 하나의 유입 장치로 재배치</b>해야 합니다. 없애라는 게 아니라 <b>종속시키라는</b> 뜻입니다 — 강의는 셀러를 모으는 깔때기, 컨설팅은 상위 셀러를 거르는 체, 콘텐츠는 그 위의 유입. 전부 하나의 숫자(활성 셀러 수)로 수렴해야 스토리가 하나가 됩니다.</div>\n</div>\n\n<h2>⑤ 산수가 맞는 유일한 경로</h2>\n<div class="card gold">\n  <p style="margin:0 0 10px">루크님이 가진 것 중 배수가 붙는 건 하나입니다 — <b>수강생이 실제로 파는 상품의 흐름을 쥐는 것.</b> 3PL로 재고를 쥐고, 소싱·등록·가격관리 프로그램으로 상품 등록을 쥐고, 역직구로 판로를 쥡니다. <b>교육은 그 셀러를 모으는 장치</b>이지 상품이 아닙니다.</p>\n  <div class="fig">\n  <svg viewBox="0 0 400 112" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="활성 셀러 수별 기업가치">\n    <line x1="259" y1="2" x2="259" y2="94" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity="0.5"/>\n    <text x="262" y="108" font-size="9" fill="currentColor" opacity="0.7">목표 300억</text>\n    <text x="2" y="15" font-size="10" fill="currentColor">1,000명 · 40만</text>\n    <rect x="92" y="6" width="64" height="11" fill="var(--f1)"/>\n    <text x="398" y="15" font-size="10" text-anchor="end" fill="currentColor">115억</text>\n    <text x="2" y="37" font-size="10" fill="currentColor">2,000명 · 40만</text>\n    <rect x="92" y="28" width="128" height="11" fill="var(--f2)"/>\n    <text x="398" y="37" font-size="10" text-anchor="end" fill="currentColor">230억</text>\n    <text x="2" y="59" font-size="10" fill="currentColor">2,000명 · 50만</text>\n    <rect x="92" y="50" width="160" height="11" fill="var(--f3)"/>\n    <text x="398" y="59" font-size="10" text-anchor="end" fill="currentColor">288억</text>\n    <text x="2" y="81" font-size="10" fill="currentColor">3,000명 · 50만</text>\n    <rect x="92" y="72" width="240" height="11" fill="var(--f4)"/>\n    <text x="398" y="81" font-size="10" text-anchor="end" fill="currentColor">432억</text>\n  </svg>\n  </div>\n  <div class="note">계산: 활성 셀러 수 × 1인당 월 수취액 × 12 = 연 매출 → 영업이익률 30% → <b>인프라 배수 8배</b>. 1인당 월 40~50만은 3PL 수수료 + 프로그램 구독 + 소싱 마진을 합친 가정치입니다 — <b>확인 필요.</b> 배수 8배도 범위의 중간값입니다.</div>\n  <div class="warn"><b>300억 라인은 "활성 셀러 2,000명 × 월 50만"입니다.</b> 현재 수강생 3,000명 + 2년 유입 2,400명(월 100명 기준) = 풀 5,400명. 그중 <b>37%를 월 50만을 내는 활성 셀러로</b> 만들면 숫자가 맞습니다.</div>\n</div>\n\n<h2>⑥ 그래서 결정적인 숫자는 하나입니다</h2>\n<div class="card accent">\n  <h3 style="margin:0 0 8px">수강생 → 돈 내는 활성 셀러 전환율</h3>\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:30%">전환율</th><th>활성 셀러</th><th>월 50만 기준 기업가치</th></tr></thead>\n    <tbody>\n      <tr><td>10%</td><td>540명</td><td>78억</td></tr>\n      <tr><td>20%</td><td>1,080명</td><td>156억</td></tr>\n      <tr><td><b>37%</b></td><td><b>2,000명</b></td><td><b>288억</b></td></tr>\n      <tr><td>50%</td><td>2,700명</td><td>389억</td></tr>\n    </tbody>\n  </table>\n  </div>\n  <div class="note"><b>지금 이 숫자가 몇 %인지 모르신다면, 그게 첫 번째로 측정할 것입니다.</b> 3PL에 재고를 맡긴 수강생이 몇 명인지, 그중 월 매출이 꾸준히 나오는 사람이 몇 명인지 — 이번 주에 셀 수 있는 숫자입니다. 10%면 300억은 포기하고 150억짜리 그림을 다시 그려야 하고, 30%가 넘으면 전부를 여기에 거는 게 맞습니다.</div>\n</div>\n\n<h2>⑦ 메이븐님·디노님 지분 — 지금 안 정하면 반드시 터집니다</h2>\n<div class="card red">\n  <p style="margin:0 0 10px">300억이면 <b>지분 1%가 3억</b>입니다. 지금 셋이 나누는 숫자가 2년 뒤에 그 무게가 됩니다. 그리고 2년짜리 게임에서 가장 흔한 사고가 여기서 납니다.</p>\n  <ul class="list">\n    <li><div class="t">베스팅이 없으면 6개월 뒤 이탈해도 지분은 그대로 갑니다</div><div class="m">통상 4년 베스팅 + 1년 클리프. 1년 안에 나가면 0, 그 뒤로는 매달 쌓이는 구조. 셋 다 동일하게 거십시오 — 루크님 본인도 포함해야 설득이 됩니다.</div></li>\n    <li><div class="t">동반매도요구권(드래그얼롱)이 없으면 한 명이 매각을 막습니다</div><div class="m">2년 뒤 인수자는 100% 지분을 원합니다. 한 명이 "나는 안 팔겠다"고 하면 딜이 깨집니다. 다수가 팔기로 하면 나머지도 따라 팔도록 미리 걸어두십시오.</div></li>\n    <li><div class="t">우선매수권·양도제한이 없으면 지분이 밖으로 샙니다</div><div class="m">실사에서 주주명부가 지저분하면 그 자체로 할인 요인입니다.</div></li>\n    <li><div class="t">누가 무엇을 책임지는지가 지분율의 근거여야 합니다</div><div class="m">메이븐님은 이미 사내이사이고 화장품 강의 쪽 실행을 쥐고 있습니다. 디노님의 역할 범위는 이 검토에 안 잡혀 있습니다 — <b>확인 필요.</b> "친하니까 1/3"은 2년 뒤에 가장 비싼 선택이 됩니다.</div></li>\n  </ul>\n  <div class="note">주주간계약은 변호사와 작성하셔야 합니다. 여기서는 빠지면 안 되는 항목만 짚었습니다.</div>\n</div>\n\n<h2>⑧ 24개월 역산</h2>\n<div class="card">\n  <ul class="list">\n    <li><div class="t">0~3개월 — 장부와 지분</div><div class="m">모든 수취 주체를 법인으로 전환 · 주주간계약 체결(베스팅·드래그얼롱) · <b>전환율 실측</b> · 6개 중 1개 선택</div></li>\n    <li><div class="t">3~9개월 — 과금 구조 세우기</div><div class="m">셀러 1인당 월 정액이 실제로 걷히는지 검증. 100명에게서 월 50만이 걷히면 모델이 증명된 것. 안 걷히면 여기서 멈추고 숫자를 다시 잡아야 합니다.</div></li>\n    <li><div class="t">9~18개월 — 숫자 쌓기</div><div class="m">활성 셀러 1,000명. 이 구간에 법인 재무제표가 처음으로 의미를 가집니다. 루크님 의존 매출 비중을 50% 아래로.</div></li>\n    <li><div class="t">18~24개월 — 매각 준비</div><div class="m">활성 셀러 2,000명 · 반복 수익 비중 70% · 실사 대응 자료 정리 · 인수 후보 접촉</div></li>\n  </ul>\n  <div class="warn">이 일정에서 <b>가장 먼저 깨지는 건 3~9개월 구간</b>입니다. "수강생은 교육비는 내도 월 이용료는 안 낸다"가 가장 흔한 벽입니다. 그래서 100명 검증을 9개월 안에 끝내야, 안 되면 남은 15개월에 다른 그림을 그릴 수 있습니다.</div>\n</div>\n\n<h2>⑨ 보부상님 건 — 검색으로 안 나옵니다</h2>\n<div class="card">\n  <p style="margin:0 0 10px">"보부상" 이름으로 매각·엑시트 관련 공개 보도를 찾지 못했습니다. 이커머스 교육 쪽 인물로도, 300억 거래 기록으로도 잡히지 않습니다. <b>지어내지 않겠습니다</b> — 비상장 소규모 M&A는 공시 의무가 없어 보도되지 않는 게 정상이기도 합니다.</p>\n  <div class="note">알려주시면 바로 분석에 넣겠습니다. 특히 이 다섯 가지가 비교의 기준이 됩니다.</div>\n  <ul class="list">\n    <li><div class="t">1. 본명·채널명·법인명</div><div class="m">제가 다시 검색해볼 수 있습니다</div></li>\n    <li><div class="t">2. 300억이 현금인가, 조건부인가</div><div class="m">계약금 / 잔류 조건부 / 성과 조건부(언아웃)의 비율. <b>여기서 대부분의 "300억"이 실제로는 절반이 됩니다.</b> 이게 가장 중요합니다</div></li>\n    <li><div class="t">3. 무엇을 팔았나</div><div class="m">교육 사업 / 커머스 브랜드 / 프로그램 / 물류 — 어느 쪽이었는지에 따라 배수가 완전히 다릅니다</div></li>\n    <li><div class="t">4. 매각 시점의 매출과 영업이익</div><div class="m">300억 ÷ 실적 = 실제 배수. 이 숫자 하나가 루크님 목표의 현실성을 재는 자가 됩니다</div></li>\n    <li><div class="t">5. 인수자가 누구인가</div><div class="m">상장사 / 사모펀드 / 동종업계. 상장사의 전략적 인수면 배수가 높게 나올 수 있고, 그건 루크님도 같은 경로를 노려야 한다는 뜻입니다</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">확인 필요</h3>\n  <ul class="list">\n    <li><div class="t">수강생 → 활성 셀러 전환율</div><div class="m">300억의 가능·불가능을 가르는 유일한 숫자</div></li>\n    <li><div class="t">3PL 현재 이용 수강생 수와 1인당 월 수취액</div><div class="m">월 40~50만은 가정치입니다</div></li>\n    <li><div class="t">법인 매출이 "거의 없다"의 실제 수치</div><div class="m">2025·2026 힐링디어스 매출과 영업이익</div></li>\n    <li><div class="t">디노님의 역할 범위</div><div class="m">지분율의 근거가 됩니다</div></li>\n    <li><div class="t">보부상님 건의 다섯 가지</div><div class="m">위 ⑨</div></li>\n    <li><div class="t">업종별 실제 거래 배수</div><div class="m">여기 쓴 4~10배는 통상 범위 추정이고 공개 자료로 확정되지 않았습니다</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  근거 · 루크님 진술(법인 통째 매각 · 2년째 법인 매출 거의 없음 · 공동창업자 지분 나눔) ·\n  수강생 약 3,000명, 월 신규 50~100명, 유튜브 약 1만, 카톡 약 1,000명은 기존 기록 ·\n  이커머스 스토어 가치평가 방식(장부·절세 재무제표의 한계, 손익 재구성, 반복 가능 수익 기준)은 이숲 관련 보도 ·\n  사교육 매각 난항 사례는 이투스교육 관련 보도(2024) ·\n  업종별 배수(교육 4~6배 / 구독 3~6배 / 인프라 6~10배)와 1인당 월 수취액 40~50만은 <b>확인 필요한 추정 범위</b>이며 공개 자료로 확정되지 않음 ·\n  기업가치 수치는 전부 위 가정에 따른 계산값이며 제안이나 평가액이 아님 ·\n  "보부상" 관련 매각 보도는 검색되지 않음\n</div>\n'

# ---------------------------------------------------------------- 11/4 3자 회의록
MIN1104 = '<div class="mtg">\n<div class="mnav"><a href="../meetings/">전체 회의록</a><a href="../min1030/">10/30 3자</a><a class="on" href="../min1104/">11/4 3자</a><a href="../min1111/">11/11 3자</a></div>\n\n<div class="hero">\n  <h1>11/4 회의록</h1>\n  <div class="sub">윤호 PD · 민트 · 루크 · 2026-11-04(수) 12:01~12:50 · 줌 · 스스로 월백 / 다마고치</div>\n  <div class="goal">\n    <div><b>11/10(화)</b><span>모집영상 촬영 1안</span></div>\n    <div><b>2명</b><span>다마고치 출연자 확정</span></div>\n    <div><b>5+1편</b><span>본편 5 + 모집영상 1</span></div>\n    <div><b>11월 말</b><span>다마고치 선정 완료</span></div>\n  </div>\n</div>\n\n<h2>마감까지 <small>실시간</small></h2>\n<div class="card">\n  <div class="ddrow"><div class="lab"><b>PD 팀 미팅 회신 — 11/10 촬영 가능?</b><span>오늘 15~16시 · 윤호 PD</span></div><span class="dday" data-due="2026-11-04T16:00:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>촬영 장소 섭외</b><span>오늘 중 · 민트</span></div><span class="dday" data-due="2026-11-04T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>\'스스로 월백\' 채널 개설 + 공동작업자 연결</b><span>루크</span></div><span class="dday" data-due="2026-11-09T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>콘티 큰 틀 · 레퍼런스 샷 전달</b><span>이번 주 안 · 민트/루크 → PD</span></div><span class="dday" data-due="2026-11-08T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>모집영상 촬영 (1안)</b><span>11/10(화) 오후 1시 가정</span></div><span class="dday" data-due="2026-11-10T13:00:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>1차 가편 — 촬영일 +72시간</b><span>윤호 PD</span></div><span class="dday" data-due="2026-11-13T13:00:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>모집영상 업로드 — 촬영일 +9일</b><span>11/19 목표</span></div><span class="dday" data-due="2026-11-19T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>다마고치 모집·선정 완료</b><span>11월 말</span></div><span class="dday" data-due="2026-11-30T23:59:00+09:00"></span></div>\n  <div class="note">한국 시간 기준으로 1초마다 다시 계산됩니다. 1안(11/10)이 어긋나면 2안 11/16~17로 전체가 6~7일씩 밀립니다.</div>\n</div>\n\n<h2>각자 해야 할 일</h2>\n\n<div class="who pd">\n  <div class="hd2"><b>조윤호 PD</b><span class="dday" data-due="2026-11-04T16:00:00+09:00"></span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">오늘(11/4) 3~4시 팀 미팅에서 11/10 촬영 가능 여부 확인</div><div class="m">확인 후 카톡방에 전달. "10일로 생각해놓고 미리 전달"하기로 합의</div></li>\n    <li><div class="t">면접관 역 출연자 4~5명 사전 컨택</div><div class="m">"미리 컨택해주셨으면 좋겠다"는 요청. 페르소나는 다양할 필요 없고 질문의 대표성만 있으면 됨</div></li>\n    <li><div class="t">세부 콘티 작성</div><div class="m">구성작가를 안 쓰기로 해서 PD가 직접. 큰 틀과 레퍼런스 샷을 받은 뒤 살을 붙이는 순서</div></li>\n    <li><div class="t">편집·업로드 가능 일정 체크해서 회신</div><div class="m">목표는 촬영일 +72시간 내 1차 가편, 촬영일 +9일 내 업로드</div></li>\n    <li><div class="t">촬영 장비 구성 체크</div><div class="m">장소가 정해지면. 카메라가 늘면 촬영 분량이 늘어나는 점을 우려</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="who mint">\n  <div class="hd2"><b>민트</b><span class="dday" data-due="2026-11-04T23:59:00+09:00"></span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">촬영 장소 섭외 — 오늘 중</div><div class="m">"장소 제가 한번 알아볼게요." 후보가 나오면 카톡방에 올려 의견 받기</div></li>\n    <li><div class="t">콘티 큰 틀 + 레퍼런스 샷 작성해 PD께 전달</div><div class="m">"가볍게만 주셔도 된다"는 PD 요청. 빠르게 전달하기로</div></li>\n    <li><div class="t">다마고치 모집 광고 집행 준비</div><div class="m">업로드 직후 시작. 예시로 11/18~27 구간을 언급</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="who luke">\n  <div class="hd2"><b>루크</b><span class="dday" data-due="2026-11-09T23:59:00+09:00"></span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">\'스스로 월백\' 채널 신규 개설 + 셀러들의 수다에 공동작업자 연결</div><div class="m">프로젝트 영상은 스스로 월백에 올리고, 셀러들의 수다가 본진. <b>채널 소유 명의는 회의에서 미정</b></div></li>\n    <li><div class="t">11/10 촬영 일정 확보</div><div class="m">수·목은 가능하면 피하고 싶다고 밝혔으나 불가피하면 비울 수 있다고 함. 11/10은 화요일이라 해당 없음</div></li>\n    <li><div class="t">회의 내용 정리해서 공유</div><div class="m">회의 말미에 정리본을 올리기로 함 — 이 페이지</div></li>\n  </ul>\n  </div>\n</div>\n\n<h2>전체 일정 한눈에</h2>\n<div class="ig">\n<svg viewBox="0 0 400 128" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="11월 4일부터 1월 중순까지 단계별 일정">\n  <defs>\n    <linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#0ea5a4"/><stop offset="1" stop-color="#14b8a6"/></linearGradient>\n    <linearGradient id="g2" x1="0" x2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#6366f1"/></linearGradient>\n    <linearGradient id="g3" x1="0" x2="1"><stop offset="0" stop-color="#f59e0b"/><stop offset="1" stop-color="#f97316"/></linearGradient>\n    <linearGradient id="g4" x1="0" x2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ec4899"/></linearGradient>\n  </defs>\n  <rect x="20" y="46" width="29" height="20" rx="5" fill="url(#g1)"/>\n  <rect x="51" y="46" width="44" height="20" rx="5" fill="url(#g2)"/>\n  <rect x="97" y="46" width="63" height="20" rx="5" fill="url(#g3)"/>\n  <rect x="162" y="46" width="218" height="20" rx="5" fill="url(#g4)"/>\n\n  <text x="20" y="40" font-size="9" fill="currentColor">11/4</text>\n  <text x="51" y="40" font-size="9" fill="currentColor">11/10</text>\n  <text x="97" y="40" font-size="9" fill="currentColor">11/19</text>\n  <text x="162" y="40" font-size="9" fill="currentColor">12/1</text>\n  <text x="380" y="40" font-size="9" text-anchor="end" fill="currentColor">1/15</text>\n\n  <line x1="20" y1="44" x2="20" y2="24" stroke="currentColor" stroke-width="1" opacity=".3"/>\n  <line x1="51" y1="44" x2="51" y2="24" stroke="currentColor" stroke-width="1" opacity=".3"/>\n  <line x1="97" y1="44" x2="97" y2="24" stroke="currentColor" stroke-width="1" opacity=".3"/>\n  <line x1="162" y1="44" x2="162" y2="24" stroke="currentColor" stroke-width="1" opacity=".3"/>\n\n  <text x="20" y="18" font-size="8.5" fill="currentColor" opacity=".75">오늘</text>\n  <text x="51" y="18" font-size="8.5" fill="currentColor" opacity=".75">촬영</text>\n  <text x="97" y="18" font-size="8.5" fill="currentColor" opacity=".75">업로드</text>\n  <text x="162" y="18" font-size="8.5" fill="currentColor" opacity=".75">선정 완료</text>\n\n  <text x="20" y="80" font-size="9.5" fill="currentColor">준비</text>\n  <text x="51" y="80" font-size="9.5" fill="currentColor">촬영·편집</text>\n  <text x="97" y="80" font-size="9.5" fill="currentColor">모집 광고</text>\n  <text x="162" y="80" font-size="9.5" fill="currentColor">다마고치 본편 5편 제작</text>\n\n  <text x="20" y="97" font-size="8.5" fill="currentColor" opacity=".65">장소·콘티·섭외</text>\n  <text x="97" y="97" font-size="8.5" fill="currentColor" opacity=".65">11/18~27 집행 예시</text>\n  <text x="162" y="97" font-size="8.5" fill="currentColor" opacity=".65">미팅 → 촬영 → 업로드 반복</text>\n  <text x="20" y="116" font-size="8.5" fill="currentColor" opacity=".55">※ 1안 11/10 기준. 2안(11/16~17)이면 전 구간 6~7일 밀림</text>\n</svg>\n<div class="cap">막대 길이는 실제 기간 비율입니다. 가장 긴 구간은 12월~1월 중순의 본편 제작이지만, 그 구간이 시작되려면 11월 말까지 다마고치 선정이 끝나야 합니다.</div>\n</div>\n\n<h2>채널 구조 — 오늘 가장 큰 결정</h2>\n<div class="ig">\n<svg viewBox="0 0 400 136" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="셀러들의 수다와 스스로 월백 채널 관계">\n  <rect x="8" y="30" width="168" height="62" rx="12" fill="none" stroke="#0ea5a4" stroke-width="1.6"/>\n  <text x="92" y="50" font-size="11" text-anchor="middle" fill="currentColor" font-weight="700">셀러들의 수다</text>\n  <text x="92" y="64" font-size="9" text-anchor="middle" fill="currentColor" opacity=".75">본진 · 구독자 보유</text>\n  <text x="92" y="78" font-size="9" text-anchor="middle" fill="currentColor" opacity=".75">조회 2,000 / 노출 3,000</text>\n\n  <rect x="224" y="30" width="168" height="62" rx="12" fill="none" stroke="#8b5cf6" stroke-width="1.6"/>\n  <text x="308" y="50" font-size="11" text-anchor="middle" fill="currentColor" font-weight="700">스스로 월백</text>\n  <text x="308" y="64" font-size="9" text-anchor="middle" fill="currentColor" opacity=".75">신규 · 다마고치 전용</text>\n  <text x="308" y="78" font-size="9" text-anchor="middle" fill="currentColor" opacity=".75">프로젝트 영상만 업로드</text>\n\n  <line x1="178" y1="61" x2="222" y2="61" stroke="currentColor" stroke-width="1.4" opacity=".55" stroke-dasharray="4 3"/>\n  <text x="200" y="54" font-size="8.5" text-anchor="middle" fill="currentColor" opacity=".8">공동작업자</text>\n  <text x="200" y="76" font-size="8.5" text-anchor="middle" fill="currentColor" opacity=".55">양쪽에 노출</text>\n\n  <text x="200" y="16" font-size="9.5" text-anchor="middle" fill="currentColor" opacity=".8">첫 영상은 광고로 노출을 구매 → CTA 반응이 알고리즘을 만든다</text>\n  <text x="200" y="112" font-size="9" text-anchor="middle" fill="currentColor" opacity=".7">신규 채널 단독 개설은 하지 않음 — 알고리즘이 붙으려면 영상 4편 이상 필요</text>\n  <text x="200" y="128" font-size="8.5" text-anchor="middle" fill="currentColor" opacity=".5">리스크: 들어왔을 때 구독자 수가 적으면 초반 이탈</text>\n</svg>\n</div>\n\n<h2>결정 사항</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:36%">안건</th><th>결론</th></tr></thead>\n    <tbody>\n      <tr><td>신규 채널 단독 개설</td><td><b>하지 않음.</b> 셀러들의 수다를 본진으로, 스스로 월백 채널을 따로 만들어 <b>공동작업자</b>로 연결</td></tr>\n      <tr><td>다마고치 인원</td><td><b>최대 2명.</b> 3명은 변수가 곱으로 늘어 무리라고 판단</td></tr>\n      <tr><td>모집 공고 표기</td><td>인원 수를 공개하지 않고 "적합한 사람만" 선발. 지원자를 늘리기 위함</td></tr>\n      <tr><td>편수</td><td>본편 <b>5편</b> + 모집영상 1편 = 실질 <b>6편</b></td></tr>\n      <tr><td>모집영상 촬영일</td><td><b>1안 11/10(화)</b> · 2안 11/16~17 · <b>11/13(금) 불가</b>(PD 남양주 촬영)</td></tr>\n      <tr><td>모집영상 콘셉트</td><td><b>청문회·압박면접.</b> 빈 공간에 루크가 들어와 당황할 때 면접관들이 들어오는 구성</td></tr>\n      <tr><td>구성작가</td><td><b>쓰지 않음.</b> 내부에서 디벨롭하고 현장에서 연출로 방향만</td></tr>\n      <tr><td>제작 일정 기준</td><td>촬영일 +72시간 내 1차 가편 · 촬영일 +9일 내 업로드</td></tr>\n      <tr><td>다마고치 모집·선정</td><td><b>11월 말까지</b> 1차 모집·선정과 컨택</td></tr>\n      <tr><td>본편 진행</td><td><b>12월 ~ 1월 중순</b> 미팅·촬영·업로드</td></tr>\n      <tr><td>출연자(엑스트라) 비용</td><td>시간당이 아니라 <b>1회차 기준 인당 15만원</b></td></tr>\n      <tr><td>소통 채널</td><td>PD의 오늘 3시 미팅 이후 <b>카톡방</b></td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<h2>상세 회의록</h2>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">0. 시작 — 음성 문제와 줌 끊김</h3>\n  <p style="margin:0">12:01 시작. 초반에 민트 음성이 들리지 않아 몇 분 지연됐고 윤호 PD는 조금 늦게 입장. 12:39경 <b>줌 무료 버전 40분 제한</b>으로 방이 종료돼 새 방에서 12:41~12:50 이어서 진행. 녹음이 두 개로 나뉜 이유.</p>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">1. 신규 채널을 팔 것인가 — 가장 길게 다룬 안건</h3>\n  <p style="margin:0 0 10px"><b>민트의 문제 제기.</b> 셀러들의 수다는 구독자 수는 있지만 <b>알고리즘 최적화가 안 돼 있을 확률이 높다</b>고 봄. 그동안 라이브와 강의 운영 위주로 써서 홍보 채널 성격이 아니고, 홈 화면 알고리즘이 타깃 연령·관심사에 맞춰져 있지 않아 보인다는 것.</p>\n  <ul class="list">\n    <li><div class="t">지표 — 셋이 화면을 같이 보며 확인</div><div class="m">최근 영상 조회수 약 <b>2,000</b>, 노출수 약 <b>3,000</b>에서 정체. 마지막 업로드 8일 전. 민트: <b>"알고리즘이 제대로 돌았으면 8일 전 영상이 최소 조회수 1,000은 나와야 한다."</b> 일부공개 영상이 다수고 반응한 사람 대부분이 수강생</div></li>\n    <li><div class="t">채널의 내력 — 루크 설명</div><div class="m">원래 <b>동기부여·명언 채널</b>. 시청자가 30~40대라 주제와 나이대가 맞아 구매. 처음엔 본인 이름으로 브랜딩하려다 방치했고, 강의를 다시 시작하며 강의용으로 돌려 수강생을 넣어둠. "되도 안 되도 된다"</div></li>\n    <li><div class="t">PD 의견 — 처음엔 신규 개설 쪽</div><div class="m">"기존 것에 영향을 받다 보니 아예 성장이 안 될 수도 있다. 잘 되는 것보다 <b>리스크를 생각하면 새로 만드는 게 낫겠다</b>"</div></li>\n    <li><div class="t">민트의 반론 — 광고로 시작하면 차이가 작다</div><div class="m">"어차피 첫 영상은 광고를 돌릴 거고, 그건 <b>노출을 돈 주고 사는 것</b>이다. 신규든 셀수다든 산 노출을 다시 알고리즘으로 뿌리는 격이라, CTA에 반응만 해주면 두 채널 다 크게 상관없을 수 있다." 다만 <b>들어왔는데 구독자가 30명이면 초반 이탈</b>이 날 수 있다는 점은 우려</div></li>\n    <li><div class="t">인베이더 사례</div><div class="m">민트: 인베이더에서 채널을 새로 팠을 때 <b>알고리즘은 바로 타지 않고 영상이 최소 4개는 올라가야 그때부터 움직였다</b>. "너무 늦어버린다"</div></li>\n    <li><div class="t">PD의 절충안</div><div class="m">기존 채널들에 영상을 시차를 두고 올려보고 반응 없으면 비공개 처리하는 <b>테스트</b> 제안. 민트도 "2~3일이면 지표가 나온다"며 동의</div></li>\n    <li><div class="t">최종 결론 — 공동작업자</div><div class="m">PD: "공동작업자로 가면 이 채널에 뭐가 올라오겠구나가 보이니까 <b>서브 채널을 같이 키운다는 느낌</b>으로 가는 게 괜찮겠다."<br>민트 정리: <b>스스로 월백 채널을 만들고 셀러들의 수다에 공동작업자로 걸어 프로젝트 영상을 올린다.</b> 스스로 월백은 다마고치 전용, 셀러들의 수다는 본진으로 두고 루크 퍼스널 브랜딩과 회사 영상을 계속 테스트</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">2. 다마고치 인원 — 3명에서 2명으로</h3>\n  <p style="margin:0 0 10px"><b>PD:</b> 촬영 리소스 기준 <b>3명까지 가능</b>. 3명이면 그룹샷 1명 + 개별 2명, 거기에 루크 마킹까지 <b>최소 3명 인력</b>, 카메라 한 대는 풀샷 거치. 출연 인물은 다마고치 3 + 루크 = 4명.</p>\n  <p style="margin:0 0 10px"><b>민트의 제동.</b> "3명이면 변수가 곱하기로 늘어난다. 가장 이상적인 그림은 <b>전원이 기간 내 목표를 달성하고 그 이후 추이가 달라지는 것</b> — 스스로 월백이면 각자 100만원씩은 벌되 그 이상에서 차등이 나는 구조다. 그런데 루크님은 다른 수강생 케어와 강의 준비도 하셔야 해서 한 명 한 명에 리소스를 다 넣을 수 있을지 모르겠다."</p>\n  <div class="warn"><b>루크 수용.</b> "첫 번째라서 3명은 무리일 수 있겠다. 많아도 2명이어야 할 것 같고, 한 명이면 전담 마크가 가능해서 좋긴 하다. 저도 새로 오픈하는 것도 있고 PD님도 연말이라 일정이 많다고 하셨으니 <b>변수를 크게 만들기보다 많아도 2명으로 제한</b>하는 게 좋겠다."</div>\n  <p style="margin:10px 0 0"><b>PD 동의:</b> "두 명이 가장 좋을 것 같다. 흑백 느낌으로 가도 된다. 다양한 패턴을 보여주는 건 무리다." → <b>모집 시에는 인원을 밝히지 않고</b> 지원자를 많이 받은 뒤 케어 가능한 선에서 결정.</p>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">3. 일정 — 11/10을 1안으로</h3>\n  <ul class="list">\n    <li><div class="t">촬영 전 체크할 세 가지 (민트 정리)</div><div class="m">① 장소 ② 촬영 인력이 그 시간에 올 수 있는지 ③ 출연자 섭외가 그때까지 되는지. 콘티는 이번 주 안에 짜면 되므로 일정과 무관</div></li>\n    <li><div class="t">각자 가능 일자</div><div class="m">루크 — 수·목만 빼주면 되고 불가피하면 비울 수 있음 / 민트 — 전부 가능 / PD — 화·수가 괜찮고 <b>11/10~11 사이</b> 선호. <b>11/13(금)은 남양주 촬영</b>으로 불가</div></li>\n    <li><div class="t">확정</div><div class="m"><b>1안 11/10(화)</b>, 2안 11/16~17. PD가 오늘 3~4시 팀 미팅에서 확인 후 카톡방 공유. "10일로 생각해놓고 미리 전달해도 되겠느냐"는 질문에 민트 동의</div></li>\n    <li><div class="t">제작 리드타임</div><div class="m">PD: 가편만 던지는 건 <b>2~3일이면 충분</b>. 다만 13일 촬영 세팅 때문에 하루는 그쪽에 써야 함. "촬영하고 이틀 안에 1차 가편을 최대한 뽑아보겠다"<br>민트가 기준으로 정리: <b>촬영일 +72시간 내 1차 가편</b>, 피드백 반영 후 업로드까지 <b>촬영일 +9일</b></div></li>\n    <li><div class="t">역산</div><div class="m">11/10 촬영 → <b>11/18~19 업로드</b> → 광고 집행(예: 11/18~27) → <b>11월 말까지 1차 모집·선정과 컨택</b> → <b>12월~1월 중순</b> 본편 미팅·촬영·업로드</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">4. 구성작가를 쓸 것인가 — 쓰지 않기로</h3>\n  <p style="margin:0 0 10px">PD가 주변 구성작가 기용 가능성을 열며 시작. 예능·스케치 코미디·숏폼 시나리오를 쓰던 분들이 있어 "재밌는 호흡"을 만들 수 있지 않을까 하는 취지.</p>\n  <ul class="list">\n    <li><div class="t">비용</div><div class="m"><b>편당 20~30만원</b> 수준. 콘티를 짜주는 대가</div></li>\n    <li><div class="t">민트 우려 1 — 커머스 이해</div><div class="m">"커머스에 대한 이해가 없으면 예능작가 식으로 해도 한계가 있다. <b>1편(모집·홍보 영상)에는 끼는 게 괜찮지만 그 이후 다마고치 프로젝트 영상에는 안 끼는 게 낫다</b>"</div></li>\n    <li><div class="t">우려 2 — 예능처럼 보일 위험</div><div class="m">"구성작가를 껴서 하면 너무 예능 형식으로 보이지 않을까"</div></li>\n    <li><div class="t">PD 최근 이력</div><div class="m">구성작가와 한 최근 작업은 예능이 아니라 <b>공공기관 건</b>(인천 스마트패스 등). 웹예능도 몇 건 있었으나 그 작가와는 연락이 끊긴 지 오래</div></li>\n    <li><div class="t">결론</div><div class="m">PD: "시간도 타이트하니 <b>웬만하면 구성작가를 안 끼는 게 좋겠다.</b> 우리끼리 디벨롭해서 현장에서 방향성만 연출로 잡으면 될 것 같다." 민트도 "우리끼리 고민하면 충분히 나올 수 있다"며 동의</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">5. 모집영상 콘셉트와 출연자</h3>\n  <ul class="list">\n    <li><div class="t">콘셉트 — 청문회 / 압박면접</div><div class="m">"올해 청문회 느낌이었으면 재밌겠다"는 의견에서 출발. 아무것도 없는 빈 공간에 루크가 들어와 당황하고 있을 때 사람들이 들어와 청문회 형식으로 질문하는 그림</div></li>\n    <li><div class="t">출연자 — 면접관 역 4~5명</div><div class="m">PD: "최소 4명은 있어야 할 것 같다." 원하는 이미지나 캐릭터를 미리 모아주면 섭외를 시도해보겠다고 함</div></li>\n    <li><div class="t">캐릭터 설정</div><div class="m">"페르소나가 여러 개일 필요는 없다. <b>그 질문에 대한 대표성만 있으면 된다</b>"</div></li>\n    <li><div class="t">일정 우려</div><div class="m">"10일은 진짜 촉박하다"는 말이 나왔고 16~17일이면 충분하다는 의견. 다만 PD가 "11일도 충분히 가능할 수 있다"고 해 1안을 유지하고 미리 컨택하기로</div></li>\n    <li><div class="t">비용</div><div class="m">"시간당 8~10만원 정도로 보면 되느냐"는 질문에 PD: 시간당보다 <b>하루 1회차 기준</b>이 낫고 <b>인당 15만원</b> 정도. 보통 6~8시간, 길면 12시간 기준. 엑스트라 개념</div></li>\n    <li><div class="t">콘티 분담</div><div class="m">큰 틀과 레퍼런스 샷은 민트·루크 측이 가볍게 만들어 전달 → PD가 받아 살을 붙여 세부 콘티 완성</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">6. 마무리</h3>\n  <p style="margin:0">루크는 "오늘은 청취자였다, 흐름은 다 이해했고 잘 준비하겠다"고 밝힘. 세부 콘티와 로케가 정해지면 다시 논의하기로 하고, PD의 3시 미팅 이후로는 <b>카톡방에서 소통</b>. PD가 별도로 연락드리겠다 했고, 일정이 있을 수 있으니 카톡을 먼저 남겨달라고 요청.</p>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">정해지지 않은 것</h3>\n  <ul class="list">\n    <li><div class="t">촬영 장소</div><div class="m">민트가 오늘 중 알아보기로만 함</div></li>\n    <li><div class="t">11/10 촬영 인력 확보 여부</div><div class="m">PD가 오늘 3~4시 미팅 후 회신. 여기서 1안·2안이 갈림</div></li>\n    <li><div class="t">출연자 4~5명 섭외 가능 여부</div><div class="m">컨택 시작 단계</div></li>\n    <li><div class="t">모집영상 촬영 총비용</div><div class="m">엑스트라 인당 15만원만 정해짐. 촬영 인력 인건비는 별도로 협의 필요</div></li>\n    <li><div class="t">다마고치 본편 5편의 회차별 구성</div><div class="m">기획 미확정</div></li>\n    <li><div class="t">광고 예산</div><div class="m">집행 구간(11/18~27)만 예시로 언급</div></li>\n    <li><div class="t">스스로 월백 채널의 소유 명의</div><div class="m">개설 주체가 회의에서 명시되지 않음 — <b>확인 필요</b></div></li>\n  </ul>\n</div>\n\n<div class="src">\n  근거 · 2026-11-04 플라우드 녹음 2건 병합 — "11-04 기획 회의: 유튜브 신규 채널 개설 및 다마고치 프로젝트 일정"(12:01~12:39, 38분, 164세그먼트)과 "[윤호PD님/민트님/루크님] 2차 회의"(12:41~12:50, 9분, 44세그먼트) 전문 ·\n  같은 제목의 "1차 회의" 녹음은 14초짜리 빈 파일이라 제외 ·\n  녹음의 화자 구분이 일부 섞여 있어 발언 귀속은 문맥으로 판단했습니다. 잘못 적힌 부분이 있으면 카톡방에 알려주세요 ·\n  날짜·요일은 2026년 11월 기준 대조(11/10 화 · 11/13 금 · 11/16 월 · 11/17 화 · 11/19 목) ·\n  엑스트라 인당 15만, 구성작가 편당 20~30만은 회의에서 나온 수치 그대로 ·\n  D-day의 시각(촬영 13시 등)은 회의에서 확정되지 않아 가정값이며 날짜만 회의 기준\n</div>\n</div>\n'

# ---------------------------------------------------------------- 회의록 허브
MEETHUB = '<div class="mtg">\n<div class="mnav"><a class="on" href="../meetings/">전체 회의록</a><a href="../min1030/">10/30 3자</a><a href="../min1104/">11/4 3자</a><a href="../min1111/">11/11 3자</a></div>\n\n<div class="hero">\n  <h1>회의록</h1>\n  <div class="sub">스스로 월백 / 다마고치 프로젝트 · 루크 · 민트 · 조윤호 PD</div>\n  <div class="goal">\n    <div><b>수 13시</b><span>정기 회의 (Zoom)</span></div>\n    <div><b>3건</b><span>기록된 회의록</span></div>\n  </div>\n</div>\n\n<h2>다음 정기 회의까지</h2>\n<div class="card">\n  <div class="ddrow"><div class="lab"><b>주간 정기 회의</b><span>매주 수요일 13시 · Zoom · 루크·민트·윤호 PD</span></div><span class="dday" data-due="2026-11-18T13:00:00+09:00"></span></div>\n  <div class="note">줌 무료 버전은 40분에서 끊깁니다. 11/4에도 한 번 끊겨 방을 다시 열었으니, 유료 전환이나 40분 단위로 안건을 끊는 진행을 고려하실 만합니다.</div>\n</div>\n\n<h2>기록된 회의</h2>\n\n<div class="card blue">\n  <div class="hd"><h3>11/11(수) · 3자 정기 회의</h3><span class="tm">13시 · 줌</span></div>\n  <p style="margin:8px 0 10px;font-size:14px">모집영상을 11/9(월) 청문회 콘셉트로 촬영한 뒤 처음 열린 회의입니다. 업로드·광고 날짜를 11/18로 잡고, 다음 주 수요일까지 각자 준비할 것을 나눴습니다.</p>\n  <ul class="list">\n    <li><div class="t">11/13(금) PD 편집·업로드 일정 공유 → 11/18 업로드·유튜브 광고</div></li>\n    <li><div class="t">다마고치 미팅·첫 촬영 11월 말~12월 초</div></li>\n    <li><div class="t">루크: 신규 유튜브 \'0원 다마고치\' · 카카오톡 채널 (다음 주 수요일까지)</div></li>\n    <li><div class="t">민트: 신청서 양식 · 신청자 CRM 관리안 (다음 주 초)</div></li>\n  </ul>\n  <p style="margin:10px 0 0"><a href="../min1111/"><b>11/11 회의록 전체 보기 →</b></a></p>\n</div>\n\n<div class="card">\n  <div class="hd"><h3>11/4(수) · 3자 정기 회의</h3><span class="tm">12:01~12:50 · 47분</span></div>\n  <p style="margin:8px 0 10px;font-size:14px">신규 채널 개설 여부를 가장 길게 다뤘고, 다마고치 인원을 3명에서 2명으로 줄였습니다. 모집영상 촬영일 1안을 11/10으로 잡았습니다.</p>\n  <ul class="list">\n    <li><div class="t">셀러들의 수다를 본진으로, 스스로 월백은 공동작업자로 연결</div></li>\n    <li><div class="t">다마고치 최대 2명 · 모집 시 인원 비공개</div></li>\n    <li><div class="t">촬영 1안 11/10(화) · 2안 11/16~17 · 11/13 불가</div></li>\n    <li><div class="t">구성작가 쓰지 않음 · 엑스트라 인당 15만</div></li>\n  </ul>\n  <p style="margin:10px 0 0"><a href="../min1104/"><b>11/4 회의록 전체 보기 →</b></a></p>\n</div>\n\n<div class="card accent">\n  <div class="hd"><h3>10/30(금) · 3자 기획 미팅</h3><span class="tm">약 112분</span></div>\n  <p style="margin:8px 0 10px;font-size:14px">브랜드와 포맷의 뼈대를 세운 자리입니다. 프로젝트명 \'스스로 월백 리턴즈\', 타깃 40대 초, 5화 구성, 상금 300만, 그리고 1화 압박 면접 콘셉트가 여기서 나왔습니다.</p>\n  <ul class="list">\n    <li><div class="t">1화 = 압박 면접 — 부업에 실패한 사람들이 멘토를 면접</div></li>\n    <li><div class="t">유튜브는 월 순수익 100만원까지만 공개 · 그 위는 강의</div></li>\n    <li><div class="t">상금 총 300만 · 매출 기준 · 광고비 일부를 전환</div></li>\n    <li><div class="t">정기회의 매주 수요일 13시 줌</div></li>\n  </ul>\n  <p style="margin:10px 0 0"><a href="../min1030/"><b>10/30 회의록 전체 보기 →</b></a></p>\n</div>\n\n<div class="src">\n  루크·민트·윤호 PD 3자 회의 녹음을 기준으로 정리했습니다. 빠진 내용이나 잘못 적힌 부분이 있으면 카톡방에 알려주세요.\n</div>\n</div>\n'

# ---------------------------------------------------------------- 10/30 3자 회의록
MIN1030 = '<div class="mtg">\n<div class="mnav"><a href="../meetings/">전체 회의록</a><a class="on" href="../min1030/">10/30 3자</a><a href="../min1104/">11/4 3자</a><a href="../min1111/">11/11 3자</a></div>\n\n<div class="hero">\n  <h1>10/30 회의록</h1>\n  <div class="sub">루크 · 민트 · 조윤호 PD · 2026-10-30(금) · 약 112분 · 스스로 월백 리턴즈 킥오프</div>\n  <div class="goal">\n    <div><b>스스로 월백 리턴즈</b><span>프로젝트명</span></div>\n    <div><b>40대 초</b><span>타깃</span></div>\n    <div><b>5화</b><span>에피소드</span></div>\n    <div><b>300만</b><span>상금 (매출 기준)</span></div>\n  </div>\n</div>\n\n<h2>마감까지 <small>실시간</small></h2>\n<div class="card">\n  <div class="ddrow"><div class="lab"><b>다마고치 모집·선정 완료</b><span>11월 말</span></div><span class="dday" data-due="2026-11-30T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>세일즈 라이브</b><span>1월 20일 · 설 전, 1월 넘기지 않기</span></div><span class="dday" data-due="2027-01-20T20:00:00+09:00"></span></div>\n  <div class="note">촬영·업로드 일정은 11/4 회의에서 다시 잡았습니다. <a href="../min1104/">11/4 회의록</a>을 함께 보십시오.</div>\n</div>\n\n<h2>각자 해야 할 일</h2>\n\n<div class="who pd">\n  <div class="hd2"><b>조윤호 PD</b><span>주말~다음 주 초</span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">다마고치 인원(1/2/3명)을 정하기 위한 촬영 여건·일정 체크 후 회신</div><div class="m">본인 외 촬영 인력 1~2명 확보 가능한지, 지인 출연 후보가 있는지 포함. "이 부분은 제가 조금 더 고민을 해가지고 말씀을 드릴게요"</div></li>\n    <li><div class="t">모집용 숏폼 스토리텔링 구상</div><div class="m">자료가 아무것도 없는 상태에서 무엇을 만들지. "제가 한번 스토리텔링을 좀 한번 해보겠습니다"</div></li>\n    <li><div class="t">기존 채널 2개 지표 확인</div><div class="m">죽은 채널인지 살릴 수 있는 채널인지 판단. 필요하면 테스트 영상 1편 올려 노출도 체크</div></li>\n    <li><div class="t">1화 세부 콘티·연출 구성</div><div class="m">면접 콘셉트, 컨퍼런스룸, 오프닝 샷</div></li>\n    <li><div class="t">채널 이름·방향성 안 공유</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="who mint">\n  <div class="hd2"><b>민트</b><span>즉시~모집 전</span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">기획안·일정표 공유</div><div class="m">회의 중 화면공유한 초기 채널 운영기획안</div></li>\n    <li><div class="t">면접 질문 1차 정리 후 공유</div><div class="m">"일단 일차적으로 한번 정리해서 같이 공유해드릴 테니까"</div></li>\n    <li><div class="t">퍼널 후단 전체 구상</div><div class="m">마케팅 페이지·DB 수집·CRM·알림톡. "후단은 제가 다 구상을 할 거고 콘텐츠 앞단은 같이 얘기하면서 잡아가면 될 것 같아요"</div></li>\n    <li><div class="t">에피소드 편수와 각 화 내용 채우기</div><div class="m">현재 의도적으로 빈칸. "편수에 들어갈 내용만 짜고 좀 빈칸으로 거의 다 뒀거든요"</div></li>\n    <li><div class="t">구글 광고 운영</div><div class="m">모집 단계</div></li>\n    <li><div class="t">과거 콘티 자료 PD께 전달</div><div class="m">개인캠 촬영 가이드용</div></li>\n    <li><div class="t">정기회의 세팅·단톡방 운영</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="who luke">\n  <div class="hd2"><b>루크</b><span>즉시</span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">PD·민트를 유튜브 채널 관리자로 추가</div><div class="m">1만명 채널 + 멘토루크 채널. "두 분 다 채널 관리자로 우선 넣어드릴까요?"</div></li>\n    <li><div class="t">채널 지표 화면 공유</div><div class="m">PD가 판단할 수 있도록 유튜브 스튜디오 화면 전달</div></li>\n    <li><div class="t">면접 콘텐츠용 질문 소재 정리</div><div class="m">수강생들이 실제로 가졌던 불만과 날카로운 질문. 민트 1차 정리본에 보강</div></li>\n    <li><div class="t">과거 사진·영상 자료 찾아보기</div><div class="m">기대치는 낮음 — "쿠팡에서 셀카를 찍어본 적도 없어요"</div></li>\n    <li><div class="t">과거 프로젝트 영상 사용 허락 가능 여부 판단</div><div class="m">4년 전 출연자 본인 동의가 필요. 루크 판단은 "반반"</div></li>\n  </ul>\n  </div>\n</div>\n\n<h2>퍼널 구조</h2>\n<div class="ig">\n<svg viewBox="0 0 400 128" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="유튜브에서 세일즈 라이브까지의 퍼널">\n  <rect x="6" y="34" width="68" height="40" rx="9" fill="none" stroke="#0ea5a4" stroke-width="1.5"/>\n  <text x="40" y="52" font-size="9.5" text-anchor="middle" fill="currentColor" font-weight="700">유튜브</text>\n  <text x="40" y="65" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">영상 5화</text>\n\n  <rect x="88" y="34" width="68" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="1.5"/>\n  <text x="122" y="48" font-size="9.5" text-anchor="middle" fill="currentColor" font-weight="700">무료자료</text>\n  <text x="122" y="60" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">카페에 게시</text>\n  <text x="122" y="70" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">질문·과제</text>\n\n  <rect x="170" y="34" width="68" height="40" rx="9" fill="none" stroke="#8b5cf6" stroke-width="1.5"/>\n  <text x="204" y="48" font-size="9.5" text-anchor="middle" fill="currentColor" font-weight="700">오픈채팅</text>\n  <text x="204" y="60" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">진입장벽 낮음</text>\n  <text x="204" y="70" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">30일 챌린지</text>\n\n  <rect x="252" y="34" width="68" height="40" rx="9" fill="none" stroke="#ec4899" stroke-width="1.5"/>\n  <text x="286" y="48" font-size="9.5" text-anchor="middle" fill="currentColor" font-weight="700">셀러들의</text>\n  <text x="286" y="59" font-size="9.5" text-anchor="middle" fill="currentColor" font-weight="700">수다</text>\n  <text x="286" y="70" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">비공개 VOD</text>\n\n  <rect x="334" y="34" width="60" height="40" rx="9" fill="#f59e0b" opacity=".18" stroke="#f59e0b" stroke-width="1.5"/>\n  <text x="364" y="52" font-size="9.5" text-anchor="middle" fill="currentColor" font-weight="700">라이브</text>\n  <text x="364" y="65" font-size="8" text-anchor="middle" fill="currentColor" opacity=".7">1/20</text>\n\n  <text x="81" y="57" font-size="11" text-anchor="middle" fill="currentColor" opacity=".45">›</text>\n  <text x="163" y="57" font-size="11" text-anchor="middle" fill="currentColor" opacity=".45">›</text>\n  <text x="245" y="57" font-size="11" text-anchor="middle" fill="currentColor" opacity=".45">›</text>\n  <text x="327" y="57" font-size="11" text-anchor="middle" fill="currentColor" opacity=".45">›</text>\n\n  <text x="200" y="18" font-size="9.5" text-anchor="middle" fill="currentColor" opacity=".8">유튜브는 월 순수익 100만원까지만 공개 · 그 위는 강의에서</text>\n  <text x="200" y="94" font-size="8.5" text-anchor="middle" fill="currentColor" opacity=".6">오픈채팅은 빠르지만 휘발성 · 셀러들의 수다는 락인되지만 설치가 어려움</text>\n  <text x="200" y="110" font-size="8.5" text-anchor="middle" fill="currentColor" opacity=".6">→ 우선 오픈채팅으로 모으고, 비공개 VOD·라이브 정보는 셀러들의 수다로 (확정 전)</text>\n  <text x="200" y="124" font-size="8" text-anchor="middle" fill="currentColor" opacity=".45">라이브는 영상을 본 상태를 전제로 진행 — 제로베이스 라이브와 분리</text>\n</svg>\n</div>\n\n<h2>결정 사항</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:32%">항목</th><th>결론</th></tr></thead>\n    <tbody>\n      <tr><td>프로젝트명</td><td><b>스스로 월백 리턴즈</b> — 4년 전 \'스스로 월백\'의 컴백</td></tr>\n      <tr><td>포맷</td><td><b>다마고치 에피소드형 교육 콘텐츠</b> (순수 다큐·관찰 다큐 배제)</td></tr>\n      <tr><td>에피소드</td><td><b>5화</b> (과거 10화 이상·4개월 호흡은 폐기)</td></tr>\n      <tr><td>다마고치 선발</td><td>기존 제자 재활용 없이 <b>무에서 신규 공개모집</b></td></tr>\n      <tr><td>타깃</td><td><b>40대, 핵심은 40대 초</b> · 5060 주 타깃 제외 · DB 보며 수정</td></tr>\n      <tr><td>페르소나</td><td><b>연령이 아니라 상황.</b> 멘티가 40대일 필요 없음</td></tr>\n      <tr><td>메시지</td><td>"쉽고 빠르게 돈 버는 건 없다 / 따라오면 되게 해준다" · 혼내는 멘토</td></tr>\n      <tr><td>공개 범위</td><td>유튜브 = 도매 사이트만으로 <b>월 순수익 100만원</b>까지 / 강의 = 마진액·ECR</td></tr>\n      <tr><td>1화</td><td><b>압박 면접</b> — 멘토가 피면접자. 면접관은 \'부업에 실패하고 불신을 가진 사람들\'</td></tr>\n      <tr><td>1화 규모</td><td>면접관 <b>8명</b>(배우 섭외) · <b>카메라 3~4대</b> · 외부 컨퍼런스룸 · 제작비 <b>약 100만원</b></td></tr>\n      <tr><td>1화 구성</td><td>하이라이트 → 맥락 10~20초(검정화면+자막) → 본 면접 5분(최대 8분) → 모집 CTA</td></tr>\n      <tr><td>광고 영상</td><td>본편과 <b>분리</b>. 1분 안에 목적 달성 · 5분 이내 · 일부공개로 운용</td></tr>\n      <tr><td>챌린지</td><td><b>30일</b>(100일 폐기) · 출연자뿐 아니라 <b>영상 시청자 전원</b> 참여 가능</td></tr>\n      <tr><td>상금</td><td><b>총 300만원</b> · <b>매출 기준</b>(순익은 검증 불가) · 영상 유입 광고비 일부를 전환</td></tr>\n      <tr><td>광고 매체</td><td><b>구글 중심</b> · 메타는 CPA 악화·계정 정지로 배제</td></tr>\n      <tr><td>일정</td><td>11월 시작 · 모집영상 11월 중순 공개 · 모집 2주 · 12월부터 본편 업로드 · <b>라이브 1/20</b></td></tr>\n      <tr><td>촬영 리듬</td><td><b>주 1회 오프라인</b> + 온라인 멘토링 주 1~2회(화면·얼굴 각각 녹화)</td></tr>\n      <tr><td>정기회의</td><td><b>매주 수요일 오후 1시 줌</b> · 비정기는 단톡방 + 필요시 즉석 줌</td></tr>\n      <tr><td>역할</td><td>퍼널·마케팅 페이지 후단 = <b>민트 단독</b> / 콘텐츠 앞단 = <b>3인 공동</b></td></tr>\n      <tr><td>제작진 노출</td><td>1기에는 <b>영상 비출연</b>. 카페 사업일지·챌린지 참여로만</td></tr>\n      <tr><td>1기 목표</td><td><b>루크 인지도 구축에 집중.</b> 서바이벌·다인 확장은 차기</td></tr>\n      <tr><td>채널명 방향</td><td><b>\'스스로 월백\'</b> 쪽 · \'셀러\' 배제 · \'부업/돈\'은 경쟁 과다로 배제</td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<h2>상세 회의록</h2>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">1. 왜 다마고치인가 — 기획 방향</h3>\n  <p style="margin:0 0 10px">민트가 안건을 열었습니다. 4년 전 루크와 함께 \'스스로 월백\'이라는 프로젝트를 유튜브에서 다마고치 에피소드 형식으로 했고, 이번에 채널을 열면서 첫 콘텐츠로 그걸 지금 시기에 맞게 되살리자는 것입니다. 11월부터 시작하는 전제로 초기 채널 운영기획안을 짜 와 화면 공유로 진행했습니다.</p>\n  <div class="warn"><b>순수 다큐 포맷을 배제한 이유.</b> 민트: "카테고리를 전체 다 다루시니까 실제로 들어오신 분들이 <b>그래서 어떤 걸 판다는 건지, 어떤 식으로 한다는 건지 이해를 못 하시기 때문에 결제 전환률이 낮다</b>고 생각했다. 차라리 직접적인 교육 영상 에피소드를 스토리 형식으로 넣어보자."</div>\n  <ul class="list">\n    <li><div class="t">1화 후보 세 가지가 올라왔습니다</div><div class="m">① 4년 전 멘티를 모셔 함께 보는 관찰형 — 본인이 유튜브 출연을 원하지 않아 사실상 제외 ② <b>멘토 역면접형</b> — 다마고치를 뽑는 게 아니라 멘토를 면접 ③ 처음부터 광고 영상. ②와 ③은 포맷이 겹쳐 하루에 함께 촬영 가능</div></li>\n    <li><div class="t">과거 프로젝트는 광고 없이 영상당 조회수 10만 회가 기본이었음</div><div class="m">다만 4개월 호흡에 영상 10개가 넘는 롱폼 구조. 지금은 숏폼 수요가 커지고 인내심이 줄어 <b>5화로 압축</b></div></li>\n    <li><div class="t">기존 제자를 다시 가르치는 방식은 배제</div><div class="m">"이 사람은 원래 제자 중에 한 명"이라는 박탈감 때문에 공감대를 얻기 힘들다는 판단</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">2. 퍼널과 커뮤니티</h3>\n  <p style="margin:0 0 10px">유튜브의 목적은 브랜딩·마케팅이고 결국 DB를 모아야 하므로, 영상을 본 사람에게 자료를 무료로 풀되 그 자료는 카페에 게시해 카페 유입을 만들고 거기서 질문과 과제가 돌게 하는 구조입니다. 챌린지는 출연자뿐 아니라 영상만 보고도 따라할 수 있는 형태로 설계합니다.</p>\n  <ul class="list">\n    <li><div class="t">오픈채팅방 vs 셀러들의 수다</div><div class="m">오픈채팅은 진입장벽이 아주 낮아 빠르게 모이지만 휘발성이 강하고 CRM을 뿌릴 정보가 안 남습니다. 셀러들의 수다는 로그인을 받아 DB가 쌓이고 알림톡·과제·매출·접속 트래킹까지 되는 확실한 락인이지만, <b>민트가 직접 받아보니 설치가 복잡해 어르신들이 다운로드를 잘 못 한다</b>는 문제가 있었습니다</div></li>\n    <li><div class="t">중간안</div><div class="m">처음엔 오픈채팅방으로 전부 몰고, <b>비공개 VOD·라이브 정보는 셀러들의 수다로</b> 넘기는 2단 구조. 퍼널을 한 번 더 거치니 이탈은 크겠지만 자료 아카이빙과 개별 질문이 가능합니다 — <b>확정 전</b></div></li>\n    <li><div class="t">챌린지는 100일에서 30일로</div><div class="m">11월 촬영 시작이면 12월부터 파일이 올라가는데 연말·연초 "새로운 시작" 동기부여와 맞물립니다</div></li>\n    <li><div class="t">광고비는 두 지점</div><div class="m">① 다마고치 모집 때 잠재고객 대상 ② 반응 좋은 영상을 돌려 시청 증폭</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">3. 타깃 — 40대 초로 좁힘</h3>\n  <p style="margin:0 0 10px">PD가 먼저 물었습니다. 기존 플랫폼 강의의 주 타깃은 사실상 시니어였는데 이번에도 같은 층으로 갈 것인지, 실행력이 더 좋은 층으로 갈 것인지. 다마고치 멘티의 연령대가 시청자의 "나도 할 수 있겠다"를 결정할 것 같다는 판단이었습니다.</p>\n  <div class="warn"><b>민트:</b> "제일 좋은 타겟은 40대. 더 좁히면 40대 초다. 그때 되면 <b>지출은 많은데 수입이 한계점에 부딪히는 시점</b>이 딱 온다. 이 삶을 어떻게 뒤바꿀 수 있을지 모르겠다고 정체되는 게 40대 초다."</div>\n  <ul class="list">\n    <li><div class="t">루크도 동의</div><div class="m">"50대·60대 분들은 너무 포기가 빠르기도 하고, 의외로 참여도가 관망하는 관중 느낌이 많다. 저도 가능하면 40대가 맞지 않을까 싶다." 일단 40대로 돌려보고 들어오는 DB를 보며 수정하기로</div></li>\n    <li><div class="t">페르소나는 연령이 아니라 상황</div><div class="m">민트의 전환: 사람들은 페르소나가 같은 사람이 아니라 <b>스토리가 있는 사람</b>에게 이입한다. 4050이 많이 듣는다고 그 연령을 주인공으로 삼았을 때 항상 터지지는 않았고, 극적으로 변할 실행력·동기가 있는 사람을 보여주면 시청자가 자기 아들이나 남편을 떠올린다. PD도 "꼭 그 역할이 나랑 같은 상황이 아니더라도 계속 이입하고 보면서 동화가 되는 것"이라고 동의</div></li>\n    <li><div class="t">시장 인식 — PD</div><div class="m">"다큐·인터뷰 채널 시장도 포화됐고, 결국 찾아오는 사람들은 짧은 시간에 쉽게 돈 버는 방법을 찾는다. 자동화로 누구나 쉽게가 셀링 포인트가 계속 되니까"</div></li>\n    <li><div class="t">그런데 이 프로젝트는 반대로 간다 — 민트</div><div class="m">"제가 이 프로젝트로 추구하는 바는 <b>그런 건 없다</b>예요. 재정 문제를 돌파하려면 따라와라, 따라오면 무조건 되게 해줄게, 대신 쉽지 않을 거다." 라이브에서 사람들은 절대 혼나지 않지만, 멘토니까 <b>잘못했다고 말하고 혼내는</b> 모습을 에피소드 포인트로</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">4. 출연 인원과 상금 — 이 회의의 분기점</h3>\n  <p style="margin:0 0 10px"><b>민트는 1명</b>을 주장했습니다. 많아지면 시선이 분산되고 몰입이 안 되니 다마고치는 한 명으로 두고 주변 인물을 늘리는 방식이 낫다는 것. 리스크로 ① 동시 진행 시 시선 분산 ② 3명으로 시작했는데 중간 이탈하면 콘텐츠가 애매해지는 점을 들었습니다.</p>\n  <p style="margin:0 0 10px"><b>PD는 여러 명</b>을 밀었습니다. 경쟁을 시킬 수 있고 콘텐츠 거리와 갈등이 생기며, 이야기의 재미는 갈등과 해소에 있다는 것. 한 명이 이탈해도 그 자체가 에피소드가 되고 돌아오는 이야기도 가능하니 완전한 리얼리티보다 약간의 연출이 필요한 영역이라고 봤습니다.</p>\n  <div class="warn"><b>PD의 근본 논리:</b> "<b>스마트스토어는 자극적으로 보여줄 게 없는 아이템</b>이다. 대표님 능력 하나로 하루 만에 천만 원, 이런 게 가능한 시장이 아니니 사람 이야기 안에서, 당근과 채찍으로 사람이 변하는 서사로 만들어야 한다."</div>\n  <ul class="list">\n    <li><div class="t">루크의 제안 — 광고비 일부를 상금으로</div><div class="m">"과거 채널은 기존 풀이 있고 후기가 쌓여 궁금증이 있었지만, 지금은 신규 채널에 광고로 사람을 뽑는 상황이라 후킹이 약한 게 사실이다. <b>광고비로 쓰려던 일부를 상금으로 걸자.</b>" 구체안: ① 매주 숙제 1등에게 소액 ② 최종 매출 1등 300만원 ③ 챌린지 참여자(비출연자) 1등 100만원 + 출연<br><b>"이런 류의 다마고치를 비슷하게 하신 분들은 있지만 실제로 상금을 걸어서 해본 적은 없으실 것 같다"</b></div></li>\n    <li><div class="t">PD 동의</div><div class="m">중간 챌린지·숙제에 소정의 상금이 있으면 당장 매출이 없어도 들어오는 돈이 있어 더 열심히 할 수 있다</div></li>\n    <li><div class="t">민트가 받으며 기준 제기</div><div class="m">3명 동시 진행 시 총 상금 300만원, 매출 1등에게. 다만 "매출은 낮은데 순익은 더 높을 수도 있는데 그걸 다 알 수는 없으니" <b>일단 매출 기준</b>으로</div></li>\n    <li><div class="t">과거에 3명을 못 한 이유</div><div class="m">제작팀이 없고 PD 한 분뿐이라 담을 수 없었던 것. <b>제작 여건이 되면 3명도 충분히 가능</b>하다는 게 민트의 정리</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">5. 촬영 여건 — 인원 결정의 실질 변수</h3>\n  <ul class="list">\n    <li><div class="t">PD의 부담</div><div class="m">"캠을 다 각각 따야 되고 편집할 때 복잡하다." 다만 여건이 되면 주변에서 카메라 들고 찍는 걸 좋아하는 사람을 <b>본인 외 1~2명</b> 붙일 수 있고, 공간이 좁으면 별도 공간을 만들어서라도 캠을 늘릴 수 있다고 함. 그들도 생업이 있어 일정 확보 체크 필요</div></li>\n    <li><div class="t">과거 운영 방식 — 루크</div><div class="m">온라인 멘토링 <b>주 1~2회</b>, 촬영은 매주 토요일 멘티가 올라와 진행, 주중 멘토링은 전화·화상으로 하고 녹화를 따로 떴음. <b>기본 원칙은 주 1회 촬영</b></div></li>\n    <li><div class="t">온라인 멘토링 녹화만으로 올라간 프로젝트도 있었음</div><div class="m">화면 녹화 + 멘티가 핸드폰으로 본인 얼굴 따로 녹화, OBS로 컷 전환. 이질감도 없었음. 다만 3명이면 화면을 계속 교체해야 하는 부담</div></li>\n    <li><div class="t">루크의 정리 — 공을 PD에게</div><div class="m">"내용이 감당되시면 저희가 기획을 할 것이고, <b>로드가 걸리실 것 같으면 안전하게 한 명으로</b> 가되 부족한 그림은 요소로 채우는 게 맞다. 되실 것 같으면 3명도 2명도 좋다"</div></li>\n    <li><div class="t">PD의 욕심</div><div class="m">"멘티들의 생업하는 모습까지 다 찍어 몰입을 만들고, 고충과 그만두고 싶어하는 상황을 밀착해 보여주고 싶다. <b>부업에 관심 없는 사람도 \'이 이야기 재밌다\'로 시작할 수 있는 콘텐츠</b>가 되면 좋겠다." 유일한 고민은 "짜놓은 로드맵과 시간 안에 머릿속 그림을 다 담을 수 있는가"</div></li>\n    <li><div class="t">2명 타협안</div><div class="m">민트: 한 명은 PD 지인, 한 명은 공개모집으로 하면 품이 덜 들고 화면도 다양해지며 경쟁 구조와 서로 다른 페르소나가 가능. 3명은 화면이 산만할 수 있지만 2명은 깔끔하고 캠·조명도 적게 듦. PD도 확실히 덜 든다고 인정</div></li>\n  </ul>\n  <div class="note">촬영 협조 능력이 선발 기준에 들어갔습니다. 개인캠으로 찍어야 하는 컷(집에서의 역할, 혼잣말하며 산책, 감정 변화)이 많고, 콘티를 주면 제대로 찍어 보내줘야 하며 감정이 안 실리면 될 때까지 재요청합니다. 과거 멘티도 5·6·7번씩 다시 받았습니다.</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">6. 채널 — 신규냐 기존이냐</h3>\n  <p style="margin:0 0 10px">루크가 보유 자산을 공개했습니다. 하나는 <b>구매한 1만명 채널</b>(원래 시니어 대상 동기부여·명언 주제), 하나는 <b>멘토루크 약 300명</b>. 둘 다 크게 활성화돼 있지는 않습니다.</p>\n  <ul class="list">\n    <li><div class="t">PD — 신규 채널의 구조적 어려움</div><div class="m">"알고리즘 형성에 시간이 필요하고 <b>첫 영상이 빵 터지는 경우는 사실상 없다.</b> 딱 하나 있다면 광고다." 콘텐츠는 노출 → 클릭률 전환 → 지속 시청 → 추가 노출 구조라 첫 편 고민이 큼</div></li>\n    <li><div class="t">민트 — 신규도 세팅이 필요</div><div class="m">"신규채널을 만들면 알고리즘을 처음에 설정해줘야 한다. 3~4일 정도는 계속 관련 콘텐츠를 보고 홈화면이 부업·스마트스토어로 세팅돼야 뿌려질 것. <b>진짜 일장일단이 있다</b>"</div></li>\n    <li><div class="t">PD — 먼저 지표를 봐야</div><div class="m">기존 채널이 <b>죽은 채널인지 살릴 수 있는 채널인지</b> 확인이 필요. "1만명인데 노출이 50, 100이면 애매해져 버린다." 유튜브 스튜디오 화면을 받으면 판단이 쉽다고 요청 → 루크가 두 사람을 채널 관리자로 넣기로</div></li>\n    <li><div class="t">민트의 대안 — 공동 게시</div><div class="m">새 채널을 하나 만들고 기존 2개 채널을 포함해 영상을 <b>공동 작업자로 동시 업로드</b>해, 실제 유입과 어느 채널이 알고리즘을 타는지 보고 판별하자는 안</div></li>\n    <li><div class="t">광고 매체</div><div class="m">구글 중심. <b>메타는 요즘 CPA가 너무 안 좋고 정지도 많다</b>는 민트 의견으로 사실상 배제</div></li>\n    <li><div class="t">채널명</div><div class="m">민트: "<b>\'셀러\'라는 말은 웬만하면 다 빼고 싶고, \'부업\'·\'돈\'은 경쟁 채널이 너무 많아 밀릴 것</b>." 그냥 \'스스로 월백\'으로. 루크도 명확해서 좋다고 동의</div></li>\n  </ul>\n  <div class="note">※ 이 안건은 11/4 회의에서 <b>셀러들의 수다를 본진으로, 스스로 월백을 공동작업자로 연결</b>하는 것으로 결론났습니다.</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">7. 1화 — 압박 면접 콘텐츠</h3>\n  <p style="margin:0 0 10px">과거 자료 기반 비포애프터가 불가능하다고 정리된 직후, PD가 "아니면 그냥 면접 콘텐츠 하시죠?"로 들어가 이 회의의 최대 산출물이 나왔습니다.</p>\n  <ul class="list">\n    <li><div class="t">내용축 — 의구심을 미리 까기</div><div class="m">민트: "그걸로 돈 잘 벌면서 굳이 왜 다마고치를 하고 왜 알려준다고 하나, 더 쉬운 사업이 많다는데 어떻게 생각하나 — <b>사람들이 댓글로 남길 법한 걸 미리 그냥 까버리는 거죠</b>"</div></li>\n    <li><div class="t">PD의 그림</div><div class="m">정장 입은 루크를 멀리서부터 찍어 들어와 인사받고, 면접인데 "월 얼마 버세요?" 같은 질문부터 시작하는 <b>압박 면접의 역구성</b>. 1화에는 멘티가 없으니 루크 이야기를 재밌게 풀 수 있는 장치</div></li>\n    <li><div class="t">민트의 결정적 명분 — 면접관이 누구인가</div><div class="m"><b>"부업을 하다가 그만뒀던 사람들을 초대한다."</b> "감히 내가 해봤는데 안 되는데, 감히 다시 나한테 부업을 하라고 시킨다고?"로 <b>책임을 묻는</b> 자리이고, 루크가 "내가 한 명은 완전히 되게 만든다는 걸 보여주겠다"로 받는 구조. 단 <b>실제 그런 사람이 오면 안 되고 배우를 섭외</b>, 질문은 제작진이 설계</div></li>\n    <li><div class="t">수위를 올려가는 대사 설계</div><div class="m">"왜 당신에게 다마고치를 받아야 하는가" → 사무실을 보여주면 "그럼 꼭 물건을 사야 돈을 버는 거네요, 자본금이 많이 들겠네요?" → 루크 "월 100까지는 자본금 없이 가능한 방법을 만들었고 알려줄 것" → "그러면 위탁이라 번거롭고 요즘 잘 안 하는데 그게 돈이 되냐?"</div></li>\n    <li><div class="t">루크의 디펜스 소재</div><div class="m">"하루 한 시간도 안 한 사람이 진짜 많다. 사업자등록증을 내라고 했더니 안 내는 분들이 너무 많다" → 민트 "그러면 <b>사업자등록증 내는 날을 라이브로</b> 하죠"로 챌린지 명분까지 연결</div></li>\n    <li><div class="t">오프닝</div><div class="m">텅 빈 컨퍼런스룸, 복도를 걸어 들어오는 부감 샷, "여기 맞아요?" 하는데 가운데 의자 하나. 앉으면 책상들이 옮겨져 둘러싸고 "이제부터 면접 진행하겠습니다" → <b>8명이 동시에 종이를 구겨 던지며 "해명해보세요"</b>. 이 장면을 하이라이트와 썸네일로</div></li>\n    <li><div class="t">마무리</div><div class="m">티키타카가 쌓이다 터지면서 <b>"내가 저거 하겠다"</b> 선언 → "나한테 불신 있는 사람 다 와, 내가 다 알려줄게" → "오늘부터 몇월 몇일까지 신청하세요" 모집 CTA</div></li>\n    <li><div class="t">장소</div><div class="m">사무실 배제 — 자주 보여줄 공간이고 면접 분위기가 안 나며 "공장 느낌"에 찬장이 들어와 개방감이 없음. <b>뜬금없이 넓은 컨퍼런스룸</b>에 루크 혼자 가운데</div></li>\n  </ul>\n  <div class="warn"><b>PD의 평가:</b> "세부 콘티는 짜봐야겠지만 <b>컨셉만으로도 오늘 나온 게 큰 승산</b>이네요." 일반인이 봐도 재밌고 부업에 관심 없던 사람도 함께 볼 수 있는 콘텐츠가 될 것 같다고.<br><b>민트:</b> "이건 광고를 돌려도 괜찮을 것 같아요."</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">8. 과거 자료 — 쓸 게 없다</h3>\n  <p style="margin:0 0 10px">PD가 루크의 스마트스토어 시작 전후 영상·사진 자료를 물었습니다. 민트가 먼저 "영상은 없을 것이고 사진도 거의 없다, <b>4년 전에도 없었다</b>"며 숏폼 비포애프터가 안 나온다고 답했습니다.</p>\n  <div class="note">루크: "저는 쿠팡에서 셀카를 한 번도 찍어본 적이 없어요. 그냥 제 일하기만 봤어서." 다른 분들은 찍는데 본인은 정말 먹고 살기만 봤기 때문에 첫 영상이 어려울 수도 있다고 인정. 그래도 한번 찾아보기로.<br><b>민트의 대체 논리:</b> "최근에 <b>강의업계에 대한 불신이라는 공감대</b>가 이미 형성돼 있다. 과거 자료가 없어도 현 시점 공감대만으로 콘텐츠가 충분히 나온다." → 7번 면접 콘텐츠로 연결</div>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">9. 모집 일정과 운영</h3>\n  <ul class="list">\n    <li><div class="t">모집영상</div><div class="m"><b>11월 중순 공개, 모집 2주</b>(최소 1주). 과거엔 일주일만 모집해도 많이 들어왔지만 그땐 구독자가 있었고 이번은 신규라 시간이 더 필요</div></li>\n    <li><div class="t">숏폼</div><div class="m">광고가 많이 필요해지는 만큼 숏폼을 여러 개 만들어야 함. PD가 소재 스토리텔링을 맡기로</div></li>\n    <li><div class="t">과거 콘텐츠 재활용</div><div class="m">\'리턴즈\'라는 이름을 붙인 이유가 여기 있음 — 4년 전 영상을 "예전에 이렇게 진행했는데 이번에 새로 모집한다"는 식으로 쓸 수 있음. <b>단 출연자 본인 허락이 필요하고, 원하지 않을 수 있음</b></div></li>\n    <li><div class="t">정기회의</div><div class="m"><b>매주 수요일 오후 1시 줌</b>으로 고정. 비정기는 단톡방, 필요하면 그때그때 줌</div></li>\n    <li><div class="t">편수와 각 화 내용은 의도적으로 빈칸</div><div class="m">민트: "일부러 편수에 들어갈 내용만 짜고 거의 다 빈칸으로 뒀다" — 셋이 함께 채울 영역</div></li>\n  </ul>\n</div>\n\n<div class="card">\n  <h3 style="margin:0 0 8px">10. 뒤로 미룬 아이디어</h3>\n  <ul class="list">\n    <li><div class="t">서바이벌 확장 (PD)</div><div class="m">다마고치가 커진 뒤 여러 명을 한 번에 봐주며 서바이벌 예능 느낌으로. 월 순수익이 가장 좋은 사람에게 보상하며 갈등을 만드는 구조</div></li>\n    <li><div class="t">패자부활전 (민트)</div><div class="m">중간에 그만둔 사람 중 사연 있는 사람을 신청받아 후발주자로 다시 뽑고, 1차가 끝난 뒤 실제로 따라했던 사람들 이야기로 재점화</div></li>\n    <li><div class="t">2기가 진짜 (민트)</div><div class="m">"1차는 아카이빙·레퍼런스 쌓기고 <b>진짜는 두 번째</b>다. 2차 다마고치 발표를 라이브에서 하고, 거기 들어온 사람 중 바로 배우고 싶다는 사람에게는 강의 수강 혜택을"</div></li>\n    <li><div class="t">같은 포맷으로 다음 멘토 (민트)</div><div class="m">"멘토 지원하기" 링크를 걸어 강사를 모집하는 창구로. 전 멘토들과 함께 2~3명이 압박 면접을 보는 그림</div></li>\n    <li><div class="t">제작진 출연</div><div class="m">1기에는 영상에 넣지 않고 카페 사업일지로만. 제작팀이 제3자로서 시청자 입장을 대변하는 창구 역할. 영상화는 후속으로</div></li>\n  </ul>\n  <div class="note">PD의 정리: "1기는 어쨌든 대표를 알리는 목적이므로 서바이벌 같은 큰 프로젝트는 뒤로 미루고 <b>집중할 수 있는 부분부터 시작하는 게 가장 좋은 방향</b>." 민트도 동의.</div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">정해지지 않은 것</h3>\n  <ul class="list">\n    <li><div class="t">다마고치 인원 — 1명 / 2명 / 3명</div><div class="m">PD가 촬영 여건·일정 체크 후 회신하기로. <b>11/4 회의에서 최대 2명으로 확정</b></div></li>\n    <li><div class="t">상금 세부 설계</div><div class="m">매주 숙제 1등 소액 / 최종 매출 1등 300만 / 챌린지 참여자 1등 100만 중 무엇을 쓸지, 총 300만의 분배 방식</div></li>\n    <li><div class="t">평가 기준</div><div class="m">매출 vs 순익 — "일단 매출 기준"으로 잠정 처리</div></li>\n    <li><div class="t">채널 선택</div><div class="m">신규 / 1만명 / 멘토루크 / 공동 게시 — <b>11/4 회의에서 결론</b></div></li>\n    <li><div class="t">DB 수집 수단</div><div class="m">오픈채팅만 / 셀러들의 수다 / 문자 CRM / 2단 구조</div></li>\n    <li><div class="t">에피소드 편수와 각 화 내용</div><div class="m">대부분 빈칸</div></li>\n    <li><div class="t">온라인 멘토링 녹화를 영상에 포함할지</div><div class="m">PD 로드 우려로 결론 없이 "그때 가서 정해도 된다"</div></li>\n    <li><div class="t">1화 촬영 장소</div><div class="m">컨퍼런스룸 등 공간 섭외 미정</div></li>\n    <li><div class="t">강의업계 비판 소재를 1화에 쓸지</div><div class="m">"뒷일을 또 모르기 때문에 그렇게 시작할 필요는 없다"며 아껴두는 쪽으로 기울었으나 결론 없음</div></li>\n    <li><div class="t">과거 프로젝트 영상 사용 허락</div><div class="m">출연자 본인 의사 확인 필요. 루크 판단 "반반"</div></li>\n    <li><div class="t">카카오톡 파트너센터 1:1 채팅 활용</div><div class="m">PD가 물었고 답이 이어지지 않음</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  2026-10-30 3자 미팅 녹음(약 112분) 전문 583세그먼트를 모두 읽고 정리했습니다 ·\n  세 사람이 함께 있었던 구간(PD 합류 이후 ~ 퇴장 전)만 담았고, 그 앞뒤의 개별 대화는 제외했습니다 ·\n  녹음의 화자 구분이 일부 섞여 있어 발언 귀속은 문맥으로 판단했습니다 ·\n  일부 고유명사와 숫자는 전사가 불명확해 확인된 것만 적었습니다 ·\n  빠진 내용이나 잘못 적힌 부분이 있으면 카톡방에 알려주세요\n</div>\n</div>\n'

MIN1111 = '<div class="mtg">\n<div class="mnav"><a href="../meetings/">전체 회의록</a><a href="../min1030/">10/30 3자</a><a href="../min1104/">11/4 3자</a><a class="on" href="../min1111/">11/11 3자</a></div>\n\n<div class="hero">\n  <h1>11/11 회의록</h1>\n  <div class="sub">윤호 PD · 민트 · 루크 · 2026-11-11(수) 13시 · 줌 정기 회의 · 스스로 월백 / 다마고치</div>\n  <div class="goal">\n    <div><b>11/9 완료</b><span>모집영상 촬영 (청문회 콘셉트)</span></div>\n    <div><b>11/18(수)</b><span>업로드 · 유튜브 광고 집행</span></div>\n    <div><b>11월 말~12월 초</b><span>다마고치 미팅 · 첫 촬영</span></div>\n    <div><b>1/20</b><span>세일즈 라이브</span></div>\n  </div>\n</div>\n\n<h2>지난 회의 이후</h2>\n<div class="card blue">\n  <p style="margin:0"><b>모집영상은 11/9(월)에 청문회·압박면접 콘셉트로 촬영을 마쳤습니다.</b> 11/4 회의에서 1안으로 잡았던 11/10(화)보다 하루 앞당겨 진행됐습니다. 이번 회의는 편집·업로드 이후 일정과 각자 준비할 것을 정했습니다.</p>\n</div>\n\n<h2>마감까지 <small>실시간</small></h2>\n<div class="card">\n  <div class="ddrow"><div class="lab"><b>편집 일정·업로드 일정 공유</b><span>11/13(금) · 윤호 PD</span></div><span class="dday" data-due="2026-11-13T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>다마고치 신청서 양식 · 신청자 CRM 관리안 공유</b><span>다음 주 초 · 민트</span></div><span class="dday" data-due="2026-11-17T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>신규 유튜브 채널 \'0원 다마고치\' 개설</b><span>다음 주 수요일까지 · 루크</span></div><span class="dday" data-due="2026-11-18T13:00:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>카카오톡 채널(플러스친구) 공유 또는 신규 개설</b><span>다음 주 수요일까지 · 루크</span></div><span class="dday" data-due="2026-11-18T13:00:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>모집영상 업로드 · 유튜브 광고 집행</b><span>11/18 목표</span></div><span class="dday" data-due="2026-11-18T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>다마고치 미팅 · 첫 촬영</b><span>11월 말~12월 초 목표</span></div><span class="dday" data-due="2026-12-04T23:59:00+09:00"></span></div>\n  <div class="ddrow"><div class="lab"><b>세일즈 라이브</b><span>2027-01-20</span></div><span class="dday" data-due="2027-01-20T20:00:00+09:00"></span></div>\n  <div class="note">한국 시간 기준으로 1초마다 다시 계산됩니다. \'다음 주 수요일까지\'는 11/18 정기 회의 시작(13시), \'11월 말~12월 초\'는 12/4(금), 라이브 시각은 20시로 가정한 값입니다. 날짜는 회의 기준입니다.</div>\n</div>\n\n<h2>결정 사항</h2>\n<div class="card">\n  <div class="wrapx">\n  <table>\n    <thead><tr><th style="width:36%">안건</th><th>결론</th></tr></thead>\n    <tbody>\n      <tr><td>편집·업로드 일정</td><td>윤호 PD가 <b>11/13(금)</b>에 편집 일정과 업로드 일정을 공유</td></tr>\n      <tr><td>모집영상 업로드</td><td><b>11/18 업로드 및 유튜브 광고 집행</b>을 목표로 함</td></tr>\n      <tr><td>다마고치 일정</td><td>다마고치 미팅과 첫 촬영은 <b>11월 말~12월 초</b> 목표</td></tr>\n      <tr><td>신규 유튜브 채널</td><td><b>\'0원 다마고치\'</b> 채널을 새로 개설 — 루크, 다음 주 수요일까지</td></tr>\n      <tr><td>카카오톡 채널</td><td>기존 플러스친구가 있으면 공유, 없으면 신규 개설 — 루크, 다음 주 수요일까지</td></tr>\n      <tr><td>신청서 · CRM</td><td>다마고치 신청서 양식과 신청자 CRM 관리 방법은 민트가 정리해 다음 주 초 공유</td></tr>\n      <tr><td>정산 관련 2건</td><td>윤호 PD 수익 배분과 제작경비 입금 방식은 11/11 카톡방 공지로 확정 — <b>세부 내용은 카톡방 공지를 기준으로</b> 하고 이 페이지에는 싣지 않습니다</td></tr>\n    </tbody>\n  </table>\n  </div>\n</div>\n\n<h2>각자 해야 할 일</h2>\n\n<div class="who pd">\n  <div class="hd2"><b>조윤호 PD</b><span class="dday" data-due="2026-11-13T23:59:00+09:00"></span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">편집 일정 · 업로드 일정 공유 — 11/13(금)</div><div class="m">11/18 업로드 목표에 맞춘 일정</div></li>\n    <li><div class="t">모집영상 편집</div><div class="m">11/9 촬영분. 업로드와 유튜브 광고 집행은 11/18 목표</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="who mint">\n  <div class="hd2"><b>민트</b><span class="dday" data-due="2026-11-17T23:59:00+09:00"></span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">다마고치 신청서 양식 정리 — 다음 주 초</div><div class="m">"신청서 양식, 신청한 사람 CRM 관리 어떻게 할지 고민해서 담주초에 공유드릴게요"</div></li>\n    <li><div class="t">신청자 CRM 관리 방법 정리 — 다음 주 초</div><div class="m">신청서와 함께 공유</div></li>\n    <li><div class="t">11/18 유튜브 광고 집행</div><div class="m">업로드와 같은 날 목표</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="who luke">\n  <div class="hd2"><b>루크</b><span class="dday" data-due="2026-11-18T13:00:00+09:00"></span></div>\n  <div class="bd">\n  <ul class="list">\n    <li><div class="t">신규 유튜브 채널 개설 — \'0원 다마고치\'</div><div class="m">다음 주 수요일(11/18)까지. 만들면 채널 주소를 카톡방에 공유하고 민트·윤호 PD를 채널 권한에 초대</div></li>\n    <li><div class="t">카카오톡 채널(플러스친구) 개설 또는 공유</div><div class="m">기존 채널이 있으면 그 채널을 공유, 없으면 신규 개설 — 다음 주 수요일까지</div></li>\n    <li><div class="t">회의 공지 확인</div><div class="m">카톡방 공지 3건에 \'확인\' 답글 완료(11/11 19:03)</div></li>\n  </ul>\n  </div>\n</div>\n\n<div class="card red">\n  <h3 style="margin:0 0 8px">아직 정해지지 않은 것</h3>\n  <ul class="list">\n    <li><div class="t">상금 300만의 분배 방식</div><div class="m">10/30에 총 300만·매출 기준까지만 정해짐. 신청서 양식에 들어갈 수 있음</div></li>\n    <li><div class="t">광고 예산</div><div class="m">11/18 유튜브 광고 집행 목표만 정해짐</div></li>\n    <li><div class="t">본편 5편의 회차별 구성</div><div class="m">기획 미확정</div></li>\n    <li><div class="t">\'0원 다마고치\' 채널과 셀러들의 수다의 관계</div><div class="m">11/4에는 \'셀러들의 수다 본진 + 스스로 월백 채널 공동작업자\'로 정했음. 새 채널 이름으로 같은 방식(공동작업자 연결)을 유지하는지 확인 필요</div></li>\n    <li><div class="t">채널 소유 명의</div><div class="m">11/4 회의록에서 \'확인 필요\'로 남은 항목</div></li>\n  </ul>\n</div>\n\n<div class="src">\n  근거 · 2026-11-11 정기 회의 뒤 민트가 카톡방에 올린 \'회의 내용 중 확인이 필요한 사항\' 공지(15:17)와 요청 2건(16:40 · 16:44), 루크의 확인 답글(19:03) ·\n  모집영상 촬영일(11/9)은 루크 확인 · 회의 녹음 전문은 반영하지 않았습니다 ·\n  날짜·요일은 2026년 11월 기준 대조(11/13 금 · 11/18 수 · 12/4 금) ·\n  빠진 내용이나 잘못 적힌 부분이 있으면 카톡방에 알려주세요\n</div>\n</div>\n'

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
    write(os.path.join(base, "relocation", "index.html"), page("10/16 등기 — 등기부 확인 끝", RELOCATION))
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
    write(os.path.join(base, "engine", "index.html"), page("식스 엔진 — 6개 수익 프로젝트", ENGINE))
    write(os.path.join(base, "map", "index.html"), page("지금 어디 있는가 — 과거·현재·미래", MAP))
    write(os.path.join(base, "ilsip", "index.html"), page("일십백천 — 유지할 것과 바꿀 것", ILSIP))
    write(os.path.join(base, "review", "index.html"), page("전략 재점검 — 남에게 가르친 것과 자기 회사", REVIEW))
    write(os.path.join(base, "park-contract", "index.html"), page("민트(박종혁) — 1차 계약서", CONTRACT))
    write(os.path.join(base, "park-terms", "index.html"), page("협업 조건 정리 — 멘토루크 × 민트", TERMS))
    write(os.path.join(base, "cash", "index.html"), page("11월 ~ 2월 — 들어올 돈과 나갈 돈", CASH))
    write(os.path.join(base, "oct23", "index.html"), page("10월 23일 — 세 대화", OCT23))
    write(os.path.join(base, "pd", "index.html"), page("조윤호 PD — 장기 파트너십 설계", PDDEAL))
    write(os.path.join(base, "pd-long", "index.html"), page("채널 운영 — 비용을 어떻게 잡나", PDLONG))
    write(os.path.join(base, "gaeul-contract", "index.html"), page("가을 대표님 계약서 — 괜찮은가", GAEULC))
    write(os.path.join(base, "pd-cost", "index.html"), page("PD 촬영비 — 민트님께 드릴 내용", PDCOST))
    write(os.path.join(base, "meetings", "index.html"), page_shared("회의록", MEETHUB))
    write(os.path.join(base, "min1030", "index.html"), page_shared("10/30 회의록", MIN1030))
    write(os.path.join(base, "min1104", "index.html"), page_shared("11/4 회의록", MIN1104))
    write(os.path.join(base, "min1111", "index.html"), page_shared("11/11 회의록", MIN1111))
    write(os.path.join(base, "exit300", "index.html"), page("300억 엑시트 — 가능한가", EXIT300))
    for g in GUIDES:
        write(os.path.join(base, "guides", g["slug"], "index.html"), page(g["title"], guide_page_html(g), root="../../"))
    write(os.path.join(base, "sources", "index.html"), page("출처·갱신 방법", SOURCES))
    print("built", UPDATED)

if __name__ == "__main__":
    main()
