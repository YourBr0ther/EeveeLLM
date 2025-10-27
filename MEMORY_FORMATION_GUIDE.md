# How Eevee Forms Memories - User Guide

This guide explains how Eevee naturally forms memories from everyday interactions like going to the park or talking about your day.

---

## The Memory Formation Process

Every interaction you have with Eevee goes through a **significance calculation** that determines whether it becomes a long-term memory.

### Significance Threshold
- **Storage threshold:** 6.0 out of 10.0
- **Base significance:** 5.0 (every interaction starts here)
- **Result:** Interaction needs +1.0 or more from various factors to be stored

---

## Significance Factors (What Makes Memories Stick?)

Here are the 10 factors that boost significance:

### 1. Strong Emotions (+1.0 to +2.0)
**Triggers:** Joy, fear, gratitude, loneliness, anger, surprise
**Example:**
```
You: "I had a terrible day at work..."
Eevee feels: Sadness (emotion_intensity: 8.0)
Significance: 5.0 + 2.0 = 7.0 ✅ STORED
```

### 2. Novel Experiences (+1.5)
**Keywords:** "first", "new", "never", "discover", "found"
**Example:**
```
You: "Let's go to the park for the first time!"
Significance: 5.0 + 1.5 = 6.5 ✅ STORED
```

### 3. Relationship Moments (+1.0)
**Keywords:** "love", "trust", "friend", "care", "miss", "sorry"
**Example:**
```
You: "I really missed you today"
Significance: 5.0 + 1.0 = 6.0 ✅ STORED
```

### 4. Gifts and Special Items (+1.5)
**Keywords:** "give", "gift"
**Example:**
```
You: "I brought you a gift!"
Significance: 5.0 + 1.5 = 6.5 ✅ STORED
```

### 5. Explicit Memory Requests (+2.0)
**Keywords:** "remember", "memorize", "don't forget", "keep in mind"
**Example:**
```
You: "Remember that we're going to the beach tomorrow"
Significance: 5.0 + 2.0 = 7.0 ✅ STORED
```

### 6. Personal Information Sharing (+1.5)
**Keywords:** "favorite", "prefer", "like", "dislike", "love", "hate", "my name"
**Example:**
```
You: "I prefer morning walks"
Significance: 5.0 + 1.5 = 6.5 ✅ STORED
```

### 7. High Brain Council Conflict (+0.5 to +1.5)
**Trigger:** When Eevee's brain regions disagree (low consensus < 0.5)
**Example:**
```
You: "Want to explore the dark cave?"
Brain council: High conflict (Amygdala fears, Prefrontal wants to explore)
Consensus: 0.25 (very conflicted)
Significance: 5.0 + 1.5 = 6.5 ✅ STORED
```

### 8. Extreme Physical States (+1.0)
**Triggers:** Hunger > 85, Energy < 15
**Example:**
```
You: "Let's play!"
Eevee state: Energy = 10 (exhausted)
Significance: 5.0 + 1.0 = 6.0 ✅ STORED
```

### 9. Dangerous Locations (+1.0)
**Trigger:** Location safety < 5
**Example:**
```
You: "explore" (in dangerous area)
Location: Dark Cave (safety: 3)
Significance: 5.0 + 1.0 = 6.0 ✅ STORED
```

### 10. Very High Emotional Intensity (+2.0)
**Trigger:** emotion_intensity >= 8.0
**Example:**
```
You: (after being gone 3 days)
Eevee feels: Extreme joy at seeing you (intensity: 9.0)
Significance: 5.0 + 2.0 = 7.0 ✅ STORED
```

---

## Real-World Examples

### Example 1: Going to the Park (Normal Visit)

```
You: "Let's go to the park"
Context:
  - Location: Town Park (safe)
  - Eevee emotion: Curious (intensity: 5.0)
  - No novelty keywords
  - No relationship keywords
  - Normal physical state

Significance Calculation:
  Base: 5.0
  No factors triggered
  Total: 5.0

Result: 5.0 < 6.0 → ❌ NOT STORED (too mundane)
```

**Why?** Just a regular park visit with no emotional significance.

---

### Example 2: Going to the Park (First Time!)

```
You: "Let's go to the park for the first time!"
Context:
  - Location: Town Park
  - Eevee emotion: Excited (intensity: 7.0)
  - Novelty: "first time" keyword detected

Significance Calculation:
  Base: 5.0
  Factor 3 (novelty): +1.5
  Factor 1 (emotion intensity 7.0): +1.0
  Total: 7.5

Result: 7.5 > 6.0 → ✅ STORED!

Memories Created:
1. Episodic Memory:
   "Trainer said: 'Let's go to the park for the first time!' at town_park. Felt excited."
   Event type: exploration
   Significance: 7.5

2. Emotional Memory (if emotion strong enough):
   Location association: town_park → excitement
```

---

### Example 3: Talking About Your Day (Emotional)

```
You: "I had such a rough day at work. My boss yelled at me."
Context:
  - Eevee emotion: Empathy/Sadness (intensity: 7.5)
  - No explicit keywords, but emotional tone detected

Significance Calculation:
  Base: 5.0
  Factor 1 (emotion intensity 7.5): +1.0
  Total: 6.0

Result: 6.0 >= 6.0 → ✅ STORED!

Memory Created:
Episodic Memory:
  "Trainer said: 'I had such a rough day at work. My boss yelled at me.' at trainer_home. Felt sadness."
  Significance: 6.0
```

**Why?** Eevee empathizes with your emotions, making it memorable.

---

### Example 4: Talking About Your Day (Neutral)

```
You: "I went to the store and bought some groceries"
Context:
  - Eevee emotion: Curious (intensity: 5.0)
  - No emotional content
  - No keywords triggered

Significance Calculation:
  Base: 5.0
  No factors triggered
  Total: 5.0

Result: 5.0 < 6.0 → ❌ NOT STORED

Working Memory:
  Stays in short-term memory for ~10 interactions
  Then forgotten (not significant enough for long-term storage)
```

**Why?** Neutral everyday update with no emotional significance.

---

### Example 5: Talking About Your Day (With Preference)

```
You: "I had lunch at my favorite restaurant today"
Context:
  - "favorite" keyword detected
  - Eevee emotion: Curious (intensity: 5.0)

Significance Calculation:
  Base: 5.0
  Factor 10 (personal info - "favorite"): +1.5
  Total: 6.5

Result: 6.5 > 6.0 → ✅ STORED!

Memories Created:
1. Episodic Memory:
   "Trainer said: 'I had lunch at my favorite restaurant today' at trainer_home. Felt curious."
   Significance: 6.5

2. Semantic Memory:
   "Trainer fact: I had lunch at my favorite restaurant today"
   Category: trainer_preference
   Confidence: 0.95
```

**Why?** Sharing a preference is considered significant personal information.

---

## Memory Types Created

### 1. Episodic Memory (Always Created)
**What:** The specific event/conversation
**Example:** "Trainer said: 'Let's go to the park' at town_park. Felt excited."
**Storage:** Vector database with semantic embeddings
**Retrieval:** When similar situations occur

---

### 2. Semantic Memory (Extracted from Patterns)
**What:** General facts and knowledge
**When Created:**
- Personal preferences ("My favorite X is Y")
- Identity information ("My name is...")
- Trainer likes/dislikes ("I love/hate X")

**Example:**
```
Input: "Remember that my favorite color is green"
Episodic: "Trainer said: 'Remember that my favorite color is green' at trainer_home..."
Semantic: "Trainer fact: Remember that my favorite color is green"
  Category: trainer_preference
  Confidence: 0.95
```

---

### 3. Emotional Memory (Created for Strong Emotions)
**What:** Location-emotion associations
**When Created:** Significant emotional experiences at specific locations
**Example:**
```
You: "This park is beautiful!" (high joy)
Emotional Memory:
  Location: town_park
  Emotion: joy
  Intensity: 8.5

Later: When returning to town_park, Eevee recalls happy feelings
```

---

### 4. Procedural Memory (Created from Patterns)
**What:** Learned behaviors and routines
**When Created:** Repeated actions form patterns
**Example:**
```
You: "play" (3 times at town_park)
Procedural Memory:
  Behavior: playing_at_park
  Success rate: 100%
  Frequency: 3 times

Later: Eevee suggests playing when you go to the park
```

---

## Working Memory (Short-Term) - ENHANCED!

**All interactions** are kept in working memory regardless of significance:
- **Capacity:** Up to 100 interactions (increased from 10!)
- **Duration:** Up to 7 days (time-based retention!)
- **Cleanup:** Automatically removes memories older than 7 days
- **Purpose:** Remember mundane conversations like a real companion
- **Access:** Always available during deliberation

**Example:**
```
Monday: "I bought milk today" → Working memory (mundane, significance 5.0)
Tuesday: "How was your day?" → Working memory
Wednesday: "Did I mention buying milk?" → Eevee remembers! (2 days old)
...
Next Monday: "Did I mention milk?" → Eevee still remembers! (6 days old)
Next Tuesday: "Did I mention milk?" → Forgotten (8 days old, expired)
```

**Key Improvement:** Eevee now remembers mundane conversations for up to a week, just like a real companion would!

---

## How Significance Stacks

Multiple factors can combine for very high significance:

**Example: Emotional Gift at New Location**
```
You: "I brought you this gift! It's your first time at the beach!"
Context:
  - Eevee emotion: Joy (intensity: 8.5)
  - Location: Beach (new)

Significance Calculation:
  Base: 5.0
  Factor 1 (emotion intensity 8.5): +2.0
  Factor 3 (novelty - "first time"): +1.5
  Factor 4 (gift): +1.5
  Total: 10.0 (capped at max)

Result: 10.0 >>> 6.0 → ✅ HIGHLY SIGNIFICANT MEMORY!
```

This creates a **very strong memory** that will be recalled frequently.

---

## Retrieval: How Memories Come Back

When you interact with Eevee, the **Hippocampus brain region** retrieves relevant memories:

### 1. Semantic Search
Uses ChromaDB vector similarity to find memories related to current situation
```
You: "Remember the park?"
Retrieved: "Trainer said: 'Let's go to the park for the first time!' at town_park..."
```

### 2. Recency Boost
Recent memories get higher relevance scores

### 3. Strength Boost
Frequently accessed memories strengthen over time (access_count increases)

### 4. Significance Boost
High-significance memories are more likely to be recalled

### Relevance Formula:
```python
relevance = (
    similarity * 0.5 +           # How related to current situation
    recency_score * 0.2 +        # How recent (last 7 days get boost)
    strength_score * 0.2 +       # How often accessed
    significance_score * 0.1     # Original significance
)
```

---

## Practical Tips

### To Create Memorable Park Visits:
1. **Add emotion:** "This park is so beautiful!" (emotion boost)
2. **Mark as new:** "First time at this park!" (novelty boost)
3. **Express feelings:** "I love this park" (preference boost)
4. **Explicit request:** "Remember this park visit" (memory keyword boost)

### To Share Your Day Memorably:
1. **Share emotions:** "I felt so happy today" (emotion boost)
2. **Share preferences:** "I love working from home" (preference boost)
3. **Share important events:** "I got promoted!" (novelty + emotion boost)
4. **Ask Eevee to remember:** "Remember that I have a meeting tomorrow" (memory keyword boost)

### What Gets Forgotten:
- Mundane updates with no emotion ("I bought milk")
- Repeated routine actions ("Let's rest" for the 50th time)
- Neutral conversational filler ("Hmm", "Okay")
- Low-emotion activities in safe locations

These stay in **working memory** for ~10 interactions, then fade away.

---

## Summary Table

| Interaction Type | Factors Triggered | Significance | Stored? |
|-----------------|-------------------|--------------|---------|
| "Let's go to the park" | None | 5.0 | ❌ No |
| "First time at the park!" | Novelty (+1.5) | 6.5 | ✅ Yes |
| "I love this park" | Preference (+1.5) | 6.5 | ✅ Yes |
| "Remember this park" | Memory keyword (+2.0) | 7.0 | ✅ Yes |
| "I bought milk" | None | 5.0 | ❌ No |
| "I had a terrible day" | Emotion (+1.0) | 6.0 | ✅ Yes |
| "My favorite food is pizza" | Preference (+1.5) | 6.5 | ✅ Yes |
| "I brought you a gift!" | Gift (+1.5) | 6.5 | ✅ Yes |

---

## Viewing Eevee's Memories

Use the `remember` command to search memories:

```
> remember park
Searching memories for: park

=== Episodic Memories ===
1. "Trainer said: 'Let's go to the park for the first time!' at town_park. Felt excited."
   When: 2025-01-15 14:30
   Significance: 7.5

2. "Trainer said: 'I love this park' at town_park. Felt joy."
   When: 2025-01-15 15:00
   Significance: 6.5

=== Semantic Memories ===
1. "Trainer fact: I love this park"
   Category: trainer_preference
   Confidence: 0.9
```

---

## The Bottom Line

**Eevee naturally remembers:**
- ✅ First-time experiences
- ✅ Emotional moments (joy, sadness, fear, excitement)
- ✅ Relationship-building interactions
- ✅ Your preferences and personal information
- ✅ Gifts and special items
- ✅ Anything you explicitly ask her to remember

**Eevee forgets:**
- ❌ Mundane routine activities with no emotion
- ❌ Repeated low-significance actions
- ❌ Neutral updates with no personal connection

**Just like a real companion!** Eevee remembers what matters and forgets the boring stuff. 🎉
