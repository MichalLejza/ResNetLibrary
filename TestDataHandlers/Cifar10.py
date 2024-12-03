from torchvision import transforms
from DataHandlers import Cifar10Dataset


if __name__ == '__main__':
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor()
    ])
    dataset = Cifar10Dataset(train=True, transform=transform)
    print(dataset)
