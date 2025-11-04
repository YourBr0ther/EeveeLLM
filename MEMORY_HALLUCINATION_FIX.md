# Memory Hallucination Fix

**Date**: 2025-10-28
**Issue**: Eevee claiming to remember things that were never said (e.g., "green")
**Status**: ✅ FIXED

---

## The Problem

User reported strange interaction:
```
User: "This meadow is so pretty, isn't it?"
Eevee: "I remember Trainer saying something about green here before!"
```

**Issue**: User never mentioned "green" in current conversation. This is a false memory / hallucination.

---

## Investigation Results

### Test Script Output

Created `test_memory_retrieval_fix.py` to debug the issue. Key findings:

**1. Retrieved Memories for Query**:
```
Query: "This meadow is so pretty, isn't it?"
Retrieved Memories:
1. "Trainer said: 'This meadow is so pretty, isn't it?' at meadow. Felt curious."
2. "Trainer said: 'clear' at meadow. Felt curious."
3. "Trainer said: 'That is great! What are you going to get into today?' at meadow."
4. "Trainer said: 'what is my favorite color?' at meadow."
5. "Trainer said: 'you are a curious little creature, aren't you?...' at meadow."
```

**2. Memories Containing "Green"**:
```
Found 20 memories about "green" (from prior conversations):
- "Trainer fact: will you remember my favorite color is green?"
- "Trainer fact: Green is my favorite color. My name is Chris"
- "Trainer said: 'Green is my favorite color. My name is Chris' at meadow."
```

**3. Critical Discovery**:
- ✅ NO "green" memories were retrieved for the meadow query
- ✅ "Green" memories exist but have LOW semantic similarity to "meadow is pretty"
- ❌ LLM is INVENTING memories based on overly permissive prompt

---

## Root Cause

**Location**: [llm/prompts.py:168-169](llm/prompts.py#L168-L169)

### Original Prompt (Problematic):
```python
- If you have relevant memories, use them to inform your response
```

**Problem**: This instruction is too vague. The LLM interprets "you have relevant memories" as "you *could* have memories" and invents plausible-sounding memories to make responses feel more natural.

This is called **confabulation** - when an AI fills memory gaps with plausible but false information.

---

## The Fix

### Changes Made:

**1. Explicit Memory Presence Indicator**:
```python
if has_memories:
    memory_context = "\nRelevant memories:\n"
    for i, (content, metadata, relevance) in enumerate(retrieved_memories[:3], 1):
        memory_context += f"- {content}\n"
else:
    memory_context = "\n(No relevant past memories for this situation)\n"
```

**2. Strict Memory Reference Instructions**:
```python
- IMPORTANT: Only reference memories if they appear in "Relevant memories" above
- Do NOT invent or assume memories that are not explicitly listed
```

### Why This Works:

1. **Clear Signal**: Explicitly shows when no memories exist
2. **Strict Constraint**: Direct instruction not to invent memories
3. **Grounding**: LLM can only reference what's literally written in the prompt

---

## Testing

### Before Fix:
```
User: "This meadow is so pretty, isn't it?"
Eevee: "I remember Trainer saying something about green here before!"
         ^ FALSE MEMORY - never said
```

### After Fix:
```
User: "This meadow is so pretty, isn't it?"
Eevee: *Eevee's ears perk up and tail swishes gently* Veevee!
       *looks around the meadow, eyes sparkling with wonder*
       ^ Natural response WITHOUT false memories
```

---

## Impact

### What's Fixed:
- ✅ Eevee won't claim to remember things that weren't said
- ✅ Memory references now grounded in actual retrieved memories
- ✅ More realistic memory behavior (doesn't always have a memory)
- ✅ Trustworthy companion (doesn't make up past conversations)

### What's Unchanged:
- ✅ Genuine memories still retrieved and used when relevant
- ✅ Memory retrieval system unchanged
- ✅ Semantic search still finds related memories
- ✅ Conversation context still intact

---

## Related Files

- **Fixed**: [llm/prompts.py:138-177](llm/prompts.py#L138-L177)
- **Test Script**: [test_memory_retrieval_fix.py](test_memory_retrieval_fix.py)
- **Memory Retrieval**: [memory/retrieval.py](memory/retrieval.py)
- **Analysis**: [CONVERSATION_CONTEXT_ANALYSIS.md](CONVERSATION_CONTEXT_ANALYSIS.md)

---

## Technical Details

### Why Confabulation Happened:

1. **LLM Training**: Language models are trained to generate plausible continuations
2. **Memory Prompting**: Prompt mentioned "memories" even when none retrieved
3. **Semantic Association**: "Meadow" + "pretty" + "color" → LLM fills in "green"
4. **Natural Language**: Saying "I remember..." sounds more natural than "Hmm..."

### Prevention Strategy:

- **Explicit grounding**: Only reference what's literally in prompt
- **Negative case handling**: Show when memories DON'T exist
- **Clear instructions**: Tell LLM not to invent information
- **Validation**: Could add post-generation check (future enhancement)

---

## Future Improvements

**Optional enhancements** (not needed now, but could help):

1. **Post-Generation Validation**:
   - Check if Eevee's response mentions memories
   - Verify those memories were actually retrieved
   - Flag or regenerate if mismatch

2. **Memory Citation Format**:
   - Require Eevee to cite memory numbers: "I remember (memory #2)..."
   - Easier to verify correctness

3. **Confidence Scoring**:
   - Track when Eevee references memories
   - Score accuracy over time
   - Adjust prompting based on accuracy

---

## Conclusion

**Root Cause**: LLM confabulation due to permissive prompt
**Solution**: Explicit memory grounding + strict instructions
**Result**: Trustworthy memory references, no more false memories

This fix maintains the natural conversational feel while ensuring memory accuracy - critical for a companion you trust!
