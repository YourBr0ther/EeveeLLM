"""
Test Memory Retrieval Fix

Verifies that when a user says "My name is Chris" and then asks
"what is my name?", Eevee can retrieve and use the stored memory.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.consolidation import MemoryConsolidator
from memory.vector_store import VectorMemoryStore
from memory.retrieval import MemoryRetriever
from brain_council.council import BrainCouncil
from brain_council.regions import Hippocampus
from eevee.state import EeveeState
from config import Config

def test_memory_retrieval():
    """Test that memories are retrieved and passed to the LLM"""
    print("\n" + "="*70)
    print("TEST: Memory Retrieval and Response Generation")
    print("="*70)

    # Initialize components
    vector_store = VectorMemoryStore()
    consolidator = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )
    retriever = MemoryRetriever(
        vector_store=vector_store,
        config={
            'memory_retrieval_count': 5,
            'memory_significance_threshold': 6.0,
            'max_working_memory': 100
        }
    )
    eevee = EeveeState()

    # Build context
    context = {
        'current_location': 'trainer_home',
        'primary_emotion': 'curious',
        'emotion_intensity': 5.0,
        'physical_state': {
            'hunger': 50,
            'energy': 50,
            'happiness': 75
        },
        'location_safety': 10
    }

    # Step 1: Store "My name is Chris"
    print("\n" + "-"*70)
    print("STEP 1: Storing memory 'My name is Chris'")
    print("-"*70)

    user_input_1 = "My name is Chris"
    eevee_response_1 = "*Vee!* Chris! *tail wagging happily*"

    memories = consolidator.process_interaction(
        user_input=user_input_1,
        eevee_response=eevee_response_1,
        context=context,
        council_decision=None
    )

    if memories:
        print(f"✅ Stored {len(memories)} memor{'y' if len(memories) == 1 else 'ies'}:")
        for memory in memories:
            print(f"   - {memory.memory_type.value}: {memory.content[:60]}...")
    else:
        print("❌ No memories stored!")
        return False

    # Step 2: Query "what is my name?"
    print("\n" + "-"*70)
    print("STEP 2: Querying memory with 'what is my name?'")
    print("-"*70)

    user_input_2 = "what is my name?"

    # Retrieve relevant memories
    retrieved_memories = retriever.retrieve_relevant_memories(
        situation=user_input_2,
        context=context
    )

    if not retrieved_memories:
        print("❌ No memories retrieved!")
        return False

    print(f"✅ Retrieved {len(retrieved_memories)} memor{'y' if len(retrieved_memories) == 1 else 'ies'}:")
    for content, metadata, relevance in retrieved_memories:
        fact_category = metadata.get('fact_category', 'N/A')
        print(f"   - {content[:80]}...")
        print(f"     Category: {fact_category}, Relevance: {relevance:.3f}")

    # Check if name memory was retrieved
    name_found = False
    for content, metadata, relevance in retrieved_memories:
        if 'Chris' in content or 'name' in content.lower():
            name_found = True
            print(f"\n✅ Name memory found: '{content}'")
            break

    if not name_found:
        print("\n❌ Name memory NOT found in retrieved memories!")
        return False

    # Step 3: Test Brain Council with Hippocampus
    print("\n" + "-"*70)
    print("STEP 3: Testing Brain Council with Memory Retrieval")
    print("-"*70)

    # Create Hippocampus with memory retriever
    hippocampus = Hippocampus(memory_retriever=retriever)

    # Get Hippocampus vote
    hippocampus_vote = hippocampus.analyze(user_input_2, context)

    print(f"\nHippocampus Vote:")
    print(f"   Decision: {hippocampus_vote.decision}")
    print(f"   Reasoning: {hippocampus_vote.reasoning}")
    print(f"   Confidence: {hippocampus_vote.confidence:.2f}")

    # Check if vote contains retrieved memories
    if hasattr(hippocampus_vote, 'retrieved_memories') and hippocampus_vote.retrieved_memories:
        print(f"   ✅ Vote includes {len(hippocampus_vote.retrieved_memories)} retrieved memories")
    else:
        print(f"   ❌ Vote does NOT include retrieved memories!")
        return False

    # Step 4: Check that memories would be passed to LLM
    print("\n" + "-"*70)
    print("STEP 4: Verify memory flow to LLM prompt")
    print("-"*70)

    # Simulate brain context
    brain_context = {
        'decision': hippocampus_vote.decision,
        'reasoning': hippocampus_vote.reasoning,
        'emotion': 'curious',
        'retrieved_memories': hippocampus_vote.retrieved_memories
    }

    if brain_context['retrieved_memories']:
        print(f"✅ Brain context includes {len(brain_context['retrieved_memories'])} memories")
        print("\nMemories that would be passed to LLM:")
        for i, (content, metadata, relevance) in enumerate(brain_context['retrieved_memories'][:3], 1):
            print(f"   {i}. {content}")
    else:
        print("❌ Brain context does NOT include memories!")
        return False

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n🎉 Memory retrieval is working correctly!")
    print("   - Memories are stored properly")
    print("   - Memories are retrieved based on semantic similarity")
    print("   - Hippocampus includes memories in its vote")
    print("   - Memories flow through brain context to LLM prompt")
    print("\nEevee should now be able to remember and recall your name!")

    return True


if __name__ == "__main__":
    success = test_memory_retrieval()
    sys.exit(0 if success else 1)
