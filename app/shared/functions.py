import streamlit as st
import time

def start_pipeline():
    with st.status("running Pipeline with your data...", expanded=True) as status:
        st.write("Import data into MongoDB...")
        time.sleep(2)
        st.write("Processing Data")
        time.sleep(1)
        st.write("Finish...")
        time.sleep(1)
        status.update(label="Pipeline run completed!", state="complete", expanded=False)