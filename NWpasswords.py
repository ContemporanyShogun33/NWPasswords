import streamlit as st
import sqlite3
import random
import string
import hashlib
import os
import base64
from cryptography.fernet import Fernet

# Configuração da página web em Modo Escuro
st.set_page_config(page_title="NWPasswords | Cryptographic Vault", layout="wide")

# Estilização CSS premium
st.markdown("""
<style>
    .vault-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

ARQUIVO_CHAVE = "master_web.key"
BANCO_DADOS = "dados_web.db"

# --- ENGINE DE CRIPTOGRAFIA AVANÇADA (AES-256 FERNET) ---
def gerar_chave_derivada(senha_mestra):
    # Deriva uma chave Fernet de 32 bytes usando o hash SHA-256 da senha mestra
    hash_senha = hashlib.sha256(senha_mestra.encode()).digest()
    return base64.urlsafe_b64encode(hash_senha)

def criptografar_texto(texto, chave):
    f = Fernet(chave)
    return f.encrypt(texto.encode()).decode()

def descriptografar_texto(texto_criptografado, chave):
    try:
        f = Fernet(chave)
        return f.decrypt(texto_criptografado.encode()).decode()
    except Exception:
        return "⚠️ Erro de Descriptografia"

# --- ENGINE DO BANCO DE DADOS SQLITE ---
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

conn, cursor = inicializar_banco()

# Estados de sessão no navegador
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "chave_sessao" not in st.session_state:
    st.session_state.chave_sessao = None

# --- FLUXO 1: CADASTRO INICIAL DA CHAVE MESTRA ---
if not os.path.exists(ARQUIVO_CHAVE):
    st.title("Configurar NWPasswords Crypt 🔒")
    st.subheader("Crie sua chave mestra. Seus dados serão trancados com criptografia simétrica AES-256.")
    
    nova_master = st.text_input("Defina sua Chave Mestra:", type="password")
    if st.button("Ativar Criptografia do Cofre", type="primary"):
        if len(nova_master) < 6:
            st.warning("A senha mestra precisa ter pelo menos 6 caracteres.")
        else:
            # Salva o hash para validação de login futura
            hash_validacao = hashlib.sha256(nova_master.encode()).hexdigest()
            with open(ARQUIVO_CHAVE, "w") as f:
                f.write(hash_validacao)
            st.success("Cofre criptografado com sucesso! Atualizando...")
            st.rerun()

# --- FLUXO 2: TELA DE LOGIN ---
elif not st.session_state.autenticado:
    st.title("NWPasswords | Criptografado 🔒")
    st.subheader("O banco dados_web.db está encriptado. Insira a Chave Mestra:")
    
    senha_login = st.text_input("Chave Mestra:", type="password")
    if st.button("Desbloquear e Derivar Chaves", type="primary"):
        hash_digitado = hashlib.sha256(senha_login.encode()).hexdigest()
        
        with open(ARQUIVO_CHAVE, "r") as f:
            hash_salvo = f.read().strip()
        
        if hash_digitado == hash_salvo:
            st.session_state.autenticado = True
            # DERIVAÇÃO DA CHAVE: Guarda a chave de descriptografia apenas na memória da sessão
            st.session_state.chave_sessao = gerar_chave_derivada(senha_login)
            st.rerun()
        else:
            st.error("Chave Mestra incorreta! Os dados permanecem trancados em blocos binários.")

# --- FLUXO 3: GERENCIADOR CRIPTOGRAFADO (PAINEL PRINCIPAL) ---
else:
    st.title("NWPasswords Enterprise v3.0 🖥️")
    st.caption("Cofre de Senhas Criptografado em Nuvem | Arquitetura Kaleb Machado")
    st.markdown("---")
    
    # Barra Lateral
    st.sidebar.title("NWPasswords Crypt")
    st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")
    if st.sidebar.button("Bloquear Cofre (Sair)", type="primary"):
        st.session_state.autenticado = False
        st.session_state.chave_sessao = None
        st.rerun()

    col_cadastro, col_cofre = st.columns([1, 1.3])
    
    with col_cadastro:
        st.write("### ➕ Criptografar Nova Credencial")
        servico = st.text_input("Serviço / Site (Ex: Google):")
        usuario = st.text_input("Usuário / E-mail:")
        
        col_senha, col_btn_gerar = st.columns(2)
        with col_senha:
            senha = st.text_input("Senha do Serviço:", type="password" if "senha_sugerida" not in st.session_state else "default")
        with col_btn_gerar:
            st.write("##")
            if st.button("Gerar Forte ⚡", use_container_width=True):
                caracteres = string.ascii_letters + string.digits + "!@#$%&*"
                st.session_state.senha_sugerida = "".join(random.choice(caracteres) for _ in range(16))
                st.rerun()
                
        if "senha_sugerida" in st.session_state:
            st.info(f"**Sugestão:** `{st.session_state.senha_sugerida}`")

        if st.button("Injetar Dados Criptografados", type="primary", use_container_width=True):
            if not servico or not usuario or (not senha and "senha_sugerida" not in st.session_state):
                st.warning("Preencha todos os dados.")
            else:
                senha_real = st.session_state.get("senha_sugerida", len)
                if not senha_real or senha_real == len: 
                    senha_real = senha
                
                # CRIPTOGRAFIA ATÔMICA ANTES DE SALVAR NO SQLITE
                senha_criptografada = criptografar_texto(senha_real, st.session_state.chave_sessao)
                
                cursor.execute("INSERT INTO credenciais (servico, usuario, senha) VALUES (?, ?, ?)", (servico, usuario, senha_criptografada))
                conn.commit()
                
                if "senha_sugerida" in st.session_state:
                    del st.session_state.senha_sugerida
                st.success(f"Dados trancados para {servico}!")
                st.rerun()

    with col_cofre:
        st.write("### 🔑 Suas Credenciais Descriptografadas em Tempo Real")
        busca = st.text_input("🔍 Rastrear serviço:")
        st.markdown("---")
        
        if busca:
            cursor.execute("SELECT id, servico, usuario, senha FROM credenciais WHERE servico LIKE ?", (f'%{busca}%',))
        else:
            cursor.execute("SELECT id, servico, usuario, senha FROM credenciais")
            
        linhas = cursor.fetchall()
        
        if not linhas:
            st.caption("Nenhum bloco de dados localizado no cofre.")
        else:
            for id_item, serv, usu, sen_cripto in linhas:
                # DESCRIPTOGRAFIA EM MEMÓRIA APENAS NA HORA DE EXIBIR NA TELA
                senha_real_exibir = descriptografar_texto(sen_cripto, st.session_state.chave_sessao)
                
                st.markdown(f"""
                <div class="vault-card">
                    <span style="color: #58A6FF; font-weight: bold; font-size: 14px;">🌐 {serv.upper()}</span>
                    <span style="color: #8B949E; font-size: 13px; margin-left: 15px;">👤 Usuário: {usu}</span>
                </div>
                """, unsafe_allow_html=True)
                st.code(f"{senha_real_exibir}", language="text")
                    
        st.write("##")
        if st.button("Formatar e Deletar Base Total"):
            cursor.execute("DELETE FROM credenciais")
            conn.commit()
            st.success("Cofre formatado!")
            st.rerun()

