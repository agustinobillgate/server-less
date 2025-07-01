
DEFINE TEMP-TABLE s-order LIKE fa-order
    /* Dzikri - 01B1DB create new input */
    /* FIELD budget-date       AS DATE */
    /* Dzikri - 01B1DB END */
    FIELD nr-budget AS INTEGER.

DEF INPUT PARAMETER TABLE FOR s-order.
DEF INPUT PARAMETER order-nr            AS CHAR.
DEF INPUT PARAMETER credit-term         AS INT.
DEF INPUT PARAMETER curr                AS INTEGER.
DEF INPUT PARAMETER dept-nr             AS INT.
DEF INPUT PARAMETER order-date          AS DATE.
DEF INPUT PARAMETER supplier-nr         AS INT.
DEF INPUT PARAMETER Expected-Delivery   AS DATE.
DEF INPUT PARAMETER order-type          AS CHAR.
DEF INPUT PARAMETER order-name          AS CHAR.
DEF INPUT PARAMETER comments            AS CHAR.
DEF INPUT PARAMETER user-init           AS CHAR.
DEF INPUT PARAMETER billdate            AS DATE.
DEF INPUT PARAMETER appr-1              AS LOGICAL.

DEF VAR pos         AS INTEGER INITIAL 0.
DEF VAR total-order AS DECIMAL INITIAL 0.
DEF VAR pr-nr       AS CHARACTER INITIAL "".

FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = order-nr EXCLUSIVE-LOCK.
IF AVAILABLE fa-ordheader THEN
DO:
    ASSIGN 
        fa-ordheader.order-nr           = order-nr
        fa-ordheader.credit-term        = credit-term 
        fa-ordheader.currency           = curr /*local-nr cmb-curr*/
        fa-ordheader.dept-nr            = dept-nr 
        fa-ordheader.order-date         = order-date
        fa-ordheader.supplier-nr        = supplier-nr 
        fa-ordheader.expected-delivery  = Expected-Delivery 
        fa-ordheader.order-type         = order-type
        fa-ordheader.order-name         = order-name
        fa-ordheader.order-desc         = comments
        fa-ordheader.modified-By        = user-init /*bediener.username */     
        fa-ordheader.modified-Date      = billdate       
        fa-ordheader.modified-Time      = TIME 
        pr-nr                           = fa-ordheader.PR-Nr
        /*fa-ordheader.printed = ?*/ .

    IF fa-ordheader.approved-1 = NO AND appr-1 = YES THEN
    DO:
        ASSIGN fa-ordheader.Approved-1         = appr-1
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
            . 
    END.
    
    IF fa-ordheader.released-flag = NO THEN
    DO:
        IF fa-ordheader.approved-1 = YES THEN
        DO:

            ASSIGN fa-ordheader.released-flag = YES
                   fa-ordheader.released-date = billdate
                   fa-ordheader.released-time = TIME.
        END.
    END.
END.

FOR EACH fa-order WHERE fa-order.order-nr = order-nr :
    DELETE fa-order.
END.

FOR EACH queasy WHERE queasy.key EQ 315 AND queasy.char1 EQ order-nr AND queasy.char2 EQ pr-nr :
    DELETE queasy.
END.

FOR EACH s-order  :
    pos = pos + 1.
    total-order = total-order + s-order.order-amount.
    CREATE fa-order.
    ASSIGN fa-order.Order-Nr    = s-order.order-nr
       fa-order.Fa-Nr           = s-order.fa-nr                  
       fa-order.Order-Qty       = s-order.order-qty     
       fa-order.Order-Price     = s-order.order-price       
       fa-order.Discount1       = s-order.discount1       
       fa-order.Discount2       = s-order.discount2        
       fa-order.VAT             = s-order.vat   
       fa-order.Order-Amount    = s-order.order-amount
       fa-order.Fa-remarks      = s-order.fa-remarks                                          
       /*
       fa-order.change-By       = user-init       
       fa-order.change-Date     = billdate       
       fa-order.change-Time     = TIME   
       */               
       fa-order.statFlag        = 0       
       fa-order.Fa-Pos          = pos       
       fa-order.op-art          = 2 
       fa-order.last-ID         = user-init.

       IF s-order.ActiveReason NE "" AND s-order.ActiveReason NE ? THEN
            fa-order.ActiveReason    = s-order.ActiveReason.
       ELSE
            fa-order.ActiveReason    = STRING(s-order.nr-budget).

    /* 
    /* Dzikri - 01B1DB create new input */
    CREATE queasy.
    ASSIGN queasy.key                = 315
           queasy.char1              = order-nr
           queasy.char2              = pr-nr
           /* queasy.char3              =  */
           queasy.number1            = s-order.fa-nr
           /* queasy.deci1              = s-order.budget-assetnr */
           queasy.number3            = pos
           queasy.date1              = s-order.budget-date
           .
    /* Dzikri - 01B1DB END */
    */
END.

ASSIGN fa-ordheader.total-amount = total-order.
