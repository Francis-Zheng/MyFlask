from flask import Flask, request
from jpype import *
from mySegment import *
import pymongo
from bson import ObjectId,json_util



app = Flask(__name__, static_folder='static/', static_url_path='')

segment_test = mySegment()
mongodbAddr = 'mongodb://xxx.xxx.xxx.xxx:27017/'

myclient = pymongo.MongoClient(mongodbAddr)
guangmingNewsDB = myclient['guangmingNews']
wordDoc = guangmingNewsDB['word']
urlDoc = guangmingNewsDB['url']

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    add_info = "empty"
    res = "我不明白你的意思"
    a = request
    print(request)
    if request.method == 'GET':
        str_in = request.args.get("queryFromUser")
    else:
        str_in = request.form.get("queryFromUser")  #这里名字改了之后，前段部分也要改，如果名字一致还是报错，就需要清理浏览器缓存
    print("this is query:")
    print(str_in)

    #对查询语句进行分词
    segment_list = segment_test.segmentFilter(str_in)
    if len(segment_list) != 1:  #按多个关键词搜索
        test_words = segment_list
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
        test_aggregate_result = wordDoc.aggregate(test_pipline) #mongodb聚合查询
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
            urlId = each
            tmp = urlDoc.find_one({"_id": ObjectId(urlId)})
            tmp["_id"] = tmp["_id"].__str__()
            url_result.append(tmp)
        print(json_util.dumps(url_result))
        myclient.close()
        return json_util.dumps(url_result)
    else:
        #按单个关键词查询
        word = "".join(segment_list)
        query_result = wordDoc.find_one({"_id": word})
        if not query_result:
            return 0
        print(query_result["count"])

        sort_result = segment_test.sort_by_value(query_result["count"])
        url_result = []
        for each in sort_result:
            #print(each)
            urlId = each
            tmp = urlDoc.find_one({"_id": ObjectId(urlId)})
            tmp["_id"] = tmp["_id"].__str__()
            url_result.append(tmp)
            #print(url_result)

        print(json_util.dumps(url_result))

        myclient.close()
        return json_util.dumps(url_result)
