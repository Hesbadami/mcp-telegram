from common.client import TelegramClientManager
from common.server import mcp

@mcp.tool()
async def info() -> dict:
    """Returns information about the Telegram client.

    Args:
        None

    Returns:
        dict: A dictionary containing the phone number, and session name.
        If an error occurs, it returns a dictionary with an error message.
    """
    try:
        t = TelegramClientManager.get_client()
        if not t.is_connected():
            await t.connect()
        t.disconnect()
        return {
            "session_name": t.session.filename
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}"
        }
    
@mcp.tool()
async def get_me() -> dict:
    """Returns the current user's information.

    Args:
        None

    Returns:
        dict: A dictionary containing username and other account details.
        If an error occurs, it returns a dictionary with an error message.
    """
    try:
        t = TelegramClientManager.get_client()
        if not t.is_connected():
            await t.connect()
        
        me = await t.get_me()
        t.disconnect()
        return {
            "id": me.id,
            "username": me.username,
            "first_name": me.first_name,
            "last_name": me.last_name,
            "phone": me.phone
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}"
        }
