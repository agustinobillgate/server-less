DEFINE TEMP-TABLE art-list 
  FIELD pos         AS INTEGER 
  FIELD artnr       AS INTEGER 
  FIELD bezeich     AS CHAR 
  FIELD epreis      AS DECIMAL
  FIELD item-bgcol  AS INTEGER INITIAL 2
  FIELD item-fgcol  AS INTEGER INITIAL 15
. 

DEF INPUT PARAMETER zero-flag AS LOGICAL.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER curr-zwkum AS INT.
DEF INPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER curr-apos AS INT.
DEF OUTPUT PARAMETER max-apos AS INT.
DEF OUTPUT PARAMETER TABLE FOR art-list.

DEFINE VARIABLE fgcol-array AS INTEGER EXTENT 17
    INITIAL [15, 15, 15, 15, 15, 15, 15, 15, 0,
             15, 0, 0, 15, 15, 0, 0, 15].


RUN build-alist.

PROCEDURE build-alist: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH art-list: 
    DELETE art-list. 
  END. 
  curr-apos = 1. 
  IF NOT zero-flag THEN 
  FOR EACH vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
    AND vhp.h-artikel.artart = 0 AND vhp.h-artikel.zwkum = curr-zwkum 
    AND vhp.h-artikel.epreis1 NE 0 AND vhp.h-artikel.activeflag 
    AND (vhp.h-artikel.s-gueltig = ? OR (vhp.h-artikel.s-gueltig LE billdate 
    AND vhp.h-artikel.e-gueltig GE billdate)) NO-LOCK 
    BY vhp.h-artikel.abbuchung DESCENDING BY vhp.h-artikel.bezeich: 
    i = i + 1. 
    CREATE art-list. 
    ASSIGN 
      art-list.pos = i 
      art-list.artnr = vhp.h-artikel.artnr 
      art-list.bezeich = vhp.h-artikel.bezeich 
      art-list.epreis = vhp.h-artikel.epreis1
      art-list.item-bgcol = vhp.h-artikel.abbuchung
      art-list.item-fgcol = fgcol-array[art-list.item-bgcol + 1] 
    . 
    IF art-list.item-bgcol = 0 THEN art-list.item-bgcol = 2.
  END. 
  ELSE 
  FOR EACH vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
    AND vhp.h-artikel.artart = 0 AND vhp.h-artikel.zwkum = curr-zwkum 
    AND vhp.h-artikel.activeflag 
    AND (vhp.h-artikel.s-gueltig = ? OR (vhp.h-artikel.s-gueltig LE billdate 
    AND vhp.h-artikel.e-gueltig GE billdate)) NO-LOCK 
    BY vhp.h-artikel.abbuchung DESCENDING BY vhp.h-artikel.bezeich: 
    i = i + 1. 
    CREATE art-list. 
    ASSIGN 
      art-list.pos = i 
      art-list.artnr = vhp.h-artikel.artnr 
      art-list.bezeich = vhp.h-artikel.bezeich 
      art-list.epreis = vhp.h-artikel.epreis1 
      art-list.item-bgcol = vhp.h-artikel.abbuchung
      art-list.item-fgcol = fgcol-array[art-list.item-bgcol + 1] 
    . 
    IF art-list.item-bgcol = 0 THEN art-list.item-bgcol = 2.
  END. 
  max-apos = i. 
END. 
