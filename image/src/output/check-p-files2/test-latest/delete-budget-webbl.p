DEFINE TEMP-TABLE del-list 
    FIELD int1  AS INT
    FIELD int2  AS INT
    FIELD date1 AS DATE.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR del-list.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH del-list NO-LOCK BY del-list.int1 :
            FIND FIRST budget WHERE budget.artnr = del-list.int1 AND budget.departement = del-list.int2
            AND budget.datum = del-list.date1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE budget THEN
            DO:
                DELETE budget.
                RELEASE budget.
                ASSIGN success-flag = YES.
            END.
        END.
       
    END.
END CASE.

