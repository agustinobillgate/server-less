#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Reservation, Guest, Zimkateg, Bediener, Res_history

def ci_cancelbl(pvilanguage:int, sortby:int, date1:date):

    prepare_cache ([Res_line, Reservation, Guest, Zimkateg, Bediener, Res_history])

    ci_list_list = []
    lvcarea:string = "arl-list"
    stat_list:List[string] = create_empty_list(14,"")
    res_line = reservation = guest = zimkateg = bediener = res_history = None

    ci_list = None

    ci_list_list, Ci_list = create_model("Ci_list", {"resno":int, "resname":string, "gname":string, "arrive":date, "depart":date, "rmno":string, "roomcat":string, "qty":int, "resstate":string, "usrid":string, "cancel":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_list_list, lvcarea, stat_list, res_line, reservation, guest, zimkateg, bediener, res_history
        nonlocal pvilanguage, sortby, date1


        nonlocal ci_list
        nonlocal ci_list_list

        return {"ci-list": ci_list_list}

    def cancel_ci():

        nonlocal ci_list_list, lvcarea, stat_list, res_line, reservation, guest, zimkateg, bediener, res_history
        nonlocal pvilanguage, sortby, date1


        nonlocal ci_list
        nonlocal ci_list_list

        if sortby == 1:

            res_history_obj_list = {}
            res_history = Res_history()
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            zimkateg = Zimkateg()
            bediener = Bediener()
            for res_history.datum, res_history._recid, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.zimmeranz, res_line.resstatus, res_line.l_zuordnung, res_line._recid, reservation.name, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest._recid, zimkateg.kurzbez, zimkateg._recid, bediener.userinit, bediener._recid in db_session.query(Res_history.datum, Res_history._recid, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.zimmeranz, Res_line.resstatus, Res_line.l_zuordnung, Res_line._recid, Reservation.name, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Bediener.userinit, Bediener._recid).join(Res_line,(Res_line.resnr == Res_history.resnr) & (Res_line.reslinnr == Res_history.reslinnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Bediener,(Bediener.nr == Res_history.nr)).filter(
                     (Res_history.datum == date1) & (Res_history.action == ("Cancel C/I").lower()) & (matches(Res_history.aenderung,("Cancel C/I Room*")))).order_by(Res_history._recid).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                ci_list = Ci_list()
                ci_list_list.append(ci_list)

                ci_list.resno = res_line.resnr
                ci_list.resname = reservation.name
                ci_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + " " + guest.anredefirma
                ci_list.arrive = res_line.ankunft
                ci_list.depart = res_line.abreise
                ci_list.rmno = res_line.zinr
                ci_list.roomcat = zimkateg.kurzbez
                ci_list.qty = res_line.zimmeranz
                ci_list.resstate = stat_list[res_line.resstatus + res_line.l_zuordnung[3 - 1]]
                ci_list.usrid = bediener.userinit
                ci_list.cancel = res_history.datum

        elif sortby == 2:

            res_history_obj_list = {}
            res_history = Res_history()
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            zimkateg = Zimkateg()
            bediener = Bediener()
            for res_history.datum, res_history._recid, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.zimmeranz, res_line.resstatus, res_line.l_zuordnung, res_line._recid, reservation.name, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest._recid, zimkateg.kurzbez, zimkateg._recid, bediener.userinit, bediener._recid in db_session.query(Res_history.datum, Res_history._recid, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.zimmeranz, Res_line.resstatus, Res_line.l_zuordnung, Res_line._recid, Reservation.name, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Bediener.userinit, Bediener._recid).join(Res_line,(Res_line.resnr == Res_history.resnr) & (Res_line.ankunft == date1) & (Res_line.reslinnr == Res_history.reslinnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Bediener,(Bediener.nr == Res_history.nr)).filter(
                     (Res_history.action == ("Cancel C/I").lower()) & (matches(Res_history.aenderung,("Cancel C/I Room*")))).order_by(Res_history._recid).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                ci_list = Ci_list()
                ci_list_list.append(ci_list)

                ci_list.resno = res_line.resnr
                ci_list.resname = reservation.name
                ci_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + " " + guest.anredefirma
                ci_list.arrive = res_line.ankunft
                ci_list.depart = res_line.abreise
                ci_list.rmno = res_line.zinr
                ci_list.roomcat = zimkateg.kurzbez
                ci_list.qty = res_line.zimmeranz
                ci_list.resstate = stat_list[res_line.resstatus + res_line.l_zuordnung[3 - 1]]
                ci_list.usrid = bediener.userinit
                ci_list.cancel = res_history.datum

        elif sortby == 3:

            res_history_obj_list = {}
            res_history = Res_history()
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            zimkateg = Zimkateg()
            bediener = Bediener()
            for res_history.datum, res_history._recid, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.zimmeranz, res_line.resstatus, res_line.l_zuordnung, res_line._recid, reservation.name, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest._recid, zimkateg.kurzbez, zimkateg._recid, bediener.userinit, bediener._recid in db_session.query(Res_history.datum, Res_history._recid, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.zimmeranz, Res_line.resstatus, Res_line.l_zuordnung, Res_line._recid, Reservation.name, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Bediener.userinit, Bediener._recid).join(Res_line,(Res_line.resnr == Res_history.resnr) & (Res_line.abreise == date1) & (Res_line.reslinnr == Res_history.reslinnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Bediener,(Bediener.nr == Res_history.nr)).filter(
                     (Res_history.action == ("Cancel C/I").lower()) & (matches(Res_history.aenderung,("Cancel C/I Room*")))).order_by(Res_history._recid).all():
                if res_history_obj_list.get(res_history._recid):
                    continue
                else:
                    res_history_obj_list[res_history._recid] = True


                ci_list = Ci_list()
                ci_list_list.append(ci_list)

                ci_list.resno = res_line.resnr
                ci_list.resname = reservation.name
                ci_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + " " + guest.anredefirma
                ci_list.arrive = res_line.ankunft
                ci_list.depart = res_line.abreise
                ci_list.rmno = res_line.zinr
                ci_list.roomcat = zimkateg.kurzbez
                ci_list.qty = res_line.zimmeranz
                ci_list.resstate = stat_list[res_line.resstatus + res_line.l_zuordnung[3 - 1]]
                ci_list.usrid = bediener.userinit
                ci_list.cancel = res_history.datum

    stat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    stat_list[1] = translateExtended ("6 PM", lvcarea, "")
    stat_list[2] = translateExtended ("Tentative", lvcarea, "")
    stat_list[3] = translateExtended ("WaitList", lvcarea, "")
    stat_list[4] = translateExtended ("OralConfirm", lvcarea, "")
    stat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    stat_list[6] = ""
    stat_list[7] = translateExtended ("Departed", lvcarea, "")
    stat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    stat_list[9] = translateExtended ("NoShow", lvcarea, "")
    stat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    stat_list[11] = translateExtended ("AccGuest", lvcarea, "")
    stat_list[12] = translateExtended ("RmSharer", lvcarea, "")
    stat_list[13] = translateExtended ("AccGuest", lvcarea, "")
    cancel_ci()

    return generate_output()