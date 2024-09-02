from functions.additional_functions import *
import decimal
from models import L_artikel, L_lieferant, L_pprice

def pchase_book1_btn_gobl(s_artnr:int):
    pchase_list_list = []
    l_artikel = l_lieferant = l_pprice = None

    pchase_list = None

    pchase_list_list, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":str, "docu_nr":str, "traubensort":str, "lief_einheit":decimal, "betriebsnr":int, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_list, l_artikel, l_lieferant, l_pprice


        nonlocal pchase_list
        nonlocal pchase_list_list
        return {"pchase-list": pchase_list_list}

    l_pprice_obj_list = []
    for l_pprice, l_artikel, l_lieferant in db_session.query(L_pprice, L_artikel, L_lieferant).join(L_artikel,(l_artikel.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
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
        pchase_list.traubensort = l_artikel.traubensorte
        pchase_list.lief_einheit = l_artikel.lief_einheit
        pchase_list.betriebsnr = l_pprice.betriebsnr
        pchase_list.anzahl = l_pprice.anzahl
        pchase_list.einzelpreis = l_pprice.einzelpreis
        pchase_list.warenwert = l_pprice.warenwert

    return generate_output()