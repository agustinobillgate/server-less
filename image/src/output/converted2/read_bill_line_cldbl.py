#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Bill_line, Res_line, Bill, Artikel

def read_bill_line_cldbl(case_type:int, pvilanguage:int, rechno:int, artno:int, deptno:int, anzahl:int, epreis:Decimal, betrag:Decimal):

    prepare_cache ([Bill, Artikel])

    t_bill_line_list = []
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    art_type:int = 0
    lvcarea:string = "fo-invoice"
    bill_line = res_line = bill = artikel = None

    t_bill_line = rlbuff = bibuff = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string, "serv":Decimal, "vat":Decimal, "netto":Decimal, "art_type":int})

    Rlbuff = create_buffer("Rlbuff",Res_line)
    Bibuff = create_buffer("Bibuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_list, serv, vat, netto, vat2, fact, art_type, lvcarea, bill_line, res_line, bill, artikel
        nonlocal case_type, pvilanguage, rechno, artno, deptno, anzahl, epreis, betrag
        nonlocal rlbuff, bibuff


        nonlocal t_bill_line, rlbuff, bibuff
        nonlocal t_bill_line_list

        return {"t-bill-line": t_bill_line_list}

    if case_type == 1:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.artnr == artno) & (Bill_line.departement == deptno) & (Bill_line.rechnr == rechno)).order_by(Bill_line._recid).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 2:

        bill_line = get_cache (Bill_line, {"artnr": [(eq, artno)],"departement": [(eq, deptno)],"rechnr": [(eq, rechno)],"anzahl": [(eq, - anzahl)],"epreis": [(eq, epreis)],"betrag": [(eq, - betrag)]})

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 3:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == rechno)).order_by(Bill_line._recid).all():
            serv =  to_decimal("0")
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")
            netto =  to_decimal("0")
            fact =  to_decimal("0")

            artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

            if artikel:
                art_type = artikel.artart


                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
            netto =  to_decimal(bill_line.betrag) / to_decimal(fact)
            t_bill_line.serv =  to_decimal(netto) * to_decimal(serv)
            t_bill_line.vat =  to_decimal(netto) * to_decimal(vat)
            t_bill_line.netto =  to_decimal(t_bill_line.betrag) - to_decimal(t_bill_line.serv) - to_decimal(t_bill_line.vat)
            t_bill_line.art_type = art_type


    elif case_type == 4:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == rechno) & (Bill_line.artnr == artno)).order_by(Bill_line._recid).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 5:

        bill_line = get_cache (Bill_line, {"_recid": [(eq, anzahl)],"rechnr": [(eq, rechno)]})

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid

    if not t_bill_line:

        return generate_output()

    bill = get_cache (Bill, {"rechnr": [(eq, rechno)]})

    for t_bill_line in query(t_bill_line_list):

        artikel = get_cache (Artikel, {"artnr": [(eq, t_bill_line.artnr)],"departement": [(eq, t_bill_line.departement)]})

        if artikel:
            t_bill_line.artart = artikel.artart

        bill_line = get_cache (Bill_line, {"_recid": [(eq, t_bill_line.bl_recid)]})

        if bill_line.massnr != 0 and bill_line.billin_nr != 0 and (bill_line.massnr != bill.resnr or bill_line.billin_nr != bill.reslinnr):

            bibuff = get_cache (Bill, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)]})

            if bibuff:

                rlbuff = db_session.query(Rlbuff).filter(
                         (Rlbuff.resnr == bibuff.resnr) & (Rlbuff.reslinnr == bibuff.parent_nr)).first()

                if rlbuff:
                    t_bill_line.tool_tip = \
                        translateExtended ("RmNo", lvcarea, "") + " " +\
                        rlbuff.zinr + " " + rlbuff.name + " " + to_string(rlbuff.ankunft) +\
                        "-" + to_string(rlbuff.abreise) + " " +\
                        translateExtended ("BillNo", lvcarea, "") + " " +\
                        to_string(bibuff.rechnr)


                else:
                    t_bill_line.tool_tip = translateExtended ("RmNo", lvcarea, "") + " " + bibuff.zinr + " " + bibuff.name + " " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(bibuff.rechnr)
            else:
                t_bill_line.tool_tip = ""

    return generate_output()