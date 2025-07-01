DEFINE TEMP-TABLE grp-compl 
  FIELD pos AS int 
  FIELD num AS int 
  FIELD bezeich AS CHAR. 


DEFINE INPUT  PARAMETER dept    AS INTEGER. 
DEFINE OUTPUT PARAMETER max-gpos AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER p-178   AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR grp-compl.

DEFINE VAR curr-num AS int. 

/*FDL Nov 20, 2024: Ticket 25A58A*/
FIND FIRST htparam WHERE htparam.paramnr EQ 178 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.fchar NE "" THEN
DO:
    p-178 = HEX-ENCODE(SHA1-DIGEST(htparam.fchar)).
END.

RUN build-compl. 


PROCEDURE build-compl: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
  AND vhp.h-artikel.artart = 11 AND vhp.h-artikel.activeflag 
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
