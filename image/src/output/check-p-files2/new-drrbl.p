DEFINE TEMP-TABLE rev-seg-list 
    FIELD ct            AS INTEGER
    FIELD segment-code  AS INTEGER 
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD dper          AS DECIMAL FORMAT ">>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd-per       AS DECIMAL FORMAT "->>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-per       AS DECIMAL FORMAT ">>9.99"
    FIELD flag          AS CHAR
    FIELD flag-grup     AS LOGICAL. /*room, outlet, otherIncome*/

DEFINE TEMP-TABLE rev-seg-list1 LIKE rev-seg-list.

DEFINE TEMP-TABLE rev-list 
    FIELD ct            AS INTEGER
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD dper          AS DECIMAL FORMAT ">>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd-per       AS DECIMAL FORMAT "->>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-per       AS DECIMAL FORMAT ">>9.99"
    FIELD flag          AS CHAR
    FIELD flag-grup     AS LOGICAL.

DEFINE TEMP-TABLE rev-list-tax LIKE rev-list.
DEFINE TEMP-TABLE rev-list-serv LIKE rev-list.
DEFINE TEMP-TABLE payable-list LIKE rev-list. 
DEFINE TEMP-TABLE tot-list LIKE rev-list.

DEFINE TEMP-TABLE stat-list
    FIELD ct            AS INTEGER
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD flag          AS CHAR.

DEFINE TEMP-TABLE payment-list LIKE stat-list.

DEFINE TEMP-TABLE segment-list
    FIELD segmentcode   AS INTEGER
    FIELD bezeich       AS CHAR.

DEFINE TEMP-TABLE gl-list
    FIELD descr       AS CHAR
    FIELD tot-rev     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

DEFINE TEMP-TABLE fb-sales-food
    FIELD ct           AS INTEGER
    FIELD artnr        AS INTEGER
    FIELD departement  AS INTEGER
    FIELD descr        AS CHAR FORMAT "x(35)"
    FIELD tday-cov     AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD tday-avg     AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD tday-rev     AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD mtd-cov      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD mtd-avg      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD mtd-rev      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD ytd-cov      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD ytd-avg      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD ytd-rev      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD flag         AS CHAR 
    .

DEFINE TEMP-TABLE fb-sales-beverage LIKE fb-sales-food.
DEFINE TEMP-TABLE fb-sales-other LIKE fb-sales-food.
DEFINE TEMP-TABLE fb-sales-tot  LIKE fb-sales-food.
DEFINE TEMP-TABLE fb-sales-material LIKE fb-sales-food.

DEFINE TEMP-TABLE setup-revenue
    FIELD artnr         AS INTEGER
    FIELD flag-used     AS LOGICAL INITIAL YES
    FIELD flag-grup     AS LOGICAL INITIAL NO
    FIELD descr         AS CHAR
    FIELD departement   AS INTEGER
    FIELD flag          AS CHAR.


DEFINE TEMP-TABLE setup-segment LIKE setup-revenue.

DEFINE TEMP-TABLE setup-payment
    FIELD artnr             AS INTEGER
    FIELD artart            AS INTEGER
    FIELD umsatzart         AS INTEGER
    FIELD departement       AS INTEGER INITIAL 0
    FIELD flag              AS LOGICAL.
    
DEFINE TEMP-TABLE setup-stat
    FIELD zwkum    AS INT
    FIELD artnr    AS INT
    FIELD flag     AS CHAR
    FIELD descr    AS CHAR.

DEFINE TEMP-TABLE setup-fbcover
    FIELD departement AS INT
    FIELD artnr       AS INT
    FIELD flag        AS CHAR.

DEFINE BUFFER   buff-umsatz     FOR umsatz.
DEFINE BUFFER   b-rev-list      FOR rev-list.
DEFINE BUFFER   b-rev-seg-list  FOR rev-seg-list.
DEFINE BUFFER   b-rev-seg-list1 FOR rev-seg-list1.

DEFINE BUFFER   b-stat-list     FOR stat-list.
DEFINE BUFFER   brev-list       FOR rev-list.
DEFINE BUFFER   b-payment-list  FOR payment-list.
DEFINE BUFFER   bpayment-list   FOR payment-list.
DEFINE BUFFER   bpayable-list   FOR payable-list.


DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR rev-seg-list.
DEFINE OUTPUT PARAMETER TABLE FOR rev-list.
DEFINE OUTPUT PARAMETER TABLE FOR payable-list.
DEFINE OUTPUT PARAMETER TABLE FOR stat-list.
DEFINE OUTPUT PARAMETER TABLE FOR payment-list.
DEFINE OUTPUT PARAMETER TABLE FOR gl-list.
DEFINE OUTPUT PARAMETER TABLE FOR fb-sales-food.
DEFINE OUTPUT PARAMETER TABLE FOR fb-sales-beverage.
DEFINE OUTPUT PARAMETER TABLE FOR fb-sales-other.
DEFINE OUTPUT PARAMETER TABLE FOR fb-sales-tot.
DEFINE OUTPUT PARAMETER TABLE FOR rev-seg-list1.
DEFINE OUTPUT PARAMETER TABLE FOR fb-sales-material.
DEFINE OUTPUT PARAMETER gsheet-link AS CHAR.

/*
DEFINE VARIABLE from-date AS DATE INITIAL 01/01/23.
DEFINE VARIABLE to-date   AS DATE INITIAL 01/01/23.
DEFINE VARIABLE gsheet-link AS CHAR.
*/

DEFINE VARIABLE ytd-flag  AS LOGICAL INITIAL YES.


DEFINE VARIABLE str1  AS CHAR.
DEFINE VARIABLE str2  AS CHAR.
DEFINE VARIABLE str3  AS CHAR.
DEFINE VARIABLE st1   AS CHAR.
DEFINE VARIABLE st2   AS CHAR.
DEFINE VARIABLE st3   AS CHAR.
DEFINE VARIABLE st4   AS CHAR.
DEFINE VARIABLE st5   AS CHAR.
DEFINE VARIABLE st6   AS CHAR.
DEFINE VARIABLE st7   AS CHAR.
DEFINE VARIABLE st8   AS CHAR.
DEFINE VARIABLE st9   AS CHAR.
DEFINE VARIABLE st10  AS CHAR.
DEFINE VARIABLE st11  AS CHAR.
DEFINE VARIABLE st12  AS CHAR.
DEFINE VARIABLE st13  AS CHAR.
DEFINE VARIABLE st14  AS CHAR.
DEFINE VARIABLE st15  AS CHAR.
DEFINE VARIABLE st16  AS CHAR.
DEFINE VARIABLE st17  AS CHAR.
DEFINE VARIABLE st18  AS CHAR.
DEFINE VARIABLE st19  AS CHAR.
DEFINE VARIABLE st20  AS CHAR.
DEFINE VARIABLE st21  AS CHAR.
DEFINE VARIABLE st22  AS CHAR.
DEFINE VARIABLE st23  AS CHAR.
DEFINE VARIABLE st24  AS CHAR.
DEFINE VARIABLE st25  AS CHAR.
DEFINE VARIABLE st26  AS CHAR.
DEFINE VARIABLE st27  AS CHAR.
DEFINE VARIABLE st28  AS CHAR.
DEFINE VARIABLE st29  AS CHAR.
DEFINE VARIABLE st30  AS CHAR.
DEFINE VARIABLE st31  AS CHAR.
DEFINE VARIABLE st32  AS CHAR.
DEFINE VARIABLE st33  AS CHAR.
DEFINE VARIABLE st34  AS CHAR.
DEFINE VARIABLE st35  AS CHAR.
DEFINE VARIABLE st36  AS CHAR.
DEFINE VARIABLE st37  AS CHAR.


DEFINE VARIABLE n     AS INT.
DEFINE VARIABLE n1    AS INT.
DEFINE VARIABLE n2    AS INT.
DEFINE VARIABLE n3    AS INT.
DEFINE VARIABLE n4    AS INT.
DEFINE VARIABLE n5    AS INT.
DEFINE VARIABLE n6    AS INT.
DEFINE VARIABLE n7    AS INT.
DEFINE VARIABLE n8    AS INT.
DEFINE VARIABLE n9    AS INT.
DEFINE VARIABLE n10   AS INT.
DEFINE VARIABLE n11   AS INT.
DEFINE VARIABLE n12   AS INT.
DEFINE VARIABLE n13   AS INT.
DEFINE VARIABLE n14   AS INT.
DEFINE VARIABLE n15   AS INT.
DEFINE VARIABLE n16   AS INT.
DEFINE VARIABLE n17   AS INT.
DEFINE VARIABLE n18   AS INT.
DEFINE VARIABLE n19   AS INT.
DEFINE VARIABLE n20   AS INT.
DEFINE VARIABLE n21   AS INT.
DEFINE VARIABLE n22   AS INT.
DEFINE VARIABLE n23   AS INT.
DEFINE VARIABLE n24   AS INT.
DEFINE VARIABLE n25   AS INT.
DEFINE VARIABLE n26   AS INT.
DEFINE VARIABLE n27   AS INT.
DEFINE VARIABLE n28   AS INT.
DEFINE VARIABLE n29   AS INT.
DEFINE VARIABLE n30   AS INT.


DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE start-date      AS DATE.
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE serv            AS DECIMAL. 
DEFINE VARIABLE vat             AS DECIMAL. 
DEFINE VARIABLE vat2            AS DECIMAL. 
DEFINE VARIABLE fact            AS DECIMAL. 
DEFINE VARIABLE n-betrag        AS DECIMAL.
DEFINE VARIABLE n-serv          AS DECIMAL. 
DEFINE VARIABLE n-tax           AS DECIMAL. 
DEFINE VARIABLE ly-betrag       AS DECIMAL. 
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag    AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.

DEFINE VARIABLE yes-serv        AS DECIMAL. 
DEFINE VARIABLE yes-vat         AS DECIMAL. 
DEFINE VARIABLE yes-vat2        AS DECIMAL. 
DEFINE VARIABLE yes-fact        AS DECIMAL. 
DEFINE VARIABLE yes-betrag      AS DECIMAL. 
DEFINE VARIABLE date1           AS DATE.
DEFINE VARIABLE date2           AS DATE.
DEFINE VARIABLE temp-date2      AS DATE.
DEFINE VARIABLE temp-curr-date  AS DATE.

DEFINE VARIABLE l-today         AS INT INIT 0.
DEFINE VARIABLE st-date         AS INT INIT 0.
DEFINE VARIABLE foreign-nr      AS INT.
DEFINE VARIABLE foreign-flag    AS LOGICAL INITIAL YES.

DEFINE VARIABLE tot-betrag      AS DECIMAL.
DEFINE VARIABLE price-decimal   AS INTEGER.
DEFINE VARIABLE no-decimal      AS LOGICAL INITIAL NO. 
DEFINE VARIABLE dept            AS INTEGER.
DEFINE VARIABLE dept1           AS INTEGER.
DEFINE VARIABLE zwkum           AS INTEGER.
DEFINE VARIABLE dper            AS INTEGER.
DEFINE VARIABLE mtd-per         AS INTEGER.
DEFINE VARIABLE ytd-per         AS INTEGER.

/*Room revenue*/
DEFINE VARIABLE tot-today           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-today-per       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-per         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-per         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*Other revenue*/
DEFINE VARIABLE tot-today1           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-today-per1       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd1             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-per1         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget1      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd1             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget1      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-per1         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*Outlets revenue*/
DEFINE VARIABLE tot-today2           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-today-per2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd2             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-per2         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget2      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd2             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget2      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-per2         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*payment total cash*/
DEFINE VARIABLE tot-today3           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd3             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget3      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance3        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd3             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget3      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*payment total Credit card*/
DEFINE VARIABLE tot-today4           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd4             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget4      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance4        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd4             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget4      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*payment total city ledger*/
DEFINE VARIABLE tot-today5           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd5             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget5      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance5        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd5             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget5      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*payment total Foreign*/
DEFINE VARIABLE tot-today6           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd6             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget6      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance6        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd6             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget6      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*payment total Deposit*/
DEFINE VARIABLE tot-today7           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd7             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-budget7      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-variance7        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd7             AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-budget7      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*fb-sales-food total*/
DEFINE VARIABLE tot-tday-cov          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-tday-avg          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-tday-rev          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-cov           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-avg           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-mtd-rev           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-cov           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-avg           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tot-ytd-rev           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*grand total revenue*/
DEFINE VARIABLE t-today          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-today-per      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-per        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-budget     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-variance       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-budget     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-per        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*grand total revenue by segment*/
DEFINE VARIABLE t-today1          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-today-per1      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd1            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-per1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-budget1     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-variance1       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd1            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-budget1     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-per1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-today11         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-today-per11     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd11           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-per11       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-budget11    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-variance11      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd11           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-budget11    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-per11       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*grand total Payment*/
DEFINE VARIABLE t-today2          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-today-per2      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd2            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-per2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-budget2     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-variance2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd2            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-budget2     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-per2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*grand total Payable*/
DEFINE VARIABLE t-today3          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-today-per3      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd3            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-per3        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-mtd-budget3     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-variance3       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd3            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-budget3     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE t-ytd-per3        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*total guest ledger*/

DEFINE VARIABLE tdy-gl1          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd-gl           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

/*revenue*/
DEFINE VARIABLE curr-flag        AS  CHAR.
DEFINE VARIABLE curr-dept        AS INTEGER.
DEFINE VARIABLE ct               AS INTEGER.
DEFINE VARIABLE ct3              AS INTEGER.
DEFINE VARIABLE ct4              AS INTEGER.
DEFINE VARIABLE t-day-serv       AS DECIMAL.
DEFINE VARIABLE mtd-serv         AS DECIMAL.
DEFINE VARIABLE mtd-budget-serv  AS DECIMAL.
DEFINE VARIABLE ytd-serv         AS DECIMAL.
DEFINE VARIABLE ytd-budget-serv  AS DECIMAL.
DEFINE VARIABLE variance-serv    AS DECIMAL.
DEFINE VARIABLE t-day-tax        AS DECIMAL.
DEFINE VARIABLE mtd-tax          AS DECIMAL.
DEFINE VARIABLE mtd-budget-tax   AS DECIMAL.
DEFINE VARIABLE ytd-tax          AS DECIMAL.
DEFINE VARIABLE ytd-budget-tax   AS DECIMAL.
DEFINE VARIABLE variance-tax     AS DECIMAL.
/*statistik*/
DEFINE VARIABLE ct1        AS INTEGER.
/*payment*/
DEFINE VARIABLE curr-flag1  AS  CHAR.
DEFINE VARIABLE ct2        AS INTEGER.

DEFINE VARIABLE banq-dept AS INT.

DEFINE VARIABLE frate           AS DECIMAL INITIAL 1.
DEFINE VARIABLE jan1            AS DATE.
jan1  = DATE(1, 1, year(to-date)).

DEFINE VARIABLE budget-flag     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE mon-saldo       AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
DEFINE VARIABLE mon-budget      AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].

DEFINE VARIABLE foreign-curr AS DECIMAL.
FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ 2 NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN foreign-curr = waehrung.ankauf.


FIND FIRST htparam WHERE htparam.paramnr EQ 184 NO-LOCK NO-ERROR.
ASSIGN foreign-nr = htparam.fint.

FIND FIRST htparam WHERE htparam.paramnr = 186 NO-LOCK. 
IF htparam.feldtyp = 3 AND htparam.fdate NE ? THEN start-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr EQ 900 NO-LOCK NO-ERROR.
ASSIGN banq-dept = htparam.fint.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK NO-ERROR. 
price-decimal = htparam.finteger. 
no-decimal = (price-decimal = 0). 

FIND FIRST htparam WHERE htparam.paramnr EQ 801 NO-LOCK NO-ERROR.

IF ytd-flag THEN datum1 = jan1. 
ELSE datum1 = from-date. 

IF price-decimal = 0 THEN
    price-decimal = 2.
no-decimal = (price-decimal = 0).

FIND FIRST queasy WHERE queasy.KEY EQ 265 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
   ASSIGN 
       str1  = queasy.char1
       str2  = queasy.char2
       str3  = queasy.char3.
END.


FOR EACH segment NO-LOCK:
    FIND FIRST segment-list WHERE segment-list.segmentcode EQ segment.segmentcode NO-ERROR.
    IF NOT AVAILABLE segment-list THEN DO:
      CREATE segment-list.
      ASSIGN 
             segment-list.segmentcode  = segment.segmentcode
             segment-list.bezeich      = segment.bezeich.
    END.
END.

DO n1 = 1 TO NUM-ENTRIES(str2,";"):
st2 = ENTRY(n1,str2,";").
    IF SUBSTR(st2,1,11)  = "$FOrevenue$" AND SUBSTR(st2,12,3) EQ "YES" THEN DO:
      ASSIGN
         st3   = SUBSTR(st2,12,3)
         st4   = SUBSTR(st2,16).
      
      DO n2 = 1 TO NUM-ENTRIES(st4,","):
         st5 = ENTRY(n2,st4,",").
         CREATE setup-revenue.
         ASSIGN
             setup-revenue.artnr        = INTEGER(ENTRY(1,st5,"-"))
             setup-revenue.flag         = "Room"
             setup-revenue.departement  = 0.
         IF ENTRY(2,st5,"-") EQ "YES" THEN DO:
             setup-revenue.flag-grup = LOGICAL(ENTRY(2,st5,"-")).
             setup-revenue.descr   = ENTRY(3,st5,"-").
         END.
      END.
   
    END.
    IF SUBSTR(st2,1,13)  = "$otherincome$" AND SUBSTR(st2,14,3) EQ "YES" THEN DO:
      ASSIGN
         st6   = SUBSTR(st2,14,3)
         st7   = SUBSTR(st2,18).

      DO n3 = 1 TO NUM-ENTRIES(st7,","):
         st8 = ENTRY(n3,st7,",").
         CREATE setup-revenue. 
         ASSIGN
             setup-revenue.artnr        =  INTEGER(ENTRY(1,st8,"-"))
             setup-revenue.flag         = "Other"
             setup-revenue.departement  = 0. 
         IF ENTRY(2,st8,"-") EQ "YES" THEN DO:
             setup-revenue.flag-grup = LOGICAL(ENTRY(2,st8,"-")).
             setup-revenue.descr   = ENTRY(3,st8,"-").
         END.
      END.   
    END.
    IF SUBSTR(st2,1,9)  = "$segment$" AND SUBSTR(st2,10,3) EQ "YES" THEN DO:
        st29 = SUBSTR(st2,14).
        
        DO n23 = 1 TO NUM-ENTRIES(st29,","):
           st30 = ENTRY(n23,st29,",").
           CREATE setup-segment.
           ASSIGN 
              setup-segment.artnr        =  INTEGER(ENTRY(1,st30,"-"))
              setup-segment.flag         = "Segment"
              setup-segment.departement  = 0. 
           IF ENTRY(2,st30,"-") EQ "YES" THEN DO:
              setup-segment.flag-grup = LOGICAL(ENTRY(2,st30,"-")).
              setup-segment.descr   = ENTRY(3,st30,"-").
           END.

        END.
    END.
    IF SUBSTR(st2,1,11)  = "$statistic$" AND SUBSTR(st2,12,3) EQ "YES" THEN DO:
        st31 = SUBSTR(st2,16).

        DO n24 = 1 TO NUM-ENTRIES(st31,"/"):
           st32 = ENTRY(n24,st31,"/").
           
           IF n24 EQ 1 AND st32 NE "" THEN ASSIGN zwkum = INTEGER(ENTRY(1,st32,"/")). 
           ELSE IF n24 GT 1 AND st32 NE "" THEN DO:
              DO n25 = 1 TO NUM-ENTRIES(st32,","):
                 st33 = ENTRY(n25,st32,",").
                     CREATE setup-stat.
                     ASSIGN setup-stat.zwkum = zwkum.   
                 DO n26 = 1 TO NUM-ENTRIES (st33,"-"):
                     ASSIGN setup-stat.artnr = INTEGER(ENTRY(1,st33,"-")) 
                            setup-stat.descr = ENTRY(2,st33,"-")
                            setup-stat.flag  = "Statistic".
                 END.
              END.
           END.
        END.                               
    END.
END.

DO n4 = 1 TO NUM-ENTRIES(str3,"*"):
    st9 = ENTRY(n4,str3,"*").

    IF SUBSTR(st9,1,16) = "$revenueOutlets$" AND SUBSTR(st9,17,3) EQ "YES" THEN DO:
       ASSIGN st10 = SUBSTR(st9, 20).
       
       DO n5 = 1 TO NUM-ENTRIES (st10,";") :
            st11 = ENTRY(n5,st10,";").
            DO n6 = 1 TO NUM-ENTRIES (st11,"|"):
               st12 = ENTRY (n6,st11,"|").
                    
               IF n6 EQ 1 AND st12 NE "" AND ENTRY(2,st11,"|") NE "" THEN ASSIGN dept = INTEGER(st12).
               ELSE IF st12 NE "" AND n6 GT 1 THEN DO:
                   DO n7 = 1 TO NUM-ENTRIES(st12, ","):
                      st13 = ENTRY(n7, st12, ",").
                        IF st13 NE "" THEN DO:
                            CREATE setup-revenue.
                            ASSIGN setup-revenue.departement = dept
                                   setup-revenue.artnr       =  INTEGER(ENTRY(1,st13,"-"))
                                   setup-revenue.flag        = "Outlet".
                            IF ENTRY(2,st13,"-") EQ "YES" THEN DO:
                                setup-revenue.flag-grup     = LOGICAL(ENTRY(2,st13,"-")).
                                setup-revenue.descr         = ENTRY(3,st13,"-").
                            END.
                       END.
                   END.
               END.                             
            END.
    
        END.
    END. 

    IF SUBSTR(st9,1,9) = "$FBcover$" AND SUBSTR(st9,10,3) EQ "YES" THEN DO:
        ASSIGN st23 = SUBSTR (st9,13).
        
        DO n18 = 1 TO NUM-ENTRIES (st23,";"):
            st24 = ENTRY(n18,st23,";").
            DO n19 = 1 TO NUM-ENTRIES (st24,"|"):
                st25 = ENTRY(n19,st24,"|").

                IF n19 EQ 1 AND st25 NE "" AND ENTRY(2,st24,"|") NE "" THEN ASSIGN dept1 = INTEGER(st25).
                ELSE IF st25 NE "" AND n19 GT 1 THEN DO:
                    DO n20 = 1 TO NUM-ENTRIES (st25,"-"):
                        st26 = ENTRY(n20,st25,"-").
                        
                        IF SUBSTR(st26,1,1) EQ "F"  THEN DO:
                            st27 = SUBSTR(st26,2).
                            DO n21 = 1 TO NUM-ENTRIES (st27,","):
                                CREATE setup-fbcover.
                                ASSIGN setup-fbcover.departement = dept1
                                       setup-fbcover.artnr       = INTEGER(ENTRY(n21,st27,",")).
                                IF dept1 EQ banq-dept THEN ASSIGN setup-fbcover.flag        = "3Banquet".
                                ELSE setup-fbcover.flag        = "1Food".
                            END.
                        END.
                        ELSE IF SUBSTR(st26,1,1) EQ "B" THEN DO:
                            st28 = SUBSTR(st26,2).
                            DO n22 = 1 TO NUM-ENTRIES (st28,","):
                                CREATE setup-fbcover.
                                ASSIGN setup-fbcover.departement = dept1
                                       setup-fbcover.artnr       = INTEGER(ENTRY(n22,st28,",")).
                                IF dept1 EQ banq-dept THEN ASSIGN setup-fbcover.flag        = "3Banquet".
                                ELSE setup-fbcover.flag        = "2Beverage".
                            END.
                        END.
                        ELSE IF SUBSTR(st26,1,1) EQ "M" THEN DO:
                            st28 = SUBSTR(st26,2).
                            DO n22 = 1 TO NUM-ENTRIES (st28,","):
                                CREATE setup-fbcover.
                                ASSIGN setup-fbcover.departement = dept1
                                       setup-fbcover.artnr       = INTEGER(ENTRY(n22,st28,",")).
                                IF dept1 EQ banq-dept THEN ASSIGN setup-fbcover.flag        = "3Banquet".
                                ELSE setup-fbcover.flag        = "4Material".
                            END.
                        END.
                    END.
                END.
            END.
        END.
    END.
END.

DO n8 = 1 TO NUM-ENTRIES(str1,";"):
    st14 = ENTRY(n8,str1,";").
    
    IF SUBSTR(st14,1,10) EQ "$otherPay$" AND SUBSTR(st14,11,3) EQ "YES"  THEN DO:
        st15 = SUBSTR(st14,15 ).
        DO n9 = 1 TO NUM-ENTRIES (st15,","):
        st16 = ENTRY(n9,st15,",").
        IF st16 NE "" THEN DO:
            CREATE setup-revenue.
            ASSIGN setup-revenue.departement = 0
                   setup-revenue.artnr       = INTEGER(ENTRY(n9,st15,","))
                   setup-revenue.flag        = "OtherPayable". 
        END.

        END.
    END.

END.

DO n10 = 1 TO NUM-ENTRIES(str1,";"):
    
    st17 = ENTRY(n10,str1,";").

    IF SUBSTR(st17,1,9)  = "$payment$" AND SUBSTR(st17,10,3) EQ "YES" THEN DO:
        st18 = SUBSTR(st17,14).
        DO n11 = 1 TO NUM-ENTRIES(st18,","):
            CREATE setup-payment.
            ASSIGN setup-payment.artnr      = INTEGER(ENTRY(n11,st18,","))
                   setup-payment.artart     = 7
                   setup-payment.umsatzart  = 0
                   setup-payment.flag       = YES.
        END.
    END.

    ELSE IF SUBSTR(st17,1,8) EQ "$ledger$" AND SUBSTR(st17,9,3) EQ "YES"  THEN DO:
        st19 = SUBSTR(st17,13).
        DO n12 = 1 TO NUM-ENTRIES(st19,","):
            CREATE setup-payment.
            ASSIGN setup-payment.artnr      = INTEGER(ENTRY(n12,st19,","))
                   setup-payment.artart     = 2
                   setup-payment.umsatzart  = 0
                   setup-payment.flag       = YES.
        END.
    END.
       

    ELSE IF SUBSTR(st17,1,6) EQ "$cash$" AND SUBSTR(st17,7,3) EQ "YES"  THEN DO:
        st20 = SUBSTR(st17,11).
        DO n13 = 1 TO NUM-ENTRIES(st20,","):
            CREATE setup-payment.
            ASSIGN setup-payment.artnr      = INTEGER(ENTRY(n13,st20,","))
                   setup-payment.artart     = 6
                   setup-payment.umsatzart  = 0 
                   setup-payment.flag       = YES.
        END.
    END.
        
    
    ELSE IF SUBSTR(st17,1,9) EQ "$foreign$" AND SUBSTR(st17,10,3) EQ "YES"  THEN DO:
        st21 = SUBSTR(st17,14).
        DO n14 = 1 TO NUM-ENTRIES(st21,","):
            CREATE setup-payment.
            ASSIGN setup-payment.artnr      = INTEGER(ENTRY(n14,st21,","))
                   setup-payment.artart     = 6
                   setup-payment.umsatzart  = 4
                   setup-payment.flag       = YES.
        END.
    END.
        
    
    ELSE IF SUBSTR(st17,1,9) EQ "$deposit$" AND SUBSTR(st17,10,3) EQ "YES"  THEN DO:
        st22 = SUBSTR(st17,14).
        DO n15 = 1 TO NUM-ENTRIES(st22,","):
            CREATE setup-payment.
            ASSIGN setup-payment.artnr      = INTEGER(ENTRY(n15,st22,","))
                   setup-payment.artart     = 5
                   setup-payment.umsatzart  = 0
                   setup-payment.flag       = YES.
        END.
    END.

    ELSE IF SUBSTR(st17,1,8) EQ "$Gsheet$" THEN DO:
        ASSIGN
            gsheet-link  = SUBSTR(st17,9).
    END.

END.


FOR EACH setup-revenue NO-LOCK BY setup-revenue.flag DESC BY setup-revenue.departement BY setup-revenue.flag-grup DESC BY setup-revenue.descr:
    FIND FIRST artikel WHERE artikel.departement = setup-revenue.departement AND artikel.artnr EQ setup-revenue.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN DO:
    
        IF setup-revenue.flag = "OtherPayable" THEN RUN create-payable-list.
        ELSE RUN create-rev-list.

    END. 
END.

FOR EACH setup-segment NO-LOCK:
    FIND FIRST segment WHERE segment.segmentcode = setup-segment.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN DO:
        RUN fill-revenue-segement.
        RUN fill-revenue-segement1.
    END.
END.

FOR EACH setup-payment NO-LOCK:

    FIND FIRST artikel WHERE artikel.departement = setup-payment.departement 
    AND artikel.artnr EQ setup-payment.artnr 
    AND artikel.artart EQ setup-payment.artart
    AND artikel.umsatzart EQ setup-payment.umsatzart NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN DO: 
        ct2 = ct2 + 1.    
        RUN create-payment-list.

    END.    
END.

FOR EACH setup-fbcover NO-LOCK BY setup-fbcover.departement:
  FIND FIRST hoteldpt WHERE hoteldpt.num EQ setup-fbcover.departement NO-LOCK NO-ERROR.
  FIND FIRST artikel WHERE artikel.artnr = setup-fbcover.artnr 
  AND artikel.departement = setup-fbcover.departement NO-LOCK NO-ERROR.
  IF AVAILABLE artikel THEN DO:

    RUN create-fbcover.
  END.
END.

FOR EACH rev-list NO-LOCK BY rev-list.flag BY rev-list.departement:
    IF curr-flag NE "" AND rev-list.flag NE "zeich-dept"  AND (curr-flag NE rev-list.flag) AND curr-dept = 0 THEN DO:
            IF curr-flag = "Room" THEN DO:  
                CREATE b-rev-list.
                ASSIGN
                    b-rev-list.ct            = ct + 1 
                    b-rev-list.descr         = "TOTAL ROOM REVENUE"
                    b-rev-list.departement   = 0
                    b-rev-list.t-day         = tot-today     
                    b-rev-list.dper          = tot-today-per 
                    b-rev-list.mtd           = tot-mtd       
                    b-rev-list.mtd-per       = tot-mtd-per   
                    b-rev-list.mtd-budget    = tot-mtd-budget
                    b-rev-list.variance      = tot-variance  
                    b-rev-list.ytd           = tot-ytd       
                    b-rev-list.ytd-budget    = tot-ytd-budget
                    b-rev-list.ytd-per       = tot-ytd-per   
                    b-rev-list.flag          = "Room"
                    tot-today                = 0
                    tot-today-per            = 0
                    tot-mtd                  = 0
                    tot-mtd-per              = 0
                    tot-mtd-budget           = 0
                    tot-variance             = 0
                    tot-ytd                  = 0  
                    tot-ytd-budget           = 0
                    tot-ytd-per              = 0  
                    .

            END.
            ELSE IF curr-flag = "Other" THEN DO:
                CREATE b-rev-list.
                ASSIGN
                    b-rev-list.ct            = ct + 1 
                    b-rev-list.descr         = "TOTAL OTHER REVENUE"
                    b-rev-list.departement   = 0 
                    b-rev-list.t-day         = tot-today1     
                    b-rev-list.dper          = tot-today-per1 
                    b-rev-list.mtd           = tot-mtd1       
                    b-rev-list.mtd-per       = tot-mtd-per1   
                    b-rev-list.mtd-budget    = tot-mtd-budget1
                    b-rev-list.variance      = tot-variance1  
                    b-rev-list.ytd           = tot-ytd1       
                    b-rev-list.ytd-budget    = tot-ytd-budget1
                    b-rev-list.ytd-per       = tot-ytd-per1   
                    b-rev-list.flag          = "Other"
                    tot-today1               = 0
                    tot-today-per1           = 0
                    tot-mtd1                 = 0
                    tot-mtd-per1             = 0
                    tot-mtd-budget1          = 0
                    tot-variance1            = 0
                    tot-ytd1                 = 0  
                    tot-ytd-budget1          = 0
                    tot-ytd-per1             = 0  
                    .
            END.
    END.
    ELSE IF curr-flag NE "" AND curr-flag NE "zeich-dept" AND curr-dept NE 0  AND curr-dept NE rev-list.departement THEN DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
        CREATE b-rev-list.
        ASSIGN
            b-rev-list.ct            = ct + 1 
            b-rev-list.descr         = "TOTAL " + hoteldpt.depart + " REVENUE" 
            b-rev-list.departement   = curr-dept
            b-rev-list.t-day         = tot-today2     
            b-rev-list.dper          = tot-today-per2 
            b-rev-list.mtd           = tot-mtd2       
            b-rev-list.mtd-per       = tot-mtd-per2   
            b-rev-list.mtd-budget    = tot-mtd-budget2
            b-rev-list.variance      = tot-variance2  
            b-rev-list.ytd           = tot-ytd2       
            b-rev-list.ytd-budget    = tot-ytd-budget2
            b-rev-list.ytd-per       = tot-ytd-per2   
            b-rev-list.flag          = "Outlet"
            tot-today2               = 0
            tot-today-per2           = 0
            tot-mtd2                 = 0
            tot-mtd-per2             = 0
            tot-mtd-budget2          = 0
            tot-variance2            = 0
            tot-ytd2                 = 0  
            tot-ytd-budget2          = 0
            tot-ytd-per2             = 0 .

    END.

    ASSIGN curr-flag = rev-list.flag
           curr-dept = rev-list.departement.
    IF rev-list.flag EQ "Room" THEN DO: 
        ASSIGN
            tot-today               = tot-today + rev-list.t-day
            tot-today-per           = tot-today-per + rev-list.dper     
            tot-mtd                 = tot-mtd + rev-list.mtd           
            tot-mtd-per             = tot-mtd-per + rev-list.mtd-per       
            tot-mtd-budget          = tot-mtd-budget + rev-list.mtd-budget    
            tot-variance            = tot-variance + rev-list.variance       
            tot-ytd                 = tot-ytd + rev-list.ytd
            tot-ytd-budget          = tot-ytd-budget + rev-list.ytd-budget
            tot-ytd-per             = tot-ytd-per + rev-list.ytd-per.
    END.
    ELSE IF rev-list.flag EQ "Other"  THEN DO:
        ASSIGN
            tot-today1               = tot-today1 + rev-list.t-day
            tot-today-per1           = tot-today-per1 + rev-list.dper     
            tot-mtd1                 = tot-mtd1 + rev-list.mtd           
            tot-mtd-per1             = tot-mtd-per1 + rev-list.mtd-per       
            tot-mtd-budget1          = tot-mtd-budget1 + rev-list.mtd-budget    
            tot-variance1            = tot-variance1 + rev-list.variance       
            tot-ytd1                 = tot-ytd1 + rev-list.ytd
            tot-ytd-budget1          = tot-ytd-budget1 + rev-list.ytd-budget
            tot-ytd-per1             = tot-ytd-per1 + rev-list.ytd-per.
    END.
    ELSE IF rev-list.flag EQ "Outlet" THEN DO:
        ASSIGN
            tot-today2               = tot-today2 + rev-list.t-day
            tot-today-per2           = tot-today-per2 + rev-list.dper     
            tot-mtd2                 = tot-mtd2 + rev-list.mtd           
            tot-mtd-per2             = tot-mtd-per2 + rev-list.mtd-per       
            tot-mtd-budget2          = tot-mtd-budget2 + rev-list.mtd-budget    
            tot-variance2            = tot-variance2 + rev-list.variance       
            tot-ytd2                 = tot-ytd2 + rev-list.ytd
            tot-ytd-budget2          = tot-ytd-budget2 + rev-list.ytd-budget
            tot-ytd-per2             = tot-ytd-per2 + rev-list.ytd-per.
    END.

END.


CREATE b-rev-list.
ASSIGN
    b-rev-list.ct            = ct + 1
    b-rev-list.descr         = "TOTAL ROOM REVENUE"
    b-rev-list.departement   = 0
    b-rev-list.t-day         = tot-today     
    b-rev-list.dper          = tot-today-per 
    b-rev-list.mtd           = tot-mtd       
    b-rev-list.mtd-per       = tot-mtd-per   
    b-rev-list.mtd-budget    = tot-mtd-budget
    b-rev-list.variance      = tot-variance  
    b-rev-list.ytd           = tot-ytd       
    b-rev-list.ytd-budget    = tot-ytd-budget
    b-rev-list.ytd-per       = tot-ytd-per   
    b-rev-list.flag          = "Room".

FOR EACH brev-list NO-LOCK :
    IF SUBSTR(brev-list.descr,1,5) EQ "TOTAL" THEN
     ASSIGN
        t-today      =  t-today      +  brev-list.t-day      
        t-today-per  =  t-today-per   +  brev-list.dper       
        t-mtd        =  t-mtd         +  brev-list.mtd        
        t-mtd-per    =  t-mtd-per     +  brev-list.mtd-per    
        t-mtd-budget =  t-mtd-budget  +  brev-list.mtd-budget 
        t-variance   =  t-variance    +  brev-list.variance   
        t-ytd        =  t-ytd         +  brev-list.ytd        
        t-ytd-budget =  t-ytd-budget  +  brev-list.ytd-budget 
        t-ytd-per    =  t-ytd-per     +  brev-list.ytd-per.    
END.


ct = ct + 1 + 1.

CREATE rev-list.
ASSIGN
    rev-list.ct            = ct
    rev-list.descr         = "TOTAL NETT REVENUE"
    rev-list.departement   = 100
    rev-list.t-day         = t-today     
    rev-list.dper          = 100 
    rev-list.mtd           = t-mtd       
    rev-list.mtd-per       = 100   
    rev-list.mtd-budget    = t-mtd-budget
    rev-list.variance      = t-variance  
    rev-list.ytd           = t-ytd       
    rev-list.ytd-budget    = t-ytd-budget
    rev-list.ytd-per       = 100   
    rev-list.flag          = "D".

FOR EACH rev-list NO-LOCK BY rev-list.flag :
    IF rev-list.t-day NE 0 THEN rev-list.dper  = (rev-list.t-day / t-today) * 100.
    IF rev-list.mtd NE 0 THEN rev-list.mtd-per = (rev-list.mtd / t-mtd) * 100.
    IF rev-list.ytd NE 0 THEN rev-list.ytd-per = (rev-list.ytd / t-ytd) * 100.
END. 

ct = ct + 1.
CREATE rev-list.
ASSIGN
    rev-list.ct            = ct
    rev-list.descr         = "Service Charge"
    rev-list.departement   = 101
    rev-list.t-day         = t-day-serv     
    rev-list.dper          = 100 
    rev-list.mtd           = mtd-serv       
    rev-list.mtd-per       = 100   
    rev-list.mtd-budget    = 0
    rev-list.variance      = 0  
    rev-list.ytd           = ytd-serv       
    rev-list.ytd-budget    = 0
    rev-list.ytd-per       = 100   
    rev-list.flag          = "B".

ct = ct + 1.
CREATE rev-list.
ASSIGN
    rev-list.ct            = ct
    rev-list.descr         = "Government Tax"
    rev-list.departement   = 101
    rev-list.t-day         = t-day-tax     
    rev-list.dper          = 100 
    rev-list.mtd           = mtd-tax       
    rev-list.mtd-per       = 100   
    rev-list.mtd-budget    = 0
    rev-list.variance      = 0  
    rev-list.ytd           = ytd-tax       
    rev-list.ytd-budget    = 0
    rev-list.ytd-per       = 100   
    rev-list.flag          = "C".

ct = ct + 1.
CREATE rev-list.
ASSIGN
    rev-list.ct            = ct
    rev-list.descr         = "TOTAL GROSS REVENUE"
    rev-list.departement   = 102
    rev-list.t-day         = t-day-serv + t-day-tax + t-today       
    rev-list.dper          = 100 
    rev-list.mtd           = mtd-serv + mtd-tax + t-mtd        
    rev-list.mtd-per       = 100   
    rev-list.mtd-budget    = 0
    rev-list.variance      = 0  
    rev-list.ytd           = ytd-serv + ytd-tax + t-ytd       
    rev-list.ytd-budget    = 0
    rev-list.ytd-per       = 100   
    rev-list.flag          = "A".


FOR EACH payment-list NO-LOCK BY payment-list.flag BY payment-list.departement:
    IF curr-flag1 NE "" AND (curr-flag1 NE payment-list.flag) THEN DO:
        IF curr-flag = "1Cash" THEN DO:
            CREATE b-payment-list.
            ASSIGN
                b-payment-list.ct           = ct2 + 1
                b-payment-list.descr        = "TOTAL CASH"
                b-payment-list.departement  = 0
                b-payment-list.t-day        = tot-today3      
                b-payment-list.mtd          = tot-mtd3        
                b-payment-list.mtd-budget   = tot-mtd-budget3 
                b-payment-list.variance     = tot-variance3   
                b-payment-list.ytd          = tot-ytd3        
                b-payment-list.ytd-budget   = tot-ytd-budget3 
                b-payment-list.flag         = "1Cash"
                tot-today3                  = 0
                tot-mtd3                    = 0
                tot-mtd-budget3             = 0
                tot-variance3               = 0
                tot-ytd3                    = 0
                tot-ytd-budget3             = 0.
        END.
        IF curr-flag = "2Payment" THEN DO:
            CREATE b-payment-list.
            ASSIGN
                b-payment-list.ct           = ct2 + 1
                b-payment-list.descr        = "TOTAL CREDIT CARD"
                b-payment-list.departement  = 0
                b-payment-list.t-day        = tot-today4      
                b-payment-list.mtd          = tot-mtd4        
                b-payment-list.mtd-budget   = tot-mtd-budget4 
                b-payment-list.variance     = tot-variance4   
                b-payment-list.ytd          = tot-ytd4        
                b-payment-list.ytd-budget   = tot-ytd-budget4 
                b-payment-list.flag         = "2Payment"
                tot-today4                  = 0
                tot-mtd4                    = 0
                tot-mtd-budget4             = 0
                tot-variance4               = 0
                tot-ytd4                    = 0
                tot-ytd-budget4             = 0.
        END.
        IF curr-flag = "3Ledger" THEN DO:
            CREATE b-payment-list.
            ASSIGN
                b-payment-list.ct           = ct2 + 1
                b-payment-list.descr        = "TOTAL CITY LEDGER"
                b-payment-list.departement  = 0
                b-payment-list.t-day        = tot-today5      
                b-payment-list.mtd          = tot-mtd5        
                b-payment-list.mtd-budget   = tot-mtd-budget5 
                b-payment-list.variance     = tot-variance5   
                b-payment-list.ytd          = tot-ytd5        
                b-payment-list.ytd-budget   = tot-ytd-budget5 
                b-payment-list.flag         = "3Ledger"
                tot-today5                  = 0
                tot-mtd5                    = 0
                tot-mtd-budget5             = 0
                tot-variance5               = 0
                tot-ytd5                    = 0
                tot-ytd-budget5             = 0.
        END.
        IF curr-flag = "4Foreign" THEN DO:
            CREATE b-payment-list.
            ASSIGN
                b-payment-list.ct           = ct2 + 1
                b-payment-list.descr        = "TOTAL FOREIGN"
                b-payment-list.departement  = 0
                b-payment-list.t-day        = tot-today6      
                b-payment-list.mtd          = tot-mtd6        
                b-payment-list.mtd-budget   = tot-mtd-budget6 
                b-payment-list.variance     = tot-variance6   
                b-payment-list.ytd          = tot-ytd6        
                b-payment-list.ytd-budget   = tot-ytd-budget6 
                b-payment-list.flag         = "4Foreign"
                tot-today6                  = 0
                tot-mtd6                    = 0
                tot-mtd-budget6             = 0
                tot-variance6               = 0
                tot-ytd6                    = 0
                tot-ytd-budget6             = 0.
        END.
        IF curr-flag = "4Foreign" THEN DO:
            CREATE b-payment-list.
            ASSIGN
                b-payment-list.ct           = ct2 + 1
                b-payment-list.descr        = "TOTAL FOREIGN"
                b-payment-list.departement  = 0
                b-payment-list.t-day        = tot-today6      
                b-payment-list.mtd          = tot-mtd6        
                b-payment-list.mtd-budget   = tot-mtd-budget6 
                b-payment-list.variance     = tot-variance6   
                b-payment-list.ytd          = tot-ytd6        
                b-payment-list.ytd-budget   = tot-ytd-budget6 
                b-payment-list.flag         = "4Foreign"
                tot-today6                  = 0
                tot-mtd6                    = 0
                tot-mtd-budget6             = 0
                tot-variance6               = 0
                tot-ytd6                    = 0
                tot-ytd-budget6             = 0.
        END.
        IF curr-flag = "5Deposit" THEN DO:
            CREATE b-payment-list.
            ASSIGN
                b-payment-list.ct           = ct2 + 1
                b-payment-list.descr        = "TOTAL ADVANCE DEPOSIT"
                b-payment-list.departement  = 0
                b-payment-list.t-day        = tot-today7      
                b-payment-list.mtd          = tot-mtd7        
                b-payment-list.mtd-budget   = tot-mtd-budget7 
                b-payment-list.variance     = tot-variance7   
                b-payment-list.ytd          = tot-ytd7        
                b-payment-list.ytd-budget   = tot-ytd-budget7 
                b-payment-list.flag         = "5Deposit"
                tot-today7                  = 0
                tot-mtd7                    = 0
                tot-mtd-budget7             = 0
                tot-variance7               = 0
                tot-ytd7                    = 0
                tot-ytd-budget7             = 0.
        END.
        
    END.
        
    ASSIGN curr-flag = payment-list.flag.

    IF payment-list.flag EQ "1Cash" THEN DO:
        ASSIGN 
            tot-today3                  = tot-today3       + payment-list.t-day     
            tot-mtd3                    = tot-mtd3         + payment-list.mtd                  
            tot-mtd-budget3             = tot-mtd-budget3  + payment-list.mtd-budget           
            tot-variance3               = tot-variance3    + payment-list.variance             
            tot-ytd3                    = tot-ytd3         + payment-list.ytd                  
            tot-ytd-budget3             = tot-ytd-budget3  + payment-list.ytd-budget.           
     END.
     IF payment-list.flag EQ "2Payment" THEN DO:
        ASSIGN 
            tot-today4                  = tot-today4       + payment-list.t-day     
            tot-mtd4                    = tot-mtd4         + payment-list.mtd                  
            tot-mtd-budget4             = tot-mtd-budget4  + payment-list.mtd-budget           
            tot-variance4               = tot-variance4    + payment-list.variance             
            tot-ytd4                    = tot-ytd4         + payment-list.ytd                  
            tot-ytd-budget4             = tot-ytd-budget4  + payment-list.ytd-budget.           
     END.
     IF payment-list.flag EQ "3Ledger" THEN DO:
        ASSIGN 
            tot-today5                  = tot-today5       + payment-list.t-day     
            tot-mtd5                    = tot-mtd5         + payment-list.mtd                  
            tot-mtd-budget5             = tot-mtd-budget5  + payment-list.mtd-budget           
            tot-variance5               = tot-variance5    + payment-list.variance             
            tot-ytd5                    = tot-ytd5         + payment-list.ytd                  
            tot-ytd-budget5             = tot-ytd-budget5  + payment-list.ytd-budget.           
     END.
     IF payment-list.flag EQ "4Foreign" THEN DO:
        ASSIGN 
            tot-today6                  = tot-today6       + payment-list.t-day     
            tot-mtd6                    = tot-mtd6         + payment-list.mtd                  
            tot-mtd-budget6             = tot-mtd-budget6  + payment-list.mtd-budget           
            tot-variance6               = tot-variance6    + payment-list.variance             
            tot-ytd6                    = tot-ytd6         + payment-list.ytd                  
            tot-ytd-budget6             = tot-ytd-budget6  + payment-list.ytd-budget.           
     END.
     IF payment-list.flag EQ "5Deposit" THEN DO:
        ASSIGN 
            tot-today7                  = tot-today7       + payment-list.t-day     
            tot-mtd7                    = tot-mtd7         + payment-list.mtd                  
            tot-mtd-budget7             = tot-mtd-budget7  + payment-list.mtd-budget           
            tot-variance7               = tot-variance7    + payment-list.variance             
            tot-ytd7                    = tot-ytd7         + payment-list.ytd                  
            tot-ytd-budget7             = tot-ytd-budget7  + payment-list.ytd-budget.           
     END.


END.

CREATE b-payment-list.
ASSIGN
    b-payment-list.ct           = ct2 + 1          
    b-payment-list.descr        = "TOTAL CASH"     
    b-payment-list.departement  = 0                
    b-payment-list.t-day        = tot-today3       
    b-payment-list.mtd          = tot-mtd3         
    b-payment-list.mtd-budget   = tot-mtd-budget3  
    b-payment-list.variance     = tot-variance3    
    b-payment-list.ytd          = tot-ytd3         
    b-payment-list.ytd-budget   = tot-ytd-budget3  
    b-payment-list.flag         = "1Cash". 

CREATE b-payment-list.
ASSIGN
    b-payment-list.ct           = ct2 + 1          
    b-payment-list.descr        = "TOTAL CREDIT CARD"     
    b-payment-list.departement  = 0                
    b-payment-list.t-day        = tot-today4       
    b-payment-list.mtd          = tot-mtd4         
    b-payment-list.mtd-budget   = tot-mtd-budget4  
    b-payment-list.variance     = tot-variance4    
    b-payment-list.ytd          = tot-ytd4         
    b-payment-list.ytd-budget   = tot-ytd-budget4  
    b-payment-list.flag         = "2Payment".

CREATE b-payment-list.
ASSIGN
    b-payment-list.ct           = ct2 + 1          
    b-payment-list.descr        = "TOTAL CITY LEDGER"     
    b-payment-list.departement  = 0                
    b-payment-list.t-day        = tot-today5       
    b-payment-list.mtd          = tot-mtd5         
    b-payment-list.mtd-budget   = tot-mtd-budget5  
    b-payment-list.variance     = tot-variance5    
    b-payment-list.ytd          = tot-ytd5         
    b-payment-list.ytd-budget   = tot-ytd-budget5  
    b-payment-list.flag         = "3Ledger".

CREATE b-payment-list.
ASSIGN
    b-payment-list.ct           = ct2 + 1          
    b-payment-list.descr        = "TOTAL FOREIGN"     
    b-payment-list.departement  = 0                
    b-payment-list.t-day        = tot-today6       
    b-payment-list.mtd          = tot-mtd6         
    b-payment-list.mtd-budget   = tot-mtd-budget6  
    b-payment-list.variance     = tot-variance6    
    b-payment-list.ytd          = tot-ytd6         
    b-payment-list.ytd-budget   = tot-ytd-budget6  
    b-payment-list.flag         = "4Foreign".

CREATE b-payment-list.
ASSIGN
    b-payment-list.ct           = ct2 + 1          
    b-payment-list.descr        = "TOTAL ADVANCE DEPOSIT"     
    b-payment-list.departement  = 0                
    b-payment-list.t-day        = tot-today7       
    b-payment-list.mtd          = tot-mtd7         
    b-payment-list.mtd-budget   = tot-mtd-budget7  
    b-payment-list.variance     = tot-variance7    
    b-payment-list.ytd          = tot-ytd7         
    b-payment-list.ytd-budget   = tot-ytd-budget7  
    b-payment-list.flag         = "5Deposit".


FOR EACH b-rev-seg-list NO-LOCK :
     ASSIGN 
        t-today1      =  t-today1       +  b-rev-seg-list.t-day      
        t-mtd1        =  t-mtd1         +  b-rev-seg-list.mtd        
        t-mtd-budget1 =  t-mtd-budget1  +  b-rev-seg-list.mtd-budget 
        t-variance1   =  t-variance1    +  b-rev-seg-list.variance   
        t-ytd1        =  t-ytd1         +  b-rev-seg-list.ytd        
        t-ytd-budget1 =  t-ytd-budget1  +  b-rev-seg-list.ytd-budget. 
END.

CREATE rev-seg-list.
ASSIGN
    rev-seg-list.ct            = 9999
    rev-seg-list.descr         = "TOTAL OCCUPANCY BY GUEST SEGMENT"
    rev-seg-list.departement   = 100
    rev-seg-list.t-day         = t-today1     
    rev-seg-list.dper          = 100 
    rev-seg-list.mtd           = t-mtd1       
    rev-seg-list.mtd-per       = 100   
    rev-seg-list.mtd-budget    = t-mtd-budget1
    rev-seg-list.variance      = t-variance1  
    rev-seg-list.ytd           = t-ytd1       
    rev-seg-list.ytd-budget    = t-ytd-budget1
    rev-seg-list.ytd-per       = 100   
    rev-seg-list.flag          = "ZZ Total".

FOR EACH rev-seg-list NO-LOCK:
    IF rev-seg-list.t-day NE 0 THEN rev-seg-list.dper     = (rev-seg-list.t-day / t-today1) * 100.                         
    IF rev-seg-list.mtd NE 0 THEN rev-seg-list.mtd-per    = (rev-seg-list.mtd / t-mtd1) * 100.
    IF rev-seg-list.ytd NE 0 THEN rev-seg-list.ytd-per    = (rev-seg-list.ytd / t-ytd1) * 100.
END.


FOR EACH b-rev-seg-list1 NO-LOCK :
     ASSIGN 
        t-today11      =  t-today11       +  b-rev-seg-list1.t-day      
        t-mtd11        =  t-mtd11         +  b-rev-seg-list1.mtd        
        t-mtd-budget11 =  t-mtd-budget11  +  b-rev-seg-list1.mtd-budget 
        t-variance11   =  t-variance11    +  b-rev-seg-list1.variance   
        t-ytd11        =  t-ytd11         +  b-rev-seg-list1.ytd        
        t-ytd-budget11 =  t-ytd-budget11  +  b-rev-seg-list1.ytd-budget. 
END.

CREATE rev-seg-list1.
ASSIGN
    rev-seg-list1.ct            = 9999
    rev-seg-list1.descr         = "TOTAL LODGING BY GUEST SEGMENT"
    rev-seg-list1.departement   = 100
    rev-seg-list1.t-day         = t-today11     
    rev-seg-list1.dper          = 100 
    rev-seg-list1.mtd           = t-mtd11       
    rev-seg-list1.mtd-per       = 100   
    rev-seg-list1.mtd-budget    = t-mtd-budget11
    rev-seg-list1.variance      = t-variance11  
    rev-seg-list1.ytd           = t-ytd11       
    rev-seg-list1.ytd-budget    = t-ytd-budget11
    rev-seg-list1.ytd-per       = 100   
    rev-seg-list1.flag          = "ZZ Total".

FOR EACH rev-seg-list1 NO-LOCK:
    IF rev-seg-list1.t-day NE 0 THEN rev-seg-list1.dper     = (rev-seg-list1.t-day / t-today11) * 100.                         
    IF rev-seg-list1.mtd NE 0 THEN rev-seg-list1.mtd-per    = (rev-seg-list1.mtd / t-mtd11) * 100.
    IF rev-seg-list1.ytd NE 0 THEN rev-seg-list1.ytd-per    = (rev-seg-list1.ytd / t-ytd11) * 100.
END.


FOR EACH bpayment-list NO-LOCK:
    IF SUBSTR(bpayment-list.descr,1,5) EQ "TOTAL" THEN
         ASSIGN
            t-today2      =  t-today2       +  bpayment-list.t-day      
            t-mtd2        =  t-mtd2         +  bpayment-list.mtd        
            t-mtd-budget2 =  t-mtd-budget2  +  bpayment-list.mtd-budget 
            t-variance2   =  t-variance2    +  bpayment-list.variance   
            t-ytd2        =  t-ytd2         +  bpayment-list.ytd    
            t-ytd-budget2 =  t-ytd-budget2  +  bpayment-list.ytd-budget. 
END.

CREATE payment-list.
ASSIGN
    payment-list.ct            = 9999
    payment-list.descr         = "TOTAL PAYMENT"
    payment-list.departement   = 100
    payment-list.t-day         = t-today2     
    payment-list.mtd           = t-mtd2       
    payment-list.mtd-budget    = t-mtd-budget2
    payment-list.variance      = t-variance2  
    payment-list.ytd           = t-ytd2       
    payment-list.ytd-budget    = t-ytd-budget2
    payment-list.flag          = "ZZ Total".

FOR EACH bpayable-list NO-LOCK:
    ASSIGN 
        t-today3      =  t-today3       +  bpayable-list.t-day      
        t-today-per3  =  t-today-per3   +  bpayable-list.dper       
        t-mtd3        =  t-mtd3         +  bpayable-list.mtd        
        t-mtd-per3    =  t-mtd-per3     +  bpayable-list.mtd-per    
        t-mtd-budget3 =  t-mtd-budget3  +  bpayable-list.mtd-budget 
        t-variance3   =  t-variance3    +  bpayable-list.variance   
        t-ytd3        =  t-ytd3         +  bpayable-list.ytd        
        t-ytd-budget3 =  t-ytd-budget3  +  bpayable-list.ytd-budget 
        t-ytd-per3    =  t-ytd-per3     +  bpayable-list.ytd-per.
END.



IF t-today3 = 0 THEN dper = 0.
ELSE dper = 100.
IF t-mtd3 = 0 THEN mtd-per = 0.
ELSE mtd-per = 100.
IF t-ytd3 = 0 THEN ytd-per = 0.
ELSE ytd-per = 100.

CREATE payable-list.
ASSIGN 
    payable-list.ct            = 9999
    payable-list.descr         = "TOTAL PAYABLE"
    payable-list.departement   = 100
    payable-list.t-day         = t-today3     
    payable-list.dper          = dper
    payable-list.mtd           = t-mtd3       
    payable-list.mtd-per       = mtd-per   
    payable-list.mtd-budget    = t-mtd-budget3
    payable-list.variance      = t-variance3  
    payable-list.ytd           = t-ytd3       
    payable-list.ytd-budget    = t-ytd-budget3
    payable-list.ytd-per       = ytd-per   
    payable-list.flag          = "ZZ Total".


FOR EACH payable-list NO-LOCK :
   IF payable-list.t-day NE 0 THEN payable-list.dper     = (payable-list.t-day / t-today3) * 100.                         
   IF payable-list.mtd NE 0 THEN payable-list.mtd-per    = (payable-list.mtd / t-mtd3) * 100.
   IF payable-list.ytd NE 0 THEN payable-list.ytd-per    = (payable-list.ytd / t-ytd3) * 100.
END.

FOR EACH fb-sales-food NO-LOCK BY fb-sales-food.departement:
    ASSIGN tot-tday-cov = tot-tday-cov + fb-sales-food.tday-cov
           tot-tday-avg = tot-tday-avg + fb-sales-food.tday-avg
           tot-tday-rev = tot-tday-rev + fb-sales-food.tday-rev
           tot-mtd-cov  = tot-mtd-cov  + fb-sales-food.mtd-cov 
           tot-mtd-avg  = tot-mtd-avg  + fb-sales-food.mtd-avg 
           tot-mtd-rev  = tot-mtd-rev  + fb-sales-food.mtd-rev 
           tot-ytd-cov  = tot-ytd-cov  + fb-sales-food.ytd-cov 
           tot-ytd-avg  = tot-ytd-avg  + fb-sales-food.ytd-avg 
           tot-ytd-rev  = tot-ytd-rev  + fb-sales-food.ytd-rev.
END.

CREATE fb-sales-food.
ASSIGN fb-sales-food.ct          = 9999                          
       fb-sales-food.departement = 0 
       fb-sales-food.artnr       = 0         
       fb-sales-food.descr       = "TOTAL FOOD"             
       fb-sales-food.tday-cov    = tot-tday-cov                   
       fb-sales-food.tday-avg    = tot-tday-avg                   
       fb-sales-food.tday-rev    = tot-tday-rev                   
       fb-sales-food.mtd-cov     = tot-mtd-cov                    
       fb-sales-food.mtd-avg     = tot-mtd-avg                    
       fb-sales-food.mtd-rev     = tot-mtd-rev                    
       fb-sales-food.ytd-cov     = tot-ytd-cov                    
       fb-sales-food.ytd-avg     = tot-ytd-avg                    
       fb-sales-food.ytd-rev     = tot-ytd-rev                    
       fb-sales-food.flag        = "1Food".

CREATE fb-sales-tot.
ASSIGN fb-sales-tot.ct          = 1                                   
       fb-sales-tot.descr       = "TOTAL FOOD"             
       fb-sales-tot.tday-cov    = tot-tday-cov                   
       fb-sales-tot.tday-avg    = tot-tday-avg                   
       fb-sales-tot.tday-rev    = tot-tday-rev                   
       fb-sales-tot.mtd-cov     = tot-mtd-cov                    
       fb-sales-tot.mtd-avg     = tot-mtd-avg                    
       fb-sales-tot.mtd-rev     = tot-mtd-rev                    
       fb-sales-tot.ytd-cov     = tot-ytd-cov                    
       fb-sales-tot.ytd-avg     = tot-ytd-avg                    
       fb-sales-tot.ytd-rev     = tot-ytd-rev                    
       fb-sales-tot.flag        = "1Food"
       tot-tday-cov = 0
       tot-tday-avg = 0
       tot-tday-rev = 0
       tot-mtd-cov  = 0
       tot-mtd-avg  = 0
       tot-mtd-rev  = 0
       tot-ytd-cov  = 0
       tot-ytd-avg  = 0
       tot-ytd-rev  = 0.

FOR EACH fb-sales-beverage NO-LOCK BY fb-sales-beverage.departement:
    ASSIGN tot-tday-cov = tot-tday-cov + fb-sales-beverage.tday-cov
           tot-tday-avg = tot-tday-avg + fb-sales-beverage.tday-avg
           tot-tday-rev = tot-tday-rev + fb-sales-beverage.tday-rev
           tot-mtd-cov  = tot-mtd-cov  + fb-sales-beverage.mtd-cov 
           tot-mtd-avg  = tot-mtd-avg  + fb-sales-beverage.mtd-avg 
           tot-mtd-rev  = tot-mtd-rev  + fb-sales-beverage.mtd-rev 
           tot-ytd-cov  = tot-ytd-cov  + fb-sales-beverage.ytd-cov 
           tot-ytd-avg  = tot-ytd-avg  + fb-sales-beverage.ytd-avg 
           tot-ytd-rev  = tot-ytd-rev  + fb-sales-beverage.ytd-rev.
END.

CREATE fb-sales-beverage.
ASSIGN fb-sales-beverage.ct          = 9999                          
       fb-sales-beverage.departement = 0 
       fb-sales-beverage.artnr       = 0         
       fb-sales-beverage.descr       = "TOTAL BEVERAGE"             
       fb-sales-beverage.tday-cov    = tot-tday-cov                   
       fb-sales-beverage.tday-avg    = tot-tday-avg                   
       fb-sales-beverage.tday-rev    = tot-tday-rev                   
       fb-sales-beverage.mtd-cov     = tot-mtd-cov                    
       fb-sales-beverage.mtd-avg     = tot-mtd-avg                    
       fb-sales-beverage.mtd-rev     = tot-mtd-rev                    
       fb-sales-beverage.ytd-cov     = tot-ytd-cov                    
       fb-sales-beverage.ytd-avg     = tot-ytd-avg                    
       fb-sales-beverage.ytd-rev     = tot-ytd-rev                    
       fb-sales-beverage.flag        = "2Beverage".

CREATE fb-sales-tot.
ASSIGN fb-sales-tot.ct          = 2                                  
       fb-sales-tot.descr       = "TOTAL BEVERAGE"             
       fb-sales-tot.tday-cov    = tot-tday-cov                   
       fb-sales-tot.tday-avg    = tot-tday-avg                   
       fb-sales-tot.tday-rev    = tot-tday-rev                   
       fb-sales-tot.mtd-cov     = tot-mtd-cov                    
       fb-sales-tot.mtd-avg     = tot-mtd-avg                    
       fb-sales-tot.mtd-rev     = tot-mtd-rev                    
       fb-sales-tot.ytd-cov     = tot-ytd-cov                    
       fb-sales-tot.ytd-avg     = tot-ytd-avg                    
       fb-sales-tot.ytd-rev     = tot-ytd-rev                    
       fb-sales-tot.flag        = "2Beverage"
       tot-tday-cov = 0
       tot-tday-avg = 0
       tot-tday-rev = 0
       tot-mtd-cov  = 0
       tot-mtd-avg  = 0
       tot-mtd-rev  = 0
       tot-ytd-cov  = 0
       tot-ytd-avg  = 0
       tot-ytd-rev  = 0.

FOR EACH fb-sales-material NO-LOCK BY fb-sales-material.departement:
    ASSIGN tot-tday-cov = tot-tday-cov + fb-sales-material.tday-cov
           tot-tday-avg = tot-tday-avg + fb-sales-material.tday-avg
           tot-tday-rev = tot-tday-rev + fb-sales-material.tday-rev
           tot-mtd-cov  = tot-mtd-cov  + fb-sales-material.mtd-cov 
           tot-mtd-avg  = tot-mtd-avg  + fb-sales-material.mtd-avg 
           tot-mtd-rev  = tot-mtd-rev  + fb-sales-material.mtd-rev 
           tot-ytd-cov  = tot-ytd-cov  + fb-sales-material.ytd-cov 
           tot-ytd-avg  = tot-ytd-avg  + fb-sales-material.ytd-avg 
           tot-ytd-rev  = tot-ytd-rev  + fb-sales-material.ytd-rev.
END.

CREATE fb-sales-material.
ASSIGN fb-sales-material.ct          = 9999                          
       fb-sales-material.departement = 0 
       fb-sales-material.artnr       = 0         
       fb-sales-material.descr       = "TOTAL MATERIAL"             
       fb-sales-material.tday-cov    = tot-tday-cov                   
       fb-sales-material.tday-avg    = tot-tday-avg                   
       fb-sales-material.tday-rev    = tot-tday-rev                   
       fb-sales-material.mtd-cov     = tot-mtd-cov                    
       fb-sales-material.mtd-avg     = tot-mtd-avg                    
       fb-sales-material.mtd-rev     = tot-mtd-rev                    
       fb-sales-material.ytd-cov     = tot-ytd-cov                    
       fb-sales-material.ytd-avg     = tot-ytd-avg                    
       fb-sales-material.ytd-rev     = tot-ytd-rev                    
       fb-sales-material.flag        = "4Material".

CREATE fb-sales-tot.
ASSIGN fb-sales-tot.ct          = 3                                   
       fb-sales-tot.descr       = "TOTAL MATRIAL"             
       fb-sales-tot.tday-cov    = tot-tday-cov                   
       fb-sales-tot.tday-avg    = tot-tday-avg                   
       fb-sales-tot.tday-rev    = tot-tday-rev                   
       fb-sales-tot.mtd-cov     = tot-mtd-cov                    
       fb-sales-tot.mtd-avg     = tot-mtd-avg                    
       fb-sales-tot.mtd-rev     = tot-mtd-rev                    
       fb-sales-tot.ytd-cov     = tot-ytd-cov                    
       fb-sales-tot.ytd-avg     = tot-ytd-avg                    
       fb-sales-tot.ytd-rev     = tot-ytd-rev                    
       fb-sales-tot.flag        = "4Material"
       tot-tday-cov = 0
       tot-tday-avg = 0
       tot-tday-rev = 0
       tot-mtd-cov  = 0
       tot-mtd-avg  = 0
       tot-mtd-rev  = 0
       tot-ytd-cov  = 0
       tot-ytd-avg  = 0
       tot-ytd-rev  = 0.

FOR EACH fb-sales-other NO-LOCK BY fb-sales-other.departement:
    ASSIGN tot-tday-cov = tot-tday-cov + fb-sales-other.tday-cov
           tot-tday-avg = tot-tday-avg + fb-sales-other.tday-avg
           tot-tday-rev = tot-tday-rev + fb-sales-other.tday-rev
           tot-mtd-cov  = tot-mtd-cov  + fb-sales-other.mtd-cov 
           tot-mtd-avg  = tot-mtd-avg  + fb-sales-other.mtd-avg 
           tot-mtd-rev  = tot-mtd-rev  + fb-sales-other.mtd-rev 
           tot-ytd-cov  = tot-ytd-cov  + fb-sales-other.ytd-cov 
           tot-ytd-avg  = tot-ytd-avg  + fb-sales-other.ytd-avg 
           tot-ytd-rev  = tot-ytd-rev  + fb-sales-other.ytd-rev.
END.

CREATE fb-sales-other.
ASSIGN fb-sales-other.ct          = 9999                          
       fb-sales-other.departement = 0 
       fb-sales-other.artnr       = 0         
       fb-sales-other.descr       = "TOTAL BANQUET"             
       fb-sales-other.tday-cov    = tot-tday-cov                   
       fb-sales-other.tday-avg    = tot-tday-avg                   
       fb-sales-other.tday-rev    = tot-tday-rev                   
       fb-sales-other.mtd-cov     = tot-mtd-cov                    
       fb-sales-other.mtd-avg     = tot-mtd-avg                    
       fb-sales-other.mtd-rev     = tot-mtd-rev                    
       fb-sales-other.ytd-cov     = tot-ytd-cov                    
       fb-sales-other.ytd-avg     = tot-ytd-avg                    
       fb-sales-other.ytd-rev     = tot-ytd-rev                    
       fb-sales-other.flag        = "3Banquet".

CREATE fb-sales-tot.
ASSIGN fb-sales-tot.ct          = 4                                  
       fb-sales-tot.descr       = "TOTAL OTHER"             
       fb-sales-tot.tday-cov    = tot-tday-cov                   
       fb-sales-tot.tday-avg    = tot-tday-avg                   
       fb-sales-tot.tday-rev    = tot-tday-rev                   
       fb-sales-tot.mtd-cov     = tot-mtd-cov                    
       fb-sales-tot.mtd-avg     = tot-mtd-avg                    
       fb-sales-tot.mtd-rev     = tot-mtd-rev                    
       fb-sales-tot.ytd-cov     = tot-ytd-cov                    
       fb-sales-tot.ytd-avg     = tot-ytd-avg                    
       fb-sales-tot.ytd-rev     = tot-ytd-rev                    
       fb-sales-tot.flag        = "3Banquet"
       tot-tday-cov = 0
       tot-tday-avg = 0
       tot-tday-rev = 0
       tot-mtd-cov  = 0
       tot-mtd-avg  = 0
       tot-mtd-rev  = 0
       tot-ytd-cov  = 0
       tot-ytd-avg  = 0
       tot-ytd-rev  = 0.

FOR EACH fb-sales-tot NO-LOCK BY fb-sales-tot.departement:
    ASSIGN tot-tday-cov = tot-tday-cov + fb-sales-tot.tday-cov
           tot-tday-avg = tot-tday-avg + fb-sales-tot.tday-avg
           tot-tday-rev = tot-tday-rev + fb-sales-tot.tday-rev
           tot-mtd-cov  = tot-mtd-cov  + fb-sales-tot.mtd-cov 
           tot-mtd-avg  = tot-mtd-avg  + fb-sales-tot.mtd-avg 
           tot-mtd-rev  = tot-mtd-rev  + fb-sales-tot.mtd-rev 
           tot-ytd-cov  = tot-ytd-cov  + fb-sales-tot.ytd-cov 
           tot-ytd-avg  = tot-ytd-avg  + fb-sales-tot.ytd-avg 
           tot-ytd-rev  = tot-ytd-rev  + fb-sales-tot.ytd-rev.
END.

CREATE fb-sales-tot.
ASSIGN fb-sales-tot.ct          = 5                                 
       fb-sales-tot.descr       = "TOTAL F&B REVENUE"             
       fb-sales-tot.tday-cov    = tot-tday-cov                   
       fb-sales-tot.tday-avg    = tot-tday-avg                   
       fb-sales-tot.tday-rev    = tot-tday-rev                   
       fb-sales-tot.mtd-cov     = tot-mtd-cov                    
       fb-sales-tot.mtd-avg     = tot-mtd-avg                    
       fb-sales-tot.mtd-rev     = tot-mtd-rev                    
       fb-sales-tot.ytd-cov     = tot-ytd-cov                    
       fb-sales-tot.ytd-avg     = tot-ytd-avg                    
       fb-sales-tot.ytd-rev     = tot-ytd-rev                    
       fb-sales-tot.flag        = "5Grand-total"
       tot-tday-cov = 0
       tot-tday-avg = 0
       tot-tday-rev = 0
       tot-mtd-cov  = 0
       tot-mtd-avg  = 0
       tot-mtd-rev  = 0
       tot-ytd-cov  = 0
       tot-ytd-avg  = 0
       tot-ytd-rev  = 0.

FIND FIRST rev-list WHERE rev-list.descr = "TOTAL GROSS REVENUE" NO-LOCK NO-ERROR.
IF AVAILABLE rev-list THEN DO:
    tdy-gl1 = rev-list.t-day.
END.

FIND FIRST payable-list WHERE payable-list.descr = "TOTAL PAYABLE" NO-LOCK NO-ERROR.
IF AVAILABLE payable-list THEN DO:
    tdy-gl1 = tdy-gl1 + payable-list.t-day.
END.

FIND FIRST payment-list WHERE payment-list.descr = "TOTAL PAYMENT" NO-LOCK NO-ERROR.
IF AVAILABLE payment-list THEN DO:
    tdy-gl1 = tdy-gl1 + payment-list.t-day.
END.

FIND FIRST uebertrag WHERE uebertrag.datum = to-date - 1 NO-LOCK NO-ERROR. 
IF AVAILABLE uebertrag THEN 
DO: 
  ytd-gl = uebertrag.betrag. 
END. 

FIND FIRST gl-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-list THEN DO:
    CREATE gl-list.
    ASSIGN gl-list.descr    = "Today Guest Ledger"
           gl-list.tot-rev  = tdy-gl1.
    CREATE gl-list.
    ASSIGN gl-list.descr    = "Yesterday Guest Ledger"
           gl-list.tot-rev  = ytd-gl.
    CREATE gl-list.
    ASSIGN gl-list.descr    = "TODAY BALANCE"
           gl-list.tot-rev  = tdy-gl1 + ytd-gl.
END.

RUN fill-tot-room. /*Agu*/
RUN fill-tot-avail.
RUN fill-inactive.
RUN fill-rmstat("ooo").
/*RUN fill-rmstat("oos").*/
RUN fill-rmocc. 
RUN fill-stat("vacant").
RUN fill-segm("HSE").
RUN fill-segm("COM").
RUN fill-comproomnew.
RUN fill-roomsold.
RUN fill-occ-pay.
RUN fill-occ-comp-hu.
RUN fill-tot-rev.
RUN fill-avg-rmrate-rp.
RUN fill-avg-rmrate-frg.
RUN fill-revpar.
RUN fill-rmstat("dayuse").
RUN fill-rmstat("No-Show").
RUN fill-rmstat("arrival-WIG").
RUN fill-rmstat("NewRes").
RUN fill-rmstat("CancRes").
RUN fill-rmstat("Early-CO").
RUN fill-rmstat("arrival").
RUN fill-rmstat("pers-arrival").
RUN fill-rmstat("departure").
RUN fill-rmstat("pers-depature").
RUN fill-rmstat("ArrTmrw").
RUN fill-rmstat("pers-ArrTmrw").
RUN fill-rmstat("DepTmrw").
RUN fill-rmstat("pers-DepTmrw").

PROCEDURE find-exrate: 
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
  IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
    AND exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. 
END.

PROCEDURE fill-revenue-segement:
DEFINE VARIABLE t-day            AS DECIMAL.
DEFINE VARIABLE mtd              AS DECIMAL.
DEFINE VARIABLE mtd-budget       AS DECIMAL.
DEFINE VARIABLE ytd              AS DECIMAL.
DEFINE VARIABLE ytd-budget       AS DECIMAL.
DEFINE VARIABLE variance         AS DECIMAL.
DEFINE VARIABLE ct1              AS INT.
DEFINE VARIABLE artnr            AS INT.
DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE mm AS INTEGER.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

    mm = MONTH(to-date).
    /*saldo*/
   
   
    ASSIGN artnr = setup-segment.artnr.

    FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode
      AND genstat.datum GE datum1 
      AND genstat.datum LE to-date 
      AND genstat.resstatus NE 13 
      /*AND genstat.gratis EQ 0 */
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] NO-LOCK:

        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(genstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 

        d-flag = (MONTH(genstat.datum) = MONTH(to-date))
             AND (YEAR(genstat.datum) = YEAR(to-date)).

        IF genstat.datum = to-date THEN DO:
            t-day = t-day + 1.   
        END.
        
        IF MONTH(genstat.datum) = mm THEN DO:
           mtd = mtd + mon-saldo[DAY(genstat.datum)] + 1.    
        END.

        ytd = ytd + 1.
    END.

    FOR EACH segmentstat WHERE segmentstat.datum GE datum1
    AND segmentstat.datum LE to-date
    AND segmentstat.segmentcode = segment.segmentcode NO-LOCK:

        IF MONTH(segmentstat.datum) = mm THEN DO:
           
           mtd-budget = mtd-budget + segmentstat.budzimmeranz.
        
        END.
        
        ytd-budget = ytd-budget + segmentstat.budzimmeranz.
    END.

    ASSIGN variance = mtd - mtd-budget.
    
    FIND FIRST rev-seg-list WHERE rev-seg-list.descr EQ setup-segment.descr NO-LOCK NO-ERROR.
    IF AVAILABLE rev-seg-list THEN DO:
        ASSIGN rev-seg-list.t-day        = rev-seg-list.t-day + t-day
               rev-seg-list.mtd          = rev-seg-list.mtd + mtd            
               rev-seg-list.mtd-budget   = rev-seg-list.mtd-budget + mtd-budget 
               rev-seg-list.ytd          = rev-seg-list.ytd + ytd        
               rev-seg-list.ytd-budget   = rev-seg-list.ytd-budget + ytd-budget
               rev-seg-list.variance     = rev-seg-list.variance + variance.
    END.
    ELSE DO:
        ct = ct + 1.
        CREATE rev-seg-list.
        ASSIGN rev-seg-list.ct           = ct
               rev-seg-list.segment-code = setup-segment.artnr 
               rev-seg-list.flag         = setup-segment.flag
               rev-seg-list.departement  = setup-segment.departement
               rev-seg-list.t-day        = t-day
               rev-seg-list.mtd          = mtd
               rev-seg-list.mtd-budget   = mtd-budget
               rev-seg-list.ytd          = ytd
               rev-seg-list.ytd-budget   = ytd-budget
               rev-seg-list.variance     = variance.
        
        IF setup-segment.flag-grup EQ YES THEN 
            ASSIGN rev-seg-list.descr = setup-segment.descr
                   rev-seg-list.flag-grup = YES.
        ELSE ASSIGN rev-seg-list.descr = segment.bezeich.    
    END.
END.

PROCEDURE fill-revenue-segement1:
    DEFINE VARIABLE t-day            AS DECIMAL.
    DEFINE VARIABLE mtd              AS DECIMAL.
    DEFINE VARIABLE mtd-budget       AS DECIMAL.
    DEFINE VARIABLE ytd              AS DECIMAL.
    DEFINE VARIABLE ytd-budget       AS DECIMAL.
    DEFINE VARIABLE variance         AS DECIMAL.
    DEFINE VARIABLE ct1              AS INT.
    DEFINE VARIABLE artnr            AS INT.
    DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
    DEFINE VARIABLE mm AS INTEGER.
    DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

    ASSIGN artnr = setup-segment.artnr.

    FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode
      AND genstat.datum GE datum1 
      AND genstat.datum LE to-date 
      AND genstat.resstatus NE 13 
      /*AND genstat.gratis EQ 0 */
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] NO-LOCK:

        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(genstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 

        d-flag = (MONTH(genstat.datum) = MONTH(to-date))
             AND (YEAR(genstat.datum) = YEAR(to-date)).

        IF genstat.datum = to-date THEN DO:
            t-day = t-day + genstat.logis.   
        END.
        
        IF MONTH(genstat.datum) = MONTH(to-date) THEN DO:
           mtd = mtd  + mon-saldo[DAY(genstat.datum)] +  genstat.logis.    
        END.

        ytd = ytd +  genstat.logis.
    END.

    FOR EACH segmentstat WHERE segmentstat.datum GE datum1
    AND segmentstat.datum LE to-date 
    AND segmentstat.segmentcode = segment.segmentcode NO-LOCK:
    
        IF MONTH(segmentstat.datum) = MONTH(to-date) THEN DO:
           mtd-budget = mtd-budget + segmentstat.budlogis.
        END.
        
        ytd-budget = ytd-budget + segmentstat.budlogis.

    END.
    ASSIGN variance = mtd - mtd-budget.
    
    FIND FIRST rev-seg-list1 WHERE rev-seg-list1.descr EQ setup-segment.descr NO-LOCK NO-ERROR.
    IF AVAILABLE rev-seg-list1 THEN DO:
        ASSIGN rev-seg-list1.t-day        = rev-seg-list1.t-day + t-day
               rev-seg-list1.mtd          = rev-seg-list1.mtd + mtd            
               rev-seg-list1.mtd-budget   = rev-seg-list1.mtd-budget + mtd-budget 
               rev-seg-list1.ytd          = rev-seg-list1.ytd + ytd        
               rev-seg-list1.ytd-budget   = rev-seg-list1.ytd-budget + ytd-budget
               rev-seg-list1.variance     = rev-seg-list1.variance + variance.
    END.
    ELSE DO:
        ct = ct + 1.
        CREATE rev-seg-list1.
        ASSIGN rev-seg-list1.ct           = ct
               rev-seg-list1.segment-code = setup-segment.artnr 
               rev-seg-list1.flag         = setup-segment.flag
               rev-seg-list1.departement  = setup-segment.departement
               rev-seg-list1.t-day        = t-day
               rev-seg-list1.mtd          = mtd
               rev-seg-list1.mtd-budget   = mtd-budget
               rev-seg-list1.ytd          = ytd
               rev-seg-list1.ytd-budget   = ytd-budget
               rev-seg-list1.variance     = variance.
        
        IF setup-segment.flag-grup EQ YES THEN 
            ASSIGN rev-seg-list1.descr = setup-segment.descr
                   rev-seg-list1.flag-grup = YES.
        ELSE ASSIGN rev-seg-list1.descr = segment.bezeich.    
    END.
END.

PROCEDURE create-rev-list:
DEFINE VARIABLE t-day            AS DECIMAL.
DEFINE VARIABLE mtd              AS DECIMAL.
DEFINE VARIABLE mtd-budget       AS DECIMAL.
DEFINE VARIABLE ytd              AS DECIMAL.
DEFINE VARIABLE ytd-budget       AS DECIMAL.
DEFINE VARIABLE variance         AS DECIMAL.

     DO curr-date = datum1 TO to-date: 
     ASSIGN 
         serv = 0
         vat  = 0.

         FIND FIRST umsatz WHERE umsatz.datum = curr-date 
           AND umsatz.artnr = artikel.artnr AND umsatz.departement = artikel.departement NO-LOCK NO-ERROR. 
         IF AVAILABLE umsatz THEN 

           RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                                  umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

         fact = 1.00 + serv + vat + vat2.

         d-flag = AVAILABLE umsatz AND (MONTH(umsatz.datum) = MONTH(to-date))
           AND (YEAR(umsatz.datum) = YEAR(to-date)).

         n-betrag = 0. 
         IF AVAILABLE umsatz THEN 
         DO: 
           IF foreign-flag THEN 
           DO:  
             RUN find-exrate(curr-date). 
             IF AVAILABLE exrate THEN frate = exrate.betrag. 
           END. 

           ASSIGN
             n-betrag = umsatz.betrag / (fact * frate) 
             n-serv   = n-betrag * serv
             n-tax    = n-betrag * vat.

           IF umsat.datum = to-date THEN
           ASSIGN t-day      = t-day + n-betrag
                  t-day-serv = t-day-serv + n-serv  
                  t-day-tax  = t-day-tax + n-tax.

           IF price-decimal = 0 THEN 
           DO:
             ASSIGN 
               n-betrag = ROUND(n-betrag, 0)
               n-serv = ROUND(n-serv, 0)
               n-tax = ROUND(n-tax, 0).
           END.
         END. 

         FIND FIRST budget WHERE budget.artnr = artikel.artnr 
         AND budget.departement = artikel.departement 
         AND budget.datum = curr-date NO-LOCK NO-ERROR.

         IF curr-date LT from-date THEN 
         DO: 
           IF AVAILABLE umsatz THEN 
               ASSIGN ytd       = ytd + n-betrag 
                      ytd-serv  = ytd-serv + n-serv
                      ytd-tax   = ytd-tax + n-tax.
           IF AVAILABLE budget THEN 
               ASSIGN ytd-budget = ytd-budget + budget.betrag. 
         END. 
         ELSE DO:
               IF AVAILABLE umsatz THEN 
               DO: 
                 IF ytd-flag THEN 
                     ASSIGN ytd = ytd + n-betrag
                            ytd-serv = ytd-serv + n-serv
                            ytd-tax = ytd-tax + n-tax. 
                 IF MONTH(curr-date) = MONTH(to-date) THEN 
                     ASSIGN mtd      = mtd + mon-saldo[DAY(umsatz.datum)] + n-betrag 
                            mtd-serv = mtd-serv + mon-saldo[DAY(umsatz.datum)] + n-serv
                            mtd-tax  = mtd-tax  + mon-saldo[DAY(umsatz.datum)] + n-tax.
               END. 

               IF AVAILABLE budget THEN 
               DO: 
                 mtd-budget = mtd-budget + budget.betrag.   
               END. 
         END.
         ASSIGN variance = mtd - mtd-budget.
     END.
    FIND FIRST rev-list WHERE rev-list.descr EQ setup-revenue.descr NO-LOCK NO-ERROR.
    IF AVAILABLE rev-list THEN DO:
        ASSIGN rev-list.t-day        = rev-list.t-day + t-day
               rev-list.mtd          = rev-list.mtd + mtd            
               rev-list.mtd-budget   = rev-list.mtd-budget + mtd-budget 
               rev-list.ytd          = rev-list.ytd + ytd        
               rev-list.ytd-budget   = rev-list.ytd-budget + ytd-budget
               rev-list.variance     = rev-list.variance + variance.
    END.
    ELSE DO:

        FIND FIRST rev-list WHERE rev-list.departement EQ setup-revenue.departement NO-LOCK NO-ERROR.
        IF NOT AVAILABLE rev-list THEN DO:
            ct = ct + 1.
            FIND FIRST hoteldpt WHERE hoteldpt.num EQ setup-revenue.departement NO-LOCK NO-ERROR.
            CREATE rev-list.
            ASSIGN rev-list.ct           = ct
                   rev-list.flag         = "zeich-dept"
                   rev-list.departement  = setup-revenue.departement
                   rev-list.descr        = hoteldpt.depart.
                   .    
        END.

        ct = ct + 1.
        CREATE rev-list.
        ASSIGN rev-list.ct           = ct
               rev-list.flag         = setup-revenue.flag
               rev-list.departement  = setup-revenue.departement
               rev-list.t-day        = t-day
               rev-list.mtd          = mtd
               rev-list.mtd-budget   = mtd-budget
               rev-list.ytd          = ytd
               rev-list.ytd-budget   = ytd-budget
               rev-list.variance     = variance.
        
        IF setup-revenue.flag-grup EQ YES THEN 
            ASSIGN rev-list.descr = setup-revenue.descr
                   rev-list.flag-grup = YES.
        ELSE ASSIGN rev-list.descr = artikel.bezeich. 
    END.
END.



PROCEDURE create-payable-list:
    CREATE payable-list.
    ASSIGN payable-list.descr        = artikel.bezeich
           payable-list.flag         = setup-revenue.flag
           payable-list.departement  = setup-revenue.departement.

     DO curr-date = datum1 TO to-date: 
     ASSIGN
         serv = 0
         vat  = 0.

         FIND FIRST umsatz WHERE umsatz.datum = curr-date 
           AND umsatz.artnr = artikel.artnr AND umsatz.departement = artikel.departement NO-LOCK NO-ERROR. 
         IF AVAILABLE umsatz THEN 

           RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                                  umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

         fact = 1.00 + serv + vat + vat2.

         d-flag = AVAILABLE umsatz AND (MONTH(umsatz.datum) = MONTH(to-date))
           AND (YEAR(umsatz.datum) = YEAR(to-date)).

         n-betrag = 0. 
         IF AVAILABLE umsatz THEN 
         DO: 
           IF foreign-flag THEN 
           DO:  
             RUN find-exrate(curr-date). 
             IF AVAILABLE exrate THEN frate = exrate.betrag. 
           END. 

           ASSIGN
             n-betrag = umsatz.betrag / (fact * frate) 
             n-serv   = n-betrag * serv
             n-tax    = n-betrag * vat.
            
           IF umsat.datum = to-date THEN
           ASSIGN payable-list.t-day = payable-list.t-day + (umsatz.betrag / (fact * frate)) .

           IF price-decimal = 0 THEN 
           DO:
             ASSIGN 
               n-betrag = ROUND(n-betrag, 0)
               n-serv = ROUND(n-serv, 0)
               n-tax = ROUND(n-tax, 0).
           END.
         END. 

         FIND FIRST budget WHERE budget.artnr = artikel.artnr 
         AND budget.departement = artikel.departement 
         AND budget.datum = curr-date NO-LOCK NO-ERROR.

         IF curr-date LT from-date THEN 
         DO: 
           IF AVAILABLE umsatz THEN payable-list.ytd = payable-list.ytd + n-betrag.
           IF AVAILABLE budget THEN payable-list.ytd-budget = payable-list.ytd-budget + budget.betrag.            
         END. 
         ELSE DO:
               IF AVAILABLE umsatz THEN 
               DO: 
                 IF ytd-flag THEN payable-list.ytd = payable-list.ytd + n-betrag. 
                 IF MONTH(curr-date) = MONTH(to-date) THEN ASSIGN payable-list.mtd = payable-list.mtd + mon-saldo[DAY(umsatz.datum)] + n-betrag .
               END. 

               IF AVAILABLE budget THEN 
               DO: 
                 payable-list.mtd-budget = payable-list.mtd-budget + budget.betrag. 
               END. 
         END.
         ASSIGN payable-list.variance = payable-list.mtd - payable-list.mtd-budget.
     END.    
END.

PROCEDURE create-payment-list:
    CREATE payment-list.
    ASSIGN payment-list.ct           = ct2
           payment-list.descr        = artikel.bezeich
           payment-list.departement  = setup-payment.departement.

    IF artikel.artart EQ 6 AND artikel.umsatzart EQ 0 THEN ASSIGN payment-list.flag = "1Cash".
    ELSE IF artikel.artart EQ 7 AND artikel.umsatzart EQ 0 THEN ASSIGN payment-list.flag = "2Payment".
    ELSE IF artikel.artart EQ 2 AND artikel.umsatzart EQ 0 THEN ASSIGN payment-list.flag = "3Ledger".
    ELSE IF artikel.artart EQ 6 AND artikel.umsatzart EQ 4 THEN ASSIGN payment-list.flag = "4Foreign".
    ELSE IF artikel.artart EQ 5 AND artikel.umsatzart EQ 0 THEN ASSIGN payment-list.flag = "5Deposit".      

     DO curr-date = datum1 TO to-date: 
     ASSIGN
         serv = 0
         vat  = 0.

         FIND FIRST umsatz WHERE umsatz.datum = curr-date 
           AND umsatz.artnr = artikel.artnr AND umsatz.departement = artikel.departement NO-LOCK NO-ERROR. 
         IF AVAILABLE umsatz THEN 

           RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                                  umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

         fact = 1.00 + serv + vat + vat2.

         d-flag = AVAILABLE umsatz AND (MONTH(umsatz.datum) = MONTH(to-date))
           AND (YEAR(umsatz.datum) = YEAR(to-date)).

         n-betrag = 0. 
         IF AVAILABLE umsatz THEN 
         DO: 
           IF foreign-flag THEN 
           DO:  
             RUN find-exrate(curr-date). 
             IF AVAILABLE exrate THEN frate = exrate.betrag. 
           END. 
           ASSIGN
             n-betrag = umsatz.betrag / (fact * frate) 
             n-serv   = n-betrag * serv
             n-tax    = n-betrag * vat.
            
           IF umsat.datum = to-date THEN
           ASSIGN payment-list.t-day = payment-list.t-day + n-betrag.

           IF price-decimal = 0 THEN 
           DO:
             ASSIGN 
               n-betrag = ROUND(n-betrag, 0)
               n-serv = ROUND(n-serv, 0)
               n-tax = ROUND(n-tax, 0).
           END.
         END. 

         FIND FIRST budget WHERE budget.artnr = artikel.artnr 
         AND budget.departement = artikel.departement 
         AND budget.datum = curr-date NO-LOCK NO-ERROR.

         IF curr-date LT from-date THEN 
         DO: 
           IF AVAILABLE umsatz THEN payment-list.ytd = payment-list.ytd + n-betrag .
           IF AVAILABLE budget THEN payment-list.ytd-budget = payment-list.ytd-budget + budget.betrag.            
         END. 
         ELSE DO:
               IF AVAILABLE umsatz THEN 
               DO: 
                 IF ytd-flag THEN payment-list.ytd = payment-list.ytd + n-betrag. 
                 IF MONTH(curr-date) = MONTH(to-date) THEN ASSIGN payment-list.mtd = payment-list.mtd + mon-saldo[DAY(umsatz.datum)] + n-betrag .
               END. 

               IF AVAILABLE budget THEN 
               DO: 
                 payment-list.mtd-budget = payment-list.mtd-budget + budget.betrag. 
               END. 
         END.
         ASSIGN payment-list.variance = payment-list.mtd - payment-list.mtd-budget.
     END.      
END.

PROCEDURE fill-tot-room:

DEFINE VARIABLE datum          AS DATE.
DEFINE VARIABLE anz             AS INTEGER. 
DEFINE VARIABLE anz0            AS INTEGER.
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
  ct1 = ct1 + 1.   
  FIND FIRST stat-list WHERE stat-list.flag EQ "tot-rm" NO-LOCK NO-ERROR.
  IF NOT AVAILABLE stat-list THEN DO:
          CREATE stat-list.
          ASSIGN stat-list.ct       = ct1
                 stat-list.descr    = "Total Room"
                 stat-list.flag     = "tot-rm".
          DO datum = datum1 TO to-date: 
              FIND FIRST zinrstat WHERE zinrstat.datum = datum
                AND zinrstat.zinr = "tot-rm" NO-LOCK NO-ERROR.
              IF AVAILABLE zinrstat THEN anz = zinrstat.zimmeranz.
              ELSE anz = anz0.
            
              d-flag = AVAILABLE zinrstat AND (MONTH(zinrstat.datum) = MONTH(to-date))
                AND (YEAR(zinrstat.datum) = YEAR(to-date)).
              IF AVAILABLE zinrstat  THEN
              IF d-flag THEN stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zinrstat.datum)] + anz.
              
              IF datum = to-date THEN stat-list.t-day = stat-list.t-day + anz. 
              IF start-date NE ? THEN
              DO:
                IF (datum LT from-date) AND (datum GE start-date) 
                  THEN stat-list.ytd = stat-list.ytd + anz. 
                ELSE 
                DO: 
                  IF ytd-flag AND (datum GE start-date) THEN 
                    stat-list.ytd = stat-list.ytd + anz. 
                END.
              END.
              ELSE
              DO:
                IF (datum LT from-date) THEN stat-list.ytd = stat-list.ytd + anz. 
                ELSE 
                DO: 
                  IF ytd-flag THEN stat-list.ytd = stat-list.ytd + anz. 
                END.
              END.
                
              IF MONTH(datum) = MONTH(to-date) THEN DO:
                  FIND FIRST setup-stat WHERE setup-stat.descr EQ "Total Room" NO-LOCK NO-ERROR.
                  IF AVAILABLE setup-stat THEN DO:
                     FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
                        AND budget.departement = 0 AND budget.datum = datum NO-LOCK NO-ERROR.
                     IF AVAILABLE budget THEN DO:                     
                         stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
                     END.                         
                  END.
              END.
          END.
      END.
END.

PROCEDURE fill-tot-avail:
    ct1 = ct1 + 1.   
    FIND FIRST stat-list WHERE stat-list.flag EQ "tot-rmavail" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE stat-list THEN DO:
    CREATE stat-list.
    ASSIGN stat-list.ct       = ct1  
           stat-list.descr    = "Room Available"
           stat-list.flag     = "tot-rmavail".

        FOR EACH zkstat WHERE zkstat.datum GE datum1 AND zkstat.datum LE to-date NO-LOCK: 
          IF zkstat.datum = to-date THEN stat-list.t-day = stat-list.t-day + zkstat.anz100. 
          IF zkstat.datum LT from-date THEN 
            stat-list.ytd = stat-list.ytd + zkstat.anz100. 
          ELSE 
          DO: 
            IF ytd-flag THEN stat-list.ytd = stat-list.ytd + zkstat.anz100. 
          END. 
          IF MONTH(zkstat.datum) = MONTH(to-date) AND YEAR(zkstat.datum) = YEAR(to-date) THEN
            stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zkstat.datum)] + zkstat.anz100.
        END.

        FIND FIRST setup-stat WHERE setup-stat.descr EQ "Rooms Available" NO-LOCK NO-ERROR.
        IF AVAILABLE setup-stat THEN DO:
            FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
            AND budget.departement = 0
            AND budget.datum = datum1 NO-LOCK NO-ERROR.
            IF datum1 LT from-date THEN .
            ELSE DO:
            IF AVAILABLE budget THEN 
                 DO: 
                   stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag. 
                 END.
            END.
        END.
    END.  
END.

PROCEDURE fill-inactive:
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
    ct1 = ct1 + 1.   
    FIND FIRST stat-list WHERE stat-list.flag EQ "tot-inactive" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE stat-list THEN DO:
        CREATE stat-list.
        ASSIGN stat-list.ct       = ct1  
               stat-list.descr    = "InactiveRoom"
               stat-list.flag     = "tot-inactive".  
        
        FOR EACH b-stat-list NO-LOCK:
            IF b-stat-list.flag EQ "tot-rm"  THEN 
                ASSIGN tday1 = b-stat-list.t-day 
                       mtd1  = b-stat-list.mtd
                       ytd1  = b-stat-list.ytd.
            
            IF b-stat-list.flag EQ "tot-rmavail"  THEN 
                ASSIGN tday2 = b-stat-list.t-day
                       mtd2  = b-stat-list.mtd
                       ytd2  = b-stat-list.ytd.
        

       END.
       ASSIGN stat-list.t-day =  tday1 - tday2
              stat-list.mtd   =  mtd1 - mtd2 
              stat-list.ytd   =  ytd1 - ytd2.
    END.
END.

PROCEDURE fill-rmstat:
DEFINE INPUT PARAMETER key-word AS CHAR.
DEFINE VARIABLE datum         AS DATE.
DEFINE VARIABLE anz             AS INTEGER. 
DEFINE VARIABLE anz0            AS INTEGER.
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE cur-key         AS CHAR.
/* DEFINE VARIABLE cur-key1        AS CHAR.  */
  ct1 = ct1 + 1.
  FIND FIRST stat-list WHERE stat-list.flag EQ key-word NO-LOCK NO-ERROR.
  IF NOT AVAILABLE stat-list THEN DO:
  CREATE stat-list.
  ASSIGN stat-list.ct       = ct1
         stat-list.flag     = key-word.

  IF key-word = "ooo" THEN ASSIGN stat-list.descr = "Out of Order Rooms".
  ELSE IF key-word = "oos" THEN ASSIGN stat-list.descr = "Rooms Occupied".
  ELSE IF key-word = "dayuse" THEN ASSIGN stat-list.descr = "Day Use".
  ELSE IF key-word = "No-Show" THEN ASSIGN stat-list.descr = "No Show".
  ELSE IF key-word = "arrival-WIG" THEN ASSIGN stat-list.descr = "Walk in Guest".
  ELSE IF key-word = "NewRes" THEN ASSIGN stat-list.descr = "Reservation Made Today".
  ELSE IF key-word = "CancRes" THEN ASSIGN stat-list.descr = "Cancellation For Today".
  ELSE IF key-word = "Early-CO" THEN ASSIGN stat-list.descr = "Early Check Out".
  ELSE IF key-word = "arrival" THEN ASSIGN stat-list.descr = "Room Arrivals".
  ELSE IF key-word = "pers-arrival" THEN DO:
      ASSIGN cur-key         = "pers-arrival"
             key-word        = "arrival"
             stat-list.descr = "Person Arrivals".
  END.
  ELSE IF key-word = "departure" THEN ASSIGN stat-list.descr = "Room Departures".
  ELSE IF key-word = "pers-depature" THEN DO:
      ASSIGN cur-key         = "pers-depature"
             key-word        = "departure"
             stat-list.descr = "Person Depatures".
  END.  
  ELSE IF key-word = "ArrTmrw" THEN ASSIGN stat-list.descr = "Room Arrivals Tomorrow".
  ELSE IF key-word = "pers-ArrTmrw" THEN DO:
      ASSIGN cur-key         = "pers-ArrTmrw"
             key-word        = "ArrTmrw"
             stat-list.descr = "Person Arrivals Tomorrow".
  END. 
  ELSE IF key-word = "DepTmrw" THEN ASSIGN stat-list.descr = "Room Departures Tomorrow".
  ELSE IF key-word = "pers-DepTmrw" THEN DO:
      ASSIGN cur-key         = "pers-DepTmrw"
             key-word        = "DepTmrw"
             stat-list.descr = "Person Departures Tomorrow".
  END. 

      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      
      d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
               AND (YEAR(zinrstat.datum) = YEAR(to-date)).

      IF d-flag THEN DO: 
         IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zinrstat.datum)] + zinrstat.personen. 
         ELSE stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz.

      END.
      /*IF (MONTH(zinrstat.datum) = MONTH(to-date))
               AND (YEAR(zinrstat.datum) = YEAR(to-date)) THEN DO: 
          IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.mtd = stat-list.mtd + zinrstat.personen. 
          ELSE stat-list.mtd = stat-list.mtd  + zinrstat.zimmeranz.
      END.*/

      IF zinrstat.datum = to-date THEN DO: 
         IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.t-day = stat-list.t-day + zinrstat.personen.
         ELSE stat-list.t-day = stat-list.t-day + zinrstat.zimmeranz. 
      END.
      IF zinrstat.datum LT from-date THEN DO:
         IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.ytd = stat-list.ytd + zinrstat.personen.
         ELSE stat-list.ytd = stat-list.ytd + zinrstat.zimmeranz.    
      END.
      ELSE 
      DO: 
        IF ytd-flag THEN DO:
          IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.ytd = stat-list.ytd + zinrstat.personen.
          ELSE stat-list.ytd = stat-list.ytd + zinrstat.zimmeranz.  
        END.
      END. 
      END.

      FOR EACH setup-stat NO-LOCK:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.

        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               IF setup-stat.descr = "OOO Room" AND key-word = "ooo" THEN stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
               ELSE IF setup-stat.descr = "Rooms Occupied" AND key-word = "occ" THEN stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.
      END.
  END.    
END.

PROCEDURE fill-rmocc: 
    DEFINE VARIABLE curr-date       AS DATE. 
    DEFINE VARIABLE datum1          AS DATE. 
    DEFINE VARIABLE datum2          AS DATE. 
    DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
    DEFINE VARIABLE dbudget-flag    AS LOGICAL NO-UNDO.
    DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
    DEFINE VARIABLE frate1          AS DECIMAL NO-UNDO.

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    
    ct1 = ct1 + 1.
    CREATE stat-list.
    ASSIGN stat-list.ct    = ct1
           stat-list.descr = "Rooms Occupied"
           stat-list.flag  = "occ".

    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE to-date NO-LOCK,
        FIRST segment WHERE segment.segmentcode = segmentstat.segmentcode NO-LOCK:

        frate = 1.
          IF foreign-flag THEN 
          DO: 
            RUN find-exrate(segmentstat.datum). 
            IF AVAILABLE exrate THEN frate = exrate.betrag. 
          END.
          
          IF segmentstat.datum = to-date THEN 
          DO:
            stat-list.t-day = stat-list.t-day + segmentstat.zimmeranz.   
          END.
          
          IF MONTH(segmentstat.datum) = MONTH(to-date) THEN
          DO:
            stat-list.mtd = stat-list.mtd + segmentstat.zimmeranz.
          END.
          stat-list.ytd = stat-list.ytd + segmentstat.zimmeranz.   
    END.  

     FIND FIRST setup-stat WHERE setup-stat.descr EQ "Rooms Occupied" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
         FOR EACH budget WHERE budget.artnr = setup-stat.artnr
         AND budget.departement = 0 
         AND budget.datum GE from-date
         AND budget.datum LE to-date NO-LOCK:
             stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
         END.
     END.
END.

PROCEDURE fill-stat:
DEFINE INPUT PARAMETER key-word AS CHAR.
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
 ct1 = ct1 + 1.
 FIND FIRST stat-list WHERE stat-list.flag EQ key-word NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = key-word.

     IF key-word = "vacant" THEN ASSIGN stat-list.descr = "Vacant Rooms".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "tot-rmavail"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "ooo"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.

        IF b-stat-list.flag EQ "occ"  THEN 
            ASSIGN tday3 = b-stat-list.t-day
                   mtd3  = b-stat-list.mtd
                   ytd3  = b-stat-list.ytd.


     END.

     ASSIGN stat-list.t-day =  tday1 - tday2 - tday3
            stat-list.mtd   =  mtd1 - mtd2 - mtd3
            stat-list.ytd   =  ytd1 - ytd2 - ytd3.

     FIND FIRST setup-stat WHERE setup-stat.descr = "Vacant Rooms" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FOR EACH budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum GE from-date
        AND budget.datum GE to-date NO-LOCK:
            stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
        END.   
     END.
 END.
END.

PROCEDURE fill-segm :
DEFINE INPUT PARAMETER key-word AS CHAR.

DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE mm AS INTEGER.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

    mm = MONTH(to-date).
    /*saldo*/
    ct1 = ct1 + 1.

    IF key-word = "HSE" THEN
        FIND FIRST segment WHERE segment.betriebsnr = 2 NO-LOCK NO-ERROR.
    ELSE IF key-word = "COM" THEN
        FIND FIRST segment WHERE segment.betriebsnr = 1 NO-LOCK NO-ERROR.

    IF AVAILABLE segment THEN DO:
        CREATE stat-list.
        ASSIGN stat-list.ct      = ct1
               stat-list.flag    = key-word .

        IF key-word EQ "HSE" THEN  stat-list.descr   = "House Uses".
        ELSE IF key-word EQ "COM" THEN  stat-list.descr   = "Complimentary".

        FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode
          AND genstat.datum GE datum1 
          AND genstat.datum LE to-date 
          AND genstat.resstatus NE 13 
          /*AND genstat.gratis EQ 0 */
          AND genstat.segmentcode NE 0 
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] NO-LOCK:

            IF foreign-flag THEN 
            DO: 
              RUN find-exrate(genstat.datum). 
              IF AVAILABLE exrate THEN frate = exrate.betrag. 
            END. 

            d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                 AND (YEAR(genstat.datum) = YEAR(to-date)).
                
            IF genstat.datum = to-date THEN DO:
                stat-list.t-day = stat-list.t-day + 1.   
            END.
            
            IF MONTH(genstat.datum) = mm THEN DO:
                stat-list.mtd = stat-list.mtd + mon-saldo[DAY(genstat.datum)] + 1.    
            END.

            stat-list.ytd = stat-list.ytd + 1.
        END.

        FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE to-date 
        AND segmentstat.segmentcode = segment-list.segmentcode NO-LOCK:
        
            IF MONTH(segmentstat.datum) = mm THEN DO:
                stat-list.mtd-budget = stat-list.mtd-budget + mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.
            END.
            
            stat-list.ytd-budget = stat-list.ytd-budget + segmentstat.budzimmeranz.

        END.

    END.
END.

PROCEDURE create-fbcover: 
DEFINE VARIABLE datum1         AS DATE. 
DEFINE VARIABLE datum2         AS DATE. 
DEFINE VARIABLE curr-date      AS DATE. 
DEFINE VARIABLE t-day          AS DECIMAL.
DEFINE VARIABLE mtd            AS DECIMAL.
DEFINE VARIABLE ytd            AS DECIMAL.
DEFINE VARIABLE t-day-rev      AS DECIMAL.
DEFINE VARIABLE mtd-rev        AS DECIMAL.
DEFINE VARIABLE ytd-rev        AS DECIMAL.
DEFINE VARIABLE t-day-avg   AS DECIMAL.
DEFINE VARIABLE mtd-avg     AS DECIMAL.
DEFINE VARIABLE ytd-avg     AS DECIMAL.


  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  /*  
  FOR EACH umsatz WHERE umsatz.datum GE datum1 AND umsatz.datum LE to-date 
    AND umsatz.artnr = setup-fbcover.artnr AND umsatz.departement = setup-fbcover.departement NO-LOCK: 
    
    IF umsatz.datum = to-date THEN 
      t-day = t-day + umsatz.anzahl. 
    
    IF umsatz.datum LT from-date THEN 
      ytd = ytd + umsatz.anzahl. 
    ELSE 
    DO: 
      IF ytd-flag THEN ytd = ytd + umsatz.anzahl.
      IF MONTH(curr-date) = MONTH(to-date) THEN ASSIGN mtd = mtd + mon-saldo[DAY(umsatz.datum)] + umsatz.anzahl.
    END. 
  END.*/ 

  DO curr-date = datum1 TO to-date: 
     ASSIGN
         serv = 0
         vat  = 0.

         FIND FIRST umsatz WHERE umsatz.datum = curr-date 
           AND umsatz.artnr = artikel.artnr AND umsatz.departement = setup-fbcover.departement NO-LOCK NO-ERROR. 
         IF AVAILABLE umsatz THEN 

           RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                                  umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

         fact = 1.00 + serv + vat + vat2.

         n-betrag = 0. 
         IF AVAILABLE umsatz THEN 
         DO: 
           IF foreign-flag THEN 
           DO:  
             RUN find-exrate(curr-date). 
             IF AVAILABLE exrate THEN frate = exrate.betrag. 
           END. 
           ASSIGN
             n-betrag = umsatz.betrag / (fact * frate) 
             n-serv   = n-betrag * serv
             n-tax    = n-betrag * vat.

           ASSIGN t-day     = t-day + umsatz.anzahl
                  t-day-rev = t-day-rev + n-betrag.
           
           IF price-decimal = 0 THEN 
           DO:
             ASSIGN 
               n-betrag = ROUND(n-betrag, 0)
               n-serv = ROUND(n-serv, 0)
               n-tax = ROUND(n-tax, 0).
           END.
         END. 

         IF curr-date LT from-date THEN 
         DO: 
           IF AVAILABLE umsatz THEN 
               ASSIGN ytd-rev = ytd-rev + n-betrag 
                      ytd     = ytd + umsatz.anzahl.
         END. 
         ELSE DO:
               IF AVAILABLE umsatz THEN 
               DO: 
                 IF ytd-flag THEN
                     ASSIGN ytd-rev = ytd-rev + n-betrag
                            ytd     = ytd + umsatz.anzahl. 
                 IF MONTH(curr-date) = MONTH(to-date) THEN 
                     ASSIGN mtd-rev = mtd-rev + mon-saldo[DAY(umsatz.datum)] + n-betrag 
                            mtd     = mtd + mon-saldo[DAY(umsatz.datum)] + umsatz.anzahl.
               END.  
         END.
         IF t-day NE 0 THEN
         ASSIGN t-day-avg = t-day-rev / t-day
                mtd-avg   = mtd-rev   / mtd
                ytd-avg   = ytd-rev   / ytd.
     END.
     
     IF setup-fbcover.flag = "1Food"  THEN DO:
         FIND FIRST fb-sales-food WHERE fb-sales-food.departement EQ setup-fbcover.departement AND fb-sales-food.flag = "1Food" NO-LOCK NO-ERROR.
         IF NOT AVAILABLE fb-sales-food THEN DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num EQ setup-fbcover.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN DO:
             ct = ct + 1.
             CREATE fb-sales-food.
             ASSIGN 
             fb-sales-food.ct          = ct
             fb-sales-food.departement = setup-fbcover.departement
             fb-sales-food.descr       = hoteldpt.depart
             fb-sales-food.flag        = "1Food".
            END.
         END.
     END.
     ELSE IF setup-fbcover.flag = "2Beverage"  THEN DO:
         FIND FIRST fb-sales-beverage WHERE fb-sales-beverage.departement EQ setup-fbcover.departement AND fb-sales-beverage.flag = "2Beverage" NO-LOCK NO-ERROR.
         IF NOT AVAILABLE fb-sales-beverage THEN DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num EQ setup-fbcover.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN DO:
             ct = ct + 1.
             CREATE fb-sales-beverage.
             ASSIGN 
             fb-sales-beverage.ct          = ct
             fb-sales-beverage.departement = setup-fbcover.departement
             fb-sales-beverage.descr       = hoteldpt.depart
             fb-sales-beverage.flag        = "2Beverage".
            END.
         END.
     END.
     ELSE IF setup-fbcover.flag = "3Banquet"  THEN DO:
         FIND FIRST fb-sales-other WHERE fb-sales-other.departement EQ setup-fbcover.departement AND fb-sales-other.flag = "3Banquet" NO-LOCK NO-ERROR.
         IF NOT AVAILABLE fb-sales-other THEN DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num EQ setup-fbcover.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN DO:
             ct = ct + 1.
             CREATE fb-sales-other.
             ASSIGN 
             fb-sales-other.ct          = ct
             fb-sales-other.departement = setup-fbcover.departement
             fb-sales-other.descr       = hoteldpt.depart
             fb-sales-other.flag        = "3Banquet".
            END.
         END.
     END.
     ELSE IF setup-fbcover.flag = "4Material"  THEN DO:
         FIND FIRST fb-sales-material WHERE fb-sales-material.departement EQ setup-fbcover.departement AND fb-sales-material.flag = "4Material" NO-LOCK NO-ERROR.
         IF NOT AVAILABLE fb-sales-material THEN DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num EQ setup-fbcover.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN DO:
             ct = ct + 1.
             CREATE fb-sales-material.
             ASSIGN 
             fb-sales-material.ct          = ct
             fb-sales-material.departement = setup-fbcover.departement
             fb-sales-material.descr       = hoteldpt.depart
             fb-sales-material.flag        = "4Material".
            END.
         END.
     END.

     ct = ct + 1.
     IF setup-fbcover.flag = "1Food"  THEN DO:
         CREATE fb-sales-food.
         IF mtd-avg = ? THEN mtd-avg = 0.
         ASSIGN 
         fb-sales-food.ct        = ct
         fb-sales-food.departement = setup-fbcover.departement
         fb-sales-food.artnr     = setup-fbcover.artnr
         fb-sales-food.descr     = artikel.bezeich
         fb-sales-food.tday-cov  = t-day
         fb-sales-food.tday-avg  = t-day-avg
         fb-sales-food.tday-rev  = t-day-rev
         fb-sales-food.mtd-cov   = mtd    
         fb-sales-food.mtd-avg   = mtd-avg
         fb-sales-food.mtd-rev   = mtd-rev
         fb-sales-food.ytd-cov   = ytd    
         fb-sales-food.ytd-avg   = ytd-avg
         fb-sales-food.ytd-rev   = ytd-rev
         fb-sales-food.flag      = "1Food"
         t-day                   = 0
         mtd                     = 0
         ytd                     = 0
         t-day-rev               = 0
         mtd-rev                 = 0
         ytd-rev                 = 0
         t-day-avg               = 0
         mtd-avg                 = 0
         ytd-avg                 = 0
         .
     END.
     ELSE IF setup-fbcover.flag = "2Beverage" THEN DO: 
         CREATE fb-sales-beverage.
         IF mtd-avg = ? THEN mtd-avg = 0.
         ASSIGN 
         fb-sales-beverage.ct        = ct
         fb-sales-beverage.departement = setup-fbcover.departement
         fb-sales-beverage.artnr     = setup-fbcover.artnr
         fb-sales-beverage.descr     = artikel.bezeich
         fb-sales-beverage.tday-cov  = t-day
         fb-sales-beverage.tday-avg  = t-day-avg
         fb-sales-beverage.tday-rev  = t-day-rev
         fb-sales-beverage.mtd-cov   = mtd    
         fb-sales-beverage.mtd-avg   = mtd-avg
         fb-sales-beverage.mtd-rev   = mtd-rev
         fb-sales-beverage.ytd-cov   = ytd    
         fb-sales-beverage.ytd-avg   = ytd-avg
         fb-sales-beverage.ytd-rev   = ytd-rev
         fb-sales-beverage.flag      = "2Beverage"
         t-day                   = 0
         mtd                     = 0
         ytd                     = 0
         t-day-rev               = 0
         mtd-rev                 = 0
         ytd-rev                 = 0
         t-day-avg               = 0
         mtd-avg                 = 0
         ytd-avg                 = 0
         .
     END.
     ELSE IF setup-fbcover.flag = "3Banquet" THEN DO:
         CREATE fb-sales-other.
         IF mtd-avg = ? THEN mtd-avg = 0.
         ASSIGN 
         fb-sales-other.ct        = ct
         fb-sales-other.departement = setup-fbcover.departement
         fb-sales-other.artnr     = setup-fbcover.artnr
         fb-sales-other.descr     = artikel.bezeich
         fb-sales-other.tday-cov  = t-day
         fb-sales-other.tday-avg  = t-day-avg
         fb-sales-other.tday-rev  = t-day-rev
         fb-sales-other.mtd-cov   = mtd    
         fb-sales-other.mtd-avg   = mtd-avg
         fb-sales-other.mtd-rev   = mtd-rev
         fb-sales-other.ytd-cov   = ytd    
         fb-sales-other.ytd-avg   = ytd-avg
         fb-sales-other.ytd-rev   = ytd-rev
         fb-sales-other.flag      = "3Banquet"
         t-day                   = 0
         mtd                     = 0
         ytd                     = 0
         t-day-rev               = 0
         mtd-rev                 = 0
         ytd-rev                 = 0
         t-day-avg               = 0
         mtd-avg                 = 0
         ytd-avg                 = 0
     .
     END.
     ELSE IF setup-fbcover.flag = "4Material" THEN DO:
         CREATE fb-sales-material.
         IF mtd-avg = ? THEN mtd-avg = 0.
         ASSIGN 
         fb-sales-material.ct        = ct
         fb-sales-material.departement = setup-fbcover.departement
         fb-sales-material.artnr     = setup-fbcover.artnr
         fb-sales-material.descr     = artikel.bezeich
         fb-sales-material.tday-cov  = t-day
         fb-sales-material.tday-avg  = t-day-avg
         fb-sales-material.tday-rev  = t-day-rev
         fb-sales-material.mtd-cov   = mtd    
         fb-sales-material.mtd-avg   = mtd-avg
         fb-sales-material.mtd-rev   = mtd-rev
         fb-sales-material.ytd-cov   = ytd    
         fb-sales-material.ytd-avg   = ytd-avg
         fb-sales-material.ytd-rev   = ytd-rev
         fb-sales-material.flag      = "4Material"
         t-day                   = 0
         mtd                     = 0
         ytd                     = 0
         t-day-rev               = 0
         mtd-rev                 = 0
         ytd-rev                 = 0
         t-day-avg               = 0
         mtd-avg                 = 0
         ytd-avg                 = 0
     .
     END.

END.

PROCEDURE fill-comproomnew :

DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE mm AS INTEGER.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

    mm = MONTH(to-date).
    /*saldo*/
    ct1 = ct1 + 1.

        CREATE stat-list.
        ASSIGN stat-list.ct      = ct1
               stat-list.flag    = "Compl" 
               stat-list.descr   = "Complimentary Paying Guest".

        FOR EACH genstat WHERE genstat.datum GE datum1
            AND genstat.datum LE to-date
            AND genstat.zipreis = 0
            AND genstat.gratis = 0
            AND genstat.resstatus = 6 
            AND genstat.res-logic[3] NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK:
                
            IF segment.betriebsnr = 0 THEN
            DO:
                IF foreign-flag THEN 
                DO: 
                  RUN find-exrate(genstat.datum). 
                  IF AVAILABLE exrate THEN frate = exrate.betrag. 
                END. 
    
                d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                     AND (YEAR(genstat.datum) = YEAR(to-date)).
                    
                IF genstat.datum = to-date THEN DO:
                    stat-list.t-day = stat-list.t-day + 1.   
                END.
                
                IF MONTH(genstat.datum) = mm THEN DO:
                    stat-list.mtd = stat-list.mtd + mon-saldo[DAY(genstat.datum)] + 1.    
            END.

            stat-list.ytd = stat-list.ytd + 1.
            END.
        END.
END.

PROCEDURE fill-roomsold :
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "rmsold" NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "rmsold"
            stat-list.descr    = "Rooms Sold".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "houseuse"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "comp"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.

        IF b-stat-list.flag EQ "occ"  THEN 
            ASSIGN tday3 = b-stat-list.t-day
                   mtd3  = b-stat-list.mtd
                   ytd3  = b-stat-list.ytd.


     END.
    
        
     ASSIGN stat-list.t-day =  tday1 + tday2 + tday3
            stat-list.mtd   =  mtd1 + mtd2 + mtd3
            stat-list.ytd   =  ytd1 + ytd2 + ytd3.
    
     FIND FIRST setup-stat WHERE setup-stat.descr = "Room Sold" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.
 END.
END.

PROCEDURE fill-occ-pay :
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "occpay" NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "occ-pay"
            stat-list.descr    = "% Occupancy (Paying)".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "tot-rm"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "rmsold"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday2 / tday1) * 100
            stat-list.mtd   =  (mtd2 / mtd1) * 100 
            stat-list.ytd   =  (ytd2 / ytd1) * 100.
    
     FIND FIRST setup-stat WHERE setup-stat.descr = "% Occupancy" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.
 END.
END.

PROCEDURE fill-occ-comp-hu :
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "occ-comp-hu" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "occ-comp-hu"
            stat-list.descr    = "% Occupancy (Comp + HU)".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "occ"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "tot-rm"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday1 / tday2) * 100
            stat-list.mtd   =  (mtd1 / mtd2) * 100 
            stat-list.ytd   =  (ytd1 / ytd2) * 100.

     FIND FIRST setup-stat WHERE setup-stat.descr = "% Occupancy with Comp and HU" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.
 END.
END.

PROCEDURE fill-tot-rev:
DEFINE VARIABLE tday1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday3 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.
    FIND FIRST stat-list WHERE stat-list.flag EQ "tot-rev" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE stat-list THEN DO:
         CREATE stat-list.
         ASSIGN stat-list.ct       = ct1
                stat-list.flag     = "tot-rev"
                stat-list.descr    = "Total Room Revenue".

         FIND FIRST rev-list WHERE rev-list.flag = "Room" AND rev-list.descr MATCHES "*Total Room Revenue*" NO-LOCK NO-ERROR. /*total*/
         IF AVAILABLE rev-list THEN DO:

            ASSIGN
                stat-list.t-day        = rev-list.t-day            
                stat-list.mtd          = rev-list.mtd        
                stat-list.ytd          = rev-list.ytd        
                stat-list.mtd-budget   = rev-list.mtd-budget.    
         END.
    END.
END.



PROCEDURE fill-avg-rmrate-rp :
DEFINE VARIABLE tday1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday3 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "avg-rmrate-rp" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "avg-rmrate-rp"
            stat-list.descr    = "Average Room Rate Rp.".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "rmsold"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     FIND FIRST rev-list WHERE rev-list.descr EQ "TOTAL ROOM REVENUE" NO-LOCK NO-ERROR.
     IF AVAILABLE rev-list THEN DO:
         ASSIGN tday1 = rev-list.t-day
                mtd1  = rev-list.mtd
                ytd1  = rev-list.ytd.
     END.

     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday1 / tday2)
            stat-list.mtd   =  (mtd1 / mtd2) 
            stat-list.ytd   =  (ytd1 / ytd2).
    
     FIND FIRST setup-stat WHERE setup-stat.descr = "Average Room Rate Rp" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.
 END.
END.


PROCEDURE fill-avg-rmrate-frg :
DEFINE VARIABLE tday1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday3 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "avg-rmrate-frg" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "avg-rmrate-frg" 
            stat-list.descr    = "Average Room Rate US$".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "rmsold"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     FIND FIRST rev-list NO-LOCK NO-ERROR.
     IF AVAILABLE rev-list THEN DO:

         RUN find-exrate(to-date). 
         IF AVAILABLE exrate THEN frate = exrate.betrag. 
        
        
         ASSIGN tday1 = rev-list.t-day / (fact * frate)
                mtd1  = rev-list.mtd / (fact * frate)
                ytd1  = rev-list.ytd / (fact * frate).
     END.
    
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday1 / tday2) / foreign-curr
            stat-list.mtd   =  (mtd1 / mtd2) / foreign-curr
            stat-list.ytd   =  (ytd1 / ytd2) / foreign-curr.

     FIND FIRST setup-stat WHERE setup-stat.descr = "Average Room Rate Rp" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.
 END.
END.

PROCEDURE fill-revpar:
DEFINE VARIABLE tday1       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd-budget1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd-budget2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.           
FIND FIRST stat-list WHERE stat-list.flag EQ "revpar" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "revpar" 
            stat-list.descr    = "Revenue Per Available Room / Revpar".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "tot-rmav"  THEN 
            ASSIGN tday2       = b-stat-list.t-day
                   mtd2        = b-stat-list.mtd
                   mtd-budget2 = b-stat-list.mtd-budget 
                   ytd2        = b-stat-list.ytd.
     END.
     
     FIND FIRST rev-list WHERE rev-list.descr EQ "TOTAL ROOM REVENUE" NO-LOCK NO-ERROR.
     IF AVAILABLE rev-list THEN DO:
         ASSIGN tday1       = rev-list.t-day
                mtd1        = rev-list.mtd
                mtd-budget1 = rev-list.mtd-budget
                ytd1        = rev-list.ytd.
     END.
        
     IF mtd-budget1 NE 0 AND mtd-budget2 NE 0 THEN
     stat-list.mtd-budget    =  (mtd-budget1 / mtd-budget2).
        
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day         =  (tday1 / tday2)
            stat-list.mtd           =  (mtd1 / mtd2) 
            stat-list.ytd           =  (ytd1 / ytd2).
 END.
END.
