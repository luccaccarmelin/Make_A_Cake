import winsound
import time
import os

# =========================
# UTIL
# =========================

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def pausa(s=1):
    time.sleep(s)

def som(tipo):
    sons = {
        "acao": "SystemAsterisk",
        "misturar": "SystemExclamation",
        "final": "SystemHand"
    }
    winsound.PlaySound(sons.get(tipo, "SystemAsterisk"),
                       winsound.SND_ALIAS | winsound.SND_ASYNC)

# =========================
# CONFIG
# =========================

CAP_INVENTARIO = 10  # Máximo de itens no inventário

# Containers agora também tem limite
LUGARES = {
    "geladeira": {"itens": {"ovos": 6, "leite": 2}, "max_itens": 10},
    "armario": {"itens": {"farinha": 3, "acucar": 3, "cacau": 2}, "max_itens": 10},
    "bancada": {"itens": {}, "max_itens": 5},
    "forno": {"itens": {}, "max_itens": 2},
    "pia": {"itens": {}, "max_itens": 3}
}

RECEITA = {
    "ovos": 2,
    "leite": 1,
    "farinha": 2,
    "acucar": 1,
    "cacau": 1
}

# Inventário inicial vazio
inventario = {}
for lugar in LUGARES.values():
    for item in lugar["itens"]:
        inventario[item] = 0
inventario["massa"] = 0

torneira_aberta = False
tempo_torneira = 0
forno_ligado = False
tempo_forno = 0

# =========================
# UTILITÁRIOS DE CAPACIDADE
# =========================

def total_itens(container):
    return sum(container.values())

def pode_entrar(inventario_atual, qtd):
    """Retorna quanto cabe do total desejado no inventario"""
    total_atual = total_itens(inventario_atual)
    if total_atual >= CAP_INVENTARIO:
        return 0
    return min(qtd, CAP_INVENTARIO - total_atual)

# =========================
# INVENTÁRIO
# =========================

def abrir_inventario(local):
    while True:
        limpar()
        print("INVENTARIO\n")

        itens = [i for i, q in inventario.items() if q > 0]

        if not itens:
            print("VAZIO\n")
        else:
            for i, item in enumerate(itens, 1):
                print(f"{i}-{item} ({inventario[item]})")

        if total_itens(inventario) >= CAP_INVENTARIO:
            print("\nSeu inventario está cheio")

        print("\n[*] - Dropar tudo")
        print("[0] - Voltar")

        escolha = input("\nDropar... ").strip().lower()

        if escolha == "0":
            break

        if escolha == "*":
            for item in itens:
                qtd = inventario[item]
                lugar_itens = LUGARES[local]["itens"]
                max_cabem = LUGARES[local]["max_itens"] - total_itens(lugar_itens)
                pegar = min(qtd, max_cabem)
                if pegar > 0:
                    lugar_itens[item] = lugar_itens.get(item, 0) + pegar
                    inventario[item] -= pegar
                    print(f"Voce dropou {pegar} {item}.")
            pausa(1)

# =========================
# RECEITA COM ASCII
# =========================

def tela_receita():
    while True:
        limpar()
        print(r"""
                   _OZQznnnczXQmpppwwmZCn|]i".                            
                   Q@@@@@@@$$$BWMMMMMWB$@@@@@@@+                          
                   X@M~                  ."I+w@$+                         
                   z@M~ ^/M*-. .'``.    .'`' |@@f                         
                   z@M~(@*xw@bd$@@@$mcZM@@@@<}B@c                         
                   Y@M~     :{-'   ,/z|,     [W@c                         
                   0@o>                      1B@n                         
                   Z@ai "c#WWz`<jk#k<'{mMWz`.n@@1                         
                   Z@ai lCr>ja#apJfmMWa0(!' ,w@B,                         
                   Z@ai                     Io@k                          
                   Z@ai              `"'    i@@Y                          
                   Z@a+cahcQpX'  [X0#@@B0bkj{@@)                          
                   Z@ajaXQ#dcv.  }p0] :cdf)!f@@>                          
                   Z@ai                     f@@>                          
                   Z@ai                     (@@[                          
                   Z@ai  ^}z0r"             _@@f                          
                   J@M~ 'X@pcB@@@@@@@@@@@@@Q!B@Q                          
                   f@@[       ;++>;'I<<<<iI.;k@M.                         
                   _@@j.           "ZMw1pddf^C@$~                         
                   ,@@Q,^^^^^``.   ^Ykr+mOz1 ($@x                         
                    #@@@@@@@@@@@@BM##MB@@@@$WW@@X                         
                    .I~++++_]]1tz0wpppOzjjrYpbkw!                         
        """)
        print("\nReceita do Bolo:\n")
        for item, qtd in RECEITA.items():
            print(f"- {item} x{qtd}")
        print("\n[0] - Voltar")

        if input("\n> ") == "0":
            break

# =========================
# INÍCIO
# =========================

limpar()
print("Make a Cake - Versao 1.0")
pausa(1.5)

while True:

    # FINAL PIA
    if torneira_aberta and time.time() - tempo_torneira >= 10:
        limpar()
        print("A casa inundou.")
        print("\nFINAL DA PIA")
        som("final")
        break

    # FINAL FOGO
    if forno_ligado and time.time() - tempo_forno >= 15:
        limpar()
        print("A cozinha pegou fogo.")
        print("\nFINAL DO FOGO")
        som("final")
        break

    # FINAL VERDADEIRO
    if forno_ligado and "massa" in LUGARES["forno"]["itens"]:
        limpar()
        print("Assando...")
        pausa(3)
        print("\nO bolo ficou perfeito!")
        print("\nFINAL VERDADEIRO")
        som("final")
        break

    limpar()
    print("COZINHA\n")

    for i, lugar in enumerate(LUGARES.keys(), 1):
        print(f"{i}-{lugar}")

    print("[?] - Receita Bolo")
    print("[0] - Sair")

    escolha = input("\nIr para... ").strip().lower()

    if escolha == "0":
        break

    if escolha == "?":
        tela_receita()
        continue

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(LUGARES)):
        continue

    local = list(LUGARES.keys())[int(escolha)-1]

    # =========================
    # LOOP LOCAL
    # =========================

    while True:
        limpar()
        print(f"{local.upper()}\n")

        itens_local = list(LUGARES[local]["itens"].items())

        if not itens_local:
            print("VAZIO\n")
        else:
            for i, (item, q) in enumerate(itens_local, 1):
                print(f"{i}-{item} ({q})")

        opcao_extra = len(itens_local) + 1

        if local == "bancada":
            print(f"[{opcao_extra}] - misturar")

        if local == "pia":
            status = "ABERTA" if torneira_aberta else "FECHADA"
            print(f"[{opcao_extra}] - torneira ({status})")

        if local == "forno":
            status = "LIGADO" if forno_ligado else "DESLIGADO"
            print(f"[{opcao_extra}] - forno ({status})")

        print("\n[.] - Inventario")
        print("[*] - Pegar tudo")
        print("[0] - Voltar")

        cmd = input("\n> ").strip().lower()

        if cmd == "0":
            break

        if cmd == ".":
            if total_itens(inventario) >= CAP_INVENTARIO:
                print("Seu inventario está cheio")
                pausa(1)
            else:
                abrir_inventario(local)
            continue

        if cmd == "*":
            for item, qtd in list(LUGARES[local]["itens"].items()):
                cabem = pode_entrar(inventario, qtd)
                if cabem == 0:
                    print("Seu inventario está cheio")
                    pausa(1)
                    break
                inventario[item] += cabem
                LUGARES[local]["itens"][item] -= cabem
                print(f"Voce pegou {cabem} {item}.")
                if LUGARES[local]["itens"][item] <= 0:
                    del LUGARES[local]["itens"][item]
            pausa(1)
            continue

        # SUPORTE 1*, 2*, nome*
        pegar_tudo = False
        if cmd.endswith("*"):
            pegar_tudo = True
            cmd = cmd[:-1]

        item = None
        if cmd.isdigit() and 1 <= int(cmd) <= len(itens_local):
            item = itens_local[int(cmd)-1][0]
        elif cmd in dict(itens_local):
            item = cmd

        if item:
            qtd_disp = LUGARES[local]["itens"][item]
            qtd = qtd_disp if pegar_tudo else 1
            cabem = pode_entrar(inventario, qtd)
            if cabem == 0:
                print("Seu inventario está cheio")
                pausa(1)
                continue
            inventario[item] += cabem
            LUGARES[local]["itens"][item] -= cabem
            if LUGARES[local]["itens"][item] <= 0:
                del LUGARES[local]["itens"][item]
            print(f"Voce pegou {cabem} {item}.")
            pausa(1)
            continue

        # AÇÕES ESPECIAIS
        if cmd.isdigit() and int(cmd) == opcao_extra:

            if local == "bancada":
                pode = all(inventario[i] >= q for i, q in RECEITA.items())
                if pode:
                    for i, q in RECEITA.items():
                        inventario[i] -= q
                    inventario["massa"] += 1
                    print("Voce criou 1 MASSA.")
                    som("misturar")
                else:
                    print("Ingredientes insuficientes.")
                pausa(1)

            elif local == "pia":
                torneira_aberta = not torneira_aberta
                if torneira_aberta:
                    tempo_torneira = time.time()
                    print("Voce abriu a torneira.")
                else:
                    print("Voce fechou a torneira.")
                pausa(1)

            elif local == "forno":
                if inventario["massa"] > 0 and not forno_ligado:
                    if total_itens(LUGARES["forno"]["itens"]) < LUGARES["forno"]["max_itens"]:
                        inventario["massa"] -= 1
                        LUGARES["forno"]["itens"]["massa"] = 1
                        print("Voce colocou a massa no forno.")
                    else:
                        print("O forno está cheio")
                    pausa(1)
                    continue

                forno_ligado = not forno_ligado
                if forno_ligado:
                    tempo_forno = time.time()
                    print("Forno ligado.")
                else:
                    print("Forno desligado.")
                pausa(1)

print("\nFim de jogo.")
