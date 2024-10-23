DEFINE TEMP-TABLE b1-list
    FIELD resnr         LIKE res-line.resnr
    FIELD reslinnr      LIKE res-line.reslinnr
    FIELD zinr          LIKE res-line.zinr
    FIELD name          LIKE res-line.name
    FIELD arrangement   LIKE res-line.arrangement
    FIELD ankunft       LIKE res-line.ankunft
    FIELD abreise       LIKE res-line.abreise.


DEFINE INPUT PARAMETER roomno   AS CHAR.
DEFINE INPUT PARAMETER sorttype AS INTEGER.
DEFINE INPUT PARAMETER gname    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

DEFINE BUFFER bbuff FOR bill.
RUN disp-it.
 
/*************** PROCEDURE ***************/
 
PROCEDURE disp-it: 
DEFINE VARIABLE name AS CHAR. 
DEFINE VARIABLE rmlen AS INTEGER. 
  rmlen = length(roomno). 
  IF sorttype = 1 THEN 
  DO: 
    FOR EACH res-line WHERE active-flag = 1 
      AND res-line.resstatus NE 12 
      AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (roomno) NO-LOCK,
      FIRST bbuff WHERE bbuff.resnr = res-line.resnr
      AND bbuff.reslinnr = res-line.reslinnr NO-LOCK
      BY res-line.zinr BY res-line.name:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 2 THEN 
  DO: 
    FOR EACH res-line WHERE active-flag = 1 
      AND res-line.resstatus NE 12 
      AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE (roomno) 
      AND res-line.name GE gname NO-LOCK,
      FIRST bbuff WHERE bbuff.resnr = res-line.resnr
      AND bbuff.reslinnr = res-line.reslinnr NO-LOCK
      BY res-line.name BY res-line.zinr:
        RUN assign-it.
    END.
    IF AVAILABLE res-line THEN roomno = res-line.zinr. 
  END. 
END. 

PROCEDURE assign-it:
    CREATE b1-list.
    ASSIGN
    b1-list.resnr         = res-line.resnr
    b1-list.reslinnr      = res-line.reslinnr
    b1-list.zinr          = res-line.zinr
    b1-list.name          = res-line.name
    b1-list.arrangement   = res-line.arrangement
    b1-list.ankunft       = res-line.ankunft
    b1-list.abreise       = res-line.abreise.
END.
