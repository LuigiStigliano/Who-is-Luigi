import luigi
# Importa le task specifiche di cui questo wrapper ha bisogno
from .base_tasks import ProcessFile
from .parallel_tasks import ProcessParallelFiles
from .csv_tasks import ProcessCSVFile
# Non importiamo le task di fallimento qui per non includere RunAllExamples nel fallimento di default

class RunAllExamples(luigi.WrapperTask):
    """
    WrapperTask per eseguire tutte le principali pipeline di esempio.
    Le WrapperTask non hanno un output() proprio, servono solo a raggruppare dipendenze.
    """
    def requires(self):
        return [
            ProcessFile(),
            ProcessParallelFiles(),
            ProcessCSVFile()
        ]