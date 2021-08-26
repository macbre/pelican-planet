check:
	# pylint *.py tests/
	pytest --cov=pelican_planet --cov-report=term --cov-report=xml --cov-fail-under=80 -vv

black:
	black .
