import openai

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_suggestion(self, current_changes, incoming_changes):
        prompt = (
            "You are a code expert helping with Git merge conflict resolution. "
            "The following text shows two conflicting code sections: one labeled 'current' "
            "and the other labeled 'incoming'. Evaluate each section and suggest a resolution. "
            "Consider which changes might be more appropriate, or suggest merging both if relevant.\n\n"
            f"Current changes:\n{current_changes}\n\n"
            f"Incoming changes:\n{incoming_changes}\n\n"
            "Suggested resolution:"
        )
        
        # OpenAI API response call
        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        
        # get suggestion from the API response
        suggestion = response.choices[0].text.strip()
        return suggestion
