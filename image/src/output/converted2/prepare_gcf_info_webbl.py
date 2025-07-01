#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Artikel, Res_line, Hoteldpt, Guest_queasy, Zimmer, Zimkateg, History

def prepare_gcf_info_webbl(pvilanguage:int, gastnr:int):

    prepare_cache ([Artikel, Zimmer, Zimkateg, History])

    payment = ""
    t_guest_list = []
    gcfinfo_list_list = []
    guest = artikel = res_line = hoteldpt = guest_queasy = zimmer = zimkateg = history = None

    gcfinfo_list = t_guest = None

    gcfinfo_list_list, Gcfinfo_list = create_model("Gcfinfo_list", {"nr":int, "dept":int, "rechnr":int, "datum":date, "str":string, "dept_str":string, "amount_food":string, "amount_bev":string, "amount_other":string, "room_number":string, "room_type":string, "arrival":string, "departure":string})
    t_guest_list, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment, t_guest_list, gcfinfo_list_list, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal pvilanguage, gastnr


        nonlocal gcfinfo_list, t_guest
        nonlocal gcfinfo_list_list, t_guest_list

        return {"payment": payment, "t-guest": t_guest_list, "gcfinfo-list": gcfinfo_list_list}

    def create_list():

        nonlocal payment, t_guest_list, gcfinfo_list_list, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal pvilanguage, gastnr


        nonlocal gcfinfo_list, t_guest
        nonlocal gcfinfo_list_list, t_guest_list

        reslin = None
        htldpt = None
        ginfo = None
        str1:string = ""
        i:int = 0
        dept_str:string = ""
        cistr:string = ""
        costr:string = ""
        curr_dept:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        sub_tot2:Decimal = to_decimal("0.0")
        sub_tot3:Decimal = to_decimal("0.0")
        total1:Decimal = to_decimal("0.0")
        total2:Decimal = to_decimal("0.0")
        total3:Decimal = to_decimal("0.0")
        sub_str:string = ""
        it_exists:bool = False
        rmno:string = ""
        rmcat:string = ""
        invdept:int = 0
        invno:int = 0
        invdate:date = None
        deptname:string = ""
        amt_food:string = ""
        amt_bev:string = ""
        amt_other:string = ""
        Reslin =  create_buffer("Reslin",Res_line)
        Htldpt =  create_buffer("Htldpt",Hoteldpt)
        Ginfo =  create_buffer("Ginfo",Guest_queasy)
        gcfinfo_list_list.clear()
        sub_str = "SUBTOTAL"

        for ginfo in db_session.query(Ginfo).filter(
                 (Ginfo.key == ("gast-info").lower()) & (Ginfo.gastnr == gastnr)).order_by(Ginfo.number1, Ginfo.date1).all():

            if curr_dept != ginfo.number1 and curr_dept != 0:
                i = i + 1
                add_line(i, fill("-", 30), fill("-", 30), fill("-", 30), fill("-", 30), "", "", -1, 0, None, "", "")
                i = i + 1
                deptname = sub_str
                amt_food = to_string(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
                amt_bev = to_string(sub_tot2, "->>,>>>,>>>,>>>,>>9.99")
                amt_other = to_string(sub_tot3, "->>,>>>,>>>,>>>,>>9.99")
                invdept = ginfo.number1
                invno = to_int(ginfo.char1)
                invdate = ginfo.date1


                add_line(i, deptname, amt_food, amt_bev, amt_other, "", "", -1, 0, None, "", "")
                i = i + 1
                add_line(i, "", "", "", "", "", "", -3, 0, None, "", "")
                sub_tot =  to_decimal("0")
                sub_tot2 =  to_decimal("0")
                sub_tot3 =  to_decimal("0")
            it_exists = True
            i = i + 1

            htldpt = db_session.query(Htldpt).filter(
                     (Htldpt.num == ginfo.number1)).first()

            if htldpt:
                dept_str = htldpt.depart
            else:
                dept_str = "UNKNOWN"
            cistr = to_string(ginfo.date1, "99/99/99")
            costr = cistr

            reslin = db_session.query(Reslin).filter(
                     (Reslin.resnr == ginfo.number2) & (Reslin.reslinnr == ginfo.number3)).first()

            if reslin:
                cistr = to_string(reslin.ankunft, "99/99/99")
                costr = to_string(reslin.abreise, "99/99/99")
                rmno = reslin.zinr

                zimmer = get_cache (Zimmer, {"zinr": [(eq, rmno)]})

                if zimmer:

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                    if zimkateg:
                        rmcat = zimkateg.kurzbez
            else:

                history = get_cache (History, {"gastnr": [(eq, gastnr)],"resnr": [(eq, ginfo.number2)],"reslinnr": [(eq, ginfo.number3)]})

                if history:
                    cistr = to_string(history.ankunft, "99/99/99")
                    costr = to_string(history.abreise, "99/99/99")
                    rmno = history.zinr

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, rmno)]})

                    if zimmer:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                        if zimkateg:
                            rmcat = zimkateg.kurzbez
                else:
                    rmno = ""
                    rmcat = ""
            deptname = dept_str
            amt_food = to_string(ginfo.deci1, "->>,>>>,>>>,>>>,>>9.99")
            amt_bev = to_string(ginfo.deci2, "->>,>>>,>>>,>>>,>>9.99")
            amt_other = to_string(ginfo.deci3, "->>,>>>,>>>,>>>,>>9.99")
            invdept = ginfo.number1
            invno = to_int(ginfo.char1)
            invdate = ginfo.date1


            add_line(i, deptname, amt_food, amt_bev, amt_other, rmno, rmcat, invdept, invno, invdate, cistr, costr)
            curr_dept = ginfo.number1
            sub_tot =  to_decimal(sub_tot) + to_decimal(ginfo.deci1)
            sub_tot2 =  to_decimal(sub_tot2) + to_decimal(ginfo.deci2)
            sub_tot3 =  to_decimal(sub_tot3) + to_decimal(ginfo.deci3)

        if it_exists:
            i = i + 1
            add_line(i, fill("-", 30), fill("-", 30), fill("-", 30), fill("-", 30), "", "", -1, 0, None, "", "")
            i = i + 1
            deptname = sub_str
            amt_food = to_string(sub_tot, "->>,>>>,>>>,>>>,>>9.99")
            amt_bev = to_string(sub_tot2, "->>,>>>,>>>,>>>,>>9.99")
            amt_other = to_string(sub_tot3, "->>,>>>,>>>,>>>,>>9.99")
            add_line(i, deptname, amt_food, amt_bev, amt_other, "", "", -1, 0, None, "", "")
            sub_tot =  to_decimal("0")
            sub_tot2 =  to_decimal("0")
            sub_tot3 =  to_decimal("0")
        i = 0

        for gcfinfo_list in query(gcfinfo_list_list, filters=(lambda gcfinfo_list: gcfinfo_list.dept_str.lower()  == ("SUBTOTAL").lower())):
            total1 =  to_decimal(total1) + to_decimal(to_decimal(gcfinfo_list.amount_food))
            total2 =  to_decimal(total2) + to_decimal(to_decimal(gcfinfo_list.amount_bev))
            total3 =  to_decimal(total3) + to_decimal(to_decimal(gcfinfo_list.amount_other))

        for gcfinfo_list in query(gcfinfo_list_list, sort_by=[("nr",True)]):
            i = gcfinfo_list.nr + 1
            break

        gcfinfo_list = query(gcfinfo_list_list, first=True)

        if gcfinfo_list:
            gcfinfo_list = Gcfinfo_list()
            gcfinfo_list_list.append(gcfinfo_list)

            gcfinfo_list.nr = i
            gcfinfo_list.dept = -1
            gcfinfo_list.rechnr = 0
            gcfinfo_list.datum = None
            gcfinfo_list.dept_str = ""
            gcfinfo_list.amount_food = ""
            gcfinfo_list.amount_bev = ""
            gcfinfo_list.amount_other = ""
            gcfinfo_list.room_number = ""
            gcfinfo_list.room_type = ""
            gcfinfo_list.arrival = ""
            gcfinfo_list.departure = ""


            i = i + 1
            gcfinfo_list = Gcfinfo_list()
            gcfinfo_list_list.append(gcfinfo_list)

            gcfinfo_list.nr = i
            gcfinfo_list.dept = -2
            gcfinfo_list.rechnr = 0
            gcfinfo_list.datum = None
            gcfinfo_list.dept_str = "TOTAL"
            gcfinfo_list.amount_food = to_string(total1, "->>,>>>,>>>,>>>,>>9.99")
            gcfinfo_list.amount_bev = to_string(total2, "->>,>>>,>>>,>>>,>>9.99")
            gcfinfo_list.amount_other = to_string(total3, "->>,>>>,>>>,>>>,>>9.99")
            gcfinfo_list.room_number = ""
            gcfinfo_list.room_type = ""
            gcfinfo_list.arrival = ""
            gcfinfo_list.departure = ""


            i = 0


    def add_line(nr:int, deptname:string, amt_food:string, amt_bev:string, amt_other:string, room_no:string, rm_type:string, dept:int, rechnr:int, datum:date, arrival:string, departure:string):

        nonlocal payment, t_guest_list, gcfinfo_list_list, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal pvilanguage, gastnr


        nonlocal gcfinfo_list, t_guest
        nonlocal gcfinfo_list_list, t_guest_list


        gcfinfo_list = Gcfinfo_list()
        gcfinfo_list_list.append(gcfinfo_list)

        gcfinfo_list.nr = nr
        gcfinfo_list.dept = dept
        gcfinfo_list.rechnr = rechnr
        gcfinfo_list.datum = datum
        gcfinfo_list.dept_str = deptname
        gcfinfo_list.amount_food = amt_food
        gcfinfo_list.amount_bev = amt_bev
        gcfinfo_list.amount_other = amt_other
        gcfinfo_list.room_number = room_no
        gcfinfo_list.room_type = rm_type
        gcfinfo_list.arrival = arrival
        gcfinfo_list.departure = departure

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        buffer_copy(guest, t_guest)

        if guest.zahlungsart > 0:

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, guest.zahlungsart)]})

            if artikel:
                payment = to_string(guest.zahlungsart) + " - " + artikel.bezeich
    create_list()

    return generate_output()