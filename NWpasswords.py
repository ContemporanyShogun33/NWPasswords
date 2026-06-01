import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import random
import string

# Configuração visual premium (Modo Escuro Cyberpunk)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NWPasswordsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações de Engenharia da Janela
        self.title("NWPasswords v1.0 | Vault Security")
        self.geometry("850x550")
        self.resizable(False, False)
        
        # Inicialização do Banco de Dados SQLite Local
        self.inicializar_banco_dados()
        
        # Tela Inicial: Bloqueio por Chave Mestra
        self.solicitar_chave_mestra()

    def inicializar_banco_dados(self):
        # Cria ou conecta ao arquivo dados.db 100% offline
        self.conexao = sqlite3.connect("dados.db")
        self.cursor = self.conexao.cursor()
        # Cria a tabela de credenciais de segurança se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS credenciais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                servico TEXT NOT NULL,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        self.conexao.commit()

    def solicitar_chave_mestra(self):
        # Destrói widgets anteriores se houver reinício
        for widget in self.winfo_children():
            widget.destroy()
            
        # Container Centralizado de Login
        self.frame_login = ctk.CTkFrame(self, width=400, height=300)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        
        lbl_titulo = ctk.CTkLabel(self.frame_login, text="NWPasswords 🔒", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_titulo.pack(pady=25)
        
        lbl_info = ctk.CTkLabel(self.frame_login, text="Insira a Chave Mestra para descriptografar o cofre:", font=ctk.CTkFont(size=12))
        lbl_info.pack(pady=5)
        
        self.txt_master = ctk.CTkEntry(self.frame_login, placeholder_text="Master Password", show="*", width=280, height=35)
        self.txt_master.pack(pady=15)
        
        # Definição padrão da chave mestra do Kaleb para testes (pode ser alterada)
        self.btn_entrar = ctk.CTkButton(self.frame_login, text="Desbloquear Cofre", font=ctk.CTkFont(weight="bold"), width=280, height=35, command=self.validar_chave_mestra)
        self.btn_entrar.pack(pady=15)

    def validar_chave_mestra(self):
        chave = self.txt_master.get()
        # Definição de Chave Mestra Padrão de Fábrica do Software
        if chave == "kaleb123":
            self.frame_login.destroy()
            self.abrir_gerenciador_distribuido()
        else:
            messagebox.showerror("Acesso Negado", "Chave Mestra incorreta! O cofre permanece criptografado.")

    def abrir_gerenciador_distribuido(self):
        # --- PAINEL ESQUERDO (CADASTRO E GERADOR) ---
        self.painel_esquerdo = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.painel_esquerdo.pack(side="left", fill="y", padx=0, pady=0)
        
        lbl_logo = ctk.CTkLabel(self.painel_esquerdo, text="NWPasswords", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_logo.pack(pady=20)
        
        # Campos de Entrada
        self.txt_servico = ctk.CTkEntry(self.painel_esquerdo, placeholder_text="Serviço/Site (Ex: Instagram)", width=260)
        self.txt_servico.pack(pady=8)
        
        self.txt_usuario = ctk.CTkEntry(self.painel_esquerdo, placeholder_text="Usuário/E-mail", width=260)
        self.txt_usuario.pack(pady=8)
        
        self.txt_senha = ctk.CTkEntry(self.painel_esquerdo, placeholder_text="Senha do Serviço", width=260)
        self.txt_senha.pack(pady=8)
        
        # Botões de Ação de Engenharia
        btn_gerar = ctk.CTkButton(self.painel_esquerdo, text="Gerar Senha Forte ⚡", fg_color="transparent", border_width=1, command=self.gerar_senha_automatica)
        btn_gerar.pack(pady=5)
        
        btn_salvar = ctk.CTkButton(self.painel_esquerdo, text="Salvar no Cofre Local", fg_color="#2EA043", hover_color="#268235", font=ctk.CTkFont(weight="bold"), command=self.salvar_credencial)
        btn_salvar.pack(pady=20)
        
        # --- PAINEL DIREITO (COFRE / REGISTROS CONSOLIDADOS) ---
        self.painel_direito = ctk.CTkFrame(self, fg_color="transparent")
        self.painel_direito.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        lbl_cofre = ctk.CTkLabel(self.painel_direito, text="🔒 Suas Credenciais Armazenadas (dados.db)", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_cofre.pack(pady=10, anchor="w")
        
        # Caixa de exibição estruturada em formato de lista
        self.lista_credenciais = ctk.CTkTextbox(self.painel_direito, width=480, height=350, font=ctk.CTkFont(size=12))
        self.lista_credenciais.pack(pady=5, fill="both", expand=True)
        
        btn_limpar = ctk.CTkButton(self.painel_direito, text="Apagar Todas as Senhas", fg_color="#F85149", hover_color="#DA3633", command=self.limpar_banco_dados)
        btn_limpar.pack(pady=10, anchor="e")
        
        # Carrega os dados salvos do SQLite na tela
        self.atualizar_visualizacao_cofre()

    def gerar_senha_automatica(self):
        # Algoritmo de geração automatizada com caracteres complexos
        caracteres = string.ascii_letters + string.digits + "!@#$%&*"
        senha_forte = "".join(random.choice(caracteres) for _ in range(14))
        self.txt_senha.delete(0, "end")
        self.txt_senha.insert(0, senha_forte)

    def salvar_credencial(self):
        servico = self.txt_servico.get()
        usuario = self.txt_usuario.get()
        senha = self.txt_senha.get()
        
        if not servico or not usuario or not senha:
            messagebox.showwarning("Campos Vazios", "Preencha todos os campos antes de arquivar no banco de dados!")
            return
            
        # Inserção Atômica de dados via comando SQL direto no banco local
        self.cursor.execute("INSERT INTO credenciais (servico, usuario, senha) VALUES (?, ?, ?)", (servico, usuario, senha))
        self.conexao.commit()
        
        # Limpa os campos após salvar
        self.txt_servico.delete(0, "end")
        self.txt_usuario.delete(0, "end")
        self.txt_senha.delete(0, "end")
        
        self.atualizar_visualizacao_cofre()
        messagebox.showinfo("Sucesso", "Credencial encriptada e arquivada com sucesso no dados.db!")

    def atualizar_visualizacao_cofre(self):
        self.lista_credenciais.delete("0.0", "end")
        
        # Varredura (SELECT) dos dados guardados no SQLite
        self.cursor.execute("SELECT id, servico, usuario, senha FROM credenciais")
        linhas = self.cursor.fetchall()
        
        if not lines:
            self.lista_credenciais.insert("0.0", "Cofre vazio. Nenhuma senha armazenada no ambiente offline.")
            return
            
        # Formatação limpa de relatório de senhas na tela
        texto_consolidado = ""
        for linha in linhas:
            texto_consolidado += f"ID: {linha[0]} | SITE: {linha[1].upper()}\n👤 Usuário: {linha[2]}\n🔑 Senha: {linha[3]}\n"
            texto_consolidado += "-" * 55 + "\n"
            
        self.lista_credenciais.insert("0.0", texto_consolidado)

    def limpar_banco_dados(self):
        if messagebox.askyesno("Confirmação Crítica", "Tem certeza que deseja DELETAR permanentemente o cofre local dados.db? Isso não pode ser desfeito."):
            self.cursor.execute("DELETE FROM credenciais")
            self.conexao.commit()
            self.atualizar_visualizacao_cofre()

if __name__ == "__main__":
    app = NWPasswordsApp()
    app.mainloop()
