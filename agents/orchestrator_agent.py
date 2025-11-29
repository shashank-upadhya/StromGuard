# agents/orchestrator_agent.py
from phi.agent import Agent
from phi.model.google import Gemini
import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.weather_forecast_agent import WeatherForecastAgent
from agents.financial_coach_agent import FinancialCoachAgent
from agents.opportunity_scout_agent import OpportunityScoutAgent
from agents.savings_manager_agent import SavingsManagerAgent

class OrchestratorAgent:
    """
    Enhanced Orchestrator with Opportunity Scout + Savings Manager
    """
    
    def __init__(self, user_profile, historical_income, spending_data):
        self.profile = user_profile
        self.user_id = user_profile.get('user_id', 'user_001')
        
        # Initialize sub-agents
        print("🔧 Initializing sub-agents...")
        self.weather_agent = WeatherForecastAgent(historical_income, self.user_id)
        self.coach_agent = FinancialCoachAgent(user_profile, spending_data)

        self.scout_agent = OpportunityScoutAgent(user_profile.get('city', 'Bangalore'))
        
        # NEW: Initialize Savings Manager
        savings_rate = user_profile.get('savings_rate', 0.03)  # Default 3%
        self.savings_agent = SavingsManagerAgent(
            self.user_id, 
            user_profile.get('goals', []),
            savings_rate
        )
        
        # Orchestrator's own AI brain
        self.agent = Agent(
            name="Orchestrator Agent",
            model=Gemini(id="gemini-2.0-flash"),
            instructions=[
                "You are the master coordinator for StormGuard financial assistant.",
                "You manage Weather Forecast Agent and Financial Coach Agent.",
                "Your job: decide WHEN and HOW to intervene in user's financial life.",
                "Prioritize: URGENT risks first, then opportunities, then general advice.",
                "Be smart about timing - don't overwhelm user with too much at once.",
                "Track what advice works - learn and improve.",
                "Keep responses concise and action-oriented."
            ],
            markdown=True,
            show_tool_calls=False,
            debug_mode=False
        )
        
        # Intervention history (for learning)
        self.intervention_history = []
        self.advice_effectiveness = {}
        
        print(f"✅ Orchestrator Agent initialized for {user_profile['name']}")
    
    def run_daily_check(self):
        """
        Enhanced daily check with opportunities and savings
        """
        print("\n" + "="*70)
        print("🌦️  RUNNING ENHANCED DAILY FINANCIAL HEALTH CHECK")
        print("="*70 + "\n")
        
        # Step 1: Get income forecast from Weather Agent
        print("📊 Step 1: Getting income forecast...")
        forecast_report = self.weather_agent.generate_complete_forecast(7)
        print(f"   ✅ Weekly forecast: ₹{forecast_report['predictions']['weekly_total']:.0f}")
        monthly_income_est = forecast_report['predictions']['weekly_total'] * 4

        # Step 2: Analyze spending patterns
        print("\n💸 Step 2: Analyzing spending...")
        spending_patterns = self.coach_agent.analyze_spending_patterns()
        print(f"   ✅ Monthly spending: ₹{spending_patterns['total_spent']:.0f}")
        
        # Step 3: Get personalized coaching
        print("\n💬 Step 3: Generating coaching advice...")
        coaching_advice = self.coach_agent.coach_on_forecast(forecast_report)
        print(f"   ✅ Coaching generated ({len(coaching_advice)} chars)")
        
        # Step 4: Analyze spending vs income
        print("\n📊 Step 4: Comparing spending vs income...")
        spending_analysis = self.coach_agent.analyze_spending_vs_income(
            forecast_report, 
            spending_patterns
        )
        print(f"   ✅ Analysis complete")
        
        # Step 5: Check for intervention needs (CRITICAL)
        print("\n⚠️  Step 5: Checking for intervention needs...")
        interventions = self._check_and_prioritize_interventions(
            forecast_report,
            spending_patterns
        )
        print(f"   ✅ {len(interventions)} intervention(s) needed")
        
        # Step 6: Generate savings recommendation
        print("\n💰 Step 6: Generating savings strategy...")
        savings_plan = self.coach_agent.generate_savings_recommendation(
            forecast_report,
            spending_patterns
        )
        print(f"   ✅ Savings plan ready")

        # NEW Step 7: Scan for opportunities
        print("\n🔍 Step 7: Scanning for earning opportunities...")
        opportunities = self.scout_agent.scan_real_time_opportunities()
        print(f"   ✅ {len(opportunities)} opportunity(ies) found")
        
        # NEW Step 8: Check savings progress
        print("\n💰 Step 8: Checking savings progress...")
        savings_summary = self.savings_agent.get_savings_summary(30)
        print(f"   ✅ Total saved: ₹{savings_summary['total_saved']:.0f}")
        
        # NEW Step 9: Get savings recommendation
        print("\n📊 Step 9: Generating savings recommendation...")
        savings_recommendation = self.savings_agent.smart_savings_recommendation(
            forecast_report,
            spending_patterns
        )
        print(f"   ✅ Recommended rate: {int(savings_recommendation['recommended_rate']*100)}%")
        
        # Step 7: Create dashboard summary
        print("\n📈 Step 7: Creating dashboard...")
        dashboard = self._create_dashboard_summary(
            forecast_report,
            spending_patterns,
            interventions
        )
        print(f"   ✅ Dashboard created\n")
        
        print("="*70)
        print("✅ DAILY CHECK COMPLETE")
        print("="*70 + "\n")
        
        # Return complete report
        return {
            'forecast': forecast_report,
            'spending': spending_patterns,
            'coaching': coaching_advice,
            'spending_analysis': spending_analysis,
            'interventions': interventions,
            'savings_plan': savings_plan,
            'dashboard': dashboard,
            
            # NEW FIELDS
            'opportunities': opportunities,
            'savings_summary': savings_summary,
            'savings_recommendation': savings_recommendation,
            'opportunity_plan': self.scout_agent.generate_daily_opportunity_plan(),
            
            'metadata': {
                'user_id': self.user_id,
                'check_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'agent_versions': {
                    'weather': '1.0',
                    'coach': '1.0',
                    'orchestrator': '1.0',
                    'opportunity_scout': '1.0',  # NEW
                    'savings_manager': '1.0'     # NEW
                }
            }
        }
    
    def process_daily_income(self, date, income_amount, platform="Swiggy"):
        """
        NEW: Process income and auto-save
        """
        return self.savings_agent.process_daily_income(date, income_amount, platform)
    
    def adjust_savings_rate(self, new_rate, reason="User requested"):
        """
        NEW: Allow user to change savings rate
        """
        return self.savings_agent.adjust_savings_rate(new_rate, reason)
    
    def get_quick_opportunities(self):
        """
        NEW: Quick opportunity check (fast)
        """
        return self.scout_agent.scan_real_time_opportunities()
    
    def _check_and_prioritize_interventions(self, forecast_report, spending_patterns):
        """
        Intelligent intervention decision-making
        Prioritizes: URGENT (0) → HIGH (1) → MEDIUM (2) → LOW (3/4)
        """
        interventions = []
        
        # Get risks from Weather Agent
        risks = forecast_report.get('risks', [])
        
        # ==============================================================================
        # NEW: 1. PROACTIVE INTERVENTION: Bridging the Gap (Priority 0 - Highest)
        # ==============================================================================
        crunch_risks = [r for r in risks if r['type'] == 'Cash Crunch Prediction']
        for risk in crunch_risks:
            # Fetch real-time opportunity to bridge the specific gap
            opportunities = self.scout_agent.scan_real_time_opportunities()
            best_opp = opportunities[0] if opportunities else {'zones': ['Central Area'], 'expected_earnings': 'standard rates'}
            
            # Extract zone name cleanly
            zone_name = best_opp.get('zones', ['your area'])[0] if isinstance(best_opp.get('zones'), list) else best_opp.get('zones', 'your area')
            
            # Calculate hours needed (Conservative estimate: ₹100/hr)
            shortfall = risk['shortfall_amount']
            hourly_rate = 100 
            hours_needed = max(2, int(shortfall / hourly_rate))
            
            # Construct the Specific Intervention Message
            message = (
                f"🚨 **Action Required:** Your {risk['bill_name']} is due in {risk['due_date']} days, "
                f"and you are projected to be short by ₹{shortfall:.0f}.\n\n"
                f"⚡ **Solution:** Demand is high in **{zone_name}** tonight. "
                f"Recommend logging in for **{hours_needed} hours** to bridge the gap."
            )
            
            interventions.append({
                'type': 'proactive_intervention',
                'priority': 0, # Top Priority (Critical)
                'severity': 'HIGH',
                'category': 'Cash Crunch Intervention',
                'message': message,
                'action_required': True,
                'timeline': 'Tonight',
                'source': 'orchestrator_ai'
            })

        # ==============================================================================
        # EXISTING: 2. HIGH SEVERITY RISKS (Immediate action needed) (Priority 1)
        # ==============================================================================
        # Filter out 'Cash Crunch Prediction' here since we handled it above specially
        high_risks = [r for r in risks if r['severity'] == 'HIGH' and r['type'] != 'Cash Crunch Prediction']
        for risk in high_risks:
            warning = self.coach_agent.generate_proactive_warning(
                'slow_week_ahead',
                {
                    'forecast': forecast_report['predictions']['weekly_total'],
                    'drop': '30%',
                    'risk_details': risk
                }
            )
            
            interventions.append({
                'type': 'urgent_risk_warning',
                'priority': 1,
                'severity': 'HIGH',
                'category': risk['type'],
                'message': warning,
                'action_required': True,
                'timeline': risk.get('timeline', 'immediate'),
                'source': 'weather_agent'
            })
        
        # ==============================================================================
        # NEW: 3. BEHAVIORAL NUDGING: Fuel Efficiency (Priority 2)
        # ==============================================================================
        fuel_data = spending_patterns.get('fuel_efficiency', {})
        if fuel_data.get('detected'):
            warning = self.coach_agent.generate_proactive_warning(
                'fuel_inefficiency',
                fuel_data
            )
            interventions.append({
                'type': 'behavioral_nudge',
                'priority': 2,
                'severity': 'MEDIUM',
                'category': 'Inefficient Spending',
                'message': warning,
                'action_required': True,
                'timeline': 'This Week',
                'source': 'coach_agent'
            })

        # ==============================================================================
        # EXISTING: 4. OVERSPENDING DETECTION (Behavioral issue) (Priority 2)
        # ==============================================================================
        velocity = spending_patterns.get('spending_velocity', {})
        if velocity.get('trend') == 'increasing' and abs(velocity.get('change_percent', 0)) > 15:
            warning = self.coach_agent.generate_proactive_warning(
                'overspending_detected',
                {
                    'recent_spending': velocity['recent_7d'],
                    'normal_spending': velocity['previous_7d'],
                    'increase': velocity['change_percent']
                }
            )
            
            interventions.append({
                'type': 'spending_alert',
                'priority': 2,
                'severity': 'MEDIUM',
                'category': 'Overspending Pattern',
                'message': warning,
                'action_required': True,
                'timeline': 'this week',
                'source': 'coach_agent'
            })
        
        # ==============================================================================
        # EXISTING: 5. WEEKEND OVERSPENDING PATTERN (Priority 3)
        # ==============================================================================
        if spending_patterns.get('weekend_pattern', {}).get('significant'):
            warning = self.coach_agent.generate_proactive_warning(
                'weekend_overspending',
                spending_patterns['weekend_pattern']
            )
            
            interventions.append({
                'type': 'behavioral_pattern',
                'priority': 3,
                'severity': 'LOW',
                'category': 'Weekend Spending Pattern',
                'message': warning,
                'action_required': False,
                'timeline': 'ongoing',
                'source': 'coach_agent'
            })
        
        # ==============================================================================
        # EXISTING: 6. LOW INCOME WEEK (Without crisis) (Priority 3)
        # ==============================================================================
        predicted_income = forecast_report['predictions']['weekly_total']
        avg_income = forecast_report['patterns']['overall']['avg_daily_income'] * 7
        
        # Only add if we haven't already added high risks
        if predicted_income < avg_income * 0.85 and not high_risks and not crunch_risks:
            interventions.append({
                'type': 'income_alert',
                'priority': 3,
                'severity': 'LOW',
                'category': 'Below Average Week',
                'message': f"Next week income predicted at ₹{predicted_income:.0f}, which is 15% below your average. Plan accordingly.",
                'action_required': False,
                'timeline': 'next week',
                'source': 'weather_agent'
            })
        
        # ==============================================================================
        # EXISTING: 7. GOAL PROGRESS CHECK (Monthly) (Priority 4)
        # ==============================================================================
        if datetime.now().day == 1:  # First of month
            interventions.append({
                'type': 'goal_reminder',
                'priority': 4,  # Low priority
                'severity': 'INFO',
                'category': 'Goal Progress',
                'message': f"Monthly goal check: Review your progress toward {self.profile.get('goals', ['financial goals'])[0]}",
                'action_required': False,
                'timeline': 'monthly',
                'source': 'orchestrator'
            })
        
        # Sort by priority (0 = highest)
        interventions.sort(key=lambda x: x['priority'])
        
        # Limit to top 3 to avoid overwhelming user
        return interventions[:3]
    
    def _create_dashboard_summary(self, forecast_report, spending_patterns, interventions):
        """
        Create unified dashboard data
        """
        forecast = forecast_report['predictions']
        patterns = forecast_report['patterns']
        risks = forecast_report.get('risks', [])
        
        # Calculate key metrics
        weekly_income = forecast['weekly_total']
        weekly_spending = spending_patterns['daily_average'] * 7
        net_cash_flow = weekly_income - weekly_spending
        savings_rate = (net_cash_flow / weekly_income * 100) if weekly_income > 0 else 0
        
        # Risk level
        risk_level = 'HIGH' if any(r['severity'] == 'HIGH' for r in risks) else \
                     'MEDIUM' if any(r['severity'] == 'MEDIUM' for r in risks) else 'LOW'
        
        # Overall health score (0-100)
        health_score = self._calculate_financial_health_score(
            forecast_report, 
            spending_patterns, 
            net_cash_flow
        )
        
        dashboard = {
            'summary': {
                'weekly_income_forecast': round(weekly_income, 2),
                'weekly_spending': round(weekly_spending, 2),
                'net_cash_flow': round(net_cash_flow, 2),
                'savings_rate': round(savings_rate, 1),
                'financial_health_score': health_score
            },
            'income': {
                'next_week': round(weekly_income, 2),
                'daily_avg': round(forecast['daily_avg'], 2),
                'best_day': list(patterns['best_days'].keys())[0] if patterns['best_days'] else 'Unknown',
                'confidence': 85
            },
            'spending': {
                'total_monthly': spending_patterns['total_spent'],
                'daily_avg': spending_patterns['daily_average'],
                'top_category': spending_patterns['top_category'],
                'discretionary_pct': spending_patterns['discretionary_percent']
            },
            'risks': {
                'level': risk_level,
                'count': len(risks),
                'urgent_count': len([i for i in interventions if i['priority'] <= 2]),
                'top_risk': risks[0]['type'] if risks else None
            },
            'patterns': {
                'efficiency': patterns['efficiency_trend']['current_per_hour'],
                'efficiency_trend': patterns['efficiency_trend']['trend'],
                'volatility': patterns['volatility']['risk_level'],
                'best_platform': patterns.get('best_platform', 'N/A')
            },
            'alerts': {
                'total': len(interventions),
                'urgent': len([i for i in interventions if i['severity'] == 'HIGH']),
                'warnings': len([i for i in interventions if i['severity'] == 'MEDIUM']),
                'info': len([i for i in interventions if i['severity'] == 'LOW'])
            }
        }
        
        return dashboard
    
    def _calculate_financial_health_score(self, forecast, spending, net_flow):
        """
        Calculate overall financial health score (0-100)
        Higher is better
        """
        score = 50  # Start at 50 (neutral)
        
        # Factor 1: Positive cash flow (+20 points max)
        if net_flow > 0:
            score += min(20, (net_flow / 1000) * 5)  # ₹1000 surplus = +5 points
        else:
            score += max(-20, (net_flow / 1000) * 5)  # ₹1000 deficit = -5 points
        
        # Factor 2: Income stability (+15 points max)
        volatility = forecast['patterns']['volatility']['coefficient']
        if volatility < 0.3:
            score += 15  # Low volatility = stable
        elif volatility < 0.5:
            score += 10
        else:
            score += 5
        
        # Factor 3: No high risks (+15 points max)
        high_risks = [r for r in forecast.get('risks', []) if r['severity'] == 'HIGH']
        if not high_risks:
            score += 15
        elif len(high_risks) == 1:
            score += 8
        else:
            score += 0
        
        # Factor 4: Efficiency trend (+10 points max)
        efficiency_trend = forecast['patterns']['efficiency_trend']['trend']
        if efficiency_trend == 'improving':
            score += 10
        elif efficiency_trend == 'stable':
            score += 5
        
        # Factor 5: Discretionary spending control (+10 points max)
        discretionary_pct = spending['discretionary_percent']
        if discretionary_pct < 15:
            score += 10
        elif discretionary_pct < 25:
            score += 5
        
        # Cap between 0-100
        return max(0, min(100, round(score)))
    
    def chat(self, user_message):
        """
        Unified chat interface - routes to appropriate agent
        """
        print(f"💬 Processing: '{user_message[:50]}...'")
        
        # Determine which agent should handle this
        message_lower = user_message.lower()
        
        # Income/forecast related → Weather Agent
        if any(word in message_lower for word in ['income', 'earn', 'forecast', 'next week', 'predict', 'weather']):
            # Get latest forecast
            forecast = self.weather_agent.predict_income(7)
            context = f"Weekly forecast: ₹{forecast['weekly_total']}, Daily avg: ₹{forecast['daily_avg']}"
            
            # But let Coach Agent respond (better at conversation)
            response = self.coach_agent.chat(user_message, context={'forecast': context})
        
        # Spending/saving related → Coach Agent
        elif any(word in message_lower for word in ['spend', 'save', 'buy', 'afford', 'money', 'budget']):
            spending = self.coach_agent.analyze_spending_patterns()
            response = self.coach_agent.chat(user_message, context={'spending': spending})
        
        # General questions → Coach Agent (better personality)
        else:
            response = self.coach_agent.chat(user_message)
        
        return response
    
    def get_quick_summary(self):
        """
        Get quick summary without full daily check (faster)
        """
        print("⚡ Generating quick summary...")
        
        # Just get predictions, skip full analysis
        forecast = self.weather_agent.predict_income(7)
        patterns = self.weather_agent.identify_patterns()
        risks = self.weather_agent.identify_risks(forecast)
        
        return {
            'weekly_forecast': forecast['weekly_total'],
            'daily_avg': forecast['daily_avg'],
            'best_day': list(patterns['best_days'].keys())[0] if patterns['best_days'] else 'Unknown',
            'risk_level': 'HIGH' if any(r['severity'] == 'HIGH' for r in risks) else 'LOW',
            'risk_count': len(risks)
        }
    
    def track_intervention_effectiveness(self, intervention_id, user_action, outcome):
        """
        Track if advice was followed and if it helped
        (Learning mechanism for future improvements)
        """
        self.intervention_history.append({
            'intervention_id': intervention_id,
            'timestamp': datetime.now().isoformat(),
            'user_action': user_action,  # 'followed', 'ignored', 'partial'
            'outcome': outcome  # 'positive', 'negative', 'neutral'
        })
        
        # Update effectiveness tracking
        if intervention_id not in self.advice_effectiveness:
            self.advice_effectiveness[intervention_id] = {
                'total': 0,
                'followed': 0,
                'positive_outcomes': 0
            }
        
        self.advice_effectiveness[intervention_id]['total'] += 1
        if user_action == 'followed':
            self.advice_effectiveness[intervention_id]['followed'] += 1
        if outcome == 'positive':
            self.advice_effectiveness[intervention_id]['positive_outcomes'] += 1
        
        return self.advice_effectiveness[intervention_id]
    

    def get_savings_rate(self):
            """
            Get current savings rate from savings agent
            """
            if hasattr(self, 'savings_agent'):
                return self.savings_agent.savings_rate
            return 0.03  # Default 3%
        
    def adjust_savings_rate(self, new_rate, reason="User requested"):
        """
        Adjust savings rate through savings agent
        """
        if not hasattr(self, 'savings_agent'):
            return {
                'success': False,
                'message': 'Savings agent not initialized'
            }
        
        try:
            # Validate rate
            if new_rate < 0.01 or new_rate > 0.20:
                return {
                    'success': False,
                    'message': f'Savings rate must be between 1% and 20%. You entered {int(new_rate*100)}%'
                }
            
            # Update in savings agent
            old_rate = self.savings_agent.savings_rate
            self.savings_agent.savings_rate = new_rate
            
            return {
                'success': True,
                'message': f'✅ Savings rate updated from {int(old_rate*100)}% to {int(new_rate*100)}%',
                'old_rate': old_rate,
                'new_rate': new_rate
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Error updating savings rate: {str(e)}'
            }



# Utility functions
def print_orchestrator_report(report):
    """Pretty print orchestrator report"""
    
    print("\n" + "="*80)
    print("📊 STORMGUARD FINANCIAL HEALTH REPORT")
    print("="*80 + "\n")
    
    # Dashboard summary
    dash = report['dashboard']
    summary = dash['summary']
    
    print("📈 FINANCIAL HEALTH OVERVIEW")
    print("-" * 80)
    print(f"💯 Health Score:      {summary['financial_health_score']}/100")
    
    # Visual health indicator
    if summary['financial_health_score'] >= 75:
        health_emoji = "💚 Excellent"
    elif summary['financial_health_score'] >= 60:
        health_emoji = "💛 Good"
    elif summary['financial_health_score'] >= 40:
        health_emoji = "🟡 Fair"
    else:
        health_emoji = "🔴 Needs Attention"
    
    print(f"📊 Status:            {health_emoji}")
    print(f"💰 Weekly Income:     ₹{summary['weekly_income_forecast']:,.0f}")
    print(f"💸 Weekly Spending:   ₹{summary['weekly_spending']:,.0f}")
    print(f"💵 Net Cash Flow:     ₹{summary['net_cash_flow']:,.0f}")
    print(f"📊 Savings Rate:      {summary['savings_rate']:.1f}%\n")
    
    # Risks & Alerts
    if report['interventions']:
        print("⚠️  PRIORITY ALERTS")
        print("-" * 80)
        for i, intervention in enumerate(report['interventions'], 1):
            severity_emoji = "🔴" if intervention['severity'] == 'HIGH' else \
                           "🟡" if intervention['severity'] == 'MEDIUM' else "🟢"
            
            print(f"{severity_emoji} Alert {i}: {intervention['category']}")
            print(f"   Priority: {intervention['priority']} | Timeline: {intervention['timeline']}")
            print(f"   Action Required: {'YES' if intervention['action_required'] else 'No'}\n")
    else:
        print("✅ NO URGENT ALERTS - You're in good shape!\n")
    
    # Coaching advice
    print("💬 YOUR FINANCIAL COACH")
    print("-" * 80)
    print(report['coaching'][:300] + "...\n")
    
    # Savings plan
    print("💰 SAVINGS STRATEGY")
    print("-" * 80)
    print(report['savings_plan'][:300] + "...\n")
    
    print("="*80 + "\n")


# Test function
if __name__ == "__main__":
    print("🧪 Testing Orchestrator Agent\n")
    
    from data.simulator import GigWorkerSimulator
    
    # Setup
    print("📊 Setting up test data...")
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    income_data = simulator.generate_income_history(90)
    spending_data = simulator.generate_spending_data(30)
    
    user_profile = {
        'user_id': 'test_user_001',
        'name': 'Rajesh',
        'city': 'Bangalore',
        'platform': 'Swiggy + Zomato',
        'language': 'hinglish',
        'goals': ['Save ₹20,000 emergency fund', 'Buy bike in 8 months']
    }
    
    print("✅ Data ready\n")
    
    # Initialize Orchestrator
    print("🤖 Initializing Orchestrator...")
    orchestrator = OrchestratorAgent(user_profile, income_data, spending_data)
    print()
    
    # Run daily check
    report = orchestrator.run_daily_check()
    
    # Print report
    print_orchestrator_report(report)
    
    # Test chat
    print("💬 Testing Chat Interface:")
    print("-" * 80)
    questions = [
        "Should I work this Sunday?",
        "How much should I save this week?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        response = orchestrator.chat(q)
        print(f"A: {response[:200]}...")
    
    print("\n✅ Orchestrator Agent test complete!")