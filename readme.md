# To start a Gateway Node
# * represents TCP port, ranges from [1,3,4,5,6] 
# & represents UDP port, ranges from [1,2,3,4,5]
python ServerStart.py g 2000* 2900&

# To start a Member Node
# * represents TCP port, ranges from [1,3,4,5,6] 
# & represents UDP port, ranges from [1,2,3,4,5]
python ServerStart.py 2000* 2900&

