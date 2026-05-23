import torch
import torch.nn as nn
import torchvision.models as models

def get_model(num_classes):
    #load a pre-trained MobileNetV2 model (trained on ImageNet)
    model = models.mobilenet_v2(pretrained=True)

    #replace the final classification layer to maych our datatset
    #original layer outputs 100 classes for ImageNet, we change it to 'num_classes'
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)

    #return thr modified model ready for training/fine-tuning
    return model