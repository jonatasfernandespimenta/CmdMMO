import random
from client.game.skills.fighting_abilities import fighting_abilities
from client.game.skills.elements import elements
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
        skillElement = skill.get("elementType", None)
        defenderElement = defender.getElementType()
        attackerElement = attacker.getElementType()
        
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
          baseDamage = skill["damage"]
        else:
          baseDamage = max(1, (skill["damage"] + attacker.getAttack() * 0.5) - defender.getDefense())
    
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
    
    Returns:
      bool: True if target died, False otherwise
    """
    # Check if attack misses
    if self.checkMiss(target):
      print(self.term.cyan(f"{attackerName}'s attack missed!"))
      return False
    
    # Check for critical hit
    criticalHit = self.checkCriticalHit(attacker)
    damage = self.calculateDamage(attacker, target)
    
    if criticalHit:
      damage *= 2
      print(self.term.bold_red("Critical hit!"))
    
    # Apply damage
    target.setHp(target.getHp() - damage)
    
    # Display results
    print(self.term.green(f"{attackerName} attacked {targetName} for {damage} damage!"))
    
    # Show HP bar if target has getMaxHp
    if hasattr(target, 'getMaxHp'):
      print(self.term.yellow(f"{targetName.capitalize()} HP: {max(0, target.getHp())}/{target.getMaxHp()}"))
    
    # Check if target died
    if target.getHp() <= 0:
      return True
    
    return False
