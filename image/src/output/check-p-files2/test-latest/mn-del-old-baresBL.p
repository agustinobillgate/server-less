
DEFINE OUTPUT PARAMETER i           AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN nt-bahistory.p.
RUN del-old-bares.

PROCEDURE del-old-bares:
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE curr-nr AS INTEGER INITIAL 0. 
/* old banquet reservation */
  FIND FIRST htparam WHERE paramnr = 722 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60.
 
  FOR EACH bk-func WHERE bk-func.datum LE (ci-date - anz) EXCLUSIVE-LOCK 
    BY bk-func.veran-nr: 
    IF curr-nr = 0 THEN curr-nr = bk-func.veran-nr. 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-func.veran-nr 
      AND bk-reser.veran-resnr = bk-func.veran-seite 
      AND bk-reser.resstatus LE 1 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN DELETE bk-reser. 
    IF curr-nr NE bk-func.veran-nr THEN 
    DO: 
      FIND FIRST bk-veran WHERE bk-veran.veran-nr = curr-nr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE bk-veran THEN 
      DO:
        FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
          AND bk-reser.datum GT (ci-date - anz) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bk-reser THEN
        DO:
          FIND CURRENT bk-veran EXCLUSIVE-LOCK.
          DELETE bk-veran. 
          RELEASE bk-veran.
          curr-nr = bk-func.veran-nr. 
          i = i + 1.
        END.
      END.
    END. 
    DELETE bk-func. 
  END. 
END. 
