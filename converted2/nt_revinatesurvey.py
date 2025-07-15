from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Queasy, Nightaudit, Htparam, Paramtext, Waehrung, Reservation, Res_line, Nation, Zimkateg, Guest_pr, Nitehist

def nt_revinatesurvey():
    reihenfolge:int = 0
    outstr:str = ""
    progname:str = "nt-revinatesurvey.p"
    ci_date:date = None
    i_counter:int = 0
    propid:str = ""
    loop_i:int = 0
    str_rsv:str = ""
    contcode:str = ""
    country_name:str = ""
    roomtype:str = ""
    guest = queasy = nightaudit = htparam = paramtext = waehrung = reservation = res_line = nation = zimkateg = guest_pr = nitehist = None

    data_list = push_list = gmember = tqueasy = None

    data_list_list, Data_list = create_model("Data_list", {"guest_title":str, "first_name":str, "last_name":str, "email":str, "nation":str, "ci_date":str, "co_date":str, "rmno":str, "city":str, "propid":str, "concode":str, "rmrate":decimal, "ci_id":str, "co_id":str, "rsv_name":str, "rcode":str, "mobile":str, "country":str, "rsvstatus":str, "rmtype":str})
    push_list_list, Push_list = create_model("Push_list", {"becode":int, "rmtypevhp":str, "rmtypebe":str, "bename":str})

    Gmember = create_buffer("Gmember",Guest)
    Tqueasy = create_buffer("Tqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal reihenfolge, outstr, progname, ci_date, i_counter, propid, loop_i, str_rsv, contcode, country_name, roomtype, guest, queasy, nightaudit, htparam, paramtext, waehrung, reservation, res_line, nation, zimkateg, guest_pr, nitehist
        nonlocal gmember, tqueasy


        nonlocal data_list, push_list, gmember, tqueasy
        nonlocal data_list_list, push_list_list

        return {}

    def add_line(s:str, line_nr:int):

        nonlocal reihenfolge, outstr, progname, ci_date, i_counter, propid, loop_i, str_rsv, contcode, country_name, roomtype, guest, queasy, nightaudit, htparam, paramtext, waehrung, reservation, res_line, nation, zimkateg, guest_pr, nitehist
        nonlocal gmember, tqueasy


        nonlocal data_list, push_list, gmember, tqueasy
        nonlocal data_list_list, push_list_list

        nitehist = db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (Nitehist.reihenfolge == reihenfolge) & (Nitehist.line_nr == line_nr)).first()

        if not nitehist:
            nitehist = Nitehist()
            db_session.add(nitehist)

            nitehist.datum = ci_date
            nitehist.reihenfolge = reihenfolge
            nitehist.line_nr = line_nr
            nitehist.line = s


    def decode_string(in_str:str):

        nonlocal reihenfolge, outstr, progname, ci_date, i_counter, propid, loop_i, str_rsv, contcode, country_name, roomtype, guest, queasy, nightaudit, htparam, paramtext, waehrung, reservation, res_line, nation, zimkateg, guest_pr, nitehist
        nonlocal gmember, tqueasy


        nonlocal data_list, push_list, gmember, tqueasy
        nonlocal data_list_list, push_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def create_reviewpro_data(out_str:str):

        nonlocal reihenfolge, outstr, progname, ci_date, i_counter, propid, loop_i, str_rsv, contcode, country_name, roomtype, guest, queasy, nightaudit, htparam, paramtext, waehrung, reservation, res_line, nation, zimkateg, guest_pr, nitehist
        nonlocal gmember, tqueasy


        nonlocal data_list, push_list, gmember, tqueasy
        nonlocal data_list_list, push_list_list


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 288
        queasy.logi1 = False
        queasy.date1 = ci_date
        queasy.char1 = out_str

        push_list = query(push_list_list, filters=(lambda push_list: push_list.rmTypeVHP == data_list.rmType), first=True)

        if push_list:
            queasy.number1 = push_list.BECode

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate


    data_list_list.clear()

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        propid = decode_string(paramtext.ptexte)

    res_line_obj_list = []
    for res_line, waehrung, reservation, gmember, guest in db_session.query(Res_line, Waehrung, Reservation, Gmember, Guest).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
             (Res_line.abreise == ci_date) & (Res_line.resstatus == 8) & (Res_line.zipreis != 0)).order_by(Res_line.ankunft, Res_line.name, Res_line.zinr).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)

        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == gmember.land)).first()

        if nation:
            country_name = nation.bezeich
        else:
            country_name = gmember.land

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            roomtype = zimkateg.kurzbez
        data_list = Data_list()
        data_list_list.append(data_list)

        data_list.guest_title = gmember.anrede1
        data_list.first_name = gmember.vorname1
        data_list.last_name = gmember.name
        data_list.email = gmember.email_adr
        data_list.nation = gmember.nation1
        data_list.ci_date = to_string(get_month(res_line.ankunft) , "99") + "/" +\
                to_string(get_day(res_line.ankunft) , "99") + "/" +\
                to_string(get_year(res_line.ankunft) , "9999")
        data_list.co_date = to_string(get_month(res_line.abreise) , "99") + "/" +\
                to_string(get_day(res_line.abreise) , "99") + "/" +\
                to_string(get_year(res_line.abreise) , "9999")
        data_list.rmno = res_line.zinr
        data_list.city = gmember.wohnort
        data_list.propid = propid
        data_list.concode = to_string(res_line.resnr) + to_string(res_line.reslinnr, "999")
        data_list.rsv_name = guest.name + " " + guest.anredefirma
        data_list.ci_id = res_line.cancelled_id
        data_list.co_id = res_line.changed_id
        data_list.rmrate =  to_decimal(res_line.zipreis)
        data_list.mobile = gmember.mobil_telefon
        data_list.country = country_name
        contcode = ""
        data_list.rsvstatus = "CheckedOut"
        data_list.rmtype = roomtype


        for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

            if substring(str_rsv, 0, 6) == ("$CODE$").lower() :
                contcode = substring(str_rsv, 6)

        if contcode == "":

            guest_pr = db_session.query(Guest_pr).filter(
                     (Guest_pr.gastnr == res_line.gastnr)).first()

            if guest_pr:
                contcode = guest_pr.code
        data_list.rcode = contcode
        data_list.guest_title = replace_str(data_list.guest_title, chr(44) , chr(46))
        data_list.first_name = replace_str(data_list.first_name, chr(44) , chr(46))
        data_list.last_name = replace_str(data_list.last_name, chr(44) , chr(46))
        data_list.email = replace_str(data_list.email, chr(44) , chr(46))
        data_list.city = replace_str(data_list.city, chr(44) , chr(46))
        data_list.rsv_name = replace_str(data_list.rsv_name, chr(44) , chr(46))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 159) & (Queasy.char1 matches "*reviewpro*")).order_by(Queasy._recid).all():

        for tqueasy in db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 161) & (Tqueasy.number1 == queasy.number1)).order_by(Tqueasy._recid).all():
            push_list = Push_list()
            push_list_list.append(push_list)

            push_list.becode = tqueasy.number1
            push_list.rmtypevhp = entry(2, tqueasy.char1, ";")
            push_list.rmtypebe = entry(3, tqueasy.char1, ";")


    nitehist = Nitehist()
    db_session.add(nitehist)

    nitehist.datum = ci_date
    nitehist.reihenfolge = reihenfolge
    nitehist.line_nr = 0
    nitehist.line = "SEND|0"

    for data_list in query(data_list_list, sort_by=[("ci_date",False)]):
        i_counter = i_counter + 1
        outstr = to_string(data_list.guest_title) + "|" + to_string(data_list.first_name) + "|" + to_string(data_list.last_name) + "|" + to_string(data_list.city) + "|" + to_string(data_list.email) + "|" + to_string(data_list.nation) + "|" + to_string(data_list.ci_date) + "|" + to_string(data_list.co_date) + "|" + to_string(data_list.rmNo) + "|" + to_string(data_list.propid) + "|" + to_string(data_list.concode) + "|" + to_string(data_list.mobile) + "|" + to_string(data_list.rmrate) + "|" + to_string(data_list.rsv_name) + "|" + to_string(data_list.rcode) + "|" + to_string(data_list.country) + "|" + to_string(data_list.ci_id) + "|" + to_string(data_list.co_id) + "|" + to_string(data_list.rsvstatus) + "|" + to_string(data_list.rmtype)
        add_line(outstr, i_counter)
        create_reviewpro_data(outstr)

    return generate_output()