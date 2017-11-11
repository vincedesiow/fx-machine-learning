import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

def glimpseMissingData(df, showAll=False, cutoff=0.1):
    print(df.name)
    for feature in df.columns:
    	if showAll or sum(pd.isnull(df[feature]))/df.shape[0] < cutoff:
        	print(feature, end = " ")
        	print("Missing data: %i out of a total of %i entries"%(sum(pd.isnull(df[feature])), df.shape[0]), end = "   ")
        	print(sum(pd.isnull(df[feature]))/df.shape[0])
    print()

def initialFilter(df, cutoff=0.1):
    selected = []
    for feature in df.columns:
        if sum(pd.isnull(df[feature]))/df.shape[0] < cutoff:
            selected.append(feature)
    return df[selected]

# def convert_float(val):
#     try:
#         return float(val)
#     except ValueError:
#         return np.nan

# def seriesToFloat(df, columns):
# 	for feature in columns:
#     	df[feature] = df[feature].apply(lambda x: convert_float(x))

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def plotStrategy(in_sample_actual, out_sample_actual, in_sample_pred, out_sample_pred):
    strat_insample = np.where(in_sample_pred<0, -1, 1)
    strat_outsample = np.where(out_sample_pred<0, -1, 1)
    positions = np.concatenate((strat_insample, strat_outsample))
    actual = np.concatenate((in_sample_actual, out_sample_actual))
    pnl = np.cumprod(positions*actual + 1)
    turnover = np.zeros(len(positions))
    turnover[1:] = np.absolute(positions[1:] - positions[:-1])
    turnover[1:] /= np.absolute(positions[:-1])
    fig, axes = plt.subplots(2,1, figsize=(15,15))
    axes[0].plot(pnl)
    axes[0].set_title("pnl")
    axes[0].axvline(x=2000, color='r', linestyle='-')
    axes[1].plot(turnover)
    axes[1].set_title("turnover")
    plt.show()
    unique_elements, counts_elements = np.unique(turnover, return_counts=True)
    print(pd.DataFrame({'turnover ratio': unique_elements,
                        'frequency': counts_elements}))

def plotDailyStrategy(pred, actual, margin=0):
    if margin == 0:  
        positions = np.where(pred>0, 1, -1)
        pnl = np.cumprod(positions*actual + 1)
        turnover = np.zeros(len(positions))
        turnover[1:] = np.absolute(positions[1:] - positions[:-1])
        turnover[1:] /= np.absolute(positions[:-1])
    else:
        positions = pred*margin
        pnl = np.cumprod(positions*actual + 1)
        turnover = np.zeros(len(positions))
        turnover[1:] = np.absolute(positions[1:] - positions[:-1])
        turnover[1:] /= np.absolute(positions[:-1])
    fig, axes = plt.subplots(2,1, figsize=(15,15))
    axes[0].plot(pnl)
    axes[0].plot(np.cumprod(actual+1))
    axes[0].set_title("pnl")
    axes[1].plot(turnover)
    axes[1].set_title("turnover")
    plt.show()
    unique_elements, counts_elements = np.unique(turnover, return_counts=True)
    print(pd.DataFrame({'turnover ratio': unique_elements,
                        'frequency': counts_elements}))
    print("Correct direction: %f"%(sum((pred < 0) == (actual < 0))/len(pred)))