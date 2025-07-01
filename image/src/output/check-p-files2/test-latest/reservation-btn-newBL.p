DEF INPUT PARAMETER i-case          AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER pvILanguage     AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER gastnr          AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER error-flag     AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAMETER pswd-str       AS CHAR    INIT ""  NO-UNDO.
DEF OUTPUT PARAMETER outstand       AS DECIMAL INIT 0   NO-UNDO. 
DEF OUTPUT PARAMETER resNo          AS INTEGER INIT 0   NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "reservation". 

DEF VARIABLE ratecode-exist AS LOGICAL NO-UNDO INIT NO.
DEF VARIABLE bill-date      AS DATE NO-UNDO.
DEF VARIABLE static-rcode   AS CHAR NO-UNDO.

DEF BUFFER rcbuff FOR ratecode.

RUN htpdate.p(110, OUTPUT bill-date).

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.

FIND FIRST htparam WHERE htparam.paramnr = 735 NO-LOCK.
IF htparam.feldtyp = 4 AND htparam.flogical THEN
DO:
    /*FOR EACH guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK:*/
    FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE guest-pr:   
        FIND FIRST queasy WHERE queasy.KEY = 2 
            AND queasy.char1 = guest-pr.CODE NO-LOCK.
        IF queasy.logi2 THEN /* dynamic rate */
        DO:
            FOR EACH rcbuff WHERE rcbuff.CODE = guest-pr.CODE NO-LOCK:
                FIND FIRST ratecode WHERE ratecode.CODE = SUBSTR(ENTRY(8, rcbuff.char1[5], ";"),3)
                    AND ratecode.endperiode GE bill-date NO-LOCK NO-ERROR.
                IF AVAILABLE ratecode THEN
                DO:
                    ratecode-exist = YES.
                    LEAVE.
                END.
            END.
        END.        
        ELSE /* static ratecode */
        DO:
            FIND FIRST ratecode WHERE ratecode.CODE = guest-pr.CODE
                AND ratecode.endperiode GE bill-date NO-LOCK NO-ERROR.
            IF AVAILABLE ratecode THEN
            DO:
                ratecode-exist = YES.
                LEAVE.
            END.
        END.

        FIND NEXT guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK NO-ERROR.
    END.
    IF NOT ratecode-exist THEN
    DO:
        msg-str =  translateExtended ("Rate code not found or expired.",lvCAREA,"").
        error-flag = YES.
        RETURN.
    END.
END.

IF i-case = 1 THEN
DO:
  /*
  FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK,
    FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
    AND segment.betriebsnr = 4 NO-LOCK:
  */
  FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE guestseg:
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
        AND segment.betriebsnr = 4 NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
        IF guest.zahlungsart > 0 THEN 
        FOR EACH debitor WHERE debitor.gastnr = guest.gastnr 
          AND debitor.opart LE 1 NO-LOCK, 
          FIRST artikel WHERE artikel.artnr = debitor.artnr 
          AND artikel.departement = 0 
          AND (artikel.artart = 2 OR artikel.artart = 7) NO-LOCK: 
          outstand = outstand + debitor.saldo. 
        END. 
        
        FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
        IF htparam.fchar NE "" THEN 
        ASSIGN
          pswd-str = htparam.fchar
          msg-str =  translateExtended ("Black List:",lvCAREA,"")  
                  + " " + ENTRY(1, segment.bezeich, "$$0")
        .
        ELSE
        msg-str = "&Q"
              +  translateExtended ("Black List:",lvCAREA,"")  
              + " " + ENTRY(1, segment.bezeich, "$$0")
              + CHR(10)
              + translateExtended ("Cancel Booking?", lvCAREA,"").
        RETURN.
    END.
    
    FIND NEXT guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK NO-ERROR.
  END.

  IF guest.kreditlimit GT 0 AND guest.zahlungsart > 0 THEN 
  DO: 
    FOR EACH debitor WHERE debitor.gastnr = guest.gastnr 
      AND debitor.opart LE 1 NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = debitor.artnr 
      AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK: 
      outstand = outstand + debitor.saldo. 
    END. 
    IF outstand GT guest.kreditlimit THEN 
    DO: 
      FIND FIRST htparam WHERE paramnr = 320 NO-LOCK. 
      IF htparam.flogical THEN           
      DO: 
        msg-str = translateExtended ("Credit Limit overdrawn:",lvCAREA,"") 
                + " " + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) 
                + " >> " + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9")). 
        /*FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
        pswd-str = htparam.fchar.*/
        RETURN.
      END. 
      ELSE 
      DO: 
        msg-str = "&Q"
                + translateExtended ("Credit Limit overdrawn:",lvCAREA,"") 
                + " " + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) 
                + " >> " + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9")) 
                + CHR(10)
                + translateExtended ("Cancel creating new reservation?", lvCAREA,"").
        RETURN.
      END. 
    END. 
  END. 
END.

error-flag = NO.
RUN get-NewResNo(OUTPUT resNo).
CREATE reservation. 
ASSIGN 
    reservation.resnr      = resNo 
    reservation.gastnr     = gastnr 
    reservation.gastnrherk = gastnr 
    reservation.name       = guest.name
    reservation.herkunft   = guest.name + ", " + guest.vorname1 
                           + guest.anredefirma     
. 
FIND CURRENT reservation NO-LOCK. 
RELEASE reservation.

PROCEDURE get-NewResNo:
DEF OUTPUT PARAMETER resNo AS INTEGER.
DEF BUFFER rline FOR res-line.    
    FIND FIRST htparam WHERE htparam.paramnr = 736 NO-LOCK.
    IF htparam.fchar NE "" THEN RUN VALUE(htparam.fchar) (OUTPUT resNo).
    ELSE
    DO:
      FIND FIRST reservation NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reservation THEN resNo = 1. 
      ELSE resNo = reservation.resnr + 1. 
    END.
    FOR EACH rline NO-LOCK BY rline.resnr DESCENDING:
      IF resNo LE rline.resnr THEN resNo = rline.resnr + 1.
      LEAVE.
    END.
END.

