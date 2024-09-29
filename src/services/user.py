import requests
from typing import Optional, Dict, Any


class User:
    def __init__(self, access_token: str, decoded_token: Dict[str, Any]):
        self.access_token = access_token
        self.payload = decoded_token
        self.user_info = self._get_user_info()

    def _get_user_info(self) -> Optional[Dict[str, Any]]:
        user_info_endpoint = self.payload["aud"][-1]
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(user_info_endpoint, headers=headers)
        if response.status_code == 200:
            print("access token:", self.access_token)
            print("user-info ", response.json())
            return response.json()
        return None

    def get_email(self) -> Optional[str]:
        return self.user_info.get("email") if self.user_info else None

    def get_given_name(self) -> Optional[str]:
        return self.user_info.get("given_name") if self.user_info else None

    def get_user_id(self) -> Optional[str]:
        return self.user_info.get("id") if self.user_info else None

    def get_name(self) -> Optional[str]:
        return self.user_info.get("name") if self.user_info else None

    def get_brand(self) -> Optional[str]:
        return self.user_info.get("brand") if self.user_info else None

    def get_types(self) -> Optional[list]:
        return self.user_info.get("types") if self.user_info else None
