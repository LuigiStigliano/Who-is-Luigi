# Who is Luigi?

Questo repository contiene un esempio che dimostra il funzionamento della libreria Python `luigi`. Luigi è un framework sviluppato da Spotify per costruire pipeline complesse di batch job. Gestisce le dipendenze, il workflow, la visualizzazione, la gestione degli errori e altro.

## Pipeline Dimostrativa

Questo progetto mostra diverse mini-pipeline per illustrare vari concetti di Luigi, organizzate in moduli per maggiore chiarezza:

### 1. Pipeline Base (`src/tasks/base_tasks.py`)
- **`CreateInputFile`**: Crea un file di testo semplice (`data/input.txt` di default).
- **`ProcessFile`**: Legge il file creato, conta il numero di righe e scrive il risultato in un altro file (`data/output.txt` di default).
  
  La task `ProcessFile` dipende da `CreateInputFile`.

### 2. Pipeline con Task Parallele (`src/tasks/parallel_tasks.py`)
- **`CreateParallelFileA`** e **`CreateParallelFileB`**: Creano due file distinti (`data/parallel_example/fileA.txt` e `fileB.txt`). Queste possono essere eseguite in parallelo.
- **`ProcessParallelFiles`**: Dipende da `CreateParallelFileA` e `CreateParallelFileB`, legge i loro output e crea un file di sommario (`data/parallel_summary.txt`).

### 3. Pipeline con Gestione Fallimenti (`src/tasks/failure_example.py`)
- **`FailingTask`**: Una task progettata per fallire sollevando un'eccezione.
- **`DependsOnFailingTask`**: Dipende da `FailingTask` per mostrare come Luigi gestisce le dipendenze fallite.

### 4. Pipeline CSV (Caso d'uso più complesso) (`src/tasks/csv_tasks.py`)
- **`CreateSampleCSV`**: Genera un file CSV con dati di esempio (`data/sample_data.csv`).
- **`ProcessCSVFile`**: Legge il file CSV, esegue calcoli (es. valore totale, conteggio prodotti) e scrive un report (`data/csv_summary_report.txt`).

### 5. `RunAllExamples` (`src/tasks/wrapper_tasks.py`)
Una `luigi.WrapperTask` che raggruppa le pipeline principali (`ProcessFile`, `ProcessParallelFiles`, `ProcessCSVFile`) per una facile esecuzione combinata. È la task di default quando si esegue `python src/pipeline.py`.

---

## Installazione

1. **Clonare il repository:**
   ```bash
   git clone https://github.com/LuigiStigliano/Who-is-Luigi.git
   cd Who-is-Luigi
   ```

2. **Creare e attivare un ambiente virtuale:**
   ```bash
   # Su Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Su macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Installare le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```
   
---

## Esecuzione

Per eseguire la pipeline, usa il comando `python src/pipeline.py` seguito dalla Task finale che vuoi eseguire (ad es. `ProcessFile`, `ProcessCSVFile`, `RunAllExamples`) e `--local-scheduler`. Lo script `src/pipeline.py` importa tutte le task necessarie dai sottomoduli.

### Comandi di Esempio

- **Eseguire tutte le pipeline principali (default):**
  ```bash
  python src/pipeline.py RunAllExamples --local-scheduler
  ```
  *(Se esegui `python src/pipeline.py --local-scheduler` senza specificare una task, `RunAllExamples` verrà eseguita come da configurazione nel file.)*

- **Eseguire la pipeline base:**
  ```bash
  python src/pipeline.py ProcessFile --local-scheduler
  ```

- **Eseguire la pipeline con task parallele:**
  ```bash
  python src/pipeline.py ProcessParallelFiles --local-scheduler
  ```

- **Eseguire la pipeline CSV:**
  ```bash
  python src/pipeline.py ProcessCSVFile --local-scheduler
  ```

- **Testare una task che fallisce:**
  ```bash
  python src/pipeline.py DependsOnFailingTask --local-scheduler
  ```

### Dettagli del comando

- **`python src/pipeline.py`**: Esegue lo script Python principale che orchestra le task.
- **`<NomeTask>`**: Specifica la task finale che vuoi eseguire. Luigi risolverà e eseguirà le dipendenze necessarie.
- **`--local-scheduler`**: Dice a Luigi di usare uno scheduler locale semplice.

### Esempio di Parametrizzazione da CLI

Puoi sovrascrivere i parametri di default delle task direttamente da riga di comando. Il formato è `--<NomeTask>-<nome-parametro> <valore>`.

Ad esempio, per cambiare il file di input per `CreateInputFile` (che è una dipendenza di `ProcessFile`):

```bash
python src/pipeline.py ProcessFile --CreateInputFile-filename data/mio_input_custom.txt --ProcessFile-input-file-param data/mio_input_custom.txt --local-scheduler
```

*In questo caso, ProcessFile usa input_file_param per specificare il nome del file che CreateInputFile deve generare.*

## Cosa succederà (Esempio con ProcessFile)

1. Luigi controllerà se l'output di `ProcessFile` (`data/output.txt`) esiste.
2. Se non esiste, controllerà le dipendenze di `ProcessFile`, ovvero `CreateInputFile` (dal modulo `base_tasks`).
3. Controllerà se l'output di `CreateInputFile` (`data/input.txt`) esiste.
4. Se `data/input.txt` non esiste, eseguirà `CreateInputFile.run()`.
5. Una volta soddisfatta la dipendenza, Luigi eseguirà `ProcessFile.run()`.

**Nota:** Se riesegui il comando, Luigi vedrà che gli output esistono già e non farà nulla (idempotenza). Per forzare una riesecuzione, cancella i file di output rilevanti.

## Visualizzazione Web con luigid

Luigi include un server web (`luigid`) che fornisce una UI per visualizzare lo stato delle task e le loro dipendenze.

### Avvia luigid

In un terminale separato, esegui:
```bash
luigid
```
Il server sarà tipicamente accessibile su http://localhost:8082.

### Esegui la tua pipeline senza --local-scheduler

Ad esempio:
```bash
python src/pipeline.py ProcessCSVFile
```
La pipeline si registrerà con il demone `luigid`.

### Apri il browser
Naviga a http://localhost:8082 per vedere la pipeline.

## Concetti chiave di Luigi mostrati

- **Task**: Unità di lavoro. Definite come classi che ereditano da `luigi.Task`.
- **Target**: L'output di una Task. Definito nel metodo `output()`.
- **requires()**: Definisce le dipendenze di una Task.
- **run()**: Contiene la logica effettiva della Task.
- **Parametri** (`luigi.Parameter`): Permettono di configurare le Task, anche da CLI.
- **Scheduler Locale**: Per esecuzioni semplici.
- **WrapperTask**: Task speciali per raggruppare altre task.
- **Idempotenza**: Le task non vengono rieseguite se il loro output esiste già.
- **Modularizzazione**: Divisione delle task in file separati per una migliore organizzazione.
