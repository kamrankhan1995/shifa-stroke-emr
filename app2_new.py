"""
════════════════════════════════════════════════════════════════════════════════
  ACUTE ISCHEMIC STROKE — ELECTRONIC MEDICAL RECORD
  Shifa International Hospitals Ltd. | FM-MSA-429 Rev:01
  AHA/ASA 2026 Guideline-Based | JCI Accredited Workflow
  Version 2.0 — Enterprise Edition
════════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
import streamlit as st
import datetime
import pandas as pd
import json
from typing import Any, Optional

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AIS EMR — Shifa International",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧠",
)

# ═══════════════════════════════════════════════════════════════════════════
# CSS — ENTERPRISE HEALTHCARE THEME (ENHANCED GRAPHICS)
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_resource
def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    font-size: 15px; /* Increased base font size */
    line-height: 1.6; color: #0F172A; /* Darker text for maximum contrast */
}
.main .block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1400px !important; }

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0B2545 0%, #0F3460 50%, #13315C 100%) !important;
    box-shadow: 4px 0 25px rgba(11,37,69,0.4);
}
[data-testid="stSidebar"] * { color: #F8FAFC !important; }
div[data-baseweb="popover"] * { color: #0F172A !important; }
div[data-baseweb="select"] * { color: #0F172A !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem !important; font-weight: 600 !important; padding: 6px 0; color: #CBD5E1 !important; transition: all 0.2s ease; }
[data-testid="stSidebar"] .stRadio label:hover { color: #ffffff !important; transform: translateX(4px); }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; border: none !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #E2E8F0 !important; font-weight: 600 !important; }

/* HEADER STYLING */
.hospital-header {
    background: linear-gradient(90deg, #0B2545 0%, #134074 60%, #1E3A8A 100%);
    color: #ffffff; padding: 18px 30px; border-radius: 12px; margin-bottom: 24px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 8px 25px rgba(11,37,69,0.3);
}
.hospital-header .hosp-name { font-size: 1.3rem; font-weight: 900; letter-spacing: 0.5px; color: #ffffff; }
.hospital-header .screen-title { font-size: 1.15rem; font-weight: 700; color: #93C5FD; }
.hospital-header .meta { font-size: 0.85rem; color: rgba(255,255,255,0.8); text-align: right; line-height: 1.8; font-weight: 500; }
.role-badge { display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
.role-physician  { background: #064E3B; color: #6EE7B7; }
.role-nurse      { background: #4A044E; color: #D8B4FE; }
.role-allied     { background: #78350F; color: #FDE68A; }
.role-admin      { background: #1E3A8A; color: #93C5FD; }
.role-readonly   { background: #374151; color: #D1D5DB; }

/* CARDS AND BANNERS WITH HOVER EFFECTS */
.card { 
    border-radius: 12px; padding: 16px 20px; margin: 12px 0; border-left: 6px solid transparent; 
    transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
.card-info    { background: #EFF6FF; border-color: #2563EB; }
.card-success { background: #F0FDF4; border-color: #16A34A; }
.card-warning { background: #FFFBEB; border-color: #D97706; }
.card-danger  { background: #FEF2F2; border-color: #DC2626; }
.section-banner {
    padding: 10px 20px; border-radius: 8px; font-weight: 800; font-size: 0.95rem;
    letter-spacing: 0.5px; margin: 20px 0 12px 0; text-transform: uppercase;
    display: flex; align-items: center; gap: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.banner-blue   { background: #1E40AF; color: #ffffff; }
.banner-green  { background: #14532D; color: #ffffff; }
.banner-orange { background: #92400E; color: #ffffff; }
.banner-red    { background: #7F1D1D; color: #ffffff; }
.banner-purple { background: #4C1D95; color: #ffffff; }
.banner-teal   { background: #134E4A; color: #ffffff; }
.banner-grey   { background: #334155; color: #ffffff; }

/* KPI GRIDS WITH POP-UP EFFECTS */
.kpi-grid { display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0; }
.kpi-box { 
    border-radius: 12px; padding: 20px; text-align: center; flex: 1; min-width: 140px; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.kpi-box:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}
.kpi-primary   { background: linear-gradient(135deg, #1E3A8A, #3B82F6); color: #fff; }
.kpi-success   { background: linear-gradient(135deg, #064E3B, #10B981); color: #fff; }
.kpi-warning   { background: linear-gradient(135deg, #78350F, #F59E0B); color: #fff; }
.kpi-danger    { background: linear-gradient(135deg, #7F1D1D, #EF4444); color: #fff; }
.kpi-neutral   { background: linear-gradient(135deg, #334155, #64748B); color: #fff; }
.kpi-val { font-size: 2.2rem; font-weight: 900; display: block; line-height: 1.1; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
.kpi-lbl { font-size: 0.85rem; opacity: 0.9; margin-top: 6px; display: block; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;}

/* DASHBOARD TILE BUTTONS WITH ENHANCED POP-UP AND GLOW */
div[data-testid="stButton"] button {
    height: 100% !important;
    min-height: 120px !important;
    border-radius: 16px !important;
    background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%) !important;
    border: 2px solid #94A3B8 !important;
    color: #0F172A !important;
    white-space: pre-wrap !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-6px) scale(1.03) !important;
    box-shadow: 0 15px 35px rgba(37,99,235,0.3) !important;
    border-color: #2563EB !important;
    background: linear-gradient(135deg, #EFF6FF 0%, #BFDBFE 100%) !important;
    color: #1E3A8A !important;
}

/* HIGH VISIBILITY INPUT LABELS */
.stCheckbox label { font-size: 0.95rem !important; color: #1E293B !important; font-weight: 500 !important; }
.stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stTimeInput label, .stTextArea label, .stRadio label { 
    font-size: 0.95rem !important; 
    font-weight: 700 !important; 
    color: #0F172A !important; 
    margin-bottom: 4px !important;
}
.stExpander summary { font-weight: 700 !important; font-size: 1rem !important; color: #1E3A8A !important; }
[data-testid="stExpander"] summary { background: #F8FAFC !important; border-radius: 8px; border: 1px solid #E2E8F0; padding: 12px !important; }
[data-testid="stExpander"] summary:hover { background: #F1F5F9 !important; border-color: #CBD5E1; }

/* HEADINGS */
h1 { color: #0B2545 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
h2 { color: #134074 !important; font-size: 1.5rem !important; font-weight: 800 !important; }
h3 { color: #1E40AF !important; font-size: 1.2rem !important; font-weight: 800 !important; border-bottom: 2px solid #BFDBFE !important; padding-bottom: 6px !important; margin-top: 20px !important;}
h4 { color: #1D4ED8 !important; font-size: 1.05rem !important; font-weight: 700 !important; }
h5 { color: #334155 !important; font-size: 0.95rem !important; font-weight: 700 !important; }

/* MISC STYLING */
.readonly-banner { background: linear-gradient(90deg, #334155, #475569); color: #F8FAFC; padding: 12px 20px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
button[data-baseweb="tab"] { font-weight: 700 !important; font-size: 0.95rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { border-bottom: 4px solid #1E40AF !important; color: #1E40AF !important; background: #EFF6FF !important; border-radius: 8px 8px 0 0; }
[data-testid="stDataEditor"] { border-radius: 12px; overflow: hidden; border: 1px solid #CBD5E1; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

@media print {
    [data-testid="stSidebar"] { display: none !important; }
    .hospital-header { background: #0B2545 !important; -webkit-print-color-adjust: exact; }
    .no-print { display: none !important; }
}
</style>
"""

st.markdown(get_css(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS & LOOKUP TABLES
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_resource
def get_nihss_opts() -> dict:
    return {
        "n1a": ["0 - Alert","1 - Not Alert (arousable)","2 - Obtunded","3 - Unresponsive"],
        "n1b": ["0 - Both correct","1 - One correct","2 - Neither correct"],
        "n1c": ["0 - Both tasks correct","1 - One task correct","2 - Neither correct"],
        "n2":  ["0 - Normal","1 - Partial gaze palsy","2 - Forced deviation"],
        "n3":  ["0 - No visual loss","1 - Partial hemianopia","2 - Complete hemianopia","3 - Bilateral hemianopia"],
        "n4":  ["0 - Normal","1 - Minor paralysis","2 - Partial paralysis","3 - Complete paralysis"],
        "n5l": ["0 - No drift","1 - Drift < 10s","2 - Some effort vs gravity","3 - No effort vs gravity","4 - No movement"],
        "n5r": ["0 - No drift","1 - Drift < 10s","2 - Some effort vs gravity","3 - No effort vs gravity","4 - No movement"],
        "n6l": ["0 - No drift","1 - Drift","2 - Some effort vs gravity","3 - No effort vs gravity","4 - No movement"],
        "n6r": ["0 - No drift","1 - Drift","2 - Some effort vs gravity","3 - No effort vs gravity","4 - No movement"],
        "n7":  ["0 - Absent","1 - Present in one limb","2 - Present in two limbs"],
        "n8":  ["0 - Normal","1 - Mild/moderate loss","2 - Severe/total loss"],
        "n9":  ["0 - No aphasia","1 - Mild/moderate aphasia","2 - Severe aphasia","3 - Mute/global aphasia"],
        "n10": ["0 - Normal","1 - Mild/moderate","2 - Severe/unintelligible"],
        "n11": ["0 - No abnormality","1 - Inattention (one modality)","2 - Profound hemi-inattention"],
    }

NIHSS_KEYS = ["n1a","n1b","n1c","n2","n3","n4","n5l","n5r","n6l","n6r","n7","n8","n9","n10","n11"]
NIHSS_LABELS = {
    "n1a":"1a. LOC","n1b":"1b. LOC Questions","n1c":"1c. LOC Commands",
    "n2":"2. Best Gaze","n3":"3. Visual Fields","n4":"4. Facial Palsy",
    "n5l":"5. Motor Arm (L)","n5r":"5. Motor Arm (R)",
    "n6l":"6. Motor Leg (L)","n6r":"6. Motor Leg (R)",
    "n7":"7. Limb Ataxia","n8":"8. Sensory",
    "n9":"9. Best Language","n10":"10. Dysarthria","n11":"11. Inattention",
}

ROLES = ["Physician", "Nurse", "Allied Health / Rehab", "Admin / Audit"]
ROLE_PERMISSIONS = {
    "Physician":            {"physician": "write", "nursing": "write", "allied": "write", "admin": "read"},
    "Nurse":                {"physician": "read",  "nursing": "write", "allied": "read",  "admin": "read"},
    "Allied Health / Rehab":{"physician": "read",  "nursing": "read",  "allied": "write", "admin": "read"},
    "Admin / Audit":        {"physician": "read",  "nursing": "read",  "allied": "read",  "admin": "write"},
}

ALL_SCREENS = [
    "🏠 Dashboard",
    "Phase 1: ER Code Activation (Duty Dr)",
    "Phase 2: Acute Neuro Eval (Responder)", 
    "Phase 3: Imaging & Routing Gate", 
    "Phase 4: Stroke Unit Orders (Days 1-3)",
    "Phase 5: Daily Rounds & Progress Notes",
    "Phase 6: Serial NIHSS & Outcomes",
    "Variance Audit",
]

MRS_LABELS = [
    "0 — No symptoms",
    "1 — No significant disability",
    "2 — Slight disability",
    "3 — Moderate disability (walks independently)",
    "4 — Moderately severe (cannot walk without help)",
    "5 — Severe disability (bedridden)",
    "6 — Death",
]

# ═══════════════════════════════════════════════════════════════════════════
# CACHED PURE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_data
def nihss_severity(score: int) -> tuple:
    if score <= 7:   return "Minor Stroke",     "4.2%",  "kpi-success"
    if score <= 13:  return "Moderate Stroke",  "13.9%", "kpi-warning"
    if score <= 21:  return "Severe Stroke",    "31.6%", "kpi-danger"
    return               "Very Severe",     "53.5%", "kpi-danger"

@st.cache_data
def calc_tpa_dose(weight_kg: float) -> tuple:
    dose = round(min(weight_kg * 0.25, 25.0), 1)
    return dose, weight_kg

@st.cache_data
def calc_dtn_minutes(door_dt: datetime.datetime, needle_dt: datetime.datetime) -> float:
    return max((needle_dt - door_dt).total_seconds() / 60, 0.0)

@st.cache_data
def get_score(val: str) -> int:
    try:
        return int(str(val).split(" - ")[0].strip().split("-")[0].strip())
    except (ValueError, IndexError):
        return 0

# ═══════════════════════════════════════════════════════════════════════════
# STATE INITIALISATION
# ═══════════════════════════════════════════════════════════════════════════
def _s(key: str, default: Any):
    if key not in st.session_state:
        st.session_state[key] = default

def init_state():
    _s("ui", {
        "screen":   "🏠 Dashboard",
        "unlocked": ALL_SCREENS.copy(),  # Everything unlocked by default
        "role":     "Physician",
        "logged_in": False,
    })

    _s("clinical_data", {
        "mrn": "", "pat_name": "", "sex": "Male",
        "dob": datetime.date(1970, 1, 1),
        "pres_date": datetime.date.today(),
        "pres_time": (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).time(),
        "location": "ED", "resident": "", "consultant": "",
        "sudden_onset": False,
        "r_loc": False, "r_seizures": False,
        "r_face": False, "r_arm": False, "r_leg": False,
        "r_speech": False, "r_visual": False,
        "r_override": False, "rosier_score": 0, "rosier_done": False,
        "chk_vitals": False, "chk_monitor": False, "chk_iv": False,
        "chk_bsr": False, "chk_ecg": False, "chk_labs": False, "chk_ptinr": False,
        "lkw_date": datetime.date.today(),
        "lkw_time": datetime.time(0, 0),
        "stroke_code": False,
        "time_since_lkw_hrs": 0.0,
        "assigned_pathway": "Pending",
        "ext_pathway_choice": "Wake Up Stroke / Unknown Onset Pathway",
        "ct_result": "Pending",
        "ncct_aspects": 10,
        "nihss_done": False, "imaging_done": False,
        "contra_done": False, "routing_done": False,
        **{k: get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        "nihss_baseline": 0, "nihss_calculated": False,
        "prisms_disabling": True,
        **{f"{k}_2h": get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        **{f"{k}_24h": get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        **{f"{k}_dc": get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        "nihss_2h": 0, "nihss_2h_done": False,
        "nihss_24h": 0, "nihss_24h_done": False,
        "nihss_dc": 0, "nihss_dc_done": False,
        "cta_lvo": "Not Performed",
        "advanced_img": "None",
        "mismatch_status": "Pending / Not Evaluated",
        **{f"abs_ci_{i}": False for i in range(1, 11)},
        **{f"rel_ci_{i}": False for i in range(1, 19)},
        "pt_weight": 70.0,
        "tpa_time": datetime.time(0, 0),
        "mt_date": datetime.date.today(),
        "mt_time": datetime.time(0, 0),
        "groin_time": datetime.time(0, 0),
        "treatment_refused": False,
        "treatment_not_indicated": False,
        "final_routing": "Pending",
        "toast": "5) Undetermined etiology",
        "mrs_pre": 0, "mrs_discharge": 0,
        "pn_bp": "", "pn_hr": "", "pn_rr": "", "pn_temp": "", "pn_spo2": "", "pn_bsr": "",
        "pn_gcs_e": "", "pn_gcs_m": "", "pn_gcs_v": "",
        "pn_speech": "", "pn_pupils": "", "pn_eom": "",
        "pn_face": "", "pn_power_grip": "", "pn_power_drift": "",
        "pn_reflexes": "", "pn_plantars": "", "pn_cerebel": "",
        "pn_sensations": "", "pn_nihss_curr": "",
        "pn_cvs": "", "pn_resp": "", "pn_abdomen": "",
        "pn_bedsore": "", "pn_bowel": "", "pn_swallowing": "",
        "pn_urinary_cath": "", "pn_io": "", "pn_oob": "",
        "pn_aspiration": "", "pn_dvt": "", "pn_cellulitis": "",
        "pn_assessment": "", "pn_plan": "",
        "pn_pt_plan": "", "pn_st_plan": "", "pn_ot_plan": "",
        "pn_discharge_days": "",
        "pn_day_num": "1", "pn_day_stroke": "",
        "toast_lacunar": False, "toast_cardioembolic": False,
        "toast_large_artery": False, "toast_other": False,
        "rf_prev_stroke": False, "rf_dm": False, "rf_htn": False,
        "rf_ihd": False, "rf_smoking": False,
    })

    def _cpoe_defaults():
        d = {}
        for sec in ["s1","s2","s3"]:
            for day in ["d1","d2","d3"]:
                for cat in ["p","l","i","n","m","f","r"]:
                    for num in range(1, 25): # Increased to 25 to accommodate full pathway orders
                        d[f"{sec}_{day}_{cat}{num}"] = False
                d[f"{sec}_{day}_signed"] = False
                d[f"{sec}_{day}_signer_name"] = ""
                d[f"{sec}_{day}_nurse_name"] = ""
                d[f"{sec}_{day}_variance"] = ""
                d[f"{sec}_{day}_locked"] = False
            d[f"{sec}_d3_disp"] = "Pending"
        return d

    _s("order_data", _cpoe_defaults())
    _s("variance_log", [])
    _s("progress_notes", [])

    if "monitor_grid" not in st.session_state:
        intervals = (
            ["00:15","00:30","00:45","01:00","01:15","01:30","01:45","02:00"] +
            ["02:30","03:00","03:30","04:00","04:30","05:00","05:30","06:00",
             "06:30","07:00","07:30","08:00"] +
            [f"{h:02d}:00" for h in range(9, 25)]
        )
        st.session_state.monitor_grid = pd.DataFrame({
            "Time since IVT": intervals,
            "Actual Time": [""] * len(intervals),
            "GCS E": [""] * len(intervals),
            "GCS M": [""] * len(intervals),
            "GCS V": [""] * len(intervals),
            "GCS Total": [""] * len(intervals),
            "Pulse": [""] * len(intervals),
            "BP": [""] * len(intervals),
            "RR": [""] * len(intervals),
        })

init_state()

# ═══════════════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════════════
def cd(key: str, default: Any = None) -> Any:
    return st.session_state.clinical_data.get(key, default)

def set_cd(key: str, val: Any):
    st.session_state.clinical_data[key] = val

def od(key: str) -> Any:
    return st.session_state.order_data.get(key, False)

def set_od(key: str, val: Any):
    st.session_state.order_data[key] = val

def go_to(screen: str):
    st.session_state.ui["screen"] = screen
    if screen not in st.session_state.ui["unlocked"]:
        st.session_state.ui["unlocked"].append(screen)
    
    # Safely force the app to render the new screen
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

def current_role() -> str:
    return st.session_state.ui.get("role", "Physician")

def can_write(section: str) -> bool:
    role = current_role()
    return ROLE_PERMISSIONS.get(role, {}).get(section, "read") == "write"

def readonly_banner(section: str):
    if not can_write(section):
        st.markdown(
            f'<div class="readonly-banner">🔒 READ-ONLY — {current_role()} role cannot edit this section</div>',
            unsafe_allow_html=True
        )

def card(text: str, style: str = "info", icon: str = ""):
    st.markdown(f'<div class="card card-{style}">{icon + " " if icon else ""}{text}</div>',
                unsafe_allow_html=True)

def banner(text: str, colour: str = "blue", icon: str = ""):
    st.markdown(f'<div class="section-banner banner-{colour}">{icon + " " if icon else ""}{text}</div>',
                unsafe_allow_html=True)

def kpi(value: str, label: str, style: str = "primary"):
    return (f'<div class="kpi-box kpi-{style}">'
            f'<span class="kpi-val">{value}</span>'
            f'<span class="kpi-lbl">{label}</span></div>')

def log_variance(section: str, day: str, item: str, reason: str):
    st.session_state.variance_log.append({
        "timestamp": (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
        "section": section, "day": day, "item": item, "reason": reason,
        "user": current_role(), "patient": cd("pat_name"), "mrn": cd("mrn"), "resolved": False,
    })

def calc_nihss_score(suffix: str = "") -> int:
    suffix_str = f"_{suffix}" if suffix else ""
    return sum(
        get_score(st.session_state.clinical_data.get(f"{k}{suffix_str}", "0 - x"))
        for k in NIHSS_KEYS
    )

def get_dtn_status():
    if not cd("nihss_calculated") or cd("tpa_time") == datetime.time(0, 0):
        return None, None
    door_dt   = datetime.datetime.combine(cd("pres_date"), cd("pres_time"))
    needle_dt = datetime.datetime.combine(cd("pres_date"), cd("tpa_time"))
    mins = calc_dtn_minutes(door_dt, needle_dt)
    if mins <= 0:
        return None, None
    if mins <= 45:   status = "ok"
    elif mins <= 60: status = "warning"
    else:            status = "danger"
    return mins, status

def generate_soap_note() -> str:
    c = st.session_state.clinical_data
    sc = c.get("nihss_baseline", 0)
    sev, mort, _ = nihss_severity(sc)
    pathway   = c.get("assigned_pathway", "Pending")
    pts_name  = c.get("pat_name", "[Patient Name]")
    age = ""
    if c.get("dob"):
        age = str((datetime.date.today() - c["dob"]).days // 365)
    soap = f"""**SUBJECTIVE:**
{pts_name}, {age}y {c.get('sex','')}, presented on {c.get('pres_date','')} at {c.get('pres_time','')} from {c.get('location','')}.
Chief complaint: Sudden onset focal neurological deficit.
ROSIER Score: {c.get('rosier_score', 0)} ({"High likelihood of stroke/TIA" if c.get('rosier_score', 0) >= 1 else "Stroke less likely — consider mimic"}).

**OBJECTIVE:**
NIHSS (Baseline): {sc} — {sev} | 30-day mortality: {mort}
CT Brain: {c.get('ct_result', 'Pending')} | ASPECTS: {c.get('ncct_aspects', 'N/A')}
CTA LVO: {c.get('cta_lvo', 'Not Performed')}
Advanced Imaging: {c.get('advanced_img', 'None')} | Mismatch: {c.get('mismatch_status', 'N/A')}
Time since LKW: {c.get('time_since_lkw_hrs', 0.0):.1f} hours
Assigned Pathway: {pathway}

**ASSESSMENT:**
Acute Ischemic Stroke — {pathway}.
{"Absolute contraindications to IVT present." if any(c.get(f"abs_ci_{i}") for i in range(1,11)) else "No absolute contraindications to IVT identified."}
{"Relative contraindications noted — consultant reviewed." if any(c.get(f"rel_ci_{i}") for i in range(1,19)) else ""}
mRS Pre-stroke: {c.get('mrs_pre', 0)} | mRS at Discharge: {c.get('mrs_discharge', 0)}

**PLAN:**
{c.get('final_routing', 'Routing decision pending.')}.
Weight: {c.get('pt_weight', 70.0)} kg.
{"tPA Administered — Door-to-Needle time documented." if "Thrombolysis" in c.get("final_routing","") else ""}
{"EVT performed." if "EVT" in c.get("final_routing","") or "MT" in c.get("assigned_pathway","") else ""}
Resident: {c.get('resident','')} | Consultant: {c.get('consultant','')}
"""
    return soap.strip()

# ═══════════════════════════════════════════════════════════════════════════
# SIGN-OFF / VARIANCE ENGINE (JCI)
# ═══════════════════════════════════════════════════════════════════════════
def sign_off_block(prefix: str, day_num: int, required_keys: list,
                   section_label: str = "", can_edit: bool = True):
    st.markdown("---")
    locked_key = f"{prefix}_locked"
    signed_key = f"{prefix}_signed"
    signer_key = f"{prefix}_signer_name"
    nurse_key  = f"{prefix}_nurse_name"
    var_key    = f"{prefix}_variance"

    if st.session_state.order_data.get(locked_key, False):
        signer = st.session_state.order_data.get(signer_key, "")
        nurse  = st.session_state.order_data.get(nurse_key, "")
        var    = st.session_state.order_data.get(var_key, "")
        st.success(f"✅ **Day {day_num} Locked & Signed** | Resident: {signer} | Nurse: {nurse}")
        if var:
            st.info(f"📋 **Variance Documented:** {var}")
        return

    if not can_edit:
        readonly_banner("physician")
        return

    banner(f"Day {day_num} Sign-Off & Order Completion", "grey", "📝")
    c1, c2 = st.columns(2)
    with c1:
        sn = st.text_input("Resident / Fellow / MO Name & ID",
                           value=st.session_state.order_data.get(signer_key, ""),
                           key=f"signer_{prefix}")
        st.session_state.order_data[signer_key] = sn
    with c2:
        nn = st.text_input("Bedside Nurse Name & ID",
                           value=st.session_state.order_data.get(nurse_key, ""),
                           key=f"nurse_{prefix}")
        st.session_state.order_data[nurse_key] = nn

    if st.button(f"📝 Sign Off Day {day_num} Orders", key=f"sign_{prefix}"):
        st.session_state.order_data[signed_key] = True
        st.rerun()

    if st.session_state.order_data.get(signed_key, False):
        missing = [k for k in required_keys
                   if not st.session_state.order_data.get(k, False)]
        if missing:
            card(f"⚠️ **{len(missing)} order(s) not completed.** Variance documentation is mandatory per JCI standards.", "warning")
            vt = st.text_area(
                "Variance Reason & Action Taken (mandatory):",
                value=st.session_state.order_data.get(var_key, ""),
                key=f"var_{prefix}", height=80
            )
            st.session_state.order_data[var_key] = vt
            if st.button(f"📌 Submit Variance & Lock Day {day_num}", key=f"submit_{prefix}"):
                if not vt.strip():
                    card("Variance notes cannot be empty.", "danger", "🚨")
                else:
                    for k in missing:
                        log_variance(section_label, f"Day {day_num}", k, vt)
                    st.session_state.order_data[locked_key] = True
                    st.rerun()
        else:
            st.session_state.order_data[locked_key] = True
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# NIHSS FORM (Reusable Component)
# ═══════════════════════════════════════════════════════════════════════════
def nihss_form(suffix: str, label: str, expand: bool = False):
    opts = get_nihss_opts()
    suffix_key = f"_{suffix}" if suffix else ""
    done_key   = f"nihss{suffix_key}_done" if suffix else "nihss_calculated"
    score_key  = f"nihss_{suffix}" if suffix else "nihss_baseline"

    with st.expander(f"NIHSS — {label}", expanded=expand):
        with st.form(f"nihss_form_{suffix or 'baseline'}"):
            col1, col2, col3, col4 = st.columns(4)
            groups = [
                ["n1a","n1b","n1c","n2"],
                ["n3","n4","n5l","n5r"],
                ["n6l","n6r","n7","n8"],
                ["n9","n10","n11"],
            ]
            for ci, grp in enumerate(groups):
                with [col1, col2, col3, col4][ci]:
                    for k in grp:
                        sk = f"{k}{suffix_key}"
                        cur = cd(sk) or opts[k][0]
                        cur_idx = opts[k].index(cur) if cur in opts[k] else 0
                        chosen = st.selectbox(NIHSS_LABELS[k], opts[k],
                                              index=cur_idx, key=f"nihss_sel_{sk}")
                        set_cd(sk, chosen)
            submitted = st.form_submit_button("✅ Calculate NIHSS")
            if submitted:
                sc = sum(get_score(cd(f"{k}{suffix_key}") or "0") for k in NIHSS_KEYS)
                set_cd(score_key, sc)
                set_cd(done_key, True)
                st.rerun()

        if cd(done_key):
            sc = cd(score_key) or 0
            sev, mort, style = nihss_severity(sc)
            st.markdown(
                f'<div class="kpi-grid">'
                f'{kpi(str(sc), "NIHSS Score", "primary")}'
                f'{kpi(sev, "Severity", style)}'
                f'{kpi(mort, "30-Day Mortality", "danger")}'
                f'</div>',
                unsafe_allow_html=True
            )

# ═══════════════════════════════════════════════════════════════════════════
# LIFESTYLE COUNSELLING (Reusable Component)
# ═══════════════════════════════════════════════════════════════════════════
def lifestyle_checks(prefix: str):
    st.markdown("##### 🌱 Lifestyle Modification Counselling")
    c1, c2 = st.columns(2)
    items = [
        ("f2","🚭 Smoking cessation"), ("f3","🥦 Healthy diet"),
        ("f4","😴 Regular sleep"),     ("f5","⚖️ Weight reduction"),
        ("f6","💊 Control cholesterol"),("f7","🩺 Manage blood pressure"),
        ("f8","🩸 Manage blood sugar"),
    ]
    for idx, (k, label) in enumerate(items):
        col = c1 if idx % 2 == 0 else c2
        with col:
            val = st.checkbox(label, value=od(f"{prefix}_{k}"),
                              key=f"ls_{prefix}_{k}",
                              disabled=not can_write("physician"))
            set_od(f"{prefix}_{k}", val)

def render_order_day(sec: str, day: str, day_num: int, orders: dict,
                     req_keys: list, section_label: str):
    locked = od(f"{sec}_{day}_locked")

    for cat_banner, items in orders.items():
        colour, icon = items[0], items[1]
        banner(cat_banner, colour, icon)
        for k, label in items[2:]:
            full_key = f"{sec}_{day}_{k}"
            write_section = (
                "nursing" if k.startswith("n") else
                "allied"  if k.startswith("m") else
                "physician"
            )
            v = st.checkbox(label,
                            value=od(full_key),
                            key=f"cb_{full_key}",
                            disabled=locked or not can_write(write_section))
            set_od(full_key, v)

    req = [f"{sec}_{day}_{k}" for k in req_keys]
    sign_off_block(f"{sec}_{day}", day_num, req, section_label, can_write("physician"))

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR — LOGIN & NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px 0;'>
      <div style='font-size:2.5rem;'>🏥</div>
      <div style='font-size:1rem; font-weight:800; color:#ffffff; letter-spacing:0.5px; line-height:1.3;'>
        Shifa International<br>Hospitals Ltd.
      </div>
      <div style='font-size:0.7rem; color:#93C5FD; margin-top:4px;'>
        AIS EMR | FM-MSA-429 Rev:01
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("#### 👤 Clinical Role")
    role_icons = {"Physician":"🩺", "Nurse":"💉",
                  "Allied Health / Rehab":"🦽", "Admin / Audit":"🔐"}
    sel_role = st.selectbox(
        "Select Role:", ROLES,
        index=ROLES.index(st.session_state.ui["role"]),
        key="sb_role",
        help="Role determines read/write permissions across all tiles (RBAC)"
    )
    st.session_state.ui["role"] = sel_role
    r_icon = role_icons.get(sel_role, "👤")
    st.markdown(
        f'<div style="margin:6px 0 12px 0;">'
        f'<span class="role-badge role-{sel_role.split()[0].lower()}">'
        f'{r_icon} {sel_role}</span></div>',
        unsafe_allow_html=True
    )

    if cd("pat_name"):
        st.markdown("---")
        st.markdown(f"**Patient:** {cd('pat_name')}")
        st.markdown(f"**MRN:** {cd('mrn') or '—'}")
        st.markdown(f"**Pathway:** `{cd('assigned_pathway')}`")
        if cd("nihss_calculated"):
            sc = cd("nihss_baseline")
            sev, mort, _ = nihss_severity(sc)
            st.markdown(f"**NIHSS:** {sc} — {sev}")
        dtn_mins, dtn_status = get_dtn_status()
        if dtn_mins:
            colour = {"ok":"#22C55E","warning":"#F59E0B","danger":"#EF4444"}.get(dtn_status,"#9CA3AF")
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:10px;margin:8px 0;">'
                f'<div style="font-size:0.72rem;color:#93C5FD;">🕐 Door-to-Needle</div>'
                f'<div style="font-size:1.6rem;font-weight:900;color:{colour};">{dtn_mins:.0f} min</div>'
                f'<div style="font-size:0.65rem;color:#93C5FD;">{"✅ On target" if dtn_status=="ok" else "⚠️ Near limit" if dtn_status=="warning" else "🚨 Exceeded 60 min"}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("#### 🗺️ Navigation")
    nav_options = st.session_state.ui["unlocked"]
    cur_idx = nav_options.index(st.session_state.ui["screen"]) \
              if st.session_state.ui["screen"] in nav_options else 0
    # REMOVED key="sb_nav" so we can programmatically change pages without crashing
    selected = st.radio("Go to Screen:", options=nav_options, index=cur_idx)
    if selected != st.session_state.ui["screen"]:
        st.session_state.ui["screen"] = selected
        st.rerun()

    vl = st.session_state.variance_log
    unresolved = sum(1 for v in vl if not v["resolved"])
    if unresolved:
        st.markdown("---")
        st.markdown(
            f'<div style="background:#7F1D1D;border-radius:8px;padding:10px;text-align:center;">'
            f'<span style="font-size:1.3rem;">⚠️</span><br>'
            f'<span style="font-weight:700;font-size:0.85rem;">{unresolved} Open Variance(s)</span><br>'
            f'<span style="font-size:0.72rem;opacity:0.8;">See JCI Audit Screen</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("<span style='font-size:0.65rem;opacity:0.5;'>AHA/ASA 2026 | JCI Standards<br>© Shifa International Hospitals</span>",
                unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE HEADER UTILITY
# ═══════════════════════════════════════════════════════════════════════════
def page_header(title: str, subtitle: str = ""):
    pat = cd("pat_name")
    mrn = cd("mrn")
    pat_str = f"{pat} | MRN: {mrn}" if pat else "No patient loaded"
    role = current_role()
    r_icon = {"Physician":"🩺","Nurse":"💉","Allied Health / Rehab":"🦽","Admin / Audit":"🔐"}.get(role,"👤")
    st.markdown(f"""
    <div class="hospital-header">
      <div>
        <div class="hosp-name">🏥 Shifa International Hospitals Ltd.</div>
        <div class="screen-title">{title}{(' — ' + subtitle) if subtitle else ''}</div>
      </div>
      <div class="meta">
        {pat_str}<br>
        <span class="role-badge role-{role.split()[0].lower()}">{r_icon} {role}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# ── SCREEN ROUTING
# ═══════════════════════════════════════════════════════════════════════════

# ── SCREEN: 🏠 DASHBOARD ──────────────────────────────────────────────────
if st.session_state.ui["screen"] == "🏠 Dashboard":
    page_header("🏠 Clinical Dashboard", "Acute Ischemic Stroke EMR")

    sc = cd("nihss_baseline") or 0
    sev, mort, sev_style = nihss_severity(sc) if cd("nihss_calculated") else ("—", "—", "neutral")
    dtn_mins, dtn_status = get_dtn_status()
    dtn_val   = f"{dtn_mins:.0f}m" if dtn_mins else "—"
    dtn_style = {"ok":"success","warning":"warning","danger":"danger"}.get(dtn_status,"neutral")

    st.markdown(
        f'<div class="kpi-grid">'
        f'{kpi(cd("assigned_pathway") or "Pending", "Active Pathway", "primary")}'
        f'{kpi(str(sc) if cd("nihss_calculated") else "—", "NIHSS Baseline", sev_style)}'
        f'{kpi(sev, "Severity", sev_style)}'
        f'{kpi(dtn_val, "Door-to-Needle", dtn_style)}'
        f'{kpi(str(len(st.session_state.variance_log)), "Variances Logged", "warning" if st.session_state.variance_log else "success")}'
        f'</div>',
        unsafe_allow_html=True
    )

    # Calculate pathway progress (PASTE THIS BLOCK HERE)
    steps_completed = sum([
        bool(cd("rosier_done")), 
        bool(cd("nihss_done")), 
        bool(cd("routing_done")), 
        bool(od("s1_d1_signed") or od("s2_d1_signed") or od("s3_d1_signed"))
    ])
    progress_pct = int((steps_completed / 4) * 100)
    
    st.markdown(f"**Pathway Completion: {progress_pct}%**")
    st.progress(progress_pct)
    st.markdown("<br>", unsafe_allow_html=True)
    # END OF PASTED BLOCK

    if dtn_mins and dtn_status == "danger":
        card(f"🚨 **Door-to-Needle time is {dtn_mins:.0f} minutes — EXCEEDS 60-minute target.** "
             f"Review delays and document variance.", "danger")
    elif dtn_mins and dtn_status == "warning":
        card(f"⚠️ **Door-to-Needle time is {dtn_mins:.0f} minutes — approaching 60-minute limit.**", "warning")

    st.markdown("---")
    st.markdown("### 🧭 Clinical Assessment Pathway")

    def tile_btn(label, icon, screen, status="active", sub="", key_sfx=""):
        status_icon = {"done":"✅","active":"▶️","warning":"⚠️","critical":"🚨","locked":"🔒"}.get(status,"▶️")
        
        # Build a clean text label with newlines (NO markdown symbols)
        if sub:
            button_label = f"{status_icon} {icon}\n{label}\n({sub})"
        else:
            button_label = f"{status_icon} {icon}\n{label}"
            
        # The entire tile is now a clickable button!
        if st.button(button_label, key=f"btn_{screen}_{key_sfx}", use_container_width=True):
            go_to(screen)

    st.markdown("### 🚑 1. ER / Code Stroke Activation")
    col1, col2 = st.columns(2)
    with col1:
        s1_status = "done" if cd("rosier_done") else "active"
        tile_btn("Code Activation", "🚨", "Phase 1: ER Code Activation (Duty Dr)", s1_status, "ROSIER, LKW & Rapid Labs")
    with col2:
        s2_status = "done" if cd("nihss_done") else "active"
        tile_btn("Acute Neuro Eval", "⚕️", "Phase 2: Acute Neuro Eval (Responder)", s2_status, "NIHSS & Neuro Exam")

    st.markdown("### 🧠 2. Neurology Decision & Routing")
    col3, col4 = st.columns(2)
    with col3:
        s3_status = "done" if cd("routing_done") else "active"
        tile_btn("Imaging & Routing", "⏱️", "Phase 3: Imaging & Routing Gate", s3_status, "CT/CTA, CIs & TPA/EVT Decision")
    with col4:
        s4_status = "active" if cd("routing_done") else "locked"
        tile_btn("Stroke Unit Admission", "🏥", "Phase 4: Stroke Unit Orders (Days 1-3)", s4_status, "Physician, Nursing, Rehab Orders")

    st.markdown("### 📋 3. Ward Management & Rounds")
    col5, col6, col7 = st.columns(3)
    with col5:
        tile_btn("Daily Rounds & Notes", "📝", "Phase 5: Daily Rounds & Progress Notes", "active", "SOAP & Attending Notes")
    with col6:
        tile_btn("Serial NIHSS & Dispo", "📈", "Phase 6: Serial NIHSS & Outcomes", "active", "2h, 24h & Discharge mRS")
    with col7:
        tile_btn("Variance Audit", "🔍", "Variance Audit", "warning" if st.session_state.variance_log else "active", f"{len(st.session_state.variance_log)} event(s)")


# ── SCREEN: S1 — TRIAGE & ROSIER ─────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 1: ER Code Activation (Duty Dr)":
    page_header("S1: Initial Triage & Rapid Assessment", "ROSIER Scale")

    banner("Patient Demographics", "blue", "👤")
    c1, c2, c3 = st.columns(3)
    with c1:
        v = st.text_input("MRN / Patient ID", value=cd("mrn"), key="w_mrn"); set_cd("mrn", v)
        v = st.date_input("Date of Birth", value=cd("dob"), key="w_dob"); set_cd("dob", v)
    with c2:
        v = st.text_input("Patient Full Name", value=cd("pat_name"), key="w_name"); set_cd("pat_name", v)
        v = st.selectbox("Sex", ["Male","Female","Other"],
                         index=["Male","Female","Other"].index(cd("sex")), key="w_sex"); set_cd("sex", v)
    with c3:
        v = st.selectbox("Location", ["ED","IPD"],
                         index=["ED","IPD"].index(cd("location")), key="w_loc"); set_cd("location", v)
        v = st.text_input("Resident / Fellow / MO", value=cd("resident"), key="w_res"); set_cd("resident", v)
        v = st.text_input("Consultant Name", value=cd("consultant"), key="w_con"); set_cd("consultant", v)

    c4, c5 = st.columns(2)
    with c4:
        v = st.date_input("Presentation Date", value=cd("pres_date"), key="w_pdate"); set_cd("pres_date", v)
    with c5:
        v = st.time_input("Presentation Time", value=cd("pres_time"), key="w_ptime", step=60); set_cd("pres_time", v)

    v = st.checkbox("🚨 Sudden onset focal neurological deficit and/or altered mental status",
                    value=cd("sudden_onset"), key="w_sudden")
    set_cd("sudden_onset", v)

    banner("ROSIER Scale", "blue", "📋")
    card("Score of <b>+1 or higher</b> indicates high likelihood of stroke/TIA.", "info")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Negative Features (subtract if present):**")
        v = st.checkbox("Has there been loss of consciousness or syncope? (−1)", value=cd("r_loc"), key="w_rloc"); set_cd("r_loc", v)
        v = st.checkbox("Has there been seizure activity? (−1)", value=cd("r_seizures"), key="w_rseiz"); set_cd("r_seizures", v)
    with r2:
        st.markdown("**New Acute Onset Features (+1 each):**")
        for key, label in [("r_face","i) Asymmetric facial weakness"),
                           ("r_arm","ii) Asymmetric arm weakness"),
                           ("r_leg","iii) Asymmetric leg weakness"),
                           ("r_speech","iv) Speech disturbance"),
                           ("r_visual","v) Visual field defect")]:
            v = st.checkbox(label, value=cd(key), key=f"w_{key}"); set_cd(key, v)

    pos = sum([cd("r_face"),cd("r_arm"),cd("r_leg"),cd("r_speech"),cd("r_visual")])
    neg = sum([cd("r_loc"),cd("r_seizures")])
    rosier = pos - neg
    set_cd("rosier_score", rosier)

    r_style = "success" if rosier >= 1 else "warning"
    r_msg   = "✅ High likelihood of stroke/TIA" if rosier >= 1 else "⚠️ Stroke less likely — consider stroke mimic"
    st.markdown(f'<div class="kpi-grid">{kpi(str(rosier), "ROSIER Score", "primary")}</div>', unsafe_allow_html=True)
    card(r_msg, r_style)

    banner("Rapid Assessment Checklist", "teal", "⚡")
    ra1, ra2 = st.columns(2)
    checks = [
        ("chk_vitals","Check Vitals & SpO₂"),("chk_monitor","Attach Cardiac Monitor"),
        ("chk_iv","📌 Large bore IV Access (MANDATORY)"),("chk_bsr","📌 BSR / Blood Glucose (MANDATORY)"),
        ("chk_ct", "🧠 Order Urgent NCCT Brain"), ("chk_ecg","ECG"),
        ("chk_labs","CBC, Na, K, Cr, Trop-I"),("chk_ptinr","PT / INR"),
    ]
    for idx, (k, label) in enumerate(checks):
        with ra1 if idx < 4 else ra2:
            v = st.checkbox(label, value=cd(k), key=f"w_{k}"); set_cd(k, v)

    st.markdown("---")
    
    # Check mandatory fields
    ready_to_proceed = cd("chk_iv") and cd("chk_bsr")
    if not ready_to_proceed:
        st.warning("⚠️ **Mandatory Action Required:** You must secure Large Bore IV Access and check Blood Glucose (BSR) to proceed to the next phase.")

    c_prev, c_next = st.columns(2)
    with c_next:
        if rosier >= 1 or cd("r_override"):
            if st.button("💾 Save Triage & Proceed ➡️", key="btn_s1_next", disabled=not ready_to_proceed, use_container_width=True):
                set_cd("rosier_done", True)
                go_to("Phase 2: Acute Neuro Eval (Responder)")
    with c_prev:
        if rosier < 1:
            v = st.checkbox("🔓 Consultant Override: Proceed despite low ROSIER score", value=cd("r_override"), key="w_rov"); set_cd("r_override", v)

# ── SCREEN: PHASE 2 — ACUTE CLINICAL EVALUATION ─────────────────────────
elif st.session_state.ui["screen"] == "Phase 2: Acute Neuro Eval (Responder)":
    page_header("Phase 2: Acute Clinical Evaluation", "Detailed Neuro Exam & NIHSS")

    # Reusable Options
    opts_sp = ["Normal", "Mild Dysarthria", "Severe Dysarthria", "Aphasia", "Mute", "Intubated", "Other (See Remarks)"]
    opts_pup = ["Equal & Reactive", "Unequal", "Sluggish", "Fixed/Dilated", "Other (See Remarks)"]
    opts_eom = ["Normal", "Partial Gaze Palsy", "Forced Deviation", "Other (See Remarks)"]
    opts_vis = ["Normal", "Partial Hemianopia", "Complete Hemianopia", "Bilateral Blindness", "Other (See Remarks)"]
    opts_face = ["Symmetric", "Minor Paralysis", "Partial/Complete Paralysis", "Other (See Remarks)"]
    opts_pow = ["5/5 Normal", "4/5 Mild Weak", "3/5 Anti-Gravity", "2/5 Not Anti-Gravity", "1/5 Flicker", "0/5 None", "Other"]
    opts_tone = ["Normal", "Flaccid/Hypotonic", "Spastic/Hypertonic", "Rigidity", "Other"]
    opts_sens = ["Normal", "Right-sided Loss", "Left-sided Loss", "Bilateral Loss", "Other (See Remarks)"]
    opts_cer = ["Absent", "Present Right", "Present Left", "Present Bilateral", "Other (See Remarks)"]
    opts_ref = ["Normal (2+)", "Brisk (3+)", "Depressed (1+)", "Absent (0)", "Other"]
    opts_pla = ["Flexor (Downward)", "Extensor (Upgoing)", "Equivocal", "Mute", "Other"]
    opts_somi = ["Negative (Supple Neck)", "Positive (Neck Stiffness/Signs)", "Other (See Remarks)"]

    def _idx(opts, val): return opts.index(val) if val in opts else 0

    banner("Detailed Neurological Examination", "teal", "🔍")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown("**Cranial Nerves / Head**")
        v = st.selectbox("Speech:", opts_sp, index=_idx(opts_sp, cd("ex_speech")), key="ex_sp"); set_cd("ex_speech", v)
        v = st.selectbox("Pupils:", opts_pup, index=_idx(opts_pup, cd("ex_pupils")), key="ex_pup"); set_cd("ex_pupils", v)
        v = st.selectbox("EOM / Gaze:", opts_eom, index=_idx(opts_eom, cd("ex_eom")), key="ex_eom"); set_cd("ex_eom", v)
        v = st.selectbox("Visual Fields:", opts_vis, index=_idx(opts_vis, cd("ex_vis")), key="ex_vis"); set_cd("ex_vis", v)
        v = st.selectbox("Face / Tongue:", opts_face, index=_idx(opts_face, cd("ex_face")), key="ex_fac"); set_cd("ex_face", v)
        v = st.text_input("Carotid Bruit (Text):", value=cd("ex_bruit",""), key="ex_bruit"); set_cd("ex_bruit", v)
    with e2:
        st.markdown("**Motor & Tone (Bilateral)**")
        p1, p2 = st.columns(2)
        with p1:
            v = st.selectbox("Right Arm Power:", opts_pow, index=_idx(opts_pow, cd("ex_pow_ra")), key="pow_ra"); set_cd("ex_pow_ra", v)
            v = st.selectbox("Right Leg Power:", opts_pow, index=_idx(opts_pow, cd("ex_pow_rl")), key="pow_rl"); set_cd("ex_pow_rl", v)
            v = st.selectbox("Right Tone:", opts_tone, index=_idx(opts_tone, cd("ex_tone_r")), key="tone_r"); set_cd("ex_tone_r", v)
        with p2:
            v = st.selectbox("Left Arm Power:", opts_pow, index=_idx(opts_pow, cd("ex_pow_la")), key="pow_la"); set_cd("ex_pow_la", v)
            v = st.selectbox("Left Leg Power:", opts_pow, index=_idx(opts_pow, cd("ex_pow_ll")), key="pow_ll"); set_cd("ex_pow_ll", v)
            v = st.selectbox("Left Tone:", opts_tone, index=_idx(opts_tone, cd("ex_tone_l")), key="tone_l"); set_cd("ex_tone_l", v)
    with e3:
        st.markdown("**Sensory, Reflexes & Systemic**")
        r1, r2 = st.columns(2)
        with r1:
            v = st.selectbox("Right Reflex:", opts_ref, index=_idx(opts_ref, cd("ex_ref_r")), key="ref_r"); set_cd("ex_ref_r", v)
            v = st.selectbox("Right Plantar:", opts_pla, index=_idx(opts_pla, cd("ex_pla_r")), key="pla_r"); set_cd("ex_pla_r", v)
        with r2:
            v = st.selectbox("Left Reflex:", opts_ref, index=_idx(opts_ref, cd("ex_ref_l")), key="ref_l"); set_cd("ex_ref_l", v)
            v = st.selectbox("Left Plantar:", opts_pla, index=_idx(opts_pla, cd("ex_pla_l")), key="pla_l"); set_cd("ex_pla_l", v)
        
        v = st.selectbox("Sensations:", opts_sens, index=_idx(opts_sens, cd("ex_sens")), key="ex_sens"); set_cd("ex_sens", v)
        v = st.selectbox("Cerebellar/Ataxia:", opts_cer, index=_idx(opts_cer, cd("ex_cer")), key="ex_cer"); set_cd("ex_cer", v)

    st.markdown("**Remarks / Free Text (Required if 'Other' selected above)**")
    v = st.text_input("Detailed notes, systemic exam (CVS/Resp), or custom neuro findings:", value=cd("ex_remarks",""), key="ex_remarks"); set_cd("ex_remarks", v)

    st.markdown("---")
    with st.expander("☑️ Step 1: NIHSS Assessment & PRISMS Criteria", expanded=not cd("nihss_done")):
        nihss_form("", "Baseline Assessment", expand=True)
        if cd("nihss_calculated"):
            sc = cd("nihss_baseline")
            
            # --- AUTOMATED PRISMS CRITERIA ---
            if sc <= 5:
                # Extract numeric scores from the NIHSS strings
                n3_val  = get_score(cd("n3"))
                n5l_val = get_score(cd("n5l"))
                n5r_val = get_score(cd("n5r"))
                n6l_val = get_score(cd("n6l"))
                n6r_val = get_score(cd("n6r"))
                n9_val  = get_score(cd("n9"))
                n11_val = get_score(cd("n11"))
                
                # Logic Gate: Are deficits clearly disabling?
                is_disabling = (n3_val >= 2 or n5l_val >= 2 or n5r_val >= 2 or 
                                n6l_val >= 2 or n6r_val >= 2 or n9_val >= 2 or n11_val >= 2)
                
                set_cd("prisms_disabling", is_disabling)
                
                if is_disabling:
                    card("✅ **Guideline Alert:** Deficits are considered CLEARLY DISABLING (Meets PRISMS criteria). Patient remains an IVT candidate.", "success")
                else:
                    card("⚠️ **Guideline Alert:** Deficits are NOT clearly disabling per AHA/ASA criteria. Consider DAPT instead of IVT.", "warning")
                    # Provide a manual override just in case clinical judgment dictates otherwise
                    v_ov = st.checkbox("Physician Override: Treat as disabling based on clinical judgment", value=cd("prisms_override", False), key="w_prisms_ov")
                    set_cd("prisms_override", v_ov)
            # ---------------------------------
            
            c_prev, c_next = st.columns(2)
            with c_prev:
                if st.button("⬅️ Back to Phase 1", use_container_width=True): go_to("Phase 1: ER Code Activation (Duty Dr)")
            with c_next:
                if st.button("💾 Save & Proceed to Imaging Gate ➡️", key="btn_s2_next", use_container_width=True):
                    set_cd("nihss_done", True)
                    go_to("Phase 3: Imaging & Routing Gate")

# ── SCREEN: S3 — TIME & IMAGING GATE ────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 3: Imaging & Routing Gate":
    page_header("S3: Time & Imaging Gate", "Diagnostics, CIs & Routing")

    banner("1. Last Known Well & Live Time Window", "blue", "🕒")
    c1, c2 = st.columns(2)
    with c1:
        v = st.date_input("Date LKW", value=cd("lkw_date"), key="w_lkwd"); set_cd("lkw_date", v)
    with c2:
        # Added step=60 for exact minute typing
        v = st.time_input("Time LKW", value=cd("lkw_time"), key="w_lkwt", step=60); set_cd("lkw_time", v)

    lkw_dt = datetime.datetime.combine(cd("lkw_date"), cd("lkw_time"))
    
    # 🔴 FIX 1: LKW is now calculated against LIVE PKT system time (UTC + 5 hours)
    live_now_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    hours   = max((live_now_dt - lkw_dt).total_seconds() / 3600, 0.0)
    set_cd("time_since_lkw_hrs", hours)
    
    st.markdown(f"**Current System Time:** `{live_now_dt.strftime('%Y-%m-%d %H:%M')}`")
    st.markdown(f'<div class="kpi-grid">{kpi(f"{hours:.1f}h", "Live Time Since LKW", "primary" if hours <= 4.5 else "warning" if hours <= 24 else "danger")}</div>', unsafe_allow_html=True)

    if hours > 24:
        set_cd("assigned_pathway", "Non-Thrombolysis Pathway (> 24h)")
    else:
        if hours <= 4.5:
            set_cd("assigned_pathway", "IVT ± EVT Pathway (≤ 4.5h)")
        else:
            opts = ["Wake Up Stroke / Unknown Onset Pathway", "EVT ± IVT Extended Window Pathway (4.5–24h)"]
            cur = cd("ext_pathway_choice")
            ch = st.radio("Select Extended Window Pathway:", opts, index=opts.index(cur) if cur in opts else 0, key="w_extpath")
            set_cd("ext_pathway_choice", ch); set_cd("assigned_pathway", ch)

    st.markdown("---")
    banner("2. Neuroimaging (NCCT, CTA, CTP)", "teal", "🧠")
    card("⚠️ <b>CRITICAL:</b> If brain imaging shows hemorrhage, switch immediately to Hemorrhagic Stroke Pathway.", "danger")
    
    c3, c4 = st.columns(2)
    with c3:
        opts_ct = ["Pending", "Normal / No Hemorrhage", "Extensive Hypodensity (> 1/3 MCA territory)", "Intracranial Hemorrhage (ICH)"]
        v = st.radio("NCCT Brain Finding:", opts_ct, index=opts_ct.index(cd("ct_result")), key="w_ct"); set_cd("ct_result", v)
        
        if v == "Normal / No Hemorrhage":
            v_asp = st.number_input("ASPECTS Score (0–10)", min_value=0, max_value=10, value=cd("ncct_aspects"), key="w_aspects"); set_cd("ncct_aspects", v_asp)
    
    with c4:
        lvo_opts = ["Not Performed", "No LVO", "Yes — LVO Confirmed"]
        v = st.radio("CTA Carotid — LVO Status:", lvo_opts, index=lvo_opts.index(cd("cta_lvo")), key="w_lvo"); set_cd("cta_lvo", v)
        
        pathway = cd("assigned_pathway")
        if "IVT ± EVT" not in pathway:
            adv_opts = ["None", "CTP Brain", "MRI Brain"] if "Wake Up" in pathway else ["None", "CTP Brain"]
            v = st.radio("Advanced Imaging:", adv_opts, index=adv_opts.index(cd("advanced_img")) if cd("advanced_img") in adv_opts else 0, key="w_adv"); set_cd("advanced_img", v)
            if v != "None":
                m_opts = ["Pending / Not Evaluated", "✅ Mismatch Present", "❌ Mismatch NOT Present"]
                v_mm = st.radio("Mismatch Criteria:", m_opts, index=m_opts.index(cd("mismatch_status")) if cd("mismatch_status") in m_opts else 0, key="w_mm"); set_cd("mismatch_status", v_mm)

    st.markdown("---")
    
    # 🔴 FIX 2: Comprehensive Contraindications Checklist & Logic Gate
    with st.expander("☑️ Step 3: IVT Contraindications Checklist", expanded=True):
        st.markdown("##### 🛑 Absolute Contraindications (NO IVT)")
        
        # Link CT results to automatically trigger absolute contraindications
        is_ct_ich = (cd("ct_result") == "Intracranial Hemorrhage (ICH)")
        is_ct_hypo = (cd("ct_result") == "Extensive Hypodensity (> 1/3 MCA territory)")
        
        ci_abs_list = [
            ("abs_ci_1", "Acute ICH on imaging", is_ct_ich),
            ("abs_ci_2", "Extensive Hypodensity > 1/3 MCA territory", is_ct_hypo),
            ("abs_ci_3", "Severe coagulopathy (Plts <100k, INR >1.7, aPTT >40s, PT >15s)", False),
            ("abs_ci_4", "Infective endocarditis (Suspected or confirmed)", False),
            ("abs_ci_5", "Aortic arch dissection", False),
            ("abs_ci_6", "Intra-axial neoplasm", False),
            ("abs_ci_7", "Recent Neurosurgery or Mod/Severe TBI (< 14 days)", False),
            ("abs_ci_8", "Acute spinal cord injury (< 3 months)", False),
            ("abs_ci_9", "Amyloid-related conditions / ARIA", False),
        ]
        
        has_absolute_ci = False
        for key, label, is_forced in ci_abs_list:
            current_val = cd(key) or is_forced
            if is_forced: set_cd(key, True)
            
            val = st.checkbox(label + (" (Auto-selected from CT)" if is_forced else ""), 
                              value=current_val, key=f"chk_{key}", disabled=is_forced)
            set_cd(key, val)
            if val: has_absolute_ci = True

        st.markdown("##### ⚠️ Relative Contraindications (Consultant Decision)")
        ci_rel_list = [
            ("rel_ci_1", "Recent DOAC (<48 h)"),
            ("rel_ci_2", "Prior Ischemic Stroke (<3 months)"),
            ("rel_ci_3", "Prior Spontaneous ICH"),
            ("rel_ci_4", "Pre-existing disability / Frailty"),
            ("rel_ci_5", "Pregnancy / Post-partum"),
            ("rel_ci_6", "Recent STEMI (<3 months) or Acute pericarditis"),
            ("rel_ci_7", "Recent GI/GU bleeding (<21 days)"),
            ("rel_ci_8", "Major non-CNS surgery/trauma (<14 days)"),
        ]
        for key, label in ci_rel_list:
            val = st.checkbox(label, value=cd(key), key=f"chk_{key}")
            set_cd(key, val)

        st.markdown("---")
        v_ref = st.checkbox("Patient / next-of-kin refused IVT/EVT", value=cd("treatment_refused"), key="w_ref"); set_cd("treatment_refused", v_ref)
        
        if has_absolute_ci:
            card("🚨 **ABSOLUTE CONTRAINDICATION MET:** Intravenous Thrombolysis (IVT) is strictly contraindicated and locked.", "danger")

    with st.expander("☑️ Step 4: Final Routing Decision", expanded=True):
        # 1. Gather all lockout variables
        has_absolute_ci = any(cd(f"abs_ci_{i}") for i in range(1, 11))
        is_ct_ich = (cd("ct_result") == "Intracranial Hemorrhage (ICH)")
        refused = cd("treatment_refused")
        hours = cd("time_since_lkw_hrs")
        mismatch_met = (cd("mismatch_status") == "✅ Mismatch Present")
        
        # Check PRISMS failure (NIHSS <=5, not disabling, and no override)
        failed_prisms = (cd("nihss_baseline", 0) <= 5 and 
                         not cd("prisms_disabling", True) and 
                         not cd("prisms_override", False))

        # 2. Determine IVT Eligibility Logic Gate
        ivt_eligible = True
        ivt_lock_reason = ""

        if is_ct_ich:
            ivt_eligible = False
            ivt_lock_reason = "Active Intracranial Hemorrhage detected on CT."
        elif has_absolute_ci:
            ivt_eligible = False
            ivt_lock_reason = "Absolute Contraindication present."
        elif refused:
            ivt_eligible = False
            ivt_lock_reason = "Treatment refused by patient/next-of-kin."
        elif failed_prisms:
            ivt_eligible = False
            ivt_lock_reason = "NIHSS 0-5 and deficits are NOT clearly disabling (Failed PRISMS)."
        elif hours > 24:
            ivt_eligible = False
            ivt_lock_reason = f"Beyond 24-hour window ({hours:.1f}h)."
        elif hours > 4.5:
            # EXTENDED WINDOW LOGIC
            if mismatch_met:
                ivt_eligible = True
                st.info(f"💡 **Extended Window Unlock:** Time is {hours:.1f}h, but Advanced Imaging Mismatch criteria are met. IVT is permitted.")
            else:
                ivt_eligible = False
                ivt_lock_reason = f"Extended Window ({hours:.1f}h), but NO imaging mismatch criteria met."

        # 3. Dynamic Pathway Options based on logic
        options = ["Pending", "Section 2 — Non-Thrombolysis", "Section 3 — EVT Only (no IVT)"]
        
        if is_ct_ich:
            # HARD STOP for Hemorrhage
            options = ["Pending", "Hemorrhagic Stroke Pathway / Ward Transfer"]
            card("🚨 **HEMORRHAGE DETECTED:** Ischemic Pathway Terminated.", "danger")
        elif not ivt_eligible:
            # Lockout UI
            card(f"🔒 **IVT Routing Disabled:** {ivt_lock_reason}", "danger")
        else:
            # IVT is allowed, add the options to the list
            options.insert(1, "Section 1 — IV Thrombolysis (IVT)")
            options.insert(2, "Section 1 — IVT + EVT")
            
            # Mini-Checklist UI for clarity
            st.markdown(
                "<div style='font-size: 0.85rem; color: #16A34A; margin-bottom: 10px;'>"
                "✅ IVT Pathway Unlocked: No hemorrhage • No absolute CIs • Time/Imaging criteria met"
                "</div>", unsafe_allow_html=True
            )

        # 4. Render the radio buttons
        cur = cd("final_routing")
        if cur not in options: cur = "Pending"
            
        v_route = st.radio("Select Execution Pathway:", options, index=options.index(cur), key="w_route")
        set_cd("final_routing", v_route)

        # 5. Render Dose Calculator ONLY if IVT is actually selected
        if "IVT" in v_route and "Non-Thrombolysis" not in v_route:
            wt = st.number_input("Patient Weight (kg):", min_value=30.0, max_value=250.0, value=float(cd("pt_weight")), step=1.0, key="w_wt")
            set_cd("pt_weight", wt)
            dose, _ = calc_tpa_dose(wt)
            card(f'💉 <b>Tenecteplase: {dose} mg IV bolus</b> (Max 25 mg)', "success")
            t_val = st.time_input("Time of IVT Administration:", value=cd("tpa_time"), key="w_tpatime")
            set_cd("tpa_time", t_val)
        
        elif "Non-Thrombolysis" in v_route:
            card("💊 <b>ER ACTION REQUIRED:</b> Load with Antiplatelets (e.g., Aspirin 300mg) and start IV Normal Saline in ER before shifting to Stroke Unit.", "warning")

        if "EVT" in v_route:
            current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).hour
            if current_hour >= 17 or current_hour < 8:
                card("⚠️ <b>TIME WARNING:</b> Outside standard hours. IR services for EVT may not be available. Refer out if necessary.", "warning")
            else:
                card("🧲 <b>EVT CANDIDATE:</b> Call Interventional Radiology and obtain consent immediately.", "info")

    c_prev, c_next = st.columns(2)
    with c_prev:
        if st.button("⬅️ Back to Phase 2", use_container_width=True): go_to("Phase 2: Acute Neuro Eval (Responder)")
    with c_next:
        if st.button("💾 Save & Transfer to Stroke Unit ➡️", key="btn_s3_route", use_container_width=True):
            set_cd("routing_done", True)
            go_to("Phase 4: Stroke Unit Orders (Days 1-3)")

# ── SCREEN: S4 — UNIFIED ORDERS WORKSPACE ───────────────────────────────
elif st.session_state.ui["screen"] == "Phase 4: Stroke Unit Orders (Days 1-3)":
    page_header("S4: Unified Orders Workspace", "Parallel Pathway Execution")
    
    st.markdown(
        f'<div class="card card-info" style="display:flex; justify-content:space-between;">'
        f'<span>📌 <b>Active Pathway:</b> {cd("assigned_pathway")}</span>'
        f'<span><b>Final Route:</b> {cd("final_routing")}</span>'
        f'<span><b>Time since LKW:</b> {cd("time_since_lkw_hrs"):.1f}h</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    tab_phys, tab_nurse, tab_allied = st.tabs([
        "🩺 1. Physician Orders", 
        "💉 2. Nursing & Vitals", 
        "🤝 3. Allied Health"
    ])

    route = cd("final_routing")
    is_ivt = "IVT" in route or "Thrombolysis" in route
    is_evt = "EVT" in route
    is_non = "Non-Thrombolysis" in route
    sec = "s1" if is_ivt else ("s2" if is_non else "s3")

    # ================= TAB 1: PHYSICIAN ORDERS =================
    with tab_phys:
        if route == "Pending" or not cd("routing_done"):
            st.warning("⚠️ Complete the Clinical Evaluation and confirm a pathway in S3 to unlock orders.")
        else:
            st.subheader(f"Physician Orders & Investigations — {route}")
            d1, d2, d3 = st.tabs(["Day 1", "Day 2", "Day 3"])
            with d1:
                banner("A — Physician Orders (Day 1)", "teal", "🩺")
                sc = cd("nihss_baseline") or 0
                
                # Blood Pressure Rules
                if is_ivt:
                    card("🔴 BP Target post-IVT: TREAT ONLY if BP ≥ 180/105 mmHg", "danger")
                    v = st.checkbox("Labetalol, 5-20 mg IV bolus q 15 min or 2 mg/min infusion (max 300 mg/day) AND/OR Hydralazine, 5-20 mg IV push q 30 min. Treat only if BP ≥ 180/105", value=od(f"{sec}_d1_p1"), key="phys_d1_p1", disabled=not can_write("physician")); set_od(f"{sec}_d1_p1", v)
                elif is_non:
                    card("🩺 BP Target (Non-TPA): Permissive hypertension. Treat ONLY if BP is ≥ 220/120 mmHg.", "warning")
                    v = st.checkbox("Labetalol, 5-20 mg IV bolus q 15 min or 2 mg/min infusion AND/OR Hydralazine, 5-20 mg IV push q 30 min. Treat ONLY if BP is ≥ 220/120 mmHg", value=od(f"{sec}_d1_p1"), key="phys_d1_p1", disabled=not can_write("physician")); set_od(f"{sec}_d1_p1", v)
                else: # EVT Only
                    card("🟠 BP Target post-EVT: TREAT ONLY if BP > 180/105 mmHg.", "warning")
                    v = st.checkbox("Labetalol / Hydralazine (Same doses as above). Treat only if BP > 180/105", value=od(f"{sec}_d1_p1"), key="phys_d1_p1", disabled=not can_write("physician")); set_od(f"{sec}_d1_p1", v)

                v = st.checkbox("Injection Normal Saline (70 mL/hr)", value=od(f"{sec}_d1_p2"), key="phys_d1_p2", disabled=not can_write("physician")); set_od(f"{sec}_d1_p2", v)
                if is_evt:
                    v = st.checkbox("🟠 [EVT] Inspect arterial access/groin site and follow post-thrombectomy orders", value=od(f"{sec}_d1_p3"), key="phys_d1_p3", disabled=not can_write("physician")); set_od(f"{sec}_d1_p3", v)
                
                v = st.checkbox(f"Tab Aspirin 50–325 mg OD {'after 24h NCCT' if is_ivt else ''} OR DAPT (Clopidogrel 300mg + Aspirin 75mg load) if NIHSS ≤ 3", value=od(f"{sec}_d1_p4"), key="phys_d1_p4", disabled=not can_write("physician")); set_od(f"{sec}_d1_p4", v)
                v = st.checkbox("Rosuvastatin 20 mg at night", value=od(f"{sec}_d1_p5"), key="phys_d1_p5", disabled=not can_write("physician")); set_od(f"{sec}_d1_p5", v)
                v = st.checkbox("Intermittent pneumatic compression OR DVT prophylaxis", value=od(f"{sec}_d1_p6"), key="phys_d1_p6", disabled=not can_write("physician")); set_od(f"{sec}_d1_p6", v)
                
                banner("B — Lab Tests (Day 1)", "teal", "🔬")
                for i, (k, label) in enumerate([("l1","Fasting lipid profile"), ("l2","HbA1c"), ("l3","CBC, Na, K, Cr, Trop-I (If not done in ER)"), ("l4","PT/INR (If not done in ER)")]):
                    v = st.checkbox(label, value=od(f"{sec}_d1_{k}"), key=f"phys_d1_L{i}", disabled=not can_write("physician")); set_od(f"{sec}_d1_{k}", v)
                
                banner("C — Imaging (Day 1)", "teal", "🖼️")
                for i, (k, label) in enumerate([("i1","Chest X-Ray"), ("i2","Carotid imaging (Doppler / CTA)"), ("i3","Transthoracic echocardiogram (TTE)"), ("i4","48-h Holter monitor (if indicated)")]):
                    v = st.checkbox(label, value=od(f"{sec}_d1_{k}"), key=f"phys_d1_img{i}", disabled=not can_write("physician")); set_od(f"{sec}_d1_{k}", v)

                sign_off_block(f"{sec}_d1_phys", 1, [f"{sec}_d1_p1", f"{sec}_d1_p2"], "Physician Orders", can_write("physician"))

            with d2:
                banner("Physician & Imaging Orders (Day 2)", "teal", "🩺")
                if is_ivt or is_evt:
                    v = st.checkbox("⭐ Repeat NCCT / MRI Brain at 24h post-treatment — MANDATORY", value=od(f"{sec}_d2_i1"), key="phys_d2_i1", disabled=not can_write("physician")); set_od(f"{sec}_d2_i1", v)
                v = st.checkbox("Continue Day 1 physician orders / Adjust BP meds as needed", value=od(f"{sec}_d2_p1"), key="phys_d2_p1", disabled=not can_write("physician")); set_od(f"{sec}_d2_p1", v)
                sign_off_block(f"{sec}_d2_phys", 2, [f"{sec}_d2_i1"] if (is_ivt or is_evt) else [], "Physician Orders", can_write("physician"))

            with d3:
                banner("Physician Orders (Day 3)", "teal", "🩺")
                v = st.checkbox("Reduce or discontinue IV fluids if tolerating oral intake", value=od(f"{sec}_d3_p1"), key="phys_d3_p1", disabled=not can_write("physician")); set_od(f"{sec}_d3_p1", v)
                if not is_ivt:
                    v = st.checkbox("Anticoagulation planning (if indicated)", value=od(f"{sec}_d3_p2"), key="phys_d3_p2", disabled=not can_write("physician")); set_od(f"{sec}_d3_p2", v)
                
                banner("G — Disposition", "green", "🏠")
                disp_opts = ["Pending", "Acute Rehab", "Home Nursing", "Step-down ward", "Discharge Home"]
                cur_d = od(f"{sec}_d3_disp")
                v = st.radio("Confirm Disposition:", disp_opts, index=disp_opts.index(cur_d) if cur_d in disp_opts else 0, key="phys_d3_disp", disabled=not can_write("physician"))
                set_od(f"{sec}_d3_disp", v)
                sign_off_block(f"{sec}_d3_phys", 3, [f"{sec}_d3_p1"], "Physician Orders", can_write("physician"))

    # ================= TAB 2: NURSING & VITALS =================
    with tab_nurse:
        if route == "Pending" or not cd("routing_done"):
            st.warning("⚠️ Complete Clinical Evaluation to unlock.")
        else:
            st.subheader(f"D — Nursing Checklist — {route}")
            banner("24-Hour Vitals Grid (BP, HR, RR, GCS)", "red", "📊")
            st.session_state.monitor_grid = st.data_editor(st.session_state.monitor_grid, use_container_width=True, num_rows="fixed", key="nurse_grid")
            
            d1, d2, d3 = st.tabs(["Day 1", "Day 2", "Day 3"])
            with d1:
                card("🩺 Supplemental O₂ if SpO₂ < 94% | Target BSR: 140–180 mg/dL (Treat if <60)", "info")
                tasks = [
                    ("n1", "GCS, vitals & SpO₂ monitoring q4h (or per IVT grid)"),
                    ("n2", "Maintain normothermia & Intake/output charting"),
                    ("n3", "Gluco-check before meals and at night"),
                    ("n4", "Aspiration & Fall precautions"),
                    ("n5", "Posture change 2 hourly, Decubitus precautions, air mattress"),
                    ("n6", "Cardiac monitoring & Foley's catheter (if needed)")
                ]
                if is_ivt:
                    tasks += [("n7", "⚠️ NO NEEDLE PRICKS except finger-prick BSR"), ("n8", "Monitor for post-IVT ICH or Angioedema")]
                if is_evt:
                    tasks += [("n9", "🟠 [EVT] Inspect groin site for hematoma, bruising, distal pulses")]
                for k, lbl in tasks:
                    v = st.checkbox(lbl, value=od(f"{sec}_d1_{k}"), key=f"n_d1_{k}", disabled=not can_write("nursing")); set_od(f"{sec}_d1_{k}", v)

            with d2:
                for k, lbl in [("n1", "Continue routine care / Day 1 orders"), ("n2", "Assess for removal of Foley's catheter"), ("n3", "Out of bed / mobilization (as tolerated)")]:
                    v = st.checkbox(lbl, value=od(f"{sec}_d2_{k}"), key=f"n_d2_{k}", disabled=not can_write("nursing")); set_od(f"{sec}_d2_{k}", v)
            
            with d3:
                v = st.checkbox("Continue Day 2 nursing orders", value=od(f"{sec}_d3_n1"), key="n_d3_n1", disabled=not can_write("nursing")); set_od(f"{sec}_d3_n1", v)

    # ================= TAB 3: ALLIED HEALTH, REHAB & EDU =================
    with tab_allied:
        if route == "Pending" or not cd("routing_done"):
            st.warning("⚠️ Complete Clinical Evaluation to unlock.")
        else:
            st.subheader(f"E, F, G — Multidisciplinary, Edu & Rehab")
            sc = cd("nihss_baseline") or 0
            sev, mort, _ = nihss_severity(sc)
            d1, d2, d3 = st.tabs(["Day 1", "Day 2", "Day 3"])
            
            with d1:
                banner("E — Multidisciplinary Care", "teal", "🤝")
                for i, lbl in enumerate(["Swallow assessment by Speech Therapist", "Speech and Language therapy consult", "Physiotherapy consult", "Occupational therapy consult", "Nutritionist Consult (If needed)", "If NG in place, reassess need"]):
                    v = st.checkbox(lbl, value=od(f"{sec}_d1_m{i}"), key=f"a_d1_m{i}", disabled=not can_write("allied")); set_od(f"{sec}_d1_m{i}", v)
                
                banner("F — Family Education", "blue", "👨‍👩‍👧")
                v = st.checkbox("Involve family in management", value=od(f"{sec}_d1_f1"), key="a_d1_f1", disabled=not can_write("physician")); set_od(f"{sec}_d1_f1", v)
                v = st.checkbox(f"Communicate 30-day mortality (NIHSS={sc}: {sev} — {mort})", value=od(f"{sec}_d1_f2"), key="a_d1_f2", disabled=not can_write("physician")); set_od(f"{sec}_d1_f2", v)
                if is_evt:
                    v = st.checkbox("🟠 [EVT] Explain EVT procedure outcome and mTICI grade", value=od(f"{sec}_d1_f3"), key="a_d1_f3", disabled=not can_write("physician")); set_od(f"{sec}_d1_f3", v)

            with d2:
                banner("F — Family Education & Lifestyle", "blue", "👨‍👩‍👧")
                v = st.checkbox("Counsel family regarding prognosis and clinical condition", value=od(f"{sec}_d2_f1"), key="a_d2_f1", disabled=not can_write("physician")); set_od(f"{sec}_d2_f1", v)
                lifestyle_checks(f"{sec}_d2")
                
                banner("G — Rehabilitation & Recovery", "green", "🦽")
                v = st.checkbox("Discharge planning and rehabilitation at 24–48 h", value=od(f"{sec}_d2_r1"), key="a_d2_r1", disabled=not can_write("physician")); set_od(f"{sec}_d2_r1", v)
                v = st.checkbox("Family counselling regarding home care", value=od(f"{sec}_d2_r2"), key="a_d2_r2", disabled=not can_write("physician")); set_od(f"{sec}_d2_r2", v)

            with d3:
                st.info("Continue standard multidisciplinary assessments, adjust lifestyle counseling, and finalize disposition (See Physician Tab).")

    st.markdown("---")
    c_prev, c_next = st.columns(2)
    with c_prev:
        if st.button("⬅️ Back to Phase 3", use_container_width=True): go_to("Phase 3: Imaging & Routing Gate")
    with c_next:
        if st.button("💾 Save Orders & View Notes ➡️", key="btn_s4_out", use_container_width=True):
            go_to("Phase 5: Daily Rounds & Progress Notes")
# ── SCREEN: S8 — SERIAL NIHSS & OUTCOMES ─────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 6: Serial NIHSS & Outcomes":
    page_header("S8: Serial NIHSS, MRS & Clinical Outcomes")

    banner("TOAST Etiological Classification", "blue", "🔬")
    toast_opts = [
        "1) Large-artery atherosclerosis",
        "2) Cardio-embolism",
        "3) Small-vessel occlusion (Lacunar)",
        "4) Stroke of other determined etiology",
        "5) Stroke of undetermined etiology",
    ]
    cur = cd("toast") or toast_opts[4]
    if cur not in toast_opts: cur = toast_opts[4]
    v = st.selectbox("TOAST Classification:", toast_opts, index=toast_opts.index(cur), key="w_toast")
    set_cd("toast", v)

    banner("Serial NIHSS Assessments", "purple", "📊")
    card("Assess NIHSS at each timepoint. Changes ≥ 4 points trigger automatic alerts.", "info")
    nihss_form("2h",  "At 2 Hours Post-Treatment")
    nihss_form("24h", "At 24 Hours Post-Treatment")
    nihss_form("dc",  "At Discharge")

    if cd("nihss_calculated"):
        banner("NIHSS Trend Summary", "blue", "📈")
        b   = cd("nihss_baseline") or 0
        h2  = cd("nihss_2h")  if cd("nihss_2h_done")  else None
        h24 = cd("nihss_24h") if cd("nihss_24h_done") else None
        dc  = cd("nihss_dc")  if cd("nihss_dc_done")  else None

        kpi_html = '<div class="kpi-grid">'
        for val, label in [(b,"Baseline"),(h2,"2 Hours"),(h24,"24 Hours"),(dc,"Discharge")]:
            if val is not None:
                sev, mort, style = nihss_severity(val)
                kpi_html += kpi(str(val), label, style)
        kpi_html += '</div>'
        st.markdown(kpi_html, unsafe_allow_html=True)

        if h24 is not None:
            delta = h24 - b
            if delta >= 4:
                card(f"🚨 <b>NIHSS worsened by {delta} points at 24h</b> — Suspect symptomatic ICH. "
                     f"Repeat NCCT STAT!", "danger")
                log_variance("S8 Outcomes", "24h", "NIHSS worsening ≥ 4 points",
                             f"NIHSS baseline {b} → 24h {h24}. STAT CT ordered.")
            elif delta <= -4:
                card(f"✅ <b>NIHSS improved by {abs(delta)} points at 24h</b> — Document clinical response.", "success")

    banner("Modified Rankin Scale (MRS)", "teal", "🎯")
    c1, c2 = st.columns(2)
    with c1:
        v = st.selectbox("MRS Before Stroke:", MRS_LABELS, index=cd("mrs_pre"), key="w_mrspre")
        set_cd("mrs_pre", MRS_LABELS.index(v))
    with c2:
        v = st.selectbox("MRS At Discharge:", MRS_LABELS, index=cd("mrs_discharge"), key="w_mrsdc")
        set_cd("mrs_discharge", MRS_LABELS.index(v))

    pre_val = cd("mrs_pre")
    dc_val  = cd("mrs_discharge")
    if pre_val != dc_val:
        delta = dc_val - pre_val
        if delta > 0:
            card(f"⚠️ Functional decline: MRS worsened by {delta} point(s). Document rehabilitation plan.", "warning")
        else:
            card(f"✅ Functional improvement: MRS improved by {abs(delta)} point(s).", "success")

    banner("Risk Factors & Secondary Prevention Workup", "grey", "🛡️")
    rf_items = [
        ("rf_prev_stroke","Previous Stroke(s)"),("rf_dm","Diabetes Mellitus"),
        ("rf_htn","Hypertension"),("rf_ihd","Ischemic Heart Disease"),("rf_smoking","Smoking/Tobacco"),
    ]
    c1, c2 = st.columns(2)
    for idx, (k, label) in enumerate(rf_items):
        col = c1 if idx % 2 == 0 else c2
        with col:
            v = st.checkbox(label, value=cd(k), key=f"w_{k}"); set_cd(k, v)

    st.markdown("---")
    if st.button("➡️ Proceed to Progress Notes", key="btn_s8_out"):
        go_to("Phase 5: Daily Rounds & Progress Notes")

# ── SCREEN: S9 — PROGRESS NOTES ──────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 5: Daily Rounds & Progress Notes":
    page_header("S9: Clinical Progress Notes", "Face Sheet & 3-Day Booklet")
    
    # Created tabs to separate the Face Sheet from the Daily Notes
    tab_facesheet, tab_notes = st.tabs(["📋 1. Booklet Face Sheet (Admission)", "📝 2. Daily Progress Notes"])
    
    with tab_facesheet:
        # ⚡ SPEED FIX: Wrapped Face Sheet in a form for fast typing!
        with st.form("facesheet_form", clear_on_submit=False):
            banner("Stroke Daily Progress Notes — Cover Page", "blue", "📄")
            c1, c2, c3 = st.columns(3)
            with c1:
                v = st.text_input("Day of admission:", value=cd("fs_doa",""), key="fs_doa"); set_cd("fs_doa", v)
                v = st.text_input("Day of stroke:", value=cd("fs_dos",""), key="fs_dos"); set_cd("fs_dos", v)
            with c2:
                v = st.text_input("Diagnosis:", value=cd("fs_dx",""), key="fs_dx"); set_cd("fs_dx", v)
                v = st.text_input("Other Diagnoses:", value=cd("fs_odx",""), key="fs_odx"); set_cd("fs_odx", v)
            with c3:
                v = st.text_input("ICH Score (For intracranial bleed):", value=cd("fs_ich",""), key="fs_ich"); set_cd("fs_ich", v)
                v = st.text_input("ABCD2 Score (For TIA):", value=cd("fs_abcd2",""), key="fs_abcd2"); set_cd("fs_abcd2", v)
            
            banner("Risk Factors & Secondary Prevention Workup", "teal", "🛡️")
            
            # Risk factors grid
            r1, r2, r3 = st.columns([1, 1, 1.5])
            with r1:
                st.markdown("**Risk Factor**")
                v1 = st.checkbox("Previous Stroke(s)", value=cd("rf_prev_stroke", False), key="fs_rf1"); set_cd("rf_prev_stroke", v1)
                v2 = st.checkbox("Diabetes Mellitus", value=cd("rf_dm", False), key="fs_rf2"); set_cd("rf_dm", v2)
                v3 = st.checkbox("Hypertension", value=cd("rf_htn", False), key="fs_rf3"); set_cd("rf_htn", v3)
                v4 = st.checkbox("Ischemic Heart Disease", value=cd("rf_ihd", False), key="fs_rf4"); set_cd("rf_ihd", v4)
                v5 = st.checkbox("Smoking / Tobacco", value=cd("rf_smoking", False), key="fs_rf5"); set_cd("rf_smoking", v5)
            with r2:
                st.markdown("**Onset Details**")
                st.markdown("<br>", unsafe_allow_html=True)
                v_dm_o = st.text_input("Onset (DM):", value=cd("fs_dm_o",""), key="fs_dm_o", label_visibility="collapsed"); set_cd("fs_dm_o", v_dm_o)
                v_htn_o = st.text_input("Onset (HTN):", value=cd("fs_htn_o",""), key="fs_htn_o", label_visibility="collapsed"); set_cd("fs_htn_o", v_htn_o)
            with r3:
                st.markdown("**Values**")
                st.markdown("<br>", unsafe_allow_html=True)
                v_hba1c = st.text_input("HbA1c:", value=cd("fs_hba1c",""), key="fs_hba1c", label_visibility="collapsed"); set_cd("fs_hba1c", v_hba1c)
                
            st.markdown("---")
            st.markdown("**Lab & Imaging Details**")
            c_l1, c_l2 = st.columns(2)
            with c_l1:
                v = st.text_input("Lipid Profile (LDL, HDL, TG, Total):", value=cd("fs_lipids",""), key="fs_lipids"); set_cd("fs_lipids", v)
                v = st.text_input("Echocardiography (EF%, Clot, etc):", value=cd("fs_echo",""), key="fs_echo"); set_cd("fs_echo", v)
                v = st.text_input("Carotid Doppler:", value=cd("fs_carotid",""), key="fs_carotid"); set_cd("fs_carotid", v)
            with c_l2:
                v = st.text_input("CTA Carotids/Brain:", value=cd("fs_cta",""), key="fs_cta"); set_cd("fs_cta", v)
                v = st.text_input("Holter Monitoring:", value=cd("fs_holter",""), key="fs_holter"); set_cd("fs_holter", v)
                v = st.text_input("Other work up (e.g., TSH) / Young Stroke:", value=cd("fs_other",""), key="fs_other"); set_cd("fs_other", v)

            # Added a dedicated Save Button for the Face Sheet!
            if st.form_submit_button("💾 Save Face Sheet"):
                st.toast("Face Sheet data saved successfully!", icon="✅")
    with tab_notes:
        card("Progress notes follow the Shifa Stroke Daily Progress Note structure (Days 1–3 per the FM booklet).", "info")

        banner("Smart Progress Note Generator", "purple", "✨")
        if st.button("🤖 Auto-Draft SOAP Note from Clinical Data", key="btn_draft"):
            draft = generate_soap_note()
            st.session_state["_soap_draft"] = draft

        if "_soap_draft" in st.session_state:
            card("⚠️ <b>Auto-draft for physician review — edit before signing.</b>", "warning")
            st.text_area("Draft Note (editable):", value=st.session_state["_soap_draft"],
                         height=300, key="draft_edit")

        st.markdown("---")

        with st.expander("➕ Add New Progress Note", expanded=False):
            # ⚡ SPEED FIX: This is the missing line that makes it lightning fast!
            with st.form("new_progress_note_form", clear_on_submit=True):
                day_num = st.selectbox("Day of Note:", ["1","2","3"], key="pn_day_select")
                c1, c2, c3 = st.columns(3)
                with c1: pn_date    = st.date_input("Date:", value=datetime.date.today(), key="pn_date")
                with c2: pn_time    = st.time_input("Time:", value=(datetime.datetime.utcnow() + datetime.timedelta(hours=5)).time(), key="pn_time")
                with c3: pn_author = st.text_input("Author (Name & ID):", value=cd("resident") or "", key="pn_auth")

                st.subheader(f"Day {day_num} Progress Note")
                banner("Vitals & Clinical Details", "teal", "🩺")
                c1, c2, c3 = st.columns(3)
                with c1:
                    pn_bp   = st.text_input("BP (mmHg):",  key="pn_bp2")
                    pn_hr   = st.text_input("HR (/min):",   key="pn_hr2")
                    pn_rr   = st.text_input("RR (/min):",   key="pn_rr2")
                with c2:
                    pn_temp = st.text_input("TMax:",        key="pn_temp2")
                    pn_spo2 = st.text_input("SpO₂:",        key="pn_spo22")
                    pn_bsr  = st.text_input("BSR (mg/dL):", key="pn_bsr2")
                with c3:
                    pn_gcs_e = st.text_input("GCS E:", key="pn_gcse2")
                    pn_gcs_m = st.text_input("GCS M:", key="pn_gcsm2")
                    pn_gcs_v = st.text_input("GCS V:", key="pn_gcsv2")

                opts_sp = ["Normal", "Mild Dysarthria", "Severe Dysarthria", "Aphasia", "Mute", "Intubated", "Other (See Remarks)"]
                opts_pup = ["Equal & Reactive", "Unequal", "Sluggish", "Fixed/Dilated", "Other (See Remarks)"]
                opts_eom = ["Normal", "Partial Gaze Palsy", "Forced Deviation", "Other (See Remarks)"]
                opts_vis = ["Normal", "Partial Hemianopia", "Complete Hemianopia", "Bilateral Blindness", "Other (See Remarks)"]
                opts_face = ["Symmetric", "Minor Paralysis", "Partial/Complete Paralysis", "Other (See Remarks)"]
                opts_pow = ["5/5 Normal", "4/5 Mild Weak", "3/5 Anti-Gravity", "2/5 Not Anti-Gravity", "1/5 Flicker", "0/5 None", "Other"]
                opts_tone = ["Normal", "Flaccid/Hypotonic", "Spastic/Hypertonic", "Rigidity", "Other"]
                opts_sens = ["Normal", "Right-sided Loss", "Left-sided Loss", "Bilateral Loss", "Other (See Remarks)"]
                opts_cer = ["Absent", "Present Right", "Present Left", "Present Bilateral", "Other (See Remarks)"]
                opts_ref = ["Normal (2+)", "Brisk (3+)", "Depressed (1+)", "Absent (0)", "Other"]
                opts_pla = ["Flexor (Downward)", "Extensor (Upgoing)", "Equivocal", "Mute", "Other"]

                banner("Detailed Examination", "teal", "🔍")
                e1, e2, e3 = st.columns(3)
                with e1:
                    st.markdown("**Cranial Nerves / Head**")
                    pn_speech = st.selectbox("Speech:", opts_sp, key="pn_sp")
                    pn_pupils = st.selectbox("Pupils:", opts_pup, key="pn_pup")
                    pn_eom    = st.selectbox("EOM / Gaze:", opts_eom, key="pn_eom")
                    pn_visual = st.selectbox("Visual Fields:", opts_vis, key="pn_vis")
                    pn_face   = st.selectbox("Face / Tongue:", opts_face, key="pn_fac")
                    pn_bruit  = st.text_input("Carotid Bruit (Text):", key="pn_bruit")
                with e2:
                    st.markdown("**Motor & Tone**")
                    p1, p2 = st.columns(2)
                    with p1:
                        pn_pow_ra = st.selectbox("Right Arm:", opts_pow, key="pn_pow_ra")
                        pn_pow_rl = st.selectbox("Right Leg:", opts_pow, key="pn_pow_rl")
                        pn_tone_r = st.selectbox("Right Tone:", opts_tone, key="pn_tone_r")
                    with p2:
                        pn_pow_la = st.selectbox("Left Arm:", opts_pow, key="pn_pow_la")
                        pn_pow_ll = st.selectbox("Left Leg:", opts_pow, key="pn_pow_ll")
                        pn_tone_l = st.selectbox("Left Tone:", opts_tone, key="pn_tone_l")
                with e3:
                    st.markdown("**Reflexes & Plantars**")
                    r1, r2 = st.columns(2)
                    with r1:
                        pn_ref_r = st.selectbox("Right Reflex:", opts_ref, key="pn_ref_r")
                        pn_pla_r = st.selectbox("Right Plantar:", opts_pla, key="pn_pla_r")
                    with r2:
                        pn_ref_l = st.selectbox("Left Reflex:", opts_ref, key="pn_ref_l")
                        pn_pla_l = st.selectbox("Left Plantar:", opts_pla, key="pn_pla_l")
                    pn_sens  = st.selectbox("Sensations:", opts_sens, key="pn_sens")
                    pn_cereb = st.selectbox("Cerebellar / Ataxia:", opts_cer, key="pn_cer")

                st.markdown("**Systemic & Remarks**")
                sys1, sys2 = st.columns([1, 2])
                with sys1:
                    pn_nihss = st.text_input("Current NIHSS:", key="pn_nih")
                    pn_cvs_resp = st.text_input("CVS/Resp:", key="pn_cvs_resp")
                with sys2:
                    pn_remarks = st.text_area("Remarks / Free Text (Required if 'Other' selected):", height=68, key="pn_remarks")

                banner("Investigations / Labs", "blue", "🧪")
                l1, l2, l3, l4 = st.columns(4)
                with l1:
                    pn_wbc = st.text_input("WBC:", key="pn_wbc")
                    pn_hb  = st.text_input("Hb:", key="pn_hb")
                with l2:
                    pn_plts = st.text_input("Plts:", key="pn_plt")
                    pn_crp  = st.text_input("CRP:", key="pn_crp")
                with l3:
                    pn_lfts = st.text_input("LFTs:", key="pn_lft")
                    pn_pt   = st.text_input("PT/INR:", key="pn_pt")
                with l4:
                    pn_na   = st.text_input("Na / Cr:", key="pn_nacr")
                    pn_cult = st.text_input("Cultures:", key="pn_cult")

                banner("Nursing Monitoring", "teal", "💉")
                c1, c2 = st.columns(2)
                with c1:
                    pn_bedsore = st.text_input("Bed Sore:", key="pn_bs2")
                    pn_bowel   = st.text_input("Bowel Movement:", key="pn_bm2")
                    pn_swallow = st.text_input("Swallowing:", key="pn_sw2")
                    pn_cath    = st.text_input("Urinary Cath:", key="pn_cath2")
                    pn_cell    = st.text_input("Cellulitis:", key="pn_cell")
                with c2:
                    pn_io  = st.text_input("Input/Output:", key="pn_io2")
                    pn_oob = st.text_input("Out of Bed:", key="pn_oob2")
                    pn_asp = st.text_input("Aspiration:", key="pn_asp2")
                    pn_dvt = st.text_input("DVT:", key="pn_dvt2")

                banner("Assessment, Plan & Rehab", "purple", "📋")
                pn_assess = st.text_area("Resident Assessment:", key="pn_assess2", height=80)
                pn_plan   = st.text_area("Plan:", key="pn_plan2", height=80)
                pn_attending = st.text_area("Consultant / Attending Note (Rounds):", key="pn_attending", height=60)

                banner("Rehabilitation", "green", "🦽")
                c_r1, c_r2, c_r3 = st.columns(3)
                with c_r1: pn_pt = st.text_area("Physical Therapy Plan:", key="pn_pt2", height=60)
                with c_r2: pn_st = st.text_area("Speech Therapy Plan:", key="pn_st2", height=60)
                with c_r3: pn_ot = st.text_area("Occupational Therapy Plan:", key="pn_ot2", height=60)
                pn_dc_days = st.text_input("Discharge expected in (days):", key="pn_dcdays2")

                # The button is now a SINGLE form_submit_button!
                if st.form_submit_button("💾 Save Progress Note"):
                    if not pn_author.strip():
                        st.error("Author name is required.")
                    else:
                        note = {
                            "date": str(pn_date), "time": str(pn_time), "author": pn_author, "day": day_num,
                            "vitals": f"BP {pn_bp} | HR {pn_hr} | RR {pn_rr} | TMax {pn_temp} | SpO₂ {pn_spo2} | BSR {pn_bsr}",
                            "gcs": f"E{pn_gcs_e} M{pn_gcs_m} V{pn_gcs_v}",
                            "exam": f"Speech: {pn_speech} | Power(R/L): Arms {pn_pow_ra}/{pn_pow_la}, Legs {pn_pow_rl}/{pn_pow_ll} | Tone(R/L): {pn_tone_r}/{pn_tone_l} | Plantars(R/L): {pn_pla_r}/{pn_pla_l} | Reflexes(R/L): {pn_ref_r}/{pn_ref_l} | Sens: {pn_sens} | Cereb: {pn_cereb} | NIHSS: {pn_nihss}",
                            "systemic": f"CVS/Resp: {pn_cvs_resp} | Remarks: {pn_remarks}",
                            "nursing": f"Bedsore: {pn_bedsore} | Bowel: {pn_bowel} | Swallow: {pn_swallow} | Cath: {pn_cath} | Cellulitis: {pn_cell} | IO: {pn_io} | OOB: {pn_oob} | Aspiration: {pn_asp} | DVT: {pn_dvt}",
                            "assessment": f"Resident: {pn_assess} | Attending: {pn_attending}",
                            "plan": pn_plan,
                            "rehab": f"PT: {pn_pt}\nST: {pn_st}\nOT: {pn_ot}",
                            "dc_days": pn_dc_days, "role": current_role(),
                        }
                        st.session_state.progress_notes.append(note)
                        
                        # Added elegant toast notification
                        st.toast("Progress note saved successfully!", icon="✅")
                        st.rerun()

        st.markdown("---")
        st.subheader(f"📝 Saved Progress Notes ({len(st.session_state.progress_notes)})")
        for i, note in enumerate(reversed(st.session_state.progress_notes)):
            with st.expander(f"Day {note['day']} — {note['date']} {note['time']} | {note['author']}"):
                st.markdown(f"**Vitals:** {note['vitals']}")
                st.markdown(f"**GCS:** {note['gcs']}")
                st.markdown(f"**Exam:** {note['exam']}")
                st.markdown(f"**Systemic:** {note['systemic']}")
                st.markdown(f"**Nursing:** {note['nursing']}")
                st.markdown(f"**Assessment:** {note['assessment']}")
                st.markdown(f"**Plan:** {note['plan']}")
                st.markdown(f"**Rehab:** {note['rehab']}")
                if note.get("dc_days"):
                    st.markdown(f"**Discharge in:** {note['dc_days']} days")
                st.caption(f"Entered by: {note['role']} — {note['author']}")
            
# ── SCREEN: S10 — JCI VARIANCE AUDIT ─────────────────────────────────────
elif st.session_state.ui["screen"] == "Variance Audit":
    page_header("S10: JCI Variance Tracking & Audit Dashboard")

    if not can_write("admin"):
        banner("Read-Only — Only Admin/Audit role can resolve variances.", "grey", "🔒")

    vl = st.session_state.variance_log
    total      = len(vl)
    unresolved = sum(1 for v in vl if not v["resolved"])
    resolved   = total - unresolved

    st.markdown(
        f'<div class="kpi-grid">'
        f'{kpi(str(total), "Total Variances Logged", "primary")}'
        f'{kpi(str(unresolved), "Open / Unresolved", "danger" if unresolved else "success")}'
        f'{kpi(str(resolved), "Resolved", "success")}'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    if not vl:
        card("✅ No variances logged. All mandatory orders completed.", "success")
    else:
        st.subheader("📋 Variance Log")
        for idx, v in enumerate(vl):
            resolved_cls = "variance-resolved" if v["resolved"] else "variance-row"
            status_icon  = "✅" if v["resolved"] else "⚠️"
            st.markdown(
                f'<div class="{resolved_cls}">'
                f'<b>{status_icon} [{v["timestamp"]}]</b> &nbsp;|&nbsp; '
                f'Patient: <b>{v["patient"]}</b> (MRN: {v["mrn"]}) &nbsp;|&nbsp; '
                f'Section: {v["section"]} | Day: {v["day"]} | Item: {v["item"]}<br>'
                f'Reason: {v["reason"]} &nbsp;|&nbsp; Entered by: {v["user"]}'
                f'</div>',
                unsafe_allow_html=True
            )
            if not v["resolved"] and can_write("admin"):
                if st.button("✅ Mark as Resolved", key=f"resolve_{idx}"):
                    st.session_state.variance_log[idx]["resolved"] = True
                    st.rerun()

        st.markdown("---")
        if can_write("admin"):
            if st.button("📥 Export Variance Log (JSON)", key="btn_export"):
                export_str = json.dumps(vl, indent=2, default=str)
                st.download_button(
                    "⬇️ Download JSON",
                    data=export_str,
                    file_name=f"variance_log_{datetime.date.today()}.json",
                    mime="application/json",
                    key="dl_variance"
                )

        st.markdown("---")
        st.subheader("📊 Mandatory Order Completion — Summary")
        mandatory_map = {
            "S5 Section 1 Day 1": ["s1_d1_n9","s1_d1_n10","s1_d1_i1","s1_d1_i2"],
            "S5 Section 1 Day 2": ["s1_d2_i1"],
            "S6 Section 2 Day 1": ["s2_d1_i1","s2_d1_m1"],
            "S7 Section 3 Day 2": ["s3_d2_i1"],
        }
        rows = []
        for label, keys in mandatory_map.items():
            for k in keys:
                done = od(k)
                rows.append({"Order Set": label, "Order Key": k,
                             "Status": "✅ Complete" if done else "❌ Incomplete"})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#9CA3AF;font-size:0.72rem;'>"
    "Shifa International Hospitals Ltd. | Acute Ischemic Stroke EMR | FM-MSA-429 Rev:01 | "
    "AHA/ASA 2026 | JCI Standards | For clinical use only — verify all orders independently"
    "</div>",
    unsafe_allow_html=True
)