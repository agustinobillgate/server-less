
DEFINE TEMP-TABLE t-res-line
    FIELD resnr     LIKE res-line.resnr
    FIELD reslinnr  LIKE res-line.reslinnr
    FIELD name      LIKE res-line.name
    FIELD zinr      LIKE res-line.zinr
    FIELD resstatus LIKE res-line.resstatus
    FIELD active-flag LIKE res-line.active-flag.

DEFINE TEMP-TABLE resline1
    FIELD resnr     LIKE res-line.resnr
    FIELD reslinnr  LIKE res-line.reslinnr
    FIELD resstatus LIKE res-line.resstatus.

/*MTDEFINE TEMP-TABLE res-list 
  FIELD zinr       AS CHAR FORMAT "x(4)" LABEL "RmNo" 
  FIELD name       AS CHAR FORMAT "x(36)" LABEL "Guest Name" 
  FIELD reslinnr   AS INTEGER 
  FIELD resstatus  AS INTEGER 
  FIELD sysdate    AS DATE 
  FIELD zeit       AS INTEGER.*/


DEF INPUT  PARAMETER resnr AS INTEGER. 
DEF INPUT  PARAMETER sorttype AS INT.
/*MTDEF OUTPUT PARAMETER TABLE FOR res-list.*/
DEF OUTPUT PARAMETER TABLE FOR t-res-line.
DEF OUTPUT PARAMETER TABLE FOR resline1.


RUN grp-co.

PROCEDURE grp-co: 
DEFINE VARIABLE checked-out AS LOGICAL. 
DEFINE buffer buf-resline1 FOR res-line. 
 
  IF sorttype = 1 THEN 
  DO: 
    FOR EACH res-line WHERE res-line.resnr = resnr 
      AND res-line.zinr NE "" AND res-line.active-flag = 1 
      /* AND res-line.abreise = ci-date */ 
      AND res-line.resstatus NE 12 NO-LOCK, 
      FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = res-line.reslinnr NO-LOCK 
      BY res-line.resstatus descending BY res-line.zinr BY res-line.name: 
      FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE bill-line THEN 
      DO:
        CREATE t-res-line.
        ASSIGN
            t-res-line.resnr = res-line.resnr
            t-res-line.reslinnr = res-line.reslinnr
            t-res-line.name = res-line.name
            t-res-line.zinr = res-line.zinr
            t-res-line.resstatus = res-line.resstatus
            t-res-line.active-flag = res-line.active-flag.
        /*MTRUN res-checkout.p(res-line.resnr, res-line.reslinnr, YES, 
                       OUTPUT checked-out). */
        FIND FIRST buf-resline1 WHERE buf-resline1.resnr = res-line.resnr 
          AND buf-resline1.reslinnr = res-line.reslinnr NO-LOCK.
        IF AVAILABLE buf-resline1 THEN
        DO:
            CREATE resline1.
            ASSIGN
            resline1.resnr     = buf-resline1.resnr
            resline1.reslinnr  = buf-resline1.reslinnr
            resline1.resstatus = buf-resline1.resstatus.
        END.
        /*MTFIND FIRST res-list WHERE res-list.reslinnr = res-line.reslinnr 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE res-list THEN 
        DO: 
          create res-list. 
          res-list.name = res-line.name. 
          res-list.zinr = res-line.zinr. 
          res-list.reslinnr = res-line.reslinnr. 
          res-list.resstatus = resline1.resstatus. 
          res-list.sysdate = today. 
          res-list.zeit = time. 
        END. */
        /*MTOPEN QUERY q1 FOR EACH res-list NO-LOCK BY res-list.sysdate 
          descending BY res-list.zeit descending. 
        IF res-line.active-flag = 2 THEN 
        DO: 
          anzahl = anzahl + 1. 
          DISP anzahl WITH FRAME frame1. 
        END. */
      END. 
    END. 
  END. 
  ELSE 
  DO: 
    FOR EACH res-line WHERE res-line.resnr = resnr 
      AND res-line.zinr NE "" AND res-line.active-flag = 1 
      AND res-line.resstatus NE 12 NO-LOCK,
      FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = res-line.reslinnr NO-LOCK 
      BY res-line.resstatus DESCENDING: 

      CREATE t-res-line.
      ASSIGN
          t-res-line.resnr = res-line.resnr
          t-res-line.reslinnr = res-line.reslinnr
          t-res-line.name = res-line.name
          t-res-line.zinr = res-line.zinr
          t-res-line.resstatus = res-line.resstatus
          t-res-line.active-flag = res-line.active-flag.

      /*MTRUN res-checkout.p(res-line.resnr, res-line.reslinnr, YES, 
          OUTPUT checked-out). */
      FIND FIRST buf-resline1 WHERE buf-resline1.resnr = res-line.resnr 
        AND buf-resline1.reslinnr = res-line.reslinnr NO-LOCK.
      IF AVAILABLE buf-resline1 THEN
      DO:
          CREATE resline1.
          ASSIGN
          resline1.resnr     = buf-resline1.resnr
          resline1.reslinnr  = buf-resline1.reslinnr
          resline1.resstatus = buf-resline1.resstatus.
      END.

      /*MTFIND FIRST res-list WHERE res-list.reslinnr = res-line.reslinnr 
          NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE res-list THEN 
      DO: 
        CREATE res-list. 
        res-list.name = res-line.name. 
        res-list.zinr = res-line.zinr. 
        res-list.reslinnr = res-line.reslinnr. 
        res-list.resstatus = resline1.resstatus. 
      END.*/ 
      /*MTOPEN QUERY q1 FOR EACH res-list NO-LOCK BY res-list.reslinnr. 
      IF res-line.active-flag = 2 THEN 
      DO: 
        anzahl = anzahl + 1. 
        DISP anzahl WITH FRAME frame1. 
        PAUSE 1. 
      END.*/ 
    END. 
  END. 
END. 
