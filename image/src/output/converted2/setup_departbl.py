#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Htparam, Umsatz

dept_list_list, Dept_list = create_model_like(Hoteldpt, {"dpttype":string})
depart_list_list, Depart_list = create_model_like(Dept_list)

def setup_departbl(icase:int, depart_list_list:[Depart_list]):

    prepare_cache ([Htparam])

    dept_list_list = []
    dept_list_list = []
    success_flag = True
    counter:int = 0
    del_flag:bool = False
    curr_num:int = 0
    hoteldpt = htparam = umsatz = None

    dept_list = depart_list = bdept = None

    Bdept = create_buffer("Bdept",Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_list_list, dept_list_list, success_flag, counter, del_flag, curr_num, hoteldpt, htparam, umsatz
        nonlocal icase
        nonlocal bdept


        nonlocal dept_list, depart_list, bdept
        nonlocal dept_list_list

        return {"dept-list": dept_list_list, "success_flag": success_flag}

    def adjust_hoteldpt_num():

        nonlocal dept_list_list, dept_list_list, success_flag, counter, del_flag, curr_num, hoteldpt, htparam, umsatz
        nonlocal icase
        nonlocal bdept


        nonlocal dept_list, depart_list, bdept
        nonlocal dept_list_list

        dept_code:int = 1
        htlbuff = None
        Htlbuff =  create_buffer("Htlbuff",Hoteldpt)

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
            while True:

                htlbuff = db_session.query(Htlbuff).filter(
                         (Htlbuff.num == dept_code)).first()

                if not htlbuff:
                    hoteldpt.num = dept_code
                    return
                dept_code = dept_code + 1

    if icase == 1:

        depart_list = query(depart_list_list, first=True)

        if depart_list:

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, depart_list.num)]})

            if not hoteldpt:
                hoteldpt = Hoteldpt()
                db_session.add(hoteldpt)

                buffer_copy(depart_list, hoteldpt)

            elif hoteldpt:
                pass
                hoteldpt.depart = depart_list.depart
                hoteldpt.departtyp = depart_list.departtyp


                adjust_hoteldpt_num()
                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 4)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 3)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 2)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 570)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass

            htparam = get_cache (Htparam, {"paramnr": [(eq, 949)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 570)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

            htparam = get_cache (Htparam, {"paramnr": [(eq, 949)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 5)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            dept_list = Dept_list()
            dept_list_list.append(dept_list)

            buffer_copy(hoteldpt, dept_list)

    elif icase == 2:

        depart_list = query(depart_list_list, first=True)

        if depart_list:

            umsatz = get_cache (Umsatz, {"departement": [(eq, depart_list.num)]})

            if umsatz:
                success_flag = False

                return generate_output()

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, depart_list.num)]})

            if hoteldpt:
                pass
                db_session.delete(hoteldpt)
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 4)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 3)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 2)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 570)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass

            htparam = get_cache (Htparam, {"paramnr": [(eq, 949)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 570)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

            htparam = get_cache (Htparam, {"paramnr": [(eq, 949)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        hoteldpt = get_cache (Hoteldpt, {"departtyp": [(eq, 5)]})

        if hoteldpt:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})

            if htparam:
                pass
                htparam.finteger = hoteldpt.num


                pass
                pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})

            if htparam:
                pass
                htparam.finteger = 0


                pass
                pass

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            dept_list = Dept_list()
            dept_list_list.append(dept_list)

            buffer_copy(hoteldpt, dept_list)

    return generate_output()