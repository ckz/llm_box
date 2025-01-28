import autogen
from typing import Any, Dict, List
import os
from datetime import datetime
import asyncio
import yfinance as yf
from serpapi.google_search import GoogleSearch

#从 OPENROUTER 获取到的API KEY做测试：
api_key="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"

#从 SERPAPI 获取到的API KEY做测试：（每月免费搜索100次）
SERPAPI_KEY = "1b7dcd7bba5426fd30a6f2baba427d41d6c17dd85fabaa136ff9ecb6110cb314"

# Configure models
config_list = [
    {
        'model': 'deepseek/deepseek-chat',
        'api_key': api_key,
        'base_url': "https://openrouter.ai/api/v1",
    }
]

async def get_stock_data(symbol: str) -> Dict[str, Any]:
    """
    Get real stock market data for a given symbol with improved error handling
    """
    try:
        stock = yf.Ticker(symbol)
        price_info = stock.history(period='1d')
        if not price_info.empty:
            current_price = price_info['Close'].iloc[-1]
        else:
            current_price = None

        info = stock.info

        return {
            "price": current_price,
            "volume": info.get("regularMarketVolume"),
            "pe_ratio": info.get("forwardPE"),
            "market_cap": info.get("marketCap"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {str(e)}")
        return {
            "price": None,
            "volume": None,
            "pe_ratio": None,
            "market_cap": None,
            "error": str(e)
        }

async def get_news(query: str) -> List[Dict[str, str]]:
    """Get recent news articles about a company"""
    params = {
        "engine": "google_news",
        "q": query,
        "gl": "us",
        "hl": "en",
        "api_key": SERPAPI_KEY,
        "num": 3
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        news_items = []
        for article in results.get("news_results", []):
            title = article.get("title", "").strip()
            source = article.get("source", {})
            source_name = source.get("name", "")
            authors = source.get("authors", [])
            author_text = f"By {', '.join(authors)}" if authors else ""

            snippet = article.get("snippet", "")
            description = article.get("description", "")
            link_text = article.get("link_text", "")

            summary_candidates = [s for s in [snippet, description, link_text] if s]
            summary = max(summary_candidates, key=len) if summary_candidates else title

            date_str = article.get("date", "")
            try:
                if date_str:
                    date_obj = datetime.strptime(date_str.split(",")[0], "%m/%d/%Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                else:
                    formatted_date = datetime.now().strftime("%Y-%m-%d")
            except:
                formatted_date = date_str

            news_items.append({
                "title": title,
                "date": formatted_date,
                "summary": f"{summary} {author_text}".strip(),
                "source": source_name
            })

        return news_items

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

# Create agents
planner = autogen.AssistantAgent(
    name="planner",
    llm_config={"config_list": config_list},
    system_message="""你是一名研究规划协调员。
    通过委派给专业智能体来协调市场研究：
    - 金融分析师：负责股票数据分析
    - 新闻分析师：负责新闻收集和分析
    - 撰写员：负责编写最终报告
    始终先发送你的计划，然后再移交给适当的智能体。
    每次只能移交给一个智能体。
    当研究完成时使用 TERMINATE 结束。"""
)

financial_analyst = autogen.AssistantAgent(
    name="financial_analyst",
    llm_config={"config_list": config_list},
    system_message="""你是一名金融分析师。
    使用 get_stock_data 工具分析股市数据。
    提供金融指标的深入见解。
    分析完成后务必移交回规划协调员。"""
)

news_analyst = autogen.AssistantAgent(
    name="news_analyst",
    llm_config={"config_list": config_list},
    system_message="""你是一名新闻分析师。
    使用 get_news 工具收集和分析相关新闻。
    总结新闻中的关键市场见解。
    分析完成后务必移交回规划协调员。"""
)

writer = autogen.AssistantAgent(
    name="writer",
    llm_config={"config_list": config_list},
    system_message="""你是一名财经报告撰写员。
    将研究发现编译成清晰简洁的报告。
    撰写完成后务必移交回规划协调员。"""
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, financial_analyst, news_analyst, writer],
    messages=[],
    max_round=50
)

manager = autogen.GroupChatManager(groupchat=groupchat)

# Start the conversation
user_proxy.initiate_chat(
    manager,
    message="为特斯拉(TSLA)股票进行市场研究，并用中文回答"
)