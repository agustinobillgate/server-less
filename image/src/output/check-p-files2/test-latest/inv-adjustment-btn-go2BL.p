/*DEFINE TEMP-TABLE c-list 
  FIELD artnr       LIKE l-artikel.artnr 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit       AS CHAR FORMAT "x(3)" COLUMN-LABEL "Unit" 
  FIELD inhalt      AS DECIMAL FORMAT ">>>>9.99" COLUMN-LABEL "Content" 
  FIELD zwkum       AS INTEGER 
  FIELD endkum      AS INTEGER 
  FIELD qty         AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1        AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto   LIKE gl-acct.fibukonto INITIAL "0000000000" 
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
  FIELD qty         AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1        AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto   LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD avrg-price  AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "  Average Price" /*FD Jan 27, 20222*/
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation".  

DEF INPUT PARAMETER from-grp    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER sorttype    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-lager  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR c-list.

DEFINE VARIABLE zwkum AS INTEGER NO-UNDO.
DEFINE VARIABLE a-bez AS CHAR    NO-UNDO.

IF from-grp = 0 THEN RUN journal-list. 
ELSE RUN journal-list1. 


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
        c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
        c-list.avrg-price   = l-artikel.vk-preis. 
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
            zwkum               = l-artikel.zwkum
            c-list.avrg-price   = l-artikel.vk-preis.
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
        c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
        c-list.avrg-price   = l-artikel.vk-preis.
  END. 
  ELSE IF sorttype = 3 THEN 
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
            c-list.artnr        = l-artikel.artnr
            c-list.bezeich      = l-artikel.bezeich 
            c-list.munit        = l-artikel.masseinheit 
            c-list.inhalt       = STRING(l-artikel.inhalt, ">>>>9.99")
            c-list.endkum       = l-artikel.endkum
            c-list.zwkum        = STRING(l-artikel.zwkum, ">>>>>>9") 
            c-list.qty          = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
            c-list.qty1         = l-bestand.anz-anf-best + anz-eingang - anz-ausgang
            zwkum               = l-artikel.zwkum
            c-list.avrg-price   = l-artikel.vk-preis.
  END. 
END. 

