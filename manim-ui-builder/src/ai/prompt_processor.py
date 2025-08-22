class PromptProcessor:
    def __init__(self, gemini_client):
        self.gemini_client = gemini_client

    def process_prompt(self, prompt):
        # Preprocess the prompt if necessary
        processed_prompt = self._preprocess_prompt(prompt)
        # Send the processed prompt to the Gemini client
        return self.gemini_client.send_prompt(processed_prompt)

    def _preprocess_prompt(self, prompt):
        # Example preprocessing: strip whitespace and convert to lowercase
        return prompt.strip().lower()