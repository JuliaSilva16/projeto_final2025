import requests
from flask import request, redirect, make_response, jsonify

base_url = 'http://10.135.232.10:5001'


def post_login(login_response):
    try:
        url = f'{base_url}/login'
        response = requests.post(url, json=login_response)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Erro ao logar: {e}"}
    except Exception as e:
        return {'error': f"Erro interno: {e}"}


def post_cadastro(cadastro_response):
    try:
        url = f'{base_url}/usuarios'
        response = requests.post(url, json=cadastro_response)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Erro ao cadastrar: {e}"}
    except Exception as e:
        return {'error': f"Erro interno: {e}"}


def get_usuarios():
    try:
        url = f'{base_url}/alunos'
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Erro ao buscar usuários: {e}"}

    except Exception as e:
        return {'error': f"Erro interno: {e}"}


