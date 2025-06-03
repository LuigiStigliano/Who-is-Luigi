import luigi
import sys

# Per permettere a Luigi di scoprire le task definite in altri moduli
# quando si specificano da riga di comando, potremmo aver bisogno di importarle
# o assicurarci che siano nel percorso di Python.
# Gli import espliciti sono più sicuri.

from src.tasks.base_tasks import CreateInputFile, ProcessFile
from src.tasks.parallel_tasks import CreateParallelFileA, CreateParallelFileB, ProcessParallelFiles
from src.tasks.failure_example import FailingTask, DependsOnFailingTask
from src.tasks.csv_tasks import CreateSampleCSV, ProcessCSVFile
from src.tasks.wrapper_tasks import RunAllExamples

# Luigi può scoprire le task se sono importate nel namespace globale
# dello script che viene eseguito, oppure se sono specificate con il loro percorso completo
# (es. src.tasks.base_tasks.ProcessFile) quando si usa luigi.build programmaticamente
# o da riga di comando se il PYTHONPATH è configurato correttamente.

if __name__ == '__main__':
    """
    Questo blocco permette di eseguire la pipeline direttamente da riga di comando.
    Luigi gestisce il parsing degli argomenti della riga di comando per determinare
    quale task eseguire e con quali parametri.
    """
    print("Avvio della pipeline Luigi...")

    # Se non viene specificata nessuna task dalla CLI, Luigi eseguirà le task
    # passate all'array di luigi.build().
    # Se viene specificata una task dalla CLI (es. python src/pipeline.py ProcessFile --local-scheduler),
    # Luigi eseguirà quella specifica task.
    # `luigi.run()` è un'alternativa a `luigi.build()` che usa il parsing degli argomenti CLI
    # per determinare le task da eseguire, rendendo l'array esplicito qui meno necessario
    # se si fa affidamento completo sulla CLI.
    # Tuttavia, `luigi.build([RunAllExamples()], ...)` fornisce un buon default.

    # Lista di tutte le task radice che potrebbero essere eseguite.
    # Luigi selezionerà quelle specificate dalla CLI. Se nessuna è specificata,
    # e non si usa un WrapperTask come default in build(), potrebbe non fare nulla
    # o dare errore a seconda della versione/configurazione di Luigi.
    # Fornire un default come RunAllExamples è una buona pratica.
    tasks_to_build = [RunAllExamples()]


    # Questo permette a Luigi di prendere il controllo e processare gli argomenti da CLI.
    # Se da CLI viene fornito un nome di task (es. ProcessFile), luigi.build
    # ignorerà il `tasks_to_build` fornito qui e userà quello da CLI.
    # Se nessun nome di task viene fornito da CLI, userà `tasks_to_build`.
    luigi.build(tasks_to_build, local_scheduler=True) #

    print("Pipeline Luigi completata (o almeno, quelle task che non sono fallite).")
