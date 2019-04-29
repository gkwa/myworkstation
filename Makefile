prep:
	@./main.py

clean:
	@rm -f playbook*.yml
	@rm -f Brewfile[0-9]* Brewfile
	@rm -f .travis.yml
	@rm -f azure-pipelines.yml
	@rm -rf __pycache__
