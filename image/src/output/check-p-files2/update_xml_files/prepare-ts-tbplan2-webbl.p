DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD bcol AS INT INITIAL 10
    FIELD fcol AS INT INITIAL 0
    FIELD rec-id AS INT
    FIELD billprint-flag AS LOGICAL
    /* Dzikri 7F6983 - missing validation */
    /* Dzikri D3D452 - Req splitbill icon */
    FIELD splitbill-flag AS LOGICAL INIT NO
.
DEF TEMP-TABLE t-queasy33 LIKE queasy.
DEF TEMP-TABLE t-queasy31 LIKE queasy
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-tisch LIKE tisch.
DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-kellner LIKE kellner.
DEF TEMP-TABLE t-mc-guest LIKE mc-guest.
DEF TEMP-TABLE t-zimmer
    FIELD zinr LIKE zimmer.zinr.

DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER location       AS INT.
DEF INPUT  PARAMETER curr-waiter    AS INT.

DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER pos1           AS INT.
DEF OUTPUT PARAMETER pos2           AS INT.
DEF OUTPUT PARAMETER mc-flag        AS LOGICAL.
DEF OUTPUT PARAMETER mc-pos1        AS INT.
DEF OUTPUT PARAMETER mc-pos2        AS INT.
DEF OUTPUT PARAMETER vpos-flag      AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-tisch.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.
DEF OUTPUT PARAMETER TABLE FOR t-kellner.
DEF OUTPUT PARAMETER TABLE FOR t-mc-guest.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.
DEF OUTPUT PARAMETER TABLE FOR t-queasy31.
DEF OUTPUT PARAMETER TABLE FOR t-queasy33.

DEF VAR s     AS CHAR FORMAT "x(4)" EXTENT 100.
DEF VAR curr-n AS INT.

/* Dzikri 7F6983 - missing validation */
DEFINE VARIABLE split-count AS INTEGER. /* Dzikri D3D452 - Req splitbill icon */

DEFINE BUFFER hbill-buf FOR h-bill.

FIND FIRST vhp.htparam WHERE paramnr = 87 NO-LOCK.
ci-date = vhp.htparam.fdate.

FIND FIRST vhp.htparam WHERE paramnr = 337 NO-LOCK.
pos1 = vhp.htparam.finteger.
IF pos1 = 0 THEN pos1 = 1.

FIND FIRST vhp.htparam WHERE paramnr = 338 NO-LOCK.
pos2 = vhp.htparam.finteger.

RUN initiate-it.


FIND FIRST vhp.htparam WHERE paramnr = 336 NO-LOCK.
IF vhp.htparam.feldtyp = 4 THEN 
DO:
  mc-flag = vhp.htparam.flogical.
  FIND FIRST vhp.htparam WHERE paramnr = 337 NO-LOCK.
  mc-pos1 = vhp.htparam.finteger.
  FIND FIRST vhp.htparam WHERE paramnr = 338 NO-LOCK.
  mc-pos2 = vhp.htparam.finteger.
END. 

FIND FIRST vhp.kellner WHERE kellner.kellner-nr = curr-waiter 
  AND kellner.departement = dept NO-LOCK NO-ERROR.
IF AVAILABLE kellner THEN
DO:
    CREATE t-kellner.
    BUFFER-COPY kellner TO t-kellner.
END.

FIND FIRST vhp.htparam WHERE paramnr = 975 no-lock.   /* VHP Front multi user */ 
vpos-flag = (vhp.htparam.finteger EQ 1). 

FOR EACH vhp.tisch WHERE vhp.tisch.departement = dept AND vhp.tisch.betriebsnr EQ location NO-LOCK:
    CREATE t-tisch.
    BUFFER-COPY tisch TO t-tisch.
END.

FOR EACH h-bill WHERE h-bill.departement = dept AND h-bill.flag = 0 NO-LOCK:
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END.

/* Dzikri 5419D3 - membership data create agent running, not used yet in vhpcloud
FOR EACH mc-guest WHERE mc-guest.activeflag = YES NO-LOCK:
    CREATE t-mc-guest.
    BUFFER-COPY mc-guest TO t-mc-guest.
END.
*/

FOR EACH zimmer NO-LOCK:
    CREATE t-zimmer.
    ASSIGN t-zimmer.zinr = zimmer.zinr.
END.

FOR EACH queasy WHERE queasy.KEY = 33 AND queasy.number1 = dept
    AND queasy.date1 = ci-date AND queasy.logi3 = YES NO-LOCK:
    CREATE t-queasy33.
    BUFFER-COPY queasy TO t-queasy33.
END.

FOR EACH vhp.queasy WHERE vhp.queasy.key = 31 AND vhp.queasy.number1 = dept
    AND vhp.queasy.betriebsnr = 0 AND vhp.queasy.deci3 EQ location NO-LOCK BY vhp.queasy.number2:
    curr-n = curr-n + 1.
    CREATE t-queasy31.
    BUFFER-COPY queasy TO t-queasy31.
    ASSIGN t-queasy31.rec-id = RECID(queasy).
END.

PROCEDURE initiate-it:
DEF VAR do-it  AS LOGICAL NO-UNDO.
DEF VAR i AS INT.

  curr-n = 0. 
  DO i = 1 TO 100: 
      s[i] = "". 
  END. 

  FOR EACH vhp.queasy WHERE vhp.queasy.key = 31 AND vhp.queasy.number1 = dept
      AND vhp.queasy.betriebsnr = 0 AND vhp.queasy.deci3 EQ location NO-LOCK BY vhp.queasy.number2:
      FIND FIRST vhp.tisch WHERE vhp.tisch.departement = vhp.queasy.number1
        AND vhp.tisch.betriebsnr EQ vhp.queasy.deci3
        AND vhp.tisch.tischnr = vhp.queasy.number2 NO-LOCK NO-ERROR.
      do-it  = AVAILABLE vhp.tisch.
      IF do-it THEN
      DO:
          curr-n = curr-n + 1.
          CREATE t-queasy.
          BUFFER-COPY queasy TO t-queasy.
          RUN assign-color(curr-n).
          ASSIGN t-queasy.rec-id = RECID(queasy).

          /*FDL Feb 12, 2024 => Ticket 00D7D2 | 752E56*/
          FIND FIRST hbill-buf WHERE hbill-buf.tischnr EQ tisch.tischnr
              AND hbill-buf.departement EQ tisch.departement
              AND hbill-buf.flag EQ 0 NO-LOCK NO-ERROR.
          IF AVAILABLE hbill-buf THEN
          DO:
              t-queasy.billprint-flag = LOGICAL(hbill-buf.rgdruck).
              /* Dzikri 7F6983 - missing validation */
              /* Dzikri D3D452 - split bill flag */
              split-count = 0.
              FOR EACH h-bill-line WHERE h-bill-line.rechnr = hbill-buf.rechnr
                  AND h-bill-line.departement = hbill-buf.departement
                  and h-bill-line.waehrungsnr NE 0 NO-LOCK:
                  split-count = split-count + 1.
                  IF split-count GE 1 THEN 
                  DO:
                    t-queasy.splitbill-flag = YES.
                    LEAVE.
                  END.
              END.
          END.
      END.
  END.
END.

PROCEDURE assign-color:
DEF INPUT PARAMETER i AS INTEGER.
DEF VAR bcol  AS INTEGER INITIAL 10.
DEF VAR fcol  AS INTEGER INITIAL 0.
DEF VAR zeit  AS INTEGER INITIAL 0.
DEF VAR hh1   AS CHAR  NO-UNDO.
DEF VAR hh2   AS CHAR  NO-UNDO.
DEF VAR hh3   AS CHAR  NO-UNDO.
DEF BUFFER qsy FOR vhp.queasy.

  IF vhp.queasy.date1 NE ? THEN 
  DO:
    zeit = (TODAY - vhp.queasy.date1) * 86400 + TIME - vhp.queasy.number3.
    IF zeit GT 0 AND zeit LE 1800 THEN ASSIGN t-queasy.bcol = 14.
    ELSE IF zeit GT 1800 AND zeit LE 3600 THEN ASSIGN 
      t-queasy.bcol = 4
      t-queasy.fcol = 15.
    ELSE IF zeit GT 3600 THEN ASSIGN
      t-queasy.bcol = 12
      t-queasy.fcol = 15.
  END.
  ELSE
  DO:
    hh1 = STRING(TIME,"HH:MM").
    hh1 = SUBSTR(hh1,1,2) + SUBSTR(hh1,4,2).
    hh2 = STRING(INTEGER(SUBSTR(hh1,1,2)) + 2, "99") + SUBSTR(hh1,3,2).
    hh3 = STRING(TIME - 1800,"HH:MM").
    hh3 = SUBSTR(hh3,1,2) + SUBSTR(hh3,4,2).
   
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = dept
       AND qsy.number2 = vhp.queasy.number2 AND qsy.date1 = ci-date
       AND qsy.logi3 = YES 
       AND hh1 LE qsy.char1 AND hh2 GE qsy.char1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE qsy THEN
    FIND FIRST qsy WHERE qsy.KEY = 33 AND qsy.number1 = dept
       AND qsy.number2 = vhp.queasy.number2 AND qsy.date1 = ci-date
       AND qsy.logi3 = YES 
       AND hh1 GE qsy.char1 AND hh3 LE qsy.char1 NO-LOCK NO-ERROR.
     IF AVAILABLE qsy THEN ASSIGN
         t-queasy.bcol = 1
         t-queasy.fcol = 15.
  END.

  IF t-queasy.bcol = 12 THEN
  DO:
      FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = INTEGER(s[i])
        AND vhp.h-bill.departement = dept
        AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE vhp.h-bill THEN
      FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
        AND vhp.h-bill-line.departement = dept NO-LOCK
        BY vhp.h-bill-line.sysdate DESCENDING BY vhp.h-bill-line.zeit DESC:
        zeit = (TODAY - vhp.h-bill-line.sysdate) * 86400 
             + TIME - vhp.h-bill-line.zeit.
        IF zeit GE 30 * 60 THEN t-queasy.bcol = 0.
        ELSE IF zeit GE 15 * 60 THEN t-queasy.bcol = 7.
        LEAVE.
      END.
  END.

END.
