import sqlite3
import csv


def list_prod():
    aqvProdutos = []
    with open("Arquivos/produtos.csv", "r", encoding='utf-8') as ref:
        aqv = csv.reader(ref, delimiter=',')
        for a in aqv:
            aqvProdutos.append(a)
    return aqvProdutos


def list_ordServ():
    aqvOdServ = []
    with open("Arquivos/od_serv.csv", "r", encoding='utf-8') as ref:
        aqv = csv.reader(ref, delimiter=',')
        for x in aqv:
            aqvOdServ.append(x)
    return aqvOdServ


class Banco:
    """Abre e faz a conexão com o banco de dados para a criação ddas tabelas."""
    def __init__(self, tabe):
        self.conexao = sqlite3.connect('Arquivos/carros&clientes.db')
        if tabe == 'Cliente':
            self.tab_cli()
        elif tabe == 'Car':
            self.tab_car()

    def tab_cli(self):
        """Cria a tabela Clientes para inserção de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(
                                 DOC TEXT PRIMARY KEY NOT NULL,
                                 NOME TEXT NOT NULL,
                                 ENDERECO TEXT NOT NULL,
                                 FONE TEXT NOT NULL,
                                 EMAIL TEXT NOT NULL)''')

        self.conexao.commit()
        cursor.close()

    def tab_car(self):
        """Cria a tabela Carros para inserção de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS carros(
                                     PLACA TEXT PRIMARY KEY NOT NULL,
                                     MARCA TEXT NOT NULL,
                                     MODELO TEXT NOT NULL,
                                     COR TEXT NOT NULL,
                                     ANO TEXT NOT NULL,
                                     CLIENTE TEXT NOT NULL)''')
        self.conexao.commit()
        cursor.close()


class CarrosBD(object):
    """Classe responsável pela manipulação dos dados dos veículos no banco de dados"""

    def __int__(self, placa, marca, modelo, cor, ano, cliente):
        """:param placa Identificador do veículo.
        :param marca Marca do veículo.
        :param modelo Modelo do veículo.
        :param cor Cor do veículo.
        :param ano A do veículo.
        :param cliente Proprietário do veículo, vinculado à tabela cliente."""
        self.placa, self.marca, self.modelo = placa, marca, modelo
        self.cor, self.ano, self.cliente = cor, ano, cliente

    @property
    def completo(self):
        return[self.placa, self.marca, self.modelo, self.cor, self.ano, self.cliente]
    def write_car(self):
        """Função de inserção de veículo na base de dados."""
        banco = Banco('Car')
        try:
            c = banco.conexao.cursor()
            c.execute('''INSERT INTO carros(PLACA, MARCA, MODELO, COR, ANO, CLIENTE) VALUES(?, ?, ?, ?, ?, ?)''',
                      (self.placa, self.marca, self.modelo, self.cor, self.ano, self.cliente))

            banco.conexao.commit()
            c.close()
            return "Usuário cadastrado com sucesso!"
        except:
            return "Ocorreu um erro na inserção do cliente"

    def updt_car(self):
        """Função de atualização de veículo na base de dados."""
        banco = Banco('Car')
        try:
            c = banco.conexao.cursor()
            c.execute(
                "UPDATE carros SET MARCA = '" + self.marca + "', MODELO = '" + self.modelo +
                "', COR = '" + self.cor + "', ANO = '" + self.ano + "', CLIENTE = '" + self.cliente +
                "' where PLACA = '" + self.placa + "'")

            banco.conexao.commit()
            c.close()
            return "Veíclo atualizado com sucesso!"
        except:
            return "Ocorreu um erro na alteração do veículo"

    def select_car(self, placa):
        """Função de seleção de veículo na base de dados."""
        banco = Banco('Car')
        try:

            c = banco.conexao.cursor()

            c.execute("SELECT * FROM carros WHERE PLACA = '" + placa + "'")

            for linha in c:
                self.placa = linha[0]
                self.marca = linha[1]
                self.modelo = linha[2]
                self.cor = linha[3]
                self.ano = linha[4]
                self.cliente = linha[5]

            c.close()

            return "Busca feita com sucesso!"
        except:
            return "Ocorreu um erro na busca do veiculo"

    def read_task(self):
        """Função que faz uma busca na base de dados e  retorna todos os registros encontrados."""
        banco = Banco('Car')
        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT * FROM carros''')
            data = c.fetchall()
            banco.conexao.commit()
            c.close()
            return data
        except:
            return None

    @staticmethod
    def delete_car(placa):
        """Função de exclusão de veículos na base de dados."""
        banco = Banco('Car')
        try:
            c = banco.conexao.cursor()
            c.execute("DELETE FROM carros WHERE PLACA = " + placa + " ")
            banco.conexao.commit()
            c.close()
            return "Veículo excluído com sucesso!"
        except:
            return "Ocorreu um erro na exclusão do veículo"


class ClientesBD(object):
    """Classe responsável pela manipulação dos dados dos clientes no banco de dados"""

    def __int__(self, doc, nome, endereco, fone, email):
        self.doc = doc
        self.nome = nome
        self.endereco = endereco
        self.fone = fone
        self.email = email

    @property
    def completo(self):
        return [self.doc, self.nome, self.endereco, self.fone, self.email]

    def write_cli(self):
        """Inclui clientes no banco de dados"""
        banco = Banco('Cliente')
        try:
            c = banco.conexao.cursor()
            c.execute('''INSERT into clientes(DOC, NOME, ENDERECO, FONE, EMAIL) 
            VALUES(?, ?, ?, ?, ?)''', (self.doc, self.nome, self.endereco, self.fone, self.email))
            banco.conexao.commit()
            c.close()
            return f"{self.nome}\nfoi cadastrado com sucesso!"
        except:
            return "Ocorreu um erro na inserção do usuário"

    def updt_cli(self):
        """Atualiza clientes no banco de dados"""
        print(self.completo)
        banco = Banco('Cliente')
        try:
            c = banco.conexao.cursor()
            c.execute("UPDATE clientes SET NOME = '" + self.nome + "', ENDERECO = '"
                      + self.endereco + "', FONE = '" + self.fone + "', EMAIL = '" + self.email + 
                      "' WHERE DOC = '" + self.doc + "'")
            banco.conexao.commit()
            c.close()

            return "Cliente atualizado com sucesso!"
        except:
            return "Ocorreu um erro na alteração do cliente"

    @staticmethod
    def delete_cli(documento):
        """Exclui clientes no banco de dados"""
        banco = Banco('Cliente')
        try:
            c = banco.conexao.cursor()
            c.execute("DELETE FROM clientes WHERE DOC = " + documento + " ")
            banco.conexao.commit()
            c.close()
            return "Cliente excluído com sucesso!"
        except:
            return "Ocorreu um erro na exclusão do cliente"

    def select_cli(self, doc):
        """Seleciona um cliente no banco de dados"""
        banco = Banco('Cliente')
        try:
            c = banco.conexao.cursor()
            c.execute("SELECT * FROM clientes WHERE DOC= '" + doc + "'")

            for linha in c:
                self.doc = linha[0]
                self.nome = linha[1]
                self.endereco = linha[2]
                self.fone = linha[3]
                self.email = linha[4]

            c.close()
            return "Busca feita com sucesso!"
        except:
            return "Ocorreu um erro na busca do cliente"

    def read_task(self):
        banco = Banco('Cliente')
        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT * FROM clientes''')
            data = c.fetchall()
            banco.conexao.commit()
            c.close()
            return data
        except:
            return None


class ProdAqv(object):
    """Classe responsável pela manipulação dos dados dos produtos na planilha produtos.csv,
    ultilizando a biblioteca csv"""
    aqvProdutos = list_prod()

    def __int__(self, cod, desc, preco: float):
        self.cod = cod
        self.desc = desc
        self.preco = preco

    @property
    def completo(self):
        return [self.cod, self.desc, self.preco]

    def grava(self):
        """Inclui ou atualiza produtos na planilha."""
        if self.cod in [self.aqvProdutos[x][0] for x in range(len(self.aqvProdutos))]:      # Atualiza
            with open("Arquivos/produtos.csv", "w", encoding='utf-8') as arquivo:
                for prod in self.aqvProdutos:
                    if prod[0] == self.cod:
                        prod[0], prod[1], prod[2] = self.cod, self.desc, self.preco
                    arquivo.write(f'{prod[0]},{prod[1]},{prod[2]}\n')
        else:
            with open("Arquivos/produtos.csv", "a+", encoding='utf-8') as arquivo:          # inclui
                arquivo.write(f'{self.cod},{self.desc},{self.preco}\n')

    def exclui(self):
        """Exclui clientes da planilha."""
        with open("Arquivos/produtos.csv", "w", encoding='utf-8') as arquivo:
            for prod in self.aqvProdutos:
                if prod[0] != self.cod:
                    arquivo.write(f'{prod[0]},{prod[1]},{prod[2]}\n')


class OdServ(object):
    """Classe responsável pela manipulação dos dados dos produtos na planilha od_serv.csv,
    ultilizando a biblioteca csv"""
    aqvOdServ = list_ordServ()

    def __init__(self, num_ord, data, doc, placa, garantia, obs, produtos, total):
        self.num_ord = num_ord      # self.aqvOdServ[-1][0] + 1
        self.data = data
        self.doc = doc
        self.placa = placa
        self.garantia = garantia
        self.obs = obs if obs else ''
        self.produtos = produtos
        self.total = total

    '''    @property
    def completo(self):
        return[self.placa, self.marca, self.modelo, self.cor, self.ano, self.cliente]
    '''
    def grava_ord(self):
        """Inclui ou atualiza produtos na planilha."""
        with open("Arquivos/od_serv.csv", "a+", encoding='utf-8') as arquivo:  # Inclui
            arquivo.write(
                f'{self.num_ord},{self.data},{self.doc},{self.placa},{self.garantia},{self.obs},{self.produtos},{self.total}\n')

    def select_ods(self, n_seq):
        if self.num_ord in [self.aqvOdServ[x][0] for x in range(len(self.aqvOdServ))]:  # Atualiza
            for ods in self.aqvOdServ:
                if ods[0] == n_seq:
                    n_seq = OdServ()
                    n_seq.num_ord = ods[0]
                    n_seq.data = ods[1]
                    n_seq.cliente = ods[2]
                    n_seq.carro = ods[3]
                    n_seq.garantia = ods[4]
                    n_seq.obs = ods[5]
                    n_seq.produtos = ods[6]
                    n_seq.total = ods[7]
            return n_seq
        else:
            return


if __name__ == '__main__':
    # CarrosBD()
    # ClientesBD()
    # ProdAqv()
    # OdServ()

    pass
