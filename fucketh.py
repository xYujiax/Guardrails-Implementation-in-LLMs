from typing import Any, Dict

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
    ErrorSpan
)

from profanity_check import predict
from transformers import pipeline

def good_sentiment(text):
    """
    Detects sentiment of text (excluding) profanity?? Will have to see performance
    """
    #sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    sentiment_pipeline = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    sentiment = sentiment_pipeline(text) 
    return sentiment


@register_validator(name="profanity-check-special", data_type="string") 
class Fucketh(Validator): 

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        prediction = predict([value])
        if prediction[0] == 1: # 1 is profane, 0 is not
            if good_sentiment(value)[0]['label'] == 'NEGATIVE':
                return FailResult(
                    error_message=f"{value} contains profanity. "
                    f"Please return profanity-free output.",
                    fix_value="",
                    error_spans=[
                        ErrorSpan(
                            start=0,
                            end=len(value),
                            reason="This text contains profanity."
                        )
                    ]
                )
        return PassResult()
   