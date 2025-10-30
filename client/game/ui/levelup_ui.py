import time

class LevelUpUI:
  """UI for level up celebration and stat upgrade selection"""
  
  def __init__(self, player, term):
    self.player = player
    self.term = term
  
  def celebrate(self):
    """Show celebration screen for level up"""
    print(self.term.home + self.term.clear)
    
    # Center the celebration message
    center_y = self.term.height // 2
    
    # Animated celebration
    for i in range(3):
      print(self.term.home + self.term.clear)
      
      if i % 2 == 0:
        print(self.term.move_y(center_y - 4) + self.term.center(self.term.bold_yellow('★ ★ ★ ★ ★')).rstrip())
        print(self.term.move_y(center_y - 2) + self.term.center(self.term.bold_green('═══ LEVEL UP! ═══')).rstrip())
      else:
        print(self.term.move_y(center_y - 4) + self.term.center(self.term.bold_white('★ ★ ★ ★ ★')).rstrip())
        print(self.term.move_y(center_y - 2) + self.term.center(self.term.bold_cyan('═══ LEVEL UP! ═══')).rstrip())
      
      print(self.term.move_y(center_y) + self.term.center(self.term.white(f'You are now level {self.player.getLevel()}!')).rstrip())
      print(self.term.move_y(center_y + 2) + self.term.center(self.term.cyan('You feel more powerful...')).rstrip())
      
      time.sleep(0.4)
    
    # Final screen with stats
    print(self.term.home + self.term.clear)
    print(self.term.move_y(center_y - 4) + self.term.center(self.term.bold_yellow('★ ★ ★ ★ ★')).rstrip())
    print(self.term.move_y(center_y - 2) + self.term.center(self.term.bold_green('═══ LEVEL UP! ═══')).rstrip())
    print(self.term.move_y(center_y) + self.term.center(self.term.white(f'You are now level {self.player.getLevel()}!')).rstrip())
    print()
    
    # Show rewards
    skillPointsGained = 1 + (self.player.level // 5)
    print(self.term.move_y(center_y + 3) + self.term.center(self.term.green('Rewards:')).rstrip())
    print(self.term.move_y(center_y + 4) + self.term.center(self.term.white(f'+ {skillPointsGained} Skill Points')).rstrip())
    print(self.term.move_y(center_y + 5) + self.term.center(self.term.white('+ 5 Max MP')).rstrip())
    print(self.term.move_y(center_y + 6) + self.term.center(self.term.white('+ 1 Luck')).rstrip())
    
    print(self.term.move_y(center_y + 9) + self.term.center(self.term.white('Press any key to continue...')).rstrip())
    self.term.inkey(timeout=None)
  
  def chooseStatUpgrade(self):
    """Allow player to choose a stat to upgrade"""
    print(self.term.home + self.term.clear)
    
    print(self.term.bold_cyan('═══ STAT UPGRADE ═══'))
    print()
    print(self.term.yellow('Choose a stat to upgrade:'))
    print()
    
    # Current stats
    print(self.term.white('Current Stats:'))
    print(self.term.cyan(f'  HP: {self.player.getHp()}/{self.player.getMaxHp()}'))
    print(self.term.cyan(f'  MP: {self.player.getMP()}/{self.player.maxMp}'))
    print(self.term.cyan(f'  ATK: {self.player.getAttack()}'))
    print(self.term.cyan(f'  LCK: {self.player.getLuck()}'))
    print()
    
    # Options
    print(self.term.bold_white('Upgrade Options:'))
    print()
    print(self.term.green('1. ') + self.term.white('HP  ') + self.term.cyan('(+15 Max HP)'))
    print(self.term.green('2. ') + self.term.white('MP  ') + self.term.cyan('(+10 Max MP)'))
    print(self.term.green('3. ') + self.term.white('ATK ') + self.term.cyan('(+3 Attack)'))
    print(self.term.green('4. ') + self.term.white('LCK ') + self.term.cyan('(+2 Luck)'))
    print()
    
    # Wait for input
    while True:
      key = self.term.inkey(timeout=None)
      
      if key == '1':
        self.player.maxHp += 15
        self.player.setHp(self.player.maxHp)  # Fully heal
        print(self.term.bold_green(f'✓ Max HP increased to {self.player.maxHp}!'))
        print(self.term.green('Your wounds have been healed!'))
        break
      elif key == '2':
        self.player.maxMp += 10
        self.player.setMP(self.player.maxMp)  # Fully restore MP
        print(self.term.bold_green(f'✓ Max MP increased to {self.player.maxMp}!'))
        print(self.term.green('Your mana has been restored!'))
        break
      elif key == '3':
        self.player.setAttack(self.player.getAttack() + 3)
        print(self.term.bold_green(f'✓ Attack increased to {self.player.getAttack()}!'))
        print(self.term.green('You feel stronger!'))
        break
      elif key == '4':
        self.player.luck += 2
        print(self.term.bold_green(f'✓ Luck increased to {self.player.getLuck()}!'))
        print(self.term.green('Fortune smiles upon you!'))
        break
    
    print()
    print(self.term.white('Press any key to continue...'))
    self.term.inkey(timeout=None)
  
  def show(self):
    """Show the complete level up flow"""
    self.celebrate()
    self.chooseStatUpgrade()
