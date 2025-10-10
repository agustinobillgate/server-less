#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from functions.load_hoteldptbl import load_hoteldptbl
from models import Hoteldpt, Artikel, Htparam

input_list_data, Input_list = create_model("Input_list", {"modtype":int, "dept_num":int})

def prepare_outlet_config_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Artikel, Htparam])

    output_list_data = []
    departtypes_data = []
    modtype:int = 0
    dept_num:int = 0
    i:int = 0
    hoteldpt = artikel = htparam = None

    input_list = output_list = t_hoteldept = departtypes = dbuff = None

    output_list_data, Output_list = create_model("Output_list", {"dept_num":int, "departement":string, "dpttype":int, "servcode":int, "taxcode":int, "msg_str":string, "success_flag":bool, "servlist":[int,5], "taxlist":[int,5]}, {"success_flag": True})
    t_hoteldept_data, T_hoteldept = create_model_like(Hoteldpt)
    departtypes_data, Departtypes = create_model("Departtypes", {"nr":int, "bezeich":string, "tr_bez":string})

    Dbuff = T_hoteldept
    dbuff_data = t_hoteldept_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, departtypes_data, modtype, dept_num, i, hoteldpt, artikel, htparam
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtypes, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtypes_data

        return {"output-list": output_list_data, "departtypes": departtypes_data}

    def chg_dept_prepare():

        nonlocal output_list_data, departtypes_data, modtype, dept_num, i, hoteldpt, artikel, htparam
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtypes, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtypes_data

        t_hoteldept = query(t_hoteldept_data, filters=(lambda t_hoteldept: t_hoteldept.num == dept_num and t_hoteldept.num != 0), first=True)

        if t_hoteldept:
            output_list.dept_num = t_hoteldept.num
            output_list.departement = t_hoteldept.depart
            output_list.dpttype = t_hoteldept.departtyp

            artikel = db_session.query(Artikel).filter(
                     ((Artikel.artnr == 10) | (Artikel.artnr == 11) | (Artikel.artnr == 30)) & (Artikel.artart == 0) & (Artikel.departement == dept_num)).first()

            if artikel:

                for htparam in db_session.query(Htparam).filter(
                         (Htparam.paramnr >= 1) & (Htparam.paramnr <= 16)).order_by(Htparam._recid).all():

                    if htparam.paramnr == artikel.mwst_code:
                        output_list.taxcode = htparam.fdecimal

                    if htparam.paramnr == artikel.service_code:
                        output_list.servcode = htparam.fdecimal


    def create_departtypes():

        nonlocal output_list_data, departtypes_data, modtype, dept_num, i, hoteldpt, artikel, htparam
        nonlocal dbuff


        nonlocal input_list, output_list, t_hoteldept, departtypes, dbuff
        nonlocal output_list_data, t_hoteldept_data, departtypes_data


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 1
        departtypes.bezeich = "Food & Beverage"
        departtypes.tr_bez = "Food & Beverage"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 2
        departtypes.bezeich = "Minibar"
        departtypes.tr_bez = "Minibar"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 3
        departtypes.bezeich = "Laundry"
        departtypes.tr_bez = "Laundry"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 4
        departtypes.bezeich = "Banquet"
        departtypes.tr_bez = "Banquet"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 5
        departtypes.bezeich = "Drug Store"
        departtypes.tr_bez = "Drug Store"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 6
        departtypes.bezeich = "Others"
        departtypes.tr_bez = "Others"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 7
        departtypes.bezeich = "Spa"
        departtypes.tr_bez = "Spa"


        departtypes = Departtypes()
        departtypes_data.append(departtypes)

        departtypes.nr = 8
        departtypes.bezeich = "Boutique"
        departtypes.tr_bez = "Boutique"

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.msg_str = "No input detected"
        output_list.success_flag = False

        return generate_output()
    else:
        modtype = input_list.modtype
        dept_num = input_list.dept_num


        t_hoteldept_data = get_output(load_hoteldptbl())
    output_list = Output_list()
    output_list_data.append(output_list)

    for i in range(1,5 + 1) :
        output_list.servlist[i - 1] = 0
        output_list.taxlist[i - 1] = 0


    output_list.servlist[0] = 10
    output_list.taxlist[0] = 5
    output_list.servlist[1] = 11
    output_list.taxlist[1] = 7
    output_list.servlist[2] = 0
    output_list.taxlist[2] = 10
    output_list.servlist[3] = 0
    output_list.taxlist[3] = 11
    output_list.servlist[4] = 0
    output_list.taxlist[4] = 0


    create_departtypes()

    if modtype == 1:
        chg_dept_prepare()
    else:

        return generate_output()

    return generate_output()