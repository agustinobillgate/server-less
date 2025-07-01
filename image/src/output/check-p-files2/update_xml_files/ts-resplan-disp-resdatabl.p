
DEF TEMP-TABLE t-queasy33 LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER case-type AS INT.
DEF INPUT  PARAMETER von-tisch AS INT.

DEF INPUT  PARAMETER curr-dept AS INT.
DEF INPUT  PARAMETER curr-date AS DATE.

DEF OUTPUT PARAMETER pax       AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-queasy33.

IF case-type = 1 THEN
DO :
    FIND FIRST tisch WHERE tisch.tischnr = von-tisch NO-LOCK.
    pax         = tisch.normalbeleg.
END.
ELSE IF case-type = 2 THEN
DO:
  FOR EACH queasy WHERE queasy.KEY = 33 AND queasy.number1 = curr-dept 
      AND queasy.date1 = curr-date AND queasy.logi2 = NO 
      AND queasy.logi3 = YES AND queasy.betriebsnr = 0 NO-LOCK: /*FD add queasy.betriebsnr = 0*/
      CREATE t-queasy33.
      BUFFER-COPY queasy TO t-queasy33.
      ASSIGN t-queasy33.rec-id = RECID(queasy).
  END.
END.
