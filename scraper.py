import discord
import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealOpportunityScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_unstop_hackathons(self):
        """REAL scraping from Unstop website"""
        opportunities = []
        try:
            url = "https://unstop.com/hackathons"
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find hackathon cards (actual HTML scraping)
            hackathon_cards = soup.find_all('div', class_=re.compile(r'challenge|card|opportunity', re.I))
            
            logger.info(f"Found {len(hackathon_cards)} potential hackathon elements")
            
            for card in hackathon_cards[:5]:  # Limit to prevent timeout
                try:
                    # Extract title
                    title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    
                    # Skip if not a proper title
                    if len(title) < 10 or any(skip in title.lower() for skip in ['navigation', 'menu', 'footer', 'header']):
                        continue
                    
                    # Extract link
                    link_elem = card.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = f"https://unstop.com{link}"
                    
                    # Extract any prize/reward info
                    prize_elem = card.find(text=re.compile(r'₹|prize|reward', re.I))
                    prize = prize_elem.strip() if prize_elem else "Check website"
                    
                    opportunity = {
                        "name": title,
                        "provider": "Unstop Platform",
                        "sector": "Technical",
                        "funding": prize,
                        "deadline": "Check website",
                        "link": link or url,
                        "status": "🤖 LIVE SCRAPED",
                        "source": "unstop.com"
                    }
                    
                    opportunities.append(opportunity)
                    logger.info(f"✅ Scraped: {title[:50]}...")
                    
                except Exception as e:
                    logger.error(f"Error parsing card: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping Unstop: {e}")
            # Fallback if scraping fails
            opportunities.append({
                "name": "Unstop Hackathons (Live Check Required)",
                "provider": "Unstop",
                "sector": "Technical", 
                "funding": "Various prizes",
                "deadline": "Multiple deadlines",
                "link": "https://unstop.com/hackathons",
                "status": "⚠️ SCRAPING FAILED - CHECK MANUALLY",
                "source": "unstop.com"
            })
        
        return opportunities
    
    def scrape_startup_india_live(self):
        """REAL scraping from Startup India website"""
        opportunities = []
        try:
            url = "https://www.startupindia.gov.in/"
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for any scheme/program mentions
            scheme_elements = soup.find_all(text=re.compile(r'scheme|fund|grant|support', re.I))
            
            logger.info(f"Found {len(scheme_elements)} scheme-related elements")
            
            # Extract unique schemes mentioned
            found_schemes = set()
            for element in scheme_elements[:10]:
                text = element.strip()
                if len(text) > 20 and len(text) < 200:
                    found_schemes.add(text)
            
            for i, scheme_text in enumerate(list(found_schemes)[:3]):
                opportunity = {
                    "name": f"Startup India Program #{i+1}",
                    "provider": "Government of India",
                    "sector": "Generalist",
                    "funding": "Government support available",
                    "deadline": "Check website for updates",
                    "link": url,
                    "status": "🤖 LIVE SCRAPED",
                    "description": scheme_text[:100] + "...",
                    "source": "startupindia.gov.in"
                }
                opportunities.append(opportunity)
            
        except Exception as e:
            logger.error(f"Error scraping Startup India: {e}")
            opportunities.append({
                "name": "Startup India Schemes (Live Check Required)",
                "provider": "Government of India",
                "sector": "Generalist",
                "funding": "Various schemes",
                "deadline": "Rolling",
                "link": "https://www.startupindia.gov.in/",
                "status": "⚠️ SCRAPING FAILED - CHECK MANUALLY",
                "source": "startupindia.gov.in"
            })
        
        return opportunities
    
    def scrape_devfolio_hackathons(self):
        """REAL scraping from Devfolio"""
        opportunities = []
        try:
            url = "https://devfolio.co/hackathons"
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find hackathon listings
            hackathon_links = soup.find_all('a', href=re.compile(r'hackathon|event', re.I))
            
            logger.info(f"Found {len(hackathon_links)} potential hackathon links")
            
            for link in hackathon_links[:3]:
                title = link.get_text(strip=True)
                if len(title) > 10:
                    href = link.get('href', '')
                    if not href.startswith('http'):
                        href = f"https://devfolio.co{href}"
                    
                    opportunity = {
                        "name": title,
                        "provider": "Devfolio Platform",
                        "sector": "Technical",
                        "funding": "Check event details",
                        "deadline": "Check website",
                        "link": href,
                        "status": "🤖 LIVE SCRAPED",
                        "source": "devfolio.co"
                    }
                    opportunities.append(opportunity)
            
        except Exception as e:
            logger.error(f"Error scraping Devfolio: {e}")
            opportunities.append({
                "name": "Devfolio Hackathons (Live Check Required)", 
                "provider": "Devfolio",
                "sector": "Technical",
                "funding": "Various prizes",
                "deadline": "Multiple events",
                "link": "https://devfolio.co/hackathons",
                "status": "⚠️ SCRAPING FAILED - CHECK MANUALLY",
                "source": "devfolio.co"
            })
        
        return opportunities
    
    def scrape_all_live_opportunities(self):
        """Scrape ALL sources with REAL web scraping"""
        all_opportunities = []
        
        logger.info("🔍 Starting LIVE web scraping...")
        
        # Real scraping from multiple sources
        unstop_opps = self.scrape_unstop_hackathons()
        startup_opps = self.scrape_startup_india_live()
        devfolio_opps = self.scrape_devfolio_hackathons()
        
        all_opportunities.extend(unstop_opps)
        all_opportunities.extend(startup_opps)
        all_opportunities.extend(devfolio_opps)
        
        logger.info(f"🎯 Total LIVE opportunities scraped: {len(all_opportunities)}")
        return all_opportunities

# Discord Bot
async def send_to_discord(opportunities):
    token = os.getenv('DISCORD_BOT_TOKEN')
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    
    if not token or not channel_id:
        return
    
    try:
        client = discord.Client(intents=discord.Intents.default())
        
        @client.event
        async def on_ready():
            channel = client.get_channel(int(channel_id))
            if channel:
                embed = discord.Embed(
                    title="🔍 LIVE Scraped Opportunities",
                    description=f"**{len(opportunities)} opportunities** found by scraping websites in real-time!",
                    color=0xff6b35,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="🤖 REAL AUTOMATED SCRAPING!")
                await channel.send(embed=embed)
                
                for i, opp in enumerate(opportunities, 1):
                    opp_embed = discord.Embed(
                        title=f"{i}. {opp['name'][:60]}",
                        color=0x4287f5,
                        url=opp["link"]
                    )
                    opp_embed.add_field(name="🏢 Provider", value=opp["provider"], inline=True)
                    opp_embed.add_field(name="🎯 Sector", value=opp["sector"], inline=True)
                    opp_embed.add_field(name="💰 Funding", value=opp["funding"][:40], inline=True)
                    opp_embed.add_field(name="⏰ Deadline", value=opp["deadline"], inline=True)
                    opp_embed.add_field(name="🌐 Source", value=opp["source"], inline=True)
                    opp_embed.add_field(name=opp['status'], value=f"[Visit Site]({opp['link']})", inline=True)
                    
                    await channel.send(embed=opp_embed)
            
            await client.close()
        
        await client.start(token)
        
    except Exception as e:
        logger.error(f"Discord error: {e}")

# Main function
async def main():
    logger.info("🚀 Starting REAL AUTOMATED SCRAPING")
    
    scraper = RealOpportunityScraper()
    opportunities = scraper.scrape_all_live_opportunities()
    
    await send_to_discord(opportunities)
    
    logger.info("✅ REAL scraping completed!")

if __name__ == "__main__":
    asyncio.run(main())
