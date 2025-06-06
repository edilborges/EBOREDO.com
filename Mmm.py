import streamlit as st
import json
import os
from datetime import datetime

# Arquivos
ARQ_USUARIOS = "usuarios.json"
ARQ_CODIGOS_USADOS = "codigos_usados.json"
ARQ_ACESSOS = "acessos.json"

# Códigos válidos (você pode aumentar essa lista)
codigos_validos = ["Desenvolvedor"]

# Funções para carregar e salvar usuários
def carregar_usuarios():
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    with open(ARQ_USUARIOS, "w") as f:
        json.dump(usuarios, f)

# Funções para controlar códigos usados
def carregar_codigos_usados():
    if os.path.exists(ARQ_CODIGOS_USADOS):
        with open(ARQ_CODIGOS_USADOS, "r") as f:
            return json.load(f)
    return []

def salvar_codigo_usado(codigo):
    usados = carregar_codigos_usados()
    usados.append(codigo)
    with open(ARQ_CODIGOS_USADOS, "w") as f:
        json.dump(usados, f)

# Função para registrar acesso
def registrar_acesso(usuario):
    if os.path.exists(ARQ_ACESSOS):
        with open(ARQ_ACESSOS, "r") as f:
            acessos = json.load(f)
    else:
        acessos = []

    acessos.append({
        "usuario": usuario,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(ARQ_ACESSOS, "w") as f:
        json.dump(acessos, f)

# Carrega dados
usuarios = carregar_usuarios()
codigos_usados = carregar_codigos_usados()

# Interface
st.title("Área Protegida - Login e Cadastro")

opcao = st.radio("Escolha uma opção:", ["Login", "Cadastrar"])

if opcao == "Cadastrar":
    st.subheader("Cadastro de novo usuário")
    novo_usuario = st.text_input("Nome de usuário")
    nova_senha = st.text_input("Senha", type="password")
    codigo = st.text_input("Código de aprovação")

    if st.button("Cadastrar"):
        if codigo not in codigos_validos:
            st.error("❌ Código inválido.")
        elif codigo in codigos_usados:
            st.error("⚠️ Este código já foi usado. Solicite outro.")
        elif novo_usuario in usuarios:
            st.warning("⚠️ Este usuário já existe.")
        else:
            usuarios[novo_usuario] = nova_senha
            salvar_usuarios(usuarios)
            salvar_codigo_usado(codigo)
            st.success("✅ Cadastro realizado com sucesso!")

elif opcao == "Login":
    st.subheader("Login")
    usuario = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            registrar_acesso(usuario)  # ⬅️ registra o acesso
            st.success(f"🎉 Bem-vindo, {usuario}!")
            st.markdown("---")
            st.markdown("### Conteúdo liberado:")
            st.write("- ✅ Acesso autorizado")
            st.write("- 📂 Material exclusivo")

            # Mostrar histórico de acessos (opcional)
            if st.checkbox("📜 Ver quem já acessou"):
                if os.path.exists(ARQ_ACESSOS):
                    with open(ARQ_ACESSOS, "r") as f:
                        acessos = json.load(f)
                        for a in acessos:
                            st.write(f"👤 {a['usuario']} - {a['data']}")
                else:
                    st.write("Nenhum acesso registrado ainda.")
        else:
            st.error("❌ Usuário ou senha incorretos.")
