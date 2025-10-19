"""Script pour exporter les trajectoires de décollage vers Grafana"""
import sys
sys.path.insert(0, r'c:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL')

from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import export_takeoffs_csv

if __name__ == "__main__":
    export_takeoffs_csv()
