from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import base64

load_dotenv()

class accident_analysis(BaseModel):
    description: str = Field(description="description of the photo")
    authority: str = Field(description="authority that can resolve the issue")
    level: int = Field(description="danger level from 1 to 100")

parser = PydanticOutputParser(pydantic_object=accident_analysis)

# Read the image file
IMG_PATH = "photos\photo2.jpg"
with open(IMG_PATH, "rb") as image_file:
    image_data = image_file.read()

# Encode the image data as a base64 string
image_data_b64 = base64.b64encode(image_data).decode("utf-8")


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    timeout = None,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }
    )


user_prompt = """
Analyze the following photo, which may depict an accident, fire, or other hazardous situation.
Please provide a concise response with the following three pieces of information:
- Detailed Description:
  Provide a thorough description of the photo, including any relevant details that would be useful for the relevant authority to know.
- Recommended Authority:
  Suggest the most relevant authority to contact in order to resolve the issue, such as Police, Hospital, Fire Station, or other emergency services.
- Danger Level:
  Assign a danger level from 1 to 100, with 1 being minimal risk and 100 being extreme risk, to help prioritize the response to this situation based on its potential danger to people."
{format_instructions}
"""
# Create a message with the image
message = HumanMessage(
    content=[
        {"type": "text", "text": user_prompt.format(format_instructions=parser.get_format_instructions())},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_data_b64}"},
        },
    ],
)

# Invoke the model with the message
response = llm.invoke([message])

x = parser.parse(response.content)
print(x.description)
print(x.authority)
print(x.level)