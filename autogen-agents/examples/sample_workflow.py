"""
Sample workflow demonstrating the interaction between financial news agents.
"""
import asyncio
import json
import os
from typing import Dict

# Import agents
from src.agents.planner_agent import PlannerAgent
from src.agents.google_news_agent import GoogleNewsAgent
from src.agents.yahoo_finance_agent import YahooFinanceAgent
from src.agents.writer_agent import WriterAgent

async def load_config() -> Dict:
    """Load agent configuration from JSON file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'agent_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

async def main():
    """Run a sample workflow demonstrating agent interaction."""
    # Load configuration
    config = await load_config()
    
    # Initialize agents
    planner = PlannerAgent(config['planner_agent'])
    google_news = GoogleNewsAgent(config['google_news_agent'])
    yahoo_finance = YahooFinanceAgent(config['yahoo_finance_agent'])
    writer = WriterAgent(config['writer_agent'])
    
    try:
        # Get workflow from planner
        workflow = await planner.create_workflow()
        print("Workflow created:", workflow)
        
        # Fetch news and market data concurrently
        news_task = asyncio.create_task(google_news.get_latest_news())
        market_task = asyncio.create_task(yahoo_finance.fetch_market_data())
        shock_task = asyncio.create_task(yahoo_finance.detect_market_shocks())
        
        # Wait for all data gathering tasks
        news_data = await news_task
        market_data = await market_task
        shock_events = await shock_task
        
        # Prepare data for article generation
        article_data = {
            "news": news_data,
            "market_data": market_data,
            "shock_events": shock_events,
            "timestamp": "2024-01-27T20:00:00Z"  # Example timestamp
        }
        
        # Generate and validate article
        article = await writer.generate_article(article_data)
        validation = await writer.validate_article(article)
        
        if validation["is_valid"]:
            # Format the article
            formatted_article = await writer.format_article(article)
            print("\nGenerated Article:")
            print("Title:", formatted_article["title"])
            print("Content:", formatted_article["content"][:200] + "...")
            print("\nSources:", formatted_article["sources"])
        else:
            print("\nArticle validation failed:")
            print("Errors:", validation["errors"])
            print("Warnings:", validation["warnings"])
        
    except Exception as e:
        print(f"Error in workflow: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())