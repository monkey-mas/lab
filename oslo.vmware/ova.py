import contextlib
import io
import tarfile
import urllib2

class OVA(object):

    def get_ovf_and_root_vmdk(self, ova):
        """Return OVF and root VMDK files

        Currently assuming path and format of OVA file is valid
        e.g) no missing fields
		
        :param ova: file path of OVA file
        """
        def offset_to_next_file(filesize, blocksize):
            offset = filesize % blocksize
            if offset != 0:
                offset = blocksize - (filesize % blocksize)
            return offset

        blocksize = tarfile.BLOCKSIZE
        chunksize = blocksize * 2 * 2048 # 2M bytes 
        ret_data = {'ovf': None, 'vmdk': None}

        with contextlib.closing(urllib2.urlopen(ova)) as ovafile:
            found_ovf = False
            found_root_vmdk = False

            while not (found_ovf and found_root_vmdk):
                header = ovafile.read(blocksize)
                info = tarfile.TarInfo.frombuf(header)
                filesize = info.size

                if info.name.endswith(('ovf', 'vmdk')):
                    s = io.BytesIO()

                    while filesize > chunksize:
                        buf = ovafile.read(chunksize)
                        s.write(buf)
                        filesize -= chunksize
                    buf = ovafile.read(filesize)
                    s.write(buf)

                    if info.name.endswith(('ovf')):
                        ret_data['ovf'] = s.getvalue()
                        found_ovf = True
                    if info.name.endswith(('vmdk')):
                        ret_data['vmdk'] = s.getvalue()
                        found_root_vmdk = True
                else:
                    while filesize > chunksize:
                        ovafile.read(chunksize)
                        filesize -= chunksize
                    ovafile.read(filesize)

                offset = offset_to_next_file(filesize, blocksize)
                ovafile.read(offset)

        return ret_data