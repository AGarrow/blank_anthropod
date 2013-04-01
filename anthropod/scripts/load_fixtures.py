import sys


def main():
    fixture_modules = sys.argv[1:] or ['organization', 'person']

    usage = ('usage: python ./scripts/load_fixtures.py '
             '[fixture_module1[, fixture_modeul2]...]')
    if not fixture_modules:
        print usage

    for fixture_module in fixture_modules:
        mod_fqname = 'anthropod.admin.%s.fixtures' % fixture_module
        mod = __import__(mod_fqname, globals(), locals(), ['object'], -1)
        mod.load()
        print 'loaded fixtures from %r' % mod_fqname


if __name__ == '__main__':
    main()
