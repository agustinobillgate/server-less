DEF TEMP-TABLE t-queasy33 LIKE queasy
    FIELD rec-id AS INT.

DEF TEMP-TABLE table-list
    FIELD tischnr  LIKE tisch.tischnr  FORMAT ">>>9"  COLUMN-LABEL "Table"
    FIELD belegung LIKE tisch.normalbeleg FORMAT ">9" COLUMN-LABEL " Pax"
    FIELD uhrzeit  AS CHAR EXTENT 32 FORMAT "x(32)"
    FIELD s-recid  AS INTEGER EXTENT 32
    FIELD bcol     AS INT
    FIELD fcol     AS INT.
.

DEF INPUT  PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER d-param87 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR table-list.
DEF OUTPUT PARAMETER TABLE FOR t-queasy33.

DEF BUFFER buf-queasy FOR queasy.
DEF VAR curr-date AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
d-param87 = htparam.fdate.
curr-date = d-param87.

RUN create-list.

FOR EACH queasy WHERE queasy.KEY = 33 AND queasy.number1 = curr-dept 
    AND queasy.date1 = curr-date AND queasy.logi2 = NO 
    AND queasy.logi3 = YES AND queasy.betriebsnr = 0 NO-LOCK: /*FD add queasy.betriebsnr = 0 (Active)*/
    CREATE t-queasy33.
    BUFFER-COPY queasy TO t-queasy33.
    ASSIGN t-queasy33.rec-id = RECID(queasy).
END.

PROCEDURE create-list:
  /* FDL Comment Dec 08, 2022
  FOR EACH queasy WHERE queasy.KEY = 31 AND queasy.number1 = curr-dept
      AND queasy.betriebsnr = 0 NO-LOCK BY queasy.number2:
      FIND FIRST tisch WHERE tisch.departement = curr-dept
          AND tisch.tischnr = queasy.number2 NO-LOCK NO-ERROR.
      CREATE table-list.
      ASSIGN table-list.tischnr = queasy.number2.
      IF AVAILABLE tisch THEN
      DO:
          table-list.belegung = tisch.normalbeleg.
          RUN row-disp.
      END.
  END.
  */
  /*FDL Dec 08, 2022 => Feature Deposit Resto*/
  FOR EACH tisch WHERE tisch.departement EQ curr-dept NO-LOCK BY tisch.tischnr:
    CREATE table-list.
    ASSIGN 
        table-list.tischnr = tisch.tischnr
        table-list.belegung = tisch.normalbeleg
        .
    RUN row-disp.
  END.
END.

PROCEDURE row-disp:
  DEF VAR bcol AS INTEGER INITIAL 12  NO-UNDO.
  DEF VAR fcol AS INTEGER INITIAL 15  NO-UNDO.
  DEF VAR zeit AS INTEGER NO-UNDO.

  /* FDL Comment Dec 08, 2022
  FIND FIRST tisch WHERE tisch.departement = curr-dept
        AND tisch.tischnr = queasy.number2 NO-LOCK.
  */
  FIND FIRST h-bill WHERE h-bill.departement = curr-dept
    AND h-bill.tischnr = tisch.tischnr 
    AND h-bill.flag = 0 NO-LOCK NO-ERROR.
  IF AVAILABLE h-bill THEN
  DO:
    FIND FIRST buf-queasy WHERE buf-queasy.KEY = 31
      AND buf-queasy.number1 = curr-dept 
      AND buf-queasy.number2 = tisch.tischnr 
      AND buf-queasy.betriebsnr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE buf-queasy THEN
    DO:
      zeit = (TODAY - buf-queasy.date1) * 86400 + TIME - buf-queasy.number3.
      IF zeit GT 0 AND zeit LE 1800 THEN ASSIGN 
         bcol = 14
         fcol = 0.
      ELSE IF zeit GT 1800 AND zeit LE 3600 THEN ASSIGN bcol = 4.
      ELSE IF zeit GT 3600 THEN ASSIGN bcol = 12.
    END.

    ASSIGN 
      table-list.bcol = bcol
      table-list.fcol = fcol.
  END.
  ELSE DO:
    ASSIGN bcol = 0
           fcol = 15.
    ASSIGN 
      table-list.bcol = bcol
      table-list.fcol = fcol.
  END.

END.
