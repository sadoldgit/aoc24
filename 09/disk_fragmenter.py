import sys

class Chunk:
    "continuous array of blocks, either a file or a free space"

    FREE_ID = sys.maxsize

    def __init__(self, blocks, fileid, chunkid=0, partid=0):
       self.blocks  = blocks
       self.fileid  = fileid
       self.chunkid = chunkid # added for 2nd part
       self.partid  = partid
       
    @property
    def is_file(self):
        return self.fileid != Chunk.FREE_ID

    @property
    def is_free(self):
        return self.fileid == Chunk.FREE_ID

    def __repr__(self):
        if self.fileid == Chunk.FREE_ID:
            return f'{self.blocks}|FREE|{self.chunkid}|{self.partid}'
        else:
            return f'{self.blocks}|{self.fileid}|{self.chunkid}|{self.partid}'


class DiskDefagmenter:
    
    def __init__(self, orig_disk_map):
        self.disk_map = list(self._parse(orig_disk_map.rstrip()))
        self.size_file_blocks = sum(map(lambda ch: ch.blocks,
                                   filter(lambda ch: ch.is_file, self.disk_map)))        
        self.size_free_blocks = sum(map(lambda ch: ch.blocks,
                                   filter(lambda ch: ch.is_free, self.disk_map)))

    def _parse(self, disk_map):
        for i in range(len(disk_map)):
            if i % 2 == 0:
                yield Chunk(int(disk_map[i]), (i//2), i)
            else:
                yield Chunk(int(disk_map[i]), Chunk.FREE_ID, i)

    def __repr__(self):
        return str(self.disk_map)

    def _backward_file_chunks(self):
        for chunk in reversed(self.disk_map):
            if chunk.is_file:
                yield chunk

    def do_defrag(self):
        backfiles = self._backward_file_chunks()
        next_file = next(backfiles)
        # the idea with the iterators might somewhat complicated loop-end
        # detection with this counters of remaining blocks
        defrag_file, defrag_free = self.size_file_blocks, self.size_free_blocks
        for chunk in self.disk_map:
            if defrag_file <= 0 or defrag_free <= 0:
                return
            if chunk.is_file:
                if chunk.blocks < defrag_file:
                    yield chunk
                else: # remaining splitted file
                    chunk.blocks = defrag_file
                    yield chunk
                defrag_file -= chunk.blocks
            else: # free space          
                free_blocks = chunk.blocks
                while defrag_file > 0 and free_blocks > 0:
                    if next_file.blocks > free_blocks:
                        # split file
                        yield Chunk(free_blocks, next_file.fileid)
                        defrag_file -= free_blocks
                        next_file = Chunk(next_file.blocks - free_blocks,
                                          next_file.fileid)
                        free_blocks = 0
                    else:
                        yield next_file
                        defrag_file -= next_file.blocks
                        free_blocks -= next_file.blocks
                        next_file = next(backfiles)
                defrag_free -= free_blocks


    def _first_free(self, fchunk):
        # massive overhead, always sorting
        for chunk in self.disk_map:
            if chunk.is_free and chunk.blocks >= fchunk.blocks and chunk.chunkid < fchunk.chunkid:
                return chunk
        else:
            return None

        
    def do_defrag2(self):
        free_pool = []
        for file_ch in self._backward_file_chunks():
            free_ch = self._first_free(file_ch)
            if free_ch is None:
                continue
            if free_ch.chunkid > file_ch.chunkid:
                break
            # free space to the previous file place
            free_pool.append(Chunk(file_ch.blocks, Chunk.FREE_ID, file_ch.chunkid))
            free_ch.blocks -= file_ch.blocks
            file_ch.chunkid = free_ch.chunkid
            file_ch.partid  = free_ch.partid
            free_ch.partid += 1 # for later sorting
            
        for chunk in sorted(self.disk_map + free_pool, key=lambda ch: ch.chunkid*100000 + ch.partid):
            if chunk.blocks > 0:
                yield chunk


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        disk_map = f.read()
    ddefrag = DiskDefagmenter(disk_map)
    i, checksum = 0, 0
    for fchunk in ddefrag.do_defrag():
        for j in range(i, i+fchunk.blocks):
            checksum += j * fchunk.fileid
        i = j + 1
    print(f'Part 1: checksum of defragmented files {checksum}')
    
    ddefrag = DiskDefagmenter(disk_map)
    i, checksum = 0, 0
    for chunk in ddefrag.do_defrag2():
        if chunk.is_free and chunk.blocks > 0:
            i += chunk.blocks
        else:
            for j in range(i, i+chunk.blocks):
                checksum += j * chunk.fileid
            i = j + 1
    print(f'Part 2: checksum of defragmented files, method 2: {checksum}')