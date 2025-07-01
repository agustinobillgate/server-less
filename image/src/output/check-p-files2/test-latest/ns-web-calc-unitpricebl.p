DEFINE TEMP-TABLE t-bill-line       LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE vatBuff       LIKE artikel.
DEFINE TEMP-TABLE bline         LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE foart         LIKE artikel.

DEFINE INPUT PARAMETER lvAnzVat         AS INTEGER INITIAL 0 NO-UNDO.
DEFINE INPUT PARAMETER vat-artlist      AS INTEGER EXTENT 4.
DEFINE INPUT PARAMETER billart          AS INTEGER.
DEFINE INPUT PARAMETER balance          AS DECIMAL.
DEFINE INPUT PARAMETER curr-department  AS INTEGER.
DEFINE INPUT PARAMETER rechnr           AS INTEGER.
DEFINE OUTPUT PARAMETER price AS DECIMAL.

DEFINE VARIABLE amt      AS DECIMAL INITIAL 0           NO-UNDO.
DEFINE VARIABLE vat      AS DECIMAL INITIAL 0           NO-UNDO.
DEFINE VARIABLE serv     AS DECIMAL INITIAL 0           NO-UNDO.
DEFINE VARIABLE serv-vat AS LOGICAL                     NO-UNDO.
DEFINE VARIABLE ind      AS INTEGER INITIAL 0           NO-UNDO.
DEFINE VARIABLE found    AS LOGICAL INITIAL NO          NO-UNDO.
DEFINE VARIABLE fdecimal AS DECIMAL INITIAL 0           NO-UNDO.

DO ind = 1 TO lvAnzVat:
    IF billArt = vat-artList[ind] THEN found = YES.
END.
IF NOT found OR curr-department GT 0 THEN 
DO:    
    price = - balance.
    RETURN.
END.

RUN read-artikelbl.p (billart, 0, ?, OUTPUT TABLE vatBuff).
FIND FIRST vatBuff NO-LOCK.
RUN htplogic.p (479, OUTPUT serv-vat).

RUN read-bill-line1bl.p(3, 0, rechnr, ?, ?, ?, ?, ?,OUTPUT TABLE bline).
FOR EACH bline NO-LOCK:
    RUN read-artikelbl.p (bline.artnr, bline.departement, ?,OUTPUT TABLE foart).
    FIND FIRST foart NO-LOCK NO-ERROR. 
    IF AVAILABLE foart AND foart.mwst-code = vatBuff.mwst-code THEN 
    DO: 
        IF bline.orts-tax NE 0 THEN amt = amt - bline.orts-tax.
        ELSE
        DO:
            RUN htpdec.p (foart.service-code, OUTPUT fdecimal).
            IF fdecimal NE ? THEN serv = fdecimal / 100. 
            RUN htpdec.p (foart.mwst-code, OUTPUT fdecimal).
            IF fdecimal NE ? THEN 
            DO:    
                vat = fdecimal / 100. 
                IF serv-vat THEN vat = vat + vat * serv.
            END.
            ELSE vat = 0.        
            IF vat NE 0 THEN amt = amt - bline.betrag * (1 - 1 / (1 + vat)).
        END.
    END.
END.
price = amt.
