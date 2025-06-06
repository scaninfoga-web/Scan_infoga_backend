from typing import *
from pathlib import Path
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
import base64

from autoslot import Slots
import httpx

from ghunt.errors import GHuntInvalidSession

import traceback

from pathlib import Path


# class SmartObj(Slots): # Not Python 3.13 compatible so FUCK it fr fr
#     pass

class SmartObj():
    pass

class AndroidCreds(SmartObj):
    def __init__(self) -> None:
        self.master_token: str = ""
        self.authorization_tokens: Dict = {}

class GHuntCreds(SmartObj):
    """
        This object stores all the needed credentials that GHunt uses,
        such as cookies, OSIDs, keys and tokens.
    """
    
    def __init__(self, creds_path: str = "") -> None:
        print("CREDS PATHSSSS: ", creds_path)
        self.cookies: Dict[str, str] = {}
        self.osids: Dict[str, str] = {}
        self.android: AndroidCreds = AndroidCreds()

        if not creds_path:
            cwd_path = Path().home()
            ghunt_folder = cwd_path / ".malfrats/ghunt"
            if not ghunt_folder.is_dir():
                ghunt_folder.mkdir(parents=True, exist_ok=True)
            creds_path = Path(settings.GHUNT_CREDS_PATH)
        self.creds_path: str = creds_path

    def are_creds_loaded(self) -> bool:
        return all([self.cookies, self.osids, self.android.master_token])

    def load_creds(self, silent=False) -> None:
        """Loads cookies, OSIDs and tokens if they exist"""
        print("READING CREDS PATH", self.creds_path)
        if self.creds_path.resolve().is_file():
            with open(self.creds_path, 'r') as f:
                content = f.read()
                
            # Decode base64 content
            decoded_content = base64.b64decode(content)
            
            # Parse and print JSON in readable format
            json_content = json.loads(decoded_content)
            print("\nCredentials Content:")
            print(json.dumps(json_content, indent=2))
        else:
            print(f"Credentials file not found at: {self.creds_path}")
        print("Load creds called with creds path: ", Path(self.creds_path).resolve())

        print("Load creds called with creds path: ", Path(self.creds_path).resolve())
        # traceback.print_stack()


        if Path(self.creds_path).resolve().is_file():
            print("ITS A FILE")
            try:
                with open(self.creds_path, "r", encoding="utf-8") as f:
                    raw = f.read()
                data = json.loads(base64.b64decode(raw).decode())

                # print("DATA: ", data)

                self.cookies = data["cookies"]
                self.osids = {"a": "a"}
                # self.osids = data["osids"]

                self.android.master_token = data["android"]["master_token"]
                self.android.authorization_tokens = data["android"]["authorization_tokens"]

            except Exception as e:
                print("EXCEPTION BLOCK")
                raise GHuntInvalidSession("Stored session is corrupted.", str(e))
        else:
            raise GHuntInvalidSession("No stored session foundss.")
        
        if not self.are_creds_loaded():
            raise GHuntInvalidSession("Stored session is incomplete.")
        if not silent:
            print("[+] Stored session loaded !")

    def save_creds(self, silent=False):
        """Save cookies, OSIDs and tokens to the specified file."""
        data = {
            "cookies": self.cookies,
            "osids": self.osids,
            "android": {
                "master_token": self.android.master_token,
                "authorization_tokens": self.android.authorization_tokens
            }
        }

        with open(self.creds_path, "w", encoding="utf-8") as f:
            f.write(base64.b64encode(json.dumps(data, indent=2).encode()).decode())

        if not silent:
            print(f"\n[+] Creds have been saved in {self.creds_path} !")

### Maps

class Position(SmartObj):
    def __init__(self):
        self.latitude: float = 0.0
        self.longitude: float = 0.0

class MapsLocation(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.address: str = ""
        self.position: Position = Position()
        self.tags: List[str] = []
        self.types: List[str] = []
        self.cost_level: int = 0 # 1-4

class MapsReview(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.comment: str = ""
        self.rating: int = 0
        self.location: MapsLocation = MapsLocation()
        self.date: datetime = None

class MapsPhoto(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.url: str = ""
        self.location: MapsLocation = MapsLocation()
        self.date: datetime = None

### Drive
class DriveExtractedUser(SmartObj):
    def __init__(self):
        self.gaia_id: str = ""
        self.name: str = ""
        self.email_address: str = ""
        self.role: str = ""
        self.is_last_modifying_user: bool = False