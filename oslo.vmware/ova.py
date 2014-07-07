import contextlib
import io
import tarfile
import urllib2

TAR_BLOCK_SIZE = tarfile.BLOCKSIZE # 512 bytes

class API(object):

    def get_ovf_and_root_vmdk(self, ova):
        """Return OVF and root VMDK files

        Currently assuming path and format of OVA file is valid
        e.g) no missing fields
		
        :param ova: file path of OVA file
        """

        def offset_to_next_file(file_size):
            """Return the number of bytes to the next file in a tar archive

            Each file in a tar archive is splitted into block-size blocks,
            and each of them is followed by binary zeros at the end to fill
            the rest of the block.
            If file size is the multiple of block size, there is a block-size
            block filled with binary zeros at the end of the file. If so,
            thus the return value is the block size not 0.

            :param file_size: file size in bytes
            """
            offset = file_size % TAR_BLOCK_SIZE
            if offset != 0:
                offset = TAR_BLOCK_SIZE - (file_size % TAR_BLOCK_SIZE)
            return offset

        chunk_size = TAR_BLOCK_SIZE * 2 * 2048 # 2 Mib if block size is 512 B
        ret_data = {'ovf': None, 'vmdk': None}

        with contextlib.closing(urllib2.urlopen(ova)) as ovafile:
            found_ovf = False
            found_root_vmdk = False

            while not (found_ovf and found_root_vmdk):
                # We keep reading OVA until we find both OVF and VMDK
                # assuming that the first VMDK file found is the root.
                # We need to do this as a tar archive is not indexed.
                # Every time we read a file, header file, which is one
                # block-size block, is read to extract file size and format.
                # chunksize is passed to read(...) so that the following
                # operations do not block instead of waitng for a whole OVA
                # to be downloaded. Also, chuncksize might not be really big,
                # , e.g. 2^31 bytes,
                # runtime error could occur otherwise.(as socket.py might not
                # be able to handle it each time read(...) is called)
                #
                # TODO: implement me to avoid any possible errors
                header = ovafile.read(TAR_BLOCK_SIZE)
                info = tarfile.TarInfo.frombuf(header)
                file_size = info.size
                file_format = info.name.split('.')[-1]

                if file_format in ('ovf', 'vmdk'):
                    file_obj = io.BytesIO()

                    while file_size > chunk_size:
                        buf = ovafile.read(chunk_size)
                        file_obj.write(buf)
                        file_size -= chunk_size
                    buf = ovafile.read(file_size)
                    file_obj.write(buf)

                    ret_data[file_format] = file_obj.getvalue()

                    if file_format == 'ovf':
                        found_ovf = True
                    if file_format == 'vmdk':
                        found_root_vmdk = True
                else:
                    while file_size > chunk_size:
                        ovafile.read(chunk_size)
                        file_size -= chunk_size
                    ovafile.read(file_size)

                offset = offset_to_next_file(file_size)
                ovafile.read(offset)

        return ret_data