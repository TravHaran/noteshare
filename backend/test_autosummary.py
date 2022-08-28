from PyPDF2 import PdfReader, PdfFileReader
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re

# file with unstrucutred text: "/Users/trav/Desktop/noteshare/backend/files/4aae9db7-a8ca-43bc-a62f-60bbc726c27d.pdf"
# file with structured text: "/Users/trav/Desktop/noteshare/backend/files/5c5c1409-d95b-4fb6-b495-0f761eef6f68.pdf"
# /Users/trav/Desktop/noteshare/backend/files/2103.13630.pdf
# file without text: "/Users/trav/Desktop/noteshare/backend/files/1ed90971-ce69-4285-bcff-cf3726cf33b7.pdf"
pdf = PdfReader("/Users/trav/Desktop/noteshare/backend/files/5c5c1409-d95b-4fb6-b495-0f761eef6f68.pdf")

text = ''
for page in pdf.pages:
    text += page.extractText()

#print(text)

# autosummarizer 
# models: distilbart-xsum-12-1
# Token indices sequence length is longer than the specified maximum sequence length for this model (1052 > 1024). Running this sequence through the model will result in indexing errors
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

# tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

# model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-xsum")
summarizer = pipeline(task='summarization', model=model, tokenizer=tokenizer)

def chunkify(text):
    # split text into sentences
    processed_text = text.replace('\n', '')
    result = re.split("(?<=[.!?])\s+", processed_text)
    return result

sentences = chunkify(text)

max_chunk = 500
current_chunk = 0
chunks = []

for sentence in sentences:
    if len(chunks) == current_chunk + 1: # check if current chunk exists
        if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk: 
            chunks[current_chunk].extend(sentence.split(' '))   
        else:
            current_chunk += 1
            chunks.append(sentence.split(' '))
    else:
        chunks.append(sentence.split(' '))

for chunk_id in range(len(chunks)):
    chunks[chunk_id] = ' '.join(chunks[chunk_id])

res = summarizer(chunks, max_length=130, min_length=30, do_sample=False)

summary = ' '.join([sum['summary_text'] for sum in res])
print(summary)



