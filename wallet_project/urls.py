from django.contrib import admin
from django.urls import path, include
from wallet_app import urls
from wallet_app.views import home, account_panel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls), name='api-home'),
    path('', home, name='home'),
    path('account/<int:account_id>/<str:account_type>/', account_panel, name='account_panel')
]
