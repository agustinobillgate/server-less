#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_op, Fa_ordheader, Bediener, Fa_order

def fa_bypolistbl():

    prepare_cache ([Bediener, Fa_order])

    op_list_data = []
    fa_ordheaderlist_data = []
    fa_op = fa_ordheader = bediener = fa_order = None

    op_list = fa_ordheaderlist = None

    op_list_data, Op_list = create_model_like(Fa_op, {"arive_amount":Decimal, "sorting":string})
    fa_ordheaderlist_data, Fa_ordheaderlist = create_model_like(Fa_ordheader, {"create_name":string, "modify_name":string, "total_amount1":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal op_list_data, fa_ordheaderlist_data, fa_op, fa_ordheader, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        return {"op-list": op_list_data, "fa-ordheaderlist": fa_ordheaderlist_data}

    def distinct_op():

        nonlocal op_list_data, fa_ordheaderlist_data, fa_op, fa_ordheader, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        temp_number:string = ""
        op_list_data.clear()

        for fa_op in db_session.query(Fa_op).filter(
                 (Fa_op.loeschflag <= 1) & (Fa_op.warenwert > 0)).order_by(Fa_op.docu_nr, Fa_op.lscheinnr, Fa_op.zeit).all():

            if temp_number == "":
                temp_number = fa_op.lscheinnr
                op_list = Op_list()
                op_list_data.append(op_list)

                buffer_copy(fa_op, op_list)
            else:

                if temp_number != fa_op.lscheinnr:
                    temp_number = fa_op.lscheinnr
                    op_list = Op_list()
                    op_list_data.append(op_list)

                    buffer_copy(fa_op, op_list)


    def create_faordheaderlist():

        nonlocal op_list_data, fa_ordheaderlist_data, fa_op, fa_ordheader, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_data, fa_ordheaderlist_data

        temp_create:string = ""
        temp_modify:string = ""
        total_amount:Decimal = to_decimal("0.0")
        fa_ordheaderlist_data.clear()

        for fa_ordheader in db_session.query(Fa_ordheader).order_by(Fa_ordheader._recid).all():

            if fa_ordheader.created_by != "":

                bediener = get_cache (Bediener, {"userinit": [(eq, fa_ordheader.created_by)]})

                if bediener:
                    temp_create = bediener.username
                else:
                    temp_create = ""
            else:
                temp_create = ""

            if fa_ordheader.modified_by != "":

                bediener = get_cache (Bediener, {"userinit": [(eq, fa_ordheader.modified_by)]})

                if bediener:
                    temp_modify = bediener.username
                else:
                    temp_modify = ""
            else:
                temp_modify = ""

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                total_amount =  to_decimal(total_amount) + to_decimal(fa_order.order_amount)
            fa_ordheaderlist = Fa_ordheaderlist()
            fa_ordheaderlist_data.append(fa_ordheaderlist)

            buffer_copy(fa_ordheader, fa_ordheaderlist)
            fa_ordheaderlist.create_name = temp_create
            fa_ordheaderlist.modify_name = temp_modify
            fa_ordheaderlist.total_amount1 =  to_decimal(total_amount)


            temp_create = ""
            temp_modify = ""
            total_amount =  to_decimal("0")


    distinct_op()
    create_faordheaderlist()

    return generate_output()