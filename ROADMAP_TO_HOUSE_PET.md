# EeveeLLM: Roadmap to House Pet Vision

**Vision**: A Pokemon companion in a virtual world that feels like a real house pet - with personality, thoughts, desires, needs, and autonomous behavior in a console-based interface that runs continuously like a real pet is always there.

**Current Status**: 75% aligned with vision
**Target**: 90%+ complete house pet experience

**Key Paradigm Shift**: The app should run continuously (like a real pet is always alive), only shutting down for maintenance.

---

## Critical Gaps Analysis

### What's Working Well ✅
- **Complex Brain System** (95%) - Brain council with 5 regions, neuromodulators
- **Memory System** (90%) - 4 memory types, working memory, consolidation
- **Console UI/UX** (95%) - Modern, natural language support, clean interface
- **Personality System** (85%) - 5 traits influencing behavior
- **Autonomous Behavior** (85%) - Time simulation when away
- **Pet Interactions** (80%) - Can pet, play, feed, observe

### Critical Missing Pieces ⚠️
1. **Pokemon-Initiated Interactions** (0%) - Eevee NEVER reaches out first
2. **Always-On Mode** (0%) - App exits after each session instead of running continuously
3. **Autonomous Movement** (10%) - Doesn't move between locations
4. **Goal/Desire System** (30%) - Limited depth beyond basic needs
5. **Environmental Reactions** (50%) - Doesn't react to world changes

---

## Prioritized Implementation Plan

---

## 🎯 PHASE 7: "Proactive Eevee" (HIGHEST PRIORITY)

**Goal**: Make Eevee feel like a real pet that initiates interaction and is always present

**Impact**: +20% toward house pet feel
**Estimated Time**: 2-3 weeks
**Difficulty**: Medium

### Task 7.0: Always-On Mode (Continuous Running) ⭐⭐⭐
**Priority**: CRITICAL (Foundation for proactive behavior)
**Files**: Modify `main.py`, create `daemon/runner.py`

**What to Build**:
- [ ] **Persistent Event Loop**: App runs continuously instead of exiting after each interaction
  - Remove `exit` command (replace with maintenance mode)
  - Keep main loop running indefinitely
  - Auto-save state every 5 minutes

- [ ] **Background Activity Simulation**: Eevee lives their life even when you're not actively chatting
  - Run time simulation every 30-60 minutes (configurable)
  - Update state, generate activities, form memories
  - Don't show timeline unless user asks - just simulate in background

- [ ] **Idle State Management**: Track when user is active vs idle
  - Last interaction timestamp
  - Idle timeout (e.g., 5 minutes of no input)
  - Different behavior when idle (Eevee does their own thing)

- [ ] **Check-In System**: User can "check in" on Eevee anytime
  - Type anything to see Eevee's current state
  - Show what Eevee is doing: "*Eevee is napping in the garden*"
  - Proactive messages appear when you check in

- [ ] **Graceful Maintenance Mode**: Replace 'exit' command
  - New command: `maintenance` (requires confirmation)
  - Save all state before shutdown
  - Log shutdown reason/time

**Example Behavior**:
```
╔══════════════════════════════════════════╗
║          EeveeLLM is now running          ║
║                                          ║
║  Eevee is living their life. Check in   ║
║  anytime by typing anything!             ║
║                                          ║
║  Type 'maintenance' to shut down         ║
╚══════════════════════════════════════════╝

[15 minutes pass, you check in]

> hello

*Eevee's ears perk up from where they were napping*

Oh! You're here! *stretches and yawns*

I was just having the nicest dream... *tail wagging*

> _
```

**Technical Approach**:
```python
class AlwaysOnManager:
    def __init__(self, eevee_state, time_simulator):
        self.last_simulation = datetime.now()
        self.simulation_interval = 3600  # 1 hour
        self.last_interaction = datetime.now()
        self.auto_save_interval = 300  # 5 minutes
        self.last_save = datetime.now()

    def check_background_simulation(self):
        """Run time simulation in background"""
        now = datetime.now()
        elapsed = (now - self.last_simulation).seconds

        if elapsed >= self.simulation_interval:
            # Simulate time passage silently
            hours = elapsed / 3600
            self.time_simulator.simulate_time_passage(hours)
            self.last_simulation = now

    def check_auto_save(self):
        """Auto-save state periodically"""
        now = datetime.now()
        if (now - self.last_save).seconds >= self.auto_save_interval:
            self.eevee_state.save()
            self.last_save = now

    def is_user_idle(self) -> bool:
        """Check if user has been idle"""
        idle_seconds = (datetime.now() - self.last_interaction).seconds
        return idle_seconds > 300  # 5 minutes
```

**Main Loop Changes**:
```python
# OLD: while self.running:
# NEW: while True:  # Always running unless maintenance mode

    # Background tasks
    self.always_on.check_background_simulation()
    self.always_on.check_auto_save()

    # Check for proactive messages
    if self.always_on.is_user_idle():
        proactive_msg = self.proactive.check_attention_needs()
        if proactive_msg:
            self.ui.print_eevee_response(proactive_msg)

    # Get user input (non-blocking with timeout)
    user_input = self.get_input_with_timeout(timeout=60)

    if user_input:
        self.always_on.last_interaction = datetime.now()

        if user_input.lower() == "maintenance":
            if self.confirm_maintenance():
                break  # Only way to exit
        else:
            self.process_command(user_input)
```

---

### Task 7.1: Pokemon-Initiated Interactions System ⭐⭐⭐
**Priority**: CRITICAL
**Files**: Create `eevee/proactive.py`, modify `main.py`

**What to Build**:
- [ ] **Idle Check System**: Monitor when trainer hasn't interacted for X minutes
- [ ] **Attention Triggers**: Define when Eevee wants attention
  - Lonely after 12+ hours
  - Very hungry (>80) or tired (<20 energy)
  - Excited about discovery (found rare item)
  - Wants to show affection (random, bond-based)
  - Bored (low happiness, high energy)

- [ ] **Proactive Message Generator**: Create context-aware messages
  - "*Eevee nudges you with their nose* Vee?"
  - "*Tugs on your sleeve excitedly*"
  - "*Brings you a shiny stone they found*"
  - "*Whines softly, looking hungry*"

- [ ] **Interruption System**: Display proactive messages during idle time
  - Show when user returns to prompt
  - Don't spam (max once per 30 minutes real-time)
  - Store pending messages if multiple triggers

**Example Behavior**:
```
[You've been idle for 15 minutes]

*Eevee pads over and nudges your hand with their nose*
Vee? *looks up at you with hopeful eyes*

> _
```

**Technical Approach**:
```python
class ProactiveSystem:
    def __init__(self, eevee_state, personality):
        self.last_proactive_time = None
        self.min_interval = 1800  # 30 minutes

    def check_attention_needs(self) -> Optional[str]:
        """Check if Eevee wants attention"""
        if not self._can_interrupt():
            return None

        # Priority order
        if self._is_critical_need():
            return self._generate_urgent_message()
        if self._is_lonely():
            return self._generate_lonely_message()
        if self._wants_to_share():
            return self._generate_excited_message()
        if self._wants_affection():
            return self._generate_affection_message()

        return None
```

---

### Task 7.2: Autonomous Movement in Virtual World ⭐⭐⭐
**Priority**: CRITICAL
**Files**: Modify `world/time_simulation.py`, `world/activities.py`

**What to Build**:
- [ ] **Dynamic Location Changes**: During autonomous time, Eevee moves to activity locations
  - Store location changes in activity data
  - Update `eevee_state.location` during simulation
  - Show location changes in timeline

- [ ] **Movement Patterns**: Personality-driven exploration
  - High curiosity → explores further locations
  - Low bravery → stays in safe areas (safety >70)
  - High hunger → goes to food-rich locations
  - High energy + high playfulness → explores Wide Meadow

- [ ] **Return Home Behavior**: Tendency to return to Trainer's Home
  - When tired (<30 energy)
  - When scared (thunderstorm event)
  - End of day cycle
  - When lonely (>24 hours away)

**Example Timeline**:
```
📅 TIMELINE: Last 8 hours

October 28, 2025
─────────────────
9:00 AM  📍 Trainer's Home → Sunny Garden
         Woke up and stretched in the morning sun
         Energy +20

10:30 AM 📍 Sunny Garden → Wide Meadow
         Chased butterflies playfully
         Happiness +15, Energy -10

12:00 PM 📍 Wide Meadow → Clear Stream
         Feeling thirsty, went to drink water
         Hunger -5

2:00 PM  📍 Clear Stream → Trainer's Home
         Felt tired and returned home for a nap
         Energy +30
```

**Technical Approach**:
```python
def _select_next_location(self, current_loc, activity_type, state, personality):
    """Choose next location based on activity and context"""

    # Needs-based movement
    if state['hunger'] > 70:
        return self._find_location_with_food(current_loc)
    if state['energy'] < 30:
        return self._find_safe_location(current_loc)

    # Personality-based movement
    if activity_type == ActivityType.EXPLORATION:
        if personality['curiosity'] > 7:
            return self._find_unexplored_location(current_loc)
        else:
            return self._find_nearby_location(current_loc)

    # Default: stay in current location
    return current_loc
```

---

### Task 7.3: Basic Goal/Desire System ⭐⭐
**Priority**: HIGH
**Files**: Create `eevee/goals.py`, modify `world/activities.py`

**What to Build**:
- [ ] **Goal Types**:
  - `EXPLORE_LOCATION`: Want to visit a specific place
  - `FIND_ITEM`: Looking for specific item type
  - `BUILD_COURAGE`: Want to become braver
  - `SPEND_TIME`: Want more interaction with trainer
  - `MAKE_FRIEND`: Want to meet other Pokemon

- [ ] **Goal Formation**: Based on personality and experiences
  - High curiosity → explores new locations
  - Low bravery + repeated scary events → wants to build courage
  - Long time away → wants more trainer time
  - Found cool item → wants to find more

- [ ] **Goal Communication**: Eevee expresses desires in conversation
  - "I've been wanting to explore the Deep Forest..."
  - "Can we spend more time together?"
  - "I want to be braver like you!"

- [ ] **Goal-Driven Activities**: Use active goals to influence autonomous behavior

**Example**:
```python
class Goal:
    def __init__(self, goal_type, target, motivation, formed_at):
        self.type = goal_type
        self.target = target  # "Deep Forest", "shiny item", etc.
        self.motivation = motivation  # Why this goal
        self.formed_at = formed_at
        self.progress = 0

class GoalSystem:
    def check_goal_formation(self, state, personality, recent_memories):
        """Detect when new goals should form"""

        # High curiosity + haven't been to location
        if personality['curiosity'] > 7:
            unexplored = self._get_unexplored_locations()
            if unexplored:
                return Goal(
                    goal_type=GoalType.EXPLORE_LOCATION,
                    target=random.choice(unexplored),
                    motivation="I'm curious about what's there",
                    formed_at=datetime.now()
                )
```

---

### Task 7.4: Spontaneous Greetings ⭐
**Priority**: MEDIUM
**Files**: Modify `main.py` (start method)

**What to Build**:
- [ ] **Greeting Variations**: Based on context
  - Time away (already implemented)
  - Current mood/state
  - Active goals or discoveries
  - Random spontaneous affection

- [ ] **Eevee Greets First**: Sometimes show greeting before prompt
  - 50% chance on startup
  - 100% if been away >12 hours
  - Include current emotional state

**Example**:
```
╔══════════════════════════════════════════╗
║          Welcome to EeveeLLM! 🌟          ║
╚══════════════════════════════════════════╝

*Eevee's ears perk up as you approach*

Vee! *bounds over excitedly*

I found something cool in the meadow while you were gone!
Want to see? *tail wagging*

> _
```

---

## 🌍 PHASE 8: "Living World" (HIGH PRIORITY)

**Goal**: Make the virtual world feel dynamic and alive

**Impact**: +10% toward immersion
**Estimated Time**: 1-2 weeks
**Difficulty**: Medium

### Task 8.1: Dynamic Weather System ⭐⭐
**Priority**: HIGH
**Files**: Create `world/weather.py`, modify `world/locations.py`

**What to Build**:
- [ ] **Weather States**: Clear, Cloudy, Rain, Thunderstorm, Snow, Fog
- [ ] **Weather Cycles**: Changes every 4-8 hours
- [ ] **Seasonal Influence**: More rain in spring, snow in winter
- [ ] **Location-Specific**: Forest has more shade, meadow more sun
- [ ] **Weather Effects on Eevee**:
  - Thunderstorm → scared, seeks shelter
  - Rain → wet fur, lower happiness
  - Sunny → energetic, happy
  - Snow → curious, wants to play

**Example**:
```python
class Weather:
    def __init__(self):
        self.current = WeatherType.CLEAR
        self.last_change = datetime.now()

    def update(self):
        """Check if weather should change"""
        hours_since = (datetime.now() - self.last_change).seconds / 3600
        if hours_since >= random.uniform(4, 8):
            self.current = self._next_weather()
            self.last_change = datetime.now()
```

---

### Task 8.2: Environmental Reactions ⭐⭐
**Priority**: HIGH
**Files**: Modify `eevee/responses.py`, `world/activities.py`

**What to Build**:
- [ ] **Observation System**: Eevee notices environmental changes
  - "The sun is setting..." (time-based)
  - "It's starting to rain!" (weather change)
  - "I hear thunder..." (weather event)
  - "The flowers are blooming!" (seasonal)

- [ ] **Reactive Behaviors**: Automatic responses to environment
  - Thunder → runs to hide (moves to safe location)
  - Sunset → starts winding down (yawns)
  - Beautiful day → suggests going out
  - Strange noise → becomes alert

- [ ] **Proactive Suggestions**: Eevee suggests activities based on environment
  - "It's such a nice day! Can we go to the meadow?"
  - "It's raining... can we stay inside and play?"

---

### Task 8.3: Time of Day Effects ⭐
**Priority**: MEDIUM
**Files**: Modify `world/time_simulation.py`

**What to Build**:
- [ ] **Time Periods**: Morning (6-12), Afternoon (12-18), Evening (18-22), Night (22-6)
- [ ] **Energy Patterns**:
  - Morning: Higher energy recovery
  - Afternoon: Normal energy
  - Evening: Starting to tire
  - Night: Low energy, sleepy

- [ ] **Activity Preferences**:
  - Morning: Exploration, play
  - Afternoon: Active activities
  - Evening: Gentle play, rest
  - Night: Sleep, occasional lonely feelings

---

### Task 8.4: Relationship Memory Integration ⭐
**Priority**: MEDIUM
**Files**: Modify `memory/consolidation.py`, `brain_council/regions.py`

**What to Build**:
- [ ] **Bond Milestones**: Detect and remember significant relationship moments
  - First play session
  - First time comforted when scared
  - Trust reaches 75 (close bond)
  - First shared adventure

- [ ] **Relationship Context**: Use bond memories in decisions
  - High trust + scary situation → "Trainer will protect me"
  - Strong bond + separated → "I miss them so much"
  - New positive memory → "This reminds me of when we..."

- [ ] **Anniversary Recognition**: Remember special dates
  - Days since first meeting
  - Relationship milestones ("We've been together for a month!")

---

## 🤝 PHASE 9: "Social World" (LOWER PRIORITY)

**Goal**: Add social dimension with other Pokemon

**Impact**: +5% toward world richness
**Estimated Time**: 2-4 weeks
**Difficulty**: High

### Task 9.1: Persistent NPCs ⭐⭐
**Priority**: MEDIUM-LOW
**Files**: Create `world/npcs.py`

**What to Build**:
- [ ] **3-5 Named NPCs**: Living in specific locations
  - Friendly Pidgey (Sunny Garden)
  - Curious Pikachu (Wide Meadow)
  - Grumpy Rattata (Forest Edge)

- [ ] **NPC Personalities**: Simple traits and behaviors
- [ ] **Location-Based Encounters**: Meet NPCs in their homes
- [ ] **NPC State**: Track friendship levels with each NPC

---

### Task 9.2: Social Interactions ⭐
**Priority**: LOW
**Files**: Modify `world/activities.py`

**What to Build**:
- [ ] **Social Activities**: Play with other Pokemon
- [ ] **Friendship System**: Build bonds with NPCs
- [ ] **Social Goals**: Want to visit friends

---

### Task 9.3: Visible Personality Evolution ⭐
**Priority**: LOW
**Files**: Modify `eevee/personality.py`

**What to Build**:
- [ ] **Experience-Based Evolution**: Traits shift based on actions
- [ ] **Personality Milestones**: Eevee notices changes
- [ ] **Memory Integration**: Remember old personality

---

## Implementation Priority Summary

### MUST HAVE (Phase 7) - Next 2-3 weeks
1. ⭐⭐⭐ Always-On Mode (Foundation - enables everything else)
2. ⭐⭐⭐ Pokemon-Initiated Interactions
3. ⭐⭐⭐ Autonomous Movement
4. ⭐⭐ Basic Goal/Desire System
5. ⭐ Spontaneous Greetings

### SHOULD HAVE (Phase 8) - Following 1-2 weeks
1. ⭐⭐ Dynamic Weather System
2. ⭐⭐ Environmental Reactions
3. ⭐ Time of Day Effects
4. ⭐ Relationship Memory Integration

### NICE TO HAVE (Phase 9) - Future enhancements
1. ⭐⭐ Persistent NPCs
2. ⭐ Social Interactions
3. ⭐ Visible Personality Evolution

---

## Success Metrics

### How We'll Know We've Achieved "House Pet" Feel:

1. **Eevee initiates interaction at least once per session** ✓
2. **Eevee moves to 2+ locations during autonomous time** ✓
3. **Eevee expresses at least one desire/goal per day** ✓
4. **Eevee reacts to environmental changes without prompting** ✓
5. **Users feel emotional connection** (subjective, feedback-based) ✓

### Target Completion: 90%+ alignment with vision

Current: 75%
After Phase 7: 85%
After Phase 8: 90%
After Phase 9: 92%

---

## Technical Debt & Maintenance

### Before Starting Phase 7:
- [ ] Review and fix remaining 10 bugs in `UX_CHANGES_BUG_REVIEW.md` (5 medium, 5 low)
- [ ] Run full test suite to ensure no regressions
- [ ] Document current system state

### During Development:
- [ ] Write tests for each new system
- [ ] Update documentation as features are added
- [ ] Gather user feedback early and iterate

---

## Conclusion

EeveeLLM has an **excellent technical foundation** (75% complete). The biggest gap for the "house pet" vision is **proactive behavior** - Eevee never initiates interaction.

**Phase 7 is the most impactful** and will transform the experience from "interactive simulation" to "virtual pet companion".

The path forward is clear, and the existing architecture supports these enhancements beautifully.
