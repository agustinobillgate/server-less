
DEF TEMP-TABLE akt-line1 LIKE akt-line.

DEF INPUT PARAMETER TABLE FOR akt-line1.
DEF INPUT PARAMETER prior        AS CHAR.
DEF INPUT PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER base64file   AS LONGCHAR NO-UNDO.
DEF INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER result-message AS CHAR.

DEF VAR curr-counter AS INT.    

FIND FIRST akt-line1.
FIND FIRST counters WHERE counters.counter-no = 27 EXCLUSIVE-LOCK NO-ERROR. 
IF NOT AVAILABLE counters THEN 
DO: 
    create counters. 
    counters.counter-no = 27. 
    counters.counter-bez = "Counter for sales activity-line". 
END. 
counters.counter = counters.counter + 1. 
akt-line1.linenr = counters.counter. 
curr-counter = counters.counter. 
FIND CURRENT counter NO-LOCK. 
RUN init-prior.
CREATE akt-line.
BUFFER-COPY akt-line1 TO akt-line.

IF (base64file NE "" OR base64file NE ?) AND user-init NE "" THEN
    RUN upload-imagesetupbl.p(case-type, base64file, user-init, curr-counter, OUTPUT result-message).

PROCEDURE init-prior:
    IF prior = "Low" THEN
        akt-line1.prioritaet = 1.
    ELSE IF prior = "Medium" THEN
        akt-line1.prioritaet = 2.
    ELSE IF prior = "High" THEN
        akt-line1.prioritaet = 3.
END.

