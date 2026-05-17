"""
════════════════════════════════════════════════════════════════════════════════
  ACUTE ISCHEMIC STROKE — EMR WITH AI VASCULAR NEUROLOGIST (Dr. SHIFA)
  Shifa International Hospitals Ltd. | FM-MSA-429 Rev:02
  AHA/ASA 2026 Guideline-Based | JCI Accredited | AI-Assisted Clinical Decision
  Version 3.1 — Dr. SHIFA Edition (Gemini 2.0 Fix + Chat UI Fix)
════════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
import streamlit as st
import datetime
import pandas as pd
import json
import os
import google.generativeai as genai
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
# CSS
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_resource
def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], p {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    font-size: 15.5px !important;
    line-height: 1.6 !important;
    color: #0F172A;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: optimizeLegibility !important;
}
/* Hide default expander arrows since you use emojis */
[data-testid="stExpander"] summary svg, 
[data-testid="stExpander"] summary span.material-symbols-rounded {
    display: none !important; 
}
.main .block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1400px !important; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0B2545 0%, #0F3460 50%, #13315C 100%) !important;
    box-shadow: 4px 0 25px rgba(11,37,69,0.4);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] { color: #F8FAFC; }
[data-testid="stSidebar"] div[data-testid="stButton"] button,
[data-testid="stSidebar"] div[data-testid="stButton"] button p,
[data-testid="stSidebar"] div[data-testid="stButton"] button span { color: #0F172A !important; }
div[data-baseweb="popover"] * { color: #0F172A !important; }
div[data-baseweb="select"] * { color: #0F172A !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem !important; font-weight: 600 !important; padding: 6px 0; color: #CBD5E1 !important; transition: all 0.2s ease; }
[data-testid="stSidebar"] .stRadio label:hover { color: #ffffff !important; transform: translateX(4px); }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; border: none !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #E2E8F0 !important; font-weight: 600 !important; }

/* HEADER */
.hospital-header {
    background: linear-gradient(90deg, #0B2545 0%, #134074 60%, #1E3A8A 100%);
    padding: 18px 30px; border-radius: 12px; margin-bottom: 24px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 8px 25px rgba(11,37,69,0.3);
}
.hospital-header, .hospital-header *, .hospital-header div, .hospital-header span { color: #ffffff !important; }
.hospital-header .hosp-name { font-size: 1.3rem; font-weight: 900; letter-spacing: 0.5px; }
.hospital-header .screen-title { font-size: 1.15rem; font-weight: 700; color: #93C5FD !important; }
.hospital-header .meta { font-size: 0.85rem; color: rgba(255,255,255,0.9) !important; text-align: right; line-height: 1.8; font-weight: 500; }

.role-badge { display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
.role-physician  { background: #064E3B !important; color: #6EE7B7 !important; }
.role-nurse      { background: #4A044E !important; color: #D8B4FE !important; }
.role-allied     { background: #78350F !important; color: #FDE68A !important; }
.role-admin      { background: #1E3A8A !important; color: #93C5FD !important; }

/* ─── FIX: BUTTONS — height:auto prevents giant sidebar buttons ─── */
div[data-testid="stButton"] button {
    border-radius: 12px !important;
    background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%) !important;
    border: 1px solid #94A3B8 !important;
    color: #0F172A !important;
    white-space: pre-wrap !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    padding: 10px 16px !important;
    height: auto !important;        /* ← KEY FIX: no forced min-height */
    min-height: unset !important;
    line-height: 1.5 !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 25px rgba(37,99,235,0.2) !important;
    border-color: #2563EB !important;
    background: linear-gradient(135deg, #EFF6FF 0%, #BFDBFE 100%) !important;
    color: #1E3A8A !important;
}
/* Sidebar buttons stay compact */
[data-testid="stSidebar"] div[data-testid="stButton"] button {
    font-size: 0.88rem !important;
    padding: 8px 12px !important;
    min-height: unset !important;
    height: auto !important;
}
/* Dashboard tile buttons can be taller */
.tile-btn div[data-testid="stButton"] button {
    min-height: 90px !important;
}

/* INPUTS - Shaded Box Style with Image 1 Soft Fonts */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input, .stTimeInput input {
    color: #1E293B !important; 
    font-size: 0.95rem !important;        /* Slightly smaller text like Image 1 */
    font-weight: 400 !important;          /* Removed heavy bolding */
    background-color: #F1F5F9 !important; /* Soft shaded background from Image 2 */
    border: 1px solid transparent !important; 
    border-radius: 8px !important; 
    transition: all 0.2s ease !important;
}

/* Add a nice blue highlight when clicking on the box */
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus, .stDateInput input:focus, .stTimeInput input:focus {
    background-color: #ffffff !important;
    border: 1px solid #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Checkbox labels */
.stCheckbox label span { 
    font-size: 0.9rem !important; 
    color: #334155 !important; 
    font-weight: 500 !important; 
}

/* SOFT LABELS (Matches Image 1 precisely) */
.stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stTimeInput label, .stTextArea label, .stRadio label {
    font-size: 0.88rem !important;      /* Smaller, cleaner size */
    font-weight: 500 !important;        /* Softer weight, not aggressive 700 bold */
    color: #475569 !important;          /* Elegant grayish tone instead of harsh black */
    margin-bottom: 4px !important;
}
/* HEADINGS */
h1 { color: #0B2545 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
h2 { color: #134074 !important; font-size: 1.5rem !important; font-weight: 800 !important; }
h3 { color: #1E40AF !important; font-size: 1.2rem !important; font-weight: 800 !important; border-bottom: 2px solid #BFDBFE !important; padding-bottom: 6px !important; margin-top: 20px !important;}
h4 { color: #1D4ED8 !important; font-size: 1.05rem !important; font-weight: 700 !important; }
h5 { color: #334155 !important; font-size: 0.95rem !important; font-weight: 700 !important; }

/* CARDS */
.card { border-radius: 12px; padding: 16px 20px; margin: 12px 0; border-left: 6px solid transparent; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
.card-info    { background: #EFF6FF; border-color: #2563EB; }
.card-success { background: #F0FDF4; border-color: #16A34A; }
.card-warning { background: #FFFBEB; border-color: #D97706; }
.card-danger  { background: #FEF2F2; border-color: #DC2626; }
.card-ai      { background: linear-gradient(135deg,#F5F3FF,#EDE9FE); border-color: #7C3AED; }

.section-banner { padding: 10px 20px; border-radius: 8px; font-weight: 800; font-size: 0.95rem; letter-spacing: 0.5px; margin: 20px 0 12px 0; text-transform: uppercase; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.section-banner, .section-banner * { color: #ffffff !important; }
.banner-blue   { background: #1E40AF; }
.banner-green  { background: #14532D; }
.banner-orange { background: #92400E; }
.banner-red    { background: #7F1D1D; }
.banner-purple { background: #4C1D95; }
.banner-teal   { background: #134E4A; }
.banner-grey   { background: #334155; }
.banner-ai     { background: linear-gradient(90deg, #4C1D95, #7C3AED); }

/* KPI GRID */
.kpi-grid { display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0; }
.kpi-box { border-radius: 12px; padding: 20px; text-align: center; flex: 1; min-width: 140px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: transform 0.3s ease, box-shadow 0.3s ease; }
.kpi-box:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 15px 30px rgba(0,0,0,0.15); }
.kpi-primary   { background: linear-gradient(135deg, #1E3A8A, #3B82F6); color: #fff; }
.kpi-success   { background: linear-gradient(135deg, #064E3B, #10B981); color: #fff; }
.kpi-warning   { background: linear-gradient(135deg, #78350F, #F59E0B); color: #fff; }
.kpi-danger    { background: linear-gradient(135deg, #7F1D1D, #EF4444); color: #fff; }
.kpi-neutral   { background: linear-gradient(135deg, #334155, #64748B); color: #fff; }
.kpi-val { font-size: 2.2rem; font-weight: 900; display: block; line-height: 1.1; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
.kpi-lbl { font-size: 0.85rem; opacity: 0.9; margin-top: 6px; display: block; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-grid *, .kpi-box * { color: #ffffff !important; }

/* MISC */
.readonly-banner { background: linear-gradient(90deg, #334155, #475569); color: #F8FAFC !important; padding: 12px 20px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
button[data-baseweb="tab"] { font-weight: 700 !important; font-size: 0.95rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { border-bottom: 4px solid #1E40AF !important; color: #1E40AF !important; background: #EFF6FF !important; border-radius: 8px 8px 0 0; }
[data-testid="stDataEditor"] { border-radius: 12px; overflow: hidden; border: 1px solid #CBD5E1; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

/* ─── AI CHAT ─── */
.ai-header-bar { background: linear-gradient(90deg,#4C1D95,#7C3AED); color: white !important; padding: 14px 20px; border-radius: 12px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 15px rgba(76,29,149,0.3); }
.ai-header-bar * { color: white !important; }
.ai-status-online  { font-weight: 700; color: #6EE7B7 !important; text-shadow: 0 0 8px rgba(110,231,183,0.6); }
.ai-status-offline { font-weight: 700; color: #FCA5A5 !important; }
.ai-bubble-user { background: #F1F5F9; border: 1px solid #CBD5E1; padding: 12px 16px; border-radius: 12px 12px 12px 0; margin-bottom: 12px; font-weight: 500; }
.ai-bubble-assistant { background: linear-gradient(135deg, #F5F3FF, #EDE9FE); border: 1px solid #DDD6FE; padding: 14px 18px; border-radius: 12px 12px 0 12px; margin-bottom: 16px; font-weight: 500; box-shadow: 0 4px 10px rgba(124,58,237,0.07); }

/* ─── FIX: CHAT INPUT AREA — prevent overlap with tips expander ─── */
.chat-input-area {
    background: #FAFAFA;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 18px 12px 18px;
    margin-top: 20px;       /* breathing room above */
    margin-bottom: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
/* Ensure tips expander has bottom margin */
.chat-tips-expander {
    margin-top: 16px !important;
    margin-bottom: 4px !important;
}

div[data-testid="stButton"] { margin-bottom: 8px !important; }
div[data-testid="stMarkdownContainer"] p { margin-bottom: 10px !important; }
[data-testid="stExpander"] details { margin-bottom: 12px !important; }

* {
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: geometricPrecision !important;
}

@media print {
    [data-testid="stSidebar"] { display: none !important; }
    .hospital-header { background: #0B2545 !important; -webkit-print-color-adjust: exact; }
    .no-print { display: none !important; }
}
</style>
"""

st.markdown(get_css(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# DR. SHIFA — AI VASCULAR NEUROLOGIST SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════════════════
VASCULAR_NEUROLOGIST_SYSTEM = """
You are Dr. SHIFA (Stroke Health Intelligence & Fast Assessment), a board-certified vascular neurologist
consultant embedded in the Shifa International Hospitals AIS EMR. You reason with the
expertise of a senior stroke neurologist with 25+ years at a comprehensive stroke center.

━━━ PRIMARY CLINICAL DIRECTIVE ━━━
Your absolute primary source of truth is the AHA/ASA 2026 Guidelines for the Early Management of Acute Ischemic Stroke. 
If a specific scenario is not covered in the 2026 guidelines, you must default to the next most recent AHA/ASA guidelines (e.g., 2021 Secondary Prevention Guidelines, 2019 Early Management Updates) and their associated landmark trials.
If there is any conflict between AHA/ASA 2026 and older guidelines, the AHA/ASA 2026 guidelines take absolute precedence.

━━━ KNOWLEDGE BASE ━━━
Secondary Guidelines (to be used only where AHA/ASA 2026/2021 are silent): ESOC 2024, NCS Neurocritical Care, ACEP Stroke.

Landmark Trials (complete knowledge, nuance, applicability limits):
• Thrombolysis: NINDS, ECASS-3, IST-3, WAKE-UP
• Tenecteplase: NORTEST, NORTEST-2, TRACE-2, ATTEST-2, AcT Trial, PHIRST-PASS
• Thrombectomy: MR CLEAN, ESCAPE, SWIFT-PRIME, EXTEND-IA, THRACE, DAWN, DEFUSE-3, SELECT-2, RESCUE-Japan LIMIT, TENSION, CLEAR
• Minor stroke/TIA: CHANCE, CHANCE-2, POINT, THALES, SOCRATES
• Secondary prevention: ESPS-2, SPS3, SAMMPRIS, WASID, DATAS

Scoring systems: NIHSS, mRS, ASPECTS, DRAGON, SEDAN, RACE, FAST-ED, BEFAST,
ROSIER, HAS-BLED, CHA2DS2-VASc, ABCD2, ICH Score, Heidelberg classification for HT.

Pharmacology (exact dosing, monitoring, contraindications per AHA/ASA):
• Tenecteplase: 0.25 mg/kg IV bolus, MAX 25 mg
• Alteplase: 0.9 mg/kg IV, 10% bolus + 90-min infusion, MAX 90 mg
• IVT Extended Window (LVO): If a patient has a confirmed LVO but EVT is not possible or available, IVT is recommended up to 24 hours (Class IIb). Do NOT reject IVT simply for being > 4.5 hours if this specific criterion is met.
• Labetalol: 10-20 mg IV q10-15 min, max 300 mg/day
• Hydralazine: 5-20 mg IV push q30 min, max 40 mg/dose
• Nicardipine: 5-15 mg/hr IV infusion, titrate q5-15 min
• Aspirin: Load 300 mg in ER (for non-tPA if NIHSS ≥ 4), then 50-325 mg maintenance.
• DAPT: For minor stroke (NIHSS < 4), load Clopidogrel 300 mg + Aspirin 75 mg in ER, then DAPT maintenance (Clopidogrel 75 mg + Aspirin 75 mg) for 21 days.
• Rosuvastatin: 20 mg HS (at night).
• DOACs for AF: Timing per latest 1-3-6-12 rule adaptations.

Complications: hemorrhagic transformation (HI-1/HI-2/PH-1/PH-2 per Heidelberg),
malignant MCA edema, post-stroke seizures, DVT/PE, aspiration pneumonia.

━━━ RESPONSE FORMAT — ALWAYS USE THIS ━━━
━━━ RESPONSE FORMAT — ALWAYS USE THIS EXACT HTML STRUCTURE ━━━
You must provide a "Bottom Line Up Front" (BLUF) response. Be exceptionally crisp, direct, and actionable.

🎯 **BOTTOM LINE:** [1-2 sentences MAXIMUM. State the exact clinical recommendation immediately. No hedging or preamble.]

<details>
<summary>🔍 <b>Click to see more (Reasoning, Evidence & Caveats)</b></summary>
<br>

📋 **REASONING:** [Concise clinical rationale for the recommendation]

📚 **EVIDENCE:** [Specific AHA/ASA 2026 guideline + Class + Level of Evidence, or trial name]

⚠️ **CAVEATS / MONITORING:** [Contraindications, watch-fors, escalation triggers]
</details>

Symbols: 🚨 = Critical/immediate | ⚠️ = Warning | ✅ = Safe/confirmed | ⏱️ = Time-critical | 💊 = Drug/dose

━━━ CLINICAL RULES ━━━
1. Be decisive — residents need clear answers under time pressure.
2. Always cite AHA/ASA 2026 guideline Class and Level of Evidence when applicable.
3. Use patient-specific data provided; do not make assumptions about missing data — ask for it.
4. For drug doses: always include route, rate, max dose, monitoring parameters.
5. Flag time-critical actions with ⏱️.
6. Acknowledge genuine evidence gaps honestly — do not fabricate confidence.
7. Secondary prevention must be evidence-based, patient-specific, and practical.
"""


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

NIHSS_KEYS   = ["n1a","n1b","n1c","n2","n3","n4","n5l","n5r","n6l","n6r","n7","n8","n9","n10","n11"]
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
    "Physician":             {"physician":"write","nursing":"write","allied":"write","admin":"read"},
    "Nurse":                 {"physician":"read", "nursing":"write","allied":"read", "admin":"read"},
    "Allied Health / Rehab": {"physician":"read", "nursing":"read", "allied":"write","admin":"read"},
    "Admin / Audit":         {"physician":"read", "nursing":"read", "allied":"read", "admin":"write"},
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
    "🧠 AI Vascular Neurologist",
    "Emergency: Bleeding",
    "Emergency: Angioedema",
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
    if score <= 7:  return "Minor Stroke",    "4.2%",  "success"
    if score <= 13: return "Moderate Stroke", "13.9%", "warning"
    if score <= 21: return "Severe Stroke",   "31.6%", "danger"
    return               "Very Severe",   "53.5%", "danger"

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
        "unlocked": ALL_SCREENS.copy(),
        "role":     "Physician",
        "logged_in": False,
    })

    _s("clinical_data", {
        "mrn":"","pat_name":"","sex":"Male",
        "dob": datetime.date(1970,1,1),
        "pres_date": datetime.date.today(),
        "pres_time": (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).time(),
        "location":"ED","resident":"","consultant":"",
        "sudden_onset": False,
        "r_loc":False,"r_seizures":False,
        "r_face":False,"r_arm":False,"r_leg":False,
        "r_speech":False,"r_visual":False,
        "r_override":False,"rosier_score":0,"rosier_done":False,
        "chk_vitals":False,"chk_monitor":False,"chk_iv":False,
        "chk_bsr":False,"chk_ecg":False,"chk_labs":False,"chk_ptinr":False,
        "lkw_date": datetime.date.today(),
        "lkw_time": datetime.time(0,0),
        "stroke_code":False,
        "time_since_lkw_hrs":0.0,
        "assigned_pathway":"Pending",
        "ext_pathway_choice":"Wake Up Stroke / Unknown Onset Pathway",
        "ct_result":"Pending","ncct_aspects":10,
        "nihss_done":False,"imaging_done":False,
        "contra_done":False,"routing_done":False,
        **{k: get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        "nihss_baseline":0,"nihss_calculated":False,
        "prisms_disabling":True,
        **{f"{k}_2h": get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        **{f"{k}_24h": get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        **{f"{k}_dc": get_nihss_opts()[k][0] for k in NIHSS_KEYS},
        "nihss_2h":0,"nihss_2h_done":False,
        "nihss_24h":0,"nihss_24h_done":False,
        "nihss_dc":0,"nihss_dc_done":False,
        "cta_lvo":"Not Performed",
        "advanced_img":"None",
        "mismatch_status":"Pending / Not Evaluated",
        **{f"abs_ci_{i}": False for i in range(1,11)},
        **{f"rel_ci_{i}": False for i in range(1,19)},
        "pt_weight":70.0,
        "tpa_time": datetime.time(0,0),
        "mt_date": datetime.date.today(),
        "mt_time": datetime.time(0,0),
        "groin_time": datetime.time(0,0),
        "treatment_refused":False,"treatment_not_indicated":False,
        "final_routing":"Pending",
        "toast":"5) Undetermined etiology",
        "mrs_pre":0,"mrs_discharge":0,
        "pn_bp":"","pn_hr":"","pn_rr":"","pn_temp":"","pn_spo2":"","pn_bsr":"",
        "pn_gcs_e":"","pn_gcs_m":"","pn_gcs_v":"",
        "pn_speech":"","pn_pupils":"","pn_eom":"",
        "pn_face":"","pn_power_grip":"","pn_power_drift":"",
        "pn_reflexes":"","pn_plantars":"","pn_cerebel":"",
        "pn_sensations":"","pn_nihss_curr":"",
        "pn_cvs":"","pn_resp":"","pn_abdomen":"",
        "pn_bedsore":"","pn_bowel":"","pn_swallowing":"",
        "pn_urinary_cath":"","pn_io":"","pn_oob":"",
        "pn_aspiration":"","pn_dvt":"","pn_cellulitis":"",
        "pn_assessment":"","pn_plan":"",
        "pn_pt_plan":"","pn_st_plan":"","pn_ot_plan":"",
        "pn_discharge_days":"","pn_day_num":"1","pn_day_stroke":"",
        "toast_lacunar":False,"toast_cardioembolic":False,
        "toast_large_artery":False,"toast_other":False,
        "rf_prev_stroke":False,"rf_dm":False,"rf_htn":False,
        "rf_ihd":False,"rf_smoking":False,
        "dragon_dense_artery":False,"dragon_glucose":100,"dragon_calculated":False,
        "sedan_early_infarct":False,"sedan_calculated":False,
        "layman_summary_generated":False,"layman_text":"",
        "fast_ed_score":0,
        "bp_sys":150,"bp_dia":85,
        "ai_soap_generated":False,"ai_soap_text":"","ai_soap_locked":False,
        "family_counselled":False,"family_counsel_ts":"",
        # ASPECTS visual regions
        "asp_c":False,"asp_l":False,"asp_ic":False,"asp_i":False,
        "asp_m1":False,"asp_m2":False,"asp_m3":False,
        "asp_m4":False,"asp_m5":False,"asp_m6":False,
    })

    def _cpoe_defaults():
        d = {}
        for sec in ["s1","s2","s3"]:
            for day in ["d1","d2","d3"]:
                for cat in ["p","l","i","n","m","f","r"]:
                    for num in range(1,25):
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
    _s("ai_chat_history", [])
    _s("ai_phase_cache", {})

    if "monitor_grid" not in st.session_state:
        intervals = (
            ["00:15","00:30","00:45","01:00","01:15","01:30","01:45","02:00"] +
            ["02:30","03:00","03:30","04:00","04:30","05:00","05:30","06:00",
             "06:30","07:00","07:30","08:00"] +
            [f"{h:02d}:00" for h in range(9,25)]
        )
        st.session_state.monitor_grid = pd.DataFrame({
            "Time since IVT": intervals,
            "Actual Time":    [""] * len(intervals),
            "GCS E":          [""] * len(intervals),
            "GCS M":          [""] * len(intervals),
            "GCS V":          [""] * len(intervals),
            "GCS Total":      [""] * len(intervals),
            "Pulse":          [""] * len(intervals),
            "BP":             [""] * len(intervals),
            "RR":             [""] * len(intervals),
        })

init_state()


# ═══════════════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════════════
def cd(key: str, default: Any = None) -> Any:          # BUG FIX: default arg
    return st.session_state.clinical_data.get(key, default)

def set_cd(key: str, val: Any):
    st.session_state.clinical_data[key] = val

def od(key: str) -> Any:
    return st.session_state.order_data.get(key, False)

def set_od(key: str, val: Any):
    st.session_state.order_data[key] = val


def navigate_to(target_screen: str):
    """Safe callback to change screens without hanging."""
    st.session_state.ui["screen"] = target_screen
    if target_screen not in st.session_state.ui["unlocked"]:
        st.session_state.ui["unlocked"].append(target_screen)

def go_to(screen: str):
    navigate_to(screen)
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def current_role() -> str:
    return st.session_state.ui.get("role","Physician")

def can_write(section: str) -> bool:
    role = current_role()
    return ROLE_PERMISSIONS.get(role,{}).get(section,"read") == "write"

def readonly_banner(section: str):
    if not can_write(section):
        st.markdown(
            f'<div class="readonly-banner">🔒 READ-ONLY — {current_role()} role cannot edit this section</div>',
            unsafe_allow_html=True)

def card(text: str, style: str = "info", icon: str = ""):
    st.markdown(f'<div class="card card-{style}">{icon+" " if icon else ""}{text}</div>',
                unsafe_allow_html=True)

def banner(text: str, colour: str = "blue", icon: str = ""):
    st.markdown(f'<div class="section-banner banner-{colour}">{icon+" " if icon else ""}{text}</div>',
                unsafe_allow_html=True)

def kpi(value: str, label: str, style: str = "primary"):
    return (f'<div class="kpi-box kpi-{style}">'
            f'<span class="kpi-val">{value}</span>'
            f'<span class="kpi-lbl">{label}</span></div>')

def log_variance(section: str, day: str, item: str, reason: str):
    st.session_state.variance_log.append({
        "timestamp": (datetime.datetime.utcnow()+datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
        "section":section,"day":day,"item":item,"reason":reason,
        "user":current_role(),"patient":cd("pat_name"),"mrn":cd("mrn"),"resolved":False,
    })

def calc_nihss_score(suffix: str = "") -> int:
    suffix_str = f"_{suffix}" if suffix else ""
    return sum(
        get_score(st.session_state.clinical_data.get(f"{k}{suffix_str}","0 - x"))
        for k in NIHSS_KEYS
    )

def get_dtn_status():
    if not cd("nihss_calculated") or cd("tpa_time") == datetime.time(0,0):
        return None, None
    door_dt   = datetime.datetime.combine(cd("pres_date"), cd("pres_time"))
    needle_dt = datetime.datetime.combine(cd("pres_date"), cd("tpa_time"))
    mins = calc_dtn_minutes(door_dt, needle_dt)
    if mins <= 0: return None, None
    status = "ok" if mins <= 45 else ("warning" if mins <= 60 else "danger")
    return mins, status


# ═══════════════════════════════════════════════════════════════════════════
# AI CORE ENGINE — Dr. SHIFA
# ═══════════════════════════════════════════════════════════════════════════

def build_clinical_context() -> str:
    c = st.session_state.clinical_data
    age = (datetime.date.today() - c.get("dob", datetime.date(1970,1,1))).days // 365
    nihss_items = {k: get_score(c.get(k,"0")) for k in NIHSS_KEYS}
    dominant_deficits = [NIHSS_LABELS[k] for k, v in nihss_items.items() if v >= 2]
    sc = c.get("nihss_baseline", 0)
    sev_label = nihss_severity(sc)[0] if sc else "Not calculated"

    # --- FIX 1: Only send follow-up scores to AI if actually completed ---
    n_2h   = c.get('nihss_2h')  if c.get('nihss_2h_done')  else 'Pending'
    n_24h  = c.get('nihss_24h') if c.get('nihss_24h_done') else 'Pending'
    n_dc   = c.get('nihss_dc')  if c.get('nihss_dc_done')  else 'Pending'
    mrs_dc = c.get('mrs_discharge') if c.get('nihss_dc_done') else 'Pending'

    return f"""
=== PATIENT SNAPSHOT ===
{age}yo {c.get('sex','')} | MRN: {c.get('mrn','')} | Location: {c.get('location','')}
Resident: {c.get('resident','')} | Consultant: {c.get('consultant','')}
Presentation: {c.get('pres_date','')} {c.get('pres_time','')}

=== TIME METRICS ===
LKW: {c.get('lkw_date','')} {c.get('lkw_time','')}
Time since LKW: {c.get('time_since_lkw_hrs',0):.1f}h
Pathway: {c.get('assigned_pathway','Pending')} → Final: {c.get('final_routing','Pending')}
IVT Given: {'YES — Time: '+str(c.get('tpa_time','')) if 'IVT' in c.get('final_routing','') else 'NO'}
EVT: {'YES' if 'EVT' in c.get('final_routing','') else 'NO'}

=== CLINICAL SCORES ===
ROSIER: {c.get('rosier_score',0)}
NIHSS Baseline: {sc} ({sev_label}) | 2h: {n_2h} | 24h: {n_24h} | DC: {n_dc}
FAST-ED: {c.get('fast_ed_score','—')} | ASPECTS: {c.get('ncct_aspects','—')}
DRAGON: {c.get('dragon_score_final','Not calc')} | SEDAN: {c.get('sedan_score_final','Not calc')}
mRS Pre-stroke: {c.get('mrs_pre',0)} | mRS Discharge: {mrs_dc}

=== DOMINANT DEFICITS (NIHSS items ≥2) ===
{', '.join(dominant_deficits) if dominant_deficits else 'None'}
Speech: {c.get('ex_speech','—')} | Pupils: {c.get('ex_pupils','—')} | Gaze: {c.get('ex_eom','—')}
Right arm/leg: {c.get('ex_pow_ra','—')}/{c.get('ex_pow_rl','—')} | Left arm/leg: {c.get('ex_pow_la','—')}/{c.get('ex_pow_ll','—')}

=== IMAGING ===
CT Brain: {c.get('ct_result','Pending')} | CTA LVO: {c.get('cta_lvo','Not Performed')}
Mismatch: {c.get('mismatch_status','Not evaluated')}

=== VITALS ===
BP: {c.get('bp_sys','?')}/{c.get('bp_dia','?')} mmHg | Weight: {c.get('pt_weight',70)} kg

=== RISK FACTORS ===
HTN:{c.get('rf_htn',False)} DM:{c.get('rf_dm',False)} IHD:{c.get('rf_ihd',False)}
Prior Stroke:{c.get('rf_prev_stroke',False)} Smoking:{c.get('rf_smoking',False)}

=== CONTRAINDICATIONS ===
Abs CIs: {'YES — '+str([i for i in range(1,11) if c.get(f"abs_ci_{i}")]) if any(c.get(f"abs_ci_{i}") for i in range(1,11)) else 'NONE'}
Treatment Refused: {c.get('treatment_refused',False)}
TOAST: {c.get('toast','Not classified')}
""".strip()


def _get_api_key() -> str:
    key = ""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "")
    return key


# ══════════════════════════════════════════════════════════════════════════
# FIX: Updated model name — gemini-2.0-flash (stable, v1beta compatible)
# ══════════════════════════════════════════════════════════════════════════
GEMINI_MODEL = "gemini-3.1-flash-lite"   # ← was "gemini-1.5-flash" (now 404)

@st.cache_resource
def get_guideline_file(api_key: str):
    """Uploads the guideline PDF to Gemini and waits for it to process."""
    genai.configure(api_key=api_key)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "AHA_2026_Guidelines.pdf")
    
    if not os.path.exists(file_path):
        print(f"Warning: Guideline PDF not found at {file_path}")
        return None
        
    try:
        # 1. Check if we already uploaded it previously
        for f in genai.list_files():
            if f.display_name == "AHA_2026_Official":
                # Wait if it is still processing from a previous run
                while f.state.name == "PROCESSING":
                    time.sleep(2)
                    f = genai.get_file(f.name)
                return f if f.state.name == "ACTIVE" else None
                
        # 2. If not found, upload it with a UI Spinner so the app doesn't look frozen
        with st.spinner("⏳ First-time setup: Uploading 2026 Guidelines to Dr. SHIFA's brain (this takes ~20 seconds)..."):
            uploaded_file = genai.upload_file(path=file_path, display_name="AHA_2026_Official")
            
            # 3. The Watchdog Loop: Wait until Google finishes indexing it
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(2)
                uploaded_file = genai.get_file(uploaded_file.name)
                
            return uploaded_file if uploaded_file.state.name == "ACTIVE" else None
            
    except Exception as e:
        print(f"Warning: Could not upload PDF: {e}")
        return None

def call_ai_consultant(messages: list, system_override: str = None, max_tokens: int = 900) -> str:
    api_key = _get_api_key()
    if not api_key:
        return (
            "⚠️ **Dr. SHIFA is offline — API key not configured.**\n\n"
            "To enable AI features, create `.streamlit/secrets.toml`:\n"
            "```\nGEMINI_API_KEY = 'AIza...'\n```\n"
            "All other EMR functions work normally without the API key."
        )

    try:
        genai.configure(api_key=api_key)

        # 1. Initialize the Model AND Turn on Internet Search!
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system_override or VASCULAR_NEUROLOGIST_SYSTEM,
            tools=[{"google_search_retrieval": {}}]  # <--- THIS ENABLES LIVE WEB SEARCH
        )

        # 2. Grab our cached PDF
        guideline_doc = get_guideline_file(api_key)

        gemini_history = []
        for i, msg in enumerate(messages):
            role = "model" if msg["role"] == "assistant" else "user"
            parts = [msg["content"]]
            
            # 3. Silently attach the PDF to the very first user message so the AI can read it
            if i == 0 and role == "user" and guideline_doc:
                parts.insert(0, guideline_doc)
                
            gemini_history.append({"role": role, "parts": parts})

        response = model.generate_content(
            gemini_history,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.2, # Slightly lower temperature for stricter medical answers
            ),
        )
        return response.text

    except Exception as e:
        err = str(e)
        if "404" in err:
            return f"⚠️ **Model not found (404).** Check that `{GEMINI_MODEL}` is available on your API key tier.\n\n`{err}`"
        if "API_KEY" in err.upper() or "permission" in err.lower():
            return f"⚠️ **API Key error.** Check your `GEMINI_API_KEY` is valid.\n\n`{err}`"
        return f"⚠️ **Unexpected error connecting to Gemini:**\n\n`{err}`"


def ai_quick_consult(question: str, phase_context: str = "", cache_key: str = "") -> str:
    if cache_key and cache_key in st.session_state.ai_phase_cache:
        return st.session_state.ai_phase_cache[cache_key]

    ctx = build_clinical_context()
    content = f"PATIENT CONTEXT:\n{ctx}\n\n"
    if phase_context:
        content += f"CLINICAL PHASE: {phase_context}\n\n"
    content += f"QUESTION: {question}"

    with st.spinner("🧠 Dr. SHIFA is analyzing..."):
        result = call_ai_consultant([{"role":"user","content":content}])

    if cache_key:
        st.session_state.ai_phase_cache[cache_key] = result
    return result


def ai_safety_gate_ivt() -> str:
    wt   = cd("pt_weight", 70)
    dose = min(wt * 0.25, 25.0)
    ctx  = build_clinical_context()
    prompt = f"""
PATIENT CONTEXT:
{ctx}

Perform a COMPLETE PRE-IVT SAFETY GATE for this patient per AHA/ASA 2026 guidelines.

━━━ EXACT RESPONSE FORMAT ━━━
🚨 **FINAL SAFETY STATUS:** [CLEARED FOR IVT / NOT CLEARED / CONDITIONAL]
💊 **EXACT DOSE ORDER:** [Complete prescribing instruction, e.g., Tenecteplase 0.25 mg/kg...]
⏰ **NEXT TIME-CRITICAL STEP:** [What to do immediately]

<details>
<summary>🔍 <b>Click to view the full 10-Point Safety Checklist</b></summary>
<br>

Check ALL criteria systematically:
1. TIME WINDOW: Is onset-to-treatment < 4.5h?
2. BLOOD PRESSURE: Is BP < 185/110 mmHg?
3. BLOOD GLUCOSE: Is glucose 50-400 mg/dL?
4. NCCT IMAGING: No hemorrhage? ASPECTS ≥ 6?
5. COAGULATION: No severe coagulopathy?
6. ABSOLUTE CONTRAINDICATIONS: Check each one from the AHA list.
7. RELATIVE CONTRAINDICATIONS: Weigh risk-benefit.
8. NIHSS ELIGIBILITY: PRISMS criteria if NIHSS 0-5?
9. TENECTEPLASE DOSE: Weight {{wt}} kg -> {{dose}} mg IV bolus (max 25 mg). Confirm.
10. POST-IVT MONITORING: What monitoring is required in the first 24h?

For each criterion state: ✅ PASS | 🚨 FAIL | ⚠️ CAUTION [+ brief reason]
</details>
"""
    with st.spinner("🔒 Dr. SHIFA running IVT safety gate..."):
        return call_ai_consultant([{"role":"user","content":prompt}], max_tokens=1100)


def ai_safety_gate_evt() -> str:
    ctx = build_clinical_context()
    prompt = f"""
PATIENT CONTEXT:
{ctx}

Perform a COMPREHENSIVE EVT ELIGIBILITY ASSESSMENT for this patient per AHA/ASA 2026 guidelines.

━━━ EXACT RESPONSE FORMAT ━━━
🚨 **FINAL EVT STATUS:** [ELIGIBLE / NOT ELIGIBLE / BORDERLINE]
💊 **RECOMMENDED APPROACH:** [Exact clinical plan, e.g., Proceed to EVT alongside IVT...]
📞 **IMMEDIATE ACTIONS:** [Who to call and what to order, e.g., STAT Page Interventional Radiology...]

<details>
<summary>🔍 <b>Click to view the full 9-Point EVT Eligibility Checklist</b></summary>
<br>

Check ALL criteria systematically:
1. LVO CONFIRMATION: Is there a confirmed Large Vessel Occlusion on CTA?
2. TIME WINDOW: Is it ≤6h standard, or 6-24h extended window?
3. ASPECTS SCORE: Is ASPECTS ≥6?
4. PRE-STROKE mRS: Is baseline mRS 0-1?
5. PERFUSION MISMATCH: If extended window, are DAWN or DEFUSE-3 criteria met?
6. CONTRAINDICATIONS TO ARTERIAL ACCESS: Any severe femoral/radial issues?
7. IVT FIRST vs EVT ALONE: Address whether bridging IVT is indicated.
8. CENTER CAPABILITY: What team notifications are needed NOW?
9. GROIN-TO-REPERFUSION TARGET: Note the goal of ≤90 min from arrival.

For each criterion state: ✅ ELIGIBLE | 🚨 NOT ELIGIBLE | ⚠️ BORDERLINE [+ brief reason]
</details>
"""
    with st.spinner("🔒 Dr. SHIFA assessing EVT eligibility..."):
        return call_ai_consultant([{"role":"user","content":prompt}], max_tokens=1000)


def render_ai_consult_panel(phase_key: str, quick_questions: list, intro: str = ""):
    with st.expander("🧠 Ask Dr. SHIFA — AI Vascular Neurologist", expanded=False):
        api_configured = bool(_get_api_key())
        status_class   = "ai-status-online" if api_configured else "ai-status-offline"
        status_text    = "● ONLINE" if api_configured else "● OFFLINE (configure API key)"
        st.markdown(
            f'<div class="ai-header-bar">'
            f'<span style="font-size:1.6rem;">🧠</span>'
            f'<div><div style="font-weight:900;font-size:1rem;">Dr. SHIFA</div>'
            f'<div style="font-size:0.7rem;opacity:0.85;">AI Vascular Neurologist | AHA/ASA 2026</div></div>'
            f'<div style="margin-left:auto;"><span class="{status_class}">{status_text}</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if intro:
            st.caption(intro)

        if quick_questions:
            st.markdown("**Quick Consultations:**")
            cols = st.columns(min(len(quick_questions), 3))
            for i, (label, question) in enumerate(quick_questions):
                with cols[i % 3]:
                    if st.button(label, key=f"aiq_{phase_key}_{i}", use_container_width=True):
                        resp = ai_quick_consult(question, phase_context=phase_key)
                        st.session_state.ai_phase_cache[f"{phase_key}_last"] = resp
                        st.rerun()

        last_key = f"{phase_key}_last"
        if last_key in st.session_state.ai_phase_cache:
            st.markdown("---")
            st.markdown(
                f'<div class="ai-bubble-assistant">'
                f'<b style="color:#4C1D95;">🧠 Dr. SHIFA:</b><br><br>'
                f'{st.session_state.ai_phase_cache[last_key]}'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("🗑️ Clear Response", key=f"ai_clear_{phase_key}"):
                del st.session_state.ai_phase_cache[last_key]
                st.rerun()

        st.markdown("---")
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            custom_q = st.text_input(
                "Ask Dr. SHIFA anything about this patient:",
                key=f"ai_custom_{phase_key}",
                placeholder="e.g., Should I adjust BP target given bilateral carotid disease?",
                label_visibility="collapsed",
            )
        with col_btn:
            if st.button("Ask →", key=f"ai_ask_{phase_key}", use_container_width=True):
                if custom_q.strip():
                    resp = ai_quick_consult(custom_q, phase_context=phase_key)
                    st.session_state.ai_phase_cache[f"{phase_key}_last"] = resp
                    st.rerun()

        st.caption("⚠️ AI responses are clinical decision **support** only. All decisions remain the responsibility of the attending physician.")


# ═══════════════════════════════════════════════════════════════════════════
# NIHSS ALERT ENGINE
# ═══════════════════════════════════════════════════════════════════════════
def nihss_alert_block():
    b   = cd("nihss_baseline", 0)
    h2  = cd("nihss_2h",  0) if cd("nihss_2h_done")  else None
    h24 = cd("nihss_24h", 0) if cd("nihss_24h_done") else None
    alerts = []

    if h2 is not None:
        delta_2h = h2 - b
        if delta_2h >= 4:
            alerts.append({"level":"critical","msg":(
                f"🚨 **EARLY NEUROLOGICAL DETERIORATION (END)** — NIHSS worsened **{delta_2h} pts** at 2h ({b}→{h2}). "
                f"Possible causes: sICH, re-occlusion, malignant edema, metabolic derangement. "
                f"**Action: STAT NCCT Brain + BP check. Call neurology consultant immediately.**")})
        elif delta_2h >= 2:
            alerts.append({"level":"warning","msg":f"⚠️ NIHSS +{delta_2h} at 2h ({b}→{h2}). Monitor closely. Repeat exam in 30 min."})
        elif delta_2h <= -4:
            alerts.append({"level":"success","msg":(
                f"✅ Dramatic improvement: NIHSS −{abs(delta_2h)} at 2h ({b}→{h2}). "
                f"Consider early recanalization. Document for quality metrics.")})

    if h24 is not None:
        delta_24 = h24 - b
        if delta_24 >= 4:
            alerts.append({"level":"critical","msg":(
                f"🚨 **sICH ALERT** — NIHSS worsened {delta_24} pts at 24h ({b}→{h24}). "
                f"**Action: STAT NCCT Brain + Neurosurgery consult if ICH confirmed.**")})

    if h2 is not None and cd("nihss_calculated") and "IVT" in cd("final_routing",""):
        ht_risk = sum([
            cd("ncct_aspects",10) <= 7,
            cd("nihss_baseline",0) > 15,
            cd("bp_sys",130) > 160,
            h2 - b >= 2,
        ])
        if ht_risk >= 2:
            alerts.append({"level":"warning","msg":(
                f"⚠️ **Hemorrhagic Transformation Risk Elevated** — {ht_risk}/4 risk factors "
                f"(ASPECTS ≤7, NIHSS >15, BP >160, early worsening). "
                f"Ensure 24h NCCT completed. Avoid anticoagulation until confirmed safe.")})

    for alert in alerts:
        card(alert["msg"], {"critical":"danger","warning":"warning","success":"success"}.get(alert["level"],"info"))

    return sum(1 for a in alerts if a["level"] == "critical")


# ═══════════════════════════════════════════════════════════════════════════
# SOAP NOTE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════
def generate_soap_note() -> str:
    c  = st.session_state.clinical_data
    sc = c.get("nihss_baseline", 0)
    sev, mort, _ = nihss_severity(sc)
    pathway  = c.get("assigned_pathway","Pending")
    pts_name = c.get("pat_name","[Patient Name]")
    age = str((datetime.date.today()-c["dob"]).days//365) if c.get("dob") else ""

    max_sys, max_dia, min_gcs = 0, 0, 15
    if "monitor_grid" in st.session_state:
        for _, row in st.session_state.monitor_grid.iterrows():
            bp_str = str(row.get("BP","")).strip()
            if "/" in bp_str:
                try:
                    bp_s, bp_d = map(int, bp_str.split("/"))    # BUG FIX: was sys, dia
                    max_sys = max(max_sys, bp_s); max_dia = max(max_dia, bp_d)
                except ValueError:
                    pass
            gcs_str = str(row.get("GCS Total","")).strip()
            if gcs_str.isdigit():
                min_gcs = min(min_gcs, int(gcs_str))

    vitals_summary = f"Max BP: {max_sys}/{max_dia} mmHg. Min GCS: {min_gcs}." if max_sys > 0 else "Vitals monitored per protocol."
    fast_ed = c.get("fast_ed_score","N/A")
    # BUG FIX: Guard against None scores
    dragon  = f"{c.get('dragon_score_final','—')}/10" if c.get("dragon_calculated") else "Not calculated"
    sedan   = f"{c.get('sedan_score_final','—')}/6"   if c.get("sedan_calculated") else "Not calculated"

    return f"""**SUBJECTIVE:**
{pts_name}, {age}y {c.get('sex','')}, presented {c.get('pres_date','')} {c.get('pres_time','')} from {c.get('location','')}.
Chief complaint: Sudden onset focal neurological deficit. ROSIER: {c.get('rosier_score',0)}.

**OBJECTIVE:**
NIHSS (Baseline): {sc} — {sev} | FAST-ED: {fast_ed}
CT Brain: {c.get('ct_result','Pending')} | ASPECTS: {c.get('ncct_aspects','N/A')} | CTA LVO: {c.get('cta_lvo','Not Performed')}
{vitals_summary}

**ASSESSMENT:**
Acute Ischemic Stroke — {pathway}.
SEDAN sICH Risk: {sedan} | DRAGON 3-Month Prognosis: {dragon}
{"Absolute CIs to IVT present." if any(c.get(f"abs_ci_{i}") for i in range(1,11)) else "No absolute CIs to IVT identified."}

**PLAN:**
{c.get('final_routing','Routing decision pending.')}.
Weight: {c.get('pt_weight',70.0)} kg.
{"Tenecteplase administered — Door-to-Needle time documented." if "Thrombolysis" in c.get("final_routing","") else ""}
{"EVT performed." if "EVT" in c.get("final_routing","") else ""}
Resident: {c.get('resident','')} | Consultant: {c.get('consultant','')}""".strip()


# ═══════════════════════════════════════════════════════════════════════════
# SIGN-OFF / VARIANCE ENGINE
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
        signer = st.session_state.order_data.get(signer_key,"")
        nurse  = st.session_state.order_data.get(nurse_key,"")
        var    = st.session_state.order_data.get(var_key,"")
        st.success(f"✅ **Day {day_num} Locked & Signed** | Resident: {signer} | Nurse: {nurse}")
        if var:
            st.info(f"📋 **Variance Documented:** {var}")
        return

    if not can_edit:
        readonly_banner("physician")
        return

    banner(f"Day {day_num} Sign-Off & Order Completion","grey","📝")
    c1, c2 = st.columns(2)
    with c1:
        sn = st.text_input("Resident / Fellow / MO Name & ID",
                           value=st.session_state.order_data.get(signer_key,""),
                           key=f"signer_{prefix}")
        st.session_state.order_data[signer_key] = sn
    with c2:
        nn = st.text_input("Bedside Nurse Name & ID",
                           value=st.session_state.order_data.get(nurse_key,""),
                           key=f"nurse_{prefix}")
        st.session_state.order_data[nurse_key] = nn

    if st.button(f"📝 Sign Off Day {day_num} Orders", key=f"sign_{prefix}"):
        st.session_state.order_data[signed_key] = True
        st.rerun()

    if st.session_state.order_data.get(signed_key, False):
        missing = [k for k in required_keys if not st.session_state.order_data.get(k, False)]
        if missing:
            card(f"⚠️ **{len(missing)} order(s) not completed.** Variance documentation mandatory (JCI).","warning")
            vt = st.text_area("Variance Reason & Action Taken (mandatory):",
                              value=st.session_state.order_data.get(var_key,""),
                              key=f"var_{prefix}", height=80)
            st.session_state.order_data[var_key] = vt
            if st.button(f"📌 Submit Variance & Lock Day {day_num}", key=f"submit_{prefix}"):
                if not vt.strip():
                    card("Variance notes cannot be empty.","danger","🚨")
                else:
                    for k in missing:
                        log_variance(section_label, f"Day {day_num}", k, vt)
                    st.session_state.order_data[locked_key] = True
                    st.rerun()
        else:
            st.session_state.order_data[locked_key] = True
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
# NIHSS FORM (Reusable)
# ═══════════════════════════════════════════════════════════════════════════
def nihss_form(suffix: str, label: str, expand: bool = False):
    opts       = get_nihss_opts()
    suffix_key = f"_{suffix}" if suffix else ""
    done_key   = f"nihss{suffix_key}_done" if suffix else "nihss_calculated"
    score_key  = f"nihss_{suffix}" if suffix else "nihss_baseline"

    with st.expander(f"NIHSS — {label}", expanded=expand):
        with st.form(f"nihss_form_{suffix or 'baseline'}"):
            col1, col2, col3, col4 = st.columns(4)
            groups = [["n1a","n1b","n1c","n2"],["n3","n4","n5l","n5r"],
                      ["n6l","n6r","n7","n8"],["n9","n10","n11"]]
            for ci, grp in enumerate(groups):
                with [col1,col2,col3,col4][ci]:
                    for k in grp:
                        sk = f"{k}{suffix_key}"
                        cur = cd(sk) or opts[k][0]
                        cur_idx = opts[k].index(cur) if cur in opts[k] else 0
                        chosen = st.selectbox(NIHSS_LABELS[k], opts[k], index=cur_idx,
                                              key=f"nihss_sel_{sk}")
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
                f'{kpi(str(sc),"NIHSS Score","primary")}'
                f'{kpi(sev,"Severity",style)}'
                f'{kpi(mort,"30-Day Mortality","danger")}'
                f'</div>',
                unsafe_allow_html=True,
            )


def lifestyle_checks(prefix: str):
    st.markdown("##### 🌱 Lifestyle Modification Counselling")
    c1, c2 = st.columns(2)
    items = [("f2","🚭 Smoking cessation"),("f3","🥦 Healthy diet"),
             ("f4","😴 Regular sleep"),("f5","⚖️ Weight reduction"),
             ("f6","💊 Control cholesterol"),("f7","🩺 Manage blood pressure"),
             ("f8","🩸 Manage blood sugar")]
    for idx, (k, label) in enumerate(items):
        col = c1 if idx % 2 == 0 else c2
        with col:
            val = st.checkbox(label, value=od(f"{prefix}_{k}"),
                              key=f"ls_{prefix}_{k}", disabled=not can_write("physician"))
            set_od(f"{prefix}_{k}", val)


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px 0;'>
      <div style='font-size:2.5rem;'>🏥</div>
      <div style='font-size:1rem;font-weight:800;color:#ffffff;letter-spacing:0.5px;line-height:1.3;'>
        Shifa International<br>Hospitals Ltd.
      </div>
      <div style='font-size:0.7rem;color:#93C5FD;margin-top:4px;'>
        AIS EMR | FM-MSA-429 Rev:02 | v3.1
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("#### 👤 Clinical Role")
    role_icons = {"Physician":"🩺","Nurse":"💉","Allied Health / Rehab":"🦽","Admin / Audit":"🔐"}
    sel_role = st.selectbox("Select Role:", ROLES,
                            index=ROLES.index(st.session_state.ui["role"]),
                            key="sb_role")
    st.session_state.ui["role"] = sel_role
    r_icon = role_icons.get(sel_role,"👤")
    st.markdown(
        f'<div style="margin:6px 0 12px 0;">'
        f'<span class="role-badge role-{sel_role.split()[0].lower()}">'
        f'{r_icon} {sel_role}</span></div>',
        unsafe_allow_html=True,
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
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### 🗺️ Navigation")
    nav_options = st.session_state.ui["unlocked"]
    cur_idx = nav_options.index(st.session_state.ui["screen"]) \
              if st.session_state.ui["screen"] in nav_options else 0
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
            unsafe_allow_html=True,
        )

    # AI sidebar panel
    st.markdown("---")
    api_ok = bool(_get_api_key())
    status_dot = "🟢" if api_ok else "🔴"
    st.markdown(
        f"""<div style='text-align:center;padding:8px 0 4px;'>
          <span style='font-size:1.6rem;'>🧠</span><br>
          <span style='font-weight:800;font-size:0.9rem;color:#ffffff;'>Dr. SHIFA</span><br>
          <span style='font-size:0.65rem;color:#93C5FD;'>AI Vascular Neurologist</span><br>
          <span style='font-size:0.62rem;color:{"#6EE7B7" if api_ok else "#FCA5A5"};'>{status_dot} {"Online" if api_ok else "Offline — configure API key"}</span>
        </div>""",
        unsafe_allow_html=True,
    )

    sb_quick_qs = [
        ("⚡ Next action?",    "What is the single most critical action I should take right now for this patient?"),
        ("💊 Drug doses?",     "What medications and exact doses are most critical for this patient at this moment?"),
        ("⚠️ Safety check?",  "What are the top 3 safety concerns I must not miss for this patient right now?"),
        ("📋 Complications?", "What complications is this patient most at risk for and how do I monitor/prevent them?"),
    ]
    for label, question in sb_quick_qs:
        if st.button(label, key=f"sb_ai_q_{label}", use_container_width=True):
            st.session_state["sb_ai_pending_q"] = question
            navigate_to("🧠 AI Vascular Neurologist")
            st.rerun()

    if st.button("💬 Open Full AI Consult →", key="sb_full_ai", use_container_width=True):
        navigate_to("🧠 AI Vascular Neurologist")
        st.rerun()

    # Emergency buttons
    st.markdown("---")
    st.markdown("### 🚨 Emergency Protocols")
    if st.button("🩸 sICH / Bleeding Reversal", use_container_width=True):
        navigate_to("Emergency: Bleeding")
        st.rerun()
    if st.button("👅 Orolingual Angioedema", use_container_width=True):
        navigate_to("Emergency: Angioedema")
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<span style='font-size:0.65rem;opacity:0.5;'>AHA/ASA 2026 | JCI Standards<br>"
        "© Shifa International Hospitals</span>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# PAGE HEADER UTILITY
# ═══════════════════════════════════════════════════════════════════════════
def page_header(title: str, subtitle: str = ""):
    pat = cd("pat_name")
    mrn = cd("mrn")
    pat_str = f"{pat} | MRN: {mrn}" if pat else "No patient loaded"
    role   = current_role()
    r_icon = {"Physician":"🩺","Nurse":"💉","Allied Health / Rehab":"🦽","Admin / Audit":"🔐"}.get(role,"👤")
    st.markdown(f"""
    <div class="hospital-header">
      <div>
        <div class="hosp-name">🏥 Shifa International Hospitals Ltd.</div>
        <div class="screen-title">{title}{(' — '+subtitle) if subtitle else ''}</div>
      </div>
      <div class="meta">
        {pat_str}<br>
        <span class="role-badge role-{role.split()[0].lower()}">{r_icon} {role}</span>
      </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ── SCREEN ROUTING
# ═══════════════════════════════════════════════════════════════════════════

# ── DASHBOARD ─────────────────────────────────────────────────────────────
if st.session_state.ui["screen"] == "🏠 Dashboard":
    page_header("🏠 Clinical Dashboard","Acute Ischemic Stroke EMR")

    sc = cd("nihss_baseline") or 0
    sev, mort, sev_style = nihss_severity(sc) if cd("nihss_calculated") else ("—","—","neutral")
    dtn_mins, dtn_status = get_dtn_status()
    dtn_val   = f"{dtn_mins:.0f}m" if dtn_mins else "—"
    dtn_style = {"ok":"success","warning":"warning","danger":"danger"}.get(dtn_status,"neutral")

    st.markdown(
        f'<div class="kpi-grid">'
        f'{kpi(cd("assigned_pathway") or "Pending","Active Pathway","primary")}'
        f'{kpi(str(sc) if cd("nihss_calculated") else "—","NIHSS Baseline",sev_style)}'
        f'{kpi(sev,"Severity",sev_style)}'
        f'{kpi(dtn_val,"Door-to-Needle",dtn_style)}'
        f'{kpi(str(len(st.session_state.variance_log)),"Variances Logged","warning" if st.session_state.variance_log else "success")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    steps_completed = sum([bool(cd("rosier_done")),bool(cd("nihss_done")),
                           bool(cd("routing_done")),
                           bool(od("s1_d1_signed") or od("s2_d1_signed") or od("s3_d1_signed"))])
    progress_pct = int((steps_completed / 4) * 100)
    st.markdown(f"**Pathway Completion: {progress_pct}%**")
    st.progress(progress_pct)
    st.markdown("<br>", unsafe_allow_html=True)

    if cd("mrn") != "":
        st.markdown("### ⏱️ Acute Stroke Time Metric (Door-to-Needle)")
        door_dt = datetime.datetime.combine(cd("pres_date"), cd("pres_time"))
        if cd("tpa_time") != datetime.time(0,0):
            needle_dt   = datetime.datetime.combine(cd("pres_date"), cd("tpa_time"))
            track_mins  = max((needle_dt - door_dt).total_seconds()/60, 0.0)
            status_label = f"Locked DTN: {track_mins:.0f} mins"
            is_done = True
        else:
            live_now    = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
            track_mins  = max((live_now - door_dt).total_seconds()/60, 0.0)
            status_label = f"Live Elapsed: {track_mins:.0f} mins"
            is_done = False

        time_pct = min(int((track_mins/60)*100),100)
        if is_done:
            bar_color   = "#16A34A" if track_mins<=45 else ("#D97706" if track_mins<=60 else "#DC2626")
            status_text = "✅ Target Met (≤60m)" if track_mins<=60 else "🚨 Target Exceeded (>60m) — Requires RCA"
        else:
            bar_color   = "#3B82F6" if track_mins<=45 else ("#F59E0B" if track_mins<=60 else "#EF4444")
            status_text = "▶️ Running Code Stroke Timer..." if track_mins<=60 else "🚨 Golden Hour Exceeded!"

        st.markdown(f"""
        <div style="margin-bottom:25px;padding:20px;background:white;border-radius:12px;
             box-shadow:0 4px 10px rgba(0,0,0,0.05);border:1px solid #E2E8F0;">
          <div style="display:flex;justify-content:space-between;margin-bottom:8px;
               font-weight:700;color:#334155;">
            <span>Door (0m)</span>
            <span style="color:{bar_color};">{status_label}</span>
            <span>AHA Target (60m)</span>
          </div>
          <div style="width:100%;background:#E2E8F0;border-radius:8px;height:24px;
               position:relative;overflow:hidden;">
            <div style="width:{time_pct}%;background:{bar_color};height:100%;
                 border-radius:8px;transition:width 0.5s ease;"></div>
            <div style="position:absolute;top:0;left:75%;height:100%;
                 border-left:2px dashed #0F172A;z-index:10;" title="45m Target"></div>
          </div>
          <div style="text-align:right;margin-top:8px;font-size:0.85rem;
               font-weight:700;color:{bar_color};">{status_text}</div>
        </div>""", unsafe_allow_html=True)

    if dtn_mins and dtn_status == "danger":
        card(f"🚨 **DTN {dtn_mins:.0f} min — EXCEEDS 60-min target.** Review delays and document variance.","danger")
    elif dtn_mins and dtn_status == "warning":
        card(f"⚠️ **DTN {dtn_mins:.0f} min — approaching 60-min limit.**","warning")

    st.markdown("---")
    st.markdown("### 🧭 Clinical Assessment Pathway")

    def tile_btn(label, icon, screen, status="active", sub="", key_sfx=""):
        si = {"done":"✅","active":"▶️","warning":"⚠️","critical":"🚨","locked":"🔒"}.get(status,"▶️")
        button_label = f"{si} {icon}\n{label}\n({sub})" if sub else f"{si} {icon}\n{label}"
        if st.button(button_label, key=f"btn_{screen}_{key_sfx}", use_container_width=True):
            go_to(screen)

    st.markdown("### 🚑 1. ER / Code Stroke Activation")
    col1, col2 = st.columns(2)
    with col1:
        tile_btn("Code Activation","🚨","Phase 1: ER Code Activation (Duty Dr)",
                 "done" if cd("rosier_done") else "active","ROSIER, LKW & Rapid Labs")
    with col2:
        tile_btn("Acute Neuro Eval","⚕️","Phase 2: Acute Neuro Eval (Responder)",
                 "done" if cd("nihss_done") else "active","NIHSS & Neuro Exam")

    st.markdown("### 🧠 2. Neurology Decision & Routing")
    col3, col4 = st.columns(2)
    with col3:
        tile_btn("Imaging & Routing","⏱️","Phase 3: Imaging & Routing Gate",
                 "done" if cd("routing_done") else "active","CT/CTA, CIs & TPA/EVT Decision")
    with col4:
        tile_btn("Stroke Unit Admission","🏥","Phase 4: Stroke Unit Orders (Days 1-3)",
                 "active" if cd("routing_done") else "locked","Physician, Nursing, Rehab Orders")

    st.markdown("### 📋 3. Ward Management & Rounds")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        tile_btn("Daily Rounds","📝","Phase 5: Daily Rounds & Progress Notes","active","SOAP & Notes")
    with col6:
        tile_btn("Serial NIHSS","📈","Phase 6: Serial NIHSS & Outcomes","active","2h, 24h & Discharge mRS")
    with col7:
        tile_btn("Variance Audit","🔍","Variance Audit",
                 "warning" if st.session_state.variance_log else "active",
                 f"{len(st.session_state.variance_log)} event(s)")
    with col8:
        tile_btn("AI Neurologist","🧠","🧠 AI Vascular Neurologist","active","Dr. SHIFA Consult")


# ── PHASE 1 ─────────────────────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 1: ER Code Activation (Duty Dr)":
    page_header("Phase 1: Initial Triage & Rapid Assessment","ROSIER Scale")

    banner("Patient Demographics","blue","👤")
    c1, c2, c3 = st.columns(3)
    with c1:
        v = st.text_input("MRN / Patient ID",  value=cd("mrn"),      key="w_mrn");  set_cd("mrn",v)
        v = st.date_input("Date of Birth",     value=cd("dob"),      key="w_dob");  set_cd("dob",v)
    with c2:
        v = st.text_input("Patient Full Name", value=cd("pat_name"), key="w_name"); set_cd("pat_name",v)
        v = st.selectbox("Sex",["Male","Female","Other"],
                         index=["Male","Female","Other"].index(cd("sex")), key="w_sex"); set_cd("sex",v)
    with c3:
        v = st.selectbox("Location",["ED","IPD"],
                         index=["ED","IPD"].index(cd("location")), key="w_loc"); set_cd("location",v)
        v = st.text_input("Resident / Fellow / MO", value=cd("resident"),   key="w_res"); set_cd("resident",v)
        v = st.text_input("Consultant Name",        value=cd("consultant"),  key="w_con"); set_cd("consultant",v)

    c4, c5 = st.columns(2)
    with c4: v = st.date_input("Presentation Date", value=cd("pres_date"), key="w_pdate"); set_cd("pres_date",v)
    with c5: v = st.time_input("Presentation Time", value=cd("pres_time"), key="w_ptime", step=60); set_cd("pres_time",v)

    v = st.checkbox("🚨 Sudden onset focal neurological deficit and/or altered mental status",
                    value=cd("sudden_onset"), key="w_sudden"); set_cd("sudden_onset",v)

    banner("ROSIER Scale","blue","📋")
    card("Score of <b>+1 or higher</b> indicates high likelihood of stroke/TIA.","info")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Negative Features (subtract if present):**")
        v = st.checkbox("Loss of consciousness or syncope? (−1)", value=cd("r_loc"),      key="w_rloc");  set_cd("r_loc",v)
        v = st.checkbox("Seizure activity? (−1)",                 value=cd("r_seizures"), key="w_rseiz"); set_cd("r_seizures",v)
    with r2:
        st.markdown("**New Acute Onset Features (+1 each):**")
        for key, label in [("r_face","i) Asymmetric facial weakness"),
                           ("r_arm","ii) Asymmetric arm weakness"),
                           ("r_leg","iii) Asymmetric leg weakness"),
                           ("r_speech","iv) Speech disturbance"),
                           ("r_visual","v) Visual field defect")]:
            v = st.checkbox(label, value=cd(key), key=f"w_{key}"); set_cd(key,v)

    pos    = sum([cd("r_face"),cd("r_arm"),cd("r_leg"),cd("r_speech"),cd("r_visual")])
    neg    = sum([cd("r_loc"),cd("r_seizures")])
    rosier = pos - neg
    set_cd("rosier_score", rosier)

    r_style = "success" if rosier >= 1 else "warning"
    r_msg   = "✅ High likelihood of stroke/TIA" if rosier >= 1 else "⚠️ Stroke less likely — consider stroke mimic"
    st.markdown(f'<div class="kpi-grid">{kpi(str(rosier),"ROSIER Score","primary")}</div>', unsafe_allow_html=True)
    card(r_msg, r_style)

    st.markdown("---")
    banner("Last Known Well (LKW) & Time Window","blue","🕒")
    c_lkw1, c_lkw2 = st.columns(2)
    with c_lkw1: v = st.date_input("Date LKW", value=cd("lkw_date"), key="w_lkwd"); set_cd("lkw_date",v)
    with c_lkw2: v = st.time_input("Time LKW", value=cd("lkw_time"), key="w_lkwt", step=60); set_cd("lkw_time",v)

    lkw_dt      = datetime.datetime.combine(cd("lkw_date"), cd("lkw_time"))
    live_now_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    hours       = max((live_now_dt - lkw_dt).total_seconds()/3600, 0.0)
    set_cd("time_since_lkw_hrs", hours)

    st.markdown(f"**Current System Time (PKT):** `{live_now_dt.strftime('%Y-%m-%d %H:%M')}`")
    st.markdown(
        f'<div class="kpi-grid">{kpi(f"{hours:.1f}h","Live Time Since LKW","primary" if hours<=4.5 else "warning" if hours<=24 else "danger")}</div>',
        unsafe_allow_html=True,
    )

    if hours > 24:
        set_cd("assigned_pathway","Non-Thrombolysis Pathway (> 24h)")
        card("🛑 **Late Presentation (>24h).** System directing to Non-Thrombolysis Pathway.","danger")
    elif hours <= 4.5:
        set_cd("assigned_pathway","IVT ± EVT Pathway (≤ 4.5h)")
        card("✅ **Primary Window (≤4.5h).** System directing to IVT ± EVT Pathway.","success")
    else:
        opts = ["Wake Up Stroke / Unknown Onset Pathway","EVT ± IVT Extended Window Pathway (4.5–24h)"]
        cur  = cd("ext_pathway_choice")
        card("⚠️ **Extended Window (4.5–24h).** Specify clinical scenario to lock pathway:","warning")
        ch = st.radio("Select Scenario:", opts, index=opts.index(cur) if cur in opts else 0,
                      key="w_extpath_p1", label_visibility="collapsed")
        set_cd("ext_pathway_choice",ch); set_cd("assigned_pathway",ch)

    banner("Rapid Assessment Checklist","teal","⚡")
    ra1, ra2 = st.columns(2)
    checks = [
        ("chk_vitals","Check Vitals & SpO₂"),("chk_monitor","Attach Cardiac Monitor"),
        ("chk_iv","📌 Large bore IV Access (MANDATORY)"),("chk_bsr","📌 BSR / Blood Glucose (MANDATORY)"),
        ("chk_ct","🧠 Order Urgent NCCT Brain"),("chk_ecg","ECG"),
        ("chk_labs","CBC, Na, K, Cr, Trop-I"),("chk_ptinr","PT / INR"),
    ]
    for idx, (k, label) in enumerate(checks):
        with ra1 if idx < 4 else ra2:
            v = st.checkbox(label, value=cd(k), key=f"w_{k}"); set_cd(k,v)

    st.markdown("---")
    ready_to_proceed = cd("chk_iv") and cd("chk_bsr")
    if not ready_to_proceed:
        st.warning("⚠️ **Mandatory:** Secure Large Bore IV Access and check BSR before proceeding.")

    render_ai_consult_panel(
        phase_key="phase1",
        intro="Dr. SHIFA can help interpret ROSIER scores, identify stroke mimics, prioritize investigations, and validate the time window.",
        quick_questions=[
            ("🎭 Stroke mimic?",   "Based on this patient's ROSIER score and presentation, what stroke mimics should I consider and how do I differentiate?"),
            ("⏱️ Time window?",    "Explain the clinical significance of this time since LKW and what pathway options are available."),
            ("🔬 Investigations?", "What investigations should I prioritize RIGHT NOW in the first 10 minutes for this patient?"),
        ],
    )

    c_prev, c_next = st.columns(2)
    with c_next:
        if rosier >= 1 or cd("r_override"):
            def handle_s1_next():
                set_cd("rosier_done", True)
                navigate_to("Phase 2: Acute Neuro Eval (Responder)")
            st.button("💾 Save Triage & Proceed ➡️", key="btn_s1_next",
                      on_click=handle_s1_next, disabled=not ready_to_proceed, use_container_width=True)
    with c_prev:
        if rosier < 1:
            v = st.checkbox("🔓 Consultant Override: Proceed despite low ROSIER",
                            value=cd("r_override"), key="w_rov")
            set_cd("r_override", v)


# ── PHASE 2 ─────────────────────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 2: Acute Neuro Eval (Responder)":
    page_header("Phase 2: Acute Clinical Evaluation","Detailed Neuro Exam & NIHSS")

    opts_sp  = ["Normal","Mild Dysarthria","Severe Dysarthria","Aphasia","Mute","Intubated","Other (See Remarks)"]
    opts_pup = ["Equal & Reactive","Unequal","Sluggish","Fixed/Dilated","Other (See Remarks)"]
    opts_eom = ["Normal","Partial Gaze Palsy","Forced Deviation","Other (See Remarks)"]
    opts_vis = ["Normal","Partial Hemianopia","Complete Hemianopia","Bilateral Blindness","Other (See Remarks)"]
    opts_face = ["Symmetric","Minor Paralysis","Partial/Complete Paralysis","Other (See Remarks)"]
    opts_pow  = ["5/5 Normal","4/5 Mild Weak","3/5 Anti-Gravity","2/5 Not Anti-Gravity","1/5 Flicker","0/5 None","Other"]
    opts_tone = ["Normal","Flaccid/Hypotonic","Spastic/Hypertonic","Rigidity","Other"]
    opts_sens = ["Normal","Right-sided Loss","Left-sided Loss","Bilateral Loss","Other (See Remarks)"]
    opts_cer  = ["Absent","Present Right","Present Left","Present Bilateral","Other (See Remarks)"]
    opts_ref  = ["Normal (2+)","Brisk (3+)","Depressed (1+)","Absent (0)","Other"]
    opts_pla  = ["Flexor (Downward)","Extensor (Upgoing)","Equivocal","Mute","Other"]

    def _idx(opts, val): return opts.index(val) if val in opts else 0

    banner("Detailed Neurological Examination","teal","🔍")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown("**Cranial Nerves / Head**")
        v = st.selectbox("Speech:",        opts_sp,   index=_idx(opts_sp,  cd("ex_speech","")),  key="ex_sp");   set_cd("ex_speech",v)
        v = st.selectbox("Pupils:",        opts_pup,  index=_idx(opts_pup, cd("ex_pupils","")),  key="ex_pup");  set_cd("ex_pupils",v)
        v = st.selectbox("EOM / Gaze:",   opts_eom,  index=_idx(opts_eom, cd("ex_eom","")),    key="ex_eom");  set_cd("ex_eom",v)
        v = st.selectbox("Visual Fields:", opts_vis,  index=_idx(opts_vis, cd("ex_vis","")),    key="ex_vis");  set_cd("ex_vis",v)
        v = st.selectbox("Face / Tongue:", opts_face, index=_idx(opts_face,cd("ex_face","")),   key="ex_fac");  set_cd("ex_face",v)
        v = st.text_input("Carotid Bruit:", value=cd("ex_bruit",""), key="ex_bruit"); set_cd("ex_bruit",v)
    with e2:
        st.markdown("**Motor & Tone (Bilateral)**")
        p1, p2 = st.columns(2)
        with p1:
            v = st.selectbox("Right Arm Power:", opts_pow,  index=_idx(opts_pow, cd("ex_pow_ra","")), key="pow_ra"); set_cd("ex_pow_ra",v)
            v = st.selectbox("Right Leg Power:", opts_pow,  index=_idx(opts_pow, cd("ex_pow_rl","")), key="pow_rl"); set_cd("ex_pow_rl",v)
            v = st.selectbox("Right Tone:",      opts_tone, index=_idx(opts_tone,cd("ex_tone_r","")), key="tone_r"); set_cd("ex_tone_r",v)
        with p2:
            v = st.selectbox("Left Arm Power:", opts_pow,  index=_idx(opts_pow, cd("ex_pow_la","")), key="pow_la"); set_cd("ex_pow_la",v)
            v = st.selectbox("Left Leg Power:", opts_pow,  index=_idx(opts_pow, cd("ex_pow_ll","")), key="pow_ll"); set_cd("ex_pow_ll",v)
            v = st.selectbox("Left Tone:",      opts_tone, index=_idx(opts_tone,cd("ex_tone_l","")), key="tone_l"); set_cd("ex_tone_l",v)
    with e3:
        st.markdown("**Sensory, Reflexes & Systemic**")
        r1, r2 = st.columns(2)
        with r1:
            v = st.selectbox("Right Reflex:",  opts_ref, index=_idx(opts_ref,cd("ex_ref_r","")), key="ref_r"); set_cd("ex_ref_r",v)
            v = st.selectbox("Right Plantar:", opts_pla, index=_idx(opts_pla,cd("ex_pla_r","")), key="pla_r"); set_cd("ex_pla_r",v)
        with r2:
            v = st.selectbox("Left Reflex:",  opts_ref, index=_idx(opts_ref,cd("ex_ref_l","")), key="ref_l"); set_cd("ex_ref_l",v)
            v = st.selectbox("Left Plantar:", opts_pla, index=_idx(opts_pla,cd("ex_pla_l","")), key="pla_l"); set_cd("ex_pla_l",v)
        v = st.selectbox("Sensations:",       opts_sens, index=_idx(opts_sens,cd("ex_sens","")), key="ex_sens"); set_cd("ex_sens",v)
        v = st.selectbox("Cerebellar/Ataxia:",opts_cer,  index=_idx(opts_cer, cd("ex_cer","")),  key="ex_cer");  set_cd("ex_cer",v)

    st.markdown("**Remarks / Free Text**")
    v = st.text_input("Detailed notes:", value=cd("ex_remarks",""), key="ex_remarks"); set_cd("ex_remarks",v)

    st.markdown("---")
    with st.expander("☑️ NIHSS Assessment & PRISMS Criteria", expanded=not cd("nihss_done")):
        nihss_form("","Baseline Assessment", expand=True)
        if cd("nihss_calculated"):
            sc = cd("nihss_baseline")

            if sc <= 5:
                n3_val  = get_score(cd("n3"));  n5l_val = get_score(cd("n5l")); n5r_val = get_score(cd("n5r"))
                n6l_val = get_score(cd("n6l")); n6r_val = get_score(cd("n6r")); n9_val  = get_score(cd("n9"))
                n11_val = get_score(cd("n11"))
                is_disabling = (n3_val>=2 or n5l_val>=2 or n5r_val>=2 or
                                n6l_val>=2 or n6r_val>=2 or n9_val>=2 or n11_val>=2)
                set_cd("prisms_disabling", is_disabling)
                if is_disabling:
                    card("✅ **Deficits are CLEARLY DISABLING (PRISMS met).** Patient remains IVT candidate.","success")
                else:
                    card("⚠️ **Deficits NOT clearly disabling.** Consider DAPT instead of IVT (AHA/ASA 2026).","warning")
                    v_ov = st.checkbox("Physician Override: Treat as disabling (clinical judgment)",
                                       value=cd("prisms_override",False), key="w_prisms_ov")
                    set_cd("prisms_override",v_ov)

            st.markdown("---")
            st.markdown("##### 🚑 FAST-ED Score (LVO Predictor)")
            f_score   = 1 if get_score(cd("n4"))>=1 else 0
            worst_arm = max(get_score(cd("n5l")), get_score(cd("n5r")))
            a_score   = 2 if worst_arm>=3 else (1 if worst_arm==2 else 0)
            worst_sp  = max(get_score(cd("n9")), get_score(cd("n10")))
            s_score   = 2 if worst_sp>=2 else (1 if worst_sp==1 else 0)
            e_score   = get_score(cd("n2"))
            d_score   = get_score(cd("n11"))
            fast_ed_total = f_score + a_score + s_score + e_score + d_score
            set_cd("fast_ed_score", fast_ed_total)

            kpi_style = "danger" if fast_ed_total>=4 else ("warning" if fast_ed_total>=2 else "success")
            hours = cd("time_since_lkw_hrs",0.0)

            c_f1, c_f2 = st.columns([1,2])
            with c_f1:
                st.markdown(
                    f'<div class="kpi-grid" style="margin-top:0;">'
                    f'{kpi(str(fast_ed_total),"FAST-ED (0-9)",kpi_style)}'
                    f'</div>', unsafe_allow_html=True,
                )
            with c_f2:
                if fast_ed_total >= 4:
                    rec_text  = f"🚨 **High LVO probability (60-85%).** Order NCCT + CTA. IVT and EVT candidate."
                    rec_color = "danger"
                elif fast_ed_total >= 2:
                    rec_text  = f"⚠️ **Moderate LVO probability (~30%).** Order NCCT + CTA."
                    rec_color = "warning"
                else:
                    rec_text  = f"✅ **Lower LVO probability (<15%).** NCCT Brain sufficient."
                    rec_color = "success"
                card(rec_text, rec_color, "🧠")

            render_ai_consult_panel(
                phase_key="phase2",
                intro="Dr. SHIFA analyzes the NIHSS pattern to identify vascular territory, predict LVO probability, and recommend optimal imaging.",
                quick_questions=[
                    ("🗺️ Vascular territory?", "Based on the NIHSS deficit pattern, what is the most likely affected vascular territory and vessel?"),
                    ("🩻 LVO prediction?",      "Based on the NIHSS pattern and FAST-ED score, what is the probability of LVO?"),
                    ("💊 IVT or DAPT?",         "Based on NIHSS, PRISMS criteria, and time window, should this patient receive IVT or DAPT?"),
                ],
            )

            c_prev, c_next = st.columns(2)
            with c_prev:
                st.button("⬅️ Back to Phase 1",
                          on_click=lambda: navigate_to("Phase 1: ER Code Activation (Duty Dr)"),
                          use_container_width=True)
            with c_next:
                def handle_s2_next():
                    set_cd("nihss_done",True)
                    navigate_to("Phase 3: Imaging & Routing Gate")
                st.button("💾 Save & Proceed to Imaging Gate ➡️", key="btn_s2_next",
                          on_click=handle_s2_next, use_container_width=True)


# ── PHASE 3 ─────────────────────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 3: Imaging & Routing Gate":
    page_header("Phase 3: Time & Imaging Gate","Diagnostics, CIs & Routing")

    banner("1. Time Window & Vitals Gate","blue","🕒")
    lkw_dt      = datetime.datetime.combine(cd("lkw_date"), cd("lkw_time"))
    live_now_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    hours       = max((live_now_dt - lkw_dt).total_seconds()/3600, 0.0)
    set_cd("time_since_lkw_hrs", hours)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="kpi-grid">{kpi(f"{hours:.1f}h","Time Since LKW","primary" if hours<=4.5 else "warning")}</div>',
            unsafe_allow_html=True,
        )
    with c2:
        bp_sys = st.number_input("Systolic BP (mmHg)", value=cd("bp_sys",150), key="w_bp_sys"); set_cd("bp_sys",bp_sys)
    with c3:
        bp_dia = st.number_input("Diastolic BP (mmHg)", value=cd("bp_dia",85),  key="w_bp_dia"); set_cd("bp_dia",bp_dia)

    bp_eligible = bp_sys < 185 and bp_dia < 110
    if not bp_eligible:
        card("🛑 **SAFETY GATE:** BP ≥185/110 mmHg. Lower BP before IVT or EVT.","danger")
    else:
        card("✅ **SAFETY GATE:** BP < 185/110 mmHg. Safe for revascularization evaluation.","success")

    st.markdown("---")
    banner("2. Neuroimaging Results","teal","🧠")
    c_img1, c_img2 = st.columns(2)
    with c_img1:
        opts_ct = ["Pending","Normal / No Hemorrhage","Extensive Hypodensity (> 1/3 MCA territory)","Intracranial Hemorrhage (ICH)"]
        v_ct = st.radio("NCCT Brain Finding:", opts_ct, index=opts_ct.index(cd("ct_result")), key="w_ct")
        set_cd("ct_result",v_ct)
        is_ct_ich  = (v_ct == "Intracranial Hemorrhage (ICH)")

        # SHOWSTOPPER 1: Visual ASPECTS Calculator
        if v_ct == "Normal / No Hemorrhage":
            with st.expander("🧠 Visual ASPECTS Calculator (Target: 10)", expanded=True):
                st.caption("Select regions with early ischemic changes. Score auto-deducts from 10.")
                aspects_score = 10
                c_a1, c_a2, c_a3 = st.columns(3)
                with c_a1:
                    st.markdown("**Subcortical**")
                    if st.checkbox("C (Caudate)",      value=cd("asp_c",False),  key="asp_c_chk"):  set_cd("asp_c", True);  aspects_score -= 1
                    else: set_cd("asp_c", False)
                    if st.checkbox("L (Lentiform)",    value=cd("asp_l",False),  key="asp_l_chk"):  set_cd("asp_l", True);  aspects_score -= 1
                    else: set_cd("asp_l", False)
                    if st.checkbox("IC (Int. Capsule)",value=cd("asp_ic",False), key="asp_ic_chk"): set_cd("asp_ic", True); aspects_score -= 1
                    else: set_cd("asp_ic", False)
                    if st.checkbox("I (Insular Ribbon)",value=cd("asp_i",False), key="asp_i_chk"):  set_cd("asp_i", True);  aspects_score -= 1
                    else: set_cd("asp_i", False)
                with c_a2:
                    st.markdown("**Cortical (Ganglionic)**")
                    if st.checkbox("M1 (Ant. MCA)",  value=cd("asp_m1",False), key="asp_m1_chk"): set_cd("asp_m1", True); aspects_score -= 1
                    else: set_cd("asp_m1", False)
                    if st.checkbox("M2 (Lat. MCA)",  value=cd("asp_m2",False), key="asp_m2_chk"): set_cd("asp_m2", True); aspects_score -= 1
                    else: set_cd("asp_m2", False)
                    if st.checkbox("M3 (Post. MCA)", value=cd("asp_m3",False), key="asp_m3_chk"): set_cd("asp_m3", True); aspects_score -= 1
                    else: set_cd("asp_m3", False)
                with c_a3:
                    st.markdown("**Cortical (Supraganglionic)**")
                    if st.checkbox("M4 (Ant. sup)", value=cd("asp_m4",False), key="asp_m4_chk"): set_cd("asp_m4", True); aspects_score -= 1
                    else: set_cd("asp_m4", False)
                    if st.checkbox("M5 (Lat. sup)", value=cd("asp_m5",False), key="asp_m5_chk"): set_cd("asp_m5", True); aspects_score -= 1
                    else: set_cd("asp_m5", False)
                    if st.checkbox("M6 (Post. sup)", value=cd("asp_m6",False), key="asp_m6_chk"): set_cd("asp_m6", True); aspects_score -= 1
                    else: set_cd("asp_m6", False)

                set_cd("ncct_aspects", aspects_score)
                asp_color = "success" if aspects_score >= 7 else "danger"
                st.markdown(
                    f'<div class="kpi-grid" style="margin-top:10px;">'
                    f'{kpi(str(aspects_score)+"/10","Total ASPECTS",asp_color)}'
                    f'</div>', unsafe_allow_html=True
                )
                if aspects_score < 7:
                    st.error("⚠️ ASPECTS < 7 — large core infarct. High risk for hemorrhagic transformation.")

    with c_img2:
        lvo_opts = ["Not Performed","No LVO","Yes — LVO Confirmed"]
        v_lvo = st.radio("CTA Carotid — LVO Status:", lvo_opts, index=lvo_opts.index(cd("cta_lvo")), key="w_lvo")
        set_cd("cta_lvo",v_lvo)
        if hours > 4.5:
            m_opts = ["Pending / Not Evaluated","✅ Mismatch Present","❌ Mismatch NOT Present"]
            v_mm = st.radio("Advanced Imaging Mismatch:", m_opts,
                            index=m_opts.index(cd("mismatch_status","Pending / Not Evaluated")), key="w_mm")
            set_cd("mismatch_status",v_mm)

    st.markdown("---")
    with st.expander("☑️ IVT Contraindications Checklist", expanded=False):
        st.markdown("##### 🛑 Absolute Contraindications (NO IVT)")
        is_ct_hypo = (cd("ct_result") == "Extensive Hypodensity (> 1/3 MCA territory)")
        ci_abs_list = [
            ("abs_ci_1","Acute ICH on imaging",                                                    is_ct_ich),
            ("abs_ci_2","Extensive Hypodensity > 1/3 MCA territory",                              is_ct_hypo),
            ("abs_ci_3","Severe coagulopathy (Plts <100k, INR >1.7, aPTT >40s, PT >15s)",        False),
            ("abs_ci_4","Infective endocarditis (Suspected or confirmed)",                         False),
            ("abs_ci_5","Aortic arch dissection",                                                  False),
            ("abs_ci_6","Intra-axial neoplasm",                                                    False),
            ("abs_ci_7","Recent Neurosurgery or Mod/Severe TBI (< 14 days)",                      False),
            ("abs_ci_8","Acute spinal cord injury (< 3 months)",                                  False),
            ("abs_ci_9","Amyloid-related conditions / ARIA",                                       False),
        ]
        has_absolute_ci = False
        for key, label, is_forced in ci_abs_list:
            current_val = cd(key) or is_forced
            if is_forced: set_cd(key,True)
            val = st.checkbox(label+(" (Auto-selected from CT)" if is_forced else ""),
                              value=current_val, key=f"chk_{key}", disabled=is_forced)
            set_cd(key,val)
            if val: has_absolute_ci = True

        st.markdown("##### ⚠️ Relative Contraindications (Consultant Decision)")
        ci_rel_list = [
            ("rel_ci_1","Recent DOAC (<48 h)"),          ("rel_ci_2","Prior Ischemic Stroke (<3 months)"),
            ("rel_ci_3","Prior Spontaneous ICH"),         ("rel_ci_4","Pre-existing disability / Frailty"),
            ("rel_ci_5","Pregnancy / Post-partum"),       ("rel_ci_6","Recent STEMI (<3 months) or Acute pericarditis"),
            ("rel_ci_7","Recent GI/GU bleeding (<21 d)"),("rel_ci_8","Major non-CNS surgery/trauma (<14 d)"),
        ]
        for key, label in ci_rel_list:
            val = st.checkbox(label, value=cd(key), key=f"chk_{key}"); set_cd(key,val)

    v_ref = st.checkbox("Patient / NOK refused IVT/EVT", value=cd("treatment_refused"), key="w_ref")
    set_cd("treatment_refused",v_ref)

    # Automated Pathway Decision
    st.markdown("---")
    banner("🤖 Automated Pathway Decision","purple","✨")

    final_decision = "Pending"
    decision_color = "grey"
    decision_text  = ""

    failed_prisms = (cd("nihss_baseline",0) <= 5 and
                     not cd("prisms_disabling",True) and
                     not cd("prisms_override",False))

    if is_ct_ich:
        final_decision = "Hemorrhagic Stroke Pathway"
        decision_color = "danger"
        decision_text  = "CRITICAL: Brain imaging shows ICH. Switch to Hemorrhagic Stroke Pathway immediately."
    elif hours > 24:
        final_decision = "Section 2: Non-Thrombolysis Pathway"
        decision_color = "warning"
        decision_text  = f"Time since LKW {hours:.1f}h > 24h. Outside standard revascularization windows."
    elif has_absolute_ci or v_ref:
        final_decision = "Section 2: Non-Thrombolysis Pathway"
        decision_color = "danger"
        decision_text  = "Absolute contraindications present OR treatment refused. IVT/EVT locked."
    elif failed_prisms:
        final_decision = "Section 2: Non-Thrombolysis Pathway"
        decision_color = "warning"
        decision_text  = "NIHSS 0–5 and deficits NOT clearly disabling (PRISMS fail). Standard medical management."
    elif not bp_eligible:
        final_decision = "Pending Blood Pressure Control"
        decision_color = "warning"
        decision_text  = "Patient meets criteria but BP must be < 185/110 mmHg before proceeding."
    elif hours <= 4.5:
        final_decision = "Section 1 — IV Thrombolysis (IVT)"
        decision_color = "success"
        decision_text  = f"Primary window ({hours:.1f}h). No hemorrhage. BP controlled. Proceed with Tenecteplase."
        if v_lvo == "Yes — LVO Confirmed":
            final_decision = "Section 1 — IVT + EVT"
            decision_text += " LVO confirmed: Call Interventional Radiology for EVT."
    elif 4.5 < hours <= 24:
        if cd("mismatch_status") == "✅ Mismatch Present":
            final_decision = ("Section 1 — IVT + EVT" if v_lvo=="Yes — LVO Confirmed"
                              else "Section 1 — IV Thrombolysis (IVT)")
            decision_color = "success"
            decision_text  = f"Extended window ({hours:.1f}h) with favorable mismatch. Proceed with treatment."
        else:
            final_decision = "Section 2: Non-Thrombolysis Pathway"
            decision_color = "warning"
            decision_text  = f"Extended window ({hours:.1f}h) but mismatch criteria NOT met."

    card(f"**RECOMMENDATION:** {decision_text}", decision_color)
    set_cd("assigned_pathway", final_decision)
    set_cd("final_routing",    final_decision)
    # --- ENHANCEMENT 7: eCONSULT AUTO-TRIGGER ---
    def econsult_trigger_block():
        banner("📞 Smart eConsult Trigger System", "purple", "📱")
        consults = []
        if "EVT" in cd("final_routing", "") or cd("cta_lvo") == "Yes — LVO Confirmed":
            consults.append({"specialty": "Interventional Radiology", "urgency": "STAT (< 15 min)", "reason": "LVO confirmed. EVT may be required.", "key": "ec_ir", "color": "danger"})
        if cd("nihss_baseline", 0) >= 16 or cd("ct_result") == "Intracranial Hemorrhage (ICH)":
            consults.append({"specialty": "Neurosurgery", "urgency": "Urgent (< 1h)", "reason": "Severe stroke or ICH. Mass effect evaluation.", "key": "ec_nsurg", "color": "danger"})
        
        consults.append({"specialty": "Speech & Language Therapy", "urgency": "Within 24h", "reason": "Formal swallowing assessment required (JCI standard).", "key": "ec_slt", "color": "warning"})
        consults.append({"specialty": "Physiotherapy", "urgency": "Within 24h", "reason": "Early mobilisation per AHA/ASA.", "key": "ec_pt", "color": "info"})

        stat_count = sum(1 for c in consults if "STAT" in c["urgency"])
        if stat_count: card(f"🚨 **{stat_count} STAT consult(s) required.** Contact on-call team NOW.", "danger")

        for c in consults:
            col_c, col_i = st.columns([1, 4])
            with col_c:
                v = st.checkbox("Done", value=cd(c["key"], False), key=f"ec_{c['key']}", disabled=not can_write("physician"))
                set_cd(c["key"], v)
            with col_i:
                bg = {"danger": "#DC2626", "warning": "#D97706", "info": "#2563EB"}.get(c["color"], "#2563EB")
                st.markdown(f'{"✅" if cd(c["key"], False) else "⏳"} **{c["specialty"]}** <span style="background:{bg};color:white;padding:2px 8px;border-radius:4px;font-size:0.75rem;">{c["urgency"]}</span><br><span style="font-size:0.85rem;color:#64748B;">{c["reason"]}</span>', unsafe_allow_html=True)

    econsult_trigger_block()

    if "IVT" in final_decision and "Non-Thrombolysis" not in final_decision:
        wt = st.number_input("Patient Weight (kg):", min_value=30.0, max_value=250.0,
                             value=float(cd("pt_weight",70.0)), step=1.0)
        set_cd("pt_weight",wt)
        dose_mg, _ = calc_tpa_dose(wt)
        card(f'💉 **Tenecteplase:** {dose_mg} mg IV bolus over 5 sec (0.25 mg/kg, max 25 mg) — AHA/ASA 2026 Class I',"info")
        t_val = st.time_input("Time of IVT Administration:", value=cd("tpa_time"), key="w_tpatime")
        set_cd("tpa_time",t_val)
        
    # --- ADD THIS BLOCK HERE ---
    elif "Non-Thrombolysis" in final_decision:
        if cd("nihss_baseline", 0) < 4:
            card("💊 **ER ACTION REQUIRED (Minor Stroke NIHSS < 4):** Load with DAPT (Clopidogrel 300 mg + Aspirin 75 mg) and start IV Normal Saline in ER before shifting to Stroke Unit.", "warning")
        else:
            card("💊 **ER ACTION REQUIRED (Stroke NIHSS ≥ 4):** Load with Aspirin 300 mg and start IV Normal Saline in ER before shifting to Stroke Unit.", "warning")
    # ---------------------------

    if "IVT" in final_decision:
        with st.expander("🎓 SEDAN Score (sICH Risk Predictor)", expanded=False):
            st.info("Predicts risk of symptomatic ICH after IVT.")
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                age = (datetime.date.today()-cd("dob")).days//365 if cd("dob") else 0
                st.markdown(f"• **Age:** {age} years | **Baseline NIHSS:** {cd('nihss_baseline',0)}")
            with c_s2:
                v_glu_sedan  = st.number_input("Baseline Glucose (mg/dL):", value=int(cd("dragon_glucose",100)), step=10, key="sedan_glu")
                set_cd("dragon_glucose",v_glu_sedan)
                v_early_inf   = st.checkbox("Early infarct signs on CT",        value=cd("sedan_early_infarct"), key="sedan_inf");  set_cd("sedan_early_infarct",v_early_inf)
                v_dense_sedan = st.checkbox("Hyperdense cerebral artery sign",  value=cd("dragon_dense_artery"), key="sedan_dense"); set_cd("dragon_dense_artery",v_dense_sedan)
            if st.button("Calculate SEDAN Risk", key="btn_sedan"):
                s_score = 0
                glu_mmol = v_glu_sedan / 18.0
                if glu_mmol > 12.0: s_score += 2
                elif glu_mmol >= 8.0: s_score += 1
                if v_early_inf:   s_score += 1
                if v_dense_sedan: s_score += 1
                if age >= 75:     s_score += 1
                if cd("nihss_baseline",0) > 10: s_score += 1
                set_cd("sedan_score_final",s_score); set_cd("sedan_calculated",True)
            if cd("sedan_calculated"):
                ss = cd("sedan_score_final",0)
                risk_map = {0:"1.4%",1:"2.9%",2:"7.1%",3:"9.8%",4:"21.6%",5:"33.3%"}
                risk_pct   = risk_map.get(ss,">33.3%")
                risk_color = "danger" if ss>=4 else ("warning" if ss>=2 else "success")
                st.markdown(f'<div class="kpi-grid">{kpi(str(ss),"SEDAN Score (0-6)","primary")}</div>', unsafe_allow_html=True)
                card(f"**Predicted sICH Risk:** {risk_pct}", risk_color)

    if "IVT" in final_decision or "EVT" in final_decision:
        st.markdown("---")
        banner("🔒 Dr. SHIFA — AI Safety Gate","ai","🧠")
        col_ivt, col_evt = st.columns(2)
        with col_ivt:
            if "IVT" in final_decision:
                if st.button("🔒 Run Full IVT Safety Gate", key="btn_ivt_gate", use_container_width=True):
                    result = ai_safety_gate_ivt()
                    st.session_state.ai_phase_cache["ivt_gate"] = result
                    st.rerun()
                if "ivt_gate" in st.session_state.ai_phase_cache:
                    st.markdown(
                        f'<div class="ai-bubble-assistant"><b style="color:#4C1D95;">🔒 IVT Safety Analysis:</b><br><br>'
                        f'{st.session_state.ai_phase_cache["ivt_gate"]}</div>',
                        unsafe_allow_html=True,
                    )
                    if st.button("Clear IVT Gate", key="clr_ivt_gate"):
                        del st.session_state.ai_phase_cache["ivt_gate"]; st.rerun()
        with col_evt:
            if "EVT" in final_decision:
                if st.button("🔒 Run Full EVT Eligibility Check", key="btn_evt_gate", use_container_width=True):
                    result = ai_safety_gate_evt()
                    st.session_state.ai_phase_cache["evt_gate"] = result
                    st.rerun()
                if "evt_gate" in st.session_state.ai_phase_cache:
                    st.markdown(
                        f'<div class="ai-bubble-assistant"><b style="color:#4C1D95;">🔒 EVT Eligibility Analysis:</b><br><br>'
                        f'{st.session_state.ai_phase_cache["evt_gate"]}</div>',
                        unsafe_allow_html=True,
                    )
                    if st.button("Clear EVT Gate", key="clr_evt_gate"):
                        del st.session_state.ai_phase_cache["evt_gate"]; st.rerun()

    render_ai_consult_panel(
        phase_key="phase3",
        intro="Dr. SHIFA provides evidence-based reasoning on pathway decisions, contraindication weighting, and drug dosing.",
        quick_questions=[
            ("💊 Tenecteplase dose?", "Confirm the correct Tenecteplase dose, administration technique, and 24h monitoring protocol."),
            ("⚖️ Relative CIs?",     "How do I weigh the relative contraindications present? Is the benefit-risk ratio favorable?"),
            ("📞 Who do I call?",    "Who should I notify RIGHT NOW based on the current pathway, and in what order?"),
        ],
    )

    c_prev, c_next = st.columns(2)
    with c_prev:
        st.button("⬅️ Back to Phase 2",
                  on_click=lambda: navigate_to("Phase 2: Acute Neuro Eval (Responder)"),
                  use_container_width=True)
    with c_next:
        can_proceed = "Pending" not in final_decision
        def handle_s3_next():
            set_cd("routing_done",True)
            navigate_to("Phase 4: Stroke Unit Orders (Days 1-3)")
        st.button("💾 Save & Transfer to Stroke Unit ➡️", key="btn_s3_route",
                  on_click=handle_s3_next, disabled=not can_proceed, use_container_width=True)


# ── PHASE 4 ─────────────────────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 4: Stroke Unit Orders (Days 1-3)":
    page_header("Phase 4: Unified Orders Workspace", "Parallel Pathway Execution")

    loc_score    = get_score(cd("n1a"))
    face_score   = get_score(cd("n4"))
    speech_score = get_score(cd("n10"))
    
    route = cd("final_routing", "")
    
    # --- STRICT PATHWAY SEPARATION ---
    is_non = "Non-Thrombolysis" in route
    is_ivt = ("IVT" in route or "Thrombolysis" in route) and not is_non
    is_evt = "EVT" in route and not is_ivt
    
    if is_ivt: sec = "s1"
    elif is_non: sec = "s2"
    else: sec = "s3"

    if loc_score > 0 or face_score > 0 or speech_score > 0:
        st.markdown(
            """<div style="background:#FEF3C7;color:#92400E;padding:15px;border-radius:8px;
                margin-bottom:15px;border-left:6px solid #F59E0B;">
              <h4 style="margin-top:0;margin-bottom:5px;color:#92400E;">⚠️ AHA/ASA SAFETY GATE: AUTOMATIC NPO</h4>
              <b>High Aspiration Risk Detected.</b> Deficits in LOC, Facial Palsy, or Dysarthria detected.
              Patient is <b>NPO</b> until formal swallow screen passed by Speech Therapist.
            </div>""", unsafe_allow_html=True
        )
        set_od(f"{sec}_d1_m0", True)

    st.markdown(
        f'<div class="card card-info" style="display:flex;justify-content:space-between;">'
        f'<span>📌 <b>Active Pathway:</b> {cd("assigned_pathway")}</span>'
        f'<span><b>Final Route:</b> {route}</span>'
        f'<span><b>Time since LKW:</b> {cd("time_since_lkw_hrs",0):.1f}h</span>'
        f'</div>', unsafe_allow_html=True
    )

    tab_phys, tab_nurse, tab_allied = st.tabs([
        "🩺 1. Physician Orders", "💉 2. Nursing & Vitals", "🤝 3. Allied Health"
    ])

    sc = cd("nihss_baseline") or 0

    # =========================================================================
    # 🩺 TAB 1: PHYSICIAN ORDERS
    # =========================================================================
    with tab_phys:
        if route == "Pending" or not cd("routing_done"):
            st.warning("⚠️ Complete Clinical Evaluation in Phase 3 to unlock orders.")
        else:
            st.subheader(f"Physician Orders — {route}")
            d1, d2, d3 = st.tabs(["Day 1", "Day 2", "Day 3"])
            
            # ─────────────────────────────────────────────────────────────────
            # SECTION 1: THROMBOLYSIS PATHWAY (IVT)
            # ─────────────────────────────────────────────────────────────────
            if sec == "s1":
                with d1:
                    banner("A — Physician", "teal", "🩺")
                    card("🔴 BP Target post-IVT: TREAT ONLY if BP ≥ 180/105 mmHg", "danger")
                    st.checkbox("Labetalol, 5-20 mg IV bolus q 15 minutes or start at 2 mg/min infusion (max 300 mg/day) AND/OR Hydralazine, 5-20 mg IV push every 30 minutes (max 300 mg/day); only treat if BP ≥ 180/105 mmHg.", value=od("s1_d1_p1"), key="s1_d1_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d1_p1", st.session_state.s1_d1_p1_chk))
                    st.checkbox("Injection normal saline", value=od("s1_d1_p2"), key="s1_d1_p2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d1_p2", st.session_state.s1_d1_p2_chk))
                    st.checkbox("If EVT also performed: Inspect arterial access/groin site and follow post-thrombectomy orders.", value=od("s1_d1_p3"), key="s1_d1_p3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d1_p3", st.session_state.s1_d1_p3_chk))
                    
                    banner("C — Imaging", "teal", "🖼️")
                    for i, lbl in enumerate(["Chest X-Ray", "Carotid imaging", "Transthoracic echo", "48-h Holter monitor (if indicated)"]):
                        st.checkbox(lbl, value=od(f"s1_d1_i{i+1}"), key=f"s1_d1_i{i+1}_chk", disabled=not can_write("physician"), on_change=lambda i=i: set_od(f"s1_d1_i{i+1}", st.session_state[f"s1_d1_i{i+1}_chk"]))
                    sign_off_block("s1_d1_phys", 1, ["s1_d1_p1", "s1_d1_p2"], "Physician Orders", can_write("physician"))

                with d2:
                    banner("A — Physician", "teal", "🩺")
                    antiplatelet_order = "Tab Aspirin 50–325 mg once daily after reviewing NCCT brain OR dual antiplatelets if NIHSS ≤ 3" if sc <= 3 else "Tab Aspirin 50–325 mg once daily after reviewing NCCT brain"
                    st.checkbox(antiplatelet_order, value=od("s1_d2_p1"), key="s1_d2_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d2_p1", st.session_state.s1_d2_p1_chk))
                    st.checkbox("Rosuvastatin 20 mg at night", value=od("s1_d2_p2"), key="s1_d2_p2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d2_p2", st.session_state.s1_d2_p2_chk))
                    st.checkbox("Intermittent pneumatic compression OR DVT prophylaxis", value=od("s1_d2_p3"), key="s1_d2_p3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d2_p3", st.session_state.s1_d2_p3_chk))
                    
                    banner("B — Lab Tests", "teal", "🔬")
                    st.checkbox("Fasting lipid profile", value=od("s1_d2_l1"), key="s1_d2_l1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d2_l1", st.session_state.s1_d2_l1_chk))
                    st.checkbox("HbA1c", value=od("s1_d2_l2"), key="s1_d2_l2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d2_l2", st.session_state.s1_d2_l2_chk))

                    banner("C — Imaging", "teal", "🖼️")
                    st.checkbox("Repeat NCCT / MRI Brain after 24 h of IVT administration", value=od("s1_d2_i1"), key="s1_d2_i1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d2_i1", st.session_state.s1_d2_i1_chk))
                    sign_off_block("s1_d2_phys", 2, ["s1_d2_i1"], "Physician Orders", can_write("physician"))

                with d3:
                    banner("A — Physician", "teal", "🩺")
                    st.checkbox("Reduce or discontinue IV fluids if tolerating oral intake", value=od("s1_d3_p1"), key="s1_d3_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d3_p1", st.session_state.s1_d3_p1_chk))
                    sign_off_block("s1_d3_phys", 3, ["s1_d3_p1"], "Physician Orders", can_write("physician"))

            # ─────────────────────────────────────────────────────────────────
            # SECTION 2: NON-THROMBOLYSIS PATHWAY
            # ─────────────────────────────────────────────────────────────────
            elif sec == "s2":
                with d1:
                    banner("A — Physician", "teal", "🩺")
                    antiplatelet_order = "Tab Aspirin 50–325 mg once daily OR dual antiplatelets if NIHSS ≤ 3" if sc <= 3 else "Tab Aspirin 50–325 mg once daily"
                    st.checkbox(antiplatelet_order, value=od("s2_d1_p1"), key="s2_d1_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_p1", st.session_state.s2_d1_p1_chk))
                    st.checkbox("Rosuvastatin 20mg at night", value=od("s2_d1_p2"), key="s2_d1_p2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_p2", st.session_state.s2_d1_p2_chk))
                    st.checkbox("Intermittent pneumatic compression OR DVT Prophylaxis", value=od("s2_d1_p3"), key="s2_d1_p3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_p3", st.session_state.s2_d1_p3_chk))
                    st.checkbox("Labetalol, 5-20 mg IV bolus every 15 minutes or start at 2 mg/min infusion (max 300 mg/day) AND/OR Hydralazine, 5-20 mg IV push q 30 min. Treat only if BP ≥ 220/120 mmHg", value=od("s2_d1_p4"), key="s2_d1_p4_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_p4", st.session_state.s2_d1_p4_chk))
                    st.checkbox("Injection normal saline", value=od("s2_d1_p5"), key="s2_d1_p5_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_p5", st.session_state.s2_d1_p5_chk))
                    st.checkbox("Treat fever with antipyretics", value=od("s2_d1_p6"), key="s2_d1_p6_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_p6", st.session_state.s2_d1_p6_chk))

                    banner("B — Lab Tests", "teal", "🔬")
                    st.checkbox("Fasting lipid profile", value=od("s2_d1_l1"), key="s2_d1_l1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_l1", st.session_state.s2_d1_l1_chk))
                    st.checkbox("HbA1c", value=od("s2_d1_l2"), key="s2_d1_l2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_l2", st.session_state.s2_d1_l2_chk))
                    
                    banner("C — Imaging", "teal", "🖼️")
                    for i, lbl in enumerate(["Chest X-Ray", "Carotid imaging", "Transthoracic echo", "48-h Holter monitor (if indicated)"]):
                        st.checkbox(lbl, value=od(f"s2_d1_i{i+1}"), key=f"s2_d1_i{i+1}_chk", disabled=not can_write("physician"), on_change=lambda i=i: set_od(f"s2_d1_i{i+1}", st.session_state[f"s2_d1_i{i+1}_chk"]))

                    sign_off_block("s2_d1_phys", 1, ["s2_d1_p4", "s2_d1_p5"], "Physician Orders", can_write("physician"))

                with d2:
                    banner("A — Physician", "teal", "🩺")
                    st.checkbox("Same as prior day", value=od("s2_d2_p1"), key="s2_d2_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d2_p1", st.session_state.s2_d2_p1_chk))
                    sign_off_block("s2_d2_phys", 2, ["s2_d2_p1"], "Physician Orders", can_write("physician"))

                with d3:
                    banner("A — Physician", "teal", "🩺")
                    st.checkbox("Reduce or discontinue IV fluids if tolerating oral intake", value=od("s2_d3_p1"), key="s2_d3_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d3_p1", st.session_state.s2_d3_p1_chk))
                    st.checkbox("Anticoagulation planning (if indicated)", value=od("s2_d3_p2"), key="s2_d3_p2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d3_p2", st.session_state.s2_d3_p2_chk))
                    sign_off_block("s2_d3_phys", 3, ["s2_d3_p1"], "Physician Orders", can_write("physician"))

            # ─────────────────────────────────────────────────────────────────
            # SECTION 3: EVT PATHWAY (ENDOVASCULAR THROMBECTOMY ONLY)
            # ─────────────────────────────────────────────────────────────────
            elif sec == "s3":
                with d1:
                    banner("A — Physician", "teal", "🩺")
                    antiplatelet_order = "Tab Aspirin 50–325 mg once daily OR dual antiplatelets if NIHSS ≤ 3" if sc <= 3 else "Tab Aspirin 50–325 mg once daily"
                    st.checkbox(antiplatelet_order, value=od("s3_d1_p1"), key="s3_d1_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_p1", st.session_state.s3_d1_p1_chk))
                    st.checkbox("Rosuvastatin 20 mg at night", value=od("s3_d1_p2"), key="s3_d1_p2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_p2", st.session_state.s3_d1_p2_chk))
                    st.checkbox("Intermittent pneumatic compression OR DVT Prophylaxis", value=od("s3_d1_p3"), key="s3_d1_p3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_p3", st.session_state.s3_d1_p3_chk))
                    card("🟠 BP Target post-EVT: TREAT ONLY if BP > 180/105 mmHg", "warning")
                    st.checkbox("Labetalol, 5-20 mg IV bolus every 15 minutes or start at 2 mg/min infusion (max 300 mg/day) AND/OR Hydralazine, 5-20 mg IV push q 30 min. Treat only if BP > 180/105 mmHg", value=od("s3_d1_p4"), key="s3_d1_p4_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_p4", st.session_state.s3_d1_p4_chk))
                    st.checkbox("Injection normal saline", value=od("s3_d1_p5"), key="s3_d1_p5_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_p5", st.session_state.s3_d1_p5_chk))
                    st.checkbox("Inspect arterial access/groin site and follow post-thrombectomy orders.", value=od("s3_d1_p6"), key="s3_d1_p6_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_p6", st.session_state.s3_d1_p6_chk))
                    
                    banner("B — Lab Tests", "teal", "🔬")
                    st.checkbox("Fasting lipid profile", value=od("s3_d1_l1"), key="s3_d1_l1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_l1", st.session_state.s3_d1_l1_chk))
                    st.checkbox("HbA1c", value=od("s3_d1_l2"), key="s3_d1_l2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_l2", st.session_state.s3_d1_l2_chk))

                    banner("C — Imaging", "teal", "🖼️")
                    for i, lbl in enumerate(["Chest X-Ray", "Carotid imaging", "Transthoracic echo", "48-h Holter monitor (if indicated)"]):
                        st.checkbox(lbl, value=od(f"s3_d1_i{i+1}"), key=f"s3_d1_i{i+1}_chk", disabled=not can_write("physician"), on_change=lambda i=i: set_od(f"s3_d1_i{i+1}", st.session_state[f"s3_d1_i{i+1}_chk"]))
                    sign_off_block("s3_d1_phys", 1, ["s3_d1_p4", "s3_d1_p5"], "Physician Orders", can_write("physician"))

                with d2:
                    banner("A — Physician", "teal", "🩺")
                    st.checkbox("Same as prior", value=od("s3_d2_p1"), key="s3_d2_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d2_p1", st.session_state.s3_d2_p1_chk))
                    
                    banner("C — Imaging", "teal", "🖼️")
                    st.checkbox("Repeat NCCT / MRI brain after 24 h of EVT", value=od("s3_d2_i1"), key="s3_d2_i1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d2_i1", st.session_state.s3_d2_i1_chk))
                    sign_off_block("s3_d2_phys", 2, ["s3_d2_i1"], "Physician Orders", can_write("physician"))

                with d3:
                    banner("A — Physician", "teal", "🩺")
                    st.checkbox("Reduce or discontinue IV fluids if tolerating oral intake", value=od("s3_d3_p1"), key="s3_d3_p1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d3_p1", st.session_state.s3_d3_p1_chk))
                    st.checkbox("Anticoagulation planning (if indicated)", value=od("s3_d3_p2"), key="s3_d3_p2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d3_p2", st.session_state.s3_d3_p2_chk))
                    sign_off_block("s3_d3_phys", 3, ["s3_d3_p1"], "Physician Orders", can_write("physician"))

    # =========================================================================
    # 💉 TAB 2: NURSING & VITALS
    # =========================================================================
    with tab_nurse:
        if route == "Pending" or not cd("routing_done"):
            st.warning("⚠️ Complete Clinical Evaluation to unlock.")
        else:
            st.subheader(f"D — Nursing Checklist — {route}")
            
            # --- VITALS GRID & WATCHDOG ---
            banner("24-Hour Vitals Grid", "red", "📊")
            st.session_state.monitor_grid = st.data_editor(st.session_state.monitor_grid, use_container_width=True, num_rows="fixed", key="nurse_grid")
            if sec == "s1": # IVT Watchdog
                bp_violations = []
                for _, row in st.session_state.monitor_grid.iterrows():
                    bp_str = str(row.get("BP", "")).strip()
                    if "/" in bp_str:
                        try:
                            sys, dia = map(int, bp_str.split("/"))
                            if sys > 180 or dia > 105:
                                bp_violations.append(f"{bp_str} at {row['Actual Time'] or row['Time since IVT']}")
                        except ValueError: pass
                if bp_violations:
                    v_list = " • ".join(bp_violations)
                    st.markdown(f"""<div style="background:#7F1D1D; color:white; padding:15px; border-radius:8px; margin-bottom:15px; border-left: 8px solid #EF4444;">
                        <h4 style="color:white; margin-top:0;">🚨 HIGH-RISK PROTOCOL ALERT</h4>
                        <b>BP Target Violation ( > 180/105 ) detected post-IVT:</b> {v_list}<br><br>
                        <i><b>Immediate Action Required:</b> Administer IV Labetalol or Hydralazine per protocol to prevent hemorrhagic transformation.</i></div>""", unsafe_allow_html=True)

            card("Give supplemental O2 if SPO2 < 94%. Target BSR range should be 140 to 180 mg/dL. (Treat hypoglycemia if BSR < 60 mg/dL). Use SC insulin protocol. Inform Physician in case of Fever.", "info")

            n_d1, n_d2, n_d3 = st.tabs(["Day 1", "Day 2", "Day 3"])
            
            if sec == "s1":
                with n_d1:
                    tasks = [
                        ("n1", "GCS, vitals, and SPO2 monitoring 4 hourly"), ("n2", "Maintain normothermia"),
                        ("n3", "Intake/output charting"), ("n4", "Glucose-check before meals and at night"),
                        ("n5", "Aspiration precautions."), ("n6", "Fall precautions."),
                        ("n7", "Posture change 2 hourly, Decubitus precautions, air mattress."),
                        ("n8", "Foley's catheter (if needed)"), ("n9", "Cardiac monitoring as per unit protocol"),
                        ("n10", "No prick to draw blood allowed except finger pick for BSR"),
                        ("n11", "Monitor for post-IVT ICH or angioedema. If suspected, see Annexure (Table 4 and/or 5) for emergency protocols."),
                        ("n12", "If EVT also performed: Inspect arterial access/groin site for hematoma, bruising, distal limb pulses as per post-EVT orders."),
                        ("n13", "Pain Assessment")
                    ]
                    for k, lbl in tasks: st.checkbox(lbl, value=od(f"s1_d1_{k}"), key=f"s1_{k}_d1_chk", disabled=not can_write("nursing"), on_change=lambda k=k: set_od(f"s1_d1_{k}", st.session_state[f"s1_{k}_d1_chk"]))
                with n_d2:
                    for k, lbl in [("n1", "Same as prior"), ("n2", "Assess for removal of Foley's catheter (if needed)")]:
                        st.checkbox(lbl, value=od(f"s1_d2_{k}"), key=f"s1_{k}_d2_chk", disabled=not can_write("nursing"), on_change=lambda k=k: set_od(f"s1_d2_{k}", st.session_state[f"s1_{k}_d2_chk"]))
                with n_d3:
                    st.checkbox("Same as prior", value=od("s1_d3_n1"), key="s1_n1_d3_chk", disabled=not can_write("nursing"), on_change=lambda: set_od("s1_d3_n1", st.session_state.s1_n1_d3_chk))

            elif sec == "s2":
                with n_d1:
                    tasks = [
                        ("n1", "GCS, vitals, and SPO2 monitoring 4 hourly"), ("n2", "Maintain normothermia"),
                        ("n3", "Intake / output charting"), ("n4", "Gluco-check before meals and at night"),
                        ("n5", "Aspiration precautions"), ("n6", "Fall precautions"),
                        ("n7", "Posture change 2 hourly, Decubitus precautions, Air mattress."),
                        ("n8", "Cardiac monitoring as per unit protocol"), ("n9", "Foley's catheter (if needed)"),
                        ("n10", "Pain Assessment")
                    ]
                    for k, lbl in tasks: st.checkbox(lbl, value=od(f"s2_d1_{k}"), key=f"s2_{k}_d1_chk", disabled=not can_write("nursing"), on_change=lambda k=k: set_od(f"s2_d1_{k}", st.session_state[f"s2_{k}_d1_chk"]))
                with n_d2:
                    for k, lbl in [("n1", "Continue routine care"), ("n2", "Assess for removal of Foley catheter (If needed)"), ("n3", "Out of bed/ mobilization (as tolerated).")]:
                        st.checkbox(lbl, value=od(f"s2_d2_{k}"), key=f"s2_{k}_d2_chk", disabled=not can_write("nursing"), on_change=lambda k=k: set_od(f"s2_d2_{k}", st.session_state[f"s2_{k}_d2_chk"]))
                with n_d3:
                    st.checkbox("Same as prior", value=od("s2_d3_n1"), key="s2_n1_d3_chk", disabled=not can_write("nursing"), on_change=lambda: set_od("s2_d3_n1", st.session_state.s2_n1_d3_chk))

            elif sec == "s3":
                with n_d1:
                    tasks = [
                        ("n1", "GCS, vitals, and SPO2 monitoring 4 hourly"), ("n2", "Maintain normothermia"),
                        ("n3", "Pain Assessment"), ("n4", "Intake / output charting"), 
                        ("n5", "Gluco-check before meals and at night"), ("n6", "Aspiration precautions"), 
                        ("n7", "Fall precautions"), ("n8", "Posture change 2 hourly, Decubitus precautions, Air mattress."),
                        ("n9", "Cardiac monitoring as per unit protocol"), ("n10", "Foley's catheter (if needed)"),
                        ("n11", "Inspect arterial access/groin site for hematoma, bruising, distal limb pulses and follow post-thrombectomy orders.")
                    ]
                    for k, lbl in tasks: st.checkbox(lbl, value=od(f"s3_d1_{k}"), key=f"s3_{k}_d1_chk", disabled=not can_write("nursing"), on_change=lambda k=k: set_od(f"s3_d1_{k}", st.session_state[f"s3_{k}_d1_chk"]))
                with n_d2:
                    for k, lbl in [("n1", "Continue routine care"), ("n2", "Assess for removal of Foley catheter (If needed)"), ("n3", "Out of bed/ mobilization (as tolerated).")]:
                        st.checkbox(lbl, value=od(f"s3_d2_{k}"), key=f"s3_{k}_d2_chk", disabled=not can_write("nursing"), on_change=lambda k=k: set_od(f"s3_d2_{k}", st.session_state[f"s3_{k}_d2_chk"]))
                with n_d3:
                    st.checkbox("Same as prior", value=od("s3_d3_n1"), key="s3_n1_d3_chk", disabled=not can_write("nursing"), on_change=lambda: set_od("s3_d3_n1", st.session_state.s3_n1_d3_chk))


    # =========================================================================
    # 🤝 TAB 3: ALLIED HEALTH & EDUCATION
    # =========================================================================
    with tab_allied:
        if route == "Pending" or not cd("routing_done"):
            st.warning("⚠️ Complete Clinical Evaluation to unlock.")
        else:
            st.subheader("E, F, G — Multidisciplinary, Education & Rehab")
            a_d1, a_d2, a_d3 = st.tabs(["Day 1", "Day 2", "Day 3"])
            
            if sec == "s1":
                with a_d1:
                    banner("E — Multidisciplinary Care", "teal", "🤝")
                    for i, lbl in enumerate(["Swallow assessment by Speech therapist", "Speech and Language therapy", "Physiotherapy consult", "Occupational therapy consult", "Nutritionist Consult (If needed)"]):
                        st.checkbox(lbl, value=od(f"s1_d1_m{i}"), key=f"s1_m{i}_d1_chk", disabled=not can_write("allied"), on_change=lambda i=i: set_od(f"s1_d1_m{i}", st.session_state[f"s1_m{i}_d1_chk"]))
                    
                    banner("F — Family Education & Prognosis", "blue", "👨‍👩‍👧")
                    st.checkbox("Involve family in management and decision making", value=od("s1_d1_f1"), key="s1_f1_d1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s1_d1_f1", st.session_state.s1_f1_d1_chk))
                    
                    # 🐉 PROMINENT DRAGON SCORE CALCULATOR 🐉
                    with st.expander("🐉 DRAGON Score (3-Month Prognosis)", expanded=True):
                        card("Predicts probability of poor functional outcome (mRS 3–6) at 3 months post-IVT.", "info")
                        age = (datetime.date.today() - cd("dob")).days // 365 if cd("dob") else 0
                        door_dt = datetime.datetime.combine(cd("pres_date"), cd("pres_time"))
                        needle_dt = datetime.datetime.combine(cd("pres_date"), cd("tpa_time")) if cd("tpa_time") != datetime.time(0,0) else door_dt
                        onset_dt = datetime.datetime.combine(cd("lkw_date"), cd("lkw_time"))
                        otn_mins = max((needle_dt - onset_dt).total_seconds() / 60, 0) if "IVT" in cd("final_routing") else 0
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"• **Age:** {age} | **NIHSS:** {cd('nihss_baseline',0)} | **Pre-mRS:** {cd('mrs_pre',0)}")
                        with c2:
                            v_dense = st.checkbox("Dense artery / early infarct on CT", value=cd("dragon_dense_artery"), key="drg_dense"); set_cd("dragon_dense_artery", v_dense)
                            v_glu = st.number_input("Glucose (mg/dL)", value=int(cd("dragon_glucose",100)), step=10, key="drg_glu"); set_cd("dragon_glucose", v_glu)
                        
                        if st.button("Calculate DRAGON Score", key="btn_calc_dragon"):
                            d_score = 0
                            if v_dense: d_score += 1
                            if cd("mrs_pre",0) > 1: d_score += 1
                            d_score += (2 if age >= 80 else (1 if age >= 65 else 0))
                            if v_glu > 144: d_score += 1
                            if otn_mins > 90: d_score += 1
                            nihss = cd("nihss_baseline", 0)
                            d_score += (3 if nihss >= 16 else (2 if nihss >= 10 else (1 if nihss >= 5 else 0)))
                            set_cd("dragon_score_final", d_score); set_cd("dragon_calculated", True); st.rerun()
                        
                        if cd("dragon_calculated"):
                            ds = cd("dragon_score_final", 0)
                            prog, color = (("Good (96% favorable)", "success") if ds <= 2 else ("Moderate (~70% favorable)", "warning") if ds <= 4 else ("Poor (~20-30% favorable)", "danger"))
                            st.markdown(f'<div class="kpi-grid">{kpi(str(ds),"DRAGON Score (0-10)","primary")}</div>', unsafe_allow_html=True)
                            card(f"**Prognosis:** {prog}", color)
                            v_counsel = st.checkbox(f"Family counseled on DRAGON prognosis ({ds}/10)", value=od("s1_d1_dragon_counsel"), key="drg_counsel", disabled=not can_write("physician"))
                            set_od("s1_d1_dragon_counsel", v_counsel)

            elif sec == "s2":
                with a_d1:
                    banner("E — Multidisciplinary Care", "teal", "🤝")
                    for i, lbl in enumerate(["Swallow assessment by Speech therapist", "Speech and Language therapy", "Physiotherapy consult", "Occupational therapy consult if needed", "Nutritionist consult (If needed)"]):
                        st.checkbox(lbl, value=od(f"s2_d1_m{i}"), key=f"s2_m{i}_d1_chk", disabled=not can_write("allied"), on_change=lambda i=i: set_od(f"s2_d1_m{i}", st.session_state[f"s2_m{i}_d1_chk"]))
                    banner("F — Family Education", "blue", "👨‍👩‍👧")
                    st.checkbox("Involve family in management and decision making", value=od("s2_d1_f1"), key="s2_f1_d1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_f1", st.session_state.s2_f1_d1_chk))
                    st.checkbox("Communicate 30-day mortality based on NIHSS score", value=od("s2_d1_f2"), key="s2_f2_d1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d1_f2", st.session_state.s2_f2_d1_chk))
                with a_d2:
                    st.checkbox("If NG in place, reassess the need for NG by speech therapist", value=od("s2_d2_m1"), key="s2_m1_d2_chk", disabled=not can_write("allied"), on_change=lambda: set_od("s2_d2_m1", st.session_state.s2_m1_d2_chk))
                    st.checkbox("Counsel family regarding prognosis and clinical condition of family", value=od("s2_d2_f1"), key="s2_f1_d2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d2_f1", st.session_state.s2_f1_d2_chk))
                    st.checkbox("Discharge planning and rehabilitation at 24–48 h", value=od("s2_d2_r1"), key="s2_r1_d2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d2_r1", st.session_state.s2_r1_d2_chk))
                    st.checkbox("Family counselling regarding home care", value=od("s2_d2_r2"), key="s2_r2_d2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d2_r2", st.session_state.s2_r2_d2_chk))
                with a_d3:
                    st.checkbox("If NG in place, reassess the need for NG by speech therapist", value=od("s2_d3_m1"), key="s2_m1_d3_chk", disabled=not can_write("allied"), on_change=lambda: set_od("s2_d3_m1", st.session_state.s2_m1_d3_chk))
                    st.checkbox("Counsel family regarding prognosis and clinical condition of family", value=od("s2_d3_f1"), key="s2_f1_d3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d3_f1", st.session_state.s2_f1_d3_chk))
                    lifestyle_checks("s2_d3")
                    st.checkbox("Confirm disposition: Acute rehab / Home nursing", value=od("s2_d3_r1"), key="s2_r1_d3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s2_d3_r1", st.session_state.s2_r1_d3_chk))

            elif sec == "s3":
                with a_d1:
                    banner("E — Multidisciplinary Care", "teal", "🤝")
                    for i, lbl in enumerate(["Swallow assessment by Speech therapist", "Speech and Language therapy", "Physiotherapy consult", "Occupational therapy consult if needed", "Nutritionist consult (If needed)"]):
                        st.checkbox(lbl, value=od(f"s3_d1_m{i}"), key=f"s3_m{i}_d1_chk", disabled=not can_write("allied"), on_change=lambda i=i: set_od(f"s3_d1_m{i}", st.session_state[f"s3_m{i}_d1_chk"]))
                    banner("F — Family Education", "blue", "👨‍👩‍👧")
                    st.checkbox("Involve family in management and decision making", value=od("s3_d1_f1"), key="s3_f1_d1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_f1", st.session_state.s3_f1_d1_chk))
                    st.checkbox("Communicate 30-day mortality based on NIHSS score", value=od("s3_d1_f2"), key="s3_f2_d1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_f2", st.session_state.s3_f2_d1_chk))
                    st.checkbox("Explain EVT procedure and its outcomes", value=od("s3_d1_f3"), key="s3_f3_d1_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d1_f3", st.session_state.s3_f3_d1_chk))
                with a_d2:
                    st.checkbox("If NG in place, reassess the need for NG by speech therapist", value=od("s3_d2_m1"), key="s3_m1_d2_chk", disabled=not can_write("allied"), on_change=lambda: set_od("s3_d2_m1", st.session_state.s3_m1_d2_chk))
                    st.checkbox("Counsel family regarding prognosis and clinical condition of family", value=od("s3_d2_f1"), key="s3_f1_d2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d2_f1", st.session_state.s3_f1_d2_chk))
                    st.checkbox("Discharge planning and rehabilitation at 24–48 h", value=od("s3_d2_r1"), key="s3_r1_d2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d2_r1", st.session_state.s3_r1_d2_chk))
                    st.checkbox("Family counselling regarding home care", value=od("s3_d2_r2"), key="s3_r2_d2_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d2_r2", st.session_state.s3_r2_d2_chk))
                with a_d3:
                    st.checkbox("If NG in place, reassess the need for NG by speech therapist", value=od("s3_d3_m1"), key="s3_m1_d3_chk", disabled=not can_write("allied"), on_change=lambda: set_od("s3_d3_m1", st.session_state.s3_m1_d3_chk))
                    st.checkbox("Counsel family regarding prognosis", value=od("s3_d3_f1"), key="s3_f1_d3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d3_f1", st.session_state.s3_f1_d3_chk))
                    lifestyle_checks("s3_d3")
                    st.checkbox("Confirm disposition: Acute rehab / Home nursing", value=od("s3_d3_r1"), key="s3_r1_d3_chk", disabled=not can_write("physician"), on_change=lambda: set_od("s3_d3_r1", st.session_state.s3_r1_d3_chk))

    st.markdown("---")
    render_ai_consult_panel(
        phase_key="phase4",
        intro="Dr. AIKEN reviews order appropriateness, flags missing guideline-mandated orders, and advises on complication monitoring.",
        quick_questions=[
            ("📋 Order review?",      "Review my Day 1 orders. Are there any guideline-mandated orders I may have missed?"),
            ("🩺 Complication risk?", "What are the top 3 complications this patient is at risk for in the next 24-48h?"),
            ("🩸 Anticoagulation?",   "Should I anticoagulate this patient? What agent, when, and what monitoring is required?"),
        ],
    )

    st.markdown("---")
    c_prev, c_next = st.columns(2)
    with c_prev:
        if st.button("⬅️ Back to Phase 3", use_container_width=True):
            go_to("Phase 3: Imaging & Routing Gate")
    with c_next:
        if st.button("💾 Save Orders & View Notes ➡️", key="btn_s4_out", use_container_width=True):
            go_to("Phase 5: Daily Rounds & Progress Notes")


# ── PHASE 5 — PROGRESS NOTES ─────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Phase 5: Daily Rounds & Progress Notes":
    page_header("Phase 5: Clinical Progress Notes","Face Sheet & 3-Day Booklet")

    tab_facesheet, tab_notes = st.tabs(["📋 1. Face Sheet (Admission)","📝 2. Daily Progress Notes"])

    # =========================================================================
    # 📋 TAB 1: FACE SHEET (EXACT WORD DOC MATCH)
    # =========================================================================
    with tab_facesheet:
        with st.form("facesheet_form", clear_on_submit=False):
            banner("Stroke Daily Progress Notes — Cover Page","blue","📄")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                v = st.text_input("Day of admission:", value=cd("fs_doa",""), key="fs_doa"); set_cd("fs_doa",v)
            with c2:
                v = st.text_input("Day of stroke:", value=cd("fs_dos",""), key="fs_dos"); set_cd("fs_dos",v)
            with c3:
                v = st.text_input("Diagnosis:", value=cd("assigned_pathway",""), key="fs_dx"); set_cd("fs_dx",v)
            with c4:
                v = st.text_input("Other Diagnoses:", value=cd("fs_odx",""), key="fs_odx"); set_cd("fs_odx",v)

            st.markdown("---")
            c_score1, c_score2, c_score3, c_score4 = st.columns(4)
            with c_score1:
                v = st.text_input("NIHSS On admission:", value=str(cd("nihss_baseline",0)), disabled=True)
            with c_score2:
                v = st.text_input("NIHSS Current:", value=cd("fs_nihss_curr", ""), key="fs_nihss_curr"); set_cd("fs_nihss_curr",v)
            with c_score3:
                v = st.text_input("mRS At baseline:", value=str(cd("mrs_pre",0)), disabled=True)
            with c_score4:
                v = st.text_input("mRS Current:", value=cd("fs_mrs_curr", ""), key="fs_mrs_curr"); set_cd("fs_mrs_curr",v)

            c_tpa1, c_tpa2, c_tpa3, c_tpa4 = st.columns(4)
            with c_tpa1:
                tpa_given = "Yes" if "IVT" in cd("final_routing", "") else "No"
                st.text_input("tPA administered:", value=tpa_given, disabled=True)
            with c_tpa2:
                v = st.text_input("tPA Details:", value=cd("fs_tpa_det", ""), key="fs_tpa_det"); set_cd("fs_tpa_det",v)
            with c_tpa3:
                evt_given = "Yes" if "EVT" in cd("final_routing", "") else "No"
                st.text_input("Thrombectomy:", value=evt_given, disabled=True)
            with c_tpa4:
                v = st.text_input("mTICI Grade:", value=cd("fs_mtici", ""), key="fs_mtici"); set_cd("fs_mtici",v)

            c_dx1, c_dx2 = st.columns(2)
            with c_dx1:
                v = st.text_input("ABCD2 Score (For TIA):", value=cd("fs_abcd2",str(cd("abcd2_score",""))), key="fs_abcd2"); set_cd("fs_abcd2",v)
            with c_dx2:
                toast_opts = ["1) Large-artery atherosclerosis","2) Cardio-embolism","3) Small-vessel occlusion","4) Stroke of other determined etiology","5) Stroke of undetermined etiology"]
                v = st.selectbox("TOAST:", toast_opts, index=toast_opts.index(cd("toast")) if cd("toast") in toast_opts else 4, key="fs_toast"); set_cd("toast",v)

            banner("Risk Factors / Secondary Prevention Workup","teal","🛡️")
            r1, r2, r3 = st.columns([1.2, 1, 1.5])
            with r1:
                st.markdown("**Risk Factor**")
                v1 = st.checkbox("Previous Stroke(s)", value=cd("rf_prev_stroke",False), key="fs_rf1"); set_cd("rf_prev_stroke",v1)
                v2 = st.checkbox("Diabetes Mellitus", value=cd("rf_dm",False), key="fs_rf2"); set_cd("rf_dm",v2)
                v3 = st.checkbox("Hypertension", value=cd("rf_htn",False), key="fs_rf3"); set_cd("rf_htn",v3)
                v4 = st.checkbox("Ischemic Heart Dis.", value=cd("rf_ihd",False), key="fs_rf4"); set_cd("rf_ihd",v4)
                v5 = st.checkbox("Smoking / Tobacco", value=cd("rf_smoking",False), key="fs_rf5"); set_cd("rf_smoking",v5)
            with r2:
                st.markdown("**Onset Details**")
                st.markdown("<br>", unsafe_allow_html=True)
                v_dm_o = st.text_input("Onset (DM):", value=cd("fs_dm_o",""), key="fs_dm_o", label_visibility="collapsed"); set_cd("fs_dm_o",v_dm_o)
                v_htn_o = st.text_input("Onset (HTN):", value=cd("fs_htn_o",""), key="fs_htn_o", label_visibility="collapsed"); set_cd("fs_htn_o",v_htn_o)
            with r3:
                st.markdown("**Values**")
                st.markdown("<br>", unsafe_allow_html=True)
                v_hba1c = st.text_input("HbA1c:", value=cd("fs_hba1c",""), key="fs_hba1c", placeholder="HbA1c %"); set_cd("fs_hba1c",v_hba1c)

            st.markdown("---")
            st.markdown("**Workup Details**")
            c_l1, c_l2 = st.columns(2)
            with c_l1:
                v = st.text_input("Lipid Profile (LDL, HDL, TG, Total Chol):", value=cd("fs_lipids",""), key="fs_lipids"); set_cd("fs_lipids",v)
                v = st.text_input("Echocardiography (EF%, Clot Y/N, Other findings):", value=cd("fs_echo",""), key="fs_echo"); set_cd("fs_echo",v)
                v = st.text_input("Carotid Doppler:", value=cd("fs_carotid",""), key="fs_carotid"); set_cd("fs_carotid",v)
                v = st.text_input("CTA Carotids/Brain:", value=cd("fs_cta",""), key="fs_cta"); set_cd("fs_cta",v)
            with c_l2:
                v = st.text_input("Holter Monitoring:", value=cd("fs_holter",""), key="fs_holter"); set_cd("fs_holter",v)
                v = st.text_input("Other work up (TSH):", value=cd("fs_other",""), key="fs_other"); set_cd("fs_other",v)
                v = st.text_input("Young Stroke (Young Screen):", value=cd("fs_young",""), key="fs_young"); set_cd("fs_young",v)

            if st.form_submit_button("💾 Save Face Sheet"):
                st.toast("Face Sheet saved!", icon="✅")

    # =========================================================================
    # 📝 TAB 2: DAILY PROGRESS NOTES (EXACT WORD DOC MATCH)
    # =========================================================================
    with tab_notes:
        card("Progress notes follow the Shifa Stroke Daily Progress Note structure (Days 1–3).","info")

        with st.expander("🔄 Auto-Generate SBAR Shift Handoff (For Shift Change)", expanded=False):
            banner("SBAR Shift Sign-Out", "blue", "📋")
            card("Instantly generates a structured handoff for the incoming on-call team.", "info")
            sc = cd("nihss_baseline", 0)
            sbar_text = f"""SITUATION:
{cd('pat_name', '[Patient]')} is a {(datetime.date.today() - cd("dob")).days // 365 if cd("dob") else '?'}y/o {cd('sex', '')} admitted under {cd('consultant', '[Consultant]')} for Acute Ischemic Stroke.
Current Pathway: {cd('final_routing', 'Pending')}
Current NIHSS: {cd('nihss_dc') or cd('nihss_24h') or cd('nihss_2h') or sc} (Baseline was {sc})

BACKGROUND:
LKW: {cd('lkw_date')} at {cd('lkw_time')}. Treatment: {"Received Thrombolysis" if "IVT" in cd('final_routing', '') else "Non-thrombolysis pathway."}
Imaging: {cd('ct_result')}, ASPECTS {cd('ncct_aspects', 'N/A')}. LVO: {cd('cta_lvo')}.
Key Risk Factors: {"HTN " if cd('rf_htn') else ""}{"DM " if cd('rf_dm') else ""}{"IHD " if cd('rf_ihd') else ""}{"Prev Stroke" if cd('rf_prev_stroke') else ""}

ASSESSMENT & RECOMMENDATION:
Target BP is {"< 180/105" if "IVT" in cd('final_routing','') else "< 220/120"}. Latest BP: {cd('bp_sys', '?')}/{cd('bp_dia', '?')}.
Call {cd('consultant', 'attending')} if NIHSS worsens by >= 4 points or BP exceeds threshold."""
            st.text_area("Copy/Paste into WhatsApp/Hospital Chat:", value=sbar_text, height=250)

        banner("Smart Progress Note Generator","purple","✨")
        col_soap, col_ai_soap, col_family = st.columns(3)
        with col_soap:
            if st.button("📝 Auto-Draft SOAP Note", key="btn_draft", use_container_width=True):
                st.session_state["_soap_draft"] = generate_soap_note()
        with col_ai_soap:
            if st.button("🧠 AI Attending SOAP Note", key="btn_ai_soap", use_container_width=True):
                ctx = build_clinical_context()
                prompt = f"PATIENT CONTEXT:\n{ctx}\n\nGenerate an attending-quality SOAP note for this stroke patient. Format: SUBJECTIVE, OBJECTIVE, ASSESSMENT, PLAN, ATTENDING REMARKS."
                with st.spinner("🧠 Dr. SHIFA drafting attending SOAP note..."):
                    ai_soap = call_ai_consultant([{"role":"user","content":prompt}], max_tokens=1100)
                set_cd("ai_soap_generated",True); set_cd("ai_soap_text", ai_soap); st.rerun()
        with col_family:
            if st.button("🗣️ Family Summary (Bilingual)", key="btn_layman", use_container_width=True):
                layman = f"**Family Update for {cd('pat_name')}:**\nPatient had a stroke. They are in the Stroke Unit for 24-48h strict observation. Do NOT give food/water until swallowing is tested.\n**اردو:** فالج کا حملہ ہوا ہے۔ 24-48 گھنٹے سخت نگرانی میں ہیں۔ براہ کرم انہیں منہ سے کچھ کھانے پینے کو نہ دیں۔"
                set_cd("layman_text",layman); set_cd("layman_summary_generated",True)

        if cd("ai_soap_generated") and cd("ai_soap_text"):
            st.markdown("---")
            edited_ai = st.text_area("Review & Edit AI SOAP Draft:", value=cd("ai_soap_text"), height=380, key="ai_soap_edit")
            set_cd("ai_soap_text",edited_ai)
            c_a, c_d = st.columns(2)
            with c_a:
                if st.button("✅ Approve & Lock", key="btn_approve_ai"): set_cd("ai_soap_locked",True); card("Note Locked","success")
            with c_d:
                if st.button("🗑️ Discard", key="btn_discard_ai"): set_cd("ai_soap_generated",False); st.rerun()

        if "_soap_draft" in st.session_state:
            st.text_area("Template Auto-Draft:", value=st.session_state["_soap_draft"], height=280)

        if cd("layman_summary_generated"):
            st.markdown("---")
            card(cd("layman_text"),"info","👨‍👩‍👧")
            st.download_button("🖨️ Download Family Handout", data=cd("layman_text"), file_name=f"Family_{cd('mrn')}.txt", mime="text/plain")

        st.markdown("---")
        
        # =========================================================================
        # 📝 NEW PROGRESS NOTE FORM (EXACT WORD DOC MATCH)
        # =========================================================================
        with st.expander("➕ Add New Progress Note (Detailed Booklet Format)", expanded=False):
            with st.form("new_progress_note_form", clear_on_submit=True):
                
                # Header Information
                c1, c2, c3, c4 = st.columns(4)
                with c1: day_num = st.selectbox("Day of Note:",["1","2","3","4","5+"], key="pn_day_select")
                with c2: pn_date = st.date_input("Date:", value=datetime.date.today(), key="pn_date")
                with c3: pn_time = st.time_input("Time:", value=(datetime.datetime.utcnow()+datetime.timedelta(hours=5)).time(), key="pn_time")
                with c4: pn_author = st.text_input("Author (Resident/MO):", value=cd("resident") or "", key="pn_auth")

                # 1. Clinical Details (Nursing)
                banner("Clinical Details","teal","🛏️")
                c_cd1, c_cd2, c_cd3 = st.columns(3)
                with c_cd1:
                    pn_bedsore = st.text_input("Bed sore:", key="pn_bedsore")
                    pn_bowel = st.text_input("Bowel Movement:", key="pn_bowel")
                    pn_swallowing = st.text_input("Swallowing:", key="pn_swallowing")
                with c_cd2:
                    pn_cath = st.text_input("Urinary Cath:", key="pn_cath")
                    pn_io = st.text_input("Input / Output:", key="pn_io")
                    pn_oob = st.text_input("Out of bed:", key="pn_oob")
                with c_cd3:
                    pn_asp = st.text_input("Aspiration:", key="pn_asp")
                    pn_dvt = st.text_input("DVT:", key="pn_dvt")
                    pn_cellulitis = st.text_input("Cellulitis:", key="pn_cellulitis")

                # Vitals
                st.markdown("**Vitals**")
                v1, v2, v3, v4 = st.columns(4)
                with v1: pn_bp = st.text_input("BP (mmHg):", key="pn_bp")
                with v2: pn_bp_max = st.text_input("BP Max:", key="pn_bp_max"); pn_bp_min = st.text_input("BP Min:", key="pn_bp_min")
                with v3: pn_hr = st.text_input("HR (/min):", key="pn_hr"); pn_rr = st.text_input("RR (/min):", key="pn_rr")
                with v4: pn_tmax = st.text_input("TMax:", key="pn_tmax"); pn_spo2 = st.text_input("SpO2:", key="pn_spo2"); pn_bsr = st.text_input("BSR (mg/dL):", key="pn_bsr")

                # 2. Examination
                banner("Examination","purple","🔍")
                st.markdown("**GCS**")
                g1, g2, g3 = st.columns(3)
                with g1: pn_gcs_e = st.text_input("GCS E:", key="pn_gcs_e")
                with g2: pn_gcs_m = st.text_input("GCS M:", key="pn_gcs_m")
                with g3: pn_gcs_v = st.text_input("GCS V:", key="pn_gcs_v")
                
                e1, e2, e3 = st.columns(3)
                with e1:
                    pn_speech = st.text_input("Speech:", key="pn_speech")
                    pn_pupils = st.text_input("Pupils:", key="pn_pupils")
                    pn_eom = st.text_input("EOM:", key="pn_eom")
                    pn_gaze = st.text_input("Gaze Restriction:", key="pn_gaze")
                    pn_vf = st.text_input("Visual Fields:", key="pn_vf")
                with e2:
                    pn_face = st.text_input("Face:", key="pn_face")
                    pn_tongue = st.text_input("Tongue:", key="pn_tongue")
                    pn_power_grip = st.text_input("Power (Grip):", key="pn_power_grip")
                    pn_power_drift = st.text_input("Power (Drift):", key="pn_power_drift")
                    pn_reflexes = st.text_input("Reflexes:", key="pn_reflexes")
                with e3:
                    pn_plantars = st.text_input("Plantars:", key="pn_plantars")
                    pn_cereb = st.text_input("Cerebellar:", key="pn_cereb")
                    pn_sens = st.text_input("Sensations:", key="pn_sens")
                    pn_somi = st.text_input("SOMI:", key="pn_somi")
                    pn_bruit = st.text_input("Carotid Bruit:", key="pn_bruit")
                
                c_other, c_nihss = st.columns([3, 1])
                with c_other: pn_exam_other = st.text_input("Other Exam Findings:", key="pn_exam_other")
                with c_nihss: pn_nihss = st.text_input("NIHSS:", key="pn_nihss_val")

                # 3. Systemic Examination
                st.markdown("**Systemic Examination**")
                s1, s2 = st.columns(2)
                with s1:
                    pn_cvs = st.text_input("CVS:", key="pn_cvs")
                    pn_resp = st.text_input("Resp:", key="pn_resp")
                with s2:
                    pn_abd = st.text_input("Abdomen:", key="pn_abd")
                    pn_sys_other = st.text_input("Other Systemic:", key="pn_sys_other")
                pn_imaging = st.text_area("Imaging findings:", key="pn_imaging", height=68)

                # 4. Investigations Table
                banner("Investigations","blue","🧪")
                i1, i2, i3, i4 = st.columns(4)
                with i1:
                    pn_wbc = st.text_input("WBC (/µL):", key="pn_wbc")
                    pn_hb = st.text_input("Hb (g/dL):", key="pn_hb")
                    pn_plts = st.text_input("Plts (/µL):", key="pn_plts")
                with i2:
                    pn_crp = st.text_input("CRP (mg/dL):", key="pn_crp")
                    pn_lfts = st.text_input("LFTs:", key="pn_lfts")
                    pn_ptinr = st.text_input("PT/INR:", key="pn_ptinr")
                with i3:
                    pn_na = st.text_input("Na (mEq/L):", key="pn_na")
                    pn_cr = st.text_input("Creatinine:", key="pn_cr")
                with i4:
                    pn_cult = st.text_input("Culture(s):", key="pn_cult")
                    pn_inv_other = st.text_input("Others:", key="pn_inv_other")

                # 5. Meds, Consults, Assessment, Plan
                banner("Plan & Summary","grey","📝")
                pn_meds = st.text_area("Medications:", key="pn_meds", height=68)
                pn_consults = st.text_area("Other Consultations:", key="pn_consults", height=68)
                pn_assess = st.text_area("Assessment:", key="pn_assess_main", height=68)
                pn_plan = st.text_area("Plan:", key="pn_plan_main", height=68)

                # 6. Rehabilitation & Screening
                banner("Rehabilitation & Screening","green","🦽")
                r_pt, r_st, r_ot = st.columns(3)
                with r_pt:
                    pn_pt_na = st.checkbox("PT Not Applicable", key="pn_pt_na")
                    pn_pt_plan = st.text_area("Physical Therapy Plan:", disabled=pn_pt_na, key="pn_pt_plan")
                with r_st:
                    pn_st_na = st.checkbox("ST Not Applicable", key="pn_st_na")
                    pn_st_plan = st.text_area("Speech Therapy Plan:", disabled=pn_st_na, key="pn_st_plan")
                with r_ot:
                    pn_ot_na = st.checkbox("OT Not Applicable", key="pn_ot_na")
                    pn_ot_plan = st.text_area("Occupational Therapy Plan:", disabled=pn_ot_na, key="pn_ot_plan")

                # 7. Discharge & Attending Remarks
                banner("Discharge & Attending","grey","🏥")
                c_dc, c_att = st.columns(2)
                with c_dc: pn_dc_days = st.text_input("Discharge expected in (days):", key="pn_dc_days")
                with c_att: pn_attending = st.text_input("Attending Name/Sign:", key="pn_attending_name")
                
                pn_attending_note = st.text_area("Attending Remarks / Note:", key="pn_attending_note", height=68)

                if st.form_submit_button("💾 Save Comprehensive Progress Note"):
                    if not pn_author.strip():
                        st.error("Author name is required.")
                    else:
                        note = {
                            "date":str(pn_date),"time":str(pn_time),"author":pn_author,"day":day_num,
                            "vitals":f"BP {pn_bp} (Max:{pn_bp_max}, Min:{pn_bp_min}) | HR {pn_hr} | RR {pn_rr} | TMax {pn_tmax} | SpO₂ {pn_spo2} | BSR {pn_bsr}",
                            "details":f"Bedsore:{pn_bedsore} | Bowel:{pn_bowel} | Swallow:{pn_swallowing} | Cath:{pn_cath} | I/O:{pn_io} | OOB:{pn_oob} | Asp:{pn_asp} | DVT:{pn_dvt} | Cellulitis:{pn_cellulitis}",
                            "exam":f"GCS: E{pn_gcs_e}M{pn_gcs_m}V{pn_gcs_v} | Speech: {pn_speech} | Pupils: {pn_pupils} | EOM/Gaze/VF: {pn_eom}/{pn_gaze}/{pn_vf} | Face/Tongue: {pn_face}/{pn_tongue} | Power/Reflex/Plantar: {pn_power_grip}/{pn_reflexes}/{pn_plantars} | NIHSS: {pn_nihss}",
                            "systemic":f"CVS:{pn_cvs} | Resp:{pn_resp} | Abd:{pn_abd} | Imaging: {pn_imaging}",
                            "labs":f"WBC:{pn_wbc} | Hb:{pn_hb} | Plt:{pn_plts} | PT/INR:{pn_ptinr} | Cr:{pn_cr}",
                            "assessment":pn_assess, "plan":pn_plan, "meds":pn_meds,
                            "rehab":f"PT: {'N/A' if pn_pt_na else pn_pt_plan} | ST: {'N/A' if pn_st_na else pn_st_plan} | OT: {'N/A' if pn_ot_na else pn_ot_plan}",
                            "dc_days":pn_dc_days, "attending": pn_attending, 
                            "attending_note": pn_attending_note, # <-- New Field Saved Here
                            "role":current_role(),
                        }
                        st.session_state.progress_notes.append(note)
                        st.toast("Comprehensive Progress note saved!", icon="✅")
                        st.rerun()

        st.markdown("---")
        st.subheader(f"📝 Saved Progress Notes ({len(st.session_state.progress_notes)})")
        for i, note in enumerate(reversed(st.session_state.progress_notes)):
            with st.expander(f"Day {note['day']} — {note['date']} {note['time']} | {note['author']}"):
                for label, field in [("Vitals","vitals"),("Clinical Details","details"),("Exam","exam"),("Systemic","systemic"),("Labs","labs"),("Assessment","assessment"),("Plan","plan"),("Rehab","rehab"),("Medications","meds")]:
                    if field in note and note[field]:
                        st.markdown(f"**{label}:** {note[field]}")
                
                # --- NEW DISPLAY LOGIC FOR ATTENDING NOTE ---
                if note.get("attending_note"):
                    st.markdown(f"**Attending Remarks:** {note['attending_note']}")
                    
                if note.get("dc_days"):
                    st.markdown(f"**Discharge in:** {note['dc_days']} days | **Attending Name/Sign:** {note.get('attending','')}")
                st.caption(f"Entered by: {note['role']} — {note['author']}")

        render_ai_consult_panel(
            phase_key="phase5",
            intro="Dr. SHIFA can draft attending-quality notes, advise on clinical trajectory, and generate family communication.",
            quick_questions=[
                ("📋 Discharge plan?", "Is this patient ready for discharge? What criteria still need to be met?"),
                ("🎯 Key priorities?", "What are the 3 most important clinical decisions I need to make in the next 24h?"),
                ("📊 Explain outcome?","Help me explain this patient's stroke outcome and prognosis to the family in plain language."),
            ],
        )


# ── VARIANCE AUDIT ─────────────────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Variance Audit":
    page_header("JCI Variance Tracking & Audit Dashboard")

    if not can_write("admin"):
        banner("Read-Only — Only Admin/Audit role can resolve variances.","grey","🔒")

    vl         = st.session_state.variance_log
    total      = len(vl)
    unresolved = sum(1 for v in vl if not v["resolved"])
    resolved   = total - unresolved

    st.markdown(
        f'<div class="kpi-grid">'
        f'{kpi(str(total),"Total Variances","primary")}'
        f'{kpi(str(unresolved),"Open / Unresolved","danger" if unresolved else "success")}'
        f'{kpi(str(resolved),"Resolved","success")}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if not vl:
        card("✅ No variances logged. All mandatory orders completed.","success")
    else:
        st.subheader("📋 Variance Log")
        for idx, v in enumerate(vl):
            status_icon = "✅" if v["resolved"] else "⚠️"
            st.markdown(
                f'<div class="card card-{"success" if v["resolved"] else "warning"}">'
                f'<b>{status_icon} [{v["timestamp"]}]</b> — Patient: <b>{v["patient"]}</b> | '
                f'Section: {v["section"]} | Day: {v["day"]} | Item: {v["item"]}<br>'
                f'Reason: {v["reason"]} | Entered by: {v["user"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
            if not v["resolved"] and can_write("admin"):
                if st.button("✅ Mark as Resolved", key=f"resolve_{idx}"):
                    st.session_state.variance_log[idx]["resolved"] = True; st.rerun()

        if can_write("admin") and vl:
            st.markdown("---")
            banner("🤖 AI-Assisted Root Cause Analysis","ai","🧠")
            if st.button("🧠 Generate AI RCA Report", key="btn_ai_rca", use_container_width=True):
                sections = [v["section"] for v in vl]
                most_common = max(set(sections), key=sections.count)
                prompt = f"""
JCI accreditation consultant reviewing variance data for a stroke unit.

VARIANCE SUMMARY:
- Total protocol deviations: {total}
- Open/unresolved: {unresolved}
- Most frequent section: {most_common}
- Variance items: {json.dumps([{"section":v["section"],"item":v["item"],"reason":v["reason"]} for v in vl], default=str)}

Provide:
1. ROOT CAUSE ANALYSIS: What systemic issues are indicated?
2. PRIMARY BOTTLENECK: Which phase/process has highest risk?
3. IMMEDIATE ACTIONS: 3 specific, actionable steps to address today
4. PROCESS IMPROVEMENTS: 3 recommendations to prevent recurrence
5. JCI COMPLIANCE RISK: Risk to JCI accreditation and what must be documented?
"""
                with st.spinner("🧠 Dr. SHIFA generating RCA report..."):
                    rca_result = call_ai_consultant([{"role":"user","content":prompt}], max_tokens=800)
                st.session_state.ai_phase_cache["rca_result"] = rca_result
                st.rerun()

            if "rca_result" in st.session_state.ai_phase_cache:
                st.markdown(
                    f'<div class="ai-bubble-assistant"><b style="color:#4C1D95;">🧠 Dr. SHIFA — RCA Report:</b><br><br>'
                    f'{st.session_state.ai_phase_cache["rca_result"]}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        if can_write("admin"):
            dtn_mins, dtn_status = get_dtn_status()
            bundle = {
                "generated": (datetime.datetime.utcnow()+datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M PKT"),
                "patient": {"mrn":cd("mrn"),"name":cd("pat_name"),"consultant":cd("consultant")},
                "pathway": {"assigned":cd("assigned_pathway"),"routing":cd("final_routing"),
                            "dtn_mins":round(dtn_mins,0) if dtn_mins else None,"dtn_met":dtn_status=="ok" if dtn_status else None},
                "scores":  {"nihss_baseline":cd("nihss_baseline",0),"nihss_2h":cd("nihss_2h"),"nihss_24h":cd("nihss_24h"),
                            "aspects":cd("ncct_aspects"),"dragon":cd("dragon_score_final"),"sedan":cd("sedan_score_final"),
                            "mrs_pre":cd("mrs_pre",0),"mrs_discharge":cd("mrs_discharge",0)},
                "variance_log": vl,
                "guideline": "AHA/ASA 2026 | JCI Standards | FM-MSA-429 Rev:02",
            }
            export_str = json.dumps(bundle, indent=2, default=str)
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button("⬇️ Download Full Audit Bundle (JSON)", data=export_str,
                                   file_name=f"JCI_audit_{cd('mrn','unknown')}_{datetime.date.today()}.json",
                                   mime="application/json", key="dl_full_bundle")
            with col_b:
                txt_summary = (
                    f"JCI AUDIT SUMMARY — Shifa International Hospitals\nFM-MSA-429 Rev:02 | {bundle['generated']}\n\n"
                    f"PATIENT: {cd('pat_name')} | MRN: {cd('mrn')}\n"
                    f"PATHWAY: {cd('assigned_pathway')}\n"
                    f"DTN: {f'{dtn_mins:.0f} min ({dtn_status.upper()})' if dtn_mins else 'N/A'}\n"
                    f"NIHSS: {cd('nihss_baseline',0)} baseline → {cd('nihss_24h','—')} at 24h\n"
                    f"VARIANCES: {total} total, {unresolved} unresolved\n"
                )
                st.download_button("⬇️ Download Summary (TXT)", data=txt_summary,
                                   file_name=f"JCI_summary_{cd('mrn','unknown')}_{datetime.date.today()}.txt",
                                   mime="text/plain", key="dl_summary_txt")


# ═══════════════════════════════════════════════════════════════════════════
# AI VASCULAR NEUROLOGIST SCREEN
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.ui["screen"] == "🧠 AI Vascular Neurologist":
    page_header("🧠 Dr. SHIFA — AI Vascular Neurologist","AHA/ASA 2026 | Clinical Decision Support")

    api_ok = bool(_get_api_key())

    st.markdown(
        f"""<div class="ai-header-bar" style="margin-bottom:20px;">
          <span style="font-size:2rem;">🧠</span>
          <div>
            <div style="font-weight:900;font-size:1.2rem;">Dr. SHIFA</div>
            <div style="font-size:0.8rem;opacity:0.85;">AI Knowledge Expert in Neurology | Vascular Neurologist Consultant</div>
            <div style="font-size:0.72rem;opacity:0.7;">AHA/ASA 2026 | ESOC 2024 | Landmark Trials | Gemini {GEMINI_MODEL}</div>
          </div>
          <div style="margin-left:auto;text-align:right;">
            <div class="{"ai-status-online" if api_ok else "ai-status-offline"}">
              {"● ONLINE — Ready to consult" if api_ok else "● OFFLINE — Configure GEMINI_API_KEY"}
            </div>
            <div style="font-size:0.65rem;opacity:0.7;margin-top:4px;">Patient: {cd("pat_name") or "None loaded"}</div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    if not api_ok:
        card(
            "**Dr. SHIFA is offline.** Configure your Gemini API key to enable AI features.\n\n"
            "**Setup:** Create `.streamlit/secrets.toml` in your project directory with:\n"
            "```\nGEMINI_API_KEY = 'AIza...'\n```",
            "warning",
        )

    # Handle pre-loaded question from sidebar
    pending_q = st.session_state.pop("sb_ai_pending_q", None)
    if pending_q and api_ok:
        ctx = build_clinical_context()
        st.session_state.ai_chat_history.append({
            "role":"user","content":f"PATIENT CONTEXT:\n{ctx}\n\nQUESTION: {pending_q}","display":pending_q
        })
        with st.spinner("🧠 Dr. SHIFA is analyzing..."):
            response = call_ai_consultant(
                [{"role":m["role"],"content":m["content"]} for m in st.session_state.ai_chat_history]
            )
        st.session_state.ai_chat_history.append({"role":"assistant","content":response,"display":response})
        st.rerun()

    # ── FIX: Two-column layout with proper spacing ──
    col_chat, col_lib = st.columns([3,1])

    with col_lib:
        st.markdown("#### 📚 Question Library")
        st.caption("Click any question to send it to Dr. SHIFA with full patient context.")

        question_library = {
            "🚨 Acute Phase": [
                ("🛡️ IVT safety check",  "Perform a complete IVT safety gate check for this patient, going through every criterion."),
                ("⚕️ EVT eligibility",   "Is this patient EVT-eligible? Apply DAWN, DEFUSE-3, and standard criteria."),
                ("🧠 Vascular territory","What vascular territory does this NIHSS pattern suggest and why?"),
                ("⚡ Next critical step","What is the single most important action to take right now?"),
                ("🩸 BP management",     "What exact BP target and drug should I use for this patient right now?"),
            ],
            "💊 Pharmacology": [
                ("💉 Tenecteplase dose","What is the correct Tenecteplase dose, administration technique, and 24h monitoring protocol?"),
                ("💊 Antihypertensive", "What antihypertensive should I use and at what dose? Calculate for this patient."),
                ("⚖️ DAPT vs anticoag", "Should this patient be on DAPT or anticoagulation? Which agent and why?"),
                ("💊 Statin loading",   "What statin and dose is recommended? When should I start?"),
            ],
            "📋 Ward Management": [
                ("⚠️ Complication risk","What are the top 3 complications this patient is at risk for in the next 24h?"),
                ("🚨 sICH recognition", "How do I recognize symptomatic ICH in this patient? What are the warning signs?"),
                ("🏥 Discharge criteria","Is this patient ready for discharge? What criteria remain unmet?"),
                ("🦽 Rehab plan",       "Generate a comprehensive rehabilitation plan for this patient."),
            ],
            "🛡️ Secondary Prevention": [
                ("🛡️ Sec. prevention",  "Generate a complete, evidence-based secondary prevention plan for this patient."),
                ("⏱️ Anticoag timing",  "When should I start anticoagulation? Apply the 1-3-6-12 rule."),
                ("❤️ AF management",    "What is the anticoagulation strategy for AF-related stroke in this patient?"),
                ("📉 Lipid targets",    "What are the LDL targets and statin strategy for secondary prevention?"),
            ],
            "👨‍👩‍👧 Family Communication": [
                ("🗣️ Explain prognosis","Help me explain this patient's prognosis to the family in plain, compassionate language."),
                ("🧠 Explain stroke",   "How do I explain what a stroke is to the family in simple terms?"),
                ("📈 Recovery expect.", "What realistic recovery expectations should I set with the family?"),
            ],
        }

        for category, questions in question_library.items():
            with st.expander(category, expanded=False):
                for label, question in questions:
                    if st.button(label, key=f"lib_{label}", use_container_width=True):
                        if api_ok:
                            ctx = build_clinical_context()
                            st.session_state.ai_chat_history.append({
                                "role":"user",
                                "content":f"PATIENT CONTEXT:\n{ctx}\n\nQUESTION: {question}",
                                "display":f"📚 [{label}] {question}"
                            })
                            with st.spinner("🧠 Dr. SHIFA is analyzing..."):
                                response = call_ai_consultant(
                                    [{"role":m["role"],"content":m["content"]} for m in st.session_state.ai_chat_history]
                                )
                            st.session_state.ai_chat_history.append({"role":"assistant","content":response,"display":response})
                            st.rerun()
                        else:
                            st.warning("Configure API key first.")

        st.markdown("---")
        if st.button("🗑️ Clear Full Chat History", key="clear_all_chat", use_container_width=True):
            st.session_state.ai_chat_history = []; st.rerun()

        if cd("pat_name"):
            st.markdown("---")
            st.markdown("#### 🏥 Patient Context")
            sc = cd("nihss_baseline",0)
            sev, mort, _ = nihss_severity(sc) if cd("nihss_calculated") else ("—","—","neutral")
            st.markdown(
                f'<div style="background:rgba(76,29,149,0.08);border-radius:8px;padding:10px;font-size:0.78rem;">'
                f'<b>{cd("pat_name")}</b> | MRN: {cd("mrn")}<br>'
                f'NIHSS: {sc} ({sev})<br>'
                f'Pathway: {cd("assigned_pathway")}<br>'
                f'LKW: {cd("time_since_lkw_hrs",0):.1f}h<br>'
                f'CTA: {cd("cta_lvo")}'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_chat:
        st.markdown("#### 💬 Consultation Chat")

        # Chat history
        history_container = st.container()
        with history_container:
            if not st.session_state.ai_chat_history:
                st.markdown(
                    '<div class="card card-ai" style="text-align:center;padding:30px;">'
                    '<div style="font-size:2rem;">🧠</div>'
                    '<div style="font-weight:800;font-size:1.1rem;color:#4C1D95;margin:8px 0;">Dr. SHIFA is ready to consult</div>'
                    '<div style="font-size:0.85rem;color:#5B21B6;">Type a question below or select from the library →<br>'
                    'All responses are grounded in AHA/ASA 2026 guidelines and your patient\'s specific clinical data.</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                for msg in st.session_state.ai_chat_history:
                    display_text = msg.get("display", msg["content"])
                    if "PATIENT CONTEXT:" in display_text:
                        display_text = display_text.split("QUESTION:")[-1].strip()
                    if msg["role"] == "user":
                        st.markdown(
                            f'<div class="ai-bubble-user">🩺 <b>You:</b> {display_text}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div class="ai-bubble-assistant">🧠 <b style="color:#4C1D95;">Dr. SHIFA:</b><br><br>{display_text}</div>',
                            unsafe_allow_html=True,
                        )

        # ── FIX: Chat input in its own styled container with top margin ──
        st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
        col_input, col_send = st.columns([5,1])
        with col_input:
            user_question = st.text_area(
                "Ask Dr. SHIFA:",
                key="ai_main_input",
                height=90,
                placeholder="e.g., 'My patient's NIHSS jumped from 6 to 14 at 3h post-IVT — what do I do?'",
                label_visibility="collapsed",
            )
        with col_send:
            st.markdown("<br>", unsafe_allow_html=True)
            send_clicked = st.button("Send 🧠", key="ai_send_main", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if send_clicked and user_question.strip():
            if not api_ok:
                st.warning("Configure your Gemini API key to use Dr. SHIFA.")
            else:
                ctx = build_clinical_context()
                st.session_state.ai_chat_history.append({
                    "role":"user",
                    "content":f"PATIENT CONTEXT:\n{ctx}\n\nQUESTION: {user_question}",
                    "display":user_question,
                })
                with st.spinner("🧠 Dr. SHIFA is thinking..."):
                    response = call_ai_consultant(
                        [{"role":m["role"],"content":m["content"]} for m in st.session_state.ai_chat_history],
                        max_tokens=1000,
                    )
                st.session_state.ai_chat_history.append({"role":"assistant","content":response,"display":response})
                st.rerun()

        # Tips expander BELOW the input — separate block with top margin
        st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
        with st.expander("💡 Tips for best results", expanded=False):
            st.markdown("""
**Make your questions specific:**
- ✅ "My 72yo patient on apixaban has NIHSS 8 — can I give Tenecteplase?"
- ❌ "Can I give tPA?"

**Dr. SHIFA knows your patient's data** — you don't need to repeat it. Just ask the clinical question.

**Multi-turn conversation is supported** — Dr. SHIFA remembers the conversation context.

**Model in use:** `{}`
            """.format(GEMINI_MODEL))
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("⚠️ Dr. SHIFA provides clinical decision **support** grounded in AHA/ASA 2026. All clinical decisions are the responsibility of the attending physician.")


# ── EMERGENCY: BLEEDING ─────────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Emergency: Bleeding":
    page_header("🚨 EMERGENCY PROTOCOL", "Symptomatic Intracranial Bleeding (sICH)")
    st.markdown("""
    <div style="background:#7F1D1D; color:white; padding:20px; border-radius:10px;">
        <h2 style="color:white; margin-top:0;">🛑 IMMEDIATE ACTIONS (AHA/ASA Table 4)</h2>
        <ol style="font-size:1.1rem; line-height:1.8;">
            <li><b>STOP Tenecteplase/Alteplase</b> immediately (if still being pushed).</li>
            <li>Send STAT labs: <b>CBC, PT (INR), aPTT, fibrinogen level, type & cross-match</b>.</li>
            <li>Order STAT <b>Non-enhanced head NCCT</b>.</li>
            <li>Call <b>Hematology and Neurosurgery</b> STAT.</li>
        </ol>
        <hr style="border-color:rgba(255,255,255,0.3);">
        <h3 style="color:#FCA5A5;">💉 REVERSAL AGENTS</h3>
        <ul>
            <li><b>Cryoprecipitate (includes Factor VIII):</b> 10 U infused over 10–30 min. (Target fibrinogen ≥150 mg/dL).</li>
            <li><b>Tranexamic acid (TXA):</b> 1000 mg IV infused over 10 min <b>OR</b><br>
            <b>ε-aminocaproic acid:</b> 4–5 g over 1 h, followed by 1 g IV until bleeding controlled.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⬅️ Return to Patient Dashboard"):
        navigate_to("🏠 Dashboard"); st.rerun()


# ── EMERGENCY: ANGIOEDEMA ───────────────────────────────────────────────
elif st.session_state.ui["screen"] == "Emergency: Angioedema":
    page_header("🚨 EMERGENCY PROTOCOL", "Orolingual Angioedema")
    st.markdown("""
    <div style="background:#7F1D1D; color:white; padding:20px; border-radius:10px;">
        <h2 style="color:white; margin-top:0;">🛑 IMMEDIATE ACTIONS (AHA/ASA Table 5)</h2>
        <ol style="font-size:1.1rem; line-height:1.8;">
            <li><b>MAINTAIN AIRWAY:</b> Awake fiberoptic intubation is optimal. Edema involving larynx, palate, or floor of mouth with rapid progression (&lt; 30 min) poses high intubation risk.</li>
            <li><b>Hold all ACE Inhibitors</b> immediately.</li>
        </ol>
        <hr style="border-color:rgba(255,255,255,0.3);">
        <h3 style="color:#FCA5A5;">💉 MEDICAL MANAGEMENT</h3>
        <ul>
            <li><b>IV Methylprednisolone:</b> 125 mg IV.</li>
            <li><b>IV Diphenhydramine:</b> 50 mg IV.</li>
            <li><b>Ranitidine 50 mg IV</b> OR <b>Famotidine 20 mg IV</b>.</li>
            <li><i>If further increase in edema:</i> Administer <b>0.1% epinephrine</b> (1 mg/mL) 0.3 mL subcutaneously OR by nebulizer (0.5 mg/mL).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ Return to Patient Dashboard"):
        navigate_to("🏠 Dashboard")
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.8rem; padding: 20px 0;'>"
    "© 2026 Shifa International Hospitals Ltd. | AI-Assisted Stroke EMR | "
    "For authorized clinical personnel only."
    "</div>",
    unsafe_allow_html=True
)