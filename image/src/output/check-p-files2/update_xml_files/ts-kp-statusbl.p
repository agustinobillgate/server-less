DEFINE TEMP-TABLE tlist
    FIELD artqty        AS INTEGER
    FIELD artname       AS CHAR
    FIELD send-print    AS DATE
    FIELD send-tprint   AS LOGICAL
    FIELD printed       AS LOGICAL
.

DEFINE TEMP-TABLE print-list
    FIELD artno     AS INTEGER
    FIELD dept-no   AS INTEGER
    FIELD art-desc  AS CHARACTER
    FIELD art-desc2 AS CHARACTER
    FIELD bill-no   AS INTEGER
    .

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER billno       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER depart       AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tlist.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "kp-status".

DEFINE VARIABLE lvDelimiter1    AS CHAR. 
DEFINE VARIABLE lvDelimiter2    AS CHAR. 
DEFINE VARIABLE loopi           AS INTEGER.
DEFINE VARIABLE loopn           AS INTEGER.
DEFINE VARIABLE curr-str        AS CHAR.
DEFINE VARIABLE str1            AS CHAR.
DEFINE VARIABLE dept-name       AS CHAR.

lvDelimiter1 = CHR(10).
lvDelimiter2 = ":::".

FIND FIRST hoteldpt WHERE hoteldpt.num EQ depart NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN dept-name = hoteldpt.depart.

/*FDL June 06, 2023 => Ticket DF3F34*/
FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ billno
    AND h-bill-line.departement EQ depart NO-LOCK,
    FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr 
    AND h-artikel.departement EQ depart AND h-artikel.artart EQ 0 NO-LOCK:

    FIND FIRST print-list WHERE print-list.bill-no EQ h-bill-line.rechnr
        AND print-list.dept-no EQ h-bill-line.departement
        AND print-list.artno EQ h-bill-line.artnr
        AND print-list.art-desc EQ h-artikel.bezeich
        AND print-list.art-desc2 EQ h-bill-line.bezeich NO-LOCK NO-ERROR.
    IF NOT AVAILABLE print-list THEN
    DO:
        CREATE print-list.
        ASSIGN
            print-list.artno    = h-bill-line.artnr   
            print-list.dept-no  = h-bill-line.departement
            print-list.art-desc = h-artikel.bezeich
            print-list.bill-no  = h-bill-line.rechnr
        .
        IF h-artikel.bezaendern THEN print-list.art-desc2 = h-bill-line.bezeich.
    END.    
END.

FIND FIRST h-bill WHERE h-bill.rechnr = billno
    AND h-bill.departement = depart
    AND h-bill.flag = 0 NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN DO:
    FOR EACH queasy WHERE queasy.KEY = 3
        AND queasy.char3 MATCHES("*" + STRING(h-bill.rechnr) + "*") 
        AND queasy.char3 MATCHES("*" + dept-name + "*") NO-LOCK:
        DO loopi = 1 TO NUM-ENTRIES(queasy.char3, lvDelimiter1):
            curr-str  = ENTRY(loopi, queasy.char3, lvDelimiter1).
            IF curr-str NE "" THEN DO:
                /*FIND FIRST h-artikel WHERE h-artikel.bezeich MATCHES ("*" + TRIM(SUBSTR(curr-str,6)) + "*")
                    AND h-artikel.departement = h-bill.departement NO-LOCK NO-ERROR.
                IF AVAILABLE h-artikel THEN DO:*/
                FIND FIRST print-list WHERE (print-list.art-desc MATCHES ("*" + TRIM(SUBSTR(curr-str,6)) + "*")
                    OR print-list.art-desc2 MATCHES ("*" + TRIM(SUBSTR(curr-str,6)) + "*"))
                    AND print-list.dept-no EQ h-bill.departement NO-LOCK NO-ERROR.
                IF AVAILABLE print-list THEN 
                DO:
                    IF TRIM(SUBSTR(curr-str,6)) NE "" THEN DO:
                        CREATE tlist.
                        ASSIGN 
                            tlist.artqty        = INTEGER(SUBSTR(curr-str,1, 5))
                            tlist.artname       = TRIM(SUBSTR(curr-str,6))
                            tlist.send-print    = queasy.date1
                            tlist.send-tprint   = NOT queasy.logi1
                            tlist.printed       = NOT queasy.logi2
                        .
                    END.
                END.
            END.
        END.
    END.
END.
ELSE IF NOT AVAILABLE h-bill THEN DO:
    ASSIGN msg-str = translateExtended ("No record Available",lvCAREA,"").
END.

