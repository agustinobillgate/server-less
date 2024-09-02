from functions.additional_functions import *
import decimal
from models import B_storno, Bk_reser, Bk_veran, Guest

def prepare_sales_activity_listbl(resnr:int):
    counter_reason = 0
    output_list_list = []
    print_list_list = []
    b_storno = bk_reser = bk_veran = guest = None

    output_list = print_list = t_b_storno = None

    output_list_list, Output_list = create_model("Output_list", {"outnr":int, "act_str":str})
    print_list_list, Print_list = create_model("Print_list", {"guest":str, "refno":str, "resstatus":str, "rechnr":str, "datum":str, "zeit":str})
    t_b_storno_list, T_b_storno = create_model_like(B_storno)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter_reason, output_list_list, print_list_list, b_storno, bk_reser, bk_veran, guest


        nonlocal output_list, print_list, t_b_storno
        nonlocal output_list_list, print_list_list, t_b_storno_list
        return {"counter_reason": counter_reason, "output-list": output_list_list, "print-list": print_list_list}

    def create_outlist():

        nonlocal counter_reason, output_list_list, print_list_list, b_storno, bk_reser, bk_veran, guest


        nonlocal output_list, print_list, t_b_storno
        nonlocal output_list_list, print_list_list, t_b_storno_list

        i:int = 0
        counter_reason = 0
        output_list_list.clear()
        for i in range(1,18 + 1) :

            if b_storno.grund[i - 1] != "":

                bk_reser = db_session.query(Bk_reser).filter(
                        (Bk_reser.veran_nr == resnr)).first()

                bk_veran = db_session.query(Bk_veran).filter(
                        (Bk_veran.veran_nr == resnr)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == bk_veran.gastnr)).first()

                print_list = query(print_list_list, first=True)

                if bk_reser and bk_veran and guest:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.outnr = i
                    output_list.act_str = b_storno.grund[i - 1]
                    counter_reason = i


                    create_print()

    def create_print():

        nonlocal counter_reason, output_list_list, print_list_list, b_storno, bk_reser, bk_veran, guest


        nonlocal output_list, print_list, t_b_storno
        nonlocal output_list_list, print_list_list, t_b_storno_list

        print_list = query(print_list_list, first=True)

        if not print_list:
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.guest = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma
            print_list.refno = to_string(bk_reser.veran_nr)
            print_list.resstatus = to_string(bk_reser.resstatus)
            print_list.rechnr = to_string(bk_veran.rechnr)
            print_list.datum = to_string(bk_reser.datum) + " - " + to_string(bk_reser.bis_datum)
            print_list.zeit = to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99")

    b_storno = db_session.query(B_storno).filter(
            (B_storno.bankettnr == resnr)).first()

    if b_storno:
        t_b_storno = T_b_storno()
        t_b_storno_list.append(t_b_storno)

        buffer_copy(b_storno, t_b_storno)

    t_b_storno = query(t_b_storno_list, first=True)

    if t_b_storno:
        create_outlist()

    return generate_output()