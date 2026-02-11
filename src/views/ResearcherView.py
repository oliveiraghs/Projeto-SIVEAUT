import streamlit as st
from src.services.DatabaseService import DatabaseService
import pandas as pd
import time

class ResearcherView:
    @staticmethod
    def render(usuario):
        inicial = usuario.nome[0].upper() if usuario.nome else "G"

        # --- CSS PARA USABILIDADE DE CAMPO (Foco Mobile/Tablet) ---
        st.markdown(f"""
            <style>
                body {{ zoom: 0.9; overflow: hidden; }}
                #MainMenu, footer, header {{ display: none !important; }}
                
                .block-container {{
                    padding-top: 1.5rem !important;
                    max-width: 100%;
                }}

                /* Sidebar Cinza Fixa */
                [data-testid="stSidebar"] {{
                    background-color: #D3D3D3 !important;
                    min-width: 200px !important;
                }}

                /* Avatar Laranja */
                .avatar-circle {{
                    width: 65px; height: 65px;
                    background-color: #FF8C00;
                    color: white;
                    border-radius: 50%;
                    text-align: center; line-height: 65px;
                    font-size: 26px; font-weight: bold;
                    margin: 10px auto;
                    border: 3px solid white;
                }}

                /* Card de Coleta */
                [data-testid="stForm"] {{
                    background-color: #FFFFFF;
                    border-radius: 20px;
                    padding: 25px !important;
                    border: 1px solid #E0E0E0;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                }}

                .stSelectbox, .stNumberInput, .stTextInput {{ margin-bottom: -10px !important; }}
            </style>
        """, unsafe_allow_html=True)

        # --- BARRA LATERAL ---
        with st.sidebar:
            st.markdown(f"<div class='avatar-circle'>{inicial}</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center; color:#333; margin:0;'>{usuario.nome}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:#666; font-size:0.9rem;'>PESQUISADOR</p>", unsafe_allow_html=True)
            st.write("---")
            
            st.button("📋 Nova Coleta", use_container_width=True)
            st.button("🕒 Minhas Coletas", use_container_width=True)
            
            st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Sair", type="primary", use_container_width=True):
                del st.session_state['usuario_ativo']
                st.rerun()

        # --- ÁREA DE COLETA ---
        st.markdown("### 📝 Nova Coleta de Campo")
        
        # Coluna única centralizada para facilitar o uso no telemóvel
        _, col_centro, _ = st.columns([0.5, 2, 0.5])

        with col_centro:
            conn = DatabaseService.get_connection()
            try:
                # 1. Busca veículos disponíveis para seleção
                df_veiculos = pd.read_sql_query("SELECT id, marca, modelo, ano FROM veiculos", conn)
                opcoes_veiculos = {f"{row['marca']} {row['modelo']} ({row['ano']})": row['id'] for _, row in df_veiculos.iterrows()}
                
                with st.form("form_coleta", clear_on_submit=True):
                    st.markdown("##### Detalhes do Veículo e Preço")
                    
                    veiculo_selecionado = st.selectbox("Selecione o Veículo:", options=list(opcoes_veiculos.keys()))
                    veiculo_id = opcoes_veiculos[veiculo_selecionado]
                    
                    valor_encontrado = st.number_input("Preço Encontrado (R$):", min_value=0.0, step=500.0, format="%.2f")
                    
                    loja = st.text_input("Nome da Loja/Concessionária:", placeholder="Ex: Campinas Veículos")
                    
                    link_foto = st.text_input("Link da Foto ou Site (Opcional):", placeholder="https://...")

                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if st.form_submit_button("🚀 Gravar Coleta", use_container_width=True, type="primary"):
                        if valor_encontrado > 0 and loja:
                            ResearcherView.salvar_coleta(veiculo_id, usuario.id, valor_encontrado, loja, link_foto)
                            st.success("Coleta registada com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Por favor, preencha o valor e o nome da loja.")

            except Exception as e:
                st.error(f"Erro ao carregar dados: {e}")
            finally:
                conn.close()

    @staticmethod
    def salvar_coleta(v_id, u_id, valor, loja, foto):
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO coletas (veiculo_id, usuario_id, valor_encontrado, local_loja, foto_url)
            VALUES (?, ?, ?, ?, ?)
        """, (v_id, u_id, valor, loja, foto))
        conn.commit()
        conn.close()