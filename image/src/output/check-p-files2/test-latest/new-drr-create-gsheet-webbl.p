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

DEFINE TEMP-TABLE payable-list
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

DEFINE TEMP-TABLE tot-list 
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

DEFINE TEMP-TABLE stat-list
    FIELD ct            AS INTEGER
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD flag          AS CHAR.

DEFINE TEMP-TABLE payment-list  
    FIELD ct            AS INTEGER
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD flag          AS CHAR.


DEFINE TEMP-TABLE gl-list
    FIELD descr       AS CHAR FORMAT "x(45)"
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

DEFINE TEMP-TABLE fb-sales-beverage 
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

DEFINE TEMP-TABLE fb-sales-other  
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

DEFINE TEMP-TABLE fb-sales-tot  
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

DEFINE TEMP-TABLE fb-sales-material  
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

DEFINE NEW SHARED VARIABLE hServer      AS HANDLE       NO-UNDO. 
CREATE SERVER hServer.
hServer = SESSION:HANDLE.

DEFINE INPUT PARAMETER from-date     AS DATE.
DEFINE INPUT PARAMETER to-date       AS DATE.
DEFINE INPUT PARAMETER gsheet-link   AS CHAR.
DEFINE INPUT PARAMETER TABLE FOR rev-seg-list.
DEFINE INPUT PARAMETER TABLE FOR rev-list.
DEFINE INPUT PARAMETER TABLE FOR payable-list.
DEFINE INPUT PARAMETER TABLE FOR stat-list.
DEFINE INPUT PARAMETER TABLE FOR payment-list.
DEFINE INPUT PARAMETER TABLE FOR gl-list.
DEFINE INPUT PARAMETER TABLE FOR fb-sales-food.
DEFINE INPUT PARAMETER TABLE FOR fb-sales-beverage.
DEFINE INPUT PARAMETER TABLE FOR fb-sales-other.
DEFINE INPUT PARAMETER TABLE FOR fb-sales-tot.
DEFINE INPUT PARAMETER TABLE FOR rev-seg-list1.
DEFINE INPUT PARAMETER TABLE FOR fb-sales-material.

RUN new-drr-del-gs-cldbl.p ON hServer(gsheet-link).
RUN new-drr-gs-cldbl.p 
       ON hServer(from-date , to-date , gsheet-link, INPUT TABLE rev-seg-list,
                  INPUT TABLE rev-list, INPUT TABLE payable-list, INPUT TABLE stat-list,
                  INPUT TABLE payment-list, INPUT TABLE gl-list, INPUT TABLE fb-sales-food,
                  INPUT TABLE fb-sales-beverage, INPUT TABLE fb-sales-other, INPUT TABLE fb-sales-tot,
                  INPUT TABLE rev-seg-list1, INPUT TABLE fb-sales-material).

OS-COMMAND SILENT VALUE("start " + gsheet-link).
