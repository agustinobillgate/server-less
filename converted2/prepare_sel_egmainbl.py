#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_subtask

def prepare_sel_egmainbl(categ_nr:int, dept_nr:int):

    prepare_cache ([Queasy])

    main_task_data = []
    queasy = eg_subtask = None

    main_task = None

    main_task_data, Main_task = create_model("Main_task", {"nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_task_data, queasy, eg_subtask
        nonlocal categ_nr, dept_nr


        nonlocal main_task
        nonlocal main_task_data

        return {"main-task": main_task_data}

    def create_main():

        nonlocal main_task_data, queasy, eg_subtask
        nonlocal categ_nr, dept_nr


        nonlocal main_task
        nonlocal main_task_data

        queasy1 = None
        subtask = None
        Queasy1 =  create_buffer("Queasy1",Queasy)
        Subtask =  create_buffer("Subtask",Eg_subtask)

        for queasy1 in db_session.query(Queasy1).filter(
                 (Queasy1.key == 133) & (Queasy1.number2 == categ_nr)).order_by(Queasy1.number1).all():
            main_task = Main_task()
            main_task_data.append(main_task)

            main_task.nr = queasy1.number1
            main_task.bezeich = queasy1.char1

    create_main()

    return generate_output()