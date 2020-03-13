help:
	@echo "Usage:"
	@echo "    make help       show this message"
	@echo "    make test       run the test suite"
	@echo "    make black      format code using black"
	@echo "    exit            leave virtual environment"

black:
	black .

test:
	python -m pytest tests

.PHONY: help activate test
