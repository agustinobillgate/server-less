#using conversion tools version: 1.0.0.117

# ============================================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Issue : Di progress ga ada define input param input_username
# ============================================================

from functions.additional_functions import *
from decimal import Decimal
from functions.load_hoteldptbl import load_hoteldptbl
from models import Hoteldpt, Queasy, Htparam, Paramtext

def prepare_outlet_landing_setup_wizardbl(input_username:string):

    prepare_cache ([Queasy, Htparam, Paramtext])

    output_list_data = []
    dept_list_data = []
    signature_list_data = []
    modtype:int = 0
    departement:string = ""
    dpttype:int = 0
    servcode:int = 0
    taxcode:int = 0
    section_progress:Decimal = to_decimal("0.0")
    setup_completed:int = 0
    dept_limit:int = 0
    curr_anz:int = 0
    epoch_signature:int = 0
    hoteldpt = queasy = htparam = paramtext = None

    output_list = value_list = signature_list = t_hoteldept = dept_list = None

    output_list_data, Output_list = create_model("Output_list", {"dept_limit":int, "curr_anz":int, "epoch_signature":int})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})
    t_hoteldept_data, T_hoteldept = create_model_like(Hoteldpt)
    dept_list_data, Dept_list = create_model("Dept_list", {"num":int, "depart":string, "departtype":string, "setup_completed":bool, "section_number":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, dept_list_data, signature_list_data, modtype, departement, dpttype, servcode, taxcode, section_progress, setup_completed, dept_limit, curr_anz, epoch_signature, hoteldpt, queasy, htparam, paramtext


        nonlocal output_list, value_list, signature_list, t_hoteldept, dept_list
        nonlocal output_list_data, value_list_data, signature_list_data, t_hoteldept_data, dept_list_data

        return {"output-list": output_list_data, "dept-list": dept_list_data, "signature-list": signature_list_data}

    def check_dept_limit():

        nonlocal output_list_data, dept_list_data, signature_list_data, modtype, departement, dpttype, servcode, taxcode, section_progress, setup_completed, dept_limit, curr_anz, epoch_signature, hoteldpt, queasy, htparam, paramtext


        nonlocal output_list, value_list, signature_list, t_hoteldept, dept_list
        nonlocal output_list_data, value_list_data, signature_list_data, t_hoteldept_data, dept_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 989)]})

        if htparam.finteger > 0:
            dept_limit = htparam.finteger
        curr_anz = -1

        for t_hoteldept in query(t_hoteldept_data):
            curr_anz = curr_anz + 1
        create_output()


    def create_output():

        nonlocal output_list_data, dept_list_data, signature_list_data, modtype, departement, dpttype, servcode, taxcode, section_progress, setup_completed, dept_limit, curr_anz, epoch_signature, hoteldpt, queasy, htparam, paramtext


        nonlocal output_list, value_list, signature_list, t_hoteldept, dept_list
        nonlocal output_list_data, value_list_data, signature_list_data, t_hoteldept_data, dept_list_data


        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "deptLimit"
        value_list.value_str = to_string(dept_limit)

        # Rulita | add input param input_username
        epoch_signature, signature_list_data = create_signature(input_username, value_list_data)
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.dept_limit = dept_limit
        output_list.curr_anz = curr_anz
        output_list.epoch_signature = epoch_signature


    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal output_list_data, dept_list_data, signature_list_data, modtype, departement, dpttype, servcode, taxcode, section_progress, setup_completed, dept_limit, curr_anz, epoch_signature, hoteldpt, queasy, htparam, paramtext


        nonlocal output_list, value_list, signature_list, t_hoteldept, dept_list
        nonlocal output_list_data, signature_list_data, t_hoteldept_data, dept_list_data

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_data)


        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_data):
            value_str = value_list.value_str.lower()
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_data.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal output_list_data, dept_list_data, signature_list_data, modtype, departement, dpttype, servcode, taxcode, section_progress, setup_completed, dept_limit, curr_anz, epoch_signature, hoteldpt, queasy, htparam, paramtext


        nonlocal output_list, value_list, signature_list, t_hoteldept, dept_list
        nonlocal output_list_data, value_list_data, signature_list_data, t_hoteldept_data, dept_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    t_hoteldept_data = get_output(load_hoteldptbl())

    for t_hoteldept in query(t_hoteldept_data, filters=(lambda t_hoteldept: t_hoteldept.num > 0)):
        section_progress =  to_decimal("0")
        setup_completed = 0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 357) & (Queasy.number1 == 2) & (Queasy.number2 == t_hoteldept.num)).order_by(Queasy._recid).all():

            if queasy.deci1 > section_progress:
                section_progress =  to_decimal(queasy.deci1)
            setup_completed = setup_completed + 1
        dept_list = Dept_list()
        dept_list_data.append(dept_list)

        dept_list.num = t_hoteldept.num
        dept_list.depart = t_hoteldept.depart
        dept_list.setup_completed = (setup_completed == 4)
        dept_list.section_number =  to_decimal(section_progress)

        if t_hoteldept.departtyp == 1:
            dept_list.departtype = "Food & Beverage"
        elif t_hoteldept.departtyp == 2:
            dept_list.departtype = "Minibar"
        elif t_hoteldept.departtyp == 3:
            dept_list.departtype = "Laundry"
        elif t_hoteldept.departtyp == 4:
            dept_list.departtype = "Banquet"
        elif t_hoteldept.departtyp == 5:
            dept_list.departtype = "Drug Store"
        elif t_hoteldept.departtyp == 6:
            dept_list.departtype = "Others"
        elif t_hoteldept.departtyp == 7:
            dept_list.departtype = "Spa"
        elif t_hoteldept.departtyp == 8:
            dept_list.departtype = "Boutique"
        else:

            if t_hoteldept.num <= 9:
                dept_list.departtype = "Food & Beverage"

            elif t_hoteldept.num == 10:
                dept_list.departtype = "Minibar"

            elif t_hoteldept.num == 20:
                dept_list.departtype = "Laundry"

            elif t_hoteldept.num == 11:
                dept_list.departtype = "Banquet"

            elif t_hoteldept.num == 15:
                dept_list.departtype = "Drug Store"

            elif t_hoteldept.num == 14:
                dept_list.departtype = "Spa"

            elif t_hoteldept.num == 16:
                dept_list.departtype = "Boutique"
            else:
                dept_list.departtype = "Others"
    check_dept_limit()

    return generate_output()