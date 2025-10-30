import time
from game.skills.fighting_abilities import fighting_abilities

class CombatUI:
    def __init__(self, player, enemy, drawFunc, term, party=None, sio=None):
        self.player = player
        self.enemy = enemy
        self.isPlayerTurn = True
        self.drawFunc = drawFunc
        self.term = term
        self.party = party
        self.sio = sio

    def start(self):
        print(self.term.home + self.term.clear)
        print(self.term.bold_red("You are fighting a " + self.enemy.getName() + " [Lvl " + str(self.enemy.getLevel()) + "]!"))
        self._display_enemy_status()
        self._display_player_status()
        while self.player.hp > 0 and self.enemy.hp > 0:
            self.enemy.setIsInCombat(True)

            if self.isPlayerTurn:
                self.isPlayerTurn = False
                self.player_turn()
                self._process_turn_end()
                self._wait_for_continue()
                self.redraw()
                self._display_player_status()
            else:
                self.isPlayerTurn = True
                self.enemy_turn()
                self._process_turn_end()
                self._wait_for_continue()
                self.redraw()
                self._display_player_status()
        
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
            
            # Sync enemy death with party if in party
            if self.sio and self.party and self.party.is_in_party():
                import json
                self.sio.emit('enemy_died', json.dumps({
                    'playerId': self.player.getName(),
                    'enemyId': self.enemy.getID()
                }))
            
            time.sleep(2)

    def player_turn(self):
        print(self.term.bold_cyan("\nIt's your turn!"))
        print(self.term.yellow("What will you do?"))
        print(self.term.green("1. ") + "Attack")
        print(self.term.green("2. ") + "Use Skill")
        print(self.term.green("3. ") + "Defend")
        print(self.term.green("4. ") + "Use Item")
        print(self.term.green("5. ") + "Run Away")
        
        choice = ''
        while True:
            key = self.term.inkey(timeout=0.1)
            if key and key.isprintable():
                choice = key
                break
        
        if choice == "1":
            self.player.attackEnemy(self.enemy)
        elif choice == "2":
            self.use_skill()
        elif choice == "3":
            print(self.term.blue("You defended!"))
            # Could add defense buff here
        elif choice == "4":
            self.open_inventory()
        elif choice == "5":
            print(self.term.red("You ran away!"))
        else:
            print(self.term.red("That's not a valid choice!"))
    
    def _display_enemy_status(self):
        """Display enemy HP and status effects"""
        hp_text = "Enemy HP: " + str(self.enemy.getHp()) + "/" + str(self.enemy.getMaxHp())
        
        status_parts = []
        
        # Check if enemy is stunned and add status
        stun_info = self.enemy.getStun()
        if stun_info['isStunned']:
            status_parts.append(self.term.bold_magenta("[STUNNED - " + str(stun_info['duration']) + " turn(s)]"))
        
        # Display active DoT effects
        dot_effects = self.enemy.getDotEffects()
        if dot_effects:
            for effect in dot_effects:
                status_parts.append(self.term.red("[" + effect['name'] + ": " + str(effect['damage']) + " dmg/turn - " + str(effect['duration']) + " turn(s)]"))
        
        # Print HP with all status effects
        if status_parts:
            print(self.term.yellow(hp_text) + " " + " ".join(status_parts))
        else:
            print(self.term.yellow(hp_text))
    
    def _display_player_status(self):
        """Display player HP and MP"""
        hp_text = "Your HP: " + str(self.player.getHp()) + "/" + str(self.player.getMaxHp())
        mp_text = "MP: " + str(self.player.getMP()) + "/" + str(self.player.maxMp)
        
        # Color code HP based on percentage
        hp_percentage = self.player.getHp() / self.player.getMaxHp()
        if hp_percentage > 0.5:
            hp_color = self.term.green
        elif hp_percentage > 0.25:
            hp_color = self.term.yellow
        else:
            hp_color = self.term.red
        
        # Color code MP based on percentage
        mp_percentage = self.player.getMP() / self.player.maxMp
        if mp_percentage > 0.5:
            mp_color = self.term.cyan
        elif mp_percentage > 0.25:
            mp_color = self.term.yellow
        else:
            mp_color = self.term.red
        
        print(hp_color(hp_text) + " | " + mp_color(mp_text))
    
    def _process_turn_end(self):
        """Process end of turn effects (e.g., decrease stun duration, apply DoT damage)"""
        # Process stun
        stun_info = self.enemy.getStun()
        if stun_info['isStunned']:
            new_duration = stun_info['duration'] - 1
            if new_duration <= 0:
                self.enemy.setStun(False, 0)
                print(self.term.cyan("The enemy recovered from stun!"))
            else:
                self.enemy.setStun(True, new_duration)
        
        # Process DoT effects on enemy
        enemy_dot_damage, enemy_expired = self.enemy.processDotEffects()
        if enemy_dot_damage > 0:
            self.enemy.setHp(self.enemy.getHp() - enemy_dot_damage)
            print(self.term.red("The enemy takes " + str(enemy_dot_damage) + " damage from effects!"))
            
            for i in enemy_expired:
                print(self.term.cyan("An effect on the enemy has worn off!"))
        
        # Process DoT effects on player
        player_dot_damage, player_expired = self.player.processDotEffects()
        if player_dot_damage > 0:
            self.player.setHp(self.player.getHp() - player_dot_damage)
            print(self.term.red("You take " + str(player_dot_damage) + " damage from effects!"))
            
            for i in player_expired:
                print(self.term.cyan("An effect on you has worn off!"))
    
    def use_skill(self):
        """Display skill selection menu and use selected skill"""
        # Get player's learned skills
        learnedSkills = []
        for skillId in self.player.skills:
            skill = next((s for s in fighting_abilities if s["id"] == skillId), None)
            if skill:
                learnedSkills.append(skill)
        
        if not learnedSkills:
            print(self.term.yellow("\nYou haven't learned any skills yet!"))
            print(self.term.cyan("Press K outside of combat to learn skills."))
            time.sleep(2)
            return
        
        # Display learned skills
        print(self.term.home + self.term.clear)
        print(self.term.bold_cyan('=== SELECT SKILL ==='))
        print()
        print(self.term.yellow(f'MP: {self.player.getMP()}/{self.player.maxMp}'))
        print(self.term.white('─' * 60))
        print()
        
        for idx, skill in enumerate(learnedSkills):
            skillId = skill["id"]
            skillLevel = self.player.getSkillLevel(skillId)
            
            # Get scaled values
            damage = self.player.getScaledSkillDamage(skillId, skill["damage"])
            mpCost = self.player.getScaledSkillMpCost(skillId, skill["mpCost"])
            
            # Check if player has enough MP
            canUse = self.player.getMP() >= mpCost
            
            # Skill display
            if canUse:
                print(self.term.green(f"{idx + 1}. ") + self.term.white(f"{skill['name']} (Lv.{skillLevel})"))
            else:
                print(self.term.white(f"{idx + 1}. {skill['name']} (Lv.{skillLevel})") + self.term.red(" - NOT ENOUGH MP"))
            
            # Skill info
            info_parts = []
            if damage > 0:
                info_parts.append(f"Damage: {damage}")
            if skill["stunChance"] > 0:
                info_parts.append(f"Stun: {int(skill['stunChance']*100)}%")
            if skill["duration"] > 0 and skill["effectPerTurn"] > 0:
                info_parts.append(f"DoT: {skill['effectPerTurn']}/turn")
            info_parts.append(f"MP: {mpCost}")
            
            print(f"   {self.term.cyan(' | '.join(info_parts))}")
            print()
        
        print(self.term.white('-' * 60))
        print(self.term.white("Q. Cancel"))
        print()
        
        # Get player choice
        choice = ''
        while True:
            key = self.term.inkey(timeout=0.1)
            if key and key.isprintable():
                choice = key
                break
        
        if choice.lower() == 'q':
            print(self.term.yellow("Cancelled."))
            time.sleep(1)
            return
        
        # Validate choice
        if choice.isdigit():
            skillIndex = int(choice) - 1
            if 0 <= skillIndex < len(learnedSkills):
                selectedSkill = learnedSkills[skillIndex]
                skillId = selectedSkill["id"]
                mpCost = self.player.getScaledSkillMpCost(skillId, selectedSkill["mpCost"])
                
                # Check if player has enough MP
                if self.player.getMP() >= mpCost:
                    # Use the skill via combat system
                    enemyDied = self.player.combat.attack(self.player, self.enemy, "You", "the enemy", skillId)
                    
                    if enemyDied:
                        print(self.term.bold_green("\nYou killed the enemy!"))
                        self.enemy.removeEnemy(self.player.lines)
                    else:
                        # Enemy counterattacks if still alive
                        print()
                        time.sleep(1)
                else:
                    print(self.term.red("\nNot enough MP!"))
                    time.sleep(1.5)
            else:
                print(self.term.red("\nInvalid skill selection!"))
                time.sleep(1)
        else:
            print(self.term.red("\nInvalid choice!"))
            time.sleep(1)
    
    def open_inventory(self):
        """Open inventory during combat"""
        from game.ui.inventoryui import InventoryUi
        
        inventory_ui = InventoryUi(self.player, self.term)
        inventory_ui.draw()
        
        # Redraw combat screen after inventory closes
        print(self.term.home + self.term.clear)
        print(self.term.bold_red("You are fighting a " + self.enemy.getName() + " [Lvl " + str(self.enemy.getLevel()) + "]!"))
        self._display_enemy_status()
        print(self.term.cyan("Your HP: " + str(self.player.getHp()) + "/" + str(self.player.getMaxHp())))

    def enemy_turn(self):
        # Check if enemy is stunned
        stun_info = self.enemy.getStun()
        if stun_info['isStunned']:
            print(self.term.bold_magenta("\nThe enemy is stunned and cannot act!"))
            return
        
        print(self.term.bold_red("\nIt's the enemy's turn!"))
        self.enemy.attackPlayer(self.player)
    
    def _wait_for_continue(self):
        """Wait for user to press a key to continue"""
        print("\n[Press any key to continue...]")
        self.term.inkey()
    
    def redraw(self):
        self.drawFunc()
