==== plugin extractXmlFromJavaSource ====

Ce plugin permet d'extraire un code source Java utilisant une librairie XML, sous la forme d'un chemin de type "path0>path1>path2>path3"

=== Exec ===

py ../../mainGt.py --regex settings/regex.properties --messages settings/messages.properties -l fr -e --plugin plugin.py --input test/xmlFile.java

=== Description ===

Ce plugin récupère la sortie python suite à l'extraction des mot-clef de traduction contenu dans '.element("..."', '.root("..."'.
Un appel à 'end()' termine et supprime la branche courante de la sortie écran suivante.

@TODO :
  Ajouter la détection d'un ';' en plus du 'end()' pour terminer la ligne courante