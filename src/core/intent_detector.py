from typing import List

class IntentDetector:
    """Detects user intent from natural language queries using the LLM."""
    
    def __init__(self, llm_client, capabilities: List[str]):
        self.llm_client = llm_client
        self.capabilities = capabilities
    
    def detect_intent(self, query: str) -> str:
        """Detect intent from user query."""
        prompt = f"""
        Detect the intent of the following query: "{query}"

        Return ONLY ONE WORD from these capabilities: {', '.join(self.capabilities)}

        If the intent is not clear or doesn't match any capability, return 'unknown'.

        Query: {query}
        Intent:"""
        
        response = self.llm_client.query(prompt, 1024, 5)
        detected_intent = response.strip().lower()
        
        print(f"🤖 Detected intent: {detected_intent}")
        
        # Validate that the response is one of our capabilities
        if detected_intent in self.capabilities:
            return detected_intent
        else:
            return "unknown"
