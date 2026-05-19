from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import Cliente, Servico, Agendamento, SlotAgendamento


HORARIOS_FIXOS = [
    '09:00', '09:30',
    '10:00', '10:30',
    '11:00', '11:30',
    '13:00', '13:30',
    '14:00', '14:30',
    '15:00', '15:30',
    '16:00', '16:30',
    '17:00', '17:30',
]


def home(request):
    return render(request, 'home.html')


def login_cliente(request):

    


    if request.method == 'POST':

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:

            cliente = Cliente.objects.get(email=email)

            senha_correta = check_password(
                senha,
                cliente.senha
            )

            if senha_correta:
                request.session.pop('admin_logado', None)

                request.session['cliente_id'] = cliente.id

                request.session['cliente_nome'] = cliente.nome

                return redirect('/painel/')

            else:

                return render(request, 'login.html', {
                    'erro': 'Senha inválida'
                })

        except Cliente.DoesNotExist:

            return render(request, 'login.html', {
                'erro': 'Usuário não encontrado'
            })

    return render(request, 'login.html')


def cadastro_cliente(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:

            return render(request, 'cadastro.html', {
                'erro': 'As senhas não coincidem'
            })

        email_existente = Cliente.objects.filter(
            email=email
        ).exists()

        if email_existente:

            return render(request, 'cadastro.html', {
                'erro': 'E-mail já cadastrado'
            })

        Cliente.objects.create(
            nome=nome,
            telefone=telefone,
            email=email,
           senha=make_password(senha)
        )

        return redirect('/')

    return render(request, 'cadastro.html')


def agendar_sem_cadastro(request):
    servicos = Servico.objects.all()
    data_selecionada = request.GET.get('data_agendamento')

    horarios_disponiveis = HORARIOS_FIXOS

    if data_selecionada:
        horarios_ocupados = SlotAgendamento.objects.filter(
            data_slot=data_selecionada
        ).values_list('horario_slot', flat=True)

        horarios_ocupados = [
            horario.strftime('%H:%M') for horario in horarios_ocupados
        ]

        horarios_disponiveis = [
            horario for horario in HORARIOS_FIXOS
            if horario not in horarios_ocupados
        ]

    return render(request, 'agendar.html', {
        'servicos': servicos,
        'data_selecionada': data_selecionada,
        'horarios_disponiveis': horarios_disponiveis
    })


def salvar_agendamento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        servico_id = request.POST.get('servico')
        data_agendamento = request.POST.get('data_agendamento')
        horario_agendamento = request.POST.get('horario_agendamento')

        servico = Servico.objects.get(id=servico_id)

        slots_necessarios = -(-servico.duracao // 30)

        horario_inicio = datetime.strptime(horario_agendamento, '%H:%M')

        slots = []

        for i in range(slots_necessarios):
            slot = horario_inicio + timedelta(minutes=30 * i)
            slots.append(slot.strftime('%H:%M'))

        conflito = SlotAgendamento.objects.filter(
            data_slot=data_agendamento,
            horario_slot__in=slots
        ).exists()

        if conflito:
            return redirect(f'/agendar/?data_agendamento={data_agendamento}')

        cliente = Cliente.objects.create(
        nome=nome,
        telefone=telefone

        )

        agendamento = Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            data_agendamento=data_agendamento,
            horario_agendamento=horario_agendamento,
            status='Agendado'
        )

        for slot in slots:
            SlotAgendamento.objects.create(
                agendamento=agendamento,
                data_slot=data_agendamento,
                horario_slot=slot
            )

        return redirect('/agendamento-confirmado/')

    return redirect('/agendar/')

def painel_cliente(request):

    cliente_id = request.session.get('cliente_id')

    if not cliente_id:
        return redirect('/login/')

    cliente = Cliente.objects.get(id=cliente_id)

    agendamentos = Agendamento.objects.filter(
        cliente=cliente
    ).order_by('data_agendamento', 'horario_agendamento')

    return render(request, 'painel.html', {
        'cliente': cliente,
        'agendamentos': agendamentos
    })


def logout_cliente(request):

    request.session.flush()

    return redirect('/')

def agendamento_confirmado(request):
    return render(request, 'agendamento_confirmado.html')

def cancelar_agendamento(request, agendamento_id):

    cliente_id = request.session.get('cliente_id')

    if not cliente_id:
        return redirect('/login/')

    agendamento = Agendamento.objects.get(
        id=agendamento_id,
        cliente_id=cliente_id
    )

    agendamento.status = 'Cancelado'
    agendamento.save()

    SlotAgendamento.objects.filter(
        agendamento=agendamento
    ).delete()

    return redirect('/painel/')

def agendar_cliente(request):

    cliente_id = request.session.get('cliente_id')

    if not cliente_id:
        return redirect('/login/')

    cliente = Cliente.objects.get(id=cliente_id)

    servicos = Servico.objects.all()

    data_selecionada = request.GET.get('data_agendamento')

    horarios_disponiveis = HORARIOS_FIXOS

    if data_selecionada:

        horarios_ocupados = SlotAgendamento.objects.filter(
            data_slot=data_selecionada
        ).values_list('horario_slot', flat=True)

        horarios_ocupados = [
            horario.strftime('%H:%M')
            for horario in horarios_ocupados
        ]

        horarios_disponiveis = [
            horario for horario in HORARIOS_FIXOS
            if horario not in horarios_ocupados
        ]

    return render(request, 'agendar_cliente.html', {
        'cliente': cliente,
        'servicos': servicos,
        'data_selecionada': data_selecionada,
        'horarios_disponiveis': horarios_disponiveis
    })

def salvar_agendamento_cliente(request):

    cliente_id = request.session.get('cliente_id')

    if not cliente_id:
        return redirect('/login/')

    cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':

        servico_id = request.POST.get('servico')

        data_agendamento = request.POST.get('data_agendamento')

        horario_agendamento = request.POST.get('horario_agendamento')

        servico = Servico.objects.get(id=servico_id)

        slots_necessarios = -(-servico.duracao // 30)

        horario_inicio = datetime.strptime(
            horario_agendamento,
            '%H:%M'
        )

        slots = []

        for i in range(slots_necessarios):

            slot = horario_inicio + timedelta(
                minutes=30 * i
            )

            slots.append(slot.strftime('%H:%M'))

        conflito = SlotAgendamento.objects.filter(
            data_slot=data_agendamento,
            horario_slot__in=slots
        ).exists()

        if conflito:

            return redirect(
                f'/meu-agendamento/?data_agendamento={data_agendamento}'
            )

        agendamento = Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            data_agendamento=data_agendamento,
            horario_agendamento=horario_agendamento,
            status='Agendado'
        )

        for slot in slots:

            SlotAgendamento.objects.create(
                agendamento=agendamento,
                data_slot=data_agendamento,
                horario_slot=slot
            )

        return redirect('/painel/')

def admin_painel(request):

    if not request.session.get('admin_logado'):
        return redirect('/login-admin/')

    status = request.GET.get('status')
    status_pagamento = request.GET.get('status_pagamento')
    data = request.GET.get('data')

    agendamentos = Agendamento.objects.all()

    if status:
        agendamentos = agendamentos.filter(status=status)

    if status_pagamento:
        agendamentos = agendamentos.filter(status_pagamento=status_pagamento)

    if data:
        agendamentos = agendamentos.filter(data_agendamento=data)

    agendamentos = agendamentos.order_by(
        'data_agendamento',
        'horario_agendamento'
    )

    return render(request, 'admin_painel.html', {
        'agendamentos': agendamentos,
        'status_filtro': status,
        'pagamento_filtro': status_pagamento,
        'data_filtro': data
    })

def login_admin(request):

    if request.method == 'POST':

        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        if usuario == 'admin' and senha == 'admin123':

            request.session['admin_logado'] = True

            return redirect('/admin-painel/')

        return render(request, 'login_admin.html', {
            'erro': 'Usuário ou senha inválidos'
        })

    return render(request, 'login_admin.html')

def logout_admin(request):

    request.session.pop('admin_logado', None)

    return redirect('/login-admin/')

def atualizar_pagamento(request, agendamento_id):

    if not request.session.get('admin_logado'):
        return redirect('/login-admin/')

    if request.method == 'POST':

        status_pagamento = request.POST.get('status_pagamento')

        agendamento = Agendamento.objects.get(id=agendamento_id)

        agendamento.status_pagamento = status_pagamento

        if status_pagamento in ['Pago', 'Pago antecipadamente']:
            agendamento.status = 'Concluido'

        agendamento.save()

    return redirect('/admin-painel/')

def admin_servicos(request):

    if not request.session.get('admin_logado'):
        return redirect('/login-admin/')

    servicos = Servico.objects.all().order_by('descricao')

    return render(request, 'admin_servicos.html', {
        'servicos': servicos
    })

def criar_servico(request):

    if not request.session.get('admin_logado'):
        return redirect('/login-admin/')

    if request.method == 'POST':

        descricao = request.POST.get('descricao')
        duracao = request.POST.get('duracao')

        Servico.objects.create(
            descricao=descricao,
            duracao=duracao
        )

    return redirect('/admin-servicos/')

def atualizar_servico(request, servico_id):

    if not request.session.get('admin_logado'):
        return redirect('/login-admin/')

    if request.method == 'POST':

        servico = Servico.objects.get(id=servico_id)

        servico.descricao = request.POST.get('descricao')
        servico.duracao = request.POST.get('duracao')
        servico.save()

    return redirect('/admin-servicos/')

def excluir_agendamento(request, agendamento_id):

    if not request.session.get('admin_logado'):
        return redirect('/login-admin/')

    agendamento = Agendamento.objects.get(id=agendamento_id)

    SlotAgendamento.objects.filter(
        agendamento=agendamento
    ).delete()

    agendamento.delete()

    return redirect('/admin-painel/')