
########################################################################################################################
# Project setup
########################################################################################################################

init_env : init_virtualenv load_direnv install precommit_install
	@echo "✅ Environment initialized and ready to use 🔥"

init_virtualenv :
	@echo "Initializing environment ..."
	@if pyenv virtualenvs | grep -q 'titanic'; then \
		echo "Virtualenv 'titanic' already exists"; \
	else \
		echo "Virtualenv 'titanic' does not exist"; \
		echo "Creating virtualenv 'titanic' ..."; \
		pyenv virtualenv 3.10.12 titanic; \
	fi
	@pyenv local titanic
	@echo "✅ Virtualenv 'titanic' activated"

load_direnv:
	@echo "Loading direnv ..."
	@direnv allow
	@echo "✅ Direnv loaded"

precommit_install:
	@echo "Installing pre-commit hooks ..."
	@pre-commit install
	@echo "✅ Pre-commit hooks installed"

install :
	@echo "Installing dependencies ..."
	@pip install --upgrade -q pip
	@pip install -q -r requirements.txt
	@echo "✅ Dependencies installed"
	@echo "Installing local package titanic ..."
	@tree src
	@pip install -q -e .


########################################################################################################################
# Training the model
########################################################################################################################

.PHONY: train
train:
	@echo "Training the model ..."
	python -m titanic.main
	@echo "✅ Model trained"

########################################################################################################################
# API
########################################################################################################################

.PHONY: run_api test_api
run_api:
	@echo "Starting the API ..."
	@echo 'Test the api by clicking on the link :\n'
	@echo 'http://127.0.0.1:$(PORT)/predict/?PassengerId=6145_01&HomePlanet=Europa&CryoSleep=True&Cabin=C%2F231%2FS&Destination=55%20Cancri%20e%09&Age=50&VIP=true&RoomService=2000&FoodCourt=2000&ShoppingMall=2000&Spa=2000&VRDeck=2000&Name=Benebah%20Asolipery'
	uvicorn api.fast:app --reload --port $(PORT)

test_api:
	@echo "Testing the API ..."
	curl -X 'GET' \
  'http://127.0.0.1:$(PORT)/predict/?PassengerId=6145_01&HomePlanet=Europa&CryoSleep=True&Cabin=C%2F231%2FS&Destination=55%20Cancri%20e%09&Age=50&VIP=true&RoomService=2000&FoodCourt=2000&ShoppingMall=2000&Spa=2000&VRDeck=2000&Name=Benebah%20Asolipery' \
  -H 'accept: application/json'
	@echo "✅ API tested"

build_docker_api:
	@echo "Building the API ..."
	docker build -t api --file api/Dockerfile .

run_docker_api:
	@echo "Running the API in a Docker container ..."
	docker run -p $(PORT):$(PORT) --env-file .env api

########################################################################################################################
# Web App
########################################################################################################################

streamlit:
	@echo "Starting the Streamlit app ..."
	streamlit run app/main.py
