from functions.additional_functions import *
import decimal
from models import L_artikel, L_lieferant, L_pprice, L_order

def pchase_book_btn_gobl(s_artnr:int):
    pchase_list_list = []
    l_artikel = l_lieferant = l_pprice = l_order = None

    pchase_list = l_art = None

    pchase_list_list, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":str, "docu_nr":str, "traubensort":str, "lief_einheit":decimal, "betriebsnr":int, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal, "remark":str})

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_list, l_artikel, l_lieferant, l_pprice, l_order
        nonlocal l_art


        nonlocal pchase_list, l_art
        nonlocal pchase_list_list
        return {"pchase-list": pchase_list_list}

    l_pprice_obj_list = []
    for l_pprice, l_art, l_lieferant in db_session.query(L_pprice, L_art, L_lieferant).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
            (L_pprice.artnr == s_artnr)).all():
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

    return generate_output()