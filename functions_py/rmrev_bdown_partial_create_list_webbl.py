#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def rmrev_bdown_partial_create_list_webbl(id_flag:string):
    cl_list_data = []
    currency_list_data = []
    sum_list_data = []
    s_list_data = []
    argt_list_data = []
    done_flag = False
    tbl_name:string = ""
    counter:int = 0
    queasy = None

    sum_list = currency_list = cl_list = s_list = argt_list = bqueasy = pqueasy = tqueasy = None

    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "pax":int, "adult":int, "ch1":int, "ch2":int, "comch":int, "com":int, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal})
    currency_list_data, Currency_list = create_model("Currency_list", {"code":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"zipreis":Decimal, "localrate":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal, "c_zipreis":string, "c_localrate":string, "c_lodging":string, "c_bfast":string, "c_lunch":string, "c_dinner":string, "c_misc":string, "c_fixcost":string, "ct_rev":string, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":string, "zinr":string, "rstatus":int, "argt":string, "currency":string, "ratecode":string, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":string, "ex_rate":string, "fix_rate":string, "adult":int, "ch1":int, "ch2":int, "comch":int, "age1":int, "age2":string, "rmtype":string, "resnr":int, "resname":string, "segm_desc":string, "nation":string}, {"sleeping": True})
    s_list_data, S_list = create_model("S_list", {"artnr":int, "dept":int, "bezeich":string, "curr":string, "anzahl":int, "betrag":Decimal, "l_betrag":Decimal, "f_betrag":Decimal})
    argt_list_data, Argt_list = create_model("Argt_list", {"argtnr":int, "argtcode":string, "bezeich":string, "room":int, "pax":int, "qty":int, "bfast":Decimal})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, done_flag, tbl_name, counter, queasy
        nonlocal id_flag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, bqueasy, pqueasy, tqueasy
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data

        return {"cl-list": cl_list_data, "currency-list": currency_list_data, "sum-list": sum_list_data, "s-list": s_list_data, "argt-list": argt_list_data, "done_flag": done_flag}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == "RRB Period") & (Queasy.char2 == id_flag)).order_by(Queasy.number1).all():
        
        print("Q:", queasy.char3)
        tbl_name = entry(0, queasy.char3, "|")
        counter = counter + 1

        if counter > 500:
            break

        if tbl_name.lower()  == ("cl-list").lower() :
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.zipreis =  to_decimal(to_decimal(entry(1 , queasy.char3 , "|")) )
            cl_list.localrate =  to_decimal(to_decimal(entry(2 , queasy.char3 , "|")) )
            cl_list.lodging =  to_decimal(to_decimal(entry(3 , queasy.char3 , "|")) )
            cl_list.bfast =  to_decimal(to_decimal(entry(4 , queasy.char3 , "|")) )
            cl_list.lunch =  to_decimal(to_decimal(entry(5 , queasy.char3 , "|")) )
            cl_list.dinner =  to_decimal(to_decimal(entry(6 , queasy.char3 , "|")) )
            cl_list.misc =  to_decimal(to_decimal(entry(7 , queasy.char3 , "|")) )
            cl_list.fixcost =  to_decimal(to_decimal(entry(8 , queasy.char3 , "|")) )
            cl_list.t_rev =  to_decimal(to_decimal(entry(9 , queasy.char3 , "|")) )
            cl_list.c_zipreis = entry(10, queasy.char3, "|")
            cl_list.c_localrate = entry(11, queasy.char3, "|")
            cl_list.c_lodging = entry(12, queasy.char3, "|")
            cl_list.c_bfast = entry(13, queasy.char3, "|")
            cl_list.c_lunch = entry(14, queasy.char3, "|")
            cl_list.c_dinner = entry(15, queasy.char3, "|")
            cl_list.c_misc = entry(16, queasy.char3, "|")
            cl_list.c_fixcost = entry(17, queasy.char3, "|")
            cl_list.ct_rev = entry(18, queasy.char3, "|")
            cl_list.res_recid = to_int(entry(19, queasy.char3, "|"))
            cl_list.sleeping = entry(20, queasy.char3, "|") == "YES"
            cl_list.row_disp = to_int(entry(21, queasy.char3, "|"))
            cl_list.flag = entry(22, queasy.char3, "|")
            cl_list.zinr = entry(23, queasy.char3, "|")
            cl_list.rstatus = to_int(entry(24, queasy.char3, "|"))
            cl_list.argt = entry(25, queasy.char3, "|")
            cl_list.currency = entry(26, queasy.char3, "|")
            cl_list.ratecode = entry(27, queasy.char3, "|")
            cl_list.pax = to_int(entry(28, queasy.char3, "|"))
            cl_list.com = to_int(entry(29, queasy.char3, "|"))
            cl_list.ankunft = date_mdy(entry(30, queasy.char3, "|"))
            cl_list.abreise = date_mdy(entry(31, queasy.char3, "|"))
            cl_list.rechnr = to_int(entry(32, queasy.char3, "|"))
            cl_list.name = entry(33, queasy.char3, "|")
            cl_list.ex_rate = entry(34, queasy.char3, "|")
            cl_list.fix_rate = entry(35, queasy.char3, "|")
            cl_list.adult = to_int(entry(36, queasy.char3, "|"))
            cl_list.ch1 = to_int(entry(37, queasy.char3, "|"))
            cl_list.ch2 = to_int(entry(38, queasy.char3, "|"))
            cl_list.comch = to_int(entry(39, queasy.char3, "|"))
            cl_list.age1 = to_int(entry(40, queasy.char3, "|"))
            cl_list.age2 = entry(41, queasy.char3, "|")
            cl_list.rmtype = entry(42, queasy.char3, "|")
            cl_list.resnr = to_int(entry(43, queasy.char3, "|"))
            cl_list.resname = entry(44, queasy.char3, "|")
            cl_list.segm_desc = entry(45, queasy.char3, "|")
            cl_list.nation = entry(46, queasy.char3, "|")

        elif tbl_name.lower()  == ("sum-list").lower() :
            sum_list = Sum_list()
            sum_list_data.append(sum_list)

            sum_list.bezeich = entry(1, queasy.char3, "|")
            sum_list.pax = to_int(entry(2, queasy.char3, "|"))
            sum_list.adult = to_int(entry(3, queasy.char3, "|"))
            sum_list.ch1 = to_int(entry(4, queasy.char3, "|"))
            sum_list.ch2 = to_int(entry(5, queasy.char3, "|"))
            sum_list.comch = to_int(entry(6, queasy.char3, "|"))
            sum_list.com = to_int(entry(7, queasy.char3, "|"))
            sum_list.lodging =  to_decimal(to_decimal(entry(8 , queasy.char3 , "|")) )
            sum_list.bfast =  to_decimal(to_decimal(entry(9 , queasy.char3 , "|")) )
            sum_list.lunch =  to_decimal(to_decimal(entry(10 , queasy.char3 , "|")) )
            sum_list.dinner =  to_decimal(to_decimal(entry(11 , queasy.char3 , "|")) )
            sum_list.misc =  to_decimal(to_decimal(entry(12 , queasy.char3 , "|")) )
            sum_list.fixcost =  to_decimal(to_decimal(entry(13 , queasy.char3 , "|")) )
            sum_list.t_rev =  to_decimal(to_decimal(entry(14 , queasy.char3 , "|")) )

        elif tbl_name.lower()  == ("currency-list").lower() :
            currency_list = Currency_list()
            currency_list_data.append(currency_list)

            currency_list.code = entry(1, queasy.char3, "|")

        elif tbl_name.lower()  == ("s-list").lower() :
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.artnr = to_int(entry(1, queasy.char3, "|"))
            s_list.dept = to_int(entry(2, queasy.char3, "|"))
            s_list.bezeich = entry(3, queasy.char3, "|")
            s_list.curr = entry(4, queasy.char3, "|")
            s_list.anzahl = to_int(entry(5, queasy.char3, "|"))
            s_list.betrag =  to_decimal(to_decimal(entry(6 , queasy.char3 , "|")) )
            s_list.l_betrag =  to_decimal(to_decimal(entry(7 , queasy.char3 , "|")) )
            s_list.f_betrag =  to_decimal(to_decimal(entry(8 , queasy.char3 , "|")) )

        elif tbl_name.lower()  == ("argt-list").lower() :
            argt_list = Argt_list()
            argt_list_data.append(argt_list)

            argt_list.argtnr = to_int(entry(1, queasy.char3, "|"))
            argt_list.argtcode = entry(2, queasy.char3, "|")
            argt_list.bezeich = entry(3, queasy.char3, "|")
            argt_list.room = to_int(entry(4, queasy.char3, "|"))
            argt_list.pax = to_int(entry(5, queasy.char3, "|"))
            argt_list.qty = to_int(entry(6, queasy.char3, "|"))
            argt_list.bfast =  to_decimal(to_decimal(entry(7 , queasy.char3 , "|")) )

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("RRB Period").lower()) & (Pqueasy.char2 == (id_flag).lower())).first()

    if pqueasy:
        done_flag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("RRB Period").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == (id_flag).lower())).first()

        if tqueasy:
            done_flag = False


        else:
            done_flag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("RRB Period").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == (id_flag).lower())).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()