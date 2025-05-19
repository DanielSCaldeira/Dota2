import pymem
import pymem.process
import time
import ctypes

PROCESS_NAME = "dota2.exe"

# Esses valores devem ser encontrados com o Cheat Engine
BASE_OFFSET = 0x12345678  # Ponteiro base da lista de jogadores (exemplo)
STRUCT_SIZE = 0x250       # Tamanho da estrutura por jogador
HERO_ID_OFFSET = 0x134    # Offset do Hero ID dentro da estrutura

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def safe_read_int(pm, address):
    try:
        return pm.read_int(address)
    except pymem.exception.MemoryReadError:
        return None
    except Exception as e:
        print(f"Erro inesperado na leitura de memória: {e}")
        return None

def main():
    if not is_admin():
        print("❌ Rode este script como administrador.")
        return

    try:
        pm = pymem.Pymem(PROCESS_NAME)
    except Exception:
        print(f"⚠️ Processo '{PROCESS_NAME}' não encontrado. Verifique se o jogo está aberto.")
        return

    try:
        module = pymem.process.module_from_name(pm.process_handle, PROCESS_NAME)
    except Exception as e:
        print(f"⚠️ Não foi possível obter o módulo do processo: {e}")
        return

    base_address = module.lpBaseOfDll + BASE_OFFSET
    print(f"✅ Monitorando picks da equipe. Base address: {hex(base_address)}")

    while True:
        try:
            for i in range(5):  # 5 jogadores da equipe
                player_base = base_address + (i * STRUCT_SIZE)
                hero_id = safe_read_int(pm, player_base + HERO_ID_OFFSET)
                if hero_id is None:
                    print(f"❌ Falha ao ler Hero ID do jogador {i + 1} (endereço: {hex(player_base + HERO_ID_OFFSET)})")
                else:
                    print(f"Jogador {i + 1}: Hero ID {hero_id}")
        except Exception as e:
            print(f"Erro inesperado na leitura de memória: {e}")
        print("-" * 30)
        time.sleep(1.75)

if __name__ == "__main__":
    main()
