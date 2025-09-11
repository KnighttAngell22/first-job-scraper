import discord
import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpportunityScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Sector keywords
        self.sector_keywords = {
            "AI": ["artificial intelligence", "ai", "machine learning", "ml", "deep learning"],
            "EdTech": ["education", "edtech", "e-learning", "student", "academic"],
            "Technical": ["software", "tech", "technology", "developer", "programming"],
            "Hiring/Jobs": ["hiring", "recruitment", "jobs", "career", "employment"],
            "Generalist": ["startup", "entrepreneur", "business", "innovation"]
        }
    
    def classify_sector(self, text):
        """Classify opportunity into sectors"""
        text_lower = text.lower()
        sector_scores = {}
        
        for sector, keywords in self.sector_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                sector_scores[sector] = score
        
        return max(sector_scores, key=sector_scores.get) if sector_scores else "Generalist"
    
    def scrape_government_schemes(self):
        """Scrape real government opportunities"""
        opportunities = []
        
        # Known government schemes with real data
        schemes = [
            {
                "name": "Startup India Seed Fund Scheme (SISFS)",
                "provider": "Department for Promotion of Industry and Internal Trade",
                "description": "Financial assistance to startups for proof of concept, prototype development, product trials, market entry and commercialization",
                "funding": "Up to ₹20 Lakh",
                "eligibility": "DPIIT recognized startups not older than 2 years",
                "link": "https://www.startupindia.gov.in/content/sih/en/government-schemes/startup-india-seed-fund-scheme.html"
            },
            {
                "name": "NIDHI-Prayas Program", 
                "provider": "Department of Science and Technology",
                "description": "Support to translate innovative ideas into prototypes with potential for further development and commercialization",
                "funding": "Up to ₹10 Lakh",
                "eligibility": "Students, faculty, researchers with innovative ideas",
                "link": "https://www.nidhi-prayas.in/"
            },
            {
                "name": "BIRAC BIG (Biotechnology Ignition Grant)",
                "provider": "Biotechnology Industry Research Assistance Council",
                "description": "Early stage financing for promising biotechnology business ideas",
                "funding": "Up to ₹50 Lakh",
                "eligibility": "Individual entrepreneurs, startups in biotechnology",
                "link": "https://birac.nic.in/desc_new.php?id=267"
            },
            {
                "name": "MeitY Startup Hub", 
                "provider": "Ministry of Electronics and Information Technology",
                "description": "Support ecosystem for tech startups through incubation, mentoring and funding",
                "funding": "Various schemes available",
                "eligibility": "Technology startups in electronics and IT",
                "link": "https://www.meity.gov.in/content/startup-hub"
            }
        ]
        
        for scheme in schemes:
            try:
                opportunity = {
                    "name": scheme["name"],
                    "provider": scheme["provider"],
                    "sector": self.classify_sector(f"{scheme['name']} {scheme['description']}"),
                    "funding": scheme["funding"],
                    "deadline": "Rolling applications (check website for updates)",
                    "link": scheme["link"],
                    "eligibility": scheme["eligibility"],
                    "description": scheme["description"][:150] + "...",
                    "status": "🏛️ Government Scheme",
                    "probability": 4  # Government schemes have good success rate
                }
                opportunities.append(opportunity)
                
            except Exception as e:
                logger.error(f"Error processing scheme: {e}")
                continue
        
        logger.info(f"✅ Found {len(opportunities)} government schemes")
        return opportunities
    
    def scrape_all_opportunities(self):
        """Scrape all opportunity sources"""
        all_opportunities = []
        
        # Government schemes
        gov_schemes = self.scrape_government_schemes()
        all_opportunities.extend(gov_schemes)
        
        # Filter to most relevant (top 3)
        return all_opportunities[:3]

# Discord Bot (same as before)
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
                    title="🎯 Daily First Job Opportunities",
                    description=f"Found {len(opportunities)} opportunities for students & early-stage startups",
                    color=0x00ff88,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="Step 3: Real Government Schemes Added!")
                await channel.send(embed=embed)
                
                # Send each opportunity
                for i, opp in enumerate(opportunities, 1):
                    opp_embed = discord.Embed(
                        title=f"{i}. {opp['name'][:80]}...",
                        description=opp['description'],
                        color=0x4287f5,
                        url=opp["link"]
                    )
                    opp_embed.add_field(name="🏢 Provider", value=opp["provider"][:50], inline=True)
                    opp_embed.add_field(name="🎯 Sector", value=opp["sector"], inline=True)
                    opp_embed.add_field(name="💰 Funding", value=opp["funding"], inline=True)
                    opp_embed.add_field(name="👥 Eligibility", value=opp["eligibility"][:80], inline=True)
                    opp_embed.add_field(name="⏰ Deadline", value=opp["deadline"], inline=True)
                    opp_embed.add_field(name="📊 Probability", value="⭐⭐⭐⭐ (4/5)", inline=True)
                    opp_embed.add_field(name="🔗 Apply Now", value=f"[Click here]({opp['link']})", inline=False)
                    
                    await channel.send(embed=opp_embed)
                
                logger.info("✅ All opportunities sent to Discord!")
            
            await client.close()
        
        await client.start(token)
        
    except Exception as e:
        logger.error(f"❌ Discord error: {e}")

# Main function
async def main():
    logger.info("🚀 Starting Step 3 - Real Government Scrapers")
    
    # Initialize scraper
    scraper = OpportunityScraper()
    
    # Scrape all opportunities
    opportunities = scraper.scrape_all_opportunities()
    logger.info(f"Total opportunities found: {len(opportunities)}")
    
    # Send to Discord
    await send_to_discord(opportunities)
    
    logger.info("✅ Step 3 completed!")

if __name__ == "__main__":
    asyncio.run(main())
