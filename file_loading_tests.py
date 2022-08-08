from little_battle import load_config_file
folder_path = "./invalid_files/"

def test_file_not_found():
  # no need to create a file for FileNotFound
  try:
    load_config_file("./invalid_files/jwfejoi.txt")
  except FileNotFoundError:
    print("Testing file not found passed")
  except Exception as e:
    assert False, "Testing file not found failed"
def test_format_error():
  # add "format_error_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/format_error_file.txt")
  except SyntaxError as e:
    assert str(e) == "Invalid Configuration File: format error!", "Testing format error is failed"
    print("Testing format error is passed")
def test_frame_format_error():
  # add "frame_format_error_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/frame_format_error_file.txt") 
  except SyntaxError as e:
    assert str(e) == "Invalid Configuration File: frame should be in format widthxheight!", "Testing frame format is failed"
    print("Testing frame format is passed")

def test_frame_out_of_range():
  # add "format_out_of_range_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/format_out_of_range_file.txt")
  except ArithmeticError as e:
    assert str(e) == "Invalid Configuration File: width and height should range from 5 to 7!", "Testing frame out of range is failed"
    print("Testing frame out of range is passed")  

def test_non_integer():
  # add "non_integer_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/non_integer_file.txt")
  except ValueError as e:
    assert str(e) == "Invalid Configuration File: Wood contains non integer characters!", "Testing non integer is failed"
    print("Testing non integer is passed")
  
def test_out_of_map():
  # add "out_of_map_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/out_of_map_file.txt")
  except ArithmeticError as e:
    assert str(e) == "Invalid Configuration File: Wood contains a position that is out of map.", "Testing out of map is failed"
    print("Testing out of map is passed")
  
def test_occupy_home_or_next_to_home():
  # add two invalid files: "occupy_home_file.txt" and
  # "occupy_next_to_home_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/occupy_home_file.txt")
  except ValueError as e:
    assert str(e) == "Invalid Configuration File: The positions of home bases are occupied!", "Testing occupy home base is failed"
    print("Testing occupy home base is passed")

  try:
    load_config_file("./invalid_files/occupy_next_to_home_file.txt")
  except ValueError as e:
    assert str(e) == "Invalid Configuration File: The positions of the positions next to the home bases are occupied!", "Testing occupy next to home base is failed"
    print("Testing occupy next to home base is passed")

def test_duplicate_position():
  # add two files: "dupli_pos_in_single_line.txt" and
  # "dupli_pos_in_multiple_lines.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/dupli_pos_in_single_line.txt")
  except SyntaxError as e:
    assert str(e) == "Invalid Configuration File: Duplicate position (1, 3)!", "Testing duplicated position in single line is failed" 
    print("Testing duplicated position in single line is passed")
  
  try:
    load_config_file("./invalid_files/dupli_pos_in_multiple_lines.txt")
  except SyntaxError as e:
    assert str(e) == "Invalid Configuration File: Duplicate position (0, 0)!", "Testing duplicated position in multiple lines is failed" 
    print("Testing duplicated position in multiple lines is passed")

def test_odd_length():
  # add "odd_length_file.txt" in "invalid_files"
  try:
    load_config_file("./invalid_files/odd_length_file.txt")
  except SyntaxError as e:
    assert str(e) == "Invalid Configuration File: Water has an odd number of elements!", "Testing odd length of file is failed" 
    print("Testing odd length of file is passed")
  

def test_valid_file():
  # no need to create file for this one, just test loading config.txt
  try:
    load_config_file("config.txt")
    print("File loading is passed")
  except:
    print("File loading is failed")
  

# you can run this test file to check tests and load_config_file
if __name__ == "__main__":
  # test_file_not_found()
  test_format_error()
  test_frame_format_error()
  test_frame_out_of_range()
  test_non_integer()
  test_out_of_map()
  test_occupy_home_or_next_to_home()
  test_duplicate_position()
  test_odd_length()
  test_valid_file()