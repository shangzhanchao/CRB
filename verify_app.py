"""Streamlit verification page for the companion robot brain.

通过 Streamlit 构建的验证界面，可录制或上传音视频并查看机器
人返回的文本、动作和表情等结果。若安装 ``st_audiorecorder``
和 ``streamlit-webrtc``，还可直接在浏览器录制声音和视频。

Run with::

    streamlit run verify_app.py
"""
from __future__ import annotations

import tempfile
from pathlib import Path
import uuid

import streamlit as st

try:  # optional component for recording from the browser microphone
    from st_audiorecorder import st_audiorecorder  # type: ignore
except Exception:  # pragma: no cover - library missing
    st_audiorecorder = None

try:  # optional video recording support
    from streamlit_webrtc import webrtc_streamer, WebRtcMode  # type: ignore
    import av  # type: ignore
except Exception:  # pragma: no cover - library missing
    webrtc_streamer = None
    WebRtcMode = None

from ai_core import IntelligentCore, UserInput

core = IntelligentCore()

st.set_page_config(page_title="CRB Verification", layout="wide")
st.title("CRB Verification")

left, right = st.columns(2)

with left:
    st.header("Input")
    with st.form("input_form"):
        robot_id = st.text_input("Robot ID", "robotA")
        text = st.text_input("Text")

        st.subheader("Audio")
        audio_bytes = None
        if st_audiorecorder is not None:
            audio_bytes = st_audiorecorder("Record", "Stop")
        audio_file = st.file_uploader("Or upload audio", type=["wav", "mp3", "ogg"])

        st.subheader("Image / Video")
        image_capture = st.camera_input("Take Photo")
        image_file = st.file_uploader("Or upload image", type=["png", "jpg", "jpeg"])
        video_file = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])

        zone = st.selectbox("Touch Zone", ("", "0", "1", "2"))
        submitted = st.form_submit_button("Send")

if submitted:
    def save_bytes(data: bytes, suffix: str) -> str:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp.write(data)
        temp.close()
        return temp.name

    audio_path = None
    if audio_bytes:
        audio_path = save_bytes(audio_bytes, ".wav")
    elif audio_file is not None:
        audio_path = save_bytes(audio_file.read(), Path(audio_file.name).suffix)

    image_path = None
    if image_capture is not None:
        image_path = save_bytes(image_capture.getvalue(), ".png")
    elif image_file is not None:
        image_path = save_bytes(image_file.read(), Path(image_file.name).suffix)

    video_path = None
    if video_file is not None:
        video_path = save_bytes(video_file.read(), Path(video_file.name).suffix)

    user = UserInput(
        robot_id=robot_id,
        text=text or None,
        audio_path=audio_path,
        image_path=image_path,
        video_path=video_path,
        touch_zone=int(zone) if zone else None,
    )
    result = core.process(user).as_dict()
    with right:
        st.header("Output")
        st.write(result["text"])
        if result["audio"] and result["audio"] != "n/a":
            st.audio(result["audio"])
        st.write("Action: ", ", ".join(result["action"]))
        st.write("Expression: ", result["expression"])
        st.json(result)