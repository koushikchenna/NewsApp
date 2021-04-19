from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("settings", views.settings, name="settings"),
    path("persnews/<str:username>", views.persnews, name="persnews"),
    path("bytopic", views.bytopic, name="bytopic"),
    path("bytopicres", views.bytopicres, name="bytopicres"),
    path("bytopicres/<slug:titlevalue>/", views.result, name="result"),
    path("allvals/", views.allvals, name="allvals"),
    path("addto/<str:holdval>/<str:uname>/", views.addto, name="addto"),
    path("persnews/remove/<slug:nameedit>/", views.remove, name="remove"),
    path("setting/corona/<str:uname>/", views.corona, name="corona"),
    path("setting/weather/<str:uname>/", views.weather, name="weather"),
    path("setting/sports/<str:uname>/", views.sports, name="sports")
]
