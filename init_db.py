"""
init_db.py – Cria e popula o banco de dados SQLite com componentes reais.
Execute uma vez antes de iniciar o servidor: python init_db.py
"""

import sqlite3
import json
import os
from dotenv import load_dotenv

load_dotenv()

nome_env = os.getenv('ADMIN_NOME')
email_env = os.getenv('ADMIN_EMAIL')
senha_env = os.getenv('ADMIN_SENHA')
DB_PATH = 'pc_builder.db'

# SCHEMA


SCHEMA = """
-- Processadores
CREATE TABLE IF NOT EXISTS processadores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    marca       TEXT    NOT NULL,
    socket      TEXT    NOT NULL,
    nucleos     INTEGER NOT NULL,
    threads     INTEGER NOT NULL,
    freq_base   REAL    NOT NULL,   -- GHz
    freq_boost  REAL,               -- GHz
    pcie_versao INTEGER NOT NULL,
    tdp_watts   INTEGER NOT NULL,
    preco       REAL
);

-- Placas-Mãe
CREATE TABLE IF NOT EXISTS placas_mae (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT    NOT NULL,
    marca        TEXT    NOT NULL,
    socket       TEXT    NOT NULL,
    chipset      TEXT    NOT NULL,
    pcie_versao  INTEGER NOT NULL,
    ddr_suporte  TEXT    NOT NULL,  -- DDR4 ou DDR5
    form_factor  TEXT    NOT NULL,  -- ATX, mATX, ITX
    preco        REAL
);

-- Placas de Vídeo (GPU)
CREATE TABLE IF NOT EXISTS gpus (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    marca       TEXT    NOT NULL,
    chip        TEXT    NOT NULL,
    pcie_versao INTEGER NOT NULL,
    vram_gb     INTEGER NOT NULL,
    tdp_watts   INTEGER NOT NULL,
    preco       REAL
);

-- Memórias RAM
CREATE TABLE IF NOT EXISTS memorias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    marca       TEXT    NOT NULL,
    tipo        TEXT    NOT NULL,  -- DDR4 ou DDR5
    capacidade  INTEGER NOT NULL,  -- GB
    velocidade  INTEGER NOT NULL,  -- MHz
    preco       REAL
);

-- Armazenamento
CREATE TABLE IF NOT EXISTS armazenamentos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    marca       TEXT    NOT NULL,
    tipo        TEXT    NOT NULL,  -- SSD NVMe, SSD SATA, HDD
    capacidade  INTEGER NOT NULL,  -- GB
    velocidade  INTEGER,           -- MB/s leitura
    preco       REAL
);

-- Refrigeração
CREATE TABLE IF NOT EXISTS refrigeracao (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    marca       TEXT    NOT NULL,
    tipo        TEXT    NOT NULL,  -- Water Cooler ou Air Cooler
    tdp         INTEGER,
    altura      INTEGER,           -- mm
    wc_fans     INTEGER,           -- caso seja WC, tamanho de fans em mm
    preco       REAL
);

-- Fontes de Alimentação
CREATE TABLE IF NOT EXISTS fontes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    marca       TEXT    NOT NULL,
    watts       INTEGER NOT NULL,
    certificacao TEXT   NOT NULL,  -- 80+ Bronze, Gold, etc.
    modular     TEXT    NOT NULL,  -- Não, Semi, Full
    preco       REAL
);

-- Gabinetes
CREATE TABLE IF NOT EXISTS gabinetes (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    marca               TEXT NOT NULL,
    tipo                TEXT NOT NULL,
    mobo_form_factor    TEXT NOT NULL,
    max_cooler          INTEGER NOT NULL,
    max_gpu             INTEGER NOT NULL,
    max_wc              INTEGER NOT NULL,
    preco               REAL
);

-- Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    senha       TEXT NOT NULL,
    is_admin    INTEGER DEFAULT 0
);


-- Relatórios Gerados (RF004)
CREATE TABLE IF NOT EXISTS relatorios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    dados_json  TEXT    NOT NULL,
    criado_em   TEXT    NOT NULL
);
"""

# DADOS DE EXEMPLO


PROCESSADORES = [
    # (nome, marca, socket, nucleos, threads, freq_base, freq_boost, pcie_versao, tdp, preco)
    ('Intel Core i5-12400F',    'Intel', 'LGA1700', 6,  12, 2.5, 4.4, 4, 65,  900.0),
    ('Intel Core i5-13600K',    'Intel', 'LGA1700', 14, 20, 3.5, 5.1, 5, 125, 1650.0),
    ('Intel Core i7-13700K',    'Intel', 'LGA1700', 16, 24, 3.4, 5.4, 5, 125, 2400.0),
    ('Intel Core i9-13900K',    'Intel', 'LGA1700', 24, 32, 3.0, 5.8, 5, 125, 3800.0),
    ('AMD Ryzen 5 5600X',       'AMD',   'AM4',     6,  12, 3.7, 4.6, 4, 65,  850.0),
    ('AMD Ryzen 5 7600X',       'AMD',   'AM5',     6,  12, 4.7, 5.3, 5, 105, 1700.0),
    ('AMD Ryzen 7 5800X',       'AMD',   'AM4',     8,  16, 3.8, 4.7, 4, 105, 1500.0),
    ('AMD Ryzen 7 7700X',       'AMD',   'AM5',     8,  16, 4.5, 5.4, 5, 105, 2200.0),
    ('AMD Ryzen 9 7950X',       'AMD',   'AM5',     16, 32, 4.5, 5.7, 5, 170, 4500.0),
    ('Intel Core i3-12100F',    'Intel', 'LGA1700', 4,  8,  3.3, 4.3, 4, 58,  550.0),
]

PLACAS_MAE = [
    # (nome, marca, socket, chipset, pcie_versao, ddr_suporte, form_factor, preco)
    ('ASUS PRIME B450M-A II',   'ASUS',      'AM4',     'B450',  3, 'DDR4', 'mATX', 450.0),
    ('Gigabyte A520M DS3H',     'Gigabyte',  'AM4',     'A520',  3, 'DDR4', 'mATX', 380.0),
    ('MSI B550 TOMAHAWK',       'MSI',       'AM4',     'B550',  4, 'DDR4', 'ATX',  900.0),
    ('ASUS ROG STRIX X570-E',   'ASUS',      'AM4',     'X570',  4, 'DDR4', 'ATX',  2200.0),
    ('ASRock B650M Pro RS',     'ASRock',    'AM5',     'B650',  5, 'DDR5', 'mATX', 1100.0),
    ('MSI MAG X670E TOMAHAWK',  'MSI',       'AM5',     'X670E', 5, 'DDR5', 'ATX',  2500.0),
    ('ASUS PRIME Z690-P',       'ASUS',      'LGA1700', 'Z690',  5, 'DDR4', 'ATX',  1400.0),
    ('MSI PRO H610M-G',         'MSI',       'LGA1700', 'H610',  4, 'DDR4', 'mATX', 600.0),
    ('Gigabyte B660M DS3H',     'Gigabyte',  'LGA1700', 'B660',  4, 'DDR4', 'mATX', 650.0),
    ('ASUS ROG MAXIMUS Z790',   'ASUS',      'LGA1700', 'Z790',  5, 'DDR5', 'ATX',  4800.0),
]

GPUS = [
    # (nome, marca, chip, pcie_versao, vram_gb, tdp_watts, preco)
    ('NVIDIA GTX 1660 Super',   'ASUS',    'TU116',  3, 6,  125, 1200.0),
    ('NVIDIA RTX 3060',         'MSI',     'GA106',  4, 12, 170, 1800.0),
    ('NVIDIA RTX 3070',         'EVGA',    'GA104',  4, 10, 220, 2800.0),
    ('NVIDIA RTX 3080',         'Gigabyte','GA102',  4, 10, 320, 3800.0),
    ('NVIDIA RTX 4060',         'Zotac',   'AD107',  4, 8,  115, 2200.0),
    ('NVIDIA RTX 4070',         'ASUS',    'AD104',  4, 12, 200, 3600.0),
    ('NVIDIA RTX 4070 Ti',      'MSI',     'AD104',  4, 12, 285, 4800.0),
    ('NVIDIA RTX 4090',         'ASUS',    'AD102',  4, 24, 450, 11000.0),
    ('AMD RX 6600 XT',          'Sapphire','Navi23', 4, 8,  160, 1600.0),
    ('AMD RX 7600',             'PowerColor','Navi33',4, 8,  165, 2000.0),
    ('AMD RX 7900 XTX',         'MSI',     'Navi31', 4, 24, 355, 7000.0),
]

MEMORIAS = [
    # (nome, marca, tipo, capacidade_gb, velocidade_mhz, preco)
    ('Kingston FURY Beast 16GB DDR4-3200', 'Kingston', 'DDR4', 16, 3200, 280.0),
    ('Corsair Vengeance LPX 32GB DDR4-3200','Corsair', 'DDR4', 32, 3200, 520.0),
    ('G.Skill Trident Z5 16GB DDR5-5600',  'G.Skill',  'DDR5', 16, 5600, 480.0),
    ('Kingston FURY Renegade 32GB DDR5-6000','Kingston','DDR5', 32, 6000, 950.0),
    ('Corsair Dominator Platinum 64GB DDR5','Corsair', 'DDR5', 64, 5600, 1800.0),
    ('Team T-Force Vulcan 16GB DDR4-3600', 'Team',     'DDR4', 16, 3600, 320.0),
    ('HyperX Fury 8GB DDR4-2666',          'HyperX',   'DDR4',  8, 2666, 150.0),
]

ARMAZENAMENTOS = [
    # (nome, marca, tipo, capacidade_gb, velocidade_mb_s, preco)
    ('WD Black SN850X 1TB NVMe',   'WD',       'SSD NVMe',  1000, 7300, 600.0),
    ('Samsung 980 Pro 1TB NVMe',   'Samsung',  'SSD NVMe',  1000, 7000, 650.0),
    ('Seagate Barracuda 2TB HDD',  'Seagate',  'HDD',       2000, 190,  250.0),
    ('Kingston NV2 500GB NVMe',    'Kingston', 'SSD NVMe',   500, 3500, 220.0),
    ('Crucial MX500 1TB SATA',     'Crucial',  'SSD SATA',  1000, 560,  400.0),
    ('WD Blue 4TB HDD',            'WD',       'HDD',       4000, 175,  380.0),
]

REFRIGERACAO = [
    # (nome, marca, tipo, tdp, altura, wc_fans, preco)
    ( 'GamerStorm X Redragon AK400', 'Redragon', 'AirCooler', 180, 155, 120, 180),
    ( 'WC Gamer Rise Mode' , 'Rise Mode' , 'WaterCooler', 220, 0, 240 , 230 ),
    ( 'WC Pichau Aqua 360X', 'Pichau', 'WaterCooler', 310, 0, 360, 255,)

]

FONTES = [
    # (nome, marca, watts, certificacao, modular, preco)
    ('Corsair CV550 550W',          'Corsair',  550,  '80+ Bronze', 'Não',   280.0),
    ('EVGA 600 BR 600W',            'EVGA',     600,  '80+ Bronze', 'Não',   350.0),
    ('Seasonic Focus GX-650 650W',  'Seasonic', 650,  '80+ Gold',   'Full',  650.0),
    ('Corsair RM750 750W',          'Corsair',  750,  '80+ Gold',   'Full',  750.0),
    ('be quiet! Straight Power 850W','be quiet',850,  '80+ Platinum','Full',  980.0),
    ('EVGA SuperNOVA 1000 G6 1000W','EVGA',    1000,  '80+ Gold',   'Full', 1300.0),
    ('Cooler Master MWE 650W',      'Cooler Master',650,'80+ Bronze','Semi',  480.0),
]

GABINETES = [
    # (nome, marca, tipo, mobo_form_factor, max_cooler, max_gpu, max_wc preco)
    ('Rise Mode Wave','Rise Mode', 'Mid Tower', 'ATX', 157, 320, 240 , 185),
    ('Wideload Lite', 'Redragon', 'Aquario', 'ATX', 175, 395, 360 ,290),

]

 
# FUNÇÕES DE CRIAÇÃO


def criar_banco():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.executescript(SCHEMA)

    # Inserir apenas se estiver vazio
    if cur.execute('SELECT COUNT(*) FROM processadores').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO processadores (nome,marca,socket,nucleos,threads,freq_base,freq_boost,pcie_versao,tdp_watts,preco) VALUES (?,?,?,?,?,?,?,?,?,?)',
            PROCESSADORES
        )
        print(f'  ✔ {len(PROCESSADORES)} processadores inseridos.')

    if cur.execute('SELECT COUNT(*) FROM placas_mae').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO placas_mae (nome,marca,socket,chipset,pcie_versao,ddr_suporte,form_factor,preco) VALUES (?,?,?,?,?,?,?,?)',
            PLACAS_MAE
        )
        print(f'  ✔ {len(PLACAS_MAE)} placas-mãe inseridas.')

    if cur.execute('SELECT COUNT(*) FROM gpus').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO gpus (nome,marca,chip,pcie_versao,vram_gb,tdp_watts,preco) VALUES (?,?,?,?,?,?,?)',
            GPUS
        )
        print(f'  ✔ {len(GPUS)} GPUs inseridas.')

    if cur.execute('SELECT COUNT(*) FROM memorias').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO memorias (nome,marca,tipo,capacidade,velocidade,preco) VALUES (?,?,?,?,?,?)',
            MEMORIAS
        )
        print(f'  ✔ {len(MEMORIAS)} memórias inseridas.')

    if cur.execute('SELECT COUNT(*) FROM armazenamentos').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO armazenamentos (nome,marca,tipo,capacidade,velocidade,preco) VALUES (?,?,?,?,?,?)',
            ARMAZENAMENTOS
        )
        print(f'  ✔ {len(ARMAZENAMENTOS)} armazenamentos inseridos.')
    
    if cur.execute('SELECT COUNT(*) FROM refrigeracao').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO refrigeracao (nome, marca, tipo, tdp, altura, wc_fans, preco) VALUES (?,?,?,?,?,?,?)',
            REFRIGERACAO
        )
        print(f'✔ {len(REFRIGERACAO)} refrigeracao inseridos.')

    if cur.execute('SELECT COUNT(*) FROM fontes').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO fontes (nome,marca,watts,certificacao,modular,preco) VALUES (?,?,?,?,?,?)',
            FONTES
        )
        print(f'  ✔ {len(FONTES)} fontes inseridas.')

    if cur.execute('SELECT COUNT(*) FROM gabinetes').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO gabinetes (nome, marca, tipo, mobo_form_factor, max_cooler, max_gpu, max_wc, preco) VALUES (?,?,?,?,?,?,?,?)',
            GABINETES
        )
        print(f'  ✔ {len(GABINETES)} gabinetes inseridos.')

    cur.execute('INSERT INTO usuarios VALUES (?,?,?,?,?)',
                (None,nome_env,email_env,senha_env,1))
    

    conn.commit()
    conn.close()
    print('\n✅ Banco de dados criado com sucesso em:', DB_PATH)


if __name__ == '__main__':
    print('🗄️  Inicializando banco de dados...')
    criar_banco()
