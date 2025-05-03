# Esempio con Luigi

Questo repository contiene un esempio basilare che dimostra il funzionamento della libreria Python `luigi`. Luigi è un framework sviluppato da Spotify per costruire pipeline complesse di batch job. Gestisce le dipendenze, il workflow, la visualizzazione, la gestione degli errori e altro ancora che devo ancora capire e imparare.

## Pipeline Dimostrativa

Questo esempio specifico mostra una pipeline con due task:

1. **`CreateInputFile`**: Crea un file di testo semplice (`data/input.txt`).
2. **`ProcessFile`**: Legge il file `data/input.txt`, conta il numero di righe e scrive il risultato in un altro file (`data/output.txt`).

La task **`ProcessFile`** dipende dalla task **`CreateInputFile`**.

---

## Struttura del Progetto

```plaintext
Who-is-Luigi/
├── src/               # Cartella principale per il codice sorgente
|    └── pipeline.py   # Codice Python con le task Luigi
├── README.md          # Documentazione del progetto
├── requirements.txt   # Dipendenze Python (solo luigi)
└── data/              # Directory creata durante l'esecuzione
    ├── input.txt      # File generato da CreateInputFile
    └── output.txt     # File generato da ProcessFile
```

---

## Prerequisiti

- **Python 3.x**

---

## Installazione

1. **Clona il repository:**
   ```bash
   git clone https://github.com/LuigiStigliano/Who-is-Luigi.git
   cd Who-is-Luigi
   ```

2. **(Consigliato) Crea e attiva un ambiente virtuale:**
   ```bash
    Su Windows
    python -m venv .venv
    .venv\Scripts\activate

    Su macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
   ```

3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Esecuzione

Per eseguire la pipeline, usa il seguente comando dalla directory principale (`Who-is-Luigi`):

```bash
python src/pipeline.py ProcessFile --local-scheduler
```

### Dettagli del comando

- **`python pipeline.py`**: Esegue lo script Python.
- **`ProcessFile`**: Specifica la task finale che vuoi eseguire. Luigi capirà che `ProcessFile` richiede `CreateInputFile` e la eseguirà per prima, se necessario.
- **`--local-scheduler`**: Dice a Luigi di usare uno scheduler locale semplice invece di cercare un demone `luigid` centrale. È ideale per lo sviluppo e l'esecuzione locale.

---

### Cosa succederà

1. Luigi controllerà se l'output di **`ProcessFile`** (`data/output.txt`) esiste già.
2. Se non esiste, controllerà le dipendenze di **`ProcessFile`**, ovvero **`CreateInputFile`**.
3. Controllerà se l'output di **`CreateInputFile`** (`data/input.txt`) esiste già.
4. Se `data/input.txt` non esiste, eseguirà il metodo `run()` di **`CreateInputFile`**. Verrà creato il file `data/input.txt`.
5. Una volta che la dipendenza è soddisfatta (cioè `data/input.txt` esiste), Luigi eseguirà il metodo `run()` di **`ProcessFile`**. Questo leggerà `data/input.txt`, conterà le righe e creerà `data/output.txt`.
6. Se riesegui il comando, Luigi vedrà che `data/output.txt` esiste già e non farà nulla, mostrando che le task sono già completate (idempotenza). Per forzare una riesecuzione, dovresti cancellare i file `data/input.txt` e `data/output.txt`.

---

## Concetti chiave di Luigi mostrati

- **Task**: Unità di lavoro (es. `CreateInputFile`, `ProcessFile`). Definite come classi che ereditano da `luigi.Task`.
- **Target**: L'output di una Task (es. un file). Definito nel metodo `output()`. Luigi usa l'esistenza del Target per determinare se una Task è completata. `luigi.LocalTarget` rappresenta un file nel filesystem locale.
- **`requires()`**: Metodo che definisce le dipendenze di una Task. Restituisce le istanze delle Task che devono essere completate prima che questa Task possa iniziare.
- **`run()`**: Metodo che contiene la logica effettiva per eseguire la Task. Viene chiamato da Luigi solo se il Target definito in `output()` non esiste e tutte le dipendenze definite in `requires()` sono soddisfatte.
- **Parametri**: Permettono di configurare le Task dall'esterno (es. `filename` in `CreateInputFile`).
- **Local Scheduler**: Un modo semplice per eseguire pipeline Luigi senza un server scheduler centrale.

---

Questo è un punto di partenza molto semplice. Luigi offre molte più funzionalità per pipeline complesse, gestione di parametri, interfacce utente web, esecuzione distribuita e integrazioni con vari sistemi (HDFS, S3, database, ecc.).

---

## Cosa verrà aggiunto in futuro in questa repository

1. **Esempio di parametrizzazione da CLI**: Mostrare come passare parametri alle task direttamente da riga di comando.
2. **Gestione errori e logging**: Utilizzare il modulo logging invece di print per la gestione dei messaggi, mostrando come Luigi integra i log.
3. **Aggiungere una sezione "Troubleshooting"**: Ad esempio, cosa fare se si riceve un errore di permessi o se i file non vengono creati.
4. **Esempio di visualizzazione web**: Anche solo una nota su come avviare il web server di Luigi (luigid) per vedere la pipeline graficamente. Dico la nota perchè ancora non ho capito bene come farlo partire neanche io :D
5. **Test Automatici**: Aggiungere un semplice test automatico che verifica la creazione dei file di output.
6. **Esempio di task parallele**: Mostrare la gestione contemporanea di task.
7. **Esempio di task che fallisce**: Per mostrare come Luigi gestisce il fallimento.
8. **Un caso pratico leggermente più complesso**: Utilizzando un file CSV o JSON da elaborare.
