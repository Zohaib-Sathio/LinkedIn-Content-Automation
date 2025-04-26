import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials
ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")  # format: urn:li:person:xxxxx
# print(ACCESS_TOKEN)
# print('-'*40)
# print(PERSON_URN)

# headers = {
#     "Authorization": f"Bearer {ACCESS_TOKEN}",
#     "Content-Type": "application/json",
#     "X-Restli-Protocol-Version": "2.0.0"
# }


def post_to_linkedin_with_images(text, image_files):
    uploaded_assets = []

    # Step 1: Upload each image separately
    for image_file in image_files:
        upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        upload_request_body = {
            "registerUploadRequest": {
                "owner": PERSON_URN,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
            }
        }

        upload_response = requests.post(upload_url, headers=headers, json=upload_request_body)
        upload_data = upload_response.json()

        asset = upload_data["value"]["asset"]
        upload_url_actual = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]

        # Upload the actual image bytes
        image_bytes = image_file.read()
        upload_image_headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/octet-stream"
        }
        requests.put(upload_url_actual, headers=upload_image_headers, data=image_bytes)

        uploaded_assets.append(asset)

    # Step 2: Create the post with all images
    post_url = "https://api.linkedin.com/v2/ugcPosts"

    media_entries = [{
        "status": "READY",
        "description": {"text": "Image"},
        "media": asset,
        "title": {"text": "Image"}
    } for asset in uploaded_assets]

    post_body = {
        "author": PERSON_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "IMAGE",
                "media": media_entries
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    post_headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    post_response = requests.post(post_url, headers=post_headers, json=post_body)
    return post_response.status_code, post_response.text
