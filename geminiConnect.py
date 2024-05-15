# TODO(developer) Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login

import vertexai
from vertexai.generative_models import GenerativeModel, Part
import datetime
import glob
import os

print(datetime.datetime.now().strftime("%H:%M"))
print('1')

# Initialize Vertex AI
vertexai.init(project="lithe-optics-422207-j7", location="us-central1")
# Load the model
# multimodal_model = GenerativeModel(model_name=gemini-1.0-pro-vision-001)
multimodal_model = GenerativeModel(model_name="gemini-pro")


prompt = "Please review the following code and identify and list any errors. If errors are present, please present a corrected version of the code as well."

for i in range(5):
  files = glob.glob('.\\Python Files\\*.py')
  for index, filePath in enumerate(files):
    if filePath.endswith('Node.py'):
      continue
    print(datetime.datetime.now().strftime("%H:%M"))
    print(f"Processing file {index+1}/{len(files)}: {filePath}")

    with open(filePath, 'r') as file:
      code = file.read()
    
    response = multimodal_model.generate_content([prompt, code])
    

    correctionPath = './llmCorrection/python/gemini/' + os.path.basename(filePath).replace('.py', '.txt')
    os.makedirs(os.path.dirname(correctionPath), exist_ok=True)
    with open(correctionPath, 'a') as geminiFile:
      geminiFile.write(response.text + "\n----- another analysis -----\n")


print("finished")