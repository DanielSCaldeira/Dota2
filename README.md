# Dota2 - Análise de Dados em Tempo Real

Este projeto realiza análise de dados de partidas do Dota 2 em tempo real utilizando a API pública do [OpenDota](https://docs.opendota.com/). O objetivo é obter informações detalhadas sobre os jogadores, heróis e itens mais comuns utilizados em partidas recentes.

## Funcionalidades

- Consulta de informações de partidas do Dota 2 por ID.
- Análise automática dos heróis e itens mais utilizados por cada jogador em uma partida.
- Probabilidade de cada item ser feito por herói/jogador, baseada no histórico recente.
- Utilização de cache para otimizar requisições à API do OpenDota.
- API desenvolvida com FastAPI, pronta para integração com frontend ou outras aplicações.

## Como usar

1. **Crie o ambiente virtual:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instale as dependências:**
   ```
   pip install fastapi uvicorn requests
   pip freeze > requirements.txt
   ```

3. **Execute o servidor FastAPI:**
   ```
   uvicorn backend.api.open_dota_router:router --reload
   ```

4. **Faça uma requisição para iniciar a análise de uma partida:**
   ```
   GET /analise-heroi/{match_id}
   ```
   Substitua `{match_id}` pelo ID da partida desejada.

## Estrutura do Projeto

- `backend/api/open_dota_router.py`: Código principal da API, responsável por buscar e processar os dados das partidas.
- `README.md`: Este arquivo.

## Observações

- É necessário ter uma conexão com a internet para acessar a API do OpenDota.
- O projeto pode ser expandido para incluir outras análises ou integração com bancos de dados.

---

Sinta-se à vontade para contribuir ou sugerir melhorias!