# Bachelor Thesis
Dieses Repository beinhaltet den Programmcode der Bachelor Thesis "Computerlinguistische Analyse empirischer neurolinguistischer Daten".


#### Inhaltsverzeichnis
- [Installation](#installation)
- [Daten](#daten)
- [Workflow](#workflow)
- [Literatur](#literatur)

## Installation
Um den Code lokal zu installieren und auszuführen, müssen die folgenden Schritte ausgeführt werden:
1. **Klonen des Repositories**
    ```bash
    git clone https://github.com/larissa0898/bachelor-thesis.git
    cd bachelor-thesis
    ```
2. **Erstellung und Aktivierung einer virtuellen Umgebung:**
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # Unter Windows: myenv\Scripts\activate
    ```
3. **Installation der erforderlichen Pakete:**
    ```bash
    pip install -r requirements.txt
    ```

Für diese Bachelor Thesis wurde die Python Version 3.9.5 benutzt.

## Daten
Die verwendeten Daten sind Ergebnisse der neurolinguistischen Studie von Espey et al. Die Originaldaten sind im Ordner `alte_Studiendaten` zu finden. 

## Workflow

In diesem Abschnitt werden die Ansätze, deren Beschreibungen, dazugehörige Python-Codes, sowie die Endergebnisse in den jeweiligen Ordnern zusammengefasst.<br />

|   Ansatz   | Pre-Processing   |Sentimentanalyse    | Transformer-Modell: DistilRoBERTa  | Transformer-Modell: BART  |
| ------------- | ------------- |------------- | ------------- | ------------- |
| Beschreibung   | Bereinigung und Übersetzung der Daten  |Berechnung der Sentimentwerte, sowie Korrelation der Valenz- & Sentimentwerte | Generierung der Feature-Ketten  | Zuordnung der Feature-Ketten & Definitionen zu Pseudowörtern  | 
| Python-Code    | `extractingData.py`<br /> `translateData.py` <br />`translateSituations.py`   |`sentimentAnalysis.py` <br />`correlationValenceSIA.py` | `generatingFeatures.py`  | `zeroShotWithMaskedFeatures.py` <br />`zeroShotWithParticipantFeatures.py`  | 
| Ergebnisse    | `PreProcessing`   |`Sentiment_Daten` | `Transformer_Daten` | `Transformer_Daten` |

## Literatur
**Linda Espey, Marta Ghio, Christian Bellebaum und Laura Bechtold (2021).** *That means something to me: the effect of linguistic and emotional experience on the acquisition and processing of novel abstract concepts.*