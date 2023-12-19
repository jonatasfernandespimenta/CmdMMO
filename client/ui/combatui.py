import time

class CombatUI:
    def __init__(self, player, enemy, drawFunc):
        self.player = player
        self.enemy = enemy
        self.isPlayerTurn = True
        self.drawFunc = drawFunc

    def start(self):
        print("You are fighting a " + self.enemy.name + "!")
        while self.player.hp > 0 and self.enemy.hp > 0:
            self.enemy.setIsInCombat(True)

            if self.isPlayerTurn:
                self.isPlayerTurn = False
                self.player_turn()
                self.redraw()
            else:
                self.isPlayerTurn = True
                self.enemy_turn()
                self.redraw()
        
        self.enemy.setIsInCombat(False)

    def player_turn(self):
        print("It's your turn!")
        print("What will you do?")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Run Away")
        choice = input(">> ")
        if choice == "1":
            self.player.attackEnemy(self.enemy)
        elif choice == "2":
            self.player.defend()
        elif choice == "3":
            self.player.use_item()
        elif choice == "4":
            self.player.run_away()
        else:
            print("That's not a valid choice!")

    def enemy_turn(self):
        print("It's the enemy's turn!")
        self.enemy.attackPlayer(self.player)
    
    def redraw(self):
        time.sleep(2)
        self.drawFunc()
