from flask import Flask , request
import requests
import json
import itertools
from operator import itemgetter

app = Flask(__name__)

def read_data_blog_comments():
    r = requests.get('https://jsonplaceholder.typicode.com/comments')
    return json.dumps(r.json() )

def get_blogpost(post_id):
    r = requests.get('https://jsonplaceholder.typicode.com/posts')
    return json.dumps(r.json())

@app.route('/api/v1/top_post/<int:n>', methods=['GET'])
def list_topblog_post(n):
    #get all the comments and then group them by post-id
    comments =  json.loads(  read_data_blog_comments() )
    comments = sorted(comments, key=itemgetter('postId') )
    blog_post_comments = []

    #count the comments per <postId>
    for key, value in itertools.groupby(comments, key=itemgetter('postId')):
        print(key)
        blog_info = {'post_id':0,'post_title':'','post_body':'','total_number_of_comments':0}
        j=0
        for i in value:
            j +=1
        blog_info['post_id'] = key
        r = json.loads( get_blogpost( int(key) ) )    
        if r:
            blog_info['post_title'] = r[0]['title']
            blog_info['post_body']  = r[0]['body']      
        else:
            blog_info['post_title'] = 'Err'
            blog_info['post_body']  = 'Err'
        blog_info['total_number_of_comments']=j
        blog_post_comments.append( blog_info )

    #print(blog_post_comments)
    #sort according to the total numbers of comments
    blog_post_comments = sorted(blog_post_comments , key=itemgetter('total_number_of_comments'))
    result = []

    #print the top <n> post
    for i in range(0,n):
        result.append(blog_post_comments[i])
    return json.dumps(result)


@app.route('/api/v1/post_comment_filter', methods=['GET'])
def post_comment_filter():
    query_parameters = request.args

    filter_key = query_parameters.get('filter_key')
    filter_value = query_parameters.get('filter_value')

    comments = json.loads(  read_data_blog_comments())

    if (filter_key in ['postId','id']):
       keyValList = [int(filter_value)]
    else:
       keyValList = [filter_value]
    print(filter_key,filter_value)
    expectedResult = [d for d in comments if d[filter_key] in keyValList]
    #print(expectedResult)
    return json.dumps(expectedResult)      


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
