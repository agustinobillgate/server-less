
DEF INPUT PARAMETER resnr       AS INTEGER.
DEF INPUT PARAMETER reslinnr    AS INTEGER.
DEF INPUT PARAMETER rmcat       AS CHAR.
DEF INPUT PARAMETER ses-param   AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER zinr        AS CHAR.
DEF OUTPUT PARAMETER msg-str    AS CHAR.

DEF VAR ci-date AS DATE NO-UNDO. 

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.


RUN enter-room.

PROCEDURE enter-room: 
  DO TRANSACTION: 
    FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.reslinnr = reslinnr 
    AND res-line.zinr = "" AND res-line.active-flag = 0 EXCLUSIVE-LOCK. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK.

    IF zimkateg.kurzbez NE rmcat THEN RUN min-resplan. 
    RUN update-resline. 
    RUN assign-zinr.
    RUN res-changes.   /* create log file IF any res-line changes */ 
    IF zimkateg.kurzbez NE rmcat THEN RUN add-resplan. 
 
    /*IF res-line.betrieb-gast GT 0 THEN 
    DO: 
      IF ses-param MATCHES "*coder=*" THEN RUN add-keycard. 
      ELSE 
      DO: 
        /*HIDE MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Replace the KeyCard / Qty =", lvCAREA, "":U) 
          + " " + STRING(res-line.betrieb-gast) VIEW-AS ALERT-BOX WARNING. */
          msg-str = ("Replace the KeyCard / Qty =") + " " + STRING(res-line.betrieb-gast).
      END. 
    END. */
  END. 
END PROCEDURE. 
 

PROCEDURE update-resline:  
  FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK. 
  ASSIGN 
    res-line.zikatnr      = zimmer.zikatnr 
    res-line.zinr         = zimmer.zinr 
    res-line.setup        = zimmer.setup 
    res-line.reserve-char = STRING(TODAY) + STRING(TIME,"HH:MM") + user-init 
    res-line.changed      = ci-date 
    res-line.changed-id   = user-init. 
 
  FIND CURRENT res-line NO-LOCK. 
 
END. 

PROCEDURE min-resplan:
DEFINE VARIABLE curr-date AS DATE.
  curr-date = res-line.ankunft.
  DO WHILE curr-date GE res-line.ankunft AND curr-date LT res-line.abreise:
    FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr
      AND resplan.datum = curr-date NO-LOCK NO-ERROR.
    IF AVAILABLE resplan THEN 
    DO:
      FIND CURRENT resplan EXCLUSIVE-LOCK.
      resplan.anzzim[res-line.resstatus] = resplan.anzzim[res-line.resstatus] 
        - res-line.zimmeranz.
      FIND CURRENT resplan NO-LOCK.
      RELEASE resplan.
    END.
    curr-date = curr-date + 1.
  END.
END.

PROCEDURE add-resplan:
DEFINE VARIABLE curr-date   AS DATE.
DEFINE BUFFER zbuff         FOR zimkateg.

  FIND FIRST zbuff WHERE zbuff.kurzbez = rmcat NO-LOCK.
  curr-date = res-line.ankunft.
  DO WHILE curr-date GE res-line.ankunft AND curr-date LT res-line.abreise:
    FIND FIRST resplan WHERE resplan.zikatnr = zbuff.zikatnr
      AND resplan.datum = curr-date NO-LOCK NO-ERROR.
    IF AVAILABLE resplan THEN 
    DO:
      FIND CURRENT resplan EXCLUSIVE-LOCK.
      resplan.anzzim[res-line.resstatus] = resplan.anzzim[res-line.resstatus] 
        + res-line.zimmeranz.
      FIND CURRENT resplan NO-LOCK.
      RELEASE resplan.
    END.
    curr-date = curr-date + 1.
  END.
END.

PROCEDURE assign-zinr:
DEF VAR curr-datum      AS DATE.
  IF zinr NE "" AND NOT (res-line.resstatus = 11) THEN
  DO:
    DO curr-datum = res-line.ankunft TO (res-line.abreise - 1): 
      FIND FIRST zimplan WHERE zimplan.datum = curr-datum
        AND zimplan.zinr = zinr NO-LOCK NO-ERROR.
      IF (NOT AVAILABLE zimplan) THEN 
      DO:
        CREATE zimplan.
        ASSIGN
          zimplan.datum = curr-datum
          zimplan.zinr = zinr
          zimplan.res-recid = RECID(res-line)
          zimplan.gastnrmember = res-line.gastnrmember
          zimplan.bemerk = res-line.bemerk
          zimplan.resstatus = res-line.resstatus
          zimplan.name = res-line.name
        .
        FIND CURRENT zimplan NO-LOCK.
        RELEASE zimplan.
      END.
    END.
  END.
END.

PROCEDURE res-changes: 
DEFINE VARIABLE do-it AS LOGICAL INITIAL NO. 
DEFINE VARIABLE cid AS CHAR FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ". 
DEFINE BUFFER guest1 FOR guest. 

  IF TRIM(res-line.changed-id) NE "" THEN 
  DO: 
    cid = res-line.changed-id. 
    cdate = STRING(res-line.changed). 
  END. 
  ELSE IF LENGTH(res-line.reserve-char) GE 14 THEN    /* created BY */ 
  cid = SUBSTR(res-line.reserve-char,14). 
 
  CREATE reslin-queasy. 
  ASSIGN 
    reslin-queasy.key = "ResChanges" 
    reslin-queasy.resnr = resnr 
    reslin-queasy.reslinnr = reslinnr 
    reslin-queasy.date2 = TODAY
    reslin-queasy.number2 = TIME
  . 
  reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
                        + STRING(res-line.ankunft) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(zimkateg.zikatnr) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + " " + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(cid) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(cdate, "x(8)") + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(res-line.NAME) + ";" 
                        + STRING(res-line.NAME) + ";". 
  IF res-line.was-status = 0 THEN 
    reslin-queasy.char3 = reslin-queasy.char3 + STRING(" NO") + ";" 
                        + STRING(" NO") + ";". 
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";" 
                        + STRING("YES") + ";".
 
  FIND CURRENT reslin-queasy NO-LOCK.
  RELEASE reslin-queasy. 
 
END. 

