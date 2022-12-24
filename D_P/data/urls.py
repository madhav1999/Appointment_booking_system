
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.mainpage, name='mainpage'),
    path("get", views.seebookinformation, name="Home"),
    path("insert/<int:id>/", views.insertview, name="insertv"),
    path("delete/<int:id>", views.deleteview, name="deletev"),
    path("detailstodeleteslot", views.detailstodeleteslot, name="detailsdelete"),
    # path("viewslots/<int:id>", views.viewslot, name='viewslot'),

]
