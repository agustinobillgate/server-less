
DEFINE TEMP-TABLE t-budget   LIKE budget.

DEF INPUT PARAMETER departement AS INT.
DEF INPUT PARAMETER artnr AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-budget.

FOR EACH budget WHERE 
    budget.departement = departement AND 
    /*budget.artnr = artnr AND*/                       /*wenni 20/07/16*/
    budget.datum GE from-date AND 
    budget.datum LE to-date BY budget.datum:
    CREATE t-budget.
    BUFFER-COPY budget TO t-budget.
END.

