from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lieferant, Dml_art, L_artikel, Dml_artdep

def dml_stockin_create_dml_listbl(curr_dept:int, billdate:date):
    dml_list_list = []
    l_lieferant = dml_art = l_artikel = dml_artdep = None

    dml_list = buf_l_lieferant = None

    dml_list_list, Dml_list = create_model("Dml_list", {"bezeich":str, "anzahl":decimal, "geliefert":decimal, "einzelpreis":decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":str})

    Buf_l_lieferant = L_lieferant

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_list, l_lieferant, dml_art, l_artikel, dml_artdep
        nonlocal buf_l_lieferant


        nonlocal dml_list, buf_l_lieferant
        nonlocal dml_list_list
        return {"dml-list": dml_list_list}

    def create_dml_list():

        nonlocal dml_list_list, l_lieferant, dml_art, l_artikel, dml_artdep
        nonlocal buf_l_lieferant


        nonlocal dml_list, buf_l_lieferant
        nonlocal dml_list_list

        liefno:int = 0
        Buf_l_lieferant = L_lieferant
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

                    buf_l_lieferant = db_session.query(Buf_l_lieferant).filter(
                            (Buf_l_lieferant.lief_nr == liefno)).first()
                    dml_list.lief_nr = liefno
                    dml_list.supplier = buf_l_lieferant.firma

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

                    buf_l_lieferant = db_session.query(Buf_l_lieferant).filter(
                            (Buf_l_lieferant.lief_nr == liefno)).first()
                    dml_list.lief_nr = liefno
                    dml_list.supplier = buf_l_lieferant.firma

    create_dml_list()

    return generate_output()