import sys
import urllib2
import tarfile
import hashlib

# URLs and SHA384 of files we need
deps = [('http://zlib.net/zlib-1.2.8.tar.gz',
         'a4d316c404ff54ca545ea71a27af7dbc29817088'),
        ('https://www.openssl.org/source/openssl-1.0.1i.tar.gz',
         '74eed314fa2c93006df8d26cd9fc630a101abd76')]

def fetch_and_extract_deps():
    for dep in deps:
        print "Fetching and extracting %s" % dep[0]
        saved_file = fetch_file(dep[0], dep[1])
        extract_tgz(saved_file)

def fetch_file(url, trusted_digest, debug=2, insecure=False):
    url_obj = urllib2.urlopen(url)
    fileobj = urllib2.StringIO(url_obj.read())

    fetched_digest = hashlib.new('sha1', fileobj.read())
    fileobj.reset()

    if fetched_digest.hexdigest() != trusted_digest:
        if debug > 0: print >>sys.stderr, "WARNING: File checksum for %s did not match, file may be tampered with or corrupt!" % url
        if insecure:
            return fileobj
        else:
            raise TypeError( "Aborting to to failed file checksum.")
    else:
        if debug > 1: print >>sys.stderr, "File checksum for %s matched" %url
        return fileobj

def extract_tgz(fileobj, dest_path='./', debug=0):
    if fileobj:
        try:
            tgz = tarfile.open(fileobj=fileobj)
            tgz.extractall()
        except Exception as ex:
            raise
        finally:
            fileobj.close()

    else:
        if debug > 0: print >>sys.stderr, "No file object provided for extraction."