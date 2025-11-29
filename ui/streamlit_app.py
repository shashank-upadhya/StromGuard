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
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

        :root {
            --primary: #A8D8EA;
            --text-dark: #2D3436;
            --text-light: #636E72;
        }

        .stApp {
            background: linear-gradient(135deg, #F7F9FC 0%, #E8F0F5 100%);
            font-family: 'Outfit', sans-serif;
            color: var(--text-dark);
        }
        
        /* HEADERS */
        .main-header {
            background: linear-gradient(120deg, #6C5CE7, #00B894);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        /* GLASS CARDS */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.8);
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
        }

        /* METRICS */
        .metric-container {
            text-align: center;
            padding: 10px;
        }
        .metric-label {
            font-size: 0.85rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-dark);
        }

        /* TABS */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 10px;
            padding: 10px 20px;
            border: 1px solid #eee;
        }
        .stTabs [aria-selected="true"] {
            background-color: #e3f2fd;
            border-color: #90caf9;
            color: #1565c0;
        }

        /* ALERTS */
        .alert-box {
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .alert-high { background: #ffebee; border-left: 4px solid #ef5350; color: #c62828; }
        .alert-medium { background: #fff3e0; border-left: 4px solid #ff9800; color: #ef6c00; }
        .alert-low { background: #e8f5e9; border-left: 4px solid #66bb6a; color: #2e7d32; }

        /* GOAL RINGS ANIMATION */
        @keyframes fillCircle {
            from { stroke-dashoffset: 314; }
            to { stroke-dashoffset: var(--target-offset); }
        }
        svg circle { transition: stroke-dashoffset 1s ease-out; }
    </style>
    """, unsafe_allow_html=True)

def apply_pastel_theme(fig):
    pastel_colors = ['#6C5CE7', '#00B894', '#FF7675', '#74B9FF', '#FAB1A0']
    fig.update_layout(
        font={'family': 'Outfit, sans-serif', 'color': '#2d3436'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=30, b=10),
        colorway=pastel_colors
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    return fig

# ==================== APP LOGIC ====================

@st.cache_resource
def get_orchestrator(profile, _income_df, _spending_df):
    return OrchestratorAgent(profile, _income_df, _spending_df)

def show_onboarding():
    apply_custom_styles()
    st.markdown('<div class="main-header">🌦️ StormGuard India</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 0.8], gap="large")
    
    with col1:
        st.markdown("""<div class="glass-card"><h3>🚀 Create Your Profile</h3></div>""", unsafe_allow_html=True)
        with st.form("onboarding_form"):
            name = st.text_input("Name", placeholder="Rajesh Kumar")
            c1, c2 = st.columns(2)
            with c1: age = st.number_input("Age", 18, 65, 25)
            with c2: city = st.selectbox("City", ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kolkata"])
            
            platform = st.multiselect("Platforms", ["Swiggy", "Zomato", "Uber", "Ola", "Dunzo"], default=["Swiggy"])
            savings_rate = st.slider("Auto-Save %", 2, 10, 5)
            generate_demo = st.checkbox("Generate demo data", value=True)
            
            if st.form_submit_button("Start Journey 🚀", use_container_width=True):
                if name:
                    user_data = {
                        'name': name, 'age': age, 'city': city,
                        'platform': " + ".join(platform), 'platforms': platform,
                        'savings_rate': savings_rate / 100, 'goals': ["Emergency Fund"], 'language': 'hinglish'
                    }
                    user_id = storage.create_user(user_data)
                    
                    if generate_demo:
                        sim = GigWorkerSimulator(name, city)
                        inc = sim.generate_income_history(90)
                        spd = sim.generate_spending_data(30)
                        for _, r in inc.iterrows(): storage.add_income(user_id, r.to_dict())
                        for _, r in spd.iterrows(): storage.add_expense(user_id, r.to_dict())
                    
                    st.session_state.user_id = user_id
                    st.session_state.onboarding_complete = True
                    st.rerun()

    with col2:
        st.markdown("""<div class="glass-card"><h3>👋 Returning User?</h3></div>""", unsafe_allow_html=True)
        users = storage.list_users()
        if users:
            for u in users:
                if st.button(f"👤 {u['name']}", key=u['user_id'], use_container_width=True):
                    st.session_state.user_id = u['user_id']
                    st.session_state.onboarding_complete = True
                    st.rerun()

def initialize_app():
    user_id = st.session_state.user_id
    profile, income_df, spending_df = storage.get_data_for_agents(user_id)
    orchestrator = get_orchestrator(profile, income_df, spending_df)
    return profile, income_df, spending_df, orchestrator

def show_main_app():
    apply_custom_styles()
    user_id = st.session_state.user_id
    
    if 'orchestrator' not in st.session_state:
        with st.spinner("Initializing..."):
            p, i, s, o = initialize_app()
            st.session_state.profile = p
            st.session_state.income_data = i
            st.session_state.spending_data = s
            st.session_state.orchestrator = o
            st.session_state.daily_report = None
            st.session_state.chat_history = []
            st.rerun()

    profile = st.session_state.profile
    orchestrator = st.session_state.orchestrator
    
    # Sidebar
    with st.sidebar:
        st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={profile['name']}", width=80)
        st.write(f"**{profile['name']}**")
        st.caption(profile.get('city', 'India'))
        
        st.markdown("---")
        
        # --- 1. ADD INCOME ---
        with st.expander("💰 Add Income"):
            with st.form("inc"):
                amt = st.number_input("Amount", 0, 5000, 500)
                if st.form_submit_button("Save"):
                    storage.add_income(user_id, {'date': datetime.now().strftime('%Y-%m-%d'), 'income': amt})
                    s_amt = amt * profile.get('savings_rate', 0.05)
                    if hasattr(storage, 'add_savings'):
                        storage.add_savings(user_id, {'date': datetime.now().strftime('%Y-%m-%d'), 'amount': s_amt, 'source': 'auto'})
                    st.success(f"Saved + ₹{s_amt:.0f}")
                    st.rerun()

        # --- 2. ADD EXPENSE (Restored!) ---
        with st.expander("💸 Add Expense"):
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
        
        st.markdown("---")
        if st.button("🔄 Daily Check", type="primary"):
            st.session_state.daily_report = orchestrator.run_daily_check()
            st.rerun()
            
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    # Main Content
    st.markdown(f"### 🌦️ Dashboard: {profile['name']}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Forecast", "💬 Coach", "📈 Trends", "🎯 Goals", "⚙️ Settings"])
    
    # --- TAB 1: FORECAST ---
    with tab1:
        if st.session_state.daily_report:
            report = st.session_state.daily_report
            dash = report['dashboard']
            
            c1, c2, c3 = st.columns(3)
            with c1: 
                st.markdown(f"""<div class="glass-card metric-container">
                    <div class="metric-label">Health Score</div>
                    <div class="metric-value" style="color: #00B894">{dash['summary']['financial_health_score']}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="glass-card metric-container">
                    <div class="metric-label">Weekly Forecast</div>
                    <div class="metric-value">₹{dash['summary']['weekly_income_forecast']:,.0f}</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="glass-card metric-container">
                    <div class="metric-label">Savings Rate</div>
                    <div class="metric-value">{dash['summary']['savings_rate']:.1f}%</div>
                </div>""", unsafe_allow_html=True)
            
            col_m, col_s = st.columns([2, 1])
            with col_m:
                st.subheader("Income Weather")
                preds = report['forecast']['predictions']['predictions']
                df_p = pd.DataFrame(preds)
                fig = px.bar(df_p, x='day_name', y='predicted_income', title="7-Day Forecast")
                st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
                st.info(f"💡 **Coach says:** {report['coaching']}")
            
            with col_s:
                st.subheader("Alerts")
                if report['interventions']:
                    for alert in report['interventions']:
                        color = "alert-high" if alert['severity'] == "HIGH" else "alert-low"
                        st.markdown(f"""<div class="alert-box {color}">
                            <div><b>{alert['category']}</b><br>{alert['message']}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.success("✅ No urgent risks detected!")
    # TAB 2: AI COACH
    with tab2:
        st.markdown("### 💬 Chat with StormGuard")
        
        # Chat container style
        st.markdown("""
        <style>
            .stChatMessage {
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                margin-bottom: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

        for chat in st.session_state.get('chat_history', []):
            with st.chat_message("user", avatar="👤"):
                st.markdown(chat['question'])
            with st.chat_message("assistant", avatar="🌦️"):
                st.markdown(chat['answer'])
        
        user_q = st.chat_input("Ask about savings, shifts, or spending...")
        if user_q:
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_q)
            with st.chat_message("assistant", avatar="🌦️"):
                with st.spinner("Thinking..."):
                    try:
                        response = orchestrator.chat(user_q)
                        st.markdown(response)
                        st.session_state.chat_history.append({'question': user_q, 'answer': response})
                    except Exception as e:
                        st.error(f"Agent error: {e}")

    # --- TAB 3: TRENDS ---
    with tab3:
        df = storage.get_income_history(user_id, 90)
        if not df.empty:
            fig = px.area(df, x='date', y='income', title="Income Trend")
            st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
        else:
            st.warning("No data yet.")

    # --- TAB 4: GOALS ---
    with tab4:
        c_head, c_btn = st.columns([3, 1])
        with c_head: st.markdown("### 🎯 Your Targets")
        with c_btn: 
            if st.button("➕ New Goal"): st.session_state.add_goal = True
            
        if st.session_state.get('add_goal'):
            with st.form("new_goal"):
                st.markdown("#### Create New Goal")
                g_name = st.text_input("Goal Name")
                g_target = st.number_input("Target Amount (₹)", 1000, 1000000, 10000)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("💾 Save"):
                        goals = storage.get_goals(user_id)
                        goals.append({
                            'description': g_name, 
                            'target_amount': g_target, 
                            'status': 'active',
                            'created_at': datetime.now().isoformat()
                        })
                        storage.set_goals(user_id, goals)
                        st.session_state.add_goal = False
                        st.rerun()
                with c2:
                    if st.form_submit_button("Cancel"):
                        st.session_state.add_goal = False
                        st.rerun()
            st.markdown("---")

        goals = storage.get_goals(user_id)
        total_savings = storage.get_total_savings(user_id)
        
        # --- NEW LOGIC: Initialize remaining savings bucket ---
        remaining_savings = total_savings 
        # ------------------------------------------------------

        if not goals:
            st.info("No goals set yet.")
        else:
            cols = st.columns(3)
            for i, goal in enumerate(goals):
                with cols[i % 3]:
                    # 1. Normalize data
                    if isinstance(goal, str): 
                        display_goal = {'description': goal, 'target_amount': 0}
                    else:
                        display_goal = goal
                    
                    target = display_goal.get('target_amount', 0)
                    
                    # 2. WATERFALL LOGIC FIX
                    # Allocate money to this goal, but don't exceed the target
                    if target > 0:
                        allocated = min(remaining_savings, target)
                        remaining_savings -= allocated # Remove used money from bucket
                        remaining_savings = max(0, remaining_savings) # Safety check
                    else:
                        allocated = 0
                    
                    current = allocated
                    # ----------------------
                    
                    # 3. Ring Calculations
                    pct = min(current / target, 1.0) * 100 if target > 0 else 0
                    
                    radius = 50
                    circumference = 314
                    offset = circumference - (pct / 100) * circumference
                    color = "#00B894" if pct >= 100 else "#6C5CE7"
                    
                    # 4. Render Card
                    html_content = f"""
<div class="glass-card" style="text-align: center; position: relative;">
<h4 style="margin: 0 0 10px 0; color: #636E72; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
    {display_goal.get('description', 'Goal')}
</h4>

<div style="display: flex; justify-content: center; margin-bottom: 10px;">
<svg width="120" height="120" style="transform: rotate(-90deg);">
    <circle cx="60" cy="60" r="{radius}" fill="none" stroke="#eee" stroke-width="8" />
    <circle cx="60" cy="60" r="{radius}" fill="none" stroke="{color}" stroke-width="8"
            stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" stroke-linecap="round" 
            style="--target-offset: {offset}; animation: fillCircle 1.5s ease-out forwards;"/>
</svg>
<div style="position: absolute; top: 38px; width: 100%; text-align: center;">
    <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{int(pct)}%</div>
</div>
</div>

<div style="font-size: 0.85rem; color: #aaa;">
    ₹{current:,.0f} of <strong style="color: #2D3436;">₹{target:,.0f}</strong>
</div>
</div>
"""
                    st.markdown(html_content, unsafe_allow_html=True)
                    
                    if target == 0:
                        st.warning("⚠️ Target not set")
                    
                    with st.expander("✏️ Edit"):
                        new_t = st.number_input("Target", value=int(target) if target > 0 else 5000, key=f"g_target_{i}")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Update", key=f"g_update_{i}"):
                                if isinstance(goals[i], str):
                                    goals[i] = {'description': goals[i], 'created_at': datetime.now().isoformat()}
                                goals[i]['target_amount'] = new_t
                                storage.set_goals(user_id, goals)
                                st.rerun()
                        with c2:
                            if st.button("Delete", key=f"g_delete_{i}"):
                                goals.pop(i)
                                storage.set_goals(user_id, goals)
                                st.rerun()

    # --- TAB 5: SETTINGS ---
    with tab5:
        st.subheader("Settings")
        
        col1, col2 = st.columns(2, gap="large")
        
        # 1. AUTO-SAVE SETTINGS
        with col1:
            st.markdown('<div class="glass-card"><h4>💰 Auto-Save</h4></div>', unsafe_allow_html=True)
            cur = int(profile.get('savings_rate', 0.05) * 100)
            
            new_r = st.slider("Rate (%)", 1, 20, cur, key="settings_savings_rate")
            
            if st.button("Update Rate", key="btn_update_rate"):
                storage.update_user(user_id, {'savings_rate': new_r/100})
                st.session_state.profile['savings_rate'] = new_r/100
                if hasattr(orchestrator, 'savings_agent'):
                    orchestrator.savings_agent.savings_rate = new_r/100
                st.success("Updated!")
                st.rerun()

        # 2. PROFILE READ-ONLY
        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <h4>👤 Profile</h4>
                <p><b>Name:</b> {profile['name']}</p>
                <p><b>City:</b> {profile.get('city', 'N/A')}</p>
                <p><b>Platform:</b> {profile.get('platform', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # 3. NEW SAVINGS ACTIVITY GRAPH
        st.markdown("### 📊 Savings Activity (Last 30 Days)")
        
        # Fetch data
        savings_history = storage.get_savings_history(user_id, 30)
        
        if not savings_history.empty:
            # Group by date to handle multiple savings in one day
            daily_savings = savings_history.groupby('date')['amount'].sum().reset_index()
            
            fig = px.bar(
                daily_savings, 
                x='date', 
                y='amount', 
                title='',
                labels={'date': 'Date', 'amount': 'Saved (₹)'}
            )
            # Use specific pastel purple color for savings bars
            fig.update_traces(marker_color='#AA96DA')
            st.plotly_chart(apply_pastel_theme(fig), use_container_width=True)
        else:
            st.info("No savings history yet. Start working to see your progress!")

def main():
    if 'onboarding_complete' not in st.session_state:
        show_onboarding()
    else:
        show_main_app()

if __name__ == "__main__":
    main()