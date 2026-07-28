import pandas as pd
import streamlit as st

st.set_page_config(page_title="中国語単語クイズ", page_icon="🇨🇳")
st.title("中国語 記述クイズ 🇨🇳")

# データ読み込み
@st.cache_data
def load_data():
    return pd.read_csv("chinese_practice.csv", encoding="utf-8")

try:
    df = load_data()
except Exception as e:
    st.error(f"chinese_practice.csv の読み込みに失敗しました: {e}")
    st.stop()

# セッション状態の初期化
if "questions" not in st.session_state:
    st.session_state.questions = df.sample(frac=1).reset_index(drop=True)
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.is_correct = False

total_q = len(st.session_state.questions)
current_idx = st.session_state.current_idx

# 全問終了時
if current_idx >= total_q:
    st.success("🎉 全問終了しました！")
    st.metric(label="最終スコア", value=f"{st.session_state.score} / {total_q}")
    if st.button("最初からやり直す"):
        st.session_state.questions = df.sample(frac=1).reset_index(drop=True)
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()
    st.stop()

# 問題表示
current_q = st.session_state.questions.iloc[current_idx]

st.subheader(f"問題 {current_idx + 1} / {total_q}")
st.info(f"**意味**: {current_q['meaning']}")

# 入力フォーム
with st.form(key=f"q_form_{current_idx}"):
    user_input = st.text_input("中国語を入力してください（簡体字等）:", key=f"input_{current_idx}")
    submit_btn = st.form_submit_button("回答する")

if submit_btn and not st.session_state.answered:
    clean_user = user_input.strip()
    clean_target = str(current_q["Chinese"]).strip()
    
    st.session_state.answered = True
    if clean_user == clean_target:
        st.session_state.is_correct = True
        st.session_state.score += 1
    else:
        st.session_state.is_correct = False

# 結果フィードバックと遷移
if st.session_state.answered:
    if st.session_state.is_correct:
        st.success("⭕️ 正解！")
    else:
        st.error(f"❌ 不正解... 正解は: **{current_q['Chinese']}**")

    if st.button("次の問題へ ➔"):
        st.session_state.current_idx += 1
        st.session_state.answered = False
        st.rerun()
