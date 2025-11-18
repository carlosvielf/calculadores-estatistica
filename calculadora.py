import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Calculadora Estatística",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Calculadora Estatística")
st.markdown("---")

# Criar abas principais
aba1, aba2, aba3 = st.tabs(["📈 Intervalo de Confiança para Média", "🔬 Testes de Hipótese para uma Média", "📊 Testes de Hipótese para Proporção"])

# ===============================
# ABA 1: INTERVALO DE CONFIANÇA
# ===============================
with aba1:
    st.header("Cálculo de Intervalo de Confiança")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Entrada de Dados")
        
        media_amostra = st.number_input(
            "Média da Amostra (x̄)",
            value=5.8,
            format="%.6f",
            help="Média calculada da sua amostra"
        )
        
        desvio_padrao = st.number_input(
            "Desvio Padrão (s)",
            value=5.0,
            min_value=0.0001,
            format="%.6f",
            help="Desvio padrão da amostra"
        )
        
        tamanho_amostra = st.number_input(
            "Tamanho da Amostra (n)",
            value=30,
            min_value=2,
            step=1,
            help="Número de observações na amostra"
        )
        
        nivel_confianca_input = st.number_input(
            "Nível de Confiança",
            value=98.0,
            min_value=0.01,
            max_value=99.99,
            step=0.01,
            format="%.2f",
            help="Probabilidade de o intervalo conter o verdadeiro parâmetro (entre 0.01 e 99.99)"
        )
        
        st.caption("Insira o valor como número decimal (ex: 95 para 95%, 98 para 98%)")
        
        calcular_ic = st.button("🔢 Calcular Intervalo", type="primary")
    
    with col2:
        if calcular_ic or 'ic_calculado' in st.session_state:
            st.session_state['ic_calculado'] = True
            
            try:
                # Converter para porcentagem se necessário
                if nivel_confianca_input <= 1:
                    nivel_confianca = nivel_confianca_input * 100
                else:
                    nivel_confianca = nivel_confianca_input
                
                # Validação do nível de confiança
                if nivel_confianca <= 0 or nivel_confianca >= 100:
                    st.error("❌ O nível de confiança deve estar entre 0.01 e 99.99")
                else:
                    # Cálculo do intervalo de confiança
                    alpha = 1 - (nivel_confianca / 100)
                    graus_liberdade = int(tamanho_amostra - 1)
                    
                    # Usar distribuição t de Student
                    t_critico = stats.t.ppf(1 - alpha/2, graus_liberdade)
                    
                    # Erro padrão
                    erro_padrao = desvio_padrao / np.sqrt(tamanho_amostra)
                    
                    # Margem de erro
                    margem_erro = t_critico * erro_padrao
                    
                    # Limites do intervalo
                    limite_inferior = media_amostra - margem_erro
                    limite_superior = media_amostra + margem_erro
                    
                    # Exibir resultados
                    st.subheader("📊 Resultados")
                    
                    # Métricas em destaque
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Limite Inferior", f"{limite_inferior:.5f}")
                    
                    with col_b:
                        st.metric("Média", f"{media_amostra:.4f}")
                    
                    with col_c:
                        st.metric("Limite Superior", f"{limite_superior:.5f}")
                    
                    st.markdown("---")
                    
                    # Informações detalhadas
                    st.markdown(f"""
                    ### 📋 Detalhes do Cálculo
                    
                    - **Nível de Confiança:** {nivel_confianca:.2f}%
                    - **Valor Crítico (t):** {t_critico:.5f}
                    - **Graus de Liberdade:** {graus_liberdade}
                    - **Erro Padrão:** {erro_padrao:.5f}
                    - **Margem de Erro:** {margem_erro:.5f}
                    - **Alpha (α):** {alpha:.5f}
                    
                    ### 🎯 Interpretação
                    
                    Com {nivel_confianca:.2f}% de confiança, podemos afirmar que a **verdadeira média populacional** 
                    está entre **{limite_inferior:.5f}** e **{limite_superior:.5f}**.
                    
                    Isso significa que, se repetíssemos este estudo 100 vezes, em aproximadamente 
                    {int(nivel_confianca)} dessas vezes o intervalo calculado conteria a verdadeira média populacional.
                    
                    ### 📊 Fórmula Utilizada
                    
                    **IC = x̄ ± t × (s / √n)**
                    
                    Onde:
                    - x̄ = {media_amostra} (média da amostra)
                    - t = {t_critico:.5f} (valor crítico t de Student)
                    - s = {desvio_padrao} (desvio padrão)
                    - n = {tamanho_amostra} (tamanho da amostra)
                    - Erro Padrão = s / √n = {desvio_padrao} / √{tamanho_amostra} = {erro_padrao:.5f}
                    """)
                    
                    # Gráfico de visualização do intervalo
                    st.markdown("---")
                    st.subheader("📈 Visualização do Intervalo")
                    
                    fig, ax = plt.subplots(figsize=(12, 5))
                    
                    # Criar distribuição t
                    x = np.linspace(media_amostra - 4*erro_padrao, media_amostra + 4*erro_padrao, 1000)
                    y = stats.t.pdf((x - media_amostra) / erro_padrao, graus_liberdade) / erro_padrao
                    
                    # Plotar distribuição
                    ax.plot(x, y, 'b-', linewidth=2, label='Distribuição t')
                    
                    # Destacar intervalo de confiança
                    x_ic = x[(x >= limite_inferior) & (x <= limite_superior)]
                    y_ic = stats.t.pdf((x_ic - media_amostra) / erro_padrao, graus_liberdade) / erro_padrao
                    ax.fill_between(x_ic, y_ic, alpha=0.3, color='green', label=f'IC {nivel_confianca:.2f}%')
                    
                    # Linhas verticais
                    ax.axvline(media_amostra, color='red', linestyle='-', linewidth=2, label=f'Média: {media_amostra:.4f}')
                    ax.axvline(limite_inferior, color='orange', linestyle='--', linewidth=2, label=f'Limite Inferior: {limite_inferior:.4f}')
                    ax.axvline(limite_superior, color='orange', linestyle='--', linewidth=2, label=f'Limite Superior: {limite_superior:.4f}')
                    
                    ax.set_xlabel('Valores', fontsize=12)
                    ax.set_ylabel('Densidade de Probabilidade', fontsize=12)
                    ax.set_title(f'Intervalo de Confiança de {nivel_confianca:.2f}%', fontsize=14, fontweight='bold')
                    ax.legend(loc='upper right', fontsize=9)
                    ax.grid(True, alpha=0.3)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    
                    st.pyplot(fig)
                    plt.close()
                    
            except Exception as e:
                st.error(f"❌ Erro no cálculo: {str(e)}")

# ===============================
# ABA 2: TESTES DE HIPÓTESE PARA MÉDIA
# ===============================
with aba2:
    st.header("Testes de Hipótese para Média")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configuração do Teste")
        
        tipo_teste = st.radio(
            "Tipo de Teste",
            options=["Z-test", "T-test"],
            help="Z-test: população grande ou σ conhecido | T-test: amostra pequena"
        )
        
        tipo_cauda = st.radio(
            "Tipo de Cauda",
            options=["Bicaudal", "Unicaudal Esquerda", "Unicaudal Direita"],
            help="Bicaudal: µ ≠ µ₀ | Esquerda: µ < µ₀ | Direita: µ > µ₀"
        )
        
        st.markdown("---")
        st.subheader("Dados do Teste")
        
        media_h0 = st.number_input(
            "Média Hipotética (H₀)",
            value=100.0,
            format="%.4f",
            help="Valor da média sob a hipótese nula"
        )
        
        media_amostra_teste = st.number_input(
            "Média da Amostra (x̄)",
            value=105.0,
            format="%.4f",
            help="Média observada na amostra",
            key="media_teste"
        )
        
        desvio_padrao_teste = st.number_input(
            "Desvio Padrão (s ou σ)",
            value=15.0,
            min_value=0.0001,
            format="%.4f",
            help="Desvio padrão da amostra ou populacional",
            key="desvio_teste"
        )
        
        tamanho_amostra_teste = st.number_input(
            "Tamanho da Amostra (n)",
            value=30,
            min_value=2,
            step=1,
            help="Número de observações",
            key="n_teste"
        )
        
        alpha_teste = st.number_input(
            "Nível de Significância (α)",
            value=0.05,
            min_value=0.0001,
            max_value=0.9999,
            step=0.01,
            format="%.4f",
            help="Probabilidade de erro tipo I (ex: 0.05 para 5%)"
        )
        
        executar_teste = st.button("🧪 Executar Teste", type="primary")
    
    with col2:
        if executar_teste or 'teste_executado' in st.session_state:
            st.session_state['teste_executado'] = True
            
            try:
                # Validação do alpha
                if alpha_teste <= 0 or alpha_teste >= 1:
                    st.error("❌ O nível de significância (α) deve estar entre 0.0001 e 0.9999")
                else:
                    # Cálculo da estatística do teste
                    erro_padrao_teste = desvio_padrao_teste / np.sqrt(tamanho_amostra_teste)
                    estatistica = (media_amostra_teste - media_h0) / erro_padrao_teste
                    
                    # Cálculo do p-valor baseado no tipo de teste e cauda
                    if tipo_teste == "Z-test":
                        if tipo_cauda == "Bicaudal":
                            p_valor = 2 * (1 - stats.norm.cdf(abs(estatistica)))
                            valor_critico_neg = stats.norm.ppf(alpha_teste/2)
                            valor_critico_pos = stats.norm.ppf(1 - alpha_teste/2)
                        elif tipo_cauda == "Unicaudal Esquerda":
                            p_valor = stats.norm.cdf(estatistica)
                            valor_critico = stats.norm.ppf(alpha_teste)
                        else:  # Unicaudal Direita
                            p_valor = 1 - stats.norm.cdf(estatistica)
                            valor_critico = stats.norm.ppf(1 - alpha_teste)
                        
                        distribuicao = "Normal Padrão"
                        
                    else:  # T-test
                        gl = tamanho_amostra_teste - 1
                        if tipo_cauda == "Bicaudal":
                            p_valor = 2 * (1 - stats.t.cdf(abs(estatistica), gl))
                            valor_critico_neg = stats.t.ppf(alpha_teste/2, gl)
                            valor_critico_pos = stats.t.ppf(1 - alpha_teste/2, gl)
                        elif tipo_cauda == "Unicaudal Esquerda":
                            p_valor = stats.t.cdf(estatistica, gl)
                            valor_critico = stats.t.ppf(alpha_teste, gl)
                        else:  # Unicaudal Direita
                            p_valor = 1 - stats.t.cdf(estatistica, gl)
                            valor_critico = stats.t.ppf(1 - alpha_teste, gl)
                        
                        distribuicao = f"T-Student (gl={gl})"
                    
                    # Decisão estatística
                    rejeita_h0 = p_valor < alpha_teste
                    
                    # Exibir resultados
                    st.subheader("📊 Resultados do Teste")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric(
                            "Estatística do Teste",
                            f"{estatistica:.4f}",
                            help="Z-score ou T-score calculado"
                        )
                    
                    with col_b:
                        st.metric(
                            "P-valor",
                            f"{p_valor:.6f}",
                            delta="Significativo" if rejeita_h0 else "Não Significativo",
                            delta_color="inverse" if rejeita_h0 else "off"
                        )
                    
                    with col_c:
                        st.metric(
                            "Nível α",
                            f"{alpha_teste:.4f}",
                            help="Nível de significância escolhido"
                        )
                    
                    st.markdown("---")
                    
                    # Decisão e interpretação
                    if rejeita_h0:
                        decisao_cor = "🔴"
                        decisao_texto = "REJEITAR H₀"
                        interpretacao = f"""
                        Como o **p-valor ({p_valor:.6f})** é **menor** que o nível de significância **α = {alpha_teste}**, 
                        **rejeitamos a hipótese nula (H₀)**.
                        
                        ### 📌 Conclusão:
                        Há **evidências estatísticas significativas** para afirmar que a média populacional 
                        **é diferente de {media_h0}** (no caso bicaudal) ou segue a direção especificada 
                        (unicaudal), ao nível de {int((1-alpha_teste)*100)}% de confiança.
                        
                        A diferença observada (x̄ = {media_amostra_teste}) em relação a H₀ ({media_h0}) 
                        **não pode ser atribuída apenas ao acaso**.
                        """
                    else:
                        decisao_cor = "🟢"
                        decisao_texto = "NÃO REJEITAR H₀"
                        interpretacao = f"""
                        Como o **p-valor ({p_valor:.6f})** é **maior ou igual** ao nível de significância **α = {alpha_teste}**, 
                        **não rejeitamos a hipótese nula (H₀)**.
                        
                        ### 📌 Conclusão:
                        **Não há evidências estatísticas suficientes** para afirmar que a média populacional 
                        seja diferente de {media_h0} (ou segue a direção especificada no teste unicaudal).
                        
                        A diferença observada (x̄ = {media_amostra_teste}) em relação a H₀ ({media_h0}) 
                        **pode ser atribuída à variação amostral aleatória**.
                        """
                    
                    st.success(f"### {decisao_cor} Decisão: **{decisao_texto}**")
                    st.markdown(interpretacao)
                    
                    # Gráfico da distribuição
                    st.markdown("---")
                    st.subheader("📈 Visualização da Distribuição")
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    # Criar valores para o eixo x
                    if tipo_teste == "Z-test":
                        x = np.linspace(-4, 4, 1000)
                        y = stats.norm.pdf(x)
                    else:
                        x = np.linspace(-4, 4, 1000)
                        y = stats.t.pdf(x, tamanho_amostra_teste - 1)
                    
                    # Plotar curva
                    ax.plot(x, y, 'b-', linewidth=2, label=distribuicao)
                    
                    # Pintar região de rejeição
                    if tipo_cauda == "Bicaudal":
                        # Região esquerda
                        x_rej_esq = x[x <= valor_critico_neg]
                        y_rej_esq = y[:len(x_rej_esq)]
                        ax.fill_between(x_rej_esq, y_rej_esq, alpha=0.3, color='red', label='Região de Rejeição')
                        
                        # Região direita
                        x_rej_dir = x[x >= valor_critico_pos]
                        y_rej_dir = y[len(y)-len(x_rej_dir):]
                        ax.fill_between(x_rej_dir, y_rej_dir, alpha=0.3, color='red')
                        
                        # Linhas críticas
                        ax.axvline(valor_critico_neg, color='orange', linestyle='--', linewidth=2, label=f'Valores Críticos: ±{abs(valor_critico_pos):.3f}')
                        ax.axvline(valor_critico_pos, color='orange', linestyle='--', linewidth=2)
                        
                    elif tipo_cauda == "Unicaudal Esquerda":
                        x_rej = x[x <= valor_critico]
                        y_rej = y[:len(x_rej)]
                        ax.fill_between(x_rej, y_rej, alpha=0.3, color='red', label='Região de Rejeição')
                        ax.axvline(valor_critico, color='orange', linestyle='--', linewidth=2, label=f'Valor Crítico: {valor_critico:.3f}')
                        
                    else:  # Unicaudal Direita
                        x_rej = x[x >= valor_critico]
                        y_rej = y[len(y)-len(x_rej):]
                        ax.fill_between(x_rej, y_rej, alpha=0.3, color='red', label='Região de Rejeição')
                        ax.axvline(valor_critico, color='orange', linestyle='--', linewidth=2, label=f'Valor Crítico: {valor_critico:.3f}')
                    
                    # Linha da estatística observada
                    ax.axvline(estatistica, color='green', linestyle='-', linewidth=3, label=f'Estatística Observada: {estatistica:.3f}')
                    
                    # Configurações do gráfico
                    ax.set_xlabel('Valores da Estatística do Teste', fontsize=12)
                    ax.set_ylabel('Densidade de Probabilidade', fontsize=12)
                    ax.set_title(f'Distribuição {distribuicao} - Teste {tipo_cauda}', fontsize=14, fontweight='bold')
                    ax.legend(loc='upper right', fontsize=10)
                    ax.grid(True, alpha=0.3)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    
                    st.pyplot(fig)
                    plt.close()
                    
                    # Tabela de resumo
                    st.markdown("---")
                    st.subheader("📋 Resumo do Teste")
                    
                    resumo = pd.DataFrame({
                        'Parâmetro': [
                            'Tipo de Teste',
                            'Tipo de Cauda',
                            'Hipótese Nula (H₀)',
                            'Média da Amostra (x̄)',
                            'Desvio Padrão',
                            'Tamanho da Amostra (n)',
                            'Estatística do Teste',
                            'P-valor',
                            'Nível de Significância (α)',
                            'Decisão'
                        ],
                        'Valor': [
                            tipo_teste,
                            tipo_cauda,
                            f'µ = {media_h0}',
                            f'{media_amostra_teste:.4f}',
                            f'{desvio_padrao_teste:.4f}',
                            tamanho_amostra_teste,
                            f'{estatistica:.4f}',
                            f'{p_valor:.6f}',
                            alpha_teste,
                            decisao_texto
                        ]
                    })
                    
                    st.dataframe(resumo, hide_index=True, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Erro no cálculo: {str(e)}")
                st.info("Verifique se todos os valores inseridos são válidos.")

# ===============================
# ABA 3: TESTE DE HIPÓTESE PARA PROPORÇÃO (Z-TEST)
# ===============================
with aba3:

    st.title("Calculadora de Proporção com Z-Test para Proporção")
    st.write("Esta ferramenta calcula a proporção, o valor-z e o valor-p para testes de proporção.")

    # Parâmetros de entrada
    st.header("Parâmetros do Teste")
    n = st.number_input("Tamanho da amostra (n):", min_value=1, step=1)
    successes = st.number_input("Número de sucessos (x):", min_value=0, step=1)
    null_proportion = st.number_input("Proporção nula (p₀):", min_value=0.0, max_value=1.0, step=0.01)

    if st.button("Calcular"):
        if successes > n:
            st.error("Erro: O número de sucessos não pode ser maior que o tamanho da amostra.")
        else:
            # Cálculos
            sample_proportion = successes / n
            standard_error = np.sqrt((null_proportion * (1 - null_proportion)) / n)
            z_value = (sample_proportion - null_proportion) / standard_error
            p_value = 2 * (1 - stats.norm.cdf(abs(z_value)))  # Teste bilateral

            # Resultados
            st.subheader("Resultados")
            st.write(f"**Proporção amostral (p̂):** {sample_proportion:.4f}")
            st.write(f"**Erro padrão (EP):** {standard_error:.4f}")
            st.write(f"**Estatística Z:** {z_value:.4f}")
            st.write(f"**Valor-p:** {p_value:.4f}")

            # Gráfico
            st.subheader("Distribuição do Teste Z")

            fig, ax = plt.subplots(figsize=(10, 5))

            # Distribuição normal padrão
            x = np.linspace(-4, 4, 500)
            y = stats.norm.pdf(x)

            ax.plot(x, y, label="Distribuição Normal Padrão")

            # Linha do valor-z
            ax.axvline(z_value, color='r', linestyle='--', label=f"Z calculado = {z_value:.4f}")

            ax.set_title("Distribuição Normal Padrão com Estatística Z")
            ax.set_xlabel("Valor Z")
            ax.set_ylabel("Densidade")
            ax.legend()

            st.pyplot(fig)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>📊 Calculadora Estatística | Desenvolvida com Streamlit</p>
    <p style='font-size: 0.8em;'>Utilize esta ferramenta para análises estatísticas de intervalos de confiança e testes de hipótese</p>
</div>
""", unsafe_allow_html=True)