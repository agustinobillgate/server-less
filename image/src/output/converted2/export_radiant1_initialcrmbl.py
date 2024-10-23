from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Res_line, Reservation, Genstat, Zimkateg, Segment, Guest, Nation, Sourccod, Waehrung, Interface

def export_radiant1_initialcrmbl(fdate:date, tdate:date):
    data_list_list = []
    loop_i:int = 0
    resv_date:date = None
    str_rsv:str = ""
    totalarr:int = 0
    curr:int = 0
    datum:date = None
    datum1:date = None
    new_status:str = ""
    p_87:date = None
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    flodging:decimal = to_decimal("0.0")
    lodging:decimal = to_decimal("0.0")
    breakfast:decimal = to_decimal("0.0")
    lunch:decimal = to_decimal("0.0")
    dinner:decimal = to_decimal("0.0")
    others:decimal = to_decimal("0.0")
    rmrate:decimal = to_decimal("0.0")
    net_vat:decimal = to_decimal("0.0")
    net_service:decimal = to_decimal("0.0")
    totrevincl:decimal = to_decimal("0.0")
    totrevexcl:decimal = to_decimal("0.0")
    calrate:decimal = to_decimal("0.0")
    htparam = res_line = reservation = genstat = zimkateg = segment = guest = nation = sourccod = waehrung = interface = None

    data_list = output_list = None

    data_list_list, Data_list = create_model("Data_list", {"resstatus":str, "bookchannel":str, "bookername":str, "resnr":int, "reslinnr":int, "totalprice":decimal, "bookdate":str, "ankunft":str, "abreise":str, "staydate":str, "countryname":str, "currencycode":str, "firstname":str, "lastname":str, "roomtypename":str, "roomtypecode":str, "ratecode":str, "argt":str, "countrycode":str, "segment":str, "nationalname":str, "nationalcode":str, "remark":str})
    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":str, "str1":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal data_list_list, loop_i, resv_date, str_rsv, totalarr, curr, datum, datum1, new_status, p_87, serv, vat, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, calrate, htparam, res_line, reservation, genstat, zimkateg, segment, guest, nation, sourccod, waehrung, interface
        nonlocal fdate, tdate


        nonlocal data_list, output_list
        nonlocal data_list_list, output_list_list
        return {"data-list": data_list_list}

    def process_data_old(from_old:date, to_old:date):

        nonlocal data_list_list, loop_i, resv_date, str_rsv, totalarr, curr, datum, datum1, new_status, p_87, serv, vat, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, calrate, htparam, res_line, reservation, genstat, zimkateg, segment, guest, nation, sourccod, waehrung, interface
        nonlocal fdate, tdate


        nonlocal data_list, output_list
        nonlocal data_list_list, output_list_list


        for datum in date_range(from_old,to_old) :

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= datum) & (Genstat.datum <= datum) & (Genstat.resstatus != 11) & (Genstat.resstatus != 12) & (Genstat.resstatus != 13) & (Genstat.resnr != 0)).order_by(Genstat._recid).all():

                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.zikatnr == genstat.zikatnr)).first()

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == genstat.resnr) & (Res_line.reslinnr == genstat.res_int[0)]).first()

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == genstat.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == genstat.segmentcode)).first()
                data_list = Data_list()
                data_list_list.append(data_list)

                data_list.resnr = genstat.resnr
                data_list.reslinnr = genstat.res_int[0]
                data_list.argt = res_line.arrangement

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == genstat.gastnr)).first()

                if guest:
                    data_list.bookername = guest.vorname1 + " " + guest.name
                    pass
                    data_list.bookername = replace_str(data_list.bookername, chr(10) , " ")
                    data_list.bookername = replace_str(data_list.bookername, chr(13) , " ")
                    data_list.bookername = replace_str(data_list.bookername, chr(59) , " ")

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == genstat.gastnrmember)).first()

                if guest:
                    data_list.lastname = guest.name
                    data_list.firstname = guest.vorname1
                    data_list.lastname = replace_str(data_list.lastname, chr(10) , " ")
                    data_list.lastname = replace_str(data_list.lastname, chr(13) , " ")
                    data_list.lastname = replace_str(data_list.lastname, chr(59) , " ")
                    data_list.firstname = replace_str(data_list.firstname, chr(10) , " ")
                    data_list.firstname = replace_str(data_list.firstname, chr(13) , " ")
                    data_list.firstname = replace_str(data_list.firstname, chr(59) , " ")

                    nation = db_session.query(Nation).filter(
                             (Nation.kurzbez == guest.land)).first()

                    if nation:
                        data_list.countryname = nation.bezeich
                        data_list.countrycode = nation.kurzbez

                    nation = db_session.query(Nation).filter(
                             (Nation.kurzbez == guest.nation1)).first()

                    if nation:
                        data_list.nationalname = nation.bezeich
                        data_list.nationalcode = nation.kurzbez


                    pass

                sourccod = db_session.query(Sourccod).filter(
                         (Sourccod.source_code == reservation.resart)).first()

                if sourccod:
                    data_list.bookchannel = sourccod.bezeich

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    calrate =  to_decimal("0")
                    data_list.currencycode = waehrung.wabkurz
                    calrate =  to_decimal(waehrung.ankauf)

                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.zikatnr == genstat.zikatnr)).first()

                if zimkateg:
                    data_list.roomtypename = zimkateg.bezeichnung
                    data_list.roomtypecode = zimkateg.kurzbez


                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str_rsv, 0, 6) == ("$CODE$").lower() :
                        data_list.ratecode = substring(str_rsv, 6)
                data_list.bookdate = to_string(get_year(reservation.resdat) , "9999") + "-" + to_string(get_month(reservation.resdat) , "99") + "-" + to_string(get_day(reservation.resdat) , "99")
                data_list.ankunft = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" + to_string(get_day(res_line.ankunft) , "99")
                data_list.abreise = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
                data_list.staydate = to_string(get_year(datum) , "9999") + "-" + to_string(get_month(datum) , "99") + "-" + to_string(get_day(datum) , "99")

                if res_line.resstatus <= 5:
                    data_list.resstatus = "new"
                    new_status = "new|init"

                if res_line.resstatus == 6 or res_line.resstatus == 8:
                    data_list.resstatus = "modified"
                    new_status = "modify|init"

                if res_line.resstatus == 9 or res_line.resstatus == 99 or res_line.resstatus == 10:
                    data_list.resstatus = "cancelled"
                    new_status = "cancel|init"

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == genstat.segmentcode)).first()

                if segment:
                    data_list.segment = segment.bemerk
                data_list.remark = reservation.bemerk


                data_list.remark = replace_str(data_list.remark, chr(10) , " ")
                data_list.remark = replace_str(data_list.remark, chr(13) , " ")
                data_list.remark = replace_str(data_list.remark, chr(59) , " ")
                data_list.totalprice =  to_decimal(genstat.logis)

                if data_list.totalprice < 0:
                    data_list.totalprice =  to_decimal("0")
                
                interface = Interface()
                db_session.add(interface)

                interface.key = 10
                interface.zinr = res_line.zinr
                interface.nebenstelle = ""
                interface.intfield = 0
                interface.decfield =  to_decimal("1")
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.parameters = new_status
                interface.resnr = res_line.resnr
                interface.reslinnr = res_line.reslinnr


                pass


    def process_data():

        nonlocal data_list_list, loop_i, resv_date, str_rsv, totalarr, curr, datum, datum1, new_status, p_87, serv, vat, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, calrate, htparam, res_line, reservation, genstat, zimkateg, segment, guest, nation, sourccod, waehrung, interface
        nonlocal fdate, tdate


        nonlocal data_list, output_list
        nonlocal data_list_list, output_list_list


        for datum1 in date_range(res_line.ankunft,res_line.abreise - 1) :
            data_list = Data_list()
            data_list_list.append(data_list)

            data_list.resnr = res_line.resnr
            data_list.reslinnr = res_line.reslinnr
            data_list.argt = res_line.arrangement

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnr)).first()

            if guest:
                data_list.bookername = guest.vorname1 + " " + guest.name
                pass

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:
                data_list.lastname = guest.name
                data_list.firstname = guest.vorname1

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.land)).first()

                if nation:
                    data_list.countryname = nation.bezeich
                    data_list.countrycode = nation.kurzbez

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation1)).first()

                if nation:
                    data_list.nationalname = nation.bezeich
                    data_list.nationalcode = nation.kurzbez


                pass

            sourccod = db_session.query(Sourccod).filter(
                     (Sourccod.source_code == reservation.resart)).first()

            if sourccod:
                data_list.bookchannel = sourccod.bezeich

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                calrate =  to_decimal("0")
                data_list.currencycode = waehrung.wabkurz
                calrate =  to_decimal(waehrung.ankauf)

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

            if zimkateg:
                data_list.roomtypename = zimkateg.bezeichnung
                data_list.roomtypecode = zimkateg.kurzbez


            for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                if substring(str_rsv, 0, 6) == ("$CODE$").lower() :
                    data_list.ratecode = substring(str_rsv, 6)
            data_list.bookdate = to_string(get_year(reservation.resdat) , "9999") + "-" + to_string(get_month(reservation.resdat) , "99") + "-" + to_string(get_day(reservation.resdat) , "99")
            data_list.ankunft = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" + to_string(get_day(res_line.ankunft) , "99")
            data_list.abreise = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
            data_list.staydate = to_string(get_year(datum1) , "9999") + "-" + to_string(get_month(datum1) , "99") + "-" + to_string(get_day(datum1) , "99")

            if res_line.resstatus <= 5:
                data_list.resstatus = "new"
                new_status = "new|init"

            if res_line.resstatus == 6 or res_line.resstatus == 8:
                data_list.resstatus = "modified"
                new_status = "modify|init"

            if res_line.resstatus == 9 or res_line.resstatus == 99 or res_line.resstatus == 10:
                data_list.resstatus = "cancelled"
                new_status = "cancel|init"

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == reservation.segmentcode)).first()

            if segment:
                data_list.segment = segment.bemerk
            data_list.remark = reservation.bemerk


            data_list.remark = replace_str(replace_str(data_list.remark, chr(10) , " ") , chr(13) , " ")
            lodging =  to_decimal("0")


            flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service = get_output(get_room_breakdown(res_line._recid, datum1, 1, datum1))
            data_list.totalprice = to_decimal(round(lodging / calrate , 2))


            
            interface = Interface()
            db_session.add(interface)

            interface.key = 10
            interface.zinr = res_line.zinr
            interface.nebenstelle = ""
            interface.intfield = 0
            interface.decfield =  to_decimal("1")
            interface.int_time = get_current_time_in_seconds()
            interface.intdate = get_current_date()
            interface.parameters = new_status
            interface.resnr = res_line.resnr
            interface.reslinnr = res_line.reslinnr


            pass


    data_list_list.clear()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    p_87 = htparam.fdate

    if fdate < p_87 and tdate < p_87:
        process_data_old(fdate, tdate)

    elif fdate < p_87 and tdate >= p_87:
        process_data_old(fdate, p_87 - 1)

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus != 11) & (Res_line.resstatus != 12) & (Res_line.resstatus != 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).first()
        while None != res_line:

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr) & (Reservation.resdat >= p_87) & (Reservation.resdat <= tdate)).first()
            while None != reservation:
                process_data()

                curr_recid = reservation._recid
                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr) & (Reservation.resdat >= p_87) & (Reservation.resdat <= tdate)).filter(Reservation._recid > curr_recid).first()

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus != 11) & (Res_line.resstatus != 12) & (Res_line.resstatus != 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).filter(Res_line._recid > curr_recid).first()
    else:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus != 11) & (Res_line.resstatus != 12) & (Res_line.resstatus != 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).first()
        while None != res_line:

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr) & (Reservation.resdat >= htparam.fdate) & (Reservation.resdat <= tdate)).first()
            while None != reservation:
                process_data()

                curr_recid = reservation._recid
                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr) & (Reservation.resdat >= htparam.fdate) & (Reservation.resdat <= tdate)).filter(Reservation._recid > curr_recid).first()

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus != 11) & (Res_line.resstatus != 12) & (Res_line.resstatus != 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).filter(Res_line._recid > curr_recid).first()

    return generate_output()