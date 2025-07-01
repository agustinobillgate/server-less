DEFINE TEMP-TABLE flist
    FIELD dept      AS INTEGER
    FIELD rechnr    AS INTEGER
    FIELD saldo     AS CHARACTER
    FIELD discount  AS CHARACTER
    FIELD created   AS CHARACTER
    FIELD checkin   AS CHARACTER
    FIELD checkout  AS CHARACTER
    FIELD pax       AS INTEGER
    FIELD usr       AS CHARACTER
    FIELD id        AS INTEGER
    FIELD reslinnr  AS CHAR
    FIELD service   AS INTEGER
    FIELD resnr     AS INTEGER
    FIELD breslin   AS INTEGER
    FIELD gastnr    AS INTEGER
    FIELD gastpay   AS INTEGER.

DEFINE TEMP-TABLE fline-list
    FIELD rechnr    AS INTEGER
    FIELD dept      AS INT
    FIELD bezeich   AS CHARACTER
    FIELD price     AS CHARACTER
    FIELD rtcode    AS CHARACTER
    FIELD rmtype    AS CHARACTER
    FIELD resnr     AS INTEGER
	FIELD reslinnr  AS CHAR
    FIELD breslin   AS INTEGER
    FIELD gastnr    AS INTEGER
    FIELD gastpay   AS INTEGER.

DEFINE INPUT PARAMETER ci-date          AS DATE.
DEFINE OUTPUT PARAMETER allocated-point    AS INTEGER  INITIAL ?.
DEFINE OUTPUT PARAMETER avail-data      AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER record_count    AS INTEGER  INITIAL 0.
DEFINE OUTPUT PARAMETER TABLE FOR flist.
DEFINE OUTPUT PARAMETER TABLE FOR fline-list.

DEFINE BUFFER buffnite FOR nitehist.

DEFINE VARIABLE reihenfolge     AS INTEGER NO-UNDO. 
DEFINE VARIABLE progname        AS CHAR    NO-UNDO 
    INITIAL "nt-loyaltyprog.p". 
FIND FIRST nightaudit WHERE nightaudit.programm = progname 
   NO-LOCK NO-ERROR.
IF NOT AVAILABLE nightaudit THEN RETURN.
ASSIGN reihenfolge = nightaudit.reihenfolge.

FIND FIRST htparam WHERE htparam.paramnr = 41 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN allocated-point = htparam.finteger.
/*
FIND FIRST nitehist WHERE nitehist.datum EQ (ci-date - 1) AND nitehist.reihenfolge EQ reihenfolge
    AND ENTRY(1,nitehist.LINE,"|") EQ "H"
    AND ENTRY(2,nitehist.LINE,"|") EQ "SEND=0" NO-LOCK NO-ERROR.
IF AVAILABLE nitehist THEN ci-date = ci-date - 1.
ELSE FIND FIRST nitehist WHERE nitehist.datum EQ ci-date AND nitehist.reihenfolge EQ reihenfolge
    AND ENTRY(1,nitehist.LINE,"|") EQ "H"
    AND ENTRY(2,nitehist.LINE,"|") EQ "SEND=0" NO-LOCK NO-ERROR.
IF NOT AVAILABLE nitehist THEN RETURN.


avail-data = YES.*/

EMPTY TEMP-TABLE flist.
EMPTY TEMP-TABLE fline-list.

FOR EACH nitehist WHERE nitehist.datum GE (ci-date - 1) AND nitehist.reihenfolge EQ reihenfolge
    AND ENTRY(1,nitehist.LINE,"|") EQ "H"
    AND ENTRY(2,nitehist.LINE,"|") EQ "SEND=0" NO-LOCK:

    CREATE flist.    
    ASSIGN
        flist.rechnr        = INTEGER(ENTRY(3,nitehist.LINE,"|"))
        flist.usr           = ENTRY(4,nitehist.LINE,"|")
        flist.saldo         = ENTRY(5,nitehist.LINE,"|")
        flist.dept          = INTEGER(ENTRY(6,nitehist.LINE,"|"))
        flist.created       = ENTRY(7,nitehist.LINE,"|")
        flist.checkin       = ENTRY(8,nitehist.LINE,"|")
        flist.checkout      = ENTRY(9,nitehist.LINE,"|")
        flist.pax           = INTEGER(ENTRY(10,nitehist.LINE,"|"))
        flist.discount      = ENTRY(11,nitehist.LINE,"|")
        flist.reslinnr      = ENTRY(12, nitehist.LINE, "|")
        flist.service       = INTEGER(ENTRY(13, nitehist.LINE, "|"))
        flist.resnr         = INTEGER(ENTRY(14, nitehist.LINE, "|"))
        flist.breslin       = INTEGER(ENTRY(15, nitehist.LINE, "|"))
        flist.gastnr        = INTEGER(ENTRY(16, nitehist.LINE, "|"))
        flist.gastpay       = INTEGER(ENTRY(17, nitehist.LINE, "|"))
        flist.id            = RECID(nitehist)
		.
	IF allocated-point EQ 2 OR allocated-point EQ 3 THEN
	DO:
		FOR EACH buffnite WHERE buffnite.datum EQ nitehist.datum
			AND buffnite.reihenfolge EQ reihenfolge
			AND ENTRY(1,buffnite.LINE,"|") EQ "L"
			AND INTEGER(ENTRY(2,buffnite.LINE,"|")) EQ flist.rechnr
			AND INTEGER(ENTRY(3,buffnite.LINE,"|")) EQ flist.dept 
			AND INTEGER(ENTRY(8,buffnite.LINE,"|")) EQ flist.resnr
			AND ENTRY(9,buffnite.LINE,"|") EQ flist.reslinnr NO-LOCK:

			CREATE fline-list.
			ASSIGN
				fline-list.rechnr       = flist.rechnr
				fline-list.dept         = flist.dept
				fline-list.bezeich      = ENTRY(4,buffnite.LINE,"|")
				fline-list.price        = ENTRY(5,buffnite.LINE,"|")
				fline-list.rtcode       = ENTRY(6,buffnite.LINE,"|")
				fline-list.rmtype       = ENTRY(7,buffnite.LINE,"|")
				fline-list.resnr        = INTEGER(ENTRY(8,buffnite.LINE,"|"))
				fline-list.reslinnr     = ENTRY(9,buffnite.LINE,"|")
				fline-list.breslin      = INTEGER(ENTRY(10,buffnite.LINE,"|"))
				fline-list.gastnr       = INTEGER(ENTRY(11,buffnite.LINE,"|"))
				fline-list.gastpay      = INTEGER(ENTRY(12,buffnite.LINE,"|"))
				.
		END.
	END.
	ELSE
	DO:
		FOR EACH buffnite WHERE buffnite.datum EQ nitehist.datum
			AND buffnite.reihenfolge EQ reihenfolge
			AND ENTRY(1,buffnite.LINE,"|") EQ "L"
			AND INTEGER(ENTRY(2,buffnite.LINE,"|")) EQ flist.rechnr
			AND INTEGER(ENTRY(3,buffnite.LINE,"|")) EQ flist.dept NO-LOCK:

			CREATE fline-list.
			ASSIGN
				fline-list.rechnr       = flist.rechnr
				fline-list.dept         = flist.dept
				fline-list.bezeich      = ENTRY(4,buffnite.LINE,"|")
				fline-list.price        = ENTRY(5,buffnite.LINE,"|")
				fline-list.rtcode       = ENTRY(6,buffnite.LINE,"|")
				fline-list.rmtype       = ENTRY(7,buffnite.LINE,"|")
				fline-list.resnr        = INTEGER(ENTRY(8,buffnite.LINE,"|"))
				fline-list.reslinnr     = ENTRY(13,buffnite.LINE,"|")
				fline-list.breslin      = INTEGER(ENTRY(10,buffnite.LINE,"|"))
				fline-list.gastnr       = INTEGER(ENTRY(11,buffnite.LINE,"|"))
				fline-list.gastpay      = INTEGER(ENTRY(12,buffnite.LINE,"|"))
				.
		END.		
	END.
END.

FOR EACH flist:
    record_count = record_count + 1.
END.

IF record_count GT 0 THEN avail-data = YES.
