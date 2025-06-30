import os
import requests

# Example script to send a message using WeChat Official Account API
# Replace APP_ID, APP_SECRET, and other placeholders with your actual configuration

APP_ID = os.getenv('WECHAT_APP_ID')  # Set your WeChat App ID in environment variables
APP_SECRET = os.getenv('WECHAT_APP_SECRET')  # Set your WeChat App Secret

# The token is obtained via the OAuth process or via the "access_token" API
ACCESS_TOKEN = os.getenv('WECHAT_ACCESS_TOKEN')

MESSAGE_TEMPLATE = {
    "touser": "OPENID",  # Replace with the receiver's openid
    "msgtype": "text",
    "text": {
        "content": "AI\u52a8\u6001\u65e5\u62a5"  # Example daily report content
    }
}

def send_message(access_token, message):
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"
    response = requests.post(url, json=message)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    if not ACCESS_TOKEN:
        print("Error: ACCESS_TOKEN not provided. Set WECHAT_ACCESS_TOKEN env variable.")
    else:
        result = send_message(ACCESS_TOKEN, MESSAGE_TEMPLATE)
        print(result)
