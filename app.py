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
    colunas = ['Nome', 'Vulgo', 'Foto', 'Partidas Jogadas', 'Vitorias', 'Gols']
    if os.path.exists('jogadores.csv'):
        return pd.read_csv('jogadores.csv')
    else:
        # Retorna um DataFrame vazio com as colunas corretas se o arquivo não existir
        return pd.DataFrame(columns=colunas)

# --- Página Principal (Home) ---
st.title("Bem-vindo ao Gerenciador de Racha de Futebol! ⚽")
st.markdown("---")

jogadores_df = carregar_dados()

if jogadores_df.empty:
    st.info("Ainda não há jogadores cadastrados. Vá para a página de **Cadastro de Jogadores** para começar.")
else:
    col1, col2 = st.columns([2, 1]) # Dando mais espaço para a tabela
    with col1:
        st.header("🏆 Ranking de Jogadores")

        # --- Cálculo do Aproveitamento ---
        # Evita divisão por zero se o jogador ainda não jogou
        jogadores_df['Aproveitamento (%)'] = jogadores_df.apply(
            lambda row: (row['Vitorias'] / row['Partidas Jogadas']) * 100 if row['Partidas Jogadas'] > 0 else 0,
            axis=1
        )
        
        # Ordena o DataFrame pelo aproveitamento
        ranking_df = jogadores_df.sort_values(by='Aproveitamento (%)', ascending=False)
        
        # Seleciona e renomeia colunas para exibição
        colunas_ranking = {
            'Nome': 'Nome',
            'Partidas Jogadas': 'Partidas',
            'Vitorias': 'Vitórias',
            'Gols': 'Gols',
            'Aproveitamento (%)': 'Aproveitamento (%)'
        }
        
        # Exibe o ranking formatado
        st.dataframe(
            ranking_df[colunas_ranking.keys()].rename(columns=colunas_ranking),
            use_container_width=True,
            # Formatação visual das colunas
            column_config={
                "Aproveitamento (%)": st.column_config.ProgressColumn(
                    "Aproveitamento (%)",
                    format="%.2f%%",
                    min_value=0,
                    max_value=100,
                ),
            },
            hide_index=True
        )

    with col2:
        st.metric(label="Total de Jogadores", value=len(jogadores_df))
        st.metric(label="Total de Gols Marcados", value=jogadores_df['Gols'].sum())
        
        st.markdown("---")

        st.header("Próximos Passos")
        st.markdown("""
            - **Cadastro de Jogadores:** Adicione novos atletas.
            - **Nova Partida:** Inicie um racha e sorteie os times.
            - **Registrar Jogo:** (Em breve) Lance os resultados para atualizar o ranking!
        """)

st.sidebar.success("Selecione uma das páginas acima para começar.")