
DEFINE TEMP-TABLE fbflash-list
    FIELD flag                  AS INTEGER
    FIELD trans-to-storage      AS CHARACTER    FORMAT "x(24)"
    FIELD cost-alloc            AS CHARACTER    FORMAT "x(34)" 
    FIELD day-cons              AS CHARACTER    FORMAT "x(17)"
    FIELD mtd-cons              AS CHARACTER    FORMAT "x(17)"
    .

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER from-grp     AS INTEGER.
DEFINE INPUT PARAMETER food         AS INTEGER.
DEFINE INPUT PARAMETER bev          AS INTEGER.
DEFINE INPUT PARAMETER date1        AS DATE.
DEFINE INPUT PARAMETER date2        AS DATE.
DEFINE INPUT PARAMETER incl-initoh  AS LOGICAL.
DEFINE INPUT PARAMETER incl-streq   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE       FOR fbflash-list.
DEFINE OUTPUT PARAMETER done        AS LOGICAL  INITIAL NO.

DEFINE VARIABLE beg-oh          AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE betrag          AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-betrag1       AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-betrag2       AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE d-betrag        AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE m-betrag        AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE d1-betrag       AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE m1-betrag       AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE flag            AS INTEGER NO-UNDO. 
 
DEFINE VARIABLE f-eknr          AS INTEGER NO-UNDO. 
DEFINE VARIABLE b-eknr          AS INTEGER NO-UNDO. 
DEFINE VARIABLE fl-eknr         AS INTEGER NO-UNDO. 
DEFINE VARIABLE bl-eknr         AS INTEGER NO-UNDO. 

DEFINE VARIABLE main-storage    AS INTEGER NO-UNDO INITIAL 1 . 
DEFINE VARIABLE bev-food        AS CHARACTER NO-UNDO. 
DEFINE VARIABLE food-bev        AS CHARACTER NO-UNDO. 

DEFINE VARIABLE ldry            AS INTEGER NO-UNDO. 
DEFINE VARIABLE dstore          AS INTEGER NO-UNDO.

DEFINE VARIABLE foreign-nr      AS INTEGER NO-UNDO INITIAL 0 . 
DEFINE VARIABLE exchg-rate      AS DECIMAL NO-UNDO INITIAL 1 . 
DEFINE VARIABLE double-currency AS LOGICAL NO-UNDO INITIAL NO . 

DEFINE VARIABLE f-sales         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE b-sales         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tf-sales        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tb-sales        AS DECIMAL NO-UNDO. 
  
DEFINE VARIABLE anf-store       AS INTEGER NO-UNDO INITIAL 1.
DEFINE VARIABLE long-digit      AS LOGICAL NO-UNDO.

DEFINE VARIABLE coa-format      AS CHARACTER NO-UNDO.

DEFINE WORKFILE s-list 
    FIELD reihenfolge AS INTEGER INITIAL 1 /* 1 = food, 2 = beverage */ 
    FIELD lager-nr    AS INTEGER 
    FIELD fibukonto   LIKE gl-acct.fibukonto 
    FIELD bezeich     LIKE gl-acct.bezeich 
    FIELD flag        AS INTEGER INITIAL 2  /* 0 cost, 5 = expense */ 
    FIELD betrag      AS DECIMAL INITIAL 0 
    FIELD t-betrag    AS DECIMAL INITIAL 0
    FIELD betrag1     AS DECIMAL INITIAL 0
    FIELD t-betrag1   AS DECIMAL INITIAL 0
.  

{ SupertransBL.i } 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "fb-flash". 


/*****************************************************************************/

IF incl-initoh THEN anf-store = 2.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
ldry = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
dstore = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
IF htparam.flogical THEN 
DO: 
  double-currency = YES. 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    foreign-nr = waehrung.waehrungsnr. 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE exchg-rate = 1. 
END. 
 
/* sales */ 
FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

/* cost, see paramgroup 21 */ 
FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
fl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK.
coa-format = htparam.fchar.

IF incl-streq EQ FALSE THEN  /*willi*/
DO:
    IF from-grp = food THEN 
    DO: 
        RUN step-food1(fl-eknr, bl-eknr). 
        RUN step-food2(fl-eknr, bl-eknr). 
        RUN beverage-to-food. 
        RUN food-to-beverage. 
        RUN step-two(f-eknr, b-eknr). 
        RUN step-three-food(fl-eknr, bl-eknr). 
        RUN food-bev(fl-eknr, bl-eknr). 
        RUN step-four(f-eknr, b-eknr).
    END. 
    
    ELSE IF from-grp = bev THEN 
    DO: 
        RUN step-bev1(fl-eknr, bl-eknr). 
        RUN step-bev2(fl-eknr, bl-eknr). 
        RUN beverage-to-food. 
        RUN food-to-beverage. 
        RUN step-two(f-eknr, b-eknr). 
        RUN step-three-bev(fl-eknr, bl-eknr). 
        RUN food-bev(fl-eknr, bl-eknr). 
        RUN step-four(f-eknr, b-eknr). 
    END. 
    END.
ELSE
    DO:
    IF from-grp = food THEN 
    DO: 
        RUN step-food1(fl-eknr, bl-eknr). 
        RUN step-food2(fl-eknr, bl-eknr). 
        RUN beverage-to-food. 
        RUN food-to-beverage. 
        RUN step-two(f-eknr, b-eknr). 
        RUN step-three-food(fl-eknr, bl-eknr). 
        RUN food-bev(fl-eknr, bl-eknr). 
        RUN step-four(f-eknr, b-eknr).
        RUN step-five(fl-eknr, bl-eknr).
    END. 
    
    ELSE IF from-grp = bev THEN 
    DO: 
        RUN step-bev1(fl-eknr, bl-eknr). 
        RUN step-bev2(fl-eknr, bl-eknr). 
        RUN beverage-to-food. 
        RUN food-to-beverage. 
        RUN step-two(f-eknr, b-eknr). 
        RUN step-three-bev(fl-eknr, bl-eknr). 
        RUN food-bev(fl-eknr, bl-eknr). 
        RUN step-four(f-eknr, b-eknr). 
        RUN step-five(fl-eknr, bl-eknr).
    END. 
END.



IF from-grp = food OR from-grp = 0 THEN 
DO: 
    ASSIGN  d-betrag  = 0
            m-betrag  = 0 
            d1-betrag = 0 
            m1-betrag = 0. 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    ASSIGN fbflash-list.cost-alloc = translateExtended ("** FOOD **",lvCAREA,""). 
    CREATE fbflash-list. 

    t-betrag1 = 0. 
    beg-oh = 0. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("OPENING INVENTORY",lvCAREA,""). 
    
    FOR EACH l-lager WHERE l-lager.lager-nr GE anf-store NO-LOCK: 
        betrag = 0. 
        FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.endkum = 1 NO-LOCK: 
            ASSIGN  betrag    = betrag + l-bestand.val-anf-best 
                    t-betrag1 = t-betrag1 + l-bestand.val-anf-best. 

            IF l-lager.lager-nr GT 1 THEN 
            DO: 
                beg-oh = beg-oh + l-bestand.val-anf-best. 
                IF incl-initoh THEN m-betrag = m-betrag + l-bestand.val-anf-best. 
            END. 
        END. 

        IF betrag GT 0 THEN 
        DO: 
            CREATE fbflash-list. 
            IF NOT long-digit THEN 
                ASSIGN  fbflash-list.cost-alloc = l-lager.bezeich
                        fbflash-list.mtd-cons   = STRING(betrag, "->,>>>,>>>,>>9.99").
            ELSE 
                ASSIGN  fbflash-list.cost-alloc = l-lager.bezeich
                        fbflash-list.mtd-cons   = STRING(betrag, "->>>>,>>>,>>>,>>9").
        END. 
    END. 

    IF t-betrag1 GT 0 THEN 
    DO: 
        CREATE fbflash-list.
        fbflash-list.flag = 1.
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("T o t a l",lvCAREA,"")
                    fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99").
        ELSE
        DO:
            fbflash-list.flag = 1.
            ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("T o t a l",lvCAREA,"")
                    fbflash-list.mtd-cons   = STRING(t-betrag1, "->>>>,>>>,>>>,>>9").
        END.
    END. 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("TRANSFER TO SIDE STORE",lvCAREA,"").
    betrag = 0. 
    t-betrag1 = 0. 

    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 1 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d-betrag  = d-betrag + s-list.betrag 
                m-betrag  = m-betrag + s-list.t-betrag. 

        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   "->,>>>,>>>,>>9.99")
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   " ->>>,>>>,>>>,>>9")
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9"). 
    END. 

    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("DIRECT PURCHASED",lvCAREA,""). 
    betrag = 0. 
    t-betrag1 = 0. 

    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 2 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag 
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d-betrag  = d-betrag + s-list.betrag
                m-betrag  = m-betrag + s-list.t-betrag. 

        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9"). 
    END. 

    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
     

    IF incl-streq EQ TRUE THEN /*willi*/
    DO:
    CREATE fbflash-list.
    fbflash-list.trans-to-storage = translateExtended ("STORE REQUISITION",lvCAREA,""). 
    betrag = 0. 
    t-betrag1 = 0. 

    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 6 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag 
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d-betrag  = d-betrag + s-list.betrag
                m-betrag  = m-betrag + s-list.t-betrag. 
       .
        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9").  

    CREATE fbflash-list.
    END.

    fbflash-list.flag = 1.
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list.
    END.
   
    /** beverage TO food **/ 
    FIND FIRST s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 3 NO-LOCK. 
    ASSIGN  d-betrag = d-betrag + s-list.betrag + s-list.betrag1
            m-betrag = m-betrag + s-list.t-betrag + s-list.t-betrag1. 

    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                fbflash-list.day-cons   = STRING((s-list.betrag + s-list.betrag1),     "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING((s-list.t-betrag + s-list.t-betrag1), "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                fbflash-list.day-cons   = STRING((s-list.betrag + s-list.betrag1),     " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING((s-list.t-betrag + s-list.t-betrag1), " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("GROSS CONSUMPTION COST",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d-betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(m-betrag, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("GROSS CONSUMPTION COST",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d-betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(m-betrag, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("LESS BY:",lvCAREA,""). 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("COMPLIMENT COST",lvCAREA,""). 
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 4 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d1-betrag = d1-betrag + s-list.betrag
                m1-betrag = m1-betrag + s-list.t-betrag 
                d-betrag  = d-betrag - s-list.betrag
                m-betrag  = m-betrag - s-list.t-betrag. 

        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                fbflash-list.day-cons   = STRING(s-list.betrag,       " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(s-list.t-betrag,     " ->>>,>>>,>>>,>>9"). 
    END. 

    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag,    " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("DEPARTMENT EXPENSES",lvCAREA,"").
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 5 NO-LOCK 
        BY s-list.bezeich:
        ASSIGN  betrag    = betrag + s-list.betrag 
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d1-betrag = d1-betrag + s-list.betrag
                m1-betrag = m1-betrag + s-list.t-betrag 
                d-betrag  = d-betrag - s-list.betrag
                m-betrag  = m-betrag - s-list.t-betrag. 

        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag,   " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9").         
    END. 

    /** food TO beverage **/ 
    FIND FIRST s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 3 NO-LOCK. 
    ASSIGN  betrag    = betrag    + s-list.betrag    /*+ s-list.betrag1*/ 
            t-betrag1 = t-betrag1 + s-list.t-betrag  /*+ s-list.t-betrag1*/ 
            d1-betrag = d1-betrag + s-list.betrag    /*+ s-list.betrag1*/
            m1-betrag = m1-betrag + s-list.t-betrag  /*+ s-list.t-betrag1*/ 
            d-betrag  = d-betrag  - s-list.betrag    /*- s-list.betrag1*/   
            m-betrag  = m-betrag  - s-list.t-betrag  /*- s-list.t-betrag1*/. 
    IF s-list.t-betrag NE 0 THEN DO:
        CREATE fbflash-list.
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING((s-list.betrag /*+ s-list.betrag1*/), "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING((s-list.t-betrag /*+ s-list.t-betrag1*/), "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING((s-list.betrag /*+ s-list.betrag1*/),     " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING((s-list.t-betrag /*+ s-list.t-betrag1*/), " ->>>,>>>,>>>,>>9"). 

    END. 
        
    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("TOTAL EXPENSES",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d1-betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(m1-betrag, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("TOTAL EXPENSES",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d1-betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(m1-betrag, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("NET CONSUMPTION COST",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d-betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(m-betrag, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("NET CONSUMPTION COST",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d-betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(m-betrag, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.cost-alloc = translateExtended ("Nett Food Sales",lvCAREA,"")
                fbflash-list.day-cons   = STRING(f-sales, "->,>>>,>>>,>>9.99")
                fbflash-list.mtd-cons   = STRING(tf-sales, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.cost-alloc = translateExtended ("Nett Food Sales",lvCAREA,"")
                fbflash-list.day-cons   = STRING(f-sales,  " ->>>,>>>,>>>,>>9")
                fbflash-list.mtd-cons   = STRING(tf-sales, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
    fbflash-list.cost-alloc = translateExtended ("R a t i o  Cost:Sales (%)",lvCAREA,""). 
    IF f-sales NE 0 THEN fbflash-list.day-cons = STRING((d-betrag / f-sales * 100), "->,>>>,>>>,>>9.99"). 
    ELSE fbflash-list.day-cons = STRING(0, "->,>>>,>>>,>>9.99"). 
    IF tf-sales NE 0 THEN fbflash-list.mtd-cons = STRING((m-betrag / tf-sales) * 100, "->,>>>,>>>,>>9.99"). 
    ELSE fbflash-list.mtd-cons = STRING(0, "->,>>>,>>>,>>9.99"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
END. 

done = YES. 
/** beverage ***/ 
IF from-grp = bev THEN 
DO: 
    ASSIGN  d-betrag  = 0 
            m-betrag  = 0 
            d1-betrag = 0 
            m1-betrag = 0. 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.cost-alloc = translateExtended ("** BEVERAGE **",lvCAREA,""). 
    
    CREATE fbflash-list. 
    t-betrag1 = 0. 
    beg-oh = 0. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("OPENING INVENTORY",lvCAREA,""). 
    FOR EACH l-lager WHERE l-lager.lager-nr GE anf-store NO-LOCK: 
        betrag = 0. 
        FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.endkum = 2 NO-LOCK: 
            ASSIGN  betrag      = betrag + l-bestand.val-anf-best
                    t-betrag1   = t-betrag1 + l-bestand.val-anf-best. 

            IF l-lager.lager-nr GT 1 THEN 
            DO: 
                beg-oh = beg-oh + l-bestand.val-anf-best. 
                IF incl-initoh THEN 
                    m-betrag = m-betrag + l-bestand.val-anf-best. 
            END. 
        END. 

        IF betrag GT 0 THEN 
        DO: 
            CREATE fbflash-list. 
            IF NOT long-digit THEN 
                ASSIGN  fbflash-list.cost-alloc = l-lager.bezeich
                        fbflash-list.mtd-cons   = STRING(betrag, "->,>>>,>>>,>>9.99"). 
            ELSE 
                ASSIGN  fbflash-list.cost-alloc = l-lager.bezeich
                        fbflash-list.mtd-cons   = STRING(betrag, " ->>>,>>>,>>>,>>9"). 
        END. 
    END. 

    IF t-betrag1 GT 0 THEN 
    DO: 
        fbflash-list.flag = 1.
        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("T o t a l",lvCAREA,"")
                    fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("T o t a l",lvCAREA,"")
                    fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 
    END. 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("TRANSFER TO SIDE STORE",lvCAREA,""). 
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 1 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d-betrag  = d-betrag + s-list.betrag
                m-betrag   = m-betrag + s-list.t-betrag. 
        
        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9"). 
    END. 

    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("DIRECT PURCHASED",lvCAREA,""). 
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 2 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d-betrag  = d-betrag + s-list.betrag
                m-betrag  = m-betrag + s-list.t-betrag. 

        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9"). 
    END. 

    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    
    
    IF incl-streq EQ TRUE THEN /*willi*/
    DO:
        CREATE fbflash-list.
        fbflash-list.trans-to-storage = translateExtended ("STORE REQUISITION",lvCAREA,""). 
        betrag = 0. 
        t-betrag1 = 0. 

        FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 6 NO-LOCK 
            BY s-list.bezeich: 
            ASSIGN  betrag    = betrag + s-list.betrag 
                    t-betrag1 = t-betrag1 + s-list.t-betrag 
                    d-betrag  = d-betrag + s-list.betrag
                    m-betrag  = m-betrag + s-list.t-betrag. 
           .
            CREATE fbflash-list. 
            IF NOT long-digit THEN 
                ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                        fbflash-list.day-cons   = STRING(s-list.betrag,   "->,>>>,>>>,>>9.99") 
                        fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
            ELSE 
                ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                        fbflash-list.day-cons   = STRING(s-list.betrag,   " ->>>,>>>,>>>,>>9") 
                        fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9"). 
        

        CREATE fbflash-list.
        END. 

        fbflash-list.flag = 1.
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                    fbflash-list.day-cons   = STRING(betrag,    "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                    fbflash-list.day-cons   = STRING(betrag,    " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9").    
    CREATE fbflash-list.
    END.

    /** food TO beverage **/ 
    FIND FIRST s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 3 NO-LOCK. 
    ASSIGN  d-betrag = d-betrag + s-list.betrag + s-list.betrag1 
            m-betrag = m-betrag + s-list.t-betrag + s-list.t-betrag1. 

    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING((s-list.betrag + s-list.betrag1), "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING((s-list.t-betrag + s-list.t-betrag1), "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING((s-list.betrag + s-list.betrag1), " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING((s-list.t-betrag + s-list.t-betrag1), " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("GROSS CONSUMPTION COST",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d-betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(m-betrag, "->,>>>,>>>,>>9.99"). 
    ELSE
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("GROSS CONSUMPTION COST",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d-betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(m-betrag, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("LESS BY:",lvCAREA,""). 

    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("COMPLIMENT COST",lvCAREA,""). 
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 4 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag    = betrag + s-list.betrag
                t-betrag1 = t-betrag1 + s-list.t-betrag 
                d1-betrag = d1-betrag + s-list.betrag
                m1-betrag = m1-betrag + s-list.t-betrag
                d-betrag  = d-betrag - s-list.betrag
                m-betrag  = m-betrag - s-list.t-betrag. 

        
        
        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9"). 
    END. 
    
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 
 
    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.trans-to-storage = translateExtended ("DEPARTMENT EXPENSES",lvCAREA,""). 

    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 5 NO-LOCK 
        BY s-list.bezeich: 
        ASSIGN  betrag      = betrag + s-list.betrag
                t-betrag1   = t-betrag1 + s-list.t-betrag 
                d1-betrag   = d1-betrag + s-list.betrag
                m1-betrag   = m1-betrag + s-list.t-betrag 
                d-betrag    = d-betrag - s-list.betrag
                m-betrag    = m-betrag - s-list.t-betrag. 

        CREATE fbflash-list. 
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING(s-list.betrag, " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING(s-list.t-betrag, " ->>>,>>>,>>>,>>9").         
    END. 
    
    /** beverage TO food **/ 
    FIND FIRST s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 3 NO-LOCK. 
    ASSIGN  betrag    = betrag    + s-list.betrag   + s-list.betrag1 
            t-betrag1 = t-betrag1 + s-list.t-betrag + s-list.t-betrag1 
            d1-betrag = d1-betrag + s-list.betrag   + s-list.betrag1 
            m1-betrag = m1-betrag + s-list.t-betrag + s-list.t-betrag1 
            d-betrag  = d-betrag  - s-list.betrag   - s-list.betrag1 
            m-betrag  = m-betrag  - s-list.t-betrag - s-list.t-betrag1. 
    

    IF s-list.t-betrag NE 0 THEN DO:
        CREATE fbflash-list.
        IF NOT long-digit THEN 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING((s-list.betrag /*+ s-list.betrag1*/), "->,>>>,>>>,>>9.99") 
                    fbflash-list.mtd-cons   = STRING((s-list.t-betrag /*+ s-list.t-betrag1*/), "->,>>>,>>>,>>9.99"). 
        ELSE 
            ASSIGN  fbflash-list.cost-alloc = s-list.bezeich
                    fbflash-list.day-cons   = STRING((s-list.betrag /*+ s-list.betrag1*/), " ->>>,>>>,>>>,>>9") 
                    fbflash-list.mtd-cons   = STRING((s-list.t-betrag /*+ s-list.t-betrag1*/), " ->>>,>>>,>>>,>>9"). 
    END.    

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    fbflash-list.flag = 1.
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("Sub T o t a l",lvCAREA,"")
                fbflash-list.day-cons   = STRING(betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(t-betrag1, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("TOTAL EXPENSES",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d1-betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(m1-betrag, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = translateExtended ("TOTAL EXPENSES",lvCAREA,"")
                fbflash-list.day-cons   = STRING(d1-betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(m1-betrag, " ->>>,>>>,>>>,>>9"). 
        
    CREATE fbflash-list. 
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.trans-to-storage    = STRING(translateExtended ("NET CONSUMPTION COST",lvCAREA,""), "x(24)") 
                fbflash-list.day-cons   = STRING(d-betrag, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(m-betrag, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.trans-to-storage    = STRING(translateExtended ("NET CONSUMPTION COST",lvCAREA,""), "x(24)") 
                fbflash-list.day-cons   = STRING(d-betrag, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(m-betrag, " ->>>,>>>,>>>,>>9"). 

    CREATE fbflash-list. 
    CREATE fbflash-list. 
    IF NOT long-digit THEN 
        ASSIGN  fbflash-list.cost-alloc = translateExtended ("Nett Beverage Sales",lvCAREA,"")
                fbflash-list.day-cons   = STRING(b-sales, "->,>>>,>>>,>>9.99") 
                fbflash-list.mtd-cons   = STRING(tb-sales, "->,>>>,>>>,>>9.99"). 
    ELSE 
        ASSIGN  fbflash-list.cost-alloc = translateExtended ("Nett Beverage Sales",lvCAREA,"")
                fbflash-list.day-cons   = STRING(b-sales, " ->>>,>>>,>>>,>>9") 
                fbflash-list.mtd-cons   = STRING(tb-sales, " ->>>,>>>,>>>,>>9"). 
    
    CREATE fbflash-list. 
    /*ITA 181213 fbflash-list.trans-to-storage = translateExtended ("R a t i o  Cost:Sales (%)",lvCAREA,""). */
    fbflash-list.cost-alloc = translateExtended ("R a t i o  Cost:Sales (%)",lvCAREA,""). 
    
    IF b-sales NE 0 THEN 
        fbflash-list.day-cons = STRING((d-betrag / b-sales * 100), "->,>>>,>>>,>>9.99"). 
    ELSE fbflash-list.day-cons = STRING(0, "->,>>>,>>>,>>9.99"). 

    IF tb-sales NE 0 THEN fbflash-list.mtd-cons = STRING((m-betrag / tb-sales) * 100, "->,>>>,>>>,>>9.99"). 
    ELSE fbflash-list.mtd-cons = STRING(0, "->,>>>,>>>,>>9.99"). 
    
END. 
done = YES. 
    
/*****************************************************************************/

/*** FOOD Cost BY calculating incoming due-to transfer TO storages ***/ 
PROCEDURE step-food1: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag    AS INTEGER NO-UNDO INITIAL 1. 
    DEFINE BUFFER l-store   FOR l-lager. 
 
    /** Transfer from (side-) store (l-op.lager-nr) TO other 
        (side-) store (l-op.pos) **/ 
    FOR EACH l-op WHERE l-op.op-art = 4 
        AND l-op.loeschflag LE 1 AND l-op.herkunftflag = 1 
        AND l-op.datum GE date1 
        AND l-op.datum LE date2 NO-LOCK, 
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = fl-eknr NO-LOCK: 
 
        /** deduct onhand IF NOT transferred from main store **/ 
        IF l-op.lager-nr NE main-storage THEN 
        DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = l-op.lager-nr 
                AND s-list.reihenfolge = 1 AND s-list.flag = flag NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
                CREATE s-list. 
                ASSIGN  s-list.reihenfolge  = 1
                        s-list.lager-nr     = l-lager.lager-nr
                        s-list.bezeich      = l-lager.bezeich 
                        s-list.flag         = flag. 
            END. 
            s-list.t-betrag = s-list.t-betrag - l-op.warenwert. 
            IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag - l-op.warenwert. 
        END. 
 
        /** add onhand IF target store is a side-store) */ 
        IF l-op.pos NE main-storage THEN 
        DO: 
            FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK. 
            FIND FIRST s-list WHERE s-list.lager-nr = l-op.pos 
                AND s-list.reihenfolge = 1 AND s-list.flag = flag NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
                CREATE s-list. 
                ASSIGN  s-list.reihenfolge  = 1
                        s-list.lager-nr     = l-store.lager-nr
                        s-list.bezeich      = l-store.bezeich
                        s-list.flag         = flag. 
            END. 
            s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
            IF l-op.datum = date2 THEN 
                s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
    END. 
END. 
 
/*** BEVERAGE Cost BY calculating incoming due-to transfer TO storages ***/ 
PROCEDURE step-bev1: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag    AS INTEGER NO-UNDO INITIAL 2. 
    DEFINE BUFFER l-store   FOR l-lager. 

    /** Transfer from (side-) store (l-op.lager-nr) TO other 
        (side-) store (l-op.pos) **/ 
    FOR EACH l-op WHERE l-op.op-art = 4 AND l-op.loeschflag LE 1 
        AND l-op.herkunftflag = 1 AND l-op.datum GE date1 
        AND l-op.datum LE date2 NO-LOCK, 
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = bl-eknr NO-LOCK: 

        /** deduct only IF interkitchen transfrer (NOT transferred from main store) */ 
        IF l-op.lager-nr NE main-storage THEN 
        DO: 
            FIND FIRST s-list WHERE s-list.lager-nr = l-op.lager-nr 
                AND s-list.reihenfolge = 1 AND s-list.flag = flag NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
                CREATE s-list. 
                ASSIGN  s-list.reihenfolge  = 1
                        s-list.lager-nr     = l-lager.lager-nr
                        s-list.bezeich      = l-lager.bezeich
                        s-list.flag         = flag. 
            END. 
            s-list.t-betrag = s-list.t-betrag - l-op.warenwert. 
            IF l-op.datum = date2 THEN 
                s-list.betrag = s-list.betrag - l-op.warenwert. 
        END. 

        /** add stock IF target store NOT the main store) */ 
        IF l-op.pos NE main-storage THEN 
        DO: 
            FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK. 
            FIND FIRST s-list WHERE s-list.lager-nr = l-op.pos 
                AND s-list.reihenfolge = 1 AND s-list.flag = flag NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
                CREATE s-list. 
                ASSIGN  s-list.reihenfolge  = 1
                        s-list.lager-nr     = l-store.lager-nr 
                        s-list.bezeich      = l-store.bezeich
                        s-list.flag         = flag.
            END. 
            s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
            IF l-op.datum = date2 THEN 
                s-list.betrag = s-list.betrag + l-op.warenwert. 
        END. 
    END. 
END. 
 
/*** FOOD Cost BY incoming due-to direct puchasing TO outlet stores ***/ 
PROCEDURE step-food2: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag    AS INTEGER NO-UNDO INITIAL 1. 

    FOR EACH l-op WHERE l-op.op-art = 1 AND l-op.pos GT 0 
        AND l-op.loeschflag LE 1 AND l-op.lager-nr NE main-storage
        AND l-op.datum GE date1 AND l-op.datum LE date2 NO-LOCK, 
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = fl-eknr NO-LOCK: 
        FIND FIRST s-list WHERE s-list.lager-nr = l-op.lager-nr 
            AND s-list.reihenfolge = 2 AND s-list.flag = flag NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
            CREATE s-list. 
            ASSIGN  s-list.reihenfolge  = 2
                    s-list.lager-nr     = l-lager.lager-nr
                    s-list.bezeich      = l-lager.bezeich
                    s-list.flag         = flag. 
        END. 
        s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
        IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert.
        
        
    END. 
END. 
 
/*** BEVERAGE Cost BY incoming due-to direct puchasing TO outlet stores ***/ 
PROCEDURE step-bev2: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag    AS INTEGER NO-UNDO INITIAL 2. 

    FOR EACH l-op WHERE l-op.op-art = 1 AND l-op.pos GT 0 
        AND l-op.loeschflag LE 1 AND l-op.lager-nr NE main-storage
        AND l-op.datum GE date1 AND l-op.datum LE date2 NO-LOCK, 
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = bl-eknr NO-LOCK: 
        FIND FIRST s-list WHERE s-list.lager-nr = l-op.lager-nr 
            AND s-list.reihenfolge = 2 AND s-list.flag = flag NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
            CREATE s-list. 
            ASSIGN  s-list.reihenfolge  = 2
                    s-list.lager-nr     = l-lager.lager-nr
                    s-list.bezeich      = l-lager.bezeich
                    s-list.flag         = flag.
        END. 
        s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
        IF l-op.datum = date2 THEN 
            s-list.betrag = s-list.betrag + l-op.warenwert. 
    END. 
END. 
 
PROCEDURE beverage-to-food: 
    FIND FIRST htparam WHERE paramnr = 272 NO-LOCK NO-ERROR. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR. 
    bev-food = htparam.fchar. 
    CREATE s-list. 
    ASSIGN  s-list.reihenfolge  = 3
            s-list.bezeich      = STRING(gl-acct.fibukonto, coa-format) + " " 
                                + CAPS(gl-acct.bezeich)
            s-list.flag         = 1. 
END. 
 
PROCEDURE food-to-beverage: 
    FIND FIRST htparam WHERE paramnr = 275 NO-LOCK NO-ERROR. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR. 
    food-bev = htparam.fchar. 
    CREATE s-list. 
    ASSIGN  s-list.reihenfolge  = 3
            s-list.bezeich      = STRING(gl-acct.fibukonto, coa-format) + " " 
                                + CAPS(gl-acct.bezeich)
            s-list.flag         = 2. 
END. 
 
/*** Less BY FB Compliment ***/ 
PROCEDURE step-two: 
    DEFINE INPUT PARAMETER f-endkum AS INTEGER. 
    DEFINE INPUT PARAMETER b-endkum AS INTEGER. 
    DEFINE BUFFER h-art     FOR h-artikel. 
    DEFINE BUFFER gl-acc1   FOR gl-acct. 
    DEFINE VARIABLE flag            AS INTEGER      NO-UNDO. 
    DEFINE VARIABLE cost-account    AS CHARACTER    NO-UNDO. 
    DEFINE VARIABLE cost-value      AS DECIMAL      NO-UNDO. 
    DEFINE VARIABLE rate            AS DECIMAL      NO-UNDO INITIAL 1. 
    DEFINE VARIABLE curr-datum      AS DATE         NO-UNDO INITIAL ?. 
    DEFINE VARIABLE cost            AS DECIMAL      NO-UNDO.  
    DEFINE VARIABLE com-artnr       AS INTEGER      NO-UNDO. 
    DEFINE VARIABLE com-bezeich     AS CHARACTER    NO-UNDO. 
    DEFINE VARIABLE com-fibu        AS CHARACTER    NO-UNDO. 

    FOR EACH h-compli WHERE h-compli.datum GE date1 
        AND h-compli.datum LE date2 AND h-compli.departement NE ldry 
        AND h-compli.departement NE dstore AND h-compli.betriebsnr = 0 NO-LOCK, 
        FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        BY h-compli.datum BY h-compli.rechnr: 

        IF double-currency AND curr-datum NE h-compli.datum THEN 
        DO: 
            curr-datum = h-compli.datum. 
            IF foreign-nr NE 0 THEN 
                FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
                AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
            ELSE 
                FIND FIRST exrate WHERE exrate.datum = curr-datum 
                    NO-LOCK NO-ERROR. 
                IF AVAILABLE exrate THEN rate = exrate.betrag. 
                ELSE rate = exchg-rate. 
        END. 
 
        FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
            AND artikel.departement = 0 NO-LOCK. 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK. 
        ASSIGN  com-artnr   = artikel.artnr
                com-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                            + CAPS(gl-acct.bezeich)
                com-fibu    = gl-acct.fibukonto. 

        FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
            AND h-artikel.departement = h-compli.departement NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
            AND artikel.departement = h-artikel.departement NO-LOCK. 
        flag = 0. 
        /*ITA 201213 IF artikel.endkum = f-endkum THEN flag = 1. 
        ELSE IF artikel.endkum = b-endkum THEN flag = 2. */
        
        IF artikel.endkum = f-endkum OR artikel.umsatzart = 3
        OR artikel.umsatzart = 5 THEN flag = 1. 
        ELSE IF artikel.endkum = b-endkum OR artikel.umsatzart = 6
        THEN flag = 2. 

        FIND FIRST s-list WHERE s-list.fibukonto = com-fibu 
            AND s-list.reihenfolge = 4 AND s-list.flag = flag NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
            CREATE s-list. 
            ASSIGN  s-list.reihenfolge  = 4
                    s-list.lager-nr     = com-artnr
                    s-list.fibukonto    = com-fibu
                    s-list.bezeich      = com-bezeich
                    s-list.flag         = flag. 
        END. 

        cost = 0. 
        FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
            AND h-cost.departement = h-compli.departement 
            AND h-cost.datum = h-compli.datum 
            AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
            cost = h-compli.anzahl * h-cost.betrag. 
        ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
            cost = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
         
        s-list.t-betrag = s-list.t-betrag + cost. 
        IF h-compli.datum = date2 THEN s-list.betrag = s-list.betrag + cost. 
    END. 
END. 
 
/* Less BY FOOD Requisition FOR Department Expenses */ 
PROCEDURE step-three-food: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag        AS INTEGER  NO-UNDO INITIAL 1. 
    DEFINE VARIABLE fibukonto   LIKE gl-acct.fibukonto. 
    DEFINE VARIABLE bezeich     AS CHARACTER NO-UNDO. 
    DEFINE BUFFER gl-acct1      FOR gl-acct. 
    DEFINE VARIABLE type-of-acct AS INTEGER.

    FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 AND l-op.datum GE date1 AND l-op.datum LE date2 
        /*ITA 201213 AND l-op.lager-nr GT 1 NO-LOCK,*/
        AND l-op.lager-nr NE main-storage NO-LOCK,
        FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
        /*ITA 201213 FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, */
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
        AND (gl-acct.acc-type = 5 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 4) NO-LOCK,
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = fl-eknr NO-LOCK: 

        ASSIGN  fibukonto    = gl-acct.fibukonto
                bezeich      = STRING(gl-acct.fibukonto, coa-format) + " " 
                               + CAPS(gl-acct.bezeich)
                type-of-acct = gl-acct.acc-type. 

        IF l-op.stornogrund NE "" THEN 
        DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
                NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN 
            ASSIGN  
                type-of-acct = gl-acct1.acc-type
                fibukonto    = gl-acct1.fibukonto
                bezeich      = STRING(gl-acct1.fibukonto, coa-format) + " " 
                               + CAPS(gl-acct1.bezeich). 
        END. 

        IF fibukonto = food-bev THEN. 
        ELSE IF fibukonto = bev-food THEN. 
        ELSE 
        DO: 
            IF type-of-acct = 3 OR type-of-acct = 4 OR type-of-acct = 5 THEN DO:
                FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                    AND s-list.reihenfolge = 5 AND s-list.flag = flag NO-ERROR. 
                IF NOT AVAILABLE s-list THEN 
                DO: 
                    CREATE s-list. 
                    ASSIGN  s-list.reihenfolge  = 5
                            s-list.fibukonto    = fibukonto
                            s-list.bezeich      = bezeich
                            s-list.flag         = flag. 
                END. 
                s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
                IF l-op.datum = date2 THEN 
                    s-list.betrag = s-list.betrag + l-op.warenwert. 
            END.
        END. 
    END. 
END. 
 
/* Less BY BEVERAGE Requisition FOR Department Expenses */ 
PROCEDURE step-three-bev: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag        AS INTEGER NO-UNDO INITIAL 2. 
    DEFINE VARIABLE fibukonto   LIKE gl-acct.fibukonto. 
    DEFINE VARIABLE bezeich     AS CHARACTER NO-UNDO. 
    DEFINE buffer gl-acct1      FOR gl-acct. 
    DEFINE VARIABLE type-of-acct AS INTEGER.
 
    FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.loeschflag LE 1 
        AND l-op.op-art = 3 AND l-op.datum GE date1 AND l-op.datum LE date2 
        /*ITA 201213 AND l-op.lager-nr GT 1 NO-LOCK, */
        AND l-op.lager-nr NE main-storage NO-LOCK, 
        FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
        /*ITA 201213 FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto NO-LOCK, */
        FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
        AND (gl-acct.acc-type = 5 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 4) NO-LOCK, 
        FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum = bl-eknr NO-LOCK: 

        ASSIGN  fibukonto    = gl-acct.fibukonto
                bezeich      = STRING(gl-acct.fibukonto, coa-format) + " " 
                                + CAPS(gl-acct.bezeich)
                type-of-acct = gl-acct.acc-type. 

        IF l-op.stornogrund NE "" THEN 
        DO: 
            FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
                NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct1 THEN 
            ASSIGN 
                fibukonto    = gl-acct1.fibukonto
                bezeich      = STRING(gl-acct1.fibukonto, coa-format) + " " 
                               + CAPS(gl-acct1.bezeich)
                type-of-acct = gl-acct1.acc-type
            . 
        END. 

        IF fibukonto = food-bev THEN. 
        ELSE IF fibukonto = bev-food THEN. 
        ELSE 
        DO:  
            IF type-of-acct = 3 OR type-of-acct = 4 OR type-of-acct = 5 THEN DO:
                FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
                    AND s-list.reihenfolge = 5 AND s-list.flag = flag NO-ERROR. 
                IF NOT AVAILABLE s-list THEN 
                DO: 
                    CREATE s-list. 
                    ASSIGN  s-list.reihenfolge  = 5
                            s-list.fibukonto    = fibukonto
                            s-list.bezeich      = bezeich
                            s-list.flag         = flag. 
                END. 
           
                s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
                IF l-op.datum = date2 THEN 
                    s-list.betrag = s-list.betrag + l-op.warenwert. 
            END.
        END. 
    END. 
END. 
 
/*** food TO beverage - baverage TO food ***/ 
PROCEDURE food-bev: 
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 

    FOR EACH l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
        AND l-op.datum GE date1 AND l-op.datum LE date2 
        AND (l-op.stornogrund = bev-food OR l-op.stornogrund = food-bev) NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
        IF l-op.stornogrund = food-bev THEN 
        DO: 
            FIND FIRST s-list WHERE s-list.reihenfolge = 3 AND s-list.flag = 2. 
            IF l-op.lager-nr /*GT*/ GE 1 THEN
            DO:
                s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
                IF l-op.datum = date2 THEN 
                    s-list.betrag = s-list.betrag + l-op.warenwert. 
            END.
            ELSE
            DO:
                s-list.t-betrag1 = s-list.t-betrag1 + l-op.warenwert. 
                IF l-op.datum = date2 THEN 
                    s-list.betrag1 = s-list.betrag1 + l-op.warenwert. 
            END.
        END. 
        ELSE IF l-op.stornogrund = bev-food THEN 
        DO: 
            FIND FIRST s-list WHERE s-list.reihenfolge = 3 AND s-list.flag = 1. 
            IF l-op.lager-nr /*GT*/ GE 1 THEN
            DO:
                s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
                IF l-op.datum = date2 THEN 
                    s-list.betrag = s-list.betrag + l-op.warenwert. 
            END.
            ELSE
            DO:
                s-list.t-betrag1 = s-list.t-betrag1 + l-op.warenwert. 
                IF l-op.datum = date2 THEN 
                    s-list.betrag1 = s-list.betrag1 + l-op.warenwert. 
            END.
        END. 
    END. 
END. 
 
/**** F&B Sales ****/ 
PROCEDURE step-four: 
    DEFINE INPUT PARAMETER f-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER b-eknr AS INTEGER. 
    DEFINE VARIABLE h-service       AS DECIMAL NO-UNDO. 
    DEFINE VARIABLE h-mwst          AS DECIMAL NO-UNDO. 
    DEFINE VARIABLE amount          AS DECIMAL NO-UNDO. 
    DEFINE VARIABLE serv-taxable    AS LOGICAL NO-UNDO. 

    f-sales = 0. 
    b-sales = 0. 
    tf-sales = 0. 
    tb-sales = 0. 

    FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
    serv-taxable = htparam.flogical. 
    
    FOR EACH hoteldpt WHERE hoteldpt.num NE ldry AND hoteldpt.num NE dstore 
        NO-LOCK BY hoteldpt.num: 
        FOR EACH artikel WHERE artikel.artart = 0 
            AND artikel.departement = hoteldpt.num 
            AND (artikel.endkum = f-eknr OR artikel.endkum = b-eknr 
                 OR artikel.umsatzart = 3 OR artikel.umsatzart = 5 
                 OR artikel.umsatzart = 6) NO-LOCK: 
            FOR EACH umsatz WHERE umsatz.datum GE date1 
                AND umsatz.datum LE date2 
                AND umsatz.departement = artikel.departement 
                AND umsatz.artnr = artikel.artnr NO-LOCK: 
                h-service = 0. 
                h-mwst = 0. 
                
                RUN calc-servvat.p(artikel.departement, artikel.artnr, 
                                   umsatz.datum, artikel.service-code, 
                                   artikel.mwst-code, 
                                   OUTPUT h-service, OUTPUT h-mwst).
                amount = umsatz.betrag / (1 + h-service + h-mwst). 

                IF artikel.endkum = f-eknr OR artikel.umsatzart = 3 
                    OR artikel.umsatzart = 5 THEN 
                DO: 
                    IF umsatz.datum = date2 THEN f-sales = f-sales + amount. 
                    tf-sales = tf-sales + amount. 
                END. 
                ELSE IF artikel.endkum = b-eknr OR artikel.umsatzart = 6 THEN 
                DO: 
                    IF umsatz.datum = date2 THEN b-sales = b-sales + amount. 
                    tb-sales = tb-sales + amount. 
                END. 
            END. 
        END. 
    END. 
END.

/**** Storeq req ****/

PROCEDURE step-five:    /*willi*/
    DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
    DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
    DEFINE VARIABLE flag           AS INTEGER. 
    DEFINE VARIABLE fibukonto   LIKE gl-acct.fibukonto. 
    DEFINE VARIABLE bezeich     AS CHARACTER NO-UNDO. 
    DEFINE BUFFER gl-acct1      FOR gl-acct. 
    DEFINE VARIABLE type-of-acct AS INTEGER.
    DEFINE VARIABLE qty         AS DECIMAL FORMAT "->>,>>>,>>9.999". 
    DEFINE VARIABLE qty1        AS DECIMAL FORMAT "->>,>>>,>>9.999". 
    DEFINE VARIABLE val         AS DECIMAL. 
    DEFINE VARIABLE t-qty       AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0.
    DEFINE VARIABLE t-qty1      AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE t-val       AS DECIMAL INITIAL 0.
    

     ASSIGN
      qty  = 0 
      val  = 0
      qty1 = 0.

IF from-grp = food THEN
DO:
    flag = 1. 
    FOR EACH l-op WHERE l-op.datum GE date1 AND l-op.datum LE date2
/*        AND l-op.reorgflag = 3 */
       AND l-op.op-art GE 13 AND l-op.op-art LE 14 
       AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1
       /*AND l-op.artnr EQ 3316021*/ 
       NO-LOCK USE-INDEX artopart_ix,
       FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr
       AND l-ophdr.op-typ = "REQ"
       AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK, 
       FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto
       AND (gl-acct.acc-type = 5 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 4) NO-LOCK, 
       FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK,
       FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr AND l-artikel.endkum = fl-eknr
       NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

      FIND FIRST s-list WHERE s-list.lager-nr = l-op.lager-nr 
            AND s-list.reihenfolge = 6 AND s-list.flag = flag NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
            CREATE s-list. 
            ASSIGN  s-list.reihenfolge  = 6
                    s-list.lager-nr     = l-lager.lager-nr
                    s-list.bezeich      = l-lager.bezeich
                    s-list.flag         = flag. 
        END. 
        s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
        IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert.
    END.
END.
ELSE IF from-grp = bev THEN
DO:
    flag = 2. 
    FOR EACH l-op WHERE l-op.datum GE date1 AND l-op.datum LE date2
/*        AND l-op.reorgflag = 3 */
       AND l-op.op-art GE 13 AND l-op.op-art LE 14 
       AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1
       /*AND l-op.artnr EQ 3316021*/ 
       NO-LOCK USE-INDEX artopart_ix,
       FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr
       AND l-ophdr.op-typ = "REQ"
       AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK, 
       FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto
       AND (gl-acct.acc-type = 5 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 4) NO-LOCK, 
       FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK,
       FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr AND l-artikel.endkum = bl-eknr
       NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

      FIND FIRST s-list WHERE s-list.lager-nr = l-op.lager-nr 
            AND s-list.reihenfolge = 6 AND s-list.flag = flag NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
            CREATE s-list. 
            ASSIGN  s-list.reihenfolge  = 6
                    s-list.lager-nr     = l-lager.lager-nr
                    s-list.bezeich      = l-lager.bezeich
                    s-list.flag         = flag. 
        END. 
        s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
        IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert.
    END.
END.
    
END.


