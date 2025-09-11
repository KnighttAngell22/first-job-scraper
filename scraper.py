import requests
import discord
import asyncio
import os
from datetime import datetime

# Simple test scraper
def scrape_opportunities():
    print("🔍 Scraping opportunities...")
    
    # For now, just return some test data to verify everything works
    test_opportunities = [
        {
            "name": "Startup India Seed Fund",
            "provider": "Government of India",
            "deadline": "Rolling basis",
            "funding": "Up to ₹20 Lakh",
            "link": "https://www.startupindia.gov.in/"
        },
        {
            "name": "100X.VC Investment",
            "provider": "100X.VC",
            "deadline": "Ongoing",
            "funding": "$25K - $200K",
            "link": "https://www.100x.vc/"
        }
    ]
    
    print(f"✅ Found {len(test_opportunities)} opportunities")
    return test_opportunities

# Simple Discord bot
async def send_to_discord(opportunities):
    token = os.getenv('DISCORD_BOT_TOKEN')
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    
    print(f"🤖 Discord Token: {'✅ Found' if token else '❌ Missing'}")
    print(f"📺 Channel ID: {'✅ Found' if channel_id else '❌ Missing'}")
    
    if not token or not channel_id:
        print("❌ Missing Discord credentials")
        return
        
    try:
        client = discord.Client(intents=discord.Intents.default())
        
        @client.event
        async def on_ready():
            print(f"🚀 Bot connected as {client.user}")
            channel = client.get_channel(int(channel_id))
            
            if channel:
                # Send header message
                embed = discord.Embed(
                    title="🎯 Daily Opportunity Update",
                    description=f"Found {len(opportunities)} opportunities for First Job seekers!",
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
                    opp_embed.add_field(name="💰 Funding", value=opp["funding"], inline=True)
                    opp_embed.add_field(name="⏰ Deadline", value=opp["deadline"], inline=True)
                    opp_embed.add_field(name="🔗 Apply", value=f"[Click here]({opp['link']})", inline=False)
                    
                    await channel.send(embed=opp_embed)
                
                print("✅ Messages sent successfully!")
            else:
                print("❌ Channel not found")
            
            await client.close()
        
        await client.start(token)
        
    except Exception as e:
        print(f"❌ Discord error: {e}")

# Main function
async def main():
    print("🚀 Starting First Job Opportunity Scraper...")
    print(f"⏰ Running at: {datetime.now()}")
    
    # Scrape opportunities
    opportunities = scrape_opportunities()
    
    # Send to Discord
    print("📤 Sending to Discord...")
    await send_to_discord(opportunities)
    
    print("✅ Scraper completed!")

if __name__ == "__main__":
    asyncio.run(main())
