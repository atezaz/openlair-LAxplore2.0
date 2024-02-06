
import pdfplumber
import re


class PdfFile:
	"""Class that represents the PDF-files that is searched for the various lables."""
	
	def __init__(self, pdf_file,single_collumn = False, content = ""):
		self.pdf_file = pdf_file
		self.content = content
		self.single_collumn = single_collumn
		

	def extract(self):
		"""Function to extract the text from the PDF file. After determining if the 
		text is two or single collumn it extracts the content of the PDF 
		and saves it as string. The text is shortened a bit by removing the
		references and made lower case so that lables can also be found if
		they are written in upper case inside the original text"""
		
		Pdftext = "" 
		with pdfplumber.open(self.pdf_file) as pdf:
			pdf_length = (len(pdf.pages))
			# checks if the PDF is single collumn. Uses for that the second page except the PDF has only one page
			if pdf_length >=2:
				self.single_collumn = bool(pdf.pages[1].extract_table(dict(vertical_strategy = 'text', text_tolerance = 12)))
			else:
				self.single_collumn = bool(pdf.pages[0].extract_table(dict(vertical_strategy = 'text', text_tolerance = 12)))
			for page in pdf.pages:
				# procedure of extracting if text is two collumn
				if self.single_collumn == False: 
					left_half = page.crop((0, 0, 0.5 * page.width, page.height))
					right_half = page.crop((0.5 * page.width, 0, page.width, page.height))
					page_content = left_half.extract_text(x_tolerance=1) + " " + right_half.extract_text(x_tolerance=1)
					Pdftext += page_content
				# procedure if PDF is single collumn
				else:
					page_content = page.extract_text(x_tolerance=1)
					Pdftext += page_content
		# splitting of the pages with references and removing them
		short_PdfText = re.split("REFERENCES", Pdftext)
		Pdftext = short_PdfText[0]
		# remove hyphens at end of line from text and reconnect the words separated by them
		Pdftext = re.sub(r'- *\n+', "", Pdftext)
		# making the resulting string lower case and saving it as content of the current PdfFile class-object
		self.content = Pdftext.lower()
		return

	

