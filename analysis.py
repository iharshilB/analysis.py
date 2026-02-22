import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# API Keys (Added as Secrets in Hugging Face)
FMP_API_KEY = os.getenv("FMP_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class MacroStrategist:
    @staticmethod
    def get_market_bias(symbol="EURUSD"):
        """Fetches sentiment and price action to determine a professional bias."""
        # 🔧 FIX: Removed space in URL before {symbol}
        url = f"https://site.financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_KEY}"
        
        try:
            response = requests.get(url, timeout=10).json()
            
            if not response or not isinstance(response, list) or len(response) == 0:
                return {"error": "Data Unavailable"}
            
            price = response[0].get('price', 0)
            change = response[0].get('changesPercentage', 0)
            
            # Professional Interpretation Logic
            bias = "Neutral"
            if change > 0.5: 
                bias = "Bullish"
            elif change < -0.5: 
                bias = "Bearish"
            
            return {
                "symbol": symbol,
                "price": price,
                "bias": bias,
                "interpretation": f"The {symbol} is currently showing a {bias.lower()} bias in the intraday session. Institutional flow suggests monitoring liquidity levels at recent highs/lows."
            }
        except Exception as e:
            print(f"❌ Error fetching bias: {e}")
            return {"error": str(e)}

    @staticmethod
    def generate_chart(symbol="EURUSD"):
        """Generates a professional candlestick/line chart."""
        # 🔧 FIX: Removed space in URL before {symbol}
        url = f"https://site.financialmodelingprep.com/api/v3/historical-price-full/{symbol}?timeseries=30&apikey={FMP_API_KEY}"
        
        try:
            data = requests.get(url, timeout=15).json()
            
            if 'historical' not in data or not data['historical']:
                return None

            df = pd.DataFrame(data['historical'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

            plt.figure(figsize=(10, 5))
            plt.plot(df['date'], df['close'], color='#2962FF', linewidth=2, label=f"{symbol} Close")
            plt.fill_between(df['date'], df['close'], color='#2962FF', alpha=0.1)
            
            plt.title(f"{symbol} Macro Trend Analysis", fontsize=14, color='white')
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.legend()
            
            # Style for Dark Mode (Hugging Face / Professional Look)
            plt.gcf().set_facecolor('#131722')
            plt.gca().set_facecolor('#131722')
            plt.tick_params(colors='white')
            
            # 🔧 CRITICAL FIX: Save to /tmp/ for HF Spaces compatibility
            chart_path = f"/tmp/{symbol}_chart.png"
            plt.savefig(chart_path, facecolor='#131722', bbox_inches='tight')
            plt.close()
            return chart_path
            
        except Exception as e:
            print(f"❌ Error generating chart: {e}")
            plt.close()
            return None

    @staticmethod
    def get_economic_calendar():
        """Fetches high-impact economic events."""
        # 🔧 FIX: Removed space in apikey= {FMP_API_KEY}
        url = f"https://site.financialmodelingprep.com/api/v3/economic_calendar?apikey={FMP_API_KEY}"
        
        try:
            events = requests.get(url, timeout=10).json()
            # Filter for high impact only
            high_impact = [e for e in events[:10] if e.get('impact') == 'High']
            return high_impact
        except Exception as e:
            print(f"❌ Error fetching calendar: {e}")
            return []
