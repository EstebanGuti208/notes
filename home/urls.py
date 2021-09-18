from django.urls import path
from home import views

urlpatterns = [
    path(
        route='',
        view=views.home_notes,
        name='main_notes'        
    ),

    #API routes

    path(
        route='delete/<int:note_id>/',
        view=views.delete_note,
        name='delete_note'
    ),

    path(
        route='edit/<int:note_id>/',
        view=views.edit_note,
        name='edit_note'
    ),

    path(
        route='register/',
        view=views.register_user,
        name='register'
    ),

    path(
        route='login/',
        view=views.login_person,
        name='login'
    ),
     path(
        route='logout/',
        view=views.logout_user,
        name='logout'
    ),
    path(
        route='sendmail/',
        view=views.send_rand_mail,
        name='randmail'
    )

]