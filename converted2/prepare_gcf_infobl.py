#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Artikel, Res_line, Hoteldpt, Guest_queasy, Zimmer, Zimkateg, History

def prepare_gcf_infobl(pvilanguage:int, gastnr:int):

    prepare_cache ([Artikel, Zimmer, Zimkateg, History])

    payment = ""
    t_guest_data = []
    output_list_data = []
    lvcarea:string = "prepare-gcf-info"
    guest = artikel = res_line = hoteldpt = guest_queasy = zimmer = zimkateg = history = None

    output_list = t_guest = None

    output_list_data, Output_list = create_model("Output_list", {"nr":int, "dept":int, "rechnr":int, "datum":date, "str":string})
    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment, t_guest_data, output_list_data, lvcarea, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal pvilanguage, gastnr


        nonlocal output_list, t_guest
        nonlocal output_list_data, t_guest_data

        return {"payment": payment, "t-guest": t_guest_data, "output-list": output_list_data}

    def create_list():

        nonlocal payment, t_guest_data, output_list_data, lvcarea, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal pvilanguage, gastnr


        nonlocal output_list, t_guest
        nonlocal output_list_data, t_guest_data

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
        sub_str:string = ""
        it_exists:bool = False
        rmno:string = ""
        rmcat:string = ""
        invdept:int = 0
        invno:int = 0
        invdate:date = None
        Reslin =  create_buffer("Reslin",Res_line)
        Htldpt =  create_buffer("Htldpt",Hoteldpt)
        Ginfo =  create_buffer("Ginfo",Guest_queasy)
        sub_str = translateExtended ("SUBTOTAL", lvcarea, "")
        output_list_data.clear()

        for ginfo in db_session.query(Ginfo).filter(
                 (Ginfo.key == ("gast-info").lower()) & (Ginfo.gastnr == gastnr)).order_by(Ginfo.number1, Ginfo.date1).all():

            if curr_dept != ginfo.number1 and curr_dept != 0:
                i = i + 1
                str1 = fill("-", 94)
                add_line(i, str1, 0, 0, None)
                i = i + 1
                str1 = to_string(sub_str, "x(24)") + to_string(sub_tot, "->>>,>>>,>>9")
                invdept = ginfo.number1
                invno = to_int(ginfo.char1)
                invdate = ginfo.date1


                add_line(i, str1, invdept, invno, invdate)
                sub_tot =  to_decimal("0")
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
            str1 = to_string(dept_str, "x(24)") + to_string(ginfo.deci3, "->>>,>>>,>>9") + to_string(cistr, "x(8)") + to_string(costr, "x(8)") + to_string(ginfo.deci1, "->>>,>>>,>>9") + to_string(ginfo.deci2, "->>>,>>>,>>9") + to_string(rmno, "x(6)") + to_string(rmcat, "x(4)")
            invdept = ginfo.number1
            invno = to_int(ginfo.char1)
            invdate = ginfo.date1


            add_line(i, str1, invdept, invno, invdate)
            curr_dept = ginfo.number1
            sub_tot =  to_decimal(sub_tot) + to_decimal(ginfo.deci3)

        if it_exists:
            i = i + 1
            str1 = fill("-", 94)
            add_line(i, str1, 0, 0, None)
            i = i + 1
            str1 = to_string(sub_str, "x(24)") + to_string(sub_tot, "->>>,>>>,>>9")
            add_line(i, str1, 0, 0, None)


    def add_line(nr:int, str1:string, dept:int, rechnr:int, datum:date):

        nonlocal payment, t_guest_data, output_list_data, lvcarea, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal pvilanguage, gastnr


        nonlocal output_list, t_guest
        nonlocal output_list_data, t_guest_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.nr = nr
        output_list.str = str1
        output_list.dept = dept
        output_list.rechnr = rechnr
        output_list.datum = datum

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        t_guest = T_guest()
        t_guest_data.append(t_guest)

        buffer_copy(guest, t_guest)

        if guest.zahlungsart > 0:

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, guest.zahlungsart)]})

            if artikel:
                payment = to_string(guest.zahlungsart) + " - " + artikel.bezeich
    create_list()

    return generate_output()