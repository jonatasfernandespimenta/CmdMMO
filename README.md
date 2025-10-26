# CmdMMO

A multiplayer terminal-based roguelike MMO game where players explore procedurally generated dungeons, fight enemies, collect loot, and level up their characters.

## Overview

CmdMMO is a real-time multiplayer game that runs entirely in the terminal. Players can see each other moving around the game world, engage in turn-based combat with enemies, collect items from chests, and progress through increasingly challenging stages. The game features a boss every 5 stages and includes RPG mechanics like leveling, stats, and inventory management.

## Features

- **Multiplayer**: See other players in real-time as they move around the map
- **Three Character Classes**: 
  - **Rogue**: High attack & luck, low defense (HP: 80, ATK: 15, DEF: 4, LUCK: 8)
  - **Knight**: High HP & defense, balanced (HP: 120, ATK: 12, DEF: 10, LUCK: 3)
  - **Wizard**: Highest attack, low defense (HP: 70, ATK: 18, DEF: 3, LUCK: 5)
- **Procedurally Generated Dungeons**: Each level features unique layouts with walls and pathways
- **Progressive Difficulty**: Enemies scale with each stage, getting stronger as you progress
- **Boss Battles**: Every 5th stage features a powerful boss with minions
- **Turn-Based Combat**: Strategic combat system with critical hits and miss chances
- **Leveling System**: Gain XP from defeating enemies to level up and improve stats
- **Loot System**: Collect potions and swords from chests scattered throughout the dungeon
- **Inventory Management**: Store and use items to enhance your character
- **Portal System**: Clear all enemies to spawn a portal to the next stage

## Tech Stack

### Backend (Server)
- **Node.js** with Express
- **Socket.IO** for real-time multiplayer communication
- WebSocket-based player synchronization

### Frontend (Client)
- **Python 3**
- **Blessed** library for terminal UI rendering
- **python-socketio** for client-server communication
- **keyboard** library for input handling

## Installation

### Prerequisites
- Python 3.7+
- Node.js 14+
- npm

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CmdMMO
   ```

2. **Install server dependencies**
   ```bash
   cd server
   npm install
   cd ..
   ```

3. **Install client dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

### Start the Server
In the `server` directory:
```bash
cd server
node index.js
```
The server will start on port 3001.

### Start the Client
In the project root directory, run:
```bash
python client/main.py
```

### Multiple Players
To play with multiple people, each player should:
1. Ensure they can connect to the server (update server address in `client/server.py` if needed)
2. Run `python client/main.py` in their own terminal

## How to Play

### Controls
- **W/↑**: Move up
- **S/↓**: Move down
- **A/←**: Move left
- **D/→**: Move right
- **I**: Toggle inventory

### Gameplay Loop
1. **Character Creation**: Enter your name and choose your class
2. **Exploration**: Navigate the procedurally generated dungeon
3. **Combat**: Collide with enemies (marked as `E`) to enter turn-based combat
4. **Looting**: Walk over chests (marked as `▣`) to collect items
5. **Progression**: Defeat all enemies to spawn a portal (`U`)
6. **Advance**: Enter the portal to proceed to the next stage

### Combat System
- **Attack**: Deal damage based on your attack stat minus enemy defense
- **Critical Hits**: Your luck stat determines critical hit chance (double damage)
- **Enemy Attacks**: Enemies attack based on their stats; luck gives you a chance to dodge
- **Victory**: Defeat enemies to gain XP and gold

### Leveling
- Gain XP by defeating enemies
- Level up to increase HP, attack, defense, and luck
- XP required for next level increases by 1.5x each time
- HP fully restored on level up

### Stage Progression
- **Normal Stages**: Fight regular enemies (Snakes)
- **Boss Stages**: Every 5th stage features a Shadow Lord boss with minions
- Enemies scale in strength with each stage
- More enemies and chests spawn at higher stages

## Project Structure

```
CmdMMO/
├── server/
│   ├── index.js           # Express + Socket.IO server
│   └── package.json       # Server dependencies
├── client/
│   ├── main.py           # Game entry point
│   ├── player.py         # Player class and mechanics
│   ├── enemy.py          # Enemy AI and combat
│   ├── board.py          # Game board and level management
│   ├── chest.py          # Loot chest mechanics
│   ├── procedural_board.py  # Dungeon generation
│   ├── server.py         # Client-server communication
│   ├── items/
│   │   ├── potions.py    # Potion definitions
│   │   └── swords.py     # Sword definitions
│   ├── ui/
│   │   ├── combatui.py   # Combat interface
│   │   └── inventoryui.py # Inventory interface
│   └── arts/
│       ├── merchant.py   # ASCII art
│       ├── potions.py    # ASCII art
│       └── swords.py     # ASCII art
└── requirements.txt      # Python dependencies
```

## Game Mechanics

### Stats
- **HP**: Health points - when it reaches 0, game over
- **Attack**: Damage dealt to enemies (reduced by enemy defense)
- **Defense**: Reduces incoming damage from enemies
- **Luck**: Increases critical hit chance and dodge chance

### Items
- **Potions**: Restore or boost HP
- **Swords**: Increase attack power
- Items can be collected from chests and used from inventory

### Enemies
- Regular enemies spawn with stats based on current stage level
- Bosses have 3x HP, 2x attack, and 2x defense of regular enemies
- Enemies drop gold and XP when defeated
- Boss encounters include minions for added challenge

## Known Limitations

- Server currently runs on localhost (port 3001)
- No authentication system
- Game state is not persisted between sessions
- Limited enemy variety (Snake and Shadow Lord)

## Roadmap

Planned features and improvements for future versions:

### Skills System
- Class-specific abilities and special attacks
- Active and passive skill trees
- Cooldown-based skill mechanics
- Skill points earned through leveling
- Ultimate abilities unlocked at higher levels

### Level Up System Enhancement
- Interactive level-up screen with stat allocation
- Choice between different upgrade paths
- Unlock new abilities and perks at milestone levels
- Visual celebrations and notifications
- Prestige system for endgame progression

### Blacksmith System
- Weapon and armor upgrading mechanics
- Material gathering from enemies and chests
- Equipment enhancement with success/failure rates
- Unique enchantments and forging recipes
- Blacksmith NPC interaction in safe zones

### Merchant System
- Buy and sell items with gold
- Rotating inventory of rare items
- Price negotiation mechanics based on luck stat
- Special merchant events and limited-time offers
- Trade-in system for unwanted equipment

### Expanded Item Variety
- Armor sets (helmets, chest plates, boots, gloves)
- Accessories (rings, amulets, talismans)
- Consumables (buff potions, scrolls, food)
- Crafting materials and resources
- Legendary and mythic rarity items
- Set bonuses for wearing complete equipment sets

### GPT Integration for Story Generation
- Dynamically generated quest narratives
- Unique enemy descriptions and lore
- Procedurally generated NPC dialogues
- Contextual story events based on player actions
- Personalized dungeon backstories
- AI-powered merchant personalities and interactions

### Farming System
- Plant and harvest crops in safe zones or home base
- Grow alchemical ingredients for potion crafting
- Time-based crop growth mechanics
- Irrigation and fertilizer systems for better yields
- Rare seed drops from enemies and chests
- Trade or sell harvested crops to merchants

### Ranking System
- Player progression tracked through rank tiers (gold, phase, level)
- Gold rank representing overall achievement milestones
- Phase system for dividing progression into distinct stages
- Level tracking within each phase
- Rank-based rewards and unlocks
- Leaderboards showing top-ranked players
- Visual rank indicators in player display

## Future Enhancements

- More enemy types and variations
- Additional character classes
- Trading between players
- More diverse procedural generation
- PvP combat system

## Contributing

Feel free to fork this project and submit pull requests for improvements or bug fixes.

## License

This project is open source and available for educational and personal use.

## Credits

Built with Python, Node.js, Socket.IO, and the Blessed terminal library.
