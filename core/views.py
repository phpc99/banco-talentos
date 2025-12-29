import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import CandidatoForm
from .models import Candidato, EntrevistaAvaliacao
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
from urllib.parse import urlparse

# ---------------------- HOME PAGE ---------------------- #

def home(request):
    return render(request, 'home.html')

# ---------------------- CADASTRO DE CANDIDATO ---------------------- #

def cadastrar(request):
    erro = None

    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        estado = request.POST.get("estado")
        cidade = request.POST.get("cidade")
        formacao = request.POST.get("formacao")
        area = request.POST.get("area")
        curriculo = request.FILES.get("curriculo")
        foto = request.FILES.get("foto")

        # VALIDAÇÃO DE EMAIL DUPLICADO
        if Candidato.objects.filter(email__iexact=email).exists():
            erro = "Email já em uso."
        else:
            Candidato.objects.create(
                nome=nome,
                email=email,
                estado=estado,
                cidade=cidade,
                formacao=formacao,
                area=area,
                curriculo=curriculo,
                foto=foto,
            )
            return render(request, 'cadastrar.html', {
                'sucesso': True
            })

    return render(request, 'cadastrar.html', {
        "erro": erro,
        "dados": request.POST
    })

# ---------------------- LOGIN DE GESTOR ---------------------- #

# credenciais fixas 
GESTOR_USERNAME = 'gestor'
GESTOR_PASSWORD = '1234' 

def gestor_login(request):
    if request.method != 'POST':
        return redirect('home')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if username == GESTOR_USERNAME and password == GESTOR_PASSWORD:
        request.session['gestor_autenticado'] = True
        return redirect('gestor-dashboard')

    # ---------- erro: voltar para a página anterior ----------
    fallback = reverse('home')
    referer = request.META.get('HTTP_REFERER', '')

    # Segurança: só aceita retorno para o mesmo host
    destino = fallback
    if referer:
        ref = urlparse(referer)
        if ref.netloc == request.get_host():
            destino = ref.path
            if ref.query:
                destino += f"?{ref.query}"

    # adiciona login_error=1 preservando query existente
    if '?' in destino:
        destino = f"{destino}&{urlencode({'login_error':'1'})}"
    else:
        destino = f"{destino}?{urlencode({'login_error':'1'})}"

    return redirect(destino)

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

        # dados dos gráficos
        'chart_area': chart_area,
        'chart_formacao': chart_formacao,
        'chart_estado': chart_estado,
    }

    return render(request, 'gestor_dashboard.html', context)

@gestor_required
def excluir_candidato(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == 'POST':
        candidato.delete()
        messages.success(request, "Candidato excluído com sucesso")
        return redirect('gestor-dashboard')

    return render(request, 'confirmar_exclusao.html', {'candidato': candidato})


@gestor_required
def atualizar_anotacoes(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == "POST":
        anotacoes = request.POST.get("anotacoes", "")
        candidato.anotacoes = anotacoes
        candidato.save()

        messages.success(request, "Anotações salvas com sucesso")

        page = request.POST.get("page", "")
        estado = request.POST.get("estado", "")
        formacao = request.POST.get("formacao", "")
        area = request.POST.get("area", "")

        params = {}
        if page: params["page"] = page
        if estado: params["estado"] = estado
        if formacao: params["formacao"] = formacao
        if area: params["area"] = area

        url = reverse("gestor-dashboard")
        if params:
            url += "?" + urlencode(params)

        return redirect(url)

    return redirect("gestor-dashboard")

@gestor_required
def atualizar_status(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == "POST":
        novo_status = request.POST.get("status")

        if novo_status:
            candidato.status = novo_status
            candidato.save()
            messages.success(request, "Status salvo com sucesso")

        page = request.POST.get("page", "")
        estado = request.POST.get("estado", "")
        formacao = request.POST.get("formacao", "")
        area = request.POST.get("area", "")

        params = {}
        if page:
            params["page"] = page
        if estado:
            params["estado"] = estado
        if formacao:
            params["formacao"] = formacao
        if area:
            params["area"] = area

        url = reverse("gestor-dashboard")
        if params:
            url += "?" + urlencode(params)

        return redirect(url)

    return redirect("gestor-dashboard")

# Consulta de status pelo usuário (onde ele vai digitar o email)
def consultar_status(request):
    candidato = None
    erro = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            erro = "Informe um email."
        else:
            candidato = (
                Candidato.objects
                .filter(email__iexact=email)
                .order_by("-data_criacao")
                .first()
            )

            if not candidato:
                erro = "Nenhuma candidatura encontrada para este email."

    return render(
        request,
        "consultar_status.html",
        {
            "candidato": candidato,
            "erro": erro
        }
    )

# ---------------------- ENTREVISTA ---------------------- #

QUESTIONARIO_COMUM = [
    "Apresentação e clareza ao se comunicar",
    "Organização do raciocínio",
    "Postura profissional",
    "Conhecimento geral da área",
    "Capacidade de resolver problemas",
]

QUESTIONARIO_POR_AREA = {
    "CONT_I": [
        "Conhecimento básico de contabilidade",
        "Noções de conciliação e lançamentos",
    ],
    "CONT_II": [
        "Análise de demonstrações contábeis",
        "Conhecimento de rotinas fiscais/contábeis",
    ],
    "CONT_III": [
        "Capacidade de liderança técnica em contabilidade",
        "Experiência com fechamento e auditorias internas",
    ],
    "AUD_I": [
        "Noções básicas de auditoria",
        "Conhecimento de controles internos",
    ],
    "AUD_II": [
        "Planejamento de auditoria e testes",
        "Identificação de riscos e recomendações",
    ],
    "AUD_III": [
        "Estratégia de auditoria e visão de risco",
        "Experiência com auditoria externa/interna avançada",
    ],
}

OPCOES_NOTA = [
    ("RUIM", "Ruim"),
    ("MEDIO", "Médio"),
    ("DESEJAVEL", "Desejável"),
    ("MUITO_BOM", "Muito bom"),
]

# ----- Páginas do gestor -----

@gestor_required
def entrevistas_lista(request):
    candidatos_qs = Candidato.objects.filter(
        Q(status=Candidato.STATUS_ENTREVISTA) | Q(entrevista__isnull=False)
    ).distinct().order_by("id")

    paginator = Paginator(candidatos_qs, 10)
    page_number = request.GET.get("page")
    candidatos = paginator.get_page(page_number)

    return render(request, "entrevistas_lista.html", {"candidatos": candidatos})

@gestor_required
def entrevista_detalhe(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if candidato.status != Candidato.STATUS_ENTREVISTA and not hasattr(candidato, "entrevista"):
        return redirect("entrevistas-lista")

    avaliacao, _ = EntrevistaAvaliacao.objects.get_or_create(candidato=candidato)

    perguntas_comuns = QUESTIONARIO_COMUM
    perguntas_especificas = QUESTIONARIO_POR_AREA.get(candidato.area, [])

    # --------- PREFILL (carrega o que já foi salvo) ---------
    respostas_salvas = avaliacao.respostas or {}
    comuns_salvos = respostas_salvas.get("comum", []) or []
    especificos_salvos = respostas_salvas.get("especifico", []) or []

    def montar_itens(perguntas, salvos):
        itens = []
        for i, pergunta in enumerate(perguntas):
            nota = ""
            obs = ""
            if i < len(salvos) and isinstance(salvos[i], dict):
                nota = salvos[i].get("nota", "") or ""
                obs = salvos[i].get("observacao", "") or ""
            itens.append({"pergunta": pergunta, "nota": nota, "observacao": obs})
        return itens

    comum_itens = montar_itens(perguntas_comuns, comuns_salvos)
    especifico_itens = montar_itens(perguntas_especificas, especificos_salvos)

    # --------- POST (salvar) ---------
    if request.method == "POST":
        comum = []
        especifico = []

        # Respostas comuns
        for idx, pergunta in enumerate(perguntas_comuns):
            nota = request.POST.get(f"comum_nota_{idx}", "")
            obs = request.POST.get(f"comum_obs_{idx}", "").strip()
            comum.append({
                "pergunta": pergunta,
                "nota": nota,
                "observacao": obs
            })

        # Respostas específicas
        for idx, pergunta in enumerate(perguntas_especificas):
            nota = request.POST.get(f"esp_nota_{idx}", "")
            obs = request.POST.get(f"esp_obs_{idx}", "").strip()
            especifico.append({
                "pergunta": pergunta,
                "nota": nota,
                "observacao": obs
            })

        # Atualiza avaliação
        decisao = request.POST.get(
            "decisao",
            EntrevistaAvaliacao.DECIDIR_DEPOIS
        )

        avaliacao.respostas = {
            "comum": comum,
            "especifico": especifico
        }
        avaliacao.decisao = decisao
        avaliacao.entrevistado = True
        avaliacao.save()

        # REGRA DE NEGÓCIO CENTRALIZADA
        if decisao == EntrevistaAvaliacao.APROVADO:
            candidato.status = Candidato.STATUS_APROVADO
        elif decisao == EntrevistaAvaliacao.REPROVADO:
            candidato.status = Candidato.STATUS_REPROVADO
        elif decisao == EntrevistaAvaliacao.NAO_COMPARECEU:
            candidato.status = Candidato.STATUS_NAO_COMPARECEU
        else:
            # Decidir depois → continua em entrevista
            candidato.status = Candidato.STATUS_ENTREVISTA

        candidato.save()

        messages.success(request, "Avaliação salva com sucesso")
        return redirect("entrevistas-lista")

    context = {
        "candidato": candidato,
        "avaliacao": avaliacao,
        "opcoes_nota": OPCOES_NOTA,
        "decisoes": EntrevistaAvaliacao.DECISAO_CHOICES,
        "comum_itens": comum_itens,
        "especifico_itens": especifico_itens,
    }
    return render(request, "entrevista_detalhe.html", context)

# ---------------------- CARREIRA PAGE ---------------------- #

def carreira(request):
    return render(request, 'carreira.html')

def gestor_logout(request):
    request.session.flush()
    return redirect('home')

@gestor_required
def excluir_entrevista(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == "POST":
        # apaga a entrevista (se existir)
        if hasattr(candidato, "entrevista"):
            candidato.entrevista.delete()

        # muda o status para sair da lista
        candidato.status = Candidato.STATUS_SUBMETIDO 
        candidato.save()

        messages.success(request, "Entrevista excluída com sucesso")

    # volta para a mesma página
    next_url = request.POST.get("next") or "entrevistas-lista"
    return redirect(next_url)