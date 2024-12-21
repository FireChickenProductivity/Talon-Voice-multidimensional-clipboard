The Talon Voice commands defined by this project let the user store the currently selected text within 1 of 26 files each associated with 1 of the letters of the English alphabet. The user can then paste the text stored within any of those files and can optionally have the contents of the first line of each file displayed.

<h1>Commands</h1>
The user can store the currently selected text within the desired file by dictating:

copy (this or that or here) (the Talon phonetic alphabet word for the desired letter)

Assuming a standard Talon set up, dictating copy that air would store the selected text in the a file, and dictating copy whale would store the selected text in the w file.

The user can paste the text stored within the desired file by dictating:

paste (this or that or here) (the Talon phonetic alphabet word for the desired letter)

Assuming a standard Talon set up, dictating paste air would paste the text within the a file, and dictating paste whale would store the text within the w file.

The user can have Talon type out the text stored within the desired file by dictating:

typeout (the Talon phonetic alphabet word for the desired letter). The word "that" can be optionally said after typeout. 

The copy line (this or that or here) and copy all commands will store the line and entire document respectively in the file associated with the letter denoted at the end of the command. The paste line and paste all commands respectively replace the line and entire document with the text stored in the file associated with the letter denoted at the end of the command. Those pasting commands can alternatively be dictated with the word replace instead of the word paste.

The command “multi clipboard display” toggles the display for those files (The word display is optional). The display can be moved to the current mouse position by dictating “move multi clipboard display” (The word display is optional).

The clipboard files can be opened with open clipboard (the talon phonetic alphabet word for the desired letter)  

If using cursorless, the user can copy the text at a cursorless target into the clipboard system by dictating: 

copy (the Talon phonetic alphabet word for the desired letter) (target or at) (cursorless target). The word "that" can be optionally said after copy.

<h1>Settings</h1>
Several settings are defined within the multidimensional clipboard settings.talon file:
  
The user.multidimensional_clipboard_display_line_length_limit setting determines how much of the first line of each file within the system will get displayed. Setting this to 0 means that there is no limit. 
  
The user.multidimensional_clipboard_file_size_limit setting determines how big a file in bytes the system is willing to paste. If properly configured, this setting should prevent the commands from loading too much data into memory to perform a single gigantic paste. Files that are too big will not have any text displayed in the clipboard display.
  
The user.multidimensional_clipboard_operation_delay setting determines how long in milliseconds the copying and pasting commands will pause. Increase this if the copying or pasting commands are not working properly on your computer.

<h1>Actions</h1>
Several actions are provided to make it easier to build custom commands for working with the clipboard system:

user.get_multidimensional_clipboard_text(clipboard_letter)

Returns the text stored in the clipboard file referred to by the letter passed to it.

user.get_multidimensional_clipboard_display_text(clipboard_letter)

Returns the display text for the clipboard file referred to by the letter passed to it.

update_multidimensional_clipboard(clipboard_letter, new_text)

Stores the new_text in the clipboard file referred to by the clipboard_letter.

# Alternatives
[Clippy](https://github.com/AndreasArvidsson/clippy) is a sophisticated standalone application clipboard manager with talon commands for it.
