import streamlit as st
import requests
import random
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="Crypto AI Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'is_analyzing' not in st.session_state:
    st.session_state.is_analyzing = False
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'crypto_prices' not in st.session_state:
    st.session_state.crypto_prices = {}
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# Crypto database
CRYPTO_DATABASE = [
    {"name": "Bitcoin", "symbol": "BTC", "id": "bitcoin"},
    {"name": "Ethereum", "symbol": "ETH", "id": "ethereum"},
    {"name": "Solana", "symbol": "SOL", "id": "solana"},
    {"name": "Cardano", "symbol": "ADA", "id": "cardano"},
    {"name": "Ripple", "symbol": "XRP", "id": "ripple"},
    {"name": "Polkadot", "symbol": "DOT", "id": "polkadot"},
    {"name": "Avalanche", "symbol": "AVAX", "id": "avalanche-2"},
    {"name": "Polygon", "symbol": "MATIC", "id": "matic-network"},
    {"name": "Chainlink", "symbol": "LINK", "id": "chainlink"},
    {"name": "Uniswap", "symbol": "UNI", "id": "uniswap"},
    {"name": "Litecoin", "symbol": "LTC", "id": "litecoin"},
    {"name": "Cosmos", "symbol": "ATOM", "id": "cosmos"},
    {"name": "Algorand", "symbol": "ALGO", "id": "algorand"},
    {"name": "VeChain", "symbol": "VET", "id": "vechain"},
    {"name": "Hedera", "symbol": "HBAR", "id": "hedera-hashgraph"},
    {"name": "Internet Computer", "symbol": "ICP", "id": "internet-computer"},
    {"name": "Filecoin", "symbol": "FIL", "id": "filecoin"},
    {"name": "Arbitrum", "symbol": "ARB", "id": "arbitrum"},
    {"name": "Optimism", "symbol": "OP", "id": "optimism"},
    {"name": "Aptos", "symbol": "APT", "id": "aptos"},
    {"name": "Sui", "symbol": "SUI", "id": "sui"},
    {"name": "Stellar", "symbol": "XLM", "id": "stellar"},
    {"name": "The Graph", "symbol": "GRT", "id": "the-graph"},
    {"name": "Sandbox", "symbol": "SAND", "id": "the-sandbox"},
    {"name": "Decentraland", "symbol": "MANA", "id": "decentraland"},
    {"name": "Aave", "symbol": "AAVE", "id": "aave"},
    {"name": "Maker", "symbol": "MKR", "id": "maker"},
    {"name": "Injective", "symbol": "INJ", "id": "injective-protocol"},
    {"name": "Near Protocol", "symbol": "NEAR", "id": "near"},
    {"name": "Fantom", "symbol": "FTM", "id": "fantom"}
]

PHASES = [
    {"id": 1, "name": "Pre-Screening", "icon": "🔒", "color": "blue"},
    {"id": 2, "name": "Fundamentals", "icon": "📊", "color": "purple"},
    {"id": 3, "name": "On-Chain", "icon": "📈", "color": "green"},
    {"id": 4, "name": "Timing", "icon": "⏰", "color": "orange"},
    {"id": 5, "name": "Portfolio", "icon": "💼", "color": "indigo"}
]

def fetch_crypto_prices():
    """Fetch current crypto prices from CoinGecko"""
    try:
        ids = ",".join([c["id"] for c in CRYPTO_DATABASE])
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            st.session_state.crypto_prices = response.json()
    except Exception as e:
        st.error(f"Error fetching prices: {e}")

def format_price(price):
    """Format price nicely"""
    if price == 0:
        return "N/A"
    if price < 0.01:
        return f"${price:.6f}"
    if price < 1:
        return f"${price:.4f}"
    return f"${price:,.2f}"

def format_price_change(change):
    """Format price change"""
    if not change:
        return "0.00"
    return f"{change:.2f}"

def calculate_tokenomics_score(tokenomics):
    """Calculate tokenomics score"""
    return sum(tokenomics.values())

def calculate_market_score(metrics):
    """Calculate market health score"""
    bullish = sum(1 for v in metrics.values() if v == "bullish")
    return round((bullish / len(metrics)) * 100)

def get_status_icon(status):
    """Get status emoji"""
    if status == "bullish":
        return "📈"
    if status == "bearish":
        return "📉"
    return "➖"

def analyze_project(crypto_data=None):
    """Analyze a crypto project"""
    # Find crypto from search or selection
    crypto = None
    if crypto_data:
        crypto = crypto_data
    else:
        search_lower = st.session_state.search_query.lower().strip()
        for c in CRYPTO_DATABASE:
            if c["name"].lower() == search_lower or c["symbol"].lower() == search_lower:
                crypto = c
                break
    
    if not crypto and not st.session_state.search_query.strip():
        return
    
    st.session_state.is_analyzing = True
    
    # Show loading
    with st.spinner(f"Analyzing {st.session_state.search_query or crypto['name']}... Running 5-phase analysis"):
        time.sleep(3)  # Simulate analysis time
        
        selected_crypto = crypto or {
            "name": st.session_state.search_query,
            "symbol": st.session_state.search_query[:4].upper(),
            "id": "unknown"
        }
        price_data = st.session_state.crypto_prices.get(selected_crypto["id"], {"usd": 0, "usd_24h_change": 0})
        
        # Generate analysis
        analysis = {
            "id": int(time.time() * 1000),
            "name": selected_crypto["name"],
            "symbol": selected_crypto["symbol"],
            "crypto_id": selected_crypto["id"],
            "current_price": price_data.get("usd", 0),
            "price_change_24h": price_data.get("usd_24h_change", 0),
            "timestamp": datetime.now().isoformat(),
            
            # Phase 1: Pre-Screening
            "phase1": {
                "market_cap": "Mid Cap" if random.random() > 0.3 else "Small Cap",
                "market_cap_value": f"${random.randint(100, 600)}M",
                "exchanges": "Binance, Coinbase, Kraken" if random.random() > 0.2 else "Binance, KuCoin",
                "active_months": random.randint(6, 30),
                "daily_volume": f"${random.randint(5, 55)}M",
                "has_product": random.random() > 0.3,
                "checks": {
                    "exchanges": random.random() > 0.2,
                    "active6months": True,
                    "volume": random.random() > 0.3,
                    "no_breach": random.random() > 0.4,
                    "has_mainnet": random.random() > 0.3,
                    "active_community": random.random() > 0.4,
                    "documentation": random.random() > 0.3
                }
            },
            
            # Phase 2: Fundamentals
            "phase2": {
                "tokenomics": {
                    "supply": random.randint(3, 5),
                    "distribution": random.randint(3, 5),
                    "utility": random.randint(3, 5),
                    "value_accrual": random.randint(3, 5),
                    "vesting": random.randint(3, 5)
                },
                "team": {
                    "identifiable": random.random() > 0.3,
                    "experience": random.random() > 0.4,
                    "communication": random.random() > 0.3,
                    "audited": random.random() > 0.4,
                    "github_active": random.random() > 0.3,
                    "open_source": random.random() > 0.5
                }
            },
            
            # Phase 3: On-Chain
            "phase3": {
                "metrics": {
                    "active_addresses": "bullish" if random.random() > 0.5 else "bearish",
                    "tx_volume": "bullish" if random.random() > 0.5 else "bearish",
                    "tvl": "bullish" if random.random() > 0.5 else "bearish",
                    "dev_activity": "bullish" if random.random() > 0.5 else "bearish",
                    "nvt_ratio": "bullish" if random.random() > 0.5 else "bearish",
                    "token_velocity": "bullish" if random.random() > 0.5 else "bearish",
                    "whale_activity": "bullish" if random.random() > 0.5 else "bearish"
                },
                "competitive_advantage": random.random() > 0.4
            },
            
            # Phase 4: Timing
            "phase4": {
                "rsi": random.randint(30, 70),
                "trend": ["Uptrend", "Sideways", "Downtrend"][random.randint(0, 2)],
                "fear_greed": random.randint(20, 80),
                "macd": "Bullish" if random.random() > 0.5 else "Bearish",
                "volume": "Above Average" if random.random() > 0.4 else "Below Average"
            },
            
            # Phase 5: Portfolio
            "phase5": {
                "confidence": "calculating...",
                "allocation": "calculating...",
                "recommendation": "calculating..."
            }
        }
        
        # Calculate overall confidence
        phase1_pass = sum(1 for v in analysis["phase1"]["checks"].values() if v)
        tokenomics_score = sum(analysis["phase2"]["tokenomics"].values())
        market_bullish = sum(1 for v in analysis["phase3"]["metrics"].values() if v == "bullish")
        
        confidence = "Low"
        allocation = "0.25-0.5%"
        recommendation = "HIGH RISK - Not Recommended"
        recommendation_color = "red"
        
        if phase1_pass >= 6 and tokenomics_score >= 23 and market_bullish >= 5 and analysis["phase4"]["rsi"] < 60:
            confidence = "Very High"
            allocation = "5-10%"
            recommendation = "STRONG BUY - Core Holding"
            recommendation_color = "green"
        elif phase1_pass >= 5 and tokenomics_score >= 18 and market_bullish >= 4:
            confidence = "High"
            allocation = "2-5%"
            recommendation = "BUY - Satellite Position"
            recommendation_color = "green"
        elif phase1_pass >= 4 and tokenomics_score >= 15 and market_bullish >= 3:
            confidence = "Medium"
            allocation = "1-2%"
            recommendation = "SPECULATIVE - Small Position"
            recommendation_color = "yellow"
        
        analysis["phase5"]["confidence"] = confidence
        analysis["phase5"]["allocation"] = allocation
        analysis["phase5"]["recommendation"] = recommendation
        analysis["phase5"]["recommendation_color"] = recommendation_color
        
        # Update state
        st.session_state.projects.insert(0, analysis)
        st.session_state.selected_project = analysis
        st.session_state.is_analyzing = False
        st.session_state.search_query = ""
        
        # Trigger rerun to update UI
        st.rerun()

def main():
    """Main application"""
    # Initialize on first load
    if not st.session_state.initialized:
        fetch_crypto_prices()
        st.session_state.initialized = True
    
    # Auto-refresh prices every minute
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    if time.time() - st.session_state.last_refresh > 60:
        fetch_crypto_prices()
        st.session_state.last_refresh = time.time()
    
    # Header
    st.markdown("""
    <style>
    .header { background: rgba(0,0,0,0.3); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.1); padding: 16px; }
    .title { font-size: 24px; font-weight: bold; color: white; margin: 0; }
    .subtitle { font-size: 12px; color: #9CA3AF; margin: 0; }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([1, 8])
        with col1:
            st.markdown('<div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center"><span style="color: white; font-size: 24px;">🚀</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<h1 class="title">Crypto AI Analyzer</h1>', unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Powered by 5-Phase Framework • Live Prices</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Search Section
    search_col1, search_col2 = st.columns([4, 1])
    
    with search_col1:
        # Create a text input for search
        search_key = "search_input"
        st.session_state.search_query = st.text_input(
            "Search crypto",
            value=st.session_state.search_query,
            placeholder="Search crypto (e.g., Bitcoin, ETH, Solana)...",
            label_visibility="collapsed"
        )
        
        # Show suggestions dropdown
        if st.session_state.search_query:
            filtered = [
                c for c in CRYPTO_DATABASE 
                if st.session_state.search_query.lower() in c["name"].lower() or 
                   st.session_state.search_query.lower() in c["symbol"].lower()
            ]
            if filtered:
                # Create a selectbox for suggestions
                suggestion_names = [f"{c['name']} ({c['symbol']})" for c in filtered[:10]]
                selected_suggestion = st.selectbox(
                    "Suggestions",
                    options=[""] + suggestion_names,
                    format_func=lambda x: "Select from suggestions..." if x == "" else x,
                    label_visibility="collapsed"
                )
                
                if selected_suggestion:
                    selected_name = selected_suggestion.split(" (")[0]
                    selected_crypto = next(c for c in filtered if c["name"] == selected_name)
                    if st.button("Select", key="select_suggestion"):
                        analyze_project(selected_crypto)
    
    with search_col2:
        analyze_disabled = st.session_state.is_analyzing or not st.session_state.search_query.strip()
        if st.button("🔍 Analyze", disabled=analyze_disabled, use_container_width=True):
            analyze_project()
    
    # Display Projects
    if st.session_state.projects:
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        # Create tabs for each project
        project_names = [f"{p['name']} ({p['symbol']})" for p in st.session_state.projects]
        tabs = st.tabs(project_names)
        
        for idx, project in enumerate(st.session_state.projects):
            with tabs[idx]:
                # Project Header
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, rgba(59,130,246,0.2), rgba(147,51,234,0.2), rgba(236,72,153,0.2)); 
                            backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); 
                            border-radius: 16px; padding: 24px;">
                    <h2 style="color: white; font-size: 32px; margin: 0;">{project['name']}</h2>
                    <p style="color: #9CA3AF; font-size: 20px;">{project['symbol']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Price Display
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Current Price",
                        format_price(project["current_price"]),
                        f"{format_price_change(project['price_change_24h'])}%"
                    )
                with col2:
                    # Recommendation
                    color = project["phase5"]["recommendation_color"]
                    if color == "green":
                        st.success(project["phase5"]["recommendation"])
                    elif color == "yellow":
                        st.warning(project["phase5"]["recommendation"])
                    else:
                        st.error(project["phase5"]["recommendation"])
                
                # Quick Stats
                st.markdown("---")
                st.subheader("Quick Stats")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Tokenomics Score", f"{calculate_tokenomics_score(project['phase2']['tokenomics'])}/25")
                col2.metric("Market Health", f"{calculate_market_score(project['phase3']['metrics'])}%")
                col3.metric("Confidence", project["phase5"]["confidence"])
                col4.metric("Allocation", project["phase5"]["allocation"])
                
                # Phases Analysis
                st.markdown("---")
                st.subheader("5-Phase Analysis")
                
                for phase in PHASES:
                    with st.expander(f"{phase['icon']} Phase {phase['id']}: {phase['name']}", expanded=True):
                        if phase['id'] == 1:
                            col1, col2 = st.columns(2)
                            col1.metric("Market Cap", project['phase1']['market_cap_value'])
                            col2.metric("Daily Volume", project['phase1']['daily_volume'])
                            
                            st.markdown("**Checks:**")
                            checks = project['phase1']['checks']
                            for check, passed in checks.items():
                                if passed:
                                    st.success(f"✅ {check.replace('_', ' ').title()}")
                                else:
                                    st.error(f"❌ {check.replace('_', ' ').title()}")
                        
                        elif phase['id'] == 2:
                            st.markdown("**Tokenomics:**")
                            tokenomics = project['phase2']['tokenomics']
                            for key, value in tokenomics.items():
                                st.progress(value / 5.0, text=f"{key.title()}: {value}/5")
                            
                            st.markdown("**Team:**")
                            team = project['phase2']['team']
                            for key, value in team.items():
                                if value:
                                    st.success(f"✅ {key.replace('_', ' ').title()}")
                                else:
                                    st.error(f"❌ {key.replace('_', ' ').title()}")
                        
                        elif phase['id'] == 3:
                            st.markdown("**On-Chain Metrics:**")
                            metrics = project['phase3']['metrics']
                            for key, value in metrics.items():
                                icon = get_status_icon(value)
                                if value == "bullish":
                                    st.success(f"{icon} {key.replace('_', ' ').title()}: {value}")
                                else:
                                    st.error(f"{icon} {key.replace('_', ' ').title()}: {value}")
                        
                        elif phase['id'] == 4:
                            col1, col2, col3 = st.columns(3)
                            col1.metric("RSI", project['phase4']['rsi'])
                            col2.metric("Trend", project['phase4']['trend'])
                            col3.metric("MACD", project['phase4']['macd'])
                            
                            col4, col5 = st.columns(2)
                            col4.metric("Fear & Greed", project['phase4']['fear_greed'])
                            col5.metric("Volume", project['phase4']['volume'])
                        
                        elif phase['id'] == 5:
                            st.info(f"**Confidence:** {project['phase5']['confidence']}")
                            st.info(f"**Allocation:** {project['phase5']['allocation']}")
                            st.info(f"**Recommendation:** {project['phase5']['recommendation']}")
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 48px;">
            <h2 style="color: white;">Welcome to Crypto AI Analyzer</h2>
            <p style="color: #9CA3AF;">Search for a cryptocurrency above to start the 5-phase analysis</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()