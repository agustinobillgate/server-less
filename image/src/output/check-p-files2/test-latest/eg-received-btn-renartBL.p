DEFINE TEMP-TABLE t-eg-budget LIKE eg-budget.

DEF OUTPUT PARAMETER TABLE FOR t-eg-budget.

FOR EACH eg-budget:
    CREATE t-eg-budget.
    BUFFER-COPY eg-budget TO t-eg-budget.
END.
