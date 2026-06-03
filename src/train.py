import torch
import torch.nn as nn
import torch.optim as optim
from dataset import get_data_loaders
from model import get_model

#PATH to the dataset folder
data_dir = "data/raw"

#load training and validation + class labels
train_loader, val_loader, classes = get_data_loaders(data_dir)

#initialize model with correct number of output classes
model = get_model(len(classes))

#use GPU if available, otherwise fallback to CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

#loss function for multi-class classification
criterion = nn.CrossEntropyLoss()

#optimizer for updating model parameters during training
optimizr = optim.Adam(model.parameters(), lr=0.0003)

#number of epochs to train the model
epochs = 20

for epoch in range(epochs):
    model.train() #set model to training mode
    train_loss = 0 #track loss for the epoch

    #loop through batches of training data
    for images, labels in train_loader:
        
        images, labels = images.to(device), labels.to(device) #move data to the same device as the model

        optimizr.zero_grad() #rest gradients from prev steps
        
        outputs = model(images) #forward pass to get model predictions

        loss = criterion(outputs, labels) #compute loss between predictions and true labels

        loss.backward() #backpropagate to compute gradients
        optimizr.step() #update model parameters based on gradients
        train_loss += loss.item() #accumulate loss for the epoch


#  VALIDATION PHASE

#put model in evaluation mode
model.eval()

correct, total, val_loss = 0, 0, 0

#turn off gradients since we are only evaluating
with torch.no_grad():
    for images, labels in val_loader:

        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        val_loss += loss.item()

        #get predicted class
        _, predicted = torch.max(outputs, 1)

        #count total labels
        total += labels.size(0)

        #count correct predictions
        correct += (predicted == labels).sum().item()

#calc accuracy
accuracy = 100*correct/total

#print results
print(f"Epoch {epoch+1}/{epochs}, Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {accuracy:.2f}%")

#save trained model weights
torch.save(model.state_dict(), "models/hair_model.pth")

print("\nTraining complete!")
