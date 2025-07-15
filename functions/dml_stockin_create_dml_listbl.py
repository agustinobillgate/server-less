#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Dml_art, L_artikel, Dml_artdep

def dml_stockin_create_dml_listbl(curr_dept:int, billdate:date):

    prepare_cache ([L_lieferant, L_artikel])

    dml_list_data = []
    l_lieferant = dml_art = l_artikel = dml_artdep = None

    dml_list = None

    dml_list_data, Dml_list = create_model("Dml_list", {"bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_data, l_lieferant, dml_art, l_artikel, dml_artdep
        nonlocal curr_dept, billdate


        nonlocal dml_list
        nonlocal dml_list_data

        return {"dml-list": dml_list_data}

    def create_dml_list():

        nonlocal dml_list_data, l_lieferant, dml_art, l_artikel, dml_artdep
        nonlocal curr_dept, billdate


        nonlocal dml_list
        nonlocal dml_list_data

        liefno:int = 0
        buf_l_lieferant = None
        Buf_l_lieferant =  create_buffer("Buf_l_lieferant",L_lieferant)
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

                    buf_l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = buf_l_lieferant.firma

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

                    buf_l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = buf_l_lieferant.firma


    create_dml_list()

    return generate_output()