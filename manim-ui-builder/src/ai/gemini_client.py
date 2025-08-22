from typing import Any, Dict, Optional
import google.generativeai as genai
from ..utils.config import config

class GeminiClient:
    def __init__(self):
        # Configure the Gemini API
        genai.configure(api_key=config.api_key)
        
        # Initialize the model (using the updated model name)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize chat session for conversational interactions
        self.chat = self.model.start_chat(history=[])

    def send_prompt(self, prompt: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a prompt to Gemini and get a response for animation generation.
        
        Args:
            prompt: User's natural language description
            context: Additional context about current scene
        
        Returns:
            Dictionary with generated code and explanation
        """
        try:
            # Enhance prompt with context for Manim code generation
            enhanced_prompt = self._build_manim_prompt(prompt, context)
            
            response = self.model.generate_content(enhanced_prompt)
            
            # Parse the response to extract Manim code
            return self._parse_response(response.text)
            
        except Exception as e:
            return {
                "error": str(e),
                "code": "",
                "explanation": f"Failed to generate animation: {str(e)}"
            }

    def chat_with_gemini(self, message: str) -> str:
        """
        Have a conversational interaction with Gemini for iterative animation editing.
        """
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error in chat: {str(e)}"

    def _build_manim_prompt(self, user_prompt: str, context: Optional[str] = None) -> str:
        """Build a comprehensive prompt for Manim code generation."""
        base_prompt = f"""
You are an expert Manim (Mathematical Animation Engine) developer. 
Generate Python code using Manim Community Edition to create the animation described below.

User Request: {user_prompt}

Requirements:
1. Use ManimCE (Community Edition) syntax
2. Create a complete Scene class that inherits from Scene
3. Include proper imports
4. Use appropriate mobjects (Text, Circle, Square, Arrow, MathTex, etc.)
5. Include smooth animations (FadeIn, FadeOut, Transform, Write, etc.)
6. Follow Manim best practices
7. Make the animation visually appealing and mathematically accurate

Additional Context: {context if context else "No additional context provided."}

Please provide:
1. Complete Python code
2. Brief explanation of what the animation does
3. Any special considerations or notes

Format your response as:
```python
# Your Manim code here
```

Explanation: Your explanation here
"""
        return base_prompt

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's response to extract code and explanation."""
        try:
            # Split response into code and explanation
            if "```python" in response_text:
                parts = response_text.split("```python")
                if len(parts) > 1:
                    code_part = parts[1].split("```")[0].strip()
                    explanation_part = response_text.split("```")[-1].strip()
                    if explanation_part.startswith("Explanation:"):
                        explanation_part = explanation_part[12:].strip()
                    
                    return {
                        "code": code_part,
                        "explanation": explanation_part,
                        "success": True
                    }
            
            # If no code block found, treat entire response as explanation
            return {
                "code": "",
                "explanation": response_text,
                "success": False,
                "error": "No Python code found in response"
            }
            
        except Exception as e:
            return {
                "code": "",
                "explanation": "",
                "success": False,
                "error": f"Failed to parse response: {str(e)}"
            }

    def get_animation_templates(self) -> Dict[str, str]:
        """Get common animation templates from Gemini."""
        template_prompt = """
        Provide 5 common Manim animation templates with brief descriptions.
        Include templates for:
        1. Basic shape animation
        2. Mathematical function plot
        3. Text animation
        4. Transformation animation
        5. 3D object animation
        
        Format as a Python dictionary with template names as keys and descriptions as values.
        """
        
        try:
            response = self.model.generate_content(template_prompt)
            # In a real implementation, you'd parse this more carefully
            return {
                "basic_shapes": "Animate basic geometric shapes with movement and color changes",
                "function_plot": "Plot and animate mathematical functions",
                "text_animation": "Animate text appearance and transformations",
                "morphing": "Transform one shape into another",
                "3d_objects": "Create and animate 3D mathematical objects"
            }
        except Exception as e:
            return {"error": f"Failed to get templates: {str(e)}"}

    def validate_api_key(self) -> bool:
        """Validate that the API key is working."""
        try:
            # Use a simple test prompt to validate the API key
            test_response = self.model.generate_content("Hello, test connection.")
            return test_response.text is not None and len(test_response.text) > 0
        except Exception as e:
            print(f"API validation error: {str(e)}")
            return False