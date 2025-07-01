/*DEFINE TEMP-TABLE c-list 
  FIELD artnr LIKE l-artikel.artnr 
  FIELD bezeich AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit AS CHAR FORMAT "x(3)" COLUMN-LABEL "Unit" 
  FIELD inhalt AS DECIMAL FORMAT ">>>>9.99" COLUMN-LABEL "Content" 
  FIELD zwkum AS INTEGER 
  FIELD endkum AS INTEGER 
  FIELD qty AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1 AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation". */
  

DEFINE TEMP-TABLE c-list 
  /*FIELD artnr       AS CHAR FORMAT "x(11)"*/
  FIELD artnr       LIKE l-artikel.artnr
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Unit" 
  FIELD inhalt      AS CHAR FORMAT "x(8)" COLUMN-LABEL "Content" 
  FIELD zwkum       AS CHAR FORMAT "x(8)"
  FIELD endkum      AS INTEGER
  FIELD qty AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1 AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto   LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD avrg-price  AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "  Average Price" /*FD Jan 27, 20222*/
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation". 

DEFINE buffer c-list1 FOR c-list. 

DEF INPUT PARAMETER TABLE FOR c-list.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.    

FOR EACH c-list1 WHERE c-list1.qty NE c-list1.qty1 
    AND c-list1.fibukonto NE "0000000000" NO-LOCK: 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list1.fibukonto 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN 
    DO: 
      err-code = 1.
      RETURN.
    END. 
END. 
