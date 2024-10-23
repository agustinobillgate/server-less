
DEF INPUT PARAMETER ap-recid AS INT.
DEF INPUT PARAMETER lief-nr  AS INT.
DEF INPUT PARAMETER bediener-nr AS INT.
DEF OUTPUT PARAMETER chr1 AS CHAR.
/*DEF VAR ap-recid AS INT INIT 118577.
DEF VAR lief-nr AS INT INIT 352.
DEF VAR bediener-nr AS INT INIT 1.
DEF VAR chr1 AS CHAR.*/

DEFINE BUFFER l-ap      FOR l-kredit. 
DEFINE BUFFER supplier  FOR l-lieferant.
DEFINE BUFFER suBuff    FOR l-lieferant.
DEFINE BUFFER opBuff    FOR l-op.

FIND FIRST l-kredit WHERE RECID(l-kredit) = ap-recid NO-LOCK. 
DO TRANSACTION: 

  FIND FIRST suBuff   WHERE suBuff.lief-nr   = l-kredit.lief-nr NO-LOCK.
  FIND FIRST supplier WHERE supplier.lief-nr = lief-nr NO-LOCK. 
  FOR EACH l-op NO-LOCK WHERE 
      l-op.lief-nr   = l-kredit.lief-nr AND
      l-op.datum     = l-kredit.rgdatum AND
      l-op.op-art    = 1                AND    
      l-op.docu-nr   = l-kredit.NAME    AND
      l-op.lscheinnr = l-kredit.lscheinnr:
      FIND FIRST opBuff WHERE RECID(opBuff) = RECID(l-op) EXCLUSIVE-LOCK.
      ASSIGN opBuff.lief-nr = lief-nr.
      FIND CURRENT opBuff NO-LOCK.
  END.
  FOR EACH l-op NO-LOCK WHERE 
      l-op.lief-nr   = l-kredit.lief-nr AND
      l-op.datum     = l-kredit.rgdatum AND
      l-op.op-art    = 3                AND    
      l-op.docu-nr   = l-kredit.NAME    AND
      l-op.lscheinnr = l-kredit.lscheinnr:
      FIND FIRST opBuff WHERE RECID(opBuff) = RECID(l-op) EXCLUSIVE-LOCK.
      ASSIGN opBuff.lief-nr = lief-nr.
      FIND CURRENT opBuff NO-LOCK.
  END.
  
  FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
  ASSIGN l-kredit.lief-nr = lief-nr. 
  FIND CURRENT l-kredit NO-LOCK. 
  
  IF l-kredit.counter NE 0 THEN 
  DO: 
    FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
      AND l-ap.opart GE 1 AND RECID(l-ap) NE RECID(l-kredit) EXCLUSIVE-LOCK: 
      l-ap.lief-nr = lief-nr. 
    END.
    RELEASE l-ap.
  END. 

  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr.
  chr1 = STRING(l-lieferant.firma, "x(26)").
  
  CREATE res-history. 
  ASSIGN 
    res-history.nr = bediener-nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.aenderung = "P/O " + l-kredit.NAME 
      + "; DeliveryNote " + l-kredit.lscheinnr
      + "; Change Supplier " + suBuff.firma 
      + " -> " + supplier.firma.
    res-history.action = "A/P". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 
END.

