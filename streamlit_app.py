import streamlit as st
import cv2
import tempfile
from processor import process_frame

st.set_page_config(layout="wide")
st.title("Football Tracker")

st.sidebar.header("Controls")

video_file = st.sidebar.file_uploader("Upload Football Video", type=["mp4", "avi", "mov"])

start = st.sidebar.button("Start Processing")

frame_placeholder = st.empty()
status_text = st.empty()

if video_file is not None and start:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    cap = cv2.VideoCapture(tfile.name)

    status_text.markdown("### Processing Video")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)

        frame_placeholder.image(processed_frame, channels="BGR")

    cap.release()
    status_text.markdown("### Processing Complete")

elif video_file is None:
    st.info("Upload a Football Video")