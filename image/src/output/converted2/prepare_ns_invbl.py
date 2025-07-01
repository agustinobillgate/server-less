#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpdec import htpdec
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Bill, Guest, Htparam, Artikel, Waehrung, Brief, Hoteldpt

def prepare_ns_invbl(inp_rechnr:int, curr_department:int, combo_pf_file1:string, combo_pf_file2:string, combo_gastnr:int, combo_ledger:int):

    prepare_cache ([Htparam, Waehrung, Hoteldpt])

    f_foinv_list = []
    t_bill_list = []
    t_guest_list = []
    golf_license:string = "False"
    bill = guest = htparam = artikel = waehrung = brief = hoteldpt = None

    t_bill = t_guest = f_foinv = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    f_foinv_list, F_foinv = create_model("F_foinv", {"price_decimal":int, "briefnr2314":int, "param60":int, "param145":int, "param487":int, "tel_rechnr":int, "pos1":int, "pos2":int, "ba_dept":int, "exchg_rate":Decimal, "max_price":Decimal, "param132":string, "ext_char":string, "curr_local":string, "curr_foreign":string, "b_title":string, "gname":string, "param219":bool, "double_currency":bool, "foreign_rate":bool, "banquet_flag":bool, "mc_flag":bool}, {"ba_dept": -1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_foinv_list, t_bill_list, t_guest_list, golf_license, bill, guest, htparam, artikel, waehrung, brief, hoteldpt
        nonlocal inp_rechnr, curr_department, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger


        nonlocal t_bill, t_guest, f_foinv
        nonlocal t_bill_list, t_guest_list, f_foinv_list

        return {"f-foinv": f_foinv_list, "t-bill": t_bill_list, "t-guest": t_guest_list, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger}


    if combo_gastnr == None:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 155)]})
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:

            guest = get_cache (Guest, {"gastnr": [(eq, combo_gastnr)]})

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, combo_ledger)],"departement": [(eq, 0)],"artart": [(eq, 2)]})

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0


            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 339)]})
        combo_pf_file1 = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 340)]})
        combo_pf_file2 = htparam.fchar
    f_foinv = F_foinv()
    f_foinv_list.append(f_foinv)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 148)]})
    f_foinv.ext_char = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 453)]})

    if htparam.feldtyp == 5 and htparam.fchar != "":
        f_foinv.ext_char = f_foinv.ext_char + ";" + htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    f_foinv.price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam:
        f_foinv.double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    f_foinv.foreign_rate = htparam.flogical

    if f_foinv.foreign_rate or f_foinv.double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            f_foinv.exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    f_foinv.max_price = get_output(htpdec(1086))
    mc_flag = get_output(htplogic(168))

    if mc_flag:
        pos1 = get_output(htpint(337))
        pos2 = get_output(htpint(338))

        if pos1 == 0:
            pos1 = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 985)]})

    if htparam.flogical:
        f_foinv.ba_dept = get_output(htpint(900))
    f_foinv.curr_local = get_output(htpchar(152))
    f_foinv.curr_foreign = get_output(htpchar(144))
    f_foinv.param132 = get_output(htpchar(132))
    f_foinv.param219 = get_output(htplogic(219))
    f_foinv.param60 = get_output(htpint(60))
    f_foinv.param145 = get_output(htpint(145))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2314)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            f_foinv.briefnr2314 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 487)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            f_foinv.param487 = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_department)]})
    f_foinv.b_title = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 299)]})

    if htparam.paramgruppe == 99 and htparam.flogical:
        golf_license = "YES"
    f_foinv.gname = golf_license + chr_unicode(2)

    if inp_rechnr != 0:

        bill = get_cache (Bill, {"rechnr": [(eq, inp_rechnr)]})
        t_bill = T_bill()
        t_bill_list.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = to_int(bill._recid)

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

        if guest:
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            f_foinv.gname = f_foinv.gname + guest.name

    return generate_output()