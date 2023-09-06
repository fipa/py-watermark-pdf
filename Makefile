install:
	pip install -r requirements

generate:
	python3 create_pdf.py $(output) $(text)

create_folders:
	mkdir imgs
	mkdir -p pdfs/generated

delete_generated:
	rm pdfs/generated/*.pdf