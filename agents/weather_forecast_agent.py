# agents/weather_forecast_agent.py
from phi.agent import Agent
from phi.model.google import Gemini
from prophet import Prophet
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.weather_api import WeatherAPI

class WeatherForecastAgent:
    """
    Income Prediction Agent
    - Uses Prophet for time series forecasting
    - Integrates real weather data from OpenWeather API
    - Identifies patterns, risks, and opportunities
    - Continuously learns from prediction accuracy
    - Provides AI-powered insights using Ollama
    """
    
    def __init__(self, historical_data, user_id="user_001"):
        self.user_id = user_id
        self.data = historical_data
        self.weather_api = WeatherAPI()
        self.prophet_model = None
        self.learning_history = []
        
        # Initialize Phidata Agent with Ollama
        self.agent = Agent(
            name="Weather Forecast Agent",
            model=Gemini(id="gemini-2.0-flash"),
            instructions=[
                "You are an expert income forecasting agent for Indian gig workers.",
                "You analyze delivery partner income patterns (Swiggy, Zomato, etc.).",
                "You predict income 7-30 days ahead using ML and external data.",
                "You identify risks proactively and suggest concrete actions.",
                "Keep responses concise, actionable, and encouraging.",
                "Use Indian context: festivals, weather patterns, local events.",
                "Speak simply - avoid jargon. Use Hinglish when appropriate.",
                "Always provide specific numbers and timelines."
            ],
            markdown=True,
            show_tool_calls=True,
            debug_mode=False
        )
        
        print(f"✅ Weather Forecast Agent initialized for {user_id}")
    
    def train_prophet_model(self):
        """
        Train Prophet model on historical data
        Adds regressors: weekend, festival, weather
        """
        print("🔧 Training Prophet model...")
        
        df = self.data.copy()
        
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df['date']),
            'y': df['income']
        })
        
        # Add regressors (external factors)
        prophet_df['is_weekend'] = prophet_df['ds'].dt.dayofweek >= 5
        prophet_df['is_festival'] = df['is_festival'].values
        prophet_df['is_rainy'] = (df['weather'] == 'rain').values
        
        # Initialize Prophet with Indian holidays
        self.prophet_model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,  # Not enough data yet
            changepoint_prior_scale=0.05,  # Flexibility in trend changes
            seasonality_prior_scale=10.0,  # Strength of seasonality
            interval_width=0.85  # Confidence intervals
        )
        
        # Add regressors to model
        self.prophet_model.add_regressor('is_weekend')
        self.prophet_model.add_regressor('is_festival')
        self.prophet_model.add_regressor('is_rainy')
        
        # Train
        self.prophet_model.fit(prophet_df)
        
        print(f"✅ Model trained on {len(prophet_df)} days of data")
        return True
    
    def predict_income(self, days_ahead=7):
        """
        Generate income predictions for next N days
        Integrates real weather forecast
        """
        if self.prophet_model is None:
            self.train_prophet_model()
        
        print(f"🔮 Generating {days_ahead}-day forecast...")
        
        # Get weather forecast
        weather_forecast = self.weather_api.get_forecast(days_ahead)
        
        # Create future dataframe
        future = self.prophet_model.make_future_dataframe(periods=days_ahead)
        
        # Add regressors for future dates
        future['is_weekend'] = future['ds'].dt.dayofweek >= 5
        future['is_festival'] = False  # Simplified - could add festival calendar
        
        # Map weather forecast to future dates
        future['is_rainy'] = False
        for i, weather_day in enumerate(weather_forecast):
            future_date = (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')
            future.loc[future['ds'] == future_date, 'is_rainy'] = weather_day['will_rain']
        
        # Generate predictions
        forecast = self.prophet_model.predict(future)
        
        # Extract future predictions only
        predictions = forecast.tail(days_ahead)
        
        # Format results with weather context
        results = []
        for i, (_, row) in enumerate(predictions.iterrows()):
            weather_day = weather_forecast[i] if i < len(weather_forecast) else {}
            weather_impact = self.weather_api.get_weather_impact_score(weather_day) if weather_day else 1.0
            
            # Adjust prediction with weather impact
            adjusted_income = row['yhat'] * weather_impact
            
            results.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'day_name': row['ds'].strftime('%A'),
                'predicted_income': round(adjusted_income, 2),
                'base_prediction': round(row['yhat'], 2),
                'lower_bound': round(row['yhat_lower'], 2),
                'upper_bound': round(row['yhat_upper'], 2),
                'confidence': 0.85,  # From Prophet's interval_width
                'weather': weather_day.get('weather', 'Unknown'),
                'will_rain': weather_day.get('will_rain', False),
                'weather_impact': weather_impact,
                'temperature': weather_day.get('avg_temp', 'N/A')
            })
        
        return {
            'predictions': results,
            'weekly_total': round(sum([r['predicted_income'] for r in results]), 2),
            'daily_avg': round(np.mean([r['predicted_income'] for r in results]), 2),
            'forecast_generated_at': datetime.now().isoformat()
        }
    
    def identify_patterns(self):
        """
        Analyze historical data to find income patterns
        """
        print("🔍 Analyzing income patterns...")
        
        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour if 'hour' in df.columns else None
        
        patterns = {}
        
        # Best/worst days of week
        daily_avg = df.groupby('day_name')['income'].mean().sort_values(ascending=False)
        patterns['best_days'] = daily_avg.head(3).to_dict()
        patterns['worst_days'] = daily_avg.tail(2).to_dict()
        
        # Platform performance
        if 'platform' in df.columns:
            platform_avg = df.groupby('platform')['income'].mean()
            patterns['best_platform'] = platform_avg.idxmax()
            patterns['platform_comparison'] = platform_avg.to_dict()
        
        # Weather impact
        if 'weather' in df.columns:
            weather_avg = df.groupby('weather')['income'].mean()
            patterns['weather_impact'] = weather_avg.to_dict()
        
        # Efficiency trend
        if 'efficiency' in df.columns:
            recent_efficiency = df.tail(14)['efficiency'].mean()
            older_efficiency = df.head(14)['efficiency'].mean()
            efficiency_change = ((recent_efficiency - older_efficiency) / older_efficiency) * 100
            
            patterns['efficiency_trend'] = {
                'current_per_hour': round(recent_efficiency, 2),
                'previous_per_hour': round(older_efficiency, 2),
                'change_percent': round(efficiency_change, 1),
                'trend': 'improving' if efficiency_change > 0 else 'declining'
            }
        
        # Income volatility (coefficient of variation)
        patterns['volatility'] = {
            'coefficient': round(df['income'].std() / df['income'].mean(), 2),
            'std_dev': round(df['income'].std(), 2),
            'risk_level': 'high' if df['income'].std() / df['income'].mean() > 0.4 else 'moderate'
        }
        
        # Overall stats
        patterns['overall'] = {
            'avg_daily_income': round(df['income'].mean(), 2),
            'median_income': round(df['income'].median(), 2),
            'best_day_ever': round(df['income'].max(), 2),
            'worst_day_ever': round(df['income'].min(), 2)
        }
        
        return patterns
    
    def identify_risks(self, predictions, upcoming_bills=None):
        """
        Identify financial risks with precise bill tracking
        """
        print("⚠️  Analyzing financial risks...")
        
        risks = []
        weekly_income = predictions['weekly_total']
        daily_predictions = predictions['predictions']
        
        # Default bills if none provided (Fallback)
        if upcoming_bills is None:
            upcoming_bills = [
                {'name': 'Rent', 'amount': 8000, 'due_in_days': 5},
                {'name': 'Insurance', 'amount': 1500, 'due_in_days': 3}
            ]

        # Risk 1: Precise Cash Crunch Prediction
        total_bills_due = sum(b['amount'] for b in upcoming_bills if b['due_in_days'] <= 7)
        # Assume 30% of income goes to daily subsistence (food/fuel) before bills
        available_cash = weekly_income * 0.70 
        
        if available_cash < total_bills_due:
            shortfall = total_bills_due - available_cash
            urgent_bill = min(upcoming_bills, key=lambda x: x['due_in_days'])
            
            risks.append({
                'type': 'Cash Crunch Prediction',
                'severity': 'HIGH',
                'probability': 0.9,
                'timeline': f"{urgent_bill['due_in_days']} days",
                'shortfall_amount': round(shortfall, 2),
                'bill_name': urgent_bill['name'],
                'due_date': urgent_bill['due_in_days'],
                'impact': f"Missed {urgent_bill['name']} payment",
                'recommendations': [
                    "Target high-demand zones immediately",
                    "Extend shift by 2-3 hours",
                ]
            })
        
        # Risk 2: Income decline trend
        recent_avg = self.data.tail(7)['income'].mean()
        older_avg = self.data.tail(21).head(7)['income'].mean()
        
        if recent_avg < older_avg * 0.85:  # 15%+ decline
            decline_pct = round((1 - recent_avg/older_avg) * 100, 1)
            
            risks.append({
                'type': 'Income Decline Trend',
                'severity': 'MEDIUM',
                'probability': 0.75,
                'decline_percent': decline_pct,
                'recent_weekly_avg': round(recent_avg, 2),
                'previous_weekly_avg': round(older_avg, 2),
                'recommendations': [
                    "Switch to UberEats for lunch shift (12-2 PM)",
                    "Try different work zone (move 2-3 km north)",
                    "Focus on dinner peak hours (7-9 PM only)",
                    "Check if platform reduced per-order pay"
                ]
            })
        
        # Risk 3: High volatility
        volatility = self.data['income'].std() / self.data['income'].mean()
        if volatility > 0.4:
            risks.append({
                'type': 'High Income Volatility',
                'severity': 'LOW',
                'volatility_score': round(volatility, 2),
                'impact': 'Difficult budgeting, increased financial stress',
                'recommendations': [
                    "Join peer insurance circle for income smoothing",
                    "Build 4-week emergency fund (₹15,000-20,000)",
                    "Diversify: Add second platform (Dunzo, Amazon Flex)"
                ]
            })
        
        # Risk 4: Weather-related income drop
        rainy_days = sum([1 for p in daily_predictions if p['will_rain']])
        if rainy_days < 2 and len(daily_predictions) >= 7:  # No rain = potentially lower income
            risks.append({
                'type': 'Low Demand Week',
                'severity': 'LOW',
                'reason': 'No rain predicted (fewer delivery orders expected)',
                'impact': 'Potential 10-15% income reduction',
                'recommendations': [
                    "Focus on lunch and dinner peaks",
                    "Accept longer-distance orders",
                    "Consider switching to ride-hailing temporarily"
                ]
            })
        
        return risks
    
    def calculate_prediction_accuracy(self, predicted, actual):
        """
        Calculate accuracy and store for continuous learning
        """
        error = abs(predicted - actual) / actual
        accuracy = max(0, 1 - error)  # Convert error to accuracy
        
        self.learning_history.append({
            'predicted': predicted,
            'actual': actual,
            'accuracy': accuracy,
            'error_percent': error * 100,
            'timestamp': datetime.now().isoformat()
        })
        
        # Calculate rolling accuracy (last 7 predictions)
        if len(self.learning_history) >= 7:
            recent_accuracy = np.mean([h['accuracy'] for h in self.learning_history[-7:]])
            improvement_needed = recent_accuracy < 0.75
            
            return {
                'current_accuracy': round(accuracy * 100, 1),
                'rolling_7day_accuracy': round(recent_accuracy * 100, 1),
                'total_predictions': len(self.learning_history),
                'should_retrain': improvement_needed
            }
        
        return {
            'current_accuracy': round(accuracy * 100, 1),
            'total_predictions': len(self.learning_history),
            'should_retrain': False
        }
    
    def generate_ai_analysis(self, forecast_data, patterns, risks):
        """
        Generate AI-powered analysis using Ollama
        """
        print("🤖 Generating AI analysis...")
        
        context = f"""
Analyze this gig worker's income forecast:

PREDICTIONS (Next 7 Days):
- Total Income: ₹{forecast_data['weekly_total']}
- Daily Average: ₹{forecast_data['daily_avg']}
- Confidence: 85%

WEATHER CONTEXT:
{self._format_weather_summary(forecast_data['predictions'])}

PATTERNS DISCOVERED:
- Best Days: {patterns['best_days']}
- Best Platform: {patterns.get('best_platform', 'N/A')}
- Efficiency: ₹{patterns['efficiency_trend']['current_per_hour']}/hour ({patterns['efficiency_trend']['trend']})
- Volatility: {patterns['volatility']['risk_level']} ({patterns['volatility']['coefficient']})

RISKS IDENTIFIED:
{len(risks)} risk(s) detected - Severity levels: {[r['severity'] for r in risks]}

Provide analysis in Hinglish (Hindi-English mix):
1. Summary: Is next week good or challenging? (2 sentences)
2. Top 3 actionable insights with specific numbers
3. Brief encouragement (1 sentence)

Keep under 180 words. Be conversational and supportive.
"""
        
        response = self.agent.run(context)
        return response.content
    
    def _format_weather_summary(self, predictions):
        """Format weather summary for AI"""
        rainy_days = [p for p in predictions if p['will_rain']]
        return f"Rainy days: {len(rainy_days)}/7, Avg temp: {np.mean([p['temperature'] for p in predictions if isinstance(p['temperature'], (int, float))])}°C"
    
    def generate_complete_forecast(self, days_ahead=7):
        """
        Main method: Generate complete forecast report
        """
        print(f"\n{'='*60}")
        print(f"🌦️  GENERATING INCOME WEATHER FORECAST")
        print(f"{'='*60}\n")
        
        # Step 1: Generate predictions
        predictions = self.predict_income(days_ahead)
        print(f"✅ Predictions generated: ₹{predictions['weekly_total']} expected")
        
        # Step 2: Identify patterns
        patterns = self.identify_patterns()
        print(f"✅ Patterns identified: Best day is {list(patterns['best_days'].keys())[0]}")
        
        # Step 3: Identify risks
        risks = self.identify_risks(predictions)
        print(f"✅ Risk analysis complete: {len(risks)} risk(s) detected")
        
        # Step 4: Generate AI analysis
        ai_analysis = self.generate_ai_analysis(predictions, patterns, risks)
        print(f"✅ AI analysis generated\n")
        
        return {
            'predictions': predictions,
            'patterns': patterns,
            'risks': risks,
            'ai_analysis': ai_analysis,
            'learning_stats': {
                'total_predictions_made': len(self.learning_history),
                'model_accuracy': round(np.mean([h['accuracy'] for h in self.learning_history]) * 100, 1) if self.learning_history else 0,
                'improvement_trend': 'learning' if len(self.learning_history) > 0 else 'new'
            },
            'metadata': {
                'user_id': self.user_id,
                'forecast_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'days_forecasted': days_ahead,
                'data_points_used': len(self.data),
                'model_type': 'Prophet + Weather Integration'
            }
        }


# Utility function for pretty printing
def print_forecast_report(report):
    """Pretty print forecast report"""
    print(f"\n{'='*70}")
    print(f"📊 INCOME WEATHER FORECAST REPORT")
    print(f"{'='*70}\n")
    
    # Predictions
    print("🔮 PREDICTIONS (Next 7 Days):")
    print(f"{'─'*70}")
    for pred in report['predictions']['predictions']:
        weather_icon = "🌧️" if pred['will_rain'] else "☀️"
        print(f"{weather_icon} {pred['day_name']:10s} {pred['date']:12s} | "
              f"₹{pred['predicted_income']:7.0f} | "
              f"{pred['weather']:10s} | "
              f"{pred['temperature']}°C")
    
    print(f"{'─'*70}")
    print(f"💰 Weekly Total:  ₹{report['predictions']['weekly_total']:,.0f}")
    print(f"📊 Daily Average: ₹{report['predictions']['daily_avg']:,.0f}")
    print(f"✅ Confidence:    85%\n")
    
    # Patterns
    print("🔍 PATTERNS DISCOVERED:")
    print(f"{'─'*70}")
    patterns = report['patterns']
    
    print("📈 Best Earning Days:")
    for day, amt in list(patterns['best_days'].items())[:3]:
        print(f"   • {day}: ₹{amt:.0f}")
    
    if 'efficiency_trend' in patterns:
        eff = patterns['efficiency_trend']
        trend_icon = "📈" if eff['trend'] == 'improving' else "📉"
        print(f"\n{trend_icon} Efficiency: ₹{eff['current_per_hour']}/hour ({eff['trend']} {abs(eff['change_percent'])}%)")
    
    if 'volatility' in patterns:
        vol = patterns['volatility']
        print(f"📊 Income Volatility: {vol['risk_level'].upper()} ({vol['coefficient']})")
    
    print()
    
    # Risks
    if report['risks']:
        print("⚠️  RISKS IDENTIFIED:")
        print(f"{'─'*70}")
        for risk in report['risks']:
            severity_icon = "🔴" if risk['severity'] == 'HIGH' else "🟡" if risk['severity'] == 'MEDIUM' else "🟢"
            print(f"{severity_icon} {risk['type']} - {risk['severity']} SEVERITY")
            
            if 'shortfall_amount' in risk:
                print(f"   Shortfall: ₹{risk['shortfall_amount']:.0f}")
            
            if 'decline_percent' in risk:
                print(f"   Decline: {risk['decline_percent']}%")
            
            if 'mitigation_strategies' in risk:
                print(f"   Actions:")
                for action in risk['mitigation_strategies'][:2]:
                    print(f"   • {action}")
            elif 'recommendations' in risk:
                print(f"   Actions:")
                for action in risk['recommendations'][:2]:
                    print(f"   • {action}")
            print()
    else:
        print("✅ NO MAJOR RISKS DETECTED\n")
    
    # AI Analysis
    print("🤖 AI COACH ANALYSIS:")
    print(f"{'─'*70}")
    print(report['ai_analysis'])
    print(f"{'─'*70}\n")
    
    # Learning stats
    if report['learning_stats']['total_predictions_made'] > 0:
        print("📚 CONTINUOUS LEARNING:")
        print(f"{'─'*70}")
        print(f"Total Predictions: {report['learning_stats']['total_predictions_made']}")
        print(f"Model Accuracy: {report['learning_stats']['model_accuracy']}%")
        print(f"Status: {report['learning_stats']['improvement_trend']}")
        print()


# Test function
if __name__ == "__main__":
    print("🧪 Testing Weather Forecast Agent\n")
    
    # Import simulator
    from data.simulator import GigWorkerSimulator
    
    # Generate test data
    print("📊 Generating test data...")
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    historical_data = simulator.generate_income_history(90)
    print(f"✅ Generated {len(historical_data)} days of data\n")
    
    # Initialize agent
    print("🤖 Initializing Weather Forecast Agent...")
    agent = WeatherForecastAgent(historical_data, user_id="test_user_001")
    print()
    
    # Generate forecast
    report = agent.generate_complete_forecast(days_ahead=7)
    
    # Print report
    print_forecast_report(report)
    
    # Test continuous learning
    print("\n🧪 Testing Continuous Learning:")
    print(f"{'─'*70}")
    
    # Simulate some predictions
    for i in range(3):
        predicted = 500 + (i * 50)
        actual = 480 + (i * 55)
        accuracy_report = agent.calculate_prediction_accuracy(predicted, actual)
        print(f"Prediction {i+1}: Predicted ₹{predicted}, Actual ₹{actual} → "
              f"Accuracy: {accuracy_report['current_accuracy']}%")
    
    print(f"\n✅ Weather Forecast Agent test complete!")