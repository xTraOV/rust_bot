import asyncio
import logging
from typing import Optional
from src.utils.config import Config

class RconHandler:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger('RconHandler')
        
    async def execute_command(self, command: str) -> Optional[str]:
        """Execute an RCON command and return the response"""
        try:
            # Construct the RCON command with credentials
            rcon_cmd = [
                self.config.RCON_BINARY_PATH,
                "-a", f"{self.config.RCON_HOST}:{self.config.RCON_PORT}",
                "-p", self.config.RCON_PASSWORD,
                "-t", "web",
                command
            ]
            
            # Execute the command
            process = await asyncio.create_subprocess_exec(
                *rcon_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Get output
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                self.logger.error(f"RCON command failed: {stderr.decode()}")
                return None
                
            return stdout.decode().strip()
            
        except Exception as e:
            self.logger.error(f"Error executing RCON command: {e}")
            return None
    
    async def add_to_group(self, steam_id: str) -> bool:
        """Add a user to the discord.group"""
        command = f'c.usergroup add {steam_id} discord.group'
        result = await self.execute_command(command)
        return result is not None
    
    async def remove_from_group(self, steam_id: str) -> bool:
        """Remove a user from the discord.group"""
        command = f'c.usergroup remove {steam_id} discord.group'
        result = await self.execute_command(command)
        return result is not None
    
    async def check_group_membership(self, steam_id: str) -> bool:
        """Check if a user is in the discord.group"""
        command = f'c.usergroup list {steam_id}'
        result = await self.execute_command(command)
        return result is not None and 'discord.group' in result 
    
    async def verify_steam_id(self, steam_id: str, verification_code: str) -> bool:
        """Verify a user's Steam ID using the verification code"""
        try:
            # Get player info from server
            command = f'playerinfo {steam_id}'
            result = await self.execute_command(command)
            
            if not result:
                return False
                
            # The verification code should be set as the player's name or some other
            # verifiable information on the server. This implementation might need
            # to be adjusted based on your specific verification requirements.
            return verification_code in result
            
        except Exception as e:
            self.logger.error(f"Error verifying Steam ID: {e}")
            return False 