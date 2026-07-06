import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime

st.set_page_config(page_title="AGROVA", layout="wide", page_icon="🌾", initial_sidebar_state="expanded")

# Ensure dark_mode always exists in session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ── Dark mode query-param sync ──────────────────────────────────
# The header iframe button sets ?dm=1 or ?dm=0. Python reads it
# here (before any UI renders), stores it in session_state, clears
# the param, then calls st.rerun() — a Python-side rerun that keeps
# the session alive, so the toggle works reliably in both directions.
_dm_param = st.query_params.get("dm")
if _dm_param is not None:
    st.session_state.dark_mode = (_dm_param == "1")
    st.query_params.clear()
    st.rerun()

# ══════════════════════════════════════════════════════════════
# DESIGN SYSTEM — single source of truth for color/spacing/type
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
:root{
  --ink:#16302b; --ink-soft:#3f5b54; --muted:#6b8079;
  --surface:#ffffff; --bg:#f4faf8; --bg-alt:#eaf4f1;
  --brand:#0f6b5c; --brand-dark:#0a4a40; --brand-light:#3f9c88;
  --accent:#c98a2e; --accent2:#e63946; --accent3:#2176ae; --accent4:#2d936c;
  --danger:#b3261e; --danger-bg:#fdecea;
  --warn:#a86a00; --warn-bg:#fff6e5; --ok:#1e7d4a; --ok-bg:#e8f6ee;
  --info:#1a5f8a; --info-bg:#e9f4fb;
  --border:#d7e6e1; --radius:14px; --radius-sm:8px;
  --shadow:0 2px 4px rgba(16,48,42,.07),0 6px 20px rgba(16,48,42,.08);
  --shadow-lg:0 4px 8px rgba(16,48,42,.1),0 12px 32px rgba(16,48,42,.1);
}
/* Full-width — no max-width cap, stretches to any screen ratio */
.block-container{
  padding-top:3.5rem !important;
  padding-bottom:4rem !important;
  max-width:100% !important;
  width:100% !important;
  padding-left:3rem !important;
  padding-right:3rem !important;
  min-height:100vh !important;
  box-sizing:border-box !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main{
  max-width:100% !important;
  width:100% !important;
  padding:0 !important;
  min-height:100vh !important;
}
/* ── Hide only specific Streamlit chrome, never the sidebar ──────── */
[data-testid="stColorBlock"],
[data-testid="stToolbarActionButtonIcon"],
[data-testid="stMainMenuButton"],
[data-testid="stActionButtonIcon"],
[data-testid="stToolbarActions"],
button[title="View app in fullscreen"],
button[title="Open settings"] { display:none !important; }

/* Header stays fully visible and interactive for sidebar arrow */
header[data-testid="stHeader"] {
  background:transparent !important;
}
/* Sidebar collapse/expand arrow — always visible and clickable */
[data-testid="stSidebarCollapsedControl"] {
  display:flex !important;
  visibility:visible !important;
  pointer-events:all !important;
  background:#0a4a40 !important;
}
/* Sidebar itself — always visible */
section[data-testid="stSidebar"] {
  display:flex !important;
  visibility:visible !important;
}

/* Light mode — cover every wrapper */
html,body{background:#f4faf8 !important; min-height:100vh; width:100%;}
.stApp,.stApp>div,.stApp>div>div,.stApp>div>div>div,
section.main,section.main>div,.main .block-container,
[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>div,
[data-testid="stAppViewBlockContainer"]{background:#f4faf8 !important;}
/* Collapsed sidebar strip */
[data-testid="stSidebarCollapsedControl"]{background:#0a4a40 !important;}
header[data-testid="stHeader"]{background:transparent !important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,var(--brand-dark),#0d5347) !important;}
section[data-testid="stSidebar"] *{color:#dcefe9 !important;}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3{color:#ffffff !important;}
section[data-testid="stSidebar"] label{color:#b7d9cf !important; font-weight:500 !important; font-size:.82rem !important;}

h1,h2,h3,h4{color:var(--ink) !important; font-weight:700 !important; letter-spacing:-.01em;}
p,span,div,td,th,li{color:var(--ink-soft);}
/* Adaptive text — elements with an explicit background get forced contrast */
[style*="background:#0"],[style*="background:rgb(0"]{color:#f0faf7 !important;}
[style*="background:#f"],[style*="background:#e"],[style*="background:#d"],[style*="background:rgb(2"]{color:#16302b !important;}

.stTabs [data-baseweb="tab-list"]{gap:4px; border-bottom:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{
  height:44px; padding:0 18px; border-radius:10px 10px 0 0; background:transparent;
  color:var(--muted) !important; font-weight:600 !important; font-size:.92rem !important;
}
.stTabs [aria-selected="true"]{background:var(--surface) !important; color:var(--brand) !important; box-shadow:0 -2px 0 var(--brand) inset;}

.stButton>button{
  background:var(--brand) !important; color:#ffffff !important; border:none !important;
  border-radius:var(--radius-sm) !important; font-weight:600 !important; font-size:.88rem !important;
  padding:.5rem 1rem !important; box-shadow:none !important; transition:background .22s ease, color .22s ease, box-shadow .22s ease, transform .12s ease;
}
.stButton>button:hover{background:var(--brand-dark) !important; color:#ffffff !important;}
.stButton>button p,.stButton>button span,.stButton>button div{color:#ffffff !important;}

/* Dark mode toggle — compact, left-aligned under subtitle */
div[data-testid="stHorizontalBlock"] > div:first-child .st-key-dm_toggle > button {
  font-size:.75rem !important;
  padding:.3rem .9rem !important;
  width:auto !important;
  display:inline-block !important;
}

.stMetric{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:.7rem .9rem;}
.stMetric label{color:var(--muted) !important; font-weight:600 !important; font-size:.72rem !important; text-transform:uppercase; letter-spacing:.04em;}
.stMetric [data-testid="stMetricValue"]{color:var(--ink) !important; font-weight:700 !important;}
hr{border:none !important; border-top:1px solid var(--border) !important; margin:1.1rem 0 !important;}

/* PPT-style cards — top accent bar + stronger shadow */
.av-card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:1.15rem 1.3rem; box-shadow:var(--shadow); margin:.5rem 0; border-top:3px solid var(--brand);}
.av-card h4{margin:0 0 .6rem 0 !important; font-size:.92rem !important; font-weight:700 !important; display:flex; align-items:center; gap:.4rem; color:var(--ink) !important;}
.av-card p{margin:.3rem 0 !important; font-size:.87rem !important; line-height:1.55;}
.av-card strong{color:var(--ink) !important; font-weight:700;}
.av-tone-brand{border-top-color:var(--brand);}
.av-tone-danger{border-top-color:var(--accent2); background:var(--danger-bg);}
.av-tone-warn{border-top-color:var(--accent); background:var(--warn-bg);}
.av-tone-ok{border-top-color:var(--ok); background:var(--ok-bg);}
.av-tone-info{border-top-color:var(--accent3); background:var(--info-bg);}

/* PPT-inspired section labels */
.av-section{margin:1.8rem 0 .8rem 0; padding-bottom:.5rem; animation:av-fadein .28s ease-out;}
@keyframes av-fadein{from{opacity:0; transform:translateY(6px);} to{opacity:1; transform:translateY(0);}}
.av-section h3{
  margin:0 !important; font-size:.72rem !important; font-weight:800 !important;
  letter-spacing:.12em !important; text-transform:uppercase !important;
  color:var(--accent2) !important; border-bottom:2px solid var(--border); padding-bottom:.5rem;
}
.av-section .av-sub{color:var(--muted); font-size:.82rem; margin-top:.3rem; font-weight:400; text-transform:none; letter-spacing:0;}

/* PPT stat accent numbers in metrics */
.stMetric{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:.75rem 1rem; box-shadow:var(--shadow); border-top:3px solid var(--brand);}
.stMetric label{color:var(--muted) !important; font-weight:700 !important; font-size:.68rem !important; text-transform:uppercase; letter-spacing:.07em;}
.stMetric [data-testid="stMetricValue"]{color:var(--brand) !important; font-weight:800 !important; font-size:1.35rem !important;}
.stMetric [data-testid="stMetricDelta"] svg{display:none;}

.av-progress-track{background:var(--bg-alt); border-radius:999px; height:10px; overflow:hidden;}
.av-progress-fill{height:10px; border-radius:999px;}

.av-crop-tile{border:1px solid var(--border); border-radius:var(--radius-sm); padding:.55rem; text-align:center; background:var(--surface); transition:border-color .22s ease, background-color .22s ease, transform .15s ease;}
/* Government scheme cards — fixed height + flex so every card in the
   grid lines up regardless of how long its description text is. */
.av-card-scheme{min-height:190px; display:flex; flex-direction:column;}
.av-card-scheme p:last-of-type{margin-top:auto !important; padding-top:.4rem;}
/* Generic equal-height card grid — used anywhere several info cards sit
   side by side (Water & Finance tab) so they all match height regardless
   of how much text each one holds. */
.av-card-grid{display:flex; flex-direction:column; margin:0 !important;}
.av-crop-tile.sel{border-color:var(--brand); background:var(--bg-alt);}
.av-crop-tile .rank{font-size:.68rem; color:var(--muted); font-weight:700;}
.av-crop-tile .name{font-size:.82rem; font-weight:700; color:var(--ink);}
.av-crop-tile .score{font-size:.72rem; color:var(--brand);}

.av-chat-user{background:var(--bg-alt); border-radius:var(--radius-sm); padding:.6rem .9rem; margin:.35rem 0; font-size:.88rem;}
.av-chat-bot{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:.6rem .9rem; margin:.35rem 0; font-size:.88rem;}

.av-hero{background:linear-gradient(135deg,var(--brand-dark) 0%,var(--brand) 60%,var(--brand-light) 100%); border-radius:20px; padding:2.8rem 2rem; text-align:center; color:#fff; margin-bottom:1.4rem; box-shadow:var(--shadow-lg); position:relative; overflow:hidden;}
.av-hero::before{content:'';position:absolute;top:-40px;right:-40px;width:180px;height:180px;background:rgba(255,255,255,.05);border-radius:50%;}
.av-hero::after{content:'';position:absolute;bottom:-30px;left:-30px;width:120px;height:120px;background:rgba(201,138,46,.12);border-radius:50%;}
.av-hero h1,.av-hero h1 *{color:#ffffff !important; font-size:2.8rem !important; letter-spacing:-.01em; margin:0 !important; font-weight:800 !important;}
.av-hero p{color:#c8e6de !important; font-size:1rem !important; margin-top:.6rem !important;}
/* Gold accent stripe below hero title */
.av-hero-accent{display:inline-block;width:48px;height:3px;background:var(--accent);border-radius:2px;margin:.7rem auto .5rem;}

/* Pills */
.av-pill{display:inline-block;padding:.18rem .6rem;border-radius:999px;font-size:.78rem;font-weight:600;margin:.12rem .2rem;line-height:1.5;}
.av-pill-neutral{background:var(--bg-alt);color:var(--ink);border:1px solid var(--border);font-weight:600;}
.av-pill-danger{background:var(--danger-bg);color:var(--danger);}
.av-pill-warn{background:var(--warn-bg);color:var(--warn);}
.av-pill-ok{background:var(--ok-bg);color:var(--ok);}
.av-pill-info{background:var(--info-bg);color:var(--info);}

/* Crop tile buttons — ghost style */
.av-crop-tile + div .stButton>button{
  background:transparent !important; color:var(--brand) !important;
  border:1px solid var(--border) !important; font-size:.76rem !important;
  padding:.25rem .5rem !important;
}
.av-crop-tile + div .stButton>button:hover{background:var(--bg-alt) !important;}

/* Sidebar widgets */
section[data-testid="stSidebar"] .stButton>button{
  background:rgba(255,255,255,.15) !important; color:#fff !important;
  border:1px solid rgba(255,255,255,.25) !important;
}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.25) !important;}
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"]>div{
  background:rgba(255,255,255,.1) !important; border-color:rgba(255,255,255,.2) !important;
}
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"]{
  background:var(--accent) !important;
}
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"]{background:rgba(255,255,255,.2) !important;}
section[data-testid="stSidebar"] .stNumberInput input{
  background:rgba(255,255,255,.18) !important; border-color:rgba(255,255,255,.35) !important;
  color:#ffffff !important; font-weight:600 !important;
}
/* +/- stepper buttons */
section[data-testid="stSidebar"] .stNumberInput button{
  background:rgba(255,255,255,.2) !important; color:#ffffff !important;
  border-color:rgba(255,255,255,.3) !important;
}

/* Links inside cards */
.av-card a{text-decoration:none;}
.av-card a:hover{text-decoration:underline;}

/* Selectbox in main area */
[data-baseweb="select"]>div{border-radius:var(--radius-sm) !important; border-color:var(--border) !important;}
/* Landing page language selector — always white text on dark bg since it sits on a dark card */
[data-baseweb="select"]>div,
[data-baseweb="select"] [data-baseweb="select-value"],
[data-baseweb="select"] [data-value],
[data-baseweb="select"] input,
[data-baseweb="select"] span,
[data-baseweb="select"] p {
  color:#ffffff !important;
  background:#1e2d28 !important;
}
[data-baseweb="select"] svg { fill:#ffffff !important; }
/* Dropdown options list */
[data-baseweb="popover"] [role="option"]{color:#ffffff !important; background:#1e2d28 !important;}
[data-baseweb="popover"] [role="option"]:hover{background:#2d4a42 !important; color:#ffffff !important;}
[data-baseweb="menu"] { background:#1e2d28 !important; }

/* ── DARK MODE — watches Streamlit's own --background-color CSS var ── */
html[data-av-dark="1"]{
  --ink:#dff0ea; --ink-soft:#b8d8d0; --muted:#8ec4b8;
  --surface:#162421; --bg:#0d1a17; --bg-alt:#172820;
  --brand:#3f9c88; --brand-dark:#2d7a68;
  --border:#253d36; --shadow:0 2px 8px rgba(0,0,0,.6);
  --shadow-lg:0 4px 20px rgba(0,0,0,.7);
  --ok-bg:#0b2418; --warn-bg:#271c00; --danger-bg:#2c0c09; --info-bg:#091d2c;
  --accent2:#ff6b6b;
}
html[data-av-dark="1"],html[data-av-dark="1"] body { background:#0d1a17 !important; }
/* Kill the white right-side scrollbar/decoration strip */
html[data-av-dark="1"] [data-testid="stDecoration"],
html[data-av-dark="1"] [data-testid="stStatusWidget"],
html[data-av-dark="1"] ::-webkit-scrollbar-track { background:#0d1a17 !important; }
html[data-av-dark="1"] ::-webkit-scrollbar { background:#0d1a17 !important; }
html[data-av-dark="1"] ::-webkit-scrollbar-thumb { background:#253d36 !important; border-radius:4px; }
html[data-av-dark="1"] *:not(svg):not(path):not(circle):not(rect):not(img):not(.av-card):not(.av-tone-danger):not(.av-tone-warn):not(.av-tone-ok):not(.av-tone-info):not(.av-hero):not(.av-progress-fill):not(.av-crop-tile):not(.stButton>button):not([class*="av-pill"]) {
  background-color:#0d1a17 !important;
}
html[data-av-dark="1"] .av-card { background:#162421 !important; }
html[data-av-dark="1"] .av-tone-danger { background:#2c0c09 !important; }
html[data-av-dark="1"] .av-tone-warn { background:#271c00 !important; }
html[data-av-dark="1"] .av-tone-ok { background:#0b2418 !important; }
html[data-av-dark="1"] .av-tone-info { background:#091d2c !important; }
html[data-av-dark="1"] .av-chat-user { background:#172820 !important; }
html[data-av-dark="1"] .av-chat-bot { background:#162421 !important; }
html[data-av-dark="1"] .stMetric { background:#1e3530 !important; }
html[data-av-dark="1"] .stButton>button { background:#2d7a68 !important; }
html[data-av-dark="1"] [data-testid="stSidebarCollapsedControl"],
html[data-av-dark="1"] [data-testid="stSidebarCollapsedControl"]>* { background:#071410 !important; }
html[data-av-dark="1"] section[data-testid="stSidebar"],
html[data-av-dark="1"] section[data-testid="stSidebar"]>div { background:linear-gradient(180deg,#071410,#0c1e1a) !important; }
html[data-av-dark="1"] section[data-testid="stSidebar"]{ background:linear-gradient(180deg,#071410,#0c1e1a) !important; }
html[data-av-dark="1"] .av-card         { background:#162421 !important; border-color:#253d36 !important; }
html[data-av-dark="1"] .stMetric        { background:#162421 !important; border-color:#253d36 !important; }
html[data-av-dark="1"] .stTabs [data-baseweb="tab-list"] { background:#0d1a17 !important; border-color:#253d36 !important; }
html[data-av-dark="1"] .stTabs [aria-selected="true"]    { background:#162421 !important; }
html[data-av-dark="1"] p,html[data-av-dark="1"] span,html[data-av-dark="1"] td,
html[data-av-dark="1"] th,html[data-av-dark="1"] li      { color:#9ec4bb !important; }
html[data-av-dark="1"] h1,html[data-av-dark="1"] h2,
html[data-av-dark="1"] h3,html[data-av-dark="1"] h4      { color:#dff0ea !important; }
html[data-av-dark="1"] strong                             { color:#dff0ea !important; }
html[data-av-dark="1"] [data-baseweb="select"]>div       { background:#162421 !important; border-color:#253d36 !important; color:#dff0ea !important; }
html[data-av-dark="1"] input,html[data-av-dark="1"] textarea { background:#162421 !important; color:#dff0ea !important; border-color:#253d36 !important; }
html[data-av-dark="1"] [data-testid="stSlider"] [data-testid="stTickBar"] { background:#253d36 !important; }
html[data-av-dark="1"] .stButton>button { background:#2d7a68 !important; }
/* Chat sticky bar */
html[data-av-dark="1"] [data-testid="stBottom"],
html[data-av-dark="1"] [data-testid="stBottom"] *,
html[data-av-dark="1"] [data-testid="stChatInputContainer"],
html[data-av-dark="1"] [data-testid="stChatInputContainer"] * { background:#0d1a17 !important; border-color:#253d36 !important; }
html[data-av-dark="1"] [data-testid="stChatInput"] textarea,
html[data-av-dark="1"] [data-testid="stChatInputTextArea"] { background:#162421 !important; color:#dff0ea !important; }
/* Sidebar collapsed control strip */
html[data-av-dark="1"] [data-testid="stSidebarCollapsedControl"],
html[data-av-dark="1"] [data-testid="collapsedControl"],
html[data-av-dark="1"] button[data-testid="baseButton-headerNoPadding"],
html[data-av-dark="1"] section[data-testid="stSidebarCollapsedControl"] { background:#0d1a17 !important; border-color:#253d36 !important; }
/* Catch-all: any white div directly under stApp */
html[data-av-dark="1"] .stApp>div { background:#0d1a17 !important; }
/* Force all card body text readable in dark mode */
html[data-av-dark="1"] .av-card p { color:#b8d8d0 !important; }
html[data-av-dark="1"] .av-card strong { color:#dff0ea !important; }
html[data-av-dark="1"] table td, html[data-av-dark="1"] table th { color:#b8d8d0 !important; }
</style>""", unsafe_allow_html=True)

st.markdown("""<script>
(function(){
  var html = document.documentElement;
  var DARK = '#0d1a17';
  var LIGHT = '#f4faf8';
  var isDark = false;

  var outerSelectors = [
    'body','html','#root',
    '.stApp','.stApp>div','.stApp>div>div','.stApp>div>div>div',
    '[data-testid="stAppViewContainer"]',
    '[data-testid="stAppViewContainer"]>div',
    '[data-testid="stAppViewContainer"]>div>div',
    '[data-testid="stAppViewBlockContainer"]',
    'section.main','section.main>div','section.main>div>div',
    '.main','.block-container'
  ];

  function paintOuter(dark){
    var color = dark ? DARK : LIGHT;
    document.querySelectorAll(outerSelectors.join(',')).forEach(function(el){
      el.style.setProperty('background-color', color, 'important');
      el.style.setProperty('background', color, 'important');
      el.style.setProperty('max-width', '100%', 'important');
      el.style.setProperty('width', '100%', 'important');
      el.style.setProperty('min-height', '100vh', 'important');
    });
    document.body.style.setProperty('background', color, 'important');
    html.style.setProperty('background', color, 'important');
    html.style.setProperty('min-height', '100vh', 'important');
  }

  function applyDark(on){
    isDark = on;
    html.setAttribute('data-av-dark', on ? '1' : '0');
    paintOuter(on);
  }

  function detect(){
    var c = getComputedStyle(html).getPropertyValue('--background-color').trim();
    if(c){ applyDark(c === '#0e1117' || c === '#0E1117'); return; }
    var app = document.querySelector('.stApp');
    if(app){
      var bg = getComputedStyle(app).backgroundColor;
      var m = bg.match(/[0-9]+/g);
      if(m){ applyDark(parseInt(m[0]) < 30); return; }
    }
    applyDark(window.matchMedia('(prefers-color-scheme:dark)').matches);
  }

  // ── Tab persistence across reruns ──────────────────────────
  var tabRestored = false;
  function saveTabs(){
    var tabs = document.querySelectorAll('[data-baseweb="tab"]');
    tabs.forEach(function(tab, i){
      tab.addEventListener('click', function(){
        localStorage.setItem('agrova_active_tab', i);
        tabRestored = true;
      });
    });
  }
  function restoreTab(){
    if(tabRestored) return;
    var idx = localStorage.getItem('agrova_active_tab');
    if(!idx || idx === '0') return;
    var tabs = document.querySelectorAll('[data-baseweb="tab"]');
    if(tabs[idx]){
      tabs[idx].click();
      tabRestored = true;
    }
  }
  // Wire up after DOM is ready
  setTimeout(function(){
    saveTabs();
    restoreTab();
  }, 400);
  // Re-wire after each rerun AND instantly repaint so no white flash
  new MutationObserver(function(){
    saveTabs();
    if(!tabRestored) restoreTab();
    paintOuter(isDark);  // repaint immediately on every DOM change
  }).observe(document.body, {childList:true, subtree:true});

  detect();
  new MutationObserver(detect).observe(html, {attributes:true, attributeFilter:['style']});
  setInterval(function(){ detect(); paintOuter(isDark); }, 100);
  window.matchMedia('(prefers-color-scheme:dark)').addEventListener('change', detect);
})();
</script>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LANGUAGES
# ══════════════════════════════════════════════════════════════
LANGS = ["English","Hindi","Bengali","Telugu","Marathi","Tamil","Urdu","Gujarati","Kannada","Odia",
         "Malayalam","Punjabi","Assamese","Maithili","Sanskrit","Kashmiri","Nepali","Sindhi",
         "Konkani","Dogri","Manipuri","Bodo"]

CONFIDENT_LANGS = {"English","Hindi","Bengali","Telugu","Marathi","Tamil","Gujarati","Kannada",
                    "Malayalam","Punjabi","Urdu","Odia","Assamese","Nepali","Sanskrit","Konkani"}
BEST_EFFORT_LANGS = {"Maithili","Kashmiri","Sindhi","Dogri","Manipuri","Bodo"}

LANG_NAMES = {
    "English":"English","Hindi":"हिंदी","Bengali":"বাংলা","Telugu":"తెలుగు","Marathi":"मराठी",
    "Tamil":"தமிழ்","Urdu":"اردو","Gujarati":"ગુજરાતી","Kannada":"ಕನ್ನಡ","Odia":"ଓଡ଼ିଆ",
    "Malayalam":"മലയാളം","Punjabi":"ਪੰਜਾਬੀ","Assamese":"অসমীয়া","Maithili":"मैथिली",
    "Sanskrit":"संस्कृतम्","Kashmiri":"کٲشُر","Nepali":"नेपाली","Sindhi":"سنڌي",
    "Konkani":"कोंकणी","Dogri":"डोगरी","Manipuri":"মৈতৈলোন্","Bodo":"बड़ो",
}

INDIAN_STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
    "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
    "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
    "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
    "Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Andaman & Nicobar","Chandigarh","Dadra & Nagar Haveli","Daman & Diu",
    "Delhi","Jammu & Kashmir","Ladakh","Lakshadweep","Puducherry"
]

def M(*vals):
    """Build a {lang: value} dict from 22 positional values in LANGS order."""
    return dict(zip(LANGS, vals))

# ══════════════════════════════════════════════════════════════
# UI LABELS — real translations, ordered to match LANGS
# en, hi, bn, te, mr, ta, ur, gu, kn, or, ml, pa, as, mai, sa, ks, ne, sd, kok, doi, mni, bodo
# ══════════════════════════════════════════════════════════════
TX = {
"app_title": M("AGROVA — AI Precision Farming","AGROVA — एआई सटीक कृषि","AGROVA — এআই নির্ভুল কৃষি","AGROVA — AI ఖచ్చిత వ్యవసాయం","AGROVA — एआय अचूक शेती","AGROVA — AI துல்லிய விவசாயம்","AGROVA — اے آئی درست زراعت","AGROVA — AI ચોક્કસ ખેતી","AGROVA — AI ನಿಖರ ಕೃಷಿ","AGROVA — AI ସଠିକ ଚାଷ","AGROVA — AI കൃത്യ കൃഷി","AGROVA — AI ਸਟੀਕ ਖੇਤੀ","AGROVA — এআই সঠিক কৃষি","AGROVA — एआई सटीक कृषि","AGROVA — कृत्रिमबुद्धि कृषिः","AGROVA — اے آئی زراعت","AGROVA — एआई सटीक खेती","AGROVA — اي آء زراعت","AGROVA — एआय अचूक शेती","AGROVA — एआई सटीक कृषि","AGROVA — AI ꯈꯨꯗꯝ ꯂꯧꯅ","AGROVA — एआई सटीक खेती"),
"app_sub": M("50 Crops · 22 Languages · Crop Loss Estimator · Planting Guide · Govt Schemes","50 फसलें · 22 भाषाएं · फसल हानि आकलन · बुवाई गाइड · सरकारी योजनाएं","৫০ ফসল · ২২ ভাষা · ফসল ক্ষতি নিরূপণ · রোপণ গাইড · সরকারি প্রকল্প","50 పంటలు · 22 భాషలు · పంట నష్ట అంచనా · నాటు మార్గదర్శి · ప్రభుత్వ పథకాలు","५० पिके · २२ भाषा · पीक नुकसान अंदाज · लागवड मार्गदर्शन · सरकारी योजना","50 பயிர்கள் · 22 மொழிகள் · பயிர் இழப்பு மதிப்பீடு · நடவு வழிகாட்டி · அரசு திட்டங்கள்","50 فصلیں · 22 زبانیں · فصل نقصان تخمینہ · کاشت رہنمائی · سرکاری اسکیمیں","50 પાક · 22 ભાષાઓ · પાક નુકસાન અંદાજ · વાવેતર માર્ગદર્શિકા · સરકારી યોજનાઓ","50 ಬೆಳೆಗಳು · 22 ಭಾಷೆಗಳು · ಬೆಳೆ ನಷ್ಟ ಅಂದಾಜು · ನಾಟಿ ಮಾರ್ಗದರ್ಶಿ · ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು","50 ଫସଲ · 22 ଭାଷା · ଫସଲ କ୍ଷତି ଆକଳନ · ଚାଷ ଗାଇଡ · ସରକାରୀ ଯୋଜନା","50 വിളകൾ · 22 ഭാഷകൾ · വിള നഷ്ട കണക്ക് · നടീൽ ഗൈഡ് · സർക്കാർ പദ്ധതികൾ","50 ਫਸਲਾਂ · 22 ਭਾਸ਼ਾਵਾਂ · ਫਸਲ ਨੁਕਸਾਨ ਅੰਦਾਜ਼ਾ · ਬਿਜਾਈ ਗਾਈਡ · ਸਰਕਾਰੀ ਸਕੀਮਾਂ","৫০ শস্য · ২২ ভাষা · শস্য ক্ষতি নিৰূপণ · ৰোপণ গাইড · চৰকাৰী আঁচনি","५० फसल · २२ भाषा · फसल हानि आकलन · बुआई गाइड · सरकारी योजना","पञ्चाशत् शस्यानि · द्वाविंशति भाषाः · हानि आकलनम् · रोपण मार्गदर्शिका · सरकारी योजनाः","50 فصلاں · 22 زبانہٕ · نقصان اندازہ · کاشت رہنمائی · سرکاری اسکیمہٕ","५० बाली · २२ भाषाहरू · बाली नोक्सान अनुमान · खेती गाइड · सरकारी योजना","50 فصلون · 22 ٻوليون · نقصان اندازو · پوک رهنمائي · سرڪاري اسڪيمون","५० पिकां · २२ भासा · नुकसान अंदाज · लागवड मार्गदर्शन · सरकारी येवजण्यो","५० फसलां · २२ भाशां · फसल नुकसान अंदाजा · बूआई गाइड · सरकारी योजनां","ꯐꯥꯎꯕꯥ 50 · ꯃꯄꯨꯡ 22 · ꯐꯥꯎꯕꯥ ꯑꯃꯦꯑꯨꯡ ꯈꯪꯅꯕ · ꯁꯤꯡ ꯃꯆꯥꯛ · ꯁꯔꯀꯥꯔ ꯗꯦ ꯍꯦꯟꯐꯝ","५० फसलां · २२ भाषा · फसल नुकसान अंदाजा · खेती गाइड · सरकारी योजना"),
"enter_btn": M("Enter AGROVA","AGROVA में प्रवेश करें","AGROVA-তে প্রবেশ","AGROVA లోకి ప్రవేశించండి","AGROVA मध्ये प्रवेश करा","AGROVA-ல் நுழையவும்","AGROVA میں داخل ہوں","AGROVA માં પ્રવેશ કરો","AGROVA ಗೆ ಪ್ರವೇಶಿಸಿ","AGROVA ରେ ପ୍ରବେଶ କରନ୍ତୁ","AGROVA-ൽ പ്രവേശിക്കുക","AGROVA ਵਿੱਚ ਦਾਖਲ ਹੋਵੋ","AGROVA ত প্ৰৱেশ কৰক","AGROVA में प्रवेश करू","AGROVA प्रविशतु","AGROVA منز داخل گژھیو","AGROVA मा प्रवेश गर्नुहोस्","AGROVA ۾ داخل ٿيو","AGROVA ात प्रवेश करचो","AGROVA च दाखल हो","AGROVA ꯗ ꯆꯪꯕ","AGROVA आव नोसो"),
"change_lang": M("Change Language","भाषा बदलें","ভাষা পরিবর্তন","భాష మార్చు","भाषा बदला","மொழி மாற்று","زبان تبدیل کریں","ભાષા બદલો","ಭಾಷೆ ಬದಲಿಸಿ","ଭାଷା ବଦଳାନ୍ତୁ","ഭാഷ മാറ്റുക","ਭਾਸ਼ਾ ਬਦਲੋ","ভাষা সলনি কৰক","भाषा बदलू","भाषां परिवर्तयतु","زبان بدلاو","भाषा परिवर्तन गर्नुहोस्","ٻولي بدلايو","भास बदल","भाशा बदलो","ꯃꯄꯨꯡ ꯍꯣꯡꯗꯣꯛꯎ","भाषा सोलो"),
"run_btn": M("Run Full Analysis","पूर्ण विश्लेषण चलाएं","সম্পূর্ণ বিশ্লেষণ চালান","పూర్తి విశ్లేషణ నడపండి","संपूर्ण विश्लेषण चालवा","முழு பகுப்பாய்வை இயக்கு","مکمل تجزیہ چلائیں","સંપૂર્ણ વિશ્લેષણ ચલાવો","ಸಂಪೂರ್ಣ ವಿಶ್ಲೇಷಣೆ ರನ್ ಮಾಡಿ","ସମ୍ପୂର୍ଣ୍ଣ ବିଶ୍ଳେଷଣ ଚଲାନ୍ତୁ","പൂർണ്ണ വിശകലനം നടത്തുക","ਪੂਰਾ ਵਿਸ਼ਲੇਸ਼ਣ ਚਲਾਓ","সম্পূৰ্ণ বিশ্লেষণ চলাওক","पूर्ण विश्लेषण चलाबू","सम्पूर्णं विश्लेषणं चालयतु","مکمل تجزیہ چلاو","पूर्ण विश्लेषण चलाउनुहोस्","مڪمل تجزيو هلايو","पुराय विश्लेषण चलय","पूरा विश्लेषण चलाओ","ꯐꯨꯜ ꯑꯅꯦꯂꯤꯁꯤꯁ ꯆꯠꯅꯕ","पूरा विश्लेषण चलाव"),
"tab_dashboard": M("Dashboard","डैशबोर्ड","ড্যাশবোর্ড","డాష్‌బోర్డ్","डॅशबोर्ड","டாஷ்போர்டு","ڈیش بورڈ","ડેશબોર્ડ","ಡ್ಯಾಶ್‌ಬೋರ್ಡ್","ଡ୍ୟାସବୋର୍ଡ","ഡാഷ്ബോർഡ്","ਡੈਸ਼ਬੋਰਡ","ড্যাশব’ৰ্ড","डैशबोर्ड","संकेतफलकम्","ڈیش بورڈ","ड्यासबोर्ड","ڊيش بورڊ","डॅशबोर्ड","डैशबोर्ड","ꯗꯦꯁ ꯕꯣꯔꯗ","डैशबोर्ड"),
"tab_advisor": M("Crop Advisor","फसल सलाहकार","ফসল পরামর্শদাতা","పంట సలహాదారు","पीक सल्लागार","பயிர் ஆலோசகர்","فصل مشیر","પાક સલાહકાર","ಬೆಳೆ ಸಲಹೆಗಾರ","ଫସଲ ପରାମର୍ଶଦାତା","വിള ഉപദേഷ്ടാവ്","ਫਸਲ ਸਲਾਹਕਾਰ","শস্য পৰামৰ্শদাতা","फसल सलाहकार","शस्य परामर्शदाता","فصل صلاحکار","बाली सल्लाहकार","فصل صلاحڪار","पीक सल्लागार","फसल सलाहकार","ꯐꯥꯎꯕꯥ ꯄꯥꯎꯖꯦꯜ","फसल सल्लाहकार"),
"tab_finance": M("Water & Finance","पानी और वित्त","জল ও অর্থ","నీరు & ఆర్థిక","पाणी व वित्त","நீர் & நிதி","پانی اور مالیات","પાણી અને નાણાં","ನೀರು & ಹಣಕಾಸು","ପାଣି ଓ ଅର୍ଥ","ജലവും ധനവും","ਪਾਣੀ ਅਤੇ ਵਿੱਤ","পানী আৰু বিত্ত","पानि आ वित्त","जल-अर्थ","آب تہٕ مالیات","पानी र वित्त","پاڻي ۽ پيسا","उदक व अर्थ","पानी ते वित्त","ꯏꯁꯤꯡ ꯑꯃꯁꯨꯡ ꯁꯦꯜ","पानी अर सेल"),
"tab_schemes": M("Govt Schemes","सरकारी योजनाएं","সরকারি প্রকল্প","ప్రభుత్వ పథకాలు","सरकारी योजना","அரசு திட்டங்கள்","سرکاری اسکیمیں","સરકારી યોજનાઓ","ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು","ସରକାରୀ ଯୋଜନା","സർക്കാർ പദ്ധതികൾ","ਸਰਕਾਰੀ ਸਕੀਮਾਂ","চৰকাৰী আঁচনি","सरकारी योजना","सरकारी योजनाः","سرکاری اسکیمہٕ","सरकारी योजना","سرڪاري اسڪيمون","सरकारी येवजण्यो","सरकारी योजनां","ꯁꯔꯀꯥꯔ ꯗꯦ ꯍꯦꯟꯐꯝ","सरकारी योजना"),
"tab_chat": M("Ask AGROVA","AGROVA से पूछें","AGROVA-কে জিজ্ঞাসা","AGROVAని అడగండి","AGROVA ला विचारा","AGROVA-விடம் கேளுங்கள்","AGROVA سے پوچھیں","AGROVA ને પૂછો","AGROVA ಗೆ ಕೇಳಿ","AGROVA କୁ ପଚାରନ୍ତୁ","AGROVA-യോട് ചോദിക്കുക","AGROVA ਨੂੰ ਪੁੱਛੋ","AGROVA ক সোধক","AGROVA सँ पुछू","AGROVA पृच्छतु","AGROVA پؤچھیو","AGROVA लाई सोध्नुहोस्","AGROVA کان پڇو","AGROVA क विचार","AGROVA थमां पुछो","AGROVA ꯗ ꯍꯪꯕ","AGROVA था हांख"),
"soil":M("Soil Moisture","मिट्टी की नमी","মাটির আর্দ্রতা","నేల తేమ","मातीतील ओलावा","மண் ஈரப்பதம்","مٹی کی نمی","જમીનની ભેજ","ಮಣ್ಣಿನ ತೇವ","ମାଟି ଆର୍ଦ୍ରତା","മണ്ണ് ഈർപ്പം","ਮਿੱਟੀ ਦੀ ਨਮੀ","মাটিৰ আৰ্দ্ৰতা","माटिक नमी","भूमि आर्द्रता","مٹی نمی","माटोको आर्द्रता","مٽي جي نمي","माती ओलावो","मिट्टी नमी","ꯂꯩ ꯅꯨꯡꯥꯏ","माटि नमी"),
"temp":M("Temperature","तापमान","তাপমাত্রা","ఉష్ణోగ్రత","तापमान","வெப்பநிலை","درجہ حرارت","તાપમાન","ತಾಪಮಾನ","ତାପମାତ୍ରା","താപനില","ਤਾਪਮਾਨ","তাপমাত্ৰা","तापमान","तापमानम्","تپمان","तापक्रम","گرمي جو درجو","तापमान","तापमान","ꯑꯇꯤꯌꯥ ꯃꯅꯨꯡ","तापमान"),
"rain":M("Rainfall","वर्षा","বৃষ্টিপাত","వర్షపాతం","पर्जन्य","மழைப்பொழிவு","بارش","વરસાદ","ಮಳೆ","ବର୍ଷା","മഴ","ਵਰਖਾ","বৰষুণ","बरखा","वृष्टिः","برشکال","वर्षा","برسات","पावस","बरखा","ꯅꯣꯡ ꯆꯨꯐꯕ","बरखा"),
"sun":M("Sunlight","धूप","রোদ","సూర్యకాంతి","सूर्यप्रकाश","சூரிய ஒளி","دھوپ","સૂર્યપ્રકાશ","ಸೂರ್ಯನ ಬೆಳಕು","ସୂର୍ଯ୍ୟାଲୋକ","സൂര്യപ്രകാശം","ਧੁੱਪ","ৰ’দ","धूप","सूर्यालोकः","دوپہر","घाम","سج جي روشني","सूर्यप्रकाश","धुप्प","ꯅꯨꯃꯤꯠ ꯃꯥꯡꯥꯜ","सिनसार"),
"fert":M("Fertility","उर्वरता","উর্বরতা","సారవంతం","सुपीकता","கருவளம்","زرخیزی","ફળદ્રુપતા","ಫಲವತ್ತತೆ","ଉର୍ବରତା","ഫലഭൂയിഷ്ഠത","ਉਪਜਾਊਪੁਣਾ","উৰ্বৰতা","उर्वरता","उर्वरता","زرخیزی","उर्वरता","زرخيزي","सुपीकता","उर्वरता","ꯑꯦꯍꯦꯟꯅꯕ ꯂꯩ","उर्वरता"),
"gas":M("Gas / Methane","गैस / मीथेन","গ্যাস / মিথেন","గ్యాస్ / మీథేన్","वायू / मिथेन","எரிவாயு / மீத்தேன்","گیس / میتھین","ગેસ / મિથેન","ಗ್ಯಾಸ್ / ಮೀಥೇನ್","ଗ୍ୟାସ / ମିଥେନ","വാതകം / മീഥെയ്ൻ","ਗੈਸ / ਮੀਥੇਨ","গেছ / মিথেইন","गैस / मिथेन","गैस / मिथेन","گیس / میتھین","ग्यास / मिथेन","گئس / ميٿين","गॅस / मिथेन","गैस / मिथेन","ꯒꯦꯁ / ꯃꯤꯊꯦꯟ","गैस / मिथेन"),
"humidity":M("Humidity","आर्द्रता","আর্দ্রতা","తేమ","आर्द्रता","ஈரப்பதம்","نمی","ભેજ","ಆರ್ದ್ರತೆ","ଆର୍ଦ୍ରତା","ആർദ്രത","ਨਮੀ","আৰ্দ্ৰতা","नमी","आर्द्रता","نمی","आर्द्रता","نمي","आद्रता","नमी","ꯅꯨꯡꯥꯏ","नमी"),
"wind":M("Wind Speed","हवा की गति","বায়ুর গতি","గాలి వేగం","वाऱ्याचा वेग","காற்றின் வேகம்","ہوا کی رفتار","પવનની ઝડપ","ಗಾಳಿಯ ವೇಗ","ପବନ ବେଗ","കാറ്റിന്റെ വേഗത","ਹਵਾ ਦੀ ਗਤੀ","বতাহৰ গতি","हवाक गति","वायुवेगः","ہوا رفتار","हावाको गति","هوا جي رفتار","वाऱ्याचो वेग","हवा दी गत्ती","ꯅꯨꯡꯁꯤꯠ ꯆꯠꯄ","हवा गति"),
"ph":M("Soil pH","मिट्टी pH","মাটির pH","నేల pH","माती pH","மண் pH","مٹی pH","જમીન pH","ಮಣ್ಣಿನ pH","ମାଟି pH","മണ്ണ് pH","ਮਿੱਟੀ pH","মাটিৰ pH","माटिक pH","भूमि pH","مٹی pH","माटोको pH","مٽي جو pH","माती pH","मिट्टी pH","ꯂꯩ pH","माटि pH"),
"nitrogen":M("Nitrogen","नाइट्रोजन","নাইট্রোজেন","నత్రజని","नत्रज","நைட்ரஜன்","نائٹروجن","નાઇટ્રોજન","ಸಾರಜನಕ","ନାଇଟ୍ରୋଜେନ","നൈട്രജൻ","ਨਾਈਟ੍ਰੋਜਨ","নাইট্ৰ’জেন","नाइट्रोजन","नाइट्रोजनम्","نایٹروجن","नाइट्रोजन","نائيٽروجن","नत्रज","नाइट्रोजन","ꯅꯥꯏꯇ꯭ꯔꯣꯖꯦꯟ","नाइट्रोजन"),
"farm_size":M("Farm Size (ha)","खेत का आकार (हे.)","খামারের আকার (হে.)","పొలం విస్తీర్ణం (హె.)","शेतीचा आकार (हे.)","பண்ணை அளவு (ஹெ.)","کھیت کا حجم (ہیکٹر)","ખેતરનું કદ (હે.)","ಜಮೀನಿನ ಗಾತ್ರ (ಹೆ.)","ଜମି ଆକାର (ହେ.)","കൃഷിസ്ഥലം (ഹെ.)","ਖੇਤ ਦਾ ਆਕਾਰ (ਹੈ.)","পথাৰৰ আকাৰ (হে.)","खेतक आकार (हे.)","क्षेत्रफलम् (हे.)","کھیتہ آکار (ہیکٹر)","खेतको आकार (हे.)","کيتيء جو آڪار (هيڪٽر)","शेतीचो आकार (हे.)","खेतर दा आकार (हे.)","ꯍꯧꯖꯤꯛ ꯃꯆꯥꯛ (ꯍꯦ.)","खेतर आकार (हे.)"),
"farm_type":M("Farming Type","खेती का प्रकार","চাষের ধরন","వ్యవసాయ రకం","शेतीचा प्रकार","விவசாய வகை","کاشتکاری کی قسم","ખેતીનો પ્રકાર","ಕೃಷಿ ವಿಧ","ଚାଷ ପ୍ରକାର","കൃഷി തരം","ਖੇਤੀ ਦੀ ਕਿਸਮ","খেতিৰ প্ৰকাৰ","खेतीक प्रकार","कृषि प्रकारः","کاشتکاری قسم","खेतीको प्रकार","پوک جو قسم","शेतीचो प्रकार","खेती दा किसम","ꯂꯧꯅꯕꯒꯤ ꯃꯈꯜ","खेती किसम"),
"market_dist":M("Distance to Market (km)","बाज़ार की दूरी (किमी)","বাজারের দূরত্ব (কিমি)","మార్కెట్ దూరం (కి.మీ)","बाजाराचे अंतर (किमी)","சந்தை தூரம் (கிமீ)","بازار کا فاصلہ (کلومیٹر)","બજારનું અંતર (કિમી)","ಮಾರುಕಟ್ಟೆ ದೂರ (ಕಿ.ಮೀ)","ବଜାର ଦୂରତା (କି.ମି)","മാർക്കറ്റ് ദൂരം (കി.മീ)","ਬਾਜ਼ਾਰ ਦੀ ਦੂਰੀ (ਕਿਮੀ)","বজাৰৰ দূৰত্ব (কিমি)","बजारक दूरी (किमी)","विपणि दूरत्वम् (कि.मी)","بازار دوٗری (کلومیٹر)","बजारको दूरी (किमी)","بازار جو مفاصلو (ڪلوميٽر)","बाजाराचे अंतर (किमी)","बजार दी दूरी (किमी)","ꯀꯦꯌꯥꯡꯒꯤ ꯂꯥꯞ (ꯀꯤꯃꯤ)","बजार दूरी (किमी)"),
}

TX.update({
"live_dash":M("Live Farm Dashboard","लाइव फार्म डैशबोर्ड","লাইভ ফার্ম ড্যাশবোর্ড","లైవ్ ఫార్మ్ డాష్‌బోర్డ్","लाइव्ह फार्म डॅशबोर्ड","நேரடி பண்ணை டாஷ்போர்டு","لائیو فارم ڈیش بورڈ","લાઈવ ફાર્મ ડેશબોર્ડ","ಲೈವ್ ಫಾರ್ಮ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್","ଲାଇଭ ଫାର୍ମ ଡ୍ୟାସବୋର୍ଡ","തത്സമയ ഫാം ഡാഷ്ബോർഡ്","ਲਾਈਵ ਫਾਰਮ ਡੈਸ਼ਬੋਰਡ","লাইভ ফাৰ্ম ড্যাশব’ৰ্ড","लाइव फार्म डैशबोर्ड","सजीव कृषि संकेतफलकम्","لائیو فارم ڈیش بورڈ","प्रत्यक्ष फार्म ड्यासबोर्ड","لائيو فارم ڊيش بورڊ","लाइव्ह फार्म डॅशबोर्ड","लाइव फार्म डैशबोर्ड","ꯍꯧꯖꯤꯛꯀꯤ ꯗꯦꯁ ꯕꯣꯔꯗ","लाइव फार्म डैशबोर्ड"),
"top_crops":M("Top 10 Recommended Crops","शीर्ष 10 अनुशंसित फसलें","শীর্ষ ১০ সুপারিশকৃত ফসল","టాప్ 10 సిఫారసు పంటలు","शीर्ष 10 शिफारस केलेली पिके","சிறந்த 10 பயிர்கள்","سرفہرست 10 تجویز کردہ فصلیں","ટોચ 10 ભલામણ કરેલા પાક","ಟಾಪ್ 10 ಶಿಫಾರಸು ಬೆಳೆಗಳು","ଶ୍ରେଷ୍ଠ 10 ପରାମର୍ଶିତ ଫସଲ","മികച്ച 10 വിളകൾ","ਚੋਟੀ ਦੀਆਂ 10 ਸਿਫਾਰਸ਼ੀ ਫਸਲਾਂ","শীৰ্ষ ১০ পৰামৰ্শিত শস্য","शीर्ष 10 अनुशंसित फसल","श्रेष्ठ 10 शस्यानि","سرِفہرست 10 فصلہٕ","शीर्ष 10 सिफारिस गरिएका बाली","مٿيان 10 تجويز ٿيل فصلون","वयर 10 शिफारस केल्लीं पिकां","सिखर 10 सिफारिशी फसलां","ꯑꯓꯕ ꯐꯥꯎꯕꯥ 10","सिफारिश फसलां 10"),
"crop_detail":M("Crop Details","फसल विवरण","ফসলের বিস্তারিত","పంట వివరాలు","पीक तपशील","பயிர் விவரங்கள்","فصل کی تفصیلات","પાક વિગતો","ಬೆಳೆ ವಿವರಗಳು","ଫସଲ ବିବରଣୀ","വിള വിശദാംശങ്ങൾ","ਫਸਲ ਵੇਰਵੇ","শস্যৰ বিৱৰণ","फसलक विवरण","शस्य विवरणम्","فصل تفصیل","बालीको विवरण","فصل جزيات","पिकाची म्हायती","फसल विवरण","ꯐꯥꯎꯕꯥ ꯃꯐꯝ","फसल जानकारी"),
"plant_guide":M("Planting Guide","बुवाई गाइड","রোপণ গাইড","నాటు మార్గదర్శి","लागवड मार्गदर्शन","நடவு வழிகாட்டி","کاشت رہنمائی","વાવેતર માર્ગદર્શિકા","ನಾಟಿ ಮಾರ್ಗದರ್ಶಿ","ଚାଷ ଗାଇଡ","നടീൽ ഗൈഡ്","ਬਿਜਾਈ ਗਾਈਡ","ৰোপণ গাইড","बुआई गाइड","रोपण मार्गदर्शिका","کاشت رہنمائی","रोपण गाइड","پوک رهنمائي","लागवड मार्गदर्शन","बूआई गाइड","ꯁꯤꯡ ꯃꯆꯥꯛ","बूआई गाइड"),
"crop_loss":M("Crop Loss Risk","फसल हानि जोखिम","ফসল ক্ষতির ঝুঁকি","పంట నష్ట ప్రమాదం","पीक नुकसान धोका","பயிர் இழப்பு அபாயம்","فصل نقصان کا خطرہ","પાક નુકસાનનું જોખમ","ಬೆಳೆ ನಷ್ಟ ಅಪಾಯ","ଫସଲ କ୍ଷତି ବିପଦ","വിള നഷ്ട സാധ്യത","ਫਸਲ ਨੁਕਸਾਨ ਦਾ ਖਤਰਾ","শস্য ক্ষতিৰ আশংকা","फसल हानि जोखिम","शस्य हानि जोखिमः","فصل نقصان خطرہ","बाली नोक्सान जोखिम","فصل نقصان خطرو","पीक नुकसान धोको","फसल नुकसान खतरा","ꯐꯥꯎꯕꯥ ꯃꯥꯡꯍꯟꯕꯒꯤ ꯐꯤꯕ","फसल नुकसान खतरा"),
"water_plan":M("Water & Irrigation Plan","पानी और सिंचाई योजना","জল ও সেচ পরিকল্পনা","నీరు & నీటిపారుదల ప్రణాళిక","पाणी व सिंचन योजना","நீர் & பாசன திட்டம்","پانی اور آبپاشی کا منصوبہ","પાણી અને સિંચાઈ યોજના","ನೀರು & ನೀರಾವರಿ ಯೋಜನೆ","ପାଣି ଓ ଜଳସେଚନ ଯୋଜନା","ജലവും ജലസേചന പദ്ധതിയും","ਪਾਣੀ ਅਤੇ ਸਿੰਚਾਈ ਯੋਜਨਾ","পানী আৰু জলসিঞ্চন পৰিকল্পনা","पानि आ सिंचाई योजना","जल-सिञ्चन योजना","آب تہٕ سینچہٕ منصوبہ","पानी र सिँचाइ योजना","پاڻي ۽ آبپاشي منصوبو","उदक व सिंचन येवजण","पानी ते सिंचाई योजना","ꯏꯁꯤꯡ ꯑꯃꯁꯨꯡ ꯄꯥꯟꯕ","पानी ते सिंचाई योजना"),
"financial":M("Financial Projection","वित्तीय अनुमान","আর্থিক অনুমান","ఆర్థిక అంచనా","आर्थिक अंदाज","நிதி மதிப்பீடு","مالی تخمینہ","નાણાકીય અંદાજ","ಆರ್ಥಿಕ ಅಂದಾಜು","ଆର୍ଥିକ ପୂର୍ବାନୁମାନ","സാമ്പത്തിക കണക്ക്","ਵਿੱਤੀ ਅਨੁਮਾਨ","আৰ্থিক আকলন","वित्तीय आकलन","आर्थिक अनुमानम्","مالی اندازہ","आर्थिक अनुमान","مالي اندازو","आर्थिक अंदाज","वित्ती अंदाजा","ꯁꯦꯜ ꯑꯃꯦꯑꯨꯡ ꯈꯪꯅꯕ","वित्ती अंदाजा"),
"soil_section":M("Soil Health","मिट्टी स्वास्थ्य","মাটির স্বাস্থ্য","నేల ఆరోగ్యం","माती आरोग्य","மண் ஆரோக்கியம்","مٹی کی صحت","જમીનનું આરોગ્ય","ಮಣ್ಣಿನ ಆರೋಗ್ಯ","ମାଟି ସ୍ୱାସ୍ଥ୍ୟ","മണ്ണിന്റെ ആരോഗ്യം","ਮਿੱਟੀ ਦੀ ਸਿਹਤ","মাটিৰ স্বাস্থ্য","माटिक स्वास्थ्य","भूमि आरोग्यम्","مٹی صحت","माटोको स्वास्थ्य","مٽي جي صحت","माती भलायकी","मिट्टी सेहत","ꯂꯩ ꯍꯛꯆꯪ","माटि सेहत"),
"pest_section":M("Pest & Disease Watch","कीट व रोग निगरानी","পোকা ও রোগ পর্যবেক্ষণ","పురుగు & వ్యాధి పర్యవేక్షణ","कीड व रोग निरीक्षण","பூச்சி & நோய் கண்காணிப்பு","کیڑے اور بیماری کی نگرانی","જીવાત અને રોગ દેખરેખ","ಕೀಟ ಮತ್ತು ರೋಗ ನಿಗಾ","କୀଟ ଓ ରୋଗ ନିରୀକ୍ଷଣ","കീട & രോഗ നിരീക്ഷണം","ਕੀੜੇ ਅਤੇ ਰੋਗ ਨਿਗਰਾਨੀ","কীট আৰু ৰোগ পৰ্যবেক্ষণ","कीट व रोग निगरानी","कीट रोग निरीक्षणम्","کیڑہٕ تہٕ بیمار نظر","किरा र रोग निगरानी","ڪيڙي ۽ بيماري نظر","किड व रोग निरीक्षण","कीड़े ते रोग निगरानी","ꯑꯃꯤꯅ ꯑꯃꯁꯨꯡ ꯂꯥꯏꯅ ꯌꯦꯡꯕ","कीड़े ते रोग निगरानी"),
"risk_section":M("Weather Risk Outlook","मौसम जोखिम पूर्वानुमान","আবহাওয়া ঝুঁকি পূর্বাভাস","వాతావరణ ప్రమాద అంచనా","हवामान धोका अंदाज","வானிலை ஆபத்து முன்னறிவிப்பு","موسمی خطرہ کا اندازہ","હવામાન જોખમ પૂર્વાનુમાન","ಹವಾಮಾನ ಅಪಾಯ ಮುನ್ಸೂಚನೆ","ପାଣିପାଗ ବିପଦ ପୂର୍ବାନୁମାନ","കാലാവസ്ഥാ അപകട സാധ്യത","ਮੌਸਮ ਖਤਰਾ ਅਨੁਮਾਨ","বতৰৰ আশংকা পূৰ্বানুমান","मौसम जोखिम पूर्वानुमान","वातावरण जोखिम आकलनम्","موسم خطرہ اندازہ","मौसम जोखिम पूर्वानुमान","موسمي خطرو اندازو","हवामान धोको अंदाज","मौसम खतरा अंदाजा","ꯅꯪꯃꯤꯖꯤꯡꯒꯤ ꯐꯤꯕ","मौसम खतरा अंदाजा"),
"sustain_section":M("Sustainability & Carbon","स्थिरता व कार्बन","স্থায়িত্ব ও কার্বন","సుస్థిరత & కార్బన్","शाश्वतता व कार्बन","நிலைத்தன்மை & கார்பன்","استحکام اور کاربن","સ્થિરતા અને કાર્બન","ಸುಸ್ಥಿರತೆ & ಇಂಗಾಲ","ସ୍ଥିରତା ଓ କାର୍ବନ","സുസ്ഥിരതയും കാർബണും","ਸਥਿਰਤਾ ਅਤੇ ਕਾਰਬਨ","স্থায়িত্ব আৰু কাৰ্বন","स्थिरता आ कार्बन","स्थिरता कार्बन च","استحکام تہٕ کاربن","दिगोपन र कार्बन","استحڪام ۽ ڪاربن","शाश्वतता व कार्बन","स्थिरता ते कार्बन","ꯄꯨꯝꯅꯃꯕ ꯑꯃꯁꯨꯡ ꯀꯥꯔꯕꯟ","स्थिरता ते कार्बन"),
"gov_section":M("Government Schemes","सरकारी योजनाएं","সরকারি প্রকল্প","ప్రభుత్వ పథకాలు","सरकारी योजना","அரசு திட்டங்கள்","سرکاری اسکیمیں","સરકારી યોજનાઓ","ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು","ସରକାରୀ ଯୋଜନା","സർക്കാർ പദ്ധതികൾ","ਸਰਕਾਰੀ ਸਕੀਮਾਂ","চৰকাৰী আঁচনি","सरकारी योजना","सरकारी योजनाः","سرکاری اسکیمہٕ","सरकारी योजना","سرڪاري اسڪيمون","सरकारी येवजण्यो","सरकारी योजनां","ꯁꯔꯀꯥꯔ ꯗꯦ ꯍꯦꯟꯐꯝ","सरकारी योजना"),
"calendar_section":M("Crop Calendar","फसल कैलेंडर","ফসল ক্যালেন্ডার","పంట క్యాలెండర్","पीक दिनदर्शिका","பயிர் நாட்காட்டி","فصل کیلنڈر","પાક કેલેન્ડર","ಬೆಳೆ ಕ್ಯಾಲೆಂಡರ್","ଫସଲ କ୍ୟାଲେଣ୍ଡର","വിള കലണ്ടർ","ਫਸਲ ਕੈਲੰਡਰ","শস্য কেলেণ্ডাৰ","फसल कैलेंडर","शस्य पञ्चाङ्गम्","فصل کیلنڈر","बाली पात्रो","فصل ڪئلينڊر","पीक दिनदर्शिका","फसल कैलेंडर","ꯐꯥꯎꯕꯥ ꯀꯦꯂꯦꯟꯗꯔ","फसल कैलेंडर"),
"chatbot_title":M("Ask AGROVA AI","AGROVA AI से पूछें","AGROVA AI-কে জিজ্ঞাসা","AGROVA AIని అడగండి","AGROVA AI ला विचारा","AGROVA AI-விடம் கேளுங்கள்","AGROVA AI سے پوچھیں","AGROVA AI ને પૂછો","AGROVA AI ಗೆ ಕೇಳಿ","AGROVA AI କୁ ପଚାରନ୍ତୁ","AGROVA AI-യോട് ചോദിക്കുക","AGROVA AI ਨੂੰ ਪੁੱਛੋ","AGROVA AI ক সোধক","AGROVA AI सँ पुछू","AGROVA AI पृच्छतु","AGROVA AI پؤچھیو","AGROVA AI लाई सोध्नुहोस्","AGROVA AI کان پڇو","AGROVA AI क विचार","AGROVA AI थमां पुछो","AGROVA AI ꯗ ꯍꯪꯕ","AGROVA AI था हांख"),
"ask_chat":M("Ask about crops, soil, water, pests, schemes...","फसल, मिट्टी, पानी, कीट, योजनाओं के बारे में पूछें...","ফসল, মাটি, জল, পোকা, প্রকল্প নিয়ে জিজ্ঞাসা করুন...","పంట, నేల, నీరు, పురుగు, పథకాల గురించి అడగండి...","पीक, माती, पाणी, कीड, योजनांबद्दल विचारा...","பயிர், மண், நீர், பூச்சி, திட்டங்கள் பற்றி கேளுங்கள்...","فصل، مٹی، پانی، کیڑے، اسکیموں کے بارے میں پوچھیں...","પાક, જમીન, પાણી, જીવાત, યોજનાઓ વિશે પૂછો...","ಬೆಳೆ, ಮಣ್ಣು, ನೀರು, ಕೀಟ, ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ...","ଫସଲ, ମାଟି, ପାଣି, କୀଟ, ଯୋଜନା ବିଷୟରେ ପଚାରନ୍ତୁ...","വിള, മണ്ണ്, ജലം, കീടം, പദ്ധതികളെക്കുറിച്ച് ചോദിക്കൂ...","ਫਸਲ, ਮਿੱਟੀ, ਪਾਣੀ, ਕੀੜੇ, ਸਕੀਮਾਂ ਬਾਰੇ ਪੁੱਛੋ...","শস্য, মাটি, পানী, কীট, আঁচনিৰ বিষয়ে সোধক...","फसल, माटि, पानि, कीट, योजनाक बारे मे पुछू...","शस्य मृदा जल कीट योजना विषये पृच्छतु...","فصل، مٹی، آب، کیڑہٕ، اسکیمن بابت پؤچھیو...","बाली, माटो, पानी, किरा, योजनाको बारेमा सोध्नुहोस्...","فصل، مٽي، پاڻي، ڪيڙا، اسڪيمن بابت پڇو...","पीक, माती, उदक, किड, येवजण्यांविशीं विचार...","फसल, मिट्टी, पानी, कीड़े, योजनां बारे पुछो...","ꯐꯥꯎꯕꯥ, ꯂꯩ, ꯏꯁꯤꯡ, ꯑꯃꯤꯅ, ꯍꯦꯟꯐꯝ ꯗ ꯍꯪꯕ...","फसल, मिट्टी, पानी, कीड़े, योजनां बारे पुछो..."),
})

def T(key, lang):
    d = TX.get(key, {})
    return d.get(lang, d.get("English", key))

# ══════════════════════════════════════════════════════════════
# STATUS / MESSAGE TOKENS — reusable across every section instead of
# one-off partial-language dicts scattered through the old file.
# ══════════════════════════════════════════════════════════════
L = {
"high":M("High","उच्च","উচ্চ","అధిక","उच्च","அதிக","زیادہ","ઊંચું","ಹೆಚ್ಚು","ଉଚ୍ଚ","ഉയർന്ന","ਉੱਚ","উচ্চ","उच्च","उच्चम्","زیادہ","उच्च","وڌيڪ","चड","उच्च","ꯑꯍꯦꯟꯕ","बांठा"),
"medium":M("Medium","मध्यम","মাঝারি","మధ్యమ","मध्यम","நடுத்தர","درمیانہ","મધ્યમ","ಮಧ್ಯಮ","ମଧ୍ୟମ","ഇടത്തരം","ਦਰਮਿਆਨਾ","মধ্যম","मध्यम","मध्यमम्","درمیانہ","मध्यम","وچولو","मध्यम","मध्यम","ꯃꯐꯝ","मझला"),
"low":M("Low","कम","কম","తక్కువ","कमी","குறைவு","کم","ઓછું","ಕಡಿಮೆ","କମ","കുറഞ്ഞ","ਘੱਟ","কম","कम","न्यूनम्","کم","कम","گھٽ","उणे","घट","ꯀꯍꯛ","गम"),
"optimal":M("Optimal","उत्तम","উত্তম","అనుకూలం","उत्तम","உகந்த","بہترین","ઉત્તમ","ಸೂಕ್ತ","ଉତ୍ତମ","ഉചിതം","ਵਧੀਆ","উত্তম","उत्तम","उत्तमम्","بہترین","उत्तम","بھترين","बरें","बेहतर","ꯑꯐꯕ","बेहतर"),
"safe":M("Safe","सुरक्षित","নিরাপদ","సురక్షితం","सुरक्षित","பாதுகாப்பானது","محفوظ","સુરક્ષિત","ಸುರಕ್ಷಿತ","ସୁରକ୍ଷିତ","സുരക്ഷിതം","ਸੁਰੱਖਿਅਤ","সুৰক্ষিত","सुरक्षित","सुरक्षितम्","محفوظ","सुरक्षित","محفوظ","सुरक्षीत","सुरक्खत","ꯅꯤꯡꯇꯝ","सुरक्षित"),
"danger":M("Danger","खतरा","বিপদ","ప్రమాదం","धोका","ஆபத்து","خطرہ","ખતરો","ಅಪಾಯ","ବିପଦ","അപകടം","ਖਤਰਾ","বিপদ","खतरा","संकटः","خطرہ","खतरा","خطرو","धोको","खतरा","ꯑꯀꯤꯕ","खतरा"),
"excess":M("Excess","अधिक","অতিরিক্ত","అధికం","अतिरिक्त","அதிகம்","زائد","વધારે","ಅಧಿಕ","ଅତିରିକ୍ତ","അധികം","ਵਾਧੂ","অতিৰিক্ত","बेसी","अधिकम्","زیادہ","बढी","وڌيڪ","अधिक","बधीक","ꯍꯦꯟꯅ","बांठा"),
"deficient":M("Deficient","कमी","ঘাটতি","లోపం","कमतरता","குறைபாடு","کمی","ઉણપ","ಕೊರತೆ","ଅଭାବ","കുറവ്","ਕਮੀ","ঘাটতি","कमी","न्यूनता","کمی","कमी","کمي","उणीव","कमी","ꯅꯦꯠꯅꯕ","गइम"),
"excellent":M("Excellent","उत्कृष्ट","চমৎকার","అద్భుతం","उत्कृष्ट","சிறந்தது","بہترین","ઉત્કૃષ્ટ","ಅತ್ಯುತ್ತಮ","ଉତ୍କୃଷ୍ଟ","മികച്ചത്","ਸ਼ਾਨਦਾਰ","উৎকৃষ্ট","उत्कृष्ट","उत्कृष्टम्","بہترین","उत्कृष्ट","بهترين","उत्कृश्ट","उत्तम","ꯑꯐꯕ ꯃꯃꯥꯡ","बेहतरीन"),
"good":M("Good","अच्छा","ভালো","మంచిది","चांगले","நல்லது","اچھا","સારું","ಚೆನ್ನಾಗಿದೆ","ଭଲ","നല്ലത്","ਚੰਗਾ","ভাল","नीक","सुष्ठु","اچھا","राम्रो","سٺو","बरें","चंगा","ꯐꯖꯕ","बेस"),
"moderate":M("Moderate","मध्यम","পরিমিত","మధ్యస్థం","मध्यम","மிதமான","معتدل","સાધારણ","ಮಧ್ಯಮ","ମଧ୍ୟମ","മിതം","ਦਰਮਿਆਨਾ","পৰিমিত","मध्यम","मध्यमम्","معتدل","मध्यम","معتدل","मध्यम","मध्यम","ꯃꯐꯝ","मझला"),
"needs_improvement":M("Needs Improvement","सुधार आवश्यक","উন্নতি প্রয়োজন","మెరుగుదల అవసరం","सुधार आवश्यक","மேம்பாடு தேவை","بہتری کی ضرورت","સુધારો જરૂરી","ಸುಧಾರಣೆ ಅಗತ್ಯ","ଉନ୍ନତି ଆବଶ୍ୟକ","മെച്ചപ്പെടുത്തൽ ആവശ്യം","ਸੁਧਾਰ ਦੀ ਲੋੜ","উন্নতিৰ প্ৰয়োজন","सुधार जरूरी","सुधारः आवश्यकः","بہتری ضروری","सुधार आवश्यक","بھتري گھرجي","सुधारणा गरज","सुधार लोड़ीन्दा","ꯍꯦꯟꯅꯕ ꯃꯇꯦꯡ ꯃꯇꯦꯡ","सुधार जरूरी"),
"apply_now":M("Apply Now","अभी आवेदन करें","এখনই আবেদন করুন","ఇప్పుడే దరఖాస్తు చేయండి","आत्ता अर्ज करा","இப்போதே விண்ணப்பிக்கவும்","ابھی درخواست دیں","હમણાં અરજી કરો","ಈಗಲೇ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ","ବର୍ତ୍ତମାନ ଆବେଦନ କରନ୍ତୁ","ഇപ്പോൾ അപേക്ഷിക്കുക","ਹੁਣੇ ਅਰਜ਼ੀ ਦਿਓ","এতিয়াই আবেদন কৰক","एखन आवेदन करू","अधुना आवेदनं कुरुत","ہاںز درخواست دِیو","अहिले आवेदन गर्नुहोस्","هاڻي درخواست ڏيو","आत्ता अर्ज कर","हुण अर्जी दिओ","ꯍꯧꯖꯤꯛ ꯑꯦꯄ꯭ꯂꯥꯏ ꯇꯧ","हुण अर्जी दिओ"),
"no_major_risk":M("No major crop-loss risk under current conditions.","वर्तमान परिस्थितियों में कोई बड़ा फसल हानि जोखिम नहीं।","বর্তমান পরিস্থিতিতে বড় ফসল ক্ষতির ঝুঁকি নেই।","ప్రస్తుత పరిస్థితుల్లో ప్రధాన పంట నష్ట ప్రమాదం లేదు।","सध्याच्या परिस्थितीत मोठा पीक नुकसान धोका नाही.","தற்போதைய நிலைமையில் பெரிய பயிர் இழப்பு அபாயம் இல்லை.","موجودہ حالات میں کوئی بڑا فصل نقصان کا خطرہ نہیں۔","હાલની પરિસ્થિતિમાં કોઈ મોટું પાક નુકસાનનું જોખમ નથી.","ಪ್ರಸ್ತುತ ಪರಿಸ್ಥಿತಿಯಲ್ಲಿ ದೊಡ್ಡ ಬೆಳೆ ನಷ್ಟ ಅಪಾಯವಿಲ್ಲ.","ବର୍ତ୍ତମାନ ପରିସ୍ଥିତିରେ ବଡ଼ ଫସଲ କ୍ଷତିର ବିପଦ ନାହିଁ।","നിലവിലെ സാഹചര്യത്തിൽ വലിയ വിള നഷ്ട സാധ്യതയില്ല.","ਮੌਜੂਦਾ ਹਾਲਾਤ ਵਿੱਚ ਕੋਈ ਵੱਡਾ ਫਸਲ ਨੁਕਸਾਨ ਖਤਰਾ ਨਹੀਂ।","বৰ্তমান পৰিস্থিতিত ডাঙৰ শস্য ক্ষতিৰ আশংকা নাই।","अखनका परिस्थिति मे कोनो पैघ फसल हानिक खतरा नहि।","वर्तमान परिस्थितौ न कोऽपि महान् शस्यहानि जोखिमः।","اکھ حالاتن منز کانہہ وڈ فصل نقصان خطرہ چھُنہ۔","हालको अवस्थामा ठूलो बाली नोक्सान जोखिम छैन।","موجوده حالتن ۾ ڪو وڏو فصل نقصان جو خطرو ناهي۔","सध्याच्या परिस्थितींत व्हड पीक नुकसानाचो धोको ना.","हुणी हालातां च कोई बड्डा फसल नुकसान खतरा नेईं।","ꯍꯧꯖꯤꯛꯀꯤ ꯑꯄꯨꯅꯕꯗ ꯃꯄꯨꯡ ꯐꯥꯎꯕꯥ ꯃꯥꯡꯍꯟꯕꯒꯤ ꯐꯤꯕ ꯑꯃꯗꯥ ꯑꯣꯏꯗꯦ।","हुणी हालातां च कोई बड्डा फसल नुकसान खतरा नेईं।"),
"register_pmfby":M("Register for PMFBY crop insurance — you pay only 2% premium, government covers the rest.","PMFBY फसल बीमा में पंजीकरण करें — सिर्फ 2% प्रीमियम आप देते हैं, बाकी सरकार वहन करती है।","PMFBY ফসল বীমার জন্য নিবন্ধন করুন — মাত্র ২% প্রিমিয়াম, বাকি সরকার বহন করে।","PMFBY పంట బీమా కోసం నమోదు చేసుకోండి — 2% ప్రీమియం మాత్రమే, మిగతా ప్రభుత్వం భరిస్తుంది।","PMFBY पीक विम्यासाठी नोंदणी करा — फक्त 2% प्रीमियम, उरलेला सरकार भरते.","PMFBY பயிர் காப்பீட்டிற்கு பதிவு செய்யுங்கள் — 2% பிரீமியம் மட்டும், மீதி அரசு.","PMFBY فصل بیمہ کے لیے رجسٹر کریں — صرف 2% پریمیم، باقی حکومت ادا کرتی ہے۔","PMFBY પાક વીમા માટે નોંધણી કરો — ફક્ત 2% પ્રીમિયમ, બાકી સરકાર ભરે.","PMFBY ಬೆಳೆ ವಿಮೆಗೆ ನೋಂದಣಿ ಮಾಡಿ — ಕೇವಲ 2% ಪ್ರೀಮಿಯಂ, ಉಳಿದದ್ದು ಸರ್ಕಾರ.","PMFBY ଫସଲ ବୀମା ପାଇଁ ପଞ୍ଜୀକରଣ କରନ୍ତୁ — କେବଳ 2% ପ୍ରିମିୟମ, ବାକି ସରକାର।","PMFBY വിള ഇൻഷുറൻസിന് രജിസ്റ്റർ ചെയ്യുക — 2% പ്രീമിയം മാത്രം, ബാക്കി സർക്കാർ.","PMFBY ਫਸਲ ਬੀਮੇ ਲਈ ਰਜਿਸਟਰ ਕਰੋ — ਸਿਰਫ਼ 2% ਪ੍ਰੀਮੀਅਮ, ਬਾਕੀ ਸਰਕਾਰ।","PMFBY শস্য বীমাৰ বাবে পঞ্জীয়ন কৰক — মাত্ৰ ২% প্ৰিমিয়াম, বাকী চৰকাৰে বহন কৰে।","PMFBY फसल बीमा मे पंजीकरण करू — सिर्फ 2% प्रीमियम, बाकी सरकार दैत छै।","PMFBY शस्यबीमार्थं पञ्जीकरणं कुरुत — केवलं 2% हप्तं शेषं सरकारः।","PMFBY فصل بیمُک واسطہٕ رجسٹر کریو — صرف 2% پریمیم، باقی حکومت۔","PMFBY बाली बीमाको लागि दर्ता गर्नुहोस् — जम्मा 2% प्रिमियम, बाँकी सरकार।","PMFBY فصل بیمي لاءِ داخلا ڪريو — رڳو 2% پریميم، باقي حڪومت۔","PMFBY पीक विम्यांखातीर नोंदणी कर — फकत 2% प्रीमियम, उरिल्लें सरकार भरता.","PMFBY फसल बीमे लेई रजिस्टर करो — सिर्फ 2% प्रीमियम, बाकी सरकार।","PMFBY ꯐꯥꯎꯕꯥ ꯚꯤꯃꯥꯒꯤꯗꯃꯛ ꯔꯦꯖꯤꯁꯇꯔ ꯇꯧ — 2% ꯄ꯭ꯔꯤꯃꯤꯌꯝ ꯈꯛꯇ, ꯑꯇꯩꯗꯨ ꯁꯔꯀꯥꯔꯅ।","PMFBY फसल बीमे लेई रजिस्टर करो — सिर्फ 2% प्रीमियम, बाकी सरकार।"),
"harvest_note":M("Stop irrigation 7 days before harvest for better grain quality.","बेहतर अनाज गुणवत्ता हेतु कटाई से 7 दिन पहले सिंचाई बंद करें।","ভালো ফলনের জন্য কাটার ৭ দিন আগে সেচ বন্ধ করুন।","మెరుగైన ధాన్యం కోసం కోతకు 7 రోజుల ముందు నీటిపారుదల ఆపండి।","चांगल्या धान्यासाठी कापणीच्या 7 दिवस आधी सिंचन बंद करा.","சிறந்த தானியத்திற்கு அறுவடைக்கு 7 நாட்கள் முன் நீர்ப்பாசனத்தை நிறுத்தவும்.","بہتر معیار کے لیے کٹائی سے 7 دن پہلے آبپاشی بند کریں۔","સારા દાણા માટે કાપણીના 7 દિવસ પહેલા સિંચાઈ બંધ કરો.","ಉತ್ತಮ ಧಾನ್ಯಕ್ಕಾಗಿ ಕೊಯ್ಲಿಗೆ 7 ದಿನ ಮೊದಲು ನೀರಾವರಿ ನಿಲ್ಲಿಸಿ.","ଭଲ ଶସ୍ୟ ପାଇଁ ଅମଳର 7 ଦିନ ପୂର୍ବେ ଜଳସେଚନ ବନ୍ଦ କରନ୍ତୁ।","മെച്ചപ്പെട്ട ധാന്യത്തിന് വിളവെടുപ്പിന് 7 ദിവസം മുമ്പ് ജലസേചനം നിർത്തുക.","ਵਧੀਆ ਦਾਣੇ ਲਈ ਵਾਢੀ ਤੋਂ 7 ਦਿਨ ਪਹਿਲਾਂ ਸਿੰਚਾਈ ਬੰਦ ਕਰੋ।","ভাল শস্যৰ বাবে চপোৱাৰ ৭ দিন আগতে জলসিঞ্চন বন্ধ কৰক।","नीक अन्नक लेल कटनीसँ 7 दिन पहिने सिंचाई बंद करू।","उत्तमधान्यार्थं कटनात् 7 दिनपूर्वं सिञ्चनं त्यजतु।","بہتر اَنّہٕ خٲطرہٕ کٹنہٕ برونٹھ 7 دۄہ سینچہٕ بند کریو۔","राम्रो अन्नको लागि कटानीभन्दा 7 दिन अघि सिँचाइ रोक्नुहोस्।","سٺي داڻي لاءِ لڻڻ کان 7 ڏينهن اڳ آبپاشي بند ڪريو۔","बरें दानाखातीर कापणेच्या 7 दिसां आदीं सिंचन बंद कर.","चंगे दाणे आस्ते कटाई थमां 7 दिन पहलें सिंचाई बंद करो।","ꯑꯐꯕ ꯃꯃꯨꯅ ꯃꯐꯝ ꯂꯧꯕꯒꯤ 7 ꯅꯨꯃꯤꯠ ꯃꯃꯥꯡꯗ ꯏꯁꯤꯡ ꯄꯤꯅꯕ ꯂꯩꯍꯪꯕ।","चंगे दाणे आस्ते कटाई थमां 7 दिन पहलें सिंचाई बंद करो।"),
}

def SEASON(s, lang):
    d = {"Kharif": L_SEASON_K, "Rabi": L_SEASON_R, "Annual": L_SEASON_A}
    return d.get(s, {}).get(lang, s)

L_SEASON_K = M("Kharif (Jun–Oct)","खरीफ (जून–अक्टूबर)","খরিফ (জুন–অক্টোবর)","ఖరీఫ్ (జూన్–అక్టోబర్)","खरीप (जून–ऑक्टो)","கரீஃப் (ஜூன்–அக்.)","خریف (جون–اکتوبر)","ખરીફ (જૂન–ઓક્ટો)","ಖರೀಫ್ (ಜೂ–ಅಕ್ಟೋ)","ଖରିଫ (ଜୁନ–ଅକ୍ଟୋ)","ഖരീഫ് (ജൂൺ–ഒക്ടോ)","ਖਰੀਫ (ਜੂਨ–ਅਕਤੂ)","খৰিফ (জুন–অক্টো)","खरीफ (जून–अक्टू)","खरीफ ऋतुः","خریف (جون–اکتوبر)","खरिफ (जुन–अक्टो)","خريف (جون–آڪٽوبر)","खरीप (जून–ऑक्टो)","खरीफ (जून–अक्टूबर)","ꯈꯔꯤꯐ (ꯖꯨꯟ–ꯑꯛꯇꯣ)","खरीफ (जून–अक्टूबर)")
L_SEASON_R = M("Rabi (Nov–Mar)","रबी (नवंबर–मार्च)","রবি (নভে–মার্চ)","రబీ (నవం–మార్చి)","रब्बी (नोव्हें–मार्च)","ரபி (நவ.–மார்.)","ربیع (نومبر–مارچ)","રવી (નવે–માર્ચ)","ರಬಿ (ನವೆಂ–ಮಾ)","ରବି (ନଭେ–ମାର୍ଚ୍ଚ)","റബി (നവം–മാർ)","ਰਬੀ (ਨਵੰ–ਮਾਰਚ)","ৰবি (নৱে–মাৰ্চ)","रबी (नवं–मार्च)","रबी ऋतुः","ربیع (نومبر–مارچ)","रबी (नोभे–मार्च)","ربيع (نومبر–مارچ)","रब्बी (नोव्हें–मार्च)","रबी (नवंबर–मार्च)","ꯔꯕꯤ (ꯅꯣꯚꯦ–ꯃꯥꯔꯆ)","रबी (नवंबर–मार्च)")
L_SEASON_A = M("Annual","वार्षिक","বার্ষিক","వార్షిక","वार्षिक","வருடாந்திர","سالانہ","વાર્ષિક","ವಾರ್ಷಿಕ","ବାର୍ଷିକ","വാർഷിക","ਸਾਲਾਨਾ","বাৰ্ষিক","वार्षिक","वार्षिकम्","سالانہ","वार्षिक","سالياني","वार्शिक","सालाना","ꯆꯍꯤꯗꯥꯗꯤ","सालाना")

# ══════════════════════════════════════════════════════════════
# CROP LOCAL NAMES — verbatim from source data; the corrupted
# Gujarati/Odia romanized placeholders (crops #24 onward) are
# replaced with real script below.
# ══════════════════════════════════════════════════════════════
CROP_NAMES = {
    "Rice":{"English":"Rice","Hindi":"चावल","Bengali":"ধান","Telugu":"వరి","Marathi":"भात","Tamil":"அரிசி","Urdu":"چاول","Gujarati":"ચોખા","Kannada":"ಅಕ್ಕಿ","Odia":"ଚାଉଳ","Malayalam":"അരി","Punjabi":"ਚੌਲ","Assamese":"ধান","Maithili":"धान","Sanskrit":"ओदनः","Kashmiri":"برنج","Nepali":"चामल","Sindhi":"چانور","Konkani":"तांदूळ","Dogri":"चौल","Manipuri":"ꯆꯥꯎ","Bodo":"বাউ"},
    "Wheat":{"English":"Wheat","Hindi":"गेहूँ","Bengali":"গম","Telugu":"గోధుమ","Marathi":"गहू","Tamil":"கோதுமை","Urdu":"گندم","Gujarati":"ઘઉં","Kannada":"ಗೋಧಿ","Odia":"ଗହମ","Malayalam":"ഗോതമ്പ്","Punjabi":"ਕਣਕ","Assamese":"ঘেঁহু","Maithili":"गहूम","Sanskrit":"गोधूमः","Kashmiri":"گندم","Nepali":"गहुँ","Sindhi":"ڪڻڪ","Konkani":"गोधुम","Dogri":"कणक","Manipuri":"ꯒꯧꯗꯨꯝ","Bodo":"গম"},
    "Maize":{"English":"Maize","Hindi":"मक्का","Bengali":"ভুট্টা","Telugu":"మొక్కజొన్న","Marathi":"मका","Tamil":"மக்காச்சோளம்","Urdu":"مکئی","Gujarati":"મકાઈ","Kannada":"ಜೋಳ","Odia":"ମକ୍କା","Malayalam":"ചോളം","Punjabi":"ਮੱਕੀ","Assamese":"মকৈ","Maithili":"मकई","Sanskrit":"मकई","Kashmiri":"مکئی","Nepali":"मकै","Sindhi":"مڪئي","Konkani":"मकई","Dogri":"मकई","Manipuri":"ꯃꯀꯥ","Bodo":"মকাই"},
    "Millets":{"English":"Millets","Hindi":"बाजरा","Bengali":"বাজরা","Telugu":"జొన్న","Marathi":"बाजरी","Tamil":"கம்பு","Urdu":"باجرہ","Gujarati":"બાજરી","Kannada":"ಸಜ್ಜೆ","Odia":"ବାଜରା","Malayalam":"ചാമ","Punjabi":"ਬਾਜਰਾ","Assamese":"বাজৰা","Maithili":"बाजरा","Sanskrit":"बाजरम्","Kashmiri":"باجرہ","Nepali":"कोदो","Sindhi":"باجرو","Konkani":"बाजरी","Dogri":"बाजरा","Manipuri":"ꯚꯥꯖꯔꯥ","Bodo":"বাজৰা"},
    "Cotton":{"English":"Cotton","Hindi":"कपास","Bengali":"তুলা","Telugu":"పత్తి","Marathi":"कापूस","Tamil":"பருத்தி","Urdu":"کپاس","Gujarati":"કપાસ","Kannada":"ಹತ್ತಿ","Odia":"କପା","Malayalam":"പരുത്തി","Punjabi":"ਕਪਾਹ","Assamese":"কপাহ","Maithili":"कपास","Sanskrit":"कार्पासः","Kashmiri":"نربز","Nepali":"कपास","Sindhi":"ڪپهه","Konkani":"कापूस","Dogri":"कपास","Manipuri":"ꯀꯄꯥꯁ","Bodo":"কপাহ"},
    "Sugarcane":{"English":"Sugarcane","Hindi":"गन्ना","Bengali":"আখ","Telugu":"చెరకు","Marathi":"ऊस","Tamil":"கரும்பு","Urdu":"گنا","Gujarati":"શેરડી","Kannada":"ಕಬ್ಬು","Odia":"ଆଖୁ","Malayalam":"കരിമ്പ്","Punjabi":"ਗੰਨਾ","Assamese":"কুঁহিয়াৰ","Maithili":"इख","Sanskrit":"इक्षुः","Kashmiri":"اکھ","Nepali":"उखु","Sindhi":"گنڍ","Konkani":"ऊस","Dogri":"गन्ना","Manipuri":"ꯉꯣꯡꯀꯣꯡ","Bodo":"আখ"},
    "Barley":{"English":"Barley","Hindi":"जौ","Bengali":"যব","Telugu":"బార్లీ","Marathi":"जव","Tamil":"வாற்கோதுமை","Urdu":"جو","Gujarati":"જવ","Kannada":"ಬಾರ್ಲಿ","Odia":"ଯବ","Malayalam":"ബാർലി","Punjabi":"ਜੌਂ","Assamese":"যৱ","Maithili":"जौ","Sanskrit":"यवः","Kashmiri":"جو","Nepali":"जौ","Sindhi":"جَوَن","Konkani":"जव","Dogri":"जौं","Manipuri":"ꯖꯧ","Bodo":"যৱ"},
    "Soybean":{"English":"Soybean","Hindi":"सोयाबीन","Bengali":"সয়াবিন","Telugu":"సోయాబీన్","Marathi":"सोयाबीन","Tamil":"சோயாபீன்","Urdu":"سویابین","Gujarati":"સોયાબીન","Kannada":"ಸೋಯಾಬೀನ್","Odia":"ସୋୟାବିନ","Malayalam":"സോയാബീൻ","Punjabi":"ਸੋਇਆਬੀਨ","Assamese":"চয়াবিন","Maithili":"सोयाबीन","Sanskrit":"सोयाबीनम्","Kashmiri":"سویابین","Nepali":"सोयाबिन","Sindhi":"سوئابين","Konkani":"सोयाबीन","Dogri":"सोयाबीन","Manipuri":"ꯁꯣꯌꯥꯕꯤꯟ","Bodo":"চয়াবিন"},
    "Groundnut":{"English":"Groundnut","Hindi":"मूंगफली","Bengali":"চিনাবাদাম","Telugu":"వేరుశెనగ","Marathi":"शेंगदाणे","Tamil":"கடலை","Urdu":"مونگ پھلی","Gujarati":"મગફળી","Kannada":"ಕಡಲೆಕಾಯಿ","Odia":"ଚିନାବାଦାମ","Malayalam":"നിലക്കടല","Punjabi":"ਮੂੰਗਫਲੀ","Assamese":"মাটিমাহ","Maithili":"मूंगफली","Sanskrit":"भूशिम्बा","Kashmiri":"مونگ پھلی","Nepali":"बदाम","Sindhi":"موڱفلي","Konkani":"शेंगो","Dogri":"मूंगफली","Manipuri":"ꯃꯨꯡꯒꯐꯂꯤ","Bodo":"মুগামাহ"},
    "Mustard":{"English":"Mustard","Hindi":"सरसों","Bengali":"সরিষা","Telugu":"ఆవాలు","Marathi":"मोहरी","Tamil":"கடுகு","Urdu":"سرسوں","Gujarati":"રાઈ","Kannada":"ಸಾಸಿವೆ","Odia":"ସୋରିଷ","Malayalam":"കടുക്","Punjabi":"ਸਰ੍ਹੋਂ","Assamese":"সৰিয়হ","Maithili":"सरिसो","Sanskrit":"सर्षपः","Kashmiri":"ہاک","Nepali":"तोरी","Sindhi":"سرنهون","Konkani":"मोरी","Dogri":"सरूं","Manipuri":"ꯁꯔꯁꯣꯡ","Bodo":"চৰিয়া"},
    "Tea":{"English":"Tea","Hindi":"चाय","Bengali":"চা","Telugu":"తేయాకు","Marathi":"चहा","Tamil":"தேயிலை","Urdu":"چائے","Gujarati":"ચા","Kannada":"ಚಹಾ","Odia":"ଚା","Malayalam":"ചായ","Punjabi":"ਚਾਹ","Assamese":"চাহ","Maithili":"चाह","Sanskrit":"चायः","Kashmiri":"چاہ","Nepali":"चिया","Sindhi":"چانهه","Konkani":"चाय","Dogri":"चाह","Manipuri":"ꯆꯥ","Bodo":"চা"},
    "Coffee":{"English":"Coffee","Hindi":"कॉफी","Bengali":"কফি","Telugu":"కాఫీ","Marathi":"कॉफी","Tamil":"காபி","Urdu":"کافی","Gujarati":"કૉફી","Kannada":"ಕಾಫಿ","Odia":"କଫି","Malayalam":"കാപ്പി","Punjabi":"ਕੌਫੀ","Assamese":"কফি","Maithili":"कॉफी","Sanskrit":"कापी","Kashmiri":"کافی","Nepali":"कफी","Sindhi":"ڪافي","Konkani":"कॉफी","Dogri":"कॉफी","Manipuri":"ꯀꯣꯐꯤ","Bodo":"কফি"},
    "Banana":{"English":"Banana","Hindi":"केला","Bengali":"কলা","Telugu":"అరటి","Marathi":"केळ","Tamil":"வாழைப்பழம்","Urdu":"کیلا","Gujarati":"કેળું","Kannada":"ಬಾಳೆ","Odia":"କଦଳୀ","Malayalam":"വാഴ","Punjabi":"ਕੇਲਾ","Assamese":"কল","Maithili":"केरा","Sanskrit":"कदली","Kashmiri":"کیل","Nepali":"केरा","Sindhi":"ڪيرو","Konkani":"केळे","Dogri":"केला","Manipuri":"ꯉꯥꯡꯁꯤ","Bodo":"কল"},
    "Mango":{"English":"Mango","Hindi":"आम","Bengali":"আম","Telugu":"మామిడి","Marathi":"आंबा","Tamil":"மாம்பழம்","Urdu":"آم","Gujarati":"કેરી","Kannada":"ಮಾವು","Odia":"ଆମ୍ବ","Malayalam":"മാമ്പഴം","Punjabi":"ਅੰਬ","Assamese":"আম","Maithili":"आम","Sanskrit":"आम्रः","Kashmiri":"آمب","Nepali":"आँप","Sindhi":"اَمُ","Konkani":"आंबो","Dogri":"अੰਬ","Manipuri":"ꯑꯥꯝꯕꯤ","Bodo":"আম"},
    "Apple":{"English":"Apple","Hindi":"सेब","Bengali":"আপেল","Telugu":"ఆపిల్","Marathi":"सफरचंद","Tamil":"ஆப்பிள்","Urdu":"سیب","Gujarati":"સફરજન","Kannada":"ಸೇಬು","Odia":"ଆପେଲ","Malayalam":"ആപ്പിൾ","Punjabi":"ਸੇਬ","Assamese":"আপেল","Maithili":"सेव","Sanskrit":"सेवः","Kashmiri":"تفاح","Nepali":"स्याउ","Sindhi":"سيب","Konkani":"सफरचंद","Dogri":"सेब","Manipuri":"ꯑꯦꯄꯨꯜ","Bodo":"আপেল"},
    "Potato":{"English":"Potato","Hindi":"आलू","Bengali":"আলু","Telugu":"బంగాళాదుంప","Marathi":"बटाटा","Tamil":"உருளைக்கிழங்கு","Urdu":"آلو","Gujarati":"બટાટા","Kannada":"ಆಲೂಗಡ್ಡೆ","Odia":"ଆଳୁ","Malayalam":"ഉരുളക്കിഴങ്ങ്","Punjabi":"ਆਲੂ","Assamese":"আলু","Maithili":"आलू","Sanskrit":"आलूकम्","Kashmiri":"اولو","Nepali":"आलु","Sindhi":"آلو","Konkani":"बटाटो","Dogri":"आलू","Manipuri":"ꯑꯥꯂꯨ","Bodo":"আলু"},
    "Tomato":{"English":"Tomato","Hindi":"टमाटर","Bengali":"টমেটো","Telugu":"టమాట","Marathi":"टोमॅटो","Tamil":"தக்காளி","Urdu":"ٹماٹر","Gujarati":"ટામેટું","Kannada":"ಟೊಮ್ಯಾಟೊ","Odia":"ଟମାଟୋ","Malayalam":"തക്കാളി","Punjabi":"ਟਮਾਟਰ","Assamese":"টমেটো","Maithili":"टमाटर","Sanskrit":"रक्तफलम्","Kashmiri":"رومی","Nepali":"गोलभेँडा","Sindhi":"ٽماٽو","Konkani":"टोमॅटो","Dogri":"टमाटर","Manipuri":"ꯇꯝꯥꯇꯣ","Bodo":"টমেটো"},
    "Onion":{"English":"Onion","Hindi":"प्याज","Bengali":"পেঁয়াজ","Telugu":"ఉల్లిపాయ","Marathi":"कांदा","Tamil":"வெங்காயம்","Urdu":"پیاز","Gujarati":"ડુંગળી","Kannada":"ಈರುಳ್ಳಿ","Odia":"ପିଆଜ","Malayalam":"ഉള്ളി","Punjabi":"ਪਿਆਜ਼","Assamese":"পিঁয়াজ","Maithili":"प्याज","Sanskrit":"पलाण्डुः","Kashmiri":"گندن","Nepali":"प्याज","Sindhi":"بصل","Konkani":"कांडो","Dogri":"प्याज","Manipuri":"ꯆꯥꯊꯣꯡ","Bodo":"পিয়াজ"},
    "Garlic":{"English":"Garlic","Hindi":"लहसुन","Bengali":"রসুন","Telugu":"వెల్లుల్లి","Marathi":"लसूण","Tamil":"பூண்டு","Urdu":"لہسن","Gujarati":"લસણ","Kannada":"ಬೆಳ್ಳುಳ್ಳಿ","Odia":"ରସୁଣ","Malayalam":"വെളുത്തുള്ളി","Punjabi":"ਲਸਣ","Assamese":"নহৰু","Maithili":"लहसुन","Sanskrit":"लशुनम्","Kashmiri":"رسن","Nepali":"लसुन","Sindhi":"لسڻ","Konkani":"लसूण","Dogri":"लहसण","Manipuri":"ꯏꯁꯤꯡ","Bodo":"নহৰু"},
    "Peas":{"English":"Peas","Hindi":"मटर","Bengali":"মটরশুঁটি","Telugu":"బఠాణీ","Marathi":"वाटाणे","Tamil":"பட்டாணி","Urdu":"مٹر","Gujarati":"વટાણા","Kannada":"ಬಟಾಣಿ","Odia":"ମଟର","Malayalam":"പച്ചപ്പയർ","Punjabi":"ਮਟਰ","Assamese":"মটৰমাহ","Maithili":"मटर","Sanskrit":"कलायः","Kashmiri":"مٹر","Nepali":"केराउ","Sindhi":"مٽر","Konkani":"वाटाणे","Dogri":"मटर","Manipuri":"ꯃꯇꯔ","Bodo":"মটৰ"},
    "Chilli":{"English":"Chilli","Hindi":"मिर्च","Bengali":"মরিচ","Telugu":"మిరపకాయ","Marathi":"मिरची","Tamil":"மிளகாய்","Urdu":"مرچ","Gujarati":"મરચું","Kannada":"ಮೆಣಸಿನಕಾಯಿ","Odia":"ଲଙ୍କା","Malayalam":"മുളക്","Punjabi":"ਮਿਰਚ","Assamese":"জলকীয়া","Maithili":"मिरचाई","Sanskrit":"मरीचम्","Kashmiri":"مرچ","Nepali":"खुर्सानी","Sindhi":"مرچ","Konkani":"मिरसांग","Dogri":"मिरचां","Manipuri":"ꯃꯔꯣꯜ","Bodo":"জলকীয়া"},
    "Turmeric":{"English":"Turmeric","Hindi":"हल्दी","Bengali":"হলুদ","Telugu":"పసుపు","Marathi":"हळद","Tamil":"மஞ்சள்","Urdu":"ہلدی","Gujarati":"હળદર","Kannada":"ಅರಿಶಿಣ","Odia":"ହଳଦୀ","Malayalam":"മഞ്ഞൾ","Punjabi":"ਹਲਦੀ","Assamese":"হালধি","Maithili":"हरदी","Sanskrit":"हरिद्रा","Kashmiri":"ليدر","Nepali":"बेसार","Sindhi":"هلدي","Konkani":"हळद","Dogri":"हलदी","Manipuri":"ꯌꯦꯡꯒꯧ","Bodo":"হালদি"},
    "Ginger":{"English":"Ginger","Hindi":"अदरक","Bengali":"আদা","Telugu":"అల్లం","Marathi":"आले","Tamil":"இஞ்சி","Urdu":"ادرک","Gujarati":"આદુ","Kannada":"ಶುಂಠಿ","Odia":"ଅଦା","Malayalam":"ഇഞ്ചി","Punjabi":"ਅਦਰਕ","Assamese":"আদা","Maithili":"अदरख","Sanskrit":"आर्द्रकम्","Kashmiri":"سونٹھ","Nepali":"अदुवा","Sindhi":"آدو","Konkani":"आले","Dogri":"अदरक","Manipuri":"ꯉꯥꯎꯕꯤ","Bodo":"আদা"},
    "Coconut":{"English":"Coconut","Hindi":"नारियल","Bengali":"নারকেল","Telugu":"కొబ్బరి","Marathi":"नारळ","Tamil":"தேங்காய்","Urdu":"ناریل","Gujarati":"નાળિયેર","Kannada":"ತೆಂಗಿನಕಾಯಿ","Odia":"ନଡ଼ିଆ","Malayalam":"തേങ്ങ","Punjabi":"ਨਾਰੀਅਲ","Assamese":"নাৰিকল","Maithili":"नारियल","Sanskrit":"नारिकेलः","Kashmiri":"نارل","Nepali":"नरिवल","Sindhi":"ناريل","Konkani":"नाळेल","Dogri":"नारियल","Manipuri":"ꯑꯦꯄꯨꯜ","Bodo":"নাৰিকল"},
    "Rajma":{"English":"Rajma","Hindi":"राजमा","Bengali":"রাজমা","Telugu":"రాజ్మా","Marathi":"राजमा","Tamil":"ராஜ்மா","Urdu":"راجما","Gujarati":"રાજમા","Kannada":"ರಾಜ್ಮಾ","Odia":"ରାଜମା","Malayalam":"രാജ്മ","Punjabi":"ਰਾਜਮਾਂ","Assamese":"ৰাজমাহ","Maithili":"राजमा","Sanskrit":"राजमाषः","Kashmiri":"راجما","Nepali":"राजमा","Sindhi":"راجما","Konkani":"राजमा","Dogri":"राजमाँ","Manipuri":"ꯔꯥꯖꯃꯥ","Bodo":"ৰাজমাহ"},
    "Sunflower":{"English":"Sunflower","Hindi":"सूरजमुखी","Bengali":"সূর্যমুখী","Telugu":"పొద్దుతిరుగుడు","Marathi":"सूर्यफूल","Tamil":"சூரியகாந்தி","Urdu":"سورج مکھی","Gujarati":"સૂર્યમુખી","Kannada":"ಸೂರ್ಯಕಾಂತಿ","Odia":"ସୂର୍ଯ୍ୟମୁଖୀ","Malayalam":"സൂര്യകാന്തി","Punjabi":"ਸੂਰਜਮੁਖੀ","Assamese":"সূৰ্যমুখী","Maithili":"सूरजमुखी","Sanskrit":"सूर्यकान्तः","Kashmiri":"سورجمکھی","Nepali":"सूर्यमुखी","Sindhi":"سج مکي","Konkani":"सूर्यफूल","Dogri":"सूरजमुखी","Manipuri":"ꯁꯨꯔꯖꯃꯨꯈꯤ","Bodo":"সূৰ্যমুখী"},
    "Lentils":{"English":"Lentils","Hindi":"मसूर","Bengali":"মসুর","Telugu":"మసూర్","Marathi":"मसूर","Tamil":"மசூர்","Urdu":"مسور","Gujarati":"મસૂર","Kannada":"ಮಸೂರ","Odia":"ମସୁର","Malayalam":"മസൂർ","Punjabi":"ਮਸਰ","Assamese":"মচুৰ","Maithili":"मसुरी","Sanskrit":"मसूरः","Kashmiri":"مسر","Nepali":"मसुरो","Sindhi":"مسور","Konkani":"मसूर","Dogri":"मसर","Manipuri":"ꯃꯁꯨꯔ","Bodo":"মচুৰ"},
    "Chickpea":{"English":"Chickpea","Hindi":"चना","Bengali":"ছোলা","Telugu":"శనగలు","Marathi":"हरभरा","Tamil":"கடலை","Urdu":"چنا","Gujarati":"ચણા","Kannada":"ಕಡಲೆ","Odia":"ଛୋଲା","Malayalam":"കടല","Punjabi":"ਛੋਲੇ","Assamese":"বুট","Maithili":"चना","Sanskrit":"चणकः","Kashmiri":"چنہ","Nepali":"चना","Sindhi":"چڻا","Konkani":"हरभरे","Dogri":"चने","Manipuri":"ꯆꯥꯅꯥ","Bodo":"বুট"},
    "Pigeon Pea":{"English":"Pigeon Pea","Hindi":"अरहर","Bengali":"অড়হর","Telugu":"కంది","Marathi":"तूर","Tamil":"துவரை","Urdu":"ارہر","Gujarati":"તુવેર","Kannada":"ತೊಗರಿ","Odia":"ହରଡ","Malayalam":"തുവര","Punjabi":"ਅਰਹਰ","Assamese":"ৰহৰ","Maithili":"अरहर","Sanskrit":"आढकी","Kashmiri":"ارہر","Nepali":"रहर","Sindhi":"ارهر","Konkani":"तूर","Dogri":"अरहर","Manipuri":"ꯑꯔꯍꯔ","Bodo":"ৰহৰ"},
    "Green Gram":{"English":"Green Gram","Hindi":"मूंग","Bengali":"মুগ","Telugu":"పెసలు","Marathi":"मूग","Tamil":"பச்சைப்பயறு","Urdu":"مونگ","Gujarati":"મગ","Kannada":"ಹೆಸರು","Odia":"ମୁଗ","Malayalam":"ചെറുപയർ","Punjabi":"ਮੂੰਗ","Assamese":"মগু","Maithili":"मूंग","Sanskrit":"मुद्गः","Kashmiri":"ماش","Nepali":"मुग","Sindhi":"مونگ","Konkani":"मूग","Dogri":"मूंग","Manipuri":"ꯃꯨꯡ","Bodo":"মগু"},
    "Sesame":{"English":"Sesame","Hindi":"तिल","Bengali":"তিল","Telugu":"నువ్వులు","Marathi":"तीळ","Tamil":"எள்","Urdu":"تل","Gujarati":"તલ","Kannada":"ಎಳ್ಳು","Odia":"ତିଳ","Malayalam":"എള്ള്","Punjabi":"ਤਿਲ","Assamese":"তিল","Maithili":"तिल","Sanskrit":"तिलाः","Kashmiri":"تل","Nepali":"तील","Sindhi":"تل","Konkani":"तीळ","Dogri":"तिल","Manipuri":"ꯇꯤꯜ","Bodo":"তিল"},
    "Pumpkin":{"English":"Pumpkin","Hindi":"कद्दू","Bengali":"কুমড়া","Telugu":"గుమ్మడికాయ","Marathi":"भोपळा","Tamil":"பரங்கிக்காய்","Urdu":"کدو","Gujarati":"કોળું","Kannada":"ಕುಂಬಳ","Odia":"କଖାରୁ","Malayalam":"മത്തൻ","Punjabi":"ਕੱਦੂ","Assamese":"কোমোৰা","Maithili":"कद्दू","Sanskrit":"कर्कटी","Kashmiri":"کدو","Nepali":"फर्सी","Sindhi":"ڪڏو","Konkani":"भोपळो","Dogri":"कद्दू","Manipuri":"ꯀꯗꯨ","Bodo":"কোমোৰা"},
    "Carrot":{"English":"Carrot","Hindi":"गाजर","Bengali":"গাজর","Telugu":"క్యారెట్","Marathi":"गाजर","Tamil":"கேரட்","Urdu":"گاجر","Gujarati":"ગાજર","Kannada":"ಗಾಜರ","Odia":"ଗାଜର","Malayalam":"കാരറ്റ്","Punjabi":"ਗਾਜਰ","Assamese":"গাজৰ","Maithili":"गाजर","Sanskrit":"गृञ्जनम्","Kashmiri":"گاجر","Nepali":"गाजर","Sindhi":"گاجر","Konkani":"गाजर","Dogri":"गाजर","Manipuri":"ꯒꯥꯖꯔ","Bodo":"গাজৰ"},
    "Spinach":{"English":"Spinach","Hindi":"पालक","Bengali":"পালং শাক","Telugu":"పాలకూర","Marathi":"पालक","Tamil":"பசலைக்கீரை","Urdu":"پالک","Gujarati":"પાલક","Kannada":"ಪಾಲಕ್","Odia":"ପାଳଙ୍ଗ ଶାଗ","Malayalam":"ചീര","Punjabi":"ਪਾਲਕ","Assamese":"পালেং শাক","Maithili":"पालक","Sanskrit":"पालक्यः","Kashmiri":"پالک","Nepali":"पालुंगो","Sindhi":"پالڪ","Konkani":"पालक","Dogri":"पालक","Manipuri":"ꯄꯥꯂꯥꯛ","Bodo":"পালেং"},
    "Brinjal":{"English":"Brinjal","Hindi":"बैंगन","Bengali":"বেগুন","Telugu":"వంకాయ","Marathi":"वांगे","Tamil":"கத்திரிக்காய்","Urdu":"بینگن","Gujarati":"રીંગણ","Kannada":"ಬದನೆಕಾಯಿ","Odia":"ବାଇଗଣ","Malayalam":"വഴുതന","Punjabi":"ਬੈਂਗਣ","Assamese":"বেঙেনা","Maithili":"बैंगन","Sanskrit":"वृन्ताकः","Kashmiri":"وانگن","Nepali":"भन्टा","Sindhi":"وڻانگڻ","Konkani":"वांगे","Dogri":"बेंगण","Manipuri":"ꯎꯃꯩꯁꯤꯡ","Bodo":"বেঙেনা"},
    "Cabbage":{"English":"Cabbage","Hindi":"पत्ता गोभी","Bengali":"বাঁধাকপি","Telugu":"కాబేజీ","Marathi":"कोबी","Tamil":"முட்டைகோஸ்","Urdu":"پت گوبھی","Gujarati":"કોબી","Kannada":"ಎಲೆಕೋಸು","Odia":"ବନ୍ଧାକୋବି","Malayalam":"കാബേജ്","Punjabi":"ਬੰਦ ਗੋਭੀ","Assamese":"বন্ধাকবি","Maithili":"पत्ता गोभी","Sanskrit":"गोभिः","Kashmiri":"گوبھی","Nepali":"बन्दा","Sindhi":"ڪاپي","Konkani":"कोबी","Dogri":"बंद गोभी","Manipuri":"ꯀꯣꯕꯤ","Bodo":"বন্ধাকবি"},
    "Cauliflower":{"English":"Cauliflower","Hindi":"फूल गोभी","Bengali":"ফুলকপি","Telugu":"కాలీఫ్లవర్","Marathi":"फुलकोबी","Tamil":"காலிஃப்ளவர்","Urdu":"گوبھی","Gujarati":"ફૂલકોબી","Kannada":"ಹೂಕೋಸು","Odia":"ଫୁଲକୋବି","Malayalam":"കോളിഫ്ലവർ","Punjabi":"ਫੁੱਲ ਗੋਭੀ","Assamese":"ফুলকবি","Maithili":"फूलगोभी","Sanskrit":"गोभिपुष्पम्","Kashmiri":"پھوگوبھی","Nepali":"काउली","Sindhi":"گوڀي","Konkani":"फुलकोबी","Dogri":"फुल गोभी","Manipuri":"ꯐꯨꯜꯒꯣꯕꯤ","Bodo":"ফুলকবি"},
    "Radish":{"English":"Radish","Hindi":"मूली","Bengali":"মূলা","Telugu":"మూలంగి","Marathi":"मुळा","Tamil":"முள்ளங்கி","Urdu":"مولی","Gujarati":"મૂળા","Kannada":"ಮೂಲಂಗಿ","Odia":"ମୂଳା","Malayalam":"മുള്ളൻ","Punjabi":"ਮੂਲੀ","Assamese":"মূলা","Maithili":"मूरी","Sanskrit":"मूलकम्","Kashmiri":"مولی","Nepali":"मूला","Sindhi":"مولي","Konkani":"मूळो","Dogri":"मूली","Manipuri":"ꯃꯨꯜꯂꯥ","Bodo":"মূলা"},
    "Bottle Gourd":{"English":"Bottle Gourd","Hindi":"लौकी","Bengali":"লাউ","Telugu":"సొరకాయ","Marathi":"दुधी","Tamil":"சுரைக்காய்","Urdu":"لوکی","Gujarati":"દૂધી","Kannada":"ಹೀರೆಕಾಯಿ","Odia":"ଲାଉ","Malayalam":"ചുരക്ക","Punjabi":"ਘੀਆ","Assamese":"জাতিলাউ","Maithili":"लौकी","Sanskrit":"अलाबुः","Kashmiri":"لوکی","Nepali":"लौका","Sindhi":"لوڪي","Konkani":"दुधी","Dogri":"घिया","Manipuri":"ꯂꯧꯀꯤ","Bodo":"লাউ"},
    "Beetroot":{"English":"Beetroot","Hindi":"चुकंदर","Bengali":"বিট","Telugu":"దుంప","Marathi":"बीट","Tamil":"பீட்ரூட்","Urdu":"چقندر","Gujarati":"બીટ","Kannada":"ಬೀಟ್ರೂಟ್","Odia":"ବିଟ","Malayalam":"ബീറ്റ്റൂട്ട്","Punjabi":"ਚੁਕੰਦਰ","Assamese":"বিট","Maithili":"चुकंदर","Sanskrit":"पालङ्कः","Kashmiri":"چقندر","Nepali":"चुकन्दर","Sindhi":"چقندر","Konkani":"बिट","Dogri":"चुकंदर","Manipuri":"ꯆꯨꯀꯟꯗꯔ","Bodo":"বিট"},
    "Black Gram":{"English":"Black Gram","Hindi":"उड़द","Bengali":"কালো ডাল","Telugu":"మినుములు","Marathi":"उडीद","Tamil":"உளுந்து","Urdu":"اڑد","Gujarati":"અડદ","Kannada":"ಉದ್ದು","Odia":"ବିରି","Malayalam":"ഉഴുന്ന്","Punjabi":"ਮਾਂਹ","Assamese":"বৰালি","Maithili":"उरद","Sanskrit":"माषः","Kashmiri":"اڑد","Nepali":"मास","Sindhi":"اڙد","Konkani":"उडीद","Dogri":"माह","Manipuri":"ꯃꯥꯁ","Bodo":"বৰালি"},
    "Horse Gram":{"English":"Horse Gram","Hindi":"कुलथी","Bengali":"কুলথি","Telugu":"ఉలవలు","Marathi":"कुळीथ","Tamil":"கொள்ளு","Urdu":"کلتھی","Gujarati":"કળથી","Kannada":"ಹುರಳಿ","Odia":"କୋଳଥ","Malayalam":"മുതിര","Punjabi":"ਕੁਲਥੀ","Assamese":"মাটিমাহ","Maithili":"कुलथी","Sanskrit":"कुलत्थः","Kashmiri":"کلتھی","Nepali":"गहत","Sindhi":"ڪلٿي","Konkani":"कुळीथ","Dogri":"कुलथी","Manipuri":"ꯀꯨꯂꯊꯤ","Bodo":"মাটিমাহ"},
    "Rubber":{"English":"Rubber","Hindi":"रबड़","Bengali":"রাবার","Telugu":"రబ్బరు","Marathi":"रबर","Tamil":"ரப்பர்","Urdu":"ربڑ","Gujarati":"રબર","Kannada":"ರಬ್ಬರ್","Odia":"ରବର","Malayalam":"റബ്ബർ","Punjabi":"ਰਬੜ","Assamese":"ৰবৰ","Maithili":"रबर","Sanskrit":"रबरः","Kashmiri":"ربڑ","Nepali":"रबर","Sindhi":"ربر","Konkani":"रबर","Dogri":"रबड़","Manipuri":"ꯔꯥꯕꯔ","Bodo":"ৰাবাৰ"},
    "Orange":{"English":"Orange","Hindi":"संतरा","Bengali":"কমলা","Telugu":"నారింజ","Marathi":"संत्रा","Tamil":"ஆரஞ்சு","Urdu":"نارنگی","Gujarati":"નારંગી","Kannada":"ಕಿತ್ತಳೆ","Odia":"କମଳା","Malayalam":"ഓറഞ്ച്","Punjabi":"ਸੰਤਰਾ","Assamese":"কমলা","Maithili":"संतरा","Sanskrit":"नारङ्गम्","Kashmiri":"نارنگ","Nepali":"सुन्तला","Sindhi":"نارنگي","Konkani":"संत्रे","Dogri":"संतरा","Manipuri":"ꯅꯥꯔꯤꯡꯒꯤ","Bodo":"কমলা"},
    "Arecanut":{"English":"Arecanut","Hindi":"सुपारी","Bengali":"সুপারি","Telugu":"వక్క","Marathi":"सुपारी","Tamil":"கமுகு","Urdu":"سپاری","Gujarati":"સોપારી","Kannada":"ಅಡಿಕೆ","Odia":"ଗୁଆ","Malayalam":"അടക്ക","Punjabi":"ਸੁਪਾਰੀ","Assamese":"তামোল","Maithili":"सुपारी","Sanskrit":"पूगफलम्","Kashmiri":"سپاری","Nepali":"सुपारी","Sindhi":"سپاري","Konkani":"सुपारी","Dogri":"सुपारी","Manipuri":"ꯁꯨꯄꯥꯔꯤ","Bodo":"তামোল"},
    "Jute":{"English":"Jute","Hindi":"जूट","Bengali":"পাট","Telugu":"జనపనార","Marathi":"ताग","Tamil":"சணல்","Urdu":"جوٹ","Gujarati":"શણ","Kannada":"ಸೆಣಬು","Odia":"ପାଟ","Malayalam":"ചണം","Punjabi":"ਜੂਟ","Assamese":"মৰাপাট","Maithili":"पटसन","Sanskrit":"पटशणः","Kashmiri":"جوٹ","Nepali":"जुट","Sindhi":"جوٽ","Konkani":"तागो","Dogri":"जूट","Manipuri":"ꯁꯟꯕꯩ","Bodo":"পাট"},
    "Flax":{"English":"Flax","Hindi":"अलसी","Bengali":"তিসি","Telugu":"అవిసె","Marathi":"जवस","Tamil":"ஆளி","Urdu":"السی","Gujarati":"અળસી","Kannada":"ಅಗಸೆ","Odia":"ଅଳସୀ","Malayalam":"ചണ","Punjabi":"ਅਲਸੀ","Assamese":"তিচি","Maithili":"तीसी","Sanskrit":"उमाः","Kashmiri":"السی","Nepali":"आलस","Sindhi":"السي","Konkani":"जवस","Dogri":"तीसी","Manipuri":"ꯑꯂꯁꯤ","Bodo":"তিচি"},
    "Cardamom":{"English":"Cardamom","Hindi":"इलायची","Bengali":"এলাচ","Telugu":"ఏలకులు","Marathi":"वेलची","Tamil":"ஏலக்காய்","Urdu":"الائچی","Gujarati":"એલચી","Kannada":"ಏಲಕ್ಕಿ","Odia":"ଏଲାଚି","Malayalam":"ഏലക്കാ","Punjabi":"ਇਲਾਇਚੀ","Assamese":"এলাচী","Maithili":"इलायची","Sanskrit":"एला","Kashmiri":"الائچی","Nepali":"अलैँची","Sindhi":"الائچي","Konkani":"वेलदोडे","Dogri":"इलायची","Manipuri":"ꯏꯂꯥꯏꯆꯤ","Bodo":"এলাচ"},
    "Clove":{"English":"Clove","Hindi":"लौंग","Bengali":"লবঙ্গ","Telugu":"లవంగాలు","Marathi":"लवंग","Tamil":"கிராம்பு","Urdu":"لونگ","Gujarati":"લવિંગ","Kannada":"ಲವಂಗ","Odia":"ଲବଙ୍ଗ","Malayalam":"ഗ്രാമ്പൂ","Punjabi":"ਲੌਂਗ","Assamese":"লং","Maithili":"लौंग","Sanskrit":"लवङ्गम्","Kashmiri":"لونگ","Nepali":"लवङ्ग","Sindhi":"لونگ","Konkani":"लवंग","Dogri":"लौंग","Manipuri":"ꯂꯧꯡ","Bodo":"লং"},
    "Black Pepper":{"English":"Black Pepper","Hindi":"काली मिर्च","Bengali":"গোলমরিচ","Telugu":"మిరియాలు","Marathi":"काळी मिरी","Tamil":"மிளகு","Urdu":"کالی مرچ","Gujarati":"કાળા મરી","Kannada":"ಕರಿಮೆಣಸು","Odia":"ଗୋଲମରିଚ","Malayalam":"കുരുമുളക്","Punjabi":"ਕਾਲੀ ਮਿਰਚ","Assamese":"জলকীয়া","Maithili":"कालीमिर्च","Sanskrit":"मरीचम्","Kashmiri":"مرچ","Nepali":"मरिच","Sindhi":"ڪارو مرچ","Konkani":"मिरसांग","Dogri":"काली मिर्च","Manipuri":"ꯃꯔꯣꯜ","Bodo":"জলকীয়া"},
}

def crop_name(crop, lang):
    """Localized crop name with graceful fallback if a cell is missing."""
    row = CROP_NAMES.get(crop, {})
    return row.get(lang, row.get("Hindi", row.get("English", crop)))
CN = crop_name

# ══════════════════════════════════════════════════════════════
# CROP DATABASE — (soil,rain,temp,sun,season,water/day,grow_days,
# price/kg,pest_risk,npk,row_cm,plant_cm,depth_cm,seeds/hole)
# ══════════════════════════════════════════════════════════════
CROP_DB = {
    "Rice":         (80,90,25,60,"Kharif",   12,120, 22,"High",  "N:120 P:60 K:60",  20,  5,  2, 2),
    "Wheat":        (60,40,20,70,"Rabi",      8,120, 20,"Medium","N:120 P:60 K:40",  22,  5,  5, 1),
    "Maize":        (65,50,25,75,"Kharif",   10, 90, 18,"Medium","N:150 P:75 K:50",  75, 25,  5, 1),
    "Millets":      (40,30,30,80,"Kharif",    4, 75, 15,"Low",   "N:40 P:20 K:20",   45, 15,  2, 2),
    "Cotton":       (50,40,35,85,"Kharif",    9,180, 60,"High",  "N:120 P:60 K:60", 100, 60,  3, 1),
    "Sugarcane":    (85,80,28,70,"Annual",   15,365, 35,"Medium","N:250 P:115 K:115",90, 30, 10, 1),
    "Barley":       (55,35,18,65,"Rabi",      6, 90, 18,"Low",   "N:60 P:30 K:20",   22,  5,  5, 1),
    "Soybean":      (60,60,27,70,"Kharif",    8,100, 45,"Medium","N:20 P:60 K:40",   45, 10,  3, 1),
    "Groundnut":    (50,40,30,80,"Kharif",    7,120, 70,"Medium","N:25 P:50 K:75",   30, 10,  5, 2),
    "Mustard":      (45,30,20,75,"Rabi",      5,110, 55,"Low",   "N:80 P:40 K:40",   45, 15,  1, 1),
    "Tea":          (80,85,22,60,"Annual",   14,365,200,"High",  "N:60 P:30 K:30",  120, 60, 10, 1),
    "Coffee":       (75,80,24,65,"Annual",   12,365,300,"Medium","N:40 P:30 K:40",  300,150, 30, 1),
    "Rubber":       (85,90,27,60,"Annual",   10,365,180,"Low",   "N:50 P:35 K:50",  600,400, 30, 1),
    "Banana":       (90,85,30,70,"Annual",   13,365, 25,"High",  "N:200 P:60 K:300",180, 90, 30, 1),
    "Mango":        (70,50,35,85,"Annual",    8,365, 80,"Medium","N:1000 P:500 K:1000",1000,800,60,1),
    "Apple":        (60,40,15,60,"Annual",    9,365,100,"High",  "N:70 P:35 K:70",  500,400, 60, 1),
    "Orange":       (65,50,25,70,"Annual",    8,365, 60,"Medium","N:600 P:300 K:600",600,500, 60, 1),
    "Potato":       (55,45,20,60,"Rabi",     10, 90, 20,"High",  "N:150 P:100 K:150",60, 25, 10, 1),
    "Tomato":       (60,50,25,70,"Annual",   11, 70, 25,"High",  "N:120 P:80 K:100", 75, 60,  1, 1),
    "Onion":        (50,40,28,75,"Rabi",      7,120, 30,"Medium","N:100 P:50 K:80",  15, 10,  2, 1),
    "Garlic":       (45,35,22,70,"Rabi",      6,150,100,"Low",   "N:100 P:50 K:80",  15,  8,  5, 1),
    "Peas":         (55,50,18,65,"Rabi",      7, 75, 50,"Low",   "N:20 P:60 K:40",   45, 10,  3, 2),
    "Cabbage":      (60,55,20,60,"Rabi",      9, 90, 15,"Medium","N:120 P:60 K:60",  60, 45,  1, 1),
    "Cauliflower":  (65,60,22,60,"Rabi",      9, 90, 20,"Medium","N:120 P:60 K:60",  60, 45,  1, 1),
    "Spinach":      (70,60,18,55,"Rabi",     10, 45, 30,"Low",   "N:80 P:40 K:40",   30, 15,  1, 4),
    "Brinjal":      (60,50,28,75,"Annual",   10, 90, 20,"High",  "N:100 P:50 K:75",  75, 60,  1, 1),
    "Chilli":       (55,45,30,80,"Annual",    9,150, 80,"High",  "N:100 P:50 K:75",  60, 45,  1, 1),
    "Turmeric":     (70,75,27,65,"Kharif",   11,270,120,"Low",   "N:30 P:20 K:60",   45, 25,  5, 1),
    "Ginger":       (75,80,25,60,"Kharif",   12,240,100,"Medium","N:75 P:50 K:100",  40, 20,  5, 1),
    "Cardamom":     (80,85,24,55,"Annual",   13,365,800,"Medium","N:40 P:30 K:60",  300,200, 10, 1),
    "Clove":        (75,80,26,60,"Annual",   11,365,600,"Low",   "N:30 P:20 K:40",  600,400, 30, 1),
    "Black Pepper": (80,85,27,65,"Annual",   12,365,400,"Medium","N:100 P:40 K:140",300,200, 10, 1),
    "Coconut":      (85,90,28,75,"Annual",   10,365, 30,"Low",   "N:500 P:320 K:1200",750,750,60,1),
    "Arecanut":     (80,85,27,70,"Annual",   11,365,350,"Low",   "N:100 P:40 K:140",270,270, 60, 1),
    "Jute":         (85,90,26,60,"Kharif",   12,120, 25,"Low",   "N:60 P:30 K:30",   30,  5,  1, 3),
    "Flax":         (60,50,20,65,"Rabi",      6,120, 90,"Low",   "N:60 P:30 K:30",   30,  5,  2, 2),
    "Sunflower":    (50,40,28,85,"Kharif",    7, 90, 55,"Low",   "N:80 P:60 K:40",   60, 30,  3, 1),
    "Sesame":       (45,35,30,85,"Kharif",    5, 90,120,"Low",   "N:30 P:15 K:15",   45, 10,  1, 3),
    "Lentils":      (50,40,22,70,"Rabi",      5,110, 70,"Low",   "N:20 P:40 K:20",   30, 10,  3, 2),
    "Chickpea":     (55,35,25,75,"Rabi",      5,110, 60,"Medium","N:20 P:40 K:20",   30, 10,  5, 1),
    "Pigeon Pea":   (60,45,28,80,"Kharif",    6,180, 65,"Medium","N:20 P:40 K:20",  120, 30,  3, 1),
    "Green Gram":   (55,40,27,75,"Kharif",    6, 65, 70,"Low",   "N:20 P:40 K:20",   30, 10,  3, 2),
    "Black Gram":   (50,40,28,75,"Kharif",    6, 75, 75,"Low",   "N:20 P:40 K:20",   30, 10,  3, 2),
    "Horse Gram":   (40,30,30,85,"Kharif",    3, 90, 40,"Low",   "N:15 P:25 K:25",   45, 15,  3, 2),
    "Rajma":        (55,45,20,65,"Rabi",      7,120,100,"Low",   "N:20 P:40 K:20",   60, 20,  5, 1),
    "Beetroot":     (60,50,20,60,"Rabi",      8, 90, 25,"Low",   "N:100 P:50 K:100", 30, 10,  2, 1),
    "Carrot":       (65,55,18,60,"Rabi",      8, 90, 30,"Low",   "N:100 P:60 K:80",  30,  5,  1, 2),
    "Radish":       (60,50,18,60,"Rabi",      7, 30, 15,"Low",   "N:80 P:40 K:40",   30,  5,  1, 2),
    "Pumpkin":      (70,60,28,75,"Kharif",    9, 90, 20,"Low",   "N:100 P:60 K:80", 200,150,  3, 2),
    "Bottle Gourd": (65,55,28,70,"Kharif",    9, 75, 18,"Low",   "N:100 P:60 K:80", 200,150,  3, 2),
}

PEST_MAP = {
    "Rice":        ["Brown Planthopper","Stem Borer","Leaf Folder"],
    "Wheat":       ["Aphids","Yellow Rust","Karnal Bunt"],
    "Cotton":      ["Pink Bollworm","Whitefly","Thrips"],
    "Tomato":      ["Fruit Borer","Whitefly","Early Blight"],
    "Potato":      ["Late Blight","Aphids","Cutworm"],
    "Maize":       ["Fall Armyworm","Stem Borer","Aphids"],
    "Sugarcane":   ["Pyrilla","Woolly Aphid","Top Borer"],
    "Chilli":      ["Thrips","Mites","Anthracnose"],
    "Banana":      ["Sigatoka","Weevil","Panama Wilt"],
    "Groundnut":   ["Leaf Spot","Rust","Tikka Disease"],
}

def crop_loss_risk(soil, rain, temp, gas, humidity, wind):
    risks, loss = [], 0
    if rain > 85:   risks.append(("flood", 30));  loss += 30
    if soil < 20:   risks.append(("drought", 35)); loss += 35
    if temp > 42:   risks.append(("heat", 20));    loss += 20
    if temp < 5:    risks.append(("frost", 40));   loss += 40
    if humidity>85: risks.append(("fungal", 15));  loss += 15
    if gas > 70:    risks.append(("gas", 50));      loss += 50
    if wind > 70:   risks.append(("wind", 10));      loss += 10
    return risks, min(loss, 90)

RISK_LABELS = {
    "flood":  M("Flood / waterlogging","बाढ़ / जलभराव","বন্যা / জলাবদ্ধতা","వరద / నీటి నిల్వ","पूर / जलसाठा","வெள்ளம் / நீர்த்தேக்கம்","سیلاب / پانی جمع","પૂર / પાણી ભરાવો","ಪ್ರವಾಹ / ನೀರು ನಿಲುಗಡೆ","ବନ୍ୟା / ଜଳ ଜମାଟ","വെള്ളപ്പൊക്കം / വെള്ളക്കെട്ട്","ਹੜ੍ਹ / ਪਾਣੀ ਖੜ੍ਹਾ","বান / পানী জমা","बाढ़ि / पानि जमाव","बाढः / जलावरोधः","سیلاب / آب زیادتی","बाढी / पानी जम्मा","ٻوڏ / پاڻي بيهڻ","पूर / उदक साठो","बाढ़ / पानी खड्डा","ꯏꯆꯥꯎ / ꯏꯁꯤꯡ ꯂꯦꯞꯄ","बाढ़ / पानी खड्डा"),
    "drought":M("Drought stress","सूखा तनाव","খরা চাপ","కరువు ఒత్తిడి","दुष्काळ ताण","வறட்சி அழுத்தம்","خشک سالی دباؤ","દુષ્કાળ તણાવ","ಬರ ಒತ್ತಡ","ମରୁଡ଼ି ଚାପ","വരൾച്ചാ സമ്മർദ്ദം","ਸੋਕਾ ਤਣਾਅ","খৰাং চাপ","सुखाड़ तनाव","अनावृष्टिः","خشڪ سالی دباؤ","खडेरी दबाब","سڪار دٻاءُ","दुष्काळ ताण","सुखा तनाव","ꯃꯤꯡꯗꯤ ꯐꯤꯕ","सुखा तनाव"),
    "heat":   M("Heat stress","गर्मी तनाव","তাপ চাপ","వేడి ఒత్తిడి","उष्णता ताण","வெப்ப அழுத்தம்","گرمی کا دباؤ","ગરમી તણાવ","ಶಾಖ ಒತ್ತಡ","ଉତ୍ତାପ ଚାପ","ചൂട് സമ്മർദ്ദം","ਗਰਮੀ ਤਣਾਅ","গৰম চাপ","गर्मी तनाव","उष्णता","گرمی دباؤ","गर्मी दबाब","گرمي دٻاءُ","उश्णता ताण","गर्मी तनाव","ꯑꯇꯤꯌꯥ ꯐꯤꯕ","गर्मी तनाव"),
    "frost":  M("Frost damage risk","पाला खतरा","কুয়াশা ক্ষতি","మంచు నష్టం","गारपीट धोका","உறைபனி சேதம்","پالا نقصان","ઠાર જોખમ","ಮಂಜು ಹಾನಿ","କୁହୁଡ଼ି କ୍ଷତି","മഞ്ഞ് നാശം","ਪਾਲਾ ਖਤਰਾ","শিশিৰ ক্ষতি","पाला खतरा","हिमपातः","برف نقصان","पाला जोखिम","سيءَ جو نقصان","गारपीट धोको","पाला खतरा","ꯏꯁꯤꯡ ꯀꯛꯄ ꯃꯥꯡꯍꯟꯕ","पाला खतरा"),
    "fungal": M("Fungal disease risk","फफूंद रोग खतरा","ছত্রাক রোগ ঝুঁকি","శిలీంధ్ర వ్యాధి","बुरशी रोग धोका","பூஞ்சை நோய் அபாயம்","پھپھوندی خطرہ","ફૂગ રોગ જોખમ","ಶಿಲೀಂಧ್ರ ರೋಗ","ଫଙ୍ଗସ ରୋଗ","കുമിൾ രോഗ സാധ്യത","ਉੱਲੀ ਰੋਗ ਖਤਰਾ","ফাঙাচ ৰোগ","फफूंद रोग खतरा","कवकरोगः","پھپھونڈی خطرہ","फफूँद रोग जोखिम","بيماري خطرو","बुरशी रोग धोको","फफूंद रोग खतरा","ꯁꯦꯛꯀꯤ ꯂꯥꯏꯅ","फफूंद रोग खतरा"),
    "gas":    M("Toxic gas alert","विषैली गैस चेतावनी","বিষাক্ত গ্যাস সতর্কতা","విషవాయు హెచ్చరిక","विषारी वायू इशारा","விஷ வாயு எச்சரிக்கை","زہریلی گیس انتباہ","ઝેરી ગેસ ચેતવણી","ವಿಷಕಾರಿ ಅನಿಲ ಎಚ್ಚರಿಕೆ","ବିଷାକ୍ତ ଗ୍ୟାସ ସତର୍କତା","വിഷ വാതക മുന്നറിയിപ്പ്","ਜ਼ਹਿਰੀਲੀ ਗੈਸ ਚੇਤਾਵਨੀ","বিষাক্ত গেছ সতৰ্কতা","विषैल गैस चेतावनी","विषवायु सूचना","زہریلی گیس وارننگ","विषालु ग्यास चेतावनी","زھريلي گئس خبردار","विषारी ग्यास इशारो","ज़हरीली गैस चेतावनी","ꯑꯆꯨꯕ ꯒꯦꯁ ꯑꯦꯂꯥꯔꯠ","ज़हरीली गैस चेतावनी"),
    "wind":   M("High-wind lodging risk","तेज़ हवा से गिरने का खतरा","প্রবল বাতাসে পড়ে যাওয়ার ঝুঁকি","గాలికి పంట పడిపోయే ప్రమాదం","जोरदार वाऱ्याने पीक कोसळण्याचा धोका","அதிக காற்றால் விழும் அபாயம்","تیز ہوا سے گرنے کا خطرہ","તેજ પવનથી પડવાનું જોખમ","ಜೋರು ಗಾಳಿಯಿಂದ ಬೀಳುವ ಅಪಾಯ","ପ୍ରବଳ ପବନରେ ପଡ଼ିବାର ବିପଦ","ശക്തമായ കാറ്റിൽ വീഴാനുള്ള സാധ്യത","ਤੇਜ਼ ਹਵਾ ਨਾਲ ਡਿੱਗਣ ਦਾ ਖਤਰਾ","প্ৰবল বতাহত পৰাৰ আশংকা","तेज़ हवा सँ खसबाक खतरा","प्रबलवायुना पतनजोखिमः","تیز ہوا کھۄسنُک خطرہ","चर्को हावाले लड्ने जोखिम","تيز هوا سان ڪري پوڻ جو خطرو","जोरदार वाऱ्यान पीक कोसळपाचो धोको","तेज़ हवा कन्नै डिगणे दा खतरा","ꯍꯧꯖꯤꯛ ꯅꯨꯡꯁꯤꯠꯅ ꯇꯨꯕꯒꯤ ꯐꯤꯕ","तेज़ हवा कन्नै डिगणे दा खतरा"),
}

# ══════════════════════════════════════════════════════════════
# GOVERNMENT SCHEMES — name kept as official short-form (unchanged
# across languages, matching real govt usage), description translated.
# ══════════════════════════════════════════════════════════════
GOV_SCHEMES = [
    ("PM-KISAN", "https://pmkisan.gov.in", M(
        "₹6,000/year paid directly to your bank account","बैंक खाते में सीधे ₹6,000/वर्ष","ব্যাংক অ্যাকাউন্টে সরাসরি ₹৬,০০০/বছর","బ్యాంక్ ఖాతాలో నేరుగా ₹6,000/సంవత్సరం","बँक खात्यात थेट ₹6,000/वर्ष","வங்கிக் கணக்கில் நேரடியாக ₹6,000/ஆண்டு","بینک اکاؤنٹ میں براہ راست ₹6,000/سال","બેંક ખાતામાં સીધા ₹6,000/વર્ષ","ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರವಾಗಿ ₹6,000/ವರ್ಷ","ବ୍ୟାଙ୍କ ଖାତାରେ ସିଧାସଳଖ ₹6,000/ବର୍ଷ","ബാങ്ക് അക്കൗണ്ടിലേക്ക് നേരിട്ട് ₹6,000/വർഷം","ਬੈਂਕ ਖਾਤੇ ਵਿੱਚ ਸਿੱਧੇ ₹6,000/ਸਾਲ","বেংক একাউণ্টত পোনপটীয়াকৈ ₹৬,০০০/বছৰ","बैंक खाता में सीधे ₹6,000/साल","बैंकखाते सीधं ₹6,000/वर्षम्","بینک کھاتہٕ سیدھا ₹6,000/سال","बैंक खातामा सिधै ₹6,000/वर्ष","بئنڪ کاتي ۾ سڌو ₹6,000/سال","बँक खात्यांत सैमकार ₹6,000/वर्सा","बैंक खाते च सिद्धा ₹6,000/साल","ꯕꯦꯪꯀ ꯑꯦꯀꯥꯎꯟꯇ ₹6,000/ꯆꯍꯤ","बैंक खाते च सिद्धा ₹6,000/साल")),
    ("Kisan Credit Card", "https://www.nabard.org", M(
        "Crop loans up to ₹3 lakh at 4% interest","4% ब्याज पर ₹3 लाख तक फसल ऋण","৪% সুদে ₹৩ লাখ পর্যন্ত ফসল ঋণ","4% వడ్డీకి ₹3 లక్షల వరకు పంట రుణం","4% व्याजाने ₹3 लाख पर्यंत पीक कर्ज","4% வட்டியில் ₹3 லட்சம் வரை பயிர் கடன்","4% سود پر ₹3 لاکھ تک فصل قرض","4% વ્યાજે ₹3 લાખ સુધી પાક લોન","4% ಬಡ್ಡಿಗೆ ₹3 ಲಕ್ಷದವರೆಗೆ ಬೆಳೆ ಸಾಲ","4% ସୁଧରେ ₹3 ଲକ୍ଷ ପର୍ଯ୍ୟନ୍ତ ଫସଲ ଋଣ","4% പലിശയിൽ ₹3 ലക്ഷം വരെ വിള വായ്പ","4% ਵਿਆਜ ਤੇ ₹3 ਲੱਖ ਤੱਕ ਫਸਲ ਲੋਨ","৪% সুতত ₹৩ লাখলৈ শস্য ঋণ","4% ब्याज पर ₹3 लाख तक फसल कर्ज","4% वृद्ध्या ₹3 लक्षपर्यन्तं ऋणम्","4% سود پؠٹھ ₹3 لاکھ تام قرض","4% ब्याजमा ₹3 लाखसम्म बाली ऋण","4% وياج تي ₹3 لک تائين فصل قرض","4% व्याजान ₹3 लाखांमेरेन पीक कर्ज","4% ब्याज पर ₹3 लक्ख तक फसल कर्ज","₹3 ꯂꯤꯃꯤꯠ ꯐꯥꯗꯨꯡ ꯁꯦꯜ 4%","4% ब्याज पर ₹3 लक्ख तक फसल कर्ज")),
    ("PMFBY Crop Insurance", "https://pmfby.gov.in", M(
        "Just 2% premium — government covers the rest","सिर्फ 2% प्रीमियम — बाकी सरकार वहन करती है","মাত্র ২% প্রিমিয়াম — বাকি সরকার বহন করে","2% ప్రీమియం మాత్రమే — మిగతా ప్రభుత్వం","फक्त 2% प्रीमियम — उर्वरित सरकार भरते","2% பிரீமியம் மட்டும் — மீதி அரசு","صرف 2% پریمیم — باقی حکومت","ફક્ત 2% પ્રીમિયમ — બાકી સરકાર","ಕೇವಲ 2% ಪ್ರೀಮಿಯಂ — ಉಳಿದದ್ದು ಸರ್ಕಾರ","କେବଳ 2% ପ୍ରିମିୟମ — ବାକି ସରକାର","2% പ്രീമിയം മാത്രം — ബാക്കി സർക്കാർ","ਸਿਰਫ਼ 2% ਪ੍ਰੀਮੀਅਮ — ਬਾਕੀ ਸਰਕਾਰ","মাত্ৰ ২% প্ৰিমিয়াম — বাকী চৰকাৰ","सिर्फ 2% प्रीमियम — बाकी सरकार","केवलं 2% — शेषं सरकारः","صرف 2% پریمیم — باقی حکومت","जम्मा 2% प्रिमियम — बाँकी सरकार","رڳو 2% پریميم — باقي حڪومت","फकत 2% प्रीमियम — उरिल्लें सरकार","सिर्फ 2% प्रीमियम — बाकी सरकार","2% ꯄ꯭ꯔꯤꯃꯤꯌꯝ ꯈꯛꯇ — ꯑꯇꯩꯗꯨ ꯁꯔꯀꯥꯔꯅ","सिर्फ 2% प्रीमियम — बाकी सरकार")),
    ("eNAM Online Mandi", "https://www.enam.gov.in", M(
        "Sell your produce online at 1,000+ mandis","1,000+ मंडियों में ऑनलाइन उपज बेचें","১,০০০+ মান্ডিতে অনলাইনে ফসল বিক্রি","1,000+ మండీలలో ఆన్‌లైన్‌లో అమ్మండి","1,000+ बाजारपेठांत ऑनलाइन विक्री करा","1,000+ சந்தைகளில் ஆன்லைனில் விற்கவும்","1,000+ منڈیوں میں آن لائن فروخت کریں","1,000+ મંડીઓમાં ઓનલાઈન વેચો","1,000+ ಮಂಡಿಗಳಲ್ಲಿ ಆನ್‌ಲೈನ್ ಮಾರಾಟ","1,000+ ମଣ୍ଡିରେ ଅନଲାଇନ୍ ବିକ୍ରୟ","1,000+ ചന്തകളിൽ ഓൺലൈനിൽ വിൽക്കുക","1,000+ ਮੰਡੀਆਂ ਵਿੱਚ ਆਨਲਾਈਨ ਵੇਚੋ","১,০০০+ মাণ্ডিত অনলাইন বিক্ৰী","1,000+ मंडी मे ऑनलाइन बेचू","सहस्राधिकमण्डीषु ऑनलाइन विक्रयः","1,000+ منڈیو منز آن لائن وکنیو","1,000+ मण्डीमा अनलाइन बेच्नुहोस्","1,000+ منڊين ۾ آن لائين وڪرو","1,000+ बाजारांनी ऑनलायन विक","1,000+ मंडियां च आनलाइन बेचो","ꯃꯥꯟꯗꯤ 1,000+ ꯑꯣꯟꯂꯥꯏꯅ ꯌꯣꯟꯕ","1,000+ मंडियां च आनलाइन बेचो")),
    ("Soil Health Card", "https://soilhealth.dac.gov.in", M(
        "Free soil testing every 2 years","हर 2 साल में मुफ्त मिट्टी परीक्षण","প্রতি ২ বছরে বিনামূল্যে মাটি পরীক্ষা","ప్రతి 2 సంవత్సరాలకు ఉచిత నేల పరీక్ష","दर 2 वर्षांनी मोफत माती चाचणी","2 ஆண்டுகளுக்கு ஒருமுறை இலவச மண் பரிசோதனை","ہر 2 سال میں مفت مٹی ٹیسٹ","દર 2 વર્ષે મફત જમીન પરીક્ષણ","ಪ್ರತಿ 2 ವರ್ಷಕ್ಕೊಮ್ಮೆ ಉಚಿತ ಮಣ್ಣು ಪರೀಕ್ಷೆ","ପ୍ରତି 2 ବର୍ଷରେ ମାଗଣା ମାଟି ପରୀକ୍ଷା","2 വർഷത്തിലൊരിക്കൽ സൗജന്യ മണ്ണ് പരിശോധന","ਹਰ 2 ਸਾਲ ਮੁਫ਼ਤ ਮਿੱਟੀ ਟੈਸਟ","প্ৰতি ২ বছৰত বিনামূলীয়া মাটি পৰীক্ষা","हर 2 साल मे मुफ्त माटि परीक्षण","प्रति 2 वर्षं निःशुल्क मृदापरीक्षा","ہر 2 ورہٕ مفت مٹی امتحان","हरेक 2 वर्षमा निःशुल्क माटो परीक्षण","هر 2 سال مفت مٽي ٽيسٽ","दर 2 वर्सां फुकट माती चांचणी","हर 2 साल मुफ्त मिट्टी टैस्ट","ꯆꯍꯤ 2 ꯏꯄꯨꯅꯅ ꯂꯩ ꯆꯦꯛꯐꯝ","हर 2 साल मुफ्त मिट्टी टैस्ट")),
    ("PMKSY Drip Irrigation", "https://pmksy.gov.in", M(
        "55–75% subsidy on drip irrigation systems","ड्रिप सिंचाई पर 55-75% सब्सिडी","ড্রিপ সেচে 55-75% ভর্তুকি","డ్రిప్ నీటిపారుదలపై 55-75% సబ్సిడీ","ठिबक सिंचनावर 55-75% अनुदान","சொட்டு நீர்ப்பாசனத்தில் 55-75% மானியம்","ڈرپ آبپاشی پر 55-75% سبسڈی","ટપક સિંચાઈ પર 55-75% સબસિડી","ಹನಿ ನೀರಾವರಿಗೆ 55-75% ಸಬ್ಸಿಡಿ","ଡ୍ରିପ ଜଳସେଚନରେ 55-75% ସବସିଡି","തുള്ളിനന ജലസേചനത്തിന് 55-75% സബ്സിഡി","ਤੁਪਕਾ ਸਿੰਚਾਈ ਤੇ 55-75% ਸਬਸਿਡੀ","ড্ৰিপ জলসিঞ্চনত 55-75% ৰেহাই","ड्रिप सिंचाई पर 55-75% छूट","स्रवसिञ्चने 55-75% अनुदानम्","ڈرپ سینچہٕ پؠٹھ 55-75% سبسڈی","थोपा सिँचाइमा 55-75% अनुदान","ڊرپ آبپاشي تي 55-75% سبسڊي","ठिबक सिंचनार 55-75% अनुदान","ड्रिप सिंचाई पर 55-75% सब्सिडी","ꯗ꯭ꯔꯤꯞ ꯏꯁꯤꯡꯗ 55-75% ꯁꯕꯁꯤꯗꯤ","ड्रिप सिंचाई पर 55-75% सब्सिडी")),
    ("Paramparagat Krishi Vikas", "https://pgsindia-ncof.gov.in", M(
        "Support for switching to organic farming","जैविक खेती अपनाने हेतु सहायता","জৈব চাষে সহায়তা","సేంద్రియ వ్యవసాయానికి మద్దతు","सेंद्रिय शेतीसाठी सहाय्य","இயற்கை விவசாயத்திற்கு உதவி","نامیاتی کاشتکاری کے لیے مدد","જૈવિક ખેતી માટે સહાય","ಸಾವಯವ ಕೃಷಿಗೆ ಬೆಂಬಲ","ଜୈବିକ ଚାଷ ପାଇଁ ସହାୟତା","ജൈവ കൃഷിക്ക് പിന്തുണ","ਜੈਵਿਕ ਖੇਤੀ ਲਈ ਸਹਾਇਤਾ","জৈৱিক খেতিৰ বাবে সহায়","जैविक खेती लेल सहायता","जैविककृषये सहायता","نامیاتی کاشتکاری خٲطرہٕ مدد","जैविक खेतीको लागि सहयोग","نامياتي پوک لاءِ مدد","सेंद्रिय शेतीखातीर आदार","जैविक खेती आस्ते मदद","ꯑꯣꯔꯒꯦꯅꯤꯛ ꯂꯧꯅꯕ ꯃꯇꯦꯡ","जैविक खेती आस्ते मदद")),
]

# ══════════════════════════════════════════════════════════════
# CARD / UI HELPERS
# ══════════════════════════════════════════════════════════════
def card(title, body, icon="", tone="brand", extra_class=""):
    st.markdown(
        f"<div class='av-card av-tone-{tone} {extra_class}'><h4>{icon} {title}</h4>{body}</div>",
        unsafe_allow_html=True
    )

def card_grid(cards, ncols=3, gap="1rem", bottom_margin="1.5rem"):
    """Render a row of cards as a CSS Grid instead of st.columns().
    st.columns() creates independent column stacks with no shared height,
    so cards with more text end up visibly taller than their neighbors.
    CSS Grid rows auto-equalize to the tallest cell, so every card in the
    row always matches — regardless of how much text each one holds.
    cards: list of (title, body_html, icon, tone) tuples.
    """
    cells = "".join(
        f"<div class='av-card av-tone-{tone} av-card-grid'><h4>{icon} {title}</h4>{body}</div>"
        for title, body, icon, tone in cards
    )
    st.markdown(
        f"<div style='display:grid;grid-template-columns:repeat({ncols},1fr);"
        f"gap:{gap};align-items:stretch;margin-bottom:{bottom_margin};'>{cells}</div>",
        unsafe_allow_html=True
    )

def section(title, sub=""):
    st.markdown(
        f"<div class='av-section'><h3>{title}</h3>"
        f"{f'<div class=av-sub>{sub}</div>' if sub else ''}</div>",
        unsafe_allow_html=True
    )

def pill(text, tone="neutral"):
    return f"<span class='av-pill av-pill-{tone}'>{text}</span>"

def bar(pct, color="var(--brand)"):
    pct = max(0, min(100, pct))
    return (f"<div class='av-progress-track'>"
            f"<div class='av-progress-fill' style='width:{pct}%;background:{color};'></div></div>")

def status_tone(level):
    return {"high":"danger","medium":"warn","low":"ok","danger":"danger","safe":"ok"}.get(level, "neutral")

# ══════════════════════════════════════════════════════════════
# LANGUAGE SELECTION SCREEN
# ══════════════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.markdown(
        "<div class='av-hero'><h1>🌾 AGROVA</h1>"
        "<div class='av-hero-accent'></div>"
        "<p>AI-Powered Precision Farming Intelligence — 50 crops, 22 Indian languages</p></div>",
        unsafe_allow_html=True
    )
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        opts = [f"{k} · {v}" for k, v in LANG_NAMES.items()]
        chosen = st.selectbox("Select Language / भाषा चुनें", opts, label_visibility="collapsed")
        lang = chosen.split(" · ")[0]
        if st.button(T("enter_btn", lang), use_container_width=True):
            st.session_state.lang = lang
            st.rerun()
    st.stop()

lang = st.session_state.lang

# ══════════════════════════════════════════════════════════════
# SIDEBAR — inputs
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<h2>🌾 AGROVA</h2><p style='opacity:.85;'>{LANG_NAMES[lang]}</p>", unsafe_allow_html=True)
    if st.button(T("change_lang", lang), use_container_width=True):
        for k in ["lang", "messages", "sel_crop"]:
            st.session_state.pop(k, None)
        st.rerun()
    st.markdown("---")

    selected_state = st.selectbox("📍 State", INDIAN_STATES, index=INDIAN_STATES.index("Maharashtra"))
    st.markdown("---")

    soil     = st.slider(T("soil", lang), 0, 100, 55)
    temp     = st.slider(T("temp", lang), 0, 50, 26)
    rain     = st.slider(T("rain", lang), 0, 100, 45)
    sun      = st.slider(T("sun", lang), 0, 100, 65)
    fert     = st.slider(T("fert", lang), 0, 100, 35)
    gas      = st.slider(T("gas", lang), 0, 100, 8)
    humidity = st.slider(T("humidity", lang), 0, 100, 60)
    wind     = st.slider(T("wind", lang), 0, 100, 18)
    ph       = st.slider(T("ph", lang), 0, 14, 7)
    nitrogen = st.slider(T("nitrogen", lang), 0, 100, 40)
    st.markdown("---")
    farm_size   = st.number_input(T("farm_size", lang), 0.5, 100.0, 2.0, 0.5)
    farm_type   = st.selectbox(T("farm_type", lang), ["Conventional","Organic","Integrated","Hydroponic"])
    market_dist = st.slider(T("market_dist", lang), 1, 200, 30)
    st.markdown("---")
    simulate = st.button(T("run_btn", lang), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ANALYSIS SNAPSHOT — makes the "Run Full Analysis" button do
# something: on click, freeze the current readings so the
# dashboard can show what changed since the last run.
# ══════════════════════════════════════════════════════════════
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None
if "prev_analysis" not in st.session_state:
    st.session_state.prev_analysis = None
if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0
if "last_analysis_time" not in st.session_state:
    st.session_state.last_analysis_time = None

current_readings = {
    "soil": soil, "temp": temp, "rain": rain, "sun": sun, "fert": fert,
    "gas": gas, "humidity": humidity, "wind": wind, "ph": ph, "nitrogen": nitrogen,
}

if simulate:
    st.session_state.prev_analysis = st.session_state.last_analysis
    st.session_state.last_analysis = current_readings
    st.session_state.last_analysis_time = datetime.now()
    st.session_state.analysis_count += 1

# ══════════════════════════════════════════════════════════════
# SCORING — unchanged formula from the original tool
# ══════════════════════════════════════════════════════════════
def score_all_crops():
    scores = {}
    for crop, vals in CROP_DB.items():
        s, r, t, su = vals[0], vals[1], vals[2], vals[3]
        diff = (abs(soil-s) + abs(rain-r) + abs(temp-t) + abs(sun-su)) / 4
        ph_penalty = abs(ph - 6.5) * 2
        n_bonus = max(0, nitrogen - 30) * 0.1
        scores[crop] = round(max(0, 100 - diff - ph_penalty + n_bonus), 1)
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

if "sel_crop" not in st.session_state:
    st.session_state.sel_crop = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"

scores = score_all_crops()
sorted_crops = list(scores.items())
if st.session_state.sel_crop is None:
    st.session_state.sel_crop = sorted_crops[0][0]
sel = st.session_state.sel_crop
sv = CROP_DB[sel]
water_need, grow_days, price_kg, pest_risk_level, npk = sv[5], sv[6], sv[7], sv[8], sv[9]
row_sp, plant_sp, depth, seeds_hole = sv[10], sv[11], sv[12], sv[13]
crop_season = sv[4]
sc = scores[sel]

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
hc1, hc2 = st.columns([3, 1.6])
with hc1:
    st.markdown(
        f"<h1 style='margin-bottom:.3rem; font-size:2.6rem; line-height:1.15;'>🌾 {T('app_title', lang)}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='color:var(--muted); font-size:1.05rem; font-weight:500; margin-top:.2rem; margin-bottom:.6rem; letter-spacing:.01em;'>{T('app_sub', lang)}</p>",
        unsafe_allow_html=True
    )
    _dm = st.session_state.get("dark_mode", False)
    if st.button("☀️ Light Mode" if _dm else "🌙 Dark Mode", key="dm_toggle"):
        st.session_state.dark_mode = not _dm
        st.rerun()

with hc2:
    _dm = st.session_state.get("dark_mode", False)
    _clock_bg  = "#1e3530" if _dm else "#e8f6ee"
    _clock_col = "#3f9c88" if _dm else "#0f6b5c"
    _clock_bdr = "#2d4a42" if _dm else "#2d936c"
    _pill_bg   = "#1e3530" if _dm else "#e8f6ee"
    _pill_col  = "#3f9c88" if _dm else "#0f6b5c"
    _pill_bdr  = "#2d4a42" if _dm else "#b5d5c8"

    components.html(f"""
    <style>
      *{{box-sizing:border-box;margin:0;padding:0;}}
      body{{background:transparent;overflow:hidden;}}
      .wrap{{
        display:flex;flex-direction:column;align-items:flex-end;
        gap:10px;padding-top:6px;
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
      }}
      .pill{{
        text-align:center;font-size:.72rem;font-weight:700;
        color:{_pill_col};background:{_pill_bg};
        border:1.5px solid {_pill_bdr};border-radius:999px;
        padding:5px 14px;width:150px;white-space:nowrap;
        letter-spacing:.03em;line-height:1.5;
      }}
      #av-clock{{
        text-align:center;font-size:.78rem;font-weight:700;
        color:{_clock_col};background:{_clock_bg};
        border:1.5px solid {_clock_bdr};border-radius:8px;
        padding:5px 14px;width:150px;
        letter-spacing:.03em;line-height:1.6;
      }}
    </style>
    <div class="wrap">
      <div class="pill">📍 {selected_state}</div>
      <div id="av-clock">loading...</div>
    </div>
    <script>
    (function(){{
      function tick(){{
        var n=new Date(),
          D=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
          M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        document.getElementById('av-clock').innerHTML=
          '<div>'+D[n.getDay()]+' '+String(n.getDate()).padStart(2,'0')+
          ' '+M[n.getMonth()]+'</div><div>'+
          String(n.getHours()).padStart(2,'0')+':'+
          String(n.getMinutes()).padStart(2,'0')+':'+
          String(n.getSeconds()).padStart(2,'0')+'</div>';
      }}
      tick(); setInterval(tick,1000);
    }})();
    </script>
    """, height=105)

if st.session_state.get("dark_mode", False):
    st.markdown("""<style>
html,body,.stApp,.main,.block-container{background:#0d1a17 !important;}
header[data-testid="stHeader"]{background:#0d1a17 !important;}
[data-testid="stColorBlock"],[data-testid="stToolbarActionButtonIcon"],
[data-testid="stMainMenuButton"],[data-testid="stToolbarActions"]{display:none !important;}
section[data-testid="stSidebar"]{display:flex !important; visibility:visible !important; background:linear-gradient(180deg,#071410,#0c1e1a) !important;}
[data-testid="stSidebarCollapsedControl"]{display:flex !important; visibility:visible !important; pointer-events:all !important; background:#071410 !important;}
/* Kill every border/shadow on every container — the white vertical line */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="stSidebarContent"],
[data-testid="stForm"],
[data-testid="stNotification"],
[data-testid="stExpander"],
[data-testid="stExpanderDetails"],
section.main,
.main .block-container,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stBottom"] {
  border:none !important;
  border-right:none !important;
  border-left:none !important;
  border-top:none !important;
  border-bottom:none !important;
  outline:none !important;
  box-shadow:none !important;
  background:#0d1a17 !important;
}
/* Toolbar icons (share, star, pen, github, dots) — make them clearly visible */
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] a,
header[data-testid="stHeader"] svg,
header[data-testid="stHeader"] [data-testid="stToolbar"] *,
header[data-testid="stHeader"] [data-testid="stDecoration"],
[data-testid="stToolbar"] button,[data-testid="stToolbar"] svg,
[data-testid="stToolbar"] path {
  color:#dff0ea !important; fill:#dff0ea !important; stroke:#dff0ea !important; opacity:1 !important;
}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#071410,#0c1e1a) !important;}
.av-card{background:#162421 !important; border-color:#253d36 !important;}
.av-card p,.av-card li,.av-card td,.av-card th{color:#c8e6de !important;}
.av-card h4{color:#dff0ea !important;}
.av-card strong{color:#dff0ea !important;}
.stMetric{background:#162421 !important; border-color:#253d36 !important;}
.stMetric label{color:#6a9e94 !important;}
.stMetric [data-testid="stMetricValue"]{color:#3f9c88 !important;}
.stMetric [data-testid="stMetricDelta"]{color:#6a9e94 !important;}
.stTabs [data-baseweb="tab-list"]{background:#0d1a17 !important; border-color:#253d36 !important;}
.stTabs [data-baseweb="tab"]{color:#6a9e94 !important;}
.stTabs [aria-selected="true"]{background:#162421 !important; color:#3f9c88 !important;}
/* Body text — bumped to bright cream so it's easy on the eyes */
.stMarkdown p,.stMarkdown li,.stMarkdown span{color:#c8e6de !important;}
p, li, span, td, th, label { color:#c8e6de !important; }
h1,h2,h3,h4{color:#dff0ea !important;}
strong{color:#dff0ea !important;}
section[data-testid="stSidebar"] *{color:#dcefe9 !important;}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2{color:#fff !important;}
section[data-testid="stSidebar"] label{color:#b7d9cf !important;}
[data-baseweb="select"]>div{background:#162421 !important; border-color:#253d36 !important; color:#dff0ea !important;}
input,textarea{background:#162421 !important; color:#dff0ea !important; border-color:#253d36 !important;}
section[data-testid="stSidebar"] .stNumberInput input{background:rgba(255,255,255,.1) !important; color:#dff0ea !important; border-color:rgba(255,255,255,.2) !important;}
/* All buttons dark-styled, including the Light Mode toggle */
.stButton>button{background:#2d7a68 !important; color:#fff !important; border:none !important;}
.stButton>button p,.stButton>button span,.stButton>button div{color:#fff !important;}
.av-section h3{color:#e63946 !important;}
.av-progress-track{background:#1f3a30 !important;}
[data-testid="stSlider"] [data-testid="stTickBar"]{background:#253d36 !important;}
.av-pill-neutral{background:#1e3530 !important; color:#c8e6de !important; border-color:#2d4a42 !important;}
.av-pill{color:#c8e6de !important;}
.av-tone-danger{background:#2c0c09 !important;}
.av-tone-warn{background:#271c00 !important;}
.av-tone-ok{background:#0b2418 !important;}
.av-tone-info{background:#091d2c !important;}
.av-crop-tile{background:#162421 !important; border-color:#253d36 !important;}
.av-crop-tile .rank{color:#8ec4b8 !important;}
.av-crop-tile .name{color:#dff0ea !important;}
.av-crop-tile .score{color:#3f9c88 !important;}
.av-crop-tile.sel{background:#1e3530 !important; border-color:#3f9c88 !important;}
/* Dark ALL wrappers — no white gaps or borders anywhere */
.stApp, .stApp > *, .main, .main > *,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > *,
[data-testid="stAppViewBlockContainer"],
[data-testid="stAppViewBlockContainer"] > *,
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlock"] > *,
[data-testid="stHorizontalBlock"],
[data-testid="stHorizontalBlock"] > *,
[data-testid="column"],
[data-testid="column"] > *,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > *,
.element-container,
.stMarkdown,
.block-container,
.block-container > *,
section.main,
section.main > * {
  background:#0d1a17 !important;
  border-color:#0d1a17 !important;
  border:none !important;
  outline:none !important;
  box-shadow:none !important;
}
/* Restore specific component backgrounds and borders */
.av-card { background:#162421 !important; border-color:#253d36 !important; box-shadow:none !important; }
.av-crop-tile { background:#162421 !important; border-color:#253d36 !important; }
.av-crop-tile.sel { background:#1e3530 !important; border-color:#3f9c88 !important; }
.stMetric { background:#162421 !important; border-color:#253d36 !important; }
.av-tone-danger { background:#2c0c09 !important; border-color:#5c1a15 !important; }
.av-tone-warn { background:#271c00 !important; border-color:#4a3500 !important; }
.av-tone-ok { background:#0b2418 !important; border-color:#1a4a30 !important; }
.av-tone-info { background:#091d2c !important; border-color:#0f3a52 !important; }
[data-baseweb="select"]>div { background:#162421 !important; border-color:#253d36 !important; }
input, textarea { background:#162421 !important; border-color:#253d36 !important; }
.st-key-navtabs{border-color:#253d36 !important;}
.st-key-navtabs .stButton>button[kind="secondary"] p,
.st-key-navtabs .stButton>button[kind="secondary"] span,
.st-key-navtabs .stButton>button[kind="secondary"] div{color:#9ec4bb !important;}
.st-key-navtabs .stButton>button[kind="primary"]{background:#162421 !important; box-shadow:0 -3px 0 #3f9c88 inset !important;}
.st-key-navtabs .stButton>button[kind="primary"] p,
.st-key-navtabs .stButton>button[kind="primary"] span,
.st-key-navtabs .stButton>button[kind="primary"] div{color:#3f9c88 !important;}
</style>""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

if gas > 70:
    card(f"{L['danger'][lang]} — {RISK_LABELS['gas'][lang]}",
         f"<p><strong>{T('gas', lang)}: {gas}%</strong> — evacuate the area, avoid electrical switches, call 101.</p>",
         icon="☠️", tone="danger")

risks, loss_pct = crop_loss_risk(soil, rain, temp, gas, humidity, wind)

# ══════════════════════════════════════════════════════════════
# NAV BAR — real buttons wired to session_state, replacing st.tabs()
# so the active section can be switched programmatically (e.g. when
# a crop tile is clicked). st.tabs() has no supported way to be
# switched from Python, which is why that approach never worked.
# ══════════════════════════════════════════════════════════════
NAV_ITEMS = [
    ("dashboard", "📊 " + T("tab_dashboard", lang)),
    ("advisor",   "🌾 " + T("tab_advisor", lang)),
    ("finance",   "💧 " + T("tab_finance", lang)),
    ("schemes",   "🏛️ " + T("tab_schemes", lang)),
    ("chat",      "💬 " + T("tab_chat", lang)),
]
# Scoped to .st-key-navtabs ONLY, so it never touches other buttons
# in the app (e.g. the Light/Dark Mode toggle, which was broken by
# an earlier unscoped [kind="secondary"] rule).
st.markdown("""<style>
.st-key-navtabs{border-bottom:1px solid var(--border); margin-bottom:1rem; padding-bottom:2px;}
.st-key-navtabs .stButton>button{
  transition:background-color .22s ease, color .22s ease, box-shadow .22s ease, transform .12s ease !important;
}
.st-key-navtabs .stButton>button:active{transform:scale(.97);}
.st-key-navtabs .stButton>button[kind="secondary"]{
  background:transparent !important; border:none !important; box-shadow:none !important;
}
.st-key-navtabs .stButton>button[kind="secondary"] p,
.st-key-navtabs .stButton>button[kind="secondary"] span,
.st-key-navtabs .stButton>button[kind="secondary"] div{
  color:var(--ink-soft) !important; font-weight:600 !important;
}
.st-key-navtabs .stButton>button[kind="secondary"]:hover{background:var(--bg-alt) !important;}
.st-key-navtabs .stButton>button[kind="primary"]{
  background:var(--surface) !important; border:none !important;
  box-shadow:0 -3px 0 var(--brand) inset !important;
}
.st-key-navtabs .stButton>button[kind="primary"] p,
.st-key-navtabs .stButton>button[kind="primary"] span,
.st-key-navtabs .stButton>button[kind="primary"] div{
  color:var(--brand) !important; font-weight:700 !important;
}
</style>""", unsafe_allow_html=True)

with st.container(key="navtabs"):
    nav_cols = st.columns(len(NAV_ITEMS))
    for col, (nav_key, nav_label) in zip(nav_cols, NAV_ITEMS):
        with col:
            is_active = st.session_state.active_tab == nav_key
            if st.button(nav_label, key=f"navtab_{nav_key}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.active_tab = nav_key
                st.rerun()

# ══════════════════════════════════════════════════════════════
# SCROLL RESET — whenever the active tab changes (nav bar click,
# or picking a crop from the Top Crops grid), snap the viewport
# back to the top so the new tab is read from its first section
# (e.g. Crop Details) instead of wherever the page was previously
# scrolled to (e.g. down at Planting Guide).
# ══════════════════════════════════════════════════════════════
if "prev_active_tab" not in st.session_state:
    st.session_state.prev_active_tab = st.session_state.active_tab
if st.session_state.prev_active_tab != st.session_state.active_tab:
    st.session_state.prev_active_tab = st.session_state.active_tab
    st.markdown("""<script>
    (function(){
      function scrollTop(){
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        var main = document.querySelector('section.main') || document.querySelector('[data-testid="stAppViewBlockContainer"]');
        if(main){ main.scrollTop = 0; }
        try{ window.parent.scrollTo(0,0); }catch(e){}
      }
      scrollTop();
      setTimeout(scrollTop, 50);
      setTimeout(scrollTop, 200);
    })();
    </script>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════
if st.session_state.active_tab == "dashboard":
    section(T("live_dash", lang))

    prev_run = st.session_state.get("prev_analysis")
    last_run_time = st.session_state.get("last_analysis_time")
    analysis_count = st.session_state.get("analysis_count", 0)

    def since_last_run(key, val, unit=""):
        """Delta vs the snapshot taken on the previous 'Run Full Analysis' click."""
        if prev_run is None:
            return None, False
        d = val - prev_run[key]
        if d == 0:
            return None, False
        sign = "+" if d > 0 else ""
        return f"{sign}{d}{unit} since last run", True

    metric_defs = [
        (T("soil",lang),     f"{soil}%",      "soil",     "%"),
        (T("temp",lang),     f"{temp}°C",     "temp",     "°C"),
        (T("rain",lang),     f"{rain}%",      "rain",     "%"),
        (T("sun",lang),      f"{sun}%",       "sun",      "%"),
        (T("humidity",lang), f"{humidity}%",  "humidity", "%"),
        (T("fert",lang),     f"{fert}%",      "fert",     "%"),
        (T("gas",lang),      f"{gas}%",       "gas",      "%"),
        (T("wind",lang),     f"{wind} km/h",  "wind",     " km/h"),
        (T("ph",lang),       f"{ph}",         "ph",       ""),
        (T("nitrogen",lang), f"{nitrogen}%",  "nitrogen", "%"),
    ]
    raw_vals = {"soil":soil,"temp":temp,"rain":rain,"sun":sun,"humidity":humidity,
                "fert":fert,"gas":gas,"wind":wind,"ph":ph,"nitrogen":nitrogen}
    metrics = []
    changed_count = 0
    for label, val, key, unit in metric_defs:
        delta, changed = since_last_run(key, raw_vals[key], unit)
        if changed:
            changed_count += 1
        metrics.append((label, val, delta, changed))

    # Status banner — this is the visible proof the button did something
    if last_run_time is None:
        st.markdown(
            "<div class='av-card av-tone-info' style='margin-bottom:1rem;'>"
            "<h4>▶️ No analysis run yet</h4>"
            "<p>Adjust the sliders in the sidebar, then press "
            f"<strong>{T('run_btn', lang)}</strong> to take a snapshot. "
            "Future runs will show exactly what changed since the last one.</p></div>",
            unsafe_allow_html=True
        )
    else:
        change_msg = (f"{changed_count} parameter(s) changed since the previous run"
                      if changed_count else "No parameters changed since the previous run")
        st.markdown(
            f"<div class='av-card av-tone-ok' style='margin-bottom:1rem;'>"
            f"<h4>✅ Analysis #{analysis_count} — run at {last_run_time.strftime('%d %b, %H:%M:%S')}</h4>"
            f"<p>{change_msg}.</p></div>",
            unsafe_allow_html=True
        )

    ACCENTS = ["#e63946","#c98a2e","#2176ae","#2d936c","#8b5cf6",
               "#e63946","#c98a2e","#2176ae","#2d936c","#8b5cf6"]
    dm = st.session_state.get("dark_mode", False)
    card_bg   = "#1e3530" if dm else "var(--surface)"
    card_bdr  = "#2d4a42" if dm else "var(--border)"
    lbl_color = "#6a9e94" if dm else "var(--muted)"
    dlt_color = "#4a7a6e" if dm else "#6b8079"
    changed_glow = "#c98a2e"
    for row_start in (0, 5):
        cols = st.columns(5)
        for ci, (label, val, delta, changed) in enumerate(metrics[row_start:row_start+5]):
            accent = ACCENTS[row_start + ci]
            border_color = changed_glow if changed else accent
            border_width = "3px" if changed else "3px"
            delta_color = changed_glow if changed else dlt_color
            delta_html = f"<div style='font-size:.78rem;color:{delta_color};margin-top:.15rem;font-weight:{700 if changed else 400};'>{delta}</div>" if delta else ""
            extra_shadow = f"box-shadow:0 0 0 2px {changed_glow}33,var(--shadow);" if changed else "box-shadow:var(--shadow);"
            cols[ci].markdown(
                f"<div style='background:{card_bg};border:1px solid {card_bdr};"
                f"border-top:{border_width} solid {border_color};border-radius:8px;padding:.75rem 1rem;"
                f"{extra_shadow}'>"
                f"<div style='font-size:.68rem;font-weight:700;text-transform:uppercase;"
                f"letter-spacing:.07em;color:{lbl_color};'>{label}</div>"
                f"<div style='font-size:1.35rem;font-weight:800;color:{accent};margin-top:.25rem;'>{val}</div>"
                f"{delta_html}</div>",
                unsafe_allow_html=True
            )
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

    section(T("crop_loss", lang))
    loss_tone = "danger" if loss_pct > 40 else ("warn" if loss_pct > 15 else "ok")
    loss_color = {"danger":"var(--danger)","warn":"var(--warn)","ok":"var(--ok)"}[loss_tone]
    st.markdown(f"<div class='av-card av-tone-{loss_tone}'>"
                f"<h4>{loss_pct}% — {T('crop_loss', lang)}</h4>{bar(loss_pct, loss_color)}</div>",
                unsafe_allow_html=True)
    if risks:
        pills_html = "".join(pill(f"{RISK_LABELS[k][lang]} (+{v}%)", "danger") for k, v in risks)
        card(L["danger"][lang], f"<p>{pills_html}</p><p>{L['register_pmfby'][lang]}</p>", icon="⚠️", tone="warn")
    else:
        card(L["safe"][lang], f"<p>{L['no_major_risk'][lang]}</p>", icon="✅", tone="ok")

    section(T("top_crops", lang))
    top10 = sorted_crops[:10]
    for row_start in (0, 5):
        cols = st.columns(5)
        for ci, (crop, score) in enumerate(top10[row_start:row_start+5]):
            i = row_start + ci
            with cols[ci]:
                is_sel = crop == sel
                cls = "av-crop-tile sel" if is_sel else "av-crop-tile"
                st.markdown(
                    f"<div class='{cls}'><div class='rank'>#{i+1}</div>"
                    f"<div class='name'>{CN(crop, lang)}</div>"
                    f"<div class='score'>{score}/100</div></div>",
                    unsafe_allow_html=True
                )
                if st.button(CN(crop, lang), key=f"pick_{crop}", use_container_width=True):
                    st.session_state.sel_crop = crop
                    st.session_state.active_tab = "advisor"
                    st.rerun()
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — CROP ADVISOR
# ══════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "advisor":
    section(f"{T('crop_detail', lang)}: {CN(sel, lang)}")
    dp = st.columns(4)
    dp[0].metric("💧 " + T("water_plan", lang).split(" ")[0], f"{water_need} L/day")
    dp[1].metric("⏱️ Days", f"{grow_days}")
    dp[2].metric("💰 ₹/kg", f"{price_kg}")
    dp[3].metric("🐛 Pest risk", L.get(pest_risk_level.lower(), L["medium"])[lang])
    season_label = L_SEASON_K if crop_season == "Kharif" else (L_SEASON_R if crop_season == "Rabi" else L_SEASON_A)
    st.markdown(bar(sc, "var(--brand)"), unsafe_allow_html=True)
    st.markdown(f"<p style='font-weight:700;color:var(--ink);'>{sc}/100 — {season_label[lang]}</p>", unsafe_allow_html=True)
    card(f"NPK · {npk} kg/ha", "<p>50% at sowing → 25% Day 30 → 25% at flowering.</p>", icon="🧪", tone="brand")
    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

    section(T("plant_guide", lang))
    card_grid([
        ("📐 Spacing",
         f"<p>↔️ Row spacing: <strong>{row_sp} cm</strong></p>"
         f"<p>↕️ Plant spacing: <strong>{plant_sp} cm</strong></p>"
         f"<p>⬇️ Sowing depth: <strong>{depth} cm</strong></p>"
         f"<p>🌰 Seeds/hole: <strong>{seeds_hole}</strong></p>", "", "ok"),
        ("📅 Tips",
         "<p>⏰ Best sowing time: early morning 5–7 AM</p>"
         "<p>🌱 Seed treatment: Thiram 2g + Bavistin 1g per kg</p>"
         "<p>📏 Mark rows with rope for uniform spacing</p>"
         f"<p>🌾 {L['harvest_note'][lang]}</p>", "", "ok"),
    ], ncols=2)

    section(T("pest_section", lang) + f": {CN(sel, lang)}")
    pests = PEST_MAP.get(sel, ["Aphids","Fungal Blight","Root Rot"])
    pest_pills = "".join(f"<p>{pill(p, 'danger')}</p>" for p in pests)
    hum_note = f"{L['danger'][lang]}: {RISK_LABELS['fungal'][lang]}" if humidity > 75 else L["safe"][lang]
    card_grid([
        (L.get(pest_risk_level.lower(), L["medium"])[lang], f"<p>{pest_pills}</p>", "🐛", "danger"),
        ("🛡️ Prevention",
         "<p>🌿 Neem oil 5ml/L every 15 days</p>"
         "<p>🔵 Trichoderma at sowing</p>"
         "<p>🟡 Yellow sticky traps — 10/acre</p>"
         f"<p>⚠️ {hum_note}</p>", "", "warn"),
    ], ncols=2)
    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

    section(T("calendar_section", lang) + f" — {CN(sel, lang)}")
    cal_rows = [
        ("Pre-sowing", "Soil prep + FYM", "2–3 weeks before"),
        ("Sowing", "Seed treatment + plant", f"Day 1 (5–7 AM), row {row_sp}cm × plant {plant_sp}cm"),
        ("Vegetative", "Irrigate + NPK dose 1", "Day 15–30"),
        ("Flowering", "Monitor pests — no spray", f"Day {int(grow_days*0.4)}–{int(grow_days*0.6)}"),
        ("Fruiting", "Support + thin", f"Day {int(grow_days*0.6)}–{int(grow_days*0.85)}"),
        ("Harvest", "Cut + dry + store", f"Day {grow_days}"),
        ("Post-harvest", "Grade + sell", "Within 3 days"),
    ]
    rows_html = "".join(
        f"<tr style='background:{'var(--bg-alt)' if i % 2 == 0 else 'transparent'};'>"
        f"<td style='padding:8px;font-weight:600;color:var(--ink);'>{stage}</td>"
        f"<td style='padding:8px;color:var(--ink-soft);'>{act}</td>"
        f"<td style='padding:8px;color:var(--ink-soft);font-weight:500;'>{timing}</td></tr>"
        for i, (stage, act, timing) in enumerate(cal_rows)
    )
    st.markdown(
        f"<div class='av-card av-tone-brand'><table style='width:100%;border-collapse:collapse;font-size:.85rem;'>"
        f"<tr style='border-bottom:2px solid var(--border);'>"
        f"<th style='text-align:left;padding:8px;color:var(--ink);font-weight:700;'>Stage</th>"
        f"<th style='text-align:left;padding:8px;color:var(--ink);font-weight:700;'>Activity</th>"
        f"<th style='text-align:left;padding:8px;color:var(--ink);font-weight:700;'>Timing</th></tr>"
        f"{rows_html}</table></div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — WATER & FINANCE
# ══════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "finance":
    section(T("water_plan", lang))
    daily_w  = round((100-rain) * water_need * 0.15, 1)
    weekly_w = round(daily_w * 7, 1)
    season_w = round(daily_w * grow_days, 1)
    total_w  = round(season_w * farm_size, 1)
    irr_type = "Drip (saves 40% water)" if rain < 40 else ("Sprinkler" if rain < 70 else "Flood irrigation")
    freq     = "Every 3 days" if soil < 40 else "Every 5–7 days"
    rainwater = round(rain * farm_size * 100, 0)
    card_grid([
        (T("rain", lang), f"<p>Daily: <strong>{daily_w} L/ha</strong></p><p>Weekly: <strong>{weekly_w} L/ha</strong></p>"
         f"<p>Season: <strong>{season_w} L/ha</strong></p><p>Farm total: <strong>{total_w} L</strong></p>", "📊", "info"),
        (irr_type, f"<p>Frequency: <strong>{freq}</strong></p><p>Best time: <strong>5–7 AM</strong></p>"
         "<p>PMKSY subsidy: <strong>55–75%</strong></p>", "🚿", "info"),
        ("Rainwater harvesting", f"<p>Estimated: <strong>{int(rainwater)} L</strong></p>"
         "<p>Pond size: <strong>10×10×2 m</strong></p><p>Saves: <strong>~30% cost</strong></p>", "♻️", "info"),
    ], ncols=3)

    section(T("financial", lang))
    base_yield = round((sc/100) * 8500 * farm_size, 0)
    gross_rev  = round(base_yield * price_kg, 0)
    input_cost = round(farm_size * 25000, 0)
    transport  = round(market_dist * base_yield * 0.002, 0)
    net_profit = round(gross_rev - input_cost - transport, 0)
    roi        = round((net_profit/input_cost)*100, 1) if input_cost > 0 else 0
    adj_yield  = round(base_yield * (1 - loss_pct/100), 0)
    adj_profit = round(adj_yield * price_kg - input_cost - transport, 0)
    card_grid([
        ("📈 Revenue", f"<p>Est. yield: <strong>{int(base_yield)} kg</strong></p>"
         f"<p>After loss risk: <strong>{int(adj_yield)} kg</strong></p>"
         f"<p>Price: <strong>₹{price_kg}/kg</strong></p><p>Gross: <strong>₹{int(gross_rev):,}</strong></p>", "", "brand"),
        ("💸 Cost", f"<p>Input cost: <strong>₹{int(input_cost):,}</strong></p>"
         f"<p>Transport: <strong>₹{int(transport):,}</strong></p><p>ROI: <strong>{roi}%</strong></p>", "", "brand"),
        ("🏆 Net", f"<p>Net profit: <strong style='font-size:1.05rem;'>₹{int(net_profit):,}</strong></p>"
         f"<p>Adj. profit (after loss): <strong>₹{int(adj_profit):,}</strong></p>"
         f"<p>Sell at: <strong>{'APMC Mandi' if market_dist<50 else 'eNAM Online'}</strong></p>", "", "brand"),
    ], ncols=3)

    section(T("soil_section", lang))
    raw_ph = "acidic" if ph < 6 else ("alkaline" if ph > 7.5 else "optimal")
    ph_note = {"acidic":"Add lime, 2–3 bags/acre","alkaline":"Add gypsum, 200 kg/acre","optimal":L["optimal"][lang]}[raw_ph]
    raw_soil = "very dry" if soil < 25 else ("dry" if soil < 45 else ("optimal" if soil < 75 else "waterlogged"))
    soil_note = {"very dry":"Irrigate now!","dry":L["low"][lang],"optimal":L["optimal"][lang],"waterlogged":"Drain now!"}[raw_soil]
    raw_n = "deficient" if nitrogen < 30 else ("optimal" if nitrogen < 70 else "excess")
    n_note = {"deficient":"Add urea","optimal":L["optimal"][lang],"excess":L["excess"][lang]}[raw_n]
    carbon_score = 100 - fert
    soil_health = round(max(0, 100 - abs(soil-60) - abs(ph-6.5)*5), 1)
    fert_formula = {"Conventional":"Urea + DAP + MOP","Organic":"Vermicompost + neem cake",
                    "Integrated":"50% chemical + 50% organic","Hydroponic":"Nutrient solution A+B"}
    card_grid([
        (f"🌍 {T('soil_section', lang)}", f"<p>{T('soil', lang)}: <strong>{soil_note}</strong></p>"
         f"<p>pH: <strong>{ph_note}</strong></p><p>{T('nitrogen', lang)}: <strong>{n_note}</strong></p>"
         f"<p>Health score: <strong>{soil_health}/100</strong></p>"
         f"<p>Carbon credit value: <strong>₹{round(carbon_score*0.5*farm_size*1500,0):,.0f}</strong></p>", "", "warn"),
        ("🧪 Fertilizer plan", f"<p>Type: <strong>{farm_type}</strong></p>"
         f"<p>Formula: <strong>{fert_formula.get(farm_type,'Integrated')}</strong></p>"
         f"<p>NPK: <strong>{npk} kg/ha</strong></p><p>Applied in 3 splits, + Zinc 25 kg/ha</p>", "", "warn"),
    ], ncols=2)

    section(T("risk_section", lang))
    def risk_level(val, high, med):
        return "high" if val > high else ("medium" if val > med else "low")
    flood_l = risk_level(rain, 80, 55)
    drought_l = "high" if soil < 25 else ("medium" if soil < 45 else "low")
    frost_l = "high" if temp < 5 else ("medium" if temp < 12 else "low")
    heat_l = "high" if temp > 42 else ("medium" if temp > 35 else "low")
    gas_l = "danger" if gas > 70 else ("medium" if gas > 40 else "safe")
    t_adv = "Too hot — use shade nets" if temp > 38 else ("Too cold — use mulching" if temp < 10 else L["optimal"][lang])
    r_adv = "Waterlogging risk" if rain > 85 else ("Good rainfall" if rain > 60 else "Irrigation needed")
    card_grid([
        ("⚠️ Risk levels",
         f"<p>🌊 Flood: {pill(L[flood_l][lang], status_tone(flood_l))}</p>"
         f"<p>🏜️ Drought: {pill(L[drought_l][lang], status_tone(drought_l))}</p>"
         f"<p>❄️ Frost: {pill(L[frost_l][lang], status_tone(frost_l))}</p>"
         f"<p>🔥 Heat: {pill(L[heat_l][lang], status_tone(heat_l))}</p>"
         f"<p>💨 {T('gas', lang)}: {pill(L[gas_l][lang], status_tone(gas_l))}</p>", "", "info"),
        ("🌦️ Climate advisory",
         f"<p>{T('temp', lang)}: <strong>{t_adv}</strong></p><p>{T('rain', lang)}: <strong>{r_adv}</strong></p>"
         f"<p>{T('wind', lang)}: <strong>{'Use windbreaks' if wind>50 else L['safe'][lang]}</strong></p>"
         f"<p>Harvest in: <strong>{grow_days} days</strong></p>", "", "info"),
    ], ncols=2)

    section(T("sustain_section", lang))
    eco = round((carbon_score*0.4) + (max(0,100-fert)*0.3) + (soil_health*0.3), 1)
    card_grid([
        ("♻️ Carbon", f"<p>Carbon score: <strong>{carbon_score}/100</strong></p>"
         f"<p>Eco score: <strong>{eco}/100</strong></p>"
         f"<p>CO₂ saved: <strong>{round(carbon_score*farm_size*0.3,2)} t</strong></p>", "", "ok"),
        ("🌱 Green practices",
         "<p>✅ Drip irrigation (40% water save)</p><p>✅ Crop rotation every season</p>"
         "<p>✅ Vermicompost + biofertilizers</p><p>✅ Solar pump — PM-KUSUM 90% subsidy</p>", "", "ok"),
    ], ncols=2)

# ══════════════════════════════════════════════════════════════
# TAB 4 — GOVERNMENT SCHEMES
# ══════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "schemes":
    section(T("gov_section", lang))
    full = GOV_SCHEMES[:-1] if len(GOV_SCHEMES) % 3 != 0 else GOV_SCHEMES
    leftover = GOV_SCHEMES[len(full):]

    def scheme_cell(name, url, desc_dict, extra_style=""):
        desc = desc_dict.get(lang, desc_dict['English'])
        return (f"<div class='av-card av-tone-brand av-card-scheme' style='margin:0;{extra_style}'>"
                f"<h4>🏛️ {name}</h4><p>{desc}</p>"
                f"<p><a href='{url}' target='_blank' style='color:var(--brand);font-weight:700;'>"
                f"🔗 {L['apply_now'][lang]}</a></p></div>")

    # Real CSS Grid instead of st.columns — grid rows auto-equalize height,
    # so cards no longer drift out of alignment or look mismatched in size
    # when one card's description text wraps to more lines than its neighbor's.
    cells_html = "".join(scheme_cell(name, url, desc_dict) for name, url, desc_dict in full)
    if len(leftover) == 1:
        name, url, desc_dict = leftover[0]
        cells_html += scheme_cell(name, url, desc_dict, extra_style="grid-column:2;")
    elif len(leftover) == 2:
        for i, (name, url, desc_dict) in enumerate(leftover):
            cells_html += scheme_cell(name, url, desc_dict, extra_style=f"grid-column:{i+1};")

    st.markdown(
        f"<div style='display:grid;grid-template-columns:repeat(3,1fr);"
        f"gap:1rem;align-items:stretch;'>{cells_html}</div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════
# TAB 5 — CHATBOT
# ══════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "chat":
    section(T("chatbot_title", lang), T("ask_chat", lang))
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_key" not in st.session_state:
        st.session_state.chat_key = 0
    if not st.session_state.get("chat_started", False):
        st.markdown("""
        <div class='av-card av-tone-brand' style='margin-bottom:1.5rem;'>
          <h4>💬 Ask me anything about your farm</h4>
          <p>Try these questions:</p>
          <ul>
            <li>Which crop should I grow this season?</li>
            <li>How much water does my crop need?</li>
            <li>What pests should I watch for?</li>
            <li>What government schemes can I apply for?</li>
            <li>What is my estimated profit?</li>
          </ul>
        </div>""", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        cls = "av-chat-user" if msg["role"] == "user" else "av-chat-bot"
        icon = "👨‍🌾" if msg["role"] == "user" else "🤖"
        st.markdown(f"<div class='{cls}'><strong>{icon}</strong> {msg['content']}</div>", unsafe_allow_html=True)

    def chat_answer(q, lang):
        ql = q.lower()
        if any(w in ql for w in ["crop","fasal","grow","sow","best"]):
            return (f"Top pick for your inputs: **{CN(sel, lang)}** ({sc}/100). "
                    f"{season_label[lang]}. Water need: {water_need} L/day, harvest in {grow_days} days.")
        if any(w in ql for w in ["water","irrigation","pani"]):
            return f"Daily water need for {CN(sel, lang)}: ~{daily_w} L/ha. Recommended: {irr_type}, at 5–7 AM."
        if any(w in ql for w in ["soil","mitti","ph"]):
            return f"Soil status: {soil_note}. pH status: {ph_note}. Health score: {soil_health}/100."
        if any(w in ql for w in ["pest","keeda","disease"]):
            return f"Watch for: {', '.join(PEST_MAP.get(sel, ['Aphids','Blight']))}. Neem oil 5ml/L every 15 days is the first line of defense."
        if any(w in ql for w in ["loss","nuksan","damage"]):
            return f"Current crop-loss risk: {loss_pct}%. {L['register_pmfby'][lang] if risks else L['no_major_risk'][lang]}"
        if any(w in ql for w in ["scheme","yojana","subsidy","pm-kisan","pmfby"]):
            return "Key schemes: PM-KISAN (₹6000/yr), KCC (4% loans), PMFBY (2% premium insurance), PMKSY (drip subsidy). See the Govt Schemes tab."
        if any(w in ql for w in ["profit","money","finance","paisa"]):
            return f"Projected net profit for {CN(sel, lang)} on {farm_size} ha: ₹{int(net_profit):,} (ROI {roi}%)."
        return "I can help with crops, soil, water, pests, crop-loss risk, government schemes, and finances — ask me anything about your farm."

    st.markdown("<div style='margin-bottom:.75rem;'></div>", unsafe_allow_html=True)
    ci1, ci2 = st.columns([5, 1])
    with ci1:
        user_input = st.text_input("", placeholder=T("ask_chat", lang), label_visibility="collapsed",
                                   key=f"chat_input_{st.session_state.chat_key}")
    with ci2:
        send = st.button("Send ➤", use_container_width=True)
    if send and user_input:
        st.session_state.chat_started = True
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = chat_answer(user_input, lang)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.chat_key += 1
        st.rerun()
    # Fill remaining viewport height so background shows — no white gap on tall/16:9 screens
    st.markdown("<div style='min-height:60vh;background:transparent;'></div>", unsafe_allow_html=True)

# Modified placeholder for app(4) dark mode improvements
