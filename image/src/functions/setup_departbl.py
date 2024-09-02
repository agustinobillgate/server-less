from functions.additional_functions import *
import decimal
from models import Hoteldpt, Htparam, Umsatz

def setup_departbl(icase:int, depart_list:[Depart_list]):
    dept_list_list = []
    success_flag = False
    counter:int = 0
    del_flag:bool = False
    curr_num:int = 0
    hoteldpt = htparam = umsatz = None

    dept_list = depart_list = bdept = htlbuff = None

    dept_list_list, Dept_list = create_model_like(Hoteldpt, {"dpttype":str})
    depart_list_list, Depart_list = create_model_like(Dept_list)

    Bdept = Hoteldpt
    Htlbuff = Hoteldpt

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_list_list, success_flag, counter, del_flag, curr_num, hoteldpt, htparam, umsatz
        nonlocal bdept, htlbuff


        nonlocal dept_list, depart_list, bdept, htlbuff
        nonlocal dept_list_list, depart_list_list
        return {"dept-list": dept_list_list, "success_flag": success_flag}

    def adjust_hoteldpt_num():

        nonlocal dept_list_list, success_flag, counter, del_flag, curr_num, hoteldpt, htparam, umsatz
        nonlocal bdept, htlbuff


        nonlocal dept_list, depart_list, bdept, htlbuff
        nonlocal dept_list_list, depart_list_list

        dept_code:int = 1
        Htlbuff = Hoteldpt

        if hoteldpt.departtyp == 2:
            hoteldpt.num = 10
        elif hoteldpt.departtyp == 3:
            hoteldpt.num = 20
        elif hoteldpt.departtyp == 4:
            hoteldpt.num = 11
        elif hoteldpt.departtyp == 5:
            hoteldpt.num = 15
        elif hoteldpt.departtyp == 7:
            hoteldpt.num = 14
        elif hoteldpt.departtyp == 8:
            hoteldpt.num = 16

        elif hoteldpt.num >= 10:
            REPEAT:

        htlbuff = db_session.query(Htlbuff).filter(
                (Htlbuff.num == dept_code)).first()

        if not htlbuff:
            hoteldpt.num = dept_code
            return
        dept_code = dept_code + 1


    if icase == 1:

        depart_list = query(depart_list_list, first=True)

        if depart_list:

            hoteldpt = db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num == depart_list.num)).first()

            if not hoteldpt:
                hoteldpt = Hoteldpt()
                db_session.add(hoteldpt)

                buffer_copy(depart_list, hoteldpt)

            elif hoteldpt:

                hoteldpt = db_session.query(Hoteldpt).first()
                hoteldpt.depart = depart_list.depart
                hoteldpt.departtyp = depart_list.departtyp


                adjust_hoteldpt_num()

                hoteldpt = db_session.query(Hoteldpt).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 4)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 900)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 900)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 3)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1081)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1081)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 2)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 570)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()


            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 949)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 570)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 949)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 5)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1082)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1082)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        for hoteldpt in db_session.query(Hoteldpt).all():
            dept_list = Dept_list()
            dept_list_list.append(dept_list)

            buffer_copy(hoteldpt, dept_list)

    elif icase == 2:

        depart_list = query(depart_list_list, first=True)

        if depart_list:

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.departement == depart_list.num)).first()

            if umsatz:
                success_flag = False

                return generate_output()

            hoteldpt = db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num == depart_list.num)).first()

            if hoteldpt:

                hoteldpt = db_session.query(Hoteldpt).first()
                db_session.delete(hoteldpt)


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 4)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 900)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 900)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 3)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1081)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1081)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 2)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 570)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()


            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 949)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 570)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 949)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.departtyp == 5)).first()

        if hoteldpt:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1082)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = hoteldpt.num

                htparam = db_session.query(Htparam).first()

        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1082)).first()

            if htparam:

                htparam = db_session.query(Htparam).first()
                htparam.finteger = 0

                htparam = db_session.query(Htparam).first()


        for hoteldpt in db_session.query(Hoteldpt).all():
            dept_list = Dept_list()
            dept_list_list.append(dept_list)

            buffer_copy(hoteldpt, dept_list)

    return generate_output()