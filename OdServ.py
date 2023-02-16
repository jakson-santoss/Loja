from Funcoes import *
from Dbase import *
from CadCar import Car

list_car = [(i[0], i[2]) for i in CarrosBD().read_task()]
forma_pagto = ['Dinheiro', 'Pix', 'Cartão', 'Cheque']
garantia = [15, 30, 60, 90]
aqvProd = list_prod()


def OrdServ():
    """Abre a janela para edição de Ordem de Seviço."""
    global edit
    _QT, _DESC, _PC, _VT = [], [], [],[]
    _CORPO = [[_QT, _DESC, _PC, _VT] for _ in range(15)]

    def search_car():
        plc = PopupDropDown('Busca de Veículos', 'Escolha ou digite a placa', list_car)
        if not plc:
            return
        if len(plc) > 2:
            placa = plc.upper()
            if placa not in (x[0]for x in list_car):
                sg.PopupOK('Veículo não existe\nRedirecionando para cadastro!')
                placa = Car()
        else:
            placa =plc[0]

        carro[placa] = CarrosBD()                              # Transforma a placa em identificador de objeto
        carro[placa].select_car(placa)                        # Lê as informações do objeto
        clt = carro[placa].cliente                                 # Transforma o cliente do carro em identificador de objeto
        cliente[clt] = ClientesBD()                               # LTransforma o doc em objeto
        cliente[clt].select_cli(clt)                                 # Lê as informações do objeto
        __atu(cliente[clt], carro[placa])                       # Passa os objetos ao atualizador do formulário
        window.find_element('GRT').set_focus()        # Passa o foco ao elemento garantia.
        return carro[placa], cliente[clt]

    def __atu(dono=None,veiculo=None):
        if dono and veiculo:
            window['NUM_ODR'].update(list_ordServ()[-1][0] + 1 if len(list_ordServ()) !=0 else 1)
            window['NOME'].update(dono.nome, background_color=sg.theme_background_color())
            window['DOC'].update(dono.doc, background_color=sg.theme_background_color())
            window['ENDER'].update(dono.endereco, background_color=sg.theme_background_color())
            window['FONE'].update(dono.fone, background_color=sg.theme_background_color())
            window['EMAIL'].update(dono.email, background_color=sg.theme_background_color())
            window['CARRO'].update(veiculo.completo)#[veiculo.marca, veiculo.modelo, veiculo.placa, veiculo.cor, veiculo.ano])
                #f'{veiculo.marca}, {veiculo.modelo} - placa: {veiculo.placa}\tcor: {veiculo.cor} - ano: {veiculo.ano}')
        else:
            for x in ('NUM_ODR', 'NOME', 'DOC', 'ENDER', 'FONE', 'EMAIL', 'CARRO', 'GRT', 'F_PAGTO', 'OBS', 'CORPO',  'VALOR', 'DEDUCAO', 'TOTAL'):
                window.find_element(x).update('')
        # corpo
        # rodapé 'SALDO', 'DEDUCAO', 'TOTAL'
        pass

    def edit_cell(window, chave, row, col, justify='left'):
        global textvariable, edit
        def callback(event, row, col, text, chave):
            global edit
            widget = event.widget
            if chave == 'Return':
                text = widget.get()
                print(text)
            widget.destroy()
            widget.master.destroy()
            values = list(table.item(row, 'values'))
            values[col] = text
            table.item(row, values=values)
            edit = False

        if edit or row <= 0:
            return

        edit = True
        root = window.TKroot
        table = window[chave].Widget

        text = table.item(row, "values")[col]
        x, y, width, height = table.bbox(row, col)

        frame = sg.tk.Frame(root)
        frame.place(x=x+4, y=y+253, anchor="nw", width=width, height=height)
        textvariable = sg.tk.StringVar()
        textvariable.set(text)
        entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
        entry.pack()
        entry.select_range(0, sg.tk.END)
        entry.icursor(sg.tk.END)
        entry.focus_force()
        entry.bind("<Return>", lambda e, r=row, c=col, t=text, k='Return':callback(e, r, c, t, k))
        entry.bind("<Escape>", lambda e, r=row, c=col, t=text, k='Escape':callback(e, r, c, t, k))

    edit = False
    window = sg.Window('', [
        [sg.T(' LOJA ', justification='c', text_color='lime', expand_x=True, font=ftTt, relief='raised'), 
         btn_menu(['&Novo::', '...::'])], 
        [sg.I(f'{hoje}', k='DATA', font=ftPd, text_color='white', s=18,
        background_color=sg.theme_background_color() , border_width=0),
        sg.P(), sg.T(' ORDEM DE SERVIÇO Nº ', font=ftBd),
         sg.In(k='NUM_ODR', font=ftBd, s=8)],
        [sg.Frame('', [
            [sg.I('CLIENTE', k='NOME',expand_x = True, border_width=0),
            sg.T('Doc: ', font=ftBt), 
            sg.I('DOCUMENTO', k='DOC', s=12, border_width=0)],
            [sg.I('ENDEREÇO', k='ENDER', expand_x=True, border_width=0)],
            [sg.T('Fone: ', font=ftBt), 
            sg.I('TELEFONE', k='FONE', s=15, border_width=0), 
            sg.P(), sg.T('Email: ', font=ftBt), 
            sg.I('E-MAIL', k='EMAIL', border_width=0)],
            [sg.I('Veículo', text_color='black', k='CARRO', font=ftBt, border_width=0, expand_x=True)]], 
            expand_x=True, font=ftPd)],
            # Corpo
        [sg.Button(button_text='Cancelar', k='BTN', border_width=0), 
         sg.T('Garantia'), sg.Combo(garantia, default_value=garantia[0], k='GRT'),
         sg.P(), sg.T('F. Pagamento'),
         sg.Combo(forma_pagto, default_value='Cartão', k='F_PAGTO')],
        [sg.T('Obs'), sg.I(key='OBS', expand_x=True)],
        [sg.Table(_CORPO, [' QT ', ' DESCRIÇÃO ', ' V.UNITÁRIO ', ' V. TOTAL '],  k= 'CORPO',
        col_widths=[4, 40,10,10], auto_size_columns=False, enable_click_events=True)],
       
       # Rodapé
        [sg.Col([[sg.B('...', disabled=True)],
                 [sg.B('...', disabled=True)],
                 [sg.B('IMPRIMIR')]]), sg.P(),
         sg.Col([[sg.T('VALOR', font=ftBt, text_color='red')],
                 [sg.T('DEDUÇÃO', font=ftBt, text_color='red')],
                 [sg.T('TOTAL', font=ftBt, text_color='red')]]),
         sg.Col([[sg.I(k='VALOR', font=ftBd,  pad=(0,0), background_color=sg.theme_background_color())],
                       [sg.I(k='DEDUCAO', font=ftBd, pad=(0,0), background_color=sg.theme_background_color())],
                       [sg.I(k='TOTAL', font=ftBd, pad=(0,0), background_color=sg.theme_background_color())]], 
                       s=(100, 90))],
        [sg.StatusBar('', k='-CLICKED-'), sg.Sizegrip()]], 
             keep_on_top=True, finalize=True)
    search_car()

    while True:
        events, values = window.read()
        if events == None or events == 'MENU::' and values['MENU::'] == 'Sair::':
            break
        elif events == 'MENU::' and values['MENU::'] == 'Novo::':
            __atu()
            search_car()
            values['MENU::'] = None
        elif isinstance(events, tuple):
            cell = row, col = events[2]
            window['-CLICKED-'].update(cell)
            edit_cell(window, 'CORPO', row+1, col, justify='left')

        elif events == 'BTN':
            pass
            odSv[values['NUM_ODR']] = OdServ(values['NUM_ODR'], values['DATA'],values['DOC'], values['CARRO'][0], 
            values['OBS'], values['CORPO'], values['TOTAL'])
        else:
            print(values['NUM_ODR'], values['DATA'],values['DOC'], values['CARRO'][0], 
            values['OBS'], '\n',  values['CORPO'], values['TOTAL'])
    window.close()


if __name__ == '__main__':
    #print ('está' if 'AAA1234' in (x[0] for x in aqvCar) else 'não está')
    OrdServ()

    pass

