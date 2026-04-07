import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 字型設定
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang TC", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="AD-AS 模型互動模擬", layout="centered")


# -----------------------------
# 模型函數
# -----------------------------
def ad_curve(Y, A=120, m=0.12):
    """
    AD 曲線（向右下傾斜）
    P = A - mY

    A 越大，AD 越右移
    m 為斜率大小
    """
    return A - m * Y


def sras_curve(Y, Pe=20, lam=0.08, Yn=500, shock=0):
    """
    短期總供給 SRAS（向右上傾斜）
    P = Pe + λ(Y - Yn) + shock

    shock > 0 代表負向供給衝擊（成本上升，SRAS 上移/左移）
    shock < 0 代表正向供給衝擊（成本下降，SRAS 下移/右移）
    """
    return Pe + lam * (Y - Yn) + shock


def solve_equilibrium(A, m, Pe, lam, Yn, shock):
    """
    解 AD = SRAS
    A - mY = Pe + λ(Y - Yn) + shock

    => Y* = [A - Pe + λYn - shock] / (m + λ)
    => P* = AD(Y*)
    """
    Y_star = (A - Pe + lam * Yn - shock) / (m + lam)
    P_star = ad_curve(Y_star, A, m)
    return Y_star, P_star


# -----------------------------
# 側邊欄頁面
# -----------------------------
page = st.sidebar.selectbox(
    "選擇主題",
    ["🏠 首頁", "📊 AD-AS 模擬", "乘數效應與模式區別", "需求衝擊 vs. 供給衝擊", "短期 vs. 長期 AS", "約翰·梅納德·凱因斯"]
)

# -----------------------------
# 首頁
# -----------------------------
if page == "🏠 首頁":
    st.title("📈 總體經濟學 AD-AS 模型互動模擬")
    st.write("""
這個應用程式可以幫助你理解：

- **AD（總需求）** 如何受政策影響而移動
- **AS（總供給）** 如何受成本與預期影響而移動
- **均衡產出 Y 與物價 P** 如何改變
""")

    st.markdown("""
**你可以觀察：**
- 政府支出增加，AD 如何右移
- 貨幣供給增加，AD 如何右移
- 成本上升時，SRAS 如何左移
- 長期均衡時，LRAS 為什麼是一條垂直線
""")

    st.info("請從左側選單進入「📊 AD-AS 模擬」頁面。")


# -----------------------------
# AD-AS 模擬
# -----------------------------
elif page == "📊 AD-AS 模擬":
    st.title("📊 AD-AS 模型互動模擬")

    scenario = st.selectbox(
        "選擇經濟情境",
        ["正常狀態", "需求衝擊（經濟繁榮）", "供給衝擊（成本上升）"]
    )

    col1, col2 = st.columns(2)
    with col1:
        G = st.slider("政府支出 (G)", min_value=50, max_value=300, value=100, step=10)
    with col2:
        M = st.slider("貨幣供給 (M)", min_value=50, max_value=300, value=100, step=10)

    show_lras = st.checkbox("顯示長期 AS (LRAS)", value=True)

    # ---- AD 參數 ----
    # 讓正常情況下的均衡點不要離 Yn 太遠
    A_base = 70
    A = A_base + 0.10 * G + 0.05 * M
    m = 0.10

    # ---- SRAS 參數 ----
    Pe = 20
    lam = 0.08
    Yn = 500
    shock = 0

    # 情境調整
    if scenario == "正常狀態":
        shock = 0
    elif scenario == "需求衝擊（經濟繁榮）":
        A += 18
    elif scenario == "供給衝擊（成本上升）":
        shock = 12

    # 先算均衡點
    Y_star, P_star = solve_equilibrium(A, m, Pe, lam, Yn, shock)

    # 根據均衡點自動決定畫圖範圍，避免交點跑到圖外
    x_min = 100
    x_max = max(900, Y_star + 120, Yn + 120)
    Y_range = np.linspace(x_min, x_max, 400)

    AD = ad_curve(Y_range, A, m)
    SRAS = sras_curve(Y_range, Pe, lam, Yn, shock)

    # 畫圖
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Y_range, AD, label="AD 總需求", linewidth=2)
    ax.plot(Y_range, SRAS, label="SRAS 短期總供給", linewidth=2)

    if show_lras:
        ax.axvline(Yn, linestyle="--", label="LRAS 長期總供給")

    ax.scatter(
        Y_star, P_star,
        color="black",
        zorder=5,
        label=f"均衡點 (Y*={Y_star:.1f}, P*={P_star:.1f})"
    )

    ax.set_xlabel("實質產出 Y")
    ax.set_ylabel("物價水準 P")
    ax.set_title(f"AD-AS 模型（{scenario}）")
    ax.grid(alpha=0.3)
    ax.legend()

    # 固定顯示範圍，避免均衡點或曲線被擠掉
    ax.set_xlim(x_min, x_max)
    y_min = min(AD.min(), SRAS.min(), P_star) - 10
    y_max = max(AD.max(), SRAS.max(), P_star) + 10
    ax.set_ylim(y_min, y_max)

    st.pyplot(fig)

    st.success(f"💡 均衡產出：Y* = {Y_star:.2f}；均衡物價：P* = {P_star:.2f}")

    # 加一小段情境解讀
    if scenario == "正常狀態":
        st.info("正常狀態下，均衡點通常應相對接近潛在產出 Yn。")
    elif scenario == "需求衝擊（經濟繁榮）":
        st.info("需求衝擊下，AD 右移，通常會帶來更高的產出與物價。")
    elif scenario == "供給衝擊（成本上升）":
        st.info("供給衝擊下，SRAS 左移，通常會造成產出下降、物價上升。")

    with st.expander("📖 什麼是 AD-AS 模型？"):
        st.write("""
**AD-AS 模型**用來分析整體經濟中的產出與物價。

- **AD（總需求）**：反映整體經濟對商品與服務的需求，通常向右下傾斜
- **SRAS（短期總供給）**：反映企業在短期願意供給的產出，通常向右上傾斜
- **LRAS（長期總供給）**：反映經濟的潛在產出，通常畫成垂直線

在這個模型中：
- **G 或 M 增加**，通常會讓 **AD 右移**
- **成本上升**，通常會讓 **SRAS 左移**
- 交點代表短期均衡的 **產出與物價**
""")

# -----------------------------
# 乘數效應與模式區別
# -----------------------------
elif page == "乘數效應與模式區別":
    st.title("🔍 乘數效應與模式區別")

    st.subheader("📌 需求乘數")
    st.latex(r"k = \frac{1}{1 - MPC}")
    st.write("""
這裡的乘數是凱因斯式需求分析中的核心概念。  
當 **MPC（邊際消費傾向）** 越高，政府支出增加所帶來的總需求擴張效果通常越大。
""")

    st.subheader("📌 AD-AS 與 45 度線模型的差別")
    st.write("""
- **45 度線模型**：重點是產出如何由總需求決定
- **IS-LM 模型**：加入利率與貨幣市場
- **AD-AS 模型**：進一步加入物價水準，分析通膨與產出的互動
""")

    st.subheader("📌 供給衝擊的特徵")
    st.write("""
供給衝擊通常不是「固定乘數」效果，而是透過生產成本、能源價格、技術條件等因素改變總供給。  
負向供給衝擊常造成：
- 物價上升
- 產出下降
- 形成滯脹壓力
""")


# -----------------------------
# 需求衝擊 vs. 供給衝擊
# -----------------------------
elif page == "需求衝擊 vs. 供給衝擊":
    st.title("⚖️ 需求衝擊 vs. 供給衝擊")

    with st.expander("🔍 需求衝擊案例"):
        st.write("""
**需求衝擊** 是指 AD 發生移動。
常見情況：
- 政府擴張支出
- 貨幣供給增加
- 民間投資或消費信心提升

典型效果：
- AD 右移
- 產出上升
- 物價上升
""")

    with st.expander("⚡ 供給衝擊案例"):
        st.write("""
**供給衝擊** 是指 SRAS 發生移動。
常見情況：
- 油價上漲
- 原料成本上升
- 供應鏈中斷
- 天災或戰爭影響生產

典型效果：
- SRAS 左移
- 物價上升
- 產出下降
- 容易形成滯脹
""")

    st.info("簡單記：需求衝擊主要看 AD，供給衝擊主要看 SRAS。")


# -----------------------------
# 短期 vs. 長期 AS
# -----------------------------
elif page == "短期 vs. 長期 AS":
    st.title("📈 短期 vs. 長期 AS 曲線")

    Yn = st.slider("潛在產出 Yn", min_value=300, max_value=700, value=500, step=20)
    Pe = st.slider("預期物價 Pe", min_value=10, max_value=40, value=20, step=2)
    lam = st.slider("SRAS 斜率 λ", min_value=0.03, max_value=0.20, value=0.08, step=0.01)

    Y_range = np.linspace(100, 900, 400)
    SRAS = sras_curve(Y_range, Pe=Pe, lam=lam, Yn=Yn, shock=0)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Y_range, SRAS, label="SRAS 短期總供給", linewidth=2)
    ax.axvline(Yn, linestyle="--", label="LRAS 長期總供給")

    ax.set_xlabel("實質產出 Y")
    ax.set_ylabel("物價水準 P")
    ax.set_title("短期 AS 與長期 AS")
    ax.grid(alpha=0.3)
    ax.legend()

    st.pyplot(fig)

    st.write("""
- **SRAS**：短期內工資、價格調整不完全，因此通常向右上傾斜  
- **LRAS**：長期產出取決於勞動、資本、技術與制度，因此通常畫成垂直線
""")


# -----------------------------
# 凱因斯介紹
# -----------------------------
elif page == "約翰·梅納德·凱因斯":
    st.title("約翰·梅納德·凱因斯")

    st.write("""
約翰·梅納德·凱因斯（John Maynard Keynes）是 20 世紀最具影響力的經濟學家之一，常被視為現代宏觀經濟學的重要奠基者。

他強調：
- 總需求會影響產出與就業
- 市場不一定能自動迅速恢復充分就業
- 在經濟衰退時，政府可以透過財政政策穩定景氣

他的思想深刻影響了後來的總體經濟學、景氣政策與政府干預理論。
""")

    st.caption("若要加入圖片，建議改用本機圖片檔，或使用直接的圖片網址。")

st.sidebar.write("🔹 選擇不同的頁面來學習 AD-AS 模型！")