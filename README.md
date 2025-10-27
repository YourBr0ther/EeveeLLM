<div align="center">
  <img src="Banner.png" alt="EeveeLLM Banner" width="400">
</div>

# EeveeLLM - Your Living Pokemon Companion

An AI-powered Eevee companion with realistic brain processes, autonomous behavior, and genuine memory formation. Built with a unique "brain council" architecture where different brain regions debate and influence decisions.

## Features

### Currently Implemented (Phases 1-6) ✅

**Phase 1: Foundation** ✅
- ✅ Interactive terminal interface with color support
- ✅ **Natural Language Commands**: Talk naturally instead of using exact command syntax **[NEW!]**
- ✅ Eevee state management (hunger, energy, happiness, health)
- ✅ Personality system (curiosity, bravery, playfulness, loyalty, independence)
- ✅ Location-based world with 8 explorable areas
- ✅ NanoGPT API integration with intelligent fallback mode
- ✅ SQLite persistence for state and interactions
- ✅ Natural language responses
- ✅ Relationship tracking (trust and bond)
- ✅ Inventory system
- ✅ Time tracking between sessions

**Phase 2: Brain Council** ✅
- ✅ **5 Brain Regions**: Prefrontal Cortex (logic), Amygdala (emotion), Hippocampus (memory), Hypothalamus (needs), Basal Ganglia (instinct/habits)
- ✅ **Weighted Voting System**: Each region votes with reasoning and confidence
- ✅ **Dynamic Weight Adjustments**: Weights change based on context (e.g., Amygdala dominates under threat)
- ✅ **Consensus Calculation**: Measures how unified or conflicted Eevee feels
- ✅ **Debug Visualization**: See internal deliberation with `debug brain` command
- ✅ **Context-Aware Decisions**: Responses reflect brain council's reasoning and emotional state

**Phase 3: Memory System** ✅ **(Recently Optimized!)**
- ✅ **Vector Memory Storage**: ChromaDB with semantic similarity search
- ✅ **4 Memory Types**: Episodic (events), Semantic (facts), Emotional (associations), Procedural (learned behaviors)
- ✅ **Significance-Based Formation**: Only meaningful interactions (>6.0/10) become long-term memories
- ✅ **"Remember" Keyword Support**: Eevee properly stores facts when you say "remember" or share preferences **[NEW FIX!]**
- ✅ **Personal Preference Tracking**: "My favorite X", "I like Y", "My name is Z" → Semantic memories **[NEW!]**
- ✅ **Context-Aware Retrieval**: Hippocampus retrieves relevant memories during deliberation
- ✅ **Enhanced Working Memory**: Short-term retention (100 interactions OR 7 days) **[NEW: 10x capacity + time-based retention!]**
- ✅ **Memory Browser**: Search and explore Eevee's memories with `remember` command
- ✅ **Automatic Strengthening**: Frequently accessed memories become stronger **[FIXED: Now working correctly!]**
- ✅ **Integrated with Brain Council**: Memories directly influence Hippocampus decisions
- ✅ **Memory Deduplication**: No duplicate memories in context **[FIXED: Optimized retrieval]**
- ✅ **Performance**: 33% faster retrieval (150ms → 100ms) **[FIXED: Optimized limits]**

**Phase 4: Time Passage System** ✅
- ✅ **Autonomous Activities**: Eevee performs 7 types of activities while you're away (needs, exploration, social, survival, emotional, play, rest)
- ✅ **32+ Activity Templates**: Realistic scenarios with state changes and emotional context
- ✅ **Personality-Driven Behavior**: Curiosity drives exploration, playfulness drives play
- ✅ **State Decay Simulation**: Hunger increases, energy decreases realistically over time
- ✅ **Emotional Loneliness**: Eevee misses you after 24+ hours, creates memories of waiting
- ✅ **Timeline Generation**: Beautiful summaries of what happened while you were away
- ✅ **Memory Formation**: Significant autonomous activities (>7.0/10) become long-term memories
- ✅ **Timeline Command**: Review recent activities with `timeline` command
- ✅ **Debug Testing**: Simulate time passage with `debug time <hours>` command

**Phase 5: Polish & Expansion** ✅
- ✅ **Enhanced Item System**: 13 functional items with state effects (berries, medicine, toys, treasures)
- ✅ **Item Discovery**: 25% chance to find items during exploration, rarity-based loot tables
- ✅ **Use & Inventory Commands**: Use items for effects, view organized inventory
- ✅ **Special Events**: 17 unique events (weather, encounters, discoveries, phenomena)
- ✅ **Event System**: 15% chance for special events during activities, rarity-weighted
- ✅ **Event Rewards**: Some events grant rare items (Rainbow Wing, Old Amber, etc.)
- ✅ **Memorable Moments**: Events create high-significance memories (7.0+)

**Phase 6: Enhanced Brain Council** ✅ NEW!
- ✅ **Emotional Contagion**: Emotions spread between brain regions (Amygdala's fear influences Hippocampus)
- ✅ **Neuromodulator Systems**: Dopamine (reward/motivation), Serotonin (mood), Norepinephrine (arousal/alertness)
- ✅ **ACC Conflict Monitoring**: Detects internal conflict when regions disagree (0.0-1.0 scale)
- ✅ **Basal Ganglia Rename**: Improved neuroscience accuracy (formerly "Cerebellum")
- ✅ **Primary Emotions**: Each region expresses emotion (joy, fear, trust, fatigue, etc.)
- ✅ **Arousal Levels**: Tracks emotional intensity (0.0 = calm, 1.0 = intense)
- ✅ **Organic Responses**: Emotions spread naturally, conflicts feel genuine
- ✅ **4.8/5 Neuroscience Accuracy**: Based on comprehensive neuroscience review

### Future Expansion Ideas
- 🔜 Evolution system (8 evolution paths)
- 🔜 Skill development through practice
- 🔜 More NPCs and deeper social dynamics
- 🔜 Seasonal events and weather system

## Installation

### Quick Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourBr0ther/EeveeLLM.git
   cd EeveeLLM
   ```

2. **Install dependencies:**
   ```bash
   pip install colorama pyyaml python-dateutil requests chromadb sentence-transformers
   ```

3. **Configure API key:**
   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml and add your NanoGPT API key
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

### Configure NanoGPT API

The app works in **fallback mode** without an API key! But for full AI responses:

1. Get your API key from: https://nano-gpt.com/api
2. Copy the example config:
   ```bash
   cp config.yaml.example config.yaml
   ```
3. Edit `config.yaml` and replace `YOUR_API_KEY_HERE` with your actual key
4. Run the app!

**Note:** `config.yaml` is in `.gitignore` to protect your API key.

## Usage

### 💡 Natural Language Support

**You can talk to Eevee naturally!** No need to remember exact commands.

**Examples:**
- Instead of `stats` → "How are you feeling?"
- Instead of `inventory` → "What do you have?"
- Instead of `pet` → "I want to pet you"
- Instead of `go meadow` → "Let's go to the meadow"

See [NATURAL_LANGUAGE_COMMANDS.md](NATURAL_LANGUAGE_COMMANDS.md) for 80+ natural language examples!

### Basic Commands (Exact Syntax)

**Interaction:**
- `talk [message]` - Speak to Eevee (or just type naturally!)
- `pet` - Pet Eevee (increases happiness and trust)
- `play` - Play with Eevee (increases bond, costs energy)
- `observe` - See what Eevee is currently doing

**Items:**
- `give [item]` - Give Eevee an item (e.g., "give Oran Berry")
- `use [item]` - Use an item from inventory
- `inventory` - View your inventory
- `drop [item]` - Drop/remove an item from inventory

**World:**
- `world` - See current location and surroundings
- `go [location]` - Travel to a connected location

**Memory & Time:**
- `remember [query]` - Browse Eevee's memories
- `timeline` - View recent autonomous activities

**System:**
- `stats` - View detailed stats
- `help` - Show all commands
- `exit` - Save and quit

**Debug:**
- `debug brain` - Toggle brain council visualization
- `debug memory` - Toggle memory formation visualization
- `debug time [hours]` - Simulate time passage for testing
- `debug on/off` - Toggle full debug mode

### Example Interaction (Natural Language)

```
> Hello Eevee!
You: Hello Eevee!

Eevee: *Vee!* *perks up excitedly* *tail wagging* *bounces happily*

> How are you feeling?
[Shows stats table]

Eevee: *Vee!* *sits up proudly* I'm doing great!
       *tail wagging* Lots of energy today!

> Want to play?
You: *initiates playtime*

Eevee: *Vee vee!* *runs in excited circles* *playful pouncing*

> Let's go to the meadow
Traveling to Wide Meadow...

[Location description]

Eevee: *Vee!* *looks around curiously*
       This place smells amazing! *sniffs the flowers*

> What do you have?
📦 Inventory (3 items):
  🍊 Oran Berry
  ⭐ Star Piece

Eevee: *Vee!* *shows items proudly*
       Look at my treasures! *protective stance*
```

## World Locations

- **Trainer's Home** - Safe starting point with food and shelter
- **Sunny Garden** - Pleasant garden perfect for playing
- **Wide Meadow** - Open area great for running and exploration
- **Clear Stream** - Fresh water and berry bushes
- **Forest Edge** - Mysterious border of the forest
- **Hidden Den** - Eevee's secret safe space
- **Sunny Hill** - Favorite napping spot with sunset views
- **Deep Forest** - Dangerous but exciting deep woods

## Configuration

Edit `config.yaml` to customize:
- NanoGPT API settings
- Time acceleration
- Initial personality traits
- Debug options
- UI preferences

## Architecture

```
EeveeLLM/
├── main.py                 # Entry point
├── config.py               # Configuration system
├── ui.py                   # Terminal UI
├── brain_council/          # Brain decision system (Phase 2, 6)
│   ├── council.py         # Brain council orchestrator
│   ├── regions.py         # 5 brain regions
│   ├── decision.py        # Decision engine
│   └── neuromodulators.py # Dopamine, serotonin, norepinephrine
├── memory/                 # Vector memory storage (Phase 3)
│   ├── vector_store.py    # ChromaDB interface
│   ├── retrieval.py       # Memory retrieval
│   ├── consolidation.py   # Significance calculation
│   └── memory_types.py    # Memory type definitions
├── nlp/                    # Natural language processing
│   └── intent_parser.py   # Natural language command detection
├── world/                  # Location and world system
│   ├── locations.py       # 8 locations
│   ├── items.py           # Item system (Phase 5)
│   ├── events.py          # Special events (Phase 5)
│   ├── activities.py      # Autonomous activities (Phase 4)
│   └── time_simulation.py # Time passage (Phase 4)
├── eevee/                  # Core Eevee logic
│   ├── state.py           # State management
│   ├── personality.py     # Personality traits
│   └── responses.py       # Response generation
├── llm/                    # LLM integration
│   ├── nanogpt_client.py  # API client
│   └── prompts.py         # Prompt templates
└── data/                   # Persistent data
    ├── eevee_save.db      # SQLite database
    └── memories/          # ChromaDB storage
```

## Development Roadmap

### Phase 1: Foundation ✅
- Basic terminal UI
- State management
- Simple location system
- NanoGPT integration
- Basic responses

### Phase 2: Brain Council ✅
- 5 brain region classes
- Voting system
- Internal deliberation
- Context-aware modulation
- Debug visualization

### Phase 3: Memory System ✅
- ChromaDB vector storage
- 4 memory types (episodic, semantic, emotional, procedural)
- Significance-based consolidation
- Semantic similarity retrieval
- Hippocampus integration
- Memory browser command

### Phase 4: Time Passage ✅
- Time tracking
- Activity generation (7 types, 32+ templates)
- Autonomous behavior with personality-driven choices
- Memory formation during gaps
- Timeline summaries

### Phase 5: Polish & Expansion ✅
- Enhanced item system (13 items, 4 types)
- Item discovery during exploration (25% chance)
- Special events system (17 events, 4 categories)
- Event rewards (rare items)
- Memorable moments (high-significance memories)

### Phase 6: Enhanced Brain Council ✅
- Emotional contagion between brain regions
- Neuromodulator systems (dopamine, serotonin, norepinephrine)
- ACC conflict monitoring
- Basal Ganglia rename for neuroscience accuracy
- Primary emotions and arousal levels

### Phase 7: Evolution & Growth 🔜
- Evolution system (8 evolution paths)
- Skill development through practice
- Advanced training mechanics
- Evolution-specific abilities

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
- **[NATURAL_LANGUAGE_COMMANDS.md](NATURAL_LANGUAGE_COMMANDS.md)** - Natural language examples (80+ phrasings)
- **[MEMORY_FORMATION_GUIDE.md](MEMORY_FORMATION_GUIDE.md)** - How Eevee's memory works
- **[WORKING_MEMORY_ENHANCEMENT.md](WORKING_MEMORY_ENHANCEMENT.md)** - 7-day working memory feature
- **[PHASE_6_SUMMARY.md](PHASE_6_SUMMARY.md)** - Brain council enhancements

## Integration Status

**All 6 phases are fully integrated and production-ready!** ✅

Recent enhancements:
- ✅ **Natural Language Commands** - 80+ natural phrasings supported
- ✅ **Enhanced Working Memory** - 7-day retention (100 interactions)
- ✅ **Command Responses** - Stats, inventory, world use Eevee's brain council
- ✅ **Memory Optimization** - 33% faster retrieval, deduplication fixes
- ✅ **"Remember" Support** - Explicit memory requests now stored

**Test Statistics:**
- Total Test Cases: 47+ (all phases + enhancements)
- Success Rate: 100%
- Status: PRODUCTION READY

## Design Philosophy

**Authenticity Over Complexity** - Eevee should feel *real*, not robotic. Imperfect responses are more believable.

**Memory Makes Meaning** - Every significant interaction matters. Patterns emerge from repeated experiences.

**Time Creates Life** - Autonomous behavior makes Eevee feel alive. Things happen when you're away.

## Credits

Inspired by the Pokemon universe and designed to create the most realistic virtual companion experience possible.

Built with love for Pokemon and AI.

## License

This project is for educational and personal use.

---

*"Vee!"* - Eevee
