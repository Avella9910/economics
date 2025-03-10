import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# 設定中文字型（防止顯示成方框）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 讓負號正常顯示

st.set_page_config(page_title="IS-LM 模型互動模擬", layout="wide")

# 側邊欄選單
page = st.sidebar.selectbox("選擇主題", ["首頁", "IS 曲線互動", "LM 曲線互動", "IS-LM 綜合分析"])

# 🔹 首頁
if page == "首頁":
    st.title("📊 IS-LM 模型互動模擬")
    st.write("""
    IS-LM 模型描述了**財政政策與貨幣政策**如何影響總產出 (Y) 和利率 (r)。  
    - **IS 曲線** 代表產品市場均衡 (投資 = 儲蓄)
    - **LM 曲線** 代表貨幣市場均衡 (貨幣供需相等)
    """)

    st.subheader("📌 互動模擬")
    st.write("請從左側選單選擇要觀察的變數！")

# 🔹 IS 曲線互動
elif page == "IS 曲線互動":
    st.title("🔍 IS 曲線與財政政策")
    st.write("調整 **政府支出 (G)** 或 **稅收 (T)**，觀察 AD 變動對 IS 曲線的影響。")

    # 互動變數
    G = st.slider("政府支出 (G)", min_value=50, max_value=300, value=100, step=10)
    T = st.slider("稅收 (T)", min_value=50, max_value=300, value=100, step=10)
    # **IS 曲線公式**
    def is_curve(Y, G, T):
        """IS 曲線: 由總需求 Z = C + I + G 決定"""
        C0, I0, b = 50, 50, 0.8  # 消費 & 投資參數
        return (C0 + I0 + b * (Y - T) + G)  # 均衡條件

    # 計算 IS 曲線
    Y_range = np.linspace(0, 500, 100)
    IS = is_curve(Y_range, G, T)

    # **繪製圖表**
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(Y_range, IS, label=f"IS 曲線 (G={G}, T={T})", color="blue")

    # 均衡點（假設固定利率 r=5）
    r_fixed = 5
    Y_star = (r_fixed - 50 - G) / -0.8 + T  # 簡化 IS 均衡條件
    ax.scatter(Y_star, r_fixed, color="black", zorder=3, label=f"均衡產出 Y*={Y_star:.1f}")

    ax.set_xlabel("總產出 Y")
    ax.set_ylabel("利率 r")
    ax.legend()
    ax.grid()

    # **顯示圖表**
    st.pyplot(fig)

    # **顯示均衡結果**
    st.write(f"📍 **均衡產出**: **Y* = {Y_star:.1f}**（在固定利率 r={r_fixed} 下）")


# 🔹 LM 曲線互動
elif page == "LM 曲線互動":
    st.title("📈 LM 曲線與貨幣政策")
    st.write("調整 **貨幣供給 (M)** 或 **價格水準 (P)**，觀察 LM 曲線變動。")

    # 互動變數
    M = st.slider("貨幣供給 (M)", min_value=100, max_value=500, value=200, step=10)
    P = st.slider("價格水準 (P)", min_value=1, max_value=5, value=2, step=1)
    # **LM 曲線公式**
    def lm_curve(Y, M, P):
        """LM 曲線: 由貨幣市場均衡決定"""
        k, h = 0.5, 0.5  # 貨幣需求彈性
        return (M / P - k * Y) / h

    # 計算 LM 曲線
    Y_range = np.linspace(0, 500, 100)
    LM = lm_curve(Y_range, M, P)

    # **繪製圖表**
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(Y_range, LM, label=f"LM 曲線 (M={M}, P={P})", color="red")

    # 均衡點（假設固定 Y=300）
    Y_fixed = 300
    r_star = lm_curve(Y_fixed, M, P)  # 計算 LM 均衡條件
    ax.scatter(Y_fixed, r_star, color="black", zorder=3, label=f"均衡利率 r*={r_star:.2f}")

    ax.set_xlabel("總產出 Y")
    ax.set_ylabel("利率 r")
    ax.legend()
    ax.grid()

    # **顯示圖表**
    st.pyplot(fig)

    # **顯示均衡結果**
    st.write(f"📍 **均衡利率**: **r* = {r_star:.2f}**（在固定產出 Y={Y_fixed} 下）")


# 🔹 IS-LM 綜合分析
elif page == "IS-LM 綜合分析":
    st.title("⚖️ IS-LM 模型的均衡點")
    st.write("調整財政或貨幣變數，觀察均衡點 (Y*, r*) 如何變動。")
    # **1️⃣ 設定互動變數**
    st.sidebar.header("🔧 調整變數")
    G = st.sidebar.slider("政府支出 (G)", min_value=50, max_value=300, value=100, step=10)
    T = st.sidebar.slider("稅收 (T)", min_value=50, max_value=300, value=100, step=10)
    M = st.sidebar.slider("貨幣供給 (M)", min_value=100, max_value=500, value=200, step=10)
    P = st.sidebar.slider("價格水準 (P)", min_value=1, max_value=5, value=2, step=1)

    # **2️⃣ IS-LM 公式**
    def is_curve(Y, G, T):
        """IS 曲線: 財政政策影響投資與消費"""
        C0, I0, b = 50, 50, 0.8  # 消費 & 投資參數
        return (C0 + I0 + b * (Y - T) + G)  # 均衡條件

    def lm_curve(Y, M, P):
        """LM 曲線: 貨幣市場均衡"""
        k, h = 0.5, 0.5  # 貨幣需求彈性
        return (M / P - k * Y) / h

    # **3️⃣ 計算均衡點**
    Y_range = np.linspace(0, 500, 100)
    IS = is_curve(Y_range, G, T)
    LM = lm_curve(Y_range, M, P)

    # 找到交點（最小誤差）
    equilibrium_index = np.argmin(np.abs(IS - LM))
    Y_star = Y_range[equilibrium_index]
    r_star = IS[equilibrium_index]

    # **4️⃣ 畫圖**
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(Y_range, IS, label="IS 曲線 (產品市場)", color="blue")
    ax.plot(Y_range, LM, label="LM 曲線 (貨幣市場)", color="red")
    ax.scatter(Y_star, r_star, color="black", zorder=3, label=f"均衡點 (Y*={Y_star:.1f}, r*={r_star:.2f})")

    ax.set_xlabel("總產出 Y")
    ax.set_ylabel("利率 r")
    ax.legend()
    ax.grid()

    # **5️⃣ 顯示圖表**
    st.pyplot(fig)

    # **6️⃣ 顯示均衡結果**
    st.write(f"📍 **IS = LM 均衡點**: 產出 **Y* = {Y_star:.1f}**，利率 **r* = {r_star:.2f}**")

st.sidebar.write("🔹 選擇不同的頁面來學習 IS-LM 模型！")