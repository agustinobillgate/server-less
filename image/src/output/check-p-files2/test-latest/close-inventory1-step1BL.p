
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inv-type AS INT.
DEF INPUT PARAMETER m-endkum AS INT.
DEF INPUT PARAMETER begindate AS DATE.
DEF INPUT PARAMETER closedate AS DATE.

DEF OUTPUT PARAMETER t-its-ok AS LOGICAL.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER msg-str2 AS CHAR.
/*MTDEF OUTPUT PARAMETER curr-anz AS INT.*/

DEF VAR its-ok AS LOGICAL.
DEFINE VARIABLE anzahl AS DECIMAL.

{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "close-inventory". 

RUN create-lbesthis.

RUN close-onhand. 
RUN check-onhand(OUTPUT its-ok). 
t-its-ok = its-ok.

PROCEDURE create-lbesthis:
DEF BUFFER lart FOR l-artikel.
    FOR EACH l-bestand NO-LOCK BY l-bestand.artnr:
      IF NOT AVAILABLE lart THEN
        FIND FIRST lart WHERE lart.artnr = l-bestand.artnr NO-LOCK.
      ELSE IF AVAILABLE lart AND lart.artnr NE l-bestand.artnr THEN
        FIND FIRST lart WHERE lart.artnr = l-bestand.artnr NO-LOCK.
      IF (inv-type = 1 AND lart.endkum LT m-endkum) OR 
         (inv-type = 2 AND lart.endkum GE m-endkum) OR 
         (inv-type = 3) THEN 
      DO:
          FIND FIRST vhp.l-besthis EXCLUSIVE-LOCK WHERE
            vhp.l-besthis.anf-best-dat  = begindate AND
            vhp.l-besthis.lager-nr      = l-bestand.lager-nr AND
            vhp.l-besthis.artnr         = l-bestand.artnr NO-ERROR.
          IF NOT AVAILABLE vhp.l-besthis THEN CREATE vhp.l-besthis.
          BUFFER-COPY l-bestand EXCEPT l-bestand.anf-best-dat TO vhp.l-besthis.
          ASSIGN vhp.l-besthis.anf-best-dat = begindate.
          FIND CURRENT vhp.l-besthis NO-LOCK.
          RELEASE vhp.l-besthis.
      END.
    END.
END.


PROCEDURE close-onhand: 
DEFINE BUFFER l-onhand FOR l-bestand. 
DEFINE VARIABLE t-qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL FORMAT "->>>,>>>,>>9.999999". 
  /*MTcurr-anz = 0.*/
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 
    AND (l-bestand.anf-best-dat LE closedate 
    OR l-bestand.anf-best-dat = ?
    OR l-bestand.anf-best-dat GE closedate) NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE l-bestand: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
      NO-ERROR. 
    IF NOT AVAILABLE l-artikel THEN 
    DO:
      msg-str2 = msg-str2 + CHR(2) + "&W"
               + translateExtended ("Article not found for stock onhand",lvCAREA,"") + " "
               + STRING(l-bestand.artnr,"9999999").
    END. 
    ELSE IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO:
      /** total qty AND onhand value (see sall-onhand.p) **/ 
      t-qty = l-bestand.anz-anf-best + l-bestand.anz-eingang 
        - l-bestand.anz-ausgang. 
      wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
        - l-bestand.wert-ausgang. 
 
      RUN close-onhand2(l-bestand.artnr, t-qty, wert, OUTPUT anzahl). 
 
      FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
      l-bestand.anz-anf-best = anzahl. 
      l-bestand.val-anf-best = wert. 
      l-bestand.anz-eingang = 0. 
      l-bestand.wert-eingang = 0. 
      l-bestand.anz-ausgang = 0. 
      l-bestand.wert-ausgang = 0. 
      l-bestand.anf-best-dat = closedate + 1. 
      FIND CURRENT l-bestand NO-LOCK. 
 
/** UPDATE average price **/ 
      IF anzahl NE 0 THEN 
      DO: 
        avrg-price = wert / anzahl. 
        FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN
        DO:
          l-artikel.vk-preis = avrg-price. 
          FIND CURRENT l-artikel NO-LOCK. 
        END.
      END.
    END. 
    FIND NEXT l-bestand WHERE l-bestand.lager-nr = 0 
      AND (l-bestand.anf-best-dat LE closedate 
      OR l-bestand.anf-best-dat = ?
      OR l-bestand.anf-best-dat GE closedate) NO-LOCK NO-ERROR. 
  END. 
END. 


PROCEDURE check-onhand: 
DEFINE OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 
    AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
    NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE l-bestand: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO:
      msg-str = msg-str + CHR(2)
              + translateExtended ("Not updated Stock Onhand found for article :",lvCAREA,"")
              + CHR(10)
              + STRING(l-artikel.artnr) + " - " + l-artikel.bezeich 
              + CHR(10)
              + translateExtended ("Last Closing Date = ",lvCAREA,"") 
              + STRING(l-bestand.anf-best-dat)
              + CHR(10)
              + translateExtended ("Fix the possible errors, then restart the program.",lvCAREA,"").
      its-ok = NO. 
      RETURN. 
    END. 
    FIND NEXT l-bestand WHERE l-bestand.lager-nr = 0 
      AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
      NO-LOCK NO-ERROR. 
  END. 
END. 


PROCEDURE close-onhand2: 
DEFINE INPUT PARAMETER artnr AS INTEGER. 
DEFINE INPUT PARAMETER t-qty AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE INPUT PARAMETER t-wert AS DECIMAL. 
DEFINE OUTPUT PARAMETER t-anz AS DECIMAL FORMAT "->,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE BUFFER l-onhand FOR l-bestand. 
DEFINE BUFFER store FOR l-lager. 
 
  FOR EACH store NO-LOCK: 
    FIND FIRST l-onhand WHERE l-onhand.artnr = artnr 
      AND l-onhand.lager-nr = store.lager-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-onhand THEN 
    DO: 
      anzahl = (l-onhand.anz-anf-best + l-onhand.anz-eingang 
        - l-onhand.anz-ausgang). 
      t-anz = t-anz + anzahl. 
      IF t-qty NE 0 THEN wert = t-wert * anzahl / t-qty. 
      ELSE wert = 0. 
      
      FIND CURRENT l-onhand EXCLUSIVE-LOCK. 
      l-onhand.anz-anf-best = anzahl. 
      l-onhand.val-anf-best = wert. 
      l-onhand.anz-eingang = 0. 
      l-onhand.wert-eingang = 0. 
      l-onhand.anz-ausgang = 0. 
      l-onhand.wert-ausgang = 0. 
      l-onhand.anf-best-dat = closedate + 1. 
      FIND CURRENT l-onhand NO-LOCK. 
    END. 
  END. 
END. 
