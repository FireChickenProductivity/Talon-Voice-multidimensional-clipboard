copy <user.letter>:
	user.copy_selected_text_into_multidimensional_clipboard(letter)
copy all <user.letter>:
	edit.select_all()
	user.copy_selected_text_into_multidimensional_clipboard(letter)
copy line <user.letter>:
	edit.select_line()
	user.copy_selected_text_into_multidimensional_clipboard(letter)

paste <user.letter>:
	user.paste_multidimensional_clipboard_text(letter)
(paste|replace) all <user.letter>:
	edit.select_all()
	user.paste_multidimensional_clipboard_text(letter)
(paste|replace) line <user.letter>:
	edit.select_line()
	user.paste_multidimensional_clipboard_text(letter)

multi clipboard [display]:
	user.toggle_multidimensional_clipboard_display()

move multi clipboard [display]:
	user.set_multidimensional_clipboard_display_position_to_current_mouse_position()

open [multi] clipboard <user.letter>:
	user.open_multidimensional_clipboard_file(letter)
