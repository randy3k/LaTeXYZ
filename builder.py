import sublime
import sublime_plugin


class LatexBoxChooseBuildSystemCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings('LaTeXBox.sublime-settings')
        bsys = settings.get("cmd_variants")
        display = [[key, " ".join(value)] for key, value in bsys.items()]

        sublime.set_timeout(lambda: self.window.show_quick_panel(display, on_action), 100)

        def on_action(action):
            if action < -1:
                return
            key = display[action][0]
            value = bsys.get(key)
            settings.set("cmd", value)
            settings.set("cmd_force", [value[0]]+["-g"]+value[1:])
            sublime.save_settings('LaTeXBox.sublime-settings')
