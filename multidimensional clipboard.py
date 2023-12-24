from talon import Module, actions, clip, imgui, ctrl, settings, fs
import os

mod = Module()
MULTIDIMENSIONAL_CLIPBOARD_FOLDER = 'multidimensional clipboard data'
OTHER_DATA_FOLDER = 'other data'
COMMAND_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
STORAGE_DIRECTORY = os.path.join(COMMAND_DIRECTORY, MULTIDIMENSIONAL_CLIPBOARD_FOLDER)
STORAGE_FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
				'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
DISPLAY_POSITION_FILE = os.path.join(COMMAND_DIRECTORY, OTHER_DATA_FOLDER, 'display position.txt')

display_line_length_limit_setting_name = 'multidimensional_clipboard_display_line_length_limit'
display_line_length_limit = 'user.' + display_line_length_limit_setting_name
mod.setting(
	display_line_length_limit_setting_name,
	type = int,
	default = 60,
	desc = 'The limit for how characters the multidimensional clipboard display will show for each line. 0 means no limit'
)

text_buffer_limit_setting_name = 'multidimensional_clipboard_text_buffer_limit'
text_buffer_limit = 'user.' + text_buffer_limit_setting_name
mod.setting(
	text_buffer_limit_setting_name,
	type = int,
	default = 100,
	desc = 'The limit for how many characters to keep in active memory to avoid having to reload the clipboard text from the file with the multidimensional clipboard'
)

file_size_limit_setting_name = 'multidimensional_clipboard_file_size_limit'
file_size_limit = 'user.' + file_size_limit_setting_name
mod.setting(
	file_size_limit_setting_name,
	type = int,
	default = 1073741824,
	desc = 'The multidimensional clipboard system will not attempt to paste the contents of any of its text files if its size in bytes exceeds this number.'
)

clipboard_operation_delay_setting_name = 'multidimensional_clipboard_operation_delay'
clipboard_operation_delay = 'user.' + clipboard_operation_delay_setting_name
mod.setting(
	clipboard_operation_delay_setting_name,
	type = int,
	default = 150,
	desc = 'How long in milliseconds the multidimensional clipboard commands will pause to ensure that they do not restore the clipboard too quickly. Increase this if copying or pasting does not work.'
)

@mod.action_class
class Actions:
	def update_multidimensional_clipboard (destination_name: str, new_text: str):
		'''Updates the multidimensional clipboard file with the specified name with the new text.'''
		with open (compute_multidimensional_clipboard_destination_path(destination_name), 'wb') as clipboard_file:
			clipboard_file.write(new_text.encode())
	def copy_selected_text_into_multidimensional_clipboard (destination_name: str):
		'''Updates the multidimensional clipboard file with the specified name with the selected text.'''
		selected_text = get_selected_text()
		actions.user.update_multidimensional_clipboard(destination_name, selected_text)
	def paste_multidimensional_clipboard_text (target_name: str):
		'''Pastes the text in the specified multidimensional clipboard file.'''
		clipboard_text = get_multidimensional_clipboard_text(target_name)
		if clipboard_text != '':
			paste_text(clipboard_text)
	def type_out_multidimensional_clipboard_text (target_name: str):
		'''Types the text in the specified multidimensional clipboard file'''
		clipboard_text = get_multidimensional_clipboard_text(target_name)
		if clipboard_text != '':
			actions.insert(clipboard_text)
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
	def open_multidimensional_clipboard_file(filename: str):
		'''Opens the desired multidimensional clipboard file'''
		filepath = compute_multidimensional_clipboard_destination_path(filename)
		actions.user.edit_text_file(filepath)

def initialize_clipboard_files ():
	for file_name in STORAGE_FILES: initialize_clipboard_file(file_name)
	
def initialize_clipboard_file (name: str):
	path = compute_multidimensional_clipboard_destination_path(name)
	if does_file_need_to_be_initialized(path):
		create_empty_file(path)

def initialize_display_position_file ():
	if does_file_need_to_be_initialized(DISPLAY_POSITION_FILE):
		update_mouse_storage_file(DISPLAY_POSITION_FILE, 0, 0)

def does_file_need_to_be_initialized (path: str):
	return not os.path.exists(path)

def create_empty_file(path: str):
	with open(path, "w") as file: pass

def paste_text (text: str):
	with clip.revert():
		clip.set_text(text)
		actions.edit.paste()
		wait_long_enough_to_let_clipboard_revert_properly()

def wait_long_enough_to_let_clipboard_revert_properly():
	actions.sleep(f'{settings.get(clipboard_operation_delay)}ms')
	

def get_multidimensional_clipboard_text (target_name: str):
	if clipboard_file_manager_collection.does_manager_contain_entire_file(target_name):
		return clipboard_file_manager_collection.get_buffer_text(target_name)
		
	filepath = compute_multidimensional_clipboard_destination_path(target_name)
	if not file_valid_for_multidimensional_clipboard_use(filepath):
		return ''
	with open (filepath, 'rb') as clipboard_file:
		return clipboard_file.read().decode()

def file_valid_for_multidimensional_clipboard_use (filepath: str):
	if not os.path.exists(filepath):
		return False
	file_size = os.path.getsize(filepath)
	if file_size == 0 or file_size > settings.get(file_size_limit):
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
	return len(line_text) > settings.get(display_line_length_limit) and settings.get(display_line_length_limit) != 0

def trim_line (line_text):
	return line_text[:settings.get(display_line_length_limit)]

class ClipboardFileManager:
	def __init__(self, name: str):
		self.name = name
		self.contains_trimmed_text: bool = False
		self.display_text = ""
		self.buffer_text = ""
		self.load()
	
	def load(self):
		filepath = compute_multidimensional_clipboard_destination_path(self.name)
		if not file_valid_for_multidimensional_clipboard_use(filepath):
			self.text = ''
			self.buffer_text = ""
			self.contains_trimmed_text = False
		with open (filepath, 'r') as clipboard_file:
			line_text = clipboard_file.readline()
			if should_trim_line(line_text):
				self.text = trim_line(line_text)
			else:
				self.text = line_text
		with open (filepath, 'r') as clipboard_file:
			self.buffer_text = clipboard_file.read(settings.get(text_buffer_limit) + 1)
			self.contains_trimmed_text = len(self.buffer_text) > settings.get(text_buffer_limit)
			if self.contains_trimmed_text: self.buffer_text = None
	
	def get_display_text(self) -> str:
		return self.text

	def get_buffer_text(self) -> str:
		print(self.buffer_text, len(self.buffer_text))
		return self.buffer_text
	
	def contains_entire_file(self) -> bool:
		return not self.contains_trimmed_text

class ClipboardFileManagerCollection:
	def __init__(self):
		self.managers = {}
		for name in STORAGE_FILES:
			self.managers[name] = ClipboardFileManager(name)
		
	def get_text(self, name: str) -> str:
		manager = self._get_manager(name)
		return manager.get_display_text()

	def get_buffer_text(self, name: str) -> str:
		manager = self._get_manager(name)
		return manager.get_buffer_text()
	
	def does_manager_contain_entire_file(self, name: str) -> bool:
		manager = self._get_manager(name)
		return manager.contains_entire_file()

	def reload(self, name: str):
		manager = self._get_manager(name)
		manager.load()

	def _get_manager(self, name: str) -> ClipboardFileManager:
		return self.managers[name]

clipboard_file_manager_collection = ClipboardFileManagerCollection()
def reload_clipboard_file(name, flags):
	global clipboard_file_manager_collection
	clipboard_file_manager_collection.reload(name[-5])

class PositionUnavailableError(Exception):
	pass

def get_stored_mouse_position (filepath):
	try:
		with open (filepath, 'r') as mouse_position_file:
			line = mouse_position_file.readline()
			position = line.split(' ')
			horizontal = int(position[0])
			vertical = int(position[1])
			return horizontal, vertical
	except:	
		raise PositionUnavailableError()
	
class PositionFileManager:
	def __init__(self, path: str):
		self.path = path
		self.load()
	
	def load(self):
		try:
			horizontal, vertical = get_stored_mouse_position(self.path)
		except PositionUnavailableError:
			horizontal = 0
			vertical = 0
		self.horizontal = int(horizontal)
		self.vertical = int(vertical)
	
	def get_horizontal(self) -> int:
		return self.horizontal

	def get_vertical(self) -> int:
		return self.vertical
	
	def get_path(self) -> str:
		return self.path

position_file_manager = PositionFileManager(DISPLAY_POSITION_FILE)

def get_display_position_coordinate (coordinate_name):
	if coordinate_name == 'horizontal':
		return position_file_manager.get_horizontal()
	elif coordinate_name == 'vertical':
		return position_file_manager.get_vertical()

@imgui.open(x = get_display_position_coordinate('horizontal'), y = get_display_position_coordinate('vertical'))
def gui(gui: imgui.GUI):
	gui.x = get_display_position_coordinate('horizontal')
	gui.y = get_display_position_coordinate('vertical')
	gui.text("Multidimensional Clipboard")
	gui.line()
	for name in STORAGE_FILES:
		file_line = name + ': ' + clipboard_file_manager_collection.get_text(name)
		gui.text(file_line)
		
def update_mouse_storage_file (filepath: str, horizontal, vertical):
	'''Stores the specified mouse position in the specified file.'''
	with open (filepath, 'w') as mouse_position_file:
		mouse_position_file.write(str(horizontal) + ' ' + str(vertical))
	position_file_manager.load()

def reload_clipboard_file_when_storage_directory_file_changes():
	fs.watch(STORAGE_DIRECTORY, reload_clipboard_file)

def setup():
	initialize_clipboard_files()
	initialize_display_position_file()
	reload_clipboard_file_when_storage_directory_file_changes()

setup()