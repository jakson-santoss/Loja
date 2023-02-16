from Funcoes import *
from CadCliente import Cliente
from Dbase import ClientesBD, CarrosBD

list_clt = [(i[0], i[1]) for i in ClientesBD().read_task()]

aqvCar = sorted(CarrosBD().read_task())

with open('Arquivos/marcas.txt', 'r', encoding='utf-8') as f:
    marcas = [_.rstrip('\n') for _ in f]

for cr in CarrosBD().read_task():
    carro[cr[0]] = CarrosBD()
    carro[cr[0]].placa = cr[0]
    carro[cr[0]].marca = cr[1]
    carro[cr[0]].modelo = cr[2]
    carro[cr[0]].cor = cr[3]
    carro[cr[0]].ano = cr[4]
    carro[cr[0]].cliente = cr[5]

def list_car():
    return [(i[0], i[2]) for i in CarrosBD().read_task()]

def Car():
    def atu_c(plc=None):
        if plc:
            for i, k in enumerate(carro[plc].completo): window[i].update(k)
        else:
            for a in range(len(kbc)): window[a].update('')
            window['_Box'].update([carro[cr[0]].completo for cr in list_car()])

    def encontra_cli(_clt):
        print(_clt, '\n', list_clt)
        if not _clt or _clt not in [list_clt[x][0] for x in (range(len(list_clt)))]:
            confirm = sg.PopupYesNo('Cliente não cadastrado!\nDeseja cadastra-lo agora?')
            if confirm == 'Yes':
                _clt = Cliente()
            else:
                _clt = 'PADRÃO'
        else:
            pass  # sg.PopupOK(aqvCliente()[_clt])
        return _clt

    kbc = ['PLACA', 'MARCA', 'MODELO', 'COR', 'ANO', 'CLIENTE']
    layout = [[sg.Frame('', [
        [sg.T('Placa', size=10), sg.T('Marca', size=10), sg.T('Modelo', size=9),
         sg.T('Cor', size=9), sg.T('Ano', size=7), sg.T('Cliente', size=11), btn_menu(['Limpar::', 'Salvar::', 'Excluir::', '...'])],
        [sg.I(size=10), sg.Combo(sorted(marcas), size=10, default_value=marcas[0]), sg.I(size=10),
         sg.I(size=10), sg.I(size=8), sg.InputCombo(list_clt, size=15)]])],
              [sg.Table([], kbc, key='_Box', font=['_', 12],
                        justification='l', expand_x=True, enable_events=True)],
              [sg.B('Salvar'), sg.P(), sg.Ok()]]
    window = sg.Window('Cadastro de Veículos', layout, font=ftBt, finalize=True)
    atu_c()
    while True:
        event, values = window.read()
        print(event,values)
        if event == sg.WIN_CLOSED or event == 'MENU::' and values['MENU::'] =='Sair::':
            break
        elif event == '_Box' and values['_Box']:
            atu_c(list_car()[values['_Box'][0]][0])
        elif event == 'Ok':
            if not values['_Box']:
                sg.PopupOK('Você precisa escolher um veículo na lista')
            else:
                window.close()
                return carro[values[0]].placa
        elif event == 'MENU::' and 'Limpar::':
            atu_c()
            continue
        elif event == 'MENU::' and 'Excluir::' and values['_Box']:
            confirma = sg.PopupOKCancel('Deseja realmente excluir este veículo?')
            if confirma == 'OK':
                CarrosBD().delete_car(values[0])
                atu_c()
                sg.PopupQuickMessage('Veículo excluido com sucesso!', no_titlebar=False, font=ftBt)
            else:
                continue

        elif event in 'Salvar':
            v_placa = values[0].upper()
            v_cliente = values[5][0] if len(values[5]) > 1 else values[5]
            v_cliente = encontra_cli(v_cliente)

            carro[v_placa] = CarrosBD()
            carro[v_placa].placa = v_placa
            carro[v_placa].marca = values[1].title()
            carro[v_placa].modelo = values[2].title()
            carro[v_placa].cor = values[3].title()
            carro[v_placa].ano = values[4]
            carro[v_placa].cliente = v_cliente

            carro[v_placa].write_car()

            if values['_Box']:
                sg.popup(carro[v_placa].updt_car())
            else:
                sg.popup(carro[v_placa].write_car())
            atu_c()
            window[0].set_focus()
    window.close()


if __name__ == '__main__':
    Car()
