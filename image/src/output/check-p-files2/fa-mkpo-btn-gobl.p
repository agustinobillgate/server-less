DEFINE TEMP-TABLE tfa-order LIKE fa-order.

DEF INPUT PARAMETER TABLE FOR tfa-order.
DEF INPUT PARAMETER cmb-curr-screen-value AS CHAR.
DEF INPUT PARAMETER local-nr AS INT.
DEF INPUT PARAMETER order-nr AS CHAR.
DEF INPUT PARAMETER pr-nr AS CHAR.
DEF INPUT PARAMETER order-date AS DATE.
DEF INPUT PARAMETER order-type AS CHAR.
DEF INPUT PARAMETER order-name AS CHAR.
DEF INPUT PARAMETER Comments AS CHAR.
DEF INPUT PARAMETER supplier-nr AS INT.
DEF INPUT PARAMETER dept-nr AS INT.
DEF INPUT PARAMETER credit-term AS INT.
DEF INPUT PARAMETER paymentdate AS DATE.
DEF INPUT PARAMETER Expected-Delivery AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER t-amount AS DECIMAL.
DEF INPUT PARAMETER appr-1 AS LOGICAL.
DEF INPUT PARAMETER answer AS LOGICAL.


DEFINE VARIABLE curr      AS INTEGER.
DEFINE VARIABLE repos     AS INTEGER INITIAL 0.

FIND FIRST tfa-order NO-ERROR.
FIND FIRST waehrung WHERE waehrung.wabkurz = cmb-curr-screen-value NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN curr = waehrung.waehrungsnr.
ELSE curr =  local-nr.
RUN re-numbering.


CREATE fa-ordheader.
ASSIGN  fa-ordheader.order-nr            = order-nr
        fa-ordheader.PR-Nr               = pr-nr 
        fa-ordheader.Order-Date          = order-date     
        fa-ordheader.Order-Type          = order-type     
        fa-ordheader.Order-Name          = order-name    
        fa-ordheader.Order-Desc          = Comments     
        fa-ordheader.Supplier-Nr         = supplier-nr      
        fa-ordheader.Dept-Nr             = dept-nr       
        fa-ordheader.Credit-Term         = credit-term  
        fa-ordheader.currency            = curr
        fa-ordheader.PaymentDate         = paymentdate     
        fa-ordheader.Expected-Delivery   = Expected-Delivery  
        fa-ordheader.created-by          = user-init /*created-by*/
        fa-ordheader.Created-Date        = billdate      
        fa-ordheader.Created-Time        = TIME   
        fa-ordheader.ActiveFlag          = 0     
        fa-ordheader.statFlag            = 0 
        fa-ordheader.printed             = ? 
        fa-ordheader.total-Amount         = t-amount.
        
IF appr-1 = YES THEN
DO:
    ASSIGN
    fa-ordheader.Approved-1         = appr-1
    fa-ordheader.Approved-1-By      = user-init  
    fa-ordheader.Approved-1-Date    = billdate     
    fa-ordheader.Approved-1-time    = TIME

    fa-ordheader.Approved-2         = appr-1
    fa-ordheader.Approved-2-By      = user-init  
    fa-ordheader.Approved-2-Date    = billdate     
    fa-ordheader.Approved-2-time    = TIME

    fa-ordheader.Approved-3         = appr-1
    fa-ordheader.Approved-3-By      = user-init  
    fa-ordheader.Approved-3-Date    = billdate     
    fa-ordheader.Approved-3-time    = TIME

    fa-ordheader.released-flag = YES
    fa-ordheader.released-by   = user-init 
    fa-ordheader.released-date = billdate.
    fa-ordheader.released-time = TIME
    . 
END.


FOR EACH tfa-order BY tfa-order.fa-pos  : 
    repos = repos + 1.
    CREATE fa-order.
    ASSIGN fa-order.Order-Nr        = order-nr
           fa-order.Fa-Nr           = tfa-order.Fa-Nr               
           fa-order.Order-Qty       = tfa-order.Order-Qty    
           fa-order.Order-Price     = tfa-order.Order-Price     
           fa-order.Discount1       = tfa-order.Discount1    
           fa-order.Discount2       = tfa-order.Discount2      
           fa-order.VAT             = tfa-order.VAT   
           fa-order.Order-Amount    = tfa-order.Order-Amount
           fa-order.Fa-remarks      = tfa-order.Fa-remarks                                          
           fa-order.Create-By       = tfa-order.Create-By     
           fa-order.Create-Date     = tfa-order.Create-Date       
           fa-order.Create-Time     = tfa-order.Create-Time                  
           fa-order.statFlag        = tfa-order.statFlag  
           fa-order.Fa-Pos          = repos /*tfa-order.Fa-Pos  */    
           fa-order.op-art          = tfa-order.op-art 
           fa-order.activeflag      = 0
           fa-order.create-by       = user-init
           fa-order.CREATE-date     = billdate
           fa-order.create-time     = TIME.

    DELETE tfa-order.

END.

IF NOT (appr-1 = YES) THEN
DO:
    IF answer THEN
    DO:
        ASSIGN
            appr-1 = YES.

        ASSIGN
            fa-ordheader.Approved-1         = appr-1
            fa-ordheader.Approved-1-By      = user-init  
            fa-ordheader.Approved-1-Date    = billdate     
            fa-ordheader.Approved-1-time    = TIME 
            fa-ordheader.Approved-2         = appr-1
            fa-ordheader.Approved-2-By      = user-init  
            fa-ordheader.Approved-2-Date    = billdate     
            fa-ordheader.Approved-2-time    = TIME 
            fa-ordheader.Approved-3         = appr-1
            fa-ordheader.Approved-3-By      = user-init  
            fa-ordheader.Approved-3-Date    = billdate     
            fa-ordheader.Approved-3-time    = TIME 
            fa-ordheader.released-flag      = YES
            fa-ordheader.released-by        = user-init 
            fa-ordheader.released-date      = billdate
            fa-ordheader.released-time      = TIME.
    END.
    
END.
ELSE
DO:
    run print-it.
END.


PROCEDURE re-numbering PRIVATE :
    DEFINE VARIABLE thereis AS LOGICAL INITIAL YES.

    DO WHILE thereis = YES :
        FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = order-nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-ordheader THEN
        DO:
            thereis = YES.
            RUN new-fapo-number.
            RUN update-counters.
        END.
        ELSE
        DO:
            thereis = NO.
            RUN new-fapo-number.
            RUN update-counters.
        END.
    END.

END PROCEDURE.

PROCEDURE new-fapo-number :
    DEFINE BUFFER fa-orderhdr1 FOR fa-ordheader. 
    DEFINE VARIABLE s AS CHAR. 
    DEFINE VARIABLE i AS INTEGER INITIAL 1. 
    DEFINE VARIABLE mm AS INTEGER. 
    DEFINE VARIABLE yy AS INTEGER. 
    DEFINE VARIABLE dd AS INTEGER.
    DEFINE VARIABLE docu-nr AS CHAR.
    DEF VAR a AS LOGICAL.

    FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
    IF htparam.paramgr = 21 THEN 
    DO:
        mm = month(billdate). 
        yy = year(billdate). 
        dd = DAY(billdate).

        s = "F" + SUBSTR(STRING(year(billdate)),3,2) 
          + STRING(MONTH(billdate), "99").   

        IF htparam.flogical THEN
        DO:
            FIND FIRST fa-counter WHERE fa-counter.count-type = 0 AND fa-counter.yy = yy AND fa-counter.mm = mm AND
                fa-counter.dd = dd AND fa-counter.docu-type = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE fa-counter THEN
            DO:
                CREATE fa-counter.
                ASSIGN fa-counter.count-type = 0
                       fa-counter.yy         = yy
                       fa-counter.mm         = mm
                       fa-counter.dd         = dd
                       fa-counter.counters   = 0
                       fa-counter.docu-type   = 0 .

            END.
            FIND CURRENT fa-counter NO-LOCK.
            i = fa-counter.counters + 1 .
            docu-nr = s + string(dd,"99") + STRING(i, "999").
        END.
        ELSE
        DO:
            FIND FIRST fa-counter WHERE fa-counter.count-type = 1 AND fa-counter.yy = yy 
                AND fa-counter.mm = mm AND fa-counter.docu-type = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE fa-counter THEN
            DO:
                CREATE fa-counter.
                ASSIGN fa-counter.count-type = 1
                       fa-counter.yy         = yy
                       fa-counter.mm         = mm
                       fa-counter.dd         = 0
                       fa-counter.counters   = 0
                       fa-counter.docu-type   = 0 .

            END.
            FIND CURRENT fa-counter NO-LOCK.
            i = fa-counter.counters + 1.
            docu-nr = s + STRING(i, "99999"). 
        END.
    END.

    ASSIGN order-nr = docu-nr.
    /*MTDISP order-nr WITH FRAME frame1.*/

END PROCEDURE.

PROCEDURE update-counters :
    DEFINE VARIABLE s AS CHAR. 
    DEFINE VARIABLE i AS INTEGER INITIAL 1. 
    DEFINE VARIABLE mm AS INTEGER. 
    DEFINE VARIABLE yy AS INTEGER. 
    DEFINE VARIABLE dd AS INTEGER.
    DEFINE VARIABLE docu-nr AS CHAR.
    DEF VAR a AS LOGICAL.
    a = YES.

    FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
    IF htparam.paramgr = 21 THEN 
    DO:
        mm = month(billdate). 
        yy = year(billdate). 
        dd = DAY(billdate).

        s = "F" + SUBSTR(STRING(year(billdate)),3,2) 
          + STRING(MONTH(billdate), "99").   

        IF htparam.flogical THEN
        DO:
            FIND FIRST fa-counter WHERE fa-counter.count-type = 0 AND fa-counter.yy = yy AND fa-counter.mm = mm AND
                fa-counter.dd = dd AND fa-counter.docu-type = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE fa-counter THEN
            DO:
                CREATE fa-counter.
                ASSIGN fa-counter.count-type = 0
                       fa-counter.yy         = yy
                       fa-counter.mm         = mm
                       fa-counter.dd         = dd
                       fa-counter.counters   = 0
                       fa-counter.docu-type  = 0.
            END.
            ELSE
            DO:
                FIND CURRENT fa-counter EXCLUSIVE-LOCK.
                ASSIGN fa-counter.counters = fa-counter.counters + 1.
                FIND CURRENT fa-counter NO-LOCK.
            END.   
        END.
        ELSE
        DO:
            FIND FIRST fa-counter WHERE fa-counter.count-type = 1 AND fa-counter.yy = yy AND fa-counter.mm = mm 
                AND fa-counter.docu-type = 0  EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE fa-counter THEN
            DO:
                CREATE fa-counter.
                ASSIGN fa-counter.count-type = 1
                       fa-counter.yy         = yy
                       fa-counter.mm         = mm
                       fa-counter.dd         = 0
                       fa-counter.counters   = 0
                       fa-counter.docu-type  = 0.
            END.
            ELSE
            DO:
                FIND CURRENT fa-counter EXCLUSIVE-LOCK.
                ASSIGN fa-counter.counters = fa-counter.counters + 1.
                FIND CURRENT fa-counter NO-LOCK.
            END.
        END.
    END.
END PROCEDURE.
