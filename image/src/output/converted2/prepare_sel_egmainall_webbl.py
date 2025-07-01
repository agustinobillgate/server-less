#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_subtask

def prepare_sel_egmainall_webbl(dept_nr:int):

    prepare_cache ([Queasy])

    main_task_list = []
    queasy = eg_subtask = None

    main_task = None

    main_task_list, Main_task = create_model("Main_task", {"nr":int, "bezeich":string, "categ_nr":int, "categ_nm":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_task_list, queasy, eg_subtask
        nonlocal dept_nr


        nonlocal main_task
        nonlocal main_task_list

        return {"main-task": main_task_list}

    def create_main():

        nonlocal main_task_list, queasy, eg_subtask
        nonlocal dept_nr


        nonlocal main_task
        nonlocal main_task_list

        queasy1 = None
        subtask = None
        Queasy1 =  create_buffer("Queasy1",Queasy)
        Subtask =  create_buffer("Subtask",Eg_subtask)

        if dept_nr == 0:

            for queasy1 in db_session.query(Queasy1).filter(
                     (Queasy1.key == 133)).order_by(Queasy1.number1).all():
                main_task = Main_task()
                main_task_list.append(main_task)

                main_task.nr = queasy1.number1
                main_task.bezeich = queasy1.char1

                queasy = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy1.number2)]})

                if queasy:
                    main_task.categ_nr = queasy.number1
                    main_task.categ_nm = queasy.char1

        else:

            for queasy1 in db_session.query(Queasy1).filter(
                     (Queasy1.key == 133)).order_by(Queasy1.number1).all():

                subtask = db_session.query(Subtask).filter(
                         (Subtask.main_nr == queasy1.number1) & (Subtask.dept_nr == dept_nr)).first()

                if subtask:
                    main_task = Main_task()
                    main_task_list.append(main_task)

                    main_task.nr = queasy1.number1
                    main_task.bezeich = queasy1.char1

                    queasy = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy1.number2)]})

                    if queasy:
                        main_task.categ_nr = queasy.number1
                        main_task.categ_nm = queasy.char1


    create_main()

    return generate_output()