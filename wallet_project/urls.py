from django.contrib import admin
from django.urls import path, include
from wallet_app import urls
from wallet_app.views import home, account_panel, add_buying_list, edit_buying_list, delete_buying_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls), name='api-home'),
    path('', home, name='home'),
    path('account/<int:account_id>/', account_panel, name='account_panel'),
    path('account/<int:account_id>/add/', add_buying_list, name='add_buying_list'),
    path('account/<int:account_id>/edit/<int:item_id>/', delete_buying_list, name='delete_buying_list'),
    path('account/<int:account_id>/delete/<int:item_id>/', edit_buying_list, name='edit_buying_list'),
]
