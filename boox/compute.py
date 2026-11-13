# -*- coding: utf-8 -*-
"""BooX engine v0.2 — leitura dos Books, resolucao via B_MAP, e calculo do score.

v0.2 — mudancas metodologicas:
- Eixo X baseado APENAS em apontamentos + controles + cobertura.
- KRIs e sinais externos NAO pesam direto no score; sao fontes potenciais
  de apontamento (veja alertas_descobertura).
- Cobertura por par (0-100%) vira dimensao de primeira classe, derivada
  do status_validacao dos controles (Interpretacao A).
"""
import csv, os

def _ler(caminho):
    if not os.path.exists(caminho): return []
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))

def _num(v, d=0.0):
    try: return float(str(v).replace(",", "."))
    except: return d

class Instancia:
    def __init__(self, pasta):
        self.pasta = pasta
        g = lambda n: _ler(os.path.join(pasta, n))
        self.processos = g("B1_processos.csv")
        self.riscos = g("B6_riscos.csv")
        self.vinculos = g("B6_vinculo_processo_risco.csv")
        self.controles = g("B5_controles.csv")
        self.apontamentos = g("B2_apontamentos.csv")
        self.indicadores = g("B10_indicadores.csv")
        self.serie = g("B10_indicador_serie.csv")
        self.externos = g("B8_externos.csv")
        self.visoes = g("B7_visoes.csv")
        self.filtros = g("B7_visao_filtros.csv")
        self.bmap = g("B_MAP_taxonomia.csv")
        self._indexar()

    def _indexar(self):
        self.proc_by_id = {p["id"]: p for p in self.processos}
        self.risco_by_id = {r["id"]: r for r in self.riscos}
        self.canon = {m["termo_local_id"]: m["canonico_id"]
                      for m in self.bmap if m.get("dominio") == "risco"
                      and m.get("status") in ("aprovado", "ajustado")}
        self.disc_by_risco = {r["id"]: r.get("disciplina_id", "") for r in self.riscos}
        self.kri_status = {}
        serie_por_kri = {}
        for s in self.serie:
            serie_por_kri.setdefault(s["indicador_id"], []).append(s)
        for k in self.indicadores:
            vals = sorted(serie_por_kri.get(k["id"], []), key=lambda x: x["competencia"])
            if not vals: continue
            atual = _num(vals[-1]["valor"]); am = _num(k.get("limite_amarelo")); ver = _num(k.get("limite_vermelho"))
            menor = k.get("direcao") == "menor_melhor"
            if menor:
                st = "vermelho" if atual >= ver else ("amarelo" if atual >= am else "verde")
            else:
                st = "vermelho" if atual <= ver else ("amarelo" if atual <= am else "verde")
            tend = "estavel"
            if len(vals) >= 3:
                ini = _num(vals[0]["valor"]); delta = atual - ini
                if menor: tend = "piora" if delta > abs(ini)*0.1 else "estavel"
                else: tend = "piora" if delta < -abs(ini)*0.05 else "estavel"
            key = (k.get("processo_id",""), k.get("risco_id",""))
            self.kri_status.setdefault(key, []).append((st, tend))

    # ---- componentes do score X (0-100, alto = pior) ----
    def _f_apont(self, p, r):
        base = {"critico":4.0,"alto":2.0,"medio":1.0,"baixo":0.5}
        tot = 0.0
        for a in self.apontamentos:
            if a.get("processo_id")==p and a.get("risco_id")==r and a.get("status")!="fechado":
                c = base.get(a.get("severidade"),0.5)
                if a.get("origem")=="regulador": c*=2
                if a.get("status")=="vencido": c+=1.5
                tot+=c
        return min(tot*5.0, 45)

    def _f_ctrl(self, p, r):
        pesos={"apenas_autoavaliado":(1.0,0.0),"validado_documentalmente":(0.7,0.3),
               "validado_amostral":(0.4,0.6),"validado_completo":(0.1,0.9)}
        defs=[]
        for c in self.controles:
            if c.get("processo_id")==p and c.get("risco_id")==r:
                pa,pv=pesos.get(c.get("status_validacao"),(1.0,0.0))
                ea=_num(c.get("eficacia_autoavaliada"),3)
                ev=_num(c.get("eficacia_validada"),ea)
                if not c.get("eficacia_validada"): ef=ea
                else: ef=pa*ea+pv*ev
                defs.append(5-ef)
        if not defs: return 18.0
        return (sum(defs)/len(defs))*6.0

    def _f_cobertura(self, p, r):
        # par tem apontamento OU controle declarado?
        tem = any(a.get("processo_id")==p and a.get("risco_id")==r for a in self.apontamentos) \
           or any(c.get("processo_id")==p and c.get("risco_id")==r for c in self.controles)
        return 0.0 if tem else 8.0

    def _cobertura_par(self, p, r):
        """Interpretacao A: cobertura = media ponderada de status_validacao dos controles.
        apenas_autoavaliado=25, doc=50, amostral=75, completo=100. Sem controle = 0."""
        pesos = {"apenas_autoavaliado":25,"validado_documentalmente":50,
                 "validado_amostral":75,"validado_completo":100}
        vals = []
        for c in self.controles:
            if c.get("processo_id")==p and c.get("risco_id")==r:
                vals.append(pesos.get(c.get("status_validacao","apenas_autoavaliado"),25))
        if not vals: return 0
        return round(sum(vals)/len(vals))

    def alertas_descobertura(self):
        """Sinais (KRI vermelho/amarelo, externos relevantes) sem apontamento associado.
        Cada item e uma 'decisao pendente': abrir apontamento ou justificar."""
        alertas = []
        def tem_apont(p, r):
            return any(a.get("processo_id")==p and a.get("risco_id")==r and a.get("status")!="fechado"
                       for a in self.apontamentos)
        # KRIs vermelho/amarelo
        for (p, r), lst in self.kri_status.items():
            if not p or not r: continue
            for st, tend in lst:
                if st in ("vermelho","amarelo") and not tem_apont(p, r):
                    alertas.append({"tipo":"kri","par":(p,r),
                                    "detalhe":f"KRI {st}" + (" e em piora" if tend=="piora" else "")})
                    break
        # externos relevantes
        for e in self.externos:
            r = e.get("risco_id","")
            disc = e.get("disciplina_id","")
            fonte = e.get("fonte","")
            qtd = _num(e.get("quantidade",""))
            sev = _num(e.get("severidade",""))
            relevante = False
            if fonte in ("bacen","procon","ouvidoria") and qtd >= 5: relevante = True
            elif fonte == "cvm" and qtd >= 1: relevante = True
            elif fonte == "anbima" and qtd >= 1: relevante = True
            elif fonte == "midia" and sev >= 4: relevante = True
            elif fonte == "sac" and qtd >= 20: relevante = True
            if not relevante: continue
            pares = []
            for v in self.vinculos:
                if r and v.get("risco_id") == r:
                    pares.append((v["processo_id"], v["risco_id"]))
                elif not r and disc and self.disc_by_risco.get(v.get("risco_id","")) == disc:
                    pares.append((v["processo_id"], v["risco_id"]))
            for p, rr in pares:
                if not tem_apont(p, rr):
                    alertas.append({"tipo":"externo","par":(p,rr),
                                    "detalhe":f"{fonte}: {e.get('descricao','sinal')[:60]}"})
        return alertas

    def computar(self):
        res=[]
        for v in self.vinculos:
            p=v["processo_id"]; r=v["risco_id"]
            mat=_num(v.get("materialidade_inerente"),3)
            score_y=[0.5,1.5,2.5,3.5,4.5][int(mat)-1] if 1<=int(mat)<=5 else 2.5
            sx = self._f_apont(p,r) + self._f_ctrl(p,r) + self._f_cobertura(p,r)
            sx = max(0, min(sx, 100))
            cob = self._cobertura_par(p, r)
            res.append({
                "processo_id":p,"risco_id":r,
                "processo_nome":self.proc_by_id.get(p,{}).get("nome",p),
                "risco_nome":self.risco_by_id.get(r,{}).get("nome",r),
                "risco_canonico":self.canon.get(r,r),
                "disciplina":self.disc_by_risco.get(r,""),
                "area_afetada":self.proc_by_id.get(p,{}).get("area_responsavel",""),
                "area_gestora":self.proc_by_id.get(p,{}).get("area_responsavel",""),
                "materialidade":int(mat),"score_y":round(score_y,2),"score_x":round(sx,1),
                "nivel_y":self._nivel_y(score_y),"nivel_x":self._nivel_x(sx),
                "prioridade":self._prioridade(self._nivel_y(score_y),self._nivel_x(sx)),
                "cobertura_pct":cob,
            })
        return res

    @staticmethod
    def _nivel_y(s):
        return ["Imaterial","Baixo","Medio","Alto","Elevado"][min(int(s),4)]
    @staticmethod
    def _nivel_x(s):
        if s<20: return "++"
        if s<40: return "+"
        if s<60: return "0"
        if s<80: return "-"
        return "--"
    @staticmethod
    def _prioridade(ny,nx):
        Y=["Imaterial","Baixo","Medio","Alto","Elevado"].index(ny)
        X=["--","-","0","+","++"].index(nx)
        M=[
         ["Medio","Medio","Baixo","Baixo","OK"],
         ["Medio","Medio","Baixo","Baixo","OK"],
         ["Alto","Medio","Medio","Baixo","Baixo"],
         ["Critico","Alto","Medio","Medio","Baixo"],
         ["Critico","Critico","Alto","Medio","Medio"],
        ]
        return M[Y][X]

def carregar(pasta): return Instancia(pasta)
