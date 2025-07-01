
DEFINE TEMP-TABLE res-list 
  FIELD gastnr     AS INTEGER
  FIELD zinr       AS CHAR FORMAT "x(5)"  LABEL "RmNo" 
  FIELD name       AS CHAR FORMAT "x(36)" LABEL "Guest Name" 
  FIELD resnr      AS INTEGER
  FIELD reslinnr   AS INTEGER 
  FIELD activeflag AS INTEGER
  FIELD resstatus  AS INTEGER 
  FIELD sysdate    AS DATE 
  FIELD zeit       AS INTEGER
  FIELD selFlag    AS LOGICAL LABEL "Selected" INITIAL YES. 

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resnr          AS INTEGER.
DEF OUTPUT PARAMETER f-tittle       AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str1       AS CHAR.
DEF OUTPUT PARAMETER f-char         AS CHAR.
DEF OUTPUT PARAMETER guest-gastnr   LIKE guest.gastnr.
DEF OUTPUT PARAMETER guest-kreditlimit LIKE guest.kreditlimit.
DEF OUTPUT PARAMETER outstand       AS DECIMAL.
DEF OUTPUT PARAMETER f-logical      AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR res-list.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "prepare-auto-checkin".

DEFINE VARIABLE ci-date  AS DATE.

FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK. 
IF (reservation.depositgef - reservation.depositbez  - reservation.depositbez2) GT 0 THEN 
DO: 
   msg-str = msg-str + CHR(2)
           + translateExtended ("Deposit not yet settled, check-in not possible",lvCAREA,"").
   RETURN. 
END.

FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. 
IF guest.karteityp GE 1 AND guest.kreditlimit GT 0 AND guest.zahlungsart > 0 THEN 
DO: 
    outstand = 0.
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
        f-logical = YES.
        msg-str1 = msg-str1 + CHR(2)
                 + translateExtended ("Credit Limit overdrawn: ",lvCAREA,"")
                 + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) /*" >> " */
                 + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9")) .
        FIND FIRST htparam WHERE paramnr = 141 NO-LOCK.
        f-char = htparam.fchar.

        IF htparam.fchar NE "" THEN 
        DO:
            guest-gastnr = guest.gastnr.
            guest-kreditlimit = guest.kreditlimit.
        END.
      END. 
    END. 
END.


FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK.
f-tittle = translateExtended ("Automatic Checkin for :",lvCAREA,"") + reservation.name. 

RUN create-list.

PROCEDURE create-list:
  FOR EACH res-line WHERE res-line.resnr = resnr 
    AND res-line.active-flag = 0 AND res-line.l-zuordnung[3] = 0
    AND res-line.ankunft = ci-date NO-LOCK 
    BY res-line.zinr BY res-line.resstatus: 
    CREATE res-list. 
    ASSIGN  
      res-list.gastnr     = res-line.gastnr
      res-list.name       = res-line.NAME
      res-list.zinr       = res-line.zinr 
      res-list.resnr      = res-line.resnr
      res-list.reslinnr   = res-line.reslinnr
      res-list.activeflag = res-line.active-flag
      res-list.resstatus  = res-line.resstatus 
      res-list.sysdate    = TODAY
      res-list.zeit       = TIME
    .
  END.
  
END.
