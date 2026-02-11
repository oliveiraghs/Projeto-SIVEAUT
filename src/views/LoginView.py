import streamlit as st
from src.controllers.AuthController import AuthController
from src.models.Veiculo import Veiculo  # <--- Importante!
import time

class LoginView:
    @staticmethod
    def render():
        # --- CSS PERSONALIZADO ---
        st.markdown("""
            <style>
                html, body, [class*="css"] { font-size: 14px; }
                .block-container { max_width: 1000px; padding-top: 2rem; }
                .main-title { font-size: 3rem; fontWeight: 700; color: #333; margin-bottom: 0; }
                .subtitle { font-size: 1.1rem; color: #666; margin-bottom: 3rem; }
                div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 15px; padding: 20px; }
                div.stButton > button:first-child { background-color: #4A90E2; color: white; border: none; }
                .result-box {
                    background-color: #FDF6C4; border: 1px solid #F0E68C;
                    border-radius: 10px; padding: 15px; color: #555;
                    margin-top: 20px; text-align: center; font-size: 0.9rem;
                }
            </style>
        """, unsafe_allow_html=True)

        # --- CABEÇALHO ---
        st.markdown('<div class="main-title">SIVEAUTO 🚗</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Sistema Integrado de Consulta de Veículos Automotores</div>', unsafe_allow_html=True)

        col1, col_gap, col2 = st.columns([1, 0.2, 1.2])

        # --- LADO ESQUERDO: LOGIN ---
        with col1:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center; color: #0F52BA;'>Login</h2>", unsafe_allow_html=True)
                st.markdown("---")
                
                email = st.text_input("Usuário:", placeholder="Digite seu user")
                senha = st.text_input("Senha:", type="password", placeholder="Digite sua senha")
                st.write("") 
                
                if st.button("Entrar", type="primary", use_container_width=True):
                    if not email or not senha:
                        st.warning("Preencha todos os campos!")
                    else:
                        usuario = AuthController.validar_login(email, senha)
                        if usuario:
                            st.toast(f"Bem-vindo, {usuario.nome}!")
                            st.session_state['usuario_ativo'] = usuario
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Credenciais inválidas.")

        # --- LADO DIREITO: CONSULTA RÁPIDA (AGORA REAL) ---
        with col2:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center; color: #006400;'>Consulta FIPE</h2>", unsafe_allow_html=True)
                st.caption("Pesquise na base de dados oficial.")

                # 1. Busca as marcas no Banco de Dados
                opcoes_marcas = ["Selecione"] + Veiculo.get_todas_marcas()
                
                marca = st.selectbox("Marca:", options=opcoes_marcas)
                
                # Campos opcionais para filtro
                col_a, col_b = st.columns(2)
                with col_a:
                    modelo = st.text_input("Modelo (Opcional):", placeholder="Ex: Mobi")
                with col_b:
                    ano = st.text_input("Ano (Opcional):", placeholder="Ex: 2024")

                st.write("")
                
                if st.button("Buscar 🔍", use_container_width=True):
                    if marca == "Selecione":
                        st.warning("Por favor, selecione pelo menos a Marca.")
                    else:
                        # Busca Real no Banco
                        resultados = Veiculo.buscar_por_filtro(marca, modelo, ano)
                        
                        if resultados:
                            # Pega o primeiro resultado (para simplificar a visualização)
                            veic = resultados[0]
                            st.markdown(f"""
                                <div class="result-box">
                                    <strong>Veículo Encontrado:</strong><br><br>
                                    🚗 {veic.marca} {veic.modelo}<br>
                                    📅 Ano: {veic.ano}<br>
                                    💰 Referência FIPE: <strong>R$ {veic.preco_referencia:,.2f}</strong>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Nenhum veículo encontrado com esses dados.")
                else:
                    st.markdown("""
                        <div class="result-box" style="color: #999;">
                            <br>O resultado da pesquisa aparecerá aqui.<br><br>
                        </div>
                    """, unsafe_allow_html=True)