from django.shortcuts import render
import json
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import login
from time import *
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from time import *
from django.db.models import Q
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db import transaction
from tablib import Dataset

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from .models import *
from .serializers import *
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import os
import string
import random

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    queryset = Empresa.objects.all()
    serializer_class = Empresa

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        grupo = None
        identifica = None
        if user.groups.exists():
            grupo = user.groups.all()[0].name
            identifica = user.id
        if user.is_superuser:
            grupo = 'Admin'
            identifica = user.id
        _, token = AuthToken.objects.create(user)

        ope = 1

        if grupo!="tribunal" and grupo!="operario" and grupo!="arquivo" :
            ope = Empresa.objects.get(user=user.id)
            ope = ope.Representante
        nuit = '2323'

        return Response({'token': token, 'nome_empresa':ope,'grupo': grupo})


class Registar_Empresa(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny)
    queryset = Empresa.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        info=self.request.data
        nome=info['nome_empresa']
        mail=info['mail']
        password=info['password']

        username = nome.replace(" ", "")
        username=username.lower()
        print(username)
        print(1)
        characters = string.ascii_letters + string.digits

        # Generate the random password
        print("==============feito=================")
        print(password)
        try:
            serializer = self.get_serializer(
                data={"username": f"{username}", "password": f"{password}", "email": f"anisio2000@gmail.com"})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except:
            serializer = self.get_serializer(data={
                "username": f"{username}{localtime().tm_year}{localtime().tm_mon}{localtime().tm_mday}{localtime().tm_hour}{localtime().tm_min}{localtime().tm_sec}",
                "password": f"{password}", "email": f"anisio2000@gmail.com"})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        print(1)
        user_id = serializer.data
        user_id = user_id['id']
        gg = Group.objects.get(name="empresa")
        gg.user_set.add(user)



        n=Empresa.objects.create(
            nome=info['nome_empresa'],
            nuit=info['nuit'],
            endereco=info['endereco'],
            vocacao=info['vocacao'],
            objectivo='dfdf',
            Representante=info['nome'],
            cidade=info['cidade'],
        provinvia = info['provincia'],
            user=user


        )
        n.save()
        print(mail)

        return Response(data={"username":username,"password":password})

class Registar_Empresa_s(generics.CreateAPIView):

    queryset = Empresa.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        info=self.request.data
        nome=info['nome']
        mail=info['mail']

        username = nome.replace(" ", "")
        username=username.lower()
        print(username)
        print(1)
        characters = string.ascii_letters + string.digits

        # Generate the random password
        password = ''.join(random.choice(characters) for _ in range(15))
        print(password)
        try:
            serializer = self.get_serializer(
                data={"username": f"{username}", "password": f"{info['password']}", "email": f"anisio2000@gmail.com"})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except:
            serializer = self.get_serializer(data={
                "username": f"{username}{localtime().tm_year}{localtime().tm_mon}{localtime().tm_mday}{localtime().tm_hour}{localtime().tm_min}{localtime().tm_sec}",
                "password": f"{info['password']}", "email": f"anisio2000@gmail.com"})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        print(1)
        user_id = serializer.data
        user_id = user_id['id']
        gg = Group.objects.get(name="empresa")
        gg.user_set.add(user)



        n=Empresa.objects.create(
            nome=info['nome_empresa'],
            nuit=info['nuit'],
            endereco=info['endereco'],
            vocacao=info['vocacao'],
            objectivo='dfdf',
            Representante=info['nome'],
            cidade=info['cidade'],
        provinvia = info['provincia'],
            user=user


        )
        n.save()
        print(mail)
        return Response(data={"username":username,"password":password})

class Get_Company_Data(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Empresa.objects.all()
    serializer_class = Empresa_Serializado

    def post(self, request, *args, **kwargs):
        company=Empresa.objects.get(user=self.request.user.id)
        company_s=Empresa_Serializado(company).data
        print(company_s)
        return Response(company_s)


class Marcar_Quitacao(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Empresa.objects.all()
    serializer_class = Empresa_Serializado

    def post(self, request, *args, **kwargs):
        print(self.request.user.id)
        company = Empresa.objects.get(user=int(self.request.user.id))
        print(company)
        company_s_q = Pedidos_Quitacao.objects.create(idEmpresa=company,estado=1,user=User.objects.get(id=int(self.request.user.id)))
        company_s_q.save()
        #0--PENDENTE PAGAMENTO
        #1--EM PRODUÇÃO
        #2--TERMINADO
        return Response({"ok":1})

class Pedidos_Da_Empresa(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Empresa.objects.all()
    serializer_class = Empresa_Serializado

    def post(self, request, *args, **kwargs):
        print("sdsdsdsdsds")

        print(self.request.user.id)

        company = Empresa.objects.get(user=int(self.request.user.id))
        company_s_q = Pedidos_Quitacao.objects.filter(idEmpresa=company.idEmpresa)
        a=list()


        for u in company_s_q:
            kl = dict()
            company_s_q_s=Pedido_Quitacao_Serializado(u).data
            #nm=Quitacao.objects.get(idPedido=company_s_q_s['idPedido'])
            #nm_s=Quitacao_Serializado(nm).data
            #kl.update(nm_s)
            kl.update(company_s_q_s)
            a.append(kl)


        return Response(a)



class Todos_Pedidos_Empresa(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado



    def post(self, request, *args, **kwargs):
        ped=Pedidos_Quitacao.objects.filter(revisto="1")
        ped_lista=list()
        for l in ped:
            ped_s=Pedido_Quitacao_Serializado(l).data
            if ped_s['estado_info']=="processamento":
                ped_s.update({"estado_info":"processado"})
            compay=Empresa.objects.get(idEmpresa=int(ped_s['idEmpresa']))
            compay_s=Empresa_Serializado(compay).data
            compay_s.update(ped_s)
            ped_lista.append(compay_s)


        return Response(ped_lista)
class Todos_Pedidos_Empresa_por_rever(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        ped=Pedidos_Quitacao.objects.filter(revisto="0",assinalado="0")
        ped_lista=list()
        for l in ped:
            ped_s=Pedido_Quitacao_Serializado(l).data

            compay=Empresa.objects.get(idEmpresa=int(ped_s['idEmpresa']))
            compay_s=Empresa_Serializado(compay).data
            compay_s.update(ped_s)
            comp_ant=Empresa_Atencedentes.objects.filter(idEmpresa=int(ped_s['idEmpresa']))
            comp_ant_s=Empresa_Atencedentes_Serializado(comp_ant,many=True).data
            if comp_ant_s!=[]:
              compay_s.update({"color":"red","info" :"Processo judicial Correndo"})
            else:
                compay_s.update({"color": "green", "info": "Sem Processo judicial"})


            ped_lista.append(compay_s)
            print(ped_lista)

        return Response(ped_lista)

class Pesquisar_Empresa(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        company=Pedidos_Quitacao.objects.get(idPedido=int(self.request.data['casa']))
        company_s=Pedido_Quitacao_Serializado(company).data
        company_emp=Empresa.objects.get(idEmpresa=company_s['idEmpresa'])
        company_emp_s=Empresa_Serializado(company_emp).data

        company_emp_s.update(company_s)
        return Response(company_emp_s)

class Pesquisar_Empresas_funcionario(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        company_emp = Empresa.objects.get(idEmpresa=int(self.request.data['casa']))
        company_emp_s = Empresa_Serializado(company_emp).data
        return Response(company_emp_s)

class Rever_Habilitar_Quitacao(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        company = Pedidos_Quitacao.objects.get(idPedido=int(self.request.data['casa']))
        company.estado_info="processamento"

        company.estado_info_inter=self.request.data['text_anotacoes']
        company.estado = 1
        company.revisto=1
        company.save()


        return Response(status="200")


class Chumbar_Habilitar_Quitacao(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        company = Pedidos_Quitacao.objects.get(idPedido=int(self.request.data['casa']))
        company.estado_info = "Reprovado"
        company.estado_info_inter = self.request.data['text_anotacoes']
        company.estado = 2
        company.revisto = 1
        company.tipo="red"
        company.save()

        return Response(status="200")

class Chumbar_Habilitar_Quitacao_admin(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        company = Pedidos_Quitacao.objects.get(idPedido=int(self.request.data['casa']))
        company.estado_info = "Reprovado"
        company.revisto = 2
        company.estado = 1
        company.save()

        return Response(status="200")


class Habilitar_Quitacao(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        company = Pedidos_Quitacao.objects.get(idPedido=int(self.request.data['casa']))
        company.estado_info="Aprovado"
        company.revisto=2
        company.estado = 2
        company.save()
        company_q=Quitacao.objects.create(
            idPedido=company,
        data_expiracao=f'{localtime().tm_year}-{localtime().tm_mon+3}-{localtime().tm_mday}'
        )
        company_q.save()
        emp=company.idEmpresa
        compay_quitacao=Empresa_Quitacao.objects.create(idEmpresa=Empresa.objects.get(idEmpresa=emp.idEmpresa),
                                                        idQuitacao=company_q)

        return Response(status="200")


class Get_quitacao(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        quitacao=Quitacao.objects.get(serialNumber=self.request.data['serialNumber'])
        quitacao_s=Quitacao_Serializado(quitacao).data

        quitacao_empresa=Empresa_Quitacao.objects.get(idQuitacao=quitacao_s['idQuitacao'])
        e_quitacao=Empresa_Quitacao_Serializado(quitacao_empresa).data
        empresa=Empresa.objects.get(idEmpresa=int(e_quitacao['idEmpresa']))
        empresa_s=Empresa_Serializado(empresa).data

        a=dict()
        a.update(empresa_s)
        a.update(quitacao_s)
        print(a)
        return Response(a)




class Get_empresas(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado
    def post(self, request, *args, **kwargs):
        emp=Empresa.objects.all()
        emp_s=Empresa_Serializado(emp,many=True).data
        return Response(emp_s)

class Registar_ocorrecnias_Empresa(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        antec=Empresa_Atencedentes(idEmpresa=Empresa.objects.get(idEmpresa=self.request.data['Empresa'])
                                   ,info=self.request.data['texto'])
        antec.save()
        return Response({"sd":1})



class Empresa_Antecentes_lista(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        company_emp = Empresa.objects.get(idEmpresa=int(self.request.data['casa']))
        company_emp_s = Empresa_Serializado(company_emp).data
        company_antc=Empresa_Atencedentes.objects.filter(idEmpresa=company_emp_s['idEmpresa'])
        company_antc_S=Empresa_Atencedentes_Serializado(company_antc,many=True).data

        company_emp_s.update({'lista':company_antc_S})
        return Response(company_emp_s)
class Assinalar_Arquivo_Usurio(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        Assin=Pedidos_Quitacao.objects.get(idPedido=int(self.request.data['idPedido']))
        Assin.user=User.objects.get(username='AntonioMarcos')
        Assin.assinalado="1"
        Assin.assinalado_er="1"
        Assin.save()
        return Response({"user":"ok"})

class Gestao_do_Map_arquivo(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado
    def post(self, request, *args, **kwargs):
        emp=Pedidos_Quitacao.objects.filter(user=self.request.user.id,assinalado_er="1")
        emp_s=Pedido_Quitacao_Serializado(emp,many=True).data
        l=list()
        for s in emp_s:
            epr=Empresa.objects.get(idEmpresa=s['idEmpresa'])
            epr_s=Empresa_Serializado(epr).data
            epr_s.update(s)
            l.append(epr_s)
        return Response(l)

class Nao_tem_nenhum(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Pedidos_Quitacao.objects.all()
    serializer_class = Pedido_Quitacao_Serializado

    def post(self, request, *args, **kwargs):
        emp = Pedidos_Quitacao.objects.get(idPedido=self.request.data['idpedido'])
        emp.revisto="0"
        emp.assinalado ="0"
        emp.assinalado_er="3"
        emp.save()
        return Response({"df":"df"})
