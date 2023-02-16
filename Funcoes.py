import PySimpleGUI as sg
from datetime import datetime as dt

carro, cliente, produto, odSv = {}, {}, {}, {}
hoje = f'{dt.now():%d/%m/%Y %H:%M}'
ftPd = ('_', 10)  # Fonte padrão para o programa
ftBt = ('_', 12, "bold")  # Fonte para Botões
ftBd = ('_', 16, "bold", "italic")  # Fonte para ...
ftTt = ("_", 20, "bold", "italic")  # Fonte para Títulos


def btn_menu(menu_list: list):
    """param menu_list Lista de comandos do botão de menu.
        Comando Sair já incluso com  o aliá 'r' e chave 'MENU::'
    return botão com fundo transparente e ☰ visível."""
    return sg.ButtonMenu('☰', ['⁝', [menu_list, 'Sai&r::']], k='MENU::',
                         button_color=sg.theme_background_color(), border_width=0)


def PopupDropDown(title: str, text: str, values: list):
    event, values = sg.Window(title, [[sg.T(text)], [sg.DropDown(values, key='-DROP-')],
                                      [sg.Ok(bind_return_key=True), sg.Cancel()]], keep_on_top=True).read(close=True)
    return None if event != 'Ok' else values['-DROP-']


def impressora_teste():
    """Ffunção para detectar impressoras intaladas em Sistema operacional Windows"""
    try:
        import win32api  # instalar pip pywin32
        import win32print
        '''Escolher qual impressora será ultilizada.'''
        list_printer = win32print.EnumPrinters(2)
        for imp in list_printer:
            print('Impressora listada: ', imp)

        print('\nConfigurações do Windows')
        for imp in list_printer:
            if 'PDF' in imp[2]:
                print(f'{imp}\n', f'"{imp[2]}" Para salvar em PDF')
        print('impressora instalada:', list_printer[-1][2])
    except:
        print('Sistema operacional não Windows!\n Ou as bibliotecas não estão instaladas! ;) ;)')


def conversor(_num):
    """Recebe um valor, se for string retorna uma mensagem de erro, caso contrário,
     verifica se há vírgula e troca por ponto e transforma em float, caso contrário,
     transforma em inteiro.
    :param: valor a ser passado à função.
    :return: retorna o valor numérico"""
    numero = _num
    if numero.isalpha():
        return 'Valor inválido, digite novamente.'
    if ',' in numero:
        numero = numero.replace(',', '.')
        numero = float(numero)
    else:
        numero = float(numero)
    return numero


def autocomplete(titulo:str, escolhas:list):
    from CadProd import produto, lista_p
    # A lista de opções que serão pesquisadas
    choices = sorted([produto[cod].desc for cod in lista_p])
    #choises =  sorted(escolhas)

    input_width = 30
    num_items_to_show = 4

    layout = [
        [sg.Text('Entre com  o nome de um produto :')],
        [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-')],
        [sg.pin(sg.Col([[sg.Listbox(values=[], size=(input_width, num_items_to_show), enable_events=True, key='-BOX-',
                                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, no_scrollbar=True)]],
                       key='-BOX-CONTAINER-', pad=(0, 0), visible=False))]
    ]

    window = sg.Window('AutoComplete', layout, return_keyboard_events=True, finalize=True, font=('_', 16))

    list_element: sg.Listbox = window.Element(
        '-BOX-')  # armazenar o elemento listbox para facilitar o acesso e acessar docstrings
    prediction_list, input_text, sel_item = [], "", 0

    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event == sg.WINDOW_CLOSED:
            break
        # pressionar a seta para baixo acionará o evento -IN- e depois o evento Down:40
        elif event.startswith('Escape'):
            window['-IN-'].update('')
            window['-BOX-CONTAINER-'].update(visible=False)
        elif event.startswith('Down') and len(prediction_list):
            sel_item = (sel_item + 1) % len(prediction_list)
            list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
        elif event.startswith('Up') and len(prediction_list):
            sel_item = (sel_item + (len(prediction_list) - 1)) % len(prediction_list)
            list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
        elif event == '\r':
            if len(values['-BOX-']) > 0:
                window['-IN-'].update(value=values['-BOX-'])
                window['-BOX-CONTAINER-'].update(visible=False)
                print(values['-IN-'])
        elif event == '-IN-':
            text = values['-IN-'].title()
            if text == input_text:
                continue
            else:
                input_text = text
            prediction_list = [item for item in choices if item.startswith(text)]
            if text:
                prediction_list = [item for item in choices if item.startswith(text)]
            list_element.update(values=prediction_list)
            sel_item = 0
            list_element.update(set_to_index=sel_item)

            if len(prediction_list) > 0:
                window['-BOX-CONTAINER-'].update(visible=True)
            else:
                window['-BOX-CONTAINER-'].update(visible=False)
        elif event == '-BOX-':
            window['-IN-'].update(value=values['-BOX-'])
            window['-BOX-CONTAINER-'].update(visible=False)

    window.close()


def login():
    """— > Função para liberar o sistema, pede Login e a senha para compara com o arquivo de cadastro,
    caso seja cadastrado libera osistema."""

    def busca_usuario(lgn: str, snh: str):
        """— > Função recebe o Login e a senha digitados e compara com o arquivo de cadastro.
        :param lgn: login digitado
        :param snh: senha digitada"""
        usuarios = []
        try:
            with open('Arquivos/users.log', 'r+', encoding='Utf-8', newline='') as rqv_usr:
                for linha in rqv_usr:
                    linha = linha.strip(',')
                    usuarios.append(linha.split())
                    print(linha)

                for usuario in usuarios:
                    nome = usuario[0]
                    password = usuario[1]
                    if lgn == nome and snh == password:
                        return True
        except FileNotFoundError:
            return False

    lay_log = [
        [sg.Frame('', [[sg.Text('Usuário:', size=7), sg.Input(key='user', size=25)],
                       [sg.Text('Senha:', size=7), sg.Input(size=10, key='pass', password_char='*'),
                        sg.Checkbox('Salvar login?', key='cadUsr')]])],
        [sg.Button('Entrar', bind_return_key=True), sg.Exit('Sair')]]
    wndLgn = sg.Window('Login', layout=lay_log, font=ftPd, finalize=True)  # , no_titlebar=True)

    while True:
        event, values = wndLgn.read()
        if event in ('Sair', sg.WIN_CLOSED):
            break
        if event in 'Entrar':
            # Usuário ou senha em branco
            if not values['user'] or not values['pass']:
                sg.PopupQuickMessage('Usuário ou senha não podem estar em branco!')
                continue

            # Cadastro
            if values['cadUsr']:
                usuario = busca_usuario(values['user'], values['pass'])
                if usuario:
                    sg.PopupQuickMessage('Usuário já cadastrado!\nDesmarque a opção de salvar.')
                    continue
                elif not usuario:  # Cadastra usuario
                    with open('users.log', 'a+', encoding='Utf-8', newline='') as arquivo:
                        arquivo.writelines(f"{values['user']} {values['pass']}\n")
                        sg.PopupQuickMessage('Cadastro Efetuado com sucesso!')

            usuario = busca_usuario(values['user'], values['pass'])
            if not usuario:
                sg.PopupQuickMessage('Usuário ou senha incorretos ', background_color='red')
                continue
            else:
                sg.PopupQuickMessage('  Bem vindo  ', font=('', 18), auto_close=True)
                break
    wndLgn.close()


if __name__ == '__main__':
    # login()
    # print(f'{dt.now():%d/%m/%Y}')
    # impressora_teste()
    autocomplete()

    pass
