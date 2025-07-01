
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER do-it AS LOGICAL INIT YES.

/*Alder - Serverless - Issue 807 - Start*/
FIND FIRST fa-grup WHERE RECID(fa-grup) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE fa-grup THEN
DO:
    FIND FIRST fa-artikel WHERE fa-artikel.subgrp EQ fa-grup.gnr NO-LOCK NO-ERROR. 
    IF AVAILABLE fa-artikel THEN 
    DO: 
      do-it = NO.
    END.
    ELSE
    DO:
        FIND CURRENT fa-grup EXCLUSIVE-LOCK.
        DELETE fa-grup.
        RELEASE fa-grup.
    END.
END.
/*Alder - Serverless - Issue 807 - End*/

