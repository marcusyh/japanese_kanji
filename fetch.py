import os
import sys
import shutil

def get_sync_flist(src_dir, synclist):
    syncflist = {
            "match": [],
            "missing": []
            }
    tmplist = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            fpath = os.path.join(root, f)
            if os.path.isfile(fpath):
                tmplist.append(fpath)

    for f in synclist:
         fpath = os.path.join(src_dir, f)

         if not os.path.isfile(fpath):
             fpaths = []
             for f in tmplist:
                 if f.find(filing) >=0:
                     fpaths.append(f)
             if len(fpaths) == 1:
                 fpath = fpaths[0]
             else:
                 print('\n'.join([f for f in fpaths]))

         if fpath:
             syncflist[
             continue

         self._sync_missing.append(f)


 
class FileSyncAgent():
    def __init__(self, source, destnation, synclist):
        self._src_dir = source
        self._dst_dir = destnation

        self._src_flist = self.__get_src_flist()

        self._synclist = synclist

        self._sync_file_list = []
        self._sync_missing = []
    
    # Source files list, storing them for search purpose to simulate find command.
   
    # generate sync file list before really sync.
    def __create_sync_flist(self, location, synclist):
        for f in synclist:
            fpath = os.path.join(location, f)

            if not os.path.isfile(fpath):
                fpaths = []
                for f in self._src_flist:
                    if f.find(filing) >=0:
                        fpaths.append(f)
                if len(fpaths) == 1:
                    fpath = fpaths[0]
                else:
                    print('\n'.join([f for f in fpaths]))

            if fpath:
                self._sync_file_list.append(fpath)
                continue

            self._sync_missing.append(f)

    def __sync_one_file(self, fpath):
        dirname = os.path.join(self._dst_dir, os.path.dirname(fpath))
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        shutil.copy2(fpath, dirname)

    def synclist(self):
        self.__create_sync_flist(

    def __get_file_path(root, location, filing):
        fpath = os.path.join(root, location, '01_VB／Excel', filing)
        if not os.path.isfile(fpath):
            fpath
            import os, fnmatch
             
             inDIR = '/home/dan/'
             pattern = '*kea'
             fileList = []


def get_sync_list(syncfile):
    synclist = []
    h = open(syncfile, 'r')
    for l in h.readlines():
        f = fpath.strip().replace('#', '/').replace('\\', '/')
        synclist.append(f)
    h.close()


def sync_file(source, destination, syncfile):
    source1 = os.path.join(source, '01_本部', '01_VB／Excel')
    source2 = os.path.join(source, '02_店舗', '01_VB／Excel')
    synclist = get_sync_list(syncfile)

    fsa2 = FileSyncAgent(source2, destination, synclist)    
    finishlist2, missinglist = fsa2.syncfile()

    fsa1 = FileSyncAgent(source1, destination, missinglist)    
    finishlist1, missinglist = fsa1.syncfile()

    return finishlist2 + finishlist1, missinglist


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('3 parameters needed.')
        sys.exit(0)
    finish, missing = syncfile(argv[1], argv[2], argv[3])
    print('%s files copied successufully, %s files missing. The missing files list here:' %(len(finish), len(missing)))
    for f in missing:
        print('\t%s' %f)


