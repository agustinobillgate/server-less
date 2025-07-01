DEF TEMP-TABLE t-nightaudit
    FIELD bezeichnung   LIKE nightaudit.bezeichnung
    FIELD hogarest      LIKE nightaudit.hogarest
    FIELD reihenfolge   LIKE nightaudit.reihenfolge
    FIELD programm      LIKE nightaudit.programm
    FIELD abschlussart  LIKE nightaudit.abschlussart.

DEFINE TEMP-TABLE na-list 
  FIELD reihenfolge AS INTEGER 
  FIELD flag AS INTEGER 
  FIELD bezeich LIKE nightaudit.bezeichnung. 

DEFINE TEMP-TABLE reslist 
   FIELD resnr AS INTEGER. 

DEFINE INPUT PARAMETER user-init         AS CHAR.
DEFINE INPUT PARAMETER def-natcode       AS CHAR.
DEFINE INPUT PARAMETER session-parameter AS CHAR.

DEFINE OUTPUT PARAMETER msg-str     AS CHAR.
DEFINE OUTPUT PARAMETER w-flag      AS LOGICAL. 
DEFINE OUTPUT PARAMETER names-ok    AS LOGICAL.
DEFINE OUTPUT PARAMETER na-can-run  AS LOGICAL.

DEFINE VARIABLE mn-stopped    AS LOGICAL NO-UNDO.
DEFINE VARIABLE msg-str2      AS CHAR NO-UNDO.
DEFINE VARIABLE msg-str3      AS CHAR NO-UNDO.
DEFINE VARIABLE msg-ans       AS LOGICAL NO-UNDO.
DEFINE VARIABLE htparam-recid AS INTEGER NO-UNDO.
DEFINE VARIABLE mnstart-flag  AS LOGICAL NO-UNDO.
DEFINE VARIABLE na-date1      AS DATE.
DEFINE VARIABLE na-time1      AS INTEGER.
DEFINE VARIABLE na-name1      AS CHAR.
DEFINE VARIABLE zugriff       AS LOGICAL. 
DEFINE VARIABLE i             AS INTEGER INITIAL 0. 
DEFINE VARIABLE its-ok        AS LOGICAL. 
DEFINE VARIABLE store-flag    AS LOGICAL.
DEFINE VARIABLE printer-nr    AS INTEGER INITIAL 0. 
DEFINE VARIABLE na-date       AS DATE.
DEFINE VARIABLE na-time       AS INTEGER. 
DEFINE VARIABLE na-name       AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE success-flag  AS LOGICAL.

RUN zugriff-testUI.p(user-init, 21, 2, OUTPUT zugriff). 
IF zugriff THEN 
DO: 
    RUN na-check1bl.p(0, def-natcode, OUTPUT msg-str, OUTPUT msg-str2, OUTPUT msg-str3,
                      OUTPUT w-flag, OUTPUT names-ok, OUTPUT its-ok, OUTPUT htparam-recid).
    
    IF msg-str NE "" THEN
    DO:
        na-can-run = NO.
        RETURN.
    END.
    
    IF w-flag = YES THEN 
    DO: 
        na-can-run = NO.
        RETURN. 
    END.
    
    IF NOT names-ok THEN
    DO:
        na-can-run = NO.
        RETURN. 
    END.
    na-can-run = YES.
    IF its-ok THEN 
    DO:
        RUN na-startbl.p(1, user-init, htparam-recid,OUTPUT mnstart-flag, OUTPUT store-flag,
                        OUTPUT printer-nr, OUTPUT TABLE t-nightaudit,OUTPUT na-date1, OUTPUT na-time1, OUTPUT na-name1).
    
        IF mnstart-flag THEN 
        DO:
            RUN mn-startUI.p("mnstartp", OUTPUT mn-stopped). 
            IF mn-stopped THEN
            DO:
                RUN na-start-update-flagbl.p(htparam-recid).
                RETURN.
            END.
            ELSE
            DO:
                RUN na-startbl.p (2, user-init, htparam-recid, OUTPUT mnstart-flag, OUTPUT store-flag,
                                 OUTPUT printer-nr, OUTPUT TABLE t-nightaudit, OUTPUT na-date1, OUTPUT na-time1, OUTPUT na-name1).
            END.
        END.
    
        RUN na-prog.
    
        RUN na-startbl.p (3, user-init, htparam-recid, OUTPUT mnstart-flag, OUTPUT store-flag,
                         OUTPUT printer-nr, OUTPUT TABLE t-nightaudit,OUTPUT na-date, OUTPUT na-time, OUTPUT na-name).
    
        msg-str = "Night Audit finished.". 
    END.
END.


PROCEDURE na-prog: 
    DEFINE VARIABLE night-type          AS INTEGER NO-UNDO.
    DEFINE VARIABLE mn-stopped          AS LOGICAL NO-UNDO.
    DEFINE VARIABLE a                   AS INT.
    
           
    FOR EACH na-list: 
        DELETE na-list. 
    END. 
    i = 0. 
    msg-str = "Night Audit is running!!". 
    
    FOR EACH t-nightaudit BY (1 - t-nightaudit.hogarest) BY t-nightaudit.reihenfolge:
        i = i + 1.
        CREATE na-list.
        na-list.reihenfolge = i.
        na-list.bezeich     = t-nightaudit.bezeichnung.
        na-list.flag        = t-nightaudit.hogarest.
       
        IF store-flag THEN 
        DO: 
            IF t-nightaudit.hogarest = 0 THEN night-type = 0. 
            ELSE night-type = 2.
            RUN delete-nitestorbl.p (1, night-type, t-nightaudit.reihenfolge,OUTPUT success-flag).
        END. 
        
        IF t-nightaudit.programm MATCHES "nt-tauziarpt.r" THEN
        DO:
            RUN nt-tauziarptui.p(session-parameter).
        END.
        ELSE IF t-nightaudit.programm MATCHES "nt-exportgcf.r" THEN
        DO:
            RUN nt-exportgcfui.p(session-parameter).
        END.
        ELSE IF t-nightaudit.programm MATCHES "nt-salesboard.r" THEN
        DO:
            RUN nt-salesboard.p(session-parameter).
        END.
        ELSE
        DO:
            IF t-nightaudit.programm MATCHES ("*bl.p*") THEN
                RUN VALUE(LC(t-nightaudit.programm)).
            ELSE 
            DO:
                IF INT(t-nightaudit.abschlussart) = 1 THEN
                RUN VALUE(LC(t-nightaudit.programm)).
                ELSE 
                DO:
                    a = R-INDEX (t-nightaudit.programm, ".p").
                    RUN VALUE(SUBSTR(LC(t-nightaudit.programm), 1, a - 1) + "bl.p").
                END.
            END.
        END.
        PAUSE 0.
        
        IF store-flag THEN RUN delete-nitehistbl.p (1, ?, t-nightaudit.reihenfolge,OUTPUT success-flag).
    END. 
END. 
