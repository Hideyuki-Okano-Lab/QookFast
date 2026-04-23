import sys

try:
    import jinja2_time
except ImportError:
    print("\n" + "!" * 60)
    print(" [ERROR] 'jinja2-time' is not installed!")
    print("   QookFast template requires the 'jinja2-time' extension.")
    print("   Please install it before running Cookiecutter:")
    print("\n   pip install jinja2-time\n")
    print("   Then, try running Cookiecutter again.")
    print("!" * 60 + "\n")

    sys.exit(1)
