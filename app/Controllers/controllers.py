from app import app
from app import db
import platform
import subprocess  
from flask import jsonify, request
from ..Models.models import Aparelho, Sensor

def ping(host):
    #Função pra dar um ping pelo terminal
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]

    #Subprocess chama o terminal e executa o comando ping com os parâmetros da variável command
    return subprocess.call(command) == 0

@app.route('/')
def home():
    return "API Online", 200

@app.route('/cria_banco')
def cria_banco():
    #RODAR ESSA PRIMEIRO! Primeira rota a ser rodada para criação do Banco de acordo com as classes criadas
    db.create_all()
    return ("Done!", 200)


"""------------------APARELHOS------------------"""
#rota que cria um novo Aparelho
@app.route('/cria_aparelho')
def criar_aparelho():
       
    nome = request.args.get('nome', type=str)
    comodo = request.args.get('comodo', type=str)
    ip = request.args.get('ip', type=str)
    consumo = request.args.get('consumo',type=int)
    
    #verifica se faltam dados
    if nome == None or comodo == None or ip == None or consumo == None:
        return ("Dados faltando, reenvie", 200)
    else:
        #instancia um novo objeto da classe Aparelho
        novo = Aparelho(nome=nome, comodo=comodo, ip=ip, consumo=consumo)
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do Flask_SQLAlchemy
        db.session.add(novo)
        db.session.commit()
        novo = None
        return "Novo aparelho inserido com sucesso!", 200
    
#Rota que atualiza dados de um aparelho existente
@app.route('/atualiza_aparelho')
def atualiza_aparelho():
    id = request.args.get('id', type=int)
    new_nome = request.args.get('nome', type=str)
    new_comodo = request.args.get('comodo', type=str)
    new_ip = request.args.get('ip', type=str)
    new_consumo = request.args.get('consumo',type=int)
    
    #verifica se faltam dados
    if new_nome == None or new_comodo == None or new_ip == None or new_consumo == None:
        return ("Dados faltando, reenvie", 200)
    else:
        #Atribui os dados do novo ao antigo aparelho
        old = Aparelho.query.filter_by(id=id).first()
        old.nome = new_nome
        old.comodo = new_comodo
        old.ip = new_ip
        old.consumo = new_consumo
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do Flask_SQLAlchemy
        db.session.add(old)
        db.session.commit()
        return ("Atualizado com sucesso!")

#Rota que remove um aparelho já existente
@app.route('/remove_aparelho')
def remove_aparelho():
    id = request.args.get('id', type=int)
    
    #verifica se faltam dados
    if id == None:
        return ("Dados faltando, reenvie", 200)
        
    else:
        old = Aparelho.query.filter_by(id=id).first()
        
        #comandos para deletar os dados do banco de dados SQLite3 através do Flask_SQLAlchemy
        db.session.delete(old)
        db.session.commit()
        return ("Removido com sucesso", 200)   
    
#Rota que lista o aparelho por Nome e ID
@app.route('/lista_nome_aparelho', methods=["POST", "GET"])
def lista_nome_aparelho():
    full_list = Aparelho.query.order_by(Aparelho.id, Aparelho.nome).all()
    
    #Dicionário para criação do arquivo JSON de retorno
    json = {"Items":[]}
    
    #Percorre todo o objeto da classe Aparelho e adiciona os respectivos ID's e Nomes ao dicionário
    for i in full_list:
        json["Items"].append([i.id, i.nome])
    
    #Converte para JSON e retorna o mesmo.    
    return jsonify(json), 200

#Rota que lista um aparelho específico por ID
@app.route('/lista_aparelho')
def lista_aparelho():
    id = request.args.get('id', type=int)
    
    ligado = True
    
    if id == None:
        return ("Dados faltando, reenvie", 200)
    else:
        obj = Aparelho.query.filter_by(id=id).first()
        
        #comando ping para saber se o objeto está ligado ou não
        ligado = "Ligado: " + str(ping(obj.ip))
        
        json = {"Items":[]}
        json["Items"].append([obj.id, obj.nome, obj.comodo, obj.ip, ligado, obj.consumo])

        return jsonify(json), 200


""" ---------------SENSORES DE TEMPERATURA---------------- """

#Rota para criação de sensores 
@app.route('/cria_sensor')
def cria_sensor():
  
    comodo = request.args.get('comodo', type=str)
    temp = request.args.get('temp',type=float)
    
    #verifica se faltam dados
    if comodo == None or temp == None:
        return ("Dados faltando, reenvie", 200)
    else:
        novo = Sensor(comodo=comodo, temp=temp)
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do Flask_SQLAlchemy
        db.session.add(novo)
        db.session.commit()
        novo = None
        return "Novo sensor inserido com sucesso!", 200

#Rota para listar todos os sensores existentes
@app.route('/lista_sensor')
def lista_sensor():
    full_list = Sensor.query.all()
    json = {"Sensores":[]}
    for i in full_list:
        json["Sensores"].append([i.comodo, i.temp])
    return jsonify(json), 200

#rota para atualizar a temperatura de um sensor já existente
@app.route('/atualiza_temperatura')
def atualiza_temperatura():
    id = request.args.get('id', type=int)
    new_temp = request.args.get('nome', type=float)
        
    #verifica se faltam dados
    if new_temp == None:
        return ("Dados faltando, reenvie", 200)
    else:
        old = Sensor.query.filter_by(id=id).first()
        old.temp = new_temp
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do Flask_SQLAlchemy
        db.session.add(old)
        db.session.commit()
        return ("Atualizado com sucesso!")

#Rota para verificação das maiores e menores temperaturas dos sensores
@app.route('/verifica_temp')
def verifica_temp():
    
    full_list = Sensor.query.all()
    
    maior = Sensor()
    menor = Sensor()
    
    #Percorre comparando a temperatura de todos os sensores cadastrados e armazena o maior e o menor
    for i in full_list:  
        if i.temp >= full_list[0].temp:
            maior = i
        if i.temp <= full_list[0].temp:
            menor = i
                    
    #Monta um json com a maior e menor temperatura, junto com seus respectivos cômodos
    json = {"Maior":[maior.comodo, maior.temp], "Menor":[menor.comodo, menor.temp]}
    return jsonify(json), 200
    
    
#Rota para remoção de um sensor já existente
@app.route('/remover_sensor')
def remover_sensor():
    id = request.args.get('id', type=int)
    
    #verifica se faltam dados
    if id == None:
        return ("Dados faltando, reenvie", 200)
        
    else:
        old = Sensor.query.filter_by(id=id).first()
        
        #comandos para deletar os dados do banco de dados SQLite3 através do Flask_SQLAlchemy
        db.session.delete(old)
        db.session.commit()
        return ("Removido com sucesso", 200)   
