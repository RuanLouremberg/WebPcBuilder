# 🖥️ PC Builder — Analisador de Compatibilidade
> Laboratório de Software

Sistema web para análise de compatibilidade de componentes de hardware,
com foco em gargalos de barramento PCIe e comunicação clara ao usuário final.

---

## 📁 Estrutura do Projeto

```
pc_builder/
├── .env
├── app.py              # Backend Flask (rotas e lógica de análise)
├── init_db.py          # Inicialização do banco SQLite com dados
├── requirements.txt    # Dependência: Flask
├── pc_builder.db       # Banco SQLite (gerado automaticamente)
├── templates/
│  └── base.html        # Frontend HTML + JavaScript
│  └── cadastro_peca.html
│  └── cadastro_usuario.html
│  └── index.html
│  └── landing.html
│  └── login.html
└── static/
    └── style.css
    └── style2.css       # Estilização CSS
```

---

## ▶️ Como Executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Inicializar o banco de dados (apenas na primeira vez)
```bash
python init_db.py
```

### 3. Iniciar o servidor
```bash
python app.py
```

### 4. Acessar no navegador
```
http://localhost:5000
```

---

## 🔗 Endpoints da API

| Método | Rota                       | Descrição                            |
|--------|----------------------------|--------------------------------------|
| GET    | `/`                        | Página principal                     |
| GET    | `/api/componentes/<tipo>`  | Lista componentes por tipo           |
| POST   | `/api/analisar`            | Analisa compatibilidade do setup     |
| GET    | `/api/relatorios`          | Histórico dos últimos relatórios     |
| GET    | `/api/relatorios/<id>`     | Detalhe de um relatório específico   |

**Tipos de componente aceitos:** `processador`, `placa_mae`, `gpu`, `memoria`, `armazenamento`, `fonte`

---

## 📋 Requisitos Atendidos

| Código  | Descrição                                                        | Implementado em          |
|---------|------------------------------------------------------------------|--------------------------|
| RF001   | Seleção de componentes individuais                               | `app.py` + `index.html`  |
| RF002   | Análise de compatibilidade de barramento PCIe                    | `app.py` → `/api/analisar` |
| RF003   | Identificação e alerta de gargalos técnicos                      | `app.py` + alertas visuais |
| RF004   | Relatório detalhado com justificativa de perda de desempenho     | `app.py` → tabela `relatorios` |
| RNF001  | Plataforma web acessível por navegadores modernos                | Flask + HTML/CSS         |
| RNF002  | Resposta em até 5 segundos                                       | Análise local (< 1s)     |
| RNF003  | Alertas visuais (cores) para indicar nível de gargalo            | `style.css` (verde/amarelo/vermelho) |
| RNF004  | Integridade dos dados técnicos                                   | SQLite + validação na API |
| RN001   | Aviso obrigatório de "Redução de Largura de Banda" PCIe 3.0/4.0 | `app.py` → código `RN001` |
| RN002   | Prioridade ao menor barramento na cadeia                         | `min(pcie_mobo, pcie_gpu)` |
| RN003   | Exigir ciência do usuário antes de finalizar                     | Checkbox + botão bloqueado |

---

## 🗄️ Modelo do Banco de Dados (SQLite)

```
processadores  (id, nome, marca, socket, nucleos, threads, freq_base, pcie_versao, tdp_watts, preco)
placas_mae     (id, nome, marca, socket, chipset, pcie_versao, ddr_suporte, form_factor, preco)
gpus           (id, nome, marca, chip, pcie_versao, vram_gb, tdp_watts, preco)
memorias       (id, nome, marca, tipo, capacidade, velocidade, preco)
armazenamentos (id, nome, marca, tipo, capacidade, velocidade, preco)
refrigeracao   (id,nome, marca, tipo, tdp, altura, wc_fans, preco)
fontes         (id, nome, marca, watts, certificacao, modular, preco)
gabinetes      (id,nome, marca, tipo, mobo_form_factor, max_cooler, max_gpu, max_wc preco)
relatorios     (id, dados_json, criado_em)
```
