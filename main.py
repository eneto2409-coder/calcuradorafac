import streamlit as st

# 1. Configuração da Página e Tema Bloodline (Preto e Roxo)
st.set_page_config(page_title="Bloodline Production", page_icon="🩸", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stMetric { 
        background-color: #0a0a0a; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #8a2be2;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.2);
    }
    h1, h2, h3 { color: #8a2be2 !important; font-family: 'Segoe UI', sans-serif; }
    .stSelectbox, .stNumberInput, .stRadio { color: white !important; }
    .stExpander { background-color: #0a0a0a; border: 1px solid #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

# 2. Banco de Dados Ajustado (Tudo por unidade individual)
database = {
    "Uzi": {
        "tipo": "Arma",
        "unidade": "unidade(s)",
        "peso": 4.25,
        "economia": 13225,
        "receita": {
            "Peças de Metal": 175, "Peças de Cobre": 175, "Peças de Vidro": 285, 
            "Peças Arma Média": 2, "Peças Plástico": 285, "Peças Borracha": 285, 
            "Sucata de Metal": 875, "Corpo de Sub": 1
        },
        "precos": {
            "Parceria": {"Limpo": 90, "Sujo": 117},
            "Pista": {"Limpo": 115, "Sujo": 149}
        }
    },
    "Steyr AUG": {
        "tipo": "Arma",
        "unidade": "unidade(s)",
        "peso": 5.75,
        "economia": 75225,
        "receita": {
            "Uzi (Base)": 1, "Peças de Metal": 85, "Peças de Cobre": 85, 
            "Fios de Cobre": 2, "Peças Borracha": 175, "Porcas e Parafusos": 2, 
            "Caixa de Aperfeiçoamento": 1
        },
        "precos": {
            "Parceria": {"Limpo": 130, "Sujo": 162},
            "Pista": {"Limpo": 180, "Sujo": 234}
        }
    },
    "Munição de Rifle (Fuzil)": {
        "tipo": "Munição",
        "unidade": "bala(s)",
        "peso": 0.025 / 30,  # Peso por bala individual
        "economia": 120 / 30, # Economia por bala individual
        "receita": {
            "Peças de Metal": 20 / 30, "Peças de Cobre": 20 / 30, "Frasco de Pólvora": 5 / 30
        },
        "precos": {
            "Parceria": {"Limpo": 200, "Sujo": 260},
            "Pista": {"Limpo": 250, "Sujo": 325}
        }
    },
    "Munição de Sub": {
        "tipo": "Munição",
        "unidade": "bala(s)",
        "peso": 0.025 / 30,
        "economia": 100 / 30,
        "receita": {
            "Peças de Metal": 10 / 30, "Peças de Cobre": 10 / 30, "Frasco de Pólvora": 3 / 30
        },
        "precos": {
            "Parceria": {"Limpo": 125, "Sujo": 162},
            "Pista": {"Limpo": 200, "Sujo": 260}
        }
    },
    "Munição de PT": {
        "tipo": "Munição",
        "unidade": "bala(s)",
        "peso": 0.025 / 30,
        "economia": 60 / 30,
        "receita": {
            "Peças de Cobre": 10 / 30, "Frasco de Pólvora": 2 / 30
        },
        "precos": {
            "Parceria": {"Limpo": 95, "Sujo": 123},
            "Pista": {"Limpo": 130, "Sujo": 169}
        }
    },
    "Flipper Hacker": {
        "tipo": "Utilitário",
        "unidade": "unidade(s)",
        "peso": 0.100,
        "economia": 500,
        "receita": {
            "Peças de Metal": 15, "Peças de Cobre": 10, "Fios de Cobre": 2, "Plástico": 15
        },
        "precos": {
            "Parceria": {"Limpo": 90, "Sujo": 90}, 
            "Pista": {"Limpo": 110, "Sujo": 110}
        }
    }
}

# 3. Interface do Usuário
st.title("🩸 BLOODLINE PRODUCTION HUB")
st.write("Módulo de cálculo simplificado por unidades reais.")

col1, col2 = st.columns(2)

with col1:
    item_selecionado = st.selectbox("O que deseja fabricar?", list(database.keys()))
    unid_medida = database[item_selecionado]["unidade"]
    # Definido step=30 para munições para ajudar a preencher de 30 em 30 se quiserem, mas aceita qualquer valor
    passo = 30 if database[item_selecionado]["tipo"] == "Munição" else 1
    quantidade = st.number_input(f"Quantidade a Produzir (em {unid_medida})", min_value=1, value=passo, step=passo)

with col2:
    tabela = st.selectbox("Tabela de Venda", ["Parceria", "Pista"])
    tipo_dinheiro = st.radio("Tipo de Pagamento", ["Limpo", "Sujo"], horizontal=True)

# 4. Processamento dos Dados
item = database[item_selecionado]
valor_tabela = item["precos"][tabela][tipo_dinheiro]

if item["tipo"] == "Arma":
    total_venda = valor_tabela * 1000 * quantidade
else:
    total_venda = valor_tabela * quantidade

total_peso = item["peso"] * quantidade
total_economia = item["economia"] * quantidade

st.markdown("---")

# 5. Exibição de Métricas (Cards Roxos)
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Venda Total", f"${int(total_venda):,}")
with m2:
    st.metric("Peso Total", f"{total_peso:.3f} kg")
with m3:
    st.metric("Economia Gerada", f"${int(total_economia):,}")

# 6. Informações de Contexto Dinâmicas
if item["tipo"] == "Munição":
    packs_necessarios = quantidade / 30
    st.info(f"🎯 **No Menu de Produção:** Para obter {quantidade} balas, você precisará clicar para fabricar **{packs_necessarios:.1f} vezes** (packs).")
elif item["tipo"] == "Arma":
    st.info(f"⚔️ **Especificação:** Valor unitário na tabela: **${valor_tabela}k** (${valor_tabela * 1000:,}).")

# 7. Detalhamento de Materiais (Arredondado para cima para garantir que não falte nada)
import math
st.subheader("📋 Lista Bruta de Materiais")
with st.expander("Clique aqui para expandir a lista de materiais necessários"):
    for mat, qtd_unit in item["receita"].items():
        qtd_total = math.ceil(qtd_unit * quantidade)
        st.write(f"🟣 **{mat}**: {qtd_total:,}")

st.caption("Desenvolvido para uso exclusivo da Bloodline RP")
