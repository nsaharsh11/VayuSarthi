PYTHON ?= python

.PHONY: setup data-check gen-demo ingest train eval-dev eval-report e2e api test precompute clean app

setup data-check gen-demo ingest train eval-dev eval-report e2e api test precompute clean:
	$(PYTHON) scripts/tasks.py $@
# Vayu Sarthi local Streamlit entry point.
app:
	$(PYTHON) scripts/tasks.py app

.PHONY: validation
validation:
	$(PYTHON) scripts/tasks.py validation
