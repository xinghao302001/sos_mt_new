# Title
## 1. Current work
### Raw Texts Preprocessing

```
Step 1. Clean Texts
		- cleaning_mod2.py: cleaning the raw texts with removing section names.
		- cleaning_mod3.py: cleaning the raw texts, but keeping some section names.
		
Step 2. Coreference Resolution
		- corefResolver.py: return the coref-resolved texts
			-- _eval_corefs: detect the coreferences in the texts.
			-- _replace: replace the word detected by _eval_corefs functions.
			-- _rebuild_contents: Utilizing the _replace function to reconstruct the 									  texts.
			-- get_resolved_texts: Combining three functions mentioned above to get the 								    coref-resolved texts.
			
Step 3: Split paragraph-level abstracts to sentence-level abstracts:
			-- nltk.sent_tokenize(option 1)
			-- import spacy
			   nlp = spacy.load(..)
			   doc = nlp(..)
			   sents = doc.sents

Step 4: Select sents for each abstracts that we need:
		1. Rule-based
		   -- selectSciStatementSents.py: define some functions and rules as tools for 						   dataSelection.py.
		    -- dataSelection.py: return the non_sci_statement_sents and 												 sci_statemnt_sents.
			-- SelectBioSentsScispacy.py: return bio_sci_statement_sents and n													   non_sci_statement_sents by using Scispacy.
					Or -- SelectBioSentsBERN2.py: return bio_sci_statement_sents and n													   non_sci_statement_sents by using 													  Scispacy.
```



### MetaMap/UMLS mapping

```
-- MetaMap.py: a wrapper used to get the mapping results when input one sentences  
-- datapreprocesForMetaMap_and_getMMres.py: Utlizing MetaMap.py tools and remove some 	  	 characters that UMLS can not recognize. Finally, store the mapping results in .json file.
```



### **Handling the Mapping results from the MetaMap**

```
Step 1: Extract the Utttext(a sent) from MetaMap results.
Step 2: Extract the mapped entities and its semTypes from the MetaMap results.


--- the steps mentioned above are achieved in combination_svo_and_metamap.py file with the function of handleMMres
```



### Get triplets w/wo semtypes from MetaMap
```
Extract SVOS for each simplified sents combing the MetaMap results.
		-- combination_svo_and_metamap.py 
			--- handleMMres: Extract the Utttext(a sent) from MetaMap results.
							  Extract the mapped entities and its semTypes from the									  MetaMap results.
		    --- getSVOs_w_sem_and_wo_sem: Extract the svo w/wo semtypes based on MetaMap 											results based on StanfordCoreNLP Tools.


```



### **Evaluation**
```
1. Evaluate whether the selected sentences belongs to the specific domain.
    -- Utilizing the results of the dataSelection.py as training to fine-tune a pre-trained LM. Then using this fine-tuned model to distinguish whether one sentence is sci statement or not and to extract the sci statement sentence. 

2. Evaluate whether the extracted triplets meets our requirements.
```


## 2. Failed attempts and why

### Extract SVOs

```
	-- Methods 1: using rule-based(syntax parsing) to extract svos directly.
		--- Failed Reason: We need more self-defined rules to extract a sentence when 								the sentence includes more complex components.
	-- Methods 2: using ClauseIE to extract svos directly.
		--- Failed Reason: Although this method could extract svos that are in clause 								sentences. But other important information of a sentence is 							lost,such as numerical information or time information.
```

##  3. Related work

### SeqKG

```
  -- It is a tool for open-domain triplets extraction.
  -- It combines rule-based and deeplearning methods to extract triplets and to filter some wrong triplets because of its syntax.
  -- But it could not be direly applied in specifical domain. The reason is that some methods for handeling biomedical texts are different from the open-domain texts.
```

### KGen

```
   -- It is a tool which can extract triplets focusing on AD-dieases domain.
   -- It utlizes most of KGC techniques that we could use them as a reference and baseline.
   -- But this work could not filter some triplets that are wrong or not required.
```





##  TODO

```
1. Simplified sents for one long sentence(e.g. clauses sents)
		-- sentSimpWrapper.py: output the simplified results into .json file for 									   handlingSimplifiedSents.py
		

		-- handlingSimplifiedSents.py: return the results in sentence form based on the 						       results from sentSimpWrapper.py
2. How to define the evaluation model or train the model.
3. Reducing such self-defined stopwords
```





