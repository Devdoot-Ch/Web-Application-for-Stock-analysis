from django import forms
from django.forms import ModelForm, widgets

class DateInput(forms.DateInput):
    input_type = 'date'

CHOICES=[('1d','1 day'),
         ('5d','5 days'),
         ('1wk','1 week'),
         ('1mo','1 month'),
         ('3mo','3 months')]

MODELS=[('Logistic Regression','Logistic Regression'),
         ('Random Forest','Random Forest')]

class DataForm(forms.Form):
    ticker = forms.CharField()
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    
    frequency = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))

class SMAForm(forms.Form):
    ticker = forms.CharField()
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    sma_short = forms.IntegerField()
    sma_long = forms.IntegerField()

class optimizedSMAForm(forms.Form):
    ticker = forms.CharField()
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

class MLBacktestingForm(forms.Form):
    ticker = forms.CharField()
    model = forms.CharField(widget=forms.RadioSelect(choices=MODELS))
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    lags = forms.IntegerField()
    trading_cost = forms.FloatField()

class optimalLagsForm(forms.Form):
    ticker = forms.CharField()
    model = forms.CharField(widget=forms.RadioSelect(choices=MODELS))
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    trading_cost = forms.FloatField()
