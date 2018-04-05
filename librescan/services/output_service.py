from librescan.patterns import Singleton
from threading import Thread
from librescan.utils.output.impl.pdfBeads import PDFBeads
from librescan.utils.output.outputPreparer import OutputPreparer
from librescan.config import config


class OutputService(metaclass=Singleton):

    def __init__(self, p_output_name="out"):
        self.working_dir = None
        self.output_name = p_output_name
        self.output_preparer = OutputPreparer()
        self.output_makers = [PDFBeads()]  # OutputMaker
        self.generators = []

    def generate(self):
        self.working_dir = config.project_folder
        self.output_preparer.run(self.working_dir)
        for output_maker in self.output_makers:
            t = Thread(target=output_maker.make, args=(self.working_dir, self.output_name))
            t.setDaemon(True)
            self.generators.append(t)
            t.start()

    def wait_process(self):
        for g in self.generators:
            g.join()
