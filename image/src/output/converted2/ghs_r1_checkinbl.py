from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Guest, Res_line

def ghs_r1_checkinbl(datum:date, propid:str):
    r_list_list = []
    birthdate:str = ""
    htparam = guest = res_line = None

    r_list = gmember = gcomp = None

    r_list_list, R_list = create_model("R_list", {"email":str, "g_title":str, "firstname":str, "lastname":str, "cardname":str, "mobile":str, "phone":str, "postcode":str, "fax":str, "address1":str, "address2":str, "city":str, "state":str, "country":str, "nationality":str, "memberno":str, "propid":str, "profile":str, "confno":str, "note":str, "passport":str, "idcard":str, "birthdate":str, "gender":str, "comp":str, "compno":str})

    Gmember = create_buffer("Gmember",Guest)
    Gcomp = create_buffer("Gcomp",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_list, birthdate, htparam, guest, res_line
        nonlocal datum, propid
        nonlocal gmember, gcomp


        nonlocal r_list, gmember, gcomp
        nonlocal r_list_list
        return {"r-list": r_list_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()

    res_line_obj_list = []
    for res_line, gmember in db_session.query(Res_line, Gmember).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
             (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.ankunft == datum)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == datum) & (Res_line.abreise == datum)) | ((Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.ankunft == datum) & (datum < htparam.fdate))).order_by(Res_line._recid).all():
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

    return generate_output()