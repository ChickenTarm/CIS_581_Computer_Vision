'''
  File name: carv.py
  Author:
  Date created:
'''

'''
  File clarification:
    Aimed to handle finding seams of minimum energy, and seam removal, the algorithm
    shall tackle resizing images when it may be required to remove more than one seam, 
    sequentially and potentially along different directions.
    
    - INPUT I: n × m × 3 matrix representing the input image.
    - INPUT nr: the numbers of rows to be removed from the image.
    - INPUT nc: the numbers of columns to be removed from the image.
    - OUTPUT Ic: (n − nr) × (m − nc) × 3 matrix representing the carved image.
    - OUTPUT T: (nr + 1) × (nc + 1) matrix representing the transport map.
'''

def carv(I, nr, nc):
  # Your Code Here 
  return Ic, T