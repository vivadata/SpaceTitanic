FROM python:3.10-slim


# Copy the current directory contents into the container at /api
WORKDIR /api
COPY api/requirements .

# Web requirements
RUN pip install -r requirements.txt
# This is a workaround to install the library
# because the library is not in the pypi repository
COPY src src
COPY pyproject.toml .
# This will overwrite the requirements.txt file but we used the first one already
COPY requirements.txt .
RUN pip install .

# Copying the rest of the files after the dependencies installation
COPY api .

# COPY CREDENTIALS
COPY credentials credentials


CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
