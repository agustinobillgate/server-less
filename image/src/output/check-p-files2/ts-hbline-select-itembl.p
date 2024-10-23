
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER help-flag      AS LOGICAL.
DEF INPUT  PARAMETER art-list-artnr AS INT.

DEF OUTPUT PARAMETER info-str       AS CHAR.

DEFINE VARIABLE price   AS DECIMAL. 
DEFINE VARIABLE price2  AS DECIMAL. 
{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-hbline".


FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = art-list-artnr 
    AND vhp.h-artikel.departement = dept NO-LOCK.
IF help-flag THEN 
DO: 
    price  = vhp.h-artikel.epreis1.
    price2 = vhp.h-artikel.epreis2.
    IF price2 = 0 THEN
    DO:
      info-str = STRING(vhp.h-artikel.artnr) + " - " 
        + STRING(vhp.h-artikel.bezeich) + ": " 
        + translateExtended ("Price",lvCAREA, "") + " "
        + TRIM(STRING(price, ">,>>>,>>>,>>9.99")). 
    END.
    ELSE
    DO:
      info-str = STRING(vhp.h-artikel.artnr) + " - " 
        + STRING(vhp.h-artikel.bezeich) + ": " 
        + translateExtended ("Price",lvCAREA, "") + " "
        + TRIM(STRING(price, ">,>>>,>>>,>>9.99")) 
        + " [" + TRIM(STRING(price2, ">,>>>,>>>,>>9.99")) + "]". 
    END.
    RETURN. 
END. 
