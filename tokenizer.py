class Tokenizer:
    def __init__(self):
        self.idx = 256 # start assigning new token ids after the byte range
        self.vocab_size = 512 # limit vocab size to avoid excessive growth
        self.token_copy = []

    def tokenize(self, text):
        token = text.encode('utf-8') # raw bytes
        self.token_copy = list(map(int, token))
        return self.compress_all(self.token_copy)

    def merge(self, ids, pair, idx):
        '''
        in the new list of ids, replace all consecutive occurrences of pair with the new token idx
        '''
        new_ids = []
        i = 0
        while i < len(ids):
            # not at the last index and the current and next ids form the pair. replace it
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                new_ids.append(idx)
                i += 2
            else:
                new_ids.append(ids[i])
                i += 1
        return new_ids
    
    def get_stats(self, byte_array):
        '''
        Find the pair of tokens that appears most frequently in the byte array and replace them with a new token.
        '''
        # k most frequent elements -- i recognize this from leetcode 
        count = {}
        for i in zip(byte_array, byte_array[1:]):
            count[i] = count.get(i, 0) + 1
        return count
        #print(sorted(((v,k) for k, v in count.items()), reverse=True))
        
    def compress_all(self, byte_array):
        '''
        Repeatedly compress the byte array until the most frequent pair is no longer found.
        '''
        vocab_size = self.vocab_size - 256 # number of new tokens we can create
        merges = {}
        for i in range(vocab_size):
            stats = self.get_stats(byte_array)
            pair = max(stats, key=stats.get)
            idx = 256 + i # new token id
            print(f"Merging pair: {pair} with count: {stats[pair]} as new token: {idx}")
            byte_array = self.merge(byte_array, pair, idx)
            merges[pair] = idx

        return byte_array, merges


if __name__ == "__main__":
    token_it = Tokenizer()
    token_it.tokenize(f"You’ll unpack this definition throughout the rest of the tutorial.As you work through the code examples, you’ll see that Python zip operations work just like the physical zipper on a bag or pair of jeans. Interlocking pairs of teeth on both sides of the zipper are pulled together to close an opening. In fact, this visual analogy is perfect for understanding zip(), since the function was named after physical zippers!")
