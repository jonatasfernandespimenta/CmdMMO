from blessed import Terminal
from engine.core.game_client import GameClient
from engine.ui.character_creation_ui import CharacterCreationUI
from game.entities.player import Player
from game.maps.dungeon import Dungeon
from game.maps.city import City
from game.entities.enemy import Enemy
from game.ui.combatui import CombatUI
from game.ui.inventoryui import InventoryUi
from game.server import Server
from game.mechanics.farm import farm
import socketio
import time

def main():
  # Initialize terminal and game client
  term = Terminal()
  client = GameClient()
  
  # Initialize game systems
  # farm = Farm()
  # client.registerSystem('farm', farm)
  
  # Initialize network
  players = []
  enemies = []
  chests = []
  
  sio = socketio.Client()
  
  # Setup maps
  city = City()
  city.createBoard()
  
  dungeon = Dungeon(enemies, chests)
  dungeon.setCityMap(city)
  city.setDungeonMap(dungeon)
  
  cityInfo = [city.getLines(), city.getWindowWidth(), city.getWindowHeight()]
  
  server = Server(sio, 'localhost', 3001, players, cityInfo)
  
  # Player creation UI
  with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    char_creator = CharacterCreationUI(term)
    
    # Define available classes
    available_classes = [
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
    
    # Create character
    character = char_creator.create(
      game_title='=== CMD MMO ===',
      name_prompt='Enter your name: ',
      class_title='=== SELECT YOUR CLASS ===',
      classes=available_classes
    )
    
    playerName = character['name']
    playerClass = character['class']

    # Create player
    player = Player(cityInfo[0], cityInfo[1], cityInfo[2], [0, 0], playerName, playerClass, term)

    combatUI = CombatUI(player, enemies, client.draw, term)
    inventoryUI = InventoryUi(player, term)

    if player not in players:
      players.append(player)

    # Setup game client
    client.setCurrentMap(city)
    client.setPlayer(player)
    client.sio = sio  # Store sio for network updates
    
    server.start()
    server.join(player.getName(), player.getPlayerPosition())

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
      
      if player.getIsInventoryOpen():
        inventoryUI.draw()
      else:
        client.draw()
      
      player.init(sio)
      client.update()

if __name__ == '__main__':
  main()
