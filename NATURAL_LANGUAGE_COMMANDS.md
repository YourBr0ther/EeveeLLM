# Natural Language Commands - User Guide

**You can now interact with Eevee using natural language!** No need to remember exact command syntax - just talk naturally.

---

## Overview

EeveeLLM now supports natural language command detection. Instead of typing exact commands like `stats` or `inventory`, you can use natural phrasings like "How are you feeling?" or "Show me your stuff".

**The system automatically detects your intent** and executes the appropriate command.

---

## Supported Commands

### 1. **Stats** - Check Eevee's condition

**Exact command:** `stats`

**Natural language alternatives:**
- "What are your stats?"
- "How are you feeling?"
- "Show me your health"
- "Are you okay?"
- "What's your energy level?"
- "Check your status"
- "Display your condition"
- "Are you hungry?"
- "Are you tired?"

**Example:**
```
You: How are you feeling?
→ Executes: stats command

[Shows Eevee's health, hunger, energy, happiness]
```

---

### 2. **Inventory** - View items

**Exact command:** `inventory`

**Natural language alternatives:**
- "Show me your inventory"
- "What do you have?"
- "What items are you carrying?"
- "Let me see your stuff"
- "Display your items"
- "What's in your bag?"

**Example:**
```
You: What do you have?
→ Executes: inventory command

[Shows all items Eevee is carrying]
```

---

### 3. **Pet** - Pet Eevee

**Exact command:** `pet`

**Natural language alternatives:**
- "I want to pet you"
- "Can I pet you?"
- "Let me pet Eevee"
- "Give you some pets"
- "Head pat"
- "I'll pet you"

**Example:**
```
You: Can I pet you?
→ Executes: pet command

Eevee: *Vee!* *tail wagging happily*
```

---

### 4. **Play** - Play with Eevee

**Exact command:** `play`

**Natural language alternatives:**
- "Let's play!"
- "Do you want to play?"
- "Want to play?"
- "Feel like playing?"
- "Playtime!"
- "Wanna play?"

**Example:**
```
You: Want to play?
→ Executes: play command

Eevee: *Vee vee!* *excited jumping*
```

---

### 5. **Observe** - See what Eevee is doing

**Exact command:** `observe`

**Natural language alternatives:**
- "What are you doing?"
- "What's happening?"
- "What are you up to?"
- "Let me see what you're doing"

**Example:**
```
You: What are you up to?
→ Executes: observe command

[Shows Eevee's current activity]
```

---

### 6. **World** - Check current location

**Exact command:** `world`

**Natural language alternatives:**
- "Where are we?"
- "Where am I?"
- "What's this place?"
- "Show me the area"
- "Describe this location"
- "Look around"

**Example:**
```
You: Where are we?
→ Executes: world command

[Shows current location and surroundings]
```

---

### 7. **Go/Travel** - Move to a new location

**Exact command:** `go [location]`

**Natural language alternatives:**
- "Let's go to the meadow"
- "Take me to the forest"
- "Can we go to the park?"
- "Travel to the beach"
- "Go to cave"
- "Head to trainer home"

**Example:**
```
You: Let's go to the meadow
→ Executes: go meadow

[Travels to meadow location]
```

---

### 8. **Give** - Give Eevee an item

**Exact command:** `give [item]`

**Natural language alternatives:**
- "Give you an Oran Berry"
- "Here's a berry"
- "Take this Potion"
- "I'll give you a Pecha Berry"
- "Have some berries"

**Example:**
```
You: Here's an Oran Berry
→ Executes: give oran berry

Eevee: *Vee!* *happily accepts berry*
```

---

### 9. **Use** - Use an item from inventory

**Exact command:** `use [item]`

**Natural language alternatives:**
- "Use the Oran Berry"
- "Let's use a Potion"
- "Can you use this berry?"
- "You should use that medicine"

**Example:**
```
You: Use the Oran Berry
→ Executes: use oran berry

[Eevee uses the Oran Berry, restores health]
```

---

### 10. **Drop** - Remove an item from inventory

**Exact command:** `drop [item]`

**Natural language alternatives:**
- "Drop the old stick"
- "Remove that item"
- "Get rid of the trash"
- "Throw away the junk"
- "I don't want the rock"

**Example:**
```
You: Drop the stick
→ Executes: drop stick

[Removes stick from inventory]
```

---

### 11. **Remember** - Browse Eevee's memories

**Exact command:** `remember [query]`

**Natural language alternatives:**
- "Do you remember the park?"
- "What do you remember about yesterday?"
- "Can you recall what happened?"
- "Show me your memories"
- "Remember the beach"

**Example:**
```
You: Do you remember the park?
→ Executes: remember park

[Shows memories related to the park]
```

---

### 12. **Timeline** - View recent activities

**Exact command:** `timeline`

**Natural language alternatives:**
- "What did you do while I was gone?"
- "Show me the timeline"
- "What have you been up to?"
- "What happened recently?"
- "View recent activities"

**Example:**
```
You: What did you do while I was gone?
→ Executes: timeline command

[Shows summary of autonomous activities]
```

---

### 13. **Help** - Show available commands

**Exact command:** `help`

**Natural language alternatives:**
- "Help"
- "What can I do?"
- "Show me the commands"
- "How do I interact with you?"
- "List available options"

**Example:**
```
You: What can I do?
→ Executes: help command

[Shows command list]
```

---

## How It Works

### Intent Detection

The system uses **pattern matching** to detect your intent:

1. **You type natural language:** "How are you feeling?"
2. **Parser matches pattern:** Detects "how are you feeling" → stats command
3. **Command executes:** Runs the stats command
4. **Eevee responds:** Shows stats and responds naturally

### Fallback to Conversation

If **no command pattern matches**, your input is treated as normal conversation:

```
You: Hello Eevee!
→ No command detected
→ Treated as: talk "Hello Eevee!"

Eevee: *Vee!* *tail wagging* *excited to see you*
```

This means you can **mix commands and conversation seamlessly!**

---

## Examples in Action

### Example 1: Morning Routine

```
You: How are you feeling?
→ stats command
[Shows Eevee is hungry and has low energy]

You: Here's an Oran Berry
→ give oran berry
Eevee: *Vee!* *happily munches berry*

You: Want to play?
→ play command
Eevee: *Vee vee!* *playful bouncing*
```

### Example 2: Exploring Together

```
You: Where are we?
→ world command
[Shows: Trainer's Home]

You: Let's go to the meadow
→ go meadow
[Travels to meadow]

You: Look around
→ world command
[Shows meadow description with berry bushes]
```

### Example 3: Checking In

```
You: What have you been up to?
→ timeline command
[Shows activities while you were gone]

You: Do you remember when we went to the beach?
→ remember beach
[Shows beach-related memories]

You: You're such a good companion
→ talk (no command)
Eevee: *Vee!* *happy tail wagging*
```

---

## Command Priority

When multiple patterns might match, the parser uses **order and specificity**:

1. **More specific patterns** match first
2. **Exact matches** take priority over partial matches
3. **Commands** are processed before treating input as conversation

**Example:**
```
"What happened recently?"
→ Matches timeline (specific)
NOT remember (less specific)
```

---

## Exact Commands Still Work!

You can **still use exact command syntax** if you prefer:

```
stats          ✅ Works
How are you?   ✅ Works (detected as stats)
```

**Both work perfectly!** Use whichever feels more natural to you.

---

## Debugging Natural Language

If you enable verbose logging, you can see intent detection:

```
export VERBOSE_LOGGING=true
```

**Console output:**
```
Natural language detected: 'How are you feeling?' → stats
```

This helps you understand what the system is detecting!

---

## Tips for Best Results

### ✅ Do:
- **Be natural:** "Want to play?" instead of forcing command syntax
- **Use common phrasings:** The system recognizes many variations
- **Mix commands and talk:** Seamlessly switch between the two
- **Try different phrasings:** Multiple ways to express the same intent

### ❌ Don't:
- **Worry about exact syntax:** Natural language is flexible
- **Overthink it:** Just talk to Eevee naturally
- **Force command keywords:** "I want to pet you" works just as well as "pet"

---

## Adding Your Own Patterns

Want to extend the natural language parser? Edit `nlp/intent_parser.py`:

```python
# Add your own pattern
custom_patterns = [
    (r"check on (you|eevee)", "stats", None, 1.0),
    (r"let's explore", "world", None, 1.0),
]
```

Pattern format:
- **Regex pattern:** What to match in user input
- **Command:** What command to execute
- **Extraction function:** Optional function to extract arguments
- **Confidence:** Score from 0.0 to 1.0

---

## Summary

**Natural Language Features:**
- ✅ 13 commands supported
- ✅ 80+ natural language phrasings
- ✅ Automatic intent detection
- ✅ Argument extraction (for go, give, use, drop, remember)
- ✅ Fallback to conversation
- ✅ Mix commands and talk seamlessly
- ✅ Exact commands still work
- ✅ 100% test coverage

**Just talk to Eevee naturally - the system handles the rest!** 🎉
