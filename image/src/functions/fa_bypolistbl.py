from functions.additional_functions import *
import decimal
from models import Fa_op, Fa_ordheader, Bediener, Fa_order

def fa_bypolistbl():
    op_list_list = []
    fa_ordheaderlist_list = []
    fa_op = fa_ordheader = bediener = fa_order = None

    op_list = fa_ordheaderlist = None

    op_list_list, Op_list = create_model_like(Fa_op, {"arive_amount":decimal, "sorting":str})
    fa_ordheaderlist_list, Fa_ordheaderlist = create_model_like(Fa_ordheader, {"create_name":str, "modify_name":str, "total_amount1":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal op_list_list, fa_ordheaderlist_list, fa_op, fa_ordheader, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list
        return {"op-list": op_list_list, "fa-ordheaderlist": fa_ordheaderlist_list}

    def distinct_op():

        nonlocal op_list_list, fa_ordheaderlist_list, fa_op, fa_ordheader, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list

        temp_number:str = ""
        op_list_list.clear()

        for fa_op in db_session.query(Fa_op).filter(
                (Fa_op.loeschflag <= 1) &  (Fa_op.warenwert > 0)).all():

            if temp_number == "":
                temp_number = fa_op.lscheinnr
                op_list = Op_list()
                op_list_list.append(op_list)

                buffer_copy(fa_op, op_list)
            else:

                if temp_number != fa_op.lscheinnr:
                    temp_number = fa_op.lscheinnr
                    op_list = Op_list()
                    op_list_list.append(op_list)

                    buffer_copy(fa_op, op_list)

    def create_faordheaderlist():

        nonlocal op_list_list, fa_ordheaderlist_list, fa_op, fa_ordheader, bediener, fa_order


        nonlocal op_list, fa_ordheaderlist
        nonlocal op_list_list, fa_ordheaderlist_list

        temp_create:str = ""
        temp_modify:str = ""
        total_amount:decimal = 0
        fa_ordheaderlist_list.clear()

        for fa_ordheader in db_session.query(Fa_ordheader).all():

            if fa_ordheader.created_by != "":

                bediener = db_session.query(Bediener).filter(
                        (Bediener.userinit == fa_ordheader.created_by)).first()

                if bediener:
                    temp_create = bediener.username
                else:
                    temp_create = ""
            else:
                temp_create = ""

            if fa_ordheader.modified_by != "":

                bediener = db_session.query(Bediener).filter(
                        (Bediener.userinit == fa_ordheader.modified_by)).first()

                if bediener:
                    temp_modify = bediener.username
                else:
                    temp_modify = ""
            else:
                temp_modify = ""

            for fa_order in db_session.query(Fa_order).filter(
                    (Fa_order.order_nr == fa_ordheader.order_nr)).all():
                total_amount = total_amount + fa_order.order_amount
            fa_ordheaderlist = Fa_ordheaderlist()
            fa_ordheaderlist_list.append(fa_ordheaderlist)

            buffer_copy(fa_ordheader, fa_ordheaderlist)
            fa_ordheaderlist.create_name = temp_create
            fa_ordheaderlist.modify_name = temp_modify
            fa_ordheaderlist.total_amount1 = total_amount


            temp_create = ""
            temp_modify = ""
            total_amount = 0

    distinct_op()
    create_faordheaderlist()

    return generate_output()