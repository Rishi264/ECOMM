
from django.urls import path
from .import views
urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("productView/<int:id>", views.productView, name="ProductView"),
    path("checkOut/", views.checkOut, name="CheckOut"),
    path("pay/", views.pay, name="pay"),
    path("registration/signup", views.signup, name="signup"),




]