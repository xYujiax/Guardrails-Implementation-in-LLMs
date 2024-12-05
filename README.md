# Guardrails-Implementation-in-Generative-AI-Apps
Guardrails implementation in Generative AI powered apps. This app will show you how to put Guardrails in LLMs.
NOTE: This replication project requires an OpenAI AND Guardrails AI API key.

1. To run this application in your virtual environment, please run the following line in terminal:
```pip install -r requirements.txt```
This contains the following dependencies:


      alt-profanity-check
      
      openai
      
      guardrails-ai   
      
      tf-keras 
      
      transformers
      
      pandas
      
      tabulate

      If you do not already have streamlit installed, please also run ```pip install streamlit```


3. [Obtain API key from OpenAI](https://openai.com/index/openai-api/) **(costs $5 - pls email me if you want me to send you my api-key instead)**
   * After obtaining API key, create a file ```apikey.env``` and enter the following line in said file:
     
     ```OPENAI_API_KEY = "replace-with-openai-api-key"```
     
     
4. We will be also be a profanity guardrail from Guardrails AI's opensource library. [Please obtain an API key (this one's free!)](https://hub.guardrailsai.com/keys)
   * After obtaining API key, please run the following in terminal:
     
     ```guardrails configure```
     
     This will prompt you to input a token. When that happens, paste your Guardrails AI API key (surrounded by quotation marks) into terminal and hit ```Enter```
     
     
5. Now we have all the dependencies required to start our streamlit application! In terminal, type the following:
   ```streamlit run app.py```
   You should be able to open the app on your local browser now.
   
   
7. Please play with the app! If you input something profane to be translated, the default guardrail should catch that and raise and error. The custom guardrail should only catch profanity if used in a negative context. **Note, every time you press the ```translate``` button, your input is sent to OpenAI and eats away at your OpenAI credits, so beware.

8. I do not recommend replicating my actual research results through brute force because that would take 60+ OpenAI API calls, and that costs time and money. Instead, I saved LLM outputs into these csv files, and conducted analysis on them in a jupyter notebook. Here is a description of files relevant to my analysis:
* prompt.json - specific user prompts sent to the LLM to achieve a response 
* test_default.csv - 60 LLM outputs under a system prompt that censors profanity
* test_custom.csv - 60 LLM outputs under a system prompt that does not censor profanity
* analysis.ipynb - A jupyter notebook with analyzing accuracy of how the default profanity guardrail from Guardrails AI performs on the outputs in each .csv file. Same analysis for my custom guardrail
