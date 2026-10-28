@echo off
setlocal enabledelayedexpansion
title Retail Sales Analysis Dashboard - Pipeline Runner
color 0B

echo ==============================================================================
echo                 RETAIL SALES ANALYSIS DASHBOARD
echo        End-to-End Analytics Pipeline (Python, SQL, Power BI)
echo ==============================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not found in your system PATH.
    echo Please install Python 3.10+ or check your environment variables.
    echo.
    pause
    exit /b 1
)

:menu
echo Select an option to execute:
echo   [1] Run Full Pipeline (Generate, Clean, SQL DB, Analytics, Tests)
echo   [2] Clean Data and Generate Data Quality Report
echo   [3] Run SQL Database Queries (SQLite)
echo   [4] Run Sales Analytics, Charts and Business Report
echo   [5] Run Automated Unit Tests (Pytest)
echo   [6] Launch Interactive Web Dashboard (Streamlit)
echo   [7] Exit
echo.
set /p choice="Enter your choice (1-7) [Default is 1]: "

if "%choice%"=="" set choice=1
if "%choice%"=="1" goto full_pipeline
if "%choice%"=="2" goto clean_data
if "%choice%"=="3" goto run_sql
if "%choice%"=="4" goto analyze_sales
if "%choice%"=="5" goto run_tests
if "%choice%"=="6" goto launch_web
if "%choice%"=="7" goto end

echo Invalid option selected. Please choose between 1 and 7.
echo.
goto menu

:full_pipeline
cls
echo ==============================================================================
echo STEP 1/5: Generating Raw Synthetic Sales Transactions...
echo ==============================================================================
python src\generate_data.py
if %errorlevel% neq 0 goto error_exit
echo.

echo ==============================================================================
echo STEP 2/5: Running Data Cleaning Pipeline and Quality Audit...
echo ==============================================================================
python src\clean_data.py
if %errorlevel% neq 0 goto error_exit
echo.

echo ==============================================================================
echo STEP 3/5: Ingesting Data into SQLite Database and Running SQL Queries...
echo ==============================================================================
python src\load_database.py
if %errorlevel% neq 0 goto error_exit
echo.
python src\run_sql_queries.py
if %errorlevel% neq 0 goto error_exit
echo.

echo ==============================================================================
echo STEP 4/5: Running Python Analytics, Generating Charts & Business Report...
echo ==============================================================================
python src\analyze_sales.py
if %errorlevel% neq 0 goto error_exit
echo.

echo ==============================================================================
echo STEP 5/5: Running 17 Automated Unit Tests (Pytest)...
echo ==============================================================================
python -m pytest tests\ -v
if %errorlevel% neq 0 goto error_exit
echo.

color 0A
echo ==============================================================================
echo [SUCCESS] Full Analytics Pipeline Completed Successfully!
echo ==============================================================================
echo - Cleaned CSV:      data\processed\retail_sales_cleaned.csv
echo - Cleaned Excel:    data\processed\retail_sales_cleaned.xlsx
echo - SQLite Database:  data\retail_sales.db
echo - Quality Report:   reports\data_quality_report.md
echo - Business Report:  reports\sales_analysis_report.md
echo - Visual Charts:    reports\figures\
echo.
set /p launch_st="Would you like to launch the interactive web dashboard now? (Y/N): "
if /i "%launch_st%"=="Y" goto launch_web
goto end

:clean_data
cls
python src\clean_data.py
pause
goto menu

:run_sql
cls
python src\load_database.py
python src\run_sql_queries.py
pause
goto menu

:analyze_sales
cls
python src\analyze_sales.py
pause
goto menu

:run_tests
cls
python -m pytest tests\ -v
pause
goto menu

:launch_web
cls
echo ==============================================================================
echo Launching Supplementary Streamlit Web Dashboard...
echo Press Ctrl + C in this terminal window to stop the web server.
echo ==============================================================================
streamlit run app.py
goto end

:error_exit
color 0C
echo.
echo [ERROR] An error occurred while executing the pipeline.
pause
exit /b 1

:end
echo.
echo Thank you for using Retail Sales Analysis Dashboard!
pause
exit /b 0
