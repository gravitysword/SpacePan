a = '''oid: 1153958824
type: 1
message: 水军test
plat: 1
at_name_to_mid: {}
pictures: []
has_vote_option: true'''

i = 1
re = ""
a = a.replace(" ","")
for x in a.split("\n"):
    re += "\""+x.replace(":","\":\"",1)+"\",\n"
print(re)








