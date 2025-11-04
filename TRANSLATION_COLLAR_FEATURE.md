# Translation Collar Feature 📿✨

## Overview
Added a mystical Translation Collar that allows Eevee to speak in broken English while maintaining her adorable Pokemon personality!

## Features Implemented

### 1. Translation Collar Item
- **Item ID**: `translation_collar`
- **Type**: Treasure (Very Rare)
- **Non-consumable**: Keeps the collar permanently once found
- **Effect**: Enables human speech mode + happiness boost
- **Emoji**: 📿✨

### 2. Speech Mode System
- **Database Field**: `has_translation_collar` (boolean)
- **Persistent State**: Collar status saves across sessions
- **Auto-Migration**: Existing databases automatically get the new field

### 3. Broken English Patterns
When collar is equipped, Eevee speaks with:
- Simple grammar: "Me happy!", "You good friend!"
- Basic vocabulary: "want food", "sleepy", "friend"
- Simple questions: "You okay?", "Where go?", "Play with me?"
- Emotional expressions: "Me so happy!", "Love you!"
- Occasional "Vee!" sounds when excited

### 4. Commands Added

#### Equip Collar
```
equip collar
wear collar
use translation_collar  (auto-equips)
```

#### Unequip Collar
```
unequip
```

#### Give Collar (if you have one)
```
give translation_collar
```

### 5. UI Enhancements
- **Stats Display**: Shows collar status with 🟢/🔴 indicators
- **Help System**: Added collar commands to items help
- **Status Messages**: Clear feedback when equipping/unequipping

### 6. Prompt System Integration
- **Dynamic Instructions**: Prompts automatically change based on collar status
- **Both Modes**: Works with simple responses and brain council responses
- **Context Awareness**: LLM knows current speech mode

## How to Test

1. **Get the Collar**:
   ```
   give translation_collar
   ```

2. **Equip It**:
   ```
   equip collar
   ```
   OR
   ```
   use translation_collar
   ```

3. **Talk to Eevee**:
   ```
   Hello Eevee!
   ```
   Expected: *"Me so happy! You here!"* (broken English)

4. **Check Status**:
   ```
   stats
   ```
   Shows: 📿 TRANSLATION COLLAR 🟢 EQUIPPED

5. **Remove Collar**:
   ```
   unequip
   ```

6. **Talk Again**:
   ```
   Hello again!
   ```
   Expected: *"Vee! Veevee!"* (Pokemon sounds)

## Example Transformations

**Before (Pokemon mode):**
> *Eevee perks up excitedly* Vee! Veevee! *bounces happily*

**After (Collar mode):**
> *Eevee perks up excitedly* "Me happy! You here!" *bounces happily*

## Technical Implementation

### Files Modified
- `world/items.py` - Added Translation Collar item
- `eevee/state.py` - Added collar state management
- `llm/prompts.py` - Added dynamic speech instructions
- `main.py` - Added equip/unequip commands
- `ui.py` - Added help text and status display

### Database Schema
```sql
ALTER TABLE eevee_state ADD COLUMN has_translation_collar BOOLEAN DEFAULT 0
```

### Special Handling
- Using the collar auto-equips it
- Collar is non-consumable (stays in inventory)
- State persists across sessions
- Graceful fallback if collar is removed from inventory

## Future Enhancements
- Multiple collar types (different speech patterns)
- Collar durability system
- Translation accuracy that improves over time
- Voice tone variations based on mood

---

🎉 **Enjoy your more talkative Eevee!** The collar adds a new dimension to interactions while preserving Eevee's loveable personality.