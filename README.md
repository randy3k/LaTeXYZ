LaTeXZeta
=====

## Installation

Package Control.

## Use mouse click to jump to pdf

<kbd>C</kbd>+<kbd>Shift</kbd>+<kbd>Click</kbd>  - jump to and forward sync with the pdf file (if [LaTeXTools](https://github.com/SublimeText/LaTeXTools) is installed)

## AutoMatch Pairs
The following is activated when `auto_match_enabled` is `true`.

* The following pairs are auto matched: `()`, `\(\)`, `\[\]` and `\{\}`.
* Single and double quotation marks are replaced by the LaTeX quotation pairs, e.g., `'foo'` becomes <code>&#96;foo'</code> and `"foo"` becomes <code>&#96;&#96;foo''</code>.
* In Math mode,

Keys                                                 | Mappings
--------                                             | -----------------
<kbd>(</kbd>,<kbd>(</kbd>                            | `\left(\right)`
<kbd>[</kbd>,<kbd>[</kbd>                            | `\left[\right]`
<kbd>&#92;</kbd>,<kbd>{</kbd>,<kbd>{</kbd>           | `\left\{\right\}`
<kbd>&#92;</kbd>,<kbd>&#124;</kbd>                   | `\|\|`
<kbd>&#92;</kbd>,<kbd>&#124;</kbd>,<kbd>&#124;</kbd> | `\left\|\right\|`
<kbd>&#92;</kbd>,<kbd>&lt;</kbd>                     | `\langle\rangle`
<kbd>&#92;</kbd>,<kbd>&lt;</kbd>,<kbd>&lt;</kbd>     | `\left\langle\right\rangle`


_Note: Some pairs will create fields. The cursor will move to the end of the pair when pressing `tab`._

## AutoComplete Math Commands

Math Commands are only valid in math environment, eg, $$, &#92;[ &#92;] or \begin{equation},
\end{equation}.
These Math Commands are similar to those of vim-latex plugin (if you know what I am talking about).

_Note: Math Commands will create fields. The cursor will move to next field when pressing `tab`._

###Math Symbols

Keys                                   | Mappings
--------                               | -----------------
<kbd>_ </kbd>,<kbd>_</kbd>             | `_{}`
<kbd>^</kbd>,<kbd>^</kbd>              | `^{}`
<kbd>.</kbd>,<kbd>.</kbd>,<kbd>.</kbd> | `\ldots`
<kbd>\`</kbd>,<kbd>/</kbd>             | `\frac{}{}`
<kbd>\`</kbd>,<kbd>0</kbd>             | `\varnothing`
<kbd>\`</kbd>,<kbd>2</kbd>             | `\sqrt{}`
<kbd>\`</kbd>,<kbd>6</kbd>             | `\partial`
<kbd>\`</kbd>,<kbd>8</kbd>             | `\infity`

Keys                                                                             | Mappings
--------                                                                         | -----------------
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>&lt;tab&gt;</kbd>                              | `\leftarrow`
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>-</kbd>,<kbd>&lt;tab&gt;</kbd>                 | `\longleftarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>&lt;tab&gt;</kbd>                              | `\Leftarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>=</kbd>,<kbd>&lt;tab&gt;</kbd>                 | `\Longleftarrow`
<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd>                              | `\rightarrow`
<kbd>-</kbd>,<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd>                 | `\longrightarrow`
<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd>                              | `\Rightarrow`
<kbd>=</kbd>,<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd>                 | `\Longrightarrow`
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd>              | `\leftrightarrow`
<kbd>&lt;</kbd>,<kbd>-</kbd>,<kbd>-</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd> | `\longleftrightarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd>              | `\Leftrightarrow`
<kbd>&lt;</kbd>,<kbd>=</kbd>,<kbd>=</kbd>,<kbd>&gt;</kbd>,<kbd>&lt;tab&gt;</kbd> | `\Longleftrightarrow`

###Greek letters

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
