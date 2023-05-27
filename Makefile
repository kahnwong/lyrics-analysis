setup:
	pyenv virtualenv 3.11.3 lyrics-analysis
	pyenv local lyrics-analysis
	pip install -r requirements.txt
	# pip install -r requirements-dev.txt
	pip install -e .
