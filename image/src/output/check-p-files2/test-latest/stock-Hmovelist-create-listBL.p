
DEF TEMP-TABLE str-list
    FIELD s AS CHAR FORMAT "x(135)".

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER s-artnr AS INT.
DEF INPUT  PARAMETER mm AS INT.
DEF INPUT  PARAMETER yy AS INT.
DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager AS INT.
DEF INPUT  PARAMETER show-price AS LOGICAL.

DEF OUTPUT PARAMETER anfDate     AS DATE NO-UNDO.
DEF OUTPUT PARAMETER endDate     AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR str-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fb-flash1".

DEFINE VARIABLE tot-anz         AS DECIMAL. 
DEFINE VARIABLE tot-val         AS DECIMAL. 
DEFINE VARIABLE t-anz           AS DECIMAL. 
DEFINE VARIABLE t-val           AS DECIMAL. 
DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

RUN create-list.

PROCEDURE create-list:
DEFINE VARIABLE t-qty       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-wert      AS DECIMAL INITIAL 0. 
DEFINE VARIABLE bemerk      AS CHAR. 
DEFINE VARIABLE preis       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE wert        AS DECIMAL INITIAL 0. 
DEFINE BUFFER usr      FOR bediener.
DEFINE BUFFER l-op1    FOR vhp.l-ophis. 
DEFINE BUFFER l-oh     FOR l-besthis. 
  
  ASSIGN
    anfDate = DATE(mm, 1, yy)
    endDate = anfDate + 31
    endDate = DATE(MONTH(endDate), 1, YEAR(endDate)) - 1
  .
  FIND FIRST l-oh WHERE l-oh.artnr = s-artnr 
    AND l-oh.lager-nr = 0 
    AND l-oh.anf-best-dat = anfDate NO-LOCK NO-ERROR. 
  IF AVAILABLE l-oh THEN 
  DO: 
    t-qty  = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
    IF show-price THEN 
      t-wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-val = 0. 
  FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
 
    FIND FIRST l-besthis WHERE l-besthis.lager-nr = l-lager.lager-nr 
      AND l-besthis.artnr = s-artnr 
      AND l-besthis.anf-best-dat = anfDate NO-LOCK NO-ERROR. 
    IF AVAILABLE l-besthis THEN 
    DO: 
      t-anz = l-besthis.anz-anf-best. 
      IF show-price THEN t-val = l-besthis.val-anf-best. 
      CREATE str-list. 
      str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
        + " " + STRING(l-lager.bezeich, "x(13)"). 
 
      CREATE str-list. 
      IF show-price THEN 
      DO: 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-besthis.anf-best-dat) 
             + STRING(" ", "x(16)") 
             + STRING(l-besthis.anz-anf-best, "->>>,>>9.99") 
             + STRING(l-besthis.val-anf-best, "->>>,>>>,>>9.99"). 
        ELSE str-list.s = STRING(l-besthis.anf-best-dat) 
             + STRING(" ", "x(16)") 
             + STRING(l-besthis.anz-anf-best, "->>>,>>9.99") 
             + STRING(l-besthis.val-anf-best, "->>,>>>,>>>,>>9"). 
      END. 
      ELSE 
      DO: 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-besthis.anf-best-dat) 
             + STRING(" ", "x(16)") 
             + STRING(l-besthis.anz-anf-best, "->>>,>>9.99") 
             + STRING(0, "->>>,>>>,>>9.99"). 
        ELSE str-list.s = STRING(l-besthis.anf-best-dat) 
             + STRING(" ", "x(16)") 
             + STRING(l-besthis.anz-anf-best, "->>>,>>9.99") 
             + STRING(0, "->>,>>>,>>>,>>9"). 
      END. 
    END. 
 
/*  calculate the incoming- AND outgoing stocks within the given periods */ 
    /*MTIF CONNECTED ("vhparch") THEN
    DO:
        RUN stockHmov-arch.p(l-lager.lager-nr, s-artnr, anfDate, endDate,
            show-price, t-anz, t-val, long-digit).
    END.
    ELSE
    DO:*/
        FOR EACH vhp.l-ophis WHERE vhp.l-ophis.lager-nr = l-lager.lager-nr 
            AND vhp.l-ophis.artnr = s-artnr
            AND vhp.l-ophis.datum GE anfDate
            AND vhp.l-ophis.datum LE endDate 
            AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*"
            NO-LOCK BY vhp.l-ophis.datum BY vhp.l-ophis.op-art: 
          IF show-price THEN 
          DO: 
            preis = vhp.l-ophis.einzelpreis. 
            wert = vhp.l-ophis.warenwert. 
          END. 
     
          IF vhp.l-ophis.op-art = 1 THEN 
          DO: 
            bemerk = "". 
            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE l-lieferant THEN bemerk = l-lieferant.firma. 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + wert. 
            CREATE str-list. 
            RUN  add-id.
            str-list.s = STRING(vhp.l-ophis.datum) 
                 + STRING(vhp.l-ophis.lscheinnr, "x(16)") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99") 
                 + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(0, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>9.99") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(bemerk, "x(16)"). 
          END. 
     /* herkunftflag = 1: to stora, 2: direct issue, 3: transform, 4: adjustment*/
          ELSE IF vhp.l-ophis.op-art = 2 THEN 
          DO: 
            FIND FIRST l-op1 WHERE l-op1.op-art = 4 AND l-op1.datum = vhp.l-ophis.datum 
                AND l-op1.artnr = vhp.l-ophis.artnr AND l-op1.anzahl = vhp.l-ophis.anzahl 
                AND l-op1.lief-nr = vhp.l-ophis.lager-nr NO-LOCK NO-ERROR. 
            IF AVAILABLE l-op1 THEN 
                bemerk = translateExtended ("From",lvCAREA,"") + " " + STRING(l-op1.lager-nr). 
            ELSE bemerk = translateExtended ("Transferred",lvCAREA,""). 
            t-anz = t-anz + vhp.l-ophis.anzahl. 
            t-val = t-val + wert. 
            CREATE str-list. 
            RUN add-id.
            str-list.s = STRING(vhp.l-ophis.datum) 
                 + STRING(vhp.l-ophis.lscheinnr, "x(16)") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99") 
                 + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(0, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>9.99") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(bemerk, "x(16)"). 
          END. 
     
          ELSE IF vhp.l-ophis.op-art = 3 THEN 
          DO: 
            IF vhp.l-ophis.fibukonto NE "" THEN 
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = vhp.l-ophis.fibukonto 
                NO-LOCK NO-ERROR. 
            ELSE 
            DO: 
              FIND FIRST vhp.l-ophhis WHERE vhp.l-ophhis.op-typ = "STT" 
                AND vhp.l-ophhis.datum = vhp.l-ophis.datum 
                AND vhp.l-ophhis.lscheinnr = vhp.l-ophis.lscheinnr 
                AND vhp.l-ophhis.fibukonto NE "" NO-LOCK NO-ERROR. 
              IF AVAILABLE vhp.l-ophhis THEN FIND FIRST gl-acct WHERE 
                gl-acct.fibukonto = vhp.l-ophhis.fibukonto NO-LOCK NO-ERROR. 
            END. 
            bemerk = "". 
            IF AVAILABLE gl-acct THEN bemerk = gl-acct.fibukonto. 
            t-anz = t-anz - vhp.l-ophis.anzahl. 
            t-val = t-val - wert. 
            CREATE str-list. 
            RUN add-id.
            IF NOT long-digit THEN 
            str-list.s = STRING(vhp.l-ophis.datum) 
                 + STRING(vhp.l-ophis.lscheinnr, "x(16)") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99") 
                 + STRING(0, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>9.99") 
                 + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(bemerk, "x(16)"). 
            ELSE str-list.s = STRING(vhp.l-ophis.datum) 
                 + STRING(vhp.l-ophis.lscheinnr, "x(16)") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(0, "   ->>>,>>>,>>9") 
                 + STRING(0, "->,>>>,>>9.99") 
                 + STRING(0, "->,>>>,>>>,>>9") 
                 + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.99") 
                 + STRING(wert, "->,>>>,>>>,>>9") 
                 + STRING(0, "->>,>>>,>>9") 
                 + STRING(bemerk, "x(16)"). 
          END. 
     
          ELSE IF vhp.l-ophis.op-art = 4 THEN 
          DO: 
            bemerk = translateExtended ("To Store",lvCAREA,"") 
                + " " + STRING(vhp.l-ophis.lief-nr). 
            t-anz = t-anz - vhp.l-ophis.anzahl. 
            t-val = t-val - wert. 
            CREATE str-list. 
            RUN add-id.
            str-list.s = STRING(vhp.l-ophis.datum) 
                 + STRING(vhp.l-ophis.lscheinnr, "x(16)") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99") 
                 + STRING(0, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>9.99") 
                 + STRING(vhp.l-ophis.anzahl, "->,>>>,>>9.99") 
                 + STRING(wert, "->>,>>>,>>9.99") 
                 + STRING(0, "->>>,>>9.99") 
                 + STRING(bemerk, "x(16)"). 
          END. 
        END.   
    /*MTEND.*/

    
    IF AVAILABLE l-besthis THEN 
    DO: 
      tot-anz = tot-anz + t-anz. 
      tot-val = tot-val + t-val. 
      CREATE str-list. 
      IF NOT long-digit THEN 
      str-list.s = "        " 
               + STRING(translateExtended ("Stock Onhand:",lvCAREA,""),"x(16)") 
               + STRING(t-anz, "->>>,>>9.99") 
               + STRING(t-val, "->>>,>>>,>>9.99"). 
      ELSE 
      str-list.s = "        "
               + STRING(translateExtended ("Stock Onhand:",lvCAREA,""),"x(16)") 
               + STRING(t-anz, "->>>,>>9.99") 
               + STRING(t-val, "   ->>>,>>>,>>9"). 
      CREATE str-list. 
    END. 
  END. 
  CREATE str-list. 
  CREATE str-list. 
  
  str-list.s = "        " + "T O T A L :     " 
             + STRING(t-qty, "->>>,>>9.99") 
             + STRING(t-wert, "->>>,>>>,>>9.99").
             
  /*MTstr-list.s = "        " + "T O T A L :     " 
             + STRING(tot-anz, "->>>,>>9.99") 
             + STRING(tot-val, "->>>,>>>,>>9.99").*/
END. 

PROCEDURE add-id:
    DEFINE BUFFER usr FOR bediener.
/*
    FIND FIRST usr WHERE usr.nr = vhp.l-ophis.fuellflag NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN
    DO:
        str-list.ID = usr.userinit.
    END.
    ELSE str-list.ID = "??".
*/
END.
