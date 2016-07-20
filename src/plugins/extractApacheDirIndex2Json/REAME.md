==== plugin extractApacheDirIndex2Json ====

Ce plugin permet d'extraire la liste des fichiers contenus dans une page HTML généré par Apache.
Le résultat est une sortie json où chaque fichier renseigné prend la forme suivante :
    ["{filename}","{date}","{size}"]

=== Exec ===

py ../../mainGt.py --regex settings/regex.properties --messages settings/messages.properties -l fr --plugin plugin.py --input test/list0.htm
