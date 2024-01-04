# ******************************************************************************************
# Autora: Amanda Lima Bezerra
# Componente Curricular: MI - Algoritmos I
# Concluido em: 03/06/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# ******************************************************************************************


# Biblioteca para construir todas as linhas de comando.
import sys
# Biblioteca para manipular os arquivos e diretórios.
import os
# Biblioteca para copiar profundamente alguns dicionários
import copy

def menu():
    # Cada argumento da linha de comando é recebido como uma lista, por isso pego o segundo e o terceiro termo.
    try:            
        if sys.argv[1] == 'buscar' and sys.argv[2] != '':
            palavra_buscada = sys.argv[2]
            # Comentário para o usuário
            print('' if busca(palavra_buscada) else 'Não foi possível buscar a palavra.')
        elif sys.argv[1] == 'atualizar' and sys.argv[2] != '':
            diretorio = sys.argv[2]
            # Comentário para o usuário
            print('Atualização realizada com sucesso!' if atualizacao(diretorio) else 'Não foi possível atualizar o índice.')
        elif sys.argv[1] == 'adicionar' and sys.argv[2] != '':
            diretorio = sys.argv[2]
            # Comentário para o usuário
            print('Índice criado com sucesso!' if adicao(diretorio) else 'Não foi possível criar o índice.')
        elif sys.argv[1] == 'remover' and sys.argv[2] != '':
            diretorio_arquivo = sys.argv[2]
            # Comentário para o usuário
            print('Remoção feita com sucesso!' if remocao(diretorio_arquivo) else 'Não foi possível remover o item solicitado.')
        elif sys.argv[1] == 'mostrar' and sys.argv[2] == 'indice':
            # Comentário para o usuário
            print('' if mostrar() else 'Não foi possível mostrar o índice.')
        elif len(sys.argv) > 3:
            print('Número de argumentos acima do permitido.', end = '\n\n')
            ajuda()
        else:
            ajuda()
    except:
        print('Número de argumentos insuficiente.', end = '\n\n')
        ajuda()

def busca(palavra_buscada):
    # Função usada para buscar o índice no arquivo.
    try:
        dicionario_indice_invertido = buscando_indice()   
        if palavra_buscada in dicionario_indice_invertido:
            # Estrutura do dicionário {'palavra': [[arquivo, contador], ...]}
            matriz = dicionario_indice_invertido[palavra_buscada]
            quant_documentos = len(matriz)
            # Usando a lógica do selection sort para organizar a apresentação da busca.
            for linhas in range(len(matriz)):
                menor = matriz[linhas][1]
                linha_ref = matriz[linhas]
                for linha_seguinte in range(linhas + 1, len(matriz)):
                    if menor > matriz[linha_seguinte][1]:
                        matriz[linhas] = matriz[linha_seguinte]
                        matriz[linha_seguinte] = linha_ref
                        menor = matriz[linhas][1]
                        linha_ref = matriz[linhas]
            print('--' * 30, end = ' ')
            print('PALAVRA BUSCADA', end = ' ')
            print('--' * 30, end = '\n\n')
            print('ARQUIVOS................................QUANTIDADE')
            for linhas in range(len(matriz)):
                for colunas in range(2):
                    print(matriz[linhas][colunas], end = '')
                    print('', end = '\t\t\t')
                print('\n')
            print('Quantidade de arquivos achados com a palavra................................', quant_documentos)
        else:
            print('Palavra não encontrada no índice.')
        return True
    except:
        return False

def atualizacao(diretorio):
    try:
        # Salvando os nomes dos arquivos que serão atualizados e fazendo um dicionário auxiliar para comparar com o antigo índice.
        # Estrutura do dicionario_caminhos_atualizados {'Nome do arquivo.txt': 'Caminho do arquivo'}
        dicionario_caminhos_atualizados = listagem_arquivos(diretorio)
        # Estrutura do dicionario_indice_invertido_aux {'Palavra': [['Nome arquivo.txt', Contagem] ...]}
        dicionario_indice_invertido_aux = indice_invertido(dicionario_caminhos_atualizados)
        # índice invertido antigo
        dicionario_indice_invertido = buscando_indice()
        # Tirando qualquer referência dos arquivos para atualizar no índice.
        dicionario_indice_invertido = filtrar_arquivos(dicionario_caminhos_atualizados)
        dicionario_indice_invertido = comparar_dicionarios(dicionario_indice_invertido_aux, dicionario_indice_invertido)
        adicionar_indice_arquivo(dicionario_indice_invertido)
        return True
    except:
        return False 

def adicao(diretorio):
    try:
        # Listando os arquivos do diretório em um dicionário.
        dicionario_caminhos = listagem_arquivos(diretorio)   
        # Criando o índice 
        dicionario_indice_invertido = indice_invertido(dicionario_caminhos)
        # Salvando o índice em um arquivo
        adicionar_indice_arquivo(dicionario_indice_invertido)
        return True
    except:
        return False

def remocao(diretorio_arquivo):
    try:
        # Verificando se é uma pasta ou um único arquivo.
        root, ext = os.path.splitext(diretorio_arquivo)
        if ext == '.txt':
            # É um arquivo
            # Como eu não consegui separar o nome do arquivo do caminho eu coloquei como nome do arquivo 'ArquivoX'
            dicionario_caminhos['ArquivoX'] = diretorio_arquivo
        elif ext == '':
            # É uma pasta
            dicionario_caminhos = listagem_arquivos(diretorio_arquivo)
        # O mesmo procedimento para ambas as situações.
        dicionario_indice_invertido = filtrar_arquivos(dicionario_caminhos)
        adicionar_indice_arquivo(dicionario_indice_invertido)
        return True
    except:
        return False

def ajuda():
    print('--' * 30, end = ' ')
    print('AJUDA', end = ' ')
    print('--' * 30, end = '\n\n')
    print('-----> ORIENTAÇÕES:\
        \nO primeiro comando deve ser adicionar seguido por o nome do diretório entre aspas.\
        \nQualquer atualização ou remoção deve ser feito depois com outros comandos.\n')
    print('-----> ARGUMENTOS VÁLIDOS:\
        \nbuscar palavra - Buscar uma palavra\
        \n\tComando usado para buscar uma palavra no índice\
        \natualizar "caminho da pasta" - Atualizar documento\
        \n\tComando usado para atualizar o índice ou adicionar mais algum diretório ou arquivo\
        \nadicionar "caminho da pasta" - Adicionar documento\
        \n\tComando usado para criar o índice\
        \nremover "caminho da pasta ou arquivo" - Remover pasta ou documento\
        \n\tComando usado para remover uma pasta ou arquivo\
        \nmostrar indice\
        \n\tComando usado para mostrar todo índice\
        \n\n-----> OBSERVAÇÃO:\
        \nTodos os nomes das pastas ou arquivos devem estar entre aspas\
        \n')

def mostrar():
    try:
        dicionario_indice_invertido = buscando_indice()
        for tupla_indice in dicionario_indice_invertido.items():
            print(*tupla_indice)
        return True
    except:
        return False

def buscando_indice():
    # Função para buscar o índice no arquivo, usado o with pois ele abre e fecha o arquivo em um único comando.
    with open('Índice Invertido.txt', 'r', encoding = 'utf-8') as arquivo_indice:
        # O dicionário é sempre salvo em uma única linha no programa por isso o looping só vai rodar uma única vez.
        for indice in arquivo_indice.readlines():
            dicionario_indice_invertido = eval(indice)
    return dicionario_indice_invertido

def listagem_arquivos(diretorio):
    # Criação de um dicionário com os arquivos e o caminho para os mesmos.
    # Estrutura do dicionário {'Nome do arquivo.txt': 'Caminho do arquivo'}
    if os.path.exists(diretorio):
        dicionario_caminhos = {}
        # Função usada para separar os nome dos arquivos e os caminhos.
        for (caminho, nome_pasta, arquivo) in os.walk(diretorio):
            for nome_arquivos in arquivo:
                root, ext = os.path.splitext(nome_arquivos)
                # Filtrando os arquivos .txt
                if ext == '.txt':
                    caminho_arquivo = os.path.join(caminho, nome_arquivos)
                    dicionario_caminhos[nome_arquivos] = caminho_arquivo          
        return dicionario_caminhos

def indice_invertido(dicionario_caminhos):
    dicionario_indice_invertido = {}
    for arquivos_caminhos in dicionario_caminhos.items():
        # Usando o with pois ele abre e fecha o arquivo em um único comando.
        # Estrutura do dicionario_caminhos {'Nome do arquivo.txt': 'Caminho do arquivo'}
        with open(arquivos_caminhos[1], 'r', encoding = 'utf-8') as arquivo_indice:
            for linhas in arquivo_indice.readlines():
                # Filtrando as possíveis linhas vazias e as linhas só com \n
                if linhas != '' and linhas != '\n':
                    lista_palavras = linhas.lower().split()
                    # Filtrando qualquer pontuação que possa existir nos textos.
                    lista_indice = filtrar_caracteres(lista_palavras)
                    for palavras in lista_indice:
                        lista_informacoes = [arquivos_caminhos[0], 1]
                        if palavras in dicionario_indice_invertido:
                            # Se a palavra existe no dicionário tem dois caminhos possíveis: 
                            # ela está no mesmo arquivo ou em um arquivo diferente.
                            # Por isso a análise é feita a partir da última lista_informações colocada como chave do dicionário.
                            if dicionario_indice_invertido[palavras][-1][0] == arquivos_caminhos[0]:
                                dicionario_indice_invertido[palavras][-1][1] += 1
                            elif dicionario_indice_invertido[palavras][-1][0] != arquivos_caminhos[0]:
                                lista_aux = dicionario_indice_invertido[palavras]
                                lista_aux.append(lista_informacoes)
                        elif palavras not in dicionario_indice_invertido:
                            # Se a palavra não existe no dicionário.
                            lista_aux = []
                            lista_aux.append(lista_informacoes)
                            dicionario_indice_invertido[palavras] = lista_aux
    return dicionario_indice_invertido

def filtrar_caracteres(lista_palavras):
    # Filtrando somente símbolos.
    lista_indice = []
    for palavras in lista_palavras:
        if not palavras.isalpha():
            for letras in palavras:
                if not letras.isalpha() and not letras.isnumeric():
                    palavras = palavras.replace(letras, '')
        lista_indice.append(palavras)
    return lista_indice

def adicionar_indice_arquivo(dicionario_indice_invertido):
    # Função para adicionar o índice no arquivo.
    try:
        with open('Índice Invertido.txt', 'w', encoding = 'utf-8') as arquivo_indice:
            arquivo_indice.write(str(dicionario_indice_invertido))
    except:
        print('Não foi possível salvar o índice no arquivo.')

def comparar_dicionarios(dicionario_indice_invertido_aux, dicionario_indice_invertido):
    # dicionario_indice_invertido_aux == Índice desatualizado
    # dicionario_auxiliar == Índice atualizado
    for palavras_atualizadas in dicionario_indice_invertido_aux.items():
        # Analisando se a palavra está ou não no índice invertido 
        # Caso a palavra exista no índice invertido.
        if palavras_atualizadas[0] in dicionario_indice_invertido:
            # Analisando se as informações estão iguais ou não.
            for lista_informacoes in palavras_atualizadas[1]:
                # Se as informações estão iguais não precisa mudar, mas caso estejam diferentes precisam atualizar.
                if lista_informacoes not in dicionario_indice_invertido[palavras_atualizadas[0]]:
                    # Criando uma lista para verificar se o arquivo tinha a palavra no índice ou não
                    lista_arquivos = []
                    for indice_arquivo in range(len(dicionario_indice_invertido[palavras_atualizadas[0]])):
                        lista_arquivos.append(dicionario_indice_invertido[palavras_atualizadas[0]][indice_arquivo][0])
                    # Caso a quantidade de vezes que a palavra aparece mude no arquivo
                    if lista_informacoes[0] in lista_arquivos:
                        for indice_aux in range(len(dicionario_indice_invertido[palavras_atualizadas[0]])):
                            if dicionario_indice_invertido[palavras_atualizadas[0]][indice_aux][0] == lista_informacoes[0]:
                                dicionario_indice_invertido[palavras_atualizadas[0]][indice_aux] == lista_informacoes
                    # Caso a palavra seja nova no arquivo
                    elif lista_informacoes[0] not in lista_arquivos:
                        lista_aux = dicionario_indice_invertido[palavras_atualizadas[0]]
                        lista_aux.append(lista_informacoes)
                        dicionario_indice_invertido[palavras_atualizadas[0]] = lista_aux
        # Caso a palavra não exista no índice invertido.
        elif palavras_atualizadas[0] not in dicionario_indice_invertido:
            dicionario_indice_invertido[palavras_atualizadas[0]] = palavras_atualizadas[1]
    return dicionario_indice_invertido

def filtrar_arquivos(dicionario_caminhos):
    dicionario_indice_invertido = buscando_indice()
    for arquivo_caminho in dicionario_caminhos.items():
        nome_arquivo = arquivo_caminho[0]
        # Percorrendo o dicionário do índice invertido
        for palavras_arquivos in dicionario_indice_invertido.items():
            # Lista auxiliar para colocar todos as listas dos arquivos menos a dos arquivos para remover.
            lista_aux = []
            # Percorrendo a matriz da chave da palavra
            for lista_valor in palavras_arquivos[1]:
                if lista_valor[0] != nome_arquivo:
                    lista_aux.append(lista_valor)
            dicionario_indice_invertido[palavras_arquivos[0]] = lista_aux
    dicionario_auxiliar = copy.deepcopy(dicionario_indice_invertido)
    # Filtrando todas as palavras que não estão aparecendo mais nos arquivos.
    for palavras in dicionario_indice_invertido.items():
        if palavras[1] == []:
            dicionario_auxiliar.pop(palavras[0])
    dicionario_indice_invertido = dicionario_auxiliar
    return dicionario_indice_invertido

if __name__ == '__main__':
    menu()