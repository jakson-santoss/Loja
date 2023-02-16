import requests
from Funcoes import *
from Dbase import ClientesBD

list_clt = [(i[0], i[1]) for i in ClientesBD().read_task()]

def aqvCliente():
    return [ClientesBD().read_task()[x] for x in range(1, len(ClientesBD().read_task()))]


def Cliente():
    fone = None
    kbc = ['DOC', 'NOME', 'ENDEREÇO', 'TELEFONE', 'EMAIL']

    def BuscaEnder():
        """Função que abre uma tela simples para busca de endereço e CEP.
                :return retorna um dicionário com o endereço do cliente."""
        endereco = {}
        wndCep = sg.Window('Busca de Endereço', [
            [sg.T('CEP:', size=12), sg.Input(key='-CEP-', size=8),
             sg.T('Número:', text_color='red'), sg.I(key='-NMR-', size=8)],
            [sg.T('Logradouro', size=12), sg.Input(key='-PLACE-', size=40)],
            [sg.T('Cidade', size=12), sg.Input(key='-CITY-', size=20),
             sg.I('SP', key='-UF-', size=4)],
            [sg.Button('OK', bind_return_key=True), sg.Button('Sair')]
        ], font=ftPd, finalize=True)

        while True:  # Event Loop
            event, values = wndCep.read()
            if event == sg.WIN_CLOSED or event in 'Sair':
                return
            elif event == 'OK':
                if not values['-NMR-']:
                    sg.PopupQuickMessage('Não se esqueça de fornecer o número!', text_color='red', font=(None, 16))
                    continue
                elif values['-CEP-']:
                    if len(values['-CEP-']) < 8 or len(values['-CEP-']) > 9 or values['-CEP-'].isalpha():
                        sg.PopupQuickMessage('CEP inválido, digite novamente.', no_titlebar=False, font=ftBt)
                        continue
                    elif '-' in values['-CEP-']:
                        values['-CEP-'] = values['-CEP-'].replace('-', '')
                    link = f"https://viacep.com.br/ws/{values['-CEP-']}/json/"
                    pedido = requests.get(link)  # Recebe o pedido do link
                    dic_pedido = pedido.json()  # Transforma o conteúdo recebido em um dicionário
                    endereco = dic_pedido
                elif not values['-CEP-'] and values['-PLACE-'] and values['-CITY-']:
                    place = values['-PLACE-'].title()
                    city = values['-CITY-'].title()
                    uf = values['-UF-'].upper()
                    link = f'https://viacep.com.br/ws/{uf}/{city}/{place}/json/'
                    pedido = requests.get(link)  # Recebe o pedido do link
                    dic_pedido = pedido.json()  # Transforma o conteúdo recebido em um dicionário
                    endereco = dic_pedido[0]
                    if len(dic_pedido) > 1:
                        sg.PopupQuickMessage(f'Atenção\nExistem {len(dic_pedido)} logradouros com {place}.'
                                             f'\nBusque pelo nome completo ou pelo CEP.'
                                             , no_titlebar=False, font=ftBt)
                        continue
                else:
                    busca = sg.PopupOKCancel('Preciso de um CEP ou "logradouro e cidade" para pesquisar.',
                                             title='Busca')
                    if busca == 'Cancel':
                        return
                    continue
                break
        endereco_cliente = f"{endereco.get('logradouro')}, {values['-NMR-']}\n" \
                           f"{endereco.get('bairro')} - {endereco.get('cep')}\n" \
                           f"{endereco.get('localidade')} - {endereco.get('uf')}"
        sg.PopupQuickMessage(endereco_cliente, no_titlebar=False, font=ftBt)
        endereco_cliente = endereco_cliente.replace('\n', ' - ')
        wndCep.close()
        wndCli[3].update(f'({endereco.get("ddd")})')
        wndCli[3].set_focus()
        return endereco_cliente

    def atu(info=None):
        if info:
            for i, k in enumerate(info): wndCli[i].update(k)
        else:
            for a in range(len(kbc)): wndCli[a].update('')
            wndCli['_Box'].update(aqvCliente())

    wndCli = sg.Window('Cadastro de Clientes', [
        [sg.Frame('', [
            [sg.T('Documento:', s=10, font=ftBt), sg.I(s=15, font=ftBt), sg.B('Buscar')],
            [sg.T('Nome:', s=12), sg.I(s=70)],
            [sg.B('Endereço', k='-B_adress-', bind_return_key=True), sg.P(), sg.I(s=70)],
            [sg.T('Telefone:', s=12), sg.I(size=15),  sg.P(), sg.T('Email:', s=6), sg.I(size=30)]]),
            sg.P(), sg.vtop( btn_menu(['Limpar::', 'Salvar::', 'Excluir::', '...']))],
        [sg.B('Salvar', bind_return_key=True), sg.P(), sg.B('Excluir'),],
        [sg.Table(aqvCliente(), kbc, key='_Box', font=['_', 12],
                  auto_size_columns=True, num_rows=10,
                  justification='l', enable_events=True)],

        [sg.P(), sg.B('Sair', bind_return_key=True)]], font=ftPd, finalize=True)

    while True:
        event, values = wndCli.read()
        if event in ('Sair', None) or event == 'MENU::' and values['MENU::'] == 'Sair::' :
            break
        elif event == 'MENU::' and values['MENU::'] == 'Limpar::' :
            pass
        elif event == 'Buscar':
            if values[0] == '0000':
                values[0] = 'PADRÃO'
            if values[0].upper() in [x[0] for x in ClientesBD().read_task()]:
                for x in ClientesBD().read_task():
                    if values[0] in x:
                        atu(x)
                pass

        elif event == '-B_adress-':
            if values[0]:
                wndCli[2].update(BuscaEnder())
            else:
                sg.PopupQuickMessage('Não há cliente válido,\n por favor insira um cliente!',
                                     title='ATENÇÃO', no_titlebar=False, font=ftBt)
        elif event == '_Box' and values['_Box']:
            atu(aqvCliente()[values['_Box'][0]])

        elif event == 'Excluir' and values['_Box'] or event == 'MENU::' and values['MENU::'] == 'Excluir::' and values['_Box']:
            confirma = sg.PopupOKCancel(f'Deseja realmente excluir {values[1]}?')
            if confirma == 'OK':
                ClientesBD().delete_cli(values[0])
                atu()
                sg.PopupQuickMessage('Cliente excluido com sucesso!', no_titlebar=False, font=ftBt)
            else:
                continue

        elif event == 'Salvar' or event == 'MENU::' and values['MENU::'] == 'Salvar::' :
            if not values[0]:
                sg.PopupOk('Não há documento válido',  font=ftBt)
            docV = values[0].upper()
            if len(values[3]) > 8 and '-' not in values[3]:  # Trata o número de telefone
                fone = values[3].replace(' ', '')
                fone = fone[:-4] + '-' + fone[-4:]
            elif len(values[3]) == 14 and '-' in values[3]:
                fone = values[3]

            cliente[docV] = ClientesBD()
            cliente[docV].doc = docV
            cliente[docV].nome = values[1].title()
            cliente[docV].endereco = values[2]
            cliente[docV].fone = fone
            cliente[docV].email = values[4].lower()
            list_clt.append((cliente[docV].doc, cliente[docV].nome))

            if docV in [x[0] for x in ClientesBD().read_task()]:
                sg.PopupQuickMessage(cliente[docV].updt_cli(), no_titlebar=False, font=ftBt)
            else:
                sg.PopupQuickMessage(cliente[docV].write_cli(), no_titlebar=False, font=ftBt)
            atu()
            wndCli[0].set_focus()
    wndCli.close()


if __name__ == '__main__':
    Cliente()
