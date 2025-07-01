DEFINE TEMP-TABLE summary-bill
    FIELD department    AS INT FORMAT ">>>"
    FIELD tableno       AS INT FORMAT ">>>"
    FIELD rechnr        AS INT FORMAT ">>>>>"
    FIELD pax           AS INT FORMAT ">>>"
    FIELD total-food    AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-bev     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-other   AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-service AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-tax     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-disc    AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-tips    AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD total-amount  AS DECIMAL FORMAT "->,>>>,>>9.99"
    .
/**/
DEFINE INPUT PARAMETER rechnr AS INT.
DEFINE INPUT PARAMETER dept AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR summary-bill.
/**/
/*
DEFINE VARIABLE rechnr   AS INT INIT 503.
DEFINE VARIABLE dept     AS INT INIT 1.
*/
/*=============*/


DEFINE VARIABLE vat     AS DECIMAL. 
DEFINE VARIABLE vat2    AS DECIMAL. 
DEFINE VARIABLE service AS DECIMAL.
DEFINE VARIABLE fact    AS DECIMAL.
DEFINE VARIABLE netto   AS DECIMAL.
DEFINE VARIABLE t-service   AS INT.

DEFINE VARIABLE discfood-artnr AS INT.
DEFINE VARIABLE discoth-artnr AS INT.
DEFINE VARIABLE discbev-artnr AS INT.

FIND FIRST htparam WHERE paramnr EQ 556 NO-LOCK NO-ERROR.
discoth-artnr = htparam.finteger.
FIND FIRST htparam WHERE paramnr EQ 557 NO-LOCK NO-ERROR.
discfood-artnr = htparam.finteger.
FIND FIRST htparam WHERE paramnr EQ 559 NO-LOCK NO-ERROR.
discbev-artnr = htparam.finteger.

FIND FIRST h-bill WHERE h-bill.departement EQ dept AND h-bill.rechnr EQ rechnr NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    CREATE summary-bill.
    ASSIGN 
        summary-bill.department = h-bill.departement
        summary-bill.tableno    = h-bill.tischnr
        summary-bill.rechnr     = h-bill.rechnr
        summary-bill.pax        = h-bill.belegung.

    FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ rechnr
        AND h-bill-line.departement EQ dept NO-LOCK:
        FIND FIRST h-artikel WHERE h-artikel.departement EQ dept 
            AND h-artikel.artnr EQ h-bill-line.artnr 
            AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN
        DO:
            IF h-artikel.artnr EQ discfood-artnr THEN
            DO:
                summary-bill.total-disc = summary-bill.total-disc + (h-bill-line.epreis * h-bill-line.anzahl).
            END.
            ELSE IF h-artikel.artnr EQ discbev-artnr THEN
            DO:
                summary-bill.total-disc = summary-bill.total-disc + (h-bill-line.epreis * h-bill-line.anzahl).
            END.
            ELSE IF h-artikel.artnr EQ discoth-artnr THEN
            DO:
                summary-bill.total-disc = summary-bill.total-disc + (h-bill-line.epreis * h-bill-line.anzahl).
            END.
            ELSE
            DO:
                IF h-artikel.artnrfront EQ 10 THEN 
                    summary-bill.total-food  = summary-bill.total-food + (h-artikel.epreis1 * h-bill-line.anzahl).
                ELSE IF h-artikel.artnrfront EQ 11 THEN 
                    summary-bill.total-bev   = summary-bill.total-bev + (h-artikel.epreis1 * h-bill-line.anzahl).
                ELSE 
                    summary-bill.total-other = summary-bill.total-other + (h-artikel.epreis1 * h-bill-line.anzahl).
            END.
    
            FIND FIRST artikel WHERE artikel.departement EQ h-artikel.departement AND artikel.artnr EQ h-artikel.artnrfront NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
                RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement, h-bill-line.bill-datum, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

                netto = h-bill-line.betrag / (1 + vat + vat2 + service). 
                summary-bill.total-service = summary-bill.total-service + (netto * service).
                summary-bill.total-tax = summary-bill.total-tax + (netto * vat).

                IF h-artikel.artnr EQ discfood-artnr THEN .
                ELSE IF h-artikel.artnr EQ discbev-artnr THEN .
                ELSE IF h-artikel.artnr EQ discoth-artnr THEN .
                /*
                IF h-artikel.artnrfront EQ 10 THEN 
                    summary-bill.total-food = summary-bill.total-food + ROUND((netto),0).
                ELSE IF h-artikel.artnrfront EQ 11 THEN 
                    summary-bill.total-bev = summary-bill.total-bev + ROUND((netto),0).
                ELSE 
                    summary-bill.total-other = summary-bill.total-other + ROUND((netto),2).
                */
                /*
                IF h-artikel.artnrfront EQ 10 THEN 
                    summary-bill.total-food  = summary-bill.total-food + ROUND((h-bill-line.epreis),0).
                ELSE IF h-artikel.artnrfront EQ 11 THEN 
                    summary-bill.total-bev   = summary-bill.total-bev + ROUND((h-bill-line.epreis),0).
                ELSE 
                    summary-bill.total-other = summary-bill.total-other + ROUND((h-bill-line.epreis),0).
                /**/*/
            END.
        END.
    END.
END.
FOR EACH summary-bill.
    summary-bill.total-service = ROUND(summary-bill.total-service,0).
    summary-bill.total-other   = ROUND(summary-bill.total-other,0).
 
    summary-bill.total-amount = ROUND(summary-bill.total-food + 
                            summary-bill.total-bev  +
                            summary-bill.total-other + 
                            summary-bill.total-service +
                            summary-bill.total-tax +
                            summary-bill.total-disc,0).

END.
/*
CURRENT-WINDOW:WIDTH = 200.
FOR EACH summary-bill.
    DISP summary-bill WITH WIDTH 180.
END.
*/


