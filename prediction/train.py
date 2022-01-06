from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
import os
import pandas as pd

import os
import sys

root_folder = os.path.join(sys.path[0], "../").replace("\\", "/")
sys.path.append(root_folder)

from prediction.predict import create_model, load_data
from prediction.parameters import *

# create these folders if they does not exist
if not os.path.isdir("results"):
    os.mkdir("results")

if not os.path.isdir("logs"):
    os.mkdir("logs")

if not os.path.isdir("data"):
    os.mkdir("data")


def train(symbol=symbol):
    # load the data
    data = load_data(symbol, N_STEPS, scale=SCALE, split_by_date=SPLIT_BY_DATE,
                     shuffle=SHUFFLE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE,
                     feature_columns=FEATURE_COLUMNS)

    # save the dataframe
    data["df"].to_csv(ticker_data_filename)

    # construct the model
    model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                         dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)

    # some tensorflow callbacks
    checkpointer = ModelCheckpoint(os.path.join("results", model_name + ".h5"), save_weights_only=True,
                                   save_best_only=True, verbose=1)
    tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))
    # train the model and save the weights whenever we see 
    # a new optimal model using ModelCheckpoint
    history = model.fit(data["X_train"], data["y_train"],
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_data=(data["X_test"], data["y_test"]),
                        callbacks=[checkpointer, tensorboard],
                        verbose=1)


if __name__ == "__main__":
    train()
