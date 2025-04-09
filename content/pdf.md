---
title: pdf
description: Stands for Portable Document Format
---

## Tools
### `wkhtmltopdf`
Can be used to convert html to pdf. Can be used a single binary, run in a docker container.
Is uses a rather old webkit engine, which means newer css syntax won't get rendered. 
For example, I had problems when using tailwindcss.

There is also a Golang-Library which utilizes the binary to create pdfs:
```golang
import(
    wkhtml "github.com/SebastiaanKlippert/go-wkhtmltopdf"
)
```
### Gotenberg
Can be used to convert html into pdf. Runs within a docker container and is accessable via an API. I don't have much experience with it, but I looks promising.
### ocrmypdf
Can be used to apply Optical Character Recogntion (OCR) to pdfs. It is written in python uses tesseract in backend.
Because of several dependancys I recommend to use the a docker image.
```bash
docker run --rm -i jbarlow83/ocrmypdf-alpine
```
