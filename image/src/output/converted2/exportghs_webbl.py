from functions.additional_functions import *
import decimal
from datetime import date
from functions.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
from models import Guest, Zimkateg, Reservation, Sourccod, Segment, Queasy, Res_line, Htparam, Nation

nation_list, Nation = create_model("Nation", {"nr":int, "nation_code":str, "nation_name":str, "nation_iso2":str, "nation_iso3":str})

def exportghs_webbl(nation_list:[Nation], currdate:date, propid:str, tax_incl:bool):
    p_list_list = []
    x_list_list = []
    r_list_list = []
    guest = zimkateg = reservation = sourccod = segment = queasy = res_line = htparam = nation = None

    p_list = x_list = r_list = nation = None

    p_list_list, P_list = create_model("P_list", {"confno":str, "arrdate":str, "depdate":str, "roomtype":str, "roomno":str, "roomrate":decimal, "gname":str, "comp":str, "sourcename":str, "memberno":str, "totrev":decimal, "rmrev":decimal, "fbrev":decimal, "others":decimal, "propid":str, "reward":str, "bookdate":str, "market":str, "note":str, "profile":str, "exportdate":str, "ratecode":str})
    x_list_list, X_list = create_model("X_list", {"confno":str, "arrdate":str, "depdate":str, "roomtype":str, "roomrate":decimal, "gname":str, "comp":str, "sourcename":str, "memberno":str, "profile":str, "email":str, "totrev":decimal, "rmrev":decimal, "fbrev":decimal, "others":decimal, "propid":str, "bookdate":str, "market":str, "bookstatus":str, "adult":int, "child":int, "note":str})
    r_list_list, R_list = create_model("R_list", {"email":str, "g_title":str, "firstname":str, "lastname":str, "cardname":str, "mobile":str, "phone":str, "postcode":str, "fax":str, "address1":str, "address2":str, "city":str, "state":str, "country":str, "nationality":str, "memberno":str, "propid":str, "profile":str, "confno":str, "note":str, "passport":str, "idcard":str, "birthdate":str, "gender":str, "comp":str, "compno":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_list_list, x_list_list, r_list_list, guest, zimkateg, reservation, sourccod, segment, queasy, res_line, htparam, nation
        nonlocal currdate, propid, tax_incl


        nonlocal p_list, x_list, r_list, nation
        nonlocal p_list_list, x_list_list, r_list_list, nation_list
        return {"p-list": p_list_list, "x-list": x_list_list, "r-list": r_list_list}

    def ghs_p1_checkout():

        nonlocal p_list_list, x_list_list, r_list_list, guest, zimkateg, reservation, sourccod, segment, queasy, res_line, htparam, nation
        nonlocal currdate, propid, tax_incl


        nonlocal p_list, x_list, r_list, nation
        nonlocal p_list_list, x_list_list, r_list_list, nation_list

        birthdate:str = ""
        str_rsv:str = ""
        contcode:str = ""
        loop_i:int = 0
        curr_i:int = 0
        rsv_date:date = None
        to_date:date = None
        datum1:date = None
        flodging:decimal = to_decimal("0.0")
        lodging:decimal = to_decimal("0.0")
        breakfast:decimal = to_decimal("0.0")
        lunch:decimal = to_decimal("0.0")
        dinner:decimal = to_decimal("0.0")
        others:decimal = to_decimal("0.0")
        rmrate:decimal = to_decimal("0.0")
        net_vat:decimal = to_decimal("0.0")
        net_service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        t_rmrev:decimal = to_decimal("0.0")
        t_fbrev:decimal = to_decimal("0.0")
        t_others:decimal = to_decimal("0.0")
        ci_date:str = ""
        co_date:str = ""
        gmember = None
        gcomp = None
        Gmember =  create_buffer("Gmember",Guest)
        Gcomp =  create_buffer("Gcomp",Guest)

        res_line_obj_list = []
        for res_line, gmember, zimkateg, reservation, sourccod, segment, queasy in db_session.query(Res_line, Gmember, Zimkateg, Reservation, Sourccod, Segment, Queasy).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Queasy,(Queasy.key == 152) & (Queasy.number1 == Zimkateg.typ)).filter(
                 (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == currdate)).order_by(Res_line._recid).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_rmrev =  to_decimal("0")
            t_fbrev =  to_decimal("0")
            t_others =  to_decimal("0")
            curr_i = 0

            if gmember:
                p_list = P_list()
                p_list_list.append(p_list)

                p_list.confno = propid + "-" + to_string(res_line.resnr) + to_string(res_line.reslinnr, "999")
                p_list.roomno = res_line.zinr
                p_list.roomrate =  to_decimal(res_line.zipreis)
                p_list.sourcename = sourccod.bezeich
                p_list.market = segment.bezeich
                p_list.note = res_line.bemerk
                p_list.memberno = ""
                p_list.reward = ""
                p_list.profile = propid + "-" + to_string(gmember.gastnr)
                p_list.propid = propid
                p_list.gname = gmember.vorname1 + " " + gmember.name + "," + gmember.anrede1

                if re.match(r".*SSRS.*",propid, re.IGNORECASE):
                    p_list.roomtype = queasy.char1
                else:
                    p_list.roomtype = zimkateg.kurzbez
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str_rsv, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str_rsv, 6)
                p_list.ratecode = contcode

                if session_date_format() == ("dmy").lower() :
                    rsv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

                elif session_date_format() == ("mdy").lower() :
                    rsv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
                else:
                    rsv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

                if rsv_date != None:
                    p_list.bookdate = to_string(get_year(rsv_date) , "9999") + "-" + to_string(get_month(rsv_date) , "99") + "-" + to_string(get_day(rsv_date) , "99")
                else:
                    p_list.bookdate = ""
                p_list.exportdate = to_string(get_year(get_current_date()) , "9999") + "-" + to_string(get_month(get_current_date()) , "99") + "-" + to_string(get_day(get_current_date()) , "99")

                if res_line.ankunft == res_line.abreise:
                    to_date = res_line.abreise
                else:
                    to_date = res_line.abreise - timedelta(days=1)
                for datum1 in date_range(res_line.ankunft,to_date) :
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum1, curr_i, currdate))

                    if not tax_incl:
                        t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging) - to_decimal(net_vat) - to_decimal(net_service)
                    else:
                        t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging)
                    t_fbrev =  to_decimal(t_fbrev) + to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)
                    t_others =  to_decimal(t_others) + to_decimal(others)


                p_list.rmrev = to_decimal(round(t_rmrev , 2))
                p_list.fbrev = to_decimal(round(t_fbrev , 2))
                p_list.others = to_decimal(round(t_others , 2))
                p_list.totrev =  to_decimal(p_list.rmrev) + to_decimal(p_list.fbrev) + to_decimal(p_list.others)

                if res_line.ankunft != None:
                    ci_date = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" + to_string(get_day(res_line.ankunft) , "99")
                else:
                    ci_date = ""

                if res_line.abreise != None:
                    co_date = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
                p_list.arrdate = ci_date
                p_list.depdate = co_date

                gcomp = db_session.query(Gcomp).filter(
                         (Gcomp.gastnr == gmember.master_gastnr)).first()

                if gcomp:
                    p_list.comp = gcomp.name + ", " + gcomp.anredefirma

        for p_list in query(p_list_list):
            p_list.confno = replace_str(p_list.confno, ",", " ")
            p_list.arrdate = replace_str(p_list.arrdate, ",", " ")
            p_list.depdate = replace_str(p_list.depdate, ",", " ")
            p_list.roomno = replace_str(p_list.roomno, ",", " ")
            p_list.roomtype = replace_str(p_list.roomtype, ",", " ")
            p_list.sourcename = replace_str(p_list.sourcename, ",", " ")
            p_list.memberno = replace_str(p_list.memberno, ",", " ")
            p_list.propid = replace_str(p_list.propid, ",", " ")
            p_list.reward = replace_str(p_list.reward, ",", " ")
            p_list.bookdate = replace_str(p_list.bookdate, ",", " ")
            p_list.exportdate = replace_str(p_list.exportdate, ",", " ")
            p_list.market = replace_str(p_list.market, ",", " ")
            p_list.profil = replace_str(p_list.profil, ",", " ")
            p_list.gname = replace_str(p_list.gname, ",", " ")
            p_list.ratecode = replace_str(p_list.ratecode, chr(10) , " ")
            p_list.comp = replace_str(p_list.comp, ",", " ")


    def ghs_x1_forecast():

        nonlocal p_list_list, x_list_list, r_list_list, guest, zimkateg, reservation, sourccod, segment, queasy, res_line, htparam, nation
        nonlocal currdate, propid, tax_incl


        nonlocal p_list, x_list, r_list, nation
        nonlocal p_list_list, x_list_list, r_list_list, nation_list

        birthdate:str = ""
        str_rsv:str = ""
        contcode:str = ""
        loop_i:int = 0
        curr_i:int = 0
        rsv_date:date = None
        to_date:date = None
        datum1:date = None
        flodging:decimal = to_decimal("0.0")
        lodging:decimal = to_decimal("0.0")
        breakfast:decimal = to_decimal("0.0")
        lunch:decimal = to_decimal("0.0")
        dinner:decimal = to_decimal("0.0")
        others:decimal = to_decimal("0.0")
        rmrate:decimal = to_decimal("0.0")
        net_vat:decimal = to_decimal("0.0")
        net_service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        t_rmrev:decimal = to_decimal("0.0")
        t_fbrev:decimal = to_decimal("0.0")
        t_others:decimal = to_decimal("0.0")
        ci_date:str = ""
        co_date:str = ""
        gmember = None
        gcomp = None
        Gmember =  create_buffer("Gmember",Guest)
        Gcomp =  create_buffer("Gcomp",Guest)

        res_line_obj_list = []
        for res_line, gmember, reservation, segment, sourccod, zimkateg, queasy in db_session.query(Res_line, Gmember, Reservation, Segment, Sourccod, Zimkateg, Queasy).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Queasy,(Queasy.key == 152) & (Queasy.number1 == Zimkateg.typ)).filter(
                 ((Res_line.ankunft <= currdate) & (Res_line.abreise >= currdate)) | (((Res_line.resstatus == 1) | (Res_line.resstatus == 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0))).order_by(Res_line._recid).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_rmrev =  to_decimal("0")
            t_fbrev =  to_decimal("0")
            t_others =  to_decimal("0")
            curr_i = 0


            x_list = X_list()
            x_list_list.append(x_list)

            x_list.confno = propid + "-" + to_string(res_line.resnr) + to_string(res_line.reslinnr, "999")
            x_list.roomrate =  to_decimal(res_line.zipreis)
            x_list.sourcename = sourccod.bezeich
            x_list.market = segment.bezeich
            x_list.note = res_line.bemerk
            x_list.memberno = ""
            x_list.profile = propid + "-" + to_string(gmember.gastnr)
            x_list.propid = propid
            x_list.gname = gmember.vorname1 + " " + gmember.name + "," + gmember.anrede1
            x_list.adult = res_line.erwachs
            x_list.child = res_line.kind1 + res_line.kind2

            if re.match(r".*SSRS.*",propid, re.IGNORECASE):
                x_list.roomtype = queasy.char1
            else:
                x_list.roomtype = zimkateg.kurzbez

            if res_line.resstatus != 9:
                x_list.bookstatus = "BOOKING"

            elif res_line.resstatus == 9 or res_line.resstatus == 10:
                x_list.bookstatus = "CANCEL"

            if session_date_format() == ("dmy").lower() :
                rsv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

            elif session_date_format() == ("mdy").lower() :
                rsv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
            else:
                rsv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

            if rsv_date != None:
                x_list.bookdate = to_string(get_year(rsv_date) , "9999") + "-" + to_string(get_month(rsv_date) , "99") + "-" + to_string(get_day(rsv_date) , "99")
            else:
                x_list.bookdate = ""

            if res_line.ankunft == res_line.abreise:
                to_date = res_line.abreise
            else:
                to_date = res_line.abreise - timedelta(days=1)
            for datum1 in date_range(res_line.ankunft,to_date) :
                curr_i = curr_i + 1
                flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum1, curr_i, currdate))

                if not tax_incl:
                    t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging) - to_decimal(net_vat) - to_decimal(net_service)
                else:
                    t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging)
                t_fbrev =  to_decimal(t_fbrev) + to_decimal(breakfast) + to_decimal(lunch)
                t_others =  to_decimal(t_others) + to_decimal(others)


            x_list.rmrev = to_decimal(round(t_rmrev , 2))
            x_list.fbrev = to_decimal(round(t_fbrev , 2))
            x_list.others = to_decimal(round(t_others , 2))
            x_list.totrev =  to_decimal(x_list.rmrev) + to_decimal(x_list.fbrev) + to_decimal(x_list.others)

            if res_line.ankunft != None:
                ci_date = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" + to_string(get_day(res_line.ankunft) , "99")
            else:
                ci_date = ""

            if res_line.abreise != None:
                co_date = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
            x_list.arrdate = ci_date
            x_list.depdate = co_date

            gcomp = db_session.query(Gcomp).filter(
                     (Gcomp.gastnr == gmember.master_gastnr)).first()

            if gcomp:
                x_list.comp = gcomp.name + ", " + gcomp.anredefirma

        for x_list in query(x_list_list):
            x_list.confno = replace_str(x_list.confno, ",", " ")
            x_list.arrdate = replace_str(x_list.arrdate, ",", " ")
            x_list.depdate = replace_str(x_list.depdate, ",", " ")
            x_list.roomtype = replace_str(x_list.roomtype, ",", " ")
            x_list.sourcename = replace_str(x_list.sourcename, ",", " ")
            x_list.memberno = replace_str(x_list.memberno, ",", " ")
            x_list.profile = replace_str(x_list.profile, ",", " ")
            x_list.email = replace_str(x_list.email, ",", " ")
            x_list.propid = replace_str(x_list.propid, ",", " ")
            x_list.bookdate = replace_str(x_list.bookdate, ",", " ")
            x_list.market = replace_str(x_list.market, ",", " ")
            x_list.bookstatus = replace_str(x_list.bookstatus, ",", " ")
            x_list.gname = replace_str(x_list.gname, ",", " ")
            x_list.comp = replace_str(x_list.comp, ",", " ")


    def ghs_r1_checkin():

        nonlocal p_list_list, x_list_list, r_list_list, guest, zimkateg, reservation, sourccod, segment, queasy, res_line, htparam, nation
        nonlocal currdate, propid, tax_incl


        nonlocal p_list, x_list, r_list, nation
        nonlocal p_list_list, x_list_list, r_list_list, nation_list

        birthdate:str = ""
        gmember = None
        gcomp = None
        Gmember =  create_buffer("Gmember",Guest)
        Gcomp =  create_buffer("Gcomp",Guest)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 87)).first()

        res_line_obj_list = []
        for res_line, gmember in db_session.query(Res_line, Gmember).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                 (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.ankunft == Res_line.currdate)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == currdate) & (Res_line.abreise == Res_line.currdate)) | ((Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.ankunft == currdate) & (Res_line.currdate < htparam.fdate))).order_by(Res_line._recid).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if gmember:
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.email = gmember.email_adr
                r_list.g_title = gmember.anrede1
                r_list.firstname = gmember.vorname1
                r_list.lastname = gmember.name
                r_list.cardname = gmember.vorname1 + " " + gmember.name
                r_list.mobile = gmember.mobil_telefon
                r_list.phone = gmember.telefon
                r_list.postcode = gmember.plz
                r_list.fax = gmember.fax
                r_list.address1 = gmember.adresse1
                r_list.address2 = gmember.adresse2
                r_list.city = gmember.wohnort
                r_list.state = gmember.geburt_ort2
                r_list.country = gmember.land
                r_list.nationality = gmember.nation1
                r_list.memberno = ""
                r_list.propid = propid
                r_list.profile = propid + "-" + to_string(gmember.gastnr)
                r_list.confno = propid + "-" + to_string(res_line.resnr) + to_string(res_line.reslinnr, "999")
                r_list.note = gmember.bemerkung

                if gmember.geburt_ort1.lower()  == ("Passport").lower() :
                    r_list.passport = gmember.ausweis_nr1
                else:
                    r_list.idcard = gmember.ausweis_nr1

                if gmember.geburtdatum1 == None:
                    birthdate = ""
                else:
                    birthdate = to_string(get_year(gmember.geburtdatum1) , "9999") + "-" + to_string(get_month(gmember.geburtdatum1) , "99") + "-" + to_string(get_day(gmember.geburtdatum1) , "99")
                r_list.birthdate = birthdate

                if gmember.geschlecht.lower()  == ("M").lower() :
                    r_list.gender = "Male"

                elif gmember.geschlecht.lower()  == ("F").lower() :
                    r_list.gender = "Female"

                gcomp = db_session.query(Gcomp).filter(
                         (Gcomp.gastnr == gmember.master_gastnr)).first()

                if gcomp:
                    r_list.comp = gcomp.name + ", " + gcomp.anredefirma
                    r_list.compno = gcomp.telefon

        for r_list in query(r_list_list):

            nation = db_session.query(Nation).filter(
                     (Nation.nation_code == r_list.country)).first()

            if nation:
                r_list.country = nation.nation_iso2
                r_list.nationality = nation.nation_iso2


            r_list.cardname = replace_str(r_list.cardname, ",", " ")
            r_list.firstname = replace_str(r_list.firstname, ",", " ")
            r_list.lastname = replace_str(r_list.lastname, ",", " ")
            r_list.comp = replace_str(r_list.comp, ",", " ")
            r_list.address1 = replace_str(r_list.address1, ",", " ")
            r_list.address2 = replace_str(r_list.address2, ",", " ")
            r_list.email = replace_str(r_list.email, ",", " ")
            r_list.g_title = replace_str(r_list.g_title, ",", " ")
            r_list.gender = replace_str(r_list.gender, ",", " ")
            r_list.birthdate = replace_str(r_list.birthdate, ",", " ")
            r_list.mobile = replace_str(r_list.mobile, ",", " ")
            r_list.phone = replace_str(r_list.phone, ",", " ")
            r_list.compno = replace_str(r_list.compno, ",", " ")
            r_list.postcode = replace_str(r_list.postcode, ",", " ")
            r_list.fax = replace_str(r_list.fax, ",", " ")
            r_list.city = replace_str(r_list.city, ",", " ")
            r_list.state = replace_str(r_list.state, ",", " ")
            r_list.passport = replace_str(r_list.passport, ",", " ")
            r_list.idcard = replace_str(r_list.idcard, ",", " ")
            r_list.memberno = replace_str(r_list.memberno, ",", " ")
            r_list.propid = replace_str(r_list.propid, ",", " ")
            r_list.profile = replace_str(r_list.profile, ",", " ")
            r_list.confno = replace_str(r_list.confno, ",", " ")
            r_list.email = replace_str(r_list.email, chr(10) , " ")
            r_list.firstname = replace_str(r_list.firstname, chr(10) , " ")
            r_list.lastname = replace_str(r_list.lastname, chr(10) , " ")
            r_list.cardname = replace_str(r_list.cardname, chr(10) , " ")
            r_list.comp = replace_str(r_list.comp, chr(10) , " ")
            r_list.address1 = replace_str(r_list.address1, chr(10) , " ")
            r_list.address2 = replace_str(r_list.address2, chr(10) , " ")
            r_list.g_title = replace_str(r_list.g_title, chr(10) , " ")
            r_list.gender = replace_str(r_list.gender, chr(10) , " ")
            r_list.birthdate = replace_str(r_list.birthdate, chr(10) , " ")
            r_list.mobile = replace_str(r_list.mobile, chr(10) , " ")
            r_list.phone = replace_str(r_list.phone, chr(10) , " ")
            r_list.compno = replace_str(r_list.compno, chr(10) , " ")
            r_list.postcode = replace_str(r_list.postcode, chr(10) , " ")
            r_list.fax = replace_str(r_list.fax, chr(10) , " ")
            r_list.city = replace_str(r_list.city, chr(10) , " ")
            r_list.state = replace_str(r_list.state, chr(10) , " ")
            r_list.passport = replace_str(r_list.passport, chr(10) , " ")
            r_list.idcard = replace_str(r_list.idcard, chr(10) , " ")
            r_list.memberno = replace_str(r_list.memberno, chr(10) , " ")
            r_list.propid = replace_str(r_list.propid, chr(10) , " ")
            r_list.profile = replace_str(r_list.profile, chr(10) , " ")
            r_list.confno = replace_str(r_list.confno, chr(10) , " ")
            r_list.email = replace_str(r_list.email, chr(13) , " ")
            r_list.firstname = replace_str(r_list.firstname, chr(13) , " ")
            r_list.lastname = replace_str(r_list.lastname, chr(13) , " ")
            r_list.cardname = replace_str(r_list.cardname, chr(13) , " ")
            r_list.comp = replace_str(r_list.comp, chr(13) , " ")
            r_list.address1 = replace_str(r_list.address1, chr(13) , " ")
            r_list.address2 = replace_str(r_list.address2, chr(13) , " ")
            r_list.g_title = replace_str(r_list.g_title, chr(13) , " ")
            r_list.gender = replace_str(r_list.gender, chr(13) , " ")
            r_list.birthdate = replace_str(r_list.birthdate, chr(13) , " ")
            r_list.mobile = replace_str(r_list.mobile, chr(13) , " ")
            r_list.phone = replace_str(r_list.phone, chr(13) , " ")
            r_list.compno = replace_str(r_list.compno, chr(13) , " ")
            r_list.postcode = replace_str(r_list.postcode, chr(13) , " ")
            r_list.fax = replace_str(r_list.fax, chr(13) , " ")
            r_list.city = replace_str(r_list.city, chr(13) , " ")
            r_list.state = replace_str(r_list.state, chr(13) , " ")
            r_list.passport = replace_str(r_list.passport, chr(13) , " ")
            r_list.idcard = replace_str(r_list.idcard, chr(13) , " ")
            r_list.memberno = replace_str(r_list.memberno, chr(13) , " ")
            r_list.propid = replace_str(r_list.propid, chr(13) , " ")
            r_list.profile = replace_str(r_list.profile, chr(13) , " ")
            r_list.confno = replace_str(r_list.confno, chr(13) , " ")
            r_list.note = replace_str(r_list.note, chr(10) , " ")
            r_list.note = replace_str(r_list.note, chr(13) , " ")
            r_list.note = replace_str(r_list.note, ",", " ")


            r_list.country = replace_str(r_list.country, ",", " ")
            r_list.country = replace_str(r_list.country, chr(10) , " ")
            r_list.country = replace_str(r_list.country, chr(13) , " ")
            r_list.nationality = replace_str(r_list.nationality, ",", " ")
            r_list.nationality = replace_str(r_list.nationality, chr(10) , " ")
            r_list.nationality = replace_str(r_list.nationality, chr(13) , " ")


    ghs_p1_checkout()
    ghs_x1_forecast()
    ghs_r1_checkin()

    return generate_output()