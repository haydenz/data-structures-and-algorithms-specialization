# python3
import sys


###############################################
############ Method I: BWMatching #############
###############################################

def LastToFirst(bwt):
  """
  return a dict s.t. given a symbol at position i in LastColumn (key), it gives
  a val of its position in FirstColumn
  """
  sorted_bwt = sorted([(b, i) for i, b in enumerate(bwt)])

  res = dict()
  for i in range(len(bwt)):
    res.update({sorted_bwt[i]: i})
  
  del sorted_bwt
  return res

def BWMatching(pattern, bwt, last_to_first):
  top, bottom = 0, len(bwt) - 1
  while top <= bottom:
    if len(pattern) > 0:
      symbol = pattern[-1]
      pattern = pattern[:-1]
      if symbol in bwt[top:bottom+1]:
        first_pos = bwt[top:bottom+1].index(symbol)
        last_pos = len(bwt[top:bottom+1]) - list(reversed(bwt[top:bottom+1])).index(symbol) - 1
        top, bottom = last_to_first[(bwt[first_pos+top], first_pos+top)], last_to_first[(bwt[last_pos+top], last_pos+top)]
      else:
        return 0
    else:
      return bottom - top + 1

###############################################
######### Method II: BetterBWMatching #########
###############################################

# def PreprocessBWT(bwt):
#   """
#   Preprocess the Burrows-Wheeler Transform bwt of some text
#   and compute as a result:
#     * starts - for each character C in bwt, starts[C] is the first position 
#         of this character in the sorted array of 
#         all characters of the text.
#     * occ_count_before - for each character C in bwt and each position P in bwt,
#         occ_count_before[C][P] is the number of occurrences of character C in bwt
#         from position 0 to position P inclusive.
#   """
#   # Implement this function yourself
#   sorted_bwt = sorted([b for b in bwt])
#   unq_bwt = list(set(bwt))
#   starts, occ_counts_before = dict(), dict()
#   for unq in unq_bwt:
#     starts.update({unq: sorted_bwt.index(unq)})
#     occ_counts_before.update({unq: [0]})
#     for i, t in enumerate(bwt): 
#       occ_counts_before[unq].append(bwt[0:i+1].count(unq))
#   del sorted_bwt
#   return starts, occ_counts_before

def PreprocessBWT(bwt):
  """
  Preprocess the Burrows-Wheeler Transform bwt of some text
  and compute as a result:
    * starts - for each character C in bwt, starts[C] is the first position 
        of this character in the sorted array of 
        all characters of the text.
    * occ_count_before - for each character C in bwt and each position P in bwt,
        occ_count_before[C][P] is the number of occurrences of character C in bwt
        from position 0 to position P inclusive.
  """
  # Implement this function yourself
  starts = {}
  occ_counts_before = {}
  chars = set(bwt)
  first_col = sorted(list(bwt))
  for c in chars:
    starts[c] = first_col.index(c)
  #print (starts)
  for i in range(len(bwt)+1):
    if i == 0:
      for c in chars:
        occ_counts_before[c] = [0]
    else:
      for c in chars:
        '''if not c in occ_counts_before:
          if bwt[i] == c:
            occ_counts_before[c] = [1]
          else:
            occ_counts_before[c] = [0]'''
        #else:
        if bwt[i-1] == c:
          occ_counts_before[c].append(occ_counts_before[c][-1] + 1)
        else:
          occ_counts_before[c].append(occ_counts_before[c][-1])
  #print (occ_counts_before)
  return starts, occ_counts_before

def CountOccurrences(pattern, bwt, starts, occ_counts_before):
  """
  Compute the number of occurrences of string pattern in the text
  given only Burrows-Wheeler Transform bwt of the text and additional
  information we get from the preprocessing stage - starts and occ_counts_before.
  """
  # Implement this function yourself
  starts, occ_counts_before = PreprocessBWT(bwt)

  top, bottom = 0, len(bwt) - 1
  while top <= bottom:
    if len(pattern) > 0:
      symbol = pattern[-1]
      pattern = pattern[:-1]

      if symbol in bwt[top:bottom+1]:
        top = starts[symbol] + occ_counts_before[symbol][top] 
        bottom = starts[symbol] + occ_counts_before[symbol][bottom+1]-1
      else:
        return 0
    else:
      return bottom - top + 1


if __name__ == '__main__':
  bwt = sys.stdin.readline().strip()
  pattern_count = int(sys.stdin.readline().strip())
  patterns = sys.stdin.readline().strip().split()
  # Preprocess the BWT once to get starts and occ_count_before.
  # For each pattern, we will then use these precomputed values and
  # spend only O(|pattern|) to find all occurrences of the pattern
  # in the text instead of O(|pattern| + |text|).  


  starts, occ_counts_before = PreprocessBWT(bwt)
  # last_to_first = LastToFirst(bwt)
  res = []
  for p in patterns:
    # Method II
    res.append(CountOccurrences(p, bwt, starts, occ_counts_before))
    # Method I
    # res.append(BWMatching(p, bwt, last_to_first))
  print(' '.join(map(str, res)))
