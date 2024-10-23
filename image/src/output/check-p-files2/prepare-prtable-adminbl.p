
DEFINE TEMP-TABLE margt-list   LIKE prmarket.
DEFINE TEMP-TABLE hargt-list   LIKE prmarket.
DEFINE TEMP-TABLE hrmcat-list  LIKE prmarket.
DEFINE TEMP-TABLE mrmcat-list  LIKE prmarket.
DEFINE TEMP-TABLE b1-list
    FIELD nr       LIKE prtable.nr
    FIELD marknr   LIKE prtable.marknr
    FIELD bezeich  LIKE prmarket.bezeich
    FIELD char3    LIKE queasy.char3
    FIELD logi3    LIKE queasy.logi3
    FIELD rec-id   AS INT
    FIELD pr-recid AS INT.
DEFINE TEMP-TABLE t-waehrung1 LIKE waehrung.
DEF TEMP-TABLE fill-t-waehrung
    FIELD wabkurz AS CHAR.


DEF TEMP-TABLE t-waehrung2 LIKE waehrung.
DEF TEMP-TABLE t-zimkateg  
    LIKE zimkateg.

DEF OUTPUT PARAMETER new-contrate   AS LOGICAL.
DEF OUTPUT PARAMETER f-char         AS CHAR.
DEF OUTPUT PARAMETER f-logical      AS LOGICAL.
DEF OUTPUT PARAMETER fill-wabkurz   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR b1-list.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung1.
DEF OUTPUT PARAMETER TABLE FOR fill-t-waehrung.
DEF OUTPUT PARAMETER TABLE FOR margt-list.
DEF OUTPUT PARAMETER TABLE FOR hargt-list.
DEF OUTPUT PARAMETER TABLE FOR hrmcat-list.
DEF OUTPUT PARAMETER TABLE FOR mrmcat-list.


FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST queasy WHERE queasy.key = 18 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE queasy THEN 
DO: 
  FOR EACH prmarket NO-LOCK: 
    create queasy. 
    ASSIGN 
      queasy.key = 18 
      queasy.number1 = prmarket.nr. 
  END. 
END. 


FOR EACH prtable WHERE prtable.prcode = "" NO-LOCK,
    FIRST prmarket WHERE prmarket.nr = prtable.marknr NO-LOCK,
    FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = prmarket.nr 
    NO-LOCK BY prtable.nr:
    CREATE b1-list.
    ASSIGN
      b1-list.nr = prtable.nr
      b1-list.marknr = prtable.marknr
      b1-list.bezeich = prmarket.bezeich
      b1-list.char3 = queasy.char3
      b1-list.logi3 = queasy.logi3
      b1-list.rec-id = RECID(prtable)
      b1-list.pr-recid = RECID(prmarket).
END.
FIND FIRST b1-list NO-ERROR.
RUN get-currency.
RUN fill-currency.


FIND FIRST prtable WHERE RECID(prtable) = b1-list.rec-id.
RUN check-array.

PROCEDURE get-currency: 
  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK.
  f-logical = htparam.flogical.
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK.
  f-char = htparam.fchar.
  FOR EACH waehrung:
      CREATE t-waehrung1.
      BUFFER-COPY waehrung TO t-waehrung1.
  END.
END.



PROCEDURE check-array: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE array AS INTEGER EXTENT 99. 
 
  FOR EACH hrmcat-list: 
    delete hrmcat-list. 
  END. 
  FOR EACH mrmcat-list: 
    delete mrmcat-list. 
  END. 
  DO i = 1 TO 99: 
    array[i] = prtable.zikatnr[i]. 
  END. 
  FOR EACH zimkateg: 
    create hrmcat-list. 
    hrmcat-list.nr = zimkateg.zikatnr. 
    hrmcat-list.bezeich = zimkateg.bezeich. 
  END. 
 
  DO i = 1 TO 99: 
    IF array[i] NE 0 THEN 
    DO: 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = array[i] NO-LOCK NO-ERROR. 
      IF AVAILABLE zimkateg THEN 
      DO: 
        create mrmcat-list. 
        mrmcat-list.nr = zimkateg.zikatnr. 
        mrmcat-list.bezeich = zimkateg.bezeich. 
      END. 
      FIND FIRST hrmcat-list WHERE hrmcat-list.nr = mrmcat-list.nr NO-ERROR. 
      IF AVAILABLE hrmcat-list THEN delete hrmcat-list. 
    END. 
  END. 
  
  FOR EACH hargt-list: 
    delete hargt-list. 
  END. 
  FOR EACH margt-list: 
    delete margt-list. 
  END.

  DO i = 1 TO 99: 
    array[i] = prtable.argtnr[i]. 
  END. 
  FOR EACH arrangement WHERE arrangement.segmentcode = 0 NO-LOCK: 
    create hargt-list. 
    hargt-list.nr = arrangement.argtnr. 
    hargt-list.bezeich = arrangement.argt-bez. 
  END. 
 
  DO i = 1 TO 99: 
    IF array[i] NE 0 THEN 
    DO:
      FIND FIRST arrangement WHERE arrangement.argtnr = array[i] 
         NO-LOCK NO-ERROR.
      /*MESSAGE arrangement.argtnr array[i]
          VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
      IF AVAILABLE arrangement THEN 
      DO: 
        create margt-list. 
        margt-list.nr = arrangement.argtnr. 
        margt-list.bezeich = arrangement.argt-bez. 
      END. 
      FIND FIRST hargt-list WHERE hargt-list.nr = margt-list.nr NO-ERROR. 
      IF AVAILABLE hargt-list THEN delete hargt-list. 
    END. 
  END.
END. 


PROCEDURE fill-currency: 
DEF VAR double-currency AS LOGICAL NO-UNDO.
  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. /* double-currency */ 
  IF htparam.flogical THEN
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN
        fill-wabkurz = waehrung.wabkurz.
    RETURN.
  END. 

  FOR EACH waehrung WHERE waehrung.betriebsnr = 0 
    AND waehrung.ankauf GT 0 NO-LOCK BY waehrung.wabkurz:
      CREATE fill-t-waehrung.
      ASSIGN 
          fill-t-waehrung.wabkurz = waehrung.wabkurz.
  END.

END. 
