from django.conf.urls import url
from basic_app import views

# SET THE NAMESPACE!
app_name = 'basic_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^food_pref_updt/$',views.food_pref_updt,name='food_pref_updt'),
    url(r'^participate/$',views.participate,name='participate'),
    url(r'^departicipate/$',views.departicipate,name='departicipate'),
    url(r'^user/$',views.user,name='user'),
]


