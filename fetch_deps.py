import os
import sys
import urllib2
import tarfile
import hashlib

# URLs and SHA384 of files we need
deps = [('http://zlib.net/zlib-1.2.8.tar.gz',
         'a4d316c404ff54ca545ea71a27af7dbc29817088'),
        ('https://www.openssl.org/source/openssl-1.0.2a.tar.gz',
         '46ecd325b8e587fa491f6bb02ad4a9fb9f382f5f')]

def basename_tar(_filename):
    return os.path.basename(_filename).rsplit('.',2)[0]

def fetch_and_extract_deps():
    for url,sha1 in deps:
        basename = basename_tar(url)
        if os.path.exists(basename):
            print "Won't fetch, already exists: {}".format(url)
        else:
            print "Fetching and extracting %s" % basename
            saved_file = fetch_file(url, sha1)
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