import os
import sys

import streamlit as st
from sqlalchemy import create_engine, text

# --- Make sure we can import app.config ---
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.config import settings  # noqa: E402

# --- DB engine ---
engine = create_engine(settings.DATABASE_URL, future=True)

# --- Session state defaults ---
if "builder_id" not in st.session_state:
    st.session_state.builder_id = None

if "project_id" not in st.session_state:
    st.session_state.project_id = None


st.title("Hygen RE – Onboarding & Leads Dashboard (MVP1)")


# ---------- STEP 1: BUILDER SETUP ----------
def builder_step():
    st.subheader("Step 1 · Builder Details")

    with st.form("builder_form"):
        name = st.text_input("Builder Name", placeholder="AlphaStar Builders")
        contact_name = st.text_input("Contact Person", placeholder="Ajal Shajahan")
        contact_phone = st.text_input("Contact Phone (WhatsApp)", placeholder="+91XXXXXXXXXX")
        contact_email = st.text_input("Contact Email", placeholder="sales@builder.com")

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
        st.success(f"Builder saved with ID {builder_id}. Moving to Project setup…")
        st.rerun()


# ---------- STEP 2: PROJECT SETUP ----------
def project_step():
    st.subheader("Step 2 · Project Details")

    builder_id = st.session_state.builder_id
    st.info(f"Active Builder ID: {builder_id}")

    with st.form("project_form"):
        name = st.text_input("Project Name", placeholder="AlphaStar Greens")
        project_type = st.selectbox("Project Type", ["flat", "villa", "plot", "mixed"])
        location = st.text_input("Location", placeholder="Kottayam")
        price_range = st.text_input("Price Range", placeholder="₹65L – ₹1.2Cr")
        bhk_options = st.text_input("BHK Options", placeholder="2 BHK,3 BHK")
        possession_date = st.text_input("Possession Date", placeholder="Dec 2026")
        wa_entry_number = st.text_input(
            "WhatsApp Number Used in Ads",
            placeholder="+91XXXXXXXXXX",
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
        st.success(f"Project saved with ID {project_id}. Showing Leads dashboard…")
        st.rerun()


# ---------- STEP 3: LEADS DASHBOARD ----------
def leads_dashboard():
    builder_id = st.session_state.builder_id
    project_id = st.session_state.project_id

    st.subheader("Step 3 · Leads Dashboard")
    st.caption(f"Builder ID: {builder_id} · Project ID: {project_id}")

    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT id,
                       wa_phone,
                       budget_min,
                       bhk_preference,
                       location_pref,
                       status,
                       visit_date,
                       visit_slot,
                       updated_at
                FROM hygen_re.leads
                WHERE project_id = :pid
                ORDER BY updated_at DESC
                """
            ),
            {"pid": project_id},
        )
        rows = result.fetchall()

    st.write(f"Total leads: {len(rows)}")
    if rows:
        st.dataframe(rows)
    else:
        st.info("No leads yet. Once your WhatsApp flow is connected, new leads will appear here automatically.")


# ---------- ROUTING LOGIC ----------
if st.session_state.builder_id is None:
    builder_step()
elif st.session_state.project_id is None:
    project_step()
else:
    leads_dashboard()
