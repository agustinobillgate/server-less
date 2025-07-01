DEFINE TEMP-TABLE menu-list 
  FIELD request AS CHAR 
  FIELD krecid AS INTEGER INITIAL 0 
  FIELD posted AS LOGICAL INITIAL NO 
  FIELD nr AS INTEGER FORMAT ">>>" LABEL "No" 
  FIELD artnr LIKE vhp.h-artikel.artnr 
  FIELD bezeich LIKE vhp.h-artikel.bezeich 
  FIELD anzahl LIKE vhp.h-bill-line.anzahl INITIAL 1 
  FIELD price AS DECIMAL 
  FIELD betrag AS DECIMAL 
  FIELD voucher AS CHAR. 

DEFINE TEMP-TABLE grp-list 
  FIELD pos         AS INTEGER 
  FIELD dept        AS INTEGER 
  FIELD zknr        AS INTEGER 
  FIELD bezeich     AS CHAR
  FIELD grp-bgcol   AS INTEGER INITIAL 1
  FIELD grp-fgcol   AS INTEGER INITIAL 15. 


DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER curr-rechnr    AS INT.
DEF OUTPUT PARAMETER zero-flag      AS LOGICAL.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER max-gpos       AS INT.
DEF OUTPUT PARAMETER cashless-license AS LOGICAL INITIAL NO. /*FDL - Cashless Payment Feature*/
DEF OUTPUT PARAMETER cashless-minsaldo AS DECIMAL. /*FDL - Cashless Payment Feature*/
DEF OUTPUT PARAMETER TABLE FOR menu-list.
DEF OUTPUT PARAMETER TABLE FOR grp-list.

DEFINE BUFFER kbuff FOR vhp.kellner.

DEFINE VARIABLE curr-zwkum AS INTEGER. 
DEFINE VARIABLE fgcol-array AS INTEGER EXTENT 17
    INITIAL [15, 15, 15, 15, 15, 15, 15, 15, 0,
             15, 0, 0, 15, 15, 0, 0, 15].

/*FDL - Cashless Payment Feature*/
/*RUN htplogic.p (1022, OUTPUT cashless-license).*/
FIND FIRST htparam WHERE htparam.paramnr EQ 1022
    AND htparam.bezeich NE "not used"
    AND htparam.flogical NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN cashless-license = YES.

RUN htpdec.p (586, OUTPUT cashless-minsaldo).

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
billdate = vhp.htparam.fdate. 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 869 NO-LOCK. 
zero-flag = vhp.htparam.flogical. 
 
FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE vhp.bediener THEN
FIND FIRST kbuff WHERE kbuff.departement = dept
    AND kbuff.kellner-nr = INTEGER(bediener.userinit) NO-LOCK NO-ERROR.


FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE vhp.bediener THEN
FIND FIRST kbuff WHERE kbuff.departement = dept
    AND kbuff.kellner-nr = INTEGER(bediener.userinit) NO-LOCK NO-ERROR.

RUN build-bline.
RUN build-glist.


PROCEDURE build-bline: 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.departement = dept 
    AND vhp.h-bill-line.rechnr = curr-rechnr NO-LOCK, 
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-artikel.artnr 
    AND vhp.h-artikel.departement = dept AND vhp.h-artikel.artart = 0 
    NO-LOCK BY vhp.h-bill-line.sysdate descending 
    BY vhp.h-bill-line.zeit descending: 
    CREATE menu-list.
    ASSIGN
      menu-list.nr      = 0 
      menu-list.posted  = YES 
      menu-list.REQUEST = ""
      menu-list.artnr   = vhp.h-bill-line.artnr
      menu-list.bezeich = vhp.h-bill-line.bezeich 
      menu-list.anzahl  = vhp.h-bill-line.anzahl 
      balance           = balance + vhp.h-bill-line.betrag
    . 
  END. 
END. 


PROCEDURE build-glist: 
DEFINE VARIABLE i AS INTEGER INITIAL 0.
DEFINE VARIABLE w-fibukonto AS INT INITIAL 0 NO-UNDO.
  IF NOT zero-flag THEN 
  FOR EACH vhp.wgrpdep WHERE vhp.wgrpdep.departement = dept NO-LOCK, 
    FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
    AND vhp.h-artikel.zwkum = vhp.wgrpdep.zknr AND vhp.h-artikel.artart = 0 
    AND vhp.h-artikel.epreis1 NE 0 AND vhp.h-artikel.activeflag NO-LOCK 
    BY vhp.wgrpdep.betriebsnr DESCENDING BY vhp.wgrpdep.bezeich: 
    w-fibukonto = 0.
    i = i + 1. 
    CREATE grp-list. 
    ASSIGN
      grp-list.pos = i
      grp-list.dept = dept 
      grp-list.zknr = vhp.wgrpdep.zknr
      grp-list.bezeich = vhp.wgrpdep.bezeich
    .
    IF i = 1 THEN curr-zwkum = vhp.wgrpdep.zknr. 
    w-fibukonto = INTEGER(ENTRY(1, vhp.wgrpdep.fibukonto,";")) NO-ERROR.
    IF w-fibukonto NE 0 THEN
    ASSIGN
      grp-list.grp-bgcol = w-fibukonto
      grp-list.grp-fgcol = fgcol-array[grp-list.grp-bgcol + 1]
    .
  END. 
  ELSE 
  FOR EACH vhp.wgrpdep WHERE vhp.wgrpdep.departement = dept NO-LOCK, 
    FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept 
    AND vhp.h-artikel.zwkum = vhp.wgrpdep.zknr AND vhp.h-artikel.artart = 0 
    AND vhp.h-artikel.activeflag NO-LOCK 
    BY vhp.wgrpdep.betriebsnr DESCENDING BY vhp.wgrpdep.bezeich: 
    w-fibukonto = 0.
    i = i + 1. 
    CREATE grp-list.
    ASSIGN
      grp-list.pos = i
      grp-list.dept = dept 
      grp-list.zknr = vhp.wgrpdep.zknr 
      grp-list.bezeich = vhp.wgrpdep.bezeich 
    .
    IF i = 1 THEN curr-zwkum = vhp.wgrpdep.zknr. 
    w-fibukonto = INTEGER(ENTRY(1, vhp.wgrpdep.fibukonto,";")) NO-ERROR.
    IF w-fibukonto NE 0 THEN
    ASSIGN
      grp-list.grp-bgcol = /*INTEGER(vhp.wgrpdep.fibukonto)*/ w-fibukonto
      grp-list.grp-fgcol = fgcol-array[grp-list.grp-bgcol + 1]
    .
  END.
  max-gpos = i. 
END. 

