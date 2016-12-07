if __name__ == "__main__":
    import urllib.request
    import re

    def tidy(x):
        if "{}" in x:
            y = x.replace("\\", "")
            y = y.replace("{}{}", "{$1}{$2}")
            y = y.replace("{}", "{$1}")
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
        ("\\text{}", "text{$1}"),

        ("\\hat", ),
        ("\\bar", ),
        ("\\tilde", ),
        ("\\widehat{}", "widehat{$1}"),
        ("\\widetilde{}", "widetilde{$1}"),
        ("\\overbrace{}{}", "overbrace{$1}{$2}"),
        ("\\underbrace{}{}", "underbrace{$1}{$2}"),
        ("\\overrightarrow{}", "overrightarrow{$1}"),
        ("\\overleftarrow{}", "overleftarrow{$1}"),

        ("\\sum_{}^{}", "sum_{$1}^{$2}"),
        ("\\prod_{}^{}", "prod_{$1}^{$2}"),
        ("\\int_{}^{}", "int_{$1}^{$2}"),
        ("\\iint_{}^{}", "iint_{$1}^{$2}"),
        ("\\iiint_{}^{}", "iiint_{$1}^{$2}"),
        ("\\iiiint_{}^{}", "iiiint_{$1}^{$2}"),
        ("\\idotsint{}^{}", "idotsint{$1}^{$2}"),
        ("\\oint_{}^{}", "oint_{$1}^{$2}"),

        ("\\frac{}{}", "frac{$1}{$2}"),
        ("\\binom{}{}", "binom{$1}{$2}"),
        ("\\overset{}{}", "overset{$1}{$2}"),
        ("\\underset{}{}", "underset{$1}{$2}")
    ]

    _general_commands = [
        ("\\usagepacage", ),
        ("\\includegraphics", ),
        ("\\part{}", "part{$1}"),
        ("\\part*{}", "part*{$1}"),
        ("\\chapter{}", "chapter{$1}"),
        ("\\chapter*{}", "chapter*{$1}"),
        ("\\section{}", "section{$1}"),
        ("\\section*{}", "section*{$1}"),
        ("\\subsection{}", "subsection{$1}"),
        ("\\subsection*{}", "subsection*{$1}"),
        ("\\subsubsection{}", "subsubsection{$1}"),
        ("\\subsubsection*{}", "subsubsection*{$1}"),

        ("\\underline{}", "underline{$1}"),
        ("\\overline{}", "overline{$1}"),

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
