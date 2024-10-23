DEF TEMP-TABLE t-budget LIKE budget.

DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER fdate       AS DATE.
DEF INPUT PARAMETER tdate       AS DATE.
DEF INPUT PARAMETER artnr       AS INT.
DEF INPUT PARAMETER departement AS INT.
DEF INPUT PARAMETER betrag      AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-budget.

DEF VAR datum AS DATE.
DO datum = fdate TO tdate: 
    FIND FIRST budget WHERE budget.datum = datum
        AND budget.artnr = artnr
        AND budget.departement = departement NO-LOCK NO-ERROR.
    IF NOT AVAILABLE budget THEN 
    DO: 
        create budget. 
        budget.datum = datum. 
        budget.artnr = artnr. 
        budget.departement = departement. 
    END. 
    FIND CURRENT budget EXCLUSIVE-LOCK.
    budget.betrag = betrag.
    FIND CURRENT budget NO-LOCK.
END.


FOR EACH budget WHERE budget.datum GE from-date
    AND budget.datum LE to-date BY budget.datum:
    CREATE t-budget.
    BUFFER-COPY budget TO t-budget.
END.
