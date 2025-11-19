import streamlit as st
import pandas as pd
import os
import random
from datetime import date

# --- Configurações da Página ---
st.set_page_config(
    page_title="Nova Partida e Sorteio",
    page_icon="📅",
    layout="wide"
)

# --- Funções Auxiliares ---
@st.cache_data
def carregar_jogadores():
    """Carrega os dados dos jogadores do arquivo CSV para seleção."""
    if os.path.exists('jogadores.csv'):
        return pd.read_csv('jogadores.csv')
    else:
        return pd.DataFrame(columns=['Nome', 'Vulgo', 'Foto'])

# --- Inicialização do Session State ---
# Usamos o session_state para manter os dados durante a interação do usuário na página
if 'times_sorteados' not in st.session_state:
    st.session_state.times_sorteados = None
if 'jogadores_partida' not in st.session_state:
    st.session_state.jogadores_partida = []
if 'times_confirmados' not in st.session_state:
    st.session_state.times_confirmados = False


# --- Interface da Página ---
st.title("📅 Registrar Nova Partida")

jogadores_df = carregar_jogadores()

if jogadores_df.empty:
    st.warning("Nenhum jogador cadastrado. Por favor, cadastre jogadores primeiro na página 'Cadastro de Jogadores'.")
else:
    # --- Seção 1: Seleção de Jogadores e Data ---
    with st.expander("Passo 1: Selecione os Jogadores e a Data", expanded=True):
        
        data_partida = st.date_input("Data da Partida", value=date.today())
        
        lista_nomes = jogadores_df['Nome'].tolist()
        jogadores_selecionados = st.multiselect(
            "Selecione os jogadores para a partida de hoje:",
            options=lista_nomes,
            default=st.session_state.jogadores_partida, # Mantém a seleção
            help="Clique no campo para ver a lista de jogadores cadastrados."
        )
        
        # Atualiza a lista de jogadores no session_state
        if jogadores_selecionados:
            st.session_state.jogadores_partida = jogadores_selecionados

    st.markdown("---")

    # --- Seção 2: Sorteio dos Times ---
    if len(st.session_state.jogadores_partida) > 1:
        st.header("⚡ Sorteio dos Times")

        num_times = st.number_input(
            "Quantos times você quer formar?", 
            min_value=2, 
            max_value=len(st.session_state.jogadores_partida), 
            value=2, 
            step=1
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sortear Times Agora!", use_container_width=True, type="primary"):
                # Lógica do sorteio
                jogadores_a_sortear = list(st.session_state.jogadores_partida)
                random.shuffle(jogadores_a_sortear)
                
                times = [[] for _ in range(num_times)]
                for i, jogador in enumerate(jogadores_a_sortear):
                    times[i % num_times].append(jogador)
                
                st.session_state.times_sorteados = times
                st.session_state.times_confirmados = False # Reseta a confirmação ao sortear de novo

        with col2:
             if st.session_state.times_sorteados and not st.session_state.times_confirmados:
                if st.button("Confirmar Times", use_container_width=True):
                    st.session_state.times_confirmados = True
                    st.rerun() # Atualiza a página para mostrar o estado "confirmado"

    st.markdown("---")

    # --- Seção 3: Exibição dos Times Sorteados ---
    if st.session_state.times_sorteados:
        if st.session_state.times_confirmados:
            st.success("✅ Times Confirmados!")
        else:
            st.info("⚠️ Times ainda não confirmados. Confirme acima ou sorteie novamente.")

        st.subheader("Composição dos Times")
        cols = st.columns(len(st.session_state.times_sorteados))
        
        for i, time in enumerate(st.session_state.times_sorteados):
            with cols[i]:
                st.markdown(f"**Time {i + 1}**")
                
                # Se os times não estiverem confirmados, permite a edição
                if st.session_state.times_confirmados == False:
                     # Usamos uma chave única para cada selectbox para que funcionem independentemente
                    jogadores_editados = st.multiselect(
                        f"Jogadores do Time {i+1}", 
                        options=st.session_state.jogadores_partida, 
                        default=time,
                        key=f"time_edit_{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.times_sorteados[i] = jogadores_editados
                else:
                    # Apenas exibe a lista se os times estiverem confirmados
                    for jogador in time:
                        st.markdown(f"- {jogador}")
        
        # Botão para permitir a edição após a confirmação
        if st.session_state.times_confirmados:
            if st.button("✏️ Editar Times Manualmente"):
                st.session_state.times_confirmados = False
                st.rerun()