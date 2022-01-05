import os
import time
from tensorflow.keras.layers import LSTM

import os
import sys
# root_folder = os.path.join(sys.path[0],"../").replace("\\","/")
# sys.path.append(root_folder)
from utility import get_current_date

# Window size or the sequence length
N_STEPS = 50
# Lookup step, 1 is the next day
LOOKUP_STEP = 15

# whether to scale feature columns & output price as well
SCALE = True
scale_str = f"sc-{int(SCALE)}"
# whether to shuffle the dataset
SHUFFLE = True
shuffle_str = f"sh-{int(SHUFFLE)}"
# whether to split the training/testing set by date
SPLIT_BY_DATE = False
split_by_date_str = f"sbd-{int(SPLIT_BY_DATE)}"
# test ratio size, 0.2 is 20%
TEST_SIZE = 0.2
# features to use
ADJCLOSE_COLUMN = "closing_price"
FEATURE_COLUMNS = ['open_price', 'high_price', 'low_price', 'total_traded_qty', ADJCLOSE_COLUMN]
# date now
date_now = time.strftime("%Y-%m-%d")

### model parameters

N_LAYERS = 10
# LSTM cell
CELL = LSTM
# 256 LSTM neurons
UNITS = 256
# 40% dropout
DROPOUT = 0.4
# whether to use bidirectional RNNs
BIDIRECTIONAL = False

### training parameters

# mean absolute error loss
# LOSS = "mae"
# huber loss
LOSS = "huber_loss"
OPTIMIZER = "adam"
BATCH_SIZE = 64
EPOCHS = 500

# Amazon stock market
symbol = "RELIANCE"
equity = "EQ"
start_date = "01-01-2020"
end_date = get_current_date()
ticker_data_filename = os.path.join("data", f"{symbol}_{date_now}.csv")
# model name to save, making it as unique as possible based on parameters
model_name = f"{date_now}_{symbol}-{shuffle_str}-{scale_str}-{split_by_date_str}-\
{LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
if BIDIRECTIONAL:
    model_name += "-b"