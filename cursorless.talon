tag: user.cursorless
-
copy [that] <user.letter> (target|at) <user.cursorless_target>:
    text = user.cursorless_get_text(cursorless_target)
    user.update_multidimensional_clipboard(letter, text)