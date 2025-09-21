import requests
import yaml
from typing import Dict, Optional


class APIClient:
    def __init__(self):
        with open("config/config.yaml") as f:
            self.config = yaml.safe_load(f)

    def get_user(self, user_id: int) -> Optional[Dict]:
        url = f"{self.config['base_url']}/users/{user_id}"
        try:
            response = requests.get(url, timeout=self.config['timeout'])
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return None

    # 其他API方法...