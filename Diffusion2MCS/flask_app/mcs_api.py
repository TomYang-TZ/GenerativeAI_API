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
# load_dotenv()
# private_key=os.environ["PRIVATE_KEY"]
# rpc_endpoint="https://polygon-rpc.com"
# api_key = os.environ["API_KEY"]
# access_token = os.environ["ACCESS_TOKEN"]


def get_image(url='https://pgmwn8b5xu.meta.crosschain.computer',
              username='admin',password='admin1234',
              prompt='a green apple',negative_prompt='violent',
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

def initialize_client(api_key,access_token,chain="polygon.mumbai",):
    mcs_api = APIClient(api_key, chain, access_token)
    return BucketAPI(mcs_api)

def save_to_MCS_bucket(bucket_client, bucket_name="diffusion2",file_path="output.png",name="output.png",
                       overwrite_file=False,initialize_bucket=True):
    if initialize_bucket: bucket_client.create_bucket(bucket_name)   
    if overwrite_file:
        print(f"Overwriting file {name}")
        bucket_client.delete_file(bucket_name, name)
    file_data = bucket_client.upload_file(bucket_name, name , file_path) 
    if not file_data:
        print("upload failed")
        raise Exception("upload failed") 
    file_data = json.loads(file_data.to_json())
    print(file_data)
    return file_data["ipfs_url"]  
    
def pipeline(prompt, access_token, api_key, folder_name, image_name, seed,
             initialize_bucket=True,overwrite_file=False,url='https://pgmwn8b5xu.meta.crosschain.computer',file_path="output.png"):
    img = get_image(prompt=prompt,url=url,seed=seed)
    img.save(file_path)  
    bucket_client = initialize_client(api_key=api_key,access_token=access_token)

    img_link = save_to_MCS_bucket(bucket_client,initialize_bucket=initialize_bucket,overwrite_file=overwrite_file,
                                  bucket_name=folder_name,file_path=file_path,name=image_name)

    return img_link

if __name__ == '__main__':
    bucket_client = initialize_client()
    img = get_image(prompt="a blue apple")
    img.save("output.png")
    img_link = save_to_MCS_bucket(bucket_client,initialize_bucket=True,overwrite_file=True)
    print("Image Link: ", img_link)
    
    
