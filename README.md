# Compliance Gap Detector and Policy Analyzer

## Problem Statement

Organizations need to ensure their internal security policies align with various compliance standards such as NIST, ISO 27001, and others. The goal of this project is to build a system that analyzes key requirements from relevant policy documents and compliance frameworks and compares them with an organization's internal knowledge base. This will allow the identification of compliance gaps or areas where security policies fall short.



### Requirements

- Python 3.x
- Install dependencies using `pip`:
  
```bash
pip install -r requirements.txt
```

## How to Use

### 1. Run the Application

- Start the Streamlit app by running the following command:
``` bash
streamlit run app.py
```

### 2. Upload Documents
- Upload your internal policy documnets as zipped.
- Choose the standard frameworks that you want to check for compliancy.
![UI Dashboard](https://scontent.fktm10-1.fna.fbcdn.net/v/t1.15752-9/494356534_650173867838969_4494052158850278101_n.png?stp=dst-png_s843x403&_nc_cat=103&ccb=1-7&_nc_sid=0024fc&_nc_eui2=AeFK7YQAc_G5VhcR7IWanShvVgNIKgo5JxNWA0gqCjknE-w8bXWDaIkAwNracn9ZAEVAZmOU3PeaPRzTsyCLRgtU&_nc_ohc=mURnofoTwJ0Q7kNvwHA5bhD&_nc_oc=AdnxCKUBlwY1ST5Q1QFJA6GE-1ROWrb4OJ44pLPZY2xKPDCuNXhRXCvyKm6XCXxZBB3KEmk3L8SBeP1qfbe7tVXR&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fktm10-1.fna&oh=03_Q7cD2AFL-PXcB0HBQTioFFLLo6XiaUgN_U8y2IYXjo3F3AomGw&oe=683AC05C)

### 3. Gap Analysis
- The system will automatically analyze and summarize the provided documents, extract key compliance requirements, and compare them with internal knowledge.

- The results will be displayed in the form of a report highlighting the gaps, complete with visualizations through chart.

![Analysis Chart](https://scontent.fktm7-1.fna.fbcdn.net/v/t1.15752-9/494577203_1245065073912920_3218624964001755083_n.png?stp=dst-png_p526x395&_nc_cat=100&ccb=1-7&_nc_sid=0024fc&_nc_eui2=AeHJh3E_uG73B00uykSC-nblqyQhhp-5rJOrJCGGn7msk35ZLTjIQBvl1B0W_JybTu7agv7lWiav5T1wz3lrii7Z&_nc_ohc=d9l914dDqHwQ7kNvwF5VJpZ&_nc_oc=AdkzxyNGM0aJfMp29DTX3SDy8z7ViSW5as2i5mNVI-kjH8n3vrhBrt0PD9HbW_pX6UWYKLmuNsimaKWJSNaGzUGz&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fktm7-1.fna&oh=03_Q7cD2AG4Yvl5ZGWDr8jiNxWijjd71iYey0Im4vZyes2e3GE7ig&oe=683AB9EB)
![Analysis Report](https://scontent.fktm7-1.fna.fbcdn.net/v/t1.15752-9/494574985_1847136959398911_5475147670000810093_n.png?stp=dst-png_s960x960&_nc_cat=111&ccb=1-7&_nc_sid=0024fc&_nc_eui2=AeFoBNhQMeWodSqZowfF-iFe0s8323_w8-bSzzfbf_Dz5uZpKk749UjPhf8p1xVGDqZx9qaT0Ju1GT3iVNr4_LV8&_nc_ohc=LbWcwjrAV3AQ7kNvwG-U_eZ&_nc_oc=Adm8-b-AM2jQr7fTM3UxMCue-gxAGctTbnQrKXDLQUZze5j7Y6mRRt79fyPf8SEo3LObN0I3lkkhfcfkMpYLzp37&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.fktm7-1.fna&oh=03_Q7cD2AFWSqUjXiwoaew_25ymjUe_fLOvS1A4YLwZa-rg0Jf5Ow&oe=683AB669)

## How it Works
![Project Workflow: A brief overview of how this works](https://cdn.discordapp.com/attachments/1366650782153183252/1367356774012817489/flowchart.png?ex=681449bb&is=6812f83b&hm=1a4c99ead165dc9004a1ff29a0ac4cd0362901c34d948639a24e3184e7b48e8f&format=webp&quality=lossless&width=865&height=649)

### Document Parsing:

- The system parses policy and compliance framework documents using custom functions in parse_docs.py. This step ensures that the necessary information is extracted for analysis.

### Summarization and Key Point Extraction:

- We utilize transformer-based models for text summarization and key point extraction. The model will condense lengthy policy and framework documents into concise key requirements.

### Semantic Embedding Generation:

- The system creates semantic embeddings for both the internal policy responses and compliance requirements using models like Sentence-BERT. This allows the system to compare the content effectively and identify any gaps.

### Gap Identification:

- By comparing the embeddings, the system identifies gaps in compliance. If internal responses do not meet the compliance requirements, the system flags it.

### Report Generation:

- A comprehensive report is generated, showing areas where internal policies are lacking or need improvement. This report includes visualizations (e.g., tables, charts) that help illustrate the gaps.

## License
This project is open-source and available under the MIT License. See the [LICENSE](https://github.com/clerisy47/Compilance_Gap_Detector_and_Policy_Analyzer/blob/main/LICENSE) file for more information.
