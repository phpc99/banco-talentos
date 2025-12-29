from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('gestor/login/', views.gestor_login, name='gestor-login'),
    path('gestor/', views.gestor_dashboard, name='gestor-dashboard'),
    path('gestor/excluir/<int:candidato_id>/', views.excluir_candidato, name='excluir-candidato'),
    path('gestor/anotacoes/<int:candidato_id>/', views.atualizar_anotacoes, name='atualizar-anotacoes'),
    path('status/', views.consultar_status, name="consultar-status"),
    path('gestor/status/<int:candidato_id>/', views.atualizar_status, name='atualizar-status'),
    path("gestor/entrevistas/", views.entrevistas_lista, name="entrevistas-lista"),
    path("gestor/entrevistas/<int:candidato_id>/", views.entrevista_detalhe, name="entrevista-detalhe"),
    path("carreira/", views.carreira, name="carreira"),
    path('gestor/logout/', views.gestor_logout, name='gestor-logout'),
    path("gestor/entrevistas/excluir/<int:candidato_id>/", views.excluir_entrevista, name="excluir-entrevista"),
]