DEFINE TEMP-TABLE t-list
    FIELD progavail      AS CHARACTER
    FIELD hotelcode      AS CHARACTER
    FIELD pushrate-flag  AS LOGICAL
    FIELD pushavail-flag AS LOGICAL
    FIELD period         AS INTEGER.

DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0
    FIELD license       AS INTEGER.

DEFINE TEMP-TABLE temp-list
    FIELD rcode   AS CHAR
    FIELD rmtype  AS CHAR
    FIELD zikatnr AS INT.   

DEFINE INPUT PARAMETER TABLE FOR t-list.
DEFINE INPUT PARAMETER TABLE FOR t-push-list.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER cur-type     AS CHARACTER.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER bookengID    AS INTEGER.
DEFINE OUTPUT PARAMETER v-success   AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER error-msg   AS CHARACTER.

DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO INITIAL NO.
DEFINE VARIABLE done-avail  AS LOGICAL NO-UNDO INITIAL NO.
DEFINE VARIABLE done-rate   AS LOGICAL NO-UNDO INITIAL NO.
DEFINE VARIABLE counter-rate AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE p-253       AS LOGICAL NO-UNDO INIT NO. 
DEFINE VARIABLE cpushrate   AS LOGICAL NO-UNDO.
DEFINE VARIABLE cupdavail   AS LOGICAL NO-UNDO.
DEFINE VARIABLE inp-str	    AS CHARACTER NO-UNDO.
DEFINE VARIABLE max-adult   AS INTEGER NO-UNDO INITIAL 2.
DEFINE VARIABLE max-child   AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE htl-code    AS CHARACTER NO-UNDO.

RUN htplogic.p(253, OUTPUT p-253).
IF p-253 THEN 
DO:
    error-msg = "Night Audit is running, Please wait until it finish.".
    RETURN.
END.

RUN read-param(INPUT TABLE t-list, OUTPUT do-it, OUTPUT cupdavail, OUTPUT cpushrate, OUTPUT inp-str).

IF do-it THEN
DO:
    EMPTY TEMP-TABLE temp-list.
    FOR EACH t-push-list NO-LOCK:
        CREATE temp-list.
        ASSIGN
            temp-list.rcode = t-push-list.rcodevhp          /* Rulita 170125 | Fixing serverless issue git 308 t-push-list.rcodeVHP lowercase */
            temp-list.rmtype = t-push-list.rmtypevhp        /* Rulita 170125 | Fixing serverless issue git 308 t-push-list.rmtypevhp lowercase */
        .
    END.
END.
ELSE 
DO:
    error-msg = "Configuration not complete.".
    RETURN.
END.

IF cupdavail THEN
DO:
    RUN if-custom-pushall-availbl.p (cur-type, from-date, to-date, bookengID, inp-str, 
                                    cpushrate, INPUT TABLE temp-list, OUTPUT done-avail).
END.

IF cpushrate THEN
DO:
    counter-rate = 1.
    RUN if-custom-pushall-ratebl.p (cur-type, counter-rate, inp-str, from-date, to-date, max-adult, 
                                    max-child, bookengID, INPUT TABLE temp-list, OUTPUT done-rate).
END.

RUN update-repeatflag-1bl.p (bookengID).
v-success = YES.

/************************************************************************************************/
PROCEDURE read-param:
DEFINE INPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER do-it AS LOGICAL INIT YES.
DEFINE OUTPUT PARAMETER cupdavail AS LOGICAL INIT NO NO-UNDO.
DEFINE OUTPUT PARAMETER cpushrate AS LOGICAL INIT NO NO-UNDO.
DEFINE OUTPUT PARAMETER inp-str AS CHAR.

DEF VAR pushpax AS LOGICAL INIT NO NO-UNDO.
DEF VAR bedsetup AS LOGICAL INIT NO NO-UNDO.
DEF VAR allotment AS LOGICAL INIT NO NO-UNDO.
DEF VAR incl-tentative AS LOGICAL INIT NO NO-UNDO.

    FIND FIRST t-list NO-ERROR.
	IF AVAILABLE t-list THEN
	DO:
		ASSIGN 
			cpushrate = t-list.pushrate-flag
			htl-code = t-list.hotelcode
			cupdavail = t-list.pushavail-flag.
		
		IF NUM-ENTRIES(t-list.progavail,"=") GE 3  THEN
		DO:
			pushpax = LOGICAL(ENTRY(3,t-list.progavail,"=")).
		END.            
		ELSE
		DO:
			pushpax = NO.
		END.

		IF NUM-ENTRIES(t-list.progavail, "=") GE 10 THEN
		DO:
			allotment = LOGICAL(ENTRY(11,t-list.progavail,"=")).
			bedsetup    = LOGICAL(ENTRY(13,t-list.progavail,"=")).
		END.
		ELSE
		DO:
			allotment = NO.
			bedsetup = NO.
		END.
		IF NUM-ENTRIES(t-list.progavail,"=") GE 24 THEN
                incl-tentative    = LOGICAL(ENTRY(24,t-list.progavail,"=")).
		ELSE incl-tentative = NO.
	END.
	ELSE do-it = NO.

    inp-str = STRING(incl-tentative) + "=" + STRING(pushpax) + "=" + STRING(allotment) + "=" + STRING(bedSetup).
END PROCEDURE.
