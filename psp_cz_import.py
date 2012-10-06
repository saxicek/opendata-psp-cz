from importer.psp_cz import import_all
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="data_dir",
                      help="directory with psp.cz export files")

    (options, args) = parser.parse_args()
    if not options.data_dir:
        parser.error("Parameter --dir must be specified!")

    import_all(options.data_dir)

if __name__ == '__main__':
    main()