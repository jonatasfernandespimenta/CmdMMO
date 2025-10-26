from blessed import Terminal
from player import Player
from maps.dungeon import Dungeon
from maps.city import City
from enemy import Enemy
from ui.combatui import CombatUI
from ui.inventoryui import InventoryUi
from server import Server
import socketio
import time

term = Terminal()

players = []
enemies = []
chests = []

sio = socketio.Client()

city = City()
city.createBoard()

dungeon = Dungeon(enemies, chests)
dungeon.setCityMap(city)
city.setDungeonMap(dungeon)

current_map = city

cityInfo = [city.getLines(), city.getWindowWidth(), city.getWindowHeight()]

server = Server(sio, 'localhost', 3001, players, cityInfo)

def draw():
  print(term.home + term.clear)
  current_map.init(players, term)

def main():
  global current_map
  with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    print(term.home + term.clear)
    print(term.move_y(term.height // 2 - 1) + term.center(term.bold_cyan('=== CMD MMO ===')).rstrip())
    print(term.move_y(term.height // 2) + term.center('Enter your name: ').rstrip(), end='', flush=True)
    
    playerName = ''
    with term.location():
      print(term.move_y(term.height // 2 + 1) + term.center(' ' * 30).rstrip())
      name_x = (term.width - 20) // 2
      print(term.move_xy(name_x, term.height // 2 + 1), end='', flush=True)
      
      while True:
        key = term.inkey(timeout=0.1)
        if key.name == 'KEY_ENTER':
          if playerName:
            break
        elif key.name == 'KEY_BACKSPACE':
          if playerName:
            playerName = playerName[:-1]
            print(term.move_xy(name_x, term.height // 2 + 1) + term.cyan(playerName) + ' ' + term.move_left, end='', flush=True)
        elif key and key.isprintable():
          if len(playerName) < 20:
            playerName += key
            print(term.cyan(key), end='', flush=True)

    print(term.home + term.clear)
    print(term.move_y(term.height // 2 - 5) + term.center(term.bold_cyan('=== SELECT YOUR CLASS ===')).rstrip())
    print()
    print(term.move_y(term.height // 2 - 3) + term.center(term.bold_green('1. Rogue') + term.white(' - High attack & luck, low defense')).rstrip())
    print(term.move_y(term.height // 2 - 2) + term.center(term.yellow('   HP: 80 | Attack: 15 | Defense: 4 | Luck: 8')).rstrip())
    print()
    print(term.move_y(term.height // 2) + term.center(term.bold_blue('2. Knight') + term.white(' - High HP & defense, balanced')).rstrip())
    print(term.move_y(term.height // 2 + 1) + term.center(term.yellow('   HP: 120 | Attack: 12 | Defense: 10 | Luck: 3')).rstrip())
    print()
    print(term.move_y(term.height // 2 + 3) + term.center(term.bold_magenta('3. Wizard') + term.white(' - Highest attack, low defense')).rstrip())
    print(term.move_y(term.height // 2 + 4) + term.center(term.yellow('   HP: 70 | Attack: 18 | Defense: 3 | Luck: 5')).rstrip())
    print()
    print(term.move_y(term.height // 2 + 6) + term.center(term.white('Choose (1-3): ')).rstrip(), end='', flush=True)
    
    playerClass = ''
    classMap = {'1': 'rogue', '2': 'knight', '3': 'wizard'}
    
    while True:
      key = term.inkey(timeout=0.1)
      if key in classMap:
        playerClass = classMap[key]
        print(term.bold_cyan(playerClass.capitalize()))
        break

    player = Player(cityInfo[0], cityInfo[1], cityInfo[2], [0, 0], playerName, playerClass, term)

    combatUI = CombatUI(player, enemies, draw, term)
    inventoryUI = InventoryUi(player, term)

    if player not in players:
      players.append(player)

    server.start()
    server.join(player.getName(), player.getPlayerPosition())

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
        draw()
      player.init(sio)
      
      # Check for portal transitions
      transition = current_map.checkPortalTransition(player)
      if transition:
        transition.execute(player, term)
        current_map = transition.getDestinationMap()

      current_map.handleCollisions(player, combatUI, draw, term)

main()
