from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import base64

GOOGLE_API_KEY = "AIzaSyDwX1XxrnPMAZhUD0DRgp0K1-EvQeqMZ3Y"
#load_dotenv()

# initialize llm with ingnoring dangerous content as the imgae will include accidents and fires 
llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            timeout = None,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )

# a class to parse llm output for accident feature to the desired outputs
class accident_analysis(BaseModel):
    description: str = Field(description="description of the photo")
    authority: str = Field(description="the most relevent authority that can help in this accident or fire")
    level: int = Field(description="danger level from 1 to 100")

accident_parser = PydanticOutputParser(pydantic_object=accident_analysis)

# a class to parse llm output for eco-isseu feature to the desired outputs
class issue_analysis(BaseModel):
    description: str = Field(description="description of the photo")
    authority: str = Field(description="authority that can resolve the issue")
    priority: int = Field(description="priority level")

issue_parser = PydanticOutputParser(pydantic_object=issue_analysis)

#def get_img_data_(IMG_PATH):
#    with open(IMG_PATH, "rb") as image_file:
#        image_data = image_file.read()
#    image_data_b64 = base64.b64encode(image_data).decode("utf-8")
#    return image_data_b64

def get_img_data(image):
    """
        Encode an image object's data in base64 format.

        Args:
            image (UploadFile): An image file object uploaded by user.

        Returns:
            image_data_b64 (str): Base64-encoded image data.
    """
    image_data = image.file.read() 
    image_data_b64 = base64.b64encode(image_data).decode("utf-8")
    return image_data_b64

def analyse_accident(image, language = "En"):
    """
        Analyze an image that may depict an accident, fire, or other hazardous situation.

        Args:
            image (UploadFile): An image file object uploaded by user.
            language (str, optional): The language in which the response should be provided. Defaults to "En" (English).

        Returns:
            tuple: A tuple containing three pieces of information:
                - description (str): A thorough description of the photo, including any relevant details.
                - authority (str): The most relevant authority to contact in order to resolve the issue.
                - level (int): A danger level from 1 to 100, with 1 being minimal risk and 100 being extreme risk.
    """
    
    # Define the prompt for the image analysis, including the format instructions
    accident_prompt = """
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
    
    # If the language is Arabic, add a note to the prompt to respond in Arabic
    if language == "Ar":
        accident_prompt = "Give the respose in Arabic language\n" + accident_prompt

    # Get the base64-encoded image data
    image_data_b64 = get_img_data(image)
    
    # Create a HumanMessage object with the prompt and image
    accident_message = HumanMessage(
        content=[
            {"type": "text", "text": accident_prompt.format(format_instructions=accident_parser.get_format_instructions())},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_data_b64}"},
            },
        ],
    )

    # Invoke the LLM with the message and get the response
    response = llm.invoke([accident_message])
    
    # Parse the response and extract the description, authority, and danger level
    x = accident_parser.parse(response.content)
    return x.description, x.authority, x.level


def analyse_isuue(image, language = "En"):
    """
        Analyze an image that may depict environmental issues such as pollution, broken streetlights, and garbage collection.

        Args:
            image (UploadFile): An image file object uploaded by user.
            language (str, optional): The language in which the response should be provided. Defaults to "En" (English).

        Returns:
            tuple: A tuple containing three pieces of information:
                - description (str): A thorough description of the photo, including any relevant details.
                - authority (str): The most relevant authority to contact in order to resolve the issue.
                - priority (int): A priority level from 1 to 5, with 1 being maximum priority and 5 being minimum priority.
    """

    # Define the prompt for the image analysis, including the format instructions
    issue_prompt = """
    Analyze the following photo, which may depict environmental issues such as pollution, broken streetlights, and garbage collection.
    Please provide a concise response with the following three pieces of information:
    - Detailed Description:
    Provide a thorough description of the photo, including any relevant details that would be useful for the relevant authority to know.
    - Recommended Authority:
    Suggest the most relevant authority to contact in order to resolve the issue.
    - Priority Level:
    Assign a priority level from 1 to 5, with 1 being maximum priority and 5 being minimum priority, to help prioritize the response to this situation based on its potential danger to people and the environment."
    {format_instructions}
    """
    
    # If the language is Arabic, add a note to the prompt to respond in Arabic
    if language == "Ar":
        issue_prompt = "Give the respose in Arabic language\n" + issue_prompt

    # Get the base64-encoded image data
    image_data_b64 = get_img_data(image)
    
    # Create a HumanMessage object with the prompt and image
    issue_message = HumanMessage(
        content=[
            {"type": "text", "text": issue_prompt.format(format_instructions=issue_parser.get_format_instructions())},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_data_b64}"},
            },
        ],
    )

    # Invoke the LLM with the message and get the response
    response = llm.invoke([issue_message])
    
    # Parse the response and extract the description, authority, and priority level
    x = issue_parser.parse(response.content)
    
    return x.description, x.authority, x.priority



