
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER j       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-rjournal.

PROCEDURE del-old-rjournal: 
DEFINE VARIABLE anz  AS INTEGER. 

DEFINE BUFFER jbuff  FOR h-journal.
DEFINE BUFFER qbuff  FOR h-queasy.

  FIND FIRST htparam WHERE paramnr = 165 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
  /*MTmess-str = translateExtended ("Deleted old restaurant journals",lvCAREA,"") 
      + "  " + STRING(i). 
  DISP mess-str WITH FRAME frame1.*/

  FIND FIRST h-journal WHERE h-journal.bill-datum LE (ci-date - anz) 
      USE-INDEX chrono_ix NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE h-journal:
      FIND FIRST guest-queasy NO-LOCK WHERE
        guest-queasy.betriebsnr = 0                        AND
        guest-queasy.KEY        = "gast-info"              AND
        guest-queasy.char1      = STRING(h-journal.rechnr) AND
        guest-queasy.number1    = h-journal.departement    AND
        guest-queasy.date1      = h-journal.bill-datum     USE-INDEX b-char_ix
        NO-ERROR.
      IF NOT AVAILABLE guest-queasy THEN
      DO TRANSACTION:
          i = i + 1. 
          /*MTmess-str = translateExtended ("Deleted old restaurant journals",lvCAREA,"") 
              + " " + STRING(i). 
          DISP mess-str WITH FRAME frame1. */
          FIND FIRST jbuff WHERE RECID(jbuff) = RECID(h-journal) EXCLUSIVE-LOCK.
          DELETE jbuff.
          RELEASE jbuff.
      END.
      FIND NEXT h-journal WHERE h-journal.bill-datum LE (ci-date - anz) 
          USE-INDEX chrono_ix NO-LOCK NO-ERROR.
  END.
/*
  FOR EACH h-journal WHERE h-journal.bill-datum LT (ci-date - anz) 
    AND h-journal.sysdate LT (ci-date - anz) 
    AND h-journal.zeit GE 0 USE-INDEX chrono_ix NO-LOCK 
    BY h-journal.departement BY h-journal.rechnr:

    FIND FIRST guest-queasy NO-LOCK WHERE
      guest-queasy.betriebsnr = 0                     AND
      guest-queasy.KEY        = "gast-info"              AND
      guest-queasy.char1      = STRING(h-journal.rechnr) AND
      guest-queasy.number1    = h-journal.departement    AND
      guest-queasy.date1      = h-journal.bill-datum     USE-INDEX b-char_ix
      NO-ERROR.

    IF NOT AVAILABLE guest-queasy THEN
    DO TRANSACTION:
      i = i + 1. 
      mess-str = translateExtended ("Deleted old restaurant journals",lvCAREA,"") 
          + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. 
      FIND FIRST hjbuff WHERE RECID(hjbuff) = RECID(h-journal) EXCLUSIVE-LOCK.
      DELETE hjbuff. 
      RELEASE hjbuff.
    END. 
  END. 
*/ 
  j = 0. 
  FIND FIRST h-queasy WHERE h-queasy.datum LE (ci-date - 2) NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE h-queasy: 
    DO TRANSACTION: 
      j = j + 1. 
      /*MTmess-str = translateExtended ("Deleted h-queasy records",lvCAREA,"") 
          + " " + STRING(j). 
      DISP mess-str WITH FRAME frame1. */
      FIND FIRST qbuff WHERE RECID(qbuff) = RECID(h-queasy) EXCLUSIVE-LOCK. 
      DELETE qbuff.
      RELEASE qbuff.
    END. 
    FIND NEXT h-queasy WHERE h-queasy.datum LE (ci-date - 2) NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 

