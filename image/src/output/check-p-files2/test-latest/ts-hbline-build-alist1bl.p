DEFINE TEMP-TABLE art-list 
  FIELD pos         AS INTEGER 
  FIELD artnr       AS INTEGER 
  FIELD bezeich     AS CHAR 
  FIELD epreis      AS DECIMAL
  FIELD item-bgcol  AS INTEGER INITIAL 2
  FIELD item-fgcol  AS INTEGER INITIAL 15
. 

DEF INPUT PARAMETER artNo      AS INTEGER.
DEF INPUT  PARAMETER dept      AS INT.
DEF OUTPUT PARAMETER curr-apos AS INT.
DEF OUTPUT PARAMETER TABLE FOR art-list.

RUN build-alist1.

PROCEDURE build-alist1:
  FOR EACH art-list: 
    DELETE art-list. 
  END. 
  curr-apos = 1. 
  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
    AND vhp.h-artikel.artnr= artNo NO-LOCK.
  CREATE art-list. 
  ASSIGN 
    art-list.pos = 1 
    art-list.artnr   = vhp.h-artikel.artnr 
    art-list.bezeich = vhp.h-artikel.bezeich 
    art-list.epreis  = vhp.h-artikel.epreis1 
  . 
END.
