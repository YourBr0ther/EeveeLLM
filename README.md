# EeveeLLM - Your Living Pokemon Companion

An AI-powered Eevee companion with realistic brain processes, autonomous behavior, and genuine memory formation. Built with a unique "brain council" architecture where different brain regions debate and influence decisions.

## Features

### Currently Implemented (Phases 1-2)

**Phase 1: Foundation** ✅
- ✅ Interactive terminal interface with color support
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
- ✅ **5 Brain Regions**: Prefrontal Cortex (logic), Amygdala (emotion), Hippocampus (memory), Hypothalamus (needs), Cerebellum (instinct)
- ✅ **Weighted Voting System**: Each region votes with reasoning and confidence
- ✅ **Dynamic Weight Adjustments**: Weights change based on context (e.g., Amygdala dominates under threat)
- ✅ **Consensus Calculation**: Measures how unified or conflicted Eevee feels
- ✅ **Debug Visualization**: See internal deliberation with `debug brain` command
- ✅ **Context-Aware Decisions**: Responses reflect brain council's reasoning and emotional state

### Coming Soon (Phases 3-5)
- 🔜 Vector-based memory system with ChromaDB (Phase 3)
- 🔜 Memory consolidation, retrieval, and types (Phase 3)
- 🔜 Autonomous time passage simulation (Phase 4)
- 🔜 Activity generation during time gaps (Phase 4)
- 🔜 Random world events and surprises (Phase 5)
- 🔜 Evolution system (Phase 5)

## Installation

### Quick Install (Recommended)

```bash
cd /Users/christophervance/EeveeLLM
pip install colorama pyyaml python-dateutil requests
python main.py
```

### Or use the install script:

```bash
./install.sh
python main.py
```

### Configure NanoGPT API (Optional)

The app works in **fallback mode** without an API key! But if you have a NanoGPT API key:

```bash
export NANOGPT_API_KEY="your_api_key_here"
```

Or edit `config.yaml`:
```yaml
nanogpt_api_key: "your_key_here"
```

## Usage

### Basic Commands

- `talk [message]` - Speak to Eevee
- `pet` - Pet Eevee (increases happiness and trust)
- `play` - Play with Eevee (increases bond, costs energy)
- `give [item]` - Give Eevee an item (e.g., "give Oran Berry")
- `observe` - See what Eevee is currently doing
- `stats` - View detailed stats
- `world` - See current location and surroundings
- `go [location]` - Travel to a connected location
- `help` - Show all commands
- `debug brain` - Toggle brain council visualization
- `debug on/off` - Toggle full debug mode
- `exit` - Save and quit

### Example Interaction

```
> talk Hey Eevee!
You: Hey Eevee!

Eevee: *Eevee perks up excitedly* Vee! Veevee! *bounces on paws happily*

> play
You: *initiates playtime*

Eevee: *Eevee runs in excited circles, pouncing on their own tail* Vee vee!

> go meadow
Traveling to Wide Meadow...

> observe
Eevee seems cheerful and full of energy.

Eevee: *Eevee sniffs around excitedly* Vee! *discovering new scents*
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
eevee-project/
├── main.py                 # Entry point
├── config.py               # Configuration system
├── ui.py                   # Terminal UI
├── brain_council/          # Brain decision system (Phase 2)
├── memory/                 # Vector memory storage (Phase 3)
├── world/                  # Location and world system
│   └── locations.py
├── eevee/                  # Core Eevee logic
│   ├── state.py           # State management
│   ├── personality.py      # Personality traits
│   └── responses.py        # Response generation
├── llm/                    # LLM integration
│   ├── nanogpt_client.py  # API client
│   └── prompts.py          # Prompt templates
└── data/                   # Persistent data
    ├── eevee_save.db       # SQLite database
    └── memories/           # ChromaDB storage (Phase 3)
```

## Development Roadmap

### Phase 1: Foundation ✅
- Basic terminal UI
- State management
- Simple location system
- NanoGPT integration
- Basic responses

### Phase 2: Brain Council 🔜
- 5 brain region classes
- Voting system
- Internal deliberation
- Context-aware modulation
- Debug visualization

### Phase 3: Memory System 🔜
- ChromaDB integration
- Memory types (episodic, semantic, emotional, procedural)
- Memory retrieval
- Memory consolidation
- Memory browser

### Phase 4: Time Passage 🔜
- Time tracking
- Activity generation
- Autonomous behavior
- Memory formation during gaps
- Timeline summaries

### Phase 5: Polish & Expansion 🔜
- Personality influence
- Complex emotions
- Rich world interactions
- Special events
- Evolution considerations

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
