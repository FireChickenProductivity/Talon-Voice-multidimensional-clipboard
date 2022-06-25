from talon import Module, actions, clip, imgui, ctrl
import os

mod = Module()
MULTIDIMENSIONAL_CLIPBOARD_FOLDER = 'multidimensional clipboard data'
OTHER_DATA_FOLDER = 'other data'
COMMAND_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
STORAGE_FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
				'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z']
DISPLAY_POSITION_FILE = os.path.join(COMMAND_DIRECTORY, OTHER_DATA_FOLDER, 'display position.txt')

display_line_length_limit = mod.setting(
	'multidimensional_clipboard_display_line_length_limit',
	type = int,
	default = 60,
	desc = 'The limit for how characters the multidimensional clipboard display will show for each line. 0 means no limit'
)

file_size_limit = mod.setting(
	'multidimensional_clipboard_file_size_limit',
	type = int,
	default = 1073741824,
	desc = 'The multidimensional clipboard system will not attempt to paste the contents of any of its text files if its size in bytes exceeds this number.'
)

clipboard_operation_delay = mod.setting(
	'multidimensional_clipboard_operation_delay',
	type = int,
	default = 150,
	desc = 'How long in milliseconds the multidimensional clipboard commands will pause to ensure that they do not restore the clipboard too quickly. Increase this if copying or pasting does not work.'
)

@mod.action_class
class Actions:
	def update_multidimensional_clipboard (destination_name: str, new_text: str):
		'''Updates the multidimensional clipboard file with the specified name with the new text.'''
		with open (compute_multidimensional_clipboard_destination_path(destination_name), 'w') as clipboard_file:
			clipboard_file.write(new_text)
	def copy_selected_text_into_multidimensional_clipboard (destination_name: str):
		'''Updates the multidimensional clipboard file with the specified name with the selected text.'''
		selected_text = get_selected_text()
		actions.user.update_multidimensional_clipboard(destination_name, selected_text)
	def paste_multidimensional_clipboard_text (target_name: str):
		'''Pastes the text in the specified multidimensional clipboard file.'''
		clipboard_text = get_multidimensional_clipboard_text(target_name)
		if clipboard_text != '':
			paste_text(clipboard_text)
	def toggle_multidimensional_clipboard_display ():
		'''Toggles whether or not the multidimensional clipboard is displayed.'''
		if gui.showing:
			gui.hide()
		else:
			gui.show()
	def set_multidimensional_clipboard_display_position_to_current_mouse_position ():
		'''Sets the display position of themultidimensional clipboard display to the current mouse position.'''
		horizontal, vertical = ctrl.mouse_pos() 
		update_mouse_storage_file(DISPLAY_POSITION_FILE, horizontal, vertical)
		if gui.showing:
			gui.hide()
			gui.show()
			gui.hide()
			actions.sleep('1s')
			gui.show()
			
def paste_text (text: str):
	with clip.revert():
		clip.set_text(text)
		actions.edit.paste()
		wait_long_enough_to_let_clipboard_revert_properly()

def wait_long_enough_to_let_clipboard_revert_properly():
	actions.sleep(f'{clipboard_operation_delay.get()}ms')
	

def get_multidimensional_clipboard_text (target_name: str):
	filepath = compute_multidimensional_clipboard_destination_path(target_name)
	if not file_valid_for_multidimensional_clipboard_use(filepath):
		return ''
	with open (filepath, 'r') as clipboard_file:
		return clipboard_file.read()

def file_valid_for_multidimensional_clipboard_use (filepath: str):
	if not os.path.exists(filepath):
		return False
	file_size = os.path.getsize(filepath)
	if file_size == 0 or file_size > file_size_limit.get():
		return False
	return True

def compute_multidimensional_clipboard_destination_path (destination_name: str):
	return os.path.join(COMMAND_DIRECTORY, MULTIDIMENSIONAL_CLIPBOARD_FOLDER, destination_name + '.txt')

def get_selected_text():
	with clip.revert():
		actions.edit.copy()
		wait_long_enough_to_let_clipboard_revert_properly()
		result = clip.text()
	return result

def should_trim_line (line_text):
	# return display_line_length_limit.get() != 0 and display_line_length_limit.get() > len(line_text)
	return len(line_text) > display_line_length_limit.get() and display_line_length_limit.get() != 0

def trim_line (line_text):
	return line_text[:display_line_length_limit.get()]
	
def get_initial_line_from_multidimensional_clipboard_file (target_name: str):
	filepath = compute_multidimensional_clipboard_destination_path(target_name)
	if not file_valid_for_multidimensional_clipboard_use(filepath):
		return ''
	with open (filepath, 'r') as clipboard_file:
		line_text = clipboard_file.readline()
		if should_trim_line(line_text):
			return trim_line(line_text)
		return line_text

class PositionUnavailableError(Exception):
	pass

def get_stored_mouse_position (filepath):
	try:
		with open (filepath, 'r') as mouse_position_file:
			line = mouse_position_file.readline()
			position = line.split(' ')
			horizontal = position[0]
			vertical = position[1]
			return horizontal, vertical
	except:	
		raise PositionUnavailableError()
	


def get_display_position_coordinate (coordinate_name):
	try:
		horizontal, vertical = get_stored_mouse_position(DISPLAY_POSITION_FILE)
		if coordinate_name == 'horizontal':
			return int(horizontal)
		elif coordinate_name == 'vertical':
			return int(vertical)
	except PositionUnavailableError:
		return 0

@imgui.open(x = get_display_position_coordinate('horizontal'), y = get_display_position_coordinate('vertical'))
def gui(gui: imgui.GUI):
	gui.x = get_display_position_coordinate('horizontal')
	gui.y = get_display_position_coordinate('vertical')
	gui.text("Multidimensional Clipboard")
	gui.line()
	for name in STORAGE_FILES:
		file_line = name + ': ' + get_initial_line_from_multidimensional_clipboard_file(name)
		gui.text(file_line)


		
def update_mouse_storage_file (filepath: str, horizontal, vertical):
	'''Stores the specified mouse position in the specified file.'''
	with open (filepath, 'w') as mouse_position_file:
		mouse_position_file.write(str(horizontal) + ' ' + str(vertical))
			

