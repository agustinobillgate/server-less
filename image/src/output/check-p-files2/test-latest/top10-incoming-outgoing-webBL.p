

DEF TEMP-TABLE str-list
    FIELD artnr-no      AS INT 
    FIELD artikel-name  AS CHAR
    FIELD qty           AS DECIMAL 
    FIELD unit-price    AS DECIMAL 
    FIELD tot-price     AS DECIMAL 
    FIELD tot-incoming  AS DECIMAL
    FIELD tot-outgoing  AS DECIMAL 
.

DEF TEMP-TABLE str-list-output
    FIELD artnr-no      AS INT 
    FIELD artikel-name  AS CHAR
    FIELD qty           AS DECIMAL 
    FIELD unit-price    AS DECIMAL 
    FIELD tot-price     AS DECIMAL 
    FIELD turnover      AS DECIMAL 
    FIELD tot-outgoing  AS DECIMAL 
.

DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER from-grp AS INT.
DEF INPUT PARAMETER to-grp AS INT.
DEF INPUT PARAMETER store AS INT.
DEF INPUT PARAMETER sorttype AS INT.
DEF OUTPUT PARAMETER TABLE FOR str-list-output.

DEF VARIABLE tot-qty AS INT INITIAL 0.
DEF VARIABLE qty AS INT INITIAL 0.
DEF VARIABLE counter AS INT INITIAL 0.
DEF VARIABLE unit-price AS DECIMAL.
DEF VARIABLE tot-price AS DECIMAL.
DEF VARIABLE tot-incoming AS INT.
DEF VARIABLE tot-outgoing AS INT.


IF sorttype = 0 THEN 
DO:
    RUN incoming-procedure.   
END.
ELSE 
DO:
    RUN outgoing-procedure.
END.


PROCEDURE incoming-procedure:
    IF store = 0 THEN 
    DO:
        tot-qty = 0.
        qty = 0.
        tot-outgoing = 0.
        tot-price = 0.
        tot-incoming = 0.

        FOR EACH str-list:
            DELETE str-list.
        END.

        FOR EACH l-ophis WHERE l-ophis.datum GE from-date            
            AND l-ophis.datum LE to-date 
            AND l-ophis.lief-nr GT 0 
            AND l-ophis.op-art EQ 1 
            AND l-ophis.anzahl NE 0 
            AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
            AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED") NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
            AND l-artikel.endkum GE from-grp
            AND l-artikel.endkum LE to-grp NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
            BY l-lieferant.firma BY l-ophis.datum BY l-artikel.bezeich: 
          
            FIND FIRST str-list WHERE str-list.artnr-no = l-ophis.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-ophis.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-ophis.anzahl
                    str-list.unit-price = l-ophis.einzelpreis
                    str-list.tot-price = l-ophis.einzelpreis * l-ophis.anzahl
                    str-list.tot-incoming = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-ophis.anzahl.
                str-list.tot-price = str-list.tot-price + (l-ophis.einzelpreis * l-ophis.anzahl).
                str-list.tot-incoming = str-list.tot-incoming + 1.        
            END.    
        END. /*end foreach close*/
          
        FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
            AND l-op.lief-nr GT 0 
            AND l-op.loeschflag LE 1
            AND l-op.op-art = 1 NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            AND l-artikel.endkum GE from-grp   
            AND l-artikel.endkum LE to-grp NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
            BY l-op.artnr BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich:

            FIND FIRST str-list WHERE str-list.artnr-no = l-op.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-op.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-op.anzahl
                    str-list.unit-price = l-op.einzelpreis
                    str-list.tot-price = l-op.einzelpreis * l-op.anzahl
                    str-list.tot-incoming = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-op.anzahl.
                str-list.tot-price = str-list.tot-price + (l-op.einzelpreis * l-op.anzahl).
                str-list.tot-incoming = str-list.tot-incoming + 1.      
            END. 
        END. /*end foreach*/

        FOR EACH str-list-output:
            DELETE str-list-output.
        END.
       
        FOR EACH str-list BY str-list.tot-incoming DESCENDING:
            counter = counter + 1.

            CREATE str-list-output.
            ASSIGN 
                str-list-output.artnr-no =  str-list.artnr-no
                str-list-output.artikel-name = str-list.artikel-name
                str-list-output.qty = str-list.qty
                str-list-output.unit-price = str-list.tot-price / str-list.tot-incoming
                str-list-output.tot-price = str-list.tot-price
                str-list-output.turnover = str-list.tot-incoming
               /*str-list-output.turnover = str-list.tot-outgoing.*/
                
            tot-qty = tot-qty + str-list.qty.
            tot-incoming = tot-incoming + str-list.tot-incoming.
            IF counter EQ 100 THEN LEAVE.  
        END.
        
        CREATE str-list-output.
        ASSIGN
            str-list-output.artnr-no = 0
            str-list-output.artikel-name = "TOTAL : "
            str-list-output.qty = tot-qty
            str-list-output.unit-price = 0
            str-list-output.tot-price = 0
            str-list-output.turnover = tot-incoming.
            /*str-list-output.turnover = 0.*/
                
    END. /*end store*/
    ELSE
    DO:
        tot-qty = 0.
        qty = 0.
        tot-outgoing = 0.
        tot-price = 0.
        tot-incoming = 0.

        FOR EACH str-list:
            DELETE str-list.
        END.

        FOR EACH l-ophis WHERE l-ophis.datum GE from-date            
            AND l-ophis.datum LE to-date 
            AND l-ophis.lief-nr GT 0 
            AND l-ophis.op-art EQ 1 
            AND l-ophis.anzahl NE 0 
            AND l-ophis.lager-nr = store
            AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
            AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED") NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
            AND l-artikel.endkum GE from-grp
            AND l-artikel.endkum LE to-grp NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
            BY l-lieferant.firma BY l-ophis.datum BY l-artikel.bezeich: 
          
            FIND FIRST str-list WHERE str-list.artnr-no = l-ophis.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-ophis.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-ophis.anzahl
                    str-list.unit-price = l-ophis.einzelpreis
                    str-list.tot-price = l-ophis.einzelpreis * l-ophis.anzahl
                    str-list.tot-incoming = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-ophis.anzahl.
                str-list.tot-price = str-list.tot-price + (l-ophis.einzelpreis * l-ophis.anzahl).
                str-list.tot-incoming = str-list.tot-incoming + 1.        
            END.    
        END. /*end foreach close*/
    
                
        FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
            AND l-op.lief-nr GT 0 
            AND l-op.loeschflag LE 1
            AND l-op.op-art = 1 
            AND l-op.lager-nr = store NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            AND l-artikel.endkum GE from-grp   
            AND l-artikel.endkum LE to-grp NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
            BY l-op.artnr BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich:
    
            FIND FIRST str-list WHERE str-list.artnr-no = l-op.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO:  
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-op.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-op.anzahl
                    str-list.unit-price = l-op.einzelpreis
                    str-list.tot-price = l-op.einzelpreis * l-op.anzahl
                    str-list.tot-incoming = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-op.anzahl.
                str-list.tot-price = str-list.tot-price + (l-op.einzelpreis * l-op.anzahl).
                str-list.tot-incoming = str-list.tot-incoming + 1.      
            END. 
        END. /*end foreach*/

        FOR EACH str-list-output:
            DELETE str-list-output.
        END.
       
        FOR EACH str-list BY str-list.tot-incoming DESCENDING:
            counter = counter + 1.
            CREATE str-list-output.
            ASSIGN 
                str-list-output.artnr-no =  str-list.artnr-no
                str-list-output.artikel-name = str-list.artikel-name
                str-list-output.qty = str-list.qty
                str-list-output.unit-price = str-list.tot-price / str-list.tot-incoming
                str-list-output.tot-price = str-list.tot-price
                str-list-output.turnover = str-list.tot-incoming
               /*str-list-output.turnover = str-list.tot-outgoing.*/
                
            tot-qty = tot-qty + str-list.qty.
            tot-incoming = tot-incoming + str-list.tot-incoming.

            IF counter EQ 100 THEN LEAVE.  
        END.
        
        CREATE str-list-output.
        ASSIGN
            str-list-output.artnr-no = 0
            str-list-output.artikel-name = "TOTAL : "
            str-list-output.qty = tot-qty
            str-list-output.unit-price = 0
            str-list-output.tot-price = 0
            str-list-output.turnover = tot-incoming.
            /*str-list-output.turnover = 0.*/

            
                
    END. /*end store*/
END PROCEDURE. /*end procedure*/

PROCEDURE outgoing-procedure:
    IF store = 0 THEN 
    DO:
        tot-qty = 0.
        qty = 0.
        tot-outgoing = 0.
        tot-price = 0.
        tot-incoming = 0.

        FOR EACH str-list:
            DELETE str-list.
        END.

        FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date
            AND l-ophis.anzahl NE 0 AND l-ophis.op-art = 3 NO-LOCK,
            FIRST l-ophhis WHERE l-ophhis.op-typ = "STT" 
            AND l-ophhis.lscheinnr = l-ophis.lscheinnr 
            AND l-ophhis.fibukonto NE "" NO-LOCK, 
            FIRST l-lager WHERE l-lager.lager-nr EQ l-ophis.lager-nr NO-LOCK,
            FIRST gl-acct WHERE gl-acct.fibukonto = l-ophhis.fibukonto NO-LOCK, 
            FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr
            AND l-artikel.endkum GE from-grp
            AND l-artikel.endkum LE to-grp NO-LOCK
            BY l-ophis.lscheinnr BY l-ophis.artnr:
          
            FIND FIRST str-list WHERE str-list.artnr-no = l-ophis.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-ophis.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-ophis.anzahl
                    str-list.unit-price = l-ophis.einzelpreis
                    str-list.tot-price = l-ophis.einzelpreis * l-ophis.anzahl
                    str-list.tot-outgoing = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-ophis.anzahl.
                str-list.tot-price = str-list.tot-price + (l-ophis.einzelpreis * l-ophis.anzahl).
                str-list.tot-outgoing = str-list.tot-outgoing + 1.        
            END.  
        END. /*end foreach close*/
    
                
        /*FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
            AND l-op.lief-nr GT 0 
            AND l-op.loeschflag LE 1
            AND l-op.op-art = 1 NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            AND l-artikel.endkum GE from-grp   
            AND l-artikel.endkum LE to-grp NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
            BY l-op.artnr BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich:*/

            FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
                AND l-op.anzahl NE 0 AND l-op.op-art = 3 
                AND l-op.loeschflag LE 1  NO-LOCK USE-INDEX artopart_ix, 
                FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
                AND l-ophdr.lscheinnr = l-op.lscheinnr 
                AND l-ophdr.fibukonto NE "" NO-LOCK, 
                FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr
                AND l-artikel.endkum GE from-grp
                AND l-artikel.endkum LE to-grp NO-LOCK 
                BY l-op.lscheinnr BY l-op.artnr:   
    
            FIND FIRST str-list WHERE str-list.artnr-no = l-op.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO: 
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-op.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-op.anzahl
                    str-list.unit-price = l-op.einzelpreis
                    str-list.tot-price = l-op.einzelpreis * l-op.anzahl
                    str-list.tot-outgoing = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-op.anzahl.
                str-list.tot-price = str-list.tot-price + (l-op.einzelpreis * l-op.anzahl).
                str-list.tot-outgoing = str-list.tot-outgoing + 1.      
            END. 
        END. /*end foreach*/

        FOR EACH str-list-output:
            DELETE str-list-output.
        END.
       
        FOR EACH str-list BY str-list.tot-outgoing DESCENDING:
            counter = counter + 1.
            CREATE str-list-output.
            ASSIGN 
                str-list-output.artnr-no =  str-list.artnr-no
                str-list-output.artikel-name = str-list.artikel-name
                str-list-output.qty = str-list.qty
                str-list-output.unit-price = str-list.tot-price / str-list.tot-outgoing
                str-list-output.tot-price = str-list.tot-price
                /*str-list-output.tot-incoming = str-list.tot-incoming*/
                str-list-output.turnover = str-list.tot-outgoing
                tot-qty = tot-qty + str-list.qty
                tot-outgoing  = tot-outgoing + str-list.tot-outgoing.
            IF counter EQ 100 THEN LEAVE.  
        END.
        
        CREATE str-list-output.
        ASSIGN
            str-list-output.artnr-no = 0
            str-list-output.artikel-name = "TOTAL"
            str-list-output.qty = tot-qty
            str-list-output.unit-price = 0
            str-list-output.tot-price = 0
            /*str-list-output.tot-incoming = 0*/
            str-list-output.turnover = tot-outgoing.
    END.
    ELSE 
    DO:
        tot-qty = 0.
        qty = 0.
        tot-outgoing = 0.
        tot-price = 0.
        tot-incoming = 0.

        FOR EACH str-list:
            DELETE str-list.
        END.

        FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND l-ophis.datum LE to-date
            AND l-ophis.anzahl NE 0 AND l-ophis.op-art = 3 NO-LOCK,
            FIRST l-ophhis WHERE l-ophhis.op-typ = "STT" 
            AND l-ophhis.lscheinnr = l-ophis.lscheinnr 
            AND l-ophhis.fibukonto NE ""  
            AND l-ophis.lager-nr = store NO-LOCK,
            FIRST gl-acct WHERE gl-acct.fibukonto = l-ophhis.fibukonto NO-LOCK, 
            FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr
            AND l-artikel.endkum GE from-grp
            AND l-artikel.endkum LE to-grp NO-LOCK
            BY l-ophis.lscheinnr BY l-ophis.artnr:
          
            FIND FIRST str-list WHERE str-list.artnr-no = l-ophis.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-ophis.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-ophis.anzahl
                    str-list.unit-price = l-ophis.einzelpreis
                    str-list.tot-price = l-ophis.einzelpreis * l-ophis.anzahl
                    str-list.tot-outgoing = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-ophis.anzahl.
                str-list.tot-price = str-list.tot-price + (l-ophis.einzelpreis * l-ophis.anzahl).
                str-list.tot-outgoing = str-list.tot-outgoing + 1.        
            END.  
        END. /*end foreach close*/
    
                
        /*FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
            AND l-op.lief-nr GT 0 
            AND l-op.loeschflag LE 1
            AND l-op.op-art = 1 NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            AND l-artikel.endkum GE from-grp   
            AND l-artikel.endkum LE to-grp NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
            BY l-op.artnr BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich:*/

            FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
                AND l-op.anzahl NE 0 AND l-op.op-art = 3 
                AND l-op.loeschflag LE 1  
                AND l-op.lager-nr = store NO-LOCK USE-INDEX artopart_ix, 
                FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
                AND l-ophdr.lscheinnr = l-op.lscheinnr 
                AND l-ophdr.fibukonto NE "" NO-LOCK, 
                FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr
                AND l-artikel.endkum GE from-grp
                AND l-artikel.endkum LE to-grp NO-LOCK 
                BY l-op.lscheinnr BY l-op.artnr:   
    
            FIND FIRST str-list WHERE str-list.artnr-no = l-op.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE str-list THEN 
            DO: 
                CREATE str-list.
                ASSIGN
                    str-list.artnr-no = l-op.artnr
                    str-list.artikel-name = l-artikel.bezeich
                    str-list.qty = l-op.anzahl
                    str-list.unit-price = l-op.einzelpreis
                    str-list.tot-price = l-op.einzelpreis * l-op.anzahl
                    str-list.tot-outgoing = 1.
            END.
            ELSE 
            DO:
                str-list.qty = str-list.qty + l-op.anzahl.
                str-list.tot-price = str-list.tot-price + (l-op.einzelpreis * l-op.anzahl).
                str-list.tot-outgoing = str-list.tot-outgoing + 1.      
            END. 
        END. /*end foreach*/

        FOR EACH str-list-output:
            DELETE str-list-output.
        END.
       
        FOR EACH str-list BY str-list.tot-outgoing DESCENDING:
            counter = counter + 1.
            CREATE str-list-output.
            ASSIGN 
                str-list-output.artnr-no =  str-list.artnr-no
                str-list-output.artikel-name = str-list.artikel-name
                str-list-output.qty = str-list.qty
                str-list-output.unit-price = str-list.tot-price / str-list.tot-outgoing
                str-list-output.tot-price = str-list.tot-price
                /*str-list-output.tot-incoming = str-list.tot-incoming*/
                str-list-output.turnover = str-list.tot-outgoing
                tot-qty = tot-qty + str-list.qty
                tot-outgoing  = tot-outgoing + str-list.tot-outgoing.
            IF counter EQ 100 THEN LEAVE.  
        END.
        
        CREATE str-list-output.
        ASSIGN
            str-list-output.artnr-no = 0
            str-list-output.artikel-name = "TOTAL"
            str-list-output.qty = tot-qty
            str-list-output.unit-price = 0
            str-list-output.tot-price = 0
            /*str-list-output.tot-incoming = 0*/
            str-list-output.turnover = tot-outgoing.
    END.
           
END PROCEDURE. /*end procedure*/













