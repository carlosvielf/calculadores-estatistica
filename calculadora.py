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
# ABA 3: TESTES DE HIPÓTESE PARA PROPORÇÃO
# ===============================
with aba3:
    st.markdown("""
        <style>
        .prop-header {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            color: #ffffff;
        }
        .prop-section {
            background-color: #1e1e1e;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .prop-section-title {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #ffa500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="prop-header">📊 Calculadora de Z-test para Proporção</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="prop-section">', unsafe_allow_html=True)
        st.markdown('<div class="prop-section-title">📝 Entrada de Dados</div>', unsafe_allow_html=True)
        
        proporcao_observada = st.number_input(
            "Proporção Observada (p̂):",
            value=0.5493,
            min_value=0.0,
            max_value=1.0,
            step=0.0001,
            format="%.4f",
            help="Proporção observada na amostra (entre 0 e 1)",
            key="prop_obs"
        )
        
        proporcao_h0 = st.number_input(
            "Proporção Esperada (p₀):",
            value=0.25,
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.4f",
            help="Valor da proporção sob a hipótese nula (entre 0 e 1)"
        )
        
        tamanho_amostra_prop = st.number_input(
            "Tamanho da Amostra (n):",
            value=71,
            min_value=1,
            step=1,
            help="Número total de observações",
            key="n_prop"
        )
        
        alpha_prop = st.number_input(
            "Nível de Significância (α):",
            value=0.10,
            min_value=0.0001,
            max_value=0.9999,
            step=0.01,
            format="%.3f",
            help="Probabilidade de erro tipo I (ex: 0.05 para 5%)",
            key="alpha_prop"
        )
        
        tipo_cauda_prop = st.selectbox(
            "Tipo de Teste:",
            options=["Unicaudal (esquerda)", "Unicaudal (direita)", "Bicaudal"],
            index=0,
            help="Tipo de teste de hipótese",
            key="cauda_prop"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        executar_teste_prop = st.button("🧮 Calcular", type="primary", use_container_width=True)
    
    with col2:
        if executar_teste_prop or 'teste_prop_executado' in st.session_state:
            st.session_state['teste_prop_executado'] = True
            
            try:
                # Validações
                if num_sucessos > tamanho_amostra_prop:
                    st.error("❌ O número de sucessos não pode ser maior que o tamanho da amostra!")
                elif alpha_prop <= 0 or alpha_prop >= 1:
                    st.error("❌ O nível de significância (α) deve estar entre 0.0001 e 0.9999")
                else:
                    # Calcular proporção amostral
                    proporcao_amostral = num_sucessos / tamanho_amostra_prop
                    
                    # Verificar condição de aproximação normal
                    n_p0 = tamanho_amostra_prop * proporcao_h0
                    n_q0 = tamanho_amostra_prop * (1 - proporcao_h0)
                    
                    aproximacao_valida = (n_p0 >= 5) and (n_q0 >= 5)
                    
                    if not aproximacao_valida:
                        st.warning(f"⚠️ **Atenção**: As condições para aproximação normal não são totalmente satisfeitas (np₀ = {n_p0:.2f}, nq₀ = {n_q0:.2f}). Os resultados podem não ser precisos. Recomenda-se n×p₀ ≥ 5 e n×(1-p₀) ≥ 5.")
                    
                    # Calcular erro padrão sob H₀
                    erro_padrao_prop = np.sqrt(proporcao_h0 * (1 - proporcao_h0) / tamanho_amostra_prop)
                    
                    # Calcular estatística Z
                    z_estatistica = (proporcao_amostral - proporcao_h0) / erro_padrao_prop
                    
                    # Calcular p-valor
                    if tipo_cauda_prop == "Bicaudal":
                        p_valor_prop = 2 * (1 - stats.norm.cdf(abs(z_estatistica)))
                        z_critico_neg = stats.norm.ppf(alpha_prop/2)
                        z_critico_pos = stats.norm.ppf(1 - alpha_prop/2)
                    elif tipo_cauda_prop == "Unicaudal Esquerda":
                        p_valor_prop = stats.norm.cdf(z_estatistica)
                        z_critico = stats.norm.ppf(alpha_prop)
                    else:  # Unicaudal Direita
                        p_valor_prop = 1 - stats.norm.cdf(z_estatistica)
                        z_critico = stats.norm.ppf(1 - alpha_prop)
                    
                    # Decisão estatística
                    rejeita_h0_prop = p_valor_prop < alpha_prop
                    
                    # Exibir resultados
                    st.subheader("📊 Resultados do Teste")
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        st.metric(
                            "Proporção Amostral",
                            f"{proporcao_amostral:.4f}",
                            help=f"{num_sucessos}/{tamanho_amostra_prop}"
                        )
                    
                    with col_b:
                        st.metric(
                            "Estatística Z",
                            f"{z_estatistica:.4f}",
                            help="Z-score calculado"
                        )
                    
                    with col_c:
                        st.metric(
                            "P-valor",
                            f"{p_valor_prop:.6f}",
                            delta="Significativo" if rejeita_h0_prop else "Não Significativo",
                            delta_color="inverse" if rejeita_h0_prop else "off"
                        )
                    
                    with col_d:
                        st.metric(
                            "Nível α",
                            f"{alpha_prop:.4f}",
                            help="Nível de significância"
                        )
                    
                    st.markdown("---")
                    
                    # Decisão e interpretação
                    if rejeita_h0_prop:
                        decisao_cor = "🔴"
                        decisao_texto = "REJEITAR H₀"
                        interpretacao_prop = f"""
                        Como o **p-valor ({p_valor_prop:.6f})** é **menor** que o nível de significância **α = {alpha_prop}**, 
                        **rejeitamos a hipótese nula (H₀)**.
                        
                        ### 📌 Conclusão:
                        Há **evidências estatísticas significativas** para afirmar que a proporção populacional 
                        **é diferente de {proporcao_h0:.4f}** (no caso bicaudal) ou segue a direção especificada 
                        (unicaudal), ao nível de {int((1-alpha_prop)*100)}% de confiança.
                        
                        A proporção observada (p̂ = {proporcao_amostral:.4f}) em relação a H₀ (p₀ = {proporcao_h0:.4f}) 
                        **não pode ser atribuída apenas ao acaso**.
                        """
                    else:
                        decisao_cor = "🟢"
                        decisao_texto = "NÃO REJEITAR H₀"
                        interpretacao_prop = f"""
                        Como o **p-valor ({p_valor_prop:.6f})** é **maior ou igual** ao nível de significância **α = {alpha_prop}**, 
                        **não rejeitamos a hipótese nula (H₀)**.
                        
                        ### 📌 Conclusão:
                        **Não há evidências estatísticas suficientes** para afirmar que a proporção populacional 
                        seja diferente de {proporcao_h0:.4f} (ou segue a direção especificada no teste unicaudal).
                        
                        A proporção observada (p̂ = {proporcao_amostral:.4f}) em relação a H₀ (p₀ = {proporcao_h0:.4f}) 
                        **pode ser atribuída à variação amostral aleatória**.
                        """
                    
                    st.success(f"### {decisao_cor} Decisão: **{decisao_texto}**")
                    st.markdown(interpretacao_prop)
                    
                    # Informações detalhadas
                    st.markdown("---")
                    st.markdown(f"""
                    ### 📋 Detalhes do Cálculo
                    
                    - **Proporção Hipotética (p₀):** {proporcao_h0:.4f}
                    - **Proporção Amostral (p̂):** {proporcao_amostral:.4f} = {num_sucessos}/{tamanho_amostra_prop}
                    - **Erro Padrão:** {erro_padrao_prop:.6f}
                    - **Estatística Z:** {z_estatistica:.4f}
                    - **P-valor:** {p_valor_prop:.6f}
                    - **Nível de Significância (α):** {alpha_prop}
                    - **Condição np₀:** {n_p0:.2f} {'✓' if n_p0 >= 5 else '✗'} (mínimo: 5)
                    - **Condição n(1-p₀):** {n_q0:.2f} {'✓' if n_q0 >= 5 else '✗'} (mínimo: 5)
                    
                    ### 📊 Fórmula Utilizada
                    
                    **Z = (p̂ - p₀) / √[p₀(1-p₀)/n]**
                    
                    Onde:
                    - p̂ = {proporcao_amostral:.4f} (proporção amostral)
                    - p₀ = {proporcao_h0:.4f} (proporção sob H₀)
                    - n = {tamanho_amostra_prop} (tamanho da amostra)
                    - Erro Padrão = √[p₀(1-p₀)/n] = √[{proporcao_h0}×{1-proporcao_h0}/{tamanho_amostra_prop}] = {erro_padrao_prop:.6f}
                    """)
                    
                    # Gráfico da distribuição
                    st.markdown("---")
                    st.subheader("📈 Visualização da Distribuição Normal")
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    # Criar valores para o eixo x
                    x = np.linspace(-4, 4, 1000)
                    y = stats.norm.pdf(x)
                    
                    # Plotar curva normal
                    ax.plot(x, y, 'b-', linewidth=2, label='Distribuição Normal Padrão')
                    
                    # Pintar região de rejeição
                    if tipo_cauda_prop == "Bicaudal":
                        # Região esquerda
                        x_rej_esq = x[x <= z_critico_neg]
                        y_rej_esq = y[:len(x_rej_esq)]
                        ax.fill_between(x_rej_esq, y_rej_esq, alpha=0.3, color='red', label='Região de Rejeição')
                        
                        # Região direita
                        x_rej_dir = x[x >= z_critico_pos]
                        y_rej_dir = y[len(y)-len(x_rej_dir):]
                        ax.fill_between(x_rej_dir, y_rej_dir, alpha=0.3, color='red')
                        
                        # Linhas críticas
                        ax.axvline(z_critico_neg, color='orange', linestyle='--', linewidth=2, label=f'Valores Críticos: ±{abs(z_critico_pos):.3f}')
                        ax.axvline(z_critico_pos, color='orange', linestyle='--', linewidth=2)
                        
                    elif tipo_cauda_prop == "Unicaudal Esquerda":
                        x_rej = x[x <= z_critico]
                        y_rej = y[:len(x_rej)]
                        ax.fill_between(x_rej, y_rej, alpha=0.3, color='red', label='Região de Rejeição')
                        ax.axvline(z_critico, color='orange', linestyle='--', linewidth=2, label=f'Valor Crítico: {z_critico:.3f}')
                        
                    else:  # Unicaudal Direita
                        x_rej = x[x >= z_critico]
                        y_rej = y[len(y)-len(x_rej):]
                        ax.fill_between(x_rej, y_rej, alpha=0.3, color='red', label='Região de Rejeição')
                        ax.axvline(z_critico, color='orange', linestyle='--', linewidth=2, label=f'Valor Crítico: {z_critico:.3f}')
                    
                    # Linha da estatística observada
                    ax.axvline(z_estatistica, color='green', linestyle='-', linewidth=3, label=f'Estatística Z Observada: {z_estatistica:.3f}')
                    
                    # Configurações do gráfico
                    ax.set_xlabel('Valores da Estatística Z', fontsize=12)
                    ax.set_ylabel('Densidade de Probabilidade', fontsize=12)
                    ax.set_title(f'Distribuição Normal Padrão - Teste {tipo_cauda_prop} para Proporção', fontsize=14, fontweight='bold')
                    ax.legend(loc='upper right', fontsize=10)
                    ax.grid(True, alpha=0.3)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    
                    st.pyplot(fig)
                    plt.close()
                    
                    # Tabela de resumo
                    st.markdown("---")
                    st.subheader("📋 Resumo do Teste")
                    
                    resumo_prop = pd.DataFrame({
                        'Parâmetro': [
                            'Tipo de Teste',
                            'Tipo de Cauda',
                            'Hipótese Nula (H₀)',
                            'Proporção Amostral (p̂)',
                            'Número de Sucessos (x)',
                            'Tamanho da Amostra (n)',
                            'Erro Padrão',
                            'Estatística Z',
                            'P-valor',
                            'Nível de Significância (α)',
                            'Aproximação Normal',
                            'Decisão'
                        ],
                        'Valor': [
                            'Z-test para Proporção',
                            tipo_cauda_prop,
                            f'p = {proporcao_h0:.4f}',
                            f'{proporcao_amostral:.4f}',
                            num_sucessos,
                            tamanho_amostra_prop,
                            f'{erro_padrao_prop:.6f}',
                            f'{z_estatistica:.4f}',
                            f'{p_valor_prop:.6f}',
                            alpha_prop,
                            'Válida ✓' if aproximacao_valida else 'Atenção ⚠️',
                            decisao_texto
                        ]
                    })
                    
                    st.dataframe(resumo_prop, hide_index=True, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Erro no cálculo: {str(e)}")
                st.info("Verifique se todos os valores inseridos são válidos.")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>📊 Calculadora Estatística | Desenvolvida com Streamlit</p>
    <p style='font-size: 0.8em;'>Utilize esta ferramenta para análises estatísticas de intervalos de confiança e testes de hipótese</p>
</div>
""", unsafe_allow_html=True)