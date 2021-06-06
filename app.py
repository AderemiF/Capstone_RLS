import torch
import streamlit as st
from transformers import pipeline
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import os 
import base64

summarizer = pipeline("summarization")

#Setting background image
main_bg = "./images/background.png"
main_bg_ext = "png"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)




st.markdown(' # **Research Literature Summarizer (RLS)**')
st.image('./images/papers.png')
# expander = st.sidebar.beta_expander('Want to try it out?')
# expander.markdown('[click here for demo](https://ded-detector.uc.r.appspot.com)')



expander = st.sidebar.beta_expander('Meet the developer')
expander.image('./images/Aderemi_net_9760.jpg')
expander.write('Aderemi Fayoyiwa')
expander.markdown('[Email](https://mail.google.com/mail/u/0/?fs=1&to=aderemifayoyiwa@gmail.com&su=SUBJECT&body=BODY&tf=cm)   [GitHub](https://github.com/AderemiF)   [Linkedin](https://www.linkedin.com/in/aderemi-fayoyiwa)')

 
# left_column, right_column = st.beta_columns(2)
# pressed = left_column.button('RLS - summarizer')
#if pressed:
#	left_column.image('images\retina.jpg')
    #left_column.write('Welcome on board!')

st.markdown('# Introduction')
st.markdown(' ### Whether there would be a scientific publication or not, most research projects begin with literature review.')
st.markdown(' ##### \nAs the name implies, literature review involves going through related published research papers to see what has already been established in the research area. \nLiterature review answers some research questions and in some cases raises more research questions. \nsResearchers also use literature review to validate/corroborate their research findings.')
st.markdown(' ##### \nResearchers spend significant amount of time reviewing published research papers that are related to their current project or potential research publication. \nAbout half of the research papers reviewed end up not being relevant to the project or publication at hand. \nDepending on how we look at it, but it can be said that half of that time is wasted. \nIf the time lost was be somewhat saved, it can be put into more productive use, say expanding the scope of research or invested in writing research reports or paper.')


st.markdown(' # Problem Statement')
st.markdown('##### \n * A significant percentage of the total research time goes into literature review. \n * Often times, over half of these literatures do not contain any useful information pertaining to the research at hand.')

st.markdown('# Goal')
st.markdown(' ##### \nThe goal of this project is: \n * To create an application that can effectively summarize research papers. \n * To significantly reduce the amount of time researchers spend on literature review. \n * To summarize research papers in a way that keeps vital information intact.')

st.markdown('# Target')
st.markdown(' ##### \nThe target audience of the RLS are: \n * Researchers \n * University students \n * High school students')


st.markdown('# Summarizer')
expander = st.beta_expander('Model')
expander.write("NLP transformer: Huggingface's pretrained transformer")
expander.write('pipeline: summarization')


expander = st.beta_expander('Technologies Used')
expander.write('Python')
expander.write('Github/Git')
expander.write('Jupyter')
expander.write('Streamlit')
expander.write('Streamlitshare')


expander = st.beta_expander('What next?')
expander.write('Further optimization of the summarizer')
expander.write('Commercialize RLS')


st.markdown('# Try it out')
st.write('Summarize your research papers') 
st.markdown(" * Upload your pdf file and you will get 2 txt files in your downloads \n * The first is 'file.txt', a txt version of your pdf file \n * The second is 'summary.txt', the summarized version of your pdf file")

st.markdown("#### Upload your pdf file below, it takes about 8 minutes to summarize")
file = st.file_uploader(label = 'RLS', type=['pdf']) 

#Converting pdf to txt
if file is not None:
    # st.write('File successfully uploaded')
    st.markdown("#### File successfully uploaded")
    st.markdown("#### Why don't you get a cup of coffee while your paper is being converted and summarized...")

    def pdf2txt(inPDFfile, outTXTFile):
                inFile = open(inPDFfile, 'rb')
                resMgr = PDFResourceManager()
                retData = io.StringIO()
                TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
                interpreter = PDFPageInterpreter(resMgr, TxtConverter)
            
                #Process each page in pdf file
                for page in PDFPage.get_pages(inFile):
                    interpreter.process_page(page)
                    
                txt = retData.getvalue()
                
                #save output data to a txt file
                return txt

    inPDFfile = file.name  
    outTXTFile = 'file.txt'

    try:
        txt = pdf2txt(inPDFfile, outTXTFile)
        with open(outTXTFile, 'w') as f:
            f.write(txt)
    except Exception as e:
            print(e)

    st.markdown("#### File conversion completed, summarization is ongoing...")
    st.markdown("#### How about that cup of coffee?")

    #Summarization
    #This is to make text readable after splitting
    def preprocessing(txt): 
        #Combining the test into one long string
        #ARTICLE = ' '.join(text)
        ARTICLE = txt.replace('.', '.<eos>')
        ARTICLE = ARTICLE.replace('!', '!<eos>')
        ARTICLE = ARTICLE.replace('?', '?<eos>')

        #Splitting ARTICLE into individual sentences using <eos>
        sentences = ARTICLE.split('<eos>')
        return sentences 

    with open('file.txt') as f:
        text = f.readlines() 

    #Combining the test into one long string
    ARTICLE = ' '.join(text)

    sentences = preprocessing(ARTICLE)

    #Dividing the text (sentences) into smaller chunks to allow all the text be passed in using small chunks
    max_chunk = 300
    current_chunk = 0
    chunks = []

    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    to_summarize = chunks[0:15]

    #Joining individual words together again to form sentences
    for chunk_id in range(len(to_summarize)):
        to_summarize[chunk_id] = ' '.join(to_summarize[chunk_id])

    #Passing the chunks to be summarized
    result = summarizer(to_summarize, max_length=150, min_length=30, do_sample=False)

    #Extracting the summary text and joining all chunk summaries in result together.
    #text = ' '.join([summ['summary_text'] for summ in result])

    #Saving summary into a txt file
    with open ('summary.txt', 'w') as f:
        #f.write(text)

        #text = ' '.join([summ['summary_text'] for summ in result])

        for v in result:
            f.write(v['summary_text'])
            f.write('\n')

    #Notice after summarization is complete
    st.markdown("#### Summarization complete!")
    st.markdown("#### Check your downloads for 'summary.txt' ")
