import torch

from flogo.discovery.hyperparameters.loss import Loss
from flogo.discovery.hyperparameters.optimizer import Optimizer
from flogo.discovery.regularization.early_stopping import EarlyStopping


class ForwardTrainer:
    def __init__(self, epochs: int, model, training_dataset, validation_dataset, loss_function: Loss, optimizer: Optimizer, early_stopping: EarlyStopping):
        self.epochs = epochs
        self.model = model
        self.training_dataset = training_dataset
        self.validation_dataset = validation_dataset
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.early_stopping = early_stopping

    def train(self):
        hit = 0
        for epoch in range(self.epochs):
            self.model.train(True)
            loss = self.__train_model()
            self.model.train(False)
            vloss, hit = self.__validate_model()
            self.__log_epoch_losses(epoch, loss, vloss)
            self.__log_epoch_accuracy(epoch, hit)
            if not self.early_stopping.check(self.__to_percentage(hit, len(self.validation_dataset)), vloss):
                return self.model
                #return self.__to_percentage(hit, len(self.validation_dataset))
        return self.model

    def __train_model(self):
        running_loss = 0.
        for i, entry in enumerate(self.training_dataset, start=1):
            inputs, labels = entry.get_inputs(), entry.get_outputs()
            preds = self.__evaluate(inputs)
            loss = self.loss_function.compute(preds, labels)
            loss.backward()
            running_loss += loss.item()
            self.optimizer.step()
        return self.__epoch_average_loss(running_loss)

    def __validate_model(self):
        running_loss = 0.
        hit = 0
        for i, entry in enumerate(self.validation_dataset, start=1):
            inputs, labels = entry.get_inputs(), entry.get_outputs()
            preds = self.__evaluate(inputs)
            running_loss += self.loss_function.compute(preds, labels).item()
            hit += self.__compute_accuracy(preds, labels)
        return self.__epoch_average_loss(running_loss), hit

    def __evaluate(self, inputs):
        return self.model(inputs)

    def __log_epoch_losses(self, epoch, train_loss, val_loss):
        print('Epoch {} Training - Validation Loss: Training = {}, Validation = {}'.format(epoch + 1, train_loss, val_loss))

    def __epoch_average_loss(self, loss):
        return loss / self.epochs

    def __compute_accuracy(self, preds, labels):
        return torch.sum(torch.eq(torch.argmax(preds, dim=1), torch.argmax(labels, dim=1)))

    def __to_percentage(self, value, size):
        return (100 * value / size).item()

    def __log_epoch_accuracy(self, epoch, correct):
        print('Epoch {} Accuracy: {}/{} ({:.0f}%)'
              .format(epoch + 1, correct, len(self.validation_dataset),
                      self.__to_percentage(correct, len(self.validation_dataset))))
