/******************************************
Author          : Irfan Fadhillah
Created Date    : 23 May 2019
Purpose         : Get Event Data
******************************************/

DEFINE TEMP-TABLE t-event
    FIELD blockId       AS CHARACTER
    FIELD counter       AS INTEGER
    FIELD nr            AS INTEGER
    FIELD eventType     AS CHARACTER
    FIELD eventStatus   AS CHARACTER    
    FIELD eventName     AS CHARACTER
    FIELD startDate     AS DATE
    FIELD endDate       AS DATE
    FIELD startTime     AS CHARACTER
    FIELD endTime       AS CHARACTER
    FIELD atendees      AS INTEGER
    FIELD minGuaranted  AS INTEGER
    FIELD actual        AS INTEGER
    FIELD venue         AS CHARACTER
    FIELD setup         AS CHARACTER
    FIELD amount        AS DECIMAL.
    
DEFINE TEMP-TABLE t-bkraum LIKE bk-raum.    
DEFINE TEMP-TABLE t-bkrset LIKE bk-rset.

DEFINE INPUT PARAMETER blockId      AS CHARACTER.
DEFINE INPUT PARAMETER nr           AS INTEGER.
DEFINE OUTPUT PARAMETER resStatus   AS INTEGER.
DEFINE OUTPUT PARAMETER guestNo     AS INTEGER.
DEFINE OUTPUT PARAMETER pax         AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-event.
DEFINE OUTPUT PARAMETER TABLE FOR t-bkraum.
DEFINE OUTPUT PARAMETER TABLE FOR t-bkrset.



FIND FIRST t-event NO-ERROR.
FIND FIRST bk-event-detail WHERE bk-event-detail.block-id EQ blockId 
  AND bk-event-detail.nr EQ nr NO-LOCK NO-ERROR.
IF AVAILABLE bk-event-detail THEN 
DO:
    CREATE t-event.
    ASSIGN 
        t-event.blockId        = blockId        
        t-event.nr             = bk-event-detail.nr        
        t-event.eventType      = bk-event-detail.event-status        
        t-event.eventName      = bk-event-detail.event-name
        t-event.startDate      = bk-event-detail.start-date        
        t-event.endDate        = bk-event-detail.end-date
        t-event.eventType      = bk-event-detail.event-type        
        t-event.startTime      = STRING(bk-event-detail.start-time, "HH:MM")
        t-event.endTime        = STRING(bk-event-detail.end-time, "HH:MM")
        t-event.atendees       = bk-event-detail.atendees        
        t-event.minGuaranted   = bk-event-detail.min-guaranteed        
        t-event.actual         = bk-event-detail.actual        
        t-event.venue          = bk-event-detail.venue
        t-event.setup          = bk-event-detail.setup
        t-event.amount         = bk-event-detail.amount.
        
    FIND FIRST bk-raum WHERE bk-raum.bezeich EQ t-event.venue NO-LOCK NO-ERROR.
    IF AVAILABLE bk-raum THEN 
    DO:
        CREATE t-bkraum.
        BUFFER-COPY bk-raum TO t-bkraum.
    END.    
    
    FIND FIRST bk-rset WHERE ENTRY(1, bk-rset.bezeichnung, "/") EQ t-event.venue
        AND ENTRY(2, bk-rset.bezeichnung, "/") EQ t-event.setup NO-LOCK NO-ERROR.
    IF AVAILABLE bk-rset THEN
    DO:
        CREATE t-bkrset.
        BUFFER-COPY bk-rset TO t-bkrset.
    END.    
END.
ELSE
DO:
    FIND FIRST bk-catering WHERE bk-catering.block-id EQ blockId NO-LOCK NO-ERROR.
    IF AVAILABLE bk-catering THEN
    DO:
        pax = bk-catering.attendees.
    END.
END.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    FIND FIRST bk-queasy WHERE bk-queasy.key EQ 1
        AND bk-queasy.number1 EQ bk-master.resstatus NO-LOCK NO-ERROR.
    IF AVAILABLE bk-queasy THEN
    DO:
        IF bk-queasy.number2 GE 1 AND bk-queasy.number2 LE 3 THEN
        DO:
            resStatus = 2.
        END.
        ELSE IF bk-queasy.number2 EQ 4 THEN
        DO:
            resStatus = 1.
        END.
    END.    
END.


FIND FIRST bk-master WHERE bk-master.block-id EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    guestNo = bk-master.gastnr.
END.
