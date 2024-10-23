DEFINE TEMP-TABLE output-list 
    FIELD gop-flag      AS LOGICAL INITIAL NO 
    FIELD nr            AS INTEGER 
    FIELD STR           AS CHAR 
    FIELD budget        AS DECIMAL 
    FIELD proz          AS DECIMAL FORMAT "->>>>>" LABEL "(%)"
    FIELD mark          AS LOGICAL INITIAL NO FORMAT "Yes/No"
    FIELD ch            AS CHAR FORMAT "x(2)"
    FIELD ref-no        AS CHARACTER
    FIELD begin-bal     AS CHARACTER
    FIELD tot-debit     AS CHARACTER
    FIELD tot-credit    AS CHARACTER
    FIELD net-change    AS CHARACTER
    FIELD ending-bal    AS CHARACTER
    FIELD ytd-bal       AS CHARACTER
    INDEX nr_idx nr
    .

DEFINE TEMP-TABLE tb-list-summary
    FIELD account-no    AS CHARACTER   
    FIELD DESCRIPTION   AS CHARACTER   
    FIELD beginingbal   AS CHARACTER
    FIELD tot-debit     AS CHARACTER
    FIELD tot-credit    AS CHARACTER
    FIELD net-change    AS CHARACTER
    FIELD ending-bal    AS CHARACTER 
    FIELD ytd-balance   AS CHARACTER
    FIELD budget        AS DECIMAL 
    FIELD proz          AS DECIMAL
    .

DEFINE TEMP-TABLE tb-list-detail
    FIELD marks         AS CHARACTER
    FIELD DATE          AS DATE
    FIELD ref-no        AS CHARACTER
    FIELD begining-bal  AS CHARACTER 
    FIELD tot-debit     AS CHARACTER  
    FIELD tot-credit    AS CHARACTER  
    FIELD net-change    AS CHARACTER  
    FIELD ending-bal    AS CHARACTER 
    FIELD note          AS CHARACTER 
    .

DEF INPUT PARAMETER acct-type    AS INT.
DEF INPUT PARAMETER from-fibu    AS CHAR.
DEF INPUT PARAMETER to-fibu      AS CHAR.
DEF INPUT PARAMETER sorttype     AS INT.
DEF INPUT PARAMETER from-dept    AS INT.
DEF INPUT PARAMETER from-date    AS DATE.
DEF INPUT PARAMETER to-date      AS DATE.
DEF INPUT PARAMETER close-month  AS INT.
DEF INPUT PARAMETER close-date   AS DATE.
DEF INPUT PARAMETER pnl-acct     AS CHAR.
DEF INPUT PARAMETER close-year   AS DATE.
DEF INPUT PARAMETER prev-month   AS INT.
DEF INPUT PARAMETER show-longbal AS LOGICAL.
DEF INPUT PARAMETER pbal-flag    AS LOGICAL.
DEF INPUT PARAMETER ASremoteFlag AS LOGICAL.
DEF OUTPUT PARAMETER msg-str     AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR tb-list-detail.
DEF OUTPUT PARAMETER TABLE FOR tb-list-summary.

DEFINE VARIABLE refNO           AS CHAR.
DEFINE VARIABLE begining-bal    AS CHAR.  
DEFINE VARIABLE tot-debit       AS CHAR.  
DEFINE VARIABLE tot-credit      AS CHAR.  
DEFINE VARIABLE net-change      AS CHAR.  
DEFINE VARIABLE ending-bal      AS CHAR.  
DEFINE VARIABLE ytd-balance     AS CHAR.  
/*
IF sorttype EQ 1 THEN
DO:
    IF acct-type EQ 0 THEN
    DO:
        msg-str = "please select account type first and can't be ALL".
        RETURN.
    END.
END.
*/


RUN trialbalance-btn-go-cldbl.p (acct-type, from-fibu, to-fibu, sorttype, from-dept, from-date,
           to-date, close-month, close-date, pnl-acct, close-year,
           prev-month, show-longbal, pbal-flag, ASremoteFlag,
           OUTPUT TABLE output-list).

IF sorttype EQ 1 THEN /*detail*/
DO:
    FOR EACH output-list:
        ASSIGN 
            /*refNO        = SUBSTRING(output-list.STR, 9, 16)                    
            begining-bal = (REPLACE(SUBSTRING(output-list.STR, 25, 22),",",""))
            tot-debit    = (REPLACE(SUBSTRING(output-list.STR, 47, 22),",","")) 
            tot-credit   = (REPLACE(SUBSTRING(output-list.STR, 69, 22),",","")) 
            net-change   = (REPLACE(SUBSTRING(output-list.STR, 91, 22),",","")) 
            ending-bal   = (REPLACE(SUBSTRING(output-list.STR, 113, 22),",",""))
            */
            /*FDL June 11, 2024 => Ticket 62094C*/             
            refNO        = output-list.ref-no
            begining-bal = output-list.begin-bal
            tot-debit    = output-list.tot-debit
            tot-credit   = output-list.tot-credit
            net-change   = output-list.net-change
            ending-bal   = output-list.ending-bal
        .
        IF begining-bal MATCHES "*(*" THEN begining-bal = REPLACE(begining-bal,"(","-").
        IF begining-bal MATCHES "*)*" THEN begining-bal = REPLACE(begining-bal,")","").

        IF tot-debit MATCHES "*(*" THEN tot-debit = REPLACE(tot-debit,"(","-").
        IF tot-debit MATCHES "*)*" THEN tot-debit = REPLACE(tot-debit,")","").

        IF tot-credit MATCHES "*(*" THEN tot-credit = REPLACE(tot-credit,"(","-").
        IF tot-credit MATCHES "*)*" THEN tot-credit = REPLACE(tot-credit,")","").

        IF net-change MATCHES "*(*" THEN net-change = REPLACE(net-change,"(","-").
        IF net-change MATCHES "*)*" THEN net-change = REPLACE(net-change,")","").

        IF ending-bal MATCHES "*(*" THEN ending-bal = REPLACE(ending-bal,"(","-").
        IF ending-bal MATCHES "*)*" THEN ending-bal = REPLACE(ending-bal,")","").
        /* FDL COmment
        refNO = REPLACE(refNO,".","").
        refNO = REPLACE(refNO,"-","").
        */
        CREATE tb-list-detail.
        ASSIGN 
            tb-list-detail.marks        = output-list.CH
            tb-list-detail.DATE         = DATE(TRIM(SUBSTRING(output-list.STR, 1, 8)))   
            tb-list-detail.ref-no       = refNO
            tb-list-detail.begining-bal = begining-bal 
            tb-list-detail.tot-debit    = tot-debit    
            tb-list-detail.tot-credit   = tot-credit   
            tb-list-detail.net-change   = net-change   
            tb-list-detail.ending-bal   = ending-bal   
            tb-list-detail.note         = SUBSTR(output-list.STR,135, 62)
            .           
    END.
END.
ELSE    /*summary*/
DO:
    FOR EACH output-list:
        ASSIGN 
            refNO        = SUBSTRING(output-list.STR, 1, 16)
            begining-bal = (REPLACE(SUBSTRING(output-list.STR, 55, 22),",",""))
            tot-debit    = (REPLACE(SUBSTRING(output-list.STR, 77, 22),",",""))
            tot-credit   = (REPLACE(SUBSTRING(output-list.STR, 99, 22),",",""))
            net-change   = (REPLACE(SUBSTRING(output-list.STR, 121, 22),",",""))
            ending-bal   = (REPLACE(SUBSTRING(output-list.STR, 143, 22),",",""))
            ytd-balance  = (REPLACE(SUBSTRING(output-list.STR, 165, 22),",",""))
        .
        IF begining-bal MATCHES "*(*" THEN begining-bal = REPLACE(begining-bal,"(","-").
        IF begining-bal MATCHES "*)*" THEN begining-bal = REPLACE(begining-bal,")","").

        IF tot-debit MATCHES "*(*" THEN tot-debit = REPLACE(tot-debit,"(","-").
        IF tot-debit MATCHES "*)*" THEN tot-debit = REPLACE(tot-debit,")","").

        IF tot-credit MATCHES "*(*" THEN tot-credit = REPLACE(tot-credit,"(","-").
        IF tot-credit MATCHES "*)*" THEN tot-credit = REPLACE(tot-credit,")","").

        IF net-change MATCHES "*(*" THEN net-change = REPLACE(net-change,"(","-").
        IF net-change MATCHES "*)*" THEN net-change = REPLACE(net-change,")","").

        IF ending-bal MATCHES "*(*" THEN ending-bal = REPLACE(ending-bal,"(","-").
        IF ending-bal MATCHES "*)*" THEN ending-bal = REPLACE(ending-bal,")","").

        IF ytd-balance MATCHES "*(*" THEN ytd-balance = REPLACE(ytd-balance,"(","-").
        IF ytd-balance MATCHES "*)*" THEN ytd-balance = REPLACE(ytd-balance,")","").
        /*
        refNO = REPLACE(refNO,".","").
        refNO = REPLACE(refNO,"-","").
        */
        CREATE tb-list-summary.
        ASSIGN 
            tb-list-summary.account-no   = TRIM(refNO)    
            tb-list-summary.DESCRIPTION  = TRIM(SUBSTRING(output-list.STR, 17, 38))     
            tb-list-summary.beginingbal  = begining-bal     
            tb-list-summary.tot-debit    = tot-debit       
            tb-list-summary.tot-credit   = tot-credit      
            tb-list-summary.net-change   = net-change  
            tb-list-summary.ending-bal   = ending-bal  
            tb-list-summary.ytd-balance  = ytd-balance 
            tb-list-summary.budget       = output-list.budget 
            tb-list-summary.proz         = output-list.proz   
            .                           
    END. 
END.
