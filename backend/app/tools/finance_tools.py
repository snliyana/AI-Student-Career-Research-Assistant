import yfinance as yf

from langchain_core.tools import tool


@tool
def stock_info_tool(ticker: str) -> str:
    """
    Get basic stock information for a company ticker symbol.
    Example ticker: AAPL, MSFT, NVDA.
    """

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        company_name = info.get("longName", ticker)
        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")
        market_cap = info.get("marketCap")
        sector = info.get("sector")

        return f"""
Company: {company_name}
Ticker: {ticker.upper()}
Current Price: {current_price}
Previous Close: {previous_close}
Market Cap: {market_cap}
Sector: {sector}
"""

    except Exception as e:
        return (
            "Finance information is temporarily unavailable. "
            f"Error: {str(e)}"
        )