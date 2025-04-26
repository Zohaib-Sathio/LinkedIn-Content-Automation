
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
# print(os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.3)


def draft_post(idea):
    template = """
    You are a professional LinkedIn content writer.
    Take the following idea and turn it into an engaging and thoughtful LinkedIn post:
    Also do not add "**" in the post content.
    ---
    {idea}
    ---
    Respond with only the LinkedIn-ready content.
    """

    prompt = PromptTemplate(input_variables=["idea"], template=template)

    linkedin_chain = LLMChain(llm=model, prompt=prompt)

    draft_post = linkedin_chain.run(idea)
    # print(draft_post)

    # print('-'*20)
    return draft_post
    

def refined_post(draft_post):
    # Refinement prompt
    refinement_template = """
    You are an expert LinkedIn content editor. Also do not add ** or * in the post content.

    Take the following draft post and enhance it by:
    - Adding a hook at the start (curiosity, story, or bold statement)
    - Making the content concise and scannable (short paras, no fluff)
    - Simplifying complex sentences
    - Formatting it with line breaks, bold ideas, and clear flow

    --- 
    {draft_post}
    ---

    Respond with only the final polished LinkedIn post, ready to publish.
    """

    refinement_prompt = PromptTemplate(input_variables=["draft_post"], template=refinement_template)

    refinement_chain = LLMChain(llm=model, prompt=refinement_prompt)

    # Run refinement
    refined_post = refinement_chain.run(draft_post)
    # print(refined_post)
    return refined_post
