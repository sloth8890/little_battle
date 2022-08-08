import os, sys
import copy

# Please implement this function according to Section "Read Configuration File"
def load_config_file(filepath):
  # It should return width, height, waters, woods, foods, golds based on the file
  # Complete the test driver of this function in file_loading_test.py
  width, height = 0, 0
  waters, woods, foods, golds = [], [], [], [] # list of position tuples

  # path check
  if not os.path.exists(filepath):
    raise FileNotFoundError
    
  def _tuple_cord(resource_ls):
    ls = []
    for elem in range(len(resource_ls)):
      if not elem % 2 == 0:
        continue
      if elem + 1 == len(resource_ls):
        break
      ls.append((resource_ls[elem],resource_ls[elem+1]))
    return ls  
  
  with open(filepath) as f:
    context = []
    while True:
      data = f.readline()
      if not data:
        break
      data =data.replace('\n','')
      context.append(data)
      
  #! test format err
  valid_test = True
  if len(context) != 5:
    raise SyntaxError("Invalid Configuration File: format error!")
  
  if context[0][:7] != "Frame: ":
    valid_test = False
  elif context[1][:7] != "Water: ":
    valid_test = False
  elif context[2][:6] != "Wood: ":
    valid_test = False
  elif context[3][:6] != "Food: ":
    valid_test = False
  elif context[4][:6] != "Gold: ":
    valid_test = False
  
  if valid_test == False:
    raise SyntaxError("Invalid Configuration File: format error!")
  
  #! test frame format err
  #? what if Frame: 5x5 fwjoiqw
  if not context[0][8] == "x" or not context[0][7].isdigit() or not context[0][9].isdigit():
    raise SyntaxError("Invalid Configuration File: frame should be in format widthxheight!")

  #! test frame out of range
  if not 5<=int(context[0][7])<=7 or not 5<=int(context[0][9])<=7:
    raise ArithmeticError ("Invalid Configuration File: width and height should range from 5 to 7!")

  #? using loop or check if rest 
  width = int(context[0][7])
  height = int(context[0][9])

  for elem in range(1,5):
    resource_name = context[elem].split(':')[0]
    resource_cords = context[elem].split(':')[1]
    
    #! test non integer:
    if not resource_cords.replace(" ","").isdigit():
      raise ValueError("Invalid Configuration File: {} contains non integer characters!".format(resource_name))
    
    #! test odd_length:
    splited_resource_cords = (resource_cords.lstrip()).split(' ')
    if not len(splited_resource_cords) % 2 == 0:
      raise SyntaxError("Invalid Configuration File: {} has an odd number of elements!".format(resource_name))

    #! test out of map
    valid_test = True
    for cord in range(len(splited_resource_cords)):
      if cord%2 == 0:
        if not int(splited_resource_cords[cord]) < width:
          valid_test = False
      else:
        if not int(splited_resource_cords[cord]) < height:
          valid_test = False
      if valid_test == False:
        raise ArithmeticError ("Invalid Configuration File: {} contains a position that is out of map.".format(resource_name))    

  with open(filepath) as f:
    context = []
    while True:
      data = f.readline()
      if not data:
        break
      
      #! only when the file format is correct (?)
      field_name = data.split(':')[0]
      file_value = (data.split(':')[1]).lstrip()
      if field_name == 'Frame':
        width = int(file_value.split('x')[0])
        height = int((file_value.split('x')[1])[0:-1])
      elif field_name in ['Water', 'Wood', 'Food', 'Gold']:
        data = (file_value.replace('\n', '').split(' '))
      
      if field_name == 'Water':
        waters_ls = list(map(int, data))
        waters = _tuple_cord(waters_ls)
      elif field_name == 'Wood':
        woods_ls = list(map(int, data))
        woods = _tuple_cord(woods_ls)
      elif field_name == 'Food':
        foods_ls = list(map(int, data)) 
        foods = _tuple_cord(foods_ls)
      elif field_name == 'Gold':
        golds_ls = list(map(int, data)) 
        golds = _tuple_cord(golds_ls)
  
  #! test occupy home or next to home    
  #TODO find if its home base or position
  coordinate_collection = (tuple(waters),tuple(woods),tuple(foods),tuple(golds))  
  restricted_cords_homebase = ((1,1),(width-2,height-2))
  restricted_cords_around_homebase = ((0,1), (1,0),(2,1),(1,2),(width-3,height-2),(width-2,height-3),(width-1,height-2),(width-2,height-1))
  total_cords = []
  for resource in range(len(coordinate_collection)):
    #TODO repeat this for specific result 
    for cords in restricted_cords_homebase:
      if cords in coordinate_collection[resource]:
        raise ValueError ("Invalid Configuration File: The positions of home bases are occupied!")
      else:
        for cords in restricted_cords_around_homebase:
          if cords in coordinate_collection[resource]:
            raise ValueError ("Invalid Configuration File: The positions of the positions next to the home bases are occupied!")
          else:
            continue
        continue
    for cords in range(len(coordinate_collection[resource])):
      total_cords.append(coordinate_collection[resource][cords])
  
  total_cords = tuple(total_cords)
  # og_len = len(total_cords)
  # new_len = len(set(total_cords))
  
  for cords in range(len(total_cords)):
    cnt = total_cords.count(total_cords[cords])
    if cnt > 1:
      duplicated_cord = total_cords[cords]
      raise SyntaxError ("Invalid Configuration File: Duplicate position {}!".format(duplicated_cord))
      
  return width, height, waters, woods, foods, golds

 
def util_ls_price():
  print("Recruit Prices:")
  print("  Spearman (S) - 1W, 1F")
  print("  Archer (A) - 1W, 1G")
  print("  Knight (K) - 1F, 1G")
  print("  Scout (T) - 1W, 1F, 1G")

def util_print_armies_to_move(player):
  next_turn_flag = True
  for army_key in player.army_move.keys():
    for flag in player.army_move[army_key]:
      if flag:
        next_turn_flag = False

  if next_turn_flag:
    print('No Army to Move: next turn.')
    print('')
    return False

  print('Armies to Move:')
  #self.army = {'Spearman': [], 'Scout': [], 'Knight': [], 'Archer': []} 

  for army_key in player.army_move.keys():
    army_list = []
    for idx in range(len(player.army_move[army_key])): # bool type list
      if player.army_move[army_key][idx]: # true
        army_list.append(idx)

    if len(army_list) == 1:
      print(f'  {army_key}: ', end='')
      print(player.army[army_key][army_list[0]])
    elif len(army_list) > 1:
      print(f'  {army_key}: ', end='')
      for i in range(0, len(army_list)-1):
        print(player.army[army_key][army_list[i]], end='')
        print(', ', end='') 
      print(player.army[army_key][army_list[-1]])

  print('') # new line
  return True
###############################################
# Game - repeating features
###############################################
class Game:
  def __init__(self, width, height, waters, woods, foods, golds):
    self.width = width
    self.height = height
    self.waters = waters
    self.woods = woods
    self.foods = foods
    self.golds = golds

    
    self.year = 617

    self.player1 = Player((1,1), 1)
    self.player2 = Player((width-2, height-2), 2)

    
    self.count = {'Spearman': {}, 'Archer': {}, 'Knight': {}, 'Scout': {} }
    self.count['Spearman']['Spearman'] = True
    self.count['Spearman']['Archer']   = True
    self.count['Spearman']['Knight']   = False
    self.count['Spearman']['Scout']    = False

    self.count['Archer']['Spearman'] = False
    self.count['Archer']['Archer']   = True
    self.count['Archer']['Knight']   = True
    self.count['Archer']['Scout']    = False

    self.count['Knight']['Spearman'] = True
    self.count['Knight']['Archer']   = False
    self.count['Knight']['Knight']   = True
    self.count['Knight']['Scout']    = False

    self.count['Scout']['Spearman'] = True
    self.count['Scout']['Archer']   = True
    self.count['Scout']['Knight']   = True
    self.count['Scout']['Scout']    = True

  def ask_winners_name_and_quit_game(self, src_loc, dst_loc, army_type):
    print('')
    print(f"You have moved {army_type} from {src_loc} to {dst_loc}.")
    print(f"The army Scout captured the enemy’s capital.")
    print('')
    print('What’s your name, commander?')
    user_name = input()
    print('')
    print(f"***Congratulation! Emperor {user_name} unified the country in {self.get_year()}.***")
    exit()

  def get_year(self):
    return self.year

  def army_count(self, my_army_type, enemy_army_type):
    return (self.count[my_army_type][enemy_army_type], self.count[enemy_army_type][my_army_type])


  def visualize_map(self, occupied_check=False):
    if not occupied_check:
      print("Please check the battlefield, commander.")
    # X part
    if not occupied_check:
      print("  X",end="")
    for w in range(width):
      if w == width-1:
        if not occupied_check:
          print("0{}X".format(w))
        break
      if not occupied_check:
        print("0{}".format(w),end=" ")
    # Y part
    if not occupied_check:
      print(" Y+{}+".format("-"*(width*3-1)))
    
    resource_char = {'water': '~~', 'wood': 'WW', 'food': 'FF', 'gold': 'GG', 'home1': 'H1', 'home2': 'H2'}
    resource_char['P1_Spearman'] = 'S1'
    resource_char['P1_Archer']   = 'A1'
    resource_char['P1_Knight']   = 'K1'
    resource_char['P1_Scout']    = 'T1'
    resource_char['P2_Spearman'] = 'S2'
    resource_char['P2_Archer']   = 'A2'
    resource_char['P2_Knight']   = 'K2'
    resource_char['P2_Scout']    = 'T2'
    
    resource = {}
    resource['water'] = self.waters
    resource['wood'] = self.woods
    resource['food'] = self.foods
    resource['gold'] = self.golds

    resource['P1_Spearman'] = self.player1.army['Spearman']
    resource['P1_Archer']   = self.player1.army['Archer']
    resource['P1_Knight']   = self.player1.army['Knight']
    resource['P1_Scout']    = self.player1.army['Scout']
    resource['P2_Spearman'] = self.player2.army['Spearman']
    resource['P2_Archer']   = self.player2.army['Archer']
    resource['P2_Knight']   = self.player2.army['Knight']
    resource['P2_Scout']    = self.player2.army['Scout']
    resource['home1'] = self.player1.home_base
    resource['home2'] = self.player2.home_base
        
    def _is_resource(h, w, resource_list):
      for (x, y) in resource_list:
        if h == y and w == x:
          return True
      return False   

    for h in range(height):
      if not occupied_check:
        print('0{}|'.format(h), end='') # 00 01 02 03 04 ..
      for w in range(width): # ok
        empty_flag = True 

        for key in resource.keys():
          if _is_resource(h, w, resource[key]):
            if not occupied_check:
              print(resource_char[key] + '|', end='')    
            empty_flag = False
            break
        if empty_flag:
          if occupied_check:
            return True
          if not occupied_check: 
            print('  |', end='')
      if not occupied_check:
        print('')
    if not occupied_check:
      print(" Y+{}+".format("-"*(width*3-1)))
    if occupied_check:
      return False

  def walk5_printYear(self):
    print('-Year {}-'.format(self.year))
    print('')

  def walk5b_print(self, player):
    print("+++Player {}'s Stage: Recruit Armies+++".format(player))
    print('')

  def isValidLocation(self, player, location): # location: tuple
    x = player.home_base[0][0]
    y = player.home_base[0][1]

    # is location next to home base?
    is_next_home_base = False
    for loc in [(x, y-1),(x, y+1), (x-1, y), (x+1, y)]:
      if location[0] == loc[0] and location[1] == loc[1]:
        is_next_home_base = True
    if not is_next_home_base:
      return False  # go to 5-i

    # vacant?
    for army in self.player1.army.keys():
      for army_loc in self.player1.army[army]: # tuple ()
        if location[0] == army_loc[0] and location[1] == army_loc[1]:
          return False 
    for army in self.player2.army.keys():
      for army_loc in self.player2.army[army]: # tuple ()
        if location[0] == army_loc[0] and location[1] == army_loc[1]:
          return False
    return True
      

  def walk5di_recruit_cord_check(self, player, army_type):
    while True:
      print("")  
      print("You want to recruit a {}. Enter two integers as format ‘x y’ to place your army.".format(army_type))
      user_input = input()
      
      if user_input == "DIS":
        self.visualize_map()
      elif user_input == "PRIS":
        util_ls_price()
      elif user_input == "QUIT":
        exit()
      elif not len(user_input) ==  3 or not user_input[0].isdigit() or not user_input[2].isdigit():
        #! 5-d-ii
        print("Sorry, invalid input. Try again.")
      else:
        
        x, y = map(int, user_input.split())
        location = (x,y)
          
        if self.isValidLocation(player, location):
          player.locate_army(army_type, location)
          player.apply_price(army_type)
          print('')
          print(f'You has recruited a {army_type}.')
          print('')
          break # or return None
        else:
          print('You must place your newly recruited unit in an unoccupied position next to your home base. Try again.')
        #! check space
      

  def walk5d_recruit_input_check(self, player):
    while True:
      if not player.money_check(): # not enough resource to recruit
        print("No resources to recruit any armies.")
        print("")
        return True
      if not self.visualize_map(occupied_check=True): # no more place to locate armies
        print('No place to recruit new armies.')
        print("")
        return True

      print("")
      print("Which type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter ‘NO’ to end this stage.")
      user_input = input()
      
      if user_input == "S" or user_input =="A" or user_input =="K" or user_input =="T":
        # print full name
        if user_input == "S":
          army_type = "Spearman"
        elif user_input == "A":
          army_type = "Archer"
        elif user_input == "K":
          army_type = "Knight"  
        elif user_input == "T":
          army_type = "Scout"

        # buy army 
        if player.buy_army(army_type):
          # locate army
          self.walk5di_recruit_cord_check(player, army_type)
          player.print_asset()
          continue
        else:
          print('Insufficient resources. Try again.')
      elif user_input == "NO":
        print('')
        return True
      elif user_input == "DIS":
        self.visualize_map()
      elif user_input == "PRIS":
        util_ls_price()
      elif user_input == "QUIT":
        exit()
      else:
        #! 5d-ii -> go to 5-d
        print("Sorry, invalid input. Try again.")
        return False


  def walk5f_move_input_check(self, player):
    print("")
    if player.no_army_check(): # true -> no mary
      print("No Army to Move: next turn.")
      print("")
      return True
    else:
      return False

  # scount 2-move 
  def isValidLocationScout(self, current_army_idx, src_loc, dst_loc, player, enemy_player):
    def _get_field_info(scout_loc, player, enemy_player):
      for army_type in enemy_player.army.keys(): # found enemy
        for idx in range(len(enemy_player.army[army_type])):
          if scout_loc[0] == enemy_player.army[army_type][idx][0] and scout_loc[1] == enemy_player.army[army_type][idx][1]:
            return army_type, idx

      for army_type in player.army.keys(): # found my own army
        for idx in range(len(player.army[army_type])):
          if scout_loc[0] == player.army[army_type][idx][0] and scout_loc[1] == player.army[army_type][idx][1]:
            return 'my_army', idx


      for idx, wood in enumerate(self.woods):# found resource
        if wood[0] == scout_loc[0] and wood[1] == scout_loc[1]:
          return 'Wood', idx
      for idx, gold in enumerate(self.golds):
        if gold[0] == scout_loc[0] and gold[1] == scout_loc[1]:
          return 'Gold', idx
      for idx, food in enumerate(self.foods):
        if food[0] == scout_loc[0] and food[1] == scout_loc[1]:
          return 'Food', idx
      for idx, water in enumerate(self.waters):
        if water[0] == scout_loc[0] and water[1] == scout_loc[1]:
          return 'Water', idx
     

      if scout_loc[0] == enemy_player.home_base[0][0] and scout_loc[1] == enemy_player.home_base[0][0]:
        return 'HomeBase', -1

      return 'emtpy', -1
      
    first_loc = ( (src_loc[0]+dst_loc[0])//2, (src_loc[1]+dst_loc[1])//2 )
    second_loc = dst_loc

    # first location field info (water? army?)
    first_type,  idx1 = _get_field_info(first_loc, player, enemy_player)
    second_type, idx2 = _get_field_info(second_loc, player, enemy_player)

    print_move_flag = False
    if first_type == 'HomeBase':
      self.ask_winners_name_and_quit_game(src_loc, dst_loc, 'Scout')

    if first_type == 'Water' or first_type == 'Spearman' or first_type == 'Archer' or first_type == 'Knight' or first_type == 'Scout':
      print('')
      print(f"You have moved Scout from {src_loc} to {dst_loc}.")
      
      if first_type != 'Scout':
        print(f"We lost the army Scout due to your command!")
      if first_type == 'Scout':
        print("We destroyed the enemy Scout with massive loss!")
        del player.army['Scout'][current_army_idx]
        del player.army_move['Scout'][current_army_idx]
        del enemy_player.army['Scout'][idx1]
        del enemy_player.army_move['Scout'][idx1]
        #! del enemy scout
      else:
        del player.army['Scout'][current_army_idx]
        del player.army_move['Scout'][current_army_idx]

      return True

    elif first_type == 'Food' or first_type == 'Gold' or first_type == 'Wood':
      print('')
      print(f"You have moved Scout from {src_loc} to {dst_loc}.")
      print_move_flag = True
      print(f"Good. We collected 2 {first_type}.")

      if first_type == 'Gold':
        self.golds.remove(first_loc)
        player.apply_resource('gold')
      if first_type == 'Wood':
        self.woods.remove(first_loc)
        player.apply_resource('wood')
      if first_type == 'Food':
        self.foods.remove(first_loc)
        player.apply_resource('food')

    # second 
    if second_type == 'HomeBase':
      self.ask_winners_name_and_quit_game(src_loc, dst_loc, 'Scout')

    if second_type == 'Water' or second_type == 'Spearman' or second_type == 'Archer' or second_type == 'Knight' or second_type == 'Scout':
      if not print_move_flag:
        print(f"You have moved Scout from {src_loc} to {dst_loc}.")
      
      if second_type != 'Scout':
        print(f"We lost the army Scout due to your command!")
        #print('')
      if second_type == 'Scout':
        print("We destroyed the enemy Scout with massive loss!")
        del player.army['Scout'][current_army_idx]
        del player.army_move['Scout'][current_army_idx]
        del enemy_player.army['Scout'][idx2]
        del enemy_player.army_move['Scout'][idx2]
        #! del enemy scout
      else:
        del player.army['Scout'][current_army_idx]
        del player.army_move['Scout'][current_army_idx]

      return True
    elif second_type == 'Food' or second_type == 'Gold' or second_type == 'Wood':
      if second_type == 'Gold':
        self.golds.remove(second_loc)
        player.apply_resource('gold')
      if second_type == 'Wood':
        self.woods.remove(second_loc)
        player.apply_resource('wood')
      if second_type == 'Food':
        self.foods.remove(second_loc)
        player.apply_resource('food')

      #! move scout location!
      player.army['Scout'][current_army_idx] = second_loc

      if not print_move_flag:
        print('')
        print(f"You have moved Scout from {src_loc} to {dst_loc}.")
      print(f"Good. We collected 2 {second_type}.")
    else:
      if not print_move_flag:
        print('')
        print(f"You have moved Scout from {src_loc} to {dst_loc}.")
      #! move scout location!
      player.army['Scout'][current_army_idx] = second_loc
      player.army_move['Scout'][current_army_idx] = False

    return True
    
    

  def isValidLocationForMovingArmy(self, src_loc, dst_loc, player, enemy_player):
    current_army_type = None
    current_army_idx = None
    for army_type in player.army.keys():
      for idx in range(len(player.army[army_type])):
        if src_loc[0] == player.army[army_type][idx][0] and src_loc[1] == player.army[army_type][idx][1]:
          # movable?
          if player.army_move[army_type][idx]: # can move!
            current_army_type = army_type
            current_army_idx = idx

    if current_army_type is None:
      print('Invalid move. Try again.')
      print('')
      util_print_armies_to_move(player)
      return False, current_army_type

    if self.width <= dst_loc[0] or self.height <= dst_loc[1]:
      return False, current_army_type

    if current_army_type == 'Scout':
      dx = 2
      dy = 2
    else:
      dx = 1
      dy = 1
    
    distance_x = abs(src_loc[0] - dst_loc[0])  
    distance_y = abs(src_loc[1] - dst_loc[1])  
    is_valid_movement = True
    if distance_x == 0 and distance_y == 0:
      is_valid_movement = False
    elif distance_x > dx or distance_y > dy or (distance_x + distance_y) > dx:
      is_valid_movement = False      
    elif distance_x*distance_y != 0:
      is_valid_movement = False
    
    if not is_valid_movement: # invalid move (wrong location)
      print('Invalid move. Try again.')
      print('')
      util_print_armies_to_move(player)
      return False, current_army_type

    # my army 
    for army_type in player.army.keys():  
      for army_loc in player.army[army_type]:
        if dst_loc[0] == army_loc[0] and dst_loc[1] == army_loc[1]:
          print('Invalid move. Try again.')
          print('')
          util_print_armies_to_move(player)
          return False, current_army_type

    # my home base
    if dst_loc[0] == player.home_base[0][0] and dst_loc[1] == player.home_base[0][1]:
      print('Invalid move. Try again.')
      print('')
      util_print_armies_to_move(player)
      return False, current_army_type

    # scout move -> different branch
    if current_army_type == 'Scout':
      player.army_move['Scout'][current_army_idx] = False
      if abs(dst_loc[0] - src_loc[0]) + abs(dst_loc[1] - src_loc[1]) == 2:
        _flag = self.isValidLocationScout(current_army_idx, src_loc, dst_loc, player, enemy_player)
        return _flag, None


    # 4) resource
    for wood in self.woods: # list [ tuple ]  
      if dst_loc[0] == wood[0] and dst_loc[1] == wood[1]:
        # resource apply
        player.apply_resource('wood') # resource_type
        # remove resource 
        self.woods.remove(wood)
        player.army[current_army_type][current_army_idx] = dst_loc
        player.army_move[current_army_type][current_army_idx] = False
        print('')
        print(f"You have moved {current_army_type} from {src_loc} to {dst_loc}.")
        print("Good. We collected 2 Wood.")
        return True, current_army_type
    
    for food in self.foods: # list [ tuple ]  
      if dst_loc[0] == food[0] and dst_loc[1] == food[1]:
        player.apply_resource('food') # resource_type
        self.foods.remove(food)
        player.army[current_army_type][current_army_idx] = dst_loc
        player.army_move[current_army_type][current_army_idx] = False
        print('')
        print(f"You have moved {current_army_type} from {src_loc} to {dst_loc}.")
        
        print("Good. We collected 2 Food.")
        return True, current_army_type
    
    for gold in self.golds: # list [ tuple ]  
      if dst_loc[0] == gold[0] and dst_loc[1] == gold[1]:
        player.apply_resource('gold') # resource_type
        self.golds.remove(gold)

        player.army[current_army_type][current_army_idx] = dst_loc
        player.army_move[current_army_type][current_army_idx] = False
        print('')
        print(f"You have moved {current_army_type} from {src_loc} to {dst_loc}.")
        print("Good. We collected 2 Gold.")
        return True, current_army_type

    # 2) water
    for water in self.waters: # list [ tuple ]  
      if dst_loc[0] == water[0] and dst_loc[1] == water[1]:
        # kill! 
        del player.army[current_army_type][current_army_idx]
        del player.army_move[current_army_type][current_army_idx]
        print('')
        print(f"You have moved {current_army_type} from {src_loc} to {dst_loc}.")
                
        print(f"We lost the army {current_army_type} due to your command!")
        return True, current_army_type

    # 3) enemy    
    for army_type in enemy_player.army.keys():
      for idx in range(len(enemy_player.army[army_type])):
        if dst_loc[0] == enemy_player.army[army_type][idx][0] and dst_loc[1] == enemy_player.army[army_type][idx][1]:
          (ret1, ret2) = self.army_count(current_army_type, army_type)

          player.army_move[current_army_type][current_army_idx] = False
          print('')
          print(f"You have moved {current_army_type} from {src_loc} to {dst_loc}.")
          if ret1:
            # kill my army
            del player.army[current_army_type][current_army_idx]
            del player.army_move[current_army_type][current_army_idx]
            
            if not ret2:
              print(f"We lost the army {current_army_type} due to your command!")
              # print('') 
              # @@
          if ret2:
            if not ret1: # if my army alive
              player.army[current_army_type][current_army_idx] = dst_loc

            # kill enemy army
            del enemy_player.army[army_type][idx]
            del enemy_player.army_move[army_type][idx]
            if army_type == current_army_type:
              print(f"We destroyed the enemy {army_type} with massive loss!")
            else:
              print(f"Great! We defeated the enemy {army_type}!")
          return True, current_army_type

    # take enemy home base
    if dst_loc[0] == enemy_player.home_base[0][0] and dst_loc[1] == enemy_player.home_base[0][1]:
      self.ask_winners_name_and_quit_game(src_loc, dst_loc, current_army_type)

    # empty
    print('')
    print(f"You have moved {current_army_type} from {src_loc} to {dst_loc}.")
    player.army[current_army_type][current_army_idx] = dst_loc
    player.army_move[current_army_type][current_army_idx] = False
    return True, current_army_type

  def walk5g_ask_army_move(self, player):
    while True:
      print("Enter four integers as a format ‘x0 y0 x1 y1’ to represent move unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.")
      user_input = input()

      if 'NO' == user_input:
        print('')
        return True
      elif 'DIS' == user_input:
        self.visualize_map()
        return False  
      elif user_input == "PRIS":
        util_ls_price()
        return False  
      elif user_input == "QUIT":
        exit()
      elif len(user_input.split()) == 1 and not user_input.isnumeric():
        print('Invalid move. Try again.')
        return False
      elif len(user_input.split()) != 4:
        print('Invalid move. Try again.')
        return False
      elif len(user_input) != 7:
        print('Invalid move. Try again.')
        return False
      else: # coords
        input_list = user_input.split()
        for data in input_list:
          if not data.isnumeric(): 
            print('Invalid move. Try again.')
            return False

        x0, y0, x1, y1 = map(int, user_input.split()) #! exception 
        if x0 < 0 or y1 < 0 or x1 < 0 or y1 < 0:
          print('Invalid move. Try again.')
          return False
        if x0 >= self.width or x1 >= self.width or y0 >= self.height or y1 >= self.height:
          print('Invalid move. Try again.')
          return False

        src_loc = (x0, y0)
        dst_loc = (x1, y1)
        # get player index
        if player.get_player_index() == 1:
          enemy_player = self.player2
        else:
          enemy_player = self.player1

        flag_5f, army_type = self.isValidLocationForMovingArmy(src_loc, dst_loc, player, enemy_player)
        if flag_5f:
          break
      
  def walk5e_army_move(self, player):
    # 5-e 
    print("===Player {}'s Stage: Move Armies===".format(player.get_player_index()))
    
    while True:
      # 5-f : no amry chcker -> turn finish
      if self.walk5f_move_input_check(player):
        return True  # goto 5-a
      else:
        if not util_print_armies_to_move(player):
          break
      # 5-g
      flag = self.walk5g_ask_army_move(player) # False -> Dis, PRIS
      if flag:                                 # True -> No, 
        break
    # set army_move to True
    player.set_all_army_movable()

  def run(self,filepath): # walkthough-5
    # 1 greeting
    print("Configuration file {} was loaded.".format(filepath))
    # 2
    print("Game Started: Little Battle! (enter QUIT to quit the game)")
    print("")
    # 3
    self.visualize_map() #debug code
    print("(enter DIS to display the map)")
    print("")
    # 4
    util_ls_price()
    print("(enter PRIS to display the price list)")
    print("")
    
    while True:
      self.walk5_printYear()

      #############################################
      # player 1
      #############################################
      self.walk5b_print('1')
      self.player1.print_asset()
      # 5-d
      while True:
        flag = self.walk5d_recruit_input_check(self.player1)
        if flag:
          break
      
      # army move!
      self.walk5e_army_move(self.player1) # if reutnr true -> goto 5-a
      #############################################
      # player 2
      #############################################
      self.walk5_printYear() # print year
      self.walk5b_print('2')
      self.player2.print_asset()
      # 5-d
      while True:
        flag = self.walk5d_recruit_input_check(self.player2)
        if flag:
          break
      # recruited finished!
      self.walk5e_army_move(self.player2) # if reutnr true -> goto 5-a
      self.year +=1

###############################################
# Player
###############################################
class Player:
  def __init__(self, home_base, player_index):
    self.gold = 2
    self.wood = 2
    self.food = 2

    self.my_index = player_index

    self.army = {'Spearman': [], 'Archer': [], 'Knight': [], 'Scout': [] }
    self.army_move = {'Spearman': [], 'Archer': [], 'Knight': [], 'Scout': [] }
    
    self.home_base = []
    self.home_base.append(home_base)

    # army price table(dict)
    self.army_price_table = {'Spearman': {'gold': 0, 'wood': 1, 'food':1},
                            'Archer': {'gold': 1, 'wood': 1, 'food':0},
                            'Knight': {'gold': 1, 'wood': 0, 'food':1},
                            'Scout': {'gold': 1, 'wood': 1, 'food':1}}

  def money_check(self):
    if self.gold + self.wood + self.food < 2:
      return False

    zero_cnt = 0
    if self.gold == 0:
      zero_cnt += 1
    if self.wood == 0:
      zero_cnt += 1
    if self.food == 0:
      zero_cnt += 1
    if zero_cnt > 1:
      return False

    return True
    


  def apply_resource(self, resource_type):
    if 'gold' == resource_type:
      self.gold += 2
    elif 'food' == resource_type:
      self.food += 2
    elif 'wood' == resource_type:
      self.wood += 2
    
  def no_army_check(self): # -> bool:
    army_cnt = 0 
    for army_key in self.army.keys():
      army_cnt += len(self.army[army_key])

    if army_cnt == 0:
      return True
    else:
      return False

  def get_player_index(self):
    return self.my_index

  def set_all_army_movable(self):
    for key in self.army_move.keys():
      for idx in range(len(self.army_move[key])):
        self.army_move[key][idx] = True

  def locate_army(self, army_type, location): # location : tuple 
    self.army[army_type].append(location)
    self.army_move[army_type].append(True)

  def apply_price(self, army_type):
    self.gold -= self.army_price_table[army_type]['gold']
    self.food -= self.army_price_table[army_type]['food']
    self.wood -= self.army_price_table[army_type]['wood']

  def buy_army(self, army_type):
    if self.army_price_table[army_type]['gold'] <= self.gold and \
      self.army_price_table[army_type]['wood'] <= self.wood and \
        self.army_price_table[army_type]['food'] <= self.food:
      return True
    else:
      return False


  def print_asset(self):
    print('[Your Asset: Wood - {} Food - {} Gold - {}]'.format(self.wood, self.food, self.gold))


if __name__ == "__main__":
  
  if len(sys.argv) != 2:
   print("Usage: python3 little_battle.py <filepath>")
   sys.exit()
  filepath = sys.argv[1]  
  width, height, waters, woods, foods, golds = load_config_file(filepath )

  game = Game(width, height, waters, woods, foods, golds)
  game.run(filepath)
