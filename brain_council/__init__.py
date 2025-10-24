"""
Brain Council Module - Multi-region decision making system
"""
from .council import BrainCouncil
from .decision import DecisionEngine, CouncilDecision
from .regions import (
    BrainRegion, PrefrontalCortex, Amygdala,
    Hippocampus, Hypothalamus, Cerebellum, RegionVote
)

__all__ = [
    'BrainCouncil',
    'DecisionEngine',
    'CouncilDecision',
    'BrainRegion',
    'PrefrontalCortex',
    'Amygdala',
    'Hippocampus',
    'Hypothalamus',
    'Cerebellum',
    'RegionVote'
]
