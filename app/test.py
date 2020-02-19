from ResNet import *
from Config import *

from torch.autograd import Variable
import torchvision.transforms.functional as F

import os
import torch
import matplotlib.pyplot as plt
from PIL import Image

# choose gpu
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def test():

    # initialize training configuration
    config = Config()

    net = resnet50(num_classes = config.classes).to(device)

    net.load_state_dict(torch.load(os.path.join(config.net_base_path, config.net))['model'])
    net = net.to(device)

    # evaluation mode
    net.eval()

    img = Image.open(config.test_base_path)
    img_resize = img.resize((224,224))
    img_tensor = F.to_tensor(img_resize).unsqueeze(0)

    img_features = net.forward(Variable(img_tensor).to(device))

    score, predicted = torch.max(img_features, 1)

    if score < config.threshold:
        print("Out of Bound")

    print(img_features)
    print(config.test_base_path)
    print(config.accuracy[predicted])


if __name__ == "__main__":

    test()