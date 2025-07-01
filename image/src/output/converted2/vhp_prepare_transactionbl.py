#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Nitehist, Nightaudit, Htparam

def vhp_prepare_transactionbl(ci_date:date):

    prepare_cache ([Nitehist, Nightaudit, Htparam])

    allocated_point = None
    avail_data = False
    record__count = 0
    flist_list = []
    fline_list_list = []
    reihenfolge:int = 0
    progname:string = "nt-loyaltyprog.p"
    nitehist = nightaudit = htparam = None

    flist = fline_list = buffnite = None

    flist_list, Flist = create_model("Flist", {"dept":int, "rechnr":int, "saldo":string, "discount":string, "created":string, "checkin":string, "checkout":string, "pax":int, "usr":string, "id":int, "reslinnr":string, "service":int, "resnr":int, "breslin":int, "gastnr":int, "gastpay":int})
    fline_list_list, Fline_list = create_model("Fline_list", {"rechnr":int, "dept":int, "bezeich":string, "price":string, "rtcode":string, "rmtype":string, "resnr":int, "reslinnr":string, "breslin":int, "gastnr":int, "gastpay":int})

    Buffnite = create_buffer("Buffnite",Nitehist)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal allocated_point, avail_data, record__count, flist_list, fline_list_list, reihenfolge, progname, nitehist, nightaudit, htparam
        nonlocal ci_date
        nonlocal buffnite


        nonlocal flist, fline_list, buffnite
        nonlocal flist_list, fline_list_list

        return {"allocated_point": allocated_point, "avail_data": avail_data, "record__count": record__count, "flist": flist_list, "fline-list": fline_list_list}


    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    htparam = get_cache (Htparam, {"paramnr": [(eq, 41)]})

    if htparam:
        allocated_point = htparam.finteger
    flist_list.clear()
    fline_list_list.clear()

    for nitehist in db_session.query(Nitehist).filter(
             (Nitehist.datum >= (ci_date - timedelta(days=1))) & (Nitehist.reihenfolge == reihenfolge) & (entry(0, Nitehist.line, "|") == ("H").lower()) & (entry(1, Nitehist.line, "|") == ("SEND=0").lower())).order_by(Nitehist._recid).all():
        flist = Flist()
        flist_list.append(flist)

        flist.rechnr = to_int(entry(2, nitehist.line, "|"))
        flist.usr = entry(3, nitehist.line, "|")
        flist.saldo = entry(4, nitehist.line, "|")
        flist.dept = to_int(entry(5, nitehist.line, "|"))
        flist.created = entry(6, nitehist.line, "|")
        flist.checkin = entry(7, nitehist.line, "|")
        flist.checkout = entry(8, nitehist.line, "|")
        flist.pax = to_int(entry(9, nitehist.line, "|"))
        flist.discount = entry(10, nitehist.line, "|")
        flist.reslinnr = entry(11, nitehist.line, "|")
        flist.service = to_int(entry(12, nitehist.line, "|"))
        flist.resnr = to_int(entry(13, nitehist.line, "|"))
        flist.breslin = to_int(entry(14, nitehist.line, "|"))
        flist.gastnr = to_int(entry(15, nitehist.line, "|"))
        flist.gastpay = to_int(entry(16, nitehist.line, "|"))
        flist.id = nitehist._recid

        if allocated_point == 2 or allocated_point == 3:

            for buffnite in db_session.query(Buffnite).filter(
                     (Buffnite.datum == nitehist.datum) & (Buffnite.reihenfolge == reihenfolge) & (entry(0, Buffnite.line, "|") == ("L").lower()) & (to_int(entry(1, Buffnite.line, "|")) == flist.rechnr) & (to_int(entry(2, Buffnite.line, "|")) == flist.dept) & (to_int(entry(7, Buffnite.line, "|")) == flist.resnr) & (entry(8, Buffnite.line, "|") == flist.reslinnr)).order_by(Buffnite._recid).all():
                fline_list = Fline_list()
                fline_list_list.append(fline_list)

                fline_list.rechnr = flist.rechnr
                fline_list.dept = flist.dept
                fline_list.bezeich = entry(3, buffnite.line, "|")
                fline_list.price = entry(4, buffnite.line, "|")
                fline_list.rtcode = entry(5, buffnite.line, "|")
                fline_list.rmtype = entry(6, buffnite.line, "|")
                fline_list.resnr = to_int(entry(7, buffnite.line, "|"))
                fline_list.reslinnr = entry(8, buffnite.line, "|")
                fline_list.breslin = to_int(entry(9, buffnite.line, "|"))
                fline_list.gastnr = to_int(entry(10, buffnite.line, "|"))
                fline_list.gastpay = to_int(entry(11, buffnite.line, "|"))


        else:

            for buffnite in db_session.query(Buffnite).filter(
                     (Buffnite.datum == nitehist.datum) & (Buffnite.reihenfolge == reihenfolge) & (entry(0, Buffnite.line, "|") == ("L").lower()) & (to_int(entry(1, Buffnite.line, "|")) == flist.rechnr) & (to_int(entry(2, Buffnite.line, "|")) == flist.dept)).order_by(Buffnite._recid).all():
                fline_list = Fline_list()
                fline_list_list.append(fline_list)

                fline_list.rechnr = flist.rechnr
                fline_list.dept = flist.dept
                fline_list.bezeich = entry(3, buffnite.line, "|")
                fline_list.price = entry(4, buffnite.line, "|")
                fline_list.rtcode = entry(5, buffnite.line, "|")
                fline_list.rmtype = entry(6, buffnite.line, "|")
                fline_list.resnr = to_int(entry(7, buffnite.line, "|"))
                fline_list.reslinnr = entry(12, buffnite.line, "|")
                fline_list.breslin = to_int(entry(9, buffnite.line, "|"))
                fline_list.gastnr = to_int(entry(10, buffnite.line, "|"))
                fline_list.gastpay = to_int(entry(11, buffnite.line, "|"))

    for flist in query(flist_list):
        record__count = record__count + 1

    if record__count > 0:
        avail_data = True

    return generate_output()