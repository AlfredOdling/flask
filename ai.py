from langchain.document_loaders import YoutubeLoader, WebBaseLoader, TextLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

def generateText(type: str, link: str, text: str, prompt: str):
    if type == "youtube":
        loader = YoutubeLoader.from_youtube_url(link, add_video_info=False)
        result = loader.load()

    elif type == "website":
        loader = WebBaseLoader(link)
        result = loader.load()

    elif type == "text":
        loader = WebBaseLoader(text)
        result = loader.load()


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(result)

    prompt_template = f"{prompt} from this text: ""{text}"". RESULT:"
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT)
    content = chain({"input_documents": texts}, return_only_outputs=True)

    prompt_template2 = f"Write a short title of max 15 words that describes the following: ""{text}"" TITLE:"
    PROMPT2 = PromptTemplate(template=prompt_template2, input_variables=["text"])

    chain2 = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=PROMPT2, combine_prompt=PROMPT2)
    title = chain2({"input_documents": texts}, return_only_outputs=True)

    return { "content": content, "title": title }