  
  
DEFINE INPUT PARAMETER deltype      AS INTEGER.  
DEFINE INPUT PARAMETER sorttype     AS INTEGER.  
DEFINE INPUT PARAMETER adr1         AS CHAR.  
DEFINE INPUT PARAMETER city         AS CHAR.  
DEFINE INPUT PARAMETER cntry        AS CHAR.  
DEFINE INPUT PARAMETER email        AS CHAR.  
DEFINE INPUT PARAMETER last-stay    AS DATE.  
DEFINE INPUT PARAMETER min-sales    AS DECIMAL.  
DEFINE INPUT PARAMETER age-history  AS INTEGER.  
  
DEFINE OUTPUT PARAMETER f-anz       AS INTEGER.  
DEFINE OUTPUT PARAMETER d-anz       AS INTEGER.  
      
  
DEFINE VARIABLE error-code AS INTEGER.   
DEFINE VARIABLE last-history AS DATE.   
  
IF deltype EQ 1 THEN RUN del-deltype1.  
ELSE IF deltype EQ 2 THEN RUN del-deltype2.  
ELSE IF deltype EQ 3 THEN RUN del-deltype3.  
ELSE IF deltype EQ 4 THEN RUN del-deltype4.  
  
  
PROCEDURE del-deltype1:  
DEFINE VARIABLE i       AS INTEGER INITIAL 0    NO-UNDO.   
DEFINE VARIABLE do-it   AS LOGICAL              NO-UNDO.  
  FOR EACH guest WHERE guest.karteityp = sorttype AND guest.gastnr GT 0 NO-LOCK:   
    f-anz = f-anz + 1.   
    do-it = YES.  
    IF do-it AND adr1  NE "" AND guest.adresse1  NE adr1  THEN do-it = NO.  
    IF do-it AND city  NE "" AND guest.wohnort   NE city  THEN do-it = NO.  
    IF do-it AND cntry NE "" AND guest.land      NE cntry THEN do-it = NO.  
    IF do-it AND email NE "" AND guest.email-adr NE email THEN do-it = NO.  
    IF do-it AND guest.date2 GT last-stay                 THEN do-it = NO.  
    IF do-it AND guest.gesamtumsatz GT min-sales          THEN do-it = NO.  
    IF do-it AND age-history GT 0 THEN  
    DO:  
      FOR EACH history WHERE history.gastnr = guest.gastnr NO-LOCK  
        BY history.abreise DESCENDING:  
        IF history.abreise GT (TODAY - age-history * 365) THEN do-it = NO.  
        LEAVE.  
      END.  
    END.  
    IF do-it THEN  
    DO:   
      RUN del-gcfbl.p(guest.gastnr, OUTPUT error-code).   
      IF error-code = 0 THEN d-anz = d-anz + 1.   
    END.   
  END.   
  RETURN NO-APPLY.  
END.   
  
PROCEDURE del-deltype2:  
DEFINE VARIABLE i       AS INTEGER INITIAL 0    NO-UNDO.   
DEFINE VARIABLE do-it   AS LOGICAL              NO-UNDO.  
  FOR EACH guest WHERE guest.karteityp = sorttype AND guest.gastnr GT 0 NO-LOCK:   
    f-anz = f-anz + 1.   
    do-it = YES.  
    FIND FIRST history WHERE history.gastnr = guest.gastnr NO-LOCK NO-ERROR.  
    do-it = NOT AVAILABLE history.  
    IF do-it AND adr1  NE "" AND guest.adresse1 NE adr1   THEN do-it = NO.  
    IF do-it AND city  NE "" AND guest.wohnort   NE city  THEN do-it = NO.  
    IF do-it AND cntry NE "" AND guest.land      NE cntry THEN do-it = NO.  
    IF do-it AND email NE "" AND guest.email-adr NE email THEN do-it = NO.  
    IF do-it AND guest.date2 GT last-stay                 THEN do-it = NO.  
    IF do-it AND guest.gesamtumsatz GT min-sales          THEN do-it = NO.      
    IF do-it THEN  
    DO:   
      RUN del-gcfbl.p(guest.gastnr, OUTPUT error-code).   
      IF error-code = 0 THEN d-anz = d-anz + 1.   
    END.   
  END.   
  RETURN NO-APPLY.  
END.   
  
PROCEDURE del-deltype3:  
DEFINE VARIABLE i       AS INTEGER INITIAL 0    NO-UNDO.   
DEFINE VARIABLE do-it   AS LOGICAL              NO-UNDO.  
  FOR EACH guest WHERE guest.karteityp = sorttype AND guest.gastnr GT 0 NO-LOCK:   
    f-anz = f-anz + 1.   
    do-it = YES.  
    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK NO-ERROR.  
    do-it = NOT AVAILABLE guestseg.  
    IF do-it AND adr1  NE "" AND guest.adresse1 NE adr1   THEN do-it = NO.  
    IF do-it AND city  NE "" AND guest.wohnort   NE city  THEN do-it = NO.  
    IF do-it AND cntry NE "" AND guest.land      NE cntry THEN do-it = NO.  
    IF do-it AND email NE "" AND guest.email-adr NE email THEN do-it = NO.  
    IF do-it AND guest.date2 GT last-stay                 THEN do-it = NO.  
    IF do-it AND guest.gesamtumsatz GT min-sales          THEN do-it = NO.  
    IF do-it AND age-history GT 0 THEN  
    DO:  
      FOR EACH history WHERE history.gastnr = guest.gastnr NO-LOCK  
        BY history.abreise DESCENDING:  
        IF history.abreise GT (TODAY - age-history * 365) THEN do-it = NO.  
        LEAVE.  
      END.  
    END.  
    IF do-it THEN  
    DO:   
      RUN del-gcfbl.p(guest.gastnr, OUTPUT error-code).   
      IF error-code = 0 THEN d-anz = d-anz + 1.   
    END.   
  END.   
  RETURN NO-APPLY.  
END.   
  
PROCEDURE del-deltype4:  
DEF BUFFER hbuff FOR history.  
  last-history = DATE(month(today), day(today), (year(today) - age-history)).   
  FIND FIRST history WHERE history.gastnr GT 0 AND   
    history.abreise LT last-history NO-LOCK NO-ERROR.  
  DO WHILE AVAILABLE history:  
    f-anz = f-anz + 1.  
    FIND FIRST guest WHERE guest.gastnr = history.gastnr NO-LOCK NO-ERROR.  
    IF AVAILABLE guest AND guest.karteityp = sorttype THEN  
    DO TRANSACTION:  
      FIND FIRST hbuff WHERE RECID(hbuff) = RECID(history) EXCLUSIVE-LOCK.  
      DELETE hbuff.  
      RELEASE hbuff.  
      d-anz = d-anz + 1.  
    END.  
  END.   
  RETURN NO-APPLY.  
END.   
