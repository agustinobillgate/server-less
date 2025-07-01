DEFINE WORKFILE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE output-list
    FIELD str AS CHAR
    FIELD pos AS INT.

DEFINE TEMP-TABLE po-list
    FIELD bestelldatum         AS DATE    LABEL "Date"
    FIELD bezeich              AS CHAR    LABEL "Department"
    FIELD firma                AS CHAR    LABEL "Supplier Name"
    FIELD docu-nr              AS CHAR    LABEL "Po Number"
    FIELD odrhdr-lieferdatum   AS DATE    LABEL "Delivery"
    FIELD bestellart           AS CHAR    LABEL "Order Type"
    FIELD besteller            AS CHAR    LABEL "Order By"
    FIELD lief-fax2            AS CHAR    LABEL "Modified-By" 
    FIELD order1-lieferdatum   AS DATE    LABEL "ModDate"
    FIELD lief-fax3            AS CHAR    LABEL "Closed By"
    FIELD lieferdatum-eff      AS DATE    LABEL "CloseDate"
    FIELD rechnungswert        AS DECIMAL FORMAT " ->>,>>>,>>9.99" LABEL "Balance"
    FIELD pr-number            AS CHARACTER.

DEFINE TEMP-TABLE detail-po-list
    FIELD bestelldatum         AS DATE    LABEL "Date"
    FIELD artnr                AS CHAR    LABEL "Art No"
    FIELD bezeich              AS CHAR    LABEL "Description" 
    FIELD lief-fax3            AS CHAR    LABEL "DeliverUnit"
    FIELD txtnr                AS INT     LABEL "Cont"
    FIELD anzahl               AS DECIMAL FORMAT "->>>,>>9.99 "     LABEL "Quantity"
    FIELD einzelpreis          AS DECIMAL FORMAT " >,>>>,>>>,>>9 "  LABEL "Unit-Price"
    FIELD warenwert            AS DECIMAL FORMAT "->>,>>>,>>>,>>9 " LABEL "Amount"
    FIELD geliefert            AS DECIMAL FORMAT "->,>>>,>>9.99 "   LABEL "Deliv-DUnit"
    FIELD angebot-lief1        AS INT     LABEL "S-Unit". 

DEFINE buffer l-odrhdr FOR l-orderhdr. 
DEFINE buffer l-order1 FOR l-order. 
DEFINE buffer l-order2 FOR l-order. 
DEFINE buffer l-supplier FOR l-lieferant. 
DEFINE buffer l-art FOR l-artikel. 
DEFINE buffer l-art2 FOR l-artikel. 

DEF INPUT  PARAMETER case-type          AS INT.
DEF INPUT  PARAMETER all-supp           AS LOGICAL.
DEF INPUT  PARAMETER stattype           AS INT.
DEF INPUT  PARAMETER deptno             AS INT. /*Dept Nr Eko 010615*/
DEF INPUT  PARAMETER from-date          AS DATE.
DEF INPUT  PARAMETER to-date            AS DATE.
DEF INPUT  PARAMETER billdate           AS DATE.
DEF INPUT  PARAMETER disp-comm          AS LOGICAL.
DEF INPUT  PARAMETER l-orderhdr-docu-nr AS CHAR.
DEF INPUT  PARAMETER str4               AS CHAR.
DEF INPUT  PARAMETER l-supp-lief-nr     AS INT.
DEF INPUT  PARAMETER dml-only           AS LOGICAL. /* Oscar -  */
DEF INPUT  PARAMETER pr-only            AS LOGICAL. /* Oscar -  */
DEF INPUT  PARAMETER excl-dml-pr        AS LOGICAL. /* Oscar -  */
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR po-list.
DEF OUTPUT PARAMETER TABLE FOR detail-po-list.

/*
DEF VARIABLE case-type          AS INT      INIT 2.
DEF VARIABLE all-supp           AS LOGICAL  INIT YES.
DEF VARIABLE stattype           AS INT      INIT 0.
DEF VARIABLE deptno             AS INT      INIT -1.
DEF VARIABLE from-date          AS DATE     INIT 01/01/19.
DEF VARIABLE to-date            AS DATE     INIT 01/14/19.
DEF VARIABLE billdate           AS DATE     INIT 01/14/19.
DEF VARIABLE disp-comm          AS LOGICAL  INIT YES.
DEF VARIABLE l-orderhdr-docu-nr AS CHAR     INIT "".
DEF VARIABLE str4               AS CHAR     INIT "".
DEF VARIABLE l-supp-lief-nr     AS INT      INIT 0. 
*/
DEFINE VARIABLE ind         AS INTEGER  NO-UNDO. 
DEFINE VARIABLE l-order1-lieferdatum AS CHAR FORMAT "x(8)".
DEFINE VARIABLE l-order1-lieferdatum-eff AS CHAR FORMAT "x(8)".
DEFINE VARIABLE l-odrhdr-lieferdatum AS CHAR FORMAT "x(8)".
DEFINE VARIABLE l-order1-rechnungswert AS CHAR FORMAT "->,>>>,>>>,>>9.99".

RUN create-costlist.

IF case-type = 1 THEN RUN print-polist1.
ELSE IF case-type = 2 THEN RUN print-polist2.
ELSE IF case-type = 3 THEN RUN print-polist11.
ELSE IF case-type = 4 THEN RUN print-polist22.
ELSE IF case-type = 5 THEN RUN print-polist1a.
ELSE IF case-type = 6 THEN RUN print-polist2a.
ELSE IF case-type = 7 THEN RUN print-polist11a.
ELSE IF case-type = 8 THEN RUN print-polist22a.
ELSE IF case-type = 9 THEN RUN print-polist1b.
ELSE IF case-type = 10 THEN RUN print-polist2b.
ELSE IF case-type = 11 THEN RUN print-polist11b.
ELSE IF case-type = 12 THEN RUN print-polist22b.
/*
current-window:width = 200.
FOR EACH po-list NO-LOCK:
    DISP
        po-list WITH WIDTH 190.
END.
*/

PROCEDURE create-costlist: 
    FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
        CREATE cost-list. 
        cost-list.nr = INTEGER(parameters.varname). 
        cost-list.bezeich = parameters.vstring. 
    END. 
END. 

PROCEDURE print-polist1:
    DEFINE VARIABLE do-it AS LOGICAL INIT NO.

    CREATE output-list.
    CREATE detail-po-list.
    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /* Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:

               
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                    IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                    DO:                                                                                                                                
                        IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                        ELSE                                                 
                        DO:                                                                                                                              
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                            ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                        END.                                                                                                                             
                    END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                /*MT*/
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN 
                        output-list.str = output-list.str + STRING(l-order2.artnr, "9999999 ")
                                        + STRING(l-art2.bezeich, "x(24) ")
                                        + STRING(l-order2.lief-fax[3], "x(12) ")
                                        + STRING(l-order2.txtnr, " >>9 ")
                                        + STRING(l-order2.anzahl, "->>>,>>9.99 ")
                                        + STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ")
                                        + STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ")
                                        + STRING(l-order2.geliefert, "->,>>>,>>9.99 ")
                                        + STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list. 
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno /*Eko 010615*/ NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.  
              
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    RUN order-instruction-detail.
                END. 
                /*MT*/
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN 
                        output-list.str = output-list.str + STRING(l-order2.artnr, "9999999 ")
                                        + STRING(l-art2.bezeich, "x(24) ")
                                        + STRING(l-order2.lief-fax[3], "x(12) ")
                                        + STRING(l-order2.txtnr, " >>9 ")
                                        + STRING(l-order2.anzahl, "->>>,>>9.99 ")
                                        + STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ")
                                        + STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ")
                                        + STRING(l-order2.geliefert, "->,>>>,>>9.99 ")
                                        + STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                             
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /* Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN 
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                       DO:                                                                                                                                
                           IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                   output-list.str = output-list.str + STRING(" ")
                                   detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                           ELSE                                                 
                           DO:                                                                                                                              
                               ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                               ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                           END.                                                                                                                             
                       END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                               
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno /*Eko 010615*/ NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0 NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN 
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                       DO:                                                                                                                                
                           IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                   output-list.str = output-list.str + STRING(" ")
                                   detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                           ELSE                                                 
                           DO:                                                                                                                              
                               ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                               ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                           END.                                                                                                                             
                       END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                          
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /* Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN 
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum )
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").
                       
                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                       DO:                                                                                                                                
                           IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                   output-list.str = output-list.str + STRING(" ")
                                   detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                           ELSE                                                 
                           DO:                                                                                                                              
                               ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                               ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                           END.                                                                                                                             
                       END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END.
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                         
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1
            AND l-odrhdr.angebot-lief[1] EQ deptno /*Eko 010615*/ NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN 
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum )
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                       DO:                                                                                                                                
                           IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                   output-list.str = output-list.str + STRING(" ")
                                   detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                           ELSE                                                 
                           DO:                                                                                                                              
                               ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                               ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                           END.                                                                                                                             
                       END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END.
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                             
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /* Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0 NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN 
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                       DO:                                                                                                                                
                           IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                   output-list.str = output-list.str + STRING(" ")
                                   detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                           ELSE                                                 
                           DO:                                                                                                                              
                               ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                               ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                           END.                                                                                                                             
                       END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END.
                
                
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                               
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno /*Eko 010615*/ NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0 NO-LOCK 
            BY l-odrhdr.bestelldatum BY l-orderhdr-docu-nr BY l-supplier.firma:
                /* Oscar (13 September 2024) - 451E05 */
                ASSIGN 
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/
                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                       DO:                                                                                                                                
                           IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                   output-list.str = output-list.str + STRING(" ")
                                   detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                           ELSE                                                 
                           DO:                                                                                                                              
                               ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                               ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                           END.                                                                                                                             
                       END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END.
                
                
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.                                             
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist2:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 

    DEFINE VARIABLE statflag AS INTEGER.
    DEFINE VARIABLE tes      AS CHAR.
    DEFINE VARIABLE do-it    AS LOGICAL.

    CREATE output-list.
    CREATE po-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO:
            
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN 
                        output-list.str = output-list.str  
                                        + STRING(l-odrhdr.bestelldatum)  
                                        + STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").
                    
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert 
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.
                    
                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO: 
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END.
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:

                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").
                    
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.
                    
                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.
                    
                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO: 
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END.
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO:   
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0 NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma: 

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").
                    
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0 NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma: 

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").
                
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").
                    
                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END.
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO:  
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma: 

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").
                    
                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                    CREATE po-list.
                    
                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO: 
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END.
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma: 

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:

                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.
                        
                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO: 
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0 NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                
                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO: 
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
        ELSE DO:       
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0 NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    /* Oscar (13 September 2024) - 451E05 */
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").
                    
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.
                    
                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO: 
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist11:
    DEFINE buffer l-odrhdr   FOR l-orderhdr. 
    DEFINE buffer l-order1   FOR l-order. 
    DEFINE buffer l-order2   FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art      FOR l-artikel. 
    DEFINE buffer l-art2     FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    
    DEFINE buffer l-supp FOR l-lieferant.
    
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.
            
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
            
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.
            
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
            
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END.
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/    
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-order2.artnr, "9999999 ") +
                        STRING(l-art2.bezeich, "x(24) ") +
                        STRING(l-order2.lief-fax[3], "x(12) ") +
                        STRING(l-order2.txtnr, " >>9 ") +
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") +
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") +
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") +
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") +
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] = deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list. 

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-order2.artnr, "9999999 ") +
                        STRING(l-art2.bezeich, "x(24) ") +
                        STRING(l-order2.lief-fax[3], "x(12) ") +
                        STRING(l-order2.txtnr, " >>9 ") +
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") +
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") +
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") +
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") +
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
            
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-order2.artnr, "9999999 ") +
                        STRING(l-art2.bezeich, "x(24) ") +
                        STRING(l-order2.lief-fax[3], "x(12) ") +
                        STRING(l-order2.txtnr, " >>9 ") +
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") +
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") +
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") +
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") +
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
           END.
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
            
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-order2.artnr, "9999999 ") +
                        STRING(l-art2.bezeich, "x(24) ") +
                        STRING(l-order2.lief-fax[3], "x(12) ") +
                        STRING(l-order2.txtnr, " >>9 ") +
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") +
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") +
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") +
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") +
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
                
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-order2.artnr, "9999999 ") +
                        STRING(l-art2.bezeich, "x(24) ") +
                        STRING(l-order2.lief-fax[3], "x(12) ") +
                        STRING(l-order2.txtnr, " >>9 ") +
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") +
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") +
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") +
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") +
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END.
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                       

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO:
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 
                
                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str +
                        STRING(l-order2.artnr, "9999999 ") +
                        STRING(l-art2.bezeich, "x(24) ") +
                        STRING(l-order2.lief-fax[3], "x(12) ") +
                        STRING(l-order2.txtnr, " >>9 ") +
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") +
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") +
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") +
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") +
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END.
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist22:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 

    DEFINE VARIABLE statflag AS INTEGER. 
    DEFINE VARIABLE do-it    AS LOGICAL.

    CREATE output-list.
    CREATE po-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum GE billdate 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.
                    
                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum GE billdate 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).
                    
                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.
                    
                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END.
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/ 
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum LT billdate 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
        ELSE DO: 
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lieferdatum LT billdate 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUN create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/       
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:
                
                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUn create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
        ELSE DO: 
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
                AND l-odrhdr.bestelldatum LE to-date 
                AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
                AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
                FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
                FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
                AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
                BY l-odrhdr.bestelldatum BY /*MTl-orderhdr*/ l-odrhdr.docu-nr BY l-supplier.firma:

                do-it = NO.

                IF dml-only THEN 
                DO:
                    IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                        do-it = YES.
                END.
                ELSE IF pr-only THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN 
                        do-it = YES.
                END.
                ELSE IF excl-dml-pr THEN
                DO:
                    IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                        (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN
                            do-it = YES.
                END.
                ELSE do-it = YES.

                IF do-it EQ YES THEN
                DO:
                    IF l-order1.lieferdatum = ? THEN
                        l-order1-lieferdatum = "".
                    ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                    IF l-order1.lieferdatum-eff = ? THEN
                        l-order1-lieferdatum-eff = "".
                    ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                    l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                    l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-odrhdr.bestelldatum) + 
                        STRING(" ").

                    FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                    IF AVAILABLE cost-list THEN 
                    DO: 
                        output-list.str = output-list.str + cost-list.bezeich.
                        po-list.bezeich = cost-list.bezeich.
                    END.
                    ELSE 
                    DO:
                        output-list.str = output-list.str + " ".
                        po-list.bezeich = "".
                    END.
                    output-list.str = output-list.str + STRING(" ").

                    ASSIGN output-list.str = output-list.str +
                        STRING(l-supplier.firma, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.docu-nr, "x(16)") + 
                        STRING(" ") +
                        STRING(l-odrhdr-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.bestellart, "x(10)") + 
                        STRING(" ") +
                        STRING(l-odrhdr.besteller, "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[2], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1.lief-fax[3], "x(12)") + 
                        STRING(" ") +
                        STRING(l-order1-lieferdatum-eff, "x(8)") + 
                        STRING(" ") +
                        STRING(l-order1-rechnungswert) /*MT*/.

                    CREATE output-list.
                    /*RUn create-po-list.*/
                    ASSIGN /*Agung*/                                          
                        po-list.bestelldatum        = l-odrhdr.bestelldatum   
                        po-list.firma               = l-supplier.firma        
                        po-list.docu-nr             = l-odrhdr.docu-nr        
                        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                        po-list.bestellart          = l-odrhdr.bestellart     
                        po-list.besteller           = l-odrhdr.besteller      
                        po-list.lief-fax2           = l-order1.lief-fax[2]    
                        po-list.order1-lieferdatum  = l-order1.lieferdatum    
                        po-list.lief-fax3           = l-order1.lief-fax[3]    
                        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                        po-list.rechnungswert       = l-order1.rechnungswert
                        po-list.pr-number           = l-order1.lief-fax[1]
                        .                                                     
                    CREATE po-list.

                    IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                    DO:
                        /*RUN order-instruction-po.*/
                        ASSIGN 
                            output-list.str = output-list.str + STRING("  Order Instruction: ")
                            po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                        DO ind = 1 TO 80:                                                                                                         
                            IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                            DO:                                                                                                                     
                                IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                    ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                                ELSE                                                                                                                  
                                DO:                                                                                                                   
                                    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                    ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                                END.                                                                                                                  
                            END.                                                                                                                    
                        END.                                                                                                                                                                                                                   
                        ASSIGN 
                            output-list.str = output-list.str + STRING("")
                            po-list.firma = po-list.firma + STRING("").                                                                    
                        CREATE output-list.                                                                                                       
                        CREATE po-list.
                    END. 
                END.
            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist1a:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END.  
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                                                                                                        

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    RUN order-instruction-detail.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                    

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist2a:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER.
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUn create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.
                CREATE output-list.
                /*RUn create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.                                  
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*EKo 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist11a:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                       

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                       

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN 
    DO:
        IF deptno LE 0 THEN 
        DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                       

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                            .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                output-list.pos = 9
                output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                              

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                             

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                               

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                          

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                         

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.
            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist22a:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.                                            

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.                                           

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.                                            

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.                                            

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.                                  

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END.  
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END.  
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist1b:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                              

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                            .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                                  

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/ 
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                    

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                           

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                               

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum: 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                            

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                                  

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                                

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist2b:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER.
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-supplier.firma BY l-odrhdr.bestelldatum BY l-odrhdr.docu-nr:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist11b:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    CREATE output-list.

    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO:  /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                                

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                              

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.                                                                                                                                                   

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.                                              
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK,  /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.
                    
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 1 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich: 
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.                                              
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum:
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                            STRING(l-order2.artnr, "9999999 ") + 
                            STRING(l-art2.bezeich, "x(24) ") + 
                            STRING(l-order2.lief-fax[3], "x(12) ") + 
                            STRING(l-order2.txtnr, " >>9 ") + 
                            STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                            STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                            STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                            STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                            STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.
                    
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list. 
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 010615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum : 
                ASSIGN
                    output-list.pos = 9
                    output-list.str = output-list.str + STRING(l-odrhdr.bestelldatum)
                    output-list.str = output-list.str + STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO:
                    output-list.str        = output-list.str + cost-list.bezeich.
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + cost-list.bezeich.
                END.
                ELSE
                DO:
                    output-list.str        = output-list.str + " ".
                    detail-po-list.bezeich = STRING(l-odrhdr.bestelldatum) + " " + " ".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN
                    output-list.str = output-list.str + STRING(l-supplier.firma, "x(16)")
                    output-list.str = output-list.str + STRING(" ")
                    output-list.str = output-list.str + STRING(l-odrhdr.docu-nr)
                    output-list.str = output-list.str + STRING(" ").

                CREATE output-list.
                /*RUN detail-po-list1.*/

                ASSIGN                                                                                                                              
                    detail-po-list.bezeich      = detail-po-list.bezeich + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
                    detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
                CREATE detail-po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-detail.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
                    DO ind = 1 TO 80:                                                                                                                    
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
                        DO:                                                                                                                                
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                                ASSIGN 
                                    output-list.str = output-list.str + STRING(" ")
                                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
                            ELSE                                                 
                            DO:                                                                                                                              
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
                            END.                                                                                                                             
                        END.                                                                                                                               
                    END.                                                                                                                                                                                                                                         
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
                    CREATE output-list.                                                                                                                  
                    CREATE detail-po-list.
                END. 

                FOR EACH l-order2 WHERE l-order2.docu-nr = l-odrhdr.docu-nr 
                AND l-order2.loeschflag EQ 2 AND l-order2.pos GT 0 NO-LOCK, 
                FIRST l-art2 WHERE l-art2.artnr = l-order2.artnr NO-LOCK 
                BY l-art2.bezeich:
                    ASSIGN output-list.str = output-list.str + 
                        STRING(l-order2.artnr, "9999999 ") + 
                        STRING(l-art2.bezeich, "x(24) ") + 
                        STRING(l-order2.lief-fax[3], "x(12) ") + 
                        STRING(l-order2.txtnr, " >>9 ") + 
                        STRING(l-order2.anzahl, "->>>,>>9.99 ") + 
                        STRING(l-order2.einzelpreis, " >,>>>,>>>,>>9 ") + 
                        STRING(l-order2.warenwert, "->>,>>>,>>>,>>9 ") + 
                        STRING(l-order2.geliefert, "->,>>>,>>9.99 ") + 
                        STRING(l-order2.angebot-lief[1], "   >>9").
                    CREATE output-list.
                    /*RUN detail-po-list2.*/
                    ASSIGN /*Agung*/                                                     
                        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
                        detail-po-list.bezeich       = l-art2.bezeich                    
                        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
                        detail-po-list.txtnr         = l-order2.txtnr                    
                        detail-po-list.anzahl        = l-order2.anzahl                   
                        detail-po-list.einzelpreis   = l-order2.einzelpreis              
                        detail-po-list.warenwert     = l-order2.warenwert                
                        detail-po-list.geliefert     = l-order2.geliefert                
                        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
                        .                                                                
                    CREATE detail-po-list.
                END. 
                ASSIGN output-list.str = output-list.str + str4.
                CREATE output-list.
                ASSIGN output-list.str = output-list.str + STRING("").
                CREATE output-list.

            END. 
        END.
    END.
END PROCEDURE.

PROCEDURE print-polist22b:
    DEFINE buffer l-odrhdr FOR l-orderhdr. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE buffer l-order2 FOR l-order. 
    DEFINE buffer l-supplier FOR l-lieferant. 
    DEFINE buffer l-art FOR l-artikel. 
    DEFINE buffer l-art2 FOR l-artikel. 
    DEFINE VARIABLE statflag AS INTEGER. 
    CREATE output-list.
    
    IF stattype = 0 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list.
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum GE billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 1 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 2 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lieferdatum LT billdate 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, /*Eko 030615*/
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum:
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END. 
        END.
    END.
    ELSE IF stattype = 3 THEN DO:
        IF deptno LE 0 THEN DO: /*Eko 010615*/
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.

                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.

                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.                                                                                                                    
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END.  
        END.
        ELSE DO:
            FOR EACH l-odrhdr WHERE l-odrhdr.bestelldatum GE from-date 
            AND l-odrhdr.bestelldatum LE to-date 
            AND l-odrhdr.lief-nr = l-supp-lief-nr AND l-odrhdr.betriebsnr LE 1 
            AND l-odrhdr.angebot-lief[1] EQ deptno NO-LOCK, 
            FIRST l-supplier WHERE l-supplier.lief-nr = l-odrhdr.lief-nr NO-LOCK, 
            FIRST l-order1 WHERE l-order1.docu-nr = l-odrhdr.docu-nr 
            AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
            BY l-odrhdr.docu-nr BY l-supplier.firma BY l-odrhdr.bestelldatum :
                IF l-order1.lieferdatum = ? THEN
                    l-order1-lieferdatum = "".
                ELSE l-order1-lieferdatum = STRING(l-order1.lieferdatum).
                IF l-order1.lieferdatum-eff = ? THEN
                    l-order1-lieferdatum-eff = "".
                ELSE l-order1-lieferdatum-eff = STRING(l-order1.lieferdatum-eff).

                l-odrhdr-lieferdatum = STRING(l-odrhdr.lieferdatum).
                l-order1-rechnungswert = STRING(l-order1.rechnungswert, " ->>,>>>,>>9.99").

                ASSIGN output-list.str = output-list.str + 
                    STRING(l-odrhdr.bestelldatum) + 
                    STRING(" ").

                FIND FIRST cost-list WHERE cost-list.nr EQ l-odrhdr.angebot-lief[1] NO-LOCK NO-ERROR.
                IF AVAILABLE cost-list THEN 
                DO: 
                    output-list.str = output-list.str + cost-list.bezeich.
                    po-list.bezeich = cost-list.bezeich.
                END.
                ELSE 
                DO:
                    output-list.str = output-list.str + " ".
                    po-list.bezeich = "".
                END.
                output-list.str = output-list.str + STRING(" ").

                ASSIGN output-list.str = output-list.str +
                    STRING(l-supplier.firma, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.docu-nr, "x(16)") + 
                    STRING(" ") +
                    STRING(l-odrhdr-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.bestellart, "x(10)") + 
                    STRING(" ") +
                    STRING(l-odrhdr.besteller, "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[2], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1.lief-fax[3], "x(12)") + 
                    STRING(" ") +
                    STRING(l-order1-lieferdatum-eff, "x(8)") + 
                    STRING(" ") +
                    STRING(l-order1-rechnungswert) /*MT*/.
                    
                CREATE output-list.
                /*RUN create-po-list.*/
                ASSIGN /*Agung*/                                          
                    po-list.bestelldatum        = l-odrhdr.bestelldatum   
                    po-list.firma               = l-supplier.firma        
                    po-list.docu-nr             = l-odrhdr.docu-nr        
                    po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
                    po-list.bestellart          = l-odrhdr.bestellart     
                    po-list.besteller           = l-odrhdr.besteller      
                    po-list.lief-fax2           = l-order1.lief-fax[2]    
                    po-list.order1-lieferdatum  = l-order1.lieferdatum    
                    po-list.lief-fax3           = l-order1.lief-fax[3]    
                    po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
                    po-list.rechnungswert       = l-order1.rechnungswert
                    po-list.pr-number           = l-order1.lief-fax[1]
                    .                                                     
                CREATE po-list.
                
                IF disp-comm AND l-odrhdr.lief-fax[3] NE "" THEN 
                DO: 
                    /*RUN order-instruction-po.*/
                    ASSIGN 
                        output-list.str = output-list.str + STRING("  Order Instruction: ")
                        po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
                    DO ind = 1 TO 80:                                                                                                         
                        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
                        DO:                                                                                                                     
                            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
                                ASSIGN 
                                output-list.str = output-list.str + STRING(" ")
                                po-list.firma = po-list.firma + STRING(" ").                                                           
                            ELSE                                                                                                                  
                            DO:                                                                                                                   
                                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
                                ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
                            END.                                                                                                                  
                        END.
                    END.                                                                                                                                                                                                                   
                    ASSIGN 
                        output-list.str = output-list.str + STRING("")
                        po-list.firma = po-list.firma + STRING("").                                                                    
                    CREATE output-list.                                                                                                       
                    CREATE po-list. 
                END. 
            END.  
        END.
    END.
END PROCEDURE.

PROCEDURE order-instruction-detail:                                                                                        
     ASSIGN 
         output-list.str = output-list.str + STRING("  Order Instruction: ")
         detail-po-list.bezeich = STRING("  Order Instruction: ").                                                          
     DO ind = 1 TO 80:                                                                                                                    
        IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                                        
        DO:                                                                                                                                
            IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                                               
                ASSIGN 
                    output-list.str = output-list.str + STRING(" ")
                    detail-po-list.bezeich = detail-po-list.bezeich + STRING(" ").                                                                      
            ELSE                                                 
            DO:                                                                                                                              
                ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                               
                ASSIGN detail-po-list.bezeich = detail-po-list.bezeich + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)"). 
            END.                                                                                                                             
        END.                                                                                                                               
     END.                                                                                                                                                                                                                                         
     ASSIGN 
         output-list.str = output-list.str + STRING("")
         detail-po-list.bezeich = detail-po-list.bezeich + STRING("").                                                                               
     CREATE output-list.                                                                                                                  
     CREATE detail-po-list.                                                                                                               
END PROCEDURE.

PROCEDURE order-instruction-po:
     ASSIGN 
         output-list.str = output-list.str + STRING("  Order Instruction: ")
         po-list.firma = STRING("  Order Instruction: ").                                                                                                                            
     DO ind = 1 TO 80:                                                                                                         
       IF ind LE length(l-odrhdr.lief-fax[3]) THEN                                                                             
       DO:                                                                                                                     
         IF SUBSTR(l-odrhdr.lief-fax[3],ind,1) = chr(10) THEN                                                                                                                                                          
             ASSIGN 
                output-list.str = output-list.str + STRING(" ")
                po-list.firma = po-list.firma + STRING(" ").                                                           
         ELSE                                                                                                                  
         DO:                                                                                                                   
            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").                     
            ASSIGN po-list.firma = po-list.firma + STRING(SUBSTR(l-odrhdr.lief-fax[3],ind,1), "x(1)").
         END.                                                                                                                  
       END.                                                                                                                    
     END.                                                                                                                                                                                                                   
     ASSIGN 
        output-list.str = output-list.str + STRING("")
        po-list.firma = po-list.firma + STRING("").                                                                    
     CREATE output-list.                                                                                                       
     CREATE po-list.                                                                                                           
END PROCEDURE.


PROCEDURE detail-po-list1: /*Agung*/
    ASSIGN                                                                                                                              
        detail-po-list.bezeich      = STRING(l-odrhdr.bestelldatum) + STRING (" ") + STRING(l-supplier.firma, "x(16)" + STRING (" ") )            
        detail-po-list.lief-fax3    = l-odrhdr.docu-nr + STRING(" ").                                                                            
    CREATE detail-po-list.                                                                                                                       
END PROCEDURE. 

PROCEDURE detail-po-list2:
    ASSIGN /*Agung*/                                                     
        detail-po-list.artnr         = STRING(l-order2.artnr, "9999999 ")
        detail-po-list.bezeich       = l-art2.bezeich                    
        detail-po-list.lief-fax3     = l-order2.lief-fax[3]              
        detail-po-list.txtnr         = l-order2.txtnr                    
        detail-po-list.anzahl        = l-order2.anzahl                   
        detail-po-list.einzelpreis   = l-order2.einzelpreis              
        detail-po-list.warenwert     = l-order2.warenwert                
        detail-po-list.geliefert     = l-order2.geliefert                
        detail-po-list.angebot-lief1 = l-order2.angebot-lief[1]          
        .                                                                
    CREATE detail-po-list.                                               
END PROCEDURE.

PROCEDURE create-po-list:
    ASSIGN /*Agung*/                                          
        po-list.bestelldatum        = l-odrhdr.bestelldatum   
        po-list.firma               = l-supplier.firma        
        po-list.docu-nr             = l-odrhdr.docu-nr        
        po-list.odrhdr-lieferdatum  = l-odrhdr.lieferdatum    
        po-list.bestellart          = l-odrhdr.bestellart     
        po-list.besteller           = l-odrhdr.besteller      
        po-list.lief-fax2           = l-order1.lief-fax[2]    
        po-list.order1-lieferdatum  = l-order1.lieferdatum    
        po-list.lief-fax3           = l-order1.lief-fax[3]    
        po-list.lieferdatum-eff     = l-order1.lieferdatum-eff
        po-list.rechnungswert       = l-order1.rechnungswert
        po-list.pr-number           = l-order1.lief-fax[1]
        .                                                     
    CREATE po-list.                                           
END PROCEDURE.

/*******************************************************************/
 
