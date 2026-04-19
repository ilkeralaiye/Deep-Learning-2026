import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_mean_and_std(dataloader):
    channels_sum, channels_squared_sum, num_batches = 0, 0, 0
    
    for data, _ in dataloader:

        channels_sum += torch.mean(data, dim=[0, 2, 3])
        channels_squared_sum += torch.mean(data ** 2, dim=[0, 2, 3])
        num_batches += 1
    
    mean = channels_sum / num_batches
    
    std = (channels_squared_sum / num_batches - mean ** 2) ** 0.5
    
    return mean, std

# Sadece ToTensor() yerine bir Compose listesi oluşturuyoruz
transform = transforms.Compose([
    transforms.Resize((64, 64)), # Modelinin giriş boyutuna göre burayı değiştirebilirsin
    transforms.ToTensor()          # Normalize işlemini BURAYA EKLEMİYORUZ
])

dataset = datasets.ImageFolder(root='data/desert101/train', transform=transform)

dataloader = DataLoader(dataset, batch_size=32, shuffle=False)

mean, std = get_mean_and_std(dataloader)

print(f"Mean: {mean}")
print(f"Std: {std}")