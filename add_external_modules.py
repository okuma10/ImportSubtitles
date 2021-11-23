import subprocess,site,sys
def add_external_modules():
    add_path = site.USER_SITE

    if add_path not in sys.path:
        sys.path.append(add_path)

    bpyexe = sys.executable

    try:
        subprocess.call([bpyexe,"-m","ensurepip"])
    except:
        pass

    try:
        import pysubs2
    except:
        subprocess.check_call([bpyexe, "-m", "pip", "install", "pysubs2"])
        import pysubs2

def remove_external_modules():
    add_path = site.USER_SITE

    if add_path not in sys.path:
        sys.path.append(add_path)

    bpyexe = sys.executable

    try:
        subprocess.call([bpyexe, "-m", "ensurepip"])
    except:
        pass

    try:
        subprocess.check_call([bpyexe, "-m", "pip", "uninstall", "pysubs2", "-y"])
    except:
        pass