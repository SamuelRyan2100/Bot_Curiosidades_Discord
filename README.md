# Bot de Curiosidades e Utilidades 🤖

Bot de Discord feito em Python com a biblioteca discord.py.

## Funcionalidades
- `!ola`: cumprimenta o usuário pelo nome
- `!dado [lados]`: rola um dado (padrão: 6 lados)
- `!curiosidade`: envia uma curiosidade aleatória
- `!clima [cidade]`: mostra o clima atual usando a API wttr.in
- `!salvar [texto]`: salva uma nota pessoal em arquivo JSON
- `!notas`: lista as notas salvas
- Mensagem de boas-vindas para novos membros

## Como instalar
1. Clone o repositório
2. Crie e ative um ambiente virtual: `python -m venv venv`
3. Instale as dependências: `pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e coloque o token do seu bot
5. Execute: `python bot.py`

## Tecnologias
Python, discord.py, requests, python-dotenv

## Conceitos praticados
Funções, eventos, async/await, consumo de API, manipulação de arquivos
e tratamento de exceções.