import random
import streamlit as st
import pandas as pd


if "dices_list" not in st.session_state:
    st.session_state.dices_list = []

st.title("2つのサイコロを振るアプリ")

multiple = st.toggle("複数回振る", False)
print(multiple)

if not multiple:

    if st.button("サイコロを振る"):
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)

        dice_sum = dice_1 + dice_2
        st.session_state.dices_list.append((dice_1, dice_2, dice_sum))
        # st.write(f"サイコロ1： {dice_1} ／サイコロ2： {dice_2}")
else:
    n = st.slider("回数", 1, 1000, 500)

    if st.button("サイコロを振る"):
        for _ in range(n):
            dice_1 = random.randint(1, 6)
            dice_2 = random.randint(1, 6)

            dice_sum = dice_1 + dice_2
            st.session_state.dices_list.append((dice_1, dice_2, dice_sum))
            # st.write(f"サイコロ1： {dice_1} ／サイコロ2： {dice_2}")

        st.write(f"{n}回サイコロを振りました")

df = pd.DataFrame(st.session_state.dices_list, columns=["サイコロ1", "サイコロ2", "合計"])
st.dataframe(df)

# debug
print(st.session_state.dices_list)

st.write("試行回数：", len(st.session_state.dices_list))

if st.button("結果を棒グラフで表示"):
    st.bar_chart(df["合計"].value_counts())