#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Hoteldpt, Kellner, H_artikel, Wgrpdep

def prepare_drstore_reportbl():

    prepare_cache ([Htparam, Hoteldpt, Kellner, H_artikel, Wgrpdep])

    p_110 = None
    dstore_dept = 0
    ekumnr = 0
    zknr1 = 0
    zknr2 = 0
    zknr3 = 0
    zknr4 = 0
    zknr5 = 0
    zknr6 = 0
    bezeich1 = ""
    bezeich2 = ""
    bezeich3 = ""
    bezeich4 = ""
    bezeich5 = ""
    bezeich6 = ""
    user_list_list = []
    htparam = hoteldpt = kellner = h_artikel = wgrpdep = None

    user_list = None

    user_list_list, User_list = create_model("User_list", {"rec_id":int, "dept":int, "depart":string, "usrnr":int, "usrname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_110, dstore_dept, ekumnr, zknr1, zknr2, zknr3, zknr4, zknr5, zknr6, bezeich1, bezeich2, bezeich3, bezeich4, bezeich5, bezeich6, user_list_list, htparam, hoteldpt, kellner, h_artikel, wgrpdep


        nonlocal user_list
        nonlocal user_list_list

        return {"p_110": p_110, "dstore_dept": dstore_dept, "ekumnr": ekumnr, "zknr1": zknr1, "zknr2": zknr2, "zknr3": zknr3, "zknr4": zknr4, "zknr5": zknr5, "zknr6": zknr6, "bezeich1": bezeich1, "bezeich2": bezeich2, "bezeich3": bezeich3, "bezeich4": bezeich4, "bezeich5": bezeich5, "bezeich6": bezeich6, "user-list": user_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        p_110 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})

    if htparam:
        dstore_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 555)]})

    if htparam:
        ekumnr = htparam.finteger

    kellner_obj_list = {}
    kellner = Kellner()
    hoteldpt = Hoteldpt()
    for kellner._recid, kellner.departement, kellner.kellner_nr, kellner.kellnername, hoteldpt.depart, hoteldpt._recid in db_session.query(Kellner._recid, Kellner.departement, Kellner.kellner_nr, Kellner.kellnername, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num == Kellner.departement)).filter(
             (Kellner.departement == dstore_dept)).order_by(Kellner.kellner_nr).all():
        if kellner_obj_list.get(kellner._recid):
            continue
        else:
            kellner_obj_list[kellner._recid] = True


        user_list = User_list()
        user_list_list.append(user_list)

        user_list.rec_id = kellner._recid
        user_list.dept = kellner.departement
        user_list.depart = hoteldpt.depart
        user_list.usrnr = kellner.kellner_nr
        user_list.usrname = kellner.kellnername

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == dstore_dept) & (H_artikel.artart == 0)).order_by(H_artikel.zwkum).all():

        if zknr1 == 0:
            zknr1 = h_artikel.zwkum

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dstore_dept)],"zknr": [(eq, h_artikel.zwkum)]})

            if wgrpdep:
                bezeich1 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and zknr2 == 0:
            zknr2 = h_artikel.zwkum

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dstore_dept)],"zknr": [(eq, h_artikel.zwkum)]})

            if wgrpdep:
                bezeich2 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and zknr3 == 0:
            zknr3 = h_artikel.zwkum

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dstore_dept)],"zknr": [(eq, h_artikel.zwkum)]})

            if wgrpdep:
                bezeich3 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and zknr4 == 0:
            zknr4 = h_artikel.zwkum

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dstore_dept)],"zknr": [(eq, h_artikel.zwkum)]})

            if wgrpdep:
                bezeich4 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and h_artikel.zwkum != zknr4 and zknr5 == 0:
            zknr5 = h_artikel.zwkum

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dstore_dept)],"zknr": [(eq, h_artikel.zwkum)]})

            if wgrpdep:
                bezeich5 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and h_artikel.zwkum != zknr4 and h_artikel.zwkum != zknr5 and zknr6 == 0:
            zknr6 = h_artikel.zwkum

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dstore_dept)],"zknr": [(eq, h_artikel.zwkum)]})

            if wgrpdep:
                bezeich6 = wgrpdep.bezeich

    return generate_output()