DEF TEMP-TABLE r-list   
    FIELD max-n AS INTEGER INITIAL 0   
    FIELD recipe-nr AS INTEGER EXTENT 99 INITIAL 0.   
  
DEFINE TEMP-TABLE t-h-rezept  LIKE h-rezept  
    FIELD rec-id AS INT.  
DEFINE TEMP-TABLE t-l-artikel LIKE l-artikel.  
DEFINE TEMP-TABLE s-rezlin   
  FIELD h-recid     AS INTEGER   
  FIELD artnr       LIKE l-artikel.artnr                    COLUMN-LABEL "     ArtNo"   
  FIELD bezeich     AS CHAR FORMAT "x(36)"                  COLUMN-LABEL "Description"   
  FIELD masseinheit LIKE l-artikel.masseinheit              COLUMN-LABEL "Unit"   
  FIELD s-unit      AS CHAR FORMAT "x(8)"                   COLUMN-LABEL "R-Unit"  
  FIELD menge       LIKE h-rezlin.menge                     COLUMN-LABEL "Quantity"   
  FIELD cost        AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"    COLUMN-LABEL "Cost"   
  FIELD inhalt      AS DECIMAL FORMAT ">>>,>>9.99"          COLUMN-LABEL "Content"   
  FIELD vk-preis    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"    COLUMN-LABEL "Avrg Price"   
  FIELD lostfact    LIKE h-rezlin.lostfact   
  FIELD recipe-flag AS LOGICAL INITIAL NO.   
  
DEF INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER h-artnr AS INT.  
DEF INPUT PARAMETER DESCRIPTION AS CHAR.  
  
DEF OUTPUT PARAMETER h-bezeich AS CHAR.  
DEF OUTPUT PARAMETER katbezeich AS CHAR.  
DEF OUTPUT PARAMETER katnr AS INT.  
DEF OUTPUT PARAMETER portion AS INT.  
DEF OUTPUT PARAMETER price-type AS INT.  
DEF OUTPUT PARAMETER amount AS DECIMAL.  
DEF OUTPUT PARAMETER msg-str AS CHAR.  
DEF OUTPUT PARAMETER msg-str2 AS CHAR.  
DEF OUTPUT PARAMETER msg-str3 AS CHAR.  
DEF OUTPUT PARAMETER record-use AS LOGICAL INIT NO.  
DEF OUTPUT PARAMETER init-time AS INT.  
DEF OUTPUT PARAMETER init-date AS DATE.  
DEF OUTPUT PARAMETER TABLE FOR r-list.  
DEF OUTPUT PARAMETER TABLE FOR s-rezlin.  
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.  
DEF OUTPUT PARAMETER TABLE FOR t-h-rezept.  
  
DEF VAR curr-i AS INTEGER INITIAL 0 NO-UNDO.   
DEF VAR flag-ok AS LOGICAL.  
  
{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "chg-rezept".  


DEFINE BUFFER hrecipe  FOR h-rezept.
  
RUN check-timebl.p(1, h-artnr, ?, "h-rezept", ?, ?, OUTPUT flag-ok,  
                   OUTPUT init-time, OUTPUT init-date).  
IF NOT flag-ok THEN  
DO:  
    record-use = YES.  
    RETURN NO-APPLY.  
END.  
CREATE r-list.  
  
FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-artnr NO-LOCK.  
h-bezeich = SUBSTR(h-rezept.bezeich, 1, 24).   
katnr = h-rezept.kategorie.   
katbezeich = SUBSTR(h-rezept.bezeich, 25, 24).   
portion = h-rezept.portion.  
CREATE t-h-rezept.  
BUFFER-COPY h-rezept TO t-h-rezept.  
ASSIGN t-h-rezept.rec-id = RECID(h-rezept).  
   
FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK.   
price-type = htparam.finteger.   
  
FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = h-artnr NO-LOCK:   
  RUN create-rezlin.   
END.   
  
FOR EACH l-artikel:  
    CREATE t-l-artikel.  
    BUFFER-COPY l-artikel TO t-l-artikel.  
END.  
  
PROCEDURE create-rezlin:   
DEFINE VARIABLE cost AS DECIMAL.   
DEFINE buffer h-recipe FOR h-rezept.   
  CREATE s-rezlin.   
  ASSIGN  
    s-rezlin.h-recid = RECID(h-rezlin)  
    s-rezlin.artnr = h-rezlin.artnrlager   
    s-rezlin.bezeich = DESCRIPTION  
    s-rezlin.menge = h-rezlin.menge   
    s-rezlin.lostfact = h-rezlin.lostfact   
    s-rezlin.recipe-flag = h-rezlin.recipe-flag  
  .   
  IF h-rezlin.recipe-flag = NO THEN   
  DO:   
    FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK.  
    ASSIGN  
      s-rezlin.bezeich = l-artikel.bezeich  
      s-rezlin.masseinheit = STRING(l-artikel.masseinheit,"x(3)")  
      s-rezlin.s-unit = ENTRY(2, l-artikel.herkunft, ";")  
      s-rezlin.inhalt = l-artikel.inhalt  
    .  
    IF s-rezlin.s-unit = "" AND s-rezlin.inhalt = 1 THEN  
       s-rezlin.s-unit = s-rezlin.masseinheit.  
      
    IF price-type = 0 OR l-artikel.ek-aktuell = 0   
      THEN s-rezlin.vk-preis = l-artikel.vk-preis.   
    ELSE s-rezlin.vk-preis = l-artikel.ek-aktuell.   
    s-rezlin.lostfact = h-rezlin.lostfact.   
    IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN   
      s-rezlin.cost = h-rezlin.menge / l-artikel.inhalt * l-artikel.vk-preis   
       / (1 - h-rezlin.lostfact / 100).   
    ELSE s-rezlin.cost = h-rezlin.menge / l-artikel.inhalt * l-artikel.ek-aktuell   
       / (1 - h-rezlin.lostfact / 100).   
    IF s-rezlin.cost = 0 THEN   
    DO:   
        msg-str = msg-str + CHR(2)  
                + translateExtended ("Article content or price not yet defined: ", lvCAREA, "":U)  
                + CHR(10)  
                + STRING(l-artikel.artnr) + " - " + l-artikel.bezeich.  
    END.   
  END.   
  ELSE IF h-rezlin.recipe-flag = YES THEN   
  DO:   
      FIND FIRST h-recipe WHERE h-recipe.artnrrezept = h-rezlin.artnrlager NO-LOCK.   
      s-rezlin.bezeich = STRING(h-recipe.bezeich,"x(24)").   
      s-rezlin.recipe-flag = YES.   
      s-rezlin.inhalt = 1.   
      cost = 0.   
      RUN cal-cost(h-recipe.artnr, 1, INPUT-OUTPUT cost).
      /* s-rezlin.cost = h-rezlin.menge * cost. */
      s-rezlin.cost = (cost / h-recipe.portion) * h-rezlin.menge.  /* cost / h-recipe.portion. BLY - 2DF41C*/
      IF s-rezlin.cost = 0 THEN   
      DO:   
        msg-str2 = msg-str2 + CHR(2)  
                 + translateExtended ("Recipe cost = 0; cost calculation not possible:", lvCAREA, "":U)   
                 + CHR(10)  
                 + STRING(h-recipe.artnrrezept) + " - " + h-recipe.bezeich.  
    END.   
  END.   
  amount = amount + s-rezlin.cost.   
END.   
  
  
PROCEDURE cal-cost:   
DEFINE INPUT PARAMETER p-artnr AS INTEGER.   
DEFINE INPUT PARAMETER menge AS DECIMAL.   
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL.   
DEFINE VARIABLE inh AS DECIMAL.   
DEFINE BUFFER h-rezln FOR h-rezlin. 
DEFINE BUFFER hrecipe  FOR h-rezept.
DEF VAR i AS INTEGER NO-UNDO.   
   
    DO i = 1 TO curr-i:   
        IF r-list.recipe-nr[i] = p-artnr THEN   
        DO:   
            /*msg-str3 = msg-str3 + CHR(2)  
                     + translateExtended ("Wrong recursive definition in Recipe :",lvCAREA,"")   
                     + STRING(p-artnr).  
            RETURN.*/  
        END.   
    END.   
    curr-i = curr-i + 1.   
    r-list.recipe-nr[curr-i] = p-artnr.
   
  FOR EACH h-rezln WHERE h-rezln.artnrrezept = p-artnr NO-LOCK: 
    /*ITA 101116
    FIND FIRST hrecipe WHERE hrecipe.artnrrezept = p-artnr NO-LOCK NO-ERROR.
    IF hrecipe.portion GT 1 THEN DO:
        IF NOT h-rezln.recipe-flag THEN   
          inh = (menge * h-rezln.menge / (1 - h-rezln.lostfact / 100)) / hrecipe.portion.   
        ELSE inh = menge * h-rezlin.menge / hrecipe.portion. /* SY 25022016 / h-recipe.portion */.
    END.
    ELSE DO:
        IF NOT h-rezln.recipe-flag THEN   
          inh = menge * h-rezln.menge / (1 - h-rezln.lostfact / 100).   
        ELSE inh = menge * h-rezln.menge /* SY 25022016 / h-recipe.portion */. 
    END.*/

    

    IF NOT h-rezln.recipe-flag THEN DO:
        inh = menge * h-rezln.menge / (1 - h-rezln.lostfact / 100). 
    END.
    ELSE DO: 
        FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezln.artnrlager NO-LOCK NO-ERROR.
        IF hrecipe.portion GT 1 THEN
               ASSIGN inh = menge * h-rezln.menge / hrecipe.portion.
        ELSE inh = menge * h-rezln.menge /* SY 25022016 / h-recipe.portion */. 
    END.

    
    IF h-rezln.recipe-flag = YES THEN   
        RUN cal-cost(h-rezln.artnrlager, inh, INPUT-OUTPUT cost).   
    ELSE   
    DO:   
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezln.artnrlager NO-LOCK.   
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN   
        cost = cost + inh / l-artikel.inhalt * l-artikel.vk-preis.   
      ELSE cost = cost + inh / l-artikel.inhalt * l-artikel.ek-aktuell.   
    END.   
  END.   
END.  



