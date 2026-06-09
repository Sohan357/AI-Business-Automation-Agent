import streamlit as st
import pandas as pd

from data import crm_leads, candidates, projects
from agent import (
    high_priority_leads,
    generate_email,
    screen_candidate,
    project_risks,
    business_summary,
    audit_logs,
    add_audit
)

st.set_page_config(
    page_title="Business Automation Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Business Automation Agent")

role = st.sidebar.selectbox(
    "Select Role",
    [
        "Admin",
        "Sales",
        "HR",
        "Project Manager"
    ]
)
st.sidebar.success(
    f"Logged in as: {role}"
)


st.sidebar.header("Dashboard")

st.sidebar.metric(
    "Total Leads",
    len(crm_leads)
)

st.sidebar.metric(
    "Candidates",
    len(candidates)
)

st.sidebar.metric(
    "Projects",
    len(projects)
)

role_permissions = {
    "Admin": ["CRM", "HRMS", "PMS", "Analytics", "Audit Logs"],
    "Sales": ["CRM", "Analytics"],
    "HR": ["HRMS", "Analytics"],
    "Project Manager": ["PMS", "Analytics"]
}

allowed_tabs = role_permissions[role]

tabs = st.tabs(allowed_tabs)

tab_map = dict(zip(allowed_tabs, tabs))

# CRM
if "CRM" in tab_map:

    with tab_map["CRM"]:

        st.header("CRM Assistant")

        if st.button("Show High Priority Leads"):

            add_audit(role, "Viewed High Priority Leads")

            leads = high_priority_leads()
            df = pd.DataFrame(leads)

            st.dataframe(df)

        st.subheader("Generate Sales Email")

        lead_name = st.selectbox(
            "Select Lead",
            [lead["name"] for lead in crm_leads]
        )

        project_name = st.selectbox(
            "Select Product / Project",
            [
                "AI Business Automation Platform",
                "CRM Upgrade Solution",
                "HRMS Automation Suite",
                "Project Tracking System"
            ]
        )

        if st.button("Generate Email"):

            add_audit(
                role,
                f"Generated Email for {lead_name}"
            )

            email = generate_email(
                lead_name,
                project_name
            )

            st.text_area(
                "Generated Email",
                email,
                height=300
            )

# HRMS
if "HRMS" in tab_map:

    with tab_map["HRMS"]:

        st.header("Resume Screening")

        candidate_name = st.selectbox(
            "Select Candidate",
            [c["name"] for c in candidates]
        )

        if st.button("Screen Candidate"):

            add_audit(role, "Screen Candidate")

            result = screen_candidate(candidate_name)

            if isinstance(result, dict):

                df = pd.DataFrame([result["candidate"]])

                st.subheader("Candidate Details")
                st.dataframe(df)

                st.subheader("Screening Result")
                st.success(f"Score: {result['score']}")

            else:
                st.error(result)

# PMS


# PMS
if "PMS" in tab_map:

    with tab_map["PMS"]:

        st.header("📌 Project Management System")

        if st.button("Show Project Risks"):

            add_audit(role, "Viewed Project Risks")

            risks = project_risks()
            df = pd.DataFrame(risks)

            st.subheader("📊 PMS Dashboard")

            # KPIs
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Projects", len(projects))

            with col2:
                st.metric("Delayed Projects", len(df))

            with col3:
                on_track = len([p for p in projects if p["status"] == "On Track"])
                st.metric("On Track Projects", on_track)

            st.divider()

            # If no risks
            if df.empty:
                st.success("🎉 No delayed projects! All projects are on track.")
            else:

                # Sort by deadline
                df = df.sort_values(by="deadline")

                st.subheader("🚨 Delayed Projects")

                # Show table
                st.dataframe(df, use_container_width=True)

                # Optional highlight
                st.subheader("⚠️ Risk View")

                st.dataframe(
                    df.style.map(
                        lambda x: "color: red; font-weight: bold"
                        if x == "Delayed" else ""
                    )
                )
# Analytics
if "Analytics" in tab_map:

    with tab_map["Analytics"]:

        st.header("Business Analytics")

        lead_df = pd.DataFrame(crm_leads)

        st.subheader("Lead Scores")

        st.bar_chart(
            lead_df.set_index("name")["score"]
        )

        project_df = pd.DataFrame(projects)

        st.subheader("Project Status")

        st.dataframe(project_df)

        if st.button("Generate AI Summary"):

            st.write(
                business_summary()
            )

# Audit
if "Audit Logs" in tab_map:

    with tab_map["Audit Logs"]:

        st.header("📋 Audit Logs")

        if len(audit_logs) == 0:
            st.info("No audit logs yet.")
        else:
            df = pd.DataFrame(audit_logs)

            st.subheader("User Activity Log")
            st.dataframe(df, use_container_width=True)