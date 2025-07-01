DEFINE TEMP-TABLE member-list
    FIELD member-code      AS CHARACTER
    FIELD member-type    AS CHARACTER
	FIELD titled  AS CHARACTER
	FIELD fullname AS CHARACTER
	FIELD firstname  AS CHARACTER
	FIELD lastname   AS CHARACTER
	FIELD email    AS CHARACTER
	FIELD mobilenumber    AS CHARACTER
	FIELD birthdate    AS DATE
	FIELD gender    AS CHARACTER
	FIELD country    AS CHARACTER
	FIELD city    AS CHARACTER
	FIELD address    AS CHARACTER
	FIELD stamps    AS INTEGER
	FIELD reg-date    AS DATE
	FIELD is-active    AS LOGICAL
.
DEFINE INPUT PARAMETER case-type  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER gastnr AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR member-list.
DEFINE INPUT PARAMETER user-init  AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER updated AS LOGICAL INIT NO NO-UNDO.
DEFINE BUFFER bguest    FOR guest.
DEFINE VARIABLE nr AS INT NO-UNDO.
DEFINE VARIABLE t-guest-nat     AS CHAR     NO-UNDO.
FIND FIRST member-list NO-LOCK NO-ERROR.
CASE case-type:
	WHEN 1 THEN /*not create new guest*/
	DO:
		FIND FIRST mc-guest WHERE mc-guest.gastnr = gastnr NO-LOCK NO-ERROR.
		IF NOT AVAILABLE mc-guest THEN
		DO :
			CREATE mc-guest.
			ASSIGN
				mc-guest.gastnr = gastnr
				mc-guest.cardnum = member-list.member-code
				mc-guest.number1 = member-list.stamps
				mc-guest.activeflag = member-list.is-active
			.
			FIND FIRST mc-types WHERE mc-types.bezeich = member-list.member-type NO-LOCK NO-ERROR.
			IF AVAILABLE mc-types THEN
			DO:
				mc-guest.nr = mc-types.nr.

			END.
			ELSE IF NOT AVAILABLE mc-types THEN
			DO:
				FIND LAST mc-types NO-LOCK NO-ERROR.
				IF AVAILABLE mc-types THEN
					nr = mc-types.nr + 1.
				CREATE mc-types.
				ASSIGN
					mc-types.bezeich = member-list.member-type
					mc-types.nr      = nr
					mc-guest.nr 	= nr.
			END.
			FIND FIRST bguest WHERE bguest.gastnr = gastnr EXCLUSIVE-LOCK NO-ERROR.
			IF AVAILABLE bguest THEN
			DO:
				IF member-list.birthdate NE ? THEN bguest.geburtdatum1 = member-list.birthdate.
				IF member-list.email NE "" THEN bguest.email-adr = member-list.email.
				IF member-list.mobilenumber NE "" THEN bguest.mobil-telefon = member-list.mobilenumber.
			END.
			FIND CURRENT bguest NO-LOCK.
			RELEASE bguest.
			/*VHP-LOG*/ /*NC-23/03/2021*/
			FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
			DO:
				CREATE res-history. 
				ASSIGN 
					res-history.nr     = bediener.nr 
					res-history.datum  = TODAY 
					res-history.zeit   = TIME 
					res-history.action = "Membership"
				.
				res-history.aenderung = "Create/Tag MemberID " + member-list.member-code + " to PMS, Date:" + STRING(TODAY,"99/99/99") + ".".
			END.
		END.
		ELSE IF AVAILABLE mc-guest THEN
		DO:
			FIND CURRENT mc-guest EXCLUSIVE-LOCK.
			ASSIGN
				mc-guest.cardnum = member-list.member-code
				mc-guest.number1 = member-list.stamps
				mc-guest.activeflag = member-list.is-active.
			FIND FIRST mc-types WHERE mc-types.bezeich = member-list.member-type NO-LOCK NO-ERROR.
			IF AVAILABLE mc-types THEN
				mc-guest.nr = mc-types.nr.
			IF NOT AVAILABLE mc-types THEN
			DO:
				FIND LAST mc-types NO-LOCK NO-ERROR.
				nr = mc-types.nr + 1.
				CREATE mc-types.
				ASSIGN
					mc-types.bezeich = member-list.member-type
					mc-types.nr      = nr
					mc-guest.nr 	= nr.
			END.
			FIND CURRENT mc-guest NO-LOCK.
			RELEASE mc-guest.
			FIND FIRST bguest WHERE bguest.gastnr = gastnr EXCLUSIVE-LOCK NO-ERROR.
			IF AVAILABLE bguest THEN
			DO:
				IF member-list.birthdate NE ? THEN bguest.geburtdatum1 = member-list.birthdate.
				IF member-list.email NE "" THEN bguest.email-adr = member-list.email.
				IF member-list.mobilenumber NE "" THEN bguest.mobil-telefon = member-list.mobilenumber.
			END.
			FIND CURRENT bguest NO-LOCK.
			RELEASE bguest.
			/*VHP-LOG*/ /*NC-23/03/2021*/
			FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
			DO:
				CREATE res-history. 
				ASSIGN 
					res-history.nr     = bediener.nr 
					res-history.datum  = TODAY 
					res-history.zeit   = TIME 
					res-history.action = "Membership"
				.
				res-history.aenderung = "Updated MemberID " + member-list.member-code + " to PMS, Date:" + STRING(TODAY,"99/99/99") + ".".
			END.
		END.
	END.
	WHEN 2 THEN /*create new guest if not found*/
	DO:
		FIND FIRST mc-guest WHERE mc-guest.cardnum = member-list.member-code NO-LOCK NO-ERROR.
		IF AVAILABLE mc-guest THEN
		DO :
			gastnr = mc-guest.gastnr.
			FIND CURRENT mc-guest EXCLUSIVE-LOCK.
			ASSIGN
				mc-guest.cardnum = member-list.member-code
				mc-guest.number1 = member-list.stamps
				mc-guest.activeflag = member-list.is-active.
			FIND FIRST mc-types WHERE mc-types.bezeich = member-list.member-type NO-LOCK NO-ERROR.
			IF AVAILABLE mc-types THEN
				mc-guest.nr = mc-types.nr.
			IF NOT AVAILABLE mc-types THEN
			DO:
				FIND LAST mc-types NO-LOCK NO-ERROR.
				nr = mc-types.nr + 1.
				CREATE mc-types.
				ASSIGN
					mc-types.bezeich = member-list.member-type
					mc-types.nr      = nr
					mc-guest.nr 	= nr.
			END.
			FIND CURRENT mc-guest NO-LOCK.
			RELEASE mc-guest.
			FIND FIRST bguest WHERE bguest.gastnr = gastnr EXCLUSIVE-LOCK NO-ERROR.
			IF AVAILABLE bguest THEN
			DO:
				IF member-list.birthdate NE ? THEN bguest.geburtdatum1 = member-list.birthdate.
				IF member-list.email NE "" THEN bguest.email-adr = member-list.email.
				IF member-list.mobilenumber NE "" THEN bguest.mobil-telefon = member-list.mobilenumber.
			END.
			FIND CURRENT bguest NO-LOCK.
			RELEASE bguest.
			/*VHP-LOG*/ /*NC-23/03/2021*/
			FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
			DO:
				CREATE res-history. 
				ASSIGN 
					res-history.nr     = bediener.nr 
					res-history.datum  = TODAY 
					res-history.zeit   = TIME 
					res-history.action = "Membership"
				.
				res-history.aenderung = "Updated MemberID " + member-list.member-code + " to PMS FROM Outlet Sync,Date:" + STRING(TODAY,"99/99/99") + ".".
			END.
		END.
		ELSE IF NOT AVAILABLE mc-guest THEN
		DO:
			FIND FIRST guest WHERE guest.NAME MATCHES member-list.lastname
                AND guest.email-adr = member-list.email NO-LOCK NO-ERROR.
			IF NOT AVAILABLE guest THEN
                FIND FIRST guest WHERE guest.NAME MATCHES member-list.lastname 
                AND guest.mobil-telefon = member-list.mobilenumber NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN
				FIND FIRST guest WHERE guest.NAME = member-list.fullname 
				AND guest.email-adr = member-list.email NO-LOCK NO-ERROR.
			IF NOT AVAILABLE guest THEN
				FIND FIRST guest WHERE guest.NAME = member-list.fullname 
				AND guest.mobil-telefon = member-list.mobilenumber NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN 
				FIND FIRST guest WHERE guest.email-adr = member-list.email NO-LOCK NO-ERROR.
			IF NOT AVAILABLE guest THEN 
				FIND FIRST guest WHERE guest.mobil-telefon = member-list.mobilenumber NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN 
				FIND FIRST guest WHERE guest.NAME = member-list.fullname NO-LOCK NO-ERROR.
			IF NOT AVAILABLE guest THEN 
			DO:
                FIND FIRST nation WHERE nation.bezeich = member-list.country NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
                ELSE 
                DO:
                    RUN if-siteminder-read-mappingbl.p (2, member-list.country, OUTPUT t-guest-nat).
					IF t-guest-nat NE "" THEN
					DO:
						FIND FIRST nation WHERE nation.kurzbez = t-guest-nat NO-LOCK NO-ERROR.
						IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
					END.
                    ELSE
                    DO:
                        FIND FIRST nation WHERE nation.bezeich MATCHES "*Unknown*"
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN t-guest-nat = nation.kurzbez.
                              
                    END.
                END.

                FIND LAST guest NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN gastnr = guest.gastnr + 1.
                CREATE guest.
                ASSIGN 
                    guest.gastnr    = gastnr
					guest.anrede1	= member-list.titled
                    guest.NAME      = member-list.firstname
                    guest.vorname1  = member-list.lastname
                    guest.adresse1  = member-list.address
                    guest.wohnort   = member-list.city
                    guest.land      = t-guest-nat
                    guest.email-adr = member-list.email
                    guest.mobil-telefon   = member-list.mobilenumber
                    guest.nation1   = t-guest-nat
					guest.geburtdatum1   = member-list.birthdate                    
                    .
					IF guest.NAME EQ "" THEN ASSIGN guest.NAME = member-list.fullname.
/*
                FIND FIRST guestseg WHERE guestseg.gastnr = ota-gastnr 
                    AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.
                IF AVAILABLE guestseg THEN
                DO:
                    rsegm = guestseg.segmentcode.
                    CREATE guestseg.
                    ASSIGN
                        guestseg.gastnr      = gastnrmember
                        guestseg.reihenfolge = 1
                        guestseg.segmentcode = rsegm
                        .    
                END.*/
            END.
            ELSE 
            DO:
                gastnr = guest.gastnr.
                FIND FIRST bguest WHERE RECID(bguest) = RECID(guest) EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN
					ASSIGN
					bguest.anrede1 = member-list.titled
					bguest.email-adr = member-list.email
					bguest.geburtdatum1 = member-list.birthdate
					bguest.mobil-telefon = member-list.mobilenumber
					.
                FIND CURRENT bguest NO-LOCK.
                RELEASE bguest.
            END.
			CREATE mc-guest.
			ASSIGN
				mc-guest.gastnr = gastnr
				mc-guest.cardnum = member-list.member-code
				mc-guest.number1 = member-list.stamps
				mc-guest.activeflag = member-list.is-active
			.
			FIND FIRST mc-types WHERE mc-types.bezeich = member-list.member-type NO-LOCK NO-ERROR.
			IF AVAILABLE mc-types THEN
			DO:
				mc-guest.nr = mc-types.nr.

			END.
			ELSE IF NOT AVAILABLE mc-types THEN
			DO:
				FIND LAST mc-types NO-LOCK NO-ERROR.
				IF AVAILABLE mc-types THEN
					nr = mc-types.nr + 1.
				CREATE mc-types.
				ASSIGN
					mc-types.bezeich = member-list.member-type
					mc-types.nr      = nr
					mc-guest.nr 	= nr.

			END.
			/*VHP-LOG*/ /*NC-23/03/2021*/
			FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
			IF AVAILABLE bediener THEN
			DO:
				CREATE res-history. 
				ASSIGN 
					res-history.nr     = bediener.nr 
					res-history.datum  = TODAY 
					res-history.zeit   = TIME 
					res-history.action = "Membership"
				.
				res-history.aenderung = "Create/Tag MemberID " + member-list.member-code + " to PMS FROM Outlet Sync,Date:" + STRING(TODAY,"99/99/99") + ".".
			END.
		END.
	END.
END.

updated = YES.