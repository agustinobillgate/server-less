#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, Fa_artikel, Fa_op, Htparam

def fa_movelistbl(c_procedure:string, bl_all:bool, user_init:string, typ_of:string, main_query:int, sub_query:int, int_query:int, fdate:date, tdate:date):

    prepare_cache ([Fa_artikel, Fa_op, Htparam])

    retmessage = 0
    output_list_data = []
    mathis = fa_artikel = fa_op = htparam = None

    output_list = tmp_mathis = fa_buff = inventory = None

    output_list_data, Output_list = create_model("Output_list", {"asset_name":string, "asset_no":string, "move_from":string, "move_to":string, "datum":date, "usrid":string, "zeit":string, "qty":int, "price":Decimal, "amount":Decimal})
    tmp_mathis_data, Tmp_mathis = create_model_like(Mathis)

    Fa_buff = create_buffer("Fa_buff",Fa_artikel)
    Inventory = create_buffer("Inventory",Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal retmessage, output_list_data, mathis, fa_artikel, fa_op, htparam
        nonlocal c_procedure, bl_all, user_init, typ_of, main_query, sub_query, int_query, fdate, tdate
        nonlocal fa_buff, inventory


        nonlocal output_list, tmp_mathis, fa_buff, inventory
        nonlocal output_list_data, tmp_mathis_data

        return {"retmessage": retmessage, "output-list": output_list_data}

    def create_list():

        nonlocal retmessage, output_list_data, mathis, fa_artikel, fa_op, htparam
        nonlocal c_procedure, bl_all, user_init, typ_of, main_query, sub_query, int_query, fdate, tdate
        nonlocal fa_buff, inventory


        nonlocal output_list, tmp_mathis, fa_buff, inventory
        nonlocal output_list_data, tmp_mathis_data

        if bl_all:

            fa_op_obj_list = {}
            for fa_op, mathis in db_session.query(Fa_op, Mathis).join(Mathis,(Mathis.nr == Fa_op.nr) & (Mathis.flag == 1)).filter(
                     (Fa_op.opart == 2) & (Fa_op.datum >= fdate) & (Fa_op.datum <= tdate)).order_by(Fa_op.datum).all():
                if fa_op_obj_list.get(fa_op._recid):
                    continue
                else:
                    fa_op_obj_list[fa_op._recid] = True


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.asset_name = mathis.name
                output_list.asset_no = mathis.asset
                output_list.datum = fa_op.datum
                output_list.zeit = to_string(fa_op.zeit, "HH:MM:SS")
                output_list.move_from = entry(2, fa_op.docu_nr, ";;")
                output_list.move_to = entry(4, fa_op.docu_nr, ";;")
                output_list.usrid = fa_op.id
                output_list.qty = fa_op.anzahl
                output_list.price =  to_decimal(fa_op.einzelpreis)
                output_list.amount =  to_decimal(fa_op.warenwert)


        else:

            if typ_of.lower()  == ("1").lower() :
                tmp_mathis_data.clear()

                if main_query != 0:

                    if sub_query != 0:

                        fa_artikel_obj_list = {}
                        for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
                                 (Fa_artikel.gnr == main_query) & (Fa_artikel.subgrp == sub_query)).order_by(Fa_artikel.nr).all():
                            if fa_artikel_obj_list.get(fa_artikel._recid):
                                continue
                            else:
                                fa_artikel_obj_list[fa_artikel._recid] = True


                            tmp_mathis = Tmp_mathis()
                            tmp_mathis_data.append(tmp_mathis)

                            buffer_copy(mathis, tmp_mathis)
                    else:

                        fa_artikel_obj_list = {}
                        for fa_artikel, mathis in db_session.query(Fa_artikel, Mathis).join(Mathis,(Mathis.nr == Fa_artikel.nr)).filter(
                                 (Fa_artikel.gnr == main_query)).order_by(Fa_artikel.nr).all():
                            if fa_artikel_obj_list.get(fa_artikel._recid):
                                continue
                            else:
                                fa_artikel_obj_list[fa_artikel._recid] = True


                            tmp_mathis = Tmp_mathis()
                            tmp_mathis_data.append(tmp_mathis)

                            buffer_copy(mathis, tmp_mathis)

                    for tmp_mathis in query(tmp_mathis_data):

                        for fa_op in db_session.query(Fa_op).filter(
                                 (Fa_op.opart == 2) & (Fa_op.datum >= fdate) & (Fa_op.datum <= tdate) & (Fa_op.nr == tmp_mathis.nr)).order_by(Fa_op.datum).all():
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.asset_name = tmp_mathis.name
                            output_list.asset_no = tmp_mathis.asset
                            output_list.datum = fa_op.datum
                            output_list.zeit = to_string(fa_op.zeit, "HH:MM:SS")
                            output_list.move_from = entry(2, fa_op.docu_nr, ";;")
                            output_list.move_to = entry(4, fa_op.docu_nr, ";;")
                            output_list.usrid = fa_op.id
                            output_list.qty = fa_op.anzahl
                            output_list.price =  to_decimal(fa_op.einzelpreis)
                            output_list.amount =  to_decimal(fa_op.warenwert)


            else:

                for mathis in db_session.query(Mathis).filter(
                         (Mathis.asset == to_string(int_query))).order_by(Mathis._recid).all():

                    for fa_op in db_session.query(Fa_op).filter(
                             (Fa_op.opart == 2) & (Fa_op.datum >= fdate) & (Fa_op.datum <= tdate) & (Fa_op.nr == mathis.nr)).order_by(Fa_op.datum).all():
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.asset_name = mathis.name
                        output_list.asset_no = mathis.asset
                        output_list.datum = fa_op.datum
                        output_list.zeit = to_string(fa_op.zeit, "HH:MM:SS")
                        output_list.move_from = entry(2, fa_op.docu_nr, ";;")
                        output_list.move_to = entry(4, fa_op.docu_nr, ";;")
                        output_list.usrid = fa_op.id
                        output_list.qty = fa_op.anzahl
                        output_list.price =  to_decimal(fa_op.einzelpreis)
                        output_list.amount =  to_decimal(fa_op.warenwert)


    def cancel_upgrade():

        nonlocal retmessage, output_list_data, mathis, fa_artikel, fa_op, htparam
        nonlocal c_procedure, bl_all, user_init, typ_of, main_query, sub_query, int_query, fdate, tdate
        nonlocal fa_buff, inventory


        nonlocal output_list, tmp_mathis, fa_buff, inventory
        nonlocal output_list_data, tmp_mathis_data

        last_depn:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 881)]})
        last_depn = htparam.fdate

        fa_op = get_cache (Fa_op, {"opart": [(eq, 4)],"nr": [(eq, fa_artikel.nr)],"datum": [(eq, fa_artikel.deleted)]})

        if get_year(fa_op.datum) == get_year(last_depn) and get_month(fa_op.datum) == get_month(last_depn):
            retmessage = 1

            return
        pass
        fa_op.loeschflag = 1


        pass
        pass
        fa_artikel.loeschflag = 0
        fa_artikel.deleted = None
        fa_artikel.did = user_init
        fa_artikel.p_nr = 0


        pass

        fa_buff = get_cache (Fa_artikel, {"nr": [(eq, fa_artikel.p_nr)]})
        fa_buff.warenwert =  to_decimal(fa_buff.warenwert) - to_decimal(fa_artikel.warenwert)
        fa_buff.book_wert =  to_decimal(fa_buff.book_wert) - to_decimal(fa_artikel.warenwert)


        pass

    if c_procedure.lower()  == ("create-list").lower() :
        create_list()

    elif c_procedure.lower()  == ("cancel-upgrade").lower() :
        cancel_upgrade()

    return generate_output()