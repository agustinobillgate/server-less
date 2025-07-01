
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-calls.


PROCEDURE del-old-calls: 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE anz1 AS INTEGER. 
DEFINE VARIABLE anz2 AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 302 no-lock. /* general delete calls */ 
  anz1 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 265 no-lock. /* special del local calls */ 
  anz2 = htparam.finteger. 
  IF anz1 GT anz2 THEN anz = anz1. 
  ELSE anz = anz2.

  /*MTmess-str = translateExtended ("Deleted old calls",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST calls WHERE (calls.datum + anz) LT ci-date 
    AND calls.buchflag = 0 AND calls.zeit GE 0 AND calls.key LE 1 
    NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE calls: 
    IF (SUBSTR(calls.rufnummer,1,1) NE "0" AND (calls.datum + anz2) LT ci-date) 
      OR (calls.datum + anz1) LT ci-date THEN 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Deleted old calls",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND CURRENT calls EXCLUSIVE-LOCK. 
      delete calls. 
    END. 
    FIND NEXT calls WHERE (calls.datum + anz) LT ci-date 
      AND calls.buchflag = 0 AND calls.zeit GE 0 AND calls.key LE 1 
      NO-LOCK NO-ERROR. 
  END. 
  FIND FIRST calls WHERE (calls.datum + anz) LT ci-date 
    AND calls.buchflag = 1 AND calls.zeit GE 0 AND calls.key LE 1 
    NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE calls: 
    IF (SUBSTR(calls.rufnummer,1,1) NE "0" AND (calls.datum + anz2) LT ci-date) 
      OR (calls.datum + anz1) LT ci-date THEN 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Deleted old calls",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND CURRENT calls EXCLUSIVE-LOCK. 
      delete calls. 
    END. 
    FIND NEXT calls WHERE (calls.datum + anz) LT ci-date 
      AND calls.buchflag = 1 AND calls.zeit GE 0 AND calls.key LE 1 
      NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 

