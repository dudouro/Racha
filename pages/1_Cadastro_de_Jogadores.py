import streamlit as st
import pandas as pd
import os
from PIL import Image

# --- Configurações da Página ---
st.set_page_config(
    page_title="Cadastro de Jogadores",
    page_icon="📝",
    layout="centered"
)

# --- Funções ---
def salvar_dados(df):
    """Salva o DataFrame em um arquivo CSV."""
    df.to_csv('jogadores.csv', index=False)

def carregar_dados():
    """Carrega os dados dos jogadores do arquivo CSV."""
    colunas = ['Nome', 'Vulgo', 'Foto', 'Partidas Jogadas', 'Vitorias', 'Gols']
    if os.path.exists('jogadores.csv'):
        return pd.read_csv('jogadores.csv')
    else:
        return pd.DataFrame(columns=colunas)

def salvar_foto(foto_carregada, nome_jogador):
    """Salva a foto do jogador em uma pasta local."""
    if foto_carregada is not None:
        if not os.path.exists('fotos_jogadores'):
            os.makedirs('fotos_jogadores')
        
        nome_arquivo = f"fotos_jogadores/{nome_jogador.replace(' ', '_').lower()}.png"
        
        imagem = Image.open(foto_carregada)
        imagem.save(nome_arquivo, "PNG")
        return nome_arquivo
    return "sem_foto.png" # Retorna um placeholder se não houver foto

# --- Interface da Página ---
st.title("📝 Cadastro de Jogadores")

jogadores_df = carregar_dados()

with st.form("cadastro_jogador_form", clear_on_submit=True):
    st.subheader("Novo Jogador")
    nome = st.text_input("Nome Completo do Jogador", placeholder="Ex: Lionel Messi")
    vulgo = st.text_input("Vulgo (Apelido)", placeholder="Ex: La Pulga")
    foto = st.file_uploader("Foto do Jogador", type=['png', 'jpg', 'jpeg'])
    
    submit_button = st.form_submit_button("Cadastrar Jogador")

    if submit_button:
        if nome:
            # Verifica se o jogador já existe
            if nome not in jogadores_df['Nome'].values:
                caminho_foto = salvar_foto(foto, nome)
                
                novo_jogador = pd.DataFrame([{
                    'Nome': nome, 
                    'Vulgo': vulgo,
                    'Foto': caminho_foto,
                    'Partidas Jogadas': 0, # Estatística inicial
                    'Vitorias': 0,         # Estatística inicial
                    'Gols': 0              # Estatística inicial
                }])
                
                jogadores_df = pd.concat([jogadores_df, novo_jogador], ignore_index=True)
                salvar_dados(jogadores_df)
                st.success(f"Jogador **{nome}** cadastrado com sucesso!")
            else:
                st.warning(f"O jogador **{nome}** já está cadastrado.")
        else:
            st.error("O campo 'Nome' é obrigatório.")

st.markdown("---")

st.header("Jogadores Cadastrados")
if not jogadores_df.empty:
    # Exibe apenas as colunas principais no cadastro
    st.dataframe(jogadores_df[['Nome', 'Vulgo']], use_container_width=True)
else:
    st.info("Nenhum jogador cadastrado até o momento.")