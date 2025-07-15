#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Guest, Res_line

def ghs_r1_checkinbl(datum:date, propid:string):

    prepare_cache ([Htparam, Guest, Res_line])

    r_list_data = []
    birthdate:string = ""
    htparam = guest = res_line = None

    r_list = gmember = gcomp = None

    r_list_data, R_list = create_model("R_list", {"email":string, "g_title":string, "firstname":string, "lastname":string, "cardname":string, "mobile":string, "phone":string, "postcode":string, "fax":string, "address1":string, "address2":string, "city":string, "state":string, "country":string, "nationality":string, "memberno":string, "propid":string, "profile":string, "confno":string, "note":string, "passport":string, "idcard":string, "birthdate":string, "gender":string, "comp":string, "compno":string})

    Gmember = create_buffer("Gmember",Guest)
    Gcomp = create_buffer("Gcomp",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_list_data, birthdate, htparam, guest, res_line
        nonlocal datum, propid
        nonlocal gmember, gcomp


        nonlocal r_list, gmember, gcomp
        nonlocal r_list_data

        return {"r-list": r_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    res_line_obj_list = {}
    res_line = Res_line()
    gmember = Guest()
    for res_line.resnr, res_line.reslinnr, res_line._recid, gmember.email_adr, gmember.anrede1, gmember.vorname1, gmember.name, gmember.mobil_telefon, gmember.telefon, gmember.plz, gmember.fax, gmember.adresse1, gmember.adresse2, gmember.wohnort, gmember.geburt_ort2, gmember.land, gmember.nation1, gmember.gastnr, gmember.bemerkung, gmember.ausweis_nr1, gmember.geburtdatum1, gmember.master_gastnr, gmember.geburt_ort1, gmember.geschlecht, gmember._recid, gmember.anredefirma in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line._recid, Gmember.email_adr, Gmember.anrede1, Gmember.vorname1, Gmember.name, Gmember.mobil_telefon, Gmember.telefon, Gmember.plz, Gmember.fax, Gmember.adresse1, Gmember.adresse2, Gmember.wohnort, Gmember.geburt_ort2, Gmember.land, Gmember.nation1, Gmember.gastnr, Gmember.bemerkung, Gmember.ausweis_nr1, Gmember.geburtdatum1, Gmember.master_gastnr, Gmember.geburt_ort1, Gmember.geschlecht, Gmember._recid, Gmember.anredefirma).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
             (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.ankunft == datum)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == datum) & (Res_line.abreise == datum)) | ((Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.ankunft == datum) & (datum < htparam.fdate))).order_by(Res_line._recid).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True

        if gmember:
            r_list = R_list()
            r_list_data.append(r_list)

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

            gcomp = get_cache (Guest, {"gastnr": [(eq, gmember.master_gastnr)]})

            if gcomp:
                r_list.comp = gcomp.name + ", " + gcomp.anredefirma
                r_list.compno = gcomp.telefon

    return generate_output()