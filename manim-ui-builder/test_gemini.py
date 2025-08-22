#!/usr/bin/env python3
"""
Test script to verify Gemini API integration is working correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai.gemini_client import GeminiClient
from src.utils.config import config

def test_api_connection():
    """Test the Gemini API connection."""
    print("Testing Gemini API connection...")
    
    try:
        # Validate configuration
        config.validate()
        print("✓ Configuration loaded successfully")
        print(f"✓ API key configured: {config.api_key[:10]}...")
        
        # Initialize client
        client = GeminiClient()
        print("✓ GeminiClient initialized")
        
        # Test API connection
        if client.validate_api_key():
            print("✓ API key is valid and working")
        else:
            print("✗ API key validation failed")
            return False
        
        # Test basic prompt
        test_prompt = "Create a simple Manim animation showing a circle that changes color from blue to red"
        print(f"\nTesting with prompt: '{test_prompt}'")
        
        response = client.send_prompt(test_prompt)
        
        if response.get("success"):
            print("✓ Prompt processed successfully")
            print(f"Generated code preview: {response['code'][:100]}...")
            print(f"Explanation: {response['explanation'][:200]}...")
        else:
            print(f"✗ Prompt processing failed: {response.get('error', 'Unknown error')}")
            return False
        
        print("\n🎉 All tests passed! Gemini integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)
