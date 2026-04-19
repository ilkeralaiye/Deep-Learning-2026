from setup_data import createDataLoaders
from model_creation import DesertClassifier
from training_testing_engine import *
from utils import save_model
import setup_data
from torchvision import transforms

# createDataLoaders()
# classifier = DesertClassifier()

def main():

    NUM_EPOCHS = 10
    BATCH_SIZE = 32
    HIDDEN_UNITS = 32
    LEARNING_RATE = 0.001

    train_dir = "data/desert101/train"
    test_dir = "data/desert101/test"

    dataTransform = transforms.Compose(
        [
            transforms.Resize((64, 64)),
            transforms.RandomHorizontalFlip(p=0.4),
            transforms.TrivialAugmentWide(),
            transforms.ToTensor(),
            transforms.Normalize(mean = [0.5482, 0.4636, 0.3866], std = [0.2540, 0.2574, 0.2628])

        ]
    )

    train_dataloader, test_dataloader, classnames = setup_data.createDataLoaders(train_dir=train_dir, test_dir=test_dir, transform=dataTransform, batch_size=BATCH_SIZE)

    model = DesertClassifier(input_shape=3, hidden_units=HIDDEN_UNITS, output_shape=len(classnames))
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), LEARNING_RATE)

    results = train(model=model, train_dataloader=train_dataloader, test_dataloader=test_dataloader, optimizer=optimizer, loss_fn=loss_fn, epochs=NUM_EPOCHS)

    print(f"\n\nFinal results: {results}\n\n")

    save_model(model, target_dir="models", model_name="desert_classifier.pth")

if __name__ == "__main__":
    # torch.multiprocessing.set_start_method("spawn", force=True)    
    main()