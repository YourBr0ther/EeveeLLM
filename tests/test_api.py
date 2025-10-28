#!/usr/bin/env python3
"""
Quick test of NanoGPT API connection
"""
from llm.nanogpt_client import NanoGPTClient
from config import Config

print("=" * 70)
print("Testing NanoGPT API Connection")
print("=" * 70)
print(f"\nAPI Key: {Config.NANOGPT_API_KEY[:20]}...")
print(f"Endpoint: {Config.NANOGPT_ENDPOINT}")
print(f"Model: {Config.NANOGPT_MODEL}")
print()

# Create client
client = NanoGPTClient()

if client.fallback_mode:
    print("❌ Client is in fallback mode (no API key)")
else:
    print("✅ Client initialized with API key")
    print("\nTesting API with simple prompt...")

    try:
        response = client.generate(
            "Say hello in one short sentence as Eevee the Pokemon.",
            max_tokens=50,
            temperature=0.7
        )

        print("\n✅ API RESPONSE:")
        print(f"   {response}")
        print("\n✅ Success! NanoGPT API is working!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: Check your API key and make sure you have credits.")

print("\n" + "=" * 70)
