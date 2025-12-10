from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('gestor/login/', views.gestor_login, name='gestor-login'),
    path('gestor/', views.gestor_dashboard, name='gestor-dashboard'),
    path('gestor/excluir/<int:candidato_id>/', views.excluir_candidato, name='excluir-candidato'),
    path('gestor/anotacoes/<int:candidato_id>/', views.atualizar_anotacoes, name='atualizar-anotacoes'),
]