import luigi
import time
from src.utils import ensure_dir

class FailingTask(luigi.Task):
    """Questa task è progettata per fallire."""
    output_file = luigi.Parameter(default='data/failing_task_output.txt')

    def output(self):
        ensure_dir(self.output_file)
        return luigi.LocalTarget(self.output_file)

    def run(self):
        print(f"Esecuzione di FailingTask: questa task fallirà intenzionalmente.")
        time.sleep(1)
        raise ValueError("Errore intenzionale: questa task è destinata a fallire!")

class DependsOnFailingTask(luigi.Task):
    """Questa task dipende da una task che fallisce."""
    output_file = luigi.Parameter(default='data/dependent_on_fail_output.txt')

    def requires(self):
        print("DependsOnFailingTask verifica le dipendenze (FailingTask)...")
        return FailingTask()

    def output(self):
        ensure_dir(self.output_file)
        return luigi.LocalTarget(self.output_file)

    def run(self):
        print(f"Esecuzione di DependsOnFailingTask...")
        input_content = "Nessun input ricevuto a causa del fallimento della dipendenza."
        try:
            with self.input().open('r') as infile: # Questo fallirà se l'input non esiste
                input_content = infile.read()
        except Exception as e:
            print(f"Errore nell'aprire l'input per DependsOnFailingTask (atteso se la dipendenza è fallita): {e}")

        with self.output().open('w') as outfile:
            outfile.write(f"Contenuto basato su FailingTask: {input_content}\n")
        print(f"DependsOnFailingTask completata (questo messaggio indica che la logica di fallimento potrebbe non essere come atteso).")