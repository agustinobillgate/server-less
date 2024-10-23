DEFINE TEMP-TABLE rlist
    FIELD gastnr        AS INTEGER
    FIELD gname         AS CHAR
    FIELD arrive        AS DATE
    FIELD depart        AS DATE
    FIELD ci-mobile     AS CHAR
    FIELD ci-fda        AS CHAR
    FIELD scan-mobile   AS CHAR
    FIELD scan-fda      AS CHAR
    FIELD sign-mobile   AS CHAR
    FIELD sign-fda      AS CHAR
    FIELD rc-mobile     AS CHAR
    FIELD rc-fda        AS CHAR.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER from-date AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-date   AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR rlist.

DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
DEFINE VARIABLE str1  AS CHAR    NO-UNDO.

DEFINE VARIABLE tot-cimb    AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-cifda   AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-scanmb  AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-scanfda AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-signmb  AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-signfda AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-rcmb    AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-rcfda   AS INTEGER NO-UNDO.

ASSIGN
    tot-cimb     = 0
    tot-cifda    = 0
    tot-scanmb   = 0
    tot-scanfda  = 0
    tot-signmb   = 0
    tot-signfda  = 0
    tot-rcmb     = 0
    tot-rcfda    = 0.

CASE case-type:
    WHEN 1 THEN DO:
        FOR EACH res-line WHERE res-line.ankunft GE from-date
            AND res-line.ankunft LE to-date
            AND res-line.resstatus NE 99
            AND res-line.resstatus NE 9
            AND res-line.resstatus NE 8 NO-LOCK:

            CREATE rlist.
            ASSIGN rlist.gastnr = res-line.gastnr
                   rlist.gname  = res-line.NAME
                   rlist.arrive = res-line.ankunft
                   rlist.depart = res-line.abreise.

            DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                MESSAGE res-line.zimmer-wunsch VIEW-AS ALERT-BOX INFO.
                str1 = ENTRY(loopi,res-line.zimmer-wunsch, ";").
                IF str1 MATCHES "*mobile-ci*" THEN
                    ASSIGN rlist.ci-mobile = "*"
                           tot-cimb        = tot-cimb + 1.
                IF str1 MATCHES "*mobile-scan*" THEN
                    ASSIGN rlist.scan-mobile = "*"
                           tot-scanmb         = tot-scanmb + 1.
                IF str1 MATCHES "*mobile-sign-bill*" THEN
                    ASSIGN rlist.sign-mobile = "*"
                           tot-signmb        = tot-signmb + 1.
                IF str1 MATCHES "*mobile-sign-rc*" THEN
                    ASSIGN rlist.rc-mobile = "*"
                           tot-rcmb        = tot-rcmb + 1.
            END.

            IF rlist.ci-mobile = " " THEN 
                ASSIGN rlist.ci-fda = "*"
                       tot-cifda    = tot-cifda + 1.
            IF rlist.scan-mobile = " " THEN 
                ASSIGN rlist.scan-fda = "*"
                       tot-scanfda    = tot-scanfda + 1.
            IF rlist.sign-mobile = " " THEN 
                ASSIGN rlist.sign-fda = "*"
                       tot-signfda    = tot-signfda + 1.
            IF rlist.rc-mobile = " " THEN 
                ASSIGN rlist.rc-fda = "*"
                       tot-rcfda    = tot-rcfda + 1.
        END.
    END.
    WHEN 2 THEN DO:
        FOR EACH res-line WHERE res-line.abreise GE from-date
            AND res-line.abreise LE to-date 
            AND res-line.resstatus NE 99
            AND res-line.resstatus NE 9 NO-LOCK:

            CREATE rlist.
            ASSIGN rlist.gastnr = res-line.gastnr
                   rlist.gname  = res-line.NAME
                   rlist.arrive = res-line.ankunft
                   rlist.depart = res-line.abreise.

            DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str1 = ENTRY(loopi,res-line.zimmer-wunsch, ";").
                IF str1 MATCHES "*mobile-ci*" THEN
                    ASSIGN rlist.ci-mobile = "*"
                           tot-cimb        = tot-cimb + 1.
                IF str1 MATCHES "*mobile-scan*" THEN
                    ASSIGN rlist.scan-mobile = "*"
                           tot-scanmb         = tot-scanmb + 1.
                IF str1 MATCHES "*mobile-sign-bill*" THEN
                    ASSIGN rlist.sign-mobile = "*"
                           tot-signmb        = tot-signmb + 1.
                IF str1 MATCHES "*mobile-sign-rc*" THEN
                    ASSIGN rlist.rc-mobile = "*"
                           tot-rcmb        = tot-rcmb + 1.
            END.

            IF rlist.ci-mobile = " " THEN 
                ASSIGN rlist.ci-fda = "*"
                       tot-cifda    = tot-cifda + 1.
            IF rlist.scan-mobile = " " THEN 
                ASSIGN rlist.scan-fda = "*"
                       tot-scanfda    = tot-scanfda + 1.
            IF rlist.sign-mobile = " " THEN 
                ASSIGN rlist.sign-fda = "*"
                       tot-signfda    = tot-signfda + 1.
            IF rlist.rc-mobile = " " THEN 
                ASSIGN rlist.rc-fda = "*"
                       tot-rcfda    = tot-rcfda + 1.
        END.
    END.
    WHEN 3 THEN DO:
        FOR EACH res-line WHERE res-line.abreise GE from-date
            AND res-line.abreise LE to-date 
            AND res-line.resstatus = 10 NO-LOCK:

            CREATE rlist.
            ASSIGN rlist.gastnr = res-line.gastnr
                   rlist.gname  = res-line.NAME
                   rlist.arrive = res-line.ankunft
                   rlist.depart = res-line.abreise.

            DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str1 = ENTRY(loopi,res-line.zimmer-wunsch, ";").
                IF str1 MATCHES "*mobile-ci*" THEN
                    ASSIGN rlist.ci-mobile = "*"
                           tot-cimb        = tot-cimb + 1.
                IF str1 MATCHES "*mobile-scan*" THEN
                    ASSIGN rlist.scan-mobile = "*"
                           tot-scanmb         = tot-scanmb + 1.
                IF str1 MATCHES "*mobile-sign-bill*" THEN
                    ASSIGN rlist.sign-mobile = "*"
                           tot-signmb        = tot-signmb + 1.
                IF str1 MATCHES "*mobile-sign-rc*" THEN
                    ASSIGN rlist.rc-mobile = "*"
                           tot-rcmb        = tot-rcmb + 1.
            END.

            IF rlist.ci-mobile = " " THEN 
                ASSIGN rlist.ci-fda = "*"
                       tot-cifda    = tot-cifda + 1.
            IF rlist.scan-mobile = " " THEN 
                ASSIGN rlist.scan-fda = "*"
                       tot-scanfda    = tot-scanfda + 1.
            IF rlist.sign-mobile = " " THEN 
                ASSIGN rlist.sign-fda = "*"
                       tot-signfda    = tot-signfda + 1.
            IF rlist.rc-mobile = " " THEN 
                ASSIGN rlist.rc-fda = "*"
                       tot-rcfda    = tot-rcfda + 1.
        END.
    END.
END CASE.

CREATE rlist.
ASSIGN rlist.gastnr         = 99999999
       rlist.gname          = "T O T A L"
       rlist.ci-mobile      = STRING(tot-cimb, ">>>>9")
       rlist.scan-mobile    = STRING(tot-scanmb, ">>>>9")
       rlist.sign-mobile    = STRING(tot-signmb, ">>>>9")
       rlist.rc-mobile      = STRING(tot-rcmb, ">>>>9")
       rlist.ci-fda         = STRING(tot-cifda, ">>>>9")
       rlist.scan-fda       = STRING(tot-scanfda, ">>>>9")
       rlist.sign-fda       = STRING(tot-signfda, ">>>>9")
       rlist.rc-fda         = STRING(tot-rcfda, ">>>>9").
       
       
       


