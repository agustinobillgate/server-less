DEFINE TEMP-TABLE grp-list 
  FIELD pos       AS INTEGER 
  FIELD num       AS INTEGER 
  FIELD bezeich   AS CHAR 
  FIELD artname   AS CHAR 
  FIELD curr      AS CHAR 
  FIELD exrate    AS DECIMAL INITIAL 1
  FIELD exrate1   AS DECIMAL INITIAL 1. 


DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER transdate      AS DATE.
DEFINE INPUT  PARAMETER amt         AS DECIMAL. 

DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER curr-local     AS CHAR.
DEF OUTPUT PARAMETER billart        AS INTEGER.
DEF OUTPUT PARAMETER max-gpos       AS INTEGER.

DEF OUTPUT PARAMETER art-exrate     AS DECIMAL.
DEF OUTPUT PARAMETER amount         AS DECIMAL.
DEF OUTPUT PARAMETER paid           AS DECIMAL.
DEF OUTPUT PARAMETER lpaid          AS DECIMAL.
DEF OUTPUT PARAMETER change         AS DECIMAL.
DEF OUTPUT PARAMETER lchange        AS DECIMAL.
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.

DEF OUTPUT PARAMETER TABLE FOR grp-list.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK.
price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK.
billdate = vhp.htparam.fdate.

RUN build-glist.

FIND FIRST grp-list.
FIND FIRST waehrung WHERE waehrung.wabkurz = grp-list.bezeich NO-LOCK. 
ASSIGN 
  art-exrate = grp-list.exrate 
  amount     = ROUND(amt / grp-list.exrate, 2) 
  paid       = - amount 
  lpaid      = - amt 
  change     = 0 
  lchange    = 0 
  . 

PROCEDURE build-glist: 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
DEFINE VARIABLE local-artnr AS INTEGER. 
 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK. 
  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
      AND vhp.h-artikel.artnr = vhp.htparam.finteger NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.h-artikel THEN 
  DO: 
      err-flag = 1.
      RETURN. 
  END. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 152 NO-LOCK. 
  curr-local = vhp.htparam.fchar. 
 
  CREATE grp-list. 
  ASSIGN 
    grp-list.pos        = 1 
    grp-list.num        = vhp.h-artikel.artnr 
    grp-list.bezeich    = curr-local 
    grp-list.artname    = vhp.h-artikel.bezeich 
    local-artnr         = vhp.h-artikel.artnr 
    billart             = vhp.h-artikel.artnr 
  . 
 
  FOR EACH vhp.h-artikel WHERE vhp.h-artikel.departement EQ dept 
      AND vhp.h-artikel.artart = 6 AND vhp.h-artikel.artnr NE local-artnr 
      NO-LOCK BY vhp.h-artikel.bezeich: 
      FIND FIRST vhp.artikel WHERE vhp.artikel.departement = 0 
          AND vhp.artikel.artnr = vhp.h-artikel.artnrfront 
          AND vhp.artikel.pricetab = YES NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.artikel THEN 
      DO: 
        IF vhp.artikel.pricetab THEN 
        DO: 
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = vhp.artikel.betriebsnr 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE waehrung THEN 
          DO: 
            
            i = i + 1. 
            CREATE grp-list. 
            ASSIGN 
              grp-list.pos      = i 
              grp-list.num      = vhp.h-artikel.artnr 
              grp-list.bezeich  = waehrung.wabkurz 
              grp-list.artname  = vhp.h-artikel.bezeich 
              grp-list.exrate   = (waehrung.ankauf / waehrung.einheit)
              grp-list.exrate1  = waehrung.einheit .

            IF (transdate NE ?) AND (transdate LT billdate) THEN 
            DO: 
              FIND FIRST exrate WHERE exrate.artnr = waehrung.waehrungsnr 
                AND exrate.datum = transdate NO-LOCK NO-ERROR. 
              IF AVAILABLE exrate THEN 
                  ASSIGN grp-list.exrate   = exrate.betrag
                         grp-list.exrate1  = exrate.betrag.               
            END. 
          END. 
        END. 
        ELSE 
        DO: 
          i = i + 1. 
          CREATE grp-list. 
          ASSIGN 
            grp-list.pos = i 
            grp-list.num = vhp.h-artikel.artnr 
            grp-list.bezeich = curr-local 
            grp-list.artname = vhp.h-artikel.bezeich 
          . 
        END. 
      END. 
  END. 
  max-gpos = i. 
END. 

