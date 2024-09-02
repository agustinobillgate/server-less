from functions.additional_functions import *
import decimal
from models import Htparam, Bill_line, Artikel

def bill_vatsum(billno:int, start_pos:int):
    vat_str = ""
    ind:int = 0
    curr_vat:decimal = 0
    vatamt:decimal = 0
    curr_str:str = ""
    gdelimit:str = "VAT%,"
    prozspace:str = ""
    vatspace:str = ""
    netspace:str = ""
    curr_pos:int = 0
    nextloop:bool = False
    variable: = None
    htparam = bill_line = artikel = None

    vat_artlist = vat_list = workfile = None

    vat_artlist_list, Vat_artlist = create_model("Vat_artlist", {"artnr":int})
    vat_list_list, Vat_list = create_model("Vat_list", {"vatproz":decimal, "vatamt":decimal, "netto":decimal, "amount":decimal})
    workfile_list, Workfile = create_model("Workfile", {"selected":bool, "bl_recid":int}, {"selected": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal vat_str, ind, curr_vat, vatamt, curr_str, gdelimit, prozspace, vatspace, netspace, curr_pos, nextloop, variable, htparam, bill_line, artikel


        nonlocal vat_artlist, vat_list, workfile
        nonlocal vat_artlist_list, vat_list_list, workfile_list
        return {"vat_str": vat_str}

    def calc_vat():

        nonlocal vat_str, ind, curr_vat, vatamt, curr_str, gdelimit, prozspace, vatspace, netspace, curr_pos, nextloop, variable, htparam, bill_line, artikel


        nonlocal vat_artlist, vat_list, workfile
        nonlocal vat_artlist_list, vat_list_list, workfile_list


        curr_vat = 0

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

        if artikel.artart != 2 and artikel.artart != 6 and artikel.artart != 7:

            vat_artlist = query(vat_artlist_list, filters=(lambda vat_artlist :vat_artlist.artnr == artikel.artnr), first=True)
            IF1 + get_index(bill_line.origin_id, gdelimit) > 0 THEN
            curr_pos = 1 + get_index(bill_line.origin_id, gdelimit)
            curr_str = substring(bill_line.origin_id, curr_pos + len(gdelimit) - 1)
            curr_vat = decimal.Decimal(entry(0, curr_str, ";")) * 0.01


            else:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == artikel.mwst_code)).first()

                if htparam:
                    curr_vat = htparam.fdecimal

            vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vatProz == curr_vat), first=True)

            if not vat_list:
                vat_list = Vat_list()
                vat_list_list.append(vat_list)

                vat_list.vatProz = curr_vat

            if vat_artlist:
                vatamt = bill_line.betrag
            else:

                if bill_line.orts_tax != 0:
                    vatamt = bill_line.orts_tax
                else:
                    vatamt = bill_line.betrag / (1 + curr_vat * 0.01) * curr_vat * 0.01
            vat_list.amount = vat_list.amount + bill_line.betrag
            vat_list.netto = vat_list.netto + bill_line.betrag - vatamt
            vat_list.vatamt = vat_list.vatamt + vatamt

    prozspace = fill("KDV% ", 1)
    vatspace = fill("KDV ", 1)
    netspace = fill("NET ", 1)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 132)).first()

    if htparam.fchar != "":
        for ind in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if to_int(entry(ind - 1, htparam.fchar, ";")) != 0:
                vat_artlist = Vat_artlist()
                vat_artlist_list.append(vat_artlist)

                vat_artlist.artnr = to_int(entry(ind - 1, htparam.fchar, ";"))

    if spbill_flag:

        for spbill_list in query(spbill_list_list, filters=(lambda spbill_list :spbill_list.selected)):

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line._recid == spbill_list.bl_recid)).first()
            calc_vat()

    else:

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == billno)).all():
            calc_vat()


    for vat_list in query(vat_list_list):

        if nextloop:
            for ind in range(1,(start_pos - 1)  + 1) :
                vat_str = vat_str + " "
        nextloop = True
        vat_str = vat_str + prozspace + trim(to_string(vat_list.vatProz, ">9.99")) + fill(" ", len(to_string(vat_list.vatProz, ">9.99")) - len(trim(to_string(vat_list.vatProz, ">9.99")))) + vatspace + trim(to_string(vat_list.vatamt, "->,>>>,>>9.99")) + fill(" ", len(to_string(vat_list.vatamt, "->,>>>,>>9.99")) - len(trim(to_string(vat_list.vatamt, "->,>>>,>>9.99")))) + netspace + trim(to_string(vat_list.netto, "->>,>>>,>>9.99")) + fill(" ", len(to_string(vat_list.netto, "->>,>>>,>>9.99")) - len(trim(to_string(vat_list.netto, "->>,>>>,>>9.99")))) + "Total " + trim(to_string(vat_list.amount, "->>,>>>,>>9.99")) + chr(10)

    return generate_output()