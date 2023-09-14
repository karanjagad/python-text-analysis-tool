# Python Text Analysis Tool README

This Python script is designed to analyze text data and provide various readability and linguistic metrics. It can process text from a URL, a file, or directly from a text string. The script uses libraries such as Beautiful Soup 4 for web scraping, spaCy for natural language processing, and pandas for data manipulation. 

## How to Use

1.  **Install Required Libraries**: Ensure you have the necessary Python libraries installed, including spaCy, Beautiful Soup, pandas, and enchant.
    
2.  **Save the Script**: Save the provided script to a Python file, for example, `text_analysis_tool.py`.

3. **Install the spacy package**: `python -m spacy download en_core_web_sm` 
    
4.  **Run the Script**: Open a command line or terminal and execute the script, providing three arguments:
    
    -   **Language**: Specify the language (e.g., "en" for English, "de" for German).
        
    -   **Source**: Choose the source type, which can be one of the following: "url" (for a web page), "file" (for a local text file), or "text" (for direct input).
        
    -   **URL, File Path, or Text**: Depending on the source type selected, provide the corresponding input:
        
        -   For "url": Provide the URL of the web page you want to analyze.
        -   For "file": Specify the file path to the local text file you want to analyze.
        -   For "text": Enter the text content directly as a string.
    
    Example usage in a command line or terminal:


    - To get result of a web page which is in english
      `python main.py en url https://someurlover2#xhere/`
    - To get result of a text which is in english
      `python main.py en file sample.txt`
      (sample.txt file contains the text needs to be scored)
    - To get result of a text which is in english
      `python main.py en text python main.py de text "Hallo, wie geht's dir"`
    
5.  **Analyze Text**: The script will execute various analyses on the provided text data, including readability metrics and identification of potential spam words.
    
5.  **Readability Grade**: You will receive information about the readability grade level of the text, helping you understand the content's difficulty.
The Code gives result as a grade as in who can read the text and also gives additional details to know more about the text
Refrence Grade Table
|Score|Age|Grade Level|
|--- |--- |--- |
|1|5-6|Kindergarten|
|2|6-7|First/Second Grade|
|3|7-9|Third Grade|
|4|9-10|Fourth Grade|
|5|10-11|Fifth Grade|
|6|11-12|Sixth Grade|
|7|12-13|Seventh Grade|
|8|13-14|Eighth Grade|
|9|14-15|Ninth Grade|
|10|15-16|Tenth Grade|
|11|16-17|Eleventh Grade|
|12|17-18|Twelfth grade|
|13|18-24|College student|
|14|24+|Professor|
    

The Python Text Analysis Tool provides valuable insights into the complexity and readability of text data. It can be a useful tool for content creators, educators, and writers.