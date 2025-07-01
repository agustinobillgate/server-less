
DEFINE TEMP-TABLE t-p-list 
  FIELD rechnr       AS INTEGER 
  FIELD dept         AS INTEGER 
  FIELD billno       AS INTEGER 
  FIELD printed-line AS INTEGER 
  FIELD b-recid      AS INTEGER 
  FIELD last-amount  AS DECIMAL 
  FIELD last-famount AS DECIMAL. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR t-p-list.

DEF INPUT PARAMETER rec-id      AS INT.
DEF INPUT PARAMETER pax         AS INT.
DEF INPUT PARAMETER belegung    AS INT.

DEF BUFFER hbline FOR vhp.h-bill-line.
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
  IF pax NE belegung THEN 
  DO: 
    
    FIND FIRST hbline WHERE hbline.rechnr = vhp.h-bill.rechnr
        AND hbline.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.
    IF AVAILABLE hbline THEN
    DO:
      FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = 0
          AND vhp.h-umsatz.departement = vhp.h-bill.departement
          AND vhp.h-umsatz.betriebsnr = vhp.h-bill.departement
          AND vhp.h-umsatz.datum = hbline.bill-datum EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE vhp.h-umsatz THEN
      DO:
        ASSIGN vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl
            - vhp.h-bill.belegung + pax.
        FIND CURRENT vhp.h-umsatz NO-LOCK.
      END.
    END.
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE vhp.h-bill THEN 
    DO:
      vhp.h-bill.belegung = pax. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END.
    
  END. 
  RUN del-queasy. 

PROCEDURE del-queasy: 
/* number2: billrecid, deci2: billnr */ 
  FOR EACH vhp.queasy WHERE vhp.queasy.key = 4 
    AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100) 
    AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK: 
    delete vhp.queasy. 
  END. 
  RELEASE queasy.

  FOR EACH t-p-list WHERE t-p-list.rechnr = vhp.h-bill.rechnr 
    AND t-p-list.dept = vhp.h-bill.departement: 
    delete t-p-list.
  END. 
END. 

