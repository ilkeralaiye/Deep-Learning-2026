import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

NUM_WORKERS = os.cpu_count()

def createDataLoaders(train_dir:str, test_dir: str, transform: transforms.Compose, batch_size:int, num_workers: int = NUM_WORKERS):
    train_dataset = datasets.ImageFolder(root = train_dir, transform=transform, target_transform=None)
    test_dataset = datasets.ImageFolder(root = test_dir, transform=transform)

    classNames = train_dataset.classes

    train_dataloader = DataLoader(dataset= train_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=True)
    test_dataloader = DataLoader(dataset= test_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)

    return train_dataloader, test_dataloader, classNames

