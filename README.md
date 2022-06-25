# Talon-Voice-multidimensional-clipboard
The Talon Voice commands defined by this project let the user store the currently selected text within 1 of 26 files each associated with 1 of the letters of the English alphabet. The user can then paste the text stored within any of those files and can optionally have the contents of the first line of each file displayed.
The user can store the currently selected text within the desired file by dictating:
copy <the Talon phonetic alphabet word for the desired letter>
Assuming a standard Talon set up, dictating copy air would store the selected text in the a file, and dictating copy whale would store the selected text in the w file.
The user can paste the text stored within the desired file by dictating:
paste <the Talon phonetic alphabet word for the desired letter>
Assuming a standard Talon set up, dictating paste air would paste the text within the a file, and dictating paste whale would store the text within the w file.

The command “multi clipboard” toggles the display for those files. The display can be moved to the current mouse position by dictating “move multi clipboard display”.

Several settings are defined within the multidimensional clipboard settings.talon file:
The user.multidimensional_clipboard_display_line_length_limit setting determines how much of the first line of each file within the system will get displayed. Setting this to 0 means that there is no limit. 
The user.multidimensional_clipboard_file_size_limit setting determines how big a file in bytes the system is willing to paste. This setting should prevent the command from either loading too much data into memory to perform a single gigantic paste or from needing to take to take multiple pastes to perform the desired task.
The user.multidimensional_clipboard_operation_delay setting determines how long in milliseconds the copying and pasting commands will pause. Increase this if the copying or pasting commands are not working properly on your computer.

