# EeveeLLM - Project Summary

## Overview
EeveeLLM is an AI-powered Pokemon companion featuring a unique "brain council" architecture where 5 different brain regions debate and influence Eevee's decisions, creating genuine, context-aware responses with realistic internal conflicts. Now includes a sophisticated vector-based memory system that allows Eevee to form and retrieve meaningful memories.

**Current Status**: Phase 3 Complete (Memory System) ✅

---

## What's Been Built

### Phase 1: Foundation ✅ (Complete)

**Core System**
- Full terminal-based UI with color support
- SQLite database for persistent state
- Configuration system with YAML support
- Modular architecture ready for expansion

**Eevee State Management**
- Physical stats: hunger, energy, health, happiness (0-100 scale)
- Personality traits: curiosity, bravery, playfulness, loyalty, independence (0-10 scale)
- Relationship tracking: trust and bond levels
- Inventory system
- Time tracking between sessions

**World System**
- 8 fully implemented locations:
  - Trainer's Home (safe base)
  - Sunny Garden (nearby play area)
  - Wide Meadow (open exploration)
  - Clear Stream (resources: water, berries)
  - Forest Edge (moderate danger)
  - Hidden Den (secret safe space)
  - Sunny Hill (favorite napping spot)
  - Deep Forest (dangerous but exciting)
- Location properties: safety level, resources, weather exposure
- Graph-based travel system

**LLM Integration**
- NanoGPT API client with full error handling
- Intelligent fallback mode with pattern-based responses
- Prompt templates for various contexts
- Configurable temperature and token settings

**Interactive Commands**
- `talk [message]` - Speak with Eevee
- `pet` - Physical affection (increases trust/happiness)
- `play` - Playtime (increases bond, costs energy)
- `give [item]` - Item giving system
- `go [location]` - Travel between locations
- `observe` - Check Eevee's current activity
- `stats` - Detailed state information
- `world` - Location information
- `help` - Command list

### Phase 2: Brain Council ✅ (Complete)

**Brain Region System**
Five distinct brain regions with unique decision-making logic:

1. **Prefrontal Cortex (25% weight)**
   - Logic and planning
   - Evaluates long-term consequences
   - Considers trainer relationship
   - Manages goal-directed behavior

2. **Amygdala (30% weight, up to 60% under threat)**
   - Emotion and survival
   - Processes fear, excitement, joy
   - Triggers fight/flight responses
   - Forms emotional memories
   - **Dynamic weighting** based on danger

3. **Hippocampus (20% weight)**
   - Memory and context
   - Retrieves relevant past experiences
   - Identifies patterns
   - Contextualizes current situation

4. **Hypothalamus (15% weight, up to 35% when needs urgent)**
   - Physical needs and drives
   - Monitors hunger, thirst, energy, comfort
   - Generates motivation for basic needs
   - **Dynamic weighting** based on urgency

5. **Cerebellum (10% weight)**
   - Instinct and coordination
   - Species-specific Eevee behaviors
   - Automatic responses
   - Physical coordination

**Decision Engine**
- Weighted voting system with configurable weights
- Dynamic weight adjustments based on context
- Confidence scoring per region
- Emotional weight calculation
- Consensus measurement (0.0-1.0 scale)
- Conflict visualization and resolution

**Integration Features**
- Context-aware prompt generation using brain decisions
- Emotional state extraction from council votes
- Debug visualization showing full deliberation
- `debug brain` command to toggle visualization
- Location safety influences Amygdala weight
- Physical needs influence Hypothalamus weight

---

## Architecture

```
eevee-project/
├── main.py                          # Application entry point
├── config.py                        # Configuration management
├── ui.py                            # Terminal UI with color support
├── requirements.txt                 # Python dependencies
│
├── brain_council/                   # Phase 2: Brain Council System
│   ├── __init__.py
│   ├── regions.py                  # 5 brain region classes
│   ├── decision.py                 # Voting and decision engine
│   └── council.py                  # Council orchestrator
│
├── eevee/                          # Core Eevee logic
│   ├── __init__.py
│   ├── state.py                    # State management & persistence
│   ├── personality.py              # Personality trait system
│   └── responses.py                # Response generation with brain council
│
├── world/                          # World and location system
│   ├── __init__.py
│   └── locations.py                # 8 locations with properties
│
├── llm/                            # LLM integration
│   ├── __init__.py
│   ├── nanogpt_client.py          # API client with fallback
│   └── prompts.py                  # Prompt templates
│
├── memory/                         # Phase 3: Memory system (coming)
│   └── __init__.py
│
└── data/                           # Persistent data
    ├── eevee_save.db              # SQLite database
    └── memories/                   # ChromaDB storage (Phase 3)
```

---

## Key Design Principles

### 1. Authenticity Over Complexity
- Responses feel genuine, not robotic
- Internal conflicts are visible (when debug enabled)
- Imperfect decisions are more realistic
- Emotions drive behavior authentically

### 2. Brain Council Innovation
- Multiple perspectives on every decision
- Dynamic weight adjustments based on context
- Consensus measurement shows internal conflict
- Each region has distinct personality and priorities

### 3. State-Driven Behavior
- Physical needs directly influence decisions
- Personality traits remain semi-permanent
- Relationships evolve over time
- Location context affects brain regions

### 4. Modular & Extensible
- Clean separation of concerns
- Easy to add new brain regions
- Pluggable LLM backends
- Expandable world system

---

## How It Works: Brain Council Example

**Scenario:** User says "Let's explore the forest!"

**Context:**
- Location: Meadow (safety: 7)
- Hunger: 60, Energy: 70, Happiness: 80
- Trust: 75, Bond: 60

**Brain Council Deliberation:**

1. **Prefrontal Cortex** (weight: 0.25)
   - Decision: "agree_cautiously"
   - Reasoning: "Exploring builds experience and strengthens bond with trainer. But we should stay alert."
   - Confidence: 0.78

2. **Amygdala** (weight: 0.30)
   - Decision: "excited_agree"
   - Reasoning: "Adventure with trainer! Exciting but safe with them!"
   - Confidence: 0.80
   - Emotional weight: 0.90

3. **Hippocampus** (weight: 0.20)
   - Decision: "trust_pattern"
   - Reasoning: "No direct memory, but past experiences with trainer have been mostly positive."
   - Confidence: 0.60

4. **Hypothalamus** (weight: 0.15)
   - Decision: "distracted_hungry"
   - Reasoning: "Hard to focus... so hungry..."
   - Confidence: 0.70

5. **Cerebellum** (weight: 0.10)
   - Decision: "explore_instinct"
   - Reasoning: "*nose twitching* Natural curiosity activated!"
   - Confidence: 0.70

**Outcome:**
- **Winner:** Amygdala (highest weighted score)
- **Consensus:** 0.72 (generally agrees)
- **Dominant Emotion:** Excited
- **Response:** "*Eevee's tail starts wagging rapidly* Vee! Veevee! *bounces excitedly towards forest*"

---

## Technical Highlights

### Intelligent Fallback System
- When NanoGPT API unavailable, uses pattern-based responses
- Maintains authentic Eevee behavior even offline
- Seamless fallback with no crashes

### Dynamic Weight Adjustment
- Amygdala: 30% → 60% when safety < 5
- Hypothalamus: 15% → 35% when hunger > 80 or energy < 20
- Context-sensitive decision making

### State Persistence
- Automatic saving after each interaction
- Interaction history logged to database
- Resume exactly where you left off

### Visual Design
- Color-coded terminal output
- Progress bars for stats
- Location headers with emoji
- Debug mode with detailed deliberation view

---

## What Makes This Special

1. **First-of-its-Kind Brain Council**: No other Pokemon companion uses multi-region brain deliberation
2. **Genuine Internal Conflict**: Eevee can be torn between options (visible in debug mode)
3. **Context-Aware Emotions**: Responses aren't random - they're driven by weighted brain regions
4. **Dynamic Personality**: Weight adjustments mean Eevee acts differently under stress
5. **Educational**: Debug mode teaches users about decision-making psychology

---

## Next Steps (Phase 3-5)

### Phase 3: Memory System ✅ (Complete)

**Vector Memory Storage**
- ChromaDB integration with persistent storage
- Sentence transformer embeddings (all-MiniLM-L6-v2)
- 4 separate collections for memory types
- Semantic similarity search for relevant retrieval

**Memory Types Implemented**
- **Episodic Memories**: Specific events ("First time exploring forest with trainer")
- **Semantic Memories**: Facts and knowledge ("Oran berries restore health")
- **Emotional Memories**: Associations ("Forest = scary but exciting")
- **Procedural Memories**: Learned behaviors ("When hungry, nuzzle trainer's leg")

**Memory Formation & Consolidation**
- Significance-based filtering (threshold: 6.0/10)
- Automatic significance calculation from:
  - Emotional intensity
  - Novel experiences
  - Brain council conflict level
  - Relationship moments
  - Extreme states (hunger, danger)
- Working memory (last 10 interactions)
- Long-term storage for significant moments

**Memory Retrieval System**
- Context-aware semantic search
- Multi-factor relevance scoring (recency, strength, significance)
- Location and emotion filtering
- Automatic memory strengthening on access
- Top-5 relevant memories per deliberation

**Integration with Brain Council**
- Hippocampus brain region now uses vector memory
- Memories directly influence voting decisions
- Graceful fallback if memory system unavailable
- Debug visualization of memory retrieval

**New Commands**
- `remember` - Show memory statistics
- `remember [query]` - Search memories semantically
- `debug memory` - Toggle memory formation visualization

**Files Added**
- `memory/memory_types.py` (370 lines) - Memory class definitions
- `memory/vector_store.py` (400 lines) - ChromaDB wrapper
- `memory/retrieval.py` (360 lines) - Context-aware retrieval
- `memory/consolidation.py` (370 lines) - Memory formation logic

### Phase 4: Time Passage
- Autonomous behavior simulation
- Activity generation during offline periods
- Memory formation during time gaps
- Timeline summaries when returning

### Phase 5: Polish & Expansion
- Evolution system triggered by bond level
- Random world events
- Special surprises and discoveries
- Voice input support
- Multiple Pokemon interactions

---

## Files Created This Session

### Core System (13 files)
1. `config.py` - Configuration management
2. `main.py` - Application entry point
3. `ui.py` - Terminal interface
4. `requirements.txt` - Dependencies

### Brain Council (4 files)
5. `brain_council/__init__.py`
6. `brain_council/regions.py` - 5 brain region classes
7. `brain_council/decision.py` - Decision engine
8. `brain_council/council.py` - Orchestrator

### Eevee System (4 files)
9. `eevee/__init__.py`
10. `eevee/state.py` - State management
11. `eevee/personality.py` - Personality system
12. `eevee/responses.py` - Response generation

### World & LLM (6 files)
13. `world/__init__.py`
14. `world/locations.py` - 8 locations
15. `llm/__init__.py`
16. `llm/nanogpt_client.py` - API client
17. `llm/prompts.py` - Prompt templates
18. `memory/__init__.py` - Placeholder

### Documentation (4 files)
19. `README.md` - User documentation
20. `TASKS.md` - Development tracking
21. `PROJECT_SUMMARY.md` - This file
22. `.gitignore` - Git configuration

---

## How to Use

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Try brain council debug mode:**
   ```
   > debug brain
   > talk Hey Eevee, want to explore?
   ```

4. **Explore the world:**
   ```
   > world
   > go forest edge
   > observe
   ```

5. **Build your relationship:**
   ```
   > pet
   > play
   > give Oran Berry
   ```

---

## Development Stats

- **Total Files Created:** 22
- **Lines of Code:** ~3,500+
- **Brain Regions:** 5
- **Locations:** 8
- **Commands:** 11
- **Phases Completed:** 2/5
- **Time Invested:** Single session
- **Architecture:** Modular, extensible, production-ready

---

## Vision

Create the most unique, real, and impressive Pokemon interaction experience ever built. An Eevee that truly *lives* in a virtual world, with realistic brain processes, autonomous behavior during time gaps, and genuine memory formation.

**Status:** Well on track! Foundation and brain council complete, memory system next.

---

*"Vee! Veevee!"* - Your Eevee, powered by brain science and AI
