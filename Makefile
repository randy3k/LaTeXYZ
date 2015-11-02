all:

subpush:
		git subtree push --prefix=syntax git@github.com:randy3k/LaTeX-Plus-Syntax.git master

subpull:
		git subtree pull --prefix=syntax git@github.com:randy3k/LaTeX-Plus-Syntax.git master --squash
