import os

import numpy as np
import torch
from PIL import Image
from matplotlib import pyplot as plt
from torch.utils.data import Dataset
from tqdm import tqdm

from . import *


class TinyImageNetDataset(Dataset):
    """
    Description of TinyImageNetDataset to be made hehe
    """
    def __init__(self, train: bool = False, test: bool = False,
                 val: bool = False, normalise: str = 'He', transform=None):
        if (train + test + val) != 1:
            raise ValueError('Error, specify which dataset to use')
        self.transform = transform
        self.folderMeaning: dict = self._get_folder_meaning()
        self.namesMapped: dict = self._map_names(self.folderMeaning)

        if train:
            self.images, self.labels = self._load_train_data(transform=transform)
        if test:
            self.images, self.labels = self._load_test_data(transform=transform)
        if val:
            self.images, self.labels = self._load_val_data(transform=transform)

    def __size__(self) -> int:
        """
        Description of __size__
        """
        return self.images.shape

    def __len__(self) -> int:
        """
        description of __len__
        """
        return self.images.shape[0]

    def __getitem__(self, index: int) -> dict:
        """
        Description of __getitem__
        """
        pass

    @staticmethod
    def _map_names(names: dict) -> dict:
        """
        Description of _map_names
        """
        index = 0
        mapped = {}
        for folder in names.keys():
            mapped[folder] = index
            index += 1
        return mapped

    @staticmethod
    def _get_folder_meaning() -> dict:
        """
        Description of _get_folder_meaning
        """
        foldersPath = get_dataset_path('IMAGENET') + SLASH + 'train'
        filePath = get_dataset_path('IMAGENET') + SLASH + 'words.txt'
        folder_descriptions = {}
        folder_meaning = {}
        with open(filePath, 'r') as f:
            for line in f:
                folder_name, description = line.strip().split('\t', 1)
                description = description.split(',')[0] if ',' in description else description
                folder_descriptions[folder_name] = description

        for name in os.listdir(foldersPath):
            if name in folder_descriptions:
                folder_meaning[name] = folder_descriptions[name]
        return folder_meaning

    @staticmethod
    def _load_train_data(transform) -> tuple:
        """
        Description of _load_train_data
        """
        print("Loading training images...")
        path = get_dataset_path('IMAGENET') + SLASH + 'train'
        images = []
        labels = []
        i = 0
        for name in tqdm(os.listdir(path)):
            print(name)
            if i == 5:
                break
            folderPath = path + SLASH + name + SLASH + 'images'
            for img in os.listdir(folderPath):
                imgPath = os.path.join(folderPath, img)
                try:
                    image = Image.open(imgPath).convert('RGB')
                    images.append(transform(image))
                    labels.append(name)
                except Exception as e:
                    print(f"Error loading {img}: {e}")
            i += 1
        return torch.stack(images), labels

    @staticmethod
    def _load_test_data(transform) -> tuple:
        """
        Description of _load_test_data
        """
        print("Loading test images...")
        folderPath = get_dataset_path('IMAGENET') + SLASH + 'test' + SLASH + 'images' + SLASH
        images = []
        for img in tqdm(os.listdir(folderPath)):
            imgPath = os.path.join(folderPath, img)
            try:
                image = Image.open(imgPath).convert('RGB')
                images.append(transform(image))
            except Exception as e:
                print(f"Error loading {img}: {e}")
        return torch.stack(images), None

    @staticmethod
    def _load_val_data(transform) -> tuple:
        """
        Description of _load_val_data
        """
        print("Loading validation images...")
        path = get_dataset_path('IMAGENET') + SLASH + 'val' + SLASH
        images = []
        labels = []
        with open(path + 'val_annotations.txt', 'r') as f:
            for line in tqdm(f):
                imgPath = path + SLASH + 'images' + SLASH + line.split("\t")[0]
                try:
                    image = Image.open(imgPath).convert('RGB')
                    images.append(transform(image))
                    labels.append(line.split("\t")[1])
                except Exception as e:
                    print(f"Error loading {imgPath}: {e}")
        return torch.stack(images), labels

    def plot_eight_images(self, random: bool = False):
        """
        Description of plot_eight_images
        """
        plt.figure(figsize=(15, 10))
        indexes = np.array([i for i in range(8)])
        if random:
            indexes = np.random.randint(0, self.images.shape[0], size=8)
        for i in range(len(indexes)):
            plt.subplot(2, 4, i + 1)
            image = self.images[indexes[i]].permute(1, 2, 0).numpy()
            plt.imshow(image)
            if self.labels is not None:
                plt.title(f"Label: {self.folderMeaning[self.labels[indexes[i]]]}")
        plt.tight_layout()
        plt.show()

    def plot_image(self, idx: int) -> None:
        """
        Description of plot_image
        """
        image = self.images[idx]
        image = image.permute(1, 2, 0).numpy()
        plt.imshow(image)
        if self.labels is not None:
            plt.title(self.folderMeaning[self.labels[idx]])
        plt.show()
