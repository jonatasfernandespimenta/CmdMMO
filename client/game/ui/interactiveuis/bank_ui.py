from game.arts.bank import banker
from engine.ui.interaction_ui import InteractionUI
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal


class BankUI:
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.player = player
    self.term = term
    self.current_account = None  # Stores current session account data
    self.current_password = None  # Stores password for current session
    
    self.ui = InteractionUI(player, term, {
      'art': banker,
      'message': 'Welcome to the Bank of CmdMMO! How can we help you today?',
      'show_gold': True,
      'options': [
        {
          'key': '1',
          'label': 'Deposit Gold',
          'action': self.deposit_money
        },
        {
          'key': '2',
          'label': 'Withdraw Gold',
          'action': self.withdraw_money
        },
        {
          'key': '3',
          'label': 'Deposit Item',
          'action': self.deposit_items
        },
        {
          'key': '4',
          'label': 'Withdraw Item',
          'action': self.withdraw_items
        },
        {
          'key': '5',
          'label': 'Check Balance',
          'action': self.check_balance
        }
      ]
    })

  def _get_text_input(self, prompt: str) -> str:
    """Get text input from user"""
    print(self.term.move_y(self.term.height - 2) + self.term.clear_eol + self.term.center(self.term.white(prompt)).rstrip())
    
    input_text = ""
    while True:
      key = self.term.inkey()
      
      if key.name == 'KEY_ENTER':
        return input_text
      elif key.name == 'KEY_BACKSPACE':
        input_text = input_text[:-1]
        print(self.term.move_y(self.term.height - 2) + self.term.clear_eol + self.term.center(self.term.white(f"{prompt}{input_text}")).rstrip())
      elif key.name == 'KEY_ESCAPE':
        return None
      elif key.isprintable():
        input_text += key
        print(self.term.move_y(self.term.height - 2) + self.term.clear_eol + self.term.center(self.term.white(f"{prompt}{input_text}")).rstrip())

  def _get_number_input(self, prompt: str) -> int:
    """Get numeric input from user"""
    input_text = ""
    print(self.term.move_y(self.term.height - 2) + self.term.clear_eol + self.term.center(self.term.white(prompt)).rstrip())
    
    while True:
      key = self.term.inkey()
      
      if key.name == 'KEY_ENTER':
        try:
          return int(input_text) if input_text else None
        except ValueError:
          return None
      elif key.name == 'KEY_BACKSPACE':
        input_text = input_text[:-1]
        print(self.term.move_y(self.term.height - 2) + self.term.clear_eol + self.term.center(self.term.white(f"{prompt}{input_text}")).rstrip())
      elif key.name == 'KEY_ESCAPE':
        return None
      elif key.isdigit():
        input_text += key
        print(self.term.move_y(self.term.height - 2) + self.term.clear_eol + self.term.center(self.term.white(f"{prompt}{input_text}")).rstrip())

  def _authenticate(self, message="Enter your account ID: "):
    """Authenticate user and return account data"""
    if not self.player.api_client:
      self.ui.showMessage("Bank services unavailable (no API connection)", 'red')
      return None
    
    self.ui.message = message
    self.ui.draw()
    
    account_id = self._get_text_input("Account ID: ")
    if not account_id:
      self.ui.message = "Operation cancelled."
      return None
    
    password = self._get_text_input("Password: ")
    if not password:
      self.ui.message = "Operation cancelled."
      return None
    
    # Verify account
    account = self.player.api_client.verifyBankAccount(account_id, password)
    
    if account and account.get('valid'):
      self.current_account = account
      self.current_password = password
      return account
    else:
      self.ui.showMessage("Invalid account ID or password!", 'red')
      return None

  def deposit_money(self):
    """Deposit gold into bank account"""
    if not self.player.api_client:
      self.ui.showMessage("Bank services unavailable", 'red')
      return
    
    # Check if user has account or wants to create one
    self.ui.message = "Do you have an existing account?\n1 - Yes\n2 - No, create new account"
    self.ui.draw()
    
    choice = self._get_number_input("> ")
    
    if choice == 2:
      self._create_new_account_with_deposit()
      return
    elif choice != 1:
      self.ui.message = "Invalid choice."
      return
    
    # Authenticate
    account = self._authenticate("Login to deposit gold")
    if not account:
      return
    
    # Get deposit amount
    self.ui.message = f"Current Balance: {account.get('gold', 0)} gold\nYour Wallet: {self.player.getGold()} gold"
    self.ui.draw()
    
    amount = self._get_number_input("Amount to deposit: ")
    
    if not amount or amount <= 0:
      self.ui.message = "Invalid amount."
      return
    
    if self.player.getGold() < amount:
      self.ui.showMessage("Insufficient gold in wallet!", 'red')
      return
    
    # Deposit via API
    result = self.player.api_client.depositGold(account['accountId'], self.current_password, amount)
    
    if result:
      self.player.removeGold(amount)
      self.ui.showMessage(f"Successfully deposited {amount} gold! New balance: {result['gold']}", 'green')
    else:
      self.ui.showMessage("Failed to deposit gold.", 'red')

  def _create_new_account_with_deposit(self):
    """Create new bank account with initial deposit"""
    self.ui.message = "Create New Bank Account"
    self.ui.draw()
    
    account_id = self._get_text_input("Choose an Account ID: ")
    if not account_id:
      self.ui.message = "Account creation cancelled."
      return
    
    password = self._get_text_input("Choose a Password: ")
    if not password:
      self.ui.message = "Account creation cancelled."
      return
    
    password_confirm = self._get_text_input("Confirm Password: ")
    if password != password_confirm:
      self.ui.showMessage("Passwords do not match!", 'red')
      return
    
    # Get initial deposit
    initial_gold = self._get_number_input("Initial deposit amount: ")
    
    if initial_gold and initial_gold > 0:
      if self.player.getGold() < initial_gold:
        self.ui.showMessage("Insufficient gold!", 'red')
        return
    else:
      initial_gold = 0
    
    # Create account via API
    result = self.player.api_client.createBankAccount(account_id, password, initial_gold)
    
    if result:
      if initial_gold > 0:
        self.player.removeGold(initial_gold)
      self.ui.showMessage(f"Account created successfully! Account ID: {account_id}", 'green')
    else:
      self.ui.showMessage("Failed to create account. ID may already exist.", 'red')

  def withdraw_money(self):
    """Withdraw gold from bank account"""
    if not self.player.api_client:
      self.ui.showMessage("Bank services unavailable", 'red')
      return
    
    # Authenticate
    account = self._authenticate("Login to withdraw gold")
    if not account:
      return
    
    # Get withdrawal amount
    self.ui.message = f"Current Balance: {account.get('gold', 0)} gold\nYour Wallet: {self.player.getGold()} gold"
    self.ui.draw()
    
    amount = self._get_number_input("Amount to withdraw: ")
    
    if not amount or amount <= 0:
      self.ui.message = "Invalid amount."
      return
    
    # Withdraw via API
    result = self.player.api_client.withdrawGold(account['accountId'], self.current_password, amount)
    
    if result:
      self.player.addGold(amount)
      self.ui.showMessage(f"Successfully withdrew {amount} gold! New balance: {result['gold']}", 'green')
    else:
      self.ui.showMessage("Failed to withdraw. Check your balance.", 'red')

  def deposit_items(self):
    """Deposit item into bank account"""
    if not self.player.api_client:
      self.ui.showMessage("Bank services unavailable", 'red')
      return
    
    # Check if player has items
    inventory = self.player.getInventory()
    if not inventory:
      self.ui.showMessage("Your inventory is empty!", 'red')
      return
    
    # Authenticate
    account = self._authenticate("Login to deposit item")
    if not account:
      return
    
    # Show inventory
    self.ui.message = "Your Inventory:\n" + "\n".join([f"{i+1}. {item.get('name', 'Item')} (ID: {item.get('id', 'N/A')})" for i, item in enumerate(inventory)])
    self.ui.draw()
    
    item_index = self._get_number_input("Select item number to deposit: ")
    
    if not item_index or item_index < 1 or item_index > len(inventory):
      self.ui.message = "Invalid item selection."
      return
    
    selected_item = inventory[item_index - 1]
    item_id = selected_item.get('id')
    
    if not item_id:
      self.ui.showMessage("Cannot deposit this item.", 'red')
      return
    
    # Deposit via API
    result = self.player.api_client.depositItem(account['accountId'], self.current_password, item_id)
    
    if result:
      self.player.removeFromInventory(selected_item)
      self.ui.showMessage(f"Successfully deposited {selected_item.get('name', 'item')}!", 'green')
    else:
      self.ui.showMessage("Failed to deposit item.", 'red')

  def withdraw_items(self):
    """Withdraw item from bank account"""
    if not self.player.api_client:
      self.ui.showMessage("Bank services unavailable", 'red')
      return
    
    # Authenticate
    account = self._authenticate("Login to withdraw item")
    if not account:
      return
    
    # Parse items
    try:
      items = json.loads(account.get('items', '[]'))
    except:
      items = []
    
    if not items:
      self.ui.showMessage("No items in bank!", 'red')
      return
    
    # Show banked items
    self.ui.message = "Banked Items:\n" + "\n".join([f"{i+1}. Item ID: {item}" for i, item in enumerate(items)])
    self.ui.draw()
    
    item_index = self._get_number_input("Select item number to withdraw: ")
    
    if not item_index or item_index < 1 or item_index > len(items):
      self.ui.message = "Invalid item selection."
      return
    
    item_id = items[item_index - 1]
    
    # Withdraw via API
    result = self.player.api_client.withdrawItem(account['accountId'], self.current_password, item_id)
    
    if result:
      # Add item back to inventory (simplified - just add the ID as a dict)
      self.player.addToInventory({'id': item_id, 'name': f'Item {item_id}'})
      self.ui.showMessage(f"Successfully withdrew item {item_id}!", 'green')
    else:
      self.ui.showMessage("Failed to withdraw item.", 'red')

  def check_balance(self):
    """Check account balance and info"""
    if not self.player.api_client:
      self.ui.showMessage("Bank services unavailable", 'red')
      return
    
    # Authenticate
    account = self._authenticate("Login to check balance")
    if not account:
      return
    
    # Parse items
    try:
      items = json.loads(account.get('items', '[]'))
    except:
      items = []
    
    # Display account info
    info = f"""
    Account ID: {account.get('accountId', 'N/A')}
    Gold Balance: {account.get('gold', 0)}
    Items Stored: {len(items)}
    """
    
    self.ui.showMessage(info, 'green')
  
  def open(self):
    """Open the bank UI"""
    self.ui.open()
