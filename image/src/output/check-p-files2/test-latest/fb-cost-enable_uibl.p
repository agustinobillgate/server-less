  
DEFINE TEMP-TABLE grid-list  
    FIELD artnr           AS INTEGER   FORMAT ">>>>9"         COLUMN-LABEL "ArtNo"   
    FIELD subgroup        AS INTEGER   FORMAT ">>9"           COLUMN-LABEL "SubGroup"  
    FIELD bezeich         AS CHARACTER FORMAT "x(24)"         COLUMN-LABEL "Description"  
    FIELD artnrrezept     AS INTEGER   FORMAT ">>>,>>9"       COLUMN-LABEL "RecipeNo"  
    FIELD unitprice       AS DECIMAL   FORMAT ">>,>>>,>>9.99" COLUMN-LABEL "UnitPrice"  
    FIELD recipecost      AS DECIMAL   FORMAT ">,>>>,>>9.99"  COLUMN-LABEL "RecipeCost"  
    FIELD cpercentage     AS DECIMAL   FORMAT ">>9.99"        COLUMN-LABEL "Cost(%)"  
    FIELD recomcost       AS DECIMAL   FORMAT ">>9.99"        COLUMN-LABEL "Recom(%)"  
    FIELD recomprice      AS DECIMAL   FORMAT ">,>>>,>>9.99"  COLUMN-LABEL "RecomPrice"  
    FIELD next_unit_price AS DECIMAL   FORMAT ">,>>>,>>9.99"  COLUMN-LABEL "NextPrice"  
    FIELD Next_2nd_price  AS DECIMAL   FORMAT ">,>>>,>>9.99"  COLUMN-LABEL "2nd Price"  
    FIELD changeddate     AS DATE      FORMAT "99/99/99"      COLUMN-LABEL "ChgDate"   
    FIELD users           AS CHARACTER FORMAT "x(32)"         COLUMN-LABEL "User".  
  
DEF INPUT  PARAMETER sorttype AS INT.  
DEF INPUT  PARAMETER dept AS INT.  
DEF INPUT  PARAMETER price-type AS INT.  
DEF OUTPUT PARAMETER d-bezeich AS CHAR.  
DEF OUTPUT PARAMETER double-currency AS LOGICAL.  
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.  
DEF OUTPUT PARAMETER amount AS DECIMAL.  
DEF OUTPUT PARAMETER TABLE FOR grid-list.  
  
  
FIND FIRST hoteldpt WHERE hoteldpt.num = dept NO-LOCK.  
d-bezeich = hoteldpt.depart.  
  
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK NO-ERROR.   
IF AVAILABLE htparam THEN double-currency = htparam.flogical.   
IF double-currency THEN   
DO:   
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK.   
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.   
    IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.   
END.   
  
RUN fb-cost-fill-grid-listbl.p  
    (double-currency, sorttype, dept, exchg-rate, price-type,  
     OUTPUT amount, OUTPUT TABLE grid-list).  
