from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_cliente, name='login_cliente'),
    path('cadastro/', views.cadastro_cliente, name='cadastro_cliente'),
    path('agendar/', views.agendar_sem_cadastro, name='agendar_sem_cadastro'),
    path('salvar-agendamento/', views.salvar_agendamento, name='salvar_agendamento'),
    path('painel/', views.painel_cliente, name='painel_cliente'),
    path('logout/', views.logout_cliente, name='logout_cliente'),
    path('agendamento-confirmado/', views.agendamento_confirmado, name='agendamento_confirmado'),
    path('cancelar-agendamento/<int:agendamento_id>/',views.cancelar_agendamento,name='cancelar_agendamento'),
    path('meu-agendamento/',views.agendar_cliente,name='agendar_cliente'),
    path('salvar-agendamento-cliente/',views.salvar_agendamento_cliente,name='salvar_agendamento_cliente'),
    path('admin-painel/',views.admin_painel,name='admin_painel'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('logout-admin/', views.logout_admin, name='logout_admin'),
    path('atualizar-pagamento/<int:agendamento_id>/',views.atualizar_pagamento,name='atualizar_pagamento'),
    path('admin-servicos/', views.admin_servicos, name='admin_servicos'),
    path('criar-servico/', views.criar_servico, name='criar_servico'),
    path('atualizar-servico/<int:servico_id>/', views.atualizar_servico, name='atualizar_servico'),
    path('excluir-agendamento/<int:agendamento_id>/',views.excluir_agendamento,name='excluir_agendamento'),
]