from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, Dml_art, L_lieferant, Dml_artdep

def dml_issue_create_dml_listbl(curr_dept:int, billdate:date):
    dml_list_list = []
    t_l_artikel_list = []
    l_artikel = dml_art = l_lieferant = dml_artdep = None

    dml_list = t_l_artikel = None

    dml_list_list, Dml_list = create_model("Dml_list", {"bezeich":str, "anzahl":decimal, "geliefert":decimal, "einzelpreis":decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":str})
    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_list, t_l_artikel_list, l_artikel, dml_art, l_lieferant, dml_artdep


        nonlocal dml_list, t_l_artikel
        nonlocal dml_list_list, t_l_artikel_list
        return {"dml-list": dml_list_list, "t-l-artikel": t_l_artikel_list}

    def create_dml_list():

        nonlocal dml_list_list, t_l_artikel_list, l_artikel, dml_art, l_lieferant, dml_artdep


        nonlocal dml_list, t_l_artikel
        nonlocal dml_list_list, t_l_artikel_list

        liefno:int = 0
        dml_list_list.clear()

        if curr_dept == 0:

            for dml_art in db_session.query(Dml_art).filter(
                    (Dml_art.datum == billdate) &  (Dml_art.anzahl > 0)).all():

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == dml_art.artnr)).first()
                dml_list = Dml_list()
                dml_list_list.append(dml_list)

                buffer_copy(dml_art, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                liefno = 0
                liefno = to_int(entry(1, dml_art.userinit, ";"))

                if liefno > 0:

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == liefno)).first()
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma

        else:

            for dml_artdep in db_session.query(Dml_artdep).filter(
                    (Dml_artdep.datum == billdate) &  (Dml_artdep.departement == curr_dept) &  (Dml_artdep.anzahl > 0)).all():

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == dml_artdep.artnr)).first()
                dml_list = Dml_list()
                dml_list_list.append(dml_list)

                buffer_copy(dml_artdep, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                liefno = 0
                liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                if liefno > 0:

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == liefno)).first()
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma


    create_dml_list()

    for dml_list in query(dml_list_list):

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == dml_list.artnr)).first()
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    return generate_output()