import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 設定中文字型（防止顯示成方框）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 讓負號正常顯示

# 設定 Streamlit 頁面
st.set_page_config(page_title="AD-AS 模擬", layout="centered")

# 🔹 建立「頁面切換」選單
page = st.sidebar.selectbox("選擇主題", ["🏠 首頁", "📊 AD-AS 模擬", "乘數效應與模式區別", "需求衝擊 vs. 供給衝擊", "短期 vs. 長期 AS", "約翰·梅納德·凱因斯"])

# 🎯 **首頁**
if page == "🏠 首頁":
    st.title("📈 總體經濟學 AD-AS 模擬")
    st.write("""
    本應用程式讓你調整 **政府支出 (G)** 與 **貨幣供給 (M)**，並即時觀察
    **總需求 (AD)** 與 **總供給 (AS)** 變化對 GDP 和物價的影響。

    **特點：**
    - **互動式調整 AD-AS 模型**
    - **不同經濟情境（需求衝擊、供給衝擊）**
    - **可視化總體經濟變化**
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/25/AS_%2B_AD_graph.svg", width=500)
    st.write("點擊左側選單進入 `📊 AD-AS 模擬` 頁面！")

# 📊 **AD-AS 模擬**
elif page == "📊 AD-AS 模擬":
    st.title("📊 AD-AS 模型互動模擬")

    # 讓使用者選擇經濟場景
    scenario = st.selectbox("選擇經濟情境", ["正常狀態", "需求衝擊（經濟繁榮）", "供給衝擊（成本上升）"])

    # 變數控制（使用者輸入）
    col1, col2 = st.columns(2)
    with col1:
        G = st.slider("政府支出 (G)", min_value=50, max_value=300, value=100, step=10)
    with col2:
        M = st.slider("貨幣供給 (M)", min_value=50, max_value=300, value=100, step=10)

    # 計算 AD 曲線
    a, b = 1.5, 0.8  # 假設係數
    GDP_ad = a * G + b * M

    # 設定 AS 曲線（根據場景調整）
    GDP_range = np.linspace(50, 500, 100)
    if scenario == "正常狀態":
        AS_curve = 0.02 * GDP_range**1.2  
    elif scenario == "需求衝擊（經濟繁榮）":
        AS_curve = 0.015 * GDP_range**1.1  # 需求上升，價格影響較小
    elif scenario == "供給衝擊（成本上升）":
        AS_curve = 0.03 * GDP_range**1.3  # 供給面受影響，通膨加劇

    # 繪製圖表
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(GDP_range, AS_curve, label="AS 總供給", color="blue", linewidth=2)
    ax.axvline(GDP_ad, color="red", linestyle="--", label="AD 總需求 (調整後)")
    ax.set_xlabel("GDP", fontsize=12)
    ax.set_ylabel("價格水準", fontsize=12)
    ax.set_title(f"AD-AS 模型（{scenario}）", fontsize=14)
    ax.legend()
    ax.grid(alpha=0.3)

    # 顯示圖表
    st.pyplot(fig)

    # 顯示結果
    st.success(f"💡 **調整後的 GDP 平衡點**：{GDP_ad:.2f}")

    # ✨ **模型說明區**
    with st.expander("📖 什麼是 AD-AS 模型？"):
        st.write("""
        **AD-AS 模型**（總需求-總供給模型）是經濟學中的一個重要框架，描述了整個經濟體系的價格水準與 GDP 之間的關係。

        - **AD (Aggregate Demand)**：總需求，由政府支出 (G)、貨幣供給 (M)、投資、消費等決定。
        - **AS (Aggregate Supply)**：總供給，受生產成本、技術水準、勞動市場等影響。

        在這個模型中：
        - **需求增加**（如政府擴大支出）會讓 **AD 右移**，提高 GDP 和通膨率。
        - **供給衝擊**（如成本上升）會讓 **AS 左移**，可能導致滯脹（Stagflation）。

        📌 你可以調整 **G（政府支出）** 和 **M（貨幣供給）**，觀察總體經濟的變化！
        """)
# 乘數效應與模式區別
elif page == "乘數效應與模式區別":
    st.title("🔍 乘數效應與模式區別")
    st.write("這裡解釋需求衝擊、供給衝擊與短期/長期影響的區別。")

    st.subheader("📌 需求乘數")
    st.latex(r"M = \frac{1}{1 - MPC}")
    st.write("MPC（邊際消費傾向）越高，乘數效果越大。")

    st.subheader("📌 供給衝擊的影響")
    st.write("供給衝擊沒有固定乘數，但可能導致成本上升與滯脹。")

# 需求衝擊 vs. 供給衝擊
elif page == "需求衝擊 vs. 供給衝擊":
    st.title("⚖️ 需求衝擊 vs. 供給衝擊")
    
    with st.expander("🔍 需求衝擊案例"):
        st.write("2020 COVID-19 刺激方案 → AD 右移 → GDP 上升，但通膨壓力增加")
        st.write("2008 金融危機 → 投資崩潰 → AD 左移 → GDP 下降，通縮風險")

    with st.expander("⚡ 供給衝擊案例"):
        st.write("1970s 石油危機 → AS 左移 → 物價上升，GDP 下降（滯脹）")
        st.write("2022 供應鏈危機 → AS 左移 → 生產成本上升，通膨加劇")

# 短期 vs. 長期 AS
elif page == "短期 vs. 長期 AS":
    st.title("📈 短期 vs. 長期 AS 曲線")

    show_lras = st.checkbox("顯示長期 AS (LRAS)")
    
    if show_lras:
        st.write("LRAS 是一條垂直線，表示長期 GDP 取決於生產力，而非物價。")
    else:
        st.write("短期 AS 會受到價格變動影響，呈現向右上傾斜的形狀。")

# 約翰·梅納德·凱因斯
elif page == "約翰·梅納德·凱因斯":
    st.title("約翰·梅納德·凱因斯")

    st.write("20世紀最具影響力的經濟學家之一，被譽為現代宏觀經濟學的奠基人。他在《就業、利息和貨幣通論》中挑戰了古典經濟學，提出總需求是決定經濟活動和就業水平的關鍵，並強調政府在應對經濟衰退中的積極作用。他的理論深刻影響了戰後的全球經濟政策，並在經濟危機時期為政策制定者提供了重要指引。*")
    image_url= "https://drive.google.com/file/d/1tuvlYa9QRmwqXRGpFirVp_z7zV0LFplg/view?usp=drive_link"
    st.image("https://zh.wikipedia.org/zh-tw/%E7%BA%A6%E7%BF%B0%C2%B7%E6%A2%85%E7%BA%B3%E5%BE%B7%C2%B7%E5%87%AF0")
    st.image(image_url, width=500)

