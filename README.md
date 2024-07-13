# BachMatch

## Participants / Team Members

| Member Name    | Student Number |
| -------------- | -------------- |
| Tim Kuhn       | 8284060        |
| Hendrik Träber | 6367227        |
| Paul Brüderle  | MISSING        |
| David Kleiner  | MISSING        |
| Gülbahar Cogac | 5801309        |

## TODO:

(This section gets deleted when everything is done)
Verfassen Sie eine Dokumentation, die den Aufbau, die Implementierung und die
Funktionalitäten der Anwendung beschreibt. Fassen Sie die Ergebnisse, Herausforderungen
und Lernerfahrungen in einem Abschlussbericht zusammen.

Dokumentation enthält Idee der Anwendung, Architektur, Entwurf, Screencast eines
Demos, etc. in der Datei README.md (keine verteilte Dokumentation)

Dokumentation, die den Aufbau, die Implementierung und die
Funktionalitäten der Anwendung beschreibt. Fassen Sie die Ergebnisse, Herausforderungen
und Lernerfahrungen in einem Abschlussbericht zusammen.

## Thema

## Zielsetzung

## Use-Case:

für Studenten, finden des idealen wissenschaftlichen Betreuers

## Structure

Grundaufbau gegeben, Anwendung basierend auf der Kappa-Architektur und Apache Spark als zentrale Technologie

Unsere Änderungen:

Unsere Daten:
BetruerFertig.csv Daten über Betreuer in Form von fachgebiet und einer genaueren Beschreibung in welchen Themenbereichen diese tätig sind
extracted_abstracts.csv DAten über Studenten, Titel und Abstract

This Proof-Of-Concept is based on a Use-Case-Demo made available by our professor, Prof. Dr. Pfisterer. We did make some changes.

Kurzerklaerung:
Nodejs Express Web-App, verbunden mit KAFKA zur Datenuebertragung,
Apache Spark nimmt die Eingaben des Abstracts und vektorisiert sie,
Spark schreibt das alles in eine Weaviate datenbank
von dort kann sich die Web-App die ergebnisse holen

kafka benutzt ein hadoop dateisystem

in weaviate werden 3 Sachen gespeichert:
Texte ueber wiss. Betreuer, und deren Vektoren
Beispiel Texte fuer 'wissen. arbeiten'
texte die die user eingeben haben

das alles wird in einem k8s ausgefuehrt.

## Implementation

## Functionality

## (Anwendung)

## Results

## Challenges

- finden eines guten Use cases
- Einrichten des vorgegebenen Grundaufbau
