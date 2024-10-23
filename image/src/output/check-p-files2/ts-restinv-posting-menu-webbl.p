DEF TEMP-TABLE t-menu-list
    FIELD request AS CHAR 
    FIELD krecid  AS INTEGER INITIAL 0 
    FIELD posted  AS LOGICAL INITIAL NO 
    FIELD nr      AS INTEGER FORMAT ">>>" LABEL "No" 
    FIELD artnr   LIKE h-artikel.artnr 
    FIELD bezeich LIKE h-artikel.bezeich 
    FIELD anzahl  LIKE h-bill-line.anzahl INITIAL 1 
    FIELD price   AS DECIMAL 
    FIELD betrag  AS DECIMAL 
    FIELD voucher AS CHAR    INITIAL "".

DEFINE TEMP-TABLE menu-list 
    FIELD request AS CHAR 
    FIELD krecid  AS INTEGER INITIAL 0 
    FIELD posted  AS LOGICAL INITIAL NO 
    FIELD nr      AS INTEGER FORMAT ">>>" LABEL "No" 
    FIELD artnr   LIKE h-artikel.artnr 
    FIELD bezeich LIKE h-artikel.bezeich 
    FIELD anzahl  LIKE h-bill-line.anzahl INITIAL 1 
    FIELD price   AS DECIMAL 
    FIELD betrag  AS DECIMAL 
    FIELD voucher AS CHAR    INITIAL "". 

DEFINE TEMP-TABLE submenu-list 
    FIELD menurecid AS INTEGER 
    FIELD zeit      AS INTEGER 
    FIELD nr        AS INTEGER 
    FIELD artnr     LIKE h-artikel.artnr 
    FIELD bezeich   LIKE h-artikel.bezeich 
    FIELD anzahl    AS INTEGER 
    FIELD zknr      AS INTEGER 
    FIELD request   AS CHAR. 

DEFINE TEMP-TABLE bmenu /*LIKE menu-list*/
    FIELD request AS CHAR 
    FIELD krecid  AS INTEGER INITIAL 0 
    FIELD posted  AS LOGICAL INITIAL NO 
    FIELD nr      AS INTEGER FORMAT ">>>" LABEL "No" 
    FIELD artnr   LIKE h-artikel.artnr 
    FIELD bezeich LIKE h-artikel.bezeich 
    FIELD anzahl  LIKE h-bill-line.anzahl INITIAL 1 
    FIELD price   AS DECIMAL 
    FIELD betrag  AS DECIMAL 
    FIELD voucher AS CHAR    INITIAL ""
    FIELD rec-menu AS INTEGER.
DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INTEGER.
DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.
DEF TEMP-TABLE kellner1 LIKE kellner. 

DEF TEMP-TABLE t-submenu-list
    FIELD menurecid AS INTEGER 
    FIELD zeit      AS INTEGER 
    FIELD nr        AS INTEGER 
    FIELD artnr     LIKE h-artikel.artnr 
    FIELD bezeich   LIKE h-artikel.bezeich 
    FIELD anzahl    AS INTEGER 
    FIELD zknr      AS INTEGER 
    FIELD request   AS CHAR. 

DEFINE TEMP-TABLE tp-bediener  LIKE bediener. 
DEFINE TEMP-TABLE tp-bediener1  LIKE bediener.  

DEFINE INPUT PARAMETER case-type            AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER pvILanguage          AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER tischnr              AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER curr-dept            AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER cancel-reason        AS CHAR      NO-UNDO.
DEFINE INPUT PARAMETER double-currency      AS LOGICAL   NO-UNDO.
DEFINE INPUT PARAMETER exchg-rate           AS DECIMAL   NO-UNDO.
DEFINE INPUT PARAMETER price-decimal        AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER transdate            AS DATE      NO-UNDO.
DEFINE INPUT PARAMETER foreign-rate         AS LOGICAL   NO-UNDO. 
DEFINE INPUT PARAMETER deptname             AS CHAR      NO-UNDO.
DEFINE INPUT PARAMETER cancel-order         AS LOGICAL   NO-UNDO.
DEFINE INPUT PARAMETER order-taker          AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER curr-waiter          AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER gname                AS CHAR      NO-UNDO.
DEFINE INPUT PARAMETER pax                  AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER kreditlimit          AS DECIMAL   NO-UNDO. 
DEFINE INPUT PARAMETER change-str           AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER cc-comment           AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER hoga-card            AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER print-to-kitchen     AS LOGICAL   NO-UNDO.
DEFINE INPUT PARAMETER from-acct            AS LOGICAL   NO-UNDO.
DEFINE INPUT PARAMETER pay-type             AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER guestnr              AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER transfer-zinr        AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER curedept-flag        AS LOGICAL   NO-UNDO.
DEFINE INPUT PARAMETER curr-room            AS CHAR      NO-UNDO. 
DEFINE INPUT PARAMETER user-init            AS CHARACTER NO-UNDO. 
DEFINE INPUT PARAMETER hoga-resnr           AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER hoga-reslinnr        AS INTEGER   NO-UNDO. 
DEFINE INPUT PARAMETER incl-vat             AS LOGICAL   NO-UNDO.
DEFINE INPUT PARAMETER get-price            AS INTEGER   NO-UNDO.   
DEFINE INPUT PARAMETER mc-str               AS CHAR      NO-UNDO.  
DEFINE INPUT PARAMETER segment-code         AS INTEGER   NO-UNDO. /*FDL April 15, 2024 => Ticket 65C56B | CD4BDA*/
DEFINE INPUT PARAMETER TABLE FOR tp-bediener.
DEFINE INPUT PARAMETER TABLE FOR submenu-list.
DEFINE INPUT-OUTPUT PARAMETER cancel-flag   AS LOGICAL   NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR menu-list. 
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-h-bill.

DEFINE OUTPUT PARAMETER avail-bill              AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER not-access              AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER not-access1             AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER bill-date               AS DATE.
DEFINE OUTPUT PARAMETER mwst                    LIKE h-bill-line.betrag INIT 0.
DEFINE OUTPUT PARAMETER mwst-foreign            LIKE h-bill-line.betrag INIT 0.
DEFINE OUTPUT PARAMETER rechnr                  AS INT.
DEFINE OUTPUT PARAMETER balance                 AS DECIMAL.
DEFINE OUTPUT PARAMETER bcol                    AS INT.
DEFINE OUTPUT PARAMETER balance-foreign         AS DECIMAL.
DEFINE OUTPUT PARAMETER fl-code                 AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER fl-code1                AS INT INIT 0.
DEFINE OUTPUT PARAMETER fl-code2                AS INTEGER NO-UNDO.  
DEFINE OUTPUT PARAMETER fl-code3                AS INT INIT 0.
DEFINE OUTPUT PARAMETER fl-code4                AS INT INIT 0.
DEFINE OUTPUT PARAMETER fl-code5                AS INT INIT 0.
DEFINE OUTPUT PARAMETER p-88                    AS LOGICAL.
DEFINE OUTPUT PARAMETER closed                  AS LOGICAL.
DEFINE OUTPUT PARAMETER amount                  AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR kellner1.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-artikel.  

DEFINE VARIABLE menurecid           AS INTEGER NO-UNDO. 
DEFINE VARIABLE add-zeit            AS INTEGER NO-UNDO INITIAL 0. 
DEFINE VARIABLE billart             AS INTEGER NO-UNDO. 
DEFINE VARIABLE req-str             AS CHAR    NO-UNDO INITIAL "". 
DEFINE VARIABLE voucher-str         AS CHAR    NO-UNDO INITIAL "".
DEFINE VARIABLE request-str         AS CHAR    NO-UNDO. 
DEFINE VARIABLE perm                AS INTEGER EXTENT 120 FORMAT "9". /* Malik 4CD2E2 */ 
DEFINE VARIABLE zugriff             AS LOGICAL INITIAL YES NO-UNDO.
DEFINE VARIABLE loopn               AS INTEGER NO-UNDO.
DEFINE VARIABLE description     AS CHAR    NO-UNDO.  
DEFINE VARIABLE qty             AS INTEGER NO-UNDO.  
DEFINE VARIABLE price           AS DECIMAL NO-UNDO.  
DEFINE VARIABLE cancel-str      AS CHAR    NO-UNDO.  
DEFINE VARIABLE amount-foreign  AS DECIMAL NO-UNDO. 
DEFINE VARIABLE curr-zeit       AS INTEGER.
DEFINE VARIABLE krecid          AS INTEGER       INITIAL 0. 
/*
MESSAGE 
    "case-type        = " case-type         SKIP     
    "pvILanguage      = " pvILanguage       SKIP
    "tischnr          = " tischnr           SKIP
    "curr-dept        = " curr-dept         SKIP
    "cancel-reason    = " cancel-reason     SKIP
    "double-currency  = " double-currency   SKIP
    "exchg-rate       = " exchg-rate        SKIP
    "price-decimal    = " price-decimal     SKIP
    "transdate        = " transdate         SKIP
    "foreign-rate     = " foreign-rate      SKIP
    "deptname         = " deptname          SKIP
    "cancel-order     = " cancel-order      SKIP
    "order-taker      = " order-taker       SKIP
    "curr-waiter      = " curr-waiter       SKIP
    "gname            = " gname             SKIP
    "pax              = " pax               SKIP
    "kreditlimit      = " kreditlimit       SKIP
    "change-str       = " change-str        SKIP
    "cc-comment       = " cc-comment        SKIP
    "hoga-card        = " hoga-card         SKIP
    "print-to-kitchen = " print-to-kitchen  SKIP
    "from-acct        = " from-acct         SKIP
    "pay-type         = " pay-type          SKIP
    "guestnr          = " guestnr           SKIP
    "transfer-zinr    = " transfer-zinr     SKIP
    "curedept-flag    = " curedept-flag     SKIP
    "curr-room        = " curr-room         SKIP
    "user-init        = " user-init         SKIP
    "hoga-resnr       = " hoga-resnr        SKIP
    "hoga-reslinnr    = " hoga-reslinnr     SKIP
    "incl-vat         = " incl-vat          SKIP
    "get-price        = " get-price         SKIP
    "mc-str           = " mc-str          
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
FOR EACH t-menu-list:
    DELETE t-menu-list.
END.

FOR EACH bmenu:
    DELETE bmenu.
END.

IF cancel-reason EQ ? THEN
DO:
    cancel-reason = "".
END.
IF change-str EQ ? THEN
DO:
    change-str = "".
END.
IF cc-comment EQ ? THEN
DO:
    cc-comment = "".
END.
IF hoga-card EQ ? THEN
DO:
    hoga-card = "".
END.
IF transfer-zinr EQ ? THEN
DO:
    transfer-zinr = "".
END.
IF curr-room EQ ? THEN
DO:
    curr-room = "".
END.
IF mc-str EQ ? THEN
DO:
    mc-str = "".
END.

IF gname EQ ? THEN
DO:
    gname = "".
END.

FOR EACH menu-list WHERE menu-list.nr GT 0 BY menu-list.nr: 
    CREATE t-menu-list.
    BUFFER-COPY menu-list TO t-menu-list.

    CREATE bmenu.
    BUFFER-COPY menu-list TO bmenu.
    ASSIGN bmenu.rec-menu = RECID(menu-list).
END.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN DO:
    CREATE tp-bediener1.
    BUFFER-COPY bediener TO tp-bediener1.
END.

FOR EACH menu-list WHERE menu-list.nr GT 0 NO-LOCK BY menu-list.nr:

    curr-zeit = TIME.
    ASSIGN
        add-zeit    = add-zeit + 1
        menurecid   = RECID(menu-list) 
        billart     = menu-list.artnr
        req-str     = menu-list.REQUEST 
        /*voucher-str = menu-list.voucher*/
        request-str = menu-list.REQUEST .

    /*FD March 17, 2022 => For Artikel Misc Get Unit Price*/
    IF NUM-ENTRIES(menu-list.voucher,";") GT 1 THEN
    DO:
        voucher-str = ENTRY(1,menu-list.voucher,";").
        incl-vat    = LOGICAL(ENTRY(2,menu-list.voucher,";")).
    END.    

    RUN ts-restinv-run-help3bl.p (menu-list.artnr, menu-list.bezeich, menu-list.anzahl,
        menu-list.price, curr-dept, cancel-reason, double-currency,
        exchg-rate, price-decimal, transdate, cancel-flag,
        foreign-rate, OUTPUT description, OUTPUT qty,
        OUTPUT price, OUTPUT cancel-str, OUTPUT amount-foreign,
        OUTPUT amount, OUTPUT fl-code, OUTPUT fl-code1,
        OUTPUT TABLE t-h-artikel).

    /*IF fl-code = 1 THEN RETURN.*/ /*Comment FDL Ticket CD13E9*/
    IF fl-code1 = 1 THEN DO:
        FIND FIRST tp-bediener1 NO-ERROR.
        DO loopn = 1 TO LENGTH(tp-bediener1.permissions):   
            perm[loopn] = INTEGER(SUBSTR(tp-bediener1.permissions, loopn, 1)).   
        END.   
        IF perm[52] LT 2 THEN ASSIGN zugriff = NO.     

        IF zugriff = NO THEN DO:
            ASSIGN not-access = YES.
            RETURN.
        END.
    END.
   
    FIND FIRST t-h-artikel.
    krecid = menu-list.krecid. 
    DELETE menu-list.
    IF price NE 0 AND amount = 0 THEN .
    ELSE
    DO:        
        RUN update-bill(t-h-artikel.artart, t-h-artikel.artnrfront).         
        FIND FIRST bmenu WHERE bmenu.rec-menu = menurecid NO-ERROR.
        IF AVAILABLE bmenu THEN DO:
            DELETE bmenu.
        END.
    END.
    add-zeit = 0.
    menurecid = 0.    
END.


PROCEDURE update-bill: 
    DEFINE INPUT PARAMETER h-artart AS INTEGER. 
    DEFINE INPUT PARAMETER h-artnrfront AS INTEGER. 
    DEFINE VARIABLE do-itprint  AS LOGICAL NO-UNDO.
    DEFINE VARIABLE by-txtprint AS LOGICAL NO-UNDO.

    DEFINE VARIABLE closed   AS LOGICAL.
    DEFINE VARIABLE rec-id   AS INT.
  
    
    IF h-artart = 0 THEN DO:
        FIND FIRST tp-bediener1 NO-ERROR.
        DO loopn = 1 TO LENGTH(tp-bediener1.permissions):   
            perm[loopn] = INTEGER(SUBSTR(tp-bediener1.permissions, loopn, 1)).   
        END.   
        IF perm[19] LT 2 THEN ASSIGN zugriff = NO.  

        IF zugriff = NO THEN DO:
            ASSIGN not-access1 = YES.
            RETURN.
        END.
    END.
    ELSE DO:
        FIND FIRST tp-bediener1 NO-ERROR.
        DO loopn = 1 TO LENGTH(tp-bediener1.permissions):   
            perm[loopn] = INTEGER(SUBSTR(tp-bediener1.permissions, loopn, 1)).   
        END.   
        IF perm[20] LT 2 THEN ASSIGN zugriff = NO.     

        IF zugriff = NO THEN DO:
            ASSIGN not-access1 = YES.
            RETURN.
        END.
    END.
        
  
    IF zugriff THEN 
    DO:
        FOR EACH submenu-list:
            CREATE t-submenu-list.
            BUFFER-COPY submenu-list TO t-submenu-list.
        END.
       

        FIND FIRST t-h-bill NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-h-bill THEN rec-id = 0.
        ELSE rec-id = t-h-bill.rec-id.
                   
        
        DEF VAR rec-id-artikel AS INT.
        DEF VAR service-code   AS INT.
        IF NOT AVAILABLE t-h-artikel THEN
        DO:
            rec-id-artikel = 0.
            service-code = 0.
        END.
        ELSE
        DO:
            rec-id-artikel = t-h-artikel.rec-id.
            service-code = t-h-artikel.service-code.
        END.                                  

        RUN ts-restinv-update-bill-cldbl.p (pvILanguage, rec-id, rec-id-artikel, deptname, transdate,
            h-artart, cancel-order, service-code, amount,
            amount-foreign, price, double-currency, qty, exchg-rate, price-decimal, order-taker,
            tischnr, curr-dept, curr-waiter, gname, pax, kreditlimit,
            add-zeit, billart, description, change-str, cc-comment,
            cancel-str, req-str, voucher-str, hoga-card, print-to-kitchen,
            from-acct, h-artnrfront, pay-type, guestnr, transfer-zinr,
            curedept-flag, foreign-rate, curr-room, user-init,
            hoga-resnr, hoga-reslinnr, incl-vat, get-price, mc-str, segment-code,
            INPUT TABLE t-submenu-list, OUTPUT bill-date,
            OUTPUT cancel-flag, OUTPUT fl-code2, OUTPUT mwst,
            OUTPUT mwst-foreign, OUTPUT rechnr, OUTPUT balance,
            OUTPUT bcol, OUTPUT balance-foreign, OUTPUT fl-code3,
            OUTPUT fl-code4, OUTPUT fl-code5, OUTPUT p-88, OUTPUT closed,
            OUTPUT TABLE t-h-bill, OUTPUT TABLE kellner1).
        
        IF fl-code2 = 1 THEN RETURN.
        
        IF case-type = 1 THEN DO:
            IF fl-code2 = 2 THEN DO:
                ASSIGN avail-bill = YES.
                RETURN.
            END.    
        END.        
    END. 
END. 
