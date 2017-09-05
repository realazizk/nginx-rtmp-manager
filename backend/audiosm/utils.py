import io
from audiosm.compat import string_types
import os
import sys
from contextlib import contextmanager


ALLOWED_EXTENSIONS = set(['mp3', 'mp4', 'aac', 'opus', 'mkv', 'webm'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class MyBuffer(io.BytesIO):
    def save(self, dst, buffer_size=16384):
        """Save the file to a destination path or file object.  If the
        destination is a file object you have to close it yourself after the
        call.  The buffer size is the number of bytes held in memory during
        the copy process.  It defaults to 16KB.
        For secure file saving also have a look at :func:`secure_filename`.
        :param dst: a filename or open file object the uploaded file
                    is saved to.
        :param buffer_size: the size of the buffer.  This works the same as
                            the `length` parameter of
                            :func:`shutil.copyfileobj`.
        """
        from shutil import copyfileobj
        close_dst = False
        if isinstance(dst, string_types):
            dst = open(dst, 'wb')
            close_dst = True
        try:
            copyfileobj(self, dst, buffer_size)
        finally:
            if close_dst:
                dst.close()


@contextmanager
def silence_stdout():
    """
    Suppresses output
    """
    new_target = open(os.devnull, "w")
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target
