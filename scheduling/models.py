from django.db import models


class Cliente(models.Model):

    nome = models.CharField(max_length=100)

    telefone = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True,
        null=True,
        unique=True
    )

    senha = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome


class Servico(models.Model):

    descricao = models.CharField(max_length=50)

    duracao = models.IntegerField()

    def __str__(self):
        return self.descricao


class Agendamento(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )

    data_agendamento = models.DateField()

    horario_agendamento = models.TimeField()

    status = models.CharField(
        max_length=20,
        default='Agendado'
    )
    status_pagamento = models.CharField(
    max_length=30,
    default='Pendente'
)




    def __str__(self):
        return f'{self.cliente.nome} - {self.data_agendamento}'


class SlotAgendamento(models.Model):

    agendamento = models.ForeignKey(
        Agendamento,
        on_delete=models.CASCADE
    )

    data_slot = models.DateField()

    horario_slot = models.TimeField()

    class Meta:
        unique_together = (
            'data_slot',
            'horario_slot'
        )