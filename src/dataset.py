import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

#func to create training and validation data loaders
def get_data_loaders(data_dir, batch_size=32):

    #define the image preprocessing steps
    #resize the images to 224x224, convert to tensor
    transform = transforms.Compose([

        # Resize all images
        transforms.Resize((224, 224)),

        # Randomly flip images horizontally
        transforms.RandomHorizontalFlip(),

        # Slight random rotation
        transforms.RandomRotation(10),

        # Random zoom/crop effect
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),

        # Convert image to tensor
        transforms.ToTensor(),

        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
        )
    ])

    #load the dataset from the specified directory
    dataset = datasets.ImageFolder(root=data_dir, transform=transform)

    #compute the number of samples for training and validation
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    #split the dataset into training and validation sets
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    #create data loaders for training and validation sets
    #shuffle the training data for better generalization
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    #validation data loader does not need to be shuffled
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, dataset.classes #return loaders + class names for label mapping