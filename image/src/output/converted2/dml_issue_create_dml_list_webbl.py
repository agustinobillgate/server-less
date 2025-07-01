#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Dml_art, L_lieferant, Dml_artdep, Reslin_queasy

def dml_issue_create_dml_list_webbl(curr_dept:int, billdate:date):

    prepare_cache ([L_lieferant])

    dml_list_list = []
    t_l_artikel_list = []
    l_artikel = dml_art = l_lieferant = dml_artdep = reslin_queasy = None

    dml_list = t_l_artikel = None

    dml_list_list, Dml_list = create_model("Dml_list", {"bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "artnr":int, "departement":int, "lief_nr":int, "supplier":string, "content":int, "dml_code":string})
    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_list_list, t_l_artikel_list, l_artikel, dml_art, l_lieferant, dml_artdep, reslin_queasy
        nonlocal curr_dept, billdate


        nonlocal dml_list, t_l_artikel
        nonlocal dml_list_list, t_l_artikel_list

        return {"dml-list": dml_list_list, "t-l-artikel": t_l_artikel_list}

    def create_dml_list():

        nonlocal dml_list_list, t_l_artikel_list, l_artikel, dml_art, l_lieferant, dml_artdep, reslin_queasy
        nonlocal curr_dept, billdate


        nonlocal dml_list, t_l_artikel
        nonlocal dml_list_list, t_l_artikel_list

        liefno:int = 0
        dml_list_list.clear()

        if curr_dept == 0:

            for dml_art in db_session.query(Dml_art).filter(
                     (Dml_art.datum == billdate) & (Dml_art.anzahl > 0) & (matches(Dml_art.chginit,"*!*"))).order_by(Dml_art._recid).all():

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_art.artnr)]})
                dml_list = Dml_list()
                dml_list_list.append(dml_list)

                buffer_copy(dml_art, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                dml_list.content = l_artikel.lief_einheit
                dml_list.dml_code = entry(1, dml_art.chginit, ";")
                liefno = 0
                liefno = to_int(entry(1, dml_art.userinit, ";"))

                if liefno > 0:

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma


        else:

            for dml_artdep in db_session.query(Dml_artdep).filter(
                     (Dml_artdep.datum == billdate) & (Dml_artdep.departement == curr_dept) & (Dml_artdep.anzahl > 0) & (matches(Dml_artdep.chginit,"*!*"))).order_by(Dml_artdep._recid).all():

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_artdep.artnr)]})
                dml_list = Dml_list()
                dml_list_list.append(dml_list)

                buffer_copy(dml_artdep, dml_list)
                dml_list.bezeich = l_artikel.bezeich
                dml_list.content = l_artikel.lief_einheit
                dml_list.dml_code = entry(1, dml_artdep.chginit, ";")
                liefno = 0
                liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                if liefno > 0:

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})
                    dml_list.lief_nr = liefno
                    dml_list.supplier = l_lieferant.firma

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == billdate) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy.deci2 > 0) & (matches(Reslin_queasy.char3,"*!*"))).first()
            while None != reslin_queasy:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))]})
                dml_list = Dml_list()
                dml_list_list.append(dml_list)

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

    for dml_list in query(dml_list_list):

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_list.artnr)]})

        if l_artikel:

            t_l_artikel = query(t_l_artikel_list, filters=(lambda t_l_artikel: t_l_artikel.artnr == l_artikel.artnr), first=True)

            if not t_l_artikel:
                t_l_artikel = T_l_artikel()
                t_l_artikel_list.append(t_l_artikel)

                buffer_copy(l_artikel, t_l_artikel)

    return generate_output()