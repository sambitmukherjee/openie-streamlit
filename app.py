# pip3 install pyopenie
# pip3 install streamlit

import numpy as np
import pandas as pd
from pyopenie import OpenIE5
import streamlit as st

@st.cache
def get_extractor(url):
	extractor = OpenIE5(url)
	return extractor

@st.cache
def get_extractions(text):
	extractions = extractor.extract(text)
	return extractions

@st.cache
def json_to_df(json):
	confidence = []
	arg1 = []
	rel = []
	arg2 = []
	context = []
	negated = []
	passive = []
	for i in range(len(json)):
		if len(json[i]["extraction"]["arg2s"]) > 0:
			for j in range(len(json[i]["extraction"]["arg2s"])):
				confidence.append(json[i]["confidence"])
				arg1.append(json[i]["extraction"]["arg1"]["text"])
				rel.append(json[i]["extraction"]["rel"]["text"])			
				arg2.append(json[i]["extraction"]["arg2s"][j]["text"])
				if json[i]["extraction"]["context"] is not None:
					context.append(json[i]["extraction"]["context"]["text"])
				else:
					context.append(None)
				negated.append(json[i]["extraction"]["negated"])
				passive.append(json[i]["extraction"]["passive"])
		else:
			confidence.append(json[i]["confidence"])
			arg1.append(json[i]["extraction"]["arg1"]["text"])
			rel.append(json[i]["extraction"]["rel"]["text"])			
			arg2.append(None)
			if json[i]["extraction"]["context"] is not None:
				context.append(json[i]["extraction"]["context"]["text"])
			else:
				context.append(None)
			negated.append(json[i]["extraction"]["negated"])
			passive.append(json[i]["extraction"]["passive"])

	df = pd.DataFrame({
		'Confidence': confidence,
		'Argument 1': arg1,
		'Relation': rel,
		'Argument 2': arg2,
		'Context': context,
		'Negated': negated,
		'Passive': passive
	})
	df.drop_duplicates(inplace=True)
	df.sort_values(by='Confidence', ascending=False, inplace=True, ignore_index=True)
	return df

@st.cache
def radio_format_func(raw_option):
	if raw_option == "example_sentence":
		return "Select an example sentence."
	else:
		return "Type your own sentence."

st.title("Relation Extraction Using OpenIE")

chosen_mode = st.radio(
	label="Choose mode:",
	options=("example_sentence", "own_sentence"),
	format_func=radio_format_func,
	key="radio_key"
)

example_sentences = [
	"The food was delicious, but the service was too slow.",
	"My mother thought the movie wasn't logical.",
	"Jack and Jill visited India and South Korea.",
	"The U.S. president Barack Obama gave his speech on Tuesday and Wednesday to thousands of people.",
	"Some people say Barack Obama was born in Kenya.",
	"Barack Obama is 6 feet tall.",
	"James Valley has 5 sq kms of fruit orchards.",
	"Everything about the new Yamaha MT15 is good, except the fact that dual-channel ABS is missing.",
	"The Kia Sonet looks good but actually sucks.",
	"If you thought the Kia Sonet drives well, you would be wrong.",
	"Tom painted the entire fence.",
	"The entire fence was painted by Tom.",
	"What bullshit!"
]

with st.form(key="form_key"):
	if chosen_mode == "example_sentence":
		sentence = st.selectbox(
			label="Sentence:",
			options=example_sentences,
			key="selectbox_key"
		)
	else:
		sentence = st.text_area(
			label="Sentence:",
			key="text_area_key"
		)
	submitted = st.form_submit_button(label="Extract")
	if submitted:
		st.write('> "' + sentence + '"')

		extractor = get_extractor('http://3.237.106.170:8000')
		extractions_json = get_extractions(sentence)
		extractions_df = json_to_df(extractions_json)

		with st.expander(label='Table', expanded=True):
			st.table(extractions_df)

		with st.expander(label='JSON'):
			st.write(extractions_json)

"""
---

**References:**

1. [Open IE](https://github.com/dair-iitd/OpenIE-standalone)
2. [pyopenie](https://github.com/vaibhavad/python-wrapper-OpenIE5)

"""
