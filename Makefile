test: FORCE
	rm -f test/Brewfile*
	python test/main.py

FORCE: