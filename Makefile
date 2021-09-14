check:
	# pylint *.py tests/

	# run ./test-server.sh before executing this one
	pytest --cov=pelican_planet --cov-report=term --cov-report=xml --cov-fail-under=80 -vv

black:
	black .
