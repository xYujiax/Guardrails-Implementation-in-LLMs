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

@register_validator(name="profanity-check-special", data_type="string")
class Fucketh(Validator):

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        prediction = predict([value])
        if prediction[0] == 1:
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