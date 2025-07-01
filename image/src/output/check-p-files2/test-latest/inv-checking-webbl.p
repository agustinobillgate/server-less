
DEF TEMP-TABLE coa-list
    FIELD fibukonto AS CHAR
    FIELD datum     AS DATE 
    FIELD wert      AS DECIMAL 
    FIELD debit     AS DECIMAL
    FIELD credit    AS DECIMAL.

DEF TEMP-TABLE coa-list2
    FIELD datum1      AS DATE COLUMN-LABEL "Date"
    FIELD wert1       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "RECEIVING Amount"
    FIELD fibu1       AS CHAR
    FIELD debitcredit AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "GL Jourrnal"
    FIELD diff        AS DECIMAL FORMAT "->>>,>>>,>>9" LABEL "DIFF".

DEF TEMP-TABLE coa-list3
    FIELD datum2      AS DATE COLUMN-LABEL "Date"
    FIELD wert2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "OUTGOING Amount"
    FIELD fibu2       AS CHAR
    FIELD creditdebit AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "GL Jourrnal"
    FIELD diff        AS DECIMAL FORMAT "->>>,>>>,>>9" LABEL "DIFF".

DEF TEMP-TABLE s-list
    FIELD fibu        AS CHAR
    FIELD saldo1      AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2      AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo       AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0.

DEF TEMP-TABLE s-list2
    FIELD fibu1     AS CHAR
    FIELD saldo1a   AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2a   AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo1    AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo3    AS DECIMAL LABEL "DIFF" format "->>>,>>>,>>9".

DEF TEMP-TABLE s-list3
    FIELD fibu2   AS CHAR
    FIELD saldo1b AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2b AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo3a AS DECIMAL LABEL "DIFF" format "->>>,>>>,>>9"
    FIELD saldo11 AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0.

DEF TEMP-TABLE artikel1
    FIELD art   AS INT
    FIELD ekum  AS INT
    FIELD zeich AS CHAR.

DEF TEMP-TABLE artikel2
    FIELD art      AS INT 
    FIELD ekum     AS INT 
    FIELD zeich    AS CHAR
    FIELD zeich2   AS CHAR
    FIELD numb     AS INT. 

DEF TEMP-TABLE artikel3
    FIELD kum       AS INT  
    FIELD zeich2    AS CHAR 
    FIELD numb      AS INT  
    FIELD fibu      AS CHAR 
    FIELD zeich3    AS CHAR. 

DEF TEMP-TABLE art-list
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF TEMP-TABLE art-list2
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF TEMP-TABLE art-list3
    FIELD datum     AS DATE
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF TEMP-TABLE art-list4
    FIELD datum     AS DATE
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

 
DEFINE INPUT PARAMETER fromDate		      AS DATE.  
DEFINE INPUT PARAMETER toDate			  AS DATE.  
DEFINE INPUT PARAMETER inventoryType	  AS INT.  
DEFINE INPUT PARAMETER outgoingPrefix	  AS CHAR.  
DEFINE INPUT PARAMETER mainGroup		  AS LOGICAL.  
DEFINE INPUT PARAMETER subGroup		      AS LOGICAL.  
DEFINE INPUT PARAMETER mainGroupGL		  AS LOGICAL.  
DEFINE INPUT PARAMETER receivingGL		  AS LOGICAL.  
DEFINE INPUT PARAMETER outgoingGL		  AS LOGICAL.  
DEFINE INPUT PARAMETER beginBalanceINVGL  AS LOGICAL.  
DEFINE INPUT PARAMETER endingBalanceINVGL AS LOGICAL.  

DEFINE OUTPUT PARAMETER TABLE FOR artikel1.
DEFINE OUTPUT PARAMETER TABLE FOR artikel2.
DEFINE OUTPUT PARAMETER TABLE FOR artikel3.
DEFINE OUTPUT PARAMETER TABLE FOR coa-list2.
DEFINE OUTPUT PARAMETER TABLE FOR coa-list3.
DEFINE OUTPUT PARAMETER TABLE FOR s-list2.
DEFINE OUTPUT PARAMETER TABLE FOR s-list3.
DEFINE OUTPUT PARAMETER TABLE FOR art-list.
DEFINE OUTPUT PARAMETER TABLE FOR art-list2.
DEFINE OUTPUT PARAMETER TABLE FOR art-list3.
DEFINE OUTPUT PARAMETER TABLE FOR art-list4.

DEFINE VARIABLE d1      AS DATE.
DEFINE VARIABLE d2      AS DATE.
DEFINE VARIABLE d       AS DATE.
DEFINE VARIABLE invType AS INTEGER.
DEFINE VARIABLE frNr    AS INTEGER.
DEFINE VARIABLE toNr    AS INTEGER.
DEFINE VARIABLE fibu    AS CHAR.
DEFINE VARIABLE art1    AS INTEGER.
DEFINE VARIABLE art2    AS INTEGER.
DEFINE VARIABLE mon     AS INTEGER.
DEFINE VARIABLE refNo   AS CHARACTER.
DEFINE VARIABLE saldo   AS DECIMAL.
DEFINE VARIABLE detail1 AS LOGICAL.
DEFINE VARIABLE detail2 AS LOGICAL.
DEFINE VARIABLE detail3 AS LOGICAL.
DEFINE VARIABLE detail4 AS LOGICAL.
DEFINE VARIABLE detail5 AS LOGICAL.
DEFINE VARIABLE detail6 AS LOGICAL.
DEFINE VARIABLE detail7 AS LOGICAL.

ASSIGN
d1      = fromDate          
d2      = toDate            
invType = inventoryType     
refNo   = outgoingPrefix    
detail1 = mainGroup         
detail2 = subGroup          
detail3 = mainGroupGL       
detail4 = beginBalanceINVGL    
detail5 = receivingGL          
detail6 = outgoingGL  
detail7 = endingBalanceINVGL.

IF detail1 THEN
DO:
    RUN inv-checking-create-main-cldbl.p (OUTPUT TABLE artikel1).
END.
IF detail2 THEN 
DO:
    RUN inv-checking-create-sub-cldbl.p (OUTPUT TABLE artikel2).
END.
IF detail3 THEN 
DO:
    RUN inv-checking-create-gl-cldbl.p (OUTPUT TABLE artikel3).
END.  
IF detail4 THEN
DO: 
    RUN inv-checking-create-list-cldbl.p (invType, d1, OUTPUT saldo, OUTPUT TABLE s-list2, OUTPUT TABLE art-list2).
END. 
IF detail5 THEN     
DO:
    RUN inv-checking-create-list2-cldbl.p (TABLE coa-list, invType, d1, d2, 
                                       OUTPUT frNr, OUTPUT toNr, OUTPUT saldo, 
                                       OUTPUT TABLE coa-list2, OUTPUT TABLE art-list3).
END.
IF detail6 THEN
DO: 
    RUN inv-checking-out-gl-cldbl.p (invType, d1, d2, OUTPUT frNr, OUTPUT toNr, OUTPUT saldo,
                                 OUTPUT TABLE coa-list3, OUTPUT TABLE art-list4).
END.
IF detail7 THEN
DO:
    RUN inv-checking-end-gl-cldbl.p (frNr, toNr, d2, saldo, OUTPUT TABLE s-list3, OUTPUT TABLE art-list).
END.
