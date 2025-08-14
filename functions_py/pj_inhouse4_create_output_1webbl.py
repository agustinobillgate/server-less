#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 21/7/25
# quesy: 280, number: 262 (idflag) 
# inhouse_guest_list.inhousedate = date_mdy(entry(35, queasy.char2, "|"))
# idFlag = 262, tidak ada date di number2=262
# pasang try-catch
#-----------------------------------------


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Paramtext

inhouse_guest_list_data, Inhouse_guest_list = create_model("Inhouse_guest_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})

def pj_inhouse4_create_output_1webbl(idflag:string, inhouse_guest_list_data:[Inhouse_guest_list]):

    prepare_cache ([Paramtext])

    doneflag = False
    summary_roomtype_data = []
    summary_nation_data = []
    summary_revenue_data = []
    summary_segment_data = []
    tot_list_data = []
    counter:int = 0
    htl_no:string = ""
    temp_char:string = ""
    queasy = paramtext = None

    inhouse_guest_list = summary_roomtype = summary_nation = summary_revenue = summary_segment = sum_list = tot_list = bqueasy = pqueasy = tqueasy = None

    summary_roomtype_data, Summary_roomtype = create_model("Summary_roomtype", {"rmcat":string, "bezeich":string, "anz":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_nation_data, Summary_nation = create_model("Summary_nation", {"nat":string, "adult":string, "proz":string, "child":string})
    summary_revenue_data, Summary_revenue = create_model("Summary_revenue", {"currency":string, "room_rate":Decimal, "lodging":Decimal, "b_amount":Decimal, "l_amount":Decimal, "d_amount":Decimal, "o_amount":Decimal})
    summary_segment_data, Summary_segment = create_model("Summary_segment", {"segmcode":int, "segment":string, "anzahl":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    sum_list_data, Sum_list = create_model("Sum_list", {"curr":string, "zipreis":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "other":Decimal})
    tot_list_data, Tot_list = create_model("Tot_list", {"tot_payrm":string, "tot_rm":string, "tot_a":string, "tot_c":string, "tot_co":string, "tot_avail":string, "inactive":string, "tot_keycard":string})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, summary_roomtype_data, summary_nation_data, summary_revenue_data, summary_segment_data, tot_list_data, counter, htl_no, temp_char, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal inhouse_guest_list, summary_roomtype, summary_nation, summary_revenue, summary_segment, sum_list, tot_list, bqueasy, pqueasy, tqueasy
        nonlocal summary_roomtype_data, summary_nation_data, summary_revenue_data, summary_segment_data, sum_list_data, tot_list_data

        return {"doneflag": doneflag, "summary-roomtype": summary_roomtype_data, "summary-nation": summary_nation_data, "summary-revenue": summary_revenue_data, "summary-segment": summary_segment_data, "tot-list": tot_list_data, "inhouse-guest-list": inhouse_guest_list_data}

    def decode_string(in_str:string):

        nonlocal doneflag, summary_roomtype_data, summary_nation_data, summary_revenue_data, summary_segment_data, tot_list_data, counter, htl_no, temp_char, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal inhouse_guest_list, summary_roomtype, summary_nation, summary_revenue, summary_segment, sum_list, tot_list, bqueasy, pqueasy, tqueasy
        nonlocal summary_roomtype_data, summary_nation_data, summary_revenue_data, summary_segment_data, sum_list_data, tot_list_data

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

    # Rd 21/7/25
    #err ticket 439.
    # inhouse_guest_list.inhousedate = date_mdy(entry(35, queasy.char2, "|"))
    # idFlag = 262, tidak ada date di number2=262
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

        #err ticket 439.
        # inhouse_guest_list.inhousedate = date_mdy(entry(35, queasy.char2, "|"))
        try:
            inhouse_guest_list.inhousedate = date_mdy(entry(35, queasy.char2, "|"))
        except:
            pass
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
        # Rd 14/8/2025
        if bqueasy:
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

    if doneflag:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == ("Inhouse List Sum").lower()) & (Queasy.number2 == to_int(idflag)) & (Queasy.char3 == ("roomtype").lower())).order_by(Queasy.number1).all():
            summary_roomtype = Summary_roomtype()
            summary_roomtype_data.append(summary_roomtype)

            summary_roomtype.rmcat = entry(0, queasy.char2, "|")
            summary_roomtype.bezeich = entry(1, queasy.char2, "|")
            summary_roomtype.anz = to_int(entry(2, queasy.char2, "|"))
            summary_roomtype.proz_qty =  to_decimal(to_decimal(entry(3 , queasy.char2 , "|")) )
            summary_roomtype.rev =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
            summary_roomtype.proz_rev =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )
            summary_roomtype.arr =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == ("Inhouse List Sum").lower()) & (Queasy.number2 == to_int(idflag)) & (Queasy.char3 == ("nation").lower())).order_by(Queasy.number1).all():
            summary_nation = Summary_nation()
            summary_nation_data.append(summary_nation)

            summary_nation.nat = entry(0, queasy.char2, "|")
            summary_nation.adult = entry(1, queasy.char2, "|")
            summary_nation.proz = entry(2, queasy.char2, "|")
            summary_nation.child = entry(3, queasy.char2, "|")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == ("Inhouse List Sum").lower()) & (Queasy.number2 == to_int(idflag)) & (Queasy.char3 == ("revenue").lower())).order_by(Queasy.number1).all():
            summary_revenue = Summary_revenue()
            summary_revenue_data.append(summary_revenue)

            summary_revenue.currency = entry(0, queasy.char2, "|")
            summary_revenue.room_rate =  to_decimal(to_decimal(entry(1 , queasy.char2 , "|")) )
            summary_revenue.lodging =  to_decimal(to_decimal(entry(2 , queasy.char2 , "|")) )
            summary_revenue.b_amount =  to_decimal(to_decimal(entry(3 , queasy.char2 , "|")) )
            summary_revenue.l_amount =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
            summary_revenue.d_amount =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )
            summary_revenue.o_amount =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == ("Inhouse List Sum").lower()) & (Queasy.number2 == to_int(idflag)) & (Queasy.char3 == ("segment").lower())).order_by(Queasy.number1).all():
            summary_segment = Summary_segment()
            summary_segment_data.append(summary_segment)

            summary_segment.segmcode = to_int(entry(0, queasy.char2, "|"))
            summary_segment.segment = entry(1, queasy.char2, "|")
            summary_segment.anzahl = to_int(entry(2, queasy.char2, "|"))
            summary_segment.proz_qty =  to_decimal(to_decimal(entry(3 , queasy.char2 , "|")) )
            summary_segment.rev =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
            summary_segment.proz_rev =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )
            summary_segment.arr =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 280) & (Queasy.char1 == ("Inhouse List Sum").lower()) & (Queasy.number2 == to_int(idflag)) & (Queasy.char3 == ("summary").lower())).order_by(Queasy.number1).all():
            sum_list = Sum_list()
            sum_list_data.append(sum_list)

            sum_list.curr = entry(0, queasy.char2, "|")
            sum_list.zipreis =  to_decimal(to_decimal(entry(1 , queasy.char2 , "|")) )
            sum_list.lodging =  to_decimal(to_decimal(entry(2 , queasy.char2 , "|")) )
            sum_list.bfast =  to_decimal(to_decimal(entry(3 , queasy.char2 , "|")) )
            sum_list.lunch =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
            sum_list.dinner =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )
            sum_list.other =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )

        pqueasy = db_session.query(Pqueasy).filter(
                 (Pqueasy.key == 280) & (Pqueasy.char1 == ("Inhouse List Sum").lower()) & (Pqueasy.number2 == to_int(idflag))).first()

        if pqueasy:
            pass
        else:

            tqueasy = db_session.query(Tqueasy).filter(
                     (Tqueasy.key == 285) & (Tqueasy.char1 == ("Inhouse List Sum").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.number2 == to_int(idflag))).first()

            if tqueasy:
                pass
            else:
                pass

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Inhouse List Sum").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.number2 == to_int(idflag))).first()

        if tqueasy:
            pass
            db_session.delete(tqueasy)
            pass
        doneflag = True

    return generate_output()