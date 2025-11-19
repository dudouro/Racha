import streamlit as st
import pandas as pd
import os

# --- Configurações da Página ---
st.set_page_config(
    page_title="Racha de Futebol App",
    page_icon="⚽",
    layout="wide"
)

# --- Funções Auxiliares ---
def carregar_dados():
    """Carrega os dados dos jogadores do arquivo CSV."""
    if os.path.exists('jogadores.csv'):
        return pd.read_csv('jogadores.csv')
    else:
        return pd.DataFrame(columns=['Nome', 'Vulgo', 'Foto'])

# --- Página Principal (Home) ---
st.title("Bem-vindo ao Gerenciador de Racha de Futebol! ⚽")
st.markdown("---")

st.header("Visão Geral do Racha")

jogadores_df = carregar_dados()

if jogadores_df.empty:
    st.info("Ainda não há jogadores cadastrados. Vá para a página de **Cadastro de Jogadores** para começar.")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total de Jogadores Cadastrados", value=len(jogadores_df))
        st.write("### Últimos Jogadores Cadastrados:")
        st.dataframe(jogadores_df[['Nome', 'Vulgo']].tail(), use_container_width=True)

    with col2:
        st.write("### Próximos Passos:")
        st.markdown("""
            - **Cadastro de Jogadores:** Adicione novos atletas ao seu time.
            - **Lista do Racha (Check-in):** Confirme quem vai jogar hoje.
            - **Sorteio de Times:** Deixe a sorte decidir as equipes.
            - E muito mais!
        """)

st.markdown("---")
st.sidebar.success("Selecione uma das páginas acima para começar.")