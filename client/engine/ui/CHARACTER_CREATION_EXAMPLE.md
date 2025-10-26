# CharacterCreationUI - Usage Examples

## Basic Usage

### Simple Name Input
```python
from engine.ui.character_creation_ui import CharacterCreationUI
from blessed import Terminal

term = Terminal()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    char_ui = CharacterCreationUI(term)
    name = char_ui.getName()
    print(f"Welcome, {name}!")
```

### Custom Name Input
```python
name = char_ui.getName(
    title='=== MY GAME ===',
    prompt='Choose your hero name: ',
    max_length=15
)
```

## Class Selection

### Basic Class Selection
```python
classes = [
    {
        'key': '1',
        'name': 'Warrior',
        'description': 'Strong melee fighter',
        'stats': 'HP: 100 | Attack: 20 | Defense: 15',
        'color': 'bold_red',
        'id': 'warrior'
    },
    {
        'key': '2',
        'name': 'Mage',
        'description': 'Master of magic',
        'stats': 'HP: 60 | Magic: 30 | Defense: 5',
        'color': 'bold_blue',
        'id': 'mage'
    }
]

selected_class = char_ui.selectClass(
    title='=== CHOOSE YOUR PATH ===',
    classes=classes
)
```

## Complete Character Creation

### All-in-One
```python
from engine.ui.character_creation_ui import CharacterCreationUI
from blessed import Terminal

term = Terminal()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    char_ui = CharacterCreationUI(term)
    
    classes = [
        {
            'key': '1',
            'name': 'Rogue',
            'description': 'High attack & luck, low defense',
            'stats': 'HP: 80 | Attack: 15 | Defense: 4 | Luck: 8',
            'color': 'bold_green',
            'id': 'rogue'
        },
        {
            'key': '2',
            'name': 'Knight',
            'description': 'High HP & defense, balanced',
            'stats': 'HP: 120 | Attack: 12 | Defense: 10 | Luck: 3',
            'color': 'bold_blue',
            'id': 'knight'
        },
        {
            'key': '3',
            'name': 'Wizard',
            'description': 'Highest attack, low defense',
            'stats': 'HP: 70 | Attack: 18 | Defense: 3 | Luck: 5',
            'color': 'bold_magenta',
            'id': 'wizard'
        }
    ]
    
    # Complete creation
    character = char_ui.create(
        game_title='=== MY RPG ===',
        name_prompt='Enter your hero name: ',
        class_title='=== SELECT CLASS ===',
        classes=classes
    )
    
    print(f"Created: {character['name']} the {character['class']}")
```

## Different Game Examples

### Example 1: Roguelike
```python
classes = [
    {
        'key': '1',
        'name': 'Explorer',
        'description': 'Quick and resourceful',
        'stats': 'Speed: High | Luck: High',
        'color': 'bold_green',
        'id': 'explorer'
    },
    {
        'key': '2',
        'name': 'Soldier',
        'description': 'Battle-hardened warrior',
        'stats': 'HP: High | Attack: High',
        'color': 'bold_red',
        'id': 'soldier'
    }
]

character = char_ui.create(
    game_title='=== DUNGEON CRAWLER ===',
    classes=classes
)
```

### Example 2: Farm Simulator
```python
classes = [
    {
        'key': '1',
        'name': 'Farmer',
        'description': 'Master of crops',
        'stats': 'Harvest: +20% | Growth: Faster',
        'color': 'bold_green',
        'id': 'farmer'
    },
    {
        'key': '2',
        'name': 'Rancher',
        'description': 'Animal specialist',
        'stats': 'Animals: +20% | Production: Higher',
        'color': 'bold_yellow',
        'id': 'rancher'
    },
    {
        'key': '3',
        'name': 'Merchant',
        'description': 'Trading expert',
        'stats': 'Prices: Better | Sales: +30%',
        'color': 'bold_cyan',
        'id': 'merchant'
    }
]

character = char_ui.create(
    game_title='=== FARM LIFE ===',
    name_prompt='Name your farm: ',
    class_title='=== CHOOSE YOUR SPECIALTY ===',
    classes=classes,
    max_name_length=25
)
```

### Example 3: Puzzle Game
```python
# Even if no classes, you can still use getName()
character = char_ui.getName(
    title='=== PUZZLE MASTER ===',
    prompt='Enter player name: '
)
```

## Customization

### Colors Available
- `bold_red`
- `bold_green`
- `bold_blue`
- `bold_yellow`
- `bold_cyan`
- `bold_magenta`
- `bold_white`
- `white`, `red`, `green`, etc.

### Key Mapping
You can use any single character as a key:
```python
{
    'key': 'w',  # Press 'w' to select
    'name': 'Warrior',
    ...
}
```

## Benefits

✅ **Reusable** - Use in any terminal game  
✅ **Customizable** - Change titles, prompts, colors  
✅ **Clean** - Separates UI from game logic  
✅ **Consistent** - Same UX across different games  
✅ **Simple** - Easy to integrate
