import re
import xlwt
import xlrd
import pandas as pd

data_path = "data/data.xls"
save_path = "data/clean_data_mod_2.xls"
class A:
    a = 0

def read(data_path, num_sheet , num_col):
    """
    读取数据
    :param data_path: xls文件位置
    :param num_sheet: 第几个sheet
    :param num_col: 第几列数据
    :return: 队列
    """
    data = xlrd.open_workbook(data_path)
    table = data.sheets()[num_sheet-1]

    return table.col_values(num_col-1)

def write(sheet, row, col, str_data):

    sheet.write(row, col-1, str_data)

def cope():
    pass

def clean_1(str_data):

    clea_data = re.sub(r"(O_FIG)[\s\S]*?(C_FIG)", "", str(str_data),flags=re.M)
    clea_data = re.sub(r"(O_TBL)[\s\S]*?(C_TBL)", "", str(clea_data),flags=re.M)
    clea_data = re.sub(r"(O_ST_ABS)([\s\S]*?(C_ST_ABS))", "", str(clea_data),flags=re.M)
    return clea_data

def clean_2_Delete(data):

    return data.group('retain')

def clean_2_AddSpaces(data):

    return data.group("retain_1")+" "+data.group('retain_2')

def dashrepl(matchobj):
    if matchobj.group(0) == '- ':
        return ''
    else:
        return '-'
def andrepl(matchobj):
    if matchobj.group(0) == ' and ':
        return ''
    else:
        return '-'
def clean_2(str_data):

    str_r = r"^([A-Z][a-z]+(?P<retain>[A-Z][a-z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_Delete, str(str_data),flags=re.M)


    str_r = r"^(?!\s)((?P<retain_1>[A-Z][a-z]+)(?P<retain_2>[A-Z][a-z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data),flags=re.M)


    str_r = r"^(?!\s)((?P<retain_1>[A-Z\-]+)(?P<retain_2>[A-Z][a-z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data),flags=re.M)


    str_r = r"(^[A-Z]+(?P<retain>[A-Z][a-z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_Delete, str(clea_data),flags=re.M)


    str_r = r"(^[a-z]+(?P<retain>[A-Z][a-z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_Delete, str(clea_data),flags=re.M)


    str_r = r"(^(?P<retain_1>[A-Z][a-z]+)(?P<retain_2>[A-Z][\w]+))(?=[ -])"
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data),flags=re.M)


    str_r = r"(^[\w]+(?P<retain>[A-Z][a-z]+))(?=[ -])"
    clea_data = re.sub(str_r, clean_2_Delete, str(clea_data),flags=re.M)


    str_r = r'^([\w\/]*_[\w\/]* )'
    clea_data = re.sub(str_r, "", str(clea_data),flags=re.M)

    str_r = r"^(?!\s)((?P<retain_1>[A-Z][a-z]+)(?P<retain_2>[A-Z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data), flags=re.M)
    str_r = r"((?P<retain_1>\s[a-z]+)(?P<retain_2>[A-Z][a-z]+))(?= )"
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data), flags=re.M)


    str_r = r"^(\-\s)"
    clea_data = re.sub(str_r, "", str(clea_data),flags=re.M)

    clea_data = re.sub("Author Summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Author summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("One sentence summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("SIGNIFICANCE STATEMENT", "", str(clea_data), flags=re.M)
    clea_data = re.sub("STATEMENT OF SIGNIFICANCE", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Results", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Key Points", "", str(clea_data), flags=re.M)
    clea_data = re.sub("One Sentence Summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Highlights", "Highlights ", str(clea_data), flags=re.M)
    clea_data = re.sub("Background/Purpose", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Materials and Methods", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Plain Language Summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Significance Statement", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Plain Language Summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("SUMMARY STATEMENT", "SUMMARY STATEMENT ", str(clea_data), flags=re.M)
    clea_data = re.sub("One-Sentence Summary", "One-Sentence Summary ", str(clea_data), flags=re.M)
    clea_data = re.sub("Availability and Implementation", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Supplementary Information", "", str(clea_data), flags=re.M)
    clea_data = re.sub("In Brief", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Summary Paragraph", "", str(clea_data), flags=re.M)
    clea_data = re.sub("HIGHLIGHTS", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Statement of Significance", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Summary Statement", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Simple Summary", "", str(clea_data), flags=re.M)
    clea_data = re.sub("ABSTRACT/SUMMARY", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Availability and implementation", "", str(clea_data), flags=re.M)
    clea_data = re.sub("MAIN CONCLUSIONS", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Impact Statement", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Conclusion and translational aspect", "", str(clea_data), flags=re.M)
    clea_data = re.sub("SalivaDirect", "SalivaDirect ", str(clea_data), flags=re.M)
    clea_data = re.sub("Older adults", "Older adults ", str(clea_data),flags=re.M)
    clea_data = re.sub("Availability|\"|\(s\) and Measure\(s\)|Competing interest statement|statement |\& AIM|STRENGTHS AND LIMITATIONS|National Institute of Allergy and Infectious Diseases|Materials and methods|Key points- |Strengths and limitations of the study- |and relevance |Methods and Analysis|Ethics and dissemination|Research design and methods|Ethics and Dissemination|\[\&ge\;\]|Study Design|KEY MESSAGES|BRIEF COMMENTARY|Translational Significance|\/design|and conclusions |Background and Objectives|Conclusions and Implications|Significance |Backgrounds and aims|Abstract\/Summary|Summary|What New Information Does This Article Contribute|Novelty and Significance|Methodology\/Principle|\/Significance|HIGHTLIGHTS|STATEMENT |and discussion |In brief|Rationale and Goal|Impact statement|Abbreviated Abstract|Systematic review|RESEARCH IN CONTEXT|Future directions|Highlights |SIGNIFICANCE |Highlights - |INTRODUCTION|Background and Objective: |and conclusion |Of |Objectives: |MRC and NIHR|Conclusions and Relevance|Discussion and Conclusion|BACKGROUND|Conclusions and Significance|Abstract |Prospero registration number-| Summary|Summary statement |Statement of Contribution|2012 ACM Subject ClassificationApplied computing  Computational genomics|Summary sentence |AUTHOR |1\.|Open Research|Significance statement|Take Away|NEW \& Noteworthyo |What This Study Adds|Whats Known on this Subject|Article Summary|PRISMA guidelines\.|STUDY DESIGN|SYNOPSIS\/PRECIS|One-sentence summary|CONCLUSIONS|Design settingparticipantsA|Primary Outcome|National Institute of AllergyInfectious Diseases|\[\-\&gt\;\]|Analysis of |NON\-TECHNICAL PARAGRAPH|AO_SCPLOWBSTRACTC_SCPLOW|What is New|Section 1|Section 2 |Section 3|Risk of BiasPEDro scaleNIH scale\.|Grant-in-Aid for JSPS Research Fellows\, 19J23020\.|KEY POINTS|Registration PROSPERO \(CRD42021230966\)|Data sources|Methods/Design|Trial registrationISRCTN12051706|Trial registrationPROSPERO IDCRD42021249818|\; |Limitation|French Ministries of SolidarityHealthResearchSanofi|FundingUnitaid|Strengthslimitations|Relevance|PROSPERO registration numberCRD42022310655|Strengthslimitations of this study |clincialtrials\.gov \(NCT04456153\)\.|Clinical Perspective|Aims/hypothesis|OBJECTIVES |DESIGN AND SETTING|PARTICIAPNTS |INTERVENTIONS|MAIN OUTCOME MEASURES|\?|ESWhat is already known about this topic\?|One-Sentence Summary |Research designmethods|Significance of this study |Introduction:|Introduction|WHAT IS ALREADY KNOWN ON THIS TOPIC|WHAT THIS STUDY ADDS|Limitations|Analysis|Strengthslimitations of this trialStrengths|EthicsDissemination|Significance statement |Main outcome measures |SettingEngland\.|Main outcome measures|Strengthslimitations of this study |Materialsmethods |INTRODUCTION |DISCUSSION |Study RegistrationNCT05366322|Measures|Clinicaltrials\.in\.th numberTCTR20211223001|Clinical Implications|Clinical PerspectiveWhat is New\?|World Health Organisation|2012 ACM Subject ClassificationComputational genomics|How this study may affect research, practice, or policy|What this study adds|Outcome measures|Strengthslimitations of this study |Key Messages|Added value of this study|Research in context Evidence before this study|Funding |Summary box|Discussion|Data Synthesis|Data Extraction|Data Sources|Study Selection|Background |Findings|Main Outcomes|Importance |Objective |Background: |Motivation: |Purpose: |SUMMARY Background |Introduction |Purpose|Background|CONCLUSIONS |Implications of all available evidence |Research in Context|Funding Source|Implications of all the available evidence |strengths and limitations of this study |1Background1\.1 Abstract| and Discussion|Background |BACKGROUND |OBJECTIVE |METHODS|RESULTS|CONCLUSION |Objective|Motivation|\: |Key Points |Importance of the Study|Discussion and conclusions |Author contributions|Key points |Significance Statement |IMPORTANCE |Brief Summary|What is already known about this subject\?|What are the new findings\?|SUMMARY BOX|Results|SUMMARY|Importance|Conclusions|Translational Perspective|Strength of Evidence|Background / Aim of Rapid Review|Key Findings|Summary of findings|AUTHOR SUMMARY |Summary paragraph|Background and Objectives|s and Implications|Data Summary|WHAT IS KNOWN|WHAT IS NEW HERE|Interpretation|TAKE-HOME MESSAGE|Methods|Conclusion","", str(clea_data),flags=re.M)

    clea_data = re.sub(r"^(\s+|\(\)|\([1-9]\)\s)","",str(clea_data),flags=re.M)
    clea_data = re.sub(r"^(Availability|Pre-registrationSeeaspredicted)\.([a-z]|[A-Z]|\.|/|[0-9]||\/|\,|\_|\(|\)|\#)*", "", str(clea_data), flags=re.M)
    clea_data = re.sub(r"^(TRIAL|Trial)\s([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_)*", "", str(clea_data), flags=re.M)
    clea_data = re.sub(r"^Clinical\s([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\))*", "", str(clea_data), flags=re.M)
    clea_data = re.sub(r"Clinical\sTrial\sRegistration([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\)|\#)*", "", str(clea_data), flags=re.M)
    clea_data = re.sub(r"^Supplementary\sinformation\s([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\)|\#)*", "",
                       str(clea_data), flags=re.M)
    clea_data = re.sub(r"^2012\sACM\s([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\)|\#)*", "",
                       str(clea_data), flags=re.M)
    clea_data = re.sub(r"^(Study registration|Snpdragon|EPFL COVID|registrationPROSPERO|PROSPERO Registration|Systematic review registration)([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\)|\#)*", "",
                       str(clea_data), flags=re.M)
    clea_data = re.sub(r"^\#([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\)|\#)*","",str(clea_data), flags=re.M)
    clea_data = re.sub(r"^Study registration([a-z]|[A-Z]|\.|/|[0-9]|\s|\/|\,|\_|\(|\)|\#)*", "", str(clea_data), flags=re.M)
    clea_data = re.sub(r"\n", " ", str(clea_data), flags=re.M)

    return clea_data

def clean_3(str_data):

    clea_data = re.sub(r"LocationWorld|\{kappa\} |\{micro\}|\[\&le\;\]|\{circ\}|Table of contents graphic|Graphical TOC\/Abstract|Abstract Objectives: |O_SCPLOWLASTC_SCPLOW|O_TEXTBOX|\* |ARTICLE|O_LI|C_LIO_LI|C_LI|C_ST_ABSP|Table of Contents _DISPLAY|Graphical Abstract|Graphical abstract|C_TEXTBOX|GRAPHICAL ABSTRACT|_DISPLAY|Graphic Abstract|Contact:|Graphical summary|FundingUKHSA|GRAPHIC ABSTRACT|", "", str(str_data),flags=re.M)

    return clea_data

def clean_4(str_data):

    str_r = r"(?<=[ \.\,\n\(])http(.*?)(?=[ \.\,\n\)])|https://(.*?)(?=[ \.\,\n])" \
            r"|[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}" #网站和邮箱
    clea_data = re.sub(str_r, "", str(str_data),flags=re.M)
    return clea_data

def clean_5(str_data):

    str_r=r"(\n){2,}"
    clea_data = re.sub(str_r, "\n", str(str_data))
    return clea_data

def cleaning_data( str_data ):

    clea_data=clean_1(str_data)
    clea_data=clean_3(clea_data)
    clea_data=clean_4(clea_data)
    clea_data=clean_5(clea_data)
    clea_data=clean_2(clea_data)

    str_r = r"^([\w\/]*_[\w\/]* )"
    A.a += 1
    if re.findall(str_r,str(clea_data)) != []:
        print(A.a)
        print(re.findall(str_r,str(clea_data)))
        print(clea_data+"\n\n\n")

    return clea_data

def main():
    data_sheet1_abstract = read(data_path, 1, 4)
    encoding_write = xlwt.Workbook(encoding='utf-8')
    sheet2 = encoding_write.add_sheet(u'clean data')
    for i in range(1, len(data_sheet1_abstract)):
        write(sheet2, i, 1, cleaning_data(data_sheet1_abstract[i]))


    encoding_write.save(save_path)

if __name__ == '__main__':
    main()
    #
    clean_data_abs = pd.read_excel(io='data/clean_data_mod_2.xls',header=None)
    clean_data_abs.columns = ['abstract']

    original_data = pd.read_excel(io='data/data.xls',dtype={"id":str,"title":str,"posted":str})
    new_data = pd.concat([original_data['id'], original_data['title'], original_data['posted'], clean_data_abs], axis=1)
    new_data.to_csv('data/cleaned_data_mod_2.csv', index=False,encoding='utf-8',index_label=False)