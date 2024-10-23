DEFINE TEMP-TABLE output-list 
  FIELD outnr AS INTEGER FORMAT ">9" 
  FIELD act-str AS CHAR FORMAT "x(78)". 

DEFINE TEMP-TABLE t-b-storno LIKE b-storno.

DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE INPUT PARAMETER add-str AS CHARACTER.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER counter-reason AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.


FIND FIRST b-storno WHERE b-storno.bankettnr = resnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE b-storno THEN
DO :
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr NO-LOCK NO-ERROR.
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR.
    CREATE b-storno.
    b-storno.bankettnr = resnr.
    b-storno.gastnr = bk-veran.gastnr.
    counter-reason = 0.
END.
FIND CURRENT b-storno EXCLUSIVE-LOCK.
b-storno.grund[18] = CAPS(add-str) + " " + STRING(TODAY, "99/99/99") + "-" +
    STRING(TIME, "hh:mm:ss") + " (" + user-init + ")".
FIND CURRENT b-storno NO-LOCK.

RUN create-outlist. 

PROCEDURE create-outlist: 
DEFINE VARIABLE i AS INTEGER. 
  counter-reason = 0. 
  FOR EACH output-list : 
    DELETE output-list. 
  END. 
  DO i = 1 TO 18: 
    IF b-storno.grund[i] NE "" THEN 
    DO: 
      CREATE output-list. 
      ASSIGN 
        outnr = i 
        act-str = b-storno.grund[i]. 
      counter-reason = i.
    END. 
  END. 
END. 
