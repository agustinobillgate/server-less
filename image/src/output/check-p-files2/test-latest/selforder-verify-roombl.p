DEFINE INPUT PARAMETER dept-number AS INT.
DEFINE INPUT PARAMETER room-number AS CHAR.
DEFINE INPUT PARAMETER inp-char    AS CHAR.

DEFINE OUTPUT PARAMETER sessionID AS CHAR.
DEFINE OUTPUT PARAMETER guest-name AS CHAR.
DEFINE OUTPUT PARAMETER guest-email AS CHAR.
DEFINE OUTPUT PARAMETER pax AS INT.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.

DEFINE VARIABLE found-flag AS LOGICAL.

IF room-number EQ "" OR room-number EQ ? THEN
DO :
    mess-result = "1-Room Number must be filled in!".
    RETURN.
END.

IF inp-char EQ ? OR inp-char EQ "" THEN
DO:
    mess-result = "2-Input Char must be filled in!".
    RETURN.
END.

IF dept-number EQ ? OR dept-number EQ 0 THEN
DO:
    mess-result = "3-Department Number must be filled in!".
    RETURN.
END.

DEFINE VARIABLE checkout-date AS DATE.
DEFINE VARIABLE rSalt AS RAW  NO-UNDO.
DEFINE VARIABLE cSalt AS CHAR NO-UNDO.
DEFINE VARIABLE mMemptr AS MEMPTR.
DEFINE VARIABLE encodedtext AS LONGCHAR NO-UNDO.
DEFINE VARIABLE encodedSession AS CHAR.

FUNCTION GetSalt RETURNS RAW (INPUT saltLengthLimit AS INTEGER):
    DEFINE VARIABLE i AS INTEGER INITIAL 0 NO-UNDO.
    
    saltLengthLimit = saltLengthLimit / 8.
    
    DO WHILE i < saltLengthLimit:
        PUT-BYTES(rSalt, LENGTH(rSalt) + 1) = GENERATE-PBE-SALT.
        i = i + 1.
    END.
    
    RETURN (rSalt).
END FUNCTION.

checkout-date = DATE(inp-char) NO-ERROR.

found-flag = NO.
FIND FIRST res-line WHERE res-line.resstatus EQ 6 
    AND res-line.zinr EQ room-number AND res-line.abreise EQ checkout-date NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN
DO:
    found-flag = NO.
    FIND FIRST res-line WHERE res-line.resstatus EQ 6 AND res-line.zinr EQ room-number NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            IF guest.NAME MATCHES '"*' + inp-char + '*"' THEN found-flag = YES.
            IF NOT found-flag THEN 
                IF guest.vorname1 MATCHES '"*' + inp-char + '*"' THEN found-flag = YES.
        END.
        ELSE found-flag = NO.
    END.
    ELSE found-flag = NO.
END.
ELSE found-flag = YES.

IF found-flag THEN
DO:
    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    guest-name  = guest.NAME + " " + guest.vorname1 + "," + guest.anrede1.
    guest-email = guest.email-adr.
    pax = res-line.erwachs + res-line.kind1 + res-line.gratis. 

    cSalt = STRING(HEX-ENCODE(GetSalt(32))).
    encodedtext = CAPS(SUBSTRING(csalt,1,20)).
    sessionID = encodedtext.

    COPY-LOB FROM encodedtext TO mMemptr.
    encodedtext = BASE64-ENCODE(mMemptr).
    encodedSession = STRING(encodedtext).
    sessionID = encodedSession.

    RUN selforder-proc-sessionbl.p (1, sessionID, dept-number, room-number, 
                                    guest-name, pax, room-number, res-line.ankunft, 
                                    res-line.abreise, "", guest-email).

    mess-result = "0-Verify Room Success!".
    RETURN.
END.
ELSE mess-result = "3-No Reservation Found!".
