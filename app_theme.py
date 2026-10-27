import streamlit as st
import plotly.graph_objects as go

def apply_app_theme():
    """Applies modern light styling, Tailwind CSS utilities, and custom typography."""
    st.markdown(
        """
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

        <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --primary-light: #eef2ff;
            --surface: #ffffff;
            --background: #f8fafc;
            --border: #e2e8f0;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --success: #10b981;
            --success-light: #ecfdf5;
            --warning: #f59e0b;
        }

        /* Base Typography & Background */
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: var(--text-main);
            background-color: var(--background);
        }

        /* Top Header & Toolbar Clean */
        [data-testid="stHeader"] {
            background: rgba(248, 250, 252, 0.85);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--border);
        }

        /* Container Padding */
        .block-container {
            max-width: 1240px;
            padding-top: 1.75rem !important;
            padding-bottom: 3.5rem !important;
        }

        /* Modern Sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.15rem 1.25rem;
            box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05);
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.08);
            border-color: #cbd5e1;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.825rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted) !important;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.85rem !important;
            color: #1e293b !important;
        }

        /* Modern Buttons */
        .stButton > button, [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
            color: #ffffff !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 0.65rem 1.5rem !important;
            min-height: 2.75rem !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #4338ca 0%, #3730a3 100%) !important;
            box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35) !important;
            transform: translateY(-1px);
        }

        /* Modern Form Container */
        [data-testid="stForm"] {
            background-color: #ffffff;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.75rem;
            box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.06);
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f1f5f9;
            padding: 6px;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 8px 18px;
            font-weight: 600;
            color: #64748b;
            background-color: transparent;
            border: none !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #4f46e5 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        }

        /* Input Controls */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border-radius: 10px !important;
            border-color: #e2e8f0 !important;
            background-color: #ffffff !important;
        }
        div[data-baseweb="select"]:hover,
        div[data-baseweb="input"]:hover {
            border-color: #cbd5e1 !important;
        }

        /* Plotly and Dataframe containers */
        [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {
            background-color: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.5rem;
            box-shadow: 0 2px 10px -2px rgba(15, 23, 42, 0.04);
        }

        /* Custom Card Elements */
        .hero-banner {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 2rem 2.25rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
            position: relative;
            overflow: hidden;
        }
        .hero-banner::after {
            content: "";
            position: absolute;
            top: 0;
            right: 0;
            width: 280px;
            height: 100%;
            background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.08), transparent 70%);
            pointer-events: none;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background-color: #eef2ff;
            color: #4f46e5;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
            border: 1px solid #c7d2fe;
        }
        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.35rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.15;
            margin: 0;
            letter-spacing: -0.02em;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #64748b;
            margin-top: 0.65rem;
            max-width: 48rem;
            line-height: 1.5;
        }
        .insight-callout {
            background-color: #f8fafc;
            border-left: 4px solid #4f46e5;
            border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem;
            margin-top: 0.75rem;
            margin-bottom: 1.5rem;
            border-top: 1px solid #f1f5f9;
            border-right: 1px solid #f1f5f9;
            border-bottom: 1px solid #f1f5f9;
        }
        .badge-pill {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_page_header(badge: str, title: str, subtitle: str):
    """Renders a consistent, high-end hero header."""
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-badge">
                <span class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                {badge}
            </div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_takeaway(takeaway_text: str, title: str = "Key Business Takeaway"):
    """Renders a friendly non-technical takeaway box."""
    st.markdown(
        f"""
        <div class="insight-callout">
            <div style="font-weight: 700; color: #1e293b; font-size: 0.9rem; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                <span>💡</span> {title}
            </div>
            <div style="color: #475569; font-size: 0.92rem; line-height: 1.5;">
                {takeaway_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def get_plotly_layout_defaults():
    """Consistent, clean, non-technical Plotly layout settings."""
    return dict(
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155", size=12),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=35, b=25),
        hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_color="#ffffff", font_family="Plus Jakarta Sans"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            linecolor="#cbd5e1",
            tickfont=dict(color="#64748b", size=11),
            title_font=dict(size=12, color="#334155", family="Plus Jakarta Sans")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            linecolor="#cbd5e1",
            tickfont=dict(color="#64748b", size=11),
            title_font=dict(size=12, color="#334155", family="Plus Jakarta Sans")
        ),
    )
