"""
Memory type definitions - Episodic, Semantic, Emotional, and Procedural memories

Following the design specification from eevee-brain-council.md Phase 3.
Each memory type has distinct properties and storage patterns.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import json


class MemoryType(Enum):
    """Four distinct memory types based on neuroscience"""
    EPISODIC = "episodic"      # Specific events: "Trainer gave me berry when sick"
    SEMANTIC = "semantic"       # Facts/knowledge: "Oran berries heal poison"
    EMOTIONAL = "emotional"     # Associations: "Forest = scary but exciting"
    PROCEDURAL = "procedural"   # Skills/behaviors: "How to ask for food"


class EmotionType(Enum):
    """Primary emotions that can be associated with memories"""
    JOY = "joy"
    FEAR = "fear"
    SADNESS = "sadness"
    ANGER = "anger"
    SURPRISE = "surprise"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    DISGUST = "disgust"
    GRATITUDE = "gratitude"
    CURIOSITY = "curiosity"
    LONELINESS = "loneliness"
    CONTENTMENT = "contentment"


@dataclass
class Memory:
    """
    Base memory class with common attributes.

    Significance threshold: 6.0+ is stored long-term
    Memories below threshold fade over time (forgetting_rate from config)
    """
    memory_id: str
    memory_type: MemoryType
    content: str
    timestamp: datetime
    significance: float  # 0-10 scale, 6.0+ is significant

    # Emotional context
    primary_emotion: Optional[EmotionType] = None
    emotion_intensity: float = 5.0  # 0-10 scale

    # Contextual metadata
    location: Optional[str] = None
    participants: List[str] = field(default_factory=list)  # ["trainer", "other_pokemon"]
    tags: List[str] = field(default_factory=list)

    # Memory strength (decays over time unless reinforced)
    strength: float = 1.0  # 0.0-1.0, affects retrieval probability
    access_count: int = 0  # How many times retrieved (strengthens memory)
    last_accessed: Optional[datetime] = None

    # Relationships to other memories
    related_memory_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary for storage"""
        return {
            "memory_id": self.memory_id,
            "memory_type": self.memory_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "significance": self.significance,
            "primary_emotion": self.primary_emotion.value if self.primary_emotion else None,
            "emotion_intensity": self.emotion_intensity,
            "location": self.location,
            "participants": self.participants,
            "tags": self.tags,
            "strength": self.strength,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "related_memory_ids": self.related_memory_ids
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory':
        """Create memory from dictionary"""
        memory_type = MemoryType(data["memory_type"])

        # Choose the appropriate subclass based on type
        if memory_type == MemoryType.EPISODIC:
            return EpisodicMemory.from_dict(data)
        elif memory_type == MemoryType.SEMANTIC:
            return SemanticMemory.from_dict(data)
        elif memory_type == MemoryType.EMOTIONAL:
            return EmotionalMemory.from_dict(data)
        elif memory_type == MemoryType.PROCEDURAL:
            return ProceduralMemory.from_dict(data)
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")

    def mark_accessed(self) -> None:
        """Mark memory as accessed (strengthens it)"""
        self.access_count += 1
        self.last_accessed = datetime.now()
        # Accessing memory strengthens it (up to max of 1.0)
        self.strength = min(1.0, self.strength + 0.05)

    def apply_decay(self, forgetting_rate: float) -> None:
        """Apply forgetting decay to memory strength"""
        # High significance memories decay slower
        effective_rate = forgetting_rate * (1.0 - self.significance / 10.0)
        self.strength = max(0.0, self.strength - effective_rate)


@dataclass
class EpisodicMemory(Memory):
    """
    Specific events and experiences.
    "What happened, when, where, who was there"

    Examples:
    - "First time exploring the deep forest with trainer - scary but exciting"
    - "Trainer gave me Pecha berry when I had a stomachache"
    - "Found a shiny smooth stone by the stream"
    """

    # Event-specific details
    event_type: str = "interaction"  # interaction, exploration, discovery, social
    outcome: Optional[str] = None  # What was the result?

    def __post_init__(self):
        self.memory_type = MemoryType.EPISODIC
        if not self.tags:
            self.tags = ["event", self.event_type]

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "event_type": self.event_type,
            "outcome": self.outcome
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EpisodicMemory':
        return cls(
            memory_id=data["memory_id"],
            memory_type=MemoryType.EPISODIC,
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            significance=data["significance"],
            primary_emotion=EmotionType(data["primary_emotion"]) if data.get("primary_emotion") else None,
            emotion_intensity=data.get("emotion_intensity", 5.0),
            location=data.get("location"),
            participants=data.get("participants", []),
            tags=data.get("tags", []),
            strength=data.get("strength", 1.0),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            related_memory_ids=data.get("related_memory_ids", []),
            event_type=data.get("event_type", "interaction"),
            outcome=data.get("outcome")
        )


@dataclass
class SemanticMemory(Memory):
    """
    Facts, knowledge, and general information.
    "Things I know to be true"

    Examples:
    - "Oran berries restore health"
    - "The meadow has the best berry bushes"
    - "Trainer always comes back eventually"
    """

    # Fact-specific details
    fact_category: str = "general"  # location, item, behavior, rule
    confidence: float = 0.8  # How confident are we in this fact? (0.0-1.0)
    evidence_count: int = 1  # How many times has this been validated?

    def __post_init__(self):
        self.memory_type = MemoryType.SEMANTIC
        if not self.tags:
            self.tags = ["fact", self.fact_category]

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "fact_category": self.fact_category,
            "confidence": self.confidence,
            "evidence_count": self.evidence_count
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SemanticMemory':
        return cls(
            memory_id=data["memory_id"],
            memory_type=MemoryType.SEMANTIC,
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            significance=data["significance"],
            primary_emotion=EmotionType(data["primary_emotion"]) if data.get("primary_emotion") else None,
            emotion_intensity=data.get("emotion_intensity", 5.0),
            location=data.get("location"),
            participants=data.get("participants", []),
            tags=data.get("tags", []),
            strength=data.get("strength", 1.0),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            related_memory_ids=data.get("related_memory_ids", []),
            fact_category=data.get("fact_category", "general"),
            confidence=data.get("confidence", 0.8),
            evidence_count=data.get("evidence_count", 1)
        )

    def validate(self) -> None:
        """Reinforce this semantic memory (increases confidence)"""
        self.evidence_count += 1
        self.confidence = min(1.0, self.confidence + 0.1)
        self.strength = min(1.0, self.strength + 0.1)


@dataclass
class EmotionalMemory(Memory):
    """
    Emotional associations and learned responses.
    "How I feel about things"

    Examples:
    - "Deep forest = scary and unknown"
    - "Trainer's voice = safety and happiness"
    - "Being alone = sad and anxious"
    """

    # Association details
    trigger: str = ""  # What triggers this emotion?
    response: str = ""  # How do I respond?
    learned_from: List[str] = field(default_factory=list)  # Related episodic memory IDs

    def __post_init__(self):
        self.memory_type = MemoryType.EMOTIONAL
        if not self.tags:
            self.tags = ["emotion", "association"]

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "trigger": self.trigger,
            "response": self.response,
            "learned_from": self.learned_from
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmotionalMemory':
        return cls(
            memory_id=data["memory_id"],
            memory_type=MemoryType.EMOTIONAL,
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            significance=data["significance"],
            primary_emotion=EmotionType(data["primary_emotion"]) if data.get("primary_emotion") else None,
            emotion_intensity=data.get("emotion_intensity", 5.0),
            location=data.get("location"),
            participants=data.get("participants", []),
            tags=data.get("tags", []),
            strength=data.get("strength", 1.0),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            related_memory_ids=data.get("related_memory_ids", []),
            trigger=data.get("trigger", ""),
            response=data.get("response", ""),
            learned_from=data.get("learned_from", [])
        )


@dataclass
class ProceduralMemory(Memory):
    """
    Learned behaviors, skills, and procedures.
    "How to do things"

    Examples:
    - "When hungry, nuzzle trainer's leg and look at them"
    - "When scared, hide behind trainer"
    - "When happy, wag tail and do zoomies"
    """

    # Behavior details
    behavior_name: str = ""
    trigger_condition: str = ""  # When to use this behavior
    success_rate: float = 0.5  # How often does this work? (0.0-1.0)
    times_used: int = 0

    def __post_init__(self):
        self.memory_type = MemoryType.PROCEDURAL
        if not self.tags:
            self.tags = ["behavior", "skill"]

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "behavior_name": self.behavior_name,
            "trigger_condition": self.trigger_condition,
            "success_rate": self.success_rate,
            "times_used": self.times_used
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProceduralMemory':
        return cls(
            memory_id=data["memory_id"],
            memory_type=MemoryType.PROCEDURAL,
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            significance=data["significance"],
            primary_emotion=EmotionType(data["primary_emotion"]) if data.get("primary_emotion") else None,
            emotion_intensity=data.get("emotion_intensity", 5.0),
            location=data.get("location"),
            participants=data.get("participants", []),
            tags=data.get("tags", []),
            strength=data.get("strength", 1.0),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            related_memory_ids=data.get("related_memory_ids", []),
            behavior_name=data.get("behavior_name", ""),
            trigger_condition=data.get("trigger_condition", ""),
            success_rate=data.get("success_rate", 0.5),
            times_used=data.get("times_used", 0)
        )

    def record_use(self, successful: bool) -> None:
        """Record usage of this procedural memory"""
        self.times_used += 1
        # Update success rate with running average
        if successful:
            self.success_rate = (self.success_rate * (self.times_used - 1) + 1.0) / self.times_used
        else:
            self.success_rate = (self.success_rate * (self.times_used - 1)) / self.times_used
        # Strengthen memory when used
        self.strength = min(1.0, self.strength + 0.03)


@dataclass
class WorkingMemory:
    """
    Short-term working memory - last 10 interactions
    Gets cleared periodically, significant ones consolidated to long-term
    """
    max_size: int = 10
    memories: List[str] = field(default_factory=list)  # List of recent interaction strings

    def add(self, content: str) -> None:
        """Add to working memory, removing oldest if full"""
        self.memories.append(content)
        if len(self.memories) > self.max_size:
            self.memories.pop(0)

    def get_recent(self, count: int = 5) -> List[str]:
        """Get the N most recent memories"""
        return self.memories[-count:]

    def clear(self) -> None:
        """Clear working memory"""
        self.memories.clear()

    def to_context_string(self) -> str:
        """Convert working memory to a context string for brain council"""
        if not self.memories:
            return "No recent memories."
        return "\n".join([f"- {mem}" for mem in self.memories[-5:]])
