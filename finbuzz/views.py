from django.shortcuts import render
from django.core.cache import cache
import requests
import google.generativeai as genai
from .config import apikey, apitoken, polygon_api, gemini_key


def predict_market(data):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Analyze the following stock market data and predict the overall market trend for the next week. Consider factors such as market sentiment, historical performance, and any relevant news: {data}"
    response = model.generate_content(prompt)
    return response.text if response.text else "No prediction available"


# Create your views here.
def home(request):
    url = f"https://api.marketaux.com/v1/news/all?countries=us&limit=3&api_token={apitoken}"
    cache_key = 'market_news'
    market_news = cache.get(cache_key)
    if not market_news:
        results = requests.get(url)
        try:
            market_news = results.json()['data']
        except ValueError:
            market_news = []
            # Log the error or handle it as needed
        cache.set(cache_key, market_news, timeout=60*300)  # Cache for 300 minutes

    context = {
        'market_news': market_news,
    }

    return render(request, 'finbuzz/home.html', context=context)


def get_top_gainers(request):
    """
    Fetches the top gainers from the stock market and renders them in the topgainers.html template.
    """
    cache_key = 'top_gainers'
    top_gainers = cache.get(cache_key)
    
    if not top_gainers:
        url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={apikey}"
        # url = f"https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={apikey}"
        results = requests.get(url)
        try:
            top_gainers = results.json().get('top_gainers', [])
        except ValueError:
            top_gainers = []
            # Log the error or handle it as needed
        cache.set(cache_key, top_gainers, timeout=60*300)  # Cache for 300 minutes

    context = {
        'top_gainers': top_gainers,
        'prediction': predict_market(top_gainers)
    }
    return render(request, 'finbuzz/topgainers.html', context=context)


def get_top_losers(request):
    cache_key = 'top_losers'
    top_losers = cache.get(cache_key)
    if not top_losers:
        url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={apikey}"
        # url = f"https://financialmodelingprep.com/api/v3/stock_market/losers?apikey={apikey}"
        results = requests.get(url)
        try:
            top_losers = results.json().get('top_losers', [])
        except ValueError:
            top_losers = []
            # Log the error or handle it as needed
        cache.set(cache_key, top_losers, timeout=60*300)  # Cache for 300 minutes

    context = {
        'top_losers': top_losers,
        'prediction': predict_market(top_losers)
    }
    return render(request, 'finbuzz/toplosers.html', context=context)


def get_holidays(request):
    cache_key = 'holidays'
    holidays = cache.get(cache_key)
    if not holidays:
        url = f"https://api.polygon.io/v1/marketstatus/upcoming?apiKey={polygon_api}"
        results = requests.get(url)
        try:
            holidays = results.json()
        except ValueError:
            holidays = []
            # Log the error or handle it as needed
        cache.set(cache_key, holidays, timeout=60*300)  # Cache for 300 minutes

    context = {
        'holidays': holidays
    }
    return render(request, 'finbuzz/holidays.html', context=context)
