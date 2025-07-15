#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Bill_line, Artikel

def bill_vatsum(billno:int, start_pos:int):

    prepare_cache ([Htparam, Bill_line, Artikel])

    vat_str = ""
    ind:int = 0
    curr_vat:Decimal = to_decimal("0.0")
    vatamt:Decimal = to_decimal("0.0")
    curr_str:string = ""
    gdelimit:string = "VAT%,"
    prozspace:string = ""
    vatspace:string = ""
    netspace:string = ""
    curr_pos:int = 0
    nextloop:bool = False
    variable = None
    htparam = bill_line = artikel = None

    vat_artlist = vat_list = workfile = None

    vat_artlist_data, Vat_artlist = create_model("Vat_artlist", {"artnr":int})
    vat_list_data, Vat_list = create_model("Vat_list", {"vatproz":Decimal, "vatamt":Decimal, "netto":Decimal, "amount":Decimal})
    workfile_data, Workfile = create_model("Workfile", {"selected":bool, "bl_recid":int}, {"selected": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vat_str, ind, curr_vat, vatamt, curr_str, gdelimit, prozspace, vatspace, netspace, curr_pos, nextloop, variable, htparam, bill_line, artikel
        nonlocal billno, start_pos


        nonlocal vat_artlist, vat_list, workfile
        nonlocal vat_artlist_data, vat_list_data, workfile_data

        return {"vat_str": vat_str}

    def calc_vat():

        nonlocal vat_str, ind, curr_vat, vatamt, curr_str, gdelimit, prozspace, vatspace, netspace, curr_pos, nextloop, variable, htparam, bill_line, artikel
        nonlocal billno, start_pos


        nonlocal vat_artlist, vat_list, workfile
        nonlocal vat_artlist_data, vat_list_data, workfile_data


        curr_vat =  to_decimal("0")

        artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

        if artikel.artart != 2 and artikel.artart != 6 and artikel.artart != 7:

            vat_artlist = query(vat_artlist_data, filters=(lambda vat_artlist: vat_artlist.artnr == artikel.artnr), first=True)

            if get_index(bill_line.origin_id, gdelimit) > 0:
                curr_pos = get_index(bill_line.origin_id, gdelimit)
                curr_str = substring(bill_line.origin_id, curr_pos + length(gdelimit) - 1)
                curr_vat =  to_decimal(to_decimal(entry(0 , curr_str , ";"))) * to_decimal(0.01)


            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                if htparam:
                    curr_vat =  to_decimal(htparam.fdecimal)

            vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vatProz == curr_vat), first=True)

            if not vat_list:
                vat_list = Vat_list()
                vat_list_data.append(vat_list)

                vat_list.vatproz =  to_decimal(curr_vat)

            if vat_artlist:
                vatamt =  to_decimal(bill_line.betrag)
            else:

                if bill_line.orts_tax != 0:
                    vatamt =  to_decimal(bill_line.orts_tax)
                else:
                    vatamt =  to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(curr_vat) * to_decimal(0.01)) * to_decimal(curr_vat) * to_decimal(0.01)
            vat_list.amount =  to_decimal(vat_list.amount) + to_decimal(bill_line.betrag)
            vat_list.netto =  to_decimal(vat_list.netto) + to_decimal(bill_line.betrag) - to_decimal(vatamt)
            vat_list.vatamt =  to_decimal(vat_list.vatamt) + to_decimal(vatamt)


    prozspace = fill("KDV% ", 1)
    vatspace = fill("KDV ", 1)
    netspace = fill("NET ", 1)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

    if htparam.fchar != "":
        for ind in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if to_int(entry(ind - 1, htparam.fchar, ";")) != 0:
                vat_artlist = Vat_artlist()
                vat_artlist_data.append(vat_artlist)

                vat_artlist.artnr = to_int(entry(ind - 1, htparam.fchar, ";"))

    if spbill_flag:

        for spbill_list in query(spbill_list_data, filters=(lambda spbill_list: spbill_list.selected)):

            bill_line = get_cache (Bill_line, {"_recid": [(eq, spbill_list.bl_recid)]})
            calc_vat()

    else:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == billno)).order_by(Bill_line._recid).all():
            calc_vat()


    for vat_list in query(vat_list_data):

        if nextloop:
            for ind in range(1,(start_pos - 1)  + 1) :
                vat_str = vat_str + " "
        nextloop = True
        vat_str = vat_str + prozspace + trim(to_string(vat_list.vatProz, ">9.99")) + fill(" ", length(to_string(vat_list.vatProz, ">9.99")) - length(trim(to_string(vat_list.vatProz, ">9.99")))) + vatspace + trim(to_string(vat_list.vatamt, "->,>>>,>>9.99")) + fill(" ", length(to_string(vat_list.vatamt, "->,>>>,>>9.99")) - length(trim(to_string(vat_list.vatamt, "->,>>>,>>9.99")))) + netspace + trim(to_string(vat_list.netto, "->>,>>>,>>9.99")) + fill(" ", length(to_string(vat_list.netto, "->>,>>>,>>9.99")) - length(trim(to_string(vat_list.netto, "->>,>>>,>>9.99")))) + "Total " + trim(to_string(vat_list.amount, "->>,>>>,>>9.99")) + chr_unicode(10)

    return generate_output()