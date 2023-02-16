from Funcoes import *
from Dbase import list_prod, ProdAqv
from random import randint

lista_p = []
for pd in list_prod():
    produto[pd[0]] = ProdAqv()
    produto[pd[0]].cod = pd[0]
    produto[pd[0]].desc = pd[1]
    produto[pd[0]].preco = float(pd[2])
    lista_p.append(pd[0])

def Produtos():
    kbc = [' CÓDIGO ', '              DESCRIÇÃO             ', '   PREÇO   ']

    def atu(cdg=None):
        if cdg:
            window[0].update(produto[cdg].cod)
            window[1].update(produto[cdg].desc)
            window[2].update(produto[cdg].preco)
        else:
            for a in range(len(kbc)): window[a].update(randint(99, 999) if a == 0 else '')
            window['_Box'].update([produto[pd].cod, produto[pd].desc,
                                    f'R$ {produto[pd].preco:3.2f}'] for pd in lista_p)
            window['-TOTAL-'].update(f'{len(lista_p)} Produtos')
            window[1].set_focus()

    layout = [[sg.Frame('Cadastro Geral de Produtos', [
        [sg.T('Código', size=10, font=ftBt), sg.T('Descrição',  font=ftBt), sg.P(), sg.T('Preço', size=5, font=ftBt), btn_menu(['Limpar::', 'Salvar::', 'Excluir::', '...'])],
        [sg.I(size=10, disabled=True), sg.I(expand_x=True), sg.I(size=12)]],
                        title_color='yellow', font=ftBt, expand_x=True)],
              [sg.Table([], kbc,
                        key='_Box', font=['_', 12], num_rows=8,
                        justification='l',
                        enable_events=True)],
              [sg.OK('Salvar'), sg.B('Excluir'), sg.StatusBar('                    ',key='-TOTAL-', justification='c'), sg.B('Sair')]]
    window = sg.Window('Cadastro de Produtos', layout, font=ftPd, finalize=True)
    atu()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Sair') or event == 'MENU::' and values['MENU::'] == 'Sair::':
            break
        elif event == '_Box' and values['_Box']:
            atu(lista_p[values['_Box'][0]])

        elif event == 'Salvar' and values[1]:
            cod = values[0]
            produto[cod] = ProdAqv()
            produto[cod].cod = values[0]
            produto[cod].desc = values[1].strip().title()
            produto[cod].preco = conversor(values[2])
            produto[cod].grava()
            lista_p.append(cod)
            atu()

        elif event == 'Excluir' and values['_Box']:
            if sg.popup_yes_no('Deseja realmente excluir este produto?') == 'Yes':
                produto[values[0]].exclui()
                lista_p.remove(values[0])
                atu()
            continue
    window.close()


if __name__ == '__main__':
    
    Produtos()

    pass
