DEFINE TEMP-TABLE t-list 
  FIELD dept        AS INTEGER FORMAT "99" LABEL "Dept"
  FIELD tischnr     LIKE vhp.tisch.tischnr 
  FIELD bezeich     LIKE vhp.tisch.bezeich FORMAT "x(16)" 
  FIELD normalbeleg LIKE vhp.tisch.normalbeleg 
  FIELD name        LIKE vhp.kellner.kellnername FORMAT "x(12)" INITIAL "" 
                    COLUMN-LABEL "Served by" 
  FIELD occupied    AS LOGICAL FORMAT "Yes/No" LABEL "OCC" INITIAL NO 
  FIELD belegung    LIKE vhp.h-bill.belegung COLUMN-LABEL "Pax" 
  FIELD balance     LIKE vhp.h-bill.saldo
  FIELD zinr        LIKE vhp.res-line.zinr
  FIELD gname       LIKE vhp.res-line.NAME
. 
 
DEF INPUT PARAMETER dept        AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER tot-saldo  AS DECIMAL NO-UNDO INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-list.

IF dept GT 0 THEN RUN build-list.
ELSE RUN build-list0.

PROCEDURE build-list0: 
  FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
    FOR EACH vhp.tisch WHERE vhp.tisch.departement = hoteldpt.num NO-LOCK, 
      FIRST vhp.h-bill WHERE vhp.h-bill.departement = hoteldpt.num 
      AND vhp.h-bill.tisch = vhp.tisch.tischnr 
      AND vhp.h-bill.flag = 0 BY vhp.tisch.tischnr: 
      CREATE t-list.
      ASSIGN
        t-list.dept           = hoteldpt.num
        t-list.tischnr        = vhp.tisch.tischnr
        t-list.bezeich        = vhp.tisch.bezeich 
        t-list.normalbeleg    = vhp.tisch.normalbeleg 
        t-list.occupied       = YES
        t-list.belegung       = vhp.h-bill.belegung
        t-list.gname          = vhp.h-bill.bilname
        t-list.balance        = vhp.h-bill.saldo
      . 
      FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr 
       = vhp.h-bill.kellner-nr 
        AND vhp.kellner.departement = hoteldpt.num NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.kellner THEN t-list.name = vhp.kellner.kellnername. 

      FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill.resnr 
        AND vhp.res-line.reslinnr = vhp.h-bill.reslinnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.res-line THEN 
      ASSIGN
        t-list.zinr  = vhp.res-line.zinr
        t-list.gname = vhp.res-line.NAME
      .    
   
      tot-saldo = tot-saldo + vhp.h-bill.saldo. 
    END. 
  END.
END. 

PROCEDURE build-list: 
  FOR EACH vhp.tisch WHERE vhp.tisch.departement = dept NO-LOCK, 
    FIRST vhp.h-bill WHERE vhp.h-bill.departement = dept 
    AND vhp.h-bill.tisch = vhp.tisch.tischnr 
    AND vhp.h-bill.flag = 0 BY vhp.tisch.tischnr: 
    CREATE t-list.
    ASSIGN
      t-list.dept           = dept
      t-list.tischnr        = vhp.tisch.tischnr
      t-list.bezeich        = vhp.tisch.bezeich 
      t-list.normalbeleg    = vhp.tisch.normalbeleg 
      t-list.occupied       = YES
      t-list.belegung       = vhp.h-bill.belegung
      t-list.gname          = vhp.h-bill.bilname
      t-list.balance        = vhp.h-bill.saldo
    . 
    FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr 
      = vhp.h-bill.kellner-nr 
      AND vhp.kellner.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.kellner THEN t-list.name = vhp.kellner.kellnername. 

    FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill.resnr 
      AND vhp.res-line.reslinnr = vhp.h-bill.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.res-line THEN 
    ASSIGN
      t-list.zinr  = vhp.res-line.zinr
      t-list.gname = vhp.res-line.NAME
    .    
   
    tot-saldo = tot-saldo + vhp.h-bill.saldo. 
  END. 
END.
