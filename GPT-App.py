# Importação das bibliotecas
import openai  # Importa a biblioteca OpenAI para interagir com o modelo GPT-3
import streamlit as st  # Importa a biblioteca Streamlit para criar a interface de usuário
import os  # Importa a biblioteca OS para manipulação de sistema operacional
from streamlit_chat import message as msg  # Importa um módulo específico do pacote "streamlit_chat"
from dotenv import load_dotenv  # Importa a função load_dotenv do pacote "dotenv" para carregar variáveis de ambiente
import io  # Importa a biblioteca "io" para manipulação de entrada/saída

# Função para inicializar a sessão do usuário
def initialize_session():
    if "hst_conversa" not in st.session_state:
        st.session_state.hst_conversa = []  # Inicializa uma lista vazia para armazenar a conversa

# Função para configurar a chave de API
def setup_api_key():
    load_dotenv(override=True)  # Carrega as variáveis de ambiente a partir de um arquivo .env
    API_KEY = os.getenv("API_KEY_ChatGPT")  # Obtém a chave de API do GPT-3 do arquivo .env
    if API_KEY:
        openai.api_key = API_KEY  # Configura a chave de API do GPT-3
    else:
        st.error("Chave de API não configurada. Por favor, configure a chave no arquivo .env.")

# Função principal
def main():
    # Cria duas colunas
    col1, col2 = st.columns([1, 3])  # Defina a proporção de largura das colunas como 1:3 (ou ajuste conforme necessário)

    # Adicione um botão para limpar todas as informações da tela
    if st.button("Limpar Tela"):
        st.session_state.hst_conversa = []  # Limpa a lista de conversa
        
    # Na primeira coluna (col1), coloque a imagem
    with col1:
        st.image("img.png", width=250)

    # Na segunda coluna (col2), coloque o título
    with col2:
        st.title('Como eu posso te ajudar?')

    st.write("***")  # Escreve um separador na interface

    initialize_session()  # Chama a função para inicializar a sessão do usuário
    setup_api_key()  # Chama a função para configurar a chave de API do GPT-3
    model_name = "gpt-3.5-turbo"  # Define o nome do modelo GPT-3 a ser utilizado

    pergunta = st.text_input("Digite a pergunta:")  # Cria um campo de entrada de texto para o usuário inserir uma pergunta
    btn_enviar = st.button("Enviar pergunta")  # Cria um botão para o usuário enviar a pergunta

    if btn_enviar:
        if not openai.api_key:
            st.error("Chave de API não configurada. Por favor, configure a chave no arquivo .env.")
            return

        st.session_state.hst_conversa.append({"role": "user", "content": pergunta})  # Adiciona a pergunta à lista de conversa

        try:
            retorno_openai = openai.ChatCompletion.create(
                model=model_name,
                messages=st.session_state.hst_conversa,
                max_tokens=1000,
                n=1
            )
            st.session_state.hst_conversa.append({"role": "assistant", "content": retorno_openai['choices'][0]['message']['content']})  # Adiciona a resposta do assistente à lista de conversa
        except Exception as e:
            st.error(f"Erro ao obter resposta do assistente: {str(e)}")

    if st.button("Salvar e Baixar Conversa"):
        if len(st.session_state.hst_conversa) > 0:
            conversation_text = "\n".join(
                [f"{item['role']}: {item['content']}" for item in st.session_state.hst_conversa]
            )
            with io.StringIO() as buffer:
                buffer.write(conversation_text)
                st.download_button(
                    label="Clique para baixar a conversa",
                    data=buffer.getvalue(),
                    file_name="conversa.txt",
                    key="conversa_txt",
                )

    # Regra para mostrar a interação do cliente com o app
    if len(st.session_state.hst_conversa) > 0:
        for i in range(len(st.session_state.hst_conversa)):
            if i % 2 == 0:
                msg("Você: " + st.session_state.hst_conversa[i]['content'], is_user=True, key=f"user_msg_{i}") # Mostra a pergunta do cliente
            else:
                msg("Resposta IA: " + st.session_state.hst_conversa[i]['content'], key=f"assistant_msg_{i}") # Mostra a resposta do assistente

if __name__ == "__main__":
    main()  # Chama a função principal quando o script é executado diretamente