DEFINE TEMP-TABLE output-list
    FIELD resdate       AS DATE                         LABEL "Date"
    FIELD zinr          AS CHARACTER    FORMAT "x(7)"   LABEL "Room No"
    FIELD resnr         AS INTEGER      FORMAT ">>>>>9" LABEL "Resv No"
    FIELD guestname     AS CHARACTER    FORMAT "x(45)"  LABEL "Guest Name"
    FIELD pax           AS INTEGER      FORMAT ">>9"    LABEL "Pax"
    FIELD arrival       AS DATE                         LABEL "Arrival"
    FIELD olddepart     AS DATE                         LABEL "Old ETD"
    FIELD newdepart     AS DATE                         LABEL "New ETD"
    FIELD customer      AS CHARACTER    FORMAT "x(35)"  LABEL "Customer"
    FIELD ratecode      AS CHARACTER    FORMAT "x(25)"  LABEL "Rate Code"   
    .

DEFINE INPUT PARAMETER from-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE oldetd AS DATE NO-UNDO.
DEFINE VARIABLE newetd AS DATE NO-UNDO.
DEFINE VARIABLE i      AS INT  NO-UNDO.
DEFINE VARIABLE str    AS CHAR NO-UNDO.

DEFINE BUFFER gmember FOR guest.

FOR EACH res-line WHERE (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13) NO-LOCK:
    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
    FIND FIRST gmember WHERE gmember.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "ResChanges" 
        AND reslin-queasy.resnr EQ res-line.resnr
        AND reslin-queasy.date2 GE from-date
        AND reslin-queasy.date2 LE to-date NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN
    DO:
        
        ASSIGN
            oldetd = DATE(ENTRY(3, reslin-queasy.char3, ";"))
            newetd = DATE(ENTRY(4, reslin-queasy.char3, ";")).
    
        IF oldetd NE newetd THEN
        DO:
            CREATE output-list.
            ASSIGN 
                output-list.resdate   = reslin-queasy.date2 
                output-list.zinr      = res-line.zinr 
                output-list.resnr     = reslin-queasy.resnr 
                output-list.guestname = gmember.name  + ", " + gmember.vorname1 + " " + gmember.anrede1
                output-list.pax       = INT(entry(7,reslin-queasy.char3,";")) +
                                        INT(entry(9,reslin-queasy.char3,";")) +
                                        INT(entry(11,reslin-queasy.char3,";"))
                output-list.arrival   = DATE(entry(1 ,reslin-queasy.char3,";"))                                 /* Rulita 041124 | Fixing for Serverless */
                output-list.olddepart = DATE(entry(3 ,reslin-queasy.char3,";")) 
                output-list.newdepart = DATE(entry(4 ,reslin-queasy.char3,";")) 
                output-list.customer  = guest.name  + ", " + guest.vorname1 + " " + guest.anrede1
                .
            
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str = ENTRY(i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str,1,6) = "$CODE$" THEN 
                DO:
                    output-list.ratecode  = SUBSTR(str,7).
                    LEAVE.
                END.
            END.
        END.
    END.   
END.

