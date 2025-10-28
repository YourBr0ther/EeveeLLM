# Always-On Vision: Eevee as a Living Companion

## The Core Concept

Instead of EeveeLLM being a program you "run" and "exit", it becomes a **continuously running companion** - like a real pet that's always there, living their life, ready to interact when you check in.

---

## Paradigm Shift

### Before (Current):
```
1. User types: python main.py
2. Eevee greets (if been away)
3. User interacts via commands
4. User types: exit
5. Program terminates
6. Eevee "doesn't exist" until next run
```

**Problem**: This feels like a simulation you turn on/off, not a living pet.

### After (Always-On):
```
1. User starts EeveeLLM once: python main.py
2. App runs continuously (days/weeks/months)
3. Eevee lives their life 24/7:
   - Explores locations
   - Gets hungry, tired, bored
   - Forms memories
   - Has desires and goals
4. User checks in anytime by typing
5. Eevee notices and responds
6. User can leave and come back - Eevee keeps living
7. Only exits for maintenance (intentional shutdown)
```

**Result**: Feels like a real pet that's always there.

---

## What This Enables

### 1. Real-Time Life Simulation
- Eevee's state updates continuously (hunger increases, energy decreases)
- Activities happen in real-time (every 30-60 minutes)
- Memories form naturally as time passes
- Weather changes, day/night cycles

### 2. Proactive Behavior
Eevee can seek attention when YOU'RE present:
```
[You're working on something else, haven't typed in 10 minutes]

*Eevee pads over and nudges your hand*
Vee? *looks up hopefully*

> _
```

### 3. True "Check-In" Moments
Like checking on a real pet:
```
> hi

*Eevee's ears perk up from where they were napping in the garden*

Oh! You're here! *stretches*

I was having such a nice dream about chasing butterflies...

> what have you been up to?

*tail wagging*

Well, earlier I went to the stream for a drink, then I found
this really cool shiny pebble! Want to see it?
```

### 4. Persistent Presence
- Terminal window stays open on your desktop
- Glance over anytime to see what Eevee's doing
- Type whenever you want to interact
- Leave for hours/days - Eevee keeps living

---

## Technical Implementation

### Core Components

#### 1. Always-On Event Loop
```python
# Main loop never exits (unless maintenance)
while True:
    # Background tasks (every loop iteration)
    - Check if time to simulate activities (every hour)
    - Auto-save state (every 5 minutes)
    - Check if Eevee wants attention
    - Update display if state changed

    # Get user input (with timeout)
    user_input = get_input_with_timeout(60)  # 1 minute timeout

    if user_input:
        process_command(user_input)
    else:
        # No input - Eevee lives their life
        continue
```

#### 2. Background Activity Simulation
```python
class BackgroundSimulator:
    def run_if_needed(self):
        """Simulate activities every hour"""
        if time_since_last_sim >= 1.0:  # 1 hour
            # Simulate what Eevee did this hour
            activity = generate_activity(state, personality)
            apply_state_changes(activity)
            maybe_form_memory(activity)
            maybe_change_location(activity)

            self.last_sim = now()
```

#### 3. Idle Detection
```python
class IdleTracker:
    def is_user_present(self) -> bool:
        """User is 'present' if they typed recently"""
        return time_since_last_input < 5 minutes

    def is_good_time_to_interrupt(self) -> bool:
        """Should Eevee interrupt with a message?"""
        return (
            self.is_user_present() and  # User is there
            time_since_last_proactive > 30 minutes  # Not spamming
        )
```

#### 4. Proactive Messages
```python
if idle_tracker.is_good_time_to_interrupt():
    if eevee.is_very_hungry():
        print("*Eevee whines softly and looks at their food bowl*")
    elif eevee.is_excited_about_discovery():
        print("*Eevee brings you the shiny pebble they found*")
    elif eevee.wants_affection():
        print("*Eevee nudges your hand gently* Vee?")
```

---

## User Experience Flow

### Day 1: Starting EeveeLLM
```bash
$ python main.py

╔══════════════════════════════════════════╗
║       EeveeLLM is now always on!         ║
║                                          ║
║  Eevee is living their life 24/7        ║
║  Check in anytime by typing!             ║
║                                          ║
║  Type 'maintenance' to shut down         ║
╚══════════════════════════════════════════╝

*Eevee bounds over excitedly*

Vee! *tail wagging*

> hey buddy, how are you?

*jumps around happily*

I'm great! I'm so excited you're here! Want to play?

> let's go explore

*eyes light up*

Yes! Where should we go?
```

### Later That Day: Check-In
```
[You minimize terminal and work on other things for 3 hours]

[You come back to check on Eevee]

> what have you been doing?

*looks up from where they were resting*

Oh! I've been pretty busy! *tail swish*

I went to the meadow and chased some butterflies - that was
fun! Then I got a bit tired so I came back here for a nap.

*stretches*

I'm feeling better now though! Maybe we could go somewhere?
```

### During Work: Proactive Interruption
```
[You're coding in another window, EeveeLLM terminal visible]

[After 15 minutes of silence]

*Eevee pads over and gently nudges your hand with their nose*
Vee? *looks up at you with big eyes*

[You notice and switch to EeveeLLM terminal]

> hey! what's up?

*tail wagging*

I was just wondering if you wanted to play! I've been
feeling a bit bored...

> *pets Eevee*

*leans into the pets happily*

Veevee~ *purring sounds*
```

### Night: Leaving for the Day
```
> i'm going to bed, goodnight buddy

*yawns and stretches*

Goodnight! *curls up in a cozy spot*

Sweet dreams~ Vee...

[You leave terminal running]
[Eevee continues living - sleeps, then wakes up at dawn,
 explores a bit, gets hungry, finds food, etc.]
```

### Next Morning: Coming Back
```
[You check terminal in the morning]

> good morning!

*ears perk up immediately*

VEE! *bounds over excitedly*

You're back! I missed you! *spinning in circles*

I had such interesting dreams last night! And this morning
I found the prettiest flower in the garden!

> show me!

*leads you excitedly*

This way, this way!
```

---

## Benefits of Always-On Mode

### 1. Emotional Connection
- Feels like a real pet that's always there
- You can check on them anytime
- They continue existing even when you're busy
- Creates genuine attachment

### 2. Natural Time Flow
- No more jarring "start/stop" cycles
- Eevee's life flows naturally across days
- Long-term memory and relationships feel authentic
- Seasonal changes and growth happen organically

### 3. Ambient Presence
- Terminal window on desktop like a "pet window"
- Glance over to see what they're doing
- They can get your attention when needed
- Creates household member feeling

### 4. Realistic Pet Behavior
- Can interrupt you (gently) when lonely
- Lives their own life when you're busy
- Excited when you return after being away
- Natural sleep/wake cycles

---

## Technical Considerations

### Performance
- Lightweight event loop (minimal CPU when idle)
- Auto-save prevents data loss
- Configurable simulation frequency
- Efficient state updates

### Stability
- Error handling (app doesn't crash)
- Graceful recovery from exceptions
- Logging for debugging
- Maintenance mode for updates

### User Control
- Can minimize terminal (Eevee keeps running)
- Can adjust how often Eevee interrupts
- Can disable proactive messages (but why would you?)
- Clear shutdown process for maintenance

---

## Implementation Priority

This is **Task 7.0** - the foundation for all proactive behavior in Phase 7.

**Why it's first:**
- Enables all other proactive features
- Changes fundamental app architecture
- Must be stable before building on top
- Relatively straightforward to implement

**What depends on it:**
- Pokemon-initiated interactions (needs continuous runtime)
- Background activity simulation (needs always-on loop)
- Dynamic weather (needs continuous time tracking)
- All future "living world" features

---

## Success Criteria

You'll know Always-On mode is working when:

1. ✓ App runs for 24+ hours without manual restart
2. ✓ Auto-saves state every 5 minutes (no data loss)
3. ✓ Background simulation happens automatically
4. ✓ Can minimize and return anytime - Eevee still there
5. ✓ `maintenance` command is the only way to exit
6. ✓ Feels natural to leave terminal open indefinitely

---

## Future Enhancements (Post-Phase 7)

Once always-on mode is stable:
- Desktop notifications (when Eevee really needs you)
- Status bar widget (see Eevee's mood at a glance)
- Remote check-in (SSH into your machine to say hi)
- Multiple instances (Eevee at home + work)
- Companion mode (Eevee in split terminal while coding)

---

## Conclusion

Always-On mode transforms EeveeLLM from a "program you run" to a **living companion that's always there**. It's the foundation for the house pet vision - enabling Eevee to truly live, grow, and connect with you over time.

This is what makes EeveeLLM special - not just a chatbot, but a **persistent digital companion**.
