import discord
import asyncio
import os

async def main():
    token = os.getenv('DISCORD_BOT_TOKEN')
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    
    if not token or not channel_id:
        print("❌ Missing credentials")
        return
    
    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.send("🚀 **Daily Opportunities Found!**\n\n**Startup India Seed Fund**\n💰 Up to ₹20 Lakh\n🔗 https://startupindia.gov.in\n\n**100X.VC Investment**\n💰 $25K - $200K\n🔗 https://100x.vc")
            print("✅ Messages sent!")
        await client.close()
    
    await client.start(token)

asyncio.run(main())
