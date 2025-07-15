#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Paramtext

inhouse_guest_list_data, Inhouse_guest_list = create_model("Inhouse_guest_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})

def pj_inhouse4_create_output_webbl(idflag:string, inhouse_guest_list_data:[Inhouse_guest_list]):

    prepare_cache ([Paramtext])

    doneflag = False
    counter:int = 0
    htl_no:string = ""
    temp_char:string = ""
    queasy = paramtext = None

    inhouse_guest_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, htl_no, temp_char, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal inhouse_guest_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "inhouse-guest-list": inhouse_guest_list_data}

    def decode_string(in_str:string):

        nonlocal doneflag, counter, htl_no, temp_char, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal inhouse_guest_list, bqueasy, pqueasy, tqueasy

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("Inhouse List").lower()) & (Queasy.number2 == to_int(idflag))).order_by(Queasy.number1).yield_per(100):
        counter = counter + 1

        if counter > 1000:
            break
        inhouse_guest_list = Inhouse_guest_list()
        inhouse_guest_list_data.append(inhouse_guest_list)

        inhouse_guest_list.bezeich = entry(0, queasy.char3, "|")
        inhouse_guest_list.bemerk = entry(1, queasy.char3, "|")
        inhouse_guest_list.bemerk1 = entry(2, queasy.char3, "|")
        inhouse_guest_list.flag = to_int(entry(0, queasy.char2, "|"))
        inhouse_guest_list.karteityp = to_int(entry(1, queasy.char2, "|"))
        inhouse_guest_list.nr = to_int(entry(2, queasy.char2, "|"))
        inhouse_guest_list.vip = entry(3, queasy.char2, "|")
        inhouse_guest_list.resnr = to_int(entry(4, queasy.char2, "|"))
        inhouse_guest_list.firstname = entry(5, queasy.char2, "|")
        inhouse_guest_list.lastname = entry(6, queasy.char2, "|")
        inhouse_guest_list.birthdate = entry(7, queasy.char2, "|")
        inhouse_guest_list.groupname = entry(8, queasy.char2, "|")
        inhouse_guest_list.rmno = entry(9, queasy.char2, "|")
        inhouse_guest_list.qty = to_int(entry(10, queasy.char2, "|"))
        inhouse_guest_list.arrive = date_mdy(entry(11, queasy.char2, "|"))
        inhouse_guest_list.depart = date_mdy(entry(12, queasy.char2, "|"))
        inhouse_guest_list.rmcat = entry(13, queasy.char2, "|")
        inhouse_guest_list.ratecode = entry(14, queasy.char2, "|")
        inhouse_guest_list.zipreis =  to_decimal(to_decimal(entry(15 , queasy.char2 , "|")) )
        inhouse_guest_list.kurzbez = entry(16, queasy.char2, "|")
        inhouse_guest_list.a = to_int(entry(17, queasy.char2, "|"))
        inhouse_guest_list.c = to_int(entry(18, queasy.char2, "|"))
        inhouse_guest_list.co = to_int(entry(19, queasy.char2, "|"))
        inhouse_guest_list.pax = entry(20, queasy.char2, "|")
        inhouse_guest_list.nat = entry(21, queasy.char2, "|")
        inhouse_guest_list.nation = entry(22, queasy.char2, "|")
        inhouse_guest_list.argt = entry(23, queasy.char2, "|")
        inhouse_guest_list.company = entry(24, queasy.char2, "|")
        inhouse_guest_list.flight = entry(25, queasy.char2, "|")
        inhouse_guest_list.etd = entry(26, queasy.char2, "|")
        inhouse_guest_list.paym = to_int(entry(27, queasy.char2, "|"))
        inhouse_guest_list.segm = entry(28, queasy.char2, "|")
        inhouse_guest_list.telefon = entry(29, queasy.char2, "|")
        inhouse_guest_list.mobil_tel = entry(30, queasy.char2, "|")
        inhouse_guest_list.created = date_mdy(entry(31, queasy.char2, "|"))
        inhouse_guest_list.createid = entry(32, queasy.char2, "|")
        inhouse_guest_list.ci_time = entry(33, queasy.char2, "|")
        inhouse_guest_list.curr = entry(34, queasy.char2, "|")
        inhouse_guest_list.inhousedate = date_mdy(entry(35, queasy.char2, "|"))
        inhouse_guest_list.sob = entry(36, queasy.char2, "|")
        inhouse_guest_list.gastnr = to_int(entry(37, queasy.char2, "|"))
        inhouse_guest_list.lodging =  to_decimal(to_decimal(entry(38 , queasy.char2 , "|")) )
        inhouse_guest_list.breakfast =  to_decimal(to_decimal(entry(39 , queasy.char2 , "|")) )
        inhouse_guest_list.lunch =  to_decimal(to_decimal(entry(40 , queasy.char2 , "|")) )
        inhouse_guest_list.dinner =  to_decimal(to_decimal(entry(41 , queasy.char2 , "|")) )
        inhouse_guest_list.otherev =  to_decimal(to_decimal(entry(42 , queasy.char2 , "|")) )
        inhouse_guest_list.rechnr = to_int(entry(43, queasy.char2, "|"))
        inhouse_guest_list.memberno = entry(44, queasy.char2, "|")
        inhouse_guest_list.membertype = entry(45, queasy.char2, "|")
        inhouse_guest_list.email = entry(46, queasy.char2, "|")
        inhouse_guest_list.localreg = entry(47, queasy.char2, "|")
        inhouse_guest_list.c_zipreis = entry(48, queasy.char2, "|")
        inhouse_guest_list.c_lodging = entry(49, queasy.char2, "|")
        inhouse_guest_list.c_breakfast = entry(50, queasy.char2, "|")
        inhouse_guest_list.c_lunch = entry(51, queasy.char2, "|")
        inhouse_guest_list.c_dinner = entry(52, queasy.char2, "|")
        inhouse_guest_list.c_otherev = entry(53, queasy.char2, "|")
        inhouse_guest_list.c_a = entry(54, queasy.char2, "|")
        inhouse_guest_list.c_c = entry(55, queasy.char2, "|")
        inhouse_guest_list.c_co = entry(56, queasy.char2, "|")
        inhouse_guest_list.c_rechnr = entry(57, queasy.char2, "|")
        inhouse_guest_list.c_resnr = entry(58, queasy.char2, "|")
        inhouse_guest_list.night = entry(59, queasy.char2, "|")
        inhouse_guest_list.city = entry(60, queasy.char2, "|")
        inhouse_guest_list.keycard = entry(61, queasy.char2, "|")
        inhouse_guest_list.co_time = entry(62, queasy.char2, "|")
        inhouse_guest_list.pay_art = entry(63, queasy.char2, "|")
        inhouse_guest_list.etage = to_int(entry(64, queasy.char2, "|"))
        inhouse_guest_list.zinr_bez = entry(65, queasy.char2, "|")
        inhouse_guest_list.flag_guest = to_int(entry(66, queasy.char2, "|"))

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Inhouse List").lower()) & (Pqueasy.number2 == to_int(idflag))).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Inhouse List").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.number2 == to_int(idflag))).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Inhouse List").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.number2 == to_int(idflag))).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()