# Financial Analyst CrewAI

A powerful AI-powered stock market analysis tool that uses CrewAI to provide comprehensive financial analysis and investment reports.

## 🚀 Features

- **Multi-Agent Analysis**: Utilizes specialized AI agents for thorough stock analysis
- **Real-time Market Data**: Fetches live stock data using YFinance
- **Professional Reports**: Generates detailed investment reports with market insights
- **User-friendly Interface**: Streamlit-based web interface for easy interaction
- **Stock Symbol Validation**: Ensures accurate stock symbol input
- **Report Download**: Export analysis reports in markdown format

## 🛠️ Technologies Used

- **CrewAI**: For orchestrating AI agents and tasks
- **Streamlit**: For the web interface
- **YFinance**: For real-time stock market data
- **Sambanova LLM**: For AI-powered analysis
- **Python**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- Sambanova API key
- Required Python packages (see Installation)

## 💻 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Financial-Analyst-CrewAI.git
   cd Financial-Analyst-CrewAI
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Sambanova API key:
   ```
   SAMBANOVA_API_KEY=your_api_key_here
   ```

## 🚀 Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. In the sidebar:
   - Enter your Sambanova API key
   - Input a stock symbol (e.g., AAPL, GOOGL, MSFT)
   - Click "Analyze Stock"

4. Wait for the analysis to complete (this may take a few minutes)

5. View the generated report and download it if desired

## 🤖 AI Agents

The system uses two specialized AI agents:

1. **Stock Analysis Agent**
   - Role: Wall Street Financial Analyst
   - Expertise: Market data analysis, financial metrics interpretation
   - Tools: YFinance integration for real-time data

2. **Report Writer Agent**
   - Role: Financial Report Specialist
   - Expertise: Creating professional investment reports
   - Focus: Clear data presentation and actionable insights

## 📊 Analysis Components

The analysis includes:
- Latest trading information
- 52-week performance metrics
- Financial metrics (P/E ratio, market cap, etc.)
- Technical analysis
- Market context and risk assessment

## ⚠️ Limitations

- Requires valid Sambanova API key
- Stock market data availability depends on YFinance
- Analysis time varies based on market conditions and data availability

## 🔒 Security

- API keys are handled securely through environment variables
- No sensitive data is stored permanently


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- CrewAI for the multi-agent framework
- YFinance for market data
- Sambanova for LLM capabilities
- Streamlit for the web interface

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🔄 Updates

Stay tuned for updates and new features!
