from Funcoes import sg, ftTt, ftPd, ftBt, ftBd, btn_menu
from CadCar import Car
from OdServ import OrdServ
from CadCliente import Cliente
from CadProd import Produtos
import Reports as rpt


def main_window():
    sg.theme('Default')

    menu_f = ['&Od. Serviço::', '&Veículos::', '&Clientes::', '&Produtos::','Re&latórios::', 'O&utros::', ['...', '&Temas'] ]
    layout = [
        [sg.Frame('',[[sg.T('Título', justification='c', text_color='lime', font=ftTt, expand_x=True),
        btn_menu(menu_f)]], expand_x=True)],
        [[sg.Col([
        [sg.Button('Od. Serviço', font=ftBt, border_width=0, s= 12)],
        [sg.Button('Veículos', font=ftBt, border_width=0, s= 12)],
        [sg.Button('Clientes', font=ftBt, border_width=0, s= 12)],
        [sg.Button('Outros', font=ftBt, border_width=0, s= 12)],
        [sg.VPush()],
        [sg.Button('Sair', font=ftBt,border_width=0, s= 12)]],expand_y=True),
         sg.Col([[sg.Image('Logo.png')]])], ],
        [sg.StatusBar(''), sg.Sizegrip()]
        ]
    return sg.Window('CADASTROS', layout=layout, font=ftPd, finalize=True)    #, button_color=sg.theme_background_color()


def rpt_window():
    layout = [[sg.StatusBar(' RELATÓRIOS GERAIS ', justification='c', text_color='lime', font=ftTt)],
              [sg.Button('Clientes', key='rpt_dri'), sg.P(), 
               sg.Button('Carros', key='rpt_car'), sg.P(), 
               sg.Button('Outros', key='rpt_otr'), sg.P(), sg.Exit()]]
    return sg.Window(' ', layout=layout, font=ftPd, element_justification='c',
                     #button_color=sg.theme_background_color(),
                     finalize=True)


def Inicio():
    janela1, janela2 = main_window(), None
    while True:
        window, events, values = sg.read_all_windows()
        print(events, values)
        if window == janela1:  # Janela Principal
            if events == None:
                break
            elif events == 'Sair' or events == 'MENU::' and values['MENU::'] == 'Sair::':
                values = exit()
            elif events == 'Od. Serviço' or events == 'MENU::' and values['MENU::'] == 'Od. Serviço::':
                OrdServ()
                continue
            elif events == 'Clientes' or events == 'MENU::' and values['MENU::'] == 'Clientes::':  # Botão Cadastros
                janela2 = Cliente()
            elif events == 'Veículos' or events == 'MENU::' and values['MENU::'] == 'Veículos::':  # Botão Cadastros
                janela2 = Car()
            elif events == 'MENU::' and values['MENU::'] == 'Produtos::':
                janela2 = Produtos()
            elif events == 'MENU::' and values['MENU::'] == 'Relatórios::':  # Botão Relatórios
                janela2 = rpt_window()
                continue
            elif events == 'Outros' or events == 'MENU::' and values['MENU::'] == 'Outros::':  # Botão Outos
                continue
                janela2 = ''
                janela1.hide()
        if window == janela2:
            if events in (None, 'Exit','Sair'):
                # Quando queremos voltar para janela interior
                janela2.hide()
                janela1.un_hide()
            # Tela Relatórios \ Botão Carros
            elif events == 'rpt_car':
                rpt.relatorio('carro')  # Lista, retorna escolha
                rpt.Reports('carro')  # Tabela, não há retorno
                continue
            # Tela Relatórios \ Botão Clientes
            elif events == 'rpt_dri':
                rpt.relatorio('cliente')
                rpt.Reports('cliente')
                continue
            # Tela Relatórios \ Botão Outros
            elif events == 'rpt_otr':
                rpt.relatorio('produto')
                rpt.Reports('produto')
                continue


# Pressione o botão verde na sarjeta para executar o script.
if __name__ == '__main__':
    # Criar as janelas iniciais
    # Funcoes.login()
    Inicio()
    print('Encerrando programa!')
    # print(*forma_pagto, sep='\n')   # Desempacota a lista
