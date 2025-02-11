from discord import app_commands
from discord.ext import commands
import discord
import logging

class KitCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('KitCommands')

    @app_commands.command(
        name="kit",
        description="Add yourself to the kit group if you have registered and verified your Steam ID"
    )
    async def kit(self, interaction: discord.Interaction):
        # Defer the response since this might take a moment
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Get user data
            user_data = await self.bot.database.get_user_data(str(interaction.user.id))
            
            if not user_data:
                await interaction.followup.send(
                    "❌ You need to register your Steam ID first using `/register`",
                    ephemeral=True
                )
                return
            
            if not user_data.get('verified', False):
                await interaction.followup.send(
                    "❌ Your Steam ID needs to be verified first",
                    ephemeral=True
                )
                return
            
            # Check if already in group
            steam_id = user_data['steam_id']
            if await self.bot.rcon.check_group_membership(steam_id):
                await interaction.followup.send(
                    "✅ You are already in the kit group!",
                    ephemeral=True
                )
                return
            
            # Add to group
            success = await self.bot.rcon.add_to_group(steam_id)
            if success:
                # Update database
                await self.bot.database.set_group_status(str(interaction.user.id), True)
                await interaction.followup.send(
                    "✅ Successfully added you to the kit group!",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Failed to add you to the kit group. Please try again later or contact an admin.",
                    ephemeral=True
                )
                
        except Exception as e:
            self.logger.error(f"Error in kit command: {e}")
            await interaction.followup.send(
                "❌ An error occurred while processing your request. Please try again later.",
                ephemeral=True
            )

    @app_commands.command(
        name="register",
        description="Register your Steam ID with the bot"
    )
    async def register(
        self, 
        interaction: discord.Interaction, 
        steam_id: str
    ):
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Basic Steam ID validation (you might want to enhance this)
            if not steam_id.isdigit() or len(steam_id) < 17:
                await interaction.followup.send(
                    "❌ Invalid Steam ID format. Please provide a valid Steam ID.",
                    ephemeral=True
                )
                return
            
            # Store the Steam ID in the database
            success = await self.bot.database.register_user(
                str(interaction.user.id),
                steam_id
            )
            
            if success:
                await interaction.followup.send(
                    "✅ Steam ID registered successfully! Please verify your Steam ID to use the kit command.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Failed to register Steam ID. Please try again later or contact an admin.",
                    ephemeral=True
                )
                
        except Exception as e:
            self.logger.error(f"Error in register command: {e}")
            await interaction.followup.send(
                "❌ An error occurred while processing your request. Please try again later.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(KitCommands(bot)) 