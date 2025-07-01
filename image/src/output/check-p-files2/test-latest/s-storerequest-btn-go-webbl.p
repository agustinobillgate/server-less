DEFINE TEMP-TABLE op-list LIKE l-op 
  /*FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD acct-bez AS CHAR*/
  FIELD bezeich     AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username    AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand      AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On Hand"
  FIELD acct-bez    AS CHAR
  FIELD masseinheit AS CHAR FORMAT "x(20)"             COLUMN-LABEL "Mess Unit"
.

/* Oscar (14/03/25) - 3E510E - change payload format and add new field sr-remark */
DEFINE TEMP-TABLE payload-list
  FIELD recid-l-ophdr AS INTEGER
  FIELD transdate     AS CHARACTER
  FIELD curr-lager    AS INTEGER
  FIELD transfered    AS LOGICAL
  FIELD cost-acct     AS CHARACTER
  FIELD deptNo        AS INTEGER
  FIELD to-stock      AS INTEGER
  FIELD lscheinnr     AS CHARACTER
  FIELD user-init     AS CHARACTER
  FIELD sr-remark     AS CHARACTER
.

/* Oscar (14/03/25) - 3E510E - change response format */
DEFINE TEMP-TABLE response-list
  FIELD s-artnr AS INTEGER
  FIELD qty     AS DECIMAL
  FIELD price   AS DECIMAL
  FIELD created AS LOGICAL
.

DEF INPUT PARAMETER TABLE FOR payload-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.
DEF OUTPUT PARAMETER TABLE FOR response-list.

DEF VARIABLE recid-l-ophdr AS INT.
DEF VARIABLE transdate     AS DATE.
DEF VARIABLE curr-lager    AS INT.
DEF VARIABLE transfered    AS LOGICAL.
DEF VARIABLE cost-acct     AS CHAR.
DEF VARIABLE deptNo        AS INT.
DEF VARIABLE to-stock      AS INT.
DEF VARIABLE lscheinnr     AS CHAR.
DEF VARIABLE user-init     AS CHAR.
DEF VARIABLE sr-remark     AS CHAR.

DEF VARIABLE s-artnr        AS INT.
DEF VARIABLE qty            AS DECIMAL.
DEF VARIABLE price          AS DECIMAL.
DEF VARIABLE created AS LOGICAL.

DEFINE VARIABLE curr-pos    AS INTEGER.
DEFINE VARIABLE zeit        AS INTEGER. 
DEFINE VARIABLE amount      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99". 

/*FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = recid-l-ophdr.

DO TRANSACTION:
    FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
    l-ophdr.datum =  transdate. 
    l-ophdr.lager-nr = curr-lager. 
    IF NOT transfered THEN l-ophdr.fibukonto = cost-acct. 
    FIND CURRENT l-ophdr NO-LOCK. 
END. 
RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1.*/

CREATE response-list.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        recid-l-ophdr = payload-list.recid-l-ophdr  
        curr-lager    = payload-list.curr-lager   
        transfered    = payload-list.transfered   
        cost-acct     = payload-list.cost-acct    
        deptNo        = payload-list.deptNo       
        to-stock      = payload-list.to-stock     
        lscheinnr     = payload-list.lscheinnr    
        user-init     = payload-list.user-init    
        sr-remark     = payload-list.sr-remark
    .

    transdate = DATE(INTEGER(SUBSTRING(payload-list.transdate, 1, 2)), 
                     INTEGER(SUBSTRING(payload-list.transdate, 4, 2)), 
                     2000 + INTEGER(SUBSTRING(payload-list.transdate, 7, 2))).

    /*Alder - Serverless - Issue 545 - Start*/
    FIND FIRST bediener WHERE bediener.userinit = user-init.


    FIND FIRST l-ophdr WHERE RECID(l-ophdr) EQ recid-l-ophdr NO-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr THEN
    DO:
        FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
        l-ophdr.datum =  transdate. 
        l-ophdr.lager-nr = curr-lager. 
        IF NOT transfered THEN l-ophdr.fibukonto = cost-acct. 
        FIND CURRENT l-ophdr NO-LOCK.
        RELEASE l-ophdr.
    END.

    RUN l-op-pos(OUTPUT curr-pos). 
    curr-pos = curr-pos - 1.
    /*Alder - Serverless - Issue 545 - End*/
    
    zeit = time. 
    FOR EACH op-list WHERE op-list.anzahl NE 0: 
        zeit = zeit + 1. 
        curr-pos = curr-pos + 1. 
        s-artnr = op-list.artnr. 
        qty = op-list.anzahl. 
        price = op-list.warenwert / qty. 
        curr-lager = op-list.lager-nr. 
        cost-acct = op-list.stornogrund. 
        RUN create-l-op (zeit). 
    END. 
    FOR EACH op-list: 
        DELETE op-list. 
    END. 

    /* Oscar (14/03/25) - 3E510E - save field sr-remark */
    CREATE queasy.
    ASSIGN
        queasy.KEY = 343
        queasy.char1 = lscheinnr
        queasy.char2 = sr-remark
        queasy.date1 = transdate
    .


    FIND FIRST response-list EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE response-list THEN
        ASSIGN
            response-list.s-artnr = s-artnr
            response-list.qty     = qty    
            response-list.price   = price  
            response-list.created = created
        .
END.


PROCEDURE l-op-pos: 
    DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
    DEFINE BUFFER l-op1 FOR l-op. 

    FOR EACH l-op1 WHERE l-op1.lscheinnr = lscheinnr 
        AND l-op1.loeschflag GE 0 AND l-op1.pos GT 0 NO-LOCK: 

        IF l-op1.pos GT pos THEN pos = l-op1.pos. 
    END. 
    pos = pos + 1. 
END. 


PROCEDURE create-l-op: 
    DEFINE INPUT PARAMETER zeit AS INTEGER. 
    DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
    DEFINE VARIABLE wert AS DECIMAL. 
    
    DEFINE VARIABLE anz-oh AS DECIMAL. 
    DEFINE VARIABLE val-oh AS DECIMAL. 
    
    ASSIGN
        anzahl   = qty 
        wert     = qty * price 
        amount   = wert
        t-amount = t-amount + wert
        created  = TRUE
    . 
    
    /* Create l-op record */ 
    CREATE l-op. 
    ASSIGN
        l-op.datum          = transdate
        l-op.lager-nr       = curr-lager 
        l-op.artnr          = s-artnr
        l-op.zeit           = zeit
        l-op.anzahl         = anzahl 
        l-op.einzelpreis    = price 
        l-op.warenwert      = wert
        l-op.reorgflag      = deptNo
    . 

    IF transfered THEN l-op.op-art = 14. 
    ELSE l-op.op-art = 13. 

    ASSIGN
        l-op.herkunftflag = 1   
        l-op.lscheinnr    = lscheinnr
    . 

    IF NOT transfered THEN 
        ASSIGN 
            l-op.pos         = curr-pos 
            l-op.stornogrund = cost-acct
        . 
    ELSE l-op.pos = to-stock. 

    IF AVAILABLE bediener THEN l-op.fuellflag = bediener.nr. 
    FIND CURRENT l-op NO-LOCK. 
END. 

