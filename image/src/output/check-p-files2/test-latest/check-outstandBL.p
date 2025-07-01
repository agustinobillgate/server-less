
DEF INPUT  PARAMETER pvILanguage    AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER gastnr         AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER from-inv       AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER error-flag     AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAMETER pswd-str       AS CHAR    INIT ""  NO-UNDO.
DEF OUTPUT PARAMETER outstand       AS DECIMAL INIT 0   NO-UNDO. 

DEF VAR black-list-flag AS LOGICAL INIT NO.
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "reservation". 

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK,
    FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
    AND segment.betriebsnr = 4 NO-LOCK:
  
    IF guest.zahlungsart > 0 THEN 
    FOR EACH debitor WHERE debitor.gastnr = guest.gastnr 
      AND debitor.opart LE 1 NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = debitor.artnr 
      AND artikel.departement = 0 
      AND (artikel.artart = 2 OR artikel.artart = 7) NO-LOCK: 
      outstand = outstand + debitor.saldo. 
    END. 

    black-list-flag = YES.
    LEAVE.
END.

IF guest.karteityp GE 1 AND guest.kreditlimit GT 0 
    AND guest.zahlungsart > 0 THEN 
DO: 
    FOR EACH debitor WHERE debitor.gastnr = guest.gastnr 
      AND debitor.opart LE 1 NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = debitor.artnr 
      AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK: 
      outstand = outstand + debitor.saldo. 
    END. 
    IF outstand GT guest.kreditlimit THEN 
    DO: 
        IF NOT from-inv THEN
        DO:
            IF black-list-flag THEN
            DO:
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
            END.
            ELSE
            DO:
                FIND FIRST htparam WHERE paramnr = 320 NO-LOCK. 
                IF htparam.flogical THEN           
                DO: 
                  msg-str = translateExtended ("Credit Limit overdrawn:",lvCAREA,"") 
                          + " " + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) 
                          + " >> " + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9")). 
                  FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
                  pswd-str = htparam.fchar.
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
        ELSE
        DO:
            msg-str = translateExtended ("Credit Limit overdrawn:",lvCAREA,"") 
                    + " " + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) 
                    + " >> " + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9")). 
            FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
            pswd-str = htparam.fchar.
            RETURN.
        END.
    END. 
END.
error-flag = NO.

