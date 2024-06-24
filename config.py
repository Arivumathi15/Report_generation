import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GOOGLE_API_KEY")
pandasai_api_key = os.getenv("PANDASAI_API_KEY")

md_filename = "report.md"
docx_filename = "Report.docx" #"analytical_report.docx"
csv_path = "D:\\learning_project\\plot_pandasai\\Amazon Sale Report.csv"
# csv_path = "D:\\learning_project\\plot_pandasai\\data_forecasting_demand_product (Master).xlsx"

os.environ['OPENAI_API_KEY'] = openai_api_key
os.environ["PANDASAI_API_KEY"] = pandasai_api_key
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {openai_api_key}"
}
gpt_model = "gpt-4o"
gemini_model = "gemini-pro"
gemini_vision = "gemini-pro-vision"
genai.configure(api_key=os.getenv("gemini_api_key"))