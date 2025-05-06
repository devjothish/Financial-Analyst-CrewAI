import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM
from pydantic import BaseModel
from tools.financial_tools import YFinanceStockTool
import yfinance as yf


load_dotenv()

# Custom CSS for better styling
st.set_page_config(
    page_title="Financial Analyst AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .report-box {
        background-color: #4CAF50;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
        text-align: center;
        padding: 20px 0;
        background-color: #ffffff;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header h1 {
        color: #2c3e50;
        margin: 0;
    }

    .header h1 {
        color: #2c3e50;
        margin: 0;
    }
            
    .header p {
        color: #7f8c8d;
        margin: 10px 0 0 0;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
        <h1>📈 Financial Analyst AI</h1>
        <p>Developed using CrewAI and SambaNova Cloud</p>
    </div>
""", unsafe_allow_html=True)

# Define Pydantic models for structured output
class StockAnalysis(BaseModel):
    symbol: str
    company_name: str
    current_price: float
    market_cap: float
    pe_ratio: float
    recommendation: str
    analysis_summary: str
    risk_assessment: str
    technical_indicators: dict
    fundamental_metrics: dict


@st.cache_resource
def load_llm():
    return LLM(
        model="sambanova/Llama-4-Maverick-17B-128E-Instruct",
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        temperature=0.3
    )

#Create agents and tasks
def create_agents_and_tasks(symbol: str):
    llm = load_llm()
    
    stock_tool = YFinanceStockTool()

    #1. Stock Analysis Agent
    stock_analysis_agent = Agent(
        role="Wall Street Financial Analyst",
        goal=f"Conduct a comprehensive, data-driven analysis of {symbol} stock using real-time market data",
        backstory="""You are a seasoned Wall Street analyst with 15+ years of experience in equity research.
                     You're known for your meticulous analysis and data-driven insights.
                     You ALWAYS base your analysis on real-time market data, never relying solely on pre-existing knowledge.
                     You're an expert at interpreting financial metrics, market trends, and providing actionable insights.""",
        llm=llm,
        verbose=True,
        memory=True,
        tools=[stock_tool]
    )

    #2. Report Writer Agent
    report_writer_agent = Agent(
        role="Financial Report Specialist",
        goal="Transform detailed financial analysis into a professional, comprehensive investment report",
        backstory="""You are an expert financial writer with a track record of creating institutional-grade research reports.
                     You excel at presenting complex financial data in a clear, structured format.
                     You always maintain professional standards while making reports accessible and actionable.
                     You're known for your clear data presentation, trend analysis, and risk assessment capabilities.""",
        llm=llm,
        verbose=True
    )

    # Analysis Task
    analysis_task = Task(
        description=f"""Analyze {symbol} stock using the stock_data_tool to fetch real-time data. Your analysis must include:

        1. Latest Trading Information (HIGHEST PRIORITY)
           - Latest stock price with specific date
           - Percentage change
           - Trading volume
           - Market status (open/closed)
           - Highlight if this is from the most recent trading session

        2. 52-Week Performance (CRITICAL)
           - 52-week high with exact date
           - 52-week low with exact date
           - Current price position relative to 52-week range
           - Calculate percentage from highs and lows

        3. Financial Deep Dive
           - Market capitalization
           - P/E ratio and other key metrics
           - Revenue growth and profit margins
           - Dividend information (if applicable)

        4. Technical Analysis
           - Recent price movements
           - Volume analysis
           - Key technical indicators

        5. Market Context
           - Business summary
           - Analyst recommendations
           - Key risk factors

        IMPORTANT: 
        - ALWAYS use the stock_data_tool to fetch real-time data
        - Begin your analysis with the latest price and 52-week data
        - Include specific dates for all price points
        - Clearly indicate when each price point was recorded
        - Calculate and show percentage changes
        - Verify all numbers with live data
        - Compare current metrics with historical trends""",
        expected_output="A comprehensive analysis report with real-time data, including all specified metrics and clear section breakdowns",
        agent=stock_analysis_agent
    )

    # Report Task
    report_task= Task(
        description=f"""Transform the analysis into a professional investment report for {symbol}. The report must:

        1. Structure:
           - Begin with an executive summary
           - Use clear section headers
           - Include tables for data presentation
           - Add emoji indicators for trends (📈 📉)

        2. Content Requirements:
           - Include timestamps for all data points
           - Present key metrics in tables
           - Use bullet points for key insights
           - Compare metrics to industry averages
           - Explain technical terms
           - Highlight potential risks

        3. Sections:
           - Executive Summary
           - Market Position Overview
           - Financial Metrics Analysis
           - Technical Analysis
           - Risk Assessment
           - Future Outlook

        4. Formatting:
           - Use markdown formatting
           - Create tables for data comparison
           - Include trend emojis
           - Use bold for key metrics
           - Add bullet points for key takeaways

        IMPORTANT:
        - Maintain professional tone
        - Clearly state all data sources
        - Include risk disclaimers
        - Format in clean, readable markdown""",
        expected_output="A professionally formatted investment report in markdown, with clear sections, data tables, and visual indicators",
        agent=report_writer_agent
    )

    # Crew Implementation
    crew = Crew(
        agents=[stock_analysis_agent, report_writer_agent],
        tasks=[analysis_task, report_task],
        process=Process.sequential,
        verbose=True
    )

    return crew

#Streamlit Application UI

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2>⚙️ Configuration</h2>
        </div>
    """, unsafe_allow_html=True)

    # API Key input with better styling
    api_key = st.text_input(
        "🔑 SambaNova API Key",
        type="password",
        value=os.getenv("SAMBANOVA_API_KEY", ""),
        help="Enter your SambaNova API key"
    )
    if api_key:
        os.environ["SAMBANOVA_API_KEY"] = api_key

    st.markdown("---")

    # Stock Symbol input with better styling
    symbol = st.text_input(
        "📊 Stock Symbol",
        value="",
        help="Enter a stock symbol (e.g., AAPL, GOOGL)"
    ).upper()

    st.markdown("---")

    # Analysis button with better styling
    analyze_button = st.button("🚀 Analyze Stock", type="primary")



#Content- display the analysis
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
    st.session_state.analysis_report = None

def is_valid_stock_symbol(symbol: str) -> bool:
    """
    Validate if the given stock symbol exists and is valid.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return bool(info and 'regularMarketPrice' in info)
    except:
        return False

if analyze_button:
    if not symbol:
        st.error("⚠️ Please enter a stock symbol")
    elif not is_valid_stock_symbol(symbol):
        st.error(f"⚠️ Invalid stock symbol: {symbol}. Please enter a valid stock symbol.")
    else:
        try:
            with st.spinner(f'🔍 Analyzing {symbol}... This may take a few minutes'):
                crew = create_agents_and_tasks(symbol)
                result = crew.kickoff()

                #Convert the crew output to string if needed
                if hasattr(result, 'raw'):
                    st.session_state.report = result.raw
                else:
                    st.session_state.report = str(result)
                    
                st.session_state.analysis_complete = True

        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")

if st.session_state.analysis_complete and st.session_state.report:
    st.markdown("""
        <div class="report-box">
            <h1>📊 Analysis Report</h1>
    """, unsafe_allow_html=True)
    
    # Display report without any formatting
    st.markdown(st.session_state.report)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Download Button
    st.download_button(
        label="📥 Download Report",
        data=st.session_state.report,
        file_name=f"stock_analysis_{symbol}_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )

# Footer
st.markdown("""
    <div style='text-align: center; padding: 20px 0; color: #7f8c8d;'>
        <p>© 2025 Financial Analyst AI. All rights reserved by Jo's Cloud AI Hub</p>
    </div>
""", unsafe_allow_html=True) 
