import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Config:
    DISCORD_BOT_TOKEN: str
    RCON_HOST: str
    RCON_PORT: str
    RCON_PASSWORD: str
    RCON_BINARY_PATH: str
    DEBUG_MODE: bool
    COMMAND_PREFIX: str

def load_config() -> Config:
    load_dotenv()
    
    return Config(
        DISCORD_BOT_TOKEN=os.getenv('DISCORD_BOT_TOKEN'),
        RCON_HOST=os.getenv('RCON_HOST'),
        RCON_PORT=os.getenv('RCON_PORT'),
        RCON_PASSWORD=os.getenv('RCON_PASSWORD'),
        RCON_BINARY_PATH=os.getenv('RCON_BINARY_PATH', '/home/rustserver/rcon_cli/rcon'),
        DEBUG_MODE=os.getenv('DEBUG_MODE', 'false').lower() == 'true',
        COMMAND_PREFIX=os.getenv('COMMAND_PREFIX', '/')
    ) 