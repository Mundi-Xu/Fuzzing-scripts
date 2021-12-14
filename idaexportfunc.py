from os import name
import idc
import idautils
import ida_entry
import ida_funcs
import idaapi
import ida_typeinf


def funcFormat(fstr):
    fstr = fstr.replace("const ", "")
    fstr.strip()
    return fstr

# int __cdecl(int, int)
# BOOL __stdcall(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
# GDALRasterBlock *__thiscall(GDALRasterBlock *__hidden this, struct GDALRasterBand *, int, int)


# parse_type = re.compile('([^\s]+)\s+([^\(]+)\((.*)\)$')
parse_type = re.compile(
    '(.*)(__thiscall|__fastcall|__cdecl|__systemcall|__stdcall|__usercall)\((.*)\)$')

# parse_type2 = re.compile("/*([^*]+)$")


output_dir = os.path.dirname(ida_nalt.get_input_file_path())
outfile_name = '{}.exportfunc.drltrace.txt'.format(
    os.path.basename(ida_nalt.get_input_file_path())
)

buf = ""

for i in range(ida_entry.get_entry_qty()):
    entry_ordinal = ida_entry.get_entry_ordinal(i)
    entry_ordinal_vaddr = ida_entry.get_entry(entry_ordinal)
    func_name = ida_funcs.get_func_name(entry_ordinal_vaddr)
    func_tinfo_t = idaapi.tinfo_t()
    ida_typeinf.guess_tinfo(func_tinfo_t, entry_ordinal_vaddr)
    if not func_tinfo_t or not func_name:
        print("error:", hex(entry_ordinal_vaddr))
        continue

    func_type = idaapi.print_tinfo(
        '', 0, 0, idaapi.PRTYPE_NOARGS | idaapi.PRTYPE_1LINE, func_tinfo_t, '', '')
    if not func_type:
        print("error:", hex(entry_ordinal_vaddr))
        continue
    print(func_type)

    rslt = parse_type.match(func_type)
    if rslt is not None:
        args_type_list = []
        rt_type, call_type, args_type = rslt.groups()

        if not args_type:
            buf += '#' + func_name + ': ' + func_type + '\n'
            continue
        elif "," in args_type:
            args_type_list = [i.strip() for i in args_type.split(",")]
        else:
            args_type_list = [args_type.strip()]

        buf += rt_type + '|' + func_name

        for a_arg_type in args_type_list:
            a_arg_type = funcFormat(a_arg_type)
            buf += '|'
            buf += a_arg_type
        buf += '\n'
        print(rt_type, call_type, args_type_list)
    else:
        buf += '#' + func_name + ': ' + func_type + '\n'

try:
    with open(os.path.join(output_dir, outfile_name), "w") as f:
        f.write(buf)
    print("成功输出到: {}".format(os.path.join(output_dir, outfile_name)))
except Exception as e:
    print("输出文件失败：{}".format(e))
