import discord
import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpportunityScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def test_scraping(self):
        """Test basic web scraping"""
        opportunities = []
        
        try:
            # Test scraping a simple website
            url = "https://www.startupindia.gov.in/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                opportunities.append({
                    "name": "Startup India Portal - Live Data",
                    "provider": "Government of India",
                    "sector": "Generalist", 
                    "funding": "Various schemes available",
                    "deadline": "Rolling basis",
                    "link": url,
                    "status": "✅ Successfully scraped"
                })
                logger.info("✅ Successfully tested web scraping!")
            else:
                logger.error(f"❌ Failed to access website: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Scraping error: {e}")
            # Fallback data if scraping fails
            opportunities.append({
                "name": "Startup India Seed Fund (Fallback)",
                "provider": "DPIIT",
                "sector": "Generalist",
                "funding": "Up to ₹20 Lakh", 
                "deadline": "Rolling applications",
                "link": "https://www.startupindia.gov.in/",
                "status": "⚠️ Using fallback data"
            })
        
        return opportunities

# Discord Bot
async def send_to_discord(opportunities):
    token = os.getenv('DISCORD_BOT_TOKEN')
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    
    if not token or not channel_id:
        logger.error("❌ Missing Discord credentials")
        return
    
    try:
        client = discord.Client(intents=discord.Intents.default())
        
        @client.event
        async def on_ready():
            channel = client.get_channel(int(channel_id))
            if channel:
                # Header message
                embed = discord.Embed(
                    title="🎯 Daily Opportunity Update",
                    description=f"Found {len(opportunities)} opportunities (Step 2 Test)",
                    color=0x00ff88,
                    timestamp=datetime.now()
                )
                await channel.send(embed=embed)
                
                # Send each opportunity
                for opp in opportunities:
                    opp_embed = discord.Embed(
                        title=opp["name"],
                        color=0x4287f5,
                        url=opp["link"]
                    )
                    opp_embed.add_field(name="🏢 Provider", value=opp["provider"], inline=True)
                    opp_embed.add_field(name="🎯 Sector", value=opp["sector"], inline=True)
                    opp_embed.add_field(name="💰 Funding", value=opp["funding"], inline=True)
                    opp_embed.add_field(name="⏰ Deadline", value=opp["deadline"], inline=True)
                    opp_embed.add_field(name="📊 Status", value=opp["status"], inline=True)
                    opp_embed.add_field(name="🔗 Apply", value=f"[Click here]({opp['link']})", inline=False)
                    
                    await channel.send(embed=opp_embed)
                
                logger.info("✅ Messages sent to Discord!")
            
            await client.close()
        
        await client.start(token)
        
    except Exception as e:
        logger.error(f"❌ Discord error: {e}")

# Main function
async def main():
    logger.info("🚀 Starting Step 2 - Basic Scraper Test")
    
    # Initialize scraper
    scraper = OpportunityScraper()
    
    # Test scraping
    opportunities = scraper.test_scraping()
    logger.info(f"Found {len(opportunities)} opportunities")
    
    # Send to Discord
    await send_to_discord(opportunities)
    
    logger.info("✅ Step 2 completed!")

if __name__ == "__main__":
    asyncio.run(main())
