#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Bk_func, Bk_rart, Bk_reser, Guest, Queasy

def rsv_list_create_list_webbl(from_date:date, to_date:date, inp_room:string, stat_screen_value:string, mi_created_chk:bool, mi_event_chk:bool, mi_engager_chk:bool, mi_room_chk:bool, mi_sales_chk:bool, mi_segment_chk:bool, mi_cutoff_chk:bool):

    prepare_cache ([Bk_veran, Bk_func, Bk_rart, Bk_reser, Guest])

    gastnr = 0
    output_list_data = []
    total_estrev:Decimal = to_decimal("0.0")
    total_paid:Decimal = to_decimal("0.0")
    troomrev:Decimal = to_decimal("0.0")
    tfbrev:Decimal = to_decimal("0.0")
    tothrev:Decimal = to_decimal("0.0")
    ttrev:Decimal = to_decimal("0.0")
    do_it:bool = False
    bk_veran = bk_func = bk_rart = bk_reser = guest = queasy = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"bk_stat":string, "bk_datum":date, "engager":string, "contact":string, "bk_event":string, "venue":string, "bk_time":string, "pax":int, "tablesetup":string, "room_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "total_rev":Decimal, "cm_id":string, "sales":string, "crdate":date, "cutoff":date, "segment":string, "sob":string, "resnr":int, "reslinnr":int, "remark":string, "resstatus":int, "datum":date, "gastnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastnr, output_list_data, total_estrev, total_paid, troomrev, tfbrev, tothrev, ttrev, do_it, bk_veran, bk_func, bk_rart, bk_reser, guest, queasy
        nonlocal from_date, to_date, inp_room, stat_screen_value, mi_created_chk, mi_event_chk, mi_engager_chk, mi_room_chk, mi_sales_chk, mi_segment_chk, mi_cutoff_chk


        nonlocal output_list
        nonlocal output_list_data

        return {"gastnr": gastnr, "output-list": output_list_data}

    def create_list():

        nonlocal gastnr, output_list_data, total_estrev, total_paid, troomrev, tfbrev, tothrev, ttrev, do_it, bk_veran, bk_func, bk_rart, bk_reser, guest, queasy
        nonlocal from_date, to_date, inp_room, stat_screen_value, mi_created_chk, mi_event_chk, mi_engager_chk, mi_room_chk, mi_sales_chk, mi_segment_chk, mi_cutoff_chk


        nonlocal output_list
        nonlocal output_list_data

        other_rev:Decimal = to_decimal("0.0")
        troomrev =  to_decimal("0")
        tfbrev =  to_decimal("0")
        tothrev =  to_decimal("0")
        ttrev =  to_decimal("0")


        output_list_data.clear()

        if stat_screen_value.lower()  == ("0").lower() :

            if mi_created_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func._recid).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_event_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.bis_datum).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_engager_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.bestellt__durch).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_room_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.raeume[inc_value(0)]).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_sales_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.vgeschrieben).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_segment_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_veran.segmentcode).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_cutoff_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_veran.segmentcode).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


        elif stat_screen_value.lower()  == ("1").lower()  or stat_screen_value.lower()  == ("2").lower()  or stat_screen_value.lower()  == ("3").lower() :

            if mi_created_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus == int (stat_screen_value))).order_by(Bk_func._recid).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_event_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus == int (stat_screen_value))).order_by(Bk_func.bis_datum).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_engager_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus == int (stat_screen_value))).order_by(Bk_func.bestellt__durch).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_room_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus == int (stat_screen_value))).order_by(Bk_func.raeume[inc_value(0)]).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_sales_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_func.vgeschrieben).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_segment_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_veran.segmentcode).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()


            elif mi_cutoff_chk :

                bk_func_obj_list = {}
                bk_func = Bk_func()
                bk_veran = Bk_veran()
                for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.bis_datum, bk_func.bestellt__durch, bk_func.v_kontaktperson, bk_func.zweck, bk_func.uhrzeit, bk_func.personen, bk_func.rpreis, bk_func.rpersonen, bk_func.c_resstatus, bk_func.resstatus, bk_func.datum, bk_func.technik, bk_func.tischform, bk_func._recid, bk_veran.kontaktfirst, bk_veran.bemerkung, bk_veran.gastnr, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.deposit, bk_veran.total_paid, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.bis_datum, Bk_func.bestellt__durch, Bk_func.v_kontaktperson, Bk_func.zweck, Bk_func.uhrzeit, Bk_func.personen, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.c_resstatus, Bk_func.resstatus, Bk_func.datum, Bk_func.technik, Bk_func.tischform, Bk_func._recid, Bk_veran.kontaktfirst, Bk_veran.bemerkung, Bk_veran.gastnr, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.deposit, Bk_veran.total_paid, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                         (Bk_func.bis_datum >= from_date) & (Bk_func.bis_datum <= to_date) & (Bk_func.resstatus <= 3)).order_by(Bk_veran.segmentcode).all():
                    if bk_func_obj_list.get(bk_func._recid):
                        continue
                    else:
                        bk_func_obj_list[bk_func._recid] = True

                    if bk_veran:

                        if (inp_room).lower()  != "" and bk_func.raeume[0] == (inp_room).lower() :
                            do_it = True

                        elif inp_room == "":
                            do_it = True
                        else:
                            do_it = False
                        other_rev =  to_decimal("0")

                        if do_it:

                            for bk_rart in db_session.query(Bk_rart).filter(
                                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(anzahl))
                            create_output_list()

    def create_output_list():

        nonlocal gastnr, output_list_data, total_estrev, total_paid, troomrev, tfbrev, tothrev, ttrev, do_it, bk_veran, bk_func, bk_rart, bk_reser, guest, queasy
        nonlocal from_date, to_date, inp_room, stat_screen_value, mi_created_chk, mi_event_chk, mi_engager_chk, mi_room_chk, mi_sales_chk, mi_segment_chk, mi_cutoff_chk


        nonlocal output_list
        nonlocal output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bk_datum = bk_func.bis_datum
        output_list.engager = bk_func.bestellt__durch
        output_list.contact = bk_func.v_kontaktperson[0]
        output_list.bk_event = bk_func.zweck[0]
        output_list.venue = bk_func.raeume[0]
        output_list.bk_time = bk_func.uhrzeit
        output_list.pax = bk_func.personen
        output_list.room_rev =  to_decimal(bk_func.rpreis[0])
        output_list.fb_rev =  to_decimal(bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])
        output_list.other_rev =  to_decimal(other_rev)
        output_list.total_rev =  to_decimal(bk_func.rpreis[0] + (bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(other_rev)
        output_list.bk_stat = bk_func.c_resstatus[0]
        output_list.resnr = bk_func.veran_nr
        output_list.reslinnr = bk_func.veran_seite
        output_list.resstatus = bk_func.resstatus
        output_list.datum = bk_func.datum
        output_list.sob = bk_func.technik[1]
        output_list.crdate = bk_veran.kontaktfirst
        output_list.tablesetup = bk_func.tischform[0]
        output_list.remark = bk_veran.bemerkung
        gastnr = bk_veran.gastnr
        output_list.gastnr = bk_veran.gastnr

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)]})

        if bk_reser:
            output_list.cutoff = bk_reser.limitdate

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:
            output_list.cm_id = guest.phonetik2
            output_list.sales = guest.phonetik3

        queasy = get_cache (Queasy, {"key": [(eq, 146)],"char1": [(eq, to_string(bk_veran.segmentcode))]})

        if queasy:
            output_list.segment = char3
        total_estrev =  to_decimal(total_estrev) + to_decimal(bk_veran.deposit)
        total_paid =  to_decimal(total_paid) + to_decimal(bk_veran.total_paid)
        troomrev =  to_decimal(troomrev) + to_decimal(bk_func.rpreis[0])
        tfbrev =  to_decimal(tfbrev) + to_decimal((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0]) )
        tothrev =  to_decimal(tothrev) + to_decimal(other_rev)
        ttrev =  to_decimal(ttrev) + to_decimal((bk_func.rpreis[0] + (bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) +\
                other_rev )

    create_list()

    return generate_output()