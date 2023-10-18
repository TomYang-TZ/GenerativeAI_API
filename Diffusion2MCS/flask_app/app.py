import os
import json
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import requests

from mcs_api import pipeline
app = Flask(__name__, template_folder='templates')
CORS(app)



@app.route("/clean", methods=["POST"])    
def clean():
    global image_link
    image_link = None
    return redirect(url_for('index'))

@app.route('/', methods=['GET','POST'])
def index():
    global image_link, prompt, diffusion_model_link, access_token, api_key, seed, bucket_name, file_name, overwrite, initialize, request
    
    image_link = None
    if request.method == 'POST':
        # Get the form values
        prompt = request.form['prompt']
        diffusion_model_link = request.form['diffusion_model_link']
        access_token = request.form['access_token']
        api_key = request.form['api_key']
        seed = request.form['seed']
        bucket_name = request.form['bucket_name']
        file_name = request.form['file_name']
        overwrite = request.form.get('overwrite',type=bool) == "on"
        initialize = request.form.get('initialize',type=bool) == "on"
        # return redirect(url_for('index'))
        # print(prompt)
        # if not prompt: return render_template('index.html')
            
        # # Call the function that returns the image link
        if prompt:
            try:
                file_path = f"{app.secret_key}.png"
                session.pop('_flashes', None)
                flash(f"Creating and uploading image...")
                image_link = generate_image_link(prompt, diffusion_model_link, access_token, api_key, seed, bucket_name, file_path, file_name, overwrite, initialize)
                os.remove(file_path)
                session.pop('_flashes', None)
                flash(f"{image_link}")
                
            except Exception as e:
                # Logging the error can be useful for debugging
                print(str(e))
                session.pop('_flashes', None)
                flash(f"An error occurred, please try again.")
                
        return redirect(url_for('index'))
    
    
    return render_template('index.html', image_link=image_link)

def generate_image_link(prompt, diffusion_model_link, access_token, api_key, seed, bucket_name, file_path, file_name, overwrite, initialize):
    # Implement the logic to interact with the desired service and generate the image link based on the parameters provided.
    # As a placeholder, this function returns a dummy link.
    image_link = pipeline(prompt=prompt, access_token=access_token, api_key=api_key, folder_name=bucket_name, file_path=file_path,image_name=file_name, 
                          seed=seed, initialize_bucket=initialize, overwrite_file=overwrite, url=diffusion_model_link)
    return image_link

if __name__ == '__main__':
    SESSION_KEY = secrets.token_urlsafe(16)   
    app.secret_key = SESSION_KEY
     
    app.run(debug=True)
