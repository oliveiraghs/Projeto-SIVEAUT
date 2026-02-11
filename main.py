import streamlit as st
from src.views.LoginView import LoginView
from src.views.AdminView import AdminView
from src.views.ManagerView import ManagerView
from src.views.ResearcherView import ResearcherView # <--- NOVO IMPORT

st.set_page_config(
    page_title="SIVEAUTO", 
    page_icon="🚗", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    if 'usuario_ativo' not in st.session_state:
        LoginView.render()
    else:
        usuario = st.session_state['usuario_ativo']
        
        if usuario.perfil == 'ADMIN':
            AdminView.render(usuario)
        elif usuario.perfil == 'GERENTE':
            ManagerView.render(usuario)
        elif usuario.perfil == 'PESQUISADOR': # <--- NOVA ROTA
            ResearcherView.render(usuario)

if __name__ == "__main__":
    main()