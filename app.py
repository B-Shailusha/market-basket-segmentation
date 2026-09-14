import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_URL ="http://127.0.0.1:8000" 

st.set_page_config(
    page_title="Market Basket Segmentation",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}
.hero h1 { font-size: 2.8rem; font-weight: 800; margin: 0; letter-spacing: -1px; }
.hero p  { font-size: 1.1rem; opacity: 0.75; margin-top: 0.5rem; }

.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    border: 1px solid #f0f0f0;
    height: 100%;
}

.segment-result {
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    color: white;
    margin-top: 1rem;
}
.segment-result h2 { font-size: 2rem; font-weight: 800; margin: 0.5rem 0; }
.segment-result p  { font-size: 1rem; opacity: 0.9; }

.metric-box {
    background: #f8f9ff;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    border: 1px solid #e8ecff;
}
.metric-box .label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
.metric-box .value { font-size: 1.6rem; font-weight: 700; color: #1a1a2e; }

.strategy-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    color: white;
    margin-top: 1rem;
}
.strategy-box h4 { margin: 0 0 0.4rem; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; }
.strategy-box p  { margin: 0; font-size: 0.95rem; }

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

.sidebar-info {
    background: #f8f9ff;
    border-radius: 12px;
    padding: 1rem;
    font-size: 0.85rem;
    color: #555;
    margin-top: 1rem;
    border-left: 4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🛍️ Market Basket Segmentation</h1>
    <p>K-Means Clustering · 6 Customer Segments · Powered by Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎯 Predict Segment", "📊 Segment Explorer", "ℹ️ About"])

# ─────────────────────────── TAB 1 : PREDICT ─────────────────────────────────
with tab1:
    st.markdown("### Enter Customer Profile")
    st.markdown("Adjust the values below to match the customer's profile, then click **Predict**.")

    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💰 Financial & Shopping")
        income = st.slider("Annual Income ($)", 5_000, 200_000, 60_000, step=1_000,
                           help="Customer's yearly household income")
        total_spending = st.slider("Total Spending ($)", 0, 2_500, 800, step=10,
                                   help="Total amount spent across all product categories in the last 2 years")
        st.markdown("#### 🛒 Purchase Channels")
        store_purchases = st.slider("Store Purchases", 0, 15, 6,
                                    help="Number of purchases made directly in stores")
        web_purchases = st.slider("Web Purchases", 0, 27, 5,
                                  help="Number of purchases made through the company's website")
        st.markdown("#### 📅 Engagement")
        web_visits = st.slider("Web Visits / Month", 0, 20, 5,
                               help="Number of visits to the company's website in the last month")
        recency = st.slider("Recency (days since last purchase)", 0, 99, 30,
                            help="Days elapsed since the customer's last purchase — lower = more recent")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Profile Summary")

        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Annual Income</div>
                <div class="value">${income:,}</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Total Spending</div>
                <div class="value">${total_spending:,}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        m3, m4 = st.columns(2)
        with m3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Store Purchases</div>
                <div class="value">{store_purchases}</div>
            </div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Web Purchases</div>
                <div class="value">{web_purchases}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        m5, m6 = st.columns(2)
        with m5:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Web Visits/Month</div>
                <div class="value">{web_visits}</div>
            </div>""", unsafe_allow_html=True)
        with m6:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Recency (days)</div>
                <div class="value">{recency}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Radar chart preview
        categories = ["Income", "Spending", "Store", "Web Buys", "Web Visits", "Recency"]
        norm_values = [
            income / 200_000,
            total_spending / 2_500,
            store_purchases / 15,
            web_purchases / 27,
            web_visits / 20,
            1 - (recency / 99),
        ]
        fig_radar = go.Figure(go.Scatterpolar(
            r=norm_values + [norm_values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(102,126,234,0.25)",
            line=dict(color="#667eea", width=2),
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20),
            height=220,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔮 Predict Customer Segment", use_container_width=True)

    if predict_btn:
        payload = {
            "income": income,
            "total_spending": total_spending,
            "num_web_purchases": web_purchases,
            "num_store_purchases": store_purchases,
            "num_web_visits_month": web_visits,
            "recency": recency,
        }
        try:
            with st.spinner("Analyzing customer profile…"):
                resp = requests.post(f"{API_URL}/predict", json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                color = data["color"]
                st.markdown(f"""
                <div class="segment-result" style="background: linear-gradient(135deg, {color}cc, {color}88);">
                    <div style="font-size:3.5rem;">{data['emoji']}</div>
                    <h2>Cluster {data['cluster']} · {data['segment_name']}</h2>
                    <p>{data['description']}</p>
                </div>""", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="strategy-box">
                    <h4>📣 Recommended Marketing Strategy</h4>
                    <p>{data['marketing_strategy']}</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.error(f"API error {resp.status_code}: {resp.text}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the API. Make sure the Render service is running and the URL is correct.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# ─────────────────────────── TAB 2 : EXPLORER ────────────────────────────────
with tab2:
    st.markdown("### 📊 All 6 Customer Segments")

    try:
        resp_seg = requests.get(f"{API_URL}/segments", timeout=10)
        if resp_seg.status_code == 200:
            segments = resp_seg.json()
        else:
            raise ValueError("bad status")
    except Exception:
        segments = {
            "0": {"name": "Premium In-Store Loyalists",    "emoji": "🏆", "color": "#FFD700",
                  "description": "High-income, high-spending, in-store focused.",
                  "strategy": "Loyalty programs & premium offers."},
            "1": {"name": "Budget-Conscious Browsers",     "emoji": "🔍", "color": "#87CEEB",
                  "description": "Low income, high web visits, low purchases.",
                  "strategy": "Flash sales & cart-abandonment campaigns."},
            "2": {"name": "Omnichannel Mid-Spenders",      "emoji": "🛒", "color": "#90EE90",
                  "description": "Mid-income, shops both online and in-store.",
                  "strategy": "Cross-channel loyalty points."},
            "3": {"name": "High-Value Digital Shoppers",   "emoji": "💻", "color": "#DDA0DD",
                  "description": "High income, prefers web purchases.",
                  "strategy": "Personalized online recommendations."},
            "4": {"name": "Affluent Occasional Buyers",    "emoji": "💎", "color": "#FFA07A",
                  "description": "High income but high recency — at risk of drifting.",
                  "strategy": "Win-back & seasonal exclusive offers."},
            "5": {"name": "Low-Engagement At-Risk",        "emoji": "⚠️", "color": "#F08080",
                  "description": "Low income, low spending, high recency.",
                  "strategy": "Re-engagement discounts & surveys."},
        }

    rows = [segments[k] if isinstance(k, str) else segments[str(k)] for k in sorted(segments.keys(), key=int)]

    for i in range(0, 6, 3):
        cols = st.columns(3, gap="medium")
        for j, col in enumerate(cols):
            if i + j >= len(rows):
                break
            seg = rows[i + j]
            with col:
                st.markdown(f"""
                <div class="card" style="border-top: 5px solid {seg['color']};">
                    <div style="font-size:2rem;">{seg['emoji']}</div>
                    <h4 style="margin:0.3rem 0 0.6rem; color:#1a1a2e;">{seg['name']}</h4>
                    <p style="font-size:0.88rem; color:#555; margin-bottom:0.8rem;">{seg['description']}</p>
                    <div style="background:#f8f9ff; border-radius:8px; padding:0.7rem; font-size:0.82rem; color:#444;">
                        <strong>Strategy:</strong> {seg['strategy']}
                    </div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Cluster size bar chart (from notebook data)
    st.markdown("### Cluster Distribution (Training Data)")
    cluster_sizes = pd.DataFrame({
        "Cluster": [f"Cluster {i}" for i in range(6)],
        "Size": [301, 513, 312, 267, 327, 492],
        "Segment": [rows[i]["name"] for i in range(6)],
        "Color": [rows[i]["color"] for i in range(6)],
    })
    fig_bar = px.bar(
        cluster_sizes, x="Cluster", y="Size", color="Cluster",
        color_discrete_sequence=cluster_sizes["Color"].tolist(),
        text="Size", custom_data=["Segment"],
        labels={"Size": "Number of Customers"},
    )
    fig_bar.update_traces(textposition="outside",
                          hovertemplate="<b>%{x}</b><br>%{customdata[0]}<br>Customers: %{y}<extra></extra>")
    fig_bar.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
                          yaxis=dict(gridcolor="#f0f0f0"), margin=dict(t=20))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Feature comparison radar
    st.markdown("### Cluster Feature Profiles (Normalized)")
    feature_labels = ["Income", "Total Spending", "Web Purchases", "Store Purchases", "Web Visits", "Recency ↓"]
    profiles = {
        "Cluster 0": [76159, 1245, 4.8, 8.6, 2.7, 20],
        "Cluster 1": [32273,   82, 1.8, 3.0, 6.5, 26],
        "Cluster 2": [51507,  544, 6.3, 6.0, 6.8, 34],
        "Cluster 3": [64330, 1110, 8.2, 9.4, 5.9, 62],
        "Cluster 4": [74986, 1232, 4.3, 8.1, 2.4, 73],
        "Cluster 5": [35948,  117, 2.2, 3.4, 6.4, 77],
    }
    maxes = [200_000, 2_500, 27, 15, 20, 99]
    colors_hex = [rows[i]["color"] for i in range(6)]

    fig_multi = go.Figure()
    for idx, (name, vals) in enumerate(profiles.items()):
        norm = [v / m for v, m in zip(vals, maxes)]
        norm[-1] = 1 - norm[-1]
        fig_multi.add_trace(go.Scatterpolar(
            r=norm + [norm[0]],
            theta=feature_labels + [feature_labels[0]],
            fill="toself",
            name=name,
            line=dict(color=colors_hex[idx], width=2),
            fillcolor=colors_hex[idx] + "33",
        ))
    fig_multi.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)),
        legend=dict(orientation="h", y=-0.15),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_multi, use_container_width=True)

# ─────────────────────────── TAB 3 : ABOUT ───────────────────────────────────
with tab3:
    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        st.markdown("""
### About This Project

**Market Basket Segmentation Using K-Means Clustering** groups customers of a retail company
into six distinct segments based on their purchasing behavior, income, and channel preferences.

#### Dataset
- **Source:** Customer Personality Analysis dataset
- **Records:** 2,240 customers · 29 original features
- **After cleaning:** 2,212 customers

#### Features Used for Clustering
| Feature | Description |
|---|---|
| Income | Annual household income |
| Total Spending | Sum across all product categories |
| Web Purchases | Online channel purchases |
| Store Purchases | In-store purchases |
| Web Visits/Month | Website engagement |
| Recency | Days since last purchase |

#### Methodology
1. **Preprocessing** — dropped 24 missing income rows, removed outliers (age > 90, income > 200k)
2. **Feature Engineering** — derived Total_Spending, Total_Purchases, AcceptedAny
3. **Scaling** — StandardScaler (zero mean, unit variance)
4. **Optimal k** — Elbow Method + Silhouette Score → **k = 6**
5. **Algorithm** — K-Means++ initialization, 10 restarts
""")
    with c2:
        st.markdown("""
### Model Performance

| Metric | Value |
|---|---|
| Algorithm | K-Means++ |
| Clusters (k) | 6 |
| Silhouette Score | 0.234 |
| PCA Variance (2D) | 69.5% |
| Training Samples | 2,212 |

### Tech Stack
- **Backend:** FastAPI + scikit-learn (Render)
- **Frontend:** Streamlit + Plotly
- **Model:** KMeans (joblib serialized)

### Cluster Sizes
""")
        sizes_df = pd.DataFrame({
            "Segment": [f"Cluster {i} · {rows[i]['name']}" for i in range(6)],
            "Customers": [301, 513, 312, 267, 327, 492],
        })
        st.dataframe(sizes_df, use_container_width=True, hide_index=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#aaa; font-size:0.82rem;'>"
    "Market Basket Segmentation · K-Means Clustering · Think Champ Internship Project"
    "</p>",
    unsafe_allow_html=True,
)
