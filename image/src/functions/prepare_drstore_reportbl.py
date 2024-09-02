from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, Kellner, H_artikel, Wgrpdep

def prepare_drstore_reportbl():
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

    user_list_list, User_list = create_model("User_list", {"rec_id":int, "dept":int, "depart":str, "usrnr":int, "usrname":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_110, dstore_dept, ekumnr, zknr1, zknr2, zknr3, zknr4, zknr5, zknr6, bezeich1, bezeich2, bezeich3, bezeich4, bezeich5, bezeich6, user_list_list, htparam, hoteldpt, kellner, h_artikel, wgrpdep


        nonlocal user_list
        nonlocal user_list_list
        return {"p_110": p_110, "dstore_dept": dstore_dept, "ekumnr": ekumnr, "zknr1": zknr1, "zknr2": zknr2, "zknr3": zknr3, "zknr4": zknr4, "zknr5": zknr5, "zknr6": zknr6, "bezeich1": bezeich1, "bezeich2": bezeich2, "bezeich3": bezeich3, "bezeich4": bezeich4, "bezeich5": bezeich5, "bezeich6": bezeich6, "user-list": user_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    p_110 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1082)).first()
    dstore_dept = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 555)).first()
    ekumnr = htparam.finteger

    kellner_obj_list = []
    for kellner, hoteldpt in db_session.query(Kellner, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == Kellner.departement)).filter(
            (Kellner.departement == dstore_dept)).all():
        if kellner._recid in kellner_obj_list:
            continue
        else:
            kellner_obj_list.append(kellner._recid)


        user_list = User_list()
        user_list_list.append(user_list)

        user_list.rec_id = kellner._recid
        user_list.dept = kellner.departement
        user_list.depart = hoteldpt.depart
        user_list.usrnr = kellner_nr
        user_list.usrname = kellnername

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == dstore_dept) &  (H_artikel.artart == 0)).all():

        if zknr1 == 0:
            zknr1 = h_artikel.zwkum

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.departement == dstore_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
            bezeich1 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and zknr2 == 0:
            zknr2 = h_artikel.zwkum

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.departement == dstore_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
            bezeich2 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and zknr3 == 0:
            zknr3 = h_artikel.zwkum

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.departement == dstore_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
            bezeich3 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and zknr4 == 0:
            zknr4 = h_artikel.zwkum

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.departement == dstore_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
            bezeich4 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and h_artikel.zwkum != zknr4 and zknr5 == 0:
            zknr5 = h_artikel.zwkum

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.departement == dstore_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
            bezeich5 = wgrpdep.bezeich

        elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and h_artikel.zwkum != zknr4 and h_artikel.zwkum != zknr5 and zknr6 == 0:
            zknr6 = h_artikel.zwkum

            wgrpdep = db_session.query(Wgrpdep).filter(
                    (Wgrpdep.departement == dstore_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
            bezeich6 = wgrpdep.bezeich

    return generate_output()