SHELL=/bin/bash
CMD_ACTIVATE_VENV = source .venv/bin/activate
PYTHON_VERSION=3.10


run:
	@( \
		$(CMD_ACTIVATE_VENV) || exit 1; \
		streamlit run app.py; \
	)