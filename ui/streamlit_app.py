# ui/streamlit_app.py
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

# # Page configuration
# st.set_page_config(
#     page_title="StormGuard India - AI Financial Coach",
#     page_icon="🌦️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize storage
# storage = UserStorage()

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .onboarding-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 1rem;
#         color: white;
#         margin: 1rem 0;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin: 0.5rem 0;
#     }
#     .risk-high { background-color: #ffebee; border-left: 4px solid #f44336; padding: 1rem; }
#     .risk-medium { background-color: #fff8e1; border-left: 4px solid #ff9800; padding: 1rem; }
#     .risk-low { background-color: #e8f5e9; border-left: 4px solid #4caf50; padding: 1rem; }
# </style>
# """, unsafe_allow_html=True)


# def show_onboarding():
#     """New user onboarding flow"""
#     st.markdown('<p class="main-header">🌦️ Welcome to StormGuard India!</p>', unsafe_allow_html=True)
#     st.markdown("<h4 style='text-align: center; color: gray;'>AI-Powered Financial Coach for Gig Workers</h4>", unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Check for existing users
#     existing_users = storage.list_users()
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("### 🆕 New User? Let's Get Started!")
#         st.markdown("Create your profile in 2 minutes")
        
#         with st.form("onboarding_form"):
#             name = st.text_input("👤 Your Name *", placeholder="e.g., Rajesh Kumar")
#             age = st.number_input("🎂 Age", min_value=18, max_value=65, value=25)
#             city = st.selectbox("📍 City *", [
#                 "Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", 
#                 "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Other"
#             ])
            
#             platform = st.multiselect("🚚 Platforms You Work With *", [
#                 "Swiggy", "Zomato", "Dunzo", "Amazon Flex", 
#                 "Uber Eats", "Ola", "Uber", "Rapido", "Other"
#             ], default=["Swiggy"])
            
#             phone = st.text_input("📱 Phone (Optional)", placeholder="9876543210")
            
#             st.markdown("#### 🎯 Your Financial Goals")
#             goal1 = st.text_input("Goal 1", placeholder="e.g., Save ₹20,000 emergency fund")
#             goal2 = st.text_input("Goal 2 (Optional)", placeholder="e.g., Buy bike in 8 months")
            
#             savings_rate = st.slider(
#                 "💰 Auto-Save Rate (% of daily income)",
#                 min_value=2, max_value=10, value=5,
#                 help="We'll automatically save this % from your earnings"
#             )
            
#             st.markdown("#### 📊 Initial Data (Optional)")
#             has_history = st.checkbox("I want to enter my past income data")
#             generate_demo = st.checkbox("Generate demo data to explore the app", value=True)
            
#             submitted = st.form_submit_button("🚀 Create My Account", type="primary", use_container_width=True)
            
#             if submitted:
#                 if not name or not city or not platform:
#                     st.error("Please fill in all required fields (*)")
#                 else:
#                     # Create user
#                     goals = [g for g in [goal1, goal2] if g]
#                     if not goals:
#                         goals = ["Build emergency fund"]
                    
#                     user_data = {
#                         'name': name,
#                         'age': age,
#                         'city': city,
#                         'platform': " + ".join(platform),
#                         'platforms': platform,
#                         'phone': phone,
#                         'goals': goals,
#                         'savings_rate': savings_rate / 100,
#                         'language': 'hinglish'
#                     }
                    
#                     user_id = storage.create_user(user_data)
                    
#                     # Generate demo data if requested
#                     if generate_demo:
#                         simulator = GigWorkerSimulator(name, city)
#                         demo_income = simulator.generate_income_history(90)
#                         demo_spending = simulator.generate_spending_data(30)
                        
#                         # Save demo data
#                         for _, row in demo_income.iterrows():
#                             storage.add_income(user_id, row.to_dict())
#                         for _, row in demo_spending.iterrows():
#                             storage.add_expense(user_id, row.to_dict())
                    
#                     st.session_state.user_id = user_id
#                     st.session_state.onboarding_complete = True
#                     st.success(f"✅ Welcome aboard, {name}! Your account is ready.")
#                     st.rerun()
    
#     with col2:
#         st.markdown("### 👋 Returning User?")
#         st.markdown("Select your profile to continue")
        
#         if existing_users:
#             for user in existing_users:
#                 if st.button(
#                     f"👤 {user['name']} ({user['city']})", 
#                     key=f"user_{user['user_id']}",
#                     use_container_width=True
#                 ):
#                     st.session_state.user_id = user['user_id']
#                     st.session_state.onboarding_complete = True
#                     st.rerun()
#         else:
#             st.info("No existing users found. Create a new account!")
        
#         st.markdown("---")
#         st.markdown("### ✨ Why StormGuard?")
#         st.markdown("""
#         - 🔮 **Predict** your income for the week
#         - ⚠️ **Get alerts** before slow weeks
#         - 💰 **Auto-save** small amounts daily
#         - 🎯 **Track** progress toward your goals
#         - 💬 **Chat** with your AI financial coach
#         """)


# def initialize_app():
#     """Initialize app with user data"""
#     user_id = st.session_state.user_id
    
#     # Load user data
#     profile, income_df, spending_df = storage.get_data_for_agents(user_id)
    
#     # Check if we have enough data
#     if income_df.empty:
#         # Generate some initial data
#         simulator = GigWorkerSimulator(profile['name'], profile['city'])
#         income_df = simulator.generate_income_history(90)
#         spending_df = simulator.generate_spending_data(30)
        
#         # Save generated data
#         for _, row in income_df.iterrows():
#             storage.add_income(user_id, row.to_dict())
#         for _, row in spending_df.iterrows():
#             storage.add_expense(user_id, row.to_dict())
    
#     # Initialize orchestrator
#     orchestrator = OrchestratorAgent(profile, income_df, spending_df)
    
#     return profile, income_df, spending_df, orchestrator


# def show_data_entry_sidebar(user_id, profile):
#     """Sidebar with data entry forms"""
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### 📝 Quick Entry")
    
#     entry_type = st.sidebar.selectbox("Add New:", ["💰 Today's Income", "💸 Expense", "🎯 New Goal"])
    
#     if entry_type == "💰 Today's Income":
#         with st.sidebar.form("income_form"):
#             income_date = st.date_input("Date", datetime.now())
#             income_amount = st.number_input("Income (₹)", min_value=0, value=500, step=50)
#             hours_worked = st.number_input("Hours Worked", min_value=1, max_value=16, value=8)
#             orders = st.number_input("Orders Completed", min_value=0, value=20)
#             platform = st.selectbox("Platform", profile.get('platforms', ['Swiggy', 'Zomato']))
            
#             if st.form_submit_button("💾 Save Income", use_container_width=True):
#                 storage.add_income(user_id, {
#                     'date': income_date.strftime('%Y-%m-%d'),
#                     'income': income_amount,
#                     'hours_worked': hours_worked,
#                     'orders_completed': orders,
#                     'platform': platform,
#                     'efficiency': round(income_amount / hours_worked, 2),
#                     'weather': 'clear',
#                     'is_festival': False,
#                     'is_weekend': income_date.weekday() >= 5
#                 })
                
#                 # Auto-save
#                 savings_rate = profile.get('savings_rate', 0.05)
#                 savings_amount = income_amount * savings_rate
#                 storage.add_savings(user_id, {
#                     'date': income_date.strftime('%Y-%m-%d'),
#                     'amount': savings_amount,
#                     'source': 'auto_save',
#                     'income_ref': income_amount
#                 })
                
#                 st.sidebar.success(f"✅ Saved! Auto-saved ₹{savings_amount:.0f}")
#                 st.rerun()
    
#     elif entry_type == "💸 Expense":
#         with st.sidebar.form("expense_form"):
#             exp_date = st.date_input("Date", datetime.now())
#             exp_amount = st.number_input("Amount (₹)", min_value=0, value=100, step=10)
#             exp_category = st.selectbox("Category", [
#                 "food", "fuel", "phone", "rent", "entertainment", 
#                 "family_support", "medical", "shopping", "other"
#             ])
#             exp_desc = st.text_input("Description", placeholder="e.g., Lunch")
            
#             if st.form_submit_button("💾 Save Expense", use_container_width=True):
#                 storage.add_expense(user_id, {
#                     'date': exp_date.strftime('%Y-%m-%d'),
#                     'amount': exp_amount,
#                     'category': exp_category,
#                     'description': exp_desc
#                 })
#                 st.sidebar.success("✅ Expense saved!")
#                 st.rerun()
    
#     else:  # New Goal
#         with st.sidebar.form("goal_form"):
#             new_goal = st.text_input("Goal Description", placeholder="e.g., Save ₹50,000 for bike")
            
#             if st.form_submit_button("🎯 Add Goal", use_container_width=True):
#                 current_goals = storage.get_goals(user_id)
#                 goals_text = [g['description'] if isinstance(g, dict) else g for g in current_goals]
#                 goals_text.append(new_goal)
#                 storage.set_goals(user_id, goals_text)
#                 st.sidebar.success("✅ Goal added!")
#                 st.rerun()


# def show_main_app():
#     """Main application"""
#     user_id = st.session_state.user_id
    
#     # Initialize
#     if 'orchestrator' not in st.session_state:
#         with st.spinner("🔧 Loading your data..."):
#             profile, income_df, spending_df, orchestrator = initialize_app()
#             st.session_state.profile = profile
#             st.session_state.income_data = income_df
#             st.session_state.spending_data = spending_df
#             st.session_state.orchestrator = orchestrator
#             st.session_state.savings_rate = profile.get('savings_rate', 0.05)
#             st.session_state.daily_report = None
#             st.session_state.chat_history = []
    
#     profile = st.session_state.profile
#     orchestrator = st.session_state.orchestrator
    
#     # Header
#     st.markdown('<p class="main-header">🌦️ StormGuard India</p>', unsafe_allow_html=True)
#     st.markdown("<h4 style='text-align: center; color: gray;'>AI-Powered Financial Weather System for Gig Workers</h4>", unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={profile['name']}", width=120)
#         st.markdown(f"### 👋 {profile['name']}")
#         st.markdown(f"📍 {profile.get('city', 'Unknown')}")
#         st.markdown(f"🚚 {profile.get('platform', 'Delivery Partner')}")
        
#         # Quick Stats
#         income_summary = storage.get_income_summary(user_id, 30)
#         total_savings = storage.get_total_savings(user_id)
        
#         st.markdown("---")
#         st.markdown("### 📊 Last 30 Days")
#         st.metric("Total Income", f"₹{income_summary['total_income']:,.0f}")
#         st.metric("Daily Average", f"₹{income_summary['avg_daily']:,.0f}")
#         st.metric("Total Saved", f"₹{total_savings:,.0f}")
        
#         # Daily Check Button
#         st.markdown("---")
#         if st.button("🔄 Run Daily Check", type="primary", use_container_width=True):
#             with st.spinner("🔮 Analyzing... (15-20 sec)"):
#                 st.session_state.daily_report = orchestrator.run_daily_check()
#             st.success("✅ Analysis complete!")
#             st.rerun()
        
#         # Data Entry
#         show_data_entry_sidebar(user_id, profile)
        
#         # Logout
#         st.markdown("---")
#         if st.button("🚪 Switch User", use_container_width=True):
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.rerun()
    
#     # Main Content Tabs
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "📊 Dashboard", "💬 AI Coach", "📈 My Data", "🎯 Goals", "⚙️ Settings"
#     ])
    
#     # TAB 1: DASHBOARD
#     with tab1:
#         if st.session_state.daily_report is None:
#             st.info("👆 Click **'Run Daily Check'** to see your financial forecast!")
            
#             # Show recent income chart
#             st.markdown("### 📈 Your Recent Income")
#             income_df = st.session_state.income_data
#             if not income_df.empty:
#                 recent = income_df.tail(30)
#                 fig = px.line(recent, x='date', y='income', title='Last 30 Days Income')
#                 fig.update_traces(line_color='#1f77b4', line_width=3)
#                 st.plotly_chart(fig, use_container_width=True)
#         else:
#             report = st.session_state.daily_report
#             dash = report['dashboard']
            
#             # Health Score
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 score = dash['summary']['financial_health_score']
#                 emoji = "💚" if score >= 75 else "💛" if score >= 50 else "🔴"
#                 st.metric("Health Score", f"{emoji} {score}/100")
#             with col2:
#                 st.metric("Weekly Forecast", f"₹{dash['summary']['weekly_income_forecast']:,.0f}")
#             with col3:
#                 st.metric("Savings Rate", f"{dash['summary']['savings_rate']:.1f}%")
#             with col4:
#                 st.metric("Risk Level", dash['risks']['level'])
            
#             st.markdown("---")
            
#             # Coaching
#             st.markdown("### 💬 Today's Advice")
#             st.success(report['coaching'])
            
#             # Alerts
#             if report['interventions']:
#                 st.markdown("### ⚠️ Alerts")
#                 for alert in report['interventions']:
#                     if alert['severity'] == 'HIGH':
#                         st.error(f"🔴 {alert['category']}: {alert['message'][:200]}...")
#                     elif alert['severity'] == 'MEDIUM':
#                         st.warning(f"🟡 {alert['category']}: {alert['message'][:200]}...")
#                     else:
#                         st.info(f"🟢 {alert['category']}: {alert['message'][:200]}...")
    
#     # TAB 2: AI COACH
#     with tab2:
#         st.markdown("### 💬 Chat with Your AI Coach")
        
#         # Chat history
#         for chat in st.session_state.get('chat_history', []):
#             with st.chat_message("user"):
#                 st.markdown(chat['question'])
#             with st.chat_message("assistant"):
#                 st.markdown(chat['answer'])
        
#         # Chat input
#         user_q = st.chat_input("Ask anything... (e.g., 'Should I work Sunday?')")
#         if user_q:
#             with st.chat_message("user"):
#                 st.markdown(user_q)
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     response = orchestrator.chat(user_q)
#                 st.markdown(response)
            
#             st.session_state.chat_history.append({'question': user_q, 'answer': response})
    
#     # TAB 3: MY DATA
#     with tab3:
#         st.markdown("### 📈 Your Financial Data")
        
#         data_view = st.radio("View:", ["Income History", "Spending History", "Savings"], horizontal=True)
        
#         if data_view == "Income History":
#             income_df = storage.get_income_history(user_id, 90)
#             if not income_df.empty:
#                 st.dataframe(income_df.tail(30), use_container_width=True)
                
#                 fig = px.line(income_df, x='date', y='income', title='Income Over Time')
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("No income data yet. Add your first entry!")
        
#         elif data_view == "Spending History":
#             spending_df = storage.get_spending_history(user_id, 30)
#             if not spending_df.empty:
#                 summary = storage.get_spending_summary(user_id, 30)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.metric("Total Spent", f"₹{summary['total_spent']:,.0f}")
#                 with col2:
#                     st.metric("Daily Average", f"₹{summary['daily_average']:,.0f}")
                
#                 # Category breakdown
#                 fig = px.pie(
#                     values=list(summary['by_category'].values()),
#                     names=list(summary['by_category'].keys()),
#                     title='Spending by Category'
#                 )
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("No spending data yet.")
        
#         else:  # Savings
#             total = storage.get_total_savings(user_id)
#             st.metric("Total Saved", f"₹{total:,.0f}")
            
#             savings_df = storage.get_savings_history(user_id, 90)
#             if not savings_df.empty:
#                 savings_df['cumulative'] = savings_df['amount'].cumsum()
#                 fig = px.area(savings_df, x='date', y='cumulative', title='Savings Growth')
#                 st.plotly_chart(fig, use_container_width=True)
    
#     # TAB 4: GOALS
#     with tab4:
#         st.markdown("### 🎯 Your Goals")
        
#         goals = storage.get_goals(user_id)
#         total_savings = storage.get_total_savings(user_id)
        
#         for i, goal in enumerate(goals):
#             desc = goal['description'] if isinstance(goal, dict) else goal
#             target = goal.get('target_amount', 0) if isinstance(goal, dict) else storage._extract_amount(goal)
            
#             if target > 0:
#                 progress = min((total_savings / target) * 100, 100)
#                 st.markdown(f"**{desc}**")
#                 st.progress(progress / 100)
#                 st.markdown(f"₹{total_savings:,.0f} / ₹{target:,} ({progress:.1f}%)")
#             else:
#                 st.markdown(f"**{desc}**")
#             st.markdown("")
    
#     # TAB 5: SETTINGS
#     with tab5:
#         st.markdown("### ⚙️ Settings")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("#### 💰 Savings Rate")
#             new_rate = st.slider(
#                 "Auto-save percentage",
#                 min_value=1, max_value=20,
#                 value=int(st.session_state.savings_rate * 100)
#             )
            
#             if st.button("Update Savings Rate"):
#                 storage.update_user(user_id, {'savings_rate': new_rate / 100})
#                 st.session_state.savings_rate = new_rate / 100
#                 orchestrator.adjust_savings_rate(new_rate / 100)
#                 st.success(f"✅ Updated to {new_rate}%")
        
#         with col2:
#             st.markdown("#### 👤 Profile")
#             profile = storage.get_user(user_id)
#             st.write(f"**Name:** {profile['name']}")
#             st.write(f"**City:** {profile.get('city', 'N/A')}")
#             st.write(f"**Platform:** {profile.get('platform', 'N/A')}")
#             st.write(f"**Member since:** {profile.get('created_at', 'N/A')[:10]}")


# # ==================== MAIN ====================

# def main():
#     # Check if user is logged in
#     if 'onboarding_complete' not in st.session_state or not st.session_state.onboarding_complete:
#         show_onboarding()
#     else:
#         show_main_app()

# if __name__ == "__main__":
#     main()


import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
import json
from datetime import datetime, timedelta

# Add parent directory to path FIRST
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.storage import UserStorage
from data.simulator import GigWorkerSimulator
from agents.orchestrator_agent import OrchestratorAgent


# Add near other imports at top of file
import base64
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes

# Import your screenshot analyzer tool (adjust path if needed)
# from .agents/financial_coach_agent import analyze_screenshot_tool
from agents.financial_coach_agent import analyze_screenshot_tool

# Page configuration
st.set_page_config(
    page_title="StormGuard India",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize storage
storage = UserStorage()

# ==================== UI STYLING & THEME ====================

def _file_to_b64(file_bytes: bytes, mime: str) -> str:
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def analyze_image_bytes(user_id: str, img_bytes: bytes, filename: str = None):
    """Send a single image (bytes) to analyze_screenshot_tool via base64 string."""
    mime = "image/png"
    b64 = _file_to_b64(img_bytes, mime)
    # Call the tool entrypoint (this will attempt to save to storage inside the tool)
    resp_json = analyze_screenshot_tool.entrypoint(user_id, image_b64=b64, filename=filename)
    try:
        return json.loads(resp_json)
    except Exception:
        return {"raw": resp_json}

def analyze_pdf_bytes(user_id: str, pdf_bytes: bytes, filename_prefix: str = None):
    """Convert PDF to images and analyze each page. Returns list of page-results."""
    pages = convert_from_bytes(pdf_bytes, dpi=200)  # adjust dpi if needed
    results = []
    for i, page in enumerate(pages, start=1):
        buff = BytesIO()
        page.save(buff, format="PNG")
        img_bytes = buff.getvalue()
        fname = f"{(filename_prefix or 'upload')}_page_{i}.png"
        r = analyze_image_bytes(user_id, img_bytes, filename=fname)
        results.append({"page": i, "filename": fname, "result": r})
    return results


def apply_custom_styles():
    st.markdown("""
    <style>
        /* IMPORT GOOGLE FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

        /* GLOBAL VARIABLES */
        :root {
            --primary: #6C5CE7;
            --secondary: #00B894;
            --accent: #FF7675;
            --bg-color: #F8F9FD;
            --card-bg: #FFFFFF;
            --text-color: #2D3436;
        }

        /* GENERAL SETTINGS */
        .stApp {
            background-color: var(--bg-color);
            font-family: 'Outfit', sans-serif;
            color: var(--text-color);
        }
        
        h1, h2, h3, h4, h5 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: #2D3436;
        }

        /* CUSTOM GRADIENT HEADER */
        .main-header {
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
            animation: fadeIn 1.5s ease-in-out;
        }

        .sub-header {
            text-align: center;
            color: #636e72;
            font-weight: 400;
            margin-bottom: 2rem;
            animation: fadeIn 2s ease-in-out;
        }

        /* ANIMATIONS */
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(108, 92, 231, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(108, 92, 231, 0); }
            100% { box-shadow: 0 0 0 0 rgba(108, 92, 231, 0); }
        }

        /* CARDS & CONTAINERS */
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeIn 0.8s ease-out;
        }

        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
        }

        /* METRIC CARDS */
        .metric-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #636e72;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2D3436;
        }

        /* ALERTS */
        .alert-box {
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .alert-high { background-color: #ffebee; border-left: 5px solid #ff7675; color: #d63031; }
        .alert-medium { background-color: #fff8e1; border-left: 5px solid #fdcb6e; color: #e17055; }
        .alert-low { background-color: #e8f5e9; border-left: 5px solid #00b894; color: #009474; }

        /* BUTTONS */
        .stButton > button {
            background: linear-gradient(90deg, #6C5CE7 0%, #a29bfe 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(108, 92, 231, 0.2);
        }
        
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 7px 14px rgba(108, 92, 231, 0.4);
        }

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #f1f1f1;
        }
        
        /* TABS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: white;
            border-radius: 10px;
            color: #636e72;
            font-weight: 600;
            border: 1px solid #f1f1f1;
            padding: 0 20px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #e3f2fd;
            color: #0984e3;
            border-color: #74b9ff;
        }
    </style>
    """, unsafe_allow_html=True)

def apply_pastel_theme(fig):
    """Apply pastel theme to Plotly charts"""
    pastel_colors = ['#6C5CE7', '#00B894', '#FF7675', '#74B9FF', '#FAB1A0', '#FFEAA7']
    
    fig.update_layout(
        font={'family': 'Outfit, sans-serif', 'color': '#2d3436'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        colorway=pastel_colors
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    return fig

# ==================== APP LOGIC ====================

@st.cache_resource
def get_orchestrator(profile, _income_df, _spending_df):
    """Cache the orchestrator to prevent reloading issues"""
    return OrchestratorAgent(profile, _income_df, _spending_df)

def show_onboarding():
    """New user onboarding flow"""
    apply_custom_styles()
    
    st.markdown('<div class="main-header">🌦️ StormGuard India</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI-Powered Financial Safety Net</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 0.8], gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>🚀 Create Your Profile</h3>
            <p style="color: #636e72;">Join thousands of gig workers securing their future.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            
            platform = st.multiselect("🚚 Platforms You Work With *", [
                "Swiggy", "Zomato", "Dunzo", "Amazon Flex", 
                "Uber Eats", "Ola", "Uber", "Rapido", "Other"
            ], default=["Swiggy"])
            
            phone = st.text_input("📱 Phone (Optional)", placeholder="9876543210")
            
            st.markdown("#### 🎯 Your Financial Goals")
            goal1 = st.text_input("Goal 1", placeholder="e.g., Save ₹20,000 emergency fund")
            
            st.markdown("#### 💰 Daily Savings (Pigmy Style)")
            savings_rate = st.slider(
                "Auto-Save Percentage (%)",
                min_value=2, max_value=10, value=5,
                help="We'll automatically save this % from your earnings"
            )
            
            generate_demo = st.checkbox("Generate demo data to explore the app", value=True)
            
            submitted = st.form_submit_button("Start My Journey 🚀", use_container_width=True)
            
            if submitted:
                if not name or not city or not platform:
                    st.error("Please fill in all required fields (*)")
                else:
                    goals = [g for g in [goal1] if g] or ["Build emergency fund"]
                    
                    user_data = {
                        'name': name, 'age': age, 'city': city,
                        'platform': " + ".join(platform), 'platforms': platform,
                        'phone': phone, 'goals': goals,
                        'savings_rate': savings_rate / 100, 'language': 'hinglish'
                    }
                    
                    user_id = storage.create_user(user_data)
                    
                    if generate_demo:
                        simulator = GigWorkerSimulator(name, city)
                        demo_income = simulator.generate_income_history(90)
                        demo_spending = simulator.generate_spending_data(30)
                        for _, row in demo_income.iterrows():
                            storage.add_income(user_id, row.to_dict())
                        for _, row in demo_spending.iterrows():
                            storage.add_expense(user_id, row.to_dict())
                    
                    st.session_state.user_id = user_id
                    st.session_state.onboarding_complete = True
                    st.rerun()

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>👋 Returning User?</h3>
            <p>Select your profile to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        existing_users = storage.list_users()
        if existing_users:
            for user in existing_users:
                if st.button(
                    f"👤 {user['name']} ({user['city']})", 
                    key=f"user_{user['user_id']}",
                    use_container_width=True
                ):
                    st.session_state.user_id = user['user_id']
                    st.session_state.onboarding_complete = True
                    st.rerun()
        else:
            st.info("No users found. Create a new one!")
            
        st.markdown("""
        <div class="glass-card" style="margin-top: 20px; background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); color: white;">
            <h4>✨ Why StormGuard?</h4>
            <ul style="padding-left: 20px;">
                <li>🔮 <b>Predict</b> income & weather</li>
                <li>⚠️ <b>Avoid</b> slow weeks</li>
                <li>💰 <b>Auto-save</b> daily</li>
                <li>💬 <b>Chat</b> with AI coach</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def initialize_app():
    """Initialize app with user data"""
    user_id = st.session_state.user_id
    profile, income_df, spending_df = storage.get_data_for_agents(user_id)
    
    # Generate data if missing
    if income_df.empty:
        simulator = GigWorkerSimulator(profile['name'], profile['city'])
        income_df = simulator.generate_income_history(90)
        spending_df = simulator.generate_spending_data(30)
        for _, row in income_df.iterrows():
            storage.add_income(user_id, row.to_dict())
        for _, row in spending_df.iterrows():
            storage.add_expense(user_id, row.to_dict())
    
    orchestrator = get_orchestrator(profile, income_df, spending_df)
    return profile, income_df, spending_df, orchestrator

def show_data_entry_sidebar(user_id, profile):
    """Sidebar with data entry forms"""
    st.sidebar.markdown("### 📝 Quick Actions")
    
    with st.sidebar.expander("💰 Add Income", expanded=False):
        with st.form("income_form"):
            income_date = st.date_input("Date", datetime.now())
            income_amount = st.number_input("Income (₹)", min_value=0, value=500, step=50)
            hours_worked = st.number_input("Hours", min_value=1, max_value=16, value=8)
            platform = st.selectbox("Platform", profile.get('platforms', ['Swiggy', 'Zomato']))
            
            if st.form_submit_button("Save Income"):
                storage.add_income(user_id, {
                    'date': income_date.strftime('%Y-%m-%d'),
                    'income': income_amount,
                    'hours_worked': hours_worked,
                    'platform': platform,
                    'is_weekend': income_date.weekday() >= 5
                })
                # Auto-save logic
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
                storage.add_expense(user_id, {
                    'date': exp_date.strftime('%Y-%m-%d'),
                    'amount': exp_amount,
                    'category': exp_category
                })
                st.success("Expense saved!")
                st.rerun()

def show_main_app():
    apply_custom_styles()
    user_id = st.session_state.user_id
    
    # Initialize
    if 'orchestrator' not in st.session_state:
        with st.spinner("🔧 Loading your financial weather..."):
            profile, income_df, spending_df, orchestrator = initialize_app()
            st.session_state.profile = profile
            st.session_state.income_data = income_df
            st.session_state.spending_data = spending_df
            st.session_state.orchestrator = orchestrator
            st.session_state.daily_report = None
            st.session_state.chat_history = []
            st.rerun()

    profile = st.session_state.profile
    orchestrator = st.session_state.orchestrator
    
    # Sidebar Profile
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={profile['name']}" width="100" style="border-radius: 50%; border: 3px solid #6c5ce7;">
            <h3 style="margin: 10px 0 0 0;">{profile['name']}</h3>
            <p style="color: #636e72; margin: 0;">{profile.get('city', 'India')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        show_data_entry_sidebar(user_id, profile)
        
        st.markdown("---")
        if st.button("🔄 Run Daily Check", type="primary", use_container_width=True):
            with st.spinner("🔮 AI is analyzing market conditions..."):
                try:
                    st.session_state.daily_report = orchestrator.run_daily_check()
                except Exception as e:
                    st.error(f"Error running check: {e}")
            st.rerun()
            
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Main Header
    st.markdown('<div class="main-header">🌦️ StormGuard Dashboard</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Forecast", "💬 AI Coach", "📈 Trends", "🎯 Goals", "⚙️ Settings"
    ])
    
    # TAB 1: DASHBOARD
    # TAB 1: DASHBOARD
    with tab1:
        if st.session_state.daily_report is None:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 40px;">
                <h2>👋 Good Morning, {profile['name']}!</h2>
                <p>Click <b>'Run Daily Check'</b> in the sidebar to get your income forecast.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show income chart even without daily report
            income_df = st.session_state.income_data
            if not income_df.empty:
                st.markdown("### 📈 Recent Trends")
                recent = income_df.tail(30)
                fig = px.area(recent, x='date', y='income', title='Last 30 Days Income')
                st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
                
        else:
            report = st.session_state.daily_report
            dash = report['dashboard']
            
            # Custom Metric Cards
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                score = dash['summary']['financial_health_score']
                color = "#00b894" if score >= 75 else "#fdcb6e" if score >= 50 else "#ff7675"
                st.markdown(f"""
                <div class="glass-card metric-container">
                    <span class="metric-label">Health Score</span>
                    <span class="metric-value" style="color: {color}">{score}/100</span>
                </div>
                """, unsafe_allow_html=True)
                
            with c2:
                st.markdown(f"""
                <div class="glass-card metric-container">
                    <span class="metric-label">Weekly Forecast</span>
                    <span class="metric-value">₹{dash['summary']['weekly_income_forecast']:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
                
            with c3:
                st.markdown(f"""
                <div class="glass-card metric-container">
                    <span class="metric-label">Savings Rate</span>
                    <span class="metric-value">{dash['summary']['savings_rate']:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
                
            with c4:
                risk = dash['risks']['level']
                r_color = "#ff7675" if risk == "HIGH" else "#00b894"
                st.markdown(f"""
                <div class="glass-card metric-container">
                    <span class="metric-label">Risk Level</span>
                    <span class="metric-value" style="color: {r_color}">{risk}</span>
                </div>
                """, unsafe_allow_html=True)

            # Main Content Grid
            col_main, col_side = st.columns([2, 1])
            
            with col_main:
                st.markdown("### 🔮 Income Weather")
                
                # --- FIX IS HERE: Access the inner 'predictions' list ---
                forecast_data = pd.DataFrame(report['forecast']['predictions']['predictions'])
                # ---------------------------------------------------------
                
                fig = px.bar(forecast_data, x='day_name', y='predicted_income', 
                             title="Next 7 Days Forecast", text_auto='.0s')
                st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
                
                st.markdown("### 💬 Coach's Advice")
                st.info(report['coaching'])

            with col_side:
                st.markdown("### ⚠️ Alerts")
                if report['interventions']:
                    for alert in report['interventions']:
                        alert_class = f"alert-{alert['severity'].lower()}"
                        st.markdown(f"""
                        <div class="alert-box {alert_class}">
                            <div>
                                <div style="font-size: 0.8rem; text-transform: uppercase;">{alert['category']}</div>
                                <div>{alert['message']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No urgent risks detected!")
       # TAB 2: AI COACH
    with tab2:
        st.markdown("### 💬 Chat with StormGuard — Upload or Ask in the same place")

        # Render existing chat history (if any)
        for chat in st.session_state.get('chat_history', []):
            with st.chat_message("user", avatar="👤"):
                st.markdown(chat['question'])
            with st.chat_message("assistant", avatar="🌦️"):
                st.markdown(chat['answer'])

        # Two-column input area: left = text chat input, right = compact uploader
        col_text, col_upload = st.columns([3, 1])

        # ---------- Text input (left) ----------
        with col_text:
            user_q = st.chat_input("Ask about savings, shifts, or spending... (or attach a file on the right)")
            if user_q:
                # append user message placeholder to history and call orchestrator
                st.session_state.chat_history.append({'question': user_q, 'answer': None})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(user_q)
                with st.chat_message("assistant", avatar="🌦️"):
                    with st.spinner("Thinking..."):
                        try:
                            response = orchestrator.chat(user_q)
                        except Exception as e:
                            response = f"Agent error: {e}"
                        st.markdown(response)
                        # update last placeholder entry
                        for h in reversed(st.session_state.chat_history):
                            if h['answer'] is None and h['question'] == user_q:
                                h['answer'] = response
                                break

        # ---------- File uploader (right) ----------
        with col_upload:
            st.markdown("**📎 Upload**")
            uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"],
                                             accept_multiple_files=False, key="coach_uploader")
            if uploaded_file is not None:
                filename = uploaded_file.name
                file_bytes = uploaded_file.read()
                file_type = uploaded_file.type

                # preview (images only)
                if file_type.startswith('image'):
                    try:
                        img = Image.open(BytesIO(file_bytes)).convert("RGB")
                        st.image(img, caption=filename, use_column_width=True)
                    except Exception:
                        st.write("(Preview unavailable)")
                else:
                    st.write(f"Uploaded: {filename} (PDF)")

                # Analyze & attach the analysis as an assistant message
                if st.button("Analyze & Attach", key=f"analyze_{filename}"):
                    with st.spinner("Analyzing upload..."):
                        try:
                            if file_type == "application/pdf":
                                page_results = analyze_pdf_bytes(
                                    st.session_state.user_id,
                                    file_bytes,
                                    filename_prefix=os.path.splitext(filename)[0]
                                )
                                # Build a short multi-page summary
                                summary_lines = [f'PDF "{filename}" — {len(page_results)} page(s) analyzed.']
                                for p in page_results:
                                    features = p.get('result', {}) if isinstance(p, dict) else {}
                                    summary_lines.append(
                                        f"Page {p['page']}: OCR blocks={features.get('ocr_blocks_count','N/A')} | saved={features.get('save_message','No')}"
                                    )
                                assistant_msg = "\n".join(summary_lines)
                            else:
                                # image
                                resp = analyze_image_bytes(st.session_state.user_id, file_bytes, filename=filename)
                                assistant_msg = (
                                    f'Image "{filename}" analyzed — OCR blocks: {resp.get("ocr_blocks_count","N/A")}\n'
                                    f'Saved: {resp.get("save_message","No")}'
                                )
                        except Exception as e:
                            assistant_msg = f"Analysis failed: {e}"

                    # Append to chat history as assistant response to an implicit user upload action
                    upload_question = f"[Uploaded file] {filename}"
                    st.session_state.chat_history.append({'question': upload_question, 'answer': assistant_msg})

                    # Rerender to show the newly appended chat message immediately
                    st.rerun()


    # TAB 3: DATA
    with tab3:
        st.markdown("### 📈 Financial Trends")
        
        data_view = st.selectbox("Select View", ["Income Analysis", "Spending Breakdown", "Savings Growth"])
        
        if data_view == "Income Analysis":
            df = storage.get_income_history(user_id, 90)
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.line(df, x='date', y='income', title='Daily Income Trend')
                    st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
                with col2:
                    if 'platform' in df.columns:
                        fig2 = px.box(df, x='platform', y='income', title='Income by Platform')
                        st.plotly_chart(apply_pastel_theme(fig2), use_container_width=True)
        
        elif data_view == "Spending Breakdown":
            summary = storage.get_spending_summary(user_id, 30)
            if summary['total_spent'] > 0:
                col1, col2 = st.columns(2)
                with col1:
                    # Pie chart
                    labels = list(summary['by_category'].keys())
                    values = list(summary['by_category'].values())
                    fig = px.pie(values=values, names=labels, title='Where is your money going?', hole=0.4)
                    st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
                with col2:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>Total Spent (30 Days)</h4>
                        <h2 style="color: #ff7675;">₹{summary['total_spent']:,.0f}</h2>
                        <p>Top Category: <b>{summary['top_category']}</b></p>
                    </div>
                    """, unsafe_allow_html=True)

        elif data_view == "Savings Growth":
             savings_df = storage.get_savings_history(user_id, 90)
             if not savings_df.empty:
                 savings_df['cumulative'] = savings_df['amount'].cumsum()
                 fig = px.area(savings_df, x='date', y='cumulative', title='Total Savings Growth')
                 st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)

    # TAB 4: GOALS
    with tab4:
        st.markdown("### 🎯 Goals Progress")
        goals = storage.get_goals(user_id)
        total_savings = storage.get_total_savings(user_id)
        
        col1, col2 = st.columns(2)
        
        for i, goal in enumerate(goals):
            # Handle both string and dict formats
            desc = goal['description'] if isinstance(goal, dict) else goal
            target = goal.get('target_amount', 0) if isinstance(goal, dict) else storage._extract_amount(goal)
            
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div class="glass-card">
                    <h4>{desc}</h4>
                """, unsafe_allow_html=True)
                
                if target > 0:
                    progress = min((total_savings / target), 1.0)
                    st.progress(progress)
                    st.caption(f"₹{total_savings:,.0f} / ₹{target:,.0f} ({progress*100:.1f}%)")
                else:
                    st.info("No target amount set")
                
                st.markdown("</div>", unsafe_allow_html=True)

    # TAB 5: SETTINGS
    # TAB 5: SETTINGS
    with tab5:
        st.markdown("### ⚙️ Account Settings")
        
        col1, col2 = st.columns(2, gap="large")
        
        # SECTION 1: Savings Settings
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="margin-top: 0; color: #6c5ce7;">💰 Auto-Save Configuration</h4>
                <p style="font-size: 0.9rem; color: #636e72;">
                    We automatically set aside this percentage from every income entry.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Slider outside the HTML card so it functions correctly
            current_rate = int(profile.get('savings_rate', 0.05) * 100)
            new_rate = st.slider("Daily Savings (%)", 1, 20, value=current_rate)
            
            if st.button("💾 Update Rate", use_container_width=True):
                # 1. Update Database
                storage.update_user(user_id, {'savings_rate': new_rate / 100})
                
                # 2. Update Session State (CRITICAL FIX)
                st.session_state.profile['savings_rate'] = new_rate / 100
                
                # 3. Update Live Agent
                if hasattr(orchestrator, 'savings_agent'):
                    orchestrator.savings_agent.savings_rate = new_rate / 100
                
                st.success(f"✅ Updated! New rate: {new_rate}%")
                st.rerun() # Refresh app to show new value
            
        # SECTION 2: Profile Read-Only
        with col2:
            # We can put static text inside the HTML card safely
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="margin-top: 0; color: #6c5ce7;">👤 Profile Details</h4>
                <div style="margin-top: 15px;">
                    <p><b>Name:</b> {profile['name']}</p>
                    <p><b>City:</b> {profile.get('city', 'N/A')}</p>
                    <p><b>Primary Platform:</b> {profile.get('platform', 'N/A')}</p>
                    <p><b>Joined:</b> {profile.get('created_at', datetime.now().isoformat())[:10]}</p>
                    <hr style="border-top: 1px solid #eee;">
                    <p style="font-size: 0.8rem; color: gray;">User ID: {user_id}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚠️ Clear All Data (Reset)", type="secondary"):
                # Add logic here if you want a hard reset feature
                st.warning("This feature is disabled in demo mode.")

def main():
    if 'onboarding_complete' not in st.session_state:
        show_onboarding()
    else:
        show_main_app()

if __name__ == "__main__":
    main()