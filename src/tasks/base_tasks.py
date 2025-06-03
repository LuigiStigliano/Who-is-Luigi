import luigi
import time
from src.utils import ensure_dir

class CreateInputFile(luigi.Task):
    """
    Questa Task crea un semplice file di testo che servirà da input
    per la task successiva.
    """
    filename = luigi.Parameter(default='data/input.txt')

    def output(self):
        ensure_dir(self.filename)
        return luigi.LocalTarget(self.filename)

    def run(self):
        print(f"Esecuzione di CreateInputFile: creazione di {self.output().path}...")
        time.sleep(2) # Simula un po' di lavoro
        with self.output().open('w') as f:
            f.write("Questa è la prima riga.\n")
            f.write("Luigi è utile per le pipeline.\n")
            f.write("Terza e ultima riga.\n")
        print(f"CreateInputFile completata: {self.output().path} creato.")

class ProcessFile(luigi.Task):
    """
    Questa Task legge il file creato da CreateInputFile,
    conta le righe e scrive il risultato in un nuovo file.
    """
    output_filename = luigi.Parameter(default='data/output.txt')
    input_file_param = luigi.Parameter(default='data/input.txt')

    def requires(self):
        print("ProcessFile verifica le dipendenze...")
        return CreateInputFile(filename=self.input_file_param)

    def output(self):
        ensure_dir(self.output_filename)
        return luigi.LocalTarget(self.output_filename)

    def run(self):
        print(f"Esecuzione di ProcessFile: lettura da {self.input().path}...")
        time.sleep(3) # Simula lavoro di processamento

        line_count = 0
        with self.input().open('r') as infile:
            for line in infile:
                print(f"  Letta riga: {line.strip()}")
                line_count += 1

        print(f"ProcessFile: scrittura risultato su {self.output().path}...")
        with self.output().open('w') as outfile:
            outfile.write(f"Il file di input '{self.input().path}' contiene {line_count} righe.\n")
        print(f"ProcessFile completata: {self.output().path} creato.")