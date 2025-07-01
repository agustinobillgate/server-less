
DEFINE TEMP-TABLE l-list LIKE fa-grup. 

DEF INPUT PARAMETER TABLE FOR l-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER fibukonto AS CHAR.
DEF INPUT PARAMETER credit-fibu AS CHAR.
DEF INPUT PARAMETER debit-fibu AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err-no AS INT INIT 0.

DEF VAR fibuChg AS LOGICAL INITIAL NO NO-UNDO.
DEF BUFFER fabuff FOR fa-artikel.

FIND FIRST l-list.
IF case-type = 1 THEN       /* create */
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      err-no = 1.
      RETURN NO-APPLY.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = credit-fibu NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      err-no = 2.
      RETURN NO-APPLY.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = debit-fibu NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      err-no = 3.
      RETURN NO-APPLY.
    END.
    DO: 
      CREATE fa-grup. 
      RUN fill-new-fa-grup.
      FIND CURRENT fa-grup NO-LOCK.
    END.
END.
ELSE IF case-type = 2 THEN       /* chg */
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      err-no = 1.
      /*MTHIDE MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Account Number incorrect.",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      APPLY "entry" TO fibukonto.*/
      RETURN NO-APPLY.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = credit-fibu NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      err-no = 2.
      /*MTHIDE MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Account Number incorrect.",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      APPLY "entry" TO credit-fibu.*/
      RETURN NO-APPLY.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = debit-fibu NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
      err-no = 3.
      /*MTHIDE MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Account Number incorrect.",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      APPLY "entry" TO debit-fibu.*/
      RETURN NO-APPLY.
    END.    
    DO: 
      FIND FIRST fa-grup WHERE RECID(fa-grup) = rec-id NO-LOCK.
      fibuChg = (fa-grup.fibukonto NE fibukonto) OR 
          (fa-grup.credit-fibu NE credit-fibu)   OR
          (fa-grup.debit-fibu NE debit-fibu).
      
      FIND CURRENT fa-grup EXCLUSIVE-LOCK. 
      ASSIGN
        fa-grup.gnr         = l-list.gnr
        fa-grup.bezeich     = l-list.bezeich
        fa-grup.fibukonto   = fibukonto
        fa-grup.credit-fibu = credit-fibu
        fa-grup.debit-fibu  = debit-fibu
      .
      IF fibuChg THEN
      FOR EACH fa-artikel WHERE fa-artikel.subgrp = fa-grup.gnr NO-LOCK:
        IF fa-artikel.fibukonto NE fibukonto OR
           fa-artikel.credit-fibu NE credit-fibu OR
           fa-artikel.debit-fibu NE debit-fibu THEN
        DO:
            FIND FIRST fabuff WHERE RECID(fabuff) = RECID(fa-artikel) 
                EXCLUSIVE-LOCK.
            ASSIGN
                fabuff.fibukonto   = fibukonto
                fabuff.credit-fibu = credit-fibu
                fabuff.debit-fibu  = debit-fibu.
            FIND CURRENT fabuff NO-LOCK.
            RELEASE fabuff.
        END.
        FIND CURRENT fa-grup NO-LOCK. 
      END.
      /*MT
      RUN init-l-list. 
      RUN set-readonly(YES).
      ENABLE btn-addart btn-renart btn-delart WITH FRAME frame1. 
      b1:REFRESH().
      curr-select = "".
      */
    END. 
END.


PROCEDURE fill-new-fa-grup: 
  ASSIGN
    fa-grup.gnr         = l-list.gnr
    fa-grup.bezeich     = l-list.bezeich
    fa-grup.fibukonto   = fibukonto
    fa-grup.credit-fibu = credit-fibu
    fa-grup.debit-fibu  = debit-fibu
    fa-grup.flag        = 1
  .
END. 

