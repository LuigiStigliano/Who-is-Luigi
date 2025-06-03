import luigi
import time
import os
from src.utils import ensure_dir

class CreateParallelFileA(luigi.Task):
    output_dir = luigi.Parameter(default='data/parallel_example')

    def output(self):
        path = os.path.join(self.output_dir, "fileA.txt")
        ensure_dir(path)
        return luigi.LocalTarget(path)

    def run(self):
        print(f"Esecuzione di CreateParallelFileA: creazione di {self.output().path}...")
        time.sleep(1)
        with self.output().open('w') as f:
            f.write("Contenuto del file A parallelo generato da Luigi.\n")
        print(f"CreateParallelFileA completata.")

class CreateParallelFileB(luigi.Task):
    output_dir = luigi.Parameter(default='data/parallel_example')

    def output(self):
        path = os.path.join(self.output_dir, "fileB.txt")
        ensure_dir(path)
        return luigi.LocalTarget(path)

    def run(self):
        print(f"Esecuzione di CreateParallelFileB: creazione di {self.output().path}...")
        time.sleep(1)
        with self.output().open('w') as f:
            f.write("Contenuto del file B parallelo generato da Luigi.\n")
        print(f"CreateParallelFileB completata.")

class ProcessParallelFiles(luigi.Task):
    """Task che dipende da due task che possono essere eseguite in parallelo."""
    output_file = luigi.Parameter(default='data/parallel_summary.txt')
    parallel_files_dir = luigi.Parameter(default='data/parallel_example')

    def requires(self):
        print("ProcessParallelFiles verifica le dipendenze...")
        return {
            "fileA": CreateParallelFileA(output_dir=self.parallel_files_dir),
            "fileB": CreateParallelFileB(output_dir=self.parallel_files_dir)
        }

    def output(self):
        ensure_dir(self.output_file)
        return luigi.LocalTarget(self.output_file)

    def run(self):
        print(f"Esecuzione di ProcessParallelFiles...")
        summary = "Sommario dei file paralleli:\n"
        with self.input()["fileA"].open('r') as f_a:
            summary += f"Da fileA.txt: {f_a.read().strip()}\n"
        with self.input()["fileB"].open('r') as f_b:
            summary += f"Da fileB.txt: {f_b.read().strip()}\n"

        with self.output().open('w') as out_f:
            out_f.write(summary)
        print(f"ProcessParallelFiles completata: {self.output().path} creato.")