LaTeXZeta
=====

This package is NOT a replacement of any LaTeX package. It is meant to be used together with [LaTeXTools](https://github.com/SublimeText/LaTeXTools) (or similar package) and to improve the typing experience with Sublime Text by providing a bunch of keybinds and helper functions.

## Installation

Package Control.

## Backslash triggered completions

It provides a list of commands to auto complete when <kbd>&#92;</kbd> is triggered.

<img width="412" src="https://cloud.githubusercontent.com/assets/1690993/20915374/743dfcd2-bb53-11e6-9e29-a1af80356405.png">


## Auto match pairs

<img width="412" src="https://cloud.githubusercontent.com/assets/1690993/20943620/4af2f0dc-bbce-11e6-88df-759df58e33da.gif">



The following auto paring is activated when `auto_match_enabled` is `true`.

* Auto pairing `\(\)`, `\[\]` and `\{\}`.
* Single and double quotation marks are replaced by the LaTeX quotation pairs, e.g., `'foo'` becomes <code>&#96;foo'</code> and `"foo"` becomes <code>&#96;&#96;foo''</code>. The <code>&#96;</code> to <code>&#96;'</code> auto completion in LaTeXTools is disabled.

* In math environment,

Keys                                                 | Mappings
--------                                             | -----------------
<kbd>(</kbd>,<kbd>(</kbd>                            | `\left(\right)`
<kbd>[</kbd>,<kbd>[</kbd>                            | `\left[\right]`
<kbd>&#92;</kbd>,<kbd>{</kbd>,<kbd>{</kbd>           | `\left\{\right\}`
<kbd>&#92;</kbd>,<kbd>&#124;</kbd>                   | `\|\|`
<kbd>&#92;</kbd>,<kbd>&#124;</kbd>,<kbd>&#124;</kbd> | `\left\|\right\|`
<kbd>&#92;</kbd>,<kbd>&lt;</kbd>                     | `\langle \rangle`
<kbd>&#92;</kbd>,<kbd>&lt;</kbd>,<kbd>&lt;</kbd>     | `\left\langle \right\rangle`


- If any text is highlighted, auto matching pair wraps the selection.
- Some pairs will create fields. The cursor will move to the end of the pair when pressing `tab`.

## Auto complete math commands

Math commands are only valid in math environment, eg, `$$`, <code>&#92;[&#92;]</code> or `\begin{equation}`, `\end{equation}`.
These Math keybinds are similar (not exactly the same) to [vim-latex](http://vim-latex.sourceforge.net/documentation/latex-suite.html#auc-tex-mappings) plugin.

_Note: Some math commands will create fields. The cursor will move to next field when pressing `tab`._

### Math symbols

Keys                                                                     | Mappings
--------                                                                 | -----------------
<kbd>_ </kbd>,<kbd>_ </kbd>                                                | `_{}`
<kbd>^</kbd>,<kbd>^</kbd>                                                | `^{}`
<kbd>\`</kbd>,<kbd>_</kbd>                                               | `\bar{}`
<kbd>_ </kbd> (with text highlighted)                                     | `\bar{SELECTION}`
<kbd>_ </kbd>,<kbd>_ </kbd> (with text highlighted)                        | `\overline{SELECTION}`
<kbd>\`</kbd>,<kbd>_ </kbd>                                               | `\hat{}`
<kbd>^</kbd> (with text highlighted)                                     | `\hat{SELECTION}`
<kbd>^</kbd>, <kbd>^</kbd> (with text highlighted)                       | `\widehat{SELECTION}`
<kbd>.</kbd>,<kbd>.</kbd>,<kbd>.</kbd>                                   | `\ldots`
<kbd>\`</kbd>,<kbd>,</kbd>                                               | `\nonumber`
<kbd>\`</kbd>,<kbd>/</kbd>                                               | `\frac{}{}`
<kbd>/</kbd> (with text highlighted)                                     | `\frac{SELECTION}{}`
<kbd>\`</kbd>,<kbd>0</kbd>                                               | `\varnothing`
<kbd>\`</kbd>,<kbd>2</kbd>                                               | `\sqrt{}`
<kbd>\`</kbd>,<kbd>6</kbd>                                               | `\partial`
<kbd>\`</kbd>,<kbd>8</kbd>                                               | `\infity`

Keys                                                                     | Mappings
--------                                                                 | -----------------
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>tab</kbd>                              | `\leftarrow`
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>-</kbd>,<kbd>tab</kbd>                 | `\longleftarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>tab</kbd>                              | `\Leftarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>=</kbd>,<kbd>tab</kbd>                 | `\Longleftarrow`
<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd>                              | `\rightarrow`
<kbd>-</kbd>,<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd>                 | `\longrightarrow`
<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd>                              | `\Rightarrow`
<kbd>=</kbd>,<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd>                 | `\Longrightarrow`
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd>              | `\leftrightarrow`
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd> | `\longleftrightarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd>              | `\Leftrightarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>tab</kbd> | `\Longleftrightarrow`

### Greek letters

Keys                       | Mappings          | Keys                       | Mappings          | Keys                       | Mappings          |
--------                   | ----------------- | --------                   | ----------------- | --------                   | ----------------- |
<kbd>\`</kbd>,<kbd>a</kbd> | `\alpha`          | <kbd>\`</kbd>,<kbd>i</kbd> | `\iota`           | <kbd>\`</kbd>,<kbd>s</kbd> | `\sigma`          |
<kbd>\`</kbd>,<kbd>b</kbd> | `\beta`           | <kbd>\`</kbd>,<kbd>k</kbd> | `\kappa`          | <kbd>\`</kbd>,<kbd>t</kbd> | `\tau`            |
<kbd>\`</kbd>,<kbd>g</kbd> | `\gamma`          | <kbd>\`</kbd>,<kbd>l</kbd> | `\lambda`         | <kbd>\`</kbd>,<kbd>u</kbd> | `\upsilon`        |
<kbd>\`</kbd>,<kbd>d</kbd> | `\delta`          | <kbd>\`</kbd>,<kbd>m</kbd> | `\mu`             | <kbd>\`</kbd>,<kbd>f</kbd> | `\varphi`         |
<kbd>\`</kbd>,<kbd>e</kbd> | `\varepsilon`     | <kbd>\`</kbd>,<kbd>n</kbd> | `\nu`             | <kbd>\`</kbd>,<kbd>c</kbd> | `\chi`            |
<kbd>\`</kbd>,<kbd>z</kbd> | `\zeta`           | <kbd>\`</kbd>,<kbd>x</kbd> | `\xi`             | <kbd>\`</kbd>,<kbd>y</kbd> | `\psi`            |
<kbd>\`</kbd>,<kbd>h</kbd> | `\eta`            | <kbd>\`</kbd>,<kbd>p</kbd> | `\pi`             | <kbd>\`</kbd>,<kbd>w</kbd> | `\omega`          |
<kbd>\`</kbd>,<kbd>q</kbd> | `\theta`          | <kbd>\`</kbd>,<kbd>r</kbd> | `\rho`            |                            |                   |


Keys                       | Mappings
--------                   | -----------------
<kbd>\`</kbd>,<kbd>G</kbd> | `\Gamma`
<kbd>\`</kbd>,<kbd>D</kbd> | `\Delta`
<kbd>\`</kbd>,<kbd>Q</kbd> | `\Theta`
<kbd>\`</kbd>,<kbd>L</kbd> | `\Lambda`
<kbd>\`</kbd>,<kbd>X</kbd> | `\Xi`
<kbd>\`</kbd>,<kbd>P</kbd> | `\Pi`
<kbd>\`</kbd>,<kbd>S</kbd> | `\Sigma`
<kbd>\`</kbd>,<kbd>Y</kbd> | `\Upsilon`
<kbd>\`</kbd>,<kbd>F</kbd> | `\Phi`
<kbd>\`</kbd>,<kbd>Y</kbd> | `\Psi`
<kbd>\`</kbd>,<kbd>W</kbd> | `\Omega`

More symbols will be defined in further versions


## Others

- <kbd>C</kbd>+<kbd>l</kbd>, <kbd>c</kbd>  - wrap the selection into by a command
- <kbd>C</kbd>+<kbd>l</kbd>, <kbd>e</kbd>  - wrap the selection into by a environment

- `LaTeXZeta: Install Jump to Pdf Mousebinding` ([LaTeXTools](https://github.com/SublimeText/LaTeXTools))
    - <kbd>C</kbd>+<kbd>Shift</kbd>+<kbd>Click</kbd>  - jump to and forward sync with the pdf file

- `LaTeXZeta: Toggle Auto Set Preview Math Template Preamble` ([LaTeXTools](https://github.com/SublimeText/LaTeXTools))
    - When set `True`, `\newcommand` commands  in the current file are included when previewing math.

- `LaTeXZeta: Install BracketHighlighter Settings` ([BracketHighlighter](https://github.com/facelessuser/BracketHighlighter))
    - ![](https://cloud.githubusercontent.com/assets/1690993/20913762/73e6a24e-bb48-11e6-8bdd-b3cd6c6f652a.png)