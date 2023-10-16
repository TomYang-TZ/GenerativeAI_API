import torch
from transformers import (AutoTokenizer, 
                          LlamaForCausalLM, 
                          AutoModelForCausalLM, 
                          AutoModel,
                          )
from flask import Flask, jsonify  


# define flask app, model path, and device
app = Flask(__name__)  
MODEL_PATH = "microsoft/phi-1_5"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  

# define inference function  
def inference(prompt):
    # load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH,trust_remote_code=True,device_map=device) 
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH,trust_remote_code=True) 

    model = torch.compile(model)
    model.eval()
    
    # process input and generate output
    inputs = tokenizer(prompt,return_tensors="pt").to(device)
    generate_ids = model.generate(**inputs, 
                                    max_new_tokens=50,
                                    ) 
    with torch.no_grad():
        result = tokenizer.decode(generate_ids[0], skip_special_tokens=True)
    
    return result  

# define api endpoint
# access inference function and return result via <API LINK>/prompt/<YOUR PROMPT>
@app.route('/prompt/<string:prompt>', methods=['GET'])
def recommend(prompt):
    print("Prompt:",prompt)
    mock_recommendation = {
        "prompt": prompt,
        "response": inference(prompt)
    }

    return jsonify(mock_recommendation)  

if __name__ == "__main__":
    # Start flask api app
    app.run(host='0.0.0.0', port=8082)