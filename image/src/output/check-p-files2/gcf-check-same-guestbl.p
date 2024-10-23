DEFINE TEMP-TABLE tlist
    FIELD gastno AS INTEGER.
   
DEFINE INPUT PARAMETER caseType    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER gastno      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER email-adr   AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER mobil-phone AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER same-guest AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR tlist.

DEFINE VARIABLE gphone AS CHAR NO-UNDO.
DEFINE BUFFER bguest FOR guest.

FOR EACH tlist:
    DELETE tlist.
END.

IF caseType = 1 THEN DO: /*modify*/
    FIND FIRST guest WHERE guest.gastnr = gastno AND guest.karteityp = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN DO:
        IF guest.mobil-telefon MATCHES "62*" THEN DO:
            ASSIGN gphone = REPLACE(SUBSTRING(guest.mobil-telefon,1,2), "62", "0") + SUBSTRING(guest.mobil-telefon,3).
        END.
        ELSE IF guest.mobil-telefon MATCHES "+62*" THEN DO:
            ASSIGN gphone = REPLACE(SUBSTRING(guest.mobil-telefon,1,3), "+62", "0") + SUBSTRING(guest.mobil-telefon,4).
        END.
        ELSE IF guest.mobil-telefon MATCHES "*-*" THEN ASSIGN gphone = REPLACE(guest.mobil-telefon, "-", "").
    
        IF guest.mobil-telefon MATCHES "62*" THEN
            ASSIGN gphone = REPLACE(SUBSTRING(guest.mobil-telefon,1,3), "62 ", "0") + TRIM(SUBSTRING(guest.mobil-telefon,4)).
        IF SUBSTRING(guest.mobil-telefon,2,1) = CHR(32) THEN
            ASSIGN gphone = REPLACE(guest.mobil-telefon, " ", "").
    
        
        IF guest.email-adr NE " " THEN DO:
            FOR EACH bguest WHERE bguest.gastnr NE guest.gastnr 
                AND bguest.email-adr = guest.email-adr NO-LOCK:
    
                FIND FIRST tlist WHERE tlist.gastno = bguest.gastnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tlist THEN DO:
                    CREATE tlist.
                    ASSIGN tlist.gastno = bguest.gastnr.
                END.
    
            END.
        END.
        ELSE IF gphone NE "" THEN DO:
            FIND FIRST bguest WHERE bguest.gastnr NE guest.gastnr 
                AND bguest.mobil-telefon MATCHES ("*" + gphone) NO-LOCK NO-ERROR.
            IF AVAILABLE bguest THEN DO:
                FOR EACH bguest WHERE bguest.gastnr NE guest.gastnr 
                    AND bguest.mobil-telefon MATCHES ("*" + gphone) NO-LOCK:
        
                    FIND FIRST tlist WHERE tlist.gastno = bguest.gastnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tlist THEN DO:
                        CREATE tlist.
                        ASSIGN tlist.gastno = bguest.gastnr.
                    END.
        
                END.
            END.
            ELSE DO:
                FOR EACH bguest WHERE bguest.gastnr NE guest.gastnr 
                    AND bguest.mobil-telefon = guest.mobil-telefon NO-LOCK:
        
                    FIND FIRST tlist WHERE tlist.gastno = bguest.gastnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tlist THEN DO:
                        CREATE tlist.
                        ASSIGN tlist.gastno = bguest.gastnr.
                    END.       
                END.
            END.            
        END.
    END.
END.
ELSE IF caseType = 2 THEN DO: /*New*/
    IF email-adr NE "" THEN DO:
        FOR EACH bguest WHERE bguest.gastnr NE gastno 
            AND bguest.email-adr = email-adr NO-LOCK:

            FIND FIRST tlist WHERE tlist.gastno = bguest.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tlist THEN DO:
                CREATE tlist.
                ASSIGN tlist.gastno = bguest.gastnr.
            END.
        END.
    END.
    ELSE IF mobil-phone NE "" THEN DO:
        IF mobil-phone MATCHES "62*" THEN DO:
            ASSIGN gphone = REPLACE(SUBSTRING(mobil-phone,1,2), "62", "0") + SUBSTRING(mobil-phone,3).
        END.
        ELSE IF mobil-phone MATCHES "+62*" THEN DO:
            ASSIGN gphone = REPLACE(SUBSTRING(mobil-phone,1,3), "+62", "0") + SUBSTRING(mobil-phone,4).
        END.
        ELSE IF mobil-phone MATCHES "*-*" THEN ASSIGN gphone = REPLACE(mobil-phone, "-", "").
    
        IF mobil-phone MATCHES "62*" THEN
            ASSIGN gphone = REPLACE(SUBSTRING(mobil-phone,1,3), "62 ", "0") + TRIM(SUBSTRING(mobil-phone,4)).
        IF SUBSTRING(mobil-phone,2,1) = CHR(32) THEN
            ASSIGN gphone = REPLACE(mobil-phone, " ", "").

        FOR EACH bguest WHERE bguest.gastnr NE gastno
            AND bguest.mobil-telefon MATCHES ("*" + gphone) NO-LOCK:

            FIND FIRST tlist WHERE tlist.gastno = bguest.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tlist THEN DO:
                CREATE tlist.
                ASSIGN tlist.gastno = bguest.gastnr.
            END.
        END.
    END.
END.





FIND FIRST tlist NO-LOCK NO-ERROR.
IF AVAILABLE tlist THEN ASSIGN same-guest = YES.

