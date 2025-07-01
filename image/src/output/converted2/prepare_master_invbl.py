#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from functions.htpint import htpint
from models import Artikel, Bill, Guest, Htparam, Waehrung, Brief, Hoteldpt

def prepare_master_invbl(inp_rechnr:int, dept:int):

    prepare_cache ([Htparam, Waehrung, Hoteldpt])

    f_foinv_list = []
    t_bill_list = []
    t_guest_list = []
    t_artikel_list = []
    artikel = bill = guest = htparam = waehrung = brief = hoteldpt = None

    t_artikel = t_bill = t_guest = f_foinv = None

    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    f_foinv_list, F_foinv = create_model("F_foinv", {"price_decimal":int, "briefnr415":int, "briefnr688":int, "briefnr2315":int, "param60":int, "param145":int, "param497":int, "exchg_rate":Decimal, "param132":string, "param173":string, "ext_char":string, "curr_local":string, "curr_foreign":string, "b_title":string, "gname":string, "param146":bool, "param199":bool, "param219":bool, "double_currency":bool, "change_date":bool, "foreign_rate":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_foinv_list, t_bill_list, t_guest_list, t_artikel_list, artikel, bill, guest, htparam, waehrung, brief, hoteldpt
        nonlocal inp_rechnr, dept


        nonlocal t_artikel, t_bill, t_guest, f_foinv
        nonlocal t_artikel_list, t_bill_list, t_guest_list, f_foinv_list

        return {"f-foinv": f_foinv_list, "t-bill": t_bill_list, "t-guest": t_guest_list, "t-artikel": t_artikel_list}

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 219)]})
    f_foinv.change_date = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    f_foinv.foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            f_foinv.exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    f_foinv.curr_local = get_output(htpchar(152))
    f_foinv.curr_foreign = get_output(htpchar(144))
    f_foinv.param132 = get_output(htpchar(132))
    f_foinv.param173 = get_output(htpchar(173))
    f_foinv.param146 = get_output(htplogic(146))
    f_foinv.param199 = get_output(htplogic(199))
    f_foinv.param219 = get_output(htplogic(219))
    f_foinv.param60 = get_output(htpint(60))
    f_foinv.param145 = get_output(htpint(145))
    f_foinv.briefnr2315 = get_output(htpint(2315))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 497)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            f_foinv.param497 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2315)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            f_foinv.briefnr2315 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 415)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            f_foinv.briefnr415 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 688)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            f_foinv.briefnr688 = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})
    f_foinv.b_title = hoteldpt.depart

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
            f_foinv.gname = guest.name

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == dept) & (((Artikel.artart == 0) | (Artikel.artart == 8) | (Artikel.artart == 9)) | ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7))) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    return generate_output()