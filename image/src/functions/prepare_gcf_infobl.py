from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Artikel, Res_line, Hoteldpt, Guest_queasy, Zimmer, Zimkateg, History

def prepare_gcf_infobl(pvilanguage:int, gastnr:int):
    payment = ""
    t_guest_list = []
    output_list_list = []
    lvcarea:str = "prepare_gcf_info"
    guest = artikel = res_line = hoteldpt = guest_queasy = zimmer = zimkateg = history = None

    output_list = t_guest = reslin = htldpt = ginfo = None

    output_list_list, Output_list = create_model("Output_list", {"nr":int, "dept":int, "rechnr":int, "datum":date, "str":str})
    t_guest_list, T_guest = create_model_like(Guest)

    Reslin = Res_line
    Htldpt = Hoteldpt
    Ginfo = Guest_queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment, t_guest_list, output_list_list, lvcarea, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal reslin, htldpt, ginfo


        nonlocal output_list, t_guest, reslin, htldpt, ginfo
        nonlocal output_list_list, t_guest_list
        return {"payment": payment, "t-guest": t_guest_list, "output-list": output_list_list}

    def create_list():

        nonlocal payment, t_guest_list, output_list_list, lvcarea, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal reslin, htldpt, ginfo


        nonlocal output_list, t_guest, reslin, htldpt, ginfo
        nonlocal output_list_list, t_guest_list

        str1:str = ""
        i:int = 0
        dept_str:str = ""
        cistr:str = ""
        costr:str = ""
        curr_dept:int = 0
        sub_tot:decimal = 0
        sub_str:str = ""
        it_exists:bool = False
        rmno:str = ""
        rmcat:str = ""
        invdept:int = 0
        invno:int = 0
        invdate:date = None
        Reslin = Res_line
        Htldpt = Hoteldpt
        Ginfo = Guest_queasy
        sub_str = translateExtended ("SUBTOTAL", lvcarea, "")
        output_list_list.clear()

        for ginfo in db_session.query(Ginfo).filter(
                (func.lower(Ginfo.key) == "gast_info") &  (Ginfo.gastnr == gastnr)).all():

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
                sub_tot = 0
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
                    (Reslin.resnr == ginfo.number2) &  (Reslin.reslinnr == ginfo.number3)).first()

            if reslin:
                cistr = to_string(reslin.ankunft, "99/99/99")
                costr = to_string(reslin.abreise, "99/99/99")
                rmno = reslin.zinr

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.zinr) == (rmno).lower())).first()

                if zimmer:

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == zimmer.zikatnr)).first()

                if zimkateg:
                    rmcat = zimkateg.kurzbez
            else:

                history = db_session.query(History).filter(
                        (History.gastnr == gastnr) &  (History.resnr == ginfo.number2) &  (History.reslinnr == ginfo.number3)).first()

                if history:
                    cistr = to_string(history.ankunft, "99/99/99")
                    costr = to_string(history.abreise, "99/99/99")
                    rmno = history.zinr

                    zimmer = db_session.query(Zimmer).filter(
                            (func.lower(Zimmer.zinr) == (rmno).lower())).first()

                    if zimmer:

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == zimmer.zikatnr)).first()

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
            sub_tot = sub_tot + ginfo.deci3

        if it_exists:
            i = i + 1
            str1 = fill("-", 94)
            add_line(i, str1, 0, 0, None)
            i = i + 1
            str1 = to_string(sub_str, "x(24)") + to_string(sub_tot, "->>>,>>>,>>9")
            add_line(i, str1, 0, 0, None)

    def add_line(nr:int, str1:str, dept:int, rechnr:int, datum:date):

        nonlocal payment, t_guest_list, output_list_list, lvcarea, guest, artikel, res_line, hoteldpt, guest_queasy, zimmer, zimkateg, history
        nonlocal reslin, htldpt, ginfo


        nonlocal output_list, t_guest, reslin, htldpt, ginfo
        nonlocal output_list_list, t_guest_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.nr = nr
        output_list.str = str1
        output_list.dept = dept
        output_list.rechnr = rechnr
        output_list.datum = datum


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    if guest:
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        buffer_copy(guest, t_guest)

        if guest.zahlungsart > 0:

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (Artikel.artnr == guest.zahlungsart)).first()

            if artikel:
                payment = to_string(guest.zahlungsart) + "  -  " + artikel.bezeich
    create_list()

    return generate_output()