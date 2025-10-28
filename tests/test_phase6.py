#!/usr/bin/env python3
"""
Test Phase 6: Enhanced Brain Council
- Emotional Contagion
- Neuromodulators (Dopamine, Serotonin, Norepinephrine)
- ACC Conflict Monitoring
- Basal Ganglia Rename
"""
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def test_emotional_contagion():
    """Test that emotions spread between brain regions"""
    from brain_council.council import BrainCouncil

    logger.info("\n" + "=" * 70)
    logger.info("TEST 1: Emotional Contagion System")
    logger.info("=" * 70)

    council = BrainCouncil()

    # Test scenario: Dangerous situation (should trigger strong fear in Amygdala)
    context = {
        'physical_state': {'hunger': 30, 'energy': 70, 'health': 100, 'happiness': 60},
        'relationship': {'trust': 50, 'bond': 40},
        'location_safety': 2,  # DANGEROUS location
        'personality': {'curiosity': 7, 'bravery': 3, 'playfulness': 6}
    }

    decision = council.deliberate(
        situation="Should we explore this dark, dangerous cave?",
        context=context,
        debug=True
    )

    # Check that emotions were set
    logger.info("\n✓ Emotional states after contagion:")
    for region in council.regions:
        emotion, intensity = region.get_emotional_state()
        logger.info(f"  {region.name}: {emotion} (intensity: {intensity:.2f})")

    # Verify Amygdala's fear/alarm influenced other regions
    amygdala = next(r for r in council.regions if r.name == "Amygdala")
    # Amygdala should show fear or alarm (both are negative threat emotions)
    if amygdala.current_emotion in ["fear", "alarm"]:
        # Check that at least 2 other regions also show fear/alarm (contagion worked)
        fear_count = sum(1 for r in council.regions
                        if r.current_emotion in ["fear", "alarm"])
        if fear_count >= 3:
            logger.info(f"\n✅ TEST 1 PASSED: Fear/alarm spread to {fear_count} regions via contagion")
            return True
        else:
            logger.error("\n❌ TEST 1 FAILED: Emotional contagion didn't spread fear")
            return False
    else:
        logger.error(f"\n❌ TEST 1 FAILED: Amygdala shows {amygdala.current_emotion}, expected fear/alarm")
        return False


def test_neuromodulators():
    """Test neuromodulator systems (dopamine, serotonin, norepinephrine)"""
    from brain_council.council import BrainCouncil

    logger.info("\n" + "=" * 70)
    logger.info("TEST 2: Neuromodulator Systems")
    logger.info("=" * 70)

    council = BrainCouncil()

    # Test with high happiness and strong bond (should boost dopamine/serotonin)
    context = {
        'physical_state': {'hunger': 20, 'energy': 80, 'health': 100, 'happiness': 90},
        'relationship': {'trust': 85, 'bond': 75},
        'location_safety': 9,
        'personality': {'curiosity': 7, 'bravery': 6, 'playfulness': 8}
    }

    decision = council.deliberate(
        situation="The trainer wants to play with us!",
        context=context,
        debug=True
    )

    # Check neuromodulator levels
    neuromod_state = council.neuromodulators.update_all(context)

    logger.info(f"\n✓ Neuromodulator levels:")
    logger.info(f"  Dopamine: {neuromod_state.dopamine:.2f} (should be high)")
    logger.info(f"  Serotonin: {neuromod_state.serotonin:.2f} (should be high)")
    logger.info(f"  Norepinephrine: {neuromod_state.norepinephrine:.2f}")

    # High happiness + strong bond should produce high dopamine and serotonin
    if neuromod_state.dopamine > 0.7 and neuromod_state.serotonin > 0.6:
        logger.info("\n✅ TEST 2 PASSED: Neuromodulators respond to positive context")
        return True
    else:
        logger.error("\n❌ TEST 2 FAILED: Expected higher dopamine/serotonin")
        return False


def test_acc_conflict_monitoring():
    """Test ACC conflict detection"""
    from brain_council.council import BrainCouncil

    logger.info("\n" + "=" * 70)
    logger.info("TEST 3: ACC Conflict Monitoring")
    logger.info("=" * 70)

    council = BrainCouncil()

    # Create conflicted scenario: very tired but trainer wants to play
    context = {
        'physical_state': {'hunger': 75, 'energy': 15, 'health': 100, 'happiness': 50},
        'relationship': {'trust': 80, 'bond': 70},
        'location_safety': 10,
        'personality': {'curiosity': 5, 'bravery': 5, 'playfulness': 8}
    }

    decision = council.deliberate(
        situation="Trainer wants to play, but I'm exhausted and hungry",
        context=context,
        debug=True
    )

    logger.info(f"\n✓ Conflict Level: {decision.conflict_level:.2f}")
    logger.info(f"✓ Conflict Detected: {decision.conflict_detected}")
    logger.info(f"✓ Consensus Level: {decision.consensus_level:.2f}")

    # Should detect some conflict (tired vs. want to please trainer)
    if decision.conflict_level > 0.3:
        logger.info("\n✅ TEST 3 PASSED: ACC detected internal conflict")
        return True
    else:
        logger.error("\n❌ TEST 3 FAILED: Expected higher conflict detection")
        return False


def test_basal_ganglia_rename():
    """Test that Cerebellum was renamed to Basal Ganglia"""
    from brain_council.council import BrainCouncil

    logger.info("\n" + "=" * 70)
    logger.info("TEST 4: Basal Ganglia Rename")
    logger.info("=" * 70)

    council = BrainCouncil()

    region_names = [r.name for r in council.regions]
    logger.info(f"\n✓ Brain regions: {region_names}")

    if "Basal Ganglia" in region_names and "Cerebellum" not in region_names:
        logger.info("\n✅ TEST 4 PASSED: Cerebellum renamed to Basal Ganglia")
        return True
    else:
        logger.error("\n❌ TEST 4 FAILED: Cerebellum should be renamed")
        return False


def test_integration():
    """Test all Phase 6 features working together"""
    from brain_council.council import BrainCouncil

    logger.info("\n" + "=" * 70)
    logger.info("TEST 5: Full Phase 6 Integration")
    logger.info("=" * 70)

    council = BrainCouncil()

    # Complex scenario that exercises all systems
    context = {
        'physical_state': {'hunger': 40, 'energy': 60, 'health': 85, 'happiness': 70},
        'relationship': {'trust': 75, 'bond': 65},
        'location_safety': 7,
        'personality': {'curiosity': 8, 'bravery': 6, 'playfulness': 7}
    }

    decision = council.deliberate(
        situation="Should we explore the new location with our trainer?",
        context=context,
        debug=True
    )

    logger.info(f"\n✓ Final Decision: {decision.winning_vote.decision}")
    logger.info(f"✓ Consensus: {decision.consensus_level:.2f}")
    logger.info(f"✓ Conflict: {decision.conflict_level:.2f}")
    logger.info(f"✓ Primary Emotion: {decision.winning_vote.primary_emotion}")
    logger.info(f"✓ Arousal: {decision.winning_vote.arousal_level:.2f}")

    # Verify all Phase 6 components present
    has_emotion = hasattr(decision.winning_vote, 'primary_emotion')
    has_arousal = hasattr(decision.winning_vote, 'arousal_level')
    has_conflict = hasattr(decision, 'conflict_level')

    if has_emotion and has_arousal and has_conflict:
        logger.info("\n✅ TEST 5 PASSED: All Phase 6 features integrated")
        return True
    else:
        logger.error("\n❌ TEST 5 FAILED: Missing Phase 6 features")
        return False


def main():
    """Run all Phase 6 tests"""
    logger.info("=" * 70)
    logger.info("PHASE 6 TEST SUITE")
    logger.info("Testing: Emotional Contagion, Neuromodulators, ACC, Basal Ganglia")
    logger.info("=" * 70)

    results = []

    try:
        results.append(("Emotional Contagion", test_emotional_contagion()))
    except Exception as e:
        logger.error(f"❌ Emotional Contagion test crashed: {e}")
        results.append(("Emotional Contagion", False))

    try:
        results.append(("Neuromodulators", test_neuromodulators()))
    except Exception as e:
        logger.error(f"❌ Neuromodulators test crashed: {e}")
        results.append(("Neuromodulators", False))

    try:
        results.append(("ACC Conflict Monitoring", test_acc_conflict_monitoring()))
    except Exception as e:
        logger.error(f"❌ ACC test crashed: {e}")
        results.append(("ACC Conflict Monitoring", False))

    try:
        results.append(("Basal Ganglia Rename", test_basal_ganglia_rename()))
    except Exception as e:
        logger.error(f"❌ Basal Ganglia test crashed: {e}")
        results.append(("Basal Ganglia Rename", False))

    try:
        results.append(("Full Integration", test_integration()))
    except Exception as e:
        logger.error(f"❌ Integration test crashed: {e}")
        results.append(("Full Integration", False))

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 6 TEST RESULTS")
    logger.info("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        logger.info("\n🎉 ALL PHASE 6 TESTS PASSED! 🎉")
        return 0
    else:
        logger.error(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
