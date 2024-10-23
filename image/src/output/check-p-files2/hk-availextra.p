
DEFINE TEMP-TABLE t-paramtext   LIKE paramtext.
DEFINE TEMP-TABLE t-htparam     LIKE htparam.
DEFINE TEMP-TABLE t-artikel     LIKE artikel.
DEFINE TEMP-TABLE t-printer     LIKE PRINTER.
DEFINE TEMP-TABLE t-printcod    LIKE printcod.

DEFINE TEMP-TABLE tmp-extra 
    FIELD reihe     AS INTEGER INITIAL 0
    FIELD typ-pos   AS CHAR
    FIELD pos-from  AS CHAR
    FIELD cdate     AS DATE
    FIELD room      AS CHAR
    FIELD qty       AS INTEGER
    FIELD resnr     AS INTEGER.

DEFINE TEMP-TABLE disp-table 
    FIELD reihe     AS INTEGER
    FIELD str-typ   AS CHAR
    FIELD str1      AS CHAR     FORMAT "x(30)"
    FIELD str2      AS CHAR     FORMAT "x(30)"
    FIELD str3      AS CHAR     FORMAT "x(30)"
    FIELD str5      AS CHAR     FORMAT "x(30)"
    FIELD str6      AS CHAR     FORMAT "x(30)".

DEFINE TEMP-TABLE temp-art 
    FIELD art-nr    AS INTEGER
    FIELD art-nm    AS CHAR FORMAT "x(50)".

DEFINE INPUT parameter fdate           AS DATE.
DEFINE INPUT parameter tdate           AS DATE.
DEFINE INPUT parameter artnr           AS INTEGER.
DEFINE INPUT parameter sorttype        AS INTEGER.
DEFINE INPUT parameter language-code   AS INTEGER.
DEFINE OUTPUT parameter msgstr         AS CHARACTER.
DEFINE OUTPUT parameter TABLE FOR disp-table.

DEFINE VARIABLE cdate       AS DATE.
/*
DEFINE VARIABLE fdate           AS DATE     FORMAT "99/99/99"   LABEL "&From Date".
DEFINE VARIABLE tdate           AS DATE     FORMAT "99/99/99"   LABEL "&To Date".
DEFINE VARIABLE artnr           AS INTEGER.
DEFINE VARIABLE sorttype        AS INTEGER.
DEFINE VARIABLE msgstr          AS CHARACTER.
DEFINE VARIABLE language-code   AS INTEGER.

fdate         = 10/01/18.
tdate         = 10/26/18.
artnr         = 110.
sorttype      = 1. 
language-code = 1.
*/
FOR EACH disp-table:
    DELETE disp-table.
END.

IF fdate > tdate THEN
DO:
    msgstr = "From Date can not be greater than To Date".
    RETURN.
END.
ELSE
DO:
    IF artnr = 0 THEN
    DO:
        msgstr = "Article For not yet define.".
        RETURN.
    END.
    ELSE
    DO:
        RUN hk-availextrabl.p (language-code, artnr, fdate, tdate, OUTPUT TABLE tmp-extra).

        IF sorttype = 1 THEN
            RUN disp-detail.
        ELSE
            RUN disp-summary.
    END.
END.
/*
DISP msgstr.
FOR EACH disp-table:
    DISP disp-table WITH WIDTH 199.
END.
*/
PROCEDURE disp-detail :
DEF VAR tot-used AS INTEGER.
DEF VAR ndate AS DATE.
DEF VAR art-qty AS INTEGER INITIAL 0.
DEF VAR art-qty1 AS INTEGER INITIAL 0.
DEF VAR up-str3 AS INTEGER.

DEF VAR fart        AS CHAR.
DEF VAR flabel      AS CHAR     FORMAT "x(50)".
DEF VAR str1        AS CHAR     FORMAT "x(50)".

ndate = fdate.

    RUN read-artikelbl.p (artnr, 0, "", OUTPUT TABLE t-artikel).
    FIND FIRST t-artikel.
    IF AVAILABLE t-artikel THEN
    DO:
        art-qty = t-artikel.anzahl.
    END.
    art-qty1 = art-qty.
    DO WHILE ndate <= tdate :
        FIND FIRST tmp-extra WHERE tmp-extra.cdate = ndate NO-LOCK NO-ERROR.
        IF AVAILABLE tmp-extra THEN
        DO:
            FOR EACH tmp-extra WHERE tmp-extra.cdate = ndate /* AND tmp-extra.qty NE 0 */ 
                BY tmp-extra.reihe BY tmp-extra.room:
                tot-used = tot-used + tmp-extra.qty.
                FIND FIRST disp-table WHERE disp-table.str1 = string(ndate , "99/99/9999") 
                    AND disp-table.str2 = tmp-extra.room NO-LOCK NO-ERROR.
                IF AVAILABLE disp-table THEN
                DO:
                    up-str3 = int(disp-table.str3) + tmp-extra.qty.
                    
                    ASSIGN 
                        disp-table.str1 = string(ndate , "99/99/9999")    
                        disp-table.str2 = tmp-extra.room   
                        disp-table.str3 = string(up-str3) /*string(tmp-extra.qty)  */
                        disp-table.str5 = string(art-qty - up-str3)
                        disp-table.str6 = STRING(tmp-extra.resnr). 
                END.
                ELSE
                DO:
                    art-qty1 = art-qty1 - tmp-extra.qty.
                    CREATE disp-table.
                    ASSIGN 
                        disp-table.reihe = tmp-extra.reihe
                        disp-table.str1  = string(ndate , "99/99/9999")    
                        disp-table.str2  = tmp-extra.room   
                        disp-table.str3  = string(tmp-extra.qty)  
                        disp-table.str5  = string(art-qty1)
                        disp-table.str6  = STRING(tmp-extra.resnr). 
                END.
            END.
    
            CREATE disp-table.
            ASSIGN  
                    disp-table.str1 = ""    
                    disp-table.str2 = "Total"     
                    disp-table.str3 = string(tot-used)  
                    disp-table.str5 = string(art-qty - tot-used). 
    
            CREATE disp-table.
            ASSIGN  
                    disp-table.str1 = ""    
                    disp-table.str2 = ""     
                    disp-table.str3 = ""  
                    disp-table.str5 = ""
                    disp-table.str6 = "".
        END.
        ELSE
        DO:
            CREATE disp-table.
            ASSIGN  
                    disp-table.str1 = string(ndate , "99/99/9999")    
                    disp-table.str2 = ""     
                    disp-table.str3 = "" 
                    disp-table.str5 = string(art-qty). 
    
            CREATE disp-table.
            ASSIGN  
                    disp-table.str1 = ""    
                    disp-table.str2 = "Total"     
                    disp-table.str3 = string(tot-used)  
                    disp-table.str5 = string(art-qty). 
    
            CREATE disp-table.
            ASSIGN  
                    disp-table.str1 = ""    
                    disp-table.str2 = ""     
                    disp-table.str3 = ""  
                    disp-table.str5 = ""
                    disp-table.str6 = "".
        END.
        art-qty1 = art-qty.
        up-str3     = 0.
        tot-used    = 0.
        ndate       = ndate + 1.
    END.
END.

PROCEDURE disp-summary :
DEF VAR tot-used    AS INTEGER.
DEF VAR ndate       AS DATE.
DEF VAR art-qty     AS INTEGER INITIAL 0.

DEF VAR fart        AS CHAR.
DEF VAR flabel      AS CHAR     FORMAT "x(50)".
DEF VAR str1        AS CHAR     FORMAT "x(50)".

ndate = fdate.
    RUN read-artikelbl.p (artnr, 0, "", OUTPUT TABLE t-artikel).
    FIND FIRST t-artikel.
    IF AVAILABLE t-artikel THEN
    DO:
        art-qty = t-artikel.anzahl.
    END.

    DO WHILE ndate <= tdate :
        FOR EACH tmp-extra WHERE tmp-extra.cdate = ndate AND tmp-extra.qty NE 0 :
            tot-used = tot-used + tmp-extra.qty.
        END.

        CREATE disp-table.
        ASSIGN   
            disp-table.str1 = string(ndate , "99/99/99") 
            disp-table.str2 = ""     
            disp-table.str3 = string(tot-used) 
            disp-table.str5 = string(art-qty - tot-used)
            disp-table.str6 = "" . 
    
        tot-used    = 0.
        ndate       = ndate + 1.
    END.
END.



