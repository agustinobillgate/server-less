DEFINE TEMP-TABLE output-list 
  FIELD l-bezeich AS CHAR FORMAT "x(24)" LABEL "Store Name" 
  FIELD STR AS CHAR. 
                                                        
DEFINE INPUT PARAMETER s-artnr          AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER price-decimal   AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER artnr           AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER bezeich         AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

    
DEFINE VARIABLE long-digit AS LOGICAL. 
MESSAGE s-artnr VIEW-AS ALERT-BOX INFO.
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-artikel THEN
  RETURN.
ASSIGN artnr = STRING(l-artikel.artnr,"9999999")
       bezeich = l-artikel.bezeich. 

RUN soh-list. 

/**************************** PROCEDURES **************************************/ 
PROCEDURE soh-list: 
    DEFINE VARIABLE qty AS DECIMAL. 
    DEFINE VARIABLE val AS DECIMAL. 
    DEFINE VARIABLE t-init-qty AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-init-val AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-in-qty AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-in-val AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-out-qty AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-out-val AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-end-qty AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-end-val AS DECIMAL INITIAL 0. 
     
    DEFINE buffer l-oh FOR l-bestand. 
    DEFINE VARIABLE t-qty AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-wert AS DECIMAL INITIAL 0. 

    DEFINE VARIABLE adjust AS DECIMAL. 
    DEFINE VARIABLE value-in AS DECIMAL. 
    DEFINE VARIABLE value-out AS DECIMAL. 
     
    FIND FIRST l-oh WHERE l-oh.artnr = s-artnr 
        AND l-oh.lager-nr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-oh THEN 
    DO: 
        t-qty  = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
        t-wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
    END. 
    ELSE IF NOT AVAILABLE l-oh THEN
      RETURN.
    
    FOR EACH l-lager NO-LOCK, 
        FIRST l-bestand WHERE l-bestand.artnr = s-artnr 
        AND l-bestand.lager-nr = l-lager.lager-nr NO-LOCK :
        
        qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
        t-end-qty = t-end-qty + qty. 
        IF t-qty NE 0 THEN val = t-wert * qty / t-qty. 
        ELSE val = 0. 
        
        ASSIGN adjust = val - l-bestand.val-anf-best - l-bestand.wert-eingang +
                        l-bestand.wert-ausgang
               value-in  = l-bestand.wert-eingang
               value-out = l-bestand.wert-ausgang. 
        
        CREATE output-list. 
        output-list.l-bezeich = l-lager.bezeich. 
        STR = STRING(l-lager.lager-nr,"99"). 
        IF l-bestand.anf-best-dat NE ? THEN 
            STR = STR + STRING(l-bestand.anf-best-dat, "99/99/99"). 
        ELSE STR = STR + "        ". 

        IF long-digit THEN 
            STR = STR + STRING(l-bestand.anz-anf-best, "->,>>>,>>9.99") 
                + STRING(l-bestand.val-anf-best, "->,>>>,>>>,>>9") 
                + STRING(l-bestand.anz-eingang,  "->,>>>,>>9.99") 
                + STRING(value-in, "->,>>>,>>>,>>9") 
                + STRING(l-bestand.anz-ausgang,  "->,>>>,>>9.99") 
                + STRING(value-out, "->,>>>,>>>,>>9") 
                + STRING(adjust, " ->>>,>>>,>>9") 
                + STRING(qty, "->,>>>,>>9.99") 
                + STRING(val, "->,>>>,>>>,>>9"). 
        ELSE 
            STR = STR + STRING(l-bestand.anz-anf-best, "->,>>>,>>9.99") 
                + STRING(l-bestand.val-anf-best, "->>,>>>,>>9.99") 
                + STRING(l-bestand.anz-eingang,  "->,>>>,>>9.99") 
                + STRING(value-in, "->>,>>>,>>9.99") 
                + STRING(l-bestand.anz-ausgang,  "->,>>>,>>9.99") 
                + STRING(value-out, "->>,>>>,>>9.99") 
                + STRING(adjust, "->,>>>,>>9.99") 
                + STRING(qty, "->,>>>,>>9.99") 
                + STRING(val, "->>,>>>,>>9.99"). 
    END. 

    CREATE output-list. 
    IF long-digit THEN 
        STR = STRING("", "x(2)") 
            + STRING("TOTAL", "x(8)") 
            + STRING(l-oh.anz-anf-best, "->,>>>,>>9.99") 
            + STRING(l-oh.val-anf-best, "->,>>>,>>>,>>9") 
            + STRING(l-oh.anz-eingang,  "->,>>>,>>9.99") 
            + STRING(l-oh.wert-eingang,  "->,>>>,>>>,>>9") 
            + STRING(l-oh.anz-ausgang, "->,>>>,>>9.99") 
            + STRING(l-oh.wert-ausgang, "->,>>>,>>>,>>9") 
            + STRING(0, "->,>>>,>>9.99") 
            + STRING(t-qty, "->,>>>,>>9.99") 
            + STRING(t-wert, "->,>>>,>>>,>>9"). 
    ELSE 
        STR = STRING("", "x(2)") 
            + STRING("TOTAL", "x(8)") 
            + STRING(l-oh.anz-anf-best, "->,>>>,>>9.99") 
            + STRING(l-oh.val-anf-best, "->>,>>>,>>9.99") 
            + STRING(l-oh.anz-eingang,  "->,>>>,>>9.99") 
            + STRING(l-oh.wert-eingang,  "->>,>>>,>>9.99") 
            + STRING(l-oh.anz-ausgang, "->,>>>,>>9.99") 
            + STRING(l-oh.wert-ausgang, "->>,>>>,>>9.99") 
            + STRING(0, "->,>>>,>>9.99") 
            + STRING(t-qty, "->,>>>,>>9.99") 
            + STRING(t-wert, "->>,>>>,>>9.99"). 
END. 
