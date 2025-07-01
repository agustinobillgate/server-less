/* DELETE  GCF */ 
DEFINE INPUT PARAMETER gastnr       AS INTEGER. 
DEFINE OUTPUT PARAMETER error-code  AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER mname       AS CHARACTER.
DEFINE BUFFER guest1 FOR guest. 
DEFINE VARIABLE answer AS LOGICAL INITIAL NO. 

/*IF 080419*/
DEFINE VARIABLE gastNo  AS CHARACTER NO-UNDO.
/*END IF*/
 
FIND FIRST res-line WHERE res-line.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO: 
    error-code = 1. 
    RETURN. 
END. 
 
FIND FIRST res-line WHERE res-line.gastnrmember = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO: 
    error-code = 1. 
    RETURN. 
END. 
 
FIND FIRST res-line WHERE res-line.gastnrpay = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO: 
    error-code = 1. 
    RETURN. 
END. 
 
FIND FIRST debitor WHERE debitor.gastnr = gastnr 
  AND debitor.zahlkonto = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE debitor THEN 
DO: 
    error-code = 2. 
    RETURN. 
END. 
 
FIND FIRST debitor WHERE debitor.gastnrmember = gastnr 
  AND debitor.zahlkonto = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE debitor THEN 
DO: 
    error-code = 2. 
    RETURN. 
END. 
 
FIND FIRST guest1 WHERE guest1.master-gastnr = gastnr 
  AND guest1.gastnr GT 0 NO-LOCK NO-ERROR. 
IF AVAILABLE guest1 THEN 
DO: 
    error-code = 3.
    mname = caps(guest1.name) + ", " + caps(guest1.vorname1) + " " +   
            caps(guest1.anredefirma) + caps(guest1.anrede1).
    RETURN. 
END. 
 
FIND FIRST akt-cust WHERE akt-cust.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE akt-cust THEN 
DO: 
    error-code = 4. 
    RETURN. 
END. 
/*  %%%  */ 

FIND FIRST bill WHERE bill.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE bill THEN 
DO: 
    error-code = 5. 
    RETURN. 
END. 

FIND FIRST billhis WHERE billhis.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE billhis THEN 
DO: 
    error-code = 5. 
    RETURN. 
END. 

FIND FIRST kontline WHERE kontline.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE kontline THEN 
DO: 
    error-code = 6. 
    RETURN. 
END. 

RUN check-global-allotment(OUTPUT error-code).
IF error-code GT 0 THEN RETURN.

FIND FIRST zimmer WHERE zimmer.owner-nr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE zimmer THEN 
DO: 
    error-code = 7. 
    RETURN. 
END. 

FIND FIRST bk-veran WHERE bk-veran.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE bk-veran THEN 
DO: 
    error-code = 8. 
    RETURN. 
END. 

FIND FIRST mc-guest WHERE mc-guest.gastnr = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE mc-guest THEN 
DO: 
    error-code = 9. 
    RETURN. 
END. 

FIND FIRST cl-member WHERE cl-member.gastnr = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE cl-member THEN 
DO: 
    error-code = 10. 
    RETURN. 
END. 

FIND FIRST akt-kont WHERE akt-kont.betrieb-gast = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE akt-kont THEN
DO:
    error-code = 11. 
    RETURN. 
END.

/*IF 080319 - Add validation for deleting Dummy Guest Card for OTA in paramnr 615 requested by Faisal*/
FIND FIRST htparam WHERE paramnr EQ 615 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN 
DO:    
    gastNo = "*" + STRING(gastnr) + "*".
       
    IF htparam.fchar MATCHES gastNo THEN 
    DO:    
        error-code = 12.
        RETURN.
    END.
END.
/*END IF*/

/*  %%%   
FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
IF (TODAY - guest.letzte-res) LT 365 THEN 
DO: 
    error-code = -99. 
    RETURN. 
END. 
*/

/*
FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
DO TRANSACTION:
    FIND CURRENT guest EXCLUSIVE-LOCK. 
    
    FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
        DELETE guestseg. 
    END. 
    FOR EACH history WHERE history.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
        DELETE history. 
    END. 
    FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
        DELETE guest-pr. 
    END. 
    FOR EACH gk-notes WHERE gk-notes.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
        DELETE gk-notes. 
    END. 
    FOR EACH guestbud WHERE guestbud.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
        DELETE guestbud. 
    END. 
    FOR EACH akt-kont WHERE akt-kont.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
        DELETE akt-kont. 
    END. 

    /* Document Scanner License */
    FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK.
    IF htparam.flogical THEN RUN delete-guestbookbl.p(guest.gastnr). 
    
    DELETE guest.
    RELEASE guest.
END.
*/

PROCEDURE check-global-allotment:
DEF OUTPUT PARAMETER error-code AS INTEGER INIT 0 NO-UNDO.
DEF VAR tokcounter AS INTEGER NO-UNDO.
DEF VAR mesValue   AS CHAR    NO-UNDO.
    FOR EACH queasy WHERE queasy.KEY = 147 NO-LOCK:
        DO tokcounter = 1 TO NUM-ENTRIES(queasy.char3, ","):
            mesValue = ENTRY(tokcounter, queasy.char3, ",").
            IF mesValue NE "" AND INTEGER(mesValue) = gastnr THEN
            DO:
                error-code = 66.
                LEAVE.
            END.
        END.
    END.
END.
