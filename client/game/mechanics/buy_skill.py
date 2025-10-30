from typing import TYPE_CHECKING
from game.skills.fighting_abilities import fighting_abilities

if TYPE_CHECKING:
  from game.entities.player import Player

class BuySkillMechanic:
  def __init__(self, player: 'Player'):
    self.player = player

  def calculateSkillCost(self, baseSkillCost: int) -> int:
    playerLevel = self.player.getLevel()
    levelPenalty = playerLevel // 10
    return baseSkillCost + levelPenalty

  def canBuySkill(self, skillId: str) -> bool:
    skill = None
    for s in fighting_abilities:
      if s["id"] == skillId:
        skill = s
        break
    
    if not skill:
      return False
    
    playerClass = self.player.playerClass
    if playerClass not in skill["classes"]:
      return False
    
    if skillId in self.player.skills:
      return False
    
    actualCost = self.calculateSkillCost(skill["skillCost"])
    return self.player.skillPoints >= actualCost
  
  def buySkill(self, skillId: str) -> bool:
    if not self.canBuySkill(skillId):
      return False
    
    skill = None
    for s in fighting_abilities:
      if s["id"] == skillId:
        skill = s
        break
    
    if not skill:
      return False
    
    actualCost = self.calculateSkillCost(skill["skillCost"])
    self.player.skillPoints -= actualCost
    self.player.addSkill(skillId)
    
    return True
  
  def getSkillCostForDisplay(self, skillId: str) -> int:
    for skill in fighting_abilities:
      if skill["id"] == skillId:
        return self.calculateSkillCost(skill["skillCost"])
    return 0
