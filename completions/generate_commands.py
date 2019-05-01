if __name__ == "__main__":
    import urllib.request
    import re

    def tidy(x):
        if "{}" in x:
            y = x.replace("\\", "")
            y = y.replace("{}{}", "{$1}{$0}")
            y = y.replace("{}", "{$0}")
            return (x, y)
        else:
            return (x, )

    def existed(x, existing):
        for c in existing:
            if x.strip("\\{}") == c[0].strip("\\{}"):
                return True
        return False

    def generate_symbols(url, a="^", b="$", existing_commands=[]):
        response = urllib.request.urlopen(url)
        webContent = response.read().decode("utf8")
        m = re.search(a, webContent)
        m2 = re.search(b, webContent)
        webContent = webContent[m.span()[1]:m2.span()[0]]
        items = list(sorted(set(re.findall(r"\\[a-zA-Z]{2,}(?:(?:\{\})+)?", webContent))))
        return [tidy(item) for item in items if not existed(item, existing_commands)]

    _math_commands = [
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
        ("\\varkappa", ),
        ("\\lambda", ),
        ("\\mu", ),
        ("\\nu", ),
        ("\\xi", ),
        ("\\pi", ),
        ("\\rho", ),
        ("\\varrho", ),
        ("\\sigma", ),
        ("\\varsigma", ),
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

        ("\\big", ),
        ("\\Big", ),
        ("\\bigg", ),
        ("\\Bigg", ),
        ("\\quad", ),
        ("\\qquad", ),
        ("\\nonumber", ),

        ("\\bigcup", ),
        ("\\bigcap", ),

        ("\\mathnormal", ),
        ("\\mathrm", ),
        ("\\mathit", ),
        ("\\mathbf", ),
        ("\\mathsf", ),
        ("\\mathtt", ),
        ("\\mathfrak", ),
        ("\\mathcal", ),
        ("\\mathbb", ),
        ("\\mathscr", ),
        ("\\text{}", "text{$0}"),

        ("\\hat", ),
        ("\\bar", ),
        ("\\tilde", ),
        ("\\widehat{}", "widehat{$0}"),
        ("\\widetilde{}", "widetilde{$0}"),
        ("\\overbrace{}{}", "overbrace{$1}{$0}"),
        ("\\underbrace{}{}", "underbrace{$1}{$0}"),
        ("\\overrightarrow{}", "overrightarrow{$0}"),
        ("\\overleftarrow{}", "overleftarrow{$0}"),
        ("\\longleftarrow",),
        ("\\Longleftarrow",),
        ("\\longrightarrow",),
        ("\\Longrightarrow",),
        ("\\longleftrightarrow",),
        ("\\Longleftrightarrow",),

        ("\\sum_{}^{}", "sum_{$1}^{$0}"),
        ("\\prod_{}^{}", "prod_{$1}^{$0}"),
        ("\\int_{}^{}", "int_{$1}^{$0}"),
        ("\\iint_{}^{}", "iint_{$1}^{$0}"),
        ("\\iiint_{}^{}", "iiint_{$1}^{$0}"),
        ("\\iiiint_{}^{}", "iiiint_{$1}^{$0}"),
        ("\\idotsint{}^{}", "idotsint{$1}^{$0}"),
        ("\\oint_{}^{}", "oint_{$1}^{$0}"),

        ("\\frac{}{}", "frac{$1}{$0}"),
        ("\\binom{}{}", "binom{$1}{$0}"),
        ("\\overset{}{}", "overset{$1}{$0}"),
        ("\\underset{}{}", "underset{$1}{$0}")
    ]

    _general_commands = [
        ("\\usepackage", ),
        ("\\includegraphics", ),
        ("\\part{}", "part{$0}"),
        ("\\part*{}", "part*{$0}"),
        ("\\chapter{}", "chapter{$0}"),
        ("\\chapter*{}", "chapter*{$0}"),
        ("\\section{}", "section{$0}"),
        ("\\section*{}", "section*{$0}"),
        ("\\subsection{}", "subsection{$0}"),
        ("\\subsection*{}", "subsection*{$0}"),
        ("\\subsubsection{}", "subsubsection{$0}"),
        ("\\subsubsection*{}", "subsubsection*{$0}"),

        ("\\underline{}", "underline{$0}"),
        ("\\overline{}", "overline{$0}"),

        ("\\bibliographystyle", ),
        ("\\bibliography", ),
        ("\\addbibresource", )
    ]

    math_commands = _math_commands + \
        generate_symbols('https://en.wikibooks.org/wiki/LaTeX/Mathematics',
                         "Relation Symbols",
                         "\\\\cis",
                         _math_commands)

    general_commands = _general_commands + \
        generate_symbols('https://en.wikibooks.org/wiki/LaTeX/Command_Glossary',
                         "^",
                         "$",
                         math_commands + _general_commands)

    with open("latex_commands.py", "w") as f:
        f.write("math_commands = [\n")
        for i, c in enumerate(math_commands):
            if len(c) == 1:
                f.write("    (\"{}\",)".format(c[0].replace("\\", "\\\\")))
            elif len(c) == 2:
                f.write("    (\"{}\", \"{}\")".format(c[0].replace("\\", "\\\\"), c[1]))
            if i < len(math_commands) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("]\n\n")

        f.write("general_commands = [\n")
        for i, c in enumerate(general_commands):
            if len(c) == 1:
                f.write("    (\"{}\",)".format(c[0].replace("\\", "\\\\")))
            elif len(c) == 2:
                f.write("    (\"{}\", \"{}\")".format(c[0].replace("\\", "\\\\"), c[1]))
            if i < len(general_commands) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("]\n")
