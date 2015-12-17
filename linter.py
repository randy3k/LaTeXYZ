import sublime


def plugin_loaded():
    s = sublime.load_settings("SublimeLinter.sublime-settings")
    if s.has("user"):
        user = s.get("user")
        user.get("syntax_map", {}).update({"latex+": "latex"})
        s.set("user", user)
        sublime.save_settings("SublimeLinter.sublime-settings")
