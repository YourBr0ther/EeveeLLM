"""
Brain Council Module - Multi-region decision making system
"""
from .council import BrainCouncil
from .decision import DecisionEngine, CouncilDecision
from .regions import (
    BrainRegion, PrefrontalCortex, Amygdala,
    Hippocampus, Hypothalamus, BasalGanglia, RegionVote
)
from .neuromodulators import NeuromodulatorOrchestrator  # Phase 6

# Phase 6: Backward compatibility alias
Cerebellum = BasalGanglia

__all__ = [
    'BrainCouncil',
    'DecisionEngine',
    'CouncilDecision',
    'BrainRegion',
    'PrefrontalCortex',
    'Amygdala',
    'Hippocampus',
    'Hypothalamus',
    'BasalGanglia',
    'Cerebellum',  # Backward compatibility
    'RegionVote',
    'NeuromodulatorOrchestrator'  # Phase 6
]
