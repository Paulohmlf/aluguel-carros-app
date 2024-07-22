import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageTk

class AluguelCarrosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Aluguel de Carros")
        self.root.geometry("1200x700")
        self.root.iconbitmap(r'C:\Users\paulo\OneDrive\Área de Trabalho\python\testee.ico')

        self.carros_disponiveis = ["Gol Branco", "Gol Vermelho", "Voyage", "Celta Bruno", "Celta", "Uno", "Agile", "Montana"]
        self.conectar_banco_de_dados()
        self.mostrar_login()

    def conectar_banco_de_dados(self):
        self.conn = sqlite3.connect('alugueis.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alugueis (
                cpf TEXT PRIMARY KEY,
                nome_pessoa TEXT UNIQUE,
                rg TEXT,
                rua TEXT,
                numero TEXT,
                bairro TEXT,
                cidade TEXT,
                data_aluguel DATE,
                carro_alugado TEXT
            )
        ''')
        self.conn.commit()

    def fechar_banco_de_dados(self):
        self.conn.close()

    def fechar_janelas_secundarias(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def fechar_janela(self):
        self.fechar_janelas_secundarias()
        self.root.quit()
        self.root.destroy()
        self.fechar_banco_de_dados()

    def abrir_nova_janela(self, opcao):
        self.fechar_janelas_secundarias()
        if opcao == "Pessoas Cadastradas":
            self.carregar_pessoas_cadastradas()
        elif opcao == "Verificar Locações Anteriores":
            self.abrir_verificar_locacoes()
        elif opcao == "Cadastrar Novo Aluguel":
            self.abrir_cadastrar_aluguel()
        elif opcao == "Alterar Dados":
            self.abrir_alterar_dados()
        elif opcao == "Deletar Dados":
            self.abrir_deletar_dados()
        elif opcao == "Pesquisar por CPF":
            self.abrir_pesquisar_por_cpf()
        elif opcao == "Gerar Termo de Responsabilidade":
            self.abrir_gerar_termo()

    def mostrar_login(self):
        self.fechar_janelas_secundarias()
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Usuário:").pack(pady=10)
        usuario_entry = tk.Entry(self.root)
        usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack(pady=10)
        senha_entry = tk.Entry(self.root, show="*")
        senha_entry.pack(pady=5)

        def tentar_login():
            usuario = usuario_entry.get()
            senha = senha_entry.get()
            if self.verificar_login(usuario, senha):
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")

        tk.Button(self.root, text="Login", command=tentar_login).pack(pady=20)
        self.root.bind('<Return>', lambda event: tentar_login())

        imagem = tk.PhotoImage(file=r'C:\Users\paulo\OneDrive\Imagens\foto.png')
        label_imagem = tk.Label(self.root, image=imagem)
        label_imagem.pack(pady=10)
        self.root.mainloop()

    def verificar_login(self, usuario, senha):
        return (usuario.lower() == "raniere") and (senha == "021209")

    def mostrar_menu_principal(self):
        self.fechar_janelas_secundarias()
        for widget in self.root.winfo_children():
            widget.destroy()

        def voltar_para_login():
            self.mostrar_login()

        imagem_original = Image.open(r'C:\Users\paulo\OneDrive\Imagens\cadeados.png')
        imagem_redimensionada = imagem_original.resize((30, 30), Image.LANCZOS)
        imagem_cadeado = ImageTk.PhotoImage(imagem_redimensionada)

        botao_cadeado = tk.Button(self.root, image=imagem_cadeado, command=voltar_para_login)
        botao_cadeado.place(x=10, y=10)

        rotulo = tk.Label(self.root, text="Selecione uma opção:")
        rotulo.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10)

        frame_opcoes = tk.Frame(self.root)
        frame_opcoes.pack(pady=10)

        opcoes_paginas = [
            ("Cadastrar Novo Aluguel", "Cadastrar Novo Aluguel"),
            ("Verificar Locações Anteriores", "Verificar Locações Anteriores"),
            ("Pessoas Cadastradas", "Pessoas Cadastradas"),
            ("Alterar Dados", "Alterar Dados"),
            ("Deletar Dados", "Deletar Dados"),
            ("Pesquisar por CPF", "Pesquisar por CPF"),
            ("Gerar Termo de Responsabilidade", "Gerar Termo de Responsabilidade")
        ]

        for texto, valor in opcoes_paginas:
            botao = ttk.Button(frame_opcoes, text=texto, command=lambda v=valor: self.abrir_nova_janela(v))
            botao.pack(pady=5, fill="x")

        botao_fechar = ttk.Button(self.root, text="Fechar", command=self.fechar_janela)
        botao_fechar.pack(pady=10)

        imagem = tk.PhotoImage(file=r'C:\Users\paulo\OneDrive\Imagens\foto.png')
        label_imagem = tk.Label(self.root, image=imagem)
        label_imagem.pack(pady=10)
        self.root.mainloop()

    def abrir_cadastrar_aluguel(self):
        janela_cadastrar = tk.Toplevel(self.root)
        janela_cadastrar.title("Cadastrar Novo Aluguel")
        janela_cadastrar.geometry("700x700")

        frame_cadastrar = tk.Frame(janela_cadastrar)
        frame_cadastrar.pack(pady=10)

        tk.Label(frame_cadastrar, text="Nome da Pessoa:").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = tk.Entry(frame_cadastrar)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="CPF:").grid(row=1, column=0, padx=5, pady=5)
        cpf_entry = tk.Entry(frame_cadastrar)
        cpf_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="RG:").grid(row=2, column=0, padx=5, pady=5)
        rg_entry = tk.Entry(frame_cadastrar)
        rg_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="Rua:").grid(row=3, column=0, padx=5, pady=5)
        rua_entry = tk.Entry(frame_cadastrar)
        rua_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="Número:").grid(row=4, column=0, padx=5, pady=5)
        numero_entry = tk.Entry(frame_cadastrar)
        numero_entry.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="Bairro:").grid(row=5, column=0, padx=5, pady=5)
        bairro_entry = tk.Entry(frame_cadastrar)
        bairro_entry.grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="Cidade:").grid(row=6, column=0, padx=5, pady=5)
        cidade_entry = tk.Entry(frame_cadastrar)
        cidade_entry.grid(row=6, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="Data de Aluguel (DD-MM-AAAA):").grid(row=7, column=0, padx=5, pady=5)
        data_entry = tk.Entry(frame_cadastrar)
        data_entry.grid(row=7, column=1, padx=5, pady=5)
        
        tk.Label(frame_cadastrar, text="Carro Alugado:").grid(row=8, column=0, padx=5, pady=5)
        carro_var = tk.StringVar(frame_cadastrar)
        carro_var.set(self.carros_disponiveis[0])

        menu_carros = tk.OptionMenu(frame_cadastrar, carro_var, *self.carros_disponiveis)
        menu_carros.grid(row=8, column=1, padx=5, pady=5)

        cadastrar_button = tk.Button(frame_cadastrar, text="Cadastrar", command=lambda: self.cadastrar_aluguel(nome_entry, cpf_entry, rg_entry, rua_entry, numero_entry, bairro_entry, cidade_entry, data_entry, carro_var.get()))
        cadastrar_button.grid(row=9, columnspan=2, pady=10)

        fechar_button = tk.Button(frame_cadastrar, text="Fechar", command=janela_cadastrar.destroy)
        fechar_button.grid(row=10, columnspan=2, pady=10)
        janela_cadastrar.bind('<Return>', lambda event: self.cadastrar_aluguel(nome_entry, cpf_entry, rg_entry, rua_entry, numero_entry, bairro_entry, cidade_entry, data_entry, carro_var.get()))

    def cadastrar_aluguel(self, nome_entry, cpf_entry, rg_entry, rua_entry, numero_entry, bairro_entry, cidade_entry, data_entry, carro_alugado):
        nome = nome_entry.get()
        cpf = cpf_entry.get()
        rg = rg_entry.get()
        rua = rua_entry.get()
        numero = numero_entry.get()
        bairro = bairro_entry.get()
        cidade = cidade_entry.get()
        data_aluguel = data_entry.get()
        
        if nome and cpf and rg and rua and numero and bairro and cidade and data_aluguel:
            if len(cpf) != 11:
                messagebox.showerror("Erro", "O CPF deve conter exatamente 11 dígitos.")
                return
            if len(rg) < 8 or len(rg) > 9:
                messagebox.showerror("Erro", "O RG deve conter entre 8 e 9 dígitos.")
                return
            
            try:
                datetime.strptime(data_aluguel, '%d-%m-%Y')
                self.cursor.execute('INSERT INTO alugueis (cpf, nome_pessoa, rg, rua, numero, bairro, cidade, data_aluguel, carro_alugado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (cpf, nome, rg, rua, numero, bairro, cidade, data_aluguel, carro_alugado))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Aluguel cadastrado com sucesso")
                nome_entry.delete(0, tk.END)
                cpf_entry.delete(0, tk.END)
                rg_entry.delete(0, tk.END)
                rua_entry.delete(0, tk.END)
                numero_entry.delete(0, tk.END)
                bairro_entry.delete(0, tk.END)
                cidade_entry.delete(0, tk.END)
                data_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "CPF já cadastrado. Insira um CPF diferente.")
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido. Use DD-MM-AAAA.")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def abrir_verificar_locacoes(self):
        janela_verificar = tk.Toplevel(self.root)
        janela_verificar.title("Verificar Locações Anteriores")
        janela_verificar.geometry("700x700")

        frame_locacoes = tk.Frame(janela_verificar)
        frame_locacoes.pack(pady=10)

        self.carregar_locacoes(frame_locacoes)

        botao_fechar = tk.Button(janela_verificar, text="Fechar", command=janela_verificar.destroy)
        botao_fechar.pack(pady=10)

    def carregar_locacoes(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        self.cursor.execute('SELECT nome_pessoa, data_aluguel, carro_alugado FROM alugueis')
        locacoes = self.cursor.fetchall()
        if locacoes:
            for locacao in locacoes:
                tk.Label(frame, text=f"Nome: {locacao[0]}, Data: {locacao[1]}, Carro: {locacao[2]}").pack(pady=2)
        else:
            tk.Label(frame, text="Nenhuma locação encontrada.").pack(pady=10)

    def carregar_pessoas_cadastradas(self):
        janela_pessoas = tk.Toplevel(self.root)
        janela_pessoas.title("Pessoas Cadastradas")
        janela_pessoas.geometry("700x700")

        frame_pessoas = tk.Frame(janela_pessoas)
        frame_pessoas.pack(pady=10)

        tk.Label(frame_pessoas, text="Digite o CPF para pesquisar:").pack(pady=5)
        cpf_pesquisa_entry = tk.Entry(frame_pessoas)
        cpf_pesquisa_entry.pack(pady=5)

        buscar_button = tk.Button(frame_pessoas, text="Buscar", command=lambda: self.buscar_pessoa_por_cpf(cpf_pesquisa_entry.get(), frame_pessoas))
        buscar_button.pack(pady=5)

        self.carregar_todas_pessoas(frame_pessoas)

        botao_fechar = tk.Button(janela_pessoas, text="Fechar", command=janela_pessoas.destroy)
        botao_fechar.pack(pady=10)
        janela_pessoas.bind('<Return>', lambda event: self.buscar_pessoa_por_cpf(cpf_pesquisa_entry.get(), frame_pessoas))

    def buscar_pessoa_por_cpf(self, cpf, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        self.cursor.execute('SELECT cpf, nome_pessoa FROM alugueis WHERE cpf=?', (cpf,))
        pessoa = self.cursor.fetchone()
        if pessoa:
            tk.Label(frame, text=f"CPF: {pessoa[0]}, Nome: {pessoa[1]}").pack(pady=2)
        else:
            tk.Label(frame, text="Nenhuma pessoa encontrada com este CPF.").pack(pady=10)

    def carregar_todas_pessoas(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        self.cursor.execute('SELECT cpf, nome_pessoa FROM alugueis')
        pessoas = self.cursor.fetchall()
        if pessoas:
            for pessoa in pessoas:
                tk.Label(frame, text=f"CPF: {pessoa[0]}, Nome: {pessoa[1]}").pack(pady=2)
        else:
            tk.Label(frame, text="Nenhuma pessoa cadastrada encontrada.").pack(pady=10)

    def abrir_alterar_dados(self):
        janela_alterar = tk.Toplevel(self.root)
        janela_alterar.title("Alterar Dados")
        janela_alterar.geometry("700x700")

        frame_alterar = tk.Frame(janela_alterar)
        frame_alterar.pack(pady=10)

        tk.Label(frame_alterar, text="CPF da Pessoa a Alterar:").grid(row=0, column=0, padx=5, pady=5)
        cpf_alterar_entry = tk.Entry(frame_alterar)
        cpf_alterar_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_alterar, text="Novo Nome (opcional):").grid(row=1, column=0, padx=5, pady=5)
        novo_nome_entry = tk.Entry(frame_alterar)
        novo_nome_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_alterar, text="Novo RG (opcional):").grid(row=2, column=0, padx=5, pady=5)
        novo_rg_entry = tk.Entry(frame_alterar)
        novo_rg_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_alterar, text="Nova Rua (opcional):").grid(row=3, column=0, padx=5, pady=5)
        nova_rua_entry = tk.Entry(frame_alterar)
        nova_rua_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_alterar, text="Novo Número (opcional):").grid(row=4, column=0, padx=5, pady=5)
        novo_numero_entry = tk.Entry(frame_alterar)
        novo_numero_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_alterar, text="Novo Bairro (opcional):").grid(row=5, column=0, padx=5, pady=5)
        novo_bairro_entry = tk.Entry(frame_alterar)
        novo_bairro_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(frame_alterar, text="Nova Cidade (opcional):").grid(row=6, column=0, padx=5, pady=5)
        nova_cidade_entry = tk.Entry(frame_alterar)
        nova_cidade_entry.grid(row=6, column=1, padx=5, pady=5)

        alterar_button = tk.Button(frame_alterar, text="Alterar", command=lambda: self.alterar_dados(cpf_alterar_entry.get(), novo_nome_entry.get(), novo_rg_entry.get(), nova_rua_entry.get(), novo_numero_entry.get(), novo_bairro_entry.get(), nova_cidade_entry.get()))
        alterar_button.grid(row=7, columnspan=2, pady=10)

        fechar_button = tk.Button(frame_alterar, text="Fechar", command=janela_alterar.destroy)
        fechar_button.grid(row=8, columnspan=2, pady=10)
        janela_alterar.bind('<Return>', lambda event: self.alterar_dados(cpf_alterar_entry.get(), novo_nome_entry.get(), novo_rg_entry.get(), nova_rua_entry.get(), novo_numero_entry.get(), novo_bairro_entry.get(), nova_cidade_entry.get()))

    def alterar_dados(self, cpf, novo_nome, novo_rg, nova_rua, novo_numero, novo_bairro, nova_cidade):
        try:
            if novo_nome:
                self.cursor.execute('UPDATE alugueis SET nome_pessoa=? WHERE cpf=?', (novo_nome, cpf))
            if novo_rg:
                self.cursor.execute('UPDATE alugueis SET rg=? WHERE cpf=?', (novo_rg, cpf))
            if nova_rua:
                self.cursor.execute('UPDATE alugueis SET rua=? WHERE cpf=?', (nova_rua, cpf))
            if novo_numero:
                self.cursor.execute('UPDATE alugueis SET numero=? WHERE cpf=?', (novo_numero, cpf))
            if novo_bairro:
                self.cursor.execute('UPDATE alugueis SET bairro=? WHERE cpf=?', (novo_bairro, cpf))
            if nova_cidade:
                self.cursor.execute('UPDATE alugueis SET cidade=? WHERE cpf=?', (nova_cidade, cpf))

            self.conn.commit()
            messagebox.showinfo("Sucesso", "Dados alterados com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao alterar dados: {e}")

    def abrir_deletar_dados(self):
        janela_deletar = tk.Toplevel(self.root)
        janela_deletar.title("Deletar Dados")
        janela_deletar.geometry("400x300")

        frame_deletar = tk.Frame(janela_deletar)
        frame_deletar.pack(pady=10)

        tk.Label(frame_deletar, text="CPF da Pessoa a Deletar:").grid(row=0, column=0, padx=5, pady=5)
        cpf_deletar_entry = tk.Entry(frame_deletar)
        cpf_deletar_entry.grid(row=0, column=1, padx=5, pady=5)

        deletar_button = tk.Button(frame_deletar, text="Deletar", command=lambda: self.deletar_dados(cpf_deletar_entry.get(), janela_deletar))
        deletar_button.grid(row=1, columnspan=2, pady=10)

        fechar_button = tk.Button(frame_deletar, text="Fechar", command=janela_deletar.destroy)
        fechar_button.grid(row=2, columnspan=2, pady=10)
        janela_deletar.bind('<Return>', lambda event: self.deletar_dados(cpf_deletar_entry.get(), janela_deletar))

    def deletar_dados(self, cpf, janela_deletar):
        try:
            self.cursor.execute('DELETE FROM alugueis WHERE cpf=?', (cpf,))
            if self.cursor.rowcount == 0:
                messagebox.showerror("Erro", "CPF não encontrado.")
            else:
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Dados deletados com sucesso.")
                janela_deletar.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao deletar dados: {e}")

    def abrir_gerar_termo(self):
        janela_termo = tk.Toplevel(self.root)
        janela_termo.title("Gerar Termo de Responsabilidade")
        janela_termo.geometry("700x400")

        label_cpf = tk.Label(janela_termo, text="Digite o CPF:")
        label_cpf.pack(pady=5)

        cpf_entry = tk.Entry(janela_termo)
        cpf_entry.pack(pady=5)

        gerar_button = tk.Button(janela_termo, text="Gerar Termo", command=lambda: self.gerar_termo(cpf_entry.get()))
        gerar_button.pack(pady=10)

        botao_fechar = tk.Button(janela_termo, text="Fechar", command=janela_termo.destroy)
        botao_fechar.pack(pady=10)
        janela_termo.bind('<Return>', lambda event: self.gerar_termo(cpf_entry.get()))

    def gerar_termo(self, cpf):
        self.cursor.execute('SELECT nome_pessoa, cidade, rg, rua, numero, bairro FROM alugueis WHERE cpf=?', (cpf,))
        informacoes = self.cursor.fetchone()

        if informacoes:
            nome, cidade, rg, rua, numero, bairro = informacoes
            c = canvas.Canvas(f"Termo_de_Responsabilidade_{cpf}.pdf", pagesize=letter)

            image_path = r'C:\Users\paulo\OneDrive\Imagens\foto.png'
            c.drawImage(ImageReader(image_path), 200, 700, width=200, height=100)

            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(300, 650, "Termo de Responsabilidade")

            c.setFont("Helvetica", 12)
            text = c.beginText(10, 600)
            text.setFont("Helvetica", 12)
            text.textLines(f"""
            Eu, {nome},
            Residente à {cidade}, {rua}, {numero}, {bairro},
            CPF: {cpf} RG: {rg},
            Estou locando o carro _______________________________ placa nº __________________________
            Pertencente ao Sr. Raniere Farias Santos (MF SERVIÇOS LTDA – ME). Caberá ao LOCATÁRIO
            devolver o veículo nas mesmas condições que lhe foi entregue, inclusive reabastecido, excetuando
            apenas o desgaste natural decorrente do seu uso regular, respondendo criminalmente por troca de
            acessórios ou peças integrantes do veículo efetuadas indevidamente. Caberá ao LOCATÁRIO
            reembolsar a Raniere Farias Santos, a importância referente a multas e infrações de trânsito aplicadas
            durante o período de locação, até a devolução do veículo. O pagamento das multas deve ser feito ao
            locador assim que identificadas. Em caso de acidente, o LOCATÁRIO deverá providenciar o registro
            de ocorrência policial, coletando dados referentes ao outro veículo e respectivo motorista, bilhete de
            seguro, vítimas, testemunhas, número do boletim de ocorrência e indicação da autoridade que
            elaborou comunicado imediatamente a Raniere Farias Santos. Utilizar de toda cautela para minimizar
            as possibilidades de danos ou furtos, não abandonando o veículo, nem transferindo a sua posse a
            terceiros e quando o estacionar fazer o uso do alarme, cadeado, ou por outro meio inibitório para
            evitar a ocorrência de danos e furtos do carro, sempre visando defender e proteger o veículo locado,
            não o deixando em lugares ermos ou perigosos, devendo preferencialmente estacioná-lo em parques
            amentos ou estacionamentos. O LOCATÁRIO terá um prazo de até 1 (uma) hora de tolerância para
            fazer a devolução do veículo, após a hora de tolerância será cobrado R$ 10,00 (Dez reais) por hora
            excedida. O LOCATÁRIO será responsável pelo pagamento da franquia do seguro no caso de
            qualquer sinistro.

            LOCAÇÃO:
            
            Data: ____/____/____ Hora: ____:____
            
            DEVOLUÇÃO:
            
            Data: ____/____/____ Hora: ____:____
            """)
            c.drawText(text)

            c.setFont("Helvetica", 12)
            c.drawCentredString(300, 110, "Pesqueira, ______ de ________________ de 2024.")
            c.drawCentredString(300, 70, "Assinatura: _____________________________________________________")
            c.drawCentredString(300, 50, "Telefone: _______________________________________________________")

            c.setFont("Helvetica", 10)
            c.drawCentredString(300, 15, "Rua Glicério de Almeida Maciel, 83 – Centenário - Pesqueira/PE – Brasil – CEP: 55200-000")
            c.drawCentredString(300, 5, "Telefone para contato: (87) 99101 5207")

            c.save()

            messagebox.showinfo("Sucesso", f"Termo de Responsabilidade gerado com sucesso: Termo_de_Responsabilidade_{cpf}.pdf")
        else:
            messagebox.showerror("Erro", "Nenhuma informação encontrada para este CPF.")

    def abrir_pesquisar_por_cpf(self):
        janela_pesquisar_cpf = tk.Toplevel(self.root)
        janela_pesquisar_cpf.title("Pesquisar por CPF")
        janela_pesquisar_cpf.geometry("700x400")

        label_cpf = tk.Label(janela_pesquisar_cpf, text="Digite o CPF:")
        label_cpf.pack(pady=5)

        cpf_entry = tk.Entry(janela_pesquisar_cpf)
        cpf_entry.pack(pady=5)

        buscar_button = tk.Button(janela_pesquisar_cpf, text="Buscar", command=lambda: self.buscar_informacoes_por_cpf(cpf_entry.get(), janela_pesquisar_cpf))
        buscar_button.pack(pady=10)

        resultado_frame = tk.Frame(janela_pesquisar_cpf)
        resultado_frame.pack(pady=10)

        janela_pesquisar_cpf.resultado_frame = resultado_frame
        janela_pesquisar_cpf.bind('<Return>', lambda event: self.buscar_informacoes_por_cpf(cpf_entry.get(), janela_pesquisar_cpf))

    def buscar_informacoes_por_cpf(self, cpf, janela_pesquisar_cpf):
        for widget in janela_pesquisar_cpf.resultado_frame.winfo_children():
            widget.destroy()

        self.cursor.execute('SELECT nome_pessoa, rg, rua, numero, bairro, cidade FROM alugueis WHERE cpf=?', (cpf,))
        informacoes = self.cursor.fetchone()

        if informacoes:
            labels = ["Nome:", "RG:", "Rua:", "Número:", "Bairro:", "Cidade:"]
            for i, info in enumerate(informacoes):
                tk.Label(janela_pesquisar_cpf.resultado_frame, text=f"{labels[i]} {info}").pack(pady=2)
        else:
            tk.Label(janela_pesquisar_cpf.resultado_frame, text="Nenhuma informação encontrada para este CPF.").pack(pady=10)

    def abrir_pesquisar_veiculos(self):
        janela_pesquisar = tk.Toplevel(self.root)
        janela_pesquisar.title("Pesquisar Veículos")
        janela_pesquisar.geometry("700x700")

        label_carro = tk.Label(janela_pesquisar, text="Selecione o carro:")
        label_carro.pack(pady=5)

        carro_var = tk.StringVar(janela_pesquisar)
        carro_var.set(self.carros_disponiveis[0])

        menu_carros = tk.OptionMenu(janela_pesquisar, carro_var, *self.carros_disponiveis)
        menu_carros.pack(pady=10)

        botao_fechar = tk.Button(janela_pesquisar, text="Fechar", command=janela_pesquisar.destroy)
        botao_fechar.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AluguelCarrosApp(root)
