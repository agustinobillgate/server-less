DEFINE TEMP-TABLE grid-list
  FIELD artnr       AS INTEGER FORMAT ">>>>9" COLUMN-LABEL "ArtNo" 
  FIELD subgroup    AS INTEGER FORMAT ">>9" COLUMN-LABEL "SubGroup"
  FIELD bezeich     AS CHARACTER FORMAT "x(24)" COLUMN-LABEL "Description"
  FIELD artnrrezept AS INTEGER FORMAT ">>>,>>9" COLUMN-LABEL "RecipeNo"
  FIELD unitprice   AS DECIMAL FORMAT ">>,>>>,>>9.99" COLUMN-LABEL "UnitPrice"
  FIELD recipecost  AS DECIMAL FORMAT ">,>>>,>>9.99" COLUMN-LABEL "RecipeCost"
  FIELD cpercentage AS DECIMAL FORMAT ">>9.99" COLUMN-LABEL "Cost(%)"
  FIELD recomcost   AS DECIMAL FORMAT ">>9.99" COLUMN-LABEL "Recom(%)"
  FIELD recomprice  AS DECIMAL FORMAT ">,>>>,>>9.99" COLUMN-LABEL "RecomPrice"
  FIELD next_unit_price AS DECIMAL FORMAT ">,>>>,>>9.99" COLUMN-LABEL "NextPrice"
  FIELD Next_2nd_price AS DECIMAL FORMAT ">,>>>,>>9.99" COLUMN-LABEL "2nd Price"
  FIELD changeddate AS DATE FORMAT "99/99/99"  COLUMN-LABEL "ChgDate" 
  FIELD users AS CHARACTER FORMAT "x(32)" COLUMN-LABEL "User".

DEF INPUT  PARAMETER price-list-artnr     AS INT.
DEF INPUT  PARAMETER price-list-deptnr    AS INT.
DEF INPUT  PARAMETER price-list-date1     AS DATE.
DEF INPUT  PARAMETER price-list-date2     AS DATE.
DEF INPUT  PARAMETER price-list-date3     AS DATE.
DEF INPUT  PARAMETER price-list-deci1     AS DECIMAL.
DEF INPUT  PARAMETER price-list-deci2     AS DECIMAL.
DEF INPUT  PARAMETER tp-bediener-username AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR grid-list.
 
FIND FIRST queasy WHERE KEY = 142 AND queasy.number1 = price-list-artnr
     AND queasy.number2 = price-list-deptnr 
     AND queasy.date1 = price-list-date1 AND queasy.deci1 = price-list-deci1
     AND queasy.deci2 = price-list-deci2 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN RETURN.
DO:
    FIND FIRST queasy WHERE KEY = 142 AND queasy.number1 = price-list-artnr /* Malik Serverless 372 */
        AND queasy.number2 = price-list-deptnr
        AND queasy.date1 = price-list-date1 NO-LOCK NO-ERROR. /* Malik Serverless 372 : EXCLUSIVE-LOCK NO-ERROR -> NO-LOCK NO-ERROR */
    IF AVAILABLE queasy THEN
    DO:
      FIND CURRENT queasy EXCLUSIVE-LOCK.
      DELETE queasy.
      RELEASE queasy.
    END.

    RUN fill-queasy.
    CREATE grid-list.
    ASSIGN
        grid-list.NEXT_unit_price = price-list-deci1
        grid-list.NEXT_2nd_price = price-list-deci2
        grid-list.changeddate = price-list-date1.
END. /*end else avail queasy*/

PROCEDURE fill-queasy:
    CREATE queasy.      
         ASSIGN
           queasy.KEY = 142
           queasy.number1 = price-list-artnr 
           queasy.number2 = price-list-deptnr 
           queasy.deci1   = price-list-deci1 
           queasy.deci2   = price-list-deci2 
           queasy.date1   = price-list-date1
           queasy.date2   = price-list-date2
           queasy.date3   = price-list-date3
           queasy.char2   = tp-bediener-username.
   /* END.*/
   CREATE grid-list.
   ASSIGN
       grid-list.NEXT_unit_price = queasy.deci1
       grid-list.Next_2nd_price = queasy.deci2
       grid-list.changeddate = queasy.date1
       grid-list.users = queasy.char2.
END.
