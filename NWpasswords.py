import streamlit as st
import sqlite3
import random
import string

# 1. Configuração de Infraestrutura da Página Web
st.set_page_config(page_title="NWPasswords", page_icon="🔐", layout="centered")

st.title("🔐 NWPasswords")
st.caption("Gerenciador de Senhas Offline & Seguro | ContemporanyShogun33")

# 2. Conexão Automática com o Banco de Dados SQLite
conn = sqlite3.connect("dados.db", check_same_thread=False)
cursor = conn.cursor()

# Cria a tabela de segurança se ela não existir no osso do silício
cursor.execute("""
CREATE TABLE IF NOT EXISTS credenciais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    servico TEXT NOT NULL,
    usuario TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")
conn.commit()

# 3. Sistema de Autenticação por Chave Mestra (Segurança Suprema)
st.sidebar.header("🔑 Autenticação")
chave_mestra = st.sidebar.text_input("Digite a Chave Mestra:", type="password")

# Senha mestra padrão para teste (Você pode mudar para a que você quiser)
SENHA_MESTRA_CORRETA = "shogun33"

if not chave_mestra:
    st.info("Aguardando Chave Mestra para liberar o cofre de dados... 🔒")
elif chave_mestra != SENHA_MESTRA_CORRETA:
    st.error("Chave Mestra incorreta! Acesso bloqueado. ❌")
else:
    st.sidebar.success("Cofre Desbloqueado! 🔓")

    # 4. Aba de Navegação do Dashboard
    aba_cadastro, aba_visualizar = st.tabs(["📝 Cadastrar Senha", "🗂️ Ver Cofre"])

    with aba_cadastro:
        st.subheader("Cadastrar Nova Credencial")
        
        servico = st.text_input("Nome do Serviço / Site:", placeholder="Ex: GitHub, Discord")
        usuario = st.text_input("Usuário / E-mail:", placeholder="Ex: kaleb@email.com")
        
        # Gerador Automático de Senhas no próprio painel
        st.write("---")
        gerar_automatica = st.checkbox("Quero que o sistema gere uma senha forte")
        
        if gerar_automatica:
            tamanho = st.slider("Tamanho da senha:", min_value=8, max_value=24, value=14)
            caracteres = string.ascii_letters + string.digits + "!@#$%&*"
            senha_final = "".join(random.choice(caracteres) for _ in range(tamanho))
            st.code(senha_final, language="")
        else:
            senha_final = st.text_input("Digite a sua senha personalizada:", type="password")

        st.write("---")
        if st.button("💾 Salvar no Banco de Dados", use_container_width=True):
            if servico and usuario and senha_final:
                cursor.execute(
                    "INSERT INTO credenciais (servico, usuario, senha) VALUES (?, ?, ?)",
                    (servico, usuario, senha_final)
                )
                conn.commit()
                st.success(f"Credencial para '{servico}' salva com sucesso no dados.db! 🔥")
                st.balloons()
            else:
                st.warning("Preencha todos os campos antes de salvar.")

    with aba_visualizar:
        st.subheader("Suas Senhas Armazenadas")
        
        # Puxa os dados direto da tabela SQLite local
        cursor.execute("SELECT id, servico, usuario, senha FROM credenciais")
        dados = cursor.fetchall()

        if not dados:
            st.info("Nenhuma senha cadastrada ainda no banco local.")
        else:
            search = st.text_input("🔍 Buscar por serviço:", placeholder="Digite para filtrar...")
            
            for item in dados:
                id_banco, serv, usu, sen = item
                
                # Filtro de busca simples
                if search.lower() in serv.lower():
                    with st.expander(f"🌐 {serv} ({usu})"):
                        st.text(f"Usuário: {usu}")
                        st.text(f"Senha: {sen}")
                        
                        # Botão de exclusão cirúrgica
                        if st.button(f"🗑️ Excluir {serv}", key=f"del_{id_banco}"):
                            cursor.execute("DELETE FROM credenciais WHERE id = ?", (id_banco,))
                            conn.commit()
                            st.rerun()
