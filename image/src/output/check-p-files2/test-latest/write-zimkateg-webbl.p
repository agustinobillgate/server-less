

DEF TEMP-TABLE t-zimkateg LIKE zimkateg
    FIELD priority  AS INTEGER
    FIELD max-avail AS INTEGER. /* max available - BLY/ED1FBE/25.03.2025 */

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-zimkateg NO-ERROR.
IF NOT AVAILABLE t-zimkateg THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE zimkateg.
        BUFFER-COPY t-zimkateg TO zimkateg.
        RELEASE zimkateg.

        FIND FIRST queasy WHERE queasy.KEY = 325
            AND queasy.number1 = t-zimkateg.zikatnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN DO:
            CREATE queasy.
            ASSIGN queasy.KEY     = 325
                   queasy.number1 = t-zimkateg.zikatnr
                   queasy.number2 = t-zimkateg.priority
                   queasy.number3 = t-zimkateg.max-avail
            .
            RELEASE queasy.
        END.
        ELSE DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN 
                queasy.number2 = t-zimkateg.priority
                queasy.number3 = t-zimkateg.max-avail
            .
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.

        ASSIGN success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = t-zimkateg.zikatnr
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
        DO:
            BUFFER-COPY t-zimkateg TO zimkateg.
            RELEASE zimkateg.

            FIND FIRST queasy WHERE queasy.KEY = 325
                AND queasy.number1 = t-zimkateg.zikatnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN DO:
                CREATE queasy.
                ASSIGN queasy.KEY     = 325
                       queasy.number1 = t-zimkateg.zikatnr
                       queasy.number2 = t-zimkateg.priority
                       queasy.number3 = t-zimkateg.max-avail
                .
                RELEASE queasy.
            END.
            ELSE DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN 
                    queasy.number2 = t-zimkateg.priority
                    queasy.number3 = t-zimkateg.max-avail
                .
                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
            END.

            ASSIGN success-flag = YES.
        END.
    END.
END CASE.

