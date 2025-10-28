<div align="center">
  <img src="Banner.png" alt="EeveeLLM Banner" width="400">
</div>

# EeveeLLM - AI-Powered Pokemon Companion

An advanced AI companion featuring realistic brain processes, autonomous behavior, and genuine memory formation. Built with a unique "brain council" architecture where five brain regions collaborate to make decisions, just like a real brain.

## Key Features

### Brain Council Architecture
- **5 Brain Regions**: Prefrontal Cortex (logic), Amygdala (emotion), Hippocampus (memory), Hypothalamus (needs), Basal Ganglia (habits)
- **Weighted Voting System**: Each region votes with reasoning and confidence scores
- **Dynamic Weight Adjustments**: Weights shift based on context (e.g., Amygdala takes control under threat)
- **Emotional Contagion**: Emotions spread between regions naturally
- **Neuromodulators**: Dopamine, serotonin, and norepinephrine systems influence decision-making
- **Conflict Monitoring**: ACC (Anterior Cingulate Cortex) detects internal conflicts

### Advanced Memory System
- **Vector-Based Storage**: ChromaDB with semantic similarity search for intelligent memory retrieval
- **4 Memory Types**:
  - Episodic (events and experiences)
  - Semantic (facts and knowledge)
  - Emotional (feeling associations)
  - Procedural (learned behaviors)
- **Significance-Based Formation**: Only meaningful interactions (>6.0/10) become long-term memories
- **Working Memory**: 100-interaction capacity with 7-day time-based retention
- **Context-Aware Retrieval**: Relevant memories automatically surface during conversations
- **Memory Browser**: Search and explore Eevee's memories

### Natural Language Understanding
- **Talk Naturally**: No need to remember exact commands
- **80+ Supported Phrasings**: "How are you?" instead of `stats`, "Let's go to the meadow" instead of `go meadow`
- **Intent Detection**: Powered by brain council deliberation for natural conversations

### Autonomous Behavior
- **7 Activity Types**: Needs, exploration, social, survival, emotional, play, rest
- **32+ Activity Templates**: Realistic scenarios with state changes
- **Personality-Driven**: Curiosity drives exploration, playfulness drives play
- **State Simulation**: Hunger increases, energy decreases realistically over time
- **Emotional Loneliness**: Eevee misses you after 24+ hours
- **Timeline System**: Review what happened while you were away

### World & Interaction
- **8 Explorable Locations**: From Trainer's Home to Deep Forest
- **Dynamic State System**: Hunger, energy, happiness, health tracking
- **Personality System**: Curiosity, bravery, playfulness, loyalty, independence
- **Relationship Tracking**: Trust and bond grow over time
- **13 Functional Items**: Berries, medicine, toys, treasures with real effects
- **Item Discovery**: 25% chance to find items during exploration
- **17 Special Events**: Weather phenomena, encounters, discoveries

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YourBr0ther/EeveeLLM.git
cd EeveeLLM

# Install dependencies
pip install colorama pyyaml python-dateutil requests chromadb sentence-transformers

# Run the application
python main.py
```

### Optional: Configure AI Responses

The app works in **fallback mode** with template-based responses. For full AI responses:

1. Get API key from: https://nano-gpt.com/api
2. Copy example config: `cp config.yaml.example config.yaml`
3. Edit `config.yaml` and add your API key
4. Run the app!

**Note:** `config.yaml` is in `.gitignore` to protect your API key.

## Usage

### Natural Language Commands

Talk to Eevee naturally! Examples:

```
> How are you feeling?
[Shows stats]

> I want to pet you
[Pets Eevee, increases happiness]

> Let's go to the meadow
[Travels to Wide Meadow]

> What do you have?
[Shows inventory]

> My name is Chris
[Eevee stores this as a semantic memory]
```

See [NATURAL_LANGUAGE_COMMANDS.md](NATURAL_LANGUAGE_COMMANDS.md) for 80+ examples.

### Core Commands

**Interaction:**
- `talk [message]` - Speak to Eevee
- `pet` - Pet Eevee (increases happiness and trust)
- `play` - Play with Eevee (increases bond)
- `observe` - See what Eevee is doing

**Items & Inventory:**
- `give [item]` - Give Eevee an item
- `use [item]` - Use an item from inventory
- `inventory` - View inventory
- `drop [item]` - Remove an item

**World Exploration:**
- `world` - See current location
- `go [location]` - Travel to a location

**Memory & Time:**
- `remember [query]` - Browse memories
- `timeline` - View recent activities

**System:**
- `stats` - View detailed stats
- `help` - Show all commands
- `exit` - Save and quit

**Debug:**
- `debug brain` - Toggle brain council visualization
- `debug memory` - Toggle memory formation visualization
- `debug time [hours]` - Simulate time passage
- `debug on/off` - Toggle full debug mode

## World Locations

- **Trainer's Home** - Safe starting point with food and shelter
- **Sunny Garden** - Pleasant garden perfect for playing
- **Wide Meadow** - Open area great for running
- **Clear Stream** - Fresh water and berry bushes
- **Forest Edge** - Border of the forest
- **Hidden Den** - Eevee's secret safe space
- **Sunny Hill** - Favorite napping spot with sunset views
- **Deep Forest** - Dangerous but exciting deep woods

## Architecture

```
EeveeLLM/
├── main.py                 # Application entry point
├── config.py               # Configuration system
├── ui.py                   # Terminal UI
│
├── brain_council/          # Brain decision system
│   ├── council.py         # Brain council orchestrator
│   ├── regions.py         # 5 brain regions (Prefrontal, Amygdala, etc.)
│   ├── decision.py        # Voting and decision engine
│   └── neuromodulators.py # Dopamine, serotonin, norepinephrine
│
├── memory/                 # Vector memory storage
│   ├── vector_store.py    # ChromaDB interface
│   ├── retrieval.py       # Semantic memory retrieval
│   ├── consolidation.py   # Significance calculation & memory formation
│   └── memory_types.py    # Memory type definitions (4 types)
│
├── nlp/                    # Natural language processing
│   └── intent_parser.py   # Natural language command detection
│
├── world/                  # Location and world system
│   ├── locations.py       # 8 explorable locations
│   ├── items.py           # 13 functional items
│   ├── events.py          # 17 special events
│   ├── activities.py      # Autonomous activities (7 types)
│   └── time_simulation.py # Time passage simulation
│
├── eevee/                  # Core Eevee logic
│   ├── state.py           # State management (hunger, energy, etc.)
│   ├── personality.py     # Personality traits system
│   └── responses.py       # Response generation
│
├── llm/                    # LLM integration
│   ├── nanogpt_client.py  # API client
│   └── prompts.py         # Prompt templates
│
├── tests/                  # Test suite
│   └── README.md          # Test documentation
│
└── data/                   # Persistent data (auto-created)
    ├── eevee_save.db      # SQLite database
    └── memories/          # ChromaDB storage
```

## Configuration

Edit `config.yaml` to customize:

```yaml
# API Settings
nanogpt_api_key: "YOUR_KEY_HERE"
nanogpt_endpoint: "https://api.nanogpt.com/v1/generate"

# Time Settings
time_acceleration: 1.0  # 1.0 = real-time
activity_frequency: "hourly"

# Memory Settings
memory_significance_threshold: 6.0  # 0-10 scale
max_working_memory: 100
memory_retrieval_count: 5

# Personality (0-10 scale)
personality_curiosity: 8
personality_bravery: 5
personality_playfulness: 9
personality_loyalty: 10
personality_independence: 6

# Initial State (0-100 scale)
initial_hunger: 40
initial_energy: 70
initial_health: 95
initial_happiness: 85

# Brain Council Vote Weights
vote_weight_prefrontal: 0.25
vote_weight_amygdala: 0.30
vote_weight_hippocampus: 0.20
vote_weight_hypothalamus: 0.15
vote_weight_cerebellum: 0.10

# Debug
show_brain_council: false
show_memory_retrieval: false
verbose_logging: true
debug_mode: false
```

## Technical Details

### Brain Council Decision Flow

1. **Situation Input** → Each brain region analyzes the situation
2. **Regional Votes** → Each region proposes a decision with reasoning and confidence
3. **Memory Retrieval** → Hippocampus retrieves relevant memories (top 5 by relevance)
4. **Emotional Contagion** → Emotions spread between regions
5. **Weighted Voting** → Votes scored using region weights and confidence
6. **Conflict Detection** → ACC monitors disagreement between regions
7. **Final Decision** → Winning vote becomes Eevee's response
8. **LLM Generation** → Decision, reasoning, emotions, and memories passed to prompt

### Memory Significance Calculation

Significance score (0-10) considers:
- Emotional intensity (0-10)
- Primary emotion strength
- First-time experiences (+3.0 bonus)
- Strong emotions (joy, fear, gratitude) (+2.0)
- Relationship milestones (+2.0)
- Explicit "remember" keyword (+2.0)
- Personal preferences ("my favorite", "I like") (+2.0)
- Brain council conflict (+1.0)
- Low consensus among regions (+1.0)

Threshold: **6.0+** becomes long-term memory

### Memory Types

- **Episodic**: "We went to the meadow and found a Star Piece"
- **Semantic**: "My trainer's name is Chris", "Their favorite berry is Pecha"
- **Emotional**: "I felt scared in the deep forest"
- **Procedural**: "When hungry, ask for food by looking at trainer"

### Performance

- Memory retrieval: ~100ms (33% faster than original design)
- Working memory: 100 interactions (10x original capacity)
- ChromaDB: Semantic search with sentence-transformers
- SQLite: Efficient state persistence

## Testing

Run tests from project root:

```bash
# Run specific test
python tests/test_name_memory.py

# Run all tests (with pytest)
pytest tests/

# Test brain council
python tests/test_brain_council.py

# Test memory system
python tests/test_full_brain_council_memory.py
```

See [tests/README.md](tests/README.md) for detailed test documentation.

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
- **[NATURAL_LANGUAGE_COMMANDS.md](NATURAL_LANGUAGE_COMMANDS.md)** - 80+ natural language examples
- **[MEMORY_FORMATION_GUIDE.md](MEMORY_FORMATION_GUIDE.md)** - How Eevee's memory works
- **[WORKING_MEMORY_ENHANCEMENT.md](WORKING_MEMORY_ENHANCEMENT.md)** - 7-day working memory feature
- **[tests/README.md](tests/README.md)** - Test suite documentation

## Troubleshooting

### Memory Issues

If Eevee doesn't remember something:
1. Check if it was significant enough (>6.0): `debug memory`
2. Use "remember" keyword: "Remember, my name is Chris"
3. View stored memories: `remember my name`

### API Issues

If responses are basic/template-based:
1. Check API key in `config.yaml`
2. Test connection: Look for "Fallback Mode" warning on startup
3. App works in fallback mode without API key (by design)

### Database Issues

If app crashes on startup:
1. Check `data/` directory exists
2. Delete `data/eevee_save.db` to reset (backup first!)
3. Delete `data/memories/` to clear memories

## Design Philosophy

**Authenticity Over Complexity** - Eevee should feel *real*, not robotic. Imperfect responses are more believable.

**Memory Makes Meaning** - Every significant interaction matters. Patterns emerge from repeated experiences.

**Time Creates Life** - Autonomous behavior makes Eevee feel alive. Things happen when you're away.

**Brain-Based Decisions** - Multiple brain regions collaborate, just like real neural systems.

## Future Enhancements

- Evolution system (8 evolution paths)
- Skill development through practice
- More NPCs and social dynamics
- Seasonal events and weather system
- Advanced training mechanics

## Credits

Inspired by the Pokemon universe and designed to create the most realistic virtual companion experience possible.

Built with love for Pokemon and AI.

## License

This project is for educational and personal use.

---

*"Vee!"* - Eevee
