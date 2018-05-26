from judgement import JudgementsCollector, Judgement, get_judgement


collector = JudgementsCollector(text="OLX")
collector.find_judgements()  # find all judgements which contain 'OLX' string

olx_courts = collector.courts()  # get a list of courts
olx_cases = collector.cases()  # get a list of law cases

documents = collector.ids()  # get a list of all ids of documents

decisions_list = []

for id in documents:
    decisions_list.append(get_judgement(id))

# Now decisions list is a list which contains Judgement objects

jud = decisions_list[0]
print(jud)

print(jud.keywords())
assert(jud.includes("OLX") == True)  # it definitely should include the "OLX" string

jud_codes = jud.codes()
print(jud.articles(jud_codes[0]))