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

DEFINE TEMP-TABLE payable-list LIKE rev-list. 
DEFINE TEMP-TABLE tot-list LIKE rev-list.

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

DEFINE TEMP-TABLE payment-list LIKE stat-list.


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

DEFINE TEMP-TABLE fb-sales-beverage LIKE fb-sales-food.
DEFINE TEMP-TABLE fb-sales-other LIKE fb-sales-food.
DEFINE TEMP-TABLE fb-sales-tot  LIKE fb-sales-food.
DEFINE TEMP-TABLE fb-sales-material LIKE fb-sales-food.

DEFINE TEMP-TABLE menu-drr
    FIELD nr    AS INT
    FIELD descr AS CHAR FORMAT "x(30)".

DEFINE TEMP-TABLE stream-list
    FIELD crow AS INTEGER
    FIELD ccol AS INTEGER
    FIELD cval AS CHARACTER
.


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


DEFINE VARIABLE tot-netpay-tdy        AS DECIMAL.
DEFINE VARIABLE tot-netpay-mtd        AS DECIMAL.
DEFINE VARIABLE tot-netpay-mtdbudget  AS DECIMAL.
DEFINE VARIABLE tot-netpay-ytd        AS DECIMAL.

DEFINE VARIABLE tot-grosspay-tdy        AS DECIMAL.
DEFINE VARIABLE tot-grosspay-mtd        AS DECIMAL.
DEFINE VARIABLE tot-grosspay-mtdbudget  AS DECIMAL.
DEFINE VARIABLE tot-grosspay-ytd        AS DECIMAL.

DEFINE VARIABLE prev-param AS CHAR.
DEFINE VARIABLE ct-row     AS INT.
DEFINE VARIABLE ct-row2    AS INT.
DEFINE VARIABLE j          AS INT.
DEFINE VARIABLE curr-row   AS INT.
DEFINE VARIABLE curr-col   AS CHAR.
DEFINE VARIABLE htl-no     AS CHAR.
DEFINE VARIABLE cell-value AS CHAR.

DEFINE STREAM s1.
DEFINE VARIABLE out-path    AS CHAR FORMAT "x(120)" LABEL "Path".

    FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
        RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 
    
    /*OS-DELETE VALUE ("C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt").
    OUTPUT STREAM s1 TO VALUE("C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt") APPEND UNBUFFERED.*/
    
    OS-DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt").
    OUTPUT STREAM s1 TO VALUE("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt") APPEND UNBUFFERED.

    ct-row = 8.
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 2
                  stream-list.ccol    = 9
                  stream-list.cval    = "DAILY REVENUE REPORT".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 5
                  stream-list.ccol    = 13
                  stream-list.cval    = "Report Date : " + STRING(from-date) + "-" + STRING(to-date).
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 6
                  stream-list.ccol    = 13
                  stream-list.cval    = "Printed : " + STRING(TODAY).
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 2
                  stream-list.cval    = "D E S C R I P T I O N".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 7
                  stream-list.ccol    = 6
                  stream-list.cval    = "O C C U P A N C Y  B Y  S E G M E N T".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 3
                  stream-list.cval    = "TODAY".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 4
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 5
                  stream-list.cval    = "MTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 6
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 7
                  stream-list.cval    = "MTD BUDGET".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 8
                  stream-list.cval    = "VARIANCE".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 9
                  stream-list.cval    = "YTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = 8
                  stream-list.ccol    = 10
                  stream-list.cval    = "%".
    
    FOR EACH rev-seg-list NO-LOCK BY rev-seg-list.flag:
        ct-row = ct-row + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 1
               stream-list.cval    = "".
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 2
               stream-list.cval    = rev-seg-list.descr. 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 3
               stream-list.cval    = STRING(rev-seg-list.t-day,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 4
               stream-list.cval    = STRING(rev-seg-list.dper,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 5
               stream-list.cval    = STRING(rev-seg-list.mtd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 6
               stream-list.cval    = STRING(rev-seg-list.mtd-per,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 7
               stream-list.cval    = STRING(rev-seg-list.mtd-budget,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 8
               stream-list.cval    = STRING(rev-seg-list.variance,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 9
               stream-list.cval    = STRING(rev-seg-list.ytd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 10
               stream-list.cval    = STRING(rev-seg-list.ytd-per,"->>9.99").
    END.
    
    ASSIGN ct-row = ct-row + 2.
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 2
                  stream-list.cval    = "D E S C R I P T I O N".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 6
                  stream-list.cval    = "L O A D G I N G  B Y  S E G M E N T".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 3
                  stream-list.cval    = "TODAY".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 4
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 5
                  stream-list.cval    = "MTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 6
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 7
                  stream-list.cval    = "MTD BUDGET".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 8
                  stream-list.cval    = "VARIANCE".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 9
                  stream-list.cval    = "YTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row
                  stream-list.ccol    = 10
                  stream-list.cval    = "%".
    
    FOR EACH rev-seg-list1 NO-LOCK BY rev-seg-list1.flag:
        ct-row = ct-row + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 1
               stream-list.cval    = "".
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 2
               stream-list.cval    = rev-seg-list1.descr. 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 3
               stream-list.cval    = STRING(rev-seg-list1.t-day,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 4
               stream-list.cval    = STRING(rev-seg-list1.dper,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 5
               stream-list.cval    = STRING(rev-seg-list1.mtd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 6
               stream-list.cval    = STRING(rev-seg-list1.mtd-per,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 7
               stream-list.cval    = STRING(rev-seg-list1.mtd-budget,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 8
               stream-list.cval    = STRING(rev-seg-list1.variance,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 9
               stream-list.cval    = STRING(rev-seg-list1.ytd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 10
               stream-list.cval    = STRING(rev-seg-list1.ytd-per,"->>9.99").
    END.

    ASSIGN ct-row = ct-row + 3.
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 6
                  stream-list.cval    = "R E V E N U E".
    
    ASSIGN ct-row = ct-row + 1.

    CREATE stream-list.
       ASSIGN stream-list.crow    = ct-row 
              stream-list.ccol    = 2
              stream-list.cval    = "D E S C R I P T I O N".

    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 3
                  stream-list.cval    = "TODAY".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 4
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 5
                  stream-list.cval    = "MTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 6
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 7
                  stream-list.cval    = "MTD BUDGET".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 8
                  stream-list.cval    = "VARIANCE".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 9
                  stream-list.cval    = "YTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 10
                  stream-list.cval    = "%".
    
    FOR EACH rev-list NO-LOCK  BY rev-list.flag DESC BY rev-list.departement BY rev-list.ct:
        ct-row = ct-row + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 1
               stream-list.cval    = "".
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 2
               stream-list.cval    = rev-list.descr. 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 3
               stream-list.cval    = STRING(rev-list.t-day,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 4
               stream-list.cval    = STRING(rev-list.dper,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 5
               stream-list.cval    = STRING(rev-list.mtd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 6
               stream-list.cval    = STRING(rev-list.mtd-per,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 7
               stream-list.cval    = STRING(rev-list.mtd-budget,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 8
               stream-list.cval    = STRING(rev-list.variance,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 9
               stream-list.cval    = STRING(rev-list.ytd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 10
               stream-list.cval    = STRING(rev-list.ytd-per,"->>9.99").
    END.

    ASSIGN ct-row = ct-row + 3.


    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 6
                  stream-list.cval    = "P A Y A B L E".
    


    ASSIGN ct-row = ct-row + 1.

    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 2
                  stream-list.cval    = "D E S C R I P T I O N".

    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 3
                  stream-list.cval    = "TODAY".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 4
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 5
                  stream-list.cval    = "MTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 6
                  stream-list.cval    = "%".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 7
                  stream-list.cval    = "MTD BUDGET".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 8
                  stream-list.cval    = "VARIANCE".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 9
                  stream-list.cval    = "YTD".
    
    CREATE stream-list.
           ASSIGN stream-list.crow    = ct-row 
                  stream-list.ccol    = 10
                  stream-list.cval    = "%".
    
    FOR EACH payable-list NO-LOCK  BY payable-list.flag:
        ct-row = ct-row + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 1
               stream-list.cval    = "".
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 2
               stream-list.cval    = payable-list.descr. 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 3
               stream-list.cval    = STRING(payable-list.t-day,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 4
               stream-list.cval    = STRING(payable-list.dper,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 5
               stream-list.cval    = STRING(payable-list.mtd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 6
               stream-list.cval    = STRING(payable-list.mtd-per,"->>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 7
               stream-list.cval    = STRING(payable-list.mtd-budget,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 8
               stream-list.cval    = STRING(payable-list.variance,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 9
               stream-list.cval    = STRING(payable-list.ytd,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row
               stream-list.ccol    = 10
               stream-list.cval    = STRING(payable-list.ytd-per,"->>9.99").
    END.

    FIND FIRST rev-list WHERE rev-list.descr EQ "TOTAL NETT REVENUE" NO-LOCK NO-ERROR.
    IF AVAILABLE rev-list THEN DO:
       ASSIGN
          tot-netpay-tdy        = rev-list.t-day
          tot-netpay-mtd        = rev-list.mtd
          tot-netpay-mtdbudget  = rev-list.mtd-budget
          tot-netpay-ytd        = rev-list.ytd.
    END.

    FIND FIRST rev-list WHERE rev-list.descr EQ "TOTAL GROSS REVENUE" NO-LOCK NO-ERROR.
    IF AVAILABLE rev-list THEN DO:
       ASSIGN
          tot-grosspay-tdy        = rev-list.t-day
          tot-grosspay-mtd        = rev-list.mtd
          tot-grosspay-mtdbudget  = rev-list.mtd-budget
          tot-grosspay-ytd        = rev-list.ytd.
    END.

    FIND FIRST payable-list WHERE payable-list.descr EQ "TOTAL PAYABLE" NO-LOCK NO-ERROR.
    IF AVAILABLE payable-list THEN DO:
        ASSIGN 
         tot-netpay-tdy          = tot-netpay-tdy         + payable-list.t-day     
         tot-netpay-mtd          = tot-netpay-mtd         + payable-list.mtd       
         tot-netpay-mtdbudget    = tot-netpay-mtdbudget   + payable-list.mtd-budget
         tot-netpay-ytd          = tot-netpay-ytd         + payable-list.ytd
         tot-grosspay-tdy        = tot-grosspay-tdy       + payable-list.t-day        
         tot-grosspay-mtd        = tot-grosspay-mtd       + payable-list.mtd          
         tot-grosspay-mtdbudget  = tot-grosspay-mtdbudget + payable-list.mtd-budget   
         tot-grosspay-ytd        = tot-grosspay-ytd       + payable-list.ytd.      
    END.

    ct-row = ct-row + 2.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 1
           stream-list.cval    = "".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 2
           stream-list.cval    = "NETT REVENUE + TOTAL PAYABLE". 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 3
           stream-list.cval    = STRING(tot-netpay-tdy,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 4
           stream-list.cval    = STRING(100,"->>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 5
           stream-list.cval    = STRING(tot-netpay-mtd,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 6
           stream-list.cval    = STRING(100,"->>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 7
           stream-list.cval    = STRING(tot-netpay-mtdbudget,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 8
           stream-list.cval    = STRING(100,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 9
           stream-list.cval    = STRING(tot-netpay-ytd,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 10
           stream-list.cval    = STRING(100,"->>9.99").

    ct-row = ct-row + 2.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 1
           stream-list.cval    = "".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 2
           stream-list.cval    = "TOTAL REVENUE + PAYABLE". 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 3
           stream-list.cval    = STRING(tot-grosspay-tdy,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 4
           stream-list.cval    = STRING(100,"->>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 5
           stream-list.cval    = STRING(tot-grosspay-mtd,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 6
           stream-list.cval    = STRING(100,"->>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 7
           stream-list.cval    = STRING(tot-grosspay-mtdbudget,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 8
           stream-list.cval    = STRING(100,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 9
           stream-list.cval    = STRING(tot-grosspay-ytd,"->>,>>>,>>>,>>9.99"). 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 10
           stream-list.cval    = STRING(100,"->>9.99").

    ct-row = ct-row + 3.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 2
           stream-list.cval    = "G U E S T  L E D G E R". 
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row
           stream-list.ccol    = 3
           stream-list.cval    = "". 

    FOR EACH gl-list NO-LOCK:
         ct-row = ct-row + 1.

         CREATE stream-list.
         ASSIGN stream-list.crow    = ct-row
                stream-list.ccol    = 1
                stream-list.cval    = "".
         CREATE stream-list.
         ASSIGN stream-list.crow    = ct-row
                stream-list.ccol    = 2
                stream-list.cval    = gl-list.descr. 
         CREATE stream-list.
         ASSIGN stream-list.crow    = ct-row
                stream-list.ccol    = 3
                stream-list.cval    = STRING(gl-list.tot-rev,"->>,>>>,>>>,>>9.99").
    END.
    
    /*Sayap kanan*/
    CREATE stream-list.
    ASSIGN stream-list.crow    = 7
           stream-list.ccol    = 15
           stream-list.cval    = "S T A T I S T I C".
    CREATE stream-list.
    ASSIGN stream-list.crow    = 8
           stream-list.ccol    = 12
           stream-list.cval    = "D E S C R I P T I O N".
    CREATE stream-list.
    ASSIGN stream-list.crow    = 8
           stream-list.ccol    = 13
           stream-list.cval    = "TODAY".
    CREATE stream-list.
    ASSIGN stream-list.crow    = 8
           stream-list.ccol    = 14
           stream-list.cval    = "MTD".
    CREATE stream-list.
    ASSIGN stream-list.crow    = 8
           stream-list.ccol    = 15
           stream-list.cval    = "MTD BUDGET".
    CREATE stream-list.
    ASSIGN stream-list.crow    = 8
           stream-list.ccol    = 16
           stream-list.cval    = "VARIANCE".
    CREATE stream-list.
    ASSIGN stream-list.crow    = 8
           stream-list.ccol    = 17
           stream-list.cval    = "YTD".
    
    ct-row2 = 8.

    FOR EACH stat-list NO-LOCK BY stat-list.flag:

        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 11
                      stream-list.cval    = "".
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 12
                      stream-list.cval    = stat-list.descr.
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 13
                      stream-list.cval    = STRING(stat-list.t-day,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 14
                      stream-list.cval    = STRING(stat-list.mtd,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 15
                      stream-list.cval    = STRING(stat-list.mtd-budget,"->>,>>>,>>>,>>9.99").  
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 16
                      stream-list.cval    = STRING(stat-list.variance,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 17
                      stream-list.cval    = STRING(stat-list.ytd,"->>,>>>,>>>,>>9.99").
    END.

    ct-row2 = ct-row2 + 3.


    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2 
           stream-list.ccol    = 15
           stream-list.cval    = "P A Y M E N T".
    
    ct-row2 = ct-row2 + 1.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2 
           stream-list.ccol    = 12
           stream-list.cval    = "D E S C R I P T I O N".

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 13
           stream-list.cval    = "TODAY".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "MTD".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 15
           stream-list.cval    = "MTD BUDGET".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "VARIANCE".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 17
           stream-list.cval    = "YTD".


    FOR EACH payment-list NO-LOCK BY payment-list.flag BY payment-list.ct:

        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 11
                      stream-list.cval    = "".
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 12
                      stream-list.cval    = payment-list.descr.
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 13
                      stream-list.cval    = STRING(payment-list.t-day,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 14
                      stream-list.cval    = STRING(payment-list.mtd,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 15
                      stream-list.cval    = STRING(payment-list.mtd-budget,"->>,>>>,>>>,>>9.99").  
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 16
                      stream-list.cval    = STRING(payment-list.variance,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
               ASSIGN stream-list.crow    = ct-row2
                      stream-list.ccol    = 17
                      stream-list.cval    = STRING(payment-list.ytd,"->>,>>>,>>>,>>9.99").
    END.
    
    ct-row2 = ct-row2 + 3.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2 
           stream-list.ccol    = 16
           stream-list.cval    = "F&B SALES BY SHIFT".
                 
    ct-row2 = ct-row2 + 1.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "FOOD REVENUE".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 13
           stream-list.cval    = "Today Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "Today Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 15
           stream-list.cval    = "Today Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "MTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 17
           stream-list.cval    = "MTD Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 18
           stream-list.cval    = "MTD Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 19
           stream-list.cval    = "YTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 20
           stream-list.cval    = "YTD Average".

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 21
           stream-list.cval    = "YTD Revenue".


    FOR EACH fb-sales-food NO-LOCK:
    
        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 12
               stream-list.cval    = STRING(fb-sales-food.descr).
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 13
               stream-list.cval    = STRING(fb-sales-food.tday-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 14
               stream-list.cval    = STRING(fb-sales-food.tday-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 15
               stream-list.cval    = STRING(fb-sales-food.tday-rev,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 16
               stream-list.cval    = STRING(fb-sales-food.mtd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 17
               stream-list.cval    = STRING(fb-sales-food.mtd-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 18
               stream-list.cval    = STRING(fb-sales-food.mtd-rev,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 19
               stream-list.cval    = STRING(fb-sales-food.ytd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 20
               stream-list.cval    = STRING(fb-sales-food.ytd-avg,"->>,>>>,>>>,>>9.99").
       
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 21
               stream-list.cval    = STRING(fb-sales-food.ytd-rev,"->>,>>>,>>>,>>9.99").
    END.

    ct-row2 = ct-row2 + 3.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "BEVERAGE REVENUE".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 13
           stream-list.cval    = "Today Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "Today Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 15
           stream-list.cval    = "Today Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "MTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 17
           stream-list.cval    = "MTD Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 18
           stream-list.cval    = "MTD Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 19
           stream-list.cval    = "YTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 20
           stream-list.cval    = "YTD Average".

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 21
           stream-list.cval    = "YTD Revenue".
    
   FOR EACH fb-sales-beverage NO-LOCK:
    
        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 12
               stream-list.cval    = STRING(fb-sales-beverage.descr).
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 13
               stream-list.cval    = STRING(fb-sales-beverage.tday-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 14
               stream-list.cval    = STRING(fb-sales-beverage.tday-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 15
               stream-list.cval    = STRING(fb-sales-beverage.tday-rev,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 16
               stream-list.cval    = STRING(fb-sales-beverage.mtd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 17
               stream-list.cval    = STRING(fb-sales-beverage.mtd-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 18
               stream-list.cval    = STRING(fb-sales-beverage.mtd-rev,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 19
               stream-list.cval    = STRING(fb-sales-beverage.ytd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 20
               stream-list.cval    = STRING(fb-sales-beverage.ytd-avg,"->>,>>>,>>>,>>9.99").
       
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 21
               stream-list.cval    = STRING(fb-sales-beverage.ytd-rev,"->>,>>>,>>>,>>9.99").
    END.

    ct-row2 = ct-row2 + 3.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "OTHER REVENUE".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 13
           stream-list.cval    = "Today Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "Today Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 15
           stream-list.cval    = "Today Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "MTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 17
           stream-list.cval    = "MTD Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 18
           stream-list.cval    = "MTD Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 19
           stream-list.cval    = "YTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 20
           stream-list.cval    = "YTD Average".

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 21
           stream-list.cval    = "YTD Revenue".
    
   FOR EACH fb-sales-material NO-LOCK:
    
        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 12
               stream-list.cval    = STRING(fb-sales-material.descr).
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 13
               stream-list.cval    = STRING(fb-sales-material.tday-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 14
               stream-list.cval    = STRING(fb-sales-material.tday-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 15
               stream-list.cval    = STRING(fb-sales-material.tday-rev,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 16
               stream-list.cval    = STRING(fb-sales-material.mtd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 17
               stream-list.cval    = STRING(fb-sales-material.mtd-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 18
               stream-list.cval    = STRING(fb-sales-material.mtd-rev,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 19
               stream-list.cval    = STRING(fb-sales-material.ytd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 20
               stream-list.cval    = STRING(fb-sales-material.ytd-avg,"->>,>>>,>>>,>>9.99").
       
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 21
               stream-list.cval    = STRING(fb-sales-material.ytd-rev,"->>,>>>,>>>,>>9.99").
    END.

    ct-row2 = ct-row2 + 3.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "BANQUET REVENUE".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 13
           stream-list.cval    = "Today Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "Today Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 15
           stream-list.cval    = "Today Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "MTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 17
           stream-list.cval    = "MTD Average".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 18
           stream-list.cval    = "MTD Revenue".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 19
           stream-list.cval    = "YTD Cover".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 20
           stream-list.cval    = "YTD Average".

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 21
           stream-list.cval    = "YTD Revenue".
    
   FOR EACH fb-sales-other NO-LOCK:
    
        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 12
               stream-list.cval    = STRING(fb-sales-other.descr).
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 13
               stream-list.cval    = STRING(fb-sales-other.tday-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 14
               stream-list.cval    = STRING(fb-sales-other.tday-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 15
               stream-list.cval    = STRING(fb-sales-other.tday-rev,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 16
               stream-list.cval    = STRING(fb-sales-other.mtd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 17
               stream-list.cval    = STRING(fb-sales-other.mtd-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 18
               stream-list.cval    = STRING(fb-sales-other.mtd-rev,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 19
               stream-list.cval    = STRING(fb-sales-other.ytd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 20
               stream-list.cval    = STRING(fb-sales-other.ytd-avg,"->>,>>>,>>>,>>9.99").
       
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 21
               stream-list.cval    = STRING(fb-sales-other.ytd-rev,"->>,>>>,>>>,>>9.99").
    END.
    
   ct-row2 = ct-row2 + 2.

   FOR EACH fb-sales-tot NO-LOCK:
    
        ct-row2 = ct-row2 + 1.

        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 12
               stream-list.cval    = STRING(fb-sales-tot.descr).
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 13
               stream-list.cval    = STRING(fb-sales-tot.tday-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 14
               stream-list.cval    = STRING(fb-sales-tot.tday-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 15
               stream-list.cval    = STRING(fb-sales-tot.tday-rev,"->>,>>>,>>>,>>9.99"). 
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 16
               stream-list.cval    = STRING(fb-sales-tot.mtd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 17
               stream-list.cval    = STRING(fb-sales-tot.mtd-avg,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 18
               stream-list.cval    = STRING(fb-sales-tot.mtd-rev,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 19
               stream-list.cval    = STRING(fb-sales-tot.ytd-cov,"->>,>>>,>>>,>>9.99").
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 20
               stream-list.cval    = STRING(fb-sales-tot.ytd-avg,"->>,>>>,>>>,>>9.99").
       
        CREATE stream-list.
        ASSIGN stream-list.crow    = ct-row2
               stream-list.ccol    = 21
               stream-list.cval    = STRING(fb-sales-tot.ytd-rev,"->>,>>>,>>>,>>9.99").
    END.

    ct-row2 = ct-row2 + 3.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "Prepared By".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "Checked By".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "Approved By".

    ct-row2 = ct-row2 + 6.

    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 12
           stream-list.cval    = "Night Audit".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 14
           stream-list.cval    = "Income Audit".
    CREATE stream-list.
    ASSIGN stream-list.crow    = ct-row2
           stream-list.ccol    = 16
           stream-list.cval    = "Chief Accountant".


    /*output to .txt*/
    FOR EACH stream-list NO-LOCK BY stream-list.crow BY stream-list.ccol:
        IF stream-list.cval NE "" THEN
            PUT STREAM s1 UNFORMATTED 
                STRING(stream-list.crow) ";" STRING(stream-list.ccol) ";" stream-list.cval SKIP.
        ELSE
            PUT STREAM s1 UNFORMATTED 
                STRING(stream-list.crow) ";" STRING(stream-list.ccol) ";" "''" SKIP.
    END.
    
    OUTPUT STREAM s1 CLOSE.
    
    /*OS-COMMAND SILENT VALUE("php C:\vhp\php-script\write-sheet.php C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt " + gsheet-link).*/
    
    OS-COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/outputFO_" + htl-no + ".txt " + gsheet-link).

PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
    END. 

