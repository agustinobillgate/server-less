from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Htparam, Nightaudit, Nitestor, Guest, Zimkateg, Reservation, Res_line, Guestseg, Nation, Zimmer

def nt_pjdepart():
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    n:int = 0
    progname:str = "nt-PJdepart.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 132
    p_length:int = 56
    curr_date:date = None
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    paramtext = htparam = nightaudit = nitestor = guest = zimkateg = reservation = res_line = guestseg = nation = zimmer = None

    s_list = cl_list = setup_list = None

    s_list_list, S_list = create_model("S_list", {"rmcat":str, "bezeich":str, "nat":str, "anz":int, "adult":int, "proz":decimal, "child":int})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "depart":date, "rmcat":str, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "bemerk":str})
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_list, cl_list_list, setup_list_list

        return {}

    def departure_list():

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_list, cl_list_list, setup_list_list

        i:int = 0
        str1:str = ""
        str2:str = ""
        it_exist:bool = False
        curr_grp:str = ""
        for i in range(1,p_width + 1) :
            str1 = str1 + "="
        for i in range(1,94 + 1) :
            str2 = str2 + "-"
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,58 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,58 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "EXPECTED DEPARTURE LIST" + " - " + to_string(curr_date)
        add_line(line)
        add_line(str1)
        line = " " + "No Guest-Name VIP RmNo RmCat A/C Co Nat" + " "
        line = line + "Company/TA Check-in Flight Time Remark"
        add_line(line)
        add_line(str1)
        add_line(" ")
        add_line("##end-header")

        for cl_list in query(cl_list_list):
            it_exist = True

            if cl_list.flag == 1:
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "="
            else:

                if cl_list.groupname != "" and curr_grp != cl_list.groupname:
                    curr_grp = cl_list.groupname
                    line = " " + cl_list.groupname
                    add_line(" ")
                    add_line(line)
                line = to_string(cl_list.nr, ">>9 ") + to_string(cl_list.name, "x(24) ") + to_string(cl_list.vip, "x(3) ") + to_string(cl_list.rmno, "x(6) ") + to_string(cl_list.rmcat, "x(6) ") + to_string(cl_list.pax, "x(5) ") + to_string(cl_list.nat, "x(3) ") + to_string(cl_list.company, "x(18) ") + to_string(cl_list.depart) + " " + to_string(cl_list.flight, "x(6) ") + to_string(cl_list.etd, "99:99") + " " + to_string(cl_list.bemerk)
                add_line(line)
        add_line(" ")
        add_line(str1)

        if not it_exist:
            add_line("*** " + "No Departure Guests found." + " ***")
        else:
            add_line(" ")
            add_line(" ")
            add_line("##header")
            line = "SUMMARY Room-Type Qty Nation" + " "
            line = line + "Adult (%) Child"
            add_line(line)
            add_line(str2)
            add_line("##end-header")

            for s_list in query(s_list_list):
                line = ""

                if s_list.rmcat != "":
                    line = " " + to_string(s_list.bezeich, "x(20) ") + to_string(s_list.anz, ">>9 ") + " "
                else:
                    for i in range(1,44 + 1) :
                        line = line + " "

                if s_list.nat != "":
                    line = line + to_string(s_list.nat, "x(20) ") + to_string(s_list.adult, ">>>>9 ") + to_string(s_list.proz, " >>9.99 ") + to_string(s_list.child, ">>>>9")
                else:
                    for i in range(1,50 + 1) :
                        line = line + " "
                add_line(line)
            add_line(str2)
            line = ""
            for i in range(1,13 + 1) :
                line = line + " "
            line = line + "T O T A L " + to_string(tot_rm, ">>>9")
            for i in range(1,27 + 1) :
                line = line + " "
            line = line + to_string(tot_a + tot_co, ">>>>9") + " 100.00" + " " + to_string(tot_c, ">>>>9")
            add_line(line)
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_list, cl_list_list, setup_list_list

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

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_list, cl_list_list, setup_list_list

        i:int = 0
        vip_flag:str = ""
        nr:int = 0
        gmember = None
        Gmember =  create_buffer("Gmember",Guest)

        res_line_obj_list = []
        for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.abreise == curr_date)).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            setup_list = query(setup_list_list, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
            nr = nr + 1
            vip_flag = ""

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

            if guestseg:
                vip_flag = "VIP"
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.nr = nr
            cl_list.groupname = reservation.groupname
            cl_list.rmcat = zimkateg.kurzbez + setup_list.char
            cl_list.kurzbez = zimkateg.kurzbez
            cl_list.bezeich = zimkateg.bezeichnung
            cl_list.nat = gmember.nation1
            cl_list.resnr = res_line.resnr
            cl_list.vip = vip_flag
            cl_list.name = res_line.name
            cl_list.rmno = res_line.zinr
            cl_list.depart = res_line.abreise
            cl_list.a = res_line.erwachs
            cl_list.c = res_line.kind1 + res_line.kind2
            cl_list.co = res_line.gratis
            cl_list.argt = res_line.arrangement
            cl_list.flight = substring(res_line.flight_nr, 11, 6)
            cl_list.etd = substring(res_line.flight_nr, 17, 5)
            cl_list.company = guest.name + ", " + guest.vorname1 +\
                    " " + guest.anrede1 + guest.anredefirma

            if cl_list.nat == "":
                cl_list.nat = "?"
            else:

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == cl_list.nat)).first()

                if nation:
                    cl_list.nation = nation.bezeich

            if res_line.resstatus == 6:
                cl_list.qty = 1
            for i in range(1,len(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr (10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(res_line.bemerk, i - 1, 1)
            cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")
            tot_rm = tot_rm + 1
            tot_a = tot_a + res_line.erwachs
            tot_c = tot_c + res_line.kind1 + res_line.kind2
            tot_co = tot_co + res_line.gratis

        for cl_list in query(cl_list_list, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_list, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = "UNKNOWN"
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

    def bed_setup():

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_list, cl_list_list, setup_list_list


        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.setup != 0)).order_by(Zimmer._recid).all():

            paramtext = db_session.query(Paramtext).filter(
                     ((Paramtext.txtnr - 9200) == zimmer.setup)).first()

            if paramtext:

                setup_list = query(setup_list_list, filters=(lambda setup_list: setup_list.nr == (zimmer.setup + 1)), first=True)

                if not setup_list:
                    setup_list = Setup_list()
                    setup_list_list.append(setup_list)

                    setup_list.nr = zimmer.setup + 1
                    setup_list.char = substring(paramtext.notes, 0, 1)


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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

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
        bed_setup()
        create_departure()
        departure_list()

    return generate_output()