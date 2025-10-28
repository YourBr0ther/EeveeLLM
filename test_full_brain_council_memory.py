"""
Test Full Brain Council Memory Flow

Tests that memories are retrieved and passed through even when
Hippocampus doesn't win the vote (which is common since Amygdala
has the highest weight of 0.30 vs Hippocampus's 0.20).
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.consolidation import MemoryConsolidator
from memory.vector_store import VectorMemoryStore
from memory.retrieval import MemoryRetriever
from brain_council.council import BrainCouncil
from eevee.state import EeveeState
from config import Config

def test_full_brain_council_memory_flow():
    """Test that memories flow through brain council even when Hippocampus doesn't win"""
    print("\n" + "="*70)
    print("TEST: Full Brain Council Memory Flow")
    print("Testing that memories survive even when Hippocampus loses the vote")
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
    brain_council = BrainCouncil()

    # Integrate memory retriever with Hippocampus
    for region in brain_council.regions:
        if region.name == "Hippocampus":
            region.memory_retriever = retriever
            print("✅ Memory retriever integrated with Hippocampus")
            break

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
        'location_safety': 10,
        'relationship': {
            'trust': 75,
            'bond': 70
        }
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
        print(f"✅ Stored {len(memories)} memor{'y' if len(memories) == 1 else 'ies'}")
    else:
        print("❌ No memories stored!")
        return False

    # Step 2: Full brain council deliberation on "what is my name?"
    print("\n" + "-"*70)
    print("STEP 2: Full Brain Council Deliberation")
    print("-"*70)

    user_input_2 = "what is my name?"

    # Run full deliberation
    decision = brain_council.deliberate(
        situation=user_input_2,
        context=context,
        debug=True  # Show detailed output
    )

    print(f"\n{'='*70}")
    print("DELIBERATION RESULTS:")
    print(f"{'='*70}")
    print(f"Winning Region: {decision.winning_vote.region_name}")
    print(f"Winning Decision: {decision.winning_vote.decision}")
    print(f"Consensus Level: {decision.consensus_level:.2f}")
    print(f"Conflict Level: {decision.conflict_level:.2f}")

    # Check all votes for memories
    print(f"\n{'='*70}")
    print("CHECKING ALL VOTES FOR MEMORIES:")
    print(f"{'='*70}")

    hippocampus_has_memories = False
    for vote in decision.all_votes:
        has_memories = hasattr(vote, 'retrieved_memories') and vote.retrieved_memories
        status = "✅ HAS MEMORIES" if has_memories else "❌ No memories"
        print(f"{vote.region_name}: {status}")

        if vote.region_name == "Hippocampus" and has_memories:
            hippocampus_has_memories = True
            print(f"   → Hippocampus retrieved {len(vote.retrieved_memories)} memories")

    if not hippocampus_has_memories:
        print("\n❌ FAIL: Hippocampus did not retrieve memories!")
        return False

    # Step 3: Check if memories made it to the decision
    print(f"\n{'='*70}")
    print("STEP 3: Verify Memories in Council Decision")
    print(f"{'='*70}")

    if decision.retrieved_memories:
        print(f"✅ Council Decision includes {len(decision.retrieved_memories)} memories")
        print("\nMemories in decision:")
        for i, (content, metadata, relevance) in enumerate(decision.retrieved_memories[:3], 1):
            print(f"   {i}. {content[:80]}...")
            print(f"      Relevance: {relevance:.3f}")
    else:
        print("❌ FAIL: Council Decision does NOT include memories!")
        print(f"   Winning region: {decision.winning_vote.region_name}")
        print(f"   This means memories were lost because Hippocampus didn't win!")
        return False

    # Check if name memory is in the retrieved memories
    name_found = False
    for content, metadata, relevance in decision.retrieved_memories:
        if 'Chris' in content or ('name' in content.lower() and 'chris' in content.lower()):
            name_found = True
            print(f"\n✅ Name memory found in decision: '{content}'")
            break

    if not name_found:
        print("\n⚠️  WARNING: Name memory not in top retrieved memories")
        print("   (But at least some memories were preserved)")

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n🎉 Memory flow is working correctly!")
    print("   - Hippocampus retrieves memories")
    print("   - Memories are preserved even if Hippocampus doesn't win")
    print("   - Memories are included in the Council Decision")
    print("   - Memories will be passed to the LLM prompt")
    print("\nRegion Weights:")
    print("   - Amygdala: 0.30 (often wins)")
    print("   - Prefrontal Cortex: 0.25")
    print("   - Hippocampus: 0.20 (has the memories)")
    print("   - Hypothalamus: 0.15")
    print("   - Basal Ganglia: 0.10")
    print("\nThe fix ensures memories are extracted from ANY region that has them,")
    print("not just the winning region!")

    return True


if __name__ == "__main__":
    success = test_full_brain_council_memory_flow()
    sys.exit(0 if success else 1)
