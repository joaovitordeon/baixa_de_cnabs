import streamlit as st
from io import StringIO


def main():
    st.set_page_config(page_title='Baixa em boletos', page_icon='❌')
    st.title("Baixa de boletos")
    st.divider()

    st.write('\n')
    arq1 = st.file_uploader("**Faça o upload do arquivo de remessa**", accept_multiple_files=False)
    
    
    st.write('\n')
    arq2 = st.file_uploader("**Faça o upload com o CPF ou n° de boleto a serem alterados**", accept_multiple_files=False)
    
    
    st.write('\n')
    seq = st.text_input("**Digite o número sequencial...**")
    
    st.write('\n')
    
    btn = st.button("Processar...")


    # iniciar logica quando o botão processar for acionado
    if btn:

        if arq1 is not None and arq2 is not None:
            # ------------------------------ dados arquivo 1 ---------------------------------------
            buf_arq1 = StringIO(arq1.getvalue().decode("utf-16"))
            header_arq1 = buf_arq1.readline()
            dados_arq1 = buf_arq1.readlines()        

            # ------------------------------ dados arquivo 2 ---------------------------------------
            buf_arq2 = StringIO(arq2.getvalue().decode("utf-8"))
            header_arq2 = buf_arq2.readline()
            dados_arq2 = buf_arq2.readlines()
            dados_arq2 = [d.strip() for d in dados_arq2]

            # --------------------------- dados de saída ------------------------------
            # mudar o numero sequencial do cabeçalho de arcordo com input
            if seq is not None:
                novo_header = header_arq1[:110] + str(seq).zfill(7) + header_arq1[117:]
            else:
                novo_header = header_arq1

            res = []
            count = 2

            # buscar por cpf
            if 'cpf' in header_arq2.lower():
                for cpf in dados_arq2:
                    for linha in dados_arq1:
                        if cpf in linha[220:236]:
                            # nova_linha = linha[:221] + cpf + linha[236:]
                            # alterar agora o código para 02 (dar baixa)
                            nova_linha = linha[:108] + '02' + linha[110:]
                            # alterar o contador no final de cada linha
                            nova_linha = nova_linha[:394] + str(count).zfill(6)

                            res.append(nova_linha)
                            
                            count+=1


            # buscar por numero do boleto
            elif 'numero' in header_arq2.lower() or 'número' in header_arq2.lower():
                for numero in dados_arq2:
                    for linha in dados_arq1:
                        if numero in linha[109:120]:
                            # nova_linha = linha[:221] + cpf + linha[236:]
                            # alterar agora o código para 02 (dar baixa)
                            nova_linha = linha[:108] + '02' + linha[110:]
                            # alterar o contador no final de cada linha
                            nova_linha = nova_linha[:394] + str(count).zfill(6)
                            res.append(nova_linha)
                            
                            count+=1
                
            
            else:
                pass

            count = 1
        

        res = [novo_header] + res

        arq_saida = ''.join(res)
        st.divider()

        st.download_button('Clique aqui para fazer o download do arquivo de saída ⬇️', arq_saida, type="primary")


if __name__ == '__main__':
    main()