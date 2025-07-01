#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill_line, Res_line, Guest, Nation, Bill

def tourism_taxbl(fdate:date, tdate:date):

    prepare_cache ([Res_line, Guest, Nation])

    tourism_report_list = []
    tot_tax:Decimal = to_decimal("0.0")
    bill_line = res_line = guest = nation = bill = None

    tourism_report = None

    tourism_report_list, Tourism_report = create_model("Tourism_report", {"gastnr":int, "gname":string, "nat":string, "passport_no":string, "ci_date":date, "co_date":date, "tourism_tax":Decimal, "rmno":string, "rechnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tourism_report_list, tot_tax, bill_line, res_line, guest, nation, bill
        nonlocal fdate, tdate


        nonlocal tourism_report
        nonlocal tourism_report_list

        return {"tourism-report": tourism_report_list}

    bill_line = get_cache (Bill_line, {"bill_datum": [(ge, fdate),(le, tdate)],"artnr": [(eq, 108)]})
    while None != bill_line:

        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)]})

        if res_line:

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                tourism_report = query(tourism_report_list, filters=(lambda tourism_report: tourism_report.gastnr == guest.gastnr), first=True)

                if not tourism_report:

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)],"natcode": [(eq, 0)]})
                    tourism_report = Tourism_report()
                    tourism_report_list.append(tourism_report)

                    tourism_report.gastnr = res_line.gastnrmember
                    tourism_report.gname = res_line.name
                    tourism_report.passport_no = guest.ausweis_nr1
                    tourism_report.ci_date = res_line.ankunft
                    tourism_report.co_date = res_line.abreise
                    tourism_report.tourism_tax =  to_decimal(bill_line.betrag)
                    tourism_report.rmno = res_line.zinr
                    tourism_report.rechnr = bill_line.rechnr

                    if nation:
                        tourism_report.nat = nation.bezeich


                else:
                    tourism_report.tourism_tax =  to_decimal(tourism_report.tourism_tax) + to_decimal(bill_line.betrag)


                tot_tax =  to_decimal(tot_tax) + to_decimal(bill_line.betrag)


        else:

            bill = get_cache (Bill, {"rechnr": [(eq, bill_line.rechnr)]})

            if bill:

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                if guest:

                    tourism_report = query(tourism_report_list, filters=(lambda tourism_report: tourism_report.gastnr == guest.gastnr), first=True)

                    if not tourism_report:

                        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)],"natcode": [(eq, 0)]})
                        tourism_report = Tourism_report()
                        tourism_report_list.append(tourism_report)

                        tourism_report.gastnr = bill.gastnr
                        tourism_report.gname = bill.name
                        tourism_report.passport_no = guest.ausweis_nr1
                        tourism_report.tourism_tax =  to_decimal(bill_line.betrag)
                        tourism_report.rechnr = bill_line.rechnr

                        if nation:
                            tourism_report.nat = nation.bezeich


                    else:
                        tourism_report.tourism_tax =  to_decimal(tourism_report.tourism_tax) + to_decimal(bill_line.betrag)


                    tot_tax =  to_decimal(tot_tax) + to_decimal(bill_line.betrag)

        curr_recid = bill_line._recid
        bill_line = db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum >= fdate) & (Bill_line.bill_datum <= tdate) & (Bill_line.artnr == 108) & (Bill_line._recid > curr_recid)).first()
    tourism_report = Tourism_report()
    tourism_report_list.append(tourism_report)

    tourism_report.gname = "T O T A L"
    tourism_report.tourism_tax =  to_decimal(tot_tax)

    return generate_output()