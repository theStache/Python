# PDFSummerizer v20190725
# Created by Tyler Williams (and alot of help from Google)
# Questions/comments/concerns/optimization ideas email me - tjwill86@gmail.com
# CYA statement - Use at own risk, make backups of original documents before use incase of a catastrophic failure
import nltk, argparse, heapq, PyPDF2, re, sys, pikepdf, sumy, os
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer


# nltk.download('punkt')

############FUNCTIONS##################
# Reads in a PDF and turns it into a text file for parsing#
def parsePDF(nfile):
    pdfFileObj = open(nfile, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    rename = re.sub(".pdf", "_text.txt", nfile)
    f = open(rename, "a")
    if args.fpage:
        print("Starting page: {}" " Ending page: {}".format(args.fpage, args.lpage))
        for x in range(args.fpage - 1, args.lpage):
            text = pdfReader.getPage(x).extractText()
            text1 = re.sub("\\n", "", text)
            text1 = text1.encode("ascii", errors="ignore")
            f.write(str(text1))
        f.close()
        pdfFileObj.close()
        print("Saved output as : " + str(rename))

    else:
        for x in range(0, pdfReader.numPages):
            text = pdfReader.getPage(x).extractText()
            text1 = re.sub("\\n", "", text)
            text1 = text1.encode("ascii", errors="ignore")
            f.write(str(text1))
        f.close()
        pdfFileObj.close()

    print("Saved output as :" + rename)
    return rename


##############TEXT PARSING FUNCTIONS###################
def luhn(nfile):
    document1 = open(nfile, "r")
    document = document1.read()
    parser = PlaintextParser.from_file(nfile, Tokenizer("english"))
    f = open(str(nfile).replace("_pike_text.txt", "_luhn.txt"), "a")
    summarizer_luhn = LuhnSummarizer()
    summary_1 = summarizer_luhn(parser.document, 4)
    for sentence in summary_1:
        f.write(str(sentence))
    f.close()
    print(str(nfile).replace("_pike_text.txt", "_lsa.txt"))


def lex(nfile):
    document1 = open(nfile, "r")
    document = document1.read()
    parser = PlaintextParser.from_file(nfile, Tokenizer("english"))
    f = open(str(nfile).replace("_pike_text.txt", "_lex.txt"), "a")
    summarizer_lex = LexRankSummarizer()
    summary_1 = summarizer_lex(parser.document, 4)
    for sentence in summary_1:
        f.write(str(sentence))
    f.close()
    print(str(nfile).replace("_pike_text.txt", "_lex.txt"))


def lsa(nfile):
    document1 = open(nfile, "r")
    document = document1.read()
    parser = PlaintextParser.from_file(nfile, Tokenizer("english"))
    f = open(str(nfile).replace("_pike_text.txt", "_lsa.txt"), "a")
    summarizer_lsa = LsaSummarizer()
    summary_1 = summarizer_lsa(parser.document, 4)
    for sentence in summary_1:
        f.write(str(sentence))
    f.close()
    print(str(nfile).replace("_pike_text.txt", "_lsa.txt"))


def nltksum(nfile):
    f = open(str(nfile).replace("_pike_text.txt", "_nltk.txt"), "a")
    input_file1 = open(nfile, "r", encoding="utf-8")
    input_file = input_file1.read()
    input_file = re.sub(r"\[[0-9]*\]", " ", input_file)
    input_file = re.sub(r"\s+", " ", input_file)
    formatted_input_file = re.sub("[^a-zA-Z]", " ", input_file)
    formatted_input_file = re.sub(r"\s+", " ", formatted_input_file)
    sentence_list = nltk.sent_tokenize(input_file)
    stopwords = nltk.corpus.stopwords.words("english")

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_input_file):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequncy

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    summary = " ".join(summary_sentences)
    f.write(summary)
    f.close()
    input_file1.close()
    print(str(nfile).replace("_pike_text.txt", "_nltk.txt"))


#####CMD LINE PARSER####
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="Input file")
parser.add_argument("--fpage", "-fp", help="First page", type=int)
parser.add_argument("--lpage", "-lp", help="Last page", type=int)
parser.add_argument(
    "--all", "-a", help="Run all parsers against file/s", action="store_true"
)
parser.add_argument("--luhn", "-lu", help="Run Luhn algorithm against file/s")
parser.add_argument("--lex", "-lx", help="Run LexRank algorithm against file/s")
parser.add_argument("--lsa", "-ls", help="Run LSA algorithm against file/s")
parser.add_argument("--nltk", "-nl", help="Run NLTK algorithm against file/s")
parser.add_argument("--dir", "-d", help="Run against this directory")
parser.add_argument("--usage", "-u", help="Usage Guide", action="store_true")
args = parser.parse_args()

if args.usage:
    print(
        "Usage Guide: script.py --input filename.pdf --fpage # --lpage # --all( or --luhn/--lex/--lsa/--nltk) \nIf you want to run the script against a directory containing multiple PDFs use --dir and not --input\n\
    If you dont put a --fpage/--lpage it will start from the beggining and go until the end of the file.\n\
        LexRank, LSA, Luhn, NLTK are differnt Text summarizing alrgorithms, use --all to run them all against the file for best results.\n\
    This script will provide alot of output: parsed pdf, text of pdf, parsed text files from each algorithm."
    )

elif args.dir:
    for x in os.listdir():
        if "pdf" in x:
            newfile = x
            print(newfile)
            pdf = pikepdf.open(newfile)
            pdf.save(str(newfile).replace(".pdf", "_pike.pdf"))
            pdf.close()
            new = parsePDF(str(newfile).replace(".pdf", "_pike.pdf"))
            print(new)
            lex(new)
            luhn(new)
            nltksum(new)
            lsa(new)

elif args.input:
    newfile = args.input
    print(newfile)
    pdf = pikepdf.open(newfile)
    pdf.save(str(newfile).replace(".pdf", "_pike.pdf"))
    pdf.close()
    new = parsePDF(str(newfile).replace(".pdf", "_pike.pdf"))
    print(new)
    if args.all:
        lex(new)
        luhn(new)
        nltksum(new)
        lsa(new)
    elif args.lex:
        lex(new)
    elif args.luhn:
        luhn(new)
    elif args.lsa:
        lsa(new)
    else:
        print("Need to pass an algorithm")

else:
    print("Please provide a PDF input file")
