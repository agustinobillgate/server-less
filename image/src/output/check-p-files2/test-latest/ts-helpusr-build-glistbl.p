DEFINE TEMP-TABLE grp-list 
  FIELD pos       AS INTEGER 
  FIELD num       AS INTEGER 
  FIELD bezeich   AS CHAR. 

DEF INPUT  PARAMETER dept     AS INT.
DEF OUTPUT PARAMETER curr-num AS INT.
DEF OUTPUT PARAMETER max-gpos AS INT.
DEF OUTPUT PARAMETER p1079    AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR grp-list.

RUN build-glist.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1079 NO-LOCK.
p1079 = htparam.flogical.

PROCEDURE build-glist: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH vhp.kellner WHERE vhp.kellner.departement EQ dept NO-LOCK 
    BY vhp.kellner.kellnername: 
    i = i + 1. 
    create grp-list. 
    grp-list.pos = i. 
    grp-list.num = vhp.kellner.kellner-nr. 
    grp-list.bezeich = vhp.kellner.kellnername. 
    IF i = 1 THEN curr-num = vhp.kellner.kellner-nr. 
  END. 
  max-gpos = i. 
END. 
