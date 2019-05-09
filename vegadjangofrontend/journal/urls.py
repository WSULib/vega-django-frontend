from django.urls import path

from . import views

urlpatterns = [

	# index/home page
    path('', views.index, name='index'),

    # issues
    path('issues', views.issues, name='issues'),
    path('issue/<str:issue_id>', views.issue, name='issue'),

]