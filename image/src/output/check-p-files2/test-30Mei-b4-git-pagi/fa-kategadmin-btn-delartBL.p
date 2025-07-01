/*Alder - Serverless - Issue 806 - Start*/
DEFINE INPUT PARAMETER rec-id AS INTEGER.
DEFINE OUTPUT PARAMETER do-it AS LOGICAL INITIAL YES.

FIND FIRST fa-kateg WHERE RECID(fa-kateg) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE fa-kateg THEN
DO:
    FIND FIRST fa-artikel WHERE fa-artikel.katnr = fa-kateg.katnr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-artikel THEN
    DO:
        do-it = NO.
    END.
    ELSE
    DO:
        FIND CURRENT fa-kateg EXCLUSIVE-LOCK.
        DELETE fa-kateg.
        RELEASE fa-kateg.
    END.
END.
/*Alder - Serverless - Issue 806 - End*/

/*DEF INPUT  PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER do-it  AS LOGICAL INIT YES.

FIND FIRST fa-kateg WHERE RECID(fa-kateg) = rec-id.

FIND FIRST fa-artikel WHERE fa-artikel.katnr = fa-kateg.katnr 
  NO-LOCK NO-ERROR. 
IF AVAILABLE fa-artikel THEN 
DO: 
  do-it = NO.
END. 
ELSE 
DO: 
    FIND CURRENT fa-kateg EXCLUSIVE-LOCK. 
    delete fa-kateg.
    RELEASE fa-kateg.
END.*/
