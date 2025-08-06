# st_chatbot.py
import google.generativeai as genai 
import streamlit as st
import pandas as pd
from io import StringIO

@st.cache  # 데이터 로딩 함수 캐싱
def load_data(file_path):
    """파일에서 데이터를 로드하는 함수"""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# CSV 데이터 로드 및 프롬프트 생성
file_path = "커머스개발팀_전달사항.csv"  # 데이터 파일 경로
data = load_data(file_path)

if data is not None:
    csv_preview = data.head(100).to_string(index=False)
    additional_context = f"다음은 전달받은 커머스개발팀 관련 내용이야:\n{csv_preview}\n 을 참고해서 대화해 줘! 단 묻기전에 먼저 말하지는 마"
else:
    additional_context = "전달받은 데이터가 없어. 일반적인 대화를 해줘."

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

