import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog

from mcs_api import pipeline
def submit():
    error = False
    prompt = prompt_entry.get()
    access_token = access_token_entry.get()
    api_key = api_key_entry.get()
    folder_name = folder_name_entry.get()
    image_name = image_name_entry.get()
    seed = seed_entry.get()
    overwrite_file = overwrite_file_var.get()
    initialize_bucket = initialize_bucket_var.get()
    diffusion_model_url = diffusion_model_entry.get()

    # Pass these values to your backend functions
    try:
        img_link = pipeline(prompt, access_token, api_key, folder_name, image_name, seed, 
                            url=diffusion_model_url,initialize_bucket=initialize_bucket, overwrite_file=overwrite_file)
        if not img_link: raise Exception
    except Exception as e:
        error = True
        print(e)
        img_link = "Sorry, an error occurred. Please check your parameters and try again."
    output_text.delete(1.0, tk.END)  # Clear the text widget first
    output_text.insert(tk.END, img_link)
    if not error:
        response = requests.get(img_link)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((250, 250), Image.ANTIALIAS)  # You can adjust the size as needed
        img_tk = ImageTk.PhotoImage(img)
        
        img_label.config(image=img_tk)
        img_label.image = img_tk

app = tk.Tk()
app.title("Input Parameters")

# Create the labels and entry widgets for each parameter
prompt_label = ttk.Label(app, text="Prompt:")
prompt_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
prompt_entry = ttk.Entry(app, width=40)
prompt_entry.grid(column=1, row=0, padx=5, pady=5)

diffusion_model_label = ttk.Label(app, text="Link to Duffusion model(no '/' at the end):")
diffusion_model_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
diffusion_model_entry = ttk.Entry(app, width=40)
diffusion_model_entry.grid(column=1, row=1, padx=5, pady=5)

access_token_label = ttk.Label(app, text="Access Token:")
access_token_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
access_token_entry = ttk.Entry(app, width=40)
access_token_entry.grid(column=1, row=2, padx=5, pady=5)

api_key_label = ttk.Label(app, text="API Key:")
api_key_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
api_key_entry = ttk.Entry(app, width=40)
api_key_entry.grid(column=1, row=3, padx=5, pady=5)

folder_name_label = ttk.Label(app, text="MCS Bucket Name:")
folder_name_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
folder_name_entry = ttk.Entry(app, width=40)
folder_name_entry.grid(column=1, row=4, padx=5, pady=5)

image_name_label = ttk.Label(app, text="Image Name:")
image_name_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
image_name_entry = ttk.Entry(app, width=40)
image_name_entry.grid(column=1, row=5, padx=5, pady=5)

seed_label = ttk.Label(app, text="Seed")
seed_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
seed_entry = ttk.Entry(app, width=40)
seed_entry.grid(column=1, row=6, padx=5, pady=5)

# Checkbutton variables
overwrite_file_var = tk.BooleanVar()
initialize_bucket_var = tk.BooleanVar()

# Create Checkbuttons
overwrite_file_checkbtn = ttk.Checkbutton(app, text="Overwrite File", variable=overwrite_file_var)
overwrite_file_checkbtn.grid(column=0, row=7, padx=5, pady=5, sticky=tk.W)

initialize_bucket_checkbtn = ttk.Checkbutton(app, text="Initialize Bucket", variable=initialize_bucket_var)
initialize_bucket_checkbtn.grid(column=1, row=7, padx=5, pady=5, sticky=tk.W)


# Submit button
submit_btn = ttk.Button(app, text="Submit", command=submit)
submit_btn.grid(column=1, row=8, pady=20)

# Add a Text widget for the output
output_label = ttk.Label(app, text="Link to Image:")
output_label.grid(column=0, row=9, sticky=tk.W, padx=5, pady=5)
output_text = tk.Text(app, width=40, height=10, wrap=tk.WORD)
output_text.grid(column=1, row=9, padx=5, pady=5)  

# Add a Label widget to display the image
img_label = ttk.Label(app,text="Output image will be displayed here")
img_label.grid(column=0, row=10, padx=5, pady=5)


app.mainloop()
