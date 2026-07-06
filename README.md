# Inventory Management System

A Flask‑based REST API for managing product inventory, featuring integration with the OpenFoodFacts public API to enrich product data via barcode or name lookup. Includes a command‑line interface (CLI) for easy interaction and a full unit test suite.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [GET /inventory](#get-inventory)
  - [GET /inventory/<id>](#get-inventoryid)
  - [POST /inventory](#post-inventory)
  - [PATCH /inventory/<id>](#patch-inventoryid)
  - [DELETE /inventory/<id>](#delete-inventoryid)
  - [GET /external/search](#get-externalsearch)
- [CLI Tool Usage](#cli-tool-usage)
  - [Interactive Menu](#interactive-menu)
  - [Available Options](#available-options)
- [Testing](#testing)
- [Debugging & Validation](#debugging--validation)
- [Notes & Limitations](#notes--limitations)
- [Future Enhancements](#future-enhancements)

---

## Features

- **Full CRUD operations** – Create, Read, Update, Delete inventory items.
- **External API enrichment** – Automatically fetch product details (name, brand, ingredients) from OpenFoodFacts when adding or updating an item with a barcode.
- **CLI interface** – Interact with the API without writing HTTP requests manually.
- **In‑memory data store** – Simple mock database (resets on server restart) for quick prototyping.
- **Unit tested** – Comprehensive tests for endpoints, CLI commands, and external API calls using `pytest` and `unittest.mock`.
- **RESTful design** – Follows standard HTTP methods and status codes.

---

## Project Structure
