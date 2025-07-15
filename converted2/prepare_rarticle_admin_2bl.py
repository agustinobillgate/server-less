#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Htparam, Wgrpdep, Hoteldpt, Queasy, Wgrpgen, Artikel

def prepare_rarticle_admin_2bl(dept:int):

    prepare_cache ([Htparam, Wgrpdep, Hoteldpt, Queasy, Wgrpgen, Artikel])

    long_digit = False
    d_bezeich = ""
    only_corp_access = False
    q1_list_data = []
    h_artikel = htparam = wgrpdep = hoteldpt = queasy = wgrpgen = artikel = None

    wbuff = q1_list = None

    wbuff_data, Wbuff = create_model("Wbuff", {"departement":int, "zknr":int, "bez":string})
    q1_list_data, Q1_list = create_model_like(H_artikel, {"bez":string, "zknr":int, "bezeich2":string, "zk_bezeich":string, "ek_bezeich":string, "fart_bezeich":string, "fo_dept":int, "barcode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, d_bezeich, only_corp_access, q1_list_data, h_artikel, htparam, wgrpdep, hoteldpt, queasy, wgrpgen, artikel
        nonlocal dept


        nonlocal wbuff, q1_list
        nonlocal wbuff_data, q1_list_data

        return {"long_digit": long_digit, "d_bezeich": d_bezeich, "only_corp_access": only_corp_access, "q1-list": q1_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1204)]})
    only_corp_access = htparam.flogical

    for wgrpdep in db_session.query(Wgrpdep).filter(
             (Wgrpdep.departement == dept)).order_by(Wgrpdep._recid).all():
        wbuff = Wbuff()
        wbuff_data.append(wbuff)

        wbuff.departement = dept
        wbuff.zknr = wgrpdep.zknr
        wbuff.bez = wgrpdep.bezeich

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    d_bezeich = hoteldpt.depart

    h_artikel_obj_list = {}
    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == dept)).order_by(H_artikel.activeflag.desc(), H_artikel.artnr).all():
        wbuff = query(wbuff_data, (lambda wbuff: wbuff.zknr == h_artikel.zwkum and wbuff.departement == h_artikel.departement), first=True)
        if not wbuff:
            continue

        if h_artikel_obj_list.get(h_artikel._recid):
            continue
        else:
            h_artikel_obj_list[h_artikel._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        buffer_copy(h_artikel, q1_list)
        q1_list.bez = wbuff.bez
        q1_list.zknr = wbuff.zknr

        queasy = get_cache (Queasy, {"key": [(eq, 38)],"number1": [(eq, h_artikel.departement)],"number2": [(eq, h_artikel.artnr)]})

        if queasy:
            q1_list.bezeich2 = queasy.char3

        wgrpdep = get_cache (Wgrpdep, {"zknr": [(eq, h_artikel.zwkum)],"departement": [(eq, dept)]})

        if wgrpdep:
            q1_list.zk_bezeich = wgrpdep.bezeich
        else:
            q1_list.zk_bezeich = "?????"

        wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, h_artikel.endkum)]})

        if wgrpgen:
            q1_list.ek_bezeich = wgrpgen.bezeich
        else:
            q1_list.ek_bezeich = "?????"

        if h_artikel.artart <= 1:
            q1_list.fo_dept = dept
        else:
            q1_list.fo_dept = 0

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, q1_list.fo_dept)]})

        if artikel:
            q1_list.fart_bezeich = artikel.bezeich
        else:
            q1_list.fart_bezeich = "????????"

        queasy = get_cache (Queasy, {"key": [(eq, 200)],"number1": [(eq, h_artikel.departement)],"number2": [(eq, h_artikel.artnr)]})

        if queasy:
            q1_list.barcode = queasy.char1

    return generate_output()