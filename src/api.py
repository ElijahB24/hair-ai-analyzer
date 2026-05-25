from fastapi import FastAPI, File, UploadFile #FastAPI framework
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #create FastAPI app
# Enable frontend-backend communication
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

#PyTorch
import torch
import torch.nn.functional as F

from PIL import Image #image processing library
from torchvision import transforms #Torchvision transforms
from src.model import get_model #model loader
import io #IO for reading uploaded files

#app = FastAPI() #create FastAPI app

classes = ['coily', 'curly', 'locs', 'straight', 'wavy'] #classes/folders from dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #use GPU if available

model = get_model(len(classes)) #initialize model architecture
model.load_state_dict(torch.load("models/hair_model.pth", map_location=device)) #load trained weights
model.to(device) #move model to device
model.eval() #set model to evaluation mode

#image transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)), #resize to match model input size
    transforms.ToTensor(), #convert to tensor
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

#home route
@app.get("/")
def home():
    return {
        "message": "Hair AI Analyzer API Running"
    }

#prediction route
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    #read uploaded images
    image_bytes = await file.read() #read file bytes

    #convert bytes into image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    #apply transformations
    image = transform(image)

    #add batch dimension
    image = image.unsqueeze(0).to(device)

    #disable gradients
    with torch.no_grad():

        #get model outputs
        outputs = model(image)

        #convert to probabilities
        probabilities = F.softmax(outputs, dim=1)

        #highest confidence prediction
        confidence, predicted = torch.max(probabilities, 1)

    #return JSON response
    return {
        "prediction": classes[predicted.item()],
        "confidence": round(confidence.item() * 100, 2) #confidence as percentage
    }