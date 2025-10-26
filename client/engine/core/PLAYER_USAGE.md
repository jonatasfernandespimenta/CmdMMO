# Engine Player Class - Usage Guide

## Overview

The engine's `Player` class provides basic functionality for any top-down terminal game:
- ✅ Movement (WASD / Arrow keys)
- ✅ Level and XP system
- ✅ Inventory system
- ✅ Gold system
- ✅ Temporary notifications
- ✅ HP/Attack/Defense management

## Basic Usage

### Simple Player (No Customization)
```python
from engine.core.player import Player
from blessed import Terminal

term = Terminal()
board = [['.' for x in range(30)] for y in range(15)]

player = Player(
    lines=board,
    windowWidth=30,
    windowHeight=15,
    playerPosition=[7, 15],
    name="Hero",
    term=term
)

# Game loop
while True:
    player.update()  # Handle movement
    player.drawPlayer()
```

### With Custom Blockers
```python
player = Player(
    lines=board,
    windowWidth=30,
    windowHeight=15,
    playerPosition=[0, 0],
    name="Hero",
    term=term,
    blockers=['#', 'W', 'T']  # Custom blocking characters
)
```

## Extending Player

### Example 1: RPG with Classes
```python
from engine.core.player import Player as BasePlayer

class RPGPlayer(BasePlayer):
    CLASSES = {
        'warrior': {'hp': 120, 'attack': 15, 'defense': 10},
        'mage': {'hp': 70, 'attack': 20, 'defense': 5},
    }
    
    def __init__(self, lines, windowWidth, windowHeight, position, name, player_class, term):
        super().__init__(lines, windowWidth, windowHeight, position, name, term)
        
        # Override stats based on class
        stats = self.CLASSES[player_class]
        self.hp = stats['hp']
        self.maxHp = stats['hp']
        self.attack = stats['attack']
        self.defense = stats['defense']
        
        self.player_class = player_class
    
    def getPlayerClass(self):
        return self.player_class.capitalize()
```

### Example 2: Adding Skills
```python
from engine.core.player import Player as BasePlayer

class PlayerWithSkills(BasePlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skills = {
            'fireball': {'damage': 50, 'mana_cost': 20},
            'heal': {'heal': 30, 'mana_cost': 15}
        }
        self.mana = 100
        self.maxMana = 100
    
    def castSkill(self, skill_name, target=None):
        if skill_name not in self.skills:
            return False
        
        skill = self.skills[skill_name]
        if self.mana < skill['mana_cost']:
            self.showNotification("Not enough mana!")
            return False
        
        self.mana -= skill['mana_cost']
        
        if 'damage' in skill and target:
            target.hp -= skill['damage']
        elif 'heal' in skill:
            self.hp = min(self.hp + skill['heal'], self.maxHp)
        
        return True
```

### Example 3: Adding Hunger System
```python
from engine.core.player import Player as BasePlayer
import time

class SurvivalPlayer(BasePlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hunger = 100
        self.last_hunger_tick = time.time()
    
    def update(self, network_callback=None):
        super().update(network_callback)
        
        # Decrease hunger over time
        if time.time() - self.last_hunger_tick > 5:  # Every 5 seconds
            self.hunger = max(0, self.hunger - 1)
            self.last_hunger_tick = time.time()
            
            if self.hunger == 0:
                self.hp -= 1  # Starving!
                self.showNotification("You're starving!")
    
    def eat(self, food_item):
        self.hunger = min(100, self.hunger + food_item['hunger_value'])
        self.showNotification(f"Ate {food_item['name']}!")
```

## Available Methods

### Movement
- `movePlayer(network_callback=None)` - Handle WASD/Arrow movement
- `pathIsBlocked(position)` - Check if position is blocked
- `drawPlayer()` - Draw player on board
- `removePlayer()` - Remove player from board

### Position
- `getPlayerPosition()` - Get [y, x] position
- `setPlayerPosition(position)` - Set position
- `setBoard(lines, width, height)` - Change board/map

### Stats
- `getHp()`, `setHp(hp)` - HP management
- `getMaxHp()` - Get max HP
- `getAttack()`, `setAttack(attack)` - Attack stat
- `getDefense()`, `setDefense(defense)` - Defense stat
- `getName()` - Get player name

### Level System
- `getLevel()` - Current level
- `getXp()` - Current XP
- `getXpToNextLevel()` - XP needed for next level
- `addXp(amount)` - Add XP (auto levels up)
- `levelUp()` - Manual level up (can override)

### Inventory
- `getInventory()` - Get inventory with quantities
- `addToInventory(item)` - Add item
- `dropItem(index)` - Remove item
- `equipItem(index)` - Equip item (applies effects)
- `getIsInventoryOpen()`, `setIsInventoryOpen(bool)` - Inventory UI state

### Gold
- `getGold()` - Get gold amount
- `addGold(amount)` - Add/remove gold

### Notifications
- `showNotification(message, duration=3.0)` - Show temp message
- `getNotification()` - Get current notification

### Update
- `update(network_callback=None)` - Called every frame

## Overriding Methods

### Custom Level Up
```python
def levelUp(self):
    super().levelUp()  # Call base levelUp
    
    # Custom stat increases
    self.mana += 10
    self.luck += 1
    
    # Custom notification
    self.showNotification(f"LEVEL {self.level}! You feel more powerful!")
```

### Custom Movement
```python
def movePlayer(self, network_callback=None):
    # Add sprint feature
    key = self.term.inkey(timeout=0.05)
    
    sprint = key == 'SHIFT'  # If holding shift
    move_distance = 2 if sprint else 1
    
    # Then call super or implement custom movement
    super().movePlayer(network_callback)
```

## Complete Example: Roguelike

```python
from engine.core.player import Player as BasePlayer
import random

class RoguelikePlayer(BasePlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hunger = 100
        self.keys = 0  # Keys collected
        self.floor = 1
    
    def levelUp(self):
        super().levelUp()
        self.showNotification(f"Level {self.level}! +10 HP, +2 ATK")
    
    def moveToNextFloor(self):
        self.floor += 1
        self.hp = self.maxHp  # Heal on new floor
        self.showNotification(f"Entered floor {self.floor}!")
    
    def collectKey(self):
        self.keys += 1
        self.showNotification(f"Found key! ({self.keys} total)")
    
    def unlockDoor(self):
        if self.keys > 0:
            self.keys -= 1
            return True
        self.showNotification("Need a key!")
        return False
```

## Benefits

✅ **Reusable** - Use in any top-down game  
✅ **Extensible** - Easy to add new features  
✅ **Complete** - Level, inventory, gold systems already ready  
✅ **Clean** - Organized and documented code  
✅ **Tested** - Used in CmdMMO
