import os 

from player import Player
from board import Board
from enemy import Enemy
from ui.combatui import CombatUI
from ui.inventoryui import InventoryUi
from server import Server
import socketio


players = []
enemies = []
chests = []

sio = socketio.Client()

board = Board(enemies, chests)
boardInfo = [board.getLines(), board.getWindowWidth(), board.getWindowHeight()]

server = Server(sio, 'localhost', 3001, players, boardInfo)


def draw():
  os.system('clear')
  board.init(players)

def main():
  playerName = input('Enter your name: ')

  player = Player(boardInfo[0], boardInfo[1], boardInfo[2], [0, 0], playerName)

  board.createRandomEnemies(5)
  board.createRandomChests(5)

  combatUI = CombatUI(player, enemies, draw)
  inventoryUI = InventoryUi(player)

  if player not in players:
    players.append(player)

  server.start()
  server.join(player.getName(), player.getPlayerPosition())

  while True:
    if player.getIsInventoryOpen():
      inventoryUI.draw()
    else:
      draw()
    player.init(sio)

    if player.collidedWithEnemy(enemies):
      for enemy in enemies:
        if enemy.getEnemyPosition() == player.getPlayerPosition():
          combatUI = CombatUI(player, enemy, draw)
          combatUI.start()
          break

main()
