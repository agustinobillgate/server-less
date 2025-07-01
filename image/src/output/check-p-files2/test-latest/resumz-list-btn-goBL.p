
DEFINE TEMP-TABLE output-list 
  FIELD mqty        AS INTEGER FORMAT "->>,>>>" LABEL "MTD Qty" 
  FIELD STR         AS CHAR. 

DEFINE WORKFILE cl-list 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD artnr      AS INTEGER FORMAT ">>>>>>>>>" INITIAL 0 
  FIELD dept       AS INTEGER 
  FIELD bezeich    AS CHAR FORMAT "x(24)" 
  FIELD dnet       AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD dgros      AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD mqty       AS INTEGER FORMAT "->>,>>9" 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz3      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD mgros      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz4      AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEF INPUT PARAMETER ldry-flag AS LOGICAL.
DEF INPUT PARAMETER ldry AS INT.
DEF INPUT PARAMETER dstore AS INT.
DEF INPUT PARAMETER from-dept AS INT.
DEF INPUT PARAMETER to-dept AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER detailed AS LOGICAL.
DEF INPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR output-list.

RUN create-h-umsatz.

PROCEDURE create-h-umsatz: 
  DEFINE VARIABLE dnet AS DECIMAL. 
  DEFINE VARIABLE dgros AS DECIMAL. 
  DEFINE VARIABLE mnet AS DECIMAL. 
  DEFINE VARIABLE mgros AS DECIMAL. 
  DEFINE VARIABLE vat AS DECIMAL. 
  DEFINE VARIABLE serv AS DECIMAL. 
  DEFINE VARIABLE it-exist AS LOGICAL. 
  DEFINE VARIABLE serv-vat AS LOGICAL. 
  DEFINE VARIABLE fact AS DECIMAL. 
 
  DEFINE VARIABLE mqty AS INTEGER INITIAL 0. 
 
  DEFINE VARIABLE curr-ldry AS INTEGER INITIAL 0. 
  DEFINE VARIABLE curr-dstore AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it AS LOGICAL. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  serv-vat = htparam.flogical. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  IF ldry-flag THEN 
  DO: 
    curr-ldry = ldry. 
    curr-dstore = dstore. 
  END. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
    AND hoteldpt.num LE to-dept AND hoteldpt.num NE curr-ldry 
    AND hoteldpt.num NE curr-dstore NO-LOCK BY hoteldpt.num: 
    
    CREATE cl-list. 
    ASSIGN
      cl-list.flag = "*"
      cl-list.bezeich = STRING(hoteldpt.num) + " - " + hoteldpt.depart
      dnet = 0
      dgros = 0 
      mnet = 0 
      mgros = 0 
      mqty = 0. 
 
    FOR EACH h-artikel WHERE (h-artikel.artart = 0 OR h-artikel.artart = 8) 
      AND h-artikel.departement = hoteldpt.num NO-LOCK BY h-artikel.artnr: 
      it-exist = NO. 
    /*  
     IF h-artikel.service-code NE 0 THEN 
      DO: 
        FIND FIRST htparam WHERE htparam.paramnr = h-artikel.service-code NO-LOCK. 
        IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
          serv = htparam.fdecimal / 100. 
      END. 
      IF h-artikel.mwst-code NE 0 THEN 
      DO: 
        FIND FIRST htparam WHERE htparam.paramnr = h-artikel.mwst-code NO-LOCK. 
        IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
        DO: 
          vat = htparam.fdecimal / 100. 
          IF serv-vat THEN vat = vat + vat * serv. 
          vat = round(vat, 2). 
        END. 
      END. 
 
      fact = 1.00 + serv + vat. 
 */
      serv = 0. 
      vat = 0. 
      FOR EACH h-umsatz WHERE h-umsatz.artnr = h-artikel.artnr 
        AND h-umsatz.departement = h-artikel.departement 
        AND h-umsatz.datum GE from-date AND h-umsatz.datum LE to-date 
        NO-LOCK BY h-umsatz.datum: 
          RUN calc-servvat.p(h-umsatz.departement, h-umsatz.artnr, h-umsatz.datum, h-artikel.service-code, 
             h-artikel.mwst-code, OUTPUT serv, OUTPUT vat).
        fact = 1.00 + serv + vat. 

        IF NOT it-exist THEN 
        DO: 
          it-exist = YES. 
          create cl-list. 
          cl-list.artnr = h-umsatz.artnr. 
          cl-list.dept = h-umsatz.departement. 
          cl-list.bezeich = h-artikel.bezeich. 
        END. 
        IF h-umsatz.datum = to-date THEN 
        DO: 
          cl-list.dnet = h-umsatz.betrag / fact. 
          cl-list.dgros = h-umsatz.betrag. 
          dnet = dnet + cl-list.dnet. 
          dgros = dgros + cl-list.dgros. 
        END. 
        cl-list.mnet = cl-list.mnet + h-umsatz.betrag / fact. 
        cl-list.mgros = cl-list.mgros + h-umsatz.betrag. 
        cl-list.mqty = cl-list.mqty + h-umsatz.anzahl. 
        mnet = mnet + h-umsatz.betrag / fact. 
        mgros = mgros + h-umsatz.betrag. 
        mqty = mqty + h-umsatz.anzahl. 
      END. 
    END. 
    FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num: 
      IF dnet NE 0 THEN cl-list.proz1 = cl-list.dnet / dnet * 100. 
      IF dgros NE 0 THEN cl-list.proz2 = cl-list.dgros / dgros * 100. 
      cl-list.proz3 = cl-list.mnet / mnet * 100. 
      cl-list.proz4 = cl-list.mgros / mgros * 100. 
    END. 
    create cl-list. 
    cl-list.flag = "**". 
    cl-list.bezeich = "T O T A L". 
    cl-list.dnet = dnet. 
    IF dnet NE 0 THEN cl-list.proz1 = 100. 
    cl-list.dgros = dgros. 
    IF dgros NE 0 THEN cl-list.proz2 = 100. 
    cl-list.mnet = mnet. 
    cl-list.proz3 = 100. 
    cl-list.mgros = mgros. 
    cl-list.proz4 = 100. 
    cl-list.mqty = mqty. 
  END. 
 
  FOR EACH cl-list NO-LOCK: 
    IF cl-list.flag = "*" THEN 
    DO: 
      create output-list. 
      output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") + STRING(cl-list.bezeich, "x(24)"). 
    END. 
    ELSE IF cl-list.flag = "" THEN 
    DO: 
        do-it = NO. 
        IF detailed OR cl-list.mgros NE 0 THEN do-it = YES. 
        IF do-it THEN 
        DO: 
          CREATE output-list. 
          output-list.mqty = cl-list.mqty. 
          IF NOT long-digit THEN 
          DO:
            output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->>,>>>,>>9.99") 
                                + STRING(cl-list.dgros, "->>,>>>,>>9.99").
            IF cl-list.proz2 GT 999 OR cl-list.proz2 LT -999 THEN
            output-list.str = output-list.str + STRING(cl-list.proz2, "->>,>>9").
            ELSE
            output-list.str = output-list.str + STRING(cl-list.proz2, "->>9.99").                             
            output-list.str = output-list.str
                                + STRING(cl-list.mnet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.mgros, "->>>,>>>,>>9.99").
            IF cl-list.proz4 GT 999 OR cl-list.proz4 LT -999 THEN
            output-list.str = output-list.str + STRING(cl-list.proz4, "->>,>>9").
            ELSE
            output-list.str = output-list.str + STRING(cl-list.proz4, "->>9.99"). 
          END.
          ELSE output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->,>>>,>>>,>>9") 
                                + STRING(cl-list.dgros, "->,>>>,>>>,>>9")
                                + STRING(cl-list.proz2, "->>9.99") 
                                + STRING(cl-list.mnet, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.mgros, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.proz4, "->>9.99"). 
        END. 
    END. 
    ELSE IF cl-list.flag = "**" THEN 
    DO: 
      create output-list. 
      output-list.mqty = cl-list.mqty. 
      IF NOT long-digit THEN 
      DO:
        output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->>,>>>,>>9.99") 
                                + STRING(cl-list.dgros, "->>,>>>,>>9.99").
        IF cl-list.proz2 GT 999 OR cl-list.proz2 LT -999 THEN
        output-list.str = output-list.str + STRING(cl-list.proz2, "->>,>>9").
        ELSE
        output-list.str = output-list.str + STRING(cl-list.proz2, "->>9.99").                             
        output-list.str = output-list.str
                                + STRING(cl-list.mnet, "->>>,>>>,>>9.99") 
                                + STRING(cl-list.mgros, "->>>,>>>,>>9.99").
        IF cl-list.proz4 GT 999 OR cl-list.proz4 LT -999 THEN
        output-list.str = output-list.str + STRING(cl-list.proz4, "->>,>>9").
        ELSE
        output-list.str = output-list.str + STRING(cl-list.proz4, "->>9.99"). 
      END.
      ELSE output-list.str = STRING(cl-list.artnr, ">>>>>>>>>") 
                                + STRING(cl-list.bezeich, "x(24)") 
                                + STRING(cl-list.dnet, "->,>>>,>>>,>>9") 
                                + STRING(cl-list.dgros, "->,>>>,>>>,>>9") 
                                + STRING(cl-list.proz2, "->>9.99") 
                                + STRING(cl-list.mnet, "->>,>>>,>>>,>>9") 
                                + STRING(cl-list.mgros, "->>,>>>,>>>,>>9") 
                               + STRING(cl-list.proz4, "->>9.99"). 
       create output-list. 
    END. 
  END. 
END. 
