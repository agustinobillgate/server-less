
DEFINE TEMP-TABLE str-list 
  FIELD billdate AS DATE 
  FIELD fibu AS CHAR 
  FIELD other-fibu AS LOGICAL 
  FIELD op-recid AS INTEGER 
  FIELD lscheinnr AS CHAR 
  FIELD s AS CHAR FORMAT "x(153)"
  FIELD ID AS CHAR FORMAT "x(4)". 

DEF INPUT-OUTPUT PARAMETER TABLE FOR str-list.
DEF INPUT  PARAMETER cost-acct AS CHAR.
DEF INPUT  PARAMETER op-recid  AS INT NO-UNDO.
DEF OUTPUT PARAMETER fl-code   AS INT INIT 0.
DEF OUTPUT PARAMETER t-fibu    AS CHAR.
DEF OUTPUT PARAMETER t-s       AS CHAR.

FIND FIRST str-list WHERE str-list.op-recid = op-recid.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct AND gl-acct.fibukonto NE str-list.fibu THEN 
DO transaction: 
  IF str-list.other-fibu THEN 
  DO: 
    FIND FIRST l-op WHERE RECID(l-op) = str-list.op-recid EXCLUSIVE-LOCK. 
    l-op.stornogrund = gl-acct.fibukonto. 
    FIND CURRENT l-op NO-LOCK. 
    t-fibu = cost-acct. 
    t-s = SUBSTR(str-list.s,1,8) + STRING(gl-acct.bezeich, "x(30)") 
      + SUBSTR(str-list.s, 39, length(str-list.s)). 
    fl-code = 1.
    /*MTb1:REFRESH().*/
  END. 
  ELSE 
  DO: 
    /*MTCLOSE QUERY q1.*/
    FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = str-list.lscheinnr 
      AND l-ophdr.op-typ = "STT" EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-ophdr THEN 
    DO: 
      FOR EACH str-list WHERE str-list.lscheinnr = l-ophdr.lscheinnr: 
        IF NOT str-list.other-fibu THEN str-list.s = SUBSTR(str-list.s,1,8) 
          + STRING(gl-acct.bezeich, "x(30)") 
          + SUBSTR(str-list.s, 39, length(str-list.s)). 
        str-list.fibu = cost-acct. 
        IF l-ophdr.betriebsnr NE 0 THEN 
        DO: 
          FIND FIRST l-op WHERE RECID(l-op) = str-list.op-recid 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE l-op THEN 
          RUN create-lartjob.p(RECID(l-ophdr), l-op.artnr, - l-op.anzahl, 
            - l-op.warenwert, l-op.datum, NO).
        END. 
      END. 
      l-ophdr.fibukonto = gl-acct.fibukonto. 

      IF l-ophdr.betriebsnr NE 0 THEN 
      DO: 
        FOR EACH str-list WHERE str-list.lscheinnr = l-ophdr.lscheinnr: 
          FIND FIRST l-op WHERE RECID(l-op) = str-list.op-recid 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE l-op THEN 
          RUN create-lartjob.p(RECID(l-ophdr), l-op.artnr, l-op.anzahl, 
            l-op.warenwert, l-op.datum, NO). 
        END. 
      END. 

      /*MTOPEN QUERY q1 FOR EACH str-list NO-LOCK.*/
      FIND CURRENT l-ophdr NO-LOCK. 
    END. 
  END. 
END. 
