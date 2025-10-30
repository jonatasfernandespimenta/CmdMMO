def draw_rank_board(rankPosition, rankType, rankList):
  """
  Draw rank board with scroll support
  rankPosition: current scroll position (0-based)
  rankType: 'gold', 'level', or 'dungeon'
  rankList: list of player rank data [{'name': str, 'value': int}, ...]
  """
  if rankType == 'gold':
    rankTitle = 'Gold Rank Board'
  elif rankType == 'level':
    rankTitle = 'Level Rank Board'
  elif rankType == 'dungeon':
    rankTitle = 'Dungeon Rank Board'
  
  # Build board
  board = []
  board.append('  |===================================|')
  
  # Title centered
  title_length = len(rankTitle)
  total_width = 35
  left_padding = (total_width - title_length) // 2
  right_padding = total_width - title_length - left_padding
  board.append(f'  |{" "*left_padding}{rankTitle}{" "*right_padding}|')
  board.append('  |===================================|')
  
  # Max 10 entries displayed
  max_display = 10
  start_idx = rankPosition
  end_idx = min(start_idx + max_display, len(rankList))
  
  # Display rankings
  for i in range(start_idx, end_idx):
    rank_num = i + 1
    player_data = rankList[i]
    name = player_data.get('name', 'Unknown')[:15]  # Limit name length
    value = player_data.get('value', 0)
    
    # Format line: "  | #1. PlayerName........... 1000 |"
    name_display = f"#{rank_num}. {name}"
    value_str = str(value)
    # Total space inside borders: 35 chars, minus ' ' at start and end (2 chars) = 33
    content_space = 33
    dots_length = content_space - len(name_display) - len(value_str)
    dots = '.' * max(dots_length, 1)
    line = f"  | {name_display}{dots}{value_str} |"
    board.append(line)
  
  # Fill empty slots if less than 10 entries
  for _ in range(max_display - (end_idx - start_idx)):
    board.append('  |' + ' ' * 35 + '|')
  
  board.append('  |===================================|')
  
  # Scroll indicator
  if len(rankList) > max_display:
    scroll_info = f"  Showing {start_idx + 1}-{end_idx} of {len(rankList)}"
    board.append(scroll_info)
  
  return '\n'.join(board)
