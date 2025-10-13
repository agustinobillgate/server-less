#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.load_hoteldptbl import load_hoteldptbl
from models import Hoteldpt, Htparam, Artikel, Queasy

input_list_data, Input_list = create_model("Input_list", {"modtype":int, "dept_num":int, "departement":string, "dpttype":int, "servcode":int, "taxcode":int})

def save_outlet_config_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Hoteldpt, Htparam, Artikel, Queasy])

    output_list_data = []
    modtype:int = 0
    departement:string = ""
    dpttype:int = 0
    servcode:int = 0
    taxcode:int = 0
    dept_limit:int = 0
    curr_anz:int = 0
    dept_num:int = 0
    hoteldpt = htparam = artikel = queasy = None

    input_list = output_list = t_hoteldept = departtype = dbuff = None

    output_list_data, Output_list = create_model("Output_list", {"dept_num":int, "msg_str":string, "success_flag":bool}, {"success_flag": True})
    t_hoteldept_data, T_hoteldept = create_model_like(Hoteldpt)
    departtype_data, departtype = create_model("departtype", {"nr":int, "bezeich":string, "tr_bez":string})

    Dbuff = T_hoteldept
    dbuff_data = t_hoteldept_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

        return {"output-list": output_list_data}

    def add_department():

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

        lreturn:bool = False
        newnum:int = 0

        if curr_anz >= dept_limit:
            output_list.msg_str = "Department limit exceeded."
            output_list.success_flag = False

            return

        dbuff = query(dbuff_data, filters=(lambda dbuff: dbuff.depart.lower()  == (departement).lower()), first=True)

        if dbuff:
            output_list.msg_str = "Department name already exists."
            output_list.success_flag = False

            return

        if dpttype == 2:
            dept_num = 10
        elif dpttype == 3:
            dept_num = 20
        elif dpttype == 4:
            dept_num = 11
        elif dpttype == 5:
            dept_num = 15
        elif dpttype == 7:
            dept_num = 14
        elif dpttype == 8:
            dept_num = 16
        else:
            dept_num = 1
        while True:

            if dept_num == 10 and dpttype != 2:
                dept_num = 12

            if dept_num == 11 and dpttype != 4:
                dept_num = 12

            if dept_num == 14 and dpttype != 7:
                dept_num = 17

            if dept_num == 15 and dpttype != 5:
                dept_num = 17

            if dept_num == 16 and dpttype != 8:
                dept_num = 17

            if dept_num == 20 and dpttype != 3:
                dept_num = 21

            t_hoteldept = query(t_hoteldept_data, filters=(lambda t_hoteldept: t_hoteldept.num == dept_num), first=True)

            if not t_hoteldept:
                return
            dept_num = dept_num + 1
        newnum = write_data(dept_num, departement, dpttype)

        if dept_num != newnum:
            dept_num = newnum
        create_section(dept_num, 0)

        if output_list.success_flag :
            output_list.dept_num = dept_num


    def chg_department():

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

        lreturn:bool = False
        newnum:int = 0

        dbuff = query(dbuff_data, filters=(lambda dbuff: dbuff.depart.lower()  == (departement).lower()  and dbuff.num != dept_num), first=True)

        if dbuff:
            output_list.msg_str = "Department name already exists."
            output_list.success_flag = False

            return
        newnum = write_data(dept_num, departement, dpttype)
        create_section(newnum, dept_num)

        if output_list.success_flag :
            output_list.dept_num = newnum


    def write_data(num:int, depart:string, departtype:int):

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

        newnum = 0
        service_codename:string = ""
        tax_codename:string = ""
        servtax = None

        def generate_inner_output():
            return (newnum)

        Servtax =  create_buffer("Servtax",Htparam)

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, num)]})

        if not hoteldpt:
            hoteldpt = Hoteldpt()
            db_session.add(hoteldpt)

            hoteldpt.num = num
            hoteldpt.depart = depart
            hoteldpt.departtyp = departtype

        elif hoteldpt:
            pass
            hoteldpt.depart = depart
            hoteldpt.departtyp = departtype


            adjust_hoteldpt_num()
        pass
        newnum = hoteldpt.num
        service_codename = "Service Code " + to_string(hoteldpt.num, "99")

        for servtax in db_session.query(Servtax).filter(
                 (Servtax.paramnr >= 1) & (Servtax.paramnr <= 16)).order_by(Servtax._recid).all():

            if servtax.fdecimal == servcode and get_index(servtax.bezeichnung, "Service Code") > 0:

                htparam = get_cache (Htparam, {"_recid": [(eq, servtax._recid)]})
                break

        if htparam:
            pass

            if htparam.bezeichnung.lower()  != ("Service Code").lower()  and htparam.bezeichnung.lower()  != (service_codename).lower() :
                htparam.bezeichnung = "Service Code"
            pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(ge, 1),(le, 16)],"fdecimal": [(ne, servcode)],"bezeichnung": [(eq, service_codename)]})

            if htparam:
                pass
                htparam.fdecimal =  to_decimal(servcode)
                pass
            else:

                htparam = get_cache (Htparam, {"paramnr": [(ge, 1),(le, 16)],"fdecimal": [(eq, 0)]})

                if htparam:
                    pass
                    htparam.bezeichnung = service_codename
                    htparam.fdecimal =  to_decimal(servcode)


                    pass

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num)).order_by(Artikel._recid).all():
            artikel.service_code = htparam.paramnr
        pass
        tax_codename = "V.A.T. POS " + to_string(hoteldpt.num, "99")

        for servtax in db_session.query(Servtax).filter(
                 (Servtax.paramnr >= 1) & (Servtax.paramnr <= 16)).order_by(Servtax._recid).all():

            if servtax.fdecimal == taxcode and get_index(servtax.bezeichnung, "V.A.T. POS") > 0:

                htparam = get_cache (Htparam, {"_recid": [(eq, servtax._recid)]})
                break

        if htparam:
            pass

            if htparam.bezeichnung.lower()  != ("V.A.T. POS").lower()  and htparam.bezeichnung.lower()  != (tax_codename).lower() :
                htparam.bezeichnung = "V.A.T. POS"
            pass
        else:

            htparam = get_cache (Htparam, {"paramnr": [(ge, 1),(le, 16)],"fdecimal": [(ne, taxcode)],"bezeichnung": [(eq, tax_codename)]})

            if htparam:
                pass
                htparam.fdecimal =  to_decimal(taxcode)
                pass
            else:

                htparam = get_cache (Htparam, {"paramnr": [(ge, 1),(le, 16)],"fdecimal": [(eq, 0)]})

                if htparam:
                    pass
                    htparam.bezeichnung = tax_codename
                    htparam.fdecimal =  to_decimal(taxcode)


                    pass

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num)).order_by(Artikel._recid).all():
            artikel.mwst_code = htparam.paramnr
        pass

        return generate_inner_output()


    def adjust_hoteldpt_num():

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

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

                htlbuff = get_cache (Hoteldpt, {"num": [(eq, dept_code)]})

                if not htlbuff:
                    hoteldpt.num = dept_code
                    return
                dept_code = dept_code + 1


    def adjust_hotel_param():

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

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


    def check_dept_limit():

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 989)]})

        if htparam.finteger > 0:
            dept_limit = htparam.finteger
        curr_anz = -1

        for t_hoteldept in query(t_hoteldept_data):
            curr_anz = curr_anz + 1
        pass


    def create_section(pos_num:int, prv_num:int):

        nonlocal output_list_data, modtype, departement, dpttype, servcode, taxcode, dept_limit, curr_anz, dept_num, hoteldpt, htparam, artikel, queasy
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtype, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtype_data

        if prv_num != 0 and prv_num != pos_num:

            queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 2)],"number2": [(eq, prv_num)],"deci1": [(eq, 2.1)],"char1": [(eq, "outlet administration")],"char2": [(eq, "outlet setup")],"logi1": [(eq, True)]})

            if queasy:
                pass
                queasy.number2 = pos_num


        else:

            queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 2)],"number2": [(eq, pos_num)],"deci1": [(eq, 2.1)],"char1": [(eq, "outlet administration")],"char2": [(eq, "outlet setup")],"logi1": [(eq, True)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 357
                queasy.number1 = 2
                queasy.number2 = pos_num
                queasy.deci1 =  to_decimal(2.1)
                queasy.char1 = "OUTLET ADMINISTRATION"
                queasy.char2 = "OUTLET SETUP"
                queasy.logi1 = True

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.msg_str = "No input detected"
        output_list.success_flag = False

        return generate_output()
    else:
        modtype = input_list.modtype
        departement = input_list.departement
        dpttype = input_list.dpttype
        servcode = input_list.servcode
        taxcode = input_list.taxcode

        if modtype == 1:
            dept_num = 0
        else:
            dept_num = input_list.dept_num
        t_hoteldept_data = get_output(load_hoteldptbl())
    check_dept_limit()
    output_list = Output_list()
    output_list_data.append(output_list)


    if modtype == 1:
        add_department()
    elif modtype == 2:
        chg_department()
    else:

        return generate_output()

    return generate_output()