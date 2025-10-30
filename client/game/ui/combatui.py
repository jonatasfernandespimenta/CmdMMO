import time

class CombatUI:
    def __init__(self, player, enemy, drawFunc, term):
        self.player = player
        self.enemy = enemy
        self.isPlayerTurn = True
        self.drawFunc = drawFunc
        self.term = term

    def start(self):
        print(self.term.home + self.term.clear)
        print(self.term.bold_red("You are fighting a " + self.enemy.getName() + " [Lvl " + str(self.enemy.getLevel()) + "]!"))
        print(self.term.yellow("Enemy HP: " + str(self.enemy.getHp()) + "/" + str(self.enemy.getMaxHp())))
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
        
        if self.player.getHp() > 0:
            drops = self.enemy.get_drops()
            self.player.addGold(drops['gold'])
            self.player.addXp(drops['xp'])
            
            print(self.term.bold_yellow("\nYou earned " + str(drops['gold']) + " gold and " + str(drops['xp']) + " XP!"))
            
            if drops['items']:
                for item in drops['items']:
                    self.player.addToInventory(item)
                    print(self.term.bold_green("You got: " + item['name'] + "!"))
            
            time.sleep(2)

    def player_turn(self):
        print(self.term.bold_cyan("\nIt's your turn!"))
        print(self.term.yellow("What will you do?"))
        print(self.term.green("1. ") + "Attack")
        print(self.term.green("2. ") + "Defend")
        print(self.term.green("3. ") + "Use Item")
        print(self.term.green("4. ") + "Run Away")
        
        choice = ''
        while True:
            key = self.term.inkey(timeout=0.1)
            if key and key.isprintable():
                choice = key
                break
        
        if choice == "1":
            self.player.attackEnemy(self.enemy)
        elif choice == "2":
            print(self.term.blue("You defended!"))
        elif choice == "3":
            self.open_inventory()
        elif choice == "4":
            print(self.term.red("You ran away!"))
        else:
            print(self.term.red("That's not a valid choice!"))
    
    def open_inventory(self):
        """Open inventory during combat"""
        from game.ui.inventoryui import InventoryUi
        
        inventory_ui = InventoryUi(self.player, self.term)
        inventory_ui.draw()
        
        # Redraw combat screen after inventory closes
        print(self.term.home + self.term.clear)
        print(self.term.bold_red("You are fighting a " + self.enemy.getName() + " [Lvl " + str(self.enemy.getLevel()) + "]!"))
        print(self.term.yellow("Enemy HP: " + str(self.enemy.getHp()) + "/" + str(self.enemy.getMaxHp())))
        print(self.term.cyan("Your HP: " + str(self.player.getHp()) + "/" + str(self.player.getMaxHp())))

    def enemy_turn(self):
        print(self.term.bold_red("\nIt's the enemy's turn!"))
        self.enemy.attackPlayer(self.player)
    
    def redraw(self):
        time.sleep(2)
        self.drawFunc()
