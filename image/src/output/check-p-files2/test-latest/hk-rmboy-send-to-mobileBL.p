
DEFINE TEMP-TABLE rmlist
    FIELD flag      AS INTEGER  FORMAT ">>>" 
    FIELD code      AS CHAR     FORMAT "x(3)"     COLUMN-LABEL "Loc"
    FIELD zinr      LIKE zimmer.zinr              COLUMN-LABEL "RmNo"
    FIELD credit    AS INTEGER  FORMAT ">>>"      COLUMN-LABEL "CP"
    FIELD floor     AS INTEGER  FORMAT ">>"       COLUMN-LABEL "FL"
    FIELD gname     AS CHAR     FORMAT "x(32)"    COLUMN-LABEL "Main Guest Name" 
    FIELD pic       AS CHAR     FORMAT "x(12)"    COLUMN-LABEL "Person in Charge"
    FIELD bemerk    AS CHAR     FORMAT "x(50)"    COLUMN-LABEL "Remarks"
    FIELD rstat     AS CHAR     FORMAT "x(20)"    COLUMN-LABEL "Room Status" 
    FIELD ankunft   AS DATE     FORMAT "99/99/99" COLUMN-LABEL "Arrival" 
    FIELD abreise   AS DATE     FORMAT "99/99/99" COLUMN-LABEL "Departure" 
    FIELD kbezeich  AS CHAR     FORMAT "x(12)"    COLUMN-LABEL "Description" 
    FIELD nation    AS CHAR     FORMAT "x(3)"     COLUMN-LABEL "Nat" 
    FIELD paxnr     AS INTEGER  FORMAT ">>>"      COLUMN-LABEL "No".

DEFINE INPUT PARAMETER TABLE FOR rmlist.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO.

DEFINE VARIABLE user-init AS CHAR NO-UNDO.

DEFINE VARIABLE ci-date AS DATE NO-UNDO.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
/* ci-date = fdate.  */             /* Rulita 211024 | Fixing for serverless */
ci-date = htparam.fdate. 

FOR EACH queasy WHERE queasy.KEY EQ 196 AND
  queasy.date1 EQ ci-date AND
  queasy.char2 EQ "" AND queasy.number1 EQ 0 AND queasy.number2 EQ 0:
  DELETE queasy.
END.

FOR EACH rmlist NO-LOCK BY rmlist.pic:
    FIND FIRST bediener WHERE bediener.username = rmlist.pic NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN ASSIGN user-init = bediener.userinit.
    ELSE ASSIGN user-init = " ".

    FIND FIRST queasy WHERE queasy.KEY = 196
        AND ENTRY(1, queasy.char1, ";") = rmlist.zinr
        AND queasy.date1 = ci-date EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        ASSIGN
            queasy.char1 = " "
            queasy.char1 = rmlist.zinr + ";" + user-init + ";" + STRING(rmlist.credit)
            queasy.char2 = ""
            queasy.number1 = 0
            queasy.number2 = 0
          .
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
    ELSE DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY   = 196
            queasy.char1 = rmlist.zinr + ";" + user-init + ";" + STRING(rmlist.credit)
            queasy.date1 = ci-date.
    END.
END.

ASSIGN success-flag = YES.
