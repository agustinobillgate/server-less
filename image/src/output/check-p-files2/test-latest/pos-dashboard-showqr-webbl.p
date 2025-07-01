
DEFINE TEMP-TABLE t-list   
    FIELD dept        AS INTEGER FORMAT "99" LABEL "Dept"  
    FIELD tischnr     AS INTEGER FORMAT ">>>>" LABEL "Table"  
    FIELD bezeich     AS CHAR FORMAT "x(16)" LABEL "Description"   
    FIELD normalbeleg AS INTEGER FORMAT ">>9"   
    FIELD name        AS CHARACTER FORMAT "x(12)" INITIAL "" COLUMN-LABEL "Served by"   
    FIELD occupied    AS LOGICAL FORMAT "Yes/No" LABEL "OCC" INITIAL NO   
    FIELD belegung    AS INTEGER FORMAT ">>9" COLUMN-LABEL "Pax"   
    FIELD balance     AS DECIMAL FORMAT "->>>,>>>,>>9.99"  
    FIELD zinr        AS CHARACTER FORMAT "x(4)"
    FIELD gname       AS CHAR FORMAT "x(28)" LABEL "Guest Name"
    FIELD ask-bill    AS LOGICAL LABEL "Ask For Bill"
    FIELD bill-print  AS LOGICAL LABEL "Printed"
    FIELD platform    AS CHAR FORMAT "x(13)" LABEL "Platform"
    FIELD allow-ctr   AS CHAR FORMAT "x(13)" LABEL "Allow Room Charge"
    FIELD bill-number AS INTEGER FORMAT ">>>>>>>>"
    FIELD pay-status  AS CHARACTER FORMAT "x(10)" LABEL "Pay Status"
    .

DEFINE TEMP-TABLE pick-table
    FIELD dept      AS INT FORMAT "99" LABEL "Dept"
    FIELD tableno   AS INT FORMAT ">>>>" LABEL "Table"
    FIELD pax       AS INT FORMAT ">>>" LABEL "Pax"
    FIELD gname     AS CHAR FORMAT "x(25)" LABEL "Guest Name"
    FIELD occupied  AS LOGICAL LABEL "Occupied"
    FIELD session-parameter AS CHAR
    FIELD gemail    AS CHAR
    FIELD expired-session AS LOGICAL
    FIELD dataQR AS CHAR
    FIELD date-time AS DATETIME FORMAT "99/99/99 HH:MM:SS" LABEL "Picked Datetime"
    .

DEFINE INPUT PARAMETER asroom-service   AS LOGICAL.
DEFINE INPUT PARAMETER dynamic-qr       AS LOGICAL.
DEFINE INPUT PARAMETER outlet-number    AS INTEGER.
DEFINE INPUT PARAMETER table-nr         AS INTEGER.
DEFINE INPUT PARAMETER guest-name       AS CHARACTER.
DEFINE INPUT PARAMETER pax              AS INTEGER.
DEFINE INPUT PARAMETER urlWS            AS CHARACTER.
DEFINE INPUT PARAMETER licenseNr        AS INTEGER.
DEFINE OUTPUT PARAMETER result-msg      AS CHARACTER.
DEFINE OUTPUT PARAMETER encodedUrl      AS CHARACTER.
DEFINE OUTPUT PARAMETER encodedSession  AS CHARACTER.
DEFINE OUTPUT PARAMETER dataQR          AS CHARACTER.
DEFINE OUTPUT PARAMETER pathQR          AS CHARACTER.
DEFINE OUTPUT PARAMETER table-taken     AS LOGICAL.
DEFINE OUTPUT PARAMETER flag-rs         AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER TABLE FOR pick-table.

DEFINE VARIABLE mMemptr         AS MEMPTR.
DEFINE VARIABLE encodedtext     AS LONGCHAR NO-UNDO.
DEFINE VARIABLE sessionID       AS CHAR.
DEFINE VARIABLE sha-sessionID   AS CHAR.
DEFINE VARIABLE session-ok      AS LOGICAL.
DEFINE VARIABLE success-taken   AS LOGICAL.
DEFINE VARIABLE loop-session    AS INT.

/**************************************************************************
                                  PROCESS
**************************************************************************/

IF guest-name EQ ? THEN guest-name = "".
IF urlWS EQ ? THEN urlWS = "".

IF urlWS EQ "" THEN
DO:
    result-msg = "UrlWebServices Not Available In Configuration Setup.".
    RETURN.
END.

IF NOT asroom-service THEN
DO:
    IF dynamic-qr THEN /*DYNAMIC QR*/
    DO:
        DO loop-session = 1 TO 10:
            sessionID = STRING(TODAY) + STRING(TIME) + STRING(outlet-number) + STRING(table-nr) + guest-name.
            sha-sessionID = HEX-ENCODE(SHA1-DIGEST(sessionID)). 
            encodedtext = SUBSTRING(sha-sessionID,1,20).
            sessionID = encodedtext.
        
            RUN pos-dashboard-checksessionbl.p(sessionID, OUTPUT session-ok).
            IF session-ok THEN LEAVE.
        END.
    
        COPY-LOB FROM encodedtext TO mMemptr.
        encodedtext = BASE64-ENCODE(mMemptr).
        encodedSession = STRING(encodedtext).
    
        IF urlWS NE "" THEN
        DO:
            encodedtext = urlWS.
            COPY-LOB FROM encodedtext TO mMemptr.
            encodedtext = BASE64-ENCODE(mMemptr).
            encodedUrl = STRING(encodedtext).
        END.
    
        pathQR = "C:\e1-vhp\Zint\QRData".
        dataQR = "https://online-order.e1-vhp.com/selforder?endpoint=" + encodedUrl + "&session=" + encodedSession.
    
        RUN pos-dashboard-proc-sessionbl.p (1, sessionID, outlet-number, table-nr, guest-name, pax, "", "", "", "", "").
    
        table-taken = YES.
    END.
    ELSE /*STATIC QR*/
    DO:
        encodedtext = STRING(licenseNr) + "d271092o" + STRING(outlet-number) + "@170763t" + STRING(table-nr).
        sessionID = encodedtext.

        COPY-LOB FROM encodedtext TO mMemptr.
        encodedtext = BASE64-ENCODE(mMemptr).
        encodedSession = STRING(encodedtext).
    
        IF urlWS NE "" THEN
        DO:
            encodedtext = urlWS.
            COPY-LOB FROM encodedtext TO mMemptr.
            encodedtext = BASE64-ENCODE(mMemptr).
            encodedUrl = STRING(encodedtext).
        END.

        pathQR = "C:\e1-vhp\Zint\QRData".
        dataQR = "https://online-order.e1-vhp.com/selforder?endpoint=" + encodedUrl + "&session=" + encodedSession.
    
        RUN pos-dashboard-proc-sessionbl.p (1, sessionID, outlet-number, table-nr, guest-name, pax, "", "", "", "", "").
    
        table-taken = YES.
    END.

    IF table-taken THEN
    DO:
        RUN pos-dashboard-taken-tablebl.p(1, sessionID, table-nr, guest-name, pax, outlet-number, dataQR, DATETIME(TODAY,MTIME), dynamic-qr,
                                        OUTPUT success-taken, OUTPUT TABLE pick-table).
        IF success-taken THEN
        DO:
            RUN pos-dashboard-opened-tischbl.p(outlet-number, OUTPUT TABLE t-list, OUTPUT TABLE pick-table).                        
        END.
    END.
END.
ELSE
DO:
    IF urlWS NE "" THEN
    DO:
        encodedtext = urlWS.
        COPY-LOB FROM encodedtext TO mMemptr.
        encodedtext = BASE64-ENCODE(mMemptr).
        encodedUrl = STRING(encodedtext).
    END.

    pathQR = "C:\e1-vhp\Zint\QRData".
    dataQR = "https://online-order.e1-vhp.com/selforder?endpoint=" + encodedUrl + "&htlid=" + STRING(licenseNr) + "&outlet=" + STRING(outlet-number).
    flag-rs = YES.
END.

