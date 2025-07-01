DEFINE TEMP-TABLE s-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD artnr AS INTEGER FORMAT ">>>>>>>" LABEL "  ArtNo" 
  FIELD bezeich AS CHAR FORMAT "x(24)" LABEL "Description" 
  FIELD munit AS CHAR FORMAT "x(3)" LABEL "Unit" 
  FIELD qty1 AS DECIMAL 
  FIELD val1 AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "  Amount-(Recipe)" 
  FIELD qty2 AS DECIMAL 
  FIELD val2 AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "  Amount-(Actual)" 
  FIELD d-qty AS DECIMAL 
  FIELD d-val AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "       Variance" 
  FIELD s-qty1 AS CHAR FORMAT "x(13)" LABEL " Qty-(Recipe)" 
  FIELD s-qty2 AS CHAR FORMAT "x(13)" LABEL " Qty-(Actual)" 
  FIELD s-qty3 AS CHAR FORMAT "x(13)" LABEL "     Variance". 

DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER incl-bf    AS LOGICAL.
DEF INPUT  PARAMETER incl-fb    AS LOGICAL.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER f-eknr     AS INT.
DEF INPUT  PARAMETER b-eknr     AS INT.
DEF INPUT  PARAMETER fL-eknr    AS INT.
DEF INPUT  PARAMETER bL-eknr    AS INT.
DEF INPUT  PARAMETER preis-typ  AS INT.
DEF INPUT  PARAMETER food-bev   AS CHAR.
DEF INPUT  PARAMETER bev-food   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR s-list.

IF sorttype = 1 AND NOT incl-bf THEN RUN create-list1. 
ELSE IF sorttype = 1 AND incl-bf THEN RUN create-list11. 
ELSE IF sorttype = 2 AND NOT incl-fb THEN RUN create-list2. 
ELSE IF sorttype = 2 AND incl-fb THEN RUN create-list22. 


/**********************************************************/
PROCEDURE create-list1: 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE t-val1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val2 AS DECIMAL INITIAL 0. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  DO datum = from-date TO to-date: 
    FOR EACH h-cost WHERE h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-cost.artnr 
      AND h-artikel.departement = h-cost.departement 
      AND (h-artikel.artnrlager NE 0 OR h-artikel.artnrrezept NE 0) NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
      AND artikel.departement = h-artikel.departement 
   /* AND artikel.endkum = f-eknr */ NO-LOCK BY h-artikel.bezeich: 
 
      IF h-artikel.artnrlager NE 0 AND artikel.endkum = f-eknr THEN 
      DO: 
        FIND FIRST l-artikel WHERE l-artikel.artnr = h-artikel.artnrlager 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE l-artikel THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.artnr = l-artikel.artnr. 
            s-list.bezeich = l-artikel.bezeich. 
/* 
            IF l-artikel.inhalt NE 1 THEN 
              s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
            ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
            s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
          END. 
          s-list.qty1 = s-list.qty1 + h-cost.anzahl. 
          s-list.val1 = s-list.val1 + h-cost.anzahl * h-cost.betrag. 
        END. 
      END. 
      ELSE IF h-artikel.artnrrezept NE 0 THEN 
      DO: 
        FIND FIRST h-rezept WHERE 
          h-rezept.artnrrezept = h-artikel.artnrrezept NO-LOCK NO-ERROR. 
        IF AVAILABLE h-rezept THEN 
          RUN recipe-bdown(h-rezept.artnrrezept, INPUT h-cost.anzahl). 
      END. 
    END. 
  END. 
  RUN create-food. 
 
  FOR EACH s-list: 
    IF s-list.qty1 = 0 AND s-list.qty2 = 0 THEN delete s-list. 
    ELSE 
    DO: 
      s-list.d-qty = s-list.qty2 - s-list.qty1. 
      s-list.d-val = s-list.val2 - s-list.val1. 
      s-list.s-qty1 = STRING(s-list.qty1, "->,>>>,>>9.99"). 
      s-list.s-qty2 = STRING(s-list.qty2, "->,>>>,>>9.99"). 
      s-list.s-qty3 = STRING(s-list.d-qty, "->,>>>,>>9.99"). 
      t-val1 = t-val1 + s-list.val1. 
      t-val2 = t-val2 + s-list.val2. 
    END. 
  END. 
  create s-list. 
  s-list.flag = 2. 
  s-list.bezeich = "T O T A L". 
  s-list.val1 = t-val1. 
  s-list.val2 = t-val2. 
  s-list.d-val = t-val2 - t-val1. 
 
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 

PROCEDURE create-list11: 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE t-val1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val2 AS DECIMAL INITIAL 0. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  DO datum = from-date TO to-date: 
    FOR EACH h-cost WHERE h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-cost.artnr 
      AND h-artikel.departement = h-cost.departement 
      AND (h-artikel.artnrlager NE 0 OR h-artikel.artnrrezept NE 0) NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
      AND artikel.departement = h-artikel.departement 
      AND artikel.endkum = f-eknr NO-LOCK BY h-artikel.bezeich: 
 
      IF h-artikel.artnrlager NE 0 THEN 
      DO: 
        FIND FIRST l-artikel WHERE l-artikel.artnr = h-artikel.artnrlager 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE l-artikel THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.artnr = l-artikel.artnr. 
            s-list.bezeich = l-artikel.bezeich. 
/* 
            IF l-artikel.inhalt NE 1 THEN 
              s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
            ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
            s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
          END. 
          s-list.qty1 = s-list.qty1 + h-cost.anzahl. 
          s-list.val1 = s-list.val1 + h-cost.anzahl * h-cost.betrag. 
        END. 
      END. 
      ELSE IF h-artikel.artnrrezept NE 0 THEN 
      DO: 
        FIND FIRST h-rezept WHERE 
          h-rezept.artnrrezept = h-artikel.artnrrezept NO-LOCK NO-ERROR. 
        IF AVAILABLE h-rezept THEN 
          RUN recipe-bdown1(h-rezept.artnrrezept, INPUT h-cost.anzahl). 
      END. 
    END. 
  END. 
  RUN create-food1. 
 
  FOR EACH s-list: 
    IF s-list.qty1 = 0 AND s-list.qty2 = 0 THEN delete s-list. 
    ELSE 
    DO: 
      s-list.d-qty = s-list.qty2 - s-list.qty1. 
      s-list.d-val = s-list.val2 - s-list.val1. 
      s-list.s-qty1 = STRING(s-list.qty1, "->,>>>,>>9.99"). 
      s-list.s-qty2 = STRING(s-list.qty2, "->,>>>,>>9.99"). 
      s-list.s-qty3 = STRING(s-list.d-qty, "->,>>>,>>9.99"). 
      t-val1 = t-val1 + s-list.val1. 
      t-val2 = t-val2 + s-list.val2. 
    END. 
  END. 
  create s-list. 
  s-list.flag = 2. 
  s-list.bezeich = "T O T A L". 
  s-list.val1 = t-val1. 
  s-list.val2 = t-val2. 
  s-list.d-val = t-val2 - t-val1. 
 
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 

PROCEDURE create-list2: 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE t-val1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val2 AS DECIMAL INITIAL 0. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  DO datum = from-date TO to-date: 
    FOR EACH h-cost WHERE h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-cost.artnr 
      AND h-artikel.departement = h-cost.departement 
      AND (h-artikel.artnrlager NE 0 OR h-artikel.artnrrezept NE 0) NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
      AND artikel.departement = h-artikel.departement 
   /* AND artikel.endkum = b-eknr */ NO-LOCK BY h-artikel.bezeich: 
 
      IF h-artikel.artnrlager NE 0 AND artikel.endkum = b-eknr THEN 
      DO: 
        FIND FIRST l-artikel WHERE l-artikel.artnr = h-artikel.artnrlager 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE l-artikel THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.artnr = l-artikel.artnr. 
            s-list.bezeich = l-artikel.bezeich. 
/* 
            IF l-artikel.inhalt NE 1 THEN 
              s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
            ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
            s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
          END. 
          s-list.qty1 = s-list.qty1 + h-cost.anzahl. 
          s-list.val1 = s-list.val1 + h-cost.anzahl * h-cost.betrag. 
        END. 
      END. 
      ELSE IF h-artikel.artnrrezept NE 0 THEN 
      DO: 
        FIND FIRST h-rezept WHERE 
          h-rezept.artnrrezept = h-artikel.artnrrezept NO-LOCK NO-ERROR. 
        IF AVAILABLE h-rezept THEN 
          RUN recipe-bdown(h-rezept.artnrrezept, INPUT h-cost.anzahl). 
      END. 
    END. 
  END. 
  RUN create-beverage. 
  FOR EACH s-list: 
    IF s-list.qty1 = 0 AND s-list.qty2 = 0 THEN delete s-list. 
    ELSE 
    DO: 
      s-list.d-qty = s-list.qty2 - s-list.qty1. 
      s-list.d-val = s-list.val2 - s-list.val1. 
      s-list.s-qty1 = STRING(s-list.qty1, "->,>>>,>>9.99"). 
      s-list.s-qty2 = STRING(s-list.qty2, "->,>>>,>>9.99"). 
      s-list.s-qty3 = STRING(s-list.d-qty, "->,>>>,>>9.99"). 
      t-val1 = t-val1 + s-list.val1. 
      t-val2 = t-val2 + s-list.val2. 
    END. 
  END. 
  create s-list. 
  s-list.flag = 2. 
  s-list.bezeich = "T O T A L". 
  s-list.val1 = t-val1. 
  s-list.val2 = t-val2. 
  s-list.d-val = t-val2 - t-val1. 
 
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 

PROCEDURE create-list22: 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE t-val1 AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-val2 AS DECIMAL INITIAL 0. 
 
  FOR EACH s-list: 
    delete s-list. 
  END. 
 
  DO datum = from-date TO to-date: 
    FOR EACH h-cost WHERE h-cost.datum = datum AND h-cost.flag = 1 NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-cost.artnr 
      AND h-artikel.departement = h-cost.departement 
      AND (h-artikel.artnrlager NE 0 OR h-artikel.artnrrezept NE 0) NO-LOCK, 
      FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
      AND artikel.departement = h-artikel.departement 
      AND artikel.endkum = b-eknr NO-LOCK BY h-artikel.bezeich: 
 
      IF h-artikel.artnrlager NE 0 THEN 
      DO: 
        FIND FIRST l-artikel WHERE l-artikel.artnr = h-artikel.artnrlager 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE l-artikel THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.artnr = l-artikel.artnr. 
            s-list.bezeich = l-artikel.bezeich. 
/* 
            IF l-artikel.inhalt NE 1 THEN 
              s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
            ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
            s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
              + l-artikel.masseinheit. 
          END. 
          s-list.qty1 = s-list.qty1 + h-cost.anzahl. 
          s-list.val1 = s-list.val1 + h-cost.anzahl * h-cost.betrag. 
        END. 
      END. 
      ELSE IF h-artikel.artnrrezept NE 0 THEN 
      DO: 
        FIND FIRST h-rezept WHERE 
          h-rezept.artnrrezept = h-artikel.artnrrezept NO-LOCK NO-ERROR. 
        IF AVAILABLE h-rezept THEN 
          RUN recipe-bdown1(h-rezept.artnrrezept, INPUT h-cost.anzahl). 
      END. 
    END. 
  END. 
  RUN create-beverage1. 
  FOR EACH s-list: 
    IF s-list.qty1 = 0 AND s-list.qty2 = 0 THEN delete s-list. 
    ELSE 
    DO: 
      s-list.d-qty = s-list.qty2 - s-list.qty1. 
      s-list.d-val = s-list.val2 - s-list.val1. 
      s-list.s-qty1 = STRING(s-list.qty1, "->,>>>,>>9.99"). 
      s-list.s-qty2 = STRING(s-list.qty2, "->,>>>,>>9.99"). 
      s-list.s-qty3 = STRING(s-list.d-qty, "->,>>>,>>9.99"). 
      t-val1 = t-val1 + s-list.val1. 
      t-val2 = t-val2 + s-list.val2. 
    END. 
  END. 
  create s-list. 
  s-list.flag = 2. 
  s-list.bezeich = "T O T A L". 
  s-list.val1 = t-val1. 
  s-list.val2 = t-val2. 
  s-list.d-val = t-val2 - t-val1. 
 
  /*MThide FRAME frame2 NO-PAUSE.*/
END. 

PROCEDURE recipe-bdown: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE buffer h-recipe FOR h-rezept. 
  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    inh = menge * h-rezlin.menge / h-recipe.portion. 
    IF h-rezlin.recipe-flag = YES THEN 
      RUN recipe-bdown(h-rezlin.artnrlager, inh). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel AND 
      (((l-artikel.endkum = fL-eknr) AND (sorttype = 1)) OR 
       ((l-artikel.endkum = bL-eknr) AND (sorttype = 2))) THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.artnr = l-artikel.artnr. 
          s-list.bezeich = l-artikel.bezeich. 
/* 
          IF l-artikel.inhalt NE 1 THEN 
            s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
          ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
          s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
        END. 
 
        s-list.qty1 = s-list.qty1 + inh / l-artikel.inhalt. 
        IF preis-typ = 0 OR l-artikel.ek-aktuell EQ 0 THEN 
        s-list.val1 = s-list.val1 + inh / l-artikel.inhalt 
          * l-artikel.vk-preis / (1 - h-rezlin.lostfact / 100). 
        ELSE 
        s-list.val1 = s-list.val1 + inh / l-artikel.inhalt 
          * l-artikel.ek-aktuell / (1 - h-rezlin.lostfact / 100). 
      END. 
    END. 
  END. 
END. 

PROCEDURE create-food: 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = fl-eknr NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 
 
/*** Add Food TO Beverage ***/ 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = food-bev NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    /* AND l-artikel.endkum = fl-eknr */ NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 

  /*ITA --> menghitung nilai dari fibukonto yang bersifat cost*/
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto NE food-bev
    AND l-ophdr.fibukonto NE "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    /* AND l-artikel.endkum = fl-eknr */ NO-LOCK: 

    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto
        AND gl-acct.acc-type = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN DO:
        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.artnr = l-artikel.artnr. 
          s-list.bezeich = l-artikel.bezeich. 
          s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
        END. 
        s-list.qty2 = s-list.qty2 + l-op.anzahl. 
        s-list.val2 = s-list.val2 + l-op.warenwert. 
    END.
  END. 
  /*end*/
END. 

PROCEDURE recipe-bdown1: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE buffer h-recipe FOR h-rezept. 
  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    inh = menge * h-rezlin.menge / h-recipe.portion. 
    IF h-rezlin.recipe-flag = YES THEN 
      RUN recipe-bdown1(h-rezlin.artnrlager, inh). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel /* AND 
      (((l-artikel.endkum = fL-eknr) AND (sorttype = 1)) OR 
       ((l-artikel.endkum = bL-eknr) AND (sorttype = 2))) */ THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.artnr = l-artikel.artnr. 
          s-list.bezeich = l-artikel.bezeich. 
/* 
          IF l-artikel.inhalt NE 1 THEN 
            s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
          ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
          s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
        END. 
 
        s-list.qty1 = s-list.qty1 + inh / l-artikel.inhalt. 
        IF preis-typ = 0 OR l-artikel.ek-aktuell EQ 0 THEN 
        s-list.val1 = s-list.val1 + inh / l-artikel.inhalt 
          * l-artikel.vk-preis / (1 - h-rezlin.lostfact / 100). 
        ELSE 
        s-list.val1 = s-list.val1 + inh / l-artikel.inhalt 
          * l-artikel.ek-aktuell / (1 - h-rezlin.lostfact / 100). 
      END. 
    END. 
  END. 
END. 

PROCEDURE create-beverage1: 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = bl-eknr NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr 
      AND s-list.flag = 0 NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 
 
/*** Add Food TO Beverage ***/ 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = food-bev NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    /* AND l-artikel.endkum = fl-eknr */ NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr 
      AND s-list.flag = 1 NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.flag = 1. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 

  /*ITA --> menghitung nilai dari fibukonto yang bersifat cost*/
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto NE food-bev
    AND l-ophdr.fibukonto NE "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK: 

    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto
        AND gl-acct.acc-type = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN DO:
        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.artnr = l-artikel.artnr. 
          s-list.bezeich = l-artikel.bezeich. 
          s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
        END. 
        s-list.qty2 = s-list.qty2 + l-op.anzahl. 
        s-list.val2 = s-list.val2 + l-op.warenwert. 
    END.
  END. 
  /*end*/
END. 

PROCEDURE create-food1: 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = fl-eknr NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr 
      AND s-list.flag = 0 NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 
 
/*** Add Beverage TO Food ***/ 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = bev-food NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    /* AND l-artikel.endkum = bl-eknr */ NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr 
      AND s-list.flag = 1 NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.flag = 1. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 

  /*ITA --> menghitung nilai dari fibukonto yang bersifat cost*/
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto NE bev-food
    AND l-ophdr.fibukonto NE "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK: 

    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto
        AND gl-acct.acc-type = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN DO:
        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.artnr = l-artikel.artnr. 
          s-list.bezeich = l-artikel.bezeich. 
          s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
        END. 
        s-list.qty2 = s-list.qty2 + l-op.anzahl. 
        s-list.val2 = s-list.val2 + l-op.warenwert. 
    END.
  END. 
  /*end*/
END. 

PROCEDURE create-beverage: 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = bl-eknr NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr 
      NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 
 
/*** Add Beverage TO Beverage ***/ 
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto = bev-food NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = fl-eknr NO-LOCK: 
    FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.artnr = l-artikel.artnr. 
      s-list.bezeich = l-artikel.bezeich. 
/* 
      IF l-artikel.inhalt NE 1 THEN 
        s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
      ELSE s-list.munit = l-artikel.masseinheit. 
*/ 
      s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
        + l-artikel.masseinheit. 
    END. 
    s-list.qty2 = s-list.qty2 + l-op.anzahl. 
    s-list.val2 = s-list.val2 + l-op.warenwert. 
  END. 

  /*ITA --> menghitung nilai dari fibukonto yang bersifat cost*/
  FOR EACH l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.datum GE from-date AND l-ophdr.datum LE to-date 
    AND l-ophdr.fibukonto NE bev-food
    AND l-ophdr.fibukonto NE "0000000000" NO-LOCK, 
    EACH l-op WHERE l-op.lscheinnr = l-ophdr.lscheinnr 
    AND l-op.loeschflag LE 1 AND l-op.op-art = 3 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK: 

    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto
        AND gl-acct.acc-type = 2 NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN DO:
        FIND FIRST s-list WHERE s-list.artnr = l-artikel.artnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.artnr = l-artikel.artnr. 
          s-list.bezeich = l-artikel.bezeich. 
          s-list.munit = TRIM(STRING(l-artikel.inhalt,">>,>>9")) + " " 
            + l-artikel.masseinheit. 
        END. 
        s-list.qty2 = s-list.qty2 + l-op.anzahl. 
        s-list.val2 = s-list.val2 + l-op.warenwert. 
    END.
  END. 
  /*end*/
END. 
