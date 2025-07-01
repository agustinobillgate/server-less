
DEFINE INPUT PARAMETER pr-973 AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER yy     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER mm     AS INTEGER NO-UNDO.

IF pr-973 THEN
DO:
    FIND FIRST fa-counter WHERE fa-counter.count-type = 0 AND fa-counter.yy = yy AND fa-counter.mm = mm AND
        fa-counter.dd = dd AND fa-counter.docu-type = 1 EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE fa-counter THEN
    DO:
        CREATE fa-counter.
        ASSIGN fa-counter.count-type = 0
               fa-counter.yy         = yy
               fa-counter.mm         = mm
               fa-counter.dd         = dd
               fa-counter.counters   = 0
               fa-counter.docu-type  = 1.
    END.
    ELSE
    DO:
        FIND CURRENT fa-counter EXCLUSIVE-LOCK.
        ASSIGN fa-counter.counters = fa-counter.counters + 1.
        FIND CURRENT fa-counter NO-LOCK.
    END.   
END.
ELSE
DO:
    FIND FIRST fa-counter WHERE fa-counter.count-type = 1 AND fa-counter.yy = yy AND fa-counter.mm = mm 
        AND fa-counter.docu-type = 1  EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE fa-counter THEN
    DO:
        CREATE fa-counter.
        ASSIGN fa-counter.count-type = 1
               fa-counter.yy         = yy
               fa-counter.mm         = mm
               fa-counter.dd         = 0
               fa-counter.counters   = 0
               fa-counter.docu-type  = 1.
    END.
    ELSE
    DO:
        FIND CURRENT fa-counter EXCLUSIVE-LOCK.
        ASSIGN fa-counter.counters = fa-counter.counters + 1.
        FIND CURRENT fa-counter NO-LOCK.
    END.
END.
