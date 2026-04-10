from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
import pandas
from typing import Optional

# Importing constants and pipeline modules from the project
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline

# Initialize FastAPI application
app = FastAPI()

# Mount the 'static' directory for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template engine for rendering HTML templates
templates = Jinja2Templates(directory='templates')

# Allow all origins for Cross-Origin Resource Sharing (CORS)
origins = ["*"]

# Configure middleware to handle CORS, allowing requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    """
    DataForm class to handle and process incoming form data.
    This class defines the vehicle-related attributes expected from the form.
    """
    def __init__(self, request: Request):
        self.request: Request = request

        self.Age: Optional[int] = None
        self.Gender: Optional[str] = None
        self.Region_Code: Optional[str] = None
        self.bmi: Optional[float] = None
        self.children: Optional[int] = None
        self.smoker: Optional[str] = None
                

    async def get_vehicle_data(self):
        """
        Method to retrieve and assign form data to class attributes.
        This method is asynchronous to handle form data fetching without blocking.
        """
        form = await self.request.form()
        self.Gender = (form.get("Gender")) if form.get("Gender") else None
        self.Age = int(form.get("Age")) if form.get("Age") else None
        self.Region_Code = (form.get("Region_Code")) if form.get("Region_Code") else None
        self.bmi = float(form.get("bmi"))
        self.children = form.get("children")
        self.smoker = str(form.get("smoker"))

        

# Route to render the main page with the form
@app.get("/", tags=["authentication"])
async def index(request: Request):
    """
    Renders the main HTML form page for vehicle data input.
    """
    return templates.TemplateResponse(name="insurancedata.html",request=request,context={"context": "Rendering"})

# Route to trigger the model training process
@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the model training pipeline.
    """
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")

# Route to handle form submission and make predictions
@app.post("/")
async def predictRouteClient(request: Request):
    """
    Endpoint to receive form data, process it, and make a prediction.
    """
    try:
        form = DataForm(request)
        await form.get_vehicle_data()
        
        vehicle_data = VehicleData(
                                gender=form.Gender,
                                smoker=form.smoker,
                                children=form.children,
                                bmi=form.bmi,
                                age=form.Age,
                                region=form.Region_Code,
                                )

        
        # Convert form data into a DataFrame for the model
        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        # Initialize the prediction pipeline
        model_predictor = VehicleDataClassifier(vehicle_df)
        # Make a prediction and retrieve the result
        value = model_predictor.predict()[0]

        return templates.TemplateResponse(name="insurancedata.html",request=request,context={"context": value})
    
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}

# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)