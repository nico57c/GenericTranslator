==== plugin extractIpRangeFromFail2Ban ====

Ce plugin permet d'extraire une plage d'adresses IP d'un mail en provenance de fail2ban.
Le résultat est une sortie json où chaque ligne prend la forme suivante :
    { range: ["{ipStart}", "{ipEnd}"], ip: "{ip}", infos: { type: "{NetType}", name: "{NetName}", orga: "{Organization}" }

=== Exec ===

py ../../mainGt.py --regex settings/regex.properties --messages settings/messages.properties -l fr -e --plugin plugin.py --input test/mail0
