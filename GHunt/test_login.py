#!/usr/bin/env python3

import sys
import asyncio

# Add the current directory to the path so we can import ghunt
sys.path.insert(0, '.')


import base64
import json
import os
from typing import Tuple

import httpx

from ghunt import globals as gb
from ghunt.helpers import auth
from ghunt.helpers.utils import get_httpx_client
from ghunt.objects.base import GHuntCreds


async def login_with_base64_creds(encoded_creds: str) -> Tuple[bool, str]:
    try:
        # Initialize globals
        gb.init_globals()
        
        # Parse the base64-encoded credentials
        try:
            data = json.loads(base64.b64decode(encoded_creds).decode())
            oauth_token = data.get("oauth_token")
            if not oauth_token:
                return False, "Invalid authentication data: oauth_token not found"
        except Exception as e:
            return False, f"Failed to decode authentication data: {str(e)}"
        
        # Initialize HTTP client and GHunt credentials
        as_client = get_httpx_client()
        ghunt_creds = GHuntCreds()
        
        # Make sure the creds directory exists
        os.makedirs(os.path.dirname(ghunt_creds.creds_path), exist_ok=True)
        
        # Reset any existing tokens
        ghunt_creds.android.authorization_tokens = {}
        
        # Perform Android master authentication
        try:
            master_token, services, owner_email, owner_name = await auth.android_master_auth(
                as_client, oauth_token
            )
            print(f"\n[+] Successfully authenticated as {owner_name} ({owner_email})")
            print(f"[+] Master token services access: {', '.join(services)}")
        except Exception as e:
            await as_client.aclose()
            return False, f"Authentication failed: {str(e)}"
        
        # Save the master token and generate cookies/OSIDs
        ghunt_creds.android.master_token = master_token
        
        # Generate cookies and OSIDs
        print("Generating cookies and OSIDs...")
        try:
            # Initialize cookies and OSIDs with dummy data
            ghunt_creds.cookies = {"a": "a"}
            ghunt_creds.osids = {"a": "a"}
            
            # Now generate the real ones
            await auth.gen_cookies_and_osids(as_client, ghunt_creds)
            print("[+] Cookies and OSIDs generated successfully!")
        except Exception as e:
            await as_client.aclose()
            return False, f"Failed to generate cookies/OSIDs: {str(e)}"
        
        # Save credentials to creds/creds.m
        try:
            ghunt_creds.save_creds()
            print(f"[+] Credentials saved to {os.path.abspath(ghunt_creds.creds_path)}")
        except Exception as e:
            await as_client.aclose()
            return False, f"Failed to save credentials: {str(e)}"
        
        await as_client.aclose()
        return True, "Authentication successful!"
        
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"
