#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_queasybl import read_queasybl
from models import Queasy, Guest, Res_line

def foreign_listbl(fdate:date, ci_date:date, all_nat:bool, sorttype:int, def_nat:string):

    prepare_cache ([Guest, Res_line])

    t_foreign_list_data = []
    queasy = guest = res_line = None

    t_foreign_list = t_queasy = None

    t_foreign_list_data, T_foreign_list = create_model("T_foreign_list", {"name":string, "nation1":string, "ausweis_nr1":string, "geburtdatum1":date, "zinr":string, "ankunft":date, "abreise":date, "adresse1":string, "wohnort":string, "land":string, "email_adr":string, "ankzeit":int, "abreisezeit":int, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "remark":string, "i_purpose":string, "gender":string, "telefon":string})
    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_foreign_list_data, queasy, guest, res_line
        nonlocal fdate, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy
        nonlocal t_foreign_list_data, t_queasy_data

        return {"t-foreign-list": t_foreign_list_data}

    def create_foreign_list():

        nonlocal t_foreign_list_data, queasy, guest, res_line
        nonlocal fdate, ci_date, all_nat, sorttype, def_nat


        nonlocal t_foreign_list, t_queasy
        nonlocal t_foreign_list_data, t_queasy_data

        i:int = 0
        str:string = ""
        purpose:int = 0
        t_foreign_list = T_foreign_list()
        t_foreign_list_data.append(t_foreign_list)

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
        t_foreign_list.erwachs = res_line.erwachs
        t_foreign_list.kind1 = res_line.kind1
        t_foreign_list.gratis = res_line.gratis
        t_foreign_list.remark = guest.bemerkung
        t_foreign_list.telefon = guest.telefon


        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                purpose = to_int(substring(str, 8))

            if purpose != 0:
                t_queasy_data = get_output(read_queasybl(1, 143, purpose, None))

                t_queasy = query(t_queasy_data, first=True)

                if t_queasy:
                    t_foreign_list.i_purpose = t_queasy.char3

    if fdate == ci_date:

        if not all_nat:

            if sorttype == 1:

                res_line_obj_list = {}
                res_line = Res_line()
                guest = Guest()
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)).order_by(Res_line.ankunft, Guest.nation1, Res_line.name, Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_foreign_list()

            elif sorttype == 2:

                res_line_obj_list = {}
                res_line = Res_line()
                guest = Guest()
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.nation1 != (def_nat).lower())).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft <= fdate) & (Res_line.abreise > fdate)).order_by(Res_line.ankunft, Guest.nation1, Res_line.name, Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_foreign_list()

            elif sorttype == 2:

                res_line_obj_list = {}
                res_line = Res_line()
                guest = Guest()
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
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
                for res_line.name, res_line.zinr, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.zimmer_wunsch, res_line._recid, guest.nation1, guest.ausweis_nr1, guest.geburtdatum1, guest.adresse1, guest.wohnort, guest.land, guest.email_adr, guest.bemerkung, guest.telefon, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.zimmer_wunsch, Res_line._recid, Guest.nation1, Guest.ausweis_nr1, Guest.geburtdatum1, Guest.adresse1, Guest.wohnort, Guest.land, Guest.email_adr, Guest.bemerkung, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.active_flag <= 2) & (Res_line.ankunft == fdate)).order_by(Guest.nation1, Res_line.name, Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_foreign_list()

    return generate_output()