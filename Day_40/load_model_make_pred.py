from model_creation import DesertClassifier
from torchvision import transforms, io
import torch
import setup_data

MODEL_SAVE_PATH = "models/desert_classifier.pth"
NUM_EPOCHS = 10
BATCH_SIZE = 32
HIDDEN_UNITS = 32
LEARNING_RATE = 0.001

train_dir = "data/desert101/train"
test_dir = "data/desert101/test"

dataTransform = transforms.Compose(
    [
        transforms.Resize((64, 64)),
        transforms.Normalize(mean = [0.5482, 0.4636, 0.3866], std = [0.2540, 0.2574, 0.2628])

    ]
)

train_dataloader, test_dataloader, classnames = setup_data.createDataLoaders(train_dir=train_dir, test_dir=test_dir, transform=dataTransform, batch_size=BATCH_SIZE)

loaded_model = DesertClassifier(input_shape=3, hidden_units=HIDDEN_UNITS, output_shape=len(classnames))

loaded_model.load_state_dict(torch.load(MODEL_SAVE_PATH))

from pathlib import Path

data_path = Path("data/")

online_image_path = data_path / "baklava.jpg"
single_image = io.read_image(str(online_image_path)).type(torch.float32) / 255

single_image_transform = transforms.Compose([
    transforms.Resize(size=(64, 64))
])
single_image = single_image_transform(single_image).unsqueeze(dim=0)

loaded_model.eval()
with torch.inference_mode():
    logits = loaded_model(single_image)
    probs = torch.softmax(logits, dim=1)
    pred_idx = probs.argmax(dim=1).item()

print("Predicted class: " + classnames[pred_idx])