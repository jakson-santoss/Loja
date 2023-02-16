from Funcoes import *
from Dbase import ClientesBD, CarrosBD, list_prod


def Reports(botao: str):
    """Exibe os relaórios.
    :param botao variável que define qual relatório será exibido."""
    if botao == 'carro':
        for kro in CarrosBD().read_task():
            sg.Print(f"{kro[1]} - {kro[2]}",
                     size=(50, 15), c='red', font=ftBd)
            sg.Print(f"\tAno: {kro[4]}    -   Cor:{kro[3]}",
                     c='black', font='any, 12')
            sg.Print(f"\tPlaca: {kro[0]}   -   Proprietário: {kro[5]}\n",
                     c='black', font='any, 12')
        sg.Print(f"Total: {len(CarrosBD().read_task())} Carros", c='blue', font='any, 18')

    elif botao == 'cliente':
        for cli in  ClientesBD().read_task():
            sg.Print(f"Documento: {cli[0]}", size=(50, 15), c='red', font='any, 16')
            sg.Print(f"{cli[1]}", c='black', font='any, 12')
            sg.Print(f"{cli[2]}", c='black', font='any, 12')
            sg.Print(f"Fone: {cli[3]}    -   Email : {cli[4]}\n",
                     c='black', font='any, 12')
        sg.Print(f"Total: {len( ClientesBD().read_task())} Clientes", c='blue', font='any, 18')

    elif botao == 'produto':
        for prod in list_prod():
            sg.Print(f"{prod[0]}  -  {prod[1]:30s}", c='black', font='any, 14', end='')
            sg.Print(f"\tR$ {float(prod[2]):.2f}", c='red', font='any, 16')
        sg.Print(f'Total: {len(list_prod())} produtos cadastrados', c='blue', font='any, 18')


def relatorio(botao: str):
    """Relatório em forma de tabela"""
    if botao == 'cliente':
        kbcalho = [' DOCUMENTO ', '  NOME  ', '  ENDEREÇO  ', ' FONE ', '  E-MAIL  ']
        event, values = sg.Window('', [
            [sg.StatusBar(' LISTA DE CARROS  ', font=['_', 14, 'bold'], justification='c', text_color='red')],
            [sg.Table([[clit[0], clit[1], clit[2], clit[3], clit[4]] for clit in  ClientesBD().read_task()], kbcalho,
                      font=['_', 12], justification='l')], [sg.HSep()],
            [sg.StatusBar(f'{len( ClientesBD().read_task())} Clientes cadastrados'), sg.OK(s=10)]], disable_close=True).read(close=True)
        if values[0]:
            print(list(ClientesBD().read_task()[values[0][0]]))
            return list(ClientesBD().read_task()[values[0][0]])
        else:
            return 'Não foi escolhido nenhum veículo'

    elif botao == 'carro':
        kbcalho = ['  PLACA  ', '  MARCA  ', '  MODELO  ', ' ANO ', '  COR  ', ' CLIENTE ']
        event, values = sg.Window('', [
            [sg.StatusBar(' LISTA DE CARROS  ', font=['_', 14, 'bold'], justification='c', text_color='red')],
            [sg.Table([[krro[0], krro[1], krro[2], krro[3], krro[4], krro[5]] for krro in CarrosBD().read_task()], kbcalho,
                      font=['_', 12], justification='l',
                  auto_size_columns=True,
                  display_row_numbers=True,
                  num_rows=10,
                  tooltip = 'tabela de cadastro de clientes',
                  #expand_x=True,
                  enable_events=True)], [sg.HSep()],
            [sg.StatusBar(f'{len(CarrosBD().read_task())} Veículos cadastrados'), sg.OK(s=10)]], disable_close=True).read(close=True)
        if values[0]:
            print(list(CarrosBD().read_task()[values[0][0]]))
            return list(CarrosBD().read_task()[values[0][0]])
        else:
            return 'Não foi escolhido nenhum veículo'

    elif botao == 'produto':
        kbcalho = ['  COD  ', '  DESCRIÇÃO  ', '  PREÇO  ']
        event, values = sg.Window('', [
            [sg.StatusBar(' LISTA DE PRODUTOS  ', font=['_', 14, 'bold'], justification='c', text_color='red')],
            [sg.Table([[prod[0], prod[1], f'R$ {float(prod[2]):.2f}'] for prod in list_prod()], kbcalho,
                      font=['_', 12], justification='l',
                  auto_size_columns=True,
                  num_rows=10,
                  tooltip = 'tabela de cadastro de produtos',
                  expand_x=True,
                  enable_events=True)], [sg.HSep()],
            [sg.StatusBar(f'{len(list_prod())} Produtos cadastrados'), sg.OK(s=10)]], disable_close=True).read(close=True)
        if values[0]:
            print(list(list_prod()[values[0][0]]))
            return list(list_prod()[values[0][0]])
        else:
            return 'Não foi escolhido nenhum Produto'


if __name__ == '__main__':
    Reports('produto')
    relatorio('produto')
