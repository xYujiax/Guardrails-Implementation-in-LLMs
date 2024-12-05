import streamlit as st
import os
from dotenv import load_dotenv
import openai
import guardrails as gd
from guardrails import Guard
from guardrails.hub import ProfanityFree # requires api key 
from rich import print
import pandas as pd
import time

from fucketh import Fucketh

# read and load variable from .env into this app's py env
load_dotenv("apikey.env") 
openai_api_key = os.getenv("OPENAI_API_KEY")

def load_prompts(file):
    """
    Loads prompts from a json file if given.
    RETURNS:
        prompt_df (df): df of prompts
    """
    prompt_df = pd.read_json(file)

    # Save table of prompts and outputs to markdown file
    markdown_df = prompt_df.to_markdown()      
    # Output the markdown table on streamlit app
    st.markdown(markdown_df)

    return prompt_df

def test_prompts(prompt_df):
    """
    Batch process LLM outputs on given prompts. For DATA section in Q1 Report.
    ARGS:
        prompt_df (df): df of prompts to process
    RETURNS:

    """
    prompts = prompt_df["prompt"] #list of prompts to process
    output_df = pd.DataFrame() #initialize df to store outputs
    for prompt in prompts:
        outputs = [without_guardrails(prompt) for _ in range(10)] #get 10 outputs for each prompt
        output_df[prompt] = outputs
    # Save table of prompts and outputs to markdown file to
    output_df.to_csv("default.csv") 
    st.markdown(output_df.to_markdown())

    return output_df

def test_custom(file):
    """
    Test custom guardrail on LLM output.
    ARGS:
        file (str): csv file containing LLM outputs to test on
    """
    custom_df = pd.read_csv(file, index_col=0) #load csv file
    result_df = pd.DataFrame()
    print("DEBUGGING")
    for col in custom_df.columns:
        result_df[col] = custom_df[col].map(with_og_guardrails) #apply custom guardrail on each output
    result_df.to_csv("custom_results.csv")
    return "Success"

def without_guardrails(text):
    """
    Returns raw response from LLM without guardrails.

    ARGS:
        text(str): input prompt from the user 
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
            "content": """You are a translator. Be succinct, focusing on clarity and brevity.
            Ensure that the intent of the original text is preserved accurately.
            Avoid unnecessary details and wordiness.
            Accurately translate profanity."""
            },
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
    RETURNS:
        passed(bool): True if validation passes, False otherwise
    """
    guard = Guard().use(ProfanityFree, on_fail='exception')
    passed = False #flag to check if validation passes
    
    try: # validate `output` and print the `validated_output` attr if successful
        st.success(guard.validate(output).validated_output)
        passed = True
    except Exception as e: # if validation fails, print error message
        st.error(e)
        #st.write(dir(e))
    return passed

def with_og_guardrails(output):
    """
    Apply sexy(?) custom-made guardrail to LLM response.
    Allows profanity to be translated if it's said in a positive context.

    ARGS:
        output (str): raw LLM output to apply guardrails on
    RETURNS:
        passed (bool): True if validation passes, False otherwise
    """
    guard = Guard().use(Fucketh) #initialize custom guardrail
    passed = False #flag to check if validation passes
    
    # If validation passes, print out the message. If not, don't write the message
    if guard.validate(output).validation_passed:
        st.success(output)
        passed = True
    else:
        st.error("I would not dare translate such blasphemy.")
    return passed

def main():
    '''
    try: # for testing prompts on analysis.ipynb
        prompt_df = load_prompts("prompts.json") #load prompts into df
        results = test_prompts(prompt_df) #test prompts on LLM
    except FileNotFoundError:
        print("No prompts file found. Input prompts manually on app.")
    test_custom("test_custom.csv") #test custom guardrail on LLM output
    '''
    st.title("Guardrails Implementation in LLMs")

    text_area = st.text_area("Enter the text you want to translate")

    if st.button("Translate"):
        if len(text_area) > 0: # ensure that len of string is > 0
            st.info(text_area) # just prints the information

            st.warning("Tanslated Response Without Guardrails")
            without_guardrails_result = without_guardrails(text_area)
            
            st.success(without_guardrails_result)

            st.warning("Translated Response With Guardrails AI Guardrail")
            with_hub_guardrails(without_guardrails_result)
            st.warning("Translated Response With Custom Guardrail Allowing Positive Profanity")
            with_og_guardrails(without_guardrails_result)
            

#if __name__ == '__main__':
main()
##########################################

