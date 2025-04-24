import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials
ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")  # format: urn:li:person:xxxxx
print(ACCESS_TOKEN)
print('-'*40)
print(PERSON_URN)

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

def post_to_linkedin(content):
    api_url = "https://api.linkedin.com/v2/ugcPosts"
    payload = {
        "author": PERSON_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    return response.status_code, response.text


# print(post_to_linkedin('Post for testing purpose!!'))
