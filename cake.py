import winsound
import time
import os

# ======================================================
# FUNCOES UTILITARIAS
# ======================================================

def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def pausa(segundos=1):
    time.sleep(segundos)


# ======================================================
# SISTEMA DE SOM
# ======================================================

def som(tipo):
    sons = {
        "pegar": "SystemAsterisk",
        "misturar": "SystemExclamation",
        "assar": "SystemHand",
        "erro": "SystemHand"
    }
    winsound.PlaySound(
        sons.get(tipo, "SystemAsterisk"),
        winsound.SND_ALIAS | winsound.SND_ASYNC
    )


# ======================================================
# CONFIGURACAO DO JOGO
# ======================================================

LUGARES = {
    "geladeira": {"ovos": 6, "leite": 2},
    "armario": {"farinha": 3, "acucar": 3, "cacau": 2},
    "bancada": {},
    "forno": {},
    "pia": {}
}

RECEITA_BOLO = {
    "ovos": 2,
    "leite": 1,
    "farinha": 2,
    "acucar": 1,
    "cacau": 1
}

inventario = {item: 0 for lugar in LUGARES.values() for item in lugar}

bolo_misturado = False
bolo_pronto = False


# ======================================================
# INICIO DO JOGO
# ======================================================

limpar()
print("Make a Cake - Versao 0.4")
pausa(1.5)

while True:
    limpar()
    print("COZINHA\n")

    for i, lugar in enumerate(LUGARES.keys(), 1):
        print(f"{i} - {lugar}")
    print("0 - Sair")

    escolha = input("\nIr para... ").lower().strip()

    if escolha == "0":
        break

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(LUGARES)):
        print("Lugar invalido.")
        pausa(1)
        continue

    lugar_atual = list(LUGARES.keys())[int(escolha) - 1]

    # ======================================================
    # GELADEIRA / ARMARIO
    # ======================================================

    if lugar_atual in ["geladeira", "armario"]:
        while True:
            limpar()
            print(f"Voce esta em {lugar_atual.upper()}\n")

            itens = LUGARES[lugar_atual]
            lista_itens = list(itens.keys())

            if not lista_itens:
                print("Nao ha itens disponiveis aqui.\n")
            else:
                for i, item in enumerate(lista_itens, 1):
                    print(f"{i} - {item} ({itens[item]})")

            print("0 - Voltar")

            opc = input("\nPegar... ").lower().strip()

            if opc == "0":
                break

            pegar_tudo = False

            # Detecta *
            if opc.endswith("*"):
                pegar_tudo = True
                opc = opc[:-1]

            item_escolhido = None

            # Escolha por numero
            if opc.isdigit() and 1 <= int(opc) <= len(lista_itens):
                item_escolhido = lista_itens[int(opc) - 1]

            # Escolha por nome
            elif opc in lista_itens:
                item_escolhido = opc

            if item_escolhido:
                quantidade_disponivel = itens[item_escolhido]

                if pegar_tudo:
                    quantidade_pega = quantidade_disponivel
                else:
                    quantidade_pega = 1

                inventario[item_escolhido] += quantidade_pega
                itens[item_escolhido] -= quantidade_pega

                if itens[item_escolhido] <= 0:
                    del itens[item_escolhido]

                som("pegar")

                nome_base = (
                    item_escolhido[:-1]
                    if item_escolhido.endswith("s")
                    else item_escolhido
                )

                print(f"\nVoce pegou {quantidade_pega} {nome_base.upper()}")
                pausa(1)

            else:
                som("erro")
                print("Acao invalida.")
                pausa(1)

    # ======================================================
    # BANCADA
    # ======================================================

    elif lugar_atual == "bancada":
        limpar()
        print("Voce esta na BANCADA\n")

        if bolo_pronto:
            print("O bolo ja esta pronto.")
            print("\n0 - Voltar")
            input()
            continue

        if not bolo_misturado:
            pode_misturar = all(
                inventario[i] >= q for i, q in RECEITA_BOLO.items()
            )

            if pode_misturar:
                print("Misturando ingredientes...")
                pausa(1.5)

                for item, q in RECEITA_BOLO.items():
                    inventario[item] -= q

                bolo_misturado = True
                som("misturar")
                print("Massa pronta. Leve ao forno.")
            else:
                print("Faltam ingredientes.")

        else:
            print("A massa ja esta pronta.")

        print("\n0 - Voltar")
        input()

    # ======================================================
    # FORNO
    # ======================================================

    elif lugar_atual == "forno":
        limpar()
        print("Voce esta no FORNO\n")

        if bolo_misturado and not bolo_pronto:
            print("Assando bolo...")
            pausa(2)
            som("assar")

            bolo_pronto = True
            bolo_misturado = False

            print("\nVoce fez um bolo.")
        elif bolo_pronto:
            print("O bolo ja foi feito.")
        else:
            print("Nao ha nada para assar.")

        print("\n0 - Voltar")
        input()

    # ======================================================
    # PIA
    # ======================================================

    elif lugar_atual == "pia":
        limpar()
        print("A pia esta limpa.")
        print("Nao serve para preparar o bolo.\n")
        print("0 - Voltar")
        input()


# ======================================================
# FINAL
# ======================================================

limpar()
print("Saindo da cozinha...")
