import bpy, sys, subprocess, site

def test_function():
    app_path = site.USER_SITE
    if app_path not in sys.path:
        sys.path.append(app_path)

    pybin = sys.executable  # bpy.app.binary_path_python # Use for 2.83

    try:
        subprocess.call([pybin, "-m", "ensurepip"])
    except ImportError:
        pass

    try:
        import pysubs2
    except ImportError:
        subprocess.check_call([pybin, "-m", "pip", "install", "pysubs2"])
        import pysubs2

