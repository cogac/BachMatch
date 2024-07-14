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

## Topic: Finding the Perfect Academic Supervisor

Finding an academic supervisor who aligns perfectly with a student's research interests is a critical step in the success of any research project. Our program addresses this need by providing a systematic and efficient way for students to connect with supervisors whose expertise closely matches their research topics. By leveraging advanced search algorithms and a comprehensive database of academic profiles, we aim to make the process of finding the right supervisor both quick and accurate.


## Objective

The primary objective of our program is to facilitate the matching process between students and academic supervisors. By inputting their research title and a brief summary, students can use our program to search through a curated database of potential supervisors. Each supervisor has listed their research areas and provided a description of their expertise. The program’s goal is to return the top 10 most suitable supervisors based on the relevance of their expertise to the student's research. This not only saves time but also enhances the quality of academic mentorship by ensuring a better fit between students and supervisors.


## Use-Case:

Students:

Graduate students can use our program to find the best academic supervisor for their research projects. They enter their project title and a brief abstract, and the program searches a database of supervisors. The program then provides a list of the top 10 supervisors whose expertise best matches the student's research topic. This process ensures that students find the most relevant and suitable supervisors efficiently.

## Datasets

- BetruerFertig.csv: This file contains data about supervisors, including their area of expertise and a detailed description of their research topics.
- extracted_abstracts.csv: This file contains data about students, including the title of their research project and an abstract.


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

## Results

## Challenges

- finden eines guten Use cases
- Einrichten des vorgegebenen Grundaufbau
