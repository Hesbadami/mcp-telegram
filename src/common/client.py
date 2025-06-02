import sys
import logging
import os
from typing import Optional, Type, Union

from common.config import TELEGRAM_CFG

import telethon
from telethon import TelegramClient
import qrcode
from io import StringIO

# Configure Telethon logging to go to stderr only
telethon_logger = logging.getLogger('telethon')
telethon_logger.setLevel(logging.WARNING)  # Reduce verbosity, only show warnings and errors

# Create a handler that outputs to stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
))

# Remove any existing handlers and add our stderr handler
telethon_logger.handlers.clear()
telethon_logger.addHandler(stderr_handler)
telethon_logger.propagate = False  # Don't propagate to root logger

def display_url_as_qr(url):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create a string representation of the QR code for terminal display
    f = StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    qr_string = f.read()
    
    # Display the QR code in terminal (using stderr to avoid MCP issues)
    print("\nScan this QR code to login to Telegram:", file=sys.stderr)
    print(qr_string, file=sys.stderr)
    print(f"Or use this URL: {url}", file=sys.stderr)

class TelegramClientManager:
    _instance: Optional[TelegramClient] = None

    @classmethod
    async def is_authenticated(cls) -> bool:
        """
        Check if the current Telegram session is authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        client = cls.get_client()
        
        # Make sure the client is connected
        if not client.is_connected():
            await client.connect() 
        
        # Check if the user is authorized
        is_authed = await client.is_user_authorized()
        if not is_authed:
            qr_login = await client.qr_login()
            display_url_as_qr(qr_login.url)

            try:
                await qr_login.wait()

            except telethon.errors.SessionPasswordNeededError as e:
                print("Session password is required. Please enter it in the terminal.", file=sys.stderr)
                password = input("Password: ")
                await client.sign_in(password=password)
                # Check if the login with password was successful
                is_authed = await client.is_user_authorized()
                if is_authed:
                    print("Successfully authenticated with password.", file=sys.stderr)
                else:
                    print("Authentication failed even after password entry.", file=sys.stderr)
                
            except Exception as e:
                print(f"An unexpected error occurred during authentication: {e}", file=sys.stderr)
                is_authed = False
        
        else:
            print("Already authenticated with Telegram.", file=sys.stderr)

        await client.disconnect()
        
        # Clear the instance after authentication so a fresh one is created in the new event loop
        cls._instance = None
            
        return is_authed

    @classmethod
    def get_client(cls) -> TelegramClient:
        # Always create a fresh client instance to avoid event loop issues
        try:
            telegram_class: Type[TelegramClient] = TelegramClient
            connection_params = {
                "api_id": TELEGRAM_CFG["api_id"],
                "api_hash": TELEGRAM_CFG["api_hash"],
                "session": TELEGRAM_CFG["session_name"]
            }

            return telegram_class(**connection_params)

        except Exception as e:
            print(f"An unexpected error occurred while creating Telegram client: {e}", file=sys.stderr)
            raise

    @classmethod
    def get_singleton_client(cls) -> TelegramClient:
        """Get or create a singleton client (use only within the same event loop)"""
        if cls._instance is None:
            cls._instance = cls.get_client()
        return cls._instance