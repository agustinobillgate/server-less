DEFINE TEMP-TABLE grp-compl 
  FIELD pos AS int 
  FIELD num AS int 
  FIELD bezeich AS CHAR. 

DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER max-gpos AS INT.
DEF OUTPUT PARAMETER TABLE FOR grp-compl.

DEFINE VAR curr-num AS int. 

RUN build-compl.

PROCEDURE build-compl:
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
  AND vhp.h-artikel.artart = 12 AND vhp.h-artikel.activeflag 
  NO-LOCK BY vhp.h-artikel.bezeich : 
    i = i + 1. 
    create grp-compl. 
    grp-compl.pos = i. 
    grp-compl.num = vhp.h-artikel.artnr. 
    grp-compl.bezeich = vhp.h-artikel.bezeich. 
    IF i = 1 THEN curr-num = vhp.h-artikel.artnr. 
  END. 
 max-gpos = i. 
END. 
