# EeveeLLM Quick Start Guide

## Installation (2 minutes)

1. **Install Python dependencies:**
   ```bash
   cd /Users/christophervance/EeveeLLM
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

That's it! The app works in fallback mode without any API keys.

---

## Optional: NanoGPT API Setup

If you have a NanoGPT API key:

```bash
export NANOGPT_API_KEY="your_key_here"
```

Or edit `config.yaml`:
```yaml
nanogpt_api_key: "your_key_here"
```

---

## First Time Experience

When you first run the app:

```
╔══════════════════════════════════════════════════════════════════════╗
║                    Welcome to EeveeLLM                               ║
║              Your Eevee companion is waiting for you!                ║
╚══════════════════════════════════════════════════════════════════════╝

🌲 TRAINER'S HOME - MORNING ☀️
==========================================

*Eevee perks up excitedly* Vee! Veevee! *bounces happily*

> _
```

---

## Essential Commands

### Talk to Eevee
```
> talk Hey Eevee!
> Hello buddy!
> Want to play?
```

### Physical Interaction
```
> pet                    # Pet Eevee (+happiness, +trust)
> play                   # Play together (+bond, -energy)
> give Oran Berry       # Give items
```

### Explore the World
```
> world                  # See current location
> go meadow             # Travel to meadow
> go stream             # Travel to stream
```

### Check Status
```
> observe               # What is Eevee doing?
> stats                 # Detailed stats
```

### Debug Features
```
> debug brain           # Toggle brain council visualization
> debug on              # Full debug mode
> debug off             # Disable debug
```

---

## See the Brain Council in Action

**This is the coolest feature!**

1. Enable brain council visualization:
   ```
   > debug brain
   ```

2. Ask Eevee something:
   ```
   > talk Want to explore the deep forest?
   ```

3. Watch the deliberation:
   ```
   ======================================================================
   BRAIN COUNCIL DELIBERATION
   ======================================================================

   1. Amygdala ← WINNER
      Decision: fear_disagree
      Reasoning: Scary... Unknown places make me nervous. Too dangerous!
      Score: 0.324 | Confidence: 0.90 | Emotional: 1.00

   2. Prefrontal Cortex
      Decision: suggest_rest_first
      Reasoning: Logic suggests we prepare first. Low safety could be dangerous.
      Score: 0.210 | Confidence: 0.80 | Emotional: 0.30

   3. Hippocampus
      Decision: no_pattern
      Reasoning: This is new. No past experience to guide us.
      Score: 0.120 | Confidence: 0.40 | Emotional: 0.40

   ... (more regions)

   Consensus Level: 0.42 (uncertain)
   Dominant Emotion: fearful
   ```

You'll see Eevee's internal conflict play out!

---

## Fun Things to Try

### Build Trust
```
> pet
> play
> talk You're such a good Eevee!
```

### Explore Together
```
> go meadow
> go stream
> go sunny hill
```

### Give Gifts
```
> give Oran Berry
> give Pecha Berry
> give smooth stone
```

### Different Locations
Each location has different safety levels and resources:
- **Safe**: Trainer's Home, Garden, Sunny Hill
- **Moderate**: Meadow, Stream, Hidden Den
- **Dangerous**: Forest Edge, Deep Forest

Watch how Eevee's brain council reacts differently!

---

## Understanding Stats

### Physical State (0-100)
- **Hunger**: Goes up over time, feed berries to reduce
- **Energy**: Decreases with play, rest to restore
- **Health**: Stays high unless in danger
- **Happiness**: Affected by interactions and treatment

### Relationship (0-100)
- **Trust**: Built through petting, caring actions
- **Bond**: Strengthened through playing together

### Personality (0-10)
- **Curiosity**: How much Eevee wants to explore
- **Bravery**: Willingness to face danger
- **Playfulness**: Desire to play and have fun
- **Loyalty**: Devotion to trainer
- **Independence**: Self-sufficiency

These slowly evolve based on experiences!

---

## Tips for Best Experience

1. **Enable brain council debug**: See the magic happen!
   ```
   > debug brain
   ```

2. **Try different scenarios**:
   - Ask to explore when Eevee is tired
   - Try going to dangerous places
   - Offer food when hungry vs. when full

3. **Watch how context matters**:
   - Same question gets different responses based on:
     - Current location (safety level)
     - Physical state (tired, hungry)
     - Relationship level (trust, bond)

4. **Build your relationship**:
   - Pet regularly for trust
   - Play for bonding
   - Give items as gifts

5. **Experiment**:
   - Go to different locations
   - Try different times (stats change)
   - See how Eevee reacts when needs are urgent

---

## Example Session

```
> python main.py

Welcome to EeveeLLM!

🌲 TRAINER'S HOME - MORNING ☀️

*Eevee perks up excitedly* Vee! Veevee! *bounces happily*

> debug brain
[Brain council visualization enabled]

> talk Hey Eevee! Want to go to the deep forest?

[Brain Council Deliberating...]

=== BRAIN COUNCIL SHOWS: ===
Amygdala wins with FEAR response!

*Eevee's ears droop* Vee... *huddles close to you nervously*

> pet
*Eevee nuzzles against you affectionately* Veeee~

> talk How about the sunny hill instead?

[Brain Council Deliberating...]

=== BRAIN COUNCIL SHOWS: ===
Prefrontal + Amygdala agree: EXCITED YES!

*Eevee's tail wags excitedly* Vee vee! *ready to go*

> go sunny hill
Traveling to Sunny Hill...

🌲 SUNNY HILL - MORNING ☀️

*Eevee arrives at the hill and stretches out in the warm sun* Veee~

> observe
Eevee seems very happy and full of energy.

*Eevee lounges contentedly in the sunshine* *peaceful purring sounds*

> stats
... (detailed stats shown)

> exit
Saving your adventure...

Eevee watches as you prepare to leave.
*Eevee nuzzles your hand one last time* Veee~

Until next time, trainer!
```

---

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
```

### No API Key Warning
**This is normal!** The app works in fallback mode. Responses are pattern-based but still authentic.

### Database Errors
The app creates `data/eevee_save.db` automatically. If you get errors, delete it and restart.

---

## What's Next?

After playing around:

1. Check out [README.md](README.md) for full documentation
2. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details
3. Look at [TASKS.md](TASKS.md) for development roadmap
4. Enable debug mode and watch the brain council!

---

## Philosophy

This isn't just a chatbot - it's a companion with:
- **Internal conflicts** between brain regions
- **Genuine emotions** that drive behavior
- **Context awareness** (location, state, relationship)
- **Memory** of your interactions (Phase 3 coming)
- **Autonomous life** when you're away (Phase 4 coming)

The brain council makes every interaction unique and meaningful!

---

**Have fun with your Eevee!**

*"Vee!"* 🦊
