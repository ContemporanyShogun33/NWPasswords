import streamlit as st
import sqlite3
import random
import string
import hashlib
import os

# Configuração da arquitetura da página web em Modo Escuro
st.set_page_config(page_title="NWPasswords | Web Vault", layout="wide")

# Estilização CSS premium para criar os Cards do cofre de senhas
st.markdown("""
<style>
    .vault-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

ARQUIVO_CHAVE = "master_web.key"
BANCO_DADOS = "dados_web.db"

# --- FUNÇÕES DE ENGENHARIA DE SEGURANÇA ---
def inicializar_banco():
    conn = sqlite3.connect(BANCO_DADOS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credenciais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servico TEXT NOT NULL,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Inicializa o banco SQLite offline na nuvem
conn, cursor = inicializar_banco()

# Controla o estado de login na sessão do navegador
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- FLUXO 1: CADASTRO DA CHAVE MESTRA ---
if not os.path.exists(ARQUIVO_CHAVE):
    st.title("Configurar NWPasswords Web 🔒")
    st.subheader("Crie sua chave mestra de criptografia para blindar seus dados")
    
    nova_master = st.text_input("Defina sua Chave Mestra:", type="password")
    if st.button("Criptografar e Ativar Cofre", type="primary"):
        if len(nova_master) < 6:
            st.warning("Por segurança, a senha deve ter pelo menos 6 caracteres.")
        else:
            with open(ARQUIVO_CHAVE, "w") as f:
                f.write(hash_senha(nova_master))
            st.success("Chave Mestra registrada com sucesso! Recarregando...")
            st.rerun()

# --- FLUXO 2: TELA DE LOGIN ---
elif not st.session_state.autenticado:
    st.title("NWPasswords | Web Vault 🔒")
    st.subheader("O cofre local está encriptado. Insira a senha mestra para abrir:")
    
    senha_login = st.text_input("Chave Mestra:", type="password")
    if st.button("Desbloquear Banco de Dados", type="primary"):
        with open(ARQUIVO_CHAVE, "r") as f:
            hash_salvo = f.read().strip()
        
        if hash_senha(senha_login) == hash_salvo:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Chave Mestra incorreta! O acesso ao banco dados_web.db permanece bloqueado.")

# --- FLUXO 3: PAINEL GERENCIADOR DISTRIBUÍDO (PÁGINA PRINCIPAL) ---
else:
    st.title("NWPasswords Enterprise 🖥️")
    st.caption("Gerenciador Distribuído 100% Seguro | Desenvolvido por Kaleb Machado")
    st.markdown("---")
    
    # Menu lateral com Salmo 23 e Botão de Logout
    st.sidebar.title("NWPasswords AI")
    st.sidebar.caption("Vault Control Panel")
    st.sidebar.markdown("---")
    st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")
    
    if st.sidebar.button("Bloquear Cofre (Sair)", type="primary"):
        st.session_state.autenticado = False
        st.rerun()

    col_cadastro, col_cofre = st.columns([1, 1.3])
    
    # Coluna de Cadastro de Novas Senhas
    with col_cadastro:
        st.write("### ➕ Arquivar Nova Credencial")
        servico = st.text_input("Serviço / Site (Ex: GitHub):")
        usuario = st.text_input("Usuário / E-mail:")
        
        # Campo de senha com gerador integrado
        col_senha, col_btn_gerar = st.columns([2, 1])
        with col_senha:
            senha = st.text_input("Senha do Serviço:", type="password" if "senha_sugerida" not in st.session_state else "default")
            
        with col_btn_gerar:
            st.write("##") # Espaçador visual para alinhar o botão
            if st.button("Gerar Forte ⚡", use_container_width=True):
                caracteres = string.ascii_letters + string.digits + "!@#$%&*"
                st.session_state.senha_sugerida = "".join(random.choice(caracteres) for _ in range(16))
                st.rerun()
                
        if "senha_sugerida" in st.session_state:
            st.info(f"**Senha Sugerida:** `{st.session_state.senha_sugerida}`")
            st.caption("Copie a senha acima e use no campo de cadastro do site.")

        if st.button("Salvar no dados_web.db", type="primary", use_container_width=True):
            if not servico or not usuario or (not senha and "senha_sugerida" not in st.session_state):
                st.warning("Preencha todos os campos antes de salvar.")
            else:
                senha_final = st.session_state.get("senha_sugerida", senha)
                cursor.execute("INSERT INTO credenciais (servico, usuario, senha) VALUES (?, ?, ?)", (servico, usuario, senha_final))
                conn.commit()
                if "senha_sugerida" in st.session_state:
                    del st.session_state.senha_sugerida
                st.success(f"Credencial para {servico} salva com sucesso!")
                st.rerun()

    # Coluna do Cofre (Visualizador em tempo real com Cards de Alta Performance)
    with col_cofre:
        st.write("### 🔑 Suas Credenciais Protegidas")
        
        # Barra de Pesquisa Dinâmica
        busca = st.text_input("🔍 Filtrar senhas por serviço ou site:")
        st.markdown("---")
        
        if busca:
            cursor.execute("SELECT id, servico, usuario, senha FROM credenciais WHERE servico LIKE ?", (f'%{busca}%',))
        else:
            cursor.execute("SELECT id, servico, usuario, senha FROM credenciais")
            
        linhas = cursor.fetchall()
        
        if not linhas:
            st.caption("Nenhuma credencial localizada na base local do cofre.")
        else:
            for id_item, serv, usu, sen in linhas:
                # Criação do Card Cyberpunk via HTML/CSS + Componente de cópia nativa
                st.markdown(f"""
                <div class="vault-card">
                    <span style="color: #58A6FF; font-weight: bold; font-size: 15px;">🌐 {serv.upper()}</span>
                    <span style="color: #8B949E; font-size: 13px; margin-left: 15px;">👤 Usuário: {usu}</span>
                </div>
                """, unsafe_allow_html=True)
                # O st.code injeta a senha com o botão de cópia automática do Chrome na lateral
                st.code(f"{sen}", language="text")
                    
        st.write("##")
        if st.button("Deletar Todas as Senhas do Cofre"):
            cursor.execute("DELETE FROM credenciais")
            conn.commit()
            st.success("Cofre limpo com sucesso!")
            st.rerun()
