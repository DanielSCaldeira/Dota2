from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
import requests
import time
from typing import List, Dict, Optional
from datetime import datetime
from time import time

router = APIRouter()
OPEN_DOTA_API = "https://api.opendota.com/api"

# Cache para não ficar repetindo requests
cache_itens = {}
cache_herois = {}

@router.get("/obter_lista_itens")
def obter_lista_itens() -> Dict[int, str]:
    global cache_itens
    if cache_itens:
        return cache_itens
    url = f"{OPEN_DOTA_API}/constants/items"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        cache_itens = {
            item_data["id"]: item_name.replace("_", " ").title()
            for item_name, item_data in data.items()
            if "id" in item_data
        }
    return cache_itens

@router.get("/obter_lista_herois")
def obter_lista_herois() -> Dict[int, str]:
    global cache_herois
    if cache_herois:
        return cache_herois
    url = f"{OPEN_DOTA_API}/constants/heroes"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        cache_herois = {
            hero_data["id"]: hero_data["localized_name"]
            for hero_data in data.values()
        }
    return cache_herois

@router.get("/obter_nome_jogador/{account_id}")
def obter_nome_jogador(account_id: int) -> str:
    url = f"{OPEN_DOTA_API}/players/{account_id}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("profile", {}).get("personaname", "Desconhecido")
    return "Desconhecido"

@router.get("/buscar_jogadores/match_id/{match_id}")
def buscar_jogadores(match_id: int):
    url = f"{OPEN_DOTA_API}/matches/{match_id}"
    for _ in range(3):
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data.get("players", [])
        time.sleep(3)
    return []

@router.get("/account_id/{account_id}/hero_id/{hero_id}")
def buscar_historico(account_id: int, hero_id: int, limit=20) -> List[Dict]:
    url = f"{OPEN_DOTA_API}/players/{account_id}/matches?hero_id={hero_id}&limit={limit}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return []

@router.get("/buscar_detalhes_partida/{match_id}")
def buscar_detalhes_partida(match_id: int) -> Dict:
    url = f"{OPEN_DOTA_API}/matches/{match_id}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return {}

def agrupar_itens(historico: List[Dict], account_id: int, itens_dict: Dict[int, str]) -> Dict[str, Dict]:
    contagem = {}
    partidas_validas = 0

    for partida in historico:
        detalhes = buscar_detalhes_partida(partida["match_id"])
        jogador = next(
            (p for p in detalhes.get("players", []) if p.get("account_id") == account_id),
            None
        )
        if not jogador:
            continue
        partidas_validas += 1
        for i in range(6):
            item_id = jogador.get(f"item_{i}")
            if item_id and item_id != 0:
                nome_item = itens_dict.get(item_id, f"Item {item_id}")
                if nome_item not in contagem:
                    contagem[nome_item] = {"vezes_feito": 0}
                contagem[nome_item]["vezes_feito"] += 1

    for item in contagem:
        vezes = contagem[item]["vezes_feito"]
        contagem[item]["probabilidade"] = round((vezes / partidas_validas) * 100, 2) if partidas_validas else 0.0

    return contagem

@router.get("/analise-heroi/{match_id}")
def analisar_herois_partida(match_id: int):
    return  processar_partida(match_id)

def processar_partida(match_id: int):
    jogadores = buscar_jogadores(match_id)
    itens_dict = obter_lista_itens()
    herois_dict = obter_lista_herois()
    resultado = []

    for jogador in jogadores:
        account_id = jogador.get("account_id")
        hero_id = jogador.get("hero_id")
        if not account_id or not hero_id:
            continue

        nome_jogador = obter_nome_jogador(account_id)
        nome_heroi = herois_dict.get(hero_id, f"Herói {hero_id}")
        historico = buscar_historico(account_id, hero_id)
        itens = agrupar_itens(historico, account_id, itens_dict)

        itens_formatados = [
            {
                "item": item,
                "vezes_feito": info["vezes_feito"],
                "probabilidade": info["probabilidade"]
            } for item, info in sorted(itens.items(), key=lambda x: x[1]["vezes_feito"], reverse=True)
        ]

        resultado.append({
            "account_id": account_id,
            "nome_jogador": nome_jogador,
            "hero_id": hero_id,
            "nome_heroi": nome_heroi,
            "itens_comuns": itens_formatados
        })

    print(f"Análise da partida {match_id} finalizada:")
    return JSONResponse(content=resultado)

@router.get("/buscar_partida_atual/account_id/{account_id}")
def buscar_partida_atual(account_id: int) -> Optional[Dict]:
    url = f"{OPEN_DOTA_API}/players/{account_id}/matches?limit=1"
    res = requests.get(url)
    
    if res.status_code != 200:
        print("Erro ao buscar partida")
        return None

    partidas = res.json()
    if not partidas:
        return None

    partida = partidas[0]
    
    agora = time()
    inicio = partida["start_time"]
    duracao = partida["duration"]
    tempo_total = inicio + duracao

    # A partida ainda está em andamento (possivelmente com atraso)
    if tempo_total > agora:
        return partida  # provável partida atual

    return None