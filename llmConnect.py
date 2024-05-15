from openai import OpenAI
import os
from dotenv import load_dotenv
import transformers
import torch
import datetime
import glob

print(datetime.datetime.now().strftime("%H:%M"))
print('program start')

# Enviroment

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print('set up chatGPT')


cl7B = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer7B = transformers.AutoTokenizer.from_pretrained(cl7B)
model7B = transformers.AutoModelForCausalLM.from_pretrained(
   cl7B,
   torch_dtype=torch.float16,
   device_map="auto",
)

pipeline7B = transformers.pipeline(
  "text-generation",
  model=cl7B,
  torch_dtype=torch.float16,
  device_map="auto"
)


print('set up codellama7b')

prompt = "Please review the following code and identify and list any errors. If errors are present, please present a corrected version of the code as well. Keep explanations short."



# Iterating over files in a folder
files = glob.glob('.\\QuixBugs\\python_programs\\*.py') # Change path and/or .py to .java when checking java files
for index, filePath in enumerate(files):
  if filePath.endswith('_test.py'):
    continue
  print(datetime.datetime.now().strftime("%H:%M"))
  print(f"Processing file {index+1}/{len(files)}: {filePath}")

  with open(filePath, 'r') as file:
    code = file.read()
  
  # gpt
  gptResponse = client.chat.completions.create(
    model='gpt-4',
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": code}
    ]
  )

  gptCorrectionPath = './llmCorrection/python/chatGPT/' + os.path.basename(filePath).replace('.py', '.txt') # Change .py to .java when checking java files
  os.makedirs(os.path.dirname(gptCorrectionPath), exist_ok=True)

  with open(gptCorrectionPath, 'a', encoding="utf-8") as gptFile:
    gptFile.write(gptResponse.choices[0].message.content + "\n----- another analysis -----\n")
  print('Iterated over gpt', end='')
  

  # CodeLlama 7B
  
  chat = [
    {"role": "user", "content": prompt + "\n\n\n" + code}
  ]
  inputs = tokenizer7B.apply_chat_template(chat, return_tensors="pt").to("cuda")
  cl7BSeq = model7B.generate(
    input_ids=inputs, 
    max_new_tokens=1500, 
    eos_token_id=tokenizer7B.eos_token_id, 
    num_return_sequences=1, 
    top_p=0.95, 
    temperature=0.3, 
    top_k=10, 
    do_sample=True
    )
  cl7BSeq = cl7BSeq[0].to("cpu")
  cl7BCorrectionPath = './llmCorrection/python/codeLlama7B/' + os.path.basename(filePath).replace('.py', '.txt') # Change .py to .java when checking java files
  os.makedirs(os.path.dirname(cl7BCorrectionPath), exist_ok=True)

  with open(cl7BCorrectionPath, 'a', encoding="utf-8") as cl7BFile:
    for seq in cl7BSeq:
      cl7BFile.write(tokenizer7B.decode(seq, skip_special_tokens=True) + " ")
    cl7BFile.write("\n----- another analysis -----\n")
  
  print('and codeLlama7B')

print(datetime.datetime.now().strftime("%H:%M"))
print('program finished')
