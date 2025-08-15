from django.contrib.auth import views
from django.urls import path
from kservice_aap import views



urlpatterns = [
    
  path('new',views.create_record,name="new"),
  path('manual_entry',views.manual_entry,name="manual_entry"),
  path('submit',views.submitrecord,name="submit"),
  path('updaterecord',views.updaterecord,name="updaterecord"),

  
  path('dashboard',views.anlyst_dashboard,name="dashboard"),
  path('reports', views.report_dashboard, name='reports'), 
  path('update_comment', views.update_comment, name='update_comment'), 

  path('view_record/<int:id>/', views.view_record, name='view_record'), 
  path('view_record_/<int:id>/', views.view_record_, name='view_record_'), 

  path('display_record', views.generate_report, name='display_record'), 
]
