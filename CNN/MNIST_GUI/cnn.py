import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm

from DataHandlers.Mnist import MnistDataset


class CNN(nn.Module):
    def __init__(self, batch_size: int, epochs: int, kind: str = 'Classic'):
        super(CNN, self).__init__()
        self.train_set = MnistDataset(kind=kind, train=True)
        self.test_set = MnistDataset(kind=kind, test=True)

        self.epochs = epochs
        self.batch_size = batch_size
        self.num_classes = self.train_set.num_classes()

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        self.fc1 = nn.Linear(128 * 7 * 7, 2048)  # Fully connected layer
        self.fc2 = nn.Linear(2048, 1024)
        self.fc3 = nn.Linear(1024, 512)
        self.fc4 = nn.Linear(512, 256)
        self.fc5 = nn.Linear(256, self.num_classes)  # Output layer for 10 classes

        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)
        print(self.device)

    def forward(self, x):
        # Define the forward pass
        x = self.pool(F.relu(self.conv1(x)))  # Convolution -> ReLU -> MaxPooling
        x = self.pool(F.relu(self.conv2(x)))  # Convolution -> ReLU -> MaxPooling
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = x.view(-1, 128 * 7 * 7)  # Flatten the tensor for the fully connected layer
        x = F.relu(self.fc1(x))  # Fully connected layer with ReLU
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))  # Fully connected layer with ReLU
        x = F.relu(self.fc4(x))
        return self.fc5(x)

    def train_model(self) -> None:
        start = time.time()
        train_loader = self.train_set.get_data_loader(batch_size=64, shuffle=False)
        for epoch in range(self.epochs):
            self.train()
            running_loss = 0.0
            for images, labels in tqdm(train_loader, desc=f'Epoch {epoch + 1}/{self.epochs}: '):
                images, labels = images.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                outputs = self(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
            print(f'  Loss: {running_loss / len(train_loader):.4f}')
            self.test_model()
        print('Training completed.')
        end = time.time()
        duration = end - start
        print(f"Program took {duration:.4f} seconds to run.")

    def test_model(self) -> None:
        test_loader = self.test_set.get_data_loader(batch_size=64, shuffle=False)
        self.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in tqdm(test_loader, desc='Testing network: '):
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
        print(f'Accuracy of the model on the test set: {accuracy:.2f}%')

    def save_model(self, dirPath: str) -> None:
        torch.save(self.state_dict(), dirPath + '\\Model4.pth')

    def load_model(self, dirPath: str) -> None:
        self.load_state_dict(torch.load(dirPath + '\\Model4.pth'))

    def predict(self, image):
        self.eval()
        image = torch.tensor(image).float().unsqueeze(0)
        with torch.no_grad():
            output = self(image)
            _, predicted = torch.max(output.data, 1)
        return predicted
