from typing import Dict, Any

class IdentityVerificationService:
    """
    Identity Document Verification Service Interface.
    Manages identity document attachment and processing boundary.
    """

    @classmethod
    def process_identity_document(
        cls,
        provided_name: str,
        document_type: str = "identity_document",
        image_b64: str = None
    ) -> Dict[str, Any]:
        """
        Processes attached document for artisan profile.
        """
        clean_name = provided_name.strip() if provided_name else "Artisan"
        
        arta_response_ta = (
            f"உங்கள் அடையாள ஆவணம் இணைக்கப்பட்டது. பெயர்: '{clean_name}'."
        )
        
        arta_response_en = (
            f"Identity document attached successfully for {clean_name}."
        )

        return {
            "verified": False,
            "extracted_name": clean_name,
            "document_type": document_type,
            "match_confidence": 0.90,
            "status": "DOCUMENT_ATTACHED",
            "arta_response_ta": arta_response_ta,
            "arta_response_en": arta_response_en
        }

# Alias for backwards compatibility
DemoIdentityVerificationService = IdentityVerificationService

