
DEF TEMP-TABLE t-zimkateg LIKE zimkateg
    FIELD priority  AS INTEGER
    FIELD max-avail AS INTEGER. /* max available - BLY/ED1FBE/25.03.2025 */
DEF TEMP-TABLE t-queasy   LIKE queasy.



DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE BUFFER pqueasy FOR queasy.


FOR EACH zimkateg NO-LOCK:
    CREATE t-zimkateg.
    BUFFER-COPY zimkateg TO t-zimkateg.

    FIND FIRST pqueasy WHERE pqueasy.KEY = 325 
        AND pqueasy.number1 = zimkateg.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE pqueasy THEN 
        ASSIGN 
            t-zimkateg.priority     = pqueasy.number2
            t-zimkateg.max-avail    = pqueasy.number3
        .
END.

FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK BY queasy.number1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
