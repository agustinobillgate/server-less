from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Sourccod, Guest, Genstat

def rm_prodsourcebl(source_name:str, ytd_flag:bool, incl_comp:bool, fr_date:date, to_date:date):
    flag = 0
    output_list_list = []
    tot_dlodge:decimal = 0
    tot_mlodge:decimal = 0
    tot_ylodge:decimal = 0
    tot_dnite:int = 0
    tot_mnite:int = 0
    tot_ynite:int = 0
    tot_drate:decimal = 0
    tot_mrate:decimal = 0
    tot_yrate:decimal = 0
    tot1_dlodge:decimal = 0
    tot1_mlodge:decimal = 0
    tot1_ylodge:decimal = 0
    tot1_dnite:int = 0
    tot1_mnite:int = 0
    tot1_ynite:int = 0
    tot1_drate:decimal = 0
    tot1_mrate:decimal = 0
    tot1_yrate:decimal = 0
    sourccod = guest = genstat = None

    output_list = t_list = gbuff = None

    output_list_list, Output_list = create_model("Output_list", {"gname":str, "flag":bool, "name":str, "dlodge":decimal, "mlodge":decimal, "ylodge":decimal, "dnite":int, "mnite":int, "ynite":int, "drate":decimal, "mrate":decimal, "yrate":decimal})
    t_list_list, T_list = create_model("T_list", {"natnr":int, "nat":str, "counts":int, "tot_nat":int, "flag":bool, "gastnr":int, "name":str, "gname":str, "dlodge":decimal, "mlodge":decimal, "ylodge":decimal, "dnite":int, "mnite":int, "ynite":int, "drate":decimal, "mrate":decimal, "yrate":decimal})

    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal gbuff


        nonlocal output_list, t_list, gbuff
        nonlocal output_list_list, t_list_list
        return {"flag": flag, "output-list": output_list_list}

    def create_list1():

        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal gbuff


        nonlocal output_list, t_list, gbuff
        nonlocal output_list_list, t_list_list

        b:int = 0
        curr_nat:int = 0
        do_it:bool = True
        Gbuff = Guest

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= fr_date) &  (Genstat.datum <= to_date) &  (Genstat.SOURCE == sourccod.source_code) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.res_logic[1])).all():
            do_it = True

            if not incl_comp:

                if (genstat.erwachs + genstat.kind1) > 0:
                    do_it = True
                else:
                    do_it = False

            if do_it:

                t_list = query(t_list_list, filters=(lambda t_list :t_list.gastnr == genstat.gastnr and t_list.natnr == genstat.SOURCE), first=True)

                if not t_list:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == genstat.gastnr)).first()

                    if guest:

                        gbuff = db_session.query(Gbuff).filter(
                                (Gbuff.gastnr == genstat.gastnrmember)).first()

                        if gbuff:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            t_list.gastnr = genstat.gastnr
                            t_list.name = guest.name + ", " + guest.vorname1 + ", " +\
                                    guest.anrede1 + guest.anredefirma
                            t_list.gname = gbuff.name + ", " + gbuff.vorname1 + ", " +\
                                    gbuff.anrede1 + gbuff.anredefirma
                            t_list.nat = sourccod.bezeich
                            t_list.natnr = genstat.SOURCE

                if t_list:

                    if genstat.datum == to_date:
                        t_list.dlodge = t_list.dlodge + genstat.logis


                        t_list.dnite = t_list.dnite + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        t_list.mlodge = t_list.mlodge + genstat.logis


                        t_list.mnite = t_list.mnite + 1


                    t_list.ylodge = t_list.ylodge + genstat.logis


                    t_list.ynite = t_list.ynite + 1

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate = t_list.dlodge / t_list.dnite

            if t_list.mnite != 0:
                t_list.mrate = t_list.mlodge / t_list.mnite

            if t_list.ynite != 0:
                t_list.yrate = t_list.ylodge / t_list.ynite


        count_sub()
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "--------------------------------------------------------------"
        output_list.gNAME = "------------------------>"


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "Total"
        output_list.dlodge = tot_dlodge
        output_list.mlodge = tot_mlodge
        output_list.ylodge = tot_ylodge
        output_list.dnite = tot_dnite
        output_list.mnite = tot_mnite
        output_list.ynite = tot_ynite
        output_list.drate = tot_drate
        output_list.mrate = tot_mrate
        output_list.yrate = tot_yrate

    def create_list2():

        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal gbuff


        nonlocal output_list, t_list, gbuff
        nonlocal output_list_list, t_list_list

        b:int = 0
        curr_nat:int = 0
        do_it:bool = True
        Gbuff = Guest

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= fr_date) &  (Genstat.datum <= to_date) &  (Genstat.SOURCE == sourccod.source_code) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.res_logic[1])).all():
            do_it = True

            if not incl_comp:

                if (genstat.erwachs + genstat.kind1) > 0:
                    do_it = True
                else:
                    do_it = False

            if do_it:

                t_list = query(t_list_list, filters=(lambda t_list :t_list.gastnr == genstat.gastnr and t_list.natnr == genstat.SOURCE), first=True)

                if not t_list:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == genstat.gastnr)).first()

                    if guest:

                        gbuff = db_session.query(Gbuff).filter(
                                (Gbuff.gastnr == genstat.gastnrmember)).first()

                        if gbuff:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            t_list.gastnr = genstat.gastnr
                            t_list.name = guest.name + ", " + guest.vorname1 + ", " +\
                                    guest.anrede1 + guest.anredefirma
                            t_list.gname = gbuff.name + ", " + gbuff.vorname1 + ", " +\
                                    gbuff.anrede1 + gbuff.anredefirma
                            t_list.nat = sourccod.bezeich
                            t_list.natnr = genstat.SOURCE

                if t_list:

                    if genstat.datum == to_date:
                        t_list.dlodge = t_list.dlodge + genstat.logis


                        t_list.dnite = t_list.dnite + 1


                    t_list.mlodge = t_list.mlodge + genstat.logis


                    t_list.mnite = t_list.mnite + 1


                    t_list.ylodge = t_list.ylodge + genstat.logis


                    t_list.ynite = t_list.ynite + 1

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate = t_list.dlodge / t_list.dnite

            if t_list.mnite != 0:
                t_list.mrate = t_list.mlodge / t_list.mnite

            if t_list.ynite != 0:
                t_list.yrate = t_list.ylodge / t_list.ynite


        count_sub()
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "--------------------------------------------------------------"
        output_list.gNAME = "------------------------>"


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "Total"
        output_list.dlodge = tot_dlodge
        output_list.mlodge = tot_mlodge
        output_list.ylodge = tot_ylodge
        output_list.dnite = tot_dnite
        output_list.mnite = tot_mnite
        output_list.ynite = tot_ynite
        output_list.drate = tot_drate
        output_list.mrate = tot_mrate
        output_list.yrate = tot_yrate

    def count_sub():

        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal gbuff


        nonlocal output_list, t_list, gbuff
        nonlocal output_list_list, t_list_list

        curr_nat:int = 0

        for t_list in query(t_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.gname = t_list.gname
            output_list.name = t_list.name
            output_list.dlodge = t_list.dlodge
            output_list.mlodge = t_list.mlodge
            output_list.ylodge = t_list.ylodge
            output_list.dnite = t_list.dnite
            output_list.mnite = t_list.mnite
            output_list.ynite = t_list.ynite
            output_list.drate = t_list.drate
            output_list.mrate = t_list.mrate
            output_list.yrate = t_list.yrate


            tot_dlodge = tot_dlodge + t_list.dlodge
            tot_dnite = tot_dnite + t_list.dnite
            tot_mlodge = tot_mlodge + t_list.mlodge
            tot_ylodge = tot_ylodge + t_list.ylodge
            tot_mnite = tot_mnite + t_list.mnite
            tot_ynite = tot_ynite + t_list.ynite
            tot_drate = tot_drate + t_list.drate
            tot_mrate = tot_mrate + t_list.mrate
            tot_yrate = tot_yrate + t_list.yrate

        if tot_dnite != 0:
            tot_drate = tot_dlodge / tot_dnite

        if tot_mnite != 0:
            tot_mrate = tot_mlodge / tot_mnite

        if tot_ynite != 0:
            tot_yrate = tot_ylodge / tot_ynite


    sourccod = db_session.query(Sourccod).filter(
            (func.lower(Sourccod.bezeich) == (source_name).lower())).first()

    if not sourccod:

        sourccod = db_session.query(Sourccod).filter(
                (substring(Sourccod.bezeich, 0, len((source_name).lower() )) == (source_name).lower())).first()

    if not sourccod:
        flag = 1

        return generate_output()

    if ytd_flag:
        create_list1()
    else:
        create_list2()

    return generate_output()