import logging
from contextlib import closing
from urllib.request import urlopen
from urllib.error import ContentTooShortError


logger = logging.getLogger(__name__)


def download(url, filename):
    logger.info("Downloading %s into %s" % (url, filename))
    with closing(urlopen(url)) as fp:
        headers = fp.info()
        tfp = open(filename, 'wb')
        with tfp:
            result = filename, headers
            bs = 1024*8*100
            size = -1
            read = 0
            blocknum = 0
            if 'content-length' in headers:
                size = int(headers['Content-Length'])

            while True:
                block = fp.read(bs)
                if not block:
                    break
                read += len(block)
                tfp.write(block)
                blocknum += 1

                logger.info("Downloaded {}/{}".format(
                    format_filesize(read),
                    format_filesize(size)))

    if size >= 0 and read < size:
        raise ContentTooShortError(
            "retrieval incomplete: got only %i out of %i bytes"
            % (read, size), result)

    return result


def format_filesize(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
