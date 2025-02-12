import os

import requests
import streamlit as st

BACKEND_URL = os.environ.get(
    "BACKEND_URL", f"http://localhost:{os.environ.get('PORT','5555')}"
)
print(BACKEND_URL)

st.title("Space Titanic Survival Prediction")

st.header("Enter Passenger Details")

PassengerId = st.text_input("Passenger ID", value="6145_01")
HomePlanet = st.selectbox("Home Planet", ["Earth", "Europa", "Mars"], index=1)
CryoSleep = st.selectbox("Cryo Sleep", [True, False])
Cabin = st.text_input("Cabin", value="C/231/S")
Destination = st.selectbox(
    "Destination", ["TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"]
)
Age = st.number_input("Age", min_value=0, max_value=100, value=25)
VIP = st.selectbox("VIP", [True, False])
RoomService = st.number_input("Room Service", min_value=0, value=0)
FoodCourt = st.number_input("Food Court", min_value=0, value=0)
ShoppingMall = st.number_input("Shopping Mall", min_value=0, value=0)
Spa = st.number_input("Spa", min_value=0, value=0)
VRDeck = st.number_input("VR Deck", min_value=0, value=0)
Name = st.text_input("Name", value="Bob")


if st.button("Predict"):
    params = {
        "PassengerId": PassengerId,
        "HomePlanet": HomePlanet,
        "CryoSleep": CryoSleep,
        "Cabin": Cabin,
        "Destination": Destination,
        "Age": Age,
        "VIP": VIP,
        "RoomService": RoomService,
        "FoodCourt": FoodCourt,
        "ShoppingMall": ShoppingMall,
        "Spa": Spa,
        "VRDeck": VRDeck,
        "Name": Name,
    }
    response = requests.get(f"{BACKEND_URL}/predict", params=params)
    if response.status_code == 200:
        prediction = response.json().get("prediction")
        st.success(
            f'The passenger will {"live happily and code for many year " if not prediction else "be transported to another dimension"}.'
        )

        if prediction == 1:
            st.image(
                "https://cdn.mos.cms.futurecdn.net/yMquMe4srNd7YKaBJUmqw6-1200-80.png.webp",
                use_container_width=True,
            )
        else:
            st.image("app/image/pro-grammer.jpg", use_container_width=True)

    else:
        st.error("Something went wrong. Please try again.")
