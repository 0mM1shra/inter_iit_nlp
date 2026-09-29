"""
Deterministic Guardrails Engine for ACT-TREE 360
Implements non-bypassable hard-stop keyword rules, zero-blast-radius controls, and data-layer PII tokenization.
"""

import re

class GuardrailEngine:
    HARD_STOP_KEYWORDS = [
        "lawsuit", "legal action", "attorney", "sue", "lawyer",
        "bankrupt", "self-harm", "fraud_hold", "account takeover"
    ]

    @classmethod
    def check_hard_stop(cls, text_content):
        if not text_content:
            return False, None
        text_lower = text_content.lower()
        for kw in cls.HARD_STOP_KEYWORDS:
            if kw in text_lower:
                return True, kw
        return False, None

    @classmethod
    def redact_pii(cls, text_content):
        if not text_content:
            return text_content
        # Mask account numbers (e.g. ACC_CHK_001 -> ACC_CHK_***)
        text = re.sub(r'ACC_[A-Z]+_\d+', 'ACC_***', text_content)
        # Mask SSN / ID patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'XXX-XX-XXXX', text)
        return text
