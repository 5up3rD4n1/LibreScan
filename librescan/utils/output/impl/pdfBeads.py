import subprocess
from librescan.utils.output.outputMaker import OutputMaker
from librescan.config import config


class PDFBeads(OutputMaker):

    def make(self, p_path, p_output_name):
        input_path = p_path + "/processed/"
        output_path = p_path + "/" + p_output_name
        print(input_path)
        command = 'cd {0} && pdfbeads *.tif > {1}.pdf'.format(input_path, output_path)
        subprocess.call(command, shell=True)

    @staticmethod
    def get():
        file = open(f'{config.project_folder}/{config.output_name}.pdf', 'rb')
        print(file)
        return file
