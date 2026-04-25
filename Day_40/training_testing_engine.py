import torch
from torch import nn

def trainStep(
        model: torch.nn.Module, 
        dataloader: torch.utils.data.DataLoader, 
        loss_fn: torch.nn.Module, optimizer: torch.optim.Optimizer
    ):

    model.train()

    train_loss = 0
    train_acc = 0

    for batch, (X, y) in enumerate(dataloader):

        y_pred = model(X)
        loss = loss_fn(y_pred, y)
        train_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        predictedClass = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
        train_acc += (predictedClass == y).sum().item() / len(y_pred)

    train_loss /= len(dataloader)
    train_acc /= len(dataloader)

    return train_loss, train_acc

def testStep(
        model: torch.nn.Module, 
        dataloader: torch.utils.data.DataLoader, 
        loss_fn: torch.nn.Module,
    ):

    model.eval()
    test_loss = 0
    test_acc = 0

    with torch.inference_mode():
        for batch, (X, y) in enumerate(dataloader):
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            test_loss += loss.item()

            testPredictedLabels = y_pred.argmax(dim=1)
            test_acc += (testPredictedLabels == y).sum().item() / len(y_pred)

    test_loss /= len(dataloader)
    test_acc /= len(dataloader)

    return test_loss, test_acc

def train(
        model: torch.nn.Module, 
        train_dataloader: torch.utils.data.DataLoader, test_dataloader: torch.utils.data.DataLoader, 
        optimizer: torch.optim.Optimizer, loss_fn: torch.nn.Module = nn.CrossEntropyLoss(), epochs: int = 10
    ):

    results = {
        "train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": []
    }

    for epoch in range(epochs):
        train_loss, train_acc = trainStep(model= model, dataloader=train_dataloader, loss_fn=loss_fn, optimizer=optimizer)
        test_loss, test_acc = testStep(model= model, dataloader=test_dataloader, loss_fn=loss_fn, optimizer=optimizer)

        print(f"Epoch: {epoch + 1}, Train loss: {train_loss}, Test loss: {test_loss}, Train acc: {train_acc}, Test acc: {test_acc}")

        results["train_loss"].append(train_loss)
        results["train_acc"].append(train_acc)
        results["test_loss"].append(test_loss)
        results["test_acc"].append(test_acc)

    return results
