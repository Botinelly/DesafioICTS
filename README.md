# DesafioICTS

A API foi criada pra ajudar o seu Chico a coletar e analisar os dados dos seus dispositivos!
API codificada usando Python através do framework Flask, onde as funções de retorno retornam JSON.

Estrutura:

- app
    - Controllers   #Controladores de rotas e códigos da API
    - Models    #Modelos das tabelas dos banco de dados
    __init__.py    #Controlador dos módulos acima
- run.py    #Script que roda a API



Pré-requisitos:
Python 3.9

Instalação:
0 - Faça o Download do repositório e abra um termina dentro da pasta

1 - Baixe o ambiente virtual do Python para a instalação ser bem limpa
      $ pip install virtualenv
      
2 - Crie um ambiente virtual para instalação dos pacotes
      $ virtualenv venv

3 - Instale o pacote de requerimentos usando o arquivo requirements.txt disponibilizado no repositório
      $ pip install -r requirements.txt
      
4 - Após os requerimentos instalados, rode a API.
      $ py run.py
      
      ![image](https://user-images.githubusercontent.com/13951346/121788574-3afe1980-cb9c-11eb-9593-8fadef758727.png)

      Se ver essa imagem, deu tudo certo e a API está instalada e funcional!
