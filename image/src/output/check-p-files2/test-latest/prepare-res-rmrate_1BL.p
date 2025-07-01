
DEFINE TEMP-TABLE dynaRate-list
  FIELD rCode   AS CHAR    FORMAT "x(10)" LABEL "RateCode"
  FIELD fr-room AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1   AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2   AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD s-recid AS INTEGER
  FIELD rmType  AS CHAR    FORMAT "x(10)" LABEL "Room Type"
.

DEF TEMP-TABLE ratecode-list
    FIELD rcode-str AS CHAR
.

DEF TEMP-TABLE output-list
    FIELD foreign-rate       AS LOGICAL
    FIELD double-currency    AS LOGICAL
    FIELD curr-foreign       AS CHAR
    FIELD local-nr           AS INTEGER
    FIELD msg-str            AS CHAR
    FIELD foreign-nr         AS INTEGER
    FIELD max-rate           AS DECIMAL
    FIELD long-digit         AS LOGICAL
    FIELD selected           AS LOGICAL
    FIELD contcode           AS CHAR
    FIELD currency-add-first AS CHAR
    FIELD zimmer-wunsch      AS CHAR
    FIELD btn-chgart         AS LOGICAL INIT NO
    FIELD fact1              AS DECIMAL
    FIELD betriebsnr         AS INT
    FIELD zipreis            AS DECIMAL
    FIELD adrflag            AS LOGICAL
    FIELD recid-resline      AS INTEGER.

DEF TEMP-TABLE t-waehrung
    FIELD wabkurz LIKE waehrung.wabkurz
    FIELD bezeich LIKE waehrung.bezeich
    FIELD betriebsnr LIKE waehrung.betriebsnr
    FIELD waehrungsnr LIKE waehrung.waehrungsnr
    FIELD exrate AS DECIMAL.

DEF TEMP-TABLE q2-reslin-queasy
    FIELD date1   LIKE reslin-queasy.date1
    FIELD date2   LIKE reslin-queasy.date2
    FIELD deci1   LIKE reslin-queasy.deci1
    FIELD char1   LIKE reslin-queasy.char1
    FIELD number3 LIKE reslin-queasy.number3
    FIELD char2   LIKE reslin-queasy.char2
    FIELD char3   LIKE reslin-queasy.char3
    FIELD recid-reslin  AS INT.

DEFINE TEMP-TABLE curr-add-last
    FIELD bezeich AS CHAR.

DEFINE TEMP-TABLE p-list 
  FIELD betrag  LIKE res-line.zipreis COLUMN-LABEL "Room Rate" 
  FIELD date1   AS DATE LABEL "From" 
  FIELD date2   AS DATE LABEL "To" 
  FIELD argt    AS CHAR FORMAT "x(8) " LABEL "ArgCode" 
  FIELD pax     AS INTEGER FORMAT ">>" LABEL "Adult"
  FIELD rcode   AS CHAR FORMAT "x(8)"  LABEL "RateCode"
.

DEFINE TEMP-TABLE reslin-list LIKE res-line. 

DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF INPUT  PARAMETER TABLE FOR reslin-list.
DEF OUTPUT PARAMETER rate-found  AS LOGICAL INITIAL NO NO-UNDO.
DEF OUTPUT PARAMETER ci-date     AS DATE               NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR p-list.
DEF OUTPUT PARAMETER TABLE FOR curr-add-last.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.
DEF OUTPUT PARAMETER TABLE FOR q2-reslin-queasy.
DEF OUTPUT PARAMETER TABLE FOR ratecode-list.
DEF OUTPUT PARAMETER rate-flag AS LOGICAL NO-UNDO.

/*MT
DEF VAR pvILanguage        AS INTEGER NO-UNDO INIT 1.
DEF VAR resnr              AS INTEGER INIT 21.
DEF VAR reslinnr           AS INTEGER INIT 1.
DEF VAR arrival     AS DATE INIT 11/05/08.
DEF VAR departure   AS DATE INIT 11/17/08.
DEF VAR inp-argt           AS CHAR INIT "RB".
DEF VAR user-init          AS CHAR INIT "01".
DEF VAR foreign-rate       AS LOGICAL.
DEF VAR double-currency    AS LOGICAL.
DEF VAR curr-foreign       AS CHAR.
DEF VAR local-nr           AS INTEGER.
DEF VAR msg-str            AS CHAR.
DEF VAR foreign-nr         AS INTEGER.
DEF VAR max-rate           AS DECIMAL.
DEF VAR long-digit         AS LOGICAL.
DEF VAR selected           AS LOGICAL.
DEF VAR contcode           AS CHAR.
DEF VAR currency-add-first AS CHAR.
DEF VAR zimmer-wunsch      AS CHAR.
DEF VAR btn-chgart         AS LOGICAL INIT NO.
DEF VAR fact1              AS DECIMAL.
*/

DEFINE VARIABLE price-decimal AS INTEGER.
DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1.
DEFINE VARIABLE ct                  AS CHAR.
DEFINE VARIABLE curr-wabnr          AS INTEGER. 
DEFINE BUFFER waehrung2 FOR waehrung.
DEFINE BUFFER waehrung1 FOR waehrung. 

/*ITA 120816*/
DEFINE VARIABLE datum           AS DATE NO-UNDO.
DEFINE VARIABLE bill-date       AS DATE NO-UNDO.
DEFINE VARIABLE co-date         AS DATE NO-UNDO.

DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE VARIABLE rm-rate         AS DECIMAL              NO-UNDO. 

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "prepare-res-rmrate".

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ASSIGN ci-date = htparam.fdate.

FIND FIRST reslin-list.
FOR EACH waehrung:
    CREATE t-waehrung.
    ASSIGN
    t-waehrung.wabkurz     = waehrung.wabkurz
    t-waehrung.bezeich     = waehrung.bezeich
    t-waehrung.betriebsnr  = waehrung.betriebsnr
    t-waehrung.waehrungsnr = waehrung.waehrungsnr
    t-waehrung.exrate      = waehrung.ankauf / waehrung.einheit.
END.

CREATE output-list.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST arrangement WHERE arrangement.arrangement = reslin-list.arrangement
   NO-LOCK.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK.
ASSIGN price-decimal = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK.
ASSIGN output-list.foreign-rate = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 240 NO-LOCK.
ASSIGN output-list.double-currency = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 144 NO-LOCK.
ASSIGN output-list.curr-foreign = fchar.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK.
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
IF NOT AVAILABLE waehrung THEN
DO:
  output-list.msg-str = output-list.msg-str + CHR(2)
          + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7).",lvCAREA,"").
  RETURN.
END.
output-list.local-nr = waehrung.waehrungsnr.

IF output-list.foreign-rate THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE waehrung THEN 
  DO: 
    output-list.msg-str = output-list.msg-str + CHR(2)
            + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7).",lvCAREA,"").
    RETURN.
  END.
  output-list.foreign-nr = waehrung.waehrungsnr.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1108 NO-LOCK. 
IF htparam.feldtyp = 1 THEN 
DO TRANSACTION: 
    FIND CURRENT htparam EXCLUSIVE-LOCK. 
    ASSIGN
      htparam.feldtyp  = 2 
      htparam.fdecimal = htparam.finteger
      htparam.finteger = 0
    . 
    FIND CURRENT htparam NO-LOCK. 
END. 
output-list.max-rate = htparam.fdecimal.

FIND FIRST htparam WHERE paramnr = 494 NO-LOCK NO-ERROR.
ASSIGN rate-flag = htparam.flogical.

FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr
    AND res-line.reslinnr = reslin-list.reslinnr NO-LOCK.
ASSIGN
  output-list.betriebsnr = reslin-list.betriebsnr
  output-list.zipreis = reslin-list.zipreis
  output-list.adrflag = reslin-list.adrflag
  output-list.recid-resline = RECID(res-line).

FIND FIRST guest WHERE guest.gastnr = reslin-list.gastnr NO-LOCK.
IF guest.notizen[3] NE "" THEN 
    FIND FIRST waehrung2 WHERE waehrung2.wabkurz = guest.notizen[3] NO-LOCK NO-ERROR.

FIND FIRST htparam WHERE htparam.paramnr = 246 NO-LOCK. 
output-list.long-digit = htparam.flogical. 

IF output-list.FOREIGN-RATE OR output-list.DOUBLE-CURRENCY THEN 
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK.
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.
END.


FIND FIRST guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest-pr THEN
DO:
  output-list.contcode = guest-pr.CODE.
  ct = reslin-list.zimmer-wunsch.
  IF ct MATCHES("*$CODE$*") THEN
  DO:
    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
    output-list.contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
  END.
END.

CREATE p-list.
IF AVAILABLE arrangement THEN 
DO: 
  output-list.selected = YES. 
  RUN fill-p-list.
END.

/*cek apakah ada ratecode atau tidak*/ 
/*ITA 120816*/
ASSIGN 
    ebdisc-flag = reslin-list.zimmer-wunsch MATCHES ("*ebdisc*")
    kbdisc-flag = reslin-list.zimmer-wunsch MATCHES ("*kbdisc*").

IF reslin-list.l-zuordnung[1] NE 0 THEN curr-zikatnr = reslin-list.l-zuordnung[1]. 
ELSE curr-zikatnr = reslin-list.zikatnr. 

co-date = reslin-list.abreise. 
IF co-date GT reslin-list.ankunft THEN co-date = co-date - 1. 
DO datum = reslin-list.ankunft TO co-date:
    bill-date = datum.
    FIND FIRST guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN DO:
        FIND FIRST vhp.queasy WHERE vhp.queasy.key = 18 AND vhp.queasy.number1 = reslin-list.reserve-int 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.queasy AND vhp.queasy.logi3 THEN bill-date = reslin-list.ankunft.
        RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, reslin-list.resnr, 
              reslin-list.reslinnr, vhp.guest-pr.CODE, ?, bill-date, reslin-list.ankunft,
              reslin-list.abreise, reslin-list.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, reslin-list.erwachs, reslin-list.kind1, reslin-list.kind2,
              reslin-list.reserve-dec, reslin-list.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).

        IF rate-found = YES THEN LEAVE.
    END.
END.
/*end*/

IF reslin-list.resstatus  = 8 THEN .
ELSE IF reslin-list.reserve-char NE "" AND SUBSTR(bediener.permission,43,1) LT "2" THEN
  output-list.btn-chgart = YES.
ELSE output-list.btn-chgart = NO.

FIND FIRST output-list.

IF reslin-list.betriebsnr NE 0 THEN 
DO:
  FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE reslin-list.betriebsnr
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
      RUN assign-it.
  END.
  FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = reslin-list.betriebsnr NO-LOCK. 
END.

ELSE IF AVAILABLE waehrung2 THEN
DO:
  curr-wabnr = waehrung2.waehrungsnr. 
  FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE curr-wabnr
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
      RUN assign-it.
  END. 
  FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = curr-wabnr NO-LOCK. 
END.
ELSE IF reslin-list.betriebsnr = 0 AND NOT reslin-list.adrflag THEN 
DO:
  DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
  IF AVAILABLE guest-pr THEN 
  DO: 
    IF reslin-list.reserve-int NE 0 THEN  /* market segment */ 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = 
        reslin-list.reserve-int NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") THEN 
      FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = output-list.contcode NO-LOCK NO-ERROR. 
    END. 
    ELSE FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
      = output-list.contcode NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
      IF queasy.key = 18 THEN FIND FIRST waehrung1 WHERE waehrung1.wabkurz 
        = queasy.char3 NO-LOCK NO-ERROR. 
      ELSE FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung1 THEN 
      DO: 
        found = YES. 
        curr-wabnr = waehrung1.waehrungsnr. 
        FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE curr-wabnr
            AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
            RUN assign-it.
        END. 
        FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = curr-wabnr NO-LOCK. 
      END. 
    END. 
  END. 
  IF NOT found THEN 
  DO: 
    IF output-list.foreign-rate THEN 
    DO: 
      FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE output-list.foreign-nr
          AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
          RUN assign-it.
      END. 
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = output-list.foreign-nr NO-LOCK. 
    END. 
    ELSE 
    DO: 
      FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE output-list.local-nr
          AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
          RUN assign-it.
      END. 
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = output-list.local-nr NO-LOCK. 
    END. 
  END. 
END.
ELSE IF reslin-list.betriebsnr = 0 AND reslin-list.adrflag THEN 
DO:
  FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE output-list.local-nr
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
      RUN assign-it.
  END. 
  FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = output-list.local-nr NO-LOCK. 
END.

output-list.currency-add-first = waehrung1.bezeich.

RUN disp-query.
output-list.zimmer-wunsch = reslin-list.zimmer-wunsch.

DEFINE VARIABLE curr-time AS INTEGER.
curr-time = TIME.

FIND FIRST guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr NO-LOCK NO-ERROR.
DO WHILE AVAILABLE guest-pr:
    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = guest-pr.CODE
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        IF NOT queasy.logi2 THEN
        DO:
          FIND FIRST ratecode-list WHERE ratecode-list.rcode-str = guest-pr.CODE
              NO-ERROR.
          IF NOT AVAILABLE ratecode-list THEN
          DO:
            CREATE ratecode-list.
            ASSIGN ratecode-list.rcode-str = guest-pr.CODE.
          END.
        END.
        ELSE
        DO:
            FOR EACH dynaRate-list:
                DELETE dynaRate-list.
            END.
            RUN create-dynaRate-list.
        END.
    END.
    FIND NEXT guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr NO-LOCK NO-ERROR.
END.
curr-time = TIME - curr-time.

/*MESSAGE STRING(curr-time, "HH:MM:SS") VIEW-AS ALERT-BOX INFO.*/

/*FOR EACH guest-pr WHERE guest-pr.gastnr = reslin-list.gastnr NO-LOCK,
    FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = guest-pr.CODE
    NO-LOCK BY queasy.logi2 DESCENDING BY queasy.char1:
    IF NOT queasy.logi2 THEN
    DO:
      FIND FIRST ratecode-list WHERE ratecode-list.rcode-str = guest-pr.CODE
          NO-ERROR.
      IF NOT AVAILABLE ratecode-list THEN
      DO:
        CREATE ratecode-list.
        ASSIGN ratecode-list.rcode-str = guest-pr.CODE.
      END.
    END.
    ELSE
    DO:
        FOR EACH dynaRate-list:
            DELETE dynaRate-list.
        END.
    END.
    RUN create-dynaRate-list.
END.*/

PROCEDURE fill-p-list: 
  IF AVAILABLE reslin-queasy THEN 
  ASSIGN
    p-list.betrag = reslin-queasy.deci1
    p-list.date1  = reslin-queasy.date1 
    p-list.date2  = reslin-queasy.date2 
    p-list.argt   = reslin-queasy.char1 
    p-list.pax    = reslin-queasy.number3
    p-list.rcode  = reslin-queasy.char2
  . 
END.

PROCEDURE assign-it:
    CREATE curr-add-last.
    ASSIGN curr-add-last.bezeich = waehrung1.bezeich.
END.

PROCEDURE disp-query: 
/* 
  IF local-rate THEN fact1 = 0. 
  ELSE fact1 = exchg-rate. 
*/ 
  output-list.fact1 = waehrung1.ankauf / waehrung1.einheit. 
  FOR EACH reslin-queasy WHERE key = "arrangement"
      AND reslin-queasy.resnr = reslin-list.resnr
      AND reslin-queasy.reslinnr = reslin-list.reslinnr NO-LOCK
      BY reslin-queasy.date1:
      CREATE q2-reslin-queasy.
      ASSIGN
          q2-reslin-queasy.date1   = reslin-queasy.date1
          q2-reslin-queasy.date2   = reslin-queasy.date2
          q2-reslin-queasy.deci1   = reslin-queasy.deci1
          q2-reslin-queasy.char1   = reslin-queasy.char1
          q2-reslin-queasy.number3 = reslin-queasy.number3
          q2-reslin-queasy.char2   = reslin-queasy.char2
          q2-reslin-queasy.char3   = reslin-queasy.char3
          q2-reslin-queasy.recid-reslin = RECID(reslin-queasy).
  END.
END.

PROCEDURE create-dynaRate-list: 
DEF VAR i                   AS INTEGER           NO-UNDO.
DEF VAR tokcounter          AS INTEGER           NO-UNDO.
DEF VAR ifTask              AS CHAR              NO-UNDO.
DEF VAR mesToken            AS CHAR              NO-UNDO.
DEF VAR mesValue            AS CHAR              NO-UNDO.
DEF VAR occ-rooms           AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR use-it              AS LOGICAL           NO-UNDO.

  FOR EACH ratecode WHERE ratecode.code = guest-pr.code NO-LOCK: 
    CREATE dynaRate-list.
    ASSIGN dynaRate-list.s-recid = RECID(ratecode).
    ifTask = ratecode.char1[5].
    DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
      mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
      mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
      CASE mesToken:
          WHEN "RT" THEN dynaRate-list.rmType = mesValue.
          WHEN "FR" THEN dynaRate-list.fr-room = INTEGER(mesValue).
          WHEN "TR" THEN dynaRate-list.to-room = INTEGER(mesValue).
          WHEN "D1" THEN dynaRate-list.days1   = INTEGER(mesValue).
          WHEN "D2" THEN dynaRate-list.days2   = INTEGER(mesValue).
          WHEN "RC" THEN dynaRate-list.rCode   = mesValue.
      END CASE.
    END.
  END.
  FOR EACH dynaRate-list BY dynaRate-list.rcode:
      FIND FIRST ratecode-list WHERE 
          ratecode-list.rcode-str = dynaRate-list.rcode NO-ERROR.
      IF NOT AVAILABLE ratecode-list THEN
      DO:
        CREATE ratecode-list.
        ASSIGN ratecode-list.rcode-str = dynaRate-list.rcode.
      END.     
  END.
END.



