import time
from game.skills.fighting_abilities import fighting_abilities
from game.mechanics.buy_skill import BuySkillMechanic

class SkillsUI:
  def __init__(self, player, term):
    self.player = player
    self.term = term
    self.buySkillMechanic = BuySkillMechanic(player)
    self.selectedSkillIndex = 0
    self.scrollOffset = 0  # For scrolling through long lists
    self.maxVisibleSkills = 8  # Maximum skills to show at once
    self.isOpen = False
  
  def getPlayerClassSkills(self):
    """Get all skills available for the player's class"""
    playerClass = self.player.playerClass
    availableSkills = []
    
    for skill in fighting_abilities:
      if playerClass in skill["classes"] and "enemy" not in skill["classes"]:
        availableSkills.append(skill)
    
    return availableSkills
  
  def getSkillDescription(self, skill, isLearned=False):
    """Generate a brief description of the skill"""
    desc_parts = []
    skillId = skill["id"]
    
    # Get scaled values if skill is learned
    damage = skill["damage"]
    mpCost = skill["mpCost"]
    
    if isLearned and hasattr(self.player, 'getScaledSkillDamage'):
      damage = self.player.getScaledSkillDamage(skillId, skill["damage"])
      mpCost = self.player.getScaledSkillMpCost(skillId, skill["mpCost"])
    
    if damage > 0:
      desc_parts.append(f"Damage: {damage}")
    
    if skill["stunChance"] > 0:
      desc_parts.append(f"Stun: {int(skill['stunChance']*100)}%")
    
    if skill["duration"] > 0 and skill["effectPerTurn"] > 0:
      desc_parts.append(f"DoT: {skill['effectPerTurn']}/turn for {skill['duration']} turns")
    
    if mpCost > 0:
      desc_parts.append(f"MP Cost: {mpCost}")
    
    if skill.get("isMagical"):
      desc_parts.append(f"Type: Magical ({skill.get('elementType', 'arcane')})")
    else:
      desc_parts.append("Type: Physical")
    
    return " | ".join(desc_parts)
  
  def draw(self):
    """Draw the skills menu with cursor navigation"""
    print(self.term.home + self.term.clear)
    print(self.term.bold_cyan('=== SKILL TREE ==='))
    print(self.term.yellow(f'Class: {self.player.getPlayerClass()}'))
    print(self.term.green(f'Skill Points Available: {self.player.skillPoints}'))
    print(self.term.white('─' * 60))
    print()
    
    availableSkills = self.getPlayerClassSkills()
    
    if len(availableSkills) == 0:
      print(self.term.red("No skills available for your class!"))
      print()
      return
    
    # Calculate visible range
    totalSkills = len(availableSkills)
    startIdx = self.scrollOffset
    endIdx = min(startIdx + self.maxVisibleSkills, totalSkills)
    
    # Show scroll indicator at top if needed
    if self.scrollOffset > 0:
      print(self.term.center(self.term.white('^ More skills above ^')).rstrip())
      print()
    
    # Display visible skills
    for idx in range(startIdx, endIdx):
      skill = availableSkills[idx]
      skillId = skill["id"]
      skillName = skill["name"]
      isLearned = skillId in self.player.skills
      
      # Calculate actual cost with level scaling
      actualCost = self.buySkillMechanic.calculateSkillCost(skill["skillCost"])
      
      # Highlight selected skill
      isSelected = (idx == self.selectedSkillIndex)
      
      # Cursor/marker
      if isSelected:
        marker = self.term.bold_yellow(">")
      else:
        marker = " "
      
      # Skill name with learned indicator and level
      if isLearned:
        skillLevel = self.player.getSkillLevel(skillId)
        nameDisplay = self.term.green(f"{skillName} [LEARNED] Lv.{skillLevel}")
      else:
        nameDisplay = self.term.white(skillName)
      
      # Skill cost
      if isLearned:
        costDisplay = self.term.green("Already learned")
      else:
        costDisplay = self.term.yellow(f"Cost: {actualCost} SP")
      
      # Highlight entire row if selected
      if isSelected:
        print(self.term.on_blue(f"{marker} {skillName}".ljust(60)))
        print(f"  {self.term.cyan(self.getSkillDescription(skill, isLearned))}")
        print(f"  {costDisplay}")
      else:
        print(f"{marker} {nameDisplay}")
        print(f"  {self.term.cyan(self.getSkillDescription(skill, isLearned))}")
        print(f"  {costDisplay}")
      print()
    
    # Show scroll indicator at bottom if needed
    if endIdx < totalSkills:
      print(self.term.center(self.term.white('v More skills below v')).rstrip())
      print()
    
    print(self.term.white('─' * 60))
    print()
    print(self.term.bold_white("Controls:"))
    print(self.term.green("UP/DOWN or W/S: ") + "Navigate")
    print(self.term.green("ENTER: ") + "Select skill to learn")
    print(self.term.green("Q: ") + "Close Skills Menu")
    print()
  
  def open(self):
    """Open the skills menu and handle input"""
    self.isOpen = True
    self.selectedSkillIndex = 0
    self.scrollOffset = 0
    
    while self.isOpen:
      availableSkills = self.getPlayerClassSkills()
      totalSkills = len(availableSkills)
      
      if totalSkills == 0:
        self.draw()
        print(self.term.yellow("No skills available!"))
        time.sleep(2)
        break
      
      self.draw()
      
      key = self.term.inkey(timeout=None)
      
      if key.lower() == 'q':
        self.isOpen = False
        break
      
      # Arrow key navigation
      elif key.name == 'KEY_UP' or key.lower() == 'w':
        if self.selectedSkillIndex > 0:
          self.selectedSkillIndex -= 1
          # Adjust scroll if needed
          if self.selectedSkillIndex < self.scrollOffset:
            self.scrollOffset = self.selectedSkillIndex
      
      elif key.name == 'KEY_DOWN' or key.lower() == 's':
        if self.selectedSkillIndex < totalSkills - 1:
          self.selectedSkillIndex += 1
          # Adjust scroll if needed
          if self.selectedSkillIndex >= self.scrollOffset + self.maxVisibleSkills:
            self.scrollOffset = self.selectedSkillIndex - self.maxVisibleSkills + 1
      
      # Enter to select
      elif key.name == 'KEY_ENTER' or key == '\n' or key == '\r':
        selectedSkill = availableSkills[self.selectedSkillIndex]
        self.handleSkillSelection(selectedSkill)
  
  def handleSkillSelection(self, skill):
    """Handle when player selects a skill"""
    skillId = skill["id"]
    skillName = skill["name"]
    
    # Check if already learned
    if skillId in self.player.skills:
      print(self.term.yellow(f"You already know {skillName}!"))
      time.sleep(1.5)
      return
    
    # Show confirmation screen
    print(self.term.home + self.term.clear)
    print(self.term.bold_cyan('=== LEARN SKILL ==='))
    print()
    print(self.term.bold_white(f"Skill: {skillName}"))
    print(self.term.cyan(self.getSkillDescription(skill, False)))
    print()
    print(self.term.cyan('Note: Skills grow stronger as you level up!'))
    print()
    
    actualCost = self.buySkillMechanic.calculateSkillCost(skill["skillCost"])
    print(self.term.yellow(f"Cost: {actualCost} Skill Points"))
    print(self.term.green(f"Available: {self.player.skillPoints} Skill Points"))
    print()
    
    if actualCost > self.player.skillPoints:
      print(self.term.red("Not enough skill points!"))
      print()
      print(self.term.white("Press any key to continue..."))
      self.term.inkey(timeout=None)
      return
    
    print(self.term.bold_white("Do you want to learn this skill?"))
    print(self.term.green("Y. ") + "Yes, learn this skill")
    print(self.term.red("N. ") + "No, go back")
    print()
    
    confirmKey = self.term.inkey(timeout=None)
    
    if confirmKey.lower() == 'y':
      # Try to buy the skill
      success = self.buySkillMechanic.buySkill(skillId)
      
      if success:
        print(self.term.bold_green(f"✓ You learned {skillName}!"))
        print(self.term.white(f"Remaining skill points: {self.player.skillPoints}"))
      else:
        print(self.term.red("Failed to learn skill!"))
      
      time.sleep(2)
    else:
      print(self.term.yellow("Cancelled."))
      time.sleep(1)
