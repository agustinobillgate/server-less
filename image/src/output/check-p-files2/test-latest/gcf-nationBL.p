
DEF TEMP-TABLE nation-list 
  FIELD nationnr LIKE nation.nationnr
  FIELD kurzbez  LIKE nation.kurzbez
  FIELD bezeich  LIKE nation.bezeich
.

DEF INPUT  PARAMETER inp-natcode AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE       FOR nation-list.

IF inp-natcode = 0 THEN
FOR EACH nation WHERE nation.natcode = 0 NO-LOCK:
  CREATE nation-list.
  BUFFER-COPY nation TO nation-list.
END.

ELSE IF inp-natcode GT 0 THEN
FOR EACH nation WHERE nation.natcode = inp-natcode NO-LOCK:
  CREATE nation-list.
  BUFFER-COPY nation TO nation-list.
END.

ELSE IF inp-natcode LT 0 THEN
FOR EACH nation WHERE nation.natcode GT 0 NO-LOCK:
  CREATE nation-list.
  BUFFER-COPY nation TO nation-list.
END.
