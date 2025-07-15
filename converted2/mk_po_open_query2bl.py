from functions.additional_functions import *
import decimal
from models import L_artikel

def mk_po_open_query2bl(sorttype:int, lief_nr:int, a_artnr:int, a_bezeich:str):
    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":str, "betriebsnr":int, "ek_aktuell":decimal, "ek_letzter":decimal, "traubensort":str, "lief_einheit":decimal, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "jahrgang":int, "alkoholgrad":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel
        nonlocal sorttype, lief_nr, a_artnr, a_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    def create_t_l_artikel():

        nonlocal t_l_artikel_list, l_artikel
        nonlocal sorttype, lief_nr, a_artnr, a_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.betriebsnr = l_artikel.betriebsnr
        t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        t_l_artikel.ek_letzter =  to_decimal(l_artikel.ek_letzter)
        t_l_artikel.traubensort = l_artikel.traubensort
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.lief_nr1 = l_artikel.lief_nr1
        t_l_artikel.lief_nr2 = l_artikel.lief_nr2
        t_l_artikel.lief_nr3 = l_artikel.lief_nr3
        t_l_artikel.jahrgang = l_artikel.jahrgang
        t_l_artikel.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)


    l_artikel = db_session.query(L_artikel).filter(
             ((L_artikel.lief_nr1 == lief_nr) | (L_artikel.lief_nr2 == lief_nr) | (L_artikel.lief_nr3 == lief_nr))).first()

    if not l_artikel:

        return generate_output()

    if sorttype == 1:

        for t_l_artikel in query(t_l_artikel_list, filters=(lambda t_l_artikel: t_l_artikel.artnr > a_artnr and (t_l_artikel.lief_nr1 == lief_nr or t_l_artikel.lief_nr2 == lief_nr or t_l_artikel.lief_nr3 == lief_nr)), sort_by=[("artnr",False)]):
            create_t_l_artikel()

    else:

        for t_l_artikel in query(t_l_artikel_list, filters=(lambda t_l_artikel: t_l_artikel.bezeich.lower()  > (a_bezeich).lower()  and (t_l_artikel.lief_nr1 == lief_nr or t_l_artikel.lief_nr2 == lief_nr or t_l_artikel.lief_nr3 == lief_nr)), sort_by=[("bezeich",False)]):
            create_t_l_artikel()


    return generate_output()