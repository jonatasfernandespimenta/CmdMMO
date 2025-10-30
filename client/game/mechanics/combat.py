import random

class CombatSystem:
  """Centralized combat system handling all battle logic"""
  
  def __init__(self, term):
    self.term = term
  
  def calculateDamage(self, attacker, defender):
    """Calculate damage dealt from attacker to defender"""
    baseDamage = max(1, attacker.getAttack() - defender.getDefense())
    return baseDamage
  
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

  def attack(self, attacker, target, attackerName=None, targetName=None):
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
