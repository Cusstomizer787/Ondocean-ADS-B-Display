"""Script pour exporter toutes les trajectoires vers Grafana"""
import sys
sys.path.insert(0, r'c:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL')

from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import export_sample_data_csv

if __name__ == "__main__":
    export_sample_data_csv()
