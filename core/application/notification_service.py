import requests
from config.ntfy_config import CHANNEL

def notify(msg):
    try:
        requests.post(
            f"https://ntfy.sh/{CHANNEL}",
                data=msg,
                headers={
                    "Title": "Streamlit",
                    "Tags": "+1"
                }
        )
    except Exception:
        pass