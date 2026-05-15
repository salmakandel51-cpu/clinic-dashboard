import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
 
# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clinic Dashboard",
    page_icon="🏥",
    layout="wide"
)
 
# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;600;700&family=DM+Mono&display=swap');
    
    * { font-family: 'DM Sans', sans-serif; }
    
    .main { background: #F8FAFC; }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border-left: 4px solid #2E86AB;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1A1A2E;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-delta {
        font-size: 0.85rem;
        color: #10B981;
        font-weight: 600;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1A1A2E;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #E2E8F0;
    }
    .insight-box {
        background: linear-gradient(135deg, #1E3A5F, #2D1B4E);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        border-left: 3px solid #2E86AB;
        font-size: 0.9rem;
        color: #F1F5F9;
    }
    .stPlotlyChart { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)
 
# ── Data ──────────────────────────────────────────────────────────────────────
months       = np.array(["Jan","Feb","Mar","Apr","May","Jun",
                          "Jul","Aug","Sep","Oct","Nov","Dec"])
patients     = np.array([130,115,125,120,110,90,85,95,115,140,155,160])
revenue      = np.array([32500,28750,31250,30000,27500,22500,
                          21250,23750,28750,35000,38750,40000])
costs        = np.array([21125,18688,20313,19500,17875,14625,
                          13813,15438,18688,22750,25188,26000])
service_type = np.array(["Consultation","Lab Tests","Consultation","X-Ray",
                          "Consultation","Lab Tests","X-Ray","Consultation",
                          "Lab Tests","Consultation","X-Ray","Lab Tests"])
 
# ── Calculations ──────────────────────────────────────────────────────────────
profit              = revenue - costs
profit_margin       = (profit / revenue) * 100
avg_patients        = np.mean(patients)
above_avg_mask      = patients > avg_patients
growth              = np.diff(revenue) / revenue[:-1] * 100
cumulative_revenue  = np.cumsum(revenue)
rev_per_patient     = revenue / patients
 
# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🏥 Clinic Annual Dashboard")
st.markdown("**Yearly performance analysis · Built with NumPy & Plotly**")
st.markdown("---")
 
# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
 
with c1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">{revenue.sum()/1000:.0f}K</div>
        <div class="metric-delta">EGP · Full Year</div>
    </div>""", unsafe_allow_html=True)
 
with c2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Profit</div>
        <div class="metric-value">{profit.sum()/1000:.0f}K</div>
        <div class="metric-delta">↑ {profit_margin.mean():.1f}% avg margin</div>
    </div>""", unsafe_allow_html=True)
 
with c3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Patients</div>
        <div class="metric-value">{patients.sum():,}</div>
        <div class="metric-delta">Avg {avg_patients:.0f}/month</div>
    </div>""", unsafe_allow_html=True)
 
with c4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Revenue / Patient</div>
        <div class="metric-value">{rev_per_patient.mean():.0f}</div>
        <div class="metric-delta">EGP per visit</div>
    </div>""", unsafe_allow_html=True)
 
# ── Chart 1: Revenue vs Costs ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Revenue vs Costs vs Profit</div>', unsafe_allow_html=True)
 
fig1 = go.Figure()
fig1.add_trace(go.Bar(name="Revenue", x=months, y=revenue,
    marker_color="#2E86AB", opacity=0.9))
fig1.add_trace(go.Bar(name="Costs", x=months, y=costs,
    marker_color="#E84855", opacity=0.8))
fig1.add_trace(go.Scatter(name="Profit", x=months, y=profit,
    mode="lines+markers", line=dict(color="#10B981", width=3),
    marker=dict(size=8)))
fig1.update_layout(
    barmode="group", plot_bgcolor="#1E293B", paper_bgcolor="#1E293B",
    height=380, margin=dict(t=20, b=20),
    legend=dict(orientation="h", y=1.1),
    yaxis=dict(gridcolor="#334155", color="#E2E8F0"),
    font=dict(family="DM Sans", color="#E2E8F0")
)
st.plotly_chart(fig1, use_container_width=True)
 
# ── Chart 2: Patients + Above Average ─────────────────────────────────────────
col1, col2 = st.columns(2)
 
with col1:
    st.markdown('<div class="section-title">👥 Patients — Above vs Below Average</div>', unsafe_allow_html=True)
    colors = ["#2E86AB" if v else "#CBD5E1" for v in above_avg_mask]
    fig2 = go.Figure(go.Bar(
        x=months, y=patients,
        marker_color=colors,
        textfont=dict(color="#E2E8F0"),
        text=patients, textposition="outside"
    ))
    fig2.add_hline(y=avg_patients, line_dash="dash",
                   line_color="#E84855", annotation_text=f"Avg: {avg_patients:.0f}")
    fig2.update_layout(
        plot_bgcolor="#1E293B", paper_bgcolor="#1E293B",
        height=320, margin=dict(t=20, b=20),
        yaxis=dict(gridcolor="#334155", color="#E2E8F0"),
        font=dict(family="DM Sans", color="#E2E8F0")
    )
    st.plotly_chart(fig2, use_container_width=True)
 
with col2:
    st.markdown('<div class="section-title">📈 Monthly Growth Rate (%)</div>', unsafe_allow_html=True)
    growth_colors = ["#10B981" if g > 0 else "#E84855" for g in growth]
    fig3 = go.Figure(go.Bar(
        x=months[1:], y=growth,
        marker_color=growth_colors,
        text=[f"{g:.1f}%" for g in growth],
        textposition="outside"
    ))
    fig3.add_hline(y=0, line_color="#94A3B8")
    fig3.update_layout(
        plot_bgcolor="#1E293B", paper_bgcolor="#1E293B",
        height=320, margin=dict(t=20, b=20),
        yaxis=dict(gridcolor="#334155", color="#E2E8F0", ticksuffix="%"),
        font=dict(family="DM Sans", color="#E2E8F0")
    )
    st.plotly_chart(fig3, use_container_width=True)
 
# ── Chart 3: Cumulative Revenue + Service Type ────────────────────────────────
col3, col4 = st.columns(2)
 
with col3:
    st.markdown('<div class="section-title">💰 Cumulative Revenue</div>', unsafe_allow_html=True)
    fig4 = go.Figure(go.Scatter(
        x=months, y=cumulative_revenue,
        fill="tozeroy", fillcolor="rgba(46,134,171,0.15)",
        line=dict(color="#2E86AB", width=3),
        mode="lines+markers", marker=dict(size=8, color="#2E86AB")
    ))
    fig4.update_layout(
        plot_bgcolor="#1E293B", paper_bgcolor="#1E293B",
        height=300, margin=dict(t=20, b=20),
        yaxis=dict(gridcolor="#334155", color="#E2E8F0"),
        font=dict(family="DM Sans", color="#E2E8F0")
    )
    st.plotly_chart(fig4, use_container_width=True)
 
with col4:
    st.markdown('<div class="section-title">🩺 Revenue by Service Type</div>', unsafe_allow_html=True)
    services = {}
    for s, r in zip(service_type, revenue):
        services[s] = services.get(s, 0) + r
    fig5 = go.Figure(go.Pie(
        labels=list(services.keys()),
        values=list(services.values()),
        hole=0.45,
        marker_colors=["#2E86AB", "#E84855", "#F59E0B"]
    ))
    fig5.update_layout(
        height=300, margin=dict(t=20, b=20),
        font=dict(family="DM Sans", color="#E2E8F0"),
        paper_bgcolor="#1E293B"
    )
    st.plotly_chart(fig5, use_container_width=True)
 
# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">💡 Key Insights</div>', unsafe_allow_html=True)
 
best  = months[np.argmax(revenue)]
worst = months[np.argmin(revenue)]
best_growth_month = months[np.argmax(growth) + 1]
above_count = above_avg_mask.sum()
 
st.markdown(f'<div class="insight-box">🏆 <b>Best month:</b> {best} with {revenue.max():,} EGP revenue</div>', unsafe_allow_html=True)
st.markdown(f'<div class="insight-box">📉 <b>Lowest month:</b> {worst} — likely summer slowdown (Jul/Aug effect)</div>', unsafe_allow_html=True)
st.markdown(f'<div class="insight-box">🚀 <b>Highest growth:</b> {best_growth_month} with +{growth.max():.1f}% month-over-month</div>', unsafe_allow_html=True)
st.markdown(f'<div class="insight-box">👥 <b>{above_count} months</b> exceeded the average of {avg_patients:.0f} patients/month</div>', unsafe_allow_html=True)
 
st.markdown("---")
st.markdown("<center><small>Built with NumPy · Plotly · Streamlit &nbsp;|&nbsp; github.com/your-username</small></center>", unsafe_allow_html=True)
