import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import yfinance as yf

class MLBacktester():

    def __init__(self, ticker, start, end, tc, model):
        model_dict = {'Logistic Regression':LogisticRegression(C = 1e6, max_iter = 100000, multi_class = "ovr"),
                    'Random Forest':RandomForestClassifier()}
        self.ticker = ticker
        self.start = start
        self.end = end
        self.tc = tc
        self.model = model_dict[model]
        self.results = None
        self.get_data()
                             
    def get_data(self):
        raw = yf.download(self.ticker, start=self.start, end=self.end)
        raw = raw.loc[:, "Close"].to_frame()
        raw.rename(columns = {'Close':'price'}, inplace=True)
        raw["returns"] = np.log(raw/raw.shift(1))
        self.data = raw
                             
    def split_data(self, start, end):
        data = self.data.loc[start:end].copy()
        return data
    
    def prepare_features(self, start, end):
        self.data_subset = self.split_data(start, end)
        self.feature_columns = []
        for lag in range(1, self.lags + 1):
            col = "lag{}".format(lag)
            self.data_subset[col] = self.data_subset["returns"].shift(lag)
            self.feature_columns.append(col)
        self.data_subset.dropna(inplace=True)
        
    def fit_model(self, start, end):
        self.prepare_features(start, end)
        self.model.fit(self.data_subset[self.feature_columns], np.sign(self.data_subset["returns"]))
        
    def test_strategy(self, train_ratio = 0.7, lags = 5):
        self.lags = lags
                  
        # determining datetime for start, end and split (for training an testing period)
        full_data = self.data.copy()
        split_index = int(len(full_data) * train_ratio)
        split_date = full_data.index[split_index-1]
        train_start = full_data.index[0]
        test_end = full_data.index[-1]
        
        # fit the model on the training set
        self.fit_model(train_start, split_date)
        print("Model trained")

        # prepare the test set
        self.prepare_features(split_date, test_end)
                  
        # make predictions on the test set
        predict = self.model.predict(self.data_subset[self.feature_columns])
        self.data_subset["pred"] = predict
        
        # calculate Strategy Returns
        self.data_subset["strategy"] = self.data_subset["pred"] * self.data_subset["returns"]
        
        # determine the number of trades in each bar
        self.data_subset["trades"] = self.data_subset["pred"].diff().fillna(0).abs()
        
        # subtract transaction/trading costs from pre-cost return
        self.data_subset.strategy = self.data_subset.strategy - self.data_subset.trades * self.tc
        
        # calculate cumulative returns for strategy & buy and hold
        self.data_subset["creturns"] = self.data_subset["returns"].cumsum().apply(np.exp)
        self.data_subset["cstrategy"] = self.data_subset['strategy'].cumsum().apply(np.exp)
        self.results = self.data_subset
        
        perf = self.results["cstrategy"].iloc[-1] # absolute performance of the strategy
        outperf = perf - self.results["creturns"].iloc[-1] # out-/underperformance of strategy
        
        return round(perf, 6), round(outperf, 6)

    def get_result(self):
        return self.results
