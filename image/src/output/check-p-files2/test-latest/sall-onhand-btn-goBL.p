DEFINE TEMP-TABLE str-list
  FIELD flag AS INTEGER 
  FIELD s AS CHAR FORMAT "x(166)". 

DEF INPUT  PARAMETER all-flag   AS LOGICAL.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF INPUT  PARAMETER zero-flag  AS LOGICAL.
DEF INPUT  PARAMETER from-grp   AS INT.
DEF INPUT  PARAMETER sub-grp    AS INT.
DEF INPUT  PARAMETER from-lager AS INT.
DEF INPUT  PARAMETER to-lager   AS INT.
DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER mattype    AS INT.
DEF OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

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


PROCEDURE create-list: 
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
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
          AND l-oh.lager-nr = 0 NO-LOCK,
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
          i = i + 1. 
          must-order = 0.

          IF i = 1 THEN 
          DO: 
            create str-list. 
            str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
              + " " + STRING(l-lager.bezeich, "x(50)").
          END. 
     
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO:              
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
     
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
                str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                    - l-oh.anz-ausgang. 
     
          IF show-price THEN 
          wert = l-oh.val-anf-best + l-oh.wert-eingang 
                    - l-oh.wert-ausgang. 
     
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 

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
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END.
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK,
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
              i = i + 1. 
              must-order = 0.

              IF i = 1 THEN 
              DO: 
                create str-list. 
                str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
                  + " " + STRING(l-lager.bezeich, "x(50)"). 
              END. 

              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 

                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                    str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                        - l-oh.anz-ausgang. 

              IF show-price THEN 
              wert = l-oh.val-anf-best + l-oh.wert-eingang 
                        - l-oh.wert-ausgang. 

              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 

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
              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END.
     
    ELSE IF sorttype = 2 THEN 
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
          AND l-oh.lager-nr = 0 NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
          i = i + 1. 
          must-order = 0.

          IF i = 1 THEN 
          DO: 
            create str-list. 
            str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
              + " " + STRING(l-lager.bezeich, "x(13)"). 
          END. 
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
                str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE 
            str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                    - l-oh.anz-ausgang. 
          IF show-price THEN 
          wert = l-oh.val-anf-best + l-oh.wert-eingang 
                    - l-oh.wert-ausgang. 
     
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 

          IF l-artikel.anzverbrauch NE 0 THEN
          DO:
            must-order = l-artikel.anzverbrauch - tot-anz.
          END.

          IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
          ELSE tot-val = 0. 
     
          t-anz = t-anz + tot-anz. 
          IF show-price THEN 
          DO: 
            t-val = t-val + tot-val. 
            t-value = t-value + tot-val. 
            tt-val = tt-val + tot-val. 
            tt-value = tt-value + tot-val. 
          END. 
     
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END.
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
              i = i + 1. 
              must-order = 0.

              IF i = 1 THEN 
              DO: 
                create str-list. 
                str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
                  + " " + STRING(l-lager.bezeich, "x(13)"). 
              END. 
              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 
                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                    str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE 
                str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                        - l-oh.anz-ausgang. 
              IF show-price THEN 
              wert = l-oh.val-anf-best + l-oh.wert-eingang 
                        - l-oh.wert-ausgang. 

              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 

              IF l-artikel.anzverbrauch NE 0 THEN
              DO:
                must-order = l-artikel.anzverbrauch - tot-anz.
              END.

              IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
              ELSE tot-val = 0. 

              t-anz = t-anz + tot-anz. 
              IF show-price THEN 
              DO: 
                t-val = t-val + tot-val. 
                t-value = t-value + tot-val. 
                tt-val = tt-val + tot-val. 
                tt-value = tt-value + tot-val. 
              END. 

              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 

    IF t-val NE 0 THEN 
    DO: 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
      create str-list. 
    END. 
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

    create str-list.
  END. 
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9"). 
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
DEFINE VARIABLE must-order AS DECIMAL.
 
DEFINE buffer l-oh FOR l-bestand. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-bezeich AS CHAR. 
DEFINE VARIABLE tt-val AS DECIMAL. 
DEFINE VARIABLE tt-value    AS DECIMAL INITIAL 0. 
 
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
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
          i = i + 1.      
          must-order = 0.

          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
     
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
                str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          IF show-price THEN 
            tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                    - l-bestand.wert-ausgang. 
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 
     
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
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END.
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
              i = i + 1. 
              must-order = 0.

              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 

                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                    str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0. 
                must-order = 0.
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              IF show-price THEN 
                tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                        - l-bestand.wert-ausgang. 
              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang.                             

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
              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 
 
    ELSE IF sorttype = 2 THEN 
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
          i = i + 1. 
          must-order = 0.

          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
                str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE 
            str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          IF show-price THEN 
            tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                    - l-bestand.wert-ausgang. 
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 
     
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
     
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END. 
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
              i = i + 1. 
              must-order = 0.

              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 
                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                    str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE 
                str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              IF show-price THEN 
                tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                        - l-bestand.wert-ausgang. 
              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 

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

              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 
 
    IF t-val NE 0 THEN 
    DO: 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
      create str-list. 
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
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1: 
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
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
            AND l-artikel.zwkum = sub-grp NO-LOCK, 
            FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
            AND l-oh.lager-nr = 0 NO-LOCK, 
            FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
            AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:
    
          i = i + 1.
          must-order = 0.

          IF i = 1 THEN 
          DO: 
            create str-list. 
            str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
              + " " + STRING(l-lager.bezeich, "x(50)"). 
          END. 
               
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
     
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
              str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE 
              str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                    - l-oh.anz-ausgang. 
          IF show-price THEN 
            wert = l-oh.val-anf-best + l-oh.wert-eingang 
                    - l-oh.wert-ausgang. 
     
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 

          IF l-artikel.anzverbrauch NE 0 THEN
          DO:
            must-order = l-artikel.anzverbrauch - tot-anz.
          END.            

          IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
          ELSE tot-val = 0. 
     
          t-anz = t-anz + tot-anz. 
          IF show-price THEN 
          DO: 
            t-val = t-val + tot-val. 
            t-value = t-value + tot-val. 
            tt-val = tt-val + tot-val. 
            tt-value = tt-value + tot-val. 
          END. 
     
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END.
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
                AND l-artikel.endkum = from-grp NO-LOCK, 
                FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
                AND l-oh.lager-nr = 0 NO-LOCK, 
                FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
                AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr:

              i = i + 1. 
              must-order = 0.

              IF i = 1 THEN 
              DO: 
                create str-list. 
                str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
                  + " " + STRING(l-lager.bezeich, "x(50)"). 
              END. 

              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 

                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                  str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE 
                  str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                        - l-oh.anz-ausgang. 
              IF show-price THEN 
                wert = l-oh.val-anf-best + l-oh.wert-eingang 
                        - l-oh.wert-ausgang. 

              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 

              IF l-artikel.anzverbrauch NE 0 THEN
              DO:
                must-order = l-artikel.anzverbrauch - tot-anz.
              END. 

              IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
              ELSE tot-val = 0. 

              t-anz = t-anz + tot-anz. 
              IF show-price THEN 
              DO: 
                t-val = t-val + tot-val. 
                t-value = t-value + tot-val. 
                tt-val = tt-val + tot-val. 
                tt-value = tt-value + tot-val. 
              END. 

              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 
     
    ELSE IF sorttype = 2 THEN 
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
          AND l-oh.lager-nr = 0 NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
          i = i + 1. 
          must-order = 0.

          IF i = 1 THEN 
          DO: 
            create str-list. 
            str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
              + " " + STRING(l-lager.bezeich, "x(13)"). 
          END. 
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
              str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE 
              str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                    - l-oh.anz-ausgang. 
          IF show-price THEN 
            wert = l-oh.val-anf-best + l-oh.wert-eingang 
                    - l-oh.wert-ausgang. 
     
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 

          IF l-artikel.anzverbrauch NE 0 THEN
          DO:
            must-order = l-artikel.anzverbrauch - tot-anz.
          END. 

          IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
          ELSE tot-val = 0. 
     
          t-anz = t-anz + tot-anz. 
          IF show-price THEN 
          DO: 
            t-val = t-val + tot-val. 
            t-value = t-value + tot-val. 
            tt-val = tt-val + tot-val. 
            tt-value = tt-value + tot-val. 
          END. 
     
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END.
        ELSE
            /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK, 
              FIRST l-oh WHERE l-oh.artnr = l-bestand.artnr 
              AND l-oh.lager-nr = 0 NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
              i = i + 1. 
              must-order = 0.

              IF i = 1 THEN 
              DO: 
                create str-list. 
                str-list.s = "        " + STRING(l-lager.lager-nr, "99") 
                  + " " + STRING(l-lager.bezeich, "x(13)"). 
              END. 
              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 
                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                  str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE 
                  str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              qty = l-oh.anz-anf-best + l-oh.anz-eingang 
                        - l-oh.anz-ausgang. 
              IF show-price THEN 
                wert = l-oh.val-anf-best + l-oh.wert-eingang 
                        - l-oh.wert-ausgang. 

              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 

              IF l-artikel.anzverbrauch NE 0 THEN
              DO:
                must-order = l-artikel.anzverbrauch - tot-anz.
              END. 

              IF qty NE 0 THEN tot-val = wert * tot-anz / qty. 
              ELSE tot-val = 0. 

              t-anz = t-anz + tot-anz. 
              IF show-price THEN 
              DO: 
                t-val = t-val + tot-val. 
                t-value = t-value + tot-val. 
                tt-val = tt-val + tot-val. 
                tt-value = tt-value + tot-val. 
              END. 

              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 
 
    IF t-val NE 0 THEN 
    DO: 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
      create str-list. 
    END. 
    IF tt-val NE 0 THEN 
    DO:       
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

      create str-list.
    END. 
  END. 
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9"). 
END. 
 
PROCEDURE create-list1A: 
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
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
          NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
          i = i + 1. 
          must-order = 0.
     
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
     
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
              str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE 
              str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          IF show-price THEN 
            tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                    - l-bestand.wert-ausgang. 
     
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 
     
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
     
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
                str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
                str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, "->,>>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END.
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
              NO-LOCK BY l-artikel.zwkum BY l-artikel.artnr: 
              i = i + 1. 
              must-order = 0.

              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 

                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                  str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE 
                  str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              IF show-price THEN 
                tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                        - l-bestand.wert-ausgang. 

              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 

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

              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                    str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                    str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, "->,>>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 
 
    ELSE IF sorttype = 2 THEN 
        /* Add by Michael @ 06/07/2018 for adding search filter by sub group inventory */
        IF sub-grp NE 000 THEN
        FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
          FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
          AND l-artikel.zwkum = sub-grp NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
          AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
            NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
          i = i + 1. 
          must-order = 0.
     
          IF zwkum = 0 THEN 
          DO: 
            zwkum = l-artikel.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
          IF zwkum NE l-artikel.zwkum THEN 
          DO: 
            create str-list. 
            str-list.flag = 1. 
            str-list.s = "       ". 
            str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
            DO j = 1 TO 84: 
              str-list.s = str-list.s + " ". 
            END. 
            IF NOT long-digit THEN 
              str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
            ELSE 
              str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
            create str-list. 
            t-anz = 0. 
            t-val = 0.             
            zwkum = l-untergrup.zwkum. 
            bezeich = l-untergrup.bezeich. 
          END. 
     
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                    - l-bestand.anz-ausgang. 
          IF show-price THEN 
            tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                    - l-bestand.wert-ausgang. 
     
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
     
          IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
          DO: 
            create str-list. 
            IF show-price THEN 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                 + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                 + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(tot-val, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
            ELSE 
            DO: 
              IF NOT long-digit THEN 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(0, ">>,>>>,>>9.99") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>>,>>>,>>9.99")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
              ELSE 
              str-list.s = STRING(l-artikel.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(50)") 
                 + STRING(l-artikel.masseinheit, "x(3)") 
                 + STRING(l-artikel.inhalt, ">>,>>9.99") 
                 + STRING(l-artikel.traubensort, "x(8)") 
                 + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(0, ">,>>>,>>>,>>9") 
                 + STRING(tot-anz, " ->>>,>>9.99") 
                 + STRING(0, "->>,>>>,>>>,>>9")
                 + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                 + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
            END. 
          END. 
        END. 
        ELSE
        /* End of add */
            FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
              FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
              AND l-artikel.endkum = from-grp NO-LOCK, 
              FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum 
              AND (l-untergrup.betriebsnr GE grp1 AND l-untergrup.betriebsnr LE grp2) 
                NO-LOCK BY l-artikel.zwkum BY l-artikel.bezeich: 
              i = i + 1. 
              must-order = 0.

              IF zwkum = 0 THEN 
              DO: 
                zwkum = l-artikel.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 
              IF zwkum NE l-artikel.zwkum THEN 
              DO: 
                create str-list. 
                str-list.flag = 1. 
                str-list.s = "       ". 
                str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
                DO j = 1 TO 84: 
                  str-list.s = str-list.s + " ". 
                END. 
                IF NOT long-digit THEN 
                  str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
                ELSE 
                  str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
                create str-list. 
                t-anz = 0. 
                t-val = 0.                 
                zwkum = l-untergrup.zwkum. 
                bezeich = l-untergrup.bezeich. 
              END. 

              tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                        - l-bestand.anz-ausgang. 
              IF show-price THEN 
                tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
                        - l-bestand.wert-ausgang. 

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

              IF tot-anz NE 0 OR (tot-anz = 0 AND zero-flag) THEN 
              DO: 
                create str-list. 
                IF show-price THEN 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.ek-aktuell, ">>>,>>>,>>9.99") 
                     + STRING(l-artikel.vk-preis, "->>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(l-artikel.ek-letzter, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9") 
                     + STRING(l-artikel.vk-preis, "->,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(tot-val, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
                ELSE 
                DO: 
                  IF NOT long-digit THEN 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(0, ">>,>>>,>>9.99") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>>,>>>,>>9.99")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                  ELSE 
                  str-list.s = STRING(l-artikel.artnr, "9999999") 
                     + STRING(l-artikel.bezeich, "x(50)") 
                     + STRING(l-artikel.masseinheit, "x(3)") 
                     + STRING(l-artikel.inhalt, ">>,>>9.99") 
                     + STRING(l-artikel.traubensort, "x(8)") 
                     + STRING(l-artikel.lief-einheit, ">>,>>9.99") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(0, ">,>>>,>>>,>>9") 
                     + STRING(tot-anz, " ->>>,>>9.99") 
                     + STRING(0, "->>,>>>,>>>,>>9")
                     + STRING(l-artikel.min-bestand, ">>,>>>") /*gerald min-stock, B3E18C*/
                     + STRING(must-order, "->,>>>,>>9.99"). /*FD Feb 18, 2022*/
                END. 
              END. 
            END. 
 
    IF t-val NE 0 THEN 
    DO: 
      create str-list. 
      str-list.flag = 1. 
      str-list.s = "       ". 
      str-list.s = str-list.s + STRING(bezeich, "x(50)"). 
      DO j = 1 TO 84: 
        str-list.s = str-list.s + " ". 
      END. 
      IF NOT long-digit THEN 
        str-list.s = str-list.s + STRING(t-val, "->>>,>>>,>>9.99"). 
      ELSE 
        str-list.s = str-list.s + STRING(t-val, "->>,>>>,>>>,>>9"). 
      create str-list. 
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
  create str-list. 
  str-list.flag = 1. 
  str-list.s = "       ". 
  str-list.s = str-list.s + STRING("GRAND T O T A L", "x(50)"). 
  DO j = 1 TO 84: 
    str-list.s = str-list.s + " ". 
  END. 
  IF NOT long-digit THEN 
    str-list.s = str-list.s + STRING(tt-value, "->>>,>>>,>>9.99"). 
  ELSE 
    str-list.s = str-list.s + STRING(tt-value, "->>,>>>,>>>,>>9").  
END. 

