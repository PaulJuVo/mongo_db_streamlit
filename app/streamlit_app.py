import streamlit as st

pages = {
    "Overview": [
        st.Page("pages/sector.py", title="Ratio Comparison"),
        st.Page("pages/companies.py", title="Company Data"),
    ],
    "Ranking": [
        st.Page("pages/ranking.py", title="Top 10 per Sector"),
        st.Page("pages/ranking_all.py", title="Full Ranking")
    ],
    "Pipeline": [
        st.Page("pages/pipeline.py", title="Import"),
    ]
}

navigation = st.navigation(pages)
navigation.run()