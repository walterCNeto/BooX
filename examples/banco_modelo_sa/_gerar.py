# -*- coding: utf-8 -*-
"""
Gerador do Banco Modelo S.A. — instancia de exemplo do BooX.
Banco multiplo S2 ficticio. Books em VOCABULARIO LOCAL; B_MAP traduz -> canonico.
Roda: python _gerar.py   (gera os CSVs dos 9 Books do Lite + B_MAP)
Dados 100% sinteticos. Ver ../../LICENSE-DATA.
"""
import csv, os, random
random.seed(42)
AQUI = os.path.dirname(os.path.abspath(__file__))

def escrever(nome, cab, linhas):
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(cab); w.writerows(linhas)
    print(f"  {nome}: {len(linhas)} linhas")

# ---------------------------------------------------------------------
# RISCOS LOCAIS (com sabor de marca) -> canonico
# (id, nome_local, canonico, disciplina_local)
# ---------------------------------------------------------------------
RISCOS = [
 ("RL-01","Inadimplencia e perda de credito","R0.U.1","CREDITO"),
 ("RL-02","Risco de mercado da carteira","R0.U.2","MERCADO"),
 ("RL-03","Descasamento e risco de liquidez","R0.U.3","LIQUIDEZ"),
 ("RL-04","Risco de juros da carteira banking","R0.U.4","JUROS"),
 ("RL-05","Exposicao cambial","R0.U.5","MERCADO"),
 ("RL-06","Falha operacional de processamento","R0.U.6","OPERACIONAL"),
 ("RL-07","Risco de Invasao Digital","R0.U.7","CYBER"),
 ("RL-08","Erro de modelo de credito","R0.U.8","MODELO"),
 ("RL-09","Indisponibilidade de sistemas","R0.U.9","BIA"),
 ("RL-10","Falha de fornecedor critico","R0.U.10","FORNECEDORES"),
 ("RL-11","Nao conformidade regulatoria","R0.U.11","CONFORMIDADE"),
 ("RL-12","Venda inadequada ao cliente","R0.U.12","CONDUTA"),
 ("RL-13","Lavagem de dinheiro","R0.U.13","LD"),
 ("RL-14","Vazamento de dados pessoais","R0.U.14","LGPD"),
 ("RL-15","Dano reputacional","R0.U.15","REPUTACIONAL"),
 ("RL-16","Fraude externa em canais","R0.U.6","FRAUDE"),
 ("RL-17","Fraude interna","R0.U.6","FRAUDE"),
]
# AREAS LOCAIS -> canonico
AREAS = [
 ("AL-VAR","Diretoria Varejo Mais","ORG.NEG.VAR"),
 ("AL-DIA","Segmento Diamante","ORG.NEG.ALT"),
 ("AL-EMP","Empresas e Negocios","ORG.NEG.EMP"),
 ("AL-CPF","Credito Pessoa Fisica","ORG.CRE.CPF"),
 ("AL-CPJ","Credito Pessoa Juridica","ORG.CRE.CPJ"),
 ("AL-COB","Recuperacao e Cobranca","ORG.CRE.REC"),
 ("AL-CAD","Central de Cadastro","ORG.OPE.CAD"),
 ("AL-CAM","Mesa de Cambio","ORG.OPE.CAM"),
 ("AL-TES","Tesouraria","ORG.TES.ALM"),
 ("AL-CORE","TI Core Banking","ORG.TEC.COR"),
 ("AL-CYBER","Nucleo Cyber","ORG.TEC.SI"),
 ("AL-INFRA","Infraestrutura de TI","ORG.TEC.INF"),
 ("AL-DICOI","DICOI","ORG.CIN.CTI"),
 ("AL-DPLD","DPLD","ORG.CIN.PLD"),
 ("AL-COMPL","Compliance Regulatorio","ORG.CIN.COM"),
 ("AL-LGPD","Encarregado de Dados (DPO)","ORG.CIN.LGP"),
 ("AL-RISCO","Risco Operacional","ORG.RIS.OPE"),
 ("AL-RCRED","Risco de Credito","ORG.RIS.CRE"),
 ("AL-AUDIT","Auditoria Interna","ORG.AUD.NEG"),
 ("AL-OUVID","Ouvidoria","ORG.OUV.OUV"),
]
DISC_NOME = {"CREDITO":"Credito","MERCADO":"Mercado","LIQUIDEZ":"Liquidez",
 "JUROS":"Taxa de Juros","OPERACIONAL":"Operacional","CYBER":"Cyber",
 "MODELO":"Modelo","BIA":"Continuidade","FORNECEDORES":"Fornecedores",
 "CONFORMIDADE":"Conformidade","CONDUTA":"Conduta","LD":"Lavagem de Dinheiro",
 "LGPD":"Privacidade e LGPD","REPUTACIONAL":"Reputacional","FRAUDE":"Fraude"}

# ---------------------------------------------------------------------
# B1 PROCESSOS (hierarquia local P0->P2)
# (id, nome, nivel, nucleo, parent, area_local)
# ---------------------------------------------------------------------
PROCESSOS = [
 ("P.NEG","Negocios e Comercial",0,"B","","AL-VAR"),
 ("P.NEG.VAR","Atendimento Varejo PF",1,"B","P.NEG","AL-VAR"),
 ("P.NEG.ALT","Atendimento Alta Renda",1,"B","P.NEG","AL-DIA"),
 ("P.NEG.EMP","Atendimento Empresas",1,"B","P.NEG","AL-EMP"),
 ("P.NEG.VEN","Venda e oferta de produtos",2,"B","P.NEG.VAR","AL-VAR"),
 ("P.CRE","Credito",0,"B","","AL-CPF"),
 ("P.CRE.PF","Concessao de credito PF",1,"B","P.CRE","AL-CPF"),
 ("P.CRE.PJ","Concessao de credito PJ",1,"B","P.CRE","AL-CPJ"),
 ("P.CRE.CON","Credito consignado INSS",2,"B","P.CRE.PF","AL-CPF"),
 ("P.CRE.IMO","Credito imobiliario",2,"B","P.CRE.PF","AL-CPF"),
 ("P.CRE.COB","Recuperacao e cobranca",1,"B","P.CRE","AL-COB"),
 ("P.OPE","Operacoes",0,"U","","AL-CAD"),
 ("P.OPE.CAD","Cadastro e KYC",1,"U","P.OPE","AL-CAD"),
 ("P.OPE.CAM","Operacoes de cambio",1,"B","P.OPE","AL-CAM"),
 ("P.OPE.LIQ","Liquidacao e processamento",1,"U","P.OPE","AL-CORE"),
 ("P.TES","Tesouraria",0,"B","","AL-TES"),
 ("P.TES.ALM","Gestao de liquidez (ALM)",1,"B","P.TES","AL-TES"),
 ("P.TES.MES","Mesa proprietaria",1,"MC","P.TES","AL-TES"),
 ("P.TEC","Tecnologia",0,"U","","AL-CORE"),
 ("P.TEC.COR","Operacao do core banking",1,"U","P.TEC","AL-CORE"),
 ("P.TEC.CAN","Canais digitais",1,"U","P.TEC","AL-CORE"),
 ("P.TEC.SI","Seguranca da informacao",1,"U","P.TEC","AL-CYBER"),
 ("P.TEC.INF","Infraestrutura e nuvem",1,"U","P.TEC","AL-INFRA"),
 ("P.CIN","Controles e Compliance",0,"U","","AL-COMPL"),
 ("P.CIN.PLD","Prevencao a lavagem (PLD-FT)",1,"U","P.CIN","AL-DPLD"),
 ("P.CIN.CON","Conformidade regulatoria",1,"U","P.CIN","AL-COMPL"),
 ("P.CIN.LGP","Privacidade e protecao de dados",1,"U","P.CIN","AL-LGPD"),
 ("P.CIN.CTI","Controles internos",1,"U","P.CIN","AL-DICOI"),
]

def g_b1():
    L=[]
    for pid,nome,niv,nuc,par,area in PROCESSOS:
        bia = 5 if niv>=1 and any(k in pid for k in ["CRE","SI","PLD","COR","CAD"]) else (4 if niv>=1 else "")
        L.append([pid,pid,nome,niv,nuc,par,nome,area,"","",bia])
    escrever("B1_processos.csv",
     ["id","codigo","nome","nivel","nucleo","parent_id","descricao","owner_area","entrada","saida","criticidade_bia"],L)

def g_b6_riscos():
    L=[]
    for rid,nome,canon,disc in RISCOS:
        L.append([rid,rid,nome,0,"U","","","DISC_"+disc,f"Risco local mapeado para {canon}"])
    escrever("B6_riscos.csv",
     ["id","codigo","nome","nivel","nucleo","parent_id","categoria_basileia","disciplina_id","descricao"],L)

# ---------------------------------------------------------------------
# B6 VINCULO PROCESSO x RISCO (a tabela central — cada linha = 1 bolha)
# (processo, risco, materialidade, area_afetada, area_gestora, gest_e_afet)
# ---------------------------------------------------------------------
VINCULOS = [
 ("P.CRE.PF","RL-01",5,"AL-CPF","AL-RCRED",0),
 ("P.CRE.PJ","RL-01",5,"AL-CPJ","AL-RCRED",0),
 ("P.CRE.CON","RL-01",4,"AL-CPF","AL-RCRED",0),
 ("P.CRE.CON","RL-12",4,"AL-CPF","AL-COMPL",0),
 ("P.CRE.IMO","RL-01",4,"AL-CPF","AL-RCRED",0),
 ("P.CRE.PF","RL-08",3,"AL-RCRED","AL-RCRED",1),
 ("P.CRE.COB","RL-01",3,"AL-COB","AL-RCRED",0),
 ("P.CRE.COB","RL-12",3,"AL-COB","AL-COMPL",0),
 ("P.TES.ALM","RL-03",5,"AL-TES","AL-TES",1),
 ("P.TES.ALM","RL-04",3,"AL-TES","AL-TES",1),
 ("P.TES.MES","RL-02",4,"AL-TES","AL-TES",1),
 ("P.OPE.CAM","RL-05",3,"AL-CAM","AL-TES",0),
 ("P.OPE.CAD","RL-13",5,"AL-CAD","AL-DPLD",0),
 ("P.OPE.CAD","RL-14",4,"AL-CAD","AL-LGPD",0),
 ("P.OPE.CAD","RL-06",3,"AL-CAD","AL-RISCO",0),
 ("P.OPE.LIQ","RL-06",4,"AL-CORE","AL-RISCO",0),
 ("P.OPE.LIQ","RL-09",4,"AL-CORE","AL-INFRA",0),
 ("P.NEG.VEN","RL-12",4,"AL-VAR","AL-COMPL",0),
 ("P.NEG.VEN","RL-15",3,"AL-VAR","AL-OUVID",0),
 ("P.NEG.ALT","RL-12",3,"AL-DIA","AL-COMPL",0),
 ("P.TEC.SI","RL-07",5,"AL-CYBER","AL-CYBER",1),
 ("P.TEC.CAN","RL-07",4,"AL-CORE","AL-CYBER",0),
 ("P.TEC.CAN","RL-16",4,"AL-CORE","AL-RISCO",0),
 ("P.TEC.COR","RL-09",5,"AL-CORE","AL-INFRA",0),
 ("P.TEC.INF","RL-09",4,"AL-INFRA","AL-INFRA",1),
 ("P.TEC.INF","RL-10",3,"AL-INFRA","AL-INFRA",1),
 ("P.TEC.CAN","RL-14",4,"AL-CORE","AL-LGPD",0),
 ("P.CIN.PLD","RL-13",5,"AL-DPLD","AL-DPLD",1),
 ("P.CIN.CON","RL-11",4,"AL-COMPL","AL-COMPL",1),
 ("P.CIN.LGP","RL-14",4,"AL-LGPD","AL-LGPD",1),
 ("P.CIN.CTI","RL-11",3,"AL-DICOI","AL-DICOI",1),
 ("P.OPE.LIQ","RL-17",3,"AL-CORE","AL-AUDIT",0),
 ("P.CRE.PF","RL-16",3,"AL-CPF","AL-RISCO",0),
 ("P.TES.MES","RL-08",3,"AL-TES","AL-RISCO",0),
]
def g_b6_vinc():
    L=[]
    for i,(p,r,m,af,ge,fa) in enumerate(VINCULOS,1):
        L.append([i,p,r,m,"CRO",af,ge,fa,""])
    escrever("B6_vinculo_processo_risco.csv",
     ["id","processo_id","risco_id","materialidade_inerente","materialidade_declarada_por",
      "area_afetada","area_gestora","eh_gestora_e_afetada","notas"],L)

print("Gerando Banco Modelo S.A. (parte estrutural)...")
g_b1(); g_b6_riscos(); g_b6_vinc()

# ---------------------------------------------------------------------
# B5 CONTROLES (5W2H) — um ou mais por vinculo critico
# ---------------------------------------------------------------------
# (id, acao, tipo, risco, processo, resp, local, freq, mec, como, cob, nat, ef_auto, ef_val, status_val)
CONTROLES = [
 ("CT-001","Comite de credito aprova operacoes acima de limite","credito","RL-01","P.CRE.PJ","AL-RCRED","Comite + sistema","semanal","manual","Voto qualificado",100,"preventivo",4,3,"validado_amostral"),
 ("CT-002","Motor de decisao automatizado com score","credito","RL-01","P.CRE.PF","AL-CPF","Esteira digital","continuo","automatico","Score + politica",100,"preventivo",4,4,"validado_amostral"),
 ("CT-003","Validacao independente anual do modelo","modelo","RL-08","P.CRE.PF","AL-RCRED","MRM","anual","manual","Backtesting",100,"detectivo",3,2,"validado_documentalmente"),
 ("CT-004","Limites de VaR e stop loss na mesa","mercado","RL-02","P.TES.MES","AL-TES","Sistema de risco","diario","automatico","Monitor intraday",100,"preventivo",4,4,"validado_completo"),
 ("CT-005","Monitoramento de gaps de liquidez","liquidez","RL-03","P.TES.ALM","AL-TES","ALM","diario","semi","Fluxo de caixa projetado",100,"detectivo",4,4,"validado_amostral"),
 ("CT-006","Monitoramento transacional PLD","operacional","RL-13","P.CIN.PLD","AL-DPLD","Sistema PLD","continuo","automatico","Regras + listas",90,"detectivo",3,2,"validado_amostral"),
 ("CT-007","Verificacao KYC na abertura","operacional","RL-13","P.OPE.CAD","AL-CAD","Onboarding","por_evento","semi","Documentos + consultas",95,"preventivo",3,2,"apenas_autoavaliado"),
 ("CT-008","SOC 24x7 e resposta a incidentes","operacional","RL-07","P.TEC.SI","AL-CYBER","SOC","continuo","automatico","SIEM + alertas",85,"detectivo",4,3,"validado_amostral"),
 ("CT-009","Gestao de acessos privilegiados","operacional","RL-07","P.TEC.CAN","AL-CYBER","IAM","continuo","semi","Revisao trimestral",70,"preventivo",3,"","apenas_autoavaliado"),
 ("CT-010","Plano de continuidade e DR testado","operacional","RL-09","P.TEC.COR","AL-INFRA","PCN","semestral","manual","Testes de failover",80,"corretivo",3,2,"validado_documentalmente"),
 ("CT-011","Dupla checagem na liquidacao","operacional","RL-06","P.OPE.LIQ","AL-CORE","Backoffice","diario","manual","Maker-checker",100,"preventivo",4,3,"validado_amostral"),
 ("CT-012","Selo de suitability na venda","operacional","RL-12","P.NEG.VEN","AL-COMPL","CRM","por_evento","semi","Perfil + alerta",80,"preventivo",3,2,"apenas_autoavaliado"),
 ("CT-013","Antifraude em canais digitais","operacional","RL-16","P.TEC.CAN","AL-CYBER","Antifraude","continuo","automatico","Device + comportamento",90,"detectivo",4,3,"validado_amostral"),
 ("CT-014","Mapa de privacidade e base legal","operacional","RL-14","P.CIN.LGP","AL-LGPD","RoPA","anual","manual","Inventario de dados",60,"preventivo",3,"","apenas_autoavaliado"),
 ("CT-015","Criptografia de dados sensiveis","operacional","RL-14","P.TEC.CAN","AL-CYBER","Plataforma","continuo","automatico","Em transito e repouso",75,"preventivo",3,2,"validado_documentalmente"),
 ("CT-016","Pauta regulatoria semanal","operacional","RL-11","P.CIN.CON","AL-COMPL","Compliance","semanal","manual","Triagem normativa",90,"preventivo",4,3,"validado_amostral"),
 ("CT-017","Limite cambial e hedge","mercado","RL-05","P.OPE.CAM","AL-TES","Mesa","diario","semi","Exposicao liquida",100,"preventivo",4,3,"validado_amostral"),
 ("CT-018","Politica de cobranca e renegociacao","credito","RL-01","P.CRE.COB","AL-COB","Sistema cobranca","mensal","semi","Reguas de cobranca",90,"corretivo",3,2,"apenas_autoavaliado"),
 ("CT-019","Due diligence de fornecedores criticos","operacional","RL-10","P.TEC.INF","AL-INFRA","GRC fornecedores","anual","manual","Avaliacao + SLA",70,"preventivo",3,"","apenas_autoavaliado"),
 ("CT-020","Conciliacao diaria de retaguarda","operacional","RL-06","P.OPE.CAD","AL-CAD","Backoffice","diario","semi","Batimento de bases",85,"detectivo",3,2,"apenas_autoavaliado"),
]
def g_b5():
    L=[[c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14]] for c in CONTROLES]
    escrever("B5_controles.csv",
     ["id","acao","tipo","risco_id","processo_id","responsavel","local","frequencia",
      "mecanismo","como","cobertura_pct","natureza","eficacia_autoavaliada","eficacia_validada","status_validacao"],L)

# ---------------------------------------------------------------------
# B2 APONTAMENTOS — mix realista, concentrados nos pares mais fracos
# ---------------------------------------------------------------------
def g_b2():
    L=[]; n=1
    # apontamentos "plantados" para criar gradiente no 20-box
    plantados = [
      ("RL-07","P.TEC.CAN","critico","aberto","auditoria","CT-009"),
      ("RL-07","P.TEC.CAN","alto","em_tratamento","controles_internos","CT-009"),
      ("RL-07","P.TEC.SI","alto","aberto","auditoria","CT-008"),
      ("RL-13","P.OPE.CAD","critico","aberto","regulador","CT-007"),
      ("RL-13","P.OPE.CAD","alto","em_tratamento","compliance","CT-007"),
      ("RL-13","P.CIN.PLD","alto","aberto","auditoria","CT-006"),
      ("RL-14","P.CIN.LGP","alto","aberto","compliance","CT-014"),
      ("RL-14","P.OPE.CAD","medio","aberto","controles_internos",""),
      ("RL-12","P.CRE.CON","critico","aberto","regulador","CT-012"),
      ("RL-12","P.NEG.VEN","alto","vencido","compliance","CT-012"),
      ("RL-12","P.CRE.COB","medio","em_tratamento","ouvidoria",""),
      ("RL-01","P.CRE.PJ","medio","aberto","controles_internos","CT-001"),
      ("RL-01","P.CRE.COB","alto","aberto","auditoria","CT-018"),
      ("RL-09","P.TEC.COR","alto","em_tratamento","gestao","CT-010"),
      ("RL-09","P.OPE.LIQ","medio","aberto","controles_internos",""),
      ("RL-06","P.OPE.LIQ","medio","aberto","auditoria","CT-011"),
      ("RL-06","P.OPE.CAD","medio","fechado","controles_internos","CT-020"),
      ("RL-11","P.CIN.CON","medio","em_tratamento","regulador","CT-016"),
      ("RL-10","P.TEC.INF","alto","aberto","controles_internos","CT-019"),
      ("RL-08","P.CRE.PF","alto","aberto","auditoria","CT-003"),
      ("RL-16","P.TEC.CAN","medio","em_tratamento","gestao","CT-013"),
      ("RL-05","P.OPE.CAM","baixo","aberto","controles_internos","CT-017"),
      ("RL-15","P.NEG.VEN","baixo","aberto","ouvidoria",""),
    ]
    titulos={"RL-07":"Deficiencia em controle cibernetico","RL-13":"Lacuna em monitoramento PLD",
     "RL-14":"Gap de privacidade","RL-12":"Falha de suitability na venda","RL-01":"Fragilidade em concessao",
     "RL-09":"Indisponibilidade de servico","RL-06":"Falha de processamento","RL-11":"Desvio de conformidade",
     "RL-10":"Risco de fornecedor","RL-08":"Desvio de modelo","RL-16":"Fraude em canal","RL-05":"Exposicao cambial",
     "RL-15":"Reclamacao reputacional"}
    base_ano=2025
    for r,p,sev,st,orig,ctrl in plantados:
        mes=random.randint(6,12); dia=random.randint(1,28)
        ab=f"{base_ano}-{mes:02d}-{dia:02d}"
        prazo=f"2026-{random.randint(2,8):02d}-28"
        fech=f"2026-{random.randint(1,4):02d}-15" if st=="fechado" else ""
        L.append([f"AP-2025-{n:04d}",titulos.get(r,"Apontamento"),
          f"{titulos.get(r,'Apontamento')} no processo {p}",orig,sev,st,p,r,ctrl,ab,prazo,fech,"Area responsavel"])
        n+=1
    escrever("B2_apontamentos.csv",
     ["id","titulo","descricao","origem","severidade","status","processo_id","risco_id",
      "controle_id","data_abertura","data_prazo","data_fechamento","responsavel"],L)

# ---------------------------------------------------------------------
# B10 INDICADORES (KRIs) + serie temporal
# ---------------------------------------------------------------------
KRIS = [
 # (id, nome, risco, processo, disc, unidade, direcao, amarelo, vermelho, meta, perfil)
 ("KRI-01","Inadimplencia 90d PF","RL-01","P.CRE.PF","CREDITO","%","menor_melhor",2.0,4.0,1.5,"sobe"),
 ("KRI-02","Inadimplencia 90d PJ","RL-01","P.CRE.PJ","CREDITO","%","menor_melhor",2.5,5.0,2.0,"estavel"),
 ("KRI-03","Tentativas de intrusao com sucesso","RL-07","P.TEC.CAN","CYBER","qtd","menor_melhor",2,5,0,"sobe"),
 ("KRI-04","Alertas PLD nao tratados no prazo","RL-13","P.OPE.CAD","LD","%","menor_melhor",5,10,2,"sobe"),
 ("KRI-05","Disponibilidade do core banking","RL-09","P.TEC.COR","BIA","%","maior_melhor",99.5,99.0,99.9,"desce"),
 ("KRI-06","Reclamacoes de venda inadequada","RL-12","P.NEG.VEN","CONDUTA","qtd","menor_melhor",20,40,10,"sobe"),
 ("KRI-07","Incidentes de vazamento de dados","RL-14","P.CIN.LGP","LGPD","qtd","menor_melhor",1,3,0,"estavel"),
 ("KRI-08","Perdas operacionais (R$ mil)","RL-06","P.OPE.LIQ","OPERACIONAL","R$mil","menor_melhor",200,500,100,"estavel"),
 ("KRI-09","VaR utilizado vs limite","RL-02","P.TES.MES","MERCADO","%","menor_melhor",70,90,50,"estavel"),
 ("KRI-10","Gap de liquidez 30d","RL-03","P.TES.ALM","LIQUIDEZ","%","maior_melhor",110,100,130,"estavel"),
 ("KRI-11","Fraude externa (R$ mil)","RL-16","P.TEC.CAN","FRAUDE","R$mil","menor_melhor",150,400,80,"sobe"),
 ("KRI-12","Apontamentos vencidos","RL-11","P.CIN.CON","CONFORMIDADE","qtd","menor_melhor",3,8,0,"estavel"),
 ("KRI-13","Cobertura de testes de controle","RL-06","P.CIN.CTI","OPERACIONAL","%","maior_melhor",70,50,90,"desce"),
 ("KRI-14","SLA de fornecedor critico","RL-10","P.TEC.INF","FORNECEDORES","%","maior_melhor",95,90,99,"estavel"),
 ("KRI-15","Acuracia do modelo de credito","RL-08","P.CRE.PF","MODELO","%","maior_melhor",75,70,85,"desce"),
 ("KRI-16","Exposicao cambial liquida","RL-05","P.OPE.CAM","MERCADO","%","menor_melhor",10,20,5,"estavel"),
]
def serie(perfil, amarelo, vermelho, direcao):
    meses=["2025-07","2025-08","2025-09","2025-10","2025-11","2025-12"]
    if direcao=="menor_melhor":
        base=amarelo*0.6
        if perfil=="sobe": vals=[base*(1+0.18*i) for i in range(6)]
        elif perfil=="desce": vals=[vermelho*(1-0.05*i) for i in range(6)]
        else: vals=[base*(1+random.uniform(-0.1,0.1)) for _ in range(6)]
    else:
        base=amarelo*1.05
        if perfil=="desce": vals=[base*(1-0.02*i) for i in range(6)]
        elif perfil=="sobe": vals=[vermelho*(1+0.02*i) for i in range(6)]
        else: vals=[base*(1+random.uniform(-0.02,0.02)) for _ in range(6)]
    return list(zip(meses,[round(v,2) for v in vals]))
def g_b10():
    L=[]; S=[]
    for k in KRIS:
        kid,nome,r,p,disc,uni,dire,am,ver,meta,perfil=k
        L.append([kid,nome,nome,r,p,"DISC_"+disc,uni,dire,am,ver,meta])
        for comp,val in serie(perfil,am,ver,dire):
            S.append([kid,comp,val])
    escrever("B10_indicadores.csv",
     ["id","nome","descricao","risco_id","processo_id","disciplina_id","unidade","direcao","limite_amarelo","limite_vermelho","meta"],L)
    escrever("B10_indicador_serie.csv",["indicador_id","competencia","valor"],S)

# ---------------------------------------------------------------------
# B8 EXTERNOS — sinais publicos vinculados a riscos/disciplinas
# ---------------------------------------------------------------------
def g_b8():
    L=[
     ["EXT-001","bacen","procedente","Procedentes sobre cobranca indevida","RL-12","","DISC_CONDUTA","",18,"","","","2025-12-31","2025-Q4"],
     ["EXT-002","bacen","procedente","Procedentes sobre oferta de credito","RL-01","","DISC_CREDITO","",9,"","","","2025-12-31","2025-Q4"],
     ["EXT-003","bacen","ranking_reclamacoes","Posicao no ranking de reclamacoes","RL-15","","DISC_REPUTACIONAL",3,"","","","","2025-12-31","2025-Q4"],
     ["EXT-004","cvm","processo_em_curso","PAS sobre suitability","RL-12","","DISC_CONDUTA","",1,"em_curso","","","2025-11-20","2025-Q4"],
     ["EXT-005","procon","procedente","Reclamacoes Procon sobre cobranca","RL-12","","DISC_CONDUTA","",12,"","","","2025-12-31","2025-Q4"],
     ["EXT-006","midia","noticia_adversa","Reportagem sobre vazamento de dados","RL-14","","DISC_LGPD",4,1,"","","","2025-10-15","2025-Q4"],
     ["EXT-007","midia","noticia_adversa","Materia sobre golpe em canal digital","RL-16","","DISC_FRAUDE",3,1,"","","","2025-11-05","2025-Q4"],
     ["EXT-008","reclame_aqui","nota_periodo","Nota geral do periodo","RL-15","","DISC_REPUTACIONAL","",1,"",6.4,7.1,"2025-12-31","2025-Q4"],
     ["EXT-009","anbima","carta_recomendacao","Carta sobre distribuicao","RL-12","","DISC_CONDUTA","",2,"","","","2025-09-30","2025-Q3"],
     ["EXT-010","bacen","procedente","Procedentes sobre conta e cadastro","RL-06","","DISC_OPERACIONAL","",6,"","","","2025-12-31","2025-Q4"],
    ]
    escrever("B8_externos.csv",
     ["id","fonte","tipo","descricao","risco_id","processo_id","disciplina_id","severidade",
      "quantidade","status","valor_metrica","valor_anterior","data","periodo"],L)

# ---------------------------------------------------------------------
# B4 REGULACAO + vinculo
# ---------------------------------------------------------------------
def g_b4():
    N=[
     ["RES_CMN_4557","res_cmn","4557","2017","CMN","Gerenciamento de riscos e capital","Estrutura de gerenciamento de riscos","vigente",""],
     ["RES_BCB_265","res_bcb","265","2022","BCB","Risco operacional","Gerenciamento continuo de risco operacional","vigente",""],
     ["RES_CMN_4658","res_cmn","4658","2018","CMN","Politica de seguranca cibernetica","Ciberseguranca e nuvem","vigente",""],
     ["LEI_13709","lei","13709","2018","Congresso","LGPD","Protecao de dados pessoais","vigente",""],
     ["LEI_9613","lei","9613","1998","Congresso","Lavagem de dinheiro","PLD-FT","vigente",""],
     ["CIRC_BCB_3978","circ_bcb","3978","2020","BCB","PLD-FT","Politica de prevencao a lavagem","vigente",""],
     ["RES_CVM_30","res_cvm","30","2021","CVM","Suitability","Dever de verificacao de adequacao","vigente",""],
     ["RES_CMN_4753","res_cmn","4753","2019","CMN","Continuidade de negocios","Politica de continuidade","vigente",""],
    ]
    escrever("B4_regulacao.csv",
     ["id","tipo","numero","ano","regulador","titulo","ementa","status","url_oficial"],N)
    V=[
     [1,"RES_CMN_4557","risco","RL-06","primaria",""],
     [2,"RES_BCB_265","risco","RL-06","primaria",""],
     [3,"RES_CMN_4658","risco","RL-07","primaria",""],
     [4,"LEI_13709","risco","RL-14","primaria",""],
     [5,"LEI_9613","risco","RL-13","primaria",""],
     [6,"CIRC_BCB_3978","risco","RL-13","primaria",""],
     [7,"RES_CVM_30","risco","RL-12","primaria",""],
     [8,"RES_CMN_4753","risco","RL-09","primaria",""],
    ]
    escrever("B4_vinculo_norma.csv",["id","norma_id","alvo_tipo","alvo_id","tipo_vinculo","notas"],V)

# ---------------------------------------------------------------------
# B9 DISCIPLINAS (subconjunto usado, referenciando canonico)
# ---------------------------------------------------------------------
def g_b9():
    usados=sorted({"DISC_"+r[3] for r in RISCOS})
    L=[]
    for d in usados:
        nome=DISC_NOME.get(d.replace("DISC_",""),d)
        L.append([d,nome,f"Disciplina {nome}","operacional","",""])
    escrever("B9_disciplinas.csv",
     ["id","nome","descricao","categoria_basileia","responsavel_2linha",""][:5],L)

# ---------------------------------------------------------------------
# B7 VISOES + filtros
# ---------------------------------------------------------------------
def g_b7():
    V=[
     ["VIS_CASA","Casa toda","livre","Visao consolidada de todos os riscos","CRO",""],
     ["VIS_CONSIGNADO","Consignado INSS","produto","Risco do produto consignado ponta a ponta","AL-CPF",""],
     ["VIS_CYBER_LGPD","Cyber e LGPD","disciplina","Seguranca cibernetica e privacidade","AL-CYBER",""],
     ["VIS_CREDITO","Credito E2E","e2e","Todo o ciclo de credito","AL-RCRED",""],
     ["VIS_CONDUTA","Conduta e Suitability","disciplina","Conduta de mercado e venda","AL-COMPL",""],
    ]
    escrever("B7_visoes.csv",["id","nome","tipo","descricao","owner","regra_afetacao"],V)
    F=[
     ["VIS_CONSIGNADO","processo","prefixo","P.CRE.CON"],
     ["VIS_CONSIGNADO","processo","prefixo","P.CRE.COB"],
     ["VIS_CYBER_LGPD","disciplina","em","DISC_CYBER|DISC_LGPD"],
     ["VIS_CREDITO","disciplina","igual","DISC_CREDITO"],
     ["VIS_CREDITO","processo","prefixo","P.CRE"],
     ["VIS_CONDUTA","disciplina","igual","DISC_CONDUTA"],
    ]
    escrever("B7_visao_filtros.csv",["visao_id","dimensao","operador","valor"],F)

# ---------------------------------------------------------------------
# B_MAP — de-para
# ---------------------------------------------------------------------
def g_bmap():
    L=[]; n=1
    for rid,nome,canon,_ in RISCOS:
        conf="media" if nome.lower().startswith("risco") else "alta"
        L.append([f"MAP-{n:03d}","risco",nome,rid,canon,conf,"similaridade",
                  f"{nome} -> {canon}","aprovado","Equipe RO","2026-01-15",""]); n+=1
    for aid,nome,canon in AREAS:
        metodo="llm" if len(nome)<=6 else "similaridade"
        conf="media" if metodo=="llm" else "alta"
        L.append([f"MAP-{n:03d}","organizacao",nome,aid,canon,conf,metodo,
                  f"{nome} -> {canon}","aprovado","Equipe RO","2026-01-15",""]); n+=1
    escrever("B_MAP_taxonomia.csv",
     ["id","dominio","termo_local","termo_local_id","canonico_id","confianca_ia",
      "metodo","justificativa","status","aprovado_por","data_revisao","notas"],L)

g_b5(); g_b2(); g_b10(); g_b8(); g_b4(); g_b9(); g_b7(); g_bmap()
print("Banco Modelo S.A. gerado com sucesso.")
