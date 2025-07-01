
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-rbill.

FIND FIRST counters WHERE counters.counter-no = 121 EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE counters THEN
DO:
    ASSIGN counters.counter = 0.
    RELEASE counters.
END.

FIND FIRST queasy WHERE queasy.KEY = 191 EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ASSIGN 
        queasy.number1 = 0
        queasy.number2 = 0.
    RELEASE queasy.
END.

PROCEDURE del-old-rbill: 
DEFINE VARIABLE anz AS INTEGER. 
DEF BUFFER bbuff    FOR h-bill.
DEF BUFFER lbuff    FOR h-bill-line.
  
  FIND FIRST htparam WHERE paramnr = 164 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 7. 
  /*MTmess-str = translateExtended ("Deleted old restaurant bills",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */

  DO: 
/*
    FIND FIRST h-bill WHERE h-bill.flag = 1 AND h-bill.departement GE 1 
      NO-LOCK USE-INDEX dept_ix NO-ERROR. 
    DO WHILE AVAILABLE h-bill: 
      FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
        AND h-bill-line.departement = h-bill.departement 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE h-bill-line OR (AVAILABLE h-bill-line 
        AND (h-bill-line.bill-datum + anz) LT ci-date) THEN 
      DO TRANSACTION: 
        i = i + 1. 
        mess-str = translateExtended ("Deleted old restaurant bills",lvCAREA,"") 
            + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. 
        FOR EACH h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr 
          AND h-bill-line.departement = h-bill.departement: 
          delete h-bill-line. 
        END. 
        FIND CURRENT h-bill EXCLUSIVE-LOCK. 
        delete h-bill. 
      END. 
      FIND NEXT h-bill WHERE h-bill.flag = 1 AND h-bill.departement GE 1 
        NO-LOCK USE-INDEX dept_ix NO-ERROR. 
    END. 
*/
    FIND FIRST h-bill-line WHERE h-bill-line.bill-datum LT (ci-date - anz)
        USE-INDEX bildat_index NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE h-bill-line:
        DO TRANSACTION:
            FIND FIRST lbuff WHERE RECID(lbuff) = RECID(h-bill-line) EXCLUSIVE-LOCK.
            DELETE lbuff.
             RELEASE lbuff.
             i = i + 1. 
             /*MTmess-str = translateExtended ("Deleted old restaurant bill lines",lvCAREA,"") 
                 + " " + STRING(i). 
             DISP mess-str WITH FRAME frame1. */
         END.
        FIND NEXT h-bill-line WHERE h-bill-line.bill-datum LT (ci-date - anz)
            USE-INDEX bildat_index NO-LOCK NO-ERROR.
    END.

    i = 0.
    FIND FIRST h-bill WHERE h-bill.flag = 1 AND h-bill.departement GE 1
        USE-INDEX dept_ix NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE h-bill:
        FIND FIRST h-bill-line WHERE h-bill-line.rechnr = h-bill.rechnr
          AND h-bill-line.departement = h-bill.departement NO-LOCK NO-ERROR.
        IF NOT AVAILABLE h-bill-line THEN
        DO TRANSACTION:
          FIND FIRST bbuff WHERE RECID(bbuff) = RECID(h-bill) EXCLUSIVE-LOCK.
          DELETE bbuff.
          RELEASE bbuff.
          i = i + 1. 
          /*MTmess-str = translateExtended ("Deleted old restaurant bills",lvCAREA,"") 
              + " " + STRING(i). 
          DISP mess-str WITH FRAME frame1. */
        END.
        FIND NEXT h-bill WHERE h-bill.flag = 1 AND h-bill.departement GE 1
          USE-INDEX dept_ix NO-LOCK NO-ERROR.
    END.
  END.

  FOR EACH queasy WHERE key = 4: 
     DELETE queasy. 
  END. 
  
  /*MTPAUSE 0. */
END. 

