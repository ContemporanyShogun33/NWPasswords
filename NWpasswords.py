import streamlit as st
import sqlite3
import random
import string
import hashlib
import os
import base64

# 1. Configuração de Arquitetura Web de Alta Performance
st.set_page_config(
    page_title="NWPasswords | Cryptographic Vault Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 UI/UX DE ANALISTA LÓGICO COM ANIMAÇÃO DA SENHA DANÇANDO
st.markdown("""
<style>
    /* Estilização Executiva (Azul e Branco sobre Fundo Escuro) */
    .vault-card {
        background-color: #0D1117;
        border: 2px solid #58A6FF;
        padding: 12px;
        border-radius: 10px;
        height: 52px;
        display: flex;
        align-items: center;
    }
    .card-text { color: #FFFFFF !important; font-size: 14px; font-weight: 500; }
    
    /* ANIMAÇÃO DA SENHA DANÇANDO (Efeito Wave Interativo) */
    @keyframes dance {
        0% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-3px) rotate(-1deg); }
        50% { transform: translateY(0px) rotate(0deg); }
        75% { transform: translateY(3px) rotate(1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    /* Aplica o efeito quando o usuário passa o mouse na senha */
    .stCodeBlock:hover {
        animation: dance 0.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

ARQUIVO_CHAVE = "master_web.key"
BANCO_DADOS = "dados_web.db"

# --- ENGINE DE CRIPTOGRAFIA PROPRIETÁRIA (MATEMÁTICA PURA NATIVA) ---
def criptografar_texto(texto, chave_mestra):
    chave_numerica = [ord(c) for c in hashlib.sha256(chave_mestra.encode()).hexdigest()]
    texto_cripto = ""
    for i, caractere in enumerate(texto):
        deslocamento = chave_numerica[i % len(chave_numerica)]
        novo_caractere = chr((ord(caractere) + deslocamento) % 1114111)
        texto_cripto += novo_caractere
    return base64.b64encode(texto_cripto.encode('utf-8')).decode('utf-8')

def descriptografar_texto(texto_criptografado, chave_mestra):
    try:
        texto_original_b64 = base64.b64decode(texto_criptografado.encode('utf-8')).decode('utf-8')
        chave_numerica = [ord(c) for c in hashlib.sha256(chave_mestra.encode()).hexdigest()]
        texto_limpo = ""
        for i, caractere in enumerate(texto_original_b64):
            deslocamento = chave_numerica[i % len(chave_numerica)]
            original = chr((ord(caractere) - deslocamento) % 1114111)
            texto_limpo += original
        return texto_limpo
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

# Estados de sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "senha_mestra_sessao" not in st.session_state:
    st.session_state.senha_mestra_sessao = ""

# --- FLUXO 1: CADASTRO INICIAL DA CHAVE MESTRA ---
if not os.path.exists(ARQUIVO_CHAVE):
    st.title("Configurar NWPasswords Pro 🔒")
    st.subheader("Crie sua chave mestra para inicializar o ecossistema de chaves simétricas.")
    
    nova_master = st.text_input("Defina sua Chave Mestra:", type="password")
    if st.button("Ativar Criptografia do Cofre", type="primary"):
        if len(nova_master) < 6:
            st.warning("A senha mestra precisa ter pelo menos 6 caracteres.")
        else:
            hash_validacao = hashlib.sha256(nova_master.encode()).hexdigest()
            with open(ARQUIVO_CHAVE, "w") as f:
                f.write(hash_validacao)
            st.success("Cofre criptografado com sucesso! Recarregando...")
            st.rerun()

# --- FLUXO 2: TELA DE LOGIN ---
elif not st.session_state.autenticado:
    st.title("NWPasswords | Autenticação Requerida 🔒")
    st.subheader("O banco de dados está trancado. Insira a credencial mestra:")
    
    senha_login = st.text_input("Chave Mestra:", type="password")
    if st.button("Desbloquear Cofre", type="primary"):
        hash_digitado = hashlib.sha256(senha_login.encode()).hexdigest()
        
        with open(ARQUIVO_CHAVE, "r") as f:
            hash_salvo = f.read().strip()
        
        if hash_digitado == hash_salvo:
            st.session_state.autenticado = True
            st.session_state.senha_mestra_sessao = senha_login
            st.rerun()
        else:
            st.error("Chave Mestra incorreta! Acesso negado.")

# --- FLUXO 3: GERENCIADOR PREMIUM (PAINEL PRINCIPAL) ---
else:
    st.title("NWPasswords Pro Enterprise 🖥️")
    st.caption("Gerenciador Distribuído de Cibersegurança | Arquitetura Kaleb Machado")
    st.markdown("---")
    
    # --- 📐 PAINEL LATERAL (SUPORTE, FEEDBACK E FÉ) ---
    st.sidebar.title("Central NW 📊")
    st.sidebar.caption("Modo Analista Ativo")
    st.sidebar.markdown("---")
    
    # Momento de Fé
    st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")
    st.sidebar.markdown("---")
    
    # Central de Ajuda Integrada
    st.sidebar.subheader("❓ Central de Ajuda")
    st.sidebar.markdown("""
    * **Como salvar?** Digite os dados à direita e clique em Injetar.
    * **Botão Copiar:** Fica direto no componente de texto da senha.
    * **Segurança:** Dados salvos localmente e criptografados.
    """)
    st.sidebar.markdown("---")
    
    # Linha de Feedback
    st.sidebar.subheader("💬 Linha de Feedback")
    nome_feed = st.sidebar.text_input("Nome do Usuário:", key="feed_nome")
    msg_feed = st.sidebar.text_area("O que achou do NWPasswords?", key="feed_msg")
    if st.sidebar.button("Enviar para a Holding", use_container_width=True):
        if nome_feed and msg_feed:
            st.sidebar.success(f"Obrigado, {nome_feed}! Kaleb Machado recebeu sua análise.")
        else:
            st.sidebar.warning("Preencha os campos de feedback.")
            
    st.sidebar.markdown("---")
    if st.sidebar.button("Bloquear Cofre (Sair)", type="primary", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.senha_mestra_sessao = ""
        st.rerun()

    # --- CORPO PRINCIPAL DIREITO ---
    col_cadastro, col_cofre = st.columns([1, 1.4])
    
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
                senha_real = st.session_state.get("senha_sugerida", "default_pass")
                if senha_real == "default_pass": 
                    senha_real = senha
                
                senha_criptografada = criptografar_texto(senha_real, st.session_state.senha_mestra_sessao)
                cursor.execute("INSERT INTO credenciais (servico, usuario, senha) VALUES (?, ?, ?)", (servico, usuario, senha_criptografada))
                conn.commit()
                
                if "senha_sugerida" in st.session_state:
                    del st.session_state.senha_sugerida
                st.success(f"Dados trancados para {servico}!")
                st.rerun()

    with col_cofre:
        st.write("### 🔑 Suas Credenciais Protegidas")
        busca = st.text_input("🔍 Rastrear serviço ou site:")
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
                senha_real_exibir = descriptografar_texto(sen_cripto, st.session_state.senha_mestra_sessao)
                
                # Alinhamento tático impecável de colunas
                c_info, c_senha_dançando = st.columns([1.5, 1])
                
                with c_info:
                    st.markdown(f"""
                    <div class="vault-card">
                        <div class="card-text">
                            <span style="color: #58A6FF; font-weight: bold;">🌐 {serv.upper()}</span><br>
                            <span style="color: #8B949E; font-size: 11px;">👤 Usuário: {usu}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with c_senha_dançando:
                    st.code(f"{senha_real_exibir}", language="text")
                    
        st.write("##")
        if st.button("Formatar e Deletar Base Total"):
            cursor.execute("DELETE FROM credenciais")

