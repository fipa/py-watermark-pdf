install:
	pip install -r requirements --target .

create_folders:
	mkdir imgs
	mkdir -p pdfs/generated
	mkdir fonts

delete_generated:
	rm pdfs/generated/*.pdf