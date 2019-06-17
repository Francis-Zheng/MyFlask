#!/usr/bin/python3

import pymongo
from bson import ObjectId, json_util

mongodbAddr = 'mongodb://xxx.xxx.xxx.xxx:27017/'
myclient = pymongo.MongoClient(mongodbAddr)

dblist = myclient.list_database_names()
print(dblist)

guangmingNewsDB = myclient['guangmingNews']
wordDoc = guangmingNewsDB['word']
guangmingnewsDoc = guangmingNewsDB['guangmingnews']
urlDoc = guangmingNewsDB['url']


# 按照词频反向排序
def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0, len(backitems))]


word = "隐私"
queryById = {"_id": word}
query_result = wordDoc.find_one(queryById)
print(query_result)
print("dict query_result[\"count\"]: ")
print(query_result["count"])

sort_result = sort_by_value(query_result["count"])
print("list sort_result: ")
print(sort_result)
for each in sort_result:
    print(each)
# for each in query_result["count"]:
#    print(each)

urlId = ObjectId("5d0044a8fe8b3e9bedd9a81e")
queryById = {"_id": urlId}
query_result = guangmingnewsDoc.find_one(queryById)
print("query_result: " + query_result["article_url"])

url_result = []
urlId = each
url_result.append(urlDoc.find_one({"_id": ObjectId(urlId)}))
print(url_result)
print(json_util.dumps(url_result))

tmp = urlDoc.find_one({"_id": ObjectId(urlId)})
tmp["_id"] = tmp["_id"].__str__()
print(tmp)

test1 = urlDoc.find_one(
    {
        "_id": {
            "$eq": ObjectId("5d04f9047bb9c26559c1bf0c")
        }
    })
print(json_util.dumps(test1))


test_words = ['陈伟霆', '钟汉良']
search_array = []
for each in test_words:
    search_array.append(dict(_id=each))

print(search_array)

test_pipline = [
    {
        '$lookup': {
            'from': 'word',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'aggregate'
        }},
    {
        '$match': {
            '$or': search_array
        }
    },

    {
        '$limit': 10
    }
]
test_aggregate_result = wordDoc.aggregate(test_pipline)
intersection_result = []
i = 0
for each in test_aggregate_result:
    if i == 0:
        intersection_result = list(each['count'].keys())
    print(each['count'])
    intersection_result = list(set(intersection_result).intersection(set(each['count'].keys())))
    i = i + 1

print("交集: ")
print(intersection_result)
url_result = []
for each in intersection_result:
    # print(each)
    urlId = each
    tmp = urlDoc.find_one({"_id": ObjectId(urlId)})
    tmp["_id"] = tmp["_id"].__str__()
    url_result.append(tmp)
    # print(url_result)
print(json_util.dumps(url_result))

myclient.close()
