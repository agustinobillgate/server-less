/*DEFINE TEMP-TABLE c-list 
  FIELD artnr LIKE l-artikel.artnr 
  FIELD bezeich AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit AS CHAR FORMAT "x(3)" COLUMN-LABEL "Unit" 
  FIELD inhalt AS DECIMAL FORMAT ">>>>9.99" COLUMN-LABEL "Content" 
  FIELD zwkum AS INTEGER 
  FIELD endkum AS INTEGER 
  FIELD qty AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1 AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation". */
  

DEFINE TEMP-TABLE c-list 
  /*FIELD artnr       AS CHAR FORMAT "x(11)"*/
  FIELD artnr       LIKE l-artikel.artnr 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Unit" 
  FIELD inhalt      AS CHAR FORMAT "x(8)" COLUMN-LABEL "Content" 
  FIELD zwkum       AS CHAR FORMAT "x(8)"
  FIELD endkum      AS INTEGER
  FIELD qty AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1 AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto   LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD avrg-price  AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "  Average Price" /*FD Jan 27, 20222*/
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation".

DEF INPUT PARAMETER from-grp AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER sorttype AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT-OUTPUT PARAMETER TABLE FOR c-list.

DEFINE VARIABLE lscheinnr AS CHAR.
DEFINE VARIABLE zwkum AS INTEGER NO-UNDO.
DEFINE VARIABLE a-bez AS CHAR    NO-UNDO.

FIND FIRST bediener WHERE bediener.userinit = user-init.
RUN do-adjustment. 
IF from-grp = 0 THEN RUN journal-list. 
ELSE RUN journal-list1.

PROCEDURE do-adjustment: 
DEFINE VARIABLE curr-fibukonto AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH c-list WHERE c-list.qty NE c-list.qty1 NO-LOCK BY c-list.fibukonto: 
    IF curr-fibukonto NE c-list.fibukonto THEN 
    DO: 
      curr-fibukonto = c-list.fibukonto. 
      i = i + 1. 
      lscheinnr = "INV" + STRING(month(transdate)) 
        + STRING(day(transdate)) + STRING((time + i),">>>>9"). 
      create l-ophdr. 
      l-ophdr.datum =  transdate. 
      l-ophdr.lager-nr = curr-lager. 
      l-ophdr.docu-nr = lscheinnr. 
      l-ophdr.lscheinnr = lscheinnr. 
      l-ophdr.op-typ = "STT". 
      l-ophdr.fibukonto = c-list.fibukonto. 
      FIND CURRENT l-ophdr NO-LOCK. 
    END. 
    RUN create-l-op (c-list.fibukonto).
  END. 
END. 


PROCEDURE journal-list: 
  FOR EACH c-list: 
    DELETE c-list. 
  END. 
  IF sorttype LE 2 THEN 
  FOR EACH l-bestand WHERE l-bestand.lager-nr = curr-lager NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
    BY l-artikel.bezeich: 
     CREATE c-list. 
     ASSIGN 
         c-list.artnr        = l-artikel.artnr
         c-list.bezeich      = l-artikel.bezeich 
         c-list.munit        = l-artikel.masseinheit 
         c-list.inhalt       = STRING(l-artikel.inhalt, ">>>>9.99")
         c-list.endkum       = l-artikel.endkum
         c-list.zwkum        = STRING(l-artikel.zwkum, ">>>>>>9") 
         c-list.qty          = l-bestand.anz-anf-best + anz-eingang - anz-ausgang 
         c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang.
   END. 
   ELSE IF sorttype = 3 THEN DO:
      FOR EACH l-bestand WHERE l-bestand.lager-nr = curr-lager NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
        BY l-artikel.zwkum BY l-artikel.bezeich: 
          IF zwkum NE l-artikel.zwkum THEN DO:
              RUN inv-adjustment-sort3bl.p (l-artikel.zwkum , OUTPUT a-bez).
              CREATE c-list. 
              ASSIGN 
                  c-list.bezeich   = a-bez
                  c-list.zwkum     = STRING(l-artikel.zwkum, ">>>>>>9")
                  c-list.fibukonto = " " .
          END.

          CREATE c-list. 
          ASSIGN 
            c-list.artnr        = l-artikel.artnr
            c-list.bezeich      = l-artikel.bezeich 
            c-list.munit        = l-artikel.masseinheit 
            c-list.inhalt       = STRING(l-artikel.inhalt, ">>>>9.99")
            c-list.endkum       = l-artikel.endkum
            c-list.zwkum        = STRING(l-artikel.zwkum, ">>>>>>9") 
            c-list.qty          = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
            c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
            zwkum               = l-artikel.zwkum. 
      END. 
   END.
END. 
 
PROCEDURE journal-list1: 
  FOR EACH c-list: 
    DELETE c-list. 
  END. 
  IF sorttype LE 2 THEN 
  FOR EACH l-bestand WHERE l-bestand.lager-nr = curr-lager NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK BY l-artikel.bezeich: 
      CREATE c-list. 
      ASSIGN 
          c-list.artnr        = l-artikel.artnr
          c-list.bezeich      = l-artikel.bezeich 
          c-list.munit        = l-artikel.masseinheit 
          c-list.inhalt       = STRING(l-artikel.inhalt, ">>>>9.99")
          c-list.endkum       = l-artikel.endkum
          c-list.zwkum        = STRING(l-artikel.zwkum, ">>>>>>9") 
          c-list.qty          = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
          c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang.
  END. 
  ELSE IF sorttype = 3 THEN DO:
      FOR EACH l-bestand WHERE l-bestand.lager-nr = curr-lager NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
        AND l-artikel.endkum = from-grp NO-LOCK 
        BY l-artikel.zwkum BY l-artikel.bezeich: 
          IF zwkum NE l-artikel.zwkum THEN DO:
              RUN inv-adjustment-sort3bl.p (l-artikel.zwkum , OUTPUT a-bez).
              CREATE c-list. 
              ASSIGN 
                  c-list.bezeich   = a-bez
                  c-list.zwkum     = STRING(l-artikel.zwkum, ">>>>>>9")
                  c-list.fibukonto = " " .
          END.

          CREATE c-list. 
          ASSIGN 
              c-list.artnr      = l-artikel.artnr
            c-list.bezeich      = l-artikel.bezeich 
            c-list.munit        = l-artikel.masseinheit 
            c-list.inhalt       = STRING(l-artikel.inhalt, ">>>>9.99")
            c-list.endkum       = l-artikel.endkum
            c-list.zwkum        = STRING(l-artikel.zwkum, ">>>>>>9") 
            c-list.qty          = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
            c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
            zwkum               = l-artikel.zwkum. 
      END. 
  END.
END. 

PROCEDURE create-l-op: 
DEFINE INPUT PARAMETER fibukonto AS CHAR. 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE delta-wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL. 
DEFINE VARIABLE anz-oh AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE val-oh AS DECIMAL. 
 
  FIND FIRST l-artikel WHERE l-artikel.artnr = INTEGER(c-list.artnr) NO-LOCK. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND l-bestand.artnr = INTEGER(c-list.artnr) NO-LOCK. 
  anz-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
    - l-bestand.anz-ausgang. 
  val-oh = l-bestand.val-anf-best + l-bestand.wert-eingang 
    - l-bestand.wert-ausgang. 
  IF anz-oh NE 0 THEN avrg-price = val-oh / anz-oh. 
  ELSE avrg-price = l-artikel.vk-preis. 
 
  anzahl = DECIMAL(c-list.qty) - DECIMAL(c-list.qty1). 
  wert = anzahl * avrg-price. 
 
/* UPDATE stock onhand  */ 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = INTEGER(c-list.artnr) EXCLUSIVE-LOCK. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
/* WRONG !!! 
    IF c-list.qty1 = 0 THEN 
    DO: 
      delta-wert = val-anf-best + wert-eingang - wert-ausgang. 
      wert-ausgang = wert-ausgang + delta-wert. 
    END. 
*/ 
    FIND CURRENT l-bestand NO-LOCK. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
    l-bestand.artnr = INTEGER(c-list.artnr) EXCLUSIVE-LOCK. 
  l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
  l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
/* WRONG !!! 
  IF c-list.qty1 = 0 AND delta-wert NE 0 THEN 
    wert-ausgang = wert-ausgang + delta-wert. 
*/ 
  FIND CURRENT l-bestand NO-LOCK. 
 
/* Create l-op record */ 
  CREATE l-op. 
  ASSIGN 
    l-op.datum          = transdate 
    l-op.lager-nr       = curr-lager 
    l-op.artnr          = INTEGER(c-list.artnr) 
    l-op.zeit           = TIME 
    l-op.anzahl         = anzahl 
    l-op.einzelpreis    = avrg-price 
    l-op.warenwert      = wert 
    l-op.deci1[1]       = c-list.qty 
    l-op.op-art         = 3 
    l-op.herkunftflag   = 4    /* 4 = inventory !!! */ 
    l-op.lscheinnr      = lscheinnr 
    l-op.pos            = 1 
    l-op.fuellflag      = bediener.nr 
    l-op.stornogrund    = fibukonto 
  . 
  
/* UPDATE consumption */ 
  DO: 
   FIND FIRST l-verbrauch WHERE l-verbrauch.artnr = INTEGER(c-list.artnr) 
     AND l-verbrauch.datum = transdate EXCLUSIVE-LOCK NO-ERROR. 
   IF NOT AVAILABLE l-verbrauch THEN 
   DO: 
     create l-verbrauch. 
     l-verbrauch.artnr = INTEGER(c-list.artnr). 
     l-verbrauch.datum = transdate. 
   END. 
   l-verbrauch.anz-verbrau = l-verbrauch.anz-verbrau + anzahl. 
   l-verbrauch.wert-verbrau = l-verbrauch.wert-verbrau + wert. 
   FIND CURRENT l-verbrauch NO-LOCK. 
  END. 
END. 

