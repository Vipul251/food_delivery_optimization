# from fastapi import FastAPI
# import pandas as pd

# app = FastAPI()

# @app.get("/assignments")
# def get_assignments():
#     df = pd.read_csv("../data/synthetic_orders.csv")
#     return df.to_dict(orient="records")

# # Run API:
# # uvicorn app.api:app --reload
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/orders")
def get_orders():
    df_orders = pd.read_csv("data/synthetic_orders.csv")
    return df_orders.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
