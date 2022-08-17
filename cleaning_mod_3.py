## 0809
import re
import xlwt
import xlrd
import pandas as pd

data_path = "data/data.xls"  # 数据xls文件位置
save_path = "data/clean_data_mod_3.xls"  # 保存文件位置
class A:
    # 静态变量
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
    """
    写入数据
    :param sheet: 输入的sheet
    :param row: 行
    :param col: 列
    :param str_data: 写入内容
    :return:
    """
    sheet.write(row, col-1, str_data)

def cope():
    pass

def clean_1(str_data):
    """
    红线前面部分的全部删掉，但要保留红线部分的文本
    即修改需求例如只保留红线部分文本信息
    :param str_data:需要清洗的数据
    :return:清洗好的数据(str)
    """
    clea_data = re.sub(r"(O_FIG)[\s\S]*?(C_FIG)", "", str(str_data),flags=re.M)
    clea_data = re.sub(r"(O_TBL)[\s\S]*?(C_TBL)", "", str(clea_data),flags=re.M)
    clea_data = re.sub(r"(O_ST_ABS)([\s\S]*?(C_ST_ABS))", "", str(clea_data),flags=re.M)
    return clea_data

def clean_2_Delete(data):
    """
    两个单词连在一起了，并且在开头，删除即论文摘要的section标题
    :param data: 连在一起的两个单词
    :return: 后面的content
    """
    return data.group('retain')

def clean_2_AddSpaces(data):
    """
    两个单词连在一起了，并且在中间，在两个单词中间添加空格
    :param data: 连在一起的两个单词
    :return: 后面的content
    """
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
    """
    两个单词连在一起了（即论文摘要的section标题和后面的content连在一起了）
    我需要把他们分开或者删除section标题。
    :param str_data:需要清洗的数据
    :return:清洗好的数据
    """
    str_r = r"^([A-Z][a-z]+(?P<retain>[A-Z][a-z]+))(?= )" # 最前面两个单词连在一起了
    clea_data = re.sub(str_r, clean_2_Delete, str(str_data),flags=re.M)
    #在开头连在一起的两个单词
    # 以上洗掉了例如MethodsThis实现了MethodsThis-> This;

    str_r = r"^(?!\s)((?P<retain_1>[A-Z][a-z]+)(?P<retain_2>[A-Z][a-z]+))(?= )"  # 中间两个单词连在一起了
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data),flags=re.M)
    # 在中间连在一起的两个单词
    # 以上洗掉了例如Summary and ResultsWe实现了Summary and ResultsWe->Summary and Results We

    str_r = r"^(?!\s)((?P<retain_1>[A-Z\-]+)(?P<retain_2>[A-Z][a-z]+))(?= )"  # 中间两个单词连在一起了
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data),flags=re.M)
    # 在中间连在一起的两个单词
    # 以上洗掉了例如TOPLINE SUMMARYO_ST_ABSWhat实现了TOPLINE SUMMARYO_ST_ABS What

    str_r = r"(^[A-Z]+(?P<retain>[A-Z][a-z]+))(?= )"  # 最前面两个单词连在一起了（一个大写一个小写）
    clea_data = re.sub(str_r, clean_2_Delete, str(clea_data),flags=re.M)
    # 在中间连在一起的两个单词
    # 以上洗掉了例如IMPORTANCEHuman实现了IMPORTANCEHuman-> Human

    str_r = r"(^[a-z]+(?P<retain>[A-Z][a-z]+))(?= )"  # 最前面两个单词连在一起了（一个小写一个小写）
    clea_data = re.sub(str_r, clean_2_Delete, str(clea_data),flags=re.M)
    # 在中间连在一起的两个单词
    # 以上洗掉了例如objectiveThis实现了objectiveThis-> This

    str_r = r"(^(?P<retain_1>[A-Z][a-z]+)(?P<retain_2>[A-Z][\w]+))(?=[ -])"  # 最前面两个单词连在一起了（一个小写一个大写）
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data),flags=re.M)
    # 在中间连在一起的两个单词
    # 以上洗掉了例如BackgroundDNA实现了BackgroundDNA->Background DNA

    str_r = r"(^[\w]+(?P<retain>[A-Z][a-z]+))(?=[ -])"  # 最前面两个单词连在一起了（一个小写一个小写）
    clea_data = re.sub(str_r, clean_2_Delete, str(clea_data),flags=re.M)
    # 在中间连在一起的两个单词
    # 以上洗掉了例如objectiveThis实现了objectiveThis-> This

    str_r = r'^([\w\/]*_[\w\/]* )'
    clea_data = re.sub(str_r, "", str(clea_data),flags=re.M)
    # 以上洗掉了例如AO_SCPLOWBSTRACTC_SCPLOWO_ST_ABSBackgroundC_ST_A
    # # One Sentence SummaryLoss
    # str_r = r"^(?!\s)((?P<retain_1> [A-Z][a-z]+)(?P<retain_2>[A-Z][a-z]+))(?= )"  # 中间两个单词连在一起了
    # clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data), flags=re.M)
    str_r = r"^(?!\s)((?P<retain_1>[A-Z][a-z]+)(?P<retain_2>[A-Z]+))(?= )"  # 中间两个单词连在一起了
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data), flags=re.M)
    str_r = r"((?P<retain_1>\s[a-z]+)(?P<retain_2>[A-Z][a-z]+))(?= )"  # 中间两个单词连在一起了
    clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data), flags=re.M)

    ## #TODO 1）去掉每段开头的 “-” 2）去掉每段开头的空格
    str_r = r"^(\-\s)"
    clea_data = re.sub(str_r, "", str(clea_data),flags=re.M)

    # clea_data = re.sub("Author Summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Author summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("One sentence summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("One sentence summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("STATEMENT OF SIGNIFICANCE", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Results", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Key Points", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("One Sentence Summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Highlights", "Highlights ", str(clea_data), flags=re.M)
    clea_data = re.sub("Background/Purpose", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Materials and Methods", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Plain Language Summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Significance Statement", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Plain Language Summary", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("SUMMARY STATEMENT", "SUMMARY STATEMENT ", str(clea_data), flags=re.M)
    # clea_data = re.sub("One-Sentence Summary", "One-Sentence Summary ", str(clea_data), flags=re.M)
    clea_data = re.sub("Availability and Implementation", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Supplementary Information", "", str(clea_data), flags=re.M)
    clea_data = re.sub("In Brief", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Summary Paragraph", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("HIGHLIGHTS", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Statement of Significance", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Summary Statement", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Summary Paragraph", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("ABSTRACT/SUMMARY", "", str(clea_data), flags=re.M)
    clea_data = re.sub("Availability and implementation", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("MAIN CONCLUSIONS", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Impact Statement", "", str(clea_data), flags=re.M)
    # clea_data = re.sub("Conclusion and translational aspect", "", str(clea_data), flags=re.M)
    clea_data = re.sub("SalivaDirect", "SalivaDirect ", str(clea_data), flags=re.M)
    clea_data = re.sub("Older adults", "Older adults ", str(clea_data),flags=re.M)
    clea_data = re.sub("Abstract\/Keywords|Availability|\"|\(s\) and Measure\(s\)|Competing interest statement|\& AIM|STRENGTHS AND LIMITATIONS|National Institute of Allergy and Infectious Diseases|Materials and methods|and relevance |Methods and Analysis|Ethics and dissemination|Research design and methods|Ethics and Dissemination|\[\&ge\;\]|Study Design|Translational Significance|\/design|Background and Objectives|Backgrounds and aims|Abstract\/Summary|Methodology\/Principle|and discussion |Rationale and Goal|Impact statement|Abbreviated Abstract|Systematic review|RESEARCH IN CONTEXT|Future directions|INTRODUCTION|Background and Objective: |Of |Objectives: |MRC and NIHR|BACKGROUND|Abstract |Prospero registration number-|2012 ACM Subject ClassificationApplied computing  Computational genomics|AUTHOR |1\.|Open Research|Take Away|NEW \& Noteworthyo |PRISMA guidelines\.|STUDY DESIGN|SYNOPSIS\/PRECIS|Design settingparticipantsA|Primary Outcome|National Institute of AllergyInfectious Diseases|\[\-\&gt\;\]|Analysis of |NON\-TECHNICAL PARAGRAPH|AO_SCPLOWBSTRACTC_SCPLOW|Section 1|Section 2 |Section 3|Risk of BiasPEDro scaleNIH scale\.|Grant-in-Aid for JSPS Research Fellows\, 19J23020\.|Registration PROSPERO \(CRD42021230966\)|Data sources|Methods/Design|Trial registrationISRCTN12051706|Trial registrationPROSPERO IDCRD42021249818|\; |Limitation|French Ministries of SolidarityHealthResearchSanofi|FundingUnitaid|Strengthslimitations|Relevance|PROSPERO registration numberCRD42022310655|clincialtrials\.gov \(NCT04456153\)\.|Clinical Perspective|Aims/hypothesis|OBJECTIVES |DESIGN AND SETTING|PARTICIAPNTS |INTERVENTIONS|MAIN OUTCOME MEASURES|\?|ESWhat is already known about this topic\?|Research designmethods|Introduction:|Introduction|WHAT IS ALREADY KNOWN ON THIS TOPIC|Limitations|Analysis|EthicsDissemination|Main outcome measures |SettingEngland\.|Main outcome measures|Strengthslimitations of this study |Materialsmethods |INTRODUCTION |DISCUSSION |Study RegistrationNCT05366322|Measures|Clinicaltrials\.in\.th numberTCTR20211223001|Clinical Implications|Clinical Perspective|World Health Organisation|2012 ACM Subject ClassificationComputational genomics|How this study may affect research, practice, or policy|Outcome measures|Research in context Evidence before this study|Funding |Data Synthesis|Data Extraction|Data Sources|Study Selection|Background |Main Outcomes|Objective |Background: |Motivation: |Purpose: |SUMMARY Background |Introduction |Purpose|Background|Implications of all available evidence |Funding Source|Implications of all the available evidence |1Background1\.1 Abstract| and Discussion|Background |BACKGROUND |OBJECTIVE |METHODS|RESULTS|CONCLUSION |Objective|Motivation|\: |Translational Perspective|Strength of Evidence|Background / Aim of Rapid Review|Background and Objectives|WHAT IS KNOWN|TAKE-HOME MESSAGE|Methods","", str(clea_data),flags=re.M)

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

    # (.gov / ct2 / show / NCT03152864?term=ellen+frank & draw=2 & rank=3)
    # Trial registration numberClinicalTrials.gov identifier NCT05124171; EudraCT identifier 2021-004550-33
    # TRIAL REGISTRATIONClinicalTrials.gov IdentifierNCT03665857
    # Grant - in -Aid for JSPS Research Fellows, 19J23020.
    # Registration PROSPERO(CRD42021230966)
    # str_r = r"((?P<retain_1>[a-z][a-z]+)(?P<retain_2>[a-z][a-z]+))(?= )"  # 中间两个单词连在一起了
    # clea_data = re.sub(str_r, clean_2_AddSpaces, str(clea_data), flags=re.M)
    return clea_data

def clean_3(str_data):
    """
    把O_LI,C_LIO_LI，C_LI这三类标签删除，保留剩下的文本
    :param str_data:需要清洗的数据
    :return:清洗好的数据
    """
    clea_data = re.sub(r"LocationWorld|\{kappa\} |\{micro\}|\[\&le\;\]|\{circ\}|Table of contents graphic|Graphical TOC\/Abstract|Abstract Objectives: |O_SCPLOWLASTC_SCPLOW|O_TEXTBOX|\* |ARTICLE|O_LI|C_LIO_LI|C_LI|C_ST_ABSP|Table of Contents _DISPLAY|Graphical Abstract|Graphical abstract|C_TEXTBOX|GRAPHICAL ABSTRACT|_DISPLAY|Graphic Abstract|Contact:|Graphical summary|FundingUKHSA|GRAPHIC ABSTRACT|", "", str(str_data),flags=re.M)

    return clea_data

def clean_4(str_data):
    """
    删除有http超链以及电子邮箱。
    :param str_data:需要清洗的数据
    :return:清洗好的数据(str)
    """
    str_r = r"(?<=[ \.\,\n\(])http(.*?)(?=[ \.\,\n\)])|https://(.*?)(?=[ \.\,\n])" \
            r"|[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}" #网站和邮箱
    clea_data = re.sub(str_r, "", str(str_data),flags=re.M)
    return clea_data

def clean_5(str_data):
    """
    在前面需求完成之后，清洗掉可能会存在没有内容的空行。
    :param str_data:需要清洗的数据
    :return:清洗好的数据(str)
    """
    str_r=r"(\n){2,}"
    clea_data = re.sub(str_r, "\n", str(str_data))
    return clea_data

def cleaning_data( str_data ):
    """
    清洗数据
    :param str_data: 需要清洗的数据
    :return: 清洗好的数据
    """
    clea_data=clean_1(str_data)
    clea_data=clean_3(clea_data)
    clea_data=clean_4(clea_data)
    clea_data=clean_5(clea_data)
    clea_data=clean_2(clea_data)

    # 对清洗好的数据进行监视
    str_r = r"^([\w\/]*_[\w\/]* )" #筛选监视数据的正则
    A.a += 1
    if re.findall(str_r,str(clea_data)) != []:
        print(A.a)
        print(re.findall(str_r,str(clea_data)))
        print(clea_data+"\n\n\n")

    return clea_data

def main():
    data_sheet1_abstract = read(data_path, 1, 4)  # 读取第1个sheet的第4列数据
    encoding_write = xlwt.Workbook(encoding='utf-8')  # 设置表格编码格式
    sheet2 = encoding_write.add_sheet(u'clean data')  # 设置新增sheet页名称
    for i in range(1, len(data_sheet1_abstract)):
        write(sheet2, i, 1, cleaning_data(data_sheet1_abstract[i]))
    #     write(sheet2, i, 1,cleaning_data(data_sheet1_abstract[i]))
        # 写入2个sheet的第i行第4列清洗后数据

    encoding_write.save(save_path)  # 将清洗后的数据保存在save_path路径下

if __name__ == '__main__':
    main()
    #
    clean_data_abs = pd.read_excel(io='data/clean_data_mod_3.xls')
    clean_data_abs.columns = ['abstract']
    #
    original_data = pd.read_excel(io='data/data.xls',dtype={"id":str,"title":str,"posted":str})
    new_data = pd.concat([original_data['id'], original_data['title'], original_data['posted'], clean_data_abs], axis=1)
    new_data.to_csv('data/cleaned_data_mod_3.csv', index=False,encoding='utf-8',index_label=False)