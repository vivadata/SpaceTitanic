import pandas as pd
from fastapi import FastAPI

from titanic.data import create_X_y
from titanic.registry import load_model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# PassengerId,HomePlanet,CryoSleep,Cabin,Destination,Age,VIP,RoomService,FoodCourt,ShoppingMall,Spa,VRDeck,Name
# 6145_01,Europa,,C/231/S,55 Cancri e,,False,3478.0,10.0,0.0,105.0,2383.0,Benebah Asolipery
@app.get("/predict/")
def predict(
    PassengerId: str,
    HomePlanet: str,
    CryoSleep: bool,
    Cabin: str,
    Destination: str,
    Age: int,
    VIP: bool,
    RoomService: float,
    FoodCourt: float,
    ShoppingMall: float,
    Spa: float,
    VRDeck: float,
    Name: str,
) -> dict:
    data = pd.DataFrame(
        {
            "PassengerId": [PassengerId],
            "HomePlanet": [HomePlanet],
            "CryoSleep": [CryoSleep],
            "Cabin": [Cabin],
            "Destination": [Destination],
            "Age": [Age],
            "VIP": [VIP],
            "RoomService": [RoomService],
            "FoodCourt": [FoodCourt],
            "ShoppingMall": [ShoppingMall],
            "Spa": [Spa],
            "VRDeck": [VRDeck],
            "Name": [Name],
        }
    )
    preprocess = load_model("preprocessor")
    model = load_model("model")
    # Prepare the data like the training data
    X = create_X_y(data)
    data = preprocess.transform(data)
    prediction = model.predict(data)
    return {
        "prediction": int(prediction[0])
    }  # NB: we HAVE to a return a int not np.int64
