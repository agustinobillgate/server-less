from functions.additional_functions import *
import decimal
from models import L_kredit, L_lieferant

def prepare_ap_editbl(recid_ap:int):
    firma = ""
    lief_nr = 0
    t_l_kredit_list = []
    l_kredit = l_lieferant = None

    t_l_kredit = None

    t_l_kredit_list, T_l_kredit = create_model_like(L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal firma, lief_nr, t_l_kredit_list, l_kredit, l_lieferant


        nonlocal t_l_kredit
        nonlocal t_l_kredit_list
        return {"firma": firma, "lief_nr": lief_nr, "t-l-kredit": t_l_kredit_list}

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit._recid == recid_ap)).first()

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == l_kredit.lief_nr)).first()
    t_l_kredit = T_l_kredit()
    t_l_kredit_list.append(t_l_kredit)

    buffer_copy(l_kredit, t_l_kredit)
    firma = l_lieferant.firma
    lief_nr = l_lieferant.lief_nr

    return generate_output()