import asyncio
from src.bot import DiscordKitBot
from src.utils.config import load_config

async def main():
    # Load configuration from environment variables
    config = load_config()
    
    # Initialize and run the bot
    bot = DiscordKitBot(config)
    await bot.start(config.DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main()) 