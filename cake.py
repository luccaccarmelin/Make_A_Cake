import winsound
import time
import os
import msvcrt  # Para capturar qualquer tecla

# ==========================
# FUNÇÃO CLEAR
# ==========================
def limpar():
    os.system("cls" if os.name == "nt" else "clear")

# ==========================
# FUNÇÃO ESPERA QUALQUER TECLA
# ==========================
def qualquer_tecla():
    msvcrt.getch()

# ==========================
# CONFIGURAÇÃO DO JOGO
# ==========================
LUGARES = {
    "geladeira": {"ovos": 6, "leite": 2},
    "armario": {"farinha": 3, "acucar": 3, "cacau": 2},
    "bancada": {},
    "forno": {},
    "pia": {}
}

RECEITAS = {
    "bolo": {
        "ingredientes": {
            "ovos": 2,
            "leite": 1,
            "farinha": 2,
            "acucar": 1,
            "cacau": 1
        },
        "etapas": ["misturar", "assar"]
    }
}

inventario = {}
for lugar in LUGARES.values():
    for item in lugar:
        inventario[item] = 0

# ==========================
# FUNÇÕES DE SOM
# ==========================
def som_pegar_item():
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

def som_misturar():
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

def som_assar():
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)

def som_erro():
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)

# ==========================
# ESTADO DO BOLO
# ==========================
bolo_pronto = False
bolo_etapa = None
pote = {}

# ==========================
# INÍCIO DO JOGO
# ==========================
limpar()
print("Make a Cake! (Versao-0.1)")
time.sleep(1)
limpar()

while True:
    limpar()
    print("\nCOZINHA :: ", end="")
    for i, lugar in enumerate(LUGARES.keys(), 1):
        print(f"{i} - {lugar}", end=" | ")
    print("0 - Sair")

    escolha = input("\nIr para... ").lower()

    if escolha == "0":
        break

    if escolha.isdigit() and 1 <= int(escolha) <= len(LUGARES):
        lugar_atual = list(LUGARES.keys())[int(escolha)-1]
    else:
        continue

    while True:
        limpar()
        print(f"Você está em {lugar_atual.upper()} ::")
        
        # ==========================
        # Geladeira / Armário
        # ==========================
        if lugar_atual in ["geladeira", "armario"]:
            itens = list(LUGARES[lugar_atual].keys())
            if not itens:
                print("Não há itens disponíveis aqui.")
            else:
                for i, item in enumerate(itens, 1):
                    print(f"{i} - {item} ({LUGARES[lugar_atual][item]})")
            print("0 - Voltar")
            opc = input("Pegar... ").lower()
            if opc == "0":
                break
            elif opc.isdigit() and 1 <= int(opc) <= len(itens):
                item = itens[int(opc)-1]
                inventario[item] += 1
                LUGARES[lugar_atual][item] -= 1
                som_pegar_item()
                print(f"Você pegou {item}! Total no inventário: {inventario[item]}")
                qualquer_tecla()
                if LUGARES[lugar_atual][item] <= 0:
                    del LUGARES[lugar_atual][item]
            else:
                som_erro()
                print("Ação inválida!")
                qualquer_tecla()

        # ==========================
        # Bancada (misturar)
        # ==========================
        elif lugar_atual == "bancada":
            if all(inventario.get(i,0) >= q for i,q in RECEITAS["bolo"]["ingredientes"].items()) and bolo_etapa != "assar":
                print("Você pode misturar os ingredientes para o bolo!")
                print("1 - Misturar tudo no pote")
            elif bolo_etapa == "assar":
                print("Os ingredientes já estão misturados! Leve ao forno para assar.")
            else:
                print("Faltam ingredientes para misturar.")
            print("0 - Voltar")
            opc = input("Escolha... ").lower()
            if opc == "0":
                break
            elif opc == "1" and all(inventario.get(i,0) >= q for i,q in RECEITAS["bolo"]["ingredientes"].items()):
                for item,q in RECEITAS["bolo"]["ingredientes"].items():
                    inventario[item] -= q
                    pote[item] = q
                bolo_etapa = "assar"
                som_misturar()
                print("Você misturou todos os ingredientes no pote!")
                qualquer_tecla()
            else:
                som_erro()
                print("Não foi possível misturar!")
                qualquer_tecla()

        # ==========================
        # Forno (assar)
        # ==========================
        elif lugar_atual == "forno":
            if bolo_etapa == "assar":
                print("Você pode assar o bolo!")
                print("1 - Assar bolo")
            else:
                print("Nada para assar ainda.")
            print("0 - Voltar")
            opc = input("Escolha... ").lower()
            if opc == "0":
                break
            elif opc == "1" and bolo_etapa == "assar":
                bolo_etapa = None
                bolo_pronto = True
                pote = {}
                som_assar()
                print("Voce fez um bolo! Obrigado por jogar Make_a_Cake 0.1")
                qualquer_tecla()
            else:
                som_erro()
                print("Não é possível assar ainda!")
                qualquer_tecla()

        # ==========================
        # Pia (decorativa)
        # ==========================
        elif lugar_atual == "pia":
            print("A pia está limpa, mas não serve para misturar o bolo ainda")
            print("0 - Voltar")
            opc = input("Escolha... ").lower()
            if opc == "0":
                break

        time.sleep(0.2)
        limpar()

limpar()
print("Saindo da cozinha...")