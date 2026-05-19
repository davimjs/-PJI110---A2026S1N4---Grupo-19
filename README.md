# Salão de Beleza - Sistema Web de Agendamento

Sistema web desenvolvido em Python com Django, utilizando HTML5, CSS3 e SQLite, com o objetivo de realizar agendamentos de serviços de barbearia/salão.

O projeto contempla fluxo para cliente cadastrado, agendamento sem cadastro e painel administrativo básico.

---

## Objetivo

O sistema foi criado para permitir que clientes possam agendar serviços como corte, barba e corte + barba, respeitando a disponibilidade de horários.

Além disso, o sistema possui um painel administrativo para acompanhar agendamentos, alterar status de pagamento, gerenciar serviços e excluir registros.

---

## Tecnologias utilizadas

- Python
- Django
- HTML5
- CSS3
- SQLite

---

## Motivo da escolha da infraestrutura

### Python + Django

O Django foi escolhido por permitir desenvolvimento rápido, organizado e com boa estrutura MVC/MVT.

Ele fornece recursos importantes como:

- gerenciamento de rotas;
- views;
- models;
- migrations;
- templates HTML;
- integração nativa com SQLite;
- painel administrativo nativo;
- controle de sessão.

Como o prazo de desenvolvimento era curto, Django foi uma boa escolha por reduzir a necessidade de configuração manual e acelerar a construção do MVP.

### SQLite

O SQLite foi utilizado por ser simples, leve e não exigir instalação/configuração de servidor de banco de dados.

Para um MVP local, ele é suficiente e permite evoluir futuramente para PostgreSQL ou MySQL.

### HTML5 e CSS3

O frontend foi construído com HTML5 e CSS3 puro para manter simplicidade, velocidade de desenvolvimento e controle visual direto.

---

## Funcionalidades

### Cliente

- Cadastro opcional
- Login
- Sessão autenticada
- Agendamento com login
- Agendamento sem cadastro
- Painel do cliente
- Visualização de seus próprios agendamentos
- Cancelamento de agendamento

### Agendamento sem cadastro

O cliente pode agendar informando apenas:

- nome
- telefone
- serviço
- data
- horário

Nesse fluxo, o acompanhamento pela plataforma não fica disponível. O cliente deve acompanhar via WhatsApp informado na tela.

### Admin

- Login administrativo
- Painel administrativo próprio
- Visualização de todos os agendamentos
- Filtros por data, status e pagamento
- Alteração de status de pagamento
- Atualização automática de status do serviço para `Concluido` quando o pagamento é marcado como `Pago` ou `Pago antecipadamente`
- Exclusão de agendamentos
- Cadastro e edição de serviços disponíveis

---

## Estrutura principal do projeto

