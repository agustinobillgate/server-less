DEFINE SHARED VARIABLE vhpgbConnect AS LOGICAL NO-UNDO. 

DEF VARIABLE pf-filename AS CHAR NO-UNDO.

IF SUBSTRING(PROVERSION, 1, 2) = "10" THEN 
    ASSIGN pf-filename = "c:\vhpgb\config\vhpgb.pfc".
ELSE IF SUBSTRING(PROVERSION, 1, 2) = "11" THEN 
    ASSIGN pf-filename = "c:\vhpgb11\config\vhpgb.pfc".

IF SEARCH("c:\vhpgb\db\vhpgb.db") = ? THEN 
DO: 
    vhpgbConnect = ?.
    RETURN.
END.

IF NOT CONNECTED("vhpgb") THEN 
DO:
    IF vhpgbConnect = ? THEN
        RUN disp-message.p("Connecting to VHPGB DB, please wait...", 2).
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait"). 
    PROCESS EVENTS. 
    CONNECT -1 c:\vhpgb\db\vhpgb NO-ERROR.
    IF NOT CONNECTED("vhpgb") THEN
      CONNECT -pf VALUE(pf-filename) NO-ERROR. 
    IF NOT CONNECTED("vhpgb") THEN
    DO:
      ASSIGN pf-filename = "c:\vhpgb11\config\vhpgb.pfc".
      CONNECT -pf VALUE(pf-filename) NO-ERROR. 
    END. 
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow"). 
END.
