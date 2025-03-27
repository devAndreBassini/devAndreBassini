def carregar_tabela_instrucoes():
    # Retorna um dicionário contendo as instruções com seus respectivos códigos hexadecimais
    # O dicionário mapeia o nome da instrução para o código hexadecimal correspondente
    return {
        "zeroL": "0",
        "umL": "1",
        "copiaA": "2",
        "copiaB": "3",
        "nA": "4",
        "nB": "5",
        "AenB": "6",
        "nAeB": "7",
        "AxB": "8",
        "nAxnB": "9",
        "nAxnBn": "A",
        "AeB": "B",
        "AeBn": "C",
        "AoBn": "D",
        "AoB": "E",
        "nAonBnB": "F"
    }


def extrair_valor(linha, numero_linha, variavel):
    try:
        # Divide a linha pela string '=', pega a segunda parte e remove o ';' no final
        valor = linha.split("=")[1].strip(";")

        # Se o valor for numérico (dígitos de 0 a 9)
        if valor.isdigit():
            # Converte o valor para inteiro
            valor_int = int(valor)
            # Converte o valor inteiro para hexadecimal, remove o prefixo '0x' e retorna em maiúsculas
            return hex(valor_int)[2:].upper()

        # Se o valor for uma letra hexadecimal de A a F (insensível a maiúsculas)
        elif all(c in "ABCDEF" for c in valor.upper()):
            # Retorna o valor em maiúsculas
            return valor.upper()

    except ValueError:
        # Se ocorrer erro na conversão, imprime mensagem de erro e retorna None
        print(
            f"Erro na linha {numero_linha}: Valor inválido encontrado em {variavel}: {linha}")
        return None


def processar_arquivo_ula():
    # Arquivos de entrada e saída
    arquivo_entrada = "testeula.ula"
    arquivo_saida = "testeula.hex"

    # Carrega a tabela de instruções
    tabela_instrucoes = carregar_tabela_instrucoes()
    inicio = False
    valor_x = None
    valor_y = None

    # Abre o arquivo de entrada para leitura e o arquivo de saída para escrita
    with open(arquivo_entrada, "r") as entrada, open(arquivo_saida, "w") as saida:
        # Itera sobre cada linha do arquivo de entrada
        for numero_linha, linha in enumerate(entrada, start=1):
            linha = linha.strip()  # Remove espaços em branco no início e no final da linha

            # Quando encontra a palavra "inicio:", ativa a flag de início
            if linha == "inicio:":
                inicio = True
                continue

            # Quando encontra a palavra "fim.", termina o processamento
            if linha == "fim.":
                break

            # Se não estiver no bloco de instruções ou a linha estiver vazia, pula
            if not inicio or not linha:
                continue

            # Se a linha começar com "X=", extrai o valor de X
            if linha.startswith("X="):
                valor_x = extrair_valor(linha, numero_linha, "X")
                continue

            # Se a linha começar com "Y=", extrai o valor de Y
            if linha.startswith("Y="):
                valor_y = extrair_valor(linha, numero_linha, "Y")
                continue

            # Se a linha começar com "W=", processa a instrução W
            if linha.startswith("W="):
                # Pega o código da instrução e remove o ponto e vírgula
                codigo_instrucao = linha.split("=")[1].strip(";")

                # Se a instrução não estiver na tabela, imprime erro e continua
                if codigo_instrucao not in tabela_instrucoes:
                    valor_W = None
                    print(
                        f"Erro na linha {numero_linha}: Instrução desconhecida: {codigo_instrucao}")
                    continue

                # Pega o valor hexadecimal da instrução a partir da tabela
                valor_w = tabela_instrucoes[codigo_instrucao]

                # Se os valores de X e Y foram definidos, escreve a linha no formato desejado
                if valor_x is not None and valor_y is not None:
                    # Formata os valores de X, Y e W como hexadecimal e escreve no arquivo de saída
                    linha_hex = f"{valor_x}{valor_y}{valor_w}"
                    saida.write(linha_hex + "\n")

if __name__ == "__main__":
    # Chama a função principal para processar o arquivo
    processar_arquivo_ula()

