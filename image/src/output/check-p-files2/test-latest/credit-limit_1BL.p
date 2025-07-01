DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS CHAR FORMAT "x(2)" LABEL "" 
  FIELD rechnr     LIKE bill.rechnr 
  FIELD zinr       LIKE res-line.zinr 
  FIELD receiver   LIKE bill.name FORMAT "x(30)" COLUMN-LABEL "Bill Receiver" 
  FIELD ankunft    LIKE res-line.ankunft INITIAL ? 
  FIELD abreise    LIKE res-line.abreise INITIAL ? 
  FIELD c-limit    LIKE guest.kreditlimit 
  FIELD saldo      LIKE bill.saldo FORMAT "->>>,>>>,>>>,>>9.99" 
  FIELD name       LIKE res-line.name FORMAT "x(29)" 
  FIELD resnr      LIKE res-line.resnr

  /*for soAsia*/
  FIELD comp-name  LIKE guest.NAME
  FIELD rmrate     LIKE res-line.zipreis
  FIELD rate-code  AS CHAR
  FIELD argt-code  AS CHAR
  FIELD pay-type   AS CHAR
  FIELD over       AS DECIMAL
  FIELD remark     AS CHAR
  FIELD stafid     AS CHAR
  . 

DEFINE INPUT PARAMETER incl-master      AS LOGICAL.     
DEFINE INPUT PARAMETER by-room          AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.

DEFINE VARIABLE saldo                   AS DECIMAL. 
DEFINE VARIABLE climit                  AS INTEGER. 
DEFINE VARIABLE g-climit LIKE guest.kreditlimit. 

DEFINE VARIABLE loopi   AS INTEGER.
DEFINE VARIABLE str     AS CHAR.

DEFINE BUFFER bguest FOR guest.

FIND FIRST htparam WHERE htparam.paramnr = 68 NO-LOCK. 
IF vhp.htparam.fdecimal NE 0 THEN g-climit = vhp.htparam.fdecimal. 
ELSE g-climit = vhp.htparam.finteger. 

FOR EACH cl-list: 
delete cl-list. 
END. 

FOR EACH bill WHERE bill.flag = 0 AND bill.resnr = 0 
    NO-LOCK BY bill.name: 
    FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE guest AND 
        guest.kreditlimit GT 0 THEN climit = guest.kreditlimit. 
    ELSE climit = g-climit. 
    IF bill.saldo GT climit THEN 
    DO: 
      CREATE cl-list.
      ASSIGN
          cl-list.flag      = "NS"
          cl-list.name      = bill.NAME
          cl-list.receiver  = bill.name 
          cl-list.c-limit   = climit 
          cl-list.rechnr    = bill.rechnr 
          cl-list.saldo     = bill.saldo 
          cl-list.ankunft   = ?
          cl-list.abreise   = ?
          cl-list.comp-name = guest.NAME
          cl-list.rmrate    = 0
          cl-list.rate-code = " "
          cl-list.argt-code = " "
          cl-list.pay-type  = " "
          cl-list.over      = bill.saldo - climit
          cl-list.remark    = " "
          cl-list.stafid    = " ". 
    END. 
END. 

IF incl-master THEN 
FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
    AND bill.zinr = "" NO-LOCK BY bill.name: 
    FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE guest AND 
        guest.kreditlimit GT 0 THEN climit = guest.kreditlimit. 
    ELSE climit = g-climit. 
    IF bill.saldo GT climit THEN 
    DO: 
      FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.reslinnr = 1 NO-LOCK NO-ERROR. 
      CREATE cl-list. 
      cl-list.flag      = "M". 
      cl-list.name      = bill.name. 
      cl-list.receiver  = bill.name. 
      cl-list.c-limit   = climit. 
      cl-list.rechnr    = bill.rechnr. 
      cl-list.saldo     = bill.saldo. 
      IF AVAILABLE res-line THEN 
      DO: 
        ASSIGN
            cl-list.ankunft   = res-line.ankunft 
            cl-list.abreise   = res-line.abreise 
            cl-list.rmrate    = res-line.zipreis
            cl-list.over      = bill.saldo - climit
            cl-list.remark    = " "
            cl-list.stafid    = " ". 
        
        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN ASSIGN cl-list.comp-name = guest.NAME.

        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN cl-list.argt-code = arrangement.argt-bez.
        
        IF res-line.code NE "" AND res-line.CODE NE "0" THEN DO: 
            FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy THEN ASSIGN cl-list.pay-type  = queasy.char1.
        END.  

        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN DO:
                cl-list.rate-code  = SUBSTR(str,7).
                LEAVE.
            END.
        END.

      END.       
    END. 
END. 

IF NOT by-room THEN 
FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
    AND bill.zinr NE "" NO-LOCK BY bill.name: 
    FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE guest AND 
        guest.kreditlimit GT 0 THEN climit = guest.kreditlimit. 
    ELSE climit = g-climit. 
    IF bill.saldo GT climit THEN 
    DO: 
      FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.reslinnr = bill.reslinnr NO-LOCK. 
      CREATE cl-list. 
      ASSIGN
          cl-list.zinr      = bill.zinr
          cl-list.resnr     = bill.resnr 
          cl-list.receiver  = guest.name + ", " + guest.vorname1 + " " 
            + guest.anrede1 + guest.anredefirma 
          cl-list.c-limit   = climit
          cl-list.rechnr    = bill.rechnr 
          cl-list.saldo     = bill.saldo 
          cl-list.ankunft   = res-line.ankunft 
          cl-list.abreise   = res-line.abreise.

      IF AVAILABLE res-line THEN DO:
       ASSIGN
            cl-list.name      = res-line.NAME
            cl-list.rmrate    = res-line.zipreis
            cl-list.over      = bill.saldo - climit
            cl-list.remark    = " "
            cl-list.stafid    = " ". 
        
        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN ASSIGN cl-list.comp-name = guest.NAME.

        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN cl-list.argt-code = arrangement.argt-bez.
        
        IF res-line.code NE "" AND res-line.CODE NE "0" THEN DO: 
            FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy THEN ASSIGN cl-list.pay-type  = queasy.char1.
        END.  

        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN DO:
                cl-list.rate-code  = SUBSTR(str,7).
                LEAVE.
            END.
        END.
      END.

    END. 
END. 
ELSE 
FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 
    AND bill.zinr NE "" NO-LOCK BY INTEGER(bill.zinr) BY bill.name: 
    FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE guest AND 
        guest.kreditlimit GT 0 THEN climit = guest.kreditlimit. 
    ELSE climit = g-climit. 
    IF bill.saldo GT climit THEN 
    DO: 
      FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.reslinnr = bill.reslinnr NO-LOCK. 
      CREATE cl-list. 
      ASSIGN
          cl-list.zinr      = bill.zinr
          cl-list.resnr     = bill.resnr 
          cl-list.receiver  = guest.name + ", " + guest.vorname1 + " " 
            + guest.anrede1 + guest.anredefirma
          cl-list.c-limit   = climit 
          cl-list.rechnr    = bill.rechnr 
          cl-list.saldo     = bill.saldo
          cl-list.ankunft   = res-line.ankunft
          cl-list.abreise   = res-line.abreise. 
      IF AVAILABLE res-line THEN DO:

        ASSIGN
            cl-list.name      = res-line.NAME
            cl-list.rmrate    = res-line.zipreis
            cl-list.over      = bill.saldo - climit
            cl-list.remark    = " "
            cl-list.stafid    = " ". 
        
        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE bguest THEN ASSIGN cl-list.comp-name = guest.NAME.

        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN cl-list.argt-code = arrangement.argt-bez.
        
        IF res-line.code NE "" AND res-line.CODE NE "0" THEN DO: 
            FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
            IF AVAILABLE queasy THEN ASSIGN cl-list.pay-type  = queasy.char1.
        END.  

        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN DO:
                cl-list.rate-code  = SUBSTR(str,7).
                LEAVE.
            END.
        END.
      END.
    END. 
END. 
 
  
