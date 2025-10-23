#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 22-10-2025 
# Issue : 
# - New compile program
# - Fix space in string 
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Htparam, Nightaudit, Nitestor, Guest, Zimkateg, Reservation, Res_line, Guestseg, Nation, Zimmer

def nt_pjarrive():

    prepare_cache ([Paramtext, Htparam, Nightaudit, Nitestor, Guest, Zimkateg, Reservation, Res_line, Nation, Zimmer])

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
    progname:string = "nt-PJarrive.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:string = ""
    p_width:int = 132
    p_length:int = 56
    curr_date:date = None
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    paramtext = htparam = nightaudit = nitestor = guest = zimkateg = reservation = res_line = guestseg = nation = zimmer = None

    s_list = cl_list = setup_list = None

    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "depart":date, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "bemerk":string})
    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_data, cl_list_data, setup_list_data

        return {}

    def arrival_list():

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_data, cl_list_data, setup_list_data

        i:int = 0
        str1:string = ""
        str2:string = ""
        it_exist:bool = False
        curr_grp:string = ""
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
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,58 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string 
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "EXPECTED ARRIVAL LIST" + " - " + to_string(curr_date)
        add_line(line)
        add_line(str1)
    
        # Rulita,
        # - Fix space in string 
        line = " " + "No   ResNo  Guest-Name                VIP  RmNo    RmCat  A/C Co Nat" + "  "
        line = line + "Company/TA          E.T.D.    Flight  Time   Remark"
        add_line(line)
        add_line(str1)
        add_line(" ")
        add_line("##end-header")

        for cl_list in query(cl_list_data):
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
                line = to_string(cl_list.nr, ">>9 ") + to_string(cl_list.resnr, ">>>>>>9 ") + to_string(cl_list.name, "x(24) ") + to_string(cl_list.vip, "x(3) ") + to_string(cl_list.rmno, "x(6) ") + to_string(cl_list.rmcat, "x(6) ") + to_string(cl_list.pax, "x(5) ") + to_string(cl_list.nat, "x(3) ") + to_string(cl_list.company, "x(18) ") + to_string(cl_list.depart) + " " + to_string(cl_list.flight, "x(6) ") + to_string(cl_list.etd, "99:99") + " " + to_string(cl_list.bemerk)
                add_line(line)
        add_line(" ")
        add_line(str1)

        if not it_exist:
            add_line("*** " + "No Arrival Guests found." + " ***")
        else:
            add_line(" ")
            add_line(" ")
            add_line("##header")
    
            # Rulita,
            # - Fix space in string             
            line = "SUMMARY      Room-Type             Qty      Nation" + "               "
            line = line + "Adult         (%)     Child"
            add_line(line)
            add_line(str2)
            add_line("##end-header")

            for s_list in query(s_list_data):
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
                    
            # Rulita,
            # - Fix space in string   
            line = line + "T O T A L            " + to_string(tot_rm, ">>>9")
            for i in range(1,27 + 1) :
                line = line + " "
                                    
            # Rulita,
            # - Fix space in string  
            line = line + to_string(tot_a + tot_co, ">>>>9") + "      100.00" + "     " + to_string(tot_c, ">>>>9")
            add_line(line)
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_data, cl_list_data, setup_list_data

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

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_data, cl_list_data, setup_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        gmember = None
        Gmember =  create_buffer("Gmember",Guest)

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        for res_line.setup, res_line.resnr, res_line.name, res_line.zinr, res_line.abreise, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.zimmeranz, res_line.bemerk, res_line.resstatus, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest._recid, gmember.name, gmember.vorname1, gmember._recid in db_session.query(Res_line.setup, Res_line.resnr, Res_line.name, Res_line.zinr, Res_line.abreise, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.zimmeranz, Res_line.bemerk, Res_line.resstatus, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest._recid, Gmember.name, Gmember.vorname1, Gmember._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                 (Res_line.active_flag == 0) & (Res_line.ankunft == curr_date)).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
            nr = nr + 1
            vip_flag = ""

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

            if guestseg:
                vip_flag = "VIP"
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

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
            cl_list.flight = substring(res_line.flight_nr, 0, 6)
            cl_list.etd = substring(res_line.flight_nr, 6, 5)
            cl_list.company = guest.name + ", " + guest.vorname1 +\
                    " " + guest.anrede1 + guest.anredefirma

            if cl_list.nat == "":
                cl_list.nat = "?"
            else:

                nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                if nation:
                    cl_list.nation = nation.bezeich
            cl_list.qty = res_line.zimmeranz
            for i in range(1,length(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(res_line.bemerk, i - 1, 1)

            if cl_list.rmno == "" and cl_list.qty > 1:
                cl_list.rmno = to_string(cl_list.qty, ">>>>>9")

            if res_line.resstatus == 3:
                                    
            # Rulita,
            # - Fix space in string 
                if cl_list.qty <= 9:
                    cl_list.rmno = "    T" + to_string(cl_list.qty, "9")

                elif cl_list.qty <= 99:
                    cl_list.rmno = "   T" + to_string(cl_list.qty, "99")

                elif cl_list.qty <= 999:
                    cl_list.rmno = "  T" + to_string(cl_list.qty, "999")
                                    
            # Rulita,
            # - Fix space in string 
            elif res_line.resstatus == 4:

                if cl_list.qty <= 9:
                    cl_list.rmno = "    W" + to_string(cl_list.qty, "9")

                elif cl_list.qty <= 99:
                    cl_list.rmno = "   W" + to_string(cl_list.qty, "99")

                elif cl_list.qty <= 999:
                    cl_list.rmno = "  W" + to_string(cl_list.qty, "999")
            cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")
            tot_rm = tot_rm + res_line.zimmeranz
            tot_a = tot_a + res_line.erwachs * res_line.zimmeranz
            tot_c = tot_c + (res_line.kind1 + res_line.kind2) * res_line.zimmeranz
            tot_co = tot_co + res_line.gratis * res_line.zimmeranz

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + (cl_list.a + cl_list.co) * cl_list.qty
            s_list.child = s_list.child + cl_list.c * cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = "UNKNOWN"
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

    def bed_setup():

        nonlocal tot_rm, tot_a, tot_c, tot_co, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, curr_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, guest, zimkateg, reservation, res_line, guestseg, nation, zimmer


        nonlocal s_list, cl_list, setup_list
        nonlocal s_list_data, cl_list_data, setup_list_data


        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.setup != 0)).order_by(Zimmer._recid).all():

            paramtext = db_session.query(Paramtext).filter(
                     ((Paramtext.txtnr - 9200) == zimmer.setup)).first()

            if paramtext:

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == (zimmer.setup + 1)), first=True)

                if not setup_list:
                    setup_list = Setup_list()
                    setup_list_data.append(setup_list)

                    setup_list.nr = zimmer.setup + 1
                    setup_list.char = substring(paramtext.notes, 0, 1)


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        bed_setup()
        create_arrival()
        arrival_list()

    return generate_output()