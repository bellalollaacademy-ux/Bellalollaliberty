import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# 1. ESTILO VISUAL (PALETA BELLA LOLLA)
st.set_page_config(page_title="Bella Lolla Studio Academy", layout="centered")

st.markdown(f"""
    <style>
    .main {{ background-color: #1A0D0A; color: #EAD2AC; font-family: 'Serif'; }}
    h1 {{ color: #B17A3E; text-align: center; border-bottom: 2px solid #B17A3E; }}
    h2, h3 {{ color: #B17A3E; }}
    .stButton>button {{ background-color: #B17A3E; color: white; border-radius: 20px; font-weight: bold; width: 100%; }}
    .stMetric {{ background-color: #3D1F1A; padding: 15px; border-radius: 15px; border: 1px solid #B17A3E; }}
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE DADOS
if 'vendas' not in st.session_state: st.session_state.vendas = []
if 'estoque' not in st.session_state: st.session_state.estoque = {}
if 'start_time' not in st.session_state: st.session_state.start_time = None

st.markdown("<h1>BELLA LOLLA <br> <span style='font-size: 0.6em;'>STUDIO ACADEMY</span></h1>", unsafe_allow_html=True)

menu = ["💎 Precificação", "⏱️ Cronômetro & Lucro", "💰 Fluxo de Caixa", "📦 Estoque", "💳 Taxas", "🏠 Espaço Aluna"]
choice = st.sidebar.radio("Navegação", menu)

# --- 1. PRECIFICAÇÃO ---
if choice == "💎 Precificação":
    st.header("Gerador de Preço")
    nome_t = st.text_input("Técnica", "Cílios Fio a Fio")
    c1, c2 = st.columns(2)
    with c1:
        mat = st.number_input("Custo Material (R$)", 10.0)
        tempo_est = st.number_input("Tempo Estimado (Horas)", 1.5)
    with c2:
        nivel = st.select_slider("Nível", ["Iniciante", "Intermediário", "Master"])
        fixo = st.number_input("Custo Fixo/Hora (R$)", 15.0)

    mult = {"Iniciante": 1.6, "Intermediário": 2.5, "Master": 4.0}
    preco_final = (mat + (tempo_est * fixo)) * mult[nivel]

    if st.button("CALCULAR PREÇO SUGERIDO"):
        st.metric("Cobrar no mínimo:", f"R$ {preco_final:.2f}")

# --- 2. NOVO: CRONÔMETRO DE SERVIÇO ---
elif choice == "⏱️ Cronômetro & Lucro":
    st.header("Cronômetro de Procedimento")
    st.write("Use para saber quanto tempo você leva e se está tendo lucro real.")
    
    col1, col2 = st.columns(2)
    if col1.button("▶️ Iniciar Atendimento"):
        st.session_state.start_time = datetime.now()
        st.success("Cronômetro iniciado!")

    if col2.button("⏹️ Finalizar e Calcular"):
        if st.session_state.start_time:
            end_time = datetime.now()
            duracao = end_time - st.session_state.start_time
            minutos = duracao.total_seconds() / 60
            horas = minutos / 60
            
            st.session_state.ultimo_tempo = minutos
            st.info(f"Tempo total: {int(minutos)} minutos.")
            
            # Cálculo de Lucro Real (Exemplo com R$ 100 de serviço)
            valor_cobrado = st.number_input("Quanto você cobrou nesse atendimento?", 100.0)
            custo_hora = 20.0 # Exemplo de custo fixo
            lucro_real = valor_cobrado - (horas * custo_hora)
            
            st.metric("Lucro Real (descontando seu tempo)", f"R$ {lucro_real:.2f}")
            st.session_state.start_time = None
        else:
            st.error("Inicie o cronômetro primeiro!")

# --- 3. FLUXO DE CAIXA & FIDELIZAÇÃO ---
elif choice == "💰 Fluxo de Caixa":
    st.header("Vendas e Fidelização")
    with st.form("venda"):
        serv = st.text_input("Serviço")
        val = st.number_input("Valor", 0.0)
        if st.form_submit_button("Registrar"):
            st.session_state.vendas.append({"Serviço": serv, "Valor": val})
            st.balloons()
            
    if st.session_state.vendas:
        df = pd.DataFrame(st.session_state.vendas)
        st.table(df)
        total = df["Valor"].sum()
        
        st.subheader("💡 Dica de Fidelização")
        proxima = datetime.now() + timedelta(days=20)
        st.warning(f"Mande mensagem para a cliente de hoje no dia **{proxima.strftime('%d/%m')}** para agendar a manutenção!")

        st.divider()
        st.subheader("🏦 Divisão do Dinheiro")
        c1, c2, c3 = st.columns(3)
        c1.metric("🛒 Estoque (20%)", f"R$ {total*0.2:.2f}")
        c2.metric("🏠 Contas (30%)", f"R$ {total*0.3:.2f}")
        c3.metric("👸 MEU SALÁRIO", f"R$ {total*0.5:.2f}")

# --- 4. ESTOQUE ---
elif choice == "📦 Estoque":
    st.header("Controle de Materiais")
    prod = st.text_input("Novo Produto")
    qtd = st.number_input("Quantidade", 1)
    if st.button("Adicionar"):
        st.session_state.estoque[prod] = qtd

    for p, q in list(st.session_state.estoque.items()):
        col_a, col_b = st.columns([3, 1])
        col_a.write(f"**{p}**")
        if col_b.button("Gastei 1", key=p):
            st.session_state.estoque[p] -= 1
            st.rerun()

# --- 5. CALCULADORA DE TAXAS ---
elif choice == "💳 Taxas":
    st.header("Calculadora de Maquininha")
    valor_quer = st.number_input("Quanto quer receber limpo?", 100.0)
    maquina = st.selectbox("Forma", ["Pix", "Débito (2%)", "Crédito (5%)"])
    taxa = 0.02 if "Débito" in maquina else (0.05 if "Crédito" in maquina else 0)
    cobrar = valor_quer / (1 - taxa)
    st.success(f"Você deve cobrar: **R$ {cobrar:.2f}**")

# --- 6. ESPAÇO DA ALUNA ---
elif choice == "🏠 Espaço Aluna":
    nome_e = st.text_input("Nome do seu Espaço profissional:")
    st.subheader(f"Bem-vinda ao {nome_e}!")
    st.write("---")
    st.markdown("**Metas Bella Lolla Academy:**")
    st.checkbox("Atender 50 clientes com perfeição")
    st.checkbox("Dominar a técnica Master")
    st.checkbox("Separar o salário das contas do Studio")
