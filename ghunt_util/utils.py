import re
import base64
import json
import httpx
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from asgiref.sync import async_to_sync
import os
import sys

# Add GHunt to system path
ghunt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GHunt')
sys.path.append(ghunt_path)

from ghunt import globals as gb
from ghunt.helpers import auth
from ghunt.helpers.utils import get_httpx_client
from ghunt.objects.base import GHuntCreds
from ghunt.modules.email import hunt as email_hunt


def clean_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r'\x1b\[(0|1;)?\d*(;\d*)?[mK]')
    return ansi_escape.sub('', text)

class GHuntError(Exception):
    """Base exception for GHunt errors"""
    pass

class GHuntAuthenticationError(GHuntError):
    """Raised when authentication fails"""
    pass

class GHuntEmailInfoError(GHuntError):
    """Raised when email info retrieval fails"""
    pass

async def login_with_base64_creds(encoded_creds: str) -> Tuple[bool, str]:
    try:
        gb.init_globals()
        
        try:
            data = json.loads(base64.b64decode(encoded_creds).decode())
            oauth_token = data.get("oauth_token")
            if not oauth_token:
                raise GHuntAuthenticationError("Invalid authentication data: oauth_token not found")
        except Exception as e:
            raise GHuntAuthenticationError(f"Failed to decode authentication data: {str(e)}")
        
        as_client = get_httpx_client()
        ghunt_creds = GHuntCreds()
        ghunt_creds.android.authorization_tokens = {}
        
        try:
            master_token, services, owner_email, owner_name = await auth.android_master_auth(
                as_client, oauth_token
            )
        except Exception as e:
            await as_client.aclose()
            return False, f"Authentication failed: {str(e)}"
        
        ghunt_creds.android.master_token = master_token
        
        try:
            ghunt_creds.cookies = {"a": "a"}
            ghunt_creds.osids = {"a": "a"}
            await auth.gen_cookies_and_osids(as_client, ghunt_creds)
        except Exception as e:
            await as_client.aclose()
            return False, f"Failed to generate cookies/OSIDs: {str(e)}"
        
        try:
            ghunt_creds.save_creds()
        except Exception as e:
            await as_client.aclose()
            return False, f"Failed to save credentials: {str(e)}"
        
        await as_client.aclose()
        return True, "Authentication successful!"
        
    except GHuntAuthenticationError as e:
        raise e
    except Exception as e:
        raise GHuntAuthenticationError(f"An unexpected error occurred: {str(e)}")

async def get_email_info(email_address: str, json_file: Optional[str] = None) -> Dict[str, Any]:
    gb.init_globals()
    as_client = get_httpx_client()
    
    try:
        ghunt_creds = await auth.load_and_auth(as_client)
        json_path = Path(json_file) if json_file else None
        
        import io
        from contextlib import redirect_stdout
        output_buffer = io.StringIO()
        
        try:
            with redirect_stdout(output_buffer):
                await email_hunt(as_client, email_address, json_path)
        except SystemExit:
            raise GHuntEmailInfoError("Target not found or invalid email address")
        except Exception as e:
            raise GHuntEmailInfoError(str(e))
        
        raw_output = clean_ansi_codes(output_buffer.getvalue())

        result = {
            "success": True,
            "email": email_address,
            "profile": {
                "gaiaId": None,
                "hasCustomProfilePicture": False,
                "hasCustomCover": False,
                "lastEdited": None,
                "userTypes": []
            },
            "googleChat": {
                "entityType": None,
                "customerId": None
            },
            "googlePlus": {
                "isEnterpriseUser": False
            },
            "playGames": {
                "hasProfile": False,
                "username": None,
                "playerId": None,
                "avatarUrl": None
            },
            "maps": {
                "profileUrl": None,
                "hasReviews": False
            },
            "calendar": {
                "isPublic": False,
                "hasEvents": False
            }
        }
        
        # Parse the output to extract key information
        output_lines = raw_output.split('\n')
        
        # Extract profile information
        for i, line in enumerate(output_lines):
            line = line.strip()
            
            # Profile info
            if "Default profile picture" in line:
                result["profile"]["hasCustomProfilePicture"] = False
            elif "Custom profile picture" in line and i + 1 < len(output_lines):
                result["profile"]["hasCustomProfilePicture"] = True
                result["profile"]["profilePictureUrl"] = output_lines[i+1].replace("=>", "").strip()
            
            if "Default cover picture" in line:
                result["profile"]["hasCustomCover"] = False
            elif "Custom cover picture" in line and i + 1 < len(output_lines):
                result["profile"]["hasCustomCover"] = True
                result["profile"]["coverPictureUrl"] = output_lines[i+1].replace("=>", "").strip()
            
            if "Last profile edit :" in line:
                result["profile"]["lastEdited"] = line.split("Last profile edit :")[1].strip()
            
            if "Gaia ID :" in line:
                result["profile"]["gaiaId"] = line.split("Gaia ID :")[1].strip()
            
            if line.startswith("-") and "(The user is a" in line:
                user_type = line.split("(")[0].strip("- ").strip()
                result["profile"]["userTypes"].append(user_type)
            
            # Google Chat
            if "Entity Type :" in line:
                result["googleChat"]["entityType"] = line.split("Entity Type :")[1].strip()
            
            if "Customer ID :" in line and "Not found" not in line:
                result["googleChat"]["customerId"] = line.split("Customer ID :")[1].strip()
            
            # Google Plus
            if "Entreprise User :" in line:
                result["googlePlus"]["isEnterpriseUser"] = line.split("Entreprise User :")[1].strip().lower() == "true"
            
            # Play Games
            if "Found player profile" in line:
                result["playGames"]["hasProfile"] = True
                # Next few lines contain player details
                for j in range(i, min(i+10, len(output_lines))):
                    if "Username :" in output_lines[j]:
                        result["playGames"]["username"] = output_lines[j].split("Username :")[1].strip()
                    elif "Player ID :" in output_lines[j]:
                        result["playGames"]["playerId"] = output_lines[j].split("Player ID :")[1].strip()
                    elif "Avatar :" in output_lines[j]:
                        result["playGames"]["avatarUrl"] = output_lines[j].split("Avatar :")[1].strip()
            
            # Maps
            if "Profile page :" in line:
                result["maps"]["profileUrl"] = line.split("Profile page :")[1].strip()
            elif "No review." in line:
                result["maps"]["hasReviews"] = False
            
            # Calendar
            if "Public Google Calendar found" in line:
                result["calendar"]["isPublic"] = True
                # Check if there are events
                for j in range(i, min(i+5, len(output_lines))):
                    if "No recent events found" in output_lines[j]:
                        result["calendar"]["hasEvents"] = False
                        break
                    elif "has events" in output_lines[j].lower():
                        result["calendar"]["hasEvents"] = True
                        break

        return result
        
    except GHuntEmailInfoError as e:
        raise e
    except Exception as e:
        raise GHuntEmailInfoError(str(e))