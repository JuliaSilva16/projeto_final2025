# routes.py

import requests
from flask import request, redirect, make_response, jsonify

# ATENÇÃO: Use o IP e porta corretos da sua API
base_url = 'http://10.135.233.150:5001'


def post_login(login_response):
    try:
        url = f'{base_url}/login'
        response = requests.post(url, json=login_response)

        # Levanta exceção para 4xx ou 5xx
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        # Tenta pegar a mensagem de erro do JSON da API se o status for erro
        try:
            return {'error': response.json().get('msg') or response.json().get('erro')}
        except:
            return {'error': f"Erro ao logar: {e}"}


def post_cadastro(cadastro_response):
    try:
        url = f'{base_url}/usuarios'
        response = requests.post(url, json=cadastro_response)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        try:
            return {'error': response.json().get('msg') or response.json().get('erro')}
        except:
            return {'error': f"Erro ao cadastrar: {e}"}


def get_usuarios():
    try:
        url = f'{base_url}/alunos'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        try:
            return {'error': response.json().get('msg') or response.json().get('erro')}
        except:
            return {'error': f"Erro ao buscar usuários: {e}"}


def post_alimento(cadastro_alimento_response, token):  # <-- RECEBENDO O TOKEN AQUI
    """Cadastra um novo alimento, enviando o Token JWT para autenticação."""
    try:
        url = f'{base_url}/novo_alimento'

        # CABEÇALHOS COM AUTORIZAÇÃO (JWT)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=cadastro_alimento_response, headers=headers)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.HTTPError as e:
        # Trata erros específicos da API (ex: 403 Acesso Negado, 400 Campos obrigatórios)
        try:
            # Retorna a mensagem de erro do JSON da API
            error_details = response.json().get('msg') or response.json().get('erro')
            return {'error': error_details}
        except:
            return {'error': f"Erro HTTP {response.status_code}: Verifique permissões (Funcionário/Token)"}
    except requests.exceptions.RequestException as e:
        return {'error': f"Erro de conexão com a API: {e}"}


def get_alimento():
    """Busca a lista de alimentos."""
    try:
        url = f'{base_url}/alimento'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        try:
            return {'error': response.json().get('msg') or response.json().get('erro')}
        except:
            return {'error': f"Erro ao buscar alimentos: {e}"}