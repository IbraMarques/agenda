from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.
#def index(request):
#    return redirect('/agenda/') função utilizada para evitar erro de página caso o endereço "vazio"  seja acessado

#Função login_user: redireciona usuário para a página de login caso ele tente acessar página web sem estar autenticado/logado
#evita o aparecimento de página com erro

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido.")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    print(data_atual, timedelta(hours=1))
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    print(id_evento)
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        local_evento = request.POST.get('local_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_update = request.POST.get('id_evento')
        print(id_update)
        if id_update:
            evento = Evento.objects.get(id=id_update)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.local_evento = local_evento
                evento.save()
            #Evento.objects.filter(id=id_update).update(titulo=titulo,
            #                                          data_evento=data_evento,
            #                                           local_evento=local_evento,
            #                                           descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  local_evento=local_evento,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    try:
        usuario = request.user
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')
#Função para retornar valores Json
#1 - Nesta é necessário login por parte  do  usuário
# @login_required(login_url='/login/')
# def json_lista_evento(request):
#     usuario = request.user
#     evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'local_evento')
#     return JsonResponse(list(evento), safe=False)

#2 - Neste caso, os valores serão passados apenas digitando o id do usuário sem a necessidade de login

def json_lista_evento(request, id_usuario):
     usuario = User.objects.get(id=id_usuario)
     evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'local_evento')
     return JsonResponse(list(evento), safe=False)