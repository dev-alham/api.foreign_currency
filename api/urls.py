from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('exchange', views.ExchangeView.as_view()),  # Done
    path('exchange/rate', views.RateView.as_view()),
    path('exchange/rate/<int:param>', views.RateView.as_view()),  # Done
    path('exchange/rate/<str:category>/<str:param>', views.DetailRateView.as_view())
]
#
# urlpatterns = format_suffix_patterns(urlpatterns)
