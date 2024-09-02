from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Segment, Genstat

def prepare_rm_stat2bl(gastno:int, segmcode:int, jan_date:date, to_date:date):
    avail_guest = False
    f_tittle = ""
    t_list_list = []
    guest = segment = genstat = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"gastnr":int, "mgastnr":int, "gname":str, "resnr":int, "reslinnr":int, "fdate":date, "tdate":date, "ankunft":date, "abreise":date, "zimmeranz":int, "dlodge":decimal, "dnite":int, "drate":decimal, "mlodge":decimal, "mnite":int, "mrate":decimal, "ylodge":decimal, "ynite":int, "yrate":decimal}, {"fdate": get_current_date(), "tdate": 01/01/1900, "ankunft": None, "abreise": None})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_guest, f_tittle, t_list_list, guest, segment, genstat


        nonlocal t_list
        nonlocal t_list_list
        return {"avail_guest": avail_guest, "f_tittle": f_tittle, "t-list": t_list_list}

    def create_list():

        nonlocal avail_guest, f_tittle, t_list_list, guest, segment, genstat


        nonlocal t_list
        nonlocal t_list_list

        for genstat in db_session.query(Genstat).filter(
                (Genstat.gastnr == gastno) &  (Genstat.datum >= jan_date) &  (Genstat.datum <= to_date) &  (Genstat.segmentcode == segmcode) &  (Genstat.res_logic[1]) &  ((Genstat.erwachs + Genstat.kind1) > 0)).all():

            t_list = query(t_list_list, filters=(lambda t_list :t_list.resnr == genstat.resnr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.resnr = genstat.resnr
                t_list.reslinnr = genstat.res_int[0]
                t_list.mgastnr = genstat.gastnrmember
                t_list.gastnr = genstat.gastnr

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

            if t_list.ankunft == None or t_list.ankunft > genstat.res_date[0]:
                t_list.ankunft = genstat.res_date[0]

            if t_list.abreise == None or t_list.abreise < genstat.res_date[1]:
                t_list.abreise = genstat.res_date[1]

            if t_list.fdate > genstat.datum:
                t_list.fdate = genstat.datum

            if t_list.tdate < genstat.datum:
                t_list.tdate = genstat.datum

            if genstat.datum == to_date:
                t_list.dlodge = t_list.dlodge + genstat.logis

                if genstat.resstatus != 13:
                    t_list.dnite = t_list.dnite + 1

            if get_month(genstat.datum) == get_month(to_date):
                t_list.mlodge = t_list.mlodge + genstat.logis

                if genstat.resstatus != 13:
                    t_list.mnite = t_list.mnite + 1


            t_list.ylodge = t_list.ylodge + genstat.logis

            if genstat.resstatus != 13:
                t_list.ynite = t_list.ynite + 1

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate = t_list.dlodge / t_list.dnite

            if t_list.mnite != 0:
                t_list.mrate = t_list.mlodge / t_list.mnite

            if t_list.ynite != 0:
                t_list.yrate = t_list.ylodge / t_list.ynite

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()

    if not guest:

        return generate_output()
    else:
        avail_guest = True

    segment = db_session.query(Segment).filter(
            (Segment.segmentcode == segmcode)).first()
    f_tittle = ": " + entry(0, segment.bezeich, "$$0") + " - " + guest.name
    create_list()

    return generate_output()