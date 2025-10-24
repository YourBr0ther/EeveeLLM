# Eevee Brain Council - Design Specification

## Project Vision
Create the most unique, real, and impressive Pokemon interaction experience ever built. An Eevee that truly *lives* in a virtual world, with realistic brain processes, autonomous behavior during time gaps, and genuine memory formation.

---

## Core Architecture

### 1. Brain Council System
The Eevee's decision-making is governed by a council of brain regions that debate, influence, and sometimes override each other.

#### Brain Regions & Roles

**Prefrontal Cortex (Logic & Planning)**
- Evaluates long-term consequences
- Plans future actions
- Considers trainer relationship
- Manages goal-directed behavior
- Vote weight: 25% (can be overridden in stress)

**Amygdala (Emotion & Survival)**
- Processes fear, excitement, joy
- Triggers fight/flight responses
- Forms emotional memories
- Influences trust/distrust
- Vote weight: 30% (increases to 60% under threat)

**Hippocampus (Memory)**
- Retrieves relevant past experiences
- Contextualizes current situation
- Identifies patterns
- Marks important moments for storage
- Vote weight: 20%

**Hypothalamus (Needs & Drives)**
- Tracks hunger, thirst, energy, comfort
- Generates motivation for basic needs
- Influences mood based on physical state
- Vote weight: 15%

**Cerebellum (Instinct & Coordination)**
- Species-specific behaviors (Eevee traits)
- Physical coordination and movement
- Automatic responses
- Vote weight: 10%

#### Decision Flow
1. **Stimulus Input** → Eevee perceives something (user message, environment change, need)
2. **Brain Council Activation** → Each region analyzes the situation from its perspective
3. **Internal Debate** → Regions propose responses with reasoning
4. **Weighted Voting** → Final response determined by vote weights + current state modifiers
5. **Response Generation** → NanoGPT generates natural language based on winning decision
6. **Memory Formation** → Significant moments stored with emotional tags

---

### 2. Autonomous Time Passage System

#### Time Simulation
- Real-world time maps to virtual world time (1:1 or accelerated)
- Eevee continues "living" between user interactions
- Activities are simulated and logged as memories

#### Activity Generation Engine
When time passes without user interaction:

**Hourly Activities** (Basic Needs Loop)
- Check internal state (hunger, energy, mood)
- Perform needs-driven actions:
  - Hungry → Search for berries
  - Tired → Find safe spot to nap
  - Bored → Explore surroundings
  - Lonely → Think about trainer

**Daily Events** (World Interactions)
- Encounter other Pokemon (NPCs)
- Discover new locations
- Find items or resources
- Weather changes affect behavior
- Random events (finds shiny stone, meets friendly Growlithe, etc.)

**Memory Worthy Moments** (Significance Threshold)
- Emotional intensity > 7/10
- Novel experiences (first time events)
- Social interactions
- Survival challenges
- Moments of joy or fear

#### Example Time Gap Simulation
```
User last interacted: Monday 8 AM
Current time: Friday 8 AM
Time elapsed: 96 hours

Generated timeline:
- Monday 10 AM: Got hungry, found Oran berries near stream
- Monday 2 PM: Napped under favorite tree
- Monday 6 PM: Heard strange sounds, felt scared, hid in den
- Tuesday 9 AM: Missed trainer, sat at meeting spot
- Tuesday 3 PM: Played with wild Pidgey, felt happy
- Wednesday 11 AM: Discovered new clearing with flowers
- Wednesday 8 PM: Thunderstorm, found shelter, felt anxious
- Thursday 10 AM: Practiced running, felt energetic
- Thursday 6 PM: Watched sunset, thought of trainer
- Friday 7 AM: Woke up excited, sensed trainer might return soon
```

---

### 3. Memory System Architecture

#### Memory Storage (Vector Database)
Using ChromaDB or similar for semantic memory retrieval.

**Memory Entry Structure**
```json
{
  "timestamp": "2025-10-21T14:30:00Z",
  "memory_type": "episodic",
  "content": "Trainer gave me a Pecha berry when I was sick",
  "emotion": "gratitude",
  "emotion_intensity": 8,
  "location": "trainer_home",
  "participants": ["trainer"],
  "significance": 9,
  "embedding": [vector],
  "tags": ["food", "care", "healing", "kindness"]
}
```

#### Memory Types

**Episodic Memories** (Specific Events)
- What happened, when, where, who was there
- Stored with full sensory detail
- High-emotion events more vivid
- Example: "The time trainer saved me from the Beedrill"

**Semantic Memories** (Facts & Knowledge)
- General knowledge about the world
- "Berries grow near water"
- "Thunder is scary but passes"
- "Trainer always comes back"

**Emotional Memories** (Feelings About Things)
- Associative emotional responses
- "Pokeballs = uncertainty and fear"
- "Trainer's voice = safety and warmth"
- "Rain = cozy den time"

**Procedural Memories** (Skills & Habits)
- How to do things
- "When scared, tail puffs up"
- "Best berry spots near the old tree"
- "Running in circles means playtime"

#### Memory Consolidation
- **Short-term (Working)**: Current context, last 10 interactions
- **Long-term**: Important memories stored in vector DB
- **Forgetting Mechanism**: Low-significance memories fade over weeks
- **Memory Strengthening**: Repeated similar experiences strengthen patterns

#### Memory Retrieval Process
1. User input analyzed for keywords/concepts
2. Vector similarity search retrieves top 5-10 relevant memories
3. Hippocampus presents memories to brain council
4. Memories influence brain region voting
5. Response reflects remembered context

---

### 4. Eevee's Internal State

#### Persistent Stats (Saved Between Sessions)
```json
{
  "personality": {
    "curiosity": 8,
    "bravery": 5,
    "playfulness": 9,
    "loyalty": 10,
    "independence": 6
  },
  "physical_state": {
    "hunger": 40,
    "energy": 70,
    "health": 95,
    "happiness": 85
  },
  "relationship": {
    "trust_level": 75,
    "bond_strength": 60,
    "time_together": "47 hours",
    "favorite_activities": ["playing", "being_petted", "exploring"],
    "fears": ["loud_noises", "being_alone_too_long"]
  },
  "world_state": {
    "current_location": "meadow_near_home",
    "time_of_day": "morning",
    "weather": "sunny",
    "inventory": ["Oran_berry", "smooth_stone"]
  }
}
```

#### Dynamic Modifiers
- Hunger affects patience and focus
- Low energy makes Eevee sleepy and less playful
- High happiness increases enthusiasm
- Weather affects mood (loves sun, anxious in storms)
- Time apart from trainer creates loneliness

---

### 5. World Model

#### Location System
Simple graph-based world with nodes and connections.

**Example Locations:**
- `trainer_home` - Safe, familiar, where you usually meet
- `meadow` - Open space, good for running
- `forest_edge` - Mysterious, sometimes scary
- `stream` - Source of water and berries
- `hidden_den` - Secret safe space only Eevee knows
- `sunny_hill` - Favorite napping spot

**Location Properties:**
- Safety level
- Resource availability (food, water, shelter)
- Weather exposure
- Exploration value (novelty)

#### Environmental Events
- Weather cycles (sunny, rainy, stormy, night)
- Seasonal changes (future expansion)
- Random encounters (wild Pokemon, items)
- Time-of-day atmosphere changes

---

### 6. NanoGPT Integration

#### API Usage Pattern

**Prompt Structure for Brain Council:**
```
You are simulating Eevee's [BRAIN_REGION] in a brain council.

Context:
- Eevee's current state: [hunger: 60, energy: 40, happiness: 70]
- Location: [meadow]
- Recent memory: [played with trainer yesterday, had fun]
- Situation: [trainer just asked "Want to go explore?"]

As the [BRAIN_REGION], what is your perspective and vote?
Respond in first-person as this brain region.
```

**Response Synthesis Prompt:**
```
You are Eevee, a curious and loyal Pokemon.

Brain council votes:
- Prefrontal Cortex: "Yes, but check if we're too tired"
- Amygdala: "Excited! Trainer = safe and fun!"
- Hippocampus: "Remember last exploration was really fun"
- Hypothalamus: "A bit hungry, but manageable"
- Cerebellum: "Tail wagging, ready to move!"

Winning decision: Enthusiastically agree to explore

Generate Eevee's response as natural dialogue/action.
Keep it authentic to a curious, energetic Eevee.
Include body language and sounds.
```

#### API Call Strategy
- **Brain Council Phase**: 5 API calls (one per region)
- **Response Generation**: 1 API call (synthesis)
- **Memory Summarization**: 1 API call (for time gaps)
- Total: ~7 calls per user interaction

#### Cost Management
- Cache common prompts
- Batch time-gap event generation
- Use shorter context for routine decisions

---

### 7. User Interface (Text-Based Terminal)

#### Core Commands
```
talk [message]        - Speak to Eevee
observe               - See what Eevee is currently doing
stats                 - View Eevee's current state
memories [query]      - Ask about specific memories
world                 - See current location and surroundings
give [item]           - Give Eevee an item
pet                   - Pet Eevee
play                  - Initiate playtime
debug brain           - [Dev] See brain council debate
debug time [hours]    - [Dev] Simulate time passage
exit                  - Save and quit
```

#### Display Format
```
===========================================
🌲 FOREST EDGE - LATE AFTERNOON 🌤️
===========================================

Eevee is sitting near the treeline, ears perked up, looking towards you with bright, curious eyes.
[Energy: ████████░░ 80% | Happiness: ██████████ 100% | Hunger: ████░░░░░░ 40%]

You: "Hey Eevee! Want to explore the forest?"

[Brain Council Deliberating...]

Eevee's tail starts wagging rapidly. *Eevee bounces on their paws excitedly*
"Vee! Veevee!" 

Eevee seems eager to explore with you, but glances back towards home briefly, 
as if remembering something. Then they look at you with complete trust and 
take a few steps towards the forest, looking back to make sure you're following.

===========================================
> _
```

---

### 8. Technical Stack

#### Core Components
- **Language**: Python 3.11+
- **Vector DB**: ChromaDB (local, no server required)
- **LLM API**: NanoGPT via REST API
- **State Storage**: SQLite for structured data, JSON for exports
- **Time Simulation**: APScheduler or custom datetime handling

#### File Structure
```
eevee-project/
├── main.py                 # Entry point, terminal UI
├── brain_council/
│   ├── __init__.py
│   ├── regions.py          # Individual brain region classes
│   ├── council.py          # Council orchestration
│   └── decision.py         # Voting and conflict resolution
├── memory/
│   ├── __init__.py
│   ├── vector_store.py     # ChromaDB wrapper
│   ├── memory_types.py     # Memory class definitions
│   └── consolidation.py    # Memory formation logic
├── world/
│   ├── __init__.py
│   ├── locations.py        # World graph
│   ├── time_simulation.py  # Autonomous activity generation
│   └── events.py           # Random event system
├── eevee/
│   ├── __init__.py
│   ├── state.py            # Eevee's internal state
│   ├── personality.py      # Personality traits
│   └── responses.py        # Response generation
├── llm/
│   ├── __init__.py
│   ├── nanogpt_client.py   # API wrapper
│   └── prompts.py          # Prompt templates
├── data/
│   ├── eevee_save.db       # SQLite database
│   ├── memories/           # ChromaDB storage
│   └── world_state.json    # Current world state
└── config.py               # Configuration settings
```

---

### 9. Implementation Phases

#### Phase 1: Foundation (Week 1)
- [ ] Basic terminal UI with text input/output
- [ ] Eevee state management (stats, location)
- [ ] Simple location system (3-5 locations)
- [ ] NanoGPT API integration
- [ ] Basic response generation (no brain council yet)

#### Phase 2: Brain Council (Week 2)
- [ ] Implement 5 brain regions as classes
- [ ] Decision voting system
- [ ] Brain council debate logging
- [ ] Debug mode to see internal deliberation
- [ ] Context-aware response modulation

#### Phase 3: Memory System (Week 3)
- [ ] ChromaDB integration
- [ ] Memory formation and storage
- [ ] Memory retrieval for context
- [ ] Memory types (episodic, semantic, emotional)
- [ ] Memory browser command

#### Phase 4: Time Passage (Week 4)
- [ ] Time tracking between sessions
- [ ] Activity generation engine
- [ ] Autonomous behavior simulation
- [ ] Memory creation during gaps
- [ ] Timeline summary generation

#### Phase 5: Polish & Expansion (Week 5+)
- [ ] Personality trait influence on decisions
- [ ] Complex emotional responses
- [ ] Item/inventory system
- [ ] Richer world interactions
- [ ] Special events and surprises
- [ ] Evolution considerations (future)

---

### 10. Key Design Principles

#### Authenticity Over Complexity
- Eevee should feel *real*, not robotic
- Imperfect responses are more believable
- Sometimes Eevee doesn't fully understand
- Emotions should be genuine and varied

#### Memory Makes Meaning
- Every significant interaction matters
- Patterns emerge from repeated experiences
- Eevee learns about you over time
- Continuity creates emotional investment

#### Time Creates Life
- Autonomous behavior makes Eevee feel alive
- Things happen when you're away
- Eevee has their own life and experiences
- Reunion after absence feels meaningful

#### Brain Council Transparency (Optional)
- Debug mode shows internal reasoning
- Understanding *why* Eevee acts a certain way
- Educational about decision-making
- Can be hidden for pure immersion

---

### 11. Example Interaction Flow

```
Session 1 (Monday 8 AM):
User: "Hey Eevee!"
Eevee: *perks up excitedly* "Vee! Veevee!" *runs in circles*
User: "Want to explore the forest?"
Eevee: *hesitates, tail twitches* "Vee..." *looks uncertain but trusting*
[Amygdala: forest=unknown=scary, Prefrontal: trainer=safe, decide yes]
Eevee follows you into the forest. You have a great adventure.
[Memory stored: "First forest exploration with trainer - scary but exciting"]

Session 2 (Friday 8 AM):
[Time gap: 96 hours simulated]
[Generated activities: napped, explored meadow, missed trainer, found berry]

User: "Hey Eevee! I'm back!"
Eevee: *SPRINTS towards you, tackles you with enthusiasm*
"VEE VEE VEEEE!!" *licks your face*
[Memory retrieved: "Trainer came back after 4 days - so happy!"]
[Amygdala: JOY = 10/10, Hypothalamus: loneliness → fulfilled]

User: "Miss me?"
Eevee: *nuzzles against you, tail wagging so hard their whole body shakes*
"Vee..." *soft, content sound*
[Eevee shows you the smooth stone they found, as if it's a gift]

User: "Want to explore the forest again?"
Eevee: *immediately excited, no hesitation this time*
"Vee vee!" *already heading towards forest*
[Hippocampus: "Last time was fun!" Memory influences confidence]
[Memory retrieved: "Forest exploration with trainer = positive experience"]
```

---

### 12. Configuration & Customization

#### Config File Options
```yaml
# NanoGPT Settings
nanogpt_api_key: "your_key_here"
nanogpt_endpoint: "https://api.nanogpt.com/v1/generate"
nanogpt_model: "gpt-2-medium"

# Time Settings
time_acceleration: 1.0  # 1.0 = real-time, 2.0 = 2x speed
activity_frequency: "hourly"
significant_event_chance: 0.15  # 15% chance per day

# Memory Settings
memory_significance_threshold: 6.0  # 0-10 scale
max_working_memory: 10
memory_retrieval_count: 5
forgetting_rate: 0.01  # Low-importance memories fade

# Eevee Personality (0-10 scale)
curiosity: 8
bravery: 5
playfulness: 9
loyalty: 10
independence: 6

# World Settings
starting_location: "trainer_home"
weather_change_frequency: "daily"
enable_random_events: true

# Debug Settings
show_brain_council: false  # Toggle internal deliberation
show_memory_retrieval: false
verbose_logging: true
```

---

### 13. Future Expansion Ideas

#### Advanced Features
- **Voice Input**: Speak to Eevee naturally
- **Multiple Pokemon**: Have Eevee interact with other Pokemon
- **Evolution Path**: Trigger evolution based on relationship
- **Seasons**: World changes over months
- **Dreams**: Eevee "dreams" during sleep, processing memories
- **Moods**: Complex emotional states beyond basic stats
- **Learning**: Eevee develops new behaviors over time

#### Technical Improvements
- **Fine-tuned Model**: Train custom Eevee personality model
- **Better Time Sim**: More sophisticated activity generation
- **Rich Media**: ASCII art for locations/emotions
- **Mobile App**: Port to mobile with notifications
- **Multi-modal**: Image generation for what Eevee "sees"

---

## Getting Started

1. Set up Python environment with dependencies
2. Configure NanoGPT API credentials
3. Initialize ChromaDB and SQLite databases
4. Run `python main.py` to meet your Eevee
5. Start building memories together

---

## Notes for Claude Code

This specification is designed to be implemented iteratively. Start with Phase 1 to establish the foundation, then layer on complexity. Each phase should result in a playable, testable version.

The most critical aspects for the "impressive experience":
1. **Realistic memory** - Eevee remembers your relationship authentically
2. **Autonomous life** - Things happen when you're away
3. **Emotional authenticity** - Brain council creates genuine, varied responses
4. **Continuity** - Every interaction builds on the last

The goal is not perfect AI, but a Pokemon that feels like it truly exists.
