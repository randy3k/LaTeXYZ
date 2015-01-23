import sublime
import sublime_plugin
import os
import re


def valid(str):
    return re.match('^[\w._\\\\]+$', str) is not None

maths = [
    ("\\alpha", ),
    ("\\beta", ),
    ("\\gamma", ),
    ("\\delta", ),
    ("\\epsilon", ),
    ("\\varepsilon", ),
    ("\\zeta", ),
    ("\\eta", ),
    ("\\theta", ),
    ("\\vartheta", ),
    ("\\iota", ),
    ("\\kappa", ),
    ("\\lambda", ),
    ("\\mu", ),
    ("\\nu", ),
    ("\\xi", ),
    ("\\pi", ),
    ("\\rho", ),
    ("\\sigma", ),
    ("\\tau", ),
    ("\\upsilon", ),
    ("\\phi", ),
    ("\\varphi", ),
    ("\\chi", ),
    ("\\psi", ),
    ("\\omega", ),
    ("\\digamma", ),
    ("\\Gamma", ),
    ("\\Delta", ),
    ("\\Theta", ),
    ("\\Lambda", ),
    ("\\Xi", ),
    ("\\Pi", ),
    ("\\Sigma", ),
    ("\\Phi", ),
    ("\\Psi", ),
    ("\\Omega", ),

    ("\\infty", ),
    ("\\varnothing", ),

    ("\\quad", ),
    ("\\qquad", ),

    ("\\bigcup", ),
    ("\\bigcap", ),
    ("\\langle", ),
    ("\\rangle", ),
    ("\\bigcup", ),
    ("\\bigcap", ),

    ("\\leftarrow", ),
    ("\\longleftarrow", ),
    ("\\Leftarrow", ),
    ("\\Longleftarrow", ),
    ("\\rightarrow", ),
    ("\\longrightarrow", ),
    ("\\Rightarrow", ),
    ("\\Longrightarrow", ),
    ("\\leftrightarrow", ),
    ("\\longleftrightarrow", ),
    ("\\Leftrightarrow", ),
    ("\\Longleftrightarrow", ),
    ("\\uparrow", ),
    ("\\downarrow", ),

    ("\\mathit", ),
    ("\\mathbf", ),
    ("\\mathbb", ),
    ("\\mathrm", ),
    ("\\mathsf", ),
    ("\\mathcal", ),

    ("\\partial", ),

    ("\\sum_{}^{}", "sum_{$1}^{$2}$0"),
    ("\\prod_{}^{}", "prod_{$1}^{$2}$0"),
    ("\\int_{}^{}", "int_{$1}^{$2}$0"),
    ("\\frac{}{}", "frac{$1}{$2}$0"),
    ("\\overset{}{}", "overset{$1}{$2}$0"),
    ("\\underset{}{}", "underset{$1}{$2}$0"),

    ("\\binom{}{}", "binom{$1}{$2}$0"),
    ("\\text{}", "text{$1}$0")
]

general = [
    ("\\includegraphics{}", "includegraphics{$1}" ),
    ("\\part{}", "part{$1}" ),
    ("\\part*{}", "part*{$1}" ),
    ("\\chapter{}", "chapter{$1}" ),
    ("\\chapter*{}", "chapter*{$1}" ),
    ("\\section{}", "section{$1}" ),
    ("\\section*{}", "section*{$1}" ),
    ("\\subsection{}", "subsection{$1}" ),
    ("\\subsection*{}", "subsection*{$1}" ),

    ("\\underline{}", "underline{$1}" ),
    ("\\textbf{}", "textbf{$1}" ),
    ("\\textit{}", "textit{$1}"),

    ("\\bibliographystyle{}", "bibliographystyle{$1}"),
    ("\\bibliography{}", "bibliography{$1}")
]

class LatexPlusAutoCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "text.tex.latex"):
            return None
        default_completions = [(item, ) for item in view.extract_completions(prefix)
                               if len(item) > 3 and valid(item)]
        command_completions = [(item, ) for item in view.extract_completions("\\")
                               if len(item) > 3 and valid(item)]

        r = default_completions + command_completions + general
        if view.match_selector(locations[0], "meta.definition.math.latex"):
            r = r + math
        return r
