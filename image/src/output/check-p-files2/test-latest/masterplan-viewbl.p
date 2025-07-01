/*****************************************
Author      : Fadly Muflih 
Created     : 03/03/2021
Purpose     : Get Data Masterplan View
*****************************************/

DEFINE TEMP-TABLE t-mplan-view
  FIELD block-id    AS CHARACTER
  FIELD event-name  AS CHARACTER
  FIELD resno       AS INTEGER
  FIELD gname       AS CHARACTER
  FIELD guest-no    AS INTEGER
  FIELD room        AS CHARACTER
  FIELD room-desc   AS CHARACTER
  FIELD stat-no     AS INTEGER
  FIELD stat-code   AS CHARACTER
  FIELD invno       AS INTEGER
  FIELD fr-date     AS DATE
  FIELD to-date     AS DATE
  FIELD fr-time     AS CHARACTER
  FIELD to-time     AS CHARACTER
  FIELD amount      AS DECIMAL
  FIELD setup       AS CHARACTER
  FIELD rsize       AS INTEGER
  FIELD person      AS INTEGER
  FIELD preparation AS INTEGER
  FIELD ext         AS CHARACTER
  FIELD flag        AS CHARACTER
.

DEFINE TEMP-TABLE t-mplan-list
  FIELD block-id    AS CHARACTER
  FIELD event-name  AS CHARACTER
  FIELD resno       AS INTEGER
  FIELD gname       AS CHARACTER
  FIELD guest-no    AS INTEGER
  FIELD room        AS CHARACTER
  FIELD room-desc   AS CHARACTER
  FIELD stat-no     AS INTEGER
  FIELD stat-code   AS CHARACTER
  FIELD invno       AS INTEGER
  FIELD fr-date     AS DATE
  FIELD to-date     AS DATE
  FIELD fr-time     AS CHARACTER
  FIELD to-time     AS CHARACTER
  FIELD amount      AS DECIMAL
  FIELD setup       AS CHARACTER
  FIELD rsize       AS INTEGER
  FIELD person      AS INTEGER
  FIELD preparation AS INTEGER
  FIELD ext         AS CHARACTER
  FIELD flag        AS CHARACTER
.


DEFINE TEMP-TABLE buff-mplan-list
  FIELD block-id    AS CHARACTER
  FIELD event-name  AS CHARACTER
  FIELD resno       AS INTEGER
  FIELD gname       AS CHARACTER
  FIELD guest-no    AS INTEGER
  FIELD room        AS CHARACTER
  FIELD room-desc   AS CHARACTER
  FIELD stat-no     AS INTEGER
  FIELD stat-code   AS CHARACTER
  FIELD invno       AS INTEGER
  FIELD fr-date     AS DATE
  FIELD to-date     AS DATE
  FIELD fr-time     AS CHARACTER
  FIELD to-time     AS CHARACTER
  FIELD amount      AS DECIMAL
  FIELD setup       AS CHARACTER
  FIELD rsize       AS INTEGER
  FIELD person      AS INTEGER
  FIELD preparation AS INTEGER
  FIELD ext         AS CHARACTER
  FIELD flag        AS CHARACTER
.


DEFINE INPUT PARAMETER mode         AS CHARACTER.
DEFINE INPUT PARAMETER curr-date    AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-mplan-view.
/*
DEFINE VARIABLE mode        AS CHARACTER NO-UNDO.
DEFINE VARIABLE curr-date   AS DATE NO-UNDO.
*/
DEFINE VARIABLE curr-week   AS DATE NO-UNDO.
DEFINE VARIABLE ftdate      AS DATE NO-UNDO.
DEFINE VARIABLE logi1       AS LOGICAL INITIAL NO.

IF mode EQ "daily" THEN RUN daily-view.
ELSE RUN weekly-view.

PROCEDURE daily-view:
  FIND FIRST bk-event-detail WHERE bk-event-detail.start-date EQ curr-date
    AND bk-event-detail.end-date EQ curr-date NO-LOCK NO-ERROR.
  IF AVAILABLE bk-event-detail THEN
  DO:
    FIND FIRST bk-master WHERE bk-master.block-id EQ bk-event-detail.block-id
      AND bk-master.cancel-flag[1] EQ NO NO-LOCK NO-ERROR.
    IF AVAILABLE bk-master THEN logi1 = YES.
  END.
  
  IF logi1 = NO THEN
  DO:
    FOR EACH bk-raum NO-LOCK BY bk-raum.bezeich:
      CREATE t-mplan-list.
      ASSIGN
        t-mplan-list.room         = bk-raum.raum
        t-mplan-list.room-desc    = bk-raum.bezeich
        t-mplan-list.flag         = "*"
      .
    END.
  END.
  ELSE
  DO:
    FOR EACH bk-event-detail WHERE bk-event-detail.start-date EQ curr-date
      AND bk-event-detail.end-date EQ curr-date NO-LOCK BY bk-event-detail.venue:
  
      CREATE t-mplan-list.
      ASSIGN
        t-mplan-list.event-name   = bk-event-detail.event-name
        t-mplan-list.room-desc    = bk-event-detail.venue
        t-mplan-list.setup        = bk-event-detail.setup
        t-mplan-list.fr-date      = bk-event-detail.start-date
        t-mplan-list.to-date      = bk-event-detail.end-date
        t-mplan-list.fr-time      = STRING(bk-event-detail.start-time, "HH:MM")
        t-mplan-list.to-time      = STRING(bk-event-detail.end-time, "HH:MM")
        t-mplan-list.amount       = bk-event-detail.amount
        t-mplan-list.flag         = "**"
      .           
      
      FIND FIRST bk-raum WHERE bk-raum.bezeich EQ bk-event-detail.venue NO-LOCK NO-ERROR.
      IF AVAILABLE bk-raum THEN t-mplan-list.room = bk-raum.raum.
  
      FIND FIRST bk-rset WHERE ENTRY(1, bk-rset.bezeichnung, "/") EQ bk-event-detail.venue
        AND ENTRY(2, bk-rset.bezeichnung, "/") EQ bk-event-detail.setup NO-LOCK NO-ERROR.
      IF AVAILABLE bk-rset THEN
      DO:
        ASSIGN        
          t-mplan-list.rsize        = bk-rset.groesse
          t-mplan-list.person       = bk-rset.personen
          t-mplan-list.preparation  = bk-rset.vorbereit
          t-mplan-list.ext          = bk-rset.nebenstelle 
        .
      END.
  
      FIND FIRST bk-master WHERE bk-master.block-id EQ bk-event-detail.block-id NO-LOCK NO-ERROR.
      IF AVAILABLE bk-master THEN
      DO:
        ASSIGN
          t-mplan-list.block-id   = bk-master.block-id
          t-mplan-list.resno      = bk-master.resnr
          t-mplan-list.guest-no   = bk-master.gastnr
          t-mplan-list.gname      = bk-master.NAME
          t-mplan-list.stat-no    = bk-master.resstatus        
        .
  
        FIND FIRST bk-queasy WHERE bk-queasy.KEY = 1
            AND bk-queasy.number1 EQ bk-master.resstatus NO-LOCK NO-ERROR.
        IF AVAILABLE bk-queasy THEN t-mplan-list.stat-code = bk-queasy.char1.
      END.
    END.
  
    FOR EACH t-mplan-list:
      CREATE buff-mplan-list.
      BUFFER-COPY t-mplan-list TO buff-mplan-list.
    END.
  
    FOR EACH bk-raum NO-LOCK BY bk-raum.raum:
      FIND FIRST buff-mplan-list WHERE buff-mplan-list.room EQ bk-raum.raum NO-LOCK NO-ERROR.
      IF NOT AVAILABLE buff-mplan-list THEN
      DO:
        CREATE t-mplan-list.
        ASSIGN
          t-mplan-list.room         = bk-raum.raum
          t-mplan-list.room-desc    = bk-raum.bezeich
          t-mplan-list.flag         = "*"
        .
      END.        
    END.
  END.
  
  FOR EACH t-mplan-list NO-LOCK BY t-mplan-list.room:
    CREATE t-mplan-view.
    BUFFER-COPY t-mplan-list TO t-mplan-view.
  END.
END PROCEDURE.

PROCEDURE weekly-view:
  curr-week = curr-date + 6.

  FOR EACH bk-event-detail WHERE bk-event-detail.start-date GE curr-date
    AND bk-event-detail.start-date LE curr-week NO-LOCK :
  
    FIND FIRST bk-master WHERE bk-master.block-id EQ bk-event-detail.block-id
      AND bk-master.cancel-flag[1] EQ NO NO-LOCK NO-ERROR.
    IF AVAILABLE bk-master THEN logi1 = YES.

    IF logi1 = YES THEN LEAVE.
  END.

  IF logi1 = NO THEN
  DO:
    FOR EACH bk-raum NO-LOCK BY bk-raum.bezeich:
      CREATE t-mplan-list.
      ASSIGN
        t-mplan-list.room         = bk-raum.raum
        t-mplan-list.room-desc    = bk-raum.bezeich
        t-mplan-list.flag         = "*"
      .
    END.
  END.
  ELSE
  DO:
    FOR EACH bk-event-detail WHERE bk-event-detail.start-date GE curr-date
      AND bk-event-detail.start-date LE curr-week NO-LOCK BY bk-event-detail.venue:
  
      CREATE t-mplan-list.
      ASSIGN
        t-mplan-list.event-name   = bk-event-detail.event-name
        t-mplan-list.room-desc    = bk-event-detail.venue
        t-mplan-list.setup        = bk-event-detail.setup
        t-mplan-list.fr-date      = bk-event-detail.start-date
        t-mplan-list.to-date      = bk-event-detail.end-date
        t-mplan-list.fr-time      = STRING(bk-event-detail.start-time, "HH:MM")
        t-mplan-list.to-time      = STRING(bk-event-detail.end-time, "HH:MM")
        t-mplan-list.amount       = bk-event-detail.amount
        t-mplan-list.flag         = "**"
      .           
      
      FIND FIRST bk-raum WHERE bk-raum.bezeich EQ bk-event-detail.venue NO-LOCK NO-ERROR.
      IF AVAILABLE bk-raum THEN t-mplan-list.room = bk-raum.raum.
  
      FIND FIRST bk-rset WHERE ENTRY(1, bk-rset.bezeichnung, "/") EQ bk-event-detail.venue
        AND ENTRY(2, bk-rset.bezeichnung, "/") EQ bk-event-detail.setup NO-LOCK NO-ERROR.
      IF AVAILABLE bk-rset THEN
      DO:
        ASSIGN        
          t-mplan-list.rsize        = bk-rset.groesse
          t-mplan-list.person       = bk-rset.personen
          t-mplan-list.preparation  = bk-rset.vorbereit
          t-mplan-list.ext          = bk-rset.nebenstelle 
        .
      END.
  
      FIND FIRST bk-master WHERE bk-master.block-id EQ bk-event-detail.block-id NO-LOCK NO-ERROR.
      IF AVAILABLE bk-master THEN
      DO:
        ASSIGN
          t-mplan-list.block-id   = bk-master.block-id
          t-mplan-list.resno      = bk-master.resnr
          t-mplan-list.guest-no   = bk-master.gastnr
          t-mplan-list.gname      = bk-master.NAME
          t-mplan-list.stat-no    = bk-master.resstatus        
        .
  
        FIND FIRST bk-queasy WHERE bk-queasy.KEY = 1
            AND bk-queasy.number1 EQ bk-master.resstatus NO-LOCK NO-ERROR.
        IF AVAILABLE bk-queasy THEN t-mplan-list.stat-code = bk-queasy.char1.
      END.
    END.
  
    FOR EACH t-mplan-list:
      CREATE buff-mplan-list.
      BUFFER-COPY t-mplan-list TO buff-mplan-list.
    END.
  
    FOR EACH bk-raum NO-LOCK BY bk-raum.raum:
      FIND FIRST buff-mplan-list WHERE buff-mplan-list.room EQ bk-raum.raum NO-LOCK NO-ERROR.
      IF NOT AVAILABLE buff-mplan-list THEN
      DO:
        CREATE t-mplan-list.
        ASSIGN
          t-mplan-list.room         = bk-raum.raum
          t-mplan-list.room-desc    = bk-raum.bezeich
          t-mplan-list.flag         = "*"
        .
      END.        
    END.
  END.

  FOR EACH t-mplan-list NO-LOCK BY t-mplan-list.room:
    CREATE t-mplan-view.
    BUFFER-COPY t-mplan-list TO t-mplan-view.
  END.
END PROCEDURE.
