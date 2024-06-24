# Function to encode the image
import os, yaml, base64, requests, subprocess
import google.generativeai as genai
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from config import headers
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd

from pandasai import SmartDataframe
import config as cg

temperature = 0

def read_prompts_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('prompts')

def read_data(path: str):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".xlsx"):
        return pd.read_excel(path, sheet_name= 'Sheet1')
    
def generate_report(model_select, prompt, temperature):
    if model_select == "gemini":
        generated_report = generate_report_gemini(model = cg.gemini_model, prompt = prompt, temperature=temperature)
        # result = generated_report.text
    
    elif model_select == "gpt":
        generated_report = generate_report_gpt4o('user', prompt, num_token=2000, temperature=temperature)
        # print(generated_report)
        # result = generated_report["choices"][0]["message"]["content"]

    return generated_report

def generate_chart(model_select, data, prompt):
    if model_select == "pandasai":
        sdf1 = SmartDataframe(data, config={"save_charts" : 'True', 
                                "save_charts_path" : "D:\\learning_project\\plot_pandasai\\img",
                                "open_charts": "False"
                                })
        sdf1.chat(prompt)
    elif model_select == "langchain":
        pandas_agent_func(data, temp=0.3)
    return "Chart generated"

def pandas_agent_func(dataframe, temp):
    print(dataframe.info())
    agent = create_pandas_dataframe_agent(llm=ChatOpenAI(temperature=temp), 
                                          df=dataframe, 
                                          verbose=True,
                                          agent_type=AgentType.OPENAI_FUNCTIONS)
    return agent


def generate_report_gemini(model, prompt, temperature):
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt, temperature = temperature)
    
    return response.text


def generate_report_gpt4o(role, content, num_token, temperature = 0): 
    # Prompt for the agent to perform the operation
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": role,
            "content": content
            }
        ],
        "max_tokens": num_token,
        "temperature": temperature
        }
   
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    output = response.json()

    return output["choices"][0]["message"]["content"]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
  

def save_as_docx(md_file, output_file):
    subprocess.run(f"pandoc -s {md_file} -o {output_file}")
    if os.path.exists(md_file):
        os.remove(md_file)


def save_chart_query(query):
    q_s = 'Just save the charts/plots localy and include the save file names in your response.'
    query += '. '+ q_s
    return query

# # Function to add parsed HTML content to the Word document
# def add_html_to_docx(soup, doc):
#     for element in soup:
#         if element.name == 'h1':
#             paragraph = doc.add_heading(level=1)
#             run = paragraph.add_run(element.get_text())
#             run.bold = True
#         elif element.name == 'h2':
#             paragraph = doc.add_heading(level=2)
#             run = paragraph.add_run(element.get_text())
#             run.bold = True
#         elif element.name == 'h3':
#             paragraph = doc.add_heading(level=3)
#             run = paragraph.add_run(element.get_text())
#             run.bold = True
#         elif element.name == 'h4':
#             paragraph = doc.add_heading(level=4)
#             run = paragraph.add_run(element.get_text())
#             run.bold = True
#         elif element.name == 'p':
#             doc.add_paragraph(element.get_text())
#         elif element.name == 'ul' or element.name == 'ol':
#             for li in element.find_all('li'):
#                 doc.add_paragraph(f"- {li.get_text()}", style='ListBullet')
#         elif element.name == 'strong':
#             paragraph = doc.add_paragraph()
#             run = paragraph.add_run(element.get_text())
#             run.bold = True
#         elif element.name == 'em':
#             paragraph = doc.add_paragraph()
#             run = paragraph.add_run(element.get_text())
#             run.italic = True








