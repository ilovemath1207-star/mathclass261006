import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Streamlit 요소 체험실",
    page_icon=":test_tube:",
    layout="wide",
)

st.title("Streamlit 요소 체험실")
st.write("웹 앱을 처음 만들어도 괜찮아요. 아래 요소를 직접 바꾸며 화면이 어떻게 달라지는지 확인해 보세요.")
st.caption("위젯을 조작하면 Streamlit이 앱을 다시 실행하고, 바뀐 값으로 화면을 업데이트합니다.")
st.divider()

st.header("1. 입력 요소")
st.markdown("각 입력 요소에 값을 넣어 보세요. 오른쪽 미리보기에 현재 선택이 표시됩니다.")

input_col, preview_col = st.columns([3, 2])

with input_col:
    learner_name = st.text_input("텍스트 입력", placeholder="이름을 입력해 보세요")
    st.caption("`st.text_input`: 한 줄의 글자나 짧은 답을 입력받습니다.")

    favorite_topic = st.selectbox(
        "선택 상자",
        ["데이터 시각화", "파이썬 기초", "웹 앱 만들기", "아직 고르는 중"],
    )
    st.caption("`st.selectbox`: 여러 항목 중 하나를 선택합니다.")

    sample_count = st.slider("슬라이더", min_value=3, max_value=10, value=6)
    st.caption("`st.slider`: 범위 안에서 숫자를 선택합니다. 아래 데이터 행 수에도 반영됩니다.")

    show_tip = st.checkbox("도움말 메시지 보기", value=True)
    st.caption("`st.checkbox`: 켜기/끄기처럼 참 또는 거짓 값을 선택합니다.")

    chart_kind = st.radio(
        "차트 종류",
        ["선 차트", "막대 차트", "영역 차트"],
        horizontal=True,
    )
    st.caption("`st.radio`: 여러 선택지 중 하나를 고릅니다.")

with preview_col:
    st.subheader("입력 미리보기")
    if learner_name.strip():
        st.success(f"반가워요, {learner_name.strip()}님!")
    else:
        st.info("텍스트 입력에 이름을 적으면 인사말이 나타나요.")

    st.metric(label="관심 주제", value=favorite_topic)
    st.metric(label="만들 데이터 행 수", value=f"{sample_count}개")
    if show_tip:
        st.info("팁: 슬라이더를 움직이면 아래 표와 차트의 데이터 개수도 바뀝니다.")
    else:
        st.warning("도움말 메시지를 숨겼습니다. 체크박스를 다시 눌러 보세요.")

st.divider()
st.header("2. 버튼과 상태")
st.markdown("버튼은 눌렀을 때 작업을 실행할 때 사용합니다. 아래 버튼을 눌러 횟수가 올라가는지 확인해 보세요.")

if "click_count" not in st.session_state:
    st.session_state.click_count = 0

button_col, count_col = st.columns([1, 3])
with button_col:
    if st.button("버튼 눌러 보기", type="primary"):
        st.session_state.click_count += 1
with count_col:
    st.metric("버튼을 누른 횟수", f"{st.session_state.click_count}회")

st.caption("`st.session_state`는 화면이 다시 그려져도 기억해야 하는 값을 저장합니다.")

with st.form("feedback_form"):
    st.subheader("양식으로 한 번에 제출하기")
    st.write("양식 안의 입력은 제출 버튼을 누를 때 앱에 전달됩니다.")
    rating = st.select_slider("오늘의 난이도", options=["쉬움", "적당함", "어려움"])
    comment = st.text_area("한 줄 소감", placeholder="직접 써 보세요")
    submitted = st.form_submit_button("소감 제출")

if submitted:
    st.success(f"제출 완료! 난이도: {rating}" + (f" · 소감: {comment}" if comment else ""))

st.divider()
st.header("3. 데이터 표와 차트")
st.markdown("표를 직접 편집하거나 슬라이더와 차트 종류를 바꾸어 보세요. 표의 데이터가 차트에도 사용됩니다.")

data = pd.DataFrame(
    {
        "차시": list(range(1, sample_count + 1)),
        "학습 점수": [min(100, 55 + index * 6 + sample_count) for index in range(sample_count)],
        "목표 점수": [80] * sample_count,
    }
)

st.subheader("편집 가능한 데이터 표")
edited_data = st.data_editor(
    data,
    hide_index=True,
    num_rows="dynamic",
    width="stretch",
    key="scores_table",
)
st.caption("`st.data_editor`: 표의 셀을 직접 수정하거나 행을 추가·삭제할 수 있습니다.")

st.subheader(f"{chart_kind} 미리보기")
if edited_data.empty:
    st.info("표에 행을 추가하면 차트가 표시됩니다.")
else:
    chart_data = edited_data.set_index("차시")
    if chart_kind == "선 차트":
        st.line_chart(chart_data, y=["학습 점수", "목표 점수"])
    elif chart_kind == "막대 차트":
        st.bar_chart(chart_data, y=["학습 점수", "목표 점수"])
    else:
        st.area_chart(chart_data, y=["학습 점수", "목표 점수"])
st.caption("`st.line_chart`, `st.bar_chart`, `st.area_chart`: 숫자 데이터의 변화와 비교를 시각화합니다.")

st.subheader("읽기 전용 표")
st.table(edited_data.head(5))
st.caption("`st.table`: 데이터를 간단한 표로 보여줍니다. 위 데이터 편집기와 달리 읽기 전용입니다.")

csv_data = edited_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "편집한 표 CSV로 다운로드",
    data=csv_data,
    file_name="streamlit-체험-데이터.csv",
    mime="text/csv",
)
st.caption("`st.download_button`: 앱에서 만든 파일을 사용자의 기기로 내려받게 합니다.")

st.divider()
st.header("4. 화면 구성과 안내 메시지")
left_col, right_col = st.columns(2)
with left_col:
    with st.expander("펼쳐서 더 알아보기"):
        st.write("`st.columns`는 화면을 나누고, `st.expander`는 내용을 접고 펼칠 수 있게 합니다.")
        st.code('st.write("안녕하세요!")', language="python")
with right_col:
    st.success("성공 메시지: 작업이 잘 끝났을 때")
    st.warning("주의 메시지: 확인할 내용이 있을 때")
    st.error("오류 메시지: 문제가 생겼을 때")
    st.caption("`st.success`, `st.warning`, `st.error`, `st.info`: 상황에 맞는 안내를 보여줍니다.")

st.divider()
st.caption("이 페이지는 Streamlit과 pandas만 사용합니다. 왼쪽 메뉴가 보이지 않으면 브라우저 창을 넓혀 보세요.")
