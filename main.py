import streamlit as st
from src.views.LoginView import LoginView

# 1. Configuração (Sempre o primeiro comando st)
st.set_page_config(page_title="SIVEAUTO", layout="wide")

def main():
    # Teste visual rápido
    st.sidebar.success("Sistema SIVEAUTO Iniciado")
    
    # Chama a tela de login
    LoginView.render()

# 2. CHAMADA OBRIGATÓRIA
if __name__ == "__main__":
    main()