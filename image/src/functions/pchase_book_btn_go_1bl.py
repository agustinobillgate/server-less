from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, L_pprice, L_lieferant, L_order

def pchase_book_btn_go_1bl(sorttype:int, f_dt:date, t_dt:date, to_dt:date, mi_ch:str, mi_call:str, s_artnr:int):
    pchase_list_list = []
    tmpart:int = 0
    f_date:date = None
    t_date:date = None
    l_artikel = l_pprice = l_lieferant = l_order = None

    pchase_list = l_art = l_ppr = l_lief = None

    pchase_list_list, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":str, "docu_nr":str, "traubensort":str, "lief_einheit":decimal, "betriebsnr":int, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal, "remark":str})

    L_art = L_artikel
    L_ppr = L_pprice
    L_lief = L_lieferant

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_list, tmpart, f_date, t_date, l_artikel, l_pprice, l_lieferant, l_order
        nonlocal l_art, l_ppr, l_lief


        nonlocal pchase_list, l_art, l_ppr, l_lief
        nonlocal pchase_list_list
        return {"pchase-list": pchase_list_list}

    if mi_ch == 'ftd':
        f_date = f_dt
        t_date = t_dt


    else:
        f_date = date_mdy(1, 1, get_year(to_dt))
        t_date = to_dt

    if not mi_call == 'all':

        l_pprice_obj_list = []
        for l_pprice, l_art, l_lieferant in db_session.query(L_pprice, L_art, L_lieferant).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                (L_pprice.bestelldatum >= f_date) &  (L_pprice.bestelldatum <= t_date) &  (L_pprice.artnr == s_artnr)).all():
            if l_pprice._recid in l_pprice_obj_list:
                continue
            else:
                l_pprice_obj_list.append(l_pprice._recid)


            pchase_list = Pchase_list()
            pchase_list_list.append(pchase_list)

            pchase_list.bestelldatum = l_pprice.bestelldatum
            pchase_list.firma = l_lieferant.firma
            pchase_list.docu_nr = l_pprice.docu_nr
            pchase_list.traubensort = l_art.traubensort
            pchase_list.lief_einheit = l_art.lief_einheit
            pchase_list.betriebsnr = l_pprice.betriebsnr
            pchase_list.anzahl = l_pprice.anzahl
            pchase_list.einzelpreis = l_pprice.einzelpreis
            pchase_list.warenwert = l_pprice.warenwert

            l_order = db_session.query(L_order).filter(
                    (L_order.docu_nr == l_pprice.docu_nr) &  (L_order.lief_nr == l_pprice.lief_nr) &  (L_order.artnr == s_artnr)).first()

            if l_order:
                pchase_list.remark = l_order.besteller

    elif mi_call == 'all':

        if sorttype == 1:

            for l_artikel, in query(l_artikel,_list, filters=(lambda l_artikel, :l_ppr.artnr == l_artikel.artnr and l_ppr.bestelldatum >= f_date and l_ppr.bestelldatum <= t_date)):

                if tmpart != l_artikel.artnr:
                    tmpart = l_artikel.artnr
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.bestelldatum = None
                    pchase_list.firma = l_artikel.bezeich.upper()

                l_pprice_obj_list = []
                for l_pprice, l_art, l_lieferant in db_session.query(L_pprice, L_art, L_lieferant).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                        (L_pprice.artnr == tmpart) &  (L_pprice.bestelldatum >= f_date) &  (L_pprice.bestelldatum <= t_date)).all():
                    if l_pprice._recid in l_pprice_obj_list:
                        continue
                    else:
                        l_pprice_obj_list.append(l_pprice._recid)


                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.bestelldatum = l_pprice.bestelldatum
                    pchase_list.firma = l_lieferant.firma
                    pchase_list.docu_nr = l_pprice.docu_nr
                    pchase_list.traubensort = l_art.traubensort
                    pchase_list.lief_einheit = l_art.lief_einheit
                    pchase_list.betriebsnr = l_pprice.betriebsnr
                    pchase_list.anzahl = l_pprice.anzahl
                    pchase_list.einzelpreis = l_pprice.einzelpreis
                    pchase_list.warenwert = l_pprice.warenwert

                    l_order = db_session.query(L_order).filter(
                            (L_order.docu_nr == l_pprice.docu_nr) &  (L_order.lief_nr == l_pprice.lief_nr) &  (L_order.artnr == l_pprice.artnr)).first()

                    if l_order:
                        pchase_list.remark = l_order.besteller

        if sorttype == 2:

            for l_artikel, in query(l_artikel,_list, filters=(lambda l_artikel, :l_ppr.artnr == l_artikel.artnr and l_ppr.bestelldatum >= f_date and l_ppr.bestelldatum <= t_date)):

                if tmpart != l_artikel.artnr:
                    tmpart = l_artikel.artnr
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.bestelldatum = None
                    pchase_list.firma = l_artikel.bezeich.upper()

                l_pprice_obj_list = []
                for l_pprice, l_art, l_lieferant in db_session.query(L_pprice, L_art, L_lieferant).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                        (L_pprice.artnr == tmpart) &  (L_pprice.bestelldatum >= f_date) &  (L_pprice.bestelldatum <= t_date)).all():
                    if l_pprice._recid in l_pprice_obj_list:
                        continue
                    else:
                        l_pprice_obj_list.append(l_pprice._recid)


                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.bestelldatum = l_pprice.bestelldatum
                    pchase_list.firma = l_lieferant.firma
                    pchase_list.docu_nr = l_pprice.docu_nr
                    pchase_list.traubensort = l_art.traubensort
                    pchase_list.lief_einheit = l_art.lief_einheit
                    pchase_list.betriebsnr = l_pprice.betriebsnr
                    pchase_list.anzahl = l_pprice.anzahl
                    pchase_list.einzelpreis = l_pprice.einzelpreis
                    pchase_list.warenwert = l_pprice.warenwert

                    l_order = db_session.query(L_order).filter(
                            (L_order.docu_nr == l_pprice.docu_nr) &  (L_order.lief_nr == l_pprice.lief_nr) &  (L_order.artnr == l_pprice.artnr)).first()

                    if l_order:
                        pchase_list.remark = l_order.besteller

        if sorttype == 3:

            for l_artikel, in query(l_artikel,_list, filters=(lambda l_artikel, :l_ppr.artnr == l_artikel.artnr and l_ppr.bestelldatum >= f_date and l_ppr.bestelldatum <= t_date)):

                if tmpart != l_artikel.artnr:
                    tmpart = l_artikel.artnr
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.bestelldatum = None
                    pchase_list.firma = l_artikel.bezeich.upper()

                l_pprice_obj_list = []
                for l_pprice, l_art, l_lieferant in db_session.query(L_pprice, L_art, L_lieferant).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                        (L_pprice.artnr == tmpart) &  (L_pprice.bestelldatum >= f_date) &  (L_pprice.bestelldatum <= t_date)).all():
                    if l_pprice._recid in l_pprice_obj_list:
                        continue
                    else:
                        l_pprice_obj_list.append(l_pprice._recid)


                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.bestelldatum = l_pprice.bestelldatum
                    pchase_list.firma = l_lieferant.firma
                    pchase_list.docu_nr = l_pprice.docu_nr
                    pchase_list.traubensort = l_art.traubensort
                    pchase_list.lief_einheit = l_art.lief_einheit
                    pchase_list.betriebsnr = l_pprice.betriebsnr
                    pchase_list.anzahl = l_pprice.anzahl
                    pchase_list.einzelpreis = l_pprice.einzelpreis
                    pchase_list.warenwert = l_pprice.warenwert

                    l_order = db_session.query(L_order).filter(
                            (L_order.docu_nr == l_pprice.docu_nr) &  (L_order.lief_nr == l_pprice.lief_nr) &  (L_order.artnr == l_pprice.artnr)).first()

                    if l_order:
                        pchase_list.remark = l_order.besteller

    for pchase_list in query(pchase_list_list):

        if pchase_list.anzahl == 0 and pchase_list.warenwert == 0:
            pchase_list_list.remove(pchase_list)

    return generate_output()