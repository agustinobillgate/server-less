#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_pprice, L_lieferant, L_order

def pchase_book_btn_go_1bl(sorttype:int, f_date:date, t_date:date, to_dt:date, mi_ch:string, mi_call:string, s_artnr:int):

    prepare_cache ([L_artikel, L_pprice, L_lieferant, L_order])

    pchase_list_list = []
    tmpart:int = 0
    l_artikel = l_pprice = l_lieferant = l_order = None

    pchase_list = l_art = l_ppr = l_lief = None

    pchase_list_list, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":string, "docu_nr":string, "traubensort":string, "lief_einheit":Decimal, "betriebsnr":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "remark":string, "artnr":int, "bezeich":string})

    L_art = create_buffer("L_art",L_artikel)
    L_ppr = create_buffer("L_ppr",L_pprice)
    L_lief = create_buffer("L_lief",L_lieferant)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_list, tmpart, l_artikel, l_pprice, l_lieferant, l_order
        nonlocal sorttype, f_date, t_date, to_dt, mi_ch, mi_call, s_artnr
        nonlocal l_art, l_ppr, l_lief


        nonlocal pchase_list, l_art, l_ppr, l_lief
        nonlocal pchase_list_list

        return {"pchase-list": pchase_list_list}

    if mi_ch == 'ytd':
        f_date = date_mdy(1, 1, get_year(to_dt))
        t_date = to_dt

    if not mi_call == 'all':

        l_pprice_obj_list = {}
        l_pprice = L_pprice()
        l_art = L_artikel()
        l_lieferant = L_lieferant()
        for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                 (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():
            if l_pprice_obj_list.get(l_pprice._recid):
                continue
            else:
                l_pprice_obj_list[l_pprice._recid] = True


            pchase_list = Pchase_list()
            pchase_list_list.append(pchase_list)

            pchase_list.bestelldatum = l_pprice.bestelldatum
            pchase_list.firma = l_lieferant.firma
            pchase_list.docu_nr = l_pprice.docu_nr
            pchase_list.traubensort = l_art.traubensorte
            pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
            pchase_list.betriebsnr = l_pprice.betriebsnr
            pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
            pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
            pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
            pchase_list.artnr = l_art.artnr
            pchase_list.bezeich = l_art.bezeich

            l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

            if l_order:
                pchase_list.remark = l_order.besteller

    elif mi_call == 'all':

        if s_artnr == 0:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date)).order_by(L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True


                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.docu_nr = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller
        else:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True


                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.docu_nr = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

    for pchase_list in query(pchase_list_list):

        if pchase_list.anzahl == 0 and pchase_list.warenwert == 0:
            pchase_list_list.remove(pchase_list)

    return generate_output()