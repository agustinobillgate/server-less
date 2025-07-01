DEFINE TEMP-TABLE tt-reslin
    FIELD group-name  AS CHARACTER
    FIELD name        AS CHAR
    FIELD resnr       AS INTEGER  
    FIELD room-qty    AS INT EXTENT 30
    FIELD zimmeranz   AS INT
    FIELD ankunft     AS DATE
    FIELD resstatus   AS INT
    .
    
DEFINE TEMP-TABLE res-output
    FIELD group-name    AS CHARACTER
    FIELD name          AS CHAR
    FIELD resnr         AS INTEGER  
    FIELD room-qty      AS INT EXTENT 31
    FIELD resstatus     AS INT
    FIELD tot-room-qty  AS INT
    FIELD description   AS CHAR
    .
    
DEFINE TEMP-TABLE summary-status
    FIELD room-qty      AS INT EXTENT 31
    FIELD resstatus     AS INT
    FIELD description   AS CHAR
    FIELD tot-room-qty  AS INT
    .

DEFINE TEMP-TABLE input-param
    FIELD input-date AS DATE.

DEFINE INPUT PARAMETER TABLE FOR input-param.
DEFINE OUTPUT PARAMETER TABLE FOR summary-status.
DEFINE OUTPUT PARAMETER TABLE FOR res-output.

DEFINE VARIABLE start-date  AS DATE NO-UNDO.
DEFINE VARIABLE end-date    AS DATE NO-UNDO.
DEFINE VARIABLE curr-date   AS DATE NO-UNDO.
DEFINE VARIABLE i           AS INTEGER NO-UNDO.
DEFINE VARIABLE room-count  AS INTEGER EXTENT 31 NO-UNDO.
DEFINE VARIABLE day-number  AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-qty     AS INT.
DEFINE VARIABLE last-day    AS INTEGER NO-UNDO.
DEFINE VARIABLE counter     AS INT INITIAL 0.
DEFINE VARIABLE prev-resnr  AS INT INIT 0.
DEFINE VARIABLE max-abreise AS DATE NO-UNDO.
DEFINE VARIABLE grand-total AS INT.
DEFINE VARIABLE summary-total AS INT.
DEFINE VARIABLE stat-list AS CHAR EXTENT 14 FORMAT "x(9)" NO-UNDO. 
stat-list[1]  = "Guaranted". 
stat-list[2]  = "6 PM". 
stat-list[3]  = "Tentative". 
stat-list[4]  = "WaitList". 
stat-list[5]  = "VerbalConfirm". 
stat-list[6]  = "Inhouse". 
stat-list[7]  = "". 
stat-list[8]  = "Departed". 
stat-list[9]  = "Cancelled". 
stat-list[10] = "NoShow". 
stat-list[11] = "ShareRes". 
stat-list[12] = "AccGuest". 
stat-list[13] = "RmSharer". 
stat-list[14] = "AccGuest". 

FIND FIRST input-param NO-LOCK.

last-day   = DAY(DATE(MONTH(input-param.input-date) + 1, 1, YEAR(input-param.input-date)) - 1).
start-date = DATE(MONTH(input-param.input-date), 1, YEAR(input-param.input-date)).  
end-date   = DATE(MONTH(input-param.input-date), last-day, YEAR(input-param.input-date)). 

FOR EACH res-line WHERE res-line.ankunft GE start-date 
    AND res-line.abreise GT end-date NO-LOCK:
    IF res-line.abreise GT max-abreise THEN
    DO:
        max-abreise = res-line.abreise.
    END.  
END.

IF max-abreise GT end-date THEN end-date = max-abreise.


FOR EACH tt-reslin:
  DELETE tt-reslin.
END.

FOR EACH res-line WHERE res-line.ankunft GE start-date 
    AND res-line.abreise LE end-date	
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 99
    AND res-line.resstatus NE 9
    AND res-line.resstatus NE 11
    AND res-line.resstatus NE 13 NO-LOCK,
    FIRST reservation WHERE reservation.resnr EQ res-line.resnr 
    AND reservation.grpFlag = YES:
  
    CREATE tt-reslin.
    ASSIGN 
      tt-reslin.group-name = reservation.groupname
      tt-reslin.name       = reservation.name
      tt-reslin.resnr      = res-line.resnr
      tt-reslin.room-qty   = 0
      tt-reslin.zimmeranz  = res-line.zimmeranz
      tt-reslin.ankunft    = res-line.ankunft
      tt-reslin.resstatus  = res-line.resstatus.      
END.

FOR EACH tt-reslin BY tt-reslin.resnr:
    FIND FIRST res-output WHERE res-output.resnr = tt-reslin.resnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE res-output THEN 
    DO:
        DO i = 1 TO last-day:
          room-count[i] = 0.
        END.

        tot-qty = 0.

        DO curr-date = start-date TO end-date:
            day-number = DAY(curr-date).
            IF day-number GE 1 AND day-number LE last-day THEN
            DO:
                IF tt-reslin.ankunft EQ curr-date THEN 
                DO:
                    room-count[day-number] = room-count[day-number] + tt-reslin.zimmeranz.
                    tot-qty = tot-qty + tt-reslin.zimmeranz.
                    grand-total = grand-total + tot-qty.
                END.
            END.
        END. /*end loop curr-date*/

        CREATE res-output.
        ASSIGN
            res-output.group-name   = tt-reslin.group-name
            res-output.NAME         = tt-reslin.NAME
            res-output.resstatus    = tt-reslin.resstatus
            res-output.description  = stat-list[res-output.resstatus]
            res-output.resnr        = tt-reslin.resnr
            res-output.tot-room-qty = tot-qty.
            
        DO i = 1 TO last-day:
            res-output.room-qty[i] = room-count[i].
        END.
    END.
    ELSE 
    DO:
        DO curr-date = start-date TO end-date:
            day-number = DAY(curr-date).
            IF day-number GE 1 AND day-number LE last-day THEN
            DO:
                IF tt-reslin.ankunft EQ curr-date THEN 
                DO:
                    room-count[day-number] = room-count[day-number] + tt-reslin.zimmeranz.
                    tot-qty = tot-qty + tt-reslin.zimmeranz.
                    grand-total = grand-total + tt-reslin.zimmeranz.
                END.
            END.
        END. /*end loop curr-date*/
        DO i = 1 TO last-day:
            res-output.room-qty[i] = room-count[i].
        END.
        res-output.tot-room-qty = tot-qty.
    END.
END.

FIND FIRST res-output WHERE res-output.resnr = tt-reslin.resnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-output THEN 
DO:
    CREATE res-output.
    ASSIGN
        res-output.group-name = "TOTAL"
        res-output.tot-room-qty = grand-total
        res-output.resstatus    = 0.
END.

FOR EACH summary-status:
  DELETE summary-status.
END.

FOR EACH res-output WHERE res-output.resstatus NE 0 BY res-output.resstatus:

    FIND FIRST summary-status WHERE summary-status.resstatus = res-output.resstatus NO-LOCK NO-ERROR.
    IF NOT AVAILABLE summary-status THEN 
    DO:
        CREATE summary-status.
        ASSIGN
            summary-status.resstatus = res-output.resstatus
            summary-status.description = stat-list[summary-status.resstatus].

    DO i = 1 TO last-day:
        summary-status.room-qty[i] = 0.
    END.
    END.
    DO i = 1 TO last-day:
        summary-status.room-qty[i] = summary-status.room-qty[i] + res-output.room-qty[i].
        summary-total = summary-total + res-output.room-qty[i].
    END.

    summary-status.tot-room-qty = summary-total.

END.










