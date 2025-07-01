/*****************************************************************
Author          : Irfan Fadhillah
Created Date    : July 1, 2019
Purpose         : Show Room & Catering Foreacast Revenue
*****************************************************************/

DEFINE TEMP-TABLE t-bk-event
    FIELD bezeich   AS CHARACTER
    FIELD amount    AS DECIMAL.
    
DEFINE TEMP-TABLE t-bk-room
    FIELD bezeich   AS CHARACTER
    FIELD amount    AS DECIMAL.    

DEFINE INPUT PARAMETER blockId  AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-event.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-room.

DEFINE VARIABLE grandTotal      AS DECIMAL      NO-UNDO.
DEFINE VARIABLE totAmount       AS DECIMAL      NO-UNDO.
DEFINE VARIABLE i               AS INTEGER      NO-UNDO.
DEFINE VARIABLE blockCode       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE revenue         AS DECIMAL      NO-UNDO.
DEFINE VARIABLE roomRates       AS DECIMAL      NO-UNDO.

ASSIGN
    grandTotal  = 0
    totAmount   = 0.    

FOR EACH bk-event WHERE bk-event.block-id EQ blockId
   AND bk-event.flag EQ "**":  
   
   FIND FIRST bk-event-detail WHERE bk-event-detail.block-id EQ bk-event.block-id
       AND bk-event-detail.nr EQ bk-event.nr NO-LOCK NO-ERROR.
   IF AVAILABLE bk-event-detail THEN
   DO:
       grandTotal    = bk-event.amount * bk-event-detail.atendees.
       totAmount = totAmount + grandTotal.
   END.        
END.   

CREATE t-bk-event.
ASSIGN 
    t-bk-event.bezeich  = "Catering Revenue"
    t-bk-event.amount   = totAmount.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    blockCode   = bk-master.block-code.
    
    ASSIGN 
        roomRates   = 0
        revenue     = 0.
    
    CREATE t-bk-room.
    ASSIGN 
        t-bk-room.bezeich   = "Room Revenue"
        t-bk-room.amount    = revenue.

    FOR EACH bk-grid WHERE bk-grid.block-code EQ blockCode:
        roomRates = bk-grid.original-qty * room-rates.
        revenue = revenue + roomRates.
        
        FIND FIRST t-bk-room EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE t-bk-room THEN
        DO:
            ASSIGN
                t-bk-room.amount    = revenue.
        END.
        
        roomRates = 0.
    END.
END.

/*
FIND FIRST bk-master WHERE bk-master.block-id EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    i = bk-master.enddate - bk-master.startdate.
    FIND FIRST bk-room WHERE bk-room.block-id EQ bk-master.block-id NO-LOCK NO-ERROR.
    IF AVAILABLE bk-room THEN 
    DO:
        FIND FIRST ratecode WHERE ratecode.code EQ ENTRY(1, bk-room.ratecode, "|") NO-LOCK NO-ERROR.
        IF AVAILABLE ratecode THEN
        DO:
            CREATE t-bk-room.
            ASSIGN
                t-bk-room.bezeich   = "Room Revenue"
                t-bk-room.amount    = ratecode.zipreis * i.
        END.    
    END.    
END.    
*/
