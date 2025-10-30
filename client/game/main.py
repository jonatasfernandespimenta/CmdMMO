from blessed import Terminal
from engine.core.game_client import GameClient
from engine.ui.character_creation_ui import CharacterCreationUI
from game.entities.player import Player
from game.maps.dungeon import Dungeon
from game.maps.city import City
from game.entities.enemy import Enemy
from game.ui.combatui import CombatUI
from game.ui.inventoryui import InventoryUi
from game.ui.skillsui import SkillsUI
from game.ui.levelup_ui import LevelUpUI
from game.ui.party_ui import PartyUI
from game.server import Server
from game.party import Party
from game.api_client import APIClient
import socketio
import time

def main():
  # Initialize terminal and game client
  term = Terminal()
  client = GameClient()
  
  # Initialize network
  enemies = []
  chests = []
  
  sio = socketio.Client()
  
  # Initialize party system (before maps)
  party = Party(sio, None)  # Will set player_id later
  
  # Setup maps
  city = City()
  city.createBoard()
  
  dungeon = Dungeon(enemies, chests, city_map=city, term=term, party=party, sio=sio)
  dungeon.setCityMap(city)
  city.setDungeonMap(dungeon)
  
  cityInfo = [city.getLines(), city.getWindowWidth(), city.getWindowHeight()]
  
  # Use client.players directly instead of a separate list
  server = Server(sio, 'localhost', 3001, client.players, cityInfo)
  
  # Player creation UI
  with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    char_creator = CharacterCreationUI(term)
    
    # Define available classes
    available_classes = [
      {
        'key': '1',
        'name': 'Rogue',
        'description': 'High attack & luck, low defense',
        'stats': 'HP: 80 | MP: 20 | ATK: 15 | DEF: 4 | LCK: 8',
        'color': 'bold_green',
        'id': 'rogue'
      },
      {
        'key': '2',
        'name': 'Knight',
        'description': 'High HP & defense, balanced',
        'stats': 'HP: 120 | MP: 20 | ATK: 12 | DEF: 10 | LCK: 3',
        'color': 'bold_blue',
        'id': 'knight'
      },
      {
        'key': '3',
        'name': 'Wizard',
        'description': 'Highest attack, low defense',
        'stats': 'HP: 70 | MP: 50 | ATK: 18 | DEF: 3 | LCK: 5',
        'color': 'bold_magenta',
        'id': 'ice_wizard'
      }
    ]
    
    # Create character
    character = char_creator.create(
      game_title='=== CMD MMO ===',
      name_prompt='Enter your name: ',
      class_title='=== SELECT YOUR CLASS ===',
      classes=available_classes
    )
    
    playerName = character['name']
    playerClass = character['class']
    
    # Initialize API client and create player on server
    api_client = APIClient('http://localhost:3001')
    server_response = api_client.createPlayer(
      name=playerName,
      player_class=playerClass,
      maxDungeonLevel=0,
      maxGold=0,
      maxLevelReached=1
    )
    
    if server_response:
      print(term.center(term.green(f"Player created on server with ID: {server_response['id']}")).rstrip())
      time.sleep(1)
    else:
      print(term.center(term.yellow("Warning: Could not connect to server. Playing offline mode.")).rstrip())
      time.sleep(1)
      api_client = None  # Disable API client if server is unavailable

    # Create player
    player = Player(cityInfo[0], cityInfo[1], cityInfo[2], [0, 0], playerName, playerClass, term, api_client)

    # Update party with player ID
    party.player_id = playerName
    
    inventoryUI = InventoryUi(player, term)
    skillsUI = SkillsUI(player, term)
    levelUpUI = LevelUpUI(player, term)
    partyUI = PartyUI(player, party, term)

    # Setup game client (this will add player to client.players)
    client.setCurrentMap(city)
    client.setPlayer(player)
    client.sio = sio  # Store sio for network updates
    
    server.start()
    server.join(player.getName(), player.getPlayerPosition())
    
    # Request current party state
    party.request_current_party()

  # Custom game loop (override GameClient's loop for now)
  with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    while True:
      if player.getHp() <= 0:
        print(term.home + term.clear)
        print(term.move_y(term.height // 2 - 3) + term.center(term.bold_red('=== GAME OVER ===')).rstrip())
        print(term.move_y(term.height // 2 - 1) + term.center(term.yellow('You have been defeated...')).rstrip())
        print()
        print(term.move_y(term.height // 2 + 1) + term.center(term.cyan('Final Stats:')).rstrip())
        print(term.move_y(term.height // 2 + 2) + term.center(term.white('Level: ') + term.green(str(player.getLevel()))).rstrip())
        print(term.move_y(term.height // 2 + 3) + term.center(term.white('Stage Reached: ') + term.magenta(str(dungeon.getCurrentLevel()))).rstrip())
        print(term.move_y(term.height // 2 + 4) + term.center(term.white('Gold Collected: ') + term.yellow(str(player.getGold()))).rstrip())
        print()
        print(term.move_y(term.height // 2 + 6) + term.center(term.white('Press any key to exit...')).rstrip())
        term.inkey()
        break
      
      # Check for pending level up first
      if player.pendingLevelUp:
        levelUpUI.show()
        player.pendingLevelUp = False
      elif player.getIsInventoryOpen():
        inventoryUI.draw()
      elif player.getIsSkillsMenuOpen():
        skillsUI.open()
        player.setIsSkillsMenuOpen(False)  # Reset after closing
      elif player.isPartyMenuOpen:
        partyUI.open()
        player.isPartyMenuOpen = False  # Reset after closing
      else:
        client.draw()
      
      player.init(sio)
      client.update()

if __name__ == '__main__':
  main()
