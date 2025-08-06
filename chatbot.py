# st_chatbot.py
import streamlit as st

import google.generativeai as genai 
genai.configure(auth=st.secrets["GOOGLE_API_KEY"])

from notion_client import Client
notion = Client(auth=st.secrets["NOTION_API_KEY"])

page_id = "2460b8e5ab1680d38eaee92db73e0193"

def get_page_text(page_id):
    blocks = notion.blocks.children.list(page_id=page_id)["results"]
    text = []
    for block in blocks:
        block_type = block["type"]
        if block_type in block and "text" in block[block_type]:
            for t in block[block_type]["text"]:
                text.append(t["plain_text"])
    return "\n".join(text)

additional_context = get_page_text(page_id)

st.title("커머스개발팀 막내")

system_instruction = (
    "당신은 커머스개발팀에 입사한지 1년이 안된 새내기 입니다.\n"
    "이름은 커냥이, 나이 6살, 성별 중성, 전생에 10년차 커머스 서버개발자로 엄청난 실력을 보유하고 있었는데 번개를 맞고 과거 기억을 가지고 환생한 고양이 입니다.\n"
    "사용자는 선배 직장동료들입니다. 밝고 명량하게 이야기하고, 문장의 끝에는 이모지와 마지막에 '냥' 이라고 써주세요.\n\n"
    f"{additional_context}"
)

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=system_instruction)
    print("model loaded...")
    return model

model = load_model()

if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)

