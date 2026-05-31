import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="학사일정 최적화 엔진",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 여백, 헤더, 사이드바 숨기기
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }

    iframe {
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

HTML_CODE = r'''
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>학사일정 최적화 v4 · 공휴일·방학 반영</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,900&family=Spline+Sans:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --ink:#0f1419;
    --ink-soft:#1a2230;
    --panel:#161e2b;
    --panel-2:#1d2735;
    --line:#2a3647;
    --txt:#e8edf4;
    --txt-dim:#8b9bb0;
    --txt-faint:#5d6b7e;
    --teal:#3dd6c4;
    --teal-deep:#1a9d8f;
    --amber:#ffb347;
    --coral:#ff6b5e;
    --violet:#9d8cff;
    --gold:#f4d35e;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:var(--ink);color:var(--txt);font-family:'Spline Sans',sans-serif;-webkit-font-smoothing:antialiased}
  body{
    background:
      radial-gradient(1200px 600px at 85% -5%, rgba(61,214,196,.07), transparent 55%),
      radial-gradient(900px 500px at 10% 110%, rgba(157,140,255,.06), transparent 55%),
      var(--ink);
    min-height:100vh;padding:32px 24px 64px;
  }
  .wrap{max-width:1240px;margin:0 auto}

  /* ---------- Header ---------- */
  header{margin-bottom:32px;position:relative}
  .eyebrow{
    font-family:'Spline Sans Mono',monospace;font-size:12px;letter-spacing:.32em;
    text-transform:uppercase;color:var(--teal);margin-bottom:10px;
    display:flex;align-items:center;gap:10px;
  }
  .eyebrow::before{content:"";width:28px;height:1px;background:var(--teal);display:inline-block}
  h1{
    font-family:'Fraunces',serif;font-weight:900;font-size:clamp(34px,5vw,58px);
    line-height:.98;letter-spacing:-.02em;margin-bottom:14px;
  }
  h1 em{font-style:italic;color:var(--amber);font-weight:400}
  .sub{color:var(--txt-dim);font-size:15px;max-width:620px;line-height:1.6}
  .sub code{font-family:'Spline Sans Mono',monospace;color:var(--teal);font-size:13px;background:rgba(61,214,196,.08);padding:2px 6px;border-radius:4px}

  /* ---------- Layout ---------- */
  .grid{display:grid;grid-template-columns:380px 1fr;gap:24px;align-items:start}
  @media(max-width:920px){.grid{grid-template-columns:1fr}}

  .panel{
    background:linear-gradient(180deg,var(--panel),var(--panel-2));
    border:1px solid var(--line);border-radius:18px;padding:26px;
    position:relative;overflow:hidden;
  }
  .panel::before{
    content:"";position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(61,214,196,.5),transparent);
  }
  .panel-title{
    font-family:'Spline Sans Mono',monospace;font-size:11px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--txt-faint);margin-bottom:22px;
    display:flex;align-items:center;justify-content:space-between;
  }
  .panel-title span:last-child{color:var(--teal)}

  /* ---------- Controls ---------- */
  .field{margin-bottom:24px}
  .field:last-child{margin-bottom:0}
  label.lbl{display:block;font-size:13px;font-weight:600;color:var(--txt);margin-bottom:4px}
  .hint{font-size:11.5px;color:var(--txt-faint);margin-bottom:11px;line-height:1.45}

  input[type=number],input[type=date],input[type=text],select{
    width:100%;background:var(--ink-soft);border:1px solid var(--line);
    color:var(--txt);font-family:'Spline Sans Mono',monospace;font-size:14px;
    padding:11px 13px;border-radius:10px;transition:border-color .2s,box-shadow .2s;
  }
  input:focus,select:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(61,214,196,.13)}

  input[type=file]{
    width:100%;background:var(--ink-soft);border:1px dashed var(--line);color:var(--txt-dim);
    font-family:'Spline Sans',sans-serif;font-size:12.5px;padding:10px;border-radius:10px;cursor:pointer;
  }
  input[type=file]::file-selector-button{
    background:rgba(61,214,196,.12);border:1px solid rgba(61,214,196,.35);color:var(--teal);
    border-radius:7px;padding:7px 10px;margin-right:10px;cursor:pointer;font-family:'Spline Sans',sans-serif;font-weight:600;
  }
  .holiday-box{
    background:rgba(61,214,196,.06);border:1px solid rgba(61,214,196,.18);border-radius:10px;
    padding:11px 12px;margin-bottom:10px;font-size:12.5px;color:var(--txt-dim);line-height:1.55;
  }
  .holiday-box b{color:var(--teal);font-weight:700}
  .holiday-add-row{display:grid;grid-template-columns:1fr 1.2fr auto;gap:8px;margin-bottom:9px;align-items:center}
  .holiday-add-row button,.holiday-actions button{
    background:rgba(61,214,196,.12);border:1px solid rgba(61,214,196,.35);color:var(--teal);
    border-radius:9px;padding:10px 11px;cursor:pointer;font-family:'Spline Sans',sans-serif;font-size:12.5px;font-weight:700;white-space:nowrap;
    transition:all .15s;
  }
  .holiday-add-row button:hover,.holiday-actions button:hover{background:rgba(61,214,196,.2)}
  .holiday-actions{display:grid;grid-template-columns:1fr;gap:8px;margin-top:9px}
  .holiday-actions button.reset{background:rgba(255,107,94,.08);border-color:rgba(255,107,94,.28);color:var(--coral)}
  .holiday-actions button.reset:hover{background:rgba(255,107,94,.16)}
  .holiday-list{max-height:144px;overflow:auto;border:1px solid var(--line);border-radius:10px;background:rgba(15,20,25,.25);margin:8px 0 10px;padding:6px}
  .holiday-item{display:grid;grid-template-columns:74px 1fr auto;gap:8px;align-items:center;padding:6px 4px;border-bottom:1px solid rgba(42,54,71,.7);font-size:12px;color:var(--txt-dim)}
  .holiday-item:last-child{border-bottom:none}
  .holiday-item .date{font-family:'Spline Sans Mono',monospace;color:var(--teal)}
  .holiday-item .name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .holiday-del{
    width:25px;height:25px;border-radius:7px;border:1px solid rgba(255,107,94,.3);
    background:rgba(255,107,94,.09);color:var(--coral);cursor:pointer;font-size:15px;line-height:1;
  }
  @media(max-width:460px){.holiday-add-row{grid-template-columns:1fr}.holiday-item{grid-template-columns:72px 1fr auto}}
  .pref-mini{display:grid;gap:14px}
  .pref-row{display:grid;grid-template-columns:1fr 70px;gap:12px;align-items:center}
  .pref-row .pref-name{font-size:12.5px;color:var(--txt-dim);line-height:1.35}
  .pref-row .pref-name b{color:var(--txt);font-weight:600}
  .pref-val{font-family:'Fraunces',serif;font-size:24px;font-weight:900;color:var(--amber);text-align:right;line-height:1}
  .pref-val small{font-family:'Spline Sans',sans-serif;font-size:11px;color:var(--txt-faint);font-weight:500;display:block;margin-top:2px}
  select{cursor:pointer;appearance:none;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='%238b9bb0' d='M6 8L0 0h12z'/%3E%3C/svg%3E");
    background-repeat:no-repeat;background-position:right 14px center;padding-right:36px}

  /* slider */
  .slider-row{display:flex;align-items:center;gap:16px}
  .slider-val{
    font-family:'Fraunces',serif;font-weight:900;font-size:30px;color:var(--amber);
    min-width:54px;text-align:right;line-height:1;
  }
  .slider-val small{font-family:'Spline Sans',sans-serif;font-size:12px;color:var(--txt-faint);font-weight:500;display:block;margin-top:2px}
  input[type=range]{
    -webkit-appearance:none;appearance:none;width:100%;height:6px;border-radius:99px;
    background:linear-gradient(90deg,var(--teal-deep),var(--teal));cursor:pointer;
  }
  input[type=range]::-webkit-slider-thumb{
    -webkit-appearance:none;width:22px;height:22px;border-radius:50%;
    background:#fff;border:4px solid var(--teal);box-shadow:0 2px 10px rgba(0,0,0,.4);cursor:pointer;transition:transform .15s}
  input[type=range]::-webkit-slider-thumb:hover{transform:scale(1.15)}
  input[type=range]::-moz-range-thumb{width:22px;height:22px;border-radius:50%;background:#fff;border:4px solid var(--teal);cursor:pointer}

  /* vacation rows */
  .vac-row{display:grid;grid-template-columns:1fr 1fr auto;gap:8px;margin-bottom:9px;align-items:center}
  .vac-row .dash{color:var(--txt-faint);text-align:center;font-size:13px}
  .vac-del{
    background:rgba(255,107,94,.1);border:1px solid rgba(255,107,94,.3);color:var(--coral);
    width:34px;height:38px;border-radius:9px;cursor:pointer;font-size:18px;line-height:1;
    transition:all .15s;display:flex;align-items:center;justify-content:center}
  .vac-del:hover{background:rgba(255,107,94,.2)}
  .vac-add{
    width:100%;background:transparent;border:1px dashed var(--line);color:var(--txt-dim);
    padding:10px;border-radius:10px;cursor:pointer;font-family:'Spline Sans',sans-serif;
    font-size:13px;font-weight:600;transition:all .15s;margin-top:4px}
  .vac-add:hover{border-color:var(--teal);color:var(--teal)}

  /* seg control */
  .seg{display:flex;background:var(--ink-soft);border:1px solid var(--line);border-radius:10px;padding:4px;gap:4px}
  .seg button{
    flex:1;background:transparent;border:none;color:var(--txt-dim);padding:10px 8px;border-radius:7px;
    cursor:pointer;font-family:'Spline Sans',sans-serif;font-size:12.5px;font-weight:600;transition:all .18s}
  .seg button.on{background:var(--teal);color:var(--ink);box-shadow:0 2px 8px rgba(61,214,196,.3)}

  /* run button */
  .run{
    width:100%;margin-top:26px;background:linear-gradient(135deg,var(--amber),var(--gold));
    color:var(--ink);border:none;padding:16px;border-radius:12px;cursor:pointer;
    font-family:'Spline Sans',sans-serif;font-weight:700;font-size:15px;letter-spacing:.02em;
    transition:transform .15s,box-shadow .2s;box-shadow:0 6px 20px rgba(255,179,71,.25)}
  .run:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 10px 28px rgba(255,179,71,.35)}
  .run:disabled{opacity:.5;cursor:not-allowed}

  /* ---------- Results ---------- */
  .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}
  .stat{background:var(--ink-soft);border:1px solid var(--line);border-radius:14px;padding:18px}
  .stat .k{font-family:'Spline Sans Mono',monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--txt-faint);margin-bottom:9px}
  .stat .v{font-family:'Fraunces',serif;font-weight:900;font-size:32px;line-height:1;letter-spacing:-.01em}
  .stat .v small{font-size:14px;color:var(--txt-dim);font-weight:400;font-family:'Spline Sans',sans-serif}
  .stat.hl .v{color:var(--teal)}
  .stat.warn .v{color:var(--amber)}

  /* progress */
  .prog-wrap{margin-bottom:22px;display:none}
  .prog-wrap.show{display:block}
  .prog-bar{height:8px;background:var(--ink-soft);border-radius:99px;overflow:hidden;border:1px solid var(--line)}
  .prog-fill{height:100%;width:0;background:linear-gradient(90deg,var(--teal-deep),var(--teal));transition:width .1s;border-radius:99px}
  .prog-txt{display:flex;justify-content:space-between;font-family:'Spline Sans Mono',monospace;font-size:11.5px;color:var(--txt-dim);margin-top:8px}

  /* calendar */
  .cal-legend{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:18px;font-size:12px;color:var(--txt-dim)}
  .cal-legend .lg{display:flex;align-items:center;gap:7px}
  .sw{width:13px;height:13px;border-radius:3px;display:inline-block}
  .cal-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
  @media(max-width:1100px){.cal-grid{grid-template-columns:repeat(3,1fr)}}
  @media(max-width:680px){.cal-grid{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:460px){.cal-grid{grid-template-columns:1fr}}
  .month{background:var(--ink-soft);border:1px solid var(--line);border-radius:12px;padding:12px}
  .month-name{font-family:'Spline Sans Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--txt-dim);margin-bottom:9px;text-align:center}
  .dow{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-bottom:4px}
  .dow span{font-size:8.5px;text-align:center;color:var(--txt-faint);font-family:'Spline Sans Mono',monospace}
  .days{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
  .day{aspect-ratio:1;border-radius:3.5px;display:flex;align-items:center;justify-content:center;font-size:9px;color:rgba(255,255,255,.4);font-family:'Spline Sans Mono',monospace;position:relative;cursor:default;transition:transform .1s}
  .day:hover{transform:scale(1.25);z-index:5}
  .day.empty{background:transparent}
  .day.class{background:var(--ink)}
  .day.weekend{background:#2b3445}
  .day.disc{background:var(--amber);color:var(--ink);font-weight:600}
  .day.vac{background:rgba(157,140,255,.22);color:var(--violet)}
  .day.holiday{background:rgba(61,214,196,.22);color:var(--teal);font-weight:600}

  .empty-state{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    min-height:480px;text-align:center;color:var(--txt-faint)}
  .empty-state svg{margin-bottom:20px;opacity:.5}
  .empty-state h3{font-family:'Fraunces',serif;font-weight:600;font-size:22px;color:var(--txt-dim);margin-bottom:8px}
  .empty-state p{font-size:13.5px;max-width:340px;line-height:1.6}

  .disc-list{margin-top:24px}
  .disc-list h4{font-family:'Spline Sans Mono',monospace;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:var(--txt-faint);margin-bottom:13px}
  .chips{display:flex;flex-wrap:wrap;gap:8px}
  .chip{background:rgba(255,179,71,.1);border:1px solid rgba(255,179,71,.3);color:var(--amber);
    padding:7px 12px;border-radius:8px;font-family:'Spline Sans Mono',monospace;font-size:12.5px}
  .chip b{color:var(--gold);font-weight:600}
  .chip.near-vac{border-color:rgba(255,107,94,.42);background:rgba(255,107,94,.09);color:var(--coral)}
  .note{font-size:12px;color:var(--txt-faint);line-height:1.6;margin-top:18px;padding:14px;background:rgba(157,140,255,.05);border:1px solid rgba(157,140,255,.15);border-radius:10px}
  .note b{color:var(--violet)}
  .err{color:var(--coral);font-size:13px;margin-top:14px;padding:12px;background:rgba(255,107,94,.08);border:1px solid rgba(255,107,94,.25);border-radius:10px;display:none}
  .err.show{display:block}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eyebrow">Ebbinghaus · Genetic Algorithm</div>
    <h1>학사일정 <em>최적화</em> 엔진</h1>
    <p class="sub">에빙하우스 망각곡선 <code>k(t)=k₀/(1+c·t)ᵈ</code> 기반 v4 모델로, 주말·국가공휴일·방학을 고정한 뒤 재량휴업일을 어디에 배치해야 <b>평균 망각지수</b>와 학사 운영 선호가 함께 좋아지는지 유전 알고리즘으로 탐색합니다.</p>
  </header>

  <div class="grid">
    <!-- ============ INPUT PANEL ============ -->
    <div class="panel">
      <div class="panel-title"><span>입력 조건</span><span>CONFIG</span></div>

      <div class="field">
        <label class="lbl" for="year">대상 연도</label>
        <div class="hint">1월 1일 ~ 12월 31일 전체를 달력으로 생성합니다.</div>
        <input type="number" id="year" value="2025" min="2000" max="2100">
      </div>

      <div class="field">
        <label class="lbl">재량휴업일 수</label>
        <div class="hint">수업 가능한 평일 중 배치할 휴업일 개수. 주말과 국가공휴일은 별도로 항상 휴업입니다.</div>
        <div class="slider-row">
          <input type="range" id="restSlider" min="0" max="40" value="10">
          <div class="slider-val"><span id="restVal">10</span><small>일</small></div>
        </div>
      </div>

      <div class="field">
        <label class="lbl">방학 기간</label>
        <div class="hint">이 기간은 계획·평가에서 제외됩니다. 여러 구간을 추가할 수 있어요.</div>
        <div id="vacList"></div>
        <button class="vac-add" id="vacAdd">+ 방학 기간 추가</button>
      </div>

      <div class="field">
        <label class="lbl">국가 공휴일 데이터</label>
        <div class="hint">2025년 국가공휴일은 코드 안에 기본값으로 내장되어 있습니다. 다른 연도는 아래에서 직접 추가하거나 CSV로 선택적으로 불러올 수 있습니다.</div>
        <div class="holiday-box" id="holidayInfo">공휴일 데이터를 확인하는 중입니다.</div>

        <div class="holiday-add-row">
          <input type="date" id="holidayDate" aria-label="추가할 공휴일 날짜">
          <input type="text" id="holidayName" placeholder="공휴일명 예: 개교기념일, 대체공휴일" aria-label="추가할 공휴일 이름">
          <button type="button" id="holidayAdd">+ 추가</button>
        </div>
        <div class="hint">추가한 날짜는 선택한 연도와 관계없이 저장되어, 해당 연도를 열면 자동으로 고정 휴업일에 반영됩니다.</div>
        <div class="holiday-list" id="holidayList"></div>
        <input type="file" id="holidayFile" accept=".csv,text/csv">
        <div class="holiday-actions">
          <button type="button" class="reset" id="holidayReset">내장 2025 공휴일만 남기기</button>
        </div>
      </div>

      <div class="field">
        <label class="lbl">목적함수 기준</label>
        <div class="hint">무엇의 평균 망각지수를 최소화할지 선택합니다.</div>
        <div class="seg" id="objSeg">
          <button data-obj="all" class="on">모든 날</button>
          <button data-obj="class">수업일만</button>
        </div>
      </div>

      <div class="field">
        <label class="lbl">현실 보정 옵션</label>
        <div class="hint">최종 목적함수는 평균 망각지수를 중심으로 하되, 방학 인접 회피만 반영합니다.</div>
        <div class="pref-mini">
          <div class="pref-row">
            <div class="pref-name"><b>방학 인접 회피 범위</b><br>방학 시작·종료일 전후 며칠까지 피할지</div>
            <div class="pref-val"><span id="vacBufferVal">5</span><small>일</small></div>
          </div>
          <input type="range" id="vacBuffer" min="0" max="14" value="5">
          <div class="pref-row">
            <div class="pref-name"><b>방학 인접 패널티</b><br>값이 클수록 방학 근처 재량휴업일을 더 강하게 회피</div>
            <div class="pref-val"><span id="vacWeightVal">5.0</span></div>
          </div>
          <input type="range" id="vacWeight" min="0" max="10" step="0.5" value="5">
        </div>
      </div>

      <button class="run" id="runBtn">⟐ 최적 일정 탐색 시작</button>
      <div class="err" id="errBox"></div>
    </div>

    <!-- ============ RESULT PANEL ============ -->
    <div class="panel">
      <div class="panel-title"><span>탐색 결과</span><span id="objLabel">OBJECTIVE · ALL</span></div>

      <div class="prog-wrap" id="progWrap">
        <div class="prog-bar"><div class="prog-fill" id="progFill"></div></div>
        <div class="prog-txt"><span id="progGen">세대 0 / 0</span><span id="progBest">—</span></div>
      </div>

      <div id="resultArea">
        <div class="empty-state">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
            <rect x="3" y="4" width="18" height="18" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/>
            <circle cx="8" cy="15" r="1.4" fill="currentColor" stroke="none"/>
            <circle cx="12" cy="15" r="1.4" fill="currentColor" stroke="none"/>
          </svg>
          <h3>아직 탐색 전입니다</h3>
          <p>왼쪽에서 조건을 설정하고 <b>탐색 시작</b>을 누르면, 유전 알고리즘이 세대를 거듭하며 최적 학사일정을 찾아냅니다.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
/* ===================================================================
   v3 망각 모델 파라미터 (Ebbinghaus 180일 데이터로 최적화 완료)
   =================================================================== */
const MODEL = { M0:100.0, K0:1.0987, C:16.6823, D:0.8666, R:0.30 };
const kAt = t => MODEL.K0 / Math.pow(1 + MODEL.C * t, MODEL.D);

/* ===================================================================
   유전 알고리즘 파라미터
   =================================================================== */
const GA = { POP:80, GEN:1200, TOUR:3, CX:0.9, MUT:0.02, ELITE:4 };

/* ---------- 날짜 유틸 ---------- */
const WD = ['일','월','화','수','목','금','토'];
const ymd = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
const parseD = s => { const [y,m,dd]=s.split('-').map(Number); return new Date(y,m-1,dd); };
const daysBetween = (a,b) => Math.round((stripTime(b)-stripTime(a))/86400000);
const stripTime = d => new Date(d.getFullYear(), d.getMonth(), d.getDate());

/* ---------- 내장 국가 공휴일 데이터: 업로드된 CSV 기준 ---------- */
const DEFAULT_HOLIDAYS = [
  {
    "date": "2025-01-01",
    "name": "신정 (New Year's Day)"
  },
  {
    "date": "2025-01-27",
    "name": "설날 연휴"
  },
  {
    "date": "2025-01-28",
    "name": "설날 연휴"
  },
  {
    "date": "2025-01-29",
    "name": "설날 연휴"
  },
  {
    "date": "2025-01-30",
    "name": "설날 연휴"
  },
  {
    "date": "2025-03-01",
    "name": "삼일절"
  },
  {
    "date": "2025-03-03",
    "name": "삼일절 대체공휴일"
  },
  {
    "date": "2025-05-01",
    "name": "근로자의 날"
  },
  {
    "date": "2025-05-05",
    "name": "부처님 오신 날"
  },
  {
    "date": "2025-05-05",
    "name": "어린이날"
  },
  {
    "date": "2025-05-06",
    "name": "부처님 오신 날 / 어린이날 대체공휴일"
  },
  {
    "date": "2025-06-06",
    "name": "현충일"
  },
  {
    "date": "2025-08-15",
    "name": "광복절"
  },
  {
    "date": "2025-10-03",
    "name": "개천절"
  },
  {
    "date": "2025-10-05",
    "name": "추석 연휴 시작"
  },
  {
    "date": "2025-10-06",
    "name": "추석 연휴"
  },
  {
    "date": "2025-10-07",
    "name": "추석 연휴"
  },
  {
    "date": "2025-10-08",
    "name": "추석 대체공휴일"
  },
  {
    "date": "2025-10-09",
    "name": "한글날"
  },
  {
    "date": "2025-12-25",
    "name": "크리스마스"
  }
];

/* ---------- 공휴일/방학 유틸 ---------- */
function holidayMapFor(year, holidayRows){
  const map = new Map();
  holidayRows.forEach(h=>{
    if(!h.date || !h.date.startsWith(String(year)+'-')) return;
    if(!map.has(h.date)) map.set(h.date, []);
    if(!map.get(h.date).includes(h.name)) map.get(h.date).push(h.name);
  });
  return map;
}

function vacationBoundaryDistance(d, vacations){
  if(!vacations.length) return Infinity;
  let best = Infinity;
  const dd = stripTime(d);
  vacations.forEach(v=>{
    best = Math.min(best, Math.abs(daysBetween(dd, stripTime(v.start))));
    best = Math.min(best, Math.abs(daysBetween(dd, stripTime(v.end))));
  });
  return best;
}


/* ---------- 달력 생성 (방학 제외, 주말·국가공휴일 고정 휴업) ---------- */
function buildCalendar(year, vacations, holidayRows){
  const holidayMap = holidayMapFor(year, holidayRows);
  const inVac = d => vacations.some(v => d >= stripTime(v.start) && d <= stripTime(v.end));
  const days = [];
  let d = new Date(year,0,1);
  const end = new Date(year,11,31);
  while(d <= end){
    const cur = stripTime(d);
    if(!inVac(cur)){
      const key = ymd(cur);
      const wd = cur.getDay();              // 0=일,6=토
      const weekend = (wd===0 || wd===6);
      const holidayNames = holidayMap.get(key) || [];
      const holiday = holidayNames.length > 0;
      days.push({
        date:new Date(cur),
        weekend,
        holiday,
        holidayNames,
        fixedRest: weekend || holiday,
        flexible: !(weekend || holiday),
        vacDist: vacationBoundaryDistance(cur, vacations),
      });
    }
    d.setDate(d.getDate()+1);
  }
  return days;
}

/* ---------- 현실 보정 점수: 방학 인접 패널티 ---------- */
function socialAdjustment(restMask, cal, pref){
  let disc=0, vacPenaltyRaw=0, nearVacCount=0;
  for(let i=0;i<restMask.length;i++){
    const c = cal[i];
    if(!(restMask[i] && c.flexible)) continue;  // 재량휴업일만 평가
    disc++;
    if(pref.vacBuffer>0 && c.vacDist>0 && c.vacDist<=pref.vacBuffer){
      // 방학에 가까울수록 더 큰 패널티. 평균 망각지수와 같은 스케일로 정규화합니다.
      vacPenaltyRaw += ((pref.vacBuffer - c.vacDist + 1) / pref.vacBuffer) * pref.vacWeight;
      nearVacCount++;
    }
  }
  const denom = Math.max(1, disc);
  const vacPenalty = vacPenaltyRaw / denom;
  return {
    adjustment: vacPenalty,
    vacPenalty,
    nearVacCount,
    discretionaryCount:disc,
  };
}

/* ---------- 적합도: 평균 망각지수 + 현실 보정 + 일별 risk 반환 ---------- */
function evaluate(restMask, objective, cal=null, pref=null){
  let memory = MODEL.M0, t = 0, sum = 0, count = 0;
  const dailyRisk = new Array(restMask.length);
  for(let i=0;i<restMask.length;i++){
    if(restMask[i]){ t++; memory *= Math.exp(-kAt(t)); }
    else{ memory += MODEL.R*(MODEL.M0-memory); t=0; }
    if(memory<0)memory=0; if(memory>100)memory=100;
    const risk = 100-memory;
    dailyRisk[i]=risk;
    if(objective==='all'){ sum+=risk; count++; }
    else if(!restMask[i]){ sum+=risk; count++; }
  }
  const baseRisk = sum/Math.max(1,count);
  const social = (cal && pref) ? socialAdjustment(restMask, cal, pref) : {adjustment:0,vacPenalty:0,nearVacCount:0,discretionaryCount:0};
  return { fitness: baseRisk + social.adjustment, baseRisk, dailyRisk, social };
}

/* ---------- GA 헬퍼 ---------- */
function sample(arr,n){ const c=arr.slice(); for(let i=c.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[c[i],c[j]]=[c[j],c[i]];} return c.slice(0,n); }

function makeIndividual(nFlex,nRest){
  const g=new Uint8Array(nFlex);
  for(const i of sample([...Array(nFlex).keys()],nRest)) g[i]=1;
  return g;
}
function decode(genome, flexIdx, fixedIdx, total){
  const mask=new Uint8Array(total);
  for(const i of fixedIdx) mask[i]=1;
  for(let i=0;i<genome.length;i++) if(genome[i]) mask[flexIdx[i]]=1;
  return mask;
}
function repair(g,nRest){
  let cnt=0; for(const v of g) cnt+=v;
  if(cnt>nRest){
    const idx=[]; for(let i=0;i<g.length;i++) if(g[i]) idx.push(i);
    for(const i of sample(idx,cnt-nRest)) g[i]=0;
  }else if(cnt<nRest){
    const idx=[]; for(let i=0;i<g.length;i++) if(!g[i]) idx.push(i);
    for(const i of sample(idx,nRest-cnt)) g[i]=1;
  }
  return g;
}
function crossover(p1,p2,nRest){
  if(Math.random()>GA.CX) return [p1.slice(),p2.slice()];
  const pt=1+(Math.random()*(p1.length-1)|0);
  const c1=new Uint8Array(p1.length), c2=new Uint8Array(p1.length);
  for(let i=0;i<p1.length;i++){
    c1[i]= i<pt? p1[i]:p2[i];
    c2[i]= i<pt? p2[i]:p1[i];
  }
  return [repair(c1,nRest),repair(c2,nRest)];
}
function mutate(g,nRest){
  for(let i=0;i<g.length;i++) if(Math.random()<GA.MUT) g[i]^=1;
  return repair(g,nRest);
}
function tournament(pop,fits){
  let best=-1;
  for(let i=0;i<GA.TOUR;i++){ const r=Math.random()*pop.length|0; if(best<0||fits[r]<fits[best]) best=r; }
  return pop[best].slice();
}

/* ---------- GA 메인 (async, 진행률 콜백) ---------- */
async function runGA(cal, nRest, objective, pref, onProgress){
  const total=cal.length;
  const flexIdx=[], fixedIdx=[], weekendIdx=[], holidayIdx=[];
  cal.forEach((c,i)=>{
    if(c.flexible) flexIdx.push(i);
    if(c.fixedRest) fixedIdx.push(i);
    if(c.weekend) weekendIdx.push(i);
    if(c.holiday) holidayIdx.push(i);
  });
  if(nRest>flexIdx.length) throw new Error(`재량휴업일(${nRest}일)이 배치 가능한 평일(${flexIdx.length}일)보다 많습니다.`);

  const fitOf=g=>evaluate(decode(g,flexIdx,fixedIdx,total),objective,cal,pref).fitness;

  let pop=Array.from({length:GA.POP},()=>makeIndividual(flexIdx.length,nRest));
  let fits=pop.map(fitOf);

  for(let gen=0;gen<GA.GEN;gen++){
    const order=[...fits.keys()].sort((a,b)=>fits[a]-fits[b]);
    const newPop=[];
    for(let i=0;i<GA.ELITE;i++) newPop.push(pop[order[i]].slice());
    while(newPop.length<GA.POP){
      const [c1,c2]=crossover(tournament(pop,fits),tournament(pop,fits),nRest);
      newPop.push(mutate(c1,nRest));
      if(newPop.length<GA.POP) newPop.push(mutate(c2,nRest));
    }
    pop=newPop; fits=pop.map(fitOf);
    const best=Math.min(...fits);
    if(gen%2===0 || gen===GA.GEN-1){
      onProgress(gen+1,GA.GEN,best);
      await new Promise(r=>setTimeout(r,0));  // UI yield
    }
  }
  const bi=fits.indexOf(Math.min(...fits));
  const bestMask=decode(pop[bi],flexIdx,fixedIdx,total);
  const ev=evaluate(bestMask,objective,cal,pref);
  return { mask:bestMask, fitness:ev.fitness, baseRisk:ev.baseRisk, dailyRisk:ev.dailyRisk, social:ev.social, flexIdx, fixedIdx, weekendIdx, holidayIdx };
}

/* ===================================================================
   UI 로직
   =================================================================== */
let vacations=[
  {start:'2025-01-01',end:'2025-02-28'},
  {start:'2025-07-21',end:'2025-08-18'},
];
let objective='all';
let holidays=loadHolidayRows();
let lastYear=2025;

const $=id=>document.getElementById(id);
const pref = () => ({
  vacBuffer: parseInt($('vacBuffer').value),
  vacWeight: parseFloat($('vacWeight').value),
});

function updatePrefLabels(){
  $('vacBufferVal').textContent=$('vacBuffer').value;
  $('vacWeightVal').textContent=parseFloat($('vacWeight').value).toFixed(1);
}

function sortHolidayRows(rows){
  return rows.slice().sort((a,b)=> (a.date+a.name).localeCompare(b.date+b.name, 'ko'));
}

function mergeHolidayRows(baseRows, addRows){
  const seen = new Set();
  const merged = [];
  [...baseRows, ...addRows].forEach(h=>{
    if(!h || !/^\d{4}-\d{2}-\d{2}$/.test(h.date || '') || !(h.name || '').trim()) return;
    const row = {date:h.date, name:h.name.trim()};
    const key = row.date + '|' + row.name;
    if(seen.has(key)) return;
    seen.add(key); merged.push(row);
  });
  return sortHolidayRows(merged);
}

function saveHolidayRows(){
  try{ localStorage.setItem('schoolOptimizerHolidays', JSON.stringify(holidays)); }catch(e){}
}

function loadHolidayRows(){
  try{
    const saved = JSON.parse(localStorage.getItem('schoolOptimizerHolidays') || 'null');
    if(Array.isArray(saved) && saved.length) return mergeHolidayRows(DEFAULT_HOLIDAYS, saved);
  }catch(e){}
  return DEFAULT_HOLIDAYS.slice();
}

function currentYearHolidays(year){
  return holidays
    .map((h,i)=>({...h, idx:i}))
    .filter(h=>h.date.startsWith(String(year)+'-'))
    .sort((a,b)=> (a.date+a.name).localeCompare(b.date+b.name, 'ko'));
}

function renderHolidayList(year){
  const box=$('holidayList');
  const rows=currentYearHolidays(year);
  if(!rows.length){
    box.innerHTML='<div class="holiday-item"><span class="date">—</span><span class="name">이 연도의 공휴일이 없습니다. 위 칸에서 직접 추가하세요.</span><span></span></div>';
    return;
  }
  box.innerHTML=rows.map(h=>`
    <div class="holiday-item">
      <span class="date">${h.date.slice(5)}</span>
      <span class="name" title="${h.name.replace(/"/g,'&quot;')}">${h.name}</span>
      <button type="button" class="holiday-del" data-i="${h.idx}" title="삭제">×</button>
    </div>`).join('');
  box.querySelectorAll('.holiday-del').forEach(btn=>{
    btn.addEventListener('click',e=>{
      holidays.splice(+e.currentTarget.dataset.i,1);
      saveHolidayRows();
      updateHolidayInfo();
    });
  });
}

function updateHolidayInfo(){
  const year=parseInt($('year').value)||lastYear||2025;
  const map=holidayMapFor(year,holidays);
  const totalNames=[...map.values()].reduce((s,names)=>s+names.length,0);
  const days=[...map.keys()].sort();
  const sample=days.slice(0,4).map(d=>`${d.slice(5)} ${map.get(d).join('/')}`).join(' · ');
  const builtInCount=DEFAULT_HOLIDAYS.filter(h=>h.date.startsWith(String(year)+'-')).length;
  $('holidayInfo').innerHTML = days.length
    ? `<b>${year}년 공휴일 ${days.length}일</b>(${totalNames}개 항목) 반영됨<br>${sample}${days.length>4?' · …':''}${year===2025?'<br>※ 2025년 데이터는 코드에 기본 내장되어 있습니다.':''}`
    : `<b>${year}년 공휴일 데이터가 없습니다.</b><br>아래 추가 칸에 직접 입력하거나 CSV를 선택적으로 불러오면 주말처럼 고정 휴업일로 반영됩니다.`;
  renderHolidayList(year);
  const hd=$('holidayDate');
  if(hd && (!hd.value || !hd.value.startsWith(String(year)+'-'))) hd.value=`${year}-01-01`;
}

function parseCSVLine(line){
  const out=[]; let cur='', q=false;
  for(let i=0;i<line.length;i++){
    const ch=line[i];
    if(ch==='"' && line[i+1]==='"'){ cur+='"'; i++; continue; }
    if(ch==='"'){ q=!q; continue; }
    if(ch===',' && !q){ out.push(cur); cur=''; continue; }
    cur+=ch;
  }
  out.push(cur); return out.map(s=>s.trim().replace(/^﻿/,''));
}

function parseHolidayCSV(text){
  const lines=text.split(/\r?\n/).filter(l=>l.trim());
  if(lines.length<2) return [];
  const head=parseCSVLine(lines[0]);
  const dateIdx=head.findIndex(h=>h.includes('날짜') || h.toLowerCase()==='date');
  const nameIdx=Math.max(0, head.findIndex(h=>h.includes('공휴일') || h.includes('휴관') || h.toLowerCase().includes('name')));
  const out=[];
  for(const line of lines.slice(1)){
    const cols=parseCSVLine(line);
    const date=cols[dateIdx];
    const name=cols[nameIdx] || cols[0];
    if(/^\d{4}-\d{2}-\d{2}$/.test(date) && name) out.push({date,name});
  }
  return out;
}

function renderVacList(){
  const box=$('vacList'); box.innerHTML='';
  vacations.forEach((v,i)=>{
    const row=document.createElement('div'); row.className='vac-row';
    row.innerHTML=`
      <input type="date" value="${v.start}" data-i="${i}" data-k="start">
      <span class="dash">—</span>
      <input type="date" value="${v.end}" data-i="${i}" data-k="end">
      <button class="vac-del" data-i="${i}">×</button>`;
    box.appendChild(row);
  });
  box.querySelectorAll('input[type=date]').forEach(inp=>{
    inp.addEventListener('change',e=>{
      vacations[+e.target.dataset.i][e.target.dataset.k]=e.target.value;
    });
  });
  box.querySelectorAll('.vac-del').forEach(b=>{
    b.addEventListener('click',e=>{ vacations.splice(+e.target.dataset.i,1); renderVacList(); });
  });
}
renderVacList();

$('vacAdd').addEventListener('click',()=>{
  const y=$('year').value||2025;
  vacations.push({start:`${y}-07-21`,end:`${y}-08-18`}); renderVacList();
});

$('restSlider').addEventListener('input',e=>$('restVal').textContent=e.target.value);
['vacBuffer','vacWeight'].forEach(id=>$(id).addEventListener('input',updatePrefLabels));
updatePrefLabels();
updateHolidayInfo();

$('holidayFile').addEventListener('change',async e=>{
  const file=e.target.files?.[0];
  if(!file) return;
  try{
    const rows=parseHolidayCSV(await file.text());
    if(!rows.length) throw new Error('날짜와 공휴일명이 있는 CSV가 아닙니다.');
    holidays=mergeHolidayRows(holidays, rows);
    saveHolidayRows();
    updateHolidayInfo();
  }catch(err){ showErr('공휴일 CSV를 읽지 못했습니다: '+err.message); }
});

$('holidayAdd').addEventListener('click',()=>{
  const date=$('holidayDate').value;
  const name=$('holidayName').value.trim();
  if(!/^\d{4}-\d{2}-\d{2}$/.test(date)){ showErr('추가할 공휴일 날짜를 올바르게 입력하세요.'); return; }
  if(!name){ showErr('추가할 공휴일 이름을 입력하세요.'); return; }
  holidays=mergeHolidayRows(holidays, [{date,name}]);
  $('holidayName').value='';
  saveHolidayRows();
  updateHolidayInfo();
});

$('holidayReset').addEventListener('click',()=>{
  holidays=DEFAULT_HOLIDAYS.slice();
  try{ localStorage.removeItem('schoolOptimizerHolidays'); }catch(e){}
  updateHolidayInfo();
});

$('year').addEventListener('change',e=>{
  const y=parseInt(e.target.value);
  if(!y || y<2000 || y>2100) return;
  // 방학 기간 입력은 원래 방식대로 사용자가 직접 지정한 값을 유지합니다.
  lastYear=y; updateHolidayInfo();
});

$('objSeg').addEventListener('click',e=>{
  if(e.target.tagName!=='BUTTON')return;
  objective=e.target.dataset.obj;
  $('objSeg').querySelectorAll('button').forEach(b=>b.classList.toggle('on',b===e.target));
  $('objLabel').textContent='OBJECTIVE · '+objective.toUpperCase();
});

function showErr(msg){ const e=$('errBox'); e.textContent='⚠ '+msg; e.classList.add('show'); }
function clearErr(){ $('errBox').classList.remove('show'); }

/* ---------- 결과 렌더 ---------- */
function renderResult(res,cal,year,nRest,objective){
  const nFlex=res.flexIdx.length, nWeek=res.weekendIdx.length, nHoliday=res.holidayIdx.length;
  const classDays=nFlex-nRest;

  // 배치된 재량휴업일
  const discDays=[];
  cal.forEach((c,i)=>{ if(res.mask[i] && c.flexible) discDays.push(c); });

  const chips = discDays.map(c=>{
    const d=c.date;
    const flags=[];
    if(pref().vacBuffer>0 && c.vacDist>0 && c.vacDist<=pref().vacBuffer) flags.push(`방학 ${c.vacDist}일 인접`);
    const cls = flags.some(f=>f.includes('방학')) ? 'chip near-vac' : 'chip';
    return `<span class="${cls}"><b>${d.getMonth()+1}/${d.getDate()}</b> ${WD[d.getDay()]}${flags.length?` · ${flags.join(' · ')}`:''}</span>`;
  }).join('');

  // 캘린더 (방학/주말/공휴일/수업/재량휴업 색)
  const maskByDate={}, vacSet=new Set();
  cal.forEach((c,i)=>{ maskByDate[ymd(c.date)]={rest:res.mask[i],weekend:c.weekend,holiday:c.holiday,holidayNames:c.holidayNames,flexible:c.flexible}; });
  vacations.forEach(v=>{ let d=parseD(v.start); const e=parseD(v.end); while(d<=e){vacSet.add(ymd(d)); d.setDate(d.getDate()+1);} });

  let calHTML='';
  for(let m=0;m<12;m++){
    const first=new Date(year,m,1), pad=first.getDay();
    const dim=new Date(year,m+1,0).getDate();
    let cells='';
    for(let p=0;p<pad;p++) cells+='<div class="day empty"></div>';
    for(let dn=1;dn<=dim;dn++){
      const key=ymd(new Date(year,m,dn));
      let cls='class', label=dn, title=key;
      if(vacSet.has(key)) cls='vac';
      else if(maskByDate[key]){
        const mday=maskByDate[key];
        if(mday.rest && mday.flexible){ cls='disc'; }
        else if(mday.holiday){ cls='holiday'; title += ' · '+mday.holidayNames.join(', '); }
        else if(mday.weekend) cls='weekend';
        else cls='class';
      }
      cells+=`<div class="day ${cls}" title="${title}">${label}</div>`;
    }
    calHTML+=`<div class="month"><div class="month-name">${m+1}월</div>
      <div class="dow"><span>일</span><span>월</span><span>화</span><span>수</span><span>목</span><span>금</span><span>토</span></div>
      <div class="days">${cells}</div></div>`;
  }

  const noteText = objective==='class'
    ? `<b>수업일 기준</b>입니다. 휴업일 자체의 망각은 평가에서 제외하고, 학생이 "수업하러 왔을 때 얼마나 잊고 왔는가"를 기본 지표로 둡니다. 여기에 <b>방학 인접 패널티</b>를 더해 실제 학사 운영 선호를 반영했습니다.`
    : `<b>모든 날 기준</b>입니다. 휴업일을 포함한 전체 평균 망각지수를 기본 지표로 둡니다. 국가공휴일은 주말처럼 고정 휴업일로 처리하고, 방학 시작·종료일 근처의 재량휴업일은 피하도록 보정합니다.`;

  $('resultArea').innerHTML=`
    <div class="stats">
      <div class="stat hl"><div class="k">평균 망각지수</div><div class="v">${res.baseRisk.toFixed(3)}</div></div>
      <div class="stat warn"><div class="k">최종 목적함수</div><div class="v">${res.fitness.toFixed(3)}</div></div>
      <div class="stat"><div class="k">수업일 / 고정휴업</div><div class="v">${classDays}<small> / ${nWeek+nHoliday}일</small></div></div>
    </div>
    <div class="stats">
      <div class="stat"><div class="k">방학 인접 회피</div><div class="v">${res.social.nearVacCount}<small>일 · +${res.social.vacPenalty.toFixed(2)}</small></div></div>
      <div class="stat"><div class="k">재량휴업 / 가능평일</div><div class="v">${nRest}<small> / ${nFlex}일</small></div></div>
      <div class="stat"><div class="k">주말 / 국가공휴일</div><div class="v">${nWeek}<small> / ${nHoliday}일</small></div></div>
    </div>

    <div class="cal-legend">
      <div class="lg"><span class="sw" style="background:var(--ink);border:1px solid var(--line)"></span>수업일</div>
      <div class="lg"><span class="sw" style="background:#2b3445"></span>주말(고정 휴업)</div>
      <div class="lg"><span class="sw" style="background:rgba(61,214,196,.32)"></span>국가공휴일(고정 휴업)</div>
      <div class="lg"><span class="sw" style="background:var(--amber)"></span>재량휴업일</div>
      <div class="lg"><span class="sw" style="background:rgba(157,140,255,.4)"></span>방학(제외)</div>
    </div>
    <div class="cal-grid">${calHTML}</div>

    <div class="disc-list">
      <h4>배치된 재량휴업일 ${discDays.length}일</h4>
      <div class="chips">${chips||'<span style="color:var(--txt-faint);font-size:13px">없음</span>'}</div>
    </div>
    <div class="note">${noteText}<br><br><b>점수식</b> = 평균 망각지수 ${res.baseRisk.toFixed(3)} + 방학 인접 패널티 ${res.social.vacPenalty.toFixed(3)} = 최종 목적함수 ${res.fitness.toFixed(3)}</div>`;
}

/* ---------- 실행 ---------- */
$('runBtn').addEventListener('click',async()=>{
  clearErr();
  const year=parseInt($('year').value);
  const nRest=parseInt($('restSlider').value);
  if(!year||year<2000||year>2100){ showErr('연도를 올바르게 입력하세요.'); return; }

 const wrongYearVacs = vacations.filter(v =>
  !v.start.startsWith(String(year) + '-') ||
  !v.end.startsWith(String(year) + '-')
);

if(wrongYearVacs.length){
  showErr(`${year}년으로 탐색하려면 방학 기간도 ${year}년 날짜로 입력해야 합니다.`);
  return;
}
  const cal=buildCalendar(year,vacs,holidays);
  const nFlex=cal.filter(c=>c.flexible).length;
  if(nRest>nFlex){ showErr(`재량휴업일(${nRest}일)이 배치 가능한 평일(${nFlex}일)보다 많습니다.`); return; }

  const btn=$('runBtn'); btn.disabled=true; btn.textContent='⟳ 진화 중…';
  $('progWrap').classList.add('show');

  try{
    const currentPref=pref();
    const res=await runGA(cal,nRest,objective,currentPref,(gen,tot,best)=>{
      $('progFill').style.width=(gen/tot*100)+'%';
      $('progGen').textContent=`세대 ${gen} / ${tot}`;
      $('progBest').textContent=`최저 목적함수 ${best.toFixed(4)}`;
    });
    renderResult(res,cal,year,nRest,objective);
  }catch(err){
    showErr(err.message);
    $('resultArea').innerHTML='';
  }finally{
    btn.disabled=false; btn.textContent='⟐ 최적 일정 탐색 시작';
    setTimeout(()=>$('progWrap').classList.remove('show'),600);
  }
});
</script>
</body>
</html>
'''
components.html(
    HTML_CODE,
    height=1600,
    scrolling=True,
)
