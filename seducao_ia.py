import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PRESENÇA IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_presenca():
    return {"perfis": {}}

_cache = get_cache_presenca()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_consultas', 'consultas_salvas',
    'nivel_atual', 'pontuacao_total', 'treinos_completos',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_consulta(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_consultas.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
NIVEIS = ["Iniciante", "Aprendiz", "Praticante", "Habilidoso", "Magnético", "Lendário"]

defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_consultas': [], 'consultas_salvas': [],
    'nivel_atual': "Iniciante", 'pontuacao_total': 0, 'treinos_completos': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO DO APP ---
PRINCIPIO = """
IDENTIDADE E PRINCÍPIO — siga isso em TODA resposta:
- Você é um mentor de presença, charme, confiança e comunicação — especializado em ajudar homens a desenvolverem
  carisma genuíno, oratória de impacto e a capacidade de criar atração através de quem realmente são, não de quem fingem ser
- Seu modelo é o protagonista de Hollywood: confiante sem arrogância, bem-humorado sem ser palhaço, direto sem ser
  grosseiro, presente sem ser ansioso — um homem que entra num ambiente e as pessoas percebem
- Você NUNCA ensina técnicas de manipulação, scripts de sedução mecânicos, ou táticas que funcionam ignorando
  a consciência da outra pessoa. Você ensina presença real, expressão autêntica e habilidades de comunicação genuínas
- Toda sugestão de abordagem ou diálogo deve respeitar o consentimento da outra pessoa. Se alguém demonstrar
  desinteresse, a resposta certa sempre é agradecer a interação e seguir em frente com elegância — nunca insistir
- Tom: direto, confiante, sem rodeios, com um leve toque de humor quando cabe — como um mentor que já passou pelo
  que o aluno está passando e fala de igual para igual, não um professor de palco
- Português do Brasil
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚡ Lembre: nenhuma técnica substitui presença real. O objetivo é você se tornar genuinamente mais interessante
e confiante — não fingir ser alguém que não é.
</div>
"""

# --- MOTOR DE IA ---
def presenca_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um mentor de presença, charme e oratória — o coach que o protagonista de Hollywood teria.
Usuário: {st.session_state.usuario}. Nível atual: {st.session_state.nivel_atual}.
{PRINCIPIO}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def calcular_nivel(pontos: int) -> str:
    if pontos >= 500: return "Lendário"
    elif pontos >= 300: return "Magnético"
    elif pontos >= 150: return "Habilidoso"
    elif pontos >= 60: return "Praticante"
    elif pontos >= 20: return "Aprendiz"
    return "Iniciante"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_consultas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#1E1E2E;border:1px solid #6D28D9;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#CBD5E1;line-height:1.6;'>"
            f"💾 <strong style='color:#F1F5F9'>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#6D28D9;font-size:0.88em;'>{total} sessões · {st.session_state.treinos_completos} treinos completos · {st.session_state.pontuacao_total} pontos</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"presenca_ia_{nome_usuario}.json", mime="application/json", use_container_width=True, key="seducaoi3")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'consultas_salvas' not in st.session_state: st.session_state['consultas_salvas'] = []
if 'historico_consultas' not in st.session_state: st.session_state['historico_consultas'] = []
if 'nivel_atual' not in st.session_state: st.session_state['nivel_atual'] = None
if 'pontuacao_total' not in st.session_state: st.session_state['pontuacao_total'] = 0
if 'treinos_completos' not in st.session_state: st.session_state['treinos_completos'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 PRESENÇA IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    (_tab_Home, _tab_Confianca, _tab_Charme, _tab_Oratoria, _tab_Atracao, _tab_Conversa, _tab_Simulador, _tab_Linguagem, _tab_Situacoes, _tab_Mentalidade, _tab_Historias, _tab_Academia, _tab_Desafio, _tab_Mentor) = st.tabs(['🏠 Painel', '💪 Confiança', '✨ Charme', '🎤 Oratória', '💘 Atração', '📱 Conversa', '🎭 Simulador', '👁️ Linguagem', '🔥 Situações', '🧠 Mentalidade', '📖 Histórias', '🎓 Academia', '🏆 Desafio', '🤖 Mentor 24h'])

    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"⚡ Bem-vindo, {st.session_state.usuario}")
        with col_r:
            if st.button("🚪 Sair", key="seducaoi3_d2"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_consultas) == 0:
            st.markdown("""<div style="background:#1E1E2E;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;font-size:0.9em;font-weight:600;">
            ⚠️ <span style='color:#FDE68A'>Seus dados não estão mais no servidor. Recupere seu .json abaixo.</span>
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Recuperar dados (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        # --- PAINEL DE NÍVEL ---
        nivel = st.session_state.nivel_atual
        pts = st.session_state.pontuacao_total
        treinos = st.session_state.treinos_completos

        st.markdown(f"""
        <div class="nivel-box">
            <div style="font-size:0.85em;opacity:0.8;">SEU NÍVEL ATUAL</div>
            <div class="nivel-titulo">⚡ {nivel}</div>
            <div style="font-size:0.9em;margin-top:4px;">{pts} pontos · {treinos} treinos completos</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_consultas)}</div><div style='color:#CBD5E1'>Sessões</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{treinos}</div><div style='color:#CBD5E1'>Treinos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{pts}</div><div style='color:#CBD5E1'>Pontos</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.consultas_salvas)}</div><div style='color:#CBD5E1'>Salvos</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>⚡ <em>'Um homem magnético não age para impressionar. Ele age — e impressiona sem perceber.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ Módulos")
        guia = {
            "💪 Confiança e Presença": "Linguagem corporal, postura, como entrar num ambiente e ser notado",
            "✨ Charme e Humor": "Como ser naturalmente engraçado, leve e agradável de estar por perto",
            "🎤 Oratória e Voz": "Dicção, ritmo, pausa, tom — como falar de forma que as pessoas ouçam",
            "💘 Atração e Sedução": "Como criar tensão, interesse e atração de forma autêntica",
            "📱 A Conversa Perfeita": "Como iniciar, manter e conduzir conversas que criam conexão",
            "🎭 Simulador de Abordagem": "Treine abordagens antes de executar na vida real",
            "👁️ Linguagem Corporal": "O que seu corpo comunica e como calibrar isso",
            "🔥 Situações Reais": "Situações específicas — bar, academia, app, trabalho — como agir em cada uma",
            "🧠 Mentalidade do Protagonista": "Como um homem confiante pensa — e como você pode pensar assim",
            "📖 A Arte de Contar Histórias": "Como narrar sua vida de forma que as pessoas se conectem",
            "🎓 Academia de Presença": "Aulas aprofundadas sobre cada pilar do magnetismo pessoal",
            "🏆 Desafio Semanal": "Desafio prático para executar essa semana e ganhar pontos",
            "🤖 Mentor 24h": "Converse sobre qualquer situação e receba orientação personalizada",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — <span style='color:#475569'>{desc}</span>", unsafe_allow_html=True)

        # ========================
        # CONFIANÇA E PRESENÇA
        # ========================

    with _tab_Confianca:
        st.header("💪 Confiança e Presença")

        area_conf = st.selectbox("Área:", [
            "Como entrar num ambiente e ser notado", "Como ficar à vontade em grupos",
            "Como lidar com nervosismo antes de uma situação importante", "Como ter postura de presença",
            "Como reagir quando te ignoram ou desrespeitam", "Como parar de precisar de aprovação",
            "Como ser confiante sem parecer arrogante",
        ], key="select_area_conf")

        if st.button("💪 TREINAR CONFIANÇA", key="seducaoi4"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Crie um guia prático e profundo sobre: {area_conf}\n\n"
                    f"FORMATO:\n\n"
                    f"💪 {area_conf.upper()}\n\n"
                    f"🎬 A CENA:\n[descreva como um homem sem esse skill age vs como um homem com esse skill age — seja específico e visual]\n\n"
                    f"🧠 O MECANISMO:\n[por que isso acontece — psicologia e comportamento por trás]\n\n"
                    f"⚙️ COMO DESENVOLVER — PASSO A PASSO:\n[instruções concretas, não conselhos vagos]\n\n"
                    f"💬 O QUE DIZER/FAZER NA PRÁTICA:\n[exemplos de falas, postura, reações específicas]\n\n"
                    f"🏋️ TREINO DESTA SEMANA:\n[1 exercício real para praticar essa habilidade em situações do dia a dia]\n\n"
                    f"⚡ A MENTALIDADE POR TRÁS:\n[o frame mental que um homem confiante carrega sobre essa situação]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Confianca", area_conf, res)
                st.session_state['conf_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('conf_temp'):
            st.markdown(f"<div class='card'>{st.session_state['conf_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['conf_temp'], file_name="confianca.txt", mime="text/plain", use_container_width=True, key="seducaoi5")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_conf", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Confianca','tema':area_conf if 'area_conf' in dir() else '','conteudo':st.session_state['conf_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CHARME E HUMOR
        # ========================

    with _tab_Charme:
        st.header("✨ Charme e Humor")

        area_charme = st.selectbox("Área:", [
            "Como ser naturalmente engraçado", "Como usar humor sem forçar",
            "Como fazer elogios que realmente funcionam", "Como ser leve e descontraído",
            "Como criar um apelido ou momento especial", "Como usar ironia sem ofender",
            "Como rir de si mesmo sem se diminuir",
        ], key="select_area_charme")

        if st.button("✨ APRENDER CHARME", key="seducaoi6"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Ensine de forma prática e com exemplos reais: {area_charme}\n\n"
                    f"FORMATO:\n\n"
                    f"✨ {area_charme.upper()}\n\n"
                    f"🎬 EXEMPLO REAL — A DIFERENÇA:\n[mini-cena mostrando quem tenta forçar vs quem tem charme genuíno — específico e visual]\n\n"
                    f"🧠 O PRINCÍPIO:\n[por que isso funciona psicologicamente]\n\n"
                    f"💬 EXEMPLOS DE FALAS E REAÇÕES:\n[pelo menos 4 exemplos concretos de como isso soa na prática]\n\n"
                    f"⚠️ O QUE ESTRAGA O CHARME:\n[os erros que tiram o efeito]\n\n"
                    f"🏋️ PRÁTICA:\n[exercício para treinar essa habilidade essa semana]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Charme", area_charme, res)
                st.session_state['charme_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('charme_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['charme_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['charme_temp'], file_name="charme.txt", mime="text/plain", use_container_width=True, key="seducaoi7")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_charme", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Charme','tema':area_charme if 'area_charme' in dir() else '','conteudo':st.session_state['charme_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # ORATÓRIA E VOZ
        # ========================

    with _tab_Oratoria:
        st.header("🎤 Oratória e Voz")

        area_orat = st.selectbox("Área:", [
            "Como projetar a voz com autoridade", "Como usar pausas para criar impacto",
            "Como contar algo e prender a atenção", "Como falar mais devagar sem parecer lento",
            "Como estruturar o que você vai dizer antes de falar", "Como se expressar sem travamentos",
            "Como dar uma opinião de forma que as pessoas ouçam", "Como falar em público com confiança",
        ], key="select_area_orat")

        if st.button("🎤 TREINAR ORATÓRIA", key="seducaoi8"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Ensine de forma prática e detalhada: {area_orat}\n\n"
                    f"FORMATO:\n\n"
                    f"🎤 {area_orat.upper()}\n\n"
                    f"🎬 A DIFERENÇA NA PRÁTICA:\n[como soa quem não tem essa habilidade vs quem tem — use exemplos de frases]\n\n"
                    f"⚙️ TÉCNICA — PASSO A PASSO:\n[instruções concretas: respiração, ritmo, pausa, tom — o que fazer fisicamente]\n\n"
                    f"💬 EXEMPLOS DE FALAS:\n[mesma ideia, dita de duas formas — a fraca e a poderosa — para cada técnica ensinada]\n\n"
                    f"🏋️ EXERCÍCIO DE VOZ:\n[exercício físico/prático para treinar essa habilidade, que pode ser feito sozinho]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Oratoria", area_orat, res)
                st.session_state['orat_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('orat_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['orat_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['orat_temp'], file_name="oratoria.txt", mime="text/plain", use_container_width=True, key="seducaoi9")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_orat", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Oratoria','tema':area_orat if 'area_orat' in dir() else '','conteudo':st.session_state['orat_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # ATRAÇÃO E SEDUÇÃO
        # ========================

    with _tab_Atracao:
        st.header("💘 Atração e Sedução")

        area_atr = st.selectbox("Área:", [
            "Como criar tensão de forma natural", "Como demonstrar interesse sem parecer desesperado",
            "Como ser direto e demonstrar intenção com elegância", "Como criar mistério sem ser frio",
            "Como lidar com rejeição com classe", "Como criar uma segunda conversa após o primeiro encontro",
            "Como convidar alguém de forma natural",
        ], key="select_area_atr")

        if st.button("💘 APRENDER", key="seducaoi10"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Ensine de forma prática, direta e com exemplos: {area_atr}\n\n"
                    f"FORMATO:\n\n"
                    f"💘 {area_atr.upper()}\n\n"
                    f"🎬 COMO PARECE NA REALIDADE:\n[cena específica com diálogo mostrando como isso se manifesta — inclua um exemplo que funciona e um que não funciona]\n\n"
                    f"⚙️ O MECANISMO:\n[por que essa dinâmica funciona — psicologia da atração por trás]\n\n"
                    f"💬 O QUE DIZER:\n[3-4 exemplos de falas/abordagens que aplicam isso — adaptáveis, não scripts robóticos]\n\n"
                    f"⚠️ ONDE A MAIORIA ERRA:\n[o erro mais comum que destrói esse efeito]\n\n"
                    f"✅ A LINHA QUE NÃO SE CRUZA:\n[como garantir que a abordagem respeita a outra pessoa — incluindo como reconhecer e aceitar desinteresse com elegância]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Atracao", area_atr, res)
                st.session_state['atr_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('atr_temp'):
            st.markdown(f"<div class='card'>{st.session_state['atr_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['atr_temp'], file_name="atracao.txt", mime="text/plain", use_container_width=True, key="seducaoi11")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_atr", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Atracao','tema':area_atr if 'area_atr' in dir() else '','conteudo':st.session_state['atr_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # A CONVERSA PERFEITA
        # ========================

    with _tab_Conversa:
        st.header("📱 A Conversa Perfeita")

        tab1, tab2 = st.tabs(["🎯 Aprender a Técnica", "💬 Me Ajuda com Esta Conversa"])

        with tab1:
            tecnica_conv = st.selectbox("Técnica:", [
                "Como abrir uma conversa presencialmente", "Como não deixar a conversa morrer",
                "Como fazer perguntas que aprofundam", "Como usar silêncios de forma poderosa",
                "Como criar uma conversa via mensagem que leva ao encontro",
                "Como responder de forma que mantém o interesse", "Como sair da friendzone conversacional",
            ], key="select_tecnica_conv")

            if st.button("🎯 APRENDER", key="seducaoi12"):
                with st.spinner("Preparando..."):
                    prompt = (
                        f"Ensine: {tecnica_conv}\n\n"
                        f"FORMATO:\n\n"
                        f"🎯 {tecnica_conv.upper()}\n\n"
                        f"🎬 EXEMPLO COMPLETO — COMO FICA NA PRÁTICA:\n[diálogo real mostrando a técnica aplicada do início ao fim]\n\n"
                        f"⚙️ OS PRINCÍPIOS:\n[o que está por trás dessa técnica]\n\n"
                        f"💬 VARIAÇÕES E ADAPTAÇÕES:\n[como adaptar para diferentes contextos: presencial, mensagem, grupo...]\n\n"
                        f"⚠️ ERRO MAIS COMUM:\n[o que a maioria faz de errado nessa situação]"
                    )
                    res = presenca_ia(prompt)
                    salvar_consulta("Conversa", tecnica_conv, res)
                    st.session_state['conv_tec_temp'] = res
                    st.session_state.pontuacao_total += 5
                    st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

            if st.session_state.get('conv_tec_temp'):
                st.markdown(f"<div class='card'>{st.session_state['conv_tec_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['conv_tec_temp'], file_name="tecnica_conversa.txt", mime="text/plain", key="dl_conv_tec")

        with tab2:
            minha_conversa = st.text_area("Cole a conversa que está emperrada ou que você quer continuar:", height=150,
                placeholder="ex: Ela: 'kk foi boa a reunião' / Eu: 'Foi sim rs' / Ela: 🙂", key="seducaoi2")

            if st.button("💬 COMO RESPONDER ISSO?", key="seducaoi13"):
                if minha_conversa.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise esta conversa e ajude com a próxima jogada.\n"
                            f"Conversa: {minha_conversa}\n\n"
                            f"FORMATO:\n\n"
                            f"📊 DIAGNÓSTICO:\n[como está a dinâmica desta conversa — curto e direto]\n\n"
                            f"💬 3 OPÇÕES DE RESPOSTA:\n\n"
                            f"🔥 DIRETA E INTENCIONAL:\n[demonstra interesse claro com confiança]\n\n"
                            f"😄 LEVE E DIVERTIDA:\n[cria leveza e humor]\n\n"
                            f"🎯 QUE AVANÇA:\n[leva a conversa para algum lugar — encontro, plano, tema novo]\n\n"
                            f"💡 QUAL USAR E POR QUÊ:\n[recomendação baseada no tom da conversa]"
                        )
                        res = presenca_ia(prompt)
                        salvar_consulta("Conversa", minha_conversa[:60], res)
                        st.session_state['conv_resp_temp'] = res
                else:
                    st.warning("Cole a conversa.")

            if st.session_state.get('conv_resp_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['conv_resp_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # SIMULADOR DE ABORDAGEM
        # ========================

    with _tab_Simulador:
        st.header("🎭 Simulador de Abordagem")
        st.markdown("A IA interpreta a pessoa. Você treina antes de executar na vida real.")

        if 'chat_simulador' not in st.session_state:
            st.session_state.chat_simulador = []
        if 'sim_key' not in st.session_state:
            st.session_state.sim_key = 0
        if 'sim_perfil_config' not in st.session_state:
            st.session_state.sim_perfil_config = ""

        if not st.session_state.chat_simulador:
            st.markdown("#### Configure o cenário:")
            col1, col2 = st.columns(2)
            with col1:
                contexto_sim = st.selectbox("Contexto:", ["Bar/balada","Academia","Trabalho/networking","App de relacionamento","Café/restaurante","Via amigos em comum"], key="seducaoi14")
                perfil_sim = st.selectbox("Perfil da pessoa:", ["Expansiva e animada","Reservada e séria","Intelectual e curiosa","Bem-humorada e irônica","Ocupada e distraída"], key="seducaoi15")
            with col2:
                nivel_sim = st.selectbox("Dificuldade:", ["Receptiva (fácil)","Neutra (médio)","Difícil de conquistar","Ocupada e sem interesse inicial"], key="seducaoi16")

            if st.button("🎭 INICIAR SIMULAÇÃO", key="seducaoi17"):
                st.session_state.sim_perfil_config = f"Contexto: {contexto_sim}. Perfil: {perfil_sim}. Dificuldade: {nivel_sim}"
                st.rerun()
        else:
            st.markdown(f"<div class='disclaimer'>🎭 Cenário: {st.session_state.sim_perfil_config}</div>", unsafe_allow_html=True)

            for msg in st.session_state.chat_simulador:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#2D1B4E;border:1px solid #7C3AED;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b style='color:#DDD6FE'>Você:</b> <span style='color:#F1F5F9'>{msg['content']}</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='treino-box' style='margin:8px 0;'><b>🎭 {st.session_state.sim_perfil_config.split('.')[1].replace('Perfil:','').strip() if '.' in st.session_state.sim_perfil_config else 'Pessoa'}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

            msg_sim = st.text_input("O que você diz:", key=f"sim_input_{st.session_state.sim_key}")

            col_env, col_feed, col_reset = st.columns([3, 2, 1])
            with col_env:
                if st.button("📤 ENVIAR", key="seducaoi18"):
                    if msg_sim.strip():
                        with st.spinner("..."):
                            resp = presenca_ia(
                                msg_sim,
                                f"MODO SIMULAÇÃO. Perfil: {st.session_state.sim_perfil_config}. "
                                f"Responda como essa pessoa responderia de forma realista e consistente com o perfil e dificuldade. "
                                f"Não saia do personagem. Seja natural, não exagerado. Se a abordagem for boa, mostre interesse gradual. "
                                f"Se for fraca, mostre frieza ou desvio do assunto."
                            )
                        st.session_state.chat_simulador.append({"role": "user", "content": msg_sim})
                        st.session_state.chat_simulador.append({"role": "assistant", "content": resp})
                        st.session_state.sim_key += 1
                        st.rerun()
            with col_feed:
                if st.button("📊 ANÁLISE DO TREINO", key="seducaoi19"):
                    with st.spinner("Analisando..."):
                        historico = "\n".join([f"{'Você' if m['role']=='user' else 'Pessoa'}: {m['content']}" for m in st.session_state.chat_simulador])
                        prompt = (
                            f"Analise esta abordagem simulada.\nSimulação: {historico}\n\n"
                            f"FORMATO:\n\n"
                            f"📊 ANÁLISE DO TREINO\n\n"
                            f"⭐ NOTA GERAL: [X]/10\n\n"
                            f"✅ O QUE FUNCIONOU BEM:\n[pontos fortes específicos]\n\n"
                            f"⚠️ O QUE PODERIA SER MELHOR:\n[erros ou oportunidades perdidas]\n\n"
                            f"💬 COMO PODERIA TER DITO MELHOR:\n[reescreva 1-2 falas que poderiam ter mais impacto]\n\n"
                            f"🎯 PARA A PRÓXIMA VEZ:\n[1 coisa principal para melhorar]"
                        )
                        res = presenca_ia(prompt)
                        st.session_state['sim_analise_temp'] = res
                        st.session_state.pontuacao_total += 10
                        st.session_state.treinos_completos += 1
                        st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)
                        salvar_consulta("Simulador", "Simulação de abordagem", res)
            with col_reset:
                if st.button("🔄", key="seducaoi20"):
                    for k in ['chat_simulador','sim_perfil_config','sim_analise_temp']:
                        st.session_state.pop(k, None)
                    st.rerun()

            if st.session_state.get('sim_analise_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['sim_analise_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # LINGUAGEM CORPORAL
        # ========================

    with _tab_Linguagem:
        st.header("👁️ Linguagem Corporal")

        area_ling = st.selectbox("Área:", [
            "Postura que transmite confiança", "Como usar o olhar de forma poderosa",
            "Como usar o espaço ao seu redor", "Como gesticular de forma natural e impactante",
            "Como controlar o sorriso (quando e como usar)", "Como aproximar-se fisicamente sem invadir",
            "Como identificar sinais de interesse ou desconforto na outra pessoa",
        ], key="select_area_ling")

        if st.button("👁️ APRENDER", key="seducaoi21"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Ensine de forma visual e prática: {area_ling}\n\n"
                    f"FORMATO:\n\n"
                    f"👁️ {area_ling.upper()}\n\n"
                    f"🎬 COMO PARECE NA PRÁTICA:\n[descreva visualmente — como o corpo, o olhar, a posição mudam entre quem tem e quem não tem essa habilidade]\n\n"
                    f"⚙️ AS TÉCNICAS ESPECÍFICAS:\n[instruções físicas concretas — onde colocar as mãos, como posicionar os ombros, etc]\n\n"
                    f"🔄 OS ERROS MAIS COMUNS:\n[o que a maioria faz que passa a mensagem errada]\n\n"
                    f"🏋️ EXERCÍCIO:\n[como treinar isso — um exercício físico real, não só teoria]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Linguagem", area_ling, res)
                st.session_state['ling_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('ling_temp'):
            st.markdown(f"<div class='card'>{st.session_state['ling_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['ling_temp'], file_name="linguagem_corporal.txt", mime="text/plain", key="seducaoi22")

        # ========================
        # SITUAÇÕES REAIS
        # ========================

    with _tab_Situacoes:
        st.header("🔥 Situações Reais")
        st.markdown("Como agir em situações específicas do dia a dia.")

        situacao_real = st.selectbox("Situação:", [
            "Abordagem no bar/balada", "Abordagem na academia", "Colega de trabalho",
            "Primeira mensagem no app", "Após pegar o número", "Primeiro encontro — presencialmente",
            "Ela ficou fria de repente", "Ela demorou a responder", "Voltando após sumir",
            "Como pedir o número de forma natural",
        ], key="select_situacao_real")

        if st.button("🔥 COMO AGIR", key="seducaoi23"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Dê um guia completo e direto para esta situação: {situacao_real}\n\n"
                    f"FORMATO:\n\n"
                    f"🔥 {situacao_real.upper()}\n\n"
                    f"📌 O CONTEXTO:\n[o que torna essa situação específica — seus desafios e oportunidades únicos]\n\n"
                    f"🎬 COMO UM HOMEM MAGNÉTICO AGE NESSA SITUAÇÃO:\n[cena detalhada — o que ele diz, como ele age, qual é o frame mental]\n\n"
                    f"💬 EXEMPLOS DE FALAS REAIS:\n[3-4 exemplos adaptáveis para essa situação específica]\n\n"
                    f"⚠️ O MAIOR ERRO:\n[o que destrói as chances nessa situação]\n\n"
                    f"✅ COMO SABER SE ESTÁ INDO BEM:\n[sinais de que a situação está evoluindo na direção certa]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Situacoes", situacao_real, res)
                st.session_state['sit_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('sit_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['sit_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['sit_temp'], file_name="situacao_real.txt", mime="text/plain", use_container_width=True, key="seducaoi24")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_sit", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Situacoes','tema':situacao_real if 'situacao_real' in dir() else '','conteudo':st.session_state['sit_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # MENTALIDADE DO PROTAGONISTA
        # ========================

    with _tab_Mentalidade:
        st.header("🧠 Mentalidade do Protagonista")

        tema_ment = st.selectbox("Tema:", [
            "Como um homem confiante pensa sobre si mesmo", "Como lidar com rejeição sem ser abalado",
            "Como parar de dar valor demais antes de ganhar a pessoa", "Como ter vida própria que te torna mais atraente",
            "Como sair do modo ansioso para o modo presente", "Como pensar em abundância em vez de escassez",
            "Como ser o protagonista da sua própria vida",
        ], key="select_tema_ment")

        if st.button("🧠 TRANSFORMAR A MENTALIDADE", key="seducaoi25"):
            with st.spinner("Preparando..."):
                prompt = (
                    f"Fale sobre a mentalidade de um homem realmente confiante em relação a: {tema_ment}\n\n"
                    f"FORMATO:\n\n"
                    f"🧠 {tema_ment.upper()}\n\n"
                    f"🔴 A MENTALIDADE LIMITANTE (como a maioria pensa):\n[o frame mental que sabota — seja específico, não genérico]\n\n"
                    f"🟢 A MENTALIDADE DO PROTAGONISTA (como um homem de presença pensa):\n[o frame mental correto — com exemplos de como esse pensamento muda o comportamento na prática]\n\n"
                    f"🔄 COMO FAZER A TRANSIÇÃO:\n[o que fazer quando pegar o pensamento limitante acontecendo — específico e prático]\n\n"
                    f"💬 O QUE UM HOMEM COM ESSA MENTALIDADE DIRIA/FARIA:\n[exemplos concretos de comportamento e fala que demonstram essa mentalidade]\n\n"
                    f"⚡ A FRASE QUE RESUME:\n[1 frase curta e poderosa para fixar essa mentalidade]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Mentalidade", tema_ment, res)
                st.session_state['ment_temp'] = res
                st.session_state.pontuacao_total += 5
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('ment_temp'):
            st.markdown(f"<div class='card'>{st.session_state['ment_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['ment_temp'], file_name="mentalidade.txt", mime="text/plain", use_container_width=True, key="seducaoi26")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_ment", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Mentalidade','tema':tema_ment if 'tema_ment' in dir() else '','conteudo':st.session_state['ment_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # A ARTE DE CONTAR HISTÓRIAS
        # ========================

    with _tab_Historias:
        st.header("📖 A Arte de Contar Histórias")

        tab_aprender, tab_praticar = st.tabs(["📖 Aprender a Técnica", "✍️ Transforme Sua História"])

        with tab_aprender:
            tecnica_hist = st.selectbox("Técnica:", [
                "Como estruturar uma história que prende atenção", "Como usar emoção na narrativa",
                "Como contar sobre si mesmo sem parecer que está se exibindo", "Como fazer as pessoas rirem contando algo que aconteceu",
                "Como criar suspense em histórias do dia a dia", "Como terminar uma história com impacto",
            ], key="select_tecnica_hist")

            if st.button("📖 APRENDER", key="seducaoi27"):
                with st.spinner("Preparando..."):
                    prompt = (
                        f"Ensine: {tecnica_hist}\n\n"
                        f"FORMATO:\n\n"
                        f"📖 {tecnica_hist.upper()}\n\n"
                        f"🎬 A DIFERENÇA:\n[mesma história contada de forma fraca vs contada com essa técnica — mostre ambas em detalhes]\n\n"
                        f"⚙️ A ESTRUTURA:\n[os elementos técnicos que criam o efeito]\n\n"
                        f"💬 EXEMPLO COMPLETO:\n[uma história curta usando exatamente essa técnica]\n\n"
                        f"🏋️ PRATIQUE:\n[exercício para aplicar isso com histórias da sua própria vida]"
                    )
                    res = presenca_ia(prompt)
                    salvar_consulta("Historias", tecnica_hist, res)
                    st.session_state['hist_tec_temp'] = res
                    st.session_state.pontuacao_total += 5
                    st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

            if st.session_state.get('hist_tec_temp'):
                st.markdown(f"<div class='card'>{st.session_state['hist_tec_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['hist_tec_temp'], file_name="tecnica_historias.txt", mime="text/plain", key="dl_hist_tec")

        with tab_praticar:
            st.markdown("Cole uma história que você quer contar melhor — a IA reescreve com mais impacto.")
            minha_historia = st.text_area("Sua história (como você contaria hoje):", height=150,
                placeholder="ex: No final de semana passado fui numa festa e aconteceu uma coisa engraçada...", key="seducaoi1")

            if st.button("✍️ REESCREVER COM IMPACTO", key="seducaoi28"):
                if minha_historia.strip():
                    with st.spinner("Reescrevendo..."):
                        prompt = (
                            f"Reescreva esta história com muito mais impacto, emoção e magnetismo narrativo.\n"
                            f"História original: {minha_historia}\n\n"
                            f"FORMATO:\n\n"
                            f"📝 VERSÃO ORIGINAL (diagnóstico):\n[o que está fraco ou pode ser melhorado]\n\n"
                            f"⚡ VERSÃO COM IMPACTO:\n[a história reescrita com tensão, ritmo e emoção — mantenha os fatos reais, só melhore a narrativa]\n\n"
                            f"📚 O QUE MUDOU:\n[explique as escolhas narrativas feitas]"
                        )
                        res = presenca_ia(prompt)
                        salvar_consulta("Historias", minha_historia[:60], res)
                        st.session_state['hist_reesc_temp'] = res
                else:
                    st.warning("Cole sua história.")

            if st.session_state.get('hist_reesc_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['hist_reesc_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # ACADEMIA DE PRESENÇA
        # ========================

    with _tab_Academia:
        st.header("🎓 Academia de Presença")
        st.markdown("Aulas aprofundadas sobre os pilares do magnetismo pessoal.")

        aulas_presenca = [
            "Aula 1 — O que é Presença e por que poucas pessoas têm",
            "Aula 2 — A Psicologia da Primeira Impressão",
            "Aula 3 — Confiança vs Arrogância — a linha que separa os dois",
            "Aula 4 — Como Desenvolver Carisma de Forma Sistemática",
            "Aula 5 — A Ciência da Atração — o que realmente funciona",
            "Aula 6 — Humor como Ferramenta Social",
            "Aula 7 — Oratória para Sedução — como sua voz te vende",
            "Aula 8 — O Poder do Mistério — como ser interessante sem se expor demais",
            "Aula 9 — Como Liderar uma Interação com Naturalidade",
            "Aula 10 — A Arte da Tensão — quando e como criar",
            "Aula 11 — Rejeição Elegante — como transformar um não em respeito",
            "Aula 12 — Como Construir uma Vida que te Torna Mais Atraente",
            "Aula 13 — Status Social — como ele funciona e como construir o seu",
            "Aula 14 — Vulnerabilidade Estratégica — como abrir-se sem perder o charme",
            "Aula 15 — O Homem Magnético — síntese de todos os princípios",
        ]

        col_aula_p, col_nivel_p = st.columns([3, 1])
        with col_aula_p:
            aula_presenca = st.selectbox("Escolha a aula:", aulas_presenca, key="select_aula_presenca")
        with col_nivel_p:
            prof_aula = st.selectbox("Profundidade:", ["Padrão","Aprofundada"], key="select_prof_aula")

        if st.button("🎓 INICIAR AULA", key="seducaoi29"):
            with st.spinner("Preparando uma aula de verdade..."):
                nivel_instrucao = ("Esta deve ser uma aula extensa e densa, no nível de um seminário avançado."
                    if prof_aula == "Aprofundada" else "Esta deve ser uma aula completa e prática.")
                prompt = (
                    f"Você está escrevendo a melhor aula possível sobre: {aula_presenca}\n"
                    f"{nivel_instrucao} Proibido ser superficial, genérico ou usar clichês vazios. "
                    f"Cada ponto deve ter exemplo concreto, mecanismo explicado e aplicação real.\n\n"
                    f"FORMATO:\n\n"
                    f"🎓 {aula_presenca.upper()}\n\n"
                    f"📖 POR QUE ISSO IMPORTA — A REALIDADE CRUA:\n"
                    f"[abra com uma verdade sobre como a maioria dos homens age e por que eles não têm os resultados que querem — sem julgamento, com clareza]\n\n"
                    f"💡 OS PRINCÍPIOS FUNDAMENTAIS:\n"
                    f"[3-4 princípios centrais, cada um com exemplo específico e mecanismo explicado]\n\n"
                    f"🎬 ESTUDO DE CASO 1 — CENA DETALHADA:\n"
                    f"[uma situação narrada em detalhe mostrando o princípio funcionando — com diálogo real, linguagem corporal, contexto]\n\n"
                    f"🎬 ESTUDO DE CASO 2 — O CONTRASTE:\n"
                    f"[a mesma situação, mas sem o princípio — mostrando a diferença de resultado]\n\n"
                    f"⚙️ COMO DESENVOLVER — PASSO A PASSO:\n"
                    f"[instruções concretas e replicáveis, sem vagueza]\n\n"
                    f"⚠️ OS ERROS QUE SABOTAM:\n"
                    f"[o que a maioria faz que destrói o efeito]\n\n"
                    f"🏋️ MISSÃO DESTA SEMANA:\n"
                    f"[1 exercício real e específico para aplicar essa semana]\n\n"
                    f"⚡ A FRASE QUE RESUME:\n"
                    f"[1 frase poderosa e memorável que cristaliza a essência da aula]"
                )
                res = presenca_ia(prompt, "Escreva para um homem inteligente que já tentou muita coisa e não quer mais teoria vaga — ele quer o mecanismo real e como aplicar.")
                salvar_consulta("Academia", aula_presenca, res)
                st.session_state['aula_temp'] = res
                st.session_state.pontuacao_total += 15
                st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)

        if st.session_state.get('aula_temp'):
            st.markdown(f"<div class='card'>{st.session_state['aula_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar aula (.txt)", data=st.session_state['aula_temp'], file_name="aula_presenca.txt", mime="text/plain", use_container_width=True, key="seducaoi30")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_aula", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Academia','tema':aula_presenca if 'aula_presenca' in dir() else '','conteudo':st.session_state['aula_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # DESAFIO SEMANAL
        # ========================

    with _tab_Desafio:
        st.header("🏆 Desafio Semanal")
        st.markdown(f"Pontuação atual: **{st.session_state.pontuacao_total} pontos** · Nível: **{st.session_state.nivel_atual}**")

        area_desafio = st.selectbox("Área do desafio:", [
            "Confiança e presença", "Conversa e abordagem", "Linguagem corporal", "Humor e charme", "Atração e tensão",
        ], key="select_area_desafio")

        nivel_desafio = st.selectbox("Dificuldade:", ["Fácil (sai da zona de conforto um pouco)","Médio (exige coragem real)","Difícil (faz agora ou nunca)"], key="select_nivel_desafio")

        if st.button("🏆 GERAR DESAFIO DA SEMANA", key="seducaoi31"):
            with st.spinner("Criando desafio..."):
                prompt = (
                    f"Crie um desafio prático semanal.\nÁrea: {area_desafio}. Nível: {nivel_desafio}\n\n"
                    f"FORMATO:\n\n"
                    f"🏆 DESAFIO DA SEMANA — {area_desafio.upper()}\n\n"
                    f"🎯 O DESAFIO:\n[descrição clara e específica do que fazer — não vago]\n\n"
                    f"📅 QUANDO E COMO FAZER:\n[instrução de execução — dia, contexto, duração]\n\n"
                    f"🧠 POR QUE ISSO FUNCIONA:\n[o que esse desafio vai desenvolver em você]\n\n"
                    f"⚠️ A REGRA PRINCIPAL:\n[o que não pode acontecer — o que tornaria o desafio inválido]\n\n"
                    f"✅ COMO SABER SE COMPLETOU:\n[critério de sucesso claro]\n\n"
                    f"⚡ BÔNUS:\n[variação mais difícil para quem quiser ir além]"
                )
                res = presenca_ia(prompt)
                salvar_consulta("Desafio", area_desafio, res)
                st.session_state['desafio_temp'] = res
                st.session_state['desafio_completo'] = False

        if st.session_state.get('desafio_temp'):
            st.markdown(f"<div class='treino-box'>{st.session_state['desafio_temp']}</div>", unsafe_allow_html=True)

            if not st.session_state.get('desafio_completo'):
                if st.button("✅ COMPLETEI O DESAFIO", key="seducaoi32"):
                    pontos_ganhos = {"Fácil (sai da zona de conforto um pouco)": 15, "Médio (exige coragem real)": 25, "Difícil (faz agora ou nunca)": 40}
                    pts = pontos_ganhos.get(nivel_desafio if 'nivel_desafio' in dir() else "Médio (exige coragem real)", 20)
                    st.session_state.pontuacao_total += pts
                    st.session_state.treinos_completos += 1
                    st.session_state.nivel_atual = calcular_nivel(st.session_state.pontuacao_total)
                    st.session_state['desafio_completo'] = True
                    st.success(f"🔥 +{pts} pontos! Nível atual: {st.session_state.nivel_atual}")
                    st.rerun()
            else:
                st.success(f"✅ Desafio completo! Nível atual: **{st.session_state.nivel_atual}** · {st.session_state.pontuacao_total} pontos")

        # ========================
        # MENTOR 24H
        # ========================

    with _tab_Mentor:
        st.header("🤖 Mentor 24h")
        st.markdown("Converse sobre qualquer situação — o mentor fala direto ao ponto.")

        if 'chat_mentor' not in st.session_state:
            st.session_state.chat_mentor = []
        if 'mentor_key' not in st.session_state:
            st.session_state.mentor_key = 0

        if st.session_state.chat_mentor:
            for msg in st.session_state.chat_mentor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#2D1B4E;border:1px solid #7C3AED;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b style='color:#DDD6FE'>Você:</b> <span style='color:#F1F5F9'>{msg['content']}</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card' style='margin:8px 0;'><b>⚡ Mentor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div class='treino-box' style='text-align:center;'>
            ⚡ <strong>Fala. O que aconteceu?</strong><br>
            <span style='font-size:0.9em;color:#6D28D9'>Situação específica, dúvida sobre o que fazer, como responder, o que está travando você...</span>
            </div>""", unsafe_allow_html=True)

        pergunta_mentor = st.text_input("Mensagem:", key=f"mentor_input_{st.session_state.mentor_key}", placeholder="Conta o que está rolando...", label_visibility="collapsed")

        col_env, col_limpar = st.columns([4, 1])
        with col_env:
            if st.button("📤 ENVIAR", key="seducaoi33"):
                if pergunta_mentor.strip():
                    with st.spinner("..."):
                        resp = presenca_ia(pergunta_mentor, "Responda como um mentor que já passou por isso — direto, sem enrolação, com conselho real. Se a situação pedir honestidade dura, dê. Se precisar de encorajamento, dê. Fale de igual para igual.")
                    st.session_state.chat_mentor.append({"role": "user", "content": pergunta_mentor})
                    st.session_state.chat_mentor.append({"role": "assistant", "content": resp})
                    st.session_state.mentor_key += 1
                    salvar_consulta("Mentor", pergunta_mentor[:60], resp)
                    st.rerun()
        with col_limpar:
            if st.button("🗑️", key="seducaoi34"):
                st.session_state.chat_mentor = []
                st.rerun()

        # ========================
        # BIBLIOTECA
        # ========================

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#4C1D95;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Presença IA — Confiança, Charme e Oratória · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
