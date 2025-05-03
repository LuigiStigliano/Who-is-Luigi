import luigi
import time
import os

# --- Task 1: Creare un file di input ---
class CreateInputFile(luigi.Task):
    """
    Questa Task crea un semplice file di testo che servirà da input
    per la task successiva.
    """
    # Parametro opzionale per rendere il nome del file configurabile
    filename = luigi.Parameter(default='data/input.txt')

    def output(self):
        """
        Definisce il file che questa Task produrrà.
        Luigi usa questo metodo per determinare se la Task è già stata completata.
        Restituisce un oggetto Target (in questo caso, un file locale).
        """
        # Assicurati che la directory 'data' esista
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        return luigi.LocalTarget(self.filename)

    def run(self):
        """
        La logica effettiva della Task. Viene eseguita solo se l'output() non esiste.
        Qui scriviamo del contenuto nel file di output.
        """
        print(f"Esecuzione di CreateInputFile: creazione di {self.output().path}...")
        time.sleep(2) # Simula un po' di lavoro
        with self.output().open('w') as f:
            f.write("Questa è la prima riga.\n")
            f.write("Luigi è utile per le pipeline.\n")
            f.write("Terza e ultima riga.\n")
        print(f"CreateInputFile completata: {self.output().path} creato.")

# --- Task 2: Processare il file di input ---
class ProcessFile(luigi.Task):
    """
    Questa Task legge il file creato da CreateInputFile,
    conta le righe e scrive il risultato in un nuovo file.
    """
    # Parametro per specificare dove salvare l'output
    output_filename = luigi.Parameter(default='data/output.txt')

    def requires(self):
        """
        Definisce le dipendenze di questa Task.
        Questa Task richiede che CreateInputFile sia completata.
        Restituisce un'istanza (o una lista/dizionario di istanze) delle Task richieste.
        """
        print("ProcessFile verifica le dipendenze...")
        # Richiede l'esecuzione della Task CreateInputFile con i parametri di default
        return CreateInputFile()

    def output(self):
        """
        Definisce il file di output di questa Task.
        """
        # Assicurati che la directory 'data' esista
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
        return luigi.LocalTarget(self.output_filename)

    def run(self):
        """
        Logica di processamento: legge l'input, conta le righe, scrive l'output.
        """
        print(f"Esecuzione di ProcessFile: lettura da {self.input().path}...")
        time.sleep(3) # Simula lavoro di processamento

        line_count = 0
        # self.input() restituisce l'output() della Task definita in requires()
        with self.input().open('r') as infile:
            for line in infile:
                print(f"  Letta riga: {line.strip()}")
                line_count += 1

        print(f"ProcessFile: scrittura risultato su {self.output().path}...")
        # self.output() restituisce il target definito nell'output() di questa Task
        with self.output().open('w') as outfile:
            outfile.write(f"Il file di input contiene {line_count} righe.\n")

        print(f"ProcessFile completata: {self.output().path} creato.")

# --- Esecuzione della Pipeline ---
if __name__ == '__main__':
    """
    Questo blocco permette di eseguire la pipeline direttamente da riga di comando.
    Specifichiamo la Task finale che vogliamo eseguire (ProcessFile).
    Luigi risolverà automaticamente le dipendenze (CreateInputFile).
    `local_scheduler=True` usa uno scheduler locale semplice, senza bisogno
    di avviare un demone `luigid` separato. È utile per test e semplici script.
    """
    print("Avvio della pipeline Luigi...")
    luigi.build([ProcessFile()], local_scheduler=True)
    print("Pipeline Luigi completata.")
