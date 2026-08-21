from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vache", views.vache, name="vache"),
    path("contact", views.contact, name="contact"),
    path("mouton", views.mouton, name="mouton"),
    path('api/avis/', views.submit_avis, name='submit_avis'),
    path('api/avis/list/', views.list_avis, name='list_avis'),
    path('api/contact/', views.submit_contact, name='submit_contact'),
     path("tousproduits", views.tousproduits, name='tousproduits'),

]