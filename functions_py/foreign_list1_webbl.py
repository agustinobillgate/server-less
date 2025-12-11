#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 8/9/2025
# beda data di range tanggal
# from functions import log_program_rd

#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_queasybl import read_queasybl
from models import Queasy, Guest, Res_line, Nation, Genstat, Zimmer, History

def foreign_list1_webbl(dtype:int, fdate:date, from_date:date, to_date:date, ci_date:date, all_nat:bool, sorttype:int, def_nat:string):

    prepare_cache ([Queasy, Guest, Res_line, Nation, Genstat, Zimmer])

    tot_pax_inhouse:int = 0
    tot_pax_depart:int = 0
    tot_pax_arrival:int = 0
    tot_pax_arrived:int = 0
    tot_pax_departed:int = 0
    tot_anz_inhouse:int = 0
    tot_anz_depart:int = 0
    tot_anz_arrival:int = 0
    tot_anz_arrived:int = 0
    tot_anz_departed:int = 0
    curr_status:int = 0
    curr_date:date = None
    tot_local:int = 0
    tot_foreign:int = 0
    t_foreign_list_data = []
    summary_list_data = []
    pax:int = 0
    queasy = guest = res_line = nation = genstat = zimmer = history = None

    t_foreign_list = t_queasy = summary_list = None

    t_foreign_list_data, T_foreign_list = create_model("T_foreign_list", {"resnr":int, "reslinnr":int, "name":string, "nation1":string, "ausweis_nr1":string, "geburtdatum1":date, "zinr":string, "ankunft":date, "abreise":date, "adresse1":string, "wohnort":string, "land":string, "email_adr":string, "ankzeit":int, "abreisezeit":int, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "remark":string, "i_purpose":string, "gender":string, "telefon":string, "guest_stat":int, "rm_qty":int})
    t_queasy_data, T_queasy = create_model_like(Queasy)
    summary_list_data, Summary_list = create_model("Summary_list", {"summ_str":string, "nation":string, "pax":int, "nation_remark":string, "pax_inhouse":int, "pax_depart":int, "pax_arrival":int, "pax_arrived":int, "pax_departed":int, "anz_inhouse":int, "anz_depart":int, "anz_arrival":int, "anz_arrived":int, "anz_departed":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, curr_date, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        return {"t-foreign-list": t_foreign_list_data, "summary-list": summary_list_data}

    def create_foreign_arrived_today():

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        curr_date:date = None
        for curr_date in date_range(from_date,to_date) :
            curr_status = 5

            if (curr_date > ci_date):
                create_arrival(curr_date)

            elif curr_date < ci_date:
                create_arrival1(curr_date)

            elif curr_date == ci_date:
                create_actual_arrived(curr_date)


    def create_foreign_departed_today(curr_date:date):

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr, Res_line.abreise).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_status = 6
                create_foreign_list()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr, Res_line.abreise).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_status = 6
                create_foreign_list()


    def create_actual_arrived(curr_date:date):

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.ankunft == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr, Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_foreign_list()

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz
                tot_pax_arrived = tot_pax_arrived + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.ankunft == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr, Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_foreign_list()

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz
                tot_pax_arrived = tot_pax_arrived + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz


    def create_foreign_departure(curr_date:date):

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        do_it:bool = False

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 11)) & (Res_line.abreise == curr_date)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_status = 2
                create_foreign_list()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 11)) & (Res_line.abreise == curr_date)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_status = 2
                create_foreign_list()


    def create_foreign_arrival():

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        curr_date:date = None
        for curr_date in date_range(from_date,to_date) :
            curr_status = 3

            if (curr_date > ci_date):
                create_arrival(curr_date)

            elif curr_date < ci_date:
                create_arrival1(curr_date)

            elif curr_date == ci_date:
                create_expected(curr_date)


    def create_inhouse():

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, curr_date, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        actflag1:int = 0
        actflag2:int = 0
        rm_sharer = None
        Rm_sharer =  create_buffer("Rm_sharer",Res_line)

        if from_date == ci_date and to_date == ci_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= from_date) & (Res_line.abreise >= to_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_status = 1
                create_foreign_list()
                t_foreign_list.rm_qty = res_line.zimmeranz
                t_foreign_list.erwachs = res_line.erwachs + res_line.gratis
                t_foreign_list.kind1 = res_line.kind1 + res_line.kind2
                t_foreign_list.gratis = res_line.gratis


                tot_pax_inhouse = tot_pax_inhouse + res_line.erwachs + res_line.gratis
                tot_anz_inhouse = tot_anz_inhouse + res_line.zimmeranz


        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= from_date) & (Res_line.abreise >= to_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_status = 1
                create_foreign_list()
                t_foreign_list.rm_qty = res_line.zimmeranz
                t_foreign_list.erwachs = res_line.erwachs + res_line.gratis
                t_foreign_list.kind1 = res_line.kind1 + res_line.kind2
                t_foreign_list.gratis = res_line.gratis


                tot_pax_inhouse = tot_pax_inhouse + res_line.erwachs + res_line.gratis
                tot_anz_inhouse = tot_anz_inhouse + res_line.zimmeranz


    def create_inhouse2():

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, curr_date, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat

        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        rm_sharer = None
        Rm_sharer =  create_buffer("Rm_sharer",Res_line)

        if not all_nat:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()

            for genstat.resstatus, genstat.resnr, genstat.res_int, genstat.erwachs, genstat.gratis, genstat.kind1, genstat.kind2, genstat.kind3, genstat.zinr, genstat.gastnr, genstat.zipreis, genstat.res_date, genstat._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid \
                in db_session.query(Genstat.resstatus, Genstat.resnr, Genstat.res_int, Genstat.erwachs, Genstat.gratis, Genstat.kind1, Genstat.kind2, \
                    Genstat.kind3, Genstat.zinr, Genstat.gastnr, Genstat.zipreis, Genstat.res_date, Genstat._recid, Guest.nation1, Guest.ausweis_nr1, \
                    Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid)\
                .join(Guest,(Guest.gastnr == Genstat.gastnrmember) & (Guest.nation1 != (def_nat).lower()))\
                .filter(
                     (Genstat.datum >= from_date) & 
                     (Genstat.datum <= to_date))\
                .order_by(Guest.nation1, Genstat.zinr).all():
                
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                # Rd, 8/9/2025, res_date None
                if not genstat.res_date[0]:
                    continue

                if genstat.res_date[0] < to_date and genstat.res_date[1] == to_date and genstat.resstatus == 8:
                    pass
                else:

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if res_line:
                        curr_status = 1
                        create_foreign_list()
                        t_foreign_list.rm_qty = 1
                        t_foreign_list.erwachs = genstat.erwachs + genstat.gratis
                        t_foreign_list.kind1 = genstat.kind1 + genstat.kind2 + genstat.kind3
                        t_foreign_list.gratis = genstat.gratis

                        if res_line.resstatus == 13 or res_line.zimmerfix:
                            t_foreign_list.rm_qty = 0

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

                if zimmer:

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_anz_inhouse = tot_anz_inhouse + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_anz_inhouse = tot_anz_inhouse + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_anz_inhouse = tot_anz_inhouse + 1


                tot_pax_inhouse = tot_pax_inhouse + genstat.erwachs + genstat.gratis


        else:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.resstatus, genstat.resnr, genstat.res_int, genstat.erwachs, genstat.gratis, genstat.kind1, genstat.kind2, genstat.kind3, genstat.zinr, genstat.gastnr, genstat.zipreis, genstat.res_date, genstat._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Genstat.resstatus, Genstat.resnr, Genstat.res_int, Genstat.erwachs, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.zinr, Genstat.gastnr, Genstat.zipreis, Genstat.res_date, Genstat._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date)).order_by(Guest.nation1, Genstat.zinr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                # Rd, 8/9/2025, res_date None
                if not genstat.res_date[0]:
                    continue

                if genstat.res_date[0] < to_date and genstat.res_date[1] == to_date and genstat.resstatus == 8:
                    pass
                else:

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if res_line:
                        curr_status = 1
                        create_foreign_list()
                        t_foreign_list.rm_qty = 1
                        t_foreign_list.erwachs = genstat.erwachs + genstat.gratis
                        t_foreign_list.kind1 = genstat.kind1 + genstat.kind2 + genstat.kind3
                        t_foreign_list.gratis = genstat.gratis

                        if res_line.resstatus == 13 or res_line.zimmerfix:
                            t_foreign_list.rm_qty = 0

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

                if zimmer:

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_anz_inhouse = tot_anz_inhouse + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_anz_inhouse = tot_anz_inhouse + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_anz_inhouse = tot_anz_inhouse + 1


                tot_pax_inhouse = tot_pax_inhouse + genstat.erwachs + genstat.gratis


    def create_arrival(curr_date:date):

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        rm_sharer = None
        Rm_sharer =  create_buffer("Rm_sharer",Res_line)

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 3) & (Res_line.ankunft == curr_date) & (Res_line.arrangement != "")).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                rm_sharer = db_session.query(Rm_sharer).filter(
                         (Rm_sharer.zinr == res_line.zinr) & (Rm_sharer.resnr == res_line.resnr) & (Rm_sharer.ankunft == res_line.ankunft) & (Rm_sharer.zipreis == 0) & (Rm_sharer.erwachs == 0) & ((Rm_sharer.resstatus == 11) | (Rm_sharer.resstatus == 13)) & (Rm_sharer.gratis < 1)).first()

                if not rm_sharer:
                    create_foreign_list()

                if res_line.resstatus != 11 and res_line.resstatus != 13:

                    if curr_status == 3:
                        tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz

                    elif curr_status == 5:
                        tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz

                if curr_status == 3:
                    tot_pax_arrival = tot_pax_arrival + ((res_line.erwachs + res_line.gratis) * res_line.zimmeranz)

                elif curr_status == 5:
                    tot_pax_arrived = tot_pax_arrived + ((res_line.erwachs + res_line.gratis) * res_line.zimmeranz)
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 3) & (Res_line.ankunft == curr_date) & (Res_line.arrangement != "")).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                rm_sharer = db_session.query(Rm_sharer).filter(
                         (Rm_sharer.zinr == res_line.zinr) & (Rm_sharer.resnr == res_line.resnr) & (Rm_sharer.ankunft == res_line.ankunft) & (Rm_sharer.zipreis == 0) & (Rm_sharer.erwachs == 0) & ((Rm_sharer.resstatus == 11) | (Rm_sharer.resstatus == 13)) & (Rm_sharer.gratis < 1)).first()

                if not rm_sharer:
                    create_foreign_list()

                if res_line.resstatus != 11 and res_line.resstatus != 13:

                    if curr_status == 3:
                        tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz

                    elif curr_status == 5:
                        tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz

                if curr_status == 3:
                    tot_pax_arrival = tot_pax_arrival + ((res_line.erwachs + res_line.gratis) * res_line.zimmeranz)

                elif curr_status == 5:
                    tot_pax_arrived = tot_pax_arrived + ((res_line.erwachs + res_line.gratis) * res_line.zimmeranz)


    def create_arrival1(curr_date:date):

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        do_it:bool = False
        rm_sharer = None
        Rm_sharer =  create_buffer("Rm_sharer",Res_line)

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 13)) & (Res_line.ankunft == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False

                if do_it:

                    rm_sharer = db_session.query(Rm_sharer).filter(
                             (Rm_sharer.zinr == res_line.zinr) & (Rm_sharer.resnr == res_line.resnr) & (Rm_sharer.ankunft == res_line.ankunft) & (Rm_sharer.zipreis == 0) & (Rm_sharer.erwachs == 0) & ((Rm_sharer.resstatus == 8) | (Rm_sharer.resstatus == 11) | (Rm_sharer.resstatus == 13)) & (Rm_sharer.gratis < 1)).first()

                    if not rm_sharer:
                        create_foreign_list()

                    if curr_status == 3:
                        tot_pax_arrival = tot_pax_arrival + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz

                        if res_line.resstatus == 6:
                            tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz

                        elif res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0:
                            tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz

                    elif curr_status == 5:
                        tot_pax_arrived = tot_pax_arrived + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz

                        if res_line.resstatus == 6:
                            tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz

                        elif res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0:
                            tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 13)) & (Res_line.ankunft == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False

                if do_it:

                    rm_sharer = db_session.query(Rm_sharer).filter(
                             (Rm_sharer.zinr == res_line.zinr) & (Rm_sharer.resnr == res_line.resnr) & (Rm_sharer.ankunft == res_line.ankunft) & (Rm_sharer.zipreis == 0) & (Rm_sharer.erwachs == 0) & ((Rm_sharer.resstatus == 8) | (Rm_sharer.resstatus == 11) | (Rm_sharer.resstatus == 13)) & (Rm_sharer.gratis < 1)).first()

                    if not rm_sharer:
                        create_foreign_list()

                    if curr_status == 3:
                        tot_pax_arrival = tot_pax_arrival + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz

                        if res_line.resstatus == 6:
                            tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz

                        elif res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0:
                            tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz

                    elif curr_status == 5:
                        tot_pax_arrived = tot_pax_arrived + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz

                        if res_line.resstatus == 6:
                            tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz

                        elif res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0:
                            tot_anz_arrived = tot_anz_arrived + res_line.zimmeranz


    def create_expected(curr_date:date):

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        rm_sharer = None
        Rm_sharer =  create_buffer("Rm_sharer",Res_line)

        if not all_nat:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                     (Res_line.active_flag == 0) & (Res_line.resstatus != 3) & (Res_line.ankunft == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                rm_sharer = db_session.query(Rm_sharer).filter(
                         (Rm_sharer.zinr == res_line.zinr) & (Rm_sharer.resnr == res_line.resnr) & (Rm_sharer.ankunft == res_line.ankunft) & (Rm_sharer.zipreis == 0) & (Rm_sharer.erwachs == 0) & ((Rm_sharer.resstatus == 8) | (Rm_sharer.resstatus == 11) | (Rm_sharer.resstatus == 13)) & (Rm_sharer.gratis < 1)).first()

                if not rm_sharer:
                    create_foreign_list()

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz
                tot_pax_arrival = tot_pax_arrival + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            guest = Guest()
            for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag == 0) & (Res_line.resstatus != 3) & (Res_line.ankunft == curr_date)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                rm_sharer = db_session.query(Rm_sharer).filter(
                         (Rm_sharer.zinr == res_line.zinr) & (Rm_sharer.resnr == res_line.resnr) & (Rm_sharer.ankunft == res_line.ankunft) & (Rm_sharer.zipreis == 0) & (Rm_sharer.erwachs == 0) & ((Rm_sharer.resstatus == 8) | (Rm_sharer.resstatus == 11) | (Rm_sharer.resstatus == 13)) & (Rm_sharer.gratis < 1)).first()

                if not rm_sharer:
                    create_foreign_list()

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    tot_anz_arrival = tot_anz_arrival + res_line.zimmeranz
                tot_pax_arrival = tot_pax_arrival + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz


    def create_foreign_list():

        nonlocal tot_pax_inhouse, tot_pax_depart, tot_pax_arrival, tot_pax_arrived, tot_pax_departed, tot_anz_inhouse, tot_anz_depart, tot_anz_arrival, tot_anz_arrived, tot_anz_departed, curr_status, curr_date, tot_local, tot_foreign, t_foreign_list_data, summary_list_data, pax, queasy, guest, res_line, nation, genstat, zimmer, history
        nonlocal dtype, fdate, from_date, to_date, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy, summary_list
        nonlocal t_foreign_list_data, t_queasy_data, summary_list_data

        i:int = 0
        str:string = ""
        purpose:int = 0
        t_foreign_list = T_foreign_list()
        t_foreign_list_data.append(t_foreign_list)

        t_foreign_list.resnr = res_line.resnr
        t_foreign_list.reslinnr = res_line.reslinnr
        t_foreign_list.name = res_line.name
        t_foreign_list.nation1 = guest.nation1
        t_foreign_list.ausweis_nr1 = guest.ausweis_nr1
        t_foreign_list.geburtdatum1 = guest.geburtdatum1
        t_foreign_list.zinr = res_line.zinr
        t_foreign_list.ankunft = res_line.ankunft
        t_foreign_list.abreise = res_line.abreise
        t_foreign_list.adresse1 = guest.adresse1
        t_foreign_list.wohnort = guest.wohnort
        t_foreign_list.land = guest.land
        t_foreign_list.email_adr = guest.email_adr
        t_foreign_list.ankzeit = res_line.ankzeit
        t_foreign_list.abreisezeit = res_line.abreisezeit
        t_foreign_list.resstatus = res_line.resstatus
        t_foreign_list.remark = guest.bemerkung
        t_foreign_list.telefon = guest.telefon
        t_foreign_list.guest_stat = curr_status

        if curr_status != 1:
            t_foreign_list.rm_qty = res_line.zimmeranz
            t_foreign_list.erwachs = res_line.erwachs + res_line.gratis
            t_foreign_list.kind1 = res_line.kind1
            t_foreign_list.gratis = res_line.gratis


        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                purpose = to_int(substring(str, 8))

            if purpose != 0:
                t_queasy_data = get_output(read_queasybl(1, 143, purpose, None))

                t_queasy = query(t_queasy_data, first=True)

                if t_queasy:
                    t_foreign_list.i_purpose = t_queasy.char3


    if dtype == 0:

        if fdate == ci_date:

            if not all_nat:

                if sorttype == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1)).order_by(Res_line.ankunft, Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 2:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 3:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             ((Res_line.resstatus == 1) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 4:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)) | (((Res_line.resstatus == 1) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0) & (Res_line.ankunft == fdate))).order_by(Res_line._recid).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()
            else:

                if sorttype == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)).order_by(Res_line.ankunft, Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 2:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 3:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.resstatus == 1) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 4:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)) | (((Res_line.resstatus == 1) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0) & (Res_line.ankunft == fdate))).order_by(Res_line._recid).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()
        else:

            if not all_nat:

                if sorttype == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)).order_by(Res_line.ankunft, Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 2:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 3:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             ((Res_line.resstatus == 1) | (Res_line.resstatus == 11) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 4:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                             (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)) | (((Res_line.resstatus == 1) | (Res_line.resstatus == 11) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft == fdate))).order_by(Res_line._recid).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()
            else:

                if sorttype == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)).order_by(Res_line.ankunft, Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 2:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 3:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.resstatus == 1) | (Res_line.resstatus == 11) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

                elif sorttype == 4:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    guest = Guest()
                    for res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zimmerfix, res_line.zinr, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line.ankzeit, res_line.abreisezeit, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zimmerfix, Res_line.zinr, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line.ankzeit, Res_line.abreisezeit, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                             (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == fdate)) | (((Res_line.resstatus == 1) | (Res_line.resstatus == 11) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft == fdate))).order_by(Res_line._recid).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_foreign_list()

    elif dtype == 1:

        if sorttype == 1:

            if from_date >= ci_date:
                create_inhouse()
            else:
                create_inhouse2()

        elif sorttype == 2:
            for curr_date in date_range(from_date,to_date) :
                create_foreign_departure(curr_date)

        elif sorttype == 3:
            create_foreign_arrival()

        elif sorttype == 4:

            if from_date >= ci_date:
                create_inhouse()
            else:
                create_inhouse2()
            for curr_date in date_range(from_date,to_date) :
                create_foreign_departure(curr_date)
                create_foreign_departed_today(curr_date)

            create_foreign_arrival()
            create_foreign_arrived_today()

        elif sorttype == 5:
            create_foreign_arrived_today()

        elif sorttype == 6:
            for curr_date in date_range(from_date,to_date) :
                create_foreign_departed_today(curr_date)

    summary_list = Summary_list()
    summary_list_data.append(summary_list)

    summary_list.summ_str = "SUMMARY"

    for t_foreign_list in query(t_foreign_list_data, sort_by=[("nation1",False)]):

        if t_foreign_list.nation1 == None or t_foreign_list.nation1 == "":
            t_foreign_list.nation1 = "?"

        summary_list = query(summary_list_data, filters=(lambda summary_list: summary_list.nation == t_foreign_list.nation1), first=True)

        if not summary_list:
            summary_list = Summary_list()
            summary_list_data.append(summary_list)

            summary_list.nation = t_foreign_list.nation1

            nation = get_cache (Nation, {"kurzbez": [(eq, summary_list.nation)]})

            if nation:
                summary_list.nation_remark = nation.bezeich

            if summary_list.nation.lower()  == ("N/A").lower()  or summary_list.nation.lower()  == ("?").lower() :
                summary_list.nation_remark = "UNKNOWN"

        if t_foreign_list.guest_stat == 1:
            summary_list.anz_inhouse = summary_list.anz_inhouse + t_foreign_list.rm_qty
            summary_list.pax_inhouse = summary_list.pax_inhouse + t_foreign_list.erwachs

            if t_foreign_list.nation1.lower()  == (def_nat).lower() :
                tot_local = tot_local + t_foreign_list.erwachs
            else:
                tot_foreign = tot_foreign + t_foreign_list.erwachs

        elif t_foreign_list.guest_stat == 2:

            if t_foreign_list.resstatus == 6:
                summary_list.anz_depart = summary_list.anz_depart + t_foreign_list.rm_qty
                tot_anz_depart = tot_anz_depart + 1


            summary_list.pax_depart = summary_list.pax_depart + t_foreign_list.erwachs
            tot_pax_depart = tot_pax_depart + t_foreign_list.erwachs

            if t_foreign_list.nation1.lower()  == (def_nat).lower() :
                tot_local = tot_local + t_foreign_list.erwachs
            else:
                tot_foreign = tot_foreign + t_foreign_list.erwachs

        elif t_foreign_list.guest_stat == 3:
            summary_list.pax_arrival = summary_list.pax_arrival + t_foreign_list.erwachs * t_foreign_list.rm_qty

            if t_foreign_list.resstatus != 11 and t_foreign_list.resstatus != 13:
                summary_list.anz_arrival = summary_list.anz_arrival + t_foreign_list.rm_qty

            if t_foreign_list.nation1.lower()  == (def_nat).lower() :
                tot_local = tot_local + t_foreign_list.erwachs * t_foreign_list.rm_qty
            else:
                tot_foreign = tot_foreign + t_foreign_list.erwachs * t_foreign_list.rm_qty

        elif t_foreign_list.guest_stat == 5:
            summary_list.anz_arrived = summary_list.anz_arrived + t_foreign_list.rm_qty
            summary_list.pax_arrived = summary_list.pax_arrived + t_foreign_list.erwachs * t_foreign_list.rm_qty

            if t_foreign_list.nation1.lower()  == (def_nat).lower() :
                tot_local = tot_local + t_foreign_list.erwachs * t_foreign_list.rm_qty
            else:
                tot_foreign = tot_foreign + t_foreign_list.erwachs * t_foreign_list.rm_qty

        elif t_foreign_list.guest_stat == 6:

            if (t_foreign_list.erwachs + t_foreign_list.gratis) > 0:
                summary_list.anz_departed = summary_list.anz_departed + t_foreign_list.rm_qty
                tot_anz_departed = tot_anz_departed + t_foreign_list.rm_qty


            summary_list.pax_departed = summary_list.pax_departed + t_foreign_list.erwachs
            tot_pax_departed = tot_pax_departed + t_foreign_list.erwachs

            if t_foreign_list.nation1.lower()  == (def_nat).lower() :
                tot_local = tot_local + t_foreign_list.erwachs
            else:
                tot_foreign = tot_foreign + t_foreign_list.erwachs
    summary_list = Summary_list()
    summary_list_data.append(summary_list)

    summary_list.nation_remark = "TOTAL"
    summary_list.pax_inhouse = tot_pax_inhouse
    summary_list.pax_depart = tot_pax_depart
    summary_list.pax_arrival = tot_pax_arrival
    summary_list.pax_arrived = tot_pax_arrived
    summary_list.pax_departed = tot_pax_departed
    summary_list.anz_inhouse = tot_anz_inhouse
    summary_list.anz_depart = tot_anz_depart
    summary_list.anz_arrival = tot_anz_arrival
    summary_list.anz_arrived = tot_anz_arrived
    summary_list.anz_departed = tot_anz_departed


    summary_list = Summary_list()
    summary_list_data.append(summary_list)

    summary_list.nation_remark = "TOTAL LOCAL"
    summary_list.pax_inhouse = tot_local


    summary_list = Summary_list()
    summary_list_data.append(summary_list)

    summary_list.nation_remark = "TOTAL FOREIGN"
    summary_list.pax_inhouse = tot_foreign

    return generate_output()