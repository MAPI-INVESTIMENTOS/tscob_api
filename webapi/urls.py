from .views import *
from django.urls import path,include
from knox import views as knox_views

urlpatterns = [

    path('web/login/',  LoginAPI.as_view(), name='login'),
    path('web/Registar_empresa/', Registar_Empresa.as_view(), name='registar_empresha'),
    path('web/Registar_empresa_s/', Registar_Empresa_s.as_view(), name='registar_empresa'),
    path('web/dados_empresa/',Get_Company_Data.as_view(),name="obter dados da empresa por id"),
    path('web/Marcar_Pedido/',Marcar_Quitacao.as_view(),name="Marcar Quitacao"),
    path('web/pedidos_empresa/',Pedidos_Da_Empresa.as_view(),name="Lista dos pedidos "),
    path('web/Todos_pedidos_empresa/',Todos_Pedidos_Empresa.as_view(),name="Listaa de todos pedidos "),
    path('web/Todos_pedidos_empresa_por_rever/', Todos_Pedidos_Empresa_por_rever.as_view(), name="Listaa de todos pedidos "),
    path('web/Pesquisar_empresa/',Pesquisar_Empresa.as_view(),name="Pesquisar Empresa "),
    path('web/Quitar_empresa/',Habilitar_Quitacao.as_view(),name="Quitar Empresa "),
    path('web/Quitar_empresa_Rever/',Rever_Habilitar_Quitacao.as_view(),name="Quitar Empresa_submeter supeiror "),
    path('web/Quitar_empresa_Chumbar/',Chumbar_Habilitar_Quitacao.as_view(),name="Quitar Empresa_chumbar "),
    path('web/Quitar_empresa_Chumbar_A/',Chumbar_Habilitar_Quitacao_admin.as_view(),name="Quitar Empresa_chumbar "),
    path('web/get_quitacao/',Get_quitacao.as_view(),name="get quitacao"),
    path('web/Lista_Empresas/',Get_empresas.as_view(),name="get quitacao"),
    path('web/Pesquisar_empresa_funcionario/',Pesquisar_Empresas_funcionario.as_view(),name="get quitacao"),
    path('web/Registar_ocorrencia/',Registar_ocorrecnias_Empresa.as_view(),name="get quitacao"),
    path('web/Pesquisar_Antecedentes_Empresa/',Empresa_Antecentes_lista.as_view(),name="get quitacao"),
    path('web/Assinalar_Funcionario/',Assinalar_Arquivo_Usurio.as_view(),name="Assinar Funcionario Arquivo"),
    path('web/Arquivo_Gestao/',Gestao_do_Map_arquivo.as_view(),name="Aio Arquivo"),
    path('web/Nao_tem_nenhum/',Nao_tem_nenhum.as_view(),name="sds")
]