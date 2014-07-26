all:

subpush:
		git subtree push --prefix=syntax git@github.com:randy3k/syntax.git master

subpull:
		git subtree pull --prefix=syntax git@github.com:randy3k/LaTeX-Extended.git master --squash
