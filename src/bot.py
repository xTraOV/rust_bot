from discord.ext import commands
import discord
import logging
from src.database.db_manager import DatabaseManager
from src.utils.rcon_handler import RconHandler
from src.utils.config import Config

class DiscordKitBot(commands.Bot):
    def __init__(self, config: Config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('/'),
            intents=intents,
            description="Discord Kit Bot for Rust server group management"
        )
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DiscordKitBot')
        
        # Initialize handlers
        self.database = DatabaseManager()
        self.rcon = RconHandler(config)
        self.config = config

    async def setup_hook(self):
        # Load cogs
        await self.load_extension('src.cogs.kit_commands')
        self.logger.info('Bot cogs loaded successfully')

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.tree.sync() 