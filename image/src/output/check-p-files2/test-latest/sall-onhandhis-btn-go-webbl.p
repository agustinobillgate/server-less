DEFINE TEMP-TABLE out-list
    FIELD artnr AS INTEGER
    FIELD bezeich AS CHARACTER
    FIELD unit  AS CHARACTER
    FIELD qty AS DECIMAL
    FIELD val AS DECIMAL
    FIELD content AS DECIMAL
    FIELD d-unit AS CHARACTER
    FIELD d-content AS DECIMAL
    FIELD last-price AS DECIMAL
    FIELD act-price AS DECIMAL
    FIELD avrg-price AS DECIMAL
    FIELD flag AS INTEGER INIT 0
.

DEF INPUT PARAMETER anf-date    AS DATE.
DEF INPUT PARAMETER end-date    AS DATE.

DEF INPUT PARAMETER all-flag    AS LOGICAL.
DEF INPUT PARAMETER show-price  AS LOGICAL.
DEF INPUT PARAMETER zero-flag   AS LOGICAL.
DEF INPUT PARAMETER from-grp    AS INT.
DEF INPUT PARAMETER sub-grp     AS INT.
DEF INPUT PARAMETER from-lager  AS INT.
DEF INPUT PARAMETER to-lager    AS INT.
DEF INPUT PARAMETER sorttype    AS INT.
DEF INPUT PARAMETER mattype     AS INT.

DEF OUTPUT PARAMETER done AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER TABLE FOR out-list.

/*
DEF VAR anf-date    AS DATE INIT 12/01/18.
DEF VAR end-date    AS DATE INIT 12/31/18.

DEF VAR all-flag    AS LOGICAL INIT YES.
DEF VAR show-price  AS LOGICAL INIT YES.
DEF VAR zero-flag   AS LOGICAL INIT NO.
DEF VAR from-grp    AS INT INIT 1.
DEF VAR sub-grp     AS INT INIT 102.
DEF VAR from-lager  AS INT INIT 1.
DEF VAR to-lager    AS INT INIT 7.
DEF VAR sorttype    AS INT INIT 1.
DEF VAR mattype     AS INT INIT 0.

DEF VAR done AS LOGICAL INIT YES.
 */
DEFINE VARIABLE long-digit AS LOGICAL.
DEFINE VARIABLE vk-preis   AS DECIMAL INIT 0.
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

FIND FIRST vhp.l-besthis WHERE vhp.l-besthis.anf-best-dat GE anf-date 
      AND vhp.l-besthis.anf-best-dat LE end-date NO-LOCK NO-ERROR.
IF NOT AVAILABLE vhp.l-besthis THEN done = NO.

IF NOT done THEN
DO:
    RETURN NO-APPLY.
END.

IF NOT all-flag THEN RUN create-list.
ELSE RUN create-listA. 

/*
FOR EACH out-list:
    DISP out-list.artnr out-list.bezeich FORMAT "x(40)" out-list.val FORMAT ">>>,>>>,>>9.99".
END.
*/

PROCEDURE create-list: 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE tot-anz     AS DECIMAL. 
DEFINE VARIABLE tot-val     AS DECIMAL. 
DEFINE VARIABLE t-anz       AS DECIMAL. 
DEFINE VARIABLE t-val       AS DECIMAL. 
DEFINE VARIABLE t-value     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE avrg-price  AS DECIMAL. 
DEFINE VARIABLE zwkum       AS INTEGER. 
DEFINE VARIABLE bezeich     AS CHAR. 
DEFINE VARIABLE qty         AS DECIMAL. 
DEFINE VARIABLE wert        AS DECIMAL. 
DEFINE VARIABLE tot-bezeich AS CHAR. 
DEFINE VARIABLE tt-val      AS DECIMAL. 
DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
 
DEFINE BUFFER l-oh   FOR vhp.l-besthis. 
DEFINE VAR s-bezeich AS CHARACTER.

  FOR EACH l-lager WHERE lager-nr GE from-lager 
    AND lager-nr LE to-lager: 
    tot-bezeich = "Ttl - " + l-lager.bezeich. 

    CREATE out-list.
    s-bezeich = STRING(l-lager.lager-nr, "99") 
                      + " " + STRING(l-lager.bezeich, "x(13)").
    out-list.bezeich = STRING(l-lager.lager-nr, "99") 
                      + " " + STRING(l-lager.bezeich, "x(13)").
    
    i = 0. 
    zwkum = 0. 
    t-anz = 0. 
    t-val = 0. 
    tt-val = 0. 

    IF sorttype = 1 THEN 
    DO:
      FOR EACH l-besthis NO-LOCK WHERE 
        l-besthis.anf-best-dat GE anf-date AND
        l-besthis.anf-best-dat LE end-date AND
        l-besthis.lager-nr = l-lager.lager-nr,
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-besthis.artnr NO-LOCK, 
        FIRST l-oh NO-LOCK WHERE 
          l-oh.anf-best-dat GE anf-date      AND
          l-oh.anf-best-dat LE end-date      AND
          l-oh.lager-nr = 0                  AND
          l-oh.artnr = vhp.l-besthis.artnr, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 

        IF (from-grp = 0 AND sub-grp = 0) OR
           (l-artikel.endkum = from-grp AND sub-grp = 0)OR
           (l-artikel.endkum = from-grp AND l-artikel.zwkum = sub-grp) OR 
           (from-grp = 0 AND l-artikel.zwkum = sub-grp) THEN
        DO:
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO:
            IF t-val NE 0 THEN
            DO:
              CREATE out-list.
              ASSIGN
                out-list.flag = 1
                out-list.bezeich = bezeich
                out-list.val = t-val.

              CREATE out-list.
            END.              
            
            ASSIGN
              out-list.flag = 0
              t-anz = 0
              t-val = 0
              zwkum = l-untergrup.zwkum
              bezeich = l-untergrup.bezeich.
          END. 
          
          qty = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
          
          IF show-price THEN 
            wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
          
          tot-anz = vhp.l-besthis.anz-anf-best + vhp.l-besthis.anz-eingang 
                  - vhp.l-besthis.anz-ausgang. 
          
          IF qty NE 0 THEN tot-val = wert * tot-anz / qty.
          ELSE tot-val = 0.
          IF tot-anz NE 0 THEN vk-preis = tot-val / tot-anz. 
          ELSE vk-preis = 0.

          t-anz = t-anz + tot-anz. 
          IF show-price THEN 
          DO:
            ASSIGN 
              t-val = t-val + tot-val. 
              t-value = t-value + tot-val. 
              tt-val = tt-val + tot-val. 
              tt-value = tt-value + tot-val. 
          END. 
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO:
            CREATE out-list.
            out-list.flag = 2.
            IF show-price THEN 
            DO: 
              ASSIGN
                out-list.artnr = l-artikel.artnr
                out-list.bezeich = l-artikel.bezeich
                out-list.unit = l-artikel.masseinheit
                out-list.content = l-artikel.inhalt
                out-list.d-unit = l-artikel.traubensort
                out-list.d-content = l-artikel.lief-einheit
                out-list.last-price = l-artikel.ek-letzter
                out-list.act-price = l-artikel.ek-aktuell
                out-list.avrg-price = vk-preis
                out-list.qty = tot-anz
                out-list.val = tot-val.
            END. 
            ELSE 
            DO: 
              ASSIGN
                out-list.artnr = l-artikel.artnr
                out-list.bezeich = l-artikel.bezeich
                out-list.unit = l-artikel.masseinheit
                out-list.content = l-artikel.inhalt
                out-list.d-unit = l-artikel.traubensort
                out-list.d-content = l-artikel.lief-einheit
                out-list.last-price = 0
                out-list.act-price = 0
                out-list.avrg-price = 0
                out-list.qty = tot-anz
                out-list.val = 0.
            END. 
          END.
        END.
      END. 
    END.
 
    ELSE IF sorttype = 2 THEN 
    DO:
      FOR EACH l-besthis NO-LOCK WHERE 
        l-besthis.anf-best-dat GE anf-date AND
        l-besthis.anf-best-dat LE end-date AND
        l-besthis.lager-nr = l-lager.lager-nr,
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-besthis.artnr NO-LOCK, 
        FIRST l-oh NO-LOCK WHERE 
          l-oh.anf-best-dat GE anf-date      AND
          l-oh.anf-best-dat LE end-date      AND
          l-oh.lager-nr = 0                  AND
          l-oh.artnr = vhp.l-besthis.artnr, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
        
        IF (from-grp = 0 AND sub-grp = 0) OR
           (l-artikel.endkum = from-grp AND sub-grp = 0)OR
           (l-artikel.endkum = from-grp AND l-artikel.zwkum = sub-grp) OR 
           (from-grp = 0 AND l-artikel.zwkum = sub-grp) THEN
        DO:
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          
          IF zwkum NE l-artikel.zwkum THEN 
          DO:
            IF t-val NE 0 THEN
            DO:
              CREATE out-list.
              ASSIGN
                out-list.flag = 1
                out-list.bezeich = bezeich
                out-list.val = t-val.

              CREATE out-list. 
            END.

            ASSIGN
              t-anz = 0
              t-val = 0
              zwkum = l-untergrup.zwkum
              bezeich = l-untergrup.bezeich. 
          END. 

          qty = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
          IF show-price THEN 
            wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
          tot-anz = vhp.l-besthis.anz-anf-best + vhp.l-besthis.anz-eingang 
                    - vhp.l-besthis.anz-ausgang.
          IF qty NE 0 THEN tot-val = wert * tot-anz / qty.
          ELSE tot-val = 0.
          IF tot-anz NE 0 THEN vk-preis = tot-val / tot-anz.
          ELSE vk-preis = 0. 

          t-anz = t-anz + tot-anz. 
          IF show-price THEN 
          DO:
            ASSIGN
              t-val = t-val + tot-val. 
              t-value = t-value + tot-val. 
              tt-val = tt-val + tot-val. 
              tt-value = tt-value + tot-val. 
          END. 

          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            CREATE out-list.
            out-list.flag = 2.
            IF show-price THEN 
            DO: 
              ASSIGN
                out-list.artnr = l-artikel.artnr
                out-list.bezeich = l-artikel.bezeich
                out-list.unit = l-artikel.masseinheit
                out-list.content = l-artikel.inhalt
                out-list.d-unit = l-artikel.traubensort
                out-list.d-content = l-artikel.lief-einheit
                out-list.last-price = l-artikel.ek-letzter
                out-list.act-price = l-artikel.ek-aktuell
                out-list.avrg-price = vk-preis
                out-list.qty = tot-anz
                out-list.val = tot-val.
            END. 
            ELSE 
            DO: 
              ASSIGN
                out-list.artnr = l-artikel.artnr
                out-list.bezeich = l-artikel.bezeich
                out-list.unit = l-artikel.masseinheit
                out-list.content = l-artikel.inhalt
                out-list.d-unit = l-artikel.traubensort
                out-list.d-content = l-artikel.lief-einheit
                out-list.last-price = 0
                out-list.act-price = 0
                out-list.avrg-price = 0
                out-list.qty = tot-anz
                out-list.val = 0.
            END.
          END.
        END.  
      END.
    END.
 
    IF t-val NE 0 THEN 
    DO: 
      CREATE out-list.
      ASSIGN
        out-list.flag = 1
        out-list.bezeich = bezeich
        out-list.val = t-val.

      CREATE out-list.
    END. 

    IF tt-val = 0 THEN
    DO:
      FIND FIRST out-list WHERE out-list.bezeich = s-bezeich.
      DELETE out-list.
    END.
    ELSE
    DO:
      CREATE out-list.
      ASSIGN
        out-list.flag = 1
        out-list.bezeich = tot-bezeich
        out-list.val = tt-val.
    END.         
  END. 
  
  IF tt-value NE 0 THEN
  DO:
    CREATE out-list.
    ASSIGN
      out-list.flag = 1
      out-list.bezeich = "GRAND T O T A L"
      out-list.val = tt-value.
  END.
END. 
 
PROCEDURE create-listA: 
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
 
DEFINE BUFFER l-oh FOR vhp.l-besthis. 
DEFINE VARIABLE qty         AS DECIMAL . 
DEFINE VARIABLE wert        AS DECIMAL .  
DEFINE VARIABLE tot-bezeich AS CHAR. 
DEFINE VARIABLE tt-val      AS DECIMAL. 
DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
 

  i = 0. 
  zwkum = 0. 
  t-anz = 0. 
  t-val = 0. 
  tt-val = 0. 
  IF sorttype = 1 THEN 
  DO:               
    FOR EACH l-besthis NO-LOCK WHERE 
      l-besthis.anf-best-dat GE anf-date AND
      l-besthis.anf-best-dat LE end-date AND
      l-besthis.lager-nr = 0, 
      FIRST l-artikel WHERE l-artikel.artnr = vhp.l-besthis.artnr NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
      NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 

      IF (from-grp = 0 AND sub-grp = 0) OR
           (l-artikel.endkum = from-grp AND sub-grp = 0)OR
           (l-artikel.endkum = from-grp AND l-artikel.zwkum = sub-grp) OR 
           (from-grp = 0 AND l-artikel.zwkum = sub-grp) THEN
      DO:
        IF zwkum = 0 THEN 
        DO: 
          zwkum = l-artikel.zwkum. 
          bezeich = l-untergrup.bezeich. 
        END. 
        IF zwkum NE l-artikel.zwkum THEN 
        DO:
          IF t-val NE 0 THEN
          DO:
            CREATE out-list.
            ASSIGN 
              out-list.flag = 1
              out-list.bezeich = bezeich
              out-list.val = t-val.
            CREATE out-list.
          END.
          ASSIGN
            t-anz = 0
            t-val = 0 
            zwkum = l-untergrup.zwkum
            bezeich = l-untergrup.bezeich. 
        END. 
          
        IF show-price THEN 
          tot-val = vhp.l-besthis.val-anf-best + vhp.l-besthis.wert-eingang 
                   - vhp.l-besthis.wert-ausgang. 
        tot-anz = vhp.l-besthis.anz-anf-best + vhp.l-besthis.anz-eingang 
                   - vhp.l-besthis.anz-ausgang.
          
        IF tot-anz NE 0 THEN vk-preis = tot-val / tot-anz.
        ELSE vk-preis = 0.
          
        t-anz = t-anz + tot-anz. 

        IF show-price THEN 
        DO: 
          ASSIGN
            t-val = t-val + tot-val
            t-value = t-value + tot-val
            tt-val = tt-val + tot-val
            tt-value = tt-value + tot-val. 
        END. 
        IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
        DO: 
          CREATE out-list.
          out-list.flag = 2.
          IF show-price THEN 
          DO: 
            ASSIGN
              out-list.artnr = l-artikel.artnr
              out-list.bezeich = l-artikel.bezeich
              out-list.unit = l-artikel.masseinheit
              out-list.content = l-artikel.inhalt
              out-list.d-unit = l-artikel.traubensort
              out-list.d-content = l-artikel.lief-einheit
              out-list.last-price = l-artikel.ek-letzter
              out-list.act-price = l-artikel.ek-aktuell
              out-list.avrg-price = vk-preis
              out-list.qty = tot-anz
              out-list.val = tot-val.
          END. 
          ELSE 
          DO: 
            ASSIGN
              out-list.artnr = l-artikel.artnr
              out-list.bezeich = l-artikel.bezeich
              out-list.unit = l-artikel.masseinheit
              out-list.content = l-artikel.inhalt
              out-list.d-unit = l-artikel.traubensort
              out-list.d-content = l-artikel.lief-einheit
              out-list.last-price = 0
              out-list.act-price = 0
              out-list.avrg-price = 0
              out-list.qty = tot-anz
              out-list.val = 0.
          END.
        END. 
      END.
    END.
  END.
  ELSE IF sorttype = 2 THEN 
  DO:               
    FOR EACH l-besthis NO-LOCK WHERE 
      l-besthis.anf-best-dat GE anf-date AND
      l-besthis.anf-best-dat LE end-date AND
      l-besthis.lager-nr = 0, 
      FIRST l-artikel WHERE l-artikel.artnr = vhp.l-besthis.artnr NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
      NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 

      IF (from-grp = 0 AND sub-grp = 0) OR
           (l-artikel.endkum = from-grp AND sub-grp = 0)OR
           (l-artikel.endkum = from-grp AND l-artikel.zwkum = sub-grp) OR 
           (from-grp = 0 AND l-artikel.zwkum = sub-grp) THEN
      DO:
        IF zwkum = 0 THEN 
        DO: 
          zwkum = l-artikel.zwkum. 
          bezeich = l-untergrup.bezeich. 
        END. 
        IF zwkum NE l-artikel.zwkum THEN 
        DO:
          IF t-val NE 0 THEN
          DO:
            CREATE out-list.
            ASSIGN 
              out-list.flag = 1
              out-list.bezeich = bezeich
              out-list.val = t-val.
            CREATE out-list.
          END.
          
          ASSIGN
            t-anz = 0
            t-val = 0 
            zwkum = l-untergrup.zwkum
            bezeich = l-untergrup.bezeich. 
        END. 
          
        IF show-price THEN 
          tot-val = vhp.l-besthis.val-anf-best + vhp.l-besthis.wert-eingang 
                   - vhp.l-besthis.wert-ausgang. 
        tot-anz = vhp.l-besthis.anz-anf-best + vhp.l-besthis.anz-eingang 
                   - vhp.l-besthis.anz-ausgang.
          
        IF tot-anz NE 0 THEN vk-preis = tot-val / tot-anz.
        ELSE vk-preis = 0.
          
        t-anz = t-anz + tot-anz. 

        IF show-price THEN 
        DO: 
          ASSIGN
            t-val = t-val + tot-val
            t-value = t-value + tot-val
            tt-val = tt-val + tot-val
            tt-value = tt-value + tot-val. 
        END. 
        IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
        DO: 
          CREATE out-list.
          out-list.flag = 2.
          IF show-price THEN 
          DO: 
            ASSIGN
              out-list.artnr = l-artikel.artnr
              out-list.bezeich = l-artikel.bezeich
              out-list.unit = l-artikel.masseinheit
              out-list.content = l-artikel.inhalt
              out-list.d-unit = l-artikel.traubensort
              out-list.d-content = l-artikel.lief-einheit
              out-list.last-price = l-artikel.ek-letzter
              out-list.act-price = l-artikel.ek-aktuell
              out-list.avrg-price = vk-preis
              out-list.qty = tot-anz
              out-list.val = tot-val.
          END. 
          ELSE 
          DO: 
            ASSIGN
              out-list.artnr = l-artikel.artnr
              out-list.bezeich = l-artikel.bezeich
              out-list.unit = l-artikel.masseinheit
              out-list.content = l-artikel.inhalt
              out-list.d-unit = l-artikel.traubensort
              out-list.d-content = l-artikel.lief-einheit
              out-list.last-price = 0
              out-list.act-price = 0
              out-list.avrg-price = 0
              out-list.qty = tot-anz
              out-list.val = 0.
          END.
        END. 
      END.
    END.
  END.

  IF t-val NE 0 THEN 
  DO:
    CREATE out-list.
    ASSIGN
      out-list.flag = 1
      out-list.bezeich = bezeich
      out-list.val = t-val.
    CREATE out-list.
  END. 
    
  CREATE out-list. 
  ASSIGN
    out-list.flag = 1
    out-list.bezeich = "GRAND T O T A L"
    out-list.val = tt-value.
END.
