"""
PC Builder - Analisador de Compatibilidade
Backend Flask com SQLite
Laboratório de Software
"""

from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import sqlite3
import sqlite3 as sql
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'adm123'

DB_PATH = 'pc_builder.db'

# ---------------------------
# CONEXÃO COM BANCO DE DADOS
# ---------------------------

def get_db():
    """Retorna conexão com o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn


# ----------
# ROTAS DE INTERFACE
# ----------

@app.route('/')
def landing():
    """Página principal."""
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return render_template('landing.html')

@app.route('/builder')
def index():
    """Página principal do PC Builder (antiga index)."""
    # Protege a rota: só entra se estiver logado
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


# ----------
# API: LISTAR COMPONENTES
# ----------

TABELAS = {
    'processador':    'processadores',
    'placa_mae':      'placas_mae',
    'gpu':            'gpus',
    'memoria':        'memorias',
    'armazenamento':  'armazenamentos',
    'refrigeracao':   'refrigeracao',
    'fonte':          'fontes',
    'gabinete':       'gabinetes'
}

@app.route('/api/componentes/<tipo>')
def get_componentes(tipo):
    """RF001 – Retorna lista de componentes por tipo."""
    tabela = TABELAS.get(tipo)
    if not tabela:
        return jsonify({'erro': f'Tipo inválido: {tipo}'}), 400

    conn = get_db()
    rows = conn.execute(f'SELECT * FROM {tabela} ORDER BY nome').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    """Rota para cadastrar novos usuários comuns."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        con = get_db()
        try:
            # is_admin por padrão é 0 (usuário comum)
            con.execute('INSERT INTO usuarios (nome, email, senha, is_admin) VALUES (?, ?, ?, 0)', 
                        (nome, email, senha))
            con.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('cadastro_usuario.html', erro='Email já cadastrado!')
        finally:
            con.close()
            
    return render_template('cadastro_usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    req = request.form
    if request.method == 'POST':
        email = req.get('email')
        senha = req.get('senha')
        
        con = sql.connect('pc_builder.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?',
                    (email,senha))
        user = cur.fetchone()
        con.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nome']
            session['is_admin'] = bool(user['is_admin'])

            return redirect(url_for('index'))
        
        return render_template('login.html', erro="E-mail ou senha incorretos!"), 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    """Limpa a sessão e desloga o usuário."""
    session.clear()
    return redirect(url_for('landing'))

# -- Cadastro de peças ----------------
@app.route('/cadastro_peca', methods = ['POST', 'GET'])
def cadastrar():
    req = request.form
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        req = request.form
        categoria = req.get('categoria')

        # características base
        nome = req.get('nome')
        marca = req.get('marca')
        preco = req.get('preco')


        # conexão com banco de dados
        con = sql.connect('pc_builder.db')
        cur = con.cursor()

        # características específicas da peça
        if categoria == 'processadores':
            socket = req.get('socket')
            nucleos = req.get('nucleos')
            threads = req.get('threads')
            freq_base = req.get('freq_base')
            freq_boost = req.get('freq_boost')
            pcie_versao = req.get('pcie_versao')
            tdp_watts = req.get('tdp_watts')

            cur.execute('INSERT INTO processadores VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                    (None,nome,marca,socket,nucleos,threads,freq_base,freq_boost,pcie_versao,tdp_watts,preco))
            
            
        elif categoria == 'placas_mae':
            socket_mae = req.get('socket_mae')
            chipset = req.get('chipset')
            pciemb_versao = req.get('pciemb_versao')
            ddr_suporte = req.get('ddr_suporte')
            form_factor = req.get('form_factor')

            cur.execute('INSERT INTO placas_mae VALUES (?,?,?,?,?,?,?,?,?)',
                        (None,nome,marca,socket_mae,chipset,pciemb_versao,ddr_suporte,form_factor,preco))
            
        
        elif categoria == 'gpus':
            chip = req.get('chip')
            pciegpu_versao = req.get('pciegpu_versao')
            vram_gb = req.get('vram_gb')
            tdp_gpu = req.get('tdp_gpu')
            

            cur.execute('INSERT INTO gpus VALUES (?,?,?,?,?,?,?,?)',
                        (None,nome,marca,chip,pciegpu_versao,vram_gb,tdp_gpu,preco))
            
            
        elif categoria == 'memorias':
            tipo_ram = req.get('tipo_ram')
            capacidade_ram = req.get('capacidade_ram')
            velocidade_ram = req.get('velocidade_ram')

            cur.execute('INSERT INTO memorias VALUES (?,?,?,?,?,?,?)',
                        (None,nome,marca,tipo_ram,capacidade_ram,velocidade_ram,preco))
            
            
        elif categoria == 'armazenamentos':
            tipo_disco = req.get('tipo_disco')
            capacidade_disco = req.get('capacidade_disco')
            velocidade_disco = req.get('velocidade_disco')

            cur.execute('INSERT INTO armazenamentos VALUES (?,?,?,?,?,?,?)',
                        (None,nome,marca,tipo_disco,capacidade_disco,velocidade_disco,preco))
            
            
        elif categoria == 'refrigeracao':
            tipo_cooler = req.get('tipo_cooler')
            tdp_cooler = req.get('tdp_cooler')
            altura_cooler = req.get('altura_cooler')
            wc_fans = req.get('wc_fans')

            cur.execute('INSERT INTO refrigeracao VALUES (?,?,?,?,?,?,?,?)',
                        (None,nome,marca,tipo_cooler,tdp_cooler,altura_cooler,wc_fans,preco))
            
            
        elif categoria == 'fontes':
            watts = req.get('watts')
            certificacao = req.get('certificacao')
            modular = req.get('modular')

            cur.execute('INSERT INTO fontes VALUES (?,?,?,?,?,?,?)',
                        (None,nome,marca,watts,certificacao,modular,preco))
            
            
        elif categoria == 'gabinetes':
            tipo_gabinete = req.get('tipo_gabinete')
            mobo_suporte = req.get('mobo_suporte')
            max_cooler = req.get('max_cooler')
            max_gpu = req.get('max_gpu')
            max_wc = req.get('max_wc')

            cur.execute('INSERT INTO gabinetes VALUES (?,?,?,?,?,?,?,?,?)',
                        (None,nome,marca,tipo_gabinete,mobo_suporte,max_cooler,max_gpu,max_wc,preco))
        con.commit()    
        con.close()

        return redirect(url_for('cadastrar'))
    return render_template('index.html')

# APi: ANALISAR COMPATIBILIDADE


@app.route('/api/analisar', methods=['POST'])
def analisar():
    """
    RF002, RF003, RF004 – Analisa a compatibilidade do setup.
    Recebe: { processador_id, placa_mae_id, gpu_id, memoria_id, armazenamento_id, refrigeracao_id, fonte_id, gabinete_id }
    Retorna: relatório completo com alertas, score e recomendações.
    """
    dados = request.get_json(silent=True) or {}

    conn = get_db()

    # ---------- Buscar componentes selecionados ----------
    def buscar(tabela, cid):
        if not cid:
            return None
        row = conn.execute(f'SELECT * FROM {tabela} WHERE id = ?', (cid,)).fetchone()
        return dict(row) if row else None

    cpu   = buscar('processadores', dados.get('processador_id'))
    mobo  = buscar('placas_mae',    dados.get('placa_mae_id'))
    gpu   = buscar('gpus',          dados.get('gpu_id'))
    ram   = buscar('memorias',      dados.get('memoria_id'))
    disco = buscar('armazenamentos',dados.get('armazenamento_id'))
    refrigeracao = buscar('refrigeracao', dados.get('refrigeracao_id'))
    fonte = buscar('fontes',        dados.get('fonte_id'))
    gabinete = buscar('gabinetes',dados.get('gabinete_id'))

    # ---------- Análise de compatibilidade ----------
    alertas = []
    score   = 100  # pontuação de performance (0–100)

    # ---------- RN001 / RN002: PCIe entre Placa-mãe e GPU ----------
    if mobo and gpu:
        pcie_mobo = int(mobo.get('pcie_versao', 3))
        pcie_gpu  = int(gpu.get('pcie_versao',  4))
        pcie_efetivo = min(pcie_mobo, pcie_gpu)  # RN002: menor da cadeia

        if pcie_gpu > pcie_mobo:
            # Largura de banda por versão (GB/s, x16)
            larguras = {3: 16, 4: 32, 5: 64}
            bw_real = larguras.get(pcie_mobo, 16)
            bw_max  = larguras.get(pcie_gpu,  32)
            perda_bw = round((1 - bw_real / bw_max) * 100)
            score   -= perda_bw // 2

            alertas.append({
                'nivel':    'aviso',          # amarelo
                'codigo':   'RN001',
                'titulo':   'Redução de Largura de Banda PCIe',
                'descricao': (
                    f'A GPU <strong>{gpu["nome"]}</strong> é nativa PCIe {pcie_gpu}.0, '
                    f'mas a placa-mãe <strong>{mobo["nome"]}</strong> suporta apenas PCIe {pcie_mobo}.0. '
                    f'A largura de banda será limitada a {bw_real} GB/s de {bw_max} GB/s disponíveis '
                    f'(perda estimada de <strong>~{perda_bw}%</strong> de banda).'
                ),
                'perda_percentual': perda_bw,
            })

    # ---------- Compatibilidade de Socket (CPU + Mobo) ----------
    if cpu and mobo:
        socket_cpu  = cpu.get('socket', '').strip().upper()
        socket_mobo = mobo.get('socket', '').strip().upper()
        if socket_cpu and socket_mobo and socket_cpu != socket_mobo:
            score = 0
            alertas.append({
                'nivel':    'critico',        # vermelho
                'codigo':   'SOCKET',
                'titulo':   'Socket Incompatível',
                'descricao': (
                    f'O processador <strong>{cpu["nome"]}</strong> usa socket <strong>{socket_cpu}</strong>, '
                    f'mas a placa-mãe <strong>{mobo["nome"]}</strong> aceita socket <strong>{socket_mobo}</strong>. '
                    'Estes componentes <strong>não são fisicamente compatíveis</strong>.'
                ),
                'perda_percentual': 100,
            })

    # ---------- Compatibilidade de RAM (tipo DDR) ----------
    if mobo and ram:
        ddr_mobo = mobo.get('ddr_suporte', '').upper()
        ddr_ram  = ram.get('tipo', '').upper()
        if ddr_mobo and ddr_ram and ddr_mobo != ddr_ram:
            score = 0
            alertas.append({
                'nivel':    'critico',
                'codigo':   'DDR',
                'titulo':   'Tipo de Memória Incompatível',
                'descricao': (
                    f'A memória selecionada é <strong>{ddr_ram}</strong>, '
                    f'mas a placa-mãe suporta <strong>{ddr_mobo}</strong>. '
                    'O pente de memória não encaixará fisicamente.'
                ),
                'perda_percentual': 100,
            })

    # ---- Verificar Fonte (consumo estimado)-----------------
    consumo_total = 50 #consumo de energia base
    if cpu:
        consumo_total += int(cpu.get('tdp_watts', 0))
    if gpu:
        consumo_total += int(gpu.get('tdp_watts', 0))
    

    if fonte:
        watts_fonte = int(fonte.get('watts', 0))
        if watts_fonte < consumo_total:
            score -= 30
            alertas.append({
                'nivel':    'critico',
                'codigo':   'FONTE',
                'titulo':   'Fonte de Energia Insuficiente',
                'descricao': (
                    f'O consumo estimado do sistema é de <strong>~{consumo_total}W</strong>, '
                    f'mas a fonte selecionada fornece apenas <strong>{watts_fonte}W</strong>. '
                    'O sistema pode sofrer instabilidades ou não ligar.'
                ),
                'perda_percentual': 100,
            })
        elif watts_fonte < consumo_total * 1.2:
            alertas.append({
                'nivel':    'atencao',        # laranja
                'codigo':   'FONTE_MARGEM',
                'titulo':   'Margem de Segurança da Fonte Baixa',
                'descricao': (
                    f'A fonte tem {watts_fonte}W e o consumo estimado é ~{consumo_total}W. '
                    'Recomenda-se uma margem de 20% acima do consumo total para estabilidade.'
                ),
                'perda_percentual': 20,
            })
    
    # ---------- Verificar Tamanho do gabinete para Air Cooler ----------
    if refrigeracao.get('tipo', 0) == 'AirCooler':
        tam_cooler = int(refrigeracao.get('altura', 0))
        max_gabinete = int(gabinete.get('max_cooler', 0))
        if tam_cooler > max_gabinete:
            score -= 80
            alertas.append({
                'nivel':    'critico',
                'codigo':   'ALTURA_COOLER',
                'titulo':   'Tamanho do gabinete Insuficiente',
                'descricao': (
                    f'''O Air Cooler tem {tam_cooler}mm de altura, e o gabinete suporta
                    apenas {max_gabinete}mm'''
                ),
                'perda_percentual': 80
            })
     # ---------- Verificar Tamanho do gabinete para Water Cooler ----------

    elif refrigeracao.get('tipo', 0) == 'WaterCooler':
        max_wc = refrigeracao.get('wc_fans', 0)
        max_gab = gabinete.get('max_wc', 0)
        if max_wc > max_gab:
            score -= 80
            alertas.append({
                'nivel':    'critico',
                'codigo':   'TAMANHO_WC',
                'titulo':   'Tamanho do gabinete insuficiente',
                'descricao':    (
                    f'''O Water cooler selecionado tem {max_wc}mm, e o gabinete selecionado suporta
                    apenas {max_gab}mm.'''
                    ),
                    'perda percentual': 80
            })



    # ---------- Garantir score entre 0 e 100 ----------
    score = max(0, min(100, score))

    # ---------- Gerar recomendações ----------
    recomendacoes = _gerar_recomendacoes(alertas, cpu, mobo, gpu, fonte, refrigeracao, gabinete, consumo_total)

    # ---------- Montar relatório final ----------
    relatorio = {
        'timestamp':        datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'componentes': {
            'processador':    cpu,
            'placa_mae':      mobo,
            'gpu':            gpu,
            'memoria':        ram,
            'armazenamento':  disco,
            'refrigeracao':   refrigeracao,
            'fonte':          fonte,
            'gabinete':       gabinete,
        },
        'alertas':              alertas,
        'score_performance':    score,
        'consumo_estimado_w':   consumo_total,
        'recomendacoes':        recomendacoes,
    }

    # ---------- Persistir no banco (RF004) ----------
    cur = conn.execute(
        'INSERT INTO relatorios (dados_json, criado_em) VALUES (?, ?)',
        (json.dumps(relatorio, ensure_ascii=False), datetime.now().isoformat())
    )
    conn.commit()
    relatorio['id'] = cur.lastrowid
    conn.close()

    return jsonify(relatorio)



# API: HISTÓRICO DE RELATÓRIOS


@app.route('/api/relatorios')
def listar_relatorios():
    """Retorna histórico dos últimos 10 relatórios gerados."""
    conn = get_db()
    rows = conn.execute(
        'SELECT id, criado_em, dados_json FROM relatorios ORDER BY id DESC LIMIT 10'
    ).fetchall()
    conn.close()

    resultado = []
    for r in rows:
        dados = json.loads(r['dados_json'])
        resultado.append({
            'id':           r['id'],
            'criado_em':    r['criado_em'],
            'score':        dados.get('score_performance', 0),
            'total_alertas': len(dados.get('alertas', [])),
        })
    return jsonify(resultado)


@app.route('/api/relatorios/<int:rid>')
def get_relatorio(rid):
    """Retorna um relatório específico pelo ID."""
    conn = get_db()
    row = conn.execute('SELECT dados_json FROM relatorios WHERE id = ?', (rid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'erro': 'Relatório não encontrado'}), 404
    return jsonify(json.loads(row['dados_json']))



# LÓGICA DE RECOMENDAÇÕES


def _gerar_recomendacoes(alertas, cpu, mobo, gpu, fonte, refrigeracao, gabinete, consumo):
    """Gera recomendações textuais baseadas nos alertas detectados."""
    recs = []
    codigos = {a['codigo'] for a in alertas}

    if 'RN001' in codigos and gpu:
        pcie_gpu = gpu.get('pcie_versao', 4)
        recs.append(
            f'Para aproveitar 100% do potencial da GPU, considere uma placa-mãe com suporte a PCIe {pcie_gpu}.0.'
        )
        recs.append(
            'Em jogos a 1080p, a diferença real de FPS entre PCIe 3.0 e 4.0 costuma ser de 2–5%. '
            'Em workloads de renderização e IA, a perda pode ser mais significativa.'
        )

    if 'SOCKET' in codigos:
        recs.append('Escolha um processador e uma placa-mãe com o mesmo socket para garantir compatibilidade física.')

    if 'DDR' in codigos:
        recs.append('Selecione memórias RAM do mesmo padrão DDR suportado pela placa-mãe.')

    if 'FONTE' in codigos:
        recs.append(
            f'Para o consumo estimado de ~{consumo}W, recomenda-se uma fonte com pelo menos {round(consumo * 1.25 / 50) * 50}W (margem de 25%).'
        )

    if 'FONTE_MARGEM' in codigos:
        recs.append(
            'Considere uma fonte com maior capacidade para garantir estabilidade e longevidade dos componentes.'
        )
    
    if 'ALTURA_COOLER' in codigos:
        recs.append(
            f'Considere um gabinete com maior altura máxima de torre de air cooler. Ou considere um air cooler com torre menor.'
        )
    if 'TAMANHO_WC' in codigos:
        recs.append(
            f'Considere um gabinete com capacidade para water cooler de 360mm. Ou considere um water cooler menor.'
        )

    if not alertas:
        recs.append('Nenhum gargalo ou incompatibilidade detectada. Configuração equilibrada e pronta para uso!')

    return recs



# INICIALIZAÇÃO


if __name__ == '__main__':
    print("🖥️  PC Builder rodando em http://localhost:5000")
    app.run(debug=True, port=5000)