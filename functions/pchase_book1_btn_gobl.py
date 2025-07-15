#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_lieferant, L_pprice

def pchase_book1_btn_gobl(s_artnr:int):

    prepare_cache ([L_artikel, L_lieferant, L_pprice])

    pchase_list_data = []
    l_artikel = l_lieferant = l_pprice = None

    pchase_list = None

    pchase_list_data, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":string, "docu_nr":string, "traubensort":string, "lief_einheit":Decimal, "betriebsnr":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_data, l_artikel, l_lieferant, l_pprice
        nonlocal s_artnr


        nonlocal pchase_list
        nonlocal pchase_list_data

        return {"pchase-list": pchase_list_data}

    l_pprice_obj_list = {}
    l_pprice = L_pprice()
    l_artikel = L_artikel()
    l_lieferant = L_lieferant()
    for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice._recid, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice._recid, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel._recid, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
             (L_pprice.artnr == s_artnr)).order_by(L_pprice._recid).all():
        if l_pprice_obj_list.get(l_pprice._recid):
            continue
        else:
            l_pprice_obj_list[l_pprice._recid] = True


        pchase_list = Pchase_list()
        pchase_list_data.append(pchase_list)

        pchase_list.bestelldatum = l_pprice.bestelldatum
        pchase_list.firma = l_lieferant.firma
        pchase_list.docu_nr = l_pprice.docu_nr
        pchase_list.traubensort = l_artikel.traubensorte
        pchase_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        pchase_list.betriebsnr = l_pprice.betriebsnr
        pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
        pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
        pchase_list.warenwert =  to_decimal(l_pprice.warenwert)

    return generate_output()