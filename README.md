This repo is a proposed solution to the **"Data Engineering Challenge"**  first step on the Titanic kaggle competition.


## Setup

First copy the `.env.sample` file to `.env` and fill in the values.

```bash
cp .env.sample .env
```

Then download your service account key from Google Cloud Platform and save it as `credentials/service-account.json`.

Once this is done and if you are using `pyenv-virtualenv` you can run the following command to setup the project.

```bash
make init_env
```

## Running the pipeline

To run the pipeline you can use the following command:

```bash
make train
```

## Web application and API

Launch the api in local with :

```bash
make run_api
```

You should test it by following the link that will be displayed in the terminal.
Don't hesitate to go the `/docs` endpoint to see the documentation of the API.
You can also test the API with the `make test_api` rule in another terminal.

Finally launch the streamlit app with :

```bash
make streamlit
```
