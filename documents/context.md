# Discord Kit Bot

## Overview
A Discord bot that adds players to an in-game permission group ("discord.group") after Steam ID verification. Once added to the group, players can access specific kits in-game through the group's permissions.

## Core Features
- Steam ID verification system
- RCON integration for group management
- One-time group assignment per verified Steam ID
- Steam ID to Discord user linking
- Secure credential management through environment variables

## Technical Details
- Built using Discord.py
- Uses RCON-CLI for server commands
- RCON binary location: `/home/rustserver/rcon_cli/rcon`
- Requires Discord server administrator permissions
- Stores user data (Discord ID, Steam ID) and verification status
- Database integration for tracking verified users

## Command Execution
### RCON Implementation
```bash
/home/rustserver/rcon_cli/rcon -a ADDRESS:PORT -p PASSWORD -t web "c.usergroup add {steamid} discord.group"
```

## Commands
- `/register [steam_id]` - Link Steam ID to Discord account
- `/kit` - Adds user to "discord.group" in-game (requires registered Steam ID)
- `/check_status` - Check if user is already in the group
- `/admin verify [discord_user] [steam_id]` - Manually verify a user's Steam ID (Admin only)
- `/admin revoke [discord_user]` - Remove user from the group (Admin only)

## Environment Variables (.env)
The bot uses a .env file to securely store sensitive credentials. This file should be located in the root directory.

### .env File Structure
```env
# Discord Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# RCON Configuration
RCON_HOST=your_server_ip
RCON_PORT=your_rcon_port
RCON_PASSWORD=your_rcon_password

# RCON Binary Path
RCON_BINARY_PATH=/home/rustserver/rcon_cli/rcon

# Optional Configuration
DEBUG_MODE=false
COMMAND_PREFIX=/
```

### Environment Variables Description
- `DISCORD_BOT_TOKEN`: Your Discord bot's authentication token
- `RCON_HOST`: IP address of your Rust server
- `RCON_PORT`: RCON port number (usually different from game port)
- `RCON_PASSWORD`: RCON password for server authentication
- `RCON_BINARY_PATH`: Full path to the RCON CLI executable
- `DEBUG_MODE`: Enable/disable debug logging (optional)
- `COMMAND_PREFIX`: Command prefix for bot commands (optional)

## Required Permissions
### Discord Bot Permissions
- Read Messages
- Send Messages
- View Channel
- Manage Roles

### File System Permissions
- Execute permission on `/home/rustserver/rcon_cli/rcon`
- Read/Write permissions for bot's working directory
- Restricted permissions on .env file (chmod 600)

## Setup Requirements
1. Discord Bot Token
2. Game Server RCON Configuration:
   - Server IP
   - RCON Port
   - RCON Password
3. Database configuration for storing:
   - User Discord IDs
   - Steam IDs
   - Group assignment status
4. Linux server environment setup
5. Verify RCON CLI binary permissions

## User Flow
1. User joins Discord server
2. User registers their Steam ID using `/register`
3. User uses `/kit` command
4. Bot verifies Steam ID and executes RCON command
5. User can now access designated kits in-game

## Installation Steps
1. Clone the repository
2. Create and configure .env file:
   ```bash
   cp .env.example .env
   nano .env  # Edit with your credentials
   chmod 600 .env
   ```
3. Ensure RCON binary is executable:
   ```bash
   chmod +x /home/rustserver/rcon_cli/rcon
   ```
4. Test RCON connectivity:
   ```bash
   /home/rustserver/rcon_cli/rcon -a ADDRESS:PORT -p PASSWORD "status"
   ```
5. Verify "discord.group" exists in-game
6. Configure proper kit permissions for the group

## Security Considerations
- Secure storage of RCON credentials
- Steam ID validation before execution
- Rate limiting for commands
- Logging of all RCON operations
- Regular audit of file permissions
- Proper ownership of RCON binary
- Never commit .env file to version control
- Add .env to .gitignore
- Keep a template .env.example file in version control
- Regularly rotate RCON password
- Use strong, unique passwords

## Maintenance
1. Regular database backups
2. Monitor RCON command execution logs
3. Update Discord.py and other dependencies
4. Review and rotate credentials periodically
5. Monitor bot performance and resource usage

## Troubleshooting
1. Check RCON connectivity
2. Verify file permissions
3. Ensure all environment variables are set
4. Check Discord bot token validity
5. Verify "discord.group" exists in-game
6. Review bot logs for errors

## Support
- Report issues through GitHub issues
- Contact server administrator for RCON-related issues
- Check Discord Developer Portal for bot token issues
