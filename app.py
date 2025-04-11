import streamlit as st
import pandas as pd
import os

# 데이터 저장 경로
DATA_PATH = "buildings.csv"

# 데이터 불러오기
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["이름", "높이", "넓이", "건설 날짜", "만든 사람", "링크"])

# 데이터 저장하기
def save_data(df):
    df.to_csv(DATA_PATH, index=False, encoding='utf-8-sig')

# 앱 시작
st.title("🏗️ 마인크래프트 건축물 기록 앱")

df = load_data()

# 건축물 등록
st.subheader("➕ 건축물 등록")
name = st.text_input("건축물 이름")
height = st.number_input("높이", min_value=0)
area = st.number_input("넓이", min_value=0)
date = st.date_input("건설된 날짜")
builder = st.text_input("만든 사람")
link = st.text_input("관련 링크 (선택사항)")

if st.button("등록"):
    if name and builder:
        new_data = pd.DataFrame([{
            "이름": name,
            "높이": height,
            "넓이": area,
            "건설 날짜": date,
            "만든 사람": builder,
            "링크": link
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("✅ 건축물 등록 완료!")
    else:
        st.warning("이름과 만든 사람은 반드시 입력해야 합니다.")

# 정렬 기능
st.subheader("🔍 정렬된 건축물 목록 보기")
sort_by = st.selectbox("정렬 기준", ["이름", "높이", "넓이", "건설 날짜", "만든 사람"])
ascending = st.radio("정렬 방식", ["오름차순", "내림차순"]) == "오름차순"

if not df.empty:
    df_sorted = df.sort_values(by=sort_by, ascending=ascending)
    
    # 링크가 있으면 클릭 가능한 마크다운으로 바꾸기
    df_sorted["링크"] = df_sorted["링크"].apply(lambda x: f"[열기]({x})" if pd.notnull(x) and x.strip() != "" else "")
    
    st.markdown(df_sorted.to_markdown(index=False), unsafe_allow_html=True)
else:
    st.info("등록된 건축물이 없습니다.")

# 건축물 삭제
st.subheader("❌ 건축물 삭제")
if not df.empty:
    selected = st.selectbox("삭제할 건축물을 선택하세요", df["이름"].unique())
    if st.button("삭제"):
        df = df[df["이름"] != selected]
        save_data(df)
        st.success(f"🗑️ '{selected}' 삭제 완료!")
