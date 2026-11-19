
<div align="center">

# Kerja Scraper

> Automated Job Scraper, NLP Extractor, Data Warehouse, and Interactive Analytics Dashboard

[Live Demo](https://jobmarketintel.streamlit.app/) · [Documentation](./docs/) · [Report Bug](https://github.com/mhdhamka/kerja-scraper/issues) · [Request Feature](https://github.com/mhdhamka/kerja-scraper/issues)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plasmo](https://img.shields.io/badge/Plasmo-Extension-000000?style=for-the-badge&logo=plasmo&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-Database-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Scrapy](https://img.shields.io/badge/Scrapy-Web%20Scraping-121212?style=for-the-badge&logo=scrapy&logoColor=white)

</div>

---

# Overview

An end-to-end data pipeline and intelligence platform designed to scrape, process, analyze, and serve live job market data. Built with a modular architecture, the system automates web harvesting across platforms (such as MYFutureJobs, LinkedIn, and RemoteOK), performs natural language processing (NLP) and regex extraction for skills and salaries, stores structured analytics in a lightning-fast local data warehouse, and exposes insights via a FastAPI backend and a Streamlit dashboard.

---

## Key Features

* **Browser Extension Tracker:** A Plasmo-powered extension injected into JobStreet and MYFutureJobs to capture and sync job applications directly with a single click. 
* **Multi-Platform Scrapers:** Automated Scrapy spiders targeting portal listings like MYFutureJobs, LinkedIn, and RemoteOK.
* **Smart Information Extraction:** NLP and regex cleaning pipelines to parse unstructured job descriptions into structured skill sets, salary ranges, and metadata.
* **Embedded Analytics Warehouse:** Powered by DuckDB for high-performance analytical queries without requiring heavy database server infrastructure.
* **RESTful API Service:** Built with FastAPI to serve job market data, metrics, and search queries with high performance and automatic documentation.
* **Interactive Dashboard:** A Streamlit-powered user interface to visualize job trends, salary distributions, and in-demand skills.

---

# Contributing

Contributions are always welcome! If you'd like to improve this project, please follow these steps:

* Fork the Repository
* Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
* Commit your Changes (`git commit -m "add: some amazing feature"`)
* Push to the Branch (`git push origin feature/AmazingFeature`)
* Open a Pull Request

---

If you found this project interesting, consider giving it a star!

Made with ❤️ by mdhamka
