import random
from game.skills.fighting_abilities import fighting_abilities
from game.skills.elements import elements
class CombatSystem:
  """Centralized combat system handling all battle logic"""
  
  def __init__(self, term):
    self.term = term
  
  def calculateDamage(self, attacker, defender, skillId=None):
    """Calculate damage dealt from attacker to defender"""
    baseDamage = max(1, attacker.getAttack() - defender.getDefense())
    damageMultiplier = 1.0

    if skillId:
      skill = next((s for s in fighting_abilities if s["id"] == skillId), None)
      if skill:
        # Get scaled values if attacker has skill scaling methods
        skillDamage = skill["damage"]
        skillMpCost = skill["mpCost"]
        
        if hasattr(attacker, 'getScaledSkillDamage'):
          skillDamage = attacker.getScaledSkillDamage(skillId, skill["damage"])
        if hasattr(attacker, 'getScaledSkillMpCost'):
          skillMpCost = attacker.getScaledSkillMpCost(skillId, skill["mpCost"])
        
        # Check if attacker has enough MP
        if hasattr(attacker, 'getMP') and attacker.getMP() < skillMpCost:
          return None  # Not enough MP to use skill
        skillElement = skill.get("elementType", None)
        defenderElement = defender.getElementType()
        attackerElement = attacker.getElementType()
        
        if skill["stunChance"] > 0:
          if random.random() < skill["stunChance"]:
            defender.setStun(True, skill["duration"])
        
        # Apply DoT effect if skill has effectPerTurn
        if skill["effectPerTurn"] > 0 and skill["duration"] > 0:
          defender.addDotEffect(skill["name"], skill["effectPerTurn"], skill["duration"])

        if skillElement and defenderElement:
          elementData = next((e for e in elements if e["type"] == skillElement), None)
          if elementData:
            if defenderElement in elementData["weaknesses"]:
              damageMultiplier *= 1.5
            elif defenderElement in elementData["resistances"]:
              damageMultiplier *= 0.75

        if attackerElement and defenderElement:
          attackerElementData = next((e for e in elements if e["type"] == attackerElement), None)
          if attackerElementData:
            if defenderElement in attackerElementData["weaknesses"]:
              damageMultiplier *= 1.2
            elif defenderElement in attackerElementData["resistances"]:
              damageMultiplier *= 0.9

        if skill["isMagical"]:
          baseDamage = skillDamage
        else:
          baseDamage = max(1, (skillDamage + attacker.getAttack() * 0.5) - defender.getDefense())

    return max(1, baseDamage * damageMultiplier)
  
  def checkCriticalHit(self, attacker):
    """Check if attacker lands a critical hit based on luck"""
    if hasattr(attacker, 'getLuck'):
      return random.random() < attacker.getLuck() / 100
    return False
  
  def checkMiss(self, defender):
    """Check if attack misses based on defender's luck"""
    if hasattr(defender, 'getLuck'):
      return random.random() < defender.getLuck() / 100
    return False

  def attack(self, attacker, target, attackerName=None, targetName=None, skillId=None):
    """
    Generic attack method - works for both player and enemy
    
    Args:
      attacker: The entity attacking
      target: The entity being attacked
      attackerName: Name to display for attacker (e.g., "You", "The enemy")
      targetName: Name to display for target (e.g., "the enemy", "you")
      skillId: Optional skill ID to use for the attack
    
    Returns:
      bool: True if target died, False otherwise
    """
    # Helper function to safely print with or without term
    def safe_print(text, color_func=None):
      if self.term and color_func:
        print(color_func(text))
      else:
        print(text)
    
    # Check if attack misses
    if self.checkMiss(target):
      safe_print(f"{attackerName}'s attack missed!", self.term.cyan if self.term else None)
      return False
    
    # Check for critical hit
    criticalHit = self.checkCriticalHit(attacker)
    damage = self.calculateDamage(attacker, target, skillId)
    
    # If damage is None, it means not enough MP
    if damage is None:
      safe_print(f"{attackerName} doesn't have enough MP!", self.term.yellow if self.term else None)
      return False
    
    # Consume MP if using a skill
    if skillId:
      skill = next((s for s in fighting_abilities if s["id"] == skillId), None)
      if skill and hasattr(attacker, 'setMP'):
        # Get scaled MP cost if available
        mpCost = skill["mpCost"]
        if hasattr(attacker, 'getScaledSkillMpCost'):
          mpCost = attacker.getScaledSkillMpCost(skillId, skill["mpCost"])
        
        attacker.setMP(attacker.getMP() - mpCost)
        
        # Show skill level if attacker has skill scaling
        skillInfo = f"{skill['name']}"
        if hasattr(attacker, 'getSkillLevel'):
          skillLevel = attacker.getSkillLevel(skillId)
          skillInfo = f"{skill['name']} (Lv.{skillLevel})"
        
        safe_print(f"{attackerName} used {skillInfo}!", self.term.cyan if self.term else None)
    
    if criticalHit:
      damage *= 2
      safe_print("Critical hit!", self.term.bold_red if self.term else None)
    
    # Apply damage
    target.setHp(target.getHp() - damage)
    
    # Display results
    safe_print(f"{attackerName} attacked {targetName} for {damage} damage!", self.term.green if self.term else None)
    
    # Show HP bar if target has getMaxHp
    if hasattr(target, 'getMaxHp'):
      safe_print(f"{targetName.capitalize()} HP: {max(0, target.getHp())}/{target.getMaxHp()}", self.term.yellow if self.term else None)
    
    # Check if target died
    if target.getHp() <= 0:
      return True
    
    return False
