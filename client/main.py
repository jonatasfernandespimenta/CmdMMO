from blessed import Terminal
from player import Player
from board import Board
from enemy import Enemy
from ui.combatui import CombatUI
from ui.inventoryui import InventoryUi
from server import Server
import socketio

term = Terminal()

players = []
enemies = []
chests = []

sio = socketio.Client()

board = Board(enemies, chests)
boardInfo = [board.getLines(), board.getWindowWidth(), board.getWindowHeight()]

server = Server(sio, 'localhost', 3001, players, boardInfo)


def draw():
  print(term.home + term.clear)
  board.init(players, term)

def main():
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

    player = Player(boardInfo[0], boardInfo[1], boardInfo[2], [0, 0], playerName, playerClass, term)

    board.createRandomEnemies(5)
    board.createRandomChests(5)

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
        print(term.move_y(term.height // 2 + 3) + term.center(term.white('Stage Reached: ') + term.magenta(str(board.getCurrentLevel()))).rstrip())
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
      
      if board.isPortalActive() and board.getPortalPosition() == player.getPlayerPosition():
        print(term.home + term.clear)
        print(term.move_y(term.height // 2 - 1) + term.center(term.bold_green('=== STAGE ' + str(board.getCurrentLevel()) + ' COMPLETE! ===')).rstrip())
        print(term.move_y(term.height // 2 + 1) + term.center(term.bold_magenta('Entering portal...')).rstrip())
        
        nextStage = board.getCurrentLevel() + 1
        if nextStage % 5 == 0:
          print(term.move_y(term.height // 2 + 3) + term.center(term.bold_red('!!! WARNING: BOSS ROOM AHEAD !!!')).rstrip())
        
        print(term.move_y(term.height // 2 + 4) + term.center(term.yellow('Advancing to Stage ' + str(nextStage) + '...')).rstrip())
        import time
        time.sleep(3)
        board.nextLevel()

      if player.collidedWithEnemy(enemies):
        for enemy in enemies:
          if enemy.getEnemyPosition() == player.getPlayerPosition():
            combatUI = CombatUI(player, enemy, draw, term)
            combatUI.start()
            break

main()
