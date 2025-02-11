import json
import os
from typing import Optional, Dict
import asyncio
from pathlib import Path
import logging

class DatabaseManager:
    def __init__(self):
        self.data_file = Path("data/users.json")
        self.data_lock = asyncio.Lock()
        self._ensure_data_file_exists()
        
    def _ensure_data_file_exists(self):
        """Ensure the data directory and file exist"""
        self.data_file.parent.mkdir(exist_ok=True)
        if not self.data_file.exists():
            self.data_file.write_text("{}")

    async def _load_data(self) -> Dict:
        """Load data from the JSON file"""
        async with self.data_lock:
            try:
                return json.loads(self.data_file.read_text())
            except json.JSONDecodeError:
                return {}

    async def _save_data(self, data: Dict):
        """Save data to the JSON file"""
        async with self.data_lock:
            self.data_file.write_text(json.dumps(data, indent=2))

    async def register_user(self, discord_id: str, steam_id: str) -> bool:
        """Register a user's Steam ID in the database"""
        try:
            # Implementation depends on your database setup
            # This is a placeholder for the actual database operation
            await self.db.execute(
                "INSERT OR REPLACE INTO users (discord_id, steam_id, verified) VALUES (?, ?, ?)",
                (discord_id, steam_id, False)
            )
            return True
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return False

    async def get_user_data(self, discord_id: str) -> Optional[Dict]:
        """Get user data by Discord ID"""
        data = await self._load_data()
        return data.get(discord_id)

    async def verify_user(self, discord_id: str) -> bool:
        """Mark a user as verified"""
        data = await self._load_data()
        if discord_id not in data:
            return False
        
        data[discord_id]['verified'] = True
        await self._save_data(data)
        return True

    async def set_group_status(self, discord_id: str, in_group: bool) -> bool:
        """Update user's group status"""
        data = await self._load_data()
        if discord_id not in data:
            return False
        
        data[discord_id]['in_group'] = in_group
        await self._save_data(data)
        return True

    async def remove_user(self, discord_id: str) -> bool:
        """Remove a user from the database"""
        data = await self._load_data()
        if discord_id not in data:
            return False
        
        del data[discord_id]
        await self._save_data(data)
        return True

    async def get_steam_id(self, discord_id: str) -> Optional[str]:
        """Get Steam ID for a Discord user"""
        data = await self._load_data()
        user_data = data.get(discord_id)
        return user_data['steam_id'] if user_data else None

    async def is_verified(self, discord_id: str) -> bool:
        """Check if a user is verified"""
        data = await self._load_data()
        user_data = data.get(discord_id)
        return user_data.get('verified', False) if user_data else False

    async def is_in_group(self, discord_id: str) -> bool:
        """Check if a user is in the group"""
        data = await self._load_data()
        user_data = data.get(discord_id)
        return user_data.get('in_group', False) if user_data else False 