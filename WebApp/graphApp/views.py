from statistics import mode
from django.shortcuts import render
from django.http import JsonResponse
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay
from . import forms
import yfinance as yf
from plotly.offline import plot
import plotly.express as px
from plotly.graph_objs import Scatter, Figure, Layout, Candlestick
from itertools import product
import datetime as dt
from . import backtester as MLB
# Create your views here.

def return_data(ticker, start, end, freq):
    stocks = yf.download(ticker, start=start, end=end, interval=freq)
    stocks.dropna(inplace=True)

    return [stocks.index.tolist(), stocks['Adj Close'].tolist(), stocks['Open'].tolist(),
            stocks['High'].tolist(), stocks['Low'].tolist(), stocks['Close'].tolist()]

def return_sma(ticker, start, end, short, long):
    stocks = yf.download(ticker, start=start-BDay(252), end=end)
    stocks['SMA_S'] = stocks['Adj Close'].rolling(short).mean()
    stocks['SMA_L'] = stocks['Adj Close'].rolling(long).mean()
    stocks.dropna(inplace=True)
    stocks = stocks.loc[stocks.index >= str(start)]
    return [stocks.index.tolist(), stocks['Adj Close'].tolist(),
            stocks['SMA_S'].tolist(), stocks['SMA_L'].tolist()]

def test_strategy(SMA,df):
    data = df.copy()
    data['returns'] = np.log(data.price/data.price.shift(1))
    data['SMA_S'] = data.price.rolling(int(SMA[0])).mean()
    data['SMA_L'] = data.price.rolling(int(SMA[1])).mean()
    data.dropna(inplace=True)

    data['position'] = np.where(data['SMA_S']>data['SMA_L'], 1, -1)
    data['strategy'] = data.position.shift(1)*data['returns']
    data.dropna(inplace=True)

    return np.exp(data['strategy'].sum())

def return_optimized_sma(ticker, start, end):
    stocks = yf.download(ticker, start=start, end=end)
    df = stocks.loc[:, "Close"].copy().to_frame()
    df.rename(columns = {'Close':'price'}, inplace=True)

    SMA_S_range = range(10,50,1)
    SMA_L_range = range(100,252,1)
    combinations = list(product(SMA_S_range,SMA_L_range))

    results = []
    for comb in combinations:
        results.append(test_strategy(comb,df))
        if len(results)%100 == 0:
            print(len(results))

    many_results = pd.DataFrame(data=combinations, columns=['SMA_S','SMA_L'])
    many_results['performance'] =  results
    many_results = many_results.nlargest(10, 'performance')
    return [many_results.SMA_S.tolist(), many_results.SMA_L.tolist(), many_results.performance.tolist()]

def return_ml_result(ticker, start, end, lags, tc, model):
    ml = MLB.MLBacktester(ticker, start, end, tc, model)
    perf,outperf = ml.test_strategy(train_ratio = 0.9, lags = lags)
    results = ml.get_result()
    dates = results.index.to_list()
    creturns = results.creturns.to_list()
    cstrategy = results.cstrategy.to_list()

    return perf,outperf,dates,creturns,cstrategy

def return_optimal_lags(ticker, start, end, tc, model):
    ml = MLB.MLBacktester(ticker, start, end, tc, model)
    
    lags = []
    perf = []
    outperf = []
    for l in range(1, 21):
        p,op =  ml.test_strategy(train_ratio = 0.9, lags = l)
        lags.append(l)
        perf.append(p)
        outperf.append(op)
    
    return lags,perf,outperf

#VIEWS FUNCTIONS
def home(request):
    return render(request, 'graphApp/home.html')

def data(request):
    form = forms.DataForm()
    
    context = {'form': form}

    if request.method == "POST":
        form = forms.DataForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            freq = form.cleaned_data.get("frequency")
            X,Y,Open,High,Low,Close = return_data(ticker,start,end,freq)
            return JsonResponse({'X':X,'Y':Y,'Open':Open,'High':High,'Low':Low,'Close':Close})

    return render(request, 'graphApp/data.html', context)

def sma(request):
    form = forms.SMAForm()
    context = {'form': form}

    if request.method == "POST":
        form = forms.SMAForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            short = form.cleaned_data.get("sma_short")
            long = form.cleaned_data.get("sma_long")
            X,Y,smaShort,smaLong = return_sma(ticker,start,end,short,long)
            return JsonResponse({'X':X,'Y':Y,'smaShort':smaShort,'smaLong':smaLong, 'short':short, 'long':long})

    return render(request, 'graphApp/sma.html', context)

def optimizedSma(request):
    form = forms.optimizedSMAForm()
    context = {'form': form}

    if request.method == "POST":
        form = forms.optimizedSMAForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            SMA_S,SMA_L,performance = return_optimized_sma(ticker,start,end)
            return JsonResponse({'SMA_S':SMA_S,'SMA_L':SMA_L,'performance':performance})

    return render(request, 'graphApp/optimizedSma.html', context)

def MLBacktesting(request):
    form = forms.MLBacktestingForm()
    context = {'form': form}

    if request.method == "POST":
        form = forms.MLBacktestingForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            lags = form.cleaned_data['lags']
            tc = form.cleaned_data['trading_cost']
            model = form.cleaned_data.get('model')

            perf,outperf,dates,creturns,cstrategy = return_ml_result(ticker, start, end, lags, tc, model)

            return JsonResponse({'dates':dates,'creturns':creturns,'cstrategy':cstrategy,'perf':perf,'outperf':outperf,'model':model})
    
    return render(request, 'graphApp/MLBacktesting.html', context)

def optimalLags(request):
    form = forms.optimalLagsForm()
    context = {'form': form}

    if request.method == "POST":
        form = forms.optimalLagsForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            tc = form.cleaned_data['trading_cost']
            model = form.cleaned_data.get('model')

            lags,perf,outperf = return_optimal_lags(ticker, start, end, tc, model)
            return JsonResponse({'lags':lags,'perf':perf,'outperf':outperf})

    return render(request, 'graphApp/optimalLags.html', context)
