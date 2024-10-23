DEFINE WORKFILE s-list 
  FIELD nr AS INTEGER 
  FIELD reihenfolge AS INTEGER INITIAL 1 /* 1 = food, 2 = beverage */ 
  FIELD lager-nr AS INTEGER 
  FIELD fibukonto LIKE gl-acct.fibukonto 
  FIELD bezeich LIKE gl-acct.bezeich 
  FIELD flag AS INTEGER INITIAL 2  /* 0 cost, 5 = expense */ 
  FIELD betrag AS DECIMAL INITIAL 0 
  FIELD t-betrag AS DECIMAL INITIAL 0. 


DEFINE TEMP-TABLE fb-flash
  FIELD flag AS INTEGER
  FIELD bezeich AS CHARACTER
  FIELD c-alloc AS CHARACTER
  FIELD t-consumed AS DECIMAL
  FIELD mtd-consumed AS DECIMAL.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER from-grp       AS INT.
DEF INPUT  PARAMETER food           AS INT.
DEF INPUT  PARAMETER main-storage   AS INT.
DEF INPUT  PARAMETER f-store        AS INT.
DEF INPUT  PARAMETER t-store        AS INT.
DEF INPUT  PARAMETER date1          AS DATE.
DEF INPUT  PARAMETER date2          AS DATE.

DEF INPUT  PARAMETER foreign-nr     AS INT.
DEF INPUT  PARAMETER exchg-rate     AS DECIMAL.
DEF INPUT  PARAMETER double-currency AS LOGICAL.

DEF OUTPUT PARAMETER TABLE FOR fb-flash.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fb-flash1".

DEFINE VARIABLE done AS LOGICAL INITIAL NO. 
DEFINE VARIABLE dstore AS INTEGER.
DEFINE VARIABLE curr-store AS INTEGER.
DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

DEFINE VARIABLE f-sales  AS DECIMAL.
DEFINE VARIABLE b-sales  AS DECIMAL.
DEFINE VARIABLE tf-sales AS DECIMAL. 
DEFINE VARIABLE tb-sales AS DECIMAL. 
DEFINE VARIABLE bev-food AS CHAR. 
DEFINE VARIABLE food-bev AS CHAR. 

DEFINE VARIABLE coa-format AS CHARACTER NO-UNDO.
DEFINE BUFFER l-store FOR l-lager. 

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK.
coa-format = htparam.fchar.

IF from-grp = food THEN RUN create-food.
ELSE RUN create-bev.

PROCEDURE create-food: 
DEFINE VARIABLE betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-betrag1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-betrag2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d1-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m1-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE flag AS INTEGER. 
 
DEFINE VARIABLE f-eknr AS INTEGER. 
DEFINE VARIABLE b-eknr AS INTEGER. 
DEFINE VARIABLE fl-eknr AS INTEGER. 
DEFINE VARIABLE bl-eknr AS INTEGER. 
 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
 
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
  
  CREATE fb-flash.
  CREATE fb-flash.
  fb-flash.c-alloc = "** FOOD **".
  CREATE fb-flash.
 
  FOR EACH l-store WHERE l-store.lager-nr NE main-storage AND 
    l-store.lager-nr GE f-store AND l-store.lager-nr LE t-store 
    AND l-store.betriebsnr GT 0 NO-LOCK BY l-store.lager-nr: 
 
    FOR EACH s-list: 
      delete s-list. 
    END. 
 
    CREATE fb-flash.
    fb-flash.c-alloc = l-store.bezeich.
 
    dstore = l-store.betriebsnr. 
    curr-store = l-store.lager-nr. 
    RUN step-food1(fl-eknr, bl-eknr). 
    IF l-store.betriebsnr GT 0 THEN RUN step-food1a. 
    RUN step-food2(fl-eknr, bl-eknr). 
    RUN beverage-to-food. 
    RUN food-to-beverage. 
    RUN step-two(f-eknr, b-eknr). 
    RUN step-three-food(fl-eknr, bl-eknr). 
    RUN food-bev(fl-eknr, bl-eknr). 
    RUN step-four(f-eknr, b-eknr, l-store.lager-nr). 
 
    d-betrag = 0. 
    m-betrag = 0. 
    d1-betrag = 0. 
    m1-betrag = 0. 
 
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 1 NO-LOCK 
      BY s-list.nr: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d-betrag = d-betrag + s-list.betrag. 
      m-betrag = m-betrag + s-list.t-betrag. 
      CREATE fb-flash.
      ASSIGN
        fb-flash.bezeich = s-list.bezeich
        fb-flash.t-consumed = s-list.betrag
        fb-flash.mtd-consumed = s-list.t-betrag.
    END. 
 
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 2 NO-LOCK 
      BY s-list.bezeich: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d-betrag = d-betrag + s-list.betrag. 
      m-betrag = m-betrag + s-list.t-betrag.            
      CREATE fb-flash.
      ASSIGN
        fb-flash.bezeich = s-list.bezeich
        fb-flash.t-consumed = betrag
        fb-flash.mtd-consumed = t-betrag.
    END. 
 
/** beverage TO food **/ 
    FIND FIRST s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 3 NO-LOCK. 
    d-betrag = d-betrag + s-list.betrag. 
    m-betrag = m-betrag + s-list.t-betrag. 
    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = s-list.bezeich
      fb-flash.t-consumed = betrag
      fb-flash.mtd-consumed = t-betrag.
 
    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "GROSS CONSUMPTION COST"
      fb-flash.t-consumed = d-betrag
      fb-flash.mtd-consumed = m-betrag.
    
    CREATE fb-flash.
    fb-flash.bezeich = "LESS BY:".
    
    CREATE fb-flash.
    fb-flash.bezeich = "COMPLIMENT COST".

    betrag = 0. 
    t-betrag1 = 0. 

    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 4 NO-LOCK 
      BY s-list.bezeich: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d1-betrag = d1-betrag + s-list.betrag. 
      m1-betrag = m1-betrag + s-list.t-betrag. 
      d-betrag = d-betrag - s-list.betrag. 
      m-betrag = m-betrag - s-list.t-betrag. 
      
      CREATE fb-flash.
      ASSIGN
        fb-flash.c-alloc = s-list.bezeich
        fb-flash.t-consumed = s-list.betrag
        fb-flash.mtd-consumed = s-list.t-betrag.
    END. 
     
    CREATE fb-flash.
    ASSIGN
      fb-flash.flag = 1
      fb-flash.c-alloc = "SUB TOTAL"
      fb-flash.t-consumed = betrag
      fb-flash.mtd-consumed = t-betrag1.
    
    CREATE fb-flash.
    fb-flash.bezeich = "DEPARTMENT EXPENSES".
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 5 NO-LOCK 
      BY s-list.bezeich: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d1-betrag = d1-betrag + s-list.betrag. 
      m1-betrag = m1-betrag + s-list.t-betrag. 
      d-betrag = d-betrag - s-list.betrag. 
      m-betrag = m-betrag - s-list.t-betrag. 
       
      CREATE fb-flash.
      ASSIGN
        fb-flash.c-alloc = s-list.bezeich
        fb-flash.t-consumed = betrag
        fb-flash.mtd-consumed = t-betrag.
    END. 
 
/** food TO beverage **/ 
    FIND FIRST s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 3 NO-LOCK. 
    betrag = betrag + s-list.betrag. 
    t-betrag1 = t-betrag1 + s-list.t-betrag. 
    d1-betrag = d1-betrag + s-list.betrag. 
    m1-betrag = m1-betrag + s-list.t-betrag. 
    d-betrag = d-betrag - s-list.betrag. 
    m-betrag = m-betrag - s-list.t-betrag. 
    
    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = s-list.bezeich
      fb-flash.t-consumed = s-list.betrag
      fb-flash.mtd-consumed = s-list.t-betrag.
    
    
    CREATE fb-flash.
    ASSIGN
      fb-flash.flag = 1
      fb-flash.c-alloc = "SUB TOTAL"
      fb-flash.t-consumed = betrag
      fb-flash.mtd-consumed = t-betrag1.

    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "TOTAL EXPENSES"
      fb-flash.t-consumed = d1-betrag
      fb-flash.mtd-consumed = m1-betrag.
 
    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "NET CONSUMPTION COST"
      fb-flash.t-consumed = d-betrag
      fb-flash.mtd-consumed = m-betrag.
    
    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = "Nett Food Sales"
      fb-flash.t-consumed = f-sales
      fb-flash.mtd-consumed = tf-sales.
                                                                                     
    CREATE fb-flash.
    ASSIGN
      fb-flash.flag = 99
      fb-flash.c-alloc = "R a t i o  Cost:Sales (%)".
    
    IF f-sales NE 0 THEN fb-flash.t-consumed = (d-betrag / f-sales * 100).
    ELSE fb-flash.t-consumed = 0.
    IF tf-sales NE 0 THEN fb-flash.mtd-consumed = (m-betrag / tf-sales) * 100.
    ELSE fb-flash.mtd-consumed = 0.

    CREATE fb-flash.
  END. 
  done = YES. 
END. 
 
PROCEDURE create-bev: 
DEFINE VARIABLE betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-betrag1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-betrag2 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE d1-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE m1-betrag AS DECIMAL INITIAL 0. 
DEFINE VARIABLE flag AS INTEGER. 
 
DEFINE VARIABLE f-eknr AS INTEGER. 
DEFINE VARIABLE b-eknr AS INTEGER. 
DEFINE VARIABLE fl-eknr AS INTEGER. 
DEFINE VARIABLE bl-eknr AS INTEGER. 
 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE amount AS DECIMAL. 
  
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
 
  CREATE fb-flash.
  CREATE fb-flash.
  fb-flash.c-alloc = "** BEVERAGE **".
  CREATE fb-flash.
  
  FOR EACH l-store WHERE l-store.lager-nr NE main-storage AND 
    l-store.lager-nr GE f-store AND l-store.lager-nr LE t-store 
    AND l-store.betriebsnr GT 0 NO-LOCK BY l-store.lager-nr: 

    FOR EACH s-list: 
      delete s-list. 
    END. 
 
    CREATE fb-flash.
    fb-flash.c-alloc = l-store.bezeich.
    
    dstore = l-store.betriebsnr. 
    curr-store = l-store.lager-nr. 
    RUN step-bev1(fl-eknr, bl-eknr).
    
    IF l-store.betriebsnr GT 0 THEN RUN step-bev1a. 
    
    RUN step-bev2(fl-eknr, bl-eknr). 
    RUN beverage-to-food. 
    RUN food-to-beverage. 
    RUN step-two(f-eknr, b-eknr). 
    RUN step-three-bev(fl-eknr, bl-eknr). 
    RUN food-bev(fl-eknr, bl-eknr). 
    RUN step-four(f-eknr, b-eknr, l-store.lager-nr). 
    
    d-betrag = 0. 
    m-betrag = 0. 
    d1-betrag = 0. 
    m1-betrag = 0. 
 
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 1 NO-LOCK 
      BY s-list.nr: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d-betrag = d-betrag + s-list.betrag. 
      m-betrag = m-betrag + s-list.t-betrag. 
      CREATE fb-flash.
      ASSIGN
        fb-flash.bezeich = s-list.bezeich
        fb-flash.t-consumed = s-list.betrag
        fb-flash.mtd-consumed = s-list.t-betrag.
    END. 
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 2 NO-LOCK 
      BY s-list.bezeich: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d-betrag = d-betrag + s-list.betrag. 
      m-betrag = m-betrag + s-list.t-betrag. 
       
      CREATE fb-flash.
      ASSIGN
        fb-flash.bezeich = s-list.bezeich
        fb-flash.t-consumed = s-list.betrag
        fb-flash.mtd-consumed = s-list.t-betrag.
    END. 
 
/** food TO beverage **/ 
    FIND FIRST s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 3 NO-LOCK. 
    d-betrag = d-betrag + s-list.betrag. 
    m-betrag = m-betrag + s-list.t-betrag. 
    
    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = s-list.bezeich
      fb-flash.t-consumed = s-list.betrag
      fb-flash.mtd-consumed = s-list.t-betrag.
    
    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "GROSS CONSUMPTION COST"
      fb-flash.t-consumed = d-betrag
      fb-flash.mtd-consumed = m-betrag.
                                                 
    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "LESS BY:".
                                                                                       
    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "COMPLIMENT COST".

    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 4 NO-LOCK 
      BY s-list.bezeich: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d1-betrag = d1-betrag + s-list.betrag. 
      m1-betrag = m1-betrag + s-list.t-betrag. 
      d-betrag = d-betrag - s-list.betrag. 
      m-betrag = m-betrag - s-list.t-betrag.            

      CREATE fb-flash.
      ASSIGN
        fb-flash.c-alloc = s-list.bezeich
        fb-flash.t-consumed = s-list.betrag
        fb-flash.mtd-consumed = s-list.t-betrag.
    END. 
 
    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = "SUB TOTAL"
      fb-flash.t-consumed = betrag
      fb-flash.mtd-consumed = t-betrag1.
    
    CREATE fb-flash.
    fb-flash.bezeich = "DEPARTMENT EXPENSES".
    
    betrag = 0. 
    t-betrag1 = 0. 
    FOR EACH s-list WHERE s-list.flag = 2 AND s-list.reihenfolge = 5 NO-LOCK 
      BY s-list.bezeich: 
      betrag = betrag + s-list.betrag. 
      t-betrag1 = t-betrag1 + s-list.t-betrag. 
      d1-betrag = d1-betrag + s-list.betrag. 
      m1-betrag = m1-betrag + s-list.t-betrag. 
      d-betrag = d-betrag - s-list.betrag. 
      m-betrag = m-betrag - s-list.t-betrag.            

      CREATE fb-flash.
      ASSIGN
        fb-flash.c-alloc = s-list.bezeich
        fb-flash.t-consumed = s-list.betrag
        fb-flash.mtd-consumed = s-list.t-betrag.
    END. 
 
/** beverage TO food **/ 
    FIND FIRST s-list WHERE s-list.flag = 1 AND s-list.reihenfolge = 3 NO-LOCK. 
    betrag = betrag + s-list.betrag. 
    t-betrag1 = t-betrag1 + s-list.t-betrag. 
    d1-betrag = d1-betrag + s-list.betrag. 
    m1-betrag = m1-betrag + s-list.t-betrag. 
    d-betrag = d-betrag - s-list.betrag. 
    m-betrag = m-betrag - s-list.t-betrag. 
    
    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = s-list.bezeich
      fb-flash.t-consumed = s-list.betrag
      fb-flash.mtd-consumed = s-list.t-betrag.
 
    CREATE fb-flash.
    ASSIGN
      fb-flash.flag = 1
      fb-flash.c-alloc = "SUB TOTAL"
      fb-flash.t-consumed = betrag
      fb-flash.mtd-consumed = t-betrag1.
                                                
    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "TOTAL EXPENSES"
      fb-flash.t-consumed = d1-betrag
      fb-flash.mtd-consumed = m1-betrag.

    CREATE fb-flash.
    ASSIGN
      fb-flash.bezeich = "NET CONSUMPTION COST"
      fb-flash.t-consumed = d-betrag
      fb-flash.mtd-consumed = m-betrag.


    CREATE fb-flash.
    ASSIGN
      fb-flash.c-alloc = "Nett Beverage Sales"
      fb-flash.t-consumed = b-sales
      fb-flash.mtd-consumed = tb-sales.
                                                                                     
    CREATE fb-flash.
    ASSIGN
      fb-flash.flag = 99
      fb-flash.c-alloc = "R a t i o  Cost:Sales (%)". 

    IF b-sales NE 0 THEN fb-flash.t-consumed = d-betrag / b-sales * 100. 
    IF tb-sales NE 0 THEN fb-flash.mtd-consumed = (m-betrag / tb-sales) * 100.

    CREATE fb-flash.
  END. 
  
  done = YES. 
END. 


/*** FOOD Cost BY calculating incoming due-to transfer TO storages ***/ 
PROCEDURE step-food1: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 1. 
 
/** Transfer from (side-) store (l-op.lager-nr) TO other 
    (side-) store (l-op.pos) **/ 
 
  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-store NO-LOCK. 
  create s-list. 
  s-list.nr = 1. 
  s-list.reihenfolge = 1. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("TRANSFER TO SIDE STORE",lvCAREA,"") . 
  s-list.flag = flag. 
 
/* 
  FOR EACH l-ophdr WHERE l-ophdr.datum GE date1 
    AND l-ophdr.datum LE date2 
    AND l-ophdr.op-typ = "STT" NO-LOCK USE-INDEX l-ophdr-dat, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
*/ 
  FOR EACH l-op WHERE l-op.loeschflag LE 1 AND l-op.op-art = 4 
    AND l-op.herkunftflag = 1 
    AND (l-op.lager-nr = curr-store OR l-op.pos = curr-store) 
    AND l-op.datum GE date1 AND l-op.datum LE date2 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = fl-eknr NO-LOCK: 
 
/** deduct onhand due TO transferred from side store **/ 
    IF l-op.lager-nr = curr-store THEN 
    DO: 
      s-list.t-betrag = s-list.t-betrag - l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag - l-op.warenwert. 
    END. 
 
/** add onhand due TO transferred TO side-store */ 
    IF l-op.pos = curr-store THEN 
    DO: 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
    END. 
  END. 
END. 
 
/*** FOOD Cost BY calculating due-to Kitchen-Transfer ***/ 
PROCEDURE step-food1a: 
DEFINE VARIABLE curr-dept AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 1. 
 
  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-store NO-LOCK. 
  curr-dept = l-lager.betriebsnr. 
  create s-list. 
  s-list.nr = 2. 
  s-list.reihenfolge = 1. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("KITCHEN TRANSFER IN",lvCAREA,"") . 
  s-list.flag = flag. 
  create s-list. 
  s-list.nr = 3. 
  s-list.reihenfolge = 1. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("KITCHEN TRANSFER OUT",lvCAREA,"") . 
  s-list.flag = flag. 
 
  FOR EACH h-compli WHERE h-compli.datum GE date1 AND h-compli.datum LE date2 
    AND h-compli.betriebsnr GT 0 AND h-compli.p-artnr = 1 
    NO-LOCK BY h-compli.departement: 
/** add cost due TO transferred from other kitchen **/ 
    FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.betriebsnr NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nr = 2. 
      s-list.t-betrag = s-list.t-betrag + h-compli.epreis. 
      IF h-compli.datum = date2 THEN s-list.betrag 
        = s-list.betrag + h-compli.epreis. 
    END. 
/** reduce cost due TO transferred TO other kitchen **/ 
    ELSE 
    DO: 
      FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.departement 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.nr = 3. 
        s-list.t-betrag = s-list.t-betrag - h-compli.epreis. 
        IF h-compli.datum = date2 THEN s-list.betrag 
          = s-list.betrag - h-compli.epreis. 
      END. 
    END. 
  END. 
END. 
 
/*** BEVERAGE Cost BY calculating incoming due-to transfer TO storages ***/ 
PROCEDURE step-bev1: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 2. 
/** Transfer from (side-) store (l-op.lager-nr) TO other 
    (side-) store (l-op.pos) **/ 
 
  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-store NO-LOCK. 
  create s-list. 
  s-list.nr = 1. 
  s-list.reihenfolge = 1. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("TRANSFER TO SIDE STORE",lvCAREA,"") . 
  s-list.flag = flag. 
/* 
  FOR EACH l-ophdr WHERE l-ophdr.datum GE date1 
    AND l-ophdr.datum LE date2 
    AND l-ophdr.op-typ = "STT" NO-LOCK USE-INDEX l-ophdr-dat, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
*/ 
  FOR EACH l-op WHERE l-op.loeschflag LE 1 AND l-op.op-art = 4 
    AND l-op.herkunftflag = 1 
    AND (l-op.lager-nr = curr-store OR l-op.pos = curr-store) 
    AND l-op.datum GE date1 AND l-op.datum LE date2 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = bl-eknr NO-LOCK: 
 
/** deduct onhand due TO transferred from side store */ 
    IF l-op.lager-nr = curr-store THEN 
    DO: 
      s-list.t-betrag = s-list.t-betrag - l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag - l-op.warenwert. 
    END. 
 
/** add onhand due TO transferred TO side-store */ 
    IF l-op.pos = curr-store THEN 
    DO: 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
    END. 
  END. 
END. 
 
/*** BEV Cost BY calculating due-to Kitchen-Transfer ***/ 
PROCEDURE step-bev1a: 
DEFINE VARIABLE curr-dept AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 2. 
 
  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-store NO-LOCK. 
  curr-dept = l-lager.betriebsnr. 
  create s-list. 
  s-list.nr = 2. 
  s-list.reihenfolge = 1. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("KITCHEN TRANSFER IN",lvCAREA,"") . 
  s-list.flag = flag. 
  create s-list. 
  s-list.nr = 3. 
  s-list.reihenfolge = 1. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("KITCHEN TRANSFER OUT",lvCAREA,"") . 
  s-list.flag = flag. 
 
  FOR EACH h-compli WHERE h-compli.datum GE date1 AND h-compli.datum LE date2 
    AND h-compli.betriebsnr GT 0 AND h-compli.p-artnr = 2 NO-LOCK 
    BY h-compli.departement: 
/** add cost due TO transferred from other kitchen **/ 
    FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.betriebsnr NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nr = 2. 
      s-list.t-betrag = s-list.t-betrag + h-compli.epreis. 
      IF h-compli.datum = date2 THEN s-list.betrag 
        = s-list.betrag + h-compli.epreis. 
    END. 
/** reduce cost due TO transferred TO other kitchen **/ 
    ELSE 
    DO: 
      FIND FIRST hoteldpt WHERE hoteldpt.num = h-compli.departement 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE hoteldpt AND hoteldpt.betriebsnr = l-lager.lager-nr THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.nr = 3. 
        s-list.t-betrag = s-list.t-betrag - h-compli.epreis. 
        IF h-compli.datum = date2 THEN s-list.betrag 
          = s-list.betrag - h-compli.epreis. 
      END. 
    END. 
  END. 
END. 
 
/*** FOOD Cost BY incoming due-to direct puchasing TO outlet stores ***/ 
PROCEDURE step-food2: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 1. 
 
  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-store NO-LOCK. 
  create s-list. 
  s-list.reihenfolge = 2. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("DIRECT PURCHASED",lvCAREA,""). 
  s-list.flag = flag. 
/* 
  FOR EACH l-ophdr WHERE l-ophdr.datum GE date1 
    AND l-ophdr.datum LE date2 
    AND l-ophdr.op-typ = "STI" NO-LOCK USE-INDEX l-ophdr-dat, 
*/ 
  FOR EACH l-op WHERE /* l-op.lscheinnr = l-ophdr.lscheinnr AND */ 
    l-op.pos GT 0 AND l-op.loeschflag LE 1 AND l-op.op-art = 1 
    AND l-op.datum GE date1 AND l-op.datum LE date2 
    AND l-op.lager-nr = curr-store NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = fl-eknr NO-LOCK: 
    s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
    IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
  END. 
END. 
 
/*** BEVERAGE Cost BY incoming due-to direct puchasing TO outlet stores ***/ 
PROCEDURE step-bev2: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 2. 
 
  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-store NO-LOCK. 
  create s-list. 
  s-list.reihenfolge = 2. 
  s-list.lager-nr = l-lager.lager-nr. 
  s-list.bezeich = translateExtended ("DIRECT PURCHASED",lvCAREA,""). 
  s-list.flag = flag. 
/* 
  FOR EACH l-ophdr WHERE l-ophdr.datum GE date1 
    AND l-ophdr.datum LE date2 
    AND l-ophdr.op-typ = "STI" NO-LOCK USE-INDEX l-ophdr-dat, 
*/ 
  FOR EACH l-op WHERE /* l-op.lscheinnr = l-ophdr.lscheinnr AND */ 
    l-op.pos GT 0 AND l-op.loeschflag LE 1 AND l-op.op-art = 1 
    AND l-op.datum GE date1 AND l-op.datum LE date2 
    AND l-op.lager-nr EQ curr-store NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = bl-eknr NO-LOCK: 
    s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
    IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
  END. 
END. 
 
PROCEDURE beverage-to-food: 
  FIND FIRST htparam WHERE paramnr = 272 NO-LOCK. 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK. 
  bev-food = fchar. 
  
  CREATE s-list. 
  ASSIGN
      s-list.reihenfolge = 3 
      s-list.bezeich     = STRING(gl-acct.fibukonto, coa-format) + " "  
                         + CAPS(gl-acct.bezeich) 
      s-list.flag        = 1
  . 
END. 
 
PROCEDURE food-to-beverage: 
  FIND FIRST htparam WHERE paramnr = 275 NO-LOCK. 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK. 
  food-bev = fchar. 
  CREATE s-list. 
  ASSIGN
      s-list.reihenfolge = 3
      s-list.bezeich     = STRING(gl-acct.fibukonto, coa-format) + " " 
                         + CAPS(gl-acct.bezeich)
      s-list.flag        = 2
  . 
END. 
 
/*** Less BY FB Compliment ***/ 
PROCEDURE step-two: 
DEFINE INPUT PARAMETER f-endkum AS INTEGER. 
DEFINE INPUT PARAMETER b-endkum AS INTEGER. 
DEFINE buffer h-art FOR h-artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE VARIABLE flag AS INTEGER. 
DEFINE VARIABLE cost-account AS CHAR. 
DEFINE VARIABLE cost-value AS DECIMAL. 
DEFINE VARIABLE rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-datum AS DATE INITIAL ?. 
DEFINE VARIABLE cost AS DECIMAL. 
DEFINE VARIABLE com-artnr AS INTEGER. 
DEFINE VARIABLE com-bezeich AS CHAR. 
DEFINE VARIABLE com-fibu AS CHAR. 
 
  IF dstore = 0 THEN RETURN. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GT 0 AND 
    (hoteldpt.num EQ l-store.betriebsnr OR 
     hoteldpt.betriebsnr = l-store.lager-nr) NO-LOCK BY hoteldpt.num: 
    FOR EACH h-compli WHERE h-compli.datum GE date1 
      AND h-compli.datum LE date2 AND h-compli.departement EQ hoteldpt.num 
      AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
      AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
      BY h-compli.datum BY h-compli.rechnr: 
 
      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
          AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        ELSE FIND FIRST exrate WHERE exrate.datum = curr-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 
 
      FIND FIRST artikel WHERE artikel.artnr = h-art.artnrfront 
        AND artikel.departement = 0 NO-LOCK. 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto 
        = artikel.fibukonto NO-LOCK. 
      ASSIGN
          com-artnr   = artikel.artnr
          com-bezeich = STRING(gl-acct.fibukonto, coa-format) + " " 
                      + CAPS(gl-acct.bezeich) 
          com-fibu    = gl-acct.fibukonto. 
 
      FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
        AND h-artikel.departement = h-compli.departement NO-LOCK. 
      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = h-artikel.departement NO-LOCK. 
      flag = 0. 
      IF artikel.endkum = f-endkum THEN flag = 1. 
      ELSE IF artikel.endkum = b-endkum THEN flag = 2. 
 
      FIND FIRST s-list WHERE s-list.fibukonto = com-fibu 
        AND s-list.reihenfolge = 4 AND s-list.flag = flag NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        create s-list. 
        s-list.reihenfolge = 4. 
        s-list.lager-nr = com-artnr. 
        s-list.fibukonto = com-fibu. 
        s-list.bezeich = com-bezeich. 
        s-list.flag = flag. 
      END. 
 
      cost = 0. 
      FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
        AND h-cost.departement = h-compli.departement 
        AND h-cost.datum = h-compli.datum 
        AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
        cost = h-compli.anzahl * h-cost.betrag. 
      ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) 
      THEN DO: 
        cost = h-compli.anzahl * h-compli.epreis * 
          h-artikel.prozent / 100 * rate. 
      END. 
      s-list.t-betrag = s-list.t-betrag + cost. 
      IF h-compli.datum = date2 THEN s-list.betrag = s-list.betrag + cost. 
    END. 
  END. 
END. 
 
/* Less BY FOOD Requisition FOR Department Expenses */ 
PROCEDURE step-three-food: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 1. 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.loeschflag LE 1 
    AND l-op.op-art = 3 AND l-op.lager-nr = curr-store 
    AND l-op.datum GE date1 AND l-op.datum LE date2 NO-LOCK, 
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
      AND (gl-acct.acc-type = 5 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 4) NO-LOCK, 
    FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = fl-eknr NO-LOCK: 
 
    ASSIGN
        fibukonto = gl-acct.fibukonto 
        bezeich   = STRING(gl-acct.fibukonto, coa-format) + " " 
                  + CAPS(gl-acct.bezeich)
    . 
    IF l-op.stornogrund NE "" THEN 
    DO: 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct1 THEN 
      ASSIGN 
          fibukonto = gl-acct1.fibukonto 
          bezeich   = STRING(gl-acct1.fibukonto, coa-format) + " " 
                    + CAPS(gl-acct1.bezeich)
      . 
    END. 
 
    IF fibukonto = food-bev THEN. 
    ELSE IF fibukonto = bev-food THEN. 
    ELSE 
    DO: 
      FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
        AND s-list.reihenfolge = 5 AND s-list.flag = flag NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        create s-list. 
        s-list.reihenfolge = 5. 
        s-list.fibukonto = fibukonto. 
         s-list.bezeich = bezeich. 
        s-list.flag = flag. 
      END. 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
    END. 
  END. 
END. 
 
/* Less BY BEVERAGE Requisition FOR Department Expenses */ 
PROCEDURE step-three-bev: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
DEFINE VARIABLE flag AS INTEGER INITIAL 2. 
DEFINE VARIABLE fibukonto LIKE gl-acct.fibukonto. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE buffer gl-acct1 FOR gl-acct. 
 
  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.loeschflag LE 1 
    AND l-op.op-art = 3 AND l-op.lager-nr = curr-store 
    AND l-op.datum GE date1 AND l-op.datum LE date2 NO-LOCK, 
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
      AND (gl-acct.acc-type = 5 OR gl-acct.acc-type = 3 OR gl-acct.acc-type = 4) NO-LOCK, 
    FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = bl-eknr NO-LOCK: 
 
    ASSIGN
        fibukonto = gl-acct.fibukonto 
        bezeich   = STRING(gl-acct.fibukonto, coa-format) + " " 
                  + CAPS(gl-acct.bezeich)
    . 
    IF l-op.stornogrund NE "" THEN 
    DO: 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct1 THEN 
      ASSIGN 
          fibukonto = gl-acct1.fibukonto 
          bezeich   = STRING(gl-acct1.fibukonto, coa-format) + " " 
                    + CAPS(gl-acct1.bezeich)
      . 
    END. 
 
    IF fibukonto = food-bev THEN. 
    ELSE IF fibukonto = bev-food THEN. 
    ELSE 
    DO: 
      FIND FIRST s-list WHERE s-list.fibukonto = fibukonto 
        AND s-list.reihenfolge = 5 AND s-list.flag = flag NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        create s-list. 
        s-list.reihenfolge = 5. 
        s-list.fibukonto = fibukonto. 
         s-list.bezeich = bezeich. 
        s-list.flag = flag. 
      END. 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag + l-op.warenwert. 
    END. 
  END. 
END. 
 
/*** food TO beverage - baverage TO food ***/ 
/* 
PROCEDURE food-bev: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE date1 AND l-ophdr.datum LE date2 
    AND (l-ophdr.fibukonto = bev-food OR l-ophdr.fibukonto = food-bev) 
    NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 
    AND l-op.lager-nr = curr-store NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
    IF l-ophdr.fibukonto = food-bev THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.reihenfolge = 3 
        AND s-list.flag = 2. 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag 
        + l-op.warenwert. 
    END. 
    ELSE IF l-ophdr.fibukonto = bev-food THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.reihenfolge = 3 
        AND s-list.flag = 1. 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag 
        + l-op.warenwert. 
    END. 
  END. 
END. 
*/ 
PROCEDURE food-bev: 
DEFINE INPUT PARAMETER fl-eknr AS INTEGER. 
DEFINE INPUT PARAMETER bl-eknr AS INTEGER. 
  FOR EACH l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
    AND l-op.datum GE date1 AND l-op.datum LE date2 
    AND (l-op.stornogrund = bev-food OR l-op.stornogrund = food-bev) 
    AND l-op.lager-nr = curr-store NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
    IF l-op.stornogrund = food-bev THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.reihenfolge = 3 
        AND s-list.flag = 2. 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag 
        + l-op.warenwert. 
    END. 
    ELSE IF l-op.stornogrund = bev-food THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.reihenfolge = 3 
        AND s-list.flag = 1. 
      s-list.t-betrag = s-list.t-betrag + l-op.warenwert. 
      IF l-op.datum = date2 THEN s-list.betrag = s-list.betrag 
        + l-op.warenwert. 
    END. 
  END. 
END. 
 
/**** F&B Sales ****/ 
PROCEDURE step-four: 
DEFINE INPUT PARAMETER f-eknr   AS INTEGER. 
DEFINE INPUT PARAMETER b-eknr   AS INTEGER. 
DEFINE INPUT PARAMETER store-nr AS INTEGER. 
DEFINE VARIABLE h-service       AS DECIMAL. 
DEFINE VARIABLE h-mwst          AS DECIMAL. 
DEFINE VARIABLE vat2            AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact            AS DECIMAL NO-UNDO.
DEFINE VARIABLE amount          AS DECIMAL. 
DEFINE VARIABLE serv-taxable    AS LOGICAL. 
  f-sales = 0. 
  b-sales = 0. 
  tf-sales = 0. 
  tb-sales = 0. 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-taxable = htparam.flogical. 
 
  IF dstore = 0 THEN RETURN. 
  FOR EACH hoteldpt WHERE (hoteldpt.num EQ dstore 
    OR hoteldpt.betriebsnr = store-nr) NO-LOCK BY hoteldpt.num: 
    FOR EACH artikel WHERE artikel.artart = 0 
      AND artikel.departement = hoteldpt.num 
      AND (artikel.endkum = f-eknr OR artikel.endkum = b-eknr 
      OR artikel.umsatzart = 3 OR artikel.umsatzart = 5 
      OR artikel.umsatzart = 6) NO-LOCK: 
      
      FOR EACH umsatz WHERE umsatz.datum GE date1 
        AND umsatz.datum LE date2 
        AND umsatz.departement = artikel.departement 
        AND umsatz.artnr = artikel.artnr NO-LOCK: 
/*
        h-service = 0. 
        h-mwst = 0. 
        RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, 
               artikel.service-code, artikel.mwst-code, OUTPUT h-service, OUTPUT h-mwst).
*/
/* SY AUG 13 2017 */
        RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            umsatz.datum, OUTPUT h-service, OUTPUT h-mwst, 
            OUTPUT vat2, OUTPUT fact).
        ASSIGN h-mwst = h-mwst + vat2.

        amount = umsatz.betrag / fact. 
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
 

