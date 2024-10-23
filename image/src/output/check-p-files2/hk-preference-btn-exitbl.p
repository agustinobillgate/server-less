DEFINE TEMP-TABLE t-queasy      LIKE queasy.

DEF INPUT PARAMETER i-zeit      AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER zinr        AS CHAR       NO-UNDO.
DEF INPUT PARAMETER reason      AS CHAR       NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR       NO-UNDO.
DEF INPUT PARAMETER answer      AS LOGICAL    NO-UNDO.
DEF INPUT PARAMETER fr-date     AS DATE       NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FIND FIRST res-line WHERE res-line.active-flag = 1 
  AND res-line.resstatus = 6 AND res-line.zinr = zinr 
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE res-line THEN 
FIND FIRST res-line WHERE res-line.active-flag = 1 
  AND res-line.resstatus = 13 AND res-line.zinr = zinr 
  AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 

IF NOT AVAILABLE res-line THEN RETURN.

CREATE queasy. 
ASSIGN 
    queasy.key = 24 
    queasy.date1 = fr-date 
    queasy.char1 = zinr 
    queasy.number1 = i-zeit
    queasy.number2 = res-line.gastnrmember
    queasy.char2 = user-init 
    queasy.char3 = reason. 
  FIND CURRENT queasy NO-LOCK. 

CREATE t-queasy.
BUFFER-COPY queasy TO t-queasy
ASSIGN t-queasy.number3 = INTEGER(RECID(queasy)).

IF answer THEN
DO:
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr
    NO-LOCK.
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.
  FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
      NO-LOCK.
  CREATE history.
  ASSIGN
    history.gastnr      = res-line.gastnrmember
    history.ankunft     = res-line.ankunft
    history.abreise     = res-line.abreise 
    history.zimmeranz   = res-line.zimmeranz 
    history.zikateg     = zimkateg.kurzbez
    history.zinr        = zinr
    history.erwachs     = res-line.erwachs
    history.gratis      = res-line.gratis
    history.zipreis     = res-line.zipreis 
    history.arrangement = res-line.arrangement
    history.abreisezeit = STRING(TIME, "HH:MM")
    history.gastinfo    = res-line.name + " - " 
                        + guest.adresse1 + ", " + guest.wohnort
    history.segmentcode = reservation.segmentcode 
    history.zi-wechsel  = NO
    history.resnr       = res-line.resnr 
    history.reslinnr    = res-line.reslinnr
    history.betriebsnr = INTEGER(res-line.pseudofix)
  .
  ASSIGN history.bemerk = "HK-Preference"
       + ":= " /*MT+ TRIM(ENTRY(2, zinr, ";")).*/
       + TRIM(zinr).
  FIND CURRENT history NO-LOCK.
END.
