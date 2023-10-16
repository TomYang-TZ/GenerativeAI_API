import os
import json
import requests
import io
import base64

from PIL import Image
from dotenv import load_dotenv

from swan_mcs import APIClient,BucketAPI

""" Install the following mcs packages before running this script
pip install python-mcs-sdk  
git clone https://github.com/filswan/python-mcs-sdk.git
cd python-mcs-sdk
git checkout main
pip install -r requirements.txt
"""

### Setup credentials for MCS in .env file  
load_dotenv()
private_key=os.environ["PRIVATE_KEY"]
rpc_endpoint="https://polygon-rpc.com"
api_key = os.environ["API_KEY"]
access_token = os.environ["ACCESS_TOKEN"]


def get_image(url='https://pgmwn8b5xu.meta.crosschain.computer',
              username='admin',password='admin1234',
              prompt='a green apple',negative_prompt='red',
              sampler_name='DPM++ 2M Karras',
              seed=985454925,cfg_scale=7,steps=20,width=512,height=512):
    # Encode the username and password in Base64
    credentials = f'{username}:{password}'
    credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    # construct payload as a dictionary
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": sampler_name,
        "seed": seed,
        "cfg_scale": cfg_scale,
        "steps": steps,
        "width": width,
        "height": height,
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload, headers=headers)  
    r = response.json()  
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    return image

def initialize_client(chain="polygon.mumbai"):
    mcs_api = APIClient(api_key, chain, access_token)
    return BucketAPI(mcs_api)

def save_to_MCS_bucket(bucket_client, bucket_name="diffusion2",file_path="output.png",
                       overwrite_file=False,initialize_bucket=True):
    if initialize_bucket: bucket_client.create_bucket(bucket_name)   
    if overwrite_file:
        print(f"Overwriting file {file_path}")
        bucket_client.delete_file(bucket_name, file_path)
    file_data = bucket_client.upload_file(bucket_name, file_path , file_path) 
    if not file_data:
        print("upload failed")
        return 
    file_data = json.loads(file_data.to_json())
    
    bucket_link = f"https://multichain.storage/my_buckets_detail?folder={bucket_name}&bucket_uuid={file_data['bucket_uid']}"
    return file_data["ipfs_url"],bucket_link  
    

    


if __name__ == '__main__':
    bucket_client = initialize_client()
    img = get_image(prompt="a blue apple")
    img.save("output.png")
    try:
        img_link, bucket_link = save_to_MCS_bucket(bucket_client,initialize_bucket=True,overwrite_file=False)
    except:
        img_link,bucket_link = None,None
    print("Image Link: ", img_link)
    print("Bucket Link: ", bucket_link)
    
