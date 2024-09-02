from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, H_artikel, Wgrpdep

def prepare_ldry1_reportbl(zknr1:int, zknr2:int, zknr3:int, zknr4:int, zknr5:int):
    from_date = None
    ldry_dept = 0
    ekumnr = 0
    bezeich1 = ""
    bezeich2 = ""
    bezeich3 = ""
    bezeich4 = ""
    bezeich5 = ""
    flag = 0
    htparam = h_artikel = wgrpdep = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, ldry_dept, ekumnr, bezeich1, bezeich2, bezeich3, bezeich4, bezeich5, flag, htparam, h_artikel, wgrpdep


        return {"from_date": from_date, "ldry_dept": ldry_dept, "ekumnr": ekumnr, "bezeich1": bezeich1, "bezeich2": bezeich2, "bezeich3": bezeich3, "bezeich4": bezeich4, "bezeich5": bezeich5, "flag": flag}

    def get_zknr():

        nonlocal from_date, ldry_dept, ekumnr, bezeich1, bezeich2, bezeich3, bezeich4, bezeich5, flag, htparam, h_artikel, wgrpdep

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.departement == ldry_dept) &  (H_artikel.artart == 0) &  (H_artikel.artnr > 0)).all():

            if zknr1 == 0:
                zknr1 = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                        (Wgrpdep.departement == ldry_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
                bezeich1 = wgrpdep.bezeich
                flag = 1

            elif h_artikel.zwkum != zknr1 and zknr2 == 0:
                zknr2 = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                        (Wgrpdep.departement == ldry_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
                bezeich2 = wgrpdep.bezeich
                flag = 2

            elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and zknr3 == 0:
                zknr3 = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                        (Wgrpdep.departement == ldry_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
                bezeich3 = wgrpdep.bezeich
                flag = 3

            elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and zknr4 == 0:
                zknr4 = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                        (Wgrpdep.departement == ldry_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
                bezeich4 = wgrpdep.bezeich
                flag = 4

            elif h_artikel.zwkum != zknr1 and h_artikel.zwkum != zknr2 and h_artikel.zwkum != zknr3 and h_artikel.zwkum != zknr4 and zknr5 == 0:
                zknr5 = h_artikel.zwkum

                wgrpdep = db_session.query(Wgrpdep).filter(
                        (Wgrpdep.departement == ldry_dept) &  (Wgrpdep.zknr == h_artikel.zwkum)).first()
                bezeich5 = wgrpdep.bezeich
                flag = 5


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()
    ldry_dept = finteger
    get_zknr()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 555)).first()
    ekumnr = htparam.finteger

    return generate_output()