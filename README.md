# Bachelor Thesis
Dieses Repository beinhaltet den Programmcode der Bachelor Thesis "Computerlinguistische Analyse empirischer neurolinguistischer Daten". Mithilfe dieses Codes ist es möglich 


#### Inhaltsverzeichnis
- [Daten](#daten)
- [Installation](#installation)
- [Nutzung](#nutzung)
- [Literatur](#literatur)

## Daten
Die verwendeten Daten sind Ergebnisse der neurolinguistischen Studie von Espey et al. Die Originaldaten sind im Ordner [alte_Studiendaten](https://github.com/larissa0898/bachelor-thesis/tree/main/Daten/alte%20Studiendaten) zu finden. Die bereinigten Daten sind in [Preprocessed_Daten](https://github.com/larissa0898/bachelor-thesis/tree/main/Daten/Preprocessed%20Daten) hinterlegt.<br />
In den Ordnern [Sentiment_Daten](https://github.com/larissa0898/bachelor-thesis/tree/main/Daten/Sentiment%20Daten) und [Transformer_Daten](https://github.com/larissa0898/bachelor-thesis/tree/main/Daten/Transformer%20Daten) sind die Ergebnisse dieser Bachelor Thesis gespeichert.

## Installation
Zunächst müssen alle Dateien dieses GitHub Repositories gedownloadet werden.<br />
Mit 'pip install -r requirements.txt' werden alle benötigten Bibliotheken installiert.<br />
Für diese Bachelor Thesis wurde die Python Version 3.9.5 benutzt. Die Versionen der benutzten Bibliotheken können in der 'requirements.txt'-Datei gefunden werden. 

## Nutzung

Um den Code verwenden zu können, müssen zunächst die Pfade in [config.ini](https://github.com/larissa0898/bachelor-thesis/blob/main/config.ini) geändert werden.<br />


### Sentimentanalyse
Für die Sentimentanalyse wird hauptsächlich der Code in [sentimentAnalysis.py](https://github.com/larissa0898/bachelor-thesis/blob/main/Code/Sentiment%20model/sentimentAnalysis.py) genutzt.
Der Code zum Vergleich der Sentimentwerte der neutralen und emotionalen Situationsbeschreibungen wird in [checkEmotionalityOfSituations.py](https://github.com/larissa0898/bachelor-thesis/blob/main/Code/Sentiment%20model/checkEmotionalityOfSituations.py) ausgeführt.
Zur Berechnung der Korrelation zwischen Valenz- und Sentimentwerten kann der Code in [correlationValenceSIA.py](https://github.com/larissa0898/bachelor-thesis/blob/main/Code/Sentiment%20model/correlationValenceSIA.py) genutzt werden


### Transformer-Modelle

#### Zero-Shot-Classification
Zur Zero-Shot-Classification wird der Code im Ordner [Zero-Shot](https://github.com/larissa0898/bachelor-thesis/tree/main/Code/Transformer%20model/Zero-Shot) benötigt. In [zeroShotWithParticipantFeatures.py](https://github.com/larissa0898/bachelor-thesis/blob/main/Code/Transformer%20model/Zero-Shot/zeroShotWithParticipantFeatures.py) wird der Code zur Zero-Shot-Classification der Features der Teilnehmenden gespeichert. In [zeroShotWithMaskedFeatures.py](https://github.com/larissa0898/bachelor-thesis/blob/main/Code/Transformer%20model/Zero-Shot/zeroShotWithMaskedFeatures.py) findet sich der Code für die generierten Modell-Features.


#### Mask-Filling

| `Workflow 1` | → | &#8594; | `Workflow 2` |

## Literatur
**Linda Espey, Marta Ghio, Christian Bellebaum und Laura Bechtold (2021).** *That means something to me: the effect of linguistic and emotional experience on the acquisition and processing of novel abstract concepts.*