import argparse

from LogTailer import LogTailer
from ConsoleParser import ConsoleParser
from ConsoleParserConfigReader import ConsoleParserConfigReader

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', default='../resources/csgo-parser.conf', help='The path to the CSGO console.log output location.')
    return parser.parse_args()

def run(config):
    tailer = LogTailer(config.log_location+'\console.log')
    
    text_file = open(config.log_location+'\console.log', "w")
    text_file.write('')
    text_file.close()
    
    tailer.start()
    console_parser = ConsoleParser(tailer,config.log_location)
    console_parser.listen()

if __name__ == '__main__':
    args = init_parser()

    print '[+] Initializing CSGO Console Parser'
    config = ConsoleParserConfigReader(args.config)

    print '[+] Config Loaded: Starting Stream'
    run(config)
