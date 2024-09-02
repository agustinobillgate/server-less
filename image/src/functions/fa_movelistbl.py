from functions.additional_functions import *
import decimal
from datetime import date
from models import Mathis, Fa_artikel, Fa_op, Htparam

def fa_movelistbl(c_procedure:str, bl_all:bool, user_init:str, typ_of:str, main_query:int, sub_query:int, int_query:int, fdate:date, tdate:date):
    retmessage = 0
    output_list_list = []
    mathis = fa_artikel = fa_op = htparam = None

    output_list = tmp_mathis = fa_buff = inventory = None

    output_list_list, Output_list = create_model("Output_list", {"asset_name":str, "asset_no":str, "move_from":str, "move_to":str, "datum":date, "usrid":str, "zeit":str, "qty":int, "price":decimal, "amount":decimal})
    tmp_mathis_list, Tmp_mathis = create_model_like(Mathis)

    Fa_buff = Fa_artikel
    Inventory = Fa_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal retmessage, output_list_list, mathis, fa_artikel, fa_op, htparam
        nonlocal fa_buff, inventory


        nonlocal output_list, tmp_mathis, fa_buff, inventory
        nonlocal output_list_list, tmp_mathis_list
        return {"retmessage": retmessage, "output-list": output_list_list}

    def create_list():

        nonlocal retmessage, output_list_list, mathis, fa_artikel, fa_op, htparam
        nonlocal fa_buff, inventory


        nonlocal output_list, tmp_mathis, fa_buff, inventory
        nonlocal output_list_list, tmp_mathis_list

        if bl_all:

            fa_op_obj_list = []
            for fa_op, mathis in db_session.query(Fa_op, Mathis).join(Mathis,(Mathis.nr == Fa_op.nr) &  (Mathis.flag == 1)).filter(
                    (Fa_op.opart == 2) &  (Fa_op.datum >= fdate) &  (Fa_op.datum <= tdate)).all():
                if fa_op._recid in fa_op_obj_list:
                    continue
                else:
                    fa_op_obj_list.append(fa_op._recid)


                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.asset_name = mathis.name
                output_list.asset_no = mathis.asset
                output_list.datum = fa_op.datum
                output_list.zeit = to_string(fa_op.zeit, "HH:MM:SS")
                output_list.move_from = entry(2, fa_op.docu_nr, ";;")
                output_list.move_to = entry(4, fa_op.docu_nr, ";;")
                output_list.usrid = fa_op.id
                output_list.qty = fa_op.anzahl
                output_list.price = fa_op.einzelpreis
                output_list.amount = fa_op.warenwert


        else:

            if typ_of.lower()  == "1":
                tmp_mathis_list.clear()

                if main_query != 0:

                    if sub_query != 0:

                        fa_artikel_obj_list = []
                        for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
                                (Fa_artikel.gnr == main_query) &  (Fa_artikel.subgrp == sub_query)).all():
                            if fa_artikel._recid in fa_artikel_obj_list:
                                continue
                            else:
                                fa_artikel_obj_list.append(fa_artikel._recid)


                            tmp_mathis = Tmp_mathis()
                            tmp_mathis_list.append(tmp_mathis)

                            buffer_copy(mathis, tmp_mathis)
                    else:

                        fa_artikel_obj_list = []
                        for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
                                (Fa_artikel.gnr == main_query)).all():
                            if fa_artikel._recid in fa_artikel_obj_list:
                                continue
                            else:
                                fa_artikel_obj_list.append(fa_artikel._recid)


                            tmp_mathis = Tmp_mathis()
                            tmp_mathis_list.append(tmp_mathis)

                            buffer_copy(mathis, tmp_mathis)

                    for tmp_mathis in query(tmp_mathis_list):

                        for fa_op in db_session.query(Fa_op).filter(
                                (Fa_op.opart == 2) &  (Fa_op.datum >= fdate) &  (Fa_op.datum <= tdate) &  (Fa_op.nr == tmp_mathis.nr)).all():
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.asset_name = tmp_mathis.name
                            output_list.asset_no = tmp_mathis.asset
                            output_list.datum = fa_op.datum
                            output_list.zeit = to_string(fa_op.zeit, "HH:MM:SS")
                            output_list.move_from = entry(2, fa_op.docu_nr, ";;")
                            output_list.move_to = entry(4, fa_op.docu_nr, ";;")
                            output_list.usrid = fa_op.id
                            output_list.qty = fa_op.anzahl
                            output_list.price = fa_op.einzelpreis
                            output_list.amount = fa_op.warenwert


            else:

                for mathis in db_session.query(Mathis).filter(
                        (Mathis.asset == to_string(int_query))).all():

                    for fa_op in db_session.query(Fa_op).filter(
                            (Fa_op.opart == 2) &  (Fa_op.datum >= fdate) &  (Fa_op.datum <= tdate) &  (Fa_op.nr == mathis.nr)).all():
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.asset_name = mathis.name
                        output_list.asset_no = mathis.asset
                        output_list.datum = fa_op.datum
                        output_list.zeit = to_string(fa_op.zeit, "HH:MM:SS")
                        output_list.move_from = entry(2, fa_op.docu_nr, ";;")
                        output_list.move_to = entry(4, fa_op.docu_nr, ";;")
                        output_list.usrid = fa_op.id
                        output_list.qty = fa_op.anzahl
                        output_list.price = fa_op.einzelpreis
                        output_list.amount = fa_op.warenwert

    def cancel_upgrade():

        nonlocal retmessage, output_list_list, mathis, fa_artikel, fa_op, htparam
        nonlocal fa_buff, inventory


        nonlocal output_list, tmp_mathis, fa_buff, inventory
        nonlocal output_list_list, tmp_mathis_list

        last_depn:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 881)).first()
        last_depn = htparam.fdate

        fa_op = db_session.query(Fa_op).filter(
                (Fa_op.opart == 4) &  (Fa_op.nr == fa_artikel.nr) &  (Fa_op.datum == fa_artikel.deleted)).first()

        if get_year(fa_op.datum) == get_year(last_depn) and get_month(fa_op.datum) == get_month(last_depn):
            retmessage = 1

            return

        fa_op = db_session.query(Fa_op).first()
        fa_op.loeschflag = 1

        fa_op = db_session.query(Fa_op).first()

        fa_artikel = db_session.query(Fa_artikel).first()
        fa_artikel.loeschflag = 0
        fa_artikel.deleted = None
        fa_artikel.DID = user_init
        fa_art.p_nr = 0

        fa_artikel = db_session.query(Fa_artikel).first()

        fa_buff = db_session.query(Fa_buff).filter(
                    (Fa_buff.nr == fa_artikel.p_nr)).first()
        fa_buff.warenwert = fa_buff.warenwert - fa_artikel.warenwert
        fa_buff.book_wert = fa_buff.book_wert - fa_artikel.warenwert

        fa_buff = db_session.query(Fa_buff).first()

    if c_procedure.lower()  == "create_list":
        create_list()

    elif c_procedure.lower()  == "cancel_upgrade":
        cancel_upgrade()

    return generate_output()