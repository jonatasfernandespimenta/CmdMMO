class PartyUI:
  """Party management UI with tabs"""
  
  TAB_INVITE = 0
  TAB_PENDING = 1
  TAB_LEAVE = 2
  
  def __init__(self, player, party, term):
    self.player = player
    self.party = party
    self.term = term
    self.current_tab = self.TAB_INVITE
    self.search_query = ""
    self.selected_index = 0
    self.is_open = False
  
  def open(self):
    """Open party UI modal"""
    self.is_open = True
    self.search_query = ""
    self.selected_index = 0
    
    # Determine initial tab based on party state
    if self.party.is_in_party():
      self.current_tab = self.TAB_LEAVE
    else:
      self.current_tab = self.TAB_INVITE
    
    # Request fresh data
    self.party.request_online_players()
    self.party.request_pending_invites()
    
    self._show()
  
  def _show(self):
    """Main UI render loop"""
    while self.is_open:
      print(self.term.home + self.term.clear)
      
      # Draw modal box
      self._draw_modal_header()
      self._draw_tabs()
      
      # Draw content based on current tab
      if self.current_tab == self.TAB_INVITE:
        self._draw_invite_tab()
      elif self.current_tab == self.TAB_PENDING:
        self._draw_pending_tab()
      elif self.current_tab == self.TAB_LEAVE:
        self._draw_leave_tab()
      
      self._draw_modal_footer()
      
      # Handle input
      key = self.term.inkey()
      self._handle_input(key)
  
  def _draw_modal_header(self):
    """Draw modal header"""
    width = 60
    height = 25
    start_y = (self.term.height - height) // 2
    start_x = (self.term.width - width) // 2
    
    print(self.term.move_y(start_y) + self.term.move_x(start_x) + self.term.bold_cyan('┌' + '─' * (width - 2) + '┐'))
    
    title = 'PARTY SYSTEM'
    padding = (width - 2 - len(title)) // 2
    title_line = ' ' * padding + self.term.bold_white(title) + ' ' * (width - 2 - padding - len(title))
    print(self.term.move_y(start_y + 1) + self.term.move_x(start_x) + self.term.bold_cyan('│') + title_line + self.term.bold_cyan('│'))
    
    print(self.term.move_y(start_y + 2) + self.term.move_x(start_x) + self.term.bold_cyan('├' + '─' * (width - 2) + '┤'))
  
  def _draw_tabs(self):
    """Draw tab selector"""
    width = 60
    height = 25
    start_y = (self.term.height - height) // 2
    start_x = (self.term.width - width) // 2
    
    # Tab names
    tabs = []
    
    if not self.party.is_in_party():
      tabs = ['[1] Invite Players', '[2] Pending Invites']
    else:
      tabs = ['[1] Invite Players', '[2] Pending Invites', '[3] Leave Party']
    
    # Draw tabs
    tab_line = ' '
    for i, tab in enumerate(tabs):
      if i == self.current_tab:
        tab_line += self.term.black_on_white(tab) + ' '
      else:
        tab_line += self.term.white(tab) + ' '
    
    # Pad to full width
    tab_line = tab_line.ljust(width - 2)
    
    print(self.term.move_y(start_y + 3) + self.term.move_x(start_x) + self.term.bold_cyan('│') + tab_line + self.term.bold_cyan('│'))
    print(self.term.move_y(start_y + 4) + self.term.move_x(start_x) + self.term.bold_cyan('├' + '─' * (width - 2) + '┤'))
  
  def _draw_invite_tab(self):
    """Draw invite players tab"""
    width = 60
    height = 25
    start_y = (self.term.height - height) // 2
    start_x = (self.term.width - width) // 2
    current_y = start_y + 5
    
    # Search field
    search_text = f' Search: {self.search_query}_'
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + 
          self.term.white(search_text.ljust(width - 2)) + self.term.bold_cyan('│'))
    current_y += 1
    
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + ' ' * (width - 2) + self.term.bold_cyan('│'))
    current_y += 1
    
    # Get filtered online players
    online = self.party.get_online_players()
    filtered = [p for p in online if self.search_query.lower() in p['playerId'].lower()]
    
    if len(filtered) == 0:
      msg = 'No players found'
      padding = (width - 2 - len(msg)) // 2
      msg_line = ' ' * padding + self.term.yellow(msg) + ' ' * (width - 2 - padding - len(msg))
      print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + msg_line + self.term.bold_cyan('│'))
      current_y += 1
    else:
      # List players
      for i, player in enumerate(filtered[:15]):  # Max 15 players
        if i == self.selected_index:
          line = self.term.black_on_white(f' > {player["playerId"]}'.ljust(width - 4))
        else:
          line = self.term.white(f'   {player["playerId"]}'.ljust(width - 4))
        
        print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + ' ' + line + ' ' + self.term.bold_cyan('│'))
        current_y += 1
    
    # Fill remaining space
    while current_y < start_y + height - 3:
      print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + ' ' * (width - 2) + self.term.bold_cyan('│'))
      current_y += 1
  
  def _draw_pending_tab(self):
    """Draw pending invites tab"""
    width = 60
    height = 25
    start_y = (self.term.height - height) // 2
    start_x = (self.term.width - width) // 2
    current_y = start_y + 5
    
    # Get pending invites
    pending = self.party.get_pending_invites()
    
    if len(pending) == 0:
      msg = 'No pending invites'
      padding = (width - 2 - len(msg)) // 2
      msg_line = ' ' * padding + self.term.yellow(msg) + ' ' * (width - 2 - padding - len(msg))
      print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + msg_line + self.term.bold_cyan('│'))
      current_y += 1
    else:
      # List invites
      for i, invite in enumerate(pending[:15]):
        leader = invite.get('leader', 'Unknown')
        member_count = invite.get('memberCount', 0)
        
        if i == self.selected_index:
          line = self.term.black_on_white(f' > From: {leader} ({member_count} members)'.ljust(width - 4))
        else:
          line = self.term.white(f'   From: {leader} ({member_count} members)'.ljust(width - 4))
        
        print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + ' ' + line + ' ' + self.term.bold_cyan('│'))
        current_y += 1
    
    # Instructions
    current_y += 1
    instructions = '[ENTER] Accept | [D] Decline'
    padding = (width - 2 - len(instructions)) // 2
    instr_line = ' ' * padding + self.term.green(instructions) + ' ' * (width - 2 - padding - len(instructions))
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + instr_line + self.term.bold_cyan('│'))
    current_y += 1
    
    # Fill remaining space
    while current_y < start_y + height - 3:
      print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + ' ' * (width - 2) + self.term.bold_cyan('│'))
      current_y += 1
  
  def _draw_leave_tab(self):
    """Draw leave party tab"""
    width = 60
    height = 25
    start_y = (self.term.height - height) // 2
    start_x = (self.term.width - width) // 2
    current_y = start_y + 5
    
    # Show party info
    members = self.party.get_members()
    leader = self.party.leader
    
    title = 'Current Party'
    padding = (width - 2 - len(title)) // 2
    title_line = ' ' * padding + self.term.bold_white(title) + ' ' * (width - 2 - padding - len(title))
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + title_line + self.term.bold_cyan('│'))
    current_y += 2
    
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + 
          self.term.white(f' Leader: {leader}').ljust(width - 2) + self.term.bold_cyan('│'))
    current_y += 1
    
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + 
          self.term.white(f' Members: {len(members)}').ljust(width - 2) + self.term.bold_cyan('│'))
    current_y += 2
    
    # List members
    for member in members[:10]:
      is_leader = '(Leader)' if member == leader else ''
      is_you = '(You)' if member == self.player.getName() else ''
      
      print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + 
            self.term.white(f'   • {member} {is_leader} {is_you}').ljust(width - 2) + self.term.bold_cyan('│'))
      current_y += 1
    
    current_y += 1
    
    # Leave button
    leave_text = '[ENTER] Leave Party'
    padding = (width - 2 - len(leave_text)) // 2
    leave_line = ' ' * padding + self.term.red(leave_text) + ' ' * (width - 2 - padding - len(leave_text))
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + leave_line + self.term.bold_cyan('│'))
    current_y += 1
    
    # Fill remaining space
    while current_y < start_y + height - 3:
      print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + ' ' * (width - 2) + self.term.bold_cyan('│'))
      current_y += 1
  
  def _draw_modal_footer(self):
    """Draw modal footer with instructions"""
    width = 60
    height = 25
    start_y = (self.term.height - height) // 2
    start_x = (self.term.width - width) // 2
    current_y = start_y + height - 3
    
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('├' + '─' * (width - 2) + '┤'))
    current_y += 1
    
    if self.current_tab == self.TAB_INVITE:
      instructions = '[TAB] Tab | [↑↓] Nav | [ENTER] Invite | [ESC] Close'
    elif self.current_tab == self.TAB_PENDING:
      instructions = '[TAB] Tab | [↑↓] Nav | [ENTER] Accept | [D] Decline | [ESC] Close'
    else:
      instructions = '[TAB] Tab | [ENTER] Leave Party | [ESC] Close'
    
    # Center the instructions
    padding = (width - 2 - len(instructions)) // 2
    instr_line = ' ' * padding + self.term.yellow(instructions) + ' ' * (width - 2 - padding - len(instructions))
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('│') + instr_line + self.term.bold_cyan('│'))
    current_y += 1
    
    print(self.term.move_y(current_y) + self.term.move_x(start_x) + self.term.bold_cyan('└' + '─' * (width - 2) + '┘'))
  
  def _handle_input(self, key):
    """Handle keyboard input"""
    if key.name == 'KEY_ESCAPE':
      self.is_open = False
    
    elif key.name == 'KEY_TAB' or key == '\t':
      # Switch tabs
      if not self.party.is_in_party():
        self.current_tab = (self.current_tab + 1) % 2  # Only 2 tabs
      else:
        self.current_tab = (self.current_tab + 1) % 3  # 3 tabs
      self.selected_index = 0
      self.search_query = ""
    
    elif key == '1':
      self.current_tab = self.TAB_INVITE
      self.selected_index = 0
      self.search_query = ""
    
    elif key == '2':
      self.current_tab = self.TAB_PENDING
      self.selected_index = 0
      self.party.request_pending_invites()
    
    elif key == '3' and self.party.is_in_party():
      self.current_tab = self.TAB_LEAVE
      self.selected_index = 0
    
    elif self.current_tab == self.TAB_INVITE:
      self._handle_invite_input(key)
    
    elif self.current_tab == self.TAB_PENDING:
      self._handle_pending_input(key)
    
    elif self.current_tab == self.TAB_LEAVE:
      self._handle_leave_input(key)
  
  def _handle_invite_input(self, key):
    """Handle input in invite tab"""
    if key.name == 'KEY_UP':
      filtered = [p for p in self.party.get_online_players() if self.search_query.lower() in p['playerId'].lower()]
      self.selected_index = max(0, self.selected_index - 1)
    
    elif key.name == 'KEY_DOWN':
      filtered = [p for p in self.party.get_online_players() if self.search_query.lower() in p['playerId'].lower()]
      self.selected_index = min(len(filtered) - 1, self.selected_index + 1)
    
    elif key.name == 'KEY_ENTER':
      # Send invite
      filtered = [p for p in self.party.get_online_players() if self.search_query.lower() in p['playerId'].lower()]
      if 0 <= self.selected_index < len(filtered):
        target_player = filtered[self.selected_index]['playerId']
        self.party.invite_player(target_player)
        # Show confirmation (will be visible in notification)
        self.player.setNotification(f'Invite sent to {target_player}')
    
    elif key.name == 'KEY_BACKSPACE' or key.name == 'KEY_DELETE':
      self.search_query = self.search_query[:-1]
      self.selected_index = 0
    
    elif key and len(key) == 1 and key.isprintable():
      self.search_query += key
      self.selected_index = 0
  
  def _handle_pending_input(self, key):
    """Handle input in pending invites tab"""
    if key.name == 'KEY_UP':
      self.selected_index = max(0, self.selected_index - 1)
    
    elif key.name == 'KEY_DOWN':
      pending = self.party.get_pending_invites()
      self.selected_index = min(len(pending) - 1, self.selected_index + 1)
    
    elif key.name == 'KEY_ENTER':
      # Accept invite
      pending = self.party.get_pending_invites()
      if 0 <= self.selected_index < len(pending):
        invite = pending[self.selected_index]
        self.party.accept_invite(invite['partyId'])
        self.player.setNotification(f'Joined party led by {invite["leader"]}')
        self.is_open = False
    
    elif key.lower() == 'd':
      # Decline invite
      pending = self.party.get_pending_invites()
      if 0 <= self.selected_index < len(pending):
        invite = pending[self.selected_index]
        self.party.decline_invite(invite['partyId'])
        self.player.setNotification(f'Declined invite from {invite["leader"]}')
  
  def _handle_leave_input(self, key):
    """Handle input in leave party tab"""
    if key.name == 'KEY_ENTER':
      # Leave party
      self.party.leave_party()
      self.player.setNotification('Left the party')
      self.is_open = False
