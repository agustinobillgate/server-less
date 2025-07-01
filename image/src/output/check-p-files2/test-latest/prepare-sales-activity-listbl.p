DEFINE TEMP-TABLE output-list 
  FIELD outnr AS INTEGER FORMAT ">9" 
  FIELD act-str AS CHAR FORMAT "x(78)".

DEFINE TEMP-TABLE print-list
  FIELD guest AS CHAR
  FIELD refno AS CHAR
  FIELD resstatus AS CHAR
  FIELD rechnr AS CHAR
  FIELD datum AS CHAR
  FIELD zeit AS CHAR. 

DEFINE TEMP-TABLE t-b-storno LIKE b-storno.

DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE OUTPUT PARAMETER counter-reason AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR print-list.

FIND FIRST b-storno WHERE b-storno.bankettnr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE b-storno THEN
DO :
    CREATE t-b-storno.
    BUFFER-COPY b-storno TO t-b-storno.
END.

FIND FIRST t-b-storno NO-LOCK NO-ERROR. 
IF AVAILABLE t-b-storno THEN RUN create-outlist. 

PROCEDURE create-outlist: 
DEFINE VARIABLE i AS INTEGER. 
  counter-reason = 0. 
  FOR EACH output-list : 
    DELETE output-list. 
  END. 
  DO i = 1 TO 18: 
    IF b-storno.grund[i] NE "" THEN 
    DO:
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr NO-LOCK NO-ERROR. 
      FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR. 
      FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
      FIND FIRST print-list NO-LOCK NO-ERROR.
      IF AVAILABLE bk-reser AND AVAILABLE bk-veran AND AVAILABLE guest THEN 
      DO:
         CREATE output-list. 
         ASSIGN 
         output-list.outnr = i 
         output-list.act-str = b-storno.grund[i]
         counter-reason = i.
         RUN create-print.   
       END.
    END. 
  END. 
END.

PROCEDURE create-print:
FIND FIRST print-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE print-list THEN
DO:
    CREATE print-list.
    ASSIGN
    print-list.guest = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma
    print-list.refno = STRING(bk-reser.veran-nr)
    print-list.resstatus = STRING(bk-reser.resstatus)
    print-list.rechnr = STRING(bk-veran.rechnr)
    print-list.datum = STRING(bk-reser.datum) + " - " + STRING(bk-reser.bis-datum)
    print-list.zeit = STRING(bk-reser.von-zeit,"99:99") + " - " + STRING(bk-reser.bis-zeit,"99:99"). 
END.
END.
