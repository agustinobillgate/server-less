DEFINE TEMP-TABLE t-list 
  FIELD pos         AS INTEGER 
  FIELD tischnr     LIKE vhp.tisch.tischnr 
  FIELD beleg       AS LOGICAL INITIAL NO 
  FIELD balance     LIKE vhp.h-bill.saldo. 

DEF INPUT  PARAMETER dept       AS INT.
DEF OUTPUT PARAMETER tablestr   AS CHAR.
DEF OUTPUT PARAMETER max-pos    AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER TABLE FOR t-list.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1007 NO-LOCK. 
IF vhp.htparam.flogical THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 200 NO-LOCK. 
  IF vhp.htparam.finteger = dept THEN 
  DO: 
    tablestr = "Cabin:". 
    /*MTFRAME frame1:TITLE = "Select Cabin". */
  END. 
END. 

RUN build-list.

PROCEDURE build-list: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH vhp.tisch WHERE vhp.tisch.departement = dept NO-LOCK BY vhp.tisch.tischnr: 
    FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = vhp.tisch.tischnr 
      AND vhp.h-bill.departement = dept AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR. 
    i = i + 1. 
    create t-list. 
    t-list.pos = i. 
    t-list.tischnr = vhp.tisch.tischnr. 
    IF AVAILABLE vhp.h-bill THEN 
    DO: 
      t-list.beleg = YES. 
      t-list.balance = vhp.h-bill.saldo. 
    END. 
  END. 
  max-pos = i. 
END. 
