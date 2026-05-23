import torch
from torchvision  import transforms
from PIL import Image #used for opening and processing images
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F #for activation functions like softmax

classes = ['coily', 'curly', 'locs', 'straight', 'wavy'] #classes/folders from dataset

#load MobileNetV2 architecture
model = models.mobilenet_v2(pretrained=False) #false since we will load OUR trained weights
#replace the final layer to match our number of classes
model.classifier[1] = nn.Linear(model.last_channel, len(classes))
#load the trained weights from the training process
model.load_state_dict(torch.load("models/hair_model.pth"))
model.eval() #set model to evaluation mode

#define the image preprocessing steps (same as during training)
transform = transforms.Compose([
    transforms.Resize((224, 224)), #resize to match model input size
    transforms.ToTensor(), #convert to tensor
])

#open the test image and apply the same transformations
image = Image.open("data/raw/wavy/wavy23.jpg").convert("RGB") #path to a test image
image = transform(image)
image = image.unsqueeze(0) #add batch dimension

#turn  off gradients since we are only doing predictions
with torch.no_grad():
    outputs = model(image) #run image through model
    probabilities = F.softmax(outputs, dim=1) #convert outputs to probabilities
    confidence, predicted = torch.max(probabilities, 1) #get predicted class and confidence score

#print prediction and confidence score
print("Prediction: ", classes[predicted.item()])
print ("Confidence: ", round(confidence.item()*100, 2), "%")