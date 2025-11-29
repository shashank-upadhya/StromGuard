# # agents/financial_coach_agent.py
# from phi.agent import Agent
# from phi.model.ollama import Ollama
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# class FinancialCoachAgent:
#     """
#     Personalized Financial Coach Agent
#     - Analyzes spending patterns
#     - Provides coaching based on income forecast
#     - Generates proactive warnings
#     - Chat interface for user questions
#     - Adapts to user preferences (learns over time)
#     """
    
#     def __init__(self, user_profile, spending_data):
#         self.profile = user_profile
#         self.spending_data = spending_data
#         self.conversation_history = []
#         self.user_preferences = {
#             'communication_style': 'supportive',  # supportive, direct, detailed
#             'language': user_profile.get('language', 'hinglish'),
#             'prefers_examples': True,
#             'responds_to_encouragement': True
#         }
        
#         # Initialize Phidata Agent with Ollama
#         self.agent = Agent(
#             name="Financial Coach Agent",
#             model=Ollama(id="llama3:8b"),
#             instructions=[
#                 f"You are a caring, empathetic financial coach for {user_profile['name']}.",
#                 f"They work as a delivery partner in {user_profile['city']} (Swiggy/Zomato).",
#                 "They earn variable income - some weeks good, some weeks bad.",
#                 "Speak in Hinglish (Hindi-English mix) - natural and conversational.",
#                 "Be encouraging and supportive, NEVER judgmental or preachy.",
#                 "Give specific, actionable advice with exact numbers and timelines.",
#                 "Use examples: 'Skip 2 Zomato orders = save ₹400'",
#                 "Keep responses under 150 words unless asked for details.",
#                 "Use emojis sparingly for friendliness: 👍 ✅ 💪 🎯",
#                 f"User's goals: {', '.join(user_profile.get('goals', ['Save money']))}",
#                 "Understand their stress - gig work is hard, income is unpredictable.",
#                 "Focus on what they CAN control, not what they can't."
#             ],
#             markdown=True,
#             show_tool_calls=False,
#             debug_mode=False
#         )
        
#         print(f"✅ Financial Coach Agent initialized for {user_profile['name']}")
    
#     def analyze_spending_patterns(self):
#         """
#         Analyze spending data to identify patterns and issues
#         """
#         print("💸 Analyzing spending patterns...")
        
#         df = self.spending_data.copy()
#         df['date'] = pd.to_datetime(df['date'])
        
#         # Basic stats
#         total_spent = df['amount'].sum()
#         daily_avg = total_spent / 30
        
#         # Category breakdown
#         by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
#         # Spending velocity (last 7 days vs previous 7 days)
#         recent_7d = df.tail(7)['amount'].sum()
#         previous_7d = df.iloc[-14:-7]['amount'].sum()
#         velocity_change = ((recent_7d - previous_7d) / previous_7d) * 100 if previous_7d > 0 else 0
        
#         # Identify wasteful spending
#         discretionary = df[df['category'].isin(['entertainment', 'shopping'])]['amount'].sum()
#         discretionary_pct = (discretionary / total_spent) * 100 if total_spent > 0 else 0
        
#         # Find largest single expense
#         largest = df.nlargest(1, 'amount').iloc[0]
        
#         # Weekend spending pattern
#         df['is_weekend'] = df['date'].dt.dayofweek >= 5
#         weekend_avg = df[df['is_weekend']]['amount'].mean()
#         weekday_avg = df[~df['is_weekend']]['amount'].mean()
#         weekend_spike = ((weekend_avg - weekday_avg) / weekday_avg) * 100 if weekday_avg > 0 else 0
        
#         patterns = {
#             'total_spent': round(total_spent, 2),
#             'daily_average': round(daily_avg, 2),
#             'by_category': by_category.to_dict(),
#             'top_category': by_category.index[0] if len(by_category) > 0 else 'Unknown',
#             'discretionary_spending': round(discretionary, 2),
#             'discretionary_percent': round(discretionary_pct, 1),
#             'spending_velocity': {
#                 'recent_7d': round(recent_7d, 2),
#                 'previous_7d': round(previous_7d, 2),
#                 'change_percent': round(velocity_change, 1),
#                 'trend': 'increasing' if velocity_change > 10 else 'decreasing' if velocity_change < -10 else 'stable'
#             },
#             'largest_expense': {
#                 'amount': round(largest['amount'], 2),
#                 'category': largest['category'],
#                 'description': largest['description']
#             },
#             'weekend_pattern': {
#                 'weekend_avg': round(weekend_avg, 2),
#                 'weekday_avg': round(weekday_avg, 2),
#                 'spike_percent': round(weekend_spike, 1),
#                 'significant': weekend_spike > 30
#             }
#         }
        
#         return patterns
    
#     def coach_on_forecast(self, forecast_data):
#         """
#         Provide coaching based on income forecast from Weather Agent
#         """
#         print("💬 Generating coaching advice...")
        
#         predictions = forecast_data['predictions']
#         risks = forecast_data.get('risks', [])
#         patterns = forecast_data.get('patterns', {})
        
#         # Build context for AI
#         context = f"""
# You're coaching {self.profile['name']} on their income forecast.

# INCOME FORECAST (Next 7 Days):
# - Total Expected: ₹{predictions['weekly_total']}
# - Daily Average: ₹{predictions['daily_avg']}
# - Confidence: 85%

# RISKS DETECTED:
# {len(risks)} risk(s) - {"HIGH severity detected!" if any(r['severity'] == 'HIGH' for r in risks) else "Manageable"}

# INCOME PATTERNS:
# - Best Days: {list(patterns.get('best_days', {}).keys())[:2] if patterns.get('best_days') else 'N/A'}
# - Efficiency: {patterns.get('efficiency_trend', {}).get('current_per_hour', 'N/A')} per hour

# Provide coaching in Hinglish:
# 1. Is next week good or challenging? (1 sentence)
# 2. Top 2 specific actions with numbers (bullet points)
# 3. Brief encouragement (1 sentence)

# Keep under 120 words. Be conversational and motivating.
# """
        
#         response = self.agent.run(context)
#         return response.content
    
#     def analyze_spending_vs_income(self, forecast_data, spending_patterns):
#         """
#         Compare spending vs predicted income
#         """
#         print("📊 Comparing spending vs income...")
        
#         weekly_income = forecast_data['predictions']['weekly_total']
#         weekly_spending = spending_patterns['daily_average'] * 7
        
#         surplus_deficit = weekly_income - weekly_spending
#         savings_rate = (surplus_deficit / weekly_income) * 100 if weekly_income > 0 else 0
        
#         context = f"""
# Analyze spending vs income for {self.profile['name']}:

# INCOME (Next Week):
# - Forecast: ₹{weekly_income}

# SPENDING (Current Pattern):
# - Average weekly: ₹{weekly_spending:.0f}
# - Top category: {spending_patterns['top_category']} (₹{spending_patterns['by_category'].get(spending_patterns['top_category'], 0):.0f}/month)
# - Discretionary: ₹{spending_patterns['discretionary_spending']} ({spending_patterns['discretionary_percent']}%)

# ANALYSIS:
# - Net: {'Surplus ₹' + str(round(surplus_deficit, 0)) if surplus_deficit > 0 else 'Deficit ₹' + str(abs(round(surplus_deficit, 0)))}
# - Savings Rate: {savings_rate:.1f}%

# Provide in Hinglish:
# 1. Quick assessment (1 sentence)
# 2. Suggest 2 easy ways to save ₹500-1000
# 3. Be specific: "Skip X = save ₹Y"

# Under 100 words. Practical, not preachy.
# """
        
#         response = self.agent.run(context)
#         return response.content
    
#     def generate_proactive_warning(self, warning_type, context_data):
#         """
#         Generate proactive warnings before problems occur
#         """
#         print(f"⚠️  Generating {warning_type} warning...")
        
#         prompts = {
#             'slow_week_ahead': f"""
# ⚠️ ALERT: Income dropping next week!

# Context: {context_data}

# Warn {self.profile['name']} proactively (in Hinglish):
# 1. What's happening (be clear, not scary)
# 2. What to do THIS week to prepare (specific actions)
# 3. How to adjust spending starting now
# 4. One income-boosting tip

# Make them feel in control. Under 130 words.
# """,
            
#             'overspending_detected': f"""
# Pattern Alert: Spending increased significantly!

# Context: {context_data}

# Gently point out to {self.profile['name']} (in Hinglish):
# 1. The pattern you noticed (use data)
# 2. Why it's risky for variable income workers
# 3. One simple strategy to avoid this
# 4. Encourage them - they can fix this

# Be supportive, not judgmental. Under 100 words.
# """,
            
#             'weekend_overspending': f"""
# Weekend Spending Pattern Detected!

# Context: {context_data}

# Explain to {self.profile['name']} (in Hinglish):
# 1. Weekend spending is {context_data.get('spike_percent', 'significantly')}% higher
# 2. Why this matters for variable income
# 3. One practical fix (not "don't enjoy weekends")
# 4. Small win they can achieve

# Keep it light and actionable. Under 100 words.
# """,
            
#             'goal_off_track': f"""
# Goal Progress Check!

# Context: {context_data}

# Update {self.profile['name']} (in Hinglish):
# 1. Current progress vs goal
# 2. What went off track (no blame)
# 3. Specific adjustment needed (with numbers)
# 4. Encouragement - it's still achievable

# Motivating tone. Under 120 words.
# """,
            
#             'festival_prep': f"""
# Festival Coming Soon! 🎉

# Context: {context_data}

# Help {self.profile['name']} prepare (in Hinglish):
# 1. Festival expenses estimate
# 2. How much to save weekly
# 3. Festival income boost opportunities
# 4. Start saving now - specific amount

# Excited but financially smart. Under 120 words.
# """,
#         }
        
#         prompt = prompts.get(warning_type, "Provide general financial advice.")
#         response = self.agent.run(prompt)
#         return response.content
    
#     def chat(self, user_message, context=None):
#         """
#         Chat interface - user can ask questions
#         """
#         print(f"💬 User asked: '{user_message[:50]}...'")
        
#         # Build comprehensive context
#         full_context = f"""
# User Question: "{user_message}"

# About {self.profile['name']}:
# - City: {self.profile['city']}
# - Work: {self.profile.get('platform', 'Delivery partner')}
# - Goals: {self.profile.get('goals', ['Financial stability'])}

# """
        
#         if context:
#             full_context += f"""
# Current Situation:
# {context}
# """
        
#         full_context += """
# Provide helpful, personalized response in Hinglish.
# Be conversational, specific, and encouraging.
# Under 150 words.
# """
        
#         response = self.agent.run(full_context)
        
#         # Store conversation
#         self.conversation_history.append({
#             'timestamp': datetime.now().isoformat(),
#             'user_message': user_message,
#             'agent_response': response.content
#         })
        
#         return response.content
    
#     def celebrate_win(self, achievement_data):
#         """
#         Celebrate user achievements
#         """
#         print("🎉 Celebrating achievement...")
        
#         context = f"""
# {self.profile['name']} achieved something! Celebrate it! 🎉

# Achievement: {achievement_data}

# In Hinglish:
# 1. Celebrate specifically (mention the numbers)
# 2. Acknowledge their effort and consistency
# 3. Show impact of this win
# 4. Encourage them to keep going

# Be genuinely excited for them! Under 100 words.
# """
        
#         response = self.agent.run(context)
#         return response.content
    
#     def generate_savings_recommendation(self, forecast_data, spending_patterns):
#         """
#         Generate smart savings recommendation
#         """
#         print("💰 Generating savings strategy...")
        
#         weekly_income = forecast_data['predictions']['weekly_total']
#         weekly_spending = spending_patterns['daily_average'] * 7
#         potential_savings = weekly_income - weekly_spending
        
#         context = f"""
# Help {self.profile['name']} save money smartly!

# SITUATION:
# - Next week income: ₹{weekly_income}
# - Current spending: ₹{weekly_spending:.0f}/week
# - Potential savings: ₹{potential_savings:.0f}

# SPENDING BREAKDOWN:
# {spending_patterns['by_category']}

# In Hinglish:
# 1. Realistic savings target for next week (specific ₹ amount)
# 2. Where to cut without suffering (2 specific tips)
# 3. Auto-save strategy suggestion
# 4. What they'll achieve in 4 weeks if they follow this

# Practical and motivating. Under 130 words.
# """
        
#         response = self.agent.run(context)
#         return response.content


# # Utility function for testing
# def print_coaching_session(coach_response):
#     """Pretty print coaching response"""
#     print(f"\n{'='*70}")
#     print(f"💬 FINANCIAL COACH")
#     print(f"{'='*70}")
#     print(coach_response)
#     print(f"{'='*70}\n")


# # Test function
# if __name__ == "__main__":
#     print("🧪 Testing Financial Coach Agent\n")
    
#     # Import dependencies
#     from data.simulator import GigWorkerSimulator
#     from agents.weather_forecast_agent import WeatherForecastAgent
    
#     # Generate test data
#     print("📊 Generating test data...")
#     simulator = GigWorkerSimulator("Rajesh", "Bangalore")
#     income_data = simulator.generate_income_history(90)
#     spending_data = simulator.generate_spending_data(30)
    
#     user_profile = {
#         'name': 'Rajesh',
#         'city': 'Bangalore',
#         'platform': 'Swiggy + Zomato',
#         'language': 'hinglish',
#         'goals': ['Save ₹20,000 emergency fund', 'Buy bike in 8 months']
#     }
    
#     print("✅ Data generated\n")
    
#     # Get forecast from Weather Agent
#     print("🔮 Getting income forecast...")
#     weather_agent = WeatherForecastAgent(income_data)
#     forecast = weather_agent.generate_complete_forecast(7)
#     print("✅ Forecast ready\n")
    
#     # Initialize Coach Agent
#     print("🤖 Initializing Financial Coach...")
#     coach = FinancialCoachAgent(user_profile, spending_data)
#     print()
    
#     # Test 1: Analyze spending
#     print("TEST 1: Spending Pattern Analysis")
#     print("-" * 70)
#     spending_patterns = coach.analyze_spending_patterns()
#     print(f"✅ Total spent: ₹{spending_patterns['total_spent']}")
#     print(f"   Top category: {spending_patterns['top_category']}")
#     print(f"   Discretionary: {spending_patterns['discretionary_percent']}%\n")
    
#     # Test 2: Coach on forecast
#     print("TEST 2: Coaching on Income Forecast")
#     print("-" * 70)
#     coaching = coach.coach_on_forecast(forecast)
#     print_coaching_session(coaching)
    
#     # Test 3: Spending vs income
#     print("TEST 3: Spending vs Income Analysis")
#     print("-" * 70)
#     analysis = coach.analyze_spending_vs_income(forecast, spending_patterns)
#     print_coaching_session(analysis)
    
#     # Test 4: Proactive warning
#     print("TEST 4: Proactive Warning")
#     print("-" * 70)
#     warning = coach.generate_proactive_warning(
#         'overspending_detected',
#         spending_patterns['spending_velocity']
#     )
#     print_coaching_session(warning)
    
#     # Test 5: Chat interface
#     print("TEST 5: Chat Interface")
#     print("-" * 70)
#     questions = [
#         "Should I work this Sunday?",
#         "Can I afford to buy new phone for ₹15,000?",
#         "How do I save for Diwali?"
#     ]
    
#     for q in questions:
#         response = coach.chat(q, context={'weekly_forecast': forecast['predictions']['weekly_total']})
#         print(f"\nQ: {q}")
#         print(f"A: {response[:200]}...\n")
    
#     # Test 6: Celebrate win
#     print("TEST 6: Celebrate Achievement")
#     print("-" * 70)
#     celebration = coach.celebrate_win({
#         'achievement': 'Saved ₹5,000 in emergency fund',
#         'time_taken': '6 weeks',
#         'consistency': '6/6 weeks contributed'
#     })
#     print_coaching_session(celebration)
    
#     print("✅ Financial Coach Agent test complete!")


# agents/financial_coach_agent.py (ENHANCED VERSION)
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools import tool
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()

# os.environ["GOOGLE_API_KEY"] = "AIzaSyBKD2IslrgfUhBBHCpW1Uu4ZYV0EEWMwVY"
os.getenv("GOOGLE_API_KEY")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our storage system
from data.storage import UserStorage

# Initialize storage
storage = UserStorage()


# ==================== PHI TOOLS FOR TRANSACTION TRACKING ====================

@tool
def add_transaction_tool(
    user_id: str,
    amount: float,
    category: str,
    kind: str = "expense",
    date: str = None,
    description: str = None,
) -> str:
    """
    Add a financial transaction to user's log.
    
    Args:
        user_id: User identifier
        amount: Positive number (e.g., 150 for ₹150)
        category: food, fuel, rent, phone, entertainment, family_support, medical, shopping, other
        kind: "income" or "expense"
        date: YYYY-MM-DD format (defaults to today)
        description: Optional note about transaction
    
    Returns:
        Confirmation message with transaction details
    """
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if kind.lower() in ["income", "credit", "earning", "earnings"]:
            # Record income
            result = storage.add_income(user_id, {
                'date': date,
                'income': amount,
                'hours_worked': 8,  # Default, can be updated
                'orders_completed': 0,
                'platform': 'Manual Entry',
                'efficiency': 0,
                'weather': 'clear',
                'is_festival': False,
                'is_weekend': datetime.fromisoformat(date).weekday() >= 5
            })
            return f"✅ Income recorded: ₹{amount} on {date}"
        else:
            # Record expense
            result = storage.add_expense(user_id, {
                'date': date,
                'amount': amount,
                'category': category,
                'description': description or category
            })
            return f"✅ Expense recorded: ₹{amount} for {category} on {date}"
    
    except Exception as e:
        return f"❌ Error adding transaction: {str(e)}"


@tool
def get_spending_summary_tool(user_id: str, days: int = 30) -> str:
    """
    Get comprehensive spending summary for a user.
    
    Args:
        user_id: User identifier
        days: Number of days to analyze (default 30)
    
    Returns:
        JSON string with income, expenses, savings rate, and category breakdown
    """
    try:
        # Get income summary
        income_summary = storage.get_income_summary(user_id, days)
        
        # Get spending summary
        spending_df = storage.get_spending_history(user_id, days)
        
        if spending_df.empty:
            return json.dumps({
                "period_days": days,
                "total_income": income_summary['total_income'],
                "total_expense": 0,
                "net_savings": income_summary['total_income'],
                "saving_rate": 100.0,
                "by_category": {},
                "message": "No expenses recorded yet."
            })
        
        # Calculate totals
        total_expense = spending_df['amount'].sum()
        by_category = spending_df.groupby('category')['amount'].sum().to_dict()
        
        net_savings = income_summary['total_income'] - total_expense
        saving_rate = (net_savings / income_summary['total_income'] * 100) if income_summary['total_income'] > 0 else 0
        
        summary = {
            "period_days": days,
            "total_income": round(income_summary['total_income'], 2),
            "total_expense": round(total_expense, 2),
            "net_savings": round(net_savings, 2),
            "saving_rate": round(saving_rate, 2),
            "by_category": {k: round(v, 2) for k, v in by_category.items()},
            "days_worked": income_summary['days_worked'],
            "avg_daily_income": round(income_summary['avg_daily'], 2),
            "avg_daily_expense": round(total_expense / days, 2)
        }
        
        return json.dumps(summary, indent=2)
    
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_spending_warnings_tool(user_id: str, days: int = 30) -> str:
    """
    Analyze spending patterns and generate warnings with actionable advice.
    
    Args:
        user_id: User identifier
        days: Analysis period in days
    
    Returns:
        JSON with warnings, advice, and detailed analysis
    """
    try:
        summary_str = get_spending_summary_tool.entrypoint(user_id, days)
        summary = json.loads(summary_str)
        
        warnings = []
        advice = []
        
        income = summary['total_income']
        expense = summary['total_expense']
        saving_rate = summary['saving_rate']
        by_cat = summary['by_category']
        
        # Warning 1: Spending exceeds income
        if income == 0 and expense > 0:
            warnings.append("⚠️ You have expenses but no recorded income this period.")
            advice.append("Start logging your daily earnings to track your financial health.")
        elif expense > income:
            deficit = expense - income
            warnings.append(f"🔴 CRITICAL: Spending ₹{deficit:.0f} more than earning!")
            advice.append(f"Cut expenses by at least ₹{deficit/30:.0f}/day to balance your budget.")
        
        # Warning 2: Low savings rate
        if income > 0 and saving_rate < 10:
            warnings.append(f"💰 Low saving rate: Only {saving_rate:.1f}% saved")
            advice.append("Target: Save at least 15-20% of income. Start with ₹50/day challenge!")
        elif income > 0 and saving_rate < 0:
            warnings.append("🔴 DEFICIT: You're not saving, you're losing money!")
            advice.append("Emergency action needed: Identify top 3 expenses to cut immediately.")
        
        # Warning 3: Category overspending
        if expense > 0:
            for cat, amt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
                share = amt / expense * 100
                
                if cat == 'food' and share > 40:
                    warnings.append(f"🍽️ Food spending is {share:.1f}% of expenses (₹{amt:.0f})")
                    advice.append("Cook at home 3 days/week = Save ₹1,500/month. Pack lunch instead of ordering.")
                
                elif cat == 'entertainment' and share > 20:
                    warnings.append(f"🎮 Entertainment: {share:.1f}% (₹{amt:.0f})")
                    advice.append("Reduce to ₹500/month. Free alternatives: YouTube, local parks, meetups.")
                
                elif cat == 'fuel' and amt > (income * 0.3):
                    warnings.append(f"⛽ High fuel costs: ₹{amt:.0f} ({share:.1f}%)")
                    advice.append("Optimize routes, maintain vehicle, consider CNG conversion.")
        
        # Warning 4: Gig worker specific - Income volatility
        if summary.get('days_worked', 0) < (days * 0.7):
            warnings.append(f"📉 Low activity: Only {summary.get('days_worked', 0)} working days")
            advice.append("Aim for 25+ days/month. Check platform incentives and surge times.")
        
        # Positive reinforcement
        if not warnings:
            advice.append("✅ Great job! Your spending is under control. Keep it up! 💪")
        
        result = {
            "period_days": days,
            "warnings": warnings,
            "advice": advice,
            "summary": summary,
            "urgency_level": "HIGH" if expense > income else "MEDIUM" if saving_rate < 10 else "LOW"
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def list_recent_transactions_tool(user_id: str, days: int = 7, kind: str = None) -> str:
    """
    List recent transactions for a user.
    
    Args:
        user_id: User identifier
        days: Number of days to look back
        kind: Filter by "income" or "expense" (None for all)
    
    Returns:
        JSON list of transactions
    """
    try:
        if kind == "income" or kind is None:
            income_df = storage.get_income_history(user_id, days)
            income_txs = []
            if not income_df.empty:
                for _, row in income_df.iterrows():
                    income_txs.append({
                        'date': row['date'].strftime('%Y-%m-%d'),
                        'amount': row['income'],
                        'kind': 'income',
                        'category': 'earnings',
                        'platform': row.get('platform', 'N/A')
                    })
        else:
            income_txs = []
        
        if kind == "expense" or kind is None:
            expense_df = storage.get_spending_history(user_id, days)
            expense_txs = []
            if not expense_df.empty:
                for _, row in expense_df.iterrows():
                    expense_txs.append({
                        'date': row['date'].strftime('%Y-%m-%d'),
                        'amount': row['amount'],
                        'kind': 'expense',
                        'category': row['category'],
                        'description': row.get('description', '')
                    })
        else:
            expense_txs = []
        
        all_txs = income_txs + expense_txs
        all_txs.sort(key=lambda x: x['date'], reverse=True)
        
        return json.dumps(all_txs[:20], indent=2)  # Limit to 20 most recent
    
    except Exception as e:
        return json.dumps({"error": str(e)})


# ==================== ENHANCED FINANCIAL COACH AGENT ====================

class FinancialCoachAgent:
    """
    Enhanced Personalized Financial Coach Agent
    - Integrates transaction tracking
    - Analyzes spending patterns with tools
    - Provides coaching based on income forecast
    - Generates proactive warnings
    - Chat interface for user questions
    - Adapts to user preferences (learns over time)
    """
    
    def __init__(self, user_profile, spending_data):
        self.profile = user_profile
        self.user_id = user_profile.get('user_id', 'user_001')
        self.spending_data = spending_data
        self.conversation_history = []
        self.user_preferences = {
            'communication_style': 'supportive',
            'language': user_profile.get('language', 'hinglish'),
            'prefers_examples': True,
            'responds_to_encouragement': True
        }
        
        # Initialize Phidata Agent with Ollama + Tools
        self.agent = Agent(
            name="Financial Coach Agent",
            model=Gemini(id="gemini-2.0-flash"),
            tools=[
                add_transaction_tool,
                get_spending_summary_tool,
                get_spending_warnings_tool,
                list_recent_transactions_tool
            ],
            instructions=[
                f"You are a caring, empathetic financial coach for {user_profile['name']}.",
                f"They work as a delivery partner in {user_profile['city']} (Swiggy/Zomato).",
                "They earn variable income - some weeks good, some weeks bad.",
                "Speak in Hinglish (Hindi-English mix) - natural and conversational.",
                "Be encouraging and supportive, NEVER judgmental or preachy.",
                "Give specific, actionable advice with exact numbers and timelines.",
                "Use examples: 'Skip 2 Zomato orders = save ₹400'",
                "Keep responses under 150 words unless asked for details.",
                "Use emojis sparingly for friendliness: 👍 ✅ 💪 🎯",
                f"User's goals: {', '.join(user_profile.get('goals', ['Save money']))}",
                "Understand their stress - gig work is hard, income is unpredictable.",
                "Focus on what they CAN control, not what they can't.",
                f"IMPORTANT: The user_id is '{user_profile.get('user_id')}' - use this when calling tools.",
                "When user mentions spending money, ALWAYS use add_transaction_tool to log it.",
                "When user asks about spending habits, use get_spending_summary_tool.",
                "When giving financial advice, use get_spending_warnings_tool for data-driven insights."
            ],
            markdown=True,
            show_tool_calls=True,
            debug_mode=False
        )
        
        print(f"✅ Enhanced Financial Coach Agent initialized for {user_profile['name']}")
    
    def analyze_spending_patterns(self, current_monthly_income=0):
        """
        Analyze spending data to identify patterns and issues
        Uses both DataFrame analysis and tool-based analysis
        """
        print("💸 Analyzing spending patterns...")
        
        # Use tool for comprehensive analysis
        summary_json = get_spending_summary_tool.entrypoint(self.user_id, days=30)
        summary = json.loads(summary_json)
        
        # --- ERROR HANDLING FIX START ---
        # If the tool returned an error, print it and use a safe default
        if "error" in summary:
            print(f"❌ Error in spending summary tool: {summary['error']}")
            # Create a safe 'empty' summary to prevent the KeyError crash
            summary = {
                'total_expense': 0,
                'avg_daily_expense': 0,
                'by_category': {},
                'total_income': 0,
                'saving_rate': 0
            }
        # --- ERROR HANDLING FIX END ---
        
        # Also do traditional DataFrame analysis for compatibility
        df = self.spending_data.copy()
        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
            # Spending velocity
            recent_7d = df.tail(7)['amount'].sum()
            previous_7d = df.iloc[-14:-7]['amount'].sum() if len(df) >= 14 else recent_7d
            velocity_change = ((recent_7d - previous_7d) / previous_7d) * 100 if previous_7d > 0 else 0
            
            # Weekend pattern
            df['is_weekend'] = df['date'].dt.dayofweek >= 5
            weekend_avg = df[df['is_weekend']]['amount'].mean()
            weekday_avg = df[~df['is_weekend']]['amount'].mean()
            weekend_spike = ((weekend_avg - weekday_avg) / weekday_avg) * 100 if weekday_avg > 0 else 0
            fuel_spend = df[df['category'] == 'fuel']['amount'].sum()
        fuel_risk = {}
        
        if current_monthly_income > 0:
            fuel_ratio = (fuel_spend / current_monthly_income) * 100
            # If fuel is >25% of income, it indicates inefficiency (poor routing/maintenance)
            if fuel_ratio > 25:
                fuel_risk = {
                    'detected': True,
                    'spend': round(fuel_spend, 2),
                    'ratio': round(fuel_ratio, 1),
                    'message': "High fuel spend detected. Check vehicle maintenance or route efficiency."
                }
            else:
                fuel_risk = {'detected': False, 'ratio': round(fuel_ratio, 1)}
            patterns = {
                'total_spent': summary.get('total_expense', 0), # Use .get() for safety
                'daily_average': summary.get('avg_daily_expense', 0),
                'by_category': summary.get('by_category', {}),
                'top_category': max(summary.get('by_category', {}), key=summary.get('by_category', {}).get) if summary.get('by_category') else 'None',
                'discretionary_spending': sum(v for k, v in summary.get('by_category', {}).items() if k in ['entertainment', 'shopping']),
                'discretionary_percent': 0,
                'spending_velocity': {
                    'recent_7d': round(recent_7d, 2),
                    'previous_7d': round(previous_7d, 2),
                    'change_percent': round(velocity_change, 1),
                    'trend': 'increasing' if velocity_change > 10 else 'decreasing' if velocity_change < -10 else 'stable'
                },
                'fuel_efficiency': fuel_risk,
                'weekend_pattern': {
                    'weekend_avg': round(weekend_avg, 2),
                    'weekday_avg': round(weekday_avg, 2),
                    'spike_percent': round(weekend_spike, 1),
                    'significant': weekend_spike > 30
                }
            }
            
            if patterns['total_spent'] > 0:
                patterns['discretionary_percent'] = round(
                    (patterns['discretionary_spending'] / patterns['total_spent']) * 100, 1
                )
        else:
            # Return summary from tool (using .get for safety)
            patterns = {
                'total_spent': summary.get('total_expense', 0),
                'daily_average': summary.get('avg_daily_expense', 0),
                'by_category': summary.get('by_category', {}),
                'top_category': max(summary.get('by_category', {}), key=summary.get('by_category', {}).get) if summary.get('by_category') else 'None',
                'discretionary_spending': 0,
                'discretionary_percent': 0,
                'spending_velocity': {
                    'recent_7d': 0,
                    'previous_7d': 0,
                    'change_percent': 0,
                    'trend': 'stable'
                },
                'fuel_efficiency': fuel_risk,
                'weekend_pattern': {
                    'weekend_avg': 0,
                    'weekday_avg': 0,
                    'spike_percent': 0,
                    'significant': False
                }
            }
        
        return patterns
    
    def coach_on_forecast(self, forecast_data):
        """Provide coaching based on income forecast"""
        print("💬 Generating coaching advice...")
        
        predictions = forecast_data['predictions']
        risks = forecast_data.get('risks', [])
        patterns = forecast_data.get('patterns', {})
        
        context = f"""
You're coaching {self.profile['name']} on their income forecast for user_id: {self.user_id}.

INCOME FORECAST (Next 7 Days):
- Total Expected: ₹{predictions['weekly_total']}
- Daily Average: ₹{predictions['daily_avg']}
- Confidence: 85%

RISKS DETECTED:
{len(risks)} risk(s) - {"HIGH severity detected!" if any(r['severity'] == 'HIGH' for r in risks) else "Manageable"}

Provide coaching in Hinglish:
1. Is next week good or challenging? (1 sentence)
2. Top 2 specific actions with numbers (bullet points)
3. Brief encouragement (1 sentence)

Keep under 120 words. Be conversational and motivating.
"""
        
        response = self.agent.run(context)
        return response.content
    
    def analyze_spending_vs_income(self, forecast_data, spending_patterns):
        """Compare spending vs predicted income with tool-based insights"""
        print("📊 Comparing spending vs income...")
        
        # Get tool-based warnings
        warnings_json = get_spending_warnings_tool.entrypoint(self.user_id, days=30)
        warnings_data = json.loads(warnings_json)
        
        weekly_income = forecast_data['predictions']['weekly_total']
        weekly_spending = spending_patterns['daily_average'] * 7
        surplus_deficit = weekly_income - weekly_spending
        
        context = f"""
Analyze spending vs income for {self.profile['name']} (user_id: {self.user_id}):

FORECAST:
- Next week income: ₹{weekly_income}
- Current weekly spending: ₹{weekly_spending:.0f}
- Net: {'Surplus ₹' + str(round(surplus_deficit, 0)) if surplus_deficit > 0 else 'Deficit ₹' + str(abs(round(surplus_deficit, 0)))}

SMART WARNINGS FROM ANALYSIS:
{json.dumps(warnings_data.get('warnings', []), indent=2)}

RECOMMENDED ACTIONS:
{json.dumps(warnings_data.get('advice', []), indent=2)}

Provide in Hinglish (under 100 words):
1. Quick assessment
2. Top 2 actionable tips with specific numbers
"""
        
        response = self.agent.run(context)
        return response.content
    
    def generate_proactive_warning(self, warning_type, context_data):
        """Generate proactive warnings before problems occur"""
        print(f"⚠️ Generating {warning_type} warning...")
        
        prompts = {
            'slow_week_ahead': f"""
⚠️ ALERT: Income dropping next week for user_id: {self.user_id}!

Context: {context_data}

Warn {self.profile['name']} proactively (in Hinglish):
1. What's happening (be clear, not scary)
2. What to do THIS week to prepare (specific actions)
3. How to adjust spending starting now
4. One income-boosting tip

Make them feel in control. Under 130 words.
""",
            'fuel_inefficiency': f"""
🚨 Behavioral Alert: High Fuel Spending!

Context: {context_data}

Warn {self.profile['name']} (in Hinglish):
1. Fuel costs are {context_data.get('ratio')}% of income (High!).
2. This suggests inefficient routing or bike maintenance issues.
3. Suggest checking tire pressure or using route optimization.
4. Calculate potential savings if reduced to 15%.

Be direct but helpful. Under 100 words.
""",
            
            'overspending_detected': f"""
Pattern Alert: Spending increased significantly for user_id: {self.user_id}!

Context: {context_data}

Gently point out to {self.profile['name']} (in Hinglish):
1. The pattern you noticed (use data)
2. Why it's risky for variable income workers
3. One simple strategy to avoid this
4. Encourage them - they can fix this

Be supportive, not judgmental. Under 100 words.
""",
            
            'weekend_overspending': f"""
Weekend Spending Pattern Detected for user_id: {self.user_id}!

Context: {context_data}

Explain to {self.profile['name']} (in Hinglish):
1. Weekend spending is {context_data.get('spike_percent', 'significantly')}% higher
2. Why this matters for variable income
3. One practical fix (not "don't enjoy weekends")
4. Small win they can achieve

Keep it light and actionable. Under 100 words.
""",
        }
        
        prompt = prompts.get(warning_type, "Provide general financial advice.")
        response = self.agent.run(prompt)
        return response.content
    
    def chat(self, user_message, context=None):
        """Enhanced chat interface with transaction tracking"""
        print(f"💬 User asked: '{user_message[:50]}...'")
        
        full_context = f"""
User Question: "{user_message}"
User ID: {self.user_id}

About {self.profile['name']}:
- City: {self.profile['city']}
- Work: {self.profile.get('platform', 'Delivery partner')}
- Goals: {self.profile.get('goals', ['Financial stability'])}

"""
        
        if context:
            full_context += f"Current Situation:\n{context}\n"
        
        full_context += """
If the user mentions any spending or earning, use the appropriate tools to log it.
Provide helpful, personalized response in Hinglish.
Be conversational, specific, and encouraging.
Under 150 words.
"""
        
        response = self.agent.run(full_context)
        
        # Store conversation
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'agent_response': response.content
        })
        
        return response.content
    
    def generate_savings_recommendation(self, forecast_data, spending_patterns):
        """Generate smart savings recommendation using tools"""
        print("💰 Generating savings strategy...")
        
        # Get tool-based analysis
        warnings_json = get_spending_warnings_tool.entrypoint(self.user_id, days=30)
        warnings_data = json.loads(warnings_json)
        
        weekly_income = forecast_data['predictions']['weekly_total']
        
        context = f"""
Help {self.profile['name']} (user_id: {self.user_id}) save money smartly!

SITUATION:
- Next week income: ₹{weekly_income}
- Current spending patterns: {json.dumps(spending_patterns['by_category'], indent=2)}
- AI Analysis: {json.dumps(warnings_data.get('advice', []), indent=2)}

In Hinglish (under 130 words):
1. Realistic savings target for next week (specific ₹ amount)
2. Where to cut based on the analysis (2 specific tips)
3. Auto-save strategy suggestion
4. What they'll achieve in 4 weeks if they follow this
"""
        
        response = self.agent.run(context)
        return response.content


# Test function
if __name__ == "__main__":
    print("🧪 Testing Enhanced Financial Coach Agent\n")
    
    from data.simulator import GigWorkerSimulator
    
    # Generate test data
    print("📊 Generating test data...")
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    spending_data = simulator.generate_spending_data(30)
    
    user_profile = {
        'user_id': 'test_user_enhanced',
        'name': 'Rajesh',
        'city': 'Bangalore',
        'platform': 'Swiggy + Zomato',
        'language': 'hinglish',
        'goals': ['Save ₹20,000 emergency fund']
    }
    
    # Create user in storage
    if not storage.user_exists(user_profile['user_id']):
        storage.create_user(user_profile)
    
    print("✅ Data generated\n")
    
    # Initialize Coach Agent
    print("🤖 Initializing Enhanced Financial Coach...")
    coach = FinancialCoachAgent(user_profile, spending_data)
    print()
    
    # Test transaction logging
    print("TEST 1: Transaction Logging (Via Agent)")
    print("-" * 70)
    
    # instead of calling add_transaction_tool(...) directly:
    print("User: I spent 150 on lunch at a restaurant")
    response1 = coach.chat("I spent 150 on lunch at a restaurant. Log this expense.")
    print(f"Agent: {response1}")
    
    print("\nUser: I earned 600 from daily delivery")
    response2 = coach.chat("I earned 600 rupees from daily delivery today.")
    print(f"Agent: {response2}")
    # print("TEST 1: Transaction Logging")
    # print("-" * 70)
    # result1 = add_transaction_tool(user_profile['user_id'], 150, 'food', 'expense', description='Lunch at restaurant')
    # print(result1)
    
    # result2 = add_transaction_tool(user_profile['user_id'], 600, 'earnings', 'income', description='Daily delivery')
    # print(result2)



    # TEST 2: FIX MANUAL CALL
    print("\nTEST 2: Spending Summary")
    print("-" * 70)
    summary = get_spending_summary_tool.entrypoint(user_profile['user_id'], 30)
    print(summary)
    
    # TEST 3: FIX MANUAL CALL
    print("\nTEST 3: Spending Warnings")
    print("-" * 70)
    warnings = get_spending_warnings_tool.entrypoint(user_profile['user_id'], 30)
    print(warnings)
    
    print("\n✅ Enhanced Financial Coach Agent test complete!")
    

    # # Test spending summary
    # print("\nTEST 2: Spending Summary")
    # print("-" * 70)
    # summary = get_spending_summary_tool(user_profile['user_id'], 30)
    # print(summary)
    
    # # Test spending warnings
    # print("\nTEST 3: Spending Warnings")
    # print("-" * 70)
    # warnings = get_spending_warnings_tool(user_profile['user_id'], 30)
    # print(warnings)
    
    # print("\n✅ Enhanced Financial Coach Agent test complete!")