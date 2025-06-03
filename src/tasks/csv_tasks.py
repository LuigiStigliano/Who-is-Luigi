import luigi
import time
import csv
from src.utils import ensure_dir

class CreateSampleCSV(luigi.Task):
    """Crea un file CSV di esempio."""
    output_file = luigi.Parameter(default='data/sample_data.csv')

    def output(self):
        ensure_dir(self.output_file)
        return luigi.LocalTarget(self.output_file)

    def run(self):
        print(f"Esecuzione di CreateSampleCSV: creazione di {self.output().path}...")
        headers = ['id', 'nome_prodotto', 'quantita', 'prezzo_unitario']
        data = [
            {'id': 'P001', 'nome_prodotto': 'Mela', 'quantita': 50, 'prezzo_unitario': 0.30},
            {'id': 'P002', 'nome_prodotto': 'Banana', 'quantita': 100, 'prezzo_unitario': 0.20},
            {'id': 'P003', 'nome_prodotto': 'Arancia', 'quantita': 75, 'prezzo_unitario': 0.25},
            {'id': 'P004', 'nome_prodotto': 'Latte', 'quantita': 30, 'prezzo_unitario': 1.10}
        ]
        time.sleep(1)
        with self.output().open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"CreateSampleCSV completata: {self.output().path} creato.")

class ProcessCSVFile(luigi.Task):
    """Elabora il file CSV per calcolare statistiche semplici."""
    input_csv_file = luigi.Parameter(default='data/sample_data.csv')
    output_summary_file = luigi.Parameter(default='data/csv_summary_report.txt')

    def requires(self):
        print("ProcessCSVFile verifica le dipendenze...")
        return CreateSampleCSV(output_file=self.input_csv_file)

    def output(self):
        ensure_dir(self.output_summary_file)
        return luigi.LocalTarget(self.output_summary_file)

    def run(self):
        print(f"Esecuzione di ProcessCSVFile: lettura da {self.input().path}...")
        total_value = 0
        num_products = 0
        product_details = []

        with self.input().open('r', newline='') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                try:
                    quantita = int(row['quantita'])
                    prezzo = float(row['prezzo_unitario'])
                    valore_riga = quantita * prezzo
                    total_value += valore_riga
                    num_products += 1
                    product_details.append(f"  - {row['nome_prodotto']}: {quantita} x ${prezzo:.2f} = ${valore_riga:.2f}")
                    print(f"  Letta riga CSV: {row['nome_prodotto']}, Valore: {valore_riga:.2f}")
                except ValueError as e:
                    print(f"  Riga saltata a causa di un errore di valore: {row} ({e})")
                    continue

        time.sleep(2) # Simula elaborazione
        print(f"ProcessCSVFile: scrittura risultato su {self.output().path}...")
        with self.output().open('w') as outfile:
            outfile.write(f"Report di Elaborazione del File CSV: {self.input().path}\n")
            outfile.write("--------------------------------------------------\n")
            outfile.write(f"Numero totale di prodotti distinti: {num_products}\n")
            outfile.write(f"Valore totale magazzino: ${total_value:.2f}\n\n")
            outfile.write("Dettaglio prodotti:\n")
            for detail in product_details:
                outfile.write(f"{detail}\n")
        print(f"ProcessCSVFile completata: {self.output().path} creato.")