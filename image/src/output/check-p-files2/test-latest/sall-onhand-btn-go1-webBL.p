DEFINE TEMP-TABLE str-list
  FIELD flag AS INTEGER 
  FIELD s AS CHAR FORMAT "x(135)". 

DEFINE TEMP-TABLE soh-list
	  FIELD artnr		      AS INTEGER FORMAT "9999999"
    FIELD bezeich	      AS CHARACTER
    FIELD unit     	    AS CHARACTER
    FIELD act-qty  	    AS DECIMAL FORMAT "->>,>>9.99"
    FIELD act-val  	    AS DECIMAL  FORMAT "->>,>>>,>>9.99"
    FIELD cont1         AS CHARACTER
    FIELD d-unit        AS CHARACTER
    FIELD cont2         AS CHARACTER
    FIELD last-price    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD act-price     AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD avrg-price    AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD min-oh        AS DECIMAL
    FIELD must-order    AS DECIMAL
    .  

DEFINE TEMP-TABLE output-list
    FIELD flag          AS INTEGER
	  FIELD artnr		      AS INTEGER FORMAT "9999999"
    FIELD bezeich	      AS CHARACTER
    FIELD unit     	    AS CHARACTER
    FIELD act-qty  	    AS DECIMAL FORMAT "->>,>>9.99"
    FIELD act-val  	    AS DECIMAL  FORMAT "->>,>>>,>>9.99"
    FIELD cont1         AS CHARACTER
    FIELD d-unit        AS CHARACTER
    FIELD cont2         AS CHARACTER
    FIELD last-price    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD act-price     AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD avrg-price    AS DECIMAL  FORMAT "->>>,>>>,>>9.99"
    FIELD min-oh        AS DECIMAL
    FIELD must-order    AS DECIMAL
    .  

DEF INPUT  PARAMETER all-flag   AS LOGICAL.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF INPUT  PARAMETER zero-flag  AS LOGICAL.
DEF INPUT  PARAMETER from-grp   AS INT.
DEF INPUT  PARAMETER sub-grp    AS INT.
DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager   AS INT.
DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER mattype    AS INT.
DEF INPUT  PARAMETER minoh-flag AS LOGICAL. /*FDL Dec 20, 2022 => 272C59*/
DEF OUTPUT PARAMETER TABLE FOR soh-list.

/* Local Testing 
DEF VAR all-flag   AS LOGICAL INIT NO.
DEF VAR show-price AS LOGICAL INIT YES.
DEF VAR zero-flag  AS LOGICAL INIT NO.
DEF VAR from-grp   AS INT INIT 0.
DEF VAR sub-grp    AS INT INIT 0.
DEF VAR from-lager AS INT INIT 1.      
DEF VAR to-lager   AS INT INIT 1.
DEF VAR sorttype   AS INT INIT 2.
DEF VAR mattype    AS INT INIT 0.
DEF VAR minoh-flag  AS LOGICAL INIT NO.
*/      
/* FD Comment
RUN sall-onhand-btn-gobl.p
    (all-flag, show-price, zero-flag, from-grp, sub-grp, from-lager, to-lager, sorttype, mattype, OUTPUT TABLE str-list).
*/

/* Malik Serverless 639 comment 
RUN sall-onhand-btn-go_1bl.p
    (all-flag, show-price, zero-flag, from-grp, sub-grp, 
     from-lager, to-lager, sorttype, mattype, minoh-flag,
     OUTPUT TABLE str-list). */

DEFINE VARIABLE curr-best AS DECIMAL.
DEFINE VARIABLE long-digit AS LOGICAL.

DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-val    AS DECIMAL. 
DEFINE VARIABLE t-anz      AS DECIMAL. 
DEFINE VARIABLE t-val      AS DECIMAL. 
DEFINE VARIABLE t-value    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE avrg-price AS DECIMAL. 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
DEFINE VARIABLE must-order AS DECIMAL.
 
DEFINE VARIABLE tt-val AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL.  
DEFINE VARIABLE tot-bezeich AS CHAR. 

DEFINE buffer l-oh FOR l-bestand.

/* Debugging 
message
  "masuk siniiii"
  view-as alert-box. */

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

/* ini yang dijalankan */
IF NOT all-flag THEN 
DO: 
    IF from-grp = 0 THEN RUN create-list. 
    ELSE RUN create-list1. 
END. 
ELSE 
DO: 
    IF from-grp = 0 THEN RUN create-listA. 
    ELSE RUN create-list1A. 
END. 

FOR EACH soh-list:
    DELETE soh-list.
END.

/* 
FOR EACH str-list:
    CREATE soh-list.
    ASSIGN             
        soh-list.artnr      = INTEGER(SUBSTR(str-list.s, 1, 7))
        soh-list.bezeich    = SUBSTR(str-list.s, 8, 50)
        soh-list.unit       = SUBSTR(str-list.s, 58, 3)
        soh-list.act-qty    = DECIMAL(SUBSTR(str-list.s, 129, 13)) 
        soh-list.act-val    = DECIMAL(SUBSTR(str-list.s, 142, 18)) 
        soh-list.cont1      = SUBSTR(str-list.s, 61, 9)        
        soh-list.d-unit     = SUBSTR(str-list.s, 70, 8)         
        soh-list.cont2      = SUBSTR(str-list.s, 78, 9)        
        soh-list.last-price = DECIMAL(SUBSTR(str-list.s, 87, 14))
        soh-list.act-price  = DECIMAL(SUBSTR(str-list.s, 101, 14))
        soh-list.avrg-price = DECIMAL(SUBSTR(str-list.s, 115, 14))
        soh-list.min-oh     = DECIMAL(SUBSTR(str-list.s, 160, 13))
        soh-list.must-order = DECIMAL(SUBSTR(str-list.s, 173, 13))
        .
END.*/

FOR EACH output-list:
  CREATE soh-list.
  ASSIGN             
      soh-list.artnr      = output-list.artnr
      soh-list.bezeich    = output-list.bezeich
      soh-list.unit       = output-list.unit
      soh-list.act-qty    = output-list.act-qty 
      soh-list.act-val    = output-list.act-val 
      soh-list.cont1      = output-list.cont1        
      soh-list.d-unit     = output-list.d-unit         
      soh-list.cont2      = output-list.cont2        
      soh-list.last-price = output-list.last-price
      soh-list.act-price  = output-list.act-price
      soh-list.avrg-price = output-list.avrg-price
      soh-list.min-oh     = output-list.min-oh
      soh-list.must-order = output-list.must-order
      .
END.

/*FOR EACH soh-list:
    DISP soh-list.
END.*/

/* Malik Serverless 639 Move Procedure from sall-onhand-btn-go_1bl.p
 to sall-onhand-btn-go1-webBL */

PROCEDURE create-list: 
  /*
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE j AS INTEGER. 
  DEFINE VARIABLE tot-anz    AS DECIMAL. 
  DEFINE VARIABLE tot-val    AS DECIMAL. 
  DEFINE VARIABLE t-anz      AS DECIMAL. 
  DEFINE VARIABLE t-val      AS DECIMAL. 
  DEFINE VARIABLE t-value    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE avrg-price AS DECIMAL. 
  DEFINE VARIABLE zwkum AS INTEGER. 
  DEFINE VARIABLE bezeich AS CHAR. 
  DEFINE VARIABLE must-order AS DECIMAL.
  
  DEFINE buffer l-oh FOR l-bestand. 
  DEFINE VARIABLE qty AS DECIMAL. 
  DEFINE VARIABLE wert AS DECIMAL. 
  DEFINE VARIABLE tot-bezeich AS CHAR. 
  DEFINE VARIABLE tt-val AS DECIMAL. 
  DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0.
  */ 
 
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  FOR EACH l-lager WHERE lager-nr GE from-lager 
    AND lager-nr LE to-lager: 
    tot-bezeich = "Ttl - " + l-lager.bezeich. 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    tt-val = 0. 
    IF sorttype = 1 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:
          /* debugging */
          message
            "masuk sini <<<<<"
            view-as alert-box.
          /* ini tidak dijalankan */        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                RUN create-lines.
            END.
          END.            
        END. /* End of add */
        ELSE        
        DO:     
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            /* Debugging (masuk sini)
            message
              "infoo <<<<<<"
              view-as alert-box. */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                RUN create-lines.
            END.
          END.                           
        END.
    END. 
    ELSE IF sorttype = 2 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:      
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich:

                RUN create-lines.
            END.
          END.            
        END. /* End of add */
        ELSE        
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                RUN create-lines.
            END.
          END.                          
        END.
    END.
    IF t-val NE 0 THEN 
    DO: 
      /* Malik Serverless 639 comment 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>>,>>9"). 
      create str-list. */
      CREATE output-list.
      ASSIGN
        output-list.flag    = 1
        /* output-list.artnr   = "       " */
        output-list.bezeich = bezeich
        output-list.act-val = t-val.
      CREATE output-list.  
    END. 
    /* Malik Serverless 639 comment 
    create str-list. 
    str-list.flag = 1. 
    str-list.s = "       ". 
    str-list.s = str-list.s + STRING(tot-bezeich, "x(50)"). 
    DO j = 1 TO 84: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
      str-list.s = str-list.s + STRING(tt-val, "->>,>>>,>>>,>>9.99"). 
    ELSE 
      str-list.s = str-list.s + STRING(tt-val, "->,>>>,>>>,>>>,>>9"). 

    create str-list.*/
    CREATE output-list.
    ASSIGN
      output-list.flag    = 1
      output-list.bezeich = tot-bezeich
      output-list.act-val = tt-val.
    CREATE output-list.  
  END. 

  /* Malik Serverless 639 comment 
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->,>>>,>>>,>>>,>>9"). */
  CREATE output-list.
  ASSIGN
    output-list.flag    = 1
    output-list.bezeich = "GRAND T O T A L"
    output-list.act-val = tt-value.
END. 
 
PROCEDURE create-listA: 
  /*DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE j AS INTEGER. 
  DEFINE VARIABLE tot-anz    AS DECIMAL. 
  DEFINE VARIABLE tot-val    AS DECIMAL. 
  DEFINE VARIABLE t-anz      AS DECIMAL. 
  DEFINE VARIABLE t-val      AS DECIMAL. 
  DEFINE VARIABLE t-value    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE avrg-price AS DECIMAL. 
  DEFINE VARIABLE zwkum AS INTEGER. 
  DEFINE VARIABLE bezeich AS CHAR. 
  DEFINE VARIABLE must-order AS DECIMAL.
  
  DEFINE buffer l-oh FOR l-bestand. 
  DEFINE VARIABLE qty AS DECIMAL. 
  DEFINE VARIABLE wert AS DECIMAL. 
  DEFINE VARIABLE tot-bezeich AS CHAR. 
  DEFINE VARIABLE tt-val AS DECIMAL. 
  DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
  */ 
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  DO: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    tt-val = 0. 
    IF sorttype = 1 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp 
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                RUN create-lines-global-oh.
            END.
          END.                     
        END. /* End of add */
        ELSE
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                RUN create-lines-global-oh.
            END.
          END.                           
        END.
    END.
    ELSE IF sorttype = 2 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:    
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich:

                RUN create-lines-global-oh.
            END.
          END.                       
        END. /* End of add */
        ELSE      
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                RUN create-lines-global-oh.
            END.
          END.                          
        END.
    END.
    IF t-val NE 0 THEN 
    DO: 
      /* Malik serverless 639 comment 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>>,>>9"). 

      create str-list. */
      CREATE output-list.
      ASSIGN
        output-list.flag    = 1
        output-list.bezeich = bezeich
        output-list.act-val = t-val.
      CREATE output-list.  
    END. 
    /* FD Comment
    create str-list. 
    str-list.flag = 1. 
    str-list.s = "       ". 
    str-list.s = str-list.s + STRING(tot-bezeich, "x(50)"). 
    DO j = 1 TO 84: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
      str-list.s = str-list.s + STRING(tt-val, "->>>,>>>,>>9.99"). 
    ELSE 
      str-list.s = str-list.s + STRING(tt-val, "->>,>>>,>>>,>>9").
    */ 
  END. 
  /* Malik serverless 639 comment 
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->,>>>,>>>,>>>,>>9"). */
  CREATE output-list.
  ASSIGN
    output-list.flag    = 1
    output-list.bezeich = "GRAND T O T A L"
    output-list.act-val = tt-value.
END. 
 
PROCEDURE create-list1: 
  /*
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE j AS INTEGER. 
  DEFINE VARIABLE tot-anz    AS DECIMAL. 
  DEFINE VARIABLE tot-val    AS DECIMAL. 
  DEFINE VARIABLE t-anz      AS DECIMAL. 
  DEFINE VARIABLE t-val      AS DECIMAL. 
  DEFINE VARIABLE t-value    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE avrg-price AS DECIMAL. 
  DEFINE VARIABLE zwkum AS INTEGER. 
  DEFINE VARIABLE bezeich AS CHAR. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE VARIABLE must-order AS DECIMAL.
  
  DEFINE VARIABLE tt-val AS DECIMAL. 
  DEFINE VARIABLE qty AS DECIMAL. 
  DEFINE VARIABLE wert AS DECIMAL. 
  DEFINE buffer l-oh FOR l-bestand. 
  DEFINE VARIABLE tot-bezeich AS CHAR. 
  */
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  FOR EACH l-lager WHERE lager-nr GE from-lager 
    AND lager-nr LE to-lager: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    tt-val = 0. 
    tot-bezeich = "Ttl - " + l-lager.bezeich. 
    IF sorttype = 1 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp 
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:
                
                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:
                
                RUN create-lines.
            END.
          END.                                
        END. /* End of add */
        ELSE         
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.endkum = from-grp 
                AND l-artikel.min-bestand GT 0 NO-LOCK, 
                FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
                AND l-oh.lager-nr = 0 NO-LOCK, 
                FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.endkum = from-grp NO-LOCK, 
                FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
                AND l-oh.lager-nr = 0 NO-LOCK, 
                FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                RUN create-lines.
            END.
          END.                          
        END.
    END. 
    ELSE IF sorttype = 2 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:       
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp 
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich:

                RUN create-lines.
            END.
          END.                       
        END. /* End of add */
        ELSE            
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                RUN create-lines.
            END.
          END.   
        END.
    END.
    IF t-val NE 0 THEN 
    DO: 
      /* Malik Serverless 639 comment 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>>,>>9"). 
      create str-list. */
      CREATE output-list.
      ASSIGN
        output-list.flag    = 1
        output-list.bezeich = bezeich
        output-list.act-val = t-val.
      CREATE output-list.
    END. 
    /*IF tt-val NE 0 THEN 
    DO:*/    
    /* Malik Serverless 639 comment 
    create str-list.
    str-list.flag = 1. 
    str-list.s = "       ". 
    str-list.s = str-list.s + STRING(tot-bezeich, "x(50)"). 
    DO j = 1 TO 84: 
      str-list.s = str-list.s + " ". 
    END. 
    IF NOT long-digit THEN 
      str-list.s = str-list.s + STRING(tt-val, "->>,>>>,>>>,>>9.99"). 
    ELSE 
      str-list.s = str-list.s + STRING(tt-val, "->,>>>,>>>,>>>,>>9"). 
    create str-list.*/
    CREATE output-list.
    ASSIGN
      output-list.flag    = 1
      output-list.bezeich = tot-bezeich
      output-list.act-val = tt-val.
    CREATE output-list.
    /*END. */
  END. 
  /* Malik Serverless 639 comment 
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->,>>>,>>>,>>>,>>9"). */
  CREATE output-list.
  ASSIGN
    output-list.flag    = 1
    output-list.bezeich = "GRAND T O T A L"
    output-list.act-val = tt-value.
END. 
 
PROCEDURE create-list1A: 
  /*
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE j AS INTEGER. 
  DEFINE VARIABLE tot-anz    AS DECIMAL. 
  DEFINE VARIABLE tot-val    AS DECIMAL. 
  DEFINE VARIABLE t-anz      AS DECIMAL. 
  DEFINE VARIABLE t-val      AS DECIMAL. 
  DEFINE VARIABLE t-value    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE avrg-price AS DECIMAL. 
  DEFINE VARIABLE zwkum AS INTEGER. 
  DEFINE VARIABLE bezeich AS CHAR. 
  DEFINE VARIABLE grp1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE grp2 AS INTEGER INITIAL 1. 
  DEFINE VARIABLE must-order AS DECIMAL.
  
  DEFINE VARIABLE tt-val AS DECIMAL. 
  DEFINE VARIABLE qty AS DECIMAL. 
  DEFINE VARIABLE wert AS DECIMAL. 
  DEFINE buffer l-oh FOR l-bestand. 
  DEFINE VARIABLE tot-bezeich AS CHAR. 
  */ 
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  IF mattype = 1 THEN grp2 = 0. 
  ELSE IF mattype = 2 THEN grp1 = 1. 
 
  DO: 
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    tt-val = 0. 
 
    IF sorttype = 1 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp 
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

                RUN create-lines-global-oh.
            END.
          END.                      
        END. /* End of add */
        ELSE     
        DO:  
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp 
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 

                RUN create-lines-global-oh.
            END.
          END.                          
        END.
    END.
    ELSE IF sorttype = 2 THEN 
    DO:    
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        DO:        
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.zwkum = sub-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                RUN create-lines-global-oh.
            END.
          END.                      
        END. /* End of add */
        ELSE
        DO:    
          IF minoh-flag THEN
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp
              AND l-artikel.min-bestand GT 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-bestand THEN RUN create-lines-global-oh.
            END.
          END.
          ELSE
          DO:
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

                RUN create-lines-global-oh.
            END.
          END.                          
        END.
    END.
    IF t-val NE 0 THEN 
    DO: 
      /* Malik Serverless 639 comment 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>>,>>9"). 
      create str-list. */
      CREATE output-list.
      ASSIGN
        output-list.flag    = 1
        output-list.bezeich = bezeich
        output-list.act-val = t-val.
      CREATE output-list.
    END. 
    IF tt-val NE 0 THEN 
    DO: 
      /* FD Comment
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(tot-bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(tt-val, "->>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(tt-val, "->>,>>>,>>>,>>9"). 
      */
    END. 
  END. 
  /* Malik Serverless 639 comment 
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->,>>>,>>>,>>>,>>9").*/
  CREATE output-list.
  ASSIGN
    output-list.flag    = 1
    output-list.bezeich = "GRAND T O T A L"
    output-list.act-val = tt-value.  
END. 

PROCEDURE create-lines:
    DEFINE VARIABLE tmp-str AS CHAR. /* Malik */
    i = i + 1. 
    must-order = 0.
  
    IF i = 1 THEN 
    DO: 
      /* Malik serverless 639 comment 
      CREATE str-list. 
      str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
        + " " + STRING(l-lager.bezeich, "x(50)").*/
      CREATE output-list.
      ASSIGN
        /* output-list.artnr   = "       " */
        output-list.bezeich = " " + STRING(l-lager.lager-nr, "99") + " " + STRING(l-lager.bezeich, "x(50)").
    END. 
  
    IF zwkum = 0 THEN 
    DO: 
      zwkum = l-artikel.zwkum. 
      bezeich = l-untergrup.bezeich. 
    END. 
    IF zwkum NE l-artikel.zwkum THEN 
    DO:         
      /* Malik Serverless 639 comment      
      CREATE str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
  
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 

      IF NOT long-digit THEN str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9.99"). 
      ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>>,>>9"). 

      CREATE str-list. */
      CREATE output-list.
      ASSIGN
        output-list.flag    = 1
        output-list.bezeich = bezeich
        output-list.act-val = t-val.
      CREATE output-list.
      t-anz = 0. 
      t-val = 0.             
      zwkum = l-untergrup.zwkum. 
      bezeich = l-untergrup.bezeich. 
    END. 

    qty = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
  
    IF show-price THEN 
    DO:
      wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
    END.     
    tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
  
    IF l-artikel.anzverbrauch NE 0 THEN
    DO:
      must-order = l-artikel.anzverbrauch - tot-anz.
    END.
  
    IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
    ELSE tot-val = 0. 
  /*    
      tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                - l-bestand.wert-ausgang. 
  */    
    
    t-anz = t-anz + tot-anz. 
    IF show-price THEN 
    DO: 
      t-val = t-val + tot-val. 
      t-value = t-value + tot-val. 
      tt-val = tt-val + tot-val. 
      tt-value = tt-value + tot-val. 
    END. 
    /* Malik */    
    IF LENGTH(l-artikel.bezeich) GT 50 OR LENGTH(l-artikel.bezeich) GE 50 THEN
    DO:
        tmp-str = l-artikel.bezeich.
    END.
    ELSE
    DO:
        tmp-str = STRING(l-artikel.bezeich) + "                                                  ".
    END.
    /* END Malik */

    /* 
    IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
    DO: 
      CREATE str-list. 
      IF show-price THEN 
      DO: 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-artikel.artnr, "9999999") 
           + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
           + STRING(l-artikel.masseinheit, "x(3)") 
           + STRING(l-artikel.inhalt, ">>,>>9.99") 
           + STRING(l-artikel.traubensort, "x(8)") 
           + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
           + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
           + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
           + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
           + STRING(tot-anz, "->,>>>,>>9.99") 
           + STRING(tot-val, "->>,>>>,>>>,>>9.99")
           + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
           + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
        ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
           + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */ 
           + STRING(l-artikel.masseinheit, "x(3)") 
           + STRING(l-artikel.inhalt, ">>,>>9.99") 
           + STRING(l-artikel.traubensort, "x(8)") 
           + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
           + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
           + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
           + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
           + STRING(tot-anz, "->,>>>,>>9.99") 
           + STRING(tot-val, "->,>>>,>>>,>>>,>>9")
           + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
           + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
      END. 
      ELSE 
      DO: 
        IF NOT long-digit THEN 
        str-list.s = STRING(l-artikel.artnr, "9999999") 
           + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */ 
           + STRING(l-artikel.masseinheit, "x(3)") 
           + STRING(l-artikel.inhalt, ">>,>>9.99") 
           + STRING(l-artikel.traubensort, "x(8)") 
           + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
           + STRING(0, ">>,>>>,>>9.99") 
           + STRING(0, ">>,>>>,>>9.99") 
           + STRING(0, ">>,>>>,>>9.99") 
           + STRING(tot-anz, "->,>>>,>>9.99") 
           + STRING(0, "->>,>>>,>>>,>>9.99")
           + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
           + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
        ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
           + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */ 
           + STRING(l-artikel.masseinheit, "x(3)") 
           + STRING(l-artikel.inhalt, ">>,>>9.99") 
           + STRING(l-artikel.traubensort, "x(8)") 
           + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
           + STRING(0, ">,>>>,>>>,>>9") 
           + STRING(0, ">,>>>,>>>,>>9") 
           + STRING(0, ">,>>>,>>>,>>9") 
           + STRING(tot-anz, "->,>>>,>>9.99") 
           + STRING(0, "->,>>>,>>>,>>>,>>9")
           + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
           + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
      END. 
    END. */      
    IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
    DO: 
      /* CREATE output-list. */ 
      IF show-price THEN 
      DO: 
        IF NOT long-digit THEN 
        DO:
            CREATE output-list. 
            ASSIGN
                output-list.artnr       = l-artikel.artnr
                output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
                output-list.unit        = l-artikel.masseinheit
                output-list.act-qty     = tot-anz
                output-list.act-val     = tot-val
                output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
                output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
                output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
                output-list.last-price  = l-artikel.ek-letzter
                output-list.act-price   = l-artikel.ek-aktuell
                output-list.avrg-price  = l-artikel.vk-preis
                output-list.min-oh      = l-artikel.min-bestand
                output-list.must-order  = must-order.
            /*     
            str-list.s = STRING(l-artikel.artnr, "9999999") 
            + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
            + STRING(l-artikel.masseinheit, "x(3)") 58
            + STRING(l-artikel.inhalt, ">>,>>9.99") 61 
            + STRING(l-artikel.traubensort, "x(8)") 70 
            + STRING(l-artikel.lief-einheit, ">>,>>9.99") 78 
            + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 87 
            + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 101 
            + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 115
            + STRING(tot-anz, "->,>>>,>>9.99") 129
            + STRING(tot-val, "->>,>>>,>>>,>>9.99") 142
            + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") 160 /*gerald min-stock, B3E18C*/
            + STRING(must-order, "->,>>>,>>9.99"). 173 /*FD Feb 18, 2022*/*/
        END.
        ELSE 
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = tot-val
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = l-artikel.ek-letzter
              output-list.act-price   = l-artikel.ek-aktuell
              output-list.avrg-price  = l-artikel.vk-preis
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /* 
          str-list.s = STRING(l-artikel.artnr, "9999999") 
            + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */ 
            + STRING(l-artikel.masseinheit, "x(3)") 
            + STRING(l-artikel.inhalt, ">>,>>9.99") 
            + STRING(l-artikel.traubensort, "x(8)") 
            + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
            + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
            + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
            + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
            + STRING(tot-anz, "->,>>>,>>9.99") 
            + STRING(tot-val, "->,>>>,>>>,>>>,>>9")
            + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
            + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
      END. 
      ELSE 
      DO: 
        IF NOT long-digit THEN 
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = 0 /* tot-val */
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = 0 /* l-artikel.ek-letzter */
              output-list.act-price   = 0 /* l-artikel.ek-aktuell */
              output-list.avrg-price  = 0 /* l-artikel.vk-preis */
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /* 
          str-list.s = STRING(l-artikel.artnr, "9999999") 
             + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */ 
             + STRING(l-artikel.masseinheit, "x(3)") 
             + STRING(l-artikel.inhalt, ">>,>>9.99") 
             + STRING(l-artikel.traubensort, "x(8)") 
             + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
             + STRING(0, ">>,>>>,>>9.99") 
             + STRING(0, ">>,>>>,>>9.99") 
             + STRING(0, ">>,>>>,>>9.99") 
             + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(0, "->>,>>>,>>>,>>9.99")
             + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
             + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
        ELSE 
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = 0 /* tot-val */
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = 0 /* l-artikel.ek-letzter */
              output-list.act-price   = 0 /* l-artikel.ek-aktuell */
              output-list.avrg-price  = 0 /* l-artikel.vk-preis */
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /*     
          str-list.s = STRING(l-artikel.artnr, "9999999") 
             + SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */ 
             + STRING(l-artikel.masseinheit, "x(3)") 
             + STRING(l-artikel.inhalt, ">>,>>9.99") 
             + STRING(l-artikel.traubensort, "x(8)") 
             + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
             + STRING(0, ">,>>>,>>>,>>9") 
             + STRING(0, ">,>>>,>>>,>>9") 
             + STRING(0, ">,>>>,>>>,>>9") 
             + STRING(tot-anz, "->,>>>,>>9.99") 
             + STRING(0, "->,>>>,>>>,>>>,>>9")
             + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
             + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
      END. 
    END.      
END PROCEDURE.

PROCEDURE create-lines-global-oh:
    DEFINE VARIABLE tmp-str AS CHAR. /* Malik 97F887 */ 
    i = i + 1.      
    must-order = 0.
    
    IF zwkum = 0 THEN 
    DO: 
      zwkum = l-artikel.zwkum. 
      bezeich = l-untergrup.bezeich. 
    END. 
    IF zwkum NE l-artikel.zwkum THEN 
    DO: 
      /* Malik Serverless 639 comment 
      CREATE str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
    
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 

      IF NOT long-digit THEN str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9.99"). 
      ELSE str-list.s = str-list.s + STRING(t-val, "->,>>>,>>>,>>>,>>9"). 
      
      CREATE str-list. */
      CREATE output-list.
      ASSIGN
        output-list.flag    = 1
        output-list.bezeich = bezeich
        output-list.act-val = t-val.
      CREATE output-list.
      t-anz = 0. 
      t-val = 0.             
      zwkum = l-untergrup.zwkum. 
      bezeich = l-untergrup.bezeich. 
    END. 
    
    IF show-price THEN 
    DO:
      tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang.
    END.       
    tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    
    IF l-artikel.anzverbrauch NE 0 THEN
    DO:
      must-order = l-artikel.anzverbrauch - tot-anz.
    END.
    
    t-anz = t-anz + tot-anz. 
    IF show-price THEN 
    DO: 
      t-val = t-val + tot-val. 
      t-value = t-value + tot-val. 
      tt-val = tt-val + tot-val. 
      tt-value = tt-value + tot-val. 
    END. 
    /* Malik 97F887 */    
    IF LENGTH(l-artikel.bezeich) GT 50 OR LENGTH(l-artikel.bezeich) GE 50 THEN
    DO:
        tmp-str = l-artikel.bezeich.
    END.
    ELSE
    DO:

        tmp-str = STRING(l-artikel.bezeich) + "                                                  ". /*bernatd EFA73E*/
       
    END.
    /* END Malik */  
    IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
    DO: 
      /*CREATE str-list.*/ 
      IF show-price THEN 
      DO: 
        IF NOT long-digit THEN 
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = tot-val
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = l-artikel.ek-letzter
              output-list.act-price   = l-artikel.ek-aktuell
              output-list.avrg-price  = l-artikel.vk-preis
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /* 
          str-list.s = STRING(l-artikel.artnr, "9999999") 
            + SUBSTR(STRING(tmp-str), 1, 50) /* Malik 97F887 : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
            + STRING(l-artikel.masseinheit, "x(3)") 
            + STRING(l-artikel.inhalt, ">>,>>9.99") 
            + STRING(l-artikel.traubensort, "x(8)") 
            + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
            + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
            + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
            + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
            + STRING(tot-anz, "->,>>>,>>9.99") 
            + STRING(tot-val, "->>,>>>,>>>,>>9.99")
            + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
            + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
        ELSE
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = tot-val
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = l-artikel.ek-letzter
              output-list.act-price   = l-artikel.ek-aktuell
              output-list.avrg-price  = l-artikel.vk-preis
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /* 
          str-list.s = STRING(l-artikel.artnr, "9999999") 
            + SUBSTR(STRING(tmp-str), 1, 50) /* Malik 97F887 : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
            + STRING(l-artikel.masseinheit, "x(3)") 
            + STRING(l-artikel.inhalt, ">>,>>9.99") 
            + STRING(l-artikel.traubensort, "x(8)") 
            + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
            + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
            + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
            + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
            + STRING(tot-anz, "->,>>>,>>9.99") 
            + STRING(tot-val, "->,>>>,>>>,>>>,>>9")
            + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
            + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
      END. 
      ELSE 
      DO: 
        IF NOT long-digit THEN 
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = 0
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = 0
              output-list.act-price   = 0
              output-list.avrg-price  = 0
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /* 
          str-list.s = STRING(l-artikel.artnr, "9999999") 
            + SUBSTR(STRING(tmp-str), 1, 50) /* Malik 97F887 : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
            + STRING(l-artikel.masseinheit, "x(3)") 
            + STRING(l-artikel.inhalt, ">>,>>9.99") 
            + STRING(l-artikel.traubensort, "x(8)") 
            + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
            + STRING(0, ">>,>>>,>>9.99") 
            + STRING(0, ">>,>>>,>>9.99") 
            + STRING(0, ">>,>>>,>>9.99") 
            + STRING(tot-anz, "->,>>>,>>9.99") 
            + STRING(0, "->>,>>>,>>>,>>9.99")
            + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
            + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
        ELSE 
        DO:
          CREATE output-list. 
          ASSIGN
              output-list.artnr       = l-artikel.artnr
              output-list.bezeich     = SUBSTR(STRING(tmp-str), 1, 50) /* Malik : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
              output-list.unit        = l-artikel.masseinheit
              output-list.act-qty     = tot-anz
              output-list.act-val     = 0
              output-list.cont1       = STRING(l-artikel.inhalt, ">>,>>9.99")
              output-list.d-unit      = STRING(l-artikel.traubensort, "x(8)")
              output-list.cont2       = STRING(l-artikel.lief-einheit, ">>,>>9.99")
              output-list.last-price  = 0
              output-list.act-price   = 0
              output-list.avrg-price  = 0
              output-list.min-oh      = l-artikel.min-bestand
              output-list.must-order  = must-order.
          /*     
          str-list.s = STRING(l-artikel.artnr, "9999999") 
            + SUBSTR(STRING(tmp-str), 1, 50) /* Malik 97F887 : STRING(l-artikel.bezeich, "x(50)") -> SUBSTR(STRING(tmp-str), 1, 50) */
            + STRING(l-artikel.masseinheit, "x(3)") 
            + STRING(l-artikel.inhalt, ">>,>>9.99") 
            + STRING(l-artikel.traubensort, "x(8)") 
            + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
            + STRING(0, ">,>>>,>>>,>>9") 
            + STRING(0, ">,>>>,>>>,>>9") 
            + STRING(0, ">,>>>,>>>,>>9") 
            + STRING(tot-anz, "->,>>>,>>9.99") 
            + STRING(0, "->,>>>,>>>,>>>,>>9")
            + STRING(l-artikel.min-bestand, "->,>>>,>>9.99") /*gerald min-stock, B3E18C*/
            + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/*/
        END.
      END. 
    END. 
END PROCEDURE.

