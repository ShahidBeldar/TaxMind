import streamlit as st
import streamlit.components.v1 as components
from utils.db import init_db, create_user, authenticate_user, update_user_profile
from utils.i18n import t
from utils.theme import inject_theme, page_title, card

st.set_page_config(
    page_title="TaxMind AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto",
)

init_db()


def _init_session():
    defaults = {
        "logged_in":        False,
        "user_id":          None,
        "username":         "",
        "name":             "",
        "employment_type":  "",
        "income_bracket":   "",
        "preferred_regime": "new",
        "language":         "en",
        "setup_complete":   0,
        "chat_history":     [],
        "auth_mode":        "login",
        "auth_error":       "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_session()


def _load_session_from_row(row):
    st.session_state.logged_in        = True
    st.session_state.user_id          = row["id"]
    st.session_state.username         = row["username"]
    st.session_state.name             = row["name"] or ""
    st.session_state.employment_type  = row["employment_type"] or ""
    st.session_state.income_bracket   = row["income_bracket"] or ""
    st.session_state.preferred_regime = row["preferred_regime"] or "new"
    st.session_state.language         = row["language"] or "en"
    st.session_state.setup_complete   = row["setup_complete"] or 0


def _process_query_params():
    params = st.query_params
    action = params.get("action", "")

    if action == "login":
        username = params.get("u", "").strip()
        password = params.get("p", "").strip()
        st.query_params.clear()
        if not username or not password:
            st.session_state.auth_error = "Please enter your username and password."
        else:
            row = authenticate_user(username, password)
            if row:
                st.session_state.auth_error = ""
                _load_session_from_row(row)
            else:
                st.session_state.auth_error = "Invalid username or password."

    elif action == "signup":
        username = params.get("u", "").strip()
        password = params.get("p", "").strip()
        confirm  = params.get("c", "").strip()
        st.query_params.clear()
        if not username or not password:
            st.session_state.auth_error = "Username and password are required."
        elif password != confirm:
            st.session_state.auth_error = "Passwords do not match."
        elif len(password) < 6:
            st.session_state.auth_error = "Password must be at least 6 characters."
        else:
            success = create_user(username, password)
            if success:
                row = authenticate_user(username, password)
                if row:
                    st.session_state.auth_error = ""
                    _load_session_from_row(row)
            else:
                st.session_state.auth_error = "Username already taken. Choose another."

    elif action == "mode":
        mode = params.get("m", "login")
        st.query_params.clear()
        st.session_state.auth_mode  = mode
        st.session_state.auth_error = ""


_process_query_params()


def render_auth():
    inject_theme()

    mode  = st.session_state.auth_mode
    error = st.session_state.auth_error

    login_display  = "block" if mode == "login"  else "none"
    signup_display = "block" if mode == "signup" else "none"
    ul_left_color  = "#4f8ef7" if mode == "login"  else "transparent"
    ul_right_color = "#4f8ef7" if mode == "signup" else "transparent"
    login_active   = "active" if mode == "login"  else ""
    signup_active  = "active" if mode == "signup" else ""
    error_html     = f'<div class="err">{error}</div>' if error else ""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:transparent;font-family:'Inter',sans-serif;display:flex;justify-content:center;padding:16px 12px 28px}}
.card{{width:100%;max-width:400px}}
.brand{{text-align:center;padding:0 0 18px}}
.brand h1{{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#e8eeff;letter-spacing:-.04em;margin-bottom:5px}}
.brand p{{color:#3d5070;font-size:11px;letter-spacing:.07em;text-transform:uppercase;font-family:'DM Mono',monospace}}
hr{{border:none;border-top:1px solid #1c2d4a;margin:0 0 18px}}
.tabs{{display:flex;gap:0;margin-bottom:4px}}
.tab-btn{{flex:1;padding:10px;background:transparent;border:1.5px solid #243858;color:#7a90b8;font-family:'Inter',sans-serif;font-size:13px;font-weight:600;cursor:pointer;transition:all .15s}}
.tab-btn:first-child{{border-radius:8px 0 0 8px;border-right:none}}
.tab-btn:last-child{{border-radius:0 8px 8px 0}}
.tab-btn.active,.tab-btn:hover{{color:#e8eeff;border-color:#4f8ef7;background:rgba(79,142,247,.1)}}
.underline{{display:flex;height:2px;margin-bottom:18px}}
.ul-l{{flex:1;background:{ul_left_color};border-radius:2px}}
.ul-r{{flex:1;background:{ul_right_color};border-radius:2px}}
.err{{background:rgba(240,90,90,.12);border:1px solid rgba(240,90,90,.3);border-left:3px solid #f05a5a;color:#f08080;border-radius:8px;padding:10px 14px;font-size:13px;margin-bottom:14px}}
label{{display:block;color:#7a90b8;font-size:12.5px;font-weight:500;margin-bottom:5px;letter-spacing:.02em}}
input[type=text],input[type=password]{{width:100%;background:#162035;border:1.5px solid #2e4a7a;border-radius:8px;color:#e8eeff;font-size:14px;font-family:'Inter',sans-serif;padding:11px 14px;margin-bottom:13px;outline:none;transition:border-color .15s,box-shadow .15s;-webkit-text-fill-color:#e8eeff;caret-color:#4f8ef7;display:block}}
input::placeholder{{color:#3d5a80;-webkit-text-fill-color:#3d5a80;opacity:1}}
input:focus{{border-color:#4f8ef7;box-shadow:0 0 0 3px rgba(79,142,247,.15)}}
.btn{{width:100%;background:#4f8ef7;border:none;border-radius:8px;color:#fff;font-family:'Syne',sans-serif;font-size:14px;font-weight:700;padding:13px;cursor:pointer;letter-spacing:.03em;margin-top:2px;transition:background .15s,transform .1s,box-shadow .15s;box-shadow:0 2px 14px rgba(79,142,247,.3)}}
.btn:hover{{background:#3a75e0;transform:translateY(-1px);box-shadow:0 6px 22px rgba(79,142,247,.4)}}
.btn:active{{transform:translateY(0)}}
.footer{{text-align:center;color:#3d5070;font-size:11px;font-family:'DM Mono',monospace;margin-top:18px}}
</style>
</head>
<body>
<div class="card">
  <div class="brand">
    <h1>TaxMind AI</h1>
    <p>Indian Tax Planning · FY 2026</p>
  </div>
  <hr>
  <div class="tabs">
    <button class="tab-btn {login_active}" onclick="switchMode('login')">Sign In</button>
    <button class="tab-btn {signup_active}" onclick="switchMode('signup')">Create Account</button>
  </div>
  <div class="underline"><div class="ul-l"></div><div class="ul-r"></div></div>
  {error_html}
  <div id="lf" style="display:{login_display}">
    <label>Username</label>
    <input type="text" id="lu" placeholder="your_username" autocomplete="username">
    <label>Password</label>
    <input type="password" id="lp" placeholder="password" autocomplete="current-password">
    <button class="btn" onclick="doLogin()">Sign In →</button>
  </div>
  <div id="sf" style="display:{signup_display}">
    <label>Username</label>
    <input type="text" id="su" placeholder="choose a username" autocomplete="username">
    <label>Password</label>
    <input type="password" id="sp" placeholder="min 6 characters" autocomplete="new-password">
    <label>Confirm Password</label>
    <input type="password" id="sc" placeholder="repeat password" autocomplete="new-password">
    <button class="btn" onclick="doSignup()">Create Account →</button>
  </div>
  <div class="footer">Data stored locally · FY 2026 · AI-powered tax advice</div>
</div>
<script>
function switchMode(m){{
  window.parent.location.href='?action=mode&m='+m;
}}
function doLogin(){{
  var u=document.getElementById('lu').value.trim();
  var p=document.getElementById('lp').value;
  if(!u||!p){{alert('Please fill in both fields.');return;}}
  window.parent.location.href='?action=login&u='+encodeURIComponent(u)+'&p='+encodeURIComponent(p);
}}
function doSignup(){{
  var u=document.getElementById('su').value.trim();
  var p=document.getElementById('sp').value;
  var c=document.getElementById('sc').value;
  if(!u||!p){{alert('Username and password are required.');return;}}
  if(p!==c){{alert('Passwords do not match.');return;}}
  if(p.length<6){{alert('Password must be at least 6 characters.');return;}}
  window.parent.location.href='?action=signup&u='+encodeURIComponent(u)+'&p='+encodeURIComponent(p)+'&c='+encodeURIComponent(c);
}}
</script>
</body>
</html>"""

    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        components.html(html, height=600, scrolling=False)


def render_wizard():
    inject_theme()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="padding:1.5rem 0 .5rem 0;">
            <h1 style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                       color:#e8eeff;margin:0;">Set Up Your Profile</h1>
            <p style="color:#3d5070;font-size:13px;margin:.4rem 0 0 0;">
                This helps personalise your tax advice and dashboard.
            </p>
        </div>
        <hr style="border-color:#1c2d4a;">
        """, unsafe_allow_html=True)

        name             = st.text_input(t("full_name"), value=st.session_state.name, placeholder="e.g. Arjun Mehta")
        employment_type  = st.selectbox(t("employment_type"), options=["Salaried", "Self-Employed", "Business"])
        income_bracket   = st.selectbox(t("income_bracket"),
            options=["Below 5L", "5L - 10L", "10L - 15L", "15L - 25L", "25L - 50L", "Above 50L"])
        preferred_regime = st.selectbox(t("preferred_regime"), options=["new", "old"],
            format_func=lambda x: "New Regime (FY 2026 default)" if x == "new" else "Old Regime")
        language         = st.selectbox(t("language_label"), options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi")

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button(t("wizard_save"), use_container_width=True):
            if not name.strip():
                st.error("Please enter your name.")
            else:
                update_user_profile(
                    st.session_state.user_id, name.strip(),
                    employment_type, income_bracket, preferred_regime, language,
                )
                st.session_state.name             = name.strip()
                st.session_state.employment_type  = employment_type
                st.session_state.income_bracket   = income_bracket
                st.session_state.preferred_regime = preferred_regime
                st.session_state.language         = language
                st.session_state.setup_complete   = 1
                st.success(t("wizard_saved"))
                st.rerun()


def render_home():
    inject_theme()

    from utils.sidebar import render_sidebar
    render_sidebar()

    st.markdown(page_title("", "TaxMind AI", "Indian Tax Planning for FY 2026"),
                unsafe_allow_html=True)

    name   = st.session_state.name or st.session_state.username
    emp    = st.session_state.employment_type or "—"
    bkt    = st.session_state.income_bracket or "—"
    regime = "New Regime" if st.session_state.preferred_regime == "new" else "Old Regime"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d1526 0%,#101e38 100%);
                border:1px solid #1c2d4a;border-left:3px solid #4f8ef7;
                border-radius:16px;padding:1.5rem 2rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
                    color:#e8eeff;margin-bottom:.35rem;">Welcome back, {name}</div>
        <p style="color:#7a90b8;font-size:13.5px;margin:0;line-height:1.65;">
            {emp} &middot; {bkt} &middot; {regime} &mdash; use the sidebar to navigate.
        </p>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("Dashboard",           "Tax calculator · slab breakdown · PDF export"),
        ("AI Advisor",          "Context-aware Indian tax Q&A via Groq"),
        ("Expenses",            "Categorised spend overview with charts"),
        ("GST & ITR Tips",      "Deadlines · penalties · regime comparison"),
        ("Predictive Planning", "Year-end projection from monthly trends"),
        ("Upload Data",         "Add transactions manually or via CSV"),
    ]
    cols = st.columns(3)
    for i, (title, desc) in enumerate(pages):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#0d1526;border:1px solid #1c2d4a;border-radius:14px;
                        padding:1.1rem 1.2rem;margin-bottom:.75rem;min-height:90px;">
                <div style="font-family:'Syne',sans-serif;font-weight:700;
                            font-size:.88rem;color:#e8eeff;margin-bottom:.25rem;">{title}</div>
                <div style="color:#3d5070;font-size:11px;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#3d5070;font-size:10.5px;margin-top:.8rem;text-align:center;
              font-family:'DM Mono',monospace;">
        transaction data stored in local sqlite · persists within current deployment instance
    </p>
    """, unsafe_allow_html=True)


if not st.session_state.logged_in:
    render_auth()
elif st.session_state.setup_complete == 0:
    render_wizard()
else:
    render_home()
