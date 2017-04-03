import sublime
import sublime_plugin

bh_core_latex_settings = {
    "user_scope_brackets": [
        {
            "name": "latexmath_block",
            "open": "((?<!\\\\)\\$\\$)",
            "close": "((?<!\\\\)\\$\\$)",
            "style": "default",
            "scopes": ["text.tex.latex meta.environment.math"],
            "sub_bracket_search": True,
            "enabled": True
        }
    ],

    "user_brackets": [
        {
            "name": "latexmath_angle",
            "open": "(\\\\langle)",
            "close": "(\\\\rangle)",
            "style": "default",
            "language_filter": "whitelist",
            "language_list": ["LaTeX"],
            "scope_exclude": ["comment"],
            "find_in_sub_search": True,
            "enabled": True
        },
        {
            "name": "latexmath_leftright",
            "open": "(\\\\left(?:[()\\[\\]|]|\\\\[{}|]|\\\\[a-zA-Z]+))",
            "close": "(\\\\right(?:[()\\[\\]|]|\\\\[{}|]|\\\\[a-zA-Z]+))",
            "style": "default",
            "language_filter": "whitelist",
            "language_list": ["LaTeX"],
            "scope_exclude": ["comment"],
            "find_in_sub_search": True,
            "enabled": True
        },
        {
            "name": "latexmath_square",
            "open": "((?<!\\\\)\\\\\\[)",
            "close": "((?<!\\\\)\\\\\\])",
            "style": "square",
            "language_filter": "whitelist",
            "language_list": ["LaTeX"],
            "scope_exclude": ["comment"],
            "find_in_sub_search": True,
            "enabled": True
        },
        {
            "name": "latexmath_curly",
            "open": "((?<!\\\\)\\\\\\{)",
            "close": "((?<!\\\\)\\\\\\})",
            "style": "curly",
            "language_filter": "whitelist",
            "language_list": ["LaTeX"],
            "scope_exclude": ["comment"],
            "find_in_sub_search": True,
            "enabled": True
        },
        {
            "name": "latexmath_round",
            "open": "((?<!\\\\)\\\\\\()",
            "close": "((?<!\\\\)\\\\\\))",
            "style": "round",
            "language_filter": "whitelist",
            "language_list": ["LaTeX"],
            "scope_exclude": ["comment"],
            "find_in_sub_search": True,
            "enabled": True
        }
    ]
}

bh_core_settings_file = "bh_core.sublime-settings"


class LatexyzInstallBhSettings(sublime_plugin.TextCommand):

    def run(self, edit, remove=False):
        bh_core_settings = sublime.load_settings(bh_core_settings_file)
        for k, v in bh_core_latex_settings.items():
            bh_core_settings.set(k, self.merge(v, bh_core_latex_settings[k], remove))
        sublime.save_settings(bh_core_settings_file)

    def merge(self, old, new, remove):
        out = []
        for o in old:
            found = False
            for n in new:
                if o["name"] == n["name"]:
                    found = True
                    break
            if not found:
                out.append(o)
        if remove:
            return out
        else:
            return out + new
