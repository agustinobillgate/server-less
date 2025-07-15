from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Htparam, Nightaudit, Nitestor, Zimkateg, Guest, Res_line

def nt_departurerm():
    n:int = 0
    progname:str = "nt-departureRm.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 88
    p_length:int = 56
    curr_date:date = None
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    paramtext = htparam = nightaudit = nitestor = zimkateg = guest = res_line = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "name":str, "arrival":date, "rmcat":str, "rmno":str, "a":int, "c":int, "co":int, "argt":str, "company":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {}

    def departure_list():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,18 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,18 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "ACTUAL DEPARTED GUEST LIST" + " - " + to_string(curr_date)
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "Guest-Name Arrival RmCat RmNo A C CO Argt Company / TA" + " "
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_list, sort_by=[("flag",False),("rmno",False)]):
            it_exist = True

            if cl_list.flag == 1:
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)
                line = to_string(cl_list.name, "x(24) ") + to_string("", "x(8) ") + to_string(cl_list.rmcat, "x(6) ") + to_string(cl_list.rmno, "x(6) ") + to_string(cl_list.a, ">>9 ") + to_string(cl_list.c, ">>9 ") + to_string(cl_list.co, ">9 ") + to_string(cl_list.argt, "x(4) ") + to_string(cl_list.company, "x(24)")
                add_line(line)
            else:
                line = to_string(cl_list.name, "x(24) ") + to_string(cl_list.arrival) + " " + to_string(cl_list.rmcat, "x(6) ") + to_string(cl_list.rmno, "x(6) ") + to_string(cl_list.a, ">>9 ") + to_string(cl_list.c, ">>9 ") + to_string(cl_list.co, ">9 ") + to_string(cl_list.argt, "x(4) ") + to_string(cl_list.company, "x(24)")
                add_line(line)

        if not it_exist:
            add_line("*** " + "No Departed Guests found." + " ***")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        nitestor = db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge) & (Nitestor.line_nr == line_nr)).first()

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1


    def create_departure():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        tot_rm:int = 0
        tot_a:int = 0
        tot_c:int = 0
        tot_co:int = 0

        res_line_obj_list = []
        for res_line, zimkateg, guest in db_session.query(Res_line, Zimkateg, Guest).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name, Res_line.zinr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.name = res_line.name
            cl_list.arrival = res_line.ankunft
            cl_list.rmcat = zimkateg.kurzbez
            cl_list.rmno = res_line.zinr
            cl_list.a = res_line.erwachs
            cl_list.c = res_line.kind1
            cl_list.co = res_line.gratis
            cl_list.argt = res_line.arrangement
            cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

            if not res_line.zimmerfix:
                tot_rm = tot_rm + 1
            tot_a = tot_a + res_line.erwachs
            tot_c = tot_c + res_line.kind1
            tot_co = tot_co + res_line.gratis
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 1
        cl_list.rmcat = "TOTAL"
        cl_list.rmno = to_string(tot_rm, ">>>>>9")
        cl_list.a = tot_a
        cl_list.c = tot_c
        cl_list.co = tot_co

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()
    htl_adr = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()
    htl_tel = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    curr_date = htparam.fdate

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:
        pass
    else:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_departure()
        departure_list()

    return generate_output()