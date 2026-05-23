import torch
import torch.nn as nn
#data visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

#metrics for evaluation
from sklearn.metrics import confusion_matrix, classification_report

from dataset import get_data_loaders
from model import get_model

data_dir = "data/raw"
train_loader, val_loader, classes = get_data_loaders(data_dir)
model = get_model(len(classes))
model.load_state_dict(torch.load("models/hair_model.pth"))
model.eval() #set model to evaluation mode

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

#lists to store predictions and true labels
all_preds = []
all_labels = []

with torch.no_grad():

    #loop through validation data
    for images, labels in val_loader:

        #move data to device
        images, labels = images.to(device), labels.to(device)

        #get model predictions
        outputs = model(images)

        #get predicted class index
        _, predicted = torch.max(outputs, 1)

        #store predictions and true labels for evaluation
        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

#generate confusion matrix
cm = confusion_matrix(all_labels, all_preds)

#create hatmap visualization
plt.figure(figsize=(8, 6))

sns.heatmap(cm, annot=True, fmt="d", xticklabels=classes, yticklabels=classes)

#axis labels and title
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix for Hair Type Classification")
plt.show() #show plot

#print detailed classification metrics
print("\nClassification Report:\n")

print(classification_report(all_labels, all_preds, target_names=classes))