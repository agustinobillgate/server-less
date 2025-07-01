DEFINE TEMP-TABLE rsv-table-list
    FIELD rec-id        AS INTEGER
    FIELD bookingDate   AS DATE
    FIELD reservationNo AS INTEGER
    FIELD guestID       AS INTEGER
    FIELD guestName     AS CHAR
    FIELD guestEmail    AS CHAR
    FIELD guestPhone    AS CHAR
    FIELD depositAmount AS DECIMAL
    FIELD paymentAmount AS DECIMAL
    FIELD statusRsv     AS CHAR
    FIELD pax           AS INTEGER
    FIELD dept-no       AS INTEGER
    FIELD dept-name     AS CHARACTER
    FIELD table-no      AS INTEGER
    FIELD f-time        AS CHARACTER
    FIELD t-time        AS CHARACTER
    FIELD remark        AS CHARACTER
    FIELD usr-id        AS CHARACTER
    FIELD bill-no       AS CHARACTER
. 

DEFINE INPUT PARAMETER from-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date   AS DATE NO-UNDO.
DEFINE INPUT PARAMETER sorttype  AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR rsv-table-list.

DEFINE BUFFER bqueasy FOR queasy.

DEFINE VARIABLE doit AS LOGICAL NO-UNDO.
DEFINE VARIABLE rstatus AS CHAR EXTENT 4 NO-UNDO.
ASSIGN
    rstatus[1] = "OPEN"
    rstatus[2] = "CLOSE"
    rstatus[3] = "CANCEL"
    rstatus[4] = "EXPIRED"
.


FOR EACH queasy WHERE queasy.KEY = 311
    AND queasy.date1 GE from-date
    AND queasy.date1 LE to-date NO-LOCK:

    ASSIGN doit = YES.


    IF sorttype GT 0 THEN DO:
        IF sorttype = 1 AND queasy.betriebsnr NE 0 THEN ASSIGN doit = NO. /*open*/
        ELSE IF sorttype = 2 AND queasy.betriebsnr NE 1 THEN ASSIGN doit = NO. /*close*/
        ELSE IF sorttype = 3 AND queasy.betriebsnr NE 2 THEN ASSIGN doit = NO. /*cancel*/
        ELSE IF sorttype = 4 AND queasy.betriebsnr NE 3 THEN ASSIGN doit = NO. /*expired*/
    END.
    
    IF doit THEN DO:
        CREATE rsv-table-list.
        ASSIGN rsv-table-list.rec-id            = RECID(queasy)
               rsv-table-list.bookingDate       = queasy.date1  
               rsv-table-list.reservationNo     = queasy.number1 
               rsv-table-list.guestID           = INTEGER(ENTRY(1, queasy.char2, "|"))
               rsv-table-list.statusRsv         = rstatus[queasy.betriebsnr + 1]
               rsv-table-list.pax               = queasy.number2                 
            .

        IF queasy.char1 NE "" AND queasy.char1 NE ? THEN DO:
            ASSIGN
               rsv-table-list.bill-no           = ENTRY(1, queasy.char1, "|") 
               rsv-table-list.dept-no           = INTEGER(ENTRY(2, queasy.char1, "|")).

            IF NUM-ENTRIES(queasy.char1, "|") GE 3 THEN
               ASSIGN rsv-table-list.table-no          = INTEGER(ENTRY(3, queasy.char1, "|"))
            .
        END.

        IF queasy.char3 NE "" AND queasy.char3 NE ? THEN DO:
            ASSIGN 
                rsv-table-list.remark            = ENTRY(2, queasy.char3, "|") 
                rsv-table-list.usr-id            = ENTRY(1, queasy.char3, "|") 
             .
        END.
        
        IF rsv-table-list.dept-no GT 0 THEN DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = rsv-table-list.dept-no NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN ASSIGN rsv-table-list.dept-name = hoteldpt.depart.
        END.
    
        FIND FIRST guest WHERE guest.gastnr = rsv-table-list.guestID NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN DO:
            ASSIGN rsv-table-list.guestName    = guest.NAME + "," + guest.vorname1
                   rsv-table-list.guestPhone   = guest.mobil-telefon
                   rsv-table-list.guestEmail   = guest.email-adr
            .
        END.
    
        FOR EACH bqueasy WHERE bqueasy.KEY = 312
            AND bqueasy.number1 = queasy.number1 NO-LOCK:
            ASSIGN rsv-table-list.depositAmount = rsv-table-list.depositAmount + bqueasy.deci1
                   rsv-table-list.paymentAmount = rsv-table-list.paymentAmount + bqueasy.deci2.
        END.
    END.
END.




