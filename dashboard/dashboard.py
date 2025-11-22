import os
import sys

import streamlit as st
from sqlalchemy import create_engine, text

# --- Make sure we can import app.config ---
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.config import settings  # noqa: E402

# --- CUSTOM CSS THEME ---
st.markdown("""
<style>
    /* Global Color Variables */
    :root {
        --primary-green: #046307;
        --primary-dark: #034b05;
        --primary-light: #0a8a0d;
        --accent-green: #10b817;
        --success-green: #28a745;
        --background-light: #F5F9F6;
        --background-white: #FFFFFF;
        --text-dark: #0D1B0D;
        --text-muted: #5a6d5b;
        --border-light: #d1e7d3;
        --shadow-green: rgba(4, 99, 7, 0.1);
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #F5F9F6 0%, #FFFFFF 100%);
    }
    
    /* Headers & Titles */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-green) !important;
        font-weight: 700 !important;
    }
    
    .stTitle {
        color: var(--primary-green) !important;
        border-bottom: 3px solid var(--primary-green);
        padding-bottom: 12px;
    }
    
    /* Primary Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px var(--shadow-green) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-green) 100%) !important;
        box-shadow: 0 6px 20px rgba(4, 99, 7, 0.25) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary Buttons */
    .stButton > button {
        background: var(--background-white) !important;
        color: var(--primary-green) !important;
        border: 2px solid var(--primary-green) !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-green) !important;
        color: white !important;
        border-color: var(--primary-dark) !important;
        box-shadow: 0 4px 12px var(--shadow-green) !important;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border: 2px solid var(--border-light) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 3px var(--shadow-green) !important;
        outline: none !important;
    }
    
    /* Form Labels */
    .stTextInput > label,
    .stSelectbox > label,
    .stTextArea > label {
        color: var(--text-dark) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Cards & Containers */
    .stContainer {
        background: var(--background-white) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px var(--shadow-green) !important;
        padding: 1.5rem !important;
        border: 1px solid var(--border-light) !important;
    }
    
    /* Info/Success/Warning Boxes */
    .stInfo {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f2 100%) !important;
        border-left: 4px solid var(--primary-green) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: var(--text-dark) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #e8f5e9 100%) !important;
        border-left: 4px solid var(--success-green) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: var(--text-dark) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #fff3f4 100%) !important;
        border-left: 4px solid #dc3545 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Dividers */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent 0%, var(--primary-green) 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border: 2px solid var(--border-light) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px !important;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background: var(--background-light) !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: #e8f5e9 !important;
        transition: background 0.2s ease !important;
    }
    
    .stDataFrame tbody tr td {
        padding: 0.9rem !important;
        color: var(--text-dark) !important;
        border-bottom: 1px solid var(--border-light) !important;
    }
    
    /* Selectbox Dropdown */
    .stSelectbox [data-baseweb="select"] {
        border-radius: 8px !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--primary-green) !important;
    }
    
    /* Captions */
    .stCaptionContainer, .css-1v0mbdj {
        color: var(--text-muted) !important;
        font-size: 0.9rem !important;
    }
    
    /* Subheaders */
    .stSubheader {
        color: var(--primary-dark) !important;
        font-weight: 600 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid var(--border-light) !important;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-new {
        background: #e8f5e9;
        color: var(--primary-green);
        border: 1px solid var(--primary-green);
    }
    
    .status-qualified {
        background: #d4edda;
        color: var(--success-green);
        border: 1px solid var(--success-green);
    }
    
    .status-contacted {
        background: #cce5ff;
        color: #004085;
        border: 1px solid #004085;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-green) 0%, var(--primary-dark) 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Form Submit Button in Forms */
    .stForm [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px var(--shadow-green) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stForm [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-green) 100%) !important;
        box-shadow: 0 6px 20px rgba(4, 99, 7, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Column Dividers */
    [data-testid="column"] {
        padding: 0.5rem !important;
    }
    
    /* Links */
    a {
        color: var(--primary-green) !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    a:hover {
        color: var(--primary-dark) !important;
        text-decoration: underline !important;
    }
    
    /* Back Arrow Button Emoji Enhancement */
    button:has-text("←") {
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DB engine ---
engine = create_engine(settings.DATABASE_URL, future=True)

# --- Session state defaults ---
if "builder_id" not in st.session_state:
    st.session_state.builder_id = None

if "project_id" not in st.session_state:
    st.session_state.project_id = None


st.title("🏗️ Hygen RE – Onboarding & Leads Dashboard")


# ---------- STEP 1: BUILDER SELECTION ----------
def builder_step():
    st.subheader("🏢 Step 1 · Select or Add Builder")

    # Fetch existing builders
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, contact_name, contact_phone FROM hygen_re.builders ORDER BY name")
        )
        builders = result.fetchall()

    if builders:
        st.markdown("### 📋 Existing Builders")
        
        # Create selection options
        builder_options = {f"{b[1]} (ID: {b[0]})": b[0] for b in builders}
        
        selected_builder = st.selectbox(
            "Choose a builder:",
            options=list(builder_options.keys()),
            key="builder_select"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select This Builder", type="primary"):
                st.session_state.builder_id = builder_options[selected_builder]
                st.success(f"Builder selected! Moving to Project selection...")
                st.rerun()
        
        with col2:
            if st.button("Add New Builder Instead"):
                st.session_state.show_add_builder = True
                st.rerun()
        
        st.divider()
    
    # Show add new builder form if no builders exist or user clicked "Add New"
    if not builders or st.session_state.get("show_add_builder", False):
        st.markdown("### ➕ Add New Builder")
        
        with st.form("builder_form"):
            name = st.text_input("Builder Name", placeholder="AlphaStar Builders")
            contact_name = st.text_input("Contact Person", placeholder="Rajesh Kumar")
            contact_phone = st.text_input("Contact Phone (WhatsApp)", placeholder="+919876543210")
            contact_email = st.text_input("Contact Email", placeholder="rajesh@builder.com")

            submitted = st.form_submit_button("Save Builder")

        if submitted:
            if not name.strip():
                st.error("Builder name is required.")
                return

            with engine.begin() as conn:
                result = conn.execute(
                    text(
                        """
                        INSERT INTO hygen_re.builders (name, contact_name, contact_phone, contact_email)
                        VALUES (:name, :contact_name, :contact_phone, :contact_email)
                        RETURNING id
                        """
                    ),
                    {
                        "name": name.strip(),
                        "contact_name": contact_name.strip() or None,
                        "contact_phone": contact_phone.strip() or None,
                        "contact_email": contact_email.strip() or None,
                    },
                )
                builder_id = result.scalar_one()

            st.session_state.builder_id = builder_id
            st.session_state.show_add_builder = False
            st.success(f"Builder saved with ID {builder_id}. Moving to Project setup…")
            st.rerun()


# ---------- STEP 2: PROJECT SELECTION ----------
def project_step():
    st.subheader("🏘️ Step 2 · Select or Add Project")

    builder_id = st.session_state.builder_id
    
    # Get builder name
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM hygen_re.builders WHERE id = :id"),
            {"id": builder_id}
        )
        builder_name = result.scalar_one()
    
    st.info(f"Builder: {builder_name} (ID: {builder_id})")
    
    # Back button
    if st.button("← Change Builder"):
        st.session_state.builder_id = None
        st.session_state.show_add_builder = False
        st.rerun()

    # Fetch existing projects for this builder
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, name, project_type, location, price_range 
                FROM hygen_re.projects 
                WHERE builder_id = :builder_id 
                ORDER BY name
            """),
            {"builder_id": builder_id}
        )
        projects = result.fetchall()

    if projects:
        st.markdown("### 📋 Existing Projects")
        
        # Create selection options
        project_options = {}
        for p in projects:
            label = f"{p[1]} ({p[2]}) - {p[3] or 'No location'}"
            project_options[label] = p[0]
        
        selected_project = st.selectbox(
            "Choose a project:",
            options=list(project_options.keys()),
            key="project_select"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Leads for This Project", type="primary"):
                st.session_state.project_id = project_options[selected_project]
                st.success(f"Project selected! Loading leads...")
                st.rerun()
        
        with col2:
            if st.button("Add New Project Instead"):
                st.session_state.show_add_project = True
                st.rerun()
        
        st.divider()
    
    # Show add new project form if no projects exist or user clicked "Add New"
    if not projects or st.session_state.get("show_add_project", False):
        st.markdown("### ➕ Add New Project")
        
        with st.form("project_form"):
            name = st.text_input("Project Name", placeholder="AlphaStar Greens")
            project_type = st.selectbox("Project Type", ["Apartment", "Villa", "Plot", "Mixed"])
            location = st.text_input("Location", placeholder="Whitefield, Bangalore")
            price_range = st.text_input("Price Range", placeholder="₹45L - ₹85L")
            bhk_options = st.text_input("BHK Options", placeholder="2BHK,3BHK")
            possession_date = st.text_input("Possession Date", placeholder="December 2025")
            wa_entry_number = st.text_input(
                "WhatsApp Number Used in Ads",
                placeholder="+919876543210",
                help="The WA Business number that receives Meta ad leads for this project.",
            )

            submitted = st.form_submit_button("Save Project")

        if submitted:
            if not name.strip():
                st.error("Project name is required.")
                return

            with engine.begin() as conn:
                result = conn.execute(
                    text(
                        """
                        INSERT INTO hygen_re.projects (
                            builder_id, name, project_type, location,
                            price_range, bhk_options, possession_date,
                            amenities, wa_entry_number
                        )
                        VALUES (
                            :builder_id, :name, :project_type, :location,
                            :price_range, :bhk_options, :possession_date,
                            '[]'::jsonb, :wa_entry_number
                        )
                        RETURNING id
                        """
                    ),
                    {
                        "builder_id": builder_id,
                        "name": name.strip(),
                        "project_type": project_type,
                        "location": location.strip() or None,
                        "price_range": price_range.strip() or None,
                        "bhk_options": bhk_options.strip() or None,
                        "possession_date": possession_date.strip() or None,
                        "wa_entry_number": wa_entry_number.strip() or None,
                    },
                )
                project_id = result.scalar_one()

            st.session_state.project_id = project_id
            st.session_state.show_add_project = False
            st.success(f"Project saved with ID {project_id}. Showing Leads dashboard…")
            st.rerun()


# ---------- STEP 3: LEADS DASHBOARD ----------
def leads_dashboard():
    builder_id = st.session_state.builder_id
    project_id = st.session_state.project_id

    # Get project and builder details
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT p.name, p.project_type, p.location, b.name 
                FROM hygen_re.projects p
                JOIN hygen_re.builders b ON p.builder_id = b.id
                WHERE p.id = :pid
            """),
            {"pid": project_id}
        )
        project_name, project_type, location, builder_name = result.fetchone()

    st.subheader(f"📊 Leads Dashboard")
    st.caption(f"**{builder_name}** → **{project_name}** ({project_type} in {location or 'Location TBD'})")
    
    # Back button
    if st.button("← Change Project"):
        st.session_state.project_id = None
        st.session_state.show_add_project = False
        st.rerun()

    # Fetch leads
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT id,
                       wa_phone,
                       name,
                       status,
                       budget_min,
                       budget_max,
                       bhk_preference,
                       location_pref,
                       visit_interested,
                       visit_date,
                       visit_slot,
                       last_message_time,
                       created_at
                FROM hygen_re.leads
                WHERE project_id = :pid
                ORDER BY last_message_time DESC NULLS LAST, created_at DESC
                """
            ),
            {"pid": project_id},
        )
        rows = result.fetchall()

    st.markdown(f"### 👥 Total Leads: **{len(rows)}**")
    
    if rows:
        # Convert to list of dicts for better display
        import pandas as pd
        
        leads_data = []
        for row in rows:
            lead_id, wa_phone, name, status, budget_min, budget_max, bhk_pref, loc_pref, visit_int, visit_date, visit_slot, last_msg, created = row
            
            budget = ""
            if budget_min or budget_max:
                if budget_min and budget_max:
                    budget = f"₹{budget_min/100000:.0f}L - ₹{budget_max/100000:.0f}L"
                elif budget_min:
                    budget = f"₹{budget_min/100000:.0f}L+"
                elif budget_max:
                    budget = f"up to ₹{budget_max/100000:.0f}L"
            
            leads_data.append({
                "ID": lead_id,
                "Phone": wa_phone,
                "Name": name or "-",
                "Status": status,
                "Budget": budget or "-",
                "BHK": bhk_pref or "-",
                "Location": loc_pref or "-",
                "Visit?": "✅ Yes" if visit_int else "❌ No",
                "Visit Date": str(visit_date) if visit_date else "-",
                "Last Contact": last_msg.strftime("%Y-%m-%d %H:%M") if last_msg else "-",
                "Created": created.strftime("%Y-%m-%d %H:%M") if created else "-"
            })
        
        df = pd.DataFrame(leads_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("💬 No leads yet. Once your WhatsApp flow is connected, new leads will appear here automatically.")


# ---------- ROUTING LOGIC ----------
if st.session_state.builder_id is None:
    builder_step()
elif st.session_state.project_id is None:
    project_step()
else:
    leads_dashboard()
