#using conversion tools version: 1.0.0.117

# ========================================================
# Rulita, 22-10-2025 
# Issue : New compile program

# Rulita, 10-11-2025 
# Issue :
# - Fixing foreach first menjadi foreach find first di py
# - Fixing to_string var table guest 
# ========================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Htparam, Nightaudit, Nitestor, Zimkateg, Guest, Res_line, Bill

def nt_arrival():

    prepare_cache ([Paramtext, Htparam, Nightaudit, Nitestor, Zimkateg, Guest, Res_line])

    n:int = 0
    progname:string = "nt-arrival.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 86
    p_length:int = 56
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    curr_date:date = None
    paramtext = htparam = nightaudit = nitestor = zimkateg = guest = res_line = bill = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "name":string, "depart":date, "rmcat":string, "rmno":string, "a":int, "c":int, "co":int, "argt":string, "company":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line, bill


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def arrival_list():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line, bill


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,18 + 1) :
            line = line + " "
        line = line + "Date/Time : " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,18 + 1) :
            line = line + " "
        line = line + "Page" + " : " + "##page"
        add_line(line)
        add_line(" ")
        line = "ACTUAL ARRIVED GUEST LIST" + " - " + to_string(curr_date)
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "Guest-Name Depart RmCat RmNo A C CO Argt Company / TA"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_data):
            it_exist = True

            if cl_list.flag == 1:
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)
                line = to_string(cl_list.name, "x(24) ") + to_string("", "x(8) ") + to_string(cl_list.rmcat, "x(6) ") + to_string(cl_list.rmno, "x(4) ") + to_string(cl_list.a, ">>9 ") + to_string(cl_list.c, ">>9 ") + to_string(cl_list.co, ">9 ") + to_string(cl_list.argt, "x(4) ") + to_string(cl_list.company, "x(24)")
                add_line(line)
            else:
                line = to_string(cl_list.name, "x(24) ") + to_string(cl_list.depart) + " " + to_string(cl_list.rmcat, "x(6) ") + to_string(cl_list.rmno, "x(4) ") + to_string(cl_list.a, ">>9 ") + to_string(cl_list.c, ">>9 ") + to_string(cl_list.co, ">9 ") + to_string(cl_list.argt, "x(4) ") + to_string(cl_list.company, "x(24)")
                add_line(line)

        if not it_exist:
            add_line("*** " + "No Arrival Guests found." + " ***")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line, bill


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        nitestor = get_cache (Nitestor, {"night_type": [(eq, night_type)],"reihenfolge": [(eq, reihenfolge)],"line_nr": [(eq, line_nr)]})

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1
        pass


    def create_arrival():

        nonlocal n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, paramtext, htparam, nightaudit, nitestor, zimkateg, guest, res_line, bill


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        tot_rm:int = 0
        tot_a:int = 0
        tot_c:int = 0
        tot_co:int = 0

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        guest = Guest()
        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.ankunft == curr_date)).order_by(Res_line.name, Res_line.zinr).all():

            # zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
            zimkateg = db_session.query(Zimkateg).filter((Zimkateg.zikatnr == res_line.zikatnr)).first()

            # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
            guest = db_session.query(Guest).filter((Guest.gastnr == res_line.gastnr)).first()

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.name = res_line.name
            cl_list.depart = res_line.abreise
            cl_list.rmcat = zimkateg.kurzbez
            cl_list.rmno = res_line.zinr
            cl_list.a = res_line.erwachs
            cl_list.c = res_line.kind1
            cl_list.co = res_line.gratis
            cl_list.argt = res_line.arrangement
            cl_list.company = to_string(guest.name) + ", " + to_string(guest.vorname1) + " " + to_string(guest.anrede1) + to_string(guest.anredefirma)

            if res_line.resstatus == 6:
                tot_rm = tot_rm + 1
            tot_a = tot_a + res_line.erwachs
            tot_c = tot_c + res_line.kind1
            tot_co = tot_co + res_line.gratis

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == curr_date) & (Res_line.abreise == curr_date)).order_by(Res_line.name, Res_line.zinr).all():
            
            bill = db_session.query(Bill).filter((Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr) & (Bill.argtumsatz > 0)).first()

            zimkateg = db_session.query(Zimkateg).filter((Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter((Guest.gastnr == res_line.gastnr)).first()
            
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.name = res_line.name
            cl_list.depart = res_line.abreise
            cl_list.rmcat = zimkateg.kurzbez
            cl_list.rmno = res_line.zinr
            cl_list.a = res_line.erwachs
            cl_list.c = res_line.kind1
            cl_list.co = res_line.gratis
            cl_list.argt = res_line.arrangement
            cl_list.company = to_string(guest.name) + ", " + to_string(guest.vorname1) + " " + to_string(guest.anrede1) + to_string(guest.anredefirma)

            if not res_line.zimmerfix:
                tot_rm = tot_rm + 1
            tot_a = tot_a + res_line.erwachs
            tot_c = tot_c + res_line.kind1
            tot_co = tot_co + res_line.gratis
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 1
        cl_list.rmcat = "TOTAL"
        cl_list.rmno = to_string(tot_rm, ">>>9")
        cl_list.a = tot_a
        cl_list.c = tot_c
        cl_list.co = tot_co

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    curr_date = htparam.fdate

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_arrival()
        arrival_list()

    return generate_output()