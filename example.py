from rfid import RFID

NAME_BLOCK = 4
PRICE_BLOCK = 12
rdr = RFID()

# input a string return a list of number(ascii code)
def str_to_ascii(tar):
  ascii = []
  for t in tar:
    ascii.append(ord(t))
  ascii.append(3)
  return ascii

# input a list of number(ascii code) return a string
def ascii_to_str(tar):
  string = ''
  for t in tar:
    if t == 3:
      return string
    string = string + chr(t)

# input a string and write to rfid tag
def write_to_rfif(target, block):
  target = str_to_ascii(target)
  count = 0
  while len(target) > 0:
    if len(target) > 16:
      temp = target[:16]
      rdr.write(block+count, temp)
      # print('write', block+count, temp)
      target = target[16:]
      count = count + 1
    else:
      n = 16-len(target)
      zero = [0 for i in range(n)]
      target = target + zero
      rdr.write(block+count, target)
      # print('write', block+count, target)
      target = []

# input block number output a string
def read_from_rfid(block):
  result = []
  while True:
    data = rdr.read(block)
    print(data)
    result = result + data[1]
    if 3 in data[1]:
      break
    else:
      block = block +1
  result = ascii_to_str(result)
  return result
  


while True:
  print('Please type mode:')
  mode = input()
  
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      if not rdr.select_tag(uid):
        if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
          if mode == 'r':
            print("Reading: " + read_from_rfid(NAME_BLOCK))
            # Always stop crypto1 when done working
            rdr.stop_crypto()
          else:
            write_to_rfif('1221', NAME_BLOCK)
            rdr.stop_crypto()

# Calls GPIO cleanup
rdr.cleanup()