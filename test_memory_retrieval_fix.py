"""
Test memory retrieval to debug the "green" hallucination issue

This script will check:
1. What memories exist in the vector store
2. What memories are retrieved for "This meadow is so pretty, isn't it?"
3. Whether "green" exists anywhere in memories
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from memory.vector_store import VectorMemoryStore
from memory.retrieval import MemoryRetriever
from config import Config

def test_memory_retrieval():
    """Test what memories are retrieved for the meadow query"""

    print("=" * 70)
    print("MEMORY RETRIEVAL DEBUGGING")
    print("=" * 70)
    print()

    # Initialize vector store
    print("1. Initializing vector store...")
    vector_store = VectorMemoryStore()  # Uses default path from vector_store.py

    # Initialize memory retriever
    retriever_config = {
        'memory_retrieval_count': 5,
        'memory_significance_threshold': 6.0,
        'max_working_memory': 100
    }
    retriever = MemoryRetriever(vector_store, retriever_config)

    print(f"   Using default vector store path (data/chroma)")
    print(f"   Memory retrieval count: {retriever_config['memory_retrieval_count']}")
    print()

    # Test query (from the screenshot)
    test_query = "This meadow is so pretty, isn't it?"
    test_location = "Wide Meadow"

    print("2. Testing memory retrieval...")
    print(f"   Query: \"{test_query}\"")
    print(f"   Location: {test_location}")
    print()

    # Build context (similar to what's passed during conversation)
    context = {
        'current_location': test_location,
        'primary_emotion': 'curious'
    }

    # Retrieve memories
    retrieved_memories = retriever.retrieve_relevant_memories(
        situation=test_query,
        context=context
    )

    print("3. Retrieved Memories:")
    print("-" * 70)
    if not retrieved_memories:
        print("   NO MEMORIES RETRIEVED")
    else:
        for i, (content, metadata, relevance) in enumerate(retrieved_memories, 1):
            print(f"\n   Memory #{i} (relevance: {relevance:.3f}):")
            print(f"   Content: {content}")
            print(f"   Emotion: {metadata.get('primary_emotion', 'unknown')}")
            print(f"   Location: {metadata.get('location', 'unknown')}")
            print(f"   Significance: {metadata.get('significance', 0.0)}")
            print(f"   Timestamp: {metadata.get('timestamp', 'unknown')}")

            # Check if "green" appears in this memory
            if 'green' in content.lower():
                print(f"   ⚠️  CONTAINS 'GREEN' - This could be the hallucination source!")

    print()
    print("-" * 70)

    # Search for any memories containing "green"
    print()
    print("4. Searching for ALL memories containing 'green'...")
    print("-" * 70)

    green_memories = retriever.search_memories(query="green", limit=20)

    if not green_memories:
        print("   NO MEMORIES FOUND containing 'green'")
    else:
        print(f"   Found {len(green_memories)} memories containing 'green':")
        for i, (content, metadata, similarity) in enumerate(green_memories, 1):
            print(f"\n   #{i} (similarity: {similarity:.3f}):")
            print(f"   Content: {content[:200]}...")
            print(f"   Location: {metadata.get('location', 'unknown')}")
            print(f"   Timestamp: {metadata.get('timestamp', 'unknown')}")

    print()
    print("-" * 70)

    # Check recent working memory
    print()
    print("5. Working Memory (last 10 interactions):")
    print("-" * 70)
    working_memory_str = retriever.get_working_memory_context()
    if working_memory_str.strip() == "No recent interactions" or not working_memory_str.strip():
        print("   NO WORKING MEMORY")
    else:
        print(working_memory_str)

    print()
    print("=" * 70)
    print("DEBUGGING COMPLETE")
    print("=" * 70)
    print()

    # Analysis
    print("ANALYSIS:")
    print("-" * 70)

    if retrieved_memories:
        has_green = any('green' in mem[0].lower() for mem in retrieved_memories)
        if has_green:
            print("✗ ISSUE FOUND: 'green' appears in retrieved memories")
            print("  This explains the hallucination - Eevee is referencing")
            print("  a memory that contains 'green' even though the current")
            print("  conversation doesn't mention it.")
        else:
            print("✓ NO 'green' in retrieved memories for this query")
            print("  The hallucination may be coming from:")
            print("  - LLM confabulation (making up memories)")
            print("  - Working memory (not checked yet)")
            print("  - Prompt structure encouraging memory references")
    else:
        print("✓ No memories retrieved at all")
        print("  The hallucination is likely pure LLM confabulation")

    print()
    print("RECOMMENDATION:")
    print("-" * 70)
    print("Based on these findings, we should:")
    print("1. Review the prompt in prompts.py line 168-169")
    print("2. Check if LLM is being over-encouraged to reference memories")
    print("3. Consider adding validation: only mention memories if they exist")
    print("4. Possibly adjust memory retrieval relevance threshold")
    print()

if __name__ == "__main__":
    test_memory_retrieval()
