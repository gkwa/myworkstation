test: FORCE
	rm -f test/Brewfile*
	python test/main.py
	perl -i -ne 'print if(!m{cask.*virtualbox.*} and !m{^mas })' test/Brewfile*

FORCE: