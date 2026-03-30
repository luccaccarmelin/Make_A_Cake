import winsound
import time
import os

# ======================================================
# UTILIDADES
# ======================================================

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def pausa(s=1):
    time.sleep(s)

def som(tipo):
    sons = {
        "pegar": "SystemAsterisk",
        "misturar": "SystemExclamation",
        "assar": "SystemHand",
        "erro": "SystemHand"
    }
    winsound.PlaySound(sons.get(tipo, "SystemAsterisk"),
                       winsound.SND_ALIAS | winsound.SND_ASYNC)

# ======================================================
# CONFIGURAÇÃO
# ======================================================

LUGARES = {
    "geladeira": {"ovos": 6, "leite": 2},
    "armario": {"farinha": 3, "acucar": 3, "cacau": 2},
    "bancada": {},
    "forno": {},
    "pia": {}
}

RECEITA = {
    "ovos": 2,
    "leite": 1,
    "farinha": 2,
    "acucar": 1,
    "cacau": 1
}

inventario = {item: 0 for lugar in LUGARES.values() for item in lugar}
inventario["massa"] = 0

torneira_aberta = False
tempo_torneira = None

forno_ligado = False
tempo_forno = None

jogo_ativo = True

# ======================================================
# INVENTARIO
# ======================================================

def abrir_inventario(local):
    while True:
        limpar()
        print("INVENTARIO\n")
        itens = [i for i, q in inventario.items() if q > 0]

        if not itens:
            print("Vazio\n")
        else:
            for i, item in enumerate(itens, 1):
                print(f"{i}-{item} ({inventario[item]})")

        print("\n[*] - Dropar tudo")
        print("[0] - Voltar")

        escolha = input("\nDropar... ").strip().lower()

        if escolha == "*":
            for item in itens[:]:
                qtd = inventario[item]
                LUGARES[local][item] = LUGARES[local].get(item, 0) + qtd
                inventario[item] = 0
                print(f"Voce dropou {qtd} {item.upper()}")
            pausa(1)
            continue

        if escolha == "0":
            break

        pegar_tudo = False
        if escolha.endswith("*"):
            pegar_tudo = True
            escolha = escolha[:-1]

        item_escolhido = None

        if escolha.isdigit() and 1 <= int(escolha) <= len(itens):
            item_escolhido = itens[int(escolha)-1]
        elif escolha in itens:
            item_escolhido = escolha

        if item_escolhido:
            qtd = inventario[item_escolhido] if pegar_tudo else 1
            inventario[item_escolhido] -= qtd
            LUGARES[local][item_escolhido] = LUGARES[local].get(item_escolhido, 0) + qtd
            print(f"Voce dropou {qtd} {item_escolhido.upper()}")
            pausa(1)
        else:
            print("Opcao invalida.")
            pausa(1)

# ======================================================
# INÍCIO
# ======================================================

limpar()
print("Make a Cake - Versao 0.2")
pausa(1.5)

while jogo_ativo:

    if torneira_aberta and time.time() - tempo_torneira >= 10:
        limpar()
        print("A casa inundou.")
        print("\nFINAL PIA?...")
        break

    if forno_ligado and time.time() - tempo_forno >= 10:
        limpar()
        print("O forno ficou ligado por tempo demais.")
        print("\nFINAL DO FOGO")
        break

    limpar()
    print("COZINHA\n")
    for i, lugar in enumerate(LUGARES.keys(), 1):
        print(f"{i}-{lugar}")
    print("[0]-Sair")

    escolha = input("\nIr para... ")

    if escolha == "0":
        break

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(LUGARES)):
        continue

    local = list(LUGARES.keys())[int(escolha)-1]

    # ======================================================
    # LOOP LOCAL
    # ======================================================

    while True:

        if torneira_aberta and time.time() - tempo_torneira >= 10:
            limpar()
            print("A casa inundou.")
            print("\nFINAL PIA?...")
            jogo_ativo = False
            break

        if forno_ligado and time.time() - tempo_forno >= 10:
            limpar()
            print("A cozinha pegou fogo.")
            print("\nFINAL DO FOGO")
            jogo_ativo = False
            break

        if local == "forno" and forno_ligado and "massa" in LUGARES["forno"]:
            limpar()
            print("FORNO\n")
            print("Assando...")
            pausa(2)
            print("\nO bolo ficou perfeito.")
            print("\nFINAL VERDADEIRO")
            jogo_ativo = False
            break

        limpar()
        print(f"{local.upper()}\n")

        itens_local = list(LUGARES[local].items())
        for i, (item, q) in enumerate(itens_local, 1):
            print(f"{i}-{item} ({q})")

        opcao_extra_inicio = len(itens_local) + 1

        if local == "bancada":
            print(f"[{opcao_extra_inicio}] - misturar")

        if local == "pia":
            status = "ABERTA" if torneira_aberta else "FECHADA"
            print(f"[{opcao_extra_inicio}] - torneira ({status})")

        if local == "forno":
            status = "LIGADO" if forno_ligado else "DESLIGADO"
            print(f"[{opcao_extra_inicio}] - forno ({status})")

        print("\n[.] - Inventario")
        print("[*] - Pegar tudo")
        print("[0] - Voltar")

        cmd = input("\n> ").strip().lower()

        if cmd == "0":
            break

        if cmd == ".":
            abrir_inventario(local)
            continue

        if cmd == "*":
            for item, qtd_disp in list(LUGARES[local].items()):
                inventario[item] += qtd_disp
                print(f"Voce pegou {qtd_disp} {item.upper()}")
                del LUGARES[local][item]
            pausa(1)
            continue

        pegar_tudo = False
        if cmd.endswith("*"):
            pegar_tudo = True
            cmd = cmd[:-1]

        total_opcoes = len(itens_local)

        if cmd.isdigit():
            numero = int(cmd)

            if 1 <= numero <= total_opcoes:
                item = itens_local[numero-1][0]
                qtd_disp = LUGARES[local][item]
                qtd = qtd_disp if pegar_tudo else 1

                inventario[item] += qtd
                LUGARES[local][item] -= qtd
                if LUGARES[local][item] <= 0:
                    del LUGARES[local][item]
                print(f"Voce pegou {qtd} {item.upper()}")
                pausa(1)

            elif numero == total_opcoes + 1:

                if local == "bancada":
                    pode = all(inventario[i] >= q for i, q in RECEITA.items())
                    if pode:
                        for i, q in RECEITA.items():
                            inventario[i] -= q
                        inventario["massa"] += 1
                        som("misturar")
                        print("\nVoce criou 1 MASSA.")
                    else:
                        print("\nIngredientes insuficientes.")
                    pausa(1)

                elif local == "pia":
                    if torneira_aberta:
                        torneira_aberta = False
                        print("\nVoce fechou a torneira.")
                    else:
                        torneira_aberta = True
                        tempo_torneira = time.time()
                        print("\nVoce abriu a torneira.")
                    pausa(1)

                elif local == "forno":
                    if forno_ligado:
                        forno_ligado = False
                        print("\nForno desligado.")
                    else:
                        forno_ligado = True
                        tempo_forno = time.time()
                        print("\nForno ligado.")
                    pausa(1)

if not jogo_ativo:
    pausa(2)

print("\nFim de jogo.")
