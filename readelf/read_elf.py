
def print_array(x):
    ret = ""
    for i in x:
        val = '%x'%i
        if len(val)==1:
            val = '0'+val
        ret += val + ' '
    return ret[0:-1]

def elf_class(name, value):
    if name == "EI_CLASS":
        if value == 0:
            return "Class None"
        if value == 1:
            return "Elf32"
        if value == 2:
            return "Elf64"
        else:
            return "Incorrect ("+hex(value)+")"
    if name == "EI_DATA":
        if value == 0:
            return "Data None"
        if value == 1:
            return "Little Endian"
        if value == 2:
            return "Big Endian"
        else:
            return "Incorrect ("+hex(value)+")"
    if name == "EI_VERSION":
        if value == 1:
            return "Current version"
        else:
            return "Incorrect ("+hex(value)+")"
    if name == "EI_OSABI":
        if value == 255:
            return "UNIX System V ABI"
        if value == 0:
            return "UNIX System V ABI"
        if value == 1:
            return "HP-UX ABI"
        if value == 2:
            return "NetBSD ABI"
        if value == 3:
            return "Linux ABI"
        if value == 6:
            return "Solaris ABI"
        if value == 7:
            return "AIX ABI"
        if value == 8:
            return "IRIX ABI"
        if value == 9:
            return "FreeBSD ABI"
        if value == 10:
            return "TRU64 UNIX ABI"
        if value == 11:
            return "Modesto ABI"
        if value == 12:
            return "Open BSD ABI"
        if value == 13:
            return "Open VMS ABI"
        if value == 14:
            return "NSK ABI"
        if value == 15:
            return "Aros ABI"
        if value == 64:
            return "ARM architecture ABI (0x40)"
        if value == 97:
            return "ARM ABI (0x61)"
        else:
            return "Incorrect ("+hex(value)+")"
    if name == "e_type":
        if value == 0:
            return "ET_NONE (No file type)"
        if value == 1:
            return "ET_REL (Relocatable file)"
        if value == 2:
            return "ET_EXEC (Executable file)"
        if value == 3:
            return "ET_DYN (Shared object file)"
        if value == 4:
            return "ET_CORE (Core file)"
        if value == 0xff00:
            return "ET_LOPROC (Processor-specific)"
        if value == 0xffff:
            return "ET_HIPROC (Processor-specific)"
        else:
            return "Incorrect ("+hex(value)+")"
    if name == "e_machine":
        if value == 0:
            return "EM_NONE (No machine)"
        if value == 2:
            return "EM_SPARC (SPARC)"
        if value == 3:
            return "EM_386 (Intel 80386)"
        if value == 18:
            return "EM_SPARC32PLUS (Sun SPARC 32+ )"
        if value == 43:
            return "EM_SPARCV9 (SPARC V9)"
        if value == 62:
            return "EM_X86_64 (AMD x86-64)"
        else:
            return "Incorrect ("+hex(value)+")"
    if name == "e_version":
        if value == 0:
            return "EV_NONE (Invalid version)"
        if value >= 1:
            return "EV_CURRENT (Current version) ("+hex(value)+")"
    return "ERROR\t" + str(name) + "\t" + str(value)

contents = open("a.out", "br").read()



elf64_ehdr = contents[0:63]

e_indent = elf64_ehdr[0:15]
EI_CLASS = e_indent[4]
EI_DATA = e_indent[5]
EI_VERSION = e_indent[6]
EI_OSABI = e_indent[7]
EI_ABIVERSION = e_indent[8]
EI_PAD = e_indent[9:15]

if EI_DATA == 1:
    endianness = "little"
else:
    endianness = "big"

e_type = int.from_bytes(elf64_ehdr[16:17], endianness)
e_machine = int.from_bytes(elf64_ehdr[18:19], endianness)
e_version = int.from_bytes(elf64_ehdr[20:23], endianness)
e_entry = int.from_bytes(elf64_ehdr[24:31], endianness)
e_phoff = int.from_bytes(elf64_ehdr[32:39], endianness)
e_shoff = int.from_bytes(elf64_ehdr[40:47], endianness)
e_flags = int.from_bytes(elf64_ehdr[48:51], endianness)
e_ehsize = int.from_bytes(elf64_ehdr[52:53], endianness)
e_phentsize = int.from_bytes(elf64_ehdr[54:55], endianness)
e_phnum = int.from_bytes(elf64_ehdr[56:57], endianness)
e_shentsize = int.from_bytes(elf64_ehdr[58:59], endianness)
e_shnum = int.from_bytes(elf64_ehdr[60:61], endianness)
e_shstrndx = int.from_bytes(elf64_ehdr[62:63], endianness)



print("ELF Header:")
print("\tMagic:"+print_array(e_indent))
print("\tClass: " + elf_class("EI_CLASS", EI_CLASS))
print("\tData: " + elf_class("EI_DATA", EI_DATA))
print("\tVersion: " + elf_class("EI_VERSION", EI_VERSION))
print("\tABI: " + elf_class("EI_OSABI", EI_OSABI))
print("\tABI Version: " + str(EI_ABIVERSION))
print("\tEI_PAD: " + print_array(EI_PAD))
print("")
print("\tType: " + elf_class("e_type", e_type))
print("\tMachine: " + elf_class("e_machine", e_machine)) #complete with https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html
print("\tVersion: " + elf_class("e_version", e_version))
print("\tEntry point: " + hex(e_entry))
print("\tFlags:", e_shstrndx)
print("\tFlags:", e_flags)
print("\tStart of Program Headers:", e_phoff, "(bytes)")
print("\tStart of Section Headers:", e_shoff, "(bytes)")
print("\tSize of this header:", e_ehsize, "(bytes)")
print("\tProgram Headers:", e_phnum, "entries of size", e_phentsize, "total of", e_phnum*e_phentsize, "bytes")
print("\tSection Headers:", e_shnum, "entries of size", e_shentsize, "total of", e_shnum*e_shentsize, "bytes")
print("\tSection header string table index:", e_shstrndx)