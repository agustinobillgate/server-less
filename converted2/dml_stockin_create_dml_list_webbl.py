#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, Dml_art, L_artikel, Dml_artdep, Reslin_queasy

def dml_stockin_create_dml_list_webbl(curr_dept:int, billdate:date):

    prepare_cache ([L_lieferant, L_artikel])

    dml_list_data = []
    l_lieferant = dml_art = l_artikel = dml_artdep = reslin_queasy = None

    dml_list = None

    dml_list_data, Dml_list = create_model("Dml_list", {"bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":string, "content":int, "dml_code":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_data, l_lieferant, dml_art, l_artikel, dml_artdep, reslin_queasy
        nonlocal curr_dept, billdate


        nonlocal dml_list
        nonlocal dml_list_data

        return {"dml-list": dml_list_data}

    def create_dml_list():

        nonlocal dml_list_data, l_lieferant, dml_art, l_artikel, dml_artdep, reslin_queasy
        nonlocal curr_dept, billdate


        nonlocal dml_list
        nonlocal dml_list_data

        liefno:int = 0
        buf_l_lieferant = None
        Buf_l_lieferant =  create_buffer("Buf_l_lieferant",L_lieferant)
        dml_list_data.clear()

        if curr_dept == 0:

            for dml_art in db_session.query(Dml_art).filter(
                     (Dml_art.datum == billdate) & (Dml_art.anzahl > 0) & (matches(Dml_art.chginit,"*!*"))).order_by(Dml_art._recid).all():

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_art.artnr)]})
                dml_list = Dml_list()
                dml_list_data.append(dml_list)

                buffer_copy(dml_art, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                dml_list.content = l_artikel.lief_einheit
                dml_list.dml_code = entry(1, dml_art.chginit, ";")
                liefno = 0
                liefno = to_int(entry(1, dml_art.userinit, ";"))

                if liefno > 0:

                    buf_l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = buf_l_lieferant.firma


        else:

            for dml_artdep in db_session.query(Dml_artdep).filter(
                     (Dml_artdep.datum == billdate) & (Dml_artdep.departement == curr_dept) & (Dml_artdep.anzahl > 0) & (matches(Dml_artdep.chginit,"*!*"))).order_by(Dml_artdep._recid).all():

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_artdep.artnr)]})
                dml_list = Dml_list()
                dml_list_data.append(dml_list)

                buffer_copy(dml_artdep, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                dml_list.content = l_artikel.lief_einheit
                dml_list.dml_code = entry(1, dml_artdep.chginit, ";")
                liefno = 0
                liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                if liefno > 0:

                    buf_l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = buf_l_lieferant.firma

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == billdate) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy.deci2 > 0) & (matches(Reslin_queasy.char3,"*!*"))).first()
            while None != reslin_queasy:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))]})
                dml_list = Dml_list()
                dml_list_data.append(dml_list)

                dml_list.bezeich = l_artikel.bezeich
                dml_list.content = l_artikel.lief_einheit
                dml_list.anzahl =  to_decimal(reslin_queasy.deci2)
                dml_list.einzelpreis =  to_decimal(reslin_queasy.deci1)
                dml_list.artnr = to_int(entry(0, reslin_queasy.char1, ";"))
                dml_list.departement = to_int(entry(1, reslin_queasy.char1, ";"))
                dml_list.dml_code = entry(1, reslin_queasy.char3, ";")
                dml_list.geliefert =  to_decimal(reslin_queasy.deci3)
                liefno = 0
                liefno = to_int(entry(1, reslin_queasy.char2, ";"))

                if liefno > 0:

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma

                curr_recid = reslin_queasy._recid
                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == billdate) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy.deci2 > 0) & (matches(Reslin_queasy.char3,"*!*")) & (Reslin_queasy._recid > curr_recid)).first()

    create_dml_list()

    return generate_output()