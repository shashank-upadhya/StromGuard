import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
import time
import json
from datetime import datetime, timedelta
import base64

try:
    from data.storage import UserStorage
    from data.simulator import GigWorkerSimulator
    from agents.orchestrator_agent import OrchestratorAgent
    
    # 👇 ADD THIS LINE HERE 👇
    from agents.financial_coach_agent import analyze_screenshot_tool 
    
except ModuleNotFoundError as e:
    st.error(f"System Error: {e}")
    st.stop()

# --- 1. PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# --- 2. LOCAL IMPORTS ---
try:
    from data.storage import UserStorage
    from data.simulator import GigWorkerSimulator
    from agents.orchestrator_agent import OrchestratorAgent
except ModuleNotFoundError as e:
    st.error(f"System Error: {e}")
    st.stop()

# --- 3. CONFIGURATION ---
st.set_page_config(
    page_title="StormGuard | AI Financial Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 4. INITIALIZE STORAGE ---
storage = UserStorage()

# --- 5. THEME & STYLES (From Dhruvan UI) ---
THEME = {
    "bg_dark": "#0B0E14",        # Deepest Navy
    "bg_card": "rgba(20, 25, 40, 0.75)", # Glassy Dark
    "primary": "#00F0FF",        # Neon Cyan
    "secondary": "#7000FF",      # Electric Purple
    "accent": "#00FFA3",         # Neon Green
    "text_main": "#FFFFFF",      # Pure White
    "text_sub": "#A0AEC0"        # Cool Grey
}

def inject_custom_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Outfit', sans-serif;
            color: {THEME['text_main']};
            background-color: {THEME['bg_dark']};
        }}
        
        /* SCROLLBAR */
        ::-webkit-scrollbar {{ width: 8px; background: {THEME['bg_dark']}; }}
        ::-webkit-scrollbar-thumb {{ background: {THEME['bg_card']}; border-radius: 4px; }}

        /* HEADERS */
        h1, h2, h3 {{
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            background: linear-gradient(120deg, #fff, {THEME['primary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        /* BACKGROUND */
        .stApp {{
            background-image: 
                radial-gradient(circle at 0% 0%, rgba(112, 0, 255, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 100% 100%, rgba(0, 240, 255, 0.1) 0%, transparent 40%),
                url('https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2832&auto=format&fit=crop'); 
            background-size: cover;
            background-attachment: fixed;
        }}

        /* SIDEBAR */
        section[data-testid="stSidebar"] {{
            background-color: rgba(11, 14, 20, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}

        /* SIDEBAR NAVIGATION */
        div[data-testid="stRadio"] > label {{ display: none; }}
        div[data-testid="stRadio"] label {{
            background: transparent;
            padding: 12px 20px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            cursor: pointer;
            transition: all 0.3s;
            color: {THEME['text_sub']};
            font-weight: 500;
        }}
        div[data-testid="stRadio"] label:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: white;
            border-color: {THEME['primary']};
        }}
        div[data-testid="stRadio"] label[data-baseweb="radio"] {{
            background: linear-gradient(90deg, rgba(0, 240, 255, 0.15), transparent);
            border-left: 4px solid {THEME['primary']};
            color: white;
            font-weight: 700;
        }}

        /* GLASS CARDS */
        .glass-card {{
            background: {THEME['bg_card']};
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.3);
        }}

        /* BUTTONS */
        .stButton > button {{
            background: linear-gradient(135deg, {THEME['primary']} 0%, #0099FF 100%);
            color: #0B0E14;
            border: none;
            padding: 12px 20px;
            font-weight: 700;
            border-radius: 8px;
            width: 100%;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 15px {THEME['primary']};
        }}

        /* ALERTS */
        .alert-box {{
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        /* FUNKY ANIMATION: CYBER KINETIC CORE */
        .kinetic-core {{
            position: relative;
            width: 250px;
            height: 250px;
            margin: 0 auto;
            transform-style: preserve-3d;
            animation: float-core 6s ease-in-out infinite;
        }}
        
        .k-ring {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            border: 3px solid transparent;
            border-top: 3px solid {THEME['primary']};
            border-bottom: 3px solid {THEME['secondary']};
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
        }}
        
        .k-ring:nth-child(1) {{ animation: rotate-x 3s linear infinite; }}
        .k-ring:nth-child(2) {{ 
            width: 80%; height: 80%; top: 10%; left: 10%; 
            border-color: transparent;
            border-left: 4px solid {THEME['accent']}; 
            border-right: 4px solid {THEME['accent']};
            animation: rotate-y 5s linear infinite; 
        }}
        .k-ring:nth-child(3) {{ 
            width: 60%; height: 60%; top: 20%; left: 20%; 
            border-color: transparent;
            border-top: 4px solid {THEME['primary']};
            animation: rotate-z 7s linear infinite;
        }}
        
        .k-orb {{
            position: absolute;
            top: 35%; left: 35%;
            width: 30%; height: 30%;
            background: radial-gradient(circle, {THEME['primary']}, transparent);
            border-radius: 50%;
            animation: pulse-core 2s ease-in-out infinite;
            filter: blur(5px);
        }}

        @keyframes rotate-x {{ 0% {{ transform: rotateX(0deg); }} 100% {{ transform: rotateX(360deg); }} }}
        @keyframes rotate-y {{ 0% {{ transform: rotateY(0deg); }} 100% {{ transform: rotateY(360deg); }} }}
        @keyframes rotate-z {{ 0% {{ transform: rotateZ(0deg); }} 100% {{ transform: rotateZ(360deg); }} }}
        @keyframes pulse-core {{ 0%, 100% {{ opacity: 0.5; transform: scale(0.8); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}
        @keyframes float-core {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}

        /* --- LOADING OVERLAY --- */
        .loading-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(8, 10, 16, 0.95); backdrop-filter: blur(25px);
            z-index: 999999; display: flex; flex-direction: column; align-items: center; justify-content: center;
        }}
        .shield-container {{
            position: relative; width: 180px; height: 180px; display: flex; align-items: center; justify-content: center;
        }}
        .shield-icon-main {{
            font-size: 5rem; z-index: 10; animation: shield-breath 2s infinite ease-in-out;
            filter: drop-shadow(0 0 20px {THEME['primary']});
        }}
        .shield-ring-outer {{
            position: absolute; width: 100%; height: 100%; border: 4px solid transparent;
            border-top: 4px solid {THEME['primary']}; border-bottom: 4px solid {THEME['primary']};
            border-radius: 50%; animation: spin-cw 2s linear infinite; box-shadow: 0 0 30px rgba(0, 240, 255, 0.1);
        }}
        .shield-ring-inner {{
            position: absolute; width: 70%; height: 70%; border: 4px solid transparent;
            border-left: 4px solid {THEME['secondary']}; border-right: 4px solid {THEME['secondary']};
            border-radius: 50%; animation: spin-ccw 1.5s linear infinite;
        }}
        .loading-text {{
            margin-top: 40px; font-family: 'Outfit', sans-serif; letter-spacing: 6px;
            color: {THEME['text_main']}; font-size: 1.2rem; font-weight: 600; text-transform: uppercase;
            animation: text-flicker 3s infinite;
        }}
        
        @keyframes spin-cw {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        @keyframes spin-ccw {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(-360deg); }} }}
        @keyframes shield-breath {{ 0%, 100% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.1); opacity: 1; }} }}
        @keyframes text-flicker {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
        
        .dashboard-header {{ text-align: center; margin-bottom: 40px; }}
    </style>
    """, unsafe_allow_html=True)

def apply_neon_theme(fig):
    """Apply neon theme to Plotly charts with distinct background"""
    fig.update_layout(
        font={'family': 'Outfit, sans-serif', 'color': '#A0AEC0', 'size': 12},
        paper_bgcolor='rgba(15, 20, 30, 0.8)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
        hoverlabel=dict(
            bgcolor="#0B0E14",
            bordercolor=THEME['primary'],
            font=dict(color='white')
        )
    )
    return fig

def simulate_loading(message="LOADING...", duration=0.5, auto_clear=True):
    """Renders a full-screen shield rotation animation overlay."""
    placeholder = st.empty()
    placeholder.markdown(f"""
        <div class="loading-overlay">
            <div class="shield-container">
                <div class="shield-ring-outer"></div>
                <div class="shield-ring-inner"></div>
                <div class="shield-icon-main">🛡️</div>
            </div>
            <div class="loading-text">{message}</div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(duration)
    if auto_clear:
        placeholder.empty()
    return placeholder

# --- 6. LOGIC WRAPPERS (From Dhruvan + Origin) ---

class SafeOrchestrator(OrchestratorAgent):
    """Patched run_daily_check to handle NoneType errors for stability."""
    def run_daily_check(self):
        forecast_report = self.weather_agent.generate_complete_forecast(7)
        spending_patterns = self.coach_agent.analyze_spending_patterns()
        coaching_advice = self.coach_agent.coach_on_forecast(forecast_report)
        if coaching_advice is None: 
            coaching_advice = "System update: Financial data processed. Advice currently unavailable."
        
        spending_analysis = self.coach_agent.analyze_spending_vs_income(forecast_report, spending_patterns)
        if spending_analysis is None: spending_analysis = "Analysis pending."
        
        interventions = self._check_and_prioritize_interventions(forecast_report, spending_patterns)
        
        savings_plan = self.coach_agent.generate_savings_recommendation(forecast_report, spending_patterns)
        if savings_plan is None: savings_plan = "Savings plan pending."
        
        opportunities = self.scout_agent.scan_real_time_opportunities()
        savings_summary = self.savings_agent.get_savings_summary(30)
        savings_recommendation = self.savings_agent.smart_savings_recommendation(forecast_report, spending_patterns)
        
        dashboard = self._create_dashboard_summary(forecast_report, spending_patterns, interventions)
        
        return {
            'forecast': forecast_report,
            'spending': spending_patterns,
            'coaching': coaching_advice,
            'spending_analysis': spending_analysis,
            'interventions': interventions,
            'savings_plan': savings_plan,
            'dashboard': dashboard,
            'opportunities': opportunities,
            'savings_summary': savings_summary,
            'savings_recommendation': savings_recommendation,
            'opportunity_plan': self.scout_agent.generate_daily_opportunity_plan(),
            'metadata': {'user_id': self.user_id, 'patched': True}
        }

@st.cache_resource
def get_orchestrator(_profile, _income_df, _spending_df):
    """Return the SafeOrchestrator instance to prevent crashes"""
    return SafeOrchestrator(_profile, _income_df, _spending_df)

def load_user_session(user_id):
    """Loads user data and initializes the Orchestrator (Logic from Origin)"""
    profile, income_df, spending_df = storage.get_data_for_agents(user_id)
    
    # Generate data if missing (Simulator logic from Origin)
    if income_df.empty:
        simulator = GigWorkerSimulator(profile['name'], profile['city'])
        income_df = simulator.generate_income_history(90)
        spending_df = simulator.generate_spending_data(30)
        for _, row in income_df.iterrows():
            storage.add_income(user_id, row.to_dict())
        for _, row in spending_df.iterrows():
            storage.add_expense(user_id, row.to_dict())
            
    st.session_state.profile = profile
    st.session_state.income_data = income_df
    st.session_state.spending_data = spending_df
    st.session_state.orchestrator = get_orchestrator(profile, income_df, spending_df)
    st.session_state.user_id = user_id
    
    # Load goals
    st.session_state.goals = storage.get_goals(user_id)

# --- 7. UI COMPONENTS WITH LOGIC INJECTION ---

def render_dashboard_landing():
    """Displayed immediately after login, before syncing"""
    st.markdown(f"""
        <div class="dashboard-header">
            <div style="font-size: 5rem; margin-bottom: 10px;">🛡️</div>
            <h1 style="font-size: 4rem !important; margin: 0; text-shadow: 0 0 40px {THEME['primary']};">STORMGUARD</h1>
            <p style="color: {THEME['text_sub']}; letter-spacing: 5px; font-weight:300;">FINANCIAL PROTECTION SYSTEM</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="kinetic-core">
            <div class="k-ring"></div>
            <div class="k-ring"></div>
            <div class="k-ring"></div>
            <div class="k-orb"></div>
        </div>
        <div style="height: 60px;"></div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INITIALIZE SYNC ⚡", use_container_width=True):
            simulate_loading(message="ANALYSING...", duration=1.0, auto_clear=False)
            try:
                st.session_state.daily_report = st.session_state.orchestrator.run_daily_check()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
            st.rerun()

def render_forecast_page(report):
    st.markdown("<h2>🔮 FINANCIAL FORECAST</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.8, 1])
    
    with col1:
        if report:
            # FIX: Access correct path from Origin's data structure
            df_forecast = pd.DataFrame(report['forecast']['predictions']['predictions'])
            
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 7-Day Income Projection")
            
            fig = px.bar(
                df_forecast, 
                x='day_name', 
                y='predicted_income',
                text='predicted_income',
                color='predicted_income',
                color_continuous_scale=[THEME['bg_dark'], THEME['primary']]
            )
            fig.update_traces(texttemplate='₹%{text:.0s}', textposition='outside', marker_line_width=0, opacity=0.9)
            fig.update_layout(height=350, coloraxis_showscale=False, yaxis_title=None, xaxis_title=None)
            st.plotly_chart(apply_neon_theme(fig), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='glass-card' style='display:flex; align-items:center; justify-content:space-between; background: linear-gradient(90deg, rgba(0,240,255,0.1), transparent);'>
                    <div>
                        <div class='metric-label' style='font-size: 0.9rem; color: #A0AEC0;'>7-Day Prediction</div>
                        <div class='metric-value' style='font-size: 1.8rem; font-weight: 700;'>₹{report['dashboard']['summary']['weekly_income_forecast']:,}</div>
                    </div>
                    <div style='text-align:right'>
                        <div class='metric-label' style='font-size: 0.9rem; color: #A0AEC0;'>Confidence</div>
                        <div style='font-size:2rem; font-weight:800; color:{THEME['accent']}'>94%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ⚠️ THREAT DETECTION")
        if report:
            alerts = report.get('interventions', [])
            if not alerts:
                 st.markdown(f"""
                    <div class='glass-card' style='text-align:center; padding:40px;'>
                        <div style='font-size:3rem;'>🛡️</div>
                        <h3 style='color:{THEME['accent']}'>SYSTEM SECURE</h3>
                        <p style='color:{THEME['text_sub']}'>No active financial threats.</p>
                    </div>
                 """, unsafe_allow_html=True)
            
            for alert in alerts:
                sev = alert['severity']
                color = "#FF003C" if sev == 'HIGH' else "#FFB800" if sev == 'MEDIUM' else "#00F0FF"
                
                st.markdown(f"""
                <div class='glass-card' style='border-left: 4px solid {color}; padding: 20px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:5px;'>
                        <strong style='color:{color}; letter-spacing:1px; font-size:0.9rem;'>{alert['category']}</strong>
                        <span style='background:{color}; color:black; font-weight:bold; font-size:0.7rem; padding:2px 8px; border-radius:4px;'>{sev}</span>
                    </div>
                    <p style='color:white; font-size:1.1rem; line-height:1.4;'>{alert['message']}</p>
                </div>
                """, unsafe_allow_html=True)

def process_uploaded_image(uploaded_file, user_id):
    """
    Convert uploaded file to base64 and call the analysis tool.
    Returns the analysis result dictionary.
    """
    try:
        # 1. Convert to bytes
        bytes_data = uploaded_file.getvalue()
        
        # 2. Encode to base64
        b64_string = base64.b64encode(bytes_data).decode('utf-8')
        full_b64 = f"data:{uploaded_file.type};base64,{b64_string}"
        
        # 3. Call the tool directly using .entrypoint logic
        # We use .entrypoint because we are calling the tool function from Python, not via LLM
        result_json = analyze_screenshot_tool.entrypoint(
            user_id=user_id,
            image_b64=full_b64,
            filename=uploaded_file.name
        )
        
        return json.loads(result_json)
    except Exception as e:
        return {"error": str(e)}

def render_ai_coach_page():
    st.markdown("<h2>🧠 AI COACH</h2>", unsafe_allow_html=True)
    
    # 1. Chat History Container
    chat_container = st.container()
    
    # 2. File Uploader Section (Expandable)
    with st.expander("📎 Upload Dashboard Screenshot / Statement", expanded=False):
        uploaded_file = st.file_uploader("Upload Image (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            col_p, col_btn = st.columns([1, 2])
            with col_p:
                st.image(uploaded_file, caption="Preview", width=150)
            with col_btn:
                if st.button("🔍 ANALYZE IMAGE", use_container_width=True):
                    with st.spinner(" extracting data..."):
                        result = process_uploaded_image(uploaded_file, st.session_state.user_id)
                    
                    if "error" in result:
                        st.error(f"Analysis Failed: {result['error']}")
                    else:
                        # Success! Format result for chat
                        features = result.get('features', {})
                        earnings = features.get('today_earnings', 0)
                        orders = features.get('orders_today', 0)
                        
                        success_msg = f"""
                        **✅ Screenshot Analyzed!**
                        - Earnings Detected: ₹{earnings}
                        - Orders: {orders}
                        - Data saved to records.
                        """
                        
                        # Add interaction to chat history
                        st.session_state.chat_history.append({
                            "question": f"📷 [Uploaded Screenshot]: {uploaded_file.name}", 
                            "answer": success_msg
                        })
                        st.success("Data extracted and saved!")
                        time.sleep(1)
                        st.rerun()

    # 3. Render Chat History
    with chat_container:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [{"question": None, "answer": f"Identity Verified: {st.session_state.profile['name']}. Clarify your doubts with me."}]
        
        for chat in st.session_state.chat_history:
            if chat['question']:
                st.markdown(f"""
                    <div style='display:flex; justify-content:flex-end; margin-bottom:15px;'>
                        <div style='background:rgba(255,255,255,0.05); padding:15px 25px; border-radius:20px 20px 0 20px; font-size:1.1rem; border:1px solid rgba(255,255,255,0.1);'>
                            {chat['question']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style='display:flex; justify-content:flex-start; margin-bottom:25px;'>
                    <div style='background:linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(11, 14, 20, 0.8)); padding:20px; border-radius:20px 20px 20px 0; border:1px solid {THEME['primary']}; max-width:85%;'>
                        <div style='color:{THEME['primary']}; font-size:0.8rem; font-weight:700; margin-bottom:8px;'>STORMGUARD AI</div>
                        <div style='font-size:1.1rem; line-height:1.5;'>{chat['answer']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # 4. Text Input Area
    with st.form("ai_chat", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input("Input", placeholder="Ask about savings, or upload a screenshot above...", label_visibility="collapsed")
        with col2:
            submit = st.form_submit_button("SEND")
        
        if submit and user_input:
            orchestrator = st.session_state.orchestrator
            # Add user message immediately
            st.session_state.chat_history.append({"question": user_input, "answer": "..."})
            st.rerun() # Quick rerun to show user message
    
    # 5. Process last message if it's waiting
    if st.session_state.chat_history and st.session_state.chat_history[-1]['answer'] == "...":
        user_last_q = st.session_state.chat_history[-1]['question']
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.orchestrator.chat(user_last_q)
        except Exception as e:
            response = f"Communication Error: {e}"
        
        # Update answer
        st.session_state.chat_history[-1]['answer'] = response
        st.rerun()
def render_trends_page():
    st.markdown("<h2>📈 FINANCIAL STATS</h2>", unsafe_allow_html=True)
    
    # Logic from Origin to get data
    income_df = storage.get_income_history(st.session_state.user_id, 90)
    spending_summary = storage.get_spending_summary(st.session_state.user_id, 30)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""<div class='glass-card'><h3 style='margin-top:0'>Income Velocity</h3>""", unsafe_allow_html=True)
        if not income_df.empty:
            fig = px.area(income_df.sort_values('date'), x='date', y='income', color_discrete_sequence=[THEME['accent']])
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(apply_neon_theme(fig), use_container_width=True)
        else:
            st.info("Insufficient data.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div class='glass-card'><h3 style='margin-top:0'>Expense Distribution</h3>""", unsafe_allow_html=True)
        if spending_summary['total_spent'] > 0:
            labels = list(spending_summary['by_category'].keys())
            values = list(spending_summary['by_category'].values())
            fig = px.pie(values=values, names=labels, hole=0.6, color_discrete_sequence=px.colors.sequential.Bluyl)
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(apply_neon_theme(fig), use_container_width=True)
        else:
            st.info("No spending recorded.")
        st.markdown("</div>", unsafe_allow_html=True)

def render_goals_page():
    st.markdown("<h2>🎯 GOALS</h2>", unsafe_allow_html=True)
    # Logic from Origin to get goals
    goals = storage.get_goals(st.session_state.user_id)
    total_savings = storage.get_total_savings(st.session_state.user_id)
    
    with st.expander("➕ INITIATE NEW TARGET"):
        with st.form("new_goal_form"):
            g_name = st.text_input("Target Name")
            g_amount = st.number_input("Target Amount (₹)", 1000)
            if st.form_submit_button("LOCK TARGET"):
                goals_text = [g['description'] if isinstance(g, dict) else g for g in goals]
                goals_text.append(g_name) # Simple string storage logic from origin
                storage.set_goals(st.session_state.user_id, goals_text)
                st.success("Target Locked")
                st.rerun()
                
    if not goals:
        st.info("No active targets.")
        
    for goal in goals:
        # Origin data parsing logic
        desc = goal['description'] if isinstance(goal, dict) else goal
        target = goal.get('target_amount', 1000) if isinstance(goal, dict) else 50000 # Default if simple string
        
        # Calculate progress using Total Savings vs Target
        current = total_savings
        progress = min(current / target, 1.0) if target > 0 else 0
        
        st.markdown(f"""
        <div class='glass-card'>
            <div style='display:flex; justify-content:space-between; margin-bottom:15px;'>
                <span style='font-size:1.5rem; font-weight:700;'>{desc}</span>
                <span style='color:{THEME['primary']}; font-size:1.2rem; font-weight:600;'>₹{current:,.0f} / ₹{target:,}</span>
            </div>
            <div style='background:rgba(255,255,255,0.1); height:12px; border-radius:6px; overflow:hidden;'>
                <div style='background:linear-gradient(90deg, {THEME['primary']}, {THEME['secondary']}); width:{progress*100}%; height:100%;'></div>
            </div>
            <div style='text-align:right; font-size:0.9rem; color:{THEME['text_sub']}; margin-top:8px;'>
                {int(progress*100)}% FUNDED
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_settings_page():
    st.markdown("<h2>⚙️ SAVINGS</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Logic from Origin for Savings Rate
    with col1:
        st.markdown("<h4 style='color: #6c5ce7;'>💰 Auto-Save Protocol</h4>", unsafe_allow_html=True)
        current_rate = int(st.session_state.profile.get('savings_rate', 0.05) * 100)
        new_rate = st.slider("Daily Deduction (%)", 1, 20, value=current_rate)
        
        if st.button("UPDATE PROTOCOL"):
            user_id = st.session_state.user_id
            storage.update_user(user_id, {'savings_rate': new_rate / 100})
            st.session_state.profile['savings_rate'] = new_rate / 100
            
            # Update live agent if exists
            if hasattr(st.session_state.orchestrator, 'savings_agent'):
                st.session_state.orchestrator.savings_agent.savings_rate = new_rate / 100
            
            st.success(f"Protocol Updated: {new_rate}%")
            time.sleep(1)
            st.rerun()

    with col2:
        st.markdown("<h4 style='color: #6c5ce7;'>👤 Operator Details</h4>", unsafe_allow_html=True)
        st.text_input("Operator Name", value=st.session_state.profile.get('name', ''), disabled=True)
        st.text_input("Region", value=st.session_state.profile.get('city', ''), disabled=True)
    
    st.markdown("---")
    if st.button("TERMINATE SESSION (LOGOUT)"):
        st.session_state.clear()
        st.session_state.page = "landing"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_onboarding_form():
    """Detailed onboarding form from Origin, styled with Dhruvan's CSS"""
    st.markdown("<h2 style='text-align:center;'>INITIALIZE NEW PROFILE</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
         st.markdown(f"""
        <div class="glass-card">
            <h3>🚀 Identity Setup</h3>
            <p style="color: {THEME['text_sub']};">Configure your digital twin for financial monitoring.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True):
            with st.form("onboarding_form"):
                name = st.text_input("👤 Your Name *", placeholder="e.g., Rajesh Kumar")
                c1, c2 = st.columns(2)
                with c1:
                    age = st.number_input("🎂 Age", min_value=18, max_value=65, value=25)
                with c2:
                    city = st.selectbox("📍 City *", [
                        "Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", 
                        "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Other"
                    ])
                
                platform = st.multiselect("🚚 Platforms *", [
                    "Swiggy", "Zomato", "Dunzo", "Amazon Flex", 
                    "Uber Eats", "Ola", "Uber", "Rapido", "Other"
                ], default=["Swiggy"])
                
                phone = st.text_input("📱 Phone (Optional)", placeholder="9876543210")
                
                st.markdown("#### 🎯 Primary Objective")
                goal1 = st.text_input("Goal", placeholder="e.g., Emergency Fund")
                
                st.markdown("#### 💰 Auto-Save Rate")
                savings_rate = st.slider("Percentage (%)", min_value=2, max_value=10, value=5)
                
                generate_demo = st.checkbox("Generate Simulation Data", value=True)
                
                submitted = st.form_submit_button("ACTIVATE PROFILE 🚀")
                
                if submitted:
                    if not name or not city or not platform:
                        st.error("Missing mandatory fields.")
                    else:
                        goals = [goal1] if goal1 else ["Build emergency fund"]
                        user_data = {
                            'name': name, 'age': age, 'city': city,
                            'platform': " + ".join(platform), 'platforms': platform,
                            'phone': phone, 'goals': goals,
                            'savings_rate': savings_rate / 100, 'language': 'hinglish'
                        }
                        
                        # Logic from Origin
                        user_id = storage.create_user(user_data)
                        
                        if generate_demo:
                            simulator = GigWorkerSimulator(name, city)
                            demo_income = simulator.generate_income_history(90)
                            demo_spending = simulator.generate_spending_data(30)
                            for _, row in demo_income.iterrows():
                                storage.add_income(user_id, row.to_dict())
                            for _, row in demo_spending.iterrows():
                                storage.add_expense(user_id, row.to_dict())
                        
                        load_user_session(user_id)
                        st.session_state.page = "dashboard"
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# --- 8. SIDEBAR & NAVIGATION ---

def show_sidebar_logic(user_id, profile):
    """Sidebar with Functional Data Entry Forms (Logic from Origin)"""
    st.sidebar.markdown("### ⚡ Quick Fixes")
    
    with st.sidebar.expander("💰 Add Income", expanded=False):
        with st.form("income_form"):
            income_date = st.date_input("Date", datetime.now())
            income_amount = st.number_input("Income (₹)", min_value=0, value=500, step=50)
            hours_worked = st.number_input("Hours", min_value=1, max_value=16, value=8)
            platform = st.selectbox("Platform", profile.get('platforms', ['Swiggy', 'Zomato']))
            
            if st.form_submit_button("Save Income"):
                # Logic from Origin
                storage.add_income(user_id, {
                    'date': income_date.strftime('%Y-%m-%d'),
                    'income': income_amount,
                    'hours_worked': hours_worked,
                    'platform': platform,
                    'is_weekend': income_date.weekday() >= 5
                })
                
                # Auto-save logic from Origin
                savings_rate = profile.get('savings_rate', 0.05)
                savings_amount = income_amount * savings_rate
                if hasattr(storage, 'add_savings'):
                     storage.add_savings(user_id, {
                        'date': income_date.strftime('%Y-%m-%d'),
                        'amount': savings_amount,
                        'source': 'auto_save'
                    })
                st.success(f"Saved! +₹{savings_amount:.0f} to savings")
                st.rerun()

    with st.sidebar.expander("💸 Add Expense", expanded=False):
        with st.form("expense_form"):
            exp_date = st.date_input("Date", datetime.now())
            exp_amount = st.number_input("Amount (₹)", min_value=0, value=100)
            exp_category = st.selectbox("Category", ["food", "fuel", "rent", "entertainment", "other"])
            
            if st.form_submit_button("Save Expense"):
                # Logic from Origin
                storage.add_expense(user_id, {
                    'date': exp_date.strftime('%Y-%m-%d'),
                    'amount': exp_amount,
                    'category': exp_category
                })
                st.success("Expense saved!")
                st.rerun()

def render_dashboard_shell():
    """Main Dashboard Container with Sidebar"""
    with st.sidebar:
        st.markdown("""
            <div style='text-align:center; padding:10px 0;'>
                <h1 style='font-size:2rem; margin:0; color:#00F0FF; text-shadow:0 0 10px rgba(0,240,255,0.5);'> 🛡️ StormGuard  </h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='text-align:center; margin-bottom:20px;'>
                <div style='width:80px; height:80px; background:linear-gradient(135deg, {THEME['primary']}, {THEME['secondary']}); border-radius:50%; margin:0 auto 10px auto; display:flex; align-items:center; justify-content:center; font-size:2rem; font-weight:bold; color:black;'>{st.session_state.profile['name'][0]}</div>
                <h3 style='margin:5px 0 0 0; font-size:1.2rem;'>{st.session_state.profile['name']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🧭 Navigation")
        # Custom Radio acts as Tab Controller
        nav = st.radio("NAV", ["Forecast", "AI Coach", "Financial Stats", "Goals", "Settings"], label_visibility="collapsed")
        
        st.markdown("---")
        show_sidebar_logic(st.session_state.user_id, st.session_state.profile)

    # Main Content Router
    if nav == "Forecast":
        if 'daily_report' not in st.session_state or st.session_state.daily_report is None:
            render_dashboard_landing()
        else:
            render_forecast_page(st.session_state.daily_report)
            
    elif nav == "AI Coach":
        if st.session_state.get('last_page') != 'AI Coach': simulate_loading(auto_clear=True)
        render_ai_coach_page()
    elif nav == "Financial Stats":
        if st.session_state.get('last_page') != 'Financial Stats': simulate_loading(auto_clear=True)
        render_trends_page()
    elif nav == "Goals":
        if st.session_state.get('last_page') != 'Goals': simulate_loading(auto_clear=True)
        render_goals_page()
    elif nav == "Settings":
        if st.session_state.get('last_page') != 'Settings': simulate_loading(auto_clear=True)
        render_settings_page()
        
    st.session_state.last_page = nav


# --- 9. APP ENTRY POINT ---

def main():
    inject_custom_css()
    if 'page' not in st.session_state: st.session_state.page = "landing"
    
    if st.session_state.page == "landing":
        st.markdown("<div style='height:25vh'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='text-align:center;'>
                <h1 style='font-size:5rem !important; margin-bottom:10px; display:inline-block; text-shadow: 0 0 30px {THEME["primary"]};'>STORMGUARD</h1>
                <p style='color:{THEME['text_sub']}; font-size:1.5rem; letter-spacing:4px;'>FINANCIAL SHIELD ACTIVE</p>
            </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            if st.button("INITIALIZE SYSTEM", use_container_width=True):
                st.session_state.page = "user_selection"
                st.rerun()
                
    elif st.session_state.page == "user_selection":
        st.markdown("<h2 style='text-align:center; margin-top:50px;'>SELECT OPERATOR</h2>", unsafe_allow_html=True)
        users = storage.list_users()
        cols = st.columns(3)
        for i, user in enumerate(users):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='glass-card' style='text-align:center;'>
                    <h3>{user['name']}</h3>
                    <p style='color:{THEME['text_sub']}'>{user.get('city', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACCESS: {user['name']}", key=user['user_id']):
                    load_user_session(user['user_id'])
                    st.session_state.page = "dashboard"
                    st.rerun()
        
        # New User Card
        with cols[len(users)%3]:
            st.markdown(f"<div class='glass-card' style='text-align:center; border:2px dashed {THEME['text_sub']}'><h3>+ NEW</h3></div>", unsafe_allow_html=True)
            if st.button("CREATE PROFILE"):
                st.session_state.page = "onboarding"
                st.rerun()

    elif st.session_state.page == "onboarding":
        render_onboarding_form()

    elif st.session_state.page == "dashboard":
        if 'user_id' not in st.session_state:
            st.session_state.page = "landing"
            st.rerun()
        render_dashboard_shell()

if __name__ == "__main__":
    main()




# import streamlit as st
# import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
# import sys
# import os
# from datetime import datetime, timedelta

# # Add parent directory to path FIRST
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# from data.storage import UserStorage
# from data.simulator import GigWorkerSimulator
# from agents.orchestrator_agent import OrchestratorAgent


# # Add near other imports at top of file
# import base64
# from io import BytesIO
# from PIL import Image
# from pdf2image import convert_from_bytes

# # Import your screenshot analyzer tool (adjust path if needed)
# # from .agents/financial_coach_agent import analyze_screenshot_tool
# from agents.financial_coach_agent import analyze_screenshot_tool

# # Page configuration
# st.set_page_config(
#     page_title="StormGuard India",
#     page_icon="🌦️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize storage
# storage = UserStorage()

# # ==================== UI STYLING & THEME ====================

# def _file_to_b64(file_bytes: bytes, mime: str) -> str:
#     b64 = base64.b64encode(file_bytes).decode("utf-8")
#     return f"data:{mime};base64,{b64}"

# def analyze_image_bytes(user_id: str, img_bytes: bytes, filename: str = None):
#     """Send a single image (bytes) to analyze_screenshot_tool via base64 string."""
#     mime = "image/png"
#     b64 = _file_to_b64(img_bytes, mime)
#     # Call the tool entrypoint (this will attempt to save to storage inside the tool)
#     resp_json = analyze_screenshot_tool.entrypoint(user_id, image_b64=b64, filename=filename)
#     try:
#         return json.loads(resp_json)
#     except Exception:
#         return {"raw": resp_json}

# def analyze_pdf_bytes(user_id: str, pdf_bytes: bytes, filename_prefix: str = None):
#     """Convert PDF to images and analyze each page. Returns list of page-results."""
#     pages = convert_from_bytes(pdf_bytes, dpi=200)  # adjust dpi if needed
#     results = []
#     for i, page in enumerate(pages, start=1):
#         buff = BytesIO()
#         page.save(buff, format="PNG")
#         img_bytes = buff.getvalue()
#         fname = f"{(filename_prefix or 'upload')}_page_{i}.png"
#         r = analyze_image_bytes(user_id, img_bytes, filename=fname)
#         results.append({"page": i, "filename": fname, "result": r})
#     return results


# def apply_custom_styles():
#     st.markdown("""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

#         :root {
#             --primary: #A8D8EA;
#             --text-dark: #2D3436;
#             --text-light: #636E72;
#         }

#         .stApp {
#             background: linear-gradient(135deg, #F7F9FC 0%, #E8F0F5 100%);
#             font-family: 'Outfit', sans-serif;
#             color: var(--text-dark);
#         }
        
#         /* HEADERS */
#         .main-header {
#             background: linear-gradient(120deg, #6C5CE7, #00B894);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             font-size: 3rem;
#             font-weight: 800;
#             text-align: center;
#             margin-bottom: 0.5rem;
#         }

#         /* GLASS CARDS */
#         .glass-card {
#             background: rgba(255, 255, 255, 0.95);
#             border-radius: 20px;
#             padding: 24px;
#             box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
#             border: 1px solid rgba(255, 255, 255, 0.8);
#             margin-bottom: 20px;
#             transition: transform 0.2s ease;
#         }
#         .glass-card:hover {
#             transform: translateY(-3px);
#             box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
#         }

#         /* METRICS */
#         .metric-container {
#             text-align: center;
#             padding: 10px;
#         }
#         .metric-label {
#             font-size: 0.85rem;
#             color: var(--text-light);
#             text-transform: uppercase;
#             letter-spacing: 1px;
#             margin-bottom: 5px;
#         }
#         .metric-value {
#             font-size: 1.8rem;
#             font-weight: 700;
#             color: var(--text-dark);
#         }

#         /* TABS */
#         .stTabs [data-baseweb="tab-list"] { gap: 8px; }
#         .stTabs [data-baseweb="tab"] {
#             background-color: white;
#             border-radius: 10px;
#             padding: 10px 20px;
#             border: 1px solid #eee;
#         }
#         .stTabs [aria-selected="true"] {
#             background-color: #e3f2fd;
#             border-color: #90caf9;
#             color: #1565c0;
#         }

#         /* ALERTS */
#         .alert-box {
#             padding: 16px;
#             border-radius: 12px;
#             margin-bottom: 10px;
#             display: flex;
#             align-items: center;
#             gap: 12px;
#         }
#         .alert-high { background: #ffebee; border-left: 4px solid #ef5350; color: #c62828; }
#         .alert-medium { background: #fff3e0; border-left: 4px solid #ff9800; color: #ef6c00; }
#         .alert-low { background: #e8f5e9; border-left: 4px solid #66bb6a; color: #2e7d32; }

#         /* GOAL RINGS ANIMATION */
#         @keyframes fillCircle {
#             from { stroke-dashoffset: 314; }
#             to { stroke-dashoffset: var(--target-offset); }
#         }
#         svg circle { transition: stroke-dashoffset 1s ease-out; }
#     </style>
#     """, unsafe_allow_html=True)

# def apply_pastel_theme(fig):
#     pastel_colors = ['#6C5CE7', '#00B894', '#FF7675', '#74B9FF', '#FAB1A0']
#     fig.update_layout(
#         font={'family': 'Outfit, sans-serif', 'color': '#2d3436'},
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(l=10, r=10, t=30, b=10),
#         colorway=pastel_colors
#     )
#     fig.update_xaxes(showgrid=False)
#     fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
#     return fig

# # ==================== APP LOGIC ====================

# @st.cache_resource
# def get_orchestrator(profile, _income_df, _spending_df):
#     return OrchestratorAgent(profile, _income_df, _spending_df)

# def show_onboarding():
#     apply_custom_styles()
#     st.markdown('<div class="main-header">🌦️ StormGuard India</div>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns([1.2, 0.8], gap="large")
    
#     with col1:
#         st.markdown("""<div class="glass-card"><h3>🚀 Create Your Profile</h3></div>""", unsafe_allow_html=True)
#         with st.form("onboarding_form"):
#             name = st.text_input("Name", placeholder="Rajesh Kumar")
#             c1, c2 = st.columns(2)
#             with c1: age = st.number_input("Age", 18, 65, 25)
#             with c2: city = st.selectbox("City", ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kolkata"])
            
#             platform = st.multiselect("Platforms", ["Swiggy", "Zomato", "Uber", "Ola", "Dunzo"], default=["Swiggy"])
#             savings_rate = st.slider("Auto-Save %", 2, 10, 5)
#             generate_demo = st.checkbox("Generate demo data", value=True)
            
#             if st.form_submit_button("Start Journey 🚀", use_container_width=True):
#                 if name:
#                     user_data = {
#                         'name': name, 'age': age, 'city': city,
#                         'platform': " + ".join(platform), 'platforms': platform,
#                         'savings_rate': savings_rate / 100, 'goals': ["Emergency Fund"], 'language': 'hinglish'
#                     }
#                     user_id = storage.create_user(user_data)
                    
#                     if generate_demo:
#                         sim = GigWorkerSimulator(name, city)
#                         inc = sim.generate_income_history(90)
#                         spd = sim.generate_spending_data(30)
#                         for _, r in inc.iterrows(): storage.add_income(user_id, r.to_dict())
#                         for _, r in spd.iterrows(): storage.add_expense(user_id, r.to_dict())
                    
#                     st.session_state.user_id = user_id
#                     st.session_state.onboarding_complete = True
#                     st.rerun()

#     with col2:
#         st.markdown("""<div class="glass-card"><h3>👋 Returning User?</h3></div>""", unsafe_allow_html=True)
#         users = storage.list_users()
#         if users:
#             for u in users:
#                 if st.button(f"👤 {u['name']}", key=u['user_id'], use_container_width=True):
#                     st.session_state.user_id = u['user_id']
#                     st.session_state.onboarding_complete = True
#                     st.rerun()

# def initialize_app():
#     user_id = st.session_state.user_id
#     profile, income_df, spending_df = storage.get_data_for_agents(user_id)
#     orchestrator = get_orchestrator(profile, income_df, spending_df)
#     return profile, income_df, spending_df, orchestrator

# def show_main_app():
#     apply_custom_styles()
#     user_id = st.session_state.user_id
    
#     if 'orchestrator' not in st.session_state:
#         with st.spinner("Initializing..."):
#             p, i, s, o = initialize_app()
#             st.session_state.profile = p
#             st.session_state.income_data = i
#             st.session_state.spending_data = s
#             st.session_state.orchestrator = o
#             st.session_state.daily_report = None
#             st.session_state.chat_history = []
#             st.rerun()

#     profile = st.session_state.profile
#     orchestrator = st.session_state.orchestrator
    
#     # Sidebar
#     with st.sidebar:
#         st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={profile['name']}", width=80)
#         st.write(f"**{profile['name']}**")
#         st.caption(profile.get('city', 'India'))
        
#         st.markdown("---")
        
#         # --- 1. ADD INCOME ---
#         with st.expander("💰 Add Income"):
#             with st.form("inc"):
#                 amt = st.number_input("Amount", 0, 5000, 500)
#                 if st.form_submit_button("Save"):
#                     storage.add_income(user_id, {'date': datetime.now().strftime('%Y-%m-%d'), 'income': amt})
#                     s_amt = amt * profile.get('savings_rate', 0.05)
#                     if hasattr(storage, 'add_savings'):
#                         storage.add_savings(user_id, {'date': datetime.now().strftime('%Y-%m-%d'), 'amount': s_amt, 'source': 'auto'})
#                     st.success(f"Saved + ₹{s_amt:.0f}")
#                     st.rerun()

#         # --- 2. ADD EXPENSE (Restored!) ---
#         with st.expander("💸 Add Expense"):
#             with st.form("expense_form"):
#                 exp_date = st.date_input("Date", datetime.now())
#                 exp_amount = st.number_input("Amount (₹)", min_value=0, value=100)
#                 exp_category = st.selectbox("Category", ["food", "fuel", "rent", "entertainment", "other"])
                
#                 if st.form_submit_button("Save Expense"):
#                     storage.add_expense(user_id, {
#                         'date': exp_date.strftime('%Y-%m-%d'),
#                         'amount': exp_amount,
#                         'category': exp_category
#                     })
#                     st.success("Expense saved!")
#                     st.rerun()
        
#         st.markdown("---")
#         if st.button("🔄 Daily Check", type="primary"):
#             st.session_state.daily_report = orchestrator.run_daily_check()
#             st.rerun()
            
#         if st.button("🚪 Logout"):
#             st.session_state.clear()
#             st.rerun()

#     # Main Content
#     st.markdown(f"### 🌦️ Dashboard: {profile['name']}")
    
#     tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Forecast", "💬 Coach", "📈 Trends", "🎯 Goals", "⚙️ Settings"])
    
#     # --- TAB 1: FORECAST ---
#     with tab1:
#         if st.session_state.daily_report:
#             report = st.session_state.daily_report
#             dash = report['dashboard']
            
#             c1, c2, c3 = st.columns(3)
#             with c1: 
#                 st.markdown(f"""<div class="glass-card metric-container">
#                     <div class="metric-label">Health Score</div>
#                     <div class="metric-value" style="color: #00B894">{dash['summary']['financial_health_score']}</div>
#                 </div>""", unsafe_allow_html=True)
#             with c2:
#                 st.markdown(f"""<div class="glass-card metric-container">
#                     <div class="metric-label">Weekly Forecast</div>
#                     <div class="metric-value">₹{dash['summary']['weekly_income_forecast']:,.0f}</div>
#                 </div>""", unsafe_allow_html=True)
#             with c3:
#                 st.markdown(f"""<div class="glass-card metric-container">
#                     <div class="metric-label">Savings Rate</div>
#                     <div class="metric-value">{dash['summary']['savings_rate']:.1f}%</div>
#                 </div>""", unsafe_allow_html=True)
            
#             col_m, col_s = st.columns([2, 1])
#             with col_m:
#                 st.subheader("Income Weather")
#                 preds = report['forecast']['predictions']['predictions']
#                 df_p = pd.DataFrame(preds)
#                 fig = px.bar(df_p, x='day_name', y='predicted_income', title="7-Day Forecast")
#                 st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
#                 st.info(f"💡 **Coach says:** {report['coaching']}")
            
#             with col_s:
#                 st.subheader("Alerts")
#                 if report['interventions']:
#                     for alert in report['interventions']:
#                         color = "alert-high" if alert['severity'] == "HIGH" else "alert-low"
#                         st.markdown(f"""<div class="alert-box {color}">
#                             <div><b>{alert['category']}</b><br>{alert['message']}</div>
#                         </div>""", unsafe_allow_html=True)
#                 else:
#                     st.success("✅ No urgent risks detected!")
#     # TAB 2: AI COACH
#     with tab2:
#         st.markdown("### 💬 Chat with StormGuard — Upload or Ask in the same place")

#         # Render existing chat history (if any)
#         for chat in st.session_state.get('chat_history', []):
#             with st.chat_message("user", avatar="👤"):
#                 st.markdown(chat['question'])
#             with st.chat_message("assistant", avatar="🌦️"):
#                 st.markdown(chat['answer'])

#         # Two-column input area: left = text chat input, right = compact uploader
#         col_text, col_upload = st.columns([3, 1])

#         # ---------- Text input (left) ----------
#         with col_text:
#             user_q = st.chat_input("Ask about savings, shifts, or spending... (or attach a file on the right)")
#             if user_q:
#                 # append user message placeholder to history and call orchestrator
#                 st.session_state.chat_history.append({'question': user_q, 'answer': None})
#                 with st.chat_message("user", avatar="👤"):
#                     st.markdown(user_q)
#                 with st.chat_message("assistant", avatar="🌦️"):
#                     with st.spinner("Thinking..."):
#                         try:
#                             response = orchestrator.chat(user_q)
#                         except Exception as e:
#                             response = f"Agent error: {e}"
#                         st.markdown(response)
#                         # update last placeholder entry
#                         for h in reversed(st.session_state.chat_history):
#                             if h['answer'] is None and h['question'] == user_q:
#                                 h['answer'] = response
#                                 break

#         # ---------- File uploader (right) ----------
#         with col_upload:
#             st.markdown("**📎 Upload**")
#             uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"],
#                                              accept_multiple_files=False, key="coach_uploader")
#             if uploaded_file is not None:
#                 filename = uploaded_file.name
#                 file_bytes = uploaded_file.read()
#                 file_type = uploaded_file.type

#                 # preview (images only)
#                 if file_type.startswith('image'):
#                     try:
#                         img = Image.open(BytesIO(file_bytes)).convert("RGB")
#                         st.image(img, caption=filename, use_column_width=True)
#                     except Exception:
#                         st.write("(Preview unavailable)")
#                 else:
#                     st.write(f"Uploaded: {filename} (PDF)")

#                 # Analyze & attach the analysis as an assistant message
#                 if st.button("Analyze & Attach", key=f"analyze_{filename}"):
#                     with st.spinner("Analyzing upload..."):
#                         try:
#                             if file_type == "application/pdf":
#                                 page_results = analyze_pdf_bytes(
#                                     st.session_state.user_id,
#                                     file_bytes,
#                                     filename_prefix=os.path.splitext(filename)[0]
#                                 )
#                                 # Build a short multi-page summary
#                                 summary_lines = [f'PDF "{filename}" — {len(page_results)} page(s) analyzed.']
#                                 for p in page_results:
#                                     features = p.get('result', {}) if isinstance(p, dict) else {}
#                                     summary_lines.append(
#                                         f"Page {p['page']}: OCR blocks={features.get('ocr_blocks_count','N/A')} | saved={features.get('save_message','No')}"
#                                     )
#                                 assistant_msg = "\n".join(summary_lines)
#                             else:
#                                 # image
#                                 resp = analyze_image_bytes(st.session_state.user_id, file_bytes, filename=filename)
#                                 assistant_msg = (
#                                     f'Image "{filename}" analyzed — OCR blocks: {resp.get("ocr_blocks_count","N/A")}\n'
#                                     f'Saved: {resp.get("save_message","No")}'
#                                 )
#                         except Exception as e:
#                             assistant_msg = f"Analysis failed: {e}"

#                     # Append to chat history as assistant response to an implicit user upload action
#                     upload_question = f"[Uploaded file] {filename}"
#                     st.session_state.chat_history.append({'question': upload_question, 'answer': assistant_msg})

#                     # Rerender to show the newly appended chat message immediately
#                     st.rerun()

#     # --- TAB 3: TRENDS ---
#     with tab3:
#         df = storage.get_income_history(user_id, 90)
#         if not df.empty:
#             fig = px.area(df, x='date', y='income', title="Income Trend")
#             st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
#         else:
#             st.warning("No data yet.")

#     # --- TAB 4: GOALS ---
#     with tab4:
#         c_head, c_btn = st.columns([3, 1])
#         with c_head: st.markdown("### 🎯 Your Targets")
#         with c_btn: 
#             if st.button("➕ New Goal"): st.session_state.add_goal = True
            
#         if st.session_state.get('add_goal'):
#             with st.form("new_goal"):
#                 st.markdown("#### Create New Goal")
#                 g_name = st.text_input("Goal Name")
#                 g_target = st.number_input("Target Amount (₹)", 1000, 1000000, 10000)
                
#                 c1, c2 = st.columns(2)
#                 with c1:
#                     if st.form_submit_button("💾 Save"):
#                         goals = storage.get_goals(user_id)
#                         goals.append({
#                             'description': g_name, 
#                             'target_amount': g_target, 
#                             'status': 'active',
#                             'created_at': datetime.now().isoformat()
#                         })
#                         storage.set_goals(user_id, goals)
#                         st.session_state.add_goal = False
#                         st.rerun()
#                 with c2:
#                     if st.form_submit_button("Cancel"):
#                         st.session_state.add_goal = False
#                         st.rerun()
#             st.markdown("---")

#         goals = storage.get_goals(user_id)
#         total_savings = storage.get_total_savings(user_id)
        
#         # --- NEW LOGIC: Initialize remaining savings bucket ---
#         remaining_savings = total_savings 
#         # ------------------------------------------------------

#         if not goals:
#             st.info("No goals set yet.")
#         else:
#             cols = st.columns(3)
#             for i, goal in enumerate(goals):
#                 with cols[i % 3]:
#                     # 1. Normalize data
#                     if isinstance(goal, str): 
#                         display_goal = {'description': goal, 'target_amount': 0}
#                     else:
#                         display_goal = goal
                    
#                     target = display_goal.get('target_amount', 0)
                    
#                     # 2. WATERFALL LOGIC FIX
#                     # Allocate money to this goal, but don't exceed the target
#                     if target > 0:
#                         allocated = min(remaining_savings, target)
#                         remaining_savings -= allocated # Remove used money from bucket
#                         remaining_savings = max(0, remaining_savings) # Safety check
#                     else:
#                         allocated = 0
                    
#                     current = allocated
#                     # ----------------------
                    
#                     # 3. Ring Calculations
#                     pct = min(current / target, 1.0) * 100 if target > 0 else 0
                    
#                     radius = 50
#                     circumference = 314
#                     offset = circumference - (pct / 100) * circumference
#                     color = "#00B894" if pct >= 100 else "#6C5CE7"
                    
#                     # 4. Render Card
#                     html_content = f"""
# <div class="glass-card" style="text-align: center; position: relative;">
# <h4 style="margin: 0 0 10px 0; color: #636E72; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
#     {display_goal.get('description', 'Goal')}
# </h4>

# <div style="display: flex; justify-content: center; margin-bottom: 10px;">
# <svg width="120" height="120" style="transform: rotate(-90deg);">
#     <circle cx="60" cy="60" r="{radius}" fill="none" stroke="#eee" stroke-width="8" />
#     <circle cx="60" cy="60" r="{radius}" fill="none" stroke="{color}" stroke-width="8"
#             stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" stroke-linecap="round" 
#             style="--target-offset: {offset}; animation: fillCircle 1.5s ease-out forwards;"/>
# </svg>
# <div style="position: absolute; top: 38px; width: 100%; text-align: center;">
#     <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{int(pct)}%</div>
# </div>
# </div>

# <div style="font-size: 0.85rem; color: #aaa;">
#     ₹{current:,.0f} of <strong style="color: #2D3436;">₹{target:,.0f}</strong>
# </div>
# </div>
# """
#                     st.markdown(html_content, unsafe_allow_html=True)
                    
#                     if target == 0:
#                         st.warning("⚠️ Target not set")
                    
#                     with st.expander("✏️ Edit"):
#                         new_t = st.number_input("Target", value=int(target) if target > 0 else 5000, key=f"g_target_{i}")
                        
#                         c1, c2 = st.columns(2)
#                         with c1:
#                             if st.button("Update", key=f"g_update_{i}"):
#                                 if isinstance(goals[i], str):
#                                     goals[i] = {'description': goals[i], 'created_at': datetime.now().isoformat()}
#                                 goals[i]['target_amount'] = new_t
#                                 storage.set_goals(user_id, goals)
#                                 st.rerun()
#                         with c2:
#                             if st.button("Delete", key=f"g_delete_{i}"):
#                                 goals.pop(i)
#                                 storage.set_goals(user_id, goals)
#                                 st.rerun()

#     # --- TAB 5: SETTINGS ---
#     with tab5:
#         st.subheader("Settings")
        
#         col1, col2 = st.columns(2, gap="large")
        
#         # 1. AUTO-SAVE SETTINGS
#         with col1:
#             st.markdown('<div class="glass-card"><h4>💰 Auto-Save</h4></div>', unsafe_allow_html=True)
#             cur = int(profile.get('savings_rate', 0.05) * 100)
            
#             new_r = st.slider("Rate (%)", 1, 20, cur, key="settings_savings_rate")
            
#             if st.button("Update Rate", key="btn_update_rate"):
#                 storage.update_user(user_id, {'savings_rate': new_r/100})
#                 st.session_state.profile['savings_rate'] = new_r/100
#                 if hasattr(orchestrator, 'savings_agent'):
#                     orchestrator.savings_agent.savings_rate = new_r/100
#                 st.success("Updated!")
#                 st.rerun()

#         # 2. PROFILE READ-ONLY
#         with col2:
#             st.markdown(f"""
#             <div class="glass-card">
#                 <h4>👤 Profile</h4>
#                 <p><b>Name:</b> {profile['name']}</p>
#                 <p><b>City:</b> {profile.get('city', 'N/A')}</p>
#                 <p><b>Platform:</b> {profile.get('platform', 'N/A')}</p>
#             </div>
#             """, unsafe_allow_html=True)

#         st.markdown("---")
        
#         # 3. NEW SAVINGS ACTIVITY GRAPH
#         st.markdown("### 📊 Savings Activity (Last 30 Days)")
        
#         # Fetch data
#         savings_history = storage.get_savings_history(user_id, 30)
        
#         if not savings_history.empty:
#             # Group by date to handle multiple savings in one day
#             daily_savings = savings_history.groupby('date')['amount'].sum().reset_index()
            
#             fig = px.bar(
#                 daily_savings, 
#                 x='date', 
#                 y='amount', 
#                 title='',
#                 labels={'date': 'Date', 'amount': 'Saved (₹)'}
#             )
#             # Use specific pastel purple color for savings bars
#             fig.update_traces(marker_color='#AA96DA')
#             st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
#         else:
#             st.info("No savings history yet. Start working to see your progress!")

# def main():
#     if 'onboarding_complete' not in st.session_state:
#         show_onboarding()
#     else:
#         show_main_app()

# if __name__ == "__main__":
#     main()

# orginal->