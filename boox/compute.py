# -*- coding: utf-8 -*-
"""BooX engine — leitura dos Books, resolucao via B_MAP, e calculo do score."""
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
        # de-para risco local -> canonico
        self.canon = {m["termo_local_id"]: m["canonico_id"]
                      for m in self.bmap if m["dominio"] == "risco"
                      and m["status"] in ("aprovado", "ajustado")}
        # disciplina por risco
        self.disc_by_risco = {r["id"]: r.get("disciplina_id", "") for r in self.riscos}
        # status do KRI mais recente + tendencia
        self.kri_status = {}
        serie_por_kri = {}
        for s in self.serie:
            serie_por_kri.setdefault(s["indicador_id"], []).append(s)
        for k in self.indicadores:
            vals = sorted(serie_por_kri.get(k["id"], []), key=lambda x: x["competencia"])
            if not vals: continue
            atual = _num(vals[-1]["valor"]); am = _num(k["limite_amarelo"]); ver = _num(k["limite_vermelho"])
            menor = k["direcao"] == "menor_melhor"
            if menor:
                st = "vermelho" if atual >= ver else ("amarelo" if atual >= am else "verde")
            else:
                st = "vermelho" if atual <= ver else ("amarelo" if atual <= am else "verde")
            tend = "estavel"
            if len(vals) >= 3:
                ini = _num(vals[0]["valor"]); delta = atual - ini
                if menor: tend = "piora" if delta > abs(ini)*0.1 else "estavel"
                else: tend = "piora" if delta < -abs(ini)*0.05 else "estavel"
            self.kri_status[(k["processo_id"], k["risco_id"])] = self.kri_status.get((k["processo_id"], k["risco_id"]), [])
            self.kri_status[(k["processo_id"], k["risco_id"])].append((st, tend))

    # ---- componentes do score X (0-100, alto = pior) ----
    def _f_apont(self, p, r):
        base = {"critico":4.0,"alto":2.0,"medio":1.0,"baixo":0.5}
        tot = 0.0
        for a in self.apontamentos:
            if a["processo_id"]==p and a["risco_id"]==r and a["status"]!="fechado":
                c = base.get(a["severidade"],0.5)
                if a["origem"]=="regulador": c*=2
                if a["status"]=="vencido": c+=1.5
                tot+=c
        return min(tot*5.0, 45)

    def _f_ctrl(self, p, r):
        pesos={"apenas_autoavaliado":(1.0,0.0),"validado_documentalmente":(0.7,0.3),
               "validado_amostral":(0.4,0.6),"validado_completo":(0.1,0.9)}
        defs=[]
        for c in self.controles:
            if c["processo_id"]==p and c["risco_id"]==r:
                pa,pv=pesos.get(c["status_validacao"],(1.0,0.0))
                ea=_num(c["eficacia_autoavaliada"],3)
                ev=_num(c["eficacia_validada"],ea)
                if not c["eficacia_validada"]: ef=ea
                else: ef=pa*ea+pv*ev
                defs.append(5-ef)
        if not defs: return 18.0
        return (sum(defs)/len(defs))*6.0

    def _f_kri(self, p, r):
        tot=0.0
        for st,tend in self.kri_status.get((p,r),[]):
            if st=="vermelho": tot+=3.0
            elif st=="amarelo": tot+=1.0
            if tend=="piora": tot+=1.0
        return min(tot*2.5, 22)

    def _f_ext(self, p, r):
        disc=self.disc_by_risco.get(r,"")
        tot=0.0
        caps={"bacen":6.0,"cvm":6.0,"anbima":3.0,"procon":3.0,"midia":4.0,"reclame_aqui":2.0}
        acc={}
        for e in self.externos:
            casa = (e["risco_id"]==r) or (e["disciplina_id"] and e["disciplina_id"]==disc)
            if not casa: continue
            f=e["fonte"]; q=_num(e["quantidade"],1)
            if f=="bacen": c=0.5*q
            elif f=="cvm": c=(2.0 if e["status"]=="julgado" else 1.0)*q
            elif f=="anbima": c=0.3*q
            elif f=="procon": c=0.3*q
            elif f=="midia": c=1.0*q if _num(e["severidade"])>=4 else 0.4*q
            elif f=="reclame_aqui":
                queda=_num(e["valor_anterior"])-_num(e["valor_metrica"])
                c=2.0 if queda>=0.5 else 0.0
            else: c=0.0
            acc[f]=min(acc.get(f,0)+c, caps.get(f,3.0))
        return min(sum(acc.values()), 25)

    def _f_cobertura(self, p, r):
        # par tem sinal proprio?
        tem = any(a["processo_id"]==p and a["risco_id"]==r for a in self.apontamentos) \
           or any(c["processo_id"]==p and c["risco_id"]==r for c in self.controles) \
           or bool(self.kri_status.get((p,r)))
        return 0.0 if tem else 8.0

    def computar(self):
        res=[]
        for v in self.vinculos:
            p=v["processo_id"]; r=v["risco_id"]
            mat=_num(v["materialidade_inerente"],3)
            score_y=[0.5,1.5,2.5,3.5,4.5][int(mat)-1] if 1<=int(mat)<=5 else 2.5
            sx=self._f_apont(p,r)+self._f_ctrl(p,r)+self._f_kri(p,r)+self._f_ext(p,r)+self._f_cobertura(p,r)
            sx=max(0,min(sx,100))
            res.append({
                "processo_id":p,"risco_id":r,
                "processo_nome":self.proc_by_id.get(p,{}).get("nome",p),
                "risco_nome":self.risco_by_id.get(r,{}).get("nome",r),
                "risco_canonico":self.canon.get(r,r),
                "disciplina":self.disc_by_risco.get(r,""),
                "area_afetada":v.get("area_afetada",""),"area_gestora":v.get("area_gestora",""),
                "materialidade":int(mat),"score_y":round(score_y,2),"score_x":round(sx,1),
                "nivel_y":self._nivel_y(score_y),"nivel_x":self._nivel_x(sx),
                "prioridade":self._prioridade(self._nivel_y(score_y),self._nivel_x(sx)),
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
         ["Medio","Medio","Baixo","Baixo","OK"],       # Imaterial
         ["Medio","Medio","Baixo","Baixo","OK"],       # Baixo  (linha base)
         ["Alto","Medio","Medio","Baixo","Baixo"],     # Medio
         ["Critico","Alto","Medio","Medio","Baixo"],   # Alto
         ["Critico","Critico","Alto","Medio","Medio"], # Elevado
        ]
        # ajuste linha Baixo conforme matriz definida
        M[1]=["Medio","Medio","Baixo","Baixo","OK"]
        return M[Y][X]

def carregar(pasta): return Instancia(pasta)
