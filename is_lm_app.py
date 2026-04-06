import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 設定字型（避免中文顯示成方框）
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang TC", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="IS-LM 模型互動模擬", layout="wide")

# -----------------------------
# 參數函數
# -----------------------------
def is_curve(Y, G, T, c0=50, c=0.8, I0=80, b=10):
    """
    IS 曲線：
    商品市場均衡 Y = C + I + G
    C = c0 + c(Y - T)
    I = I0 - b r

    整理得：
    r = [c0 + I0 + G - cT - (1-c)Y] / b
    """
    return (c0 + I0 + G - c * T - (1 - c) * Y) / b


def lm_curve(Y, M, P, k=0.6, h=8):
    """
    LM 曲線：
    M/P = kY - h r

    整理得：
    r = (kY - M/P) / h
    """
    return (k * Y - M / P) / h


def solve_equilibrium(G, T, M, P, c0=50, c=0.8, I0=80, b=10, k=0.6, h=8):
    """
    聯立 IS 與 LM：
    [c0 + I0 + G - cT - (1-c)Y] / b = (kY - M/P) / h

    解出 Y* 與 r*
    """
    A = c0 + I0 + G - c * T
    numerator = h * A + b * (M / P)
    denominator = h * (1 - c) + b * k
    Y_star = numerator / denominator
    r_star = is_curve(Y_star, G, T, c0, c, I0, b)
    return Y_star, r_star


# 側邊欄選單
page = st.sidebar.selectbox(
    "選擇主題",
    ["首頁", "IS 曲線互動", "LM 曲線互動", "IS-LM 綜合分析"]
)

# -----------------------------
# 首頁
# -----------------------------
if page == "首頁":
    st.title("📊 IS-LM 模型互動模擬")
    st.write("""
    IS-LM 模型用來分析 **財政政策** 與 **貨幣政策** 如何影響：
    - **總產出 \(Y\)**
    - **利率 \(r\)**

    其中：
    - **IS 曲線**：商品市場均衡
    - **LM 曲線**：貨幣市場均衡
    """)

    st.subheader("📌 互動模擬")
    st.write("請從左側選單選擇要觀察的頁面。")

# -----------------------------
# IS 曲線互動
# -----------------------------
elif page == "IS 曲線互動":
    st.title("🔍 IS 曲線與財政政策")
    st.write("調整 **政府支出 (G)** 或 **稅收 (T)**，觀察 IS 曲線如何移動。")

    G = st.slider("政府支出 (G)", min_value=50, max_value=300, value=100, step=10)
    T = st.slider("稅收 (T)", min_value=0, max_value=200, value=50, step=10)

    Y_range = np.linspace(0, 1000, 300)
    r_values = is_curve(Y_range, G, T)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Y_range, r_values, label=f"IS 曲線 (G={G}, T={T})")

    ax.set_xlabel("總產出 Y")
    ax.set_ylabel("利率 r")
    ax.set_title("IS 曲線")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.markdown(f"""
    **解讀：**
    - 當 **G 上升** 時，IS 曲線會 **右移**
    - 當 **T 上升** 時，IS 曲線會 **左移**
    """)

# -----------------------------
# LM 曲線互動
# -----------------------------
elif page == "LM 曲線互動":
    st.title("📈 LM 曲線與貨幣政策")
    st.write("調整 **貨幣供給 (M)** 或 **價格水準 (P)**，觀察 LM 曲線如何移動。")

    M = st.slider("貨幣供給 (M)", min_value=100, max_value=1000, value=400, step=20)
    P = st.slider("價格水準 (P)", min_value=1, max_value=10, value=2, step=1)

    Y_range = np.linspace(0, 1000, 300)
    r_values = lm_curve(Y_range, M, P)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Y_range, r_values, label=f"LM 曲線 (M={M}, P={P})")

    ax.set_xlabel("總產出 Y")
    ax.set_ylabel("利率 r")
    ax.set_title("LM 曲線")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.markdown(f"""
    **解讀：**
    - 當 **M 上升** 時，LM 曲線會 **右移 / 下移**
    - 當 **P 上升** 時，實質貨幣供給 \(M/P\) 下降，LM 曲線會 **左移 / 上移**
    """)

# -----------------------------
# IS-LM 綜合分析
# -----------------------------
elif page == "IS-LM 綜合分析":
    st.title("⚖️ IS-LM 模型的均衡點")
    st.write("同時調整財政與貨幣變數，觀察均衡產出與均衡利率的變化。")

    st.sidebar.header("🔧 調整變數")
    G = st.sidebar.slider("政府支出 (G)", min_value=50, max_value=300, value=100, step=10)
    T = st.sidebar.slider("稅收 (T)", min_value=0, max_value=200, value=50, step=10)
    M = st.sidebar.slider("貨幣供給 (M)", min_value=100, max_value=1000, value=400, step=20)
    P = st.sidebar.slider("價格水準 (P)", min_value=1, max_value=10, value=2, step=1)

    Y_range = np.linspace(0, 1000, 300)
    IS = is_curve(Y_range, G, T)
    LM = lm_curve(Y_range, M, P)

    Y_star, r_star = solve_equilibrium(G, T, M, P)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Y_range, IS, label="IS 曲線")
    ax.plot(Y_range, LM, label="LM 曲線")
    ax.scatter(Y_star, r_star, color="black", zorder=5,
               label=f"均衡點 (Y*={Y_star:.1f}, r*={r_star:.2f})")

    ax.set_xlabel("總產出 Y")
    ax.set_ylabel("利率 r")
    ax.set_title("IS-LM 均衡")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.subheader("📍 均衡結果")
    st.write(f"**均衡產出**：Y* = **{Y_star:.1f}**")
    st.write(f"**均衡利率**：r* = **{r_star:.2f}**")

    st.subheader("📘 經濟直覺")
    st.markdown("""
    - **政府支出增加（G↑）**：IS 右移，通常使 **Y 上升、r 上升**
    - **稅收增加（T↑）**：IS 左移，通常使 **Y 下降、r 下降**
    - **貨幣供給增加（M↑）**：LM 右移，通常使 **Y 上升、r 下降**
    - **價格水準上升（P↑）**：LM 左移，通常使 **Y 下降、r 上升**
    """)

st.sidebar.write("🔹 選擇不同頁面來學習 IS-LM 模型！")
