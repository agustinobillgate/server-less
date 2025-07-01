
DEFINE TEMP-TABLE main-task
    FIELD nr        AS INTEGER COLUMN-LABEL "No" FORMAT ">>9"
    FIELD bezeich   AS CHAR    COLUMN-LABEL "Object" FORMAT "x(32)"
    FIELD categ-nr AS INTEGER               /*FD for web*/
    FIELD categ-nm AS CHAR  FORMAT "x(24)"  /*FD for web*/
    .

DEF INPUT PARAMETER dept-nr AS INT.
DEF OUTPUT PARAMETER TABLE FOR main-task.

RUN create-main.


PROCEDURE create-main:
    DEF BUFFER queasy1 FOR queasy.
    DEF BUFFER subtask FOR eg-subtask.

    IF dept-nr = 0 THEN
        FOR EACH queasy1 WHERE queasy1.KEY = 133 NO-LOCK BY queasy1.number1:
            CREATE main-task.
            ASSIGN 
                main-task.nr = queasy1.number1
                main-task.bezeich = queasy1.CHAR1.

            FIND FIRST queasy WHERE queasy.KEY EQ 132 AND queasy.number1 EQ queasy1.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN 
            DO:
                ASSIGN
                    main-task.categ-nr = queasy.number1
                    main-task.categ-nm = queasy.char1.
            END.                
        END.
    ELSE
        FOR EACH queasy1 WHERE queasy1.KEY = 133 NO-LOCK BY queasy1.number1:
            FIND FIRST subtask WHERE subtask.main-nr = queasy1.number1 AND
                subtask.dept-nr = dept-nr /*AND subtask.reserve-int = ""*/ NO-LOCK NO-ERROR.
            IF AVAILABLE subtask THEN
            DO:
                CREATE main-task.
                ASSIGN
                    main-task.nr = queasy1.number1
                    main-task.bezeich = queasy1.char1.

                FIND FIRST queasy WHERE queasy.KEY EQ 132 AND queasy.number1 EQ queasy1.number2 NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN 
                DO:
                    ASSIGN
                        main-task.categ-nr = queasy.number1
                        main-task.categ-nm = queasy.char1.
                END. 
            END.
            /*
            ELSE
            DO:
                    CREATE main-task.
                    ASSIGN 
                        main-task.nr = queasy1.number1
                        main-task.bezeich = queasy1.CHAR1.

            END.
            */
        END.
END.
