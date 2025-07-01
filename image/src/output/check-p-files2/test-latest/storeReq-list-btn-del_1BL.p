DEFINE TEMP-TABLE t-list 
  FIELD s-recid     AS INTEGER
  FIELD t-status    AS INTEGER
  FIELD datum       AS DATE 
  FIELD deptNo      AS INTEGER
  FIELD lager-nr    AS INTEGER
  FIELD to-stock    AS INTEGER
  FIELD anzahl      AS DECIMAL
  FIELD einzelpreis AS DECIMAL
  FIELD warenwert   AS DECIMAL
  FIELD deptName    AS CHAR FORMAT "x(24)"
  FIELD lscheinnr   AS CHAR FORMAT "x(11)" 
  FIELD f-bezeich   AS CHAR FORMAT "x(16)" 
  FIELD t-bezeich   AS CHAR FORMAT "x(16)" 
  FIELD artnr       AS CHAR FORMAT "x(7)" 
  FIELD bezeich     AS CHAR FORMAT "x(24)" 
  FIELD einheit     AS CHAR FORMAT "x(3)" 
  FIELD content     AS DECIMAL FORMAT ">>>,>>>" 
  FIELD price       AS CHAR FORMAT "x(13)" 
  FIELD qty         AS DECIMAL FORMAT ">>>,>>9.999" 
  FIELD qty1        AS DECIMAL FORMAT ">>>,>>9.999" 
  FIELD val         AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
  FIELD fibukonto   AS CHAR FORMAT "x(12)" LABEL "AcctNo"
  FIELD ID          AS CHAR FORMAT "x(4)"
  FIELD appStr      AS CHAR FORMAT "x(3)" LABEL "APP" INIT ""
  FIELD appFlag     AS LOGICAL INIT NO

  FIELD stornogrund AS CHARACTER
  FIELD gl-bezeich  AS CHARACTER
  FIELD art-bezeich AS CHARACTER
  FIELD art-lief-einheit AS INT
  FIELD art-traubensort  AS CHAR
  FIELD zwkum            LIKE l-artikel.zwkum
  FIELD endkum           LIKE l-artikel.endkum
  FIELD centername       AS CHAR
. 
  
DEF INPUT PARAMETER t-list-s-recid AS INT.  
DEF INPUT PARAMETER bediener-nr    AS INT.  
  
DEF INPUT PARAMETER from-date AS DATE.  
DEF INPUT PARAMETER to-date AS DATE.  
DEF INPUT PARAMETER from-dept AS INT.  
DEF INPUT PARAMETER to-dept AS INT.  
DEF INPUT PARAMETER curr-lschein AS CHAR.  
DEF INPUT PARAMETER show-price AS LOGICAL.  
  
DEF OUTPUT PARAMETER it-exist AS LOGICAL.  
DEF OUTPUT PARAMETER TABLE FOR t-list.  

/* Malik Serverless 681 Comment 
FIND FIRST l-op WHERE RECID(l-op) = t-list-s-recid.  
ASSIGN   
    l-op.loeschflag = 2  
    l-op.fuellflag  = bediener-nr.  */

/* Malik Serverless 681 update l-op */
FIND FIRST l-op WHERE RECID(l-op) = t-list-s-recid NO-LOCK NO-ERROR.
IF AVAILABLE l-op THEN
DO:
  FIND CURRENT l-op EXCLUSIVE-LOCK.
  ASSIGN   
    l-op.loeschflag = 2  
    l-op.fuellflag  = bediener-nr. 
  FIND CURRENT l-op NO-LOCK.
  RELEASE l-op.
END.
  
RUN storereq-list-create-list_1bl.p  
    (from-date, to-date, from-dept, to-dept, curr-lschein, show-price,  
     OUTPUT it-exist, OUTPUT TABLE t-list).  
