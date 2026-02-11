import streamlit as st
from src.services.DatabaseService import DatabaseService
import pandas as pd
import hashlib
import time

# ⚠️ IMPORTANTE: Se este não for seu arquivo principal, mova este bloco 
# st.set_page_config para a PRIMEIRA LINHA do seu arquivo main.py ou app.py
try:
    st.set_page_config(
        page_title="Admin System",
        layout="wide",
        initial_sidebar_state="expanded" # Isso obriga a sidebar a abrir
    )
except:
    pass

class AdminView:
    @staticmethod
    def render(usuario):
        # 1. Gerenciamento de Navegação e Estados
        if 'admin_aba' not in st.session_state:
            st.session_state['admin_aba'] = 'Usuarios'
        
        if 'user_to_edit' not in st.session_state:
            st.session_state['user_to_edit'] = None

        nome_display = usuario.nome if usuario and usuario.nome else "Admin"
        inicial = nome_display[0].upper()

        # --- CSS FORTE PARA RECUPERAR A SIDEBAR ---
        st.markdown(f"""
            <style>
                /* 1. FUNDO CINZA MAIS ESCURO (Conforme pedido) */
                [data-testid="stAppViewContainer"] {{
                    background-color: #C0C0C0 !important; /* Cinza mais forte */
                }}
                
                /* 2. CORREÇÃO DO BODY (Removendo Zoom que quebra sidebar) */
                body {{ 
                    overflow: auto !important; 
                    /* zoom: 1.0 !important; Garantir zoom normal */
                }}
                
                #MainMenu, footer, header {{ display: none !important; }}
                .block-container {{ padding-top: 1.5rem !important; max-width: 100%; }}
                
                /* 3. FORÇAR A SIDEBAR A APARECER (CSS "Nuclear") */
                section[data-testid="stSidebar"] {{ 
                    background-color: #D3D3D3 !important; /* Cinza Sidebar */
                    display: block !important;
                    visibility: visible !important;
                    width: 300px !important;
                    z-index: 99999 !important; /* Força ficar por cima de tudo */
                    position: fixed !important; /* Força posição fixa na esquerda */
                    left: 0 !important;
                    top: 0 !important;
                    height: 100vh !important;
                }}

                /* Ajusta o conteúdo principal para não ficar "embaixo" da sidebar fixa */
                [data-testid="stSidebar"] + section {{
                    margin-left: 300px !important; 
                }}
                
                /* Estilo do Avatar */
                .avatar-circle {{
                    width: 70px; height: 70px; background-color: #FF8C00; color: white;
                    border-radius: 50%; text-align: center; line-height: 70px; font-size: 28px;
                    font-weight: bold; margin: 20px auto 10px auto; border: 3px solid white;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}

                /* Cards dos Formulários */
                [data-testid="stForm"] {{ 
                    background-color: #FFFFFF; 
                    border-radius: 15px; 
                    border: 1px solid #999; 
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15); 
                }}
                
                .stTextInput, .stSelectbox, .stNumberInput {{ margin-bottom: -15px !important; }}
                .stButton button {{ border-radius: 8px; font-weight: bold; }}
            </style>
        """, unsafe_allow_html=True)

        # --- SIDEBAR (Conteúdo) ---
        # Usamos st.sidebar normalmente, mas o CSS acima garante a posição
        with st.sidebar:
            st.markdown(f"<div class='avatar-circle'>{inicial}</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;'>{nome_display}</h3>", unsafe_allow_html=True)
            st.write("---")
            
            # Botões
            if st.button("🏠 Dashboard", key="btn_d", use_container_width=True): 
                st.session_state['admin_aba'] = 'Dashboard'; st.rerun()
            if st.button("👥 Usuários", key="btn_u", use_container_width=True): 
                st.session_state['admin_aba'] = 'Usuarios'; st.rerun()
            if st.button("🚗 Veículos", key="btn_v", use_container_width=True): 
                st.session_state['admin_aba'] = 'Veiculos'; st.rerun()
            
            st.markdown("<div style='height: 35vh;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Sair", key="btn_s", type="primary", use_container_width=True):
                st.session_state.clear() 
                st.rerun()

        # --- ROTEAMENTO ---
        aba = st.session_state['admin_aba']
        if aba == 'Usuarios':
            AdminView.render_usuarios()
        elif aba == 'Veiculos':
            AdminView.render_veiculos()
        else:
            st.markdown("### 🏠 Dashboard")
            st.info("Área de Dashboard - Em desenvolvimento")

    @staticmethod
    def render_usuarios():
        st.markdown("### 👥 Gestão de Usuários")
        col_lista, col_form = st.columns([2, 1.2])

        with col_lista:
            conn = DatabaseService.get_connection()
            try:
                df = pd.read_sql_query("SELECT id, nome, email, perfil FROM usuarios ORDER BY id DESC", conn)
                
                # Cabeçalho da tabela
                h1, h2, h3, h4 = st.columns([0.5, 2, 2, 1.2])
                h1.caption("**ID**"); h2.caption("**Nome**"); h3.caption("**E-mail**"); h4.caption("**Ações**")
                st.markdown("---")

                for _, row in df.iterrows():
                    c1, c2, c3, c4 = st.columns([0.5, 2, 2, 1.2])
                    c1.write(f"#{row['id']}")
                    c2.write(row['nome'])
                    c3.write(row['email'])
                    
                    b1, b2 = c4.columns(2)
                    if b1.button("✏️", key=f"be_{row['id']}"):
                        st.session_state['user_to_edit'] = row.to_dict()
                        st.rerun() 
                    if b2.button("🗑️", key=f"bd_{row['id']}"):
                        AdminView.excluir_usuario(row['id'])
                        st.rerun()
                    st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro: {e}")
            finally:
                conn.close()

        with col_form:
            user_data = st.session_state['user_to_edit']
            is_editing = user_data is not None
            
            default_nome = user_data['nome'] if is_editing else ""
            default_email = user_data['email'] if is_editing else ""
            default_perfil = user_data['perfil'] if is_editing else "PESQUISADOR"
            
            titulo = "📝 Editar" if is_editing else "➕ Novo"
            
            with st.form("form_users", clear_on_submit=not is_editing):
                st.markdown(f"#### {titulo}")
                nn = st.text_input("Nome:", value=default_nome)
                ne = st.text_input("E-mail:", value=default_email)
                ns = st.text_input("Senha:", type="password", placeholder="Nova senha" if is_editing else "Senha")
                
                l_perfis = ["ADMIN", "GERENTE", "COORDENADOR", "LOJISTA", "PESQUISADOR"]
                idx_p = l_perfis.index(default_perfil) if default_perfil in l_perfis else 4
                np = st.selectbox("Perfil:", options=l_perfis, index=idx_p)

                st.markdown("<br>", unsafe_allow_html=True)
                
                if is_editing:
                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("Salvar", type="primary", use_container_width=True):
                        AdminView.atualizar_usuario(user_data['id'], nn, ne, ns, np)
                        st.session_state['user_to_edit'] = None 
                        st.success("Ok!"); time.sleep(0.5); st.rerun()
                    if c2.form_submit_button("Voltar", use_container_width=True):
                        st.session_state['user_to_edit'] = None; st.rerun()
                else:
                    if st.form_submit_button("Cadastrar", type="primary", use_container_width=True):
                        if nn and ne and ns:
                            AdminView.salvar_usuario(nn, ne, ns, np)
                            st.success("Criado!"); time.sleep(0.5); st.rerun()
                        else:
                            st.error("Preencha tudo.")

    @staticmethod
    def render_veiculos():
        st.markdown("### 🚗 Gestão de Veículos")
        col_list, col_form = st.columns([1.8, 1])
        conn = DatabaseService.get_connection()
        try:
            with col_list:
                df = pd.read_sql_query("SELECT id, marca, modelo, versao, ano, preco_referencia FROM veiculos ORDER BY id DESC", conn)
                st.dataframe(df, use_container_width=True, hide_index=True)
            with col_form:
                with st.form("fv", clear_on_submit=True):
                    st.markdown("#### Adicionar")
                    ma = st.text_input("Marca"); mo = st.text_input("Modelo"); ve = st.text_input("Versão")
                    an = st.number_input("Ano", value=2024); pr = st.number_input("Preço")
                    if st.form_submit_button("Salvar", use_container_width=True):
                        conn.execute("INSERT INTO veiculos (marca, modelo, versao, ano, preco_referencia) VALUES (?,?,?,?,?)", (ma,mo,ve,an,pr))
                        conn.commit(); st.rerun()
        except Exception as e: st.error(str(e))
        finally: conn.close()

    @staticmethod
    def salvar_usuario(n, e, s, p):
        h = hashlib.sha256(s.encode()).hexdigest()
        conn = DatabaseService.get_connection()
        conn.execute("INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES (?,?,?,?)", (n,e,h,p))
        conn.commit(); conn.close()

    @staticmethod
    def atualizar_usuario(id_u, n, e, s, p):
        conn = DatabaseService.get_connection()
        if s: 
            h = hashlib.sha256(s.encode()).hexdigest()
            conn.execute("UPDATE usuarios SET nome=?, email=?, senha_hash=?, perfil=? WHERE id=?", (n,e,h,p,id_u))
        else: 
            conn.execute("UPDATE usuarios SET nome=?, email=?, perfil=? WHERE id=?", (n,e,p,id_u))
        conn.commit(); conn.close()

    @staticmethod
    def excluir_usuario(id_u):
        conn = DatabaseService.get_connection()
        conn.execute("DELETE FROM usuarios WHERE id=?", (id_u,))
        conn.commit(); conn.close()
