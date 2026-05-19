from django.contrib import admin
from .models import Cliente, Servico, Agendamento, SlotAgendamento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone', 'email')
    search_fields = ('nome', 'telefone', 'email')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'duracao')
    search_fields = ('descricao',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'servico',
        'data_agendamento',
        'horario_agendamento',
        'status'
    )

    list_filter = (
        'status',
        'data_agendamento',
        'servico'
    )

    search_fields = (
        'cliente__nome',
        'cliente__telefone',
        'servico__descricao'
    )


@admin.register(SlotAgendamento)
class SlotAgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'agendamento',
        'data_slot',
        'horario_slot'
    )

    list_filter = (
        'data_slot',
    )