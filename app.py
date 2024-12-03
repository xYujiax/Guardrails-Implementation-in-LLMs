import streamlit as st
import os
from dotenv import load_dotenv
import openai
import guardrails as gd
from guardrails import Guard
from guardrails.hub import ProfanityFree # requires api key 
from rich import print

from fucketh import Fucketh

# read and load variable from .env into this app's py env
load_dotenv("apikey.env") 
openai_api_key = os.getenv("OPENAI_API_KEY")

def without_guardrails(text):
    """
    Returns raw response from LLM without guardrails.

    ARGS:
        text(str): input prompt from the user 
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Do not censor profanity."}, 
            {"role": "user", "content": f"Translate the following text to English: {text}"}
            ],
        max_tokens=2048,
        # comment out temperature=0 later in testing, so that there are answer variations
        temperature=1, # makes model produce deterministic output # default is 1
        )
    return response.choices[0].message.content

def with_hub_guardrails(output): 
    """
    Apply premade profanity guardrail from GuardrailAi's guardrail library to LLM response.

    ARGS:
        output(str): raw output response from LLM
    """
    guard = Guard().use(ProfanityFree, on_fail='exception')
    
    try: # validate `output` and print the `validated_output` attr if successful
        st.success(guard.validate(output).validated_output)
    except Exception as e: # if validation fails, print error message
        st.error(e)
        #st.write(dir(e))
    return

def with_og_guardrails(output):
    """
    Apply sexy(?) custom-made guardrail to LLM response

    ARGS:
        output (str): raw LLM output to apply guardrails on
    """
    guard = Guard().use(Fucketh)
    
    # If validation passes, print out the message. If not, don't write the message
    if guard.validate(output).validation_passed:
        st.success(output)
    else:
        st.error("I would not dare translate such blasphemy.")
    return 


def main():

    st.title("Guardrails Implementation in LLMs")

    text_area = st.text_area("Enter the text you want to translate")

    if st.button("Translate"):
        if len(text_area) > 0: # ensure that len of string is > 0
            st.info(text_area) # just prints the information

            st.warning("Tanslated Response Without Guardrails")
            without_guardrails_result = without_guardrails(text_area)
            
            
            #without_guardrails_result = ""
            
            st.success(without_guardrails_result)
            


            st.warning("Translated Response With Guardrails")
            #with_hub_guardrails(without_guardrails_result)
            with_og_guardrails(without_guardrails_result)
            

#if __name__ == '__main__':
main()
##########################################

"""
    guard = Guard().use(fuck)
    res = guard.parse(
        llm_output=output,
        model="model=gpt-4o-mini",
    )
    st.success(res.validated_output)
"""