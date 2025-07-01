
DEFINE TEMP-TABLE h-list LIKE history
    FIELD chgdate      AS CHARACTER   FORMAT "x(8)"       COLUMN-LABEL "Chg Date"
    FIELD tzinr        LIKE history.zinr                  COLUMN-LABEL "MoveTo"
    FIELD reason       AS CHARACTER   FORMAT "x(82)"  /*william*/
    FIELD usr-id    AS CHARACTER   FORMAT "x(5)"       COLUMN-LABEL "ID"
    FIELD res-name     AS CHARACTER   FORMAT "x(32)"      COLUMN-LABEL "Reservation Name"
    FIELD abreisezeit1 AS INTEGER     FORMAT ">,>>>,>>9"  COLUMN-LABEL "Time".

DEFINE INPUT PARAMETER  from-date        AS DATE.
DEFINE INPUT PARAMETER  to-date          AS DATE.
DEFINE OUTPUT PARAMETER TABLE            FOR h-list.

DEFINE VARIABLE s1                       AS CHAR NO-UNDO.
DEFINE VARIABLE s2                       AS CHAR NO-UNDO.
DEFINE VARIABLE s3                       AS CHAR NO-UNDO.
DEFINE VARIABLE user-init                AS CHAR NO-UNDO.

FOR EACH h-list:
  DELETE h-list.
END.

FOR EACH history WHERE history.ankunft LE to-date 
    AND history.abreise GE from-date AND history.zi-wechsel 
    AND SUBSTR(history.bemerk,1,8) GE STRING(from-date) 
    AND SUBSTR(history.bemerk,1,8) LE STRING(to-date) NO-LOCK 
    BY SUBSTR(history.bemerk,1,8) BY history.zinr:
    FIND FIRST res-line WHERE res-line.resnr = history.resnr NO-LOCK NO-ERROR. 
    FIND FIRST bediener WHERE bediener.userinit = user-init  NO-LOCK NO-ERROR.
    s1 = ENTRY(1,history.bemerk,CHR(10)).
    IF INDEX(history.bemerk,CHR(10)) GT 0 THEN
    DO:
        /*s2 = ENTRY(2, history.bemerk, CHR(10))*/
        s2 = ENTRY(1, ENTRY(2, history.bemerk, CHR(10)), CHR(2)). /*FD September 17, 2020*/
    END.
        
    ELSE s2 = "".
    
    CREATE h-list.
    BUFFER-COPY history TO h-list.
    ASSIGN
      h-list.reason       = s2
      h-list.tzinr        = TRIM(SUBSTR(s1,20)) /*wen 180517*/
      h-list.chgdate      = SUBSTR(history.bemerk,1,8)
      h-list.resnr        = res-line.resnr 
      h-list.reslinnr     = res-line.reslinnr
      h-list.abreisezeit1 = res-line.ankzeit
      h-list.res-name     = res-line.resname
      usr-id              = "".
      IF NUM-ENTRIES (history.bemerk, CHR(2)) GT 1 THEN
          usr-id = ENTRY(2, history.bemerk, CHR(2)).
END.
