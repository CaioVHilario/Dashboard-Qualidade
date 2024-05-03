import sys
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "Home.py"]
sys.exit(stcli.main())
