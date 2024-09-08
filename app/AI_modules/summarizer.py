import numpy as np

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv

def summarize(feedbacks_list):
    feedbacks = "\n*".join(feedbacks_list)
    feedbacks_doc = Document(page_content=feedbacks)
    
    prompt = """
    You will be given a series of user feedbacks , The feedbacks will be enclosed in triple backticks (```)
    Your goal is to give a verbose summary of what said in those feedbacks.
    The finall summary you give me should be coherance and easy to grasp the whole feedbacks.

    ```{text}```
    VERBOSE SUMMARY:
    """
    prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
    chain = load_summarize_chain(
        llm=llm,
        prompt=prompt_template
        )
    output = chain.invoke([feedbacks_doc])
    summary = output['output_text']
    return summary


# TEST
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-pro")
En_feedbacks_list = [
    "I absolutely love the new feature, it's exactly what I've been waiting for!",
    "The UI is really confusing, I've been trying to figure it out for hours but I still can't get the hang of it.",
    "Can you please add more customization options, I want to be able to personalize my experience?",
    "The app is so slow, it takes forever to load and it's really frustrating.",
    "I wish I could sort my data by date, it would make it so much easier to track my progress.",
    "The customer support is really helpful, they responded to my question right away and solved my problem.",
    "I'm not sure what this feature does, can you please provide more instructions or a tutorial?",
    "Can you please make the font size bigger, I'm having trouble reading the text?",
    "I'm getting an error message when I try to login, it says my password is incorrect but I know it's right.",
    "The app is really easy to use, I was able to figure it out right away.",
    "I don't like the new design, it's too cluttered and overwhelming.",
    "Can you please add a dark mode, it would be easier on my eyes?",
    "I'm having trouble with the payment process, it keeps saying my card is declined but I know it's valid.",
    "The app is really helpful for my business, it's saved me so much time and effort.",
    "I wish I could export my data to CSV, it would make it so much easier to analyze and report on."
]

Ar_feedbacks_list = [
    "الخدمة كانت ممتازة، ولكنني واجهت مشكلة في الدفع عبر الإنترنت.",
    "منتج رائع، ولكنني أتمنى لو كان هناك خيار لاختيار لون آخر.",
    "المنتج وصلني في الوقت المحدد، ولكنني لم أستلم أي رسالة تأكيد.",
    "الخدمة كانت سريعة جدا، ولكنني واجهت مشكلة في التواصل مع فريق الدعم.",
    "المنتج كان جيدا، ولكنني أتمنى لو كان هناك خيار لشراء كميات أكبر.",
    "الخدمة كانت رائعة، ولكنني واجهت مشكلة في إرجاع المنتج.",
    "المنتج كان رائعا، ولكنني أتمنى لو كان هناك خيار لاختيار موديل آخر.",
    "الخدمة كانت ممتازة، ولكنني واجهت مشكلة في الدفع عبر البطاقة الائتمانية.",
    "المنتج وصلني في الوقت المحدد، ولكنني لم أستلم أي رسالة تأكيد.",
    "الخدمة كانت سريعة جدا، ولكنني واجهت مشكلة في التواصل مع فريق الدعم.",
    "المنتج كان جيدا، ولكنني أتمنى لو كان هناك خيار لشراء كميات أكبر.",
    "الخدمة كانت رائعة، ولكنني واجهت مشكلة في إرجاع المنتج.",
    "المنتج كان رائعا، ولكنني أتمنى لو كان هناك خيار لاختيار موديل آخر.",
    "الخدمة كانت ممتازة، ولكنني واجهت مشكلة في الدفع عبر الإنترنت.",
    "المنتج وصلني في الوقت المحدد، ولكنني لم أستلم أي رسالة تأكيد.",
    "الخدمة كانت سريعة جدا، ولكنني واجهت مشكلة في التواصل مع فريق الدعم."
]
