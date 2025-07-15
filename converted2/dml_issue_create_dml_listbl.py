#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Dml_art, L_lieferant, Dml_artdep

def dml_issue_create_dml_listbl(curr_dept:int, billdate:date):

    prepare_cache ([L_lieferant])

    dml_list_data = []
    t_l_artikel_data = []
    l_artikel = dml_art = l_lieferant = dml_artdep = None

    dml_list = t_l_artikel = None

    dml_list_data, Dml_list = create_model("Dml_list", {"bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":string})
    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_data, t_l_artikel_data, l_artikel, dml_art, l_lieferant, dml_artdep
        nonlocal curr_dept, billdate


        nonlocal dml_list, t_l_artikel
        nonlocal dml_list_data, t_l_artikel_data

        return {"dml-list": dml_list_data, "t-l-artikel": t_l_artikel_data}

    def create_dml_list():

        nonlocal dml_list_data, t_l_artikel_data, l_artikel, dml_art, l_lieferant, dml_artdep
        nonlocal curr_dept, billdate


        nonlocal dml_list, t_l_artikel
        nonlocal dml_list_data, t_l_artikel_data

        liefno:int = 0
        dml_list_data.clear()

        if curr_dept == 0:

            for dml_art in db_session.query(Dml_art).filter(
                     (Dml_art.datum == billdate) & (Dml_art.anzahl > 0)).order_by(Dml_art._recid).all():

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_art.artnr)]})
                dml_list = Dml_list()
                dml_list_data.append(dml_list)

                buffer_copy(dml_art, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                liefno = 0
                liefno = to_int(entry(1, dml_art.userinit, ";"))

                if liefno > 0:

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma

        else:

            for dml_artdep in db_session.query(Dml_artdep).filter(
                     (Dml_artdep.datum == billdate) & (Dml_artdep.departement == curr_dept) & (Dml_artdep.anzahl > 0)).order_by(Dml_artdep._recid).all():

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_artdep.artnr)]})
                dml_list = Dml_list()
                dml_list_data.append(dml_list)

                buffer_copy(dml_artdep, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                liefno = 0
                liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                if liefno > 0:

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma

    create_dml_list()

    for dml_list in query(dml_list_data):

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_list.artnr)]})
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    return generate_output()