# STR Chimerism Analysis Automation

A lightweight web application built with Python and Streamlit to automate donor chimerism percentage calculations from Short Tandem Repeat (STR) capillary electrophoresis data.

> **Live App:** https://kimerizm-test-paneli.streamlit.app/

## Why I Built This

During my internship at a clinical genetics diagnostic laboratory, I noticed that post-transplant chimerism calculations were performed manually using peak area (integral) values from capillary electrophoresis (**3500 Genetic Analyzer**). Doing this across multiple STR loci for every patient was repetitive, time-consuming, and open to simple arithmetic mistakes. 

I built this tool to automate those calculations, speed up the routine workflow, and eliminate manual calculation errors.

## What It Does

*   **Automated Calculations:** Computes donor and recipient chimerism percentages directly from STR peak area inputs.
*   **Multiple Allele Formulas:** Handles different informative allele configurations automatically.
*   **Batch Loci Processing:** Evaluates multiple loci at once and calculates the overall mean donor chimerism percentage.
*   **Lab-Ready UI:** Simple browser interface designed for daily laboratory use without needing any coding knowledge.

## Validation

The tool was tested with real laboratory STR datasets during my internship and showed 100% concordance with the standard manual calculations.
