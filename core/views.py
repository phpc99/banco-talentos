import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import CandidatoForm
from .models import Candidato
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.




# ---------------------- HOME PAGE ---------------------- #

def home(request):
    return render(request, 'home.html')




# ---------------------- CADASTRO DE CANDIDATO ---------------------- #

def cadastrar(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'cadastro_sucesso.html')
    else:
        form = CandidatoForm()

    return render(request, 'cadastrar.html', {'form': form})




# ---------------------- LOGIN DE GESTOR ---------------------- #

# credenciais fixas 
GESTOR_USERNAME = 'gestor'
GESTOR_PASSWORD = '1234' 

def gestor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == GESTOR_USERNAME and password == GESTOR_PASSWORD:
            request.session['gestor_autenticado'] = True
            return redirect('gestor-dashboard')
        else:
            return render(
                request,
                'gestor_login.html',
                {'erro': 'Credenciais inválidas.'}
            )

    return render(request, 'gestor_login.html')

def gestor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('gestor_autenticado'):
            return redirect('gestor-login')
        return view_func(request, *args, **kwargs)
    return wrapper

@gestor_required
def gestor_dashboard(request):
    
    estado = request.GET.get('estado', '')
    formacao = request.GET.get('formacao', '')
    area = request.GET.get('area', '')

    candidatos_filtrados = Candidato.objects.all().order_by('-data_criacao')

    if estado:
        candidatos_filtrados = candidatos_filtrados.filter(estado=estado)
    if formacao:
        candidatos_filtrados = candidatos_filtrados.filter(formacao=formacao)
    if area:
        candidatos_filtrados = candidatos_filtrados.filter(area=area)

    # ----- Paginator -----
    paginator = Paginator(candidatos_filtrados, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ---------------- DADOS PARA GRÁFICOS (usam TODOS filtrados) ----------------
    dict_areas = dict(Candidato.AREAS)
    dict_formacoes = dict(Candidato.FORMACOES)
    dict_estados = dict(Candidato.ESTADOS)

    # 1) Candidatos por área (barras)
    agreg_area = (
        candidatos_filtrados.values('area')
        .annotate(total=Count('id'))
        .order_by('area')
    )

    chart_area = {
        "labels": [dict_areas.get(item['area'], item['area']) for item in agreg_area],
        "values": [item['total'] for item in agreg_area],
    }

    # 2) Candidatos por formação (barras)
    agreg_formacao = (
        candidatos_filtrados.values('formacao')
        .annotate(total=Count('id'))
        .order_by('formacao')
    )

    chart_formacao = {
        "labels": [dict_formacoes.get(item['formacao'], item['formacao']) for item in agreg_formacao],
        "values": [item['total'] for item in agreg_formacao],
    }

    # 3) Candidatos por estado (pizza)
    agreg_estado = (
        candidatos_filtrados.values('estado')
        .annotate(total=Count('id'))
        .order_by('estado')
    )

    chart_estado = {
        "labels": [dict_estados.get(item['estado'], item['estado']) for item in agreg_estado],
        "values": [item['total'] for item in agreg_estado],
    }

    context = {
        'candidatos': page_obj,
        'page_obj': page_obj,
        'total_candidatos_filtrados': candidatos_filtrados.count(),
        'estado_selecionado': estado,
        'formacao_selecionada': formacao,
        'area_selecionada': area,
        'opcoes_estados': Candidato.ESTADOS,
        'opcoes_formacoes': Candidato.FORMACOES,
        'opcoes_areas': Candidato.AREAS,

        # dados dos gráficos em JSON
        'chart_area_json': json.dumps(chart_area),
        'chart_formacao_json': json.dumps(chart_formacao),
        'chart_estado_json': json.dumps(chart_estado),
    }

    return render(request, 'gestor_dashboard.html', context)

@gestor_required
def excluir_candidato(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == 'POST':
        candidato.delete()
        return redirect('gestor-dashboard')

    return render(request, 'confirmar_exclusao.html', {'candidato': candidato})


@gestor_required
def atualizar_anotacoes(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == 'POST':
        texto = request.POST.get('anotacoes', '').strip()
        candidato.anotacoes = texto
        candidato.save()
        messages.success(request, "Anotações salvas com sucesso")
        return redirect('gestor-dashboard')

    return redirect('gestor-dashboard')