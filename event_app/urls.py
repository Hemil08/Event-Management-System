from django.urls import path
from . import views


urlpatterns = [
    path("",views.event_list,name="event_list"),
    path("register/",views.register,name="register"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("event/<int:pk>/",views.event_details,name="event_details"),
    path("event/create/",views.event_create,name="event_create"),
    path("event/<int:pk>/update",views.event_update,name="event_update"),
    path("event/<int:pk>/delete",views.event_delete,name="event_delete"),
    path("event-registration/<int:event_id>",views.registration_create,name="registration_create"),
    path("event-registration/<int:pk>/update",views.registration_update,name="registration_update"),
    path("event-registration/<int:pk>/delete",views.registration_delete,name="registration_delete"),
    path("event-registration/",views.registration_list,name="registration_list"),
    path("event-registration/<int:pk>/",views.registration_details,name="registration_details"),
    path("dashboard/",views.manager_dashboard,name="dashboard")
]