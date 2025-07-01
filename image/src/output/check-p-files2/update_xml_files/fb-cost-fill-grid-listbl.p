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
  
DEF INPUT  PARAMETER double-currency AS LOGICAL.  
DEF INPUT  PARAMETER sorttype        AS INT.  
DEF INPUT  PARAMETER dept            AS INT.  
DEF INPUT  PARAMETER exchg-rate      AS DECIMAL.  
DEF INPUT  PARAMETER price-type      AS INT.  
DEF OUTPUT PARAMETER amount          AS DECIMAL.  
DEF OUTPUT PARAMETER TABLE FOR grid-list.  
  
IF sorttype = 3 THEN DO:  
     
  FOR EACH h-artikel WHERE h-artikel.departement = dept   
      NO-LOCK BY h-artikel.artnr:  
      CREATE grid-list.  
      ASSIGN   
       grid-list.artnr = h-artikel.artnr  
       grid-list.artnrrezept = h-artikel.artnrrezept  
       grid-list.subgroup = h-artikel.zwkum  
       grid-list.bezeich  = h-artikel.bezeich  
       grid-list.unitprice = h-artikel.epreis1  
       grid-list.recipecost = 0  
      .  
    IF double-currency THEN   
          grid-list.unitprice = grid-list.unitprice * exchg-rate.  
  
    amount = 0.  
     RUN count-recipe-cost.  
     RUN count-cost-percentage.  
  
     FIND FIRST queasy WHERE KEY = 142 AND grid-list.artnr = queasy.number1 AND dept = queasy.number2 NO-LOCK NO-ERROR. /*DODY 120716 add dept*/ 
     IF AVAIL queasy THEN DO:  
         ASSIGN  
           grid-list.NEXT_unit_price = queasy.deci1  
           grid-list.Next_2nd_price = queasy.deci2  
           grid-list.changeddate = queasy.date1   
           grid-list.USERs = queasy.char2.    
     END.  
    END.      
END.  
ELSE IF sorttype = 2 THEN DO:  
    
   FOR EACH h-artikel WHERE h-artikel.departement = dept AND h-artikel.artnrrezept NE 0 NO-LOCK BY h-artikel.artnr:  
      
    CREATE grid-list.  
     ASSIGN   
     grid-list.artnr = h-artikel.artnr  
     grid-list.artnrrezept = h-artikel.artnrrezept  
     grid-list.subgroup = h-artikel.zwkum  
     grid-list.bezeich  = h-artikel.bezeich  
     grid-list.unitprice = h-artikel.epreis1  
     grid-list.recipecost = 0  
    .  
     IF double-currency THEN   
         grid-list.unitprice = grid-list.unitprice * exchg-rate.  
      
    amount = 0.  
    RUN count-recipe-cost.  
    RUN count-cost-percentage.  
      
    FIND FIRST queasy WHERE KEY = 142 AND grid-list.artnr = queasy.number1 AND dept = queasy.number2 NO-LOCK NO-ERROR.  /*DODY 120716 add dept*/ 
    IF AVAIL queasy THEN DO:  
     ASSIGN  
      grid-list.NEXT_unit_price = queasy.deci1  
      grid-list.Next_2nd_price = queasy.deci2  
      grid-list.changeddate = queasy.date1  
      grid-list.USERs = queasy.char2.    
    END.  
   END.      
END.  
ELSE DO:  
    FOR EACH h-artikel WHERE h-artikel.departement = dept AND h-artikel.artnrrezept = 0 NO-LOCK BY h-artikel.artnr:  
    CREATE grid-list.  
     ASSIGN   
       grid-list.artnr = h-artikel.artnr  
       grid-list.artnrrezept = h-artikel.artnrrezept  
       grid-list.subgroup = h-artikel.zwkum  
       grid-list.bezeich  = h-artikel.bezeich  
       grid-list.unitprice = h-artikel.epreis1  
       grid-list.recipecost = 0  
       grid-list.cpercentage = 0  
     .  
     IF double-currency THEN   
         grid-list.unitprice = grid-list.unitprice * exchg-rate.  
  
     FIND FIRST queasy WHERE KEY = 142 AND grid-list.artnr = queasy.number1 AND dept = queasy.number2 /*DODY 120716 add dept*/ 
         NO-LOCK NO-ERROR.  
     IF AVAIL queasy THEN DO:  
         ASSIGN  
             grid-list.NEXT_unit_price = queasy.deci1  
             grid-list.Next_2nd_price = queasy.deci2  
             grid-list.changeddate = queasy.date1  
             grid-list.USERs = queasy.char2.    
     END.  
   END.      
END.  
  
  
PROCEDURE count-recipe-cost:  
  
  RUN fb-cost-count-recipe-costbl.p  
      (grid-list.artnrrezept, price-type, INPUT-OUTPUT amount).  
  grid-list.recipecost = amount.  
    
END.  
  
PROCEDURE count-cost-percentage:  
    /* Rd, pisah perhitungan pct, #368, 12-Des-24 */
    /* grid-list.cpercentage = grid-list.recipecost / grid-list.unitprice * 100.  */
    DEF VAR tmp-pct AS DECIMAL INIT 0.
    
    IF grid-list.unitprice > 0 THEN 
    DO:
        tmp-pct = grid-list.recipecost / grid-list.unitprice.
    END.
    grid-list.cpercentage = tmp-pct * 100.  
END.  
