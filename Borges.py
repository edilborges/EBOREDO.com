import streamlit as st
import json
import os
from datetime import datetime

# Arquivos
ARQ_USUARIOS = "usuarios.json"
ARQ_CODIGOS_USADOS = "codigos_usados.json"
ARQ_LOG_REGISTROS = "logs_registros.json"
ARQ_LOG_LOGINS = "logs_logins.json"

# Códigos válidos
codigos_validos = ["INF2025", "ABC123", "COD45"]

# Dados fixos do administrador
ADMIN_USER = "Borges"
ADMIN_PASS = "101419edil"

# Funções para carregar e salvar dados
def carregar_json(caminho, padrao):
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            return json.load(f)
    return padrao

def salvar_json(caminho, dados):
    with open(caminho, "w") as f:
        json.dump(dados, f, indent=4)

# Funções para registrar logs
def registrar_log(caminho, usuario):
    logs = carregar_json(caminho, [])
    logs.append({"usuario": usuario, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    salvar_json(caminho, logs)

# Carrega dados
usuarios = carregar_json(ARQ_USUARIOS, {})
codigos_usados = carregar_json(ARQ_CODIGOS_USADOS, [])
log_registros = carregar_json(ARQ_LOG_REGISTROS, [])
log_logins = carregar_json(ARQ_LOG_LOGINS, [])

# Interface
st.title("Área Protegida - Login e Cadastro")

opcao = st.radio("Escolha uma opção:", ["Login", "Cadastrar"])

# Cadastro
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
            codigos_usados.append(codigo)
            salvar_json(ARQ_USUARIOS, usuarios)
            salvar_json(ARQ_CODIGOS_USADOS, codigos_usados)
            registrar_log(ARQ_LOG_REGISTROS, novo_usuario)
            st.success("✅ Cadastro realizado com sucesso!")

# Login
elif opcao == "Login":
    st.subheader("Login")
    usuario = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.success(f"🎉 Bem-vindo, {usuario}!")
            registrar_log(ARQ_LOG_LOGINS, usuario)

            # Área protegida
            st.markdown("---")
            st.markdown("### Conteúdo liberado:")
            st.write("- ✅ Acesso autorizado")
            st.write("- 📂 Material exclusivo")
            st.markdown("[📘 Guia de Estudo](https://www.empowerdata.com.br/material-yt-guia-estudos-python)")

            # Se for administrador
            if usuario == ADMIN_USER and senha == ADMIN_PASS:
                st.markdown("---")
                st.markdown("## 👑 Painel do Administrador")
                st.subheader("📌 Registros de Cadastro")
                for item in carregar_json(ARQ_LOG_REGISTROS, []):
                    st.write(f"Usuário: `{item['usuario']}` | Data: {item['timestamp']}")

                st.subheader("📌 Registros de Login")
                for item in carregar_json(ARQ_LOG_LOGINS, []):
                    st.write(f"Usuário: `{item['usuario']}` | Data: {item['timestamp']}")

        else:
            st.error("❌ Usuário ou senha incorretos.")
