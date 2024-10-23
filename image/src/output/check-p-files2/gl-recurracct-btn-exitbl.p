DEF TEMP-TABLE b1-list LIKE queasy
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD rec-id    AS INT.


DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER case-type      AS INTEGER.
DEF INPUT  PARAMETER titel          AS CHAR.
DEF INPUT  PARAMETER remark         AS CHAR.
DEF INPUT  PARAMETER fibu           AS CHAR.
DEF INPUT  PARAMETER rec-id         AS INTEGER.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-recurracct".

DEFINE buffer gl-acc1 FOR gl-acct.

IF case-type = 1 THEN       /* add */
DO:
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fibu NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acc1 THEN
    DO:
      msg-str = msg-str + CHR(2)
              + translateExtended ("No such G/L Account number.",lvCAREA,"").
      /*MTAPPLY "entry" TO fibu. */
      RETURN NO-APPLY.
    END.
    ELSE
    DO:
      create queasy.
      RUN fill-queasy.
      /*MTfibu = "0000000000".
      remark = "".
      RUN disp-queasy-list.
      RUN disp-it.*/
      /*MTAPPLY "entry" TO titel. */
      RUN disp-it.
      RETURN NO-APPLY.
    END.
END.
ELSE IF case-type = 2 THEN       /* chg */
DO: 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fibu NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acc1 THEN 
    DO: 
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("No such G/L Account number.",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      /*MTAPPLY "entry" TO fibu. */
      RETURN NO-APPLY. 
    END. 
    ELSE 
    DO:
      FIND FIRST queasy WHERE RECID(queasy) = rec-id EXCLUSIVE-LOCK.
      IF AVAILABLE queasy THEN
      RUN fill-queasy. 
      /*MTRUN init-queasy-list. */
      FIND CURRENT queasy NO-LOCK. 
      /*MTDISABLE titel fibu remark WITH FRAME frame1. 
      ENABLE b1 btn-addname btn-chgname btn-delname WITH FRAME frame1. */
      /*MTRUN disp-it. 
      curr-mode = "". 
      APPLY "entry" TO b1. */
      RUN disp-it.
      RETURN NO-APPLY. 
    END. 
END.


PROCEDURE fill-queasy: 
  ASSIGN 
    queasy.key = 106 
    queasy.char1 = titel 
    queasy.char2 = remark 
    queasy.char3 = fibu. 
END. 


PROCEDURE disp-it:
  FIND CURRENT queasy.
  IF AVAILABLE queasy THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = queasy.char3 .
    CREATE b1-list.
    BUFFER-COPY queasy TO b1-list.
    b1-list.rec-id = RECID(queasy).
    ASSIGN
      b1-list.fibukonto = gl-acct.fibukonto
      b1-list.bezeich   = gl-acct.bezeich.
  END.
END. 











/*MT
DEF INPUT  PARAMETER curr-mode   AS CHAR.
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER titel       AS CHAR.
DEF INPUT  PARAMETER remark      AS CHAR.
DEF INPUT  PARAMETER fibu        AS CHAR.
DEF OUTPUT PARAMETER msg-str     AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "main-gc".

DEFINE buffer gl-acc1 FOR gl-acct. 

IF curr-mode = "add" THEN 
DO: 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fibu NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acc1 THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("No such G/L Account number.",lvCAREA,"").
      /*MTAPPLY "entry" TO fibu. */
      RETURN NO-APPLY. 
    END. 
    ELSE 
    DO: 
      create queasy. 
      RUN fill-queasy. 
      fibu = "0000000000". 
      /*MTremark = "". 
      RUN disp-queasy-list. 
      RUN disp-it. 
      APPLY "entry" TO titel. */
      RETURN NO-APPLY. 
    END. 
END. 
ELSE IF curr-mode = "chg" THEN 
DO: 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fibu NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acc1 THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("No such G/L Account number.",lvCAREA,"").
      /*MTAPPLY "entry" TO fibu. */
      RETURN NO-APPLY. 
    END. 
    ELSE 
    DO: 
      FIND FIRST queasy WHERE queasy.KEY = 106 AND queasy.char1 = titel
          AND queasy.char2 = remark AND queasy.char3 = fibu EXCLUSIVE-LOCK. 
      RUN fill-queasy. 
      /*RUN init-queasy-list. */
      FIND CURRENT queasy NO-LOCK. 
      /*MTDISABLE titel fibu remark WITH FRAME frame1. 
      ENABLE b1 btn-addname btn-chgname btn-delname WITH FRAME frame1. 
      RUN disp-it. 
      curr-mode = "". 
      APPLY "entry" TO b1. */
      RETURN NO-APPLY. 
    END. 
END. 

PROCEDURE fill-queasy: 
  ASSIGN 
    queasy.key = 106 
    queasy.char1 = titel 
    queasy.char2 = remark 
    queasy.char3 = fibu. 
END. 

*/

